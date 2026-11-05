# Gate 208 commission — Secuura / Blockchain, PR 2017 (KS-692: status revoke/unrevoke bound to the credential's creator, vc-issuer), TIER 1, ROUND 1 of 2

Written by Wednesday 2026-11-05 ~22:08 AEDT. Model: Opus (tier 1: an authorization check on a credential-status write path; Kam's card says "gated"). QA GATE: findings only; fix nothing; write nothing outside this folder; no box; post nothing to Linear or GitHub; no external network.
`verdict.md` holds the INCOMPLETE stub; overwrite at the end. Final line 1 is exactly `GO`, `GO WITH NOTES` or `NO GO (<reason>)`.
Read first, whole: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md, then `ready_2017.txt` here (Seat F 34th's READY, verbatim) and `card_ks692.txt` here (Kam's ruling). Clone read-only: `git clone --shared /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files <subfolder here>`; if objects are missing, another gate folder's clone under /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate20*/ may be a second --shared source; never fetch into the shared checkout. Never `cd`; never a recursive grep/find over 0_Brain/reference, local-model/ or 5_Project_History.

## Subject (Wednesday's `git ls-remote origin`, 22:08:16 AEDT)
refs/pull/2017/head = `536bca3aa4754b46639ffc4df2e55ed368633dd8` (2 commits: 71c3abf6be5b the change on 5fc5569ed96a, then a merge of develop c9cb07738cf6); develop NOW = `1b1b65c7415ff02b9e3b44e83b62d9a609adfe8b` (NOT merged into the PR). Seat-stated 8 files +649/-24: services/vc-issuer/src/routes/status.ts, five vc-issuer test files, a fragment pair.

## Rulings you check against (binding)
- Kam card secuura-ks692-status-revoke-bind-creator-1105 = a (16:54:07): "Build it now (an Opus seat, same pattern as KS-1851, gated)". Model ruled earlier by Kam: bind-creator (13 Sep).
- Wednesday's design rulings to the seat (06:18Z / 06:20Z): Q-A the owner is the credential's STORED owner via getRecordById(body.credentialId), no list owner, no migration; Q-B (i) exactly the KS-1851 pattern (platform roles NARROWED: no platform bypass); Q-C the gate stays default-deny, the exemption is exactly a signed-in POST /<id>/revoke or /<id>/unrevoke, anonymous still 401; Q-D a refusal answers the existing 404 "Credential not found in status list" byte-identical; order: shape, list, owner, entry, KS-1371 lines untouched, write.

## Questions
1. Scope: exactly the 8 paths; status.ts changes only the revoke/unrevoke ownership check and the gate exemption; the merge commit brings nothing but develop's files (0 shared).
2. Authorization table, base vs head on the real routes with only storage doubled: {anonymous, creator, same-tenant non-creator, other-tenant user, platform SYSTEM_ADMIN own tenant / other tenant} x {owned credential, owner-less with tenant, owner-less without tenant, not stored} x {revoke, unrevoke}. Head: only the creator (and nobody on owner-less/not-stored) is admitted; no caller head admits that base refused EXCEPT the creator's two declared gains; every refusal is the byte-identical 404; anonymous 401. "N of M". Confirm the seat's 14 NARROWED platform cells are what Q-B (i) requires.
3. The gate exemption: reproduce the path tricks (encoded slashes, trailing segments, case, double slash, method override, a different POST) and show the exemption admits exactly signed-in POST /<id>/revoke|unrevoke; one widen-to-any-POST mutant of your own.
4. Ordering and side effects: no write, no list mutation and no status change on any refusal; the owner check happens before any entry read that could leak existence (404 identical for not-owned vs not-stored: compare bodies, headers, timing-insensitive fields).
5. Mutants: reproduce 4 of the seat's 11 (incl. M8 owner-less admitted, M10 exemption to every POST) and one of your own.
6. Suites: vc-issuer vitest (classify failures same-on-base vs new; ks1868 C1 is a known timeout), tsc incl. tests, eslint, docs-fragments with a planted defect. systemTest test_status_list_authz.py:136 will read 404 not 403 (seat-declared): confirm by reading, and say whether the PR names it.
7. Merge tree onto develop 1b1b65c7415f: rc and tree; shared paths with everything merged since c9cb07738cf6 = 0 (planted control).

## Output
`verdict.md` (verdict line, BLUF, findings with severity, file:line, evidence path). Final message: verdict line + one line per finding.
