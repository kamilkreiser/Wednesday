---
date: 2026-10-07
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE 2026-10-07 05:3x by the night seat c1dbe0b9 (booted 01:5x) at the 05:30 shift-change wrap, ctx ~63%. Previous copy in that session's scratchpad. Replace wholesale again; never stack.
---

# NEXT PICKUP

## 🔴 FIRST ACTS (in order) — the 06:00 MORNING seat
0. `kam_rulings_today.sh` + `reconcile_rulings.py`. **TWO CARDS OPEN WITH KAM, both block work, lead the morning brief with them:**
   - **`secuura-advisory-freeze-3-ghsa-1007`** (filed 05:0x). EVERY Secuura push is frozen by pre-push legs 6/7 on three newly published advisories that are develop's: shell-quote GHSA-pqg4-j6r4-53mv CRITICAL; @modelcontextprotocol/sdk GHSA-6qxp-vccf-f47h HIGH (services/mcp-server); pbkdf2 GHSA-477h-4r7f-fvrx moderate (frontend/issuer, packages/shared, services/anchoring). Rec (a): one dependency seat does an in-range lock refresh, gated T1, merged first (the shape Kam ruled (a) on 10-06's five-advisory card). (b) baseline all three. (c) hold until the renewal. **Default: nothing baselined, bumped or pushed.** Wednesday's 2026-09-09 advisory grant does NOT cover it (high/critical; pbkdf2 is in shipped trees). On (a): the dependency seat's brief carries R 5th's four-way proof (in `fleet/briefs_staged/2026-10-07_seatR5_ctx_preB5.txt`) and the 10-06 card's (a) text as the shape; runtime reach of shell-quote and the MCP SDK is UNMEASURED and is item 0 of that seat.
   - **`secuura-demo-disk-retire-old-rollback-sets-1007`** (filed 01:4x). Rec (a): delete demo's `rollback-2026-09-03` + 4 small sets, KEEP `pre-20260910`, tag a fresh set first, then deploy. **Default: nothing deleted, no demo deploy.** **D 13th WRAPPED COLD at 05:3x** (0 writes to demo; scored 0.96; pane closed). On (a): brief and launch **Seat D 14th** from `5_Project_History/HANDOVER-seatD13-demo-deploy.md` (sha256/16 077d2879ec4dff8b, its READ THIS FIRST + Wednesday's rulings logged verbatim) and the D 13th brief `fleet/briefs_staged/2026-10-07_seatD13_demo_deploy.md`. Its GO subject is `GO (Seat D 14th): deploy d75bfe2deb80 to demo`, the body naming the card and the exact sets (rollback-2026-09-03 + rollback-2026-08-27-ks661, pre-ks488, rollback-20260901-prefix, pre-ks719; KEEP pre-20260910 + the new pre-<stamp>). It RE-MEASURES free space before Phase 0. On (b): re-run `boot/disk_forecast_d13.py` with the new F0. On (c): nothing. The advisory freeze does NOT block it (it deploys an already-merged develop).
1. `inbox_digest.sh --inbound` WHOLE, + `--all` for `[QUESTION]` rows in the last 12 h, each matched to a later ANSWER. Bodies are fetched by message id and saved to `fleet/briefs_staged/`.
2. **Morning ticket sweep + receipt** (the standing grant). Value first: kintsugi deployed + swept at d75bfe2 (night of 10-06); gate71 GO; the #1404 merge-in built and verified, held by the freeze; the KS-1436 ticket filed.

## MORNING SEAT — LIVE STATE (refreshed at the 51% checkpoint, 07:2x 2026-10-07)
- **Kam ruled BOTH cards (a)** at 06:46:01 / 06:46:04 (live board); reconciled, cards RULED. The FIRST ACTS above are DONE; do not re-raise them.
- **%73 Seat D 14th (`Secuura/Blockchain-D`), DEMO deploy of d75bfe2deb80.** Brief `fleet/briefs_staged/2026-10-07_seatD14_demo_deploy.md`; plan `…_seatD14_plan.txt` (read whole); **GO SENT 20:26:56Z** (`…_seatD14_GO.md`): Phase 0 re-tag 31 → `pre-20261006`, prove it + `pre-20260910` (33, 969f8db925918256) intact → ITEM 1b delete exactly 33 ids (`5_Project_History/2026-10-07_seatD-14th/boot/delete_cmds_d14.txt`; 38 tags) → settled re-read (< 16,174 MiB = STOP; projected 20,371) → rsync → **Gate B mail, HOLD**. NEXT for Wednesday: answer Gate B with a pane ctx read (< 50% builds), then Gate S (< 65% swaps), STOP 2-demo (pre-ruled: 038a only), Gate W (< 80% sweep). On DEPLOYED: report to Kam (October grant), then #1383 may merge (Q8).
- **%74 Seat G 3rd (`Secuura/Blockchain-G`), the advisory lock refresh.** Brief `…_seatDep_advisory_lock_refresh_3ghsa.md`; plan `…_seatG3_plan.txt` (read whole); **ANSWER 20:25:05Z** (`…_seatG3_ANSWER_plan.md`): ITEM 1 released (ticket, Urgent, board account, "Dependency and Version Currency"; worktree `s-g3-advlock`); method SURGICAL; a scratch-only overrides cross-check permitted (7 entries field-for-field). Targets shell-quote 1.11.0 / sdk 1.31.0 / pbkdf2 3.1.7 over 5 locks, 7 entries. Measured: pbkdf2 reaches 25 images, sdk the mcp-server image, root lock none. NEXT: its ctx mails (before the first lock edit, before the push, after the PR), then READY → commission a **T1 QA gate** (next number gate72) → GO `GO (Seat G 3rd): merge <PR#> on gate<NN>` → after the merge, develop moves: #1404's M is VOID, R 6th re-predicts with the gate71 kit.
- usage 97% (renews ~4d 5h); this seat's 100% row covers these seats. Ornith PAUSE to 06:00 10-08 (reason in the file). 
- OWED (tooling): `cockpit.sh say %<id>` printed nothing and delivered nothing; by pane NAME it works. Make it refuse loudly on an unrecognised pane.

## STATE AT THE WRAP (05:3x)
- **develop = b39051390ff6** (#1405, history.md only, on top of 40270d26 = Peter's KS-571 a-d, which REWROTE both platform docs as table matrices with a static guard `systemTest/__tests__/html_docs_matrix.test.sh`, and RENUMBERED the flow doc: tail 22 timings, 23 KS-571, 24 KS-1305). Re-read before anything; Peter merges at night.
- **#1404 (KS-1436, job-06 stderr fix): gate71 GO.** Merge-in **M = 7849f0a23d0609f618736c69a0a33a6a38c6f077** is RETAINED in `worktrees/s-ra4-ks1436`, UNPUSHED. tree(M) = d717255d5376 == T; qm 8/8; the mergein script's record is "first run FAIL 44 of 45 → F-6 (its own added gate) → corrected → standalone PASS" (ruled: keep M, no reset). The **16:20:45Z GO** (`fleet/briefs_staged/2026-10-07_seatR5_GO_1404.md`) STAYS VALID for the next R seat ONLY while develop == b39051390ff6. If develop moved, T is VOID: re-predict with the gate71 kit before any push.
- **#1398 (KS-1136): CONDITIONAL GO**, only after #1404 lands, flow `28.`, re-predicted on the REAL post-#1404 develop with its own qm (ruling W-Q8). Kit prediction 960e71800ea1 is on a SIM base.
- **PRs 3-5 UNRAISED** (KS-998 `29.`, KS-1313 + KS 1326 `25.`, KS-1164 `26.`), RAISE_BASE ruled = live develop (b39051390ff6). All strict-apply. **Q-A owed:** KS-1313's board-account assignment at PR 4 open (third seat to carry it).
- **R 6th** (when the freeze clears): its brief is built from `5_Project_History/HANDOVER-seatR5-2026-10-06.md` (sha256/16 1492bb1a44ed13d4) + R 5th's brief (`fleet/briefs_staged/2026-10-07_seatR5_raise_prs3to5_and_merge_gate71.md`, its WEDNESDAY'S RULINGS section) + the GO. First act: re-read develop; push M only if develop == D AND legs 6/7 are green; then B5 squash; then #1398's GO; then the raises. R 5th's re-keyed tools (ra5 set + the four merge tools with required args) are in its record folder `5_Project_History/2026-10-06_seatR-5th/raise/`.
- **gate71 kit** `fleet/qa-agent/gatesets/2026-10-06_gate71/` (widened; RULINGS has every ruling). Report: `!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-06-gate71/report.md` (5cbc607a…). Its residue, NOT filed: N-1404-6 (job 06 "tested nothing" reads clean: KS-676 class), N-1398-3 (false cause text), N-1398-5 REPEAT, the aggregate.ts sibling; polish N-1404-3/-4. A board search comes before any filing.
- **#1383** (KS-1401, a docs PR, head 32e8459bc0f5) is held until D 13th DEPLOYED (Q8). If it lands first, #1404's T is void.
- Kintsugi DEPLOYED + SWEPT CLEAN at d75bfe2deb80 (D 12th, 10-06). Rollback `:pre-20261006`.
- Ornith PAUSE_QUEUE to 06:00 10-07 (lapses at the boot). Spark queue EMPTY; the job-06 PASS is consumed (#1404). **The morning seat re-screens for Spark briefs** (Kam 19:30: Spark on all tickets). Any PASS is held; raising waits for the freeze.

## FLOOR AT THE WRAP
%0 wednesday · %1 monitor (D 13th wrapped 05:3x, pane closed). Orphaned DETACHED watchers of wrapped seats F 3rd, E 7th and F 4th were also found and stopped by Wednesday (pids 12127/41307/89913, identity by command line; `inbox_watch` count now 0). No subagents running. R 5th's detached watcher was stopped by Wednesday (pid 22699, identity by command line).

## BUDGET
7d gauge 95% at 05:1x; Kam's 19:30:43 grant lets THIS seat run to 100% until the renewal (~Sun 11 Oct), shaped as card (a): Spark on all tickets, raise/gate/merge/deploy seats only, at most two deployers. **A dependency seat (advisory card (a)) is a BUILD seat, so it needs his tap on that card; the card says so.**

## OWED (Wednesday's own)
- ~~Card for Kam (D 13th's two-history.md finding)~~ DROPPED 2026-10-07 06:06 by the morning seat: the repo copy is PETER's project history (#1405 merged by PeterObeden; last 6 commits author `t`, +0100), the root copy is ours by the layout. Two owners by design, no decision for Kam. Reason in the 10-07 note.
- **Mechanism (four orphaned watchers in one night):** `pane_close.sh` should list the seat's DETACHED `inbox_watch*` processes by its record-folder path and stop them (or refuse until stopped). Today it checks listeners only.
- **Watcher: the "turn ended on an announced next step, nothing running" STALL** (THREE instances in two nights: R 4th, D 12th, R 5th). Promote from candidate to a watcher leg: flag a turn whose last line announces work, with no background job live, as a STALL, not a hold. Claim with Tuesday first (shared tooling).
- Residue cards for Kam (not urgent, after the demo deploy settles): demo's admin seeding protected by ONE variable (NODE_ENV=development, userRepo.ts:1234); GATEWAY_VOUCH_SECRET absent on demo (fail-open).
- `safe_push.sh:108` and `wed_claim.sh:54` still `rebase --autostash` internally.
- A send_brief check flagging "nothing else" near a tool path (ledger w=4); hold_ready.py `--model-tag` for bash_patch.
- Tuesday owes (her pickup) the send_brief.sh `[Wednesday -> …]` prefix fix; she claims it with Wednesday first.

## OWED (board-pass list, unfiled)
- namecheck's +8 subject gate refuses 85-92 char subjects.
- history.md's stale D 10th and R 3rd handover shas (the files were edited after the history entries).
- BACKLOG.md lacks the CI findings.
- The 6 shell suites red on CI, green in-hook.
- 11 overlapping lockfile PRs.
- `dev-reload.sh:73` UTF-8 unbound variable.
- KS-729 past due.
- Signatory routes' org-membership check.
- `--no-optional-locks` stale-stat blindness.
- Leg-6 CLEANUP advisory: 15 stale baseline rows (12 KS-470, 3 KS-559).
- `git for-each-ref` `*` does not cross `/`: STANDING_LINES candidate.
- gate71 residue: Q1 (persisting unreadable artefact exits 0 on run 2), Q3 (`ci/aggregate.ts:241-243` skipping unparseable).
- `tmux display-message` without `-t` returns the active pane: six recurrences across seats, a tool default that is wrong.
- KS-1422 stale origin/develop. Ledger w=4: a mechanism for "ruling on a seat's tool unread".

## STANDING NOTES
- Pathspec-only commits; pull with `tools/safe_pull.sh`. decisions.json and the chat stores are STATE.
- A seat CANNOT read its own context: gates are mail handshakes, and Wednesday reads the pane.
- Receipts quoting a send's output are written AFTER the output is visible. Close a gate's pane on reading its verdict. Quoted heredocs only (inject live values by sed afterwards).
- Before any GO, open the brief's GO section and copy its required shape.
- A develop move is identified in Wednesday's OWN scratch clone, never by a write verb in the project checkout.
- After a pane close, check the seat's watcher: a detached one (tty ??) survives and stays keyed to the pane NAME.
