# Spark operator 50, 2026-11-02: KS-1868 services/auth routes/auth.ts x3 (held), KS-1796 (skipped)
Written by the operator (Bash heredoc). Gen/briefs in gen/, outputs ctl*/rnd*/dry*/hold*.

## BLUF
KS-1868 auth.ts: 3 passes, all 3 HELD. P1 and P3 PASS 7/7 byte-identical on the original brief; P2's first real round was byte-identical but FAILED A6 on a pre-existing timing flake (ks949), its re-run of the SAME brief PASSed (content equal to golden, one header line missing). No rebrief spent on any task. Three of the five control rounds failed first for instrument or brief-defect reasons (see lessons). KS-1796: SKIPPED, refused by build_input2 before any model call: "not under the ONE service Blockchain/Dev/services/auth/ ... ['Blockchain/Dev/docs/openapi/secuura-api.yaml']". The generator itself WORKS (see below) and its output is ready for a Claude seat. Tip: brief at ca36945e9740; develop moved to a1350ccbc738 then 8afcf256ed5f during the session; auth.ts, auth.openapi.ts and the yaml were not touched by those moves (round.sh compared). Open-PR scan: start 22 PRs / 128 files, end 22 PRs / 124 files; no PR touches routes/auth.ts, auth.openapi.ts, the yaml or a new test path (services/auth appears only as users.ts and a ks1006 test in PR 1796/1798, and package.json in 575/649/948/1726); positive control services/auth = 7 entries both times. Lanes beyond open PRs not checked.

## Held (pasted from ls night | grep O50)
READY_KS-1868-KS-1868-O50-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-BRIEFED-CODEPATCH2-AUTH-REGISTER-PUBLISH-EVENT-UNREADABLE-THROW-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O50-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-BRIEFED-CODEPATCH2-AUTH-LOGIN-PUBLISH-EVENT-UNREADABLE-THROW-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O50-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-BRIEFED-CODEPATCH2-AUTH-RESET-PASSWORD-REVOKE-UNREADABLE-THROW-PASS-7of7_2026-11-02.diff.md

## Task 1: KS-1868 services/auth/src/routes/auth.ts (security surface; the raise will be gated tier 1)
Sites at the tip (the three KS-1868-form reads; line numbers are +1 against Seat S 10th's tree): :306 register publishEvent catch, :612 login publishEvent catch, :880 reset-password revocation catch. These are the ONLY three `X instanceof Error ? X.message : String(X)` reads in the file (grep). NOT touched: the `err?.message` reads (:372, :547, :587, :768 here; S 10th's :371/:546/:586/:767) - a different form; and KS-1885 (`authoredExchangeText` :989-990 and exchange handling near :1113/:1403 at this tip; S 10th's :1080-1081/:1362 do not match this tip's numbers).
Fix shape (inline, no helper): inner try reading into `reason`, catch -> constant `unreadable thrown value`; the .catch arrow becomes a block body for P1/P2.
Each pass: 2 files (1 product hunk + 1 NEW test, 4 cells: C1 ordinary Error, C2 normal path, R1 revoked Proxy, R2 message-getter throws), code_patch2, tests given whole by the operator.

### P1 register :306 (ref ks1460)
- hold_ready: golden: BYTE-IDENTICAL; touched=2 product_plus=9 product_minus=1 red=2/4 green=4/4 suite=1459->1463 strict=False
- Run: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_p1_auth_register_publish_event_unreadable_throw ; model 68.7 s, 30827+2274 tok. Control r3 PASS (r1, r2 FAILED on ks949 timeout).
- Callers: the route handler itself (authRoutes.post('/register'), mounted /api/auth, src/index.ts:112). publishEvent (src/events.ts) swallows its own errors and returns early without Redis, so at this tip the handler is not reached: defence in depth.
- BEHAVIOUR CHANGE: a rejection value that cannot be read today throws inside the .catch => UNHANDLED REJECTION in the auth process after the 201 was sent. auth installs no unhandledRejection handler (only the gateway sets UNHANDLED_REJECTION_MODE=survive in docker-compose; auth Dockerfile is node:24-alpine), so under Node's default the process would exit. After: logs `error: unreadable thrown value`. The HTTP response is unchanged. (Read from source and Dockerfile; NOT run.)
### P2 login :612 (ref ks1157)
- hold_ready: golden: bytes differ; applied result not compared; touched=2 product_plus=9 product_minus=1 red=2/4 green=4/4 suite=1459->1463 strict=False  (the "differ" is exactly the missing first header line `diff --git a/.../auth.ts b/.../auth.ts` in section 1; `diff` of patch.diff vs golden.diff shows only that line; the hunk and the test file are byte-equal)
- Run (held): /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_p2_auth_login_publish_event_unreadable_throw-r2 ; model 80.9 s, 34675+3015 tok. Round 1 (/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_p2_auth_login_publish_event_unreadable_throw): BYTE-IDENTICAL but FAIL A6 (ks949 two cells timed out at 5.0 s). Control PASS first time.
- Callers/behaviour change: as P1, on the LOGIN path (every successful password login publishes user.login). Same unhandled-rejection class; same "defence in depth, not reached today".
### P3 reset-password :880 (ref ks1407)
- hold_ready: golden: BYTE-IDENTICAL; touched=2 product_plus=7 product_minus=1 red=2/4 green=4/4 suite=1459->1463 strict=True
- Run: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_p3_auth_reset_password_revoke_unreadable_throw ; model 74.6 s, 32070+2497 tok. Control r2 PASS (r1 FAILED: my brief defect, below).
- Callers: the public pre-auth route handler (POST /api/auth/reset-password); reachable whenever revokeAllUserSessions REJECTS (KS-1692).
- BEHAVIOUR CHANGE (security): an unreadable throw from the session revocation today escapes the catch block as a TypeError and the route answers 500 INTERNAL_ERROR (password already written, other sessions NOT revoked, token not burned, caller told only "unexpected"); after the fix it answers the 503 SERVICE_UNAVAILABLE ("Your password WAS reset, but your other sessions could not be ended ...") that every ordinary revocation failure already gets. Writes and burns identical. The same read exists in routes/users.ts change-password (~:1034, outside this file, not touched, not a listed site).
### Combined (P3, P1, P2 applied in order to a scratch clone at the tip; P1/P2 with `git apply -C1`)
All three product hunks present; the 3 new test files: 3 files / 12 tests passed; `tsc -p tsconfig.test.json` 42 errors = the 42 baseline errors, 0 in ks1868 files.
**Apply note for the raise seat:** P1 and P2 product hunks have 3 leading / 0 trailing context lines; plain `git apply` and `patch` (even -F1) refuse them (anchored-to-EOF rule); `git apply -C1` works (what the checker did).

## Task 2: KS-1796 - SKIP (refused before any model call)
Ticket (board screen section 3 item 4): add 422 and change the 400 text; confirmed against routes/users.ts change-password: wrong current password => BadRequestError 400, weak new password => ValidationError 422 after the verify. Sibling reset-password block at auth.openapi.ts :813 has `422: { ...commonErrorResponses[422], description: 'New password too weak' }`.
Generator: built a pipeline-style clone (git clone --shared of the cache + prepare_clone.sh), baseline `npx tsx scripts/generate-openapi.ts --check` rc 0 ("CHECK PASS"), edited auth.openapi.ts (400 text 'Wrong current password' + 422 entry with a 2-line comment), ran the generator: 314 paths written; diff = 1 source hunk (+4/-1) and 2 yaml hunks: "400" description changed, and a new "422" block (description New password too weak, schema ValidationErrorResponse) between 415 and 429. Golden + brief + 5-cell yaml/source test were written and lint rc 0, but `round.sh --dry-run` rc 2: build_input2 only accepts product files under the one service. (The yaml is also 1.39 MB, past the 160 KB excerpt ceiling.) Brief dir (kept, not queued): /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1796_o50_p1_auth_change_password_422_openapi (golden.diff holds the generator-produced yaml hunks). A Claude seat can raise: edit auth.openapi.ts as in that golden, run `npm run generate-openapi` (builds shared first), commit both files, run `npm run check:openapi`. The new test t50_k.ts.txt in gen/ is a candidate for the PR (not run: it only ever ran inside the golden build; UNMEASURED).
done.md row added (SKIP). Counter unspent.

## Lessons (also in IMPROVEMENTS.md)
1. git apply and patch refuse a 3-leading/0-trailing-context hunk; only `git apply -C1`. strict=False even for a byte-identical patch.
2. The checker's decl-splice copies ref-test consts into a new test when the new test uses the same word as a property name (my P3 r1: `h.passwordWrites`/`h.tokenBurns`); KS-1000 red.
3. ks949 services/auth tree-walk cells run 3.4-4.1 s against a 5 s timeout and timed out in 4 of 10 whole-suite runs: A6 NEW red on a correct patch. Re-run the same brief; do not count it as a round.
4. Spark re-sample is not deterministic (P2 r1 byte-identical vs r2 missing header line).
5. code_patch2 cannot carry a generated product outside the service (KS-1796).
6. git clone --shared of the cache HEAD is a workable scratch clone given the hook refuses `git -C ... checkout`.

## Control/round log
ctl1_p1 FAIL (ks949 x2 timeouts) ; ctl2_p1 FAIL (ks949 once) ; ctl2_p2 PASS ; ctl2_p3 FAIL (baseline ks949 flake + my splice defect, KS-1000) ; ctl3_p3 PASS ; ctl3_p1 PASS. Real: rnd1_p1 PASS, rnd1_p2 FAIL (ks949), rnd2_p2 PASS, rnd1_p3 PASS. KS-1796 dry-run REFUSED. Model times 68.7 / 87.1 / 80.9 / 74.6 s.

## UNMEASURED
Whole-suite run with all three passes applied together; real Redis / Postgres / Node 24 process behaviour on an unhandled rejection (read, not run); docker/prod; eslint; the KS-1796 test and any consumer reaction to a new 422 (gateway spec method map, Schemathesis, docs fragments); BSD vs GNU patch on the raise seat's machine (use git apply -C1); live lanes beyond open PRs; Seat S 10th's listing itself (not re-read; the three sites were re-found by grep at the tip).
