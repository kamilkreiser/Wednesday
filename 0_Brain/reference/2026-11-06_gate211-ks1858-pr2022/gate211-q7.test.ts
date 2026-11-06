// Gate 211 Q7 and wire-shape probe. Token answer stubbed; the profile call is built with the real Request constructor, then answered 401: no socket opens.
import { describe, it, vi } from 'vitest';
import { appendFileSync } from 'node:fs';
const { sink } = vi.hoisted(() => ({ sink: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() } }));
vi.mock('../utils/logger', () => ({ logger: sink, createLogger: () => sink, validateEnv: vi.fn() }));
vi.mock('@secuura/shared/utils/logger', () => ({ logger: sink, createLogger: () => sink }));
import { GoogleProvider } from '../providers/social/google';
import { FacebookProvider } from '../providers/social/facebook';
import { LinkedInProvider } from '../providers/social/linkedin';
import { MicrosoftPersonalProvider } from '../providers/social/microsoft-personal';
import { GitHubProvider } from '../providers/social/github';
const OUT = process.env.GATE211_OUT as string;
const CONFIG = { clientId: 'c', clientSecret: 's', callbackUrl: 'https://app.test/cb', enabled: true };
const AD: [string, new (c: typeof CONFIG) => { exchangeCode(c: string): Promise<unknown> }][] = [['google', GoogleProvider as never], ['facebook', FacebookProvider as never], ['linkedin', LinkedInProvider as never], ['microsoft-personal', MicrosoftPersonalProvider as never], ['github', GitHubProvider as never]];
const SHAPES: [string, string][] = [['null_body', 'null'], ['non_json_200', '<html>nope</html>'], ['zwsp', JSON.stringify({ access_token: '​' })], ['_abc_', JSON.stringify({ access_token: ' abc ' })], ['abc_lf', JSON.stringify({ access_token: 'abc\n' })]];
describe('gate211 q7', () => { for (const [a, C] of AD) it(a, async () => { for (const [label, raw] of SHAPES) {
  let n = 0; let wire: unknown = null;
  vi.stubGlobal('fetch', vi.fn(async (u: string, init?: RequestInit) => { n++; if (n === 1) return new Response(raw, { status: 200 }); const q = new Request(u, init); wire = { auth: q.headers.get('authorization'), url: q.url.split('&access_token=')[1] ?? null }; return new Response('{}', { status: 401 }); }));
  let res = 'RESOLVED', name = ''; try { await new C(CONFIG).exchangeCode('x'); } catch (e) { res = (e as Error).message; name = (e as Error).constructor.name; }
  vi.unstubAllGlobals(); appendFileSync(OUT, JSON.stringify({ a, label, n, name, res: res.slice(0, 90), wire }) + '\n');
} }); });
