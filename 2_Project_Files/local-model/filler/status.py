#!/usr/bin/env python3
"""status.py - the filler queue's line for the never-idle check (fleet/spark_status.py prints it after its own lines).

  FILLER: queued N · running R · done D (accepted a · flagged f · rejected r) · failed X
  FILLER: ⚠ Spark IDLE with N filler task(s) queued - run: python3 <abs path>/run_filler.py     (only when the gates are open)
  FILLER: Spark busy (<reasons>) - N queued, waiting                                           (queued but a gate is closed)
Never raises: an error prints 'FILLER: status unreadable - ...'. Env FILLER_NO_NET=1 skips the tunnel probe (tests).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def lines():
    import filler_lib as L
    rows = L.read_queue(os.path.join(HERE, "queue.tsv"))
    c = {}
    for r in rows:
        c[r["status"]] = c.get(r["status"], 0) + 1
    q = c.get("queued", 0)
    done = sum(c.get(k, 0) for k in ("done_accepted", "done_flagged", "done_rejected"))
    out = ["FILLER: queued %d · running %d · done %d (accepted %d · flagged %d · rejected %d) · failed %d" % (
        q, c.get("running", 0), done, c.get("done_accepted", 0), c.get("done_flagged", 0), c.get("done_rejected", 0), c.get("failed", 0))]
    if q:
        if os.environ.get("FILLER_NO_NET") == "1":
            why = [w for w in L.gate_reasons_local()]
        else:
            why = L.gate_reasons()
        if why:
            out.append("FILLER: Spark busy (%s) - %d queued, waiting" % ("; ".join(why), q))
        else:
            out.append("FILLER: ⚠ Spark IDLE with %d filler task(s) queued - run: python3 %s" % (q, os.path.join(HERE, "run_filler.py")))
    return out


def main():
    try:
        for l in lines():
            print(l)
    except Exception as e:  # noqa: BLE001
        print("FILLER: status unreadable - %s: %s" % (type(e).__name__, e))


if __name__ == "__main__":
    main()
    sys.exit(0)
