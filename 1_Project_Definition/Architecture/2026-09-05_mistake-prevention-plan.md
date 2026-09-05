---
date: 2026-09-05
type: plan
source: Kam, 16:4x — "Tell me if you have any ideas to prevent these types of mistakes in the future. if so, let's put a plan together to improve the system as constant improvement is a high priority"
status: proposed — items 1–2 BUILT 16:4x, the rest for Kam's word at the next consolidation or sooner
---

# Mistake-prevention plan — what today's ledger says, and the mechanisms that answer it

## BLUF
Today's 15 corrections sort into three classes, and the biggest one has a mechanical fix that is already built. **Class A (5 of 15): Kam's word not surviving a coordinator rotation as a rule** — the extranet re-ask, the Peter test blocks said three times, the Founders Hub credit raised four times. **Class B (6 of 15): a fact composed from a nearby text instead of read** — a diffstat read as file status, a tree called "not clean" unread, a brief narrower than its ticket. **Class C (4 of 15): a tool contract or shell idiom used from memory** — `cd` at the head of a command, `timeout` on macOS, a kill list from a parent walk. The decisions held in every case; what drifted was bookkeeping, and every class already has a gate that catches part of it. The plan is to move each remaining gap from "remember" to "in the path", and to measure the catch rate by who caught it at every weekly consolidation, with Kam-caught → 0 as the target and agent-caught kept (that is the loop working).

## The mechanisms, ordered by leverage

| # | Class | Mechanism | State |
|---|---|---|---|
| 1 | A | `decision_queue.sh add` REFUSES a card whose subject Kam has already written on the panel, printing his words; `--override-prior-rulings` records the override | **BUILT + exercised 16:4x** (refuse / pass / override) |
| 2 | A | `tools/kam_rulings_today.sh` — every Kam panel message of the day, verbatim, read at boot after the brain load and at every checkpoint; the launcher's boot prompt names it | **BUILT 16:4x**; first run surfaced a ruling this seat had missed |
| 3 | A | "Said once → a rule": the rulings extract flags lines containing *rule / every time / going forward / always / never / don't forget*; the checkpoint ritual files or discards each flagged line in the same action | Proposed — one grep in the extract + a checkpoint step; ~20 min |
| 4 | A | Fewer rotations: the boot costs ~27 points (digest 246 KB + ledger 274 KB); five seats today. Options: (a) ledger window 3 → 2 days (≈ −5 points per boot, measured on today's file sizes); (b) keep the window, move rows with w=1 that never recurred to the archive at consolidation | **Kam's ruling** — the 3c window is his rule; numbers at the weekly consolidation |
| 5 | B | `send_brief.sh` refuses a queued ticket id whose provenance line lacks a `scope:` clause, and refuses a repo/PR reference outside the addressed `<Client>/<Project>` unless the client CLAUDE.md declares the pair (the w=2 candidate from today's validate-brief-pointers extension) | Proposed — ~40 min in the gate; promotes at w=3 anyway |
| 6 | B | The brief template's TARGET line carries `porcelain read at HH:MM` or `unread` — a characterisation of a tree cannot be typed | Proposed — template edit, 5 min; ledger w=89 status column already names it |
| 7 | C | The pretooluse hook gains `timeout` beside `cd`; `pane_close.sh` already refuses pid 1 and tty listeners; a `kill_by_port.sh` helper (port + cwd, `${PID:?}`, pid 1 excluded) replaces ad-hoc kill lists | Proposed — hook clause 5 min; helper ~20 min |
| 8 | all | Weekly consolidation reports the catch rate BY CATCHER (Kam / agent / self / hook) as the KPI, alongside boot cost; Kam-caught → 0 is the target, agent-caught is kept | Proposed — a script over the ledger (the 16:43 measurement is the prototype) |

## What is NOT proposed, and why
- **Not** "the coordinator holds more in memory." Memory is where every class-A miss lived. Each mechanism above is a read or a refusal in the path.
- **Not** fewer agents or slower work. The rate scales with volume (93 panel messages, ~45 fleet mails in 40 minutes today) — the fix is gates that scale, not throttling (Kam, 2026-08-17: separate the surfaces, never throttle the work).
- **Not** trusting the fleet less. The agents and testers caught 5 of today's 15 before any cost; that culture is the detector and it is rewarded, not tightened.

## Sequence
1. Done today: items 1–2. Launcher line in at this seat's wrap.
2. This weekend's consolidation (first session after Sunday): items 4 and 8 with numbers; Kam rules the ledger window.
3. Next week, first quiet seat: items 3, 5, 6, 7 — each exercised both ways before arming, per the 08-06 rule.

## Provenance
- Today's rows and classes | `0_Brain/learnings/_ledger.md`, rows dated 2026-09-05 (15 incl. the 16:4x re-raise row); the 16:43 measurement (5 Kam / 5 agent / 4 self + the re-raise) | read 2026-09-05 16:4x
- Boot cost | this seat's statusline: 16% → 27% across the ledger read; digest 245,951 B, ledger 273,963 B at boot | read 2026-09-05 16:0x
- Kam's rules cited | `learnings/2026-08-17_conversation-needs-a-stable-panel.md` (never throttle), `CLAUDE.md` rule 3c (the ledger window), `learnings/2026-08-06_exercise-mechanisms-before-arming.md` | read 2026-09-05 16:0x
