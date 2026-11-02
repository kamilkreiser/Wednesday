# Spark operator 77, 2026-11-02: KS-1938 gdprService retention sweep + KS-1868 signatories/thirdPartyVerifiers, TIER 1 (3 held, 0 failed, 1 skipped)

## BLUF
- HELD 3 passes, all PASS 7/7 on the ORIGINAL brief (0 rebriefs), golden BYTE-IDENTICAL, strict=True. All TIER 1, Opus gate required (Kam 11:34:59, card secuura-spark-ks1868-safe-sites-exhausted-1102 = a).
- O77-P1 (KS-1938, HIGH GDPR) gdprService.ts enforceRetentionImpl: per-policy catch (:499) + outer catch (:503), one hunk. DELETION-CONTINUITY change: after the fix a failed policy no longer abandons later policies.
- O77-P2 (KS-1868) signatories.ts nominate catch: `error.code` (:126) + `String(error)` (:132), one hunk.
- O77-P3 (KS-1868) thirdPartyVerifiers.ts: register `error.code` (:103) + `String(error)` (:109), approve `String(error)` (:199), two hunks.
- SKIPPED: originate index.ts :75-81 unhandledRejection handler (reason below).
- Tip: develop 968f17070208 at start (tip_start.out) and at end (tip_end.out): UNCHANGED.
- Open-PR scan start 20 PRs / 114 files, end 21 PRs / 121 files (new: 1925 verification route, OUT list); planted control (services/auth/ entries) = 7 both times (the script label says "originate", the filter is services/auth/). No PR lists gdprService.ts, signatories.ts, thirdPartyVerifiers.ts or originate index.ts (checked at end on open_prs_end.json: empty). PR 1924 lists certifications.ts only (OUT).

## Held (ls night | grep O77, pasted)
READY_KS-1868-KS-1868-O77-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-SIGNATORIES-NOMINATE-CATCH-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O77-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-THIRDPARTYVERIFIERS-REGISTER-APPROVE-CATCHES-PASS-7of7_2026-11-02.diff.md
READY_KS-1938-KS-1938-O77-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-GDPR-RETENTION-SWEEP-CATCHES-PASS-7of7_2026-11-02.diff.md

## Per pass
- P1 `golden: BYTE-IDENTICAL; touched=2 product_plus=14 product_minus=2 red=4/6 green=6/6 suite=2084->2090 strict=True` (jest, originate). Inline `let reason` guard, the form gate 104 gave. Ticket key KS-1938 (Refs KS-1938). Callers: `enforceRetention` (:428, runWithPlatformScope) from retentionScheduler.ts:43 and POST /api/gdpr/retention/enforce (routes/gdpr.ts:627, SYSTEM_ADMIN). Ordinary Error today and after: failure logged, sweep continues. Unreadable today: first policy's failure skips the rest (cells: statements stop after the failing DELETE), policy-SELECT failure makes enforceRetention REJECT (manual route fail500). After = ordinary path. Cells: C1/C2 ordinary (DELETE, SELECT), R1-R4; the RED cell asserts policy 2's DELETE, deletion-log INSERT and stamp run after policy 1 fails with a revoked Proxy (exact statement sequence). BEHAVIOUR CHANGE (for the PR): for an unreadable thrown value only, a failure on one retention policy no longer abandons the later policies of the same sweep; their DELETE/anonymise, deletion-log rows and last_enforcement_at stamps now run as after an ordinary Error; the manual enforce route answers 200 instead of fail500 in the policy-SELECT case. No statement or predicate changes. Tier 1.
- P2 `golden: BYTE-IDENTICAL; touched=2 product_plus=14 product_minus=2 red=2/5 green=5/5 suite=2084->2089 strict=True`. `code` read in its own try (unreadable = no code), `reason` guard on String(error). Callers: HTTP only (INSERT INTO signatories precedes the catch; catch persists nothing). Unreadable today: NO ANSWER, no log; after: constant 500 + one log line with the constant = ordinary Error without a code. Cells C1 ordinary, C2 string, C3 code 23505 still 409 (nothing logged), R1/R2. BEHAVIOUR CHANGE: unreadable value only gets the constant 500 and a constant-reason log instead of no answer; an unreadable code counts as no code (never 409). Tier 1.
- P3 `golden: BYTE-IDENTICAL; touched=2 product_plus=21 product_minus=3 red=4/9 green=9/9 suite=2084->2093 strict=True`. Same guards for register (code + String) and approve (String). Cells: C1/C2 per route, C3 register 23505 -> 409, R1/R2 per route. Same behaviour text; note G104-F3: a throw after the approve UPDATE loses the one-time API key for ordinary Errors too (pre-existing, unchanged). Tier 1.

## Raise-seat notes
- All strict (plain git apply). Hunk distances: P1 one hunk (both catches 4 lines apart, merged by diff context), P2 one hunk, P3 two hunks (:103-:109 and :199, > 3 lines apart). Different files, mutually disjoint.
- New tests: ks1938-gdpr-retention-sweep-catches-unreadable-throw.test.ts, ks1868-signatories-nominate-catch-o77p2-unreadable-throw.test.ts, ks1868-third-party-verifiers-register-approve-catches-o77p3-unreadable-throw.test.ts. Names `control ksNNNN C1..`, `RED ksNNNN R1..`.
- P1 PR should say Refs KS-1938 (not KS-1868); P2/P3 Refs KS-1868 and close out G104-F3 candidates (:126, :132, :103, :109, :199).
- The other 17 unguarded reads in gdprService.ts (consent, DSR, erasure :917, export :978-1028, :1603) are NOT covered (G104-F1); they sit on request paths, not the sweep.

## SKIPPED
- originate src/index.ts :75-81 unhandledRejection handler: it reads `reason instanceof Error ? ... : String(reason)` unguarded. If that read throws inside the handler, Node raises an uncaughtException, which the handler at :83 answers with process.exit(1) after 100 ms. Guarding it would stop that exit for an unreadable rejection, i.e. change whether the process exits (assignment SKIP rule); also not drivable in jest (module-load side effects, real process). Left for a design call.

## Round log (spark/done.md row times, AEDT 2026-11-02)
- P1: CONTROL-PASS 15:03:36 (169 s, first control, harness proven); model PASS 7/7 15:08:21 (257 s, 77.5 s model).
- P2: CONTROL-PASS 15:11:05 (163 s); model PASS 7/7 15:20:27 (217 s, 54.7 s model).
- P3: CONTROL-PASS 15:15:07 (240 s); model PASS 7/7 15:23:59 (210 s, 58.8 s model).
- Queue discipline: one control (P1) until its CONTROL-PASS; then P1 model + P2/P3 controls together; P2/P3 model lines only after their own CONTROL-PASS. Dry runs rc 0 (a warm-up dry run of operator 75's brief fetched the new tip into the cache). No recursive grep over spark/ or night/.
- hold_ready lines: see hold_p1.log, hold_p2.log, hold_p3.log.

## UNMEASURED
Whole-suite CI with the patches (the checker's own suite counts 2084->2090/2089/2093 are per pass, not combined); eslint; real Postgres/Prisma; a real boot; whether an unreadable value is reachable in production; the three patches applied together (different files, disjoint); drift of these three files after 968f170 (tip unchanged at end).
Evidence: this folder (tip_*, open_prs_*.json, prscan_*, lint_*, dry_*, hold_p*.log, mk.out, gen/mk77.py sites77.py t77_p*.ts.txt hold77.sh).
