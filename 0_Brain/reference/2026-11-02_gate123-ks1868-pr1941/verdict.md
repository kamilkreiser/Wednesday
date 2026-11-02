# QA Gate 123 verdict: Secuura/Distributed_Secuura PR 1941 (KS-1868, originate verification public surface: O78-P3 verificationV2.ts fetchChainFact :111; O79-B1 verification.ts :1443/:1478/:1506; O79-B2 verification.ts :758; O79-B3 verificationV2.ts :440/:482), TIER 1

## BLUF
**GO WITH NOTES (TIER 1). Nothing has to be fixed before merge.** I ran the real `verificationRouter` and `verificationV2Router` on a loopback listener, with v2 behind the REAL `authenticate({ required: false })` and, unlike gate 106, the **REAL winston logger**. Its formats ran, and each transport's `log()` was captured instead of written. Only these were replaced: the db (`$queryRaw` row store, `$executeRaw` counter), the JWKS verifier, the heal (write counter), the lineage repo, and the anchoring-service `fetch`. The same probe ran 412 cells at base e2a2426d and at head (scripts/probe.test.ts; logs/probe_{base,head}.jsonl, logs/probe_table.log, logs/probe_checks.log). It covered 7 PR sites plus 2 v1 chain-first sibling sites, 4 injection points (req.db getter, db reject, first res.json, chain fetch reject), 11 thrown values plus controls, and 2 callers (anonymous, and the owner's bearer).
- **Q1 held-patch identity:** all 4 `patch.diff` sha256 values equal the brief. Each is contained in its held READY file (python `in`, True 4/4), and section_1+section_2 equals patch.diff 4/4. Strict apply at e2a2426d in the brief's order (P3, B3, B1, B2) and in the reverse order: every `--check` gives rc 0 with empty output and no fuzz. B3 applies at offset +6 after P3, nothing else is offset. Both orders give the same tree `c7952bc7`. **The product blobs equal the PR head (`3097c26d` verification.ts, `c45550c5` verificationV2.ts) and all 4 test files are byte-equal.** The only paths that differ from the head are the two doc fragments, which are author-written and not part of the passes. 0 byte differences.
- **Q2 public surface:** at every PR site an unreadable value at head gets exactly what an ordinary Error gets. Judge: **176 cells OK = ordinary, 0 DIFF, 28 PRE-EXISTING (base == head, explained in F2/F3), 0 escaped handlers at head (52 at base), 0 NO ANSWER at head (40 at base), 0 unhandled rejections.**
  - B sites: an Error whose message getter RETURNS a revoked Proxy, or an object with a throwing toJSON, got **NO ANSWER at base** (the real logger threw inside the catch, outside the guard). At head it gets the route's constant 500, byte-identical to the ordinary-Error body.
  - P3: an unreadable value got **500 "Verification failed" / "File verification failed" at base**. At head it gets **200 `{hash, count:0, matches:[]}`**, which is what an ordinary chain-read Error gets today.
  - **No new disclosure:** every head non-control body is one of the route's existing constants or the existing count:0 answer (1 distinct failure body per B site). The leak scan of head bodies (planted values, tenant, holder, org, "proxy", "toJSON", "stack", "[object Object]") finds none. Anonymous and owner get the same body in every failure cell.
  - **Persisted state:** the counters for queries, `$executeRaw`, heal writes, chain fetches and errorHandler are identical base vs head in all 412 cells. `$executeRaw` = 0 everywhere, and the errorHandler (system_errors path) is never reached.
- **Q3 verdict sites:** verification.ts base vs head differs on exactly 4 lines (761, 1446, 1481, 1509; logs/verdict_sites.log). The four verdict-lineage catches (:883/:920/:1021/:1310) and the lookup catch :1437 are byte-identical. Across 412 cells, the only verdict-tuple changes base -> head are NO ANSWER -> constant 500 (B) and 500 -> count:0 (P3, F1). **0 cells newly answer verified/valid/found.**
- **Q4 P3 residual:** confirmed, base == head (F2). There is no disclosure to callers (the response is the constant 500). INFO.
- **Q5 merge orders with PR 1940 (96208f37):** both onto develop 0e3a9b65 are clean. 1940 then 1941 and 1941 then 1940 give the same tree `23fee71f`. The union changes exactly the 12 paths of both PRs (5 + 8, 1 shared file verification.ts). **No shared line:** the nearest hunks are 1940's :1438 and 1941's :1446, 8 base lines apart (F6). Develop then moved to 58b5042c (F7). Merge-tree onto it is also clean, and both orders give the same tree `4ba34fde`. In the union, both PRs' new tests pass (41/41) and so does the whole originate suite (186 files, 2204/2204), with tsc 0 errors.
- **Q6 re-measure:**
  - red-first: 15/30 by assertion (3/6, 2/4, 4/8, 6/12; every control passed)
  - green: 30/30
  - originate suite: 2163/2163 (180) -> 2193/2193 (184), 30 new, 0 vanished, 0 passed->not
  - tsc with tests: 0 errors at base (208 test files) and head (212); planted TS2322 gives rc 2
  - eslint: 0/0 on the 6 files; planted file gives 1 error + 1 warning
  - docs-fragments: rc 0 ("84 new"); planted `<div>` gives rc 1, restored by sha
  - **mutants: 43/43 killed** (F5 on how they were killed)
  - ks1346: compliant (F4)

## Heads
- START (logs/head_start.log, 2026-11-02T10:36:31Z): PR 1941 head `33644960bc2270f6850d82dbbf4323780b942b9f` (equal to the commission), PR 1940 head `96208f377d14…`, develop `0e3a9b65cdd632fbc1783257c6cb9833934e1404`, merge-base/parent `e2a2426d221d8bd672e97c43c6bbcd6c4027b350`. 1 commit, Kam Kreiser <kamil.kreiser@secuura.ai>, "Refs KS-1868: verification catches coerce a hostile message; v2 chain-fact read is guarded".
- END (logs/head_end.log, 2026-11-02T10:56:33Z; re-read in logs/merge_tree_dev2.log): **PR 1941 head UNCHANGED `33644960`**, PR 1940 unchanged. **Develop MOVED to `58b5042ccdb5a06a213ba53f5d4f7644f5f52549`** (one commit, KS-1940 governance, 5 paths, none shared; F7). The clone is at 33644960 with a clean working tree. Product sha256 was restored after every swap (RESTORE_OK for runs, probe base/head, tsc base and union; `restore True` 43/43 for the mutants).
- Diffstat, three-dot (logs/diffstat.log): **8 files, +734/-7.** That is verification.ts +4/-4, verificationV2.ts +10/-2, 4 new tests (166/159/168/183) and 1 fragment pair (22/23). Nothing is outside the declared paths. This matches the READY mail.
- **PR body not read** (no Secuura gh login here). I used the author's READY mail (evidence/v16_ready_pr1941.txt) and the committed flow fragment.

## FINDINGS
- **G123-F1 (INFO; the gate's answer to the author's GATE QUESTION; measured).** I accept 500 -> 200 `count:0` for an unreadable value in `fetchChainFact`.
  - `fetchChainFact` runs only when `matchesForHash` has ALREADY found zero registry rows, local and cross-tenant (:351). The chain read can only ADD a chain-only match.
  - Every ordinary chain-read failure already answers count:0 at base: a timeout, a refused socket, non-2xx, or a JSON parse error (probe cells chain/ordinaryError, chain503, nomatch, base == head).
  - So the head answer for this value class equals the ordinary one byte for byte (normalised timestamps) and claims nothing the stored state does not say. It is not a new "not found" outcome, only the existing one reached by one more input.
  - The value cannot be caller-chosen: the rejection comes from `fetch`/`resp.json()` against the internal anchoring service, with no bearer forwarded and no caller object involved.
  - Pre-existing and outside this PR: a chain-read failure is indistinguishable in the response from "never registered" (no `chainRead: 'failed'` signal). That is a design question for a card, not a block.
- **G123-F2 (INFO; the author's disclosed P3 residual; measured, base == head).** In `fetchChainFact`, `reason = err?.message` is not coerced.
  - An Error whose message getter RETURNS a revoked Proxy or an object with a throwing toJSON passes the guard. The REAL logger then throws inside `logger.warn`, `fetchChainFact` rejects, and the route answers **500 "Verification failed"** at base and head alike, where an ordinary Error gets 200 count:0. This is 8 of the 28 PRE-EXISTING cells.
  - **Not a disclosure risk to callers:** the body is the constant 500 with no new field, message, stack or id.
  - Log-side: when the message is a READABLE object (field values, or a null-prototype object), its field VALUES are written to the console line (`{"error":{"field":"SECRETVAL"}}`), base == head. That is ks1346-adjacent, logs only, and the values are not caller-supplied.
  - Optional follow-up, the same form as the B passes, which keeps the thrown-string control C2 logging `undefined`:
    ```
    reason = err?.message === undefined ? undefined : String(err.message);
    ```
- **G123-F3 (RECOMMENDED follow-up; pre-existing, NOT in this PR; measured, base == head).** These are the v1 siblings of P3. Both chain-first catches read `chainErr?.message` unguarded:
  - `verification.ts:698-699` (`POST /verify-file`): an unreadable value gets 500 "File verification failed", where an ordinary Error gets 200 "NOT in the Secuura registry".
  - `:1243` (`POST /verify` hash): an unreadable value gets 200 "Verification lookup failed", or 500 for a getter throwing a Proxy, where an ordinary Error gets 200 "not registered".
  - These are 20 of the 28 PRE-EXISTING cells. They belong on the KS-1868 site list.
- **G123-F4 (INFO; ks1346; measured).** The B passes IMPROVE the log for an object-valued message.
  - Base wrote the object's field values (`{"error":{"field":"SECRETVAL","tenant":"tenant-owner-x"}}`). Head writes `"[object Object]"`.
  - One shift to name: an object message with its OWN `toString` now logs that text (`"custom SECRETVAL"`), where base logged `{}`. Likewise a number logs `"42"` and undefined logs `"undefined"`. This is the same class as an ordinary string message, which is logged verbatim (G106-F7).
  - In production, `keepFileFields` keeps `error` only when it is a string, so these strings now also reach the file logs. That is read from logger.ts, not run (no production-mode run; it would write files into the cwd).
  - Response bodies never carry any of these.
- **G123-F5 (INFO; mutant tooling).**
  - M5 (the fallback rethrows) at the 6 B sites is killed by a suite crash (jest formatting a revoked Proxy), not by assertion. This is the same as G106-F5.
  - P3's M0 (revert only the log line's read) is killed by TS6133 (`reason` unused), a compile kill. The behaviourally equivalent M1 (drop the try) is killed by assertion (R1-R3).
  - Every other mutant is killed by `expect(`. Each B site's kills land only in its own test file.
- **G123-F6 (INFO; wording).** The fragment and the READY mail say the union with the KS-1939 passes is "81 lines apart". Measured, the closest hunks are 1940's `:1438` (`+7`) and 1941's `:1446`, **8 base lines apart**. Seven context lines separate them, and no line is shared. Correct it in the body, or give both distances.
- **G123-F7 (INFO).** Develop moved during the gate, 0e3a9b65 -> 58b5042c (KS-1940, 5 paths, 0 shared with either PR). Merge-tree of 1941 onto it is clean with exactly its 8 paths (`66d36fe7`), and both union orders give `4ba34fde`. The author's "develop NOT merged in" stands. The forward-move rule is satisfied (shared paths 0).
- **G123-F8 (INFO; for gate 122 / the union).** In the union, verification.ts carries two guard forms. PR 1940's `:1438` uses `reason = dbErr?.message` with no `String()`, so it has the same residual as F2. A hostile-object message there escapes to PR 1941's `:1446` guard and becomes a constant 500, so neither PR leaves a request unanswered. A follow-up should make the forms consistent.
- No FIX-BEFORE-MERGE item.

## Q2. Behaviour, measured (logs/probe_table.log; the judge is scripts/table.py, the extra checks logs/probe_checks.log)
| site (injection) | ordinary Error, base = head | unreadable (revoked Proxy, throwing getter, getter throws Proxy), base -> head | message getter RETURNS a revoked Proxy / a throwing-toJSON object, base -> head | null-prototype object as message, base -> head |
|---|---|---|---|---|
| B2 v1 /verify-file :758 (db reject, json) | 500 constant, the message logged | 500 constant / same (already guarded by PR 1925) | **NO ANSWER -> 500 constant**, log constant / `[object Object]` | 500, object logged -> 500, log constant |
| B1 v1 /verify :1443 (req.db), /hash :1478, /status :1506 (json) | 500 constant | same | **NO ANSWER -> 500 constant** | as above |
| B3 v2 /verify (hash and id) :446 (req.db, db reject, json); /verify-file :488 | 500 constant | same | **NO ANSWER -> 500 constant** | as above |
| P3 v2 /verify, /verify-file chain read :111 | 200 count:0, warn with the message | **500 constant -> 200 count:0**, warn constant | 500 -> 500 (F2, base == head) | 200 count:0 both (object logged, F2) |
| v1 chain-first :698 / :1243 (not in PR) | 200 not-in-registry | 500 / lookup-failed, base == head (F3) | base == head | base == head |
Controls (success, nomatch, chainok, chain503) give base == head in every cell. Readable kinds (string, object, toString, number) never change status or body. Only the log's `error` field changes, for object or number messages at the B sites (F4).
**What was READ vs RUN:** RUN means the routers, the optional-auth middleware, the logger formats, the handlers' catches, the response bodies and the counters. READ means the production-mode file format (F4), the real heal/Prisma/PostgreSQL, multi-tenant mode (`getTenantManager` null), the gateway hop, and whether any real value of these shapes occurs.

## Q4. Re-measure (Node v26.8.1; NOT measured on Node 24)
- Red-first (logs/red_base.json, logs/red_base_cells.log): 15 failed of 30, every failure by `expect(`, all 15 controls pass. This equals the author.
- Green (logs/head_new.log): 30/30. Whole suite (logs/whole_{base,head}.log): 180 files 2163/2163 -> 184 files 2193/2193. Cell by cell: 30 new, 0 vanished, 0 passed->not. Load1 13-22 (logs/load_runs.log).
- tsc: plain rc 0. With tests (scripts/tsconfig.tests.json): rc 0, 0 errors at base (208 test files) and head (212). Planted TS2322 gives rc 2.
- eslint (scripts/lint.cjs, ESLint API with cwd = originate): 6 files, 0 errors, 0 warnings, 0 ignored. Planted file: 1 error (no-debugger) + 1 warning, rc 1. (A first CLI attempt with `--config` from Wednesday's cwd mis-based the flat config and reported "file ignored"/parse errors. That is an instrument fault, discarded.)
- docs-fragments: rc 0, "flow 117 legacy + 84 new, cheat 112 legacy + 84 new". It prints the known cheat ADVISORY at line 6235 (G90-F7, from develop). A planted `<div>` in the PR's cheat fragment gives rc 1 "tags are not balanced", and FRAG_RESTORED.
- The author's recorder (160 scenarios, judge 561/561, tampers 6/6) was not re-run. My own probe stands in its place.

## Q5. Mutants (scripts/mutants.py; product only, tests untouched, all 4 new test files per run, sha256 restore True 43/43; logs/mutants_rows.json, logs/mut_*.log)
| mutant | B2:758 | B1:1443 | B1:1478 | B1:1506 | B3:446 | B3:488 | P3:111 |
|---|---|---|---|---|---|---|---|
| M0 revert the hunk | K (R1,R2) | K | K | K | K | K | K (TS6133, F5) |
| M1 drop the inner try | K (R1) | K | K | K | K | K | K (R1-R3) |
| M2 fallback -> 'x' | K | K | K | K | K | K | K (R1-R3) |
| M3 constant for every value | K (C1,C2,R2) | K | K | K | K | K | K (C1,C2) |
| M4 log the wrong value (`String(error)`) | K (C1,C2,R2) | K | K | K | K | K | K (C1,C2) |
| M5 rethrow when unreadable | K (suite crash, F5) | K* | K* | K* | K* | K* | K (R1-R3) |
| M6 fallback -> undefined | - | - | - | - | - | - | K (R1-R3) |
0 survivors.

## Q6. merge-tree (logs/merge_tree.log, logs/merge_tree_dev2.log)
- Onto 0e3a9b65: 1941 alone rc 0 `f306f8b5`, exactly its 8 paths (SAME_PATHS). 1940 alone rc 0 `27b94184`. Union in both orders rc 0, identical `23fee71f`, paths = 1940 ∪ 1941 (12). 1940 x 1941 directly: rc 0.
- Union run (scripts/union.sh: the union product blobs placed in my clone with PR 1940's 2 tests added; the rest of the tree is the PR head, not develop's other originate files): 6 new-test files 41/41, the whole originate suite 186 files 2204/2204, tsc 0 errors. Restored UNION_RESTORE_OK.
- Develop's move e2a2426d..0e3a9b65: 46 paths, 0 shared with 1941. The later move to 58b5042c: 5 paths, 0 shared. Both are clean (F7).

## Q7. Kam's ks1346 rule
No new log line, no new key and no new message text. 7 existing lines change only the VALUE source of `error`. For unreadable values it is the constant, measured. For readable non-string messages it is `String(message)`, which no longer writes object field values (an improvement). The one shift is an object's own toString text (F4). P3's readable path is unchanged (F2 residual pre-existing). **Compliant.**

## Notes for the PR body
1. G123-F1 (info): the Opus gate's answer to the GATE QUESTION. 500 -> 200 count:0 is accepted, because the registry miss is established before the chain read and every ordinary chain-read failure already answers count:0. Measured through the real v2 routes, anonymous and owner.
2. G123-F3 (recommended): name v1 `verification.ts:698` and `:1243` (`chainErr?.message`) as follow-up KS-1868 sites.
3. G123-F2 (info): the P3 residual is confirmed base == head and has no response disclosure. Give the suggested `String(err.message)` form for the follow-up, and note that an object message's field values reach the console log there.
4. G123-F4 (info): an object message with its own toString now logs that text, and in production the coerced string enters the file log.
5. G123-F6 (info): "81 lines apart" -> the nearest hunks are 8 base lines apart (:1438 vs :1446), no shared line, union clean in both orders (tree 23fee71f at 0e3a9b65; 4ba34fde at 58b5042c).
6. G123-F7 (info): develop is at 58b5042c, 0 shared paths, merge-tree clean.

## NOT TESTED
- The real PR body (no gh auth); real PostgreSQL/Prisma; the real heal; multi-tenant mode (the cross-tenant lookups and their own catches); a real boot; the gateway hop and its limiter; production-mode logger transports (read only); Node 24; the four platform suites; CI; the pre-push hook legs (quoted from the READY mail).
- Whether any value of these shapes can occur in production. All thrown values are synthetic. I found no caller-controlled path that yields one (reasoned from source).
- The author's recorder and their apply-order evidence beyond my own two-order apply.

Processes: every background run I started (install, runs.sh, mutants.py, two wait loops) has exited. `ps` shows 0 gate-123 processes (logs/ps_end.log). Nothing was written into Wednesday's tree outside this workdir (no node_modules/.vite added), and nothing into !CODING.
