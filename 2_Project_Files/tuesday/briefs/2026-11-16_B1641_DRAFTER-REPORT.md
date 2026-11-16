STARTABLE: YES (after the stamp; 2 questions below, each with a default the kit already assumes)

# B1641 drafter report: MPS Commercial Calculator, lane M-S2, the dev stub's follow-up pins and the shared refusal titles (seat M152, MPSCALC-408)

Drafted 2026-11-16 from 21:54 to about 22:06 AEDT (`date` printed 21:54:35, 21:54:48, 21:55:23, 21:55:35, 21:57:25, 21:58:33, 21:58:41, 21:59:13, 22:00:11, 22:03:19, 22:03:48 and 22:04:26). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1641_SEAT-M152_mps-lane-ms2-stub-followups.md` (86 lines, 12 stamp slots left as four underscores) with sidecar `.measured` (105 lines, tags M00 to M15; about 33 are INSTRUCTION lines in the form of B1617's sidecar). `stamp_check.py <kit>` rc 0 (105 claims, 105 measured, 0 not measured). Scratch and every instrument: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s284/b1641/` (`meas.sh` and `meas.log`, `mut.py`, `mutlog.sh` and `mut.log`, `rowsA.ts`, `rowsB.ts`, `purchaseQuotesB.ts`, `plant.diff`, `jira.txt`, `prs.jsonl`, `build_kit.py`, `compose.py`).

## BLUF
- **Lane M-S2 fits one Sonnet seat in two parts, two commits, on one new branch `b1641/mps-lane-ms2-stub-followups`, paths only under `web/src/api/stub/`.** Part A = items 1 and 2 of MPSCALC-408, tests only (three new rows: control codes 31 and 159; an explicit null target GP counts as absent). Part B = item 3: the three refusal titles written once as constants (`guarded` and `requireCopyable` share them; seven literal lines rewritten, no word changes) plus one comparing row (the update path's words are asserted by no row today).
- **Everything in the kit was run on a scratch copy of main `56bfe232`** (a tarball of the sha, `npm ci --offline` rc 0): at main 146 files, 1610 tests (stub file 122, `client.duplicate.test.ts` 8); with Part A 1613; with Part A and B 1616; eslint and `tsc -b` rc 0 in all three states; 10 mutants each killed by exactly the rows the kit predicts (table in the kit's FACT 5).
- **Both Sonnet-row facts hold:** C2 (`model-routing.md:92`; Part B edits a non-test file), gate G2 (`:109`), `BRIEF_SEAT_LEVEL=sonnet` inside the quotes. Target READY Step 0 + 90 minutes, Part A pushed by +45. No port, no browser step (the gate runs them).
- **The ticket's pointers are all still right at today's main** (`:289`, `:295`, `:316`, `:318`, `:320`, `:321`, `:87`, `:95`, `:99`, `:101`): nothing needed re-pointing, unlike B1617's.

## Facts re-measured (instrument and control in the sidecar)
- Main `56bfe232cbf4c98a9752f949f1f279d755565750` (#205), open PRs 0 (205 PRs paginated; #72, #181, #201 present), `heads/b1641` 0 rows (control `heads/b1617` 1). MPSCALC-408 Backlog, 0 comments (controls: 361 Done; 404 shows its comment). No PR names 408 (control: #201 names 404). The six origin branches touching the stub are each the head of a merged PR (#55, #109, #111, #114, #193, #201).
- The three titles exist 2, 2 and 3 times in `purchaseQuotes.ts` (`:95/:316`, `:99/:318`, `:101/:320/:321`) and in no other file under `web/src` but the test file's `INTERNAL_WORDS`, `MANUAL_WORDS`, `PRICE_WORDS`. A fourth text (the Seller-role title) is also twice (`:88`, `:326`).
- No row names code 31 or 159 (`grep -c` 0; control `, 160]` 1) and none stores a null target GP (0; control `targetGrossMargin` 2). The update path's refusal words are asserted by no row (the only use of the three `*_WORDS` is the Duplicate row's `toContain(words)` at `:879`); that is why Part B adds a comparing row in addition to the constants.
- Disjoint from the siblings: M-F owns `tests/MpsCalc.Api.Tests/FleetLineIdTests.cs`, M-E2 owns `web/e2e/dashboard-390.spec.ts`; this lane owns two files under `web/src/api/stub/`. The one coupling (the 390 px spec runs against this stub) is stated in FACT 11: this lane changes no stub answer.
- Held and dropped check (rule 3): the pickup `0_Brain/tasks/NEXT-PICKUP-TUESDAY.md` holds no MPSCALC-408 line (its `408` hits are HPSMPOC-408 and other contexts); the 11-16 daily note names MPSCALC-408 only as a candidate (lines 134, 139, 140). No hold, no drop.

## Chain inputs (rule 4: each step's inputs and where they come from)
| Step | Inputs | Produced by / exists at |
|---|---|---|
| 0 | the kit copy, Stamp slots | Tuesday's stamp; `Briefs/` exists in the project |
| 1 | base sha, ticket, PR and branch lists, clone, node, baseline names list | origin main (S2), Jira GET, `gh api -X GET`, the machine npm cache |
| 2 | predictions file | Step 1's baseline and FACT 5 |
| 3 (Part A) | `stubApi.test.ts` at base: `expectRefusedRef` `:945`, `analystHeld` `:864`, `PLAIN` `:845`, `DRAFT` | exist at base (printed) |
| 4 (Part B) | Part A's pushed commit; `purchaseQuotes.ts` at base; fixtures `TARGET` `:846`, `MANUAL_LINE` `:848`, `FIXED_RATE` `:850`, `PURCHASE` `:615`, `stubAs` `:608`, `rejection` `:35` | Part A (the rows) and base (the rest) |
| 5-7 | the diff, the commit, the push | steps 3 and 4 |

## D-decisions (mine, in the kit)
- **D1:** item 3 is built as BOTH the shared constants and a comparing row, although the ticket accepts either: the constants make a change to one copy impossible, and the row pins what an update tells a Seller, which no row pinned. The one-sentence option is Q1's alternative.
- **D2:** the survivor `if (target)` (a truthy test; a numeric `0` target) is NAMED in the kit and left unbuilt: the ticket asks for null only and says no existing row is to change. The seat reports it in FOR TUESDAY.
- **D3:** only the ticket's two codes (31 and 159) are added, not 126, 128 or 158: the plant measured that the other directions of both bounds are already killed by the existing 32 and 160 rows and that moving `127` is killed by the existing DEL row.
- **D4:** the null row's `null as unknown as string` cast is told to the seat (the generated type `DecimalInput: number | string` has no null) with its non-vacuity proof (the stored JSON holds `"targetGrossMargin":null`).
- **D5:** the rows are placed by anchors (`:992`/`:994` for Part A, the end of the block `:1022` for Part B) and described by shape; the plant text is a readable claim in the scratch folder, not pasted into the kit, so the seat writes its own rows and its own names.

## Q-questions for Tuesday (each with a default the kit assumes)
- **Q1:** build item 3 as shared constants plus the comparing row (the default), or record the one-sentence "two copies are accepted" option? Default: constants plus row (the builder of #201 named the gap and was forbidden the constant; the ticket offers both). If Tuesday says sentence-only, Part B is that sentence in a `purchaseQuotes.ts` comment and READY says so.
- **Q2:** the fourth duplicated text ("Editing a draft needs the Seller role. (stub)", `purchaseQuotes.ts:88` and `:326`) is not one of the ticket's three. Default: reported in FOR TUESDAY, not shared, not edited.

## UNMEASURED
- The seat's own wall-clock for Part A and B, and whether the machine stays under the load gate (load1 was 7.9 to 11.0 during drafting, under 24 on every read).
- The entra build and bundle check at the head of Part B and the CodeQL pre-scan (named for the seat; the drafter ran neither). Both browser steps (the gate's).
- Whether the comparing row's update-path fixture (a Seller `updateDraft` at revision 1 of a Seller-created held quote) stays green if main moves under `stubApi.ts` before the seat starts: the kit's Step 7 re-reads main for that path.
- Node 24 (CI): every drafter run was node v26.13.0.
- The hosted CI of the squash and CodeQL for this lane (Tuesday's, after the PR).

## Outside-the-fences disclosure
- Read-only reads only: Jira GET through a copy of `fleet/state/s284/sweep2150/jdesc.py` (the sweep agent's helper, copied into my own scratch folder as the rules ask; it reads the project `.env` in-process, token never printed); `gh api -X GET` for refs, pulls, branches, compare, file contents and ONE tarball of main (GET); `tmux list-panes`; `uptime`; `df`.
- Writes: the kit, its sidecar, this report, and my scratch folder `fleet/state/s284/b1641/` (including an extracted tarball of main, `npm ci --offline --ignore-scripts` rc 0 into it from the machine cache, and plant edits made in that scratch copy only, each undone by `cmp` against the raw file; last `cmp` printed `restored`). The first `--init` sidecar was moved to `measured.todo.bak` in the scratch folder when I rebuilt the kit; the sidecar beside the kit is the final one.
- One slip: a one-line probe output went to `/tmp/x` (a stray file outside the allowed paths; empty of any secret; removed with `rm -f` of my own file the same minute). No push, no PR, no Jira write, no mail, no board, no `az`, no deploy, no `cd`, no listener, no token printed, no `.local`, no ledger read, no Artifact tool, no `decision_queue.sh` call at all (no card was needed: the ticket carries the words).
- The HPSM standing line is not in this kit (an MPS lane).

DRAFTED B1641: kit 86 lines, sidecar rc 0, questions 2
