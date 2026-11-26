# QA-AUDIT-EMAIL-2 scope checks (property a). Usage: python3 -B scope.py <clone>
import sys, subprocess, difflib, hashlib, re
C = sys.argv[1]; B = 'd4979dfe554c26019ed23139852813f95d5a4b25'; H = '5aa56e1217947471bbb358c6a5a5214f31ee65a8'
def git(*a): return subprocess.run(['git', '--no-optional-locks', '-C', C, *a], capture_output=True).stdout
def show(rev, p):
    r = subprocess.run(['git', '-C', C, 'show', f'{rev}:{p}'], capture_output=True)
    return r.stdout if r.returncode == 0 else None
NINE = ['BACKLOG.md', 'crates/coagent-audit/Cargo.toml', 'crates/coagent-audit/build.rs', 'crates/coagent-audit/src/redact.rs',
        'crates/coagent-audit/tests/ae2_email.rs', 'crates/coagent-audit/tests/ae_email.rs', 'docs/AUDIT.md', 'docs/M0-OUTCOMES.md', 'scripts/red-controls-audit.sh']
ex = [f':(exclude){p}' for p in NINE]
out = git('diff', '--name-only', B, H, '--', '.', *ex).decode().split()
print('1. paths outside the nine:', len(out), out)
out2 = git('diff', '--name-only', B, H, '--', '.', *ex[:-1]).decode().split()
print('   control (last exclusion dropped):', len(out2), out2)
def ops(p):
    a = (show(B, p) or b'').decode().split('\n'); b = (show(H, p) or b'').decode().split('\n')
    return a, b, [o for o in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if o[0] != 'equal']
# 2. redact.rs removed lines (base numbering)
a, b, op = ops('crates/coagent-audit/src/redact.rs')
fn_line = next(i for i, l in enumerate(a) if l.strip().startswith('pub fn emails('))
doc0 = fn_line
while a[doc0 - 1].strip().startswith('///'): doc0 -= 1
def body_end(lines, start):
    d = 0; seen = False
    for j in range(start, len(lines)):
        d += lines[j].count('{') - lines[j].count('}')
        if '{' in lines[j]: seen = True
        if seen and d == 0: return j
edl = next(i for i, l in enumerate(a) if l.strip().startswith('fn email_domain_ok('))
em_end = body_end(a, fn_line); ed_end = body_end(a, edl)
allowed = {6, 138, 249} | set(range(doc0, em_end + 1)) | set(range(edl, ed_end + 1))
print(f'2. base emails doc :{doc0+1}-{fn_line}, body :{fn_line+1}-{em_end+1}; email_domain_ok :{edl+1}-{ed_end+1}')
rem = [i for t, i1, i2, j1, j2 in op if t in ('replace', 'delete') for i in range(i1, i2)]
bad = [i + 1 for i in rem if i not in allowed]
print('   removed lines of redact.rs:', len(rem), 'outside allowed places:', bad)
print('   hunks (base i1-i2 -> head j1-j2):', [(t, i1 + 1, i2, j1 + 1, j2) for t, i1, i2, j1, j2 in op])
# 3. ae_email.rs
a, b, op = ops('crates/coagent-audit/tests/ae_email.rs')
print('3. ae_email.rs opcodes:', [(t, i1 + 1, i2, j1 + 1, j2) for t, i1, i2, j1, j2 in op])
for t, i1, i2, j1, j2 in op: print('   removed:', a[i1:i2])
print('   head sha256', hashlib.sha256(show(H, 'crates/coagent-audit/tests/ae_email.rs')).hexdigest(), 'base', hashlib.sha256(show(B, 'crates/coagent-audit/tests/ae_email.rs')).hexdigest())
# 4. AUDIT.md
a, b, op = ops('docs/AUDIT.md')
print('4. AUDIT.md opcodes (base lines):', [(t, i1 + 1, i2, j1 + 1, j2) for t, i1, i2, j1, j2 in op])
print('   base :679 =', repr(a[678][:90]), '| head same line index 680:', repr(b[679][:90]) if len(b) > 679 else None)
ok4 = all((t == 'insert' and i1 in (40, 686, 882)) or (set(range(i1, i2)) <= set(range(36, 40)) | set(range(679, 686)) | {881}) for t, i1, i2, j1, j2 in op)
print('   all hunks inside base 37-40, 680-686, 882:', ok4)
# 5. BACKLOG, M0
for p in ('BACKLOG.md', 'docs/M0-OUTCOMES.md'):
    a, b, op = ops(p)
    print(f'5. {p}: non-insert ops', [o for o in op if o[0] != 'insert'], 'inserts after base lines', [(i1, j2 - j1) for t, i1, i2, j1, j2 in op if t == 'insert'])
mb, mh = show(B, 'docs/M0-OUTCOMES.md'), show(H, 'docs/M0-OUTCOMES.md')
print('   M0 base is a byte prefix of head:', mh.startswith(mb), len(mb), len(mh))
# 6. red script
a, b, op = ops('scripts/red-controls-audit.sh')
print('6. red script opcodes:', [(t, i1 + 1, i2, j1 + 1, j2) for t, i1, i2, j1, j2 in op])
for t, i1, i2, j1, j2 in op: print('   -', a[i1:i2]); print('   +', b[j1:j2])
def rows(lines):
    s = next(i for i, l in enumerate(lines) if l.startswith('ROWS=(')); e = next(i for i in range(s, len(lines)) if lines[i].strip() == ')')
    return [l for l in lines[s + 1:e] if l.strip().startswith('"')], s, e
ra, _, _ = rows(a); rb, s_, e_ = rows(b)
print('   rows base', len(ra), 'head', len(rb), '; base rows equal head prefix except:', [(i, x, y) for i, (x, y) in enumerate(zip(ra, rb)) if x != y])
def mut(lines):
    s = next(i for i, l in enumerate(lines) if l.startswith('MUTANTS=(')); e = next(i for i in range(s, len(lines)) if lines[i].strip() == ')')
    return [l for l in lines[s + 1:e] if l.strip().startswith('"')]
print('   MUTANTS base', len(mut(a)), 'head', len(mut(b)), 'equal', mut(a) == mut(b))
print('   new rows:'); [print('    ', r) for r in rb[len(ra):]]
# 7. build.rs, Cargo.toml
for p in ('crates/coagent-audit/build.rs', 'crates/coagent-audit/Cargo.toml'):
    a, b, op = ops(p)
    print(f'7. {p}:', [(t, i1 + 1, i2, j1 + 1, j2) for t, i1, i2, j1, j2 in op])
    for t, i1, i2, j1, j2 in op: print('   +', b[j1:j2]); print('   context after:', b[j2:j2 + 1], 'before:', b[j1 - 1:j1])
    print('   lines starting 4 spaces + quote:', sum(l.startswith('    "') for l in a), sum(l.startswith('    "') for l in b))
# 8. Cargo.lock / root Cargo.toml / unsafe
print('8. diff Cargo.lock Cargo.toml bytes:', len(git('diff', B, H, '--', 'Cargo.lock', 'Cargo.toml')))
added = [l[1:] for l in git('diff', B, H).decode().split('\n') if l.startswith('+') and not l.startswith('+++')]
print('   added lines', len(added), 'with unsafe:', sum('unsafe' in l for l in added), 'control (+1 planted):', sum('unsafe' in l for l in added + ['    unsafe { x() }']))
print('   src paths changed:', git('diff', '--name-only', B, H, '--', 'crates/coagent-audit/src').decode().split())
