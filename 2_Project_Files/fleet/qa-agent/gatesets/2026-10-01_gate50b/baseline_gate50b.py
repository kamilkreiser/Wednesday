#!/usr/bin/env python3
"""baseline_gate50b.py — the drafter's PREDICTION of requirement 1 and 3 (#1364's diff re-derived by PARSING both blobs, never by reading the diff),
in the SCRATCH clone (<scratchpad>/g50b_sp/clone), read-only (git show / ls-tree only). Every check prints its reading; a zero sits beside a control.
  B0  file list develop..head == the 2 kit paths (control: the same call on develop..develop reads 0 paths).
  B1  rows: base 26, head 25 (kit.json baseline.rows_*).
  B2  removed == {GHSA-mwp4-54f8-5fhr}; added == {}.
  B3  surviving rows that differ from base == {GHSA-r53p-7pc4-xj5r}; B4 its differing fields == {reason}; package / ticket / decidedAt equal; no `expires` after.
  B5  r53p's head reason == the B 49th extracted file, CHARACTER-EXACT (file 1948 B, no trailing newline); the stale clause present before, absent after.
      CONTROL: the same compare against the BASE reason reads False.
  B6  the 2026-10-09 cohort: base 4 -> head 3; the three survivors BYTE-EQUAL (parsed entry AND its raw text block); names == kit fuse_head.
  B7  no row's `expires` changed anywhere; no row added.
  B8  GRANDFATHERED_NO_EXPIRY block text byte-equal base/head; ids 18; == the no-expiry set of the head baseline (the contract's own invariant).
  B9  baseline-contract.mjs: exactly ONE differing line, its number and text == kit (:44 17 -> 18); line count equal.
  B10 baseline-contract.test.mjs: the FILENAME is asserted (the seat's own fault: a floor probe on the wrong file); blob base == head; line :217 carries `> 20`;
      head rows 25 > 20. CONTROL: the same `> 20` probe on baseline-contract.mjs reads False (the wrong file).
  B11 the fuse cohort at END (pins_gate50b.json end_tree): rows with expires 2026-10-09 == the kit's three.
Options (controls): --head <sha> (a planted head), --reason-file <path>. Usage: baseline_gate50b.py <scratchpad> [--head sha] [--reason-file p]"""
import json, os, subprocess, sys, hashlib, datetime, re
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8')); BK = K['baseline']
A = sys.argv[1:]; SP = A[0]; CL = os.path.join(SP, 'g50b_sp', 'clone')
P = json.load(open(os.path.join(G, 'pins_gate50b.json'), encoding='utf-8'))
N = K['order'][0]; DEV = P['develop']; H = A[A.index('--head') + 1] if '--head' in A else P['pr_pins']['head']
RF = A[A.index('--reason-file') + 1] if '--reason-file' in A else BK['reason_file']
def git(*a):
    r = subprocess.run(['git', '-C', CL] + list(a), capture_output=True, text=True)
    if r.returncode: raise SystemExit('REFUSING: git %s rc %d: %s' % (' '.join(a), r.returncode, r.stderr.strip()[:200]))
    return r.stdout
H = git('rev-parse', H + '^{commit}').strip()
show = lambda t, p: git('show', '%s:%s' % (t, p))
fails = []; n = 0
def chk(tag, ok, msg):
    global n; n += 1; print('%s %s: %s' % ('PASS' if ok else 'FAIL', tag, msg))
    if not ok: fails.append(tag)
print('baseline_gate50b %s | base %s | head %s | END_TREE %s | clone %s' % (datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), DEV[:12], H[:12], P['end_tree'][:12], CL))
names = sorted(git('diff', '--name-only', DEV, H).split()); want = sorted(K['prs'][N]['files'])
chk('B0', names == want, 'changed paths %d %s == kit %s | CONTROL develop..develop reads %d path(s)' % (len(names), names, want, len(git('diff', '--name-only', DEV, DEV).split())))
bt, ht = show(DEV, BK['path']), show(H, BK['path'])
bj, hj = json.loads(bt), json.loads(ht)
chk('B1k', sorted(bj) == sorted(hj), 'top-level keys base %s head %s' % (sorted(bj), sorted(hj)))
key = 'accepted' if 'accepted' in bj else sorted(bj)[0]; B, Hh = bj[key], hj[key]
chk('B1', len(B) == BK['rows_base'] and len(Hh) == BK['rows_head'], 'rows base %d (want %d) head %d (want %d)' % (len(B), BK['rows_base'], len(Hh), BK['rows_head']))
rem = sorted(set(B) - set(Hh)); add = sorted(set(Hh) - set(B))
chk('B2', rem == BK['removed'] and add == [], 'removed %s (want %s) | added %s' % (rem, BK['removed'], add))
if rem: print('     removed row(s) at base: %s' % '; '.join('%s package=%s ticket=%s expires=%s' % (r, B[r].get('package'), B[r].get('ticket'), B[r].get('expires')) for r in rem))
diff = sorted(r for r in set(B) & set(Hh) if B[r] != Hh[r])
chk('B3', diff == [BK['reason_changed']], 'surviving rows that differ %s (want [%s])' % (diff, BK['reason_changed']))
r = BK['reason_changed']
if r in B and r in Hh:
    fd = sorted(f for f in set(B[r]) | set(Hh[r]) if B[r].get(f) != Hh[r].get(f))
    chk('B4', fd == ['reason'] and 'expires' not in Hh[r], '%s fields that differ %s | package %r ticket %r decidedAt %r | expires after: %s' % (r, fd, Hh[r].get('package'), Hh[r].get('ticket'), Hh[r].get('decidedAt'), 'expires' in Hh[r]))
    ft = open(RF, encoding='utf-8').read(); fb = os.path.getsize(RF)
    chk('B5', Hh[r]['reason'] == ft and fb == BK['reason_file_bytes'], 'head reason == %s CHARACTER-EXACT: %s | file %d B (kit %d) sha256 %s, ends in newline: %s | head reason %d chars | CONTROL base reason == file: %s' % (
        os.path.basename(RF), Hh[r]['reason'] == ft, fb, BK['reason_file_bytes'], hashlib.sha256(open(RF, 'rb').read()).hexdigest()[:16], ft.endswith('\n'), len(Hh[r]['reason']), B[r]['reason'] == ft))
    sc = BK['stale_clause']
    chk('B5s', sc in B[r]['reason'] and sc not in Hh[r]['reason'], 'stale clause %r: before %s, after %s' % (sc, sc in B[r]['reason'], sc in Hh[r]['reason']))
else: chk('B4', False, '%s absent at base or head' % r)
def block(txt, rid):  # the raw text block of one row, from its key line to its closing brace
    m = re.search(r'\n(\s*)"%s": \{.*?\n\1\}' % re.escape(rid), txt, re.S); return m.group(0) if m else None
fb_ = sorted(x for x in B if B[x].get('expires') == BK['fuse_date']); fh = sorted(x for x in Hh if Hh[x].get('expires') == BK['fuse_date'])
same = all(B.get(x) == Hh.get(x) and block(bt, x) is not None and block(bt, x) == block(ht, x) for x in fh)
chk('B6', len(fb_) == 4 and fh == sorted(BK['fuse_head']) and same, '%s cohort base %d %s -> head %d %s | survivors byte-equal (parsed AND raw block): %s' % (BK['fuse_date'], len(fb_), [x[5:9] for x in fb_], len(fh), fh, same))
ech = sorted(x for x in set(B) & set(Hh) if B[x].get('expires') != Hh[x].get('expires'))
chk('B7', ech == [] and add == [], 'rows whose expires changed %s | rows added %s | expires histogram base %s head %s' % (ech, add,
    dict(sorted({e: sum(1 for v in B.values() if v.get('expires', 'none') == e) for e in set(v.get('expires', 'none') for v in B.values())}.items())),
    dict(sorted({e: sum(1 for v in Hh.values() if v.get('expires', 'none') == e) for e in set(v.get('expires', 'none') for v in Hh.values())}.items()))))
bc, hc = show(DEV, BK['contract']), show(H, BK['contract'])
gfb = re.search(r'export const GRANDFATHERED_NO_EXPIRY = new Set\(\[.*?\]\);', bc, re.S); gfh = re.search(r'export const GRANDFATHERED_NO_EXPIRY = new Set\(\[.*?\]\);', hc, re.S)
ids = re.findall(r"'(GHSA-[^']+)'", gfh.group(0)) if gfh else []
noexp = sorted(x for x in Hh if 'expires' not in Hh[x])
chk('B8', gfb and gfh and gfb.group(0) == gfh.group(0) and len(ids) == BK['grandfathered_count'] and sorted(ids) == noexp,
    'GRANDFATHERED_NO_EXPIRY block byte-equal: %s | ids %d (want %d) | == the head no-expiry set (%d): %s' % (bool(gfb and gfh and gfb.group(0) == gfh.group(0)), len(ids), BK['grandfathered_count'], len(noexp), sorted(ids) == noexp))
bl, hl = bc.split('\n'), hc.split('\n')
dl = [i + 1 for i in range(max(len(bl), len(hl))) if (bl[i] if i < len(bl) else None) != (hl[i] if i < len(hl) else None)]
ok9 = dl == [BK['contract_changed_line']] and bl[dl[0] - 1] == BK['contract_line_before'] and hl[dl[0] - 1] == BK['contract_line_after'] and len(bl) == len(hl)
chk('B9', ok9, 'baseline-contract.mjs differing line(s) %s (want [%d]) | line count %d -> %d%s' % (dl, BK['contract_changed_line'], len(bl) - 1, len(hl) - 1,
    ''.join(' | :%d %r -> %r' % (i, bl[i - 1], hl[i - 1]) for i in dl[:3])))
tp = BK['contract_test']; tb = git('rev-parse', '%s:%s' % (DEV, tp)).strip(); th = git('rev-parse', '%s:%s' % (H, tp)).strip()
tl = show(H, tp).split('\n'); fl = tl[BK['floor_line'] - 1] if len(tl) >= BK['floor_line'] else ''
wrong = BK['floor_text'] in hc
chk('B10', os.path.basename(tp) == 'baseline-contract.test.mjs' and tb == th and BK['floor_text'] in fl and len(Hh) > 20,
    'FILE %s (asserted by name) blob base %s head %s equal %s | :%d %r carries %r: %s | head rows %d > 20: %s | CONTROL the same probe on %s (the WRONG file) reads %s' % (
        tp.split('/')[-1], tb[:12], th[:12], tb == th, BK['floor_line'], fl.strip()[:110], BK['floor_text'], BK['floor_text'] in fl, len(Hh), len(Hh) > 20, BK['contract'].split('/')[-1], wrong))
ej = json.loads(show(P['end_tree'], BK['path']))[key]; fe = sorted(x for x in ej if ej[x].get('expires') == BK['fuse_date'])
chk('B11', fe == sorted(BK['fuse_head']), 'FUSE at END %s: %d row(s) %s | control at develop: %d' % (P['end_tree'][:12], len(fe), fe, len(fb_)))
print('%s: %d FAIL of %d checks | base %s head %s | rows %d -> %d | removed %s | fuse %d -> %d' % ('BASELINE PASS' if not fails else 'BASELINE FAIL', len(fails), n, DEV[:12], H[:12], len(B), len(Hh), rem, len(fb_), len(fh)))
sys.exit(1 if fails else 0)
