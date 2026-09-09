# QA GATE BRIEF — Secuura/Blockchain PR #935 (KS-1057) — TIER 1, ROUND 2

## WHY THERE IS A ROUND 2, AND IT IS NOT BECAUSE ROUND 1 FAILED

Round 1 returned **GO WITH FINDINGS** on head `0b5ad9ac2` — 1 Major (F1), 3 Minor. **The head has since moved to `039da8d6e`.** Round 1's verdict is a verdict on a commit that is no longer at the head, which is the *head-moved-off-your-GO* shape this fleet has hit three times. **A GO is a statement about a SHA, never about a PR.**

**Round 2 exists for two reasons and the second is the important one:**

1. F1 and F2 were fixed on the new head.
2. **The fix round introduced a BEHAVIOUR CHANGE that no gate has ever seen** — see below. It was found by the builder's own test, not by round 1's gate and not by Wednesday.

**This is round 2 of 2 under the cap.** A NO GO here ships the closed instances and tickets the residue; it does not open a round 3 without Kam.

## THE UNREVIEWED BEHAVIOUR CHANGE — this is the pass's centre of gravity

The builder reports: with `status` carried into the tier-2 synthesised blob (F1's fix), **a FAILED anchor still reported `pending-onchain`, because that helper mapped EVERY non-confirmed status to pending.** So it changed the mapping: **`failed` now maps to `off-chain-only`; `submitted` and `pending` keep `pending-onchain`.**

**That is a change to what the endpoint SAYS about a document, made inside a fix round, and nobody outside the builder has looked at it.**

**Drive it. All of it.** Enumerate every status value that reaches that mapping and observe what each one reports, at base and at head. **The question is not "does `failed` now say off-chain-only" — it is "what does EVERY status say now, and is any of them newly wrong?"** A mapping change tested only on the value that motivated it is a change tested on one cell.

## WHAT ELSE CHANGED, as the builder reports it — RE-DERIVE, DO NOT INHERIT

- **F1 fix:** `status: latest.status` added to the synthesised blob in `makeFetchDocFromAnchorStore`. The builder states it verified `formatAnchorResponse` (`anchoring/src/index.ts:1480`) emits `status: anchor.status` before using the field. **Check that it does.**
- **The carve-out was deliberately NOT deleted**, and a CONTROL cell was added so a future "fix" cannot come to mean "delete it". **Confirm that cell exists and that it CAN fail.**
- **F2 fix:** the carve-out's comment rewritten to count producers from source and to say the branch is fail-**open** and load-bearing.
- Reported evidence: target suite **9/9**; red proof **2 failed / 7 passed / 9 total, exit 1**, the two being the F1 defect cells with the CONFIRMED control green, restore byte-identical; full api-gateway suite **303/303** across 28 files.

**Everything above is the builder's account, relayed by Wednesday, which holds no client identity and re-derived none of it.**

## CARRY FORWARD FROM ROUND 1 — verify these survived

- **Round 1's four answers must still hold at the new head**: the tier-1 fix still works, the carve-out still admits the four real seeded blobs (including the KS-481 canonical example), the test is still behavioural with tests actually RUNNING, and the KS-1067 lock merge is still fully separable with merge-base `d4cf7e3cf`.
- **F3 and F4 were filed as KS-1069 and deliberately NOT fixed.** Do not re-report them as new; confirm they are unchanged and move on.

## THE TSCONFIG LIMIT — round 1 established it, state it again if you cite tsc

api-gateway's `tsconfig` **excludes `src/__tests__`**, and `--listFiles` finds zero occurrences of the test file. **A `tsc --noEmit` green on this package type-checks the product and ZERO added test lines.** If you cite a tsc green, cite it with that limit attached.

## NOT REQUIRED LEGS, and why — said before running, not after

**Schemathesis and both spec legs are NOT required and must not be run as required legs.** Round 1 established with evidence: `VerifyResponse.verificationConfidence` is declared `type: string` **with no enum**, so a schema sweep has nothing to compare against on the field that changed; the spec-examples gate is a content/PII gate that cannot see a value flip; the cassette leg keeps shape only. **All three are structurally blind to a change in the VALUE of an unconstrained field.**

## WHAT ROUND 1 NAMED AS ITS OWN WEAKEST PREMISE — close it if you cheaply can

Round 1's F1 rested on tier 2 having no ownership check, **read from the helper's docstring and the route, NOT driven with two identities**, because its harness stubbed `authenticateToken` open. It flagged that itself. **If you can drive two identities cheaply, do — and if you cannot, say so in the same words rather than inheriting the premise silently.**

## HOW TO REPORT — unchanged

Findings only; you never fix. Every zero gets a control that could have produced a non-zero, run in the same action, and the control must fail independently of the failure it tests for. **Say which property each green establishes.** State what you did NOT test at the same prominence as what you did. **If a claim in this brief is false, that is Wednesday's error and report it as one** — round 1 did exactly that and was right.

## BOUNDS

- **Demo and UAT are HELD.** Local, disposable, no hosted requests.
- **`develop` is merge-frozen repo-wide, so a `blocked` state tells you nothing about #935.**
- No contact with Peter or Stuart. No `--no-verify`. Never delete — quarantine. Do not touch the advisory baseline or branch protection.

## VERDICT DESTINATION

**Mail your verdict to `wednesday-agent@agentmail.to`**, subject
`[QA -> Wednesday] TIER 1 GATE #935 ROUND 2 (KS-1057) 039da8d6e — GO / GO WITH FINDINGS / NO GO`,
with a CLOSING section naming anything you want acted on. **Your pane has no scrollback and you cannot receive mail: the verdict mail is the only thing that survives your session.**
