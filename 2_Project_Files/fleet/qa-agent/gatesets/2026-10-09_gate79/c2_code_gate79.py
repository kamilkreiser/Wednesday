#!/usr/bin/env python3
"""c2_code_gate79.py — the COMMIT'S CODE CLAIMS, read against the diff, for #1437 (KS-1402). Read verbs only (git show / diff / grep
into YOUR clone). NEW in gate79 (gate78 had no source change). Every census is taken on CODE-ONLY text (lib code_only: comments
blanked, strings and templates kept) BESIDE the raw-text count, because #1437's comments quote the very strings being counted
("/api/users/lookup", "$queryRawUnsafe") — a raw grep counts the prose. Every zero sits beside a control that fires.

  claims --repo R --head H --base B [--json-out F]
    D0 OUTSIDE-HANDLER: documents.ts code-only, OUTSIDE the transfer-custody handler, base vs head: the only added / removed
       lines are kit expected_outside_handler_adds / _dels (the zod import, the lookupHash import widening, HOLDER_EMAIL_SCHEMA).
       Any other code line moved outside the handler = "no other route's behaviour changes" DOES NOT HOLD (attack e).
    D1 PURE-MOVE (Q-HOIST): inside the handler, code-only, the three hoisted statements occur exactly once at base and at head;
       with the resolution block AND the three statements removed, base and head handler code are IDENTICAL line for line.
    D2 ORDER: at the head, act gate < format check < lookupHash < the email $queryRaw < getDocument (first occurrence after the
       previous), and the act gate's 403 return immediately follows the act-gate condition.
    D3 SQL-SAFETY: in the resolution block (code-only): $queryRawUnsafe / $executeRawUnsafe / Prisma.raw / Prisma.join / string
       `+` concatenation into the query = 0; the query is a TAGGED template (`$queryRaw` + backtick); its ${...} interpolations
       are EXACTLY [holderEmailHash, tenantId]; whole originate src code-only *Unsafe call COUNT base == head (no new unsafe
       call anywhere) beside the CONTROL count of tagged `$queryRaw\\`` > 0. The id path's query carries the SAME tenant predicate
       text (parity with the id path, attack b, textual).
    D4 RETIRED-SUBJECTS (attack f, static half): in originate src CODE-ONLY: `users/lookup` inside a fetch, `lookupRes`,
       `RECIPIENT_LOOKUP_FAILED`, the caller-Authorization forward, the 401/403 hint strings, 'Recipient lookup service
       unavailable' — base > 0 (CONTROL: the instrument sees them) and head == 0. RAW counts printed beside (comments).
    D5 PARITY WITH AUTH (attacks b, d): auth users.ts lookupQuerySchema email chain == originate HOLDER_EMAIL_SCHEMA == kit; auth
       userRepo getUserByEmail normalisation `toLowerCase().trim()` present at base AND head; originate normalises the RAW body
       value with `.toLowerCase().trim()`; auth's 404 compare `(callerTenantId && user.tenantId && ...)` quoted (the NULL-tenant
       tolerance AND the skip-when-caller-tenantless hole).
    D6 BYTES: the VALIDATION_ERROR and RECIPIENT_NOT_FOUND message strings are byte-identical base vs head (the response-body claim).
    D7 TENANTLESS CALLER (attack a, static half): getReqTenantId's body at the head (does it EVER return null / undefined, or fall
       back to DEFAULT_TENANT_ID?) and DEFAULT_TENANT_ID's value, printed; whether `${tenantId}::uuid` can bind NULL is then a
       reading, and what Prisma binds for undefined is the c3 `probe` cell's job.
    D8 Q-LEGACY (read at BASE): auth getUserByEmail's legacy fallback (`auth_find_user_by_email_legacy`) and that /lookup calls
       getUserByEmail; the legacy function's definition in the migrations (which rows it returns), printed with file:line.
       POPULATION: UNMEASURED (no database) — the kit says so, it never guesses.
    D9 RLS / GUC (attack j): where originate sets req.db (tenantGucContext) and every migration line that ENABLES / FORCES RLS or
       creates a POLICY on `users`, printed with file:line; the commit's "tenant RLS has been inert (KS-160)" and the id path's
       "users is FORCE RLS fail-closed" are both QUOTED for the gate to reconcile. READ, never assumed.
    D10 KS739-CELLS: it(/it.each( titles of the ks739 file at base vs head (counts; retired / kept / new), for the per-cell
       unreachability ruling.
    D11 PATCH-SHA: the commit body's "patch sha256/16 ab8e9e441864e05c" re-derived by four named instruments; a miss is
       UNREPRODUCED (the instrument is unnamed), never a defect by itself.
  --selftest   planted arms: a comment-only string is not code; a template `${}` with braces; a planted extra outside-handler line;
               a planted change to a non-block handler line; a planted $queryRawUnsafe; a planted `+` concatenation; a planted
               third interpolation; a planted order swap; a planted changed message byte.
rc 0 every D-check PASS (INFO lines are readings for the gate) / 1 a FAIL / 2 refused."""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate79 import K, Tally, git, show, req, opt, code_only, handler, block, norm_lines, sha256_16, resolvable

RF = K['route_file']; OD = K['originate_dir'] + '/src'
AUTH_USERS = K['auth_prefix'] + 'src/routes/users.ts'; AUTH_REPO = K['auth_prefix'] + 'src/repositories/userRepo.ts'


def split_handler(src):
    hs, he = handler(src); bs, be = block(src, hs, he)
    return hs, he, bs, be


def outside_delta(base_src, head_src):
    """D0: code-only lines outside the handler, as multisets: (added, removed)."""
    def outside(s):
        c = code_only(s); hs, he = handler(s)
        return norm_lines(c[:hs] + c[he:])
    a, b = outside(base_src), outside(head_src)
    from collections import Counter
    ca, cb = Counter(a), Counter(b)
    return sorted((cb - ca).elements()), sorted((ca - cb).elements())


def pure_move(base_src, head_src):
    """D1: handler code-only minus the resolution block minus the hoisted lines; returns (ok, counts, first_diff)."""
    res = {}
    seqs = []
    for tag, s in (('base', base_src), ('head', head_src)):
        c = code_only(s); hs, he, bs, be = split_handler(s)
        lines = norm_lines(c[hs:bs] + '\n' + c[be:he])
        whole = norm_lines(c[hs:he])
        res[tag] = [whole.count(h) for h in K['hoisted_lines']]
        seqs.append([l for l in lines if l not in K['hoisted_lines']])
    a, b = seqs
    first = None
    for i in range(max(len(a), len(b))):
        x = a[i] if i < len(a) else '<END>'; y = b[i] if i < len(b) else '<END>'
        if x != y: first = (i, x, y); break
    ok = first is None and res['base'] == [1, 1, 1] and res['head'] == [1, 1, 1]
    return ok, res, first, (len(a), len(b))


def order(head_src):
    c = code_only(head_src); hs, he = handler(head_src); pos = []; at = hs
    for a in K['order_anchors']:
        i = c.find(a, at, he); pos.append(i); at = i + 1 if i >= 0 else at
    ok = all(p >= 0 for p in pos) and pos == sorted(pos)
    g = c.find(K['order_anchors'][0], hs, he)
    after = c[g:g + 400]
    gate403 = bool(re.match(r"[^\n]*\)\s*\{\s*return res\.status\(403\)", after.replace('\n', ' ')))
    return ok and gate403, pos, gate403


def sql_safety(src):
    c = code_only(src); hs, he, bs, be = split_handler(src); blk = c[bs:be]
    bad = {k: len(re.findall(rx, blk)) for k, rx in (('queryRawUnsafe', r'\$queryRawUnsafe'), ('executeRawUnsafe', r'\$executeRawUnsafe'),
                                                     ('Prisma.raw', r'Prisma\.raw'), ('Prisma.join', r'Prisma\.join'))}
    m = re.search(r'\$queryRaw`', blk)
    if not m:
        return False, bad, None, 'no tagged $queryRaw in the block'
    j = blk.find('`', m.end())
    tpl = blk[m.end():j]
    interp = re.findall(r'\$\{\s*([^}]*?)\s*\}', tpl)
    tail = blk[j + 1:j + 40]
    concat = bool(re.match(r'\s*\+', tail)) or bool(re.search(r'\+\s*$', blk[:m.start()].rstrip()[-5:]))
    ok = not any(bad.values()) and interp == ['holderEmailHash', 'tenantId'] and not concat
    return ok, bad, interp, 'concatenation %s | template text %r' % (concat, re.sub(r'\s+', ' ', tpl).strip())


def census(repo, rev, path_prefix, rx_list):
    """{name: (code_only_count, raw_count)} over every .ts under path_prefix excluding __tests__."""
    files = [f for f in git(repo, 'ls-tree', '-r', '--name-only', rev, '--', path_prefix).split('\n')
             if f.endswith('.ts') and '/__tests__/' not in f]
    out = dict((n, [0, 0]) for n, _ in rx_list)
    for f in files:
        raw = show(repo, rev, f); co = code_only(raw)
        for n, rx in rx_list:
            out[n][0] += len(re.findall(rx, co)); out[n][1] += len(re.findall(rx, raw))
    return out, len(files)


RETIRED = [('fetch users/lookup', r'fetch\(\s*[^)]{0,200}users/lookup'), ('lookupRes', r'\blookupRes\b'),
           ('RECIPIENT_LOOKUP_FAILED', r'RECIPIENT_LOOKUP_FAILED'), ('caller Authorization forward', r'Authorization:\s*authHeader'),
           ('401 re-authenticate hint', r'Re-authenticate and retry'), ('403 users:read hint', r'Grant it the `users:read` scope'),
           ('Recipient lookup service unavailable', r'Recipient lookup service unavailable'),
           ('lookup 502 via users/lookup', r'Could not resolve recipient email via users/lookup')]
UNSAFE = [('$queryRawUnsafe(', r'\$queryRawUnsafe\s*\('), ('$executeRawUnsafe(', r'\$executeRawUnsafe\s*\('),
          ('CONTROL tagged $queryRaw`', r'\$queryRaw`')]


def chain_of(src, anchor_rx):
    m = re.search(anchor_rx, code_only(src))
    return re.sub(r'\s+', '', m.group(1)) if m else None


def strings_of(src, s):
    return code_only(src).count("'%s'" % s)


def lines_with(repo, rev, paths, rx, ctx=0, limit=40):
    out = []
    for p in paths:
        txt = show(repo, rev, p)
        if not txt: out.append('  %s ABSENT at %s' % (p, rev[:12])); continue
        L = txt.split('\n')
        for i, l in enumerate(L):
            if re.search(rx, l):
                for k in range(max(0, i - ctx), min(len(L), i + ctx + 1)):
                    out.append('  %s:%d %s' % (p, k + 1, L[k].rstrip()[:200]))
                if len(out) >= limit: return out
    return out


def claims(repo, head, base, json_out):
    t = Tally(); J = {}
    for s, n in ((head, 'head'), (base, 'base')):
        if not resolvable(repo, s): print('REFUSED: %s %s not in %s' % (n, s, repo)); return 2
    hb, bb = show(repo, head, RF), show(repo, base, RF)
    print('documents.ts base %s sha256/16 %s | head %s sha256/16 %s' % (base[:12], sha256_16(bb), head[:12], sha256_16(hb)))
    add, rem = outside_delta(bb, hb)
    J['D0'] = {'added': add, 'removed': rem}
    t.check('D0', sorted(add) == sorted(K['expected_outside_handler_adds']) and sorted(rem) == sorted(K['expected_outside_handler_dels']),
            'OUTSIDE the handler (code-only): +%d %s | -%d %s (want exactly kit adds %d / dels %d)' % (len(add), add, len(rem), rem,
            len(K['expected_outside_handler_adds']), len(K['expected_outside_handler_dels'])))
    ok, cnt, first, lens = pure_move(bb, hb)
    J['D1'] = {'hoisted_counts': cnt, 'first_diff': first, 'lens': lens}
    t.check('D1', ok, 'PURE-MOVE: hoisted statements once each base %s head %s | handler minus block minus hoist: %d vs %d lines, first difference %s'
            % (cnt['base'], cnt['head'], lens[0], lens[1], first or 'NONE'))
    ok, pos, g403 = order(hb)
    J['D2'] = {'positions': pos, 'gate403': g403}
    t.check('D2', ok, 'ORDER at the head (char offsets) %s for %s | act gate returns 403 next: %s' % (pos, [a[:28] for a in K['order_anchors']], g403))
    ok, bad, interp, note = sql_safety(hb)
    J['D3'] = {'bad': bad, 'interp': interp}
    t.check('D3a', ok, 'SQL-SAFETY in the block: unsafe/raw/join %s | interpolations %s (want [holderEmailHash, tenantId]) | %s' % (bad, interp, note))
    cb_, nb = census(repo, base, OD, UNSAFE); ch_, nh = census(repo, head, OD, UNSAFE)
    J['D3']['census'] = {'base': cb_, 'head': ch_}
    t.check('D3b', all(cb_[n][0] == ch_[n][0] for n, _ in UNSAFE[:2]) and ch_[UNSAFE[2][0]][0] > 0,
            'originate src (%d / %d .ts, tests excluded) code-only [raw] base -> head: %s' % (nb, nh,
            '; '.join('%s %d[%d] -> %d[%d]' % (n, cb_[n][0], cb_[n][1], ch_[n][0], ch_[n][1]) for n, _ in UNSAFE)))
    hs, he = handler(hb); tp = 'AND (tenant_id IS NULL OR tenant_id = ${tenantId}::uuid)'
    n_tp = code_only(hb)[hs:he].count(tp)
    t.check('D3c', n_tp == 2, 'tenant predicate text in the handler (code-only): %d (want 2: the email read AND the id path\'s existence read — textual parity, attack b)' % n_tp)
    def in_handler(src):
        c = code_only(src); hs_, he_ = handler(src); return c[hs_:he_], src[hs_:he_]
    (cbh, rbh), (chh, rhh) = in_handler(bb), in_handler(hb)
    rb, _ = census(repo, base, OD, RETIRED); rh, _ = census(repo, head, OD, RETIRED)
    J['D4'] = {'base_src': rb, 'head_src': rh}
    for n, rx_ in RETIRED:
        b_, h_ = len(re.findall(rx_, cbh)), len(re.findall(rx_, chh))
        t.check('D4', b_ > 0 and h_ == 0, 'RETIRED-SUBJECT %-38s IN THE HANDLER code-only base %d -> head %d (raw %d -> %d; CONTROL: base > 0) | '
                'whole originate src code-only %d -> %d' % (n, b_, h_, len(re.findall(rx_, rbh)), len(re.findall(rx_, rhh)), rb[n][0], rh[n][0]))
        if rh[n][0]:
            print('INFO D4-CLASS %r survives ELSEWHERE in originate src at the head (%d): the KS-1402 CLASS (a caller credential forwarded '
                  'to auth for user resolution) — hunt it, report it; not this PR\'s diff' % (n, rh[n][0]))
    for l in lines_with(repo, head, [OD + '/routes/certifications.ts'], r'/api/users/stub|Authorization: authHeader'):
        print('INFO D4-CLASS certifications.ts at the HEAD: %s' % l.strip())
    au_h, au_b = show(repo, head, AUTH_USERS), show(repo, base, AUTH_USERS)
    rx = r'lookupQuerySchema\s*=\s*z\.object\(\{\s*email:\s*([^\n,]+(?:\([^)]*\))*[^\n,]*),'
    ch_auth_b, ch_auth_h = chain_of(au_b, rx), chain_of(au_h, rx)
    ch_or = chain_of(hb, r'HOLDER_EMAIL_SCHEMA\s*=\s*([^;]+);')
    want = re.sub(r'\s+', '', K['holder_email_schema'])
    J['D5'] = {'auth_base': ch_auth_b, 'auth_head': ch_auth_h, 'originate': ch_or}
    t.check('D5a', ch_auth_b == ch_auth_h == ch_or == want, 'SCHEMA auth base %s | auth head %s | originate %s | kit %s' % (ch_auth_b, ch_auth_h, ch_or, want))
    ar_b, ar_h = show(repo, base, AUTH_REPO), show(repo, head, AUTH_REPO)
    gn = lambda s: re.search(r'export async function getUserByEmail[\s\S]{0,400}?toLowerCase\(\)\.trim\(\)', code_only(s)) is not None
    orn = 'const normalisedHolderEmail = String(newHolderEmail).toLowerCase().trim();' in code_only(hb)
    t.check('D5b', gn(ar_b) and gn(ar_h) and orn, 'NORMALISATION auth getUserByEmail toLowerCase().trim() base %s head %s | originate String(raw).toLowerCase().trim() %s' % (gn(ar_b), gn(ar_h), orn))
    for l in lines_with(repo, base, [AUTH_USERS], r'callerTenantId && user\.tenantId'):
        print('INFO D5c auth /lookup tenant compare at BASE (NULL-tenant tolerance AND skip-when-caller-tenantless): %s' % l.strip())
    for k, s in (('validation', K['messages']['validation']), ('not_found', K['messages']['not_found'])):
        nb_, nh_ = strings_of(bb, s), strings_of(hb, s)
        t.check('D6', nb_ >= 1 and nh_ >= 1, 'BYTES %s message %r: base %d occurrence(s) -> head %d' % (k, s[:50], nb_, nh_))
    print('INFO D6 key-absent 502 message at the head: %d occurrence(s) of %r' % (strings_of(hb, K['messages']['key_absent_502']), K['messages']['key_absent_502']))
    for l in lines_with(repo, head, [RF], r'^const DEFAULT_TENANT_ID|^function getReqTenantId|return tid \|\| DEFAULT_TENANT_ID|const tid = \(req as any\)\.tenantId'):
        print('INFO D7 tenantless-caller reading at the HEAD: %s' % l.strip())
    for l in lines_with(repo, head, [OD + '/index.ts'], r'MULTI_TENANCY_ENABLED|extractTenantContext\(|tenantGucContext'):
        print('INFO D7 originate index.ts tenant mount at the HEAD: %s' % l.strip())
    for l in lines_with(repo, base, [AUTH_USERS], r'getUserByEmail\(') + lines_with(repo, base, [AUTH_REPO], r'auth_find_user_by_email_legacy|email_lookup_hash = \$1|normalised = '):
        print('INFO D8 Q-LEGACY at BASE: %s' % l.strip())
    rc_, mig = git(repo, 'grep', '-n', '-E', 'FUNCTION[[:space:]]+(public\\.)?auth_find_user_by_email_legacy', base, '--', 'Blockchain/Dev', check=False)[:2]
    for l in (mig.strip().split('\n') if mig.strip() else ['(no definition found by the kit\'s grep: the gate finds it, or says so)'])[:6]:
        print('INFO D8 legacy function definition: %s' % l[:220])
    print('INFO D8 POPULATION (plaintext-email users with NO email_lookup_hash that auth resolved at base): UNMEASURED — no database in this kit')
    rc_, rls = git(repo, 'grep', '-n', '-i', '-E', 'users_auth_lookup|Backfills users\\.tenant_id|NULL rows are invisible|FORCE ROW LEVEL SECURITY|fail-closed tenant_isolation|An unset context now yields ZERO rows', head, '--', 'Blockchain/Dev/migrations', check=False)[:2]
    rl = [l for l in rls.strip().split('\n') if l.strip()]
    print('INFO D9 RLS readings in migrations at the HEAD: %d line(s) (CONTROL: 0 means the grep is blind, not that RLS is absent)' % len(rl))
    for l in rl[:16]:
        print('INFO D9 RLS: %s' % l[:220])
    rc_, k160 = git(repo, 'grep', '-n', '-c', 'KS-160', head, '--', 'Blockchain/Dev', check=False)[:2]
    print('INFO D9 files naming KS-160 at the HEAD: %d (read them: is tenant RLS on `users` INERT, or FORCE fail-closed under the request GUC?)' % len([l for l in k160.split('\n') if l.strip()]))
    for l in lines_with(repo, head, [RF], r'inert before now|FORCE RLS fail-closed|tenant GUC'):
        print('INFO D9 the claims to reconcile (documents.ts at the HEAD): %s' % l.strip())
    tit = {}
    for tag, rev in (('base', base), ('head', head)):
        src = code_only(show(repo, rev, K['test_files']['ks739']))
        tit[tag] = re.findall(r'''\bit(?:\.each\([\s\S]*?\))?\(\s*(['"`])(.*?)\1''', src)
        tit[tag] = [x[1] for x in tit[tag]]
    kept = [x for x in tit['base'] if x in tit['head']]
    J['D10'] = tit
    print('INFO D10 ks739 it()/it.each titles: base %d, head %d, kept verbatim %d, base-only %d, head-only %d (the READY: 20 definitions -> 17 RETIRED + 3 RE-POINTED + 13 guard rows)'
          % (len(tit['base']), len(tit['head']), len(kept), len(tit['base']) - len(kept), len(tit['head']) - len(kept)))
    for x in tit['head']: print('INFO D10 head title: %s' % x[:150])
    ins = {}
    for name, args in (('git diff base head', ['diff', base, head]), ('git diff base head -- (non-doc)', ['diff', base, head, '--', '.', ':!Projects Documents']),
                       ('git show head (format=)', ['show', '--format=', head]), ('git diff --binary base head', ['diff', '--binary', base, head])):
        ins[name] = sha256_16(subprocess.run(['git', '-C', repo] + args, capture_output=True).stdout)
    hit = [n for n, v in ins.items() if v == K['ready_claims']['patch_sha256_16']]
    print('INFO D11 PATCH-SHA claimed %s | %s | %s' % (K['ready_claims']['patch_sha256_16'], ins, ('REPRODUCED by ' + hit[0]) if hit else 'UNREPRODUCED by these 4 instruments (instrument unnamed in the commit)'))
    if json_out: json.dump(J, open(json_out, 'w'), indent=1, default=str)
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    rep(code_only("a // users/lookup\nb").count('users/lookup') == 0, 'code_only: a // comment is blanked')
    rep(code_only("x = '// not a comment'").count('// not a comment') == 1, 'code_only: // inside a string is CODE')
    rep(code_only("q = `a ${ {x:1}.x } // still template`; // gone").count('still template') == 1 and 'gone' not in code_only("q = `a ${ {x:1}.x } // still template`; // gone"),
        'code_only: a template with braces in ${} keeps its // text; the trailing comment is blanked')
    rep(code_only("/* $queryRawUnsafe */ y").count('queryRawUnsafe') == 0 and code_only("a\n/*\nb\n*/c").count('\n') == 3, 'code_only: block comment blanked, newlines kept')
    hb = '\n'.join(['import x;', 'documentsRouter.post(', "  '/:id/transfer-custody',", '  async () => {',
                    '      const tenantId = getReqTenantId(req);', "      const { prisma: defaultPrisma, withTenant } = await import('../db');",
                    '      const db = (req as any).db || defaultPrisma;', '      let resolvedHolderId = newHolderId;',
                    '      const r = await db.$queryRaw`SELECT id FROM users WHERE email_lookup_hash = ${holderEmailHash} AND (tenant_id IS NULL OR tenant_id = ${tenantId}::uuid)`;',
                    '      if (!resolvedHolderId) {', '      keep();', '  });', 'documentsRouter.get(', '  );'])
    bb = '\n'.join(['import x;', 'documentsRouter.post(', "  '/:id/transfer-custody',", '  async () => {', '      let resolvedHolderId = newHolderId;',
                    '      old();', '      if (!resolvedHolderId) {', '      const tenantId = getReqTenantId(req);',
                    "      const { prisma: defaultPrisma, withTenant } = await import('../db');", '      const db = (req as any).db || defaultPrisma;',
                    '      keep();', '  });', 'documentsRouter.get(', '  );'])
    ok, cnt, first, _ = pure_move(bb, hb); rep(ok, 'pure_move: a moved hoist + a replaced block passes %s' % (first,))
    ok, _, first, _ = pure_move(bb, hb.replace('keep();', 'keep(1);')); rep(not ok, 'PLANTED change to a NON-block handler line FAILS D1: %s' % (first,))
    ok, _, _, _ = pure_move(bb, hb.replace('getReqTenantId(req);', 'getReqTenantId(req) ?? null;')); rep(not ok, 'PLANTED changed hoist expression FAILS D1')
    a, r = outside_delta(bb, hb); rep(not a and not r, 'outside_delta: nothing outside the handler changed')
    a, r = outside_delta(bb, hb.replace('import x;', 'import x;\nimport y;')); rep(a == ['import y;'], 'PLANTED extra outside-handler line is SEEN by D0')
    ok, bad, interp, _ = sql_safety(hb); rep(ok and interp == ['holderEmailHash', 'tenantId'], 'sql_safety: the bound tagged template passes')
    ok, *_ = sql_safety(hb.replace('db.$queryRaw`', 'db.$queryRawUnsafe(`').replace('::uuid)`;', '::uuid)`);')); rep(not ok, 'PLANTED $queryRawUnsafe FAILS D3a')
    ok, *_ = sql_safety(hb.replace("${tenantId}::uuid)`;", "${tenantId}::uuid)` + extra;")); rep(not ok, 'PLANTED `+` concatenation after the template FAILS D3a')
    ok, *_ = sql_safety(hb.replace('${tenantId}::uuid)', '${tenantId}::uuid) AND x = ${other}')); rep(not ok, 'PLANTED third interpolation FAILS D3a')
    ok, *_ = sql_safety(hb.replace('// x', '').replace("db.$queryRaw`SELECT", "db.$queryRaw`SELECT /* ${'x'} */")); rep(not ok, 'PLANTED interpolation inside an SQL comment is still an interpolation (FAILS)')
    rep(strings_of("a('newHolderEmail is not a valid email address')", K['messages']['validation']) == 1 and
        strings_of("a('newHolderEmail is not a valid email address.')", K['messages']['validation']) == 0, 'BYTES: one changed byte in the message reads 0 (D6 fires)')
    rep(chain_of('const HOLDER_EMAIL_SCHEMA = z.string().trim().email().min(3).max(320);', r'HOLDER_EMAIL_SCHEMA\s*=\s*([^;]+);') == re.sub(r'\s+', '', K['holder_email_schema']), 'schema chain extractor reads the kit chain')
    rep(chain_of('const HOLDER_EMAIL_SCHEMA = z.string().email().min(3).max(320);', r'HOLDER_EMAIL_SCHEMA\s*=\s*([^;]+);') != re.sub(r'\s+', '', K['holder_email_schema']), 'PLANTED schema without .trim() FAILS parity')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if not A: print(__doc__); return 2
    if A[0] == '--selftest': return selftest()
    try:
        if A[0] == 'claims':
            return claims(req(A, '--repo'), req(A, '--head', True), req(A, '--base', True), opt(A, '--json-out'))
    except SystemExit as e:
        print(e); return 2
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
