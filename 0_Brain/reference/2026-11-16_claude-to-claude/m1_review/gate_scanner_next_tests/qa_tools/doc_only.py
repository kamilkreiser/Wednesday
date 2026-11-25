# Reads a unified diff on stdin; every +/- line (not +++/---), trimmed, must start with '///'.
import sys
bad=[]; n=0
for l in sys.stdin.read().splitlines():
    if l.startswith(('+++','---')) or not l[:1] in '+-' or l=='' : continue
    n+=1
    if not l[1:].strip().startswith('///'): bad.append(l)
print(f"{n} changed lines; {len(bad)} not ///: {bad}")
