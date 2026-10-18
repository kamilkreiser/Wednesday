# Gate brief: PR #1568 (KS-1612 + KS-1385 (b)), ROUND 2 OF 2 = THE CAP, Opus TIER 1 FULL

Commissioned by the Wednesday seat on 2026-10-18 at about 22:0x AEDT, under routing v1.0, row G1: model claude-opus-5-5. Round 1 went NO GO: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-18_gate-pr1568/verdict.md (sha 41dc7991bc4fd6ff). It found MAJ-1, a cross-tenant identity rewrite through an external_id equal to another tenant's pkey (cells XT1/XT2 in that folder's cells/gate_matrix.ts), plus MIN-1 (the quiet set) and MIN-2 (stale authority comments). **This is the LAST round:** if it is NO GO, the closed instances ship and the residue is ticketed. A third round needs Kam. Say plainly what would block. 0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/, and project paths are under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

- **Head:** 767ab575818f75b68664ddad1a511478db63c09d, per Wednesday's ls-remote. develop 833984fc9 is merged in. Live develop has since moved to 26378a40378dc53787f69a96609a90cad499d50b (Seat R's tier-2 merges); re-read it.
- **WEDNESDAY'S RULING, a claim for you to test:** design (b). The id namespaces are made disjoint database-wide by migration 050. It is an uncallable SECURITY DEFINER `BEFORE INSERT OR UPDATE OF id, external_id` trigger on documents, which refuses a uuid-shaped external_id equal to another row's pkey, or a pkey equal to another row's external_id, in any tenant. It raises 23505 with CONSTRAINT documents_id_namespaces_disjoint and a fixed message that names no id and no tenant. Legacy collisions fail closed: the migration counts them and refuses. A read-only census is in 050's header. The ruling asked for no callable cross-tenant function and no (a). originate maps ONLY that code plus that constraint to the existing 409 body, byte for byte. The guard's logic is unchanged. The race is accepted as a residual. KS-1603's direct POST /api/anchors route is out of scope.
- **Author's additions, beyond the design mail:**
  - An RLS-bypass assert in the migration, so that a run as a non-bypass role cannot read a false 0.
  - CASE and nested-IF cast guards, so that a `doc-...` external_id cannot raise 22P02.
- **Author's claims (NOT evidence):**
  - A fresh DB built through scripts/run-migrations.sh: applied=52, failed=0.
  - Red-first in two dimensions (the DB without 050, and the code without the fix), with the predicted cells red.
  - R2: another 23505 stays at 500. R3: the right constraint with a different SQLSTATE also stays at 500.
  - MIN-1: Q5-Q8 through the real guard, including the L3 connector token. MIN-2: three comment sites rewritten.
  - Preflight: the PR body's table (13/16 or 12/16; name the skipped legs).

## Gate
1. **Re-run round 1's MAJ-1 cells XT1/XT2 with the colliding row in ANOTHER tenant**, through the booted anchoring service and originate's saveDocument, at your own Postgres. Use a free port via lsof, not 55418, with FORCE RLS and a NOBYPASSRLS app role. Expected: the colliding create is refused 409, its anchor never lands, and public verify keeps the victim's identity. Also run the raw INSERT as secuura_app.
2. **The trigger itself:**
   - Is the function uncallable by every app role, and even by its owner? Does it fire for every insert and update path, including UPDATE OF either column, COPY, and bulk inserts?
   - Test both directions, case variants of the uuid, and leading or trailing whitespace in external_id.
   - Confirm the race residual as stated.
   - Check what the 409 reveals (byte-compare it with the same-tenant refusal).
   - Confirm R2 and R3 (only that code plus that constraint maps to 409).
3. **The migration:**
   - Does it apply clean on a fresh DB, and REFUSE (with a planted collision) and name the census?
   - Does the RLS-bypass assert refuse under a non-bypass role (prove it fires)?
   - Is it safe to re-run (idempotent)?
   - Does its census match the trigger's rule exactly?
4. **Kam's (b) still holds:** a NULL-issuer certification is updated by the holder's organisation, and refused for others. INF-1/INF-2 behaviour is unchanged; Kam has a card on it.
5. **MIN-1 and MIN-2 closed:** check develop's quiet set (round 1's L1-L5) and the three comment sites.
6. **Mutants:** run the author's, plus two of your own on the trigger and two on the 409 mapping, plus a comment-only control.
7. **Merge prediction on the LIVE develop,** with an overlap check and a planted conflicting control.

## Rules
- Read-only on the project. Work in your own clone under /private/tmp/claude-501/ (folder gate1568r2):
  - git clone --shared from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files;
  - set origin to git@github.com:Secuura/Distributed_Secuura.git;
  - fetch with that checkout's core.sshCommand plus `-o ServerAliveInterval=30`.
- No git write verb in !CODING, no push, no GitHub or Linear writes, no Docker, no remote box.
- Never cd, and delete nothing.
- **Every loop or multi-step command goes in a script FILE, run as `/bin/bash /abs/path/script.sh`.**
- Write only in this folder and in your scratch dir.

## Output
- Write 0_Brain/reference/2026-10-18_gate-pr1568-r2/verdict.md.
- Line 1: the VERDICT, naming the head.
- Line 2: the sha256/16 of the report (delete line 2, sha256 the rest, take the first 16 hex).
- Then: FOUND / TESTED / HOW, NOT tested, severities with file:line, and `WALL-CLOCK: <min>`.
- This is round 2 of 2. A merge happens only on Wednesday's head-bound GO, and nothing deploys. Migration 050 needs the census on every box first.
