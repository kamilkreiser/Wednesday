# Candidate defect VERIFIED REAL (read-only, code at develop 06328efa1770): a self-registering user can join any EXISTING organisation

Found by Seat D 73rd (2026-11-19, live-check sweep, unverified note); verified by a read-only Sonnet subagent of the 19 Nov afternoon Wednesday seat (gh api reads at 06328efa17703b41ddd0107046b00c82dd235a92, kksecura). Nothing was run against any server. Paths under Blockchain/Dev/.

VERDICT: REAL at schema, handler, DB and token level; UNCLEAR on the exact reach (data reads by a joined OWNER, cross-tenant).

1. services/auth/src/routes/auth.ts:152 — register schema `organizationId: z.string().guid().optional()`: only a GUID check.
2. Handler ~175-224 — gates: role-field rejection, email 409, strength, breach check. NOTHING checks organizationId (existence, membership, invitation, tenant).
3. :254 — `organizationId: data.organizationId` written; role hard-coded OWNER (~246); tenantId from the gateway's x-tenant-id; repositories/userRepo.ts ~691-724 inserts organization_id.
4. register returns 201 with an access token BEFORE email verification; services/jwt.ts:197 and :223 copy organizationId into the token claims.
5. migrations/001_initial-schema.sql:531 — users.organization_id UUID REFERENCES organizations(id): plain FK, no tenant link; users RLS (migrations 009, 038, 039) is tenant-only.
CONTRAST: the admin PATCH services/auth/src/routes/users.ts ~803-812 (KS-467) requires the org to exist and be in the caller's tenant; register has no equivalent.
REACH (token org trusted by): m365-integration index.ts ~397-430 (requireCallerOrg binds connections/sites/documents to the token org, "no bypass for any role"); originate routes/documents.ts:570, :142, :176, :123, :454; anchoring anchorReadGate.ts:125; security src/index.ts:1739; keyRevokePolicy.ts:231; auth middleware/authenticate.ts:248 requireSameOrganization.
BLOCKERS SEEN: OWNER is not in security KEY_ADMIN_ROLES (index.ts:1187); cross-tenant RLS on org-owned tables UNVERIFIED; org ids are UUIDs (an attacker needs a valid id first).
TESTS: none found pinning organizationId on /register (searched files matching 'regist').
NOT ESTABLISHED: org-scoped query behaviour for a joined OWNER; cross-tenant block; bad-FK status code; emailVerified enforcement; org-id discoverability.
Scratch copies of the read files: /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d327cd11-b29f-4b08-aa98-071329018ac4/scratchpad/orgcheck/ (session scratchpad: NOT durable).

NEXT (Wednesday): (1) a board seat searches the KS board for an existing ticket (by symbol: register organizationId, KS-467) before filing; files High if none; (2) a BUILD seat on OPUS (routing row C3: auth surface) with red-first cells: register must not accept a caller-chosen organizationId (strip or refuse); STOP and QUESTION if any consumer (Platform S, admin frontend, e2e fixtures) sends organizationId on register (consumer census first); tier-1 Opus gate; (3) tell Peter on the ticket after the fix (BLUF), per 2026-10-08 fix-our-own-problems.
