# gate77 — RULINGS for Wednesday (drafted 2026-10-09 ~09:20–10:30 AEDT, 2026-10-08T22:20Z–23:30Z; NOT launched)

Every OPEN question carries the drafter's recommendation and a DEFAULT. The default is what kit.json and the prompt already assume, so ruling "as recommended" changes no file. **None blocks the dry run** (rc 0 at the defaults). Q-SEAT77, Q-ORDER77 and Q-MERGEINS77 bind the MERGE SEAT more than the gate.

## CARRIED (binding on the gate, written into the prompt)
- **R1 TIER.** #1432 T1 (security surface: error-text disclosure on the public edge). #1429 #1430 #1431 #1433 #1434 T2. Reasons per row in kit.json `rows.<n>.tier_reason`. The gate may go UP, never down.
- **R2 ACTIONS.** SUBSET, never equality; PENDING never a pass; classify by WORKFLOW ID (three workflows are named `pr`). Security Scanning, PR Security Gates (KS-168) and pr-platform-suites fail on develop itself (R 19th, measured by id): base-state, classified, never a new red by default.
- **R3 PRE-EXISTING MISMATCH.** `VERDICT: MISMATCH — STOP` inside a green run is the F-925-3 fixture arm (gate73 R3, G 5th re-verified it as an asserted `expect` arm at preflight_deps.test.sh:459-460).
- **R4 PLATFORM SUITES** UNMEASURED locally, never counted as passing.
- **R5 MERGE SEAT** never an author (E 11th, F 5th, R 19th, G 5th): the launcher refuses an author ordinal (rc 8).
- **R6 CONTROLS.** Every check can fail; every zero has a control; an arm counts only if it refuses at its OWN assert.
- **R7 RESTORE TO THE HEAD STATE**, never checkout / restore / reset / clean.
- **R8 Q-UNION (gate73, binding, re-measured on THIS batch).** `merge-file --union` leaves table/tr/td +1 open on the flow doc at every step and div/table/tr/td +1 on the cheat doc from step 3; keep-both composition is balanced at every step.
- **R9** No `--no-verify`. A refused push is a STOP.
- **R10 SUBJECTS LAND AS WRITTEN** (STANDING_LINES :320-322): no `(#n)` suffix in any declared subject or addendum, no suffix-length arithmetic; `len(declared) <= 92`, ASCII, own key first.

## OPEN QUESTIONS

**Q-1427FIRST — launch before or after #1427 (gate76 GO 2) lands?**
- At draft develop is `1e7f90e26137` (#1428). #1427 is GO'd and held for the account renewal, which has happened (gauge 1%).
- The repin decides by CONTENT, not sha: if develop's `04-container-trivy.sh` blob != #1427's, the chain is `1427,<order>` with #1427 modelled as step 1. The drafter's composer reproduces gate76's predicted #1427 tree `57c9b5eaec95` and both composed blobs byte for byte, so the model is calibrated.
- *Rec / default:* **(a) land #1427 first, then run the repin**: one fewer moving part, and the prompt then reads "LANDED". The repin will refuse rc 10 on the moved develop. Re-run it with `--repin-develop <origin develop>`; c1 P7 confirms #1427's advance touched no gate77 code path (measured: disjoint). (b) Launch now. The chain then carries #1427 as step 1, and the gate re-predicts when it lands mid-gate.

**Q-ORDER77 — the landing order.**
- *DEFAULT `1432,1433,1429,1434,1431,1430`*: ascending flow number (36 37 38 40 42 43), which also lands the one tier-1 row first. After #1427 (35) the batch tail then reads ascending. Q-N5 does not require that; this order gets it free.
- Every order needs SIX docs-only merge-ins (develop moved on both docs at #1428). The order changes only which composed docs each M carries.
- Predicted final trees at develop 1e7f90e26137: with #1427 first `8ce413c386c691dcb7e2e349c3d4d4e696ca7888`; without #1427 `8304089bf1b7ef734d18d3e31d619dec997aaf56`. Ascending PR-number order (no #1427) gives `4e557c3a5773…`.
- *Rec / default:* as defaulted.

**Q-SEAT77 — who merges?**
- *DEFAULT Seat R 20th* on `Secuura/Blockchain-R` (the gate76 merge seat, which holds the R-lane merge lineage). It is not an author of any gate77 row.
- If R 20th has wrapped (git log: "99% usage stand-down handover; GO 2 held for the renewal"), put its successor ordinal in kit.json `merge_seat_ordinal` and re-run the repin. kit.json is pinned by nothing; the launcher checks lane == ordinal letter and not an author.
- *Rec:* whichever R seat merges #1427 merges gate77, after #1427.

**Q-MERGEINS77 — six merge-ins, six full in-hook preflights.**
- Every M's push delta carries Blockchain/Dev paths (OURS..M 9 → 27 paths along the chain), so the hook runs the FULL preflight on each: about 7 min × 6, plus the SIGPIPE risk on long hooks (STANDING_LINES: never export GIT_SSH_COMMAND; read the push tool's `.rc` + ls-remote).
- No alternative exists: GitHub cannot squash a conflicted PR, and a single combined PR would re-gate everything.
- *Rec / default:* accept. The merge seat re-runs `c2_merge_gate77.py chain --drop <landed rows>` on the REAL develop before EVERY step and takes the composed docs VERBATIM. A STOP on any CODE-UNMOVED failure.

**Q-TIER1355 — #1431 in the data-destruction guard file: T2 or T1?**
- The diff changes only `list_other_stacks()`. Its output is printed under "Other Secuura stacks running on this host (NOT affected by this operation)" and never reaches `blocked` / the return code (drafter READ, head blob :145-258).
- The pre-existing 25 decision cells of stack_guard.test.sh pass with the product reverted AND at the head. Drafter run: c3 `product` R = 25 passed, 2 failed, only the two new cells.
- check-stack-safety.sh greps stack_guard.sh for its filter and resolve lines. Both pushes printed `OK — 13 code guards passed.`
- *Rec / default:* **T2 + a mandatory DECISION-INVARIANT arm** (exit code + BLOCKED lines identical base vs head across fixtures). The gate goes to T1 if any decision consumes that output.

**Q-TIERSCALE — "TIER 1" in the READY mails / raise briefs.**
- G 5th's READY says "TIER 1, test-only"; F 5th's and R 19th's raise briefs call test-only rows "TIER 1". That is the raise-brief review scale. On the QA-gate scale (2026-09-05 learning) tests-only is tier 2.
- *Rec / default:* the gate uses the QA scale (as kit.json does). Consider renaming the raise-brief scale so the two cannot be confused (a template change, not this gate's).

**Q-KEYS1449 — #1429's code carries 0 occurrences of KS-1449.**
- The two new test files are NAMED and KEYED `ks591-*` / `ks1364-*`: 8 hyphenated KS-591 and 12 KS-1364 in added lines, and describe names open `KS-591:`. The six `required: true` lines carry no comment at all.
- E 11th de-hyphenated both register keys in the COMMIT message on purpose, "so neither ticket attaches". In code they do not attach (STANDING_LINES :281), but SKILL §5d asks every changed line to carry WHY + the ticket.
- *Rec / default:* **Minor, not a blocker**; the gate rules it. If Wednesday wants it fixed, it is a one-commit follow-up (re-key the describe names / file headers to KS-1449 with the register keys de-hyphenated), never a reason to hold the other five rows.

**Q-UNNAMED — #1430 / #1431 bodies call the skipped preflight legs "unnamed".**
- The push logs name them: `s-f5-ks1328-d9928f4a8a4d-push.out:1650` (sha256/16 47830b52d185c422) and `s-f5-ks1355-d715e5dfbbf2-push.out:1653` (06ea46b93e640727) both read `legs 3 4 8 — local stack not up; you can clear this by starting it.` F 5th's READY repeats the false claim ("Neither push's output names WHICH three").
- *Rec / default:* a BODY-CORRECTION, polish, not a code defect. The gate corrects the SQUASH bodies to name legs 3 4 8. No PR-body PATCH.

**Q-SUBJ77 — squash subjects (staged in merge_inputs/).**
- #1430 and #1431: the PR titles read `KS 1328:` / `KS 1355:` (de-hyphenated) and the head subjects `test(KS-1328):` / `fix(KS-1355):`. Staged, re-hyphenated from the titles: `KS-1328: pin the kyc db-retry suite to a 60 s describe budget` (61) and `KS-1355: stack_guard lists a project once when its owners disagree` (66).
- The other four are their PR titles as-is (71, 82, 69, 82). All ASCII, <= 92, no `(#`.
- *Rec / default:* as staged; the gate's wording wins.

**Q-ATTR77 — attribution and foreign keys in the bodies.**
- `Generated with` lines are in the #1429, #1430, #1431 and #1434 bodies. #1429's body hyphenates KS-656 (it would ATTACH in a squash body).
- *Rec / default:* the squash bodies drop the attribution lines and de-hyphenate KS-656. No PR PATCH.

**Q-COMP77 — the Actions comparator.**
- base `0a6177ea5482` is no longer develop.
- *Rec / default:* **develop** (the develop read at launch), with base named where develop has no run of that workflow.

**Q-1433BASH — KS-1139's defect needs bash >= 4.1; the host has 3.2.57 and no other bash.**
- The suite's RED cells measure the counter statement's STATUS, which is version-independent. The drafter reproduced 3 passed, 3 failed on the base product, controls ok.
- The abort itself is unreproduced locally.
- *Rec / default:* the head's CI shell step (Linux, bash 5.x) is the only >= 4.1 witness. A live run stays OWED and KS-1139 does not move to Done. Docker is not the gate's to start.

**Q-1429LEG8 — preflight leg 8 (served-spec consistency, KS-656) is the leg #1429 most wants, and it is UNRUN (no stack).**
- *Rec / default:* a GO can carry it as a NAMED limitation. KS-1449 stays open, and leg 8 rides with the owed live run.

**Q-USAGE77 — no WED_USAGE_STOP override.**
- gate76's grant (2026-10-08 new-account) expired on its EVENT, the account renewal: `usage_gate.sh --check` read 1% at the default 90 at draft.
- *Rec / default:* the repin runs at the default and refuses rc 12 above it. A new override needs a new recorded grant from Kam.

**Q-PREFLIGHT77 — one preflight by hand on wtFinal (the SIM final tree)**, not one per head: the seats' in-hook runs at each head are on record.
- *Rec / default:* accept.

**Q-LIVE77 — runtime rows (#1429, #1431, #1432, #1433) each owe a live run.**
- *Rec / default:* none of KS-1449 / KS-1355 / KS-1410 / KS-1139 moves to Done on this merge. The tests-only rows (#1430, #1434) owe none of their own: KS-1328 is a pin, and KS-1171's live sweep is owed by the ticket, not this PR.

## WEDNESDAY'S RULINGS — (to be written by Wednesday)
