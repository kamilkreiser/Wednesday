# Gate 305, TIER 2 (Sonnet): R 94th round 1 batch: PR 2163 (KS-1145 item 2), PR 2164 (KS-2098), PR 2165 (KS-2095). ONE session, three verdicts. Commissioned 2026-11-10 ~16:2x AEDT by the 15:46 Wednesday seat (batched under Kam's 2026-09-18 minimise-gate-duplication rule; all three are raised held Spark passes, file-disjoint by the seat's READY: prove it).

Common rules: the tier-2 shape of /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate289-tier2-pr2133-pr2134/commission.md (read whole; its common-rules pointer applies) at tier-2 depth.

Pins (Wednesday's ls-remote at 16:22:46 AEDT; RE-READ at start and end, say whether each moved):
- develop b602c418296a3191d9efba5511d6c0ffda4e3212 (PR 2122 squash; all three PRs were built on 0e6479d7b6c0: read what develop's one-commit move changed and whether it touches any PR's paths)
- PR 2163 head 8f0048de07fa6ea20d9242a24b710b73dfe00b9b (KS-1145 item 2 only: one bash test file, +12 -1, by the READY)
- PR 2164 head f03f4e72a8b7725f5dac5b7254e13b67cb2deb6b (KS-2098: one bash test file under systemTest/, +4 -0, by the READY)
- PR 2165 head f11dc645401aca105aeb2fc1f7b94bbf9f48e4e5 (KS-2095: TWO files, +35 -0: ONE PRODUCT file BlockchainCard.tsx +3 in the issuer frontend, one vitest file +32, by the READY)

READY (read whole; reproduce, do not trust): /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-10_seatR-94th/mail/ready_round1.md. Wednesday's rulings to this seat (read whole): /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-10_R94_answer_plan.md, _R94_answer_second_tree.md, _R94_addendum_o132.md, and the stamped brief 2026-11-10_seatR94_raise.md (RULED sections). The held Spark READY files behind the PRs are in /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/ (READY_KS-1145-*, READY_KS-2098-*, READY_KS-2095-*): compare each PR's diff with its held diff, per file (git sorts files), and name any difference.

Questions (each PR):
1. File set: 2163 and 2164 test-only, no product byte; 2165 exactly one product file + one test file. Prove by the PR files API and a diff read.
2. Red proof: the new cells fail on a plant and pass on develop as the seat says. Your own mutant per PR reddens a NAMED cell. Are the cells PINS and labelled honestly? For 2165: product reverted with the test kept reddens R1-R3 (the seat's claim: 3 failed); re-run it.
3. Do the cells (and for 2165, the +3 product lines) do what the ticket's scope sentence asks (read KS-1145, KS-2098, KS-2095 at Linear read-only), and does each PR body claim no more than the change? KS-1145 item 1 is NOT in PR 2163.
4. PR 2165 changes a RENDERED condition (the issuer Block card leaves out the block row when there is no height). Read the component; say what a user sees in each case. If you can render it locally in your OWN scratch (a component test render counts; a browser render is better), do; otherwise list the render as NOT TESTED.
5. Whole suites: the issuer suite (vitest) for 2165; the bash suites the two test PRs touch; counts before and after. Whole-suite legs only when load1 < 8 (a long drive copy is running on this machine; say if you could not).
6. Merge trees onto today's develop, each alone and all together; any open PR sharing a path (planted control).
7. No closing word in closing form in title, body, commit or comments.
8. The seat's PRETTIER FLAG (warns on touched AND untouched files): report whether it distinguishes this change; do not rule.

SPARK SHADOW (rule 2026-10-26: every tier-2 Claude gate gets a Spark shadow): after your own verdicts are written, run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/gate/spark_gate.sh on each PR exactly as /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-shadow-pr2127/commission.md did (read it whole; check the tunnel is UP with python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/spark_status.py first), and append a calibration row per PR to this folder's calibration.md: the Spark's verdict and findings vs yours, recall, false positives checked at source. If the tunnel is DOWN or the script refuses, say so with its exit code and output; never skip silently.

Constraints: never cd. In /Volumes/DevMASTER/!CODING/ only ls-remote, show, log, diff, ls-tree, cat-file, grep; never fetch, push, post, comment or mail there; tests and mutants in your OWN scratch clone (clone from the project remote into your scratch, or reuse a scratch clone under /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/ that the spark-shadow commission names). No rm outside your scratch. Never print a real secret or any .env value.

Verdict path: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-10_gate305-tier2-pr2163-2165/verdict.md. Line 1 per PR exactly: 'PR <n>: <GO | GO WITH NOTES | NO GO>'. Then FOUND / TESTED / HOW, NOT TESTED, findings G305-<pr>-<n> with severities. Return the whole verdict in your final message as well.
