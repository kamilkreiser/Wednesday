---
date: 2026-08-04
type: correction
source: "Self-caught at w=2: 08-03 Codex binary rejected the push; 08-04 code review found __pycache__/*.pyc + checkpoint *.pkl + run artifacts committed in 0642e0d"
status: live
supersedes: ""
---

# Gitignore artifacts AT CREATION, not at wrap — and retro candidates need files

**The lesson (two layers):**

1. **The mistake itself:** any time a tool, script, or run CREATES a new class
   of on-disk artifact (binaries, caches, checkpoints, output dirs, venvs,
   scratch dirs), the `.gitignore` entry is written in the SAME action as the
   creation — never deferred to wrap-up. Yesterday the Codex install swept a
   258MB binary into a commit (caught only by GitHub's push rejection); the
   same commit quietly carried `__pycache__/`, `*.pkl` checkpoints, and run
   output dirs that nothing rejected — today's code review caught them.
   What the push-size check doesn't catch, nothing catches automatically.

2. **The meta-failure (why w=2 instead of a fired lesson):** yesterday's slip
   was noted in the daily retro as "retro-worthy" but never became a lesson
   file or ledger row — and un-filed candidates don't fire at the next boot.
   A retro line is episodic memory; only a `learnings/` file is semantic.
   **If a retro candidate would change behaviour, file it the same session.**

**How to apply:**
1. New tool install / new run-output dir / new cache → `.gitignore` line in the
   same breath, then `git status` to confirm the tree stays clean.
2. At wrap, `git status --short` review is a BACKSTOP, not the mechanism.
3. Retro candidates that pass the importance filter get a lesson file
   immediately — "candidate" is a queue, not a destination.

**Related:** [[_ledger]], [[2026-08-03_frequency-weighted-reinforcement]],
[[2026-08-03_workflow-systemisation-duty]]
