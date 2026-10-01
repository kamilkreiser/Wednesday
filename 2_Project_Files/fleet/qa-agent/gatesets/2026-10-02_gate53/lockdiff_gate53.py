#!/usr/bin/env python3
"""lockdiff_gate53.py — the drafter's prediction for requirements 1 and 5 (the row) of gate53, read from BLOBS in the scratch clone (no install,
no network). Base = pins develop, head = pins head (overridable for controls). Every check prints its counts; a zero prints beside a control.
  L1 ROOT LOCK, `packages` map diffed KEY BY KEY as parsed JSON: removed == {kit nested_key} exactly, added 0, changed 0, dev/devOptional/optional/peer
     flag flips 0; every top-level key but `packages` equal (lockfileVersion, name, requires).
  L2 `node_modules/@prisma/dev` (kit prisma_dev_key): value-equal AND its raw text block byte-identical in both blobs; its dependencies still record
     its OWN manifest (`@hono/node-server` == the base nested version), i.e. the override is not written into it.
  L3 the hoisted `node_modules/@hono/node-server` (kit hoisted_key): equal in both, version == kit hoisted_version (its integrity printed for registry_gate53).
  L4 THE OTHER LOCKS: every tracked `package-lock.json` in both trees (count == kit locks_total); the blobs that differ == {the root lock} exactly.
  L5 the root lock's TEXT diff: deletions only, ONE block, and head == base with EXACTLY the nested member's lines cut, byte for byte (a hand
     prune that left a stray comma, whitespace or a second edit would show here).
  M1 ROOT MANIFEST: every top-level key but `overrides` equal; overrides: every base key kept with an equal value, added exactly
     {override_parent: {override_child: override_value}}; no top-level override of the child; text diff insertions only (+3/-0).
  B1 BASELINE KEY SETS (parsed, never grep): `accepted` removed == {removed_row}, added none; top-level keys and `$comment` equal.
  B2 BASELINE BYTES: the text diff is deletions only, ONE block, head == base with EXACTLY the removed row's member cut, byte for byte; and every
     surviving row's raw text block is byte-identical base vs head (the value-level proof is not the byte-level one).
  B3 FUSES: no `expires` changed on any surviving row; dated rows base -> head; the cohort on kit cohort_date == kit cohort_base -> cohort_head.
  B4 THE SUBSTRING TRAP (a control, not a check of the PR): the removed id's SUBSTRING still occurs at head (kit frvp_substring_hits_head, inside
     other rows' reason text) while its KEY count is 0 — a grep would read a correct removal as a failure.
Overrides (controls): --base <sha> --head <sha>. rc 0 PASS / rc 1 FAIL. Usage: lockdiff_gate53.py <scratchpad> [--base sha] [--head sha]"""
import json, os, re, subprocess, sys, difflib, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate53.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
CL = os.path.join(SP, 'g53_sp', 'clone'); N = K['order'][0]; E = K['expect_counts']
def git(*a):
    r = subprocess.run(['git', '-C', CL] + list(a), capture_output=True, text=True)
    if r.returncode: raise SystemExit('REFUSING: git %s rc %d: %s' % (' '.join(a)[:80], r.returncode, r.stderr.strip()[:200]))
    return r.stdout
B = git('rev-parse', opt('--base', P['develop']) + '^{commit}').strip(); H = git('rev-parse', opt('--head', P['pr_pins'][N]['head']) + '^{commit}').strip()
print('lockdiff_gate53 %s | base %s | head %s%s' % (datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), B[:12], H[:12],
      ' (OVERRIDDEN for a control)' if (opt('--base') or opt('--head')) else ''))
res = []
def chk(tag, ok, msg): res.append(ok); print('%s %s: %s' % ('PASS' if ok else 'FAIL', tag, msg))
def show(sha, p): return git('show', '%s:%s' % (sha, p))
def block(text, key):
    """the raw text of the JSON member `"key": {...}` (from its line to the matching close brace), or None"""
    ls = text.split('\n'); want = '"%s": {' % key
    st = [i for i, l in enumerate(ls) if l.strip() == want]
    if len(st) != 1: return None
    depth = 0
    for j in range(st[0], len(ls)):
        depth += ls[j].count('{') - ls[j].count('}')
        if depth == 0: return '\n'.join(ls[st[0]:j + 1]).rstrip(',')
    return None
def textdiff(a, b):
    sm = difflib.SequenceMatcher(None, a.split('\n'), b.split('\n'), autojunk=False)
    return [op for op in sm.get_opcodes() if op[0] != 'equal'], a.split('\n')
def cut(text, key):
    """text with EXACTLY the lines of member `"key": {...}` (its comma included) removed — what a surgical one-member prune must produce"""
    ls = text.split('\n'); want = '"%s": {' % key
    st = [i for i, l in enumerate(ls) if l.strip() == want]
    if len(st) != 1: return None
    depth = 0
    for j in range(st[0], len(ls)):
        depth += ls[j].count('{') - ls[j].count('}')
        if depth == 0: break
    out = ls[:st[0]] + ls[j + 1:]
    if not ls[j].rstrip().endswith(','):   # the LAST member: the comma goes from the line before it
        k = st[0] - 1; out[k] = out[k].rstrip().rstrip(',')
    return '\n'.join(out), j + 1 - st[0]
# ---- L1 - L3, L5: the root lock
LK = K['root_lock']; lb_t, lh_t = show(B, LK), show(H, LK); lb, lh = json.loads(lb_t), json.loads(lh_t)
pb, ph = lb['packages'], lh['packages']
rem = sorted(set(pb) - set(ph)); add = sorted(set(ph) - set(pb)); both = set(pb) & set(ph)
FL = ('dev', 'devOptional', 'optional', 'peer')
chg = sorted(x for x in both if pb[x] != ph[x]); flips = sorted(x for x in both if any(pb[x].get(f) != ph[x].get(f) for f in FL))
print('INFO L1 entries %d -> %d | ADDED %d | REMOVED %d %s | CHANGED %d %s | flag flips %d %s' % (len(pb), len(ph), len(add), len(rem), rem, len(chg), chg[:5], len(flips), flips[:5]))
chk('L1 key-by-key', rem == [K['nested_key']] and not add and not chg and not flips and len(pb) == E['lock_entries_base'] and len(ph) == E['lock_entries_head'],
    'removed %s (want [%s]), added %d, changed %d, flips %d, entries %d -> %d (want %d -> %d)' % (rem, K['nested_key'], len(add), len(chg), len(flips), len(pb), len(ph), E['lock_entries_base'], E['lock_entries_head']))
if rem == [K['nested_key']]: print('INFO L1 the removed entry was: %s' % json.dumps(pb[K['nested_key']], sort_keys=True))
tk = sorted(k for k in set(lb) | set(lh) if k != 'packages' and lb.get(k) != lh.get(k))
chk('L1 top-level', not tk, 'top-level keys other than packages that differ: %s' % (tk or 'NONE'))
PD = K['prisma_dev_key']; bb, hb = block(lb_t, PD), block(lh_t, PD)
dep = (ph.get(PD) or {}).get('dependencies', {}).get(K['override_child'])
chk('L2 @prisma/dev', pb.get(PD) == ph.get(PD) and bb is not None and bb == hb and ph.get(PD, {}).get('version') == K['prisma_dev_version'] and dep == K['nested_version_base'],
    'value-equal %s | raw block byte-identical %s (%s bytes) | version %s | its dependencies["%s"] = %r (records its own manifest, not the override)' % (
        pb.get(PD) == ph.get(PD), bb is not None and bb == hb, len(hb or ''), ph.get(PD, {}).get('version'), K['override_child'], dep))
HK = K['hoisted_key']; hv = ph.get(HK, {})
chk('L3 hoisted', pb.get(HK) == ph.get(HK) and hv.get('version') == K['hoisted_version'],
    '%s equal base/head %s | version %s (want %s) | devOptional %s | integrity %s' % (HK, pb.get(HK) == ph.get(HK), hv.get('version'), K['hoisted_version'], hv.get('devOptional'), hv.get('integrity')))
ops, _ = textdiff(lb_t, lh_t); dels = [o for o in ops if o[0] == 'delete']; c = cut(lb_t, K['nested_key'])
okblk = c is not None and c[0] == lh_t
chk('L5 text diff', len(ops) == 1 and len(dels) == 1 and okblk, '%d hunk(s), %d deletion-only block(s), %d line(s) deleted | head == base with EXACTLY the %s member (%s lines) cut: %s' % (
    len(ops), len(dels), sum(o[2] - o[1] for o in dels), K['nested_key'], c[1] if c else '?', okblk))
# ---- L4: every lock
def locks(sha): return {l.split('\t')[1]: l.split()[2] for l in git('ls-tree', '-r', sha).splitlines() if l.split('\t')[1].endswith('package-lock.json')}
kb, kh = locks(B), locks(H); diffl = sorted(p for p in set(kb) | set(kh) if kb.get(p) != kh.get(p))
chk('L4 other locks', len(kb) == len(kh) == E['locks_total'] and diffl == [LK], 'tracked package-lock.json: base %d, head %d (want %d) | blobs that differ: %s (want [%s]) | %d others byte-identical' % (
    len(kb), len(kh), E['locks_total'], diffl, LK, len(set(kb) & set(kh)) - len([p for p in diffl if p in kb and p in kh])))
# ---- M1: the root manifest
PJ = K['root_manifest']; mb_t, mh_t = show(B, PJ), show(H, PJ); mb, mh = json.loads(mb_t), json.loads(mh_t)
tk = sorted(k for k in set(mb) | set(mh) if k != 'overrides' and mb.get(k) != mh.get(k))
ob, oh = mb.get('overrides', {}), mh.get('overrides', {})
kept = all(k in oh and oh[k] == v for k, v in ob.items()); added = {k: v for k, v in oh.items() if k not in ob}
want = {K['override_parent']: {K['override_child']: K['override_value']}}
ops2, _ = textdiff(mb_t, mh_t); ins = sum(o[4] - o[3] for o in ops2 if o[0] == 'insert'); other = [o for o in ops2 if o[0] != 'insert']
chk('M1 manifest', not tk and kept and added == want and K['override_child'] not in oh and not other and ins == 3,
    'other top-level keys that differ %s | base overrides kept %s (%d) | added %s (want %s) | top-level "%s" override %s | text: +%d insert-only %s' % (
        tk or 'NONE', kept, len(ob), json.dumps(added), json.dumps(want), K['override_child'], 'PRESENT' if K['override_child'] in oh else 'absent', ins, not other))
# ---- B1 - B4: the baseline
BL = K['baseline']; bb_t, bh_t = show(B, BL), show(H, BL); jb, jh = json.loads(bb_t), json.loads(bh_t); ab, ah = jb.get('accepted', {}), jh.get('accepted', {})
rr = sorted(set(ab) - set(ah)); ra = sorted(set(ah) - set(ab)); RID = K['removed_row']
print('INFO B1 rows %d -> %d | removed %s | added %s' % (len(ab), len(ah), rr, ra))
chk('B1 key sets', rr == [RID] and not ra and len(ab) == E['baseline_rows_base'] and len(ah) == E['baseline_rows_head'] and sorted(jb) == sorted(jh) and jb.get('$comment') == jh.get('$comment'),
    'removed exactly {%s}: %s | added none: %s | rows %d -> %d (want %d -> %d) | top-level keys equal %s | $comment equal %s' % (
        RID, rr == [RID], not ra, len(ab), len(ah), E['baseline_rows_base'], E['baseline_rows_head'], sorted(jb) == sorted(jh), jb.get('$comment') == jh.get('$comment')))
ops3, _ = textdiff(bb_t, bh_t); d3 = [o for o in ops3 if o[0] == 'delete']; c3 = cut(bb_t, RID); okb = c3 is not None and c3[0] == bh_t; nb = sum(o[2] - o[1] for o in d3)
surv = sorted(set(ab) & set(ah)); vdiff = [k for k in surv if ab[k] != ah[k]]; rdiff = [k for k in surv if block(bb_t, k) is None or block(bb_t, k) != block(bh_t, k)]
chk('B2 bytes', len(ops3) == 1 and len(d3) == 1 and okb and not vdiff and not rdiff,
    'text diff %d hunk(s), %d line(s) deleted | head == base with EXACTLY the %s member cut: %s | surviving rows %d: changed by value %d, by raw bytes %d %s | trailing newline %s' % (
        len(ops3), nb, RID, okb, len(surv), len(vdiff), len(rdiff), rdiff[:3], bh_t.endswith('\n')))
eb = {k: v.get('expires') for k, v in ab.items()}; eh = {k: v.get('expires') for k, v in ah.items()}
exch = sorted(k for k in surv if eb[k] != eh[k]); dated = (sum(1 for v in eb.values() if v), sum(1 for v in eh.values() if v))
cb = sorted(k for k, v in eb.items() if v == K['cohort_date']); chh = sorted(k for k, v in eh.items() if v == K['cohort_date'])
chk('B3 fuses', not exch and dated == (E['dated_base'], E['dated_head']) and cb == sorted(K['cohort_base']) and chh == sorted(K['cohort_head']),
    'expires changed on a surviving row: %s | dated %d -> %d (want %d -> %d) | cohort %s: %s -> %s' % (exch or 'NONE', dated[0], dated[1], E['dated_base'], E['dated_head'], K['cohort_date'], cb, chh))
sub = [i + 1 for i, l in enumerate(bh_t.split('\n')) if RID in l]; keyc = sum(1 for k in ah if k == RID)
subb = [i + 1 for i, l in enumerate(bb_t.split('\n')) if RID in l]
chk('B4 substring trap (control)', len(sub) == E['frvp_substring_hits_head'] and keyc == 0,
    'at head the id occurs as a SUBSTRING on line(s) %s (%d, want %d; inside other rows\' reason text) while its KEY count is %d — a grep would misread a correct removal | at base: line(s) %s' % (
        sub, len(sub), E['frvp_substring_hits_head'], keyc, subb))
nf = res.count(False)
print('LOCKDIFF %s: %d FAIL of %d checks | base %s head %s' % ('PASS' if nf == 0 else 'FAIL', nf, len(res), B[:12], H[:12]))
raise SystemExit(1 if nf else 0)
