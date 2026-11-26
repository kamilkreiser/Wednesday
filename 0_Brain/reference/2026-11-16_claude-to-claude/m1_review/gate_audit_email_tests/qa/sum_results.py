# sum every "test result" line of a cargo test log, split into test targets and doc-tests
import re, sys
acc = {'targets': [0, 0, 0, 0], 'doc-tests': [0, 0, 0, 0]}; kind = 'targets'; per = {}; name = None
for l in open(sys.argv[1], errors='replace'):
    if 'Running ' in l: kind = 'targets'; name = l.split('Running ')[1].split(' (')[0].strip() + ' ' + l.split('(')[-1].split('/')[-1].split('-')[0]
    if 'Doc-tests' in l: kind = 'doc-tests'; name = l.strip()
    m = re.search(r'test result: (\w+)\. (\d+) passed; (\d+) failed; (\d+) ignored', l)
    if m:
        a = acc[kind]; a[0] += 1; a[1] += int(m.group(2)); a[2] += int(m.group(3)); a[3] += int(m.group(4)); per[name] = m.group(2, 3, 4)
for k, a in acc.items(): print(f'{sys.argv[1].split("/")[-1]} {k}: {a[0]} result lines, {a[1]} passed, {a[2]} failed, {a[3]} ignored')
if len(sys.argv) > 2:
    import json; json.dump(per, open(sys.argv[2], 'w'), indent=0)
