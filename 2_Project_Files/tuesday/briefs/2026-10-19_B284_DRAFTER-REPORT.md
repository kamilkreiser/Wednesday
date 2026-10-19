# B284 DRAFTER REPORT (read-only drafter, 2026-10-19)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-19_B284_SEAT-W5_hpsmpoc-l3-feedback-290-226.md`. Nothing built, nothing written outside these two files (plus a scratch Jira-GET script in the session scratchpad). Clocks quoted from `date` output (15:45:13 and 15:46:22 AEDT).

## What I read (with lines)
- Template `2026-10-19_B276_SEAT-W1_hpsmpoc-closeouts-docs-tests.md` WHOLE (118 lines): shape, headings, REFUSE/slot grep trick (`:9`), Step 0, launch line (`:22`), standing lines (`:25-33`), BASE (`:35-42`), HOLDS (`:85-93`), STATUS and last-line markers (`:98-110`), stamp (`:112-117`).
- `2026-10-19_B282_SEAT-W4_hpsmpoc-291-fix-round2.md` WHOLE (91 lines): newest standing lines, scope-guard-by-program, one-comment-after-push-readback rule (`:64`), per-command `GIT_SSH_COMMAND` (`:35`).
- `2026-10-19_B283_SEAT-G9_...` lines 1-51 (grep also on B280-B282 for model lines): model line shape for Sonnet launch, port block 7210-7219, partition names (`.tools/b283/`, `wt-b283-*`, PR #161 head 7329804).
- `0_Brain/projects_index/2026-10-19_ticket-sweep-hpsmpoc-composer.md` lines 55-95: class B/C/D lists and the lane table (L3 row).
- `!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-10-19_B282_STATUS.md` WHOLE (136 lines): project state (main befd45e, branch head 7329804, SDK 10.0.402, `.tools/dotnet`, load rule, gitleaks path, `kamilDatasec`, stale `core.sshCommand` of the records repo).
- Live Jira GET (own project credentials in-process via the B265 `jira.py`, nothing printed; output grep for "token" and "Basic " = 0): HPSMPOC-290 whole (no comments), HPSMPOC-226 whole (description + comments 39152, 39161, 39383).
- Code at `origin/main` (local ref equals ls-remote main): `api/src/HpsmPoc.Modules.Feedback/Endpoints/FeedbackFiles.cs` whole (446 lines); `Delivery/FeedbackDispatcher.cs` greps (`:76-85`); `git grep` for "226" in the module and tests; `git log` of the module (PRs #129 `3a9288a`, #133 `a50b22d`, #152 `a6576ce`); `git show --stat` of 3a9288a and a6576ce.
- Project Briefs: `2026-10-09_B188_SEAT-B_feedback-module-98-226.md:27-28`, `2026-10-13_B241_STATUS.md:11, :33, :82, :105`, `2026-10-13_B241_SEAT-B...md:21`, `2026-10-13_B243_STATUS.md` (N-8 there is a different note, -228's).
- `ls-remote`: main `befd45e77b391467a1313af8b7b5e0fc580f7b63`; `b276/l1-tests-291-227` `7329804e7b31d5fd8a84de9056ed81731d2ba859`; `refs/heads/b284*` and `b283*` return nothing.

## Premises and where each came from
1. Main is befd45e: MEASURED, `git ls-remote origin refs/heads/main`.
2. -290 fix site `FeedbackFiles.cs:360` catches only `IOException or InvalidDataException`; `cd.Name` read at `:310`; `cd.FileName`/`FileNameStar` at `:332-333`: MEASURED (`git show origin/main:...`). The 500 itself: from the ticket text only (reasoned, never run). `CappedStream` throws `NotSupportedException` by design at `:423-444`: MEASURED; this is why the brief asks for a narrow catch choice.
3. **-226 disagreement with the sweep (the main finding).** The sweep (RELAYED, lines 65-85) and the ticket description say N-4, N-5, N-7, N-8 are open. MEASURED in source: N-4 built (`FeedbackFiles.cs:122-146`, tests `FeedbackAttachmentTests.cs:158, :314`), N-5 built (`:149-166`, `:191-194`, tests `:186, :342`), N-7 built (`FeedbackDispatcher.cs:76-85`, `IFeedbackSink.cs:20`, `AutomationWebhookSink.cs:25`, test `FeedbackAttachmentDeliveryTests.cs:158`), all PR #129 B188. N-6 built in PR #152 (RELAYED from B241 STATUS:105; BFF code, not read by me). N-3/N-9 ruled "confirm as built" (Jira comment 39383, MEASURED by GET). N-8: B241 STATUS:33 says not built, needs contract + schema; B188 brief:27 says the timeout is in `bff.ts`: so it is out of lane. Tests were NOT run by me; the brief makes the seat run them and quote pass lines.
4. Port block 7220-7229: `lsof -nP -iTCP:7200-7299 -sTCP:LISTEN` printed 0 lines at 15:46; briefs B282 and B283 claim 7200-7219 (grep of B27x/B28x). Proposal only; it is a slot.
5. Load: `uptime` 15:45 showed load1 6.06; the brief's heavy-run rule is load1 < 8 as commissioned.
6. Jira helper kit at `.tools/b265/` (jira.py, post.py, read.py, search.py, lock.sh exist): MEASURED by `ls`. `^JIRA_API_TOKEN=` count 1: MEASURED. `.tools/b198/lock.sh`: taken on trust from B276/B282 (I did not `ls` it).
7. Partition names (`b271 b273 b274 b276 b279 b282 b283`, `wt-b282`, `wt-b283-*`): MEASURED by `ls -d`.
8. Model `claude-sonnet-5-5`, BRIEF_SEAT_LEVEL=sonnet, launch line shape: from the commission and B283 line 5; the `BRIEF_SEAT_LEVEL=sonnet` env prefix inside the cockpit command string is my construction (B283 does not show its exact launch string with the prefix): Tuesday should check how the cockpit passes the level.
9. Comment policy (one BLUF comment on each ticket after push read-back, no transition): modelled on B282 `:39, :64` and B276 R-W1-3; I made it a ruling slot (R-W5-1) because the commission said "only if the template allows".
10. Records: no records branch, no C-entry, no history entry (matches B282 `:69`); the STATUS stays in the project folder.

## What I could not measure
- The 500 for a utf-7 part name, or for any neighbouring encoded-word input (no dotnet run, by commission). Whether `FileName`/`FileNameStar` throw.
- Whether any cited test passes; the full-suite baseline on main; `.tools/dotnet` health; `gh auth status`; records `CLARIFICATIONS.md` C-99 full text (only the Jira comment 39383 and the Briefs mention); the export code for N-9 and the payload test for N-3 (not located; seat does it).
- Other multipart readers in the API (not searched; brief asks the seat to list them).
- Whether the cockpit accepts `BRIEF_SEAT_LEVEL=sonnet` as an inline env prefix in the quoted command (see premise 8).

## Slots left (all on one line of the brief, so the slot-grep counts 1 line, 3 tokens; MEASURED)
- `STAMP_TIME`, `B_NUMBER_CONFIRM` (folder check for B284/B285: 0 files named B284 at drafting), `PORT_BLOCK` (default proposal 7220-7229).
- Filled by me from the commission: model, pane `Datasec/HPSM-POC-W5`, suffix W5, main sha.
- Rulings Tuesday should make: R-W5-1 to R-W5-4 at the end of the brief.
