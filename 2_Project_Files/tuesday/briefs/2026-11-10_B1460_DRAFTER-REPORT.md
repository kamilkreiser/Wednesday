STARTABLE: NO until all of these are done: (1) the step-10-reword and readiness-hub PR has landed and CI is green at its squash; (2) the stamp is done: `@TARGET@` and `@READINESS@` are filled, slots S1, S2 and S5-S14 are filled, and the READ-WHOLE line is filled; (3) the D57 pane is closed. After that the kit is YES. See Q-1 to Q-4.

# B1460 DRAFTER REPORT: SEAT-D58, HPSM-POC UAT deploy of main at `@TARGET@` as a delta on 884fd72b

**Files:**
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_B1460_SEAT-D58_hpsmpoc-uat-deploy-main.md`. At 09:33:50 AEDT it was 630 lines, sha256 `3c8e642f90326e49d5d9e512c58c80f7518e73d2edfae71e695596ee80bc75fe`. Lines holding four underscores: 13 (S1, S2, S5-S14, and the last line). Lines with five or more: 0. Slot tokens: `@TARGET@` x2 (the intro and S4), `@READINESS@` x2 (D-13 (R) and S15). The last line is `READ-WHOLE-BY-TUESDAY: ____`. The digest was taken after the drafter's last edit; Tuesday re-prints it at the stamp.
- Words file (written FIRST): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_B1460_WORDS-FOR-KAM.md`, 54 lines, sha256 `c272e013d5fd4e1ce253a8797b6c7c125f9a09a80b019f5a60ccb105178d9c8f` at 09:33:50.

## BLUF
- **This deploy is NOT web-only.**
  - **API product code:** `884fd72b...0820efe9` holds one API product change: `api/src/HpsmPoc.Modules.Assessment/Endpoints/ReportingEndpoints.cs` +6/-0 (#302, HPSMPOC-436). It refuses a finding explanation of no visible finding with a 422 `narrative.no-findings`.
  - **infra:** one `infra/` path, which is a test only (`infra/tests/test_ci_workflow.py`).
  - **Not in the range:** any migration, `.github/`, `scripts/`, `package*.json`, `*.csproj` or `appsettings` path.
  - **How the kit handles this:** the API package property becomes "Modules.Assessment carries code; the other 4 DLLs are stamp-only; every non-DLL file is equal". It adds a user-string proof in the DLL, a CI test-result count for `Hpsmpoc436`, and a local-pair 422 proof. It never exercises this on UAT, because a narrative request is a write.
- **Only one change in the range is visible to UAT users: the step 10 caveat (#299).** Main's version (`steps.ts:130` at `0820efe9`) still says "score the assessment and approve the narrative before you show it". That is the wording the 09:13 census says was ruled out at 09:03. The pending PR replaces it: at its head `9302bc0d` (09:23) it drops that clause. **So deploying main WITHOUT the pending PR would put rejected wording on UAT**, and the kit pins `TARGET` as a descendant of `0820efe9` through slot S4.
- **Recent activity (#300) changes layout only.** #298 (Entra token renewal) and the mock changes (#300) do not run on UAT.
- **The readiness change (R) exists only in the pending PR.** The kit makes the seat report what it SEES on `/assessments` as Partner: H1, `document.title`, the first panel's heading, the statement and area counts, and the sidebar label. Those values go in the STATUS BLUF. Any difference from S15 is a STOP. "Start a self-assessment" is never clicked.
- **PART F (new) reads UAT's feedback store, GET only, after PART P passes.** Measured at source, there are two traps:
  - **The "Feedback received" page lists ONLY category `review`** (`AdminFeedback.tsx:75`). Reading that page would miss bug, idea, content and question items. The kit therefore adds ONE Admin in-page `GET /api/v1/feedback?limit=200` (all categories; max 200 and no cursor, so it has a truncation rule).
  - **On UAT, Approve and Delete on the approval page are LIVE for anyone** (`FeedbackModule.cs:170-172`). The kit has zero clicks on both pages, a router that aborts every non-GET and every `/attachments/` GET, no screenshots, and summaries with no names in STATUS.
- **The way back is the D57 kit's own packages for `884fd72b`,** re-digested by the drafter at 09:28. They are equal to B1454's record. The CI artifacts expire on 2026-11-16.

## Facts re-measured with instruments
All read-only, using `gh api -X GET` under the project GH_CONFIG_DIR. Clocks are from `date`, 09:21:11-09:33:50 AEDT.
- **Main and the range:**
  - `branches/main` = `0820efe9ff08d32bc0d4710643081abb268f4725` (09:21:11).
  - `compare 884fd72b...0820efe9`: ahead 5, behind 0, 5 commits, 18 files, +720/-48. There are 6 product paths and 12 test paths.
  - `commits/<sha>/pulls`: `192c0a94` = #298 (head `d7df877a`), `90d30d5f` = #299 (`aca2290c`), `7d4e3142` = #301 (`0cdfc74e`), `856d15d1` = #302 (`c0a5fa17`), `0820efe9` = #300 (`b18457c2`). The check-runs on each head read 23 of 23 success.
- **Tree proof** (python over the recursive trees, blobs only):
  - The union of the PR file lists equals the 18 range paths, with 0 overlap between PRs.
  - The blob at `0820efe9` equals the blob at the PR head for every path.
  - The number of blobs that differ outside the union is 0 (a planted path reads 1).
  - The schema regex matches 0 paths.
  - `deploy-from-ci.sh` (`0024302d1ea3`) and `deploy-package.py` (`77dc49939859`) are equal at both ends. The script is 109 lines; `:49` is the predicate and `:68`/`:69` are the deploy lines (grep, with header controls `:10` and `:18`).
- **CI at `0820efe9`:**
  - Run `42689075848` succeeded on all jobs except `dependency review`, which was skipped. That includes all 3 SQL Server legs, `infra` and 8 e2e shards.
  - CodeQL run `42689076911` succeeded. Open alerts: 0 (control: `fixed` reads 1).
  - The deploy artifacts are `expired=false` and expire on 2026-11-16.
- **Scans of the added lines of the product paths:**
  - Configuration-key reads: 0 (the plant reads 1).
  - Hidden or bidirectional characters: 0 (the plant reads 1).
- **Gates** (`head -n 1` of each project STATUS):
  - #298: B1450 GO WITH FINDINGS @ d7df877, with B1450-1..6 Minor.
  - #300: B1451 GO WITH FINDINGS @ 121ee23, with B1451-1..4 Minor. The landed head `b18457c2` is +1 commit and 1 test path past the gate (`compare 121ee23...b18457c2` measured).
  - #299: B1452 GO WITH FINDINGS @ aca2290, with B1452-1..5 Minor. B1452-1's "becomes a Major" clause does not apply, because UAT's sample is at report-issued (B1454).
  - #301: B1453 GO WITH FINDINGS @ 0cdfc74, with B1453-1 Minor and -2..10 Notes.
  - #302: B1455 GO WITH FINDINGS @ c0a5fa1, with B1455-1..2 Minor.
- **Words:** the extractor `words1460.py` (scratchpad) ran over the added and removed lines of the 6 product paths.
  - Plant controls: a planted JSX sentence is found (1), and a planted comment string is ignored (0).
  - Every `file:line` was re-printed with `awk NR==n` over the raw files at `0820efe9` and `884fd72b`.
  - The API reply text is equal to nothing in the web app's screens. A code search for `finding-explanation` in `web/` hits only `web/src/api/schema.gen.ts`.
  - The two mock messages equal the API's existing words at `Requests.cs:141`/`:149`.
- **Pending PR:** `refs/heads/b1392/hpsmpoc-caveat-reword` = `9302bc0d` at 09:23. It is ahead 2 commits, with 7 paths, all under `web/`. Open PRs: 0. At that head:
  - `AssessmentsHub.tsx:131` is the header: title `READINESS_TITLE`, eyebrow "My readiness".
  - `:86-100` is the current-statements panel, `[data-testid="readiness-current"]`, with heading `${READINESS_TITLE}: current statements` and a "Start a self-assessment" button.
  - `:127` holds the `leadWithCurrent` condition.
  - `READINESS_TITLE` = "Playbook Partner Readiness" (`content/readiness.ts:11`).
  - The tab title template is `%s · HP Security Services Playbook` (`app/layout.tsx:7`).
- **Feedback at source (`0820efe9`, none of it in the range):**
  - `listFeedback` is Admin only (`FeedbackModule.cs:166`).
  - The list takes a limit from 1 to 200, sorts newest first by id, has no cursor, and takes category and state filters (`FeedbackEndpoints.cs:50-56`, `:209-227`).
  - The Received page shows category `review` only (`AdminFeedback.tsx:75`). The approval page shows `state=held` (`FeedbackReview.tsx:42`).
  - Approve and delete are not switched off on UAT (`FeedbackModule.cs:170-172`).
- **The way back:** `.tools/b1454/target/` was re-digested at 09:28:
  - web `279f184a...` 16,542,627 B; API `7741578d...` 49,630,884 B;
  - `.sql` files `8a4084b6...` / `2a587ac2...`;
  - both manifests read commit = `884fd72b`; RUN = `42659375588`;
  - `rollback1454uat.sh` sha256 is `f52193f7...6dc9a`.
  - The last line of B1454 STATUS is `DEPLOYED B1454: 884fd72b...`. The deploy-STATUS listing reads B1307, B1391, B1454.
- **Ports, panes, models:**
  - Ports 9970-9979: 0 listening at 09:25:07 (control: 17 in all).
  - A word-boundary scan of 58 SEAT kits for `997x` hits D56, G374's reservation for D56, and D57 (control: `994x` hits 6).
  - Panes at 09:25:07: **`%24 Datasec/HPSM-POC-D57` is still open.** `%13 -H142` is building the pending branch; its kit forbids hosted calls (`:15`).
  - Model-routing `:96`/`:145`; `claude-opus-5-5`. `launch_when_cool.sh` and `brief_seat.sh` exist. load1 = 29.97.
- **Name scan of the kit** (python, underscore-aware): the 0-count holds for the names tried, except for the file name `...WORDS-FOR-KAM.md`, which Tuesday dictated and which appears twice as a path (control: `x_by_steve_` reads 1). The kit contains no decision-card id.

## D-decisions (in the kit, in summary)
- **D-1:** pin `TARGET`; it must descend from `0820efe9`.
- **D-3:** both packages; the API restarts with NEW code.
- **D-7:** the way back is `884fd72b`, from `.tools/b1454/target/`.
- **D-8:** a closed list by STRING. It is the WORDS-FOR-KAM file plus S14, the pending PR's strings that Tuesday lists.
- **D-12:** the hub changes by design, but only in its header and first panel. The runner and results pages stay equal.
- **D-13:**
  - (R): the readiness SEEN fields against S15.
  - (C): the step 10 caveat on UAT equals the source.
  - (W): the walkthrough is unchanged.
  - (A): Recent activity text is equal after whitespace normalisation.
  - (N), (E) and (M) are listed as NOT TESTED on UAT, with their proof given elsewhere.
- **D-17 and PART F:** the read-only feedback census, as described in the BLUF.
- **BUILD 4:** the API property is "Modules.Assessment carries code, plus its user strings; the other 4 DLLs are stamp-only".
- **BUILD 7 (iii):** the local 422 `narrative.no-findings` proof, with an unchanged row count.

## Q-questions for Tuesday (each with a default)
- **Q-1. S15 / `@READINESS@` text.** Default:

  > On /assessments as Partner: h1 "Playbook Partner Readiness"; document.title "Playbook Partner Readiness · HP Security Services Playbook"; the first panel is [data-testid="readiness-current"] headed "Playbook Partner Readiness: current statements" with 16 statements (li) in 4 areas (readiness-current-area), shown because the newest completed run is on an older content version; the header eyebrow and the sidebar label read "My readiness"; the runs list follows; "Start a self-assessment" present, never clicked.

  Re-check the heading and testids against the landed head. They come from `9302bc0d`, which may still change.
- **Q-2. S14, the pending PR's strings.** Default: Tuesday runs the extractor (`words1460.py` in the drafter's scratchpad, or the same method) over `0820efe9...TARGET` and lists every string with its `file:line`. At `9302bc0d` the list is the hub lines `:87`, `:88`, `:99` and `:131` (the H1/eyebrow/lead), the page title at `page.tsx:6`, and the new caveat at `steps.ts:130`. Then append them to WORDS-FOR-KAM for the product owner's read before the stamp (S11).
- **Q-3. Close the D57 pane (`%24`) before the launch.** Default: close it. If it stays open, the pane REFUSE fires.
- **Q-4. Port block 9970-9979 (D57's, now ended).** Default: reuse it. G377's and G378's kits list 9900-9999 / 9940-9999 as "taken at drafting" (D57's block among them), not as their own claim. If you prefer a block nobody has ever named, write it in S10 (e).
- **Q-5. PART F storage.** Default: the raw JSON stays in `.tools/b1460/fb/` (mode 600, never in `Briefs/`). STATUS gets summaries of at most 25 words, with no names, and no screenshots. If you would rather have the raw comment text never written to disk at all, say "PART F IN MEMORY ONLY" in S10 (f).
- **Q-6. PART F timing.** Default: after PART P PASSED, or after a healthy-site STOP, and never after a rollback. If the deploy cannot start (the PR is not landed in time), PART F still answers the product owner's "check all feedback items". Do you want a separate read-only seat for it? Default: no; it waits for D58.
- **Q-7. S5, S6 and S12.** Default: Tuesday fills them from the landed PR. S12 = `298 299 300 301 302 <N>`. S6 carries the five gates' findings as listed in the kit's S6 label, plus the pending PR's gate line.
- **Q-8. S10 (d), HP review session.** The drafter cannot know whether one is under way. Default: Tuesday states it.

## UNMEASURED (by the drafter)
- Every hosted fact is RELAYED from B1454 STATUS: whether UAT still runs `884fd72b`; the settings; the activity since 18:33:46Z; the database; the deployment ids. No `az` and no HTTP were used.
- The full range at `TARGET`. The pending PR is unlanded and still building; its gate, CI and final strings are unknown.
- Whether the UAT Partner's newest completed readiness run is on an older content version. B1454 saw two 0.3.0 runs; the hub's lead condition depends on this. The seat records BEFORE.
- How many feedback items UAT holds, and whether any category reaches 200.
- Whether `HpsmPoc.Modules.Assessment.dll`'s user-string heap search works as written on this build (the seat runs its control first).
- The exact `generateNarrative` route and precondition shape on the local pair. The seat reads them from source.
- `layout.tsx:7` and `readiness.ts:11` were read at `9302bc0d`, not at `TARGET`.

## Outside-the-fences disclosure
- **Not used:** `az`, ssh or docker; HTTP to any hosted host; any git write verb; `cd`; `decision_queue.sh`.
- **`gh` was used with `-X GET` only,** under the project GH_CONFIG_DIR. That includes one `search/code` GET (three queries) to find callers of `finding-explanation`, and `contents` GETs of raw files at `0820efe9`, `884fd72b` and the pending head `9302bc0d`.
- **`0_Brain/learnings/_ledger.md` was not read.**
- **Local reads:**
  - the drafter rules, and the D57 kit, report and STATUS (all whole);
  - FINDINGS.md and CENSUS.md (whole);
  - the first and last lines of the gate STATUS files, plus grep for finding ids and the B1452-1 lines;
  - the port lines of the G374, G377, G378 and H142 kits, and H142's `:15` no-hosted line;
  - `.tools/b1454/` listings and digests;
  - `lsof`, `tmux list-panes`, `sysctl vm.loadavg`, model-routing lines, `models_latest.json`.
- **Two Bash commands were refused by the project's zsh hooks** (`set -- $x` word-splitting, and an unquoted `===`). Both were re-run correctly; neither ran in its refused form.
- **Scratch:** the JSON, raw files and the extractor were written only to the session scratchpad: `/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/017af1b7-c908-4074-bd26-db14582a6cfd/scratchpad/b1460/` (extractor: `/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/017af1b7-c908-4074-bd26-db14582a6cfd/scratchpad/b1460/words1460.py`).
- **Files written in briefs: three.** The words file, the kit and this report. The rules say "two files"; the third (WORDS-FOR-KAM) was commissioned explicitly.
