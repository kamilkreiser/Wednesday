# SWEEP-EVENING commission (2026-11-20) -- refresh of SWEEP-1630: what is buildable NOW on MPS and Composer, and where each of its candidate decisions stands (read-only)
Commissioned by Tuesday (seat s299), 2026-11-20. Model: Sonnet (routing row C8). You write ONE document and your own scratch files; you change nothing else.

WHY: the product owner's standing words (live board 2026-11-19 16:26:43, verbatim: "keep working on other outstanding tickets and the backlog.  we will move onto the OXPd project when files are ready.  this will be our next big project"). Yesterday's sweep (SWEEP-1630) is a day old and work has landed since. Tuesday needs today's state before drafting the next lanes and before posting any decision card.

Output: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_SWEEP-EVENING_datasec-backlog-refresh.md`
Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s299/sweep_evening/` (create it).

READ WHOLE FIRST (each listed by Tuesday with `ls -d` in the command before this commission was written; all exist):
1. `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-19_SWEEP-1630_COMMISSION.md` (the form: its fences, its predicate, its output shape; they bind here unless this file says otherwise).
2. `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-19_SWEEP-1630_datasec-backlog-unblock.md` (282 lines: yesterday's result).
3. `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-19_SWEEP-1630_TUESDAY-ANSWERS.md` (Tuesday's answers and two rulings of her own).
4. The instruments in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s293/sweep1630/` (read each before use; copy what you use into your scratch; GET only).

FENCES (as SWEEP-1630, restated): no Jira, GitHub or git write; no mail; no az; no deploy; no request to any app host; no `cd`; no token printed; `decision_queue.sh` (`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/decision_queue.sh`) for `show` and `prior` only, and `list` if it is a read (read its header first); credentials read by name in-process from each project's own `4_Credentials/.env`; `gh` under each project's own `GH_CONFIG_DIR`, `-X GET` only; never delete; nothing under any other client's tree; no test, no build, no server.

## HARD EXCLUSIONS
- **Datasec/HPSM-POC: do NOT sweep, count, read or list its board or repository at all** (the product owner's hold to the end of 2026-12-10). Say in the BLUF that it was excluded and why.
- **NexusAI and OXPd 2 are NOT in this sweep** (NexusAI has a serial queue already decided; OXPd 2 has its own lane plan). Scope: MPS Calculator (Jira MPSCALC; `/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial Calculator`) and Security Composer (Jira PCOMP; `/Volumes/Datasec_DEV/!CODING/Datasec/Datasec Security Composer`).
- **Live now, do not disturb:** a records seat (`Datasec/MPS-R284`, kit B1781) is writing Jira MPSCALC and the MPS root record files while you read. It files up to two new tickets and two comments (MPSCALC-426, MPSCALC-278). Your reads are GET only; if a count moves under you, say so with both readings. Do not take `.tools/.git-lock` in the MPS root; use `git -C '<root>' --no-optional-locks` read verbs only.

## JOB 1 -- what landed since SWEEP-1630, measured at source (not from any note)
For MPS and Composer each: code main now (sha, by `gh api -X GET`), every pull request merged since 2026-11-19 16:30 AEDT (number, title, merge sha, the ticket keys it names), open pull requests, and the newest clarification entry of the project's records (its heading line). For each lane or key SWEEP-1630 called buildable (MPS: lane M-G, MPSCALC-195 + 316; MPSCALC-314 after Tuesday's ruling in the answers file; Composer: PCOMP-44 conditional) say: landed (which pull request), in flight (which branch or kit), or not started, with the line that shows it.

## JOB 2 -- the buildable keys NOW (same predicate as SWEEP-1630, quoted from it)
Re-run the census and the predicate on MPSCALC and PCOMP. List every buildable key with: its scope sentence quoted from the ticket, the files it would touch (read at code main; print the sha), a size guess, a gate tier guess, what would STOP it, and whether it shares a file with another buildable key (lanes must be file-disjoint). A zero is an answer only with the control SWEEP-1630 used. Counts through `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/board_count.sh` (read its header first), never a hand-capped query.

## JOB 3 -- the candidate decisions of SWEEP-1630, one by one
For each candidate decision the SWEEP-1630 document ranks for MPS and for Composer (the answers file names the first five: the MPS words pack for the v13.4.1 lanes; the MPS hosted deploy and the seed identity's expired secret; the Composer reviewer-round hold; the Composer Guided hold; the MPS question sheet):
- Has the product owner ALREADY decided it? Run `decision_queue.sh prior` on its subject words and grep the project's `1_Project_Definition/CLARIFICATIONS.md`; quote the ruling with its entry or card id and date if one exists. (Example to check, not to trust: an MPS hosted deploy of main 50d2a471 was ruled and done on 2026-11-20 by entry C-185 of the MPS records; main has since moved to debb5e28.)
- Is a card for it open now? (`decision_queue.sh` reads only.)
- If it is still undecided: the ONE sentence that would be asked, the tickets it frees today (keys, re-counted today), the default Tuesday could take if he does not answer, and every premise of the question with its source line. Do NOT write a card.
- Every HOLD you rely on: quote the line that sets it and its date; say whether it names an end.

## JOB 4 -- tickets built on main but still open (MPS and Composer)
SWEEP-1630 read 46 on MPS and 4 on Composer. Re-count today. For each (or, if more than 30, for the 30 with the clearest evidence, saying which were not read): the key, the pull request or commit that built it, and whether a client human opened it (those are theirs to close). Propose nothing be closed; Tuesday decides and a records seat does it.

## Output shape
First line `SWEEP-EVENING: <n> buildable keys, <m> decisions still open, <k> built-but-open`. Then: BLUF (6 lines at most); census table with controls; Job 1; Job 2 as proposed file-disjoint lanes; Job 3 as a table plus one paragraph per undecided decision; Job 4; EXCLUDED and why; QUESTIONS for Tuesday (each with your default); FOUND / TESTED (and what was NOT tested) / HOW (instruments, controls, instrument errors). State the frame of every "all tickets" claim. Every zero needs a positive control. Clocks from `date`, never typed. ASCII; build the document whole, write a temp file beside the target, then os.replace.
Your reply to Tuesday: the first line of the document, then at most 15 lines: the lanes you propose, the decisions still open, anything that contradicts yesterday's sweep or this commission (say plainly where this commission is wrong), and what you did not read.
