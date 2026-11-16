PR 2249: GO WITH NOTES (at head 10057c4f63c3641eab82ec5688c1d41ef77c325d; tier 1)
Head unmoved (gh api 23:30:19Z and again 23:56:47Z). Develop MOVED during the gate: cf2b2a1a5d5f -> 553c0f8ab334 (KS-1783, 3 ks1634 test files only); both develops gated below. MERGE SHOULD WAIT ON KAM'S ANSWER TO ITEM K1 (personal data now public).

# Gate 374, tier 1, QA findings only (nothing fixed, posted, mailed, pushed or written to Linear/GitHub)

Own clone: scratch/repo (local clone + PR/develop refs fetched from GitHub), worktrees scratch/h (PR head) and scratch/d (develop cf2b2a1), npm ci at Blockchain/Dev and services/originate, shared built. Every run below gated on load1 <= 8 (logged in the run outputs). One process slip, disclosed: at 10:32 one jest invocation was launched at load1 11.47; it died on config resolution before any test ran (scratch/five_head.json.out). Every later run went through the load-gated runner scratch/run_jest.py.

## K1 — FOR KAM: personal data now reaching anonymous and cross-tenant callers

What the four fields hold at the data layer (documents table: title VARCHAR(500), metadata JSONB, certification_metadata JSONB, owner_user_id UUID, issuer_organization_id UUID; docker/init/01-schema.sql):
- title = documents.title, the registrant's free text.
- issuer = first non-empty of certification_metadata.issuerName, certificationData.issuedBy, metadata.issuedBy, metadata.certifiedBy, metadata.issuerName, doc.issuer_name, organizations.name.
- certification.certifiedBy = certification_metadata.issuerName, else certificationData.issuedBy, else organizations.name.
- certification.certifierOrganizationId = certification_metadata.issuerId.

The write side (certifications.ts, legacy certify path ~line 840) stores `issuerName: data.issuedBy || issuer.name` and `issuerId: issuer.id`. `issuer` comes from getUserFromRequest (line 81): `id = req.user.userId`, `name = the local part of the user's email` (`userEmail.split('@')[0]`). So:
- **certifiedBy (and issuer) is the certifying person's email local part (for example "jane.citizen") whenever the certifier did not send issuedBy.** It is a person's name, or a caller-chosen display string. It is NEW to anonymous and other-company callers on all four paths (null on develop). Kam's 09:17 words open "certifiedBy"; whether a person's email-derived name is one of "the names" is his call.
- **certifierOrganizationId is NOT an organisation id. It is the certifying USER's id** (req.user.userId, or a connector principal string). The repo says so too: verification.ts comment ~line 318 ("the certification row stores the issuer's USER id, not an organisation id") and gdprService.ts ~line 830 ("issuerId, a uuid pointing at the anonymised user row"). When the owner certifies their own document, which is the normal flow, this is the OWNER's user id.
  - It already reached anonymous and cross-tenant callers on develop on all four paths, because scopeTenantFields never nulled it. That exposure predates this PR.
  - THIS PR adds it on the KS-1986 D-B3 foreign-original path, where develop nulled it.

Measured with my own cells and realistic write-side data (issuerId = owner_user_id = a user UUID, issuerName = "jane.citizen", issuer_organization_id set, an email in metadata):
- **Four paths** (scratch/mine/parked/g374b-four-paths-realistic.test.ts):
  - Head, anonymous and other-company callers: owner/user id PRESENT on 4/4 paths. Email local part PRESENT on 4/4.
  - Develop: owner/user id PRESENT on 4/4 (pre-existing). Email local part ABSENT on 4/4.
  - Column `issuer_organization_id` absent and the full email absent everywhere, at head and on develop.
  - Positive control: the same check fires on planted values (G3-control green).
- **D-B3 path** (g374a-dB3-realistic.test.ts, cell G1, /verify and verify-file): green on develop. RED at head: `coid` is the owner's user UUID and `cby` is "jane.citizen".
- The answers carry no caller id, caller email, IP or user agent at head (N-C5 holds; my dump shows no such keys).

The PR body, the fragments and the READY say "the owner id and the issuer_organization_id column stay asserted absent". That is true of the columns only, not of the owner's id VALUE. The new test fixtures (ks590n ORG_UUID, ks1986 FOREIGN ORIGINAL CERTIFIED CANARY_ORG_UUID) model issuerId as an organisation UUID, which is not what production writes.

## Findings

| # | Sev | Finding |
|---|---|---|
| K1 | Major, Kam's | As above. Net new from this PR: the email-derived certifier name on four paths, and the certifier/owner user id on the D-B3 path. The user id on the other three paths is pre-existing. Not a code defect against the ruling's words: it is the ruling's premise ("the organisation id") failing at the data layer. Recommend merge waits for Kam's yes. |
| F1 | Minor | Owner-id absence is pinned only on v1 /verify and verify-file foreign-original (ks1986 LEAK CANARY). My mutants gB (v2 buildMatch adds owner_user_id) and gC (by-id adds owner_user_id for cross-tenant callers) both SURVIVE all 119 cells. Cause: the ks590n fixture has no owner_user_id or issuer_organization_id. gA, gD and gE are killed by LEAK CANARY. gF (anonymous-only email+owner on by-id) is killed by N-C1, so my prediction was wrong. Predictions: scratch/mutant_predictions.txt; results: scratch/chain.out. Every restore had equal sha256. |
| F2 | Minor | PR body does not name tier 1 (`grep -i tier` = 0; control "Kam" = 3). The READY and both fragments do. |
| F3 | Minor (doc) | Stale contract, left untouched as D4 ruled. originate.openapi.ts lines 674-677 (fieldsWithheld field) and 2092-2093 (v2 route prose "KS-584 tenant scoping with an explicit fieldsWithheld marker"); yaml lines 6873 and 30222 match. A client reading it would believe cross-tenant names are withheld and would code for a marker that never arrives. Harmless at runtime: the field is optional and absent means "not withheld", which is now true. Also pre-existing: the contract describes certifierOrganizationId as "Organisation id of the certifying issuer" (line 446), which is wrong per K1. That is the more misleading line. Candidate filing. |
| F4 | Note | PR-body and fragment wording "the certifier's organisation id" and "owner id ... stay asserted absent" (see K1). |
| F5 | Note | Pre-existing: ks1937 and ks488 share a global `EmailModule` type. They are the 4 tsc test errors, and one whole-suite develop run failed to load ks488 (TS2300). ks488 alone: 8/8. Not this PR. |

## The six questions

1. **Names open, nothing else.** All four paths, anonymous and other-company: title, issuer, certifiedBy and certifierOrganizationId are named at head and were null (title, issuer, certifiedBy) on develop. Builder's 9 N-cells were red on develop by assertion. Data-layer meanings: see K1. issuer_organization_id is absent, measured with a positive control. The owner id is absent as a column but present as a VALUE via certifierOrganizationId (K1).
2. **Nothing else changed.**
   - Own dump: 72 answers (4 paths x 3 callers x 6 fixtures: certified, realistic, anchored-only, revoked, no-tenant, pending-chain), head vs develop product bytes, lineage-walk counts included. Facts are identical in 72/72. Same-tenant and no-tenant answers are byte-identical apart from verifiedAt (32/32). The only differences are the four names and v2's fieldsWithheld. The comparator fired on those 40 differences (control).
   - Lineage skip (D5) holds: walk counts are equal.
   - Chain-first lines are not in the diff.
   - The diff is 2 originate route files + 5 test files + 4 fragments. No auth, rate-limit, billing, gateway, schema or OpenAPI file is touched.
3. **Forced cells (15 in 4 files).** Each inversion is required by the 09:17 card and is narrow. Each keeps its non-name assertions:
   - "cert-a-" absent and the PLANTED issuer absent;
   - the owner and org-column canaries;
   - facts and isAnchored;
   - lineage undefined.
   None is wholesale. ks1561-g188-f1 line 355 (outside the plan list) flips only the title, and issuer stays null as data. FOREIGN ORIGINAL CERTIFIED dropped `not.toContain(CANARY_ORG_UUID)`. In that fixture it guarded only issuerId, so the drop is required, but in production that value is a user id (K1). No Major under Q3.
4. **Tests honest.**
   - Develop product bytes under head tests: 24 red (9 new + 15 forced), all AssertionError, the same as the builder's m0.
   - The harness correction hides nothing. verifiedAt is a per-request time. The marker is pinned by N4. My independent dump (Q2) finds no other difference.
   - m-N7's 10-red set: that mutant nulls the verify-file title for EVERY caller. So ks1986's verify-file cells that assert title "same bytes" on local, foreign and no-local paths also go red. The prediction was too narrow, not a defect.
   - Own mutants: see F1.
5. **Stale contract**: F3, Minor.
6. **PR body and suites.**
   - PR body:
     - Override line present verbatim: "overlap gate: OVL_IGNORE_PRS=2138 2161 on Wednesday's ANSWER 2026-11-16 10:1x ...".
     - No closing keyword (0; a planted "Fixes" control fired).
     - No self-hold sentence: 2 grep hits, "holds" and "withholding", both prose.
     - NOT-run list honest (Schemathesis, Akto, Playwright, k6, real multi-tenant PostgreSQL, production).
     - Tier 1 not named (F2).
   - Whole originate jest:
     - Head: 228 suites, 2739/2739 (load1 6.15).
     - Develop cf2b2a1 in its own tree: 227 suites, 2716/2716 (2708 + ks488 8/8 rerun, F5).
   - tsc:
     - src: rc 0; a planted TS2322 is reported.
     - Tests: 4 errors, all ks1937 and ks488 (pre-existing), 0 in PR files.
   - eslint, 7 changed files: 0 errors, 0 warnings. Planted unused var flagged.
   - docs-fragments check: green; planted unbalanced div red; restored by sha256; green.

## Merge-tree (planted control: PR 2138 conflicts in verification.ts both orders, rc 1)
- PR x develop cf2b2a1: clean both orders (tree 659c5932).
- PR x develop 553c0f8: clean both orders (tree f3a2060b).
- PR x PR 2161 at 0e50defb7819 (re-pinned): clean both orders (tree 0aca64bc, the builder's tree).
- (develop + 2161) x PR: clean both orders, on cf2b2a1 (tree 5607d685) and on 553c0f8 (tree f7e37619).
- develop 553c0f8's three changed ks1634 test files, run against PR head bytes: 22/22 green.

Evidence: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-16_gate374-tier1-pr2249-ks590-names-open/scratch/ (mine_head.json, mine_dev.json, dump_head.json, dump_dev.json, cmp_dump.py, chain.out, chain2.out, mutant_predictions.txt, tsc_*.out, mine/parked/*.test.ts).
