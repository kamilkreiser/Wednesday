# B1742 commission — decision pack for the product owner from SWEEP-1630 (read-only drafting; two jobs, two drafters)
Commissioned by Tuesday (s293), 2026-11-19. Model: Sonnet (routing row C8). You DRAFT files for Tuesday; you post nothing.

WHY: Kam (live board 2026-11-19 16:26:43): "keep working on other outstanding tickets and the backlog". SWEEP-1630
(`2026-11-19_SWEEP-1630_datasec-backlog-unblock.md`, same folder; read its sections "Holds relied on", "Candidate
decisions" and "Keys by class" whole) found that most of the MPS and Composer backlog waits on a few decisions of his.
His standing rule: anything that waits on him is a card on his board, one decision per card, BLUF first, options, a
recommendation and a default; and a premise under a question to him is verified at source first, or written
"reported, unverified". Tuesday posts the cards after reading your drafts; you never run `decision_queue.sh add`.

HARD EXCLUSION: nothing of Datasec/HPSM-POC (project, repo or Jira board) is read, counted or named.

Common rules: read-only everywhere except your output folder
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-19_B1742_decision_pack/` and your scratch
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s293/d1742/`. Jira GET only (credentials by name in-process from
each project's own `4_Credentials/.env`; the MPS names are JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN: check each
project's key names without printing values). gh under each project's own GH_CONFIG_DIR, `-X GET` only. Git read verbs
only. `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/decision_queue.sh` only as `prior` and `show` and `list`.
No az, no request to any app host, no mail, no jest, no server. No `cd`; no unquoted word starting with `=`; zsh;
absolute paths; never delete; clocks from `date`; every zero with a positive control; never an absence read through
head or cut. Files ASCII, built whole, temp file then os.replace. No credential value anywhere. Kam listens to cards
read aloud: plain words, short sentences, no file paths or ids in the BLUF (they go in a "detail" field).

## JOB A — three card drafts (drafter A)
For each decision below write `card_<id>.json` with the fields: id, client_project, title, bluf, options (each: key,
label, detail), recommended, default, detail (the evidence: every premise with its source and the date you read it, or
"reported, unverified"), prior (what `decision_queue.sh prior` and a grep of the project's CLARIFICATIONS.md returned,
quoted, with your reading of whether he already ruled it), and frees (the ticket keys). Read the form of real cards with
`decision_queue.sh show datasec-morning-plan-1119` and two older ruled cards of the same project from `list ruled`.
A decision he has ALREADY made is not a card: write `NOT-A-CARD_<id>.md` quoting the ruling and what it makes buildable.
- A1 `composer-reviewer-round-hold-1119` (Datasec/Security Composer): the content lanes wait until "the reviewer's
  current review round ends" (the sweep quotes CLARIFICATIONS.md line 1764 and C-92 K6; re-read both, and every later
  entry and ruled card that mentions the review round: has an end been recorded?). Question: has that round ended, so
  the content lanes may start? Options at least: still running, keep holding; ended, start; do-nothing. Verify the 13
  keys and the 17 behind them by reading each ticket's status and its blocking line.
- A2 `composer-guided-hold-1119` (Datasec/Security Composer): C-71 COMP-2 (a) "No Guided work until you turn it back on"
  (re-read it and anything later about Guided). Question: stays off, turn back on, or off for good (then the ten
  tickets are closed as not wanted, by him or on his word). Verify the ten keys.
- A3 `mps-hosted-deploy-and-seed-secret-1119` (Datasec/MPS Commercial Calculator): the sweep says 11 tickets wait on a
  hosted deploy of main and on an expired client secret of the seed identity (MPSCALC-395). MPS hosted is
  card-per-deploy by a standing rule. Verify at source what can be verified WITHOUT az and without touching a host:
  the tickets' own text and comments, CLARIFICATIONS.md line 1708 and later entries, the repo's deploy runbook and any
  record of the last deploy; say plainly what stays "reported, unverified" (which commit the hosted site runs; the
  secret's state). If the secret renewal is his hands in a portal, the card's default action lists it as HIS step in
  plain words, separate from the deploy question. If these are really two decisions, draft two cards.
Also write `A_REPORT.md`: per card, premises verified / unverified, prior rulings found, and your recommendation.

## JOB B — two documents for his reading (drafter B), MPS Commercial Calculator only
- B1 `MPS_words_pack_v13-4-1.md`: the sweep's decision M1: 35 tickets wait on customer-facing words (labels, proposal
  text, help topics, the Enterprise book text, the hint catalogue) for the v13.4.1 lanes. FIRST find prior work: was a
  words pack for these lanes ever drafted or sent (search the project's 1_Project_Definition, its Briefs folder,
  CLARIFICATIONS.md for C-45, C-109, C-116 and "word", Tuesday's briefs folder, and ruled cards via `prior`)? If one
  exists, do not redo it: report where it is, what he ruled on it and what remains. Otherwise assemble, per ticket, the
  EXACT words each ticket proposes or needs (quoted from the ticket or its source document, never invented), where they
  would appear, and what is missing (a ticket that needs words nobody has drafted is listed as "words not drafted",
  with the source material that would supply them). You do not write new customer words yourself. Group by lane.
- B2 `MPS_open_questions_sheet.md`: the sweep's decision M3: the open "Questions for Kam" (Q-03, Q-09, Q-10, Q-13, Q-14,
  Q-16, Q-17) and the four design-rule tickets (MPSCALC-110, 288, 314, 360). For each: the question word for word from
  its source, what is already answered and where (the sweep says D-10 may answer Q-10 and that 288 was ruled
  2026-10-25: check each at source), the options the source offers, the tickets it frees, and a recommendation only
  where the source material supports one. A question already answered is listed as ANSWERED with the quote.
Also write `B_REPORT.md`: what exists already, what you assembled, what is missing, and what you did NOT read.

First line of your reply: `PACK A: <n> cards, <m> not-a-card` or `PACK B: words <n> tickets covered, questions <k> open`
(or `STOPPED: <why>`), then at most 20 lines.
