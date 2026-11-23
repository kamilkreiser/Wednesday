---
date: 2026-11-23
type: reference
source: in-session design drafter for Friday; read-only (files 03, 05, 06, 11, 12, 19, 20 in this folder; CoAgent repo at 3768a67 by git show; p1p_review/live_demo_report.md and c2_session_2026-11-23/mac_host.log by search); nothing run, nothing changed
status: DRAFT, for Friday; no card posted
project: General/Claude to Claude (CoAgent), no client
---

# CoAgent: the two modes (ALLOW, APPROVE) and the two views (CONVERSATION, LOCAL ACTIVITY)

**FRIDAY'S RULINGS ON THIS DRAFT (read whole by Friday, 2026-11-23; coordinator's design rulings, nothing built from them yet; each can be changed by the owner's word):** P1 YES (every session starts in APPROVE). P2 YES (the switch to ALLOW needs an act the agent cannot perform; the surface is chosen after measurement M7). P3 YES. P4 YES. P5 YES (back to APPROVE by one owner command; the agent never changes the mode either way). P6 YES. P7 YES. P8 YES (never read from disk). P9: the notice's WORDING is the owner's experience and so his: variant 2 is Friday's recommendation, shown to him with the first on-screen build, not shipped as final. P10 YES (LOCAL ACTIVITY never enters the shared audit chain). P11: attack classes only (the safer of the two). Q2 (owner away while on ALLOW): keep going, from his own words "lasts the entire session"; Friday's reading, told to him, his to correct. Assumption A-ii (terminal commands in ALLOW) and Q1 (does the other side see the chosen mode) are carded for the owner: `general-c2c-allow-terminal-commands-1123` and `general-c2c-mode-visible-to-peer-1123`. Section 7's measurements are commissioned as lane L0 (brief `2_Project_Files/friday/briefs_drafts/2026-11-23_coagent_ALLOW-MEASURE_brief.md`). The four lines of his in section 2 were compared by Friday with the board by program when they were recorded (see the daily note of this date).

Tags: READ (path:line) = read there; REASONED = the drafter's argument; UNVERIFIED = no source read; PROPOSED = a behaviour the drafter had to pick (all collected in section 9). Repo paths are at 3768a67. "03", "11", "12", "20" are files of those numbers in this folder.

## 1. BLUF for the owner
- You ruled: each owner picks ALLOW or APPROVE for his own machine, for the whole session, changeable any time.
- Each side sees the conversation; what Claude does on your machine is shown to you only, with a small notice saying so.
- When built: a mode switch only you can flip, plus an activity view beside your terminal.
- First: one short test of whether Claude Code stays silent when our gate says "allow" (6 runs, Mac).
- Nothing of this is built today; your terminal asks, and nothing records or shows a history.

## 2. His words, Friday's reading, the open assumptions
**His words (2026-11-23, verbatim as given to the drafter by Friday; the board itself NOT READ):**
- 10:24: "This is an acceptable risk during development.  Naturally, the final product will have the two modes we discussed - allow and monitor, approve and monitor"
- 12:10:15: "one user clicks allow, Claude on that machine keeps displaying what its doing but no longer asks for permission.  the other user can do the same or approve each action depending on their choice.  The choice lasts the entire session but can be changed at any time"
- 12:13:06: "The other side should see instructions sent to it and communication between Claudes.  But what happens on your machine is for your eyes."
- 12:13:40: "and there should be a message to tell the user that.  Not big but there"

> **Friday's reading (the coordinator's, NOT his words).** Each owner chooses for his own machine, per session: APPROVE (each action asked) or ALLOW (actions shown, not asked). Either side may choose either; no agreement from the other side. Switchable at any time both ways. Two views: CONVERSATION (instructions sent to a side, and what the two Claudes say), seen by both; LOCAL ACTIVITY, seen only by that machine's owner. A small standing notice says which is which. "Both agree" (11) and time-limited grants (03 §5.3) are not the product's modes; they stay on file; nothing is built from them.

**Open assumptions (put to him, NOT confirmed):**
- **A-i: the always-refused list still holds in ALLOW** (credentials, the gate's own files, the classes of `docs/POLICY.md:71-84`). If wrong: those become plain allows; steps 5 and 6 (exclusions, hard deny of writes to gate files) still come first and hold "in every mode" (`docs/POLICY.md:48-51`), so only the step 7c classes are lost: credential reads, gate-file reads, permission-mode changes, sandbox off, untaught tools, privilege. The policy part would then need a new "nothing refused" path (Profile B of 11:161, never built). REASONED.
- **A-ii: ALLOW covers terminal commands too**, which changes "Keep it: every terminal command asks" (`05:21`) for ALLOW only. If wrong: nothing new is needed; step 7d already sends every shell command on to the red card when `shell_verified` is false (`docs/POLICY.md:86-91`), and ALLOW removes far fewer prompts, since searches arrive as shell (`06:574`). If right: ruling D2 "Only with the sandbox on" was made for the both-agree mode (`12:30` as quoted in 20:28); whether it carries over is OPEN, and review F-6 (the sandbox tick nobody checks) bites in full (`12:129-141`). On Windows a PowerShell call is never allowed by step 7d (`docs/POLICY.md:89-91`), so there A-ii changes nothing.

**Older documents his ruling overrides (both recorded; his 23 Nov words are newer):** `03:347` guest follow-along default "summaries" of the host's actions; `11:204` "at least summaries for every member"; his own 2026-08-21 words "the administrator on the other side would be able to see everything that's done" (20:23). All three now yield to "what happens on your machine is for your eyes". `03:339` "Mode changes are announced to both parties" is neither confirmed nor overridden: owner question Q1.

## 3. The user's experience, one session (Mac A on ALLOW, Mac B on APPROVE)
1. **Start.** A and B link as today. Each machine starts in APPROVE (P1). Each owner sees, in his own terminal window beside Claude Code, the two views and the notice. REASONED: the first build can be a second terminal window, as 11:201 designed (`coagent watch`, "never in the agent's own context"); the console (03 §6) comes later.
2. **Choose.** A's owner types the mode command himself in that window and confirms on a surface his agent cannot drive (P2). A's notice line changes to the ALLOW wording. B's owner does nothing; B stays APPROVE.
3. **What A's owner sees on A.** Claude Code's own pane keeps showing each tool call as it always does (REASONED: his "keeps displaying what its doing" is met first by Claude Code's own transcript, which already exists). LOCAL ACTIVITY adds one line per call: time, tool, target (path, command text whole, URL), CoAgent's decision and why, then the result when PostToolUse capture exists (P3). Refusals appear in red. No prompts, except for the always-refused list (refused, never asked, under A-i) and shell (asked, unless A-ii).
4. **What B's owner sees on B.** Every action asks in Claude Code's own prompt, as today (`docs/DAEMON.md:806-811`). His LOCAL ACTIVITY lists each ask and his answer once the daemon learns answers (not built: `docs/DAEMON.md:915-916`); until then it lists "asked" only.
5. **What each sees of the other.** CONVERSATION only: the instructions each side's Claude received from the other, and every message between the Claudes, identical on both sides (P4). A sees nothing of B's tool calls; B sees nothing of A's. Whether B sees "A is on ALLOW": Q1.
6. **Switch mid-session.** A goes back to APPROVE with one command, no confirmation (P5); effective at the very next hook call (as Revoke, `03:319`). B may move to ALLOW the same way as step 2.
7. **A prompt already open when A switches to ALLOW.** Today that prompt is Claude Code's own and the daemon cannot withdraw it (`docs/DAEMON.md:810-811`). P6: it stays on screen and A's owner answers it by hand; the next call is decided under ALLOW.
8. **Actions in flight when A switches back to APPROVE.** P7: a call already allowed and running is not recalled (`03:319`); every later call asks. Stop (`03:322`) remains the way to halt a turn.
9. **Owner away while on ALLOW.** Q2. Earlier designs pause after 10 minutes without presence (`03:324`, `11:210`); his "lasts the entire session" reads against a silent pause. REASONED.
10. **End.** At session end the mode is gone; the next session starts in APPROVE (P1). A daemon restart also returns to APPROVE (P8).

**The notice (P9; words counted with wc -w):**
- Variant 1 (one line, 22 words): "Shared with the other side: messages between the two Claudes and instructions sent here. Not shared: what Claude does on this machine."
- Variant 2 (one line per view, 5 + 12 words): CONVERSATION: "Both sides see this conversation." LOCAL ACTIVITY: "Only you see this. Nothing here is sent to the other side."

## 4. The product's obligations
| # | Requirement | Source |
|---|---|---|
| R1 | Two modes per machine: APPROVE (every action not refused is asked, as the gate does today) and ALLOW (shown, not asked) | his words: "no longer asks for permission" / "approve each action" |
| R2 | Each owner chooses for his own machine only; no agreement from the other side is needed | his words: "the other user can do the same or approve each action depending on their choice"; `03:245` "set only by that machine's owner" |
| R3 | The choice lasts the session and changes at any time, both directions | his words: "The choice lasts the entire session but can be changed at any time" |
| R4 | The mode is ONE value held in the daemon's memory, not per Claude Code session `State`, not on disk | PROPOSED, from F-10 (`12:163-167`) and P8 |
| R5 | Only the owner, at that machine, can change it. Never the peer, never a wire message, never an MCP tool, never the agent | `03:68` and `03:337` (earlier design); PROPOSED for "never the agent" in the safe direction too (P5 covers who may lower it) |
| R6 | The switch to ALLOW cannot be completed by anything the agent can do: an IPC command alone is not enough, because any same-user process reaches the socket (`docs/DAEMON.md:853-861`) | PROPOSED (P2) |
| R7 | ALLOW applies only to Claude Code sessions bound to the CoAgent session (`bound_sessions`, `docs/POLICY.md:722-724`) | PROPOSED; prerequisite "session binding" not built (`docs/DAEMON.md:815`, `:915`) |
| R8 | In ALLOW, steps 1-7b keep deciding exactly as without the mode; under A-i the step 7c classes are refused, never asked | `docs/POLICY.md:83-84`; A-i OPEN |
| R9 | Shell in ALLOW: asks unless A-ii is confirmed; even then only `Bash` with a verified sandbox | `05:21`; `docs/POLICY.md:86-91`; A-ii OPEN |
| R10 | LOCAL ACTIVITY shows every gated call: time, tool, kind, target, decision and its reason, result (exit, size) when captured; display-safe strings only | his words: "keeps displaying what its doing"; fields from `11:201`; P3 |
| R11 | LOCAL ACTIVITY never enters the agent's context (no tool result, no hook text the model reads) | `11:201` (design); his words "for your eyes"; measurement M3 |
| R12 | Nothing of LOCAL ACTIVITY crosses the link: no event, count, time or header of it is sent to a peer | his words: "what happens on your machine is for your eyes"; PROPOSED that counts and times count too (see section 6, audit) |
| R13 | CONVERSATION shows instructions received and every message between the Claudes; both sides see the same items in the same order | his words: "should see instructions sent to it and communication between Claudes"; "same items" PROPOSED (P4) |
| R14 | A small standing notice in both views says what is shared and what is not | his words: "there should be a message to tell the user that.  Not big but there"; text P9 |
| R15 | The current mode is always visible to the owner on his machine | `03:364` ("Hidden mode state is a known pitfall"); PROPOSED |
| R16 | Kept after the session: LOCAL ACTIVITY in a local-only record for that owner; CONVERSATION by each side for itself | PROPOSED (P10); capacity ruled "Fixed capacity now, seal and continue as the next piece" (`05:55`); retention OPEN (`BACKLOG.md:611` DQ-S2) |
| R17 | In ALLOW no action is allowed without its LOCAL ACTIVITY record written first | `11:235` "record before allow" (design); PROPOSED to keep |
| R18 | Owner away in ALLOW: behaviour per Q2 | his words "lasts the entire session" vs `03:324` |
| R19 | In ALLOW the agent can still read its inbox and send (otherwise "communication between Claudes" stops) | REASONED from F-1, F-2 (section 4a) |

### 4a. Review 12's findings against the ruled per-owner ALLOW
| Finding | Verdict | One-line reason |
|---|---|---|
| F-1 inbox tools untaught, refused in the mode | applies | ALLOW reuses step 7c; `inbox_read`/`wait` are still untaught (`docs/POLICY.md:796-797`; `BACKLOG.md:925-928`) |
| F-2 every send refused (no scanner) | applies | an unscanned share is a refused class (`docs/POLICY.md:72`); the scanner is the caller's and not wired (`:27`) |
| F-3 recursive search reads excluded files | applies in part | safety closed in the crate (`docs/POLICY.md:729-730`); the cost remains: with credential exclusions every recursive search is refused |
| F-4 deputy admission | does not apply | no consent set; one owner decides for one machine |
| F-5 clocks | applies in part | no time limit in his ruling; any away timer (Q2) still needs both clocks |
| F-6 sandbox tick | applies in part | only if A-ii is confirmed; then in full |
| F-7, F-8 gate-file reads, later-running writes | apply; closed in the crate | refused classes rules 30, 31 (`docs/POLICY.md:731-738`), under A-i |
| F-9 owner act and console authentication | applies in part | no agree-words, but the switch needs an act the agent cannot perform (R6) |
| F-10 mode in per-session state; binding | applies | R4, R7 |
| F-11 consents restored from disk | applies in part | no consents; the same rule for the mode: never restored (P8) |
| F-12 recording | applies in part | record-before-allow and the seal window (`12:178`) apply; peer charging does not, if LOCAL ACTIVITY is local-only |
| F-13 U-B1, hook allow silent? | applies in full | the whole of ALLOW depends on it (M1) |
| F-14 checked at the decision | applies | the switch to APPROVE must bind the next decision, under one lock |
| F-17, F-18 observers, rounds | do not apply | no group agreement |
| F-20 home-folder reads plus fetch | applies | `docs/POLICY.md:776-777`: only listed credential and gate paths are protected |
| F-24 subagent session ids | applies | decides whether a subagent's calls are in `bound_sessions` (M5) |

## 5. What exists and what is missing
| Requirement | Built today (code a running product calls) | Designed only | New |
|---|---|---|---|
| R1 APPROVE | the gate asks via Claude Code's prompt: `crates/coagent-daemon/src/gate.rs:366` calls `decide(.., Surface::TerminalPrompt, ..)`; `verdict` maps Allow/Deny/Ask to allow/deny/ask (`gate.rs:489-507`); the hook prints `permissionDecision` (`crates/coagent-hook/src/main.rs:208-235`) | held requests, console approvals (`03:278-286`) | none |
| R1 ALLOW | nothing. Steps 7c/7d exist in the policy crate but are SHIPPED DARK: the daemon calls `decide`, never `decide_with_mode` (`gate.rs:366`; `docs/POLICY.md:64-68`); dark "holds by usage only" (`BACKLOG.md:930-933`) | 11 §3 | the daemon passing a mode view; texts: today's allow text says "both agree; consent set <id>" (`docs/POLICY.md:86-87`), wrong for a per-owner choice |
| R4 one value in the daemon | no mode value | F-10 fix (`12:167`) | yes |
| R5, R6 owner-only switch | none; IPC reachable by any same-user client (`docs/DAEMON.md:853-861`); MCP elicitation measured (spike U4) but unused | 03:337 (console or elicitation) | yes, plus a source-audit test that only the mode module builds the view (`BACKLOG.md:933`) |
| R7 session binding | none: "every call of every Claude Code session that loads the plugin is decided" (`docs/DAEMON.md:814-816`) | `docs/DAEMON.md:915` | yes |
| R8 refused list | in the crate, unreached (`docs/POLICY.md:71-84`; `crates/coagent-policy/src/bypass.rs:19-30` `BypassView`) | 11 §3.3 | reuse as is under A-i |
| R9 shell | every shell call is a red card (`docs/POLICY.md:94-98`) | `shell_verified` input (`bypass.rs:27-29`) | a verified-sandbox route only if A-ii (F-6 Route P, `12:138`) |
| R10, R11 LOCAL ACTIVITY | the daemon logs only `gate: <decision>` to stderr, deliberately without the command (`crates/coagent-daemon/src/engine.rs:1914-1915`); 5 such ask lines in the Mac host log of 2026-11-23 (counted, `c2_session_2026-11-23/mac_host.log`) | stream `11:201`; console Activity tab `03:373` | an activity record and a viewer; PostToolUse registration (hook is PreToolUse and ConfigChange only, `docs/DAEMON.md:869`) |
| R12 nothing crosses | nothing of it is sent today (REASONED: no activity record exists) | the audit design shares chains with members by share level; even at share level "nothing" counts and times leak (`BACKLOG.md:377-378`) | a local-only record, kept out of the shared chain |
| R13 CONVERSATION | messages exist in the daemon (`inbox.json`, outbox; `docs/DAEMON.md:60`); a human sees them only inside the agent's tool results | chat dock `03:375`, audiences `03:345` | a viewer from the daemon's own sent and received messages |
| R14, R15 notice, mode shown | none | strip with mode dial `03:372` | yes |
| R16, R17 record | audit crate and `coagent-audit-host` exist; the daemon does not use them (`docs/DAEMON.md:916`; no audit dependency in the daemon, searched) | 11 §5, design 10 | wiring (L) |
| R19 inbox and send in ALLOW | refused today in the mode (F-1, F-2) | F-1 fix `12:104` | `KNOWN_TOOLS` lane; the protected test pins 24 taught names (`BACKLOG.md:928`) |

## 6. Honest limits (with the product as it stands)
**A hand `send` passes the gate.** Any same-user program that reaches the socket can send as this device with no ask; it RAN on Mac loopback 2026-11-23 (`docs/DAEMON.md:853-861`; `BACKLOG.md:1136-1139`). So CONVERSATION can show only what the daemon sent, which is everything on the wire, but ALLOW plus "keeps displaying" cannot say that the agent wrote it. READ.

**Unread peer text at rest.** `inbox.json` holds unread peer messages in clear, 0600, until released; the gate guards the release, not the file (`docs/DAEMON.md:862-865`; `BACKLOG.md:1141-1144`). A same-user process sees peer instructions before the owner's view does. READ.

**Shell text is opaque.** LOCAL ACTIVITY shows a command's text, not what it did: aliases, variables, scripts and what a program does with its arguments are invisible to the gate (`docs/POLICY.md:756-759`, `:763`). Under A-ii the refusals for shell are text matching only (`docs/POLICY.md:767-771`). The result column needs PostToolUse, which gives exit and output, not every file touched. READ, the last clause REASONED.

**The witness window.** A same-user client can consume a read witness inside its 330 s window (`docs/DAEMON.md:825`, `:848-851`). READ.

**Windows has no gate yet.** `coagentd --gate` exits 2 on Windows: "nothing on this machine is then checked by CoAgent" (`docs/DAEMON.md:669-671`; `BACKLOG.md:1022-1025`). Neither mode nor LOCAL ACTIVITY exists there until stage C3b; CONVERSATION needs no gate and could exist sooner (REASONED). Native Windows has no sandbox (`docs/POLICY.md:763`), so PowerShell asks in every mode.

**The audit design and "for your eyes".** The audit crate was built to share each author's chain with members by share level; at share level "nothing" a member still learns the count and millisecond time of events disclosed to a third member (`BACKLOG.md:377-378`). LOCAL ACTIVITY must therefore not enter that shared chain at all (P10). READ for the leak, REASONED for the consequence.

## 7. Measure first (before any build)
What the spikes measured (12 U and 8 G folders listed with `git ls-tree`; RESULT files read: G1-deny-blocks-write, G2-dead-daemon-blocks, U1, U2, plus U4, U9):
- G1: hook allow ran the Write in default mode only WITH `--allowedTools Write`, and in bypassPermissions (`spikes/G1-deny-blocks-write/RESULT.md:7,10`). G2: allow ran in bypassPermissions (`spikes/G2-dead-daemon-blocks/RESULT.md:4,9`). U2: allow controls carried `--allowedTools Write` in every non-bypass mode (`spikes/U2-ask-in-bypass-dontask/RESULT.md:5,7`). All headless, Claude Code 2.1.325.
- U1: interactive, default mode, a PermissionRequest hook (not PreToolUse) answering allow after 20 s created the file and closed the dialog, which was on screen meanwhile (`spikes/U1-permission-dialog-race/RESULT.md:11`).
- **Not measured anywhere read: "hook says allow, the user has no allow rule: does Claude Code still prompt?"** (also `11:193`, `12:188-191`). Since then Claude Code 2.1.328 starts in auto mode by default (`p1p_review/live_demo_report.md:52`).

| # | Question | Smallest experiment | Model runs | Machine |
|---|---|---|---|---|
| M1 | Hook allow, no allow rule: silent? For a Write in the workspace and a Bash command; in default mode and in auto mode | U1-style rig: interactive, private tmux, stub daemon answering allow, no rules; capture the pane. Controls: no hook, same prompt (dialog expected) | 6 (2 tools x default, auto, control) | Mac |
| M2 | What the user sees in the terminal in M1's case (the call line, any CoAgent text) | read M1's pane captures | 0 | Mac |
| M3 | Can hook output show the owner a line the model never reads? Candidates: `permissionDecisionReason` on allow, and a user-facing message field (field name UNVERIFIED, from the hooks docs to be re-read) | one interactive run (is the marker on screen?) and one headless stream-json run (is the marker in anything the model receives?), distinct markers per field | 2 | Mac |
| M4 | Only if M1 prompts: does a PermissionRequest hook answering allow at once keep the dialog off screen? | U1 case B with no delay, Write and Bash | 2 (conditional) | Mac |
| M5 | Do a local subagent's tool calls carry the parent's `session_id` (F-24)? | headless, hook logs stdin, one `Agent` call that does one Read | 1 | Mac |
| M6 | Does PostToolUse stdin carry exit and output for Bash and Write? | read U9's recorded PostToolUse inputs (`spikes/U9-sandbox-detection/raw/hook-on/`) first; run only if absent | 0 or 1 | Mac |
| M7 | Can a command run by the agent's Bash tool open the terminal (`/dev/tty`)? Decides whether a typed confirmation is agent-proof (P2) | headless and interactive, one command each | 2 | Mac |

Total: 11 runs certain, up to 14 (counted from the table), smallest model. Windows repeats of M1 and M3 wait for C3b; they are not part of C3a's ruled run count (daily 2026-11-23:47).

## 8. Build order proposal
Paths checked against the trees named in `docs/POLICY.md` and `docs/DAEMON.md` §8 at 3768a67.
| Lane | Owned paths | Outcome (one sentence) | Size | Proven by |
|---|---|---|---|---|
| L0 MEASURE | new `spikes/U-B1-hook-allow-silent/` only | M1 to M7 answered with raw captures | S | RESULT file with pane captures and controls |
| L1 ACTIVITY (first on screen) | new `crates/coagent-daemon/src/activity.rs`; the `log!` site in `engine.rs:1915`; a viewer subcommand (new file in the daemon crate, not `coagent-cli`, kept untouched per `docs/DAEMON.md:770-771`) | the owner sees, in a second window, one display-safe line per gate decision (APPROVE today) with the notice | S | a test that no activity text reaches IPC answers or the wire; red control "activity line sent to peer" |
| L2 POLICY-OWNER-MODE | `crates/coagent-policy/src/bypass.rs`, `engine.rs` (AllowWhy text), `docs/POLICY.md` §2 7c/7d, `tests/` | the dark mode view gains a per-owner origin and its own text; still dark | S | t24-style differential: mode absent equals today |
| L3 KNOWN-TOOLS | `crates/coagent-policy/src/known.rs`, `action.rs` classify arm, the protected `tests/qa_strict_m2/qa_strict.rs` (coordinator's ruling needed) | `inbox_read`/`wait` taught, so ALLOW can read peer text (F-1) | M | the 4 pinned tests updated by ruling; witness tests unchanged |
| L4 SCANNER | daemon share path in `engine.rs` send handling plus a new scanner file | `share_flagged` set before `decide`, so sends work in ALLOW (F-2) | M | flagged and clean corpora |
| L5 DAEMON-MODE | new `crates/coagent-daemon/src/mode.rs`; `gate.rs:366`; session binding | one mode value, owner-only switch (per M7 and P2), bound sessions, back to APPROVE at restart and session end | L | red controls: switch by IPC alone, by MCP, by peer message, restored from disk, unbound session allowed |
| L6 CONVERSATION | new `crates/coagent-daemon/src/conversation.rs`; `store.rs` read side | both sides list the same messages in the same order, with the notice | M | two-daemon loopback test comparing both lists |
| L7 RECORD | daemon wiring of `crates/coagent-audit-host`; a local-only store | record before allow; nothing of LOCAL ACTIVITY in the shared chain | L | the audit-host tests plus a no-cross test |

Collision: L1, L4 and L5 all touch `crates/coagent-daemon/src/engine.rs`; run them one after another, or give L5 the IPC dispatch and let L1 and L4 add only their own files. L2 and L3 both touch the policy crate; serial. L1 is the first lane that shows the owner something; ALLOW itself is visible only after L2, L3, L4, L5. **Windows:** L1's activity and L5's mode wait for C3a (W1 and W4 tests, no product change) and then C3b (the gate switched on); L6 does not need the gate.

## 9. For Friday to rule, and for the owner
**PROPOSED (the drafter's; Friday to rule):**
- P1 every session starts in APPROVE; the choice is not remembered across sessions.
- P2 switching to ALLOW needs a typed confirmation on a surface the agent cannot drive (elicitation per U4, or `/dev/tty` per M7); an IPC command alone never suffices.
- P3 LOCAL ACTIVITY line fields: time, tool, kind, target, decision, reason, result when captured.
- P4 CONVERSATION shows the same items in the same order on both sides, built from each daemon's sent and received messages.
- P5 going back to APPROVE: one owner command, no confirmation; system events (gate missing, peer key change) may also lower it, with a notice; the agent never changes the mode in either direction.
- P6 a prompt open at the switch to ALLOW stays and is answered by hand.
- P7 a running call is not recalled at the switch to APPROVE.
- P8 a daemon restart returns to APPROVE; the mode is never read from disk.
- P9 the notice wording (two variants, section 3).
- P10 LOCAL ACTIVITY is kept in a local-only record, never in the shared audit chain; CONVERSATION each side for itself.
- P11 no tripwire in ALLOW (F-16 shows it fires in ordinary use, `12:203`), or attack classes only.

**For the owner (two questions; the open assumptions A-i and A-ii are already with him):**
- Q1 Does the other side see which mode you chose? a) yes, one word in the conversation view (default; it tells them their instructions run unasked); b) no.
- Q2 On ALLOW, when you have been away 10 minutes: a) keep going, as you said "lasts the entire session" (default); b) pause until you are back.

## 10. NOT READ / NOT ESTABLISHED
- His four lines at source (the board): taken from Friday's brief. His 2026-11-20 rulings D1 to D3 at source.
- 03 beyond §5 and §6.1-6.2 by search; 04, 07, 09, 10, 13 to 18 not opened; 11 only §3 and §4; `docs/POLICY.md` lines 1-120, 195-210, 695-797; `docs/DAEMON.md` §8 and lines found by search; BACKLOG by search.
- U9 raw PostToolUse inputs (M6), U4 beyond RESULT, the hooks documentation (field names in M3 UNVERIFIED).
- Whether the allow reason text reaches the model in an interactive session; whether the agent's Bash has a terminal.
- Whether D2 carries over from "both agree" to the per-owner ALLOW.
- Differing lines recorded, not reconciled: `docs/POLICY.md:204-205` says the bypass note was "asked and not answered"; his 18 Nov answer exists (19:17). `03:347` and his August words versus his 23 Nov words (section 2).
