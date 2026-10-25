STARTABLE: YES

# B708 DRAFTER REPORT (SEAT-H28, HPSM-POC, lane H-INFRA, HPSMPOC-353)
Drafted Mon 26 Oct 2026 07:5x AEDT (clock from `date`) by the Sonnet kit drafter. Kit: `2026-10-26_B708_SEAT-H28_hpsmpoc-353-ci-workflow-reader.md` (119 lines, 8 lines match the four-underscore pattern: the 7 slots and the last line; `@X@` count 0).

## BLUF
1. Startable now: origin main is still `b069274c` (the sweep's pin), no open PR, no `b708*` ref, the reader file is byte-unchanged since #217 (blob `aef9509c`), so the B677 gate's line numbers hold.
2. The gap is real and re-measured: on the base reader (31 OK, also 31 OK under /usr/bin/python3 3.9.6) the plants d01 (added step), a31 (workflow `env:` with `BASH_FUNC_exit%%`), m01 (duplicate flow-style `strategy:`) and a job-level `env` key all stay GREEN; the planted timeout 30 to 20 control FAILS as it should.
3. The kit specifies three new tests (ordered 12-step list by identity, env/job/workflow key pins, job-level duplicate-key refusal), a one-line `len(set(names))` assertion, and a measured docstring; expected 34 tests (base 31). It loosens nothing; B677-3 rides as docstring only.
4. Ports and base: block 9750-9759 free (lsof rc 1, positive control fired), no live claim (4 old 10-25 kits mention it, none live); the local clone lacks `b069274c`, the builder fetches it under `lock.sh`.
5. Round count needs your word (Q-1).

## Facts re-measured (instrument, control)
| Fact | Instrument | Control |
|---|---|---|
| main = `b069274cfc201bc451ab2c22dc6adc2a6e231bef` (2026-10-25T12:39:06Z) | `git ls-remote origin refs/heads/main` and `gh api -X GET commits/main` agree | `ls-remote` also printed `b629/...` (old head) so the pattern fires |
| open PRs 0 | `pulls?state=open` length | `state=closed&per_page=2` length 2 |
| reader blob `aef9509c...`, 626 lines, 34247 bytes, sha256 `a6936f86...` | `contents?ref=` raw, `git hash-object` equals API sha | made-up path 404 |
| `ci.yml` blob `0176b491...`, 679 lines, 43422 bytes, sha256 `1b4538e5...` (moved from the #217 squash by the one-line #218 comment edit) | same | same |
| reader not touched since #217 | `compare/4e63fc41...b069274c` file list (ci.yml, RequestTimingLogTests.cs, e2e-runner.test.ts, 3 others; no reader) and `commits?path=` for the reader (4e63fc41, 0a85b89e only) | the compare list names ci.yml, so the call returns real rows |
| base reader 31 OK, py 3.14.7 and /usr/bin/python3 3.9.6 | scratch two-folder layout, `python3 -I` | timeout 30 to 20 gives FAILED (failures=1), `diff` shows one line |
| survivors green on base: d01, a31, m01, job env key | plant script on scratch copies | same control as above |
| shard job: 7 job keys, 5 env keys, 12 steps (steps 4 and 5 have no name and no `uses`; step 6 is the only one with `env:`) | reader loaded as a module, `steps(shard_job())`, `step_keys` on each | `awk` count of `^      - ` over lines 165-351 agrees |
| workflow column-0 keys: name, on, permissions, concurrency, jobs (no `env:`, no `defaults:`) | python over `code(ci_text())` | the a31 plant adds one and the reader module sees it |
| CI predicate: `infra` job -> `validate.sh:21` -> `test_security_baseline.py` main() runs all 10 `infra/tests/test_*.py`, fails on ResourceWarning/open files | read `ci.yml:575-627`, `validate.sh`, `test_security_baseline.py:1557-1617` via `gh api` raw | file list from `contents/infra/tests` |
| rules on main: deletion, non_fast_forward, code_scanning, required_status_checks | `rules/branches/main` | n/a |
| ports 9750-9759 free | `lsof -nP -iTCP:9750-9759 -sTCP:LISTEN` rc 1 | bound 9751 for 4 s: listed 1, then 0 |
| kit scan | word-boundary scan of 98 non-`.pre-` SEAT kits of 10-25 and 10-26: 4 hits (B625, B649, B682, B686), all 10-25, none a live claim; 0 kits name H28/b708 | `x 9751 y` reads 1, `x 19751 y` reads 0 |
| live panes | `tmux list-panes`: tuesday, Datasec/NexusAI-M13, Datasec/Security-Composer-G133, fleet-monitor | n/a |
| models | `models_latest.json` line 23 `claude-sonnet-5-5`; model-routing rows C2 line 92, G2 line 109 | n/a |
| load | uptime 6.54 7.13 6.43 at 07:54 | n/a |

## D-decisions (Tuesday may change)
- D-1. Identity of a step: `name` (comment/space stripped), else `uses` path before `@` (so SHA/tag bumps stay green, the gate's 12 bumps), else the one-line `run:` value (steps 4, 5). `if:` is NOT in the identity (keeps the gate's shape; avoids extra legit-edit reds).
- D-2. Three new tests, not one: steps order, env/keys, duplicate keys. Expected count 34 against 31; a different count is a Correction.
- D-3. B677-3 is docstring-only (the ticket says so); no regex loosened. The trailing-comment table in the docstring is MEASURED by the builder with one-space and two-space plants, not copied from the gate.
- D-4. The residual limit (a body of an unpinned step writing `GITHUB_ENV`) is stated in the docstring, not pinned (pinning script bodies is a new closed-shape lane; the ticket permits "records why a line cannot be pinned").
- D-5. Env VALUES are not pinned (image digests move); only keys.
- D-6. Plants in scratch layouts only, never in a worktree; the gate's 161-edit battery is not rebuilt (its tools are read-forbidden); the builder replays the `uses:`-bump and comment rows from the readable table.
- D-7. Tier-2 gate after, per G2 line 109 (tests-only).

## Q-questions for Tuesday (each with a default)
- Q-1. Round count: the two gates on PR #217 were NO GO round 1 of 2 (B669) and NO GO round 2 of 2 (B677, ROUND CAP REACHED, landed on the product owner's ruling). Is the gate after this follow-up "round 1 of 2 on a new class" or "round 3 on the old one"? Default: round 1 of 2 on a new class ("closing the open lists of the shard-job reader"), with the cap history quoted at the gate commission; the kit says so and asks you to state it at stamp.
- Q-2. Pane names for the siblings: the kit names H29 (B710) and H30 (B709) as "or the next free name". Default: you assign at launch; the kit tolerates any.
- Q-3. Jira after landing (HPSMPOC-353 to Done once the PR lands; a note on HPSMPOC-351 if wanted): Tuesday's, not the seat's. Default: yours.

## UNMEASURED
The plants d02, d03, d05b, c02 on the base reader (gate-measured, RELAYED); the trailing-comment table; whether the identity rule leaves all 161 legitimate edits unchanged except an added step; whole-infra run and whether it needs the Bicep binary; the runner's Python; GitHub's acceptance of a duplicate mapping key and the env name; whether any non-test step of the shard job writes `GITHUB_ENV` (script bodies not read beyond first lines).

## Outside-the-fences disclosure
Writes: the kit, this report, and scratch files in my session scratchpad (`.../scratchpad/b708/`: copies of the two base files, plant layouts, a plant script). Reads: DRAFTER_RULES, the B687 template, the sweep (greps), the ticket via the project's Jira helper (HPSMPOC-353 only, one GET set; no token printed), the B677 STATUS lines 596-626 and 950-962 and the plant diffs file, `gh api -X GET` only under the project's `GH_CONFIG_DIR` (commits, pulls, compare, contents, rules, `commits?path=`), `gh auth status`, `git config core.sshCommand` and `ls-remote`/`ls -d` on the project clone (read verbs only; `cat-file` failed on the missing object, no fetch), `lsof`, `tmux list-panes`, `uptime`, one 4-second socket bind on 9751 as the port control. One miss: my first `ls` of kits wrote an empty redirect target (`> /tmp/x` hit an existing directory and errored; no file was written). One `gh api search/code` call printed 0 (not used). No decision_queue, no scoreboard, no ledger, no staged briefs, no non-Datasec tree, no HTTP to a hosted host.
