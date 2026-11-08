import sys
sys.path.insert(0,'/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator107/gen')
import brieflib
TIP='2935f723109756a60cadc5521977c7a036ec322d'
TEST='''import { describe, it, expect, vi } from 'vitest';

// KS-1971: resolvePublicAddresses (src/security/ssrf-guard.ts) resolves a host and refuses it when the lookup fails. Its catch
// reads the failure's `.message` inside a try (KS-1868, pull request 1992) but builds the refusal text with the template
// literal `could not be resolved (${reason})` OUTSIDE any guard. When the read succeeds and returns something a template
// literal cannot turn into text (a Symbol, an object whose toString throws, a revoked Proxy) the template literal throws, so the
// call REJECTS instead of returning { ok: false, error }, and so do assertResolvedHostPublic and the callers above it. The DNS
// module is a plain stand-in whose lookup rejects with the cell's value; no network.
const h = vi.hoisted(() => ({ toThrow: undefined as unknown }));

vi.mock('dns/promises', () => ({
  lookup: () => Promise.reject(h.toThrow),
}));

import { assertResolvedHostPublic, resolvePublicAddresses } from '../security/ssrf-guard';

type Outcome = { rejected: boolean; result: { ok: boolean; error?: string } | undefined };

async function run(value: unknown): Promise<Outcome> {
  h.toThrow = value;
  try {
    const result = await resolvePublicAddresses('ks1971.example.test');
    return { rejected: false, result };
  } catch {
    return { rejected: true, result: undefined };
  }
}

const withMessage = (m: unknown): unknown =>
  Object.create(Error.prototype, {
    message: {
      get() {
        return m;
      },
    },
  });

const revokedProxy = (): unknown => {
  const { proxy, revoke } = Proxy.revocable({}, {});
  revoke();
  return proxy;
};

const toStringThrows = (): unknown => ({
  toString() {
    throw new Error('toString boom');
  },
});

describe('KS-1971 resolvePublicAddresses builds its refusal text safely', () => {
  it('control ks1971 C1 an ordinary Error is refused with its message in the reason', async () => {
    const out = await run(new Error('ENOTFOUND boom'));
    expect(out.rejected).toBe(false);
    expect(out.result?.ok).toBe(false);
    expect(out.result?.error).toContain('host "ks1971.example.test" could not be resolved (ENOTFOUND boom)');
  });

  it('control ks1971 C2 a thrown plain string is refused with an undefined message in the reason', async () => {
    const out = await run('plain text failure');
    expect(out.rejected).toBe(false);
    expect(out.result?.ok).toBe(false);
    expect(out.result?.error).toContain('host "ks1971.example.test" could not be resolved (undefined)');
  });

  it('RED ks1971 R1 an Error whose message is a Symbol is refused with that symbol as text', async () => {
    const out = await run(withMessage(Symbol('ks1971')));
    expect(out.rejected).toBe(false);
    expect(out.result?.ok).toBe(false);
    expect(out.result?.error).toContain('host "ks1971.example.test" could not be resolved (Symbol(ks1971))');
  });

  it('RED ks1971 R2 an Error whose message is an object whose toString throws is refused with a constant reason', async () => {
    const out = await run(withMessage(toStringThrows()));
    expect(out.rejected).toBe(false);
    expect(out.result?.ok).toBe(false);
    expect(out.result?.error).toContain('host "ks1971.example.test" could not be resolved (unreadable thrown value)');
  });

  it('RED ks1971 R3 an Error whose message is a revoked Proxy is refused with a constant reason', async () => {
    const out = await run(withMessage(revokedProxy()));
    expect(out.rejected).toBe(false);
    expect(out.result?.ok).toBe(false);
    expect(out.result?.error).toContain('host "ks1971.example.test" could not be resolved (unreadable thrown value)');
  });

  it('RED ks1971 R4 assertResolvedHostPublic answers the refusal text for an Error whose message is a Symbol', async () => {
    h.toThrow = withMessage(Symbol('ks1971'));
    let answer: string | null | undefined;
    let rejected = false;
    try {
      answer = await assertResolvedHostPublic('ks1971.example.test');
    } catch {
      rejected = true;
    }
    expect(rejected).toBe(false);
    expect(typeof answer).toBe('string');
  });
});
'''
spec=dict(
 key='ks_1971_o107_p2_shared_ssrf_guard_refusal_text_survives_non_string_message',
 ticket='KS-1971', tag='ks1971', tip=TIP, area='shared',
 title='shared: `resolvePublicAddresses` in `src/security/ssrf-guard.ts` must still return its refusal when the failed lookup\'s message is not text (SECURITY SURFACE: SSRF guard, tier 1 gate owed)',
 origin='Origin: KS-1971 (gate 176 finding G176-F2, LOW, pre-existing): the catch reads `(err as Error).message` inside a `try` but builds the refusal with the template literal on the next statement, outside any guard, so a message that is a Symbol, a revoked Proxy or an object whose `toString` throws makes the template literal throw and the function REJECTS instead of returning `{ ok: false, error }`. Every affected cell is LESS permissive than the ordinary refusal (nothing allowed, 0 requests built): a robustness gap, not a bypass. The fix shape is the ticket\'s own ("coerce the message there, inside the same try").',
 product='packages/shared/src/security/ssrf-guard.ts',
 test='packages/shared/src/__tests__/ks1971-ssrf-guard-refusal-text-non-string-message.test.ts',
 ref='packages/shared/src/__tests__/ks1868-ssrf-guard-resolve-public-addresses-catch-unreadable-throw.test.ts',
 runner='vitest', runcmd='npx vitest run src/__tests__/ks1971-ssrf-guard-refusal-text-non-string-message.test.ts', rundir='packages/shared',
 edits=[("""    let reason: string;
    try {
      reason = (err as Error).message;
""","""    let reason: string;
    try {
      reason = String((err as Error).message);
""")],
 reds=[('R1',),('R2',),('R3',),('R4',)], controls=[('C1',),('C2',)],
 test_body=TEST,
 test_note='The shape is copied from the merged sibling suite of this directory (`ks1868-ssrf-guard-resolve-public-addresses-catch-unreadable-throw.test.ts`; pinned ref the same file). The DNS module is a plain stand-in whose lookup rejects with the cell\'s value (`vi.hoisted` + `vi.mock(\'dns/promises\')`, exactly as the sibling); no network.',
 wrong='In `resolvePublicAddresses`, the lookup-failure catch reads the message inside a `try` (`reason = (err as Error).message;`, fallback `\'unreadable thrown value\'`), and the next statement builds `error: \\`host "${bare}" could not be resolved (${reason}) - refusing to contact an unverifiable destination\\``. When the read RETURNS a value a template literal cannot convert (a Symbol; an object whose `toString` throws; a revoked Proxy) the read passes the guard and the template literal throws outside it, so the function REJECTS instead of returning the refusal; `assertResolvedHostPublic`, `assertSafeOutboundUrl` and `safeOutboundRequest` reject with it. The fix is ONE line: coerce inside the existing `try` with `String(...)`: `reason = String((err as Error).message);`. A Symbol then reads as its text `Symbol(...)`, a value `String()` cannot convert lands in the existing fallback constant, and every string, `undefined` and `null` message reads exactly as it did in the template (`undefined` stays the word `undefined`). The template literal line is NOT touched.',
 where='line 327 (`resolvePublicAddresses`, the lookup-failure catch; the template literal that uses `reason` is line 333 and stays). CALLERS: `assertResolvedHostPublic` (351), `assertSafeOutboundUrl` (364) and `safeOutboundRequest` (483) await it. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the call returns `{ ok: false, error: \'host "<h>" could not be resolved (<message>) ...\' }` and the caller refuses the destination, builds no request. Today (non-string message): the call rejects. After: the same refusal, with the symbol\'s text or the constant in the parentheses. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** for a lookup failure whose message is a Symbol, an object whose toString throws or a revoked Proxy, the guard answers its normal refusal instead of rejecting; every string, undefined and null message reads exactly as before. The guard stays fail-closed: nothing in this change can turn a refusal into a pass. SECURITY SURFACE (SSRF guard): TIER 1 GATE OWED before any raise; the edit is one fully spelled-out line.',
 cells_text="""- RED at the tip, GREEN after: `R1` (message is a Symbol), `R2` (message is an object whose toString throws), `R3` (message is a revoked Proxy) and `R4` (assertResolvedHostPublic with a Symbol message) (4 cells). At the tip the template literal throws and the call rejects, so the first assertion fails; after the edit the refusal is returned.
- GREEN at the tip and after: 'control ks1971 C1' (an ordinary Error) and 'C2' (a thrown plain string, whose message reads `undefined`), both already true at the tip (2 cells).
""",
 premises='- Premise: `ssrf-guard.ts` lines 300-349 and 351-354 read at `2935f7231097` (git show); the `String(...)` coercion sits inside the same `try` the file already has (324-330); the template literal at 333 is unchanged.\n- Ticket KS-1971 (Backlog, 0 comments) read whole at source on 2026-11-09. A `${undefined}` in a template literal and `String(undefined)` both give the word `undefined` (control C2 pins it).',
 unmeasured='A real DNS lookup was not run. Whether any real resolver emits a non-string message is not known (the ticket says the same). The downstream effect in originate\'s `dispatchEvent` (loop abort) was not run; the `safeOutboundRequest` request-construction catch (non-string `error`, ticket remark) is a different site and is NOT touched.',
 scope='Refs KS-1971; does NOT close it (the request-construction catch is separate), and introduces no new helper.',
 started_ok='KS-1971_gate176_finding_G176-F2;_security_surface_(ssrf-guard)_tier_1_gate_owed;_operator_107_screen;_status_not_read_by_operator;_open_PRs_(44_PRs_295_files_read_2026-11-09_by_op107,_planted_control_services/originate_in_16_entries)_checked;_live_lanes_beyond_PRs_not_checked',
)
brieflib.make(spec)
