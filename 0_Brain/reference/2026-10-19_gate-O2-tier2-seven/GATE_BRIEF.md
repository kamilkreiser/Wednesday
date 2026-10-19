# Gate brief: GATE O2 = seven TIER-2 PRs, batched, Sonnet, round 1 of 2

Commissioned by the Wednesday seat, 2026-10-19 ~11:4x AEDT. Routing v1.0 tier-2 gate row (tests only, logging, ordering; no auth decision). Seat R 50th raised them. Its READY mail of 00:37Z is the author's claim, NOT evidence. develop = 78cb3c3939e319332e387ffecb075a169edd4a39 (Wednesday ls-remote ~11:4x; re-read it).
0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/. Project paths are under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

| PR | ticket | head (Wednesday ls-remote, equal to R's) | what (R's description) | author's suite figure |
|---|---|---|---|---|
| #1591 | KS-1620 item 1 | a992894cdbf74e7eaf7b93cb280520d77c442948 | mcp-server get_info bounds the relayed gateway text to 200 | mcp-server 15/15 |
| #1592 | KS-1621 (1 of 2) | ac758817103cfb1208a27fc0f508250512556b03 | test only: a real prior height of 0 is carried as 0 | originate 1406/1406 |
| #1593 | KS-1621 (2 of 2) | 587fe9dbf0a77bc54e19b3227ec9394280ce4376 | test only: a thrown class instance logs its constructor name | api-gateway 1196/1196 |
| #1594 | KS-1627 (2 of 2) | 2cda8fe5243f0308c85f44f9d6261125db9583db | test only: the info reader's 200 with the REAL redis in Redis mode | api-gateway 1196/1196 |
| #1595 | KS-1526 | 46795487b69cafbc96012f9e9b792551b19d5ff5 | api-gateway production File logs are JSON lines | api-gateway 1199/1199 |
| #1600 | KS-1544 | 6499cce63ab90bd28c566c13a0f722947136029d | tenant-provisioning audit log `ORDER BY created_at DESC, id DESC` | tenant-provisioning 21/21 |
| #1601 | KS-1525 | c08b786603c3a30fcc1a985e0effdab9041c9923 | test only: two rowToApiKey isActive boundaries (G1, G10) | security 346/346 |

#1591-#1595 were built on develop 83ed01af70fd; develop has moved 3 merges since (originate/api-gateway). **Re-predict each merge onto the live develop (tree id) and run the owning suites on the PREDICTED tree.**

## Gate (through code, tier 2)
1. Diff each at its head; nothing outside its named files; the seven pairwise file-disjoint (check it). Test-only PRs: product files byte-unchanged.
2. Red-first on each: the RED cells fail on develop (or under the PR's named tamper) by an assertion; the controls pass on both.
3. One mutant per product hunk (#1591, #1595, #1600), killed by a named cell.
4. **#1600 questions:** the tie-break `id` is a random UUID (migrations/003_platform_tenancy.sql:50), so paging is deterministic, NOT chronological: say whether the route's consumers need more. And does a test that pins the ORDER BY text satisfy a ticket whose own test spec asks for the two-window behaviour? The query-plan check was not done. Leave this as a NOTE, not a NO GO, unless the PR claims more than it does.
5. **#1601:** the ticket's G7/G8 are deliberately not added. R measured that `rowToApiKey` returns `''` for empty-string ids at the tip. Confirm by calling the real function.
6. **#1591:** its "no ellipsis" differs from the ticket's example, not from the ticket. Confirm against the ticket text.
7. Merge prediction: all seven onto live develop, tree ids. Note any pair that collides with the tier-1 five in gate O1 (#1597 originate verification.ts, #1590 anchoring anchorReadback.ts, #1596 originate gdpr test, #1598 api-gateway middleware/auth.ts, #1599 auth oauth.ts + auth.openapi.ts + the yaml).

## Rules
- Read-only on the project. **Your OWN scratch folder is /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2ce15c23-3025-4dcd-9e03-2be96a0a6754/scratchpad/o2/. Use nothing else in that scratchpad** (o1/ is the tier-1 gate running beside you). Clone with `git clone --shared` from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, set origin to git@github.com:Secuura/Distributed_Secuura.git in YOUR clone, and fetch with that checkout's `core.sshCommand` plus `-o ServerAliveInterval=30`. Build `packages/shared` before any suite.
- No git write verb in !CODING, no push, no GitHub or Linear writes, no Docker, no servers. No cd. Never send stderr to /dev/null. Loops go in script FILES run with /bin/bash. Every zero needs a control that fired. One heavy suite at a time.

## Output
- Write 0_Brain/reference/2026-10-19_gate-O2-tier2-seven/verdict.md.
- Lines 1-7: one verdict per PR, each naming its FULL head.
- Line 8: `sha256/16: <16 hex>` of the report with line 8 deleted.
- Then FOUND / TESTED / HOW per PR, the merge-prediction table, NOT tested, severities with file:line. Final lines: `MODEL:` and `WALL-CLOCK:`.
