STARTABLE: YES

# B1570 DRAFTER REPORT (kit `2026-11-15_B1570_SEAT-M137_mps-lane-mo-followups-400-403.md`, drafted 11:43 to 11:50 AEDT, `date` printed 11:43:08 and 11:48:46)

## BLUF
One Sonnet kit, seat `Datasec/MPS-M137`, branch `b1570/mps-lane-mo-followups-400-403`, three commits, no PR, nothing deployed. **Built: MPSCALC-400 (the order only), MPSCALC-401, MPSCALC-403. LEFT: MPSCALC-402** (every item changes a stop word; its own text says the words are pending the product owner's approval and its acceptance needs that approval; 0 comments on it, so no comment id carries a ruling; the pending approval is hand-off item 1 of the records seat's STATUS `B1562_STATUS.md:53`). **LEFT inside 400:** "decide separately whether one token may serve the whole count" (the ticket makes no decision; the kit only counts token calls and states them).

## Slice keys
400 (swap `deploy-from-ci.sh:237` and `:238`; rows by program-read order and runtime order; token-call table, count unchanged) | 401 (shallow checkout becomes undecided, reusing the existing undecided line, no new word) | 403 (`deploy-package.py:50`, `:671`, `:672` end `\Z`).

## Facts re-measured (instrument, 11:43 to 11:48 AEDT)
- Main `ccc413677810b8b06e88e74e7cf3d3f8c2729592` (`gh api -X GET .../git/ref/heads/main`); open PRs 0; `matching-refs/heads/b1570` length 0.
- Tickets: own GET-only helper (`fleet/state/s277/d1570/jget.py`, credentials read in-process by name, never printed), `project = MPSCALC AND ( key = MPSCALC-400 )` and the other three; all Backlog, label `records-pass-1115`, 0 comments each (control: the helper's comment loop prints `--- comment` lines for a ticket with comments; not run on a control ticket in this pass, so "0 comments" rests on the endpoint answering an empty list: UNMEASURED control).
- Seat id: highest earlier `SEAT-M<n>` in the briefs folder by program printed M136; so M137. Live panes: `Datasec/MPS-M135`, `Datasec/MPS-M136` (no M137). Ports 9870-9879: `lsof` 0 listeners (control: unfiltered list 32), word-boundary scan of today's and yesterday's non-`.pre-` SEAT kits 0 files.
- Model: `model-routing.md:92` row C2 (Sonnet 1st), C3 `:93` not applicable (spelled-out edit), C6 `:96` not applicable (nothing deploys), gate tier G1 `:108`. Model id `claude-sonnet-5-5` at `models_latest.json:23`. Nothing left out of a Sonnet kit for routing reasons; `brief_seat.sh:31` defaults to Opus, so `BRIEF_SEAT_LEVEL=sonnet` is inside the quotes.
- **Premise of 401 run by program** (synthetic scratch repo F-G-H, depth-1 clone, then fetch F at depth 1; git 2.54.0): shallow clone prints `true` for `rev-parse --is-shallow-repository` and `merge-base --is-ancestor F HEAD` answers rc 1; full repo control prints `false` and rc 0; reverse rc 1. So the ticket's claim holds.
- **THE FINDING THAT SHAPES THE KIT:** hosted CI `python` job checks out with default depth (`ci.yml:89-91`, no `fetch-depth`), so `ROOT` is shallow on the runner. `test_deploy_rollforward.py`'s `git_shim` (`:220`) answers only `is-ancestor` and passes every other git call to the real git. If the script asks `rev-parse --is-shallow-repository` and the shim does not answer it, rows `:306`, `:318`, `:325` would turn red on hosted CI and stay green in a seat's full clone. The kit makes the shim answer it (default `false`), and its CHECKS run the whole loop in a depth-1 copy plus a control (base test file against head script in that copy must read those rows red).
- Design choices (D): D1 the shallow question is asked only AFTER an `is-ancestor` answer of 1 (a 0 is certain even on a shallow checkout; count 0 never asks), minimising the rows touched. D2 any answer other than exactly `false` is undecided (safe side). D3 the shallow case sets the answer to 128, routing into the existing undecided arm: no new word, but that line prints `git answered 128` while git answered 1.
- CI jobs whose tests read the changed files: `python` (`ci.yml:84`; pass predicate every `tools/demo/test/test_*.py`, `infra/tests/test_*.py`, `scripts/tests/test_*.py` rc 0 under `python3 -I`, shallow checkout, runner's real `az` on PATH) and `package` (`:109`, `needs: [dotnet, web, python]`; runs `scripts/package.sh`, which calls `deploy-package.py make --commit "$(git rev-parse HEAD)"`, no newline, so 403 keeps it). `dotnet` and `web` read none: GitHub code search for `deploy-package`, `deploy-from-ci`, `test_deploy_rollforward` listed only `scripts/**`, `infra/README.md`, `.github/workflows/ci.yml`; index completeness UNMEASURED, the kit makes the seat re-prove it with a repo grep. Known environmental reds on this machine (RELAYED): `test_run_demo.py`, `test_infra.py`.
- CodeQL: CLI v2.27.4 present (binary and `python` folder listed). The kit's pre-scan runs the python pack over the seat's clone under a heavy lock with planted controls (`eval`, and a sensitive-NAME constant written to a file), plus all hand rows including the sensitive-NAME row; if it cannot run it says NOT RUN. I did not run CodeQL myself (the kit's code does not exist yet).

## By-program census of existing tests pinning behaviour the slice changes (frame: the 5 test files that read the two scripts, `grep -c -i -E` over main `ccc41367` copies)
| Behaviour | `test_deploy_rollforward` | `test_scripts` | `test_deploy_pre1` | `test_deploy_pre1_forms` | `test_ci_workflow` |
|---|---|---|---|---|---|
| `git_shim(` uses | 13 | 0 | 0 | 0 | 0 |
| `older than the first build` | 1 | 0 | 0 | 0 | 0 |
| `cannot say whether` | 2 | 0 | 0 | 0 | 0 |
| `is-shallow` (control: absent at main by design) | 0 | 0 | 0 | 0 | 0 |
| `--commit` / `--expect-commit` | 0 | 2 each | 0 | 0 | 0 |
Order: no row reads the order of the three calls (grep for `reread`, `just before`, `roll-forward rule` found only message and read-count rows; `test_deploy_pre1.py:214`, `:655` count overlay reads as 2 and stay equal after the swap because the roll-forward reads no overlay: DERIVED, the kit's row (c) proves it). Pins likely affected: rows `:306`, `:318`, `:325` (older wording, shim 1) only by the shallow hazard, closed by the shim default. `test_scripts.py:464` xtrace row with one care-pack row uses the real git and a synthetic sha (git answers 128, not 1), so it never reaches the shallow question (DERIVED).

## Chain-input table (rule 4)
| Step | Inputs | Produced by |
|---|---|---|
| 0 | kit, REFUSE counts | exist at BASE |
| 1 | clone, main-tree, baseline loops | Step 0; origin main |
| 2 (400) | rows, script lines `:237-238`, fakes | BASE files; Step 1 clone |
| 3 (401) | scratch synthetic repo (premise), shim edit, rows, script `:225-226` | scratch repo made in Step 3 itself; shim edit before rows; BASE script |
| 4 (403) | patterns `:50`, `:671-672`, existing `make` helper `test_scripts.py:49` | BASE |
| 5 | depth-1 copy of the clone at head | commits of Steps 2-4 |
| 6 | CodeQL database of the clone | commits of Steps 2-4, heavy lock |
| 8 | 3 commits | Steps 2-4 |
No step needs a file a later step makes.

## Questions for Tuesday (each with a default)
- Q-1 Build 400, 401, 403 only, 402 and the single-token decision left. Default: yes.
- Q-2 401 reuses the existing undecided line, so it prints `git answered 128` although git answered 1. Default: accept, and fold a truthful wording into 402's pending word pack. Alternative (a new line) needs the product owner's word.
- Q-3 On a shallow checkout an `is-ancestor` answer of 0 goes on (the ticket's recommendation says treat shallow as undecided outright). Default: only the 1 is distrusted; the acceptance check is met either way.
- Q-4 Gate tier G1 (edits the deploy stop logic). Default G1.
- Q-5 One commit per ticket, 3 commits. Default yes.

## UNMEASURED
Whether the roll-forward and re-read ordering changes hosted behaviour (no host run, by design); the runner's own Python and bash; "0 comments" control (above); GitHub code-search completeness; the other `$`-ended patterns of `deploy-package.py` (`:58`, `:153`, `:165`, `:329`) are listed for the seat to report, not judged. Sidecar: 110 claims; a part of them are seat-side instruction fragments or prose that stamp_check picked up, recorded as such (grep counts over the kit and sources), not as tool outputs; the premise run and spot prints are appended as `#` lines. Tuesday should spot-measure at least five lines.

## Outside-the-fences disclosure
Wrote only the kit, its `.measured` sidecar, this report and scratch under `fleet/state/s277/d1570/` (helper, saved GET copies of main files, a synthetic scratch git repo with its own throwaway identity, `GIT_CONFIG_GLOBAL=/dev/null`, under TUESDAY's own scratch). Read: the template kits, rules, the records STATUS, the sweep headings, the model-routing and gate-standard rows, `brief_seat.sh` and `stamp_check.py` headers. `gh api -X GET` only (including one code-search GET). No Jira write, no project-repo git verb, no az, ssh, docker, tmux send-keys, hosted HTTP, no message; read no other client's tree, no WEDNESDAY or FRIDAY tree, no ledger, no `decision_queue.sh`. A first attempt at the scratch repo was refused by the cd/git-write hook (variable-path write verb); redone with literal paths inside TUESDAY.

DRAFTED B1570: kit 81 lines, sidecar rc 0, questions 5
