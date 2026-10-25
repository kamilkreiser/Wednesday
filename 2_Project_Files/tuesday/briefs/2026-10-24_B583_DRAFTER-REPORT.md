# B583 drafter report (SEAT-R30, MPS records for 2026-10-24), written 2026-10-24 about 15:45 AEDT

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B583_SEAT-R30_mps-records-1024-landings-rulings.md` (+ byte-identical `.pre-stamp`, `cmp` clean, 58,288 bytes). Stamp slots: **9 lines** end in four underscores (8 slot lines + the last line); `grep -c` printed 9 on both copies.

## What I read, and how (every sha, count, key, path and option text in the brief)
- Template: B556 brief whole (with its stamp) and B551 brief whole. No ADDENDUM exists for B556 (`ls`).
- Cards: `decision_queue.sh show` of all 11 cards named (5 + 6), option text copied verbatim. Day's rulings: `kam_rulings_today.sh` (13 rows).
- PR facts: `gh api -X GET pulls/102,104,105,106` and `git/commits/<full sha>` for the four squashes (short shas 404 there; the brief says so). Times: 01:15:06Z, 01:50:03Z, 02:48:59Z, 03:24:26Z = 12:15, 12:50, 13:48, 14:24 AEDT, matching your list. Pinned heads match yours. Main = `05c598f3`. No PR open (paginated list: 106 PRs, 104 merged).
- Gates: B575/B576/B580/B581 first lines, findings, round-cap and FOR TUESDAY sections (line numbers in the brief).
- Jira (GET only, creds read in-process from the project `.env`, never printed): highest key 327; `created >= 2026-10-24` = 321..327; `labels = mpscalc-b583` 0; labels/status/comment counts of 316, 204, 261, 153, 176, 295, 321..327.
- Root repo: HEAD `83ea99f` (B556's ff), C-56 highest, CLARIFICATIONS 1145 lines, BACKLOG 2658, JIRA.md 231, history 1104, `records/b583` absent.

## Rulings that already had C-entries
- `mpscalc-pr102-cap-nogo-third-round-1024` = **C-55** (`CLARIFICATIONS.md:1101`) and `mpscalc-body-not-json-object-words-1024` = **C-56** (`:1111`): already recorded, not repeated (their "Delivered: none" is superseded by the new section, not edited).
- **No C-entry** for the other nine, including the readiness card of today (its only grep hits are the older 17 Oct ruling at `:697-706`): C-57 pr105 cell (b), C-58 readiness (a tap superseded by the 09:24 message = effective c), C-59 review list (b), C-60 ink hint (b + note), C-61 176 draft words (a), C-62 204 (a), C-63 261 (a), C-64 316 (a), C-65 176 word pack (a).

## Decisions I made that you may want to change at the stamp
1. **Label removal: NOT allowed by the project's rule.** `JIRA.md` has no line permitting a records seat a label edit; every section B164..B556 is create + comment, and the B551/B556 briefs say "no label change on an existing ticket". So `needs-ruling` stays on 316, 204, 261 (and 153); the seat comments the ruling instead. Slot LABELS-REMOVE default no.
2. **Done transitions: NOT allowed.** `JIRA.md:174/:185/:208`: "no project rule moves a ticket on merge or deploy"; only MPSCALC-67 and -71 were ever moved. So the 74 get one evidence-only comment each (never the word "done"). Slot DONE-TRANSITION default no.
3. **The 74 'strong' keys are not all provable.** My paginated GET of 106 PRs maps **55 of 74** to a merged PR's title/body; **19 are named in no merged PR** (199, 208, 220, 301, 229, 311, 240, 241, 298, 299, 34, 312, 292, 293, 294, 303, 318, 319, 320). The seat must resolve those from squash messages/gate Done-when tables or HOLD them. Several keys map to 2-3 PRs (28, 150, 151, 165, 174); 310 maps only to #99, probably a cross-reference.
4. **Comment volume:** up to ~91 Jira writes (3 creates, 7 ruling/landing comments, 5 carried-FACT comments on 323..327, up to 74 evidence comments). The B556 "one write per command" rule would be impractical, so I allowed a loop driver (one write per step, max 10 per command, stop on first non-2xx, read-back with mutant each) as slot BULK-DRIVER. Hard stop suggestion 3.5 h, target 2 h.
5. **"Carried tickets 323..327" read as "carried open".** B575 says they are unchanged and stay open; the landing closed only B552-1 = MPSCALC-322. So 322 gets a "closed by #102" comment; 323..327 get a "landed, stays open" comment (slot CARRIED-COMMENTS, default yes).
6. **Stray files: two are not zero-byte.** `head-B104CarePackApiTests.cs` is 6,491 bytes (a C# test head) and `/Volumes/Laptop-DEV/!CODING/Datasec/Datasec` is 63 bytes (a script's stray `ALLDONE ...` line); `=`, `Commercial`, `MPS`, `seller` are 0 bytes. You named all six, so the brief moves all six (nothing deleted; sha256 before/after; the `Datasec` move writes outside the project folder, justified only by your instruction and noted in the brief).
7. **Word pack register file.** The seat creates `1_Project_Definition/Registers/2026-10-24_mps-176-feedback-triage-approved-words.md` on the same branch (commit is path-limited to 2 paths). It copies pack lines 22-125 by program (pack sha256 `e720db64...fa64d3`, 135 lines, asserted at launch; mismatch = no file). Two forced deviations from byte-for-byte: line 72 carries a decision-card id (replaced by a topic phrase) and lines 60/80/102 carry U+2026 inside the approved word `Loading...` (kept; the one non-ASCII exception). Pack counts I read: 24 NEW, 20 REUSED, 2 no-words = 46 rows.
8. **Money and names.** C-60 must quote the option label `Show $0.70` verbatim (the ruling's own text); I made it the single allow-listed money token and banned any other rate; Jira text for 153 says "the lower of the two ink rates", no figure. Two card titles/quotes carry the reviewer's name: the brief has the seat write `[name left out]`. The brief copies no card id and no person name (grep: 0 for the reviewer's name and for `mpscalc-...-10dd` tokens).
9. **Tuesday's reading for 153** ("mil" unit, words back before shipping) is recorded as the coordinator's reading in the section and in the Jira comment, not as the product owner's ruling.
10. **Items I added that you did not list:** C-58 (readiness) as an entry; comment on MPSCALC-295 and MPSCALC-322; a #102 landing-supersedes statement in Tuesday's section; a check that C-56's sentence is in main at `459db8b8`.

## Things I could NOT verify (all in the brief's UNMEASURED)
Jira descriptions/Acceptance of the touched tickets and the lane labels for the 3 creates; the 19 unmapped keys' evidence; whether the hosted site moved; the old reference-length wording in docs at `05c598f3`; the "mil" unit in the 16 Oct quote.

## Fences kept
Wrote only the brief, its `.pre-stamp`, this report, plus scratch files in the session scratchpad (`jget.py`, `q1.py`, `pulls.json`). No git write verb, no Jira write, no hosted-site call, no az, no store `list`. One accidental `cd` in a Bash call was refused by the hook and did nothing.
