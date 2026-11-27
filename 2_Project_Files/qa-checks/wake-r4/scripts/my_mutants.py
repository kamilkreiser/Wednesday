# my_mutants.py — round-4 checker's OWN mutants on round 4's lock and register code. Each breaks ONE behaviour in a scratch COPY of
# the lane and runs the lane's own suite group against the copy. CAUGHT = at least one check goes red. SURVIVED = the suite stays green.
# (R group runs with WAKE_RACE_TRIALS=40 to save time; that alone turns R08 red on its 'n >= 200' clause, so R08 is counted as red
# only when its own line reports a lost or duplicated block.)
import os, re, shutil, subprocess, sys
LANE = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/wake"; REAL = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files"
S = "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/435f0b28-fa4c-43b1-8811-a27f707f05c7/scratchpad/qa-wake-r4/mymut_%d" % os.getpid()
HC, WP = "handover_core.py", "wake_pack.py"
GW = '          [sec(rel, b.size(rel), head + text + tail, label=rel + " (whole, verbatim)")])'
def carried(expr): return [(WP, GW, GW.replace("head + text + tail", "head + %s + tail" % expr))]
M = [
 # ── the lock (round 4 guards) ──
 ("L1 holds() no longer reads the token: any lock directory at the path counts as mine", [(HC, '    return bool(token) and lock_owner(lock).get("token") == token', '    return bool(token) and os.path.isdir(lock)')], "R"),
 ("L2 the owner is re-read before the ARCHIVE rename only, not before the STATE rename", [(HC, '        if not holds(lock, token):\n            raise LockLost("before the %s rename', '        if what == "archive" and not holds(lock, token):\n            raise LockLost("before the %s rename')], "R"),
 ("L3 a rename that finds the lock directory gone is an I/O fault (rc 4), not LOCK LOST (rc 5)", [(HC, "        except FileNotFoundError:\n            if holds(lock, token):\n                raise\n            raise LockLost(", "        except FileNotFoundError:\n            if True:\n                raise\n            raise LockLost(")], "R"),
 ("L4 release says 'released' when the lock is not this call's (so rc 0 and 'written')", [(HC, '                   % (lock, ("owner pid %s" % o.get("pid")) if o else "no lock or no owner file there"))\n            return False', '                   % (lock, ("owner pid %s" % o.get("pid")) if o else "no lock or no owner file there"))\n            return True')], "R"),
 ("L5 release says 'released' when removing the owner file or the directory FAILED", [(HC, '        eprint("handover: WARNING — could not release the lock at %s: %s" % (lock, e))\n        return False', '        eprint("handover: WARNING — could not release the lock at %s: %s" % (lock, e))\n        return True')], "R"),
 ("L6 on rc 6 the plan and 'written' line are still printed on stdout", [(HC, "    if rc == 0 and not released:\n", '    if rc == 0 and not released:\n        print("\\n".join(a.said))\n')], "R"),
 ("L7 the token is the pid alone (no random part: a reused pid has the same token)", [(HC, 'token = "%d-%s" % (os.getpid(), binascii.hexlify(os.urandom(8)).decode("ascii"))', 'token = "%d" % os.getpid()')], "R"),
 ("L8 an owner-less lock is stale after ONE second, not sixty", [(HC, "OWNERLESS_STALE_SECONDS = 60.0", "OWNERLESS_STALE_SECONDS = 1.0")], "R"),
 ("L9 only the archive temp file is inside the lock; the STATE temp file is beside the state file again", [(HC, '        t2 = os.path.join(lock, "state.tmp." + token)', '        t2 = state_path + ".tmp." + token')], "R"),
 ("L10 the second look accepts ANY stale-looking lock, not the same one (kind only)", [(HC, "            if stale_look(lock, host) == seen:", "            if (stale_look(lock, host) or (None,))[0] == seen[0]:")], "R"),
 ("L11 a writer stopped by an I/O fault leaves its temp files inside the lock directory", [(HC, '        left = set_aside()\n        eprint("handover: REFUSED — I/O fault', '        left = []\n        eprint("handover: REFUSED — I/O fault')], "R"),
 # ── the register (round 4: carried whole) ──
 ("G1 trailing spaces and tabs are stripped from every register line", carried(r'"\n".join(x.rstrip(" \t") for x in text.split("\n"))'), "W"),
 ("G2 CRLF line ends are normalised to LF", carried(r'text.replace("\r\n", "\n")'), "W"),
 ("G3 a register line longer than 2000 characters is CUT at 2000", carried(r'"\n".join(x[:2000] for x in text.split("\n"))'), "W"),
 ("G4 only the first 120 lines of the register are carried", carried(r'"\n".join(text.split("\n")[:120]) + "\n"'), "W"),
 ("G5 no newline is added before the END line when the file has none (END glued to the last row)", [(WP, '    tail = "%s<<< END %s (verbatim) >>>\\n" % ("" if text.endswith("\\n") else "\\n", rel)', '    tail = "%s<<< END %s (verbatim) >>>\\n" % ("", rel)')], "W"),
 ("G6 --check compares the pack's LENGTH, not its content", [(WP, "                if sha(have) != sha(want):", "                if len(have) != len(want):")], "W"),
 ("G7 NUL bytes are removed from the register", carried(r'text.replace("\x00", "")'), "W"),
 ("G8 the BEGIN line is not written (the register starts with no marker) [control: must be caught]", [(WP, '"<<< BEGIN %s (verbatim) >>>\\n" % (rel, len(raw), rows, hashlib.sha256(raw).hexdigest()[:16], rel))', '"%s" % (rel, len(raw), rows, hashlib.sha256(raw).hexdigest()[:16], ""))')], "W"),
 ("G9 a row whose first cell starts with a struck-through marker is dropped ONLY when the register has more than 70 rows", carried(r'("\n".join(x for x in text.split("\n") if not x.startswith("| ~~")) if rows > 70 else text)'), "W"),
 ("G10 over budget: the register is trimmed to its first half instead of the build refusing", [(WP, "    over = tok(total) > a.budget_tokens\n", "    over = tok(total) > a.budget_tokens\n    if over:\n        for _t, _secs in b.parts:\n            for _s in _secs:\n                if 'EXPIRING-GRANTS' in _s['source']:\n                    _s['text'] = _s['text'][:len(_s['text']) // 2] + '\\n'\n        text, rows, total = make(generated)\n        over = tok(total) > a.budget_tokens\n")], "W"),
]
only = sys.argv[1:]
caught = survived = err = 0
for n, (name, edits, group) in enumerate(M, 1):
    mid = name.split()[0]
    if only and mid not in only: continue
    mroot = os.path.join(S, mid, "2_Project_Files"); mlane = os.path.join(mroot, "wake"); os.makedirs(mlane)
    shutil.copytree(os.path.join(LANE, "proposed"), os.path.join(mlane, "proposed"))
    for f in ("handover.sh", "handover_core.py", "wake_pack.py", "wake_census.sh"): shutil.copy(os.path.join(LANE, f), os.path.join(mlane, f))
    for rel in ("tools/seat_note.sh", "fleet/cockpit/seat_resolve.sh"):
        os.makedirs(os.path.dirname(os.path.join(mroot, rel)), exist_ok=True); shutil.copy(os.path.join(REAL, rel), os.path.join(mroot, rel))
    ok = True
    for rel, needle, repl in edits:
        p = os.path.join(mlane, rel); s = open(p, encoding="utf-8").read()
        if s.count(needle) != 1:
            print("MUTANT-ERROR %s :: needle found %d times in %s" % (name, s.count(needle), rel)); ok = False; err += 1; break
        open(p, "w", encoding="utf-8").write(s.replace(needle, repl))
    if not ok: continue
    r0 = subprocess.run([sys.executable, "-c", "import ast,sys; ast.parse(open(sys.argv[1]).read())", os.path.join(mlane, edits[0][0])], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if r0.returncode: print("MUTANT-ERROR %s :: the mutated file does not parse: %s" % (name, r0.stdout.decode()[-200:])); err += 1; continue
    ms = os.path.join(S, mid + "_scratch"); os.makedirs(ms)
    e = dict(os.environ); e.update({"WAKE_UNDER_TEST": mlane, "WAKE_TEST_SCRATCH": ms, "PYTHONDONTWRITEBYTECODE": "1", "WAKE_RACE_TRIALS": "40"})
    r = subprocess.run([sys.executable, os.path.join(LANE, "tests", "run_tests.py"), "--groups", group], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=e)
    out = r.stdout.decode("utf-8", "replace")
    red = []
    for l in out.split("\n"):
        if l.startswith("FAIL "):
            tid = l.split()[1]
            if tid == "R08" and re.search(r"lost 0; both acknowledged 40 of 40; refused 0; base block not exactly once in the archive 0", l): continue
            red.append(tid)
    npass = sum(1 for l in out.split("\n") if l.startswith("PASS "))
    if red: caught += 1; print("CAUGHT   %s :: red: %s (passed %d)" % (name, " ".join(red), npass))
    else: survived += 1; print("SURVIVED %s :: no check went red (passed %d)" % (name, npass))
    sys.stdout.flush()
print("my mutants: %d caught, %d SURVIVED, %d instrument errors, of %d" % (caught, survived, err, caught + survived + err))
