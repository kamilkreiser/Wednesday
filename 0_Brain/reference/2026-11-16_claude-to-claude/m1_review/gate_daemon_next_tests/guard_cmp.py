#!/usr/bin/env python3
"""QA-DAEMON-NEXT (b): compare qa_guard.py's BASE and HEAD outputs case by case, after normalising only
the values that change from run to run (elapsed time, the relay's timestamps and port, thread ids).
Usage: python3 -B -I guard_cmp.py <base out> <head out>"""
import re, sys


def norm(l):
    l = re.sub(r"\| \d+\.\d+s \|", "| <t> |", l)
    l = re.sub(r"\d{10} relay (listening|stopped)", r"<ts> relay \1", l)
    l = re.sub(r"127\.0\.0\.1:\d+", "127.0.0.1:<port>", l)
    l = re.sub(r"thread 'main' \(\d+\)", "thread 'main' (<tid>)", l)
    return l.split(" | ", 1)[1] if " | " in l else l


a = [norm(l) for l in open(sys.argv[1]).read().splitlines()]
b = [norm(l) for l in open(sys.argv[2]).read().splitlines()]
same = diff = 0
for x, y in zip(a, b):
    if x == y:
        same += 1
    else:
        diff += 1
        print("BASE:", x)
        print("HEAD:", y)
        print()
print(f"lines {len(a)}/{len(b)}; identical after normalising: {same}; different: {diff}")
