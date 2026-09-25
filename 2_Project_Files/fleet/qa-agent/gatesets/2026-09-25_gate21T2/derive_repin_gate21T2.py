#!/usr/bin/env python3
"""derive_repin_gate21T2.py <tier-1 repin> <out> — derive repin_and_launch_gate21T2.sh from the sibling tier-1 kit's script by anchored replacements
(every anchor must be present; a missing one aborts). Kept beside the kit so the derivation is reproducible."""
import sys
t = open(sys.argv[1], encoding='utf-8').read()
R = [
 ("# repin_and_launch_gate21T1.sh — the LAUNCH ACTION for the round-21 tier-1 batch gate over #1213 KS-530, #1214 KS-528, #1216 KS-975, #1217 KS-976.",
  "# repin_and_launch_gate21T2.sh — the LAUNCH ACTION for the round-21 TIER-2 batch gate over #1215 KS-1288, #1218 KS-897+896, #1220 KS-1129,\n# #1221 KS-1266, #1222 KS-1181, #1223 KS-1118 (FROZEN at six)."),
 ("# never trusts a pin it did not just re-read:", "# never trusts a pin it did not just re-read (six rows; #1218 is two commits, ahead 2):"),
 ("#   (0b) the kit is at the home it was filled for; if it was MOVED (copied into gatesets/), re-fill HERE in the same action (fill_gate21T1.py re-reads\n#        develop + the four heads and refuses on any disagreement with the pins) — rc 8;",
  "#   (0b) the kit is at the home it was filled for; if it was MOVED (copied into gatesets/), re-fill HERE in the same action (fill_gate21T2.py re-reads\n#        develop + the six heads and refuses on any disagreement with the pins) — rc 8;"),
 ("#   (1)  origin develop + refs/pull/N/head + the branch for all four by `git ls-remote`, READ from the Secuura checkout (read verb only) — rc 2;\n#   (2)  the four heads re-read",
  "#   (1)  origin develop + refs/pull/N/head + the branch for all six by `git ls-remote`, READ from the Secuura checkout (read verb only) — rc 2;\n#   (2)  the six heads re-read"),
 ("#   (3)  rc 11 unless every head == the launcher's pin on BOTH instruments AND every PR is open (A STALE HEAD REFUSES — e.g. #1213's pending frvp\n#        re-date commit: a new head needs its READY re-captured, predict + fill re-run; this script never adopts a head it was not given);",
  "#   (3)  rc 11 unless every head == the launcher's pin on BOTH instruments AND every PR is open (A STALE HEAD REFUSES: a new head needs its READY\n#        re-captured, predict + fill re-run; this script never adopts a head it was not given);"),
 ("#   (3b) develop: if origin develop != the launcher's pinned launch develop, RE-PIN IN THIS SAME ACTION — predict_gate21T1.py over the develop just read\n#        (a scratch clone FROM ORIGIN under <scratchpad>; it REFUSES unless the move descends from BASE, touches none of the 13 paths, and the END_TREE\n#        agrees in three orders + a second instrument), then fill_gate21T1.py",
  "#   (3b) develop: if origin develop != the launcher's pinned launch develop (the tier-1 batch merging on ITS GO is the likely mover), RE-PIN IN THIS\n#        SAME ACTION — predict_gate21T2.py over the develop just read (a scratch clone FROM ORIGIN under <scratchpad>; it REFUSES unless the move\n#        descends from BASE, touches none of the 14 paths, and the END_TREE agrees in three orders + a second instrument), then fill_gate21T2.py"),
 ("# launcher itself. Derived from gatesets/2026-09-23_gate20T1r2_1210/repin_and_launch_r2.sh, widened to four PRs.",
  "# launcher itself. Derived (derive_repin_gate21T2.py) from the sibling tier-1 kit's repin script of the same round, re-keyed to six rows."),
 ("# Usage: repin_and_launch_gate21T1.sh", "# Usage: repin_and_launch_gate21T2.sh"),
 ("echo \"usage: repin_and_launch_gate21T1.sh <launcher path> <scratchpad dir> [--dry-run] — e.g. $GS/launch_qa_secuura_batch1213-t1.sh\"",
  "echo \"usage: repin_and_launch_gate21T2.sh <launcher path> <scratchpad dir> [--dry-run] — e.g. $GS/launch_qa_secuura_batch1215-t2.sh\""),
 ("OUTP=\"$SP/repin_g21_dry_$T\"", "OUTP=\"$SP/repin_g21T2_dry_$T\""),
 ("PANE='QA/Secuura-batch1213'", "PANE='QA/Secuura-batch1215'"),
 ("row() { sed -n \"s/^  \\\"$1|[^|]*|\\([^|]*\\)|\\([0-9a-f]\\{40\\}\\)|[0-9]*\\\"$/\\\\$2/p\" \"$L\"; }",
  "row() { sed -n \"s/^  \\\"$1|[^|]*|\\([^|]*\\)|\\([0-9a-f]\\{40\\}\\)|[0-9]*|[0-9]*\\\"$/\\\\$2/p\" \"$L\"; }\nNS='1215 1218 1220 1221 1222 1223'"),
 ("for n in 1213 1214 1216 1217; do [ -n \"$(row $n 2)\" ]", "for n in $NS; do [ -n \"$(row $n 2)\" ]"),
 ("for n in 1213 1214 1216 1217; do echo \"  pin #$n $(row $n 2)\"; done", "for n in $NS; do echo \"  pin #$n $(row $n 2)\"; done"),
 ("control: QA/Secuura-batch1204 = $(/usr/bin/grep -c -F 'QA/Secuura-batch1204|coagent@agentmail.to|yes' \"$ROUTING\"))",
  "control: QA/Secuura-batch1213 = $(/usr/bin/grep -c -F 'QA/Secuura-batch1213|coagent@agentmail.to|yes' \"$ROUTING\"))"),
 ("pass $GS/launch_qa_secuura_batch1213-t1.sh\"; exit 8; }", "pass $GS/launch_qa_secuura_batch1215-t2.sh\"; exit 8; }"),
 ("python3 \"$GS/fill_gate21T1.py\" \"$SP\" > \"$OUTP.refill.out\"", "python3 \"$GS/fill_gate21T2.py\" \"$SP\" > \"$OUTP.refill.out\""),
 ("echo \"  DRY RUN: MOVED KIT — the real run re-fills here (fill_gate21T1.py) in the same action\"", "echo \"  DRY RUN: MOVED KIT — the real run re-fills here (fill_gate21T2.py) in the same action\""),
 ("git -C \"$CHECKOUT\" ls-remote origin refs/heads/develop refs/pull/1213/head refs/pull/1214/head refs/pull/1216/head refs/pull/1217/head \\\n  \"$(row 1213 1)\" \"$(row 1214 1)\" \"$(row 1216 1)\" \"$(row 1217 1)\" > \"$OUTP.lsremote.out\" 2>&1",
  "git -C \"$CHECKOUT\" ls-remote origin refs/heads/develop refs/pull/1215/head refs/pull/1218/head refs/pull/1220/head refs/pull/1221/head refs/pull/1222/head refs/pull/1223/head \\\n  \"$(row 1215 1)\" \"$(row 1218 1)\" \"$(row 1220 1)\" \"$(row 1221 1)\" \"$(row 1222 1)\" \"$(row 1223 1)\" > \"$OUTP.lsremote.out\" 2>&1"),
 ("for n in ('1213', '1214', '1216', '1217'):", "for n in ('1215', '1218', '1220', '1221', '1222', '1223'):"),
 ("for n in 1213 1214 1216 1217; do\n  H=", "for n in $NS; do\n  H="),
 ("capture_mail_gate21T1.py, predict_gate21T1.py and fill_gate21T1.py first\"; exit 11; }", "capture_mail_gate21T2.py, predict_gate21T2.py and fill_gate21T2.py first\"; exit 11; }"),
 ("echo \"  BOTH INSTRUMENTS AGREE with all four pins.\"", "echo \"  BOTH INSTRUMENTS AGREE with all six pins.\""),
 ("python3 \"$GS/predict_gate21T1.py\" \"$SP\"", "python3 \"$GS/predict_gate21T2.py\" \"$SP\""),
 ("python3 \"$GS/fill_gate21T1.py\" \"$SP\" > \"$OUTP.repin_fill.out\"", "python3 \"$GS/fill_gate21T2.py\" \"$SP\" > \"$OUTP.repin_fill.out\""),
]
for a, b in R:
    assert t.count(a) >= 1, ('anchor absent', a[:90])
    t = t.replace(a, b)
left = [l for l in t.splitlines() if ('gate21T1' in l or ('1213' in l and 'batch1213' not in l) or '1214' in l or '1216' in l or '1217' in l)]
assert not left, left
open(sys.argv[2], 'w', encoding='utf-8').write(t)
print('written', sys.argv[2], len(t), 'B')
