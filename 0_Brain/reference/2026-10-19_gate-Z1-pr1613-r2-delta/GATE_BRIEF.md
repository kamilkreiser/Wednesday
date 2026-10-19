# Gate brief: GATE Z1 = PR #1613 round 2 DELTA (KS-1195 per-hour window), Sonnet, tier 2 delta

Commissioned by Wednesday after Seat E 3rd's READY FOR DELTA GATE of 06:25Z (beside this brief: E3_READY_DELTA_0625Z.txt, the author's CLAIM). Round 1 was gate X1 (Opus, GO at 009749ed2565; verdict /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-19_gate-X1-pr1613-ks1195/verdict.md). Secuura only. Project: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files (READ ONLY: ls-remote, show, diff, cat-file, log; work in your own clone).

**The delta:** 009749ed2565..c336de8312211a188f22a41b63e68df8046bb293 adds an explicit `rateLimitWindow: 3600` (const `CONNECTOR_RATE_LIMIT_WINDOW_SECONDS`) to the register-connector mint body, so Kam's ruled "3,000 per HOUR" no longer depends on the security service's `.default(3600)`; plus WINDOW and ROTATE-WINDOW cells, and CONTROL-1/CONTROL-2 widened to "carries rate OR window". develop = 722e07f19cee683ea037930e601e380a9491f7b5.

## Questions (each with its instrument; name what you did NOT run)
1. **The delta is exactly as claimed:** `git diff 009749ed2565 c336de831221` = platform.ts (+12) and the test file only; the PR's 3-dot diff vs develop = exactly 2 files.
2. **3600 is accepted by the security service's mint schema** on that route: read its `rateLimitWindow` bound (author says `.min(60).max(86400)`), cite the line, and confirm the value is stored and reaches the gateway limiter (X1's chain: validate returns it, `rateLimitEnforce.ts:184` uses it).
3. **The widened controls still fail when they should:** plant a mutation that makes the re-register path send `rateLimitWindow` only (no rate) and confirm CONTROL-1 or CONTROL-2 reds; W1 (window -> 60) and W2 (line removed) red the two new cells.
4. **Landing:** merge-tree onto LIVE develop (re-read ls-remote at start and before the verdict): author predicts 9a3a5619e806511f2861ced32ae1aacc2a3cb8c7. api-gateway suite on the landing tree (author: 117 files, 1153); tsc.

Verdict file: verdict.md in this folder; first line `VERDICT: ... at head c336de831221...`; last line the sha256 of the file with its first and last lines removed. Scratch: /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fab5379f-182f-40a2-8bd3-ff9052525009/scratchpad/z1/. Findings only: no fixes, no GitHub or Linear writes, nothing under !CODING, no `cd`, no `rm`, no stderr to /dev/null, no Docker. Every zero gets a positive control.
