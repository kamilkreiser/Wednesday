# gate77 — RULINGS for Wednesday (drafted 2026-10-09 ~09:20–10:30 AEDT, 2026-10-08T22:20Z–23:30Z; NOT launched)

Every OPEN question carries the drafter's recommendation and a DEFAULT. The default is what kit.json and the prompt already assume, so ruling "as recommended" changes no file. **None blocks the dry run** (rc 0 at the defaults). Q-SEAT77, Q-ORDER77 and Q-MERGEINS77 bind the MERGE SEAT more than the gate.

## EXTENSION 2026-10-09 (~14:10 AEDT, extension drafter): a SEVENTH row, #1436 KS-808 (Seat F 6th, T2)
Full record: `KIT_REPORT_ADDENDUM_1436.md`. Backups of every changed file: `<name>.pre-1009-1436`. Every default below is what kit.json and the prompt now assume; ruling "as recommended" changes no file.
- **#1436 is a MERGE-IN row**, not one commit on the raise_base: head M `90d98754db7b`, parents [`a24efb3c5e04` (one commit on 1e7f90e26137), develop `81d2e5f4c415`]. The kit measures it from its own base 81d2e5f4c415 (`rows.1436.base`), adds c1 P2M (NO-EVIL-MERGE: merge-tree a24efb3c5e04 x 81d2e5f4c415 == M's tree 43a9d3089e19) and c2 BASE-CONTAINED (#1436 is refused onto a develop that lacks 81d2e5f4c415).
- **develop moved** 1e7f90e26137 -> `81d2e5f4c4151f5291a7a9c186d93a02dc5d38d6` (#1435, 5 package-lock.json files). The launch command keeps `--develop 1e7f90e26137…` and must carry `--repin-develop <origin develop at launch>`.
- **Q-ORDER77 (amended default):** `1432,1433,1429,1434,1436,1431,1430` (flow 36 37 38 40 **41** 42 43; T1 first). Predicted final trees at develop 81d2e5f4c415: with #1427 first `550d0ef42882fd861a9781622681094caa545bf8`, without `408cae8897302aea5ece58f4d0ff7831421d1265`.
- **Q-TIER808 — #1436 T2 or T1?** run-migrations.sh is a deploy-path script (the `migrations` image), the tier-1 class "anything deploying to dev or demo". But the diff moves ONLY a report counter (applied_count / skipped_count feed two echo lines); failed_count, the return codes, `exit 3` and all SQL are byte-unchanged, and no non-test, non-doc code reads `Summary: applied=`. *Rec / default:* **T2 + a mandatory EXIT-INVARIANT arm** (exit code + per-file lines identical base vs head over the four stub fixtures; drafter: rc 0 0 0 3 both sides). T1 if the gate finds any decision consuming applied=.
- **Q-SEAT77 (re-asked):** the default `Seat R 20th` predates R 22nd (live now, rebuilding #1427). Q-SEAT77's own rec is "whichever R seat merges #1427 merges gate77". *Rec:* if R 22nd lands #1427, put its ordinal (or its successor's) in kit.json `merge_seat_ordinal` before the repin. Not an author of any row (author_seats now include Seat F 6th).
- **Q-KEY1452 — the MERGE commit's subject hyphenates a foreign key** (`… (KS-1452 lock refresh in, no conflict)`), while F 6th's body spaces it on purpose ("would have linked #1436 to that ticket"). F 6th's board control read KS-1452 without #1436 afterwards. The squash replaces the commit message, so nothing lands. *Rec / default:* Minor, not a blocker. The gate reads whether the integration linked it.
- **Q-ERRTEXT808 — the runner's own ERROR text (:187-188) still says "the remaining applied=N-counts-skips defect is KS-808"**, and the diff leaves it in place. After this PR that sentence is false at runtime, the same class as a doc that states more than the code. *Rec / default:* the gate rules it. If it is Minor, it rides a one-line follow-up. Not a reason to hold the row.
- **Q-PROSE808:** seven prose sites still describe the old `applied=N` line. They are named in the body, not edited (no MD edits in this PR). *Rec / default:* accept as named, with a follow-up ticket.
- **Q-ATTR77 / Q-SUBJ77 / Q-LIVE77 extended:** #1436's body carries a `Generated with` line (drop it in the squash). The title is de-hyphenated `KS 808:`; it is staged as `KS-808: run-migrations.sh no longer counts skipped migrations as applied` (72). KS-808 does not move to Done: a live run is owed (a rebuilt `migrations` service against a real PostgreSQL with a skip).
- **Q-1427REBUILD:** R 22nd is rebuilding #1427 onto 81d2e5f4c415, and its M' is not pushed. The kit still pins #1427's OLD head `2b6da5f561b0` as the modelled step 1, and decides "landed" by the job-04 blob. If the rebuilt #1427 lands with a job-04 blob different from the old head's, the repin reads it as NOT landed and models the old head onto a develop that already moved job-04. CODE-UNMOVED then refuses rc 13. That refusal is SAFE: re-draft the pending pin, never force.

## CARRIED (binding on the gate, written into the prompt)
- **R1 TIER.** #1432 T1 (security surface: error-text disclosure on the public edge). #1429 #1430 #1431 #1433 #1434 #1436 T2. Reasons per row in kit.json `rows.<n>.tier_reason`. The gate may go UP, never down.
- **R2 ACTIONS.** SUBSET, never equality; PENDING never a pass; classify by WORKFLOW ID (three workflows are named `pr`). Security Scanning, PR Security Gates (KS-168) and pr-platform-suites fail on develop itself (R 19th, measured by id): base-state, classified, never a new red by default.
- **R3 PRE-EXISTING MISMATCH.** `VERDICT: MISMATCH — STOP` inside a green run is the F-925-3 fixture arm (gate73 R3, G 5th re-verified it as an asserted `expect` arm at preflight_deps.test.sh:459-460).
- **R4 PLATFORM SUITES** UNMEASURED locally, never counted as passing.
- **R5 MERGE SEAT** never an author (E 11th, F 5th, R 19th, G 5th, F 6th): the launcher refuses an author ordinal (rc 8).
- **R6 CONTROLS.** Every check can fail; every zero has a control; an arm counts only if it refuses at its OWN assert.
- **R7 RESTORE TO THE HEAD STATE**, never checkout / restore / reset / clean.
- **R8 Q-UNION (gate73, binding, re-measured on THIS batch).** `merge-file --union` leaves table/tr/td +1 open on the flow doc at every step and div/table/tr/td +1 on the cheat doc from step 3; keep-both composition is balanced at every step. **CORRECTED 2026-10-09 (extension drafter):** the six-row draft's own chain output (`_scratch/runs/dry_225602.c2chain.out`) shows union BALANCED on the flow doc at the #1434 and #1431 steps, so "every step" over-stated it. Re-measured on seven rows at 81d2e5f4c415 with #1427: flow +1 at 6 of 8 steps, cheat +1 at 4 of 8. The binding rule (never union) is unchanged.
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

## Wednesday's rulings on the #1436 addendum (14:3x 2026-10-09, after reading the drafter's report)
1. **Merge seat:** NOT R 20th. Named at launch, after #1427 lands (R 22nd is live on #1427 now). Edit `kit.json` `merge_seat` / `merge_seat_ordinal` then, before the repin.
2. **#1436 tier = TIER 1** (not 2): `run-migrations.sh` is on the deploy path, and the tiered gate gives deploys full weight. The batch already runs at T1 weight for #1432. Keep the mandatory exit-code-unchanged arm.
3. **`run-migrations.sh:187-188` stale "applied=N defect remains" text** and **the hyphenated KS-1452 in #1436's merge-commit subject:** input findings for the GATE to grade, not drafter verdicts.
4. **#1427 pin:** if the rebuilt #1427 lands with different job-04 bytes, rc 13 is the intended refusal; re-draft that one pin.
5. **Union-hazard correction** (6 of 8 steps on the flow doc, not "every step"): accepted.
6. **Q-SEAT77 RULED (15:2x):** merge seat = **Seat R 23rd** on `Secuura/Blockchain-R` (R 22nd merged #1427 as `349b35c9163a`, verified by Wednesday at source, and wraps; the R lane holds the keep-both merge-in tooling). `kit.json` `merge_seat_ordinal` edited (backup `kit.json.pre-1009-seat77`). R 22nd's handover is the source for R 23rd's tools.
