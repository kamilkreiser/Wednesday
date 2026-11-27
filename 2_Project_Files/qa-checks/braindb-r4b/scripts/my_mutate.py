#!/usr/bin/env python3
"""my_mutate.py <name|--list> <scratch lane copy> <its 2_Project_Files> <dst> - the third checker's own mutants.
Each breaks ONE thing in a copy of the scratch lane copy (never the lane). expect = what I predicted BEFORE running:
'caught' or 'survive' (a predicted survivor is a claim with no test that can fail)."""
import sys, os, shutil
I, B = "braindb_index.py", "braindb.sh"
M = {
 "none": None,
 "K01_key_case_folded": (I, '    mine = [r for r in idx["rows"] if r["base"] == key]\n', '    mine = [r for r in idx["rows"] if r["base"].casefold() == key.casefold()]\n', "caught", "(a) a key that differs from the file name only in case counts as its row"),
 "K02_unread_line_first_field_only": (I, "        if stem in bad:\n", '        if stem in bad.split("\\t")[0]:\n', "survive", "(a) an unread line leaves a lesson out only when the name is in its FIRST field, not anywhere in it"),
 "K03_comment_lines_skipped": (I, '        if ln == 1 and line.startswith("#"):\n', '        if line.startswith("#"):\n', "caught", "(a) a comment line below line 1 is ignored instead of counting against the lesson it names"),
 "K04_plain_is_first_row": (I, '    plain = [r for r in mine if r["n"] == 1]\n', "    plain = mine[:1]\n", "caught", "(a) a '#n' row alone counts as the lesson's row"),
 "K05_tier_value_stripped": (I, '        if k == "tier":\n            tier = v\n', '        if k == "tier":\n            tier = v.strip()\n', "caught", "(c) outer white space round the tier value is forgiven"),
 "K06_closing_fence_padded": (I, '    try:\n        end = lines.index("---", 1)\n', '    try:\n        end = [l.rstrip() for l in lines].index("---", 1)\n', "survive", "(c) the closing fence may carry trailing white space (not 'exactly ---')"),
 "K07_many_boms": (I, "    for c in set(text):\n", '    text = text.lstrip("\\ufeff")\n    for c in set(text):\n', "survive", "(t) any number of BOMs at the start is accepted (and the returned text then starts at the frontmatter)"),
 "K08_arrow_close_ok": (I, '    if "<!--" in text or "-->" in text:\n', '    if "<!--" in text:\n', "caught", "(d) a stray comment end '-->' no longer leaves the lesson out"),
 "K09_tier_line_exempt_anywhere": (I, '        if i < end and i != 0 and line.startswith("tier:"):\n', '        if line.startswith("tier:"):\n', "caught", "(d) a line 'tier: ...' is excused anywhere, not only the one frontmatter line"),
 "K10_assign_colon_only": (I, '[:=]")', '[:]")', "caught", "(c, d) 'tier = value' is no longer an assignment"),
 "K11_daily_rel_unchecked": (I, "    if daily_rel != SEAT_DAILY[seat]:\n", "    if False:\n", "survive", "(N5) the daily folder from tools/seat_note.sh need not agree with the code's table"),
 "K12_create_db_unasserted": (I, '    full = ("BEGIN;\\n" if txn else "") + ASSERT_SQL + sql', '    full = ("BEGIN;\\n" + ASSERT_SQL if txn else "") + sql', "survive", "(N3) the session that CREATEs the database no longer asserts the data directory"),
 "K13_lesson_name_any": (I, '                if kind == "lesson" and not LESSON_NAME.fullmatch(name):\n', "                if False:\n", "survive", "a file taken as a lesson need not have a lesson's (dated) name"),
 "K14_ledger_names_by_pattern": (I, "        if pat not in names:\n", "        if not any(fnmatch.fnmatchcase(n_, pat) for n_ in names):\n", "caught", "(N5) a ledger or pickup line may be a pattern that matches a table name"),
 "K15_left_out_total_off_by_one": (I, 'dict(total=len(sc_res["left_out"]),', 'dict(total=len(sc_res["left_out"]) - 1,', "caught", "(N8) the stored left-out total (search's NOTE, status) disagrees with the names"),
 "K16_rejected_lines_not_normalised": (I, "            rejected.append((ln, nline))\n", "            rejected.append((ln, line))\n", "survive", "(a) an unread line is compared without NFC and format-character removal"),
 "K17_parent_symlink_unseen": (I, "        if d and os.path.realpath(absd) != os.path.join(rroot, d):\n", "        if d and os.path.islink(absd):\n", "survive", "a table folder is refused only when it is ITSELF a symlink, not when a folder above it is"),
 "K18_nonzero_psql_is_done": (I, "    if rc != 0:\n        die(\"REBUILD FAILED (psql rc %d). The transaction was rolled back; the previous index, if any, is unchanged.\" % rc, 1)\n", "", "survive", "a rebuild whose psql session FAILED still prints 'rebuild: done' and exits 0"),
}
name = sys.argv[1]
if name == "--list":
    print(" ".join(M)); sys.exit(0)
if name == "--expect":
    print(M[sys.argv[2]][3] if M[sys.argv[2]] else "control"); sys.exit(0)
if name == "--what":
    print(M[sys.argv[2]][4] if M[sys.argv[2]] else "nothing (control)"); sys.exit(0)
lane, pf, dst = sys.argv[2:5]
t = os.path.join(dst, "WEDNESDAY", "2_Project_Files")
os.makedirs(os.path.join(t, "fleet", "cockpit")); os.makedirs(os.path.join(t, "tools"))
shutil.copytree(lane, os.path.join(t, "brain-db"), ignore=shutil.ignore_patterns("pgdata-*", "_quarantine_*", "__pycache__", "evidence", "*.lock"))
shutil.copy2(os.path.join(pf, "fleet", "cockpit", "seat_resolve.sh"), os.path.join(t, "fleet", "cockpit"))
shutil.copy2(os.path.join(pf, "tools", "seat_note.sh"), os.path.join(t, "tools"))
if M[name] is None:
    sys.exit(0)
f, old, new, expect, what = M[name]
p = os.path.join(t, "brain-db", f)
s = open(p, encoding="utf-8").read()
if s.count(old) != 1:
    sys.exit("mutation anchor for %s found %d times in %s, need exactly 1" % (name, s.count(old), f))
open(p, "w", encoding="utf-8").write(s.replace(old, new))
