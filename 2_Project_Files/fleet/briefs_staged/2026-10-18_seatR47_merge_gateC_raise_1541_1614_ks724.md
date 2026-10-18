## BLUF

You are the R LANE (Secuura/Blockchain-R, the raise lane), Seat R 47th, on Opus 5.5. The weekly allowance renewed today (gauge 0%); Kam, 2026-10-18 ~19:0x: "new account so please work on the tickets, backlog and definition of which agent to use for what. Spark connected so give it as many tickets as it can handle". Your job, in this order:
1. **Merge #1560 then #1561 on Wednesday's GO.** Wednesday launched GATE C (one batched Opus gate, both PRs) at 19:0x today; its verdict lands in Wednesday's project and Wednesday mails you a head-bound GO per PR. One merge at a time, head == GO sha, develop re-read after each, the Linear links restored to `contributes` and the tickets to In Progress if the merge event moved them (your R 46th handover has the recipe).
2. **Raise KS-1541** from the held Spark READY (unmodified Spark patch).
3. **Raise KS-1614 item 4** from Wednesday's test-only golden (a test-only cell; not a Spark pass).
4. **KS-724: Kam ruled (a) "Accept as built".** Quote his ruling beside the exclusion constant and comment KS-724. One small change, gated like any other.
Send a plan confirmation first (QUESTION, topic `plan confirmation`); Wednesday answers it. Items 2-4 can be ONE PR each or batched where the files are disjoint; say which in the plan.

## QUEUE

1. **#1560 / #1561 merges.** Heads: #1560 180c7c822b571b8ff8b5ea15d4286277948c66c0, #1561 ba8c18794beddd47e7704891e6cbd4efda7664f6 (Wednesday's ls-remote 2026-10-18). Develop has MOVED to d0c5d2e0ef8bf8c1e70f9684503c5fb3a3e53c4f since you raised them (Peter's own #1562-#1564, systemTest only; Wednesday measured 0 file overlap with either PR). Do not merge before the GO; if GitHub needs develop merged in first, mail Wednesday before pushing (that changes the head the gate read).
2. **KS-1541** (MCP get_info names a gateway 403/503 refusal with status + error text; 401/404/thrown keep the old note). The READY: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1541-REFUSALNOTE-1_spark-dsv4flash_BRIEFED-CODEPATCH-INFO-PASS-7of7_2026-10-16.diff.md (Wednesday's project, read-only to you). Files: `Blockchain/Dev/services/mcp-server/src/tools/info.ts` + a NEW test `services/mcp-server/src/__tests__/ks1541-get-info-names-a-gateway-refusal.test.ts`. It was checked at 76698952; `git apply --check` it at the live tip and say the mode (strict vs recount). Red-first + green yourself, the mcp-server suite before/after. PR `Refs KS-1541`, link `contributes`, credit the Spark. READY FOR GATE.
3. **KS-1614 item 4** (a refused `[1n]` must print `[object Array]`, killing the #1554 gate's surviving catch mutant M2). Golden: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1614_p1/golden.diff + KS-1614.md beside it (test-only, one in-place hunk in `services/api-gateway/src/__tests__/ks1185-f1-workflow-approve-forward-bound-is-validated.test.ts`). It touches the api-gateway tests area #1560 also touches (different file): raise it AFTER #1560 merges. Prove the mutant: with the tamper named in KS-1614.md applied to verification.ts the new cell is RED, restored GREEN. Wednesday wrote it by hand at the 99% stop; check it against the file at the tip and say what you changed, if anything.
4. **KS-724.** The constant is in `systemTest/akto/src/scan/credentialLiveness.ts` (Kam's card cites line 88, read by Wednesday at f8c86f85, not today's develop). **Peter's own merge #1563 (a systemTest PR) changed this file and added `credentialLivenessByDesign.test.ts`.** Read the file at the LIVE tip first: if the AUTH_BYPASS_LOCKED_ACCOUNT_TOKEN_ROLE exclusion is no longer what Kam's card describes (gone, moved, or reshaped by Peter), STOP and mail Wednesday with what you found; do not re-add it. Otherwise: a code comment beside the constant quoting Kam's ruling verbatim with its date and the card id, and a KS-724 BLUF comment saying it is accepted as built (Peter asked on 2026-10-14T10:35Z; read his comment). Tier 3 hygiene unless the gate decides otherwise.

## PARTITION

Yours: `services/api-gateway/src/routes/verification.ts` and its tests (merge only), `services/originate/src/routes/adminConfig.ts` + its test (merge only), `services/mcp-server/`, the ks1185-f1 test file, `systemTest/akto/src/scan/credentialLiveness.ts` (comment only). **NOT yours:** a second seat (Secuura/Blockchain-J) is working KS-1114 in `services/originate/src/routes/verification.ts`, `originate.openapi.ts`, `docs/openapi/secuura-api.yaml`, and KS-1385/KS-1612 in `services/anchoring/` and originate's `saveDocument` path. If an item needs one of those, STOP and mail Wednesday. You share one inbox with that seat: a mail addressed to Blockchain-J is not yours.

## HOLDS

- No deploy, no demo, no production. Merges only on Wednesday's GO naming the head SHA. Never `--no-verify`, never `--force`.
- Push with the transport named in full: `GIT_SSH_COMMAND` unset and `git -c core.sshCommand="<the repo's own core.sshCommand> -o ServerAliveInterval=30 -o ServerAliveCountMax=20" push ...` (you proved this shape on 10-16).
- Client-facing communication = ticket comments only. Nothing to Stuart or Peter beyond ticket comments.
- Never delete; quarantine. Every loop in a script FILE, never inline `bash -c`.
- Wait instructions name their wake: re-arm your watcher first (your R 46th handover has the command) and read its log at every break.

## RULED BY KAM, NOT YET IN AN ARTEFACT

- secuura-gate-at-99pct-two-spark-prs-1016 = **a** "Switch account now" (2026-10-18 18:59:49, live board). Option detail, verbatim: "You run /login in the Wednesday pane (and R 46th's pane if it is per pane); Wednesday launches the gate and merges on its GO." The allowance renewed; Wednesday launched the gate. Lands in: the #1560/#1561 merges.
- secuura-ks724-locked-account-template-exclusion-1015 = **a** "Accept as built" (2026-10-18 19:00:36, live board). Option detail, verbatim: "A seat quotes your ruling beside the constant and comments it on KS-724. One small change, gated like any other." Lands in: the credentialLiveness.ts comment + a KS-724 comment.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE

- The GO is addressed to the R LANE, never to a named seat.
- Linear links stay `contributes`; a ticket closes only once tested, working and deployed.
- Gating on 13/16 preflight legs (3, 4, 8 skipped, local stack not up) stands for these raises; say so in every READY.

PROVENANCE:
- KS-1543 state (open: In Progress, last comment 2026-10-15T21:29Z) | Linear ticket KS-1543 | read 2026-10-18
- KS-1462 state (open: In Progress, last comment 2026-10-15T22:08Z) | Linear ticket KS-1462 | read 2026-10-18
- KS-1541 state (open: Backlog, no comments, unassigned) | Linear ticket KS-1541 | read 2026-10-18
- KS-1614 state (open: Backlog, no comments) | Linear ticket KS-1614 | read 2026-10-18
- KS-724 state (open: Todo, last comment 2026-10-14T10:35Z by Peter) | Linear ticket KS-724 | read 2026-10-18
- #1560 / #1561 heads | git ls-remote origin (pull 1560 and 1561 heads), run by Wednesday, not a path in your tree | read 2026-10-18
- develop d0c5d2e0 and the 0-overlap measurement (control 51) | Wednesday's scratch clone, git diff --name-only 76698952..d0c5d2e0 vs each PR | read 2026-10-18
- credentialLiveness.ts changed by Peter's #1563 | git diff --name-only 76698952..d0c5d2e0 in Wednesday's scratch clone | read 2026-10-18
- KS-1541 READY files | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1541-REFUSALNOTE-1_spark-dsv4flash_BRIEFED-CODEPATCH-INFO-PASS-7of7_2026-10-16.diff.md (+++ lines; Wednesday's project) | read 2026-10-18
- Kam's card rulings | kam_rulings_today.sh + decision_queue.sh (options[].detail from decisions.json) | read 2026-10-18

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-18 19:12
