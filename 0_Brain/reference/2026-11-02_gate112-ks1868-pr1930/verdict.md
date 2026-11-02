# QA Gate 112 verdict (TIER 1): Secuura/Distributed_Secuura PR 1930 (KS-1868, services/security index.ts + db.ts, nine catches)

## BLUF
**GATE 112 (TIER 1) on PR 1930 at 3b2dd7cb05a9: GO WITH NOTES. Nothing has to be fixed before merge.**

Measured with the REAL app (real routes, real auth middleware, real shared `errorHandler`), the REAL `db.ts` and shared `queryWithTenantGuc`, and the REAL winston logger in both formats (dev printf and production json). Only `pg` was replaced, by a recording Pool that stages writes per transaction and applies them on COMMIT. Base (cd9c4a7) and head, 11 route cells x 11 thrown-value kinds x 2 formats = 488 records, plus 36 db.ts records.
- **Fail closed holds everywhere (Q a).** In no record, at base or head, does validate answer `valid:true` except an ACTIVE key whose usage write failed (the KS-888 card-3 ruling, identical to an ordinary Error). Mint never issued a key or stored a row. Revoke never reported success while the stored row stayed active, and the key validated `Key revoked` afterwards in every revoke cell. A stored-revoked key was refused with **0 usage-write attempts** in every kind. A failed stored-state read answered 503, never `valid:true`.
- **Head unreadable == head ordinary (Q b)** on status, body, persisted keys/audit/events, cache, usage attempts, committed writes, unhandled and uncaught, at every site, with one disclosed exception (G112-F2, base == head). Ordinary, ordinary-08006 and plain-string records are identical base vs head (no regression).
- **The only status change for a readable-code value:** an Error with SQLSTATE 08006 and a throwing `message` getter moves 500 -> 503 on mint and revoke, equal to the ordinary 08006 Error. The STOP CHECK did not fire. No key issued; revoke stays in-memory only, as for the ordinary one.
- **Judge:** 990 checks, 0 fails (logs/judge.log). Four planted tampers (valid:true on a failed stored read, key issued on a failed mint, revoke success without persisting, a usage write on a revoked key) each give rc 1.
- **Held passes:** the five held O74 Spark outputs, applied strictly at cd9c4a7, give blobs byte-identical to the PR for every file under services/security/src (index.ts e4d5beac, db.ts 22177891, five tests). Corrupted-context control: rc 1.

The residual is G109-F1's shape again: a hostile NON-string `message` (a getter returning a revoked Proxy; a BigInt under the dev format) makes the REAL winston logger (and db.ts's `JSON.stringify` dbLog) throw, so validate and resolve stay unanswered with an unhandled rejection. Identical at base and head, still fail closed (G112-F1, recommended follow-up).

## 1. Heads + diffstat (logs/head_start.log, head_end.log, fetch.log, fetch_end.log)
- PR head `3b2dd7cb05a9b9ff516d6851b3a1250df4e4753d` at START (07:02:48Z) and END (07:26:09Z): unchanged. One commit, parent = merge-base `cd9c4a7dd3b8`, author Kam Kreiser <kamil.kreiser@secuura.ai>, "Refs KS-1868: ...", no close words.
- Diff vs merge-base: exactly 9 files, +967/-9, all 100644. M: `db.ts` (+14/-2), `index.ts` (+49/-7). A: five `ks1868-security-*` tests, one flow and one cheat fragment. Matches the READY mail.
- Develop: `c2c2e03afdb3` at START (as briefed); **`c234c2388a16` at END** (one more commit, "Refs KS-1868: admin routes answer an unreadable throw...", not security). See section 6.
- PR body NOT read (no Secuura gh auth here); used the READY and BUILT mails (evidence/).

## 2. The hunks (logs/product.diff)
Nine sites. Eight are the same 6-line guard `let reason: string; try { reason = err?.message; } catch { reason = 'unreadable thrown value'; }` followed by the unchanged log call with `err?.message` -> `reason`:
- db.ts `runDbReadyHook` (dbLog), `probeDb` (returned `error`).
- index.ts `dbSaveAuditLog`, `dbSaveSecurityEvent`, `dbSaveApiKey` (the `if (opts.rethrow) throw err;` after it is unchanged), `dbRecordApiKeyUsage`, validate stored-state read (still `return 503`), validate cache-miss lookup (still falls through to `Key not found`).
- admin-scopes GET: `error instanceof z.ZodError` moved into a try; if `instanceof` throws, `return next(new Error('unreadable thrown value'))`.
- **Proof of inventory:** applying the eight "revert guard" mutants cumulatively plus the S7 revert reproduces the base index.ts and db.ts byte-for-byte (scripts/mutants.py dry run). Nothing else in the product changed.
- Unchanged: levels, messages, field names, every response, the rethrow, the KS-888 classifier.

## 3. Behaviour: real routes, persisted-state recorder (scripts/g112_probe.test.ts, probe.sh, judge.py; logs/g112_probe_{base,head}_{test,production}.jsonl)
HOW: vitest 4.1.12, `SECURITY_DISABLE_BOOT=1`, real app on a loopback listener, real RS256 `super_admin` token. `initDb()` positive control true at every run. The REAL `utils/logger` was created under the requested NODE_ENV (test -> dev printf format, production -> json), then NODE_ENV restored before the app loaded; its transport `log` was wrapped call-through only to capture lines. Kinds: ordinary, ordinary+08006, revokedProxy, getterThrows, getterThrows+08006, nullProto, plainString, msgSymbol, msgRevokedProxy, msgBigInt, msgToStringThrows.

Key cells (dev format; production identical except msgBigInt, see section 4):

| cell (failing statement) | ordinary base=head | unreadable BASE | unreadable HEAD |
|---|---|---|---|
| mint (INSERT) | 500 no key, 0 rows | 500 no key | 500 no key, constant logged |
| mint, code 08006 | 503 | getterThrows: **500** | **503** (= ordinary) |
| revoke (upsert) | 500, row active, mem revoked, then `Key revoked` | same | same, constant logged |
| revoke, code 08006 | 503 | getterThrows: 500 | 503 |
| validate stored read (cached) | 503 | **no answer + 1 unhandled** | 503, 0 usage writes |
| same, key revoked in memory | 503 | no answer | 503 |
| validate lookup (miss) | 200 `Key not found` | no answer | 200 `Key not found` |
| validate usage write (active key) | 200 valid:true, 1 attempt, usage not persisted | no answer | 200 valid:true (G112-F3) |
| validate stored-REVOKED | 200 `Key revoked`, 0 attempts | same | same |
| POST /api/audit | 201, mem only, 0 rows | 500 | 201, 0 rows |
| POST /api/events | 201, 0 rows | 500 | 201, 0 rows |
| PATCH /api/events/:id/resolve | 200, mem only | no answer + unhandled | 200 |
| GET admin-scopes | 500 INTERNAL_ERROR | revokedProxy: no answer; getterThrows: Express default 500 | revokedProxy: 500 INTERNAL_ERROR; getterThrows: unchanged (G112-F2) |

db.ts (scripts/g112_dbprobe.test.ts, logs/g112_dbprobe_{base,head}_test.jsonl, real initDb): revokedProxy/getterThrows from the probe -> base `initDb` REJECTS; head resolves `false` (= ordinary), constant logged. From the boot hook -> base rejects; head resolves `true`, DB stays flagged available (= ordinary).

Fail-open surface (audit/event persistence and the usage write) is existing behaviour for an ordinary Error; this PR extends it to the unreadable value only, as the author states.

## 4. Real winston logger, hostile non-string messages (Q c)
- `msgRevokedProxy` (getter returns a revoked Proxy): the guard stores it uncoerced; both winston formats throw while serialising. Base = head: validate (stored, lookup, usage) and resolve **unanswered + unhandled rejection**; audit/event 500; mint/revoke 500; admin-scopes 500 no code. db.ts: `dbLog`'s `JSON.stringify` throws, `initDb` rejects (and boot's `initDb(...).then` has no catch). Never `valid:true`, no key, nothing persisted.
- `msgBigInt`: dev format throws (`JSON.stringify` BigInt) -> same unanswered outcome as above, base = head; production json format serialises it -> ordinary outcome, base = head. db.ts throws at base and head.
- `msgSymbol`, `msgToStringThrows`, `nullProto`: no crash, ordinary outcome, base = head.
- No regression in any hostile shape (judge asserts base == head for all five). G112-F1.

## 5. Re-measure (Node v26.8.1 only; NOT measured on Node 24)
- `npm ci --ignore-scripts` rc 0; shared built.
- **Red-first** (logs/red_base.json): new tests at base product: 31 cells, **17 fail, all AssertionError** (admin-scopes 1/4, audit-event 4/7, db 4/6, save-api-key 2/4, validate 6/10); the 14 controls pass. Matches the author.
- **Suite:** base (new tests absent) 40 files 393/393; head **45 files 424/424**, 0 failed. Matches.
- **tsc:** plain rc 0; tsconfig.test.json rc 0; leg-16 checker "64 files, 0 errors, 0 new"; planted unused local -> TS6133 rc 2, file restored.
- **eslint** (index.ts, db.ts, 5 tests): 0 errors, 2 warnings (`isZod` 1806, `infra` 1807, both in the PUT route, pre-existing per the author's base read). Planted file -> `no-debugger` rc 1.
- **docs-fragments:** clean rc 0 ("flow 117 legacy + 79 new, cheat 112 + 79"); four planted defects (flow div, flow `<!--n-->.`, cheat div, cheat `</table>`) each rc 1; restored by sha. The cheat ADVISORY at :6235 is develop's own (G90-F7).
- **Mutants** (scripts/mutants.py, logs/mutants.log, product only, sha-restored each, tree clean after): 46 mutants on the changed lines (8 guard sites x revert / constant-for-all / fallback `String(err)` / inner rethrow / fallback text 'x'; admin-scopes x revert / `next(error)` / swallow `isZod=false` / rethrow / answer 400 / error text 'x'). **45 killed, 1 survived:** admin-scopes `new Error('x')` (G112-F5). Each guard site's mutants turn only its own file's cells red.
- Pre-push hook (13/16 legs, PREFLIGHT INCOMPLETE) and CI: the author's, not re-run.

## 6. Held passes + merge-tree (logs/held_vs_pr.log, mergetree.log, mergetree_end.log)
- Held = the `diff` blocks of `out.md` in the five runs `2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p{1..5}_*` (each `SPARK RESULT: PASS`), copied to evidence/held/. Each applies alone at cd9c4a7 with `git apply --cached` (no fuzz, no offset). Combined in order, P4 lands at offsets +18/+24 (P1-P3 change index.ts first), as the author said. Combined blobs == PR blobs for all 64 files under services/security/src (`diff` rc 0). Corrupted context line -> rc 1. Fragments are the author's own (not in the held passes).
- Develop `c2c2e03afdb3`: 14 paths past base (nft-certificate, originate, fragments), **0 shared** with the PR (control 14), services/security and packages/shared unchanged; `merge-tree --write-tree` rc 0, tree `11b2a119`, result vs develop = exactly the PR's 9 paths, +967/-9.
- Develop re-read at END = `c234c2388a16`: 20 paths past base, 0 shared, security/shared unchanged; merge-tree rc 0, tree `92dbecf4`, SAME_PATHS, +967/-9, merged index/db blobs = the PR's.
- Probe not re-run on the merged tree (read: 0 shared paths, product blobs identical).

## 7. Kam's ks1346 logging rule (Q d)
- Every new/changed log line carries field name `error` with either the constant `'unreadable thrown value'` (unreadable values) or the same `err?.message` value base logged (readable values). No new value reaches a log or a response.
- **Key material:** across all 488 route records, 0 log lines contain the raw API key or its sha256 hash. The `dbSaveApiKey` / `dbRecordApiKeyUsage` lines carry only `error`; the KS-888 lines carry `keyId` (internal id), `code`, `infra`.
- Pre-existing, unchanged: readable `message` values are logged (as at base), and a non-string object `message` is serialised whole (`msgToStringThrows`: its extra field reached the log at base and head). G112-F6.

## 8. FINDINGS
- **G112-F1 (RECOMMENDED follow-up, not FIX-BEFORE-MERGE; measured, base = head).** The guard does not coerce: `reason = err?.message` keeps a non-string. With a getter returning a revoked Proxy (both formats) or a BigInt (dev format), the real winston logger throws, so validate's three catches and resolve leave the request unanswered with an unhandled rejection; audit/event answer 500; db.ts `dbLog` throws and `initDb` rejects (boot's `initDb(...).then` has no catch). Still fail closed: no `valid:true`, no key, nothing persisted. Suggested form (PR 1924's): inside the same try, `const m = err?.message; reason = typeof m === 'string' ? m : String(m);` (a `String()` throw lands in the catch and gives the constant), plus one cell per shape. Note this would newly move those shapes onto the ordinary path (same tier-1 class as this PR).
- **G112-F2 (INFO/RECOMMENDED card; disclosed by the author as O74-P1; measured, base = head).** admin-scopes GET with an Error whose `message` getter throws: `instanceof` does not throw, so it reaches the SHARED `errorHandler`, which reads `err.message` unguarded and crashes; Express's default handler answers 500 HTML. Under a non-production NODE_ENV that page **echoes the getter's thrown message and stack in the response body** (seen in the probe). In production Express omits it. Belongs to the author's board candidate (packages/shared/src/errors/index.ts:237-239).
- **G112-F3 (INFO).** One new `valid:true`: an ACTIVE key whose usage write rejects with an unreadable value now answers `valid:true` (base: no answer). Equals the ordinary Error (KS-888 card 3, log-only usage write). A stored-revoked key never reaches the usage write (0 attempts, all kinds).
- **G112-F4 (INFO).** Mint/revoke: getterThrows + 08006 moves 500 -> 503, equal to the ordinary 08006 Error (STOP CHECK did not fire). No key issued; revoke stays process-local, response says not saved.
- **G112-F5 (LOW, test gap).** Mutant "admin-scopes `new Error('x')`" survives: the constant reaches only the shared errorHandler's log, not the response, and no cell asserts it. Optional.
- **G112-F6 (INFO, ks1346, pre-existing).** Readable `message` values (and a non-string object `message` in full) are logged at base and head alike; no key or hash in any line.
- **G112-F7 (INFO).** Develop moved during the gate to `c234c238`; merge-tree onto it clean, same 9 paths, 0 shared.
- **G112-F8 (INFO).** The author's "9/9 mutants" is per-hunk undo; this gate ran 46 per-site mutants, 45 killed.
- **No FIX-BEFORE-MERGE item.**

## 9. NOT TESTED / UNMEASURED
- Node 24; the live PR body, Linear ticket, CI, pre-push legs.
- A real Postgres (the store is a model; SQL not executed), a real service boot, the gateway hop (`middleware/auth.ts:288`) and auth's connector-token caller, the rotate path (`saveKeyAndRetirePriors`, gate 90's), the retry-timer caller of `probeDb`.
- The shared errorHandler's own log line for the admin-scopes constant (its logger output was not captured).
- **Outbound network (Q e):** `pg` mocked, JWT verified from `JWT_PUBLIC_KEY` (JWKS/AUTH_SERVICE_URL unset), all HTTP to 127.0.0.1. A `net.Socket.connect` witness recorded only loopback-style targets and 0 outbound, but its host formatting was weak (`localhost:undefined` for the undici fetch sockets), so "no outbound call" is by construction plus that witness, not a packet capture.
- Whether any real pg failure can produce these values (all synthetic).
- The author's own recorder (tier1_compare_pr2_w16.py) was not run; this gate built its own.
