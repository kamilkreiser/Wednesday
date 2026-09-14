#!/bin/bash
# controls_check.sh — every :N anchor, blob, size, line count, numstat and token count the #989 brief cites, checked against
# the GitHub contents API (blobs at the head + develop M38 + the live develop) AND git at the checkout (read verbs only).
# Usage: bash controls_check.sh [--neg-head-as-dev] [--neg-token] [--neg-dev-as-0911]
#   --neg-head-as-dev  : develop M38 passed where the head is expected (must FAIL on the two fixture blobs + the new files + anchors)
#   --neg-token        : a token demanded PRESENT that is known ABSENT + one demanded ABSENT that is present (must FAIL 2)
#   --neg-dev-as-0911  : develop pinned at the 09-11 develop 2d864ae92 (must FAIL: pre-suite.ts / provision.ts differ there — KS-969 rounds)
# Prints ok/FAIL lines and a tally; rc 1 if FAILS>0. No secrets printed (GH_TOKEN by name from the Secuura .env).
set -u
ARGS="${1:-}"
python3 - "$ARGS" <<'PY'
import sys, json, urllib.request, urllib.error, base64, subprocess, datetime
arg = sys.argv[1]
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
R = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
tok = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
def git(*a):
    return subprocess.run(['git', '-C', R] + list(a), capture_output=True, text=True).stdout
HEAD = '9d0e2016ae60658ec908ee5e500583fd3a318c8a'; M38 = '0e78c7270188ac45c1c29f927bdf90728f10215d'; P3FA = '3fa0a22b10ba3f3ee7b1efc3a229a1ee8d167284'
D0911 = '2d864ae92'
if arg == '--neg-head-as-dev': HEAD = M38
DEV = D0911 if arg == '--neg-dev-as-0911' else M38
F = 'systemTest/fixtures/'; T = 'systemTest/performance/tests/unit/fixtures/'; PF = 'systemTest/performance/'
ok = fail = 0
def chk(cond, msg):
    global ok, fail
    if cond: ok += 1; print('ok   ' + msg)
    else: fail += 1; print('FAIL ' + msg)
print('controls_check', arg or '(positive)', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
live = get('/branches/develop')['commit']['sha']; print('live develop =', live)
cache = {}
def blob(ref, path):
    k = (ref, path)
    if k not in cache:
        try:
            j = get('/contents/' + path + '?ref=' + ref)
            cache[k] = (j['sha'], j['size'], base64.b64decode(j['content']).decode('utf-8') if j.get('encoding') == 'base64' and j.get('content') else None)
        except urllib.error.HTTPError as e:
            cache[k] = (None, None, None) if e.code == 404 else (('ERR', e.code, None))
    return cache[k]
# --- blobs at the head + develop (the brief's TARGET table) ---
EXPECT = {
  (HEAD, F+'provision.ts'): ('68c801d626c2b65d76bd6c48d5323a5ce70a82c7', 11488), (HEAD, F+'pre-suite.ts'): ('f5f839a84db447dc08115a7e37d253f48b205654', 12339),
  (HEAD, T+'provisionRedaction.test.ts'): ('2cc4be3d64044268427ca4978eac255e326fddf9', 8970), (HEAD, T+'preSuiteStreams.test.ts'): ('1e384fb1d9d679db41a27f2cefbc0727480324f3', 5357),
  (HEAD, T+'provisionDriftQuarantine.test.ts'): ('2de77e9db2aa95a8ae7b9f86c595f0ec58043a4f', 7888),
  (HEAD, F+'provision-actors.ts'): ('2795b5937049e8e1a265e69b032f2914c674bd7d', 17376), (HEAD, F+'manifest.ts'): ('a6bfe3e7662791866e16c04331ba8fdc473a535a', 7574), (HEAD, F+'actors.ts'): ('8443c682b585afc4f39c43094588898a0c92795e', 6235),
  (HEAD, PF+'vitest.unit.config.ts'): ('cb1864d783c32d3bea3f574767092828ce541e0b', 1383), (HEAD, PF+'package.json'): ('b9ae2c052abcd6601c79569abde371cd5e73dddb', None), (HEAD, PF+'package-lock.json'): ('4694ee0a7a8cbc06e9e17c2441f9c535ae8d224c', 170665),
  (HEAD, 'systemTest/__tests__/pre_suite.test.sh'): ('f4d08fa29449e43c07a90e2c58caaaee2e3fb907', 19053), (HEAD, 'systemTest/akto/tests/preSuiteSetup.ts'): ('9e74cdd8fad92757f0f01697238b1021fdb1727d', None), (HEAD, 'systemTest/schemathesis/scripts/run.py'): ('89d30de6ee127d1e91eca4816dea656bad05e525', None),
  (DEV, F+'provision.ts'): ('b95f4ee393ab5da261eff06d95069f8bdf24ee3f', 10190), (DEV, F+'pre-suite.ts'): ('01024faddd0ad311aa160de02683b16973603928', 12777),
  (DEV, F+'provision-actors.ts'): ('2795b5937049e8e1a265e69b032f2914c674bd7d', 17376), (DEV, F+'manifest.ts'): ('a6bfe3e7662791866e16c04331ba8fdc473a535a', 7574), (DEV, F+'actors.ts'): ('8443c682b585afc4f39c43094588898a0c92795e', 6235),
  (DEV, 'systemTest/akto/tests/preSuiteSetup.ts'): ('9e74cdd8fad92757f0f01697238b1021fdb1727d', None), (DEV, 'systemTest/schemathesis/scripts/run.py'): ('89d30de6ee127d1e91eca4816dea656bad05e525', None),
  (DEV, F+'tsconfig.json'): ('2df1d1d65235dd885c769d3580c8007b81ba3d29', None), (DEV, PF+'tsconfig.json'): ('aae0fb3c16541be70d4c0b526b1015094cb6b145', None), (DEV, PF+'tsconfig.node.json'): ('12b2a634124366a8e6d74dfb0e571f0626ad2043', None), (DEV, PF+'eslint.config.js'): ('1a539ed5b55c744d58bdd1b9a2091982abf09a45', None),
}
for (ref, path), (sha, size) in EXPECT.items():
    b = blob(ref, path)
    chk(b[0] == sha and (size is None or b[1] == size), f'{ref[:9]} {path.split("/")[-1]} blob {str(b[0])[:9]} size {b[1]} (expect {sha[:9]} {size})')
ABSENT = [(DEV, T+'provisionRedaction.test.ts'), (DEV, T+'preSuiteStreams.test.ts'), (DEV, T+'provisionDriftQuarantine.test.ts'), (DEV, 'systemTest/package.json'), (HEAD, 'systemTest/package.json')]
for ref, path in ABSENT:
    chk(blob(ref, path)[0] is None, f'{ref[:9]} {path.split("/")[-1]} ABSENT')
# --- line anchors + token counts on the API-fetched bytes (the brief's :N) ---
def lines(ref, path): return (blob(ref, path)[2] or '').split('\n')
def at(ref, path, n, needle):
    L = lines(ref, path); return n <= len(L) and needle in L[n-1]
def cnt(ref, path, needle): return (blob(ref, path)[2] or '').count(needle)
PV = F+'provision.ts'; PS = F+'pre-suite.ts'
chk(len(lines(HEAD, PV)) == 330 and len(lines(DEV, PV)) == 285, 'provision.ts 329 lines at head / 284 at develop')
chk(len(lines(HEAD, PS)) == 245 and len(lines(DEV, PS)) == 234, 'pre-suite.ts 244 lines at head / 233 at develop')
chk(at(HEAD, PV, 234, '/**') and at(HEAD, PV, 248, ' */') and at(HEAD, PV, 249, 'export function redactSecrets(') and at(HEAD, PV, 260, '}'), 'provision.ts:234-248 docblock / :249-260 redactSecrets')
chk(at(HEAD, PV, 255, 'for (const secret of secrets) {') and at(HEAD, PV, 256, 'if (secret.length === 0) continue;') and at(HEAD, PV, 257, 'scrubbed = scrubbed.split(secret).join("[REDACTED]");') and at(HEAD, PV, 258, '}'), 'provision.ts:255-258 the loop (empty skipped, split/join)')
chk(at(HEAD, PV, 323, 'const reason = redactSecrets(envelope.error?.message ?? `HTTP ${status}`, [') and at(HEAD, PV, 324, 'spec.password,') and at(HEAD, PV, 325, ']);'), 'provision.ts:323-325 THE ONE interpolation site (redacted)')
chk(at(HEAD, PV, 326, 'throw new Error(') and at(HEAD, PV, 327, '`could not provision actor "${spec.key}" (${spec.email}): ${reason}`,') and at(HEAD, PV, 328, ');'), 'provision.ts:326-328 the throw (key + email + reason)')
chk(cnt(HEAD, PV, 'throw new Error(') == 1 and cnt(HEAD, PV, 'redactSecrets(') == 3, 'provision.ts: ONE throw new Error( ; redactSecrets( x3 (docblock example + def + call)')
chk(cnt(HEAD, PV, 'redactSecrets(envelope.error?.message') == 1 and cnt(DEV, PV, 'redactSecrets') == 0, 'T2 anchor count 1 at head / redactSecrets 0 at develop (control)')
chk(at(DEV, PV, 282, 'const reason = envelope.error?.message ?? `HTTP ${status}`;') and at(DEV, PV, 283, 'throw new Error(`could not provision actor "${spec.key}" (${spec.email}): ${reason}`);'), 'develop provision.ts:282-283 the raw interpolation (the M38 site)')
chk(at(HEAD, PV, 137, 'async function login(') and at(HEAD, PV, 158, '}') and at(HEAD, PV, 167, 'export async function bootstrapToken(') and at(HEAD, PV, 177, '}') and at(HEAD, PV, 192, 'async function createAsAdmin(') and at(HEAD, PV, 232, '}'), 'provision.ts:137-158 login / :167-177 bootstrapToken / :192-232 createAsAdmin (return null, no throw)')
chk(at(HEAD, PS, 226, '// KS-973 residue (e):') and at(HEAD, PS, 229, '// by `performance/tests/unit/fixtures/preSuiteStreams.test.ts`.') and at(HEAD, PS, 230, 'const invokedDirectly =') and at(HEAD, PS, 232, 'import.meta.url === pathToFileURL(process.argv[1]).href;'), 'pre-suite.ts:226-229 the comment / :230-232 invokedDirectly')
chk(at(HEAD, PS, 239, '(result.outcome === "PROVISIONED" ? console.log : console.error)(') and at(HEAD, PS, 240, 'result.summary,') and at(HEAD, PS, 241, ');'), 'pre-suite.ts:239-241 the CLI tail (T1 anchor)')
chk(cnt(HEAD, PS, '(result.outcome === "PROVISIONED" ? console.log : console.error)(') == 1, 'T1 anchor count 1')
chk(at(HEAD, PS, 195, '`[pre-suite:${suite}] DEGRADED — provisioning did not complete: ${reason}\\n` +') and at(HEAD, PS, 140, 'const reason = err instanceof Error ? err.message : String(err);'), 'pre-suite.ts:195 the DEGRADED banner / :140 reason = err.message')
def two_sp(ref, path): return sum(1 for l in lines(ref, path) if l.startswith('  ') and not l.startswith('   '))
chk(cnt(HEAD, PV, "'") == 22 and cnt(DEV, PV, "'") == 50 and cnt(HEAD, PS, "'") == 22 and cnt(DEV, PS, "'") == 65, "the reformat: apostrophes provision 50 -> 22, pre-suite 65 -> 22 (string quotes ' -> \"; the rest are prose)")
chk(two_sp(DEV, PV) == 0 and two_sp(HEAD, PV) == 85 and two_sp(DEV, PS) == 0 and two_sp(HEAD, PS) == 27, 'the reformat: exactly-2-space-indented lines 0 -> 85 (provision) / 0 -> 27 (pre-suite) — 4-space at develop, 2-space at head')
# the three cell files
RD = T+'provisionRedaction.test.ts'; ST = T+'preSuiteStreams.test.ts'; DQ = T+'provisionDriftQuarantine.test.ts'
chk(cnt(HEAD, RD, "    it('") == 5 and cnt(HEAD, ST, "    it('") == 2 and cnt(HEAD, DQ, "    it('") == 2, 'cells 5 / 2 / 2 = 9')
chk(at(HEAD, ST, 31, "const TSX = path.resolve(HERE, '..', '..', '..', 'node_modules', '.bin', 'tsx');") and at(HEAD, ST, 48, 'function runStep(script: string): SpawnOutcome {') and at(HEAD, ST, 62, '}'), 'preSuiteStreams :31 the package tsx / :48-62 runStep')
chk(at(HEAD, ST, 33, "const REFUSING_BASE = 'http://127.0.0.1:1';") and at(HEAD, ST, 53, "SECUURA_STACK_SLOT: '1',") and at(HEAD, ST, 56, "BOOTSTRAP_ADMIN_PASSWORD: 'unused-port-1-refuses-first',"), 'preSuiteStreams :33 refusing port / :53 slot / :56 the synthetic bootstrap value')
chk(at(HEAD, ST, 85, "if (tmpDir !== '' && fs.existsSync(tmpDir)) {") and at(HEAD, ST, 86, 'fs.rmSync(tmpDir, { recursive: true, force: true });') and at(HEAD, RD, 122, "if (tmp.dir !== '' && fs.existsSync(tmp.dir)) {") and at(HEAD, RD, 124, 'fs.rmSync(path.join(tmp.dir, entry), { force: true });') and at(HEAD, DQ, 99, 'afterEach(() => {') and at(HEAD, DQ, 106, 'fs.rmSync(path.join(tmp.dir, entry), { force: true });'), 'the rmSync sites :85-87 / :122-126 / :99-107 — each on its own mkdtemp')
chk(cnt(HEAD, RD, 'mkdtempSync') == 1 and cnt(HEAD, ST, 'mkdtempSync') == 1 and cnt(HEAD, DQ, 'mkdtempSync') == 1 and cnt(DEV, T+'manifestPaths.test.ts', 'rmSync') == 1, 'one mkdtemp per file; manifestPaths.test.ts at develop already uses rmSync (the precedent)')
chk(at(HEAD, RD, 36, "vi.mock('../../../../fixtures/manifest.ts', async (importActual) => {") and at(HEAD, RD, 46, 'quarantineManifest: (provisionedAt: string) => actual.quarantineManifest(provisionedAt, tmp.target),'), 'provisionRedaction :36 the manifest mock / :46 the real quarantineManifest aimed at the temp target')
chk(at(HEAD, RD, 161, "it('CONTROL — a server message with no secret in it passes through unchanged'") and at(HEAD, RD, 130, "it('replaces every occurrence of each secret and leaves everything else alone'") and at(HEAD, RD, 136, "it('ignores an empty secret"), 'provisionRedaction :130 every-occurrence / :136 empty-secret / :161 CONTROL')
chk(at(HEAD, RD, 154, 'expect(message).not.toContain(spec.password);') and at(HEAD, RD, 157, 'expect(message).toContain(spec.key);') and at(HEAD, RD, 158, 'expect(message).toContain(spec.email);'), 'provisionRedaction :154 not password / :157-158 key + email kept (G7 basis)')
# fixtures the cells depend on
MF = F+'manifest.ts'; AC = F+'actors.ts'
chk(at(HEAD, MF, 45, 'export function manifestPath(): string {') and at(HEAD, MF, 46, "return path.join(fixturesDir, 'generated', manifestFileName());") and at(HEAD, MF, 137, 'export function quarantineManifest(provisionedAt: string, target: string = manifestPath()): string | null {'), 'manifest.ts:45-46 manifestPath fixed / :137 quarantineManifest(provisionedAt, target = …)')
chk(at(HEAD, AC, 91, 'export function buildPassword(key: string, seed: string): string {') and at(HEAD, AC, 92, 'const password = `Ks256-${key}-${seed}-Pw!`;') and at(HEAD, AC, 97, '}') and at(HEAD, AC, 137, "if (!/^[a-z0-9-]{1,32}$/.test(seed)) {") and at(HEAD, AC, 119, 'return `ks256-${key}-${seed}@${GENERATED_EMAIL_DOMAIN}`.toLowerCase();'), 'actors.ts:91-97 buildPassword / :137 the seed alphabet / :119 buildEmail lower-cases (G5/G7 basis)')
# performance package facts
pj = blob(HEAD, PF+'package.json')[2] or ''
chk('"test:unit": "vitest run --config vitest.unit.config.ts"' in pj and '"format:check": "prettier --check --editorconfig --ignore-path .prettierignore ."' in pj and '"lint": "tsc -p tsconfig.json --noEmit && tsc -p tsconfig.node.json --noEmit && eslint . --ext .ts --config eslint.config.js"' in pj, 'performance package.json test:unit / format:check (over . only) / lint')
pc = blob(HEAD, PF+'prettier.config.js')[2] or ''
chk('printWidth: 120' in pc and 'tabWidth: 4' in pc and 'singleQuote: true' in pc, 'performance prettier.config.js: 120 / 4 / singleQuote (the head fixtures are 80 / 2 / double = prettier defaults)')
chk(len(git('ls-tree', '--name-only', M38, 'systemTest/.prettierrc', 'systemTest/.editorconfig', '.prettierrc', '.editorconfig', 'systemTest/fixtures/.prettierrc').split()) == 0, 'no prettier/editorconfig resolves for systemTest/fixtures/ (none at systemTest/, fixtures/ or the root)')
RS = 'Blockchain/Dev/scripts/run-shell-suites.sh'
chk(at(HEAD, RS, 49, '"Blockchain/Dev/scripts/__tests__"') and at(HEAD, RS, 50, '"systemTest/__tests__"'), 'run-shell-suites.sh:49-50 the two roots')
PT = 'systemTest/__tests__/pre_suite.test.sh'
chk(at(HEAD, PT, 92, 'npx tsx "$STEP"') and at(HEAD, PT, 139, 'run_step degraded-arm') and at(HEAD, PT, 104, 'run_step_unslotted noslot-arm') and at(HEAD, PT, 113, 'noslot-ci'), 'pre_suite.test.sh:92 tsx / :139 DEGRADED arm / :104 :113 the no-slot arms')
# --- git-side: parents, merge-base, counts, numstats (exact and -w), subtrees ---
chk(git('log', '-1', '--format=%P', HEAD).split() == [P3FA] and git('log', '-1', '--format=%P', P3FA).split() == [M38], 'head parent 3fa0a22b1 <- M38')
chk(git('merge-base', M38, HEAD).strip() == M38 and git('rev-list', '--count', f'{M38}..{HEAD}').strip() == '2', 'M38 is an ancestor; rev-list --count = 2')
chk(git('rev-parse', HEAD + '^{tree}').strip() == '562dacac87d5490ae172ca35b9a1ac465f8147fa' and git('rev-parse', HEAD + ':Blockchain').strip() == git('rev-parse', M38 + ':Blockchain').strip() == '38a814360031bb3a4f505276c7bb67e806200fc5', 'head tree 562dacac8; Blockchain subtree = M38 (38a814360)')
def numstat(*flags):
    rows = [l.split('\t') for l in git('diff', '--numstat', *flags, M38, HEAD).strip().split('\n') if l.count('\t') == 2]
    return {r[2].split('/')[-1]: (r[0], r[1]) for r in rows}
ns = numstat(); nw = numstat('-w')
chk(ns == {'pre-suite.ts': ('161', '150'), 'provision.ts': ('171', '126'), 'preSuiteStreams.test.ts': ('106', '0'), 'provisionDriftQuarantine.test.ts': ('154', '0'), 'provisionRedaction.test.ts': ('203', '0')}, f'numstat EXACT = {ns}')
chk(nw.get('pre-suite.ts') == ('33', '22') and nw.get('provision.ts') == ('65', '20'), f'numstat -w: pre-suite 33/22, provision 65/20 (got {nw.get("pre-suite.ts")} / {nw.get("provision.ts")})')
chk(sum(int(a) for a, b in ns.values()) == 795 and sum(int(b) for a, b in ns.values()) == 276, 'totals +795 -276 (the PR body says +332 -1)')
chk(len(git('ls-tree', '-r', '--name-only', HEAD, 'systemTest/performance/tests/unit').split()) - len(git('ls-tree', '-r', '--name-only', M38, 'systemTest/performance/tests/unit').split()) == 3 and len([x for x in git('ls-tree', '-r', '--name-only', HEAD, T).split() if x.endswith('.test.ts')]) == 11 and len([x for x in git('ls-tree', '-r', '--name-only', M38, T).split() if x.endswith('.test.ts')]) == 8, 'tests/unit +3 files; fixtures/ 11 test files at head / 8 at develop')
# the sibling PRs share no file with #989 (the merge-order claim)
mine = set(git('diff', '--name-only', M38, HEAD).split())
for n, h in ((916, '12507d200375a5ebcab1579920cb75e74a6391f1'), (988, '8cb99a002c5177bb1418ee1fab7cd2974076989a')):
    c = get(f'/compare/develop...{h}'); theirs = {f['filename'] for f in c.get('files') or []}
    chk(not (mine & theirs) and len(theirs) > 0, f'#{n} shares no file with #989 ({len(theirs)} files)')
p927 = get('/pulls/927'); chk(p927['state'] in ('open', 'closed') and set(f['filename'] for f in get('/pulls/927/files')) == {'systemTest/__tests__/pre_suite.test.sh', 'systemTest/__tests__/quarantine_call_sites.test.sh'}, f"#927 {p927['state']} merged={p927['merged']} head={p927['head']['sha'][:9]} — two shell files, none shared with #989")
# negative-token arm
if arg == '--neg-token':
    chk(cnt(HEAD, PV, 'throw new Error(') == 2, 'NEG: provision.ts throw new Error( demanded 2 (known 1)')
    chk(cnt(HEAD, PV, 'redactSecrets(envelope.error?.message') == 0, 'NEG: the T2 anchor demanded ABSENT at head (known 1)')
print(f'TALLY ok={ok} FAILS={fail} live_develop={live[:9]} {datetime.datetime.now().astimezone().strftime("%H:%M:%S")}')
sys.exit(1 if fail else 0)
PY
