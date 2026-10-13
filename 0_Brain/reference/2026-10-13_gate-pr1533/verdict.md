# Gate verdict: Secuura PR #1533 (KS-1553 (a), key list compares a normalised organisation id), Sonnet tier 2
Report sha256/16: 4fc478e33f32e0b3
Recipe: sha256 of this file with the single line beginning "Report sha256/16:" deleted, first 16 hex chars.

**VERDICT: GO WITH NOTE** (0 Major, 3 Minor). Not a deploy recommendation.

Head under test f4828b1d9ab7f81f7753419a1357c3abecd7a53e (ls-remote of refs/pull/1533/head, asserted after fetch); develop 3a87133760595b625617617daa587f8af1b821a7 (asserted). Instruments: own `git clone --shared` of 2_Project_Files into the scratchpad (push URL DISABLED), `npm ci`, shared package built with tsc, throwaway PostgreSQL 15.14 on 127.0.0.1:55411, docker/init/* in order, scripts/run-migrations.sh (applied=50 failed=0, evidence/migrations.log), service as `secuura_app` (rolsuper f, rolbypassrls f; svc_api_keys relrowsecurity t, relforcerowsecurity t; the file's own RIG CONTROL cell re-asserts it). Postgres stopped, port 55411 no longer listening. Project folder untouched (no git write verb there). Raw outputs in evidence/.

## 1. The 17 cells (FOUND / TESTED / HOW)
- Head: 17/17, 3 runs (evidence/head_run1-3.txt). Develop: index.ts swapped for develop's blob, same test file, same DB: 6 failed / 11 passed, 3 runs, identical (evidence/dev_run1-3.txt). The 6 red on develop: own UPPER; own PADDED; platform UPPER; legacy upper-case row; ISSUER_ADMIN own org any case form; MEASURED GAP "case variant of another org". The author's "6 of 17" is confirmed. Control that the harness can fail: the develop run itself, plus 12 mutants below that go red.
- Suites at head: services/security unit 31 files / 336 tests passed; integration 3 files / 43 passed (evidence/unit_head.txt, integration_head_all.txt). eslint on index.ts + the new file: rc 0 (planted `var` control fires: 1 error). `tsc -p tsconfig.json` rc 0 but that config EXCLUDES src/__tests__, so I typechecked with an include-all config: 0 errors in the new file; 2 pre-existing errors in ks952-*.test.ts (not this PR); a planted type error in a copy of the new file is caught (control).
- Scope: `git diff --stat develop..head` = 2 files (+285/-1): index.ts +9/-1 (mostly comment) and the new test. Head vs 75f8ce59: 6 files, ALL under services/originate (the KS-1557 merge); 0 files in services/security. Author's scope claim confirmed.

## 2. Normalisation: what it does, collisions, "lists more" (item 2, the thorough one)
`normaliseOrgId` (packages/shared/src/security/orgId.ts:42) = `typeof v==='string' && v.trim()!=='' ? v.trim().toLowerCase() : null`. JS `trim` strips ASCII and Unicode whitespace (NBSP, U+FEFF BOM, tab/LF); `toLowerCase` is locale-free but not ASCII-only: U+212A KELVIN SIGN lowercases to ASCII "k"; U+0130 lowercases to "i"+U+0307 (so "İstanbul" does NOT collide with "istanbul"; measured).
I built a caller x query matrix (7 callers: super_admin, SYSTEM_ADMIN, ADMIN no-org, ORG_ADMIN, ISSUER_ADMIN same tenant, ISSUER_ADMIN other tenant, tenant-less ISSUER_ADMIN; 31 query forms; 14 seeded keys including legacy upper/padded/whitespace-only/empty/NBSP-padded stored ids and case-colliding pairs in two tenants), run on develop and on head (evidence/matrix_develop.json vs matrix_head.json, matrix2_* for the blank-stored rows; script evidence/gatematrix.integration.test.ts.txt).
- Cross-tenant: NO new read. tenant-B ISSUER_ADMIN sees only tenant-B keys under every form (e.g. `coll_upper` -> only coll-C-otherTenant); tenant-less non-platform caller 403 on every query form (29 cells, same as develop). Control: the same cells are 200 with keys for platform.
- Lists MORE (measured, all within the caller's own tenant or platform scope): (a) the padded/UPPER/tab/BOM/NBSP forms of an id now list the same keys as the canonical id (the intended fix); (b) legacy keys stored upper-case/padded now list under the canonical id AND still under their raw stored form (legacy_upper_exact and legacy_pad_exact identical to develop); (c) COLLISION: two keys in one tenant whose stored ids differ only by case (`COLL-ORG`, `coll-org`) now both list under either query (develop: each only under its exact form); (d) U+212A "Kelvin" query now lists the ASCII `kelvin-org` key; (e) an NBSP-padded stored id folds into the canonical one. None crosses a tenant. Because the list has no organisation bound (KS-1574), an org-bounded admin could already list any org in its tenant by exact id, so (c)-(e) reveal nothing a known id did not; they matter only when (c) represents two genuinely different legacy organisations. This is the same equivalence class as the revoke arm (keyRevokePolicy.ts:174-175) and the mint (index.ts:1242), so it is consistent. Recorded as Minor m3.
- Lists FEWER (the opposite direction, a regression of a kind): a legacy key whose stored organization_id is whitespace-only (`'   '`, `' '`) was listable on develop by the exact whitespace query (`?organizationId=%20%20%20` -> 200 + that key); at head NO query reaches it (both sides normalise to null and the guard refuses). The key becomes invisible in the list for every caller class (platform, tenant admins). It is still revocable by id. Minor m1.
- Org-less (NULL organization_id) keys: never listed by any of the 31 forms for any caller at head (and none on develop). Control: the same key is created, present in the DB, and listable by nothing else.

## 3. Null guard (item 3)
Head vs develop identical on: empty (`organizationId=` -> 400), whitespace (spaces, NBSP) -> 200 + 0 keys, repeated parameter (`a&b`, and `&own-org` after an empty one) -> 200 + 0, `organizationId[a]=..` and `organizationId[]=..` -> 200 + 0, `own%00org` and `%00` -> 200 + 0 (a NUL does not 400 on this route; unchanged, not this PR), 8,000-char value -> 200 + 0, 100,000-char value -> 431 from Node's header limit, `null`/`undefined` strings -> 200 + 0 (they are just strings), prefix `own` -> 0 (does not match `own-org`). Org-less keys never appear. Guard-dropping mutants die on the PIN cell (below). The `typeof organizationId === 'string'` ternary is redundant at runtime (normaliseOrgId already returns null for non-strings) but is needed for tsc; an equivalent mutant, harmless.

## 4. Mutants (killed by cell name; original 17/17 re-confirmed between runs)
Author's seven, re-derived by me (my own wording of each):
- M1 no normalisation either side: KILLED by 6 cells: own UPPER, own PADDED, platform UPPER, legacy upper row, ISSUER_ADMIN own any case, MEASURED GAP case variant.
- M2 raw query vs normalised nothing: KILLED, same 6.
- M3 (my variant: guard dropped, norm == norm): KILLED by PIN (query normalises to nothing). Note the author's "normalise after the compare" is the same shape as M5; not separately built.
- M4a trim only: KILLED by 5 (UPPER, platform UPPER, legacy, ISSUER own any case, GAP case variant).
- M4b lower only: KILLED by 2 (PADDED, ISSUER own any case).
- M5 stored side raw: KILLED by 1 (legacy upper-case row).
- M6 null guard removed: KILLED by 1 (PIN).
Mine:
- X1 normalise only for org-bounded callers, raw for platform: KILLED by 2 (platform UPPER, legacy row).
- X2 platform compares raw stored: KILLED by 1 (legacy row).
- X3 tenant filter dropped: KILLED by 1 (CONTROL: ISSUER_ADMIN of another tenant).
- X4 guard only for non-string (whitespace string not refused): KILLED by 1 (PIN).
- X7 array query uses its first element: KILLED by 1 (PIN).
- X6 an organisation bound added for org-bounded callers: both MEASURED GAP (exact id, case variant) go red (the cells would turn red if someone adds a bound, as claimed).
- X5 prefix match (`startsWith`) instead of equality: SURVIVED, 17/17 green. No cell asserts that a near-miss/other id is NOT listed apart from `default-org` vs ORG_OTHER on the platform arm, which is not a prefix. Minor m2.
Comment-only control: the author's claim not independently needed; `orig` re-applied between mutants was 17/17 each time.

## 5. Do the cells pin what they claim? (item 5)
MEASURED GAP cells pass for the right reason (they assert the foreign org's key id IS in the list, and go red under X6). They are honest about KS-1574 in the title and header. The PR does not widen the gap beyond case/pad folding (section 2). No existing test in services/security asserted the old raw behaviour: whole unit (336) and integration (43) green at head with no test edited (diff touches only the new file). One unit-cell nit: the legacy "stored in legacy form" assertion reads the DB back, good.

## Findings
- **m1 (Minor)** services/security/src/index.ts:1349-1358. The comment says a query that normalises to null "matches nothing, as it did before". True for the query side, false for a legacy key whose STORED id is blank: develop listed it under the exact blank query, head cannot list it under anything. Repro: seed organization_id `'   '` (service as secuura_app), `GET /api/keys?organizationId=%20%20%20` as super_admin: develop 200 + key, head 200 + []. Fix: either accept (document that blank-stored keys are unlistable and revoke-by-id only) and correct the comment, or add a one-line test; no code change needed unless such rows exist in the live DB (not tested: I did not look at any real data).
- **m2 (Minor)** the integration file lacks a negative "different id is not listed" cell for a near-miss on the org-bounded arm; X5 (prefix match) survives 17/17. Fix: add one cell: `?organizationId=<first 8 chars of ORG_OWN>` and `<ORG_OWN>x` must not list the own key.
- **m3 (Minor)** case-/whitespace-distinct legacy ids now fold (COLL-ORG vs coll-org, NBSP-padded, U+212A) so one query lists several legacy orgs' keys within the same tenant. No cross-tenant, nothing beyond what KS-1574 already gives, same equivalence as revoke/mint. Fix: none required; note it on KS-1574 so a future bound is built on normaliseOrgId equality (as X6 shows the cells would catch a bound) and add a cell if distinct-orgs-by-case ever matters.

## NOT tested
Live/production data (existence of blank-stored or case-colliding legacy rows); the gateway proxy (/api/security/keys) and the Admin Dashboard front end beyond the file's own shape cells (green on both trees); the PR body on GitHub (not fetched; claims checked against code instead); non-HTTP callers of memApiKeys; performance (normalising per key per request is O(n) as before).
