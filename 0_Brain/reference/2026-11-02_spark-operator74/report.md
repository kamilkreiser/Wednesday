# Spark operator 74, 2026-11-02: KS-1868 security service leftovers (5 held, 0 failed, 0 rebriefs; all TIER 1)

## BLUF
- HELD 5 passes, all PASS 7/7, golden BYTE-IDENTICAL, strict=True. Files: services/security/src/index.ts (P1-P4), src/db.ts (P5). Disjoint, any order.
- Tip: start d9acf71a3fcc (tip_start.out); mid/end 92a26320e30a (tip_mid.out, tip_end.out; develop moved by PR 1917 etc.); `git diff --stat d9acf71..92a2632 -- services/security` empty (tip_diff_security.out), so the holds apply at the new tip (rounds and controls ran at 92a26320e30a except P1 control at d9acf71).
- Open-PR scan: start 21 PRs/120 files, end 23 PRs/141 files, planted control services/originate 7 both times; `services/security/src` appears in no open PR at start or end (security only via package.json at start).

## Held (ls night | grep O74): see held_files.txt
## Per pass (hold_ready lines in the held-file listing; summaries)
- P1 GET /api/keys/admin-scopes/:userId catch (Zod pre-check, PR 1912's isZod form, `let isZod: boolean` no initialiser per G94-F4). red=1/4 green=4/4 suite 393->397. BEHAVIOUR: unreadable only: today no answer + unhandled rejection; after 500 INTERNAL_ERROR (= ordinary Error). Read-only route. C3 pins the 400 (G94-F2 shape).
- P2 dbSaveApiKey catch (`let reason` around `err?.message`). red=2/4 green=4/4 suite 393->397. BEHAVIOUR: today callers get a TypeError and no log line; after the line is logged with the constant and callers get the ORIGINAL value, which PR 1912's guarded route catches classify. Both routes still 500; revoke stays in memory; mint issues no key. NOTE: an Error with throwing `message` but readable infrastructure `code` now classifies 503 (what an ordinary Error with that code gets); today 500. Not pinned by a cell.
- P3 dbSaveAuditLog + dbSaveSecurityEvent catches. red=4/7 green=7/7 suite 393->400. BEHAVIOUR: today helper rejects, POST /api/audit and /api/events answer 500 (record in memory, nothing in DB); after swallow + log, 201 (= ordinary Error).
- P4 validate path: dbRecordApiKeyUsage, stored-state read (503), cache-miss lookup. red=6/10 green=10/10 suite 393->403. BEHAVIOUR: today request never answered + unhandled rejection; after 503 / Key not found / valid:true, each = ordinary Error. Valid only after the stored read succeeded; a revoked key is refused before the usage write.
- P5 db.ts probeDb + runDbReadyHook. red=4/6 green=6/6 suite 393->399. BEHAVIOUR: today initDb rejects / retry timer raises unhandled rejection; after initDb resolves false (flag stays false, retry scheduled) or true (hook failure logged).

## Skipped (reasons)
- Zod pre-check catches :834 (POST /api/audit), :967 (POST /api/events), :1453 (POST /api/keys outer), :2066 (rate-limit check): no seam to inject a throw into the try without mocking internals; same fix shape as P1 if a seam is wanted.
- index.ts :75 decryptDetails, :592 loadFromDb, :2138 PII init, :2172 migration: boot/load paths, not reachable from a route test with SECURITY_DISABLE_BOOT.
- db.ts :37 pool.on('error') (not a catch); :66 transaction rethrow (no read); index.ts :1553 `next(err)` (no read).
- Other security files (adminScope, keyRevokePolicy, provisioningPolicy, rate-limit*, requestRefusal, requestSchemas, converters): no unguarded catch read.

## Raise-seat notes
All strict=True. index.ts hunks (P1 ~1825, P2 ~475, P3 ~177/193, P4 ~515/1897/1920) are >15 lines apart, one combined PR possible; P5 is db.ts. New tests: ks1868-security-{admin-scopes-get-catch,save-api-key-catch,audit-and-event-save-catches,validate-route-catches,db-probe-and-hook-catches}-unreadable-throw.test.ts, cells `control ks1868 C*` / `RED ks1868 R*`. Refs KS-1868 only. R2-style (message getter) cell is absent from P1 on purpose: that value passes `instanceof` and reaches the shared errorHandler (out of scope, Claude-seat job).

## Round log (done_rows.txt)
P1 CP 12:07:32, PASS 12:29:02; P2 CP 12:30:40, PASS 12:56:50; P3 CP 12:34:01, PASS 13:00:00; P4 CP 12:35:42, PASS 13:03:15; P5 CONTROL-FAIL 12:36:28 (my test: `.resolves` on a rejection is a non-assertion failure; added a `settle` helper, not a model round), CP 13:04:38, PASS 13:12:39. Lint rc 0 all; dry runs rc 3 BUSY (controls queued instead).

## UNMEASURED
Whole-suite CI, eslint outside the checker, real pg, gateway hop, memory-only mode, process-level exit on unhandled rejection, rotate path, the five patches applied together (textually disjoint).
