#!/usr/bin/env python3
"""capacity_status.py — is the fleet using every seat this machine can carry?

Kam 2026-10-28 17:5x (terminal): "its good refinement so please track so we can make sure that we
always keep as many agents active as possible. there are a lot of tickets to get through".
Rule: learnings/2026-10-28_track-agent-capacity-keep-the-floor-full.md.

Prints ONE line, always exits 0 (it rides send_brief.sh, doctor.sh and the boot, so it must never block):
  CAPACITY: seats N (letters) · load1 L · mem free M% · ROOM -> launch the next lane NOW
  CAPACITY: seats N (letters) · load1 L · mem free M% · FULL (load) / FULL (memory)
and appends the same reading to fleet/state/capacity_log.tsv (one row per call) so the day can be
reviewed: how much of the time the floor had room and nobody filled it.

Thresholds are the fleet's existing launch rule (load1 < 7, STANDING wave rule) plus a memory floor;
override with CAP_LOAD_MAX / CAP_MEM_MIN. Test hooks: CAP_PANES_CMD, CAP_LOAD, CAP_MEMFREE, CAP_LOG.
"""
import os, re, subprocess, sys, time

LOAD_MAX = float(os.environ.get("CAP_LOAD_MAX", "7"))
MEM_MIN = float(os.environ.get("CAP_MEM_MIN", "25"))
HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.environ.get("CAP_LOG", os.path.join(HERE, "state", "capacity_log.tsv"))


def run(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10).stdout
    except Exception as e:  # never block a send
        return ""


def main():
    try:
        panes = run(os.environ.get("CAP_PANES_CMD", "tmux list-panes -t fleet:0 -F '#{@cockpit_name}'"))
        seats = [p.strip() for p in panes.splitlines() if re.match(r"^(Secuura|Datasec)/", p.strip())]
        letters = ",".join(s.split("-")[-1] if "-" in s else s.split("/")[-1] for s in seats) or "-"
        load = os.environ.get("CAP_LOAD") or run("sysctl -n vm.loadavg").split()[1]
        load = float(load)
        mem = os.environ.get("CAP_MEMFREE")
        if mem is None:
            m = re.search(r"free percentage:\s*(\d+)", run("memory_pressure"))
            mem = m.group(1) if m else "-1"
        mem = float(mem)
    except Exception as e:
        print(f"CAPACITY: status unreadable ({e.__class__.__name__}) — read tmux list-panes and uptime by hand")
        return 0
    if load >= LOAD_MAX:
        verdict = f"FULL (load1 >= {LOAD_MAX:g})"
    elif 0 <= mem < MEM_MIN:
        verdict = f"FULL (memory free < {MEM_MIN:g}%)"
    else:
        verdict = "ROOM -> launch the next lane NOW (rule 2026-10-28: keep the floor full)"
    line = f"CAPACITY: seats {len(seats)} ({letters}) · load1 {load:.1f} · mem free {mem:.0f}% · {verdict}"
    print(line)
    try:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        new = not os.path.exists(LOG)
        with open(LOG, "a") as f:
            if new:
                f.write("ts\tseats\tletters\tload1\tmemfree\tverdict\n")
            f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S%z')}\t{len(seats)}\t{letters}\t{load:.2f}\t{mem:.0f}\t{verdict.split(' ')[0]}\n")
    except Exception:
        print("CAPACITY: log not written (state dir unwritable)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
