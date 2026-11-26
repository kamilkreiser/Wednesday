# QA-AUDIT-EMAIL scope checks (property a). Usage: python3 -B qa_scope.py <repo>
import subprocess, sys, hashlib, difflib, re
R = sys.argv[1]; B = '5e11609cee1cb483bd006547e9092d49522691cc'; H = 'e31b29ac78fc19c6fc3c8fb206d44e2e91d7877c'
def show(sha, path):
    p = subprocess.run(['git', '--no-optional-locks', '-C', R, 'show', f'{sha}:{path}'], capture_output=True)
    return p.stdout if p.returncode == 0 else None
def block(text, start_re, end_re, item_re):
    out, f = [], False
    for l in text.split('\n'):
        if not f and re.match(start_re, l): f = True; continue
        if f and re.match(end_re, l): break
        if f and re.match(item_re, l): out.append(l)
    return out
# rows
rb = block(show(B,'scripts/red-controls-audit.sh').decode(), r'^ROWS=\(', r'^\)', r'^  "')
rh = block(show(H,'scripts/red-controls-audit.sh').decode(), r'^ROWS=\(', r'^\)', r'^  "')
print('rows base', len(rb), 'head', len(rh), 'base rows prefix of head:', rh[:len(rb)] == rb)
for l in rh[len(rb):]: print('  new row:', l.strip(), 'fields', len(l.strip().strip('"').split('|')))
want = ["redact_no_email|ae_email|ae_listed_addresses_never_appear_in_a_preview|AE-1|address: leaked",
 "email_keeps_domain|ae_email|ae_listed_addresses_never_appear_in_a_preview|AE-1b|domain: leaked",
 "redact_no_email|ae_email|ae_prop_generated_addresses_never_survive|AE-3|leaked",
 "email_keeps_domain|ae_email|ae_prop_generated_addresses_never_survive|AE-3b|leaked"]
got = [l.strip().strip('"') for l in rh[len(rb):]]
print('  lane-brief rows present verbatim:', all(w in got for w in want), '; AE-1c row:', [g for g in got if '|AE-1c|' in g])
mb = block(show(B,'scripts/red-controls-audit.sh').decode(), r'^MUTANTS=\(', r'^\)', r'^  "')
mh = block(show(H,'scripts/red-controls-audit.sh').decode(), r'^MUTANTS=\(', r'^\)', r'^  "')
print('mutants', len(mb), len(mh), mb == mh)
nb = block(show(B,'crates/coagent-audit/build.rs').decode(), r'^const RED', r'^\];', r'^    "')
nh = block(show(H,'crates/coagent-audit/build.rs').decode(), r'^const RED', r'^\];', r'^    "')
print('RED names', len(nb), len(nh), 'prefix:', nh[:len(nb)] == nb, 'new:', [x.strip() for x in nh[len(nb):]])
# line-level: every base line kept in order (base is a subsequence of head) for files with 0 removed
for f in ['BACKLOG.md','crates/coagent-audit/Cargo.toml','crates/coagent-audit/build.rs','scripts/red-controls-audit.sh','docs/M0-OUTCOMES.md','crates/coagent-audit/src/redact.rs']:
    a = show(B,f).decode().split('\n'); b = show(H,f).decode().split('\n')
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    ops = [(t,i1,i2,j1,j2) for t,i1,i2,j1,j2 in sm.get_opcodes() if t != 'equal']
    print(f, 'non-insert ops:', [o for o in ops if o[0] != 'insert'], 'insert runs at head lines:', [(j1+1, j2-j1) for t,i1,i2,j1,j2 in ops if t=='insert'])
# M0 prefix
a = show(B,'docs/M0-OUTCOMES.md'); b = show(H,'docs/M0-OUTCOMES.md')
print('M0 base', len(a.split(b'\n'))-1, 'lines', len(a), 'bytes; byte prefix:', b[:len(a)] == a, hashlib.sha256(b[:len(a)]).hexdigest() == hashlib.sha256(a).hexdigest())
a = show(B,'BACKLOG.md'); b = show(H,'BACKLOG.md'); print('BACKLOG byte prefix:', b[:len(a)] == a)
# AUDIT.md
a = show(B,'docs/AUDIT.md').decode().split('\n'); b = show(H,'docs/AUDIT.md').decode().split('\n')
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
for t,i1,i2,j1,j2 in sm.get_opcodes():
    if t == 'equal': continue
    print('AUDIT.md', t, 'base', i1+1, i2, 'head', j1+1, j2)
    if t == 'replace':
        ow = ' '.join(a[i1:i2]).split(); nw = ' '.join(b[j1:j2]).split()
        # every old word kept in order?
        sm2 = difflib.SequenceMatcher(None, ow, nw, autojunk=False)
        dele = [(ow[x1:x2], nw[y1:y2]) for tt,x1,x2,y1,y2 in sm2.get_opcodes() if tt in ('delete','replace')]
        print('   old words not kept verbatim in order:', dele)
        # subsequence test
        it = iter(nw); print('   old words a subsequence of new words:', all(w in it for w in ow))
        print('   removed base lines:'); [print('     -', x) for x in a[i1:i2]]
