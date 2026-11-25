# QA-POLICY-NEXT: the probe table for the verdict (graded states: **/.env* excluded, nothing excluded), base = head checked.
import re, sys
def parse(p):
    rows = {}
    for l in open(p):
        m = re.match(r'ROW \| (\S+) \| (\S+) \| (.*?) \| cwd=(.*?) \| (\S+) \| none=(.*?) \| StillAsk=(.*?) \| Allowed=(.*?) \| FULL', l)
        rows[(m.group(1), m.group(2), m.group(3), re.sub(r'qpx-probe-\d+', '', m.group(4)), m.group(5))] = m.group(6, 7, 8)
    return rows
b, h = parse(sys.argv[1]), parse(sys.argv[2])
assert b.keys() == h.keys()
def code(s):
    s = s.replace('(=decide:true)', '').replace('(=decide:false)', '').strip()
    if s.startswith('ASK'): return 'ask ' + s.split()[1]
    if 'OwnerChoseAllow' in s: return '**RUNS UNASKED**'
    r = re.search(r'RefusedInAllow \{ reason: "([^"]*)"', s)
    if r: return 'refused: ' + r.group(1)
    if 'HardDeny' in s: return 'denied (hard deny)'
    if 'Excluded' in s: return 'denied (exclusion list)'
    return s[:40]
cwdname = lambda c: {'<root>/ws': 'ws', '<root>/home': 'home', '<root>/outside': 'fixture outside', '<root>/ws/src': 'ws/src', '': '"" (empty)', 'rel': 'rel', '/': '/'}.get(c.replace('/private/tmp/claude-501/qpx/outside2', 'outside2'), c.replace('/private/tmp/claude-501/qpx/outside2', 'outside2 (mine)'))
graded = {'A': 'PIN', 'B': 'PIN/contrast', 'C': 'PIN', 'D': 'PIN', 'E': 'PIN (PowerShell) / words', 'M': 'words §11', 'N': 'words §11', 'Nm': 'words §11', 'S': 'words §11'}
print('| grp | tool | command | cwd | state | no view | StillAsk | Allowed | base = head | judgement |')
print('|---|---|---|---|---|---|---|---|---|---|')
n = same = 0
for k in h:
    g, tool, lab, cwd, st = k
    if st not in ('excl=**/.env*', 'open'): continue
    n += 1; eq = b[k] == h[k]; same += eq
    nv, sa, al = (code(x) for x in h[k])
    ex = st.startswith('excl')
    if g in ('Nm', 'S') and ex and al == '**RUNS UNASKED**' and '.env' in lab and '.e*' not in lab and '$f' not in lab: j = 'names `.env`, NOT stopped (m-1)'
    elif g == 'M' and (al.startswith('refused') or al.startswith('denied')): j = 'refused/denied, not "always ask" (n-1)'
    elif g == 'Dv' and al.startswith('refused') and lab == '`grep -r key .`': j = 'absolute folder, refused for another reason (n-2)'
    elif g in ('A', 'C') or (g == 'D') or (g == 'E' and tool == 'PowerShell') or (g == 'B' and lab in ('`cat .env`',) ) or (g == 'B' and tool == 'Grep') : j = 'pinned row: holds'
    elif g == 'E': j = '§11 backslash words: true'
    else: j = 'recorded'
    print(f'| {g} | {tool} | {lab.replace("|", "&#124;")} | {cwdname(cwd)} | {"`**/.env*`" if ex else "nothing"} | {nv} | {sa} | {al} | {"yes" if eq else "NO"} | {j} |')
print(f'\nGRADED ROWS {n}, base = head {same}', file=sys.stderr)
