#!/usr/bin/env python3
# nb_core.py — the engine behind nas_backup.sh / nas_backup_nightly.sh / nas_backup_watch.sh.  ROUND 3 (2026-11-27).
#
# THE ONE RULE (Kam, card wed-nas-backup-second-nogo-round3-1127, 2026-11-27 16:40: "unproven means failed").
# A night is GOOD only if every file in the plan made when its set starts is PROVEN at the destination with the
# source's content. Anything else fails the night and is named. There is no special case that counts toward GOOD:
#   - a planned file that cannot be read at proof time, for ANY reason, is NOT DELIVERED. The one exception is a
#     file DELETED from the source: its parent folder must be listable and the name absent from that listing, twice;
#     such files are counted and named, and above a small stated limit the night fails (deleted_allowed below);
#   - a set whose plan holds zero files fails the night, on a first run too;
#   - a destination copy the nightly sample finds wrong loses its index row at once and is re-sent in the same run;
#     if the repair is not proven the night fails, and it keeps failing until the file is proven;
#   - proof is saved as it goes (the engine works in chunks; each chunk is proven and indexed before the next).
# Round 2's file is kept at round2/nb_core.py.round2, round 1's at round1/nb_core.py.round1.
#
# ROUND 4 (2026-11-27, ANSWER-6: six fixes after the third check, and nothing else). Round 3's file is kept at
# round3/nb_core.py.round3. Each fix is marked "ROUND 4" where it sits:
#   1. two sets of one client whose destination names NEST, and one destination name under two clients: refused
#      at load (load_conf);
#   2. a SYMLINK anywhere in the destination chain is refused (ensure_dest_chain), and before each set the real
#      paths of its destination, versions, manifests, runs and _tmp_incoming must lie inside the seat's own
#      nightly-backup folder (dest_escape);
#   3. a planned file that has gained a second HARD LINK is kept out of the chunk it would travel in, and at
#      proof time it is a verdict of its own that is never proven (hard_linked_now, prove_arrival);
#   4. what the secret-shape rule leaves out is written BY NAME, per set, to a file on the DRIVE only
#      (write_left_out_list); that file is never copied to the share and never part of a backup;
#   5. the deletion proof also needs the planned path not to resolve, and the parent folder to be the very
#      folder that was listed (source_deleted);
#   6. the HOLD is tested before the conf is read (cmd_backup).
#
# WED-170, Kam 2026-11-27 12:03: a NIGHTLY, STAGGERED, COPY-ONLY backup of one coordinator seat's folder and its
# working projects to the DEV-Working NAS, with next-night catch-up and a three-day flag.
# Round 2 answers the independent check of 2026-11-27 (0_Brain/reference/2026-11-27_qa-nasbackup/verdict.md, NO GO)
# under Wednesday's rulings in ANSWER-2.md. Round 1's file is kept at round1/nb_core.py.round1.
#
# WHAT A RUN MAY CLAIM (finding 1). GOOD means: every in-scope source file is PROVEN at the destination with the
# source's content. Proof for a file the run sent = sha256 of the source equals sha256 of the destination, with
# the source unchanged across the read. Proof for a file the run did not send = it is at the destination with the
# same size AND (the local index holds its exact stat from an earlier proof, OR its sha256 was compared now).
# A file enters the index ONLY when proven. The engine's exit code proves nothing either way: 23 and 24 are
# survived only because every listed path is then proven one by one; anything unproven FAILS the run and is NAMED
# in the run's last lines and in the state file the watch reads.
#
# WHAT A RUN MAY CARRY (findings 2, 3). Secrets are excluded by SHAPE, case-insensitively (secret_shape below):
# over-exclusion is the accepted cost. A regular file with more than one hard link is skipped and named. The
# other client's own name, and other seats' names inside the seat's tree, are excluded case-insensitively by
# containment; a set= source is resolved with realpath first and refused if any component contains a forbidden
# token. The other client's PROJECT names are reported per token, not excluded (Kam's ruling nas-shared-folders-
# owner, 2026-09-11, as read by Wednesday in ANSWER-2: the general folders are this seat's records).
#
# COPY ONLY. The source drive is only read. On the NAS nothing is deleted: a replaced file, and an entry whose
# type changed, is MOVED into versions/<run stamp>/ first. The rsync argv is built here and checked for
# deletion-capable flags before every call. No rm, unlink or rmtree anywhere: a released lock and a damaged
# state file are MOVED aside.
#
# Python 3.9-compatible, standard library only. Never discards stderr.
import datetime
import fnmatch
import hashlib
import json
import os
import random
import re
import shlex
import signal
import sqlite3
import stat
import subprocess
import sys
import time
import unicodedata

SCHEMA = 3
LANE = os.path.dirname(os.path.realpath(__file__))
REAL_NAS_ROOT = "/Volumes/DEV-Working"
BACKUP_FOLDER = "nightly-backup"
FLAG_AFTER_HOURS = 72
MAX_PASSES = 3            # engine passes per chunk: one copy, then up to two re-sends of files that changed meanwhile
RECENT_ATTEMPTS = 40      # ten nights of four fires
PROOF_BATCH = 200         # proven files are committed to the index at least every this many (finding 8, round 2 check)
CHUNK_BYTES = 2 << 30     # an engine chunk ends at chunk_files files (conf) or this many bytes, whichever comes first
WATCHDOG_MARGIN = 900     # seconds after the cap at which the whole run is stopped (a blocked read on the share)
FUTURE_SLACK = 300        # a recorded time more than this far ahead of the clock makes the state file DAMAGED

# ── THE ALLOW-LIST. Only seats listed here can run at all. Tuesday and Friday are NOT listed: each gets an entry
# only when her own coordinator has confirmed her scope (proposed/INSTRUCTIONS-for-other-seats.md, step 1).
#   clients     = the only client folders this seat may write into, as <NAS>/<Client>/<SeatCap>/.
#   forbid      = tokens (lower case). A set= source whose REAL path has a component CONTAINING one is refused.
#   other_client_tokens = a name containing one is excluded at any depth, in every set (any case).
#   other_seat_tokens   = the same, but only inside the seat's own tree (in project folders these words hit
#                         library files such as a date library's nextFriday.js).
SEATS = {
    "wednesday": {
        "cap": "Wednesday",
        "clients": ["Secuura", "General"],
        "forbid": ["datasec", "tuesday", "friday"],
        "other_client_tokens": ["datasec"],
        "other_seat_tokens": ["tuesday", "friday"],
    },
}

# ── SECRETS, BY SHAPE (finding 2). Every test is on the lower-cased name of ONE path component. ────────────────
KEY_EXTENSIONS = (".pem", ".key", ".p12", ".pfx", ".ppk", ".jks", ".keystore", ".kdbx", ".skey")
# ROUND 3 (second check, finding 2): more key and certificate containers, matched at the END of the name only.
KEY_EXTENSIONS_END = (".p8", ".der", ".pkcs12", ".ovpn", ".mobileprovision", ".kdb", ".agekey", ".gpg", ".asc", ".cer",
                      ".crt", ".vkey", ".addr", ".wallet", ".priv")
SECRET_STORE_NAMES = (".ssh", ".aws", ".azure", ".gh-config", ".gnupg", ".kube",
                      ".docker", ".auth", "gcloud", ".secret", ".secrets")
SECRET_FILE_NAMES = (".netrc", ".npmrc", ".pypirc", ".pgpass", ".git-credentials", "credentials.json",
                     "secrets.json", "secrets.yaml", "secrets.yml", "service_principal_entries.json",
                     # round 3: the conventional names that still travelled, and the two real files by their names
                     "local.settings.json", "application_default_credentials.json", ".dockercfg", ".vault-token",
                     ".boto", ".s3cfg", ".terraformrc", ".yarnrc.yml", "credentials", "auth.json", "token.json",
                     "tokens.json", "accesstokens.json", "azureprofile.json", "wallet.dat", "env.backup", "env.bak")
SSH_KEY_PREFIXES = ("id_rsa", "id_ed25519", "id_ecdsa", "id_dsa")
CREDENTIAL_DATA_EXT = (".json", ".yaml", ".yml", ".csv", ".ini", ".xml", ".txt", ".toml", ".db")
_RX_SERVICE_ACCOUNT = re.compile(r"^service[-_ ]?account.*\.json$|-sa\.json$|sa[-_]key.*\.json$")
_RX_PRIVATE_KEY = re.compile(r"priv(ate)?[-_. ]?key|signing[-_.]?key|seed[-_ ]?phrase|recovery[-_ ]?phrase|mnemonic")
_RX_SECRET_DOT = re.compile(r"^secrets?\.[a-z0-9]+$")


def secret_shape(name):
    """Returns the name of the secret shape this path component has, or None. Fails closed: a name that merely
    looks like a secret is excluded (.envrc, .env1, prod.env.bak, 'old_3_Access_Keys', presentation.key)."""
    n = name.lower()
    if "4_credentials" in n or "3_access_keys" in n:
        return "credentials-folder-name"
    if n.startswith(".env") or ".env." in n or n.endswith(".env"):
        return "env-file"
    for e in KEY_EXTENSIONS:
        if n.endswith(e) or (e + ".") in n or (e + " ") in n:
            return "key-or-certificate"
    if ".tfstate" in n:
        return "terraform-state"
    for p in SSH_KEY_PREFIXES:
        if n.startswith(p):
            return "ssh-key"
    if n in SECRET_STORE_NAMES:
        return "credential-store"
    if (n in SECRET_FILE_NAMES or n.startswith("client_secret") or n.startswith("msal_token_cache")
            or n.startswith("github_deploy") or "deploy_key" in n or "deploy-key" in n
            or n.endswith("_deploy_rw") or n.endswith("_deploy_ro")):
        return "credential-file"
    # ── ROUND 3: conventional credential names (BEST-EFFORT by ruling: a name rule cannot be complete) ──
    if n.endswith(KEY_EXTENSIONS_END) or n.startswith("keystore") or n.startswith("utc--"):
        return "key-or-certificate"
    if ".tfvars" in n:
        return "terraform-variables"
    if _RX_PRIVATE_KEY.search(n):
        return "private-key-or-wallet-name"
    if (n.startswith("htpasswd") or n.startswith(".htpasswd") or n.startswith("kubeconfig") or ".kubeconfig" in n
            or _RX_SERVICE_ACCOUNT.search(n) or _RX_SECRET_DOT.match(n)
            or ("credential" in n and n.endswith(CREDENTIAL_DATA_EXT))):
        return "credential-file"
    return None


# ── OTHER FIXED EXCLUSIONS (lower-case globs against the lower-cased name). "files" = the glob applies to files
# only (finding 12: a real FOLDER named ._something is not AppleDouble litter). ─────────────────────────────────
EXCLUDES = [
    ("git", "any", [".git"]),
    ("quarantine", "any", ["_quarantine_*"]),
    ("live-database", "any", ["pgdata-*"]),
    ("rebuildable", "any", ["node_modules", "worktrees", "qa-worktrees*", "deploy-worktrees", "wt-*", ".venv", "venv",
                            "__pycache__", ".next", ".turbo", ".pytest_cache", ".mypy_cache", ".ruff_cache",
                            ".hypothesis", ".pnpm-store"]),
    ("system", "any", [".ds_store", ".spotlight-v100", ".fseventsd", ".trashes", ".temporaryitems",
                       ".smbdelete*", ".unison*", "#recycle"]),
    ("system", "files", ["._*"]),
    # ROUND 4 (finding 4): this tool's own lists of what the secret-shape rule left out hold the NAMES of real
    # secret files. They live on the drive, inside the seat's tree; they must never travel to the share.
    ("own-left-out-list", "files", ["*_left_out_by_secret_shape.tsv"]),
]
LEFT_OUT_SUFFIX = "_left_out_by_secret_shape.tsv"          # must match the pattern in the line above
FORBIDDEN_RSYNC = ("--del", "--delete", "--remove-source-files", "--force", "--inplace", "--prune-empty-dirs",
                   "--existing", "--ignore-existing")

RC_OK, RC_REFUSED, RC_HELD, RC_CAP, RC_ENGINE, RC_LOCKED, RC_STALLED, RC_VERIFY, RC_DELETING = 0, 2, 3, 4, 5, 6, 7, 8, 9
RC_OVERDUE, RC_OVERDUE_RAISED, RC_DAMAGE_NOTICE = 3, 4, 5


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


def test_root():
    """NB_TEST_ROOT turns on TEST MODE; honoured only for a directory under /private/tmp, so a test can never be
    pointed at the real NAS or the real lane state."""
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


_PROBE_PLAIN = ("a", "readme", "1", "x_y-z", "makefile", "src", "notes")
_PROBE_DOTTED = ("a.txt", "readme.md", "x.y.z", "1.0", "index.html", "run.sh", "data.json")


def match_everything(pattern):
    """True for a glob that excludes (nearly) every name: `*`, `?*`, `**`, `*.*`, `[!~]*`, `*[a-z0-9]*` (finding 4
    of both checks: such a line emptied the backup and the run said GOOD). Tested against ordinary probe names: a
    pattern that matches every plain probe, or every dotted one, is refused. What a pattern does to the real tree
    is caught by the other rule: a set whose plan holds zero files fails the night."""
    pt = pattern.strip().lower()
    if pt == "" or all(ch in "*?" for ch in pt):
        return True
    return (all(fnmatch.fnmatchcase(x, pt) for x in _PROBE_PLAIN)
            or all(fnmatch.fnmatchcase(x, pt) for x in _PROBE_DOTTED))


def contains(outer, inner):
    """True when realpath `inner` is `outer` or lies inside it."""
    return inner == outer or inner.startswith(outer.rstrip("/") + "/")


class Ctx(object):
    def __init__(self, seat, tree, now=None):
        if seat not in SEATS:
            raise Refused("REFUSED — seat '%s' has no confirmed scope in this lane: only %s can run. Tuesday and Friday "
                          "run nothing from here until each coordinator has confirmed her own scope "
                          "(proposed/INSTRUCTIONS-for-other-seats.md)" % (seat, ", ".join(sorted(SEATS))))
        self.seat = seat
        self.info = SEATS[seat]
        self.troot = test_root()
        if now is not None and not self.troot:
            raise Refused("--now is a TEST-MODE parameter (NB_TEST_ROOT unset); the real clock is never supplied by hand")
        self.now = float(now) if now is not None else time.time()
        self.tree = os.path.realpath(tree)
        if os.path.basename(self.tree).lower() != seat:
            raise Refused("the tree %s is not a '%s' tree: its folder name is the discriminator and it disagrees with the seat"
                          % (self.tree, seat))
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
        self.tokens_file = os.path.join(self.lane, "seats", seat + ".tokens")
        self.conf = None
        self.state_note = None
        self.readonly = False          # a dry run: a damaged state file or index is REPORTED, never moved or rewritten
        self.found_by = "unknown caller"
        self.damage_file = os.path.join(self.state_dir, "DAMAGE_NOTICE_" + seat + ".jsonl")

    def mkdirs(self):
        for d in (self.state_dir, self.log_dir, self.manifest_dir):
            os.makedirs(d, exist_ok=True)

    # ── conf: FAILS CLOSED (finding 4) ──
    def load_conf(self):
        if not os.path.isfile(self.conf_file):
            raise Refused("no seat configuration at %s" % self.conf_file)
        c = {"sets": [], "exclude_name": [], "exclude_name_in": [], "exclude_path": [], "allow_empty": [], "status": "unconfirmed",
             "fire": None, "window_hours": "5", "late_fire": "refuse", "min_free_gib": "200", "max_seconds": "18000",
             "stall_seconds": "900", "io_timeout": "1800", "hash_sample": "40", "rsync": "/opt/homebrew/bin/rsync",
             "card_client_project": "WED", "source_volume": None, "nas_root": None, "report_unlisted_under": None,
             "max_files": "400000", "max_drop_fraction": "0.5", "est_files_per_s": "8.9", "est_list_per_s": "390",
             "chunk_files": "200", "max_deleted_files": "5", "max_deleted_fraction": "0.001"}
        scalar_seen = {}
        with open(self.conf_file, "r", encoding="utf-8") as fh:
            raw_lines = fh.read().split("\n")
        content = [(n, ln.strip()) for n, ln in enumerate(raw_lines, 1) if ln.strip() and not ln.strip().startswith("#")]
        # THE END MARKER: the last content line must be `END lines=<N>`, N = the content lines before it. A conf
        # that lost its tail, or any line, no longer adds up, and is refused instead of silently widening the scope.
        if not content or not re.match(r"^END lines=\d+$", content[-1][1]):
            raise Refused("REFUSED — %s does not end with its `END lines=<N>` marker: the file is truncated or was edited "
                          "without updating the count; nothing run" % self.conf_file)
        declared = int(content[-1][1].split("=")[1])
        if declared != len(content) - 1:
            raise Refused("REFUSED — %s declares %d lines and holds %d: a line was lost or added without updating the "
                          "END marker; nothing run" % (self.conf_file, declared, len(content) - 1))
        for n, line in content[:-1]:
            if line.startswith("END "):
                raise Refused("%s line %d: a second END marker" % (self.conf_file, n))
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
            elif k == "allow_empty":
                c["allow_empty"].append(v)
            elif k == "exclude_name_in":
                parts = v.split("|")
                if len(parts) != 2 or "/" in parts[1]:
                    raise Refused("%s line %d: exclude_name_in=<dest name>|<name pattern>" % (self.conf_file, n))
                c["exclude_name_in"].append((parts[0], parts[1]))
            elif k == "exclude_path":
                parts = v.split("|")
                if len(parts) != 2:
                    raise Refused("%s line %d: exclude_path=<dest name>|<path inside the set>" % (self.conf_file, n))
                c["exclude_path"].append((parts[0], parts[1].strip("/")))
            elif k in c:
                # A KEY GIVEN TWICE is refused (second check, finding 14: `status=unconfirmed` followed by
                # `status=confirmed` ran, with no warning; which line wins must never be a guess).
                if k in scalar_seen:
                    raise Refused("REFUSED — %s gives the key '%s' twice (lines %d and %d): which one wins is never "
                                  "guessed; nothing run" % (self.conf_file, k, scalar_seen[k], n))
                scalar_seen[k] = n
                c[k] = v
            else:
                raise Refused("%s line %d: unknown key '%s'" % (self.conf_file, n, k))
        if c["status"] != "confirmed":
            raise Refused("the configuration %s says status=%s: not confirmed; nothing run" % (self.conf_file, c["status"]))
        if c["late_fire"] not in ("refuse", "run"):
            raise Refused("late_fire must be 'refuse' or 'run'")
        try:
            hh, mm = c["fire"].split(":")
            c["fire_h"], c["fire_m"] = int(hh), int(mm)
            assert 0 <= c["fire_h"] <= 23 and 0 <= c["fire_m"] <= 59
            for k in ("window_hours", "min_free_gib", "max_drop_fraction", "est_files_per_s", "est_list_per_s",
                      "max_deleted_fraction"):
                c[k] = float(c[k])
            for k in ("max_seconds", "stall_seconds", "io_timeout", "hash_sample", "max_files", "chunk_files",
                      "max_deleted_files"):
                c[k] = int(c[k])
            assert c["est_files_per_s"] > 0 and c["est_list_per_s"] > 0 and 0 < c["max_drop_fraction"] <= 1
            assert c["chunk_files"] >= 1 and c["hash_sample"] >= 0
            assert 0 <= c["max_deleted_files"] <= 100 and 0 <= c["max_deleted_fraction"] <= 0.01
        except Exception:
            raise Refused("%s: fire must be HH:MM and the numeric keys must be numbers in range" % self.conf_file)
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
        for p in c["exclude_name"] + [p for _, p in c["exclude_name_in"]]:
            if match_everything(p):
                raise Refused("REFUSED — the exclusion pattern '%s' in %s matches every name: it would empty the backup; "
                              "nothing run" % (p, self.conf_file))
        seen = set()
        for s in c["sets"]:
            if s["client"] not in self.info["clients"]:
                raise Refused("REFUSED — client folder '%s' is not on seat %s's allow-list %s: a seat writes only "
                              "inside its own client's folder" % (s["client"], self.seat, self.info["clients"]))
            if not s["dest"] or s["dest"].startswith("/") or any(p in ("", ".", "..") for p in s["dest"].split("/")):
                raise Refused("REFUSED — set destination name '%s' must be a plain relative name" % s["dest"])
            if any(secret_shape(p) for p in s["dest"].split("/")):
                raise Refused("REFUSED — set destination name '%s' is secret-shaped" % s["dest"])
            key = (s["client"], s["dest"].casefold())
            if key in seen:
                raise Refused("two sets share the destination %s/%s" % (s["client"], s["dest"]))
            seen.add(key)
            if not s["src"].startswith("/"):
                raise Refused("set source must be absolute: %s" % s["src"])
            # FORBIDDEN ROOTS (finding 3): the REAL path, every component, by CONTAINMENT, any case. So a symlinked
            # parent, `DataSec` and `Datasec-archive` are refused like `Datasec`.
            s["real"] = os.path.realpath(s["src"])
            for cand in (s["src"], s["real"]):
                for comp in [p for p in cand.split("/") if p]:
                    for f in self.info["forbid"]:
                        if f in comp.casefold():
                            raise Refused("REFUSED — source %s (real path %s) has the component '%s', which contains '%s': "
                                          "that is another seat's or another client's material, never backed up by seat %s"
                                          % (s["src"], s["real"], comp, f, self.seat))
        # ROUND 4 (third check, finding 1): NESTED DESTINATIONS. Two sets of ONE client whose destination names
        # nest (`X` and `X/sub`) write into each other's folder: each night the inner set overwrote the outer
        # set's file of the same path, both proofs passed in turn, and every night said GOOD. Refused at load,
        # like a nested source. Compared part by part (split at `/`), each part NFC-normalised and case-folded.
        # (Finding 5, its smallest form:) the SAME destination name under TWO clients is refused too: the
        # baseline of the fall rule, allow_empty and the index are kept by the destination name alone, so two
        # sets of one name would share one row in each of the three.
        def dparts(s):
            return tuple(unicodedata.normalize("NFC", p).casefold() for p in s["dest"].split("/"))
        for i, a in enumerate(c["sets"]):
            for b in c["sets"][i + 1:]:
                pa, pb = dparts(a), dparts(b)
                n = min(len(pa), len(pb))
                if a["client"] == b["client"] and pa[:n] == pb[:n]:
                    raise Refused("REFUSED — the destinations of two sets of client %s NEST: '%s' and '%s' (one name is a "
                                  "path prefix of the other). The inner set would write inside the outer set's folder and "
                                  "the two would overwrite each other's files every night; give them names that do not "
                                  "nest; nothing run" % (a["client"], a["dest"], b["dest"]))
                if a["client"] != b["client"] and pa == pb:
                    raise Refused("REFUSED — the destination name '%s' is used under two clients (%s and %s): the baseline "
                                  "of the fall rule, allow_empty and the index are kept by that name alone, so the two sets "
                                  "would share them; give one of them another name; nothing run"
                                  % (a["dest"], a["client"], b["client"]))
        # FORBIDDEN ROOTS, BOTH DIRECTIONS (second check, finding 3: a set= naming the PARENT of the seat trees
        # carried TUESDAY and FRIDAY to the NAS). A source is refused when it IS a forbidden root, lies INSIDE one,
        # or is an ANCESTOR of one, by real path.
        roots = self.forbidden_roots(c["source_volume"])
        for s in c["sets"]:
            for r, why in roots:
                if contains(r, s["real"]) or contains(s["real"], r):
                    raise Refused("REFUSED — source %s (real path %s) %s the forbidden root %s (%s): never backed up by "
                                  "seat %s. Name the folders you mean one by one; nothing run"
                                  % (s["src"], s["real"], "is, or is inside," if contains(r, s["real"]) else "is an ANCESTOR of",
                                     r, why, self.seat))
            if s["real"] != self.tree and contains(s["real"], self.tree):
                raise Refused("REFUSED — source %s is an ANCESTOR of this seat's own tree %s: a set that wide sweeps in "
                              "whatever lies beside the tree; nothing run" % (s["src"], self.tree))
        # One set inside another is allowed only when the outer set excludes exactly that path (so nothing is
        # copied twice, and nothing arrives by a second route under another client's folder).
        for a in c["sets"]:
            for b in c["sets"]:
                if a is not b and contains(a["real"], b["real"]):
                    relp = os.path.relpath(b["real"], a["real"])
                    if a["real"] == b["real"] or (a["dest"], relp) not in c["exclude_path"]:
                        raise Refused("REFUSED — the set %s (%s) lies inside the set %s (%s) and that set has no "
                                      "exclude_path=%s|%s line: the same files would travel twice; nothing run"
                                      % (b["dest"], b["src"], a["dest"], a["src"], a["dest"], relp))
        dests = [s["dest"] for s in c["sets"]]
        for dest in c["allow_empty"]:
            if dest not in dests:
                raise Refused("allow_empty names the set '%s', which is not defined" % dest)
        for dest, p in c["exclude_name_in"]:
            if dest not in dests:
                raise Refused("exclude_name_in names the set '%s', which is not defined" % dest)
        for dest, p in c["exclude_path"]:
            if any(ch in p for ch in "*?[]\\") or not p or ".." in p.split("/"):
                raise Refused("exclude_path '%s' must be a literal path inside the set (no wildcards)" % p)
            if dest not in dests:
                raise Refused("exclude_path names the set '%s', which is not defined" % dest)
            src = [s["src"] for s in c["sets"] if s["dest"] == dest][0]
            if os.path.isdir(src) and not os.path.lexists(os.path.join(src, p)):
                raise Refused("REFUSED — exclude_path=%s|%s names nothing: %s does not exist. A mistyped exclusion "
                              "silently widens the backup, so it is refused by name; nothing run"
                              % (dest, p, os.path.join(src, p)))
        self.conf = c
        return c

    def forbidden_roots(self, volume):
        """The folders this seat must never back up, as REAL paths with the reason: the other seats' trees (the
        folders beside this seat's tree, and at the top of the drive, whose names contain another seat's name) and
        the other client's folders (a name containing the client's name at the top of the drive or one level
        below it, where the client folders live: `!CODING/Datasec`, `Notes (MASTER)/Datasec`). The seat's own tree
        is not searched: inside it those names are excluded by the walker, at every depth."""
        info, roots, seen = self.info, [], set()

        def consider(parent, tokens_why):
            try:
                names = sorted(os.listdir(parent))
            except OSError as e:
                raise Refused("REFUSED — cannot list %s to find the forbidden roots (%s); nothing run" % (parent, e))
            subs = []
            for name in names:
                full = os.path.join(parent, name)
                if not os.path.isdir(full):
                    continue
                real = os.path.realpath(full)
                hit = None
                for tokens, why in tokens_why:
                    for t in tokens:
                        if t in name.casefold():
                            hit = "%s: its name contains '%s'" % (why, t)
                if hit:
                    if real not in seen and real != self.tree:
                        seen.add(real)
                        roots.append((real, hit))
                elif not os.path.islink(full):
                    subs.append(full)
            return subs

        both = [(info["other_seat_tokens"], "another seat's tree"), (info["other_client_tokens"], "another client's folder")]
        vol = os.path.realpath(volume)
        level1 = consider(vol, both) if os.path.isdir(vol) else []
        parent = os.path.dirname(self.tree)
        if os.path.realpath(parent) != vol and os.path.isdir(parent):
            consider(parent, both)
        for d in level1:
            if os.path.realpath(d) != self.tree and not os.path.basename(d).startswith("."):
                try:
                    consider(d, both)
                except Refused:
                    pass          # a top-level folder this user cannot list holds nothing this seat could name as a source
        return roots

    def load_tokens(self):
        """seats/<seat>.tokens: the OTHER clients' project names, for REPORTING. token=<text> is matched as a
        contained string; word=<text> must be bounded by non-alphanumerics (so `mps` does not swallow `lamps`)."""
        toks = []
        if not os.path.isfile(self.tokens_file):
            return toks
        with open(self.tokens_file, "r", encoding="utf-8") as fh:
            for raw in fh:
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                v = v.strip().lower()
                if k.strip() == "token" and v:
                    toks.append((v, re.compile(re.escape(v))))
                elif k.strip() == "word" and v:
                    toks.append((v + " (whole word)", re.compile(r"(?<![a-z0-9])" + re.escape(v) + r"(?![a-z0-9])")))
        return toks

    def client_root(self, client):
        if client not in self.info["clients"]:
            raise Refused("REFUSED — '%s' is not on seat %s's allow-list" % (client, self.seat))
        return os.path.join(self.conf["nas_root"], client, self.info["cap"], BACKUP_FOLDER)

    # ── state: ONE json file per seat on the drive. A damaged one is MOVED aside and said out loud (finding 9) ──
    def fresh_state(self):
        return {"schema": SCHEMA, "seat": self.seat, "armed_at": None, "first_attempt_at": None, "last_good": None,
                "last_attempt": None, "last_fire": None, "recent_attempts": [], "flag": None, "damage": None,
                "held_seen": False, "clock_floor": None}

    def validate_state(self, st):
        """Raises ValueError unless `st` is a state this tool could have written (second check, finding 13: valid
        JSON that is not a valid state gave a traceback; a last_good in the FUTURE made every night a skip and the
        watch say ok with negative hours). A time ahead of the clock by more than FUTURE_SLACK is damage."""
        def num(v):
            return isinstance(v, (int, float)) and not isinstance(v, bool)

        def when(v, what, future=True):
            if not num(v):
                raise ValueError("%s is not a time" % what)
            if future and v > self.now + FUTURE_SLACK:
                raise ValueError("%s is in the FUTURE (%s; the clock says %s)" % (what, now_local_str(v), now_local_str(self.now)))

        if not isinstance(st, dict) or not isinstance(st.get("seat"), str):
            raise ValueError("not a state object")
        for k in ("armed_at", "first_attempt_at", "clock_floor"):
            if st.get(k) is not None:
                when(st[k], k)
        for k in ("last_good", "last_attempt", "last_fire"):
            v = st.get(k)
            if v is None:
                continue
            if not isinstance(v, dict) or not isinstance(v.get("time_local"), str):
                raise ValueError("%s lacks its fields" % k)
            when(v.get("time"), k + ".time", future=(k == "last_good"))
            if k == "last_attempt" and not isinstance(v.get("status"), str):
                raise ValueError("last_attempt has no status")
            if k == "last_fire" and not isinstance(v.get("reason"), str):
                raise ValueError("last_fire has no reason")
        ra = st.get("recent_attempts", [])
        if not isinstance(ra, list):
            raise ValueError("recent_attempts is not a list")
        for a in ra:
            if (not isinstance(a, dict) or not num(a.get("time")) or not isinstance(a.get("time_local"), str)
                    or not isinstance(a.get("status"), str) or not isinstance(a.get("reason"), str)):
                raise ValueError("an entry of recent_attempts lacks its fields")
        lg = st.get("last_good")
        if lg is not None and lg.get("set_counts") is not None and not isinstance(lg.get("set_counts"), dict):
            raise ValueError("last_good.set_counts is not a table")
        for k in ("flag", "damage"):
            if st.get(k) is not None and not isinstance(st[k], dict):
                raise ValueError("%s is not a record" % k)

    def note_damage(self, what, moved_to, error):
        """THE DAMAGE NOTICE (second check, finding 6: a damaged state file found first by the nightly job spent its
        flag-worthy exit on a log no seat reads, and doctor said nothing for three more days). Whoever finds damage
        appends one line here. The watch exits 5 and doctor's block fails hard while this file exists; only a seat
        clears it, with `nas_backup_watch.sh --ack-damage` (it is moved aside, never deleted)."""
        os.makedirs(self.state_dir, exist_ok=True)
        with open(self.damage_file, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"time": self.now, "time_local": now_local_str(self.now), "what": what,
                                 "moved_to": moved_to, "error": str(error)[:200], "found_by": self.found_by},
                                sort_keys=True) + "\n")

    def damage_notices(self):
        """The unacknowledged damage notices, oldest first. An unreadable notice file is itself a notice."""
        if not os.path.lexists(self.damage_file):
            return []
        res = []
        try:
            with open(self.damage_file, "r", encoding="utf-8") as fh:
                for ln in fh:
                    if ln.strip():
                        try:
                            d = json.loads(ln)
                            res.append(d if isinstance(d, dict) else {"what": "unreadable notice line"})
                        except ValueError:
                            res.append({"what": "unreadable notice line"})
        except OSError as e:
            res.append({"what": "the damage notice file itself could not be read", "error": str(e)[:120]})
        return res or [{"what": "an empty damage notice file"}]

    def read_state(self):
        if not os.path.exists(self.state_file):
            return self.fresh_state()
        try:
            with open(self.state_file, "r", encoding="utf-8") as fh:
                st = json.load(fh)
            self.validate_state(st)
        except (ValueError, OSError) as e:
            if self.readonly:
                # A dry run writes nothing: the damaged file stays where it is and the run SAYS so.
                self.state_note = ("STATE FILE DAMAGED: %s could not be used (%s). This dry run leaves it where it is and "
                                   "reads on with an empty state; the next real caller will move it aside"
                                   % (self.state_file, str(e)[:120]))
                return self.fresh_state()
            q = os.path.join(self.state_dir, "_quarantine_%s" % time.strftime("%Y-%m-%d"))
            os.makedirs(q, exist_ok=True)
            dst = os.path.join(q, "%s.json.damaged.%s.%d" % (self.seat, time.strftime("%H%M%S"), os.getpid()))
            os.rename(self.state_file, dst)
            st = self.fresh_state()
            st["damage"] = {"time": self.now, "time_local": now_local_str(self.now), "moved_to": dst,
                            "error": str(e)[:160]}
            st["first_attempt_at"] = self.now
            self.write_state(st)
            self.note_damage("state file", dst, e)
            self.state_note = ("STATE FILE DAMAGED: %s could not be used (%s). It was MOVED to %s (not deleted) and a "
                               "clean state was started: the record of the last good backup is gone, so the three-day "
                               "clock restarts now. A damage notice is kept for doctor until a seat acknowledges it"
                               % (self.state_file, str(e)[:120], dst))
            return st
        if st.get("seat") != self.seat:
            raise Refused("REFUSED — state file %s belongs to seat '%s', not '%s'" % (self.state_file, st.get("seat"), self.seat))
        return st

    def write_state(self, st):
        os.makedirs(self.state_dir, exist_ok=True)
        tmp = self.state_file + ".tmp.%d" % os.getpid()
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(st, fh, indent=1, sort_keys=True)
            fh.write("\n")
        os.replace(tmp, self.state_file)

    def hold_lifted(self, st):
        """Called by anything that runs with NO hold file in place. If all the state has seen so far is the hold,
        the three-day clock starts NOW, once (second check, finding 10: refusals under the hold started the
        clock, so lifting the hold for the first copy would have raised OVERDUE at once). Returns True if it did."""
        if not (st.get("held_seen") or legacy_held(st)):
            return False
        st["held_seen"] = False
        for a in st.get("recent_attempts") or []:
            if a.get("status") == "refused" and "HOLD_" in a.get("reason", "") and "HELD" in a.get("reason", ""):
                a["status"] = "held"          # a pre-round-3 record of a refusal under the hold, relabelled
        st["clock_floor"] = self.now
        if not st.get("last_good"):
            st["first_attempt_at"] = self.now
        return True

    def note_attempt(self, status, reason, extra=None):
        st = self.read_state()
        a = {"time": self.now, "time_local": now_local_str(self.now), "status": status, "reason": reason,
             "pid": os.getpid()}
        if extra:
            a.update(extra)
        st["last_attempt"] = a
        if status == "held":
            # A refusal under the HOLD is not an attempt at a backup: it never starts the three-day clock
            # (second check, finding 10), and the first un-held attempt or check restarts it (clock_floor).
            st["held_seen"] = True
        else:
            self.hold_lifted(st)
            if not st.get("first_attempt_at"):
                st["first_attempt_at"] = self.now      # stored ONCE, never rolled (finding 5)
        if status != "running":
            st["recent_attempts"] = ([{"time_local": a["time_local"], "time": a["time"], "status": status,
                                       "reason": reason}] + st.get("recent_attempts", []))[:RECENT_ATTEMPTS]
        if status == "good":
            st["last_good"] = a
            st["damage"] = None
        self.write_state(st)


def legacy_held(st):
    """True when everything a pre-round-3 state file has on record is refusals under the HOLD (they were stored as
    `refused` and they started the clock: the real lane's state of 2026-11-27 is exactly this)."""
    ra = st.get("recent_attempts") or []
    return (bool(ra) and not st.get("last_good") and any(a.get("status") == "refused" for a in ra) and all(
        a.get("status") in ("refused", "held") and "HOLD_" in a.get("reason", "") and "HELD" in a.get("reason", "") for a in ra))


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
    """os.listdir returns the REAL names (the 2026-08-25 incident: a case-folding share answers for 'Datasec' when
    the folder is 'datasec'). Returns 'exact', 'absent', or the differing real name."""
    try:
        names = os.listdir(parent)
    except OSError as e:
        raise Refused("cannot list %s: %s" % (parent, e))
    if name in names:
        return "exact"
    for n in names:
        if unicodedata.normalize("NFC", n).casefold() == unicodedata.normalize("NFC", name).casefold():
            return n
    return "absent"


def ensure_dest_chain(root_existing, rel_parts, create):
    """Walks root_existing/rel_parts one level at a time. A level that exists must be spelled EXACTLY so.
    Returns (path, existed_fully, deepest_existing_path)."""
    cur = root_existing
    existed = True
    deepest = root_existing
    # ROUND 4 (third check, finding 2): A SYMLINK IS NEVER A LEVEL OF THE DESTINATION. os.path.isdir follows a
    # link, so `<NAS>/General/Wednesday -> <NAS>/Datasec/x` was accepted and the whole backup was written into
    # another client's folder. The level the walk starts from (the client folder) is held to the same rule.
    if os.path.islink(root_existing):
        raise Refused("REFUSED — %s on the NAS is a SYMLINK (to %s): this tool writes only into real folders, never "
                      "through a link; nothing written" % (root_existing, os.readlink(root_existing)))
    for part in rel_parts:
        chk = real_name_check(cur, part) if os.path.isdir(cur) else "absent"
        nxt = os.path.join(cur, part)
        if chk == "exact":
            if os.path.islink(nxt):
                raise Refused("REFUSED — %s on the NAS is a SYMLINK (to %s): this tool writes only into real folders of "
                              "its own destination, never through a link; nothing written" % (nxt, os.readlink(nxt)))
            if not os.path.isdir(nxt):
                raise Refused("REFUSED — %s exists on the NAS but is not a folder" % nxt)
            if existed:
                deepest = nxt
        elif chk == "absent":
            existed = False
            if create:
                os.mkdir(nxt)
        else:
            raise Refused("REFUSED — the NAS has '%s' where '%s' is expected under %s: the names differ in CASE. "
                          "A case-folding share would mix the two (2026-08-25 incident); nothing written"
                          % (chk, part, cur))
        cur = nxt
    return cur, existed, deepest


DEST_SUBFOLDERS = ("versions", "manifests", "runs", "_tmp_incoming")


def dest_escape(ctx, client, dest=None):
    """ROUND 4 (third check, finding 2). Returns None when every folder this tool writes for `client` resolves
    INSIDE the seat's own folder, realpath(<NAS>/<Client>/<Seat>/nightly-backup); else one sentence naming the
    first that does not. Looked at: the set's destination (current/<dest>, when `dest` is given), versions,
    manifests, runs and _tmp_incoming. A path that does not exist yet resolves to itself, which is inside."""
    croot = ctx.client_root(client)
    base = os.path.realpath(croot)
    paths = [os.path.join(croot, sub) for sub in DEST_SUBFOLDERS]
    if dest is not None:
        paths.insert(0, os.path.join(croot, "current", *dest.split("/")))
    for p in paths:
        rp = os.path.realpath(p)
        if rp == base or not contains(base, rp):
            return ("%s resolves to %s, which is OUTSIDE this seat's own destination folder %s (a symlink on the "
                    "share leads out of it)" % (p, rp, base))
    return None


def ckey(rel):
    return unicodedata.normalize("NFC", rel).casefold()


# ── the walker: ONE implementation of what is in scope ────────────────────────────────────────────────────────
class Rules(object):
    def __init__(self, ctx, s):
        self.fixed = [(cat, kind, p) for cat, kind, pl in EXCLUDES for p in pl]
        self.tokens = [("other-client", t) for t in ctx.info["other_client_tokens"]]
        self.seat_names = set(ctx.info["other_seat_tokens"])
        if os.path.realpath(s["src"]) == ctx.tree:
            self.tokens += [("other-seat", t) for t in ctx.info["other_seat_tokens"]]
        self.conf_names = [p.lower() for p in ctx.conf["exclude_name"]]
        self.conf_names += [p.lower() for d, p in ctx.conf["exclude_name_in"] if d == s["dest"]]
        self.paths = set(p for d, p in ctx.conf["exclude_path"] if d == s["dest"])
        # THIS TOOL'S OWN RUN STATE (the lock, the index, their quarantine) is never part of a backup: the index is
        # rewritten while the run proves files, so as a planned file it could only be chased, and it is a cache.
        # logs/ and manifests/ are records and stay in.
        self.own_state = None
        sd, root = os.path.realpath(ctx.state_dir), os.path.realpath(s["src"])
        if sd != root and contains(root, sd):
            self.own_state = os.path.relpath(sd, root)

    def match(self, name, rel, is_dir):
        shape = secret_shape(name)
        if shape:
            return ("secret", shape)
        n = name.lower()
        for cat, kind, p in self.fixed:
            if (kind == "any" or not is_dir) and fnmatch.fnmatchcase(n, p):
                return (cat, p)
        for cat, t in self.tokens:
            if t in n:
                return (cat, "*%s*" % t)
        if is_dir and n in self.seat_names:
            # In EVERY set a FOLDER named exactly as another seat is that seat's (round 3; inside project folders
            # the looser contained-word rule is not applied, because there those words are library file names).
            return ("other-seat", "a folder named exactly %s" % n)
        for p in self.conf_names:
            if fnmatch.fnmatchcase(n, p):
                return ("conf-name", p)
        if rel in self.paths:
            return ("conf-path", rel)
        if self.own_state is not None and rel == self.own_state:
            return ("own-run-state", rel)
        return None


def walk(top, rules=None):
    """dict(files={rel:(size,mtime_ns,ctime_ns)}, dirs=set, links={rel:target}, specials=[rel],
    excluded={(cat,pattern):entries}, hardlinks=[rel], errors=[str]). Never follows a symlink."""
    res = {"files": {}, "dirs": set(), "links": {}, "specials": [], "excluded": {}, "hardlinks": [], "errors": [],
           "secret_names": [], "dir_ids": {}}
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
                    is_link = e.is_symlink()
                    is_dir = (not is_link) and e.is_dir(follow_symlinks=False)
                    m = rules.match(e.name, r, is_dir) if rules else None
                    if m:
                        res["excluded"][m] = res["excluded"].get(m, 0) + 1
                        if m[0] == "secret":
                            res["secret_names"].append((r, m[1]))          # ROUND 4: named on the drive, never on the share
                        continue
                    if is_link:
                        try:
                            res["links"][r] = os.readlink(e.path)
                        except OSError as ex:
                            res["links"][r] = "?unreadable: %s" % ex
                    elif is_dir:
                        res["dirs"].add(r)
                        if rules is not None:
                            # ROUND 4 (finding 6): which folder this IS, for the deletion proof (source walks only)
                            ds = e.stat(follow_symlinks=False)
                            res["dir_ids"][r] = (ds.st_dev, ds.st_ino)
                        stack.append((r, e.path))
                    elif e.is_file(follow_symlinks=False):
                        s = e.stat(follow_symlinks=False)
                        if rules is not None and s.st_nlink > 1:
                            # A second name for the same file: the other name may sit inside a secrets folder this
                            # walk never enters (finding 2). Skipped, counted and NAMED in the manifest.
                            res["excluded"][("hard-link", "link count > 1")] = res["excluded"].get(("hard-link", "link count > 1"), 0) + 1
                            res["hardlinks"].append(r)
                            continue
                        res["files"][r] = (s.st_size, s.st_mtime_ns, s.st_ctime_ns)
                    else:
                        res["specials"].append(r)
                except OSError as ex:
                    res["errors"].append("%s: %s" % (e.path, ex))
    return res


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


def stat3(path):
    s = os.stat(path, follow_symlinks=False)
    return (s.st_size, s.st_mtime_ns, s.st_ctime_ns)


# ── window arithmetic: LOCAL WALL TIME (finding 12, daylight saving). The clock is a parameter. ───────────────
def wall(epoch):
    return datetime.datetime.fromtimestamp(epoch)


def window_for(now, fire_h, fire_m, window_hours):
    """The most recent window opening at or before `now`, as naive LOCAL wall-clock datetimes. Wall time, not
    elapsed seconds: on the night the clocks change a 02:30-05:30 window is still 02:30 to 05:30 on the wall,
    so a fire at 03:20 is inside it and it still closes at the 05:30 shift change."""
    w = wall(now)
    o = w.replace(hour=fire_h, minute=fire_m, second=0, microsecond=0)
    if w < o:
        o = o - datetime.timedelta(days=1)
    c = o + datetime.timedelta(hours=window_hours)
    return (o, c, o <= w < c)


def wstr(dt):
    return dt.strftime("%Y-%m-%d %H:%M")


# ── lock (mkdir on the drive). A stale lock is REPORTED, never removed silently. The engine runs in its OWN
# process group, recorded in the lock, so "is anything of this seat still copying" has an answer (finding 8). ──
def proc_started(pid):
    r = subprocess.run(["/bin/ps", "-o", "lstart=", "-p", str(pid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       universal_newlines=True)
    return r.stdout.strip()


def pid_alive(owner):
    """Alive only if the pid exists AND it started when the lock says it did: a reused pid is not the holder."""
    pid = owner.get("pid")
    if not pid:
        return False
    try:
        os.kill(int(pid), 0)
    except (OSError, ValueError):
        return False
    return proc_started(pid) == owner.get("pid_started")


def pid_exists(pid):
    try:
        os.kill(int(pid), 0)
    except (OSError, ValueError, TypeError):
        return False
    return True


def engine_processes(ctx, owner):
    """Engine processes of THIS seat still alive: the recorded process group, plus any rsync whose command line
    names this seat's destination folder. Returns a list of 'pid command' strings."""
    hits = []
    pg = (owner or {}).get("engine_pgid")
    # A REUSED GROUP ID (second check, finding 15): the group leader's pid is the group id. If a process with that
    # pid is alive but started at another time than the lock recorded, the id now belongs to something unrelated.
    if pg and (owner or {}).get("engine_started") and pid_exists(pg) and proc_started(pg) != owner.get("engine_started"):
        pg = None
    r = subprocess.run(["/bin/ps", "-axo", "pid=,pgid=,command="], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       universal_newlines=True)
    needles = []
    if ctx.conf:
        needles = [os.path.join(ctx.conf["nas_root"], c, ctx.info["cap"], BACKUP_FOLDER) + "/" for c in ctx.info["clients"]]
    for ln in r.stdout.splitlines():
        parts = ln.split(None, 2)
        if len(parts) < 3 or int(parts[0]) == os.getpid():
            continue
        if pg and parts[1] == str(pg):
            hits.append("%s %s" % (parts[0], parts[2][:80]))
        elif "rsync" in parts[2].split(" ")[0] and any(n in parts[2] for n in needles):
            hits.append("%s %s" % (parts[0], parts[2][:80]))
    return hits


def lock_status(ctx):
    """None if free; else the owner dict with alive (holder process), engines (list), fresh (taken this moment)."""
    if not os.path.isdir(ctx.lock_dir):
        return None
    info = {"pid": None, "started_local": "unknown"}
    op = os.path.join(ctx.lock_dir, "owner.json")
    readable = False
    try:
        with open(op, "r") as fh:
            info = json.load(fh)
        readable = True
    except (OSError, ValueError):
        pass
    try:
        age = time.time() - os.stat(ctx.lock_dir).st_mtime
    except OSError:
        age = 0
    # A lock directory with no owner record yet, a few seconds old, is a run that has JUST taken it (finding 12:
    # the loser of a simultaneous start was told STALE about a live run).
    info["fresh"] = (not readable) and age < 15
    info["alive"] = readable and pid_alive(info)
    info["engines"] = engine_processes(ctx, info) if readable else []
    return info


def write_owner(ctx, mode, engine_pgid=None):
    tmp = os.path.join(ctx.lock_dir, "owner.json.tmp")
    with open(tmp, "w") as fh:
        json.dump({"pid": os.getpid(), "pid_started": proc_started(os.getpid()), "started": time.time(),
                   "started_local": now_local_str(time.time()), "mode": mode, "seat": ctx.seat,
                   "engine_pgid": engine_pgid, "engine_started": proc_started(engine_pgid) if engine_pgid else None}, fh)
    os.replace(tmp, os.path.join(ctx.lock_dir, "owner.json"))


def lock_take(ctx, mode):
    os.makedirs(ctx.state_dir, exist_ok=True)
    try:
        os.mkdir(ctx.lock_dir)
    except FileExistsError:
        ls = lock_status(ctx) or {}
        if ls.get("alive") or ls.get("fresh"):
            raise Refused("REFUSED — another run holds the lock %s (pid %s, started %s); nothing run"
                          % (ctx.lock_dir, ls.get("pid") or "just starting", ls.get("started_local")), RC_LOCKED)
        if ls.get("engines"):
            raise Refused("REFUSED — the run that held the lock %s is gone (pid %s) but its copy engine is STILL RUNNING "
                          "(%s). Nothing run; the lock stays until that engine has ended"
                          % (ctx.lock_dir, ls.get("pid"), "; ".join(ls["engines"][:2])), RC_LOCKED)
        raise Refused("REFUSED — STALE lock at %s: pid %s (started %s) is not running. It is NOT removed for you. "
                      "After checking no copy is running: nas_backup.sh --clear-stale-lock (moves it into "
                      "state/_quarantine_<date>/)" % (ctx.lock_dir, ls.get("pid"), ls.get("started_local")), RC_LOCKED)
    write_owner(ctx, mode)


def lock_release(ctx):
    if not os.path.isdir(ctx.lock_dir):
        return
    dst_parent = os.path.join(ctx.state_dir, "released_locks")
    os.makedirs(dst_parent, exist_ok=True)
    os.rename(ctx.lock_dir, os.path.join(dst_parent, "%s.%s.%d.lock.d" % (ctx.seat, time.strftime("%Y%m%d-%H%M%S"), os.getpid())))


def cmd_clear_stale_lock(ctx):
    try:
        ctx.load_conf()
    except Refused:
        pass          # the lock can be judged without a readable conf (the process-group check still applies)
    ls = lock_status(ctx)
    if ls is None:
        out("no lock at %s" % ctx.lock_dir)
        return RC_OK
    if ls.get("alive") or ls.get("fresh"):
        raise Refused("REFUSED — the lock is LIVE (pid %s, started %s): not stale, not moved" % (ls.get("pid"), ls.get("started_local")), RC_LOCKED)
    if ls.get("engines"):
        raise Refused("REFUSED — the holder (pid %s) is gone but %d copy-engine process(es) of this seat are STILL RUNNING "
                      "(%s). The lock is not moved while anything is still writing: wait for them to end"
                      % (ls.get("pid"), len(ls["engines"]), "; ".join(ls["engines"][:3])), RC_LOCKED)
    q = os.path.join(ctx.state_dir, "_quarantine_%s" % time.strftime("%Y-%m-%d"))
    os.makedirs(q, exist_ok=True)
    dst = os.path.join(q, "%s.stale.%s.%d.lock.d" % (ctx.seat, time.strftime("%H%M%S"), os.getpid()))
    os.rename(ctx.lock_dir, dst)
    out("stale lock (pid %s, started %s) MOVED to %s" % (ls.get("pid"), ls.get("started_local"), dst))
    return RC_OK


# ── index: a cache of PROVEN arrivals. Rebuildable: losing it costs one night of sha256 comparison. ───────────
class Index(object):
    """note: one plain line when the index file was found damaged (None otherwise)."""

    def __init__(self, ctx, readonly):
        path = ctx.index_file
        self.readonly = readonly
        self.db = None
        self.note = None
        if readonly and not os.path.exists(path):
            return
        try:
            self._open(path)
        except sqlite3.Error as e:
            # A DAMAGED INDEX (second check, finding 7: a traceback, the lock left behind, every night until a
            # person moved the file). It is a cache: move it aside, say so in one line, start an empty one.
            if self.db is not None:
                self.db.close()
            self.db = None
            if readonly:
                self.note = ("INDEX DAMAGED: %s could not be read (%s). This dry run leaves it where it is and treats "
                             "it as empty" % (path, str(e)[:80]))
                return
            q = os.path.join(ctx.state_dir, "_quarantine_%s" % time.strftime("%Y-%m-%d"))
            os.makedirs(q, exist_ok=True)
            dst = os.path.join(q, "%s.index.sqlite.damaged.%s.%d" % (ctx.seat, time.strftime("%H%M%S"), os.getpid()))
            os.rename(path, dst)
            ctx.note_damage("index", dst, e)
            self.note = ("INDEX DAMAGED: %s could not be read (%s). It was MOVED to %s (not deleted) and an empty one "
                         "was started: tonight every file already on the NAS is compared by sha256 again"
                         % (path, str(e)[:80], dst))
            self._open(path)

    def _open(self, path):
        self.db = sqlite3.connect(path)
        self.db.execute("SELECT count(*) FROM sqlite_master").fetchone()        # a file that is not a database fails HERE
        if not self.readonly:
            self.db.execute("CREATE TABLE IF NOT EXISTS files (setname TEXT, rel TEXT, size INTEGER, mtime_ns INTEGER, "
                            "ctime_ns INTEGER, copied_at REAL, PRIMARY KEY (setname, rel))")
            self.db.execute("CREATE TABLE IF NOT EXISTS meta (k TEXT PRIMARY KEY, v TEXT)")
            self.db.commit()
        if not self.readonly:
            row = self.db.execute("PRAGMA quick_check").fetchone()
            if not row or row[0] != "ok":
                raise sqlite3.DatabaseError("quick_check says: %s" % (row[0] if row else "nothing"))

    def _has(self, table):
        return self.db.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone()[0] == 1

    def load(self, setname):
        if self.db is None or not self._has("files"):
            return {}
        return dict((r[0], (r[1], r[2], r[3])) for r in
                    self.db.execute("SELECT rel,size,mtime_ns,ctime_ns FROM files WHERE setname=?", (setname,)))

    def put_many(self, setname, rows, when):
        if self.db is None or self.readonly or not rows:
            return
        self.db.executemany("INSERT OR REPLACE INTO files (setname,rel,size,mtime_ns,ctime_ns,copied_at) VALUES (?,?,?,?,?,?)",
                            [(setname, rel, s[0], s[1], s[2], when) for rel, s in rows])
        self.db.commit()

    def drop(self, setname, rels):
        """Forget earlier proofs (a sample found the destination copy wrong): committed at once, so the file can
        never again rest on that proof, whatever happens to the rest of this run."""
        if self.db is None or self.readonly or not rels:
            return
        self.db.executemany("DELETE FROM files WHERE setname=? AND rel=?", [(setname, r) for r in rels])
        self.db.commit()

    def baseline(self):
        """The per-set file counts of the last good run: a SECOND copy of what the state file holds, so a damaged
        state file does not take the fall rule's baseline with it (second check, finding 4)."""
        if self.db is None or not self._has("meta"):
            return {}
        row = self.db.execute("SELECT v FROM meta WHERE k='set_counts'").fetchone()
        try:
            d = json.loads(row[0]) if row else {}
            return d if isinstance(d, dict) else {}
        except ValueError:
            return {}

    def set_baseline(self, set_counts):
        if self.db is None or self.readonly:
            return
        self.db.execute("INSERT OR REPLACE INTO meta (k,v) VALUES ('set_counts',?)", (json.dumps(set_counts, sort_keys=True),))
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
    if "openrsync" in r.stdout or "version 2." in first or "version 3." not in first:
        return "%s is not rsync 3 (%s): --backup-dir behaviour is not trusted on it" % (binary, first.strip())
    return None


def cpu_seconds(pgid):
    r = subprocess.run(["/bin/ps", "-axo", "pgid=,time="], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    total = 0.0
    for ln in r.stdout.splitlines():
        parts = ln.split()
        if len(parts) != 2 or parts[0] != str(pgid):
            continue
        bits = parts[1].replace(",", ".").split(":")
        try:
            sec = float(bits[-1])
            if len(bits) >= 2:
                sec += int(bits[-2]) * 60
            if len(bits) >= 3:
                sec += int(bits[-3].split("-")[-1]) * 3600
            total += sec
        except ValueError:
            pass
    return total


_child = {"p": None}


def check_argv(argv):
    for a in argv[1:]:
        for bad in FORBIDDEN_RSYNC:
            if a == bad or a.startswith(bad + "=") or a.startswith("--delete") or a.startswith("--del"):
                raise Refused("REFUSED — forbidden engine flag %s (this tool never passes a deletion flag)" % a)


def run_rsync(ctx, argv, log_path, err_path, deadline, stall_seconds, record_group=False):
    """Returns (status, rc): status in ok|killed-cap|stalled. The engine gets its own session and process group."""
    check_argv(argv)
    with open(log_path, "wb") as lo, open(err_path, "wb") as le:
        p = subprocess.Popen(argv, stdout=lo, stderr=le, start_new_session=True)
    _child["p"] = p
    if record_group and ctx is not None and os.path.isdir(ctx.lock_dir):
        write_owner(ctx, "run", engine_pgid=p.pid)
    started = time.time()
    stall_checked = False
    try:
        while True:
            try:
                return ("ok", p.wait(timeout=2))
            except subprocess.TimeoutExpired:
                pass
            if not stall_checked and time.time() - started >= stall_seconds:
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
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(p.pid, sig)        # the whole group: rsync forks a receiver
        except OSError:
            pass
        try:
            p.wait(timeout=5)
            return
        except subprocess.TimeoutExpired:
            continue


def parse_engine_log(log_path):
    res = {"new": 0, "updated": 0, "dirs": 0, "deleting": [], "paths": [], "transferred_bytes": None}
    with open(log_path, "rb") as fh:
        text = fh.read().decode("utf-8", "replace").replace("\r", "\n")
    for ln in text.split("\n"):
        if not ln:
            continue
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
def preflight(ctx, mode, out_of_sequence, lines):
    c = ctx.conf
    if not source_is_local_volume(ctx):
        raise Refused("REFUSED — the source volume %s is not mounted as a local drive (the mount table has no "
                      "local entry for it); nothing run" % c["source_volume"])
    if not under(ctx.tree, c["source_volume"]):
        raise Refused("REFUSED — this seat's tree %s is not on the configured source drive %s: a seat backs up "
                      "only its own drive" % (ctx.tree, c["source_volume"]))
    tree_dev = os.stat(ctx.tree).st_dev
    for s in c["sets"]:
        if os.path.islink(s["src"]):
            raise Refused("REFUSED — source %s is a symlink (to %s); name the real folder; nothing run" % (s["src"], s["real"]))
        if not os.path.isdir(s["src"]):
            raise Refused("REFUSED — source %s is absent or not a folder; nothing run" % s["src"])
        if s["real"] != os.path.normpath(s["src"]):
            raise Refused("REFUSED — source %s reaches %s through a symlinked parent; name the real folder; nothing run" % (s["src"], s["real"]))
        if not under(s["src"], c["source_volume"]) or os.stat(s["src"]).st_dev != tree_dev:
            raise Refused("REFUSED — source %s is not on the seat's own drive (%s); nothing run" % (s["src"], c["source_volume"]))
    if not nas_is_smb_mounted(ctx):
        raise Refused("REFUSED — %s is not mounted as a network share (the mount table shows no smbfs entry): an "
                      "unmounted path would fill the local disk under /Volumes; nothing run" % c["nas_root"])
    for client in sorted(set(s["client"] for s in c["sets"])):
        chk = real_name_check(c["nas_root"], client)
        if chk == "absent":
            raise Refused("REFUSED — the NAS has no top-level folder '%s'; it is never created by this tool; nothing run" % client)
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
                          % (now_local_str(ctx.now), wstr(o), wstr(cl)))


def plan_set(ctx, s, index_rows, last_count, accept_shrink, do_hash=True, on_proven=None, deadline=None):
    """Lists the source and the destination and decides what must be copied. READS ONLY (a real run passes
    on_proven, which saves each file found identical by sha256 into the index as it goes)."""
    rules = Rules(ctx, s)
    rs = os.stat(s["src"])
    src = walk(s["src"], rules)
    c = ctx.conf
    plan = {"set": s, "src": src, "problems": [], "copy": [], "copy_dirs": [], "reason": {}, "proven_unsent": [],
            "type_changes": [], "collisions": [], "collision_skipped": {}, "nas_listed": [], "notes": [],
            "root_id": (rs.st_dev, rs.st_ino), "cap_hit": False}
    n_src = len(src["files"])
    if n_src > c["max_files"]:
        tops = {}
        for rel, v in src["files"].items():
            t = tops.setdefault("/".join(rel.split("/")[:2]), [0, 0])
            t[0] += 1
            t[1] += v[0]
        worst = sorted(tops.items(), key=lambda kv: -kv[1][0])[:5]
        raise Refused("REFUSED — set %s has %d files in scope, above max_files=%d: too many to copy and count in one "
                      "night. Largest by file count: %s. Narrow the scope or raise max_files on the coordinator's word; "
                      "nothing copied for this set"
                      % (s["dest"], n_src, c["max_files"], "; ".join("%s (%d files, %s)" % (k, v[0], fmt_bytes(v[1])) for k, v in worst)))
    if src["errors"]:
        plan["problems"].append("source could not be fully read: %d error(s), first: %s" % (len(src["errors"]), src["errors"][0]))
    croot = ctx.client_root(s["client"])
    dest_dir = os.path.join(croot, "current", *s["dest"].split("/"))
    _, dest_exists, deepest = ensure_dest_chain(os.path.join(c["nas_root"], s["client"]),
                                                [ctx.info["cap"], BACKUP_FOLDER, "current"] + s["dest"].split("/"), create=False)
    plan.update({"dest_dir": dest_dir, "dest_exists": dest_exists, "croot": croot})
    if dest_exists:
        dst = walk(dest_dir)
        plan["nas_listed"].append("%s: %d files, %d folders (walked whole)" % (dest_dir, len(dst["files"]), len(dst["dirs"])))
    else:
        dst = {"files": {}, "dirs": set(), "links": {}, "specials": [], "errors": [], "excluded": {}, "hardlinks": [],
               "secret_names": [], "dir_ids": {}}
        try:
            plan["nas_listed"].append("%s: %d entries at its top level; the destination below it does not exist yet"
                                      % (deepest, len(os.listdir(deepest))))
        except OSError as e:
            plan["problems"].append("could not list %s on the NAS: %s" % (deepest, e))
    plan["dst"] = dst
    if dst["errors"]:
        plan["problems"].append("destination could not be fully read: %d error(s), first: %s" % (len(dst["errors"]), dst["errors"][0]))
    # Names differing only in case (the drive is case-sensitive, the NAS is not): neither is copied, both are named.
    groups = {}
    for rel in list(src["files"]) + list(src["dirs"]):
        groups.setdefault(ckey(rel), []).append(rel)
    clash = sorted(r for v in groups.values() if len(v) > 1 for r in v)
    plan["collisions"] = clash
    if clash:
        clashset = set(clash)
        clash_dirs = tuple(r + "/" for r in clash if r in src["dirs"])
        for rel in list(src["files"]):
            if rel in clashset or rel.startswith(clash_dirs):
                plan["collision_skipped"][rel] = src["files"].pop(rel)
        for rel in list(src["dirs"]):
            if rel in clashset or rel.startswith(clash_dirs):
                src["dirs"].discard(rel)
    # THE PLAN IS WHAT IS LEFT NOW (after the names that differ only in case were taken out): the rules about an
    # empty or collapsed plan are applied to THAT number, the same number the good run records as its baseline.
    n_src = len(src["files"])
    # AN EMPTY PLAN IS NEVER GOOD (the one rule; both checks' finding 4): zero files fails the night, with or
    # without folders, on a first run too. The ONE exception is a set the conf names in an allow_empty= line.
    if n_src == 0 and s["dest"] not in c["allow_empty"]:
        plan["problems"].append("EMPTY SCOPE: 0 files in the plan for this set (%d folders; last good run: %s). A backup "
                                "of nothing is never recorded as good; if this set is really empty, the conf must say "
                                "allow_empty=%s" % (len(src["dirs"]), last_count if last_count is not None else "no record", s["dest"]))
    elif n_src == 0:
        plan["notes"].append("this set holds 0 files and the conf allows it to be empty (allow_empty=%s)" % s["dest"])
    elif last_count is None:
        plan["notes"].append("NO BASELINE: there is no earlier good run to compare this set's %d files with, so a wrong "
                             "exclusion could not be noticed by the fall rule tonight" % n_src)
    elif last_count and n_src < last_count * (1.0 - c["max_drop_fraction"]) and not accept_shrink:
        plan["problems"].append("SCOPE FELL SHARPLY: %d files in scope now, %d at the last good run (more than a %d%% fall). "
                                "If the source really shrank, run once with --accept-shrink \"<card id>\""
                                % (n_src, last_count, int(c["max_drop_fraction"] * 100)))
    dfiles = dict((ckey(r), (r, v)) for r, v in dst["files"].items())
    ddirs = dict((ckey(r), r) for r in dst["dirs"])
    # TYPE CHANGES (finding 7): a folder that became a file, or a file that became a folder. The old destination
    # entry is MOVED into versions/<stamp>/ by the run, then the new one is copied. Planned here, done in the run.
    for rel in sorted(src["files"]):
        k = ckey(rel)
        if k in ddirs:
            plan["type_changes"].append((rel, ddirs[k], "folder at the destination, file at the source"))
    for rel in sorted(src["dirs"]):
        k = ckey(rel)
        if k in dfiles:
            plan["type_changes"].append((rel, dfiles[k][0], "file at the destination, folder at the source"))
    for rel, drel, what in plan["type_changes"]:
        k = ckey(drel)
        if k in ddirs:
            pre = k + "/"
            for kk in [x for x in ddirs if x == k or x.startswith(pre)]:
                del ddirs[kk]
            for kk in [x for x in dfiles if x.startswith(pre)]:
                del dfiles[kk]
        else:
            del dfiles[k]
    plan["dfiles"], plan["ddirs"] = dfiles, ddirs
    for rel in sorted(src["dirs"]):
        if ckey(rel) not in ddirs:
            plan["copy_dirs"].append(rel)
    to_hash = []
    for rel, sv in src["files"].items():
        d = dfiles.get(ckey(rel))
        if d is None:
            plan["copy"].append(rel)
            plan["reason"][rel] = "new"
        elif d[1][0] != sv[0]:
            plan["copy"].append(rel)
            plan["reason"][rel] = "size"
        else:
            ix = index_rows.get(rel)
            if ix is not None and tuple(ix) == tuple(sv):
                plan["proven_unsent"].append(rel)          # proven earlier: exact stat in the index
            else:
                to_hash.append((rel, d[0]))
    plan["to_hash_count"] = len(to_hash)
    plan["hash_bytes"] = sum(src["files"][r][0] for r, _ in to_hash)
    plan["hash_equal"] = []
    plan["unverified_same_size"] = []
    if do_hash:
        for i, (rel, drel) in enumerate(to_hash):
            if deadline is not None and time.time() >= deadline:
                # The cap is honoured HERE, between files, not left to the watchdog (second check, finding 8).
                plan["cap_hit"] = True
                plan["problems"].append("stopped by the run-time cap while comparing files already at the destination: "
                                        "%d of %d compared; what was found identical is saved, so the next run goes on "
                                        "from there" % (i, len(to_hash)))
                break
            try:
                same = sha256_of(os.path.join(s["src"], rel)) == sha256_of(os.path.join(dest_dir, drel))
            except OSError:
                same = False
            if same:
                plan["hash_equal"].append(rel)
                if on_proven is not None:
                    on_proven(rel, src["files"][rel])
            else:
                plan["copy"].append(rel)
                plan["reason"][rel] = "content"
    else:
        plan["unverified_same_size"] = [r for r, _ in to_hash]
    plan["copy"].sort()
    return plan


DELETE_RECHECK_SECONDS = 0.2
_TEST = {"hash_delay": 0.0}


def prove_arrival(src_path, dst_path):
    """THE ARRIVAL PROOF. Returns (verdict, stat, why):
       proven      sha256(source) == sha256(destination), the source unchanged across the read
       unstable    the source changed while it was being read (send it again)
       unreadable  the source could not be read, for ANY reason (permission, I/O error, a privacy refusal, no such
                   file, no longer a regular file). This is NOT 'gone': the caller treats it as NOT DELIVERED
                   unless source_deleted() then proves the file was deleted.
       hardlinked  ROUND 4 (third check, finding 3): the source now has more than one hard link. It had one when
                   it was planned (the walk leaves out every file with more), so another name was given to it
                   since, and that other name may sit inside a secrets folder. NEVER proven, whatever the
                   destination holds.
       differs     the destination is absent, unreadable, or holds other content."""
    try:
        s1 = stat3(src_path)
        ls = os.lstat(src_path)
        if not stat.S_ISREG(ls.st_mode):
            return ("unreadable", None, "the source is no longer a regular file")
        if ls.st_nlink > 1:
            return ("hardlinked", None, "the source has %d hard links now and had one when it was planned" % ls.st_nlink)
        if _TEST["hash_delay"]:
            time.sleep(_TEST["hash_delay"])
        hs = sha256_of(src_path)
        s2 = stat3(src_path)
    except OSError as e:
        return ("unreadable", None, "the source could not be read (%s)" % (e.strerror or e))
    if s1 != s2:
        return ("unstable", None, "the source changed while it was being read")
    try:
        if os.stat(dst_path).st_size != s1[0]:
            return ("differs", s1, "the destination copy has another size")
        hd = sha256_of(dst_path)
    except OSError as e:
        return ("differs", s1, "the destination copy is absent or could not be read (%s)" % (e.strerror or e))
    return ("proven", s1, "") if hs == hd else ("differs", s1, "the destination copy holds other content")


def hard_linked_now(path):
    """ROUND 4 (third check, finding 3): True when `path` is a regular file with more than one hard link NOW.
    Asked immediately before a chunk is handed to the engine. A path that cannot be looked at is not judged here:
    the arrival proof judges it."""
    try:
        st = os.lstat(path)
    except OSError:
        return False
    return stat.S_ISREG(st.st_mode) and st.st_nlink > 1


def source_deleted(root, root_id, rel, parent_id=None):
    """True ONLY when the planned file is provably DELETED from the source: the set's root is still the very folder
    that was listed, the file's PARENT folder can be listed, and the name is absent from that listing; checked
    twice. A folder that cannot be listed, a parent that is itself gone, a root that was moved or unmounted: False
    (the file is then NOT DELIVERED). 'Could not read it' is never taken to mean 'it was deleted'.
    ROUND 4 (third check, finding 6), two more conditions, each of which a file that STILL EXISTS failed to meet:
      - the planned path must not resolve (os.path.lexists): on a volume that folds case, a file renamed to another
        case is absent from the listing BY NAME while its planned path still opens it;
      - when the caller knows which folder the parent WAS when it was listed (parent_id: device and inode), the
        parent must still be that folder: a folder REPLACED by a new one of the same name lists without the file,
        and the file lives on wherever the old folder went."""
    path = os.path.join(root, rel)
    parent = os.path.dirname(path)
    name = os.path.basename(rel)
    for attempt in (1, 2):
        try:
            rs = os.stat(root)
            if (rs.st_dev, rs.st_ino) != tuple(root_id) or not stat.S_ISDIR(rs.st_mode):
                return False
            if parent_id is not None:
                ps = os.stat(parent)
                if (ps.st_dev, ps.st_ino) != tuple(parent_id):
                    return False
            names = os.listdir(parent)
        except OSError:
            return False
        if name in names:
            return False
        if os.path.lexists(path):
            return False
        if attempt == 1:
            time.sleep(DELETE_RECHECK_SECONDS)
    return True


def parent_id_of(plan, rel):
    """The (device, inode) of the folder that held `rel` when the set was listed. A parent the walk has no record
    of gets an id nothing can equal, so the deletion proof fails closed."""
    prel = os.path.dirname(rel)
    return plan["root_id"] if prel == "" else plan["src"]["dir_ids"].get(prel, (-1, -1))


def left_out_line(rel, shape):
    """One line of the left-out list: <relative path> TAB <shape>. A backslash, tab, newline or carriage return
    inside a name is written as \\\\, \\t, \\n, \\r, so one entry is always exactly one line."""
    return "%s\t%s\n" % (rel.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r"), shape)


def write_left_out_list(ctx, stamp, mode, safe, secret_names):
    """ROUND 4 (third check, finding 4; ANSWER-5's condition for keeping the wide name rule). What the secret-shape
    rule left out of this set, BY NAME: one line per excluded entry (a folder is one entry; nothing under it was
    looked at), relative path TAB shape, sorted. Written in the lane's manifests/ ON THE DRIVE, beside the symlink
    list, by a dry run as well. NEVER written to the share: these are the names of real secret files, and whoever
    can read the share could read them. The file's own name is excluded from every backup (EXCLUDES)."""
    lp = os.path.join(ctx.manifest_dir, "%s_%s_%s%s" % (stamp, mode, safe, LEFT_OUT_SUFFIX))
    with open(lp, "w", encoding="utf-8", errors="surrogateescape") as fh:
        for rel, shape in sorted(secret_names):
            fh.write(left_out_line(rel, shape))
    return lp


def deleted_allowed(conf, planned):
    """How many planned files may be deleted from the source during a run before the night fails: the larger of
    max_deleted_files (default 5) and max_deleted_fraction of the plan (default 0.1%)."""
    return max(conf["max_deleted_files"], int(planned * conf["max_deleted_fraction"]))


class Saver(object):
    """Proven files are committed to the index AS THE PROOF GOES, at least every PROOF_BATCH files, so an
    interrupted first copy does not re-read what it had already proven (second check, finding 8)."""

    def __init__(self, index, setname):
        self.index, self.setname, self.rows, self.saved = index, setname, [], 0

    def add(self, rel, st3):
        self.rows.append((rel, st3))
        if len(self.rows) >= PROOF_BATCH:
            self.flush()

    def flush(self):
        if self.rows:
            self.index.put_many(self.setname, self.rows, time.time())
            self.saved += len(self.rows)
            self.rows = []


def make_chunks(rels, sizes, chunk_files):
    chunks, cur, nbytes = [], [], 0
    for rel in rels:
        cur.append(rel)
        nbytes += sizes[rel][0]
        if len(cur) >= chunk_files or nbytes >= CHUNK_BYTES:
            chunks.append(cur)
            cur, nbytes = [], 0
    if cur:
        chunks.append(cur)
    return chunks


def watchdog_margin(ctx):
    """900 s after the cap. TEST MODE ONLY: NB_TEST_WATCHDOG_MARGIN shortens it so the watchdog can be exercised."""
    if ctx.troot and os.environ.get("NB_TEST_WATCHDOG_MARGIN"):
        return int(os.environ["NB_TEST_WATCHDOG_MARGIN"])
    return WATCHDOG_MARGIN


def folder_table(plan, proven, deleted=()):
    t = {}
    blank = {"src_files": 0, "src_bytes": 0, "dst_files": 0, "dst_bytes": 0, "dst_only_files": 0, "dst_only_bytes": 0}
    src = plan["src"]["files"]
    for rel, sv in src.items():
        if rel in deleted:
            continue          # provably deleted at the source during the run: on neither side of tonight's count
        row = t.setdefault(top_of(rel), dict(blank))
        row["src_files"] += 1
        row["src_bytes"] += sv[0]
        if rel in proven:
            row["dst_files"] += 1
            row["dst_bytes"] += sv[0]
    skeys = set(ckey(r) for r in src)
    for k, (drel, dv) in plan["dfiles"].items():
        if k not in skeys:
            row = t.setdefault(top_of(drel), dict(blank))
            row["dst_only_files"] += 1
            row["dst_only_bytes"] += dv[0]
    return t


def fmt_bytes(n):
    n = float(n)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if n < 1024 or unit == "TiB":
            return ("%d %s" % (n, unit)) if unit == "B" else ("%.2f %s" % (n, unit))
        n /= 1024.0


def sum_by_cat(excluded):
    d = {}
    for (cat, _), v in excluded.items():
        d[cat] = d.get(cat, 0) + v
    return d


def cmd_backup(ctx, mode, scheduled=False, out_of_sequence=None, max_seconds=None, no_hash=False, accept_shrink=None):
    stamp = "%s_%d" % (time.strftime("%Y-%m-%d_%H%M%S", time.localtime(ctx.now)), os.getpid())
    lines = []

    def say(msg):
        lines.append(msg)
        out(msg)

    ctx.readonly = (mode != "run")
    if ctx.found_by == "unknown caller":
        ctx.found_by = "a real run (nas_backup.sh --run)" if mode == "run" else "a dry run"
    ctx.mkdirs()
    run_log = os.path.join(ctx.log_dir, "%s_%s.log" % (stamp, mode))
    say("=== nas-backup seat=%s mode=%s %s ===" % (ctx.seat, mode.upper(), now_local_str(time.time())))
    if mode == "dry":
        say("DRY RUN: reads only. Nothing is written to the NAS, the state file or the index. The engine is never "
            "handed a NAS path in a dry run: the destination is LISTED by this tool.")
    try:
        # ROUND 4 (third check, finding 10): THE HOLD IS TESTED FIRST, before the conf is read. A held --run that
        # would also be refused for another reason (an unconfirmed conf) was recorded as `refused` and started the
        # three-day clock; lifting the hold days later then raised OVERDUE at the first check. Under the hold
        # every --run is `held`, whatever else is wrong, and never starts the clock.
        if mode == "run" and os.path.exists(ctx.hold_file):
            raise Refused("REFUSED — %s exists: real runs are HELD (arming is the coordinator's word on Kam's "
                          "instruction); --dry is still allowed; nothing run" % ctx.hold_file, RC_HELD)
        ctx.load_conf()
        st0 = ctx.read_state()
        if ctx.state_note:
            say(ctx.state_note)
        for label, val in (("--out-of-sequence", out_of_sequence), ("--accept-shrink", accept_shrink)):
            if val is not None and len(val.strip()) < 6:
                raise Refused("REFUSED — %s needs the id of the card Kam ruled (it is recorded in the manifest)" % label)
        preflight(ctx, mode, out_of_sequence, lines)
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
                # A refusal under the HOLD is recorded as `held`: it is not an attempt and never starts the clock.
                ctx.note_attempt("held" if e.rc == RC_HELD else "refused", str(e))
                if ctx.state_note and ctx.state_note not in lines:
                    say(ctx.state_note)          # a damaged state file met while recording a held run is still said
            except Exception as ex:
                err("nas-backup: could not record the refusal in the state file: %s" % ex)
        with open(run_log, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        return e.rc
    # FROM HERE THE LOCK IS HELD (a real run). Whatever happens below, it is released: a damaged index, a full
    # disk, a bug. A lock left behind by a crash stopped every later night (second check, finding 7).
    try:
        return backup_body(ctx, mode, stamp, lines, say, st0, run_log, scheduled, out_of_sequence, max_seconds,
                           no_hash, accept_shrink)
    except Exception as e:
        msg = "the run stopped on an unexpected error: %s: %s" % (type(e).__name__, str(e)[:300])
        say("FAILED: %s" % msg)
        if mode == "run":
            try:
                ctx.note_attempt("failed", msg, {"stamp": stamp})
            except Exception as ex:
                err("nas-backup: could not record the failure in the state file: %s" % ex)
        try:
            with open(run_log, "w", encoding="utf-8", errors="surrogateescape") as fh:
                fh.write("\n".join(lines) + "\n")
        except OSError as ex:
            err("nas-backup: could not write the run log: %s" % ex)
        return RC_ENGINE
    finally:
        signal.alarm(0)
        if mode == "run":
            lock_release(ctx)


def backup_body(ctx, mode, stamp, lines, say, st0, run_log, scheduled, out_of_sequence, max_seconds, no_hash, accept_shrink):
    c = ctx.conf
    tokens = ctx.load_tokens()
    result = {"rc": RC_VERIFY}
    manifest = {"schema": SCHEMA, "seat": ctx.seat, "mode": mode, "stamp": stamp, "started": time.time(),
                "started_local": now_local_str(time.time()), "host": os.uname().nodename,
                "trigger": ("out-of-sequence: " + out_of_sequence) if out_of_sequence else ("scheduled" if scheduled else "manual-in-window"),
                "accept_shrink": accept_shrink, "sets": [], "copy_only": True}
    started = time.time()
    cap = max_seconds if max_seconds is not None else c["max_seconds"]
    deadline = started + cap
    margin = watchdog_margin(ctx)
    interrupted = {"sig": None}

    def on_signal(signum, frame):
        interrupted["sig"] = signum
        kill_child()
        raise KeyboardInterrupt()

    def on_alarm(signum, frame):
        kill_child()
        raise Refused("WATCHDOG: the run was still going %d s after its %d s cap (a blocked read or write on the NAS, "
                      "or a macOS privacy prompt waiting on this Mac's screen); stopped" % (margin, cap), RC_CAP)

    if mode == "run":
        # SIGHUP too (second check, finding 11): closing the terminal of a hand-run first copy killed the tool,
        # left the engine copying, the lock in place and the state saying `running`.
        for sg in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
            signal.signal(sg, on_signal)
        signal.signal(signal.SIGALRM, on_alarm)
        signal.alarm(int(cap) + margin)
        if ctx.troot and os.environ.get("NB_TEST_HASH_DELAY"):
            _TEST["hash_delay"] = float(os.environ["NB_TEST_HASH_DELAY"])
        ctx.note_attempt("running", "started %s" % stamp, {"stamp": stamp})
    problems = []
    undelivered_all = []
    deleted_all = []
    totals = {"src_files": 0, "src_bytes": 0, "copy_files": 0, "copy_bytes": 0, "new": 0, "changed": 0,
              "dst_files": 0, "dst_bytes": 0, "dst_only_files": 0, "versioned": 0, "deleted": 0, "resent": 0,
              "symlinks": 0, "excluded_entries": 0, "case_collision_files": 0, "hard_link_files": 0,
              "type_changes": 0, "undelivered": 0, "proven_by_sha256": 0, "repaired": 0, "sampled": 0,
              "hard_linked_after_plan": 0}
    hardlink_all = []          # ROUND 4: (set/path, SENT or NOT SENT, where) for every file that gained a hard link after the plan
    secret_counts, token_counts, set_counts = {}, dict((t[0], 0) for t in tokens), {}
    client_roots = {}
    index = None
    try:
        index = Index(ctx, readonly=(mode != "run"))
        if index.note:
            say(index.note)
        # THE BASELINE of the fall rule: the last good run's per-set counts, from the state file, and from the
        # index's own copy for any set the state does not know (a damaged state file must not take it away).
        last_counts = dict(index.baseline())
        last_counts.update(((st0.get("last_good") or {}).get("set_counts")) or {})
        for s in c["sets"]:
            # THE MOUNT IS CHECKED BEFORE EVERY SET, not once (second check, finding 12).
            if not nas_is_smb_mounted(ctx):
                raise Refused("REFUSED — %s is no longer mounted as a network share (it was when this run started); "
                              "stopped before set %s" % (c["nas_root"], s["dest"]))
            say("--- set %s/%s  <-  %s" % (s["client"], s["dest"], s["src"]))
            croot = ctx.client_root(s["client"])
            if mode == "run":
                ensure_dest_chain(os.path.join(c["nas_root"], s["client"]), [ctx.info["cap"], BACKUP_FOLDER], create=True)
            # ROUND 4 (third check, finding 2): BEFORE ANYTHING IS WRITTEN FOR THIS SET, every folder it would write
            # into must resolve inside this seat's own nightly-backup folder. A dry run is held to it as well.
            esc = dest_escape(ctx, s["client"], s["dest"])
            if esc:
                raise Refused("REFUSED — %s; nothing written for set %s" % (esc, s["dest"]))
            if mode == "run":
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
                                     "manifests/ one manifest per run\n"
                                     "runs/      RUN_<stamp>_STARTED.txt without a matching _COMPLETE.txt = an INCOMPLETE copy\n"
                                     "Nothing here is ever removed by the tool. Clean-up is Kam's word only.\n" % ctx.info["cap"])
                    with open(os.path.join(croot, "runs", "RUN_%s_STARTED.txt" % stamp), "w", encoding="utf-8") as fh:
                        fh.write("started %s by seat %s (pid %d). Without RUN_%s_COMPLETE.txt beside this file the copy did "
                                 "NOT finish: do not trust current/ as complete.\n" % (now_local_str(time.time()), ctx.seat, os.getpid(), stamp))
            index_rows = index.load(s["dest"])
            saver = Saver(index, s["dest"])
            t0 = time.time()
            try:
                plan = plan_set(ctx, s, index_rows, last_counts.get(s["dest"]), accept_shrink,
                                do_hash=not (mode == "dry" and no_hash),
                                on_proven=(saver.add if mode == "run" else None),
                                deadline=(deadline if mode == "run" else None))
            finally:
                saver.flush()          # whatever was found identical so far is kept, also when the plan is interrupted
            src = plan["src"]
            dest_dir = plan["dest_dir"]
            # ROUND 4 (finding 4): what the secret-shape rule left out of this set, BY NAME, on the drive only.
            # Written as soon as the set is listed, so an interrupted run has it too.
            left_out_file = write_left_out_list(ctx, stamp, mode, s["dest"].replace("/", "__"), src["secret_names"])
            n_src = len(src["files"])
            src_bytes = sum(v[0] for v in src["files"].values())
            set_counts[s["dest"]] = n_src
            copy_bytes = sum(src["files"][r][0] for r in plan["copy"])
            n_new = sum(1 for r in plan["copy"] if plan["reason"][r] == "new")
            n_chg = len(plan["copy"]) - n_new
            exc_entries = sum(src["excluded"].values())
            for (cat, pat), n in src["excluded"].items():
                if cat == "secret":
                    secret_counts[pat] = secret_counts.get(pat, 0) + n
            for label, rx in tokens:
                token_counts[label] += sum(1 for rel in src["files"] if rx.search(rel.lower()))
            say("    source in scope: %d files, %s, %d folders, %d symlinks (recorded, not copied), %d special files (skipped)"
                % (n_src, fmt_bytes(src_bytes), len(src["dirs"]), len(src["links"]), len(src["specials"])))
            say("    excluded at the source: %d entries (%s)" % (exc_entries, ", ".join(
                "%s=%d" % (cat, n) for cat, n in sorted(sum_by_cat(src["excluded"]).items())) or "none"))
            say("    left out by secret shape: %d entries, listed BY NAME on this drive only, never on the share: %s"
                % (len(src["secret_names"]), left_out_file))
            for ln in plan["nas_listed"]:
                say("    listed on the NAS (read-only): %s" % ln)
            say("    to copy: %d files, %s (%d new, %d changed -> previous copy kept in versions/%s/); %d new folders"
                % (len(plan["copy"]), fmt_bytes(copy_bytes), n_new, n_chg, stamp, len(plan["copy_dirs"])))
            if plan["to_hash_count"]:
                if plan["unverified_same_size"]:
                    say("    same size, not yet proven: %d files (%s) NOT compared by content in this dry run (--no-hash)"
                        % (plan["to_hash_count"], fmt_bytes(plan["hash_bytes"])))
                else:
                    say("    compared by sha256 (same size, source changed or not yet proven): %d files, %d identical"
                        % (plan["to_hash_count"], len(plan["hash_equal"])))
            if src["hardlinks"]:
                say("    SKIPPED: %d file(s) with more than one hard link (another name for the same file may sit in a "
                    "secrets folder); first: %s. All are named in the manifest." % (len(src["hardlinks"]), src["hardlinks"][0]))
            if plan["collisions"]:
                say("    NOT BACKED UP: %d file(s), because %d name(s) differ only in case from a sibling and the NAS cannot hold "
                    "both (first: %s | %s). They are listed in the manifest."
                    % (len(plan["collision_skipped"]), len(plan["collisions"]), plan["collisions"][0], plan["collisions"][1]))
            for rel, drel, what in plan["type_changes"]:
                say("    TYPE CHANGE: %s (%s): the old destination entry %s into versions/%s/, then the new one is copied"
                    % (rel, what, "is MOVED" if mode == "run" else "WOULD BE MOVED", stamp))
            say("    planning took %.1f s" % (time.time() - t0))
            for note in plan["notes"]:
                say("    note: %s" % note)
            for p in plan["problems"]:
                say("    PROBLEM: %s" % p)
                problems.append("%s: %s" % (s["dest"], p))
            mset = {"client": s["client"], "dest": s["dest"], "source": s["src"], "destination": dest_dir,
                    "src_files": n_src, "src_bytes": src_bytes, "src_dirs": len(src["dirs"]),
                    "symlinks": len(src["links"]), "specials": len(src["specials"]),
                    "excluded": [{"category": k[0], "pattern": k[1], "entries": v} for k, v in sorted(src["excluded"].items())],
                    "hard_link_files_skipped": src["hardlinks"][:500],
                    "left_out_by_secret_shape_entries": len(src["secret_names"]),
                    "left_out_by_secret_shape_list_on_the_drive": left_out_file,
                    "to_copy_files": len(plan["copy"]), "to_copy_bytes": copy_bytes, "new": n_new, "changed": n_chg,
                    "case_collision_names": plan["collisions"][:200],
                    "case_collision_files_not_backed_up": len(plan["collision_skipped"]),
                    "type_changes": [list(x) for x in plan["type_changes"]],
                    "nas_listed": plan["nas_listed"], "notes": list(plan["notes"]), "problems": list(plan["problems"]),
                    "engine_passes": []}
            for k, v in (("src_files", n_src), ("src_bytes", src_bytes), ("copy_files", len(plan["copy"])), ("copy_bytes", copy_bytes),
                         ("new", n_new), ("changed", n_chg), ("symlinks", len(src["links"])), ("excluded_entries", exc_entries),
                         ("case_collision_files", len(plan["collision_skipped"])), ("hard_link_files", len(src["hardlinks"])),
                         ("type_changes", len(plan["type_changes"]))):
                totals[k] += v
            proven = set(plan["proven_unsent"]) | set(plan["hash_equal"])
            if mode == "dry":
                proven |= set(plan["unverified_same_size"])
            deleted = []
            safe = s["dest"].replace("/", "__")
            scope_broken = any(p.startswith(("EMPTY SCOPE", "SCOPE FELL")) for p in plan["problems"])

            if mode == "dry":
                # The engine validates the list against an EMPTY LOCAL folder. It never sees a NAS path here.
                if plan["copy"] or plan["copy_dirs"]:
                    list_path = os.path.join(ctx.log_dir, "%s_dry_%s.files0" % (stamp, safe))
                    with open(list_path, "wb") as fh:
                        for rel in plan["copy_dirs"] + plan["copy"]:
                            fh.write(rel.encode("utf-8", "surrogateescape") + b"\0")
                    empty = os.path.join(ctx.state_dir, "empty_for_dry_run")
                    os.makedirs(empty, exist_ok=True)
                    eng_log = os.path.join(ctx.log_dir, "%s_dry_%s.rsync.log" % (stamp, safe))
                    argv = [c["rsync"], "-n", "-t", "-O", "-I", "--from0", "--files-from=" + list_path, "--out-format=%i %n%L",
                            "--stats", "--no-h", s["src"].rstrip("/") + "/", empty + "/"]
                    status, rc = run_rsync(ctx, argv, eng_log, eng_log[:-4] + ".err", deadline, c["stall_seconds"])
                    pl = parse_engine_log(eng_log)
                    say("    engine check of the list (against an empty LOCAL folder, -n): %s rc=%s, %d files listed; deleting lines: %d"
                        % (status, rc, pl["new"] + pl["updated"], len(pl["deleting"])))
                    if pl["deleting"]:
                        problems.append("%s: the engine's log holds a DELETING line" % s["dest"])
                    if status != "ok" or (rc == 0 and pl["new"] + pl["updated"] != len(plan["copy"])):
                        problems.append("%s: the engine's dry list (%d files, %s rc=%s) disagrees with the plan (%d files)"
                                        % (s["dest"], pl["new"] + pl["updated"], status, rc, len(plan["copy"])))
            elif scope_broken:
                say("    NOT COPIED: the scope of this set is broken (above); nothing was sent for it")
            elif plan["cap_hit"]:
                say("    NOT COPIED: the run-time cap was reached while this set was being compared (above)")
                result["rc"] = RC_CAP
            else:
                # THE PLAN. Every one of these files must end PROVEN at the destination, or provably deleted at
                # the source; whatever is neither is NOT DELIVERED and fails the night. This set is the ONLY
                # accounting: nothing below can take a file out of it.
                planned = set(src["files"])
                why = {}                    # rel -> why it is not proven (printed with its name)
                held_back = []              # ROUND 4: gained a second hard link after the plan; kept out of its chunk
                sent_linked = []            # ROUND 4: (rel, destination path, content there now) seen only at proof time
                missing_dirs = []
                stop = None                 # set when the engine was stopped (cap, stall) or the cap passed mid-proof
                try:
                    # 1. THE SAMPLE of files NOT sent tonight (they rest on an earlier proof), taken FIRST. One that
                    #    is no longer proven loses its index row AT ONCE and joins tonight's copy list, so it is
                    #    repaired in this run (the old destination content is kept in versions/), or the night fails
                    #    and every later night compares it by content again: a sample finding never ages out.
                    pool = sorted(plan["proven_unsent"])
                    random.seed(stamp + s["dest"])
                    sample = random.sample(pool, min(c["hash_sample"], len(pool)))
                    repair = []
                    wrong_at_dest = 0
                    for rel in sample:
                        drel = plan["dfiles"][ckey(rel)][0]
                        verdict, _, note = prove_arrival(os.path.join(s["src"], rel), os.path.join(dest_dir, drel))
                        if verdict != "proven":
                            repair.append(rel)
                            why[rel] = "the nightly sample: " + note
                            wrong_at_dest += 1 if verdict == "differs" else 0
                    if repair:
                        index.drop(s["dest"], repair)
                        for rel in repair:
                            proven.discard(rel)
                            plan["reason"][rel] = "repair"
                        say("    SAMPLE: %d of %d files not sent tonight are NO LONGER PROVEN at the destination (first: %s: %s). "
                            "Their earlier proof is withdrawn and they are sent again now; the destination's present "
                            "content goes to versions/%s/" % (len(repair), len(sample), repair[0], why[repair[0]], stamp))
                    totals["sampled"] += len(sample)
                    if wrong_at_dest:
                        # ONE WRONG DESTINATION COPY WITHDRAWS EVERY EARLIER PROOF OF THIS SET. The sample looked at
                        # a few files; the rest rest on proofs of exactly the kind that just turned out false (the
                        # second check's N3d: 30 copies altered, the 10 sampled repaired, the night said GOOD over
                        # 20 it had not looked at). So every other unsent file of the set is read back NOW; what
                        # agrees is proven again, what does not joins the repair. If the cap passes first, the
                        # night fails and the next run goes on with the comparison: nothing is trusted meanwhile.
                        sampled = set(sample)
                        rest = [r for r in pool if r not in sampled]
                        index.drop(s["dest"], rest)
                        for rel in rest:
                            proven.discard(rel)
                        n_again = 0
                        for i, rel in enumerate(rest):
                            if time.time() >= deadline:
                                for r2 in rest[i:]:
                                    why.setdefault(r2, "its earlier proof was withdrawn after the sample found a wrong copy, and the "
                                                       "run-time cap passed before it was read back")
                                problems.append("%s: the run-time cap (%ds) passed during the full read-back that follows a sample "
                                                "finding: %d of %d files read back; the next run goes on" % (s["dest"], cap, i, len(rest)))
                                result["rc"] = RC_CAP
                                stop = "the cap"
                                break
                            drel = plan["dfiles"][ckey(rel)][0]
                            verdict, st3, note = prove_arrival(os.path.join(s["src"], rel), os.path.join(dest_dir, drel))
                            if verdict == "proven":
                                proven.add(rel)
                                saver.add(rel, st3)
                            else:
                                repair.append(rel)
                                why[rel] = "read back after the sample finding: " + note
                                plan["reason"][rel] = "repair"
                                n_again += 1
                        saver.flush()
                        say("    FULL READ-BACK after the sample finding: the earlier proofs of all %d other unsent files of this "
                            "set were withdrawn and each file was compared with its source again: %d more are wrong and are "
                            "sent again now" % (len(rest), n_again))
                    # 2. type changes: MOVE the old destination entry into versions/<stamp>/ (never deleted)
                    for rel, drel, what in plan["type_changes"]:
                        vpath = os.path.join(croot, "versions", stamp, *(s["dest"].split("/") + drel.split("/")))
                        os.makedirs(os.path.dirname(vpath), exist_ok=True)
                        os.rename(os.path.join(dest_dir, drel), vpath)
                    # 3. THE COPY, IN CHUNKS. Each chunk is sent, then every file of it is proven and the proof is
                    #    saved, before the next chunk starts: an interruption loses at most one chunk's proof.
                    todo_all = sorted(set(plan["copy"]) | set(repair))
                    chunks = make_chunks(todo_all, src["files"], c["chunk_files"])
                    if not chunks and plan["copy_dirs"]:
                        chunks = [[]]
                    base = os.path.join(ctx.log_dir, "%s_run_%s" % (stamp, safe))
                    if chunks:
                        with open(base + ".files0", "wb") as fh:          # everything this set sends tonight, once
                            for rel in plan["copy_dirs"] + todo_all:
                                fh.write(rel.encode("utf-8", "surrogateescape") + b"\0")
                    for ci, chunk in enumerate(chunks, 1):
                        if stop:
                            break
                        if not nas_is_smb_mounted(ctx):
                            raise Refused("REFUSED — %s is no longer mounted as a network share; stopped in set %s before "
                                          "chunk %d of %d" % (c["nas_root"], s["dest"], ci, len(chunks)))
                        # ROUND 4 (finding 2): ... and so is the destination, before every chunk: a symlink put into
                        # the chain while the set is being copied gets at most the one chunk that was in flight.
                        esc = dest_escape(ctx, s["client"], s["dest"])
                        if esc:
                            raise Refused("REFUSED — %s; stopped in set %s before chunk %d of %d"
                                          % (esc, s["dest"], ci, len(chunks)))
                        todo = list(chunk)
                        todo_dirs = list(plan["copy_dirs"]) if ci == 1 else []
                        for npass in range(1, MAX_PASSES + 1):
                            # ROUND 4 (third check, finding 3): IMMEDIATELY BEFORE THE CHUNK IS HANDED TO THE ENGINE,
                            # every file of it is looked at again. One that has more than one hard link now (it had
                            # one when planned) is taken out of the chunk: it is not sent, it is never proven, and
                            # the night fails naming it. This narrows the window to the one chunk in flight.
                            linked = set(rel for rel in todo if hard_linked_now(os.path.join(s["src"], rel)))
                            if linked:
                                for rel in sorted(linked):
                                    why[rel] = ("%s: it has more than one hard link now and had one when it was planned; "
                                                "another name for the same file may sit in a secrets folder"
                                                % ("NOT SENT" if npass == 1 else "NOT SENT AGAIN (pass %d of this run sent it while "
                                                   "it was changing, before the second link was seen)" % (npass - 1)))
                                    held_back.append(rel)
                                todo = [rel for rel in todo if rel not in linked]
                            if not todo and not todo_dirs:
                                break
                            tag = "" if npass == 1 else "_pass%d" % npass
                            # the chunk's own three files are overwritten by the next chunk; what the engine said
                            # is appended to ONE log and ONE error file per set (a first copy has thousands of chunks)
                            list_path, eng_log, eng_err = base + ".chunk.files0", base + ".chunk.rsync.log", base + ".chunk.rsync.err"
                            with open(list_path, "wb") as fh:
                                for rel in todo_dirs + todo:
                                    fh.write(rel.encode("utf-8", "surrogateescape") + b"\0")
                            # a separate versions folder per pass: a re-send must never overwrite the previous copy pass 1 kept
                            bdir = os.path.join(croot, "versions", stamp + tag, *s["dest"].split("/"))
                            argv = [c["rsync"], "-t", "-O", "-I", "--from0", "--files-from=" + list_path, "--backup",
                                    "--backup-dir=" + bdir, "--timeout=%d" % c["io_timeout"], "--out-format=%i %n%L", "--stats", "--no-h",
                                    "--temp-dir=" + os.path.join(croot, "_tmp_incoming"), s["src"].rstrip("/") + "/", dest_dir.rstrip("/") + "/"]
                            if ci == 1 and npass == 1:
                                say("    engine: %s" % " ".join(shlex.quote(a) for a in argv))
                            status, rc = run_rsync(ctx, argv, eng_log, eng_err, deadline, c["stall_seconds"], record_group=True)
                            pl = parse_engine_log(eng_log)
                            with open(eng_err, "rb") as fh:
                                etxt = fh.read().decode("utf-8", "replace").strip()
                            for part, whole in ((eng_log, base + ".rsync.log"), (eng_err, base + ".rsync.err")):
                                with open(part, "rb") as a, open(whole, "ab") as b:
                                    b.write(("## chunk %d of %d, pass %d: %s rc=%s\n" % (ci, len(chunks), npass, status, rc)).encode("utf-8"))
                                    b.write(a.read())
                            say("    chunk %d of %d, engine pass %d: %s rc=%s; its log lists %d new + %d replaced files; deleting lines: %d%s"
                                % (ci, len(chunks), npass, status, rc, pl["new"], pl["updated"], len(pl["deleting"]),
                                   ("; stderr (%d lines), first: %s" % (len(etxt.splitlines()), etxt.splitlines()[0][:200])) if etxt else ""))
                            if len(mset["engine_passes"]) < 400:
                                mset["engine_passes"].append({"chunk": ci, "pass": npass, "status": status, "rc": rc, "sent": len(todo), "log": base + ".rsync.log",
                                                              "deleting_lines": len(pl["deleting"]), "stderr_lines": len(etxt.splitlines())})
                            if pl["deleting"]:
                                problems.append("%s: the engine's log holds %d DELETING line(s) (first: %s): that must be impossible"
                                                % (s["dest"], len(pl["deleting"]), pl["deleting"][0][:200]))
                                result["rc"] = RC_DELETING
                            for pth in pl["paths"]:
                                if any(secret_shape(part) for part in pth.split("/")):
                                    problems.append("%s: a secret-shaped name travelled: %s" % (s["dest"], pth))
                                    break
                            if status == "stalled":
                                problems.append("%s: STALLED: after %ds the engine had written nothing and used no CPU. Most likely a "
                                                "macOS privacy prompt for rsync is waiting on this Mac's screen (PORTABILITY 15a)" % (s["dest"], c["stall_seconds"]))
                                result["rc"] = RC_STALLED
                                stop = "stalled"
                            elif status == "killed-cap":
                                problems.append("%s: stopped by the run-time cap (%ds); whole files only were written, what was "
                                                "proven is saved, and the next run goes on from there" % (s["dest"], cap))
                                result["rc"] = RC_CAP
                                stop = "the cap"
                            elif rc not in (0, 23, 24):
                                problems.append("%s: engine exit code %s (%s)" % (s["dest"], rc, (etxt.splitlines() or ["no stderr"])[-1][:200]))
                                if result["rc"] == RC_VERIFY:
                                    result["rc"] = RC_ENGINE
                            # THE ARRIVAL PROOF, for every file this pass was given. The engine's exit code decides nothing.
                            again = []
                            for i, rel in enumerate(todo):
                                if time.time() >= deadline:
                                    for r2 in todo[i:]:
                                        why.setdefault(r2, "not proven before the run-time cap")
                                    if not stop:
                                        problems.append("%s: the run-time cap (%ds) passed while files were being proven; what was "
                                                        "proven is saved, and the next run goes on from there" % (s["dest"], cap))
                                        result["rc"] = RC_CAP
                                        stop = "the cap"
                                    break
                                drel = plan["dfiles"][ckey(rel)][0] if ckey(rel) in plan["dfiles"] else rel
                                verdict, st3, note = prove_arrival(os.path.join(s["src"], rel), os.path.join(dest_dir, drel))
                                if verdict == "proven":
                                    proven.add(rel)
                                    why.pop(rel, None)
                                    saver.add(rel, st3)              # into the index ONLY when proven, and as it goes
                                    totals["proven_by_sha256"] += 1
                                    if plan["reason"].get(rel) == "repair":
                                        totals["repaired"] += 1
                                elif verdict == "hardlinked":
                                    # ROUND 4 (finding 3): the second link appeared after the chunk was handed over.
                                    # NEVER proven. The file was sent; say plainly whether its content is there.
                                    dpath = os.path.join(dest_dir, drel)
                                    try:
                                        there = os.path.isfile(dpath) and sha256_of(dpath) == sha256_of(os.path.join(s["src"], rel))
                                    except OSError:
                                        there = False
                                    why[rel] = ("%s; it was SENT before that was seen, and its content %s %s, where this tool "
                                                "never deletes" % (note, "ALREADY REACHED THE DESTINATION at" if there
                                                                   else "may have reached the destination (the copy there does not match it now) at", dpath))
                                    sent_linked.append((rel, dpath, there))
                                elif verdict == "unreadable":
                                    if source_deleted(s["src"], plan["root_id"], rel, parent_id_of(plan, rel)):
                                        deleted.append(rel)
                                        why.pop(rel, None)
                                    else:
                                        why[rel] = note
                                elif verdict == "unstable" or (st3 is not None and st3 != tuple(src["files"][rel])):
                                    again.append(rel)                # the source moved on since it was listed: send it again
                                    src["files"][rel] = st3 if st3 is not None else src["files"][rel]
                                    why[rel] = "the source kept changing while it was being copied"
                                else:
                                    why[rel] = note
                            saver.flush()
                            for rel in todo_dirs:
                                if not os.path.isdir(os.path.join(dest_dir, rel)) and os.path.isdir(os.path.join(s["src"], rel)):
                                    missing_dirs.append(rel + "/")
                            todo_dirs = []
                            if stop or status != "ok" or npass == MAX_PASSES:
                                todo = []
                            else:
                                if again:
                                    totals["resent"] += len(again)
                                todo = again
                        if len(chunks) > 1:
                            say("    after chunk %d of %d: %d of %d planned files proven and saved" % (ci, len(chunks), len(proven & planned), len(planned)))
                    if stop:
                        for rel in todo_all:
                            if rel not in proven and rel not in deleted:
                                why.setdefault(rel, "not sent: the run was stopped by %s first" % stop)
                finally:
                    saver.flush()          # an interruption keeps every proof made so far
                versioned = 0
                for d in os.listdir(os.path.join(croot, "versions")):
                    if d == stamp or d.startswith(stamp + "_pass"):
                        vd = os.path.join(croot, "versions", d, *s["dest"].split("/"))
                        if os.path.isdir(vd):
                            versioned += len(walk(vd)["files"])
                # THE ACCOUNTING: planned, minus proven, minus provably deleted. Whatever is left is NOT DELIVERED.
                gone = set(deleted)
                not_proven = sorted(rel for rel in planned if rel not in proven and rel not in gone)
                undelivered = not_proven + missing_dirs
                allowed = deleted_allowed(c, len(planned))
                if deleted:
                    say("    DELETED at the source during the run: %d planned file(s). Each one's folder was listed twice and "
                        "the name was absent both times; they are not at the destination from tonight. Allowed before the "
                        "night fails: %d. First: %s" % (len(deleted), allowed, ", ".join(sorted(deleted)[:5])))
                    deleted_all += ["%s/%s" % (s["dest"], r) for r in sorted(deleted)]
                if len(deleted) > allowed:
                    problems.append("%s: %d planned files were deleted from the source during the run, above the %d allowed "
                                    "(max_deleted_files=%d, max_deleted_fraction=%g of %d planned): that many is not a few "
                                    "temporary files" % (s["dest"], len(deleted), allowed, c["max_deleted_files"],
                                                         c["max_deleted_fraction"], len(planned)))
                # ROUND 4 (finding 3): a second hard link that appeared after the plan fails the night, by name.
                held_only = sorted(r for r in set(held_back) if r not in proven and r not in set(x[0] for x in sent_linked))
                if held_only:
                    problems.append("%s: %d planned file(s) gained a second HARD LINK after the plan and were NOT SENT (first: %s). "
                                    "Another name for the same file may sit in a secrets folder; the walk leaves such files out, "
                                    "and so does the copy" % (s["dest"], len(held_only), held_only[0]))
                    hardlink_all += [("%s/%s" % (s["dest"], r), "NOT SENT", "") for r in held_only]
                if sent_linked:
                    problems.append("%s: %d planned file(s) gained a second HARD LINK after the plan and were SENT before that was "
                                    "seen. THE CONTENT ALREADY REACHED THE DESTINATION and this tool never deletes there: look at "
                                    "each path named below and remove it by hand if the other name is a secret (first: %s at %s)"
                                    % (s["dest"], len(sent_linked), sent_linked[0][0], sent_linked[0][1]))
                    hardlink_all += [("%s/%s" % (s["dest"], r), "SENT", "%s (its content is there now: %s)" % (dp, "YES" if th else "no"))
                                     for r, dp, th in sent_linked]
                totals["hard_linked_after_plan"] += len(held_only) + len(sent_linked)
                mset.update({"hard_linked_after_plan_not_sent": held_only[:500],
                             "hard_linked_after_plan_sent": [[r, dp, th] for r, dp, th in sent_linked[:500]]})
                if undelivered:
                    first = undelivered[0]
                    problems.append("%s: %d file(s) NOT PROVEN at the destination with the source's content (first: %s: %s)"
                                    % (s["dest"], len(undelivered), first, why.get(first, "the folder is missing at the destination"
                                                                                  if first.endswith("/") else "not proven")))
                    undelivered_all += [("%s/%s" % (s["dest"], r), why.get(r, "the folder is missing at the destination"
                                                                           if r.endswith("/") else "not proven")) for r in undelivered]
                say("    proven at the destination: %d of %d source files (%d compared by sha256 tonight, %d re-sent because the "
                    "source changed meanwhile); deleted at the source and confirmed absent: %d; previous copies kept: %d; "
                    "sample of unsent files %d/%d agree; NOT PROVEN: %d"
                    % (len(proven & planned), len(planned), totals["proven_by_sha256"], totals["resent"], len(deleted),
                       versioned, len(sample) - len(repair), len(sample), len(undelivered)))
                mset.update({"deleted_during_run": sorted(deleted)[:5000], "deleted_count": len(deleted),
                             "undelivered": undelivered[:100], "versioned": versioned,
                             "hash_sample": len(sample), "hash_sample_repaired": repair[:20]})
                totals["versioned"] += versioned
                totals["deleted"] += len(deleted)
                totals["undelivered"] += len(undelivered)
            tbl = folder_table(plan, proven, set(deleted))
            mset["folders"] = tbl
            say("    %-34s %10s %14s | %10s %14s | %s" % ("top-level folder", "src files", "src bytes", "dst files", "dst bytes", "dst-only (kept)"))
            for top in sorted(tbl):
                r = tbl[top]
                flag = "" if (r["src_files"] == r["dst_files"] and r["src_bytes"] == r["dst_bytes"]) else ("  <- to copy" if mode == "dry" else "  <- differs")
                say("    %-34s %10d %14d | %10d %14d | %d%s" % (top[:34], r["src_files"], r["src_bytes"], r["dst_files"], r["dst_bytes"], r["dst_only_files"], flag))
                totals["dst_files"] += r["dst_files"]
                totals["dst_bytes"] += r["dst_bytes"]
                totals["dst_only_files"] += r["dst_only_files"]
            mset["symlink_list_file"] = None
            if src["links"]:
                lp = os.path.join(ctx.manifest_dir, "%s_%s_%s_symlinks.tsv" % (stamp, mode, safe))
                with open(lp, "w", encoding="utf-8", errors="surrogateescape") as fh:
                    for rel in sorted(src["links"]):
                        fh.write("%s\t%s\n" % (rel, src["links"][rel]))
                mset["symlink_list_file"] = lp
            manifest["sets"].append(mset)
            if result["rc"] in (RC_STALLED, RC_CAP):
                break
        # ... AND BEFORE GOOD: a run must not say GOOD about a share that has gone away meanwhile.
        if mode == "run" and not nas_is_smb_mounted(ctx):
            problems.append("%s is no longer mounted as a network share at the end of the run" % c["nas_root"])
        done_sets = set(m["dest"] for m in manifest["sets"])
        for s in c["sets"]:
            if s["dest"] not in done_sets:
                problems.append("%s: this set was not reached (the run stopped before it): nothing of it is proven tonight" % s["dest"])
    except KeyboardInterrupt:
        problems.append("interrupted by signal %s" % interrupted["sig"])
        result["rc"] = RC_ENGINE
    except Refused as e:
        problems.append(str(e))
        result["rc"] = e.rc
    except Exception as e:
        problems.append("unexpected error: %s: %s" % (type(e).__name__, e))
        result["rc"] = RC_ENGINE
    finally:
        signal.alarm(0)
        if index is not None:
            index.close()

    unlisted = []
    parent = c.get("report_unlisted_under")
    if parent and os.path.isdir(parent):
        listed = set(os.path.realpath(x["src"]) for x in c["sets"])
        try:
            for name in sorted(os.listdir(parent)):
                full = os.path.join(parent, name)
                if not os.path.isdir(full) or os.path.islink(full) or os.path.realpath(full) in listed:
                    continue
                if any(f in name.casefold() for f in ctx.info["forbid"]):
                    say("not this seat's (never backed up from here): %s" % full)
                else:
                    unlisted.append(full)
                    say("NOT LISTED in seats/%s.conf, so NOT backed up: %s" % (ctx.seat, full))
        except OSError as e:
            say("could not list %s: %s" % (parent, e))
    manifest.update({"unlisted_folders": unlisted, "totals": totals, "problems": problems, "finished": time.time(),
                     "finished_local": now_local_str(time.time()), "seconds": round(time.time() - started, 1),
                     "secret_shape_counts": secret_counts, "other_client_token_counts": token_counts,
                     "undelivered": [u for u, _ in undelivered_all[:500]], "deleted_during_run": deleted_all[:5000]})
    good = not problems
    manifest["good"] = good if mode == "run" else None
    mpath = os.path.join(ctx.manifest_dir, "%s_%s_manifest.json" % (stamp, mode))
    with open(mpath, "w", encoding="utf-8", errors="surrogateescape") as fh:
        json.dump(manifest, fh, indent=1, sort_keys=True)
        fh.write("\n")
    say("--- totals: source in scope %d files, %s; to copy %d files, %s (%d new, %d changed); %d symlinks recorded; "
        "%d entries excluded; took %.0f s"
        % (totals["src_files"], fmt_bytes(totals["src_bytes"]), totals["copy_files"], fmt_bytes(totals["copy_bytes"]),
           totals["new"], totals["changed"], totals["symlinks"], totals["excluded_entries"], time.time() - started))
    say("excluded as secret-shaped (entries, by shape; counts only): %s"
        % (", ".join("%s=%d" % kv for kv in sorted(secret_counts.items())) or "none"))
    say("skipped for having more than one hard link: %d file(s); left out for names differing only in case: %d file(s)"
        % (totals["hard_link_files"], totals["case_collision_files"]))
    if tokens:
        say("in-scope paths that carry another client's project name (REPORTED, not excluded; seats/%s.tokens): %s"
            % (ctx.seat, ", ".join("%s=%d" % kv for kv in sorted(token_counts.items()))))
    say("manifest: %s" % mpath)
    if deleted_all:
        say("DELETED AT THE SOURCE during the run (%d file(s); each one's folder was listed twice and the name was absent "
            "both times; not backed up tonight):" % len(deleted_all))
        for d in deleted_all[:600]:
            say("  DELETED AT SOURCE: %s" % d)
        if len(deleted_all) > 600:
            say("  ... and %d more, all in the manifest" % (len(deleted_all) - 600))
    if hardlink_all:
        say("HARD LINK AFTER THE PLAN (%d file(s)): each had one name when its set was listed and has more than one now. None "
            "is proven; the night fails. This tool deletes nothing at the destination:" % len(hardlink_all))
        for name, what, where in hardlink_all[:600]:
            say("  HARD LINK AFTER THE PLAN, %s: %s%s" % (what, name, (" -> " + where) if where else ""))
        if len(hardlink_all) > 600:
            say("  ... and %d more, in the manifest" % (len(hardlink_all) - 600))
    if mode == "dry":
        est_copy_h = totals["copy_files"] / c["est_files_per_s"] / 3600.0
        est_list_min = (totals["src_files"] / c["est_list_per_s"]) / 60.0
        say("estimate (not a measurement of this run): copying %d files at about %.1f files/s takes about %.1f hours, plus "
            "reading every sent file back for the sha256 proof; after the first copy, each night lists about %d destination "
            "files at about %.0f entries/s (about %.0f minutes) and copies only what changed"
            % (totals["copy_files"], c["est_files_per_s"], est_copy_h, totals["src_files"], c["est_list_per_s"], est_list_min))
        if problems:
            say("DRY RUN finished WITH PROBLEMS (a real run would fail):")
            for p in problems:
                say("  - %s" % p)
            rcode = result["rc"]
        else:
            say("DRY RUN finished: a real run would copy the files above. Nothing was written to the NAS.")
            rcode = RC_OK
    else:
        # ROUND 4 (finding 2): the manifest and the completion marker are written on the share too, so the same
        # question is asked once more, for every client folder, before either is written.
        escapes = [e for e in (dest_escape(ctx, client) for client in sorted(client_roots)) if e]
        for e in escapes:
            problems.append("the manifest and the completion marker were NOT written on the NAS: %s" % e)
            good = False
        try:
            for client, croot in ([] if escapes else list(client_roots.items())):
                cm = dict(manifest)
                cm["sets"] = [m for m in manifest["sets"] if m["client"] == client]
                with open(os.path.join(croot, "manifests", "%s_manifest.json" % stamp), "w", encoding="utf-8", errors="surrogateescape") as fh:
                    json.dump(cm, fh, indent=1, sort_keys=True)
                for m in cm["sets"]:
                    if m.get("symlink_list_file"):
                        with open(m["symlink_list_file"], "rb") as a, open(os.path.join(croot, "manifests", os.path.basename(m["symlink_list_file"])), "wb") as b:
                            b.write(a.read())
                if good:
                    with open(os.path.join(croot, "runs", "RUN_%s_COMPLETE.txt" % stamp), "w", encoding="utf-8") as fh:
                        fh.write("complete and proven %s: manifest manifests/%s_manifest.json\n" % (now_local_str(time.time()), stamp))
        except OSError as e:
            problems.append("could not write the manifest or the completion marker on the NAS: %s" % e)
            good = False
        if good:
            say("GOOD: every in-scope source file is PROVEN at the destination with the source's content (every file of "
                "the plan made when its set started). Nothing was deleted on either side by this tool.%s%s"
                % ((" DELETED at the source during the run, confirmed absent twice, so not backed up tonight: %d file(s), named above "
                    "and in the manifest." % totals["deleted"]) if totals["deleted"] else "",
                   (" NOTE, not backed up and named in the manifest: %d file(s) whose names differ only in case, %d with more than one hard link."
                    % (totals["case_collision_files"], totals["hard_link_files"])) if (totals["case_collision_files"] or totals["hard_link_files"]) else ""))
            ctx.note_attempt("good", "every planned file proven", {"stamp": stamp, "manifest": mpath, "trigger": manifest["trigger"],
                                                                  "counts": totals, "seconds": manifest["seconds"], "set_counts": set_counts,
                                                                  "deleted_during_run": deleted_all[:20]})
            try:
                ix = Index(ctx, readonly=False)
                ix.set_baseline(set_counts)          # the fall rule's baseline, kept a second time beside the proofs
                ix.close()
            except sqlite3.Error as e:
                say("note: the baseline could not be written into the index (%s); the state file holds it" % e)
            rcode = RC_OK
        else:
            say("FAILED (the exit code of the engine is never success; the proof is):")
            for p in problems:
                say("  - %s" % p)
            if undelivered_all:
                say("NOT DELIVERED (%d file(s)), the first %d:" % (len(undelivered_all), min(20, len(undelivered_all))))
                for u, reason in undelivered_all[:20]:
                    say("  NOT DELIVERED: %s (%s)" % (u, reason))
            status = {RC_CAP: "killed-cap", RC_STALLED: "stalled"}.get(result["rc"], "failed")
            ctx.note_attempt(status, "; ".join(problems)[:900], {"stamp": stamp, "manifest": mpath,
                                                                 "undelivered_count": len(undelivered_all),
                                                                 "undelivered": [u for u, _ in undelivered_all[:20]]})
            rcode = result["rc"]
    with open(run_log, "w", encoding="utf-8", errors="surrogateescape") as fh:
        fh.write("\n".join(lines) + "\n")
    out("log: %s" % run_log)
    return rcode


# ── nightly: what the scheduler calls ─────────────────────────────────────────────────────────────────────────
def nightly_decide(ctx, st, lock):
    c = ctx.conf
    o, cl, inw = window_for(ctx.now, c["fire_h"], c["fire_m"], c["window_hours"])
    lg = st.get("last_good")
    if lock is not None and (lock.get("alive") or lock.get("fresh") or lock.get("engines")):
        return ("skip", "a run is in progress (pid %s, started %s%s)" % (lock.get("pid"), lock.get("started_local"),
                                                                        "; its copy engine is still running" if lock.get("engines") and not lock.get("alive") else ""))
    if lg and wall(lg["time"]) >= o:
        return ("skip", "already backed up for the window that opened %s (good at %s)" % (wstr(o), lg["time_local"]))
    if not inw:
        if c["late_fire"] == "run":
            return ("run-late", "outside the window, late_fire=run: catching up the window that opened %s" % wstr(o))
        return ("skip", "fired outside the nightly window (%s to %s); it never runs outside its window on its own. "
                        "The missed night is caught up when the next window opens" % (wstr(o), wstr(cl)))
    if lg:
        missed = (o - wall(lg["time"])).days
        return ("run", "no good backup since the window opened %s (last good %s%s)"
                % (wstr(o), lg["time_local"], ", %d night(s) missed: catching up" % missed if missed >= 1 else ""))
    return ("run", "no good backup on record")


def cmd_nightly(ctx, decide_only=False):
    ctx.mkdirs()
    nlog = os.path.join(ctx.log_dir, "nightly.log")

    def record(msg):
        out(msg)
        with open(nlog, "a", encoding="utf-8") as fh:
            fh.write("%s %s\n" % (now_local_str(ctx.now), msg))

    ctx.found_by = "the nightly job (launchd; its output is a log no seat reads)"
    try:
        if os.path.exists(ctx.hold_file):
            record("nightly[%s]: HELD: %s exists; nothing run" % (ctx.seat, ctx.hold_file))
            return RC_HELD
        ctx.load_conf()
        st = ctx.read_state()
        if ctx.state_note:
            record("nightly[%s]: %s" % (ctx.seat, ctx.state_note))
        action, reason = nightly_decide(ctx, st, lock_status(ctx))
    except Refused as e:
        record("nightly[%s]: REFUSED: %s" % (ctx.seat, e))
        return e.rc
    record("nightly[%s]: %s: %s" % (ctx.seat, action.upper(), reason))
    if decide_only:
        return RC_OK
    st["last_fire"] = {"time": ctx.now, "time_local": now_local_str(ctx.now), "decision": action, "reason": reason}
    ctx.hold_lifted(st)
    if not st.get("first_attempt_at"):
        st["first_attempt_at"] = ctx.now
    ctx.write_state(st)
    rc = RC_OK
    if action == "run":
        rc = cmd_backup(ctx, "run", scheduled=True)
    elif action == "run-late":
        rc = cmd_backup(ctx, "run", scheduled=True, out_of_sequence="late-fire (late_fire=run in the seat conf)")
    record("nightly[%s]: finished rc=%s" % (ctx.seat, rc))
    # The three-day check runs here in its READ-ONLY mode (finding 6): this output goes to a launchd log that no
    # seat reads, so it must never be the place the card is issued, and it changes nothing.
    cmd_watch(ctx, "check")
    return rc


# ── watch: the three-day flag. Reads the state file and the clock; needs neither the NAS nor the job. ─────────
def card_argv(ctx, st, ref, ref_what, hours, reasons):
    try:
        ctx.load_conf()
        cproj = ctx.conf["card_client_project"]
    except Refused:
        cproj = "WED"
    cid = "nas-backup-overdue-%s-%s" % (ctx.seat, time.strftime("%Y%m%d", time.localtime(ref)))
    dq = os.path.join(ctx.tree, "2_Project_Files", "tools", "decision_queue.sh")
    title = "No NAS backup of the %s seat for %d days: approve one now, outside the nightly window?" % (ctx.info["cap"], int(hours // 24))
    bluf = ("The nightly copy of the %s seat's folder and projects to the NAS has not completed since %s (%s, %d hours ago). "
            "What happened: %s. The nightly job keeps trying inside its window either way. Nothing is deleted by a backup: it only copies."
            % (ctx.info["cap"], now_local_str(ref), ref_what, int(hours), " | ".join(reasons[:4])))
    return cid, [dq, "add", "--id", cid, "--client-project", cproj, "--title", title, "--bluf", bluf,
                 "--option", "a:Approve an out-of-sequence backup now:The seat runs one backup straight away, outside the nightly window, and reports the counted result",
                 "--option", "b:Wait for tonight's window:Nothing runs now; the nightly job tries again at its usual time",
                 "--recommended", "b", "--default-action", "b: wait for tonight's window; no backup runs outside the window without your word"]


def cmd_watch(ctx, action, card_id=None):
    """action: check (read-only status), card (print the card command; consumes nothing), mark-raised, mark-armed,
    ack-damage. Exit: 0 ok, held or nothing on record; 3 OVERDUE and the card is not recorded as raised; 4 overdue,
    card recorded as raised; 5 a state file or index was found DAMAGED and no seat has acknowledged it yet (said at
    EVERY call by EVERY caller until `--ack-damage`: the nightly job can find the damage, it cannot use the notice up)."""
    if ctx.found_by == "unknown caller":
        ctx.found_by = "the watch (doctor at a seat's boot, or a hand run)"
    if action == "ack-damage":
        notices = ctx.damage_notices()
        if not notices:
            out("no damage notice to acknowledge")
            return RC_OK
        q = os.path.join(ctx.state_dir, "_quarantine_%s" % time.strftime("%Y-%m-%d"))
        os.makedirs(q, exist_ok=True)
        dst = os.path.join(q, "DAMAGE_NOTICE_%s.acknowledged.%s.%d.jsonl" % (ctx.seat, time.strftime("%H%M%S"), os.getpid()))
        os.rename(ctx.damage_file, dst)
        out("acknowledged %d damage notice(s); the notice file was MOVED to %s (not deleted)" % (len(notices), dst))
        return RC_OK
    st = ctx.read_state()
    if ctx.state_note:
        out("nas-backup watch[%s]: %s" % (ctx.seat, ctx.state_note))
    notices = ctx.damage_notices()
    for d in notices:
        out("nas-backup watch[%s]: DAMAGE NOTICE, not yet acknowledged by a seat: the %s was found damaged at %s by %s and "
            "moved to %s (%s). The three-day clock restarted then. Once read: nas_backup_watch.sh --ack-damage"
            % (ctx.seat, d.get("what", "?"), str(d.get("time_local", "an unknown time"))[:19], d.get("found_by", "?"),
               d.get("moved_to", "?"), str(d.get("error", ""))[:80]))
    rc_quiet = RC_DAMAGE_NOTICE if notices else RC_OK
    if action == "mark-armed":
        if st.get("armed_at"):
            out("already marked armed at %s; unchanged" % now_local_str(st["armed_at"]))
            return RC_OK
        st["armed_at"] = ctx.now
        ctx.write_state(st)
        out("marked armed at %s" % now_local_str(ctx.now))
        return RC_OK
    lg, la, lf = st.get("last_good"), st.get("last_attempt"), st.get("last_fire")
    if os.path.exists(ctx.hold_file) and action in ("check", "card"):
        out("nas-backup watch[%s]: HELD: %s exists, so real runs are refused by design and the three-day flag is not raised%s"
            % (ctx.seat, ctx.hold_file, "; last good backup %s" % lg["time_local"] if lg else "; no good backup on record"))
        return rc_quiet
    if not os.path.exists(ctx.hold_file) and ctx.hold_lifted(st):
        ctx.write_state(st)
        out("nas-backup watch[%s]: the hold is no longer in place and nothing but the hold is on record since: the "
            "three-day clock starts now, %s" % (ctx.seat, now_local_str(ctx.now)))
    # THE CLOCK (finding 5). It starts at the last good backup; before the first good backup, at the EARLIEST thing
    # on record: an arming mark, the first attempt or fire ever (stored once, never rolled), or a damage recovery.
    ref, ref_what = None, None
    if lg:
        ref, ref_what = lg["time"], "the last good backup"
    else:
        cands = [(st.get("armed_at"), "arming (no good backup yet)"),
                 (st.get("first_attempt_at"), "the first attempt on record (no good backup yet)")]
        cands = [x for x in cands if x[0]]
        if cands:
            ref, ref_what = min(cands)
    if ref is None:
        # Nothing on record and not held: the watch itself starts the clock, ONCE, so a job that was meant to be
        # running and never fired at all is still flagged after three days. No other script has to set a mark.
        st["first_attempt_at"] = ctx.now
        ctx.write_state(st)
        out("nas-backup watch[%s]: nothing on record for this seat (no attempt, no fire, no good backup) and it is not held: "
            "the three-day clock starts now, %s" % (ctx.seat, now_local_str(ctx.now)))
        return rc_quiet
    if st.get("clock_floor") and st["clock_floor"] >= ref:
        ref, ref_what = st["clock_floor"], "the hold was lifted (the clock does not run while real runs are held)"
    hours = (ctx.now - ref) / 3600.0
    reasons, grouped, order = [], {}, []
    for a in st.get("recent_attempts", []):
        if a["time"] > ref and a["status"] not in ("good", "held"):
            why = a["reason"].replace("REFUSED — ", "").replace("; nothing run", "")[:400]
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
    if st.get("damage"):
        reasons.append("the state file was found damaged at %s and restarted" % st["damage"]["time_local"][:16])
    ls = lock_status(ctx)
    lock_note = ""
    if ls is not None:
        lock_note = " | lock: pid %s %s" % (ls.get("pid"), "RUNNING since %s" % ls.get("started_local") if (ls.get("alive") or ls.get("engines"))
                                              else "STALE since %s (nas_backup.sh --clear-stale-lock)" % ls.get("started_local"))
    overdue = hours >= FLAG_AFTER_HOURS
    gap_key = "%d" % int(ref)
    flag = st.get("flag") or {}
    raised = bool(flag.get("raised")) and flag.get("gap_key") == gap_key
    cid, argv = card_argv(ctx, st, ref, ref_what, hours, reasons)
    notes = ""
    if la and la.get("undelivered_count"):
        notes += " | last attempt left %d file(s) NOT DELIVERED, first: %s" % (la["undelivered_count"], (la.get("undelivered") or ["?"])[0])
    if lg and (lg.get("counts") or {}).get("case_collision_files"):
        notes += " | %d file(s) not backed up (names differ only in case)" % lg["counts"]["case_collision_files"]
    out("nas-backup watch[%s]: %s; %.1f h since %s (%s)%s%s%s"
        % (ctx.seat, "OVERDUE" if overdue else "ok", hours, ref_what, now_local_str(ref),
           "; last attempt %s %s" % (la["time_local"][:16], la["status"]) if la else "; no attempt on record", lock_note, notes))
    if action == "mark-raised":
        if not overdue:
            raise Refused("REFUSED — nothing is overdue, so there is no card to mark raised")
        st["flag"] = {"gap_key": gap_key, "card_id": card_id or cid, "raised": True, "raised_at": ctx.now}
        ctx.write_state(st)
        out("marked: card %s raised for the gap since %s" % (card_id or cid, now_local_str(ref)))
        return RC_OK
    if not overdue:
        return rc_quiet
    if raised:
        out("  the card for this gap is recorded as raised (%s). Nothing more to do until Kam rules or a backup completes." % flag.get("card_id"))
        return RC_DAMAGE_NOTICE if notices else RC_OVERDUE_RAISED
    if action == "card":
        # Printing the command CONSUMES NOTHING: it is printed at every call until a seat records --mark-raised.
        # The card id is fixed per gap and decision_queue.sh refuses a second card with the same id, so the card
        # itself can be raised once per gap however often this line is printed.
        out("FLAG: no good backup for %d hours (threshold %d). ONE decision card for Kam. This tool PRINTS the command and never runs it:" % (int(hours), FLAG_AFTER_HOURS))
        out("CARD-COMMAND: " + " ".join(shlex.quote(a) for a in argv))
        out("After adding the card: nas_backup_watch.sh --mark-raised %s . If Kam rules a: nas_backup.sh --run --out-of-sequence %s" % (cid, cid))
    else:
        out("  CARD NOT RAISED for this gap. To get the one card command for Kam: bash 2_Project_Files/nas-backup/nas_backup_watch.sh --card")
    return RC_OVERDUE


# ── scan: what is in scope, per set (reads the drive only) ───────────────────────────────────────────────────
def cmd_scan(ctx):
    ctx.load_conf()
    for s in ctx.conf["sets"]:
        t0 = time.time()
        w = walk(s["src"], Rules(ctx, s))
        b = sum(v[0] for v in w["files"].values())
        out("SET %s/%s <- %s : in scope %d files, %d bytes (%s), %d folders, %d symlinks, %d hard-linked files skipped, %d read errors [%.1fs]"
            % (s["client"], s["dest"], s["src"], len(w["files"]), b, fmt_bytes(b), len(w["dirs"]), len(w["links"]), len(w["hardlinks"]), len(w["errors"]), time.time() - t0))
        tops = {}
        for rel, v in w["files"].items():
            r = tops.setdefault(top_of(rel), [0, 0])
            r[0] += 1
            r[1] += v[0]
        for top in sorted(tops, key=lambda k: -tops[k][1]):
            out("    %-40s %9d files %16d bytes (%s)" % (top[:40], tops[top][0], tops[top][1], fmt_bytes(tops[top][1])))
        out("  excluded:")
        for (cat, pat), v in sorted(w["excluded"].items(), key=lambda kv: -kv[1]):
            out("    %-16s %-28s %7d entries" % (cat, pat, v))
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
    ap.add_argument("--accept-shrink", default=None)
    ap.add_argument("--max-seconds", type=int, default=None)
    ap.add_argument("--no-hash", action="store_true")
    ap.add_argument("--decide-only", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--card", action="store_true")
    ap.add_argument("--mark-raised", default=None)
    ap.add_argument("--mark-armed", action="store_true")
    ap.add_argument("--ack-damage", action="store_true")
    a = ap.parse_args(argv)
    try:
        ctx = Ctx(a.seat, a.tree, a.now)
        if a.command == "backup":
            if a.run and a.dry:
                raise Refused("give --run or --dry, not both")
            return cmd_backup(ctx, "run" if a.run else "dry", scheduled=a.scheduled, out_of_sequence=a.out_of_sequence,
                              max_seconds=a.max_seconds, no_hash=a.no_hash, accept_shrink=a.accept_shrink)
        if a.command == "nightly":
            return cmd_nightly(ctx, decide_only=a.decide_only)
        if a.command == "watch":
            if a.ack_damage:
                return cmd_watch(ctx, "ack-damage")
            if a.mark_armed:
                return cmd_watch(ctx, "mark-armed")
            if a.mark_raised:
                return cmd_watch(ctx, "mark-raised", a.mark_raised)
            return cmd_watch(ctx, "card" if a.card else "check")
        if a.command == "scan":
            ctx.readonly = True
            return cmd_scan(ctx)
        if a.command == "clear-stale-lock":
            return cmd_clear_stale_lock(ctx)
        if a.command == "window":
            ctx.load_conf()
            o, c, inw = window_for(ctx.now, ctx.conf["fire_h"], ctx.conf["fire_m"], ctx.conf["window_hours"])
            out("window opens %s, closes %s (local wall time), in window now: %s" % (wstr(o), wstr(c), inw))
            return RC_OK
    except Refused as e:
        err("nas-backup: %s" % e)
        return e.rc
    return RC_REFUSED


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
