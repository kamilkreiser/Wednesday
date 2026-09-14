#!/usr/bin/env python3
"""redproof_patch_L5.py — derive redproof.sh for the L5 launcher (develop M20) from the prior set's redproof.sh (sha256
asserted) by asserted substitutions: the L5 names, the QAL5_ overrides, the M20 pin, cell 0's develop-still note, and the
develop-guard cells re-aimed at the LIVE deltas from M19 (one squash / three files) and M18 (two squashes / six files)."""
import hashlib, os
O = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gateL5'
src = O + '/prior/redproof.sh'; dst = O + '/redproof.sh'
s = open(src, encoding='utf-8').read(); got = hashlib.sha256(s.encode()).hexdigest()[:16]
print('template redproof.sh sha256', got)
n = 0
def sub(old, new, count=1):
    global s, n; c = s.count(old); assert c == count, f'{c}!={count}: {old[:90]!r}'; s = s.replace(old, new); n += 1
sub('# redproof.sh — red-proof launch_qa_secuura_ks764_577_780_799_880_985.sh on SCRATCH COPIES only.',
    '# redproof.sh — red-proof launch_qa_secuura_L5_799_880_985.sh (develop pinned at M20) on SCRATCH COPIES only.')
sub('# against LIVE deltas: pinned to M18 (M18..M19 = #982, three services/auth files, disjoint), to M15 and to M9 (M9..develop carries the ks860 guard file) and to an unknown SHA.',
    '# against LIVE deltas: pinned to M19 (M19..M20 = #903, three hook/preflight files, disjoint), to M18 (M18..M20 = two squashes / six files,\n# disjoint), to M15 and to M9 (M9..develop carries the ks860 guard file) and to an unknown SHA.')
sub('G="${G:?set G to the gate799 scratch dir}"', 'G="${G:?set G to the gateL5 scratch dir}"')
sub('L="$G/launch_qa_secuura_ks764_577_780_799_880_985.sh"', 'L="$G/launch_qa_secuura_L5_799_880_985.sh"')
sub('B="$G/2026-09-14_secuura-799-880-ks764-577-tier1.md"', 'B="$G/2026-09-14_secuura-L5-799-880-985-ks764-577-780-tier1.md"')
sub('P="$G/2026-09-14_secuura-799-880-ks764-577-tier1.prompt.txt"', 'P="$G/2026-09-14_secuura-L5-799-880-985-ks764-577-780-tier1.prompt.txt"')
sub("M19='6e78961e1d04277ecbdb0537e630afa0bf63b13c'", "M19='6e78961e1d04277ecbdb0537e630afa0bf63b13c'; M20='a5334350221c819f54d4a20a3308daeb9ca09617'")
sub('QA799_', 'QAL5_', 15)   # grep -c on the template read 15 (5 run() modes x env lines)
sub('DEVPIN="DEVELOP_SHA=\'$M19\'"', 'DEVPIN="DEVELOP_SHA=\'$M20\'"')
sub('"origin develop still $M19 (M19 = M18"', '"origin develop still $M20 (M20 = M18"')
sub('"origin develop MOVED $M19 -> .*— disjoint"', '"origin develop MOVED $M20 -> .*— disjoint"')
# substring counts read from the template with Python str.count (10:52 AEST): 'live M15..M18 delta' 5, 'M9..M18' 5 (3 'the OTHER M9..M18 hits' + 1 '3c: … M9..M18 delta' + 1 '3d: … moved in M9..M18')
sub('live M15..M18 delta', 'live M15..develop delta', 5)
sub('M9..M18', 'M9..develop', 5)
# cell 3e re-aimed: M18 pin -> the LIVE M18..M20 delta; new cell 3f: M19 pin -> M19..M20
old3e = '''# 3e: pinned to M18 — the LIVE M18..M19 delta (#982's squash, three services/auth files) -> DISJOINT -> 0 (the move this set lived through at 08:5x AEST)
cp "$L" "$W/l_dev18.sh"; ld="$(tamper "$L" "$W/l_dev18.sh" "$DEVPIN" "DEVELOP_SHA='$M18'" 1)"
run "3e pinned to M18: the live M18..M19 delta (#982, three auth files) DISJOINT -> 0" 0 "$W/l_dev18.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "origin develop MOVED $M18 -> $M19: commits=1 files=3" "$W/3e pinned to M18: the live M18..M19 delta (#982, three auth files) DISJOINT -> 0.out" || { echo "  cell 3e did not report MOVED commits=1 files=3 (develop moved again? re-read)"; FAILS=$((FAILS+1)); }
'''
new3e = '''# 3e: pinned to M18 — the LIVE M18..M20 delta (#982's three services/auth files + #903's three hook/preflight files) -> DISJOINT -> 0
cp "$L" "$W/l_dev18.sh"; ld="$(tamper "$L" "$W/l_dev18.sh" "$DEVPIN" "DEVELOP_SHA='$M18'" 1)"
run "3e pinned to M18: the live M18..M20 delta (two squashes, six files) DISJOINT -> 0" 0 "$W/l_dev18.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "origin develop MOVED $M18 -> $M20: commits=2 files=6" "$W/3e pinned to M18: the live M18..M20 delta (two squashes, six files) DISJOINT -> 0.out" || { echo "  cell 3e did not report MOVED commits=2 files=6 (develop moved again? re-read)"; FAILS=$((FAILS+1)); }
# 3f: pinned to M19 — the LIVE M19..M20 delta (#903's squash: .githooks/pre-push, the hook's shell test, preflight.sh) -> DISJOINT -> 0 (the move the first drafter's launcher lived through at 09:18 AEST)
cp "$L" "$W/l_dev19.sh"; ld="$(tamper "$L" "$W/l_dev19.sh" "$DEVPIN" "DEVELOP_SHA='$M19'" 1)"
run "3f pinned to M19: the live M19..M20 delta (#903, three hook and preflight files) DISJOINT -> 0" 0 "$W/l_dev19.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "origin develop MOVED $M19 -> $M20: commits=1 files=3" "$W/3f pinned to M19: the live M19..M20 delta (#903, three hook and preflight files) DISJOINT -> 0.out" || { echo "  cell 3f did not report MOVED commits=1 files=3 (develop moved again? re-read)"; FAILS=$((FAILS+1)); }
'''
sub(old3e, new3e)
sub('"/briefs/2026-09-14_secuura-799-880-ks764-577-tier1.md" "/briefs/2026-09-14_secuura-OTHER-tier1.md"',
    '"/briefs/2026-09-14_secuura-L5-799-880-985-ks764-577-780-tier1.md" "/briefs/2026-09-14_secuura-OTHER-tier1.md"')
sub('"brief missing or empty: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-799-880-ks764-577-tier1.md"',
    '"brief missing or empty: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-L5-799-880-985-ks764-577-780-tier1.md"')
sub('"$G/controls_check.sh" "$G/redproof.sh" "$G/gen_launcher_799.py" "$G/guards_sim.py" "$G/gh_read.py" "$G/linear_read.py" "$G/linear_titles.py"',
    '"$G/controls_check.sh" "$G/redproof.sh" "$G/gen_launcher_L5.py" "$G/brief_patch_L5.py" "$G/prompt_patch_L5.py" "$G/controls_patch_L5.py" "$G/redproof_patch_L5.py" "$G/gh_read_m20.py"')
for bad in ['QA799_', 'ks764_577_780_799_880_985', '799-880-ks764-577-tier1', 'DEVPIN="DEVELOP_SHA=\'$M19\'"', 'M18..M19', 'gen_launcher_799']:   # cell 3f legitimately tampers TO M19; the PIN must not be M19
    assert bad not in s, f'residual: {bad!r}'
open(dst, 'w', encoding='utf-8').write(s); os.chmod(dst, 0o755)
print(f'{n} substitutions asserted; written {dst} sha256 {hashlib.sha256(s.encode()).hexdigest()[:16]}')
