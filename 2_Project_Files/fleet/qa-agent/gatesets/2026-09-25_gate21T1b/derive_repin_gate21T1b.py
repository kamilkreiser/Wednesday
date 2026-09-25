#!/usr/bin/env python3
"""derive_repin_gate21T1b.py <tier-1 repin> <out> — derive repin_and_launch_gate21T1b.sh from the sibling tier-1 kit's script by anchored replacements
(every anchor must be present; a missing one aborts; a leftover sibling token aborts). Kept beside the kit so the derivation is reproducible."""
import sys
t = open(sys.argv[1], encoding='utf-8').read()
R = [
 ("# repin_and_launch_gate21T1.sh — the LAUNCH ACTION for the round-21 tier-1 batch gate over #1213 KS-530, #1214 KS-528, #1216 KS-975, #1217 KS-976.",
  "# repin_and_launch_gate21T1b.sh — the LAUNCH ACTION for the round-21 SECOND tier-1 batch gate over #1224 KS-1179, #1226 KS-872, #1228 KS-1171,\n# #1230 KS-1131 (FROZEN at four)."),
 ("# never trusts a pin it did not just re-read:", "# never trusts a pin it did not just re-read (four rows; #1230 is two commits, ahead 2; every head's merge base is the OLD develop 6ab9d5021):"),
 ("#   (0b) the kit is at the home it was filled for; if it was MOVED (copied into gatesets/), re-fill HERE in the same action (fill_gate21T1.py re-reads\n#        develop + the four heads and refuses on any disagreement with the pins) — rc 8;",
  "#   (0b) the kit is at the home it was filled for; if it was MOVED (copied into gatesets/), re-fill HERE in the same action (fill_gate21T1b.py re-reads\n#        develop + the four heads and refuses on any disagreement with the pins) — rc 8;"),
 ("#   (2)  the four heads re-read from the GitHub PULLS API (a second, independent instrument) — rc 3 if a read fails;",
  "#   (2)  the four heads re-read from the GitHub PULLS API (a second, independent instrument; also `mergeable`) — rc 3 if a read fails;"),
 ("#   (3)  rc 11 unless every head == the launcher's pin on BOTH instruments AND every PR is open (A STALE HEAD REFUSES — e.g. #1213's pending frvp\n#        re-date commit: a new head needs its READY re-captured, predict + fill re-run; this script never adopts a head it was not given);",
  "#   (3)  rc 11 unless every head == the launcher's pin on BOTH instruments AND every PR is open AND none is `mergeable: false` (A STALE HEAD REFUSES:\n#        a new head needs its READY re-captured, predict + fill re-run; this script never adopts a head it was not given);"),
 ("#   (3b) develop: if origin develop != the launcher's pinned launch develop, RE-PIN IN THIS SAME ACTION — predict_gate21T1.py over the develop just read\n#        (a scratch clone FROM ORIGIN under <scratchpad>; it REFUSES unless the move descends from BASE, touches none of the 13 paths, and the END_TREE\n#        agrees in three orders + a second instrument), then fill_gate21T1.py",
  "#   (3b) develop: if origin develop != the launcher's pinned launch develop, RE-PIN IN THIS SAME ACTION — predict_gate21T1b.py over the develop just read\n#        (a FULL scratch clone FROM ORIGIN under <scratchpad>; it REFUSES unless the move descends from BASE, the move ∩ EACH PR's own paths is EMPTY,\n#        the base-invariant checks hold per PR, and the END_TREE agrees in three orders + a second instrument), then fill_gate21T1b.py"),
 ("# launcher itself. Derived from gatesets/2026-09-23_gate20T1r2_1210/repin_and_launch_r2.sh, widened to four PRs.",
  "# launcher itself. Derived (derive_repin_gate21T1b.py) from the sibling tier-1 kit's repin script of the same round, re-keyed to these four rows."),
 ("# Usage: repin_and_launch_gate21T1.sh", "# Usage: repin_and_launch_gate21T1b.sh"),
 ("echo \"usage: repin_and_launch_gate21T1.sh <launcher path> <scratchpad dir> [--dry-run] — e.g. $GS/launch_qa_secuura_batch1213-t1.sh\"",
  "echo \"usage: repin_and_launch_gate21T1b.sh <launcher path> <scratchpad dir> [--dry-run] — e.g. $GS/launch_qa_secuura_batch1224-t1.sh\""),
 ("OUTP=\"$SP/repin_g21_dry_$T\"", "OUTP=\"$SP/repin_g21b_dry_$T\""),
 ("PANE='QA/Secuura-batch1213'", "PANE='QA/Secuura-batch1224'"),
 ("row() { sed -n \"s/^  \\\"$1|[^|]*|\\([^|]*\\)|\\([0-9a-f]\\{40\\}\\)|[0-9]*\\\"$/\\\\$2/p\" \"$L\"; }",
  "row() { sed -n \"s/^  \\\"$1|[^|]*|\\([^|]*\\)|\\([0-9a-f]\\{40\\}\\)|[0-9]*|[0-9]*|[^|\\\"]*\\\"$/\\\\$2/p\" \"$L\"; }\nNS='1224 1226 1228 1230'"),
 ("for n in 1213 1214 1216 1217; do [ -n \"$(row $n 2)\" ]", "for n in $NS; do [ -n \"$(row $n 2)\" ]"),
 ("for n in 1213 1214 1216 1217; do echo \"  pin #$n $(row $n 2)\"; done", "for n in $NS; do echo \"  pin #$n $(row $n 2)\"; done"),
 ("control: QA/Secuura-batch1204 = $(/usr/bin/grep -c -F 'QA/Secuura-batch1204|coagent@agentmail.to|yes' \"$ROUTING\"))",
  "control: QA/Secuura-batch1213 = $(/usr/bin/grep -c -F 'QA/Secuura-batch1213|coagent@agentmail.to|yes' \"$ROUTING\"))"),
 ("pass $GS/launch_qa_secuura_batch1213-t1.sh\"; exit 8; }", "pass $GS/launch_qa_secuura_batch1224-t1.sh\"; exit 8; }"),
 ("python3 \"$GS/fill_gate21T1.py\" \"$SP\" > \"$OUTP.refill.out\"", "python3 \"$GS/fill_gate21T1b.py\" \"$SP\" > \"$OUTP.refill.out\""),
 ("echo \"  DRY RUN: MOVED KIT — the real run re-fills here (fill_gate21T1.py) in the same action\"", "echo \"  DRY RUN: MOVED KIT — the real run re-fills here (fill_gate21T1b.py) in the same action\""),
 ("git -C \"$CHECKOUT\" ls-remote origin refs/heads/develop refs/pull/1213/head refs/pull/1214/head refs/pull/1216/head refs/pull/1217/head \\\n  \"$(row 1213 1)\" \"$(row 1214 1)\" \"$(row 1216 1)\" \"$(row 1217 1)\" > \"$OUTP.lsremote.out\" 2>&1",
  "git -C \"$CHECKOUT\" ls-remote origin refs/heads/develop refs/pull/1224/head refs/pull/1226/head refs/pull/1228/head refs/pull/1230/head \\\n  \"$(row 1224 1)\" \"$(row 1226 1)\" \"$(row 1228 1)\" \"$(row 1230 1)\" > \"$OUTP.lsremote.out\" 2>&1"),
 ("for n in ('1213', '1214', '1216', '1217'):", "for n in ('1224', '1226', '1228', '1230'):"),
 ("    print('API #%s head %s base %s state %s' % (n, p['head']['sha'], p['base']['ref'], p['state']))",
  "    print('API #%s head %s base %s mergeable %s state %s' % (n, p['head']['sha'], p['base']['ref'], p.get('mergeable'), p['state']))"),
 ("for n in 1213 1214 1216 1217; do\n  H=", "for n in $NS; do\n  H="),
 ("  A=\"$(awk -v n=\"#$n\" '$1==\"API\" && $2==n{print $4}' \"$OUTP.api_heads.out\")\"; S=\"$(awk -v n=\"#$n\" '$1==\"API\" && $2==n{print $NF}' \"$OUTP.api_heads.out\")\"",
  "  A=\"$(awk -v n=\"#$n\" '$1==\"API\" && $2==n{print $4}' \"$OUTP.api_heads.out\")\"; S=\"$(awk -v n=\"#$n\" '$1==\"API\" && $2==n{print $NF}' \"$OUTP.api_heads.out\")\"\n  M=\"$(awk -v n=\"#$n\" '$1==\"API\" && $2==n{print $8}' \"$OUTP.api_heads.out\")\""),
 ("  echo \"  #$n  ls-remote pull/head ${P:-ABSENT} | branch ${B:-ABSENT} | API ${A:-ABSENT} (state ${S:-?}) | pinned $H\"\n  [ \"$P\" = \"$H\" ] && [ \"$B\" = \"$H\" ] && [ \"$A\" = \"$H\" ] && [ \"$S\" = \"open\" ] || { echo \"    STALE or CLOSED: #$n\"; bad=1; }",
  "  echo \"  #$n  ls-remote pull/head ${P:-ABSENT} | branch ${B:-ABSENT} | API ${A:-ABSENT} (state ${S:-?}, mergeable ${M:-?}) | pinned $H\"\n  [ \"$P\" = \"$H\" ] && [ \"$B\" = \"$H\" ] && [ \"$A\" = \"$H\" ] && [ \"$S\" = \"open\" ] && [ \"$M\" != \"False\" ] || { echo \"    STALE, CLOSED or NOT MERGEABLE: #$n\"; bad=1; }"),
 ("capture_mail_gate21T1.py, predict_gate21T1.py and fill_gate21T1.py first\"; exit 11; }", "capture_mail_gate21T1b.py, predict_gate21T1b.py and fill_gate21T1b.py first\"; exit 11; }"),
 ("python3 \"$GS/predict_gate21T1.py\" \"$SP\"", "python3 \"$GS/predict_gate21T1b.py\" \"$SP\""),
 ("python3 \"$GS/fill_gate21T1.py\" \"$SP\" > \"$OUTP.repin_fill.out\"", "python3 \"$GS/fill_gate21T1b.py\" \"$SP\" > \"$OUTP.repin_fill.out\""),
 ("a move that touches the batch's paths is re-predicted BY HAND, never here", "a move that touches a PR's OWN paths is re-predicted BY HAND, never here"),
]
for a, b in R:
    assert t.count(a) == 1, ('anchor count != 1', t.count(a), a[:100])
    t = t.replace(a, b)
left = [l for l in t.splitlines() if ('gate21T1.' in l or 'gate21T1_' in l or '1213' in l and 'batch1213' not in l or '1214' in l or '1216' in l or '1217' in l)]
assert not left, left
open(sys.argv[2], 'w', encoding='utf-8').write(t)
print('written', sys.argv[2], len(t), 'B')
