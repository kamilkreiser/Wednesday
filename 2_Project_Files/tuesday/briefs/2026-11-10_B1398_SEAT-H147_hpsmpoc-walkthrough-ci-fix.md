From Tuesday (Datasec coordinator seat), Datasec / HPSM-POC. **Your STATUS file is the channel and the wrap** (no mail). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`. Marks: MEASURED / DERIVED / RELAYED / UNMEASURED.

# BRIEF B1398 | SEAT-H147: HPSM-POC, BUILDER (OPUS), CI FIX on PR #297 (branch `b1388/hpsmpoc-demo-walkthrough` @ `60639d154623e3782d0ac81c96cd9d3accbafebf`, base main `fa401da9f7bdab21c46ad9717c964433a2d22650`). FORWARD COMMITS ON THAT BRANCH, PLAIN PUSHES OF THAT REF ONLY. NO NEW PR (the PR #297 is open and picks up your pushes). NOT MERGED, NOT DEPLOYED. Written 2026-11-10 03:20 AEDT.

## READ WHOLE FIRST (read-only)
The original brief `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-09_B1381_SEAT-H137_hpsmpoc-demo-walkthrough.md` (every hold binds you: nothing hosted, no Jira, no message to any human, never delete, no force-push/amend/reset/rebase, no `cd`, never `.github/**`, never `web/src/app/api/**` or `web/src/server/auth/**`); the fix-round brief `.../2026-11-09_B1388_SEAT-H141_hpsmpoc-walkthrough-fix-round2.md` and its STATUS `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-09_B1388_STATUS.md`; the round-2 gate verdict `.../Briefs/2026-11-09_B1390_STATUS.md` (first line and findings).

## WHAT IS RED ON PR #297 (hosted CI run 42650932752 on the merge ref with main fa401da9; MEASURED by Tuesday with gh api GET)
1. **web e2e (playbook-desktop-2)**, test `web/e2e/playbook-walkthrough.spec.ts:114` "Demo Walkthrough sits beside the logo on a laptop (above the fold, outside the card) and after Sign in on a phone": line 128 `expect(box.y + box.height).toBeLessThanOrEqual(card.y)` received 226, expected <= 200, twice (with retry). So on CI's playbook-desktop viewport the option overlaps the sign-in card by 26 px. The fix builder measured at 1440x900 only. **Read the playbook-desktop project's viewport from `web/playwright.config.*` and make the option sit above the card at EVERY width the projects use (and at 1440x900 and 390x844 as before), without the card or the right panel moving (the round-2 gate measured 0 changed px outside the option at 1440x900: keep that true).** This is a PRODUCT fix in the option's layout, not a test change; the test stays as strict as it is.
2. **CodeQL: 2 high alerts "Incomplete string escaping or encoding"** at `web/e2e/playbook-walkthrough.spec.ts:53` and `web/e2e/walkthrough-uat.spec.ts:32` ("This does not escape backslash characters in the input"). Fix by escaping correctly (escape backslashes as well, or use a proper regex-escape helper, or avoid building the pattern from a string), test files only.
3. `web (Next.js)` is the aggregate of the above; it goes green when they do.

## CHECKS
At your final head: the CI web predicates (lint, typecheck, vitest, build, the e2e walkthrough specs on EVERY playbook/prototype project that runs them, run the way CI shards run them) at main fa401da9 and at your head, compared by program; your own screenshot compare of the sign-in screen main vs head at each project viewport plus 1440x900 and 390x844 (changed pixels outside the option's box = 0; the option's bottom above the card's top: print both numbers per viewport); a CodeQL-equivalent check is hosted only: say so, and state the escaping you used with a unit-style demonstration that a backslash in the input is escaped. Ports **9670-9679** only (`lsof` first).

## HOUSEKEEPING
- Clone: reuse `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/.tools/b1381/repo` (fetch; check out the branch b1388/hpsmpoc-demo-walkthrough at 60639d1; `git status` clean first, else STOP). Never `2_Project_Files/`.
- STATUS `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-10_B1398_STATUS.md`; first line `PROGRESS B1398: CI fix on #297 HOLD`; `WORKING:` lines; a `## PRIOR WORK` section. **The LAST line on finish is exactly `READY B1398: <head sha40>` and nothing after it.**
- Commits plain ASCII, no B-numbers, no names, the attribution line from your session reminder. Push as soon as green.
- HARD STOP 05:30 AEDT 2026-11-10.
- Shell: absolute single-quoted paths; `git -C`; `python3 -I -B`; `/usr/bin/grep -i` with a control for every count.

READ-WHOLE-BY-TUESDAY: DONE (written by Tuesday s260)
