# BRIEF: Seat D 78th, Secuura/Blockchain-D. DEPLOY/OPS seat on OPUS (claude-opus-5-5), ONE job: QUARANTINE demo's dead copies of its OLD Redis password, per Kam's card `secuura-demo-dead-redis-copies-cleanup-1120` = a. MEASURE read-only first, then a PLAN QUESTION, then WAIT for the ANSWER. Written by Wednesday (the 09:4x rotation-successor seat) directly, as a DELTA on Seat D 77th's brief (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-20_seatD77_b4_rotation.md`) and records: D 77th's (`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-20_seatD-77th/`, HANDOVER FINAL whole first; its STATUS section 4 is the LIST) and D 76th's PHASE A on Kintsugi (`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-20_seatD-76th/`: tools deadlist, qdead, qshred, qrev, the MANIFEST and conservation method; reverse `tools/qrev_d76.sh`). Its HOLDS, box-access mechanics and PACE apply as written, with the substitutions below.

## THE AUTHORITY (read at source by Wednesday)
Card `secuura-demo-dead-redis-copies-cleanup-1120`, ruled a by Kam on the live board 2026-11-20 11:43:29 (view=wednesday), verbatim: "Decision secuura-demo-dead-redis-copies-cleanup-1120: a — Quarantine the dead copies, keep the rollback for a day (recommended)". Option a's detail (Wednesday's card text): "A deploy agent moves the 22 files into one locked quarantine folder on demo with a manifest (never deleted), as on Kintsugi; the rollback copy joins it after a day; the Mac capture is listed for you, not touched. The 14 containers drop the old value at their next restart."

## THE SET (D 77th's STATUS of 00:35Z, section 4; re-measure every item: each must hold the OLD value and NOT the new one, by boolean, values never printed)
- 10 envcopies (600): `/home/secuura/seatD36-envcopy/.env.pre-20261027d6`, then the `.env` in seatD37, D38, D41, D42, D43, D44, D45, D52 and D69 `-envcopy/` (re-list by glob: the exact names are D 77th's evidence/demo/P7_deadcopies.txt).
- 10 gateway captures (664), under `/home/secuura/secuura/Dev/`: `.rebuild-seatD38/apigw.since.d8.log`, D41 d9, D42 d10, D43 d11, D44 d12, D45 d13, D52 d14a and d14b, D69 d15a and d15b.
- `Dev/.env.bak-2026-09-03` (644) and `Dev/.env.pre-20261019-vouch` (644).
= 22 files. A file that reads NEW = a STOP (it is live). A file in the set that reads neither OLD nor NEW: list it, do not move it, ask.
**NOT in this job:** `Dev/.env.pre-d16r` (the rollback: it joins on/after 2026-11-21 ~11:20 AEDT, a day after the rotation, in a LATER seat); Kintsugi's `.env.pre-k35r` (same later step, ruled 19 Nov); D 39th's Mac capture (Kam's, listed, never touched); the 14 containers' env (they drop it at their next restart); `.env.local`, `.env.example`, `test-wallet.env` (D 77th: hold neither value).

## THE WORK
1. **MEASURE** (read-only on demo): the 22, each with path, mode, owner, size, sha16 (of the FILE, not its value), OLD yes/no, NEW yes/no; whether any running process holds one open (lsof); whether any is referenced by a compose file, a script or cron (grep by path); free disk.
2. **PLAN mail** `QUESTION: plan confirmation (Seat D 78th)` (body line 1 exactly `Seat D 78th`): the table, then: Q1 the quarantine folder (D 76th's shape: `/home/secuura/quarantine_dead_redis_<date>`, 700, files 600, MANIFEST.tsv 600 with path, sha256, mode, owner, OLD flag); Q2 the move method (mv within one filesystem, or cp -p + verify + remove the original: a REMOVE of the original after a verified copy counts as the move; say which; never rm without the verified copy), conservation asserted (22 in = 22 manifest rows = 22 files in the folder; 0 left at the old paths); Q3 the reverse script (qrev shape) as commands; Q4 whether the emptied `seatD*-envcopy/` folders stay (Wednesday's default: they STAY, empty; removing folders is not in the card).
3. **WAIT for the ANSWER.** Then run it, STATUS (the conservation figures, the reverse command, the folder listing by name only), WRAP.

## SUBSTITUTIONS
- **NEW SEAT:** you are **Seat D 78th** (cockpit pane Secuura/Blockchain-D; claude-opus-5-5; trust `$TMUX_PANE`). Act ONLY on mail naming `(Seat D 78th)`. THE INBOX IS SHARED: Seat W 46th (pane Secuura/Blockchain-W, auth build, blocked) and Seat K 63rd (pane Secuura/Blockchain-K, merge seat) are live; their mail is not yours. Ordinal: D lane max D 77th (history.md; re-check). REC = `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/<machine date>_seatD-78th/`. Mail to `wednesday-agent@agentmail.to` ONLY, prefix `[Secuura/Blockchain-D -> Wednesday]`, body line 1 exactly `Seat D 78th`. Launcher preflight warnings VERBATIM in the plan mail.
- **HOLDS:** DEMO ONLY, these 22 files ONLY. No container restart, no compose action, no .env edit, no Redis action, no Kintsugi, no production, no message to people; no secret value in any mail, file, log line or transcript (booleans and file hashes only); never delete a dead copy (move to the quarantine); no cd; no rm except the original after a VERIFIED copy if the ANSWER licenses that method; kill by ancestry only.

## ROUTING AND MODEL
Model: **claude-opus-5-5** (`/Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/models_latest.json`, checked 2026-11-20 09:48:21). Row **C6** (ops on a box; credential copies), Opus, as D 76th's Kintsugi quarantine. Weekly gauge 44%.

RULED BY KAM, NOT YET IN AN ARTEFACT
- 2026-11-20 11:43:29 (live board, view=wednesday), verbatim: "Decision secuura-demo-dead-redis-copies-cleanup-1120: a — Quarantine the dead copies, keep the rollback for a day (recommended)".
- 2026-11-19 (live board), the Kintsugi twin, verbatim per Wednesday's 11-20 pickup: "Decision secuura-kintsugi-dead-redis-copies-cleanup-1119: a — Quarantine the dead copies, keep the rollback for a day (recommended)" (done on Kintsugi by D 76th; NOT this seat's).
- 2026-11-19 16:49:14 (live board, view=wednesday), verbatim: "Decision secuura-board-grant-reask-1119: a — Renew to Fri 27 Nov and run the queue now".
- No other Kam ruling for this lane (kam_rulings_today.sh live 11:41:04: newest row 08:32:36, then his 11:43:29 tap above).

PROVENANCE:
- card text and Kam's ruling | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-demo-dead-redis-copies-cleanup-1120 and /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/kam_msgs.sh 1 (read by Wednesday at 11:43) | read 2026-11-20
- the 22-file set, the exclusions and the .env.local reading | Seat D 77th STATUS mail of 00:35Z, recorded in /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-11-20.md (11:38 line) | read 2026-11-20
- D 77th's record and HANDOVER | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-20_seatD-77th/HANDOVER.md | read 2026-11-20
- the Kintsugi quarantine method (PHASE A) | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-20_seatD-76th/HANDOVER.md | read 2026-11-20
- model row | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/model-routing.md (row C6) | read 2026-11-20

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-20 11:44
