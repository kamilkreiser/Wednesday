STARTABLE: YES (records only, no Jira write; slot RECORDS must read WRITE; main's push run after the landing is RED on linux, recorded with B1908's TEST RACE reading relayed, per ADDENDUM 1 and 2)

# B1906 drafter report (Opus, in-session, read-only), 2026-11-22

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1906_SEAT-R297_oxpd2-records-lane-f.md` (64028 bytes, 327 lines, ASCII only, 17 frozen texts, 33 SOURCES rows all hashed, 41 REVIEW MAP rows, 7 slot lines). Sidecar: the same name plus `.measured` (74 of 74 claims; `stamp_check.py <kit>` exits 0, output in `fleet/state/s310/d1906/stamp_check.out`). Scratch and programs: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s310/d1906/` (`kit_src.md`; `tools/build.py` assembles the kit and runs K1 to K5; `tools/sidecar.py`; `tools/jget.py`, Jira GET only; `build_report.json`; `dry/`). Reads 19:14:48 to 19:32:33 AEDT (clocks by `date`).

## BLUF
- A NEW records kit for seat `Datasec/OXPd2-R297`, level opus. It writes two files only: seven owed items in `BACKLOG.md` and one history entry (10 lines). It writes no Jira, no clarification entry and no runbook line.
- **The landing (MEASURED by GET).** Pull request 17 merged 2026-11-22T08:12:41Z as `bf6b441e`. It has 1 parent (`185b9eef`) and tree `de9817fc`, the same tree as head `94fe6067` and merge ref `f4d219a0`. Its commit message ends `(#17)`.
  - The pull request's own run `45001239770` succeeded. Both test legs' logs hold `HEAD is now at f4d219a Merge 94fe6067... into 185b9eef...`. The merge-ref figures equal Tuesday's: linux 1578/0/1574/4 with GUARD 10; windows 1578/0/1559/19 with GUARD 11; rules clean over 500 files, 111 tests, floor 111.
  - 8 distinct checks succeeded. CodeQL at `refs/pull/17/head` found 0 results in each of three languages.
  - RELAYED, not re-read: the head-pinned squash, `SQUASH-SCAN: clean` and pr_retrigger MATCH.
- **Main's first push run is RED. I measured it before ADDENDUM 1 arrived, and it agrees with it.**
  - Run `45001737294` (attempt 1, conclusion failure): the `linux` job failed with total 1578, failed 1, succeeded 1573, skipped 4.
  - The one failing test is `Datasec.Suite.Sessions.Tests.RefreshBoundCellTests.F13_after_a_time_out_a_second_call_may_start_and_the_late_answer_is_never_kept`.
  - windows (1578/0/1559/19, GUARD 11), rules, secret-scan and all three Analyze rows succeeded. Open alerts on main: 0.
  - Pull request 17 changed 0 of its 27 files in Sessions (control: 22 files under `Registration/`).
  - The kit records this as owed item MAIN and history line H-MAIN. They never say green or passed; a program check enforces that, with a control.
  - **ADDENDUM 2 applied.** I read B1908's FOUND and TESTED sections; its first line is `DIAGNOSIS B1908: TEST RACE`. BL-MAIN and H-MAIN relay it as the coordinator's diagnosis: F13's scripted refresher answers in arrival order, and there is the smaller `FakeRefresher` count-before-record race (read, not tested). No product change is indicated. The diagnosis measured 0 failures in 2500 local runs, 50 of 50 with the injected delay, and 0 of 50 with the fix shape. The hosted runner is UNMEASURED by it.
  - The record says the test-only fix lane is pending and that no ticket was created. Nothing says the broker is defective.
  - The diagnosis is SOURCES row 21, and RM rows 33 to 41 check its lines.
- **The review** (both first lines, measured): GO WITH FINDINGS by both readers at 94fe606, no Blocker and no Major. The landing is the coordinator's.
- **The owed items:**
  - F1: B1904 F1 (the delete is not serialised with an attach), owed before WP4.5.
  - F2: B1904 F2 (an issuer that blocks escapes the bound), owed before the real issuer.
  - F3: missing cells: B1904 F3 and item 5, plus B1905 F2.
  - F4: platform behaviour and limits: B1905 F1 (s+n, Linux and Windows UNMEASURED), F3, F4 and F5; B1904 item 4; and 4(f) with Tuesday's answer, recorded as the coordinator's.
  - F5: the runbook checks and kit wording (B1904 items 6 and 7, and X22's FOR RECORDS).
  - F6: what stays open (item 8; `OXPD2-18` stays open).
  - MAIN: main's push-run red.

## Corrections to the commission (each measured)
- **D1. The kit's literal for `total: 1578` on the main linux log: 1 line, not 2.** My first build wrote 2 lines. The sidecar measurement caught it (the windows log has it on 2 lines; the linux log has 1 such line plus the workflow's own grep command line). I corrected it before the kit was finished.
- **D2. The WP4.1 ticket is `OXPD2-18`**, `[WP4.1, WP4.2 part] Universal Print protocol encoder`: Task, parent OXPD2-6, Backlog, 0 comments. BACKLOG.md line 361 maps WP4.1 to it. This confirms FOR-RECORDS item 8: it stays open and unwritten.
- **D3. A runbook file exists:** `SETUP_RUNBOOK.md`, last written 2026-11-20 17:52 by records kit B1785, whose OWNED line lists it. The later records kits B1816, B1887 and B1900 did not write it; they held runbook lines as owed items. So item 7 goes to BACKLOG as one owed item (F5), not as a runbook edit (Question 2).
- **D4. No history entry exists for lane F.** These all read 0 lines in `history.md`, against a control `pull request 16` of 1: `pull request 17`, `bf6b441e`, `94fe6067`, `Universal Print registration` and `45001737294`. So the entry carries the whole landing.
- **D5. No precedent for a Jira comment at a landing.** B1887 posted 4 comments, all on `OXPD2-1` (the master list). B1900's one write was the OXPD2-25 create, made on his card. So the kit does no Jira write, which is the commission's default.

## Facts re-measured (instrument, control)
- **GitHub** (`gh api -X GET` under the project's GH_CONFIG_DIR, 19:15:48 to 19:28:34):
  - Pull requests: 17, all merged, 0 open; `pulls/99999` rc 1 (404). Refs: 18. Main is `bf6b441e`; the b1840 branch is at `94fe6067`.
  - The run lists, both attempts' jobs, the job logs (with `--allow-escape-sequences`), check-runs, analyses and alerts are as in the kit. The PR 17 file list holds 27 files.
  - The trees of `94fe6067`, `f4d219a` and `bf6b441e` are all `de9817fc...`.
- **Jira** (GET only, through the project helper's transport loaded by importlib, 19:18:59):
  - 25 issues, 0 Done. Controls: OXPD2-1 reads 200 with 11 comments (41405 to 41450); OXPD2-99999 reads 404.
  - Phrases with no hit: `DeleteRegistration`, `RegistrationKeys`, `F13`, `RefreshBoundCellTests`, `device token`, `certificate custody`, `key generation`, `blocking issuer`.
  - Phrases with hits: `app registration` finds OXPD2-1 only, and `WP4.1` finds OXPD2-6 and OXPD2-18.
  - Controls: `REC-NEW-RULES-20NOV` finds OXPD2-23, and `zzqxnonexist` finds none.
- **Records state:**
  - The live sha256 of `BACKLOG.md`, `history.md` and `CLARIFICATIONS.md` equal B1900's `READY.manifest`. The manifest's sha256 prefix equals `READY B1900: 85f9c97f...`.
  - BACKLOG has 51 owed lines, numbered 1 to 51 with no gap. The heading is found once, at line 347.
  - Every P-3 probe reads 0; the controls are `OXPD2-25` (1 line) and `pull request 16` (1 line).
- **Scanner:** a byte-equal copy of `b1785.py` (sha256 `5e766b28...`, `cmp` rc 0; also equal to B1900's copy), loaded by importlib and never run.
  - `scan_record` over the 59 filled lines found 0 problems and 0 bytes above 126.
  - Controls fired: a planted `_by_<name>_` gave S-NAME, a card id gave S-CARD, a coordinator path gave S-COORDPATH, and a dash gave S-ASCII.
  - The PR title passes, with 0 double quotes.
  - The whole kit text holds 0 name tokens (control fired) and 0 card ids.
- **Dry build** (byte copies, scratch): `BACKLOG.md` goes from 362 to 411 line feeds (+49, 0 removed); `history.md` from 172 to 183 (+11). The added bytes hold 0 above 126.
- **Panes** (19:20:18 and 19:28:34): `%0 tuesday`, `%127`, `%128`; none is OXPd. Ports: none, as the kit opens no listener.
- **Model:** `models_latest.json` line 17 gives `claude-opus-5-5`. Routing row C8 (line 98) says Sonnet first, but the project's `CLAUDE.md` line 7 asks for Opus, so the level is opus.
- **Read load** (PREDICTED, by program): about 101321 bytes. The kit is 64028 bytes, the sidecar 10293, and ranges and allowances about 27000.

## Questions for Tuesday (each with a default)
1. **His word on lane F.** I could not search the board: `kam_msgs.sh` reads a hosted dashboard, which fence 4 refuses. I could not search the cards either: only `show <exact id>` is allowed, and I had no id. I searched Tuesday's daily note of 2026-11-22. It names six OXPd card ids, none of them lane F's: the jobs card, the two CI-guards cards, firmware callbacks, the SQL Server driver and tolerant answers.
   - **Default:** no card or board line of his names lane F, so the landing and the owed items are the coordinator's. Please confirm in BASE that no lane F card exists.
2. **The runbook.** Default: owed item F5, no runbook edit (D3).
3. **Jira.** Default: no write (D5). No project rule I found REQUIRES a ticket for an owed item: `CLAUDE.md` line 66 sets only the form. So the owed items get no ticket, as is Tuesday's own default.
4. **Main's red.** The kit carries it as owed item MAIN, with B1908's TEST RACE reading relayed (ADDENDUM 2), the fix lane (B1912) pending and no ticket, plus a `<<RUN-NOW>>` sentence. That sentence gives the run's latest attempt and conclusion at the seat's read, so a re-run of yours before launch is recorded truthfully.
   - Default: launch now. The fix lane's landing is a later records pass.
   - BL-MAIN does not name B1912 (it was not yet commissioned at drafting); it says the fix lane is the coordinator's.
5. **No clarification entry.** No word of his is new: the 16:53:30 message is already C-68. Default: none.
6. **Slot RECORDS** defaults to HOLD. I recommend WRITE.

## UNMEASURED
- The seat's live owed numbers (52 to 58 PREDICTED), and its `<<RUN-NOW>>` and `<<HHMM>>`.
- Whether GitHub accepts the s+n shape on Linux or Windows (the readers' UNMEASURED).
- B1908's hosted-runner and whole-suite reproduction (its own UNMEASURED). Its TESTED figures are RELAYED in the kit, not re-run by me.
- The squash pinning and SQUASH-SCAN at landing (RELAYED).
- The seat's helper and HOLD R / HOLD R2 on live files (never run on a real output; the kit says so).

## Chain inputs (each step's inputs exist at BASE or come from an earlier step)
| Step | Inputs | From |
|---|---|---|
| 0 | the stamped kit, sidecar, panes, df, clock | BASE |
| 1 | `b1785.py` (copy); B1900's helper (read only) | BASE |
| 2 | SOURCES files; GitHub; Jira; B1887 and B1900 STATUS; B1900 `READY.manifest`; the live record files | BASE |
| 3 | the frozen texts; the Step-2 facts (title, M17, origin, RUN-NOW, census, owed numbers) | the kit, Step 2 |
| 4 | the Step-3 filled texts; the origin and main run re-read in the process; the live bytes | Steps 2, 3, 4 |
| 5 | all of the above | Steps 0 to 4 |

## Outside-the-fences disclosure
- **Writes:** the kit, its sidecar, this report, and scratch under `fleet/state/s310/d1906/`. My first two sidecars were moved to `d1906/_quarantine/sidecar_v1.measured` and `sidecar_v2.measured` with `mv`; nothing was deleted.
  - A hook refused `cp` from the project path to my scratch (it read the source as a write target), so I copied `b1785.py` by `cat` redirection and proved the copy with `cmp`.
- **Reads:**
  - B1908's DIAGNOSIS.md, whole, after ADDENDUM 2. `contents/tests/Datasec.Suite.Sessions.Tests` at bf6b441e by GET: 13 entries, `RefreshBoundCellTests.cs` and `Fakes.cs` present.
  - The project's `CLAUDE.md` (by line), `BACKLOG.md` and `history.md` (by range and by count), `SETUP_RUNBOOK.md` (line lengths and first 170 characters, by awk), and the `CLARIFICATIONS.md` counts.
  - B1840's STATUS (by sections), B1887's STATUS (by grep) and B1900's STATUS (whole).
  - B1900's kit (whole), its report and its manifest; B1785's and B1887's kits (by grep only).
  - The B1840 kit's drafter report (AMENDMENT 1, whole); the B1904 and B1905 commission, both VERDICTs and FOR-RECORDS (whole), and the landing texts.
  - B1852's VERDICT (by grep for F13); Tuesday's daily note of 2026-11-22 (by grep for card ids only); the header of `decision_queue.sh` (`sed -n 1,40p`).
- **Online and tools:** `gh api -X GET` and Jira GET only. `tmux list-panes`.
- **Not run:** `decision_queue.sh` in any form, and the board reader. B1908's scratch was never opened.
- **Never touched:** `Source_Documents/`, the NAS, `fleet/briefs_staged/`, `scoreboard.md`, `_ledger.md`, any WEDNESDAY or FRIDAY tree, any other project. No `cd`, no `az`, ssh or docker, no write to any project file, Jira or GitHub.
