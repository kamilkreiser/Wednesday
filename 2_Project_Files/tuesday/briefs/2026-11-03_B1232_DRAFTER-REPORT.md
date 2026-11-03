STARTABLE: YES (once Tuesday fills the 9 stamp slots; no MPS pane, no heavy.lock/light.lock under .tools/*, load1 1.79, 202 GiB free, .tools/b1232 absent, origin b1232 ref absent)

# B1232 drafter report: SEAT-M91, MPSCALC-379 + comment half of -381, tests only

Kit: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1232_SEAT-M91_mps-379-template-isolation.md (72 lines, 9 slots by `grep -c -E '_''_''_''_'`, 0 non-ASCII). Slots: 2026-11-03_B1232_slots.json. Clocks (date, AEDT): 20:00:17 start, 20:00:59 main read, 20:03:03 branch census, 20:04:02 last panes/load read.

## BLUF
One file (tests/MpsCalc.Api.Tests/TemplateIsolationTests.cs), one commit, new branch b1232/mps-379-template-isolation off main 0d656f90. Two Assert.Matches lines added inside the existing fact (:337, after :378) plus two one-line comment rewrites (:98, :315). Rows add no test result (counts must be equal before and after). No product byte, no new user-facing word.

## Facts re-measured
- Jira GET (own copy of the b1194 reader, output to scratchpad): 379, 381, 382 Backlog, comments 0; control 361 comments 1. Ticket text quoted in the kit.
- Main `gh api -X GET git/ref/heads/main` = 0d656f90; open PRs 121, 120; matching-refs b1232 = 0 (control b1093 = 1).
- File raw at main: 473 lines, blob be020307, 0 non-ASCII; lines by awk NR/grep -n: :67-68, :98, :315, :337, :370-374 verbatim rows, :375-378 quiet rows, :379, :402-403, :247. Ticket's own pointers (:62-63) are off; comment is :61-65 (not edited).
- Plant anchors: C5 and C9 old strings each count 1 by grep -c -F. Insertion anchor for the probe facts (:403 line) count 1.
- Partition: 178 branches paged; 6 branches matching ^b1(17|18|19|2) compared to main: 0 files matching TemplateIsolation; control compare 069751a0^...069751a0 = 1. compare 9bdf4548...0d656f90: 7 paths, 0 match.
- CI: ci.yml :42/:43, Directory.Build.props :6 (raw at main). CLARIFICATIONS.md :774, :2218 (local file). Model rows :92 C2, :109 G2; models_latest.json :23 claude-sonnet-5-5.
- Panes: tuesday, fleet-monitor, Datasec/HPSM-POC-G325 (G324 is no longer listed). Ports: none needed.

## D-decisions
- D-1 Both new lines sit in ONE fact (the ticket's shape), so under a plant the fact fails at the first failing line; the kit adds a -mut-only probe (two throwaway facts) so each row is seen alone and the C5/C9 orthogonality is measured, not assumed.
- D-2 The two comment sentences are checked by a -mut-only probe (five cases via Violations) before the seat commits them.
- D-3 Plant/runner scripts are written by the seat for the Api project (the b1212 ones plant Engine product files); only helpers are copied from .tools/b1212.
- D-4 381 items 1, 2, 4 and S3p/S4p/C13 stay out; the sentence at :55 (same imprecision, not listed) is reported, not edited.

## Q-questions for Tuesday (default)
- Q-1 Comment wording: (a) "an apostrophe or a quote in a directive, outside a trailing // comment" (b) "misreads these three shapes (a format in a hole only when it holds an unbalanced apostrophe; see CodeOnly)". The ticket gives fix shapes, not final text, and the raw-string case of (b) is also conditional. Default: as printed, the probe decides "or a quote".
- Q-2 Correct the sentence at :55 too? Default: no.
- Q-3 Gate round: ROUND 1 OF 2 (earlier B1186 rounds judged PR #152). Default: yes; confirm from verdict lines.
- Q-4 Sonnet C2 (sweep row). Default: yes.
- Q-5 Hard stop: it is already evening; kit says 60/120 minutes after Step 0. Default: not after the clock you stamp.
- Q-6 Rows for S3p, S4p, C13? Default: no (ticket excludes).

## UNMEASURED
Baseline test counts (Step 3); that the plants turn the fact red (hand derivation only; .NET negated-class-matches-newline is the premise); whether a card cites either ticket (no decision_queue read); the five comment-probe results; Api csproj path (the seat prints it).

## Outside the fences
Read-only: Jira GET (one search, scratchpad copy of the reader), gh api -X GET (refs, pulls, branches, compare, contents, tree, commits), local reads of CLARIFICATIONS.md, model-routing.md, models_latest.json, .tools listings and the b1212 helper files; tmux list-panes, lsof, df, uptime. No fetch, no ref write, no card read.
