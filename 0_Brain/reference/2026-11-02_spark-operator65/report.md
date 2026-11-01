# Spark operator 65, 2026-11-02: KS-1868 originate repositories (2 held, 10 sites skipped, 0 failed model rounds)

## BLUF
HELD: O65-P1 (certificationRepo.ts verifyDbReady :60) and O65-P2 (documentRepo.ts verifyDbReady :141), the only two of the 12 assigned sites that meet the strict rule. Both model rounds PASS 7/7 on the original brief, golden BYTE-IDENTICAL, strict=True. SKIPPED: the other 10 sites (reasons below). Numbering: with 1 hunk per file, the passes are P1 = certificationRepo, P2 = documentRepo (not P1-P4). Tip 03977e89a343ad7362760e4fb0270602fb6da5ce at start (tip_start.out) and end (tip_end.out). Open-PR scan start and end: 22 PRs / 125 files, no entry under src/repositories/ (prscan_start.out, prscan_end.out); planted control printed 11 entries both times.

## Held (held_files.txt)
READY_KS-1868-KS-1868-O65-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-PASS-7of7-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O65-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-PASS-7of7-PASS-7of7_2026-11-02.diff.md

## Per pass
Both: one hunk; inline `let reason` guard (the shape already merged in originate routes/certifications.ts); no helper added. The catch logs, then throws a CONSTANT Error, so the thrown value never leaves the function.
- O65-P1 certificationRepo.ts :58-61. hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=7 product_minus=1 red=2/5 green=5/5 suite=1999->2004 strict=True`. Test: src/__tests__/ks1868-certification-repo-verify-db-ready-p1-unreadable-throw.test.ts (db stub passed as the `db` argument, mocks ../db and the logger).
- O65-P2 documentRepo.ts :138-141. Same hold_ready line (suite 1999->2004). Test: ks1868-document-repo-verify-db-ready-p2-unreadable-throw.test.ts. @secuura/shared is deliberately NOT mocked (a hand-written factory fails ks1061-shared-mock-completeness; this was my golden's first fault, see round log).
- Callers (callers_cert.out, git grep at the tip, positive control = the definitions and tests are found): src/index.ts :411/:412 `Promise.all([...]).then(...).catch(err => logger.warn(..., { error: err?.message }))`; certification also via routes/certifications.ts :70 `initRepo().catch(log message)`. Both only log. Documents: no other non-test caller.
- BEHAVIOUR CHANGE for the PR: for an unreadable thrown value only, the rejection reaching the startup `.catch` goes from a TypeError to the constant Error `Database is required for <certification|document> operations` (what an ordinary Error already gives), and the repository now writes its own `database connection FAILED` line with `error: 'unreadable thrown value'` where today it writes none. No response, persisted state or verdict changes. Ordinary Errors and strings behave as today (cells C1, C2; existing certificationRepo.test.ts / documentRepo.test.ts pin the ordinary path).
- Tier: 2 (startup readiness log only).

## SKIPPED (strict rule)
- certificationRepo.ts :176 getCertification, :308 saveCertification, :354 saveShare; documentRepo.ts :260 getDocument: the catch FIRST reads `err?.message?.includes('invalid input syntax for type uuid')` (a second unguarded read; fixing only the log line is half a fix, same as the Zod pre-check class) and then RETHROWS the original value.
- certificationRepo.ts :200 listCertifications, :378 getSharesByCertification; documentRepo.ts :292 listDocuments, :512 saveDocument outer catch, :691 updateDocument: log then `throw err`. Today a hostile value becomes a readable TypeError; after, the HOSTILE value itself propagates to the route. Routes whose catch is unguarded (certifications.ts :1000 list route, :1584 lineage, :1692 evidence bundle, all `error instanceof Error ? ...`) would then throw inside their own catch: a 500 becomes a hang. That is a verdict/response change an ordinary Error does not produce. Not briefed. (The saveCertification / saveDocument / updateDocument paths are custody writes: certification and document persistence.)
- documentRepo.ts :498 (fkErr message read inside the FK-retry loop): the read drives control flow (retry with null owner vs rethrow) of a custody INSERT; guarding it changes which branch a hostile value takes. Skip.
- Not all callers of the document write/read sites were traced individually: the skip is by the rethrow rule plus the certifications.ts route catches above; documentRepo callers (many routes) were not enumerated (UNMEASURED).

## Raise-seat notes
strict=True both; each pass touches a different file, any order, one PR possible. Refs KS-1868 only. Reds R1/R2 per pass; controls C1 (ordinary Error), C2 (string), C3 (healthy db). Test names start `RED ks1868 R1/R2`, `control ks1868 C1/C2/C3`. Hunk distances: single hunk each.

## Round log (done_rows.txt)
- Controls queued 08:5x behind o64/o66 rounds (queued_controls.txt). 08:54:17 CONTROL-PASS P1 (106 s). 08:57:00 CONTROL-FAIL P2 (161 s): A6 NEW red ks1061 (my golden test mocked @secuura/shared by hand; checker.out copied to p2_ctl_checker.out). The golden test (my file, not model output) was fixed, P2 regenerated, re-linted, dry run rc 3 BUSY, control re-queued: 09:03:26 CONTROL-PASS P2 (110 s). No model round had been queued behind the failing control.
- P1 model: queued 08:55, PASS 08:59:32 (151 s round, 36.4 s model, 15117+1395 tok). P2 model: queued 09:03, PASS 09:09:26 (170 s, 53.7 s model, 32463+1380 tok). Harness baseline 1999/0, after 2004.
- Counter: 1 original brief per pass, 0 rebriefs (the one P2 golden fix was before any model round).

## UNMEASURED
Whole-suite CI beyond the harness A6; eslint; real Postgres; whether an unreadable value is reachable in production; patched behaviour of the 10 skipped sites (read only); all callers of documentRepo's skipped functions; the second dry run of P2 (rc 3 BUSY, input not rebuilt before the control, which passed).
Evidence: this folder (tip_*, prscan_*, open_prs*.json, lint_*, dry_*, hold_p*.out, held_files.txt, done_rows.txt, callers_cert.out, *.tip.ts, gen/).
