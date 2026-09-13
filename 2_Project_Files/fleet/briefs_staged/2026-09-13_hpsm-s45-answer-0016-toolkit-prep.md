BLUF. **Your M16 finding is the most important measurement of the night.** A rollback to `9b8ea76` after `0016` is an outage: base's migrator refuses the database (`9b8ea76:packages/db/src/migrate.ts` L53-58, your citation), api and worker stay down with 502, and the toolkit as written would trigger that outage itself. Thank you for measuring it BEFORE the head mail.
- **Approved now, as PREPARATION ONLY (local, nothing live):** your a), b), c) and d), with ONE refinement below.
- **The LIVE feedback upgrade is NOT ruled yet.** Tuesday rules it at the formal head mail (after step 10 GREEN), with the pre-check output, the pin answer and the d) proof in hand. **Nothing deploys before that ruling.**

## Approved preparation
- **a) A seat-written S45 copy of the toolkit, plus the REFINEMENT.** Before any redeploy, rollback() reads `pc_meta.schema_migrations`:
  - **0016 NOT recorded** (the failure came before migrate): roll back to `9b8ea76` as today.
  - **0016 recorded, and the DEPLOY step itself failed** (redeploy rc, no DEPLOYED line, migrate or PREFLIGHT failure, healthz down): **roll FORWARD once** to the target (R1). If that also fails, STOP, leave the stack as is, and mail Tuesday at once.
  - **0016 recorded, the deploy SUCCEEDED, and only a post-deploy CHECK failed** (the tunnel dropped, smoke, post-check A/B, the public browser check, the public gate probes, B's PDF markers, the Caddy fingerprint): **redeploy NOTHING. STOP and mail Tuesday** with the failing check, leaving the site as it is.
  - **Why the refinement:** a dropped tunnel or a flaky probe must never restart Kam's demo. On Azure you listed 9 checks at `run-azure.sh:47-78`, and only the deploy failures are grounds to touch the stack.
- **b)** Add `Error|not in the migrations` to the migrate log filter (`deploy-lane-a.sh:37`), with your positive control (the refusal line matches; the upgrade log still matches its 3).
- **c)** `EXPECT_MIGRATIONS` = 16 from the next base on (`lib-target-checks.sh:8`), and the "migrations changed since base" STOP compares against the NEW base.
- **d) Positive-control all three branches on a LOCAL stack before any live use:**
  - (i) force a failure BEFORE migrate: base rollback taken;
  - (ii) force a DEPLOY failure after 0016 applies: roll-forward taken, and it recovers;
  - (iii) force a CHECK failure after a good deploy: no redeploy, STOP plus mail.
  Put the three transcripts in the head mail.
- **e) R2 (reverse SQL) is Kam's word only.** It deletes whatever feedback exists. Keep the script out of the repo, as it is.

## For the head mail (so Tuesday can rule in one read)
1. The pre-check STOP lines verbatim; the pin answer in one line (0016 adds only new tables; say whether any content or capability pin moves).
2. The d) proof, all three branches.
3. **The order:** pc-lane-a FIRST, and Azure only after lane-a's full post-check is GREEN. **Name what Kam will notice,** and **say what feedback rows exist on live at that moment** (expected: none), so R2's cost is known.
4. **One line:** "after this upgrade, the rollback target is the NEW head (roll forward), not 9b8ea76."

## Unchanged
- Step 9 re-chain `m10b-s45` on `cfd3cc6` (G9 tests only), fast-forward on GREEN; then step 10.
- CR running with W4B-m3; its start-time correction (~13:15Z) is noted.
- Your free agent slots are yours to use under the partition rules (Kam's 09:17 standing rule).
- No push. C11 STOPs for Kam. Mail `tuesday-agent@` only.
