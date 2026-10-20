# B366 DRAFTER REPORT (Sonnet drafter, row C8) for brief `2026-10-21_B366_SEAT-DEP3_hpsmpoc-hosted-deploy-6818896.md`

Drafted 2026-10-21 ~04:2x AEDT (`date` printed 04:26:24 and 04:27:05 AEDT). Marks: MEASURED = I ran it and saw the output; RELAYED = read from a file at path:line; UNMEASURED = nobody ran it. Fences kept: two files written; `gh api` GET only under the project's `GH_CONFIG_DIR` (`kamilDatasec`, `gh auth status` MEASURED); no `az`, no HTTP to hosted or Azure, no git write verb (I ran none: only `gh api`, `lsof`, `ls`, `grep`, `sed -n`, `uptime`, one `python3` read of `models_latest.json`); no tmux, no mail, no Artifact/Docs; no `cd`. Not opened: `HP Reporting and Docs/`, `HP Docs/`, `.local/`, `Source_Documents/`, `.env`, any key, B300/B304 STATUS, `briefs_staged/`.

## 1. What I read
Whole: grant learning `0_Brain/learnings/2026-10-16_tuesday-inherits-push-to-demo-hpsmpoc-unfrozen-account-controls-datasec.md` (26 lines); B316 brief (131 lines) and `B316_STATUS.md` (340 lines); B316 ADDENDUM-1 (12 lines); `B363_DRAFTER-REPORT.md` (64 lines). Parts: B316 `.pre-stamp` slot lines (`:19`, `:123-131`), B363 brief grep for the STANDING HOLD (`:91`) and the Done rule (`:35`), `B363_STATUS.md:1-60` and last two lines, `model-routing.md` rows C6-C8, `EXPIRING-GRANTS.md:11`, `brief_seat.sh:15-30`, `.tools/b316/rollback316.zsh` and `id.zsh` (whole), `.tools/` directory listing, B364 brief (grep only: its pane `Datasec/HPSM-POC-D9`, "main is not the STAMPED MAIN" line, no open PR). Records `CLARIFICATIONS.md` on main by `gh api` (raw, 1,986 lines, saved in my scratchpad): C-124 `:1892-1910`, C-127 `:1960-1986` read whole.

## 2. Facts (each with where)
- **Code main** `6818896b68090777c8edbf0e694741928c96ca3f`: MEASURED `gh api repos/datasecau/HPSM-POC/git/ref/heads/main` 04:26 AEDT. Commit: tree `4fac7e01b81d893f02d1883333db7e8ef8d7d52f`, one parent `c149a3037463d38bf7cec38c16a182c746b3b1b3`, committer date 2026-10-20T16:16:57Z, subject "HPSMPOC-301 + HPSMPOC-302: import failure keeps the first failure; sweep count rows (#165)" (MEASURED `git/commits/…`).
- **PR #165**: `merged=true`, `merged_at` 2026-10-20T16:16:58Z, `merge_commit_sha` = the pin, base `main`, merged by `kamilDatasec` (MEASURED `pulls/165`). Check-runs on the merge: skipped 1, success 18 (MEASURED).
- **CI on the merge sha** (MEASURED `actions/runs?head_sha=`): "Push on main" 39456055558 (`dynamic`, attempt 1, completed/success) and `ci` 39456056849 (`push`, attempt 1, completed/success), both created 2026-10-20T16:17:01Z. Open code-scanning alerts on `refs/heads/main`: 0 (MEASURED; I did NOT run the `state` control that fires, so this 0 is unconfirmed by a control: the brief tells the seat to run one. B363 measured control `fixed` = 1, RELAYED `B363_STATUS.md` Step 1).
- **New artefacts** (MEASURED `runs/39456056849/artifacts`): `deploy-api-6818896b…` id 12279874564, 49,631,691 B, expires 2026-10-27T16:26:42Z, `expired=false`; `deploy-web-6818896b…` id 12281601583, 15,359,655 B, expires 2026-10-27T16:24:35Z, `expired=false`. (A second web artifact `web-deploy-package-unkept` 12280287532 also exists, expires 2026-10-21T16:19:01Z: not the deploy one.)
- **Way-back artefacts** (MEASURED `runs/39346182958/artifacts`, same time): `deploy-web-c149a30…` 12231098107, 15,359,643 B, expires 2026-10-27T00:21:09Z; `deploy-api-c149a30…` 12231547296, 49,631,694 B, expires 2026-10-27T00:25:25Z; both `expired=false`. They match `B316_STATUS.md:87`. `.tools/wt-B316/out/deploy-packages/c149a3037463d38bf7cec38c16a182c746b3b1b3` exists (MEASURED `ls`), and the kit `.tools/b316/` holds the `*316` files (MEASURED `ls`; the manifest has 139 lines).
- **Deploy delta c149a30 -> 6818896b** (MEASURED `compare/c149a30...6818896b`, `ahead_by` 1, `behind_by` 0, `total_commits` 1, one commit with one parent): 4 files only: `api/src/HpsmPoc.Modules.Assessment/Ingest/ImportEndpoints.cs` +6 −3 (modified); `api/tests/HpsmPoc.Api.Tests/Imports/ImportFailGuardTests.cs` +331 (added); `…/ImportSweepCountTests.cs` +160; `…/ImportSweptUploadTests.cs` +2 −1. **This confirms your expectation** (tests + one `ImportEndpoints.cs` change). The `ImportEndpoints.cs` patch (MEASURED, read in full): comment lines plus one condition, `run.StatusReason == reason` becomes `run.StatusReason is not null`; it only widens an early `return`, so it writes less. No migration, `appsettings`, `scripts/`, `web/` path in the list.
- **Unchanged blobs** (MEASURED contents API at both shas): `scripts/deploy-from-ci.sh` `0024302d1ea35ff5de4047824e2cb46ced16ecdf`; `api/src/HpsmPoc.Api/appsettings.json` `f10fcc8ce37b106f116d6a247498924672306c1b` (equals B316's blob, `B316_STATUS.md:80`).
- **Records main** `e2a0d72193dd11f98a6d582cd06fb7fdffecac5e`, "Merge pull request #126 from datasecau/records/b363" (MEASURED, `commits/main`) = the sha you quoted. `CLARIFICATIONS.md` 1,986 lines; headings C-124 `:1892`, C-125 `:1911`, C-126 `:1942`, C-127 `:1960` (MEASURED `grep -n`). I did not scan other refs for C-128, so "C-128 is next free" is main-only (UNMEASURED against other refs).
- **C-124 deploy block** (read whole): authority C-105; deploy sequence, deployments, live-check lines, restore point, way back, "NOT TESTED" list, and the Jira the records seat then did (comments 39798-39806 and HPSMPOC-298/-299/-300 Backlog -> Done by transition 41). **The rule that Done follows a verified live deploy** is the coordinator's R-R10-1 as quoted in C-124 and C-127.
- **C-127's "Not deployed" bullet** says hosted is on `c149a30`; the brief tells the seat not to edit it (Tuesday supersedes).
- **Runbook**: no standalone file (RELAYED B363 report section 3, `SETUP_RUNBOOK.md` is setup); the runbook is the B316 brief + STATUS, which the brief names and tells the seat to read whole. `deploy-from-ci.sh` not read by me (blob only).
- **B316 did no Jira write** (RELAYED `B316 brief :107`: "no Jira write"; STATUS Records section `:304`, `:333-338`). So the brief gives the seat none.
- **Ports**: `lsof -nP -iTCP:7350-7399 -sTCP:LISTEN` printed nothing, rc 1, at 04:27 AEDT (MEASURED). Other projects' briefs already use 7350-7359; the brief assigns 7360-7369. A `grep` of `tuesday/briefs/2026-10-2*.md` showed 7350-7359 ×16 and no 736x (MEASURED).
- **Load**: `uptime` 04:27: 11.22 / 8.94 / 8.44 (MEASURED).
- **Model id**: `claude-opus-5-5` from `0_Brain/dashboard/data/models_latest.json` `levels.opus.model_id` (MEASURED) = the id in your task.
- **Routing**: row C6 Deploy: Opus 1st; "Any rollback: Kam is told" (`model-routing.md:96`, MEASURED grep). The brief carries that in the way-back section.
- **Slots**: `/usr/bin/grep -c -E '@SLOT:[A-Z0-9_]+''@'` on the finished brief prints 9 lines; 12 distinct tokens (MEASURED). No `.pre-stamp` created (fence: two files only): Tuesday copies it before stamping (the brief's refusal accepts a scratch-file control otherwise). Title sha is 40 lowercase hex.
- **B-number**: B366 free in `tuesday/briefs/` and the project's `Briefs/` at my `ls` (MEASURED: the listings showed up to B365 in `tuesday/briefs/` and B364 in the project). Tuesday confirms in the B_NUMBER_CONFIRM slot.
- **In flight**: B364 (pane D9, HPSM-POC tests) is a live HPSM-POC seat, `.tools/b364` exists. It ends at a pushed branch; if its PR merged before this deploy, main would move and the seat's re-pin would STOP. Hence slot R_DEP3_5.

## 3. Choices I made that you may want changed
- The brief says **no Jira at all** for the seat, and puts HPSMPOC-301/-302 Done under Tuesday's later records step with the rule and its source (C-124, C-127). The rule is clear in the files, so no "unclear" fallback was needed; `FOR TUESDAY` still asks the seat to state whether the deploy is verified live.
- Pre-switch steps are B316's, adapted: 5A, 5B, the word sweep (one source file, expectation 0 new literals), the data-effect check (one guard line), a ports block 7360-7369, and `.tools/b366` kit by re-pointing B316's files.
- I added two stamp slots beyond B316's format: R_DEP3_4 (the old-process overlap rule, from B316 FOUND-3 / HPSMPOC-303) and R_DEP3_5 (main must not move). Slot names: STAMP_TIME, B_NUMBER_CONFIRM, MODEL_LINE, CODE_MAIN_PIN, COMPLETION_CHECK_165, PANE_FREE, DEMO_WINDOW_NOTE, R_DEP3_1 to R_DEP3_5.
- Names: I removed the sample-customer and a contact's name from lines I wrote. "Kam" remains in the opening line, the grant quote and the "Kam-stated freeze" phrase, copied from B316; the STANDING HOLD is quoted as B363 carries it (verbatim, `B363 brief :91`).

## 4. UNMEASURED items and the instrument that closes each
| Item | Instrument |
|---|---|
| Hosted today equals B316's after-set; any restart/move since | seat: step 2a (`az` read-only, ARM activity log) |
| Both packages' differences (API 5 DLL/PDB; Feedback stamp-only?; web 12 files) | seat: step 5 (`pe316` successor, `webid260.py`, `webkeys.py`) |
| Local boot of both zips on 10.0.12/10.0.13, health codes | seat: 5A/5B |
| Pkcs `2 · 2 · 2 · 121` on the new api.zip | seat: `postmerge255.sh` |
| Whether the FOUND-3 old-process overlap recurs with unchanged Feedback source | seat: step 7 scan with old-container lines separated |
| Platform image for the new containers / `DOTNETCORE-10.0.13` | seat: `platlog.zsh` |
| Open code-scanning alerts 0 with a firing control | seat: `code-scanning/alerts` plus `state=fixed` control |
| Tuesday's completion check for #165 | Tuesday's stamp slot COMPLETION_CHECK_165 |
| Demo window, pane free | Tuesday at stamp |
| C-128 free on every ref | the records seat's C-scan |
| `deploy-from-ci.sh` behaviour | seat reads it in `wt-B366`; blob equal at both shas (MEASURED) |
| Container runtime user | UNMEASURED at B316 too; no instrument allowed |

## 5. Questions for Tuesday (numbered; recommended answer first)
1. **R_DEP3_5: hold every HPSM-POC merge (B364's PR included) until this deploy's STATUS ends?** Recommend **yes**: a moved main makes the seat STOP at the re-pin, and the deploy is short (B316: 5 min 12 s of deploy, about an hour end to end).
2. **R_DEP3_4: is a `fail:` from the OLD container during the overlap a FOUND (default a) or a rollback trigger (b)?** Recommend **(a)** with the new-process-0 condition: B316 chose it, you filed HPSMPOC-303 rather than faulting it, and this range changes no Feedback source. The brief makes it Tuesday's ruling, not the seat's.
3. **Should the seat's `FOR TUESDAY` also carry the ticket-closing call?** Recommend **no**: it states whether the deploy is verified live; you (or the records seat, as with C-124) move -301/-302 to Done afterwards under R-R10-1.
4. **Completion check wording for #165:** my default quotes C-127 and B357; C-127 says only "merged by the coordinator after the gate". Replace with your daily-note line and time.
5. **Port block 7360-7369:** change if another seat holds it (I could not see other projects' live seats).
6. **Launch timing:** recommend launching only when no HP session is scheduled and B364 will not merge; the brief's demo-window slot is where you say so.

## 6. COST note
**Does this deploy create a new paid resource? No by design, MEASURED for the brief's text only, UNMEASURED for hosted.** The brief forbids any new resource, setting, SKU, Bicep or runtime change, and the deploy is a zip push (`deploy-from-ci.sh deploy`) onto the two existing apps in `hpsm-poc-demo-rg`; B316's identical deploy added none (RELAYED: settings 34 = 34, 15 = 15, access 5 = 5, `B316_STATUS.md:235`; the only budget event was a user's budget write, FOUND-2, unrelated). Not measured by me: Azure cost for the window (no `az`, per the fence); the seat's access-list and settings before/after comparison is the closing instrument, and cost itself is closed only by Cost Management, which the brief does not use. Transient usage during a deploy (two containers overlapping about 2 minutes) is existing capacity, B316 FOUND-3.

## 7. Self-check
Every sha, id, byte count, expiry and count in the brief was copied from a command output above or a file line read; the one hand-derived item is "C-128 next" (main only). The brief's last line is `READ-WHOLE-BY-TUESDAY: PENDING`.
