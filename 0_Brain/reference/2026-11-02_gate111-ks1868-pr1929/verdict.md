# QA Gate 111 verdict (TIER 1): Secuura/Distributed_Secuura PR 1929 (KS-1868, governance verifyDbReady, O73-P2 only)

## BLUF
**GATE 111 (TIER 1) on PR 1929 at 55cd79e1dc09: GO WITH NOTES. Nothing has to be fixed before merge.**

This is a re-launch: the first run cloned and checked out, then died at ~17:47 AEDT with the coordinator rotation and wrote no verdict. I re-verified its clone (HEAD = pr1929 = 55cd79e1, push URL `no_push_qa_gate`, worktree clean) and re-ran everything below myself.

What I ran:
- the REAL `db.ts` (`initDb` and `runDbReadyHook`, wired exactly as `index.ts` wires them);
- the REAL `governanceService`;
- the REAL governance router and the REAL `@secuura/shared` errorHandler on a loopback HTTP server;
- the REAL winston logger, wrapped call-through so a throw from the logger propagates.

Only the `pg` Pool (a stateful fake) and `console.log` (to capture `dbLog`) were replaced. I ran base and head, each under NODE_ENV test and production: 4 runs x 122 records. A mechanical judge made 360 checks with 0 fails, and fails (rc 1) on two planted tampers.

- **a) The KS-1940 path is byte-identical at base and head.**
  - `createProposal`, `registerParticipant`, `getParticipant`, `dbGetParticipant`, `dbGetParticipantByAddress`, `dbSaveParticipant` and `rowToParticipant` have equal sha256 at base and head. They only move by +6 lines (`let proposer = await dbGetParticipant` is at :501 at base and :507 at head).
  - `routes/governance.ts`, `db.ts`, `index.ts` and `governance.types.ts` are the same blobs at base, head and develop.
  - The product diff is ONE hunk, inside `verifyDbReady`'s catch. Its only caller is `index.ts`'s `initDb` hook, and it touches no participant code.
  - All 99 route records per run are identical at base and head. That includes the KS-1940 overwrite, the 500 and the no-response, measured (G111-F3).
- **b) Unreadable value: ordinary path, no write, no new disclosure.**
  - Covered shapes: revoked Proxy, an Error whose `message` getter throws, and a thrown null-prototype object.
  - At head, `verifyDbReady` resolves and logs exactly one error line: `Failed to seed proposal counter from DB {error:'unreadable thrown value'}`. This equals the ordinary-Error record on every field except the error text.
  - At base it REJECTS with no log of its own, and the boot hook logs `DB ready boot work failed` with the raised TypeError text. For the getter shape, that text is `getter boom`, the getter's own message.
  - Writes in every verifyDbReady record: 0. No response changes.
- **c) Real winston with a hostile NON-string message** (the G108-F1 class): it still crashes, and it is identical to base.
  - An Error whose `message` returns a revoked Proxy makes winston throw `Cannot perform 'get' on a proxy that has been revoked` in both formats. `verifyDbReady` rejects, and at boot `runDbReadyHook` contains it. This is the same at base and head.
  - Symbol, toString-throws and null-proto messages log `{}` and resolve, identically at base and head.
  - Not a regression (G111-F1, recommended follow-up).
- **d) Outbound network: none to disclose.**
  - The governance service has no outbound HTTP client (read), `pg` was replaced, and `DATABASE_URL` pointed at 127.0.0.1:1.
  - The connect guard recorded only loopback targets: 33 connects per run, outbound `[]` (G111-F7 caveat).
- **e) Byte-identity, mutants, suite, merge-tree:**
  - The held O73-P2 patch applies strictly at 968f1707 and yields the PR's exact blobs: svc `813622b8`, test `ff466dfe`. The product +/- lines are byte-equal (8 lines). The evidence copy equals the canonical `patch.diff` (cmp).
  - Mutants: 8 of 8 killed; 1 extra mutant survives (G111-F2).
  - Suite: 12 files / 194 at base, 13 / 197 at head, 0 failed.
  - Develop MOVED during the gate to `c2c2e03a` (PR 1927 merged). The merge-tree onto it is clean, changes exactly the PR's 4 paths, and shares 0 paths with develop's move.

## 1. Heads + diffstat (logs/head_start.log, head_start2.log, head_end.log, diffstat.log)
- **PR head:** `55cd79e1dc096b24a0ce56dc68d8beb41f7ebc7d` at the first run's start (06:43:52Z), at my restart (06:52:14Z) and at END (07:01:12Z). Unchanged.
- **Develop:** `829233f1a388` at 06:43Z and 06:52Z, and **`c2c2e03afdb3` at 07:01Z**. The move is "nft verifier answers an unreadable throw...", i.e. PR 1927 merged.
- **Commit:** one commit, parent `968f17070208` (= merge-base), author Kam Kreiser <kamil.kreiser@secuura.ai>, subject "Refs KS-1868: governance counter seed logs a constant on an unreadable throw". "Refs" only, no close word. The body names the held sibling as "KS 1940", so the PR does not attach to it.
- **Three-dot diff vs 968f1707:** exactly 4 files, **+101/-1**, as claimed. One M, three A, all mode 100644.
  - `governanceService.ts` 7/1
  - the new test 54/0
  - the flow fragment 21/0
  - the cheat fragment 19/0
- **Byte-identity to the held pass** (logs/held_vs_pr.log from the first run, re-run by me in logs/held_vs_pr_rerun.log):
  - `git apply --cached` of evidence/o73_p2_patch.diff on a temporary index of 968f1707 gives rc 0. The blobs are svc `813622b8`, test `ff466dfe`, equal to the PR's.
  - The patch equals the concatenation of the two sections, and equals the canonical `local-model/runs/...o73_p2.../out.md.checker/patch.diff`.
  - The product `-`/`+` lines of the PR's hunk are byte-equal to section 1's (8 lines, cmp rc 0).
  - The first run's control: a corrupted context gives `patch does not apply` (rc 1).
  - So there is no hand edit in code. The fragments are the author's own.
- **PR body:** NOT read (no Secuura gh auth on this host). I used the READY and BUILT mails (evidence/).

## 2. The hunk
`verifyDbReady` catch (base :390):
- **Before:** `logger.error('Failed to seed proposal counter from DB', { error: err instanceof Error ? err.message : String(err) });`
- **After:** `let reason: string; try { reason = <same expression>; } catch { reason = 'unreadable thrown value'; }`, then the same log call with `{ error: reason }`.

A readable value takes the identical expression, so it produces the identical log line. The try path (the SELECT, the counter assignment, the info line) is unchanged. So is the `isDbAvailable` warn branch. No other line in the file changes.

## 3. Behaviour (scripts/g111_probe.test.ts, runprobe.sh, short.py, judge.py; logs/probe_{base,head}_{test,production}.jsonl, short.txt, routes_table.txt, judge*.log)
HOW:
- jest 29 / ts-jest (lockfile). Fresh module registry per scenario.
- `pg` Pool replaced by a stateful fake:
  - participants table with upsert-by-id and DELETE;
  - proposals recorder;
  - `SELECT 1` ok;
  - `MAX(proposal_number)` returns 7 or throws the scenario value;
  - participant-by-id lookup can be made to throw.
- Real `initDb(() => verifyDbReady())`, then a direct `verifyDbReady()`, then 9 HTTP steps on the real router.
- 11 seed scenarios: none, ordinary Error (message carrying an IP and `password=`), revoked Proxy, getter-throws, null-proto, plain string, undefined, plus message = revoked Proxy / Symbol / toString-throws / null-proto.

verifyDbReady (identical under both logger formats):

| seed value | base direct | base boot | head direct | head boot | writes |
|---|---|---|---|---|---|
| none | resolves, info "counter seeded" | ok | same | same | 0 |
| ordinary Error | resolves, error line with message | error line | same | same | 0 |
| revoked Proxy | **rejects** TypeError, no own log | dbLog "DB ready boot work failed" (TypeError text) | resolves, error line `unreadable thrown value` | same, no dbLog | 0 |
| message getter throws | **rejects** `getter boom` | dbLog with `getter boom` | resolves, constant | same | 0 |
| null-proto object | **rejects** "Cannot convert object to primitive value" | dbLog | resolves, constant | same | 0 |
| plain string / undefined | resolves, logs the string / "undefined" | same | same | same | 0 |
| message = revoked Proxy | rejects (winston throws) | dbLog | **same as base** | **same as base** | 0 |
| message = Symbol / toString-throws / null-proto | resolves, logs `{}` | same | same | same | 0 |

- **Judge** (360 checks, 0 fails, rc 0), per logger format:
  - all 99 route records equal at base and head;
  - every non-unreadable boot and direct record equals at base and head;
  - head unreadable (revoked, getterThrows, nullProto) == head ordinary on every field with the error text masked;
  - the head log is exactly one error line with keys `['error']` and the constant;
  - the base direct rejects, and the base boot has the "boot work failed" line;
  - 0 writes in any verifyDbReady record;
  - R3's proposalNumber is 8 when seeded and 1 when unseeded, at base and head alike (so the counter is unseeded either way, as claimed);
  - no outbound connect.
- **Tamper controls:**
  - head R5 participant stake altered: rc 1, 1 fail;
  - head direct getterThrows set to rejected: rc 1, 1 fail.
- **Run vs read.** RUN: db.ts boot hook, service, router, errorHandler, winston (dev printf format and production json). NOT run: the `index.ts` process itself, real pg, auth middleware (a stub sets `req.user`).
- **jest status.** The probe's jest run reports rc 1 at BOTH base and head. The reason is that step R8 (GET `/participants/:id` with an unreadable lookup) leaves an unhandled rejection, which jest attributes to the test. Every record was written (122 per run).

## 4. KS-1940 path (key question a) — measured, unchanged
From logs/routes_table.txt, which is identical at base and head for every seed scenario:
- **R5, `POST /proposals` as an existing proposer whose by-id lookup fails with an ordinary Error:** 201. The proposer's row is overwritten: stake 99999 → 1000, `is_drep` true → false, vote_power 777 → 1000. This is the KS-1940 defect, present at base and identical at head.
- **R6, same with a revoked-Proxy lookup:** 500 INTERNAL_ERROR with 0 writes. The unguarded `dbGetParticipant` catch throws.
- **R8, GET `/participants/user-B` with a revoked-Proxy lookup:** NO RESPONSE (1.5 s client timeout). The route has no catch.

This PR touches none of these. Merging O73-P1 (routing unreadable lookups into "not registered") would move R6 onto R5's overwrite. That is why O73-P1 must stay held until KS-1940 is fixed. The author's hold is correct.

## 5. Re-measure (Node v26.8.1; NOT measured on Node 24)
- **Install:** `npm ci --ignore-scripts` in the governance service gave rc 0. `packages/shared` was installed and built (rc 0) and symlinked as `node_modules/@secuura/shared` inside the clone.
- **Red-first** (logs/red_base.json): head test file against base product gives C1 passed, **R1 and R2 failed by assertion** (`Received promise rejected instead of resolved`, rejected with the read's own TypeError / `getter boom`). Head: 3/3 pass.
- **Suite** (logs/suite_base.json, suite_head.json):
  - base (968f1707 product = develop's at both 829233f1 and c2c2e03a, sha `2346aba1`; new test absent): **12 files, 194 tests, 194 pass, 0 fail**;
  - head: **13 files, 197 pass, 0 fail**.
  - Matches the author.
- **tsc:**
  - plain config at head: rc 0;
  - with tests (scripts/tsconfig.tests.json, 13 test files in the program): rc 0 with 0 errors at head, and rc 0 with 0 errors at base;
  - a planted file gives rc 2 with TS2322 and TS6133.
- **eslint** (Dev flat config; Dev node_modules borrowed by symlink from gate 110's clone, whose lockfile and eslint config sha are identical; the symlink was moved to scripts/_quarantine afterwards):
  - the 2 changed .ts files: **0 errors, 0 warnings**;
  - planted file: rc 1 (no-debugger, unused var).
- **docs-fragments** (scripts/frag.sh, logs/frag_run.log):
  - clean run: rc 0, "flow 117 legacy + 78 new, cheat 112 legacy + 78 new; lint clean, render passes";
  - 4 planted defects (unclosed div in each fragment, `<!--n-->.` removed from flow, `</table>` corrupted in cheat) each give rc 1;
  - restored by sha, then rc 0;
  - the one ADVISORY (cheat :6235) is develop's own.
- **Pre-push hook** (13/16 legs, PREFLIGHT INCOMPLETE) and CI are the author's; not re-run.

## 6. Mutants (scripts/mutants.py, mutants_extra.py; logs/mutants.log, mutants_extra.log; product only, test untouched, sha256-restored each time, RESTORE_OK 6b0f364b6f4a, worktree clean)

| mutant | red cells |
|---|---|
| undo guard (base line) | R1 R2 |
| fallback rethrows | R1 R2 |
| wrong constant `'x'` | R1 R2 |
| always constant (read dropped) | C1 |
| fallback reads the value (`String(err)`) | R1 R2 |
| log call dropped | C1 R1 R2 |
| logged at warn | C1 R1 R2 |
| meta key renamed `{ reason }` | C1 R1 R2 |

8/8 killed. **Extra:** guarding only `instanceof` and `.message` while leaving `String(err)` unguarded **SURVIVES** (G111-F2).

## 7. merge-tree (logs/mergetree.log, mt_paths.log, dev_paths.log, pr_paths.log, develop_moved.txt)
- Develop was re-read at END by ls-remote: `c2c2e03afdb3`. I fetched it and ran `git merge-tree --write-tree c2c2e03a pr1929`: rc 0, tree `dc957c5b`. The earlier attempt onto the stale `829233f1` was also clean, tree `20226e60`.
- The result vs develop changes exactly the PR's 4 paths (SAME_PATHS), +101/-1. The merged `governanceService.ts` = the PR's blob `813622b8`.
- Develop's 21 paths past the base share **0** paths with the PR (control: 21). No governance file is among them. routes, db and index are the same blobs in develop and in the merged tree.
- The probe and the fragments check were not re-run on the merged tree (read only).

## 8. Kam's ks1346 logging rule
- The changed line logs only the constant under the field name `error` when the value is unreadable. No thrown value reaches a log or a response in that case.
- At base, the boot hook's dbLog carried the read's own error text (e.g. the getter's `getter boom`). At head that line is not produced. So head discloses LESS.
- **Pre-existing, unchanged, not this PR's:** for a readable value the line still logs the message VALUE (the probe's `db down at 10.0.0.7 password=hunter2` appears verbatim at base and head). The same applies to `db.ts`'s `err?.message`. This is a value, not a field name (G111-F4).

## 9. FINDINGS
- **G111-F1 (RECOMMENDED follow-up, not FIX-BEFORE-MERGE; measured).** A hostile non-string `message` is not coerced, because `reason` holds whatever the getter returned.
  - With an Error whose `message` returns a revoked Proxy, the REAL winston throws while formatting (both formats). `verifyDbReady` rejects, and at boot `runDbReadyHook` contains it.
  - Identical at base and head. 0 writes, no response affected. Symbol / toString-throws / null-proto log `{}` and resolve, also identical.
  - Follow-up (PR 1924's form): `reason = String(err instanceof Error ? err.message : err);` inside the same try, plus a cell for it.
  - The author's cells stub the logger, so they cannot see this.
- **G111-F2 (RECOMMENDED; measured).** No committed cell pins the `String(err)` branch. A thrown null-prototype object is the shape that reaches it; my probe shows head handles it (constant, resolves) where base rejected. A mutant that leaves `String(err)` unguarded survives the 3 cells. Suggest a null-proto cell.
- **G111-F3 (INFO; measured).** KS-1940 is real and unchanged by this PR:
  - an ordinary lookup failure lets `createProposal` overwrite an existing proposer's stake, DRep flag and vote power (201);
  - an unreadable lookup gives 500;
  - GET `/participants/:id` on an unreadable lookup never answers.

  All of this is identical at base and head. O73-P1 must stay held until KS-1940 is fixed.
- **G111-F4 (INFO, pre-existing).** Readable thrown values still log their message VALUE (service and db.ts), against the ks1346 names-not-values card. Unchanged here; the new constant complies.
- **G111-F5 (INFO).** Develop moved during the gate (829233f1 → c2c2e03a, PR 1927 merged). The author's mail predates it. The merge-tree onto c2c2e03a is clean with 0 shared paths.
- **G111-F6 (INFO, doc accuracy).** The fragments say initDb's handling of a rejecting hook was "read from db.ts, not run". This gate RAN the real `initDb`/`runDbReadyHook` and confirms it: base logs "DB ready boot work failed", head logs the constant and does not reach the hook's catch. The fragments' figures (2 of 3 red, 194 → 197, 0 failed) match mine.
- **G111-F7 (INFO, probe caveat).** The connect guard attributed every target as loopback (`localhost`, 33 connects per run, outbound `[]`). Its host extraction is coarse, so the stronger evidence is structural: the governance code has no outbound client, `pg` was replaced, and `DATABASE_URL` was 127.0.0.1:1. No external URL was contacted to my knowledge, and there is nothing to disclose.
- **No FIX-BEFORE-MERGE item.**

## 10. NOT TESTED
- The live PR body, the Linear tickets (KS-1868, KS-1940), CI, the pre-push legs, and Node 24.
- Real PostgreSQL. SQL was matched by a fake; I did not check whether the real table has a unique constraint on wallet_address.
- A real `index.ts` process boot, and the auth middleware (a stub set `req.user`).
- The probe and the fragments check on the merge-tree result (read only; 0 shared paths).
- Whether a real pg driver can throw any of these values (all values are synthetic).
- The author's own recorder and judge (not in evidence; I built my own).
- The jest `unhandledRejection` count for R8. Jest intercepts it, so my counter reads 0 and the effect shows only as NO_RESPONSE plus the jest failure, at both base and head.
- Mutant forms beyond the 8 + 1 listed.
