PR 2249: GO WITH NOTES (at head d04080d7a5233d0d1de2d0d755ec304d3d0e0f9f; tier 1)
Head re-pinned by gh api at 01:41:40Z and again at 02:02:46Z: unmoved, OPEN. Develop MOVED during the gate, 72aeaec533dd -> 6f5ac0ec59ad (KS-2125: packages/shared test files and two fragments only). It shares 0 paths with the branch's 16 (control: the branch with itself gives 16). Merge-tree is clean both orders (tree 5e5be8383028). ROUND 2 OF 2: every gate-374 finding is graded below as closed, or as ticketable residue.

# Gate 376, tier 1, round 2: QA findings only (nothing fixed, posted, mailed, pushed or written to Linear or GitHub)

Own clone: scratch/repo, with worktrees h (PR head d04080d7a523), d (develop 72aeaec533dd) and o (round-1 head 10057c4f63c3). node_modules are APFS clones of gate 374's install; the package files are unchanged between the three commits. Every jest, tsc and eslint run went through the load gate (load1 <= 8 at start; logged in the *.out files). Product files were restored by sha256 after every mutant and planted defect. `git status` in h is clean at the end.

## FOR KAM, BY NAME (independent of this PR's verdict)

K-A. LIVE PERSONAL-DATA EXPOSURE ON DEVELOP: CONFIRMED by my own probe.
- What leaks. On develop 72aeaec533dd, an anonymous caller is modelled as the live app does: index.ts line 265 runs `resolveRequestTenantId` unconditionally, so the caller carries the default tenant `a0000000-...0001`.
  - On a default-tenant row, that caller gets the certifier's email local part (as issuer and certifiedBy) and the certifier's (= owner's) user id (as certifierOrganizationId). This holds on all six row-backed paths: v1 by hash, v1 by document id, v1 verify-file, v2 verify, v2 by document id and v2 verify-file.
  - On ANY row, every caller (anonymous, another company, the same tenant, the owner) gets the user id through certifierOrganizationId.
  - Chain-first answers give every caller the anchor's user id (issuerOrgId) and, on a legacy anchor, the local part.
  - Evidence: scratch/dump_dev.json, scan_dev.txt, table_dev.txt; 336 answers; 260 carry the user id or the local part.
- Kintsugi runs the same code.
  - Kintsugi's originate is D 65th's k29 build `6185f0f1ace8`. D 66th's k30 (pin 72aeaec533dd) was building, not yet swapped, at its 01:24Z HANDOVER.
  - `git diff --quiet 6185f0f1ace8 72aeaec533dd` over verification.ts, verificationV2.ts, index.ts, utils/requestTenant.ts, certifications.ts and certificationRepo.ts gives rc 0. The control, adminConfig.ts, gives rc 1.
  - So the k29 build now running and the k30 build being deployed carry this exposure byte-for-byte.
  - Not probed live: no box, no ssh. Whether Kintsugi runs single-tenant (where every anonymous caller is a default-tenant caller) is UNMEASURED. The demo's build and production are UNMEASURED.
- This PR closes the exposure. Develop and Kintsugi stay exposed until it merges and deploys.

K-B. C44-R4 residual, sized (not a defect of this PR). Rule R still shows whatever a registrant or certifier TYPES into a company field:
- a person's name ("Rowan G Citizen" in certificationData.issuedBy is shown: FX7);
- an email written with a fullwidth at sign "＠" (U+FF20): the "@" filter is ASCII only (FX6);
- the TITLE, which Kam opened, is free text and can carry an email ("Payslip for rowan...@example.test" is shown: FX9).
No server path writes a person-derived value into any field Rule R reads. My write-side read found:
- organizations rows are created only by admin and seed routes and by Platform-S registration, with an explicit name or "Organisation <externalRef>";
- documents.ts refuses an "@" in a top-level issuerName;
- certifications.ts puts the local part only in certification_metadata.issuerName, which Rule R never reads;
- certificationData is the caller's typed `data`.
So the residual is limited to typed text.

K-C. DIDs on chain-first answers (pre-existing; this PR does not change it). `onChainMetadata` is anchoring's buildVerifyResponse metadata. publicOnChainMetadata nulls only issuerOrgId and issuerName, so `identity.actorDid`, `identity.orgDid` and `identityCommitment` reach every caller on all four chain-first paths, at head and on develop alike (CH2, 16 of 16).
- KS-1175 ruled the block non-PII, and it is already on the public chain.
- An actorDid is a persistent per-person identifier, though, and the commission lists "a DID". Whether it counts as personal data under the 11:12 ruling is Kam's call.

## Round-1 (gate 374) findings: status

| # | Round 1 | Now |
|---|---|---|
| K1 | Major, Kam's: local part on 4 paths, user id on D-B3 | **CLOSED.** Rule R never reads certification_metadata.issuerName. certifierOrganizationId is null with the key kept. Chain-first issuer, certifiedBy, COID, issuerOrgId and issuerName are null. Measured: 0 of 288 answers carry the user id, local part, org column or connector principal (my fixtures, typed-content fixtures excluded). |
| F1 | Minor: gB, gC survive | **CLOSED.** Re-run on my bytes: gB 6 red, gC 5 red, all by assertion. |
| F2 | Minor: PR body did not name tier 1 | **CLOSED** (`TIER 1` 2 hits). |
| F3 | Minor (doc): stale contract | **OPEN, ticketable** (S 86th; the brief kept it out of scope). Now slightly wider: originate.openapi.ts line 446 still says "Organisation id of the certifying issuer", and examples 547 and 750 show a UUID for a field that is now ALWAYS null. fieldsWithheld 674-677 and 2093, yaml 6873 and 30222. Harmless at runtime: the field is nullable. |
| F4 | Note: wording | **CLOSED.** The PR body and fragments are corrected. |
| F5 | Note: ks488 / ks1937 EmailModule | **OPEN, pre-existing, ticketable** (the READY's candidate 6). It did not fire in my two whole-suite runs. |

## New findings (round 2)

| # | Sev | Finding |
|---|---|---|
| G1 | Minor (ticketable) | publicCompanyName's filter has two gaps. It is ASCII-"@" only, so "rowan.g376＠example.test" (U+FF20) is shown. `trim()` does not remove U+200B, so a zero-width-only typed name is shown as an invisible issuer (FX5). Both need a typed value. This is the C44-R4 class, not a person-derived write. Fix shape: NFKC-normalise before the check, and treat format characters as blank. |
| G2 | Note | Cell-strength gaps. Mutant g7 (certificationData.issuedBy swapped ahead of metadata.issuerName) SURVIVES all 206 cells, so the order between the typed fields is unpinned. Not a personal-data risk. The rewritten ks1557 order cell is green on the round-1 bytes too, so the reverse red-first is 19 forced cells, not 20. ks1986 FOREIGN ORIGINAL CERTIFIED asserts COID null but has no text-level `not.toContain(CANARY_ORG_UUID)`; ks590p's leak check covers that. |
| G3 | Note (for Wednesday and gate 375, out of this PR's scope) | PR 2250 (9ec3e460b68d) answers certification verify with issuer.id and issuer.did to ANY signed-in caller, another company's included; only anonymous callers get null. That is narrower than this PR's view X for document verify. |

## The six questions

**1. Personal data out, measured from the write side.**
- What each disclosed field HOLDS at head:
  - title = documents.title (free text);
  - issuer = certification.certifiedBy = publicIssuerName(row): organizations.name, else metadata.issuerName, certificationData.issuedBy, metadata.issuedBy, metadata.certifiedBy, each trimmed, non-empty and without "@";
  - certifierOrganizationId = null;
  - blockchain = the stored anchor blob (anchorId, txHash, height, status; no identity: its writers are certifications.ts 586, documents.ts 1038/1054/1780, anchorStateSync confirmedBlobOf);
  - chain-first onChainMetadata = anchoring's metadata, with issuerOrgId and issuerName nulled (identity block: K-C).
- My dump (scratch/mine/parked/g376-dump.*.test.ts) has 12 row fixtures and 3 chain fixtures. They are not the builder's: certification_metadata exactly as insertCertificationRow writes it (issuerDid, holderId, holderName, holderDid, certificationData.recipientEmail), metadata uploadedBy and ownerId, a connector principal, a GDPR-erased issuer, unicode, NBSP and "@" org names, typed person and email values, and an email in the title. The paths are 6 row paths and 4 chain paths; the callers are anonymous-live, another company, the same tenant and the owner. That is 336 answers per tree.
  - Leak scan with a planted control (every value plus an IP planted; all 16 detected):
    - head: 0 user id, 0 holder id, 0 org column, 0 issuer or holder DID, 0 holder name, 0 connector principal, 0 IP, 0 caller id or email;
    - local part and email hits only in FX6 and FX9 (typed: K-B, G1);
    - DIDs only in CH2 (K-C).
  - READY's "54 of 54 vs 0 of 54" REPRODUCED in shape with my fixtures, excluding the two typed-content fixtures. Carrying the user id, local part, org column or connector principal:
    - round-1 head 10057c4f: 248 of 288;
    - develop: 236 of 288;
    - head d04080d7: **0 of 288**.
- Fixture caveat: the builder's ks590p models single-tenant mode (getTenantManager null), and so does mine. Cross-tenant pools are not exercised by either. By reading, every issuer, certifiedBy and COID site on every path goes through publicIssuerName, buildCertification, resolveTrustedCertificationEvidence or the chain-first nulls (grep of both route files).

**2. Names still open.**
- Title and company reach every caller on all six row paths. One view: 84 of 84 fixture-and-path groups give byte-identical answers to all four callers (verifiedAt removed).
- Rule R edges:
  - "  Contoso Pty Ltd  " -> trimmed;
  - NBSP-padded -> trimmed;
  - "Société Générale — Zürich 株式会社" -> kept exactly;
  - "Support @ Acme" -> skipped to metadata.issuerName;
  - "[erased]" in certification_metadata -> never read;
  - G1's two gaps.
- certifierOrganizationId is null with the key PRESENT on every certified answer.

**3. The owner's own answer changed (view X).**
- No in-repo consumer reads certifierOrganizationId: the frontend schema only (verify.ts 121, nullable and optional).
- `issuer` and `certifiedBy` are read only as display text: verifier ResultPage 397-405, gmail-addon, outlook-addin, whatsapp-bot, flutter app, nextcloud, euro-office plugin, python SDK and mcp-server.
- The issuer portal's verificationApi.verify has no caller.
- Admin views read certification_metadata.issuerName from the DB directly (adminConfig ~1638) and are unaffected.
- Client-visible consequences:
  - a certified document with no organizations.name and no typed company now shows NO issuer to anyone, the owner included ("Unknown" or blank in those clients), where it showed the certifier's local part;
  - chain-only answers show no issuer;
  - the user id is gone.
  - Wednesday's receipt already names the chain-only change; name the no-company case too.

**4. Develop today.** CONFIRMED: see K-A.

**5. Chain-first (b).**
- On all chain paths (v1 by hash, v1 verify-file, v2 verify, v2 verify-file) and every caller, issuer, certifiedBy, certifierOrganizationId, onChainMetadata.issuerOrgId and onChainMetadata.issuerName are null (CH1, CH3: 32 of 32).
- Mutants:
  - my g3 (v2 chainOnlyMatch issuer restored to the "@"-filtered chain name): 2 red (P6b and P6c on v2), as predicted;
  - the builder's m7 and m8 are reported red (not re-run).
- Nothing else changed: with the name fields removed, head and develop agree on 336 of 336 answers (status, verdict, checks and anchor facts). A planted `checks` flip is detected (1).

**6. Tests and housekeeping.**
- Red-first, all by AssertionError, 0 other:
  - ks590p on develop bytes: 48 of 53 red;
  - head's 7 test files on round-1 bytes: 67 red (48 ks590p + 19 forced; the ks1557 order cell is green both ways: G2).
- Forced edits: 20 cells in 6 files (ks590n 13, ks1986 2, ks1557 2, ks584-p3 1, ks1561 1, ks563 1). Each changes only a name value (certifiedBy or COID) and cites the 11:12 card. Every non-name assertion is kept.
  - ks1561 C2's 'Org B' -> null is required by Rule R. 'Org B' sat in certification_metadata.issuerName. A legacy certify with a typed issuedBy still names it through certificationData.issuedBy (certifications.ts 840-846 stores both), so no typed company is lost.
  - None weakens a tenant, owner or column guarantee.
- My mutants. Predictions are in scratch/mutant_predictions.txt and results in mutants.out and mutants2.out, run over the 7 files (206 cells), m0 206 of 206 green:
  - g1 trim dropped: 8 red;
  - g3: 2 red;
  - g4 (a same-tenant-only owner id on v1 by hash): 4 red;
  - g5 (anonymous-only raw metadata on verify-file): 5 red;
  - g6 (v2 org-column leak): 5 red;
  - g9 (the local part back in certifiedBy only): 36 red;
  - gB: 6 red; gC: 5 red;
  - g7 (order swap) SURVIVES (G2).
  - All reds are AssertionError; sha256 equal after each.
- Whole originate suite:
  - head: 229 suites, 2,792 of 2,792 (load1 4.44 at start);
  - develop 72aeaec533dd: 227 suites, 2,716 of 2,716 (load1 7.89).
  - The difference is exactly ks590n (23) and ks590p (53).
- tsc over originate src: rc 0. A planted unused local in verificationV2.ts gives rc 2 with TS6133 x1; restored sha256 OK.
- eslint `--max-warnings 0` on the 2 product files and 7 test files: rc 0, no output. A planted unused variable is flagged (@typescript-eslint/no-unused-vars).
- docs-fragments check: OK (two expected ADVISORY lines). A planted unbalanced div gives FAIL rc 1; restored sha256 OK; re-check OK.
- PR body:
  - TIER 1 named (2);
  - rulings quoted as facts (Kam 7 hits);
  - the chain-first sentence verbatim (1);
  - the new override line "OVL_IGNORE_PRS=2138 2161 2249 on Wednesday's ANSWER 2026-11-16 00:56:07Z (grant C44-R3...)", with the round-1 line labelled;
  - no closing keyword (0; a planted "Fixes KS-1" gives 1);
  - no self-hold sentence (the one "hold" hit is "the lineage skip holds");
  - an honest NOT-run list (Schemathesis, Akto, Playwright, k6, multi-tenant PostgreSQL, production, preview's legacy anchors).

## Merge-tree (scratch/mt.out; planted control: PR 2138 fdf80425 conflicts both orders, rc 1, in verification.ts, ks563 and VERIFICATION.md)
| other side | order a | order b | tree |
|---|---|---|---|
| develop 72aeaec533dd | clean | clean | 2ebc664bdeed |
| develop 6f5ac0ec59ad | clean | clean | 5e5be8383028 |
| PR 2161, head 0e50defb7819 | clean | clean | 4a9b6deee237 |
| PR 2250, head 9ec3e460b68d | clean | clean | c31a543df990 |

PR 2161's own diff to the two route files touches no issuer, certifiedBy, owner or organization line (grep 0; the same grep on this PR's diff gives 53). PR 2250 does not touch verification.ts or verificationV2.ts.

NOT RUN: a live probe on Kintsugi, the demo or production; real multi-tenant PostgreSQL (cross-tenant pools); Schemathesis, Akto, Playwright, k6; the builder's m1-m8 re-runs.
Evidence: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-16_gate376-tier1-pr2249r2-ks590-personal-data-out/scratch/ (dump_{head,dev,old}.json, scan_*.txt, table_*.txt, cmp_facts.py, scan_dump.py, mutants.py, mutants*.out, rf_*.out, whole_*.out, tsc_*.out, docs_*.out, mt.sh, mt.out, pr_body.md).
