"""Wednesday's coordination harness — Multi-LLM AB-MCTS over model seats.

Modelled on SakanaAI/ab-mcts-arc2 (study notes:
1_Project_Definition/Architecture/2026-08-03_treequest-study-notes.md).
The search decides wider-vs-deeper AND which seat generates, from evidence.

Usage: build a Task (spec + test file), call run_search(). Budget-capped,
checkpointed each step, resumable from a checkpoint pickle.
"""

from __future__ import annotations

import json
import pickle
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import treequest as tq

from seats import CALL_COUNTS, SEATS
from verifiers import Verdict, extract_python, test_suite_verifier


@dataclass
class Task:
    name: str
    spec: str            # what to build, in plain language
    test_file: Path      # the unmodifiable verifier


@dataclass
class Attempt:
    code: str
    seat: str
    verdict: Verdict


def initial_prompt(task: Task) -> str:
    return f"""Write a Python module solving the task below.
Reply with ONE ```python fenced code block containing the complete module
(it will be saved as solution.py and run against a fixed unittest suite).
No commentary outside the block.

# Task
{task.spec}
"""


def refine_prompt(task: Task, parent: Attempt) -> str:
    return f"""A previous attempt at the task below passed {parent.verdict.passed}/{parent.verdict.total} tests.
Improve it. Reply with ONE ```python fenced code block containing the complete
fixed module. No commentary outside the block.

# Task
{task.spec}

# Previous attempt
```python
{parent.code}
```

# Test output (what failed and why)
{parent.verdict.report}
"""


def make_generate_fn(seat_name: str, seat: Callable[[str], str], task: Task):
    def generate(parent: Attempt | None) -> tuple[Attempt, float]:
        prompt = initial_prompt(task) if parent is None else refine_prompt(task, parent)
        try:
            raw = seat(prompt)
        except Exception as e:  # seat failure scores 0 — the bandit learns to route around it
            print(f"  seat '{seat_name}' errored: {e}")
            verdict = Verdict(score=0.0, passed=0, total=0, report=f"seat error: {e}")
            return Attempt(code="", seat=seat_name, verdict=verdict), 0.0
        code = extract_python(raw)
        try:
            verdict = test_suite_verifier(code, task.test_file)
        except subprocess.TimeoutExpired:
            # a candidate that loops forever must cost the SEAT, not the run
            print(f"  verifier timeout on candidate from '{seat_name}' — scored 0")
            verdict = Verdict(score=0.0, passed=0, total=0,
                              report="verifier timeout: candidate exceeded the test time limit "
                                     "(likely an infinite loop or pathological complexity)")
        return Attempt(code=code, seat=seat_name, verdict=verdict), verdict.score
    return generate


def run_search(
    task: Task,
    seat_names: list[str],
    budget: int,
    out_dir: Path,
    checkpoint: Path | None = None,
    priors: dict[str, float] | None = None,
) -> Attempt:
    """Run AB-MCTS-A over the given seats until budget nodes exist.

    priors: optional per-seat reward averages (the track record, seeded in).
    Returns the best attempt; writes checkpoints + a run summary to out_dir.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    algo = tq.ABMCTSA(dist_type="beta", reward_average_priors=priors)
    if checkpoint and checkpoint.exists():
        tree = pickle.loads(checkpoint.read_bytes())
    else:
        tree = algo.init_tree()

    generate_fns = {
        name: make_generate_fn(name, SEATS[name], task) for name in seat_names
    }

    t0 = time.time()
    done = len(algo.get_state_score_pairs(tree))
    for i in range(done, budget):
        tree = algo.step(tree, generate_fns)
        (out_dir / "checkpoint_latest.pkl").write_bytes(pickle.dumps(tree))
        best_state, best_score = tq.top_k(tree, algo, k=1)[0]
        print(f"[{i + 1}/{budget}] best={best_score:.2f} "
              f"(latest by {best_state.seat}) calls={dict(CALL_COUNTS)}")
        if best_score >= 1.0:
            print("Perfect score — stopping early.")
            break

    best_state, best_score = tq.top_k(tree, algo, k=1)[0]
    summary = {
        "task": task.name,
        "budget": budget,
        "nodes": len(algo.get_state_score_pairs(tree)),
        "best_score": best_score,
        "best_seat": best_state.seat,
        "calls_by_seat": dict(CALL_COUNTS),
        "wall_seconds": round(time.time() - t0, 1),
        "scores_by_seat": {
            name: [round(s, 3) for st, s in algo.get_state_score_pairs(tree)
                   if st.seat == name]
            for name in seat_names
        },
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    return best_state
