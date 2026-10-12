# QA gate: PR #1481 (KS-1457), head 614efee94e62e48af28d8ea1afeb3b8d6ec15048, 2026-10-12

## VERDICT: GO WITH NOTE
Code change is correct, minimal and safe. The "bug is LIVE in production" claim is only half true (see defect 1).

## Method
Own clone in scratchpad (fetched head from origin, which has it as refs/pull/1481/head; no ref writes in the shared repo).
Develop moved to 5bfa5a804 (only auth/originate files); I merged it with the head: clean, diff vs develop = exactly the 2 PR files
(predicted tree d3d96877). I built @secuura/shared fresh in each of my trees (the shared stale dist otherwise fails 11 files; env, not PR).

## Confirmed (my runs)
1. Diff vs d38302a9: audit.ts +5/-3 (three reads -> auditPath: lines 263, 290, 335) + 1 test file. Nothing else. 3 commits as described.
2. Base source + head test: 4 red (A1, B1, B4, C1), 5 green incl. controls A2 B2 B3 C2 and completeness. (Tests-first commit alone: 3 red per seat; B4 came later.) Head: 9/9.
   Tampers (head src, one read put back to req.path): A1 -> only A1 red; email -> B1 and B4 red only; warning path -> C1 only.
   My own tamper (email gate widened to startsWith('/api/auth/')) -> only B3 red. Restored: 9/9, tree clean.
3. Gateway suite head AND predicted merge: 107 files / 1019 tests, 0 failed (KS-871 cells included). tsc rc 0, eslint rc 0 on both.
   Control: eslint on a file with `var`/`debugger` -> 2 errors (so the 0 is not blind).
4. Semantics: auditPath === req.path at entry, and differs at finish only behind a responding router.use gate. Matching stays exact:
   trailing slash and case variants fell out of the login match before and still do (unchanged; case variants are not audited at all, KS-1191).
   attemptedEmail is only taken at the login path (B3 control + tamper D), lower-cased, from a string field. No password/token in rows
   (my harness posted password hunter2: absent from every row). Written inside JSON.stringify, so no log/JSON injection; the warn log does not carry the email.
   No NEW rows: on the base source the 429s already produced one audit row each (prodshape_rows.txt, "wb" lines); only the email field changes.

## Defects
1. **Minor (claim accuracy, not code)** `ks1457-...test.ts:15-17` and B4 `:126`: the "live in production, lost attemptedEmail" claim does not hold.
   index.ts:385 lists `/api/auth` in proxyPaths and index.ts:399-402 skips body parsing for it, so `req.body` is undefined at audit finish in
   production: attemptedEmail is never written for /api/auth/login, throttled or not, before or after this PR. B4 passes only because the test
   mounts `express.json()` globally (`:47`, `:126`). My prod-shaped harness (same gating, real limiter): head and base both produce rows WITHOUT
   attemptedEmail (prodshape_rows.txt, PRODSHAPE lines); with a parser on (CONTROL lines) base loses the email on 429s and head keeps it.
   What IS live in prod: only C (write-failed warning logging path '/' behind the limiter). A is latent (proxy streams, 200 body never via res.json).
   Fix: reword the header/PR text; optionally make B4 mirror the proxyPaths gating. I could not check the deployed box.
2. **Minor, separate ticket (pre-existing, not this PR)** H29 attemptedEmail is dead in production because of defect 1's cause (index.ts:385/399).
   Note for the follow-up: if someone enables parsing there, throttled attempts will store an unvalidated email up to 1 MB each (audit.ts:290-292, no length cap)
   with no per-IP cap on audit rows beyond the global limiter (300/min). Cap length when it is turned on.

Not checked: deployed gateway, real audit_logs rows, GitHub CI.
Evidence: scratchpad r2.out/r3.out; prodshape_rows.txt in this folder.
