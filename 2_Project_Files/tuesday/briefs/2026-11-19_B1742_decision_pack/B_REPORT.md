# B_REPORT: drafter B, JOB B (words pack and open questions sheet), 2026-11-19

Clock from `date`: start 17:00 AEDT, files written 17:12 to 17:14 AEDT. Nothing posted, nothing written outside this
folder and the scratch folder `fleet/state/s293/d1742/b/`.

## What exists already (prior work)

- Words: the standing process is per-lane word packs after the build, approved by card at deploy (C-45 option a detail).
  Packs drafted, sent and ruled: list W (C-36), list W2 (C-43), the 346-word B449 pack (C-48), the 55-word pack (C-46),
  feedback triage (C-65), the one-page words and 31 staff strings (2026-11-12), the roll-forward stop words (C-152).
  None covers lanes V2 to V11. Tuesday's own 2026-10-24 pack already says of those tickets: "Words arrive per lane, not
  as one rulings list now."
- The 2026-11-12 words review page (rental proposal vs the mock, plus the unreadable-file sentence) was sent on
  2026-11-12 10:26; no marks recorded.
- Questions: all seven are untouched in CLARIFICATIONS.md; 110 and 288 are answered (C-104, C-69); Q-10 is narrowed by D-10 a.

## What I assembled

- `MPS_words_pack_v13-4-1.md`: 35 tickets, each with its words verdict and its quoted source words. 2 approved
  (129, 139), 2 with exact proposed words awaiting marks (121, 130), 23 with source material only, 8 not drafted.
- `MPS_open_questions_sheet.md`: 11 items. 2 answered (110, 288), 1 half answered (Q-10), 8 open (Q-03, 09, 13, 14, 16,
  17; 314 and 360 are the coordinator's by their own text).

## Findings that change what Tuesday does

1. M1 as worded has nothing to approve: 31 of 35 tickets have no owed words drafted. Choices are Tuesday's.
2. MPSCALC-139 and MPSCALC-129 look blocked on words that were approved (list W items 34 to 45; the 2026-10-14 ruling).
   Jira comments 41307 (139) and the ticket text of 129 are out of date. Records fix, not a card.
3. MPSCALC-110 and 288 are not open questions; the sweep counted them as class R.
4. D-10 a does not answer Q-10 (C-45 says so in terms).
5. The 11-11 register's "other 6" decisions are not identified anywhere readable; some of the seven may sit there.
6. In passing, for the A drafter and Tuesday: `decision_queue.sh list ruled` shows MPS hosted deploys on 2026-11-12
   (DEPLOYED 0bb3ed12) and 2026-11-16 (DEPLOYED 5e800095) and an expired-secret ruling on 2026-11-16; the sweep's
   "not ruled" line (CLARIFICATIONS.md:1708) may be stale. Not examined here.

## What is missing

Words for 23 tickets (nobody drafted them); the product owner's marks on the 2026-11-12 page; the two approved-words
checks on main (that main prints the three approved rental sentences; not re-read).

## What I did NOT read

Other projects and boards (excluded). The 2026-11-11 decision register PDF. The spec, workbook and reviewer's
transcript. HTML:242-281 (Standard proposal body) and the handoff zips/docx. The B100 STATUS words list. The built
product's caps and retention at main. Jira tickets beyond the 48 read in full (35 words tickets, the 11 question and
rule tickets, plus 195 and 316 which were read and not used) and 359, 361, 253, 34, 27. Code at main: file names only
(`gh api -X GET` tree). The local repository clone was not used (it is stale at 2026-10-01). No test, no az, no host, no
mail, no card posted.

## Controls

Zero counts were paired with positive controls: comments (121 returns 1 where the V-lane tickets return 0); file-name
absences at main (`infoHintWords` 1, `ConsolidatedBom` 6, `Lifecycle` 34); K-17 (K-14 returns 1); the Q labels
(Q-03 returns 2, MPSCALC-69 returns 5). `decision_queue.sh prior --title` returned 0 for the control word "deploy" and
was discarded as evidence; `list ruled` and `show` were used instead. Jira reads: GET only, credentials read by name
in-process, never printed.
