#!/usr/bin/env python3
# secrets_move.py — ANSWER-1 (Kam, live board 2026-11-27 13:36:06, card wed-nas-backup-share-holds-secuura-credentials-1127 = a).
# COUNTS ONLY: this program never opens a file inside the secrets folders and never prints a name from inside them.
# No delete verb exists in this file. The only write verbs are os.mkdir (the quarantine folder) and os.rename (one folder per call).
import json, os, subprocess, sys, time
SHARE = "/Volumes/Backup"
MIRROR = SHARE + "/DevMASTER-mirror"
PARENT = MIRROR + "/!CODING/Secuura/Blockchain"
NAMES = ["4_Credentials", "3_Access_Keys"]
QUAR = SHARE + "/_quarantine_2026-11-27_secuura-secrets"

def now(): return time.strftime("%Y-%m-%d %H:%M:%S %Z")

def mounted_smb():
    r = subprocess.run(["/sbin/mount"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return any((" on %s (smbfs" % SHARE) in ln for ln in r.stdout.splitlines())

def count(top):
    """top-level entries, files, dirs, bytes. Metadata only (listdir, lstat)."""
    errs = []
    files = dirs = nbytes = 0
    top_entries = len(os.listdir(top))
    for dp, dn, fn in os.walk(top, followlinks=False, onerror=lambda e: errs.append(e.errno)):
        dirs += len(dn)
        for f in fn:
            files += 1
            try: nbytes += os.lstat(os.path.join(dp, f)).st_size
            except OSError as e: errs.append(e.errno)
    return {"top_level_entries": top_entries, "files": files, "dirs": dirs, "bytes": nbytes, "walk_errors": len(errs)}

def main():
    cmd = sys.argv[1]
    print("[%s] %s" % (now(), cmd))
    if not mounted_smb():
        print("STOP: %s is not in the mount table as smbfs" % SHARE); return 10
    if cmd == "list":
        out = {}
        for n in NAMES:
            p = os.path.join(PARENT, n)
            if not os.path.isdir(p) or os.path.islink(p):
                print("STOP: absent or not a plain folder: %s" % p); return 11
            real = [x for x in os.listdir(PARENT) if x.casefold() == n.casefold()]
            out[n] = count(p); out[n]["real_name_in_parent"] = real
            print("BEFORE %s: %s" % (p, json.dumps(out[n], sort_keys=True)))
        json.dump(out, open(sys.argv[2], "w"), indent=1, sort_keys=True); return 0
    if cmd == "mkquar":
        if os.path.lexists(QUAR):
            if not os.path.isdir(QUAR) or os.listdir(QUAR):
                print("STOP: %s already exists with content (or is not a folder); refused" % QUAR); return 12
            print("quarantine folder already exists and is EMPTY: used as is"); return 0
        os.mkdir(QUAR); print("created %s" % QUAR); return 0
    if cmd == "move":
        n = sys.argv[2]
        if n not in NAMES: print("STOP: not one of the two named folders"); return 13
        src, dst = os.path.join(PARENT, n), os.path.join(QUAR, n)
        if os.path.lexists(dst): print("STOP: destination already exists: %s" % dst); return 14
        if not os.path.isdir(src): print("STOP: source absent: %s" % src); return 11
        try:
            os.rename(src, dst)          # same-share rename; no fallback of any kind
        except OSError as e:
            print("STOP: rename failed errno=%s (%s). Nothing copied, nothing deleted." % (e.errno, e.strerror)); return 15
        print("renamed %s -> %s" % (src, dst)); return 0
    if cmd == "after":
        before = json.load(open(sys.argv[2])); ok = True; out = {}
        for n in NAMES:
            p = os.path.join(QUAR, n)
            out[n] = count(p)
            same = all(out[n][k] == before[n][k] for k in ("top_level_entries", "files", "dirs", "bytes"))
            gone = not os.path.exists(os.path.join(PARENT, n)) and not os.path.lexists(os.path.join(PARENT, n))
            ok = ok and same and gone
            print("AFTER  %s: %s | equals before: %s | original path exists: %s" % (p, json.dumps(out[n], sort_keys=True), same, not gone))
        ctl = os.path.isdir(PARENT)
        print("positive control: parent %s still exists: %s (entries now: %d)" % (PARENT, ctl, len(os.listdir(PARENT)) if ctl else -1))
        print("quarantine top level entry count: %d" % len(os.listdir(QUAR)))
        json.dump(out, open(sys.argv[3], "w"), indent=1, sort_keys=True)
        print("RESULT: %s" % ("EQUAL and originals gone" if ok and ctl else "INEQUALITY - STOP")); return 0 if ok and ctl else 16
    return 2
sys.exit(main())
