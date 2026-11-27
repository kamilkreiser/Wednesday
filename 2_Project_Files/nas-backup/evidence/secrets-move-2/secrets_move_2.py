#!/usr/bin/env python3
# secrets_move_2.py — ANSWER-4 TASK 1 (Kam, live board 2026-11-27 16:40:18, card
# wed-nas-mirror-37-more-secrets-folders-1127 = a: "Move all 37 aside, same method").
# The same method as secrets_move.py (ANSWER-1), for the 37 folders the sweep listed.
# COUNTS ONLY: this program never opens a file inside the secrets folders and never prints a name from inside them.
# No delete verb exists in this file. The only write verbs are os.makedirs (the PARENTS of a destination, inside
# the existing quarantine folder) and os.rename (one folder per call). A failed rename is a STOP: no fallback.
#   secrets_move_2.py check <old sweep json> <fresh sweep json> <plan.json>   read-only: the set must be exactly the listed 37
#   secrets_move_2.py before <plan.json> <before.json>                        read-only: the four counts of each folder
#   secrets_move_2.py move <plan.json> <before.json> <n>                      ONE folder: recount, rename, recount, verify
#   secrets_move_2.py after <plan.json> <before.json> <after.json>            read-only: every folder counted at its new place
import json, os, subprocess, sys, time
SHARE = "/Volumes/Backup"
MIRROR = SHARE + "/DevMASTER-mirror"
QUAR = SHARE + "/_quarantine_2026-11-27_secuura-secrets"
MORE = QUAR + "/more"
NAMES = ("4_credentials", "3_access_keys")
FIG = ("top_level_entries", "files", "dirs", "bytes")


def now():
    return time.strftime("%Y-%m-%d %H:%M:%S %Z")


def mounted_smb():
    r = subprocess.run(["/sbin/mount"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return any((" on %s (smbfs" % SHARE) in ln for ln in r.stdout.splitlines())


def count(top):
    """top-level entries, files, dirs, bytes. Metadata only (listdir, lstat). Hidden names included."""
    errs = []
    files = dirs = nbytes = 0
    top_entries = len(os.listdir(top))
    for dp, dn, fn in os.walk(top, followlinks=False, onerror=lambda e: errs.append(e.errno)):
        dirs += len(dn)
        for f in fn:
            files += 1
            try:
                nbytes += os.lstat(os.path.join(dp, f)).st_size
            except OSError as e:
                errs.append(e.errno)
    return {"top_level_entries": top_entries, "files": files, "dirs": dirs, "bytes": nbytes, "walk_errors": len(errs)}


def dest_of(src):
    rel = os.path.relpath(src, MIRROR)
    assert not rel.startswith(".."), rel
    return os.path.join(MORE, rel)


def main():
    cmd = sys.argv[1]
    print("[%s] %s" % (now(), " ".join(sys.argv[1:2] + sys.argv[4:])))
    if not mounted_smb():
        print("STOP: %s is not in the mount table as smbfs" % SHARE)
        return 10
    if cmd == "check":
        old = json.load(open(sys.argv[2]))["secret_named_directories"]
        fresh_doc = json.load(open(sys.argv[3]))
        fresh = fresh_doc["secret_named_directories"]
        print("listed by the earlier sweep: %d ; found by the fresh sweep: %d ; read errors in the fresh sweep: %d"
              % (len(old), len(fresh), fresh_doc.get("read_errors", -1)))
        extra = sorted(set(fresh) - set(old))
        missing = sorted(set(old) - set(fresh))
        bad_shape = [p for p in fresh if os.path.basename(p).lower() not in NAMES or not p.startswith(MIRROR + "/")]
        for p in extra:
            print("NOT ONE OF THE LISTED: %s" % p)
        for p in missing:
            print("LISTED BUT NOT FOUND NOW: %s" % p)
        ok = (len(fresh) == 37 and not extra and not missing and not bad_shape and len(set(fresh)) == 37
              and fresh_doc.get("read_errors") == 0)
        live = [p for p in fresh if "/_nas_push_overwritten/" not in p]
        print("in the live mirror: %d ; under _nas_push_overwritten/<stamp>/: %d" % (len(live), len(fresh) - len(live)))
        dests = [dest_of(p) for p in sorted(fresh)]
        print("distinct destinations: %d ; destinations that already exist: %d ; %s exists: %s"
              % (len(set(dests)), sum(1 for d in dests if os.path.lexists(d)), MORE, os.path.lexists(MORE)))
        if not ok or len(set(dests)) != len(dests) or any(os.path.lexists(d) for d in dests):
            print("RESULT: STOP — the set is not exactly the listed 37, or a destination exists. Nothing moved.")
            return 20
        json.dump({"folders": [{"n": i, "src": p, "dst": dest_of(p)} for i, p in enumerate(sorted(fresh))]},
                  open(sys.argv[4], "w"), indent=1, sort_keys=True)
        print("RESULT: the fresh sweep found exactly the 37 listed folders; plan written.")
        return 0
    plan = json.load(open(sys.argv[2]))["folders"]
    if cmd == "before":
        out = {}
        for f in plan:
            p = f["src"]
            if not os.path.isdir(p) or os.path.islink(p):
                print("STOP: absent or not a plain folder: %s" % p)
                return 11
            out[str(f["n"])] = count(p)
            print("BEFORE %2d %s: %s" % (f["n"], p, json.dumps(out[str(f["n"])], sort_keys=True)))
        json.dump(out, open(sys.argv[3], "w"), indent=1, sort_keys=True)
        print("RESULT: %d folders counted, walk errors in total: %d" % (len(out), sum(v["walk_errors"] for v in out.values())))
        return 0 if all(v["walk_errors"] == 0 for v in out.values()) else 12
    before = json.load(open(sys.argv[3]))
    if cmd == "move":
        n = int(sys.argv[4])
        f = plan[n]
        assert f["n"] == n
        src, dst = f["src"], f["dst"]
        if os.path.basename(src).lower() not in NAMES or not src.startswith(MIRROR + "/") or not dst.startswith(MORE + "/"):
            print("STOP: not a listed secrets folder under the mirror, or a destination outside the quarantine")
            return 13
        if not os.path.isdir(QUAR):
            print("STOP: the quarantine folder %s does not exist" % QUAR)
            return 13
        if os.path.lexists(dst):
            print("STOP: destination already exists: %s" % dst)
            return 14
        if not os.path.isdir(src) or os.path.islink(src):
            print("STOP: source absent or not a plain folder: %s" % src)
            return 11
        b = count(src)
        if any(b[k] != before[str(n)][k] for k in FIG) or b["walk_errors"]:
            print("STOP: the folder's counts changed since the list step (%s then, %s now). Not moved."
                  % (json.dumps(before[str(n)], sort_keys=True), json.dumps(b, sort_keys=True)))
            return 17
        parent_src = os.path.dirname(src)
        os.makedirs(os.path.dirname(dst), exist_ok=True)          # the PARENTS only; the folder itself is never pre-created
        if os.path.lexists(dst):
            print("STOP: destination appeared: %s" % dst)
            return 14
        try:
            os.rename(src, dst)          # same-share rename; no fallback of any kind
        except OSError as e:
            print("STOP: rename failed errno=%s (%s). Nothing copied, nothing deleted." % (e.errno, e.strerror))
            return 15
        a = count(dst)
        same = all(a[k] == b[k] for k in FIG) and a["walk_errors"] == 0
        gone = not os.path.exists(src) and not os.path.lexists(src)
        parent_ok = os.path.isdir(parent_src)
        print("MOVED %2d %s -> %s | before %s | after %s | equal: %s | original path gone: %s | its parent still present: %s"
              % (n, src, dst, json.dumps(b, sort_keys=True), json.dumps(a, sort_keys=True), same, gone, parent_ok))
        return 0 if (same and gone and parent_ok) else 16
    if cmd == "after":
        ok = True
        out = {}
        for f in plan:
            n = str(f["n"])
            if not os.path.isdir(f["dst"]):
                print("AFTER  %2d MISSING at its new place: %s" % (f["n"], f["dst"]))
                ok = False
                continue
            out[n] = count(f["dst"])
            same = all(out[n][k] == before[n][k] for k in FIG) and out[n]["walk_errors"] == 0
            gone = not os.path.lexists(f["src"])
            ok = ok and same and gone
            print("AFTER  %2d %s: %s | equals before: %s | original path exists: %s" % (f["n"], f["dst"], json.dumps(out[n], sort_keys=True), same, not gone))
        json.dump(out, open(sys.argv[4], "w"), indent=1, sort_keys=True)
        tb = dict((k, sum(v[k] for v in before.values())) for k in FIG)
        ta = dict((k, sum(v[k] for v in out.values())) for k in FIG)
        print("TOTALS before: %s" % json.dumps(tb, sort_keys=True))
        print("TOTALS after:  %s" % json.dumps(ta, sort_keys=True))
        print("quarantine top level entry count: %d (the first two folders and `more`)" % len(os.listdir(QUAR)))
        print("positive control: the mirror %s still exists: %s" % (MIRROR, os.path.isdir(MIRROR)))
        print("RESULT: %s" % ("EQUAL for all %d and originals gone" % len(plan) if ok and tb == ta else "INEQUALITY - STOP"))
        return 0 if ok and tb == ta else 16
    return 2


sys.exit(main())
