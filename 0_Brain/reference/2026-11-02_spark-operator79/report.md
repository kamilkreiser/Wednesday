# Spark operator 79, 2026-11-02: KS-1868 originate certifications.ts (G105-F5 + G105-F2) and String() coercion (verification, v2, retention) -- 10 HELD, written by operator 80 FROM ARTEFACTS ONLY

Operator 79 died with the coordinator rotation (~17:47 AEDT) before writing this. Operator 80 reconstructed it from spark/done.md o79 rows, the ten held READY files, hold_*.out and the tip_* snapshots in this folder. No rounds were re-run. Anything not in those artefacts is UNMEASURED.

## BLUF
- 10 passes HELD (A1..A6, B1..B4), every one model PASS 7/7, golden BYTE-IDENTICAL, strict=True. Zero model FAILs in done.md. Tip 8f313815f415 for A1-A6 and the first B controls; B1/B2 control-r2 rows show tip 829233f1a388 (develop moved during the run; drift check UNMEASURED, no tip_end file exists).
- Control history: first-time CONTROL-FAIL on A1, A2, A3, B1, B2 (checker rc=1; A3 and B2 also golden DIFFERS); each re-passed as `-control-r2` after a brief/harness fix (the fix content is UNMEASURED here: the failing checker output was not re-read). A4, A5, A6, B3, B4 passed control first time. No model round ran behind a failing control (every model row is later than its CONTROL-PASS row).
- Rebrief count: A1 has an extra mk (`mk_a1b.out`, `lint_a1b`, `dry_a1b`) = a pre-model brief rebuild; no model round was ever run twice (one model row per pass).

## Held files (ls night | grep O79)
READY_KS-1868-KS-1868-O79-A1_spark-dsv4flash_BRIEFED-CODEPATCH2-RECERTIFY-ANCHORING-CATCH-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O79-A2_spark-dsv4flash_BRIEFED-CODEPATCH2-ISSUE-ANCHORING-CATCH-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O79-A3_spark-dsv4flash_BRIEFED-CODEPATCH2-ISSUE-RESERVE-SAVE-CHARGE-CATCHES-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O79-A4_spark-dsv4flash_BRIEFED-CODEPATCH2-ISSUE-HOLDER-AND-LEGACY-UPDATE-CATCHES-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O79-A5_spark-dsv4flash_BRIEFED-CODEPATCH2-ISSUE-COMPENSATING-DELETE-CATCH-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O79-A6_spark-dsv4flash_BRIEFED-CODEPATCH2-REPO-LIST-AND-SHARES-CATCHES-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O79-B1_spark-dsv4flash_BRIEFED-CODEPATCH2-VERIFICATION-VERIFY-HASH-STATUS-COERCE-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O79-B2_spark-dsv4flash_BRIEFED-CODEPATCH2-VERIFICATION-VERIFY-FILE-COERCE-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O79-B3_spark-dsv4flash_BRIEFED-CODEPATCH2-VERIFICATION-V2-COERCE-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O79-B4_spark-dsv4flash_BRIEFED-CODEPATCH2-RETENTION-SCHEDULER-COERCE-PASS-7of7_2026-11-02.diff.md
(all under /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/)

## Per pass: sites (tip line numbers = hunk starts in the held diffs), hold_ready line, tier
Product file for A1-A5: Blockchain/Dev/services/originate/src/routes/certifications.ts. Fix form in all A passes: `let reason: string; try { reason = String(e instanceof Error ? e.message : e); } catch { reason = 'unreadable thrown value'; }` then log `error: reason`.

- A1 (G105-F2) certifications.ts hunk @@ -1443 (recertify route): `logger.warn('Anchoring service unreachable for verification cert', { error: err?.message })`. hold: red=5/7 green=7/7 suite 2163->2170. TIER 1 (certifications route; recertify). Note: the original read `err?.message`, so a thrown non-Error value logged `undefined`; after, it logs String(value). Log-content change for readable non-Error values only.
- A2 (issue anchoring catch) @@ -629: `'Anchoring service unreachable for certification', { certId, error: err?.message }`. hold: red=4/6 green=6/6 suite ->2169. TIER 1 (issue route). Same `err?.message` -> String(...) note as A1.
- A3 (G105-F5, issuance + charge) three catches in the issue route: @@ -579 `reserveErr` (KS-1633 pre-anchor reservation; its comment says the request must continue when the reservation fails), @@ -745 `saveErr` (KS-70 derived-document lineage write; code comment: certification row already landed, fall through, "We don't 500 the cert"), @@ -826 `chargeErr` (KS-216 charge events; message "continuing, certification already issued"). hold: product +21/-3, red=9/15 green=15/15 suite ->2178. TIER 1. Consequence as the code states it: today `String(x)` inside each catch throws on an unreadable value, which escapes the catch that is meant to swallow it, so issuance is aborted/500 after the reservation or after the certification row and anchor already landed, and the charge-event catch (billing) fails after the cert is issued; after, each continues exactly as for an ordinary Error. The measured per-cell response/state table was in the (lost) brief; UNMEASURED here beyond the held diff and test file names.
- A4 (G105-F5) @@ -404 holderId validation catch (`errMsg`, then branches on `errMsg.includes('invalid input syntax'|'uuid')` -> 400 variants) and @@ -781 `updateErr` (KS-70 legacy documents UPDATE). hold: +13/-2, red=6/10 green=10/10 suite ->2173. TIER 1. Note the :404 `errMsg` also feeds control flow: the constant 'unreadable thrown value' falls to the generic 400 'could not validate', as any non-uuid DB error already does.
- A5 (G105-F5) @@ -653 `delErr` in the KS-1633 compensating-delete catch (followed by the 503 'anchoring unavailable' answer). hold: +7/-1, red=3/5 green=5/5 suite ->2168. TIER 1: today a throwing read here replaces the 503 with an unhandled path and leaves a certification row with no anchor unlogged; after, the "certification remains with no anchor" error line is written with the constant and the 503 is returned. (Inference from the tip source at tip_certifications.ts :640-668 and the diff, not from a saved cell table: UNMEASURED.)
- A6 certificationRepo.ts @@ -203 (`DB list failed`) and @@ -387 (`Failed to fetch shares from DB`): same guard. hold: +14/-2, red=6/10 green=10/10 suite ->2173. Recommended TIER 2 (read paths that already fall back after the log; the first catch is followed by a fallback return). Not G105-listed; extra site from the repo file.
- B1 verification.ts @@ -1443, @@ -1478, @@ -1506 (verify-hash status guards): `reason = error instanceof Error ? error.message : String(error)` -> `String(error instanceof Error ? error.message : error)`. hold: +3/-3, red=6/12 green=12/12 suite ->2175. TIER 1 (public no-login verification surface; `reason` is a status-guard value). B1 control-r2 tip 829233f1a388.
- B2 verification.ts @@ -758 (verify-file guard), same coercion. hold: +1/-1, red=2/4 green=4/4 suite ->2167. TIER 1 (public verify-file).
- B3 verificationV2.ts @@ -440 and @@ -482, same coercion. hold: +2/-2, red=4/8 green=8/8 suite ->2171. TIER 1 (public v2 verify).
- B4 retentionScheduler.ts @@ -50, same coercion. hold: +1/-1, red=2/4 green=4/4 suite ->2167. Recommended TIER 2 (internal scheduler, no public response).
- B-pass mechanism: `String(...)` now wraps the whole ternary, so an Error whose `message` is a non-string (object, number) becomes a string before `reason` is used. The diff adds no try/catch: whether String() itself can still throw on a null-prototype or throwing-toString message, and whether the enclosing code guards it, was NOT established from the artefacts (UNMEASURED; the raise seat should read the enclosing try and the O79 test cells).

## Round log (done.md row times, AEDT)
- A1 ctl FAIL 16:25:33, ctl PASS 16:29:58, model PASS 7/7 16:34:17 (232 s, 88.8 s model, 36848+3023 tok)
- A2 ctl FAIL 16:37:08, ctl-r2 PASS 17:02:13, model PASS 17:34:41 (247 s, 112.7 s)
- A3 ctl FAIL 16:39:41 (golden DIFFERS), ctl-r2 PASS 17:05:15, model PASS 17:39:12 (266 s, 123.7 s)
- A4 ctl PASS 16:42:05, model PASS 17:09:44 (268 s, 121.7 s)
- A5 ctl PASS 16:46:25, model PASS 17:14:18 (273 s, 111.8 s)
- A6 ctl PASS 16:59:04, model PASS 17:30:33 (172 s, 47.2 s)
- B1 ctl FAIL 16:49:31, ctl-r2 PASS 17:16:30, model PASS 17:42:58 (225 s, 84.0 s)
- B2 ctl FAIL 16:52:45 (golden DIFFERS), ctl-r2 PASS 17:19:19, model PASS 17:46:18 (199 s, 74.9 s)
- B3 ctl PASS 16:55:09, model PASS 17:22:50 (210 s, 62.1 s)
- B4 ctl PASS 16:57:01, model PASS 17:27:39 (288 s, 42.6 s)

## UNMEASURED
Why the five first controls failed and what was fixed; the open-PR scan result (prscan_start.out: 19 PRs / 108 files, planted control services/originate = 7, no end-of-run scan file exists); tip at end (no tip_end file; two B controls show 829233f1a388, so develop moved after 8f31381 and drift on the touched files was not checked); whole-suite CI, eslint, tsc, real Postgres, a real boot; the per-site today-vs-after cell tables (they lived in the briefs/tests, only summarised above from source and diffs); P-sets applied together (A1-A5 share certifications.ts, hunk sites 1443/629/579/745/826/404/781/653: all > 3 lines apart; A-passes applied together were NOT run).
