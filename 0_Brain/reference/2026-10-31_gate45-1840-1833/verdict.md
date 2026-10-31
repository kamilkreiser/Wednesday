## QA GATE 45 - TIER 1, ROUND 2 (delta) - Secuura/Blockchain (Platform K) - Sat 31 Oct 2026
Findings-only. Nothing pushed, commented, merged or mailed; nothing under !CODING written. Clone `repo/` (toplevel asserted equal before any fetch; push URL `no_push_qa_gate`; ends clean, `git status --porcelain` empty). ls-remote at 10:01 and 10:27 AEDT: #1840 = 4b166a00d60b, #1833 = e4767d5838cb, develop = cb2320368ae4 (develop has moved past both PRs' merged bases). Load1 ~8.5 throughout; runs sequential, `--maxWorkers=2`.

---
# A) PR #1840 (KS-1845, Seat E 22nd), head 4b166a00d60b - VERDICT: GO WITH NOTES

**BLOB TABLE** (`probes/blobtable.py`, PR file list = diff merge-base a41909b50b44..head; out `probes/blob_1840.txt`): 15 files, 11 EQ to gated 9fc20b583645, 4 DIFF = kyc/src/index.ts (6927693e -> 0bda6a2e, numstat +10 -2), the kyc ks1845 test (3020fed9 -> b0734f38, +75 -4), the two Projects Documents html. E's claim confirmed exactly. Develop-merge files (anchoring etc.) are develop's side, not in the PR diff.

**The fix** (index.ts:1063-1064 `foldedUserId`, :1094-1098; read at `probes/kyc_index_head.ts`): both ids pass through `typeof id === 'string' ? id.toLowerCase() : ''`; refuse when either key is '' or they are equal. Correct:
- Case folding both directions: K1b (row UPPER, token lower) and K1c (row lower, token UPPER) both 403; mutants G2/G3 (fold one side only) each killed by exactly the opposite cell.
- Non-string / missing / empty: reviewer undefined, 7, '' -> 403 (K6a-c); row with null subject -> 403 (K7). G6 (`String(id)`) and G7 (truthy check) killed by K6b/K6a/K7.
- Fail-open direction: refusal is on equality, so over-folding only over-refuses. The only writer of svc_kyc_verifications.user_id is /api/kyc/initiate (git grep, index.ts:173 INSERT is the only one; control count 12 hits in that file), fed by `z.string().uuid()` (index.ts:519: ASCII hex + hyphens, any case). For that alphabet toLowerCase is the canonical fold; G11 (toUpperCase) and G12 (ASCII-only fold) are equivalent mutants and survive, as expected. Real tokens carry `userId: string` (shared middleware/index.ts:22, :110/:121 set req.user from the verified token).
- Other new compares in product files: governance.ts, stake.ts, delegations.ts, wallet-connector server.ts each add only `if (!isPlatformRole(role))` (blob-equal to gated head); isPlatformRole (shared security/keyRevokePolicy.ts:140-145) refuses non-strings and folds ASCII only. No other compare fails open.

**Tests**: kyc whole suite at head 7 files / 58 tests pass (`probes/kyc_head_full.log`); ks1845 kyc file 24/24 verbose (`probes/kyc_head_ks1845.log`). Red-first: the new test file against the gated-head index.ts (G13) = 6 red exactly K1b K1c K6a K6b K6c K7, K1d control green. Gate 45 own mutants (`probes/mut1840.py`, summary `probes/mut1840/summary.txt`): 11 of 11 non-equivalent killed (G1-G10, G13), 2 equivalent survive (G11, G12); G10 "always refuse" killed by R9-R11 + K1d. tsc kyc rc 0; eslint index.ts 0 messages (same instrument fires on #1833's gated head, see B). html_docs_check on both html: rc 0, positive control (injected prose `<p>`) fires rc 1.

**Round-1 findings**
- F1 CLOSED (above).
- F2 RE-OPENED, mechanical: E merged a41909b50b44 cleanly, but develop moved to cb2320368ae4; `git merge-tree --write-tree develop pr1840` again conflicts ONLY in the two Projects Documents html (`probes/mergetree_1840.txt`). No product/test file conflicts.
- F3 CLOSED: docs now say 72 cells (24 + 4x12), red at develop 18 of 24 (kyc) and 9 of 12 each; Spark's deterministic BASE run independently gives kyc 6 pass/18 fail, others 3/9; kyc whole 58/58 matches mine.
- F10 CLOSED as a record: the test header now pins lower-case `system_admin` as ADMITTED with the deviation stated (R9 green).

**FINDINGS (new)**
- F11 Mechanical, fix-before-merge YES (any merge needs it): F2's html conflict, again, vs develop cb2320368ae4.
- F12 Info, no: index.ts:1083 `reviewerId = userId || 'admin'` fallback is now unreachable (an empty/missing userId is refused at :1096). Dead code, harmless.
- F13 Info, no: foldedUserId uses full-Unicode toLowerCase while isPlatformRole deliberately uses an ASCII fold (KS-1591). Safe here (equality-refuse => over-fold fails closed; uuid alphabet), but the two folds differ in kind; worth one line if anyone reuses foldedUserId for an ALLOW decision.
- E's own mutants F1-M1..M8 were not available to me as files; I wrote my own (above) rather than re-running E's.

**NOT TESTED**: the other four services' whole suites (blob-equal to the gated head; gate 42 ran them; Spark targeted 12/12 each at head); real Postgres; running stack/gateway; real RS256 tokens this round; Node 24; deploy; platform suites.

**Spark shadow** (`spark_gate.sh` facts: HEAD 72 pass/0 fail 5/5 files; BASE product 18 pass/54 fail. First run without `--node-modules` gave 0/0 "Preset ts-jest not found" - instrument, re-run with node_modules). spark_review verdict NO GO, 5 findings: 2 "Major" on kyc (404-before-own-subject existence oracle; refusing a userId-less admin is a behaviour change) - both false as defects: the oracle is only open to an ALREADY-ADMITTED platform admin, and the refusal is the intended F1 close; 2 Minor on stake/wallet test strength (unchanged blobs, out of delta); 1 Note (mutant counts not in facts). It did NOT find F11 (the re-opened html conflict) or F12/F13. Nothing I would promote.

---
# B) PR #1833 (KS-1844, Seat U 7th), head e4767d5838cb - VERDICT: GO WITH NOTES

**BLOB TABLE** (`probes/blob_1833.txt`, merge-base 4c14143b3426): 4 files, all DIFF vs gated 9361d5979e23: certifications.ts (f7214662 -> ab869e18), the ks1844 test (7ae086c1 -> 78548b66), the two html. Product delta read by `git diff 9361d5979e23 head`: exactly `let invalidId: boolean;` and `reason = String(error instanceof Error ? error.message : error);` plus comments (+5 -2 as claimed). Develop did not touch services/originate, packages/ or the lockfile since the merge base (git diff --stat empty), and merge-tree's certifications.ts blob = head's, so the merged tree's originate == head's.

**No leak of the thrown value into the 500 body - by any path.** The 500 body is a literal (certifications.ts:1094); nothing from `error`/`reason` reaches `res`. Measured:
- Gate 36's REAL-logger hunt re-run on the new head (`probes/g36/run.sh head-real HEAD g36-hunt 1`, harness ported, paths only + `--maxWorkers=2`): 23/23 (H13-H15 now 500, one write, server alive). Control: the gated head under the same run = 3 red, H13 H14 H15 (reproduces gate 36 F1). Mock logger 23/23. Base 12 red (the original hangs).
- Same hunt with NODE_ENV=production (json() console + keepFileFields FILE transports, run from a scratch cwd so logs/ landed there): head 23/23; gated head 3 red (H13-H15). Closes gate 36's "production logger path NOT TESTED".
- Gate 45 extra hunt (`probes/g36/g45-extra.test.ts`, 17 new thrown values + 8 exact-body shapes): undefined, BigInt, number, array, toString->object, message getter -> {toString->SECRET} / Symbol / {toPrimitive->object}, AggregateError holding a revoked proxy, function, 1st-read-ok/2nd-read-throws getter, String object, cause = revoked proxy, 200 KB message, frozen Error with numeric message, subclass with throwing prototype getter, plain throwing getter. Head REAL 25/25, MOCK 25/25, PROD 25/25: every one 500 + constant envelope + no SECRET in body + one write + follow-up 404 + no rejection + the logged `error` is typeof string. Control: gated head REAL 4 red (E06 E07 E08 E15: logged object/symbol/number), base 8 red.
- 404 paths unchanged: S1-S4, S6 404 and S5, S7, S8 500 with exact bodies at head (S5 = gate 36 F3, pre-existing).

**Tests**: author file 8/8 at head; red-first: gated-head product 1 red (D4), base product 4 red (D1-D4), controls green - matches U's and the doc's claims (`probes/mut1833/R1_*`, `R2_*`). Whole originate unit suite at head (= merged tree for originate): 153 files / 1868 tests pass, rc 0 (`probes/originate_unit_head.log`). tsc originate rc 0 (`probes/tsc_originate_head.txt`); eslint certifications.ts 0 messages; control = gated head file in the same tree gives 1075:11 no-useless-assignment (gate 36 F4 closed). Gate 45 mutants vs the author file (`probes/mut1833.py`): N1 (revert coercion) killed by D4; N2 (fallback '') D1 D3 D4; N3 (`detail: reason` in body) and N4 (reason as message) D1-D4 + C4; N5 (404 off) C1-C3; N6 (raw message also logged) D1 D3 C4; N8 (unreadable -> 404) D1-D4; N9 (`String(error)`) C4. N7 (`res.end()` after json) survives - equivalent (a no-op on a finished response). Tree clean after (`git status` empty).

**Round-1 findings**: F1 CLOSED (above, real + production logger). F2 CLOSED (whole-envelope asserts; gate 36 M3 and M7 equivalents N2/N3 killed). F4 CLOSED. F3 and F5 pre-existing / class, unchanged.

**FINDINGS (new)**
- F6 Mechanical, fix-before-merge YES (any merge needs it): `merge-tree develop(cb2320368ae4) pr1833` conflicts ONLY in the two Projects Documents html (`probes/mergetree_1833.txt`).
- F7 Info, no: the doc's "153 files / 1862 cells" was measured at develop 530f091120d5; on the merged head it is 1868 (develop added cells). Not false, dated.
- F8 Info, no: the 404 controls C1-C3 still assert status + code only, not the whole 404 envelope (the 500s now assert the whole envelope). My exact-body S1-S4 show the 404 body is constant.
- F9 Info, no: the log line (console and the production FILE logs) carries String() of the thrown message, e.g. a secret-bearing message reaches logs/error.log (`probes/g36/...PROD` runs, error.log grep 20 SECRET lines). That is the stated design ("otherwise String() of the message"), and KS-1348 redaction is key-based; noted only because "never leaks" is about the BODY, not the log.

**NOT TESTED**: originate integration (needs DB); the real app's process-level unhandledRejection handler; whether any real path throws such values; the 87 sibling `instanceof Error ? message : String` sites (gate 36 F5); platform suites; running stack; Node 24; U's exact mutant files (mine are re-derived).

**Spark shadow** (facts: HEAD 8 pass/0 fail; BASE product 4/4 - matches my red-first). spark_review GO WITH NOTES, 7 findings: Minor "suite mocks the logger" (true of U's file; I closed it with the real + production logger hunt); Minor "D2 does not pin the log call" (true, trivial - I did not raise it); Notes that 1862 cells / lint are not in its facts (I measured: 1868, eslint 0 with control). It did not see F6 (html conflict) or F9.

---
**HOW (both)**: clone `git clone --shared` from gate 36's local clone, remote set to git@github.com:Secuura/Distributed_Secuura.git with the Blockchain deploy key as core.sshCommand (copied from gate 36's `remote -v` / config), push URL no_push_qa_gate; fetched refs/pull/{1840,1833}/head and develop. `npm ci` in repo/Blockchain/Dev (1806 packages), shared `npm run build`. Repo runners only: vitest (kyc) via `npm exec -- vitest run --root ... --maxWorkers=2`, jest (originate) via `npx jest --rootDir --config jest.config.js --maxWorkers=2`. Spark work dirs in the session scratchpad (spark_gate.sh refuses a work dir under /Volumes/DevMASTER/WEDNESDAY). No containers, no Postgres, no background servers left (jest/vitest exit by themselves). Instrument faults: a zsh word-split broke my first blob-table loop (re-done in python); `--minWorkers` is not a vitest 4 flag (dropped); my first extra probe failed TS6133 (unused helper; fixed, not a product result).
