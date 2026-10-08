#!/usr/bin/env python3
"""seat_ctx.py — read each live seat's context use from its session transcript.

WHY (2026-10-08 17:5x): with four raise seats beside Wednesday, each cockpit pane is 8 rows
tall and Claude Code's statusline (ctx:NN%) no longer renders in it, so a pane capture
returns nothing. Every ctx gate is a mail handshake in which Wednesday reads the seat's
context; this is the instrument for when the pane cannot show it.

HOW: the last `usage` record in a transcript (input + cache_read + cache_creation tokens)
is the context the model saw on its last turn. The seat is identified from the transcript
itself: the "(Seat <L> <nth>)" label that occurs most often. Percent = tokens / WINDOW,
and WINDOW is CALIBRATED, never assumed: pass --calibrate <own-jsonl> <statusline %> (a seat
whose statusline you CAN read) or the default 1,000,000 is used and printed as UNCALIBRATED.

Usage: seat_ctx.py [--project-dir <~/.claude/projects/...>] [--hours 6]
                   [--calibrate <jsonl> <pct>]
"""
import argparse, glob, json, os, re, sys, time
from collections import Counter

ap = argparse.ArgumentParser()
ap.add_argument("--project-dir", default=os.path.expanduser(
    "~/.claude/projects/-Volumes-DevMASTER--CODING-Secuura-Blockchain"))
ap.add_argument("--hours", type=float, default=6.0)
ap.add_argument("--calibrate", nargs=2, metavar=("JSONL", "PCT"))
a = ap.parse_args()

def last_tokens(path):
    last = None
    with open(path, errors="replace") as fh:
        for line in fh:
            try:
                j = json.loads(line)
            except ValueError:
                continue
            m = j.get("message")
            if isinstance(m, dict) and m.get("usage"):
                last = m["usage"]
    if not last:
        return None
    return sum((last.get(k) or 0) for k in
               ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))

window, cal = 1_000_000, "UNCALIBRATED (default 1,000,000)"
if a.calibrate:
    t = last_tokens(a.calibrate[0])
    if not t:
        sys.exit("seat_ctx: calibration transcript has no usage record")
    window = round(t / (float(a.calibrate[1]) / 100.0))
    cal = f"calibrated: {t:,} tokens = {a.calibrate[1]}% -> window ~{window:,}"

cutoff = time.time() - a.hours * 3600
files = [f for f in glob.glob(os.path.join(a.project_dir, "*.jsonl")) if os.path.getmtime(f) >= cutoff]
if not files:
    sys.exit(f"seat_ctx: 0 transcripts modified in the last {a.hours} h under {a.project_dir}")
print(f"# {cal}")
seat_re = re.compile(r"\(Seat ([A-Z]) (\d+(?:st|nd|rd|th))\)")
for f in sorted(files, key=os.path.getmtime):
    with open(f, errors="replace") as fh:
        c = Counter(f"{m.group(1)} {m.group(2)}" for m in seat_re.finditer(fh.read()))
    seat, n = (c.most_common(1)[0] if c else ("?", 0))
    second = c.most_common(2)[1][1] if len(c) > 1 else 0
    tok = last_tokens(f)
    pct = f"{100.0 * tok / window:.0f}%" if tok else "n/a"
    flag = "" if n > 2 * second else "  AMBIGUOUS seat label"
    print(f"{os.path.basename(f)[:8]}  {time.strftime('%H:%M:%S', time.localtime(os.path.getmtime(f)))}"
          f"  seat={seat} ({n} vs next {second})  tokens={tok}  ctx~{pct}{flag}")
