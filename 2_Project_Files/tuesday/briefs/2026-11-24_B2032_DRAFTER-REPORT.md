STARTABLE: YES

# B2032 DRAFTER REPORT: NexusAI lane NX-S1 (RD-1021 + RD-1034), kit `2026-11-24_B2032_SEAT-N169_nexusai-rd1021-routes.md`

Drafter: an Agent-tool drafter for Tuesday (s321), commission `2026-11-24_B2032_NEXUSAI-NXS1-RD1021-RD1034_DRAFTER_COMMISSION.md`. Read window: Tue 24 Nov 2026 from 11:09:46 AEDT (first `date`) to the `date` on the last line of this report. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s321/d2032/`. Files written outside scratch: this report and the kit (and the kit's `.measured` sidecar, by `stamp_check.py --init`).

Read load for Tuesday (wc -c before this line was added): kit 58781 bytes, this report about 13103 bytes, sidecar 14985 bytes.

## BLUF
- The fix is small and proven on a prototype: the RD-1011 three-line administrator check as the first statement of `GET /api/setup/data-sources` and `GET /api/debug/data-sources`. Red-first at BASE: a viewer gets 200 with 2 connects and 2 stored-source reads (setup list) and 200 with 1 and 1 (debug read). After the edit: every non-administrator role of the permission table and the role value `Admin` get 403 `Admin access required` with 0 connects and 0 reads. Administrator and open-window controls read and connect as before.
- **The commission's partition does not fit the ticket (Q-0).** The ticket's acceptance and three older tests that pin the old answers need six more paths: the two generated inventory files, the RD-793, RD-988 and RD-978 test files, and the counts file. With only the commission's paths changed, five cells outside them go red. The kit is drafted with OWNS-B2032 widened to ten paths, marked `[Q-0 widening]`. `rd929-capability-design-census.test.js` (commission-owned) needs no change.
- **Deploy (Q-1): a merge of this lane starts a `Deploy demo` run** (`backend/**` is not path-ignored). Every job is gated on `vars.CI_DEPLOY_ENABLED == 'true'`; the last 100 runs all read `skipped`, including the last two `backend/` merges. The kit lands nothing; the landing read is Tuesday's.
- The full verify of the prototype (all nine A paths) passed: `VERDICT: PASS — 6280/6280 tests passed across 396 suites`, about 23 minutes. Counts move 6245/395 to 6280/396, the new file's 35 cells and nothing else. The frozen chain script `lane2032.sh` ran end to end on scratch trees in about 3 minutes, all judges PASS.
- Local CodeQL on the prototype (base `21a07e3c` = BASE for every scanned path, head the prototype K): `RESULT rc 0 PASS (KEPT high+ 0, NEW high+ 0)`, results 29 at both base and head.

## FACTS RE-MEASURED (instrument; control)
- origin main `d96a83d3ee6df25f74bcfe2f9ec0d0b42714e029` (gh GET 11:09:52; control: matching-refs b2013 length 1, b2032 length 0); open PRs 0; open code-scanning alerts 22, 13 at server.js, none inside the two handlers.
- The drafter's tree is the checkout's `21a07e3c`. `compare/21a07e3c...d96a83d3` shows 3 files (HISTORY.md and two `tests/e2e` files). 97 of BASE's 99 top-level entries are equal by object sha; the two that differ are HISTORY.md and tests.
- Jira GET, whole, comments paginated (`jwhole.py` in scratch). RD-1021: To Do, 0 comments, 6692 characters. RD-1034: To Do, 0 comments, 2596 characters. RD-1011: Testing, 2 comments (the landing note and the ruling note). RD-1030: Testing, 1 comment.
- Prior work by gh GET: PR 236 (merge `98e6a4d7`) touched 14 paths, including rd793, rd958, rd978, rd988, the inventory, its page and the counts. PR 242 (merge `85b39c77`) touched 4 paths.
- Red-first at BASE: 35 tests, 28 failed, 7 passed. The viewer gets `[200, undefined, 2, 2]` on the setup list and `[200, undefined, 1, 1]` on the debug read. `Admin` reads the same as the viewer.
- Green: 25 suites, 352 of 352, about 21 s. Red-proof (only the gates reverted): 81 tests, 29 failed, exactly as frozen in `judge2032.py`. `judge2032.py` controls: green1 judged as rf FAILs; red0 judged as redproof FAILs.
- The generator: `rows 203; 429s 0; ...`. It changes exactly two rows plus the meta, and the page by 5/5 lines. It writes 2 backup files, ignored by git (`.gitignore:129`).
- Full verify with `--update-counts`: `VERDICT: PASS — 6280/6280 tests passed across 396 suites (jest exit 0)`, 11:21:18 to 11:44:23, `EADDRINUSE` 0. Counts go from 6245/395 to 6280/396 (+35 tests, +1 suite).
- Prototype commits in scratch: A `6a8201eb03de` (9 paths) and K `c9c37d06581b` (1 path). `static2032.py` A and K both PASS; every scan's control fires. gitleaks over staged A: `no leaks found`. The gitleaks control needs a key-plus-secret pair (`leaks found: 1`); a bare AKIA string reads no leaks, so the kit's control wording was corrected.
- Local CodeQL (`pr_codeql_check.sh`, base 21a07e3c, head prototype K): results 29 at both base and head, KEPT 0, NEW 0, GONE 0, `rc 0 PASS`, 63 s.
- `lane2032.sh` end to end on scratch trees (only its `T=` line pointed at scratch): 11:46:24 to 11:49:31. Every judge PASSed. `product-apply` restored server blob `6d8e5139...`.
- `apply2032.py` round trip on a BASE copy: 6 of 6 files back to the BASE blobs. A second apply refuses with an anchor count of 0.
- Slots (sha256 mod 19 rule; controls b1977-nodot/work4 = 17 and b2013-nodot/chk26 = 17): vupd3 17, chk24 17, rf 2, work 3. lsof on the three bands at 11:25: 0 (control: the drafter's own listener at 20680 was seen).
- `stamp_check.py <kit>`: 136 claims, 136 measured, rc 0. The four-underscore count in the kit is 5 (four slots and the last line). Name scan over the kit (underscore-aware, the four names from scanlib1114.py line 20): 0, control fires.

## D-DECISIONS (the drafter's, each overrulable)
- D-1: two commits A (nine paths) and K (the counts file), the B1977 form, because the counts file can only be written by the project's verify after A exists.
- D-2: the new test file boots the real server through `__tests__/helpers/rd395-server-harness.js` `bootServer` (not `inventory.bootShape`), because `bootShape`'s seed has only an administrator and a viewer and the commission asks for every non-admin role of the table. It reuses `inventory.serverEnv`, `inventory.PRELOAD` and `roles-inventory-seed.js`'s constants, so the fence and the ledger are the inventory's own.
- D-3: stored-source reads are counted by a preload the test writes into its own temporary folder at run time (it `require`s the inventory's preload first, then wraps `JsonStorage.prototype.getDataSourceDecrypted`). The commission allows at most one new test file, so there is no separate helper file.
- D-4: the moved rows go to the end of the `admin.read` block with a two-line comment, the place RD-1030 used. RD-1022's rows stay under `config.read`.
- D-5: RD-1034's about text: `administrator-only reads: audit, incidents, retention, state, users, provisioning, and the data-source reads that use stored sign-in details`. The ticket says RD-929 owns that wording; this is the shortest true form.
- D-6: three jest-lock acquisitions (lane, update verify, plain verify), each through a frozen script so the command is identical across seats.
- D-7: chain trees `rf` and `work` live under `.tools/b2032/` (slots 2 and 3); only the two verify trees use slot 17 (`b2032-nodot/vupd3`, `b2032-nodot/chk24`).

## Q-QUESTIONS FOR TUESDAY (each with a default)
- **Q-0 (partition).** OWNS-B2032 adds six paths beyond the commission's list: `docs/role-capabilities.json` and `docs/ROLE-CAPABILITIES.md` (generator only), `__tests__/rd793-...`, `__tests__/rd988-...` and `__tests__/rd978-...` (four cells, the narrowest new answer), and `scripts/verify-expected-counts.json` (`--update-counts` only). **Default: accept.** The ticket's own acceptance names the inventory, its page and the counts, and pull request 236 changed the same file classes. If refused, the lane cannot meet RD-1021's acceptance and the kit is not startable (REFUSE 1 says so).
- **Q-1 (deploy).** The merge starts a `Deploy demo` run whose jobs skip unless `vars.CI_DEPLOY_ENABLED == 'true'`, and whose deploy job needs the `demo` environment's reviewer. Measured: 100 of the last 100 runs skipped. **Default: the landing holds for Tuesday's read of that variable or of the run's job conclusions after the merge. No deploy is covered by this commission. If a job would run, Tuesday stops the landing and the C-224 demo hold applies.**
- **Q-2 (the refused answer).** Frozen: 403 `{ "error": "Admin access required" }` from `requireAdminFor` (server.js lines 19106 and 19111 at BASE), the same answer RD-1011's four routes give. A request with no session still gets 401 from the sign-in check. **Default: as frozen.**
- **Q-3 (cell coverage).** The cells cover the nine non-admin roles of `ROLE_CAPABILITIES` (read at run time) plus `Admin`, the administrator, and no session. They also cover three request shapes that are not the tested GET: a query string, a trailing slash, and HEAD. Named as limits (not covered): upper-case paths, method-override headers, the sign-in-unproven mode, a hosted instance, and the open window after a first-run reset. RD-1011's review measured upper case and method override on the sibling routes, and they read 403. **Default: as built.**
- **Q-4 (jest on this Mac).** Yes. The drafter's runs: red-first 35 tests in about 3.5 s, green 25 suites (352 tests) in about 21 s, red-proof 81 tests, the generator in about 2.5 minutes, and the full verify (finding 9). **Default: none needed.**
- **Q-5 (the setup list for a viewer).** RD-1021 asks the product owner only if a viewer should keep the list. The callers are the wizard (open while first run is unfinished) and the Data Sources tab of `admin.html`. After the change a viewer on that tab sees `HTTP 403` in its error box, as on neighbouring administrator tabs. **Default: refuse (the ticket's proposal and the RD-1011 form). The commit and test header call it a default, not the product owner's choice. The records pass asks the ticket's question with the landing. Reversing it is the setup handler's three lines, two inventory rows and three cells.**
- **Q-6 (the about text and the comment wording).** D-5's wording, plus the RD-1011 header reworded to three lines that cite "the product owner's 2026-11-20 ruling". **Default: as frozen.**

## UNMEASURED
- The seat's own clone, `npm ci`, commits, push and CodeQL at the real BASE sha (the drafter's tree is `21a07e3c`, equal to BASE for every path read).
- The generated docs at the seat: `generatedAt` and `originMain` differ by construction. `static2032.py` checks rows, not blobs.
- The `Deploy demo` variable's value: not readable at repository level.
- A browser on `admin.html` as a viewer after the change. The `HTTP 403` text is read from `admin.js` line 183, not rendered.
- The plain verify at K (the kit's step 8). Its pair is PREDICTED equal to the update run's 6280/396.

## CHAIN INPUTS (every step's inputs are produced by an earlier step or exist at BASE)
| step | inputs | made by |
|---|---|---|
| Step 0 | the kit, the frozen files, Jira | Tuesday's stamp; the drafter's folder; Jira |
| Step 1 | the project checkout, the deploy key | BASE |
| Step 1b | the clone at BASE, `apply2032.py` | Step 1, Step 0 |
| 0 `trees` | BASE, the frozen test file, `apply2032.py` | Step 1, Step 0 |
| 1 `quiet`, 2 `backups` | the lock base, `work` | Step 1, step 0 |
| 3 `lane` | `rf`, `work`, `lane2032.sh`, `judge2032.py`, `suites2032.txt` | step 0, Step 0 |
| 4 `inventory` | `work`'s generated docs | step 3 |
| 5 `astep` | `work`'s nine paths, `msg-A.txt`, `static2032.py` | steps 3 and 4, Step 0 |
| 6 `update` | A, `v2032.sh` | step 5 |
| 7 `kstep` | `vupd3`'s counts file, `msg-K.txt` | step 6, Step 0 |
| 8 `plain` | K | step 7 |
| 9 and CQ, push | K, origin | step 7 |

## OUTSIDE-THE-FENCES DISCLOSURE
- **Jest without the lock.** Every jest run and the generator ran WITHOUT the project's jest lock. The commission (Q-4) asks for a prototype run, and writing a lock ticket would be a write in the project tree. Before each run the lock base listed no holder, `queue-jest` held 0 tickets, and no NexusAI pane was live. Load averages were 2.6 to 7.9 on 18 CPUs.
- **Two hook refusals.** A hook refused `ln -s` and then `cp -R` of `.tools/b2013/clone/node_modules` into scratch (the guard read the source path as a write target). I took each refusal as a STOP for that action and ran my own `npm ci` in the scratch clone instead. The registry download was over HTTPS to npm, not to any project host.
- **Writes in my own scratch clone (never pushed):** a branch `proto2032`, a repo-local scratch git identity (`drafter-scratch@invalid.test`), commits A and K, two worktrees `t/rf` and `t/work`. This was not a project repo, but it was disclosed under the identity rule.
- **Reads only toward the project:** git read verbs on the checkout (the clone itself reads it), cat/grep/sed of project files, gh `-X GET` and Jira GET only. Nothing was written under `!CODING`. No az, no ssh, and no HTTP to any hosted site.
- **One reading error, mine.** My first `static2032.py` A run passed a wrong name list (a parse slip, so the name check FAILed). I fixed the parse and re-ran, and it PASSed. The kit tells the seat to print line 20 with `sed -n 20p` and pass its four plain names.

Last `date` of the drafting: Tue 24 Nov 2026 11:52:05 AEDT
