import sys
sys.path.insert(0,'/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator107/gen')
import brieflib
TIP='2935f723109756a60cadc5521977c7a036ec322d'
TEST='''import { describe, it, expect, vi, afterEach } from 'vitest';

// KS-1974 (identus client only): IdentusClient.resolveDID (src/prism/identus-client.ts) is a resolver: a failed lookup is a result
// with `didDocument: null` and `didResolutionMetadata.error: 'notFound'` plus an `errorMessage` TEXT. Its catch reads the failure
// into `errorMessage` inside a try (KS-1868) as `err instanceof Error ? err.message : String(err)`, which guards a read that
// THROWS but not a read that RETURNS a non-string: an Error whose `message` is a Symbol, an object whose toString throws comes back as that value itself, so `errorMessage` is not text. The fetch stand-in is a plain function rejecting
// with the cell's value (stubbed with `vi.stubGlobal`, removed after each cell); the logger is a plain no-op object; no network.
vi.mock('../logger', () => ({
  logger: {
    debug: () => undefined,
    info: () => undefined,
    warn: () => undefined,
    error: () => undefined,
  },
}));

import { IdentusClient } from '../prism/identus-client';

/** The resolution result, or the string 'rejected' when resolveDID rejects (an assertion can then fail on it). */
async function resolve(value: unknown): Promise<unknown> {
  vi.stubGlobal('fetch', () => Promise.reject(value));
  const client = new IdentusClient({ cloudAgentUrl: 'http://agent.invalid' });
  try {
    return await client.resolveDID('did:prism:ks1974');
  } catch {
    return 'rejected';
  }
}

const notFound = (errorMessage: string): unknown => ({
  didDocument: null,
  didResolutionMetadata: { error: 'notFound', errorMessage },
  didDocumentMetadata: {},
});

const withMessage = (m: unknown): unknown =>
  Object.create(Error.prototype, {
    message: {
      get() {
        return m;
      },
    },
  });

const toStringThrows = (): unknown => ({
  toString() {
    throw new Error('toString boom');
  },
});

describe('KS-1974 IdentusClient.resolveDID answers text for a non-string message', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('control ks1974 C1 an ordinary Error gives the notFound result with its message', async () => {
    expect(await resolve(new Error('connection refused'))).toEqual(notFound('connection refused'));
  });

  it('control ks1974 C2 a thrown plain string gives the notFound result with that text', async () => {
    expect(await resolve('plain text failure')).toEqual(notFound('plain text failure'));
  });

  it('RED ks1974 R1 an Error whose message is a Symbol gives the notFound result with the symbol as text', async () => {
    expect(await resolve(withMessage(Symbol('ks1974')))).toEqual(notFound('Symbol(ks1974)'));
  });

  it('RED ks1974 R2 an Error whose message is an object whose toString throws gives the notFound result with a constant reason', async () => {
    expect(await resolve(withMessage(toStringThrows()))).toEqual(notFound('unreadable thrown value'));
  });
});
'''
spec=dict(
 key='ks_1974_o107_p4b_shared_identus_client_resolve_did_non_string_message_is_text',
 ticket='KS-1974', tag='ks1974', tip=TIP, area='shared',
 title='shared: `IdentusClient.resolveDID` in `src/prism/identus-client.ts` must answer an `errorMessage` that is text when the failure\'s message is not a string (identus client only; PART of KS-1974)',
 origin='Origin: KS-1974 (gate 177 finding G177-F3, LOW, pre-existing): the KS-1868 guards protect a message read that THROWS, not one that RETURNS a non-string, so `IdentusClient.resolveDID` returns an `errorMessage` of type symbol or object (6 cells in the gate). It fails closed (`didDocument` stays null, status `notFound`). THIS brief covers the identus client only; the credential verifier template (outer catch), `ServiceClient.healthCheck` and the gateway health dashboard are NOT in it.',
 product='packages/shared/src/prism/identus-client.ts',
 test='packages/shared/src/__tests__/ks1974-identus-client-resolve-did-non-string-message-is-text.test.ts',
 ref='packages/shared/src/__tests__/ks1868-identus-client-resolve-did-catch-unreadable-throw.test.ts',
 runner='vitest', runcmd='npx vitest run src/__tests__/ks1974-identus-client-resolve-did-non-string-message-is-text.test.ts', rundir='packages/shared',
 edits=[("""        errorMessage = err instanceof Error ? err.message : String(err);
""","""        errorMessage = String(err instanceof Error ? err.message : err);
""")],
 reds=[('R1',),('R2',)], controls=[('C1',),('C2',)],
 test_body=TEST,
 test_note='The shape is copied from the merged sibling suite of this directory (`ks1868-identus-client-resolve-did-catch-unreadable-throw.test.ts`; pinned ref the same file): `fetch` is stubbed with `vi.stubGlobal` to a plain function rejecting with the cell\'s value and removed after each cell, the logger is a plain no-op object.',
 wrong='In `IdentusClient.resolveDID`, the catch computes `errorMessage` inside a `try` as `err instanceof Error ? err.message : String(err)` with the constant `\'unreadable thrown value\'` on throw. A message READ that returns a non-string passes the guard and is returned as is, so `errorMessage` of the resolution metadata is a Symbol or an object instead of text. The fix is ONE line inside the same `try`: coerce the whole conditional with `String(...)`: `errorMessage = String(err instanceof Error ? err.message : err);`. For every string message and every non-Error value the result is exactly what it was (`String(err)` for a non-Error; the message itself for a string; `undefined`/`null` messages read as the words `undefined`/`null` as `String` would have said for a non-Error); a Symbol message reads as its text `Symbol(...)`; a value `String()` cannot convert lands in the existing constant fallback.',
 where='line 134 (`IdentusClient.resolveDID`, the `errorMessage` line inside the catch\'s `try`). CALLERS: resolvers of PRISM DIDs read `didResolutionMetadata.errorMessage`. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): `{ didDocument: null, didResolutionMetadata: { error: \'notFound\', errorMessage: <text> }, didDocumentMetadata: {} }`. Today (non-string message): the same shape with a non-text `errorMessage`. After: text. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** for a lookup failure whose Error message is a Symbol or an object whose toString throws, `errorMessage` is text (the symbol\'s text, or the constant) instead of the non-string value; every other failure reads exactly as before. Fail-closed, as before. TIER 2 (a result field, no money or authorization path).',
 cells_text="""- RED at the tip, GREEN after: `R1` (message is a Symbol) and `R2` (message is an object whose toString throws) (2 cells). At the tip `errorMessage` is the non-string value, so `toEqual` fails by assertion; after the edit it is text.
- GREEN at the tip and after: 'control ks1974 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells).
""",
 premises='- Premise: `identus-client.ts` lines 115-147 read at `2935f7231097` (git show); the `String(...)` coercion sits inside the `try` the file already has (133-137).\n- Ticket KS-1974 (Backlog, 0 comments) read whole at source on 2026-11-09.',
 unmeasured='A real Identus cloud agent was not run. Whether any real client emits such a value is not known. The three other KS-1974 sites (verifier outer catch, ServiceClient.healthCheck, health-dashboard) are NOT touched. P3 (KS-1973) of this operator edits vc/verifier.ts, a different file.',
 scope='Refs KS-1974; does NOT close it (identus client only), and introduces no new helper.',
 started_ok='KS-1974_gate177_finding_G177-F3_identus_client_part;_operator_107_screen;_status_not_read_by_operator;_open_PRs_(44_PRs_295_files_read_2026-11-09_by_op107,_planted_control_services/originate_in_16_entries)_checked;_live_lanes_beyond_PRs_not_checked',
)
spec['roundtxt']='ROUND 2 OF 2: this REBRIEFS round 1 (ks_1974_o107_p4, quarantined in night/_quarantine_2026-11-09/briefs_unused/), whose control FAILED at A4: cell R3 (a revoked Proxy as the message) crashes vitest\'s toEqual with a TypeError instead of failing by assertion, a test-side defect; the model round ran on that brief anyway (operator sequencing error) and answered the golden byte for byte. R3 is dropped. Counter: original + this one rebrief.'
brieflib.make(spec)
