STARTABLE: YES (after Tuesday's stamp. All four tickets have their words: F1 and F4 are ruled verbatim, F5+F6 needs no new word, and F7 is Tuesday's recorded reading (Q-1, default build). Six questions follow, each with a default that lets the seat start. Q-1 and Q-4 change what the client tester sees, so read them first.)

# B1597 drafter report: HPSM-POC builder, lane Q of the reviewer feedback (HPSMPOC-485, -487, -488, -489), seat H170

Drafted 2026-11-15 from 22:31 to 22:5x AEDT (`date` printed 22:31:22, 22:32:29, 22:41:09, 22:41:32, 22:44:21, 22:48:17).
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1597_SEAT-H170_hpsmpoc-lane-q-question-set.md` (89 lines).
- Sidecar: `...lane-q-question-set.md.measured` (62 claims, all measured; `stamp_check.py <kit>` rc 0).
- Work folder: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s280/d1597/`.

## BLUF
- **One new question-set version: ruleset 0.1.4 and package 0.7.2.** Both are made by program from 0.1.3 / 0.7.1 (the industry field version that landed as #320, `f4e79a7a`). They carry four changes:
  - F5+F6: the new order. Inventory first; held release becomes the 9th question and sign-in the 10th.
  - F7: the reviewer's two sentences on Q-CS-05 and Q-CS-07.
  - F1: Q-CS-01 gains `partly`, scored 50. R-001 now fires on it too.
  - F4: Q-CS-06 gains `compensating`, scored 100. R-006 is unchanged, so it raises no finding. It also gets the ruled help line.
  - Still 16 questions, with the same ids, weights and sections. The drafter's program checked this on its prototype.
- **A hidden rule the plan missed: A05.** `validate.ts:109` (and the API loader) refuse a set whose sections do not run audience by audience in the declared `audiences` order. Moving Identity & access ahead of Network (the ticket's "section moves from 3rd to 2nd") therefore also reorders the `audiences` list to PF, IA, NW, GR, SO. As a result, the "Show questions for" filter lists Identity & access before Network.
  - The drafter's A05 re-implementation printed `['S2']` violations on a prototype without the reorder (the control), and `[]` with it.
  - The live-API spec pins the old filter order (`playbook-content-050-live-api.spec.ts:58-60`). It is a REWRITE row.
- **The prototype's hashes are in the kit for the seat to match:**
  - 0.1.4: canonical `sha256:774164cc...14ad`, file `6afb1222...`, 29 diff lines.
  - 0.7.2: canonical `sha256:5173dcd4...af82`, file `76670e23...`, 80 diff lines.
  - Deep-diff: 11 paths and 15 paths. The kit lists each one by name.
- **F7's words are not on the ticket.** HPSMPOC-489 has 0 comments. Its description says only "This puts the reviewer's two sentences in, verbatim". C-373 records the reading ("read as approved words"). The sentences exist only in Tuesday's `FEEDBACK.md:11`, and the seat extracts them from there by program. That is why Q-1 exists.
- **One product code change beyond content:** the result recap counts Unsure only for `yes-no-unsure` questions (`SnapshotResult.tsx:34,37`). Q-CS-01 and Q-CS-06 become single-choice, so the count must go by answer id (Q-3).
- **Partition: 0 shared paths, proved by program.**
  - Lane Q's 46 candidate paths against lane N's 13 OWNED entries: 0 shared (control 1).
  - Against PR #322's 11 paths: 0 shared (control 1).
  - #322 landed at 22:40 while I drafted, so BASE is now `a9e0052f`. The `d607c8fb...a9e0052f` compare is exactly #322's 11 files, and the census is identical at both.
- **The known flaky test** (`ForwardedProofTests...is_gone...`) has its own section. A red of only that test is not lane Q's: the seat records it, runs it five times at BASE and head, and never edits `Hosting/`.
- **Routing:**
  - Model Sonnet: `model-routing.md:92`, row C2. Gate G1: `model-routing.md:108`, "anything handed to a client tester". Id `claude-sonnet-5-5` (`models_latest.json:23`).
  - The drafter's own row: C8 at `model-routing.md:98`.
  - Seat H170, ports 10120-10129, branch `b1597/hpsmpoc-lane-q-question-set`. Nothing deployed.

## Facts re-measured with instruments
- **Main.**
  - `gh api branches/main` gave `d607c8fb...` at 22:31, then `a9e0052fe2f4e861a9571732d1eaa707b2968087` at 22:41 (commit 11:39:52Z, one parent `d607c8fb`). The 22:40 daily note shows #322 landed.
  - Open PRs: 0 at 22:41. At 22:31 there was 1 (#322, head `78680128`).
  - `pulls/99999` returned 404. `matching-refs/heads/b1597` returned 0 and `heads/b1585` returned 0, so lane N has not pushed. Control `heads/b1541` returned 1.
  - The b1577 landing is `f4e79a7a`: 41 files, parent `f32b209b`.
- **Tickets** (my GET-only copy of the B1577 drafter's `jget.py`; the token was read in-process and never printed):
  - 485, 487, 488 and 489 are all Backlog, created 18:11-18:12. Comments total 0 on each; control HPSMPOC-168 has 2.
  - 485 and 487 still read "Awaiting the product owner's words … not yet approved". This is records debt; see FOR TUESDAY.
  - 488 holds the 16-position order verbatim. 489 holds the reading, but not the sentences.
- **Cards** (`decision_queue.sh show <exact id>` into scratch; each id appears 1 time):
  - `hpsmpoc-q1-partly-answer-1115`: ruled, `choice='a'`, `ruled_ts=2026-11-15T19:32:32`.
  - `hpsmpoc-q5-covered-another-way-1115`: ruled, `choice='a'`, `ruled_ts=19:32:44`.
  - `hpsmpoc-narrative-reedit-migration-1115`: read; not this lane's.
  - The store's ruled_ts (19:32) differs from the board clock Tuesday quotes (18:30). The option texts equal the brief's quotes byte for byte.
  - The F4 help line on the card has no quotes around Covered another way. The kit copies the card exactly. The plan's version had quotes there; the card's does not.
- **Clarifications:**
  - The analysis repo origin main is `b7500c93` (`gh api`; the local checkout's deploy key path is not accessible, so I did not use it). C-373 is the last entry (382 `### C-` headings).
  - The landing rule is at `:3617` ("The landing form is a head-pinned squash"). The standing HP-tools line is at `:2676`.
- **Content, at a9e0052f:**
  - Both 0.7.1 and 0.1.3 round-trip byte-identical, and web equals seed (`cmp`). The canonical recipe reproduces `registry.ts:31` and `PROVENANCE.md:16`.
  - 0.7.1 has 16 `"type": "yes-no-unsure"` lines; the prototype 0.7.2 has 14 (two converted).
  - The ruleset already scores single-choice options (`answerOptions` yes/no/unsure at `:907`). Package options take `{id,label,help}` (schema `$defs.option`), ruleset options take `{id,label,score}` (`answerOption`), and labels may be up to 200 characters.
  - The `Yes`/`No`/`Unsure` labels are `adapt.ts:9`.
- **PROVENANCE.md:14** still says "Named by the hosted demo"; the phrase is on 1 line of the file. This is the gate's F1, still true at a9e0052f.
- **Toolchains** (by path): dotnet `10.0.404`, node `v24.21.0`, and bicep present under `HPSM-POC/.tools/`. `brief_seat.sh:31` defaults to Opus.
- **Ports:**
  - `lsof` on 10120-10129 gave 0; the unfiltered list gave 16.
  - A scan of the 14-15 Nov briefs, today's and yesterday's notes and verdicts gave 0. Control `1001x` gave 11.
  - Taken elsewhere: 10050-10059 (B1582 gate) and 10060-10069 (B1578 gate), so I skipped them.
  - Panes at 22:41: tuesday, NexusAI-N134, MPS-M142, HPSM-POC-H168, fleet-monitor, plus unnamed panes. Load 8.65.
- **CI pointers:** unchanged from B1577's at a9e0052f (87, 184, 252, 255, 303, 314, 396, 409, 413, 426, 478, 494, 518, 630). `ci.yml:252` includes `Hosting.` in the api-assessment SQL Server part, which is where the flake runs.

## Census by program
Frame: every file of the a9e0052f tarball except the four versioned-content folders; 1499 files.
- Program: `scripts/census.py`. Rows: `census_rows2.tsv`. Verdicts per file: `census_verdicts.tsv`.
- **180 rows in 47 files:** R013 66, P071 76, TEXT 1, HELP 1, QID 28, COUNT 4, KIND 4. The planted control printed 1 row. The result is identical at d607c8fb.
- **REWRITE: 33 files, 149 rows.** That is every non-versioned file of `f4e79a7a`'s list in its same role, plus:
  - the three `8` seeded-package pins and `19 client copies`;
  - `SnapshotResult.tsx`;
  - the live-API spec `:56` / `:58-60`.
- **UNAFFECTED: 14 files, 31 rows:**
  - `package-lock.json` (dependency ranges `^0.1.3` / `^0.7.1`);
  - Golden inputs and README (they score 0.1.2 by question id);
  - `Content061Tests.cs` (0.6.1's own help lines);
  - `stamped-set.test.ts` (0.5.0);
  - `InternalNotesScanTests.cs` (derives its pins);
  - `_superseded/`;
  - `server/mock/readiness.ts`;
  - `QuestionCard.tsx` (D4);
  - the Reporting fixtures PROVENANCE;
  - two 0.1.3 comments about the four-choice field (still true).
- `ShowcaseSeeder.cs`: `:91` is REWRITE, and its answer rows are UNAFFECTED.
- These verdicts are my reading of each line, not runs. The kit's Step 4 dynamic census decides. I expect e2e specs that walk the snapshot by position to appear there; my static patterns cannot see them.

## Chain table (rule 4)
| step | inputs | produced by |
|---|---|---|
| 0 | kit, project identity, the `.tools` toolchains, docker, pinned MSSQL image, FEEDBACK.md:11 | exist at BASE / on the box (the drafter checked the toolchain versions, not docker) |
| 1 | `mut`, gh, lane N kit | step 0; exists |
| 2 | `mut` with npm ci, dotnet restore, Azurite; writes `base-unit.json`, `base.trx`, `census.tsv` | step 0 |
| 3 | `head`; the 0.1.3 and 0.7.1 sources (BASE); `words.json`; Q-answers (stamp) | steps 0, stamp |
| 4 | `head` product files and a build | step 3 (build listed inside step 4 before the Playwright run) |
| 5 | REWRITE list (steps 2 and 4), `mut` for red-at-BASE runs | steps 2, 4 |
| 6 | `head` complete; `base-unit.json`; containers (started in 2 / 6d) | steps 2, 5 |
| 6e | CodeQL CLI (on the box), the diff | step 5 |
| 7 | all green | steps 4-6e |
| 8 | pushed sha, census files | steps 2, 4, 7 |

## D-decisions (made in the kit; Tuesday can reverse each at the stamp)
- **D-1 New versions, never edits.** 0.1.4 and 0.7.2 are made by program. There is a no-edit round-trip control and a named-path deep-diff (11 / 15 paths). No text, weight, severity, bucket, recommendation, provenance or note changes beyond the listed paths.
- **D-2 Option ids `partly` and `compensating`,** placed right after `yes` (the F1 ruling says "between Yes and No"). Scores 50 / 100. R-001 gets `partly` added; R-006 is unchanged. `targetOptionId` stays `yes`.
- **D-3 Audience order becomes PF, IA, NW, GR, SO** (rule A05). Without it the ticket's order cannot load.
- **D-4 Readiness stays on 0.7.0** (as at #320). The showcase seed moves to 0.7.2. The hosted pin trio moves to 0.1.4 together.
- **D-5 PROVENANCE:** the "Named by the hosted demo" sentence moves from the 0.1.2 row to the new 0.1.4 row, so it stays on exactly one line.
- **D-6 The commit message carries no ticket key.** Added code comments may cite the four keys (house style). The seat's name scan runs over genuinely new lines only: copied provenance lines carry names already on main (the B1577 gate's F4).

## QUESTIONS FOR TUESDAY (each with a default)
- **Q-1 F7: build the reviewer's two sentences (W4, W5)?**
  - They are Tuesday's recorded reading (C-373; HPSMPOC-489's description), not a quoted ruling. HPSMPOC-489 does not quote them; the source is `FEEDBACK.md:11`.
  - Default: **yes**, byte for byte, keeping "e.g.," and US "color".
  - If no: drop W4/W5 and the two `text` paths from D1. The deep-diff becomes 9 / 13 paths, and the hashes change, so the seat re-prints them and the kit's four values no longer apply.
- **Q-2 Where the `compensating` option sits.** The F4 ruling does not say. Default: right after Yes, mirroring F1, so it reads Yes / Covered another way / No / Unsure.
- **Q-3 May lane Q edit `web/src/components/snapshot/SnapshotResult.tsx:34,37`?**
  - That folder was lane P's (landed #321), and lane N lists it as NOT its own.
  - Default: **yes, those two lines only.** Without the edit, an Unsure on Q-CS-01 or Q-CS-06 stops counting on the recap.
- **Q-4 Visible layout effects, both without new words:**
  - (a) Q-CS-01 and Q-CS-06 render as a stacked column of four radios instead of inline buttons (`QuestionCard.tsx:106`).
  - (b) The audience filter and the runner's audience grouping list Identity & access before Network (A05).
  - Default: accept both. No `QuestionCard.tsx` edit; both effects go in the PR body.
- **Q-5 Deploy notes (D6).** Measured by the seat and stated in the PR body:
  - in-progress 0.7.1 snapshots stop scoring once the hosted setting names 0.1.4;
  - the API and the setting must ship together (start-up refuses in both directions);
  - the in-progress sample stays on 0.7.1 until a reset;
  - S1's PDF finding order follows the new question order.
  - Default: accept. The deploy is the single later round after all feedback lanes land (the 19:16 note), not this kit.
- **Q-6 Model and window.** Default: Sonnet (C2), with a G1 Opus gate (round 1 of 2). READY target 360 minutes after Step 0, one window, with the context band and handover form. The size is about 46 files on the 41-file precedent.

## FOR TUESDAY (not questions)
- **Records debt (not this kit):**
  - HPSMPOC-485 and -487 descriptions still say "Awaiting the product owner's words … not yet approved". The F1 and F4 rulings are not recorded on them.
  - HPSMPOC-489 has no comment quoting the two sentences.
  - The PROVENANCE fix and the flaky-test fix ticket are already listed as OWED in the pickup.
- **The plan's F5 text** says "the Identity & access section moves from 3rd to 2nd". It needs the audience reorder (D-3) that the plan did not name. The ticket text stays true.
- **Card times:** the store's `ruled_ts` reads 19:32:32 / 19:32:44 for q1 / q5, against the board's 18:30:12 / 18:30:07 that Tuesday quotes. The kit quotes no clock for those two.

## UNMEASURED
- **Everything the seat runs.** The drafter ran no build, no test, no browser, no container and no CodeQL. In particular:
  - the Step 4 red set: the census predicts it, nobody has run it;
  - whether Ajv and the API loader accept 0.7.2. JSON Schema was not run (no `jsonschema` module), but the shapes match `$defs.option` and `answerOption`, and A05 and X4 were checked by my own re-implementation (A05) and by reading (X4);
  - the client-copy count after the change (DERIVED 21);
  - where the PDF prints W1 for a `partly` finding (`ReportModelBuilder.cs`, not read this session; the plan says `:208`);
  - whether CodeQL C# can extract on this machine (the B1577 gate said it cannot).
- **Relayed, not re-read:** the hosted CodeQL language set, and the flaky test's red rates (B1577 gate, and Tuesday's tonight).
- **Partition:** checked against lane N's KIT (OWNED entries plus its census REWRITE files). Lane N's real diff does not exist yet; REFUSE 5 makes the seat re-check it if lane N pushes.

## Outside-the-fences disclosure
**Reads:**
- Briefs and plans: the WAVE-1800 common file, `DRAFTER_RULES.md`, the B1577 kit (and the `.pre-stamp` Stamp section), the B1577 drafter report and gate verdict, ACTION-PLAN.md, FEEDBACK.md, the B1585 kit (partition, ports and census lines), and the B1584 / B1586 kits (port lines only, by grep).
- Routing and launch: `model-routing.md`, `models_latest.json`, `brief_seat.sh` (grep), the `stamp_check.py` header.
- Notes, by grep only: today's note and the pickup.
- Cards: three, by `decision_queue.sh show <exact id>` into scratch.
- Jira: four tickets by GET and comment totals for five, through my GET-only copies (`jget.py`, `jcount.py`). The credentials were read in-process from the project `.env` and never printed.
- `gh api -X GET` under the project's `GH_CONFIG_DIR`: main, pulls, PR #322 files, matching-refs, compares, the branch list, commit `f4e79a7a`, the two main tarballs, and the analysis repo's main and CLARIFICATIONS.md (raw).
- Local: one `git ls-remote` attempt from the analysis checkout (it failed on its key; a read verb), and the project's `git config user.*`.

**Local runs, in my work folder only:** tarball extraction; the census; the prototype writer (`proto3/`; the earlier prototypes are moved to `_quarantine/`); deep-diff, A05, round-trip and hash checks; `lsof`, `tmux list-panes`, `uptime`, toolchain `--version`.

**Writes:** only the kit, its sidecar (`--init`, then filled by my script) and this report, besides those scratch files.

**Not touched:**
- no `decision_queue.sh list`;
- no Jira write;
- no git or GitHub write;
- no file under `/Volumes/Datasec_DEV/!CODING/`;
- no message, no tmux send-keys, no az, no docker;
- nothing deployed;
- no `_ledger.md`, no WEDNESDAY, FRIDAY or non-Datasec tree;
- nothing published.

One read went wider than its target: a background grep scanned the whole `*_verify` folders, work trees included, for a port pattern. It only read files.

DRAFTED B1597: kit 89 lines, sidecar rc 0, questions 6
