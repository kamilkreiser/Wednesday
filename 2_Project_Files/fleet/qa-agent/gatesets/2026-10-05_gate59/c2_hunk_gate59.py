#!/usr/bin/env python3
"""c2_hunk_gate59.py — gate59 C2: the routes/users.ts hunk ONLY, read against KS-1005's claim ("change-password must read the same hash it
verifies"; a passwordless account keeps 404 per Q-1005). Git objects in YOUR scratch clone only; nothing is run.
  H1 SHAPE    users.ts develop -> head: the ONLY non-comment change is kit hunk.removed_code_line -> kit hunk.added_code_line; every other
              added line is a `//` comment, 0 other removed lines; the comment lines carry KS-1005 and state the prior behaviour (§5d:
              "was getUserById").
  H2 SAME-HASH inside the change-password handler (kit hunk.handler_open to the next `userRoutes.`): the loader is the ONLY statement that
              assigns `user`; nothing between the loader and verifyPassword writes `user` / `user.passwordHash`; verifyPassword reads
              `user.passwordHash` (kit verify_line_kept) — so the hash verified IS the hash the hash-carrying loader read.
  H3 Q-1005   the guard `if (!user || !user.passwordHash) throw new NotFoundError('User');` byte-identical develop vs head, and the next
              code line after the loader (a passwordless account still 404s, before verifyPassword).
  H4 COUNTS   word-bounded `getUserById(` calls in users.ts 8 -> 7 ("the other seven untouched"); `getUserByIdWithPasswordHash(` 0 -> 1; every
              surviving getUserById line byte-identical and in order.
  H5 REPO     userRepo.ts blob identical develop vs head (the PR does not widen USER_COLS); at head getUserByIdWithPasswordHash's SELECT names
              password_hash and USER_COLS does NOT; CONTROL: USER_COLS DOES name mfa_secret (the column test answers both ways).
  INFO (printed, never asserted — the gate rules them): getUserByIdWithPasswordHash `return fromRow(` without `await` (getUserById has the
       KS-999 `return await fromRow`), its missing tenantId parameter, and every non-test `.passwordHash` reader in services/auth/src.
--selftest  T0 the REAL head PASSES; tamper arms each FAIL on the named check: T1 the 404 guard changed to 400 (Q-1005), T2 a second
            getUserById site switched too, T3 the loader kept (comments only), T4 the KS-1005 key stripped from the comments, T5 a statement
            clearing user.passwordHash before verify, T6 USER_COLS widened with password_hash in userRepo.ts.
Usage: c2_hunk_gate59.py --repo <your clone> [--head sha] [--selftest]       rc 0 PASS / 1 FAIL / 2 usage"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate59 import K, git, now, Checks, opt_factory, show, blob, has_commit, opcodes, selftest_arm

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A); REPO = opt('--repo'); HEAD = opt('--head', K['head']); DEV = K['develop']; H = K['hunk']
for s in (HEAD, DEV):
    if not has_commit(REPO, s): print('REFUSING: %s not in %s' % (s[:12], REPO)); raise SystemExit(2)


def is_comment(l):
    s = l.strip(); return s.startswith('//') or s == ''


def handler(src):
    ls = src.split('\n'); st = [i for i, l in enumerate(ls) if l.startswith(H['handler_open'])]
    if len(st) != 1: return None, None
    en = next((j for j in range(st[0] + 1, len(ls)) if ls[j].startswith('userRoutes.')), len(ls))
    return st[0], ls[st[0]:en]


def calls(src, name):
    return [l for l in src.split('\n') if re.search(r'\b%s\(' % re.escape(name), l)]


def judge(C, d, h, repo_d, repo_h):
    dl, hl = d.split('\n'), h.split('\n'); ops = opcodes(dl, hl)
    rem = [dl[i] for o in ops for i in range(o[1], o[2])]; add = [hl[j] for o in ops for j in range(o[3], o[4])]
    crem = [l for l in rem if not is_comment(l)]; cadd = [l for l in add if not is_comment(l)]; com = [l for l in add if is_comment(l) and l.strip()]
    C.chk('H1 shape', crem == [H['removed_code_line']] and cadd == [H['added_code_line']] and len(rem) == 1 and any('KS-1005' in l for l in com) and any('was getUserById' in l for l in com),
          'non-comment removed %r | added %r | removed lines total %d (want 1) | comment lines added %d, carry KS-1005: %s, state the prior call ("was getUserById"): %s' % (
              [l.strip()[:80] for l in crem], [l.strip()[:80] for l in cadd], len(rem), len(com), any('KS-1005' in l for l in com), any('was getUserById' in l for l in com)))
    for l in rem: print('INFO H1 - %s' % l.rstrip()[:160])
    for l in add: print('INFO H1 + %s' % l.rstrip()[:160])
    i0, hb = handler(h); _, db = handler(d)
    if hb is None:
        C.chk('H2 same-hash', False, 'change-password handler not found exactly once at head'); return
    code = [l for l in hb if not is_comment(l)]
    li = [k for k, l in enumerate(code) if l == H['added_code_line']]; vi = [k for k, l in enumerate(code) if l == H['verify_line_kept']]
    assigns = [l for l in code if re.search(r'\b(const|let|var)\s+user\b|(^|[^.\w])user\s*=[^=]', l)]
    between = code[li[0] + 1:vi[0]] if li and vi and li[0] < vi[0] else None
    writes = [l for l in (between or []) if re.search(r'\buser(\.passwordHash)?\s*=[^=]|delete\s+user', l)]
    C.chk('H2 same-hash', len(li) == 1 and len(vi) == 1 and between is not None and len(assigns) == 1 and not writes,
          'handler at head :%d (%d code lines) | hash-carrying loader %d time(s), verifyPassword(user.passwordHash) %d time(s), loader BEFORE verify: %s | statements assigning `user`: %d (want 1) | writes to user / user.passwordHash between them: %s' % (
              i0 + 1, len(code), len(li), len(vi), between is not None, len(assigns), writes or 'NONE'))
    dcode = [l for l in (db or []) if not is_comment(l)]
    nxt = code[li[0] + 1] if li and li[0] + 1 < len(code) else None
    C.chk('H3 Q-1005 404 kept', H['guard_line_kept'] in dcode and H['guard_line_kept'] in code and nxt == H['guard_line_kept'],
          'guard %r at develop: %s, at head: %s, the next code line after the loader: %s' % (H['guard_line_kept'].strip(), H['guard_line_kept'] in dcode, H['guard_line_kept'] in code, nxt == H['guard_line_kept']))
    gd, gh = calls(d, 'getUserById'), calls(h, 'getUserById'); wd, wh = calls(d, 'getUserByIdWithPasswordHash'), calls(h, 'getUserByIdWithPasswordHash')
    surv = list(gd)
    if H['removed_code_line'] in surv: surv.remove(H['removed_code_line'])   # ONE occurrence: all eight lines are byte-identical text
    C.chk('H4 counts', len(gd) == H['getUserById_calls_develop'] and len(gh) == H['getUserById_calls_head'] and len(wd) == 0 and len(wh) == 1 and surv == gh,
          'getUserById( lines %d -> %d (kit %d -> %d) | getUserByIdWithPasswordHash( %d -> %d (want 0 -> 1) | the surviving getUserById lines byte-identical and in order: %s' % (
              len(gd), len(gh), H['getUserById_calls_develop'], H['getUserById_calls_head'], len(wd), len(wh), surv == gh))
    m = re.search(r"const USER_COLS = '([^']*)'", repo_h); cols = [c.strip() for c in m.group(1).split(',')] if m else []
    fn = repo_h[repo_h.find('export async function getUserByIdWithPasswordHash'):][:900]
    sel = re.search(r'SELECT\s+\$\{USER_COLS\},\s*password_hash\s+FROM users', fn) is not None
    C.chk('H5 repo', repo_d == repo_h and m is not None and 'password_hash' not in cols and 'mfa_secret' in cols and sel,
          'userRepo.ts identical develop vs head: %s | USER_COLS %d columns, password_hash in it: %s | CONTROL mfa_secret in it: %s | getUserByIdWithPasswordHash SELECTs ${USER_COLS}, password_hash: %s' % (
              repo_d == repo_h, len(cols), 'password_hash' in cols, 'mfa_secret' in cols, sel))
    print('INFO H6 getUserByIdWithPasswordHash body: `return fromRow(` without await: %s (getUserById: `return await fromRow`: %s) — KS-999 sibling: a throw inside fromRow escapes the 503 classifier on THIS path' % (
        'return fromRow(' in fn, 'return await fromRow(' in repo_h[repo_h.find('export async function getUserById('):][:700]))
    print('INFO H6 getUserByIdWithPasswordHash takes a tenantId parameter: %s (getUserById does: %s) — RLS rests on the ALS tenant GUC; UNMEASURED without a real Postgres' % (
        bool(re.search(r'getUserByIdWithPasswordHash\(id: string, tenantId', repo_h)), bool(re.search(r'getUserById\(id: string, tenantId', repo_h))))


print('c2_hunk_gate59 %s | clone %s | develop %s | head %s' % (now(), REPO, DEV[:12], HEAD[:12]))
P = K['product']; RP = K['repo_file']
d, h = show(REPO, DEV, P), show(REPO, HEAD, P); rd, rh = show(REPO, DEV, RP), show(REPO, HEAD, RP)
print('INFO blobs: users.ts develop %s head %s | userRepo.ts develop %s head %s' % (blob(REPO, DEV, P)[:12], blob(REPO, HEAD, P)[:12], blob(REPO, DEV, RP)[:12], blob(REPO, HEAD, RP)[:12]))
if '--selftest' in A:
    st = {'ok': 0, 'n': 0}; HA = H['added_code_line']; G = H['guard_line_kept']
    first_other = 'userRepo.getUserById(req.user!.userId)'   # the FIRST surviving site at head (every site is the same text)

    def plant(old, new, src=h):
        assert src.count(old) >= 1, 'plant anchor absent: %r' % old[:60]   # an edit with no anchor is a silent no-op (charter §6)
        return src.replace(old, new, 1)
    selftest_arm(st, 'T0 the REAL head (positive control)', lambda C: judge(C, d, h, rd, rh), None)
    selftest_arm(st, 'T1 passwordless 404 -> 400 (Q-1005 broken)', lambda C: judge(C, d, plant(G, G.replace("NotFoundError('User')", "BadRequestError('No password set')")), rd, rh), 'H3')
    selftest_arm(st, 'T2 a second getUserById site switched', lambda C: judge(C, d, plant(first_other, 'userRepo.getUserByIdWithPasswordHash(req.user!.userId)'), rd, rh), 'H4')
    selftest_arm(st, 'T3 the loader kept (comments only)', lambda C: judge(C, d, plant(HA, H['removed_code_line']), rd, rh), 'H1')
    selftest_arm(st, 'T4 KS-1005 stripped from the comments', lambda C: judge(C, d, '\n'.join(l.replace('KS-1005', 'the fix') if is_comment(l) else l for l in h.split('\n')), rd, rh), 'H1')
    selftest_arm(st, 'T5 user.passwordHash cleared before verify', lambda C: judge(C, d, plant(G, G + '\n    user.passwordHash = undefined as any;'), rd, rh), 'H2')
    selftest_arm(st, 'T6 USER_COLS widened with password_hash', lambda C: judge(C, d, h, rd, plant("const USER_COLS = 'id, ", "const USER_COLS = 'id, password_hash, ", rh)), 'H5')
    print('SELFTEST %s %d of %d' % ('OK' if st['ok'] == st['n'] else 'BROKEN', st['ok'], st['n'])); raise SystemExit(0 if st['ok'] == st['n'] else 1)
C = Checks(); judge(C, d, h, rd, rh)
print('INFO H6 class census — every non-test `.passwordHash` READ in services/auth/src at head (the gate reads each loader; `hunt the class`):')
rc_g, out_g, _ = git(REPO, 'grep', '-n', '-F', '.passwordHash', HEAD, '--', 'Blockchain/Dev/services/auth/src', check=False)
rows = [l for l in out_g.splitlines() if '__tests__' not in l and not re.search(r':\d+:\s*(//|\*)', l) and re.search(r'[A-Za-z_\]\)]\.passwordHash\b', l)]
for l in rows:
    print('INFO H6   %s' % l.split(':', 1)[1][:170])
print('INFO H6 class census: %d reader line(s) (git grep rc %d); MUST-HIT control: the change-password verify line is among them: %s' % (
    len(rows), rc_g, any('verifyPassword(data.currentPassword, user.passwordHash)' in l for l in rows)))
n = C.nfail()
print('C2 HUNK %s: %d FAIL of %d checks | head %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), HEAD[:12]))
raise SystemExit(1 if n else 0)
