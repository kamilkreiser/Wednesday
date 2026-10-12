# Gate brief: Secuura Platform K PR #1525 (ticket KS-1538), OPUS tier 1 — authorisation write path

Commissioned 2026-10-13 ~06:4x AEDT by the Wednesday seat.

## What you are gating
- Head `b8393a44ec33984f7380cf5fdfb4f9cd8e87cd74` (Wednesday's ls-remote). Base develop 69878dc5; develop is now `81ac1ea60ec684f1636a25832d9a7f3bf28470f5` (KS-1521, tests only in governance/staking/transfer; author says 0 overlap). Author Seat J 5th. Two commits: fix 1251ae7a3242 plus a develop merge.
- Change: POST /api/certifications/issue with a documentId and NO parentDocumentId now requires the SAME access GET /api/documents/:id requires (owner, system admin, designated recipient, creating connector), checked BEFORE the holder lookup, the anchoring submission and saveCertification; one refusal byte-identical for an unknown and a not-yours documentId; the UPDATE's empty catch now logs one line and keeps the 201. Wednesday's rulings: predicate (O) like GET; NO extra predicate on the UPDATE (external_id is unique); a STRICTER rule for OWNERLESS documents (a connector that created a document without onBehalfOf can no longer legacy-certify it; pinned by a cell named DECISION).
- Author's numbers (NOT evidence): unfixed develop: 6 of 10 integration and 13 of 19 unit cells red ("Expected 403, Received 201"); fixed: unit 19/19, integration 10/10 in BOTH tenancy modes as secuura_app (NOSUPERUSER NOBYPASSRLS); 22 mutants all killed plus a control; whole originate jest 103 suites / 1234 tests; hook 13/16 legs, 3 skipped.
- The author's own attack list (unprobed): (1) getDocument resolves external_id then the pkey UUID while the UPDATE addresses external_id only; (2) wasCreatedByConnector uses the module's global prisma client, not req.db, with no tenant predicate; (3) timing difference between unknown and not-yours; (4) check and UPDATE not in one transaction; (5) the lineage path (parentDocumentId set) does not run this check; (6) GET's ownerless pass-through left as is.

## How to get the code (READ-ONLY on the project)
- `git clone --shared` of `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` into YOUR scratchpad; fetch `refs/pull/1525/head` and develop with the project's `core.sshCommand`, or use `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-13_seatJ-5th/ks1538_pr1525_b8393a44_full.bundle` (sha256/16 ac583727d5683561, verified). Assert the head. Throwaway Postgres you start yourself (J's recipe: `5_Project_History/2026-10-12_seatJ-4th/tools/setup1497.sh`, read it before running; use a port in 55410-55419 not in use); stop it when done. No pushes, no GitHub/Linear writes, no remote boxes.

## What to attack
1. Re-measure the hole on unfixed develop and its closure at the head, over the REAL route in both tenancy modes as the app role: org A user, org A admin, org A connector (with and without onBehalfOf), system admin, designated recipient, the creating connector, each against org B's document, an unknown id, a pkey-UUID-addressed id, an ownerless document. Assert the stored row after each call (status, certified_at, certification_metadata), not only the status code.
2. Probe the author's items 1-4 and say for each: exploitable / not / unmeasured, with the shape.
3. Item 5, the lineage path: can a caller attach a derived document under, or certify through, someone else's document via parentDocumentId? Measure; if yes, it is a finding against the ticket's scope, report it as a separate item and say whether it blocks this PR (it should not block unless this PR made it worse).
4. Does anything that legitimately used this path before now break (the issuer frontend's issue() call sites; the creating-connector arm with onBehalfOf)? Read the call sites.
5. Kill at least: predicate removed from the pre-check, pre-check moved after saveCertification, unknown-vs-not-yours made distinguishable, creating-connector arm dropped. Suites at the head.

## Output
- `0_Brain/reference/2026-10-13_gate-pr1525/verdict.md` (this folder only, plus your scratchpad; raw outputs under `evidence/`, never a directory named `out`). Head under test; numbers with instruments and controls; FOUND / TESTED / HOW; NOT tested.
- VERDICT: GO / GO WITH NOTE / NO GO; Majors and Minors with file:line and the reproducing shape. The merge also waits for a client answer; do not recommend merging.
