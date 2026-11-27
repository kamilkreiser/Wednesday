# QA-AUDIT-EMAIL-3 scope checks by program (new). Reads `git show` of base and head from the fetch-only repo.
import subprocess, difflib, re, hashlib
G = '/private/tmp/claude-501/qae3/gho'; B = '5aa56e1217947471bbb358c6a5a5214f31ee65a8'; Hd = '627431877d5fa3b86f91ec23d0dc2879c800eb33'
def show(rev, p):
    r = subprocess.run(['git', '-C', G, 'show', f'{rev}:{p}'], capture_output=True)
    return r.stdout.decode() if r.returncode == 0 else None
def ops(a, b):
    return [o for o in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if o[0] != 'equal']
# redact.rs: removed lines must lie in the base doc comment of `emails`, its body, or the `if c != b'-'` line
ba, he = show(B, 'crates/coagent-audit/src/redact.rs').split('\n'), show(Hd, 'crates/coagent-audit/src/redact.rs').split('\n')
def find_fn(lines, sig):
    i = next(k for k, l in enumerate(lines) if sig in l)
    j = i
    while not lines[j].startswith('    }'): j += 1
    d = i
    while lines[d - 1].strip().startswith('///'): d -= 1
    return d, i, j  # doc start, fn line, closing line (0-based)
ds, fi, fj = find_fn(ba, 'pub fn emails(')
dash = next(k for k, l in enumerate(ba) if l.strip() == "if c != b'-'")
print(f"redact.rs base: emails doc {ds+1}-{fi}, fn {fi+1}-{fj+1}; the dash line {dash+1}")
bad = []; nrem = 0; hunks = []
for tag, i1, i2, j1, j2 in ops(ba, he):
    hunks.append((tag, i1 + 1, i2, j1 + 1, j2))
    for k in range(i1, i2):
        nrem += 1
        if not (ds <= k <= fj or k == dash): bad.append((k + 1, ba[k]))
print(f'redact.rs removed/changed base lines: {nrem}; outside the doc comment+body of emails and the dash line: {len(bad)} {bad[:3]}')
print('redact.rs hunks (tag, base from-to, head from-to):', hunks)
# a control: a one-line change planted outside, reported
he2 = list(he); k = next(i for i, l in enumerate(he2) if 'pub fn find(' in l); he2[k + 2] = he2[k + 2] + ' '
cbad = [k for tag, i1, i2, j1, j2 in ops(ba, he2) for k in range(i1, i2) if not (ds <= k <= fj or k == dash)]
print('control (one byte planted in find): lines reported outside:', len(cbad))
# ae_email.rs: base 412-418 replaced by the eight prescribed lines exactly
NEW8 = '''/// The join actually used: the generator does not produce the shapes below, and falls back to a
/// space for them. The first email rule did not catch them; the coordinator's later rulings
/// narrowed those exclusions (the doc comment of `patterns::emails` holds the current grammar),
/// and this property still does not generate them:
/// - before the address, a `scheme://` token joined by nothing, `:` or `=`;
/// - after the address, `:`;
/// - after the address, nothing, when the neighbour starts with domain bytes that are not letters
///   only, or with letters then `:` and a non-space.'''.split('\n')
ab, ah = show(B, 'crates/coagent-audit/tests/ae_email.rs').split('\n'), show(Hd, 'crates/coagent-audit/tests/ae_email.rs').split('\n')
exp = ab[:411] + NEW8 + ab[418:]
print('ae_email.rs: head == base[:411] + the 8 prescribed lines + base[418:]:', ah == exp, '; base line 419:', ab[418][:40], '; git-style ops:', ops(ab, ah))
print('   common line kept by git (base 417 / head 418):', ab[416] == ah[417], repr(ab[416][:70]))
# docs/AUDIT.md hunks
db, dh = show(B, 'docs/AUDIT.md').split('\n'), show(Hd, 'docs/AUDIT.md').split('\n')
print('docs/AUDIT.md hunks (base from-to):', [(t, i1 + 1, i2) for t, i1, i2, j1, j2 in ops(db, dh)])
# BACKLOG and M0: every base line kept in order (only inserts); M0 base a byte prefix
for p in ('BACKLOG.md', 'docs/M0-OUTCOMES.md'):
    x, y = show(B, p), show(Hd, p)
    o = ops(x.split('\n'), y.split('\n'))
    print(p, 'ops:', [(t, i1 + 1, i2, j1 + 1, j2) for t, i1, i2, j1, j2 in o], 'only inserts:', all(t == 'insert' for t, *_ in o), '; base is a byte prefix:', y.startswith(x))
# red script
rb, rh = show(B, 'scripts/red-controls-audit.sh'), show(Hd, 'scripts/red-controls-audit.sh')
def rows(s):
    L = s.split('\n'); a = next(i for i, l in enumerate(L) if l.startswith('ROWS=(')); b = next(i for i in range(a, len(L)) if L[i] == ')')
    body = L[a + 1:b]; r = [l for l in body if l.strip() and not l.strip().startswith('#')]
    m1 = next(i for i, l in enumerate(L) if l.startswith('MUTANTS=(')); m2 = next(i for i in range(m1, len(L)) if L[i] == ')')
    return a + 1, b + 1, body, r, [l for l in L[m1 + 1:m2] if l.strip() and not l.strip().startswith('#')], L
ra, rbb, bodyb, rowsb, mb, Lb = rows(rb); ha, hb, bodyh, rowsh, mh, Lh = rows(rh)
print(f'red script: base ROWS=( at {ra}, ) at {rbb}, rows {len(rowsb)}, MUTANTS {len(mb)}; head ROWS=( at {ha}, ) at {hb}, rows {len(rowsh)}, MUTANTS {len(mh)}')
print('   base rows = head first rows, in order:', rowsh[:len(rowsb)] == rowsb, '; head body = base body + 7 lines:', bodyh[:len(bodyb)] == bodyb, len(bodyh) - len(bodyb), '; MUTANTS equal:', mb == mh)
print('   lines outside ROWS equal:', Lb[:ra] == Lh[:ha] and Lb[rbb - 1:] == Lh[hb - 1:])
for l in bodyh[len(bodyb):]: print('   +', l[:200])
# build.rs
bb, bh = show(B, 'crates/coagent-audit/build.rs').split('\n'), show(Hd, 'crates/coagent-audit/build.rs').split('\n')
print('build.rs ops:', [(t, i1 + 1, i2, j1 + 1, j2) for t, i1, i2, j1, j2 in ops(bb, bh)])
for t, i1, i2, j1, j2 in ops(bb, bh):
    for l in bh[j1:j2]: print('   +', l)
print('   lines starting 4 spaces and a quote: base', sum(1 for l in bb if l.startswith('    "')), 'head', sum(1 for l in bh if l.startswith('    "')))
want = "    // The coordinator's ruling: email addresses joined to a link with no path, and before a colon (the owner's ruling: email addresses blanked)"
print('   comment line worded exactly as build brief l.47:', want in bh)
cb, ch = show(B, 'crates/coagent-audit/Cargo.toml').split('\n'), show(Hd, 'crates/coagent-audit/Cargo.toml').split('\n')
print('Cargo.toml ops:', [(t, i1 + 1, i2, j1 + 1, j2) for t, i1, i2, j1, j2 in ops(cb, ch)])
for t, i1, i2, j1, j2 in ops(cb, ch):
    print('   context before:', cb[i1 - 1], '| after:', cb[i1:i1 + 2]); [print('   +', l) for l in ch[j1:j2]]
