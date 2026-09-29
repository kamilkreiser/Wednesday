---
date: 2026-09-29
type: preference
source: Kam, Friday's terminal, 2026-09-29 ~13:2x AEST
status: live
tier: W
---

# Datasec GitHub: a commit reaches main only after CodeQL has scanned THAT commit on a PR. Never bypass, never dismiss an alert

**His words, verbatim:** *"there has been a change to the datasec github account.  this is an organisational policy recently implemented.   we need to adhere to it so adjust accordingly - commits need to go through codeQL"*

**The operative case, so the headline matches it:** a seat (or Friday) is about to land work on `main` of ANY `datasecau` repo: code, records or docs (HPSM-POC, HPSM-POC-analysis, HPSM-analysis, HPSM-light, …). **Every commit that lands on main is one CodeQL scanned on a PR:** branch → PR → CodeQL green → then EITHER a head-pinned squash merge (Friday's route) OR a fast-forward push of that SAME scanned commit (NexusAI's route, C-190, PR #32, 2026-09-29; the ruleset accepts it and marks the PR merged). **What is forbidden is a commit on main that CodeQL never scanned on a PR**, not the push verb. It was first measured 2026-09-29 ~06:14 AEST, as a GH013 refusal: "Code scanning is waiting for results from CodeQL".

**How to apply:**
1. **Every Datasec brief carries the standing line:** *"Push your branch only. Friday opens the PR and lands it once CodeQL and the checks are green (the org ruleset requires CodeQL results; never push an unscanned commit to main)."* Records go on a `records/<round>` branch from the seat's own worktree.
2. **Friday's merge sequence:** `friday_as.sh datasec gh pr create` → wait for the check-runs (CodeQL + the Analyze jobs + the repo's CI) → `gh pr merge --squash --match-head-commit <sha>` → compare the merge's tree (or its delta blobs) with the head.
3. **A CodeQL alert is FIXED in the code, never dismissed by a seat or by Friday**, even in a test file where it is harmless in practice. Dismissing an alert is Kam's call. Precedent: 2026-09-29, alert #21 (`js/incomplete-multi-character-sanitization`) in a test helper on HPSM-light #10 was fixed by the builder, not dismissed.
4. **Never ask for, add or use a ruleset bypass.** Changing the org policy is Kam's (and Datasec IT's).
5. **Scope:** the Datasec GitHub organisation. Other clients' repos follow their own rules. Do not generalise this to them without Kam's word.

**Family:** [[2026-08-07_protocol-v1.3-signed-delegation]] (merges are Friday's; the policy decides HOW) · [[2026-09-09_my-authority-and-the-targets-rules-are-two-checks]] (my authority AND the target's rules; this is the target's rule) · [[2026-08-09_an-enforcement-you-must-arm-is-not-one]] (the ruleset is in-path enforcement: work with it, never around it).

**NARROWED 2026-09-29 13:3x, the same hour, by Tuesday** (mail `[Tuesday -> Friday] Re: Datasec GitHub CodeQL`): the first headline said "never a direct push", which is wider than the ruleset and would have contradicted NexusAI's recorded C-190 procedure. Her formulation was adopted: *"never push a commit to main that CodeQL has not scanned on a PR; never bypass; never dismiss"*. This is [[2026-09-08_a-new-rule-is-most-dangerous-just-after-adoption]] caught within the hour.
