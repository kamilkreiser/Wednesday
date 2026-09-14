#!/usr/bin/env python3
"""gen_launcher_L5.py — generate launch_qa_secuura_L5_799_880_985.sh from the prior drafter's three-head launcher
(gatesets/2026-09-14_gate799/launch_qa_secuura_ks764_577_780_799_880_985.sh, sha256 d11f93e0af26962f — itself adapted
from the #982 launcher) by ASSERTED substitutions: the develop pin M19 -> M20 (the re-pin Wednesday asked for), the L5
file names, the QAL5_ override prefix, the header's develop paragraph and the --check DEV_NOTE, the lineage line.
Same guard family, same exit codes (2..18, 20, 21). Every anchor must occur exactly the stated number of times.
Written by a generator because the launcher contains a legitimate `cd`."""
import hashlib, re, subprocess, datetime
O = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gateL5'
SRC = O + '/prior/launch_qa_secuura_ks764_577_780_799_880_985.sh'
DST = O + '/launch_qa_secuura_L5_799_880_985.sh'
EXPECT = 'd11f93e0af26962f'
s = open(SRC, encoding='utf-8').read()
got = hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]
assert got == EXPECT, f'template sha256 {got} != {EXPECT}'
print(f'template sha256 {got} (asserted)')
M19 = '6e78961e1d04277ecbdb0537e630afa0bf63b13c'; M20 = 'a5334350221c819f54d4a20a3308daeb9ca09617'
n = 0
def sub(old, new, count=1):
    global s, n
    c = s.count(old); assert c == count, f'anchor count {c} != {count} for: {old[:100]!r}'
    s = s.replace(old, new); n += 1

# names
sub('launch_qa_secuura_ks764_577_780_799_880_985.sh', 'launch_qa_secuura_L5_799_880_985.sh', 2)          # header + Usage
sub('2026-09-14_secuura-799-880-ks764-577-tier1', '2026-09-14_secuura-L5-799-880-985-ks764-577-780-tier1', 3)   # BRIEF, PROMPT_FILE, REAL_BRIEF
sub('QA799_', 'QAL5_', 10)                                                                                # 5 defaults + 5 in the override guard
# the develop pin
sub(f"DEVELOP_SHA='{M19}'", f"DEVELOP_SHA='{M20}'")
# the header's compare sentence: develop is no longer an ancestor of the heads (behind 2 at M20)
sub("# M18, ahead 12, behind 0, TWELVE files) — so the head tree IS the PR merged onto live develop. #880's head is ONE fix",
    "# M18, ahead 12, behind 2 at M20, TWELVE files) — so the head tree IS the PR merged onto M18, and the PR merged onto\n# M20 is the 3-way tree 16ea40dc3 (0 conflicts; = the head's PR blobs + M20's six develop files). #880's head is ONE fix")
# the header's develop paragraph
sub("""# origin develop = M19 6e78961e1 (#982's squash "KS-790: the OAuth token grants resolve the user through the pre-auth
# carve-out…", 2026-09-13T23:00:09Z; read 09:07 AEST 2026-09-14) — ONE squash past M18 8861e6216 (the builder's cut; the
# merge-base of all three heads, unchanged), THREE files under services/auth/, disjoint from every guarded path below —
# the launcher's own MOVED judgement at 08:5x AEST, then re-pinned deliberately. The develop pin below is
# DISJOINTNESS-CHECKED, not bare: if origin develop has moved past M19, the GitHub compare of that delta is read and the launcher REFUSES (exit 18) only when the
""",
"""# origin develop = M20 a5334350221c819f54d4a20a3308daeb9ca09617 (#903's squash "KS-991: skip a local develop that
# origin/develop provably supersedes", 2026-09-13T23:18:09Z; read 10:38 and 10:41 AEST 2026-09-14) — TWO squashes past
# M18 8861e6216 (the builder's cut; the merge-base of all three heads, unchanged): M19 6e78961e1 (#982, three files
# under services/auth/) and M20 (#903: .githooks/pre-push, scripts/__tests__/pre_push_hook_base.test.sh,
# scripts/preflight/preflight.sh) — SIX files, disjoint from every guarded path below, MEASURED: every develop blob the
# brief cites is the same at M18 and M20 and the five suite subtrees the gate runs are byte-identical M18 = M20. The
# merges onto M20 in Wednesday's own clone: #799 -> 16ea40dc3, #880 -> 2246dae85, #985 -> 42a6fb6c5, 0 conflicts each.
# (The first drafter's launcher pinned M19 and judged the M19..M20 move DISJOINT at 09:18; this one is the deliberate
# re-pin to M20.) The develop pin below is
# DISJOINTNESS-CHECKED, not bare: if origin develop has moved past M20, the GitHub compare of that delta is read and the launcher REFUSES (exit 18) only when the
""")
# the --check note when develop is still the pin
sub("(M19 = M18 + the KS-790 squash of three services/auth files; the merge-base of all three heads is M18 and the ratios 828/205/598/343, 195/13 and 835/601 were written against M18 = M19 for the four suites the gate runs; git ls-remote)",
    "(M20 = M18 + #982's three services/auth files + #903's hook / shell test / preflight.sh; the merge-base of all three heads is M18; the five suite subtrees are byte-identical M18 = M20, so the ratios 828/205/598/343, 195/13 and 835/601 hold; the merges onto M20 are 16ea40dc3 / 2246dae85 / 42a6fb6c5, 0 conflicts; git ls-remote)")
# lineage
sub("# Adapted from the #982 launcher by gen_launcher_799.py (asserted substitutions, three asserted block replacements,\n# residual guard): the same guard family and exit codes 2..18, 20, 21",
    "# Adapted from the first L5 drafter's three-head launcher (gatesets/2026-09-14_gate799, template sha256 d11f93e0af26962f;\n# itself from the #982 launcher) by gen_launcher_L5.py (asserted substitutions: the M20 re-pin, the L5 names, the QAL5_\n# overrides, the header and --check wording; residual guard): the same guard family and exit codes 2..18, 20, 21")

# residual guard
for bad in [M19 + "'", 'M19 = M18 +', 'past M19', 'QA799_', 'gen_launcher_799', 'ks764_577_780_799_880_985', '799-880-ks764-577-tier1', 'behind 0']:
    assert bad not in s, f'residual: {bad!r}'
# output controls (counts read from the generated text, then asserted)
controls = {f"DEVELOP_SHA='{M20}'": 1, 'QAL5_BRIEF': 2, 'QAL5_PROMPT': 2, 'QAL5_HEAD:': 2, 'QAL5_HEAD_880': 2, 'QAL5_HEAD_985': 2,
            '2026-09-14_secuura-L5-799-880-985-ks764-577-780-tier1.md': 2, '2026-09-14_secuura-L5-799-880-985-ks764-577-780-tier1.prompt.txt': 1,
            # counts read from the template's own lines (grep -n -F, 10:49 AEST): exit 10 = 3 code lines (:125-127) + 1 header (:18);
            # exit 18 = 2 code (:131, :187) + 2 header (:46, :54); exit 21 = 1 code (:224) + 1 --check echo (:220) + 1 header (:58);
            # each compare string = its assertion line + its REFUSING message on the same line
            'exit 6': 1, 'exit 10': 4, 'exit 13': 1, 'exit 18': 4, 'exit 20': 1, 'exit 21': 3, 'exit 16': 2, "MERGE_BASE='8861e62161466c40f08d2b10a30edeb203123993'": 1,
            '[ -t 0 ]': 1, '16ea40dc3': 3, '2246dae85': 2, '42a6fb6c5': 2, 'HEAD_799 ahead=1 files=7': 2, 'MERGE_BASE ahead=12 files=12': 2, 'MERGE_BASE ahead=4 files=5': 2}
bad = {k: (s.count(k), v) for k, v in controls.items() if s.count(k) != v}
assert not bad, f'output controls: {bad}'
raw = s.encode('utf-8'); assert not [i for i, x in enumerate(raw) if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f]
open(DST, 'w', encoding='utf-8').write(s)
import os; os.chmod(DST, 0o755)
rc = subprocess.run(['/bin/bash', '-n', DST]).returncode
print(f'{n} substitutions asserted; {len(controls)} output controls; residual guard clean; written {DST} ({len(raw)} bytes, sha256 {hashlib.sha256(raw).hexdigest()[:16]}); bash -n rc={rc}; {datetime.datetime.now():%H:%M:%S}')
assert rc == 0
