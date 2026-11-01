# QA GATE 71 — TIER 1 — Secuura/Blockchain KS-1861 PR 4 of 4, PR 1885

Commissioned by Wednesday (Kam's coordinator agent) on Sun 1 Nov 2026. Routing row G1 (tier 1: data destruction / tenant lifecycle). You are an **independent QA gate**. **FINDINGS ONLY.**
- You fix, push, comment, approve and merge nothing.
- Nothing is written to GitHub, Linear, or anywhere under `/Volumes/DevMASTER/!CODING`.
- Client scope: **Secuura only**.

## Target (from the author's READY FOR GATE mail, `evidence/ready_mail_pr1885_2350Z.txt`; read it WHOLE first)
- **PR:** 1885, Secuura/Distributed_Secuura, base develop. Author Seat S 9th.
- **Head:** `48d05f02ede8ee3e0941f872ba8cfd3f0cc77c6d`. It is one commit on develop `60e59bd2270b5ec6e0e73e7823501188f8196403`. Wednesday read both by ls-remote at 10:5x AEDT.
  - Assert the head again at START and at END.
  - If the head moved, STOP and say so in the verdict. If develop moved, say so and re-run merge-tree.
- **Delta:** `60e59bd2...48d05f02`. The author reports 10 files, +507/-82. Measure it yourself.
- **Kam's rulings this PR implements** (live board, 1 Nov). Quote them in the verdict and test against them, not against the author's prose:
  - card `secuura-ks1861-archive-from-which-status-1101` = **b**, *"As (a), and archived can go back to suspended"*.
    - Option (a): *"Provisioning, active or suspended can be archived by Delete; an already-archived tenant answers 409. Coming back from archived needs a database edit or a later ruling. The admin Delete keeps working."*
    - Option (b): *"Same as (a), plus the status route allows archived to suspended, so 'reversible' holds through the API. Archived to active stays refused, as you ruled. One extra allowed change and one test."*
  - Earlier rulings that still bind:
    - Kam 31 Oct 11:33, KS-1861 "Archive, not erase" (option a, "keeps every row");
    - KS-1860 refuses archived -> active;
    - Wednesday's 31 Oct ANSWER: **no DROP DATABASE anywhere**, under any flag.
  - card `secuura-ks1860-status-refresh-fails-at-startup-1101` = **a**, *"Keep it as built and say so"*. This PR carries the docs statement for it.
- **Previous gate on this service:** `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate64-ks1860-1876/verdict.md` (KS-1860 PR 3, GO WITH NOTES). Read it whole. It is also the **output shape** to follow. Its notes G64-F1..F4 are context: F1 is the start-up behaviour, now ruled; F2 is the Schemathesis isolation fixture, now KS 1914.

## Required work (Q-sections in the verdict)
**Q1. The transition matrix, exhaustively.** For every (from, to) pair over {provisioning, active, suspended, archived}, on BOTH the Delete route and the status route:
- what the code allows, against what the rulings allow;
- the response code and body;
- what is written to the database and to `platform_audit_log`.
Build it from the code at the head (give file:line), then prove each cell with a test of your own or the author's. Any cell where code and ruling disagree is a finding.

**Q2. "Keeps every row" / no erase / no DROP.** Show that Delete, on every path including error paths and with every relevant flag (PROVISION_PER_TENANT_DB, MULTI_TENANCY_ENABLED) true and false:
- drops no database;
- deletes no row in any table;
- erases no vault entry;
- revokes nothing irreversibly.

Search the whole delta and the code it calls for DROP, DELETE FROM, TRUNCATE, `.destroy`, `.delete(` and vault erase calls. A grep is a selector: read every hit.

**Q3. Reversal through the API.** Archived -> suspended -> active must restore a working tenant. Does anything Delete did (key revocation, pool eviction, cache, connector state, audit) stop the tenant working again after the reversal? A one-way side effect hidden behind a reversible status is a finding.

**Q4. Concurrency and idempotency.** Two Deletes at once; Delete racing a status change; Delete of an already-archived tenant (must be 409 with no write). Is the status change atomic with its audit row (the transaction)?

**Q5. Authorisation.** Who may call Delete and the status route at the head? Did the delta widen either? Compare with develop.

**Q6. The author's evidence, re-run.**
- 30/30 green and 10/30 red at develop (with develop's index.ts);
- the 16 mutants: re-run at least DM2 (DROP under the flag), TB1 (Kam's (b) removed), TB2 (archived -> active admitted) and one SS mutant, and confirm each dies;
- the whole tenant-provisioning suite (84/84);
- check:openapi with a planted control.

Then write at least 3 mutants of your own on the riskiest lines and report killed/survived.

**Q7. The docs.**
- Read `docs/MULTI-TENANCY.md` at the head against the code and against Kam's rulings: Status Transitions, Deleting a Client, the route tables, Suspending a Tenant, the start-up paragraph.
- Every statement that is false at the head is a finding.
- Check that the start-up paragraph states Kam's KS-1860 (a) faithfully: serve while unknown, flag-on only, not a regression.

**Q8. Merge and overlap.**
- `merge-tree --write-tree <develop> 48d05f02` (the author reports rc 0, tree 91c50fde98d4).
- The yaml excusal: PR 4 shares `docs/openapi/secuura-api.yaml` with open #1874 and #1884. Re-run the merge-trees of each against develop alone and against develop + PR 4, and confirm 0 yaml conflicts.

**Q9. NOT covered by the author** (their list: the platform suites, a real Postgres, the admin portal (KS 1912/1913), the Schemathesis fixture (KS 1914), erasure). For each, say whether it is a merge blocker, a note, or out of scope, and why. **Real Postgres matters here:** the author's cells use a fake platform database. If you can, run the Delete and status paths against a throwaway real Postgres (your own container **gate71-pg**) with the repo's migrations, and report it.

## SPARK first
- Run `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/gate/spark_gate.sh` on the two new test files: base `develop`, `--work /private/tmp/gate71_spark_work`.
- **Build `@secuura/shared` before the run.** Gates 68 and 69 lost a run to an unbuilt shared package.
- Then run `spark_review.py` on the delta, and give a calibration table as gate 64 / gate 68 did.

## HOW
- **Clone:** `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate71-ks1861-1885/repo`, made with `git clone --shared --no-checkout` from `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate65-r1r3-1868/repo`.
  - Push URL `no_push_qa_gate`; refs fetched into `refs/gate/*`.
  - Assert `git rev-parse --show-toplevel` equals the clone directory before every fetch or write.
  - The hook refuses `cd`: use `git -C <abs>`. If it refuses a write verb on a variable path, use `bash <<'EOF'` with literal paths.
- **Install:** `npm ci --ignore-scripts`, then the `@secuura/shared` build and the Prisma generate. Record each rc.
- **Load:** this Mac also runs three seats plus gate 70. Copy `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate68-ks1384-r2a-1874/scripts/jest_run.sh` (nice 10; waits while load1 > 8). No unbounded parallel tests.
- **DB:** if used, your own container **gate71-pg** (loopback, random port, passwords from `openssl rand` into a 0600 scratch file, scrubbed from logs). Stop it at the end. Never touch gate65-pg, gate68-pg, gate70-pg or s-w13-pg.
- No secrets in any file. `git status` in your clone is empty at the end. Never discard stderr.

## OUTPUT
- Write `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate71-ks1861-1885/verdict.md` (scripts in `scripts/`, evidence in `evidence/`).
- Shape, as gate 64:
  - Title;
  - **BLUF** with **GO / GO WITH NOTES / NO GO**;
  - Heads at START and END;
  - FINDINGS `G71-Fn · SEVERITY · area`, each with file:line and a red-before;
  - Q1–Q9 (Q1 as a table);
  - SPARK;
  - **NOT TESTED**;
  - HOW.
- Every number is pasted from a log you name.
- Your final message to Wednesday is ONLY: the verdict, the finding ids with severity, and the verdict.md path.
