---
date: 2026-11-19
type: reference
source: security design seat for Friday, commissioned after Kam's terminal line of 2026-11-18 (morning wrap)
status: DESIGN ONLY — nothing built; building waits for Kam's word after he reads this
project: General/Claude to Claude (CoAgent) — no client
---

# CoAgent: "both agree" mode (approvals off, people watch). Design

**Kam's words, verbatim (Friday's terminal, after the 2026-11-18 morning wrap):** "what I meant by bypass permission.  the same setting as in claude.  if both users agree to let the agents work, monitoring but no approval for any aciton necessary"

**Friday's reading, recorded then:** a session-wide mode, on only when BOTH people agree, in which agents act with no approval card and the people watch. It is a new piece. **One question to Kam is still open: do the hard refusals (the gate's own settings, credentials, excluded paths) still hold while the mode is on?** Friday recommended yes, plus either person can switch it off at once and everything is recorded. This design builds on that recommendation as the default (Profile A) and shows the alternative (Profile B).

**How to read the labels.** **[main: file:line]** is a line read with `git show 36537eb799a36e9c99860cfe952b52aee8700d95:<path>` in the repo `coagent/2_Project_Files` (paths under `crates/coagent-policy/` unless named). **[p1p: file:line]** is the same at `f2603fd9d1993954e98812bc142ec05e22f27841` (branch `p1p-gate`). **[G1]**, **[U1]**, **[U2]**, **[U6]**, **[G2]** are `spikes/<name>/RESULT.md` at main. **[03 §x]**, **[04 §x]**, **[05]**, **[06 §x]**, **[07 §x]**, **[09 §x]** are the design files in this folder. **REASONED** means my argument from reading, untested. **PROPOSED** means a number I chose. **(computed, not run)** marks arithmetic. **UNKNOWN** says what would settle it. I give no Claude Code behaviour beyond what a spike or a cited document shows.

---

## 1. BLUF for Kam

**What turning it on does.** Each person turns it on from their own console. When **everyone in the session** has done so for the same session and the same member list, the gate stops showing approval cards on every machine. Actions that would have asked are allowed. Each allowed action appears straight away in a live stream that every member can watch. It lasts until someone turns it off or the time limit you picked runs out (60 minutes unless you choose otherwise, 8 hours at most).

**What still stops an agent (Profile A, Friday's recommendation and this design's default).** These are still refused, with no card and no way to approve them while the mode is on: writes to the gate's own settings and plugin files (Claude Code settings, hooks, CoAgent's own folder, git hooks); credentials (SSH keys, cloud logins, browser profiles and the rest of the credential list); paths you excluded; an agent changing its own permission mode or switching the sandbox off; a share the secret scanner flags; and tools the gate has not been taught. Settings changes stay blocked. If the CoAgent service is not running, every action is blocked, as now.

**The honest catch, before anything else.** The gate cannot read shell commands (that is why every terminal command asks today, your ruling of 2026-11-17 [05]). If the mode lets terminal commands run without approval, then a command can reach anything your user account can reach, credentials and gate settings included. The gate can catch only commands whose text names a protected path or a forbidden word. So "hard refusals hold" is **exact for file edits, reads, web fetches, outside tools and shares, and only best-effort for terminal commands.** Section 3.4 offers three choices. I recommend terminal commands run without approval only where you have ticked "my Claude Code sandbox is on". Elsewhere they keep asking.

**How either person turns it off.** One button in the console, or `coagent bypass off` in any terminal, or the agent itself may call "off". Off on your own machine takes effect from the very next action. Nobody can delay it, because nothing travels over the network. When someone else turns it off, your machine hears about it within seconds. If a relay tries to hold that message back, your machine switches off by itself within 45 seconds, measured on your own clock (PROPOSED figure). It also ends by itself when: someone joins, leaves or is removed; any service restarts; the link drops; the time limit passes; you have been away from the screen 10 minutes (unless you chose "keep going while I'm away until HH:MM"); the agent hits three refusals in ten minutes; or your recording space for this mode is full.

**What is recorded.** In each machine's signed audit log: every person's agreement and withdrawal, the moment the mode started on that machine and why it ended, and every action it let through. For each such action the log also records **what would have happened without it** (for example "would have asked: terminal command"). Other members keep a signed copy of what you let them see. During the mode they must see at least summaries, so they can watch.

**Your decisions, in order:** D1 the hard-refusal question (A or B). D2 whether the mode overrides your "every terminal command asks" ruling, and how (S1/S2/S3). D3 whether "both" means every member, including observers. Then the smaller interpretations in §8.

---

## 2. Agreement

### 2.1 Why this is not "collective approval"

[04 §3.4] rule 1 says phase 1 has no collective approval: only the machine's owner decides about that machine. This mode keeps that rule. On machine M the mode can only start through **M's owner's own act on M**. The other members' agreement is an **extra condition**. It can stop the mode on M and can never start it. This is the "add a condition to the owner's decision, never replace it" shape that [04 §3.4] already allows for a future four-eyes mode.

### 2.2 Turning it on

1. **A round.** Any member opens a round from the console: *"Ask everyone to let the agents work without approvals"*. The proposer's daemon sends `bypass.round` to every member. It carries a fresh random `round_id` (128 bits), `session_id`, the current roster version and its hash, the **profile** (§3: A or B, the terminal option S1/S2/S3, the presence rule; given as a canonical object and its hash), and a proposed duration. The round lapses after 5 minutes (PROPOSED). A round is an invitation. It carries no authority.
2. **Each person, on their own machine.** The console shows one fixed dialog built only from fields the daemon has verified: who proposed; the full member list and who has agreed so far, where "agreed" means a signed statement the daemon checked and never a chat line; the profile in plain words, including "what still stops an agent" and the terminal option; the duration (they may shorten it, never lengthen it past 8 hours); and the share level the mode needs: *"While this is on, every member sees at least summaries of your agent's actions."*
3. **The human's act: console plus words read aloud (§6.3).** The person confirms in the authenticated console. Then they type the **agree-words** that another member's console shows (three words, derived as below), and their own console shows words that another member types. Each machine's words are shown only on that machine's console. They are never put into an MCP result, an IPC answer or anything an agent can read. The words travel between people by voice, like the verify-words at pairing [03 §4.1].
   *Derivation (PROPOSED):* the words shown on X's console for round r are `words(H("coagent-bypass-words" ‖ round_id ‖ X's per-round secret))`. X's daemon sends a commitment `H(secret)` in its consent and reveals the secret, inside the encrypted pairwise channel, only to the member whose console will display it. M's daemon accepts M's typed words only when they match words derived from a secret that the other member's daemon revealed for this `round_id`. With 2 people each types the other's words. With more, each types the words of the next member in key order (a ring), so every person is proven present by someone else.
4. **The signed statement.** M's daemon signs `bypass.consent { session_id, round_id, roster_version, roster_hash, required_members: [key ids], profile_hash, duration_s, presence_rule, words_commitment, consenter: M, sig }` with M's device signing key, and sends it to every member.
5. **Activation on M.** M's daemon sets the mode on its own machine when **all** of these hold:
   - M's own consent for this `round_id` exists, made on M's console with words verified;
   - a valid consent from every key in `required_members` for the same `round_id`, `roster_hash` and `profile_hash`, where `required_members` equals the member keys of M's current roster version (D3: observers too, by default);
   - every required member's **lease** is live (§2.4);
   - the link is open (not `ClosedTainted`), the session has not ended, M's own audit log has room (§5);
   - M's share level for every member is at least *summaries*. The dialog raised it, and lowering it later ends the mode.
   M records `bypass.active { consent_set_id = H(sorted consents ‖ roster_hash), expires_at }`. The **expiry** is the shortest `duration_s` among the consents, counted on M's clock from the moment M activated. Durations, not wall-clock times, so clock skew between machines does not matter.

**Profile mismatch.** Every consent must carry the same `profile_hash`. M enforces only the profile M's owner saw and agreed to. A peer cannot widen M's mode by sending a consent with a wider profile, because then the hashes differ, there is no agreement, and nothing starts.

### 2.3 How it ends: either person, instantly, no peer can block

| Cause | On M | Delay at M | Recorded on M as |
|---|---|---|---|
| M's owner presses Off (console), runs `coagent bypass off`, or the agent calls off | the state flag clears in memory first, then the state file is written, then `bypass.withdraw` is sent | **next hook call**. No network step comes first, so no peer and no relay can delay it | `bypass.ended {own_withdrawal}` + own `bypass.withdraw` |
| Another member X withdraws | a verified `bypass.withdraw` from X clears the flag **before any storage step** (§5.2) | arrival of the message | `bypass.ended {peer_withdrawal: X}` |
| X's withdrawal is withheld (relay, network) | X's lease lapses | **at most L = 45 s after M sent its last challenge that X answered** (PROPOSED; §2.4) | `bypass.ended {lease_lapsed: X}` |
| Roster changes in any way: join, leave, removal, role change, a deputy's provisional admission [06 §2.8], session end | ends at once on the verified object | arrival | `{roster_change: v}` |
| M's daemon restarts | the mode is **never restored**. On start, a "was on" marker in the state file produces the end record | none | `{restart}` |
| Another member's daemon restarts | its leases stop | ≤ L | `{lease_lapsed: X}` |
| The link closes or the session is `ClosedTainted` | ends | at once | `{link_closed}` |
| Time limit | ends | at once (M's clock) | `{expiry}` |
| M's owner absent (§4.2) | **pauses**: approvals come back on M. Not ended | 10 min (PROPOSED) | `bypass.paused` / `bypass.resumed` |
| Tripwire: 3 refused actions within 10 min on M | ends | at once | `{tripwire}` |
| M's mode allowance is full, or an action cannot be recorded | ends; that action goes through the ordinary gate | at once | `{log_full}` (written from the reserve, §5) |
| A member signs that it no longer keeps M's records (`held_from: None`, [07 §1.5 C]) | ends on M | arrival | `{peer_not_keeping: X}` |
| M lowers any member's share level below summaries | ends | at once | `{share_lowered: X}` |

**Ended means ended.** Nothing resumes the mode except a new round with fresh consents and fresh words. The one exception is the presence pause, which resumes when the owner is back, because nothing about the agreement changed.

**Withdrawal needs no consent and no signature check from anyone else.** "Off" is accepted from every local surface, the IPC socket and the agent included, because switching off is always safe (the same direction rule as [03 §5.4]: "anything can move down").

### 2.4 The lease: why a withheld withdrawal costs at most 45 seconds

A plain heartbeat ("I still agree", every 10 s) has a gap. A relay can deliver each heartbeat late by up to the lease length, then hold back the withdrawal, and so double the delay (REASONED). So the lease is a **challenge and answer, measured on M's own clock**:

- Every 10 s (PROPOSED) M sends each required member X `bypass.challenge { round_id, nonce_M_k }` (fresh 128-bit nonce) inside the pairwise channel.
- While X still agrees, X answers `bypass.alive { round_id, nonce_M_k, sig }`.
- M treats X's agreement as live while M holds an answer to a challenge **M sent less than L = 45 s ago, by M's monotonic clock**. Delay cannot stretch it, because the timing starts when M sent the challenge, not when the answer arrived.
- After X withdraws, X stops answering. Whatever the relay does, M's last useful answer is to a challenge sent no later than the withdrawal, so the mode ends at M within L of the withdrawal (REASONED). It ends earlier if the withdrawal itself arrives.
- L must be longer than an ordinary repair of a healthy link, which [09 §1 item 6] puts at about 17 s. 45 s gives room. A worse link ends the mode, and that is the safe direction.
- Challenges and answers are kept in memory only, at most one outstanding challenge and one latest answer per member. They are never written to disk (§5).

### 2.5 Membership and restarts, case by case

| Event | Result |
|---|---|
| A newcomer is proposed but not yet admitted | no change (a proposal is not a roster change) |
| The starter admits someone, or a deputy admits someone provisionally [06 §2.8.3] | ends everywhere; a new round needs the newcomer's consent too |
| A member leaves or is removed | ends everywhere; a new round among those left |
| The starter names or revokes a deputy (a roster grant [06 §2.8.2]) | ends (it is a roster version) |
| Guest ↔ observer change | ends |
| The bound Claude Code session ends or `/clear` runs | the mode applied to the agent sessions bound at activation; a new agent session is not covered until a new round (INTERPRETATION I-B6) |
| Link drop shorter than L | no change |
| Link drop longer than L | ends at M (lease) |
| A peer is behind on the roster | its consent names an older `roster_hash`, so there is no agreement |

### 2.6 Time limit

Every consent carries a duration: default 60 minutes, maximum 8 hours, matching the trust grants [04 §6.4]. The shortest one wins. There is no "extend". To continue, start a new round. The remaining time shows on every console. Two minutes before the end the stream says "approvals come back at HH:MM".

---

## 3. What the mode changes in the gate, exactly

### 3.1 Where it sits in the decision order

`decide` today runs: [1] wrong session → [2] stop → [3] pause → [4] over a bound → [5] exclusions → [6] hard deny → [7] link closed and tainted → [7b] owner's exact-command list → [8] T3 asks → [9]/[10] session approvals and memory → [11] grant → [12] ask / [13] deny when nobody can answer [main: src/engine.rs:620-742; docs/POLICY.md:37-87].

The mode adds two steps **after [7b] and before [8]**. Everything above stays in front of it:

- **[7c] mode refusals.** If the mode is active and the assessment carries a refused class (§3.3), the result is `Deny(BypassRefused{reason})`, with the text "coagent: not allowed even with approvals off: <reason>". It never becomes a card. (The mode promises no cards, and a refused thing is refused.)
- **[7d] mode allow.** If the mode is active, the result is `Allow(Bypass{consent_set_id})`. This covers every remaining T0, T1, T2 and T3 action, including those that would have reached [12].

Why this placement:
- Steps [1]-[6] are unchanged and come first, so stop, pause, size bounds, **exclusions** [main: src/engine.rs:652-665] and **hard denies** [main: src/engine.rs:666-674] hold in both profiles. Exclusions and hard denies are not part of the A/B question.
- [7] comes first, so a closed, tainted link keeps its rule. The mode also requires an open link (§2.2 step 5). Both conditions are checked, belt and braces.
- [7b] comes first. A listed command is allowed as before, and its audit line says "owner's list", not "mode".
- [8]-[13] never run while the mode is active. Grant counters are not spent (`State::record` counts only grant allows [main: src/state.rs:288-298]).

`decide` stays pure [main: docs/POLICY.md:12-26]. The mode reaches it as data: a new `State.bypass: Option<BypassState { consent_set_id, profile, expires_at }>`. `decide` checks `now < expires_at` itself. Everything else is the daemon's job: leases, rounds, presence, the roster, and setting or clearing the field. The daemon clears the field; `decide` never mutates [main: docs/POLICY.md:22-26].

### 3.2 Which `ask` becomes `allow`, per tier

| Tier (today's default) | Today, CONTROLLED | Mode on, Profile A (default) | Mode on, Profile B (alternative) |
|---|---|---|---|
| T0 read/search in workspace (ask on first touch) | ask | allow | allow |
| T1 edit in workspace (ask, with diff) | ask | allow (the diff goes to the stream) | allow |
| T2 execute (non-shell), fetch, outside tools that the gate has been taught, reads outside the workspace, shares | ask | allow, except the refused classes in §3.3 | allow |
| T3, for a refused reason in §3.3 | red ask | **deny** | allow, except hard deny and exclusions (always) |
| T3, other reasons (recursive delete, delete outside workspace, push/publish, cloud CLI, deploy, fetch with body, network send, `.git`/build-file writes, worktree removal, privilege*) | red ask | allow | allow |
| T3, shell command (every `Bash`/`PowerShell`/`Monitor`) [main: src/known.rs:87-102; src/engine.rs:498-504] | red ask (your ruling [05]) | per §3.4 (S1/S2/S3) | per §3.4 |
| Excluded path, any tier | deny | deny | deny |
| Hard deny (gate's own files) | deny | deny | deny |

\*Privilege (`sudo` and the rest [main: src/patterns.rs:386-389]) sits in Profile A's refused list by default, because a privileged command can rewrite the gate from outside it. INTERPRETATION I-B4.

### 3.3 The refused classes (Profile A)

Each comes from an existing assessment reason, so the engine already computes it. Nothing new is parsed.

| Refused class | Source in the engine | Why it stays refused |
|---|---|---|
| Credential path or folder | `Reason::CredentialPath` / `CredentialFolder` [main: src/engine.rs:447-451]; list [main: src/patterns.rs:127-209] | Friday's "credentials". **Needed even though the policy offers credentials as default exclusions** [main: src/patterns.rs:364-375]: the preview daemon passes only the owner's `--exclude` globs [p1p: crates/coagent-daemon/src/gate.rs:220-231], so a credential path today is a T3 ask, not a deny. In the mode an ask would become an allow. |
| Odd spelling of a path (`NormPath::Critical`) | `Reason::CriticalSpelling` [main: src/engine.rs:452-454] | it may be a protected path in disguise |
| An agent changing a permission mode | `Reason::PermissionModeChange` from `ExitPlanMode` (`Strict::ModeChange`) and permission flags in command text [main: src/engine.rs:542-544, 564-571; src/patterns.rs:425-435] | "the gate's own settings": an agent must not turn off Claude Code's own second gate |
| Switching the sandbox off | `Reason::SandboxBypass` [main: src/engine.rs:545-547] | removes the defence-in-depth the mode leans on (§3.4 S3) |
| A share the scanner flags, or one it could not scan | `Reason::ShareFlaggedOrUnscanned` [main: src/engine.rs:514-517] | the outgoing counterpart of "credentials" |
| A tool the gate has not been taught | `Strict::NotTaught` → `Reason::UnknownTool` [main: src/known.rs:93-95] | the gate cannot say what it does. This includes browser and desktop-control tools, which could click the console (§6.3) |
| Teammate or remote subagent | `Strict::PossibleTeammate` / `RemoteSubagent` [main: src/known.rs:97-101] | it starts work outside the bound session, where this gate may not see it |
| Privilege (default; I-B4) | `Reason::Privilege` [main: src/engine.rs:553-555] | can rewrite the gate from outside |
| **New word list:** command text naming CoAgent's control programs (`coagent`, `coagentd`, `coagent-hook`) or another agent CLI (`claude`, and others to list) | new `BYPASS_REFUSED_WORDS` in `patterns.rs`, matched like `T3_PRIVILEGE` [main: src/engine.rs:550-560] | stops an agent driving its own gate, or starting a nested agent without the gate, by the plain route. Best-effort, like every word list |

Profile B keeps only steps [5] and [6] and the always-on items of §3.5. Everything in the table above becomes an allow.

### 3.4 Terminal commands: three options (D2)

Your ruling "Keep it: every terminal command asks" [05; 06 §6] and the lesson "a recogniser of safe shell commands is never to be built" [06 §6 item 4] stay true **outside** the mode. Inside it:

| Option | Behaviour in the mode | What the refusals are worth |
|---|---|---|
| **S1** allowed | a shell command is allowed unless a deny scan hits: hard-deny paths named in the text [main: docs/POLICY.md:56-57], credential names, the §3.3 word lists. This is the same shape as the owner's exact list: "a listed command is still denied when a deny scan hits" [06 §6 item 3] | **best-effort only.** `cat ~/.ss''h/id_*`, a script file, an environment variable or base64 slip past any text scan. With S1, "credentials and gate settings are refused" is not true for shell. |
| **S2** still asks | shell commands keep their red card; everything else is approval-free | exact. The cost: most real work arrives as shell commands (searches included, [06 §6 item 5]), so you would still see many cards |
| **S3** allowed only with the sandbox (**recommended**) | S1, but only while the owner has ticked "my Claude Code sandbox is on, set to deny the credential and gate paths"; otherwise S2. Native Windows has no sandbox [04 §5.4], so there it is S2 | as good as the sandbox. A hook cannot see whether the sandbox is on [main: src/state.rs:93-100], so the tick is the owner's word. The sandbox settings live in protected files (hard deny + `ConfigChange` block), so an agent cannot quietly turn the sandbox off. The sandbox does not cover file tools or MCP servers [03 §3.6], and the exact rules in §3.3 cover those |

### 3.5 What the mode never changes (both profiles)

| Property | Where it lives today | Under the mode |
|---|---|---|
| Hard denies on the gate's own files | [main: src/patterns.rs:29-75; src/engine.rs:666-674] | unchanged, before [7c] |
| Exclusions | [main: src/engine.rs:652-665] | unchanged, before [7c] |
| `ConfigChange` blocked | always `block` [p1p: crates/coagent-daemon/src/gate.rs:305-319]; needed per [U6] | unchanged; the mode adds no code path to `ConfigChange` |
| Liveness invariant for peer text | a peer read is released only against a witness from a `PreToolUse` that the gate allowed or asked [p1p: crates/coagent-daemon/src/gate.rs:367-375; docs/DAEMON.md:519-546] | unchanged. With the mode on, `inbox_read` is allowed, so a witness is made on the allow path. No witness, no text |
| Fail closed when the daemon is absent | hook exits 2 on every error [p1p: docs/DAEMON.md:548-566]; [G2] | unchanged; the mode lives in the daemon, so no daemon means no mode |
| A hook deny holds in Claude Code's `bypassPermissions` | [G1] | unchanged; the refusals of §3.3 reach Claude Code as deny |
| Claude Code's own mode never raises CoAgent's trust | `permission_mode` "used only to lower the surface, never to raise trust" [main: src/action.rs:142-143] | unchanged. **Claude Code's `bypassPermissions` never turns this mode on, and this mode never changes Claude Code's mode** |
| Stop and Pause | [main: src/engine.rs:630-640] | unchanged, before the mode |
| Owner's Claude Code deny/ask rules after our allow | [03 §3.4, V2] | unchanged (§3.6) |

### 3.6 Does "allow" really mean no prompt at all? (UNKNOWN U-B1)

The gate's allow prints `permissionDecision: "allow"` [p1p: docs/DAEMON.md:556-558]. [03 §3.4] cites the documentation that an allow from a hook does not skip the user's own deny and ask rules. The spikes show:
- in `bypassPermissions`, hook allow runs the call [G1];
- in default mode, allow runs the call **when an allow rule is also present** (`--allowedTools Write`) [G1].

**Not measured:** whether a hook allow in an interactive default-mode session with **no** allow rule still shows Claude Code's own dialog. *What settles it:* one interactive run in the style of the U1 rig: default mode, no rules, hook answers allow, Write in the workspace, watch the pane. If a dialog appears, the person also needs their own Claude Code settings to stop prompting. CoAgent must never make that change for them (it is a hard-denied write and a blocked `ConfigChange`). The consent dialog would then say so.

---

## 4. Monitoring

### 4.1 What each person sees live

- **The stream** (console rail, and `coagent watch --stream` in a separate terminal, never in the agent's own context). One line per action the mode allowed, on every machine the viewer may see: machine owner, time, tool, kind, target (path, URL, MCP tool, command; whole and escaped, using the same display-safe fields the card uses today [main: src/engine.rs:1091-1180]), **what it would have been** (tier and the reasons that would have asked, e.g. "would have asked: T3 terminal command, names a push"), and the result when it ends (exit, size; PostToolUse capture is a prerequisite, §9.1).
- **Refusals** in red: "refused even with approvals off: credential path". Three in ten minutes end the mode (§2.3).
- **The header**: "Approvals off — agreed by Kam, Sam — ends 14:32 — Off". The Off button is always visible on every console.
- **Detail level**: each host's share level for that viewer. While the mode is on it is at least *summaries* for every member (§2.2), so everyone can see what every agent does. *Full* adds diffs and output previews, which are redacted and short by default [04 §6.5].
- **Peer strings**: escaped as on the agent path [p1p: docs/DAEMON.md:380-382]; the deviation note there requires any display path to escape again [p1p: docs/DAEMON.md:384-389].

### 4.2 When nobody is watching

- **Presence** is the existing signal: a visible console tab's heartbeat, or terminal input in the linked session [03 §5.3 "Walking away"].
- **Per machine, owner's presence only.** If M's owner shows no presence for 10 minutes (PROPOSED, the grant default), the mode **pauses on M**. M's actions get ordinary cards again, and unanswered cards expire to deny [03 §5.2]. It resumes when the owner is back. The other members' presence does not count for M, because it is M's machine.
- **"Keep going while I'm away until HH:MM"**: chosen per person in their consent, capped by the expiry, and shown to everyone as "unattended until HH:MM", the same as the grant's `on_leave: continue` [03 §5.3].
- **When the stream cannot keep up**: a slow viewer's stream is coalesced (counts per kind per minute) and the full list stays in the audit log, the same as the action-stream back-pressure in [04 §3.8]. A viewer never slows the agent.
- **When a member stops keeping your records** (their copy of your log is full): your mode ends (§2.3), because watching includes recording.

---

## 5. Recording

### 5.1 What the audit log records

All of these are audit-class events in the author's own chain [04 §3.9], signed, with the summary and full tiers set by share level.

| Event | Author | Fields (summary tier) | Full tier adds |
|---|---|---|---|
| `bypass.round` | proposer | round_id, roster_version + hash, profile + hash, duration | — |
| `bypass.consent` | each member | as §2.2 step 4 (signed statement) | — |
| `bypass.active` | M, about M | consent_set_id, expires_at, profile_hash, bound agent sessions (hashed) | — |
| `action.decided` with `why = bypass` | M | tool, kind, target summary, input hash, **would-have-been: tier + reasons**, consent_set_id | redacted preview (D12) |
| `action.decided` with `deny = BypassRefused` | M | tool, kind, refused class | — |
| `action.finished` | M | exit / size / duration | output preview |
| `bypass.paused` / `bypass.resumed` | M | cause (presence) | — |
| `bypass.withdraw` | withdrawer | round_id, at | — |
| `bypass.ended` | M, about M | cause (the table in §2.3), the member named where there is one | — |

**Record before allow.** M writes and syncs the `action.decided` event **before** the hook receives `allow`. This is the "durable before told" rule [09 §3.2 R9] applied to the gate. If the write fails (allowance full, disk error), the mode ends and that action goes through the ordinary decision, so it gets a card or a deny. Under the mode, **no action is allowed without a record** (REASONED; red control `allow_before_record`).

`bypass.challenge` / `bypass.alive` are **not** audit events (§5.2).

### 5.2 Storage: who causes, who is charged, what it can block

This follows the model in [07 §1.3-1.8]: a fixed part that never refuses for space, eight seats, and charges to the causer. The audit lanes failed four times on "one party fills another's storage". Each row says what filling it can block and what it can never block.

| Record (at member V) | Causer | Charged to | Bound (PROPOSED) | Filling it can block | It can never block |
|---|---|---|---|---|---|
| V's own `bypass.round`, `consent`, `active`, `paused`/`resumed` | V | **mode-control reserve** inside V's own seat: 32 records kept back, like the closing checkpoint [07 §1.4 b] | 32 records × ≤ 1,028 bytes ≈ 32,896 bytes (computed, not run) | V starting further rounds this session (safe: no mode) | V's withdrawal or end record (next row); anything in the fixed part |
| V's own `bypass.withdraw` and `bypass.ended` | V | **2 records always held back** in the reserve, refilled after each end | 2 records | nothing: the **effect** (mode off) is applied first, in memory and in the state file, before any storage step, and the reserve guarantees the record | the withdrawal itself |
| X's `bypass.consent` / `bypass.withdraw` / `bypass.round` received at V | X | **fixed part**: one slot per member for X's latest round, one for X's latest consent-or-withdraw, replaced in place (latest-state, as in [07 §1.5 D]) | 2 × 31 slots × 1,028 bytes = 63,736 bytes (computed, not run) | nothing (fixed part) | V applying X's withdrawal: **effect first, store second**, a new step 3b in [07 §1.7]'s order (after the signature check, before space) |
| Lease challenges and answers | V (challenge), X (answer) | memory only, never stored | one outstanding challenge + one latest answer per member: ≤ 31 × 2 × ~200 bytes (computed, not run) | nothing | anything |
| V's `action.decided` / `action.finished` under the mode | V (V chose the mode) | **mode allowance**: half of V's free part [07 §1.4 b] | 2,534,443 / 2 = 1,267,221 bytes ≈ 940 ordinary events at ~1,350 bytes, i.e. ~470 actions at two events each (computed, not run; real sizes UNKNOWN as in [07 U2]) | the mode on V: full → `bypass.ended {log_full}`, then the ordinary gate | V's other free recording (the other half), V's normal-mode actions, roster changes, evidence, withdrawals |
| X's mode actions as V holds them | X | X's seat at V (as every X event, [07 §1.4 b]) | one seat | V keeping copies of X's actions; then V signs `held_from: None` and **X's mode ends** | every other seat, the fixed part, V's own log |
| Stream display buffer | — | memory, ring per machine | last 500 lines per machine (PROPOSED) | nothing (old lines drop; the log has them) | anything |

**Effect on [07]'s numbers.** The new fixed slots take 63,736 bytes out of the eight seats, about 7,967 bytes per seat (computed, not run), and the mode-control reserve comes out of V's own seat. [07 P1-P9] must be re-run with the new tables. Add a P10: *a withdrawal is applied whatever the state of every seat and table* (red control `withdraw_after_store`).

**What a hostile member can cost V here.** Two fixed slots, replaced in place; one lease answer in memory; signature checks (rate-limited by the daemon); and, by steering V's agent through text (which the mode accepts), V's mode allowance, which ends V's mode. That is the same denial a withdrawal would cause. **They can never** block V's withdrawal, V's roster changes, V's evidence, or V's recording outside the allowance.

**What it costs in session length (computed, not run).** At ~470 actions per mode allowance, an agent making 6 tool calls a minute uses it up in about 78 minutes; at 2 a minute, about 4 hours. With your earlier ruling of "fixed capacity now, seal and continue next" [05], long sessions in this mode will meet the end of the allowance first. This is a reason to build seal-and-continue [07 §1.12] before or with this mode (DQ-5).

---

## 6. Who can do what

### 6.1 A hostile peer (holds its own roster key)

| Attempt | Possible? | Why not / what limits it |
|---|---|---|
| Turn the mode on for the other person's machine | **No** | M's mode needs M's own consent, made only on M's console with words another human read aloud (§2.2, §6.3). No wire message type can carry M's consent: messages are typed and a peer message can never carry a decision about another's machine [04 §3.4 rule 3]. |
| Forge M's consent toward a third member | No, without M's signing key | consents are signed by roster keys; the KEY-THEFT attack (§7 A14) is the exception |
| Keep M's mode on after M withdraws | **No** | M's withdrawal is local and comes first (§2.3) |
| Keep M's mode on after a third member Y withdraws | No | Y's withdrawal reaches M directly over the Y↔M channel, or Y's lease lapses at M within L |
| Keep **its own** machine in the mode after others withdraw | **Yes**: it is its machine, and it could equally run a patched daemon | the others' daemons stop answering its challenges. If it reports honestly, its signed headers show `why = bypass` after the withdrawal, which is evidence. It gains no power over anyone else's machine |
| Widen M's mode (wider profile, longer time) | No | M enforces its owner's profile and duration. A different `profile_hash` means no agreement. The shortest duration wins |
| Replay an old consent | No | it is bound to `round_id`, `roster_hash` and `session_id`; an ended mode needs a new round |
| Bring the mode back after a roster change | No | consents name the roster hash |
| Stop the mode (withdraw, stall leases, fill its seat, steer the agent into refusals) | Yes | denial only; always allowed by design |
| Steer M's agent while the mode is on | **Yes — this is what the mode accepts** | the refusals of §3.3; the tripwire; the stream; presence; the time limit. Residual R-B1 |

### 6.2 A hostile relay

| Attempt | Possible? | Why not / what limits it |
|---|---|---|
| Hold back a withdrawal | **For at most L = 45 s** | challenge/answer timed on M's clock (§2.4). The relay cannot forge `bypass.alive` (signed, inside the channel) or produce answers to nonces it never saw answered |
| Delay answers to stretch the lease | No | timing starts when the challenge is sent |
| Replay old `bypass.alive` | No | the answer names M's fresh nonce; channel counters reject replays [09 §2.1] |
| Hold back consents or rounds | Yes: the mode does not start | safe direction |
| Hold back a roster change so the mode outlives it | Only on members not yet told; the convener sees unacknowledged versions [04 §3.5] | the members already told end it at once; the leases of the departed member stop |
| Forge a consent | No | signed; channel-bound |

### 6.3 A ghost-text or prompt-injected agent trying to turn it on

The human's act must not be forgeable by an agent. These things together make it so (REASONED unless cited):

1. **No agent-reachable path carries "on".** The IPC socket that the hook, the MCP server and `coagentd ctl` use has verbs for `bypass off` and read-only `bypass status` only. There is no MCP tool for it. No wire message type turns on another machine's mode. "On" exists in one place: the console's authenticated WebSocket (loopback, `Host` allow-list, `Origin` check, `HttpOnly; SameSite=Strict` cookie, per-socket CSRF token [03 §9.1 row D]). **By type**, in the style of `GateWitness` [p1p: docs/DAEMON.md:362-366, 537-541]: `BypassConsent` has private fields and one `pub(crate)` constructor in the console module. It takes a `WordsVerified` value that only the agree-words check produces. A source audit like `release_audit` checks that this stays true (red control `ipc_on_verb`).
2. **Words from another human.** The agree-words for M come from another member's console and travel by voice (§2.2 step 3). M's agent never sees them: they are not in any tool result, inbox item or IPC answer. A peer's agent does not see them either, since they are console-only on the peer's machine. To forge the act, an agent would need both a driven console **and** words spoken on a call it cannot hear.
3. **Before the mode is on, every route to the console is gated.** Every shell command is a red card [05]. Browser and desktop-control tools are untaught tools and therefore red cards [main: src/known.rs:93-95]. `~/.coagent/**`, where the console's bootstrap and the socket live, is hard-denied for writes and for command text that names it [main: src/patterns.rs:63-67; docs/POLICY.md:56-57]. The new word list (§3.3) refuses command text naming the CoAgent programs, so `coagent open` run by an agent is refused rather than shown as a card.
4. **Peer text is never shown as status.** The consent dialog shows only daemon-verified consents. "Kam agreed" in chat is chat [03 §5.5].
5. **Once on, an agent cannot extend or widen.** There is no extend verb. Any change is a new round with words, and the profile is fixed at consent. An agent that kills the daemon blocks itself [G2]. One that edits settings is hard-denied for file tools and blocked at `ConfigChange` for project settings [U6] (user-scope settings were not tested, UNKNOWN U-B4).
6. **What remains:** a person can be talked into it ("Sam says switch approvals off"). The dialog's fixed text and the spoken words, which make the two people talk, are the only defence. Under S1, a shell command can read the device key or the console's cookie store by a spelling the scan misses (§7 A14, A15).

---

## 7. Attack list for a future independent check

Each line is something to try, with what must happen.

1. **A1 single consent.** Only M agrees; X never does. The mode must not start on M or X.
2. **A2 stale roster.** X consents on roster v4; the convener issues v5; replay X's consent. No agreement.
3. **A3 profile widening.** X sends a consent with Profile B while M chose A. Nothing starts; M never applies B.
4. **A4 withheld withdrawal.** A relay passes everything except X's `bypass.withdraw` and then X's answers. M must end within L by its own clock. Try delaying earlier answers by up to L−1 s first (the delay-stretch attack). Red control `lease_from_arrival` must let it stretch.
5. **A5 replayed lease answer** across rounds and across reconnects. It must not count.
6. **A6 withdrawal under full storage.** Fill X's seat at M, fill the fixed slots with valid replacements, make M's disk writes fail, then send X's withdrawal. The mode ends at M (effect before store).
7. **A7 IPC "on".** Every same-user client of the socket (`coagentd ctl`, a forged hook, a forged MCP client) tries every verb and argument shape. No way to "on". Source audit plus mutated copies.
8. **A8 MCP elicitation spoof.** The agent tries to answer or trigger a console-only dialog. If elicitation is used for anything near this, prove the model cannot answer it (UNKNOWN U-B2; the console-only default avoids it).
9. **A9 agent drives the console** via a browser or desktop tool before the mode is on: a red card at every step, and the words still missing.
10. **A10 restart revival.** Kill M's daemon while the mode is on and start it again. The mode stays off, and an end record cause `restart` exists. Red control `restart_restores_mode`.
11. **A11 roster churn.** Join, provisional deputy admission, removal, role change: each must end the mode on every member, including one that learns late.
12. **A12 refusal bypasses.** For every §3.3 class, try every spelling the policy's existing attack suites use (`q01`/`r2`-`r5b` tests [main: tests/]) with the mode on. Each is denied; none becomes allow.
13. **A13 exclusions and hard denies under Profile B.** Still denied.
14. **A14 key theft under S1.** A shell command reads the device signing key by a spelling the scan misses and shares it. Measure what a stolen key forges: consents toward third members, not M's own mode on M. Decide whether the key must sit in a keychain that asks the user.
15. **A15 cookie theft under S1.** Read the browser's cookie store for the console origin. Check whether that gives "on" without words (it must not: the words are the second factor).
16. **A16 nested ungated agent.** `claude -p …` or another agent CLI through the shell while the mode is on: refused by the word list, plus a probe for spellings that slip past. Report what an unbound nested session can do.
17. **A17 allow without record.** Make the audit write fail between decision and allow. The action must not run with `why = bypass`.
18. **A18 presence spoofing.** The agent produces "terminal input" or a console heartbeat to keep a paused mode running. Measure and report. The impact is limited to resuming a mode the humans agreed to.
19. **A19 tripwire evasion.** Spread refusals to stay under 3 per 10 minutes. Report.
20. **A20 clock games.** Change M's wall clock forward and back. Expiry and lease use monotonic time.
21. **A21 equivocation.** X tells M "consent" and Y "withdraw" for one round. Each daemon acts on what it holds; the heads exchange catches the fork [04 §3.9].
22. **A22 unbound session.** A second Claude Code session on M, not bound, makes calls while the mode is on. It must get no mode allow (needs session binding, §9.1; the preview decides every session [p1p: docs/DAEMON.md:513-515]).
23. **A23 witness theft under the mode.** `inbox_read` is allowed, so witnesses are always fresh. A same-user process consumes one within the TTL [p1p: docs/DAEMON.md:543-546]. Report what it gets.

---

## 8. INTERPRETATIONS for Kam (each with the alternative)

- **I-B1 (D1, the open question).** *Default:* the hard refusals hold (Profile A, Friday's recommendation). *Alternative:* Profile B, where only the gate's own files and your excluded paths are refused and credentials, permission-mode changes, flagged shares and untaught tools are all allowed. Under B a misled agent can read and send your keys without a card.
- **I-B2 (D2).** *Default:* the mode overrides your "every terminal command asks" ruling only with the sandbox ticked (S3). *Alternatives:* S1, commands run freely with best-effort text checks; S2, commands keep asking.
- **I-B3 (D3).** *Default:* "both users" means **every member of the session**, observers included, since they are the people watching. *Alternative:* only members who can address agents (guests and hosts); observers neither block nor need to agree.
- **I-B4.** *Default:* `sudo`/privilege is refused in Profile A. *Alternative:* allowed, as other T3 classes are.
- **I-B5.** *Default:* the mode covers **every machine at once**: each person's agreement includes their own machine. *Alternative:* a person may agree "for the others' machines, not mine" (useful in Assist, where only one side works).
- **I-B6.** *Default:* the mode covers the agent sessions bound at activation; a new agent session or a `/clear` that changes the session id needs a new round. *Alternative:* it follows whatever session is bound on M.
- **I-B7.** *Default:* any link drop longer than L **ends** the mode. *Alternative:* it **suspends** and resumes when leases return within, say, 5 minutes.
- **I-B8.** *Default:* the owner's 10 minutes away **pauses** M. *Alternative:* it ends the mode.
- **I-B9.** *Default:* while the mode is on, requests from members reach the agent without being held (as a grant's `requests: auto_accept` [03 §5.3]). *Alternative:* requests are still held for the owner and only actions are approval-free.
- **I-B10.** *Default:* turning the mode on raises every member's share level to at least summaries. *Alternative:* share levels stay as set, and members at *nothing* see only that the mode is on.
- **I-B11.** *Default:* the agree-words are required (§2.2). *Alternative:* the console click alone, with no words. Easier, but then a driven console is enough (§6.3).
- **I-B12.** *Default:* the mode allowance is half the free part. *Alternative:* all of it (longer mode, but a steered agent can then use up your normal recording too).

## 9. DESIGN QUESTIONS (not decided here)

- **DQ-1.** Is an OS user-presence prompt (Touch ID or password; Windows Hello) available to the daemon as a third factor? UNKNOWN. A spike on each platform would settle it.
- **DQ-2.** Should a long mode re-confirm (e.g. words again every 2 hours) instead of a single limit of up to 8 hours?
- **DQ-3.** Does a mode allow count toward the "3 consecutive T3 denials auto-revoke" counter [03 §5.4]? Here only refusals count.
- **DQ-4.** Phone approval devices [03 §6.7]: may a paired phone give consent? Default no (the console only) until its pairing is reviewed.
- **DQ-5.** Order of building: seal-and-continue [07 §1.12] first, given §5.2's session-length figures?
- **DQ-6.** Should the stream also be pushed as OS notifications, for a person who has the console closed but is at the machine?

### UNKNOWN, and what settles each

| # | Unknown | What settles it |
|---|---|---|
| U-B1 | hook `allow` in an interactive default-mode session with no allow rule: is there a Claude Code dialog? | one U1-style interactive run (§3.6) |
| U-B2 | MCP elicitation flow (unverified in [03 §3.4]) | not needed if consent stays console-only |
| U-B3 | OS presence prompt from a daemon | DQ-1 spike |
| U-B4 | `ConfigChange` blocking of `user_settings` edits (not tested in [U6]) | U6 rig run against a scratch user scope |
| U-B5 | cost of one synced audit write per allowed action | measure in the build; if large, batch writes per turn, still syncing before allow |
| U-B6 | real event sizes, and so the §5.2 action counts | [07 U2]'s measurement |
| U-B7 | does `/clear` issue a new session id ([03 §3.4] said M0 would check; I did not find the result) | read the M0 report or run once |

## 10. Build outline (for after Kam's word)

### 10.1 Prerequisites (not in the preview [p1p: docs/DAEMON.md:589-595])

Session binding (`${CLAUDE_SESSION_ID}`); the console with its authenticated WebSocket; the audit log wired into the daemon; `PostToolUse` capture; the multi-member roster in the daemon. The mode must not ship on the preview alone, because the preview decides every Claude Code session that loads the plugin [p1p: docs/DAEMON.md:513-515].

### 10.2 Files and minimal API

| Crate / file | Change |
|---|---|
| `coagent-policy/src/state.rs` | `pub bypass: Option<BypassState>`; `BypassState { consent_set_id: String, profile: BypassProfile, expires_at: Timestamp }`; `BypassProfile { refuse: RefuseSet /* A or B */, shell: ShellOption /* S1 S2 S3 */, sandbox_ticked: bool }` |
| `coagent-policy/src/engine.rs` | steps [7c]/[7d]; `AllowWhy::Bypass { consent_set_id }`; `DenyReason::BypassRefused { reason: &'static str }`; `would_have_been(&Assessment) -> (Tier, Vec<Reason>)` for the record |
| `coagent-policy/src/patterns.rs` | `BYPASS_REFUSED_WORDS` with a reason line; generated into POLICY.md §4 (the `t12_docs` check) |
| `coagent-policy/docs/POLICY.md` | §2 gains [7c]/[7d]; §10 gains the mode |
| `coagent-daemon/src/bypass.rs` (new) | rounds, consents, leases (challenge/answer, monotonic), activation, ends, presence pause, tripwire; the only setter of `State.bypass` |
| `coagent-daemon/src/gate.rs` | record-before-allow for `AllowWhy::Bypass`; on a failed record, clear and re-decide |
| console module | the round dialog, words entry, `BypassConsent` constructor (private), stream view, Off |
| `coagent-proto` / wire | `bypass.round`, `bypass.consent`, `bypass.withdraw`, `bypass.challenge`, `bypass.alive`; a decoder rule: none of them changes the receiver's own consent |
| `coagent-audit` | event kinds; the two fixed tables; mode-control reserve; mode allowance; step 3b (apply withdrawal before space) |
| IPC | `bypass off`, `bypass status` only |

### 10.3 Tests

Policy (no model): `t20_bypass_order` (stop, pause, bound, exclusion, hard deny and closed link all come first; [7b] keeps its own why); `t21_bypass_refusals` (each §3.3 class, with the existing spelling corpora); `t22_bypass_allows` (every other T0-T3 becomes allow; shell per S1/S2/S3); `t23_bypass_expiry` (`now ≥ expires_at` → ordinary decision); a property test (for any state and action, the mode never turns a step-[5]/[6] deny into an allow, and Profile A never allows a refused class).

Daemon (no model): consent needs all members; profile mismatch; replay across rounds; lease lapse with delayed answers; withdrawal before store with storage full; roster change ends; restart does not restore; presence pause/resume; tripwire; record-before-allow with a failing store; IPC has no "on" (source audit + mutated copies).

Live red tests against real Claude Code ([03 §11.3] item 2 style, smallest model, nightly): mode on → a Write in the workspace is created with no card (in `-p`); a write to `.claude/settings.json` is denied; a credential read is denied; with the daemon killed → blocked; the same in `bypassPermissions` [G1]; with the mode off → back to asks/denials.

### 10.4 Red controls (each must fail its own test's assertion)

`bypass_one_consent_enough`, `bypass_skips_hard_deny`, `bypass_skips_exclusion`, `bypass_allows_credentials`, `bypass_allows_untaught`, `bypass_on_closed_link`, `peer_profile_wins`, `lease_from_arrival`, `withdraw_after_store`, `roster_change_keeps_mode`, `restart_restores_mode`, `ipc_on_verb`, `allow_before_record`, `expiry_by_wallclock`.

---

## 11. Residual risks, plainly

- **R-B1 — A steered agent acts without a card.** While the mode is on, a peer's text (or anything in the context) can lead the agent to do anything outside the refused classes: delete, push, deploy, send. This is what the mode means. The backstops are the refusals, the stream, the time limit, presence and the tripwire.
- **R-B2 — Shell commands are opaque.** Under S1, the refusals are best-effort for shell. Under S3 they are as good as the sandbox, and the sandbox does not exist on native Windows.
- **R-B3 — A person can be talked into it.** The spoken words make it a conversation; they do not make it wise.
- **R-B4 — A hostile peer can run its own machine in the mode after everyone withdraws.** That is its machine. The evidence is in its signed log, if it logs honestly.
- **R-B5 — Fixed recording capacity** ends long sessions in this mode early (§5.2) until seal-and-continue exists.
- **R-B6 — The device key is readable by a shell command** (A14), unless it sits in a keychain that asks the user.

## Appendix: what I read

Design: `03_architecture-design.md` §2-3.6, §5, §9, §11.3; `04_design-revision-rulings.md` §3.4-3.9, §6.4-6.5; `05_kam-rulings-2026-11-17.md`; `06_design-addendum-rulings-2026-11-17.md` §2.8.4, §6; `07_audit-storage-accounting-redesign.md` §0-3; `09_daemon-recovery-rules-design.md` §1-3.2. Code at main `36537eb`: `crates/coagent-policy/src/engine.rs`, `state.rs`, `patterns.rs`, `known.rs`, `action.rs`, `docs/POLICY.md` §1-2; spikes `G1-deny-blocks-write`, `U1-permission-dialog-race`, `U2-ask-in-bypass-dontask`, `U6-configchange-block`, `G2-dead-daemon-blocks`. Branch `p1p-gate` at `f2603fd`: `crates/coagent-daemon/src/gate.rs`, `docs/DAEMON.md` §4 "Peer text to the agent", §8. Git read verbs only; nothing in the repository was changed; no model was run.
