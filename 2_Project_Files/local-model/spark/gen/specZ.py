# TEST-ONLY twin B for KS-1588 (error-path cell, gate mutant N8). Tier test_only via gen/mk_testonly.py.
import importlib.util, os
_s = importlib.util.spec_from_file_location('sy', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'specY.py')); _m = importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)
CELL='''
  // KS-1588 (gate mutant N8): no cell made the lookup throw, so the error path was never entered; an echo of the thrown message, the address or the row into the 500 body passed every cell.
  it('RED KS-1588 E1 - a lookup that throws answers the generic 500 body, with nothing of the thrown text, the address or the seeded row in it', async () => {
    const { query } = await import('../db');
    vi.mocked(query).mockImplementationOnce(async () => { throw new Error('boom-ks1588-db-down'); });
    const res = await fetch(`${base}/api/auth/wallet/status/${REGISTERED}`);
    const text = await res.text();
    expect(res.status).toBe(500);
    expect(text).not.toContain('boom-ks1588-db-down');
    expect(text).not.toContain(REGISTERED);
    expect(text).not.toContain(SEEDED.id);
    expect(JSON.parse(text)).toEqual({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
  });

  it('control KS-1588 E0 - after the one-shot throwing stub the lookup answers normally again', async () => {
    const r = await status(REGISTERED);
    expect(r.json).toEqual({ exists: true });
  });
'''
T=dict(_m.T)
T.update(dict(dir='ks_1588_p1_error', title='ks1009 wallet-status cells never enter the error path: add the 500-body cell (gate mutant N8, the error path echoing into the 500 body) (RUNG 3, TEST-ONLY: one in-place test hunk with a planted tamper; the product does not change)',
 intro=_m.T['intro'].replace('ks_1588_p1_error (the 500-body cell, mutant N8)', 'ks_1588_p1_header (the response-header cell, mutant N3)'),
 tamper_line=438, tamper_from="    next(error);", tamper_to="    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: String(error) } });",
 statement_ok="line 438 is the one statement inside the `catch (error)` block of the `/status/:walletAddress` handler (:437-439); the tamper answers the 500 itself and echoes the thrown error's text into the body instead of handing it to the shared error handler; `res` is in scope and the file still compiles",
 edit=(_m.ANCHOR, "    expect(await res.text()).toContain('exists');\n  });\n"+CELL+"});\n"),
 red=['RED KS-1588 E1 - a lookup that throws answers the generic 500 body, with nothing of the thrown text, the address or the seeded row in it'],
 what_wrong="The cells of `ks1009-wallet-status-reveals-only-existence.test.ts` never make the lookup throw, so the route's error path is never entered. The pull request 1538 gate's mutant N8 (the error path echoing a message or the address into the 500 body) therefore survived every cell. No such leak exists in the code today (the catch hands the error to the shared handler with `next(error)`); this is a guard gap. This task adds the error-path cell the ticket asks for: with the database call made to throw once (`vi.mocked(query).mockImplementationOnce`), the route answers 500 with the generic body `{ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } }`, carrying none of the thrown text, the address or the seeded id; plus a control that the next call answers normally.",
 where="- `routes/wallet.ts:438` - (correct, STAYS) `    next(error);` - the line the tamper corrupts in the checker's clone.\n- The test hunk is added at the END of the first `describe` block of the test file, directly after cell `C2`, before that describe's closing `});`.",
 cells="- RED under the tamper: `RED KS-1588 E1` fails at `expect(text).not.toContain('boom-ks1588-db-down')` (the tamper echoes the error text), an assertion red; its status check passes first.\n- GREEN at the untouched tip: the shared error handler answers the generic 500 body.\n- CONTROL `E0`: green on both trees.\n- Every existing cell stays green on both trees (none enters the error path).",
 unmeasured="- The drafter did NOT run vitest by hand: the RED-under-tamper / GREEN-at-tip result is the `round.sh --control` run on this golden.\n- The generic body is the gate's measurement (ticket text); the control run measures it at the tip against the real `errorHandler`.\n- Open PRs touching this test file: none by the file lists of every open PR read on 2026-10-28.",
 scope="**Closes the error-path half of KS-1588 (mutant N8) only.** The header half (mutant N3) is the twin brief `ks_1588_p1_header`. Link the PR as Refs KS-1588, never a close-word.",
))
