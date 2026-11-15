STARTABLE: YES (after Tuesday's stamp; five questions, each with a default that lets it start; Q-1 and Q-4 decide what the client tester sees, read them first)

# B1584 drafter report: HPSM-POC builder, lane P of the reviewer-feedback plan (F9, the assessor chooses how each answer is known), seat H167

Drafted 2026-11-15 17:30 to 17:40 AEDT (`date` printed 17:30:59, 17:31:26, 17:31:34, 17:33:52, 17:36:31, 17:39:47). Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1584_SEAT-H167_hpsmpoc-lane-p-answer-basis-chooser.md` (83 lines). Sidecar `...answer-basis-chooser.md.measured` (75 claims, 75 measured; `stamp_check.py <kit>` rc 0). Work folder `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s278/d1584/`.

## BLUF
- **What gets built.** The live snapshot card gets the scripted sample's existing "How do we know?" select. It sits inside the note's disclosure, offers the five existing words of `evidenceText()` (verified, observed, stated by the customer, assumed, not assessed) and is pre-filled with today's default. The choice is stored as the answer's `evidenceBasis`. The PDF already prints the stored basis (`ReportModelBuilder.cs:208`, `:414`), so the report, the API and the contract do not change. No new user-readable word.
- **A hidden gap the plan did not name.** `fromRecords` (`useSnapshot.ts:44`) never reads the stored basis back. A chooser alone would therefore lose the assessor's choice on the next save after a reload. DESIGN P1 carries the basis in the draft, and builds today's exact object for every record that holds the default. So existing `toEqual` tests are predicted to stay green.
- **The import rule is the one real fork (Q-1).** If an answer carries an import citation, the API refuses any basis other than `observed`/`verified` that matches the citation (`AssessmentEndpoints.cs:155`). A save without the citation deletes the provenance row (`Cite`, `:227`). Default: cited answers show no chooser and keep today's rule. The alternative is a data-removing path (row C4, Opus).
- **Scope is four product files, web only:** `questionnaire.ts` (one optional field), `useSnapshot.ts`, `QuestionCard.tsx` and `SnapshotRunner.tsx` (one prop). There are three new test files. The chooser is opt-in, so the client follow-up and the partner's review stay as they are (Q-4).
- **Partition:** none of the 7 paths is among b1577's 41 (by program). None is in lane N's or R's lists from the plan.
- Base `f32b209bfa6f33c3c0268c1daa76753c816b316e` (#319 landed), 0 open PRs, b1577 in its gate. Seat H167, pane `Datasec/HPSM-POC-H167`, branch `b1584/hpsmpoc-answer-basis-chooser`. Model Sonnet (`model-routing.md:92` C2), gate G1 (`:108`, client tester), id `claude-sonnet-5-5`. Ports 10000-10009, WEB 10002 / hosted 10003 / stub 10004 / chooser 10005. No containers unless Step 6d's program fires.

## Facts re-measured with instruments
- **Main** (`gh api branches/main`, 17:31): `f32b209b...`, committed 2026-11-15T05:04:28Z ("Give the accessibility journey test its own timeout...", which is H165's landing).
  - `pulls?state=open`: 0. Control `state=all&per_page=3`: 319, 318, 317 closed. `pulls/99999`: 404.
  - `matching-refs`: b1584, b1585 and b1586 are 0. b1577 is 1 (`fda88777`). Control b1541: 1.
  - `compare main...fda88777`: ahead 1, behind 0, 41 files. The commission says 41 paths; the plan said 43, from an earlier read.
- **The F9 code at main** (tarball; read whole: `useSnapshot.ts` 332 lines, `QuestionCard.tsx` 214, `QuestionBlock.tsx` 107, `plain-words.ts` 36):
  - `toWrite` at `:67` with its basis rule at `:70`.
  - `fromRecords` at `:44`. Lines 44-58 read `evidenceBasis` 0 times; control: lines 67-77 read it 4 times.
  - `NotesField` at `QuestionCard.tsx:200`, with its open state `useState(!!r.notes)` at `:203`.
  - `Disclosure` puts its children in `hidden={!open}` (`Disclosure.tsx:19`), so a closed chooser is invisible to `getByRole`.
  - `QuestionCard` has two other users: `ClientFollowUpScreen.tsx:193` and `ReviewAnswer.tsx:103`. `clientWrite` drops the basis (`followup/model.ts:35`).
- **API:**
  - `Requests.cs:103` and `:164` accept all five values.
  - With a citation, the basis must match it (`AssessmentEndpoints.cs:155`; the mock mirrors this at `mock/provenance.ts:28`).
  - `Cite` with no citation removes the held provenance row (`:227` onward, read).
  - `ProvenanceTests.cs:552` `Without_a_citation_every_basis_is_accepted_as_before` already pins all five values.
- **Report:** `ReportModelBuilder.cs:208` (Evidence column), `:371` (methodology line), `:414` (`asserted` printed as "stated by the customer"). The plan's pointers are confirmed.
- **Words:** `How do we know?` appears 0 times in `web/src/components/snapshot` and once in `QuestionBlock.tsx` (line 64). `evidenceText` is at `plain-words.ts:6-14`.
- **Do API or infra tests read a changed web file?** `grep -rl -i` over `api/` and `infra/` found 0 files each for `questionnaire\.ts|content/questionnaire`, `useSnapshot`, `QuestionCard` and `SnapshotRunner`. Control `web/src/content`: 3 files. This is why the kit runs `dotnet test` once but not the SQL Server parts, unless the seat's re-run fires (DRAFTER_RULES fence 8: infra still runs).
- **Ports:**
  - `lsof` on 10000-10009 found 0 listeners; the unfiltered list has 18.
  - The scan of 31 non-`.pre-` SEAT kits of 14-15 Nov hit 3 kits, none of them on a host port: B1563 and B1568 mention the number 10000 in NexusAI code, and B1565 uses Azurite's in-container `:10000`. Control: `992[0-9]` over B1577 hit 2.
  - Panes at 17:33: `%0 tuesday`, `%63 Datasec/MPS-M141`, `%54 Datasec/MPS-M140`, `%1 fleet-monitor`. No HPSM-POC pane is live.
  - Load 23.33, close to the gate of 24, so the seat should expect to wait.
- **Toolchains:** `.tools/dotnet-10.0.404/dotnet --version` gives 10.0.404. `.tools/node24/bin/node` gives v24.21.0 and npm gives 11.19.0. `global.json` 3-4 pins 10.0.404 with rollForward disable. `.nvmrc` reads 24. Disk: 1198 GiB free.
- **Other checks:**
  - CI pointers at f32b209b are on the same lines as B1577's: 87, 184, 252, 255, 303, 314, 396, 409, 413, 426, 478, 494, 518, 630.
  - `brief_seat.sh:31` is the default-Opus line.
  - CodeQL 2.27.4, with `javascript-queries/2.5.0` present.

## Census by program (frame: every `*.test.ts(x)` / `*.spec.ts` under `web/src` and `web/e2e` at f32b209b)
The program `census.py` found 184 rows in 49 files: BASIS 98, FN 36, NOTE 16, COMBO 34. Rows are in `census_rows.tsv`. Control: a planted `toWrite(` line in a scratch tree gave ROWS 1.

**Predicted REWRITE: none.** The reasons:
- P1 builds today's exact object whenever the stored basis is the default.
- P2 is opt-in, and only `SnapshotRunner` sets it.
- The chooser sits in a `hidden` region until the disclosure is opened.

Rows to watch:
- `SnapshotRunner.provenance.test.tsx`: FN 11, BASIS 16, NOTE 5. These are cited answers, which P1 leaves unchanged.
- `SnapshotRunner.refused.test.tsx` and `SnapshotRunner.test.tsx`.
- `playbook-snapshot.spec.ts:111-118`: the note round trip. It now opens a disclosure that also holds the select. `getByLabel("Consultant note")` is still unique.
- `playbook-invisible-characters.spec.ts:29`.
- `ClientFollowUpScreen.test.tsx` and `FollowUpPanel.test.tsx`: these must stay green untouched, which is the Q-4 proof.
- `mock-api.contract.test.ts`: the mock is unchanged.

The COMBO rows are all on other screens (customer, feedback, partner and others), so they are UNAFFECTED. The dynamic census in Step 4 decides; the verdicts here are readings of context, not runs.

## Chain table (rule 4)
| step | inputs | produced by |
|---|---|---|
| 0 | kit, project identity, the two `.tools` toolchains (exist, measured) | exist at BASE / on the box |
| 1 | `mut`, gh | step 0 |
| 2 | `mut` with npm ci; writes `base-unit.json`, `census.tsv` | step 0 |
| 3 | `head`; Q-answers (stamp) | step 0, stamp |
| 4 | `head` product files; a build (run inside step 4 before the Playwright specs) | step 3 |
| 5 | REWRITE list (steps 2, 4); `mut` for red-at-BASE runs | steps 2, 4 |
| 6 | `head` complete; `base-unit.json`; Step 6d's program | steps 2, 5 |
| 6e | CodeQL CLI and suite (on the box), the diff | step 5 |
| 7 | all green; b1577's file list (re-read by gh) | steps 4-6e |
| 8 | pushed sha, census files | steps 2, 4, 7 |

## D-decisions (made in the kit; Tuesday can reverse each at the stamp)
- D-1 **Words come from one function.** The option texts are `evidenceText(<id>)`, so the screen, the PDF and the finding screens always say the same thing. The label is the existing `How do we know?`. Check 7c lets no other added literal through.
- D-2 **Storage needs no API change.** `ResponseWrite` and `ResponseRecord` already carry `evidenceBasis`, and the mock already stores and returns it (`mock/api.ts:374`).
- D-3 **Keep the default object.** `fromRecords` adds `evidenceBasis` only for an uncited record that is not `asserted`, which keeps every existing equality assertion true.
- D-4 **A choice saves at once** (not delayed), as radios do. Before an answer exists, the choice is held locally and travels with the answer, as a note does today.
- D-5 **The disclosure opens at first** when a note exists or a non-default basis is held, so a chosen basis is never hidden on return.
- D-6 **CI scope.**
  - All eight e2e shards run, because the live card is on every playbook journey.
  - `dotnet test` runs once. The SQL Server parts are NOT RUN, with a measured reason that the seat re-measures.
  - Infra always runs (fence 8).
  - CodeQL runs for JavaScript/TypeScript only.
- D-7 **Ticket keys:** code comments may cite a ticket key in the house style. The commit message carries none. The F9 ticket is being created by B1583 now, so its key is unknown at drafting, and the kit names none.

## QUESTIONS FOR TUESDAY (each with a default)
- **Q-1 Answers drawn from an import.**
  - The plan says "an imported answer keeps its observed or verified source unless the person changes it".
  - The API allows only the citation's own basis while the citation is sent (`AssessmentEndpoints.cs:155`). A change to another basis would have to drop the citation, and the API then deletes the provenance row (`Cite`, `:227`).
  - **Default (a):** a cited answer shows no chooser and keeps today's rule. That needs no new word and no destroying path, and it fits row C2.
  - (b): show the chooser, and let a different choice drop the citation. That is a destroying path (row C4, Opus builder) and arguably needs words that warn about it.
- **Q-2 Option texts in lower case.** `evidenceText()` returns lower-case words ("stated by the customer"), because they sit mid-sentence in the PDF.
  - **Default:** use them byte for byte as the five option texts, so the screen equals the PDF.
  - Alternative: capitalise the first letter on screen. That is arguably new text, so it would need the product owner's word.
- **Q-3 The plan's optional words sub-item** (changing the default's words to "stated, not checked").
  - The 17:16 ruling's last clause confirms that the label prints. It does not choose new words.
  - **Default:** the words stay, no report file is touched, and the PR body lists it as NOT BUILT.
  - If Tuesday reads the ruling otherwise, it is a word card to the product owner first, and lane P would then touch `ReportModelBuilder.cs` (lane R does not).
- **Q-4 Where the chooser appears.**
  - **Default:** only on the assessor's live card (`SnapshotRunner`).
  - It does not appear on the client follow-up, where the customer answers and the partner sets the basis on acceptance (`model.ts:35`), or on the partner's review card (`ReviewAnswer.tsx:103`).
  - The alternative widens lane P into `followup/**` and the follow-up API's basis rules.
- **Q-5 The disclosure's summary still reads "Add a note" / "Edit note"**, although it now also holds the chooser. The reviewer asked for it to be nested under notes.
  - **Default:** keep the summary text, because a new summary would be a new word.
  - If Tuesday wants the summary to name both, that is a word card.

## UNMEASURED
- Everything the seat runs. The drafter ran no build, test, browser or CodeQL. In particular:
  - the Step 4 red set (predicted empty);
  - whether `playbook-snapshot.spec.ts` stays green with the select inside the opened disclosure;
  - the a11y scan of the opened disclosure;
  - where `--check-shards` places the new spec (DERIVED: once per playbook project's halves).
- The census verdicts are readings of context.
- The lane N and lane R file lists are RELAYED from the plan's section 3. The B1585 and B1586 kits did not exist when the drafter listed the briefs folder.
- The landing-rule quote (CLARIFICATIONS line 3617) and the hosted CodeQL language list are RELAYED from the B1577 kit.
- The F9 ticket key (B1583 is creating it).

## Outside-the-fences disclosure
Reads:
- `DRAFTER_RULES.md`, the commission, the plan folder (ACTION-PLAN, FEEDBACK, RESULT, COMMISSION-ACTION-PLAN).
- The B1577 kit, drafter report, ANSWER-1 and sidecar (for its style).
- `model-routing.md` (grep), `models_latest.json` (grep), `brief_seat.sh` (grep of its level lines), the `stamp_check.py` header.
- The kit filenames in `briefs/`, for the port scan.
- `gh api -X GET` under the project's `GH_CONFIG_DIR`: main, pulls, matching-refs, compare, the b1577 commit's file list, recent commits, and the tarball of f32b209b.

Local runs, in my work folder only: tarball extraction, the census program and its control, the partition check, `lsof`, `tmux list-panes`, `uptime`, `df`, and the `--version` of the two `.tools` binaries and of CodeQL.

Writes: only the kit, its sidecar (made by `stamp_check.py --init`, then filled by my script `fill.py`), this report, and scratch files under `s278/d1584/`.

Not done:
- No card read (the 17:16 ruling is quoted from the commission; I was not given an exact card id) and no `decision_queue.sh list`.
- No Jira read or write; no git or GitHub write.
- No file under `/Volumes/Datasec_DEV/!CODING/` written; the `.tools` binaries were run for `--version` only.
- No message, no az, no docker; nothing deployed.
- No `_ledger.md`, and no WEDNESDAY, FRIDAY or non-Datasec tree.

DRAFTED B1584: kit 83 lines, sidecar rc 0, questions 5
