#!/usr/bin/env python3
"""prompt_patch_L5.py — derive the L5 agent prompt (develop M20) from the prior drafter's prompt (sha256 asserted) by
ASSERTED substitutions (each anchor exactly once). The pins are the same reads brief_patch_L5.py cites."""
import hashlib, datetime
O = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gateL5'
SRC = O + '/prior/2026-09-14_secuura-799-880-ks764-577-tier1.prompt.txt'
DST = O + '/2026-09-14_secuura-L5-799-880-985-ks764-577-780-tier1.prompt.txt'
EXPECT_SRC_SHA = 'a0ebd314c2d9c93a'   # the prior set's pristine prompt (redproof.out cell 23)
s = open(SRC, encoding='utf-8').read()
got = hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]
assert got == EXPECT_SRC_SHA, f'source prompt sha256 {got} != {EXPECT_SRC_SHA}'
print(f'source prompt sha256 {got} (asserted)')
n = 0
def sub(old, new, count=1):
    global s, n
    c = s.count(old); assert c == count, f'anchor count {c} != {count} for: {old[:90]!r}'
    s = s.replace(old, new); n += 1

# P1 — the brief path
sub('/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-799-880-ks764-577-tier1.md',
    '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-L5-799-880-985-ks764-577-780-tier1.md')

# P2 — the develop paragraph (Subject A)
sub("""  origin develop = M19 6e78961e1 (#982's squash, 23:00:09Z; read 09:07 AEST 2026-09-14) = M18 8861e6216 (the builder's
  cut, the merge-base of all three heads) + three services/auth files — disjoint from every guarded path; the four suites
  you run are untouched by it (develop-alone figures hold at M19 = M18 for them). The
""",
"""  origin develop = M20 a5334350221c819f54d4a20a3308daeb9ca09617 (#903 / KS-991, 23:18:09Z; read 10:38 and 10:41 AEST
  2026-09-14) = M18 8861e6216 (the builder's cut; the merge-base of all three heads — the compares now read ahead
  12 / 4 / 13, BEHIND 2) + TWO squashes / SIX files (M19 = #982: three services/auth files; M20 = #903: .githooks/
  pre-push, the hook's shell test, preflight.sh) — MEASURED disjoint: every develop blob the brief cites is the same
  blob at M18 and M20, and the five suite subtrees you run (packages/shared, services/security, services/originate,
  services/api-gateway, services/tenant-provisioning) are byte-identical M18 = M20, so every develop-alone figure holds
  at M20 = M18. The merges onto M20 in Wednesday's clone, 0 conflicts in either order: #799 -> tree 16ea40dc3,
  #880 -> 2246dae85, #985 -> 42a6fb6c5 — each = the head's PR blobs + M20's six files and nothing else. THOSE are the
  trees you measure (the same bytes as the heads under every suite; say which tree you ran beside every count). The
""")
sub("If develop moved past M19 at launch, merge the then-current tip in your own clone and re-derive:",
    "If develop moved past M20 at launch, merge the then-current tip in your own clone and re-derive:")

# P4 — the Repo line's worktrees
sub("detached worktrees at 6da848891, a704137de, fcd8a01e4 and 8861e6216 (develop-alone control); node_modules",
    "detached worktrees at 6da848891, a704137de, fcd8a01e4 — each with M20 a53343502 merged in your clone (trees 16ea40dc3 /\n  2246dae85 / 42a6fb6c5, 0 conflicts; `git diff <head> <tree> --name-only` = exactly M20's six files) — and at\n  a53343502 (the develop-alone control; = M18 for every suite subtree); node_modules")

# P5 — item 1: the M20 trees
sub("the head tree 0f2c7b9b5 =\n   `merge-tree --write-tree 8861e6216 6da848891`; the 12 blobs",
    "the head tree 0f2c7b9b5 =\n   `merge-tree --write-tree 8861e6216 6da848891` and `merge-tree --write-tree a53343502 6da848891` = 16ea40dc3 (M20 —\n   the tree you measure; its diff from the head = exactly the six develop paths); the 12 blobs")
sub("the merge\n   tree 654a000ce = `merge-tree --write-tree 85f8263c2 8861e6216`; the 3 feature files",
    "the merge\n   tree 654a000ce = `merge-tree --write-tree 85f8263c2 8861e6216`; onto M20 = 2246dae85 (0 conflicts); the 3 feature files")
sub("`merge-tree --write-tree 8861e6216 fcd8a01e4` =\n    07553a609; the definitions census",
    "`merge-tree --write-tree 8861e6216 fcd8a01e4` =\n    07553a609 and onto M20 = 42a6fb6c5 (0 conflicts; the tree you measure); the definitions census")
sub("`merge-tree\n    --write-tree fcd8a01e4 a704137de` clean (name the tree).",
    "`merge-tree\n    --write-tree fcd8a01e4 a704137de` = 26fc332a7, clean (Wednesday's clone; re-derive it).")

# P6 — item 3: the tree the suites run on, and the develop-alone worktree
sub("the full suites\n   on the head tree — packages/shared 42 files / 828",
    "the full suites\n   on the M20-merged tree 16ea40dc3 (the same bytes as the head under every suite — say which you ran) — packages/shared 42 files / 828")
sub("develop-alone (your 8861e6216 worktree, own\n   farm)",
    "develop-alone (your a53343502 M20 worktree, own\n   farm; = M18 for every suite subtree)")

# P7 — the verdict lines name M20
sub("as the\nround's delta over e6e25421e AND as the whole PR merged onto the develop you measured (name it);",
    "as the\nround's delta over e6e25421e AND as the whole PR merged onto the develop you measured (M20 at launch — tree 16ea40dc3; name it);")

# P8 — the subject (the tasking's format)
sub("[QA -> Wednesday] TIER 1 GATE #799 (KS-764) 6da848891 -- <GO|GO WITH FINDINGS|NO GO> ; TIER 2 #880 (KS-577) a704137de -- <GO|GO WITH FINDINGS|NO GO> ; TIER 2 #985 (KS-780) fcd8a01e4 -- <GO|GO WITH FINDINGS|NO GO>",
    "[QA -> Wednesday] GATE L5 #799 (T1) #880 (T2, Kam merges) #985 (T2) 6da848891 a704137de fcd8a01e4 -- #799 <GO|GO WITH FINDINGS|NO GO> ; #880 <GO|GO WITH FINDINGS|NO GO> ; #985 <GO|GO WITH FINDINGS|NO GO>")

for bad in ['M19 6e78961e1', 'past M19', 'M19 = M18 for them', '8861e6216 (develop-alone control)']:
    assert bad not in s, f'residual: {bad!r}'
assert s.startswith('ultrathink\n') and 'TIER 1' in s and 'ROUND 1' in s and 'MAIL YOUR VERDICT' in s
assert 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' in s and 'Do no memory maintenance' in s and 'NEVER print a credential value' in s
for h in ('6da848891924f859179d097d464a7b97c9783a6a', 'a704137de38a3055e40ee62adc343c0239f34ea9', 'fcd8a01e40d34d6cb4055e7b4fd58b9bb908bbe0'):
    assert h in s, h
raw = s.encode('utf-8'); assert not [i for i, x in enumerate(raw) if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f]
open(DST, 'w', encoding='utf-8').write(s)
print(f'{n} substitutions asserted; written {DST} ({len(raw)} bytes, {s.count(chr(10))} lines, sha256 {hashlib.sha256(raw).hexdigest()[:16]}); raw control bytes 0; {datetime.datetime.now():%H:%M:%S}')
