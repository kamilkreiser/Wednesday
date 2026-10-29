# KS-1816-1 (gate 20 finding 1816-1, Spark operator 14, 2026-10-30): R6 pins the fallback TEXT, not the TYPE for a message-less thrown value (mutants Y7, Y10). test_only, gen/mk_testonly.py.
PROD = 'Blockchain/Dev/services/originate/src/routes/adminConfig.ts'
TEST = 'Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts'
ANCHOR = "  });\n\n  it('control KS-1802 C1: an ordinary Error on every insert"
CELL = '''  // KS-1816-1 (gate 20 mutants Y7 and Y10): R6 pins the fallback TEXT for a hostile value, but nothing pinned the TYPE of what is logged for a thrown value that is readable and has no `message` (a plain string, a number).
  // readableErrorMessage returns `err?.message`, which is undefined for those, so `error` is undefined; `String(err?.message)` logs the text "undefined" and a fallback to `String(err)` logs the value itself.
  it('RED KS-1816-1 R7: every insert rejecting with a plain string or a number logs error undefined, once per user, not a coerced string', async () => {
    for (const bare of ['ks1816 plain string', 42]) {
      mockLogError.mockReset();
      mockExecuteRaw.mockReset();
      mockExecuteRaw.mockRejectedValue(bare);
      expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: 0, created: 0, alreadyPresent: 0, failed: USERS } });
      const logged = mockLogError.mock.calls.filter((call) => call[0] === 'Demo user seed failed');
      expect(logged).toHaveLength(USERS);
      expect(logged[0][1]).toStrictEqual({ email: 'james.wilson@ox.ac.uk', error: undefined });
      expect(logged.map((call) => (call[1] as { error: unknown }).error)).toEqual(Array(USERS).fill(undefined));
    }
  });

'''
FROM = "    return err?.message;"
TO = "    return String(err?.message);"
T = dict(dir='ks_1816_p1_message_less',
 ticket='KS-1817',
 title="originate ks1802 seed-demo-users cells pin the fallback TEXT but not what is logged for a message-less thrown value: `String(err?.message)` logs the text \"undefined\" unnoticed (gate 20 finding 1816-1, mutants Y7 and Y10): add one cell whose insert rejects with a plain string (RUNG 3, TEST-ONLY: one in-place test hunk with a planted tamper; the product does not change)",
 intro="DRAFT by Spark operator 14 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / originate) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: QA gate 20 (`0_Brain/reference/2026-10-30_gate20-1815-1816/verdict.md`), minor 1816-1: after #1816 (KS-1817's R6 and KS-1818's guard) the fallback text is pinned, but a mutant making `readableErrorMessage` return `String(err?.message)` (Y7) or fall back to `String(err)` for a message-less value (Y10) leaves the 9 cells of the KS-1802 file green. This is the same gap as the earlier brief ks_1817_p1b_no_message (written at tip 5a5c4d2b and HELD by Wednesday because it pins the current weaker behaviour: a plain string logs `error: undefined`, so a later change that logs the string would turn the cell red). It is re-based on #1816, which already uses the names R4 and R5, and named R7 here. Link the PR as Refs KS-1817 and KS-1802, never a close-word.",
 product=PROD, test=TEST, ref='Blockchain/Dev/services/originate/src/__tests__/ks1114-title-lookup-hidden-statuses-case-and-space.test.ts',
 tamper_line=152, tamper_from=FROM, tamper_to=TO,
 statement_ok="line 152 is the one `return err?.message;` statement inside the `try` of `readableErrorMessage`; the tamper wraps it in `String(...)` (mutant Y7) and the function still returns `string | undefined`, so the file compiles; the revoked-Proxy and throwing-getter paths still reach the catch and the fixed fallback text",
 edit=(ANCHOR, "  });\n\n" + CELL + "  it('control KS-1802 C1: an ordinary Error on every insert"),
 nh_txt='1 hunk, the new cell added after cell R6 of the one describe',
 red=['RED KS-1816-1 R7: every insert rejecting with a plain string or a number logs error undefined, once per user, not a coerced string'],
 runner='jest` (`npx jest src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts` from `Blockchain/Dev/services/originate',
 rung='3 (test-only mode: a planted tamper must redden the new cell; the hunk is given byte-exact)',
 what_wrong="`readableErrorMessage` (`routes/adminConfig.ts:150-156`) is `try { return err?.message; } catch { return 'thrown value that could not be described'; }`. A thrown plain string or number is readable and has no `message`, so `err?.message` is `undefined` and the per-user catch logs `{ email, error: undefined }`. Nothing in `ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts` asserts what is logged for such a value (R6 covers only the fixed fallback TEXT for a revoked Proxy and a throwing getter), so `return String(err?.message);` (the text \"undefined\", mutant Y7) and `return err?.message ?? String(err);` (the value as text, mutant Y10) both stay green. The product is right today; the gap is a missing pin. Add cell R7: for a plain string and for a number, every insert rejects with it, the route still reports 14 failed, and the 14 `'Demo user seed failed'` log calls each carry exactly `{ email, error: undefined }` (strict equality, so a coerced string is red).",
 where="- `src/routes/adminConfig.ts:152` - (correct, STAYS) `    return err?.message;` - the line the tamper corrupts in the checker's clone.\n- Test file: cell R6 is :132-143 (its closing `  });` is :143); :144 is blank; :145 starts `control KS-1802 C1`. **The new cell goes between :144 and :145** (a blank line after it, before C1). `seed`, `USERS`, `mockLogError` and `mockExecuteRaw` are in scope at module level; `beforeEach` resets the mocks and the cell resets them itself per value, as R6 does.",
 cells="- RED under the tamper: `RED KS-1816-1 R7: every insert rejecting with a plain string or a number logs error undefined, ...` fails by assertion (the tamper logs the text \"undefined\", `toStrictEqual` and the array equality see a string).\n- GREEN at the untouched tip: R7 (the helper returns `err?.message`, which is undefined for a string and a number) and every other cell.\n- CONTROL: the existing `control KS-1802 C1` (an ordinary Error logs its message through the same log filter) stays green under the tamper, which shows the tamper changes only the message-less path.\n- Every existing cell stays green on both trees.",
 unmeasured="- The drafter did NOT run jest through the round machinery: the RED-under-tamper / GREEN-at-tip result is the `round.sh --control` run on this golden.\n- Mutant Y10 is a different edit from the planted tamper (Y7); the operator measures Y10 against the cell separately and reports it.\n- Whether `{ email, error: undefined }` under `toStrictEqual` also holds when the logger mock is given the object by reference: it does at the tip by the helper's code, and the control run is the measurement.\n- This pins the current `undefined`; if the behaviour is ever changed on purpose to log the string, this cell must change with it (the reason ks_1817_p1b was held).\n- Open PRs touching either file: see the overlap count in the operator report.",
 scope="**Closes finding 1816-1 (minor), test half.** Link the PR as Refs KS-1817 / KS-1802. No product file changes. Not in scope: changing what `readableErrorMessage` returns for a message-less value.",
)
