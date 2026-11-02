# QA Gate 125 verdict (TIER 2): Secuura/Distributed_Secuura PR 1943 (KS-1868, originate certificationRepo.ts listCertifications and getSharesByCertification catches, held Spark pass O79-A6)

## BLUF
**GATE 125 (TIER 2) on PR 1943 at 4ad60f682588: GO WITH NOTES. Nothing has to be fixed before merge.**
(1) Commit 1 equals held pass O79-A6 byte for byte (product and test blobs sha256-equal to the pass applied with patch(1) to base); commit 2 changes one character group in the test (`});` to `}, 30000);`) and nothing else.
(2) I ran the REAL `GET /api/certifications`, `/:id/lineage` and `/:id/evidence-bundle` routes with the REAL repository, replacing only the db driver, the logger, auth and the charge service, at base and at head, for an ordinary Error, a thrown string, a revoked Proxy, a throwing message getter and a getter returning a revoked Proxy (15 cells each). Answer (500 and the constant body), persisted writes (0), charge events (0) and unhandled rejections (0) are IDENTICAL base vs head in all 15; the unreadable-value after-state equals the ordinary Error's after-state exactly (same status, same body, same two log lines in the same order). The only change is log text: at base the unreadable value lost the repository's own line and the route logged the text of an unrelated TypeError; at head both lines carry the constant `unreadable thrown value`.
(3) No caller turns the rethrow into a verdict or an authorisation. TIER 2 holds.
Not measured on Node 24 (host Node v26.8.1). Mac arm64, load average 10 to 22 throughout.

## 1. Heads + diffstat (logs/head_start.log, head_end.log, commits.log)
- START 2026-11-02T11:22:08Z: PR head `4ad60f682588cb3f978aae472bb9f49dd38c7ae6` (= Wednesday's), develop `3e688ee239f2b742feb658c2763e11d5cdd99521` (= brief). END 11:41:11Z: PR head UNCHANGED. **Develop MOVED during the gate** to `fbacb63af446ecbb81a7a08de8c236a34c8b20f4` (1 commit); I re-ran the overlap and merge-tree on it (section 6).
- Merge-base with develop = `e2a2426d221d8bd672e97c43c6bbcd6c4027b350` (matches). 2 commits: `db76eec6` (held pass + fragments), `4ad60f68` (timeout). Three-dot numstat: 4 files, **+149/-2** as claimed: test +92, certificationRepo.ts +14/-2, cheat fragment +21, flow fragment +22. Nothing outside the declared paths. Develop NOT merged in (confirmed: 2 commits above the base, no merge commit).
- PR body not read (no Secuura gh auth here); the author's READY mail copied in evidence/v17_ready_pr1943.txt is the substitute. Body wording not verified.

## 2. The hunks (the whole product change)
`certificationRepo.ts`, two sites, same shape:
- `listCertifications` (head :206-212, old :206) and `getSharesByCertification` (old :390). `-` `logger.warn('<ctx>', { error: err instanceof Error ? err.message : String(err) });` `+` a `let reason: string; try { reason = String(err instanceof Error ? err.message : err); } catch { reason = 'unreadable thrown value'; }` guard and `logger.warn('<ctx>', { error: reason });`.
- UNCHANGED at both: the message texts (`DB list failed`, `Failed to fetch shares from DB`), level `warn`, `throw err` (the ORIGINAL value, by identity), the try body, the return shape. There is no fallback return at base or head (the seat's correction of the brief is right; the fragment says so).
- One expression change beyond the guard: `String(...)` now wraps the Error branch too, so an Error whose message getter returns a non-string is coerced (and, if the coercion throws, becomes the constant). At base the raw non-string was handed to the logger (see G125-F3).
- Other catches in the file (`getCertification` :182, `saveCertification` :320, `saveShare` :366, plus :61) still have the unguarded `err instanceof Error ? err.message : String(err)`: not in this diff, named by the author as NOT done.

## 3. (1) Held-patch identity (scripts/identity.sh, logs/identity.log)
- The held pass's checker artefacts: `patch.diff` = `cat section_1.diff section_2.diff` (cmp rc 0). Applied both section diffs with `patch -p1` to a `git archive` of base `e2a2426d221d` in scratch: dry-runs rc 0 and 0, applies rc 0 and 0.
- sha256, held vs commit 1 (`db76eec6`) vs PR head: product `e4604d9d177c...` = `e4604d9d177c...` = `e4604d9d177c...` (all three EQUAL); test held `8f8af6b834f7...` = commit 1 `8f8af6b834f7...`, **PR head `3fbce91fabec...` (differs, by commit 2 only)**.
- Commit 2 (`git diff db76eec6 pr1943`): 1 file, +1/-1: `-  });` `+  }, 30000);`. No assertion, no product line, no other file. The edited `it(` is the single template inside `describe.each(CASES)` that is R3, so it gives the 30000 ms timeout to **both** R3 cells (listCertifications and getSharesByCertification). The ruling named one cell (A6 R3 for listCertifications); the second R3 is the same template line (G125-F2, info).

## 4. (2) Behaviour (logs/probe_base.jsonl, probe_head.jsonl; scripts/probe_routes.test.ts; RUN, not read)
Harness: jest, the real `certificationsRouter` on a real loopback listener, the real `certificationRepo.ts` (base file for the base run, swapped in by sha-checked script, restored `RESTORE_OK`), `../db` replaced by a stand-in whose `$queryRaw` rejects with the chosen value (for lineage/evidence-bundle the first call, `getCertification`, returns a row and the second, the shares read, rejects), auth stubbed to a `super_admin`, logger and `chargeEvents` recording. Probe file was copied in and moved to logs/_quarantine; the clone ends clean.

Callers re-established by `git grep -nw` over the whole repo (logs/callers_all.log; positive control: both definitions show): the ONLY non-test callers are `routes/certifications.ts` :974 (`GET /`), :1559 (`GET /:id/lineage`), :1652 (`GET /:id/evidence-bundle`). The `e2e-v2` hits are an HTTP client method of the same name, not the repository. As the seat said.

All three: plain `await` inside a `try` whose catch is already guarded (KS-1868 P1, on develop) and answers a constant 500. Lineage and evidence-bundle both run `callerMayReadCertification` BEFORE the shares read, so the read decision was taken first. Evidence-bundle writes its `evidence_export` charge event AFTER the shares read.

| route | thrown value | status base / head | body | repo log line base / head | route log line base / head | writes, charges, unhandled |
|---|---|---|---|---|---|---|
| all 3 | ordinary Error | 500 / 500 | constant | own message / same | own message / same | 0, 0, 0 both |
| all 3 | thrown string | 500 / 500 | constant | the string / same | the string / same | 0, 0, 0 both |
| all 3 | revoked Proxy | 500 / 500 | constant | **none** / `unreadable thrown value` | "Cannot perform 'getPrototypeOf' on a proxy that has been revoked" (a different error's text) / `unreadable thrown value` | 0, 0, 0 both |
| all 3 | throwing message getter | 500 / 500 | constant | **none** / constant | "getter threw" / constant | 0, 0, 0 both |
| all 3 | getter returning a revoked Proxy | 500 / 500 | constant | the raw Proxy handed to the logger / constant | constant / constant | 0, 0, 0 both |

- 15 of 15 cells: status, body, query count, db write count, charge count and unhandled count equal base vs head. The after-state for every unreadable kind equals the ordinary Error's: 500, constant body, two log lines (`warn` from the repository, `error` from the route), nothing written, no charge.
- Persisted state: none from either function (both are SELECTs); evidence-bundle's charge insert is never reached (chargeCalls 0 in all 5 evidence cells at both versions).
- Base's difference was observability only: for the three unreadable kinds the repository logged nothing useful and the route logged a message belonging to the TypeError raised INSIDE the catch, not to the failure.
- Limits: a stand-in driver, not PostgreSQL or Prisma; the real production logger and the pg error type are not exercised (R3 in the committed test does use the real logger). Nobody who acts on the system chooses what Prisma's `$queryRaw` rejects with; the unreadable cases are synthetic, as with every KS-1868 site.

## 5. (3) Tier
No caller maps the rethrow to a verdict, a decision or an authorisation: a throw becomes the constant 500 `INTERNAL_ERROR`, same as before. The read-authorisation gate runs earlier and is untouched; the list route's non-admin filter runs after the call and is skipped by a throw at base and head alike (so a throw never widens the result). No persisted state. **TIER 2 stands.** Not tier 1.

## 6. (4) Re-measure
- **Red-first** (logs/newtest_base.log): the new file against the BASE product: **6 failed, 4 passed** of 10; the failures are R1, R2, R3 for both functions, each an assertion diff (`Expected - 1 / Received + 1`), controls C1 and C2 pass (4). Matches the author. Note R3 for listCertifications took **10705 ms** in that red run on this loaded host (the timeout edit allows it).
- **Green at head:** 10 of 10, three more runs (logs/timing_head_1..3.log, load 10 to 11): all 10/10; R3 list 598, 43, 33 ms.
- **Originate suite** (logs/suite_base_excl_new.log, suite_head.log; whole service, `--silent`, anchored with `--rootDir`): base product without the new file **180 suites, 2163/2163**; head **181 suites, 2173/2173**. Ratio +10 tests, +1 suite, 0 failures, as claimed (2163/180 to 2173/181).
- **tsc** (originate has no tsconfig.test.json; scratch config `tsconfig.g125.json` that includes src/__tests__ with jest types): `tsconfig.json --noEmit` rc 0 at head; with tests included rc 0, **0 errors at head and 0 with the base product**. Planted type error reported (rc 2, 1 error).
- **eslint** (Dev's own `eslint.config.mjs`, eslint 10.7 installed in a workdir tools folder, symlinked as the clone's `Dev/node_modules`; cwd = Dev): new test **0 problems**; certificationRepo.ts **0 errors, 1 warning at :68 `preserve-caught-error`** (pre-existing, outside both hunks, as the seat and Wednesday said). Planted file: 1 error (`no-debugger`) and 1 warning.
- **docs-fragments** (scripts/frag.sh, `docs-fragments.mjs check --root`): clean rc 0, "flow 117 legacy + 84 new, cheat 112 legacy + 84 new; lint clean, render passes", with the same cheat ADVISORY at line 6235 that gate 90 recorded as present on develop alone (G90-F7; not re-attributed here). Planted defects, all caught rc 1 and restored by sha (4 of 4 restore OK; rc 0 after): flow unclosed `<div>`; flow `<!--n-->.` removed; cheat unclosed `<div>`; cheat `</table>` corrupted.
- **merge-tree:** onto develop `3e688ee2`: rc 0, tree `611637492828...`, result changes exactly the PR's 4 paths; 55 files moved on develop since the base, **0 shared with the PR's 4** (control: develop's list against itself, 55). Re-run onto the moved develop `fbacb63af446` (62 files since the base): rc 0, tree `028341275b24...`, again exactly the 4 PR paths, 0 shared.

## 7. Mutants (scripts/mutants.py, logs/mutants_table.log, mutants_table_M8.log; product file only, tests untouched, sha256 restored after every run, all `restore=True`)
11 mutants x 2 sites = **22 runs, 22 killed, all by assertion** (a first M8, "log line removed", failed only by a TS6133 compile error, not a test; I redid it as `void reason;` instead of the log and it is killed by the 5 log-asserting cells).
| mutant | killed by (at either site) |
|---|---|
| M0 revert to base | R1 R2 R3 |
| M1 drop the inner try | R1 R2 R3 |
| M2 constant reason for all values | C1 C2 |
| M3 no `String()` coercion | R3 only (the real-logger cell is the only pin on it) |
| M4 readable non-Error branch to `'x'` | C2 |
| M5 swallow, no rethrow | all 5 |
| M6 rethrow `new Error(reason)` instead of the value | all 5 |
| M7 rethrow only the readable ones | R1 R2 R3 |
| M8 log removed | all 5 |
| M9 wrong context text | all 5 |
| M10 `warn` to `error` | all 5 |
Both sites are pinned by their own cells (a per-site file filter was not needed: each mutant is applied to one site and only that function's cells go red). No survivor (this differs from gate 90's M6, because C2 here throws a readable string).

## 8. Kam's ks1346 logging rule (type and field NAMES of a thrown object, never values)
- The rule's own test as the brief states it: does any changed log line print thrown-value text it did not print before? **No.** Error: its message, as before (now `String()`-coerced). Non-Error: `String(err)`, as before. Unreadable: a constant, which prints less than base (base printed another error's text or a raw object).
- The two changed lines still log a thrown value's message/string content rather than names only (pre-existing at base, identical to every KS-1868 sibling; the route catches that log the same values are older). That is the card's open class, not something this PR adds. G125-F4 (info).
- The `String()` now applied to an Error's non-string `message` would print that object's `toString()` text where base passed the object to the logger; a getter whose toString exposes secrets is outside any realistic Prisma/pg Error. Read, not run.

## 9. FINDINGS
- **G125-F1 (INFO, measured)** Held-patch identity holds: product and test blobs of commit 1 are sha256-equal to O79-A6 applied to base; commit 2 is `}, 30000);` on one line.
- **G125-F2 (INFO, measured)** The edited `it(` is the single R3 template inside `describe.each`, so BOTH R3 cells (list and shares) get the 30000 ms timeout; the ruling and the commit message name one. Harmless and the right result (getShares R3 is 0 to 1 ms). Say "both R3 cells" in the body.
- **G125-F3 (INFO, measured)** At base a message getter returning a hostile object made the repository hand that raw object to the logger (my probe saw it). R3 pins the head behaviour through the real logger; nothing else does (M3 is killed by R3 only).
- **G125-F4 (INFO, pre-existing, ks1346-adjacent)** The two changed lines, like the route catches, log message text rather than "type and field names only". Not new, not worse. Belongs with the KS-1346 card, not here.
- **G125-F5 (INFO)** The R3 timing: 40 to 61 ms in the author's three good runs, 5338 and 5432 ms in two bad ones, and 10705 ms in my base red run at load 15 to 20. The 30000 ms edit is warranted by that spread; the cause stays unmeasured, as the body says.
- **G125-F6 (INFO, measured)** Develop moved from `3e688ee2` to `fbacb63a` during the gate; 0 shared paths, merge-tree clean on both.
- **G125-F7 (INFO)** Other unguarded copies of the same read remain in certificationRepo.ts (:61, :182, :320, :366) and are named as out of scope by the author's body; not a defect of this PR.
- **G125-F8 (INFO, wording)** Fragment says "the caller's own guard logged the TypeError's text" before, which my probe confirms for revoked-Proxy and throwing-getter ("Cannot perform 'getPrototypeOf' ...", "getter threw"). For the getter-returns-Proxy kind the route logged the constant at base too (the repository logged the raw Proxy). The fragment's sentence covers the first two kinds only; harmless.
- **No FIX-BEFORE-MERGE item.**

## 10. Notes for the PR body
1. (F2) State that the 30000 ms applies to both R3 cells.
2. (F5) Add the 10705 ms base red-run figure if wanted; the cause remains unmeasured.
3. (F8) Optionally narrow the "TypeError text before" sentence to the two kinds it holds for.

## 11. NOT TESTED
- The live PR body, Linear, CI, the author's pre-push hook (13 of 16 legs; quoted from the READY mail), Node 24.
- Real PostgreSQL/Prisma, a real boot, the gateway hop, the production logger configuration; the four platform suites.
- `tsc` and eslint were run with my own scratch config and a workdir-local eslint install (not the repo's `npm ci`); leg 16 (`typecheck-tests/check.cjs`) does not cover originate.
- The Seat's mutant claims (2/2) were not re-run as written; I ran my own 22.
- Whether any frontend or sibling service parses the old log text.
- Cleanup: no process of mine is left (ps read at 11:41Z shows only other seats' vitest and playwright-mcp processes). Scratch kept in the workdir: repo/, scratch_base_product.ts, scratch_head_product.ts, scratch_base/, eslint_tools/, logs/_quarantine/ (probe and planted files).
