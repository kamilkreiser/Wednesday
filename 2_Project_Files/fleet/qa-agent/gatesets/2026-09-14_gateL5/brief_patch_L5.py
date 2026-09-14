#!/usr/bin/env python3
"""brief_patch_L5.py — derive the L5 gate brief (develop pinned at M20) from the prior drafter's brief
(gatesets/2026-09-14_gate799/2026-09-14_secuura-799-880-ks764-577-tier1.md, sha256 asserted) by ASSERTED substitutions:
every anchor must occur exactly once (or the stated count) or the script refuses. Every new pin below was read by
Wednesday's drafting helper at 10:38–10:41 AEST 2026-09-14 (lsremote_m20_1.out, develop_m20_read.out, merge_m20_read.out,
lstree_m20_read.out, gh_read_m20.out) — nothing here is carried from memory."""
import hashlib, sys, re, datetime
O = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gateL5'
SRC = O + '/prior/2026-09-14_secuura-799-880-ks764-577-tier1.md'
DST = O + '/2026-09-14_secuura-L5-799-880-985-ks764-577-780-tier1.md'
EXPECT_SRC_SHA = '85bbc9238cc604e5'   # the prior set's pristine brief (redproof.out cell 23, 09:26 AEST)
s = open(SRC, encoding='utf-8').read()
got = hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]
assert got == EXPECT_SRC_SHA, f'source brief sha256 {got} != {EXPECT_SRC_SHA}'
print(f'source brief sha256 {got} (asserted)')
n_sub = 0
def sub(old, new, count=1):
    global s, n_sub
    c = s.count(old)
    assert c == count, f'anchor count {c} != {count} for: {old[:90]!r}'
    s = s.replace(old, new); n_sub += 1

M20 = 'a5334350221c819f54d4a20a3308daeb9ca09617'

# E1 — title
sub('ONE launcher pinning three heads + develop, ONE verdict mail with a verdict per PR',
    'ONE launcher pinning three heads + develop M20 `' + M20 + '`, ONE verdict mail with a verdict per PR — every merge MEASURED onto M20')

# E2 — the merge-shaped paragraph: the M20 tree
sub("so **the head tree `0f2c7b9b5` IS the PR merged onto live develop** — `git merge-tree --write-tree 8861e6216 6da848891` in Wednesday's own clone = `0f2c7b9b5` = the head's tree, 0 conflicts.",
    "so **the head tree `0f2c7b9b5` IS the PR merged onto develop M18** — `git merge-tree --write-tree 8861e6216 6da848891` in Wednesday's own clone = `0f2c7b9b5` = the head's tree, 0 conflicts. **Onto the CURRENT develop M20 `a53343502` the merge is a real 3-way: `git merge-tree --write-tree a53343502 6da848891` = `16ea40dc3`, 0 conflicts, the same tree in either order (Wednesday's clone, 10:39 AEST); its 12 PR paths carry the HEAD's blobs, its diff from the head tree is EXACTLY M20's six develop paths (`.githooks/pre-push`, `Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh`, `Blockchain/Dev/scripts/preflight/preflight.sh`, and #982's three `services/auth` files), and the five suite subtrees you run (`packages/shared` `d4acb0abe`, `services/security` `805c6c7c8`, `services/originate` `23f99dd4e`, `services/api-gateway` `29f59a3fd`, `services/tenant-provisioning` `0f023fb96`) are byte-identical at M18 and M20 — so the head tree and `16ea40dc3` carry the SAME bytes under every suite. THE TREE YOU MEASURE IS `16ea40dc3` (merge M20 into `6da848891` in your clone, or check that tree out detached; assert `git diff 6da848891 <yours> --name-only` = the six).**")

# E3 — the develop bullet of TARGET, rewritten whole (the GUARDED list is carried verbatim from the old line)
lines = s.split('\n')
idx = [i for i, l in enumerate(lines) if l.startswith('- **develop = M19 `6e78961e1d04277ecbdb0537e630afa0bf63b13c`**')]
assert len(idx) == 1, f'develop bullet count {len(idx)}'
old = lines[idx[0]]
a = old.index('refused (exit 18) only on a GUARDED path — ') + len('refused (exit 18) only on a GUARDED path — ')
b = old.index(' — **#880 landing before this gate trips exit 18 by design')
guarded = old[a:b]
assert guarded.startswith("#799's 12 paths, #880's 5 paths,") and 'qa-f4-resolveonbehalfof-org-normalisation' in guarded, guarded[:80]
new = ("- **develop = M20 `" + M20 + "`** (#903's squash \"KS-991: skip a local develop that origin/develop provably supersedes (#903)\", 2026-09-13T23:18:09Z; read 09:18:18, 10:38:03 AEST by ls-remote and 10:41:16 AEST by `/branches/develop` — unmoved since) = **M18 `8861e6216`** (#980's squash, 12:00:26Z; the builder's cut; **the merge-base of ALL THREE heads — unchanged**: compare `develop...6da848891` = merge_base `8861e6216`, status `diverged`, ahead 12, behind 2, files 12; `...a704137de` ahead 4 behind 2 files 5; `...fcd8a01e4` ahead 13 behind 2 files 17 — read 10:41 AEST; the launcher asserts merge_base / ahead / files, not the status) **+ TWO squashes / SIX files: M19 `6e78961e1`** (#982 / KS-790, 23:00:09Z — `services/auth/src/routes/oauth.ts` +23 −5, NEW `services/auth/src/__tests__/ks790-token-pre-auth-user-lookup.test.ts` +249, `ks820-821-token-client-auth-and-apptype.test.ts` +8) **and M20** (#903 / KS-991 — `.githooks/pre-push` +39 −1, `Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh` +123 −1, `Blockchain/Dev/scripts/preflight/preflight.sh` +24 −0). **Disjoint from every path this brief's expectations rest on, MEASURED (`lstree_m20_read.out`, 0 FAIL): every develop blob cited in this brief (the neighbours and the three PRs' develop-side files — 21 paths) is the SAME blob at M18 and M20; the five suite subtrees are byte-identical M18 = M20 (`services/auth` `4ffd02ef8` → `3e50b73de` and `scripts` `600f912c4` → `908fdef57` are the two that moved — the positive control); so every develop-alone figure below holds at M20 = M18 for every suite you run, and the ratio you predict on a merged tree is the head-tree ratio.** **The merges onto M20, in Wednesday's own `--shared` clone (10:39 AEST), all 0 conflicts, the same tree in either order: #799 `merge-tree --write-tree a53343502 6da848891` = `16ea40dc3`; #880 `… a704137de` = `2246dae85`; #985 `… fcd8a01e4` = `42a6fb6c5`** — each merged tree = the head's PR blobs + M20's six + nothing else (`git diff <head> <tree> --name-only` = exactly the six; the merged path set = the head's + the ks790 NEW file). Onto M18 (the earlier pins, re-derived 10:39): `0f2c7b9b5` / `3f496a12e` / `07553a609` = the head trees. **The launcher's develop pin is M20 and is DISJOINTNESS-CHECKED:** if develop moved past M20 at launch, the launcher read the GitHub compare of that delta and refused (exit 18) only on a GUARDED path — " + guarded + " — **#880 or #799 landing before this gate trips exit 18 by design (they move `services/security/src/index.ts`, the policy and the yaml) — a deliberate re-pin, not a work-around**; otherwise it printed the move. If it printed a move: `ls-remote` again at start and end, merge the THEN-CURRENT develop in your own clone (a real 3-way; `merge-tree --write-tree <dev> <head>`, 0 conflicts expected, name any), and re-derive the full-suite counts: **packages/shared = develop's own + 15, services/security = develop's own + 18, services/originate = develop's own + 10, services/api-gateway = develop's own + 0, 0 failed** (and for #985's tree: + 22 / + 18 / + 13 / + 0) — state the instrument. The API's `mergeable` for all three PRs read `null / unknown` at 10:41 AEST (GitHub recomputing after M20; the 08:xx reads said `true / unstable`) — not a finding; the merge-tree above is the instrument.")
lines[idx[0]] = new
s = '\n'.join(lines); n_sub += 1

# E4 — #799 item 1 scope
sub("**`git merge-tree --write-tree 8861e6216 6da848891` = `0f2c7b9b5` = the head tree** (or, if develop moved, a real 3-way with 0 conflicts — name any);",
    "**`git merge-tree --write-tree 8861e6216 6da848891` = `0f2c7b9b5` = the head tree** (M18 an ancestor) **and `git merge-tree --write-tree a53343502 6da848891` = `16ea40dc3`, 0 conflicts — the M20 merged tree you MEASURE; `git diff 6da848891 16ea40dc3 --name-only` = exactly M20's six develop paths** (if develop moved past M20, a real 3-way onto the then-current tip with 0 conflicts — name any);")

# E5/E6 — items 2(e) and 2(f)
sub("**(e) the full suites on the head tree (= the PR merged onto develop): `packages/shared` → predicted",
    "**(e) the full suites on the MERGED tree `16ea40dc3` (= the PR merged onto M20; the same bytes as the head tree under every suite — the five suite subtrees are byte-identical M18 = M20 — say which tree you ran): `packages/shared` → predicted")
sub("**(f) the control: develop-alone (a detached worktree at `8861e6216` in your clone, its own farm) — predicted",
    "**(f) the control: develop-alone (a detached worktree at M20 `a53343502` in your clone, its own farm; = M18 for every suite subtree, by sha) — predicted")

# E7/E8 — the #880 section
sub("; `merge-tree --write-tree 85f8263c2 8861e6216` = `654a000ce` = `6114a15d7`'s tree; the 3 feature files blob-identical",
    "; `merge-tree --write-tree 85f8263c2 8861e6216` = `654a000ce` = `6114a15d7`'s tree; **`merge-tree --write-tree a53343502 a704137de` = `2246dae85`, 0 conflicts — the M20 merged tree you measure**; the 3 feature files blob-identical")
sub("**(d) the suites, ONE run each on the head tree (MEASURED):",
    "**(d) the suites, ONE run each on the merged tree `2246dae85` (= the head onto M20; the same bytes under every suite; MEASURED):")

# E9/E10 — the #985 section
sub("`git merge-tree --write-tree 8861e6216 fcd8a01e4` = the head tree `07553a609` (develop an ancestor); **the definitions census",
    "`git merge-tree --write-tree 8861e6216 fcd8a01e4` = the head tree `07553a609` (M18 an ancestor) and **`git merge-tree --write-tree a53343502 fcd8a01e4` = `42a6fb6c5`, 0 conflicts — the M20 merged tree you measure**; **the definitions census")
sub("the pair with #880: `merge-tree --write-tree fcd8a01e4 a704137de` → predicted clean (the same `services/security/src/index.ts` hunks as #799's pair; name the tree).",
    "the pair with #880: `merge-tree --write-tree fcd8a01e4 a704137de` = `26fc332a7`, 0 conflicts (Wednesday's clone, 10:39 AEST; the same `services/security/src/index.ts` hunks as #799's pair).")

# E12 — KNOWN-FRAGILE
sub("- **develop moves under you** — M18 at 08:40, M19 (#982's squash) at 09:07; #881",
    "- **develop moves under you** — M18 at 08:40, M19 (#982's squash) at 09:07, M20 (#903's) at 09:18 — unmoved at 10:38 and 10:41; #881")

# E13 — BOUNDS readings
sub("(09:07:10 AEST: `6e78961e1` / `6da848891` / `a704137de` / `6da848891` / `a704137de`); `ls .git/worktrees | wc -l` (99).",
    "(10:38:03 AEST: `a53343502` / `6da848891` / `a704137de` / `6da848891` / `a704137de`); `ls .git/worktrees | wc -l` (103 at 10:38).")
sub("`git for-each-ref | wc -l` (848); `git ls-remote origin refs/heads/develop refs/pull/799/head",
    "`git for-each-ref | wc -l` (850 at 10:38); `git ls-remote origin refs/heads/develop refs/pull/799/head")

# E14 — the verdict subject (the tasking's format)
sub("`[QA -> Wednesday] TIER 1 GATE #799 (KS-764) 6da848891 -- <GO|GO WITH FINDINGS|NO GO> ; TIER 2 #880 (KS-577) a704137de -- <GO|GO WITH FINDINGS|NO GO> ; TIER 2 #985 (KS-780) fcd8a01e4 -- <GO|GO WITH FINDINGS|NO GO>`,",
    "`[QA -> Wednesday] GATE L5 #799 (T1) #880 (T2, Kam merges) #985 (T2) 6da848891 a704137de fcd8a01e4 -- #799 <GO|GO WITH FINDINGS|NO GO> ; #880 <GO|GO WITH FINDINGS|NO GO> ; #985 <GO|GO WITH FINDINGS|NO GO>`,")

# E15 — the verdict paragraph names M20's trees
sub("AND as the whole PR merged onto the develop you read (name it). Severity per the charter",
    "AND as the whole PR merged onto the develop you read (M20 `a53343502` at launch — the tree `16ea40dc3`; name it). Severity per the charter")
sub("(Peter's condition) AND merged onto the develop you read; **the merge is KAM's regardless of the verdict.**",
    "(Peter's condition) AND merged onto the develop you read (M20 — the tree `2246dae85`); **the merge is KAM's regardless of the verdict.**")
sub("as the delta over its stack parent `6da848891` AND merged onto the develop you read; **merge order #799 → #985.** A GO is",
    "as the delta over its stack parent `6da848891` AND merged onto the develop you read (M20 — the tree `42a6fb6c5`); **merge order #799 → #985.** A GO is")

# E21 — REPORT bullet
sub("the merged shape (head tree `0f2c7b9b5` onto the develop you read, 0 conflicts) with the four full-suite counts",
    "the merged shape (the M20 merged tree `16ea40dc3` = the head onto the develop you read, 0 conflicts; head tree `0f2c7b9b5`) with the four full-suite counts")

# E16 — the #799 mergeable read
sub("`mergeable: true / unstable` (`unstable` = develop's own CI; ignore), **5 reviews, all PeterObeden COMMENTED**",
    "`mergeable: true / unstable` at 08:12 (`unstable` = develop's own CI; ignore) and `null / unknown` at 10:41 (GitHub recomputing after M20; ignore — Wednesday's merge-tree is the instrument), **5 reviews, all PeterObeden COMMENTED**")

# E17 — Peter's commission, verbatim, inserted as its own bullet before "The commits"
commission = ("- **THE COMMISSION, VERBATIM — Peter's PR comment `5600549339` (PeterObeden, 2026-09-09T10:43:01Z, 974 chars, 0 at-signs; re-read 10:41 AEST, unchanged; `gh/pr799_comment_5600549339.md`):** "
  "*\"**Outstanding at head `7dfc7ebca` — three lines and a fixture.** Short version of the review above, so it isn't buried: "
  "[ ] **KS-860** — `app.listen(0, '127.0.0.1', cb)` in both new wire test files (`originate …revoke-route-contract.test.ts:121`, `security …revoke-organisation-route-contract.test.ts:128`). Now red on the branch itself: the develop merge at `7dfc7ebca` brought the guard in. **2 lines** · "
  "[ ] **F-2** — `expect(typeof shared.decideKeyRevoke).toBe('function')` ahead of the existing mock control (`originate …:153`), which passes today when the export is absent. **1 line** · "
  "[ ] **F-3** — one fixture with no `tenantId`, to cover the `403 caller has no tenant` this PR introduces. **1 fixture** · "
  "Everything else is closed and verified. Push those and I'll bring a stack up against that head, run the 8-case matrix on both routes, and post the result either way. Refs KS-764. Refs KS-860.\"* "
  "(the Claude Code footer omitted). His line numbers are `7dfc7ebca`'s; the head's are `:145` / `:138` / `:184`. His \"Refs KS-860\" is HIS to type — the builder's never-type list forbids it to the builder (the guard is named by path in the commit; item 1 checks). His \"8-case matrix on both routes\" is the live leg this gate does NOT run (NOT TESTED).")
sub("\n- **The commits (every one Kam Kreiser `<kamil.kreiser@secuura.ai>` except Peter's two merges):**",
    "\n" + commission + "\n- **The commits (every one Kam Kreiser `<kamil.kreiser@secuura.ai>` except Peter's two merges):**")

# E18 — PROVENANCE: the M20 re-pin line, appended
prov = ("- THE M20 RE-PIN (Wednesday's second drafting helper, 10:38–10:41 AEST 2026-09-14, after the first died mid-repin at 09:2x): origin refs/heads/develop " + M20 + " (M20; ls-remote 10:38:03; /branches/develop 10:41:16, 2026-09-13T23:18:09Z \"KS-991: skip a local develop that origin/develop provably supersedes (#903)\"); refs/pull/799/880/985/head and the three branches UNMOVED (6da848891 / a704137de / fcd8a01e4); checkout porcelain 0, 850 refs, 103 .git/worktrees, .git/config e0fa706f4bdae277, HEAD 355d82c8b; worktrees s216-ks764-r3 / s216-ks577-r2 / s216-ks780 at their heads, porcelain 0; M18..M20 = 2 commits (M19 6e78961e1 #982 23:00:09Z; M20 #903 23:18:09Z) / 6 files (git log/diff --numstat; the API compare M18...M20 ahead 2 files 6, M19...M20 ahead 1 files 3); compares develop...6da848891 = merge_base 8861e6216 diverged ahead 12 behind 2 files 12, ...a704137de ahead 4 behind 2 files 5, ...fcd8a01e4 ahead 13 behind 2 files 17, 6da848891...fcd8a01e4 = merge_base 6da848891 ahead 1 files 7; PRs #799/#880/#985 open, not merged, heads unchanged, mergeable null/unknown at 10:41; Peter's comment 5600549339 (974 chars, 0 at-signs) and the builder's 5656460918 / 5529715057 present unchanged; #799 5 reviews / #880 2 / #985 0 as before | lsremote_m20_1.out, develop_m20_read.out, gh_read_m20.py / .out (token by NAME) | read 2026-09-14\n"
        "- the merges onto M20, in the drafting helper's own --shared --no-checkout clone (gatesets/2026-09-14_gateL5/model/clone; write verbs there only): merge-tree --write-tree a53343502 6da848891 = 16ea40dc3, a53343502 a704137de = 2246dae85, a53343502 fcd8a01e4 = 42a6fb6c5 — rc 0, one output line (no conflict list), the same tree in the reverse order; onto M18 re-derived 0f2c7b9b5 / 3f496a12e / 07553a609 = the head trees; the pair 6da848891 + a704137de = c1758ada4 either order (re-derived); fcd8a01e4 + a704137de = 26fc332a7; for each merged tree: the PR paths (12 / 5 / 17) carry the head's blobs, the six M18..M20 paths carry M20's blobs, the path set = the head's + the ks790 NEW file (3725 = 3724 + 1 for #799), git diff <head> <tree> --name-only = exactly the six; the 21 neighbour/develop-side blobs the brief cites are identical M18 == M20 (ks860 e0dfadb9c, ks742 d35e2d5dc, jwt.ts d0d55c11b, audit-baseline 03d1680e3, shared index.ts 6731f0f2f, shared middleware/index.ts b5932490c, security index.ts ed0239d79, security keyRevokePolicy.ts 60bd9ef5e, adminConfig.ts ccb3222a6, originate middleware/auth.ts 38a0db12a, originate orgId.ts a40475112, provenance.ts 483aa9eb3, gdprService.ts 4d138883c, documents.ts b2f4bf351, ks695 d377aa8c2, the yaml f14ab17ed, the .ts source 5903759c7, platform.ts 2e1699aa0, generate-openapi.ts e84acdc9e, startup-migrations.ts ed3e52142, BACKLOG.md 9d99b3bec; ks597-b 255103343, ks597-issuer-org-bind 9bb899a10, qa-f4 2dbc65f4c; ks577 test ABSENT at both); the five suite subtrees byte-identical M18 == M20 (packages/shared d4acb0abe, services/security 805c6c7c8, services/originate 23f99dd4e, services/api-gateway 29f59a3fd, services/tenant-provisioning 0f023fb96) with services/auth and scripts MOVED as the positive control | merge_m20_read.out, lstree_m20_read.out (0 FAIL) | read 2026-09-14\n")
assert s.endswith('\n'), 'brief must end with a newline'
s = s + prov; n_sub += 1

# residual guard: no M19-as-pin wording survives
for bad in ['develop = M19', 'the pin stays M19', 'moved past M19', 'M19 = M18 for them', 'hold at M19 = M18']:
    assert bad not in s, f'residual: {bad!r}'
assert s.count(M20) >= 2 and s.count('16ea40dc3') >= 5 and s.count('2246dae85') >= 4 and s.count('42a6fb6c5') >= 4, 'M20 pins under-stated'
assert 'TIER 1' in s and 'ROUND 1' in s and 'MAIL YOUR VERDICT' not in s
for h in ('6da848891924f859179d097d464a7b97c9783a6a', 'a704137de38a3055e40ee62adc343c0239f34ea9', 'fcd8a01e40d34d6cb4055e7b4fd58b9bb908bbe0'):
    assert h in s, h
raw = s.encode('utf-8')
ctrl = [i for i, x in enumerate(raw) if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f]
assert not ctrl, f'raw control bytes at {ctrl[:5]}'
open(DST, 'w', encoding='utf-8').write(s)
print(f'{n_sub} substitutions asserted; written {DST} ({len(raw)} bytes, {s.count(chr(10))} lines, sha256 {hashlib.sha256(raw).hexdigest()[:16]}); raw control bytes 0; {datetime.datetime.now():%H:%M:%S}')
