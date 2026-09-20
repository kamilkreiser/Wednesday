#!/usr/bin/env python3
"""shape_1.py — READ-ONLY local object reads in the Secuura checkout (cat-file / rev-list / rev-parse / diff --raw / diff --numstat / ls-tree):
each of the seven heads is ONE commit whose parent is develop 362e51fe0 (the seat's base = origin develop NOW — no develop move this round, so
each PR over develop is a FAST-FORWARD and its merged tree IS its head tree); head trees vs the seat's GROUPING; the changed paths per PR with
(develop blob | ABSENT, head blob, status, mode); pairwise disjointness of the union (11 paths, 21 pairs); every path under __tests__/; numstat
per PR (0 deletions everywhere — test-only); the develop blobs of the ten tamper files; the seven heads' file lists vs the GROUPING table.
Nothing written to the checkout. Derived from gatesets/2026-09-21_gate1106to1111/shape_1.py."""
import subprocess, sys, itertools
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
DEV = '362e51fe0db7e73d5557924902763fe3f10fd8c7'
DEV_TREE_CLAIM = '2e981e7779dc9bcabecd099c6e93da21345a8ed0'
# n, letter, ticket(s), head, seat's per-PR tree (GROUPING), seat's file count, seat's target blob(s)
PRS = [('1112', 'A', 'KS-1203', '3a28d2a3c4d030cb73b7775bb19c5844ce190e56', '7b8734234ed58c55bf1ff427d6cd03fdfdc36e20', 1),
       ('1113', 'B', 'KS-1283', 'abf8321a9ca426a1d623a54a41453824dce34def', '5c8e116814348c78207055424af12a43b93ab564', 1),
       ('1114', 'C', 'KS-1244+KS-1198', '762a70117c6cf40545f8a4ac5f24708e7fcd91fe', 'c6a6a7380f1d4554de724f9a38257e0498e3a261', 1),
       ('1115', 'D', 'KS-1275', 'b008489e4fbc72bb8b68cb3bb925557978399780', 'fea63ca447a2d2d54aada84575236780b03fa948', 1),
       ('1116', 'E', 'KS-1284+KS-1175', '9a485cfe77406f47103ed6ab65c14ec01144cb68', 'ea9fc7d7cefc2b88d7fec7b694fc1204b07f1777', 5),
       ('1117', 'G', 'KS-1137', 'b3f94f14a0cf3e0236284481b85781417fd233f3', '8de2a19066c964a23b052e0db6395ea3f2bb74ec', 1),
       ('1118', 'F', 'KS-1006+KS-1236', 'f132c92147b5005c36e405d0116faa541d978a67', '7e75405911ec06a01839d4bcf86ccd747b4a3802', 1)]
D = 'Blockchain/Dev/'
SEAT_BLOBS = {  # the GROUPING / READY target blobs (seat's claim, re-read here)
  D + 'services/api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts': ('e05c6bd21f64ad766083c72d0fc070ebeb478b7f', 'd68c6b2be95bf7c72b31903c27a0f26bbeee0332'),
  D + 'services/api-gateway/src/__tests__/ks480-org-provisioner-gate.test.ts': ('38787a194855ddb6931c81611c096cab8ec49c0d', '92966f9c1f6291e8190b139d117ce39148fc6752'),
  D + 'services/api-gateway/src/__tests__/auth.test.ts': ('72348995a66ea324ffe78dc64136f46e64985aad', '6d837e0aeeb8fdc7434033ae5d91fd018cfc5b66'),
  D + 'services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts': ('22485a7ab3c5022912bf5216e9207875bc530aa4', '27366baf325148d402822609f8ebe4d3c822724d'),
  D + 'services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts': ('05793d9254002f951e46d882510ec39e3d38dd37', 'd3d29533c9eeb962a6c1f7b3d4603b0a43658fd8'),
  D + 'services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts': ('c3f430d783ba0d8594d962ceef13ad27325f402b', 'a6765883d409756eed8f7e73cca1dd05dd121d81'),
  D + 'services/anchoring/src/__tests__/ks1175-getid-view-wired.test.ts': ('ABSENT', '57de9c9e24787dc33e3ec1006eae3f6640848b3f'),
  D + 'services/anchoring/src/__tests__/ks1284-chain-read-order.test.ts': ('ABSENT', 'f461e832c5662bbe5258347654b0aa949008a1d3'),
  D + 'services/anchoring/src/__tests__/ks1284-attach-point.test.ts': ('ABSENT', 'd42259343d79141948ff3e879f8a7b34187dcb95'),
  D + 'scripts/__tests__/container_trivy_image_filter.test.sh': ('dec2db8dee6326369ebc16cacb1f8d58287a7562', '35bbb4519950f77188ad30f3f1d46683ac63ddf5'),
  D + 'services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts': ('703c80dca84cde113b585788317f56cb5184f3d3', 'bfa8b1d3fc3611ad04266d9e520848958f2a4b55'),
}
TAMPER_FILES = {  # the ten tamper files: seat's (bytes, sha256 prefix, blob prefix) at the tip
  D + 'services/api-gateway/src/services/enforcement.ts': (10708, '69709f07956e', 'be466fbf4441'),
  D + 'services/api-gateway/src/routes/platform.ts': (44888, '7d04a92ca724', 'b80a8cd8d4e1'),
  D + 'services/api-gateway/src/middleware/auth.ts': (19524, '9abef1c21164', 'bf09d315a644'),
  D + 'services/originate/src/originate.openapi.ts': (150298, '3056d0a26e5e', '2d1b48a0c7ea'),
  D + 'services/anchoring/src/anchorReadback.ts': (6836, '9a41f455eb22', 'f49ffb6afaaf'),
  D + 'services/anchoring/src/cardano/cardanoMetadatum.ts': (4650, '48497ffc0937', 'aaaec6c63655'),
  D + 'services/anchoring/src/index.ts': (84682, '31422a6ab3c7', 'b6386f402a4b'),
  D + 'services/anchoring/src/cardano/transaction.ts': (5414, '68ddee40814d', 'e047630ea004'),
  D + 'services/auth/src/routes/users.ts': (66724, '96408a532a73', '3bfa47dcde01'),
  'Blockchain/Testing/jobs/04-container-trivy.sh': (6117, '0720a4bfa4a4', '88444463f9d4'),
}
def git(*a):
    p = subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr
print('date', subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip())
for c in [DEV] + [h for *_a, h, t, nf in PRS]:
    rc, o, e = git('cat-file', '-t', c); print('object', c[:9], (o.strip() or e.strip()))
rc, o, e = git('rev-parse', DEV + '^{tree}'); dt = o.strip(); print('develop tree', dt, '== seat claim', dt == DEV_TREE_CLAIM)
rc, o, e = git('log', '--format=%H %T %s', '-1', DEV); print('develop log', o.strip())
union = {}; per = {}; ok = True
for n, L, tk, h, seat_tree, nf in PRS:
    rc, o, e = git('rev-list', '--parents', '-n1', h); par = o.split()[1:]
    rc, t, e = git('rev-parse', h + '^{tree}'); t = t.strip()
    rc, lr, e = git('rev-list', '--left-right', '--count', DEV + '...' + h)
    rc, raw, e = git('diff', '--raw', '--abbrev=40', DEV, h)
    rc, ns, e = git('diff', '--numstat', DEV, h)
    rc, subj, e = git('log', '--format=%s', '-1', h)
    files = []
    for l in raw.strip().splitlines():
        meta, path = l.split('\t', 1); m1, m2, b1, b2, st = meta.split()
        files.append((path, 'ABSENT' if b1 == '0' * 40 else b1, b2, st, m2))
    per[n] = files
    print('#%s PR %s %s head %s parents %s (== [DEV] %s) | develop...head behind/ahead %s (want 0 1) | head tree %s == seat %s %s | files %d (want %d)' % (
        n, L, tk, h[:9], [p[:9] for p in par], par == [DEV], lr.split(), t, seat_tree[:12], t == seat_tree, len(files), nf))
    print('    subject: %s (%d chars)' % (subj.strip(), len(subj.strip())))
    if par != [DEV] or lr.split() != ['0', '1'] or t != seat_tree or len(files) != nf: ok = False
    for f in files:
        sb = SEAT_BLOBS.get(f[0])
        print('    %s %-8s dev %s head %s mode %s under __tests__/ %s | seat (dev, head) = %s' % (f[3], f[0].split('/')[-1][:44], f[1][:12], f[2][:12], f[4], '__tests__/' in f[0], 'EQUAL' if sb == (f[1], f[2]) else ('DIFFERS ' + str(sb))))
        print('       ', f[0])
        union.setdefault(f[0], []).append(n)
        if sb != (f[1], f[2]) or '__tests__/' not in f[0] or f[4] != '100644' or f[3] not in 'AM': ok = False
    print('    numstat:', ' | '.join(l.replace('\t', ' ') for l in ns.strip().splitlines()))
    dels = sum(int(l.split('\t')[1]) for l in ns.strip().splitlines()); adds = sum(int(l.split('\t')[0]) for l in ns.strip().splitlines())
    print('    additions %d deletions %d (want deletions 0)' % (adds, dels))
    if dels != 0: ok = False
print('UNION paths', len(union), '(want 11) | multi-PR paths', {k: v for k, v in union.items() if len(v) > 1} or 'NONE')
print('pairwise overlap counts:', [(a, b, len(set(f[0] for f in per[a]) & set(f[0] for f in per[b]))) for a, b in itertools.combinations(per, 2) if set(f[0] for f in per[a]) & set(f[0] for f in per[b])] or 'ALL ZERO (21 pairs)')
print('seat GROUPING paths ∖ measured union:', sorted(set(SEAT_BLOBS) - set(union)) or 'NONE', '| measured ∖ GROUPING:', sorted(set(union) - set(SEAT_BLOBS)) or 'NONE')
print('--- the ten tamper files at develop (bytes / sha256 prefix / blob) vs the seat')
import hashlib
for p, (nb, sh, bl) in TAMPER_FILES.items():
    rc, b, e = git('rev-parse', DEV + ':' + p); b = b.strip()
    pr = subprocess.run(['git', '-C', REPO, 'show', DEV + ':' + p], capture_output=True)
    data = pr.stdout; s = hashlib.sha256(data).hexdigest()
    eq = (len(data) == nb and s.startswith(sh) and b.startswith(bl))
    print('  %-70s %6d B sha256 %s blob %s | seat %d %s %s -> %s' % (p.replace(D, ''), len(data), s[:12], b[:12], nb, sh, bl, 'EQUAL' if eq else 'DIFFERS'))
    if not eq: ok = False
# the ten tamper files unchanged at EVERY head (they are not PR paths)
for p in TAMPER_FILES:
    rc, b, e = git('rev-parse', DEV + ':' + p); b = b.strip()
    for n, L, tk, h, seat_tree, nf in PRS:
        rc, bh, e = git('rev-parse', h + ':' + p)
        if bh.strip() != b: print('  DIFFERS at head', n, p); ok = False
print('the ten tamper files carry the develop blob at every one of the seven heads: True' if ok else 'SEE ABOVE')
# unchanged-read paths the gate will run/read: same blob at develop and every head
UNCH = [D + 'services/api-gateway/package.json', D + 'services/api-gateway/vitest.config.ts', D + 'services/api-gateway/vitest.setup.ts', D + 'services/api-gateway/tsconfig.json',
        D + 'services/originate/package.json', D + 'services/originate/jest.config.js', D + 'services/originate/tsconfig.json',
        D + 'services/anchoring/package.json', D + 'services/anchoring/vitest.config.ts', D + 'services/anchoring/tsconfig.json',
        D + 'services/auth/package.json', D + 'services/auth/vitest.config.ts', D + 'services/auth/tsconfig.json',
        D + 'packages/shared/package.json', D + 'packages/shared/vitest.config.ts', D + 'packages/shared/tsconfig.json',
        D + 'scripts/run-shell-suites.sh', '.githooks/pre-push', D + 'package.json', D + 'package-lock.json', D + 'eslint.config.mjs',
        D + 'scripts/__tests__/aggregate_report_trivy_artefact.test.sh', D + 'scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh', D + 'scripts/__tests__/orchestrate_jobs.test.sh',
        D + 'services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts', D + 'services/api-gateway/src/__tests__/ks480-connector-auth.test.ts',
        D + 'services/anchoring/src/__tests__/ks1284-cardano-metadatum.test.ts', D + 'services/api-gateway/src/__tests__/db.retry.test.ts', D + 'services/anchoring/src/anchorIdentityView.ts']
print('--- unchanged-read paths: presence at develop + same blob at every head')
for p in UNCH:
    rc, b, e = git('rev-parse', '-q', '--verify', DEV + ':' + p); b = b.strip() or 'ABSENT'
    same = all(git('rev-parse', '-q', '--verify', h + ':' + p)[1].strip() == b for *_a, h, t, nf in PRS) if b != 'ABSENT' else False
    print('  %-100s %s same-at-7-heads %s' % (p, b[:12], same))
print('ALL SHAPE ASSERTIONS HELD:', ok)
