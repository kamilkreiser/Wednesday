# B346 DRAFTER REPORT (Tuesday's drafter, 2026-10-20 ~21:45 AEDT)

**BLUF.** Brief written: `2026-10-20_B346_SEAT-D7_hpsmpoc-wu-window-and-records.md` (109 long lines; one slot, `STAMP_TIME`, once, on the Stamp line; stamp check prints 1 unstamped, MEASURED `grep -c`). Part 1: a Sunday 03:00 Windows Update install window on `vm-hpsm-sm` by two DWORD values (`ScheduledInstallDay=1`, `ScheduledInstallTime=3`) under `HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU`, applied by ONE new managed run-command `b346-wu`, before values saved, UNDO written not run, read-back asserts exactly two values added. Part 2: one records branch `records/b346`: 3 C-entries (hosted deploy; SM VM access incl. B306, B337 and Part 1; B329 shape), 9 Jira comments, 3 Done transitions (-298/-299/-300 per Tuesday's R-R10-1, B316 now deployed), 2 tickets (B316 FOUND-3; cleanup candidate), 5 history entries, 15 catch-up files. Expected last line `DONE: B346 ... 3 C-entries, 2 tickets, 9 comments, 3 Done`. Model: Opus 5.5 (`claude-opus-5-5`), row C6 by analogy for Part 1; Part 2 alone is row C2 (Sonnet 5.5, `claude-sonnet-5-5`). I executed nothing the brief describes.

## MEASURED (by me, read-only)
- B337 brief and STATUS read whole. The WU facts: policy key `...\WindowsUpdate` empty, `...\WindowsUpdate\AU` holds `AUOptions=4`, `NoAutoUpdate=0` and nothing else (`B337_evidence/s1-guest-read.txt:19-26`). No `ScheduledInstall*` value is listed there. B337 says "no 'no auto-restart' policy, active hours not set by policy" (`B337_STATUS.md:47`).
- B316 STATUS (340 lines, last line `DEPLOYED: c149a30 @ ao-MW9SSW6F032uELvuyv`), B329 STATUS (185), B337 STATUS (218), B306 STATUS, B315 brief (161 lines) and STATUS (154) read; every line cite in the brief was checked against the file (three were wrong in my first draft and fixed: VM-names cite, the boot-time hint, the B315 correction cite).
- B329's two shape files exist at `1_Project_Definition/Content/hpsm-sm-3.16/` (8,175 B and 12,083 B). The project root has no `Content/` at its top; the path is under `1_Project_Definition/`.
- `.tools/b346` and `.tools/wt-b346` do not exist; `.tools/b315/` holds the helper set named in the brief.
- Model rows: `model-routing.md:92` (C2, Sonnet 5.5 first for records), `:96` (C6, Opus first for deploys); `models_latest.json` checked 2026-10-20 20:55:31 +1100: opus `claude-opus-5-5`, sonnet `claude-sonnet-5-5`.
- The records precedent files Jira (B315: 3 comments, 2 tickets, HPSMPOC-301/-302) with C-entries and history on a `records/bNNN` branch; `BACKLOG.md` and `JIRA.md` are not written by records seats (B293, B315).

## RELAYED (not re-measured)
- Records `main` = `9af1d55` after #124, C-123 at `CLARIFICATIONS.md:1854` (daily note 11:45 entry; `B315_STATUS.md:81`). Next C-numbers C-124..C-126 are an expectation.
- Tuesday's rulings on B337's four items and the WU sentence (daily note 21:32 entry); R-R10-1 (Done only after the hosted deploy is verified) and R-R10-3 (B306 records go to a later seat) from the B315 brief stamp.
- Budget card `hpsmpoc-sm-vm-budget-24x7-1020`: status OPEN is inferred from the 21:32 note; the seat reads it with `decision_queue.sh show`.
- Others: no HPSM-POC seat live (commission, Tuesday's tmux list 21:33).

## UNMEASURED (the brief makes the seat measure each, or STOP)
- The guest's time zone (no file states it; two files hint Sydney time). `ScheduledInstallTime` is guest-local, so the brief STOPs Part 1 unless `Get-TimeZone` reads `AUS Eastern Standard Time`.
- Whether the Windows Update agent re-reads the policy without a service restart (the brief reads the COM effective settings and forbids restarting anything to find out).
- Records `main`, Jira keys and statuses, code `main`: my `git ls-remote` on the records repo failed (the repo's `core.sshCommand` names another machine's identity file), so GitHub was not reached at all.
- The count of managed run-commands now on the VM (B329 read 13; B337 added one); the seat lists names only.
- Whether HPSMPOC-290/-267/-293/-275/-263 are already Done (B293 closed 7 Done; the brief has the seat read each and not transition them).

## Conflicts with the project's rules, and how the brief handles them
1. **"No person's name" in Jira/C-entries vs Kam's verbatim 18:55 words (which contain "Paul") and the account name `hpsm-sm\paul.waite`.** The brief scopes the exception to C-125 only (verbatim quote and the account id the undo needs); Jira texts and history name no person.
2. **Self-contained project (`CLAUDE.md:40`) vs K8 (a), a Composer card.** The brief tells the seat to cite `B329_STATUS.md:44` and not open Composer files.
3. **Hold on HP material:** B306/B337 copies contain a public IPv4 (a laptop, `B306_STATUS.md:41`) and the VM's public IP; they are byte copies, listed under HPWIN, not edited.
4. **R-R10-1 says Done after deploy; B316's text says the two test tickets (-291, -227) are "on the demo",** but the packages hold 0 test files (`B316_STATUS.md:116`). The brief skips a deployed line for them and says why.

## Questions for Tuesday (each with my recommendation)
1. **One Opus seat or two?** Part 1 is a short reversible VM change; Part 2 is records (Sonnet 5.5, row C2). Recommendation: ONE Opus seat as written (one Step 0, one STATUS, and the Done transitions benefit from the stronger model); split into B346 (Part 1, Opus) and a Sonnet records seat only if the account gauge is the constraint.
2. **Include B306's three files and its facts in C-125 and history?** B315's R-R10-3 left them to "a later seat" and no later seat exists. Recommendation: yes (default in the brief); strike the B306 bullets and the "13" catch-up count (becomes 10 plus the 2 Content files) if you want it elsewhere.
3. **If the guest zone is not Sydney, STOP or adapt?** The brief STOPs. Recommendation: STOP. A UTC-based day/hour would drift by an hour at the April daylight-saving change.
4. **Done transitions on -298/-299/-300 now?** The brief does them (R-R10-1 ruled; B316 `DEPLOYED:`). Recommendation: keep, since Done means merged, gated and deployed; strike the transition column if you want the product owner's say first.

## Stamp and launch notes
- Tuesday fills `STAMP_TIME` (one slot), keeps a `.pre-stamp` copy as the refuse control, and replaces the last line ("READ-WHOLE-BY-TUESDAY: not yet") after reading.
- Launch line is B337's form with pane `Datasec/HPSM-POC-D7`, `BRIEF_SEAT_LEVEL=opus`; `WED_USAGE_STOP=100` is kept only under the 2026-10-20 no-90%-line grant (RELAYED from B337's launch line).

## Fence
- Wrote only the two files named. No `.pre-stamp` copy, no Artifact/Docs/mail/publish tool, no `az`, no HTTP, no Jira write, no credentials file opened.
- **One slip:** my first Bash call began with a `cd` (the project's hook refused it before it ran, so it had no effect); I then used absolute paths only. One `git ls-remote origin` against the HPSM-POC records repo (a git read verb, allowed) failed on its identity file; nothing was changed.
- I read Tuesday's daily note (`grep -n` and `sed -n` on a few lines) for the rulings, as the commission directed; I did not open the decision store, Composer, `Source_Documents/` or any credentials.
