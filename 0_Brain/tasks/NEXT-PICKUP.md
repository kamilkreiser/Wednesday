---
date: 2026-10-07
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE 2026-10-07 01:5x by the night seat (booted 22:4x on 10-06) at 78%, before its rotation. Previous copy in that session's scratchpad. Replace wholesale again; never stack.
---

# NEXT PICKUP

## 🔴 FIRST ACTS (in order)
0. `kam_rulings_today.sh` + `reconcile_rulings.py`. **OPEN with Kam (filed 01:4x): `secuura-demo-disk-retire-old-rollback-sets-1007`.** Rec (a): delete demo's `rollback-2026-09-03` (32) + 4 small sets (6), KEEP `pre-20260910`, tag a fresh set first, then deploy. (b) grow the disk. (c) don't deploy demo now. **Default: nothing deleted, no demo deploy.** Re-raise it in the morning brief.
1. `inbox_digest.sh --inbound` WHOLE + `--all` for `[QUESTION]` rows in the last 12 h, each matched to a later ANSWER. Bodies: fetch by message id from the AgentMail API and save to `fleet/briefs_staged/`.
2. **develop = 40270d263ab0** (PeterObeden merged #1400, #1401, #1403 and #1402, KS-571 a-d, 01:3x-01:4x). Identified in Wednesday's own scratch clone. 189 paths vs d75bfe2: systemTest 170, **BOTH platform docs rewritten as table matrices with a static guard (#1402)**, CLAUDE.md, .claude. **0 overlap with any raise product path.** Both live seats accept 8a8d7b96 and 40270d26 BY NAME; any other value is their STOP.

## 🔴 NEWEST (01:56): R 4th READY — **#1404 (KS-1436, job 06), head c117c0160684, END_TREE ec95d1995880, T2** → gate71 batched with #1398 (saved `fleet/briefs_staged/2026-10-07_seatR4_READY_1404.txt`, DKIM pass). PRs 3-5 UNRAISED → R 5th. Its merge-tree vs develop 40270d26 conflicts in the two platform docs ONLY. **Successor's first heavy act: WIDEN the gate71 kit** (add #1404 as T2, GO_WANT → R 5th, re-predict both docs merge-ins on 40270d26 under #1402's static guard), then launch it. R 4th now wraps cold: re-hash its handover, score it, `pane_close %69`.

## LIVE NOW (01:5x)
- **Seat R 4th (%69 `Secuura/Blockchain-R`, RAISE).** Row 06 = **KS-1436** (the job-06 stderr fix, filed, board account), commit c117c0160684 on RAISE_BASE d75bfe2. **Push RELEASED at ctx 43%** (14:37:25Z). Its pane read 46% later, past the 45% build line. Expect: raise of row 06 → a ctx-read request → answer "ONE READY with what is raised (row 06), then WRAP COLD". PRs 3-5 (KS-998, KS-1313 + KS 1326, KS-1164) then go to **R 5th** from its handover. Rulings it carries: Q-06N flow `27.`; Q-5D a 3-line WHY comment (disclosed amendment); the ks-1136 namecheck row DROPPED (it would have claimed R 3rd's #1398); told that every docs merge-in now needs re-composing onto 40270d26.
- **Seat D 13th (%70 `Secuura/Blockchain-D`, DEMO deploy of d75bfe2deb80).** STOP 1-demo answered 14:50:13Z. **HOLDING for Kam's disk card; NO GO sent.** On (a): send THE GO as its own mail, subject exactly `GO (Seat D 13th): deploy d75bfe2deb80 to demo`, body naming the card and the exact sets (rollback-2026-09-03 + rollback-2026-08-27-ks661, pre-ks488, rollback-20260901-prefix, pre-ks719; KEEP pre-20260910 + the new pre-<stamp>). On (c): tell it to WRAP COLD. Already ruled for it: Q3 auth released while ALLOW_DEFAULT_SEED_PASSWORDS stays empty (Wednesday read `userRepo.ts:1230-1232`); STOP 2-demo pre-approved (one migrations run, an `Applying 038a…` line, exactly 1 tracker row, then gateway 0/0); class-level error diff; demo-service excluded; ctx gates 50/65/80 by mail handshake (Wednesday reads the pane, `tmux capture-pane -t %70`).
- **Kintsugi DEPLOYED + SWEPT CLEAN at d75bfe2deb80** (D 12th, 0.96, wrapped). Reported to Kam. Rollback `:pre-20261006`.
- **gate71 (#1398 KS-1136 + R 4th's raises): NOT launched.** Kit `fleet/qa-agent/gatesets/2026-10-06_gate71/` (RULINGS_wednesday.md has every ruling). **On R 4th's READY, the kit must be WIDENED:** add row 06 (+ any 3-5 raised), GO_WANT → R 5th, doc check = unique + keyed (not ascending), **re-predict every docs merge-in on 40270d263ab0 under #1402's new static guard** (a docs-format re-composition, not a simple tail append), then launch. Merge order: row 06 (KS-1436) → #1398 → 3-5. #1398 must NOT merge before KS-1436 (Q2: job 06 would read HIGH on routine fallback runs).
- **#1383 is held** until D 13th's DEPLOYED (Q8).
- Ornith PAUSE_QUEUE to 06:00 10-07. Spark queue empty (the job-06 brief ran: PASS 7/7, held as `night/READY_KS-1136-06-TENANT-STDERR-OWN-FILE-1_spark-dsv4flash_…`).

## BUDGET
7d gauge 92% at 01:1x; Kam's 19:30:43 grant lets THIS seat run to 100% until the renewal (~Sun 11 Oct), shaped as card (a). Launches pass `WED_USAGE_STOP=100` naming the EXPIRING-GRANTS row. At this burn (~1.4%/h) the 100% ceiling is ~6 h away. **Spend only on: R 5th (raise), the gate71 widening + launch, the merge seat, D 13th.** Nothing else Claude-shaped.

## OWED (Wednesday's own)
- **Residue cards for Kam (not urgent):** (1) demo's admin seeding is protected by ONE variable: auth runs NODE_ENV=development, so the second gate (`ENABLE_DEMO_SEED`, userRepo.ts:1234) never applies, and setting ALLOW_DEFAULT_SEED_PASSWORDS=true suspends admin@secuura.com. (2) GATEWAY_VOUCH_SECRET is absent on demo (fail-open, as today). File both after the demo deploy settles.
- `safe_push.sh:108` and `wed_claim.sh:54` still `rebase --autostash` internally (shared tools). Until fixed, after either runs, read `git stash list` for a new autostash. **`safe_pull.sh` is BUILT and the no-autostash hook is armed** (00:0x).
- A send_brief check flagging "nothing else" near a tool path (ledger w=4); hold_ready.py `--model-tag` for bash_patch (it still writes the Ornith tag: rename by hand).
- **Watcher candidate (two seats, one night):** a turn that ends on an announced step with nothing running is a STALL, not a hold.

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
- Pathspec-only commits; pull with `tools/safe_pull.sh` (never a hand `--autostash`; the hook refuses it). decisions.json and the chat stores are STATE.
- A seat CANNOT read its own context: gates are mail handshakes, and Wednesday reads the pane.
- Receipts quoting a send's output are written AFTER the output is visible. Close a gate's pane on reading its verdict. Quoted heredocs only.
- Before any GO, open the brief's GO section and copy its required shape (subject vs body).
- A develop move is identified in Wednesday's OWN scratch clone (`clone --shared`, fetch by SHA from the GitHub URL with the checkout's core.sshCommand), never by a write verb in the project checkout.
