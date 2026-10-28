## You are Seat D 41st (lane Secuura/Blockchain-D, DEPLOY), in the pane the launcher prints ("pane ... added (%NN)"); trust `$TMUX_PANE` if it differs and say so. Job: deploy develop `5dccdcb29ec20393e80cbdb1e359a49caa633165` to KINTSUGI, verify, then DEMO, then re-apply the `secuura-demo-service` stop on both boxes as the last step.

**Seat ordinal (measured by Wednesday 2026-10-29 ~09:1x AEDT):** `/usr/bin/grep -i -c 'Seat D 41st' 5_Project_History/history.md` = 0; control `Seat D 40th` = 1. You are the first D 41st.

**Routing receipt:** `model: claude-opus-5-5 -- C6 (deploy with box rights) -- P1-P4 -- gauge 94%`. Launched with `SEAT_MODEL_ENV=claude-opus-5-5`; quote the launcher's `[seat-model] launching on <model>` line in your plan confirmation. Why Opus at 94% (Kam 2026-10-29 07:29, "you and the spark with minimal (but used when necessary) Claude agents"): box rights are a necessary Claude use; no local tier can deploy. This is the ONE deploy seat Wednesday's reading of that ruling allows.

## BLUF
- **Authority:** the October deploy grant, kept alive by Kam 2026-10-19 18:22:57 "keep the grant alive until further notice" (`/Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/EXPIRING-GRANTS.md`, row OCTOBER), plus card `wed-morning-plan-1029` ruled **a** "Carry on with the plan" at 07:29:49 (finish the merge chain, then a deploy round kintsugi -> demo). Kintsugi first; demo ONLY after kintsugi is verified.
- **The runbook is Seat D 38th's brief, whole:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-28_seatD38_deploy_round.md`, plus the "FOR A SUCCESSOR" lines of `5_Project_History/2026-10-28_seatD-38th/HANDOVER.md` (binding) and D 38th's tools in `5_Project_History/2026-10-28_seatD-38th/tools/` (re-key them to `*_d41` with a re-keyer, as D38 did from D37). **Its PROCEDURE stands. Its FACTS are VOID for this round:** every sha, stamp, rebuild set, swap set, fix string, content-change prediction, M1 measurement and notice text in it belongs to the 8894c7486f82 -> bd6697e079fc round. Re-derive each one for this round in section A and report it in STATUS A **before any build**.
- **This round is NOT small.** Delta `bd6697e079fc..5dccdcb29ec2`: 22 first-parent commits, 76 files, +6376/-207 (Wednesday's cache clone, `git rev-list --count --first-parent` and `git diff --shortstat`, read 2026-10-29). **`packages/shared/src` changes** (`errors/index.ts`, `security/keyRevokePolicy.ts`), so every image that copies `/shared/dist` is expected to rebuild: treat it as a near-whole-graph round, like D 37th's, never like D 38th's three-image round. Do not carry any build time, rate or count from either.

## QUEUE
### A. PIN, DELTA, PRECHECK (read-only), then STATUS A
1. Re-read develop (`git ls-remote origin refs/heads/develop`) and each box's `REVISION`. **Expected develop 5dccdcb29ec2; expected box REVISION bd6697e079fc (Wednesday's pickup; UNMEASURED by Wednesday: you read it).** Any other value is a STOP and QUESTION.
2. Derive the delta in your own clone `deploy-clones/seatD41-5dccdcb29ec2`, and from the Dockerfiles and `docker-compose.yml` at the pin derive the REBUILD set and the SWAP order, by D 38th's method (`map_images_*` re-keyed). Wednesday's measurement for you to confirm or correct: 0 `.sql`, 0 lockfiles, 0 Dockerfile, 0 docker-compose, 0 `package.json`, 0 `.dockerignore` in the delta (`grep -i -E` over `git diff --name-only`, a `services/` control counted 52). Services with changed paths: api-gateway 7, auth 23, m365-integration 3, nft-certificate 2, originate 10, security 2, tenant-provisioning 5; plus `packages/shared` 4, `scripts/` 6, `Blockchain/Testing` 5, `tests/e2e` 1, `docs` 3. **Some of those may be test-only: the image set is YOURS to derive, not this list.** If you find a `.sql` or a lockfile, STOP and QUESTION (a migration changes the swap rules).
3. Runtime-visible PRs: list every PR in the delta whose product change is in an image, with its fix string read by `git show <sha>:<path> | grep -c -F --` at both ends, exactly as D 38th's "Fix strings" table does. **Each row says ADD or REMOVE from the diff's own +/- lines, and its assertion follows from that** (ledger 2026-10-26: a removal cannot be asserted as "running>=1").
4. Baselines and the precheck per D 38th's A4 (tracker, anchor_store, provenance tables, `.env` sha16, wallet hashes, infra StartedAt). **Seats D 39th and D 40th ran on kintsugi AFTER D 38th** (an M1b measurement, then ONE POST and one GET under Kam's card b; Wednesday's SCORE to D 40th, `fleet/briefs_staged/2026-10-28_score_seatD40.md`), so kintsugi's row counts will NOT equal D 38th's: read both of their HANDOVERs in `5_Project_History/2026-10-28_seatD-39th*` and `2026-10-28_seatD-40th*` before you call any baseline moved. **KS-535 is absolute: kintsugi must never share demo's `PLATFORM_WALLET_MNEMONIC`.** Read both wallet hashes before and after.
5. **UNMEASURED, read it:** KS-1717 (#1690, `28e2d27de`) is on develop and NOT in this delta, so it shipped in an earlier round. Whether `EMITTER_SIGNING_SECRET` is set on each box and whether anchoring logs `[emitter-guard] ACTIVE` is unknown to Wednesday. Read it (log line and the variable's PRESENCE only, never its value) and report it in STATUS A. Do not set or change it.
6. Stamps: rollback tags `pre-20261029k9` (kintsugi) and `pre-20261029d9` (demo); confirm each ABSENT before use (box clocks read UTC). Phase 0 re-tag before any build (both boxes run bare `:latest`).
7. Mail **STATUS A** (the delta, the rebuild and swap sets, the fix-string table, the baselines, item 5) and WAIT for Wednesday's GO before building anything.

### B. KINTSUGI, C. DEMO
As D 38th's sections B and C: build everything before swapping anything; swap in the derived order; KS-535 after each box; the live sweep; the dist fingerprints (`contentfp`) against the predictions you wrote in STATUS A; `[gateway-provenance] ACTIVE` on originate. **Demo starts only on Wednesday's GO after STATUS B (kintsugi verified).** A rollback, a SAME-ID image you predicted would change, or a content change you did not predict is a STOP and mail.

### D. TICKETS AND NOTICES
- Draft the deploy notices for KS-485 (Peter) and KS-772 (Stuart) as D 38th did. **They post ONLY on Wednesday's word** ("POST NOTICES"); times rendered with `TZ=Australia/Sydney date -r <epoch>`, UTC and AEDT both, one value checked by a second instrument.
- Tickets that become Done by this deploy: list them with the evidence (merged PR + deployed build containing the commit + the live check). Do not move them: Wednesday rules each one (Kam 2026-10-12: Done = tested + works + deployed).

## COMMS
Mail `wednesday-agent@agentmail.to`, subject `[Secuura/Blockchain-D -> Wednesday] <topic>`, `Seat D 41st` on body line 1, no CC, no secret values, no tenant slugs, no document titles, no emails. Milestones: PLAN CONFIRMATION (launcher preflight warnings VERBATIM), STATUS A, STATUS B (kintsugi), STATUS C (demo), WRAP.

## PARTITION
**Yours:** both boxes through the project's tooling, your clone `deploy-clones/seatD41-5dccdcb29ec2`, `5_Project_History/2026-10-29_seatD-41st/`. **Live seats on the shared inbox `secuura-blockchain@`:** Seat R 7th (pane `Secuura/Blockchain-R`, %68; raising H2, a NEW PR for KS-1780 part 2, then filing tickets). A mail naming another seat is not for you; a GO is acted on only if it names Seat D 41st. You open no PR, edit no source, push nothing. `2_Project_Files` is READ-ONLY. Stop only PIDs you started; never pkill or killall by name.

## HOLDS
- D 38th's HOLDS section applies whole (production, money, external comms, irreversible pause for Kam; no `az`, no prune, no `--no-verify`, no force push, no `--admin`; never delete, quarantine; never edit a running script; exit codes on their own line; the ADMIN CREDENTIALS hold). **NO test write on either box** (no create, key, login, document, tenant or user row).
- Never mix tenants or clients: this is Secuura only.
- Drive hygiene: regenerable leftovers you create (your clone's `node_modules`, build scratch) are removed at your wrap, your own only, with `df` before and after (Kam 2026-09-29). Images on the boxes are NOT pruned.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Card `wed-morning-plan-1029` = a (2026-10-29 07:29:49): finish the merge chain, then this deploy round. The artefact is this brief.
- Kam 2026-10-29 07:29:41: "with usage at 92%, lets work on you and the spark with minimal (but used when necessary) Claude agents". So: ONE deploy seat, no sub-agents of your own beyond what the runbook needs.
- `secuura-demo-service-crash-loop` (2026-09-05): `docker stop` only, re-applied as the last step on each box.
- Older ruled Secuura cards show no delivery mark in `decision_queue.sh list ruled --undelivered` (Aug-Sep 2026: ks661-vocab, secuura-agent-github-identity, secuura-dependabot-triage, secuura-ks229-disclosure-mailbox, secuura-ps-759-760-merge-owner, secuura-demo-kam-admin-default-password, secuura-f5-login-limiter-bypass, secuura-f5-demo-exposure-probe). None is a deploy instruction; act on none of them. If one of them seems to bear on a box you are changing, QUESTION.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- The four held containers stay held (2026-10-19). demo-service's restart loop is KS-1079's.
- Seat D reads, builds, swaps and reports; it opens no PR and edits no source. Notices post only on Wednesday's word. Demo takes a build only after kintsugi is verified. Never quote a rebuild count or build rate across boxes.

PROVENANCE:
- develop = 5dccdcb29ec20393e80cbdb1e359a49caa633165, single parent c571a626e53c | `git -C <Wednesday cache clone> fetch` + `log -1` after #1799 merged | read 2026-10-29
- box REVISION bd6697e079fc (UNMEASURED by Wednesday) | /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/NEXT-PICKUP.md 06:2x block ("boxes on bd6697e079fc") | read 2026-10-29
- delta 22 first-parent commits, 76 files, +6376/-207 | `git rev-list --count --first-parent bd6697e079fc..develop` and `git diff --shortstat` in the cache clone | read 2026-10-29
- no .sql, lockfile, Dockerfile, compose, package.json or .dockerignore in the delta; packages/shared/src changed | `git diff --name-only` + `grep -i -E` with a services/ control (52) | read 2026-10-29
- KS-1717 (#1690, 28e2d27de) on develop, not in the delta | `git log --first-parent --grep=KS-1717` both ranges in the cache clone | read 2026-10-29
- October deploy grant alive until further notice | /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/EXPIRING-GRANTS.md row OCTOBER (Kam 2026-10-19 18:22:57) | read 2026-10-29
- card wed-morning-plan-1029 ruled a 07:29:49 and Kam's 07:29:41 usage words | `kam_rulings_today.sh` live board read 08:01 | read 2026-10-29
- D 38th runbook and HANDOVER exist | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-28_seatD38_deploy_round.md and `ls` of your own 5_Project_History/2026-10-28_seatD-38th/ (HANDOVER.md, tools/) | read 2026-10-29
- KS-485 state Todo (open, last comment 2026-10-28T06:56:14Z; newest-first page of 50) - the Peter review-stream parent the deploy notice is DRAFTED for | Linear ticket KS-485 | read 2026-10-29
- KS-772 state Todo (open, last comment 2026-10-28T06:56:15Z; newest-first page of 50) - the Stuart S<->K stream parent the deploy notice is DRAFTED for | Linear ticket KS-772 | read 2026-10-29
- KS-535 state Done (closed, last comment 2026-08-02T00:44:49Z) - named in this brief as the STANDING wallet rule, not as open work (one wallet per box) | Linear ticket KS-535 + /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-10_kintsugi-first-then-demo-behind-gates.md rule 3 | read 2026-10-29
- ordinal Seat D 41st unused | `/usr/bin/grep -i -c` over your own 5_Project_History/history.md (D 40th = 1 control) | read 2026-10-29

## UNMEASURED (what Wednesday could not establish)
- Each box's REVISION, the image set, the swap order, every fix string, the expected `contentfp` verdicts, the M-style database counts: yours, in STATUS A.
- KS-1717's secret and `[emitter-guard]` state on each box (item A5).
- Whether any merged ticket in the delta needs a live check that this deploy cannot do (list it, do not invent it).

Self-check notes: D 38th's facts are declared void in line 9, so its stop rule's old REVISION does not contradict line 14; a push is forbidden in both HOLDS and PARTITION.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-29 09:18
