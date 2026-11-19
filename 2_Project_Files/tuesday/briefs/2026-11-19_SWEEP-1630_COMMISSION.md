# SWEEP-1630 commission — Datasec backlog: what can be built next, and what ONE decision would unblock the most (read-only)
Commissioned by Tuesday (s293), 2026-11-19. Model: Sonnet (routing row C8). You write ONE document; you change nothing.

WHY: Kam, live board 2026-11-19 16:26:43, verbatim: "keep working on other outstanding tickets and the backlog.  we will
move onto the OXPd project when files are ready.  this will be our next big project". And 16:25:45: "no more HPSM work for
the next 3 weeks or until I request something new". This morning's sweep (SWEEP-1115) found 4 buildable lanes; two have
landed, one is building, one is drafted. MPS read 163 open tickets with 1 buildable and the Composer 78 with 0. That is a
backlog that is mostly BLOCKED, not empty, so this sweep has two jobs.

Output: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-19_SWEEP-1630_datasec-backlog-unblock.md`.
FORM AND INSTRUMENTS: copy `2026-11-19_SWEEP-1115_datasec-actionable-lanes.md` in the same folder (read it whole first;
its instruments are in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s292/sweep1115/`: read each before use,
GET-only; copy them to your scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s293/sweep1630/`).
Fences: no Jira, GitHub or git write; no mail; no az; no deploy; no request to any app host; no `cd`; no token printed;
`decision_queue.sh` for `show` and `prior` only; nothing under any other client's tree. Credentials are read by name
in-process from each project's own `4_Credentials/.env`; gh under each project's own `GH_CONFIG_DIR`, `-X GET` only.

## HARD EXCLUSION: Datasec/HPSM-POC
Do NOT sweep, count, read or list the HPSMPOC board or the HPSM-POC repository at all (Kam's hold, to 2026-12-10).
Say in the BLUF that it was excluded and why. Projects in scope: MPS Calculator (MPSCALC), Security Composer (PCOMP),
NexusAI (RD).

## What changed since SWEEP-1115 (verify each at source; do not trust this list)
Landed: MPS #217 (MPSCALC-415) with its records; NexusAI #230 (history), #231 (RD-793 + RD-990, merge 9373976e) with
records (RD-793 and RD-990 in Testing; RD-1011, RD-1012, RD-1013 filed today); earlier today RD-1008, RD-1009, RD-1010.
In flight: NexusAI lane N-F (RD-835 + RD-861) building; a history pull request #232 under checks. Drafted, waiting its
turn: lane N-J (RD-445 item 2). NexusAI lanes run SERIALLY (one jest lock, one expected-counts file).
Not lanes (already decided by Tuesday): RD-929 is drafted after N-J lands (Opus builder); RD-1006 waits on a question for
the product owner (a census of it exists: `2026-11-19_B1740_RD-1006_audit-write-census.md`).

## JOB 1 — the next buildable keys (same predicate as SWEEP-1115, quoted from it)
- NexusAI: propose the NEXT three serial lanes after N-J. Read up to ~40 candidates not read by SWEEP-1115 (rank: label
  security or records-pass-*, then priority, then newest; include RD-1008 to RD-1013 and the census finding below).
  For each lane: keys, the files it touches (read at main; print the sha), size, gate tier guess, why buildable, what
  would STOP it. Census finding to check on the board and, if no ticket names it, list as "to be ticketed":
  `AUDIT_ACTIONS.SETTINGS_CHANGE` is used at backend/server.js 17353 and 17600 and defined nowhere.
- MPS and Composer: re-run the census and the buildable predicate; list every buildable key (0 is an answer only with
  the control SWEEP-1115 used).

## JOB 2 — why the rest is blocked, and the fewest decisions that free the most (MPS and Composer; NexusAI top 60 by rank)
For every open ticket that FAILS the predicate, one reason class from a closed list you define and print first (for
example: needs customer-facing words; needs a product ruling; waits on a named hold; waits on a client human; needs a
deploy; needs an HP tool or outside system; too vague to build; duplicate or stale; other). Count per class per project
(the counts must sum to the open count: show the arithmetic). Then:
- For each class that a single decision by the product owner could lift, name the decision in ONE sentence, the tickets
  it would free (keys), and whether he has ALREADY decided it: run `decision_queue.sh prior` on the subject words and
  grep `1_Project_Definition/CLARIFICATIONS.md` of that project; quote the ruling if one exists (a ticket blocked on a
  question he already answered is BUILDABLE and belongs in Job 1 with the ruling quoted).
- Every HOLD you rely on: quote the line that sets it and its date; say if it names an end.
- Stale or duplicate candidates: list keys with the evidence; propose nothing be closed (Tuesday decides).
Rank the candidate decisions by tickets freed. At most 5 candidate decisions per project. Do not write cards.

## Output shape
First line `SWEEP-1630: <n> buildable keys, <m> candidate decisions`. BLUF; census table with controls; Job 1 lanes; Job 2
tables; EXCLUDED and why; QUESTIONS for Tuesday; FOUND / TESTED (and what was NOT) / HOW. State the frame of every
"all tickets" claim. Counts through `2_Project_Files/fleet/board_count.sh` (never a hand-capped query). Every zero needs
a positive control. Clocks from `date`, never typed. No jest and no server (a build seat holds the NexusAI lock).
ASCII; build the document whole, write a temp file beside the target, then os.replace.
