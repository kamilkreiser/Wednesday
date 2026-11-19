# CoAgent "both agree" mode: independent review of design 11 (2026-11-20)

Status: review only. Nothing built, nothing run, no card posted. Design 11 is not rewritten here.

## BLUF

1. Design 11 is NOT ready to build past the policy crate: 6 Blockers, 8 Majors, 6 Minors, 4 Notes (§3).
2. As written the mode cannot work: the agent's own inbox read and every send are refused classes, and three refusals switch the mode off (F-1, F-2).
3. As written it is unsafe in four places: a whole-folder search reads excluded files (F-3); the sandbox rule rests on a tick nobody checks, and a wrong tick gives the option the owner ruled out (F-6); the gate's own folder is readable (F-7); files that run later can be planted (F-8).
4. A deputy's admission does not change the roster, so it neither ends the mode nor makes the newcomer agree (F-4). The time limit runs on the wall clock, and sleep is not handled (F-5).
5. Section 5 (recording) predates seal-and-continue: every seal would end the mode, and its charging rule contradicts the standing one (F-12).
6. The three rulings close I-B1 to I-B3 and kill Profile B, S1 and S2 as choices (§1). Eleven new questions are the owner's (§5); the first is "who checks the sandbox".
7. Buildable today with no prerequisite: the policy-crate decision steps, refused classes, tests, property and red controls, shipped dark (§4.1).

---

## 0. How to read this

- **[main: file:line]** was read with `git show 32beb563837341560b908d9ba5b0a60de240d860:<path>` in the repository `coagent/2_Project_Files`. Design 11 cites `36537eb`; `git diff --stat 36537eb 32beb56 -- crates/coagent-policy` is empty, so its policy line numbers are the same lines at today's main.
- **[p1p: file:line]** was read at `b7e8da4` (local head of `p1p-gate`, a merge of main into lane A's `fa10a14`). Design 11 cites `f2603fd`; where a line number moved I give the `b7e8da4` number. `git diff --stat 32beb56 b7e8da4 -- crates/coagent-policy` is empty: lane A does not touch the policy crate.
- **[seal: file:line]** was read at `841c4459e5cdda0637e4df2cdf77ba133f51bd18` (`m3-audit-seal`).
- **TESTED-BY-READING** = I read the cited lines and they say what the claim says. **REASONED** = my argument, not read in this repository and not run. **UNVERIFIED** = I could not read a source for it.
- Nothing was built, run or changed. No model was run.
- Severity: **Blocker** = design 11 cannot be built as written without breaking a ruling or a stated safety property, or the mode cannot work. **Major** = a real hole or a missing piece with a bounded effect. **Minor** = wrong or unclear text. **Note** = for the record.

---

## 1. The three rulings applied to design 11

Rulings (the owner, 2026-11-20 07:08-07:09): D1 "a — Yes, they all still hold" (Profile A). D2 "a — Only with the sandbox on" (S3). D3 "a — Every member, observers included". Seal: IS1 "a — Only you or your settings decide"; IS6 "a — Each on their own schedule".

### 1.1 Places the rulings fix (text that changes from "default" or "recommended" to RULED)

| Section of 11 | Text today | After the rulings |
|---|---|---|
| header, "Friday's reading" | "One question to Kam is still open: do the hard refusals … still hold" | closed by D1: they hold |
| §1 "What still stops an agent" | "(Profile A, Friday's recommendation and this design's default)" | ruled; the word "Profile" can go |
| §1 "The honest catch" | "Section 3.4 offers three choices. I recommend …" | ruled S3. The catch itself stays true and is now the centre of finding F-6 |
| §1 "Your decisions, in order" | D1, D2, D3 listed as open | all three closed; what is left is §8 I-B4 to I-B12 and this review's §5 |
| §2.2 step 1 | profile = "A or B, the terminal option S1/S2/S3, the presence rule" | profile = the presence rule and the duration only; the refuse set and the shell rule are fixed, not negotiated |
| §2.2 step 5, second bullet | "(D3: observers too, by default)" | ruled: `required_members` is every member, observers included. See F-4 for provisional members |
| §3.2 table | column "Mode on, Profile A (default)" | the only mode column |
| §3.2 row "T3, shell command" | "per §3.4 (S1/S2/S3)" | allowed only where the sandbox is on; elsewhere it asks, as today |
| §3.4 row S3 | "(recommended)" | ruled |
| §8 I-B1, I-B2, I-B3 | "Default … Alternative …" | closed, defaults ruled |
| §5.2 last paragraph and §9 DQ-5 | "a reason to build seal-and-continue before or with this mode" | seal-and-continue is built on `m3-audit-seal`; IS1 and IS6 are ruled. §5 must be rewritten against design 10, see F-12 |

### 1.2 Text that is now dead (remove, do not build)

1. §3.2: the whole column "Mode on, Profile B (alternative)".
2. §3.3 last paragraph: "Profile B keeps only steps [5] and [6] …".
3. §3.4: rows S1 and S2 **as choices**. S2's behaviour survives as the fallback on a machine where the sandbox is not on (and on native Windows). S1's inner rule ("allowed unless a deny scan hits") survives only as what happens inside S3.
4. §6.3 item 6, second sentence: "Under S1, a shell command can read the device key …" (re-aim it at "the sandbox is not really on", F-6).
5. §7 A3 as worded ("X sends a consent with Profile B"): keep the test, reword to "a consent whose profile hash differs". §7 A13 ("exclusions and hard denies under Profile B"): dead; A12 covers it.
6. §7 A14 and A15 "under S1": re-aim at S3 with the sandbox absent or not covering the path.
7. §8 I-B1, I-B2, I-B3: the "Alternative" halves.
8. §10.2: `RefuseSet /* A or B */` and `ShellOption /* S1 S2 S3 */` in `BypassProfile`. One refuse set; the shell rule is one boolean fact about this machine, not a profile field (F-6 item 4).
9. §11 R-B2 first sentence ("Under S1 …").
10. §9 DQ-5 (the order question is answered: seal is built first).

### 1.3 What the rulings do NOT settle

- I-B4 to I-B12 and DQ-1 to DQ-4, DQ-6 of design 11 are still open, unchanged.
- D2 says "only with the sandbox on". It does not say **who establishes that the sandbox is on**. Design 11 answers "the owner ticks a box". That is this review's first safety finding (F-6) and the first question in §5.
- D3 says "every member". Whether a person the deputy let in provisionally is a "member" for this purpose is UNDECIDED (the owner). See F-4.

---
## 2. Design 11's claims, checked at source

| # | Claim in 11 | Where | Result |
|---|---|---|---|
| C1 | Decision order [1] to [13]; a new step fits after [7b] and before [8] | §3.1 | TESTED-BY-READING [main: crates/coagent-policy/src/engine.rs:620-742]. Markers [1] :624, [2][3] :630, [4] :641, [5] :652, [6] :666, [7] :677, [7b] :698, [8] :704, [9][10] :716, [11] :734, [12] :740 |
| C2 | Exclusions and hard denies come first, so they hold | §3.1, §3.5 | TRUE for a direct hit [main: engine.rs:652-672]. **FALSE for a recursive read whose root contains an excluded path**: that case is not a deny, it is the flag `may_read_excluded`, guarded only at steps [9] to [11] [main: engine.rs:396-404, :710-715, :930, :1034]. A step placed before [8] skips the guard. Finding F-3 |
| C3 | Hard deny covers "the gate's own files" | §1, §3.5 | TRUE for writes, deletes, moves and for command text that names them; **not for reads**: the hard-deny test runs only when `role.is_write()` or the role is `Mentioned` [main: engine.rs:407-417]. Finding F-7 |
| C4 | Each refused class comes from an existing assessment reason | §3.3 | TESTED-BY-READING: `CredentialPath`/`CredentialFolder` [main: engine.rs:447-451], `CriticalSpelling` [:452-454], `PermissionModeChange` [:542-544, :565-571], `SandboxBypass` [:545-547], `ShareFlaggedOrUnscanned` [:513-517], `UnknownTool` via `Strict::NotTaught` [main: known.rs:107-116], `Privilege` [main: engine.rs:553-555]. All reasons are kept in a set [main: engine.rs:298-313], so a refuse test on reasons is possible |
| C5 | "With the mode on, `inbox_read` is allowed, so a witness is made on the allow path" | §3.5 row "Liveness invariant" | **FALSE.** `inbox_read` and `wait` have no entry in `KNOWN_TOOLS`: the only two own tools taught are `share` and `send` [main: known.rs:60-61]; every other `mcp__` tool is `NotTaught` [main: known.rs:93-95]. Lane A's own document says so: "With the policy as merged both tools are strict: every read asks" [p1p: docs/DAEMON.md:523] and lists the two entries under "Not in the preview" [p1p: docs/DAEMON.md:600-603]. "A tool the gate has not been taught" is a refused class of §3.3, so in the mode both tools are **denied**, and a deny records no witness [p1p: crates/coagent-daemon/src/gate.rs:370-377]. Finding F-1 |
| C6 | A share the scanner flags is refused, others are allowed | §3.2, §3.3 | The policy rule is "T3 unless `share_flagged == Some(false)`" [main: engine.rs:515]. `classify` always sets `share_flagged: None` [main: crates/coagent-policy/src/action.rs:562], and nothing in the daemon, the hook or the MCP server sets it (`git grep share_flagged b7e8da4 -- crates/coagent-daemon/src crates/coagent-mcp crates/coagent-hook`: no line). So today every `send` is "unscanned", and in the mode every `send` would be refused. Finding F-2 |
| C7 | "`decide` checks `now < expires_at` itself", and (§7 A20) "expiry and lease use monotonic time" | §3.1, §7 A20, §10.4 `expiry_by_wallclock` | **The two statements contradict each other.** The policy's only clock is `Timestamp`, "whole seconds since the Unix epoch" [main: crates/coagent-policy/src/time.rs:1-7], and the gate passes the wall clock: `now_unix` "is the wall clock in seconds (the policy's `now`)" [p1p: gate.rs:295-303, :366]. Finding F-5 |
| C8 | "A hook cannot see whether the sandbox is on [main: src/state.rs:93-100], so the tick is the owner's word" | §3.4 | TESTED-BY-READING: `Sandbox { On, Off, Unknown }`, "owner-declared … a hook cannot see it: M0 outcome 5" [main: state.rs:93-99]; "Hook input and environment are identical with the sandbox on and off. `SANDBOX_RUNTIME=1` exists only inside the sandboxed command" [main: docs/M0-OUTCOMES.md:29-30]. Also read: `State.sandbox` is set once, to `Unknown` [main: state.rs:226], and **read nowhere** in the policy crate or the daemon (`git grep -i '\.sandbox\b\|Sandbox::' 32beb56 -- crates/coagent-policy/src crates/coagent-daemon/src`: that one line only). The owner's tick has no code path today. Finding F-6 |
| C9 | The preview daemon passes only the owner's `--exclude` globs, so a credential path is a T3 ask, not a deny | §3.3 row 1 | TESTED-BY-READING [p1p: gate.rs:220-232]. `default_exclusions()` is offered, not applied [main: patterns.rs:364-375] |
| C10 | `ConfigChange` is always blocked | §3.5 | TESTED-BY-READING [p1p: gate.rs:304-320] |
| C11 | Fail closed when the daemon is absent | §3.5 | TESTED-BY-READING in the document [p1p: docs/DAEMON.md:566-571]; I did not read `crates/coagent-hook/src/main.rs` line by line: UNVERIFIED at source, verified by the check (gate_P1P_verdict.md line 28, "FAIL CLOSED: HOLDS") |
| C12 | `permission_mode` is "used only to lower the surface, never to raise trust" | §3.5 | TESTED-BY-READING [main: action.rs:142-143; engine.rs:611-617] |
| C13 | Grant counters are not spent by a mode allow | §3.1 | TESTED-BY-READING [main: state.rs:287-298] |
| C14 | The preview decides every session that loads the plugin | §10.1, A22 | TESTED-BY-READING [p1p: docs/DAEMON.md:513-515]; one policy `State` per Claude Code session id, at most 64, least recently used dropped [p1p: gate.rs:383-404]. Finding F-10 |
| C15 | "a deputy's provisional admission … ends at once on the verified object", recorded as `{roster_change: v}`; "consents name the roster hash" | §2.3, §2.5, §6.1 | **The mechanism named does not fire.** "the deputy never signs a roster version" [main: docs/ROSTER.md:395-397]; "Only the starter signs roster versions" [:401]; provisional members live in a combined view, "the roster plus the provisional members" [:410-413], with its own hash that moves with each admission [:456-458]. A provisional admission produces no roster version and leaves the roster hash unchanged. Finding F-4 |
| C16 | Browser and desktop-control tools are untaught, therefore refused | §3.3, §6.3 item 3 | TESTED-BY-READING for the rule [main: known.rs:76-83, :93-95]: any name not in the list is strict |
| C17 | `~/.coagent/**` is hard-denied for writes and for command text naming it | §6.3 item 3 | TESTED-BY-READING [main: patterns.rs:62-66; engine.rs:407-417]. Reads: see C3 |
| C18 | The witness is consumable by any same-user client inside its TTL | §7 A23 | TESTED-BY-READING [p1p: docs/DAEMON.md:547-550]; confirmed by the check as P1-7 |
| C19 | Hook `allow` semantics (U-B1) | §3.6 | UNVERIFIED, as design 11 says. New fact from the live demo: Claude Code 2.1.328 "starts in auto mode by default", and for a `Write` the gate's `ask` showed Claude Code's own dialog (`p1p_review/live_demo_report.md`, Surprises 1 and 7). Whether a hook `allow` with no allow rule is silent in that version is still unmeasured. Finding F-13 |
| C20 | The console's authentication [03 §9.1 row D] | §6.3 item 1 | The console is not built. Design 03 line 671 (row D) lists the defences and ends: "malware running as the same OS user (already game over, out of scope)". Finding F-9 |

---

## 3. Findings

Count: **6 Blocker, 8 Major, 6 Minor, 4 Note.**

### Blockers

**F-1 (Blocker). In the mode, the agent can never read its inbox, and the tripwire then ends the mode.**
- What: `inbox_read` and `wait` are untaught tools (C5). "Untaught" is a refused class. So the mode turns today's ask into a deny for exactly the two calls that carry peer text. Three refusals in ten minutes end the mode (§2.3 tripwire), so an agent that checks its inbox three times switches the mode off. The mode fails safe and does nothing useful.
- Where: 11 §3.3 row "A tool the gate has not been taught", §3.5 row "Liveness invariant", §2.3 tripwire. [main: known.rs:60-61, :93-95]; [p1p: gate.rs:370-377; docs/DAEMON.md:523, :600-603].
- Smallest change: give `mcp__plugin_coagent_link__inbox_read` and `mcp__plugin_coagent_link__wait` their `KNOWN_TOOLS` entries (already owed: lane A's BACKLOG entry "`KNOWN_TOOLS` entries owed for this product's own `inbox_read` and `wait`", read at `b7e8da4`). Add both to §10.1 as a prerequisite and correct §3.5. Who decides the tier of the two entries: the coordinator, under the existing ruling "one entry per tool that exists in the tree" [main: BACKLOG.md:556-560].

**F-2 (Blocker). In the mode, every `send` is refused, because nothing scans a share.**
- What: C6. The scanner that would set `share_flagged = Some(false)` is not wired anywhere. "A share the scanner flags, or one it could not scan" is a refused class, so with the mode on no agent can send to another. Each refused send also counts toward the tripwire.
- Where: 11 §3.3 row "A share the scanner flags", §10.1 (the scanner is missing from the prerequisites). [main: engine.rs:513-517; action.rs:562].
- Smallest change: add "the secret scanner, run by the daemon on every outgoing share before `decide`" to §10.1. Until it exists the mode must not be buildable past the policy crate. Design 03 puts "gated shares" in M2 (03 line 917).

**F-3 (Blocker, safety). The mode lets a recursive search read excluded files.**
- What: C2. A `Grep` or `Glob` whose root is a folder above an excluded path is not a deny. It carries `may_read_excluded`, and today that flag blocks every automatic allow (session approval, memory, grant) and forces an ask. Step [7d] sits before those guards and allows it. So "paths you excluded are still refused" (§1) is false for the most common search an agent makes.
- Where: 11 §3.1 "Exclusions … hold in both profiles", §1 BLUF. [main: engine.rs:396-404, :684, :710-715, :930, :1034]. The owner-visible cost of this guard is already recorded [main: BACKLOG.md:62-66].
- Smallest change: [7c] refuses when `a.may_read_excluded` is true (a new refused class, "a search that could read excluded files"). Add red control `bypass_allows_may_read_excluded`. Note the consequence for the owner: with the default credential exclusions, every recursive search of the workspace is refused in the mode (`**/.env*` can match under any folder). This needs a card (§5 Q-4).

**F-4 (Blocker). A deputy's admission does not change the roster, so the mode does not end and the newcomer never agrees.**
- What: C15. Design 11 binds consents to `roster_hash` and ends the mode "on the verified object" as a roster change. A provisional admission is a separate object signed by the deputy; the roster version and hash stay the same. As written: (a) the mode on M does not end when the deputy lets someone in; (b) a later round's `required_members`, built from "the member keys of M's current roster version" (§2.2 step 5), leaves the provisional member out, so the mode runs with a member who never agreed. That breaks D3 ("every member").
- Where: 11 §2.2 steps 1, 4, 5; §2.3 row "Roster changes in any way"; §2.5 row 2; §6.1 "Bring the mode back after a roster change". [main: docs/ROSTER.md:395-397, :401, :410-413, :456-458].
- Smallest change: replace "roster version and hash" by "member view and view hash" everywhere in §2: the consent carries the view hash (`SHA-256("coagent-roster-view-v1" ‖ 0x00 ‖ roster hash ‖ hash of the last admission)`, which equals the roster hash when there is no admission [main: docs/ROSTER.md:456-458]); `required_members` is every key of the view; an accepted admission ends the mode with cause `{admission}`; a drop of provisional members by the starter's next version ends it as a roster change. Add attack A11b: "provisional admission while the mode is on" and red control `admission_keeps_mode`.
- Confirmations asked for: **an admission counts** only after this change; as written it does not. **Observers**: they are roster entries with a role [main: docs/ROSTER.md:47], so they are in `required_members` once D3 is applied; a provisional observer is covered by the view. Whether a provisional member is one of "every member" is UNDECIDED (the owner, §5 Q-5); the safe reading built here is yes.
- Dependency: the daemon does not carry admissions yet and still calls `admit`, not `admit_view` [main: BACKLOG.md:634-638, D-7]. The deputy must be wired in before the mode's daemon part.

**F-5 (Blocker). The time limit runs on the wall clock, and neither clock is safe alone.**
- What: C7. As written `decide` compares the wall clock with `expires_at`. Anything that sets the machine's clock back (the owner, a time-sync step, a same-user command where that is allowed) lengthens the mode. Design 11's own test A20 and red control `expiry_by_wallclock` assume the opposite. Moving everything to a monotonic clock is not enough either: on a laptop the monotonic clock can stop while the machine sleeps (REASONED from general knowledge of the platform; not read or measured here), so a 60-minute mode could still be "on" after a night with the lid closed, and the 10-minute "owner away" timer would not have advanced.
- A hostile relay or peer cannot touch either clock on M. The risk is local: clock changes and sleep.
- Where: 11 §2.2 step 5 ("counted on M's clock"), §3.1 last paragraph, §4.2, §7 A20, §10.4. [main: time.rs:1-7]; [p1p: gate.rs:295-303, :366].
- Smallest change: (1) the daemon keeps the deadline in BOTH clocks and the mode ends when EITHER says so; (2) a wall-clock step backward, or a gap between two ticks larger than a stated bound (a sleep), ends the mode with cause `{clock}`; (3) `decide` keeps its wall-clock check as a backstop only; rename the red control to `expiry_one_clock_only`; (4) say in §2.3 that closing the lid ends the mode. Who decides (4): the owner, it is visible (§5 Q-6).

**F-6 (Blocker, safety). S3 rests on a tick nobody checks; when the tick is false the owner gets exactly what he ruled out.**
- What the ruling says: terminal commands run without approval "only with the sandbox on". What design 11 builds: they run without approval when the owner has **ticked** "my Claude Code sandbox is on, set to deny the credential and gate paths". These are different things.
- When the tick is false (the sandbox is off, was switched off later, or is on but does not hide the credential and gate folders): every shell command is allowed after a text scan. That is option S1, which the owner did not choose. A command the scan does not recognise can then read the device key and the browser's console cookie, edit Claude Code's settings, or start an ungated agent. Design 11 says this itself for S1 (§3.4 row S1, §6.3 item 6, §7 A14-A16).
- More ways the tick can be false without anyone lying (all UNVERIFIED here: none is covered by a spike in this repository, so each needs a measurement before it is relied on):
  1. the sandbox setting can exempt named commands from the sandbox; the hook sees no flag for that (only `dangerouslyDisableSandbox` on the call is visible [main: action.rs:144-145, :555-557]);
  2. the tick is made once; the sandbox can be changed inside Claude Code afterwards, and whether that fires `ConfigChange` is unmeasured (U6 tested project settings only [main: BACKLOG.md:13-17]);
  3. `PowerShell` and `Monitor` are shell tools for the policy [main: known.rs:88-90]; whether the sandbox wraps them is unmeasured;
  4. the sandbox's default read rules may allow reading the whole disk; the tick's second half ("set to deny the credential and gate paths") is a claim about a deny list the gate never reads.
- Can the gate verify instead of trusting? The hook cannot (C8). Two routes exist, both to be proven by a spike before any build:
  - **Route P, a probe inside each command (recommended to spike first).** `SANDBOX_RUNTIME=1` exists inside a sandboxed command [main: docs/M0-OUTCOMES.md:30]. If a `PreToolUse` hook may return a changed tool input together with its decision, the gate can put a fixed prefix in front of every mode-allowed command that (a) stops unless `SANDBOX_RUNTIME` is `1`, and (b) stops unless a canary file the daemon keeps inside its own data folder and inside one credential folder is NOT readable. Then each command proves, where it runs, the two facts S3 needs. UNVERIFIED: that a hook can rewrite the input; that an earlier command cannot plant the variable for a later one; that the prefix cannot be escaped by the command text behind it. Each is one spike row.
  - **Route R, the daemon reads the settings.** The daemon runs as the same user and can read the settings files and compute "sandbox enabled, these paths denied". It cannot see settings given on the command line, so this is a cross-check, not proof.
- Smallest change to design 11: (1) the rule becomes "shell is allowed in the mode only when the gate has itself verified the sandbox for this command; the owner's tick is necessary, never sufficient"; (2) until Route P is proven, S3 behaves as S2 on every machine (shell keeps asking) and the dialog says so; (3) only the `Bash` tool can qualify, never `PowerShell`, `Monitor` or a command field on another tool; (4) the tick is a fact about one machine: it is NOT part of the profile hash (otherwise one member without a sandbox blocks agreement for everyone, or members silently differ), but each consent discloses it, and every dialog shows "Sam: terminal commands still ask"; (5) use the existing `State.sandbox` field for it instead of a second `sandbox_ticked` field (C8); (6) red control `bypass_shell_without_verified_sandbox`.
- Who decides: the owner, since this is the safety boundary he ruled on (§5 Q-1, Q-2).

### Majors

**F-7 (Major, safety). Reads of the gate's own folder are allowed in the mode.**
- What: C3. The hard-deny list protects writes. A `Read` of a file in the daemon's data folder is an ordinary "read outside the workspace": T2, an ask today, an allow in the mode. That folder holds `inbox.json`, "unread peer messages" [main: docs/DAEMON.md:50], so the agent can read peer text with no witness and no taint, which is the liveness rule §3.5 says is unchanged. It also holds `session.json`, `contacts.json`, `gate.json`, and later the console's bootstrap secret (design 03 row D: "One-time bootstrap token"). The identity key itself is caught, by luck of its name: `identity.key` [main: docs/DAEMON.md:47] matches the credential pattern `*.key` [main: patterns.rs:174]. The same holds for Claude Code's own configuration folder (hard-denied for writes [main: patterns.rs:32-51], readable).
- Where: 11 §1 ("writes to the gate's own settings …" is accurate; the reader will take it as "the gate's files are protected"), §3.5 liveness row, §6.3 items 1 and 3.
- Smallest change: a new refused class in [7c], "any access to a gate file": a read-role target that matches the hard-deny set. That needs one new bit in the assessment (today the match is skipped for reads). Red control `bypass_allows_gate_reads`. Outside the mode nothing changes.

**F-8 (Major, safety). The mode allows writes that run code later, outside the gate and after the mode has ended.**
- What: §3.2 allows the T3 class "`.git`/build-file writes". That class is one list [main: patterns.rs:217-362] and it includes login agents (`~/Library/LaunchAgents/**`, :351), programs early on the path (`~/.local/bin/**`, :352), `~/.gitconfig` (:341-345), editor and terminal start-up files (:353-361), and every `.git/**` path (:218-222; `core.hooksPath`, `core.fsmonitor`, `core.sshCommand` live in `.git/config`). A file tool, not shell, writes these, so the sandbox does not apply. Code planted there runs with the owner's rights, with no gate, after the mode is over, and can then rewrite the gate. Design 11 refuses `sudo` for exactly that reason ("can rewrite the gate from outside", §3.3 Privilege row).
- Where: 11 §3.2 row "T3, other reasons", §3.3.
- Smallest change: add to the refused classes "a write to a file outside the workspace that runs code later" (`Reason::RepositoryConfigWrite` where the pattern's root is the home folder) and "a write under `.git`". Workspace build files (`Makefile`, `package.json`, `build.rs`, `CLAUDE.md` …) are ordinary work for an agent; whether they stay allowed is the owner's call (§5 Q-3).

**F-9 (Major). "Agree-words in the console" is weaker than §6.3 states, and the console's authentication does not exist yet.**
- (a) The console is unbuilt (design 03 M3). Its stated defences are against web pages, not against a process running as the same user, which design 03 puts out of scope (line 671). In the mode's threat model the agent IS a same-user process whenever a shell command runs. Before the mode is on, each such command is a red card the human approves, plus whatever the owner put on the exact-command list, which runs with no card [main: engine.rs:698-703].
- (b) The console's secret (bootstrap token, cookie store) would be a file. Under F-7 a `Read` of it is an ordinary ask before the mode. So §6.3 item 3 ("every route to the console is gated") holds only as "gated by a card the human may approve without knowing what the file is".
- (c) The words do not work as written. §2.2 step 3: X's daemon "sends a commitment `H(secret)` in its consent" and reveals the secret so that M's typed words can be checked. But M must type X's words BEFORE M's consent exists, and X must type M's words before X's consent exists. With two people each consent waits for the other's secret, and each commitment travels inside a consent that cannot be made yet. The order is circular. Also unstated: when a daemon reveals its secret (before or after its own human acted), how many wrong tries are allowed, and how much the three words are worth in bits.
- (d) What the words do prove once fixed: that whoever typed on M's console heard from someone who could see another member's console. They do not prove a human typed them if the agent can read M's daemon memory or the decrypted channel, and they do not stop the agent asking its own human for the words (`AskUserQuestion` is a taught tool [main: known.rs:69]) and then needing only the console.
- Is it enough? As one factor of two (an authenticated console AND words from another person), it is a reasonable design for a preview between people who trust each other. It is not an authentication of the human. The real one is an operating-system presence prompt (design 11 DQ-1), which nothing here can forge.
- Smallest change: (1) fix the order: every daemon commits to its per-round secret when it JOINS the round (no human act), secrets are revealed only after all commitments are held, consents come last; reuse the pairing ceremony's commit-then-reveal code rather than a new one (`crates/coagent-crypto/src/sas.rs` exists at main; I did not read it: UNVERIFIED); (2) three wrong tries end the round; (3) state the entropy; (4) console secrets go under the F-7 refused class and under the credential list so that even before the mode a read of them is a red card; (5) decide DQ-1 before the console is designed (§5 Q-9).

**F-10 (Major). The mode's on/off state must not live in the per-session policy state.**
- What: §3.1 puts the mode in `State.bypass`. The daemon keeps one `State` per Claude Code session, up to 64, drops the least recently used and re-creates it on next sight [p1p: gate.rs:383-404]. Lane A's safety argument for dropping is "the state holds no approval the daemon could lose" [p1p: gate.rs:8-11]. With the mode in `State`: switching off must reach every copy (one missed copy stays on), and a re-created state must be told whether the mode is on (a second source of truth). §2.3's promise "the state flag clears in memory first" has no single flag.
- Also: which sessions does the mode cover? I-B6 says "the agent sessions bound at activation". The preview has no binding [p1p: docs/DAEMON.md:513-515], so an unrelated Claude Code session that loaded the plugin would get the mode too (11 §7 A22 names it).
- Where: 11 §3.1, §10.2 row `state.rs`.
- Smallest change: the mode is ONE value in the daemon. `decide` receives it as a separate argument (or the gate copies it into the state for the length of one call, as it already does for `link` and `context_from` [p1p: gate.rs:357-365]). `decide` stays pure. The value carries the set of bound session ids; a session not in the set gets no mode step. Session binding stays a hard prerequisite.

**F-11 (Major). Consents have no lifetime, and a restart can rebuild a consent set from disk.**
- What, replay across rounds: fine as designed; a consent names its `round_id`.
- What, replay across rosters: fine once F-4 is applied (view hash).
- What, inside one round: the signed consent (§2.2 step 4) carries no time and no expiry. "The round lapses after 5 minutes" is stated once, with no word on whose clock or who enforces it. X can agree at 09:00 and leave; if M agrees at 15:00 and X's daemon still answers challenges for that round, every activation condition holds. Nothing in the text makes X's daemon stop answering for a round that never started.
- What, across restarts: §5.2 stores each member's latest round and latest consent-or-withdraw in fixed slots on disk, and M's own consent is an audit event. After M's daemon restarts, a design that "holds a valid consent from every member for this round" can be satisfied from disk, provided leases come back. §2.3 says the mode "is never restored" but gives no rule that prevents re-activation from stored consents.
- Where: 11 §2.2 steps 1, 4, 5; §2.3 "M's daemon restarts"; §5.2 row 3; §6.1 "Replay an old consent".
- Smallest change: (1) a round is single-use on each machine: once M has activated or ended for a `round_id`, that id is dead on M (kept in the end record); (2) activation needs M's own consent made in THIS run of the daemon (the `WordsVerified` value lives in memory only and has no way to be loaded); every round id found on disk at start is dead; (3) each daemon stops answering challenges for a round that it has not seen become active within 5 minutes of its own consent, by its own clock; M enforces the same 5 minutes from its first sight of the round; (4) attack A2b "restart, then replay stored consents" and red control `consent_survives_restart`.

**F-12 (Major). Recording: §5 was written before seal-and-continue and collides with it, with the causer rule, and with pinned numbers.**
1. **A seal closes the store for a window.** The daemon may make "no other mutating call on this member" between the two seal calls (design 10 §2.2, precondition D-S2; BACKLOG entry D-S2 [seal: BACKLOG.md], read in the diff against main). In that window step 2 writes a file of up to 64 MiB. Record-before-allow cannot write, so by §5.1 "the mode ends and that action goes through the ordinary decision". So every seal on M ends M's mode, and since §5.2 says a long session "will meet the end of the allowance first", the mode cannot outlive its own allowance even with the seal built. Smallest change: a decision that arrives during a seal waits for it, up to a bound below the hook's 10-second deadline [p1p: docs/DAEMON.md:556]; past the bound it gets the ordinary decision (a card), and the mode does NOT end.
2. **Who refills the mode allowance?** IS1: only the owner or the owner's settings seal. So "log full during the mode" has two outcomes that §2.3 does not distinguish: with an automatic setting the daemon seals and the mode continues; with a manual setting the mode ends with cause `{log_full}` and the owner must seal and start a new round. UNDECIDED which is the default (the owner; it is design 10's DQ-S1). §5 Q-7.
3. **A peer can now drive seals.** Design 10 allows a seal on "V's own free part … reaching a threshold" and forbids one driven by a peer (D-S1). In the mode, a peer's text steers V's agent, V's agent fills V's allowance (11 §5.2 "What a hostile member can cost V"), and with an automatic setting V writes a new file each time. That is the class D-S1 exists to prevent, reached through the mode. Smallest change: a bound on seals per round (PROPOSED: one), after which the mode ends.
4. **IS6 ends modes.** "Each on their own schedule" means a member who seals less often than M "stops keeping copies" of M's activity until it seals (design 10 §0 item 6, I-S6). §2.3 row "A member signs that it no longer keeps M's records" then ends M's mode, and only that other member can cure it. With 8 members the mode lasts as long as the slowest sealer's seat. State this in §1 and decide whether "not keeping" should end the mode or only show a warning (§5 Q-8).
5. **Who is charged.** §5.2 charges the mode's actions to V ("V chose the mode"). The standing rule is the opposite for anything a peer caused: "the daemon must record every event that was not a local human act with `record_for(causer)`" [main: BACKLOG.md:403-407, D5]. In the preview every action is `Origin::Member(peer)` while a session is active [p1p: gate.rs:353-356]. The two rules give different numbers and different "who can fill what". UNDECIDED (the owner: it changes ruling-level accounting, design 07 I-A9; the coordinator may not pick).
6. **New fixed slots and reserves move pinned numbers.** §5.2 adds 63,736 bytes of fixed slots and a 32-record reserve. The fixed part is pinned to a 8-byte range in the seal brief (R5: `FIXED_BYTES` within 17,940,329..17,940,336) and every seat size is pinned by tests. This is a full audit-crate round with its own property run (07 P1-P9 and design 10's seal properties), not a row in a table.
7. **In-flight and parallel calls.** The allow is recorded before the action; the finish is recorded after. If the allowance fills between the two, an allowed action has no finish record. Parallel tool calls reach the gate at the same time. Smallest change: reserve room for the finish record at the moment of the allow; the reservation is taken under one lock.
8. **Cost.** One forced write per allowed action; the daemon's own measurement is about 5 ms per forced write on this volume [main: docs/DAEMON.md:98-99]. Acceptable; say so instead of U-B5's "if large, batch".
- Where: 11 §5.1, §5.2, §2.3 rows `log_full` and `peer_not_keeping`, §9 DQ-5, §11 R-B5.

**F-13 (Major, planning). The mode's whole value depends on an unmeasured host behaviour.**
- What: U-B1. If a hook's `allow` still produces Claude Code's own prompt when the user has no allow rule, then "approvals off" does nothing unless the person also changes their own Claude Code settings, which CoAgent blocks and must never do for them. The live demo adds that the host's default mode changed between 2.1.325 and 2.1.328 (C19).
- Where: 11 §3.6, §9 U-B1.
- Smallest change: make U-B1 the first act of the round (one interactive run, smallest model, in the style of the U1 rig), before any daemon or console work for the mode. The policy-crate part (§4 below) does not depend on it.

**F-14 (Major). Lease and expiry must be checked at the decision, not by a timer.**
- What: §2.4 says M "treats X's agreement as live while M holds an answer to a challenge M sent less than 45 s ago". If a timer task clears the mode and the daemon is busy (a forced write, a seal, a long IPC call; pairing setup already stalls the engine task for up to about 50 s [main: BACKLOG.md:262-266, G10]), a hook decision can be answered after the lease has lapsed.
- The 45 seconds itself: the argument in §2.4 holds (REASONED, I agree): timing starts at M's send, a relay cannot forge or pre-date an answer, and an answer after X's withdrawal does not exist. What a hostile relay can do: hold a withdrawal for at most 45 s; end anyone's mode at will by dropping challenges (safe direction). What a hostile peer can do: keep answering after its human walked away (a lease proves the daemon, not the person; say so in §2.4). Sleep and clock changes: F-5.
- Also a contradiction: §2.3 "The link closes … ends at once" and §2.5 "Link drop shorter than L: no change". One of them must name the daemon's own state. Smallest change: "ends at once" applies to the session ending or `ClosedTainted`; a transport drop is judged by the lease alone.
- Smallest change: one function `mode_live(now_monotonic, now_wall)` evaluated inside every gate decision under the same lock as the off switch; timers only produce the end record sooner. Red control `lease_checked_by_timer_only`.

### Minors

**F-15 (Minor).** Step [7d] as worded "covers every remaining T0, T1, T2 and T3 action" (§3.1). Under S3 a shell command on a machine without a verified sandbox must fall through to [8]. Write the step as: refused class → deny; shell and not verified → continue to [8]; else allow.

**F-16 (Minor).** The tripwire (3 refusals in 10 minutes) will fire in ordinary use: a reply that names an excluded path is refused (live demo, Surprise 2: the policy matches free text against exclusions by name [main: engine.rs:393-395; action.rs:214, :522]), and under F-3 so is every recursive search. Count only refusals of the classes that signal an attack (credentials, gate files, permission mode, sandbox bypass, privilege), or raise the figure. PROPOSED numbers need the owner's eye (11 §8 has no entry for the tripwire).

**F-17 (Minor).** D3 makes observers agree. An observer therefore needs a running daemon and a console, and an observer's absence (closed laptop) blocks or ends the mode for everyone through the lease. State it in §1. I-B5 ("my machine too?") matters more for observers and is still open.

**F-18 (Minor).** §2.3 lets the agent call "off", and any member open a round. Nothing limits rounds per hour except the 32-record reserve (§5.2). A steered agent can turn the mode off and a peer can re-propose at once: a fatigue loop for the humans. Add a floor between rounds proposed by the same member (PROPOSED: 2 minutes).

**F-19 (Minor).** §3.3's new word list (`coagent`, `claude`, …) is described as stopping "an agent driving its own gate … by the plain route". Under S3 with a verified sandbox it is a second layer; without one, shell asks anyway. Keep the list, but delete the sentence in §6.3 item 3 that relies on it ("so `coagent open` run by an agent is refused rather than shown as a card"): before the mode is on, the list is not consulted at all (it is a mode refusal), so that command is a red card like any other.

**F-20 (Minor).** §3.2 row "T2 … reads outside the workspace" becomes allow. Together with `WebFetch` (allow) this sends any file not on the credential list to any host with no card: `Read` a document in the home folder, then fetch a URL with the content in it. §11 R-B1 covers "send" in general; the BLUF's "what still stops an agent" should say in plain words that only listed credential folders are protected, not "your files". Owner question §5 Q-10.

### Notes

**F-21 (Note). What in the hard-refusal list is only as strong as text matching.**

| Refused class | For file tools, web, MCP | For a shell command |
|---|---|---|
| Hard-deny paths | exact after path normalisation [main: engine.rs:407-417] | text only: the path must appear as a word [main: engine.rs:385-392] |
| Excluded paths | exact; plus F-3 for recursion | text only, by name |
| Credential paths | exact for the paths on the list [main: patterns.rs:129-209]; a credential stored anywhere else is not known | text only |
| Odd spelling | a heuristic of the normaliser | text only |
| Permission-mode change | exact for `ExitPlanMode` [main: known.rs:91-92] | six word prefixes [main: patterns.rs:425-435] |
| Sandbox switched off | exact: a field on the call [main: action.rs:144-145] | same field; a sandbox exemption set elsewhere is invisible (F-6) |
| Flagged share | as strong as the scanner, which is pattern matching with known misses [main: BACKLOG.md:360, :389] and is not wired (F-2) | n/a |
| Untaught tool | exact by name [main: known.rs:76-83] | n/a |
| Teammate / remote subagent | exact on the call's fields; a helper's own definition can set its isolation unseen [main: BACKLOG.md:561-570] | n/a |
| Privilege | n/a | six words [main: patterns.rs:386-389]; any other route to more rights is unseen (REASONED) |
| New word list (CoAgent programs, agent CLIs) | n/a | words only |

So with the sandbox verified, the shell column is backed by the sandbox for reads and writes of files. It is NOT backed for the three word-only rows (permission flags, privilege, agent CLIs): a nested agent started from an allowed command by a spelling the list misses runs inside the sandbox but outside this gate's session (11 §7 A16). That residual stays; say it in §11.

**F-22 (Note).** A hostile relay that withholds an admission or a roster version from M keeps M's mode on while the membership has changed elsewhere (11 §6.2 row 5). The effect is bounded: M shares nothing with a member it does not know. Under F-4 add: the deputy's admission chain has no acknowledgement step that M's mode could watch; the lease of a member who has ended the mode stops, which ends M's within 45 s. That is the real bound; say it.

**F-23 (Note).** §5.2's figures (940 events, 470 actions, 78 minutes) are computed from estimated event sizes. The check for this mode must measure them (11 U-B6), because the tripwire, the reserve and the "ends early" text all hang on them.

**F-24 (Note).** `Agent`/`Task` (a local subagent) is a taught tool at T2 [main: known.rs:62-63], so the mode allows it. Its own tool calls "come back through this gate one by one" by the list's own reason line; whether they carry the parent's session id (and so the mode) is not stated anywhere I read: UNVERIFIED. It decides whether I-B6's "sessions bound at activation" covers subagents.

---

## 4. What can be built and tested NOW, and what must wait

### 4.1 Buildable now: the policy-crate part (no daemon, no console, no model)

All of it is inside `crates/coagent-policy` plus `docs/POLICY.md`, on today's main. The policy crate is untouched by both preview lanes (§0), so there is no merge dependency.

1. **The mode as data.** A `BypassView { consent_set_id, expires_at, bound, shell_verified }` passed to the decision (F-10: not a field of the long-lived `State`, or a field the caller sets for one call). No profile enum (D1, D2 ruled).
2. **Steps [7c] and [7d]** after [7b] and before [8] (C1), written as F-15 says.
3. **The refused classes**: the nine of 11 §3.3, plus F-3 (`may_read_excluded`), F-7 (reads of gate files), F-8 (home-level and `.git` writes that run later). Privilege stays refused (I-B4's default) until the owner says otherwise.
4. **`AllowWhy::Bypass`, `DenyReason::BypassRefused`, `would_have_been`** (tier and reasons for the record).
5. **The word list** `BYPASS_REFUSED_WORDS` with its row in `docs/POLICY.md` §4 (the `t12_docs` check).
6. **The two `KNOWN_TOOLS` entries** for `inbox_read` and `wait` (F-1), with their rows in `docs/POLICY.md` §3a. This also closes lane A's BACKLOG entry and removes most of the preview's prompts.
7. **Tests**: `t20_bypass_order`, `t21_bypass_refusals` (each class, with the existing spelling corpora), `t22_bypass_allows`, `t23_bypass_expiry`; the generated property "for any state and action, the mode never changes a deny at steps [1] to [6] into anything else, never allows a refused class, never allows a shell command unless `shell_verified`, and with the mode absent `decide` returns exactly what it returns today" (the last clause is a differential against the unchanged function, the strongest guard that nothing outside the mode moved).
8. **Red controls**, one feature each, red on its own assertion: `bypass_skips_hard_deny`, `bypass_skips_exclusion`, `bypass_allows_may_read_excluded`, `bypass_allows_credentials`, `bypass_allows_gate_reads`, `bypass_allows_untaught`, `bypass_allows_home_persistence`, `bypass_on_closed_link`, `bypass_shell_without_verified_sandbox`, `bypass_ignores_expiry`, `bypass_unbound_session`.
9. **Dark by construction.** Nothing in the tree can switch it on: the daemon never builds a `BypassView`. A source check in the daemon's tests (in a later lane) or a line in the brief's final-tree checks (now) proves no crate other than the policy crate's own tests names the type.

What this part does NOT need decided: Q-1/Q-2 (the policy takes "shell verified" as an input and never computes it), the words, the lease, the recording. What it DOES need decided before the build brief goes out: Q-3 (which later-running writes are refused) and Q-4 (recursive searches), or the brief builds the safe reading and lists both as "INTERPRETATION, built as stated, open for the owner".

### 4.2 Must wait

| Part | Waits for |
|---|---|
| Rounds, consents, leases, ends (`bypass.rs` in the daemon) | a revised design 11 §2 (F-4, F-5, F-9c, F-11, F-14); the multi-member roster and the deputy carried by the daemon (D-7); session binding (F-10) |
| The human's act (dialog, words, Off button) | the console (design 03 M3); the decision on an OS presence prompt (Q-9) |
| Shell without approval | the sandbox probe spike (F-6 Route P) and the owner's Q-1/Q-2; until then shell asks |
| Any `send` in the mode | the secret scanner in the daemon (F-2) |
| Record-before-allow, the stream's "result" line | the audit log wired into the daemon (D5, D-S1 to D-S3, resume limits); `PostToolUse` capture; a revised §5 (F-12); an audit-crate round for the new slots and reserves |
| "No prompt at all" | the U-B1 measurement (F-13) |
| Wire messages | `coagent-proto` types; they follow the revised §2 |
| Live red tests | everything above |

---

## 5. Decisions still the owner's (candidate cards; nothing is posted)

Each is a plain question with options and my recommended default.

- **Q-1. How does CoAgent know your sandbox is on?** (a) It checks by itself on every command, and until it can, terminal commands keep asking. (b) You tick a box and it believes you. **Recommend (a).** With (b), a wrong tick silently gives the "commands run freely" option you did not choose.
- **Q-2. If the check finds the sandbox on but not hiding your key folders and CoAgent's own folder: treat it as off?** (a) Yes, commands ask. (b) No, on is on. **Recommend (a).**
- **Q-3. With approvals off, may an agent write files that run later by themselves?** (a) Not in your home folder and not in a project's `.git` folder; project build files (Makefile, package.json and the like) are allowed. (b) None of them. (c) All of them. **Recommend (a).** (c) lets a misled agent plant something that runs after the mode has ended, outside every check.
- **Q-4. With approvals off, a search across a whole folder could read a file you excluded. What should happen?** (a) The search is refused (safe; with the default key-file exclusions this refuses most whole-project searches). (b) It still asks you. (c) It runs. **Recommend (b)**: a card for this one case breaks "no approvals" the least while keeping your exclusions true. (a) is what gets built if you do not answer.
- **Q-5. Someone your deputy let in while you were away: must they agree too before approvals can be switched off again?** (a) Yes. (b) No, only people you admitted yourself. **Recommend (a)**; it follows your "every member" answer.
- **Q-6. Does closing the laptop lid, or the clock being changed, end approvals-off?** (a) Yes, always. (b) Only when the time limit has really passed. **Recommend (a).**
- **Q-7. Your log fills up while approvals are off.** (a) CoAgent follows your filing setting: on "automatic" it files the log away once and carries on; on "ask me" the mode ends and you are told. (b) The mode always ends. **Recommend (a), with at most one automatic filing per agreement.**
- **Q-8. Another member's computer has stopped keeping copies of your activity (its log is full and they have not filed it away). Does that end approvals-off on your machine?** (a) Yes (design 11). (b) No, you see a warning and that member sees "not recording Kam". **Recommend (a) for now**: watching includes recording. It means the mode lasts only as long as the slowest person's log.
- **Q-9. Should switching approvals off also need your fingerprint or password on your own computer?** (a) Yes, where the computer offers it. (b) No, the console click and the spoken words are enough. **Recommend (a), after a one-day test that it can be done on macOS.** It is the only step an agent cannot fake.
- **Q-10. With approvals off, may an agent read files outside the project folder?** (a) Yes, except the listed key folders and CoAgent's own (design 11). (b) It still asks. (c) Refused. **Recommend (a), and say in the dialog that only the listed folders are protected.** (b) is safer and costs cards.
- **Q-11. Who pays for the recording space the mode uses: the person who asked for the work (today's rule) or the owner of the machine (design 11)?** **Recommend today's rule.** UNDECIDED; it changes an accounting ruling.
- Still open from design 11, unchanged: I-B4 (is `sudo` refused: default yes), I-B5 (does your agreement cover your own machine: default yes), I-B6 (new agent session needs a new round: default yes), I-B7 (link drop ends or suspends: default ends), I-B8 (10 minutes away pauses or ends: default pauses), I-B9 (requests reach the agent unheld: default yes), I-B10 (everyone sees at least summaries: default yes), I-B11 (words required: default yes), I-B12 (half or all of the free space: default half), DQ-2, DQ-3, DQ-4, DQ-6.

For the coordinator (build mechanics inside the rulings): the tier of the two `KNOWN_TOOLS` entries (F-1); where the mode value lives (F-10); the bound on a decision that waits for a seal (F-12 item 1); the tripwire's counted classes (F-16) if the owner leaves the figure alone.

---

## Appendix: what I read, and what I could not

Read: design 11 whole; design 10 §0, §2.1-2.2, §7; design 08 whole; design 03 §12 table and line 671; `p1p_review/live_demo_report.md` whole; `p1p_review/gate_P1P_verdict.md` findings table; `m1_review/gate_M3_DEPUTY_verdict.md` findings table. Code at `32beb56`: `crates/coagent-policy/src/engine.rs` :36-75, :130-200, :296-878; `state.rs` whole; `patterns.rs` :1-470; `known.rs` whole; `time.rs` :1-60; `action.rs` by search only (:132-171, :214, :522, :555-562); `docs/POLICY.md` §2 :37-60; `docs/DAEMON.md` :42-110; `docs/ROSTER.md` :386-460; `docs/M0-OUTCOMES.md` :29-32; `BACKLOG.md` :1-359 whole, :360-638 titles and the entries cited. At `b7e8da4`: `crates/coagent-daemon/src/gate.rs` whole; `docs/DAEMON.md` :440-603; the BACKLOG additions. At `841c445`: the BACKLOG additions; signatures in `crates/coagent-audit/src/session.rs` and `store.rs`.

Not read (so nothing here rests on them): designs 04, 05, 06, 07, 09 (I relied on design 11's and 10's quotations of them); `crates/coagent-hook/src/main.rs`; `crates/coagent-crypto/src/sas.rs` and `words.rs`; the spikes' RESULT files; `m1_review/gate_M3_AUDIT_SEAL_verdict.md` (12 bytes at the time: the check was still running). Any Claude Code behaviour beyond the spikes' stated outcomes is marked UNVERIFIED where used.
