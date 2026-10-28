PD='Blockchain/Dev/services/auth/src/providers/social/'
PG,PGO,PL=PD+'apple.ts',PD+'facebook.ts',PD+'microsoft-personal.ts'
TP='Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded-apple-facebook-microsoft.test.ts'
IMP="import { SocialProvider, SocialProviderConfig, SocialProfile } from './types';\n"
CONST=IMP+"""
// KS-1240 (class): every hand-built outbound fetch carries a timeout signal. Without one an identity provider that accepts the connection and never answers holds the callback request open for as
// long as the socket lives. On expiry the fetch rejects, exchangeCode rejects, and the callback's existing catch answers as it already does for any other provider failure.
const SOCIAL_PROVIDER_FETCH_TIMEOUT_MS = 10_000;
"""
SIG="signal: AbortSignal.timeout(SOCIAL_PROVIDER_FETCH_TIMEOUT_MS),"
G_edits=[(IMP,CONST),
("        grant_type: 'authorization_code',\n        redirect_uri: this.config.callbackUrl,\n      }),\n    });",
 "        grant_type: 'authorization_code',\n        redirect_uri: this.config.callbackUrl,\n      }),\n      "+SIG+"\n    });")]
GO_edits=[(IMP,CONST),
("        code,\n      })}`,\n    );\n\n    if (!tokenRes.ok) {",
 "        code,\n      })}`,\n      { "+SIG+" },\n    );\n\n    if (!tokenRes.ok) {"),
("picture&access_token=${access_token}`,\n    );",
 "picture&access_token=${access_token}`,\n      { "+SIG+" },\n    );")]
LI_edits=[(IMP,CONST),
("        scope: 'openid email profile User.Read',\n      }),\n    });",
 "        scope: 'openid email profile User.Read',\n      }),\n      "+SIG+"\n    });"),
("      headers: { Authorization: `Bearer ${access_token}` },\n    });",
 "      headers: { Authorization: `Bearer ${access_token}` },\n      "+SIG+"\n    });")]
TEST='''// KS-1240 (class: hand-built outbound fetches with no timeout), services/auth social adapters apple.ts, facebook.ts and microsoft-personal.ts: their five fetches (apple token; facebook token and /me;
// microsoft token and graph /me) passed no `signal`, so an identity provider that accepts the connection and never answers held the OAuth callback open for as long as the socket lived. Facebook's two
// fetches were called with a URL only, so they gain an init object. The adapters are driven directly with a stubbed global fetch that honours `init.signal` (and never answers when there is none); nothing
// touches the network. R1 to R3 pin that every fetch carries an AbortSignal, R4 that each bound is a sane positive number, R5 to R7 that a provider that never answers ends in a rejection, not a hang.
import { describe, it, expect, afterEach, vi } from 'vitest';
import { AppleProvider } from '../providers/social/apple';
import { FacebookProvider } from '../providers/social/facebook';
import { MicrosoftPersonalProvider } from '../providers/social/microsoft-personal';

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

/** An Apple id_token whose payload segment carries `sub`, as the adapter decodes it. */
function appleIdToken(): string {
  return 'h.' + Buffer.from(JSON.stringify({ sub: 'a1', email: 'a@x.test', email_verified: true })).toString('base64') + '.s';
}

/** Answers by URL and records the signal each call carried (the second argument may be missing). */
function stubAnswering(seen: Seen[]): void {
  vi.spyOn(globalThis, 'fetch').mockImplementation((async (url: unknown, init?: { signal?: unknown }) => {
    const u = String(url);
    seen.push({ url: u, signal: init?.signal });
    if (u.includes('appleid.apple.com/auth/token')) return reply(200, { id_token: appleIdToken() });
    if (u.includes('graph.facebook.com/v19.0/oauth/access_token')) return reply(200, { access_token: 'tok' });
    if (u.includes('graph.facebook.com/v19.0/me')) return reply(200, { id: 'f1', email: 'f@x.test', name: 'F B' });
    if (u.includes('login.microsoftonline.com/consumers')) return reply(200, { access_token: 'tok' });
    if (u.includes('graph.microsoft.com/v1.0/me')) return reply(200, { id: 'm1', mail: 'm@x.test', displayName: 'M S' });
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

describe('KS-1240: the apple, facebook and microsoft-personal adapters bound their outbound fetches', () => {
  it('RED KS-1240 R1 the apple token fetch carries an AbortSignal', async () => {
    const seen: Seen[] = [];
    stubAnswering(seen);
    await new AppleProvider(CONFIG).exchangeCode('code');
    expect(seen).toHaveLength(1);
    for (const call of seen) expect(call.signal).toBeInstanceOf(AbortSignal);
  });

  it('RED KS-1240 R2 both facebook fetches (token, me) carry an AbortSignal', async () => {
    const seen: Seen[] = [];
    stubAnswering(seen);
    await new FacebookProvider(CONFIG).exchangeCode('code');
    expect(seen).toHaveLength(2);
    for (const call of seen) expect(call.signal).toBeInstanceOf(AbortSignal);
  });

  it('RED KS-1240 R3 both microsoft fetches (token, graph me) carry an AbortSignal', async () => {
    const seen: Seen[] = [];
    stubAnswering(seen);
    await new MicrosoftPersonalProvider(CONFIG).exchangeCode('code');
    expect(seen).toHaveLength(2);
    for (const call of seen) expect(call.signal).toBeInstanceOf(AbortSignal);
  });

  it('RED KS-1240 R4 the five bounds handed to AbortSignal.timeout are positive and at most 30000 ms', async () => {
    const timeout = vi.spyOn(AbortSignal, 'timeout');
    stubAnswering([]);
    await new AppleProvider(CONFIG).exchangeCode('code');
    await new FacebookProvider(CONFIG).exchangeCode('code');
    await new MicrosoftPersonalProvider(CONFIG).exchangeCode('code');
    const bounds = timeout.mock.calls.map((c) => c[0] as number);
    expect(bounds).toHaveLength(5);
    for (const ms of bounds) {
      expect(ms).toBeGreaterThan(0);
      expect(ms).toBeLessThanOrEqual(30000);
    }
  });

  it('RED KS-1240 R5 an apple token endpoint that never answers ends in a rejection, not a hang', async () => {
    vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => AbortSignal.abort());
    stubNeverAnswering();
    expect(await outcome(() => new AppleProvider(CONFIG).exchangeCode('code'))).toBe('REJECTED');
  });

  it('RED KS-1240 R6 a facebook token endpoint that never answers ends in a rejection, not a hang', async () => {
    vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => AbortSignal.abort());
    stubNeverAnswering();
    expect(await outcome(() => new FacebookProvider(CONFIG).exchangeCode('code'))).toBe('REJECTED');
  });

  it('RED KS-1240 R7 a microsoft token endpoint that never answers ends in a rejection, not a hang', async () => {
    vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => AbortSignal.abort());
    stubNeverAnswering();
    expect(await outcome(() => new MicrosoftPersonalProvider(CONFIG).exchangeCode('code'))).toBe('REJECTED');
  });

  it('control KS-1240 C1 the full exchange of each adapter still resolves to the same provider id', async () => {
    stubAnswering([]);
    expect((await new AppleProvider(CONFIG).exchangeCode('code')).providerId).toBe('a1');
    expect((await new FacebookProvider(CONFIG).exchangeCode('code')).providerId).toBe('f1');
    expect((await new MicrosoftPersonalProvider(CONFIG).exchangeCode('code')).providerId).toBe('m1');
  });

  it('control KS-1240 C2 a refused apple token exchange still throws its own message', async () => {
    vi.spyOn(globalThis, 'fetch').mockImplementation((async () => reply(400, 'invalid_grant')) as never);
    await expect(new AppleProvider(CONFIG).exchangeCode('code')).rejects.toThrow('Apple token exchange failed: invalid_grant');
  });
});
'''
S=dict(dir='ks_1240_p5_social2',ticket='KS-1240',
 title='(class, slice 5) auth social adapters apple.ts, facebook.ts, microsoft-personal.ts: five outbound fetches carry no timeout, two of them are called with a URL only (no init object yet); add AbortSignal.timeout (RUNG 3, code_patch2: 3 products, 5 sites + 3 constants, one NEW behavioural vitest file)',
 intro="DRAFT by a Spark brief drafter for Wednesday, batch 4 of 2026-10-28 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Slice 5 of the KS-1240 class (hand-built fetch with no timeout): the other three identity-provider adapters in services/auth, beside slice 4 (github, google, linkedin; a different brief and different files). KS-1240 is the gateway ticket; applying it to the auth adapters is the drafter's extension, stated: the raise seat confirms the scope with the owner. On expiry the fetch rejects and `exchangeCode` rejects like it does for any provider failure; nothing new is built. The variation from slice 4: facebook's two fetches are called with a URL only, so they GAIN a second argument. The Spark may fail this one (capability data).",
 products=[(PG,G_edits),(PGO,GO_edits),(PL,LI_edits)],
 prodnote=['product 1 (apple.ts), modified in place: TWO hunks - the constant after the import, then one `signal:` line in the token fetch','product 2 (facebook.ts), modified in place: THREE hunks - the constant, then a new second argument `{ signal: ... },` on each of the 2 fetches','product 3 (microsoft-personal.ts), modified in place: THREE hunks - the constant, then one `signal:` line in each of the 2 fetches'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 9 cells (7 red, 2 control; stubbed fetch, no network)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1240-social-provider-fetches-are-bounded-apple-facebook-microsoft.test.ts` from `Blockchain/Dev/services/auth',
 tier='code_patch2', rung='3 (eight hunks in three products given byte-exact; the new test given whole)',
 pins='''# code_patch2: 3 products in services/auth providers/social (apple.ts 2 hunks; facebook.ts 3; microsoft-personal.ts 3) + 1 NEW vitest file; ref = ks1617 (fetch-stub adapter spec, shape only); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/auth/src/__tests__/ks1617-social-profile-fetch-failure-names-the-http-status.test.ts
line=2
ctx=65536
''',
 wrong="The Apple, Facebook and Microsoft-personal adapters (`services/auth/src/providers/social/apple.ts`, `facebook.ts`, `microsoft-personal.ts`) call `fetch` five times in all (apple: token exchange; facebook: token exchange and `/me`; microsoft: token exchange and graph `/me`) with no `signal`. An identity provider that accepts the connection and never answers holds the OAuth callback request open for as long as the socket lives. In each adapter `exchangeCode` lets a rejected fetch propagate, so a timeout needs no new handling. The change adds, per file, one module constant `SOCIAL_PROVIDER_FETCH_TIMEOUT_MS = 10_000` (with a comment) after the `./types` import and `signal: AbortSignal.timeout(SOCIAL_PROVIDER_FETCH_TIMEOUT_MS),` in each fetch's init object. Facebook's two fetches pass the URL alone, so each gains a second argument `{ signal: AbortSignal.timeout(SOCIAL_PROVIDER_FETCH_TIMEOUT_MS) },` on its own line before the closing parenthesis. For a healthy provider nothing changes.",
 where="- each file: **must change** (insertion) - after line 1 (`import { SocialProvider, ... } from './types';`) a blank line, three comment lines and the constant line.\n- `apple.ts` (tip numbers): the init object of the fetch at :25, after `body: new URLSearchParams({...}),`.\n- `facebook.ts`: the fetch at :24 (token) and the fetch at :39 (`/me`): a new line `      { signal: ... },` after the URL argument, before `    );`.\n- `microsoft-personal.ts`: the init objects at :25 (after `body: new URLSearchParams({...}),`) and :44 (after `headers: {...},`).\n- Every other line of the three files and the other three adapters (github, google, linkedin: slice 4) are NOT touched.",
 exactnote="EIGHT hunks in three files: apple two, facebook three, microsoft-personal three. Each file's first hunk is the constant block.\n",
 donot="**Do NOT touch** any other line of the three adapters, github / google / linkedin, `types.ts`, or any other file.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. Pure ASCII, vitest imports, no top-level await. It drives the three adapters directly with a stubbed global `fetch` (answering by URL, or honouring `init.signal`), spies on `AbortSignal.timeout`, and never touches the network.",
 red=['RED KS-1240 R1','RED KS-1240 R2','RED KS-1240 R3','RED KS-1240 R4','RED KS-1240 R5','RED KS-1240 R6','RED KS-1240 R7'],
 cells="- RED `R1` to `R3`: at the tip no fetch carries `init.signal` (facebook's calls have no init at all), so `toBeInstanceOf(AbortSignal)` fails; after the edit every call carries one.\n- RED `R4`: at the tip `AbortSignal.timeout` is never called (0 bounds, not 5); after the edit 5 bounds, each positive and at most 30000.\n- RED `R5` to `R7`: `AbortSignal.timeout` is made to return an already-aborted signal and the fetch stub honours it; at the tip no signal is passed, the stub never answers and the cell reads `HUNG` after 300 ms; after the edit the fetch rejects and the cell reads `REJECTED`.\n- CONTROL `C1`, `C2`: green at the tip AND after (each adapter's full exchange resolves to the same provider id; a 400 token reply still throws Apple's message).",
 premises="- Each adapter's `exchangeCode` awaits its fetches with no try/catch of its own (apple.ts :24-:48, facebook.ts :23-:60, microsoft-personal.ts :24-:57), so a rejection propagates to the caller (read from the cache clone at the tip).\n- The first line of each of the three files is the `./types` import quoted above (byte-identical in all three; the generator edits each file separately).\n- facebook.ts calls `fetch(` with a template-literal URL and no second argument at :24 and :39 (read at the tip).\n- ks1617 already stubs `globalThis.fetch` with `vi.spyOn` against adapters of this shape.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- Whether 10000 ms is the right bound for a social login: the value is the drafter's; the raise seat confirms with the owner. A signal also bounds reading the response body.\n- How the OAuth callback presents a rejected exchangeCode (the existing catch is relied on, not read or pinned here).\n- Open PRs touching these files: none by the file lists of every open PR read on 2026-10-28.",
 scope="**Slice 5 of the KS-1240 class, services/auth social adapters (the other three of six).** Link the PR as Refs KS-1240, never a close-word.",
)
