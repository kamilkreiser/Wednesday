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

TYPED CLOCKS (ledger _ledger_laptop_datasec.md 2026-10-24, w=4: "08:2x", "08:5x" typed into stamp prose
while the clock read 08:14 / 09:01). Also refuses, before anything is written, a slot VALUE that holds
  (a) a placeholder clock such as 08:2x / 9:1X: an estimate is never a reading, so it is never stamped;
  (b) an exact literal clock right after one of Tuesday's OWN reading phrases ("read whole", "read whole
      at/by", "printed nothing ... at", "empty at", "free at", "absent at", "MEASURED <word> at"): that
      time is this script's to write, so the value must say @NOW@ there.
Exact clocks QUOTED from someone else's artefact (a drafter's MEASURED-BY-DRAFTER 08:56:24, a ruling's
08:52, a deadline "HARD STOP 11:30") are not refused: they are copies, and their source is named beside them.
STAMP_ALLOW_CLOCK="<reason>" passes a refused value and prints the reason (for a phrase this rule
misreads; say which in the note).
"""
import datetime, json, os, re, sys

CLOCK_X = re.compile(r"\b[0-2]?[0-9]:[0-5][xX]\b")
OWN_READ = re.compile(
    r"(read whole(?: at| by)?|printed nothing(?: \(rc \d+\))? at|(?:empty|free|absent|clean) at|"
    r"MEASURED \w+ at)\s+[0-2]?[0-9]:[0-5][0-9](?::[0-5][0-9])?\b", re.I)

def clock_refusal(key, raw):
    hits = [m.group(0) for m in CLOCK_X.finditer(raw)] + [m.group(0) for m in OWN_READ.finditer(raw)]
    if not hits:
        return None
    return (f"REFUSED: label {key!r} holds a typed clock {hits!r}; an estimate (HH:Mx) is never stamped "
            f"and Tuesday's own reading time is written as @NOW@ (ledger 2026-10-24 w=4); nothing written")

brief, slots_path = sys.argv[1], sys.argv[2]
text = open(brief, encoding="utf-8").read()
slots = json.load(open(slots_path, encoding="utf-8"))
now = datetime.datetime.now().strftime("%H:%M")
U = "_" * 4
lines = text.split("\n")
done = {}
allow = os.environ.get("STAMP_ALLOW_CLOCK", "").strip()
for key, val in slots.items():
    why = clock_refusal(key, val)
    if why and not allow:
        sys.exit(why)
    if why:
        print(f"STAMP_ALLOW_CLOCK used for {key!r}: {allow}")
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
