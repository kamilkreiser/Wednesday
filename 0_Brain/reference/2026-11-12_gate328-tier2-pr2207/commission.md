# Gate 328, TIER 2 (Sonnet; routing v1.0 tier-2 row: config only — ten tsconfig.json files + a docs fragment pair; no source, no lockfile). Seat A 26th's lane L5 of KS-1398 step one = child KS-2177 = PR 2207. Commissioned 2026-11-12 ~13:2x AEDT by the 12:3x Wednesday seat.

Method: copy-and-change of `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate326-tier2-pr2205/commission.md` (the sibling L1 lane's gate; read it and its verdict.md whole: same project step, same shapes) and, through it, gate 320's commission (Constraints, output shape and controls). Lane design: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_ts7-step1-lanes/` (lanes.md, lane L5; the seat reports its "node16/bundler" text is wrong for commonjs).

Pins (Wednesday's `git ls-remote origin` 13:25:49 AEDT; RE-READ at start and end, and say if either moved): develop 1247e1af3c203d369d01b4d574de377adeec4b98; refs/pull/2207/head 0d82e65bc5be13443e83b6ccc7d1e2149f823242. Merge-tree onto develop with each side's own merge-base (never `git merge-file` with a hand-chosen base).

READY (read whole; reproduce, do not trust): `ready_a26_ks2177_mail.txt` in THIS folder.

What the row claims (from the READY, unverified by Wednesday): ten tsconfig.json files drop `moduleResolution: node` (five files) and `baseUrl` (five files, `paths` values gain `./`); under TypeScript 5.9.3 tsc --noEmit + sorted --listFiles equal 9/9 packages; six emitted trees byte-equal 638/638; three frontends' dist byte-equal 90/90 (vite deterministic by a two-run control); check:test-types ratchet unchanged in five services; NO `types` array added.

Questions:
1. **Equivalence under the shipping compiler (TS 5.9.3):** for each of the ten files, reproduce tsc --noEmit rc and the sorted --listFiles before/after (your own run), and at least two emitted trees and one frontend dist byte-equal before/after, with a planted control that DOES change the output (e.g. a changed `target` in a scratch copy).
2. **Resolution semantics:** with `moduleResolution` removed under `module: commonjs`, what does TS 5.9.3 default to, and can any import in those five packages resolve differently (package.json `exports`, deep imports, `.js` extension imports)? Name the rule you read (TS docs or `tsc --showConfig` before/after) and test one deep import per package if any exist.
3. **baseUrl removal:** for the five `paths` files, does every `paths` target resolve identically without `baseUrl` (`tsc --traceResolution` on one aliased import per package)? services/vc-issuer's tsconfig.test.json extends the edited file: check it too. mobile/secuura-app (Expo base, Metro uses `paths`): the seat did NOT measure it; read whether Metro/Babel resolve aliases from tsconfig `paths` without `baseUrl` (read only; say UNMEASURED if you cannot run it).
4. **TS 7 claim (measurement, not a gate):** the seat says 8 of 9 main configs go rc 0 on TS 7.0.2 and billing reads TS6059. Reproduce billing's TS6059 in a scratch install only; do not grade the PR on TS 7.
5. Ratchet: `check:test-types` before/after in the five services, with a planted type error in a scratch copy turning it red.
6. Census: open PRs touching the 12 paths (with a control); the seat reports none.
7. docs-fragments check passes; a planted defect exits 1. PR body: no closing word; Refs only.

Spark: the test-digest STANDARD (`2_Project_Files/local-model/digest/digest.py`) on any long build/test log you produce, raw logs kept; then the Spark shadow review (`2_Project_Files/local-model/gate/spark_gate.sh` / `spark_review.py` with `--pr-body-file`), one request at a time. Record recall/false positives against your findings.

OUTPUT: `verdict.md` in THIS folder. First line: 'PR 2207: GO / GO WITH NOTES / NO GO (at head 0d82e65bc5be; tier 2)'. Findings G328-2207-N, graded. NOT TESTED. The Spark result. If your Write is refused, return the text in full.

Constraints: exactly gate 320's. Read-only on the project checkout (clone into `scratch/` in THIS folder for any write verb; installs only there, `--ignore-scripts`). **Every npm/npx/vitest/tsc invocation names its directory explicitly (`--prefix <abs>` / `--root <abs>` / `-p <abs tsconfig>`) and never runs from the WEDNESDAY working directory: gate 327 left a stray vitest cache at the WEDNESDAY root this way (quarantined at 13:26).** No push, no comment, no ticket write, no merge, no mail. If DevMASTER drops, wait, re-read what you wrote, then resume.
