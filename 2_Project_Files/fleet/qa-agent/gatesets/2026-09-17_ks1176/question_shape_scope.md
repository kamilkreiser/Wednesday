SUBJECT: [Secuura/Blockchain -> Wednesday] QUESTION: KS-1176 shape and scope
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TIMESTAMP: 2026-09-16T19:50:58.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat A

## BLUF
- KS-1176 is assigned to the board account; it stays in Backlog. The census at develop e0f41a8fa reaches past the two sites your brief names: three more level-order consumers sit in my partition. So, per the brief, I am asking before building.
- **Proposal: Peter's shape (1), gateway only.** In `meetsVerificationLevel` (`services/api-gateway/src/services/enforcement.ts:53-57`), an unrecognised user level (`api_key` included) satisfies a `none` requirement and nothing higher. One product file; the order array does not change.
- Why (1):
  - It cannot grant more than an anonymous caller already gets: with no user at all, `enforceDocumentTypeRules` already passes a `none` type (`enforcement.ts:136-141`).
  - Every non-`none` requirement still refuses a connector key.
  - The verifier gate at `routes/verification.ts:554-557` only compares when the verifier level is not `none`, so (1) changes nothing there.

## Recommendation
Question: do you approve shape (1), gateway only, with the other three level-order copies recorded in the READY but not edited?
Meanwhile: the KS-1176 build is BLOCKED on this. I am doing read-only prep for A15 KS-1018 (no branch, no commit) and re-checking the inbox every ~3 minutes.
Needed-by: no hard deadline. This is approval-class (an auth design choice), so I wait however long it takes.

## Detail

### Census at e0f41a8fa
Method: git grep over Blockchain/Dev, non-test files unless stated. Every cited line range was re-read at source.

**Who produces the `api_key` level:**
- gateway `middleware/auth.ts:276-277`: the sk_ key principal gets `verificationLevel 'api_key'` and `authMethod 'api_key'`. `:307` forwards `x-verification-level: api_key`.
- auth `services/jwt.ts:269` and `:293`: the connector JWT carries `verificationLevel: 'api_key'`, `type: 'connector'`.
- Gateway JWT principals default to 'BASIC' (`middleware/auth.ts:146`).
- `x-verification-level` has 0 consumers in any service.

**Who consumes a level order:**
1. **gateway `enforcement.ts:39-47` and `:53-57`: THE TARGET.**
   - `:145` inside `enforceDocumentTypeRules`, called at `routes/verification.ts:1223` in `POST /api/documents` (`:1123`).
   - `routes/verification.ts:557` in `POST /api/documents/:id/verify` (`:483`), injected via `index.ts:894`. It only compares when `verifierVerificationLevel` is not `none` (`:554-555`).
   - Tests: `enforcement.test.ts:56-72` pins the array with `toEqual` (shape (1) leaves it untouched); 13 test files mock `meetsVerificationLevel: () => true`.
2. **auth `middleware/authenticate.ts:193-208` `requireVerificationLevel`,** over auth's own uppercase order (`types/index.ts:26`). Same -1 semantics, so a connector token would fail any level. **0 production call sites**; 8 auth test files mock it.
3. **shared `middleware/index.ts:157-176` `requireVerificationLevel`,** over its own uppercase array. Same -1 semantics. **0 callers** beyond the shared export (`src/index.ts:163`).
4. **shared `verification/policy-engine.ts:22` order.** `levelIndex` (`:110-113`) already maps an unknown level to 0 (NONE), so it already behaves like shape (1). Used by `evaluatePolicy` (`:149`), then `evaluatePolicies`, then `requirePolicy` (`middleware/index.ts:193`): **0 callers**.
5. **NOT my partition, report only:** `frontend/issuer/src/components/DocumentUpload.tsx:74-78`. The upload pre-check has the same -1 semantics; it runs in human sessions.

**A machine-principal notion already exists:** `api-gateway/src/middleware/rateLimitEnforce.ts:61` defines `MACHINE_AUTH_METHODS = {'api_key','oauth_app'}`. Nothing in non-test source produces `authMethod: 'oauth_app'`.

### The three shapes, against the sites
- **(1) an unknown level satisfies `none` only.**
  - `:145`: connector keys pass `none` types (SSD_DOCUMENT) and still fail every higher type.
  - `:557`: unchanged, because it never compares against `none`.
  - The array is untouched, so `enforcement.test.ts:56-72` stays green.
  - Peter's three cells hold, including "an arbitrary unknown string behaves as `api_key`".
- **(2) place `api_key` in the order.**
  - At index 0 it equals (1) for `api_key` alone, and the `toEqual` pin goes red.
  - Anywhere higher, a machine key is ranked against human KYC levels, and verifier-gated types at `:557` open to connector keys.
  - Peter calls this a product decision.
- **(3) machine-principal short-circuit (Stuart's lean on PS-519).**
  - Skipping the comparison for `api_key` lets a connector key originate a STANDARD/ENHANCED/HIGH-gated type and pass the `:557` verifier gate at any level. That is broader than the bug.
  - Keyed on `MACHINE_AUTH_METHODS`, it also pulls in `oauth_app`, which is an OAuth design question.

### A pre-existing fail-open the census surfaced (not KS-1176; yours to route)
READ only, not measured:
- With an UNKNOWN *required* level, `reqIdx` is -1, so `userIdx >= -1` is true for every authenticated principal.
- originate's `POST /document-types` (`routes/adminConfig.ts:156-160`, outside my partition) checks only `name` and `code`, then stores any level string.
- So a mistyped requirement (e.g. `standrd`) would admit every authenticated caller, connector keys included. An anonymous caller is still refused (`enforcement.ts:137`).
- I have not traced how the gateway's Redis catalogue is filled from those rows.
- Shape (1) as proposed leaves this unchanged. I would record it in the READY. No board search has been run for it yet.

### Baselines at e0f41a8fa
Worktree raise-0916-a, detached; shared dist rebuilt, rc 0.
- api-gateway 48 files / 410 tests; shared 44 / 851; auth 61 / 745. 0 failed, 0 skipped, 0 pending in each.
- tsc --noEmit: api-gateway rc 0, auth rc 0, both with empty output.

### Since my last mail
- Vault: 09-11 and 09-14 committed per your ANSWER as 2811299b3e1fb4bd82021b0f1e1d69afa3785145. Origin main = local; vault porcelain 0.
  - grep -i -w per term: 0 hits in both files.
  - Controls: 1/1 per term; `-w vision` = 3 on the workspace CLAUDE.md.
  - fetch 0 behind before the commit. Secret check: 0 of 13 values, 0 patterns.
- develop e0f41a8fa and #1011 head 6dc825644 are unmoved (ls-remote 19:4xZ). No GO or NO GO for #1011 yet.
