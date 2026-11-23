#!/usr/bin/env python3
"""Item 5b follow-up for raw/M3-int-r2/pane.bytes: the old file with ONLY the URL-encoded run-folder path replaced by
<RUN> must equal the head file byte for byte; and the OSC-8 link structure and the W1.txt text are unchanged.
usage: qa2_meaning_panebytes.py <clone> <old> <new>   (run path from env QA_RUN; never printed)"""
import os, subprocess, sys
clone, old, new = sys.argv[1:4]; f = "spikes/U-B1-hook-allow-silent/raw/M3-int-r2/pane.bytes"
a = subprocess.run(["git","-C",clone,"show","%s:%s"%(old,f)],capture_output=True).stdout
b = subprocess.run(["git","-C",clone,"show","%s:%s"%(new,f)],capture_output=True).stdout
run = os.environ["QA_RUN"]; enc = run.replace(" ","%20").replace("!","%21").encode()
print("old bytes %d, new bytes %d; URL-encoded run path occurrences in old: %d (plain-space-encoded only: %d)" % (len(a), len(b), a.count(enc), a.count(run.replace(" ","%20").encode())))
for e in (enc, run.replace(" ","%20").encode()):
    if a.count(e): x = a.replace(e, b"<RUN>"); print("old with only that path -> <RUN> equals new:", x == b)
print("OSC-8 opens old/new:", a.count(b"\x1b]8;;"), b.count(b"\x1b]8;;"), "| 'W1.txt' old/new:", a.count(b"W1.txt"), b.count(b"W1.txt"))
