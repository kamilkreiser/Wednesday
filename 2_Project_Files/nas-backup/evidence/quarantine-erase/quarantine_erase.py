#!/usr/bin/env python3
# quarantine_erase.py — ANSWER-6 TASK 1 (Kam, live board 2026-11-27 21:24:41, card
# wed-nas-quarantine-39-secrets-folders-erase-or-keep-1127 = a: "Erase the quarantine from the NAS").
# COUNTS ONLY: this program never opens a file inside the 39 folders and never prints a name from inside them.
# The ONLY delete verbs are two shutil.rmtree calls, each on ONE literal absolute path that is asserted
# immediately before the call: the quarantine folder, and (only if the NAS moved the erase there) its
# namesake inside the share's #recycle folder. No glob. An error during a removal is recorded and STOPS.
#   quarantine_erase.py list <before.json>            read-only: the 39 folders, four counts each, compared with the records
#   quarantine_erase.py originals <out.json>          read-only: the seven originals on the drive, four counts each
#   quarantine_erase.py tops <out.json>               read-only: top-level names of the share, the mirror, #recycle
#   quarantine_erase.py recycle <out.json>            read-only, names only: is anything of the quarantine in #recycle
#   quarantine_erase.py erase <before.json>           THE ERASE (re-lists and re-compares first; any difference: STOP)
#   quarantine_erase.py erase-recycle                 removes exactly #recycle/<the quarantine's name>, if present
#   quarantine_erase.py after <before.json> <tops_before.json> <tops_after.json>
import json, os, shutil, subprocess, sys, time

SHARE = "/Volumes/Backup"
QUAR = "/Volumes/Backup/_quarantine_2026-11-27_secuura-secrets"
RECYCLE = "/Volumes/Backup/#recycle"
RECYCLED_QUAR = "/Volumes/Backup/#recycle/_quarantine_2026-11-27_secuura-secrets"
MIRROR = "/Volumes/Backup/DevMASTER-mirror"
DRIVE = "/Volumes/DevMASTER"
HERE = os.path.dirname(os.path.abspath(__file__))
REC_FIRST = os.path.join(HERE, "..", "secrets-move", "after.json")        # the first move's result (2 folders)
REC_PLAN = os.path.join(HERE, "..", "secrets-move-2", "plan.json")        # the second move's 37 destinations
REC_SECOND = os.path.join(HERE, "..", "secrets-move-2", "after.json")     # their counts after the move
NAMES = ("4_credentials", "3_access_keys")
FIG = ("top_level_entries", "files", "dirs", "bytes")
REHEARSAL = os.environ.get("QE_REHEARSAL") == "1" and not SHARE.startswith("/Volumes/")


def now():
    return time.strftime("%Y-%m-%d %H:%M:%S %Z")


def mounted_smb():
    if REHEARSAL:
        return True
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


def expected():
    """The 39 folders and their recorded counts, from the two earlier results' own evidence files."""
    exp = {}
    first = json.load(open(REC_FIRST))
    for name in sorted(first):
        exp[QUAR + "/" + name] = dict((k, first[name][k]) for k in FIG)
    plan = json.load(open(REC_PLAN))["folders"]
    second = json.load(open(REC_SECOND))
    for f in plan:
        dst = f["dst"]
        if not REHEARSAL:
            assert dst.startswith(QUAR + "/more/"), dst
        else:
            dst = QUAR + dst.split("_quarantine_2026-11-27_secuura-secrets", 1)[1]
        exp[dst] = dict((k, second[str(f["n"])][k]) for k in FIG)
    return exp


def sweep_quarantine():
    """Every folder named 4_Credentials or 3_Access_Keys (any case) under the quarantine, NOT entered;
    and how many files and other entries lie OUTSIDE those folders (names never recorded)."""
    found, files_outside, links_outside, errs, dirs_outside = [], 0, 0, 0, 0
    stack = [QUAR]
    while stack:
        path = stack.pop()
        try:
            it = os.scandir(path)
        except OSError:
            errs += 1
            continue
        with it:
            for e in it:
                try:
                    if e.is_symlink():
                        links_outside += 1
                    elif e.is_dir(follow_symlinks=False):
                        if e.name.lower() in NAMES:
                            found.append(e.path)
                        else:
                            dirs_outside += 1
                            stack.append(e.path)
                    else:
                        files_outside += 1
                except OSError:
                    errs += 1
    return sorted(found), files_outside, links_outside, dirs_outside, errs


def list_and_compare(verbose):
    """Returns (ok, counts by path). ok is False on ANY difference from the records."""
    exp = expected()
    found, files_outside, links_outside, dirs_outside, errs = sweep_quarantine()
    ok = True
    print("recorded folders: %d ; found now: %d ; files outside them: %d ; symlinks outside them: %d ; "
          "plain parent folders between them: %d ; read errors: %d"
          % (len(exp), len(found), files_outside, links_outside, dirs_outside, errs))
    for p in sorted(set(found) - set(exp)):
        print("DIFFERENCE: found but not in the records: %s" % p)
        ok = False
    for p in sorted(set(exp) - set(found)):
        print("DIFFERENCE: in the records but not found: %s" % p)
        ok = False
    if len(exp) != 39 or len(found) != 39 or files_outside or links_outside or errs:
        print("DIFFERENCE: not exactly 39 folders with nothing else beside them")
        ok = False
    top = sorted(os.listdir(QUAR))
    if top != ["3_Access_Keys", "4_Credentials", "more"]:
        print("DIFFERENCE: the quarantine's top level is not the two folders and `more` (%d entries)" % len(top))
        ok = False
    got = {}
    for i, p in enumerate(sorted(found)):
        c = count(p)
        got[p] = c
        e = exp.get(p)
        same = e is not None and all(c[k] == e[k] for k in FIG) and c["walk_errors"] == 0
        if not same:
            ok = False
        if verbose or not same:
            print("%s %2d %s | now %s | recorded %s | equal: %s"
                  % ("ROW" if same else "DIFFERENCE", i + 1, os.path.relpath(p, QUAR), json.dumps(c, sort_keys=True),
                     json.dumps(e, sort_keys=True) if e else "none", same))
    tot = dict((k, sum(v[k] for v in got.values())) for k in FIG)
    tot_exp = dict((k, sum(v[k] for v in exp.values())) for k in FIG)
    print("TOTALS now:      %s" % json.dumps(tot, sort_keys=True))
    print("TOTALS recorded: %s" % json.dumps(tot_exp, sort_keys=True))
    if tot != tot_exp:
        ok = False
    return ok, got


def originals():
    """The seven folders on the drive that the 39 were copies of. Counts only."""
    rels = set()
    rels.add("!CODING/Secuura/Blockchain/4_Credentials")
    rels.add("!CODING/Secuura/Blockchain/3_Access_Keys")
    for f in json.load(open(REC_PLAN))["folders"]:
        rel = f["src"].split("/DevMASTER-mirror/", 1)[1]
        if rel.startswith("_nas_push_overwritten/"):
            rel = rel.split("/", 2)[2]
        rels.add(rel)
    out = {}
    for rel in sorted(rels):
        p = os.path.join(DRIVE, rel)
        if os.path.islink(p) or not os.path.isdir(p):
            out[rel] = {"present": False}
        else:
            c = count(p)
            c["present"] = True
            out[rel] = c
        print("ORIGINAL %s: %s" % (rel, json.dumps(out[rel], sort_keys=True)))
    return out


def tops():
    out = {}
    for label, p in (("share", SHARE), ("mirror", MIRROR), ("recycle", RECYCLE)):
        try:
            out[label] = sorted(os.listdir(p))
        except OSError as e:
            out[label] = "CANNOT LIST: errno %s" % e.errno
        print("TOP %s (%s): %s" % (label, p, json.dumps(out[label])))
    return out


def recycle_look():
    """Names only. Is the quarantine, or any of the 39 folders' paths, inside #recycle?"""
    res = {"recycle_listable": True, "hits": []}
    try:
        names = os.listdir(RECYCLE)
    except OSError as e:
        res["recycle_listable"] = False
        print("CANNOT SEE INTO %s: errno %s (%s)" % (RECYCLE, e.errno, e.strerror))
        return res
    print("%s is listable: %d top-level entries" % (RECYCLE, len(names)))
    cands = [RECYCLED_QUAR]
    for p in sorted(expected()):
        cands.append(RECYCLE + "/" + os.path.relpath(p, SHARE))           # where it was erased from
    for f in json.load(open(REC_PLAN))["folders"]:
        cands.append(RECYCLE + "/DevMASTER-mirror/" + f["src"].split("/DevMASTER-mirror/", 1)[1])   # its older path
    cands.append(RECYCLE + "/DevMASTER-mirror/!CODING/Secuura/Blockchain/4_Credentials")
    cands.append(RECYCLE + "/DevMASTER-mirror/!CODING/Secuura/Blockchain/3_Access_Keys")
    for n in names:
        if "quarantine" in n.lower() or n.lower() in NAMES:
            cands.append(RECYCLE + "/" + n)
    seen = set()
    for c in cands:
        if c in seen:
            continue
        seen.add(c)
        if os.path.lexists(c):
            res["hits"].append(c)
            print("IN THE RECYCLE FOLDER: %s" % c)
    print("candidate paths looked for: %d ; present: %d" % (len(seen), len(res["hits"])))
    return res


class Stop(Exception):
    pass


def _onerror(func, path, exc_info):
    # records and STOPS. The path is printed only down to the folder level of the 39 (never a name inside them).
    shown = path
    low = path.lower()
    for nm in NAMES:
        i = low.find("/" + nm)
        if i >= 0:
            shown = path[:i + 1 + len(nm)] + ("/<inside>" if len(path) > i + 1 + len(nm) else "")
            break
    raise Stop("removal error in %s at %s: %s" % (getattr(func, "__name__", func), shown, exc_info[1].__class__.__name__
                                                 + " errno " + str(getattr(exc_info[1], "errno", "?"))))


def main():
    cmd = sys.argv[1]
    print("[%s] %s" % (now(), cmd))
    if not mounted_smb():
        print("STOP: %s is not in the mount table as smbfs" % SHARE)
        return 10
    if cmd == "list":
        ok, got = list_and_compare(True)
        json.dump(got, open(sys.argv[2], "w"), indent=1, sort_keys=True)
        print("RESULT: %s" % ("the 39 recorded folders, every count equal to the records" if ok
                              else "DIFFERENCE FROM THE RECORDS - STOP, erase nothing"))
        return 0 if ok else 20
    if cmd == "originals":
        json.dump(originals(), open(sys.argv[2], "w"), indent=1, sort_keys=True)
        return 0
    if cmd == "tops":
        json.dump(tops(), open(sys.argv[2], "w"), indent=1, sort_keys=True)
        return 0
    if cmd == "recycle":
        res = recycle_look()
        json.dump(res, open(sys.argv[2], "w"), indent=1, sort_keys=True)
        return 0 if res["recycle_listable"] else 30
    if cmd == "erase":
        before = json.load(open(sys.argv[2]))
        ok, got = list_and_compare(False)
        if not ok or got != before:
            print("STOP: the quarantine differs from the records or from the list step. Nothing erased.")
            return 20
        if os.path.islink(QUAR) or not os.path.isdir(QUAR):
            print("STOP: the quarantine path is not a plain folder. Nothing erased.")
            return 21
        target = QUAR
        if not REHEARSAL:
            assert target == "/Volumes/Backup/_quarantine_2026-11-27_secuura-secrets", target
        assert target and os.path.isabs(target) and target.endswith("/_quarantine_2026-11-27_secuura-secrets"), target
        t0 = time.time()
        print("[%s] shutil.rmtree(%r) starts" % (now(), target))
        try:
            shutil.rmtree(target, onerror=_onerror)
        except Stop as e:
            print("[%s] STOPPED: %s" % (now(), e))
            return 22
        print("[%s] shutil.rmtree returned without error after %.1f s" % (now(), time.time() - t0))
        print("the quarantine path exists now: %s (lexists: %s)" % (os.path.exists(QUAR), os.path.lexists(QUAR)))
        return 0 if not os.path.lexists(QUAR) else 23
    if cmd == "erase-recycle":
        target = RECYCLED_QUAR
        if not REHEARSAL:
            assert target == "/Volumes/Backup/#recycle/_quarantine_2026-11-27_secuura-secrets", target
        assert target and os.path.isabs(target) and target.endswith("/#recycle/_quarantine_2026-11-27_secuura-secrets"), target
        if os.path.lexists(QUAR):
            print("STOP: the quarantine itself still exists; the recycle step runs only after the erase.")
            return 24
        if not os.path.lexists(target):
            print("nothing to remove: %s does not exist" % target)
            return 0
        if os.path.islink(target) or not os.path.isdir(target):
            print("STOP: %s is not a plain folder" % target)
            return 21
        c = count(target)
        print("in the recycle folder before its removal (counts only): %s" % json.dumps(c, sort_keys=True))
        t0 = time.time()
        print("[%s] shutil.rmtree(%r) starts" % (now(), target))
        try:
            shutil.rmtree(target, onerror=_onerror)
        except Stop as e:
            print("[%s] STOPPED: %s" % (now(), e))
            return 22
        print("[%s] shutil.rmtree returned without error after %.1f s" % (now(), time.time() - t0))
        print("the recycled path exists now: %s" % os.path.lexists(target))
        return 0 if not os.path.lexists(target) else 23
    if cmd == "after":
        tb = json.load(open(sys.argv[3]))
        ta = json.load(open(sys.argv[4]))
        ok = True
        gone = not os.path.exists(QUAR) and not os.path.lexists(QUAR)
        print("the quarantine path is gone: %s" % gone)
        ok = ok and gone
        missing = sorted(set(tb["share"]) - set(ta["share"]))
        added = sorted(set(ta["share"]) - set(tb["share"]))
        print("share top level: %d names before, %d after ; gone: %s ; new: %s"
              % (len(tb["share"]), len(ta["share"]), json.dumps(missing), json.dumps(added)))
        ok = ok and missing == ["_quarantine_2026-11-27_secuura-secrets"] and added == []
        print("mirror top level unchanged: %s (%d names)" % (tb["mirror"] == ta["mirror"], len(ta["mirror"])))
        ok = ok and tb["mirror"] == ta["mirror"]
        print("control: the mirror folder still exists: %s ; the share still lists: %s"
              % (os.path.isdir(MIRROR), len(os.listdir(SHARE)) > 0))
        print("RESULT: %s" % ("GONE, and nothing else at the share's top level changed" if ok else "NOT AS EXPECTED - STOP"))
        return 0 if ok else 16
    return 2


sys.exit(main())
