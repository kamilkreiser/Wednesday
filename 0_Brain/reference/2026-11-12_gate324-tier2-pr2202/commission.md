# Gate 324, TIER 2 (Sonnet; routing v1.0 tier-2 row: shell TEST files + one new suite + a docs fragment pair, no product code, no service source, no config). Seat A 24th's row A4 = KS-1728 batch 3 = PR 2202. Commissioned 2026-11-12 ~11:1x AEDT by the 11:0x Wednesday seat.

Method: copy-and-change of `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate320-tier2-pr2196/commission.md`. Read it whole: its Constraints, output shape and controls all apply. Calibration: gate 320's and gate 322's verdict.md.

Pins (Wednesday's `git -C <checkout> ls-remote origin` 11:1x; RE-READ at start and end, and say if either moved): develop 697f422f1a394ab00454ced051f018556573837e; refs/pull/2202/head 3c2b6ebe2ab86e679038c50c508f63dc60b76adf. The branch was cut on d35f75875275; develop moved by one docs-only commit (Blockchain/Dev/docs/METERING-USAGE-API.md), so merge-tree onto 697f422f1a39 (each side's own merge-base; never `git merge-file` with a hand-chosen base: ledger 2026-11-12).

READY (read whole; reproduce, do not trust): `ready_a24_ks1728b3_mail.txt` in THIS folder.

What the row claims (from the READY, unverified by Wednesday):
- 28 grading lines across ten shell test files move off a closing pipe (`printf … | grep -q` under pipefail) to a here-string or a `[[ ]]` match; the 2 git-fed lines in pre_push_hook_current_develop (53, 57) capture git output first. Scope = the ticket's 26 + those 2, predicate = batch 2's class with `[^|]*` narrowed to `[^|;&)]*`; five `-eq` false positives in docs_fragments (344, 350, 379, 387, 394) deliberately excluded.
- A new suite `ks1728_batch3_test_files_grade_without_a_closing_pipe` (126 lines) that is RED against develop's ten files (12 failed) and GREEN at the head.
- A fragment pair (the KS-1728 batch 3 flow fragment, 20 + 25 lines).

Questions:
1. Behaviour preserved: for EACH of the 28 changed lines, does the new form grade the same inputs the same way (pass AND fail)? Plant one failing input per file family (positive shape, negative `[[ ]]` shape, git-fed shape) and show the old and new lines agree on it. A form change that silently always passes is the defect this gate exists to catch.
2. The new suite: RED at develop for the right reason (read which cells fail and why), GREEN at the head; a planted closing-pipe line in one of the ten files must turn it RED (independent control: a file the seat did not choose).
3. Completeness: run the SUITE'S OWN predicate (never a hand grep) over the whole test tree at the head: does any closing-pipe grading line remain outside the 28 + the five documented exclusions? Name each.
4. The ten suites themselves pass at the head under /bin/bash 3.2 `env -i` (the seat's environment); report counts before/after.
5. docs-fragments check passes with the new pair; a planted defect must exit 1.
6. Census: open PRs and held READYs touching the 13 paths (GraphQL or ls-remote + diff, with a control). The seat names PR 2137 and held KS-937 as editing scripts/check-shared-relink.sh (not the suites): confirm no shared path.

Spark shadow after your verdict: run `2_Project_Files/local-model/gate/spark_gate.sh` / `spark_review.py` with `--pr-body-file`, in the session scratchpad (the Spark tunnel was UP at 11:1x; one request at a time). Record recall/false positives against your findings.

OUTPUT: `verdict.md` in THIS folder. First line: 'PR 2202: GO / GO WITH NOTES / NO GO (at head 3c2b6ebe2ab8; tier 2)'. Findings G324-2202-N, graded. NOT TESTED. The Spark shadow result. If your Write is refused, return the text in full.

Constraints: exactly gate 320's. Read-only on the project checkout (clone into your scratchpad for any write verb). DevMASTER has dropped several times today (enclosure power). If it drops, wait, re-read what you wrote, then resume.
