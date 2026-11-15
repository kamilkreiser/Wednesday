STARTABLE: YES

# B1583 DRAFTER REPORT (kit for seat R236, HPSM-POC records pass: ticket the action plan for the reseller reviewer's feedback, per the 2026-11-15 17:16 ruling)
Drafted 2026-11-15 17:31:35 to 17:5x AEDT (`date`; first read 17:31:35, sidecar measured 17:47:56, last check 17:49:45, report written after). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1583_SEAT-R236_hpsmpoc-records-reviewer-feedback.md` (296 lines, sha256 prefix `bab26fe29e776d9b`; 14 four-underscore lines = 13 Stamp slots + the last line; 0 `@X@` tokens; 0 non-ASCII characters; 0 card ids). Sidecar `.md.measured`: 93 claims, every one measured by program (`fleet/state/s278/d1583/measure.py`). `stamp_check.py <kit>` exits 0 ("93 claims, 93 measured, 0 not measured"). Model: Sonnet (`claude-sonnet-5-5`, with the level written inside the launch quotes). Sources: rows C7 (line 97) and G3 (line 110) of `model-routing.md`; the model id at line 23 of `models_latest.json`; `brief_seat.sh`, which defaults to Opus at line 31.

## BLUF
1. **The kit sets up 14 Jira writes and 1 entry, and moves nothing.**
   - **9 new Tasks** (W1 to W9), each one plan item:
     - F1, Partly answer on Q1: awaiting the product owner's words.
     - F3, Q4 keep or reword: `awaiting-hp`.
     - F4, covered another way: awaiting words.
     - F5+F6, question order (one ticket, as the plan says).
     - F7, the reviewer's two replacement questions.
     - F9, how each answer is known.
     - F10, re-edit an approved narrative.
     - F11, contents page with links.
     - F12, R-001 timeframe: `awaiting-hp`.
   - **5 comments** (W10 to W14):
     - HPSMPOC-241: the plan's section 5, four questions for the vendor, verbatim.
     - HPSMPOC-476: F2.
     - HPSMPOC-474: F13, the plan's optional comment.
     - HPSMPOC-392: F14, the plan's optional comment.
     - HPSMPOC-87: the 16-question ruling. This text is mine.
   - **One entry, C-373**, through a records PR in the analysis repo, by the R234 route (head-pinned merge commit).
2. **The texts are the plan's own, copied by program.** `texts.py` reads ACTION-PLAN.md (sha256 prefix `07ebb84bccfbbcb7`) by line number. Eight transforms are declared (T1 to T8) and nothing else changes. The kit's 14 frozen bodies equal the built ones byte for byte (14 of 14, checked by program). Only the 9 summaries and the HPSMPOC-87 comment are my own words, because the plan gives no summaries.
3. **Prior work: none.** No ticket, comment or entry already records any plan item:
   - Board phrase searches each read 0 (control `firmware` 22): reseller reviewer, mixed fleet, compensating, covered another way, brought up to date, table of contents, contents page, stated by the customer, How do we know, reapprove, Q-CS-05, Q-CS-07, Q-CS-13, D-002, D-010, D-011, D-016, D-018, R-001, hardware purchase, partial answer.
   - All 14 markers read 0.
   - HPSMPOC-241 has 0 lines naming WXP, EWS or automat.
   - Records main has 0 lines for `reseller reviewer` and 0 for `keep the 16 questions`; bounded `C-373` is 0.
   - No key above 484 exists.
4. **One real conflict needs your call (Q-1).** The plan's texts use "HP" as a prose word 10 times, in W1, W2, W9, W10, W11 and W13. The records-seat scanner convention bans that word. The commission says "verbatim". The kit therefore carries a slot, HP-WORD, with VERBATIM or HOLD; I recommend VERBATIM. Every other ban passes with 0 problems. One banned word, "seat" in the 241 text, is changed to "agent" (T5, Q-2).

## Facts re-measured (instrument, time)
- **GitHub** (`gh api -X GET` under the project's `GH_CONFIG_DIR`, 17:33):
  - Code main is `f32b209bfa6f33c3c0268c1daa76753c816b316e`, 1 parent `8766b253`. `compare f32b209...main` reads identical. Open code PRs: 0.
  - Records main is `a91447c45f7ff25a1b0276250b7cca313128a78c`, which is #202 with 2 parents. #201 `d43f6bec` and #200 `51eebb62` also have 2 parents each.
  - Open analysis PRs: 0. `records/b1583` refs: 0 (control `records/b1575` 1).
  - `CLARIFICATIONS.md` raw read: 2090175 bytes, 6347 lines, sha256 `e3b3bf11b0a2cab2`. Headings: C-263 [5114], C-358 [6196], C-371 [6329], C-372 [6340]; C-373 and C-374 absent.
  - Bounded `C-373` reads 0. The bare string sits on 5 lines, all inside `HPSMPOC-373`, so the kit counts only the bounded form.
- **Code at f32b209b** (raw contents, `awk NR==n`):
  - Every pointer in the kit's table printed its fragment. The `client/` copies of the package and ruleset differ from `packages/` and `rulesets/` (`cmp`; 4435 and 2771 lines against 4727 and 3579). The texts' bare file names mean the latter, and the kit says so.
  - The package has 16 Q-CS questions, all yes-no-unsure. On screen Q-CS-13 is 9th, Q-CS-06 5th and Q-CS-05 11th. Section weights: S1 26, S3 9.
  - W4's order list is 16 distinct ids numbered 1 to 16.
  - Line 80 of `registry.ts` names 0.6.1 as the snapshot start package.
  - `ReportModelBuilder.cs:414` maps asserted to "stated by the customer", and `:371` lists the five words.
- **Jira** (my own GET-only reader `d1583/jget.py`; 0 non-GET methods by grep; every JQL is `project = HPSMPOC AND ( ... )`):
  - Board: 484 issues, highest HPSMPOC-484. Status counts: 347 Done, 134 Backlog, 3 In Progress.
  - Comment targets:

    | Ticket | Status | Comments | Newest comment |
    |---|---|---|---|
    | 241 | Backlog | 3 | 41028 |
    | 476 | Backlog | 0 | none |
    | 474 | Backlog | 0 | none |
    | 392 | Backlog | 2 | 41175 |
    | 87 | In Progress | 5 | 40893 |

  - Comment 38607 on HPSMPOC-87 holds "(16, 20 or other)".
  - Labels: `rec-2026-11-15` 3, `needs-product-owner` 1, `awaiting-hp` 10. `reviewer-feedback` is new (0).
  - Priorities: Medium on 448 of 484 issues. Types: Task on 466.
  - 33 summaries on the board use "HP" as a word, for example HPSMPOC-241 and HPSMPOC-181.
- **Plan and sources:** ACTION-PLAN.md has 292 lines, 36549 bytes, sha256 `07ebb84bccfbbcb7`. Quote checks by program: every double-quoted fragment in the 14 texts is a substring of its source (the package, the ruleset, `QuestionBlock.tsx`, `SecurityDashboard.tsx`, FEEDBACK.md, the cards or the commission), with two exceptions:
  - W5's "administrative settings ... device configuration" is the plan's elision of the reviewer's Q12 sentence.
  - W8's "Table of contents" is the plan's proposed heading.
- **Cards (read with `decision_queue.sh show <exact id>` into `d1583/cardq1.raw` and `cardq5.raw`):** Both are open, not ruled; each file is 11 lines with the id on 1. W1 and W3 quote the cards' proposal text and their options a to d verbatim, and no card id is written.
- **Scan** (`d1583/scan.py`, a marker-only copy of the B1575 drafter's scanner with stale fixtures repointed; selftest 90/90 PASS):
  - Over the 14 texts filled with stand-ins: 0 problems other than hp-word, on 6 items, and W10's by-design 8 paragraphs.
  - The entry template reads 0 problems over 11 lines, and each of the 8 controls fires.
  - Summary lengths: 178, 182, 187, 199, 181, 197, 192, 181 and 180.
- **Identity:** the project root's email equals the B1575 records clone's (True) and is not equal to `2_Project_Files` (False). The B1575 records commit's author and committer equal the root email. Values were compared by program and never printed.
- **Panes:** none at 17:32. `Datasec/HPSM-POC-H167` (B1584) appeared by 17:48. The kits of B1584, B1585 and B1586 each contain "Jira: 0 reads, 0 writes" once (grep), so none of them writes Jira or the analysis repo. R236 and B1583 are used in 0 non-`.pre-` kits (control R234 5). Ports: none.

## D-decisions
- **D-1 Ticket set.** It follows the plan item by item:
  - F5 and F6 share one ticket, as the plan says ("also covers F6 and the order part of F12").
  - F8 gets none; the plan says nothing is owed.
  - F2 is a comment on HPSMPOC-476, not a duplicate, because 476's row K3 already holds the question.
  - F13 and F14 are the plan's optional comments on 474 and 392 (slot COMMERCIAL).
  - The 16-question ruling is commented on HPSMPOC-87, whose comment 38607 left the count open (slot RULING-87).
- **D-2 One entry (C-373)**, as the commission says. It records the ruling verbatim, keeping the commission's spacing: three spaces after the first full stop, two after the second. It labels the reading as "an interpretation made when the work was planned, not the product owner's words", because the entry's ban list refuses "Tuesday" and "coordinator".
- **D-3 Transforms T1 to T8** are listed in the kit's PART 1:
  - T1: strip the list prefixes.
  - T3: take the inner text of the plan's quoted comments.
  - T4: an "awaiting the product owner's words" line in F1 and F4, quoting the card, and F1's `[date]` sentence replaced.
  - T5: `seat` becomes `agent` in the 241 text.
  - T6: the one U+2026 becomes `...`.
  - T7: backticks are kept.
  - T8: a records line or sentence before each marker; RECORDS HOLD drops it.
- **D-4 Write order:** creates W1 to W9, then W10 (241), then W11 (476). W11's text says the two questions are "now on HPSMPOC-241", so 241 is written first. W12 and W13 follow, then W14, which lists W1 to W9's keys.
- **D-5 Labels and fields:**
  - Every create gets `rec-2026-11-15` and the new `reviewer-feedback`.
  - F1 and F4 also get `needs-product-owner`, an existing label chosen because the other existing label carries a name.
  - F3 and F12 also get `awaiting-hp`, as the plan says for F12.
  - Type Task, priority Medium (the board norm).
- **D-6 Comments may have more than one paragraph.** W10 keeps the plan's 8 lines as 8 ADF paragraphs. Every other comment is one paragraph. The helper rule changes to match.
- **D-7 Clock:** JIRA DONE +45, RECORDS COMMITTED +85, HARD STOP +120. The kit has a context band and a handover form, because 14 writes is long.
- **D-8 REFUSE 6 guards the build-dependent texts.** If code main moves and a lane P, N or R file has changed, W6, W7 and W8 hold unless every one of their pointers still prints. H167 (lane P) is running now.

## Q-questions for Tuesday (each with a default)
- **Q-1 HP-WORD slot.** Default: VERBATIM.
  - Why: the commission says "the plan's ticket texts, verbatim". The ban is a records-seat convention, not a project or DRAFTER_RULES rule. The board already uses "HP" in 33 summaries, including HPSMPOC-241's.
  - HOLD skips the 6 items with a prose HP: W1, W2, W9, W10, W11 and W13.
  - The summaries, W14 and the entry contain no prose "HP" either way.
- **Q-2 T5, "from any seat" becomes "from any agent" in the 241 text.** Default: agent. "seat" is banned in Jira text. To post the word "seat" verbatim, the scanner's seat rule would need an exemption, and that is not drafted.
- **Q-3 COMMERCIAL (W12, W13), the plan's "optional" comments on 474 and 392.** Default: WRITE. The commission says the other tickets the plan names get a comment.
- **Q-4 RULING-87 (W14).** This is my own text, not the plan's. It records "keep the 16 questions" on the question-set ticket, which left the count open in comment 38607. Default: WRITE. Read the text byte for byte in the kit before you stamp.
- **Q-5 The F4 help line differs between the card and the plan.** The card has `choose Covered another way and say how in the note.` without inner quotes; the plan has `choose 'Covered another way'`. W3 quotes the card, as the commission says ("card wording quoted"). Default: the card's wording.
- **Q-6 Labels.** Default: the new `reviewer-feedback`, plus `needs-product-owner` on F1/F4 and `awaiting-hp` on F3/F12, priority Medium. An alternative is the existing `hp-feedback`, but its 5 tickets are feedback-button items titled "[HP feedback]".
- **Q-7 The 9 summaries are my words.** Default: approve as drafted. Each is under 200 characters, has no prose HP, and passes the scan.
- **Q-8 T8, a records line on each plan text.** This follows the records convention (a line naming entry C-373). Default: yes. RECORDS HOLD removes it by program.
- **Q-9 Slots.** Default:
  - JIRA `WRITE`, CREATE `WRITE`, HP-WORD `VERBATIM`, COMMERCIAL `WRITE`, RULING-87 `WRITE`.
  - MOVE `HOLD`, RECORDS `WRITE`, REC-MERGE `FF`.

## Inputs of every chain step (each from an earlier step or present at BASE)
| Step | Inputs | Source |
|---|---|---|
| 0 | the stamped kit; `df`; `tmux`; `.tools/b1583/` (made here) | stamp; machine; this step |
| 1 | the helpers in `.tools/b1575/` (27 entries, including `jira1575.py`, `scan1575.py`, `post1575.py`, `snap1575.py`, `diff1575.py`, `entries1575.py`, `search1575.py`, `build1575.py`) | exist at BASE (`ls`, 17:32) |
| 2 | code and records main reads; Jira reads; ACTION-PLAN.md and its sha256; the package, ruleset and code files of the pointer table | GitHub, Jira, disk at BASE |
| 3 | the 14 frozen texts and the entry template (kit); Step 2 facts; Step 1 helpers; the plan extraction | kit; steps 1 and 2 |
| 4 | Step 3 payloads and sha256s; slots JIRA, CREATE, HP-WORD, COMMERCIAL, RULING-87; W1 to W9's keys for W14 | step 3; stamp; W1 to W9's read-backs |
| 5 | `.tools/b1575/analysis` (exists at BASE, `core.sshCommand` present) for the `cp -R` route; entry fills from step 4 | BASE; step 4 |
| 6 | the branch from step 5; the parents of the last three merged analysis PRs | step 5; GitHub at BASE |
| 7 | all of the above | steps 0 to 6 |

## UNMEASURED
- **Duplicate checks were made by summary only.** The open hits for `Partly` (27), `asserted` (4), `30-day` (6) and `narrative` (17) were judged from their summaries, not read whole. The kit tells the seat to read whole every open hit on the question set, the narrative, the report or the timeframes. HPSMPOC-87 is the umbrella ticket for the question set, not a duplicate of any item.
- **Plan facts I did not re-derive.** Whether `validate.ts`/`ContentModel.cs` reject a single-choice snapshot question (the plan marks this UNMEASURED; it is not in any ticket text). The plan's decision-document citations (D-002 and the others) are RELAYED; I did not read the decision document.
- **The ruling.** Its wording is RELAYED from the commission; I read no ruling card. The two word cards were read.
- **Ticket references in the texts are not linked.** I did not check whether "the reorder ticket" (W9) and "question on HPSMPOC-241" (W2, W9) should become Jira links. The closed list forbids links, so they stay as text.

## Outside-the-fences disclosure
- **Read:**
  - DRAFTER_RULES.md, the commission, and the B1575 kit (stamped and pre-stamp tail) with its drafter report and sidecar head.
  - The B1575 STATUS: section list, Deviations and last line.
  - ACTION-PLAN.md, FEEDBACK.md, RESULT.md and COMMISSION-ACTION-PLAN.md, all whole.
  - The project's CLAUDE.md and JIRA.md.
  - Header reads of `stamp_check.py` and `decision_queue.sh`; greps of `model-routing.md`, `models_latest.json`, `brief_seat.sh` and `status_watch.sh`.
  - The B1575 drafter's `jget.py` and `scan.py`, copied into my scratch.
  - Greps of the B1584, B1585 and B1586 kits for their Jira lines.
  - The header of `.tools/b1575/jira1575.py`.
  - Greps of older kits (B1543, B1523, B1089, the B1461 report) to find where the HP-word rule came from (not found).
- **Cards:** two, by `decision_queue.sh show hpsmpoc-q1-partly-answer-1115` and `show hpsmpoc-q5-covered-another-way-1115`, each into a scratch file. No `list`, no other card. No `fleet/briefs_staged/`, scoreboard, ledger, WEDNESDAY, FRIDAY or non-Datasec tree.
- **GitHub:** `gh api -X GET` only. Code repo: commits, compare, pulls, tree, raw contents. Analysis repo: commits, pulls, matching-refs, raw `CLARIFICATIONS.md`, `rate_limit`.
- **Jira:** GET only, about 150 reads (the searches, one label census over all 484 issues, the ticket reads).
- **Git in the project:**
  - `config user.email` and `user.name` (root, `2_Project_Files`, the b1575 clone), compared by program and never printed.
  - `config core.sshCommand`, existence only; the value was never printed.
  - One `log -1` on `.tools/b1575/analysis`.
  - All with `--no-optional-locks`.
- **The `.env`:** read in-process by `jget.py`. `measure.py` counted the three variable names in it; no value was printed.
- **Hook events:** one refused `echo ======` (zsh `=` expansion); I re-ran it with `----`. Advisories on grep/cut had no effect on any count I report: each count was re-taken untruncated in `measure.py`.
- **Slip:** one command began with a stray assignment `cd_unused=1;`. It was not a directory change, and I typed no `cd`.
- **Wrote:** only the kit, its `.measured` sidecar (made with `--init`, then filled by `measure.py`; one row re-worded by program to name the fills still open), this report, and scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s278/d1583/`.
- **Not used:** az, ssh, docker, HTTP to any app host, mail, or any publish tool.

DRAFTED B1583: kit 296 lines, sidecar rc 0, questions 9
