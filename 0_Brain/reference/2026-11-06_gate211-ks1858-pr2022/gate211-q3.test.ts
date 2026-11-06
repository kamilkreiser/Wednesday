// Gate 211 Q3 probe. FAIL at head = a trim-removable whitespace-only token reaches the profile call, a visible token is altered
// on its way to the profile call, or a non-string causes a TypeError. Only fetch and the logger sink are replaced; each adapter's guard is the real code.
import { describe, it, vi, afterAll } from 'vitest';
import { appendFileSync } from 'node:fs';

const { sink } = vi.hoisted(() => ({
  sink: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() },
}));
vi.mock('../utils/logger', () => ({ logger: sink, createLogger: () => sink, validateEnv: vi.fn() }));
vi.mock('@secuura/shared/utils/logger', () => ({ logger: sink, createLogger: () => sink }));

import { GoogleProvider } from '../providers/social/google';
import { FacebookProvider } from '../providers/social/facebook';
import { LinkedInProvider } from '../providers/social/linkedin';
import { MicrosoftPersonalProvider } from '../providers/social/microsoft-personal';
import { GitHubProvider } from '../providers/social/github';

const OUT = process.env.GATE211_OUT as string;
const CONFIG = { clientId: 'cid', clientSecret: 'sec', callbackUrl: 'https://app.test/cb', enabled: true };
const ADAPTERS: [string, string, new (c: typeof CONFIG) => { exchangeCode(c: string): Promise<unknown> }][] = [
  ['google', 'Google', GoogleProvider as never], ['facebook', 'Facebook', FacebookProvider as never], ['linkedin', 'LinkedIn', LinkedInProvider as never],
  ['microsoft-personal', 'Microsoft', MicrosoftPersonalProvider as never], ['github', 'GitHub', GitHubProvider as never],
];

const ABSENT = Symbol('absent');
// The commission's 18 values.
const VALUES: [string, unknown, string][] = [
  ['empty', '', 'ws'], ['space', ' ', 'ws'], ['tab', '\t', 'ws'], ['lf', '\n', 'ws'], ['mixed', ' \t\r\n ', 'ws'], ['nbsp', ' ', 'ws'], ['emsp', ' ', 'ws'], ['bom', '﻿', 'ws'],
  ['zwsp', '​', 'zwsp'], ['abc', 'abc', 'vis'], ['_abc_', ' abc ', 'vis'], ['a_b', 'a b', 'vis'],
  ['absent', ABSENT, 'nonstr'], ['null', null, 'nonstr'], ['zero', 0, 'nonstr'], ['n123', 123, 'nonstr'], ['obj', {}, 'nonstr'], ['arr', [], 'nonstr'],
];
// Every BMP code unit trim removes, derived from the runtime rather than from a list, each alone and padded.
const TRIMSET: number[] = [];
for (let c = 0; c <= 0xffff; c++) if (String.fromCharCode(c).trim() === '') TRIMSET.push(c);
// Extra visible-or-odd shapes the commission did not list.
const EXTRA: [string, unknown, string][] = [
  ['true', true, 'nonstr'], ['false', false, 'nonstr'], ['arr_space', [' '], 'nonstr'], ['longws1M', ' '.repeat(1 << 20), 'ws'],
  ['nul', '\u0000', 'odd'], ['nel', '\u0085', 'odd'], ['zwsp_padded', ' ​ ', 'odd'], ['tab_abc_lf', '\tabc\n', 'vis'], ['nbsp_abc', ' abc', 'vis'],
];

function row(o: unknown) { appendFileSync(OUT, JSON.stringify(o) + '\n'); }

async function drive(adapter: string, brand: string, Ctor: new (c: typeof CONFIG) => { exchangeCode(c: string): Promise<unknown> }, label: string, cls: string, value: unknown, extra: Record<string, unknown> = {}) {
  sink.warn.mockClear();
  const calls: { url: string; auth?: string }[] = [];
  const body: Record<string, unknown> = { ...extra };
  if (value !== ABSENT) body.access_token = value;
  vi.stubGlobal('fetch', vi.fn(async (url: unknown, init?: { headers?: Record<string, string> }) => {
    calls.push({ url: String(url), auth: init?.headers?.Authorization });
    // First call is the token endpoint; anything after it is a profile call, answered 401.
    if (calls.length === 1) return new Response(JSON.stringify(body), { status: 200, headers: { 'content-type': 'application/json' } });
    return new Response('{}', { status: 401 });
  }));
  let outcome = 'RESOLVED'; let errName = '';
  try { await new Ctor(CONFIG).exchangeCode('code'); } catch (e) { outcome = (e as Error).message; errName = (e as Error).constructor.name; }
  vi.unstubAllGlobals();
  const refusalMsg = `${brand} token exchange failed (no access token)`;
  const reached = calls.length > 1;
  let carried: string | null = null;
  if (reached) {
    const p = calls[1];
    carried = p.auth !== undefined ? p.auth.replace(/^Bearer /, '') : decodeURIComponentSafe(p.url.split('access_token=')[1] ?? '');
  }
  const cell = outcome === refusalMsg && !reached ? 'REFUSED' : reached ? 'PROFILE' : 'OTHER';
  row({ adapter, label, cls, cell, reached, carried, sent: typeof value === 'string' ? value : null, exact: typeof value === 'string' && reached ? carried === value : null,
    outcome, errName, calls: calls.length, warn: JSON.stringify(sink.warn.mock.calls), extra });
}
function decodeURIComponentSafe(s: string) { return s; }

describe('gate211 q3', () => {
  for (const [adapter, brand, Ctor] of ADAPTERS) {
    it(`${adapter} matrix`, async () => {
      for (const [label, v, cls] of [...VALUES, ...EXTRA]) await drive(adapter, brand, Ctor, label, cls, v);
      for (const c of TRIMSET) {
        await drive(adapter, brand, Ctor, `trimset_U+${c.toString(16).padStart(4, '0')}`, 'trimset', String.fromCharCode(c));
      }
    }, 120000);
  }
  it('github error field', async () => {
    const [adapter, brand, Ctor] = ADAPTERS[4];
    for (const err of ['bad_verification_code', 1, true, '', null, 0, false, {}]) {
      await drive(adapter, brand, Ctor, `SENTINELtok+error=${JSON.stringify(err)}`, 'errfield', 'SENTINELtok', { error: err });
    }
    await drive(adapter, brand, Ctor, 'space+error', 'errfield', ' ', { error: 'x' });
    await drive(adapter, brand, Ctor, 'SENTINELtok+error=long', 'errfield', 'SENTINELtok', { error: 'E'.repeat(200) });
  });
  afterAll(() => { row({ end: true, trimset: TRIMSET.length }); });
});
