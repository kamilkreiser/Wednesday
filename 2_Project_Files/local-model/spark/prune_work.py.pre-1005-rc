#!/usr/bin/env python3
"""prune_work.py — remove the Spark runner's OWN per-round work clones once their round is recorded (2026-10-05).

Kam's 2026-09-29 rule: regenerable build leftovers are not kept once used; a tool removes only what it created.
A work dir (spark/cache/work/<run-id>/, holding clone/ + the checker's quarantine/) is regenerable from the cache at the
pinned tip; the RECORD is the run dir under local-model/runs/, which this never touches. Neither is the cache clone.

  prune_work.py <work_dir>                 remove that one work dir (queue.sh calls this after writing the done row)
  prune_work.py --older-than-hours H       catch-up: every work dir under the root older than H hours (queue.sh start)

A work dir is removed ONLY when ALL hold (each refusal is printed with its reason, and the dir survives):
  1. the path is non-empty, resolves (realpath) strictly UNDER the absolute work root + "/", and is not the root;
  2. it carries round.sh's marker `.spark_round_work` (written at creation: run_dir, pid, created);
  3. the marker names a run dir that has a VERDICT ROW in done.md (`| <run_dir> |`);
  4. the round is not live: the marker's pid is not alive, and spark/state/round.lock (if held by a live pid) does not
     name this work dir. A marker pid that is empty or <= 1 is malformed -> refused.
Env: SPARK_WORK_ROOT, SPARK_DONE, SPARK_STATE (same defaults as round.sh / queue.sh).
rc 0 (removals and refusals both printed) · 64 usage. Python 3 stdlib.
"""
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.realpath(__file__))
ROOT = os.environ.get("SPARK_WORK_ROOT") or os.path.join(HERE, "cache", "work")
DONE = os.environ.get("SPARK_DONE") or os.path.join(HERE, "done.md")
STATE = os.environ.get("SPARK_STATE") or os.path.join(HERE, "state")
MARKER = ".spark_round_work"


def alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def read_kv(p):
    d = {}
    for line in open(p, encoding="utf-8"):
        if "=" in line:
            k, v = line.rstrip("\n").split("=", 1)
            d[k] = v
    return d


def locked_work():
    """the work dir named by a round.lock held by a LIVE pid, else None."""
    lk = os.path.join(STATE, "round.lock")
    try:
        pid = int(open(os.path.join(lk, "pid")).read().strip())
        if pid > 1 and alive(pid):
            w = os.path.join(lk, "work")
            return os.path.realpath(open(w).read().strip()) if os.path.isfile(w) else "<live lock, work not yet named>"
    except (OSError, ValueError):
        pass
    return None


def prune(path):
    if not path or not path.strip():
        print("prune: REFUSED empty path"); return False
    if not ROOT or not os.path.isabs(ROOT):
        print(f"prune: REFUSED work root is not absolute: {ROOT!r}"); return False
    root = os.path.realpath(ROOT)
    real = os.path.realpath(path)
    if real == root or not real.startswith(root + os.sep):
        print(f"prune: REFUSED {path} — resolves to {real}, not strictly under {root}/"); return False
    if not os.path.isdir(real):
        print(f"prune: REFUSED {real} — not a directory"); return False
    mk = os.path.join(real, MARKER)
    if not os.path.isfile(mk):
        print(f"prune: REFUSED {real} — no {MARKER} marker (not created by round.sh)"); return False
    m = read_kv(mk)
    run, pid_s = m.get("run_dir", "").strip(), m.get("pid", "").strip()
    if not run:
        print(f"prune: REFUSED {real} — marker names no run_dir"); return False
    try:
        pid = int(pid_s)
    except ValueError:
        pid = 0
    if pid <= 1:
        print(f"prune: REFUSED {real} — marker pid {pid_s!r} is empty or <= 1 (malformed)"); return False
    if alive(pid):
        print(f"prune: KEPT {real} — its round (pid {pid}) is still running"); return False
    lw = locked_work()
    if lw is not None and (lw == real or lw.startswith("<")):
        print(f"prune: KEPT {real} — round.lock is held by a live round ({lw})"); return False
    try:
        rows = open(DONE, encoding="utf-8").read()
    except OSError:
        rows = ""
    if f"| {run} |" not in rows:
        print(f"prune: KEPT {real} — no verdict row for {run} in {DONE}"); return False
    size = subprocess.run(["du", "-sh", real], capture_output=True, text=True).stdout.split("\t")[0].strip() or "?"
    shutil.rmtree(real)
    print(f"prune: REMOVED {real} ({size}) — round recorded in done.md; run dir {run} kept")
    return True


def main():
    a = sys.argv[1:]
    if len(a) == 2 and a[0] == "--older-than-hours":
        hours = float(a[1]); cutoff = time.time() - hours * 3600
        root = os.path.realpath(ROOT)
        if not os.path.isdir(root):
            print(f"prune: no work root at {root}"); return 0
        n = 0
        for name in sorted(os.listdir(root)):
            p = os.path.join(root, name)
            if os.path.isdir(p) and os.path.getmtime(p) < cutoff:
                n += prune(p)
        print(f"prune: catch-up (> {hours:g} h) removed {n}")
        return 0
    if len(a) == 1:
        prune(a[0]); return 0
    print("usage: prune_work.py <work_dir> | --older-than-hours H", file=sys.stderr)
    return 64


if __name__ == "__main__":
    sys.exit(main())
