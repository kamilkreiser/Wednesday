PD='Blockchain/Dev/services/auth/src/providers/social/'
PG,PGO,PL=PD+'github.ts',PD+'google.ts',PD+'linkedin.ts'
TP='Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded.test.ts'
IMP="import { SocialProvider, SocialProviderConfig, SocialProfile } from './types';\n"
CONST=IMP+"""
// KS-1240 (class): every hand-built outbound fetch carries a timeout signal. Without one an identity provider that accepts the connection and never answers holds the callback request open for as
// long as the socket lives. On expiry the fetch rejects, exchangeCode rejects, and the callback's existing catch answers as it already does for any other provider failure.
const SOCIAL_PROVIDER_FETCH_TIMEOUT_MS = 10_000;
"""
SIG="signal: AbortSignal.timeout(SOCIAL_PROVIDER_FETCH_TIMEOUT_MS),"
G_edits=[(IMP,CONST),
("        redirect_uri: this.config.callbackUrl,\n      }),\n    });\n\n    if (!tokenRes.ok) {",
 "        redirect_uri: this.config.callbackUrl,\n      }),\n      "+SIG+"\n    });\n\n    if (!tokenRes.ok) {"),
("      headers: { Authorization: `Bearer ${access_token}`, Accept: 'application/json' },\n    });\n\n    if (!profileRes.ok) {",
 "      headers: { Authorization: `Bearer ${access_token}`, Accept: 'application/json' },\n      "+SIG+"\n    });\n\n    if (!profileRes.ok) {"),
("        headers: { Authorization: `Bearer ${access_token}`, Accept: 'application/json' },\n      });\n      if (emailsRes.ok) {",
 "        headers: { Authorization: `Bearer ${access_token}`, Accept: 'application/json' },\n        "+SIG+"\n      });\n      if (emailsRes.ok) {")]
GO_edits=[(IMP,CONST),
("        grant_type: 'authorization_code',\n      }),\n    });",
 "        grant_type: 'authorization_code',\n      }),\n      "+SIG+"\n    });"),
("      headers: { Authorization: `Bearer ${tokens.access_token}` },\n    });",
 "      headers: { Authorization: `Bearer ${tokens.access_token}` },\n      "+SIG+"\n    });")]
LI_edits=[(IMP,CONST),
("        redirect_uri: this.config.callbackUrl,\n      }),\n    });\n\n    if (!tokenRes.ok) {",
 "        redirect_uri: this.config.callbackUrl,\n      }),\n      "+SIG+"\n    });\n\n    if (!tokenRes.ok) {"),
("      headers: { Authorization: `Bearer ${access_token}` },\n    });",
 "      headers: { Authorization: `Bearer ${access_token}` },\n      "+SIG+"\n    });")]
TEST='''// KS-1240 (class: hand-built outbound fetches with no timeout), services/auth social adapters github.ts, google.ts and linkedin.ts: their seven fetches (github token, user, user/emails; google token,
// userinfo; linkedin token, userinfo) passed no `signal`, so an identity provider that accepts the connection and never answers held the OAuth callback open for as long as the socket lived. The adapters are
// driven directly with a stubbed global fetch that honours `init.signal` (and never answers when there is none); nothing touches the network. R1 to R3 pin that every fetch carries an AbortSignal, R4 that
// each bound is a sane positive number, R5 to R7 that a provider that never answers ends in a rejection, not a hang. C1 and C2 pin that the full exchange and the refusal message are unchanged.
import { describe, it, expect, afterEach, vi } from 'vitest';
import { GitHubProvider } from '../providers/social/github';
import { GoogleProvider } from '../providers/social/google';
import { LinkedInProvider } from '../providers/social/linkedin';

const CONFIG = { clientId: 'cid-ks1240', clientSecret: 'secret-ks1240', callbackUrl: 'https://app.test/cb', enabled: true };

function reply(status: number, body: unknown): Response {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
    text: async () => (typeof body === 'string' ? body : JSON.stringify(body)),
  } as unknown as Response;
}

type Seen = { url: string; signal: unknown };

/** Answers by URL and records the signal each call carried. `emailless` makes github's user profile carry no email, so the emails fetch happens too. */
function stubAnswering(seen: Seen[], emailless = false): void {
  vi.spyOn(globalThis, 'fetch').mockImplementation((async (url: unknown, init?: { signal?: unknown }) => {
    const u = String(url);
    seen.push({ url: u, signal: init?.signal });
    if (u.includes('github.com/login/oauth/access_token')) return reply(200, { access_token: 'tok' });
    if (u.endsWith('api.github.com/user')) return reply(200, emailless ? { id: 7, login: 'octo', name: 'Octo Cat' } : { id: 7, login: 'octo', email: 'o@x.test', name: 'Octo Cat' });
    if (u.endsWith('api.github.com/user/emails')) return reply(200, [{ email: 'o@x.test', primary: true, verified: true }]);
    if (u.includes('googleapis.com/token')) return reply(200, { access_token: 'tok' });
    if (u.includes('googleapis.com/oauth2/v2/userinfo')) return reply(200, { id: 'g1', email: 'g@x.test', verified_email: true });
    if (u.includes('linkedin.com/oauth/v2/accessToken')) return reply(200, { access_token: 'tok' });
    if (u.includes('api.linkedin.com/v2/userinfo')) return reply(200, { sub: 'l1', email: 'l@x.test', email_verified: true });
    return reply(404, 'unexpected url ' + u);
  }) as never);
}

/** Every call honours its signal; a call with NO signal never answers (the hang the fix removes). */
function stubNeverAnswering(): void {
  vi.spyOn(globalThis, 'fetch').mockImplementation(((_url: unknown, init?: { signal?: AbortSignal }) =>
    new Promise<Response>((_resolve, reject) => {
      const signal = init?.signal;
      if (!signal) return;
      if (signal.aborted) reject(new Error('aborted'));
      else signal.addEventListener('abort', () => reject(new Error('aborted')));
    })) as never);
}

afterEach(() => { vi.restoreAllMocks(); });

/** 'REJECTED' when exchangeCode rejects, 'RESOLVED' when it resolves, 'HUNG' when it is still pending after 300 ms, so a hang is a red assertion and not a stuck run. */
async function outcome(run: () => Promise<unknown>): Promise<string> {
  return Promise.race([
    run().then(() => 'RESOLVED', () => 'REJECTED'),
    new Promise<string>((resolve) => setTimeout(() => resolve('HUNG'), 300)),
  ]);
}

describe('KS-1240: the social adapters bound their outbound fetches', () => {
  it('RED KS-1240 R1 every github fetch (token, user, emails) carries an AbortSignal', async () => {
    const seen: Seen[] = [];
    stubAnswering(seen, true);
    await new GitHubProvider(CONFIG).exchangeCode('code');
    expect(seen).toHaveLength(3);
    for (const call of seen) expect(call.signal).toBeInstanceOf(AbortSignal);
  });

  it('RED KS-1240 R2 every google fetch (token, userinfo) carries an AbortSignal', async () => {
    const seen: Seen[] = [];
    stubAnswering(seen);
    await new GoogleProvider(CONFIG).exchangeCode('code');
    expect(seen).toHaveLength(2);
    for (const call of seen) expect(call.signal).toBeInstanceOf(AbortSignal);
  });

  it('RED KS-1240 R3 every linkedin fetch (token, userinfo) carries an AbortSignal', async () => {
    const seen: Seen[] = [];
    stubAnswering(seen);
    await new LinkedInProvider(CONFIG).exchangeCode('code');
    expect(seen).toHaveLength(2);
    for (const call of seen) expect(call.signal).toBeInstanceOf(AbortSignal);
  });

  it('RED KS-1240 R4 the seven bounds handed to AbortSignal.timeout are positive and at most 30000 ms', async () => {
    const timeout = vi.spyOn(AbortSignal, 'timeout');
    stubAnswering([], true);
    await new GitHubProvider(CONFIG).exchangeCode('code');
    await new GoogleProvider(CONFIG).exchangeCode('code');
    await new LinkedInProvider(CONFIG).exchangeCode('code');
    const bounds = timeout.mock.calls.map((c) => c[0] as number);
    expect(bounds).toHaveLength(7);
    for (const ms of bounds) {
      expect(ms).toBeGreaterThan(0);
      expect(ms).toBeLessThanOrEqual(30000);
    }
  });

  it('RED KS-1240 R5 a github token endpoint that never answers ends in a rejection, not a hang', async () => {
    vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => AbortSignal.abort());
    stubNeverAnswering();
    expect(await outcome(() => new GitHubProvider(CONFIG).exchangeCode('code'))).toBe('REJECTED');
  });

  it('RED KS-1240 R6 a google token endpoint that never answers ends in a rejection, not a hang', async () => {
    vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => AbortSignal.abort());
    stubNeverAnswering();
    expect(await outcome(() => new GoogleProvider(CONFIG).exchangeCode('code'))).toBe('REJECTED');
  });

  it('RED KS-1240 R7 a linkedin token endpoint that never answers ends in a rejection, not a hang', async () => {
    vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => AbortSignal.abort());
    stubNeverAnswering();
    expect(await outcome(() => new LinkedInProvider(CONFIG).exchangeCode('code'))).toBe('REJECTED');
  });

  it('control KS-1240 C1 the full exchange of each adapter still resolves to the same provider id', async () => {
    stubAnswering([], true);
    expect((await new GitHubProvider(CONFIG).exchangeCode('code')).providerId).toBe('7');
    expect((await new GoogleProvider(CONFIG).exchangeCode('code')).providerId).toBe('g1');
    expect((await new LinkedInProvider(CONFIG).exchangeCode('code')).providerId).toBe('l1');
  });

  it('control KS-1240 C2 a refused github token exchange still throws its own message', async () => {
    vi.spyOn(globalThis, 'fetch').mockImplementation((async () => reply(401, 'bad_verification_code')) as never);
    await expect(new GitHubProvider(CONFIG).exchangeCode('code')).rejects.toThrow('GitHub token exchange failed: bad_verification_code');
  });
});
'''
S=dict(dir='ks_1240_p4_social',ticket='KS-1240',
 title='(class, slice 4) auth social adapters github.ts, google.ts, linkedin.ts: seven outbound fetches carry no timeout; add AbortSignal.timeout (RUNG 3, code_patch2: 3 products, 7 sites + 3 constants, one NEW behavioural vitest file)',
 intro="DRAFT by a Spark brief drafter for Wednesday, batch 4 of 2026-10-28 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. KS-1240 is the gateway ticket (hand-built fetch without a timeout); this slice applies the same class to the identity-provider adapters in services/auth (the drafter's extension, stated: the ticket does not name these files; the raise seat confirms the scope with the owner or files the class ticket). On expiry the fetch rejects, `exchangeCode` rejects like it does for any provider failure, and the callback's existing catch answers; nothing new is built. Three of the six adapters only (the tier takes at most three products). The Spark may fail this one (capability data): it is the widest brief so far by sites (7 sites, 3 files) and has behavioural cells that stub fetch and AbortSignal.",
 products=[(PG,G_edits),(PGO,GO_edits),(PL,LI_edits)],
 prodnote=['product 1, modified in place: FOUR hunks - the constant after the import, then one `signal:` line in each of the 3 fetches','product 2, modified in place: THREE hunks - the constant, then one `signal:` line in each of the 2 fetches','product 3, modified in place: THREE hunks - the constant, then one `signal:` line in each of the 2 fetches'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 9 cells (7 red, 2 control; stubbed fetch, no network)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1240-social-provider-fetches-are-bounded.test.ts` from `Blockchain/Dev/services/auth',
 tier='code_patch2', rung='3 (ten hunks in three products given byte-exact; the new test given whole)',
 pins='''# code_patch2: 3 products in services/auth providers/social (github.ts 4 hunks; google.ts 3; linkedin.ts 3) + 1 NEW vitest file; ref = ks1617 (fetch-stub adapter spec, shape only); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/auth/src/__tests__/ks1617-social-profile-fetch-failure-names-the-http-status.test.ts
line=2
ctx=65536
''',
 wrong="The GitHub, Google and LinkedIn adapters (`services/auth/src/providers/social/github.ts`, `google.ts`, `linkedin.ts`) call `fetch` seven times in all (github: token exchange, `/user`, `/user/emails`; google: token exchange, userinfo; linkedin: token exchange, userinfo) with no `signal`. An identity provider that accepts the connection and never answers holds the OAuth callback request open for as long as the socket lives. In each adapter `exchangeCode` already lets a rejected fetch propagate, so a timeout needs no new handling. The change adds, per file, one module constant `SOCIAL_PROVIDER_FETCH_TIMEOUT_MS = 10_000` (with a comment) after the `./types` import, and `signal: AbortSignal.timeout(SOCIAL_PROVIDER_FETCH_TIMEOUT_MS),` as the LAST property of each fetch's init object. For a healthy provider nothing changes.",
 where="- each file: **must change** (insertion) - after line 1 (`import { SocialProvider, ... } from './types';`) a blank line, three comment lines and the constant line.\n- `github.ts` (tip numbers): the init objects of the fetches at :23 (after the `body: JSON.stringify({...}),`), :43 (after `headers: {...},`) and :57 (after `headers: {...},`).\n- `google.ts`: the init objects at :26 (after `body: new URLSearchParams({...}),`) and :45 (after `headers: {...},`).\n- `linkedin.ts`: the init objects at :24 and :42, same placement.\n- Every other line of the three files and the other three adapters (apple, facebook, microsoft-personal) are NOT touched.",
 exactnote="TEN hunks in three files: github four, google three, linkedin three. Each `signal:` line is an insertion; each file's first hunk is the constant block.\n",
 donot="**Do NOT touch** any other line of the three adapters, the apple / facebook / microsoft-personal adapters, `types.ts`, or any other file.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. Pure ASCII, vitest imports, no top-level await. It drives the three adapters directly with a stubbed global `fetch` (answering by URL, or honouring `init.signal`), spies on `AbortSignal.timeout`, and never touches the network.",
 red=['RED KS-1240 R1','RED KS-1240 R2','RED KS-1240 R3','RED KS-1240 R4','RED KS-1240 R5','RED KS-1240 R6','RED KS-1240 R7'],
 cells="- RED `R1` to `R3`: at the tip no fetch carries `init.signal`, so `toBeInstanceOf(AbortSignal)` fails for the first call; after the edit every call carries one.\n- RED `R4`: at the tip `AbortSignal.timeout` is never called (0 bounds, not 7); after the edit 7 bounds, each positive and at most 30000.\n- RED `R5` to `R7`: `AbortSignal.timeout` is made to return an already-aborted signal and the fetch stub honours it; at the tip no signal is passed, the stub never answers and the cell reads `HUNG` after 300 ms; after the edit the fetch rejects and the cell reads `REJECTED`.\n- CONTROL `C1`, `C2`: green at the tip AND after (each adapter's full exchange resolves to the same provider id; a 401 token reply still throws the same message).",
 premises="- Each adapter's `exchangeCode` awaits its fetches with no try/catch of its own (github.ts :22-:70, google.ts :25-:58, linkedin.ts :23-:51), so a rejection propagates to the caller (read from the cache clone at the tip).\n- The first line of each of the three files is the `./types` import quoted above (byte-identical in all three; the generator edits each file separately).\n- ks1617 already stubs `globalThis.fetch` with `vi.spyOn` against these adapters, so adding a `signal` to the init does not change what those stubs see beyond an extra property.\n- `AbortSignal.timeout` and `AbortSignal.abort` exist on the Node the suite runs on (ks1240 slices 1-3 use the former).",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- Whether 10000 ms is the right bound for a social login: the value is the drafter's; the raise seat confirms with the owner. A signal also bounds reading the response body.\n- How the OAuth callback presents a rejected exchangeCode (the existing catch is relied on, not read or pinned here).\n- The apple, facebook and microsoft-personal adapters have the same shape and are left for a later slice (three-product limit).\n- Open PRs touching these files: none by the file lists of every open PR read on 2026-10-28.",
 scope="**Slice 4 of the KS-1240 class, services/auth social adapters (three of six).** Link the PR as Refs KS-1240, never a close-word; the raise seat decides with the owner whether KS-1240 covers auth or a class ticket is filed.",
)
