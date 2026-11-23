---
date: 2026-11-23
type: reference
source: in-session design drafter for Friday; read-only (files in this folder, CoAgent repo at 3768a67 by git show, CLARIFICATIONS.md, daily notes); nothing run, nothing changed
status: DRAFT, for Friday; no card posted
project: General/Claude to Claude (CoAgent), no client
---

# CoAgent: the two modes, "allow and monitor" and "approve and monitor"

**Friday's notes on this draft (read whole by Friday, 2026-11-23; carded as `general-c2c-allow-mode-meaning-1123`):** two lines of section 3 were already out of date when written. (1) "approved three times" is the owner's own count at one point of the session, not a measurement: the Mac host's log of that session holds 5 gate-ask lines and 2 hand-out lines (counted by the build seat and by the independent check of the findings lane). (2) The PC's report of that session HAS since been read whole by Friday (`windows/2026-11-23_WO-14_4_results.md`): one run, the agent's own report names the loader once and the send and wait tools twice each, the working folder was empty after it and the settings checksums identical. Neither changes the note's argument. The recommendation in section 4 is the drafter's; Friday put it on the card as her own recommendation after reading the note.

Tags: READ (path:line) = read in that file; REASONED = the drafter's argument; UNVERIFIED = no source read. Repo paths are at commit 3768a67. "03", "11", "12" are the files of those numbers in this folder.

## 1. BLUF for the owner
- You said the final product has two modes: allow and monitor, approve and monitor.
- "Approve and monitor" is the CONTROLLED mode. It half-works today: your terminal asks, but nothing records or shows a history.
- "Allow" has two separate designs (trust grants; "both agree"). Neither is switched on anywhere.
- "Monitor" (a live view plus a kept record) is designed twice and built nowhere.
- One question: is "allow" one mode that merges the two designs, or one of them?

## 2. His words, in date order (copied from the sources)
1. 2026-08-21 19:49, `1_Project_Definition/Discovery/00_prompt-log.md:1175`: "A) everything is permission-based so nothing is done without express permission; and B) the administrator on the other side would be able to see everything that's done and, in most cases, approve calls, actions, or commands." READ
2. 2026-11-16, `00_prompt-log.md:2831`: "Once connected, there should be 2 modes 1)controlled.  Under this mode, the user should be able to monitor every file, folder or service that is being interacted with and approve it. [...] 2) option 2 is approvewd trust.  Once trust is given, the user gets to follow what is going on but no longer has to approve things.  The user should always be able to jump in and pause, ask questions or revoke approval." READ
3. 2026-11-17, `05_kam-rulings-2026-11-17.md:21`: "Keep it: every terminal command asks". `:37`: "for the above, change - same rules as mac". READ
4. 2026-11-18, `daily_friday/2026-11-18.md:69`, note on card policy-worktree-and-remote-agent: "yes but there should be an option to bypass permission." READ
5. 2026-11-18, `daily_friday/2026-11-18.md:97`: "what I meant by bypass permission.  the same setting as in claude.  if both users agree to let the agents work, monitoring but no approval for any aciton necessary" READ
6. 2026-11-20, rulings on design 11 (`12:30`): D1 "a — Yes, they all still hold"; D2 "a — Only with the sandbox on"; D3 "a — Every member, observers included". READ (as quoted in 12 and `13:317`; the board message itself NOT READ)
7. 2026-11-23 10:24, `coagent/1_Project_Definition/CLARIFICATIONS.md:6-10`: choice "c — Skip all prompts" (dev test agent on his PC) and "This is an acceptable risk during development.  Naturally, the final product will have the two modes we discussed - allow and monitor, approve and monitor" READ

## 3. What exists today, per mode
| Mode | Designed | Built (code that a running product calls) | Shown working end to end |
|---|---|---|---|
| CONTROLLED ("approve and monitor") | `03:245`, `03:276-287` (held requests, every action asked, real diff, 5-min expiry) | Policy decision core: `docs/POLICY.md:37-113`, called by the preview gate: `docs/DAEMON.md:802-818`. NOT built: session binding, held requests, the daemon learning the answer, session approvals, audit log, PostToolUse capture, console (`docs/DAEMON.md:913-918`). Approvals appear only as Claude Code's own prompt (`docs/DAEMON.md:810-811`). READ | Partly. 2026-11-23 11:34 the Mac host ran GATED; the owner "approved three times (the read and two sends)" in Claude Code's prompts (`daily_friday/2026-11-23.md:44`). That is "approve" with no monitoring view beyond those prompts: no record, no history pane. READ |
| APPROVED TRUST (scoped, time-limited signed grant) | `03:289-339`; M4 row `03:919` (grants, live stream, revoke, presence) | Grant check in the policy crate only: `docs/POLICY.md:103-107`; signature check is the caller's (`:25`). The daemon has no grants: "session approvals and grants" are "Not in the preview" (`docs/DAEMON.md:915-916`). A grant never allows a shell command (`docs/POLICY.md:699`, `06:570`). READ | No. Nothing issues, stores or shows a grant. READ |
| "Both agree" (approvals off, everyone agreed) | `11` whole; monitoring `11:197-213`; review `12` (6 Blockers, `12:7`, `12:97`) | Policy steps [7c]/[7d] SHIPPED DARK: "nothing in the tree builds a `BypassView` outside this crate's tests" (`docs/POLICY.md:64-93`). Dark "holds by usage only" (`BACKLOG.md:930-933`). No rounds, consents, leases, console, stream (`12:259-270`). READ | No. READ |
| Dev set-up of 2026-11-23 on the PC ("allow" with NO monitoring) | Not a product mode; allowed by C-1 for development only | The Windows daemon refuses `--gate`: "nothing on this machine is then checked by CoAgent" (`docs/DAEMON.md:669-671`; `BACKLOG.md:1022-1025`). The agent ran "skip-permissions" (`daily_friday/2026-11-23.md:44`). READ | It ran; nothing in CoAgent recorded or streamed what that agent did. The PC's own report and agent log are "NOT YET READ" (`daily_friday/2026-11-23.md:44`). READ |

## 4. Candidate readings of "allow and monitor"
**A. "Allow" = the both-agree mode.**
- User: every person in the session agrees, by console and spoken words; on every machine approval cards stop; everyone watches one live stream and anyone can switch it off at once (`11:21-27`).
- Reuses: the dark policy steps [7c]/[7d] and their tests (`docs/POLICY.md:64-93`).
- Needs: everything in `12:259-270` (daemon rounds and leases, console, scanner, audit wiring, session binding, U-B1 measurement), a revised design 11 (`13:110`), answers to Q-1 to Q-11 (`12:278-288`; 11 counted).
- Main risk: a peer's text steers the agent to delete, push or send with no card (`11:405`, R-B1); a user may read "refused" as "my files are safe" when only listed credential and gate paths are protected (`docs/POLICY.md:776-777`).
- Review found: all six Blockers apply. F-1 inbox unreadable in the mode (`12:101-104`, still OPEN: `BACKLOG.md:925`), F-2 every send refused, F-3 excluded files readable by a recursive search, F-4 deputy admission, F-5 clocks, F-6 the sandbox tick nobody checks (`12:106-141`).

**B. "Allow" = approved trust (scoped, time-limited grants).**
- User: the owner picks a preset (read-only audit, workspace developer, ...) for 60 minutes (max 8 h); in-scope file actions run and appear in the stream; anything outside the scope, and the always-ask class, still asks (`03:315-318`).
- Reuses: grant checking in the policy crate (`docs/POLICY.md:103-107`, `:709-711`).
- Needs: the whole M4 row (`03:919`) plus the console (M3, `03:918`); no group consent; the peer's agreement plays no part (`03:337`).
- Main risk: since every shell command asks under any grant (`06:570`, `06:574` "In-scope actions flow" means file-tool actions only), trust removes few cards in practice: most real work arrives as shell (`06:574`). A user may feel "allowed" while still clicking much. REASONED from those lines.
- Review: design 12 reviewed design 11 only; nothing in 12 is a finding against grants. The grant design has had no independent review that the drafter read (UNVERIFIED either way).

**C. One "allow" mode: the scope is a grant, and everyone in the session must agree before it starts (A and B merged).**
- User: one dialog; the owner sets how far "allow" reaches (a preset up to "everything except the always-refused list") and the time limit; every member agrees; then the same stream, Pause, Stop, Revoke for all.
- Reuses: grant scopes and limits (`docs/POLICY.md:103-107`), the dark refused-class list for the widest scope (`docs/POLICY.md:71-84`), design 11's consent and lease ideas.
- Needs: a new short design that merges `03 §5.3` and `11 §2`; still every prerequisite of A for the widest scope; grants for the narrow ones.
- Main risk: the most to build before anything works; and any absent member (an observer with a closed laptop) blocks or ends it for everyone (`12:205`, F-17).
- Review found: F-1 to F-6 apply to the widest scope as to A; narrow scopes inherit F-17. REASONED.

**Drafter's recommendation (label: the drafter's, not ruled).** C, built in two steps: first the narrow, grant-scoped "allow" for one machine's owner (B's mechanics, which need no consent rounds), then "everyone agrees" plus the widest scope once design 11 is revised. Reason: his 16 Nov mode 2 is a grant given by "the user" and his 18 Nov words add "if both users agree", and only C keeps both; two allow modes would mean two monitoring designs, which is exactly what is missing today. REASONED.

## 5. What "monitor" must mean in BOTH modes (checkable list)
| # | Requirement | Status |
|---|---|---|
| M1 | Every file, folder, service and command the agent touches is shown, with what was decided and why | RULED in words: "monitor every file, folder or service" (`00_prompt-log.md:2831`). Designed `03:318`, `11:201`. Unbuilt. |
| M2 | Shown live, as it happens, not only afterwards | RULED in words: "follow what is going on" (`:2831`). Designed `03:318`. Unbuilt. |
| M3 | The other side's owner sees it too | RULED in words (Aug): "the administrator on the other side would be able to see everything" (`:1175`). Designs differ: `03:347` default "summaries"; `11:204` at least summaries in the mode. OPEN: "everything" vs "summaries" by default. |
| M4 | A kept record, signed, checkable later | Designed (M2 audit chain `03:917`; `11:217-237`). Audit crate exists, not wired into the daemon (`docs/DAEMON.md:916`). |
| M5 | How long it is kept, and what happens when space runs out | Ruled: "Fixed capacity now, seal and continue as the next piece" (`05:55`). Retention period OPEN. |
| M6 | The result of each action (exit, size, output) | Designed `11:201`; needs PostToolUse capture, unbuilt (`docs/DAEMON.md:916`). |
| M7 | Pause, Stop, Revoke, ask a question, jump in | RULED in words: "always be able to jump in and pause, ask questions or revoke approval" (`:2831`). Designed `03:320-323`, `03:343-346`. Policy has stop/pause steps (`docs/POLICY.md:43-44`); the hold and queue are the caller's (`:27-28`); no console. |
| M8 | When the viewer is away | Designed: pause after 10 minutes (`03:324`, `11:210`). Pause vs end OPEN (I-B8, `11:341`). Unbuilt. |
| M9 | The view never enters the agent's own context | Designed `11:201`. Unbuilt. |
| M10 | One monitoring design shared by both modes | OPEN: no document defines it (`19:32`). |
| M11 | Whether an unmonitored "allow" (like today's dev PC) may exist in the product | OPEN. C-1 limits it to development (`CLARIFICATIONS.md:10`). |

**What monitoring CANNOT promise with the product as it is (READ):**
- It shows what the gate saw, not everything the machine did. A hand `send` passes the gate: any same-user program can send as this device with no ask (`docs/DAEMON.md:853-861`; `BACKLOG.md:1136`).
- Unread peer text sits in clear in `inbox.json` until released (`docs/DAEMON.md:862-865`; `BACKLOG.md:1141`).
- The read witness can be used by another same-user client inside its time window (`docs/DAEMON.md:848-851`).
- Shell text is opaque: the view shows a command's text, not what it did (`docs/POLICY.md:756-759`, `:763`).
- On native Windows today nothing is checked or shown (`docs/DAEMON.md:669-671`).

## 6. Windows
Today, under every reading, the Windows daemon refuses the gate, so nothing is checked, allowed, asked or recorded by CoAgent there (`docs/DAEMON.md:669-671`, `BACKLOG.md:1022-1025`); a seat is building the blocking test for the Windows hook now (W-GATE-TEST, `daily_friday/2026-11-23.md:47`). Once a gate exists there, every PowerShell command asks as on the Mac (`05:37`, `06:570`), and native Windows has no sandbox (`11:171`, `docs/POLICY.md:763`), so under A or C a shell command never runs approval-free there (`docs/POLICY.md:86-91`); under B grants never cover shell anyway. So on Windows "allow" would cover file tools only, under every reading. REASONED from the cited lines.

## 7. Card draft (not posted)
**Title:** CoAgent final product: what "allow and monitor" means

**BLUF (88 words, counted with wc -w):** You said the final product has two modes: allow and monitor, approve and monitor. "Approve" is clear: the controlled mode. "Allow" has two designs on file: time-limited trust you give for your own machine, and "both agree", where everyone in the session switches approvals off. They differ in who must agree and in how much they allow. Monitoring (a live view and a kept record) is designed twice and built nowhere. Which should "allow" be? Nothing is built from this answer yet; it decides the next design note.

**Options:**
- a: One allow mode: you set how far it reaches and for how long, and everyone in the session agrees before it starts.
- b: Allow means "both agree" only: approvals off everywhere, everyone agrees; trust grants are dropped.
- c: Allow means trust only: each owner allows a chosen scope on his own machine, nobody else agrees; "both agree" is shelved.
- d: Keep both as two kinds of allow.

**Drafter's recommendation:** a, built narrow first (one owner's scoped allow), group agreement and the widest scope second.

**Default if unanswered:** no mode work starts; the three designs stay as they are; Friday drafts the shared monitoring design (words only, section 5 list) since every option needs it; the Windows gate test continues.

**Premises and sources:** his words (section 2, items 2, 5, 7); three modes defined, no mapping (`19:25,31`); grant check and both-agree steps exist only in the policy crate (`docs/POLICY.md:64-107`); daemon has no grants, console or audit log (`docs/DAEMON.md:913-918`); 6 Blockers on both-agree (`12:7`); shell never auto-allowed by a grant (`06:570`); Windows has no gate (`docs/DAEMON.md:669-671`).

## 8. If he answers X
- **a:** a merge design note (M): one dialog, one consent rule, scope presets up to the refused list, one stream. Must prove: the narrow step needs no consent rounds; F-1 to F-6 are closed for the widest scope. Then the shared monitoring piece (L: audit wiring, PostToolUse, console stream).
- **b:** revise design 11 against F-4, F-5, F-9, F-11, F-12, F-14 (`13:110`) and get Q-1 to Q-11 answered (M); mark grants retired in 03 (S). Must prove: inbox and send work in the mode (F-1, F-2).
- **c:** shelve design 11 and decide what happens to the dark steps (S); grants and console per M3/M4 (L). Must prove: Revoke takes effect on the next call, walking away pauses (`03:919`).
- **d:** a short note that defines one shared stream and record for both (M), then both build paths (L, L).

## 9. NOT READ / NOT ESTABLISHED
- `docs/POLICY.md` read in parts (lines 1-262, 448 area by search, 673-712, 754-797), not every line of §4 to §9. `docs/DAEMON.md` read §8 and §6a parts only. `BACKLOG.md` by search.
- Design 03 §6.6 (surfaces), §5.5 beyond line 347, designs 04, 07, 08, 09, 10, 14-18: not read.
- The owner's 2026-11-20 board messages at source; the PC's WO-14 report and agent log.
- Whether the policy grant code has had an independent check; whether seal-and-continue is merged to main (`13:101` says "built, in check" on 20 Nov).
- Stale or differing lines, both recorded, not reconciled: `docs/POLICY.md:204-205` (3768a67) says the bypass note "has been asked and not answered"; `daily_friday/2026-11-18.md:97` records his answer (older date, but the repo line is the later text). `13:130` says L1 closes the two `KNOWN_TOOLS` entries; `BACKLOG.md:925` (newer) says they were withdrawn and F-1 stays OPEN.
- Whether a hook "allow" is silent in Claude Code without an allow rule (U-B1, `12:188-191`): unmeasured, and it decides whether any "allow" mode removes prompts at all.
