# Gate 192 commission — Secuura / Blockchain, PR 2004 (KS-1986: verify v1 judges the original registration across tenants, as v2 does), TIER 1, ROUND 1 of 2

Written by Wednesday 2026-11-05 07:5x AEDT. Model: Opus (routing v1.0 tier-1 gate: a public verify path's certification and tenant-disclosure behaviour). Spark shadow: NOT run (Kam 2026-11-04 16:42 "ignore the spark until further notice").

## What was ruled, so what this PR must be
- Kam's rulings: card secuura-ks1561-duplicate-hash-certifier-1102 = a ("Certify only for the org holding the ORIGINAL registration ... Stops the later registrant outranking the original") and secuura-ks590-verify-disclosure-four-questions-1102 = a ("Strict: no tenant-owned naming incl. org UUID on all four paths"). Merge hold RELEASED by Kam 07:07:25 AEDT (card wed-morning-fleet-activity-1105 = a).
- Accepted design (Wednesday's ANSWERs to Seat F 31st 19:32Z, 19:43Z, 19:54Z; F 32nd 20:16Z, 20:24Z): D-B1 combined eligibility (a local row presents a certification only if eligible under BOTH today's rule and the cross-tenant rule: head never more permissive than base by construction; one stated edge where v1 refuses what v2 accepts); D-B2 present the foreign original (scrubbed) when no local candidate remains, NO fallback to crossTenantLookup; D-B3 certifierOrganizationId nulled on the NEW path only; D-B4 fail closed on any registry/originals read failure; chain-first re-read and crossTenantLookup unchanged; ONE existing cell (ks1561-g188-f1 test, N-SPLIT) changed by ruling (numstat 2 2). Pushed on its built base 035685291b9d by ruling (no merge commit).

## Questions (tier 1: measure, do not take the READY's word)
1. **Scope:** the 5 files in the READY and nothing else; the existing-test change is exactly 1 expect + 1 describe line (numstat 2 2), 0 other lines; no api-gateway file, no migration, no verificationV2.ts.
2. **The class bar (Kam's):** over v1 /verify and verify-file, base vs head, over the seat's matrix AND at least 3 cases of your own design (e.g. three tenants with the original tied in two; the caller holding both a certified latecomer AND an uncertified later copy; a soft-deleted/revoked foreign original if the schema has such a state): any head response presenting a certification base did not = a Major; a head response presenting a DIFFERENT certification must be the original holder's own. Count it yourself on a real PostgreSQL 15 (your OWN cluster, socket only, pid-recorded; the keg is /opt/homebrew/opt/postgresql@15).
3. **Disclosure (KS-590 a):** field-by-field diff of the v1 response head vs base for every cross-tenant case; plant a distinctive org name, owner id, issuer org UUID and title on the foreign original and search the WHOLE serialized body and headers (a control that shows the search finds a planted value where base does expose one). Any foreign tenant field visible at head that base did not show = HOLD-FOR-KAM.
4. **Fail closed:** registry read fails, one tenant's originals read fails, a tenant DB missing: v1 must not present a certification as if the original were local; any 500 or uncaught throw is a finding.
5. **G188-F1 not reintroduced:** the original is MIN over the FULL same-hash set; 24+ later copies in the original's tenant must not let a latecomer's certification reappear (reproduce the seat's m3 and make it fail).
6. **m4 survivor (dedupe by object identity instead of id):** judge F 31st's equivalence argument (it is in the PR body). Try to construct an input where it changes an answer; if you cannot, say what you tried.
7. **Cost:** count queries per v1 verify (multi-tenant with local rows; single-tenant must be 0 extra); the registry cap of 8 and what happens when more than 8 tenants hold the hash (which tenants are dropped, and can that hide the original?). If dropping can hide the original and present a latecomer's cert, that is a Major.
8. **Red-proof + suites:** reproduce at least 3 of the seat's mutants incl. m1 and m2, plus ONE of your own; whole originate suite at head; tsc incl. tests; eslint on the three files; docs check with a planted defect.
9. **Title/body:** "Refs KS-1986:" <= 92 chars; body line 1 = Kam's release line; the commit body carries a stale "HOLD: do not merge ..." line (known, superseded in the PR body line 2): confirm the PR body says so; no close word before a key.
10. **Merge:** merge-tree of the head onto CURRENT develop 4ff25fb4f2c05192be178f941d746175d609471f (PR 2002 merged since the base; re-read develop at your start and end) rc + full tree; 0 shared paths with the range 035685291b9d..develop, with a planted control.
11. **Filing candidate (c) in the READY** (verify-file passes 'sha256:<hex>' to crossTenantLookup whose registry read compares content_hash = $1): read the create path (documents.ts:794 area) and the registry writer at head, and say which form registry rows hold in code; mark it pre-existing (base = head) or not.

## Subjects (re-pin yourself at start and end)
- Repo Secuura/Distributed_Secuura; read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (fetch the PR ref into YOUR clone only; never write to the checkout).
- **PR 2004** head `577f668f478679a3e4965a28fba6b96a9e2212d6`, base (built on) `035685291b9d58ae6ea8ba5f05adf9379f9c2944`, develop now `4ff25fb4f2c05192be178f941d746175d609471f` (Wednesday's ls-remote 07:5x AEDT).
- F 32nd's READY: `ready_2004.txt` here (read it whole). Seat records: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-05_seatF-31st/` and `.../2026-11-05_seatF-32nd/` (its PG harness pgcell/ and evidence/pg/ may be reused by copying, never run in place).
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate192-ks1986-pr2004/`. Dependencies only from an install matching the lock at the head.
- Live seats: D 52nd (demo deploy, box only), B 93rd (merge seat), F 32nd (wrapping). Do not touch their worktrees, processes, ports or clusters. No contact with demo or kintsugi.
- NOT TESTED by design unless you do it: Node 24, a real deploy, real Platform S traffic. Say so.

## Verdict
Line 1 per gate_common section 6, for PR 2004, and the merge tree on develop 4ff25fb4f2c0 for the merge seat. Then FOUND / TESTED / HOW with controls.

