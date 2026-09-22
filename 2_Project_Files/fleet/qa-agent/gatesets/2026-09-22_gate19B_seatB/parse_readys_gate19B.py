#!/usr/bin/env python3
"""parse_readys_gate19B.py — read the nine captured READY mails and print a COMPACT per-PR pin table (head / tree / branch / title / files +/- /
per-section apply rows (blob12, lines, canonical sha16, opts) / A4-A5 counts / lane counts / lock window / in-hook legs / typecheck / batch tree).
Read-only; stdout. The drafter builds round19B.py from this output (every value a CLAIM of the seat until re-derived)."""
import re, glob, os
G = os.path.dirname(os.path.abspath(__file__))
files = sorted(glob.glob(G + '/mail_seatB19_ready0[1-3]_*.md')) + sorted(glob.glob(G + '/mail_seatB20_ready0[4-9]_*.md'))
PAT = [('READY', r'^READY FOR QA'), ('BRANCH', r'^feature/'), ('TIER', r'Tier: '), ('LOCK', r'lock started_utc'), ('PR', r'^1\. PR number'),
       ('FILES', r'^   Blockchain/Dev|^   systemTest/'), ('HEAD', r'^2\. Head SHA'), ('TREE', r'^   = item 0'), ('STAGE', r'--- code_patch stage|--- test_only stage|--- .* stage '),
       ('OPTS', r'section_[0-9]\.opts'), ('CAT', r'cat\(section'), ('APPLY', r'^       apply '), ('CHECK', r'^       --check:'), ('AFTER', r'^       after .* blob'),
       ('A4', r'A4 the test file at the head|A4: [0-9]+ red|RED-FIRST'), ('A5', r'A5 the test file WITH|A5: '), ('LANE', r'whole services|whole packages|whole systemTest'),
       ('TSC', r'tsc --noEmit'), ('TC', r'typecheck_pre19'), ('COUNTS', r'LANE COUNTS'), ('HOOK', r'In-hook preflight'), ('PROTO', r'Push protocol'), ('NUMSTAT', r'numstat vs HEAD'),
       ('PRTREE', r'The per-PR tree'), ('BATCH', r'Batch tree'), ('AMEND', r'[Aa]mend|whitespace-stripped|git diff -w|instrument'), ('CLAUDE', r'Claude-written|Claude-authored|CLAUDE-WRITTEN'),
       ('TAMPER', r'tamper|TAMPER'), ('CENSUS', r'Connection census|CENSUS'), ('PAIR', r'PAIR|pair blob|--pair-blob'), ('SUBJECT', r'The commit subject')]
for f in files:
    print('#' * 10, os.path.basename(f))
    seen = set()
    for line in open(f, encoding='utf-8'):
        line = line.rstrip('\n')
        for tag, p in PAT:
            if re.search(p, line):
                key = (tag, line[:120])
                if key in seen: break
                seen.add(key)
                print('[%s] %s' % (tag, line.strip()[:420]))
                break
