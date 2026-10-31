# QA GATE 70 — TIER 1, MONEY PATH — Secuura/Blockchain KS-1384 R2b, PR 1884

Commissioned by Wednesday (Kam's coordinator agent) on Sun 1 Nov 2026. You are an **independent QA gate**. **FINDINGS ONLY.**
- You fix nothing, push nothing, comment nothing, approve nothing and merge nothing.
- Nothing is written to GitHub, Linear, or anywhere under `/Volumes/DevMASTER/!CODING`.
- Client scope: **Secuura only**. Never read or write any Datasec path or mail.

## Target (copied from the author's READY mail, `evidence/ready_mail_r2b_2231Z.txt`; read it WHOLE first)
- **PR:** 1884, Secuura/Distributed_Secuura, base develop.
- **Head:** `ecfe4f07fdcec78b8d45d897bd4dccd4be829be7`. Assert it equals `refs/pull/1884/head` before you start, and again before you write the verdict. If it moved, STOP and say so in the verdict.
- **Gate delta:** `31d1466788bea96f6175b595c8fb3078229668be...ecfe4f07fdcec78b8d45d897bd4dccd4be829be7`. The author reports 52 files, +3432/-589. Measure it yourself.
  - R2b has **never been gated**, so the WHOLE delta is in scope.
  - It is stacked on R2a's gated head `31d146678` (PR 1874, gate 68 = GO WITH NOTES) and contains R2a's local merge-prep commit `b86dcf7f5`. Verify that it is an ancestor.
- **Previous gates to read before designing cells:**
  - `0_Brain/reference/2026-11-01_gate68-ks1384-r2a-1874/verdict.md`, whole. It is also the **output shape** to follow.
  - `0_Brain/reference/2026-11-01_gate65-r1r3-1868/` (verdict + evidence/probe/).

## Required work (Q-sections in the verdict, in this order)
**Q1. Re-run BOTH probe files, UNCHANGED, at the head.**
- Gate 65's: `0_Brain/reference/2026-11-01_gate65-r1r3-1868/evidence/probe/gate65-r1r3-probe.integration.test.ts`, sha256 `3be022f874a62e61…`.
- Gate 68's: `0_Brain/reference/2026-11-01_gate68-ks1384-r2a-1874/evidence/probe/gate68-r2a-probe.integration.test.ts`, sha256 `ec9401c1d09dda6f…`.
- State the sha256 you ran. The author's copies in `evidence/r2b/probes/` each add one own-create line. Run the ORIGINALS. If an original cannot run at this head without that line, run the author's copy too, diff the two, and say exactly what the added line changes.
- The author reports 47/50, with three reds. Reproduce each and explain it at source:
  - **Q2b-past** (round 3's residual 2);
  - **R2-f3** (the author says its fake keeps the old 404 on purpose; verify that claim);
  - **H-diff-repeat** (= G68-F3 / KS-1919).
- A red the author did not predict is a finding.

**Q2. G65-F1, the narrower restore.** Is R2b's restore the narrower one gate 65 asked for? Is it correct on every path that reaches it? Give file:line.

**Q3. G68-F1: the network comparison was dropped.**
- Cells: **L3, f2g (inverted), n1, n2.**
- Establish whether a landed anchor can be paid for twice when originate's and anchoring's `CARDANO_NETWORK` differ, at this head.
- State whether the train's DEPLOY HOLD (both services' `CARDANO_NETWORK` must be equal on each box) is still required, and why.

**Q4. G68-F2: real-shaped rows.** Do the fakes now return rows shaped like real anchoring's rows? Re-run the money cells with real-shaped rows of your own as well.

**Q5. D3 as written + KS-1918.**
- Does D3 behave as its text says?
- Confirm and bound the known limit that a verify without a bearer shows the stored state (KS-1918). Is it a money risk or a disclosure risk? Is either new in this delta?

**Q6. FEE COUNTS: R2a head `31d146678` vs R2b head `ecfe4f07`, in EVERY money cell.** Count the POSTs on arrival, exactly as gate 68's Q6 table did.
- **No cell may pay more at the head.** Any cell that does is a NO GO finding unless you prove it is an instrument artefact.
- For the base runs, swap the product files to `31d146678` and restore them, with a sha256 check, as gate 68 did.

**Q7. threadTokenMint's emulator round-trip.** It is red at R2a, at gate 68 and here. Is it host-dependent (prove or disprove), and does anything in this delta touch it?

**Q8. R2b's own claims**, which gate 68 did not test (the R1-wedge fix, part 4). Test each claim in the PR body's Test Evidence against the code, not against the prose.

**Q9. Merge onto develop `77fac4727758`:** report merge-tree's result. The author expects rc 1 on 3 train-own files (fb-sweep, anchoring index.ts, ks1293). Say whether any conflict falls inside this delta's hunks.

Plus your own adversarial cells and mutants on the money path. **Ask what would make each check fail**, and record a red-before for every new cell.

## SPARK first (run it, then calibrate it, as gate 68 did)
- Script: `2_Project_Files/local-model/gate/spark_gate.sh`, base `develop`, `--work` under `/private/tmp/gate70_spark_work`.
- **Build `@secuura/shared` BEFORE the spark run.** Gate 68's run 1 and gate 69 (N3) both lost a run to an unbuilt shared package.
- Then run `spark_review.py` on the delta, and give a calibration table: Spark finding | Gate 70 | true/partial/noise/missed.

## HOW (mirror gate 68's HOW section; deviations are stated)
- **Clone:** `0_Brain/reference/2026-11-01_gate70-ks1384-r2b-1884/repo`, made with `git clone --shared --no-checkout` from `0_Brain/reference/2026-11-01_gate65-r1r3-1868/repo`.
  - Push URL `no_push_qa_gate`; refs fetched into `refs/gate/*`.
  - Assert `git rev-parse --show-toplevel` equals the clone directory before every fetch or write.
  - `repo/` is gitignored; keep it that way.
- **Install:** `npm ci --ignore-scripts`, then the `@secuura/shared` build and the Prisma generate. Record each rc.
- **DB:** your own container **gate70-pg** (postgres:15-alpine, loopback, random port).
  - Migrations come from the repo's scripts.
  - Passwords are generated with `openssl rand` into a 0600 scratch file and scrubbed from every log.
  - Cells run as `secuura_app` with RLS on; the superuser is used for seeding only.
  - **Stop the container at the end.**
  - Do not touch gate65-pg or gate68-pg.
- **Load:** copy gate 68's `scripts/jest_run.sh` (nice 10, waits while load1 > 8). This machine also runs three live seats; never run unbounded parallel jest.
- **Probe placement:** copy probes into `src/__tests__` only for the runs, then move them out to a scratch quarantine. `git status` in your clone must be empty at the end.
- **Node:** record the version (gate 68 ran on v26.8.1, not LTS).
- **Secrets:** none in any file you write.

## OUTPUT
- Write `0_Brain/reference/2026-11-01_gate70-ks1384-r2b-1884/verdict.md`, with scripts in `scripts/` and evidence in `evidence/`.
- Shape, as gate 68:
  - Title line;
  - **BLUF** with the verdict **GO / GO WITH NOTES / NO GO** and the money-cell headline;
  - "What is not clean";
  - Merge onto develop;
  - Heads (each read in the same action);
  - VERDICT;
  - FINDINGS `G70-Fn · SEVERITY · area`, each with file:line and a red-before;
  - Q1–Q9;
  - SPARK;
  - **NOT TESTED** (be exhaustive and plain);
  - HOW.
- Every number in the verdict is pasted from a log you name, never retyped.
- Your final message to Wednesday is a short summary of the verdict file's BLUF and its path. Nothing else.
