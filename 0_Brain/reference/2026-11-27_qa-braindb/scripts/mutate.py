import sys, os, shutil
name, dst = sys.argv[1], sys.argv[2]
SRC = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files"
lane = os.path.join(dst, "2_Project_Files", "brain-db")
os.makedirs(lane)
for f in ("braindb.sh", "braindb_index.py"):
    shutil.copy2(os.path.join(SRC, "brain-db", f), lane)
for d in ("scope", "tests", "proposed"):
    shutil.copytree(os.path.join(SRC, "brain-db", d), os.path.join(lane, d))
os.makedirs(os.path.join(dst, "2_Project_Files", "fleet", "cockpit"))
shutil.copy2(os.path.join(SRC, "fleet/cockpit/seat_resolve.sh"), os.path.join(dst, "2_Project_Files/fleet/cockpit"))
M = {
 "none": [],
 "M1_deny_path_off": [("braindb_index.py", "            hit = next((x for x in sc[\"deny_path\"] if x in low), None)\n", "            hit = None\n")],
 "M2_stop_trusts_pidfile": [("braindb.sh", "  case \"$cmd \" in *\" -D $PGDATA \"*) return 0 ;; esac\n  return 1\n", "  return 0\n")],
 "M3_symlinked_dir_through": [("braindb_index.py", "        if d and os.path.realpath(absd) != os.path.join(rroot, d):", "        if False:")],
 "M4_weak_line_off": [("braindb_index.py", "    elif main and float(main[0][0]) < WEAK:", "    elif False:")],
 "M5_symlinked_file_through": [("braindb_index.py", "            if os.path.islink(p):", "            if False:")],
 "M6_seats_test_off": [("braindb_index.py", "            if seat_rows.get(os.path.basename(rel)) is False:", "            if False:")],
 "M7_tier_always_ok": [("braindb_index.py", "    t = (tier or \"\").strip().strip('\"').strip()\n", "    return True, 'mutant'\n    t = ''\n")],
 "M8_check_always_green": [("braindb_index.py", "    if not diffs and not stale:", "    if True:")],
 "M9_version_guard_off": [("braindb.sh", "  if [ \"$have\" != \"$want\" ]; then", "  if false; then")],
 "M11_hard_deny_off": [("braindb_index.py", "HARD_DENY_PREFIX = (\"4_credentials\", \"3_access_keys\", \"0_brain/dashboard\", \"0_brain/reference\")\nHARD_DENY_SEGMENT = (\"4_credentials\", \"3_access_keys\")", "HARD_DENY_PREFIX = ()\nHARD_DENY_SEGMENT = ()")],
 "M13_seat_word_off": [("braindb_index.py", "            hit = next((x for x in sc[\"deny_seat_word\"] if x in dlow or (kind in RECORD_KINDS and x in nlow)), None)", "            hit = None")],
 "M14_lessons_first_off": [("braindb_index.py", "    if mode != \"default\":", "    if True:")],
}
for f, old, new in M[name]:
    p = os.path.join(lane, f)
    s = open(p, encoding="utf-8").read()
    assert s.count(old) == 1, "mutation anchor not found exactly once: %r" % old
    open(p, "w", encoding="utf-8").write(s.replace(old, new))
print("mutant", name, "at", lane)
