#!/usr/bin/env python3
"""stamp_brief.py <brief.md> <slots.json>

Fills a brief's four-underscore Stamp slots BY LABEL and asserts the result.

slots.json maps a label prefix (the text a slot line starts with, after "- ", e.g. "STAMP:" or
"Scope slot YOURS-EXTENSION") to its value. "@NOW@" in a value becomes the local clock read by THIS
script (datetime.now()), never a typed time (ledger 2026-10-20 w=2, typed stamp clocks).
The READ-WHOLE-BY-TUESDAY line is filled from the "READ-WHOLE" key.

Refuses (rc 1, file untouched) unless: every label matches exactly ONE slot line, every replacement
changes its line, and the stamped text holds 0 lines with four underscores. Prints each stamped line.
WHY (ledger 2026-10-19 position-keyed stamp, 2026-10-18 counter that counted attempts): a stamp keyed
on line numbers misaligned slots, and a counter that counted matches reported 9 stamped while 7 were
empty. This one matches labels and counts effects.
"""
import datetime, json, re, sys

brief, slots_path = sys.argv[1], sys.argv[2]
text = open(brief, encoding="utf-8").read()
slots = json.load(open(slots_path, encoding="utf-8"))
now = datetime.datetime.now().strftime("%H:%M")
U = "_" * 4
lines = text.split("\n")
done = {}
for key, val in slots.items():
    val = val.replace("@NOW@", now)
    if key == "READ-WHOLE":
        idx = [i for i, l in enumerate(lines) if l.startswith("READ-WHOLE-BY-TUESDAY:") and U in l]
        new_line = "READ-WHOLE-BY-TUESDAY: " + val
    else:
        idx = [i for i, l in enumerate(lines) if l.startswith("- " + key) and l.rstrip().endswith(U)]
        new_line = None
    if len(idx) != 1:
        sys.exit(f"REFUSED: label {key!r} matched {len(idx)} slot lines (need exactly 1); nothing written")
    i = idx[0]
    old = lines[i]
    if new_line is None:
        new_line = old.rstrip()[: -len(U)] + val
    if new_line == old:
        sys.exit(f"REFUSED: label {key!r} replacement did not change the line; nothing written")
    lines[i] = new_line
    done[key] = i + 1
out = "\n".join(lines)
left = [n + 1 for n, l in enumerate(out.split("\n")) if U in l]
if left:
    sys.exit(f"REFUSED: {len(left)} line(s) still hold four underscores: {left}; nothing written")
open(brief, "w", encoding="utf-8").write(out)
for key, n in done.items():
    print(f"stamped line {n}: {out.split(chr(10))[n-1][:160]}")
print(f"OK: {len(done)} slots stamped by label, 0 four-underscore lines left, clock {now}")
