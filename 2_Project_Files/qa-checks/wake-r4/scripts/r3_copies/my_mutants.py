# my_mutants.py — (a) the first checker's 18 mutants, needles ADAPTED to round 3's code where the old needle is gone (marked "adapted");
# (b) 16 NEW mutants of my own (Y01..Y16). Each is applied to a scratch COPY of the tools; the lane's own run_tests.py is run against the
# copy (WAKE_UNDER_TEST) for the named groups. CAUGHT = at least one check went red. The lane's files are only read.
import os, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
SCR = os.path.join(BASE, "mymut_%s" % sys.argv[1]); WHICH = sys.argv[1]
HC, HS, WP = "handover_core.py", "handover.sh", "wake_pack.py"
HA, HB = "proposed/launcher_hunk_A.sh", "proposed/launcher_hunk_B.sh"
Q = [
 ("Q01 rename order swapped", [(HC, "        if new_arch is not None:\n            os.replace(tmps[0], arch_path)\n        os.replace(t2, state_path)\n",
                                "        os.replace(t2, state_path)\n        if new_arch is not None:\n            os.replace(tmps[0], arch_path)\n")], "HSR"),
 ("Q02 changed-on-disk check removed", [(HC, "        if read_bytes(state_path) != cur or read_bytes(arch_path) != prev_arch:", "        if False:")], "HSR"),
 ("Q03 temp-file read-back checks removed", [(HC, "            if read_bytes(t) != new_arch:", "            if False:"), (HC, "        if read_bytes(t2) != new_state:", "        if False:")], "HSR"),
 ("Q04 cap off by one", [(HC, "    if len(block) > cap:", "    if len(block) >= cap:")], "HS"),
 ("Q05 trailing newline no longer ensured", [(HC, "    if block.strip() and not block.endswith(b\"\\n\"):\n        block += b\"\\n\"\n", "")], "HS"),
 ("Q06 seat guard blinded to WED_AGENT", [(HS, "seat_note_dir \"$TREE\" handover || exit 2", "unset WED_AGENT; seat_note_dir \"$TREE\" handover || exit 2")], "HS"),
 ("Q07 (adapted) dead marker needs no date and no word boundary", [(WP, "    dm = DEAD_FORM.match(lead(first))", "    dm = re.match(r\"(DEAD|EXPIRED|ENDED|LAPSED|CLOSED|RETIRED)()\", lead(first))")], "W"),
 ("Q08 (adapted) other-seat match needs no separator", [(WP, "\\b\\s*(?::|\\(|\\u2014|\\u2013|-(?![\\w])|,)\" % (SEAT_ALT, SEAT_ALT))", "\\b\" % (SEAT_ALT, SEAT_ALT))")], "W"),
 ("Q09 budget counts characters, not bytes", [(WP, "            rows.append((title.split(\".\")[0], s[\"label\"], s[\"src_bytes\"], len(s[\"text\"].encode(\"utf-8\"))))",
                                                "            rows.append((title.split(\".\")[0], s[\"label\"], s[\"src_bytes\"], len(s[\"text\"])))"),
                                               (WP, "    body_b = len(body.encode(\"utf-8\"))", "    body_b = len(body)"),
                                               (WP, "        new_total = len(head.encode(\"utf-8\")) + body_b", "        new_total = len(head) + body_b")], "W"),
 ("Q10 ledger Rule sentence cut at 70", [(WP, "RULE_MAX = 700", "RULE_MAX = 70")], "W"),
 ("Q11 (adapted) --check ignores a changed sidecar", [(WP, "                    if sha(shave) != sha(swant):", "                    if False:")], "W"),
 ("Q12 (adapted) end date found anywhere in the EXPIRES cell", [(WP, "        em = END_FORM.match(lead(exp))", "        em = END_FORM.search(lead(exp))")], "W"),
 ("Q13 (adapted) hunk B uses the pack prompt even when the build failed", [(HB, " if [ \"${WAKE_PACK_OK:-0}\" = \"1\" ]; then", " if true; then")], "P"),
 ("Q14 (adapted) hunk A ignores the build's exit code (file test kept)", [(HA, "    if [ \"$WAKE_RC\" -eq 0 ] && [ -s \"$WAKE_PACK\" ]; then", "    if [ -s \"$WAKE_PACK\" ]; then")], "P"),
 ("Q15 check ignores a header naming another seat", [(HC, "        if fields.get(\"seat\") != a.seat:", "        if False:")], "HSD"),
 ("Q16 every grant row dropped (control)", [(WP, "        verdict, why = classify_grant(line, b.seat, b.today)", "        verdict, why = (\"dead\", \"qa\")")], "W"),
 ("Q17 (adapted) unreadable state file treated as absent", [(HC, "    except OSError as e:\n        raise ReadFault(path, e)", "    except OSError as e:\n        return None")], "HS"),
 ("Q18 (adapted) strike-through no longer unwrapped", [(WP, "MARKUP = EMPH + \"~\"", "MARKUP = EMPH")], "W"),
]
Y = [
 ("Y01 release removes a lock that is NOT this process's (the pid test dropped)", [(HC, "        if o.get(\"pid\") != str(os.getpid()):", "        if False:")], "HR"),
 ("Y02 STALE is declared for a dead pid on ANY host (the host test dropped)", [(HC, "            if pid is not None and o.get(\"host\") == host and not pid_alive(pid):", "            if pid is not None and not pid_alive(pid):")], "R"),
 ("Y03 the changed-on-disk check looks at the state file only (an archive edit during the write is unseen)", [(HC, "        if read_bytes(state_path) != cur or read_bytes(arch_path) != prev_arch:", "        if read_bytes(state_path) != cur:")], "HR"),
 ("Y04 the owner file records the PARENT's pid, not the writer's", [(HC, "% (os.getpid(), host, stamp, int(time.time())))", "% (os.getppid(), host, stamp, int(time.time())))")], "HR"),
 ("Y05 the lock path is different for every process (no mutual exclusion) [control: must be caught]", [(HC, "    return os.path.join(tasks_dir, \"STATE-%s.lock.d\" % seat)", "    return os.path.join(tasks_dir, \"STATE-%s.lock.d.%d\" % (seat, os.getpid()))")], "R"),
 ("Y06 a refused lock exits 0 [control: must be caught]", [(HC, "        eprint(\"handover: REFUSED — %s\" % e)\n        return 5", "        eprint(\"handover: REFUSED — %s\" % e)\n        return 0")], "R"),
 ("Y07 --check no longer reports 'a build now would be over budget'", [(WP, "        if over:\n            faults.append(\"a build now would be over budget", "        if False:\n            faults.append(\"a build now would be over budget")], "WD"),
 ("Y08 --check is silent when the pack's front matter has no generated: line", [(WP, "            if stamp is None:\n                faults.append(", "            if stamp is None:\n                (lambda x: None)(")], "WD"),
 ("Y09 the state part accepts a STATE file with no '## FLOOR' part", [(WP, "        if not re.search(r\"^## FLOOR\\s*$\", state, re.M):", "        if False:")], "WD"),
 ("Y10 the pack is written BEFORE its sidecar", [(WP, "        for path, body in ((side, side_text), (out, text)):", "        for path, body in ((out, text), (side, side_text)):")], "WC"),
 ("Y11 hunk A accepts an EMPTY pack file (-e, not -s)", [(HA, "    if [ \"$WAKE_RC\" -eq 0 ] && [ -s \"$WAKE_PACK\" ]; then", "    if [ \"$WAKE_RC\" -eq 0 ] && [ -e \"$WAKE_PACK\" ]; then")], "P"),
 ("Y12 estimated tokens round DOWN (the budget lets one more token through)", [(WP, "    return (n + 3) // 4", "    return n // 4")], "WC"),
 ("Y13 the archive entry is added at the END, not the top [control: must be caught]", [(HC, "    new = prefix + entry_head + old_body + sep + rest", "    new = prefix + rest + entry_head + old_body + sep")], "H"),
 ("Y14 the seats' client words are swapped [control: must be caught]", [(WP, "SEAT_CLIENTS = {\"wednesday\": (\"secuura\",), \"tuesday\": (\"datasec\",), \"friday\": None}", "SEAT_CLIENTS = {\"wednesday\": (\"datasec\",), \"tuesday\": (\"secuura\",), \"friday\": None}")], "W"),
 ("Y15 temp files are not fsynced [expected to survive: no test can see it]", [(HC, "        f.flush()\n        os.fsync(f.fileno())\n    return tmp", "        f.flush()\n    return tmp")], "H"),
 ("Y16 handover.sh's seam guard looks at HANDOVER_TREE only (a typed HANDOVER_TEST_STAMP is honoured on a real tree)", [(HS, "if [ -n \"${HANDOVER_TREE:-}${HANDOVER_TEST_STAMP:-}${HANDOVER_TEST_BREAK:-}\" ] && ! tree_is_temp \"$TREE\"; then", "if [ -n \"${HANDOVER_TREE:-}\" ] && ! tree_is_temp \"$TREE\"; then")], "H"),
]
M = Q if WHICH == "Q" else Y
caught = 0; errs = 0
for n, (name, edits, groups) in enumerate(M, 1):
    mroot = os.path.join(SCR, "m%02d" % n, "2_Project_Files"); mlane = os.path.join(mroot, "wake"); os.makedirs(mlane)
    shutil.copytree(os.path.join(LANE, "proposed"), os.path.join(mlane, "proposed"))
    for f in ("handover.sh", "handover_core.py", "wake_pack.py", "wake_census.sh"): shutil.copy(os.path.join(LANE, f), os.path.join(mlane, f))
    for rel in ("tools/seat_note.sh", "fleet/cockpit/seat_resolve.sh"):
        os.makedirs(os.path.dirname(os.path.join(mroot, rel)), exist_ok=True); shutil.copy(os.path.join(REAL, rel), os.path.join(mroot, rel))
    ok = True
    for rel, needle, repl in edits:
        p = os.path.join(mlane, rel); s = open(p, encoding="utf-8").read()
        if s.count(needle) != 1:
            print("MUTANT-ERROR %s :: needle found %d times in %s" % (name, s.count(needle), rel)); ok = False; errs += 1; break
        open(p, "w", encoding="utf-8").write(s.replace(needle, repl))
    if not ok: continue
    if any(rel.startswith("proposed/launcher_hunk") for rel, _, _ in edits):
        subprocess.run([sys.executable, os.path.join(mlane, "proposed", "build_launcher_diff.py"), "--launcher", R + "/Launch_Wednesday.command", "--write"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=ENV())
    ms = os.path.join(SCR, "m%02d_scratch" % n); os.makedirs(ms)
    e = ENV({"WAKE_UNDER_TEST": mlane, "WAKE_TEST_SCRATCH": ms, "WAKE_RACE_TRIALS": "200"})
    r = subprocess.run([sys.executable, "-B", os.path.join(LANE, "tests", "run_tests.py"), "--groups", groups], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=e)
    out = r.stdout.decode("utf-8", "replace")
    red = [l.split()[1] for l in out.split("\n") if l.startswith("FAIL ")]
    tail = [l for l in out.split("\n") if l.startswith("checks:")]
    caught += bool(red)
    print("%s %s :: groups %s :: red: %s :: %s" % ("CAUGHT  " if red else "SURVIVED", name, groups, " ".join(red) or "-", tail[-1] if tail else "no count line"))
    sys.stdout.flush()
print("%s mutants: %d applied, %d caught, %d survived, %d needle errors" % (WHICH, len(M) - errs, caught, len(M) - errs - caught, errs))
