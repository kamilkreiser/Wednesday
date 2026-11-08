# Gate 259, tier 1, ROUND 2 OF 2: PR 2052, KS-1081 (production config refuses published template values; demo-service out of the production overlay). Launched 2026-11-08 by the 21:2x Wednesday seat

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole first. Corrections: develop cfb6c1573ba9c948ebbe898fb2aec283bb9954ab by Wednesday's ls-remote at 22:2x AEDT (re-read at start and end; B 98th is merging tonight); QA no-rm (leave your clone at /private/tmp/g259, name its size); one clone; stop under 12 GiB free; load1 under 8 (two other gates run beside you); never cd; if a hook refuses merge-tree, use a clone under the session scratchpad and say so. No box, no docker daemon start: the docker half is NOT RUN unless Docker is already up, and you say which.

Head b61674e7b7635a50d51f837849cb9caf1259235d (Wednesday's ls-remote, equal to the READY). 5 commits, 32 files.
READY: J 21st's mail of 11:25Z (body in its seat folder /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-08_seatJ-21st/; find the ready file and STATUS_ks1081_option_a.md). Round 1: gate 233 NO GO, /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-06_gate233-tier2-pr2052-ks1081/verdict.md, F1 to F10. Kam's card secuura-ks1081-template-flips-secrets-production-path-1106 = a (decision_queue.sh show).

Cap round: a further NO GO ships what is closed and tickets the rest; say per finding whether it blocks.
1. Each of gate 233's F1 to F10 closed, by your own read and run.
2. The production guard: under NODE_ENV=production, does every one of the eight PUBLISHED_TEMPLATE_VALUES get refused at boot by every service that consumes it, and does NO real, non-template value get refused? Plant a value of your own.
3. demo-service: out of the production overlay by profile; if the profile is enabled, its own guard refuses the published key. Can anything in the production path start it without the profile? nginx-gateway depends_on required:false: does nginx still start and serve when demo-service is absent?
4. The docs (env.example, DEPLOYMENT.md, the checklist, both fragments): every sentence true of the code.
5. The 36 mutants / 39 tamper rows: reproduce a sample and plant one defect of your own.
6. Merge tree on develop; open PRs sharing a path (2074, 2070 by J's census).

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-08_gate259-tier1-pr2052-r2/verdict.md, per the common rules. Findings only; post nothing.
