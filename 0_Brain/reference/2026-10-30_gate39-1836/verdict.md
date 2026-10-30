## QA GATE - TIER 2, round 1: GO WITH NOTES
(Filed by the Wednesday seat from gate 39's returned text, 18:2x AEDT. Probes in `probes/` beside this file.)

**Subject:** PR #1836, KS-1807 PR-2, docs only (WORKFLOWS.md, QUICK-REFERENCE.md, VOCABULARY.md), author Seat V 11th. **Head** 3974f364cbc8 at 18:16 and 18:24 AEDT; parent 85cd24d81cb9; develop e43a289c1c7b. Net diff the 3 docs (+184/-121). Gate 39, Sonnet, tier 2. Clone `repo/` (git init + depth-50 fetch of the two refs).

### Verdict
~60 behaviour sentences read against handlers, middleware and error mappers; 34 in the claims table. None flatly FALSE; 2 false/contradictory in a way a reader would act on (wording-only fixes). The issuer-certs class did not recur: every "gateway stand-in answers first" claim traced to a real ungated mount ahead of the proxy.

### FIX BEFORE MERGE (wording)
- **FIX 1 (WF:71 vs WF:70/72):** WF:71 says create needs a DOCUMENT_WRITE_ROLES role or documents:write else 403. That check lives only in originate (documents.ts ~388). The GATEWAY handler (api-gateway verification.ts 669-880) answers 201 pending_approval for approval-gated types after only authenticateToken(true), the connector-scope check (API-key callers only), type rules and the verification level, and never calls originate. So an authenticated NON-write-role caller gets 201 on an approval-gated type. **Read from code, not run.** Wording fix: "On the originate path: needs …; the approval-gated 201 is returned before this check runs." **The behaviour itself is a candidate authorisation finding (Wednesday: filed via V 11th).**
- **FIX 2 (QR:179):** labels OWNER admission to POST /admin/credits "Known deviation (KS-1850)"; merged PR-1 (ROLES-AND-AUTHORIZATION-INVENTORY.md:125) says UNDECIDED, "Do not assert either behaviour until ruled". Reuse the PR-1 UNDECIDED wording.

### FOLLOW-UP / INFO
- F3 error tables omit emitted codes: create 401; 403 (connector allow-list / organizationUuid mismatch / DOC_TYPE_DISABLED / MFA_REQUIRED / AUTH_PROVIDER_NOT_ALLOWED); 409 CONFLICT; 502/503/500. Anchor: 403 PENDING_APPROVAL (gateway blockPendingApproval), 404, 503 in production when anchoring is unreachable (dev records failed + 202), 403 FORBIDDEN missing from the table. Verify: 400 express-validator branch. KYC initiate: 400 consent-false + Zod 400.
- F4 WF:77 "an admin" = only system_admin/SYSTEM_ADMIN/super_admin (ORG_ADMIN, ISSUER_ADMIN non-owners get 404).
- F5 verify: verified:true also from documentData and the chain fallback; the title-hit answer carries no warning.
- F6 WF:76-77 assert re-anchor semantics inside an ON HOLD step (leaky hold boundary); WORKFLOWS steps 4-5 were rewritten, not byte-unchanged (disclosed as "not re-verified").
- F7 info: 415 exceptions (application/*+json, form-encoded token endpoint, octet-stream verify-file); unknown export type 202 then fails async; export status from an in-memory map; ADMIN_USER_EMAIL override. F8 commit 0338bd327 unverifiable in a shallow clone (behaviour TRUE).
- Row 10 PARTIAL: /api/v2/verification is NOT exempt from the global limiter (READ_ONLY_PATHS is /api/verification only).

### Q4 ON HOLD: VOCABULARY anchor-rows section and the KS-1175 note byte-identical to the parent (sha-256); QR status-sketch unchanged.
### Q5 KYC (evidence for the owner): approval sets only the KYC record (status approved, currentLevel); NO path from KYC to users.verification_level. The user's level is written by /api/users/me/verification (auto STANDARD with MFA), the admin review /api/users/verification/:requestId/review, MFA enable/disable, admin PATCH. The PR's sentence is accurate.
### Q6: contradicts PR-1 only at QR:179 (FIX 2).

### NOT TESTED
Nothing run (static reading); the 405/401 pre-check derived, not executed; not every one of the 137 identifiers / 32 paths; VOCABULARY verb lists, the "16 actions" count, KS-1454 signatureHash, Docker table, Platform-S statements; deployed state; PR-1 skimmed by grep.
