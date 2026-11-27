#!/usr/bin/env python3
# nb_core.py — the engine behind nas_backup.sh / nas_backup_nightly.sh / nas_backup_watch.sh.
#
# WHAT IT IS (WED-170, Kam 2026-11-27 12:03): a NIGHTLY, STAGGERED, COPY-ONLY backup of one coordinator seat's
# folder and its working projects to the DEV-Working NAS, with next-night catch-up and a three-day flag.
#
# WHAT IT GUARANTEES, and what it does NOT (named, per 2026-09-08_a-safety-claim-names-the-property-it-checked):
#   - COPY ONLY. The source drive is only ever read. On the NAS nothing is deleted and nothing is overwritten in
#     place: a file that changed is first moved by the engine into versions/<run stamp>/ (rsync --backup
#     --backup-dir), then the new copy lands. The rsync argv is built here and checked for forbidden flags
#     before every call; there is no code path that passes a deletion flag.
#   - A seat writes ONLY inside <NAS>/<its own client>/<Seat>/nightly-backup/. The path is built from the resolved
#     seat and a hard-coded allow-list (SEATS below); a conf file can narrow it, never widen it.
#   - SECRETS never travel: 4_Credentials/, 3_Access_Keys/ and secret-shaped names are excluded by a fixed list
#     that no conf can shorten, and the engine's own log is re-read for any such name afterwards.
#   - Exit 0 is not success. A run is GOOD only when every in-scope source file, as listed at the start of the
#     run, is observed at the destination with the same size (or is proven to have changed or vanished at the
#     source during the run), the engine's log holds no deleting line, and a sha256 sample agrees.
#   - NOT covered: .git directories (see README: repos travel by git push; unpushed commits are NOT in this
#     backup); symlinks are RECORDED in the manifest, not created on the NAS; a secret inside an ordinary-named
#     file cannot be detected; files that exist only on the NAS stay there forever.
#
# WHY IT DOES NOT TRUST FILE TIMES ON THE NAS (measured 2026-11-27): on the same NAS box's Backup share the armed
# nas_push leg shows every file as changed-in-time every night (128,421 of 128,421 lines `>f..t......` on
# 2026-11-26; mirror CLAUDE.md mtime = the copy time, not the source's), so an engine that decides by
# size+mtime re-copies everything nightly, and with --backup would version everything nightly. Here the decision
# is made in this file: absent at destination, size differs, or the source's own (size, mtime, ctime) differs
# from the local index AND the sha256 differs. rsync is only the transport for an explicit --files-from list.
#
# Python 3.9-compatible, standard library only. Never discards stderr. No `rm`: a released lock is MOVED aside.
import datetime
import fnmatch
import hashlib
import json
import os
import random
import shlex
import signal
import sqlite3
import subprocess
import sys
import time
import unicodedata

SCHEMA = 1
LANE = os.path.dirname(os.path.realpath(__file__))
REAL_NAS_ROOT = "/Volumes/DEV-Working"
BACKUP_FOLDER = "nightly-backup"
FLAG_AFTER_HOURS = 72

# ── THE ALLOW-LIST. A seat may only ever write inside these client folders, as <NAS>/<Client>/<SeatCap>/. ──────
# forbid = path components (compared case-folded) that may never appear in one of the seat's SOURCE paths.
# other_seat_names = basename globs excluded at any depth INSIDE THE SEAT'S OWN TREE: another seat's material
# that lives in the shared repo (the WEDNESDAY tree carries tuesday/ and friday/ folders). Not applied to project
# folders: there the same globs hit library files (a date library's "nextFriday.js").
# other_client_names = basename globs excluded at any depth in EVERY set: another client's material.
SEATS = {
    "wednesday": {
        "cap": "Wednesday",
        "clients": ["Secuura", "General"],
        "forbid": ["datasec", "tuesday", "friday"],
        "other_seat_names": ["*[Tt]uesday*", "*TUESDAY*", "*[Ff]riday*", "*FRIDAY*"],
        "other_client_names": ["*[Dd]atasec*", "*DATASEC*"],
    },
    "tuesday": {
        "cap": "Tuesday",
        "clients": ["Datasec"],
        "forbid": ["secuura", "friday"],
        "other_seat_names": ["*[Ff]riday*", "*FRIDAY*"],
        "other_client_names": ["*[Ss]ecuura*", "*SECUURA*"],
    },
    "friday": {
        "cap": "Friday",
        "clients": ["General"],
        "forbid": [],
        "other_seat_names": [],
        "other_client_names": [],
    },
}

# ── FIXED EXCLUSIONS (basename globs, matched case-sensitively against EVERY path component). ──────────────────
# A conf can ADD names (exclude_name=) and anchored paths (exclude_path=); it cannot remove one of these.
EXCLUDES = [
    ("secret", ["4_Credentials", "3_Access_Keys", ".env", ".env.*", "*.env", "*.pem", "*.key", "*.p12", "*.pfx",
                "*.keystore", "*.jks", "*.kdbx", "id_rsa*", "id_ed25519*", "id_ecdsa*", "id_dsa*", ".azure",
                ".gh-config", ".aws", ".ssh", ".gnupg", ".netrc", ".npmrc", ".pypirc", ".pgpass",
                "service_principal_entries.json", "msal_token_cache*", "credentials.json", "secrets.json"]),
    ("git", [".git"]),
    ("quarantine", ["_quarantine_*"]),
    ("live-database", ["pgdata-*"]),
    ("rebuildable", ["node_modules", "worktrees", "qa-worktrees*", "deploy-worktrees", "wt-*", ".venv", "venv",
                     "__pycache__", ".next", ".turbo", ".pytest_cache", ".mypy_cache", ".ruff_cache",
                     ".hypothesis", ".pnpm-store"]),
    ("system", [".DS_Store", "._*", ".Spotlight-V100", ".fseventsd", ".Trashes", ".TemporaryItems",
                ".smbdelete*", ".unison*", "#recycle"]),
]
FORBIDDEN_RSYNC = ("--del", "--delete", "--remove-source-files", "--force", "--inplace", "--prune-empty-dirs",
                   "--existing", "--ignore-existing")

RC_OK, RC_REFUSED, RC_HELD, RC_CAP, RC_ENGINE, RC_LOCKED, RC_STALLED, RC_VERIFY, RC_DELETING = 0, 2, 3, 4, 5, 6, 7, 8, 9


class Refused(Exception):
    def __init__(self, msg, rc=RC_REFUSED):
        Exception.__init__(self, msg)
        self.rc = rc


def now_local_str(epoch):
    return time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime(epoch))


def out(msg):
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


def err(msg):
    sys.stderr.write(msg + "\n")
    sys.stderr.flush()


# ── test mode ─────────────────────────────────────────────────────────────────────────────────────────────────
def test_root():
    """NB_TEST_ROOT turns on TEST MODE; it is honoured only for a directory under /private/tmp (the session
    scratchpad lives there), so a test can never be pointed at the real NAS or the real lane state."""
    t = os.environ.get("NB_TEST_ROOT")
    if not t:
        return None
    rt = os.path.realpath(t)
    if not rt.startswith("/private/tmp/") or not os.path.isdir(rt):
        raise Refused("NB_TEST_ROOT must be an existing directory under /private/tmp (got %s)" % t)
    return rt


def under(path, root):
    rp, rr = os.path.realpath(path), os.path.realpath(root)
    return rp == rr or rp.startswith(rr.rstrip("/") + "/")


class Ctx(object):
    """Everything a command needs, resolved once: seat, tree, lane paths, conf."""

    def __init__(self, seat, tree, now=None):
        if seat not in SEATS:
            raise Refused("unknown seat '%s' (wednesday, tuesday or friday)" % seat)
        self.seat = seat
        self.info = SEATS[seat]
        self.troot = test_root()
        if now is not None and not self.troot:
            raise Refused("--now is a TEST-MODE parameter (NB_TEST_ROOT unset); the real clock is never supplied by hand")
        self.now = float(now) if now is not None else time.time()
        self.tree = os.path.realpath(tree)
        if os.path.basename(self.tree).lower() != seat:
            raise Refused("the tree %s is not a '%s' tree: its folder name is the discriminator "
                          "(2026-09-09 seat-resolver lesson), and it disagrees with the seat" % (self.tree, seat))
        if self.troot:
            if not under(self.tree, self.troot):
                raise Refused("TEST MODE: the tree must live under NB_TEST_ROOT")
            self.lane = os.path.join(self.troot, "lane")
        else:
            if not under(LANE, self.tree):
                raise Refused("this lane (%s) is not inside the seat's tree %s" % (LANE, self.tree))
            self.lane = LANE
        self.state_dir = os.path.join(self.lane, "state")
        self.log_dir = os.path.join(self.lane, "logs", seat)
        self.manifest_dir = os.path.join(self.lane, "manifests", seat)
        self.state_file = os.path.join(self.state_dir, seat + ".json")
        self.index_file = os.path.join(self.state_dir, seat + ".index.sqlite")
        self.lock_dir = os.path.join(self.state_dir, seat + ".lock.d")
        self.hold_file = os.path.join(self.lane, "HOLD_" + seat)
        self.conf_file = os.path.join(self.lane, "seats", seat + ".conf")
        self.conf = None

    def mkdirs(self):
        for d in (self.state_dir, self.log_dir, self.manifest_dir):
            os.makedirs(d, exist_ok=True)

    # ── conf ──
    def load_conf(self):
        if not os.path.isfile(self.conf_file):
            raise Refused("no seat configuration at %s" % self.conf_file)
        c = {"sets": [], "exclude_name": [], "exclude_name_in": [], "exclude_path": [], "status": "unconfirmed", "fire": None,
             "window_hours": "5", "late_fire": "refuse", "min_free_gib": "200", "max_seconds": "18000",
             "stall_seconds": "900", "io_timeout": "1800", "hash_sample": "40",
             "rsync": "/opt/homebrew/bin/rsync", "card_client_project": "WED", "source_volume": None,
             "nas_root": None, "report_unlisted_under": None, "max_files": "400000",
             "est_files_per_s": "8.9", "est_list_per_s": "390"}
        with open(self.conf_file, "r", encoding="utf-8") as fh:
            for n, raw in enumerate(fh, 1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise Refused("%s line %d: not key=value" % (self.conf_file, n))
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip()
                if k == "set":
                    parts = v.split("|")
                    if len(parts) != 3:
                        raise Refused("%s line %d: set=<Client>|<dest name>|<absolute source>" % (self.conf_file, n))
                    c["sets"].append({"client": parts[0], "dest": parts[1], "src": parts[2]})
                elif k == "exclude_name":
                    c["exclude_name"].append(v)
                elif k == "exclude_name_in":
                    parts = v.split("|")
                    if len(parts) != 2 or "/" in parts[1] or not parts[1]:
                        raise Refused("%s line %d: exclude_name_in=<dest name>|<folder or file name pattern>" % (self.conf_file, n))
                    c["exclude_name_in"].append((parts[0], parts[1]))
                elif k == "exclude_path":
                    parts = v.split("|")
                    if len(parts) != 2:
                        raise Refused("%s line %d: exclude_path=<dest name>|<path inside the set>" % (self.conf_file, n))
                    c["exclude_path"].append((parts[0], parts[1].strip("/")))
                elif k in c:
                    c[k] = v
                else:
                    raise Refused("%s line %d: unknown key '%s'" % (self.conf_file, n, k))
        if c["status"] != "confirmed":
            raise Refused("the configuration %s says status=%s: this seat's sources have not been confirmed on "
                          "its own machine (see proposed/INSTRUCTIONS-for-other-seats.md); nothing run"
                          % (self.conf_file, c["status"]))
        if c["late_fire"] not in ("refuse", "run"):
            raise Refused("late_fire must be 'refuse' or 'run'")
        try:
            hh, mm = c["fire"].split(":")
            c["fire_h"], c["fire_m"] = int(hh), int(mm)
            assert 0 <= c["fire_h"] <= 23 and 0 <= c["fire_m"] <= 59
            for k in ("window_hours", "min_free_gib", "max_seconds", "stall_seconds", "io_timeout", "hash_sample", "max_files"):
                c[k] = float(c[k]) if k in ("window_hours", "min_free_gib") else int(c[k])
            c["est_files_per_s"], c["est_list_per_s"] = float(c["est_files_per_s"]), float(c["est_list_per_s"])
            assert c["est_files_per_s"] > 0 and c["est_list_per_s"] > 0
        except Exception:
            raise Refused("%s: fire must be HH:MM and the numeric keys must be numbers" % self.conf_file)
        if not (0 < c["window_hours"] <= 12):
            raise Refused("window_hours must be between 0 and 12")
        if not c["sets"]:
            raise Refused("%s names no set= line: nothing to back up" % self.conf_file)
        if not c["source_volume"]:
            raise Refused("%s names no source_volume" % self.conf_file)
        if self.troot:
            if not c["nas_root"] or not under(c["nas_root"], self.troot) or not under(c["source_volume"], self.troot):
                raise Refused("TEST MODE: nas_root and source_volume must both live under NB_TEST_ROOT")
            if not under(c["rsync"], self.troot) and c["rsync"] != "/opt/homebrew/bin/rsync":
                raise Refused("TEST MODE: rsync must be the real binary or a stub under NB_TEST_ROOT")
        else:
            if c["nas_root"] not in (None, REAL_NAS_ROOT):
                raise Refused("nas_root is fixed at %s outside test mode (the conf says %s)" % (REAL_NAS_ROOT, c["nas_root"]))
            c["nas_root"] = REAL_NAS_ROOT
            if c["rsync"] != "/opt/homebrew/bin/rsync":
                raise Refused("rsync is fixed at /opt/homebrew/bin/rsync outside test mode")
        seen = set()
        for s in c["sets"]:
            if s["client"] not in self.info["clients"]:
                raise Refused("REFUSED — client folder '%s' is not on seat %s's allow-list %s: a seat writes only "
                              "inside its own client's folder" % (s["client"], self.seat, self.info["clients"]))
            if not s["dest"] or s["dest"].startswith("/") or any(p in ("", ".", "..") for p in s["dest"].split("/")):
                raise Refused("set destination name '%s' must be a plain relative name" % s["dest"])
            key = (s["client"], s["dest"].casefold())
            if key in seen:
                raise Refused("two sets share the destination %s/%s" % (s["client"], s["dest"]))
            seen.add(key)
            if not s["src"].startswith("/"):
                raise Refused("set source must be absolute: %s" % s["src"])
            comps = [p.casefold() for p in s["src"].split("/") if p]
            for f in self.info["forbid"]:
                if f in comps:
                    raise Refused("REFUSED — source %s has the path component '%s': that is another seat's or "
                                  "another client's material, never backed up by seat %s" % (s["src"], f, self.seat))
        for dest, p in c["exclude_name_in"]:
            if dest not in [s["dest"] for s in c["sets"]]:
                raise Refused("exclude_name_in names the set '%s', which is not defined" % dest)
        for dest, p in c["exclude_path"]:
            if any(ch in p for ch in "*?[]\\") or not p or ".." in p.split("/"):
                raise Refused("exclude_path '%s' must be a literal path inside the set (no wildcards)" % p)
            if dest not in [s["dest"] for s in c["sets"]]:
                raise Refused("exclude_path names the set '%s', which is not defined" % dest)
        self.conf = c
        return c

    def client_root(self, client):
        if client not in self.info["clients"]:
            raise Refused("REFUSED — '%s' is not on seat %s's allow-list" % (client, self.seat))
        return os.path.join(self.conf["nas_root"], client, self.info["cap"], BACKUP_FOLDER)

    # ── state (ONE json file per seat, on the drive) ──
    def read_state(self):
        if not os.path.exists(self.state_file):
            return {"schema": SCHEMA, "seat": self.seat, "armed_at": None, "last_good": None, "last_attempt": None,
                    "last_fire": None, "recent_attempts": [], "flag": None}
        with open(self.state_file, "r", encoding="utf-8") as fh:
            st = json.load(fh)   # a corrupt state file FAILS LOUDLY: it is never silently replaced
        if st.get("seat") != self.seat:
            raise Refused("state file %s belongs to seat '%s', not '%s'" % (self.state_file, st.get("seat"), self.seat))
        return st

    def write_state(self, st):
        os.makedirs(self.state_dir, exist_ok=True)
        tmp = self.state_file + ".tmp.%d" % os.getpid()
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(st, fh, indent=1, sort_keys=True)
            fh.write("\n")
        os.replace(tmp, self.state_file)

    def note_attempt(self, status, reason, extra=None):
        st = self.read_state()
        a = {"time": self.now, "time_local": now_local_str(self.now), "status": status, "reason": reason,
             "pid": os.getpid()}
        if extra:
            a.update(extra)
        st["last_attempt"] = a
        if status != "running":
            st["recent_attempts"] = ([{"time_local": a["time_local"], "time": a["time"], "status": status,
                                       "reason": reason}] + st.get("recent_attempts", []))[:12]
        if status == "good":
            st["last_good"] = a
        self.write_state(st)


# ── mounts, free space, names ─────────────────────────────────────────────────────────────────────────────────
def mount_lines(ctx):
    if ctx.troot:
        p = os.path.join(ctx.troot, "mount.txt")
        if not os.path.exists(p):
            return []
        with open(p, "r", encoding="utf-8") as fh:
            return fh.read().splitlines()
    r = subprocess.run(["/sbin/mount"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if r.returncode != 0:
        raise Refused("cannot read the mount table: %s" % r.stderr.strip())
    return r.stdout.splitlines()


def nas_is_smb_mounted(ctx):
    needle = " on %s (smbfs" % ctx.conf["nas_root"]
    return any(needle in ln for ln in mount_lines(ctx))


def source_is_local_volume(ctx):
    vol = ctx.conf["source_volume"].rstrip("/")
    for ln in mount_lines(ctx):
        if (" on %s (" % vol) in ln:
            opts = ln.split(" on %s (" % vol, 1)[1]
            return ("local" in opts) and ("smbfs" not in opts) and ("nfs" not in opts)
    return False


def nas_free_gib(ctx):
    if ctx.troot:
        p = os.path.join(ctx.troot, "free_gib.txt")
        if os.path.exists(p):
            with open(p, "r") as fh:
                return float(fh.read().strip())
    sv = os.statvfs(ctx.conf["nas_root"])
    return sv.f_bavail * sv.f_frsize / float(1 << 30)


def real_name_check(parent, name):
    """The 2026-08-25 incident: a case-folding share answers for 'Datasec' when the folder is 'datasec'.
    os.listdir returns the REAL names. Returns 'exact', 'absent', or the differing real name."""
    try:
        names = os.listdir(parent)
    except OSError as e:
        raise Refused("cannot list %s: %s" % (parent, e))
    if name in names:
        return "exact"
    for n in names:
        if n.casefold() == name.casefold() or unicodedata.normalize("NFC", n).casefold() == unicodedata.normalize("NFC", name).casefold():
            return n
    return "absent"


def ensure_dest_chain(root_existing, rel_parts, create):
    """Walk root_existing/rel_parts one level at a time. Every level that exists must exist with EXACTLY this
    spelling (else Refused). Missing levels are created when create=True. Returns (path, existed_fully)."""
    cur = root_existing
    existed = True
    for part in rel_parts:
        chk = real_name_check(cur, part) if os.path.isdir(cur) else "absent"
        nxt = os.path.join(cur, part)
        if chk == "exact":
            if not os.path.isdir(nxt):
                raise Refused("REFUSED — %s exists on the NAS but is not a folder" % nxt)
        elif chk == "absent":
            existed = False
            if create:
                os.mkdir(nxt)
        else:
            raise Refused("REFUSED — the NAS has '%s' where '%s' is expected under %s: the names differ in CASE. "
                          "A case-folding share would mix the two (2026-08-25 incident); nothing written"
                          % (chk, part, cur))
        cur = nxt
    return cur, existed


def ckey(rel):
    """Comparison key: NFC + casefold. The NAS is case-insensitive and may normalise Unicode."""
    return unicodedata.normalize("NFC", rel).casefold()


# ── the walker: ONE implementation of what is in scope ────────────────────────────────────────────────────────
class Rules(object):
    def __init__(self, ctx, set_dest):
        self.pats = []
        for cat, pl in EXCLUDES:
            for p in pl:
                self.pats.append((cat, p))
        src = [x["src"] for x in ctx.conf["sets"] if x["dest"] == set_dest]
        if src and os.path.realpath(src[0]) == ctx.tree:
            for p in ctx.info["other_seat_names"]:
                self.pats.append(("other-seat", p))
        for p in ctx.info["other_client_names"]:
            self.pats.append(("other-client", p))
        for p in ctx.conf["exclude_name"]:
            self.pats.append(("conf", p))
        for d, p in ctx.conf["exclude_name_in"]:
            if d == set_dest:
                self.pats.append(("conf", p))
        self.paths = set(p for d, p in ctx.conf["exclude_path"] if d == set_dest)

    def match(self, name, rel):
        for cat, p in self.pats:
            if fnmatch.fnmatchcase(name, p):
                return (cat, p)
        if rel in self.paths:
            return ("conf-path", rel)
        return None


def is_secret_name(name):
    for cat, pl in EXCLUDES:
        if cat == "secret":
            for p in pl:
                if fnmatch.fnmatchcase(name, p):
                    return p
    return None


def walk(top, rules=None, measure_excluded=False, no_measure=()):
    """Returns dict(files={rel:(size,mtime_ns,ctime_ns)}, dirs=set, links={rel:target}, specials=[rel],
    excluded={(cat,pattern):[entries,files,bytes]}, errors=[str]). Never follows a symlink."""
    res = {"files": {}, "dirs": set(), "links": {}, "specials": [], "excluded": {}, "errors": [], "excluded_list": []}
    stack = [("", top)]
    while stack:
        rel, path = stack.pop()
        try:
            it = os.scandir(path)
        except OSError as e:
            res["errors"].append("%s: %s" % (path, e))
            continue
        with it:
            for e in it:
                r = e.name if not rel else rel + "/" + e.name
                try:
                    m = rules.match(e.name, r) if rules else None
                    if m:
                        slot = res["excluded"].setdefault(m, [0, 0, 0])
                        slot[0] += 1
                        if len(res["excluded_list"]) < 400:
                            res["excluded_list"].append((m[0], r))
                        if measure_excluded and r not in no_measure:
                            f, b = measure(e.path, e)
                            slot[1] += f
                            slot[2] += b
                        continue
                    if e.is_symlink():
                        try:
                            res["links"][r] = os.readlink(e.path)
                        except OSError as ex:
                            res["links"][r] = "?unreadable: %s" % ex
                    elif e.is_dir(follow_symlinks=False):
                        res["dirs"].add(r)
                        stack.append((r, e.path))
                    elif e.is_file(follow_symlinks=False):
                        s = e.stat(follow_symlinks=False)
                        res["files"][r] = (s.st_size, s.st_mtime_ns, s.st_ctime_ns)
                    else:
                        res["specials"].append(r)
                except OSError as ex:
                    res["errors"].append("%s: %s" % (e.path, ex))
    return res


def measure(path, entry=None):
    """files, bytes under path (no rules). Used only to SIZE what is excluded."""
    try:
        if entry is not None and (entry.is_symlink() or not entry.is_dir(follow_symlinks=False)):
            return (1, entry.stat(follow_symlinks=False).st_size)
    except OSError:
        return (0, 0)
    f = b = 0
    stack = [path]
    while stack:
        p = stack.pop()
        try:
            with os.scandir(p) as it:
                for e in it:
                    try:
                        if e.is_dir(follow_symlinks=False) and not e.is_symlink():
                            stack.append(e.path)
                        else:
                            f += 1
                            b += e.stat(follow_symlinks=False).st_size
                    except OSError:
                        pass
        except OSError:
            pass
    return (f, b)


def top_of(rel):
    return rel.split("/", 1)[0] if "/" in rel else "(files at the top)"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


# ── window arithmetic (pure: the clock is a parameter) ────────────────────────────────────────────────────────
def window_for(now, fire_h, fire_m, window_hours):
    """The most recent scheduled window opening at or before `now`, in local time.
    Returns (open_epoch, close_epoch, in_window)."""
    lt = datetime.datetime.fromtimestamp(now)
    today_open = lt.replace(hour=fire_h, minute=fire_m, second=0, microsecond=0)
    if lt < today_open:
        today_open = today_open - datetime.timedelta(days=1)
    o = today_open.timestamp()
    c = o + window_hours * 3600.0
    return (o, c, o <= now < c)


# ── lock (mkdir on the drive; a stale lock is REPORTED, never removed silently) ───────────────────────────────
def pid_alive(pid):
    try:
        os.kill(int(pid), 0)
    except (OSError, ValueError):
        return False
    r = subprocess.run(["/bin/ps", "-o", "command=", "-p", str(pid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       universal_newlines=True)
    return ("nb_core" in r.stdout) or ("nas_backup" in r.stdout)


def lock_status(ctx):
    """None if free; else dict(owner..., alive=bool)."""
    if not os.path.isdir(ctx.lock_dir):
        return None
    info = {"pid": None, "started_local": "unknown"}
    op = os.path.join(ctx.lock_dir, "owner.json")
    try:
        with open(op, "r") as fh:
            info = json.load(fh)
    except (OSError, ValueError):
        pass
    info["alive"] = bool(info.get("pid")) and pid_alive(info["pid"])
    return info


def lock_take(ctx, mode):
    os.makedirs(ctx.state_dir, exist_ok=True)
    try:
        os.mkdir(ctx.lock_dir)
    except FileExistsError:
        ls = lock_status(ctx) or {}
        if ls.get("alive"):
            raise Refused("REFUSED — another run holds the lock %s (pid %s, started %s); nothing run"
                          % (ctx.lock_dir, ls.get("pid"), ls.get("started_local")), RC_LOCKED)
        raise Refused("REFUSED — STALE lock at %s: pid %s (started %s) is not running. It is NOT removed for you. "
                      "After checking no copy is running: nas_backup.sh --clear-stale-lock (moves it into "
                      "state/_quarantine_<date>/)" % (ctx.lock_dir, ls.get("pid"), ls.get("started_local")), RC_LOCKED)
    with open(os.path.join(ctx.lock_dir, "owner.json"), "w") as fh:
        json.dump({"pid": os.getpid(), "started": time.time(), "started_local": now_local_str(time.time()),
                   "mode": mode, "seat": ctx.seat}, fh)


def lock_release(ctx):
    """No delete verb: the released lock directory is MOVED into state/released_locks/."""
    if not os.path.isdir(ctx.lock_dir):
        return
    dst_parent = os.path.join(ctx.state_dir, "released_locks")
    os.makedirs(dst_parent, exist_ok=True)
    dst = os.path.join(dst_parent, "%s.%s.%d.lock.d" % (ctx.seat, time.strftime("%Y%m%d-%H%M%S"), os.getpid()))
    os.rename(ctx.lock_dir, dst)


def cmd_clear_stale_lock(ctx):
    ls = lock_status(ctx)
    if ls is None:
        out("no lock at %s" % ctx.lock_dir)
        return RC_OK
    if ls.get("alive"):
        raise Refused("REFUSED — the lock is LIVE (pid %s, started %s): not stale, not moved" % (ls.get("pid"), ls.get("started_local")), RC_LOCKED)
    q = os.path.join(ctx.state_dir, "_quarantine_%s" % time.strftime("%Y-%m-%d"))
    os.makedirs(q, exist_ok=True)
    dst = os.path.join(q, "%s.stale.%s.lock.d" % (ctx.seat, time.strftime("%H%M%S")))
    os.rename(ctx.lock_dir, dst)
    out("stale lock (pid %s, started %s) MOVED to %s" % (ls.get("pid"), ls.get("started_local"), dst))
    return RC_OK


# ── index (engine cache, rebuildable: losing it costs one night of sha256 comparison, never correctness) ──────
class Index(object):
    def __init__(self, path, readonly):
        self.readonly = readonly
        self.db = None
        if readonly and not os.path.exists(path):
            return
        self.db = sqlite3.connect(path)
        if not readonly:
            self.db.execute("CREATE TABLE IF NOT EXISTS files (setname TEXT, rel TEXT, size INTEGER, mtime_ns INTEGER, "
                            "ctime_ns INTEGER, copied_at REAL, PRIMARY KEY (setname, rel))")
            self.db.commit()

    def load(self, setname):
        if self.db is None:
            return {}
        try:
            return dict((r[0], (r[1], r[2], r[3])) for r in
                        self.db.execute("SELECT rel,size,mtime_ns,ctime_ns FROM files WHERE setname=?", (setname,)))
        except sqlite3.Error:
            return {}

    def put_many(self, setname, rows, when):
        if self.db is None or self.readonly:
            return
        self.db.executemany("INSERT OR REPLACE INTO files (setname,rel,size,mtime_ns,ctime_ns,copied_at) VALUES (?,?,?,?,?,?)",
                            [(setname, rel, s[0], s[1], s[2], when) for rel, s in rows])
        self.db.commit()

    def close(self):
        if self.db is not None:
            self.db.close()


# ── rsync (transport only) ────────────────────────────────────────────────────────────────────────────────────
def rsync_version_ok(binary):
    if not (os.path.isfile(binary) and os.access(binary, os.X_OK)):
        return "missing or not executable: %s" % binary
    r = subprocess.run([binary, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    first = (r.stdout.splitlines() or [""])[0]
    if "openrsync" in r.stdout or "version 2." in first:
        return "%s is not rsync 3 (%s): --backup-dir behaviour is not trusted on it" % (binary, first.strip())
    return None


def cpu_seconds(pid):
    r = subprocess.run(["/usr/bin/pgrep", "-P", str(pid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    pids = [str(pid)] + r.stdout.split()
    r = subprocess.run(["/bin/ps", "-o", "time=", "-p", ",".join(pids)], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       universal_newlines=True)
    total = 0.0
    for ln in r.stdout.split():
        parts = ln.replace(",", ".").split(":")
        try:
            sec = float(parts[-1])
            if len(parts) >= 2:
                sec += int(parts[-2]) * 60
            if len(parts) >= 3:
                sec += int(parts[-3].split("-")[-1]) * 3600
            total += sec
        except ValueError:
            pass
    return total


_child = {"p": None}


def run_rsync(ctx, argv, log_path, err_path, deadline, stall_seconds):
    """Returns (status, rc): status in ok|killed-cap|stalled."""
    for a in argv[1:]:
        for bad in FORBIDDEN_RSYNC:
            if a == bad or a.startswith(bad + "=") or a.startswith("--delete") or a.startswith("--del"):
                raise Refused("REFUSED — forbidden engine flag %s (this tool never passes a deletion flag)" % a)
    with open(log_path, "wb") as lo, open(err_path, "wb") as le:
        p = subprocess.Popen(argv, stdout=lo, stderr=le)
    _child["p"] = p
    started = time.time()
    stall_checked = False
    try:
        while True:
            try:
                rc = p.wait(timeout=2)
                return ("ok", rc)
            except subprocess.TimeoutExpired:
                pass
            el = time.time() - started
            if not stall_checked and el >= stall_seconds:
                stall_checked = True
                if os.path.getsize(log_path) == 0 and os.path.getsize(err_path) == 0 and cpu_seconds(p.pid) < 2:
                    kill_child()
                    return ("stalled", None)
            if time.time() >= deadline:
                kill_child()
                return ("killed-cap", None)
    finally:
        _child["p"] = None


def kill_child():
    p = _child["p"]
    if p is None or p.poll() is not None:
        return
    p.terminate()
    try:
        p.wait(timeout=5)
    except subprocess.TimeoutExpired:
        p.kill()
        p.wait()


def parse_engine_log(log_path):
    """Counts from the engine's own itemised output. A line that deletes is a failure whatever the exit code."""
    res = {"new": 0, "updated": 0, "dirs": 0, "deleting": [], "paths": [], "transferred_bytes": None, "lines": 0}
    with open(log_path, "rb") as fh:
        text = fh.read().decode("utf-8", "replace").replace("\r", "\n")
    for ln in text.split("\n"):
        if not ln:
            continue
        res["lines"] += 1
        low = ln.lower()
        if low.startswith("*deleting") or low.startswith("deleting "):
            res["deleting"].append(ln)
        elif ln.startswith(">f+++++++++ "):
            res["new"] += 1
            res["paths"].append(ln[12:])
        elif ln.startswith(">f"):
            res["updated"] += 1
            res["paths"].append(ln[12:])
        elif ln.startswith("cd"):
            res["dirs"] += 1
        elif low.startswith("total transferred file size:"):
            digits = "".join(ch for ch in ln.split(":", 1)[1] if ch.isdigit())
            res["transferred_bytes"] = int(digits) if digits else None
    return res


# ── the backup ────────────────────────────────────────────────────────────────────────────────────────────────
def preflight(ctx, mode, out_of_sequence, scheduled, lines):
    """Every refusal the brief names. Returns the list of per-client roots. Raises Refused."""
    c = ctx.conf
    if not source_is_local_volume(ctx):
        raise Refused("REFUSED — the source volume %s is not mounted as a local drive (the mount table has no "
                      "local entry for it); nothing run" % c["source_volume"])
    if not under(ctx.tree, c["source_volume"]):
        raise Refused("REFUSED — this seat's tree %s is not on the configured source drive %s: a seat backs up "
                      "only its own drive" % (ctx.tree, c["source_volume"]))
    tree_dev = os.stat(ctx.tree).st_dev
    for s in c["sets"]:
        if not os.path.isdir(s["src"]):
            raise Refused("REFUSED — source %s is absent or not a folder; nothing run" % s["src"])
        if os.path.islink(s["src"]):
            raise Refused("REFUSED — source %s is a symlink; nothing run" % s["src"])
        if not under(s["src"], c["source_volume"]) or os.stat(s["src"]).st_dev != tree_dev:
            raise Refused("REFUSED — source %s is not on the seat's own drive (%s); nothing run" % (s["src"], c["source_volume"]))
    if not nas_is_smb_mounted(ctx):
        raise Refused("REFUSED — %s is not mounted as a network share (the mount table shows no smbfs entry): an "
                      "unmounted path would fill the local disk under /Volumes; nothing run" % c["nas_root"])
    for client in sorted(set(s["client"] for s in c["sets"])):
        chk = real_name_check(c["nas_root"], client)
        if chk == "absent":
            raise Refused("REFUSED — the NAS has no top-level folder '%s' (real names: %s); it is never created by "
                          "this tool; nothing run" % (client, sorted(os.listdir(c["nas_root"]))))
        if chk != "exact":
            raise Refused("REFUSED — the NAS top-level folder is '%s', not '%s': the names differ in CASE "
                          "(2026-08-25 incident: a case-folding share); nothing run" % (chk, client))
        ensure_dest_chain(os.path.join(c["nas_root"], client), [ctx.info["cap"], BACKUP_FOLDER], create=False)
    free = nas_free_gib(ctx)
    lines.append("NAS free space: %.1f GiB (floor %.0f GiB)" % (free, c["min_free_gib"]))
    if free < c["min_free_gib"]:
        raise Refused("REFUSED — NAS free space %.1f GiB is below the floor of %.0f GiB; nothing run" % (free, c["min_free_gib"]))
    bad = rsync_version_ok(c["rsync"])
    if bad:
        raise Refused("REFUSED — engine %s" % bad)
    if mode == "run":
        o, cl, inw = window_for(ctx.now, c["fire_h"], c["fire_m"], c["window_hours"])
        if not inw and not out_of_sequence:
            raise Refused("REFUSED — %s is outside this seat's nightly window (%s to %s). An out-of-sequence backup "
                          "needs Kam's approval: --out-of-sequence \"<the card id he ruled>\"; nothing run"
                          % (now_local_str(ctx.now), now_local_str(o), now_local_str(cl)))


def plan_set(ctx, s, index_rows, lines, do_hash=True):
    """Lists the source, lists the destination, decides what must be copied. Reads only."""
    rules = Rules(ctx, s["dest"])
    src = walk(s["src"], rules)
    if len(src["files"]) > ctx.conf["max_files"]:
        # A scope this size does not finish in a night (measured: the armed nas_push leg has been stopped by its
        # 4-hour cap every night since 2026-11-14). Refuse loudly and name where the files are, rather than start.
        tops = {}
        for rel, v in src["files"].items():
            k = "/".join(rel.split("/")[:2])
            t = tops.setdefault(k, [0, 0])
            t[0] += 1
            t[1] += v[0]
        worst = sorted(tops.items(), key=lambda kv: -kv[1][0])[:5]
        raise Refused("REFUSED \u2014 set %s has %d files in scope, above max_files=%d: too many to copy and count in one "
                      "night. Largest by file count: %s. Narrow the scope (exclude_path= or exclude_name= in seats/%s.conf) "
                      "or raise max_files on the coordinator's word; nothing copied for this set"
                      % (s["dest"], len(src["files"]), ctx.conf["max_files"],
                         "; ".join("%s (%d files, %s)" % (k, v[0], fmt_bytes(v[1])) for k, v in worst), ctx.seat))
    croot = ctx.client_root(s["client"])
    dest_dir = os.path.join(croot, "current", *s["dest"].split("/"))
    dest_exists = True
    try:
        _, dest_exists = ensure_dest_chain(os.path.join(ctx.conf["nas_root"], s["client"]),
                                           [ctx.info["cap"], BACKUP_FOLDER, "current"] + s["dest"].split("/"), create=False)
    except Refused:
        raise
    dst = walk(dest_dir) if dest_exists else {"files": {}, "dirs": set(), "links": {}, "specials": [], "errors": [], "excluded": {}}
    plan = {"set": s, "src": src, "dst": dst, "dest_dir": dest_dir, "dest_exists": dest_exists, "problems": [],
            "copy": [], "copy_dirs": [], "reason": {}, "hash_equal": [], "collisions": [], "type_conflicts": []}
    if src["errors"]:
        plan["problems"].append("source could not be fully read: %d error(s), first: %s" % (len(src["errors"]), src["errors"][0]))
    if dst["errors"]:
        plan["problems"].append("destination could not be fully read: %d error(s), first: %s" % (len(dst["errors"]), dst["errors"][0]))
    # Names that differ only in case (or Unicode form). The drive is case-sensitive, the NAS is not (both
    # measured 2026-11-27), so the NAS can hold one of such a pair, never both. NEITHER is copied: copying one
    # would silently stand in for the other. This DEGRADES rather than blocks (2026-09-10 lesson: five such pairs
    # exist in the Secuura folder today, and a refusal would have meant no backup at all), and it is never
    # silent: the names are counted, printed at every run, and listed in the manifest.
    groups = {}
    for rel in list(src["files"]) + list(src["dirs"]):
        groups.setdefault(ckey(rel), []).append(rel)
    clash = sorted(r for v in groups.values() if len(v) > 1 for r in v)
    plan["collisions"] = clash
    plan["collision_skipped"] = {}
    if clash:
        clashset = set(clash)
        clash_dirs = tuple(r + "/" for r in clash if r in src["dirs"])
        for rel in list(src["files"]):
            if rel in clashset or rel.startswith(clash_dirs):
                plan["collision_skipped"][rel] = src["files"].pop(rel)
        for rel in list(src["dirs"]):
            if rel in clashset or rel.startswith(clash_dirs):
                src["dirs"].discard(rel)
    dfiles = dict((ckey(r), (r, v)) for r, v in dst["files"].items())
    ddirs = dict((ckey(r), r) for r in dst["dirs"])
    plan["dfiles"], plan["ddirs"] = dfiles, ddirs
    for rel in sorted(src["dirs"]):
        k = ckey(rel)
        if k in dfiles:
            plan["type_conflicts"].append(rel)
        elif k not in ddirs:
            plan["copy_dirs"].append(rel)
    to_hash = []
    for rel, sv in src["files"].items():
        k = ckey(rel)
        if k in ddirs:
            plan["type_conflicts"].append(rel)
            continue
        d = dfiles.get(k)
        if d is None:
            plan["copy"].append(rel)
            plan["reason"][rel] = "new"
        elif d[1][0] != sv[0]:
            plan["copy"].append(rel)
            plan["reason"][rel] = "size"
        else:
            ix = index_rows.get(rel)
            if ix is None or tuple(ix) != tuple(sv):
                to_hash.append((rel, d[0]))
    plan["to_hash_count"] = len(to_hash)
    plan["hash_bytes"] = sum(src["files"][r][0] for r, _ in to_hash)
    if do_hash:
        for rel, drel in to_hash:
            try:
                a = sha256_of(os.path.join(s["src"], rel))
                b = sha256_of(os.path.join(dest_dir, drel))
            except OSError as e:
                plan["problems"].append("could not compare %s: %s" % (rel, e))
                continue
            if a == b:
                plan["hash_equal"].append(rel)
            else:
                plan["copy"].append(rel)
                plan["reason"][rel] = "content"
    else:
        plan["unverified_same_size"] = [r for r, _ in to_hash]
    if plan["type_conflicts"]:
        plan["problems"].append("%d path(s) are a file on one side and a folder on the other (first: %s); not copied"
                                % (len(plan["type_conflicts"]), plan["type_conflicts"][0]))
    plan["copy"].sort()
    return plan


def folder_table(plan, observed_ok):
    """Per top-level folder, BOTH sides. observed_ok = set of source rels observed at the destination with the
    source's size. Returns {top: {...}}."""
    t = {}
    src = plan["src"]["files"]
    for rel, sv in src.items():
        row = t.setdefault(top_of(rel), {"src_files": 0, "src_bytes": 0, "dst_files": 0, "dst_bytes": 0,
                                         "dst_only_files": 0, "dst_only_bytes": 0})
        row["src_files"] += 1
        row["src_bytes"] += sv[0]
        if rel in observed_ok:
            row["dst_files"] += 1
            row["dst_bytes"] += sv[0]
    skeys = set(ckey(r) for r in src)
    for k, (drel, dv) in plan["dfiles"].items():
        if k not in skeys:
            row = t.setdefault(top_of(drel), {"src_files": 0, "src_bytes": 0, "dst_files": 0, "dst_bytes": 0,
                                              "dst_only_files": 0, "dst_only_bytes": 0})
            row["dst_only_files"] += 1
            row["dst_only_bytes"] += dv[0]
    return t


def fmt_bytes(n):
    n = float(n)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if n < 1024 or unit == "TiB":
            return ("%d %s" % (n, unit)) if unit == "B" else ("%.2f %s" % (n, unit))
        n /= 1024.0


def cmd_backup(ctx, mode, scheduled=False, out_of_sequence=None, max_seconds=None, no_hash=False):
    # PID in the stamp: two runs inside the same second otherwise share a log and a versions/ folder
    # (found by exercising nas_sync.sh in 2026-09; the same trap is here).
    stamp = "%s_%d" % (time.strftime("%Y-%m-%d_%H%M%S", time.localtime(ctx.now)), os.getpid())
    lines = []

    def say(msg):
        lines.append(msg)
        out(msg)

    ctx.mkdirs()
    run_log = os.path.join(ctx.log_dir, "%s_%s.log" % (stamp, mode))
    say("=== nas-backup seat=%s mode=%s %s ===" % (ctx.seat, mode.upper(), now_local_str(time.time())))
    if mode == "dry":
        say("DRY RUN: reads only. Nothing is written to the NAS, the state file or the index.")
    try:
        ctx.load_conf()
        if mode == "run" and os.path.exists(ctx.hold_file):
            raise Refused("REFUSED — %s exists: real runs are HELD (arming is the coordinator's word on Kam's "
                          "instruction); --dry is still allowed; nothing run" % ctx.hold_file, RC_HELD)
        if out_of_sequence is not None and len(out_of_sequence.strip()) < 6:
            raise Refused("REFUSED — --out-of-sequence needs the id of the card Kam ruled (it is recorded in the manifest)")
        preflight(ctx, mode, out_of_sequence, scheduled, lines)
        if mode == "run":
            lock_take(ctx, mode)
        else:
            ls = lock_status(ctx)
            if ls:
                say("note: a lock is present (pid %s, alive=%s); the dry run only reads" % (ls.get("pid"), ls.get("alive")))
    except Refused as e:
        say(str(e))
        if mode == "run":
            try:
                ctx.note_attempt("refused", str(e))
            except Exception as ex:   # the refusal must still be printed even if the state cannot be written
                err("nas-backup: could not record the refusal in the state file: %s" % ex)
        with open(run_log, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        return e.rc

    c = ctx.conf
    result = {"status": "failed", "reason": "", "rc": RC_VERIFY}
    manifest = {"schema": SCHEMA, "seat": ctx.seat, "mode": mode, "stamp": stamp, "started": time.time(),
                "started_local": now_local_str(time.time()), "host": os.uname().nodename,
                "trigger": ("out-of-sequence: " + out_of_sequence) if out_of_sequence else ("scheduled" if scheduled else "manual-in-window"),
                "sets": [], "copy_only": True, "review_after_note":
                "versions/<stamp>/ folders are dated so they can be reviewed; nothing here is removed by this tool, "
                "and clean-up is Kam's word only (2026-11-11 lesson rule 5)."}
    started = time.time()
    cap = max_seconds if max_seconds is not None else c["max_seconds"]
    deadline = started + cap
    index = Index(ctx.index_file, readonly=(mode != "run"))
    interrupted = {"sig": None}

    def on_signal(signum, frame):
        interrupted["sig"] = signum
        kill_child()
        raise KeyboardInterrupt()

    def on_alarm(signum, frame):
        kill_child()
        raise Refused("WATCHDOG: the run was still going %d s after its %d s cap (a blocked read or write on the "
                      "NAS, or a macOS privacy prompt waiting on this Mac's screen); stopped" % (900, cap), RC_CAP)

    if mode == "run":
        signal.signal(signal.SIGTERM, on_signal)
        signal.signal(signal.SIGINT, on_signal)
        signal.signal(signal.SIGALRM, on_alarm)
        signal.alarm(int(cap) + 900)
        ctx.note_attempt("running", "started %s" % stamp, {"stamp": stamp})
    problems = []
    totals = {"src_files": 0, "src_bytes": 0, "copy_files": 0, "copy_bytes": 0, "new": 0, "changed": 0,
              "dst_files": 0, "dst_bytes": 0, "dst_only_files": 0, "versioned": 0, "changed_during_run": 0,
              "vanished": 0, "symlinks": 0, "excluded_entries": 0, "case_collision_files": 0}
    client_roots = {}
    try:
        for s in c["sets"]:
            say("--- set %s/%s  <-  %s" % (s["client"], s["dest"], s["src"]))
            croot = ctx.client_root(s["client"])
            if mode == "run":
                ensure_dest_chain(os.path.join(c["nas_root"], s["client"]), [ctx.info["cap"], BACKUP_FOLDER], create=True)
                for sub in ("current", "versions", "manifests", "runs", "_tmp_incoming"):
                    ensure_dest_chain(croot, [sub], create=True)
                ensure_dest_chain(croot, ["current"] + s["dest"].split("/"), create=True)
                if s["client"] not in client_roots:
                    client_roots[s["client"]] = croot
                    readme = os.path.join(croot, "README.txt")
                    if not os.path.exists(readme):
                        with open(readme, "w", encoding="utf-8") as fh:
                            fh.write("NIGHTLY BACKUP of the %s seat (copy only). Written by 2_Project_Files/nas-backup/nas_backup.sh.\n"
                                     "current/   the latest copy of each set\n"
                                     "versions/  <run stamp>/ holds the PREVIOUS copy of every file a run replaced\n"
                                     "manifests/ one manifest per run (per-folder counts on both sides, symlinks, exclusions)\n"
                                     "runs/      RUN_<stamp>_STARTED.txt without a matching _COMPLETE.txt = an INCOMPLETE copy\n"
                                     "Nothing here is ever removed by the tool. Clean-up is Kam's word only.\n" % ctx.info["cap"])
                    with open(os.path.join(croot, "runs", "RUN_%s_STARTED.txt" % stamp), "w", encoding="utf-8") as fh:
                        fh.write("started %s by seat %s on %s (pid %d). If no RUN_%s_COMPLETE.txt sits beside this file, "
                                 "the copy did NOT finish: do not trust current/ as complete.\n"
                                 % (now_local_str(time.time()), ctx.seat, os.uname().nodename, os.getpid(), stamp))
            index_rows = index.load(s["dest"])
            t0 = time.time()
            plan = plan_set(ctx, s, index_rows, lines, do_hash=not (mode == "dry" and no_hash))
            src, dst = plan["src"], plan["dst"]
            copy_bytes = sum(src["files"][r][0] for r in plan["copy"])
            n_new = sum(1 for r in plan["copy"] if plan["reason"][r] == "new")
            n_chg = len(plan["copy"]) - n_new
            src_bytes = sum(v[0] for v in src["files"].values())
            exc_entries = sum(v[0] for v in src["excluded"].values())
            say("    source in scope: %d files, %s, %d folders, %d symlinks (recorded, not copied), %d special files (skipped)"
                % (len(src["files"]), fmt_bytes(src_bytes), len(src["dirs"]), len(src["links"]), len(src["specials"])))
            say("    excluded at the source: %d entries (%s)" % (exc_entries, ", ".join(
                "%s=%d" % (cat, n) for cat, n in sorted(sum_by_cat(src["excluded"]).items())) or "none"))
            say("    destination now: %s, %d files" % ("present" if plan["dest_exists"] else "ABSENT (first run: everything is new)", len(dst["files"])))
            say("    to copy: %d files, %s (%d new, %d changed -> previous copy kept in versions/%s/); %d new folders"
                % (len(plan["copy"]), fmt_bytes(copy_bytes), n_new, n_chg, stamp, len(plan["copy_dirs"])))
            if plan["to_hash_count"]:
                if mode == "dry" and no_hash:
                    say("    same size, no index entry: %d files (%s) NOT compared by content in this dry run (--no-hash); a "
                        "real run compares them by sha256 once" % (plan["to_hash_count"], fmt_bytes(plan["hash_bytes"])))
                else:
                    say("    compared by sha256 (same size, source changed or not yet indexed): %d files, %d identical"
                        % (plan["to_hash_count"], len(plan["hash_equal"])))
            say("    planning took %.1f s" % (time.time() - t0))
            if plan["collisions"]:
                say("    NOT BACKED UP: %d file(s), because %d name(s) differ only in case from a sibling and the NAS cannot hold "
                    "both (first: %s | %s). They are listed in the manifest."
                    % (len(plan["collision_skipped"]), len(plan["collisions"]), plan["collisions"][0], plan["collisions"][1]))
            for p in plan["problems"]:
                say("    PROBLEM: %s" % p)
                problems.append("%s: %s" % (s["dest"], p))
            mset = {"client": s["client"], "dest": s["dest"], "source": s["src"], "destination": plan["dest_dir"],
                    "src_files": len(src["files"]), "src_bytes": src_bytes, "src_dirs": len(src["dirs"]),
                    "symlinks": len(src["links"]), "specials": len(src["specials"]),
                    "excluded": [{"category": k[0], "pattern": k[1], "entries": v[0]} for k, v in sorted(src["excluded"].items())],
                    "to_copy_files": len(plan["copy"]), "to_copy_bytes": copy_bytes, "new": n_new, "changed": n_chg,
                    "case_collision_names": plan["collisions"][:200],
                    "case_collision_files_not_backed_up": len(plan["collision_skipped"]),
                    "problems": list(plan["problems"])}
            totals["src_files"] += len(src["files"])
            totals["src_bytes"] += src_bytes
            totals["copy_files"] += len(plan["copy"])
            totals["copy_bytes"] += copy_bytes
            totals["new"] += n_new
            totals["changed"] += n_chg
            totals["symlinks"] += len(src["links"])
            totals["excluded_entries"] += exc_entries
            totals["case_collision_files"] += len(plan["collision_skipped"])

            # the list the engine is given: new folders first, then files. NUL-separated.
            list_path = os.path.join(ctx.log_dir, "%s_%s_%s.files0" % (stamp, mode, s["dest"].replace("/", "__")))
            with open(list_path, "wb") as fh:
                for rel in plan["copy_dirs"] + plan["copy"]:
                    fh.write(rel.encode("utf-8", "surrogateescape") + b"\0")
            observed_ok = set()
            for rel in src["files"]:
                if rel not in plan["reason"] and ckey(rel) in plan["dfiles"]:
                    observed_ok.add(rel)      # listed at the destination with the source's size
            engine = {"ran": False}
            if plan["copy"] or plan["copy_dirs"]:
                eng_log = os.path.join(ctx.log_dir, "%s_%s_%s.rsync.log" % (stamp, mode, s["dest"].replace("/", "__")))
                eng_err = eng_log[:-4] + ".err"
                bdir = os.path.join(croot, "versions", stamp, *s["dest"].split("/"))
                argv = [c["rsync"], "-t", "-O", "-I", "--from0", "--files-from=" + list_path, "--backup",
                        "--backup-dir=" + bdir, "--timeout=%d" % c["io_timeout"], "--out-format=%i %n%L", "--stats", "--no-h"]
                dest_arg = plan["dest_dir"]
                if mode == "dry":
                    argv.insert(1, "-n")
                    if not plan["dest_exists"]:
                        # The destination does not exist yet: compare against an EMPTY LOCAL folder, so the engine
                        # is never handed a path on the NAS at all in this case (everything is new anyway).
                        dest_arg = os.path.join(ctx.state_dir, "empty_for_dry_run")
                        os.makedirs(dest_arg, exist_ok=True)
                        argv = [x for x in argv if not x.startswith("--backup-dir=")]
                        argv.append("--backup-dir=" + os.path.join(ctx.state_dir, "empty_for_dry_run_versions"))
                else:
                    argv.append("--temp-dir=" + os.path.join(croot, "_tmp_incoming"))
                argv += [s["src"].rstrip("/") + "/", dest_arg.rstrip("/") + "/"]
                say("    engine: %s" % " ".join(shlex.quote(a) for a in argv))
                status, rc = run_rsync(ctx, argv, eng_log, eng_err, deadline, c["stall_seconds"])
                engine = {"ran": True, "status": status, "rc": rc, "log": eng_log, "err": eng_err}
                pl = parse_engine_log(eng_log)
                engine.update({"new": pl["new"], "updated": pl["updated"], "deleting_lines": len(pl["deleting"]),
                               "transferred_bytes": pl["transferred_bytes"]})
                with open(eng_err, "rb") as fh:
                    etxt = fh.read().decode("utf-8", "replace").strip()
                say("    engine result: %s rc=%s; its log lists %d new + %d replaced files, %s; deleting lines: %d"
                    % (status, rc, pl["new"], pl["updated"],
                       fmt_bytes(pl["transferred_bytes"]) if pl["transferred_bytes"] is not None else "bytes not reported",
                       len(pl["deleting"])))
                if etxt:
                    say("    engine stderr (%d lines), first: %s" % (len(etxt.splitlines()), etxt.splitlines()[0][:300]))
                if pl["deleting"]:
                    problems.append("%s: the engine's log holds %d DELETING line(s) (first: %s): that must be impossible"
                                    % (s["dest"], len(pl["deleting"]), pl["deleting"][0][:200]))
                    result["rc"] = RC_DELETING
                for pth in pl["paths"]:
                    hit = [is_secret_name(part) for part in pth.split("/")]
                    if any(hit):
                        problems.append("%s: a secret-shaped name travelled: %s" % (s["dest"], pth))
                        break
                if status == "stalled":
                    problems.append("%s: STALLED: after %ds the engine had written nothing and used no CPU. Most likely a "
                                    "macOS privacy prompt for rsync is waiting on this Mac's screen (PORTABILITY 15a)"
                                    % (s["dest"], c["stall_seconds"]))
                    result["rc"] = RC_STALLED
                elif status == "killed-cap":
                    problems.append("%s: stopped by the run-time cap (%ds); whole files only were written and the next run resumes" % (s["dest"], cap))
                    result["rc"] = RC_CAP
                elif rc not in (0, 23, 24):
                    # 23/24 = "some files were not transferred / vanished": on a live tree a listed file can go
                    # away between the listing and the copy. Those codes are NOT trusted either way: the
                    # observation below accounts for every listed file one by one, and an unexplained absence fails.
                    problems.append("%s: engine exit code %s (%s)" % (s["dest"], rc, (etxt.splitlines() or ["no stderr"])[-1][:200]))
                    if result["rc"] == RC_VERIFY:
                        result["rc"] = RC_ENGINE
                elif mode == "dry" and rc == 0 and (pl["new"] + pl["updated"]) != len(plan["copy"]):
                    problems.append("%s: the engine's dry list (%d files) disagrees with the plan (%d files)"
                                    % (s["dest"], pl["new"] + pl["updated"], len(plan["copy"])))
            mset["engine"] = engine

            if mode == "run":
                # OBSERVE the destination for every file the engine was given.
                changed_during, vanished, missing, mismatch, good_rows = [], [], [], [], []
                versioned = 0
                for rel in plan["copy"]:
                    sv = src["files"][rel]
                    try:
                        dsz = os.stat(os.path.join(plan["dest_dir"], rel)).st_size
                    except OSError:
                        dsz = None
                    if dsz == sv[0]:
                        observed_ok.add(rel)
                        good_rows.append((rel, sv))
                        continue
                    try:
                        cur = os.stat(os.path.join(s["src"], rel), follow_symlinks=False)
                        if (cur.st_size, cur.st_mtime_ns, cur.st_ctime_ns) != tuple(sv):
                            changed_during.append(rel)
                        elif dsz is None:
                            missing.append(rel)
                        else:
                            mismatch.append(rel)
                    except OSError:
                        vanished.append(rel)
                for rel in plan["copy_dirs"]:
                    if not os.path.isdir(os.path.join(plan["dest_dir"], rel)) and os.path.isdir(os.path.join(s["src"], rel)):
                        missing.append(rel + "/")
                good_rows += [(rel, src["files"][rel]) for rel in plan["hash_equal"]]
                index.put_many(s["dest"], good_rows, time.time())
                bdir = os.path.join(croot, "versions", stamp, *s["dest"].split("/"))
                if os.path.isdir(bdir):
                    versioned = len(walk(bdir)["files"])
                # sha256 sample, source against destination
                pool = [r for r in observed_ok if r not in changed_during]
                random.seed(stamp + s["dest"])
                sample = random.sample(pool, min(c["hash_sample"], len(pool)))
                bad_hash = []
                for rel in sample:
                    try:
                        sp = os.path.join(s["src"], rel)
                        before = os.stat(sp)
                        a = sha256_of(sp)
                        drel = plan["dfiles"][ckey(rel)][0] if ckey(rel) in plan["dfiles"] else rel
                        b = sha256_of(os.path.join(plan["dest_dir"], drel))
                        after = os.stat(sp)
                        if a != b and (before.st_mtime_ns, before.st_size) == (after.st_mtime_ns, after.st_size) \
                                and (before.st_size, before.st_mtime_ns, before.st_ctime_ns) == tuple(src["files"][rel]):
                            bad_hash.append(rel)
                    except OSError:
                        pass
                if missing:
                    problems.append("%s: %d file(s) NOT at the destination (first: %s)" % (s["dest"], len(missing), missing[0]))
                if mismatch:
                    problems.append("%s: %d file(s) differ in size at the destination (first: %s)" % (s["dest"], len(mismatch), mismatch[0]))
                if bad_hash:
                    problems.append("%s: sha256 sample: %d of %d differ (first: %s)" % (s["dest"], len(bad_hash), len(sample), bad_hash[0]))
                say("    observed after the copy: %d of %d source files at the destination with the same size; changed at the "
                    "source during the run: %d (copied again tomorrow); vanished at the source: %d; previous copies kept: %d; "
                    "sha256 sample %d/%d agree"
                    % (len(observed_ok), len(src["files"]), len(changed_during), len(vanished), versioned,
                       len(sample) - len(bad_hash), len(sample)))
                mset.update({"changed_during_run": len(changed_during), "vanished_during_run": len(vanished),
                             "missing": missing[:50], "size_mismatch": mismatch[:50], "versioned": versioned,
                             "hash_sample": len(sample), "hash_sample_bad": bad_hash[:20]})
                totals["changed_during_run"] += len(changed_during)
                totals["vanished"] += len(vanished)
                totals["versioned"] += versioned
                tolerated = set(changed_during) | set(vanished)
            else:
                tolerated = set(plan["copy"])
            tbl = folder_table(plan, observed_ok)
            mset["folders"] = tbl
            say("    %-34s %10s %14s | %10s %14s | %s" % ("top-level folder", "src files", "src bytes", "dst files", "dst bytes", "dst-only (kept)"))
            for top in sorted(tbl):
                r = tbl[top]
                flag = "" if (r["src_files"] == r["dst_files"] and r["src_bytes"] == r["dst_bytes"]) else ("  <- to copy" if mode == "dry" else "  <- differs")
                say("    %-34s %10d %14d | %10d %14d | %d%s" % (top[:34], r["src_files"], r["src_bytes"], r["dst_files"], r["dst_bytes"], r["dst_only_files"], flag))
                totals["dst_files"] += r["dst_files"]
                totals["dst_bytes"] += r["dst_bytes"]
                totals["dst_only_files"] += r["dst_only_files"]
            if mode == "run":
                short = [rel for rel in src["files"] if rel not in observed_ok and rel not in tolerated]
                if short and not (missing or mismatch):
                    problems.append("%s: %d source file(s) are not accounted for at the destination (first: %s)" % (s["dest"], len(short), short[0]))
            # symlinks are recorded, per set
            mset["symlink_list_file"] = None
            if src["links"]:
                lp = os.path.join(ctx.manifest_dir, "%s_%s_%s_symlinks.tsv" % (stamp, mode, s["dest"].replace("/", "__")))
                with open(lp, "w", encoding="utf-8", errors="surrogateescape") as fh:
                    for rel in sorted(src["links"]):
                        fh.write("%s\t%s\n" % (rel, src["links"][rel]))
                mset["symlink_list_file"] = lp
            manifest["sets"].append(mset)
            if result["rc"] in (RC_STALLED, RC_CAP):
                break
    except KeyboardInterrupt:
        problems.append("interrupted by signal %s" % interrupted["sig"])
        result["rc"] = RC_ENGINE
    except Refused as e:
        problems.append(str(e))
        result["rc"] = e.rc
    except Exception as e:     # an unexpected error is a FAILED run with its reason recorded, never a silent one
        problems.append("unexpected error: %s: %s" % (type(e).__name__, e))
        result["rc"] = RC_ENGINE
    finally:
        signal.alarm(0)
        index.close()

    # FAIL CLOSED, BUT SAY SO: a folder beside the listed projects is never swept in, and never silently skipped.
    unlisted = []
    parent = c.get("report_unlisted_under")
    if parent and os.path.isdir(parent):
        listed = set(os.path.realpath(x["src"]) for x in c["sets"])
        try:
            for name in sorted(os.listdir(parent)):
                full = os.path.join(parent, name)
                if not os.path.isdir(full) or os.path.islink(full) or os.path.realpath(full) in listed:
                    continue
                if name.casefold() in ctx.info["forbid"]:
                    say("not this seat's (never backed up from here): %s" % full)
                else:
                    unlisted.append(full)
                    say("NOT LISTED in seats/%s.conf, so NOT backed up: %s" % (ctx.seat, full))
        except OSError as e:
            say("could not list %s: %s" % (parent, e))
    manifest["unlisted_folders"] = unlisted
    manifest["totals"] = totals
    manifest["problems"] = problems
    manifest["finished"] = time.time()
    manifest["finished_local"] = now_local_str(time.time())
    manifest["seconds"] = round(time.time() - started, 1)
    good = not problems
    manifest["good"] = good if mode == "run" else None
    mpath = os.path.join(ctx.manifest_dir, "%s_%s_manifest.json" % (stamp, mode))
    with open(mpath, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1, sort_keys=True)
        fh.write("\n")
    say("--- totals: source in scope %d files, %s; to copy %d files, %s (%d new, %d changed); %d symlinks recorded; "
        "%d entries excluded; took %.0f s"
        % (totals["src_files"], fmt_bytes(totals["src_bytes"]), totals["copy_files"], fmt_bytes(totals["copy_bytes"]),
           totals["new"], totals["changed"], totals["symlinks"], totals["excluded_entries"], time.time() - started))
    say("manifest: %s" % mpath)
    if mode == "dry":
        # An ESTIMATE, from two rates measured on this NAS box on 2026-11-27 (seats/<seat>.conf est_*): the armed
        # nas_push leg moved 8.9 files a second (three nights of its own logs), and the share lists 390 entries a
        # second. Small files dominate, so the estimate goes by file count, not bytes.
        est_copy_h = totals["copy_files"] / c["est_files_per_s"] / 3600.0
        est_list_min = (totals["src_files"] / c["est_list_per_s"]) / 60.0
        say("estimate (not a measurement of this run): copying %d files at about %.1f files/s takes about %.1f hours; "
            "after the first copy, each night lists about %d destination files at about %.0f entries/s (about %.0f minutes) "
            "and copies only what changed" % (totals["copy_files"], c["est_files_per_s"], est_copy_h, totals["src_files"],
                                              c["est_list_per_s"], est_list_min))
        manifest["estimate"] = {"copy_hours": round(est_copy_h, 1), "nightly_listing_minutes": round(est_list_min, 0),
                                "files_per_s": c["est_files_per_s"], "list_entries_per_s": c["est_list_per_s"]}
        if problems:
            say("DRY RUN finished WITH PROBLEMS (a real run would fail):")
            for p in problems:
                say("  - %s" % p)
            rcode = result["rc"]
        else:
            say("DRY RUN finished: a real run would copy the files above. Nothing was written to the NAS.")
            rcode = RC_OK
    else:
        try:
            for client, croot in client_roots.items():
                cm = dict(manifest)
                cm["sets"] = [m for m in manifest["sets"] if m["client"] == client]
                with open(os.path.join(croot, "manifests", "%s_manifest.json" % stamp), "w", encoding="utf-8") as fh:
                    json.dump(cm, fh, indent=1, sort_keys=True)
                for m in cm["sets"]:
                    if m.get("symlink_list_file"):
                        with open(m["symlink_list_file"], "rb") as a, open(os.path.join(croot, "manifests", os.path.basename(m["symlink_list_file"])), "wb") as b:
                            b.write(a.read())
                if good:
                    with open(os.path.join(croot, "runs", "RUN_%s_COMPLETE.txt" % stamp), "w", encoding="utf-8") as fh:
                        fh.write("complete and counted %s: manifest manifests/%s_manifest.json\n" % (now_local_str(time.time()), stamp))
        except OSError as e:
            problems.append("could not write the manifest or the completion marker on the NAS: %s" % e)
            good = False
        if good:
            say("GOOD: every in-scope source file is at the destination and counted. Nothing was deleted on either side.%s"
                % ((" NOTE: %d file(s) were NOT backed up because their names differ only in case from a sibling (listed in the manifest)."
                    % totals["case_collision_files"]) if totals["case_collision_files"] else ""))
            ctx.note_attempt("good", "counted equal", {"stamp": stamp, "manifest": mpath, "trigger": manifest["trigger"],
                                                       "counts": totals, "seconds": manifest["seconds"]})
            rcode = RC_OK
        else:
            say("FAILED (exit code alone is never success):")
            for p in problems:
                say("  - %s" % p)
            status = {RC_CAP: "killed-cap", RC_STALLED: "stalled"}.get(result["rc"], "failed")
            ctx.note_attempt(status, "; ".join(problems)[:900], {"stamp": stamp, "manifest": mpath})
            rcode = result["rc"]
        lock_release(ctx)
    with open(run_log, "w", encoding="utf-8", errors="surrogateescape") as fh:
        fh.write("\n".join(lines) + "\n")
    out("log: %s" % run_log)
    return rcode


def sum_by_cat(excluded):
    d = {}
    for (cat, _), v in excluded.items():
        d[cat] = d.get(cat, 0) + v[0]
    return d


# ── nightly: what the scheduler calls ─────────────────────────────────────────────────────────────────────────
def nightly_decide(ctx, st, lock):
    """Pure decision. Returns (action, reason): action in run | skip."""
    c = ctx.conf
    o, cl, inw = window_for(ctx.now, c["fire_h"], c["fire_m"], c["window_hours"])
    lg = st.get("last_good")
    if lock is not None and lock.get("alive"):
        return ("skip", "a run is in progress (pid %s, started %s)" % (lock.get("pid"), lock.get("started_local")))
    if lg and lg["time"] >= o:
        return ("skip", "already backed up for the window that opened %s (good at %s)" % (now_local_str(o), lg["time_local"]))
    if not inw:
        if c["late_fire"] == "run":
            return ("run-late", "outside the window, late_fire=run: catching up the window that opened %s" % now_local_str(o))
        return ("skip", "fired outside the nightly window (%s to %s); it never runs outside its window on its own. "
                        "The missed night is caught up when the next window opens" % (now_local_str(o), now_local_str(cl)))
    if lg:
        missed = int((o - lg["time"]) // 86400)
        return ("run", "no good backup since the window opened %s (last good %s%s)"
                % (now_local_str(o), lg["time_local"], ", %d night(s) missed: catching up" % missed if missed >= 1 else ""))
    return ("run", "no good backup on record")


def cmd_nightly(ctx, decide_only=False):
    ctx.mkdirs()
    nlog = os.path.join(ctx.log_dir, "nightly.log")

    def record(msg):
        out(msg)
        with open(nlog, "a", encoding="utf-8") as fh:
            fh.write("%s %s\n" % (now_local_str(ctx.now), msg))

    try:
        ctx.load_conf()
        st = ctx.read_state()
        action, reason = nightly_decide(ctx, st, lock_status(ctx))
    except Refused as e:
        record("nightly[%s]: REFUSED: %s" % (ctx.seat, e))
        return e.rc
    record("nightly[%s]: %s: %s" % (ctx.seat, action.upper(), reason))
    if decide_only:
        return RC_OK
    st["last_fire"] = {"time": ctx.now, "time_local": now_local_str(ctx.now), "decision": action, "reason": reason}
    ctx.write_state(st)
    rc = RC_OK
    if action == "run":
        rc = cmd_backup(ctx, "run", scheduled=True)
    elif action == "run-late":
        rc = cmd_backup(ctx, "run", scheduled=True, out_of_sequence="late-fire (late_fire=run in the seat conf)")
    record("nightly[%s]: finished rc=%s" % (ctx.seat, rc))
    # The three-day check is ALSO called here, but it does not live only here: the launcher and doctor call it too.
    cmd_watch(ctx, "flag")
    return rc


# ── watch: the three-day flag (runs on the caller's clock, never needs the NAS) ───────────────────────────────
def cmd_watch(ctx, action, card_id=None):
    st = ctx.read_state()
    if action == "mark-armed":
        if st.get("armed_at"):
            out("already marked armed at %s; unchanged" % now_local_str(st["armed_at"]))
            return RC_OK
        st["armed_at"] = ctx.now
        ctx.write_state(st)
        out("marked armed at %s: the three-day clock for seat %s starts here" % (now_local_str(ctx.now), ctx.seat))
        return RC_OK
    lg, la, lf = st.get("last_good"), st.get("last_attempt"), st.get("last_fire")
    if os.path.exists(ctx.hold_file) and action in ("check", "flag"):
        # HELD is a deliberate state, set by the coordinator; it is not a missed backup, so it raises no card.
        # It is still said out loud at every call (and doctor reports HELD), so a forgotten hold stays visible.
        out("nas-backup watch[%s]: HELD: %s exists, so real runs are refused by design and the three-day flag is not raised%s"
            % (ctx.seat, ctx.hold_file, "; last good backup %s" % lg["time_local"] if lg else "; no good backup on record"))
        return RC_OK
    attempt_times = [a["time"] for a in st.get("recent_attempts", [])]
    first_attempt = min(attempt_times) if attempt_times else None
    ref, ref_what = None, None
    if lg:
        ref, ref_what = lg["time"], "the last good backup"
    elif st.get("armed_at"):
        ref, ref_what = st["armed_at"], "arming (no good backup yet)"
    elif first_attempt is not None:
        ref, ref_what = first_attempt, "the first recorded attempt (no good backup yet)"
    if ref is None:
        out("nas-backup watch[%s]: NOT ARMED on this seat: no state on record (no arming mark, no attempt, no good backup). Nothing to flag." % ctx.seat)
        return RC_OK
    hours = (ctx.now - ref) / 3600.0
    reasons, grouped, order = [], {}, []
    for a in st.get("recent_attempts", []):          # newest first
        if a["time"] > ref and a["status"] != "good":
            why = a["reason"].replace("REFUSED \u2014 ", "").replace("; nothing run", "")[:220]
            if why not in grouped:
                grouped[why] = [0, a["time_local"][:16]]
                order.append(why)
            grouped[why][0] += 1
    for why in order:
        n, latest = grouped[why]
        reasons.append("%d attempt%s, latest %s: %s" % (n, "" if n == 1 else "s", latest, why))
    if not reasons:
        if lf and lf["time"] > ref:
            reasons.append("no run was attempted; the last scheduler fire (%s) decided: %s" % (lf["time_local"][:16], lf["reason"][:160]))
        else:
            reasons.append("no attempt and no scheduler fire is on record since then: the job did not fire (machine asleep or off, or the job is not loaded)")
    ls = lock_status(ctx)
    lock_note = ""
    if ls is not None:
        lock_note = " | lock: pid %s %s" % (ls.get("pid"), "RUNNING since %s" % ls.get("started_local") if ls.get("alive") else "STALE since %s (nas_backup.sh --clear-stale-lock)" % ls.get("started_local"))
    overdue = hours >= FLAG_AFTER_HOURS
    skipped_note = ""
    if lg and (lg.get("counts") or {}).get("case_collision_files"):
        skipped_note = " | %d file(s) not backed up (names differ only in case)" % lg["counts"]["case_collision_files"]
    out("nas-backup watch[%s]: %s; %.1f h since %s (%s)%s%s%s"
        % (ctx.seat, "OVERDUE" if overdue else "ok", hours, ref_what, now_local_str(ref),
           "; last attempt %s %s" % (la["time_local"][:16], la["status"]) if la else "; no attempt on record", lock_note, skipped_note))
    gap_key = "%d" % int(ref)
    flag = st.get("flag") or {}
    cid = "nas-backup-overdue-%s-%s" % (ctx.seat, time.strftime("%Y%m%d", time.localtime(ref)))
    if action == "mark-raised":
        if not overdue:
            raise Refused("REFUSED — nothing is overdue, so there is no card to mark raised")
        st["flag"] = {"gap_key": gap_key, "card_id": card_id or cid, "printed_at": flag.get("printed_at") if flag.get("gap_key") == gap_key else None,
                      "raised": True, "raised_at": ctx.now}
        ctx.write_state(st)
        out("marked: card %s raised for the gap since %s" % (card_id or cid, now_local_str(ref)))
        return RC_OK
    if not overdue:
        return RC_OK
    if action == "check":
        return 3
    same_gap = flag.get("gap_key") == gap_key
    if action == "flag" and same_gap:
        out("  the card command for this gap was already issued at %s (card %s, raised on the board: %s). Not issued again. "
            "To see it again: nas_backup_watch.sh --reprint"
            % (now_local_str(flag["printed_at"]) if flag.get("printed_at") else "an earlier check", flag.get("card_id"), "yes" if flag.get("raised") else "NOT YET RECORDED"))
        return 3
    try:
        ctx.load_conf()
        cproj = ctx.conf["card_client_project"]
    except Refused:
        cproj = "WED"
    dq = os.path.join(ctx.tree, "2_Project_Files", "tools", "decision_queue.sh")
    title = "No NAS backup of the %s seat for %d days: approve one now, outside the nightly window?" % (ctx.info["cap"], int(hours // 24))
    bluf = ("The nightly copy of the %s seat's folder and projects to the NAS has not completed since %s (%s, %d hours ago). "
            "What happened: %s. The nightly job keeps trying inside its window either way. Nothing is deleted by a backup: it only copies."
            % (ctx.info["cap"], now_local_str(ref), ref_what, int(hours), " | ".join(reasons[:4])))
    argv = [dq, "add", "--id", cid, "--client-project", cproj, "--title", title, "--bluf", bluf,
            "--option", "a:Approve an out-of-sequence backup now:The seat runs one backup straight away, outside the nightly window, and reports the counted result",
            "--option", "b:Wait for tonight's window:Nothing runs now; the nightly job tries again at its usual time",
            "--recommended", "b", "--default-action", "b: wait for tonight's window; no backup runs outside the window without your word"]
    out("FLAG: no good backup for %d hours (threshold %d). ONE decision card for Kam. This tool PRINTS the command and never runs it:" % (int(hours), FLAG_AFTER_HOURS))
    out("CARD-COMMAND: " + " ".join(shlex.quote(a) for a in argv))
    out("After adding the card: nas_backup_watch.sh --mark-raised %s . If Kam rules a: nas_backup.sh --run --out-of-sequence %s" % (cid, cid))
    if action == "flag":
        st["flag"] = {"gap_key": gap_key, "card_id": cid, "printed_at": ctx.now, "raised": False}
        ctx.write_state(st)
    return 3


# ── scan: census numbers for the configured sets (reads only) ────────────────────────────────────────────────
def cmd_scan(ctx, measure_excluded):
    ctx.load_conf()
    for s in ctx.conf["sets"]:
        rules = Rules(ctx, s["dest"])
        no_measure = set(p for d, p in ctx.conf["exclude_path"] if d == s["dest"])
        t0 = time.time()
        w = walk(s["src"], rules, measure_excluded=measure_excluded, no_measure=no_measure)
        b = sum(v[0] for v in w["files"].values())
        out("SET %s/%s <- %s : in scope %d files, %d bytes (%s), %d folders, %d symlinks, %d specials, %d read errors [%.1fs]"
            % (s["client"], s["dest"], s["src"], len(w["files"]), b, fmt_bytes(b), len(w["dirs"]), len(w["links"]), len(w["specials"]), len(w["errors"]), time.time() - t0))
        tops = {}
        for rel, v in w["files"].items():
            r = tops.setdefault(top_of(rel), [0, 0])
            r[0] += 1
            r[1] += v[0]
        for top in sorted(tops, key=lambda k: -tops[k][1]):
            out("    %-40s %9d files %16d bytes (%s)" % (top[:40], tops[top][0], tops[top][1], fmt_bytes(tops[top][1])))
        out("  excluded:")
        for (cat, pat), v in sorted(w["excluded"].items(), key=lambda kv: -kv[1][2]):
            out("    %-22s %-28s %7d entries%s" % (cat, pat, v[0], ("  %9d files %16d bytes (%s)" % (v[1], v[2], fmt_bytes(v[2]))) if measure_excluded else ""))
        seen, coll = {}, 0
        for rel in list(w["files"]) + list(w["dirs"]):
            k = ckey(rel)
            if k in seen and seen[k] != rel:
                coll += 1
                if coll <= 8:
                    out("  CASE COLLISION (neither is copied): %s | %s" % (seen[k], rel))
            seen[k] = rel
        out("  case collisions in scope: %d" % coll)
        big = sorted(w["files"].items(), key=lambda kv: -kv[1][0])[:12]
        out("  largest in-scope files:")
        for rel, v in big:
            out("    %14d  %s" % (v[0], rel))
        for e in w["errors"][:5]:
            out("  READ ERROR: %s" % e)
    return RC_OK


def main(argv):
    import argparse
    ap = argparse.ArgumentParser(prog="nb_core.py")
    ap.add_argument("command", choices=["backup", "nightly", "watch", "scan", "clear-stale-lock", "window"])
    ap.add_argument("--seat", required=True)
    ap.add_argument("--tree", required=True)
    ap.add_argument("--now", default=None, help="TEST MODE ONLY: the clock, as epoch seconds")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--scheduled", action="store_true")
    ap.add_argument("--out-of-sequence", default=None)
    ap.add_argument("--max-seconds", type=int, default=None)
    ap.add_argument("--no-hash", action="store_true")
    ap.add_argument("--decide-only", action="store_true")
    ap.add_argument("--measure-excluded", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--flag", action="store_true")
    ap.add_argument("--reprint", action="store_true")
    ap.add_argument("--mark-raised", default=None)
    ap.add_argument("--mark-armed", action="store_true")
    a = ap.parse_args(argv)
    try:
        ctx = Ctx(a.seat, a.tree, a.now)
        if a.command == "backup":
            if a.run and a.dry:
                raise Refused("give --run or --dry, not both")
            return cmd_backup(ctx, "run" if a.run else "dry", scheduled=a.scheduled, out_of_sequence=a.out_of_sequence,
                              max_seconds=a.max_seconds, no_hash=a.no_hash)
        if a.command == "nightly":
            return cmd_nightly(ctx, decide_only=a.decide_only)
        if a.command == "watch":
            if a.mark_armed:
                return cmd_watch(ctx, "mark-armed")
            if a.mark_raised:
                return cmd_watch(ctx, "mark-raised", a.mark_raised)
            if a.flag:
                return cmd_watch(ctx, "flag")
            if a.reprint:
                return cmd_watch(ctx, "reprint")
            return cmd_watch(ctx, "check")
        if a.command == "scan":
            return cmd_scan(ctx, a.measure_excluded)
        if a.command == "clear-stale-lock":
            return cmd_clear_stale_lock(ctx)
        if a.command == "window":
            ctx.load_conf()
            o, c, inw = window_for(ctx.now, ctx.conf["fire_h"], ctx.conf["fire_m"], ctx.conf["window_hours"])
            out("window opens %s, closes %s, in window now: %s" % (now_local_str(o), now_local_str(c), inw))
            return RC_OK
    except Refused as e:
        err("nas-backup: %s" % e)
        return e.rc
    return RC_REFUSED


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
