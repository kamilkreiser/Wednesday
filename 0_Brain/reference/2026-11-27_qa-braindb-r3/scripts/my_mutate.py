#!/usr/bin/env python3
"""my_mutate.py <name|--list> <lanecopy 2_Project_Files dir> <dst>: copy the lane COPY into <dst>/WEDNESDAY/2_Project_Files and break one thing.
NEW mutants against round-3 code (and the first checker's M6/M7/M13 re-anchored). The lane itself is never touched."""
import sys, os, shutil
M = {
 "none": None,
 # --- first checker's mutants whose anchors no longer matched, re-anchored on round-3 text
 "C_M6_seats_test_off": ("braindb_index.py", "            if seat_rows.get(k) is False:\n", "            if False:\n"),
 "C_M7_tier_always_ok": ("braindb_index.py", "    t = (tier or \"\").strip().strip(\"\\\"'\").strip()\n    if not t:\n", "    return True, 'mutant'\n    t = ''\n    if not t:\n"),
 "C_M13_seat_word_off": ("braindb_index.py", "            hit = next((x for x in sc[\"deny_seat_word\"] if x in dlow or (not name_exempt and x in nlow)), None)\n", "            hit = None\n"),
 # --- new
 "N01_second_block_fault_off": ("braindb_index.py", "            faults.append(\"a second frontmatter block follows the first\")\n", "            pass\n"),
 "N02_stray_tier_scan_off": ("braindb_index.py", "    for line in lines[start:start + 60]:\n", "    for line in lines[start:start]:\n"),
 "N03_unclosed_fault_off": ("braindb_index.py", "            faults.append(\"the frontmatter is not closed\")\n", "            pass\n"),
 "N04_tierline_no_value_fault_off": ("braindb_index.py", "    if tier_lines >= 1 and not fm.get(\"tier\"):\n", "    if False:\n"),
 "N05_deny_client_off": ("braindb_index.py", "        if c in low:\n            return False, \"tier '%s' names %s\" % (t, c)\n", "        if False:\n            return False, \"tier '%s' names %s\" % (t, c)\n"),
 "N06_ledger_only_by_allow_ledger_off": ("braindb_index.py", "            if kind != \"ledger\" and nlow.startswith(\"_ledger\"):\n", "            if False:\n"),
 "N07_daily_folder_only_by_allow_daily_off": ("braindb_index.py", "            if kind != \"daily\" and os.path.basename(dlow).startswith(\"daily\"):\n", "            if False:\n"),
 "N08_search_any_server": ("braindb_index.py", "    need_server()\n    ensure_index(root, sc, seat)\n    words = ", "    ensure_index(root, sc, seat)\n    words = "),
 "N09_at_any_server": ("braindb_index.py", "    need_server()\n    ensure_index(root, sc, seat)\n    if not re.fullmatch", "    ensure_index(root, sc, seat)\n    if not re.fullmatch"),
 "N10_status_info_any_server": ("braindb_index.py", "    need_server()                                   # refuses (rc 4) when another cluster answers on this socket\n", "    pass\n"),
 "N11_rebuild_lock_off": ("braindb_index.py", "    lock_fd = None if lock_held else take_lock()\n", "    lock_fd = None\n"),
 "N12_running_ignores_pidfile_dir": ("braindb.sh", "  [ \"$PF_DIR\" = \"$PGDATA\" ] || return 1\n  pid_alive \"$PF_PID\" || return 1\n", "  pid_alive \"$PF_PID\" || return 1\n"),
 "N13_stop_ignores_pidfile_dir": ("braindb.sh", "  if [ \"$PF_DIR\" != \"$PGDATA\" ]; then\n    echo \"braindb: REFUSED: $PIDFILE names", "  if false; then\n    echo \"braindb: REFUSED: $PIDFILE names"),
 "N14_sockdir_mode_unchecked": ("braindb.sh", "  [ \"$(stat -f '%Lp' \"$SOCKDIR\")\" = \"700\" ] || die", "  true || die"),
 "N15_sockdir_symlink_allowed": ("braindb.sh", "  [ ! -L \"$SOCKDIR\" ] || die", "  true || die"),
 "N16_doctor_rc4_not_named": ("braindb.sh", "    4) echo \"WARN brain-db: ANOTHER cluster is answering", "    44) echo \"WARN brain-db: ANOTHER cluster is answering"),
 "N17_done_with_faults_never": ("braindb_index.py", "    if nu or nt:\n        print(\"rebuild: DONE WITH FAULTS", "    if False:\n        print(\"rebuild: DONE WITH FAULTS"),
 "N18_check_ignores_indexer_change": ("braindb_index.py", "    if meta.get(\"indexer_sha256\") != idx_sha:\n", "    if False:\n"),
 "N19_untagged_not_listed": ("braindb_index.py", "                untagged.append(rel)\n", "                pass\n"),
 "N20_failclosed_names_sampled": ("braindb_index.py", "            full = key.startswith((\"tier cannot\", \"a damaged\", \"unreadable\", \"hard link\", \"unknown tier\", \"project tier\", \"tier names\"))\n", "            full = False\n"),
 "N21_restart_retest_off": ("braindb.sh", "    if running; then\n      echo \"start: already running (pid $PF_PID, $PGDATA; started by another command meanwhile)\"; return 0\n    fi\n", ""),
 "N22_lesson_name_any": ("braindb_index.py", "            if kind == \"lesson\" and not LESSON_NAME.fullmatch(name):\n", "            if False:\n"),
 "N23_no_autostart_ignored": ("braindb.sh", "  [ \"${BRAINDB_NO_AUTOSTART:-}\" = \"1\" ] && return 0\n", ""),
 "N24_check_scope_change_ignored": ("braindb_index.py", "    if meta.get(\"scope_sha256\") != scope_sha:\n", "    if False:\n"),
 "N25_foreign_guard_dir_branch_off": ("braindb.sh", "  read_pidfile || return 0\n  if [ \"$PF_DIR\" != \"$PGDATA\" ]; then\n", "  read_pidfile || return 0\n  if false; then\n"),
 "N26_marker_no_heading_keeps": ("braindb_index.py", "            end = next((h for h in heads if h > k), len(lines))\n", "            end = k + 1\n"),
 "N27_hard_deny_segment_off": ("braindb_index.py", "    if any(s in HARD_DENY_SEGMENT for s in low.split(\"/\")):\n", "    if False:\n"),
 "N28_chat_refusal_off": ("braindb_index.py", "    if pat.lower().startswith(\"chat_\"):\n", "    if False:\n"),
 "N29_truncated_not_counted_in_check": ("braindb_index.py", "len(res[\"unreadable\"]), last.get(\"unreadable\", \"?\"), last.get(\"truncated\", \"?\"))", "0, 0, 0)"),
 "N30_scope_seat_mismatch_allowed": ("braindb_index.py", "    if sc[\"seat\"] != seat:\n", "    if False:\n"),
}
name = sys.argv[1]
if name == "--list":
    print(" ".join(M)); sys.exit(0)
pf, dst = sys.argv[2], sys.argv[3]
t = os.path.join(dst, "WEDNESDAY", "2_Project_Files")
shutil.copytree(pf, t, ignore=shutil.ignore_patterns("__pycache__", "evidence"))
if M[name] is None:
    sys.exit(0)
f, old, new = M[name]
p = os.path.join(t, "brain-db", f)
s = open(p, encoding="utf-8").read()
if s.count(old) != 1:
    sys.exit("ANCHOR for %s found %d times in %s, need exactly 1" % (name, s.count(old), f))
open(p, "w", encoding="utf-8").write(s.replace(old, new))
