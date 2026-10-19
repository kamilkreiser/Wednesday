---
date: 2026-10-19
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the 18:2x Wednesday seat (booted after the 17:31 MACHINE REBOOT), 2026-10-19 18:5x. Replace wholesale again; never stack. Previous: NEXT-PICKUP.md.pre-1019-1856 + git.
---

# NEXT PICKUP (Mon 19 Oct, ~19:30; 70% checkpoint refresh)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says. Then kam_rulings_today.sh (whole day), reconcile_rulings.py, `bash 2_Project_Files/tools/newmail.sh` (to a file), fleet_ack.sh list, decision_queue.sh list open, fleet/usage_gate.sh --check, `local-model/spark/tunnel.sh check`, `tmux list-panes -t fleet:0 -F '#{pane_id} #{@cockpit_name}'`.
2. **`cockpit.sh say` takes the cockpit NAME (`Secuura/Blockchain-J`), never a pane id** — since 18:5x it refuses `%N` with rc 8 (it used to exit 1 silently).
3. In force: Kam 10-18 new-account grant (tickets, backlog, Spark max), routing v1.0, Kam 15:50 Stuart's list, **October deploy grant EXTENDED "until further notice" (Kam 18:22:57)**. Gauge 38% at 18:48.
4. Every brief naming a push route cites `.githooks/pre-push` lines read at develop (non-ff :57-80, ALLOW_FORCE :76-80, tip-not-HEAD :323-358 at 722e07f19cee; read in `local-model/spark/cache/src`, the only Wednesday clone holding develop). Fresh clones: `git config core.hooksPath .githooks && chmod +x .githooks/pre-push`.
5. Commit your own files by pathspec before any tool that pulls. `send_brief.sh` wants ABSOLUTE provenance paths and a ticket provenance line for every queued ticket, plus a SELF-CHECK line.

## 0b. ROTATION NOTE (19:5x, ctx ~76%)
- **Background sub-agents die with the rotating seat.** In flight at this note: GATE AE1 (#1619 KS-1557, brief `0_Brain/reference/2026-10-19_gate-AE1-pr1619-ks1557/GATE_BRIEF.md`), GATE AF1 (#1620 KS-1402 stub, `..._gate-AF1-pr1620-ks1402/GATE_BRIEF.md`, plus Wednesday's addendum: the one added not.toBe line in the KINTSUGI cell is an authorised strengthening), GATE AG1 (#1621 KS-1634 v2, `..._gate-AG1-pr1621-ks1634v2/GATE_BRIEF.md`), and the DATASEC OFFLOAD agent (brief `2_Project_Files/fleet/briefs_staged/2026-10-19_datasec-offload-devmaster-to-gdrive.md` + two addenda: a per-folder count table + MANIFEST/README "keep until Kam says"; case-collision twins preserved under `_case_twins/` with MAP.txt, since G-DRIVE is APFS). **On boot: for each gate, if `verdict.md` is absent, re-run the gate from its brief (new scratch path). For Datasec: check `0_Brain/reference/2026-10-19_datasec-offload/REPORT.md`; if absent, check whether rsync (homebrew, `-aHX`) is still running (`ps aux | grep -i rsync`; `pgrep -fl` misses it because of the `!` in the path), whether `devnas.prf` carries `ignore = Path !CODING/Datasec` (it did at 18:35), then re-commission the verify + twins + removal steps from the brief.** Nothing has been removed from DevMASTER at this note.
- **20:1x STATE:** #1619 (G, KS-1557) GO WITH NOTE from AE1 (live landing 9579105768a7 on 6ec1b7badb9b): G merges, then builds KS-1633 (ruled (a): row first + compensating delete; held cells a96c877c6 + an AE1-N2 ordering-pin cell). **#1620 (C, KS-1402 stub) NO GO from AF1** (B1 the race fallback never runs: auth upserts with a phantom id; B2 the 200 alreadyExisted branch re-read is untested): **fix round 2 of 2 sent 20:1x**; the next NO GO ships nothing and tickets the residue. #1621 (R, KS-1634 v2) at AG1; R works the addendum queue meanwhile (KS-1641 in push: Refs only, 1 of 3 sites). Gate verdicts: `0_Brain/reference/2026-10-19_gate-{AE1,AF1,AG1}-*/verdict.md`.
- **MERGED since 19:5x, verified by Wednesday's fetch:** #1617 (66faac9aebc3, tree 83c945a644b8) and #1618 (6ec1b7badb9b, tree d90ae12944e0). develop = 6ec1b7badb9b. J 15th wrapped (0.95), pane closed. R 54th: #1621 at AG1, then the addendum queue (KS-1641/KS-1460/KS-1568 held READYs). G 11th: KS-1633 cells held at a96c877c6, product edit after #1619 merges; KS-1659 filed.
- **Merges awaiting their seats (older line, superseded where the line above says so):** #1617 (J, KS-1629) MERGED as 66faac9aebc3 (J's MERGED mail pending; verify the tree in the cache clone). #1618 (R, KS-1642) GO given; R merges after PR-C's push window. #1619 (AE1) and #1620 (AF1) at gate. KS-1633 ruled (a), G builds after #1619 merges.

## 1. KAM'S 18:22 INSTRUCTION — DATASEC OFF DEVMASTER (in flight)
- Background Opus agent (this seat's Agent tool) running brief `2_Project_Files/fleet/briefs_staged/2026-10-19_datasec-offload-devmaster-to-gdrive.md` + ADDENDUM (per-folder count table, MANIFEST.txt + README.txt "keep until Kam says" at the destination). Steps: devnas.prf ignore line `ignore = Path !CODING/Datasec` FIRST (backup devnas.prf.pre-1019-no-datasec) -> rsync to `/Volumes/G-DRIVE/DEVELOPMENT WORK/DevMASTER-Datasec-offload_2026-10-19/Datasec` -> verify (counts, bytes, sha sample, every repo, per-folder table) -> `rm -rf` source only if all EQUAL. **If the seat died, the agent died with it: check the REPORT at `0_Brain/reference/2026-10-19_datasec-offload/REPORT.md`; if absent, check whether the source still exists and whether devnas.prf carries the ignore, and re-run the brief (rsync is resumable).** A never-delete hook refused Tuesday's rm on the laptop; ours may too — then the brief says STOP and report; the next move would be Kam's word.
- Card `wed-devmaster-datasec-leftovers-1019` (rec a: move /Volumes/DevMASTER/TUESDAY to G-DRIVE too; default: nothing beyond !CODING/Datasec moves) — open.
- Tuesday clears Secuura off the laptop (mirror ruling 18:21:50). Wednesday supplied the master counts + a path diff (DevMASTER holds every content file; 7 laptop-only git ref files of a temp remote t9-drive-2026-10-15) + hidden folders (.cursor 18, .github 3, .planning 54, all equal). Laptop-DEV/WEDNESDAY (140 GB): Wednesday does not need it; Kam's call after Tuesday checks no laptop seat launches from it.

## 2. LIVE FLOOR (19:3x) — develop = ad784e702ca205230e39d329abefa8a85fb5946c (#1615). Nothing deployed.
- **MERGED tonight, each verified by Wednesday's own fetch into local-model/spark/cache/src:** #1613 KS-1195 (31cfb44dce84, tree 9a3a5619e806 = Z1), #1614 KS-1402 500 fix (80868551e679, tree 9fec48e29e34), #1615 KS-1603 (ad784e702ca2, tree 8b67dde748 = AA1). None closes its ticket (Done = deployed + live check).
- **R 54th (%2):** #1616 KS-1645 item 3 has GO WITH NOTE from AB1 (landing 34aebee73a39 on ad784e702ca2): R corrects the PR body for N1 (security never reads `type`: item 3 NARROWED not closed), merges, comments KS-1645. Then PR-B (KS-1642 p1+p2), PR-C (KS-1634 v2 + in-process S cell), then ADDENDUM: three held Spark READYs, one PR each: KS-1641 OAUTHCAP-2 (tier 1), KS-1460 STUBCLAIMCONFIRM-1 (tier 1), KS-1568 ROTATEWAITPARSE-1 (tier 2). On each MERGED: verify the tree in the cache clone.
- **J 15th (%3):** #1615 merged; KS-1652 filed (tenantless arm WAS ruled 05:55:40Z; Wednesday's GO sentence withdrawn). KS-1629 built to ruling (b) (always 404 without a row; ks520 re-pinned, disclosed), commit f8b3bf0cd313: READY FOR GATE owed -> tier-1 Opus gate.
- **G 11th (%4):** KS-1557 write side built; SHAPE CHANGED to getDocument + identity guard (accepted as a shape; the gate gets three questions: guard exactness incl. migration 050, access-before-cycle ordering, the six re-pinned cells). READY owed -> tier-1 Opus gate. Then two tickets + KS-1633.
- **C 26th (%6):** KS-1402 stub-holder build APPROVED as a shape (auth /api/users/stub, tenant re-read through originate's bound predicate, admission via certifications:write + a cell pinning it, KINTSUGI parity cell re-pinned + renamed). READY owed -> tier-1 Opus gate.
- **E lane:** E 20th wrapped, scored 1.0, pane closed. No E seat live.
- Gate letters used today up to AB1; next is AC1.
- Spark: SCREEN_14 done (3 held). Next screen when the held READYs are raised or the pool changes; KS-846 (packages/shared build trap, now Medium) is a Spark-able candidate if one file.

## 3. KAM'S CARDS
All five 18:22-18:23 rulings DELIVERED (comment ids in the cards; ks1570 card now carries ruling_note "keep the grant alive until further notice"). DEPLOY-BLOCKERS.md (WEDNESDAY's own file, 0_Brain/tasks/) row ks1533-admin-bounded moved to ## Closed 19:13. Open for Kam: wed-devmaster-datasec-leftovers-1019 (rec a), wed-delegation-grant-mail-lost-its-signature-1019 (rec a re-send; default b vault record) + Tuesday's Datasec cards.

## 4. OWED BY WEDNESDAY (own tools, small)
1. pretooluse_no_cd.sh: a `git -C $VAR` write on WEDNESDAY itself is refused (bit twice today); allow variables resolving inside WEDNESDAY.
2. receiptguard false positive (note + safe_push chain).
3. fleet_ack: a QUESTION is not collected for ~1-2 min after arrival; `answered` refuses until then (expected, re-run).
4. Deploy round (Kintsugi): READ-ONLY census seat first, once DEPLOY-BLOCKERS clears (KS-1570 row closing via E 20th's PR; Stuart's dev-ps deploy; #1614 merged).
5. Fable 5.1 coordinator/gate trial (routing decision 7). Gate brief template: name touched services' suites RUN or NOT-tested.
6. The 95 `t <t@e.com>`-authored commits on develop; keep every stash.
7. Secuura launcher prompt "CC Kam on every email" is stale (carried in every brief's HOLDS now).
8. Regenerate BOTH boot digests at the wrap (ledger edited 18:5x).
