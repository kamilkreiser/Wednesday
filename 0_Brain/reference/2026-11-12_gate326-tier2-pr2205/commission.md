# Gate 326, TIER 2 (Sonnet; routing v1.0 tier-2 row: tooling + config + lockfiles, no service src change). Seat T 24th's lane L1 of KS-1398 step one = child KS-2176 = PR 2205. Commissioned 2026-11-12 ~12:3x AEDT by the 12:3x Wednesday seat.

Method: copy-and-change of `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate320-tier2-pr2196/commission.md`. Read it whole: its Constraints, output shape and controls all apply. Calibration: gate 320's, 322's and 324's verdict.md.

Pins (Wednesday's `git ls-remote origin` 12:35:34 AEDT; RE-READ at start and end, and say if either moved): develop 1247e1af3c203d369d01b4d574de377adeec4b98; refs/pull/2205/head 06fbdf9906d0d6f5726f987a51ed8627507f05bc. The branch was cut on 088fa84da10c; develop moved by one commit (PR 2202's squash, shell test files only). Merge-tree onto 1247e1af3c20 with each side's own merge-base (never `git merge-file` with a hand-chosen base: ledger 2026-11-12).

READY (read whole; reproduce, do not trust): `ready_t24_ks2176_mail.txt` in THIS folder. Lane design: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_ts7-step1-lanes/` (lanes.md, lane L1).

What the row claims (from the READY, unverified by Wednesday): dead ts-jest removed from referral and vc-issuer; ts-node -> tsx in five packages; 19 files, +2337 -8495 (mostly lockfiles); vitest referral 142/142, vc-issuer 842/842, staking 99/99 equal before and after; tsc builds rc 0 in 4 packages; root lock changes exactly one named key (node_modules/tsx gains resolved + integrity, version unchanged); four standalone locks change 0 kept keys.

Wednesday's TIER NOTE, which this gate must test, not assume: the seat reads tier 2 and asks whether the six cardano scripts move it. **The cardano scripts have NO tsconfig, so ts-node -> tsx removes their ONLY type signal** (the seat's own run: faucet.ts TS18046 surfaced only under ts-node). That is a real loss of checking, not a form change. Grade it: is any of the six scripts' type error a real defect now hidden? Should the PR carry a tsc --noEmit leg (or a tsconfig) for them, or is it a filing?

Questions:
1. Removal is safe: for referral and vc-issuer, no remaining import, config, script or CI reference to ts-jest/jest config (search the whole package and the root, with a positive control that finds a known ts-jest reference at develop).
2. Runtime equivalence: for each of the five packages, the dev/start entry boots under tsx to the same first log line as under ts-node at develop (reproduce one yourself, independent of the seat's), and a planted syntax error exits non-zero.
3. Locks: reproduce the root-lock claim (exactly one key changed, by a structured diff of the two JSON locks, not a text diff); `npm ci --dry-run` rc 0 on each changed lock; npm ls shows the removed names absent and tsx present.
4. Tests: re-run referral and vc-issuer vitest at the head (counts); one planted failing assertion turns each red.
5. The cardano tier note above: run `tsc --noEmit` over the six scripts at develop and at the head with a scratch tsconfig and list every diagnostic; say whether any is a real bug.
6. Leftovers: the seat names services/billing/scripts/setup-products.ts (ts-node shebang), services/api-gateway/src/startup-migrations.ts and systemTest/akto/bin/run.ts (ts-node mentions). Read each; with ts-node removed from which packages, does any of them now break? Then census the WHOLE tree at the head for remaining `ts-node` references (a search with a positive control) and classify each: broken by this PR / unaffected / later lane.
7. Census: open PRs touching the 19 paths (GraphQL or ls-remote + diff, with a control). PR 2099: the seat reports merge-tree rc 0 with 2099's head 8967de8b1755 and 4/4 + 11/11 entry survival; reproduce the merge-tree.
8. docs-fragments check passes; a planted defect exits 1.

Spark shadow after your verdict: run `2_Project_Files/local-model/gate/spark_gate.sh` / `spark_review.py` with `--pr-body-file`, in the session scratchpad (Spark tunnel UP at 12:3x; one request at a time). Record recall/false positives against your findings.

OUTPUT: `verdict.md` in THIS folder. First line: 'PR 2205: GO / GO WITH NOTES / NO GO (at head 06fbdf9906d0; tier 2)'. Findings G326-2205-N, graded. NOT TESTED. The Spark shadow result. If your Write is refused, return the text in full.

Constraints: exactly gate 320's. Read-only on the project checkout (clone into your scratchpad for any write verb; install only in the scratch clone, `--ignore-scripts`). No push, no comment, no ticket write, no merge. DevMASTER has dropped several times on earlier days (enclosure power). If it drops, wait, re-read what you wrote, then resume.
