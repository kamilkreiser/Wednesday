--- comment 5857010658 by linear[bot] at 2026-09-27T15:03:48Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1121/security-credentialrepogetbyid-resolves-a-credential-by-substring-like">KS-1121 Security: credentialRepo.getById resolves a credential by SUBSTRING (LIKE '%id%' + includes()) — reached from GET /api/credentials/:id AND under POST /api/credentials/:id/revoke, and the partial match is pinned as intended by its own test (KS-1020's sibling)</a></summary>
<p>

## BLUF

The lookup shape PR #966 deleted from `getPresentation` (KS-1020 item 1) still exists, documented as intended, in `repositories/credentialRepo.ts:72-108` `getById`: an exact `SELECT credential FROM vc_credentials_store WHERE id = $1` (`:81-84`), then `… WHERE id LIKE $1 LIMIT 1` with `` [`%${id}%`] `` (`:88-91`), then `key.includes(id) || value.id.includes(id)` over the memory store (`:102-106`). Its JSDoc (`:72-74`) reads "Retrieve a credential by its full ID, **or by a partial-match substring**". Two callers: `GET /api/credentials/:id` (`routes/credentials.ts:264-278` → `:268` `credentialRepo.getById(id)`, no `requireRole`, no ownership check) — the same class as KS-1020: a fragment returns an arbitrary credential to any authenticated principal; and `POST /api/credentials/:id/revoke` (`routes/credentials.ts:284-289` → `credentialRepo.ts:235` inside `revoke()`, which rewrites `credentialStatus.revoked = true` at `:238-245`) — the same lookup under a **mutating** route: a fragment could revoke an arbitrary credential. `__tests__/credentialRepo.test.ts:59-64` pins the partial match as intended (`getById('abcdef')` → `urn:vc:abcdef-1234`), so a verbatim transfer of #966's deletion breaks that test: this is a design change, not a mechanical port. READ ONLY at `1f0d08841`; nothing run.

## Recommendation

1. **Decide** whether any caller legitimately needs substring resolution of a credential id (the pin at `credentialRepo.test.ts:59-64` says someone once did). If none: delete the LIKE branch and the `includes()` scan exactly as #966 did for presentations, flip the pin to assert 404/undefined for `'abcdef'`, and add the KS-1020-shaped cells (suffix, middle, prefix, metacharacters `%`/`_`, the bare uuid) for BOTH routes — the revoke route asserting no row is mutated on a fragment.
2. **Sequence with KS-1116** (which subject owns a presentation / credential): exact-or-404 closes the fragment disclosure; ownership is the remaining half on both routes.
3. Until then, treat `POST /api/credentials/:id/revoke` as the higher-risk half (a mutation on an arbitrary row), and prefer fixing it first if the two are split.

## Detail

* **Where (READ ONLY at** `1f0d08841`**):** `Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts:72-108` (`getById`), `:235` (inside `revoke()`), `:238-245` (the status rewrite); `src/routes/credentials.ts:264-278` (`GET /:id`), `:284-289` (`POST /:id/revoke`); `src/__tests__/credentialRepo.test.ts:59-64` (the pin).
* **Class sweep at head** (`git grep -n -E 'LIKE |\.includes\(' -- Blockchain/Dev/services/vc-issuer/src/`, non-test): the two sites above, `credentialRepo.ts:199` (a `type` filter, not a lookup) and the two why-comment lines `presentations.ts:111-112` — nothing else.
* **First recorded:** PR #966 comment 5650197614 (2026-09-13, the builder's sibling note — which did not say that `:235` sits under the revoke route); the gate's §4 added the revoke half.
* **Source:** `Testing Agent MAIN/projects/secuura/reports/2026-09-13-ks1020-966-1f0d08841-tier1-r1/report.md`, §4 "The sibling (item 5) — READ ONLY".
* **Related:** KS-1020 (the presentations half, fixed by #966); KS-1116 (ownership model); KS-625 (`/presentations/verify`, same service).
* **Dedupe, before filing (s200, 2026-09-13):** literal census over 1,106 KS issues (685 archived) and 899 comments — `credentialRepo.getById` → KS-1020 (the builder's comment) and KS-1116 (a pointer in its description); `credentialRepo.ts` → 0 titles/descriptions; `routes/credentials.ts` → KS-1020, KS-1116, KS-588, KS-624, KS-625 and two archived — none about the substring lookup or the revoke route. Controls: `LIKE` → KS-1020; a nonsense token → 0.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1121-resolve-a-credential-by-exact-id-only-drop-the-substring-9f9f6ae8c35e">Review in Linear</a></p>

