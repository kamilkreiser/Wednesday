# KS-1797 (GET half): /api/oauth/authorize answers 500 for a repeated state or code_challenge query parameter. Spark operator 17. code_patch2: ONE product hunk (oauth.ts GET handler) + 1 NEW vitest file.
import subprocess
def _rd(p):
    return subprocess.run(['git','-C','/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/52e2783b-09e1-49d1-9200-c6e9ede3ba54/scratchpad/op16/src','show','e3d8456ec81d0b02172dd5a3060404815e797bde:'+p],check=True,capture_output=True).stdout.decode()
P='Blockchain/Dev/services/auth/src/routes/oauth.ts'
TP='Blockchain/Dev/services/auth/src/__tests__/ks1797-authorize-get-refuses-a-repeated-state-or-code-challenge.test.ts'
REF='Blockchain/Dev/services/auth/src/__tests__/ks1219-authorize-refuses-an-array-valued-scope.test.ts'
OLD="    } = req.query as Record<string, string>;\n\n    // KS-804: every app-derived rule lives in the resolver now"
NEW=("    } = req.query as Record<string, string>;\n"
"    // KS-1797: a repeated query parameter (?state=a&state=b) reaches this handler as an ARRAY whatever the cast above says. generateConsentPage then calls escapeHtml on it, an array has no\n"
"    // `replace`, and the catch below answered 500 server_error. A malformed request is a 400 invalid_request, the existing message the resolver's rules use, so no published message changes.\n"
"    if ((state !== undefined && typeof state !== 'string') || (code_challenge !== undefined && typeof code_challenge !== 'string')) {\n"
"      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'invalid_request', description: 'state and code_challenge must each be a single string' } });\n"
"    }\n"
"    // KS-804: every app-derived rule lives in the resolver now")
_t=_rd(REF).split('\n')
# header comment (own), then the ks1219 mocks and server setup verbatim (lines 4-75 of the reference)
HEAD=("// KS-1797 (GET half): GET /api/oauth/authorize answered 500 server_error when `state` or `code_challenge` arrived as a repeated query parameter (an array at run time): generateConsentPage calls\n"
"// escapeHtml on it and an array has no `replace`. A malformed request is a 400 invalid_request. Driven through the real router on a loopback listener with the same mocks as\n"
"// ks1219-authorize-refuses-an-array-valued-scope.test.ts; one string value is the control. The POST half of KS-1797 (a JSON array state or code_challenge) is NOT covered here.\n")
MID='\n'.join(_t[3:75])+'\n'
TAIL='''const CB = encodeURIComponent('https://app.example.com/cb');
const GET_BASE = `client_id=client-1&redirect_uri=${CB}&response_type=code`;

async function get(extraQuery: string): Promise<{ status: number; message: string | undefined }> {
  const res = await fetch(`${base}/api/oauth/authorize?${GET_BASE}${extraQuery}`, { redirect: 'manual' });
  const text = await res.text();
  let message: string | undefined;
  try { message = JSON.parse(text)?.error?.message; } catch { /* html consent page */ }
  return { status: res.status, message };
}

describe('KS-1797: GET /api/oauth/authorize refuses a repeated state or code_challenge', () => {
  it('RED KS-1797 R1 GET with a repeated state parameter is 400 invalid_request, not 500', async () => {
    expect(await get('&state=xyz&state=second')).toEqual({ status: 400, message: 'invalid_request' });
    expect(createAuthorizationCode).not.toHaveBeenCalled();
  });

  it('RED KS-1797 R2 GET with a repeated code_challenge parameter is 400 invalid_request, not 500', async () => {
    expect(await get('&state=xyz&code_challenge=aaa&code_challenge=bbb')).toEqual({ status: 400, message: 'invalid_request' });
    expect(createAuthorizationCode).not.toHaveBeenCalled();
  });

  it('CONTROL KS-1797 C1 GET with one state still serves the consent page', async () => {
    expect((await get('&state=xyz')).status).toBe(200);
  });

  it('CONTROL KS-1797 C2 GET with no state still serves the consent page', async () => {
    expect((await get('')).status).toBe(200);
  });

  it('CONTROL KS-1797 C3 GET with one code_challenge still serves the consent page', async () => {
    expect((await get('&state=xyz&code_challenge=aaa')).status).toBe(200);
  });

  it('CONTROL KS-1797 C4 GET with a repeated scope is still 400 invalid_request (KS-1219)', async () => {
    expect(await get('&state=xyz&scope=openid&scope=profile')).toEqual({ status: 400, message: 'invalid_request' });
  });
});
'''
TEST=HEAD+MID+'\n'+TAIL
S=dict(dir='ks_1797_p1_authorize_get_state_challenge',ticket='KS-1797',
 title='auth routes/oauth.ts GET /authorize: a repeated state or code_challenge query parameter answers 500 server_error instead of 400 invalid_request (KS-1797, GET half only): refuse a non-string state or code_challenge in the handler (RUNG 3, code_patch2: one product hunk of one inserted block + one NEW vitest file)',
 intro="DRAFT by Spark operator 17 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / auth) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. **oauth.ts is an AUTH surface (the OAuth authorize endpoint): routing row 4 applies and the raise PR needs a TIER-1 gate.** The change only REFUSES more (a malformed request that used to 500 becomes a 400 with an existing message). Origin: KS-1797 (gate 9 note 1797-2 on PR 1797, measured by the filing seat). ONLY the GET half is in this brief; the POST half (a JSON array state or code_challenge is coerced, not refused) and the scope dedupe/cap are decisions the ticket leaves open and are NOT touched. Link the PR as Refs KS-1797, never a close-word.",
 products=[(P,[(OLD,NEW)])],
 prodnote=['product, modified in place: ONE inserted block of 5 lines (a 2-line comment and a 3-line guard) that also takes the blank line that stood between the destructure and the KS-804 comment in the GET /authorize handler'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 6 cells (2 red, 4 control); the mocks and server setup are copied from ks1219-authorize-refuses-an-array-valued-scope.test.ts'],
 runner='vitest` (`npx vitest run src/__tests__/ks1797-authorize-get-refuses-a-repeated-state-or-code-challenge.test.ts` from `Blockchain/Dev/services/auth',
 tier='code_patch2', rung='3 (two files: a product file with one inserted block, a new test given whole)',
 pins='''# code_patch2: auth routes/oauth.ts (1 hunk) + a NEW vitest file; ref = the ks1219 oauth authorize test (shape only); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/auth/src/__tests__/ks1219-authorize-refuses-an-array-valued-scope.test.ts
line=493
ctx=65536
''',
 wrong="`GET /api/oauth/authorize` (the handler at `services/auth/src/routes/oauth.ts:487`) reads its query as `req.query as Record<string, string>` (`:492`). The cast does nothing at run time, so `?state=a&state=b` or `?code_challenge=a&code_challenge=b` reaches the handler as an ARRAY. `generateConsentPage` then calls `escapeHtml(params.state)` and `escapeHtml(params.codeChallenge || '')` (`:1522`, `:1523`) and `escapeHtml(s)` is `s.replace(...)` (`:1582`), which an array does not have: the call throws and the handler's catch answers 500 `server_error`. KS-1219 closed the same class for `scope` (`:396`); a repeated `code_challenge_method` is already a 400 by accident. A malformed request is a 400 `invalid_request`, the message the file already uses.",
 where="- `services/auth/src/routes/oauth.ts:492` - (correct, STAYS) `    } = req.query as Record<string, string>;` the last line of the destructure; the new block goes right after it, before the `// KS-804: every app-derived rule lives in the resolver now` comment (`:494`), The one blank line that stood there is consumed (the diff removes it, so no hunk has a blank context line).\n- `:396` - (correct, STAYS) the KS-1219 `scope` refusal in the resolver, the pattern the new guard follows (same `invalid_request` message).\n- `:518` - (correct, STAYS) `state: state || '',` is where `state` is consumed.",
 exactnote="ONE product hunk: an inserted block after the destructure. The refusal body has the same shape as the file's other 400s (`success:false`, `error.code BAD_REQUEST`, `error.message invalid_request`, a description).\n",
 donot="**Do NOT touch** the resolver, `generateConsentPage`, `escapeHtml`, the POST handler, or any other line of `oauth.ts`; no other file.",
 testnote2="The test section is a NEW file given whole. The `+` lines are byte-exact. It imports from `vitest`, drives the real router on a loopback listener, and has no top-level await.",
 red=['RED KS-1797 R1','RED KS-1797 R2'],
 cells="- RED `R1` and `R2` at the tip: the handler answers 500 `server_error` for the repeated parameter (an array has no `replace`).\n- GREEN at the tip and after: `C1` to `C4` (one state, no state, one code_challenge, and the KS-1219 repeated-scope 400).\n- After the edit all six are green.",
 premises="- `oauth.ts:487-492` (handler and destructure), `:518` (`state: state || ''`), `:1522-1523` and `:1582-1584` (escapeHtml) are as quoted, read at the tip by script; the golden is generated from the tree at the tip, not typed.\n- The ticket's measurement: single `state=xyz` answers 200, `&state=xyz&state=second` answers 500; `&code_challenge=aaa&code_challenge=bbb` answers 500; a single `code_challenge=aaa` answers 200 (all on a confidential app, repository mocked, as in the new test).\n- auth's runner is vitest (`ks1219-authorize-refuses-an-array-valued-scope.test.ts` is the same shape).",
 unmeasured="- The drafter did NOT run the new file; the RED-at-tip / GREEN-after result is the `round.sh --control` run on this golden.\n- The POST half (JSON array `state` coerced to a comma-joined string, JSON array `code_challenge` reaching `createAuthorizationCode`) is not changed and not tested: the ticket records it as a decision (refuse or coerce).\n- Order: the new guard answers before the client/redirect checks, so a request with both a repeated state and an unknown client_id now reads 400 invalid_request from this guard rather than the resolver's own refusal; not measured.\n- Scope dedupe/cap, and the other authorize parameters as arrays (`client_id`, `redirect_uri`, `response_type`), are untouched.",
 scope="**KS-1797, GET half (repeated `state` and `code_challenge`) only.** Link the PR as Refs KS-1797, never a close-word. Tier-1 gate on the PR because oauth.ts is an auth surface.",
)
