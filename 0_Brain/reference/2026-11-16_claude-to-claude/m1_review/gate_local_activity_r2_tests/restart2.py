#!/usr/bin/env python3
"""QA-LOCAL-ACTIVITY-R2 item 3: restarts under the viewer. The viewer is held with SIGSTOP between two polls while
the daemon is killed and started again (same data dir) and decides N calls through the REAL hook; then SIGCONT.
Scenarios: fewer / equal / more decisions than the viewer had seen; two restarts inside one hold; zero decisions
after the restart; a restart before the viewer had any entry. Each twice.
usage: python3 -B restart2.py <bin dir> <root (new, short)> <out dir (new)>"""
import os, re, signal, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "forge2.py")).read()
exec(src.split("\ndef aim(")[0])          # helpers only (start, hook, ev, viewer, all_lines, render, wrap, ...)

RESTART = FIXED[0]


def entries(text):
    out, cur = [], None
    for r in text.split("\n"):
        if HEAD.match(r):
            out.append(r)
        elif r.startswith(MARK) and out:
            out[-1] += r[len(MARK):]
    return out


def scenario(name, seen, plan, rep_i):
    """seen: decisions before the viewer starts; plan: list of decision counts, one per restart inside the hold."""
    tag = f"{name}{rep_i}"
    dd = os.path.join(ROOT, tag)
    start(tag, dd)
    for i in range(seen):
        hook(dd, ev("Read", {"file_path": f"{WS}/old{i}"}))
    v = viewer(dd, tag)
    t0 = time.time()
    while True:  # wait until the viewer has printed all `seen` entries (or the header when 0)
        t = open(os.path.join(OUTD, tag + ".out")).read()
        if len(entries(t)) == seen and HEADER in t:
            break
        if time.time() - t0 > 15:
            raise SystemExit(f"{tag}: viewer did not show {seen}")
        time.sleep(0.05)
    time.sleep(0.1)                  # it is now in its 0.5 s pause (no request in flight)
    os.kill(v.pid, signal.SIGSTOP)
    starts = []
    for j, n in enumerate(plan):
        starts.append(all_lines(dd)[1]["start"])
        procs.pop(tag).kill(); time.sleep(0.05)
        start(tag, dd)
        for i in range(n):
            hook(dd, ev("Read", {"file_path": f"{WS}/r{j}new{i}"}))
    starts.append(all_lines(dd)[1]["start"])
    os.kill(v.pid, signal.SIGCONT)
    want = plan[-1]
    t0 = time.time()
    while time.time() - t0 < 6:
        t = open(os.path.join(OUTD, tag + ".out")).read()
        if RESTART in t and len(entries(t.split(RESTART)[-1])) >= want:
            break
        time.sleep(0.05)
    time.sleep(1.2)                  # a few more polls: nothing more may appear
    v.terminate(); v.wait()
    procs.pop(tag).terminate()
    t = open(os.path.join(OUTD, tag + ".out")).read()
    rows = t.split("\n")
    n_restart = rows.count(RESTART)
    before = entries(t.split(RESTART)[0]) if RESTART in t else entries(t)
    after = entries(t.split(RESTART, 1)[1]) if RESTART in t else []
    last = plan[-1]
    ok = (n_restart == 1 and len(before) == seen
          and [int(e.split(" ")[0][1:]) for e in after] == list(range(1, last + 1))
          and all(f"/r{len(plan)-1}new{i}" in after[i] for i in range(last))
          and len(set(starts)) == len(starts))
    say(f"{'PASS' if ok else 'FAIL'} {tag}: seen {seen}, restarts {len(plan)} with {plan} decisions -> restart lines {n_restart}; "
        f"entries before {len(before)}, after {[e.split(' ')[0] for e in after]}; distinct start values {len(set(starts))}/{len(starts)}")
    if not ok:
        fails.append(tag)
        say("   output:\n   " + "\n   ".join(r[:100] for r in rows))
    return starts


def main():
    allstarts = []
    for rep_i in (1, 2):
        allstarts += scenario("fewer", 5, [2], rep_i)
        allstarts += scenario("equal", 3, [3], rep_i)
        allstarts += scenario("more", 3, [6], rep_i)
        allstarts += scenario("two", 3, [2, 4], rep_i)
        allstarts += scenario("zero", 3, [0], rep_i)
        allstarts += scenario("empty", 0, [2], rep_i)
    say(f"start values seen: {len(allstarts)}, distinct {len(set(allstarts))}, all 32 lowercase hex: "
        f"{all(re.fullmatch(r'[0-9a-f]{32}', s) for s in allstarts)}")
    open(os.path.join(OUTD, "starts.txt"), "w").write("\n".join(allstarts) + "\n")
    # search every start value as bytes in the data dirs and the stderr logs of all these runs
    hits = []
    for root, _, files in os.walk(ROOT):
        for f in files:
            p = os.path.join(root, f)
            try:
                b = open(p, "rb").read()
            except OSError:
                continue
            for s in allstarts:
                if s.encode() in b or s.upper().encode() in b:
                    hits.append((p, s))
    say(f"{'PASS' if not hits else 'FAIL'} start values found in files under the run root (data dirs, sockets dir, stderr logs): {len(hits)} {hits[:3]}")
    if hits:
        fails.append("start on disk")
    # control: the same search over a planted file holding one start value
    cp = os.path.join(OUTD, "control_plant.bin"); open(cp, "wb").write(b"\x00junk" + allstarts[3].encode() + b"\xff")
    found = any(s.encode() in open(cp, "rb").read() for s in allstarts)
    say(f"{'PASS' if found else 'FAIL'} control: the search finds a planted start value: {found}")
    if not found:
        fails.append("control")
    say(f"FAILS: {len(fails)} {fails}")


try:
    main()
finally:
    for nm, p in list(procs.items()):
        try:
            os.kill(p.pid, signal.SIGCONT)
        except Exception:
            pass
        p.kill(); p.wait()
