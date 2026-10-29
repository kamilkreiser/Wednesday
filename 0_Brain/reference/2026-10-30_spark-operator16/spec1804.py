# KS-1804 note 2 (KS-1188 F3 gate note carried on KS-1467): no cell pins that the backup-code burn runs exactly once. Spark operator 16. test_only, gen/mk_testonly.py.
PROD = 'Blockchain/Dev/services/auth/src/services/passwordLoginGate.ts'
TEST = 'Blockchain/Dev/services/auth/src/__tests__/ks1188-f3-a-spent-backup-code-503-says-so.test.ts'
OLD = "    expect(state.recordSuccess).toBe(1);\n  });\n});\n"
CELLS = '''
  // KS-1804 note 2 (KS-1188 F3 gate note carried on KS-1467): the two cells that look at `state.queries` only ask whether SOME `UPDATE users` ran (or none). Nothing counted them, so a burn that runs twice stayed green.
  const burns = () => state.queries.filter((q) => /^\\s*UPDATE\\s+users/i.test(q.sql));

  it('RED KS-1804 N2 a healthy backup-code sign-in burns the code with exactly one UPDATE users', async () => {
    await expect(assertAccountMayReceiveCredential(mfaUser(), input(BACKUP_CODE))).resolves.toEqual({ ok: true });
    expect(burns()).toHaveLength(1);
  });

  it('RED KS-1804 N2 the faulted case (the read-back fails after the burn landed) still issued exactly one UPDATE users', async () => {
    state.readBackFails = CONNECTION_LOST;
    await rejection(BACKUP_CODE);
    expect(burns()).toHaveLength(1);
  });
'''
NEW = OLD[:-len("});\n")] + CELLS + "});\n"
FROM = "          await userRepo.updateUserOrThrow("
TO = "          await userRepo.updateUserOrThrow(user.id, { mfaBackupCodes: user.mfaBackupCodes }, 'tamper').catch(() => undefined); await userRepo.updateUserOrThrow("
T = dict(dir='ks_1804_p1_burn_exactly_once',
 ticket='KS-1804',
 title="auth KS-1188 F3 test: no cell counts the backup-code burn's UPDATE statements, so a burn that runs twice stays green (KS-1804 note 2): add two cells asserting exactly one `UPDATE users` in the healthy and the faulted case (RUNG 3, TEST-ONLY: one in-place test hunk with a planted tamper; the product does not change)",
 intro="DRAFT by Spark operator 16 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / auth) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. **The tamper target `services/passwordLoginGate.ts` is a CREDENTIAL file: routing row 4 applies (the Spark takes a fully spelled-out edit inside an auth file) and this PR then needs a TIER-1 gate.** The PR itself touches only the test file. Origin: KS-1804 note 2 (PR 1479 / KS-1188 F3 gate note, carried on KS-1467). Note 1 (move a const below the imports) is NOT in this brief: it edits the credential file itself. The product is right today (one `updateUserOrThrow` call per burn). The gap is a missing pin. Link the PR as Refs KS-1804, never a close-word.",
 product=PROD, test=TEST, ref='Blockchain/Dev/services/auth/src/__tests__/ks1052-backup-code-burn-cause-a.test.ts',
 tamper_line=281, tamper_from=FROM, tamper_to=TO,
 statement_ok="line 281 is the opening `await userRepo.updateUserOrThrow(` of the one burn statement inside the `try` (lines 281-285); the tamper prepends an identical burn call whose rejection is swallowed with `.catch(() => undefined)`, then runs the original call, so the file compiles and every outcome (200 path, the 503 reword) is unchanged while the number of `UPDATE users` statements doubles in the healthy and in the faulted case",
 edit=(OLD, NEW),
 nh_txt='1 hunk, two new cells and a small helper added at the end of the one describe',
 red=['RED KS-1804 N2 a healthy backup-code sign-in burns the code with exactly one UPDATE users', 'RED KS-1804 N2 the faulted case (the read-back fails after the burn landed) still issued exactly one UPDATE users'],
 runner='vitest` (`npx vitest run src/__tests__/ks1188-f3-a-spent-backup-code-503-says-so.test.ts` from `Blockchain/Dev/services/auth',
 rung='3 (test-only mode: a planted tamper must redden the new cells; the hunk is given byte-exact)',
 what_wrong="`ks1188-f3-a-spent-backup-code-503-says-so.test.ts` records every SQL statement the db stub sees in `state.queries`, but its only two assertions on it are `some UPDATE users ran` (line 132) and `no UPDATE users ran` (line 152). Nothing counts the statements, so a change that burns the backup code twice (a retry, a duplicated call) leaves all six cells green. KS-1804 note 2 asks for one cell asserting exactly one `UPDATE users`. Add two: the healthy sign-in, and the faulted case (the read-back fails after the burn landed, the gate's measured case).",
 where="- `services/passwordLoginGate.ts:281` - (correct, STAYS) `await userRepo.updateUserOrThrow(`; the line the tamper replaces in the checker's clone.\n- Test file: the last cell (`CONTROL ... records success once`) ends at :158 and `});` at :159 closes the describe. **The new block goes between :158 and :159**, after one blank line. `state`, `assertAccountMayReceiveCredential`, `mfaUser`, `input`, `rejection`, `BACKUP_CODE` and `CONNECTION_LOST` are in scope at module level.",
 cells="- RED under the tamper: both `RED KS-1804 N2 ...` cells fail by assertion (two `UPDATE users` statements instead of one).\n- GREEN at the untouched tip: both new cells and the six existing ones.\n- The tamper keeps every existing cell green (the first burn's error is swallowed, the second behaves as the original), so the two new cells are the only reds.",
 unmeasured="- The drafter did NOT run vitest through the round machinery for the brief; the RED-under-tamper / GREEN-at-tip result is the `round.sh --control` run on this golden.\n- Whether another backup-code test file (for example ks1052-backup-code-burn-cause-a) already pins the count (the ticket says it is 'probably not done, not proven').\n- Note 1 of the ticket (the const among the imports) is untouched.\n- Open PRs touching either file: see the overlap count in the operator report.",
 scope="**KS-1804 note 2 only.** Link the PR as Refs KS-1804, never a close-word. No product file changes. Tier-1 gate on the PR because the file the cells guard is a credential gate.",
)
