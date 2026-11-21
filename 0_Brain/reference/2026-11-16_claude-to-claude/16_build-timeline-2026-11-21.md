# CoAgent (Claude to Claude): build timeline and blockers, Sat 21 Nov 2026

From Friday, the laptop coordinator. Written 21 Nov at about 14:40. Every date below is an **estimate**: I sized each one from this week's real lane times, nothing more. I mark the shaky ones.

## BLUF

1. **Five lanes are in their final checks today.** Over the next 24 hours I expect four of them on main: the "approvals off" rules (kept switched off), the fix for the dead link after reconnecting, the Windows pipe security, and the kit that builds Windows programs on the Mac. The fifth, the audit log kept on disk, should follow by about Sunday midday.
2. **Windows first link: about Mon 23 to Tue 24 Nov.** That date assumes your machine report arrives and you can give 30 minutes at the Windows machine. The Windows background program starts building tonight.
3. **Agents talking Mac to Windows: about Tue 24 to Wed 25 Nov.** The permission gate on Windows: about 27 Nov to 2 Dec, and this is the shakiest date because the first Windows experiment could stop the plan.
4. **No decision of yours is open right now.** What I need from you is the **Windows machine report**, which is still outstanding, plus two half-hours at that machine. The full list is in section 4.
5. **Honest note: no work moved between about 08:20 and 14:20 today.** My seat ran out of Fable credit, and all five lanes finished and sat waiting on me. I'm on Opus now and they are all moving again.

## 1. Where we are (done)

| Phase | What it gave you | When |
|---|---|---|
| Design | Requirements, architecture, your rulings (docs 00 to 15) | 16 to 20 Nov |
| M0 experiments | macOS proofs that the hook can block an action | 17 Nov |
| M1 core | Background program, meeting point (relay), member list, signed audit log, deputy, seal-and-continue | 17 to 20 Nov |
| **Phase 1 preview** | **Two Claude Code sessions on one Mac send each other requests through the gate; the denied step provably does not run** | **On main 20 Nov** |
| Member-list settle (your D-2 = a) | Your next change settles anyone your deputy let in | On main 20 Nov |

## 2. This round: the five lanes in final checks

| Lane | What it does for you | Where it is now | Expected on main |
|---|---|---|---|
| **Relay reconnect** (you're waiting on this) | Restart the host and the guest reconnects by itself. The fix also stops a fast new invitation from landing on a dead link | Fix round done, every test green. Independent re-check started 14:24 | **Tonight, about 19:00 to 20:00** |
| **Approvals-off rules** (policy mode) | The rules for "approvals off" exist and are tested but switched off. Your ruling b: the one known gap is written down | My own clean-copy check started 14:28 (about 2 hours) | **Today, about 17:00** |
| **Windows pipe security** (win-ipc) | The Windows side refuses an impostor server. Written and type-checked; it cannot run until it reaches your Windows machine | Fix round done. Independent re-check started 14:27 | **Tonight, about 21:00** (it merges after relay reconnect) |
| **Windows build kit** (w-kit) | The Mac builds the Windows `.exe` files, so your old machine only runs finished programs | Built, with the cache folder you granted. Its check is next | **Tonight, about 20:00 to 22:00** |
| **Audit log on disk** (audit-host) | The signed log survives being stopped at any moment and gets filed away. Not yet connected to a live session | Your 'a' ruling applied: one fix round for 3 faults, then a short re-check | **About Sunday 22 Nov, midday** (it merges after the two Windows lanes) |

If a re-check fails a **second** time, I don't run a third round. It comes back to you as a card.

## 3. What comes next, in order

### 3a. Windows (your priority since Fri 18:49), route C

| Stage | What you would see | Work | Estimate |
|---|---|---|---|
| W-DAEMON lane | The background program builds and type-checks for Windows | Starts when relay reconnect and win-ipc are both on main (tonight). About 12 to 20 agent-hours including its check | **Ready about Mon 23 Nov** |
| **C1: first link** | Copy one small file to the Windows machine and type one command; the Mac shows "connected". No AI on Windows yet | **Your 30 minutes at the machine** | **Mon 23 to Tue 24 Nov** |
| **C2: agents talking** | A Claude Code session on Windows and one on the Mac send each other a request and a reply. Windows side not gated by us yet (your Q1 answer = a) | 2 to 4 hours, mostly at the machine; **your 30 minutes again** | **Tue 24 to Wed 25 Nov** |
| **C3: gate on Windows** | Every action on Windows is checked too | 15 to 30 agent-hours plus several sessions at the machine. **The first Windows experiment (W1) can stop the plan**; if it fails, WSL becomes the fallback | **27 Nov to 2 Dec (low confidence)** |

Native Windows has no Claude Code sandbox. Even with our gate there, an approved command on Windows can do anything your account can.

### 3b. Finishing M2, "the gate, controlled" (the milestone where Sam asks, you approve each step, one step is denied and provably does not run, and the audit log verifies on both sides)

| Lane | What it adds | Estimate |
|---|---|---|
| Spikes, roster notes, preview tidy | Six measured answers about Claude Code, the deputy's loose ends tidied, and a demo that runs from any folder | Small; fits in the gaps next week |
| Gate-bind | Only linked sessions are gated, and the cards tell the truth | About 1 to 2 days, after relay reconnect |
| Audit wiring + `coagent audit verify` | The live session writes the log and you can verify it | About 2 to 3 days, after audit-host and gate-bind |
| Share scanner | Outgoing messages are scanned for secrets instead of asking every time | About 2 days |
| Deputy wiring | The deputy works in a live session | About 2 days |
| **M2 acceptance** | | **About 7 to 12 Dec (low confidence)** |

### 3c. After M2 (not sized yet; rough guesses only)

- **M3, browser console:** an approval queue, chat dock, and Stop/Pause buttons. About 2 to 3 weeks.
- **M4, trust grants:** allow something for a period, live stream, revoke. About 1 to 2 weeks.
- **M5, release:** packaging, `coagent doctor`, soak test, private beta. About 2 to 3 weeks. **The earliest realistic private beta is late January 2027.** I'll size M3 to M5 properly once M2 lands.

## 4. Blockers and what I need from you

**Needed now:**
1. **The Windows machine report.** Run `Launch_Friday_Windows.cmd` (on your board's file drawer since 20 Nov) on the Windows machine and send me the `machine-report.md` it writes. Windows version, processor, memory and whether WSL is there are all unknown, and C1 can't be scheduled firmly without them.

**Needed later (I'll ask on a card when it's due, not before):**

2. **About 30 minutes at the Windows machine** for C1 (about Mon/Tue) and again for C2.
3. For C3: your OK for model runs on the Windows machine (experiment W1), a yes or no on installing Git for Windows there, and a **second Windows user account** for the "another user cannot get in" test.
4. Later decisions, not yet due: the eleven "approvals off" questions (doc 12, once that design is revised) and which outside connection service to use. Neither blocks anything this month.

**Risks I'm watching:**
- **Usage:** weekly usage reads 69%. New agent launches stop at 90% until the reset, which would slow everything above.
- **Heavy runs:** three test suites at once is the machine's limit, so merges queue behind each other. That's built into the dates.
- **Coordinator gaps:** today's six-hour stall. I'm now on Opus as you asked, and I only flag Fable if a job needs it.

## Sources

- Round plan: `0_Brain/reference/2026-11-16_claude-to-claude/13_next-round-plan-2026-11-20.md` (lanes L1 to L11, M2 to M5 from design 03 §12).
- Windows plan: `…/15_windows-plan-2026-11-20.md` (route C, stage sizes in its BLUF item 5, spikes W1 to W6).
- Lane states: the five STATUS files in the project's `5_Project_History/`, read 14:21 today. Branch heads by `git ls-remote` at 14:23.
