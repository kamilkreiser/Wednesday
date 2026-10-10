From Friday (laptop seat), Datasec / MPS Commercial Calculator.

# BRIEF B33 · SEAT-C — redeploy the hosted showcase to main `db8edfd` (CODE ONLY), the same way B31 PART A did
**From:** Friday, 10:23 AEDT 2026-10-11. **Pane:** `Datasec/MPS-C`; your commission is the newest `Briefs/` file containing `_SEAT-C_`. Report `Briefs/2026-10-11_B33_STATUS.md`; last line `DEPLOYED: <sha> live-check <rc>` or `STOPPED: NEEDS FRIDAY` + one question.

## AUTHORITY
- Kam, live board (Friday tab), 2026-10-11 10:22:57, verbatim: *"Decision mpscalc-b30-new-words-hosted-deploy-1011: a — Approve the wording and deploy"*. Option a: *"A deploy seat ships main db8edfd to the same link, code only; Friday checks it live and tells you."*

## THE RUNBOOK IS B31 PART A — follow it step for step, with these substitutions only
- Read `Briefs/2026-10-11_B31_SEAT-C_hosted-redeploy-4f27f55-and-approver-account.md` (§ Target, § HOLDS, § PART A, § Rollback, § Other holds) and `Briefs/2026-10-11_B31_STATUS.md` (the exact commands B31 ran and what each printed). **PART B is NOT part of this brief: no Entra or Graph call of any kind.**
- **Target:** `git ls-remote origin refs/heads/main` must start with `db8edfd5082e49f9a1a1b3c23feeb02b36834b21` (Friday's read of PR #24's merge at 09:3x). Anything else: STOP.
- **What changed since the live build:** `git log --oneline 4f27f55..<sha>` = the B30 squash (#24) only; `git diff --name-only 4f27f55 <sha> -- infra scripts .github` = empty (Friday measured 0 such files from the GitHub compare API at 10:2x).
- **Live today:** main `4f27f55`, deployed by B31. **Rollback = 4f27f55** from B31's kept package (find it from B31_STATUS; re-verify its sha256 before deploying the new build). Keep this build's package too.
- **Post-deploy items:** B31's set (L1, R1, MATCH, start log, settings `diff` empty, quotes and overlay unchanged, leak counts) PLUS every item in `Briefs/2026-10-11_B32_STATUS.md` § `Post-deploy check items` that a seat can run. Items that need a signed-in human browser (Kam's account, or the Approver account whose MFA is not yet registered) are `NOT TESTED (Kam)`, never faked. Confirm the NEW WORDS strings from `B30_STATUS.md` (round 0 and ADDENDUM-1 tables) are present in the served bundle (counts, as B31 did).
- Same HOLDS as B31: no app-setting change; SITE HOLD stands; no new Azure resource; nothing to any human; never delete; never print a secret; Datasec only.
