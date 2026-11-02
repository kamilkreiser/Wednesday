# Spark operator 81, 2026-11-02: KS-1868 G112-F1 (security index.ts + db.ts) and the admin.ts identity catches -- 4 HELD, 0 model FAILs, 0 control FAILs, 0 rebriefs

## BLUF
- HELD 4 passes, each model PASS 7/7 on the ORIGINAL brief, golden BYTE-IDENTICAL, strict=True. Every control passed FIRST time (no CONTROL-FAIL). Model lines queued only after that pass's CONTROL-PASS.
- P1-P3 = G112-F1 on services/security (PR 1930, merged): db.ts (2 sites), index.ts audit/event (2), index.ts validate path (3). P4 = G110-F1 class on api-gateway admin.ts: three identity catches (1288/1316/1346) that operator 80's G3-G5 did not cover.
- Fix form chosen for security (NOT bare String and NOT gate 112's `typeof m === 'string' ? m : String(m)`): `const m = err?.message; reason = m === undefined || m === null ? m : String(m);` inside the existing try. WHY: gate 112's form (and a bare String) turns an undefined message into the TEXT 'undefined'. A thrown plain string/null has no message; today it is logged with no `error` field and db.ts probeDb returns `error: undefined`. Gate 112 measured plainString as identical base vs head, so a bare String would be a new, unrequested change for those values (the probe's returned `error` would become 'undefined'). Controls C3/C4 pin the unchanged behaviour. All string messages stay byte-identical; a hostile value throws inside String() into the existing catch (constant); a Symbol logs as its text.
- P4 (admin.ts) uses `String(err instanceof Error ? err.message : err)` (operator 80 G2 form): a non-Error throw is still stringified exactly as before, so no undefined issue.
- Skipped (reasons below): index.ts rotate catches 306/419, dbSaveApiKey 489, admin-scopes GET (Zod pre-check), services/governance and every file an open PR or live seat touches.
- Tip: develop e2a2426d221d at start (tip_start.out). Mid 466a0d6c4c55 then bc8558db6b66 (rounds' control rows show these tips); drift e2a2426..466a0d6 and e2a2426..bc8558d on services/security and api-gateway admin.ts: EMPTY (drift_466.out, drift_bc85.out, 0 bytes). End tip 66a36e3f777d (tip_end.out): NOT in the cache clone, drift to it UNMEASURED. Open-PR scans: start 22 PRs/128 files (control services/originate 8), mid 22/130 (8), end 21/120 (6): no PR lists services/security/src, api-gateway admin.ts, or any of my four new test names (only security package.json in 575/649, not mine). prscan_*.out, open_prs_*.json.

## Held (ls night | grep O81, ls_held.out; all under /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/)
READY_KS-1868-KS-1868-O81-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-SECURITY-DB-PROBE-HOOK-MESSAGE-COERCE-PASS-7of7-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O81-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-SECURITY-AUDIT-EVENT-MESSAGE-COERCE-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O81-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-SECURITY-VALIDATE-MESSAGE-COERCE-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O81-P4_spark-dsv4flash_BRIEFED-CODEPATCH2-APIGATEWAY-ADMIN-IDENTITY-MESSAGE-COERCE-PASS-7of7_2026-11-02.diff.md

## Per pass (hold_ready lines from hold_p*.log)
### O81-P1 (G112-F1) security db.ts, 2 hunks @@ -103 (runDbReadyHook) and -121 (probeDb) -- recommended TIER 1 (same service as the key validate/mint path; Spark default for security index.ts, and db.ts is its availability probe)
- `golden: BYTE-IDENTICAL; touched=2 product_plus=4 product_minus=2 red=8/12 green=12/12 suite=424->436 strict=True` (vitest). Test `ks1868-security-db-message-coercion-unreadable-throw.test.ts` (C1-C4, R1-R8).
- Callers: initDb (boot and the retry timer). Today (hostile non-string message, gate 112): boot hook dbLog JSON.stringify throws so initDb REJECTS (boot's initDb(...).then has no catch); after: probe -> initDb false, hook -> initDb true, constant logged = the ordinary-Error rows.
- BEHAVIOUR CHANGE (PR text): for a readable-but-hostile non-string message only, initDb resolves (false for the probe, true for the hook) instead of rejecting; Symbol message logs as its text; every string message and a no-message throw unchanged. Nothing persisted either way.
### O81-P2 (G112-F1) security index.ts, 2 hunks @@ -179 (dbSaveAuditLog) and -201 (dbSaveSecurityEvent) -- recommended TIER 1 (security service)
- `golden: BYTE-IDENTICAL; touched=2 product_plus=4 product_minus=2 red=8/12 green=12/12 suite=424->436 strict=True`. Test `ks1868-security-audit-event-message-coercion-unreadable-throw.test.ts` (C1-C4, R1-R8; the brief header says "14 cells", it is 12: operator typo in KS-1868.md only).
- Today (gate 112, real logger): POST /api/audit and /api/events answer 500; after the ordinary 201 with the constant logged. Nothing stored either way (the insert failed).
- BEHAVIOUR CHANGE (PR text): hostile non-string message only: those routes answer 201 instead of 500.
### O81-P3 (G112-F1) security index.ts, 3 hunks @@ -535 (dbRecordApiKeyUsage), -1929 (validate stored-state read), -1958 (validate cache-miss lookup) -- recommended TIER 1 (API-key validate)
- `golden: BYTE-IDENTICAL; touched=2 product_plus=6 product_minus=3 red=12/17 green=17/17 suite=424->441 strict=True`. Test `ks1868-security-validate-message-coercion-unreadable-throw.test.ts` (C1-C5, R1-R12).
- Today (gate 112, real logger): all three leave the request unanswered with an unhandled rejection (validate takes no next). After: stored read 503 SERVICE_UNAVAILABLE, lookup `Key not found`, usage write valid:true for an ACTIVE key (the same valid:true an ordinary Error already gets, KS-888 card 3; gate 112 F3). A stored-revoked key never reaches the usage write. Never newly valid:true for a revoked/unknown key.
- BEHAVIOUR CHANGE (PR text): hostile non-string message only: validate answers (503 / Key not found / valid:true for an active key whose usage write failed) instead of hanging. The valid:true row is the one a QA gate must re-check (fail-open surface is log-only usage write, existing behaviour).
### O81-P4 (G110-F1 class) api-gateway admin.ts, 3 hunks @@ -1285 (GET identity users), -1313 (GET identity organizations), -1343 (PATCH identity user level) -- recommended TIER 2 (gate 110's ruling for the sibling admin.ts passes)
- `golden: BYTE-IDENTICAL; touched=2 product_plus=3 product_minus=3 red=12/18 green=18/18 suite=1412->1430 strict=True`. Test `ks1868-admin-identity-routes-message-coercion-unreadable-throw.test.ts` (C1 and C2 x3 routes, R1-R12). Ref pin: ks1868-admin-identity-seed-catch-unreadable-throw.test.ts (same as O80-G5).
- Today (hostile non-string message, real logger): no answer (gate 110 measured the same for the sibling guards: log() itself throws); after the ordinary constant 500 and the constant reason in the log. PATCH issues its UPDATE before the catch either way. Auth untouched.
- BEHAVIOUR CHANGE (PR text): hostile non-string message only: constant 500 instead of no answer. Note: I did not re-measure the real-winston hang for these three routes; it is carried from gate 110 for the sibling guards (stub logger in the cells).

## Raise-seat notes
- All strict (plain git apply). P1-P3: hunks in db.ts / index.ts are >3 lines apart (P2: 22 apart; P3: 1394 and 29 apart). P2 and P3 are the same file (index.ts) and P1 is db.ts; the passes applied together were NOT run. P4 is admin.ts, which O80-G3/G4/G5 also edit: sites are distinct (O80: 1020,1246,1469,1495,1527,1546,1646; mine 1288,1316,1346), >40 lines from the nearest, but the union was not applied together.
- Cell names: `control ks1868 C<n>` / `RED ks1868 R<n> ...`. Tests compare strings (typeof) so a revoked Proxy never reaches toEqual; the checker splice of `const status` was avoided (no bare status identifier; responses read as `http:`).
- Stub loggers record what they receive: real winston is pinned indirectly (logged reason must be the safe text), not run.

## Round log (spark/done.md row times, AEDT)
- P1: ctl PASS 18:52:06 (211 s); model PASS 7/7 18:57:46 (274 s, 51.5 s model).
- P2: ctl PASS 18:59:14 (85 s); model PASS 7/7 19:08:47 (340 s, 94.4 s).
- P3: ctl PASS 19:00:24 (69 s); model PASS 7/7 19:12:30 (222 s, 115.5 s).
- P4: ctl PASS 19:03:05 (160 s); model PASS 7/7 19:15:41 (190 s, 81.3 s).
- Queue discipline: one control (P1) until CONTROL-PASS; then P1 model + P2/P3/P4 controls together; each model line only after its own CONTROL-PASS. Polled by grep -c -i on done.md. P3's first dry run was REFUSED by a transient GitHub RemoteDisconnected on an attached-PR read (dry_p3.out), re-run BUSY (rc 3), and its control built fine; P4 dry run was BUSY (rc 3), control queued per the common file.

## Skipped (with reasons)
- index.ts 306 and 419 (revoke-on-rotate catches, `err instanceof Error ? err.message : String(err)`): not named by gate 112 F1, rotate path not exercised by gate 112 (UNMEASURED there), and Seat S 11th/gate 90 territory; left for a separate brief.
- index.ts 489 (dbSaveApiKey, rethrows to the revoke/mint route whose own catch behaviour with a hostile non-string message I did not read): a cell asserting the route outcome would be a guess, so skipped rather than briefed.
- admin-scopes GET (1813/1854 area): Zod pre-check, `instanceof z.ZodError` throws first; out per the common file.
- services/governance (Seat F 23rd / KS-1940), services/auth (PR 1931), anchoring/originate anchors.ts (PR 1932), Seat V/E/S files: excluded as instructed.
- admin.ts: the create-user forward (:1432 `err?.message` in console.error, G110-F4) and the three read-less catches: not briefed this round.

## UNMEASURED
Whole-suite CI; eslint; real winston (the hang itself); real Postgres/pg; a real boot; Node 24; the four passes applied together or with O80's admin.ts passes; the PR bodies and Linear text; drift of my files to develop 66a36e3f777d (end tip, not in the cache clone); whether any hostile non-string message occurs in production. Evidence: this folder (tip_*.out, prscan_*, open_prs_*.json, lint_p*.out, dry_p*.out, drift_*.out, hold_p*.log, mk_p*.out, ls_held.out, round_tips.out, gen/mk81.py sites81.py t81_p*.ts.txt hold81.sh).
