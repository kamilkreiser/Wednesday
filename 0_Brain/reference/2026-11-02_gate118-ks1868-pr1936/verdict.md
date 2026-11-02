# QA Gate 118 verdict: Secuura/Distributed_Secuura PR 1936 (KS-1868, originate routes/signatories.ts nominate + routes/thirdPartyVerifiers.ts register / approve catches, held passes O77-P2 / O77-P3), TIER 1

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.**
- **What I ran:** the REAL nominate (`POST /api/signatories/`), register (`POST /api/third-party-verifiers/register`) and approve (`POST /api/third-party-verifiers/:id/approve`) handlers on a real loopback listener, with only prisma replaced by a statement recorder (full SQL text + values per statement), auth and logger stubbed, uuid fixed. Grid: 3 routes x 12 thrown values x 2 failure points (the INSERT/UPDATE rejects; a throw AFTER the write succeeded, injected through `logger.info`) plus a success control and approve's 0-rows control: 76 cells per version, base and head (scripts/g118_probe.test.ts, scripts/judge.py, logs/probe_{base,head}.json, logs/probe_table.log).
- **Comparator: 436 of 436 checks pass** (logs/judge.log). Every unreadable shape at head equals what an ordinary Error (no code) gets at base AND at head: status, body, statements, key issued / not, unhandled = 0. Every readable value (Error, Error+23505, Error+other code, string) and every control is byte-identical base vs head, log lines included.
- **The code question (Q2): confirmed.** A real 23505 path is byte-identical base vs head at both failure points on all three routes (409 at nominate/register with nothing logged; 500 at approve, which never reads `.code`). No unreadable shape newly produces 409, and none loses a 409 an ordinary 23505 gets: an Error with a readable code 23505 and a throwing message getter answers 409 at both versions (the message is never read on that path).
- **Persisted state (Q3): confirmed.** Exactly one statement in every one of the 152 cells, SQL and values identical base vs head; the catch issues nothing.
- **G104-F3 (Q4): unchanged, base = head;** head newly loses no key (the only cell that returns a key, success, returns it at both versions with sha256(key) = the hash written).
- **Re-measure:** red-first 6/14 (each by assertion), green 14/14 three runs, whole originate suite 180/2163 -> 182/2177 with 0 vanished, 14 new, 0 changed; tsc incl. tests 0 -> 0; eslint 0; docs-fragments clean + 4 planted defects caught; merge-tree clean onto develop at commission AND at end (develop moved).
- **Mutants: 32 of 32 killed** (28 by assertion in the site's own cells, 4 rethrow mutants by a crash of the site's own test file, G118-F6). The readable-non-Error branch is pinned this time (C1/C2 kill Mr5 at every site).

## Heads
- START (logs/head_start.log, 2026-11-02T08:50:11Z): PR head `28c0669169abed3522b0f288c35b8a3d1f693c88` (matches the commission), develop `91ccb1553f027c712d0d0c2d93871fd46f67dffa` (matches). One commit; its parent = merge-base = `8f313815f415c65849210f5d3e30cae44d15a516` (matches the claimed base).
- END (logs/head_end.log, 09:07:14Z): PR head `28c06691...` **unchanged**; local HEAD the same; working tree clean; both product blobs equal the PR blobs. **develop MOVED** to `c70f339063eedd6ee5d937f4a79274c464091866`, one commit, `c70f3390 Refs KS-1938: retention sweep ...` (= PR 1935, gdprService.ts + its test + 2 fragments). It touches none of this PR's paths; merge-tree re-run onto it (Q6).
- Both product files are byte-identical at 8f313815 and 91ccb155 (git diff --quiet rc 0), so "base" is the same file whichever is meant.
- Diffstat (logs/diffstat.log, three-dot): **6 files, +356/-5, exactly as claimed**: signatories.ts +14/-2, thirdPartyVerifiers.ts +21/-3, two new tests (+137, +146), flow fragment +20, cheat fragment +18. Nothing outside the declared paths (logs/names.log).
- **PR body not read directly** (no gh login for Secuura used). Worked from the author's READY mail (evidence/e28_ready_pr1936.txt), the commit message (evidence/commit_msg.txt) and the two fragments.

## FINDINGS
- **G118-F1 (INFO, measured, not stated by the author)** A thrown `null` (or `undefined`) at nominate and register: base reads `error.code` on null, the catch throws, **NO ANSWER** + a rejected handler promise; head answers the ordinary 500 and logs `{"error":"null"}` (String(null)), i.e. what a thrown string gets. Approve already answered 500 / "null" at base (it never reads `.code`). Head is no worse; worth one line in the PR body's behaviour section.
- **G118-F2 (INFO, pre-existing, base = head; read from the installed runtime, NOT run)** In single-tenant mode (`MULTI_TENANCY_ENABLED` not true) `prisma` is a Prisma 7 client with `@prisma/adapter-pg`. Its adapter maps pg 23505 to `UniqueConstraintViolation` (node_modules/@prisma/adapter-pg/dist/index.js:472) and the client surfaces raw-query driver errors as `PrismaClientKnownRequestError` code `P2010` / `P2002`, not `'23505'`. So the 409 branch at nominate/register looks reachable only on the multi-tenant pg pool proxy (`req.db`, index.ts:226-235), where node-postgres puts `code: '23505'` on the error. A duplicate nomination/registration in single-tenant mode would then answer 500 and log the Prisma message. Not this PR's change; a card candidate if confirmed against a real Postgres.
- **G118-F3 (INFO, pre-existing G104-F3, measured, base = head)** Approve, a throw after the UPDATE (cell `approve | after`): the UPDATE is issued once (status 'active' + api_key_hash written), the answer is 500 with no key, for an ordinary Error at both versions. For an unreadable value base gave NO ANSWER (key also lost, connection hung until the client gave up) and head gives the same 500 an ordinary Error gets. The success cell returns the key at both versions and sha256(key) equals the hash in the recorded UPDATE. **The head does not newly lose a key any ordinary path returns.**
- **G118-F4 (INFO, pre-existing, synthetic, base = head)** A 23505-coded value thrown AFTER a successful INSERT (cell `after | error23505`) answers 409 "already ..." though the row was written. Only reachable if something after the INSERT (the info log, the response build) throws a code-23505 value; not plausible in practice. Recorded for completeness.
- **G118-F5 (LOW, test gap)** No committed cell throws an Error whose CODE getter throws while its message is readable (the one shape where head logs the message, not the constant), and none throws a readable-code 23505 with an unreadable message. Both are pinned only by this gate's uncommitted probe (logs/probe_table.log rows `codeGetterThrows*`, `code23505MsgThrows`). Optional: one cell each at nominate or register.
- **G118-F6 (INFO, measured)** The rethrow mutants (Mc3 "code catch rethrows", Mr3 "rethrow when unreadable") are killed by a crash of the site's own test file (`TypeError: Cannot perform 'IsArray' on a proxy that has been revoked`: jest cannot format a revoked-Proxy rejection), not by a named red cell. Still red, still confined to that file. Likewise each red-first cell at base reports the handler's TypeError as a second failure message beside its assertion.
- **G118-F7 (INFO, ks1346, pre-existing)** The readable branch still logs `String(error)` (name + message), which for a pg or Prisma error carries the driver message text (a Prisma P2010 message embeds the database message). That is a value, not the rule's type + field names form; it is unchanged base = head and the same shape as every other catch in both files. The one new constant `'unreadable thrown value'` complies.
- **G118-F8 (INFO, wording)** The flow fragment lists "an Error whose code getter throws" among the values that "is logged as the constant"; at nominate/register that shape logs `String(error)` (the readable message), as the READY mail correctly says. The fragment's line numbers (:126/:132, :103/:109, :199) are base lines. The fragment's own per-file counts (+14/-2, +21/-3) are correct.
- **G118-F9 (INFO)** docs-fragments `check` prints the pre-existing cheat ADVISORY at line 6235 (same as G90-F7 / G117-F7), not this PR.

## Q1. Response, log, persisted state per route (in full; run, not read)
**Code (head).** Nominate (signatories.ts:58-147) and register (thirdPartyVerifiers.ts:52-124): validation, then one `$executeRaw` INSERT, `logger.info`, `res.status(201).json`. Catch: `code` read in its own try (unreadable -> undefined), `code === '23505'` -> 409, else `String(error)` in its own try (unreadable -> constant), `logger.error`, 500. Approve (:166-220): `generateApiKey`, one UPDATE ... `WHERE id = $ AND status = 'pending'`, 0 rows -> 404, `logger.info`, 200 with `apiKey`. Catch: `String(error)` guarded, log, 500. Approve never reads `.code` (source + probe: Error+23505 at approve = 500 both versions).

**Grid result** (logs/probe_table.log; "point db" = the INSERT/UPDATE rejects, "after" = the write succeeded and the next step throws):

| thrown value | nominate / register, base | nominate / register, head | approve, base | approve, head |
|---|---|---|---|---|
| Error (no code) | 500, log `Error: db down` | same | 500, log `Error: db down` | same |
| Error code 23505 | **409**, nothing logged | **409**, nothing logged (identical) | 500, log `Error: db down` | same |
| Error code 23503 | 500, log message | same | 500 | same |
| string | 500, log the string | same | 500 | same |
| null | **NO ANSWER**, handler rejected | 500, log `null` (G118-F1) | 500, log `null` | same |
| revoked Proxy | NO ANSWER | 500, log constant | NO ANSWER | 500, log constant |
| message getter throws (Error / revoked Proxy) | NO ANSWER | 500, log constant | NO ANSWER | 500, log constant |
| CODE getter throws (Error / revoked Proxy), message readable | NO ANSWER | 500, log `Error: db down` = the ordinary Error's log exactly | 500, log `Error: db down` | same (base = head) |
| code 23505 readable + message getter throws | 409 | 409 (identical) | NO ANSWER | 500, log constant |
| Symbol.toPrimitive throws | NO ANSWER | 500, log constant | NO ANSWER | 500, log constant |
| control: success | 201 | 201 | 200 + key | 200 + key |
| control: approve 0 rows | | | 404 | 404 |

The same holds at both failure points. Unhandled (rejected handler promises, observed by wrapping each route handle without changing it): **38 at base, 0 at head**. Response bodies at head for every 500 are the existing constant `{"success":false,"error":{"code":"INTERNAL_ERROR","message":"Failed to ..."}}`.

**Acceptability:** every unreadable after-state equals what an ordinary Error (no code) already gets: judge checks B (head == base-Error and == head-Error on status, body, statements, key, unhandled) 0 failures.

**Reachability:** the rejection value is whatever Prisma / node-postgres rejects with (Error subclasses with data `message`); the parameters are validated request strings and server-built values; no caller chooses the thrown object. Defence-in-depth, as at every other KS-1868 site. All thrown values here are synthetic.

## Q2. The code question
- 23505 byte-identical base vs head: judge checks A cover `error23505` at both points on all three routes (status, body, statements, logs): 0 failures.
- No unreadable shape newly 409: check B2 (every unreadable cell at head != 409): 0 failures. The only way head reaches 409 is `code === '23505'` read successfully, the same single read base does (one `.code` read in both; a getter with side effects sees the same count).
- No 409 lost: the only shapes that can carry a readable 23505 are the readable ones and `code23505MsgThrows`; all answer 409 at both versions at nominate/register. A thrown value whose code read throws cannot carry 23505 at base either (base's catch threw before answering).
- Approve never reads `.code`: confirmed in source (only `String(error)` in its catch) and measured (23505 -> 500 both versions).
- Pre-existing beside it: G118-F2 (Prisma mode may never produce `'23505'`).

## Q3. Persisted state
- The recorder logs every `$executeRaw`/`$queryRaw`. Check C: **exactly 1 statement in every cell at both versions, SQL text and values identical base vs head** (Dates and the api-key hash normalised): 228 checks, 0 failures. No catch issues a statement; no compensation or rollback exists in any of the three handlers (all autocommit). The author's claim re-measures.

## Q4. G104-F3 (approve key loss)
See G118-F3. Unchanged base = head for an ordinary Error; for an unreadable value head moves NO ANSWER -> the ordinary 500; in both the key was never sent. The head changes nothing about which paths return the key.

## Q5. Re-measure (Node v26.8.1 only; nothing measured on Node 24; load1 ~10-14, shared host)
- **Green, head, the two new files:** 14/14, three runs (logs/green_head_{1,2,3}.json).
- **Red-first, base products + new files:** 6 failed, 8 passed, rc 1 (logs/red_base.json): R1 + R2 on each of nominate, register, approve; each has an `expect(received).toEqual` failure (plus the handler's TypeError as a second message, G118-F6). C1-C3 pass. No compile or import error.
- **Whole originate jest** (logs/suites.log): base without the new files 180 files 2163/2163; head 182 files 2177/2177; per cell 0 vanished, 14 new, 0 changed. The author's figures re-measure exactly.
- **tsc:** plain rc 0 both; scratch config with tests 0 errors both (originate src files 243 -> 245; the author's 271 -> 273 uses another config, delta +2 agrees); planted control TS2322 + TS6133 rc 2, restored byte-identical. Leg 16 does not cover originate (author's statement, not re-run).
- **eslint:** the 2 products + 2 new tests, 0 problems rc 0; planted file `no-debugger` error + unused warning rc 1.
- **docs-fragments** (logs/frag_outer.log): rc 0 "flow 117 legacy + 80 new, cheat 112 legacy + 80 new"; planted defects flow unclosed div, flow `<!--n-->.` removed, cheat unclosed div, cheat `</table>` corrupted: each rc 1; all restored by sha; rc 0 after.
- **Quoted, not re-run:** the pre-push hook "PREFLIGHT INCOMPLETE 13/16, nothing failed"; the author's 60/60 recorder (superseded by this gate's 436-check grid).

## Q6. Mutants (scripts/mutants.py; product only, tests untouched, both new files each run, sha256 restored after every run, all `restore True`; logs/mutants_table.log)
32 runs: **32 KILLED**, each only in its own site's file.

| Mutant | S1 nominate | S2 register | S3 approve |
|---|---|---|---|
| M0 revert to base | KILLED R1 R2 | KILLED R1 R2 | KILLED R1 R2 |
| Mc1 drop the code try | KILLED R1 | KILLED R1 | n/a |
| Mc2 unreadable code -> '23505' | KILLED R1 | KILLED R1 | n/a |
| Mc3 code catch rethrows | KILLED (file crash) | KILLED (file crash) | n/a |
| Mc4 409 check removed | KILLED C3 | KILLED C3 | n/a |
| Mr1 drop the reason try | KILLED R1 R2 | KILLED R1 R2 | KILLED R1 R2 |
| Mr2 fallback -> String(error) | KILLED R1 R2 | KILLED R1 R2 | KILLED R1 R2 |
| Mr3 rethrow when unreadable | KILLED (file crash) | KILLED (file crash) | KILLED (file crash) |
| Mr4 constant for every value | KILLED C1 C2 | KILLED C1 C2 | KILLED C1 C2 |
| Mr5 readable branch -> 'x' | KILLED R1 R2 C1 C2 | same | same |
| M7 log removed | KILLED R1 R2 C1 C2 | same | same |
| M8 no 500 sent | KILLED R1 R2 C1 C2 | same | same |

## Q7. merge-tree
- Onto develop at commission `91ccb155` (logs/merge_tree.log): rc 0, tree `5ef294a4db28...`, clean; merged tree differs from develop in exactly the PR's 6 paths, +356/-5 (SAME_PATHS); the 4 code/test blobs equal the PR blobs. 0 of the 55 paths develop changed since the base are shared with the PR.
- Onto develop at end `c70f3390` (logs/merge_tree_end.log): rc 0, tree `a68940c1293b...`, clean, 6 files +356/-5, SAME_PATHS.
- docs-fragments not run on the merged tree (the PR's fragments are new files with unique names).

## Q8. Kam's ks1346 logging rule (type and field NAMES, never values)
- New log content: the constant `'unreadable thrown value'` only. Compliant.
- The code-getter-only case at nominate/register logs `String(error)` = `Error: <message>`. Measured equal to the ordinary Error's log at base for the same message (judge check B3 on all four `codeGetter*` cells x 2 points: 0 failures). It is the existing readable-branch content, not a new disclosure. That existing content is itself a value (G118-F7), pre-existing, base = head.

## Q9. Notes for the PR body
- G118-F1: add the thrown-null row (NO ANSWER -> 500, log "null") to the behaviour section.
- G118-F2: card candidate: is 409 reachable in Prisma (single-tenant) mode at all? Pre-existing.
- G118-F3: G104-F3 confirmed unchanged by measurement; head newly loses no key.
- G118-F5: optional cells for the code-getter-only shape and readable-23505 + unreadable message.
- G118-F8: fragment wording for the code-getter shape; line numbers are base lines.
- None is FIX-BEFORE-MERGE.

## NOT TESTED
- the real PR body text
- a real PostgreSQL (statements recorded by a stand-in; Prisma's real error class for 23505 read from the runtime source, not raised)
- a booted originate, the gateway hop, the real auth middleware (stubbed), the multi-tenant `req.db` path
- the process-level `unhandledRejection` handler (index.ts:75) at base: the probe observed rejections at the handler instead
- Node 24; the four platform suites; CI; the pre-push hook legs (quoted only); the Linear ticket text
- docs-fragments on the merged tree
- whether an unreadable thrown value is reachable in production (reasoned, not measured)

## Tier
**TIER 1 confirmed.** Register creates a verifier record and approve activates it and issues a one-time API credential (the key exists only in the 200 response); the changed catches decide the answer on those credential paths, and nominate grants signing authority. The change alters status codes (NO ANSWER -> 500) on an authority/credential path, so the Opus gate applies.
