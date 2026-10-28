# op6 task 2 (KS-1039): replace the echo assertion at auth-exhaustive.spec.ts 2.4.6 with a stored-value assertion. Tier test_only via gen/mk_testonly.py.
PROD='Blockchain/Dev/services/auth/src/routes/auth.ts'
TEST='Blockchain/Dev/tests/e2e/tests/auth-exhaustive.spec.ts'
OLD="    expect(body.toLowerCase()).not.toContain('drop table');\n    expect(status).toBeLessThan(500);\n"
NEW='''    // KS-1039: 'drop table' is the INPUT, and a register that stores and returns a display name returns it verbatim, so asserting it is absent from
    // the body fails on the echo and says nothing about injection. Parameterised SQL means the string is stored as data: the user object the
    // response carries must hold the exact input, and the call must have succeeded (a rejected call would otherwise skip this check).
    expect(status).toBe(201);
    expect(JSON.parse(body).data.user.displayName).toBe("Robert'); DROP TABLE users; --");
    expect(status).toBeLessThan(500);
'''
T=dict(dir='ks_1039_p1_stored_value',ticket='KS-1039',
 title="auth-exhaustive.spec.ts 2.4.6: the assertion `not.toContain('drop table')` fails on an echo of the INPUT; assert the stored displayName equals the input instead (RUNG 3, TEST-ONLY Playwright: one in-place hunk, planted tamper in the register route)",
 intro="DRAFT by a Spark operator (op6) for Wednesday, 2026-10-28 AEDT (never-keep-the-Spark-idle). Secuura only. A local PASS is a candidate, never a merge. The ticket offers two fixes (status < 500 plus no SQL error, both ALREADY asserted two lines above, so that choice is a plain deletion that asserts nothing new; or assert the stored value equals the exact input); this brief takes the stored-value one because it cannot pass vacuously.",
 product=PROD, test=TEST, ref='Blockchain/Dev/services/auth/src/__tests__/ks942-public-wallet-routes-stay-open.test.ts',
 tamper_line=315, tamper_from="        displayName: user.displayName,", tamper_to="        displayName: user.displayName ? user.displayName.replace(/[;']/g, '') : user.displayName,",
 statement_ok="line 315 is one property of the `user:` object literal in the register response; the tamper keeps it a single property whose value strips `;` and `'` from the stored name, so the register answer no longer carries the exact input; the file still compiles",
 edit=(OLD,NEW),
 nh_txt='1 hunk, one line replaced by five', nh_word='ONE hunk', nh_head='ONE EDIT in the TEST file (one hunk)',
 red=["2.4.6: SQL injection in registration name is sanitized"],
 runner='playwright` (`npx playwright test auth-exhaustive.spec.ts -g 2.4.6` from `Blockchain/Dev/tests/e2e` against a running stack',
 rung='3 (test-only mode: one line replaced with five, byte-exact)',
 what_wrong="Test `2.4.6` registers with `name = \"Robert'); DROP TABLE users; --\"` and then asserts the lower-cased response body does NOT contain `drop table`. The register route stores `displayName` and returns it in `data.user.displayName`, so the body carries the input verbatim and the assertion is red on every healthy run (measured 5 of 5, KS-1039). It fails on an echo, not on an injection. The sibling assertions (no `sql`, no `syntax error`, `status < 500`) already pass and stay. Replace the one `drop table` line with an assertion of what is meant: the call answered `201` and the stored display name equals the exact input.",
 where="- `Blockchain/Dev/tests/e2e/tests/auth-exhaustive.spec.ts:751` - **must change**: `    expect(body.toLowerCase()).not.toContain('drop table');` is replaced by the comment and two assertions given below; the line after it, `    expect(status).toBeLessThan(500);`, STAYS.\n- `:747` and `:748` (`not.toContain('sql')`, `not.toContain('syntax error')`) - (correct, STAYS).\n- `Blockchain/Dev/services/auth/src/routes/auth.ts:315` - the product-side line the checker tampers; not modified by you.",
 cells="- RED under the tamper: the stored-value assertion fails (the answer's `displayName` no longer equals the input).\n- GREEN at the untouched tip: status 201 and the exact input comes back.\n- NOTE: this is a Playwright test that needs a running stack; whether the checker can run it is not known to the drafter.",
 unmeasured="- Not run by the drafter (no stack here): the 201 and the verbatim `data.user.displayName` are from the ticket's measurement (KS-1039, re-confirmed 2026-09-09) and from reading `routes/auth.ts:220-321` at the tip.\n- Whether `expect(status).toBe(201)` is too strict for an environment whose rate limit answers 429: the ticket measured 201 five of five; not measured elsewhere.\n- The output-escaping question (frontend renderers) is separate and not addressed.",
 scope="**KS-1039 only, the one assertion line.** Refs KS-1039, never a close-word.",
)
