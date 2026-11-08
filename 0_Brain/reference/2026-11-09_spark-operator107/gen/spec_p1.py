import sys
sys.path.insert(0,'/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator107/gen')
import brieflib
TIP='2935f723109756a60cadc5521977c7a036ec322d'
TEST='''import { describe, it, expect } from 'vitest';

// KS-1972: ContractEventIndexer.isRateLimited (src/blockchain/event-indexer.ts) reads `err?.status_code`, `err?.statusCode`,
// `err?.response?.status` and `err?.message` of a thrown value with no guard, and poll() calls it BEFORE handleError. When the
// read throws (a revoked Proxy, a Proxy whose get trap throws, an Error whose message getter throws) the throw leaves poll()'s
// catch, so poll() rejects and handleError (which already survives such values) is never reached. The cells make the Blockfrost
// stand-in reject with such a value and assert poll() resolves and onError is called, as for an ordinary Error. The api object
// is a plain stand-in, the indexer is reached through a type cast, no network, no timers.
import { ContractEventIndexer } from '../blockchain/event-indexer';

type Outcome = { rejected: boolean; received: unknown[]; backoffMs: unknown };

async function pollWith(value: unknown): Promise<Outcome> {
  const received: unknown[] = [];
  const indexer = new ContractEventIndexer({
    onError: (e: Error) => {
      received.push(e);
    },
  } as never);
  const inner = indexer as unknown as { running: boolean; api: unknown; backoffMs: number; poll(): Promise<void> };
  inner.running = true;
  inner.api = {
    blocksLatest: async () => {
      throw value;
    },
  };
  let rejected = false;
  try {
    await inner.poll();
  } catch {
    rejected = true;
  }
  return { rejected, received, backoffMs: inner.backoffMs };
}

const messageOf = (o: Outcome): unknown => (o.received[0] as { message?: unknown } | undefined)?.message;

const revokedProxy = (): unknown => {
  const { proxy, revoke } = Proxy.revocable({}, {});
  revoke();
  return proxy;
};

const getTrapThrows = (): unknown =>
  new Proxy(
    {},
    {
      get() {
        throw new Error('get trap boom');
      },
    },
  );

const messageGetterThrows = (): unknown =>
  Object.create(Error.prototype, {
    message: {
      get() {
        throw new Error('getter boom');
      },
    },
  });

describe('KS-1972 ContractEventIndexer.poll survives a thrown value whose read throws', () => {
  it('control ks1972 C1 an ordinary Error reaches onError as is and poll resolves', async () => {
    const err = new Error('rpc down');
    const out = await pollWith(err);
    expect(out.rejected).toBe(false);
    expect(out.received.length).toBe(1);
    expect(out.received[0] === err).toBe(true);
  });

  it('control ks1972 C2 a 429 Error backs off and does not reach onError', async () => {
    const out = await pollWith(new Error('429 Too Many Requests'));
    expect(out.rejected).toBe(false);
    expect(out.received.length).toBe(0);
    expect(out.backoffMs).toBe(2000);
  });

  it('RED ks1972 R1 a revoked Proxy reaches onError as an Error with a constant reason and poll resolves', async () => {
    const out = await pollWith(revokedProxy());
    expect(out.rejected).toBe(false);
    expect(out.received.length).toBe(1);
    expect(messageOf(out)).toBe('unreadable thrown value');
  });

  it('RED ks1972 R2 a Proxy whose get trap throws reaches onError as an Error with a constant reason and poll resolves', async () => {
    const out = await pollWith(getTrapThrows());
    expect(out.rejected).toBe(false);
    expect(out.received.length).toBe(1);
    expect(messageOf(out)).toBe('unreadable thrown value');
  });

  it('RED ks1972 R3 an Error whose message getter throws reaches onError as is and poll resolves', async () => {
    const err = messageGetterThrows();
    const out = await pollWith(err);
    expect(out.rejected).toBe(false);
    expect(out.received.length).toBe(1);
    expect(out.received[0] === err).toBe(true);
  });
});
'''
spec=dict(
 key='ks_1972_o107_p1_shared_event_indexer_is_rate_limited_survives_unreadable_value',
 ticket='KS-1972', tag='ks1972', tip=TIP, area='shared',
 title='shared: `ContractEventIndexer.isRateLimited` in `src/blockchain/event-indexer.ts` must answer false, not throw, when the thrown value cannot be read',
 origin='Origin: KS-1972 (gate 176 finding G176-F3, pre-existing): `isRateLimited(err)` reads the thrown value unguarded and `poll()`, `processBlock` and `processTransaction` call it before `handleError`, so a value whose read throws leaves their catch and `poll()` rejects (or the indexer re-reads one block forever). This follows the house guard of the merged KS-1868 passes (a `try` around the read, a safe fallback on throw), inline, no new helper.',
 product='packages/shared/src/blockchain/event-indexer.ts',
 test='packages/shared/src/__tests__/ks1972-event-indexer-is-rate-limited-unreadable-throw.test.ts',
 ref='packages/shared/src/__tests__/ks1868-event-indexer-handle-error-unreadable-throw.test.ts',
 runner='vitest', runcmd='npx vitest run src/__tests__/ks1972-event-indexer-is-rate-limited-unreadable-throw.test.ts', rundir='packages/shared',
 edits=[("""  private isRateLimited(err: any): boolean {
    return (
""","""  private isRateLimited(err: any): boolean {
    try {
      return this.readsAsRateLimited(err);
    } catch {
      // KS-1972: a thrown value whose read throws is not a rate limit; answer false so the caller reaches handleError.
      return false;
    }
  }

  private readsAsRateLimited(err: any): boolean {
    return (
""")],
 ctxn=1, reds=[('R1',),('R2',),('R3',)], controls=[('C1',),('C2',)],
 test_body=TEST,
 test_note='The shape is copied from the merged sibling suite of this directory (`ks1868-event-indexer-handle-error-unreadable-throw.test.ts`; pinned ref the same file). The Blockfrost stand-in is a plain function that throws the value (not `vi.fn()`, on purpose: a spy inspects what it throws and may fail on a revoked Proxy before the code under test sees it); `onError` records what it is given; no network, no timers (the 429 control only sets the backoff, it does not sleep).',
 wrong='`poll()` catches a failure of `blocksLatest` and asks `this.isRateLimited(err)` before it calls `this.handleError(err)`. `isRateLimited` reads `err?.status_code`, `err?.statusCode`, `err?.response?.status` and `err?.message` with no guard, so a thrown value whose read throws (a revoked Proxy; a Proxy whose get trap throws; an Error whose `message` getter throws) makes `isRateLimited` throw inside the catch: `poll()` REJECTS, `handleError` (already guarded by KS-1868, which hands such values to `onError`) is never reached, and `onError` is never called. The fix keeps the existing expression byte for byte (it moves, unchanged, into a new private method `readsAsRateLimited`, so no existing line is re-indented) and makes `isRateLimited` call it inside a `try`, answering `false` when the read throws, so the caller falls to `handleError` exactly as for an ordinary non-429 Error. Every value that can be read returns exactly what it returned before.',
 where='line 334-341 (`ContractEventIndexer.isRateLimited`). CALLERS: `poll` (catch at 199), `processBlock` (catch at 222) and `processTransaction` (catch at 325) call it and fall to `handleError` when it answers false. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): a non-429 Error is handed to `handleError` and so to `options.onError`; a 429 backs off. Today (hostile value): `isRateLimited` throws inside the catch, `poll()` rejects and `onError` is not called. After: the value is "not rate limited", reaches `handleError`, and `onError` receives it (or an Error with the constant message when it is not an Error). Persisted state: none (`lastProcessedBlock` is advanced only on success, as before). **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value whose read throws, `poll()` resolves and `onError` is called instead of `poll()` rejecting; every readable value behaves exactly as before. TIER 2 (blockchain indexer polling, log/callback only, no money path).',
 cells_text="""- RED at the tip, GREEN after: `R1` (a revoked Proxy), `R2` (a Proxy whose get trap throws) and `R3` (an Error whose message getter throws) (3 cells). At the tip `isRateLimited` throws inside `poll()`'s catch, so `poll()` rejects and the first assertion fails; after the edit `poll()` resolves and `onError` is called.
- GREEN at the tip and after: 'control ks1972 C1' (an ordinary Error reaches `onError` as is) and 'C2' (a 429 Error backs off to 2000 ms and does not reach `onError`), both already true at the tip (2 cells).
- The Blockfrost stand-in throwing the value is a plain function, not `vi.fn()`, on purpose.
""",
 premises='- Premise: `event-indexer.ts` read whole (lines 1-356) with `git show` at `2935f7231097`; `isRateLimited` is at 334-341 and is called at 200, 223 and 326; `handleError` (343-355) is already guarded by merged PR 1992 (ea5134d6b).\n- Ticket KS-1972 (Backlog, 0 comments) read whole at source on 2026-11-09.',
 unmeasured='The `setInterval` path and a real Blockfrost client were not run; whether any real client emits such a value is not known (the ticket says the same). Sites 133 and 321 (`console.error(error.message)` default path) are NOT touched.',
 scope='Refs KS-1972; does NOT close the whole class, and adds one private method only because the builder refuses re-indented lines (the existing expression is unchanged). The `handleError` console fallback (`error.message`) is deliberately not touched.',
 started_ok='KS-1972_gate176_finding_G176-F3;_operator_107_screen;_status_not_read_by_operator;_open_PRs_(44_PRs_295_files_read_2026-11-09_by_op107,_planted_control_services/originate_in_16_entries)_checked;_live_lanes_beyond_PRs_not_checked',
)
brieflib.make(spec)
