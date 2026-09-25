#!/usr/bin/env python3
"""derive_repin_gate21T2b.py <gate21T2 repin> <out> — derive repin_and_launch_gate21T2b.sh from the sibling tier-2 kit's script
(gatesets/2026-09-25_gate21T2/repin_and_launch_gate21T2.sh) by anchored replacements (every anchor must be present; a missing one aborts; no
sibling key may survive). One addition over the sibling: step 2 also reads `mergeable` from the pulls API (Wednesday 04:35Z: "check ... that
`mergeable` on the PR is true") and step 3 refuses on an explicit False (null = GitHub still computing, reported, not refused)."""
import re, sys
t = open(sys.argv[1], encoding='utf-8').read()
R = [
 ("It READS develop and the six heads AT LAUNCH and", "It READS develop and the five heads AT LAUNCH and"),
 ("# repin_and_launch_gate21T2.sh — the LAUNCH ACTION for the round-21 TIER-2 batch gate over #1215 KS-1288, #1218 KS-897+896, #1220 KS-1129,\n# #1221 KS-1266, #1222 KS-1181, #1223 KS-1118 (FROZEN at six).",
  "# repin_and_launch_gate21T2b.sh — the LAUNCH ACTION for the round-21 SECOND tier-2 batch gate over #1225 KS-1291, #1227 KS-1252+1253,\n# #1229 KS-865+808(3), #1231 KS-1281, #1232 KS-1128 (FROZEN at five)."),
 ("# never trusts a pin it did not just re-read (six rows; #1218 is two commits, ahead 2):",
  "# never trusts a pin it did not just re-read (five rows; #1227 and #1229 are two commits each, ahead 2):"),
 ("re-fill HERE in the same action (fill_gate21T2.py re-reads\n#        develop + the six heads and refuses",
  "re-fill HERE in the same action (fill_gate21T2b.py re-reads\n#        develop + the five heads and refuses"),
 ("the branch for all six by `git ls-remote`", "the branch for all five by `git ls-remote`"),
 ("#   (2)  the six heads re-read from the GitHub PULLS API (a second, independent instrument) — rc 3 if a read fails;",
  "#   (2)  the five heads re-read from the GitHub PULLS API (a second, independent instrument), with `mergeable` — rc 3 if a read fails;"),
 ("every head == the launcher's pin on BOTH instruments AND every PR is open",
  "every head == the launcher's pin on BOTH instruments AND every PR is open AND none reads mergeable=False"),
 ("(the tier-1 batch merging on ITS GO is the likely mover), RE-PIN IN THIS\n#        SAME ACTION — predict_gate21T2.py",
  "(the batch1215 tier-2 gate's and the next tier-1 batch's merges are the\n#        likely movers), RE-PIN IN THIS SAME ACTION — predict_gate21T2b.py"),
 ("touches none of the 14 paths, and the END_TREE agrees in three orders + a second instrument), then fill_gate21T2.py",
  "touches none of the 10 paths, the BASE-INVARIANT check holds, and the END_TREE agrees in three orders + a second instrument), then fill_gate21T2b.py"),
 ("Derived (derive_repin_gate21T2.py) from the sibling tier-1 kit's repin script of the same round, re-keyed to six rows.",
  "Derived (derive_repin_gate21T2b.py) from the sibling tier-2 kit's repin script of the same round, re-keyed to five rows."),
 ("# Usage: repin_and_launch_gate21T2.sh", "# Usage: repin_and_launch_gate21T2b.sh"),
 ("usage: repin_and_launch_gate21T2.sh <launcher path> <scratchpad dir> [--dry-run] — e.g. $GS/launch_qa_secuura_batch1215-t2.sh",
  "usage: repin_and_launch_gate21T2b.sh <launcher path> <scratchpad dir> [--dry-run] — e.g. $GS/launch_qa_secuura_batch1225-t2.sh"),
 ('OUTP="$SP/repin_g21T2_dry_$T"', 'OUTP="$SP/repin_g21T2b_dry_$T"'),
 ("PANE='QA/Secuura-batch1215'", "PANE='QA/Secuura-batch1225'"),
 ("NS='1215 1218 1220 1221 1222 1223'", "NS='1225 1227 1229 1231 1232'"),
 ("control: QA/Secuura-batch1213 = $(/usr/bin/grep -c -F 'QA/Secuura-batch1213|coagent@agentmail.to|yes' \"$ROUTING\"))",
  "control: QA/Secuura-batch1215 = $(/usr/bin/grep -c -F 'QA/Secuura-batch1215|coagent@agentmail.to|yes' \"$ROUTING\"))"),
 ('echo "  DRY RUN: MOVED KIT — the real run re-fills here (fill_gate21T2.py) in the same action"', 'echo "  DRY RUN: MOVED KIT — the real run re-fills here (fill_gate21T2b.py) in the same action"'),
 ('pass $GS/launch_qa_secuura_batch1215-t2.sh"; exit 8; }', 'pass $GS/launch_qa_secuura_batch1225-t2.sh"; exit 8; }'),
 ('python3 "$GS/fill_gate21T2.py" "$SP" > "$OUTP.refill.out"', 'python3 "$GS/fill_gate21T2b.py" "$SP" > "$OUTP.refill.out"'),
 ('git -C "$CHECKOUT" ls-remote origin refs/heads/develop refs/pull/1215/head refs/pull/1218/head refs/pull/1220/head refs/pull/1221/head refs/pull/1222/head refs/pull/1223/head \\\n  "$(row 1215 1)" "$(row 1218 1)" "$(row 1220 1)" "$(row 1221 1)" "$(row 1222 1)" "$(row 1223 1)" > "$OUTP.lsremote.out" 2>&1',
  'git -C "$CHECKOUT" ls-remote origin refs/heads/develop refs/pull/1225/head refs/pull/1227/head refs/pull/1229/head refs/pull/1231/head refs/pull/1232/head \\\n  "$(row 1225 1)" "$(row 1227 1)" "$(row 1229 1)" "$(row 1231 1)" "$(row 1232 1)" > "$OUTP.lsremote.out" 2>&1'),
 ("for n in ('1215', '1218', '1220', '1221', '1222', '1223'):", "for n in ('1225', '1227', '1229', '1231', '1232'):"),
 ("    print('API #%s head %s base %s state %s' % (n, p['head']['sha'], p['base']['ref'], p['state']))",
  "    print('API #%s head %s base %s mergeable %s state %s' % (n, p['head']['sha'], p['base']['ref'], p.get('mergeable'), p['state']))"),
 ('  A="$(awk -v n="#$n" \'$1=="API" && $2==n{print $4}\' "$OUTP.api_heads.out")"; S="$(awk -v n="#$n" \'$1=="API" && $2==n{print $NF}\' "$OUTP.api_heads.out")"\n  echo "  #$n  ls-remote pull/head ${P:-ABSENT} | branch ${B:-ABSENT} | API ${A:-ABSENT} (state ${S:-?}) | pinned $H"\n  [ "$P" = "$H" ] && [ "$B" = "$H" ] && [ "$A" = "$H" ] && [ "$S" = "open" ] || { echo "    STALE or CLOSED: #$n"; bad=1; }',
  '  A="$(awk -v n="#$n" \'$1=="API" && $2==n{print $4}\' "$OUTP.api_heads.out")"; S="$(awk -v n="#$n" \'$1=="API" && $2==n{print $NF}\' "$OUTP.api_heads.out")"; M="$(awk -v n="#$n" \'$1=="API" && $2==n{print $(NF-2)}\' "$OUTP.api_heads.out")"\n  echo "  #$n  ls-remote pull/head ${P:-ABSENT} | branch ${B:-ABSENT} | API ${A:-ABSENT} (state ${S:-?}, mergeable ${M:-?}) | pinned $H"\n  [ "$P" = "$H" ] && [ "$B" = "$H" ] && [ "$A" = "$H" ] && [ "$S" = "open" ] && [ "$M" != "False" ] || { echo "    STALE, CLOSED or NOT MERGEABLE: #$n"; bad=1; }'),
 ("capture_mail_gate21T2.py, predict_gate21T2.py and fill_gate21T2.py first\"; exit 11; }", "capture_mail_gate21T2b.py, predict_gate21T2b.py and fill_gate21T2b.py first\"; exit 11; }"),
 ('echo "  BOTH INSTRUMENTS AGREE with all six pins."', 'echo "  BOTH INSTRUMENTS AGREE with all five pins."'),
 ('python3 "$GS/predict_gate21T2.py" "$SP"', 'python3 "$GS/predict_gate21T2b.py" "$SP"'),
 ('python3 "$GS/fill_gate21T2.py" "$SP" > "$OUTP.repin_fill.out"', 'python3 "$GS/fill_gate21T2b.py" "$SP" > "$OUTP.repin_fill.out"'),
]
for a, b in R:
    assert t.count(a) >= 1, ('anchor absent', a[:100])
    t = t.replace(a, b)
left = [l for l in t.splitlines() if re.search(r'gate21T2(?!b)', l) or re.search(r'(?<!batch)\b12(18|20|21|22|23)\b', l) or ('1215' in l and 'batch1215' not in l) or re.search(r'\bsix\b', l)]
assert not left, left
open(sys.argv[2], 'w', encoding='utf-8').write(t)
print('written', sys.argv[2], len(t), 'B')
