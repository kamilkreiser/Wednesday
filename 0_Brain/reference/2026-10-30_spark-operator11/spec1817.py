# KS-1817 (gate 17 survivors X3 and X5, Spark operator 11, 2026-10-30): the readableErrorMessage fallback is unpinned. test_only, gen/mk_testonly.py. Two twins: p1 = X3 (fallback text), p1b = X5 (no message logs as undefined).
PROD='Blockchain/Dev/services/originate/src/routes/adminConfig.ts'
TEST='Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts'
ANCHOR="    expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: 13, created: 13, alreadyPresent: 0, failed: 1 } });\n  });\n"
FALLBACK_CELL = r'''
  // KS-1817 (gate 17 mutant X3): R1-R3 pin the HTTP report and the counts for a hostile thrown value, but nothing pinned what is LOGGED for it, so the fixed fallback of readableErrorMessage could be
  // changed or dropped (the catch returning undefined) and every cell stayed green. The fallback text is also the one fail500 and migrate-tenant-data use.
  it('RED KS-1817 R4: every insert rejecting with a revoked Proxy or a throwing message getter logs the fixed fallback text, once per user', async () => {
    for (const hostile of [revokedProxy(), throwingMessageGetter()]) {
      mockLogError.mockReset();
      mockExecuteRaw.mockReset();
      mockExecuteRaw.mockRejectedValue(hostile);
      await seed();
      const logged = mockLogError.mock.calls.filter((call) => call[0] === 'Demo user seed failed');
      expect(logged).toHaveLength(USERS);
      expect(logged[0][1]).toEqual({ email: 'james.wilson@ox.ac.uk', error: 'thrown value that could not be described' });
      expect(logged.map((call) => (call[1] as { error: unknown }).error)).toEqual(Array(USERS).fill('thrown value that could not be described'));
    }
  });
'''
NOMSG_CELL = r'''
  // KS-1817 (gate 17 mutant X5): nothing pinned what is logged for a thrown value that has no message (a plain string), so `String(err?.message)` (which logs the literal text 'undefined') passed every cell.
  it('RED KS-1817 R5: every insert rejecting with a plain string (no message) logs error undefined, not the text "undefined" and not the fallback', async () => {
    mockExecuteRaw.mockRejectedValue('ks1817 plain string');
    expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: 0, created: 0, alreadyPresent: 0, failed: USERS } });
    const logged = mockLogError.mock.calls.filter((call) => call[0] === 'Demo user seed failed');
    expect(logged).toHaveLength(USERS);
    expect(logged.map((call) => (call[1] as { error: unknown }).error)).toEqual(Array(USERS).fill(undefined));
  });

  it('control KS-1817 C4: an ordinary Error still logs its message (the plain-string cell reads the same log calls)', async () => {
    mockExecuteRaw.mockRejectedValue(new Error('ks1817 ordinary'));
    await seed();
    const logged = mockLogError.mock.calls.filter((call) => call[0] === 'Demo user seed failed');
    expect(logged.map((call) => (call[1] as { error: unknown }).error)).toEqual(Array(USERS).fill('ks1817 ordinary'));
  });
'''
COMMON=dict(ticket='KS-1817', product=PROD, test=TEST, ref='Blockchain/Dev/services/originate/src/__tests__/ks1114-title-lookup-hidden-statuses-case-and-space.test.ts',
 runner='jest` (`npx jest src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts` from `Blockchain/Dev/services/originate',
 rung='3 (test-only mode: a planted tamper must redden the new cell; the hunk is given byte-exact)',
 intro="DRAFT by Spark operator 11 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / originate) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: QA gate 17 (`0_Brain/reference/2026-10-29_gate17-1808-1809/verdict.md`), minor 1809-1, filed as KS-1817: mutants X3 (the catch of `readableErrorMessage` returns undefined) and X5 (`String(err?.message)`) both leave the 6 cells of the KS-1802 test file green. The test_only tier plants ONE tamper, so the two mutants are two TWIN briefs (ks_1817_p1 = X3, ks_1817_p1b = X5) that edit the SAME test file at the SAME place: raise them together as one change (apply one, then the other with its context re-read), never as two competing PRs. Link the PR as Refs KS-1817 and KS-1802, never a close-word.",
 nh_txt="1 hunk, the new cell(s) added after cell R3 of the one describe",
 unmeasured="- The drafter did NOT run jest by hand: the RED-under-tamper / GREEN-at-tip result is the `round.sh --control` run on this golden.\n- The cell pins the TEXT the helper returns, which the ticket and gate 17 ask for; it does not pin the logger call that sits outside the helper's guard (that is KS-1818, a separate decision).\n- The logged email `james.wilson@ox.ac.uk` is read from the existing control C1 of the same file (the first seeded user); the count `USERS` (14) is the file's own constant.\n- Open PRs touching either file: see the overlap count in the operator report (checked against every open PR on 2026-10-30).",
)
T=dict(COMMON, dir='ks_1817_p1_fallback_text',
 title='ks1802 seed-demo-users cells never assert what is logged for an unreadable thrown value, so the readableErrorMessage fallback can be changed or dropped (gate 17 mutant X3): add a log-text cell (RUNG 3, TEST-ONLY: one in-place test hunk with a planted tamper; the product does not change)',
 tamper_line=154, tamper_from="    return 'thrown value that could not be described';", tamper_to="    return undefined;",
 statement_ok="line 154 is the single `return` statement of the `catch` block of `readableErrorMessage` (:150-:156, return type `string | undefined`, so `return undefined;` still compiles); the tamper is gate 17's mutant X3 (the catch returns undefined). The same text also appears at :118 and :2283 (other sites) and those are NOT touched",
 edit=(ANCHOR, ANCHOR+FALLBACK_CELL),
 red=['RED KS-1817 R4'],
 what_wrong="`readableErrorMessage` (`routes/adminConfig.ts:150-156`) returns `err?.message` and, when reading it throws, the fixed text `thrown value that could not be described`; the call site is `:2121` (`logger.error('Demo user seed failed', { email: u.email, error: readableErrorMessage(err) })`). The six cells of `ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts` assert the HTTP report and the counts for a hostile thrown value (R1-R3) and the logged message for an ordinary Error (C1), but none asserts what is logged for a hostile value, so the fallback can be changed or dropped (mutant X3: the catch returns undefined) and every cell stays green. The product is right today; the gap is a missing pin. This task adds ONE cell, R4, that drives both hostile kinds (a revoked Proxy and a throwing `message` getter) and asserts the 14 `Demo user seed failed` log calls each carry the fallback text.",
 where="- `src/routes/adminConfig.ts:154` - (correct, STAYS) `    return 'thrown value that could not be described';` - the line the tamper corrupts in the checker's clone.\n- Test file: cell R3 is lines 107-110 (its closing `  });` is :110); :111 is blank; :112 starts `control KS-1802 C1`. **The new cell goes between :110 and :111.** `revokedProxy`, `throwingMessageGetter`, `seed`, `USERS`, `mockLogError` and `mockExecuteRaw` are in scope at module level.",
 cells="- RED under the tamper: `RED KS-1817 R4` fails by assertion (the logged `error` is undefined, expected the fallback text). R1-R3 and the controls stay green under the tamper (that is the survivor).\n- GREEN at the untouched tip: R4 (14 log calls per hostile kind, each with the fallback text).\n- Every existing cell stays green on both trees.",
 scope="**Closes the X3 half of KS-1817 only** (the fallback text); the X5 half is the twin `ks_1817_p1b_no_message`. Link the PR as Refs KS-1817 / KS-1802. No product file changes.",
)
T2=dict(COMMON, dir='ks_1817_p1b_no_message',
 title='ks1802 seed-demo-users cells never assert what is logged for a thrown value with no message, so String(err?.message) logs the text "undefined" unnoticed (gate 17 mutant X5): add a no-message log cell (RUNG 3, TEST-ONLY: one in-place test hunk with a planted tamper; the product does not change)',
 tamper_line=152, tamper_from="    return err?.message;", tamper_to="    return String(err?.message);",
 statement_ok="line 152 is the single `return` statement of the `try` block of `readableErrorMessage` (:150-:156, return type `string | undefined`; `String(...)` is a string so it still compiles); the tamper is gate 17's mutant X5 (a non-string message coerced with String()). A revoked Proxy still throws inside the try, so the fallback path is unchanged",
 edit=(ANCHOR, ANCHOR+NOMSG_CELL),
 red=['RED KS-1817 R5'],
 what_wrong="`readableErrorMessage` (`routes/adminConfig.ts:150-156`) returns `err?.message` as it is: a thrown plain string has no `message`, so the logged `error` is `undefined`. Nothing in `ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts` asserts what is logged for such a value, so mutant X5 (`return String(err?.message);`, which logs the literal text 'undefined' for a message-less value) passes all 6 cells. The product is right today; the gap is a missing pin. This task adds cell R5 (a plain string rejection: the 14 log calls each carry `error: undefined`) and a control C4 (an ordinary Error logs its message, read through the same filter).",
 where="- `src/routes/adminConfig.ts:152` - (correct, STAYS) `    return err?.message;` - the line the tamper corrupts in the checker's clone.\n- Test file: cell R3 is lines 107-110 (its closing `  });` is :110); :111 is blank; :112 starts `control KS-1802 C1`. **The new cells go between :110 and :111.** `seed`, `USERS`, `mockLogError` and `mockExecuteRaw` are in scope at module level.",
 cells="- RED under the tamper: `RED KS-1817 R5` fails by assertion (the logged `error` is the text 'undefined', expected the value undefined). The control C4 stays green under the tamper (an Error's message is already a string).\n- GREEN at the untouched tip: R5 and C4.\n- Every existing cell stays green on both trees.",
 scope="**Closes the X5 half of KS-1817 only**; the X3 half (the fallback text) is the twin `ks_1817_p1_fallback_text`. Link the PR as Refs KS-1817 / KS-1802. No product file changes.",
)
