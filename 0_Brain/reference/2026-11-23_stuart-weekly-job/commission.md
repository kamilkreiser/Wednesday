# Commission: the weekly Monday Stuart-meeting list (WED tooling, claim `stuart-weekly-monday-list`)

**Commissioned by Wednesday, Mon 2026-11-23 10:2x. Builder: a Sonnet tooling sub-agent (routing row C8). Repo: /Volumes/DevMASTER/WEDNESDAY (Wednesday's own tree; you may write here only).**

## Kam's words (the spec, verbatim, live board 2026-11-23 10:22:08, a note on card secuura-stuart-meeting-items-1123)

> "please create a formatted PDF that I can easily reference during the meeting.  Also create a weekly schedule to create this list every Monday morning by 10am and post on fleet activity card for me with link to download"

The PDF half is DONE (today's model output, read both before you design anything):
- research output: `0_Brain/reference/2026-11-23_stuart-meeting-items/items.md` (12 items, each measured, with sources)
- meeting layout: `0_Brain/reference/2026-11-23_stuart-meeting-items/Stuart-meeting-2026-11-23.md` -> rendered by `2_Project_Files/tools/md2pdf/md2pdf.sh` to the `.pdf` beside it.

## What to build

A job that, **every Monday, has the list ready by 10:00 local (Australia/Sydney)**, unattended:

1. **Research** (read-only): produce `0_Brain/reference/<YYYY-MM-DD>_stuart-meeting-items/items.md` in the same shape as today's items.md: BLUF + sections A Decisions only Stuart can make / B Waiting on Stuart or Peter / C Things Stuart should know / D Long-term + "Not verified / limits". Sources the research must read: the Secuura Linear board (team KS) READ-ONLY with the project's own key sourced transiently from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env` (verify the path and the variable name exist before relying on them; never copy or echo the key; never write to that board); the decision store (`2_Project_Files/tools/decision_queue.sh list ruled` / `show <id>`, cards mentioning Stuart or Peter); `0_Brain/tasks/NEXT-PICKUP.md` top block (merge/deploy counts). Counts follow the board rules: unbounded (page until hasNextPage false), predicate stated, `comments(first:50)` sorted client-side, never `last:N`. Write a `commission_research.md` prompt file in the tool folder that carries these rules; today's items.md is the golden shape.
   **Mechanism:** a headless Claude Code run (`claude -p` with the research prompt file; read-only tools; model Sonnet: read the exact id from `0_Brain/dashboard/data/models_latest.json`, never type one from memory). FIRST establish that `claude -p` works when launched from launchd (PATH, auth, cwd): measure it, do not assume. If it cannot run unattended, STOP and report what blocks it with the measurement; do not build a fallback that skips the research.
2. **Layout**: turn items.md into `Stuart-meeting-<date>.md` in today's meeting layout (ask / why / blank answer line per item; "not checked" marked; Sources and limits last). Either the same headless run writes it, or a deterministic converter: your choice, stated with the reason.
3. **Render**: `md2pdf.sh` (rc 0 and a page count, else failure).
4. **Share + card**: put the PDF in the live board's file drawer and post ONE fleet-activity card for Kam with the download link. Read how `2_Project_Files/tools/chat_reply.sh --file` shares a file (dashboard-cloud/seat/share_file.py, file_id) and how `decision_queue.sh add --json` posts a card (JSON on stdin; `_override_prior` key if the prior-rulings gate refuses a weekly repeat: the weekly card is a new agenda each week, state that in the override). Card: id `secuura-stuart-meeting-items-<MMDD>`, client_project `Secuura/Blockchain`, title "For this week's meeting with Stuart: N items, three that most need him", BLUF = the top three + the download link/file id, options a "Raise as listed" / b "Change the list", recommended a, default a. Use today's card (`decision_queue.sh show secuura-stuart-meeting-items-1123`) as the golden.
5. **Schedule**: a launchd job via the tracked-template pattern: `2_Project_Files/scheduler/jobs/stuartweekly.plist.template` (placeholders @PROJECT_DIR@ and @SEAT@ as the other templates), registered in `2_Project_Files/scheduler/install_all_jobs.sh` for the **wednesday seat only** (Secuura is Wednesday's; never Tuesday's machine). Start time Monday **08:00** local so a slow run still lands before 10:00; the script itself refuses to post a second card for the same Monday (idempotent: a marker in the dated folder).
6. **Loud failure** (rule: a refusal nobody reads is indistinguishable from working): any failed step posts ONE panel line to Kam via `chat_reply.sh --project Secuura` naming the step and the log path, and the log keeps stderr (never `2>/dev/null`).
7. **doctor.sh**: a check that the job is loaded (`launchctl list | grep`) and prints the last run's result; PORTABILITY.md line if anything machine-local is new (claude binary path, Chrome for md2pdf).

## Rules that bind you
- Write only inside `/Volumes/DevMASTER/WEDNESDAY`. Never edit any file under `/Volumes/DevMASTER/!CODING/`. Read-only there.
- Never delete files: quarantine (move into a dated `_quarantine_YYYY-MM-DD/` folder) if needed.
- Scripts: bash 3.2 compatible (macOS), no `declare -A`, no `timeout` (use perl alarm or a background watchdog), self-locating paths, stderr kept, `<<'EOF'` heredocs. Do not run `cd` in the Bash tool (a hook refuses it): use absolute paths.
- Before arming: prove BOTH paths in the real environment. (a) fire path: run the script end to end with a `--dry` flag that does everything except the share and the card post (research, layout, render), and show the PDF's page count; (b) quiet/idempotent path: a second run for the same Monday refuses; (c) failure path: force one step to fail (e.g. a bogus md2pdf input) and show the panel line would be sent (use a `--no-post` flag that prints the line instead of posting). Do NOT post a real card or share a real file today: Kam already has today's card and PDF. Do not load the launchd job: leave `install_all_jobs.sh` updated, and report the exact install command for Wednesday to run.
- Headless claude runs cost usage: run the real research at most ONCE during testing.
- Commit your files by pathspec in the WEDNESDAY repo with a message starting "WED tooling: stuart-weekly" and ending with the line `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`; push only if `git -C /Volumes/DevMASTER/WEDNESDAY push` succeeds cleanly without a force; if it is rejected, pull with rebase once, then push; never force.

## Report back (your final message; Wednesday reads it whole)
FOUND / TESTED (what, and what was NOT tested) / HOW (commands, controls) for: claude -p under launchd, each step, the three paths above; the files written (paths); the commit SHA and whether it is pushed; the install command; anything you could not do and why. Name any assumption you could not measure as "unmeasured".
