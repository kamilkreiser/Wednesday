#!/usr/bin/env python3
"""derive_repin_gate21T2c.py <gate21T1b repin> <out> — derive repin_and_launch_gate21T2c.sh from the sibling tier-1 kit's (gate21T1b) script by anchored
replacements (every anchor must be present exactly once; a missing one aborts; a leftover sibling token aborts). Kept beside the kit so the derivation is
reproducible. Eight rows with a tier field; #1218 ahead 3, #1223 / #1236 ahead 2; routing QA/Secuura-batch1218."""
import sys
t = open(sys.argv[1], encoding='utf-8').read()
NS = '1218 1219 1223 1233 1235 1236 1237 1238'
R = [
 ("# repin_and_launch_gate21T1b.sh — the LAUNCH ACTION for the round-21 SECOND tier-1 batch gate over #1224 KS-1179, #1226 KS-872, #1228 KS-1171,\n# #1230 KS-1131 (FROZEN at four).",
  "# repin_and_launch_gate21T2c.sh — the LAUNCH ACTION for the round-21 THIRD tier-2 batch gate over #1218 KS-897 (r2), #1219 KS-1277, #1223 KS-1118 (r2),\n# #1233 KS-1133, #1235 KS-1140, #1236 KS-1110, #1237 KS-1229, #1238 KS-1158 (FROZEN at eight)."),
 ("It READS develop and the four heads AT LAUNCH and", "It READS develop and the eight heads AT LAUNCH and"),
 ("# never trusts a pin it did not just re-read (four rows; #1230 is two commits, ahead 2; every head's merge base is the OLD develop 6ab9d5021):",
  "# never trusts a pin it did not just re-read (eight rows; #1218 ahead 3, #1223 / #1236 ahead 2; every head's merge base is the OLD develop 6ab9d5021):"),
 ("#   (0b) the kit is at the home it was filled for; if it was MOVED (copied into gatesets/), re-fill HERE in the same action (fill_gate21T1b.py re-reads\n#        develop + the four heads and refuses on any disagreement with the pins) — rc 8;",
  "#   (0b) the kit is at the home it was filled for; if it was MOVED (copied into gatesets/), re-fill HERE in the same action (fill_gate21T2c.py re-reads\n#        develop + the eight heads and refuses on any disagreement with the pins) — rc 8;"),
 ("#   (1)  origin develop + refs/pull/N/head + the branch for all four by `git ls-remote`",
  "#   (1)  origin develop + refs/pull/N/head + the branch for all eight by `git ls-remote`"),
 ("#   (2)  the four heads re-read from the GitHub PULLS API", "#   (2)  the eight heads re-read from the GitHub PULLS API"),
 ("#   (3b) develop: if origin develop != the launcher's pinned launch develop, RE-PIN IN THIS SAME ACTION — predict_gate21T1b.py over the develop just read\n#        (a FULL scratch clone FROM ORIGIN under <scratchpad>; it REFUSES unless the move descends from BASE, the move ∩ EACH PR's own paths is EMPTY,\n#        the base-invariant checks hold per PR, and the END_TREE agrees in three orders + a second instrument), then fill_gate21T1b.py",
  "#   (3b) develop: if origin develop != the launcher's pinned launch develop, RE-PIN IN THIS SAME ACTION — predict_gate21T2c.py over the develop just read\n#        (a FULL scratch clone FROM ORIGIN under <scratchpad>; it REFUSES unless the move descends from BASE, the move ∩ EACH PR's own paths is EMPTY —\n#        or ONLY the declared #1221 x #1237 overlap in its exact shape — the base-invariant checks hold per PR, and the END_TREE agrees in three orders +\n#        a second instrument), then fill_gate21T2c.py"),
 ("# launcher itself. Derived (derive_repin_gate21T1b.py) from the sibling tier-1 kit's repin script of the same round, re-keyed to these four rows.",
  "# launcher itself. Derived (derive_repin_gate21T2c.py) from the sibling tier-1 kit gate21T1b's repin script, re-keyed to these eight rows."),
 ("# Usage: repin_and_launch_gate21T1b.sh", "# Usage: repin_and_launch_gate21T2c.sh"),
 ("echo \"usage: repin_and_launch_gate21T1b.sh <launcher path> <scratchpad dir> [--dry-run] — e.g. $GS/launch_qa_secuura_batch1224-t1.sh\"",
  "echo \"usage: repin_and_launch_gate21T2c.sh <launcher path> <scratchpad dir> [--dry-run] — e.g. $GS/launch_qa_secuura_batch1218-t2.sh\""),
 ("OUTP=\"$SP/repin_g21b_dry_$T\"", "OUTP=\"$SP/repin_g21c_dry_$T\""),
 ("PANE='QA/Secuura-batch1224'", "PANE='QA/Secuura-batch1218'"),
 ("row() { sed -n \"s/^  \\\"$1|[^|]*|\\([^|]*\\)|\\([0-9a-f]\\{40\\}\\)|[0-9]*|[0-9]*|[^|\\\"]*\\\"$/\\\\$2/p\" \"$L\"; }\nNS='1224 1226 1228 1230'",
  "row() { sed -n \"s/^  \\\"$1|[^|]*|\\([^|]*\\)|\\([0-9a-f]\\{40\\}\\)|[0-9]*|[0-9]*|[^|\\\"]*|T[0-9]\\\"$/\\\\$2/p\" \"$L\"; }\nNS='" + NS + "'"),
 ("control: QA/Secuura-batch1213 = $(/usr/bin/grep -c -F 'QA/Secuura-batch1213|coagent@agentmail.to|yes' \"$ROUTING\"))",
  "control: QA/Secuura-batch1224 = $(/usr/bin/grep -c -F 'QA/Secuura-batch1224|coagent@agentmail.to|yes' \"$ROUTING\"))"),
 ("pass $GS/launch_qa_secuura_batch1224-t1.sh\"; exit 8; }", "pass $GS/launch_qa_secuura_batch1218-t2.sh\"; exit 8; }"),
 ("python3 \"$GS/fill_gate21T1b.py\" \"$SP\" > \"$OUTP.refill.out\"", "python3 \"$GS/fill_gate21T2c.py\" \"$SP\" > \"$OUTP.refill.out\""),
 ("echo \"  DRY RUN: MOVED KIT — the real run re-fills here (fill_gate21T1b.py) in the same action\"", "echo \"  DRY RUN: MOVED KIT — the real run re-fills here (fill_gate21T2c.py) in the same action\""),
 ("git -C \"$CHECKOUT\" ls-remote origin refs/heads/develop refs/pull/1224/head refs/pull/1226/head refs/pull/1228/head refs/pull/1230/head \\\n  \"$(row 1224 1)\" \"$(row 1226 1)\" \"$(row 1228 1)\" \"$(row 1230 1)\" > \"$OUTP.lsremote.out\" 2>&1",
  "git -C \"$CHECKOUT\" ls-remote origin refs/heads/develop " + ' '.join('refs/pull/%s/head' % n for n in NS.split()) + " \\\n  " + ' '.join('"$(row %s 1)"' % n for n in NS.split()) + " > \"$OUTP.lsremote.out\" 2>&1"),
 ("for n in ('1224', '1226', '1228', '1230'):", "for n in (" + ', '.join("'%s'" % n for n in NS.split()) + "):"),
 ("capture_mail_gate21T1b.py, predict_gate21T1b.py and fill_gate21T1b.py first\"; exit 11; }", "capture_mail_gate21T2c.py, predict_gate21T2c.py and fill_gate21T2c.py first\"; exit 11; }"),
 ("echo \"  BOTH INSTRUMENTS AGREE with all four pins.\"", "echo \"  BOTH INSTRUMENTS AGREE with all eight pins.\""),   # derive_repin_1: the anchor carried two leading spaces the source line does not
 ("python3 \"$GS/predict_gate21T1b.py\" \"$SP\"", "python3 \"$GS/predict_gate21T2c.py\" \"$SP\""),
 ("python3 \"$GS/fill_gate21T1b.py\" \"$SP\" > \"$OUTP.repin_fill.out\"", "python3 \"$GS/fill_gate21T2c.py\" \"$SP\" > \"$OUTP.repin_fill.out\""),
]
for a, b in R:
    assert t.count(a) == 1, ('anchor count != 1', t.count(a), a[:100])
    t = t.replace(a, b)
left = [l for l in t.splitlines() if not l.startswith('# launcher itself. Derived (derive_repin_gate21T2c.py)') and ('gate21T1' in l or 'g21b' in l or 'batch1224-t1' in l or '1226' in l or '1228' in l or '1230' in l
                                      or ('1224' in l and 'batch1224' not in l) or 'four' in l.lower())]
assert not left, left
open(sys.argv[2], 'w', encoding='utf-8').write(t)
print('written', sys.argv[2], len(t), 'B')
