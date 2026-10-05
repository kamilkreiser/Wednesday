#!/usr/bin/env python3
"""c2_product_gate66.py — C2 PRODUCT for #1385 (KS-938, T1). READ verbs only. Judges the product hunks by TEXT; the behaviour is C3's.

  W1  hunks exactly: d784..head on mfa.ts removes EXACTLY 4 lines (`mfaSecret: undefined,` x2, `mfaBackupCodes: undefined,` x2) and
      adds EXACTLY 4 non-comment lines (`mfaSecret: null,` x2, `mfaBackupCodes: null,` x2); on users.ts removes EXACTLY
      `mfaSecret: undefined,` and adds EXACTLY `mfaSecret: null,` + `mfaBackupCodes: null,` (every other added line is a `//` comment)
  W2  per site (S1 setup-verify revert, S2 POST /api/auth/mfa/disable, S3 POST /api/users/me/mfa/disable), located BY ANCHOR then the
      first `updateUser(`/`updateUserOrThrow(` object after it: the object carries `mfaEnabled: false` AND `mfaSecret: null` AND
      `mfaBackupCodes: null`; at the base the same object carries `undefined` (S1, S2) / `undefined` + NO backup-codes key (S3)
  W3  CROSS-ROUTE CONSISTENCY over every non-test .ts under services/auth/src at the head: every object literal passed to
      updateUser( / updateUserOrThrow( that contains `mfaEnabled: false` nulls BOTH columns (creation defaults are not clears) (count printed; must be >= 3); 0 `mfa(Secret|BackupCodes): undefined` anywhere (base count
      printed as the control: it must be > 0, else the instrument is blind)
  W4  the users.ts site at its MOVED line: the S3 `mfaSecret` line is :1123 at d784 AND at --develop (users.ts blob identical,
      68f402bb56f0, re-read, not inherited); `git diff d784 head -- users.ts` hunk header is `@@ -1120,7 +1120,13 @@`
  W5  updateUser is UNCHANGED (the PR's stated non-change): userRepo.ts blob head == d784 == --develop; the `!== undefined` skip and the
      `typeof val === 'string'` encryption guard are both present at the head (so null bypasses encryption and is bound as SQL NULL)
  INFO W6 ATTACKER VIEW facts, read at the head (the gate rules whether each is a blocker): re-arm path, re-enable paths overwrite the
      backup codes, the disable residue (TOTP only if a seed exists), the login gate's no-seed refusal, a pending seed from
      /me/mfa/enable that no disable clears, the S1 revert's non-throwing write, users.ts storing generated codes without a hash call.
Usage: c2_product_gate66.py --repo <git dir> [--head <sha>] [--develop <sha>]  |  --selftest --scratch-clone <clone>
rc 0 all PASS / rc 1 any FAIL / rc 2 an object unresolvable (BY NAME)."""
import io, contextlib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate66 import K, git, Tally

MFA, USERS, REPO = K['mfa_file'], K['users_file'], K['repo_file']
SRC = 'Blockchain/Dev/services/auth/src/'
CALL = re.compile(r'updateUser(?:OrThrow)?\(')


def resolvable(repo, s): return bool(s) and git(repo, 'rev-parse', '--verify', '--quiet', s + '^{commit}', check=False)[0] == 0


def diff_lines(patch):
    rem = [l[1:].strip() for l in patch.splitlines() if l.startswith('-') and not l.startswith('---')]
    add = [l[1:].strip() for l in patch.splitlines() if l.startswith('+') and not l.startswith('+++')]
    return rem, [a for a in add if a and not a.startswith('//')], [a for a in add if a.startswith('//')]


def obj_after(text, anchor):
    """the `{...}` object literal of the first updateUser(/updateUserOrThrow( call after the anchor (brace-matched)."""
    i = text.find(anchor)
    if i < 0 or text.count(anchor) != 1: return None
    m = CALL.search(text, i)
    if not m: return None
    j = text.find('{', m.end()); d = 0
    for k in range(j, len(text)):
        d += {'{': 1, '}': -1}.get(text[k], 0)
        if d == 0: return text[j:k + 1]
    return None


def has(obj, key, val): return bool(re.search(r'(?m)^\s*%s:\s*%s,' % (key, val), obj or ''))


def judge(t, mfa_b, mfa_h, users_b, users_h, users_d, mpatch, upatch, uhdr, srcs_h, srcs_b, repo_blobs, repo_text):
    rem, add, com = diff_lines(mpatch)
    w = sorted(rem) == sorted(['mfaSecret: undefined,'] * 2 + ['mfaBackupCodes: undefined,'] * 2) and sorted(add) == sorted(['mfaSecret: null,'] * 2 + ['mfaBackupCodes: null,'] * 2)
    rem2, add2, com2 = diff_lines(upatch)
    w2 = rem2 == ['mfaSecret: undefined,'] and sorted(add2) == sorted(['mfaSecret: null,', 'mfaBackupCodes: null,'])
    t.check('W1', w and w2, 'mfa.ts removed %s added(code) %s (+%d comment lines) | users.ts removed %s added(code) %s (+%d comment lines)' % (rem, add, len(com), rem2, add2, len(com2)))
    rows = []; ok = True
    for sid, base_t, head_t in (('S1', mfa_b, mfa_h), ('S2', mfa_b, mfa_h), ('S3', users_b, users_h)):
        a = K['sites'][sid]['anchor']; ob, oh = obj_after(base_t, a), obj_after(head_t, a)
        hok = oh is not None and has(oh, 'mfaEnabled', 'false') and has(oh, 'mfaSecret', 'null') and has(oh, 'mfaBackupCodes', 'null')
        if sid == 'S3':
            bok = ob is not None and has(ob, 'mfaSecret', 'undefined') and 'mfaBackupCodes' not in ob
        else:
            bok = ob is not None and has(ob, 'mfaSecret', 'undefined') and has(ob, 'mfaBackupCodes', 'undefined')
        ok &= hok and bok; rows.append('%s head nulls both %s / base shape %s' % (sid, hok, bok))
    t.check('W2', ok, ' | '.join(rows))
    objs = []
    for path, txt in srcs_h.items():
        for m in CALL.finditer(txt):   # ONLY objects passed to updateUser( / updateUserOrThrow( — creation defaults are not clears
            j = txt.find('{', m.end()); o = None; d = 0
            if j < 0 or txt[m.end():j].strip(' \n').rstrip(',').count(',') > 1: continue
            for k in range(j, len(txt)):
                d += {'{': 1, '}': -1}.get(txt[k], 0)
                if d == 0: o = txt[j:k + 1]; break
            if o and has(o, 'mfaEnabled', 'false'):
                objs.append((path.rsplit('/', 1)[-1] + ':%d' % (txt.count('\n', 0, m.start()) + 1), has(o, 'mfaSecret', 'null') and has(o, 'mfaBackupCodes', 'null')))
    und_h = sum(len(re.findall(r'mfa(?:Secret|BackupCodes):\s*undefined', x)) for x in srcs_h.values())
    und_b = sum(len(re.findall(r'mfa(?:Secret|BackupCodes):\s*undefined', x)) for x in srcs_b.values())
    t.check('W3', len(objs) >= 3 and all(v for _, v in objs) and und_h == 0 and und_b > 0, '`mfaEnabled: false` objects at head %d, nulling both %s | `mfa*: undefined` head %d (want 0), base CONTROL %d (want > 0)' % (
        len(objs), objs, und_h, und_b))
    lines = lambda txt: [i + 1 for i, l in enumerate(txt.split('\n')) if l.strip() == 'mfaSecret: undefined,']
    t.check('W4', lines(users_b) == [1123] and lines(users_d) == [1123] and uhdr == ['@@ -1120,7 +1120,13 @@'], 'users.ts `mfaSecret: undefined,` at d784 %s, at develop %s (want [1123] both) | hunk headers %s' % (lines(users_b), lines(users_d), uhdr))
    skip = "if (tsField in updates && updates[tsField as keyof User] !== undefined) {" in repo_text
    enc = "if (encryptedCols[tsField] && typeof val === 'string' && val !== '') {" in repo_text
    t.check('W5', len(set(repo_blobs)) == 1 and skip and enc, 'userRepo.ts blobs head/d784/develop %s (one value: %s) | undefined-skip present %s | string-only encryption guard %s' % (
        [b[:12] for b in repo_blobs], len(set(repo_blobs)) == 1, skip, enc))


def attacker(t, users_h, mfa_h, gate_h):
    f = {
        'users.ts /me/mfa/verify refuses with no seed (re-arm needs a seed; after a disable there is none)': "if (!user.mfaSecret) throw new BadRequestError('MFA setup not initiated" in users_h,
        're-enable via users.ts /me/mfa/verify OVERWRITES mfaBackupCodes': bool(re.search(r"mfaEnabled: true,\s*\n\s*verificationLevel: 'STANDARD',\s*\n\s*mfaBackupCodes: backupCodes,", users_h)),
        're-enable via mfa.ts /setup/verify OVERWRITES both (pending.secret, hashedBackupCodes)': 'mfaSecret: pending.secret,\n      mfaBackupCodes: hashedBackupCodes,' in mfa_h,
        'RESIDUE users.ts disable verifies TOTP only `if (user.mfaSecret && ...)`': 'if (user.mfaSecret && !verifyTOTP(user.mfaSecret, code)) {' in users_h,
        'login gate refuses mfaEnabled with no seed (no bypass by a nulled seed)': 'if (!user.mfaSecret) {' in gate_h and "return { ok: false, reason: 'refused' };" in gate_h,
        'users.ts /me/mfa/enable writes a PENDING seed while mfaEnabled stays false (no disable clears it: disable refuses when !mfaEnabled)': "{ mfaSecret: secret } as any, 'MFA setup'" in users_h,
        'S1 revert uses NON-throwing updateUser (a failed revert leaves the row enabled WITH its seed; logged, not thrown)': 'const reverted = await userRepo.updateUser(userId, {' in mfa_h,
        'users.ts /me/mfa/verify stores generated backup codes with NO hash call in the handler (pre-existing; not KS-938)': ('hashBackupCode' not in users_h[users_h.find("userRoutes.post('/me/mfa/verify'"):users_h.find("userRoutes.post('/me/mfa/disable'")]),
    }
    for k, v in f.items(): t.info('W6', '%s: %s' % (k, v))


def collect(repo, head, develop):
    b = K['base']; g = lambda r, p: git(repo, 'show', '%s:%s' % (r, p))
    files = [p for p in git(repo, 'ls-tree', '-r', '--name-only', head, '--', SRC).splitlines() if p.endswith('.ts') and '__tests__' not in p]
    filesb = [p for p in git(repo, 'ls-tree', '-r', '--name-only', b, '--', SRC).splitlines() if p.endswith('.ts') and '__tests__' not in p]
    srcs_h = {p: g(head, p) for p in files}; srcs_b = {p: g(b, p) for p in filesb}
    up = git(repo, 'diff', b, head, '--', USERS)
    return dict(mfa_b=g(b, MFA), mfa_h=g(head, MFA), users_b=g(b, USERS), users_h=g(head, USERS), users_d=g(develop, USERS),
                mpatch=git(repo, 'diff', '-U0', b, head, '--', MFA), upatch=git(repo, 'diff', '-U0', b, head, '--', USERS),
                uhdr=[l.split(' @@')[0] + ' @@' for l in up.splitlines() if l.startswith('@@')], srcs_h=srcs_h, srcs_b=srcs_b,
                repo_blobs=[git(repo, 'rev-parse', '%s:%s' % (r, REPO)).strip() for r in (head, b, develop)], repo_text=g(head, REPO)), g(head, SRC + 'services/passwordLoginGate.ts')


def main(repo, head, develop):
    for n, s in (('head', head), ('develop', develop), ('base', K['base'])):
        if not resolvable(repo, s): print('REFUSED: %s unresolvable: %r is not a commit in %s' % (n, s, repo)); return 2
    d, gate = collect(repo, head, develop); t = Tally(); judge(t, **d); attacker(t, d['users_h'], d['mfa_h'], gate); return t.end()


def selftest(clone):
    ok = total = 0
    def rep(c, m):
        nonlocal ok, total
        total += 1; ok += bool(c); print('SELFTEST %s %s' % ('OK' if c else 'MISS', m))
    real, gate = collect(clone, K['head'], K['develop_at_draft'])
    def run(d):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): judge(t, **d)
        return t
    t0 = run(real); rep(not t0.fails and t0.n == 5, 'positive control (real blobs): %d checked, fails %s' % (t0.n, t0.fails))
    def sub(s, a, b, n=1):
        assert s.count(a) >= n, 'anchor %r found %d' % (a[:50], s.count(a)); return s.replace(a, b, n)
    T = K['tampers']
    arms = []
    for tid in ('T1', 'T3', 'T5', 'T6'):
        tm = T[tid]; key = 'mfa_h' if tm['file'] == MFA else 'users_h'
        assert real[key].count(tm['from']) == 1, '%s anchor not unique' % tid
        arms.append(('tamper %s (%s) in the head text' % (tid, tm['what']), key, lambda s, tm=tm: s.replace(tm['from'], tm['to']), ['W2']))
    arms.append(('a 4th `mfaEnabled: false` object elsewhere that keeps the seed', 'srcs_h', None, ['W3']))
    arms.append(('users.ts at develop moved the site (+1 line above)', 'users_d', lambda s: sub(s, "/** POST /api/users/me/mfa/disable */", "/** POST /api/users/me/mfa/disable */\n// moved"), ['W4']))
    arms.append(('updateUser undefined-skip edited at the head', 'repo_text', lambda s: sub(s, 'updates[tsField as keyof User] !== undefined', 'updates[tsField as keyof User] != null'), ['W5']))
    arms.append(('the base CONTROL blinded (no `undefined` anywhere at base)', 'srcs_b', None, ['W3']))
    for name, key, fn, want in arms:
        d = dict(real)
        if key == 'srcs_h':
            d['srcs_h'] = dict(real['srcs_h']); d['srcs_h']['SIM.ts'] = "await userRepo.updateUserOrThrow(id, {\n  mfaEnabled: false,\n  mfaSecret: null,\n}, 'SIM');"
        elif key == 'srcs_b':
            d['srcs_b'] = {p: re.sub(r'mfa(Secret|BackupCodes):\s*undefined', r'mfa\1: null', v) for p, v in real['srcs_b'].items()}
        else:
            d[key] = fn(d[key]); assert d[key] != real[key], 'tamper did not land: ' + name
        t = run(d); new = set(t.fails) - set(t0.fails); rep(set(want) <= new, '%s: want NEW FAIL %s | got %s' % (name, want, sorted(new)))
    print('SELFTEST %s %d of %d' % ('OK' if ok == total else 'BROKEN', ok, total)); print('CHECKED %d arm(s)' % total)
    return 0 if ok == total else 1


if __name__ == '__main__':
    A = sys.argv[1:]
    if '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    if '--selftest' in A:
        c = opt('--scratch-clone')
        if not c: print('--selftest needs --scratch-clone'); raise SystemExit(2)
        raise SystemExit(selftest(c))
    raise SystemExit(main(opt('--repo', K['checkout']), opt('--head', K['head']), opt('--develop', K['develop_at_draft'])))
