import sys, re, collections
a_path, b_path = sys.argv[1], sys.argv[2]
U = 'BypassRefused { reason: "a path the gate could not resolve" }'
N = 'BypassRefused { reason: "a fetch that is not to a web address" }'
tot = dec = cand_dec = ord_dec = ord_diff = noncand_diff = 0
per = collections.Counter(); other = []; act_diff = 0
cur_action = None
with open(a_path, encoding='utf-8', errors='surrogateescape') as fa, open(b_path, encoding='utf-8', errors='surrogateescape') as fb:
    for la, lb in zip(fa, fb):
        tot += 1
        if la.startswith('A'):
            cur_action = la
            if la != lb: act_diff += 1; other.append(('ACTION', la[:300], lb[:300]))
            continue
        if not la.startswith(' A'):
            if la != lb: other.append(('TRAILER', la, lb))
            continue
        dec += 1
        cand = ' cand=1 ' in la; ordi = ' ord=1 ' in la
        cand_dec += cand; ord_dec += ordi
        if la == lb: continue
        pa = la.split(' ', 7); pb = lb.split(' ', 7)
        da, db = pa[7].rstrip('\n'), pb[7].rstrip('\n')
        if pa[:7] != pb[:7]: other.append(('HEADER', la[:300], lb[:300])); continue
        ordi and None
        if ordi: ord_diff += 1
        if not cand: noncand_diff += 1
        was_allow = da.startswith('Allow { why: Bypass')
        if was_allow and db == 'Deny { reason: ' + U + ' }':
            per['UnresolvedTarget'] += 1
            per['UnresolvedTarget unres=1' if ' unres=1 ' in cur_action else 'UnresolvedTarget unres=0 (!)'] += 1
        elif was_allow and db == 'Deny { reason: ' + N + ' }':
            per['NonWebFetch'] += 1
            per['NonWebFetch nonweb=1' if ' nonweb=1 ' in cur_action else 'NonWebFetch nonweb=0 (!)'] += 1
        else:
            other.append(('OTHER', cur_action[:400], la.rstrip(), lb.rstrip()))
    rest_a = fa.read(1); rest_b = fb.read(1)
print(f'lines {tot} decisions {dec} cand-decisions {cand_dec} ordinary-resolved-decisions {ord_dec}')
print(f'diffs per class {dict(per)}; diffs on ordinary-resolved {ord_diff}; diffs on non-candidate actions {noncand_diff}; action-line diffs {act_diff}; length mismatch {bool(rest_a or rest_b)}')
print(f'OTHER differences: {len(other)}')
for o in other[:20]: print(o)
