#!/bin/bash
# controls_check.sh (ROUND 3, DELTA) — every :N anchor, blob, size and token count the round-3 brief cites for the
# delta cd5e62e96..a4d182bf9 (three files: confirmation.ts, anchorSubmission.ts, the new ks726-gate-f1-unreachable-chain
# test), checked against the GitHub contents API (blobs at head + current develop) AND git at the checkout (read verbs
# only), PLUS a re-assertion that the eight round-2 blobs this brief carries forward are UNCHANGED, plus the prompt's
# MAIL paragraph (with a positive control) and the deliverables' guard phrases (TIER 1, ROUND 3, the head SHA).
# Usage: bash controls_check.sh [--neg-head-as-dev] [--neg-token] [--neg-dev-as-0908]
#   --neg-head-as-dev  : current develop (0f37b85c8, which does NOT carry this round's three blobs) passed where the
#                        head is expected — must FAIL on the three round-3 blobs + their line anchors
#   --neg-token        : a token demanded PRESENT that is known ABSENT + one demanded ABSENT that is present + the MAIL
#                        paragraph demanded under a wrong verb (must FAIL 3)
#   --neg-dev-as-0908  : develop pinned at the 09-08 develop 067554d65 — MEASURED to FAIL on exactly 4: anchoring
#                        index.ts / cardano/index.ts / provider.ts / the yaml (all differ there — #728/#813 landed
#                        after 09-08); confirmation.ts, anchorSubmission.ts, reconciler.ts, anchoring.openapi.ts and
#                        generate-openapi.ts correctly stay green (measured, not assumed — none of them is #728's or
#                        #813's file) — a mix of ok/FAIL is the honest reading of this arm, not a design flaw
# Prints ok/FAIL lines and a tally; rc 1 if FAILS>0. No secrets printed (GH_TOKEN by name from the Secuura .env).
set -u
ARGS="${1:-}"
python3 - "$ARGS" <<'PY'
import sys, json, urllib.request, urllib.error, base64, subprocess, datetime, os, re
arg = sys.argv[1]
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
R = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-15_gate805r3'
tok = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
def git(*a):
    return subprocess.run(['git', '-C', R] + list(a), capture_output=True, text=True).stdout
HEAD = 'a4d182bf9efaa5b19b74c4a861f22746491e91b4'; R2 = 'cd5e62e96c373c2690b97bafb277683402f1e70b'; M44 = '346b491f27fb1cbf4d72cc1c86d417d0252a5f84'
DEV0 = '0f37b85c80b65d742a01e6529ee8194317a7cc57'; D0908 = '067554d65'
if arg == '--neg-head-as-dev': HEAD = DEV0
DEV = D0908 if arg == '--neg-dev-as-0908' else DEV0
D = 'Blockchain/Dev/'; A = D + 'services/anchoring/src/'
ok = fail = 0
def chk(cond, msg):
    global ok, fail
    if cond: ok += 1; print('ok   ' + msg)
    else: fail += 1; print('FAIL ' + msg)
print('controls_check (round 3)', arg or '(positive)', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
live = get('/branches/develop')['commit']['sha']; print('live develop =', live)
cache = {}
def blob(ref, path):
    k = (ref, path)
    if k not in cache:
        try:
            j = get('/contents/' + path + '?ref=' + ref)
            cache[k] = (j['sha'], j['size'], base64.b64decode(j['content']).decode('utf-8') if j.get('encoding') == 'base64' and j.get('content') else None)
        except urllib.error.HTTPError as e:
            cache[k] = ('ABSENT', None, None) if e.code == 404 else (('ERR', e.code, None))
    return cache[k]
def gitblob(ref, path):
    return git('rev-parse', '--verify', '-q', f'{ref}:{path}').strip() or 'ABSENT'
def gittext(ref, path):
    return git('show', f'{ref}:{path}')
def lines(ref, path): return (blob(ref, path)[2] or '').split('\n')
def at(ref, path, n, needle):
    L = lines(ref, path); return n <= len(L) and needle in L[n-1]
def cnt(ref, path, needle): return (blob(ref, path)[2] or '').count(needle)

# --- the three round-3 delta blobs at head, sizes asserted (the drafter's own measurement) ---
AS = A+'anchorSubmission.ts'; CF = A+'cardano/confirmation.ts'; F1T = A+'__tests__/ks726-gate-f1-unreachable-chain.test.ts'
EXPECT_HEAD = {
  AS:  ('d3ad106d8e5764a526456b3218e1e8d9ad1a38ba', 32849),
  CF:  ('5690eb24fe8dca6ac175fec021031524d6904221', 3369),
  F1T: ('82058c305ffaf375ef7941351063d4f236f878b9', 10327),
}
for path, (sha, size) in EXPECT_HEAD.items():
    b = blob(HEAD, path)
    chk(b[0] == sha and b[1] == size, f'{path.split("/")[-1]} blob {str(b[0])[:9]} size {b[1]} (expect {sha[:9]} {size}) at head')

# --- the eight round-2 blobs this brief carries forward, RE-ASSERTED unchanged at head (never copied) ---
CARRIED = {
  A+'index.ts': 'da4abd43292186da45c1533017fe042fa512bd43', A+'cardano/index.ts': 'd7b44482d54dd35550536cd3c24c0d9a4fb87c3f',
  A+'__tests__/ks726-write-ahead-tx-hash.test.ts': 'ea5495f58ec40fde9c462f8f3c56f450924229ec',
  A+'__tests__/ks726-review-f1-f3.test.ts': '6dc62c8dbcc1ff462b33af8b50ea0ffee5d4643f',
  A+'reconciler.ts': '55e2fe6949bc0e1c200e4ea314bd5262e2886bca', A+'verifyAnchorStatus.ts': 'b8b73078e456916c9d3d47c350046758975a1208',
  A+'anchoring.openapi.ts': '49b8b38da7764e071711ded751fa006ae21e808d',
}
for path, sha in CARRIED.items():
    chk(gitblob(HEAD, path) == sha, f'carried-forward {path.split("/")[-1]} blob {sha[:9]} unchanged at head (git, not API — avoids a 9th API round-trip)')
chk(gitblob(HEAD, D+'docs/openapi/secuura-api.yaml') == '122d3a2f84cf77bf2b7e2dc51489a0d5f823db1f', 'yaml blob 122d3a2f8 unchanged at head (git)')
# the round-2 untouched seven, minus confirmation.ts (now itself touched this round)
UNTOUCHED = {
  A+'cardano/provider.ts': '9232d4d0a8a5950a1096cfa473da6705751da77e', D+'scripts/generate-openapi.ts': 'e84acdc9e1be073751fcd6a8bb95504e23688019',
  D+'package-lock.json': '17d2061b397595677ae789683b0ca1d4b8398bec', D+'scripts/audit/audit-baseline.json': '03d1680e3c7a87f8df70e71082b67775536acde5',
  A+'__tests__/threadTokenMint.test.ts': 'b88b3a43ec5dcb8651b91d5df90e9dec42a1795f', A+'chainHealthStatus.ts': '8be4e7e166fc4b62c754393be2c6e639578ef33b',
}
for path, sha in UNTOUCHED.items():
    chk(gitblob(HEAD, path) == sha, f'untouched {path.split("/")[-1]} blob {sha[:9]} == develop\'s == round-2\'s (git)')

# --- develop: the thirteen judged paths, at the pinned DEV (M44's blobs unless --neg-dev-as-0908) ---
DEV_OK = {
  A+'anchorSubmission.ts': '66fa7e6f759284c2d96ca07fb53995e71b6c5f6b', A+'index.ts': '9f3eba10ccd40b3eb8b6716725e7efb4c01b5d88',
  A+'cardano/index.ts': 'c59345d03532ebf9ade1a6ba6d337756c11af4f2', D+'docs/openapi/secuura-api.yaml': 'd327a249a2ef7261b685d1baeb6aec3c9f7b677d',
  A+'reconciler.ts': 'dc65347f63b7e754acc370396d49569810aa7e9c', A+'anchoring.openapi.ts': 'ca7c92850ae9d80a86a22490382a842c61891c46',
  A+'cardano/provider.ts': '9232d4d0a8a5950a1096cfa473da6705751da77e', A+'cardano/confirmation.ts': 'c5042ca91b2e4fb211da50f30c097efd3a0b8902',
  D+'scripts/generate-openapi.ts': 'e84acdc9e1be073751fcd6a8bb95504e23688019',
}
# The SAME positive assertion run against whichever DEV is pinned (--neg-dev-as-0908 pins the 09-08 develop and
# lets the real differences fire naturally — index.ts / cardano/index.ts / provider.ts / the yaml / the generator
# all differ there because #728/#813 landed after 09-08; confirmation.ts / anchorSubmission.ts / reconciler.ts /
# anchoring.openapi.ts correctly stay green because they are NOT #728's/#813's files — a mix of ok/FAIL on this
# arm is the measured, honest result, not a design flaw in the arm).
for path, sha in DEV_OK.items():
    b = blob(DEV, path)
    chk(b[0] == sha, f'develop {path.split("/")[-1]} blob {str(b[0])[:9]} == M44 {sha[:9]}' + (' [NEG(0908) arm]' if arg == '--neg-dev-as-0908' else ''))
for path in (A+'__tests__/ks726-write-ahead-tx-hash.test.ts', A+'__tests__/ks726-review-f1-f3.test.ts', A+'verifyAnchorStatus.ts', A+'__tests__/ks726-gate-f1-unreachable-chain.test.ts'):
    b = blob(DEV, path)
    chk(b[0] == 'ABSENT', f'develop {path.split("/")[-1]} ABSENT (pinned state)')

# --- line anchors + counts on the API-fetched bytes: confirmation.ts (round 3's own file) ---
chk(len(lines(HEAD, CF)) == 99 and at(HEAD, CF, 9, "import { getTransaction } from './provider';"), 'confirmation.ts 98 lines / :9 import')
chk(at(HEAD, CF, 11, 'export interface ConfirmationResult {') and at(HEAD, CF, 26, '  polled?: number;') and at(HEAD, CF, 27, '  errored?: number;') and at(HEAD, CF, 28, '}'), 'confirmation.ts:11-28 ConfirmationResult (:26-27 the new counters)')
chk(at(HEAD, CF, 39, 'export async function waitForConfirmation(') and at(HEAD, CF, 45, '): Promise<ConfirmationResult> {'), 'confirmation.ts:39-45 the signature (return type unchanged)')
chk(at(HEAD, CF, 51, '  let polled = 0;') and at(HEAD, CF, 52, '  let errored = 0;'), 'confirmation.ts:51-52 the two counters initialised')
chk(at(HEAD, CF, 56, '      const tx = await getTransaction(txHash);') and at(HEAD, CF, 57, '      polled += 1;'), 'confirmation.ts:56-57 an ANSWERED attempt increments polled')
chk(at(HEAD, CF, 74, '    } catch (err: any) {') and at(HEAD, CF, 75, '      errored += 1;'), 'confirmation.ts:74-75 a THROWN attempt increments errored')
chk(at(HEAD, CF, 86, '  return {') and at(HEAD, CF, 87, '    confirmed: false,') and at(HEAD, CF, 88, '    polled,') and at(HEAD, CF, 89, '    errored,') and at(HEAD, CF, 90, '    error: polled === 0'), 'confirmation.ts:86-90 the not-confirmed return carries both counters')
chk(cnt(HEAD, CF, 'polled += 1;') == 1 and cnt(HEAD, CF, 'errored += 1;') == 1 and cnt(HEAD, CF, 'polled') >= 8 and cnt(HEAD, CF, 'errored') >= 7, 'confirmation.ts tamper anchors: polled += 1; (1), errored += 1; (1) — positive controls: polled/errored appear 8/7+ times total')
CFTXT = blob(HEAD, CF)[2] or ''
chk(len(re.findall(r'(?m)^\s*throw ', CFTXT)) == 0 and CFTXT.lower().count('throw') == 1, 'confirmation.ts: 0 CODE throw statements (regex, multiline); the word "throw" appears once, in the :48 comment only (positive control)')

# --- line anchors + counts on the API-fetched bytes: anchorSubmission.ts (the mapping) ---
chk(len(lines(HEAD, AS)) == 587 and at(HEAD, AS, 135, 'export interface ConfirmationLike {') and at(HEAD, AS, 147, '  polled?: number;') and at(HEAD, AS, 148, '  errored?: number;'), 'anchorSubmission.ts 586 lines / :135 ConfirmationLike / :147-148 the two optional counters')
chk(at(HEAD, AS, 242, '  async function reconfirmKnownSubmission(') and at(HEAD, AS, 246, "): Promise<'confirmed' | 'absent' | 'unknown'> {"), 'anchorSubmission.ts:242-246 the (unchanged) tri-state signature, shifted +8 from round 2\'s :234-238')
chk(at(HEAD, AS, 260, "if (confirmation.confirmed) {"), 'anchorSubmission.ts:260 the CONFIRMED check runs FIRST (the new branch cannot pre-empt a FOUND result)')
chk(at(HEAD, AS, 281, "      // #805 tier-1 gate F1 (2026-09-14): the poll ended without ONE attempt") and at(HEAD, AS, 292, '      if (confirmation.polled === 0) {') and at(HEAD, AS, 293, "        deps.log('warn', 'Anchor confirmation poll never reached the chain") and at(HEAD, AS, 296, '        return \'unknown\';') and at(HEAD, AS, 297, '      }') and at(HEAD, AS, 298, "      deps.log('warn', 'Anchor confirmation timed out") and at(HEAD, AS, 299, "      return 'absent';"), 'anchorSubmission.ts:281-299 the F1 fix — THE TAMPER ANCHOR at :292, THIRD in the if-chain after :260 (confirmed) and BEFORE the old :299 absent fallthrough')
chk(cnt(HEAD, AS, 'if (confirmation.polled === 0) {') == 1, 'anchorSubmission.ts tamper anchor T1: "if (confirmation.polled === 0) {" count 1')
# guard 5 / guard 3 shifted +26 from round 2 (spot check only — full re-litigation NOT commissioned this round)
chk(at(HEAD, AS, 489, 'if (writtenAheadTxHash && REAL_TX_64HEX.test(writtenAheadTxHash) && isChainReachableError(err)) {'), 'anchorSubmission.ts:489 guard 5\'s discriminated condition (round 2\'s :463, shift +26 — UNCHANGED text, confirmed present at the shifted line)')
chk(at(HEAD, AS, 529, "const found = await reconfirmKnownSubmission(anchorId, known, 'node reported the transaction is already included');"), 'anchorSubmission.ts:529 guard 3\'s re-poll call (round 2\'s :503, shift +26)')
chk(at(HEAD, AS, 542, '      const refusedAndAbsent =') and at(HEAD, AS, 543, "        found === 'absent' &&") and at(HEAD, AS, 544, '        known === writtenAheadTxHash &&') and at(HEAD, AS, 545, "        !ALREADY_INCLUDED_REPLY.test(message ?? '');"), 'anchorSubmission.ts:542-545 refusedAndAbsent (round 2\'s :516-519, shift +26 — the T7/T8/T9 anchors, NOT re-tampered this round)')

# --- the new test file: 8 source it( lines / 10 runtime cells (the for-loop over 3 UNREACHABLE shapes) ---
chk(len(lines(HEAD, F1T)) == 188 and cnt(HEAD, F1T, "  it(") == 8, 'ks726-gate-f1-unreachable-chain.test.ts 187 lines / 8 SOURCE it( lines (10 RUNTIME cells: the :137-154 for-loop over 3 UNREACHABLE shapes multiplies one source line into three cells — count both ways)')
chk(cnt(HEAD, F1T, 'UNREACHABLE') >= 4 and at(HEAD, F1T, 50, 'const UNREACHABLE: Array<{ label: string; make: () => Error }> = [') and at(HEAD, F1T, 51, "  { label: 'ServerError 503 on every attempt'") and at(HEAD, F1T, 52, "  { label: 'ServerError 402 (quota) on every attempt'") and at(HEAD, F1T, 53, "  { label: 'ClientError ENOTFOUND (network) on every attempt'"), 'test :50-54 the three UNREACHABLE shapes (503, 402, ENOTFOUND — E8/E8b/E8c)')
chk(at(HEAD, F1T, 101, "it('every attempt THROWS") and at(HEAD, F1T, 110, "it('CONTROL — every attempt ANSWERS") and at(HEAD, F1T, 118, "it('a mixed window") and at(HEAD, F1T, 126, "it('found on attempt 2"), 'test :101/:110/:118/:126 the four unit cells on waitForConfirmation')
chk(at(HEAD, F1T, 138, "it(`E8 — ${shape.label}: NO scheduleRetry") and at(HEAD, F1T, 156, "it('CONTROL — the chain ANSWERS") and at(HEAD, F1T, 169, "it('a mixed window (throw, not found, throw) reads ABSENT") and at(HEAD, F1T, 178, "it('CONTROL — an injected confirm that reports NO counters"), 'test :138 the E8-shape template (x3 runtime) / :156/:169/:178 the three harness-level cells')
chk(cnt(HEAD, F1T, "import { BlockfrostServerError, BlockfrostClientError } from '@blockfrost/blockfrost-js';") == 1 and cnt(HEAD, F1T, "import { waitForConfirmation } from '../cardano/confirmation';") == 1, 'test imports the SDK classes and the REAL poller (0 synthetic status_code doubles this round — contrast with round 2\'s six shipped cells)')

# --- git-side: parent, merge-base, tree, numstat, exact 3-file delta ---
chk(git('log', '-1', '--format=%P', HEAD).split() == [R2], 'head parent = cd5e62e96 (round 2\'s head — ONE parent, fast-forward)')
chk(git('cat-file', '-t', HEAD).strip() == 'commit', 'the head object is present in the local store (git cat-file -t) — no fetch run by the drafter')
chk(git('merge-base', HEAD, DEV0).strip() == M44, 'merge-base(head, current develop) = STILL M44 (unaffected by this round)')
chk(git('rev-list', '--count', f'{M44}..{HEAD}').strip() == '8', 'rev-list --count M44..head = 8 (was 7 at round 2)')
chk(git('rev-parse', HEAD + '^{tree}').strip() == '41be8de2b90c98f24a5333f7628b68549ef82894', 'head tree 41be8de2b')
chk(sorted(git('diff', '--name-only', R2, HEAD).split()) == sorted([F1T.replace('src/', 'src/'), AS, CF]), f'git diff --name-only cd5e62e96..head = EXACTLY the three round-3 files')
ns = sorted((l.split('\t') for l in git('diff', '--numstat', R2, HEAD).strip().split('\n') if l.count('\t') == 2), key=lambda x: x[2])
chk([x[:2] for x in ns] == [['187', '0'], ['29', '3'], ['25', '1']] and len(ns) == 3, 'numstat cd5e62e96..head = the three rows, sorted by path (187/0 test, 29/3 anchorSubmission.ts, 25/1 confirmation.ts — total +241 -4)')
chk(len(git('diff', '--name-only', M44, DEV0).strip().split('\n')) == 92, 'M44..current-develop touches 92 files total (git); the Blockchain/Dev subset is 11, none under services/anchoring/ or the yaml — see the next check')
devfiles = [f for f in git('diff', '--name-only', M44, DEV0).split('\n') if f.startswith(D)]
chk(len(devfiles) == 11 and not any('services/anchoring' in f or f.endswith('secuura-api.yaml') or 'generate-openapi' in f or 'spec-examples' in f or 'packages/shared/src/openapi' in f or f.endswith('package-lock.json') for f in devfiles), f'M44..develop under Blockchain/Dev/ = 11 files, 0 guarded-path hits: {[f.split("/")[-1] for f in devfiles]}')

# --- pristine sha256 for the tamper restore mechanic (re-derived, not trusted from the brief) ---
sha_as = subprocess.run(['bash', '-c', f'git -C {R} show {HEAD}:{AS.replace(chr(39), "")} | shasum -a 256'], capture_output=True, text=True).stdout.split()[0]
sha_cf = subprocess.run(['bash', '-c', f'git -C {R} show {HEAD}:{CF} | shasum -a 256'], capture_output=True, text=True).stdout.split()[0]
chk(sha_as == '173d350af394931131deca0ecd301aef1b363c6fc7b71eb000fb04d42711f92b', f'anchorSubmission.ts pristine sha256 re-derived = {sha_as[:16]} (matches the brief\'s printed value — re-checked, not trusted)')
chk(sha_cf == 'a7ddcdcd7c15a622485c0e1fa23d38522d7e56c803cc8102744f80f3a5493b43', f'confirmation.ts pristine sha256 re-derived = {sha_cf[:16]} (matches the brief\'s printed value — re-checked, not trusted)')

# --- the deliverables: the MAIL paragraph (with a positive control), the guard phrases, the brief path, the SHA ---
PR = open(os.path.join(G, '2026-09-15_secuura-805-ks726-tier1-r3.prompt.txt'), encoding='utf-8').read()
BR = open(os.path.join(G, '2026-09-15_secuura-805-ks726-tier1-r3.md'), encoding='utf-8').read()
mail_para = 'MAIL YOUR VERDICT to wednesday-agent@agentmail.to when the pass is complete, using\nthe project\'s send_brief.sh.'
chk(PR.count(mail_para) == 1 and PR.count('the verdict MAIL is the wait signal') == 1 and PR.count('[QA -> Wednesday] TIER 1 GATE #805 (KS-726) a4d182bf9 — <VERDICT>') == 1 and PR.startswith('ultrathink\n'), 'prompt: the MAIL YOUR VERDICT paragraph verbatim (1), the subject (1), ultrathink first line (positive control)')
chk(PR.count('SEND YOUR VERDICT') == 0 and PR.count('/briefs/2026-09-15_secuura-805-ks726-tier1-r3.md') == 1, 'prompt: no rival verb (SEND YOUR VERDICT 0 — negative control); the INSTALLED brief path once')
for ph in ('NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout', 'no memory maintenance', 'NEVER print a credential value', 'ROUND 3', HEAD):
    chk(ph.lower() in PR.lower(), f'prompt carries {ph[:48]!r}')
chk('TIER 1' in BR and 'ROUND 3' in BR and HEAD in BR and BR.count('[QA -> Wednesday] TIER 1 GATE #805 (KS-726) a4d182bf9 — <VERDICT>') == 1 and 'predicted-by' in BR, 'brief carries TIER 1, ROUND 3, the head SHA, the subject once, predicted-by')
chk(len(re.findall(r'\| drafter \|$', BR, re.M)) + BR.count('/ drafter') + BR.count('predicted-by: drafter') >= 5 and 'Wednesday-read' not in BR, 'brief: >= 5 predictions carry drafter (table rows ending "| drafter |" or "/ drafter N", plus inline predicted-by: drafter — a smaller DELTA brief than round 2\'s 20+, honestly sized to this round\'s scope); no Wednesday-read row composed here')
chk('cd5e62e96' in BR and 'F1' in BR, 'brief names round 2\'s head (the parent) and F1 (the finding it closes)')

# negative-token arm
if arg == '--neg-token':
    chk(cnt(HEAD, AS, "return 'unknown';") == 0, 'NEG: anchorSubmission.ts "return \'unknown\';" demanded ABSENT at head (known present, at :296 and :303-ish — the catch block\'s own unknown return)')
    chk(cnt(HEAD, CF, 'polled += 1;') == 0, 'NEG: confirmation.ts "polled += 1;" demanded ABSENT at head (known present, count 1)')
    chk(PR.count('SEND YOUR VERDICT to wednesday-agent@agentmail.to') == 1, 'NEG: the MAIL paragraph demanded under a rival verb (known 0)')
print(f'TALLY ok={ok} FAILS={fail} live_develop={live[:9]} {datetime.datetime.now().astimezone().strftime("%H:%M:%S")}')
sys.exit(1 if fail else 0)
PY
