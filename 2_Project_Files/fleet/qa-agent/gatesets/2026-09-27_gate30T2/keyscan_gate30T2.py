#!/usr/bin/env python3
r"""keyscan_gate30T2.py <scratchpad> — the MG-3 KEY SCAN for ONE gate30 kit (kit.json beside this script), READ only: hyphenated `KS-\d+` and
un-hyphenated `KS\d+` keys in each PR's TITLE, BODY (gh_body_<n>.md, written by gh_read_gate30T2.py) and EVERY commit message in its chain (the scratch
clone, `git log --format=%B mb..head`). Only the PR's OWN key may stay hyphenated in a squash subject / body; every other hyphenated key is FOREIGN and
must be un-hyphenated if quoted. A closing word before a key is counted too. Ends with a CONTROL line (the scanner must find exactly the planted
keys). Writes nothing; prints to stdout."""
import json, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
CL = os.path.join(sys.argv[1], 'g30T2_sp', 'clone.git'); P = json.load(open(os.path.join(G, 'pins_%s.json' % K['kit']), encoding='utf-8'))
HY, UN = r'KS-\d+', r'(?<![-\w])KS\d+'
CLOSE = r'(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+KS-\d+'
def scan(t): return sorted(set(re.findall(HY, t))), sorted(set(re.findall(UN, t)))
print('keyscan_gate30T2 (READ): hyphenated `KS-\\d+` and un-hyphenated `KS\\d+` keys in each PR TITLE, BODY (gh_body_<n>.md) and EVERY commit message of its chain (scratch clone)')
for n in sorted(K['prs']):
    own = set(K['prs'][n]['keys']); gb = open(os.path.join(G, 'gh_body_%s.md' % n), encoding='utf-8').read()
    title = gb.splitlines()[0].split(' ', 1)[1]; body = gb.split('\n', 3)[3]
    pr = P['prs'][n]; msg = subprocess.run(['git', '--git-dir', CL, 'log', '--format=%B', '%s..%s' % (pr['merge_base'], pr['head'])], capture_output=True, text=True).stdout
    for lab, t in (('title', title), ('body', body), ('commit message(s)', msg)):
        hy, un = scan(t)
        print('#%s %s: hyphenated %s | un-hyphenated %s | FOREIGN hyphenated (must be un-hyphenated in the squash): %s' % (n, lab, hy, un, sorted(set(hy) - own) or 'none'))
    print('#%s closing word + key in title %d; in body %d; in commit message(s) %d' % (n, len(re.findall(CLOSE, title)), len(re.findall(CLOSE, body)), len(re.findall(CLOSE, msg))))
print('CONTROL: scanner on "Refs KS-1 and KS22, closes KS-3" -> %s %s closing %d' % (*scan('Refs KS-1 and KS22, closes KS-3'), len(re.findall(CLOSE, 'Refs KS-1 and KS22, closes KS-3'))))
