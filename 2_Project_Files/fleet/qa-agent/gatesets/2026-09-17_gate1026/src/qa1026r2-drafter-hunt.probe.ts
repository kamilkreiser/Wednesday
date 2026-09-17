// QA #1026 ROUND 2 (KS-839) DRAFTER HUNT — exhaustive over every Unicode code point (surrogates excluded) and over multi-entry concatenations of fragments.
// Oracle = the REAL resolver arithmetic: grant = validateScopes(A, A) (scope omitted) and validateScopes(parseScopeString('openid *'), A) (named); token = parseScopeString(grant.join(' '))
// (routes/oauth.ts:390 / :776 / :972). LEAK = any token entry === '*'. NFKC = any token entry whose NFKC form is '*' (a Record unless a consumer normalizes).
import { describe, it, vi } from 'vitest';
import { writeFileSync } from 'node:fs';
vi.mock('../db', () => ({ query: vi.fn(async () => ({ rows: [], rowCount: 0 })) }));
vi.mock('../utils/logger', () => ({ logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() } }));
import { validateScopes, parseScopeString } from '../services/oauth';
describe('qa1026r2 hunt', () => {
  it('every code point x 5 forms, and fragment concatenations', () => {
    const out: any = { leaks: [], nfkc: [], checked: 0, controlLeaksOnPlainStar: 0 };
    const judge = (A: string[], label: string) => {
      out.checked += 1;
      const toks = [...parseScopeString(validateScopes(A, A).join(' ')), ...parseScopeString(validateScopes(parseScopeString('openid *'), A).join(' '))];
      if (toks.includes('*')) { if (out.leaks.length < 200) out.leaks.push([label, JSON.stringify(A), toks]); out.leakCount = (out.leakCount || 0) + 1; }
      else if (toks.some((t) => t.normalize('NFKC') === '*')) { if (out.nfkc.length < 50) out.nfkc.push([label, JSON.stringify(A), toks]); out.nfkcCount = (out.nfkcCount || 0) + 1; }
    };
    // positive control: the raw splitter itself (no validateScopes guard) DOES turn ' *' into '*'
    out.controlLeaksOnPlainStar = parseScopeString([' *'].join(' ')).includes('*') ? 1 : 0;
    for (let cp = 0; cp <= 0x10ffff; cp++) {
      if (cp >= 0xd800 && cp <= 0xdfff) continue;
      const c = String.fromCodePoint(cp);
      const hex = 'U+' + cp.toString(16).toUpperCase().padStart(4, '0');
      judge([c + '*'], hex + ' c*'); judge(['*' + c], hex + ' *c'); judge(['openid' + c + '*'], hex + ' openid c *'); judge([c], hex + ' c'); judge(['openid', c + '*' + c], hex + ' [openid, c*c]');
    }
    const F = ['', ' ', ',', '*', 'openid', ' ', ';', '|', '​', '\t', ':', 'documents', '＊', '　'];
    const S: string[] = [];
    for (const a of F) for (const b of F) for (const c of F) S.push(a + b + c);
    const U = Array.from(new Set(S));
    out.fragmentStrings = U.length;
    for (const x of U) judge([x], 'frag1');
    const small = U.filter((x) => x.length <= 2);
    out.pairBase = small.length;
    for (const x of small) for (const y of small) judge([x, y], 'frag2');
    writeFileSync(process.env.QA_OUT as string, JSON.stringify(out, null, 1));
  }, 600000);
});
