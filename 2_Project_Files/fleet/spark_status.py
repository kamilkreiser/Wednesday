#!/usr/bin/env python3
"""spark_status.py — the Spark ALLOCATION check: is the local model working right now, and if not, say so loudly.

WHY (Kam, 2026-10-28 ~12:1x AEDT, terminal): "keep the rule and maybe introduce an allocation check for local LLM
into your wakeup procedure". The rule is learnings/2026-10-28_never-keep-the-spark-idle-quota-and-capability-data.md.
On 2026-10-28 the Spark sat idle all morning: its tunnel was DOWN and nothing at any boot or checkpoint asked whether
it was working. A rule I must remember to check is not a check (2026-08-09 lesson), so this rides the actions that
already happen: the boot doctor (doctor.sh) and every send through send_brief.sh, beside ornith_status.py.

Prints one or two lines to stdout:
  SPARK: tunnel UP|DOWN · queue N · drainer LIVE pid P | not running · round LIVE pid P | none · last <tag> <verdict> <when>
  SPARK: ⚠ IDLE — <why> — allocate a task NOW (rule 2026-10-28: never keep the Spark idle)
IDLE = no round running AND (queue empty OR no drainer). A DOWN tunnel is reported as its own reason.

Never fails the caller: any error prints 'SPARK: status unreadable — <reason>' and exits 0 (a status line must not
block a send or a boot; an unreadable status is printed, never silent).

Test seams: SPARK_DIR (the local-model/spark dir), SPARK_NOW ('YYYY-MM-DD HH:MM'), SPARK_SKIP_NET=1 (tunnel reads
'UNCHECKED' with no network call), SPARK_URL (default http://127.0.0.1:47788).
"""
import json
import os
import sys
import urllib.request
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SPARK_DIR = os.environ.get("SPARK_DIR") or os.path.normpath(os.path.join(HERE, "..", "local-model", "spark"))
SPARK_URL = os.environ.get("SPARK_URL", "http://127.0.0.1:47788")


def now():
    v = os.environ.get("SPARK_NOW")
    return datetime.strptime(v, "%Y-%m-%d %H:%M") if v else datetime.now()


def live_pid(lock_dir):
    """A lock is a dir holding a 'pid' file. Returns the pid if that process is alive, else None."""
    pf = os.path.join(lock_dir, "pid")
    if not os.path.isfile(pf):
        return None
    try:
        pid = int(open(pf).read().strip())
        os.kill(pid, 0)
        return pid
    except (ValueError, ProcessLookupError, PermissionError, OSError):
        return None


def tunnel():
    if os.environ.get("SPARK_SKIP_NET") == "1":
        return "UNCHECKED"
    try:
        with urllib.request.urlopen(SPARK_URL + "/v1/models", timeout=3) as r:
            return "UP" if r.status == 200 else "DOWN (HTTP %s)" % r.status
    except Exception as e:  # noqa: BLE001 — any failure is DOWN, with its reason
        return "DOWN (%s)" % type(e).__name__


def main():
    state = os.path.join(SPARK_DIR, "state")
    qfile = os.path.join(SPARK_DIR, "queue.md")
    queued = 0
    if os.path.isfile(qfile):
        for line in open(qfile):
            s = line.strip()
            if s and not s.startswith("#"):
                queued += 1
    drainer = live_pid(os.path.join(state, "queue.lock"))
    rnd = live_pid(os.path.join(state, "round.lock"))
    last = "none"
    last_dt = None
    lr = os.path.join(state, "last_round.json")
    if os.path.isfile(lr):
        d = json.load(open(lr))
        last_dt = datetime.fromtimestamp(os.path.getmtime(lr))
        last = "%s %s %s" % (d.get("tag", "?"), d.get("verdict", "?"), last_dt.strftime("%m-%d %H:%M"))
    tun = tunnel()
    print("SPARK: tunnel %s · queue %d · drainer %s · round %s · last %s" % (
        tun, queued,
        ("LIVE pid %d" % drainer) if drainer else "not running",
        ("LIVE pid %d" % rnd) if rnd else "none",
        last))
    if rnd:
        return
    reasons = []
    if tun.startswith("DOWN"):
        reasons.append("tunnel DOWN (run local-model/spark/tunnel.sh up)")
    if queued == 0:
        reasons.append("queue EMPTY")
    elif not drainer:
        reasons.append("%d queued but NO drainer (start local-model/spark/queue.sh)" % queued)
    if reasons or not drainer:
        since = ""
        if last_dt:
            mins = int((now() - last_dt).total_seconds() // 60)
            since = " since last round %d min ago" % mins
        print("SPARK: ⚠ IDLE%s — %s — allocate a task NOW (rule 2026-10-28: never keep the Spark idle)" % (
            since, "; ".join(reasons) if reasons else "no round running"))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # noqa: BLE001
        print("SPARK: status unreadable — %s: %s" % (type(e).__name__, e))
    sys.exit(0)
