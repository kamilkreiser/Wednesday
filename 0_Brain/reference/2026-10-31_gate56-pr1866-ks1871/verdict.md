# QA GATE 56: Secuura/Blockchain PR #1866 (KS-1871, Seat S 9th), Tier 1, Round 1
**Head gated: e9f19a55c2183c8cc2195a7bd40c744348edd74f.** `refs/pull/1866/head` was fetched and equals it. It is the merge of develop dc8c210cb29d into fix 4f529d12c617; merge-base dc8c210cb29d. Develop tip now 7da12a4488d5. Between head and develop, `git diff -- Blockchain/Dev/services Blockchain/Dev/packages` shows only this PR's own three files, so develop has added no code since. `git merge-tree --write-tree origin/develop e9f19a55` merges clean (rc 0).

## VERDICT: GO WITH NOTES. No finding needs fixing before merge. No unguarded door.

| File | Change | Gated |
|---|---|---|
| services/api-gateway/src/routes/verification.ts | +34: `canCreateDocument` (a string role, ASCII-folded, in a copy of DOCUMENT_WRITE_ROLES, OR `hasScope(scopes,'documents:write')` over an array of strings); 403 placed just before `createWorkflowInstanceIfRequired` | yes |
| api-gateway/src/__tests__/ks1871-…-write-role-or-scope.test.ts | new, **26 tests** | yes |
| api-gateway/src/__tests__/ks1176-…-ranks-as-none.test.ts | 1 line: HUMAN_STANDARD role ISSUER → ISSUER_ADMIN | yes (Q4) |
| Projects Documents/*.html (2) | +12 / +17 | noted only; they become fragments at merge prep |

**Shape vs Wednesday's ruling** (allowed = a write role OR documents:write): it matches. Wildcards `documents:*` and `*` count through the shared `hasScope`, the same predicate originate uses. The 403 body matches originate's byte for byte (originate documents.ts:389), and D2 pins it.

### Q1: matrix over the real route, over HTTP (probe `probes/g56-create-matrix.test.ts`, rows in `rows_head.json` / `rows_base.json`)
- **Harness:** the real `createVerificationRoutes`, the **real `authenticateToken`**, and the **real `createWorkflowInstanceIfRequired`**.
  - User tokens are RS256 JWTs signed with the suite's throwaway key and verified by the real verifier, so claims land on `req.user` exactly as the middleware leaves them.
  - API keys go down the real `x-api-key` branch, with the security-service validate and the auth connector-token exchange faked at the fetch boundary.
  - originate is a fake on 127.0.0.1 that counts POSTs. `enforceDocumentTypeRules` is stubbed to return a gated or non-gated type. That function is read-only: static read of enforcement.ts, which only calls `resolveDocumentType` and `getAllDocumentTypes`.
- **Axes:** 464 cells, every one run on an approval-gated type and on a non-gated type.
  - **Login JWT:** 57 role shapes × {no scopes, `['documents:read']`}. The shapes are:
    - every role in the codebase: OWNER, ISSUER_ADMIN, ISSUER_APPROVER, VERIFIER, ORG_ADMIN, SYSTEM_ADMIN, SUPER_ADMIN, ISSUER, HOLDER, USER, ADMIN, PLATFORM_ADMIN, admin, super_admin, platform_admin, user, connector;
    - ASCII case variants;
    - leading or trailing space, tab, LF, NUL, ZWSP, BOM;
    - hyphen, no separator, inner space;
    - dotless ı, dotted İ, long ſ, fullwidth, Cyrillic О, Greek Ι, NFD I+U+0307;
    - empty string, `__proto__`, constructor, toString, hasOwnProperty;
    - arrays (flat, nested, two elements), null, 0, 1, true, false, `{}`, a nested `{role}`, and an absent claim.
  - **Login JWT and OAuth JWT** (`authMethod:'oauth'`, `client_id`): {VERIFIER, OWNER} × 25 scope shapes. The shapes are:
    - absent;
    - `documents:write`, `documents:*`, `*`, read+write;
    - `'documents:write '`, `' documents:write'`, `DOCUMENTS:WRITE`, `Documents:Write`, ZWSP;
    - `documents:writex`, `documents`, `documents:read`, `register`, `certifications:write`, `documents:share`, `[]`;
    - the string `'documents:write'`, the space-separated string `'documents:read documents:write'`, the string `'*'`;
    - nested array, `[{}]`, `[null]`, an array-like object, null.
  - **The RFC 6749 `scope` string claim** with no `scopes` array: 3 shapes.
  - **API keys:** 9 scope sets × workflowPolicy {default, bypass}.
  - **A `type:'connector'` JWT presented as a Bearer.**
- **Oracle** (written in the probe, independent of verification.ts):
  - role: `typeof r==='string' && /^(ISSUER_ADMIN|ORG_ADMIN|SYSTEM_ADMIN|SUPER_ADMIN)$/i` (no `u` flag, so non-ASCII never folds to ASCII);
  - scope: `Array.isArray(s) && s.some(x => x==='documents:write'||x==='documents:*'||x==='*')`;
  - the connector gate and bypass behave as in the existing code.
  - The oracle self-check passes.
- **Result at head: 464/464 match** (vitest 2/2). The cells admitted with no write scope are exactly the ASCII case variants of the four write roles. VERIFIER is admitted only with `documents:write`, `documents:*`, `*`, or read+write in an array. Everything else gets 403 with originate's exact body. The scope token format is the `scopes` **array** that auth mints (jwt.ts:192-205; attachScopes is not mounted on this route), so a string or space-separated `scopes`, and the `scope` claim, are refused. A connector JWT used as a Bearer gets 401 (KS-1198) before the route runs.
- **Positive control:** with base verification.ts (dc8c210cb29d) swapped in, **362/464 cells fail**. Base admitted every refused caller on the gated type: 181 cells got 201 `pending_approval` with both store writes. On the non-gated type it forwarded every refused caller (the fake originate admits all). The file was restored and its sha256 asserted (`head_sha256.txt`).
- **OWNER:** S's correction to the ticket holds. A login mint for OWNER carries `scopes:['documents:write']` (auth jwt.ts:192, `getDefaultScopesForRole`), so OWNER keeps 201, as it does at originate. An OAuth OWNER token is admitted only if `documents:write` (or a wildcard) was granted.

### Q2: nothing written on a refused request (instrument: the boundary)
- Every mutating export of `services/redis` is wrapped in a counting spy (`set*`, `delete*`, `add*`, `cleanup*`; 22 functions).
- Also counted: the deps `query` and `dbSaveRejection`, POSTs reaching the fake originate, and every outbound `fetch` other than the key validate and connector-token exchange.
- Across all 380 refused cells (status ≠ 201) (gated and non-gated): **0 redis writes, 0 queries, 0 dbSaveRejection calls, 0 originate hits, 0 outbound calls.**
- Admitted gated cells write exactly `setWorkflowInstance` + `setPendingDocument`. That shows the spies are live.
- Before the guard, the handler only reads: the connector settings and the doc-type enforcement.
- A refused caller can still get enforcement's 400/403 (unknown type, disabled, MFA, level) before the role 403. That is pre-existing ordering and writes nothing (F4).

### Q3: other doors (instrument: grep for writers, route enumeration, then reading each guard)
- **Workflow start:** `createWorkflowInstanceIfRequired` / `setWorkflowInstance` / `setPendingDocument` are written only by:
  - enforcement.ts:249-251, whose only caller is verification.ts `POST /api/documents`, wired once at index.ts:901;
  - verification.ts:541/554/651, the approve and reject routes, which mutate an **existing** instance and create none.
- **Gateway proxy catch-all** `router.use('/api/documents', …)` (proxy.ts:654) → originate. POST `/api/documents` is answered first by the verification router; Express is case-insensitive and non-strict, and normaliseRepeatedSlashes and the `/api/v1/` rewrite (index.ts:236/543) canonicalise the path first. If some spelling did reach the catch-all, originate guards it anyway.
- **originate `POST /`** (documents.ts:388): `isAllowedByRoleOrScope(DOCUMENT_WRITE_ROLES,'documents:write')`.
- **originate `POST /:id/version`** (:2330): the same guard.
- **`/api/certifications` and `/api/batch/certifications`** → originate certifications.ts:246, `isAllowedByRoleOrScope(DOCUMENT_WRITE_ROLES,'certifications:write')`. certificationRepo also inserts into `documents`.
- **`/api/documents/upload`** (proxy.ts:567) forwards to originate `/api/documents/upload`. originate has no such route.
- **mcp-server** creates through the gateway with its own `sk_` key, so it goes through this guard.
- **m365-integration** only verifies and lists; it creates nothing.
- **transfer's approvalWorkflowService** handles transfer approvals, not document create.
- **No unguarded door.** Bypass connectors skip the new guard but reach a guarded originate (F1).

### Q4: the ks1176 fixture edit
- ks1176 tests that a connector key's verification level `api_key` ranks as `none`. The edited fixture belongs to its control, "a standard human creating the same type passes, so the refusal above is the level".
- enforcement.ts reads no role, so the role is not the subject.
- **Instrument:** setting HUMAN_STANDARD's verificationLevel to BASIC makes that control fail (14/15). So it still discriminates on level.
- Putting role ISSUER back at head also fails it (14/15), which reproduces S's measurement.
- The head fixture passes on base product code too (Spark facts: 15/15).
- **Not weakened.**

### Q5: red/green and mutants
- **Red-first** (Spark's deterministic half): on base product code ks1871 is **13 of 26 red** and ks1176 is 15/15. At head: 26/26 and 15/15. This matches S.
- **Suite at head:** api-gateway, `--maxWorkers=2`: **131 files, 1347/1347**. This matches S.
- **tsc** `--noEmit -p api-gateway`: 0 errors. Positive control: an injected TS2322 is caught (rc 2).
- **My mutants:** 16, in `probes/mut1866/` (anchored replace, sha256 restored after each).
  - **My probe kills 16/16. S's test kills 12/16.**
  - Survivors of S's test: M3 trim the role, M5 split a string `scopes`, M6 case-fold scopes, M7 trim scopes (F2).
  - The other 12: guard removed, Unicode toUpperCase, String() coercion, exact scope only (no wildcards), guard after the writes, guard on gated types only, `return` dropped, message changed, OWNER added locally, scope arm dropped, role arm dropped, tr-locale upper.

## FINDINGS
- **F1 Note (n). The guard sits inside `if (!bypassWorkflow)`, so a connector whose config says `workflowPolicy:'bypass'` skips it.**
  - Measured: a `['register']` or `['register','documents:read']` key with bypass is forwarded to originate once (cells K…, bypass=true). It makes no workflow write.
  - Static read: the connector JWT carries the key's scopes verbatim (auth jwt.ts:294), and originate's `hasScope(['register'],'documents:write')` is false, so real originate answers 403.
  - So nothing is created and the ticket's claim ("before the approval workflow writes anything") holds. On that path, though, the refusal comes from originate, not from the gateway.
  - Spark called this a Major. It is not one, because no workflow is involved and the forward is guarded.
- **F2 Note (n). The tests do not pin the whitespace and case shapes.** S's 26 cells do not kill trim-role, trim-scope, case-folded scope, or string-`scopes`. The behaviour at head is correct (the probe refuses all four). Suggested cells: `' ISSUER_ADMIN'`, `['documents:write ']`, `['DOCUMENTS:WRITE']`, `scopes:'documents:write'`.
- **F3 Info (n). Stricter than originate on one more shape.** originate's `user.scopes ?? []` passes a **string** `scopes` to `hasScope`, and `String.includes` then matches a substring (`'xdocuments:writex'` would pass). The gateway refuses any non-array. No mint produces a string, so this is a pre-existing laxness in originate rbac.ts:61, worth a filing next to S's own "originate String(role).toUpperCase()" candidate.
- **F4 Info (n), pre-existing.** The role 403 comes after `enforceDocumentTypeRules`. A caller with no write role still learns the type configuration (unknown type, disabled, MFA, verification level) from enforcement's answers. Nothing is written.
- **F5 Info (n). S's disclosed fault checks out and did no harm.**
  - The commit message of e9f19a55 contains `KS-1891` once (subject "(PR 1859, KS-1891)"). 4f529d12 names only KS-1871.
  - Linear attachments read now: KS-1891 → #1859 only; KS-1848 → #1835 only; KS-1403 → #1373, #1865; KS-1871 → #1866 only; KS-1881 → #1861.
  - Nothing stray is attached. S's plan, an explicit squash subject and body at merge, keeps the key out of develop.
- **F6 Note (DOCS).** The two html files are hand-numbered entries (Flow Diagrams 129 and the Cheat Sheet). They convert to fragments at merge prep, as briefed. merge-tree is clean today.

**UNMEASURED:**
- a real originate behind the gateway (F1's 403, and the non-gated forward, are static reads);
- a running stack, real Redis, and real Postgres;
- the real `enforceDocumentTypeRules` inside my matrix (stubbed; ks1176 exercises the real one);
- JWKS key resolution (static key only);
- interactive tokens carrying a `sessionId` (the revocation lookup was not exercised);
- the approve forward (KS-1184 / KS-1087);
- the four platform suites, eslint, the pre-push hook, and the html docs content;
- the PR body itself (gh in the Blockchain config dir is not logged in, so S's READY mail and the KS-1871 comment stood in).

## HOW
- **Clone:** `git clone --no-checkout` (local) from gate 47's clone into the non-existent `repo/`. `rev-parse --show-toplevel` was asserted equal to it before any fetch. Remote set to Secuura/Distributed_Secuura, deploy key as `core.sshCommand`, push URL `no_push_qa_gate`. Fetched `refs/pull/1866/head` and develop, then a detached checkout of e9f19a55.
- **Setup:** `npm ci --ignore-scripts` in Blockchain/Dev (1795 packages), then a build of @secuura/shared. vitest via `npx --prefix <gw> vitest run --root <gw>`.
- **Probes:** copied into `src/__tests__` only for their runs, then moved to `probes/_quarantine/`. The base swap, mutants and the ks1176 instrument edits were restored, sha256 asserted. `git status` was clean afterwards.
- Linear was read only.
- No git write verb was run in /Volumes/DevMASTER/!CODING/**. Every process I started has exited.
- The clone was moved to the session scratchpad and removed there.

## Spark shadow (`spark_gate.sh` with `--node-modules`, work dir in the session scratchpad; `spark_review.py` with S's mail as the PR body; copies in `probes/spark/`)

| Item | Spark | Me |
|---|---|---|
| Red-first base / head | 13 of 26 red → 26/26; ks1176 15/15 both | same (from its facts) |
| Verdict | **none: SCHEMA FAILURE ×2** (both attempts aborted for repetition, invalid JSON) | GO WITH NOTES |
| Raw findings | bypass skips the guard (Major, ×4 repeats); "role arm unreachable for connectors" (Major) | bypass = F1 Note (measured: forwarded, no workflow write, originate guards); connectors carry role `connector`, so a role arm for them is correct, not a defect (false Major) |
| Role/scope matrix + base control | not run | 464 cells, base fails 362 |
| No-write boundary instrument | not run | 22 redis writers + query + originate + fetch, 0 on refusal |
| Other doors | not done | enumerated, none unguarded |
| Test gaps (F2) | missed | 4 surviving mutants |
| Fixture subject (Q4) | not examined | level-discriminating, confirmed |

Spark's deterministic half agrees exactly. Its review produced no usable verdict this time. The one real observation in its raw text (bypass) was over-graded, and it added one false Major.
