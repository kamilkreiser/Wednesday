#!/bin/bash
# controls_check.sh — every :N anchor, blob, size, line count and token count the #805 brief cites, checked against the
# GitHub contents API (blobs at the head + develop M46 + the live develop) AND git at the checkout (read verbs only), plus
# the prompt's MAIL paragraph (with a positive control) and the deliverables' guard phrases.
# Usage: bash controls_check.sh [--neg-head-as-dev] [--neg-token] [--neg-dev-as-0908]
#   --neg-head-as-dev  : develop M46 passed where the head is expected (must FAIL on the nine PR blobs + the new anchors)
#   --neg-token        : a token demanded PRESENT that is known ABSENT + one demanded ABSENT that is present + the MAIL
#                        paragraph demanded under a wrong verb (must FAIL 3)
#   --neg-dev-as-0908  : develop pinned at the 09-08 develop 067554d65 (the branch's earlier merge-in; must FAIL: anchoring
#                        index.ts / cardano/index.ts / the yaml differ there — KS-671 #728 and #813 landed after it)
# Prints ok/FAIL lines and a tally; rc 1 if FAILS>0. No secrets printed (GH_TOKEN by name from the Secuura .env).
set -u
ARGS="${1:-}"
python3 - "$ARGS" <<'PY'
import sys, json, urllib.request, urllib.error, base64, subprocess, datetime, os, re
arg = sys.argv[1]
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
R = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate805'
tok = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
def git(*a):
    return subprocess.run(['git', '-C', R] + list(a), capture_output=True, text=True).stdout
HEAD = 'cd5e62e96c373c2690b97bafb277683402f1e70b'; M44 = '346b491f27fb1cbf4d72cc1c86d417d0252a5f84'; M46 = 'bc067e3e91821116f3344b2aa5a1d7a5cc968d18'
M45 = '852e1fff773bd358170c11334d59496f05fdd8a7'; R1 = '1885d5166d5ca04e62eb8d1d6e9c8c2d496184f9'; P97 = '97e2161fa'; D0908 = '067554d65'
if arg == '--neg-head-as-dev': HEAD = M46
DEV = D0908 if arg == '--neg-dev-as-0908' else M46
D = 'Blockchain/Dev/'; A = D + 'services/anchoring/src/'
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
            cache[k] = ('ABSENT', None, None) if e.code == 404 else (('ERR', e.code, None))
    return cache[k]
def gitblob(ref, path):
    return git('rev-parse', '--verify', '-q', f'{ref}:{path}').strip() or 'ABSENT'
def gittext(ref, path):
    return git('show', f'{ref}:{path}')
# --- blobs at the head + develop (the brief's TARGET table); sizes asserted where the drafter measured them (head) ---
EXPECT = {
  (HEAD, A+'anchorSubmission.ts'): ('7879a6ba14a1411fc7cdc14afb786252ca199d69', 31270), (HEAD, A+'index.ts'): ('da4abd43292186da45c1533017fe042fa512bd43', 86184),
  (HEAD, A+'__tests__/ks726-write-ahead-tx-hash.test.ts'): ('ea5495f58ec40fde9c462f8f3c56f450924229ec', 21263), (HEAD, A+'__tests__/ks726-review-f1-f3.test.ts'): ('6dc62c8dbcc1ff462b33af8b50ea0ffee5d4643f', 7831),
  (HEAD, A+'verifyAnchorStatus.ts'): ('b8b73078e456916c9d3d47c350046758975a1208', 2287), (HEAD, A+'cardano/index.ts'): ('d7b44482d54dd35550536cd3c24c0d9a4fb87c3f', 12019),
  (HEAD, A+'reconciler.ts'): ('55e2fe6949bc0e1c200e4ea314bd5262e2886bca', 5631), (HEAD, A+'anchoring.openapi.ts'): ('49b8b38da7764e071711ded751fa006ae21e808d', 19538),
  (HEAD, A+'cardano/provider.ts'): ('9232d4d0a8a5950a1096cfa473da6705751da77e', 13398), (HEAD, A+'cardano/confirmation.ts'): ('c5042ca91b2e4fb211da50f30c097efd3a0b8902', 2222),
  (HEAD, D+'scripts/generate-openapi.ts'): ('e84acdc9e1be073751fcd6a8bb95504e23688019', None), (HEAD, D+'scripts/audit/audit-baseline.json'): ('03d1680e3c7a87f8df70e71082b67775536acde5', None),
  (DEV, A+'anchorSubmission.ts'): ('66fa7e6f759284c2d96ca07fb53995e71b6c5f6b', None), (DEV, A+'index.ts'): ('9f3eba10ccd40b3eb8b6716725e7efb4c01b5d88', None),
  (DEV, A+'__tests__/ks726-write-ahead-tx-hash.test.ts'): ('ABSENT', None), (DEV, A+'__tests__/ks726-review-f1-f3.test.ts'): ('ABSENT', None), (DEV, A+'verifyAnchorStatus.ts'): ('ABSENT', None),
  (DEV, A+'cardano/index.ts'): ('c59345d03532ebf9ade1a6ba6d337756c11af4f2', None), (DEV, A+'reconciler.ts'): ('dc65347f63b7e754acc370396d49569810aa7e9c', None),
  (DEV, A+'anchoring.openapi.ts'): ('ca7c92850ae9d80a86a22490382a842c61891c46', None), (DEV, A+'cardano/provider.ts'): ('9232d4d0a8a5950a1096cfa473da6705751da77e', None),
  (DEV, A+'cardano/confirmation.ts'): ('c5042ca91b2e4fb211da50f30c097efd3a0b8902', None), (DEV, D+'scripts/generate-openapi.ts'): ('e84acdc9e1be073751fcd6a8bb95504e23688019', None),
}
for (ref, path), (sha, size) in EXPECT.items():
    b = blob(ref, path)
    chk(b[0] == sha and (size is None or b[1] == size), f'{ref[:9]} {path.split("/")[-1]} blob {str(b[0])[:9]} size {b[1]} (expect {sha[:9]} {size})')
chk(gitblob(HEAD, D+'docs/openapi/secuura-api.yaml') == '122d3a2f84cf77bf2b7e2dc51489a0d5f823db1f' and gitblob(DEV, D+'docs/openapi/secuura-api.yaml') == 'd327a249a2ef7261b685d1baeb6aec3c9f7b677d', 'yaml blobs head 122d3a2f8 / develop d327a249a (git)')
chk(gitblob(HEAD, D+'package-lock.json') == gitblob(DEV, D+'package-lock.json') == '17d2061b397595677ae789683b0ca1d4b8398bec', 'lockfile 17d2061b3 unchanged')
chk(gitblob(HEAD, A+'__tests__/threadTokenMint.test.ts') == gitblob(DEV, A+'__tests__/threadTokenMint.test.ts') == 'b88b3a43e' + gitblob(DEV, A+'__tests__/threadTokenMint.test.ts')[9:] and gitblob(HEAD, A+'chainHealthStatus.ts') == gitblob(DEV, A+'chainHealthStatus.ts'), 'threadTokenMint.test.ts b88b3a43e and chainHealthStatus.ts unchanged head == develop')
# --- line anchors + token counts on the API-fetched bytes (the brief's :N) ---
def lines(ref, path): return (blob(ref, path)[2] or '').split('\n')
def at(ref, path, n, needle):
    L = lines(ref, path); return n <= len(L) and needle in L[n-1]
def cnt(ref, path, needle): return (blob(ref, path)[2] or '').count(needle)
def lcnt_i(ref, path, needle): return sum(1 for l in lines(ref, path) if needle.lower() in l.lower())   # case-insensitive LINE count = /usr/bin/grep -i -c
AS = A+'anchorSubmission.ts'
chk(len(lines(HEAD, AS)) == 561 and len(lines(DEV, AS)) == 345, 'anchorSubmission.ts 560 lines at head / 344 at develop (split +1)')
chk(at(HEAD, AS, 3, 'KS-705 — ANCHOR SUBMISSION') and at(HEAD, AS, 5, 'The real-Cardano half of `processAnchor`') and at(HEAD, AS, 9, 'a real transaction).'), 'anchorSubmission.ts:3-9 the header (bootless by design)')
chk(at(HEAD, AS, 38, 'NOT HANDLED') and at(HEAD, AS, 41, 'HTTP 400') and at(HEAD, AS, 46, 'BadInputsUTxO') and at(HEAD, AS, 48, '"Already included" on a row carrying NO real transaction hash') and at(HEAD, AS, 52, 'which this module does not and cannot fix.') and at(HEAD, AS, 57, 'so this entry stands as written.'), 'anchorSubmission.ts:38-57 NOT HANDLED (:41 400, :46 BadInputsUTxO, :48-52 the no-hash entry)')
chk(lines(HEAD, AS)[37:57] == lines(DEV, AS)[37:57] if len(lines(DEV, AS)) > 57 else False, 'the NOT HANDLED block :38-57 is byte-identical to develop (unchanged this round)')
chk(at(HEAD, AS, 72, 'Guard 5 rests ONLY a LOST reply.') and at(HEAD, AS, 73, '`isChainReachableError`') and at(HEAD, AS, 74, 'BadInputsUTxO, ValueNotConservedUTxO') and at(HEAD, AS, 78, 'ruled 2026-09-14') and at(HEAD, AS, 82, 'when the bounded poll shows it ABSENT does the ordinary retry follow.'), 'anchorSubmission.ts:72-82 the header re-wording')
chk(at(HEAD, AS, 95, "import { isChainReachableError } from './cardano/provider';") and cnt(HEAD, AS, '\nimport ') == 1, 'anchorSubmission.ts:95 the ONLY import')
chk(at(HEAD, AS, 98, 'const REAL_TX_64HEX = /^[0-9a-f]{64}$/i;'), 'anchorSubmission.ts:98 REAL_TX_64HEX')
chk(at(HEAD, AS, 112, 'const ALREADY_INCLUDED_REPLY = /already been included/i;') and at(HEAD, AS, 114, 'const ALREADY_SUBMITTED_REPLIES = [') and at(HEAD, AS, 115, '/all inputs are spent/i,') and at(HEAD, AS, 117, '];'), 'anchorSubmission.ts:112-117 the two reply matchers')
chk(at(HEAD, AS, 120, 'export function isAlreadySubmittedError(err: unknown): boolean {') and at(HEAD, AS, 124, '}'), 'anchorSubmission.ts:120-124 isAlreadySubmittedError')
chk(at(HEAD, AS, 158, 'bumpRetryCount: (anchorId: string) => Promise<void>;'), 'anchorSubmission.ts:158 the bumpRetryCount dep')
chk(at(HEAD, AS, 214, 'function knownChainSubmission(anchor: AnchorSnapshot | null): string | undefined {') and at(HEAD, AS, 216, "if (anchor.status !== 'submitting' && anchor.status !== 'submitted' && anchor.status !== 'confirmed') {") and at(HEAD, AS, 221, '}'), 'anchorSubmission.ts:214-221 knownChainSubmission (:216 the status set)')
chk(at(HEAD, AS, 234, 'async function reconfirmKnownSubmission(') and at(HEAD, AS, 238, "): Promise<'confirmed' | 'absent' | 'unknown'> {") and at(HEAD, AS, 239, '// The return value is read by guard 3 only (KS-726)') and at(HEAD, AS, 242, 'nothing about the chain and keeps today') , 'anchorSubmission.ts:234-242 the tri-state signature + its comment')
chk(at(HEAD, AS, 247, "if (current?.status === 'confirmed') return 'confirmed';") and at(HEAD, AS, 251, 'if (confirmation.confirmed) {') and at(HEAD, AS, 270, "return 'confirmed';") and at(HEAD, AS, 272, "deps.log('warn', 'Anchor confirmation timed out'") and at(HEAD, AS, 273, "return 'absent';") and at(HEAD, AS, 274, '} catch (err) {') and at(HEAD, AS, 276, "return 'unknown';") and at(HEAD, AS, 277, '}') and at(HEAD, AS, 278, '}'), "anchorSubmission.ts:247/:251/:270/:272-273 'absent'/:274-277 'unknown'/:278")
chk(at(HEAD, AS, 286, 'const alreadyKnown = knownChainSubmission(anchor);') and at(HEAD, AS, 290, '}'), 'anchorSubmission.ts:286-290 guard 1')
chk(at(HEAD, AS, 343, 'onSigned: async (txHash) => {') and at(HEAD, AS, 360, "await deps.updateStatus(anchorId, { status: 'submitting', transactionHash: txHash });") and at(HEAD, AS, 361, 'writtenAheadTxHash = txHash;') and at(HEAD, AS, 362, '},'), 'anchorSubmission.ts:343-362 the onSigned hook (:360 the write, :361 assigned AFTER)')
chk(at(HEAD, AS, 366, 'submittedTxHash = submission.txHash;') and at(HEAD, AS, 367, "await deps.updateStatus(anchorId, { status: 'submitted', transactionHash: submission.txHash });") and at(HEAD, AS, 377, "status: 'confirmed',"), 'anchorSubmission.ts:366-367/:377 the submitted + confirmed writes')
chk(at(HEAD, AS, 417, 'if (submittedTxHash && REAL_TX_64HEX.test(submittedTxHash)) {') and at(HEAD, AS, 423, '}'), 'anchorSubmission.ts:417-423 guard 4')
chk(at(HEAD, AS, 425, '// Guard 5 (KS-726) — the write-ahead branch.') and at(HEAD, AS, 434, '// Guard 5 covers ONE case: the reply was LOST.') and at(HEAD, AS, 443, '// fail-and-retry write — a ~15 s recovery instead of the reconciler') and at(HEAD, AS, 447, '// Why the LOST-reply case does NOT re-poll') and at(HEAD, AS, 462, '// on chain. Ordering it here removes the window rather than documenting it.'), 'anchorSubmission.ts:425-462 the guard-5 comment (:434 ONE case, :443 the ~15 s claim)')
chk(at(HEAD, AS, 463, 'if (writtenAheadTxHash && REAL_TX_64HEX.test(writtenAheadTxHash) && isChainReachableError(err)) {'), 'anchorSubmission.ts:463 THE DISCRIMINATED CONDITION')
chk(at(HEAD, AS, 467, "deps.log('warn', 'Node REFUSED the written-ahead transaction") and at(HEAD, AS, 468, 'statusCode: (err as { status_code?: number })?.status_code, error: message,') and at(HEAD, AS, 469, '});'), 'anchorSubmission.ts:467-469 the fall-through log')
chk(at(HEAD, AS, 470, '} else if (writtenAheadTxHash && REAL_TX_64HEX.test(writtenAheadTxHash)) {') and at(HEAD, AS, 471, 'await deps.updateStatus(anchorId, {') and at(HEAD, AS, 472, "status: 'submitting',") and at(HEAD, AS, 483, 'transactionHash: writtenAheadTxHash,') and at(HEAD, AS, 484, 'errorMessage: `Submit reply lost after signing; tx ${writtenAheadTxHash} may be on chain') and at(HEAD, AS, 485, '});'), 'anchorSubmission.ts:470-485 the LOST-reply branch (:483 F2 carry)')
chk(at(HEAD, AS, 486, '// #805 review (2026-09-08), note 2: NO `bumpRetryCount` here.') and at(HEAD, AS, 489, '// spend budget that a later front-door re-anchor inherits reduced.') and at(HEAD, AS, 490, "deps.log('warn', 'Anchor submit failed AFTER the hash was written ahead") and at(HEAD, AS, 493, 'return;') and at(HEAD, AS, 494, '}'), 'anchorSubmission.ts:486-494 note 2 + the rest + return')
chk(at(HEAD, AS, 499, 'if (isAlreadySubmittedError(err)) {') and at(HEAD, AS, 500, 'const current = await deps.getAnchor(anchorId);') and at(HEAD, AS, 501, 'const known = knownChainSubmission(current);') and at(HEAD, AS, 502, 'if (known) {') and at(HEAD, AS, 503, "const found = await reconfirmKnownSubmission(anchorId, known, 'node reported the transaction is already included');"), 'anchorSubmission.ts:499-503 guard 3 (the re-poll FIRST)')
chk(at(HEAD, AS, 516, 'const refusedAndAbsent =') and at(HEAD, AS, 517, "found === 'absent' &&") and at(HEAD, AS, 518, 'known === writtenAheadTxHash &&') and at(HEAD, AS, 519, "!ALREADY_INCLUDED_REPLY.test(message ?? '');") and at(HEAD, AS, 520, 'if (!refusedAndAbsent) return;') and at(HEAD, AS, 521, "deps.log('warn', 'The transaction just written ahead is ABSENT on chain") and at(HEAD, AS, 523, '});') and at(HEAD, AS, 524, '} else {') and at(HEAD, AS, 530, '}') and at(HEAD, AS, 531, '}'), 'anchorSubmission.ts:516-531 refusedAndAbsent (:517/:518/:519 the three clauses, :520 the return)')
chk(at(HEAD, AS, 533, 'const currentRetry = anchor.retryCount + 1;') and at(HEAD, AS, 535, 'await deps.updateStatus(anchorId, {') and at(HEAD, AS, 536, "status: 'failed',") and at(HEAD, AS, 537, "errorMessage: message || 'Cardano submission failed',") and at(HEAD, AS, 538, '});') and at(HEAD, AS, 539, 'await deps.bumpRetryCount(anchorId);'), 'anchorSubmission.ts:533-539 the terminal failed write + bump')
chk(at(HEAD, AS, 552, 'if (currentRetry < maxRetries) {') and at(HEAD, AS, 555, "await deps.updateStatus(anchorId, { status: 'pending' });") and at(HEAD, AS, 556, 'deps.scheduleRetry(anchorId, backoff);') and at(HEAD, AS, 557, '}'), 'anchorSubmission.ts:552-557 pending + scheduleRetry')
# tamper anchors (count 1 each at head; 0 at develop where the round-2 text is new)
chk(cnt(HEAD, AS, '} else if (writtenAheadTxHash && REAL_TX_64HEX.test(writtenAheadTxHash)) {') == 1 and cnt(DEV, AS, 'writtenAheadTxHash') == 0, 'T1 anchor count 1 (develop 0 — control)')
chk(cnt(HEAD, AS, "status: 'failed',") == 1 and cnt(HEAD, AS, 'await deps.bumpRetryCount(anchorId);') == 1, "T2 anchors `status: 'failed',` 1 and `await deps.bumpRetryCount(anchorId);` 1")
chk(cnt(HEAD, AS, 'transactionHash: writtenAheadTxHash,') == 1 and cnt(HEAD, AS, 'txHash: writtenAheadTxHash,') == 2, 'T3 anchor `transactionHash: writtenAheadTxHash,` 1 (the two log lines use txHash: — 2, not the anchor)')
chk(cnt(HEAD, AS, '&& isChainReachableError(err)') == 1 and cnt(DEV, AS, 'isChainReachableError') == 0, 'T4 anchor `&& isChainReachableError(err)` 1 (develop 0)')
chk(cnt(HEAD, AS, "found === 'absent' &&") == 1 and cnt(HEAD, AS, "return 'absent';") == 1 and cnt(HEAD, AS, 'known === writtenAheadTxHash &&') == 1 and cnt(HEAD, AS, "!ALREADY_INCLUDED_REPLY.test(message ?? '')") == 1, 'T5/T6/T7/T8/T9 anchors count 1 each')
# the round-1 READY markers (case-insensitive LINE counts = /usr/bin/grep -i -c), head vs develop
for m, h, d in (('400', 1, 1), ('BadInputs', 2, 1), ('refus', 6, 0), ('status_code', 4, 0), ('definitive', 5, 0), ('reply lost', 2, 0), ('isChainReachableError', 5, 0), ("'absent'", 4, 0), ("'unknown'", 3, 0), ('ALREADY_INCLUDED_REPLY', 3, 0), ('bumpRetryCount', 3, 2), ('NOT HANDLED', 3, 3)):
    chk(lcnt_i(HEAD, AS, m) == h and lcnt_i(DEV, AS, m) == d, f'marker {m!r} lines {h} at head / {d} at develop')
TT = A+'__tests__/ks726-write-ahead-tx-hash.test.ts'
chk(len(lines(HEAD, TT)) == 463 and cnt(HEAD, TT, "  it('") == 13, 'ks726-write-ahead-tx-hash.test.ts 462 lines / 13 it( cells')
chk(at(HEAD, TT, 24, 'WHAT IS NOT TESTED HERE') and at(HEAD, TT, 29, 'reach its subject. It is named here so the gap is visible.'), 'test :24-29 the onSigned-contract gap named')
chk(at(HEAD, TT, 51, "const LOST_REPLY = new Error('socket hang up (ECONNRESET) reading submit response');"), 'test :51 LOST_REPLY')
chk(at(HEAD, TT, 72, 'function makeHarness(opts: {') and at(HEAD, TT, 135, '}'), 'test :72-135 makeHarness')
chk(at(HEAD, TT, 142, "it('writes the hash ahead, and the write-ahead lands BEFORE the submitted write'"), 'test :142')
chk(at(HEAD, TT, 172, "it('rests the row in submitting, names the tx, and never submits again'") and at(HEAD, TT, 188, 'expect(h.deps.bumpRetryCount).not.toHaveBeenCalled();') and at(HEAD, TT, 189, 'expect(h.row.retryCount).toBe(0);'), 'test :172 + :188-189 (retryCount 0, note 2)')
chk(at(HEAD, TT, 211, "it('never writes failed at any point — asserted on the call sequence, not the end state'"), 'test :211 the ORDERING cell')
chk(at(HEAD, TT, 245, "it('prefers guard 4 (submit returned) over guard 5 (reply lost) when both apply'") and at(HEAD, TT, 283, "it('does not fire for a fabricated tx ref") and at(HEAD, TT, 318, "it('re-polls the written-ahead hash instead of minting a second transaction'") and at(HEAD, TT, 341, "it('CONTROL — a pending row is still submitted"), 'test :245/:283/:318/:341')
chk(at(HEAD, TT, 353, "describe('KS-726 — a DEFINITIVE node rejection keeps the ordinary retry") and at(HEAD, TT, 366, 'function throwingSubmit(reply: Error) {') and at(HEAD, TT, 371, '}') and at(HEAD, TT, 372, "const refused = (message: string) => Object.assign(new Error(message), { status_code: 400 });"), 'test :353 the round-2 describe / :366-371 throwingSubmit / :372 the SYNTHETIC status_code')
chk(at(HEAD, TT, 374, "it('a 400 the node answered with (ValueNotConservedUTxO) after onSigned") and at(HEAD, TT, 388, "it('CONTROL — the same throw with NO status_code") and at(HEAD, TT, 406, "it('a 400 \"All inputs are spent\" after onSigned, the re-poll finds the hash ABSENT") and at(HEAD, TT, 424, "it('CONTROL — a 400 \"already been included\" after onSigned") and at(HEAD, TT, 436, "it('CONTROL — a 400 \"All inputs are spent\" whose re-poll FINDS the hash") and at(HEAD, TT, 448, "it('CONTROL — a 400 \"All inputs are spent\" whose re-poll THROWS") and at(HEAD, TT, 462, '});'), 'test :374/:388/:406/:424/:436/:448 the six cells / :462 end')
chk(at(HEAD, TT, 443, 'expect(h.deps.submit).toHaveBeenCalledTimes(1);') and cnt(HEAD, TT, 'BlockfrostServerError') == 0 and cnt(HEAD, TT, 'waitForConfirmation') == 0, 'test :443 h.deps.submit (the slip corrected); the file never imports the SDK class or the real poller (0/0)')
FT = A+'__tests__/ks726-review-f1-f3.test.ts'
chk(len(lines(HEAD, FT)) == 154 and cnt(HEAD, FT, "  it('") == 7 and at(HEAD, FT, 110, "it('carries transactionHash even when the write-ahead write was SWALLOWED'") and at(HEAD, FT, 127, "it('carries it in the ordinary case too") and at(HEAD, FT, 137, "it('does not arm guard 5, and takes the ordinary retry path instead'"), 'ks726-review-f1-f3.test.ts 153 lines / 7 cells / :110 :127 (F2) :137 (F3)')
IX = A+'index.ts'
chk(len(lines(HEAD, IX)) == 2105 and at(HEAD, IX, 1687, 'const submitAnchorToChain = createAnchorSubmitter({') and at(HEAD, IX, 1706, 'confirm: (txHash, onStatusUpdate) => waitForConfirmation(txHash, 30, 10_000, 60_000, onStatusUpdate),') and at(HEAD, IX, 1708, 'bumpRetryCount: async (anchorId) => {') and at(HEAD, IX, 1712, '},') and at(HEAD, IX, 1713, 'scheduleRetry: (anchorId, delayMs) => { setTimeout(() => { processAnchor(anchorId); }, delayMs); },') and at(HEAD, IX, 1716, '});'), 'index.ts:1687-1716 the submitter deps (:1706 the 30 / 10 s / 60 s poll)')
chk(at(HEAD, IX, 1829, 'onSigned: async (txHash) => {') and at(HEAD, IX, 1837, 'for (const anchorId of anchorIds) {') and at(HEAD, IX, 1838, "await dbUpdateAnchorStatus(anchorId, { status: 'submitting', transactionHash: txHash });") and at(HEAD, IX, 1840, 'batchWrittenAheadTxHash = txHash;') and at(HEAD, IX, 1841, '},'), 'index.ts:1829-1841 the batch onSigned (note 1: assigned AFTER the writes)')
chk(at(HEAD, IX, 1894, 'if (batchWrittenAheadTxHash && REAL_TX_64HEX_RETRY.test(batchWrittenAheadTxHash)) {') and at(HEAD, IX, 1897, "status: 'submitting',") and at(HEAD, IX, 1911, 'return;') and at(HEAD, IX, 1912, '}') and at(HEAD, IX, 1914, "await dbUpdateBatchStatus(batchId, 'failed');") and cnt(HEAD, IX, 'isChainReachableError') == 0, 'index.ts:1894-1912 the batch blanket (no discriminator: isChainReachableError 0 in index.ts) / :1914 the terminal failed')
chk(at(HEAD, IX, 2033, "minAgeMs: parseInt(process.env.ANCHOR_RECONCILE_MIN_AGE_MS || String(10 * 60_000), 10),") and at(HEAD, IX, 2034, "giveUpMs: parseInt(process.env.ANCHOR_RECONCILE_GIVE_UP_MS || String(24 * 60 * 60_000), 10),"), 'index.ts:2033-2034 the reconciler bounds (10 min / 24 h)')
PV = A+'cardano/provider.ts'
chk(at(HEAD, PV, 128, 'export function isChainReachableError(err: any): boolean {') and at(HEAD, PV, 129, "const status = typeof err?.status_code === 'number' ? err.status_code : null;") and at(HEAD, PV, 131, 'if (status === 402 || status === 408 || status === 429) return false;') and at(HEAD, PV, 132, 'if (status >= 500) return false;') and at(HEAD, PV, 133, 'return status >= 400 && status < 500;') and at(HEAD, PV, 134, '}'), 'provider.ts:128-134 isChainReachableError')
chk(cnt(HEAD, PV, 'return await blockfrost.txSubmit(txBytes);') == 1 and cnt(HEAD, PV, 'if (err?.status_code === 404) return null;') == 1, 'provider.ts submitTransaction = a bare blockfrost.txSubmit; getTransaction 404 -> null')
CF = A+'cardano/confirmation.ts'
chk(at(HEAD, CF, 9, "import { getTransaction } from './provider';") and at(HEAD, CF, 29, 'export async function waitForConfirmation(') and at(HEAD, CF, 55, '} catch (err: any) {') and at(HEAD, CF, 59, '}') and at(HEAD, CF, 62, "await sleep(delay + require('crypto').randomInt(0, 2000));") and at(HEAD, CF, 66, 'return {') and at(HEAD, CF, 67, 'confirmed: false,') and at(HEAD, CF, 69, '};') and at(HEAD, CF, 70, '}') and cnt(HEAD, CF, 'throw') == 0, 'confirmation.ts:9 import / :29 / :55-59 the swallowing catch / :62 jitter / :66-69 confirmed:false / 0 throws (E8 premise)')
RC = A+'reconciler.ts'
chk(at(HEAD, RC, 73, "WHERE status IN ('pending', 'submitted', 'submitting')") and at(HEAD, RC, 74, 'AND transaction_hash IS NOT NULL') and at(HEAD, RC, 98, '} else if (now() - new Date(row.created_at).getTime() > config.giveUpMs) {') and at(HEAD, RC, 100, "status: 'failed',"), 'reconciler.ts:73-74 the selection / :98-100 the time-based give-up')
CI = A+'cardano/index.ts'
chk(at(HEAD, CI, 234, 'if (demoMode && mockProvider) {') and at(HEAD, CI, 259, 'if (options.onSigned) await options.onSigned(txHash);') and at(HEAD, CI, 262, 'const submittedHash = await submitTransaction(txCborHex);') and at(HEAD, CI, 247, 'const { txCborHex, txHash, fee } = await buildAnchorTransaction(') and at(HEAD, CI, 252, ');'), 'cardano/index.ts:234 demo carve-out / :247-252 build+sign / :259 onSigned BEFORE / :262 submit')
OA = A+'anchoring.openapi.ts'
chk(at(HEAD, OA, 48, "// KS-726: 'submitting' is part of the published contract.") and at(HEAD, OA, 57, "status: z.enum(['pending', 'submitting', 'submitted', 'confirmed', 'failed'])," ) and cnt(HEAD, OA, "status: z.enum(['pending', 'submitting', 'submitted', 'confirmed', 'failed'])") == 1 and cnt(DEV, OA, "'submitting'") == 0, "anchoring.openapi.ts:48 docblock / :57 the enum (anchor count 1; develop 0)")
y = gittext(HEAD, D+'docs/openapi/secuura-api.yaml'); y0 = gittext(DEV, D+'docs/openapi/secuura-api.yaml'); Y = y.split('\n'); Y0 = y0.split('\n')
chk(len(Y) == 39733 and len(Y0) == 39732, 'yaml 39,732 lines at head / 39,731 at develop')
chk(Y[999] == '        status:' and Y[1001] == '          enum:' and Y[1003] == '            - submitting' and Y[1002] == '            - pending' and Y[1006] == '            - failed', 'yaml :1000-1007 the enum (:1004 - submitting)')
chk(sum(1 for l in Y if 'submitting' in l.lower()) == 1 and sum(1 for l in Y0 if 'submitting' in l.lower()) == 0 and sum(1 for l in Y if 'pending' in l.lower()) == 39, "yaml 'submitting' 1 at head / 0 at develop (control: 'pending' 39)")
# package.json + tsconfig + the SDK version in the farm
pj = blob(HEAD, D+'package.json')[2] or ''
chk('"check:openapi": "npm run generate-openapi -- --check && npm run check:spec-examples"' in pj and '"generate-openapi": "npm run build --workspace=packages/shared && tsx scripts/generate-openapi.ts"' in pj, 'root package.json check:openapi / generate-openapi scripts')
apj = blob(HEAD, A.replace('src/', '') + 'package.json')[2] or ''; ats = blob(HEAD, A.replace('src/', '') + 'tsconfig.json')[2] or ''
chk('"test": "vitest run"' in apj and '"vitest": "^4.1.9"' in apj and '"@blockfrost/blockfrost-js": "^6.1.0"' in apj and '"src/__tests__"' in ats and '"strict": true' in ats, 'anchoring package.json (vitest ^4.1.9, blockfrost-js ^6.1.0) / tsconfig excludes src/__tests__, strict')
GEN = D+'scripts/generate-openapi.ts'
chk(at(HEAD, GEN, 257, 'if (checkMode) {') and at(HEAD, GEN, 264, "console.error('[gen-openapi] CHECK FAIL: generated YAML differs from on-disk version');") and at(HEAD, GEN, 268, "console.log('[gen-openapi] CHECK PASS: on-disk YAML matches generated');") and at(HEAD, GEN, 269, 'process.exit(0);'), 'generate-openapi.ts:257-269 the --check semantics')
sdk = None
for base in ('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s231-ks726/Blockchain/Dev', R + '/Blockchain/Dev'):
    p = os.path.join(base, 'node_modules/@blockfrost/blockfrost-js/package.json')
    if os.path.exists(p):
        sdk = json.load(open(p))['version']; errs = open(os.path.join(base, 'node_modules/@blockfrost/blockfrost-js/lib/utils/errors.js')).read(); break
chk(sdk == '6.1.1' and 'this.status_code = error.status_code;' in errs and 'class BlockfrostClientError extends Error' in errs and errs.count('status_code') >= 4, f'the farm has @blockfrost/blockfrost-js {sdk}; BlockfrostServerError carries status_code, BlockfrostClientError does not (errors.js)')
# --- git-side: parents, merge-base, counts, numstats ---
chk(git('log', '-1', '--format=%P', HEAD).split() == [R1], 'head parent = 1885d5166 (one parent — not a merge)')
chk(git('merge-base', HEAD, M46).strip() == M44 and subprocess.run(['git', '-C', R, 'merge-base', '--is-ancestor', M44, HEAD]).returncode == 0, 'merge-base(head, M46) = M44; M44 is an ancestor of the head')
chk(subprocess.run(['git', '-C', R, 'merge-base', '--is-ancestor', M45, HEAD]).returncode == 1, 'M45 is NOT an ancestor of the head (the compare reads diverged)')
chk(subprocess.run(['git', '-C', R, 'merge-base', '--is-ancestor', P97, HEAD]).returncode == 0 and subprocess.run(['git', '-C', R, 'merge-base', '--is-ancestor', R1, HEAD]).returncode == 0, "97e2161fa (Peter's reviewed head) and 1885d5166 (round 1) are ancestors of the head (fast-forward pushes)")
chk(git('rev-list', '--count', f'{M44}..{HEAD}').strip() == '7' and git('rev-list', '--count', f'{M44}..{M46}').strip() == '2', 'rev-list --count M44..head = 7; M44..M46 = 2')
chk(git('rev-parse', HEAD + '^{tree}').strip() == '32e6396ab20f7f2b72cbe46dd40eae8f4de67491', 'head tree 32e6396ab')
ns = sorted((l.split('\t') for l in git('diff', '--numstat', M44, HEAD).strip().split('\n') if l.count('\t') == 2), key=lambda x: x[2])   # an empty numstat reads as [] (a FAIL, not a crash)
chk([x[:2] for x in ns] == [['1', '0'], ['153', '0'], ['462', '0'], ['237', '21'], ['10', '1'], ['76', '2'], ['127', '6'], ['7', '1'], ['47', '0']] and len(ns) == 9, 'numstat M44..head = the nine rows (+1120 -31)')
chk(git('diff', '--name-only', f'{M46}...{HEAD}').split() == git('diff', '--name-only', M44, HEAD).split() and len(git('diff', '--name-only', M44, HEAD).split()) == 9, 'three-dot M46 == two-dot M44 == exactly 9 files')
mv = git('diff', '--name-only', M44, M46).split()
chk(len(mv) == 3 and not any(f.startswith(A) or f.endswith('secuura-api.yaml') for f in mv), f'M44..M46 moved 3 files, none under services/anchoring/ or the yaml: {[f.split("/")[-1] for f in mv]}')
rns = sorted((l.split('\t') for l in git('diff', '--numstat', R1, HEAD).strip().split('\n') if l.count('\t') == 2), key=lambda x: x[2])
chk([x[:2] for x in rns] == [['117', '3'], ['94', '16'], ['8', '2']] and len(rns) == 3, 'the round-2 commit 1885d5166..head = test +117 -3 / anchorSubmission +94 -16 / index +8 -2')
# --- the deliverables: the MAIL paragraph (with a positive control), the guard phrases, the brief path, the SHA ---
PR = open(os.path.join(G, '2026-09-14_secuura-805-ks726-tier1-r1.prompt.txt'), encoding='utf-8').read(); BR = open(os.path.join(G, '2026-09-14_secuura-805-ks726-tier1-r1.md'), encoding='utf-8').read()
mail_para = 'MAIL YOUR VERDICT to wednesday-agent@agentmail.to when the pass is complete, using\nthe project\'s send_brief.sh.'
chk(PR.count(mail_para) == 1 and PR.count('the verdict MAIL is the wait signal') == 1 and PR.count('[QA -> Wednesday] TIER 1 GATE #805 (KS-726) cd5e62e96 — <VERDICT>') == 1 and PR.startswith('ultrathink\n'), 'prompt: the MAIL YOUR VERDICT paragraph verbatim (1), the subject (1), ultrathink first line (positive control)')
chk(PR.count('SEND YOUR VERDICT') == 0 and PR.count('/briefs/2026-09-14_secuura-805-ks726-tier1-r1.md') == 1, 'prompt: no rival verb (SEND YOUR VERDICT 0 — negative control); the INSTALLED brief path once')
for ph in ('NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout', 'no memory maintenance', 'NEVER print a credential value', 'TIER 1 ROUND 1', 'cd5e62e96c373c2690b97bafb277683402f1e70b'):
    chk(ph.lower() in PR.lower(), f'prompt carries {ph[:48]!r}')
chk('TIER 1' in BR and 'ROUND 1' in BR and 'cd5e62e96c373c2690b97bafb277683402f1e70b' in BR and BR.count('[QA -> Wednesday] TIER 1 GATE #805 (KS-726) cd5e62e96 — <VERDICT>') == 1 and 'predicted-by' in BR, 'brief carries TIER 1, ROUND 1, the head SHA, the subject once, predicted-by')
chk(len(re.findall(r'\| drafter \|$', BR, re.M)) + BR.count('predicted-by: drafter') >= 20 and 'Wednesday-read' not in BR, 'brief: >= 20 predictions carry drafter (table rows + predicted-by: drafter); no Wednesday-read row composed here')
# negative-token arm
if arg == '--neg-token':
    chk(cnt(HEAD, IX, 'isChainReachableError') == 1, 'NEG: index.ts isChainReachableError demanded 1 (known 0)')
    chk(cnt(HEAD, AS, '&& isChainReachableError(err)') == 0, 'NEG: the :463 discriminator demanded ABSENT at head (known 1)')
    chk(PR.count('SEND YOUR VERDICT to wednesday-agent@agentmail.to') == 1, 'NEG: the MAIL paragraph demanded under a rival verb (known 0)')
print(f'TALLY ok={ok} FAILS={fail} live_develop={live[:9]} {datetime.datetime.now().astimezone().strftime("%H:%M:%S")}')
sys.exit(1 if fail else 0)
PY
