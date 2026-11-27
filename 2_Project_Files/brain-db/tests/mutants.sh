#!/bin/bash
# tests/mutants.sh <scratch directory> [mutant name ...] - proof that the suite can fail.
# For each mutant: copy this lane into <scratch>/mut-.../WEDNESDAY/2_Project_Files/brain-db (with the seat
# resolver and seat_note.sh), BREAK ONE THING in the copy, run the copy's own tests/run.sh, and require
# at least one FAIL line that matches the assertion the broken thing is meant to trip. The lane itself is
# never modified. "none" is the control: the unmutated copy must pass with 0 failures.
# Runs up to 4 mutants at a time (each run has its own directories and socket directories).
set -u
SCR="${1:-}"; [ -n "$SCR" ] && [ -d "$SCR" ] || { echo "usage: mutants.sh <scratch directory> [mutant ...]" >&2; exit 2; }
shift
PY="${BRAINDB_PYTHON:-python3}"
SELF="${BASH_SOURCE[0]}"; case "$SELF" in /*) ;; *) SELF="$PWD/$SELF" ;; esac
TESTS="$("$PY" -c 'import os,sys; print(os.path.dirname(os.path.realpath(sys.argv[1])))' "$SELF")"
LANE="$(dirname "$TESTS")"; PF="$(dirname "$LANE")"
OUT="$SCR/mutants-$(date +%Y%m%d-%H%M%S)-$$"; mkdir -p "$OUT" || exit 2

cat > "$OUT/mutate.py" <<'PY'
import sys, os, shutil
name, lane, pf, dst = sys.argv[1:5]
# name: (file, old text that must occur exactly once, new text, regex one FAIL line must match, what was broken)
I, B = "braindb_index.py", "braindb.sh"
M = {
 "none": None,
 # ---- ROUND 4: one or more mutants per clause of the qualify rule; each lets an UNQUALIFIED lesson in
 "Qa_no_row_qualifies": (I, "    plain = [r for r in mine if r[\"n\"] == 1]\n", "    plain = [r for r in mine if r[\"n\"] == 1] or [dict(seats=[ALL_SEATS])]\n",
     "xcanary301", "(a) a lesson with no row qualifies on its tier alone, as in round 3"),
 "Qa_unread_lines_ignored": (I, "        if stem in bad:\n", "        if False:\n",
     "xcanary315|xcanary319|xcanary320", "(a) a rules-index line that could not be read no longer leaves out the lesson it names"),
 "Qa_duplicate_rows_ok": (I, "    if len(plain) != 1:\n", "    if len(plain) < 1:\n",
     "xcanary316|xcanary331|clauses differ", "(a) two rows with the same key are accepted"),
 "Qa_duplicate_hash_rows_ok": (I, "    if len(ns) != len(set(ns)):\n", "    if False:\n",
     "xcanary317", "(a) the same '#n' key twice is accepted"),
 "Qa_seats_cell_loose": (I, "                and (seats == [ALL_SEATS] or all(x in SEATS for x in seats))):\n", "                ):\n",
     "xcanary328", "(a) a seats cell is no longer held to the spec's words"),
 "Qa_key_any_shape": (I, "        m = ROW_KEY.fullmatch(f[0]) if ok else None\n", "        m = re.fullmatch(r\"(.*?)(?:#(\\d+))?\", f[0].strip().rsplit(\"/\", 1)[-1]) if len(f) == 7 else None\n",
     "xcanary315|xcanary3(05|06|14)", "(a) a key need no longer be exactly the file name (paths, outer spaces and #1 accepted)"),
 "Qb_seat_not_tested": (I, "    if not (ALL_SEATS in seats or sc[\"seat\"] in seats):\n", "    if False:\n",
     "xcanary03|xcanary17|xcanary401", "(b) the row's seats cell is not tested"),
 "Qb_any_row_counts": (I, "    seats = plain[0][\"seats\"]\n", "    seats = [x for r in mine for x in r[\"seats\"]]\n",
     "xcanary402", "(b) a '#n' row naming this seat is enough although the plain row names another"),
 "Qb_other_seat_rule_line_in": (I, "                           and (ALL_SEATS in r[\"seats\"] or sc[\"seat\"] in r[\"seats\"])]\n", "                           ]\n",
     "xcanary405ruletwo", "(b) a rule line scoped to another seat enters with an indexed lesson"),
 "Qc_any_tier": (I, "    if not allowed_tier(tier, sc):\n", "    if False:\n",
     "xcanary08|xcanary502|xcanary504", "(c) any tier value is accepted"),
 "Qc_no_tier_is_W": (I, "    if tier is None:\n        return \"c\", \"no tier line in the frontmatter\"\n", "    if tier is None:\n        tier = \"W\"\n",
     "xcanary501", "(c) a lesson with no tier is treated as W, as in round 3"),
 "Qc_line1_loose": (I, "    if lines[0] != \"---\":\n", "    while len(lines) > 1 and not lines[0].strip():\n        lines.pop(0)\n    if lines[0].strip() != \"---\":\n",
     "xcanary533|xcanary534|xcanary535", "(c) the frontmatter need not open on line 1 with exactly ---"),
 "Qc_odd_lines_skipped": (I, "        if not m:\n            return \"c\", \"frontmatter line %d is not a plain 'key: value' line\" % (i + 1)\n", "        if not m:\n            continue\n",
     "xcanary5(12|13|14|15|16|17|23|24|28)|clauses differ", "(c) a frontmatter line that is not a plain key: value line is skipped, not refused"),
 "Qc_dup_key_ok": (I, "        if k in seen:\n", "        if False:\n",
     "xcanary520|xcanary521", "(c) tier given twice is accepted (the last one wins)"),
 "Qc_keylike_ok": (I, "        elif \"tier\" in fold_key(k):\n", "        elif False:\n",
     "xcanary518|xcanary519", "(c) a second key that folds to tier (tiers:, tier_project:) is accepted"),
 "Qc_value_tierlike_ok": (I, "        elif TIER_ASSIGN.search(fold(v)) or TIER_LINE_START.search(fold(v)):\n", "        elif False:\n",
     "clauses differ", "(c) a tier assignment inside another key's value is not refused by (c) (clause (d) still catches it: the clause table goes red)"),
 "Qc_second_block_ok": (I, "    if nxt.lstrip().startswith(\"---\") or nxt.lstrip().startswith(\"+++\"):\n", "    if False:\n",
     "clauses differ", "(c) a second frontmatter block is not refused by (c) (clause (d) still catches its tier line: the clause table goes red)"),
 "Qc_closed_list_loose": (I, "    return bool(m) and m.group(1).casefold() in sc[\"own\"]\n", "    return bool(m) or (value or \"\").strip().strip(\"\\\"'[]\").upper() in (\"W\", \"M\")\n",
     "xcanary504|xcanary507|xcanary508|xcanary510", "(c) the tier list is not closed: any P- client, and W in other spellings"),
 "Qd_comment_ok": (I, "    if \"<!--\" in text or \"-->\" in text:\n", "    if False:\n",
     "xcanary706|xcanary707|xcanary708", "(d) an HTML comment no longer leaves the lesson out"),
 "Qd_tierlike_line_ok": (I, "        if TIER_LINE_START.search(f) or TIER_ASSIGN.search(f):\n", "        if False:\n",
     "xcanary709|xcanary710|xcanary711|xcanary712|xcanary713|xcanary714", "(d) a tier-like line in the body no longer leaves the lesson out"),
 "Qd_entity_ok": (I, "    if \"&#\" in text:\n", "    if False:\n",
     "xcanary715", "(d) a numeric character reference is accepted"),
 "Qd_name_test_put_back": (I, "    if \"&#\" in text:\n", "    if \"datasec\" in fold(text) or \"datasec\" in fold(name) or any(\"datasec\" in fold(r[\"raw\"]) for r in mine):\n        return \"d\", \"it names another client\"\n    if \"&#\" in text:\n",
     "present xneighbour74|present xneighbour75", "(4b) the client-name test is put back: this seat's own lessons that name the other client drop out"),
 "Qt_any_bytes": (I, "    except UnicodeDecodeError:\n        return None, \"the file is not valid UTF-8\"\n", "    except UnicodeDecodeError:\n        text = raw.decode(\"utf-8\", errors=\"replace\")\n",
     "xcanary801|xcanary817", "(t) a file that is not valid UTF-8 is read anyway"),
 "Qt_controls_ok": (I, "        if cat in (\"Cc\", \"Cf\", \"Zl\", \"Zp\", \"Cs\", \"Co\", \"Cn\"):\n", "        if False:\n",
     "xcanary803|xcanary816", "(t) control and format characters are accepted"),
 "Qt_letters_ok": (I, "            if not base or any(ord(x) > 127 or not x.isalpha() for x in base):\n", "            if False:\n",
     "xcanary812|xcanary814|xcanary815", "(t) look-alike letters of other scripts are accepted"),
 "Qf_hard_link_through": (I, "        if st.st_nlink != 1:\n", "        if False:\n",
     "xcanary680", "(f) a hard link is read"),
 "Qf_symlink_followed": (I, "os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK |", "os.O_RDONLY | os.O_NONBLOCK |",
     "xcanary15|xcanary681|4_Credentials text entered|  rebuild \\(rc 5, wanted 0\\)", "(f, N6) files are opened following symlinks (round 5: the snapshot check now refuses EVERY rebuild under this mutant, rc 5, because a file read through a symlink is not the file its name stats as; nothing is indexed at all, so the old token assertions cannot fire)"),
 "no_index_not_refused": (I, "    if wants_lessons and (idx[\"fatal\"] or not idx[\"rows\"]):\n", "    if False:\n",
     "rules index missing is refused|no row is refused|SYMLINK is refused", "a missing or unusable rules index no longer refuses the rebuild"),
 "builtin_deny_path_off": (I, "BUILTIN_DENY_PATH = (\"(conflict_on_\", \".pre-\")", "BUILTIN_DENY_PATH = ()",
     "sync copies and backups stay out", "sync copies and backups are held out by the scope file's lines only"),
 "daily_name_any": (I, "                if kind == \"daily\" and not DAILY_NAME.fullmatch(name):\n", "                if False:\n",
     "xcanary69[0-3]", "a daily note need no longer be named as a plain date"),
 "underscore_names_through": (I, "                if kind not in (\"ledger\", \"rules_index\") and name.lower().startswith(\"_\"):\n", "                if False:\n",
     "xcanary43|ledger-named skill|never a skill", "a file named _ledger* is taken as a skill"),
 # ---- N5, N7: the closed table and the scope checked first
 "N5_names_not_closed": (I, "        if pat not in names:\n", "        if False:\n",
     "NOT refused: allow (ledger|pickup)|TUESDAY tree: 'allow ledger", "(N5, checker's N06) a ledger or pickup line may name any file in the folder"),
 "N5_folders_not_closed": (I, "    if d != want_dir:\n", "    if False:\n",
     "NOT refused: allow (daily|skill|lesson)|tree: 'allow daily", "(N5, checker's N07) a kind may be indexed from any folder"),
 "N5_rules_not_closed": (I, "        if glob_ not in ROOT_RULES:\n", "        if False:\n",
     "NOT refused: allow rules", "(N5) any file may be allowed as kind rules"),
 "N7_scope_validated_late": (B, "  need_scope_file\n  indexer validate || exit 2\n", "  need_scope_file\n",
     "cluster dir CREATED|tree: 'allow", "(N7) a scope file that exists is validated only after the cluster is created and started"),
 "F4_scope_checked_late": (B, "           need_scope; find_pgbin; ensure_up || exit 1; indexer \"$@\" ;;\n", "           find_pgbin; ensure_up || exit 1; indexer \"$@\" ;;\n",
     "created a cluster directory|cluster dir created|cluster dir CREATED|left a server running", "the scope file is tested after the cluster is created and started"),
 # ---- N3: the right database inside the same session
 "N3_no_assert_in_load": (I, "        w(\"BEGIN;\\n\" + ASSERT_SQL)\n", "        w(\"BEGIN;\\n\")\n",
     "INSIDE the load transaction|t2's index is untouched|t2 was written", "(N3) the load transaction no longer asserts the data directory"),
 "N3_no_assert_in_reads": (I, "    full = (\"BEGIN;\\n\" if txn else \"\") + ASSERT_SQL + sql", "    full = (\"BEGIN;\\n\" if txn else \"\") + sql",
     "addressed to c2|refused in its own session|REFUSED with rc 4|exits 4", "(N3, checker's N10) read sessions no longer assert the data directory"),
 "N3_assert_always_true": (I, "  IF current_setting('data_directory') IS DISTINCT FROM current_setting('braindb.want_dd') THEN\n", "  IF false THEN\n",
     "REFUSED with rc 4|INSIDE the load transaction", "(N3) the assertion compares nothing"),
 # ---- N9 to N15, N24, N8
 "N9_rules_row_after_the_cut": (I, "    SELECT id, score, grp FROM grouped WHERE rn <= :lim OR (lead AND rn_lead <= :lim)\n", "    SELECT id, score, grp FROM grouped WHERE rn <= :lim\n",
     "q1: result 1 is not the rules row|q3: result 1 is not the rules row", "(N9) the rules row is chosen after the top-N cut again"),
 "N10_no_realpath": (B, "PGDATA=\"$(\"$PY\" -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' \"$PGDATA\")\" || die \"cannot resolve the data directory path\"\n", "",
     "trailing slash|doubled slash|through a symlink", "(N10) the data directory is used as spelled"),
 "N11_status_rc0": (B, "indexer info; return $?; fi", "indexer info; return 0; fi",
     "exits 4, not 0", "(N11) status exits 0 whatever its indexer part printed"),
 "N11_down_is_rc4": (I, "        if on_down == \"die\":\n            die(\"the index server is not answering on %s (run: braindb.sh start)%s\" % (env(\"BRAINDB_SOCKDIR_EFF\"), DOWN_SUFFIX), 3)\n", "        if on_down == \"die\":\n            die(\"REFUSED: the server serves data directory '(unknown)'\", 4)\n",
     "rc 3|not answering", "(N11) an empty answer is reported as another cluster"),
 "N13_no_rebuild_lock": (I, "    lock_fd = None if lock_held else take_lock()\n", "    lock_fd = None\n",
     "rebuild behind a lock holder waits|gives up at its limit", "(N13, checker's N11) a rebuild no longer takes the cluster lock"),
 "N13_lock_wait_unbounded": (I, "            if time.time() > deadline:\n                print(\"braindb: another braindb command has held %s for more than %.0f s; nothing was done\" % (path, wait_s),\n                      file=sys.stderr)\n                sys.exit(75)\n", "            pass\n",
     "gives up at its limit", "(N13) the indexer's lock wait has no limit and says nothing"),
 "N14_sock_mode_untested": (B, "  [ \"$(stat -f '%Lp' \"$SOCKDIR\")\" = \"700\" ] || die \"REFUSED: $SOCKDIR is not mode 700 (it is $(stat -f '%Lp' \"$SOCKDIR\"))\"\n", "",
     "not mode 700 is refused|for its MODE", "(N14) the socket directory's mode is not tested"),
 "N15_sock_symlink_ok": (B, "  [ ! -L \"$SOCKDIR\" ] || die \"REFUSED: the socket directory $SOCKDIR is a symlink\"\n", "",
     "symlink is refused|no 'is a symlink'", "(N15) a symlinked socket directory is accepted"),
 "N24_scope_change_unseen": (I, "    if meta.get(\"scope_sha256\") != scope_sha:\n", "    if False:\n",
     "differs only by a comment line", "(N24) check does not notice a changed scope file"),
 "N8_left_out_not_shown": (I, "        print(\"  left out: \" + left_out_line(res))\n", "",
     "check prints the same count|doctor's one line", "(N8) check and doctor no longer print what was left out"),
 "N8_last_line_silent": (I, "    tail = left_out_line(sc_res)\n", "    tail = \"\"\n",
     "LAST line gives the count", "(N8) the rebuild's last line no longer counts what was left out"),
 # ---- ROUND 5, F1: one snapshot. Each lets text of one moment be paired with a row of another, or hides a refusal
 "F1_no_validation": (I, "        moved = snapshot_moved(out, held, attempt)\n", "        moved = []\n",
     "F1\\.1 the OTHER text", "(F1) the read is not validated at all, as in round 4b"),
 "F1_lessons_not_restatted": (I, "                if now != stamp(st):\n", "                if False:\n",
     "F1\\.2 the OTHER text", "(F1) only the rules index is hashed again; the lessons are not stat-ed again (the verdict's 'hash alone', A, B, A)"),
 "F1_index_not_rehashed": (I, "                if again != hashlib.sha256(out[rel][1]).digest():\n", "                if False:\n",
     "F1\\.3 the OTHER text", "(F1) the rules index is not hashed again"),
 "F1_validate_order_swapped": (I, "VALIDATE_ORDER = (\"rules_index\", \"lesson\")\n", "VALIDATE_ORDER = (\"lesson\", \"rules_index\")\n",
     "F1\\.4 the OTHER text", "(F1) the lessons are stat-ed again BEFORE the index is hashed again"),
 "F1_stamp_inode_only": (I, "    return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)\n", "    return (st.st_dev, st.st_ino)\n",
     "F1\\.5 the OTHER text", "(F1) a lesson is 'the same' when it is the same inode: a rewrite in place is not seen"),
 "F1_stamp_no_ctime": (I, "    return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)\n", "    return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns)\n",
     "F1\\.5 the OTHER text", "(F1) inode, size and modification time only, as the verdict's fix was worded: a rewrite in place that puts the time back is not seen"),
 "F1_torn_read_accepted_at_the_end": (I, "    die(\"REFUSED: the tree changed while it was read; nothing was changed in the index.", "    return judge_snapshot(root, sc, want_text, listed, skipped0)\n    die(\"REFUSED: the tree changed while it was read; nothing was changed in the index.",
     "F1\\.6 the lesson replaced under each of three reads", "(F1) after three tries the last, torn, read is used instead of refusing"),
 "F1_single_try": (I, "SNAPSHOT_TRIES = 3\n", "SNAPSHOT_TRIES = 1\n",
     "F1\\.1 the lesson read in state B", "(F1) no second read: one moved file refuses the rebuild at once"),
 "F1_fourth_try": (I, "SNAPSHOT_TRIES = 3\n", "SNAPSHOT_TRIES = 4\n",
     "F1\\.6 .*three", "(F1) a fourth try: not 'at most three'"),
 # ---- ROUND 5, F2: no GREEN, done or OK over a gap
 "F2_check_green_over_gaps": (I, "    if not diffs and not stale and n_gaps:\n", "    if False:\n",
     "F2 g1: check", "(F2) check says GREEN, rc 0, while files that matched the allow-list are not indexed, as in round 4b"),
 "F2_amber_exits_0": (I, "        return CHECK_GAPS_RC\n", "        return 0\n",
     "F2 g1: check", "(F2) check says AMBER but exits 0"),
 "F2_not_plain_uncounted": (I, "        return \"L\"\n", "        return None\n",
     "F2 g1: ", "(F2) a symlink, a hard link or another non-plain file is not counted"),
 "F2_unreadable_uncounted": (I, "        return \"U\"\n", "        return None\n",
     "F2 g4: ", "(F2) an unreadable file or folder is not counted"),
 "F2_cut_uncounted": (I, "    cut_files = len(set(rel for rel, _, _, _ in truncated))        # F2: files with at least one row cut\n", "    cut_files = 0\n",
     "F2 g5: |F2 9b: ", "(F2) a cut row is not counted"),
 "F2_rebuild_done_over_gaps": (I, "    if nu or nt or sc_res[\"gap_u\"] + sc_res[\"gap_l\"] + cut_files + sc_res[\"gap_f\"]:\n", "    if nu or nt:\n",
     "F2 g1: rebuild", "(F2) the rebuild's last line says 'done' over a skipped symlink, as in round 4b"),
 # ---- ROUND 5b: a lesson that cannot be read as a plain file is a gap; a lesson left out by the rule is not
 "F2b_lesson_faults_uncounted": (I, "                gap_f=sum(1 for _, clause, _ in left_out if clause == \"f\"),", "                gap_f=0,",
     "F2 l1: |F2 5b: check after the first rebuild", "(5b) an unreadable or non-plain LESSON is not counted, as in round 5"),
 "F2b_check_green_over_lesson_fault": (I, "    n_gaps = gap_u + gap_l + (gap_c or 0) + gap_f\n", "    n_gaps = gap_u + gap_l + (gap_c or 0)\n",
     "F2 l1: check", "(5b) check counts the lesson on its line but still says GREEN, rc 0"),
 "F2b_rebuild_done_over_lesson_fault": (I, " + cut_files + sc_res[\"gap_f\"]:\n", " + cut_files:\n",
     "F2 l2: rebuild", "(5b) the rebuild's last line says 'done' over a lesson that is a symlink"),
 "F2b_doctor_stopped_ok_over_lesson_fault": (B, "         \"0 other file(s)\"*\", and 0 lesson file(s)\"*) echo", "         \"0 other file(s)\"*) echo",
     "F2 l1s: ", "(5b) with the server stopped doctor says OK when only a lesson is unreadable"),
 "F2b_rule_leftouts_are_gaps": (I, "                gap_f=sum(1 for _, clause, _ in left_out if clause == \"f\"),", "                gap_f=len(left_out),",
     "F2 5b MUST STAY GREEN", "(5b) every left-out lesson is counted as a gap: the rule at work turns check AMBER"),
 "F2_doctor_ok_over_gaps": (B, "    6) echo \"WARN brain-db: index current but it has GAPS, ", "    6) echo \"OK brain-db: index current, ",
     "F2 g1: doctor", "(F2) doctor says OK over a gap"),
 "F2_doctor_rc0_over_gaps": (B, "then braindb.sh rebuild (${first#check: }); $lo\"; return 1 ;;\n", "then braindb.sh rebuild (${first#check: }); $lo\"; return 0 ;;\n",
     "F2 g1: doctor", "(F2) doctor prints WARN over a gap but exits 0"),
 "F2_doctor_stopped_ok": (B, "         *) echo \"WARN brain-db: server stopped, and $gap, ", "         *) echo \"OK brain-db: server stopped, and $gap, ",
     "F2 g7: ", "(F2) with the server stopped doctor says OK over the gaps it can count"),
 "F2_up_rc0_over_gaps": (B, "  case \"$rc\" in 0|6) return \"$rc\" ;; esac", "  case \"$rc\" in 0|6) return 0 ;; esac",
     "F2 g1: up", "(F2) up exits 0 over a gap, so a launcher block would print its check line as success"),
 # ---- ROUND 5, F4 and K18
 "F4_init_unscoped": (B, "  init)    need_scope; locked __init ;;", "  init)    locked __init ;;",
     "'init'", "(F4) init does not validate the scope first, as in round 4b"),
 "F4_start_unscoped": (B, "  start)   need_scope; locked __start ;;", "  start)   locked __start ;;",
     "'start'", "(F4) start does not validate the scope first, as in round 4b"),
 "F4_stop_makes_a_lock_file": (B, "           if [ ! -e \"$PGDATA\" ] && [ ! -L \"$PGDATA\" ]; then echo \"stop: not running (no cluster at $PGDATA)\"; exit 0; fi\n", "",
     "'stop'", "(F4) stop takes the lock, and so creates the lock file, where no cluster exists (the last line of the checker's DB12 and M2)"),
 "K18_nonzero_psql_is_done": (I, "    if rc != 0:\n        die(\"REBUILD FAILED (psql rc %d). The transaction was rolled back; the previous index, if any, is unchanged.\" % rc, 1)\n", "",
     "K18 ", "(K18, the third checker's surviving mutant) a rebuild whose psql session FAILED still prints 'rebuild: done' and exits 0"),
 # ---- kept from round 3
 "F5_no_lock": (B, "locked() { \"$PY\" \"$LANE/braindb_lock.py\" \"$LOCKFILE\" \"${BRAINDB_LOCK_WAIT:-150}\" /bin/bash \"$SELF\" \"$@\"; }\n", "locked() { /bin/bash \"$SELF\" \"$@\"; }\n",
     "double init|two starts|two self-starting|NO cluster at all|stop behind the same holder", "init, start and stop are no longer serialised by the lock"),
 "F6_stale_pid_unexplained": (B, "  foreign_pidfile_guard\n  check_sockdir\n", "  check_sockdir\n",
     "STALE PID FILE|recovery", "start no longer explains a pid file that names a live foreign process"),
 "F7_unreadable_aborts": (I, "                except OSError as e:\n                    skipped.append((rel, \"unreadable: %s\" % type(e).__name__))\n", "                except ZeroDivisionError as e:\n                    skipped.append((rel, \"unreadable: %s\" % type(e).__name__))\n",
     "unreadable lesson|traceback|unreadable file is listed", "an unreadable file is no longer caught"),
 "F7_row_not_capped": (I, "        if v is None or len(v) <= limit:\n", "        if True:\n",
     "3 MB section|truncated row", "an over-long row is no longer truncated"),
 "F8_separators_kept": (I, "STRIP_BYTES = {0x00: None, 0x1e: None, 0x1f: None}", "STRIP_BYTES = {0x00: None}",
     "separator bytes", "the two separator bytes are no longer stripped on read"),
 "F9_stop_trusts_pidfile": (B, "  case \"$cmd \" in *\" -D $PGDATA \"*) return 0 ;; esac\n  return 1\n", "  return 0\n",
     "foreign process was killed", "the first checker's M2: stop signals whatever the pid file names"),
 "rules_row_always_first": (I, "    first = [r for r in know if r[1] == \"rules\" and holds_all(r)]\n    rest = [r for r in know if not (r[1] == \"rules\" and holds_all(r))]\n", "    first = [r for r in know if r[1] == \"rules\"]\n    rest = [r for r in know if r[1] != \"rules\"]\n",
     "result 1 is not the lesson", "a rules-file row is put first whatever it matched"),
 "lessons_first_off": (I, "    if mode != \"default\":\n", "    if True:\n",
     "the lesson is result 1 although ledger rows score higher|incident rows follow", "the default order is the old mixed one"),
 "seat_follows_WED_AGENT": (B, "  seat_note_dir \"$CODE_ROOT\" braindb || exit 2\n  SEAT=\"$SEAT_NOTE_SEAT\"\n  DAILY_REL=\"$SEAT_NOTE_REL\"\n", "  . \"$RESOLVER\"; seat_resolve \"$CODE_ROOT\"\n  DAILY_REL=\"\"\n",
     "WED_AGENT=tuesday on a tree named WEDNESDAY is refused with rc 2|not WEDNESDAY, TUESDAY or FRIDAY is refused with rc 2", "the seat follows WED_AGENT and an unknown tree defaults to wednesday"),
}
if name == "--list":
    print(" ".join(M)); sys.exit(0)
t = os.path.join(dst, "WEDNESDAY", "2_Project_Files")
os.makedirs(os.path.join(t, "fleet", "cockpit")); os.makedirs(os.path.join(t, "tools"))
shutil.copytree(lane, os.path.join(t, "brain-db"),
                ignore=shutil.ignore_patterns("pgdata-*", "_quarantine_*", "_probe_*", "__pycache__", "evidence", "*.lock"))
shutil.copy2(os.path.join(pf, "fleet", "cockpit", "seat_resolve.sh"), os.path.join(t, "fleet", "cockpit"))
if os.path.isfile(os.path.join(pf, "tools", "seat_note.sh")):
    shutil.copy2(os.path.join(pf, "tools", "seat_note.sh"), os.path.join(t, "tools"))
if M[name] is None:
    open(os.path.join(dst, "EXPECT"), "w").write("\n"); open(os.path.join(dst, "WHAT"), "w").write("nothing (control)\n")
    sys.exit(0)
f, old, new, expect, what = M[name]
p = os.path.join(t, "brain-db", f)
s = open(p, encoding="utf-8").read()
if s.count(old) != 1:
    sys.exit("mutation anchor for %s found %d times in %s, need exactly 1" % (name, s.count(old), f))
open(p, "w", encoding="utf-8").write(s.replace(old, new))
open(os.path.join(dst, "EXPECT"), "w").write(expect + "\n"); open(os.path.join(dst, "WHAT"), "w").write(what + "\n")
PY

if [ "$#" -gt 0 ]; then NAMES="$*"; else NAMES="$("$PY" "$OUT/mutate.py" --list x x x)"; fi
one() { # run one mutant; writes $OUT/<name>/verdict
  local n="$1" d="$OUT/$1"
  mkdir -p "$d/scr" || return 1
  if ! "$PY" "$OUT/mutate.py" "$n" "$LANE" "$PF" "$d" > "$d/mutate.out" 2>&1; then echo "SETUP-ERROR $(tail -1 "$d/mutate.out")" > "$d/verdict"; return 0; fi
  /bin/bash "$d/WEDNESDAY/2_Project_Files/brain-db/tests/run.sh" "$d/scr" > "$d/suite.log" 2>&1
  local rc=$? nf np hit
  nf="$(/usr/bin/grep -i -F -c '  FAIL  ' "$d/suite.log")"; np="$(/usr/bin/grep -i -F -c '  PASS  ' "$d/suite.log")"
  if [ "$n" = "none" ]; then
    if [ "$rc" -eq 0 ] && [ "$nf" = "0" ]; then echo "CONTROL-OK  $np passed, 0 failed" > "$d/verdict"; else echo "CONTROL-BROKEN  $np passed, $nf failed (rc $rc)" > "$d/verdict"; fi
    return 0
  fi
  hit="$(/usr/bin/grep -i -F '  FAIL  ' "$d/suite.log" | /usr/bin/grep -i -E -c -- "$(cat "$d/EXPECT")")"
  if [ "$hit" != "0" ]; then echo "CAUGHT  $nf failing line(s), $hit on the expected assertion  [$(/usr/bin/grep -i -F '  FAIL  ' "$d/suite.log" | /usr/bin/grep -i -E -- "$(cat "$d/EXPECT")" | head -1 | cut -c9-150)]" > "$d/verdict"
  elif [ "$nf" != "0" ]; then echo "RED-ELSEWHERE  $nf failing line(s), none on the expected assertion /$(cat "$d/EXPECT")/" > "$d/verdict"
  else echo "SURVIVED  the suite passed ($np) with this broken" > "$d/verdict"; fi
}
echo "mutants: output $OUT ; $(date '+%Y-%m-%d %H:%M:%S %Z')"
running=0
for n in $NAMES; do
  one "$n" &
  running=$((running+1))
  if [ "$running" -ge 4 ]; then wait; running=0; fi
done
wait
caught=0; total=0; other=0
for n in $NAMES; do
  v="$(cat "$OUT/$n/verdict" 2>&1)"
  printf '%-30s %s\n' "$n" "$v"
  printf '%-30s   broke: %s\n' "" "$(cat "$OUT/$n/WHAT" 2>&1)"
  case "$n" in none) ;; *) total=$((total+1)); case "$v" in CAUGHT*) caught=$((caught+1)) ;; *) other=$((other+1)) ;; esac ;; esac
done
snap="$(ps -axww -o pid=,command=)"; echo "server processes left under $OUT: $(printf '%s\n' "$snap" | /usr/bin/grep -F -c -- "-D $OUT")"
echo "finished $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "MUTANTS: $caught of $total caught on the expected assertion; $other not"
[ "$other" -eq 0 ]
