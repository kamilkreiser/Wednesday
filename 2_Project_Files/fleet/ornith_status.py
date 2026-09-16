#!/usr/bin/env python3
"""ornith_status.py — one or two lines about the local model's queue, printed on every send.

WHY (ledger 2026-09-17, w=5 of the idle-on-a-verdict-turn costume): five times in one day a
coordinator seat worked verdicts, GOs and receipts while the local model had finished its
queue and sat idle — twice with a PASS nobody had held. The rule "read the queue at every
verdict-class turn" was a habit, and it failed every time the seat was busy. Every such turn
already sends a mail through send_brief.sh, so the read rides that action instead.

Prints to stdout (send_brief.sh sends it to stderr, so callers parsing stdout are untouched):
  ORNITH: queue N · runner LIVE pid P | not running · newest <ID> <verdict> done HH:MM
  ORNITH: ⚠ UNHELD PASS <ID> (done HH:MM, no READY_<ID>* written since) — source-read and hold it NOW
  ORNITH: ⚠ IDLE <N> min (queue empty, runner not running since HH:MM) — brief the next ticket NOW

Never fails the caller: any error prints 'ORNITH: status unreadable — <reason>' and exits 0,
because a status line must not be able to block a send. An unreadable status is itself printed,
never silent (a refusal nobody reads is indistinguishable from working).

Test seams: ORNITH_NIGHT_DIR (the night/ dir) and ORNITH_NOW ('YYYY-MM-DD HH:MM').
"""
import os
import re
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
NIGHT = os.environ.get("ORNITH_NIGHT_DIR") or os.path.join(HERE, "..", "local-model", "night")
IDLE_WARN_MIN = 10  # one brief-writing interval (2026-09-16 if-something-blocks rule 4)


def now():
    s = os.environ.get("ORNITH_NOW")
    return datetime.strptime(s, "%Y-%m-%d %H:%M") if s else datetime.now()


def main():
    qpath = os.path.join(NIGHT, "queue.md")
    dpath = os.path.join(NIGHT, "done.md")
    if not os.path.isfile(qpath) or not os.path.isfile(dpath):
        print(f"ORNITH: status unreadable — queue.md or done.md missing under {NIGHT}")
        return
    depth = 0
    with open(qpath) as f:
        for line in f:
            if line.lstrip().startswith("#"):
                continue
            if "input=" in line:
                depth += 1

    pid = ""
    live = False
    pidfile = os.path.join(NIGHT, "log", ".night_run.lock", "pid")
    if os.path.isfile(pidfile):
        pid = open(pidfile).read().strip()
        if pid.isdigit() and pid != "1":
            try:
                os.kill(int(pid), 0)
                live = True
            except OSError:
                live = False

    newest = None
    pat = re.compile(r"^(\S+) .*\| done (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) \| verdict (.*?) \| run ")
    with open(dpath) as f:
        for line in f:
            m = pat.match(line)
            if m:
                newest = (m.group(1), datetime.strptime(m.group(2), "%Y-%m-%d %H:%M"), m.group(3).strip())
    if newest is None:
        print(f"ORNITH: status unreadable — no parseable '| done … | verdict … | run' line in {dpath}")
        return
    tid, done_at, verdict = newest
    runner = f"runner LIVE pid {pid}" if live else "runner not running"
    print(f"ORNITH: queue {depth} · {runner} · newest {tid} {verdict} done {done_at:%H:%M}")

    if "PASS" in verdict:
        held = False
        for name in os.listdir(NIGHT):
            if not name.startswith("READY_"):
                continue
            rest = name[len("READY_"):]
            if not (rest.startswith(tid + "_") or rest.startswith(tid + "-")):
                continue
            mt = datetime.fromtimestamp(os.path.getmtime(os.path.join(NIGHT, name)))
            if mt >= done_at:
                held = True
                break
        if not held:
            print(f"ORNITH: ⚠ UNHELD PASS {tid} (done {done_at:%H:%M}, no READY_{tid}* written since) — source-read and hold it NOW")

    if depth == 0 and not live:
        idle = int((now() - done_at).total_seconds() // 60)
        if idle >= IDLE_WARN_MIN:
            print(f"ORNITH: ⚠ IDLE {idle} min (queue empty, runner not running since {done_at:%H:%M}) — brief the next ticket NOW")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # a status line must never block a send — but it must never be silent either
        print(f"ORNITH: status unreadable — {type(e).__name__}: {e}")
    sys.exit(0)
