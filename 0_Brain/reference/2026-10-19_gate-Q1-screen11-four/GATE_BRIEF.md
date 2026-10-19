# Gate brief: GATE Q1 = the SCREEN_11 four, batched, Opus, round 1 of 2

Commissioned by the Wednesday seat, 2026-10-19 after R 51st's READY of 02:32Z. Routing v1.0 row G1 (three tier-1 PRs: an API-key usage write in the security service, two OAuth error paths in auth; the tier-2 test-only PR rides in the same batch to avoid a second session). Secuura only.
0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/. Project paths are under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

**METHOD:** exactly the method of gate O1 — read `0_Brain/reference/2026-10-19_gate-O1-tier1-five/GATE_BRIEF.md` whole (its method, controls, verdict format and hard limits apply here unchanged) and its `verdict.md` for the expected shape. The author's claim is R 51st's READY mail, copied whole beside this brief as `R51_READY_0232Z.txt`: it is a CLAIM, not evidence.

develop = 37834600a543cb0276f427d969ac034d9df74fbd (Wednesday ls-remote, just before writing this brief; re-read it).

| PR | ticket | head (Wednesday ls-remote, equal to R's) | tier | author's suite figure |
|---|---|---|---|---|
| #1602 | KS-1377 | 70dc59643b5aaa089606e51a43d2948ab5c671b2 | 1 | security 347/347 |
| #1603 | KS-1617 A.3 | f51d7cab124b9dc9e15172b1fba0cd01fe41e819 | 1 | auth 1073/1073 |
| #1604 | KS-1617 A.2 | 0cc48741299c9d4d8277eafd31c8b6f674ed2da1 | 1 | auth 1071/1071 |
| #1605 | KS-1507 | 934ce30c3c118626647ced229a11ad55a4fabb41 | 2 | auth 1070/1070 |

## Named questions (each answered with its instrument, or "unmeasured")
1. **#1602 GREATEST/NULL arms: MEASURE them on your own scratch PostgreSQL** (not Docker; the author could not; nobody has). `usage_count = usage_count + 1` and `last_used_at = GREATEST(last_used_at, $2)` with last_used_at NULL, with $2 older, with $2 newer, and concurrent increments (several clients). Then judge R's two residue sites (`services/security/src/index.ts:425` upsert clobbers usage_count on mint/revoke/rotate; `:1494` serves usageCount from memory): acceptable residue on KS-1377, or a reason to hold #1602 because it WIDENS the API-vs-row divergence? Recommend one.
2. **#1603 Q3: R says the new text reaches the caller's 400 body** (`routes/auth.ts:1032-1035` -> `errorHandler.ts:293`, `:300`). Re-read that chain yourself. Then recommend: ship as is (the provider's HTTP status in a 400 body), or the alternative shape (status in the log line only, thrown message unchanged). Name what a caller learns that it could not learn before.
3. **#1604 Q2:** confirm R's logger reading in both modes (`services/auth/src/utils/logger.ts:16`, `:33-34`): the caller-supplied `error_description` cannot forge a log line, and is not echoed in any auth response (cell A2-3).
4. **KS-1641** (R filed it from Q2): not in this batch; do not gate it. If your reading of m365-integration `index.ts:465` disagrees with R's, say so in one line.
5. Each PR: red-first reproduced by you (or a planted mutant for #1605), the suite count at the landing parent, `git apply --check` on the live tip, the chained landing tree of all four onto develop (no collisions), and whether any PR touches a file of open #1597 or #1568.
6. **Read the PR's Test Evidence for every suite of every service it touches**; any such suite you did not run goes in NOT tested BY NAME with the reason (gate P1 left one unnamed today, and it was red).

Verdict file: `verdict.md` in this folder; first line `VERDICT:` per PR; sha256 of the file with its first line deleted on the last line. Scratch: your own `q1/` under /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c4419525-d2e2-49d0-8b3f-577263d823bb/scratchpad/. No writes under !CODING, no GitHub or Linear writes, no `cd`, no `rm`, no stderr to /dev/null.
