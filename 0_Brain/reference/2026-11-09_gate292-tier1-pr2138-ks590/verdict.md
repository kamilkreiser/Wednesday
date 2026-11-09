PR 2138: GO WITH NOTES

# Gate 292, tier 1 (Opus): PR 2138, Refs KS-590, Seat G 32nd. Findings only.

| PR | head | verdict |
|---|---|---|
| 2138 | d769c05d0a9b4e47413ed7ec9d02024b3180edc0 | GO WITH NOTES |

## BLUF
All four gaps and the v2 chain-only twin are closed at the head, on every verify response builder in originate v1 and v2. Each gap was red on develop and green at the head in my own runs. Same-tenant callers lose nothing on any DB-row answer. The KS 1114 T9 integration golden was measured on a local PostgreSQL 15 with no docker and no box: it passes at develop and at the head, and my planted control makes it fail. All 10 of the seat's mutants reproduce exactly. Of my own per-gap mutants, gaps 2 (on /verify), 3 and 4 are killed. The gap 1 mutant SURVIVES, and so does a verify-file probe: those are test gaps, not code defects (G292-2, G292-3). The PR, the code comment and the ticket comment give the wrong reason for gap 3's safety, though the conclusion holds for a stronger reason (G292-1). Nothing here needs Kam before merge. G292-4 is for his awareness.

## Pins (re-read at start and end)
- Start, 20:09:48 AEDT: develop 1b3a3ec34a5b, PR head d769c05d0a9b. Both match the commission.
- End, 20:55:30 AEDT: PR head d769c05d0a9b (unchanged). Develop MOVED to d0b4825cc244: one commit, KS-2133, one file, `services/api-gateway/src/__tests__/ks1505-spec-reload-warns-when-it-re-read-the-same-bytes.test.ts`. It shares 0 of the PR's 9 paths (control: the PR's paths matched against themselves = 9). The merge onto d0b4825c is clean: tree ae533525, 9 files, +538/-21.
- The pinned move f98afb11 -> 1b3a3ec3 is PR 2115: one file, `ks1534-an-allow-list-of-non-strings-is-refused-by-both-reads.test.ts` (+3). It shares no path with the PR.
- df DevMASTER: 98 GiB available at start, 100 GiB at end.

## FOUND / TESTED / HOW

**Instrument.** A blobless clone with a sparse checkout at /private/tmp/g292. `repo` holds the head. `dev` is a worktree of my own clone at develop 1b3a3ec3.
- Node v26.8.1 (not an LTS line); jest 29.7.0.
- node_modules are symlinked read-only from the seat's s-g32-ks590 tree. For the DB runs, `dev` instead uses a private copy of @prisma and prisma with a client I generated myself. The seat's tree stayed untouched: no .prisma or .generate appeared there (count 0, against a control count of 1 in my copy).

### Q1. Each gap closed, on every route
The response builders in v1 `verification.ts` at the head, and how each is scoped:

| # | Builder (head line) | Scope |
|---|---|---|
| 1 | verify-file chain-first (:988) | `scopeTenantFields(..., true)` (new) |
| 2 | verify-file not-found (:1030) | names nothing |
| 3 | verify-file main (:1061) | `isCrossTenantResponse(req, doc)` |
| 4 | /verify by-id `respondExistenceOnly` (:1352) | scoped by row (gap 4 now selects `d.tenant_id`, :1680/:1690) |
| 5 | /verify chain-first downgrade (:1510) | `isCrossTenantResponse(req, localDoc)` (new); both narrow reads select `tenant_id` (:566-567, :1481-1482) |
| 6 | /verify chain-first verified (:1556) | `scopeTenantFields(..., true)` (new) |
| 7 | /verify hash main (:1617-1663) | scoped; the lineage path spreads the scoped `base`, and a scoped answer returns before lineage |
| 8 | not-found / title existence / errors / `/status` / `/hash` | name nothing |

v2 `verificationV2.ts`:
- `buildMatch` (:194): scoped by `isCrossTenantResponse`. The local, cross-tenant and by-id reads all select `tenant_id` (:84, :297, :466, :476).
- `chainOnlyMatch` (:253): scoped for every caller, plus `fieldsWithheld: true`.

Other checks:
- `crossTenantLookup` and the KS-1986 foreign originals set `_tenantId`.
- `scopeTenantFields` and `isCrossTenantResponse` have no other caller in originate's src. Grep found 12 in verification.ts and 5 in verificationV2.ts. Other services are outside my sparse checkout (NOT TESTED).
- `publicDocumentsRouter /:id/sig-json` reads only the caller's own tenant (`getDocument(id, tenantId)`). The certifications routes are under `authenticate()`.

Evidence, red on develop and green at the head:
- I copied the four head test files onto develop: 19 of 51 fail. That is the 16 declared new cells plus the 3 changed cells, and the 7 controls stay green. At the head, 51 of 51 pass.
- My own probe file (`g292-probe.test.ts`, 7 cells, in `dev`, not part of the PR). Each zero has a control beside it:
  - P1-ctl, a v2 cross-tenant org id: red on develop, green at the head.
  - P2-ctl, a v2 anonymous by-id org id: red on develop, green at the head.
  - P5, the /verify chain-first answer for an authenticated caller: red on develop, green at the head.
  - P1, P2 and P3, the own-tenant controls: green on both.

### Q2. Over-withholding (looked at first)
- **DB-row answers, same tenant: no field is lost** on any route. Evidence:
  - the seat's controls C-1, C-2, C-5, G4-C/D and G2-E/F, green at the head;
  - my P1 (v2 by hash), P2 (v2 by id) and P3 (row tenant in upper case), green at the head;
  - P4 shows a cross-tenant answer keeps `verified`, `checks`, `blockchain` (txHash), `documentId`, `contentHash` and the certification's id, type and time identical to the own-tenant answer.
- **Chain-first and v2 chain-only answers: every caller loses** `issuer`, `certification.certifiedBy`, `certification.certifierOrganizationId` and `onChainMetadata`, authenticated callers included (P5). On the facts:
  - `verified`, `checks.isCertified`, `checks.integrityVerified`, `blockchain.txHash` and `certificationId` are unchanged (P5).
  - The only additions are `fieldsWithheld: true` on v2 chain-only matches, and null `title` on scoped by-id and downgrade answers.
  - See G292-4.
- I traced whether the chain-first branch ever runs while the caller's tenant holds rows. `judgeAcrossTenants`' `originals.length === 0` exit (:704) is the only path to `rows=[]` with no read failure. By my reading of `certificationEligibility`, it is unreachable when local rows exist: the earliest local row is always eligible. Not exercised.

### Q3. What gap 3 assumes, and whether it is true
- The change assumes that a documents row read with `tenant_id` selected always carries a non-null value. The PR, the code comment (:458-461), the flow fragment and the ticket comment attribute this to migration 039's fail-closed RLS.
- **Measured** on a local PostgreSQL 15.19, built from develop's docker/init and then `run-migrations.sh` (applied 60, failed 0):
  - `documents.tenant_id attnotnull = true`;
  - an INSERT with `tenant_id NULL` is refused with a not-null violation, and the control INSERT with the default tenant succeeds.
- The guarantee is migration **011** (`ALTER COLUMN tenant_id SET NOT NULL`, :139; its DROP sits only in the commented Down block). It holds for every role, BYPASSRLS included. 039 only filters rows, and only for roles without BYPASSRLS: `secuura` here is `super=true`, `bypassrls=true`.
- **The code does not trust RLS. It fails closed:** any row without a tenant is scoped (M3 and X3 are killed).
- See G292-1.

### Q4. Gap 4
- Both local strategy-2 reads now select `d.tenant_id` (:1680, :1690), and `respondExistenceOnly` scopes by it (:1323).
- Cells: G4-A and G4-B (red on develop, green at the head) and G4-C and G4-D (own tenant named).
- My mutant X4 drops the column from the uuid read only. It reddens exactly G4-D.
- The DB golden sees it too: head minus gap 4 turns T9 red, because the by-id body's `title` becomes null for the default-tenant anonymous caller.

### Q5. Red-first and mutants
- Red-first reproduced: 16 of 23 on develop, exactly the declared cells, and 23 of 23 at the head.
- The seat's 10 mutants, re-implemented from predictions.md §5 and §9 and run against the WHOLE originate suite, reproduce exactly. Every red set equals the seat's summary.txt, including the out-of-file reds: M1 reddens ks563, and M3 reddens ks584, ks563 and ks1939 C2.
- My own mutants, run against the whole suite:

| Mutant | What it does | Red |
|---|---|---|
| X1 (gap 1) | org id nulled only when `certifiedBy` is set | **0 of 2615, SURVIVES** (G292-2) |
| X2 (gap 2) | /verify chain-first scoped only for anonymous callers | 1 (G2-C) |
| X2b (probe) | the same on verify-file | **0, SURVIVES** (G292-3) |
| X2c (probe) | onChainMetadata keeps its identity block, only issuerName and issuerOrgId stripped | 4 (G2-A, G2-B, G2-C, G2-V via the ORG_DID canary) |
| X3 (gap 3) | untenanted row scoped only for anonymous callers | 1 (G3-D) |
| X4 (gap 4) | uuid by-id read only | 1 (G4-D) |
| X5 (v2) | no `fieldsWithheld` marker | 1 (G2-V) |
| X6 (v2) | onChainMetadata kept | 1 (G2-V) |

- **Pins:** G2-E, G2-F, G4-C, G4-D, C-1, C-2 and C-5 are green on develop by design. Each is labelled CONTROL in its title, and M2e, M2f and M4 show each can go red. Honest.

### Q6. The three changed cells (each diff hunk read)
- ks584: relabelled; `title` 'Grad cert' becomes null; added `issuer` null, `verified` true and `isAnchored` true. Only the withdrawn assertion is inverted.
- ks563: `certifiedBy` and `certifierOrganizationId` become null. `isCertified` TRUE and the id, type and time are kept. Label kept.
- ks1939 C2: `title` becomes null. `verified:false`, `documentId`, `status`, `contentHash` and the checks objectContaining are unchanged. Label kept.
- All three are as Wednesday ruled.

### Q7. Whole suite, tsc and eslint
- Whole originate suite: develop 2,592 of 2,592 in 220 suites; head 2,615 of 2,615 in 221 suites. Compared cell by cell: 2,591 common, 0 changed result. The only rename is the ks584 cell, plus 23 new ks590 cells.
- tsc over src with tests (temporary config): 4 errors at both develop and the head, an identical list (ks1937 and ks488 duplicate globals). Over src alone: 0 and 0.
- eslint src: 0 errors and 29 warnings at both develop (311 files) and the head (312 files). verification.ts, verificationV2.ts and the four test files carry 0 warnings at both.

### Q8. DB-gated golden (KS 1114 T9)
- R 84th's recipe (`2026-11-04_seatR-84th/tools/pg_up_r84.sh`) needs docker. I re-expressed it for a LOCAL Homebrew postgres 15:
  - initdb under /private/tmp/g292/pg, loopback port 55392, trust auth, fixture passwords only;
  - docker/init in entrypoint order, then the platform schema, then `scripts/run-migrations.sh` (60 applied, 0 failed);
  - server TimeZone UTC, which T9's precondition requires.
- Results:
  - **develop: 17 of 17**, T9 green;
  - **head** (the head's two route files over develop, which equals the merge tree's code): **17 of 17**, T9 green;
  - planted control (head minus gap 4): T9 RED, only on the by-id body's `title`.
  - ks1119 integration: 18 of 18 at the head and passing at develop.
- ks1557 and ks1662 fail at SETUP on my layout at develop ("relation tenants does not exist"; they need R 84th's SINGLE-DB layout), so they are uninformative. I did not set that layout up: UNMEASURED.

### Q9. docs/VERIFICATION.md
- The example now shows `issuer: null` and `onChainMetadata: null`.
- The new paragraph says that `issuer`, `certifiedBy`, `certifierOrganizationId` and `onChainMetadata` are withheld for every caller on a chain-only hit, and that the tx, the anchor facts and the certification id stay. Both match the code (:988, :1556, :253).
- It is the only product doc change; the other two are the KS-590 fragment pair.
- Stale text the seat already names as a follow-up: the Lookup algorithm still says chain-FIRST, and "sparse onChainMetadata" in Known gaps.

### Q10. Merge tree and census
- Merge onto 1b3a3ec3 is clean: tree 408d6336, the same 9 files, +538/-21. The end merge onto d0b4825c is also clean (above).
- Census: my own git-based reading, not the GitHub API (see NOT TESTED). The set was the seat's 59 open PRs at 08:19Z plus PRs 2136 and 2137, which ls-remote shows as newer, 61 in all. Each PR's files = `git diff --name-only $(merge-base develop, head) head`.
  - **0 PRs touch any of the 9 paths.**
  - Controls: `routes/adminConfig.ts` -> PR 2087. The originate `__tests__/` prefix -> PRs 2052, 2087, 2093, 2094, 2099, 2100 and 2101. A planted line on the PR's own path is matched (2 of 2).
  - **PR 2131** touches `docs/openapi/secuura-api.yaml`, vc-issuer `routes/presentations.ts`, `vc-issuer.openapi.ts`, one vc-issuer test and the KS-625 fragments. It shares nothing with PR 2138.
  - No open PR touches `originate/src/routes/` except 2087 (adminConfig.ts).
  - No head moved against the seat's census SHAs.

### Q11. The PR body and the ticket comment
Read from the seat's record (drafts/pr_body.md, body_sha1 19cf5292...; drafts/comment_ks590_final.md and comment_real.out read-back), not from the GitHub or Linear APIs.
- The behaviour change is stated first and plainly: titles, issuers, org ids and onChainMetadata disappear for anonymous and cross-tenant callers; facts are unchanged; demo is affected on chain-only hits; kintsugi and demo untenanted rows are UNMEASURED.
- Every count I re-measured matches: 16/23, 23/23, 2,592 -> 2,615, 4 = 4, 29 = 29, 10 of 10 mutants, 0 overlap.
- Over-claim: the 039 sentences (G292-1). The ticket comment's "Under migration 039's row-level security such rows are invisible to the app's reads" is stated as fact. The PR body itself lists "whether demo or kintsugi connect as a role it binds" as not measured.

## Findings

**G292-1 (LOW, accuracy of client-facing text and of a code comment).** Gap 3's safety is attributed to migration 039's RLS. The real guarantee is migration 011's `documents.tenant_id NOT NULL`, which I measured on PG15 at develop's schema: attnotnull true, a NULL insert refused, the control insert accepted. RLS binds only non-BYPASSRLS roles, and that is UNMEASURED for demo and kintsugi.
- Where: `verification.ts:458-461` (comment), the PR body's Gap 3 and NOT-run lines, ticket comment 845cb0df ("invisible to the app's reads"), and the flow fragment.
- The conclusion (no production row reaches the check without a tenant) holds more strongly than claimed. On any DB that ran 011, untenanted rows cannot exist, so the "kintsugi/demo untenanted rows" risk is moot there.
- Fix: wording only, follow-up; no code change.

**G292-2 (LOW, test quality, gap 1).** My mutant X1 nulls `certifierOrganizationId` only when `certifiedBy` is set, and it survives the whole suite (0 of 2,615).
- Every fixture, the chain one included, carries `issuerName`. Yet post-KS-238 on-chain metadata carries `issuerOrgId` WITHOUT `issuerName` (`docs/VERIFICATION.md:30`). That is the realistic chain-first shape, and no cell has it.
- The code is right (it nulls unconditionally), but nothing pins it on that shape.
- Follow-up: one cell with chain metadata `{issuerOrgId, certId}` and no name.

**G292-3 (LOW, test quality, coverage).** Two scrubs are correct at the head but pinned by no cell:
- (a) verify-file's chain-first answer for a caller WITH a tenant. X2b, scoped only for anonymous callers, survives at 0 red. G2-C covers /verify only.
- (b) v2 `buildMatch`'s cross-tenant org id. M1 reddens no v2 buildMatch cell; my probe P1-ctl is red on develop and green at the head.
- Follow-up cells.

**G292-4 (NOTE, scope, for Kam's awareness; not a blocker).** Chain-first answers (v1 /verify, v1 verify-file) and v2 chain-only matches withhold issuer, certifiedBy, org id and onChainMetadata for EVERY caller, authenticated callers included (probe P5).
- Kam's card text is "withhold ... from an anonymous verify". Withholding from authenticated callers too is the seat's design (D2b), and Wednesday CONFIRMED it in the plan answer. It is a ruling inside Kam's card, wider than its literal words.
- No DB-row field is lost by a same-tenant caller.
- A chain hit carries no tenant to compare, so the alternative design is not obvious. Recorded so the scope is visible.

**G292-5 (INFO, docs).** The openapi `fieldsWithheld` description (`originate.openapi.ts:674-677`) says "because the registration belongs to a different tenant". It is now also set on chain-only matches (no registration), and it lists only title, issuer and certifiedBy. The seat already names this as a follow-up; I add the "different tenant" wording.

## NOT TESTED
- The GitHub PR body and files API, and the Linear comment as stored. The commission bars real credential files, so I did not source the project `.env` (`GH_TOKEN`, Linear key). The body and comment were read from the seat's record. The census set was the seat's 08:19Z open list plus the two newer pull refs, so a PR CLOSED since then would only over-include. Open/closed state was not re-read.
- ks1557 and ks1662 integration (they need the single-DB layout); the platform suites (Schemathesis, Akto, Playwright, k6); a live chain-first answer with a real anchor_store tx; Node 24.
- Which DB role demo and kintsugi use (moot for gap 3 by G292-1), and whether any non-migrated DB lacks 011.
- Services outside originate (my sparse checkout held originate, docs, migrations, prisma, packages, shared, scripts and docker/init).
- Reachability of `judgeAcrossTenants`' empty-originals exit, which was read only.

## Conduct
- No cd. No git write verb in any !CODING checkout (the hook refused two attempts that pointed at my own clone through a shell variable, and I reran them with literal paths). Nothing posted or mailed. No docker, no box, no rm. No real .env or credential file read (fixture passwords only).
- Clone /private/tmp/g292: 478 MB at the end, left in place (no rm). The local postgres was stopped (`pg_ctl stop`, rc 0); its data dir stays inside /private/tmp/g292/pg.
- load1 rose above 8 from other seats' work (peaks of 10-15 at 20:23 and 20:41, while my jest jobs also ran). I stopped my 3-worker mutant run at 20:23 and reran at 1 worker behind a load1 < 7 gate.
- A TaskStop during the first mutant run left verification.ts mutated in my clone. I caught it (git status), restored it with git checkout in my clone, and checked the tree was clean before any further run. Every mutant result above comes from runs after that restore.
