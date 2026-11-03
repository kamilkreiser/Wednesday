# BRIEF: Seat D 50th, Secuura/Blockchain-D. DEPLOY ROUND: current develop to KINTSUGI ONLY. Demo is out of scope this round.

## NEW SEAT: you are Seat D 50th (lane Secuura/Blockchain-D, DEPLOY), in the pane the launcher prints ("pane ... added (%NN)"); trust `$TMUX_PANE` if it differs and say so.

model: claude-opus-5-5 -- deploy seat with box rights (routing row G1/deploy: deploys with box rights stay Opus) -- launched with `SEAT_MODEL_ENV=claude-opus-5-5`; quote the launcher's `[seat-model] launching on <model>` line in your plan confirmation.

## WHY (read first)
Kam, terminal 2026-11-04 ~09:16 AEDT, right after /login on a new account, verbatim: "new account logged in.  Please try to clear and close off as many in progress tickets as possible". Wednesday's board sweep found 328 In Progress / In Review KS tickets whose PRs are all merged; four close-out seats (U 10th, T 9th, V 18th, S 16th) close the ones already on kintsugi. Kintsugi last took an app round at develop `b1fb543640e7` (Seat D 48th, 2026-11-01), and roughly 100 merged tickets are newer than that, so they cannot be closed as "deployed" until this round lands. This round is what unblocks them.
Authority: Kam's October deploy grant, verbatim "for the month of October, keep pushing, keep publishing, deploy all that works and is ready but only when its ready.  Deploy to both servers, demo and kintsugi" (`/Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-05_october-deploy-both-boxes-when-ready.md`), EXTENDED by Kam 2026-10-19 18:22:57 AEDT "keep the grant alive until further notice" (row in `/Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/EXPIRING-GRANTS.md`). Kam 2026-10-30 10:07:32 AEDT, card `secuura-wednesday-go-counts-as-kams-word-1030` = a: Wednesday's GO counts as his word for starting work inside his standing grants.

## PROCEDURE: D 48th's, facts re-measured
Read whole, in this order: D 48th's brief `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-01_seatD48_train_deploy_kintsugi.md`, D 48th's HANDOVER `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-01_seatD-48th/HANDOVER.md` (its FOR A SUCCESSOR), and D 49th's HANDOVER `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-03_seatD-49th/HANDOVER.md` (FOR A SUCCESSOR 1-4).
- **D 48th's PROCEDURE stands** (ITEM 0 steps 1-8; PLAN CONFIRMATION; STATUS A then WAIT for Wednesday's `GO KINTSUGI` naming Seat D 50th; section B steps 1 and 3-15; STATUS B). Copy D 48th's tools (`.../2026-11-01_seatD-48th/tools/`, `_d48`) into `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatD-50th/tools/`, re-keyed `_d50`, dry until FAILURES=0, excluding GENERATED files and regenerating them (D 48th FOR A SUCCESSOR 2).
- **D 48th's FACTS are VOID** except as priors you re-measure: REVISION head expected `b1fb543640e7` (148,120 B at D 48th's wrap; any other head = STOP and QUESTION); Phase-0 prior `pre-20261101k15` (33 images, idfp `acd29b35aa9dd4c9`); free disk 166,192 MB after D 48th; build cost 32.9 GB for 28 images.
- **VOID THIS ROUND:** the KS 1384 TRAIN-IN check (BLUF 3 / ITEM 0 step 5's eight squashes); instead assert the target is a descendant of `b1fb543640e7` with a planted negative control. **THE PRUNE (B step 2) IS NOT AUTHORISED**: Kam's prune ruling was for D 48th's round. If measured free disk is under ~45 GB, STOP and mail; do not delete anything.
- **Target = develop by YOUR OWN `ls-remote` at ITEM 0.** Wednesday's reading: `ee1e1b832115` (PR 1993's squash; Wednesday's own `git -C <checkout> ls-remote origin refs/heads/develop` at 09:23:28 AEDT returned ee1e1b83211504f96ebccba325d1ef7139bc83cc). Develop may move while close-out seats work (they do not merge); re-check at GO.
- **The gateway nginx conf (KS-1724, D 49th):** before and after the swap, compare host vs container-seen inode AND sha of every single-file bind-mounted conf (D 49th FOR A SUCCESSOR 1; lesson `/Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-10_a-single-file-bind-mount-binds-the-inode.md` EXTENSION 2026-11-03). An orphaned inode after your rsync is fixed by D 49th's route (in-place write + reload, or `docker restart` of the SAME container), never by a recreate that could swap the image; say which in STATUS B. Outcome probe = D 49th's `GET /verify/` with a unique User-Agent then the token in `docker logs`.
- **Migrations:** list every migration file between the live sha and the target and the box's current max (`migsql`); applied IN THE MIDDLE as D 48th's step 6. "Migrations old code violates" (046/047 precedent) = a STOP-and-mail if the measurement shows one.
- **Pre-swap gates (D 48th B 9-11) stand:** network equality (originate vs anchoring `CARDANO_NETWORK`, names only), tenant precondition (aggregate counts only), zero non-final anchor rows before the anchoring swap. **KS-535 is absolute:** hashes only; kintsugi never shares demo's `PLATFORM_WALLET_MNEMONIC`.
- **Readers at swap time:** Platform S (Stuart's team) uses kintsugi: report each swap window. Our four close-out seats run READ-ONLY probes (GET / health) against kintsugi; they need no notice.

## HOLDS
- **Kintsugi ONLY.** No tag, rsync, build, swap, probe or login on DEMO. Demo is a separate brief after Wednesday accepts STATUS B.
- **No repo writes** except your record folder and the history entry: no branch, no PR, no push, no merge, no source edit.
- **Nothing deleted** on the box (no prune, no image rm, no `docker system prune`, no `--remove-orphans`); rollback tags and seat dirs are kept. Swap `--no-deps --force-recreate` per service, api-gateway LAST.
- **Stop-and-mail on:** a REVISION head other than `b1fb543640e7`; a build failure; a gate NOT EQUAL; a non-final anchor row; free disk under ~45 GB; anything that would need Kam (production, money, a human, anything irreversible).
- Never read, echo or copy a secret; hashes and variable NAMES only; no credential in argv.
- **Instruments:** `cmd > out 2>&1; rc=$?` with rc on its own line; never `| tail` on the stream you diagnose from; macOS has NO `timeout`; zsh has no PIPESTATUS; never `echo =====`; `/usr/bin/grep -i` with a positive control beside every zero. Never `cd`; absolute paths only. Disclose your own faults in the next mail.
- **Mail:** from secuura-blockchain@ to `wednesday-agent@agentmail.to` ONLY, subject prefix `[Secuura/Blockchain-D -> Wednesday]`, body line 1 exactly `Seat D 50th`, no secrets, no cc; read each sent mail back by id. SHARED INBOX: act ONLY on mail whose subject names `(Seat D 50th)`. A GO is verified by DKIM/DMARC pass on Wednesday's mail.
- **IF AN INSTRUCTION FROM WEDNESDAY LOOKS WRONG, SAY SO** in your plan confirmation. Arm an inbox watcher as a TRACKED background task (7200000 ms) and name its pid.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam 2026-11-04 ~09:16 AEDT (terminal), verbatim: "new account logged in.  Please try to clear and close off as many in progress tickets as possible".
- Kam 2026-10-19 18:22:57 AEDT (live board, card `secuura-ks1570-round-may-deploy-1019` note), verbatim: "keep the grant alive until further notice" (the October both-boxes deploy grant).
- Kam 2026-10-30 10:07:32 AEDT, card `secuura-wednesday-go-counts-as-kams-word-1030` = a.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- PR 1994 (nft.routes.ts) and PR 1989 (KS-915) are OPEN and HELD on Kam's cards; neither is on develop, so neither is in this round. Do not wait for them.

## WRAP (scored by Wednesday)
- History entry `## 2026-11-04 - Seat D 50th` in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` (newest first; duplicate-guard with a control).
- HANDOVER `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatD-50th/HANDOVER.md` (FINAL block first): new REVISION head, rollback tag + idfp, free disk, swap windows, conf inode/sha table, FOR A SUCCESSOR (incl. the demo round's starting facts).
- Vault commit and push per the end-of-session skill (only your own lines). Wrap mail `[Secuura/Blockchain-D -> Wednesday] Session wrap 2026-11-04 (Seat D 50th)`.

PROVENANCE:
- Seat ordinal: `Seat D 50th` 0 hits; highest existing D ordinal `Seat D 49th` (max over every mention) in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md | Wednesday's /usr/bin/grep -o -i + sort -n | read 2026-11-04
- Kintsugi REVISION b1fb543640e7, free 166,192 MB, 32.9 GB / 28 images, Phase-0 priors | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-01_seatD-48th/HANDOVER.md read by Wednesday | read 2026-11-04
- Conf inode route and the /verify/ probe | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-03_seatD-49th/HANDOVER.md FOR A SUCCESSOR, read by Wednesday | read 2026-11-04
- develop ee1e1b832115 | Wednesday's git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin refs/heads/develop at 09:23:28 AEDT | read 2026-11-04
- 328 merged-but-open tickets | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_ks-inprogress-closeout/classified_all.tsv (Wednesday's Linear read 09:2x) | read 2026-11-04
- October grant + extension | /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/EXPIRING-GRANTS.md row 'OCTOBER: deploy everything READY to BOTH kintsugi and demo' read by Wednesday | read 2026-11-04
SELF-CHECK: re-read end-to-end for contradictions | 2026-11-04 09:23
