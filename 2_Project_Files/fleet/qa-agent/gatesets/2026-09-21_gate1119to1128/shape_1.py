#!/usr/bin/env python3
"""shape_1.py — READ-ONLY object reads in the Secuura checkout (rev-list / rev-parse / diff --raw / diff --numstat / show / cat-file):
each of the TEN heads is ONE commit whose parent IS develop 7be81d5c9; each head tree == the seat's GROUPING per-PR tree; the 13 (path,
develop blob | ABSENT, head blob) triples == the seat's; 13 paths pairwise disjoint; 12 test-only under __tests__/ + PR F's ONE product path
Blockchain/Testing/jobs/04-container-trivy.sh (-1/+2); numstat +508/-1; the 11 tamper files (never a target) same blob at develop and every head;
every tamper `from` (from the run dirs' input.json) counted at the tip by exact line AND by raw substring; the two-line LIVETENANTRAW block.
Derived from gatesets/2026-09-21_gate1112to1118/shape_1.py."""
import json, subprocess, itertools, hashlib, os
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
RUNS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs'
DEV = '7be81d5c9b109959b559e03652fb092c12de58e8'; DEV_TREE = '6aa9873f974019a92574d6db52e6356734573c8c'
D = 'Blockchain/Dev/'; A = D + 'services/api-gateway/'; O = D + 'services/originate/'; S = D + 'services/security/'; T = D + 'services/timestamping/'
R = D + 'services/referral/'; M = D + 'services/mcp-server/'; SC = D + 'scripts/'
def git(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
def out(*a):
    p = git(*a); assert p.returncode == 0, (a, p.stderr); return p.stdout
print(subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip())
PRS = [  # n, letter, tickets, head, seat tree, nfiles, tier, adds, dels
 ('1119', 'B', 'KS-753', 'e9e20196f2a91ca57ec6bc6d24087843e2611a08', 'c35d59b310b6b9d456a4f6b7b1eb8b26859b179d', 1, 2, 32, 0),
 ('1120', 'E', 'KS-1232', '2a66cd17ec3bd5d91e2fc72c7e3f9102ce1eb839', 'e8b4659fab666a47c2e42c6fe1ec68d0945eb4dc', 2, 2, 87, 0),
 ('1121', 'G', 'KS-957 + KS-930', '939de1ba519629cacd22031cbc42dbbb765b4040', 'c11e01c5e18b91705ebefec6e160b2c235f1daf6', 1, 2, 74, 0),
 ('1122', 'F', 'KS-1273', '9aa5442aeef4d07a3d39e3c3e73e65ef9a42a350', '743126250635ef59c2421471712d90f3a4636449', 2, 2, 116, 1),
 ('1123', 'H', 'KS-1275', 'c346999ad3956c02e56fca61f9ad30396ceee2ff', '85ddc802fe50371f051132a88c5141e9b133a0f0', 1, 2, 9, 0),
 ('1124', 'A', 'KS-880', 'bd907c5538286ee9333e2182d7b388c1007b7163', '192f34492e33c1b0e00b5fda33531b9cf2234afb', 1, 1, 9, 0),
 ('1125', 'D', 'KS-1223', 'c50c0a8d402cb6fc585b889c528802fba74c0e40', 'b058d498b3b6b86d8eb88df7b03e48d5426dab13', 2, 1, 124, 0),
 ('1126', 'I', 'KS-1283', 'b23ad259a880ecb207b2ab3cf7e9a1b0b8368dad', '4b32a4d50b3758b2597f2a76e2aa84287a13aae8', 1, 1, 26, 0),
 ('1127', 'J', 'KS-1244', 'f0cc0aadc1a7856f76cbb69e925e23b94dd05a40', 'bf45a0ddb07a6154b394a70fcb583b44fe5c988f', 1, 1, 13, 0),
 ('1128', 'C', 'KS-1234', 'e35b5ddc27dffca5ad1a7cea17b4433484d460ac', '127d9d55be7796ca36449faa123be949f72dee50', 1, 1, 18, 0),
]
dt = out('rev-parse', DEV + '^{tree}').strip(); print('develop', DEV[:9], 'tree', dt, '== seat', dt == DEV_TREE)
print('develop subject:', out('log', '-1', '--format=%s', DEV).strip())
CHANGED = {}; PERPR = {}; tot_a = tot_d = 0
for n, L, tk, h, ht, nf, tier, adds, dels in PRS:
    par = out('rev-list', '--parents', '-n1', h).split()[1:]
    lr = out('rev-list', '--left-right', '--count', DEV + '...' + h).split()
    t = out('rev-parse', h + '^{tree}').strip()
    subj = out('log', '-1', '--format=%s', h).strip()
    raw = out('diff', '--raw', '--abbrev=40', DEV, h).strip().splitlines()
    ns = {l.split('\t')[2]: (int(l.split('\t')[0]), int(l.split('\t')[1])) for l in out('diff', '--numstat', DEV, h).strip().splitlines()}
    files = {}
    for l in raw:
        meta, path = l.split('\t', 1); m1, m2, b1, b2, st = meta.split()
        files[path] = ('ABSENT' if b1 == '0' * 40 else b1, b2, st, m2, n)
    a_sum = sum(v[0] for v in ns.values()); d_sum = sum(v[1] for v in ns.values()); tot_a += a_sum; tot_d += d_sum
    tests_only = all('__tests__/' in p for p in files)
    print('#%s PR %s %s head %s parent==DEV %s | develop...head behind/ahead %s (want 0 1) | tree %s == seat %s | files %d (want %d) | +%d/-%d (want +%d/-%d) | modes %s | all under __tests__/ %s | subject %d chars %r' % (
        n, L, tk, h[:9], par == [DEV], lr, t[:9], t == ht, len(files), nf, a_sum, d_sum, adds, dels, sorted({v[3] for v in files.values()}), tests_only, len(subj), subj))
    for p, v in files.items():
        print('     %s %s %s -> %s (+%d/-%d)' % (v[2], p.replace(D, ''), v[0][:12], v[1][:12], ns[p][0], ns[p][1]))
        assert p not in CHANGED, ('path in two PRs', p); CHANGED[p] = v
    PERPR[n] = files
print('union paths', len(CHANGED), '(want 13) | added', sum(1 for v in CHANGED.values() if v[2] == 'A'), '(want 6) | modified', sum(1 for v in CHANGED.values() if v[2] == 'M'), '(want 7) | total +%d/-%d (want +508/-1)' % (tot_a, tot_d))
print('pairwise overlaps:', [(a, b) for a, b in itertools.combinations(PERPR, 2) if set(PERPR[a]) & set(PERPR[b])] or 'NONE (45 pairs)')
print('paths NOT under __tests__/:', [p for p in CHANGED if '__tests__/' not in p], '(want exactly the trivy job)')
SEAT = {  # the GROUPING / READY blobs (develop-side, head)
  T + 'src/__tests__/ks740-bounded-fanout.test.ts': ('6fdf0e80a46c', 'd732631dc0c2adfa1cbf3345074f7c39ba41c2f5'),
  M + 'src/__tests__/ks1232-connector-info-relay.test.ts': ('ABSENT', 'e93bfae369f0ba940739c2a22ad25f9718ebda0a'),
  M + 'src/__tests__/ks1232-generate-package-doctypes-default.test.ts': ('ABSENT', '59bc927624043f1b5c3bccd03dc98cfec00ef400'),
  SC + '__tests__/check_shared_relink_tooling_tokens.test.sh': ('ABSENT', 'fdb125ca3e6ae4516836c4c12ac88e5b34b2ca46'),
  'Blockchain/Testing/jobs/04-container-trivy.sh': ('88444463f9d4', '6dfc5731e56ede5e5a6f420cccd92874b7566a87'),
  SC + '__tests__/container_trivy_exit_code_env_keeps_findings.test.sh': ('ABSENT', 'd119e64ba755e41e41d719d03ded24f79f297e04'),
  O + 'src/__tests__/ks978-published-contract-organizationuuid.test.ts': ('27366baf3251', '530fa32f8d886e70375e967304cf8881edf0e950'),
  S + 'src/__tests__/ks869-connector-id-persisted.test.ts': ('7a3fc7e16d0c', 'f452db039b9dceb34bebd5046525de1e42b1879e'),
  A + 'src/__tests__/ks1223-wallet-forwarded-to-originate.test.ts': ('ABSENT', '82a92ea52407fba3cdeb755efab488854b3e5758'),
  R + 'src/__tests__/ks1223-wallet-header-fallback.test.ts': ('ABSENT', 'daf9f5c1a6bb586065fcf44559073c25624dcf48'),
  A + 'src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts': ('50298953359e', '94d0813cc861333a2dc60457d7fac8af9ec6fd17'),
  A + 'src/__tests__/auth.test.ts': ('6d837e0aeeb8', '41f85fcb250ea6cd1b1e6bc33117dab2e7ee93ae'),
  A + 'src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts': ('3f85887f7268', 'e5cc79c5e29b0b657240feb2b8afc2b1d6073ba8'),
}
ok = True
for p, (b1, b2) in SEAT.items():
    v = CHANGED.get(p); good = v is not None and v[0].startswith(b1) and v[1] == b2
    ok &= good
    if not good: print('DISAGREE', p, v)
print('13 seat (develop blob, head blob) pairs agree with the live objects:', ok)
# head lines / bytes / sha256 per target
for p, (b1, b2) in SEAT.items():
    data = subprocess.run(['git', '-C', REPO, 'cat-file', 'blob', b2], capture_output=True).stdout
    print('   head blob %s %s: %d lines %d B sha256 %s' % (b2[:12], p.split('/')[-1], data.count(b'\n'), len(data), hashlib.sha256(data).hexdigest()[:16]))
# tamper files (11, never a target) — same blob at develop and every head
TAMPER = [S + 'src/index.ts', T + 'src/index.ts', A + 'src/index.ts', A + 'src/routes/verification.ts', A + 'src/routes/platform.ts', A + 'src/middleware/auth.ts',
          O + 'src/originate.openapi.ts', R + 'src/routes/referrals.ts', M + 'src/tools/info.ts', M + 'src/http-server.ts', SC + 'check-shared-relink.sh']
for p in TAMPER:
    b = out('rev-parse', DEV + ':' + p).strip()
    same = all(out('rev-parse', h + ':' + p).strip() == b for _, _, _, h, *_ in PRS)
    data = subprocess.run(['git', '-C', REPO, 'cat-file', 'blob', b], capture_output=True).stdout
    print('tamper file %-60s develop blob %s same at all 10 heads %s | %d lines %d B sha256 %s' % (p.replace(D, ''), b[:12], same, data.count(b'\n'), len(data), hashlib.sha256(data).hexdigest()[:12]))
# the trivy job: changed ONLY by F
tj = 'Blockchain/Testing/jobs/04-container-trivy.sh'; bdev = out('rev-parse', DEV + ':' + tj).strip()
print('trivy job blob at develop', bdev[:12], '| heads where it differs:', [n for n, _, _, h, *_ in PRS if out('rev-parse', h + ':' + tj).strip() != bdev], '(want [1122])')
# siblings + config the gate runs — same at every head
UNCH = [SC + '__tests__/container_trivy_image_filter.test.sh', SC + '__tests__/container_trivy_failed_scan_is_loud.test.sh', SC + '__tests__/check_shared_relink.test.sh',
        SC + '__tests__/aggregate_report_trivy_artefact.test.sh', SC + '__tests__/orchestrate_jobs.test.sh', A + 'src/__tests__/ks480-org-provisioner-gate.test.ts', A + 'src/__tests__/db.retry.test.ts',
        A + 'src/__tests__/ks1207-connector-api-key-optional-mount.test.ts', A + 'vitest.setup.ts', A + 'package.json', A + 'vitest.config.ts', A + 'tsconfig.json', A + 'package-lock.json',
        O + 'package.json', O + 'jest.config.js', O + 'tsconfig.json', O + 'package-lock.json', S + 'package.json', S + 'vitest.config.ts', S + 'tsconfig.json', S + 'package-lock.json',
        T + 'package.json', T + 'vitest.config.ts', T + 'tsconfig.json', T + 'package-lock.json', R + 'package.json', R + 'vitest.config.ts', R + 'tsconfig.json', R + 'package-lock.json',
        M + 'package.json', M + 'vitest.config.ts', M + 'tsconfig.json', M + 'package-lock.json', D + 'packages/shared/package.json', D + 'packages/shared/vitest.config.ts', D + 'packages/shared/tsconfig.json',
        D + 'scripts/run-shell-suites.sh', D + 'scripts/preflight/preflight.sh', '.githooks/pre-push', D + 'package.json', D + 'package-lock.json', D + 'eslint.config.mjs', D + 'scripts/fix-libsodium-symlink.js',
        D + 'systemTest/__tests__/manifest_quarantine.test.sh']
for p in UNCH:
    q = git('rev-parse', '-q', '--verify', DEV + ':' + p)
    if q.returncode: print('  unchanged-read path ABSENT at develop:', p); continue
    b = q.stdout.strip(); same = all(out('rev-parse', h + ':' + p).strip() == b for _, _, _, h, *_ in PRS)
    print('  unchanged-read %-70s %s same at all heads %s' % (p.replace(D, ''), b[:12], same))
# tampers: `from` texts from the run dirs' input.json; count by exact line and raw substring at the tip
RUNMAP = {'B': ['2026-09-21_ks753-ornith35b-night2'], 'E': ['2026-09-21_ks1232-ornith35b-night3', '2026-09-21_ks1232-ornith35b-night2'], 'G': ['2026-09-21_ks957-ornith35b-night'],
          'F': ['2026-09-21_ks1273-ornith35b-night'], 'H': ['2026-09-21_ks1275-ornith35b-night2'], 'A': ['2026-09-21_ks880-ornith35b-night'],
          'D': ['2026-09-21_ks1223-ornith35b-night', '2026-09-21_ks1223-ornith35b-night2'], 'I': ['2026-09-21_ks1283-ornith35b-night2'], 'J': ['2026-09-21_ks1244-ornith35b-night2'],
          'C': ['2026-09-21_ks1234-ornith35b-night', '2026-09-21_ks1234-ornith35b-night2', '2026-09-21_ks1234-ornith35b-night3']}
ntamp = 0; plants = []
for L, runs in RUNMAP.items():
    for r in runs:
        ip = os.path.join(RUNS, r, 'input.json'); j = json.load(open(ip, encoding='utf-8'))
        tampers = j.get('tampers') or []
        tip = j.get('tip') or j.get('develop') or '?'
        print('PR %s run %s tip %s tampers %d mode %s target %s' % (L, r, str(tip)[:9], len(tampers), j.get('mode', '?'), str(j.get('target_file') or j.get('file') or j.get('test_file') or '?')[-60:]))
        for tm in tampers:
            ntamp += 1
            f = tm['file']; f = f if f.startswith('Blockchain/') else (D + f if not f.startswith('services/') and not f.startswith('scripts/') else D + f)
            src = out('show', DEV + ':' + f)
            frm = tm['from']; lines = src.split('\n')
            fl = frm.split('\n')
            if len(fl) == 1:
                cnt_line = lines.count(frm); cnt_raw = src.count(frm)
                at = [i + 1 for i, l in enumerate(lines) if l == frm]
            else:
                cnt_line = sum(1 for i in range(len(lines) - len(fl) + 1) if lines[i:i + len(fl)] == fl); cnt_raw = src.count(frm)
                at = [i + 1 for i in range(len(lines) - len(fl) + 1) if lines[i:i + len(fl)] == fl]
                print('      (%d-line block; first line alone count %d)' % (len(fl), lines.count(fl[0])))
            pl = ''
            po = os.path.join(RUNS, r, 'out.md.checker', 'tamper_%s.plant.out' % tm['id'])
            if os.path.exists(po): pl = open(po, encoding='utf-8', errors='replace').read().strip().replace('\n', ' | ')[:120]
            plants.append((tm['id'], pl))
            print('   %-22s %-40s line-count %d raw-count %d at %s (declared :%s) reds %s | plant.out: %s' % (tm['id'], f.replace(D, ''), cnt_line, cnt_raw, at, tm.get('line'), tm.get('reds'), pl))
print('tampers total', ntamp, '(want 20)')
# PR F's product hunk `-` line
job = out('show', DEV + ':' + tj); ln = '    "$img" 2>/dev/null)"; trc=$?'
print('PR F product hunk `-` line count at develop:', job.split('\n').count(ln), 'at', [i + 1 for i, l in enumerate(job.split('\n')) if l == ln], '(want 1 at 93); control `latest` lines:', sum(1 for l in job.split('\n') if 'latest' in l))
hj = out('show', PRS[3][3] + ':' + tj).split('\n')
print('PR F job at head: lines', len(hj) - 1, '| --exit-code 0 lines:', sum(1 for l in hj if '--exit-code 0' in l), '| KS-1273 comment lines:', sum(1 for l in hj if 'KS-1273' in l))
print('develop -> F job numstat:', out('diff', '--numstat', DEV, PRS[3][3], '--', tj).strip())
print(subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip())
