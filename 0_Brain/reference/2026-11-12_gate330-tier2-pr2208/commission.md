# Gate 330, TIER 2 (Sonnet; routing v1.0 tier-2 row: build config + a standalone lock + emitted declarations for one package, no product source). Seat A 27th's lane L7 of KS-1398 step one = child KS-2179 = PR 2208. Commissioned 2026-11-12 ~14:53 AEDT by the 14:49 Wednesday seat.

Method: copy-and-change of `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate328-tier2-pr2207/commission.md` (the sibling L5 lane's gate; read it and its verdict.md whole: same project step) and, through it, gate 326's and gate 320's commissions (Constraints, output shape, controls). Lane design: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_ts7-step1-lanes/lanes.md` (lane L7). The seat's stamped brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/` file named `*seatA27*` (read its grants: emitter = tsup 9 for JS + tsc for declarations; LOCK D = tsup ^9, the eslint devDependency and the dead lint script REMOVED by Wednesday's grant 03:12Z (restoring lint is a filing, not a defect of this PR); `dev` loses --dts; KS-2136 test-script fix folded in with Refs KS-2136).

Pins (Wednesday's `git ls-remote origin` 14:52:41 AEDT; RE-READ at start and end, and say if either moved): develop 581296f039b4890ccf6f56e1c1f13575dc1098d4; refs/pull/2208/head 44457d12eaa1fa51223bee28526db5a05b058342. The PR is cut on b7137aa97c79; develop moved one commit (PR 2205's squash, KS-2176, 19 files). Merge-tree onto develop with each side's own merge-base (never `git merge-file` with a hand-chosen base).

READY (read whole; reproduce, do not trust): `ready_a27_ks2179_mail.txt` in THIS folder.

What the row claims (from the READY, unverified by Wednesday): sdk/javascript gets a tsconfig, a standalone lock and tsc-written declarations; 5 files, +3131 -7 (most of it the lock). `npm run build` rc 1 before, rc 0 after, 9 files in dist; index.js and index.mjs BYTE-EQUAL to before (so no published JS change); 7 d.ts files; 10 of 10 public names; consumer check rc 0 under node16-CJS, node16-ESM and bundler; `npm test` rc 0; `npm run audit:locks` rc 0 and `audit:gate` rc 0; TS 7.0.2 scratch build byte-equal (measurement only).

Questions:
1. **JS byte-equal (the central claim):** reproduce the before (develop / PR base) and after builds of sdk/javascript yourself, compare index.js and index.mjs by sha256, with a planted control that DOES change the output in a scratch copy. If "before" cannot build (the seat says rc 1), say how the before artefact was obtained and whether the comparison is sound.
2. **Declarations:** the 7 d.ts files: do they declare every name the JS exports (and no more), and does a consumer type-check under node16-CJS, node16-ESM and bundler (reproduce at least two, with a planted break that goes red)? Do package.json `types`/`exports` point at files that exist in dist?
3. **Lock D:** the new standalone lock: `npm ci --ignore-scripts` in a scratch clone rc 0; tsup ^9 resolved; eslint gone; `npm run audit:locks` rc 0 reproduced, and the sdk lock is actually among the scanned set (a control that would show it scanned).
4. **Scope:** the lint script/devDependency removal and `dev` without --dts are as granted; KS-2136's test-script fix is present and named with Refs only. PR body: no closing word; Refs only. Is anything outside sdk/javascript + the docs fragment pair changed?
5. **Develop move:** merge-tree onto 581296f039b4 clean; overlap with PR 2205's 19 paths = 0 (reproduce). Census: open PRs touching the 5 paths (with a control); the seat reports none.
6. docs-fragments check passes; a planted defect exits 1.
7. TS 7 claim: measurement only, do not grade.

Spark: the test-digest STANDARD (`2_Project_Files/local-model/digest/digest.py`) on any long build/test log you produce, raw logs kept; then the Spark shadow review (`2_Project_Files/local-model/gate/spark_gate.sh` / `spark_review.py` with `--pr-body-file`), one request at a time. Record recall / false positives against your findings. If the Spark is busy or down, say so and continue.

OUTPUT: `verdict.md` in THIS folder. First line: 'PR 2208: GO / GO WITH NOTES / NO GO (at head 44457d12eaa1; tier 2)'. Findings G330-2208-N, graded. NOT TESTED. The Spark result. If your Write is refused, return the text in full.

Constraints: exactly gate 320's (via 328). Read-only on the project checkout (clone into `scratch/` in THIS folder for any write verb; installs only there, `--ignore-scripts`). Every npm/npx/vitest/tsc invocation names its directory explicitly (`--prefix <abs>` / `-p <abs tsconfig>`) and never runs from the WEDNESDAY working directory. No push, no comment, no ticket write, no merge, no mail. Never `cd` (use absolute paths / `-C`). If DevMASTER drops, wait, re-read what you wrote, then resume.
