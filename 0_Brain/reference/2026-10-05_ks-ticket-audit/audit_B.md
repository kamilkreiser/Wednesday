# KS ticket audit — auditor B (older half of Backlog+Todo), 2026-10-05

**Partition:** KS tickets that are not archived and in state Backlog or Todo: 276 in the snapshot, sorted by createdAt ascending. B takes the first 138: **KS-61 (2026-05-14) through boundary KS-1012 (createdAt 2026-09-08T12:28:43.064Z)**. C starts at KS-1014 (2026-09-08T13:17:01.682Z). The 138 split as 115 Backlog and 23 Todo. **Rows written: 138 of 138 expected** (`audit_B.tsv`, 13 columns).

**Code instrument:** origin develop `3ce8cd4026a6`, which matches `ls-remote` at audit time. It was read in a `--shared` scratch clone; nothing under `!CODING` was written. Linear and GitHub were used with GET/GraphQL reads only.

## BLUF — counts per class

| Class | n |
|---|---|
| TEST-OR-TOOLING | 55 |
| NEEDS-HUMAN | 30 |
| GENUINE-HARDENING | 28 |
| GENUINE-DEFECT | 9 |
| ALREADY-FIXED | 8 |
| NOT-GENUINE | 5 |
| UNVERIFIED | 3 |
| DUPLICATE | 0 |

**ARCHIVE:**
- **yes: 5.** KS-618 · KS-777 · KS-953 · KS-977 · KS-997.
- **ASK: 2.** KS-607 (Stuart created it) and KS-982 (Peter is assigned). Both are ALREADY-FIXED.
- **no: 131.**
- KS-768 is ALREADY-FIXED in its core (PR #796), but archive is **no**: a residue remains at `scripts/preflight/lockfile-cleanroom.sh`, which still walks 4 dirs. Open that residue as its own ticket before archiving.

**Parents:** archiving KS-770 would cascade to 12 children; KS-772 to 17; KS-485 to 12; KS-492 to 9. None of these is marked yes.

**Answer to Kam's question:** the old half is mostly *real but not product-breaking*.
- Only 9 tickets in 138 are provable product defects at develop.
- 55 are test, harness, CI or process work.
- 30 are waiting on a human decision, not on code.
- Outright not-genuine is small (5). The bigger noise is tooling and process tickets that sit on a product board.

## Genuine defects — all 9, ranked by risk to "stable by 31 Oct"

1. **KS-1005 — no user can change their password.** The route calls `getUserById`, but the `USER_COLS` it selects leave out `password_hash`, so `passwordHash` is always undefined and the route throws 404. A variant that includes the hash already exists (`getUserByIdWithPasswordHash`, `userRepo.ts:440`) and is not used here. The cause is `services/auth/src/routes/users.ts:966-967` plus `repositories/userRepo.ts:346,409`. *Re-read by B.*
2. **KS-938 — disabling MFA leaves the TOTP seed and backup codes in the row.** The disable code passes `undefined`, and `updateUser` skips undefined fields, so the old seed can be re-armed later. Sites: `mfa.ts:241-242,376-377`, `users.ts:1116`, `userRepo.ts:827`. *Re-read by B.*
3. **KS-1009 — anonymous `GET /api/auth/wallet/status/:addr` returns userId, role and createdAt.** A public wallet address resolves to an internal id and role, which is an enumeration surface. Code at `wallet.ts:403-428`. Akto independently rated it HIGH. *Re-read by B.*
4. **KS-735 — the verifier ResultPage never shows the document title or issuer.** The card is gated on `result.document`, which the API never emits (`frontend/verifier/src/components/ResultPage.tsx:423`). Users see this directly and Stuart raised it. Peter has to choose the contract shape.
5. **KS-625 — `/api/presentations/verify` never checks the holder signature.** It compares challenge and domain only, and only when the caller supplies them; `// In production, verify the cryptographic signature` is all that is there. Code at `services/vc-issuer/src/routes/presentations.ts:321-328`, and the gateway routes to it. *Re-read by B.* This is critical only if VP verify is in the demo scope.
6. **KS-758 — the connector-erasure "unresolvable" branch returns `completed` with no `data_deletion_log` row.** That is a GDPR audit-trail gap (`originate/src/services/gdprService.ts:1473-1488`). Separately, config-fault 403/500 responses never dead-letter.
7. **KS-757 — the erasure re-drive SELECT takes no lock.** Overlapping Platform S retries can drive the same request twice (`gdprService.ts:1371-1378`).
8. **KS-593 — fuzzed input still produces raw 500s.** `admin/create` lowercases an email it never type-checks (`users.ts:592` → `userRepo.ts:641`).
9. **KS-565 — a negative offset gives a 500 at 6 sites in 4 services** (`users.ts:456,512`, `adminConfig.ts:1104,1264`, tenant-provisioning `index.ts:556`). It overlaps KS-593 but is not a duplicate.

**Critical-path items that are not code defects:**
- **KS-749** — a baseline fuse fires on **15 Oct** and blocks pushes that touch `Blockchain/Dev` (`audit-baseline.json:146-151`).
- **KS-1012** — the ruleset requires 0 approvals and lets admins bypass always. The 7 dead required checks are now gone (live GET).
- **KS-889** — Kam and Stuart need to re-mint Platform S keys before the KS-843 erasure-scope flip; a backfill was measured as impossible.
- **KS-658** — the demo runs `NODE_ENV=development` on 26 services. This is Kam's decision.
- **KS-915** — there is no first-admin bootstrap path for a fresh production stack.
- **KS-960** — the two schema sources disagree.
- **KS-1003** — `/api/oauth/` is outside the credential-stuffing zone in nginx.
- **KS-723** — S's anchors hot path is still missing from the spec.
- **KS-955** — a fresh clone cannot run the four suites.
- **KS-987** — a deploy can publish a stale contract silently, because of the single-file spec bind mount.

## NOT-GENUINE patterns

1. **Agent process and incident notes filed as product tickets:** KS-765 (an agent merge-helper SHA fallback), KS-866 (a merge-race incident whose fix is already ruled), KS-995 and KS-996 (Linear archive-cascade behaviour and a board-hygiene measurement).
2. **Tickets against a PR that never merged:** KS-678 was filed on PR #568, which closed unmerged. The develop spec has 0 `secuura.io` occurrences.
3. **Two more patterns, not counted as NOT-GENUINE because they are real:**
   - About 20 "gate integrity" and "a test can be green vacuously" tickets: KS-709, 752, 825, 829, 837, 939, 940, 948, 951, 967, 998, 1000, and others. They are about the agents' own harness, not the platform.
   - Several decision tickets (`[Decision]`, BM-*) that are product requirements, not problems.

## Could not verify

- **KS-591 and KS-595** need a live Schemathesis sweep at develop.
- **KS-636** needs a trivy scan of a fresh `node:24-alpine` pull.
- **KS-919 and KS-959** (and the measured numbers in KS-699 and KS-748) depend on the live demo database, which this audit could not read.
- **KS-954** needs a live check of the billing `//` 404.
- **KS-638**'s verdict bug lives in `secuura-extranet`, which was not read.
- **KS-683**'s S-side PR #581 is in another repo and was not checked.
- **KS-562** was not re-run; it was classed from its 09-25 comment.

## Method and controls

- **Pull.** Description, all comments (`first:50`, sorted client-side), attachments, relations and children were pulled for all 138 tickets.
- **Reading.** The ticket set was split into four contiguous chunks, each read by a fork of this auditor against the same spec. Every ticket that cited code was read at `3ce8cd4026a6` and given a file:line cite.
- **Merge checks.** PR merge state comes from GitHub `merged_at` (for example #678, #795, #796, #892, #1000 and #1215 were all confirmed merged). Duplicates were searched by symbol, path or error string with Linear `searchIssues` (archived included); 0 duplicates were found.
- **Controls:**
  - (a) B re-read the code for 5 cited claims itself: KS-1005, KS-938, KS-1009, KS-625 and KS-618 (the nginx realip block at `docker/nginx-gateway/nginx-demo.conf:100-107` plus #678 merged 2026-08-13). All matched the cites.
  - (b) All 138 ids are present once each, with 13 fields per row.
  - (c) No `yes` archive is on a ticket Peter or Stuart created or is assigned to.
  - (d) Every NOT-GENUINE, ALREADY-FIXED or DUPLICATE row rests on more than the title: either the description, or a code or PR cite.
- **Limits.** The per-row "critical path" judgement is the forks', not separately re-checked. The prior spark screens were treated only as pointers; they rank briefability, not genuineness.
