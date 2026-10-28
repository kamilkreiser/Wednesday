# TEST-ONLY twin A for KS-1588 (header cell, gate mutant N3). Tier test_only via gen/mk_testonly.py.
PROD='Blockchain/Dev/services/auth/src/routes/wallet.ts'
TEST='Blockchain/Dev/services/auth/src/__tests__/ks1009-wallet-status-reveals-only-existence.test.ts'
ANCHOR="    expect(await res.text()).toContain('exists');\n  });\n});\n"
CELL='''
  // KS-1588 (gate mutant N3): every cell above reads only the response BODY, so an id sent in a response HEADER with the body untouched passed them all.
  // Every header of a registered wallet's answer must be one of Express's defaults, and none may carry the seeded id, role or date.
  it('RED KS-1588 H1 - a REGISTERED wallet answers with only Express default headers, none carrying the seeded id, role or timestamp', async () => {
    const res = await fetch(`${base}/api/auth/wallet/status/${REGISTERED}`);
    const allowed = ['connection', 'content-length', 'content-type', 'date', 'etag', 'keep-alive', 'x-powered-by'];
    const names = [...res.headers.keys()];
    expect(names.filter((n) => !allowed.includes(n))).toEqual([]);
    const values = [...res.headers.values()].join('\\n');
    expect(values).not.toContain(SEEDED.id);
    expect(values).not.toContain(SEEDED.role);
    expect(values).not.toContain('2026-01-02');
  });

  it('control KS-1588 H0 - the same reader sees the response headers it is checking (content-type is among them)', async () => {
    const res = await fetch(`${base}/api/auth/wallet/status/${REGISTERED}`);
    expect([...res.headers.keys()]).toContain('content-type');
  });
'''
T=dict(dir='ks_1588_p1_header',ticket='KS-1588',
 title='ks1009 wallet-status cells pin the response BODY only: add the header cell (gate mutant N3, an id in a response header) (RUNG 3, TEST-ONLY: one in-place test hunk with a planted tamper; the product does not change)',
 intro="DRAFT by a Spark brief drafter for Wednesday, batch 5 of 2026-10-28 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge (auth service, public route). TWIN WARNING: ks_1588_p1_error (the 500-body cell, mutant N8) edits the SAME test file at the same place; raise the two together as one change, or one after the other.",
 product=PROD, test=TEST, ref='Blockchain/Dev/services/auth/src/__tests__/ks942-public-wallet-routes-stay-open.test.ts',
 tamper_line=436, tamper_from="    res.json({ exists: true });", tamper_to="    res.setHeader('x-user-id', String(result.rows[0].id)); res.json({ exists: true });",
 statement_ok="line 436 is one complete statement inside the `try` block of the `/status/:walletAddress` handler, after the `rows.length === 0` early return, so `result.rows[0].id` exists; the tamper adds a second statement on the same line (an `X-User-Id` response header carrying the id) and leaves the body `{ exists: true }`; the file still compiles",
 edit=(ANCHOR, "    expect(await res.text()).toContain('exists');\n  });\n"+CELL+"});\n"),
 red=['RED KS-1588 H1 - a REGISTERED wallet answers with only Express default headers, none carrying the seeded id, role or timestamp'],
 runner='vitest` (`npx vitest run src/__tests__/ks1009-wallet-status-reveals-only-existence.test.ts` from `Blockchain/Dev/services/auth',
 rung='3 (test-only mode: a planted tamper must be reddened by the cell; the cell is given byte-exact)',
 what_wrong="The cells of `ks1009-wallet-status-reveals-only-existence.test.ts` pin `GET /api/auth/wallet/status/:walletAddress` to `{ exists }` by reading the response BODY (cells 1 and 2) and nothing else. The pull request 1538 gate's mutant N3 (the user id returned in an `X-User-Id` response header, body unchanged) therefore survived every cell. No such leak exists in the code today; this is a guard gap. This task adds the header cell the ticket asks for: a registered wallet's answer carries only Express's default headers (`connection`, `content-length`, `content-type`, `date`, `etag`, `keep-alive`, `x-powered-by`) and no header value contains the seeded id, role or date; plus a control that the reader sees headers at all.",
 where="- `routes/wallet.ts:436` - (correct, STAYS) `    res.json({ exists: true });` - the line the tamper corrupts in the checker's clone.\n- The test hunk is added at the END of the first `describe` block of the test file, directly after cell `C2` (whose last assertion is `expect(await res.text()).toContain('exists');`), before that describe's closing `});`.",
 cells="- RED under the tamper: `RED KS-1588 H1` fails at the first `expect` (the header list contains `x-user-id`), an assertion red.\n- GREEN at the untouched tip: the headers are the Express defaults and none carries a seeded value.\n- CONTROL `H0`: green on both trees (content-type is present).\n- Every existing cell stays green on both trees (the tamper changes only a header).",
 unmeasured="- The drafter did NOT run vitest by hand: the RED-under-tamper / GREEN-at-tip result is the `round.sh --control` run on this golden.\n- The exact set of default Express headers is the gate's measurement (ticket text), not re-measured here; the control run measures it at the tip.\n- Open PRs touching this test file: none by the file lists of every open PR read on 2026-10-28.",
 scope="**Closes the header half of KS-1588 (mutant N3) only.** The error-path half (mutant N8) is the twin brief `ks_1588_p1_error`. Link the PR as Refs KS-1588, never a close-word.",
)
