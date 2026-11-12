PR 2157: GO WITH NOTES (at head 2c0692100527; tier 1; round 2)

Gate 329, tier 1 (Opus), one session, 2026-11-12 03:35Z to 03:47Z (14:35 to 14:47 AEDT). Findings only: nothing fixed, posted, mailed, pushed, merged, or written to Linear, GitHub or a board.

Where things ran:
- Everything that wrote ran in my own clone `scratch/repo` in this folder: a fresh `git clone --filter=blob:none` with sparse checkout of `/.github/`, `/Blockchain/Dev/`, `/frontend/`, `/Projects Documents/`, `/systemTest/` and `CLAUDE.md` (`scratch/setup.sh`). Write verbs (fetch, merge-tree) ran only there.
- Root `node_modules` is a symlink to gate 313's `r2` install, and `services/api-gateway/node_modules` is a symlink to the shared checkout's copy. Both are used read-only, as gate 325 did (`scratch/nm.sh`). The only `packages/shared` difference from r2 is one test file (`diff -rq`).
- In the shared Secuura checkout I ran read verbs only, with `GIT_OPTIONAL_LOCKS=0`.
- Every product or test file I changed in the clone was restored, and each restore was confirmed by git blob hash (`c12c71c753c0` for verification.ts). `git status` in the clone shows only the two node_modules symlinks.
- Machine: Node v26.8.1, macOS arm64, load1 about 6 to 8.

## Summary

The fix does what Wednesday's ruling asks:
- While `redisService.isRedisAvailable()` is false, every authenticated, well-formed `POST /api/documents` from a user now answers 503 before enforcement. That covers typed, untyped, `''`, falsy non-string and truthy non-string types.
- The G325-2204-1 hole is closed. I measured it with the REAL `enforceDocumentTypeRules`: on the old guard, a strict DOCUMENT entry refused an untyped create with 403 while Redis was up, and the same create passed with 201 while Redis was down. At the head the Redis-down case is 503.
- The merge commit is honest. The head's tree equals develop b7137aa97c79 plus the branch, exactly.
- Every READY number I re-ran reproduces: 3 of 7 red on the old guard, 7 of 7 at the head, the six suites at 72, the whole suite at 170 files and 1,904 tests, tsc 0 errors, and the ratchet at 25 / 25 / 0 new.
- No Major and no Minor. The notes are about precision (stale title and body lines, one unpinned shape) and one small new 403-to-503 change for callers with no write role.

## Pins

| when | develop | refs/pull/2157/head | refs/pull/2204/head |
|---|---|---|---|
| start, 03:35:30Z (`scratch/pins_start.txt`) | b7137aa97c79221730804ad208a8d080743ace5a (= commission) | 2c0692100527329a6c1d262b58fc2fd51740e4ac (= commission) | 25ad80bc8298 (merged) |
| end, 03:46:23Z (`scratch/pins_end.txt`) | **MOVED to 581296f039b4890ccf6f56e1c1f13575dc1098d4** | unchanged | unchanged |

**develop moved by one commit:** 581296f0, "Refs KS-2176: ts-node moves to tsx in five packages, dead ts-jest leaves two" (`scratch/newdev.sh`, list in `out/newdev_files.txt`).
- It changes 19 files and shares 0 paths with the PR. Control: the PR's own list compared with itself gives 3.
- `merge-tree --write-tree p2157 origin/develop`: rc 0, tree 6069f0a4c7f1.
- On that tree, the `services/api-gateway` subtree (dea63b673bd4) and the `packages/shared` subtree (0a2dc925bf53) are IDENTICAL to the head's. Positive control: `services/referral`, which develop changed, differs (4b6413fc to 6175a0fd).
- All 3 PR blobs survive into that tree.
- So every api-gateway result below holds on the new merge tree as source. The root `package-lock.json` changed, and I did not reinstall (see NOT TESTED).

## Q1. Is the merge commit honest? Yes.

Instruments: `scratch/q1.sh`, `q1b.sh`, `q1c.sh`.

**The commit's shape:**
- 2c0692100527 has two parents: 424bcfb752c8 (the fix) and b7137aa97c79 (develop at the pin). Its tree is 8f7aaa561b57.
- Commits on the PR that are not on develop: three, namely 1a8e6dd8 (round 1), 424bcfb7 (the fix) and 2c069210 (the merge).
- The branch's merge-base with develop is 0d286210f98b, 27 commits behind (`rev-list --count`).

**The tree equals develop plus the branch:**
- `git merge-tree --write-tree p2157^1 origin/develop` gives rc 0 and tree **8f7aaa561b57**, which equals the head's tree byte for byte. So the merge commit's tree is exactly git's own merge of the fix branch with develop; nothing was hand-edited during the merge.
- **The merge commit's own diff against its first parent** is exactly develop's diff since the merge-base. The 70 path names are equal, and the full patch text is equal (`PATCH_EQUAL`).
- **Blob equality, develop side:** for all 70 paths develop changed since 0d286210, the head's blob equals develop's blob: 70 of 70, 0 mismatches. Positive control: comparing the same 70 paths against the branch tip gives 70 mismatches, so the instrument can fail.
- **Blob equality, branch side:** for the branch's 3 paths, the head's blob equals 424bcfb's blob: 3 of 3.
- There are 0 shared paths between the branch and develop's 70.

**The PR's diff against develop** is 3 files, +143 -1, both by `git diff --numstat origin/develop p2157` and by GraphQL (additions 143, deletions 1, changedFiles 3):
- ks1952 test: +132 -0
- ks466 test: +2 -1
- routes/verification.ts: +9 -0

`git diff origin/develop p2157` is patch-identical to `git diff 0d286210 p2157^1`, the branch's own change.

**The fix commit alone** (`diff p2157^1^ p2157^1`) is verification.ts +5 -3 and the ks1952 test +19 -4, which equals the READY.

## Q2. The guard

**Where it is.** At the head, `routes/verification.ts:928`: `if (!redisService.isRedisAvailable()) { 503 SERVICE_UNAVAILABLE 'Document type configuration is currently unreadable; refusing until it can be read' }`. It is inside the `POST /api/documents` handler (line 739), and nowhere else. The commit diff touches only lines 921 to 931.

**Order inside the request:**
1. `authenticateToken(true)` is the route's middleware (line 739).
2. Then the hand-rolled body read and `JSON.parse`, with KS-529's 400 BAD_REQUEST for invalid or non-object bodies.
3. Then the KS-815 control-byte guard (400).
4. Then the connector block. A connector caller with Redis down already answered 503 at line 840 (KS-1256), so connectors are unchanged.
5. Then the new guard.
6. Then `enforceDocumentTypeRules`.
7. Then the KS-1871 write-role check (403).
8. Then the workflow gate and the forward to originate.

**Measured** with my route-level probe over loopback HTTP: `scratch/zzprobe-gate329.test.ts`, kept as `out/zzprobe-gate329.test.ts.ran`, driver `scratch/probe.sh`, table in `out/probe_table.txt`, raw `out/probe_{old,head}.tsv`. The probe has 2 routers, 2 Redis states and 46 rows each, run on the OLD guard (the 1a8e6dd8 x develop merge tree e1ecc213012d) and on the HEAD.

| Redis DOWN | old guard | head |
|---|---|---|
| untyped `{}`, `documentType ''`, `type ''`, `documentType null`, `false`, `0`, `type 0` | 201 past enforcement (enforcement ran) | **503 SERVICE_UNAVAILABLE**, enforcement 0 |
| `documentType` 123, true, [], ["DOCUMENT"], {}, "SECURE", "DOCUMENT", "  "; `type "SECURE"` | 503 | 503 (unchanged since round 1) |
| no Authorization header, typed or untyped | 401 | 401 (unchanged) |
| invalid JSON / non-object `[]` / NUL control byte | 400 / 400 / 400 VALIDATION_ERROR | the same (unchanged) |
| connector key, untyped | 503 (allow-list) | 503 (unchanged) |
| role VIEWER (no write role), **untyped** | **403 FORBIDDEN** | **503** (see G329-2157-3) |
| role VIEWER, typed | 503 | 503 (unchanged since round 1) |
| `POST /api/documents/` and `POST /api/DOCUMENTS` (Express non-strict routing reaches the same handler) | 201 | 503 (the same create, which is correct) |
| GET /api/documents/:id, GET /api/document-types, POST /api/documents/:id/sign, GET /api/workflow-instances | 404 / 200 / 404 / 200 | identical |

- **Redis UP:** all 46 rows are identical between old and head, for both routers.
- **Nothing that should not be refused is refused.** Other routes on the router, non-creates and the health paths are untouched. The health paths are mounted elsewhere: `index.ts:836`, `:871`. `routes/batch.ts` posts to originate's `/api/certifications`, not this route, and does not call enforcement. The only non-test callers of `enforceDocumentTypeRules` are the route, `index.ts` (wiring) and `admin.ts` (a comment), found with `grep -rln` over src.
- **Can an unauthenticated caller learn Redis state? No.** The 401 comes from route middleware before the handler runs (the probe's 401 rows, both states, both trees).
- A caller with a malformed body still gets its 400 first.
- An **authenticated** caller already learned Redis state from a typed create in round 1 (and a connector learned it on develop). The only newly revealing case is an untyped create by a no-write-role user (G329-2157-3).

## Q3. The cells

Instruments: `scratch/q3.sh`, logs `out/t_oldguard_ks1952.log` and `out/t_head_ks1952.log`.
- **Against 2157's previous guard on today's baseline** (the verification.ts of `merge-tree 1a8e6dd8 x develop`, with the head's tests): **3 failed | 4 passed (7)**. The 3 are C2 inverted, R3 and R4, all by assertion: `expected [201,'past-enforcement',1,…] to deeply equal [503,'SERVICE_UNAVAILABLE',0,msg]`. This equals the READY.
- **At the head:** 7 of 7. C1 and C3 (Redis up) are green on both trees and unchanged in the diff.
- Spark's deterministic half, an independent instrument, ran the same tests against **develop's** verification.ts (no guard at all): ks1952 5 failed / 2 passed (R1, R2, C2, R3, R4) and ks466 4 of 4.

**Mutants** (`scratch/mut.py`, results in `out/mutants.json`, logs `out/t_mut_*.log`). Each mutant was run against ks1952 plus ks466 (11 cells), and the file was restored to blob c12c71c7 afterwards.

| mutant | red | killed by |
|---|---|---|
| M1 guard reads only `body.documentType` (the commission's example) | 4 | C2, R2, R3, R4 |
| M2 the old `(documentType \|\| type) &&` condition | 3 | C2, R3, R4 |
| M3 guard only if the `documentType`/`type` key is present | 1 | C2 |
| M4 guard only for a string or absent type | 1 | R4 |
| M5 guard moved after enforcement | 5 | C2, R1-R4 |
| M6 guard removed | 5 | C2, R1-R4 |
| M7 guard inverted | 9 | all 5 Redis-down cells, C1, C3, 2 ks466 |
| **M8 guard skipped when `documentType === null`** | **0, SURVIVES** | see G329-2157-2 |

7 of 8 killed, including the commission's mutant.

## Q4. On the merge tree with 2204 (develop b7137aa97c79 already contains 2204)

The head's tree is that merge tree (Q1). On develop 581296f0 the api-gateway subtree is identical (Pins).

**The six named suites** (`out/t_six.log`, verbose, per-file counts from `✓` lines): **72 of 72**.

| suite | cells |
|---|---|
| ks1952 | 7 |
| ks466 | 4 |
| enforcement | 21 |
| ks501 | 9 |
| ks1466 | 11 |
| ks1203 | 20 |

This equals the READY's 72 (gate 325's 70 plus R3 and R4).

**The whole api-gateway vitest suite, proven whole:**
- `out/t_whole_head.log`: **Test Files 170 passed (170), Tests 1904 passed (1904), rc 0**. Spark DIGEST CHECKED PASS (`out/digest_whole_head/digest.md`); its two anomaly lines are a deprecation warning and a MaxListeners warning, nothing about failures.
- Whole-ness: a second run with the JSON reporter (`out/whole_head.json`, `out/t_whole_head_json.log`, again 170 / 1,904 / 0 failed / 0 pending) lists 170 file names. That list is **set-equal** to `find services/api-gateway -name node_modules -prune -o -name '*.test.ts' …` (170, `out/test_files_find.txt`; `diff` empty). The find list includes ks1952, so the instrument sees the new file.
- This equals the READY's 170 / 1,904.

**Does the G325-2204-1 hole close? YES, measured at full fidelity.** Probe router B uses the REAL `enforceDocumentTypeRules` over a redis module whose catalogue is STRICT while Redis is up (DOCUMENT needs creator level `standard` and MFA; the user is `basic` with no MFA) and EMPTY while it is down (the in-memory fallback with nothing written).
- **Old guard:** an untyped create (and `''`, `type ''`, null, false, 0, `type 0`) gets **403 INSUFFICIENT_VERIFICATION_LEVEL with Redis up and 201 created with Redis down**. The DOCUMENT rules are skipped during the outage. That is G325-2204-1, reproduced.
- **Head:** **503** for every one of them with Redis down, and the same 403 with Redis up.

**The cell that catches it.** The inverted C2 already catches the old guard at route level, through its enforcement-spy count (0 vs 1). It is red on the old guard and on M1 to M6. So a catching cell exists in the PR. Router B of my probe is a stronger form of the same cell (real enforcement plus a strict catalogue, Redis up giving 403 and Redis down giving 503). It is available in `out/zzprobe-gate329.test.ts.ran` if Wednesday wants it filed.

## Q5. Gate 301's notes and the body (the live body was read by GraphQL: `scratch/pr.py`, saved as `scratch/prbody2157.txt`, 13,503 chars)

- **G301-2157-1** ("the catalogue reads EMPTY while Redis is unavailable", stated as fact): **still present** in the code comment (verification.ts:923), the test header and the body's first bullet. It is still too strong (redis.ts 546-558 reads `documentTypesStore`, which `setDocumentType` fills in fallback mode). The guard no longer depends on the premise: it refuses on availability alone, for every body. So it is now a wording Note only (G329-2157-4).
- **G301-2157-2** (typed non-string `documentType` 400 to 503 during an outage, unstated): still true, and now **wider**. Every enforcement refusal and the KS-1871 403 for an untyped create also become 503 during an outage. The Fix round's "for any caller … enforcement does not run" covers it literally; the 403 case is not named (G329-2157-3).
- **G301-2157-3** ("502 files"/"504 files" do not reproduce): **still in the body**, in the round-1 Test plan section. The new section's 170 files / 1,904 tests reproduce (G329-2157-5).
- **"## Gate 301 notes" section: there is none in the live body.**
  - The count of `^## Gate 301 notes` is 0, and a case-insensitive count of "gate 301" anywhere is 1, the line "Gate 301's pin on the previous head is void by this push".
  - Positive control: `^## Fix round (G325-2204-1)` counts 1.
  - So that part of Q5 has nothing to read true or false. Gate 301's three notes were never carried into the body (G329-2157-6).
- **The "Fix round (G325-2204-1)" section:** present, placed before Summary, and **accurate** on every claim I could measure:
  - the merge commit and its parents;
  - "changes nothing else" (Q1);
  - the tree 8f7aaa561b57;
  - the 3 files;
  - +5 -3 and +19 -4;
  - C2 inverted, R3 and R4 added, C1 and C3 unchanged;
  - 3 of 7 red, then 7 of 7;
  - the six suites 72;
  - 170 / 1,904;
  - tsc rc 0;
  - leg 16's 25 / 25 / 0 new (my ratchet run reproduces the line verbatim);
  - 0 shared paths;
  - merge-tree rc 0;
  - the census.

  It honestly names the three superseded lines and the narrow title. One wording slip: "70 of 70 suites were green" should be 70 tests (cells). That is Info, folded into G329-2157-5.

**Other PR state** (GraphQL):
- OPEN, not draft, base develop, headRefOid equals the pin, 3 commits, mergeable MERGEABLE.
- closingIssuesReferences 0. The only comment is the `linear` bot's, from 2026-11-10.
- The title is unchanged: "Refs KS-1952: a typed document create answers 503 while Redis is unavailable".

## Q6. Census and typecheck

**Census** (`scratch/census_gql.py`, raw `scratch/census_rows_gql.tsv`): 101 open PRs, 454 file rows. Every PR's files were paged to totalCount and asserted.

| path | open PRs |
|---|---|
| `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (exact full path) | [2157] |
| ks1952 test | [2157] |
| ks466 test | [2157] |

- A suffix match on `routes/verification.ts` also hits 2138 and 2161, but both are `services/originate/src/routes/verification.ts`, a different file.
- **Control:** `api-gateway/src/index.ts` maps to [2125], so it FIRED.
- **Negative control:** an absent path maps to [].
- `services/enforcement.ts` maps to [] (2204 has merged).

**Typecheck** (`scratch/tsc.sh`):
- `tsc --noEmit -p services/api-gateway/tsconfig.json`: **rc 0, 0 errors** (`out/tsc_head.log`).
- Planted control (`isRedisAvailableX`): rc 2, 2 errors at verification.ts(840) and (928). Restored, and verified by blob.

**Ratchet:** `node scripts/typecheck-tests/check.cjs services/api-gateway` gives rc 0 and `tsc examined 208 files, 170 of them under __tests__; 25 errors: 25 in the baseline, 0 new; 0 stale baseline entries.` (`out/ratchet_head.log`). This equals the seat's leg 16. None of the touched files appears in that output: a grep of the three names gives 0.
- Planted control (a `number = "string"` line appended to the ks1952 test): rc 1, "27 errors: 25 in the baseline, **2 new**", both naming ks1952 (`out/ratchet_planted.log`). Restored, and verified by blob.

## Q7. The live-behaviour statement for the GO

After this merges and a gateway deploys (nothing deploys from the merge):
- **While the gateway's Redis is unavailable,** every authenticated `POST /api/documents` from a signed-in user with a well-formed JSON object body answers **503 SERVICE_UNAVAILABLE**, "Document type configuration is currently unreadable; refusing until it can be read". This applies whether it names a `documentType`, names a `type`, sends an empty or falsy one, or sends none. The create is not checked, not gated for approval and not forwarded to originate.
- **New compared with round 1:** untyped creates (and `''`, `null`, `false`, `0`) now get this 503. Before, they were checked against an empty fallback catalogue and created.
- **Also new for those bodies:** a user with no document-write role now gets 503 where they got 403.
- **Unchanged:** an unauthenticated request still gets 401, and an invalid or non-object or control-byte body still gets its 400. Connector-key creates already got a 503 from the allow-list check during an outage, and still do.
- **Every create behaves exactly as today when Redis is up,** including a fresh boot with an empty catalogue.
- **Production** refuses to start without Redis, but enters fallback on a sustained mid-run drop (redis.ts:78), so the 503 window there is a mid-run Redis outage.
- **Dev, local or E2E gateways** booted without Redis will 503 every create, typed or untyped.

## Findings

- **G329-2157-1 (Note, PR text): the title and three round-1 body lines are narrower than the behaviour.**
  - The title says "a typed document create answers 503". The opening bullet "Unchanged: … an untyped create with Redis up or down" is now false. The Summary says "one new file with 5 cells" (it is 7), and "Before this deploys" says "typed document creates answer 503" (it is every create).
  - The test's `describe` title still reads "a typed create answers 503" (ks1952 test, line 91).
  - The Fix round section explicitly names all of these as superseded, so a careful reader is not misled. A skimmer of the title or the "Before this deploys" line would be.
  - Recommend that Wednesday authorise a title and line edit before merge, or accept it as stated. It does not block.
- **G329-2157-2 (Note, test gap): `documentType: null` is not pinned.**
  - Mutant M8 (`if (body.documentType !== null && !isRedisAvailable())`) passes all 11 cells.
  - Under M8, a null-typed create during an outage would reach enforcement, resolve as DOCUMENT over the empty fallback catalogue and pass. That is the G325-2204-1 class for one body shape.
  - `false`, `type: ''` and `type: 0` are likewise covered only by the probe, not by a cell.
  - The guard as written has no such condition, so this is about future regressions only. A table cell over `[{}, {documentType:''}, {documentType:null}, {documentType:false}, {documentType:0}, {type:''}, {type:0}, {documentType:123}]` all expecting `[503,'SERVICE_UNAVAILABLE',0]` would pin the "every create" contract.
- **G329-2157-3 (Note, an unstated behaviour change): during an outage, an authenticated user without a document-write role who sends an untyped create now gets 503 instead of KS-1871's 403.**
  - Measured: probe row "role VIEWER, untyped", old 403, head 503.
  - The same is true for every enforcement refusal (400, 403) on untyped bodies.
  - The guard sits before both the enforcement call and the KS-1871 role check. Round 1 already did this for typed bodies, so this is consistent and fails closed. It is not an authorization weakening: nothing that was refused is admitted.
  - What changes is what the caller learns. A signed-in non-writer now gets "configuration unreadable" (Redis state) where they got "forbidden". They could already learn it with a typed body since round 1, and a connector could on develop. Unauthenticated callers learn nothing new (401 first).
  - The GO sentence should name it (Q7 does).
- **G329-2157-4 (Note, carried G301-2157-1): "the catalogue reads EMPTY while Redis is unavailable" is still stated as fact** in verification.ts:923, the ks1952 header and the body.
  - The fallback store can hold types written during the outage (redis.ts 525-533, 546-558).
  - Since the guard now refuses on availability for every body, the claim no longer affects behaviour. It is a comment-accuracy Note only.
- **G329-2157-5 (Info): the body's round-1 "(502 files)" and "(504 files)" (G301-2157-3) are still there and still do not reproduce.** The new section's 170 files and 1,904 tests reproduce exactly. Separately, the Fix round's "70 of 70 suites" means 70 tests.
- **G329-2157-6 (Info): the commission's "## Gate 301 notes" body section does not exist** (0 hits, case-insensitive, with a positive control). Gate 301's three notes were not recorded in the PR body by either round. If Wednesday expected them there, they are missing. Otherwise there is nothing to grade.
- **G329-2157-7 (Info): develop moved during the gate,** from b7137aa97c79 to 581296f039b4 (KS-2176, ts-node to tsx, 19 files).
  - It shares 0 paths with the PR, merge-tree is rc 0, and the api-gateway and packages/shared subtrees are identical on the new merge tree.
  - The PR head did not move, so the head is not stale for audit purposes against anything this gate can see. Whether the pre-push audit gate needs a new merge after KS-2176's lockfile change is UNMEASURED.

No Major, no Minor.

## NOT TESTED

- A real Redis or ioredis client, fallback-mode transitions, or a live gateway or originate. Everything was at route level over loopback with mocked Redis.
- The real `authenticateToken` middleware: the probe's 401 is a stub. The ordering claim rests on the route definition at line 739.
- A reinstall at develop 581296f0. Its root `package-lock.json` changed, and I ran on the symlinked existing installs.
- Node 24 (everything ran on v26.8.1).
- eslint, docs-fragments, `npm run audit:gate`, the pre-push hook and its legs (quoted by the seat), and the four platform suites.
- Whether any E2E or smoke run starts the gateway without Redis: UNMEASURED, as the body says.
- Whether the OpenAPI spec lists 503 for POST /api/documents: not read (the READY's item e).
- Linear: the KS-1952 ticket text and the seat's comment 3e05e5d3 were not read. The Spark review therefore ran without ticket text.
- The seat's `evidence/fwd_proof_1952_r106.out`: not read; Q1 is my own instrument.

## Spark

**DIGEST STANDARD** on the whole-suite raw log (`out/t_whole_head.log`, kept): `CHECKED verdict=PASS raw=5903B digest=695B spark_s=4.9`. Only `out/digest_whole_head/digest.md` was read, and its counts (170 / 1,904 / 0 failed / 0 skipped) match the raw summary lines grepped directly. No finding rests on an anomaly sentence.

**Shadow review.** Driver `scratch/spark_run.sh`, copies in `scratch/spark/`, work dir in the session scratchpad (`spark_work_2157`). It ran `spark_gate.sh` and then ONE `spark_review.py` request with `--pr-body-file scratch/prbody2157.txt`. `missing_inputs: ["ticket text"]`, `valid: True`. Two attempts: the first ended in a repetition abort, the second finished normally (102.5 s total).
- **Deterministic half:** merge-base b7137aa97c79 (base tip 581296f0, the moved develop); diff 3 files +143 -1; targeted HEAD 11 passed / 0 failed; base product code 6 passed / 5 failed. All equal mine.
- **Spark verdict: NO GO (disagrees).** 4 Majors, 2 Minors, 2 Notes:
  1. Major, "the guard applies to EVERY create, wider than the ticket's typed scope": **false positive.** That width is the ruling this round executes, and Spark had no ticket text. It is adjacent to G329-2157-1 (the stale title) but frames it as a defect of the code.
  2. Major, "the root cause is inferred, not measured": **partial recall of G329-2157-4 / G301-2157-1** (the "reads EMPTY" overstatement), over-graded. Its evidence quote was not found in the input.
  3. Major, "other callers of enforcement could bypass the route guard": **false.** The only runtime caller is the route (grep; gate 325 Q3).
  4. Major, "the fake redisService never throws": **false positive.** The guard is a synchronous boolean read before any Redis call; a throwing read is KS-1256's catch on the connector path and is irrelevant here.
  5. Minor, "C1 and C3 prove only the fake's empty catalogue": weak, Info at most.
  6. Minor, "the whole-suite claim is not in facts.json": bookkeeping. I reproduced it (170 / 1,904).
  7. Note, ticket text missing: true.
  8. Note, the UNMEASURED E2E blast radius: a restatement of the body.
- **Recall against this gate's 7 findings:** 0 full and 1 partial (G329-2157-4). It missed G329-2157-1 as a text staleness issue, the null-shape gap (2), the 403-to-503 change (3), and 5 to 7.
- **False positives:** 3 of 4 Majors are wrong or misframed, and they drive a wrong NO GO. As a shadow it would have blocked a correct change and caught none of the real notes.
