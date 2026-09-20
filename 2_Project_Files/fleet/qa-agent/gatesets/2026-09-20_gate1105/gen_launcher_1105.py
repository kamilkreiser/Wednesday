#!/usr/bin/env python3
"""gen_launcher_1105.py — write launchers/launch_qa_secuura_1105.sh (ONE tier-1 round-1 gate over PR #1105, KS-1175 real fix + KS-1284 codec,
Seat A 15th, READY 2026-09-20T13:55:07Z) in the SHAPE of launchers/launch_qa_secuura_batch1100_1101.sh (the most recent tier-1 gate launcher, which
ran cleanly): the same guard ladder and exit codes (6 head moved · 10 compare · 18/19 develop pin judged by CONTENT with LANDED detection · 7/15/8/9
/20/12/11/14/17/22/23/24/25/26/27/28/29/30/31/32/33 prompt + READY greps · 16 overrides at launch · 21 TTY), the same test overrides (QAB1105_*),
the same --check block. The data changed: ONE PR, a PRODUCT change (12 files under services/anchoring/** + the yaml + VOCABULARY.md), so the
"zero product bytes" guard of the template becomes "nothing OUTSIDE the allowed paths" and the LANDED detection covers 12 blobs (5 of them ABSENT
at develop).
Pins are RE-READ at generation, READ-ONLY throughout — no git write verb in the Secuura checkout:
  * origin: git ls-remote of refs/heads/develop, refs/pull/1105/head AND the branch — all must equal the pins;
  * local objects (rev-list / rev-parse / diff --raw / ls-tree): the head is ONE commit whose parent IS develop; the 12 (path, develop blob, head
    blob) triples as pinned; the 5 ADDED paths absent at develop; every "unchanged read" path has the SAME blob at develop and head; the CSL pin
    "15.0.3" in both lockfiles at both trees; the yaml diff has exactly ONE hunk.
  * every value the launcher carries is asserted present in its output exactly as often as intended (output controls), heredoc quote/paren
    parity is checked, and `bash -n` must pass, or nothing is written.
Usage: gen_launcher_1105.py <output launcher>
Exit: 0 written · 1 pin/control disagreed · 2 residual token · 3 bash -n"""
import hashlib, os, re, subprocess, sys, tempfile
OUT = sys.argv[1]
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_1105', now())
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
DEV = '778e6cfe2b6061d60ffcf3a57a951c84dc152b67'   # origin develop after Seat B 10th merged #1102-#1104 (re-pin 2026-09-21 00:3x AEST)
BASE = 'dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa'  # the head's parent = merge-base = the develop the builder READY'd against
SQUASHES = ['6e2fbc234788b23c446490efb6cb20fcc16ae629', '3232656cb13be8220a911edaac974123e62e6ee2', '778e6cfe2b6061d60ffcf3a57a951c84dc152b67']
MERGED_TREE = '1f2bc512aee2a55d74142d9ba8206a795b0c975c'   # predict_merge_scratch.out (real 3-way merge, both orders, clean); re-derived below by pure tree hashing
HEAD = 'e02d3ecb51a457b0eb490db1854f28c6b1af69ad'
HEAD_TREE = '8f066a81784c89ae3531938a006c7ae69bdb4ba1'
DEV_TREE = 'd0c8bfd095b65861efc1a4e8524017235b42e382'
BASE_TREE = '1ccb80e0d66ab0ff12d5dbb61753b8c0c274e923'
BRANCH = 'refs/heads/feature/ks-1175-anchor-originate-lifecycle-event-schemas-accept-and-anchor'
D = 'Blockchain/Dev/'; A = D + 'services/anchoring/'
def git(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
def out(*a):
    p = git(*a)
    if p.returncode: print('REFUSING: git', a[:3], p.stderr.strip()[:200]); sys.exit(1)
    return p.stdout
# 1. origin
lsr = out('ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/1105/head', BRANCH)
print('ls-remote', now(), '|', len(lsr.strip().splitlines()), 'refs read')
refs = dict((l.split('\t')[1], l.split('\t')[0]) for l in lsr.strip().splitlines())
for ref, want in (('refs/heads/develop', DEV), ('refs/pull/1105/head', HEAD), (BRANCH, HEAD)):
    print('  %-90s %s %s' % (ref, refs.get(ref, '?')[:9], 'OK' if refs.get(ref) == want else 'MOVED'))
    if refs.get(ref) != want: print('REFUSING: pin moved at origin'); sys.exit(1)
# 2. local objects
par = out('rev-list', '--parents', '-n1', HEAD).split()
print('head parents', par[1:], '| ONE parent == BASE dc061f2bb:', par[1:] == [BASE])
if par[1:] != [BASE]: sys.exit(1)
mb = out('merge-base', DEV, HEAD).strip(); print('merge-base develop..head', mb[:9], '== BASE:', mb == BASE)
if mb != BASE: sys.exit(1)
lr = out('rev-list', '--left-right', '--count', DEV + '...' + HEAD).split(); print('develop...head behind/ahead', lr, '(want 3 1)')
if lr != ['3', '1']: sys.exit(1)
sq = out('rev-list', '--reverse', BASE + '..' + DEV).split(); print('the squashes BASE..develop', [x[:9] for x in sq], '== pinned:', sq == SQUASHES)
if sq != SQUASHES: sys.exit(1)
ht, dt, bt = out('rev-parse', HEAD + '^{tree}').strip(), out('rev-parse', DEV + '^{tree}').strip(), out('rev-parse', BASE + '^{tree}').strip()
print('head tree', ht, '==', HEAD_TREE, ht == HEAD_TREE, '| develop tree', dt, '==', DEV_TREE, dt == DEV_TREE, '| base tree', bt[:9], '==', BASE_TREE[:9], bt == BASE_TREE)
if ht != HEAD_TREE or dt != DEV_TREE or bt != BASE_TREE: sys.exit(1)
ahead = out('rev-list', '--count', BASE + '..' + HEAD).strip()
print('ahead of BASE', ahead, '(want 1)')
if ahead != '1': sys.exit(1)
# the 12 changed paths: (path, develop blob or ABSENT, head blob)
raw = out('diff', '--raw', '--abbrev=40', BASE, HEAD).strip().splitlines()
CHANGED = {}
for l in raw:
    meta, path = l.split('\t', 1)
    m1, m2, b1, b2, st = meta.split()
    CHANGED[path] = ('ABSENT' if b1 == '0' * 40 else b1, b2, st, m2)
print('changed paths', len(CHANGED), '(want 12) | added', sum(1 for v in CHANGED.values() if v[2] == 'A'), '(want 5) | deleted/renamed', sum(1 for v in CHANGED.values() if v[2] not in 'AM'), '(want 0)')
if len(CHANGED) != 12 or sum(1 for v in CHANGED.values() if v[2] == 'A') != 5 or any(v[2] not in 'AM' for v in CHANGED.values()): sys.exit(1)
ALLOWED_EXACT = {D + 'docs/openapi/secuura-api.yaml', D + 'docs/VOCABULARY.md'}
outside = [p for p in CHANGED if not (p.startswith(A) or p in ALLOWED_EXACT)]
print('outside services/anchoring/** + yaml + VOCABULARY.md:', outside, '(want [])')
if outside: sys.exit(1)
# the develop blob of each of the 12 must be UNCHANGED by the three squashes (the squash paths are disjoint from the 12)
SQPATHS = out('diff', '--name-only', BASE, DEV).strip().splitlines()
print('squash paths', len(SQPATHS), [x.split('/')[-1] for x in SQPATHS], '| overlap with the 12:', sorted(set(SQPATHS) & set(CHANGED)), '(want [])')
if len(SQPATHS) != 4 or set(SQPATHS) & set(CHANGED): sys.exit(1)
for p_ in CHANGED:
    b_dev = git('rev-parse', '-q', '--verify', DEV + ':' + p_).stdout.strip() or 'ABSENT'
    if b_dev != CHANGED[p_][0]: print('REFUSING: develop blob of', p_, 'changed by the squashes', b_dev, CHANGED[p_][0]); sys.exit(1)
print('the 12 develop-side blobs identical at BASE and at develop 778e6cfe2: True')
SQBLOB = {p_: out('rev-parse', DEV + ':' + p_).strip() for p_ in SQPATHS}
if any(v[3] != '100644' for v in CHANGED.values()): print('REFUSING: a non-100644 mode'); sys.exit(1)
PINNED = {  # the drafter's shape_1.out reads, asserted against the live objects
  D + 'docs/VOCABULARY.md': ('7b7072b4e1da', '75633ef85930'), D + 'docs/openapi/secuura-api.yaml': ('a34b59363b81', '1871025e2c11'),
  A + 'src/__tests__/anchorSchema.test.ts': ('c1a3e865a101', '570d21683504'), A + 'src/__tests__/ks1175-anchor-readback.test.ts': ('ABSENT', '05793d925400'),
  A + 'src/__tests__/ks1175-identity-anchoring.test.ts': ('ABSENT', 'c3f430d783ba'), A + 'src/__tests__/ks1284-cardano-metadatum.test.ts': ('ABSENT', '33cf6608e6a4'),
  A + 'src/anchorReadback.ts': ('ABSENT', 'f49ffb6afaaf'), A + 'src/anchorSchema.ts': ('8341c8221b50', 'af95458d00b7'), A + 'src/anchoring.openapi.ts': ('29c089bb0abc', '5d0a1b9eb19b'),
  A + 'src/cardano/cardanoMetadatum.ts': ('ABSENT', 'aaaec6c63655'), A + 'src/cardano/transaction.ts': ('3a86936bef0b', 'e047630ea004'), A + 'src/index.ts': ('da4abd432921', 'b6386f402a4b')}
for p, (b1, b2) in PINNED.items():
    if p not in CHANGED or not CHANGED[p][0].startswith(b1) or not CHANGED[p][1].startswith(b2): print('REFUSING: pinned blob disagrees for', p, CHANGED.get(p)); sys.exit(1)
print('the 12 pinned (develop blob, head blob) pairs agree with the live objects: True')
# unchanged paths the gate reads or runs: same blob at develop and head
UNCHANGED = [A + 'package.json', A + 'package-lock.json', A + 'tsconfig.json', A + 'vitest.config.ts', A + 'src/verifyAnchorStatus.ts',
             A + 'src/__tests__/ks480-provenance-exclusion.test.ts', A + 'src/__tests__/ks566-connector-attribution.test.ts',
             A + 'src/__tests__/threadTokenMint.test.ts', A + 'src/__tests__/db.retry.test.ts', A + 'src/cardano/provider.ts', A + 'src/cardano/wallet.ts',
             D + 'package.json', D + 'package-lock.json', D + 'eslint.config.mjs', 'BACKLOG.md', '.githooks/pre-push',
             D + 'scripts/generate-openapi.ts', D + 'scripts/spec-examples/check-spec-examples.mjs', D + 'scripts/preflight/preflight.sh',
             D + 'services/originate/src/routes/documents.ts', D + 'services/originate/src/routes/anchors.ts',
             D + 'services/api-gateway/src/routes/proxy.ts', D + 'services/api-gateway/src/routes/verification.ts']
UBLOB = {}
for p in UNCHANGED:
    b1 = out('rev-parse', DEV + ':' + p).strip(); b2 = out('rev-parse', HEAD + ':' + p).strip()
    if b1 != b2 or not re.fullmatch(r'[0-9a-f]{40}', b1): print('REFUSING: unchanged-read path differs or missing', p, b1, b2); sys.exit(1)
    UBLOB[p] = b1
print('unchanged-read paths', len(UNCHANGED), 'all same blob at develop and head: True')
# CSL pin in both lockfiles at both trees; one yaml hunk
for tree in (DEV, HEAD):
    for lock in (A + 'package-lock.json', D + 'package-lock.json'):
        txt = out('show', tree + ':' + lock)
        m = re.search(r'"node_modules/@emurgo/cardano-serialization-lib-nodejs": \{\s*"version": "([^"]+)"', txt)
        if not m or m.group(1) != '15.0.3': print('REFUSING: CSL pin', tree[:9], lock, m and m.group(1)); sys.exit(1)
print('CSL 15.0.3 pinned in both lockfiles at develop and head: True')
hunks = out('diff', BASE, HEAD, '--', D + 'docs/openapi/secuura-api.yaml').count('\n@@')
print('yaml hunks', hunks, '(want 1)')
if hunks != 1: sys.exit(1)
# BACKLOG.md line of the threadTokenMint entry at develop (the drafter's lead D1)
bl = out('show', BASE + ':BACKLOG.md').splitlines()
assert out('rev-parse', DEV + ':BACKLOG.md') == out('rev-parse', BASE + ':BACKLOG.md')
tl = [i + 1 for i, l in enumerate(bl) if 'threadTokenMint.test.ts` fails on develop' in l]
print('BACKLOG.md threadTokenMint entry at develop: lines', tl, '| :155 is', bl[154][:60])

# 2b. the MERGED TREE re-derived WITHOUT any git write: develop's tree with the 12 head entries composed in, hashed in Python from
# `git ls-tree` reads; must equal the scratch-clone 3-way merge (predict_merge_scratch.out). Control: composing the 12 into BASE's tree = the head tree.
def ls_tree(oid):
    ents = []
    for l in out('ls-tree', oid).strip().splitlines():
        meta, name = l.split('\t', 1); mode, typ, sha = meta.split()
        ents.append([mode, typ, sha, name])
    return ents
def hash_tree(ents):
    def key(e): return e[3] + ('/' if e[1] == 'tree' else '')
    # git stores the mode WITHOUT the leading zero that ls-tree prints (040000 -> 40000)
    body = b''.join((e[0].lstrip('0') + ' ' + e[3]).encode() + b'\0' + bytes.fromhex(e[2]) for e in sorted(ents, key=key))
    return hashlib.sha1(b'tree ' + str(len(body)).encode() + b'\0' + body).hexdigest()
def compose(tree_oid, changes):
    ents = ls_tree(tree_oid)
    for e in ents:
        assert hash_tree(ls_tree(e[2])) == e[2] if e[1] == 'tree' and e[3] in {c.split('/', 1)[0] for c in changes} else True
    groups = {}
    for path, (mode, blob) in changes.items():
        top, rest = (path.split('/', 1) + [None])[:2]
        groups.setdefault(top, {})[rest] = (mode, blob)
    byname = {e[3]: e for e in ents}
    for top, sub in groups.items():
        if None in sub:
            mode, blob = sub[None]
            if top in byname: byname[top][0], byname[top][2] = mode, blob
            else: ents.append([mode, 'blob', blob, top]); byname[top] = ents[-1]
        else:
            byname[top][2] = compose(byname[top][2], sub)
    return hash_tree(ents)
ctrl = hash_tree(ls_tree(DEV_TREE)); print('tree-hash control: re-hashing develop root tree ->', ctrl[:9], '==', DEV_TREE[:9], ctrl == DEV_TREE)
if ctrl != DEV_TREE: sys.exit(1)
twelve = {p_: (v[3], v[1]) for p_, v in CHANGED.items()}
ff = compose(BASE_TREE, twelve); print('CONTROL compose(the 12 into BASE tree) ->', ff[:9], '== head tree', ff == HEAD_TREE)
if ff != HEAD_TREE: sys.exit(1)
mt = compose(DEV_TREE, twelve); print('compose(the 12 into develop 778e6cfe2 tree) ->', mt, '== MERGED_TREE', mt == MERGED_TREE)
if mt != MERGED_TREE: sys.exit(1)
pm = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'predict_merge_scratch.out')).read()
print('predict_merge_scratch.out names MERGED TREE', MERGED_TREE, ':', ('MERGED TREE ' + MERGED_TREE) in pm, '| clean rc=0:', 'x head rc=0' in pm, '| both orders same:', 'same: True' in pm, '| 12 head blobs + 4 squash blobs:', 'carry the head blobs: True' in pm and "carry develop's blobs: True" in pm)
if not (('MERGED TREE ' + MERGED_TREE) in pm and 'x head rc=0' in pm and 'same: True' in pm): sys.exit(1)

# 3. the launcher
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets'
BRIEF = GS + '/2026-09-20_gate1105_READY_seatA15.txt'
STATUS = GS + '/2026-09-20_gate1105_STATUS2_seatA15.txt'
PROMPT = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-20_secuura-1105.prompt.txt'
REPORT = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-pr1105-tier1-r1/'
PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1100-1101-tier1-r1/'
EXEMPLAR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks1215-1034-e4624218b-tier1-r1/'
INDEXTS = A + 'src/index.ts'
def jline(path, ok, landed):
    short = path.replace(D, '')
    return '  %-84s (%s, %s),' % ('"' + path + '":', '{"%s": DV}' % ok, ('{"%s": "#1105 own"}' % landed) if landed else '{}')
judged = []
for p, (b1, b2, st, m) in CHANGED.items():
    judged.append(jline(p, b1, b2))
for p in UNCHANGED:
    judged.append(jline(p, UBLOB[p], ''))
for p in SQPATHS:  # the three squashes' paths, at their develop blobs (what the merged tree carries)
    judged.append(jline(p, SQBLOB[p], ''))
JUDGED_BLOCK = '\n'.join(judged)
# the by-name keyword ladder (exit 33): one or more exact phrases per item, all must be in the prompt
BYNAME = [
 ('1', ['parent of e02d3ecb5 is dc061f2bb', 'two instruments']),
 ('2', ['red by ASSERTION', 'red by MODULE ABSENCE', 'TWO DIFFERENT KINDS OF RED', 'BACKLOG.md:155', 'threadTokenMint']),
 ('3', ['tampers/tampers.json', 'T3b', '0 red', 'FINDING to re-measure and grade', 'WHOLE anchoring suite']),
 ('4', ['BYTE-IDENTICAL NO-OP', 'UTF-8 BYTES ON CODE-POINT BOUNDARIES', 'STRADDLING byte 64', '"true"/"false"', 'FLOATS / NULL are rejected UPSTREAM']),
 ('5', ['VERIFY-BY-HASH ORDER', 'REORDERED copy', 'prove the check can fail']),
 ('6', ['DECIDE 2 superRefine', 'MEASURE the anchored key set']),
 ('7', ['WHITELIST / STRIP', 'smuggled', 'ks566 ×6', '!== undefined']),
 ('8', ['GET /api/anchors/verify/:hash', 'GET /api/anchors/:id', 'buildVerifyResponse', 'byte-for-byte', 'DIFF IT']),
 ('9', ['check:openapi', 'check:spec-examples', 'ONE FlatAnchorRequest hunk', 'MASKED', '405']),
 ('10', ['FILES API', 'CSL 15.0.3', 'no migration', 'no dependency change']),
 ('11', ['SEVEN-not-six', 'documents.ts:1263-1285', 'anchors.ts:282-297']),
 ('12', ['3 SKIPPED', 'NOT RUN, never as passes', ':6882']),
 ('13', ['NOT DONE ITEMS (six)', '21af3285-0a40-490c-bfff-bc3466b6066b', '4999', 'BY LENGTH ONLY']),
 ('14', ['NOT-PINNED', 'one-line tamper', "local model's next feed", 'proposed cell']),
 ('15', ['DKIM-VERIFY', 'NOT-TESTED.written-first.md', 'census', 'GO / GO WITH FINDINGS / NO GO', 'Majors/Minors', 'prediction slips named BY NAME']),
]
def shq(kw):  # a keyword with an apostrophe is double-quoted (none carries $, a backtick or a backslash — asserted)
    assert not re.search(r'[$`\\]', kw), kw
    return ('"' + kw + '"') if "'" in kw else ("'" + kw + "'")
BYNAME_GREP = ' && '.join('grep -qF -- %s "$PROMPT_FILE"' % shq(kw) for _, kws in BYNAME for kw in kws)
# the seat items BOTH the READY and the prompt must carry (exit 30) — the builder's own figures and words
BOTH = ['318 / 319', '242', '293', '247 / 46', 'T1', 'T2a', 'T2b', 'T3a', 'T3b', 'T3c', 'T4', 'T5', 'T6', '0 red', '21af3285-0a40-490c-bfff-bc3466b6066b', '4999/4999',
        'CSL 15.0.3', 'dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa', ':6882', ':5432', 'BACKLOG.md:155', '+65', '405', 'documents.ts:1263-1285', 'anchors.ts:282-297',
        'transaction.ts:107', 'SEVEN', 'login_stub', '12/15', 'SKIPPED', 'threadTokenMint', 'R8', 'R9', 'MODULE ABSENCE', 'superRefine', 'NOT DONE']
BOTH_GREP = ' && '.join('grep -qF -- %s "$PROMPT_FILE" && grep -qF -- %s "$BRIEF"' % (("'" + t + "'"), ("'" + t + "'")) for t in BOTH)

L = r'''#!/bin/bash
# launch_qa_secuura_1105.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over ONE Secuura/Blockchain PRODUCT PR
#   #1105 KS-1175 (+ KS-1284 codec, Refs KS-721) @ e02d3ecb5 — the KS-1175 REAL FIX: the flat-anchor schema accepts a top-level `identity` block
#   (seven non-PII fields + identityCommitment), the KS-1284 Cardano metadatum codec at the ONE tx-build attach point and its inverse at the
#   verify-by-hash chain read, two read-backs (GET /api/anchors/verify/:hash metadata.identity; GET /api/anchors/:id identityCommitment + identity),
#   the regenerated OpenAPI yaml (ONE FlatAnchorRequest hunk) and VOCABULARY.md §2. Raised by Seat A 15th, READY 2026-09-20T13:55:07Z.
# TIER 1: it changes the schema of what goes on the immutable Cardano record. Round 1 of 2 (Kam 2026-09-05 cap). ONE verdict.
# 12 files +1084/-64, ALL under Blockchain/Dev/services/anchoring/** except docs/openapi/secuura-api.yaml and docs/VOCABULARY.md (generator: local
# objects AND the PR files API, gh_pr_reads.out); 5 ADDED (absent at develop), 7 MODIFIED, 0 deleted; no migration / config / dependency (CSL 15.0.3
# pinned in both lockfiles at both trees, generator-read).
# EVERY VALUE HERE IS THE BUILDER'S MEASUREMENT RE-DERIVED BY THE DRAFTER, never adopted: the head, its parent, its tree, the 12 blob pairs, the
# unchanged-read blobs, the CSL pin, the one yaml hunk — all re-read from origin + local objects by gen_launcher_1105.py at generation.
# NAMESPACE TRAP: KS-1105 is a real, unrelated ticket (Backlog, 0 attachments at 14:03Z); PR #1105 is KS-1175. The READY mail AND the prompt must
# BOTH state it, or the launch refuses (exit 32).
# MERGE AUTHORITY: WEDNESDAY'S signed GO naming e02d3ecb5 (exit 26). THE DEPLOY AND THE ANCHOR ARE KAM'S — the gate rules nothing about either.
#
# THE SHAPE, re-read live by the generator (git ls-remote develop + refs/pull/1105/head + the branch; rev-list --parents; diff --raw): the head is
# ONE commit whose parent IS dc061f2bb (tree 1ccb80e0d = the #1100-#1101 batch gate's both-PRs tree, landed); head tree 8f066a817. DEVELOP MOVED
# after the READY: origin develop = 778e6cfe2 (tree d0c8bfd09) = dc061f2bb + THREE squashes by Seat B 10th on Wednesday's GO (6e2fbc234 KS-1275 #1102,
# 3232656cb KS-1203 #1103, 778e6cfe2 KS-1272 #1104), touching 4 paths DISJOINT from the 12 (originate lifecycleEventRepo.test.ts, api-gateway
# ks501 test, startup-migrations.ts + ks1272 test). So the merge is NOT a fast-forward: MERGED TREE 1f2bc512a, predicted by a REAL 3-way merge in a
# --shared --no-checkout scratch clone (both orders, clean rc 0, predict_merge_scratch.out) AND re-derived by pure tree hashing in the generator;
# compare develop...head = merge_base dc061f2bb, ahead 1, BEHIND 3, files 12 (exit 10 — a fourth squash changes the figure and refuses).
#
# The develop pin is judged by CONTENT — THIRTY-NINE paths by blob at the CURRENT develop: the 12 PR paths (7 at develop blobs, 5 ABSENT; any at its
# head blob -> exit 19 LANDED), the 4 squash paths at their 778e6cfe2 blobs, and what the gate runs or reads: anchoring package.json + lock + tsconfig + vitest.config, verifyAnchorStatus.ts,
# the control test files (ks480, ks566, threadTokenMint, db.retry), cardano/provider.ts + wallet.ts, the Dev package.json + lock, eslint.config.mjs,
# BACKLOG.md, the pre-push hook, generate-openapi.ts, check-spec-examples.mjs, preflight.sh, originate documents.ts + anchors.ts (the SEVEN-endpoint
# count), api-gateway proxy.ts + verification.ts (NOT DONE 2).
# GUARDED: services/anchoring/, docs/openapi/, docs/VOCABULARY.md, scripts/, packages/shared src/, .githooks/, the Dev package.json + lock,
# eslint.config.mjs, BACKLOG.md, the two originate route files, the two api-gateway route files, api-gateway startup-migrations.ts.
#
# SOURCE = gatesets/2026-09-20_gate1105_READY_seatA15.txt (the READY, 13:55:07Z) + gatesets/2026-09-20_gate1105_STATUS2_seatA15.txt (STATUS 2,
# 13:51:06Z), both captured verbatim by Wednesday from wednesday-agent@ and re-listed by message id by the drafter (list_ready_mail.out).
#
# exit 6:  the head is not at its branch AND at refs/pull/1105/head on origin.
# exit 7:  the prompt must carry 'TIER 1' AND the PR's own tier line '#1105 KS-1175: TIER 1'.
# exit 20: the READY mail AND the prompt must name the head in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and the three verdict words.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (the #1100-#1101 batch, whose both-PRs tree IS this develop), the EXEMPLAR
#          REPORT (the ks1215 #1034 single-PR product gate) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO naming e02d3ecb5 as the merge authority, with no Kam-tap and no "not ... alone" condition.
# exit 27: the READY mail AND the prompt must BOTH carry the builder's own words: 'PREFLIGHT', '12/15', 'login_stub', 'SKIPPED', 'threadTokenMint'.
# exit 28: the prompt must forbid entering any seat worktree (s-a15-ks1175) and writing in the builder's 2026-09-20_seatA-15th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201).
# exit 30: the READY mail AND the prompt must BOTH carry the builder's items (the counts 318/319, 242, 293, 247/46; T1-T6 and T3b's '0 red'; the
#          facts comment id and 4999/4999; CSL 15.0.3; develop in full; :6882 and :5432; BACKLOG.md:155; the +65 hunk and 405 blocks; the two
#          originate line ranges; transaction.ts:107; SEVEN; R8/R9 by MODULE ABSENCE; superRefine; NOT DONE), and the prompt must ask the gate to
#          MEASURE, not conclude, and to RULE WHETHER IT BLOCKS.
# exit 31: the prompt must name the MERGED tree 1f2bc512a in full AND develop 778e6cfe2 in full, the NOT-PINNED list with a proposed cell per row, and a loopback GATEWAY_URL for any
#          preflight run.
# exit 32: the READY mail AND the prompt must BOTH state that PR #1105 is KS-1175 (KS-1105 is another ticket).
# exit 33: the prompt must carry Wednesday's FIFTEEN BY-NAME items, each by its own keywords (see the ladder below): head/base re-read by two
#          instruments; red-first as TWO kinds of red; the six tampers with T3b's 0 red as a finding; the codec's four (no-op, UTF-8 bytes straddling
#          64, booleans as strings, floats/null upstream); the verify-by-hash order with the reorder control; DECIDE 2; whitelist/strip; the two
#          read-backs with the byte-for-byte diff; the spec (check:openapi, one hunk, 405, masked); nothing outside the allowed paths / no
#          dependency change; SEVEN-not-six; the 3 SKIPPED legs NOT RUN; the six NOT DONE with the facts comment by id by length only; NOT-PINNED
#          as the local model's feed; the standard closing (DKIM, NOT-TESTED first, census, the verdict words, Majors/Minors, slips by name).
# QAB1105_CUR_DEV (test override, --check only): stands in for origin develop. QAB1105_HEAD (test override): stands in for the pinned head.
# QAB1105_INDEXTS_FILE (test fixture, --check only): a local file stands in for develop services/anchoring/src/index.ts (its git blob).
# A launch with any QAB1105_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-20_gate1105/gen_launcher_1105.py in the shape of launch_qa_secuura_batch1100_1101.sh (pins re-read from origin +
# local objects + output controls + heredoc parity + bash -n).
#
# Usage: launch_qa_secuura_1105.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..33 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1105_BRIEF:-__BRIEF__}"
STATUS2="__STATUS__"
PROMPT_FILE="${QAB1105_PROMPT:-__PROMPT__}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket|branch|head — pinned from the builder's READY (13:55:07Z) and re-read by the drafter (git ls-remote 13:59:46Z and 14:13:57Z, branch AND
# refs/pull/1105/head; the pulls API 14:03:26Z; re-pinned to the MOVED develop at 14:27:16Z). NAMESPACE TRAP: KS-1105 is another ticket; the ticket column is the truth (exit 32)
PRS=(
  "1105|KS-1175|__BRANCH__|${QAB1105_HEAD:-__HEAD__}"
)
DEVELOP_SHA='__DEV__'   # the pin = develop at 14:27:16Z (MOVED off dc061f2bb by the three squashes)
MERGE_BASE='__BASE__'    # the head's parent = merge-base = the develop the builder READY'd against
HEAD_TREE='__HEADTREE__'     # the head tree; over dc061f2bb it was a fast-forward
MERGED_TREE='__MERGEDTREE__'  # the predicted 3-way merge over the pin (scratch clone, both orders, clean; generator tree-hash)
REPORT_DIR='__REPORT__'
PRIOR_REPORT='__PRIOR__'
EXEMPLAR_REPORT='__EXEMPLAR__'
REAL_BRIEF="__BRIEF__"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief (READY capture) missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$STATUS2" ]        || { echo "STATUS 2 capture missing or empty: $STATUS2" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head, pinned at its branch AND at refs/pull/1105/head on origin (one ls-remote). A moved head refuses the launch: re-pin.
HEADS_NOTE=""
for _pr in "${PRS[@]}"; do
  IFS='|' read -r _n _t _br _h <<< "$_pr"
  _lsr="$(git -C "$REPO" ls-remote origin "$_br" "refs/pull/$_n/head")"
  if ! printf '%s\n' "$_lsr" | grep -q "^${_h}[[:space:]]${_br}\$" || ! printf '%s\n' "$_lsr" | grep -q "^${_h}[[:space:]]refs/pull/${_n}/head\$"; then
    echo "REFUSING: #$_n $_t — $_h is not at $_br AND refs/pull/$_n/head on origin — that head moved; a verdict is valid ONLY at its head" >&2
    printf '%s\n' "$_lsr" >&2
    exit 6
  fi
  HEADS_NOTE="$HEADS_NOTE #$_n@${_h:0:9}"
done

# The compare (GitHub compare API), asserted whole (merge_base + ahead + files; NOT behind — develop is expected to move):
# develop...head = merge_base dc061f2bb ahead 1 BEHIND 3 files 12 (git rev-list --left-right, drafter 14:27Z; the launcher reads the compare API).
COMPARE="$(
  set -a; . "$SECUURA_ENV"; set +a
  PRS_FLAT="${PRS[*]}" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/"
for pr in os.environ["PRS_FLAT"].split():
    n, tk, br, h = pr.split("|")
    r = urllib.request.urlopen(urllib.request.Request(api + "develop..." + h, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60)
    c = json.load(r)
    print("%s %s ahead=%d behind=%d files=%d" % (n, c["merge_base_commit"]["sha"], c["ahead_by"], c["behind_by"], len(c.get("files") or [])))
PY
)"
[ -n "$COMPARE" ] || { echo "REFUSING: could not read the compare develop...head from the GitHub compare API" >&2; exit 13; }
WANT_COMPARE="1105 $MERGE_BASE ahead=1 behind=3 files=12"
[ "$COMPARE" = "$WANT_COMPARE" ] || { echo "REFUSING: develop...head compare read" >&2; printf '%s\n' "$COMPARE" >&2; echo "the gateset pins" >&2; printf '%s\n' "$WANT_COMPARE" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): thirty-nine paths by PATH BLOB at the CURRENT develop (no region judgement), then — if
# develop moved — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).
CUR_DEV="${QAB1105_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
DEV_JUDGEMENT="$(
  set -a; . "$SECUURA_ENV"; set +a
  DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" MERGED_TREE="$MERGED_TREE" python3 - <<'PYJ'
import hashlib, json, os, sys, urllib.request, urllib.error
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]; merged_tree = os.environ["MERGED_TREE"]
D = "Blockchain/Dev/"
A = D + "services/anchoring/"
INDEXTS = A + "src/index.ts"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop
JUDGED = {
__JUDGED__
}
# No REGION judgement: every path is judged by exact blob (a develop move of any judged path refuses, exit 18; the PR head blob, exit 19).
state = []
for f, (ok, landed) in JUDGED.items():
    fixture = os.environ.get("QAB1105_INDEXTS_FILE", "") if f == INDEXTS else ""
    try:
        if fixture:
            data = open(fixture, "rb").read()
            blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        else:
            blob = get("/contents/" + f + "?ref=" + cur)["sha"]
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print("UNJUDGEABLE develop blob unreadable for " + f.split("/")[-1] + ": HTTP " + str(e.code)); sys.exit(0)
        blob = "ABSENT"
    except Exception as e:
        print("UNJUDGEABLE develop blob unreadable for " + f.split("/")[-1] + ": " + type(e).__name__); sys.exit(0)
    short = f.replace(D, "")
    if blob in landed:
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — that PR has landed; this gateset is stale"); sys.exit(0)
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (dc061f2bb + three squashes; merge-base dc061f2bb; predicted merged tree " + merged_tree + " by a real 3-way merge, both orders, clean; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [A,
           D + "docs/openapi/",
           D + "docs/VOCABULARY.md",
           D + "scripts/",
           D + "packages/shared/src/",
           ".githooks/",
           D + "package.json",
           D + "package-lock.json",
           D + "eslint.config.mjs",
           "BACKLOG.md",
           D + "services/originate/src/routes/documents.ts",
           D + "services/originate/src/routes/anchors.ts",
           D + "services/api-gateway/src/routes/proxy.ts",
           D + "services/api-gateway/src/routes/verification.ts",
           D + "services/api-gateway/src/startup-migrations.ts"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: EMPTY. Nothing is pre-cleared for this gate; any GUARDED move refuses: re-pin deliberately.
DEV_CONTENT_ALLOWED = {}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") in DEV_CONTENT_ALLOWED[h])
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto the head in its own clone, names the merged-tree OID (drafter over the pin: 1f2bc512a) and re-runs every item and suite on it"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list (services/anchoring/, docs/openapi/, VOCABULARY.md, scripts/, packages/shared src/, .githooks/, the Dev package.json + lock, eslint.config.mjs, BACKLOG.md, the two originate and two api-gateway route files, startup-migrations.ts); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA / JUDGED blobs + prompt)" >&2
     exit 18 ;;
esac
grep -qF 'TIER 1' "$PROMPT_FILE" && grep -qF '#1105 KS-1175: TIER 1' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry TIER 1 and the PR's own tier line (#1105 KS-1175: TIER 1)" >&2; exit 7; }
grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: prompt does not name ROUND 1" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" && grep -qF "$STATUS2" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the READY and STATUS 2 capture paths" >&2; exit 9; }
for _pr in "${PRS[@]}"; do
  IFS='|' read -r _n _t _br _h <<< "$_pr"
  grep -qF "$_h" "$PROMPT_FILE" && grep -qF "$_h" "$BRIEF" \
    || { echo "REFUSING: the READY mail or the prompt does not name #$_n's head $_h — a gate about another SHA is another gate" >&2; exit 20; }
done
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict" >&2; exit 12; }
grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid pushing / running the hook in the real checkout" >&2; exit 11; }
grep -qi 'no memory maintenance' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid memory maintenance inside the gate session" >&2; exit 14; }
grep -qi 'NEVER print a credential value' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }
grep -qi 'node_modules per ENTRY' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require node_modules farmed per ENTRY (a wholesale link can write through to the checkout .vite cache)" >&2; exit 22; }
grep -qF '[QA/Secuura-1105 -> Wednesday] TIER 1 GATE #1105 (KS-1175 + KS-1284) @ e02d3ecb5' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'GO, GO WITH FINDINGS, or NO GO' "$PROMPT_FILE" && grep -qF 'Majors <n> / Minors <m>' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact verdict subject, coagent@ / wednesday-agent@, the three verdict words and Majors / Minors" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$EXEMPLAR_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the EXEMPLAR REPORT $EXEMPLAR_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'ONE MERGE ADDENDUM line' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry ONE MERGE ADDENDUM line and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming e02d3ecb5" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming e02d3ecb5 as the merge authority, or carries a Kam-tap / not-alone condition" >&2; exit 26; }
grep -qF 'PREFLIGHT' "$PROMPT_FILE" && grep -qF -- '12/15' "$PROMPT_FILE" && grep -qF -- '12/15' "$BRIEF" && grep -qF 'login_stub' "$PROMPT_FILE" && grep -qF 'login_stub' "$BRIEF" && grep -qF 'SKIPPED' "$PROMPT_FILE" && grep -qF 'SKIPPED' "$BRIEF" && grep -qF 'threadTokenMint' "$PROMPT_FILE" && grep -qF 'threadTokenMint' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the builder's words: PREFLIGHT / 12/15 / login_stub / SKIPPED / threadTokenMint" >&2; exit 27; }
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF 's-a15-ks1175' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-20_seatA-15th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree (s-a15-ks1175) and writing in the builder's 2026-09-20_seatA-15th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener the gate starts ended by pid with a census (KS-1201)" >&2; exit 29; }
__BOTH_GREP__ && grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the builder's items, or the prompt does not say MEASURE, not conclude and RULE WHETHER IT BLOCKS" >&2; exit 30; }
grep -qF "$MERGED_TREE" "$PROMPT_FILE" && grep -qF "$DEVELOP_SHA" "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'proposed cell' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the merged tree 1f2bc512a and develop 778e6cfe2 in full, the NOT-PINNED list with a proposed cell per row, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
grep -qF 'PR #1105 is KS-1175.' "$PROMPT_FILE" && grep -qF 'KS-1105' "$PROMPT_FILE" && grep -F 'PR #1105' "$BRIEF" | grep -qF 'KS-1175' \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH state that PR #1105 is KS-1175 (KS-1105 is another ticket) — the PR number is another ticket's number too" >&2; exit 32; }
__BYNAME_GREP__ && grep -qF -- 'round 1 of 2' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not carry Wednesday's fifteen by-name items (head/base by two instruments; red-first as TWO kinds of red; the six tampers with T3b's 0 red as a finding; the codec's four; the verify-by-hash order with the reorder control; DECIDE 2; whitelist/strip; the two read-backs with the byte-for-byte diff; the spec; nothing outside the allowed paths; SEVEN-not-six; the 3 SKIPPED legs NOT RUN; the six NOT DONE with the facts comment by length only; NOT-PINNED as the local model's feed; the standard closing) or round 1 of 2" >&2; exit 33; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  the head on origin (branch AND refs/pull/1105/head):$HEADS_NOTE"
  echo "  compare (GitHub API), develop...head:"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY + STATUS 2 captures, prompt, QA project and repo all present"
  echo "  prompt carries TIER 1 and the PR tier line (#1105 KS-1175: TIER 1); names ROUND 1"
  echo "  prompt opens with the thinking directive and names both mail captures"
  echo "  READY mail and prompt both name the head in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact verdict subject, coagent@ sender, wednesday-agent@ recipient, the three verdict words, Majors / Minors"
  echo "  prompt names the report directory, the #1100-#1101 PRIOR REPORT, the ks1215 EXEMPLAR REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries ONE MERGE ADDENDUM line and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming e02d3ecb5; no Kam-tap or not-alone condition"
  echo "  READY mail and prompt BOTH carry: PREFLIGHT / 12/15 / login_stub / SKIPPED / threadTokenMint"
  echo "  prompt forbids any seat worktree (s-a15-ks1175) and the builder's 2026-09-20_seatA-15th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201)"
  echo "  READY mail and prompt BOTH carry the builder's items; the prompt says MEASURE, not conclude, and RULE WHETHER IT BLOCKS"
  echo "  prompt names the merged tree 1f2bc512a and develop 778e6cfe2 in full, the NOT-PINNED list with a proposed cell per row and a loopback GATEWAY_URL"
  echo "  READY mail and prompt BOTH state that PR #1105 is KS-1175 (namespace trap; KS-1105 is another ticket)"
  echo "  prompt carries Wednesday's fifteen by-name items and round 1 of 2"
  [ -n "${QAB1105_CUR_DEV:-}" ] && echo "  (develop read from the QAB1105_CUR_DEV test override, not ls-remote)"
  [ -n "${QAB1105_INDEXTS_FILE:-}" ] && echo "  (develop services/anchoring/src/index.ts read from the QAB1105_INDEXTS_FILE fixture, not the contents API)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1105_BRIEF:-}${QAB1105_PROMPT:-}${QAB1105_HEAD:-}${QAB1105_CUR_DEV:-}${QAB1105_INDEXTS_FILE:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
'''
s = L
SUBS = {'__BRIEF__': BRIEF, '__STATUS__': STATUS, '__PROMPT__': PROMPT, '__BRANCH__': BRANCH, '__HEAD__': HEAD, '__DEV__': DEV, '__BASE__': BASE, '__HEADTREE__': HEAD_TREE, '__MERGEDTREE__': MERGED_TREE,
        '__REPORT__': REPORT, '__PRIOR__': PRIOR, '__EXEMPLAR__': EXEMPLAR, '__JUDGED__': JUDGED_BLOCK, '__BOTH_GREP__': BOTH_GREP, '__BYNAME_GREP__': BYNAME_GREP}
for k, v in SUBS.items():
    n = s.count(k)
    if n == 0: print('REFUSING: token absent', k); sys.exit(1)
    s = s.replace(k, v)
if re.search(r'__[A-Z]+__', s): print('REFUSING: residual token', re.findall(r'__[A-Z]+__', s)); sys.exit(2)
# 4. output controls: every carried value present as often as intended
# counts explained (run1): HEAD full only in PRS (the header, exit 26 and the subject use the short form); DEV full in DEVELOP_SHA + the BOTH grep x2;
# exit 18 = PYJ comment + empty-CUR_DEV refusal + case; exit 32 = 3 header mentions + code; QAB1105_HEAD = header + PRS + launch guard;
# 'PR #1105 is KS-1175.' = header NAMESPACE line + the exit-32 grep.
want = {HEAD: 1, DEV: 1, BASE: 3, HEAD_TREE: 1, MERGED_TREE: 1, 'behind=3': 1, 'startup-migrations.ts': 5, BRIEF: 2, STATUS: 1, PROMPT: 1, REPORT: 1, PRIOR: 1, EXEMPLAR: 1, 'exit 6': 2, 'exit 10': 2, 'exit 19': 3, 'exit 18': 3,
        'exit 30': 2, 'exit 32': 4, 'exit 33': 2, 'exit 16': 3, 'exit 21': 3, '[ -t 0 ]': 1, 'exec claude --dangerously-skip-permissions': 1, 'DEV_CONTENT_ALLOWED = {}': 1,
        ': DV}': 39, '"ABSENT": DV': 5, '"#1105 own"': 12, 'QAB1105_CUR_DEV': 5, 'QAB1105_INDEXTS_FILE': 5, 'QAB1105_HEAD': 3, 'refs/pull/$_n/head': 2,
        'ahead=1 behind=3 files=12': 1, "[QA/Secuura-1105 -> Wednesday] TIER 1 GATE #1105 (KS-1175 + KS-1284) @ e02d3ecb5": 1, 'PR #1105 is KS-1175.': 2}
got = {k: s.count(k) for k in want}
bad = {k: (got[k], want[k]) for k in want if got[k] != want[k]}
print('output controls', {(k[:28] + '…' if len(k) > 28 else k): v for k, v in got.items()})
if bad: print('REFUSING: output control mismatch (got, want)', bad); sys.exit(1)
for kw in [kw for _, kws in BYNAME for kw in kws] + BOTH:
    if s.count(kw) < 1: print('REFUSING: ladder keyword missing from launcher', kw); sys.exit(1)
print('by-name ladder keywords', sum(len(k) for _, k in BYNAME), 'across 15 items; BOTH-list tokens', len(BOTH))
# heredoc parity (the PYJ block sits inside $( ) — apostrophes and parens must be even)
for tag in ("<<'PY'\n", "<<'PYJ'\n"):
    i = s.index(tag); end = s.index('\n' + tag[3:-2] + '\n', i)
    blk = s[i:end]
    print('heredoc', tag.strip(), '@', s.count('\n', 0, i) + 1, 'apostrophes', blk.count("'") - 2, 'parens (', blk.count('('), ')', blk.count(')'))
    if (blk.count("'") - 2) % 2 or blk.count('(') != blk.count(')'): print('REFUSING: heredoc parity'); sys.exit(1)
tmp = tempfile.NamedTemporaryFile('w', delete=False, suffix='.sh', dir=os.path.dirname(OUT)); tmp.write(s); tmp.close()
p = subprocess.run(['bash', '-n', tmp.name], capture_output=True, text=True); print('bash -n rc', p.returncode, p.stderr.strip()[:300])
if p.returncode: print('REFUSING: bash -n; the tmp file is left for reading at', tmp.name); sys.exit(3)
os.replace(tmp.name, OUT); os.chmod(OUT, 0o755)
print('written', OUT, 'mode', oct(os.stat(OUT).st_mode & 0o777), 'sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))
