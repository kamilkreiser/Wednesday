# Gate 195 commission — Secuura / Blockchain, PR 2006 (KS-1990: POST /api/admin/seed-demo-users answered 200 success true when every insert failed), TIER 2, ROUND 1 of 2

Written by Wednesday 2026-11-05 ~11:4x AEDT. Model: Sonnet (routing v1.0 row G2).
**TIER 2, reason:** the change alters only the RESPONSE (HTTP status and the `success` flag) of an admin-only route, plus moved test cells. The demo-seed gate, the authorisation check and the INSERT are unchanged by design. **Your first job is to PROVE that.** If any of the three changed, stop and write `NO GO (TIER WRONG: <what changed>)`: Wednesday re-gates at tier 1.
**Round count:** round 1 of 2.
**A rotation KILLS it:** you run as a subagent of Wednesday's seat. Write `verdict.md` EARLY as a stub (line 1 `NO GO (INCOMPLETE: killed before the verdict)`), then overwrite it at the end.

## What was ruled, so what this PR must be
Wednesday ruled this contract in her ANSWER to Seat W 28th, 23:49:40Z 2026-11-04 (Kam's 2026-10-27 design grant). The PR body should state it; check it.
1. `success = (failed === 0)` in every case.
2. `created === 0 AND failed > 0` gives HTTP **500** with the SAME report body fields as before: `success`, `seededUsers`, `created`, `alreadyPresent`, `failed`. No new field, no new message text.
3. Partial (`created > 0 AND failed > 0`) gives 200 with `success: false` and the counts unchanged.
4. Healthy, and alreadyPresent-only, give 200 with `success: true`, unchanged from base.
5. The org-link `catch { /* skip */ }` (~adminConfig.ts:2145) is OUT of scope and must be untouched.
6. The INSERT (`ON CONFLICT (email)`, ~:2111) is untouched. Its 42P10 cause is recorded on KS-960, not fixed here.
7. Six existing cells in `Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts` (R1, R2, R3, R4, R5, C1) were moved IN PLACE to the new contract by Wednesday's ruling. C2, C3 and R6 must be byte-equal to base, and no other line in that file changes.

- **Commit `6311c141f99e5ade8d94e60ee15b0c80006a52cd`** = refs/pull/2006/head; **base/develop `07a2d62be6a09c9cd504864d1cf1906543d55317`** (both from Wednesday's own git ls-remote 11:4x AEDT 2026-11-05). One commit, 5 files, by Seat W 28th (Sonnet).
- **The seat's figures, to RE-MEASURE, not trust:** red at base 12 of 20 by assertion; direction 14 scenarios, 0 more permissive; mutants 8 of 8; originate 2,496 of 2,496 (base 2,485); leak 0 with a control. Full READY: `ready_2006.txt` in this folder.

## Questions (measure; do not take the READY's word)
1. **Scope.** `git diff --name-only 07a2d62be6a0...6311c141f99e` must be exactly the five paths the READY names (adminConfig.ts, the ks1802 test, the new ks1990 test, the two docs fragments). Read the adminConfig.ts hunk whole. **Prove** that the demo-seed gate call (demoSeedGate), the authorisation middleware on the route, the users array and the INSERT statement are byte-equal base vs head. Show the lines, with sha.
2. **ks1802 in-place edit.** Show a hunk count; show that only R1/R2/R3/R4/R5/C1 changed; show C2/C3/R6 byte-equal, with a control that reads unequal on an edited cell.
3. **Contract table, base vs head, real router.** Use the KS-1802 harness shape: a real express router with the real handler, only the DB faked. Cells:
   - all 14 inserts fail;
   - all succeed;
   - all already present;
   - partial 13/1;
   - partial 1/13;
   - gate closed (each flag false in turn);
   - non-admin;
   - no token (if reachable in the harness);
   - a throw outside the loop (the outer catch at ~2156).
   For each: status, `success`, the counts. Predicate: **head never MORE permissive than base**: no 2xx or `success: true` at head where base had a non-2xx or false. Report "N of M" and every changed cell.
4. **Leak check.** Plant a distinctive token in the thrown DB error's message, detail, hint and where, plus a SQLSTATE, a table name, a seed e-mail and a file path. Search the WHOLE serialized body and ALL headers at head on the 500 and partial cells. Expect 0 hits. Include a positive control in the same run that CAN fail (the token in the captured log; a mutant returning the raw error).
5. **Mutants.** Reproduce at least 4 of the seat's 8 from its table, plus one of your own on the 500 boundary (`created === 0` vs `created <= 0` or similar). Each anchor count must be 1, the mutant must parse, and the restore must be sha-equal. Count the RAW table yourself.
6. **Consumers.** `git grep -n 'seed-demo-users'` across the whole tree at head, with a positive control. Name every reader of the response. Confirm the seat's claim that the only one is systemTest/schemathesis `tests/support/demo_seed_gate.py` (`parse_seed_counts`, `rerun_overwrote_nothing`), and that the PR body names its availability cost.
7. **Merge tree.** In YOUR clone, `git merge-tree --write-tree 07a2d62be6a09c9cd504864d1cf1906543d55317 6311c141f99e5ade8d94e60ee15b0c80006a52cd`. Report rc and the tree id; expect rc 0 and a tree equal to the head tree (the branch sits on the tip).
8. **Suites and static checks at head:** the whole originate workspace (files and tests, base vs head), tsc on the service config, and eslint on the touched files, each with a planted-defect control. KS-1989 (TS2451 under `--maxWorkers=4`) is pre-existing; do not count it against the PR.
9. **PR body.** Read it whole. It should state: the contract and who ruled it; the cause with the proof and the KS-960 pointer; the availability cost; Node v26 not 24; a NOT-tested list. Report each as present or absent, and flag any sentence the body makes that your measurement contradicts.

## HOLD-FOR-KAM conditions
Beyond gate_common section 6: any new user-facing words (a new message string, a field rename, a UI string) is HOLD-FOR-KAM. So is any change reaching the seeded accounts themselves (their passwords, roles or tenant). The 200-to-500 change on the all-failed cell is the INTENDED change and is NOT by itself HOLD-FOR-KAM.

## Mechanics
- **Workdir:** `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate195-ks1990-pr2006/`. Start with `.gitignore` (gate_common section 2). Every process cwd is inside the workdir, under `env -i`, with HOME and TMPDIR inside it.
- **Clone:** clone by SHA from origin into the workdir (read-only transport via the Secuura deploy key, as gate 194 did; see that gate's `scripts/` for the exact clone and install commands). `npm ci --ignore-scripts` at the head lock; build shared. Never link from the shared checkout's node_modules.
- No PostgreSQL or Docker stack is needed: the DB seam is faked, as KS-1802's harness does. The seat's own stack run of the cause is in the READY and is NOT re-run.
- **Never post:** the gate does not push, merge, comment on the PR or any ticket, send mail, or write to any board. It only READS.

## Output
`verdict.md` in the workdir. Line 1 per gate_common section 6, for PR 2006, naming the merge tree on develop 07a2d62be6a0 for the merge seat. Then the findings, F1..Fn, each with severity and its evidence path.
