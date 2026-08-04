"""Model seats for the coordination harness.

A "seat" is a callable (prompt: str) -> str. Each wraps a CLI/API channel.
Seats are subscription-backed where possible (zero marginal cost); every call
is counted so the harness can report usage per seat.

Machine-local dependency: the `claude` CLI itself (see PORTABILITY.md).
The codex CLI + its auth live on-drive.
"""

from __future__ import annotations

import os
import subprocess
from collections import Counter
from pathlib import Path

DRIVE_ROOT = Path(__file__).resolve().parents[2]
CODEX_BIN = DRIVE_ROOT / "2_Project_Files/tools/codex-cli/node_modules/.bin/codex"
CODEX_HOME = DRIVE_ROOT / "4_Credentials/.codex"

# Seats are bare code generators: run them from an EMPTY scratch dir so neither
# CLI inherits Wednesday's project context or gets file-read reach over the
# drive (code-review finding #2, 2026-08-04). Gitignored.
SEAT_CWD = Path(__file__).resolve().parent / "seat_scratch"
SEAT_CWD.mkdir(exist_ok=True)

CALL_COUNTS: Counter[str] = Counter()

TIMEOUT_S = 600


def gpt_seat(prompt: str) -> str:
    """GPT via OpenAI Codex CLI (ChatGPT-subscription auth, exec mode, read-only)."""
    CALL_COUNTS["gpt"] += 1
    env = dict(os.environ, CODEX_HOME=str(CODEX_HOME))
    out = subprocess.run(
        [str(CODEX_BIN), "exec", "--skip-git-repo-check", "-s", "read-only", prompt],
        capture_output=True, text=True, timeout=TIMEOUT_S, env=env,
        cwd=str(SEAT_CWD),
    )
    if out.returncode != 0:
        raise RuntimeError(f"codex exec failed: {out.stderr[-500:]}")
    return out.stdout


def claude_seat(prompt: str) -> str:
    """Claude via the claude CLI in print mode (Max-subscription auth)."""
    CALL_COUNTS["claude"] += 1
    out = subprocess.run(
        ["claude", "-p", prompt, "--model", "claude-sonnet-5"],
        capture_output=True, text=True, timeout=TIMEOUT_S,
        cwd=str(SEAT_CWD),
    )
    if out.returncode != 0:
        raise RuntimeError(f"claude -p failed: {out.stderr[-500:]}")
    return out.stdout


def gpt_low_seat(prompt: str) -> str:
    """GPT with minimal reasoning effort — a deliberately weak seat."""
    CALL_COUNTS["gpt-low"] += 1
    env = dict(os.environ, CODEX_HOME=str(CODEX_HOME))
    out = subprocess.run(
        [str(CODEX_BIN), "exec", "--skip-git-repo-check", "-s", "read-only",
         "-c", 'model_reasoning_effort="none"', prompt],
        capture_output=True, text=True, timeout=TIMEOUT_S, env=env,
        cwd=str(SEAT_CWD),
    )
    if out.returncode != 0:
        raise RuntimeError(f"codex exec failed: {out.stderr[-500:]}")
    return out.stdout


def haiku_seat(prompt: str) -> str:
    """Claude Haiku — the cheap, weak Claude seat."""
    CALL_COUNTS["haiku"] += 1
    out = subprocess.run(
        ["claude", "-p", prompt, "--model", "claude-haiku-4-5-20251001"],
        capture_output=True, text=True, timeout=TIMEOUT_S,
        cwd=str(SEAT_CWD),
    )
    if out.returncode != 0:
        raise RuntimeError(f"claude -p failed: {out.stderr[-500:]}")
    return out.stdout


SEATS = {
    "gpt": gpt_seat,
    "claude": claude_seat,
    "gpt-low": gpt_low_seat,
    "haiku": haiku_seat,
}
