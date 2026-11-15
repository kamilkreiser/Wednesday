# Drafter notes: Seat K 22nd merge brief (2026-11-15, read-only drafter, Sonnet)

Output: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-15_seatK22_merge.md (about 49.7 KB). Scratch and evidence: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-15_drafter-seatK22/_work/ (scripts survey22.py, shift22.py, matcher22.py, trees22.py, stack22.py, linear22.py; outputs heads_live.json, titles_live.json, trees_live.json, files_live.json, gate_hits.json, linear_live.json, queue_rows.md; shifted kit copy kit22/; clone c22/).

## What was found
- develop = dc42dc89493f4235e7954dcd6c181e05072d1231 (PR 2229 squash; API merged_at 08:07:35Z, committer 08:07:34Z, not 08:09Z which is K 21st's own live read). Equal at 19:11, 19:17, 19:18.
- K 21st HAS WRAPPED: HANDOVER.md has a FINAL block (WRAP 08:11Z), measured r 51.0, Wednesday ruled WRAP naming 2235 first. The brief is drafted from the FINAL block.
- Queue: 61 rows (62 minus 2229); order equals K 21st's FINAL 'Remaining order' string; 61 of 61 heads equal and open; 28 T1 / 33 T2; 27 DNM.
- Trees on dc42dc89: 61 of 61 rc 0 both orders, same tree; 2 planted controls hold; 10 of 10 stacked pairs plus 7 neighbour pairs clean. 2235 tree cf72670ec7bc; its billing subtree 5f0230534cd7 equals the gate 361 merge's billing tree (2229 touched vc-issuer only), so gate figures 21/395, 22/400, 23/418 are controls.
- Re-key: source set 103 files (tools 38, evidence 48 = 42 rule + SIX _build.py, aids 17), not K 21st's 86 (38/35/13). Counts: P1 1/0/0, G1 20/47/18, G4 1/0/5, G5 113/108/59, G6 19/10/5, G7 135/288/113, N 37/48/10. Matcher: 738/738 table alone; 743/743 table + T; no-P1 fails with 5 MISMATCH lines. T appends FIVE items, not six: "K 220th" is already in OTHER_SEATS. Syntax 0 bad of 103; sed cross-check 103 of 103.
- Only PR 2195 has a two-key title (Refs KS-1988, KS-2075); no queued row needs K22_TITLE_EXTRA_KEYS.
- Linear: all 62 KS ids In Progress; newest comment times are in the QUEUE table.

## Things Wednesday must rule (also in the brief)
1. Whether the SIX _build.py models stand as the declared extension (K 21st's ANSWER covered four; it wrote the two 2229 models afterwards).
2. Whether K22_TITLE_EXTRA_KEYS (shifted from K21_) stays in the kit as shipped or is reverted to the pre-edit copy; the brief says it is not a licence.
3. The NAME MAP in CARRIED (two generations of 'K 20th/K 21st' wording in the two referenced briefs) is correct as written.
4. Row-1 cost: 103-file re-key vs 86 is unmeasured; the brief expects a one-row seat (2235) by the 52.0 line.

## UNMEASURED
- Every install, suite, tsc, eslint, audit run; K 21st's suite figures (claims).
- Whether K 21st's pane is closed; whether Seat A 32nd has pushed to billing; which seats C, F, AA, R, E are live; whether PR 2230 merged after 19:18.
- Gate verdicts beyond line 1 for the 57 older rows (found by head sha scan; 2075 by hand); each gate's findings.
- decisions.json since 17:5x; mergeable state beyond 'unstable'; check-run counts (403 for the runner token per K 21st).
- The pre-push hook location (not at Blockchain/2_Project_Files/.git/hooks/pre-push).
- The test command for PR 2234 (systemTest/schemathesis, Python; not vitest).
- Whether merge_k21.py's comma-list KEY matches 'Refs KS-1988, KS-2075:' (KEYS_TXT join form).
- Running any re-keyed tool beyond syntax and the matcher self-test; the re-key's cost; whether K 21st's tools changed after 19:17.
- ls-remote (no deploy key in the drafter's shell).
