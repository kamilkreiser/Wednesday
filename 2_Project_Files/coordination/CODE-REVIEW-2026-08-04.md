# Code review — coordination harness (yesterday's agentic work)

**Date:** 2026-08-04 · **Commissioned by Kam** · Scope: `2_Project_Files/coordination/`
(harness.py, seats.py, verifiers.py, runners, tests — built 2026-08-03 during the
TreeQuest study, commit 0642e0d). Format: risk tiers per the freshly-adopted
review standard (orchestrator-adws review, adoption #5) — structured verdict line.

## Quick reference

| # | Finding | Tier | Fix |
|---|---|---|---|
| 1 | Infinite-loop solution crashes the whole run (verifier timeout uncaught) | HIGH | try/except around verify, score 0 |
| 2 | Seats run with cwd=drive root — model context/read reach includes the whole drive incl. `4_Credentials/` | HIGH | neutral scratch cwd |
| 3 | Untrusted generated code executes unsandboxed with full user privileges | HIGH (accepted-risk for now) | document; sandbox before real-problem use |
| 4 | `__pycache__/*.pyc` + checkpoint `*.pkl` + run artifacts committed to git | MEDIUM | gitignore + rm --cached (ledger w=2 — same root cause as yesterday's Codex-binary slip) |
| 5 | Refining from a seat-error node (code="", score 0) wastes budget | LOW | acceptable — bandit routes around it |
| 6 | `run_search` on empty tree with budget=0 → `top_k` on nothing raises | LOW | not a real calling pattern |
| 7 | Progress line says "latest by" but prints the BEST node's seat | LOW | relabel |
| 8 | 3 near-duplicate day3 runners | LOW | teaching artifacts; fold into one parametrised runner if reused |

## Detail on the three HIGHs

**1. Uncaught verifier timeout (the real bug).** In `make_generate_fn`
(harness.py:70-81) the `try` covers only `seat(prompt)`. `test_suite_verifier`
runs OUTSIDE it, and `subprocess.run(..., timeout=120)` raises `TimeoutExpired`
when the candidate loops forever — which weak seats genuinely produce. One bad
candidate kills the entire search (checkpoint makes it resumable, but the run
dies mid-flight, which in an overnight/pilot context means silent loss).
*Fix applied: wrap verification; timeout → Verdict(0, "verifier timeout").*

**2. Seat working directory = drive root.** Both CLIs run with
`cwd=DRIVE_ROOT`: `claude -p` inherits WEDNESDAY's project context (CLAUDE.md,
settings) into what should be a bare code-generator, and both tools get
file-read reach over the whole drive — including `4_Credentials/` — for a task
that needs zero filesystem context. Wasteful and an unnecessary secrets
surface. *Fix applied: seats run from `seat_scratch/` (empty, gitignored).*

**3. Unsandboxed execution of generated code.** The verifier executes
model-written code with full user privileges, network, and filesystem. Fine for
self-authored kata in a supervised run; NOT fine once the harness is pointed at
real stuck problems with bigger budgets (WED-23 break-glass posture). The arc2
reference sandboxes this. *Not fixed today — accepted risk recorded here;
sandboxing is a precondition for the first break-glass use.*

## What's genuinely good (keep)

Seat-failure→score-0 so the bandit routes around broken seats · checkpoint
every step + resume from `done` count · unmodifiable test file copied into a
temp dir · failure text fed into refinement prompts · `extract_python` takes
the LAST fenced block · per-seat call counting surfaced in the summary ·
priors hook ready for the scoreboard.

## Verification of fixes

Post-fix smoke run: see `smoke/out/summary.json` (re-run 2026-08-04) — harness
end-to-end green after changes.

VERDICT: PASS (after fixes 1, 2, 4 applied; finding 3 recorded as accepted risk
with a named precondition)
