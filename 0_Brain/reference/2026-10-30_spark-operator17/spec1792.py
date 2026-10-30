# KS-1792: GitHub sign-in: a 200 token answer with no access_token is not refused (the adapter calls /user with 'Bearer undefined'). Spark operator 17. code_patch2: ONE product hunk (github.ts) + 1 NEW vitest file.
P='Blockchain/Dev/services/auth/src/providers/social/github.ts'
TP='Blockchain/Dev/services/auth/src/__tests__/ks1792-github-refuses-a-token-answer-without-an-access-token.test.ts'
OLD="    const { access_token } = (await tokenRes.json()) as { access_token: string };\n\n"
NEW=("    // KS-1792: GitHub answers a bad or expired code with HTTP 200 and an {error, error_description} body, so the !ok branch above never sees it. Refuse an answer that has no usable\n"
"    // access_token (or that carries an error field) here, as a token-exchange failure, before any profile call: the guard must not be GitHub's 401 for `Bearer undefined`.\n"
"    const tokenBody = (await tokenRes.json()) as { access_token?: unknown; error?: unknown };\n"
"    if (typeof tokenBody.access_token !== 'string' || tokenBody.access_token === '' || tokenBody.error !== undefined) {\n"
"      logger.warn('GitHub token endpoint answered 200 without an access token', { provider: 'github', error: typeof tokenBody.error === 'string' ? tokenBody.error.slice(0, 80) : undefined });\n"
"      throw new Error('GitHub token exchange failed (no access token)');\n"
"    }\n"
"    const access_token = tokenBody.access_token;\n")
TEST='''// KS-1792: GitHub answers a bad or expired sign-in code with HTTP 200 and an {error, error_description} body. The adapter used to read access_token from it unchecked and call /user with
// `Bearer undefined`, relying on GitHub answering that 401. GitHubProvider.exchangeCode now refuses such an answer before any profile call. fetch is replaced by a recording stub, so no
// socket is opened; a good token answer is the control.
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';

const { silentLogger } = vi.hoisted(() => ({
  silentLogger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() },
}));
vi.mock('../utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger, validateEnv: vi.fn() }));
vi.mock('@secuura/shared/utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger }));

import { GitHubProvider } from '../providers/social/github';

const CONFIG = { clientId: 'cid-ks1792', clientSecret: 'secret-ks1792', callbackUrl: 'https://app.test/cb', enabled: true };

let calls: string[];

type Answer = { status: number; body: unknown };

// A recording stub keyed by URL: the token endpoint answers `token`, api.github.com/user answers `user` (default: GitHub's own 401 for a bad bearer), anything else 404.
function stubFetch(token: Answer, user: Answer = { status: 401, body: { message: 'Bad credentials' } }) {
  calls = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    calls.push(String(url));
    const a = String(url).includes('/login/oauth/access_token') ? token : String(url).endsWith('/user') ? user : { status: 404, body: {} };
    return new Response(JSON.stringify(a.body), { status: a.status, headers: { 'content-type': 'application/json' } });
  }));
}

// The message exchangeCode rejects with, or 'RESOLVED' if it did not reject: a plain value, so a wrong answer fails by assertion.
async function refusal(code: string): Promise<string> {
  return new GitHubProvider(CONFIG).exchangeCode(code).then(() => 'RESOLVED', (e: Error) => e.message);
}

beforeEach(() => { vi.clearAllMocks(); });
afterEach(() => { vi.unstubAllGlobals(); });

describe('KS-1792: the GitHub adapter refuses a 200 token answer that has no access_token', () => {
  it('RED KS-1792 R1 a 200 error answer (bad_verification_code) is refused and /user is never called', async () => {
    stubFetch({ status: 200, body: { error: 'bad_verification_code', error_description: 'The code passed is incorrect or expired.' } });
    expect(await refusal('bad')).toBe('GitHub token exchange failed (no access token)');
    expect(calls).toEqual(['https://github.com/login/oauth/access_token']);
  });

  it('RED KS-1792 R2 a 200 answer with an empty body object is refused and /user is never called', async () => {
    stubFetch({ status: 200, body: {} });
    expect(await refusal('bad')).toBe('GitHub token exchange failed (no access token)');
    expect(calls).toEqual(['https://github.com/login/oauth/access_token']);
  });

  it('RED KS-1792 R3 a 200 answer whose access_token is not a string is refused and /user is never called', async () => {
    stubFetch({ status: 200, body: { access_token: 42 } });
    expect(await refusal('bad')).toBe('GitHub token exchange failed (no access token)');
    expect(calls).toEqual(['https://github.com/login/oauth/access_token']);
  });

  it('CONTROL KS-1792 C1 a good token answer still signs in: the profile call carries the Bearer token', async () => {
    stubFetch(
      { status: 200, body: { access_token: 'tok-ks1792' } },
      { status: 200, body: { id: 7, email: 'a@secuura.test', name: 'Ada Lovelace', login: 'ada' } },
    );
    const profile = await new GitHubProvider(CONFIG).exchangeCode('good');
    expect(profile.providerId).toBe('7');
    expect(profile.email).toBe('a@secuura.test');
    expect(calls).toEqual(['https://github.com/login/oauth/access_token', 'https://api.github.com/user']);
    const profileInit = (vi.mocked(fetch).mock.calls[1] as unknown as [string, { headers: Record<string, string> }])[1];
    expect(profileInit.headers.Authorization).toBe('Bearer tok-ks1792');
  });

  it('CONTROL KS-1792 C2 a non-2xx token answer is still the status-only failure', async () => {
    stubFetch({ status: 400, body: { error: 'bad_verification_code' } });
    expect(await refusal('bad')).toBe('GitHub token exchange failed (HTTP 400)');
  });
});
'''
S=dict(dir='ks_1792_p1_github_no_access_token',ticket='KS-1792',
 title="auth providers/social/github.ts: a 200 token answer with no access_token (GitHub's bad-code answer) is not refused; the adapter calls /user with 'Bearer undefined' (KS-1792): refuse it as a token-exchange failure before any profile call (RUNG 3, code_patch2: one product hunk replacing one line + one NEW vitest file)",
 intro="DRAFT by Spark operator 17 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / auth) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. **github.ts is an AUTH surface (social sign-in token exchange): routing row 4 applies and the raise PR needs a TIER-1 gate.** The change only REFUSES more (defence in depth: against real GitHub the profile call already fails 401 and no sign-in happens). Origin: KS-1792 (tier-1 gate 7 probe P4 / finding 1788-13 on PR 1788, which is merged). Link the PR as Refs KS-1792, never a close-word.",
 products=[(P,[(OLD,NEW)])],
 prodnote=['product, modified in place: ONE line and the blank line after it replaced by 8 lines in `exchange` (2 comment lines, the typed read, a 4-line refusal, the `access_token` constant)'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 5 cells (3 red, 2 control); fetch is a recording stub'],
 runner='vitest` (`npx vitest run src/__tests__/ks1792-github-refuses-a-token-answer-without-an-access-token.test.ts` from `Blockchain/Dev/services/auth',
 tier='code_patch2', rung='3 (two files: a product file with one hunk, a new test given whole)',
 pins='''# code_patch2: auth providers/social/github.ts (1 hunk) + a NEW vitest file; ref = ks1240b social-provider test (shape only); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/auth/src/__tests__/ks1240b-social-provider-fetches-are-bounded-and-classified.test.ts
line=86
ctx=65536
''',
 wrong="`GitHubProvider.exchange` (`services/auth/src/providers/social/github.ts:63`) POSTs to GitHub's token endpoint and handles only a non-2xx answer (`:79-84`). GitHub answers a bad or expired code with HTTP 200 and an `{error, error_description}` body, so the next line (`:86`), `const { access_token } = (await tokenRes.json()) as { access_token: string };`, reads `undefined` and `:88-91` calls `https://api.github.com/user` with `Authorization: Bearer undefined`. The only thing that stops the sign-in is GitHub answering that 401 (the adapter then throws 'Failed to fetch GitHub user profile'). Refuse a token answer with no usable `access_token` (or one carrying an `error` field) as a token-exchange failure, before any profile call.",
 where="- `services/auth/src/providers/social/github.ts:86` - **must change**: the one line `    const { access_token } = (await tokenRes.json()) as { access_token: string };` is replaced by the block in the diff below (comment, typed read, refusal, `const access_token = tokenBody.access_token;`).\n- `:79-84` (the `!tokenRes.ok` branch and its `logger.warn`), `:88` onward (the profile and emails calls, which keep using the name `access_token`) - (correct, STAY).",
 exactnote="ONE product hunk. The later lines use the name `access_token`, so the replacement ends by declaring a constant with that name. The thrown message is `GitHub token exchange failed (no access token)`, the shape of the `!ok` branch's `GitHub token exchange failed (HTTP <status>)`.\n",
 donot="**Do NOT touch** the `!tokenRes.ok` branch, the profile and emails calls, any other provider adapter, `routes/auth.ts`, or any other line of `github.ts`; no other file.",
 testnote2="The test section is a NEW file given whole. The `+` lines are byte-exact. It imports from `vitest`, mocks the logger, replaces `fetch` with a recording stub (no socket), and has no top-level await.",
 red=['RED KS-1792 R1','RED KS-1792 R2','RED KS-1792 R3'],
 cells="- RED `R1`, `R2`, `R3` at the tip: the adapter goes on to call `https://api.github.com/user` (the stub answers it 401), so the rejection message is 'Failed to fetch GitHub user profile' (the stub answers /user 401, as GitHub does) instead of the new text, and `calls` has two entries.\n- GREEN at the tip and after: `C1` (a good token answer signs in; the profile call carries `Bearer tok-ks1792`) and `C2` (a 400 token answer is still the status-only failure).\n- After the edit all five are green.",
 premises="- `github.ts:79-84` (the `!ok` branch), `:86` (the unchecked read), `:88-91` (the profile call with `Bearer ${access_token}`) are as quoted, read at the tip by script; the golden is generated from the tree at the tip, not typed.\n- The test imports `GitHubProvider` the way `ks1240b-social-provider-fetches-are-bounded-and-classified.test.ts` does (its CONFIG shape and logger mocks), and `exchangeCode` is the public method.\n- No other file in the tip reads GitHub's token answer without `access_token`: the `ks1240b` file stubs real answers (not re-read in full by the drafter).",
 unmeasured="- The drafter did NOT run the new file; the RED-at-tip / GREEN-after result is the `round.sh --control` run on this golden.\n- Whether existing cells (for example in `ks1240b`) answer the token call with a body that has no `access_token` and would now fail: the control run's suite counts are the check; not read by the drafter.\n- How the login callback renders the new message (`OAuth authentication failed: GitHub token exchange failed (no access token)`) is not tested here.\n- The other five social adapters may share the shape; they are not touched.",
 scope="**KS-1792 only (the GitHub adapter).** Link the PR as Refs KS-1792, never a close-word. Tier-1 gate on the PR because github.ts is an auth surface.",
)
