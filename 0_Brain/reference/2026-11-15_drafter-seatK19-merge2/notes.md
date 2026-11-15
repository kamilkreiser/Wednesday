# Notes: drafter for Seat K 19th (second parallel merge seat), 2026-11-15 15:2x to 15:40 AEDT

Output brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-15_seatK19_merge2.md (about 58 KB). Scratch: `_work/` here (clone `_work/clone`, no push URL; nothing written outside this folder and the brief; nothing in !CODING touched).

## Method (instruments)
- Candidate list: p_verdicts_wed.json (63 entries) minus the commission's exclusions = 60. `_work/cand.json`.
- Per PR: `gh api pulls/N` and `/files` (project GH_CONFIG_DIR) -> `_work/gh.json` (head, state, mergeable_state, files, +/-, body do-not-merge count, gh==git file equality). Heads re-read for all 52 at 15:34:43: none moved.
- Verdict at head: `_work/build.py` parses `PR N: <verdict>` / table row with head12 / `## PR N ...` heading in the gate's verdict.md, then `_work/rows.json`; all 60 = GO WITH NOTES (Wednesday's 5 plain GO were the regex taking a neighbour's verdict).
- Holds and findings: keyword and severity scans over each gate file (before merge / merge after / hold / do not merge / MEDIUM / MAJOR / BLOCKER / Wednesday's call / for Kam), every hit on a queued row read; Secuura decision cards matched by KS-N / ksN / PR N / #N / pull/N across 559 cards (`_work/cards.json`), the relevant ruled options read.
- Linear: `_work/linear.py` (key in-process from the project .env, no 'Bearer'), comments(first:100) sorted client-side -> `_work/linear.json`.
- Merge trees: `_work/mt.sh` (both orders, rc from the command alone) -> `mt.out` 62/62 rc 0/0; planted controls `plants.sh` -> `plants.out`; stacked pairs `stack.sh` -> `stack.out`.
- Overlap and B-seat paths: python over gh.json and `bpaths.json` (B 176th's 10 PRs by gh api).
- Re-key: `_work/rekeysim.py` (scratch copy of REC175/tools -> `_work/kit_sim/tools`, plus 13 evidence scripts), `_work/matcherK/derive.py` and `k19_match.py` (scratch), cross-seat table by python importlib over the K scratch matcher, b175_match.py and b176_match.py (read-only).

## Findings worth the coordinator's eye
1. Naive re-key (G1..G7 only) leaves the MINE regex in the `seat\s+B\s+175th` form untouched; after the bare 175th -> 19th it would read `seat\s+B\s+19th` and classify an OLD B seat ("B 19th", in OTHER_SEATS) as MINE: self-test 714/719. Bare `175th` rule also corrupts `B 1175th`. Both are in the brief as FORBIDDEN with the measured numbers.
2. The matcher separates seats by NAME only; B and K share one mailbox (inbox_routing.conf lines 36 and 216).
3. Wednesday's list had two wrong gates (2052 -> gate 343 is PR 2219's; 2075 -> gate 320 only mentions it) and 5 mislabelled GOs.
4. 22 of the 52 rows carry the 'Do not merge' sentence that card ...nine-prs-1113 (c) addressed for nine PRs: Q1.
5. PR 2159 carries gate 301's MEDIUM with an explicit 'should not merge as written': dropped.
6. Ticket keys for 2052 and 2087 in the list differ from the PR titles (KS-1081, KS-1600).

## UNMEASURED
- Any suite, install, tsc, eslint, fragments, audit; the re-keyed kit beyond `ast.parse`/`bash -n` and the matcher self-test; mailwatch against the live inbox; per-row derive scripts.
- Why 2075, 2052, 2073, 2131, 2135, 2136 sit on the B-lineage not-in-queue list (reason not in any brief read).
- Whether a card holds a row but matched none of the keyword forms; whether a gate finding phrased outside the scanned keywords holds a row.
- Box text of the 22 DNM bodies beyond the count; the team's Linear automation; tmux floor; push queue and lock-holder today; whether any build seat pushed since 15:3x; whether a K launcher/pane config exists beyond the routing line.
- The 15:07:32 and 15:08:26 Kam quotes are the commission's text, not re-read from the terminal.
