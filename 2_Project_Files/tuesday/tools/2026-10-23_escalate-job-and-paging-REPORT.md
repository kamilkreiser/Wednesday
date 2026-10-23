# 2026-10-23 escalate48h hourly job + board_count.sh Jira paging (builder report, ~11:35 AEDT)

## Files
- NEW scheduler/jobs/escalate48h.plist.template - label com.@SEAT@.escalate48h, StartInterval 3600, runs `ESCALATE_SEND=1 exec bash <PROJECT_DIR>/2_Project_Files/tuesday/tools/escalate_48h.sh`. Logs go to ~/Library/Logs/<seat>_escalate48h.{out,err} (same as every other job: PORTABILITY 22, launchd cannot open drive paths; scheduler/logs is not used by any template). plutil -lint OK.
- scheduler/install_all_jobs.sh - one `case` line skipping escalate48h unless SEAT=tuesday (same pattern as naspush/trmnlpush). Backup install_all_jobs.sh.pre-1023-escalate48h.
- doctor.sh - new block before the PYTHON TOOLS section: on seat tuesday, `fail` (hard) if com.tuesday.escalate48h is not loaded. Backup doctor.sh.pre-1023-escalate48h. (The existing generic --check sweep only warns.)
- fleet/board_count.sh - jira branch pages on nextPageToken until isLast. Backup board_count.sh.pre-1023-paging.
(All edits copy-edit-mv; no installer was running (pgrep empty). mv printed a harmless "set owner/group" warning on this volume; the new files are in place.)

## Job arms
- bash -n on install_all_jobs.sh and doctor.sh: OK.
- BEFORE (template present, gating not yet added), `WED_AGENT=tuesday install_all_jobs.sh --check`: `MISSING escalate48h on-disk-matches=0 loaded=0` ... `5 current, 1 missing`.
- AFTER, same command: still `MISSING escalate48h` (correct: not installed).
- Wednesday gating: WED_AGENT=wednesday in the Tuesday tree REFUSES (tree/env disagreement guard, by design). So I copied scheduler/ to a scratch tree named WEDNESDAY and ran --check there: `skip escalate48h - the 48h escalation mailer is Tuesday's; seat is wednesday` (it is not counted as expected). Nothing loaded, nothing mailed.
- doctor.sh new check was syntax-checked only (bash -n); not run end-to-end.

## Paging design and arms (HPSMPOC, creds read in a subshell, never printed)
Per-request size = min(BOARD_COUNT_PAGE,100); BOARD_COUNT_PAGE is now the cap on TOTAL rows fetched (default 5000 for jira; linear keeps 250 per request). Fetch stops at the cap with pages outstanding => refuses (rule 1). A request error or empty page mid-way refuses. Rule 2 unchanged. Per-status breakdown on stderr. Cosmetic: the OK line says "limit was 5001" (cap+1 passed to the unchanged guard).
- `project = HPSMPOC` -> TOTAL=325 (203 Done, 119 Backlog, 3 In Progress). Newest key HPSMPOC-325. Matches 11:06.
- `project = HPSMPOC AND statusCategory != Done` -> TOTAL=122 (119 Backlog, 3 In Progress). Matches.
- Zero arm: `text ~ "zzqxvbw"` did NOT return zero - Jira's text search is fuzzy and returned 14 (12 Done, 2 Backlog); do not use it as a zero control. Substitutes: `project = HPSMPOC AND key = HPSMPOC-999999` and `project = HPSMPOC AND created > "2099-01-01"` both REFUSED with UNVALIDATED ZERO (exit 1); with BOARD_COUNT_ZERO_OK set the latter prints `TOTAL=0 (UNVALIDATED-ZERO discharged by control: ...)`.
- Cap arm: BOARD_COUNT_PAGE=150 on `project = HPSMPOC` -> `TRUNCATION SUSPECTED ... fetched 200 rows (cap 150) and Jira still reports more pages`, exit 1.

## How Tuesday installs (do not run from the builder)
    bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/scheduler/install_all_jobs.sh
(from her own tree, WED_AGENT unset or =tuesday; this loads com.tuesday.escalate48h and leaves the other jobs "unchanged"). Verify: `bash .../install_all_jobs.sh --check` shows `ok escalate48h`, then doctor.sh. Note it fires hourly with ESCALATE_SEND=1 as soon as loaded (no RunAtLoad, first run is within the hour); to test first, run `bash .../tuesday/tools/escalate_48h.sh --dry-run`. Commit is Tuesday's.
