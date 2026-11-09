# Gate 288, TIER 1 (Opus): PR 2132 (KS-1473, round 1, Seat G 31st) + PR 2127 (KS-785, ROUND 2 OF 2, Seat R 91st). ONE session, two independent verdicts. Commissioned 2026-11-09 17:5x by the 17:3x Wednesday seat (batched under Kam's 2026-09-18 minimise-gate-duplication rule: both tier 1, disjoint paths by the seats' READYs; prove disjointness yourself).

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole, applied at FULL tier-1 depth to PR 2132 and at tier-1 COMPARE depth to PR 2127 (round 2 of 2 under the two-NO-GO cap: a NO GO on PR 2127 ships the closed instances and tickets the residue; say which instances are closed).

Pins (Wednesday's ls-remote at 17:55:22 AEDT; RE-READ at start and end, and say whether each moved):
- develop e8d23ce366e292ed6ca13f296cc2cfb2a3796496 (PR 2113 squash; both seats built on older bases: G 31st on 204e62acdc35, R 91st's round 2 cut from round 1 on 4d6b7bb17fd3: read what develop's move changed and whether it touches either PR's paths)
- PR 2132 head ba0ab4f453497257e9848c16f884ae8900a2f195 (one commit, parent 204e62acdc35)
- PR 2127 head 7dc6ff72cf61de04bb65a0e859cf670e9ff0ac85 (a new commit on round 1's 190ffa868d7d; no force, no rebase, by the seat)
- PR 2052 head b61674e7b7635a50d51f837849cb9caf1259235d (open, overlaps PR 2127 on check-slot-credentials.sh)

READYs (read whole; reproduce, do not trust):
- PR 2132: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatG-31st/mail/out_07_ready_ks1473.txt (evidence under that seat folder, evidence/measure_ks1473/, drafts/predictions_ks1473.md). Wednesday's rulings to G 31st on the two test-list edits are among /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-09_G31_answer_*.md (the READY cites 05:24:39Z and 05:26:34Z: find them and say which files).
- PR 2127 round 2: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatR-91st/mail/ready_ks785_r2_r91.txt. Round 1 verdict to compare against: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate283-tier1-pr2127-ks785/verdict.md (read whole). The fix-round ruling: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-09_R91_answer_gate283_fixround.md. R's 'export KEY=' widening of the ruled `^KEY=` pattern is ACCEPTED by Wednesday as a shape; whether it is correct about what Compose and the checker read is YOUR question (Q B2).

Questions, PR 2132 (KS-1473, CSRF):
A1. The change: csrf.ts drops the two verify-batch exclusions; the developer portal row is replaced by an HTML comment. Read csrf.ts whole at the head. Which exclusions remain, and is each still needed? Can a cookie-authenticated browser now reach any state-changing route that was exempt before, and does any legitimate NON-browser client of verify-batch (SDK, connector, server-to-server, the MCP server's own /verify-batch at http-server.ts:161) now get 403 where it used to work? Enumerate the callers at develop (grep for verify-batch across services, packages, frontends, docs, tests) and say whether each sends the CSRF token or a non-cookie auth that the middleware skips.
A2. The premise: before the change, is a cookie-only POST to /api/verification/verify-batch (v1 alias and case variants) really CSRF-exempt, and is there really no router or spec path for it? Reproduce with the seat's harness and an independent request of your own.
A3. The suite: red on develop for exactly N1, N2, N3a, N3b, P1; green at the head 8/8; the controls C1 and C2 green on both. Your own mutants (each entry back separately, the portal row back) redden named cells. Do the two removed KS-1461/KS-1469 cells and the relabelled one lose coverage of anything still true at the head?
A4. tsc and eslint deltas zero against develop; docs-fragments OK with a planted defect proving it can fail.

Questions, PR 2127 round 2 (KS-785):
B1. Compare: for each gate 283 finding (G283-1 ... G283-K, KEYS), CLOSED / OPEN / CHANGED at the new head, by your own reproduction (Compose render-only, fixtures only).
B2. The shape: start-environment.sh never executes .env; it greps for `^(export[[:space:]]+)?(POSTGRES_PASSWORD|REDIS_PASSWORD)=` and unsets only those exports. Is the grep exactly the set of lines Compose's env_file parsing and the checker (its lines 171-172) read? Cases: quoted key, leading spaces, a commented line, `export  KEY=` with two spaces, KEY with no value, CRLF lines. Can the grep or the unset print or trace a secret value? Does any OTHER export now behave differently from develop?
B3. check-slot-credentials.sh claimed COMMENT ONLY again (154 non-comment lines identical): prove or refute with a comment-stripped compare and a planted control both ways; are the rewritten comments (develop 109-112) true?
B4. Overlap: merge tree of 2127 with PR 2052 in both orders, both edits present; and 2127 with 2132 (expect disjoint).
B5. The suite 46/46 with the 32 develop labels kept; your own mutants (develop's script; source .env back; unset every .env key; unconditional unset) each redden a named cell.

Both: any path covered ONLY by a skipped hook leg (3, 4, 8)?

Constraints: clones on the boot volume under /private/tmp/g288 (no rm; state its size at the end); never cd; NEVER git fetch or any git write verb in any /Volumes/DevMASTER/!CODING checkout (fetch only in your own /private/tmp clone); never push; never run the hook against the real remote; never source or open any real .env or credential file (fixtures only); never run `docker compose up` or start containers; keep load1 under 8; df DevMASTER at start and end.

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate288-tier1-pr2132-pr2127r2/verdict.md (if your Write is refused, put the whole verdict in your final message). Line 1 exactly: 'PR 2132: <V>; PR 2127: <V>' with each V one of GO | GO WITH NOTES | NO GO. Then per PR: FOUND / TESTED / HOW (instrument, controls), NOT TESTED, and findings with ids G288-2132-<n> and G288-2127-<n>, each with a severity. Findings only; post nothing; mail nothing.
