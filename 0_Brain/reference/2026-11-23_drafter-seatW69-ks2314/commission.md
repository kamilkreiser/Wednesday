# COMMISSION: draft the brief for Seat W 69th (Secuura/Blockchain-W), KS-2314, design-first build on Opus

Commissioned by Wednesday (the 13:11 rotation's successor seat), 2026-11-23. You are a DRAFTER: you READ and WRITE ONE FILE. You launch nothing, mail nobody, write nothing to Linear, GitHub or any project folder.

## OUTPUT (the only file you write)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-23_seatW69_ks2314_design.md`
Then reply with: the path, its line count, and a list of every fact in it with the command or file you read it from. Say plainly anything you could not measure.

## THE SHAPE TO COPY
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-23_seatW68_ks2294_design.md` (read WHOLE). Same sections, same standing lines (no cd; credentials read inside a python script, never argv; GIT_OPTIONAL_LOCKS=0 on shared-checkout git reads; the launcher's boot ls-remote is Kam's ruled line; shared inbox warning; MEASURE FIRST then ONE plan QUESTION then WAIT; red-first + mutants; ONE commit ONE push; READY FOR GATE tier 1). Change only what this ticket needs. Every timestamp you write comes from `date` in a command, never typed.

## THE TICKET AND THE RULING
- Ticket: KS-2314 on the Secuura Linear board (read-only: source `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env` INSIDE a python script for the Linear key; never print it; GraphQL, key in Authorization header without Bearer; read the description and ALL comments with `comments(first:50)` sorted client-side). Quote its scope sentence verbatim in the brief.
- Kam's ruling (verbatim, from `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-platform-config-who-may-write-ks2314-1122`): "Decision secuura-platform-config-who-may-write-ks2314-1122: a — Platform admins only, for all five (recommended)", ruled 2026-11-23 10:13:07 +11:00. Option detail a and the card's default are the spec: platform settings (including each connector's allowed document types), document types, workflows, integrations and verification policies become platform-admin-only writes in the gateway AND originate's copies; organisation and issuer admins get a refusal; the Settings page stops saving for them. Put it under RULED BY KAM, NOT YET IN AN ARTEFACT.
- Platform-admin check: Kam's KS-1701 ruling (card secuura-platform-role-spellings-ks1701-1123 = a: every platform-admin check uses the ONE shared check; SYSTEM_ADMIN + SUPER_ADMIN any case; platform_admin stays refused). Read that card too with `decision_queue.sh show`. The brief tells the seat to use the shared check if it exists at develop, and to say so if it does not.

## MEASURE (read-only, in the shared checkout `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`, GIT_OPTIONAL_LOCKS=0, git read verbs only: show, grep, ls-tree, log; NEVER fetch/pull/worktree/checkout)
1. The write routes for the five kinds, in api-gateway and originate: file paths and the current role check on each (git grep at origin/develop as the shared checkout has it; say which ref you read and its sha).
2. The PARTITION: list the paths this lane will touch, and check them against the live seats' paths: K 80th merges PR 2284 (originate routes/documents.ts, routes/certifications.ts, utils/callerEmailVerified.ts and test files); W 68th owns PR 2285 (12 frontend/issuer paths: read them by `GH_CONFIG_DIR='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config' gh api repos/Secuura/Distributed_Secuura/pulls/2285/files --paginate --jq '.[].filename'`, read-only). Also list every OPEN PR's files the same way and name any PR that touches the lane's paths. If the lane overlaps a live seat's paths, say so at the top of your reply and do not hide it.
3. The seat ordinal: `/usr/bin/grep -o -i -c 'seat w 68th'` and `'seat w 69th'` over `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` (with the 68th as positive control); the brief says RE-MEASURE.
4. develop's sha by `git -C <checkout> ls-remote origin refs/heads/develop` (read verb).

## ROUTING
Model claude-opus-5-5 (read from `/Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/models_latest.json`, never typed): row C3 (a build on an access DESIGN surface). Usage gauge: read `/Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/usage_wednesday.json`.

## HOLDS to carry
Client-facing words = ticket comments only; no deploy (the deploy is a D seat's under Kam's grant); demo only with Stuart's nod; tickets on Peter or Stuart stay theirs; no 'do not merge' self-hold sentence in the PR body; the shared packages/shared guards run on both arms (the 11-22 develop-red lesson); a sibling found outside the ruled five is LISTED and STOPPED on, never fixed (the 11-18 closed-list lesson).
