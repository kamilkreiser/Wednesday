---
date: 2026-10-19
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the 18:2x Wednesday seat (booted after the 17:31 MACHINE REBOOT), 2026-10-19 18:5x. Replace wholesale again; never stack. Previous: NEXT-PICKUP.md.pre-1019-1856 + git.
---

# NEXT PICKUP (Mon 19 Oct, ~18:56)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says. Then kam_rulings_today.sh (whole day), reconcile_rulings.py, `bash 2_Project_Files/tools/newmail.sh` (to a file), fleet_ack.sh list, decision_queue.sh list open, fleet/usage_gate.sh --check, `local-model/spark/tunnel.sh check`, `tmux list-panes -t fleet:0 -F '#{pane_id} #{@cockpit_name}'`.
2. **`cockpit.sh say` takes the cockpit NAME (`Secuura/Blockchain-J`), never a pane id** — since 18:5x it refuses `%N` with rc 8 (it used to exit 1 silently).
3. In force: Kam 10-18 new-account grant (tickets, backlog, Spark max), routing v1.0, Kam 15:50 Stuart's list, **October deploy grant EXTENDED "until further notice" (Kam 18:22:57)**. Gauge 38% at 18:48.
4. Every brief naming a push route cites `.githooks/pre-push` lines read at develop (non-ff :57-80, ALLOW_FORCE :76-80, tip-not-HEAD :323-358 at 722e07f19cee; read in `local-model/spark/cache/src`, the only Wednesday clone holding develop). Fresh clones: `git config core.hooksPath .githooks && chmod +x .githooks/pre-push`.
5. Commit your own files by pathspec before any tool that pulls. `send_brief.sh` wants ABSOLUTE provenance paths and a ticket provenance line for every queued ticket, plus a SELF-CHECK line.

## 1. KAM'S 18:22 INSTRUCTION — DATASEC OFF DEVMASTER (in flight)
- Background Opus agent (this seat's Agent tool) running brief `2_Project_Files/fleet/briefs_staged/2026-10-19_datasec-offload-devmaster-to-gdrive.md` + ADDENDUM (per-folder count table, MANIFEST.txt + README.txt "keep until Kam says" at the destination). Steps: devnas.prf ignore line `ignore = Path !CODING/Datasec` FIRST (backup devnas.prf.pre-1019-no-datasec) -> rsync to `/Volumes/G-DRIVE/DEVELOPMENT WORK/DevMASTER-Datasec-offload_2026-10-19/Datasec` -> verify (counts, bytes, sha sample, every repo, per-folder table) -> `rm -rf` source only if all EQUAL. **If the seat died, the agent died with it: check the REPORT at `0_Brain/reference/2026-10-19_datasec-offload/REPORT.md`; if absent, check whether the source still exists and whether devnas.prf carries the ignore, and re-run the brief (rsync is resumable).** A never-delete hook refused Tuesday's rm on the laptop; ours may too — then the brief says STOP and report; the next move would be Kam's word.
- Card `wed-devmaster-datasec-leftovers-1019` (rec a: move /Volumes/DevMASTER/TUESDAY to G-DRIVE too; default: nothing beyond !CODING/Datasec moves) — open.
- Tuesday clears Secuura off the laptop (mirror ruling 18:21:50). Wednesday supplied the master counts + a path diff (DevMASTER holds every content file; 7 laptop-only git ref files of a temp remote t9-drive-2026-10-15) + hidden folders (.cursor 18, .github 3, .planning 54, all equal). Laptop-DEV/WEDNESDAY (140 GB): Wednesday does not need it; Kam's call after Tuesday checks no laptop seat launches from it.

## 2. LIVE FLOOR (18:56) — develop = 722e07f19cee683ea037930e601e380a9491f7b5. Nothing deployed.
- **E 20th (%5, Secuura/Blockchain-E):** merge #1613 (KS-1195) at c336de831221 on Wednesday's GO (X1 GO r1 + Z1 GO r2, landing tree 9a3a5619e806), then deliver Kam's five rulings as ticket comments (KS-1575, KS-1596, KS-1570 + DEPLOY-BLOCKERS row 7 PR, KS-1580, KS-1384, KS-1402) + KS-1195 merged-not-deployed comment. Plan confirmation owed. On MERGED: verify landed tree, then `decision_queue.sh --delivered` each of the five cards naming the comment ids.
- **C 26th (%6):** merge #1614 (KS-1402 500 fix) at ddd54b836394 AFTER #1613 lands (Y1 GO tier 1 r1; disjoint file sets; STOP on overlap), then DESIGN the KS-1402 stub holder (Kam a) — design mail before code; tier-1 gate on the build. Plan confirmation owed.
- **R 54th (%2):** CONFIRMED; three PRs from the held Spark READYs (KS-1645 item 3, KS-1642 p1+p2, KS-1634 v2 + in-process S cell). Each -> READY FOR GATE (tier 1 KS-1645/KS-1634, tier 2 KS-1642).
- **J 15th (%3):** CONFIRMED; #1615 (KS-1603, head 4db96203546b) re-verify in a fresh clone -> READY FOR GATE (tier 1); then KS-1629 (box reading SIMULATE_ANCHORING approved, then the fix).
- **G 11th (%4):** CONFIRMED; KS-1557 write side (existence read accepted as a shape; the gate measures the SQL match), one PR tier 1; then two tickets (registerInPlatformRegistry silent catch; certifications.ts:417 assertNoCycle cycle arm) after cells; then KS-1633.
- Gates Y1/Z1 verdicts: `0_Brain/reference/2026-10-19_gate-{Y1-pr1614-ks1402,Z1-pr1613-r2-delta}/verdict.md`. Next gates as READYs land (tier-1 Opus, tier-2 Sonnet per routing v1.0).
- Spark: tunnel re-opened 18:3x (pid 21270). Held READYs all assigned to R 54th. Spent v1 KS-1634 READYs moved to `night/_spent_2026-10-19/`. **Spark is IDLE: next action = SCREEN_14 (brief drafter) for new candidates.**

## 3. KAM'S CARDS
Ruled 18:22-18:23 (recorded 18:28): signing additions a, ks1570 a (+grant extension), ks1580 a, ks1384 b, ks1402 a — **NOT YET DELIVERED** (E 20th's job). Open: wed-devmaster-datasec-leftovers-1019 + Tuesday's Datasec cards.

## 4. OWED BY WEDNESDAY (own tools, small)
1. pretooluse_no_cd.sh: a `git -C $VAR` write on WEDNESDAY itself is refused (bit twice today); allow variables resolving inside WEDNESDAY.
2. receiptguard false positive (note + safe_push chain).
3. fleet_ack: a QUESTION is not collected for ~1-2 min after arrival; `answered` refuses until then (expected, re-run).
4. Deploy round (Kintsugi): READ-ONLY census seat first, once DEPLOY-BLOCKERS clears (KS-1570 row closing via E 20th's PR; Stuart's dev-ps deploy; #1614 merged).
5. Fable 5.1 coordinator/gate trial (routing decision 7). Gate brief template: name touched services' suites RUN or NOT-tested.
6. The 95 `t <t@e.com>`-authored commits on develop; keep every stash.
7. Secuura launcher prompt "CC Kam on every email" is stale (carried in every brief's HOLDS now).
8. Regenerate BOTH boot digests at the wrap (ledger edited 18:5x).
