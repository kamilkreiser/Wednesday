# Spark operator o119 (carve round) — report
Saved by Wednesday (18:46 seat) from the operator's final message, because the operator's own Write was refused. The text below is the operator's, in condensed form; the lint, dry-run and control outputs, prscan.py, prs_start.json and prs_end.json are in this folder.

Spark rounds o119: 1 briefed, 0 PASS (0 held), 0 FAIL, 0 still queued. Run 18:49 to ~19:05. develop f98afb113c2d at both ends (ls-remote). Open PRs checked: 58 at both ends, through the GitHub PR files API (303 -> 302 files, no PR added or dropped). Controls on the scan: PR 2099 gdprService.ts; PR 2087 originate adminConfig.ts; PR 2073 api-gateway routes/platform.ts; PR 2092 scripts/audit/*; PR 2101 originate ks1634 tests. Nothing queued, raised, pushed, posted or mailed.

## Per source ticket
- **KS-590:** carved gap 3 only (old rows with no tenant). In services/originate/src/routes/verification.ts:458, `if (!rowTenant) return false;` becomes `return true;`, plus an inverted pin cell and one new cell in ks584-verify-row-selection.test.ts. This is an anonymous-verify security file, so it is a fully spelled-out edit (routing v1.0 item 4); tier code_patch2; a tier-1 gate is owed.
  - Brief: 2_Project_Files/local-model/night/briefs/ks_590_o119_p1_verify_withholds_tenant_fields_of_a_row_with_no_tenant/KS-590.md, with golden.diff and spark.pins. Lint rc 0, dry-run rc 0.
  - NOT QUEUED (brief defect). The golden --control run fails A6 (whole suite): two other existing cells go red, ks563-certified-vs-anchored ('reports isCertified TRUE only for a certified document') and ks1939 'control ks1939 C2'. Both build untenanted rows and call anonymously. A1, A2, A3, A3c and A3x pass; A4 shows 2 red by assertion; A5 13/13; A7 tsc rc 0.
  - The change needs 3 test files edited (ks584, ks563, ks1939), over code_patch2's 1-2, so it fits a Claude seat.
  - Not carved: gap 1 (certifierOrganizationId survives scopeTenantFields); gap 2 (the chain-first branches skip the scrub; needs a real 64-hex tx); gap 4 (the by-id path selects no tenant_id).
  - Behaviour change for the gate: the titles of untenanted rows disappear for every caller. Whether demo data has such rows is UNMEASURED.
- **KS-1632: no honest piece.** One change across 6 files, and no part is safe alone: removing the seed alone leaves the UI rendering an empty pill; frontend/admin has 0 test files; adminConfig.ts is in PR 2087; platform.ts:989 is in PR 2073.
- **KS-757: no honest piece.** gdprService.ts is in PR 2099. A GDPR erasure concurrency design can't be shown with a mocked test.
- **KS-960 / KS-1200: no honest piece.** Each starts with a per-environment schema read, which is a runtime read the Spark can't do. The KS-1990 seed fix is in adminConfig.ts (PR 2087).
- **KS-651: no honest piece.** The doc half is under Blockchain/Dev/docs/ (excluded); lock-discovery.mjs and baseline-contract.mjs are in PR 2092. Measured: packages/shared/package-lock.json is tracked, so the ticket's 'invisible to audit gates' claim is partly STALE (the 22-service count was not re-measured).
- **KS-636: no honest piece.** New infrastructure (scheduled Trivy, a deploy record, a doctor check), not a repo file.

## Why the Spark is idle after o119
Each row either spans more files than a tier allows (KS-590 needs 3 test files, measured by the golden control; KS-1632 needs 6) or sits in a file an open PR holds (PRs 2099, 2087, 2073, 2092). KS-960 and KS-1200 need a runtime read. The next widening is a Claude seat for KS-590 gap 3 with its three test edits, or a raise/merge round that frees adminConfig.ts, gdprService.ts and platform.ts.
