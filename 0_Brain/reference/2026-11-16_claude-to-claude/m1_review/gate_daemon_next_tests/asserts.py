#!/usr/bin/env python3
"""QA-DAEMON-NEXT (f): every assert!/assert_eq!/assert_ne!/panic! of a Rust file, each joined to one line
(whitespace runs collapsed), in source order, with its starting line number.
Usage: python3 -B -I asserts.py <file>   (reads the file; prints one statement per line)"""
import re, sys

s = open(sys.argv[1], encoding="utf-8").read()
pat = re.compile(r"\b(assert_eq|assert_ne|assert|panic)!\s*\(")
i = 0
while True:
    m = pat.search(s, i)
    if not m:
        break
    j = m.end()
    depth = 1
    in_str = False
    while depth and j < len(s):
        c = s[j]
        if in_str:
            if c == "\\":
                j += 1
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
        j += 1
    line = s.count("\n", 0, m.start()) + 1
    print(f"{line}: " + re.sub(r"\s+", " ", s[m.start():j]))
    i = j
