---
date: 2026-10-05
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE 2026-10-05 22:5x by seat 9a78af86 (53% checkpoint). Replace wholesale again; never stack.
---

# NEXT PICKUP

## 🔴 FIRST ACTS (65% checkpoint 23:3x AEDT 2026-10-05, seat 9a78af86)
0. `kam_rulings_today.sh` + `reconcile_rulings.py`. Kam silent since 20:07.
1. Read `inbox_digest.sh --inbound` WHOLE; full bodies via `inbox_digest.sh full <inbox> '<id>'`.
2. **develop = d784b613c81e** (#1388 KS-1404 squash, VERIFIED AT SOURCE by Wednesday: tree f65ddbbd560c, 1 parent 3cb93b9c731e). Present history tonight: #1384 232623892f24 → Peter's #1392 3cb93b9c731e → #1388 d784b613c81e.
3. **D 9th (%43)**: merged #1388; expect its follow-up ticket (N-1388-1..6, board account) + WRAP → verify handover hash, score, pane_close.
4. **F lane**: Kam's merge-order card satisfied. **F 4th LAUNCHED %47 12:40:04Z** — ITEM 0 owed (rule Q-AKTO yes, Q-1376 leave; its merge-in tree must be checked by Wednesday before push; GO string `GO (Seat F 4th): merge 1383 on gate61`). Brief was → `fleet/briefs_staged/2026-10-05_seatF4_successor.md` (#1383 docs-only merge-in, tree to Wednesday before push, GO `GO (Seat F 4th): merge 1383 on gate61`). If missing after a rotation, re-commission from `HANDOVER-seatF3-2026-10-05.md`. Read the brief WHOLE before `brief_and_launch.sh` (run it BARE — a `script -q` wrapper failed with tcgetattr tonight; the gate launcher needs `script`, brief_and_launch does not). The send gate needs a Linear provenance line for EVERY ticket id in the QUEUE.
5. **B 64th (%46)** launched 12:26:48Z: ITEM 0 owed (PR C KS-723 anchors-tx; #1393 merge-in on gate65's GO).
6. **E 5th (%45)** launched 12:04:53Z: ITEM 0 owed. Rule Q-1256-CLOSE (if a Redis close returns NULL, the close cell stays open under Kam's b → maybe a fresh card), Q-SEAT5, Q-WAIT5, Q-F5 (develop is now in the shared store).
7. **gate64 (%44)** on #1389: running the whole runner at the sim merge-in. On GO: launch **G 2nd** from `HANDOVER-seatG1-2026-10-05.md`; its merge-in tree re-predicted on the CURRENT develop (gate64's d1f3c5cb6c1c was on 3cb93b9c731e, now stale).
8. **gate65 kit drafter running** → `fleet/qa-agent/gatesets/2026-10-05_gate65/` for #1393 (B 63rd's KS-1278, head 4a1620588819). On kit: routing line (backup), dry run, launch under `script -q /dev/null`, rung 5.
9. **Spark**: queue empty. HOLDs awaiting a raise seat: KS-998, KS-1136, KS-1164, KS-1305, KS-1313 (reviews in run dirs). Tunnel re-opened 23:0x (`ssh -f -N … -L 47788:127.0.0.1:8888 Spark`); check /health first. Pool thin: carve tickets.
10. Read seat ctx only after `tmux resize-pane -t %NN -y 16`; then `tmux select-pane -t %0`. macOS has no `timeout`. The no-cd hook refuses `git -C $VAR <write verb>` → use literal paths for scratch-repo writes.

## SECUURA LANES
| lane | seat / pane | state | next |
|---|---|---|---|
| B | B 64th %46 | ITEM 0 | PR C; #1393 merge on gate65 GO |
| D | none (D 9th WRAPPED 0.95) | #1388 MERGED d784b613c81e | idle; owed: C6 image proof at the next kintsugi deploy; N-1388-2 doc sentence follow-up |
| F | F 4th %47 | ITEM 0 | #1383 merge-in → GO → merge |
| G | none; gate64 %44 | #1389 under gate | G 2nd on GO |
| E | E 5th %45 | ITEM 0 | #1385 merge-in → gate; KS-1256 b |
Scored tonight (this seat): E 4th 0.93 · B 63rd 0.95 · D 9th 0.95. E 5th %45 ITEM 0 ANSWERED 12:3xZ (re-predict on d784b613c81e; KS-1256 Redis-down = 503 ruled inside Kam's card, Kam told on panel).

## OWED (added this seat)
- Gate-kit defect (D 9th's finding): `c4_docs_gate63.py predict` on an ABSENT develop returns None for every blob → a false M6 "re-gate" refusal. predict must refuse "develop unresolvable" by name; carry into every new kit.
## RULES LEARNED TONIGHT (in STANDING_LINES / the ledger)
- Doc merge-ins: the cheat sheet has NO readable ordering invariant. **The target tree from a gate's key-anchored prediction is the authority**, never a div-anchored M1.
- A push is judged by the push tool's `.rc` file + `ls-remote`. rc 141 = KS-1149: retry under the lock, no transport change. A first push uses the seat's first-push tool.
- `git fetch --dry-run` writes the shared store; signal harnesses run in the FOREGROUND.
- A conditional GO states its act and no-act branches as two separate lines. Before sending, read the BLUF's order against the numbered list's (w=2 tonight).
- Name a seat's tool or flag only from its brief or `--help` (w=2 tonight).
- Gate-kit drafters' `_scratch/` dirs are now gitignored (gate63 left 1.4 GB).

## OWED
- Kam's three 20:06-20:07 rulings → tickets via a board seat (DECISIONS-24, last section; the #1245/#1278 pairing was corrected 20:3x).
- DECISIONS-24 queue (17 items: 4 Spark briefs, 12 Claude lanes, 1 board pass). Spark queue EMPTY; Kam's target is 50/day.
- Stale "Actions is retired" premise in Secuura's project CLAUDE.md (CI live and red; KS-1148 is Kam's). Tell Kam in ONE line next time he is on the panel.
- Tooling: the idle leg cannot tell an API-error stall from a waiting seat (two today); cockpit `say` with a pane id is a silent no-op; cockpit launch should tell a seat its pane name; 1-row panes defeat ctx reads.
- 136 ruled-but-undelivered cards (board-pass backlog). Ornith paused to 06:00; Ollama DOWN.
- Gate kits gate61r2 / gate62 / gate63 are untracked in git: commit them WITHOUT `_scratch/` (now ignored). Check `git status` sizes first.

## WITH KAM
Nothing waiting on him. The October deploy grant (kintsugi + demo) and the week instruction (to Sun 11 Oct) are live.
