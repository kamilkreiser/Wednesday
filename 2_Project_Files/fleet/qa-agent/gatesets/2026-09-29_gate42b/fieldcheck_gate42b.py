#!/usr/bin/env python3
"""fieldcheck_gate42b.py — requirements 1 and 2, FIELD BY FIELD (never off the diff text): the audit baseline at the merge-base vs the head.
Default inputs: the blobs `git show <merge_base>:<path>` / `<head>:<path>` and `git diff --name-only` from the scratch clone (pins_gate42b.json).
Overrides (the controls plant defects through these): --base-file F --head-file F --files a,b --authority F (a text file) --clone DIR.
The AUTHORITY is Kam's instruction text (kit.json authority.text; the capture proves it is in his mail verbatim). From it the tool PARSES the
named ids, the ticket each is named under, and the date — it never hard-codes the four ids.
  F1 the PR's file list == [kit path]                    F2 top-level keys identical, `$comment` byte-identical
  F3 row count == kit rows_expected at BOTH sides        F4 the row id set and ORDER identical (none added, removed or moved)
  F5 the rows that differ == EXACTLY the ids Kam named   F6 on each: the fields that differ == {expires, reason}, nothing else
  F7 each named row's `expires` == Kam's date            F8 each named row's `ticket` == the ticket Kam named it under (and unchanged)
  F9 each new `reason` == old reason + an APPENDED tail carrying the Message-ID and Kam's instruction verbatim
  F10 no row of the HEAD (named or not) expires on or before the fuse day (2026-09-30) — the fuse is defused by the file itself
rc 0 all PASS, rc 1 any FAIL. Prints `N checked`; 0 rows checked is a FAIL. Usage: fieldcheck_gate42b.py <scratchpad> [overrides]"""
import json, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
P = json.load(open(os.path.join(G, 'pins_gate42b.json'), encoding='utf-8'))
CL = opt('--clone', os.path.join(SP, 'g42b_sp', 'clone')); PATH = K['path']
def show(sha): return subprocess.run(['git', '-C', CL, 'show', '%s:%s' % (sha, PATH)], capture_output=True, text=True, check=True).stdout
base_t = open(opt('--base-file')).read() if opt('--base-file') else show(P['merge_base'])
head_t = open(opt('--head-file')).read() if opt('--head-file') else show(P['head'])
files = opt('--files').split(',') if opt('--files') else subprocess.run(['git', '-C', CL, 'diff', '--name-only', P['merge_base'], P['head']], capture_output=True, text=True, check=True).stdout.split()
auth = open(opt('--authority')).read().strip() if opt('--authority') else K['authority']['text']
B, H = json.loads(base_t), json.loads(head_t); ba, ha = B.get('accepted', {}), H.get('accepted', {})
# parse the authority: GHSA ids accumulate until a "(KS-n)" names their ticket; the date follows "to "
named, pend = {}, []
for m in re.finditer(r'(GHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4})|\((KS-\d+)\)', auth):
    if m.group(1): pend.append(m.group(1))
    else: named.update({g: m.group(2) for g in pend}); pend = []
dm = re.search(r'\bto (\d{4}-\d{2}-\d{2})\b', auth); DATE = dm.group(1) if dm else None
res = []
def chk(tag, ok, msg): res.append(ok); print('%s %s: %s' % ('PASS' if ok else 'FAIL', tag, msg))
print('authority parsed: %d id(s) %s | ungrouped %s | date %s | kit new_expires %s' % (len(named), named, pend, DATE, K['new_expires']))
chk('F0', len(named) > 0 and not pend and DATE == K['new_expires'], 'the authority names %d id(s), every one under a ticket, and the date %s == kit %s' % (len(named), DATE, K['new_expires']))
chk('F1', files == [PATH], 'files %s' % files)
chk('F2', list(B.keys()) == list(H.keys()) and B.get('$comment') == H.get('$comment'), 'top-level keys %s -> %s; $comment identical %s' % (list(B), list(H), B.get('$comment') == H.get('$comment')))
chk('F3', len(ba) == len(ha) == K['rows_expected'], 'rows %d -> %d (want %d)' % (len(ba), len(ha), K['rows_expected']))
chk('F4', list(ba) == list(ha), 'row ids and order identical: %s' % (list(ba) == list(ha)))
diff = [k for k in ha if k in ba and ha[k] != ba[k]]
chk('F5', sorted(diff) == sorted(named), 'rows that differ %s | Kam named %s' % (sorted(diff), sorted(named)))
nck = 0
for k in sorted(set(diff) | set(named)):
    b, h = ba.get(k, {}), ha.get(k, {}); nck += 1
    fd = sorted(f for f in set(b) | set(h) if b.get(f) != h.get(f))
    chk('F6 ' + k, fd == ['expires', 'reason'], 'fields that differ %s' % fd)
    chk('F7 ' + k, h.get('expires') == DATE, 'expires %s -> %s (Kam: %s)' % (b.get('expires'), h.get('expires'), DATE))
    chk('F8 ' + k, h.get('ticket') == b.get('ticket') == named.get(k), 'ticket %s -> %s (Kam named it under %s)' % (b.get('ticket'), h.get('ticket'), named.get(k)))
    ob, nr = b.get('reason', ''), h.get('reason', '')
    tail = nr[len(ob):] if nr.startswith(ob) else None
    ok9 = tail is not None and K['authority']['message_id'] in tail and ' '.join(auth.split()) in ' '.join(tail.replace('\\"', '"').split())
    chk('F9 ' + k, ok9, 'reason = old + appended tail (%s chars) carrying the Message-ID and the instruction verbatim: %s' % (len(tail) if tail is not None else 'NOT APPENDED', ok9))
early = sorted('%s %s' % (k, v.get('expires')) for k, v in ha.items() if v.get('expires') and v['expires'] <= K['fuse_utc'][:10])
chk('F10', not early, 'head rows expiring on/before %s: %s' % (K['fuse_utc'][:10], early or 'none'))
soon = sorted('%s %s' % (k, v.get('expires')) for k, v in ha.items() if v.get('expires'))
print('INFO head rows with an expires: %s' % soon)
chk('FN', nck > 0, '%d named/differing row(s) checked, %d rows compared' % (nck, len(ha)))
nf = res.count(False)
print('FIELDCHECK %s: %d checks, %d FAIL, %d row(s) checked field by field' % ('PASS' if nf == 0 else 'FAIL', len(res), nf, nck))
raise SystemExit(1 if nf else 0)
