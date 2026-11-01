# Spark operator 54, 2026-11-02: KS-1868 security key-register save catch (1 held), auth users.ts change-password (1 STOPPED)

## BLUF
O54-P1 HELD (PASS 7/7, TREE-IDENTICAL to golden, original brief, control PASS first time, no rebrief). O54-P2 STOPPED at the open-PR scan, not briefed: open PRs 1796 and 1798 both list services/auth/src/routes/users.ts. Tip: develop 03977e89a343ad7362760e4fb0270602fb6da5ce at start (ls-remote 07:0x) and at end (07:11), unchanged. Scan: start and end 19 PRs / 108 files; planted controls services/auth = 7, services/security = 2 both times; services/security/src/index.ts in no PR; no KS-1868-titled PR. Lanes beyond open PRs not checked. The model round ran through the queue (queue.md -> keepdraining -> done.md); the control cannot be queued (no flag on a queue line) so it was hand-run, lock free.

## Held (pasted from ls night | grep O54)
READY_KS-1868-KS-1868-O54-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-SECURITY-KEY-REGISTER-SAVE-CATCH-PASS-7of7_2026-11-02.diff.md

## O54-P1 services/security/src/index.ts, POST /api/keys save catch (:1411-1417 at the tip; the changed line anchor :1413)
- hold_ready verbatim: `golden: bytes differ; applied result not compared; touched=2 product_plus=9 product_minus=2 red=2/4 green=4/4 suite=378->382 strict=True`. The "bytes differ" is exactly the missing first header line `diff --git a/.../index.ts b/.../index.ts` (diff of patch.diff vs golden.diff in patch_vs_golden.out is that one line); done.md calls it TREE-IDENTICAL. Model 81.8 s, 42935+2348 tok.
- Today vs after (read at the tip; gate 90 G90-F4 measured the "today" side): an INSERT rejecting with an unreadable value throws inside the catch (isInfrastructureDbError reads e.code/e.message; saveErr?.code). No KS-888 line; generic 500 "An unexpected error occurred"; no key issued, ROLLBACK, nothing committed, unhandled = 0. After: KS-888 line logged (infra false, no code), 500 INTERNAL_ERROR "The API key could not be saved, so no key was issued". An ordinary non-infra Error already gets exactly the after state (test cell C1 pins it, R1/R2 assert the same expectations), so no new outcome; 503 is never produced for an unreadable value.
- Reachability note: the catch is reached with the RAW value only on the rotate path (saveKeyAndRetirePriors/transaction() rethrows raw). On the non-rotate path dbSaveApiKey's own catch reads `err?.message` first and so converts an unreadable value into a TypeError (an ordinary Error) before the route catch: a different read, not touched (it is its own KS-1868 site, :479).
- Callers: the route itself (:1176, requireKeyAdminOrProvisioner); production caller is the gateway register-connector (platform.ts).
- BEHAVIOUR CHANGE text for the PR: "When the rotate INSERT rejects with a value that cannot be read, POST /api/keys today loses the KS-888 log line and answers the generic 500 'An unexpected error occurred'; after, it logs the KS-888 line (infra: false) and answers 500 INTERNAL_ERROR 'The API key could not be saved, so no key was issued', the same as any ordinary non-infrastructure Error. Fail-closed unchanged: no key issued, nothing committed."
- Tier: 1 (security surface, auth/security file) by default; recommend tier 1 Opus gate.
- Same-file siblings NOT in this pass (same unguarded isInfrastructureDbError read): revoke save catch :1582-1583 and admin-scopes catch :1773. Candidates for a further pass, not briefed.

## Raise-seat notes
- strict=True: plain `git apply` works. One product hunk (@@ -1410,8 +1410,15 @@) plus one NEW test.
- Test file: services/security/src/__tests__/ks1868-security-key-register-save-catch-unreadable-throw.test.ts (4 cells: C1 ordinary Error, C2 normal rotate 201, R1 revoked Proxy, R2 throwing message getter). It is route level (real app on loopback + real RS256 token, ../db stubbed), so it also closes gate 90's G90-F2 shape for this site. Ref used by the checker: ks1868-security-save-key-and-retire-priors-unreadable-throw.test.ts (PR 1908). Suite baseline 378 -> 382.
- Comment line inside the empty catch is part of the hunk.

## O54-P2 services/auth/src/routes/users.ts change-password, revoke catch (~:1027-1034) - STOPPED, not briefed
Reason: open PR 1796 (Refs KS-1458, ks1006 comment/header/userRepo import/auth baseline) and open PR 1798 (Refs KS-1459, users.ts canonical level order) both list services/auth/src/routes/users.ts (prscan_start.out, prscan_end.out; unchanged at end). Per commission, STOP. Site read for the record: today an unreadable throw from revokeAllUserSessions escapes the catch as a TypeError and the outer catch hands it to next(error) (generic 500, password already written); an ordinary Error already gets ServiceUnavailableError 503 "Your password WAS changed, but ...", so the fix would NOT be a new outcome; it is brief-able once 1796/1798 merge (same shape as O50-P3). Also in the same file: :838 revokeAllUserSessions call, not examined.

## Round log (done.md rows)
- control: ctl1_p1 CONTROL-PASS 07:07 AEDT, 44 s, no model, golden BYTE-IDENTICAL.
- queue line appended to spark/queue.md ~07:08; Spark picked it up from the drainer.
- done.md row (copied to done_rows.txt): `2026-11-02 07:10:26 | ks_1868_o54_p1_... | PASS (7/7) | 128 s round | 81.821 s model | 42935+2348 tok | TREE-IDENTICAL`. Preceding rows from op53: 07:01, 07:04, 07:05. The drainer began op55's billing round straight after (queue.log 07:10:32), so no Spark idle gap was observed on my side.
- hold_ready 07:1x -> HELD.
- Spark busy time attributable to me: 81.8 s model time (128 s round wall). Nothing else queued: P2 was stopped.

## UNMEASURED
Whole-suite run with the patch in the full monorepo CI; real Postgres/transaction() (the stand-in is the 1908 style); eslint; the 503-never-produced claim for other fault shapes (read from source); lanes beyond open PRs; the P2 behaviour (read, not run); revoke :1582 and admin-scopes :1773 siblings.
Artifacts: gen/mk54.py, gen/t54_p1.ts.txt, gen/prscan54.py, lint_p1.out, dry_p1.out, ctl1_p1.out, rnd1_p1.out, hold_p1.out; brief dir night/briefs/ks_1868_o54_p1_security_key_register_save_catch_unreadable_throw/.
