STARTABLE: YES (after Tuesday stamps the 7 slots and the last line; PR #233 head adcd0fd6 and main d415a3fe unmoved at 10:34 AEDT; ports 8910-8919 free; no G170 or .tools/b805 anywhere)

# B805 DRAFTER REPORT (drafted Tue 27 Oct 2026 from 10:34 AEDT)

## BLUF
1. One tier-2 Sonnet gate (`BRIEF_SEAT_LEVEL=sonnet` inside the launch quotes; routing row G2, `model-routing.md` line 109; id `claude-sonnet-5-5`, `models_latest.json` line 23) for PR #233 `b800/hpsmpoc-356-strip-invisible-space @ adcd0fd6`, one path, +70 -2, one commit on main `d415a3fe`. Round 1 of 2 on the class "the reader strips Unicode white space as space".
2. The relayed shape ("one line and one row") does NOT match the PR: it is two strip sites, a docstring paragraph and ONE method of 137 subTest rows. The kit records this as a contradiction for the gate to re-measure; not a finding by itself.
3. #233 is OPEN and CI already exists (the B772 shape assumed no PR). At 10:34 `infra (Bicep validate)` (the job that runs this file) was `success`; the three `api` rows and some `web e2e` rows were `in_progress`. The kit makes `infra` on the CURRENT head the CI predicate and caps GO at GO WITH FINDINGS (conditional) if it is not finished.
4. The heart (C3): defect plant (both strips reverted to `.strip()`) must turn the new method RED and the head GREEN, plus an independent arm of six gate-written plants (P1-P6) that must read green at BASE (instrument control) and red at head, with controls (U+200B, inner NBSP, clean file) and a legitimate-edit set that must stay green. C4 covers callers of `step_identity` and the wrong-reason check on negative-asserting cells.
5. Python-only gate (no dotnet): ports bound none.

## Facts re-measured (instrument, control)
- `gh api -X GET pulls/233`: open, head `adcd0fd67fee9eab3707974d676bdfb560760821`, base `d415a3fe...`, changed_files 1, +70 -2, mergeable_state `blocked`. `pulls/233/files`: one path. Control: matches the builder's STATUS.
- `git/matching-refs/heads/main` = `d415a3fe...`. Open PRs: #233, #232, #222.
- `check-runs` on the head: 18 rows; infra success, gitleaks success, CodeQL and four Analyze success, dependency review success, web build/unit success, api and SQL Server shards in_progress. Control: `commits/main/check-runs` total_count 19.
- Head file 891 lines, main 823 (contents API raw, diffed in scratch): additions at 310-312, 325, 339, 788+; the two strip lines read `.strip(" \t")`; `step_identity` appears 15 times at main (control for the callers list); head callers at 765-786, 799-839, 872.
- Round count: loop over first lines of 82 `GATE VERDICT` STATUS files; 6 name white space/Unicode/invisible/strip (B549, B660, B690, B729, B734, B799); none is a NO GO on this class. B734 is `GO WITH FINDINGS` (round 2 of 2) on the neighbouring class "closing the open lists of the shard-job reader", which FOUND B734-3; B729 `GO WITH FINDINGS` is "control-character refusal by the shard ..." (different). Control: B734 prints. The earlier NO GOs on this reader (B669, B677 on #217; B716 on #221) are other classes. Result: NO GO 0 of 2.
- Landing rule: `/usr/bin/grep -n -i -E 'squash|match-head'` over project CLAUDE.md and CLARIFICATIONS.md = one hit, `CLARIFICATIONS.md:138` (PR #27 squash-merged head-pinned). One precedent, not a written rule; quoted as such in the kit.
- CI predicate: `ci.yml` at main lines 14-18 (`on:`), 575-627 (`infra` job, last step `bash infra/scripts/validate.sh`); `validate.sh` line 7 `set -euo pipefail`, line 21 `BICEP="$BICEP" python3 tests/test_security_baseline.py`. Pass predicate written into the kit: exit 0 of validate.sh. That `test_security_baseline.py` loads this file is the builder's claim; the gate must read the loader.
- Ports: `lsof -nP -iTCP:8910-8919 -sTCP:LISTEN` rc 1 (no control bound; the kit has the gate bind one itself). Word-boundary scan of the non-`.pre-` SEAT kits of 10-26 and 10-27 for `891x`: 0 hits; control `886x` hits B799, B800, B801, B804. `tmux list-panes -a`: tuesday, HPSM-POC-D37, MPS-R57, NexusAI-G169, HPSM-POC-H44, HPSM-POC-G168, fleet-monitor (no G170). `ls -d .tools/b805`: absent (control: `.tools/b772` lists).
- Kit self-checks: four-underscore lines 8 (7 slots + last line), `@[A-Z_]+@` 0, non-ASCII 0 (one raw NBSP slipped in because the Write tool decodes a backslash-u escape; found by the scan and replaced), no owner name.

## D-decisions
- D1 Ports 8910-8919, bind none.
- D2 One verdict for the whole PR; one STATUS first line.
- D3 Target 70 min, HARD STOP 110 min after the gate's Step 0 (Python-only, lighter than B772).
- D4 Unnamed-character survivors: a `str.strip()` whitespace character outside the builder's disclosed set (U+0085, U+2028, U+2029 are disclosed rulings) that stays green is Major SAME; the line-break characters and the ref after the `@` are Notes (B734-9, B734-6).
- D5 The builder's `rstrip` survivor must be re-proved equivalent by the gate's own fuzz, else a Note.
- D6 The sibling strip sites (nine green, three caught elsewhere) are Notes, not findings against the PR.
- D7 Round-1 findings are `B805-n` (single PR).

## Q-questions for Tuesday
- Q1 Does B734's class ("closing the open lists of the shard-job reader") count as this class? Default: NO, different class, round 1 of 2. The gate raises a Q if it disagrees, never rules.
- Q2 The PR is open and CI has run: should the gate also judge the finished api and web rows? Default: NO, they cover nothing of this test-only infra path; the gate reads `infra (Bicep validate)` on the current head and states the others are not evidence.
- Q3 The relayed fix shape ("one line and one row") became 137 rows in one method. Default: accept, record the contradiction as a Note; judge the rows by the plants.
- Q4 Run the whole-infra suite at main as well as the head (about 70 s each)? Default: YES, cut after C3/C4 if the hard stop nears.

## UNMEASURED
No python test, clone, fetch or plant was run. Not measured: the method's row count and the builder's red counts (85, 32, 101); P1-P6; how `test_security_baseline.py` loads the reader; whether the real `ci.yml` shard job carries an edge `str.strip()` character; the finish of the in_progress rows; the runner's Python; the commit message beyond its first 600 characters; the Q for the PR title versus the builder's suggested title (differs slightly, not a finding).

## Outside-the-fences disclosure
Read-only: DRAFTER_RULES.md, the B772 and B734 and B800 kits, the B800 STATUS, first lines of the `*_STATUS.md` files (a loop, plus B734/B772/B716 first lines and B734 line 449 context), the B772 drafter report, `brief_seat.sh` lines 18-25, `model-routing.md` lines 105-112, `models_latest.json` by grep. `gh api -X GET` only under the project's `GH_CONFIG_DIR` (pulls, files, check-runs, contents raw at main and head, the commit message, matching-refs, `check-runs` of main). Contents of `ci.yml` and the two reader versions were written to the session scratchpad only. No decision_queue.sh, no Jira, no fetch, clone or git write, no `fleet/briefs_staged/`, no scoreboard, no `_ledger.md`, no WEDNESDAY/FRIDAY tree, no mail/chat/Artifact/Docs tool. Hook advisories on case-sensitive grep were noted; the counts that matter were paired with a control. One `ls` of the project `.tools` for `b800` count only (3 entries).
