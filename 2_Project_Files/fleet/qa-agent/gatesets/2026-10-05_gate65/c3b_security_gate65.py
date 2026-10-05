#!/usr/bin/env python3
"""c3b_security_gate65.py — C3b SECURITY READ for #1393: can the new `null` -> 400 mapping (missing doc vs already revoked) ever
turn a 404 / 403 into a 400 that leaks a document's existence across tenants? READ verbs only; reads the revoke route AT THE HEAD
BY LINE and the repository it calls. This is an ORDER instrument, not a runtime one: the gate pairs it with C3 R1 and its own probe.

  S1 ORDER inside the `/:id/revoke` handler (head line numbers printed):
       401 UNAUTHORIZED < the tenant-scoped read getDocument(id, tenantId, …) < EVERY 404 NOT_FOUND < the 403 FORBIDDEN (owner)
       < the read-time 400 < checkOnBehalfOf < the guarded updateDocument(… ifStatusIsNot …) < the guard 400 < recordOnBehalfOf
       < emitLifecycleAnchor < res.json
  S2 the guard 400 is BYTE-IDENTICAL to the read-time 400 (no new information in the body) and the handler has EXACTLY these two
     `status(400)` lines; nothing between the guarded call and its null check writes a response or a record
  S3 the repository: getDocument's lookups are BOTH tenant-scoped (`tenant_id = ${tenantId}::uuid` on the external_id AND the uuid
     SELECT); updateDocument returns null on `!doc` BEFORE the UPDATE, and the UPDATE is scoped `external_id = ${id}` AND
     `tenant_id = ${tenantId}::uuid`
  => a cross-tenant id cannot reach the guard (S1 + S3: the route's own tenant-scoped read 404s first); a 400 from the guard needs a
     document the caller's tenant holds AND the caller owns (403 otherwise). The leak question is then about the SAME tenant only.
  INFO the three ways the inner `null` can differ from "already revoked" (the gate rules each; none is cross-tenant):
     N1 deleted between the route read and the write (KS-1419, the PR's named residual)
     N2 a revoke addressed by the document UUID: both reads fall back to `id = ${id}::uuid`, but the UPDATE matches ONLY
        `external_id = ${id}` -> 0 rows -> guard null -> 400 "already revoked" for a live document (before: 200 + a provenance row + an
        anchor for a write that changed nothing)
     N3 MULTI_TENANCY_ENABLED=true: the route reads with (req as any).db, the guarded write passes db=undefined (default prisma)
Usage: c3b_security_gate65.py --repo <git dir> [--head <sha>]  |  --selftest --repo <git dir>
rc 0 all PASS / rc 1 any FAIL or 0 checked / rc 2 refused."""
import os, re, sys, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate65 import K, git, Tally

MSG = K['msg_400']


def handler(src):
    ln = src.split('\n')
    s = next((i for i, l in enumerate(ln) if "'/:id/revoke'" in l), None)
    if s is None: return None, []
    e = next((i for i in range(s + 1, len(ln)) if ln[i].startswith('documentsRouter.')), len(ln))
    return s, ln[s:e]


def judge_route(t, src):
    s, H = handler(src)
    if s is None:
        t.check('S1', False, 'the /:id/revoke handler not found'); t.check('S2', False, 'no handler'); return
    at = lambda pred: [s + i + 1 for i, l in enumerate(H) if pred(l)]
    L = {'401': at(lambda l: "'UNAUTHORIZED'" in l), 'read': at(lambda l: 'getDocument(id, tenantId' in l),
         '404': at(lambda l: "'NOT_FOUND'" in l), '403': at(lambda l: "'FORBIDDEN'" in l), '400': at(lambda l: l.strip() == MSG),
         'obo': at(lambda l: 'checkOnBehalfOf(req, res)' in l), 'upd': at(lambda l: 'updateDocument(' in l and 'ifStatusIsNot' in l),
         'null': at(lambda l: l.strip() == 'if (revoked === null) {'), 'rec': at(lambda l: "recordOnBehalfOf(req, id, 'revoke'" in l),
         'anc': at(lambda l: 'emitLifecycleAnchor(' in l), 'json': at(lambda l: l.strip() == 'res.json({')}
    one = all(len(L[k]) == 1 for k in ('401', 'read', '403', 'obo', 'upd', 'null', 'rec', 'anc', 'json')) and len(L['404']) >= 1 and len(L['400']) == 2
    if one:
        seq = [L['401'][0], L['read'][0], max(L['404']), L['403'][0], L['400'][0], L['obo'][0], L['upd'][0], L['null'][0], L['400'][1], L['rec'][0], L['anc'][0], L['json'][0]]
        ordered = seq == sorted(seq) and min(L['404']) > L['read'][0]
    else:
        seq, ordered = [], False
    t.check('S1', one and ordered, 'head lines: 401 %s | read %s | 404 %s | 403 %s | 400 %s | obo %s | guarded write %s | null-check %s | record %s | anchor %s | res.json %s | each found once (404 >= 1, 400 == 2) %s | ascending %s' % (
        L['401'], L['read'], L['404'], L['403'], L['400'], L['obo'], L['upd'], L['null'], L['rec'], L['anc'], L['json'], one, ordered))
    s400 = at(lambda l: 'status(400)' in l)
    between = []
    if one:
        between = [x for x in range(L['upd'][0] + 1, L['null'][0]) if src.split('\n')[x - 1].strip()]
    t.check('S2', one and s400 == L['400'] and not between, 'status(400) lines %s == the two exact-message lines %s: %s | non-blank lines between the guarded write and its null check %s' % (
        s400, L['400'], s400 == L['400'], between))
    rd = [x for x in L['read']]
    t.info('N3', 'the route read at %s passes %s; the guarded write passes db=undefined (default prisma)' % (rd, 'req.db' if any('(req as any).db' in src.split('\n')[x - 1] for x in rd) else 'NOT req.db'))


def judge_repo(t, src):
    ln = src.split('\n')
    g0 = next((i for i, l in enumerate(ln) if l.startswith('export async function getDocument(')), None)
    u0 = next((i for i, l in enumerate(ln) if l.startswith('export async function updateDocument(')), None)
    if g0 is None or u0 is None:
        t.check('S3', False, 'getDocument / updateDocument not found'); return
    g = '\n'.join(ln[g0:g0 + 40]); u = ln[u0:u0 + 90]
    gsel = re.findall(r'WHERE (external_id = \$\{id\}|id = \$\{id\}::uuid)\s*\n\s*AND tenant_id = \$\{tenantId\}::uuid', g)
    nd = next((i for i, l in enumerate(u) if l.strip() == 'if (!doc) return null;'), None)
    up = next((i for i, l in enumerate(u) if 'UPDATE documents SET' in l), None)
    wh = '\n'.join(u[up:up + 16]) if up is not None else ''
    scoped = 'WHERE external_id = ${id}' in wh and 'AND tenant_id = ${tenantId}::uuid' in wh
    t.check('S3', len(gsel) == 2 and nd is not None and up is not None and nd < up and scoped,
            'getDocument tenant-scoped SELECTs %d (want 2: external_id and uuid) | updateDocument `if (!doc) return null;` at +%s before the UPDATE at +%s | UPDATE scoped external_id AND tenant_id %s' % (
                len(gsel), nd, up, scoped))
    ext_only = 'WHERE external_id = ${id}' in wh and 'id = ${id}::uuid' not in wh
    t.info('N2', 'the guarded UPDATE matches external_id ONLY (%s) while both reads fall back to the uuid: a uuid-addressed revoke of a live document -> 0 rows -> null -> 400 "already revoked"' % ext_only)
    t.info('N1', 'a row deleted between the route read and the inner read/UPDATE -> null -> 400 (KS 1419, the PR\'s named residual)')


def run_all(t, repo, head, ov=None):
    ov = ov or {}
    judge_route(t, ov.get('route', git(repo, 'show', '%s:%s' % (head, K['route_file']))))
    judge_repo(t, ov.get('repo', git(repo, 'show', '%s:%s' % (head, K['repo_file']))))


def selftest(repo):
    if not repo or git(repo, 'rev-parse', '--verify', '--quiet', K['head'] + '^{commit}', check=False)[0] != 0:
        print('SELFTEST REFUSED: --repo must hold the head %s' % K['head']); return 2
    RT = git(repo, 'show', '%s:%s' % (K['head'], K['route_file'])); RP = git(repo, 'show', '%s:%s' % (K['head'], K['repo_file']))
    s, H = handler(RT); HB = '\n'.join(H)
    def sub(x, a, b):
        assert x.count(a) == 1, 'anchor must occur once (%d): %r' % (x.count(a), a[:70]); return x.replace(a, b)
    def go(ov):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): run_all(t, repo, K['head'], ov)
        return t
    t0 = go({}); ok = int(not t0.fails and t0.n == 3); total = 1
    print('SELFTEST %s T0 positive control (the REAL head route + repo): %d checked, fails %s' % ('OK' if ok else 'MISS', t0.n, t0.fails))
    own = "      if (document.owner?.id !== user.id) {\n        return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Only the owner can revoke this document' } });\n      }\n"
    guard = "      const revoked = await updateDocument(id, tenantId, { status: 'revoked' }, undefined, { ifStatusIsNot: 'revoked' });\n      if (revoked === null) {\n        " + MSG + "\n      }\n"
    rec = "      recordOnBehalfOf(req, id, 'revoke', revokeObo);\n"
    nf = "      if (!document) {\n        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Document not found' } });\n      }\n"
    def hsub(h, a, b):
        if h is HB:
            return RT.replace(HB, sub(HB, a, b))
        _, H2 = handler(h); hb2 = '\n'.join(H2)
        return h.replace(hb2, sub(hb2, a, b))
    arms = [
        ('the guarded write moved ABOVE the owner 403', {'route': sub(sub(RT, guard, ''), own, guard + own)}, ['S1']),
        ('the !document 404 moved BELOW the owner 403 (a 403 for a missing doc)', {'route': hsub(hsub(HB, nf, ''), own, own + nf)}, ['S1']),
        ('a harmless comment line added in the handler (must not over-fire)', {'route': hsub(HB, rec, '      // gate65 selftest: a comment only\n' + rec)}, []),
        ('record moved before the null check', {'route': sub(sub(RT, rec, ''), guard, guard.replace('      if (revoked === null) {', rec.rstrip('\n') + '\n      if (revoked === null) {'))}, ['S1', 'S2']),
        ('a third 400 (a distinct guard message)', {'route': sub(RT, '      if (revoked === null) {\n        ' + MSG, '      if (revoked === null) {\n        ' + MSG.replace('already revoked', 'gone'))}, ['S1', 'S2']),
        ('the anchor emitted before the null check', {'route': sub(RT, guard, "      void emitLifecycleAnchor({ documentId: id, contentHash: '', authHeader: '', eventType: 'revoke' });\n" + guard)}, ['S1']),
        ('getDocument uuid SELECT loses its tenant scope', {'repo': sub(RP, "           WHERE id = ${id}::uuid\n             AND tenant_id = ${tenantId}::uuid\n", "           WHERE id = ${id}::uuid\n")}, ['S3']),
        ('updateDocument UPDATE loses its tenant scope', {'repo': sub(RP, "      WHERE external_id = ${id}\n        AND tenant_id = ${tenantId}::uuid\n        AND (${guardStatus}", "      WHERE external_id = ${id}\n        AND (${guardStatus}")}, ['S3']),
        ('the !doc early return removed', {'repo': sub(RP, '  if (!doc) return null;\n', '')}, ['S3']),
    ]
    # want [] = a non-firing arm: proves the instrument does not over-fire on a harmless edit.
    for name, ov, want in arms:
        t = go(ov); total += 1; new = set(t.fails) - set(t0.fails)
        g = (set(want) <= new) if want else not new; ok += g
        print('SELFTEST %s %s: want NEW FAIL %s | got %s' % ('OK' if g else 'MISS', name, want or 'NONE (must not over-fire)', sorted(new)))
    print('SELFTEST %s %d of %d' % ('OK' if ok == total else 'BROKEN', ok, total)); print('CHECKED %d arm(s)' % total)
    return 0 if ok == total else 1


if __name__ == '__main__':
    A = sys.argv[1:]
    if not A or '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    repo = opt('--repo')
    if '--selftest' in A: raise SystemExit(selftest(repo))
    head = opt('--head', K['head'])
    if git(repo, 'rev-parse', '--verify', '--quiet', head + '^{commit}', check=False)[0] != 0:
        print('REFUSED: head %s unresolvable in %s' % (head, repo)); raise SystemExit(2)
    print('c3b_security_gate65 repo %s head %s' % (repo, head[:12]))
    t = Tally(); run_all(t, repo, head); raise SystemExit(t.end())
