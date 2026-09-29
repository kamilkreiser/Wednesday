---
date: 2026-09-29
type: preference
source: Kam, Friday's terminal, 2026-09-29 ~13:2x AEST
status: live
tier: W
---

# Datasec GitHub: every change reaches main through a PR that passes CodeQL. Never a direct push, never a dismissed alert

**His words, verbatim:** *"there has been a change to the datasec github account.  this is an organisational policy recently implemented.   we need to adhere to it so adjust accordingly - commits need to go through codeQL"*

**The operative case, so the headline matches it:** a seat (or Friday) is about to land work on `main` of ANY `datasecau` repo: code, records or docs (HPSM-POC, HPSM-POC-analysis, HPSM-analysis, HPSM-light, …). **It goes by branch → PR → CodeQL green → a head-pinned merge.** It was first measured 2026-09-29 ~06:14 AEST, as a GH013 refusal: "Code scanning is waiting for results from CodeQL".

**How to apply:**
1. **Every Datasec brief carries the standing line:** *"Push your branch only, never main (the org ruleset requires CodeQL results). Friday opens the PR, and merges head-pinned once CodeQL and the checks are green."* Records go on a `records/<round>` branch from the seat's own worktree.
2. **Friday's merge sequence:** `friday_as.sh datasec gh pr create` → wait for the check-runs (CodeQL + the Analyze jobs + the repo's CI) → `gh pr merge --squash --match-head-commit <sha>` → compare the merge's tree (or its delta blobs) with the head.
3. **A CodeQL alert is FIXED in the code, never dismissed by a seat or by Friday**, even in a test file where it is harmless in practice. Dismissing an alert is Kam's call. Precedent: 2026-09-29, alert #21 (`js/incomplete-multi-character-sanitization`) in a test helper on HPSM-light #10 was fixed by the builder, not dismissed.
4. **Never ask for, add or use a ruleset bypass.** Changing the org policy is Kam's (and Datasec IT's).
5. **Scope:** the Datasec GitHub organisation. Other clients' repos follow their own rules. Do not generalise this to them without Kam's word.

**Family:** [[2026-08-07_protocol-v1.3-signed-delegation]] (merges are Friday's; the policy decides HOW) · [[2026-09-09_my-authority-and-the-targets-rules-are-two-checks]] (my authority AND the target's rules; this is the target's rule) · [[2026-08-09_an-enforcement-you-must-arm-is-not-one]] (the ruleset is in-path enforcement: work with it, never around it).
