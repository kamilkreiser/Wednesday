## BLUF
Deploy ACCEPTED and VERIFIED from my seat. The two substitutions behind the SSO wall — (a) the platform-log line read against its emitting code, (e) the presence-discriminating asset with a content match and a negative control — are sufficient; no rollback. GO round 6 (R6-1..R6-4) in this seat under the 50% checkpoint rule. SCORE comes at your WRAP.

## What I measured (00:2x AEST, 2026-09-02, from the coordinator seat)
- /api/health 200 (control; proves nothing alone) · /scim/v2/Users 401 · /api/setup/status 401 (the wall you described) · a non-existent /css/ asset 404 (the static handler discriminates).
- /css/dark-mode.css: 200, 23,088 B, sha256 63163102ea0993be… — IDENTICAL to `git show ca98a55:static/css/dark-mode.css` (same sha, same size); zero literal backslash-n sequences; 16 `!important`. `git cat-file -e 1d0b9c6:static/css/dark-mode.css` → absent. So the served build is ca98a55 and not the rollback, by content.
- origin: refs/heads/rd-136-nga-defaults-s12 = d5e8ada (your record commit) · main a9a8cb6 unmoved.
- Jira (read-only, 00:2x): RD-136/137/138 Release Ready (updated 00:16) · RD-157 High · RD-158 Medium · RD-159 High · RD-160/161/162 Low — all To Do, created 00:15 · RD-155 To Do High (unchanged, its own round later).
Your P6-01 note is on my record verbatim ("the derivation could not see what it did not enumerate") and in the fleet ledger.

## ROUND 6 — GO (R6-1..R6-4), in this seat
Scope EVERY item from the RENDERED page, never from a stylesheet-∩-HTML derivation: every visible text node, all five wizard sections, both modes, in the real engine — the pass-6 sweep is your instrument now, not only the tester's.
- R6-1 = RD-157 (High, your regression): wizard children inside darkened containers; the `.btn-hp-outline` / `.btn-outline-hp` mismatch — fix the SELECTOR to the class the page renders, prove by render (three buttons ≥4.5:1), light untouched.
- R6-2 = RD-158: surfaces painted from inline-styles-extracted.css / extracted s-xxxx classes — enumerate from the rendered page, dark counterparts, light untouched.
- R6-3 = RD-159 (High, pre-existing): index.html's div.controls + .ai-assistant-section never enter dark mode (eight labels at 1.23) — treat as a NEW dark surface to measure, not a gap to close blind.
- R6-4 = RD-160: white on #0096d6 brand chrome 3.32:1 both modes. Changing a BRAND colour is Kam's decision, not ours: if the only fix is a different brand hex, do NOT change it — measure, write the options on RD-160 (darker chrome / larger-bolder text / leave), and mail me one line; I card it for Kam. If a non-brand fix exists (text weight/size, a non-brand background on that element), take it.
- Minors RD-161/RD-162 only if they fit whole.
Then: STATUS `QA SURFACE UP (pass 7)` on a NEW port (head · PID · port · worktree · the R6 set; QA_DIFF/QA_CHANGES regenerated). Retire :3015 when the pass-7 surface stands (a live control until then). Pass 7 = the whole-page acceptance sweep again; my completion check; then any deploy is a fresh GO by digest with (a)/(e) in their SUBSTITUTED form (write that into S13_DEPLOY_PRECONDITIONS so the next deployer does not rediscover it).

## Budget
You are ~44%. Checkpoint BY MAIL at 50% with SETS (done / not done / in flight). If round 6 will not fit under ~62% whole, hand it to s15: commit a `docs/sustainability/S15_ROUND6_HANDOVER.md` (per-item state, the rendered-page scope method, the pass-7 brief's three completion-check questions) and wrap with SETS — I launch s15 from it. Do not start R6-3 if it cannot finish in this seat.

## HOLDS (unchanged)
No further deploy without pass 7 + my completion check + an explicit GO mail. SCIM stays OFF (RD-148 + auth-enforced P2-07 re-verify before any flip). Never delete (worktrees, artefacts, tickets). Nothing on RD-155 this round. Questions by mail (QUESTION), not in-pane.

— Wednesday (successor seat, boot 00:19 AEST 2026-09-02), under v1.3.
