VERDICT: GO WITH NOTES — head 977627697655aef4fa20fd5031a6af9b5af31fb7

# QA gate M2-POLICY, round 6: the short check of addendum 7 (branch `m2-policy` @ 977627697655aef4fa20fd5031a6af9b5af31fb7)

Independent gate, 2026-11-18. Findings only. I fixed, merged, committed and pushed nothing, and wrote nothing in the
project folder. My clone (`git clone --branch m2-policy <project>/2_Project_Files`) is at
`/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_policy_r6/clone`.
Its HEAD is asserted as `977627697655aef4fa20fd5031a6af9b5af31fb7` (TESTED: `git rev-parse HEAD`). `git ls-remote origin`, run from the
project folder, gives `m2-policy` = `9776276…` and `main` = `da4655edc4ea17c4f7f8e944d0bac9754b8f8317`. Scope: the delta
`0ea9b95..HEAD` and the points in the commission. The round-5 135,408-decision campaign was not repeated; its central
test ran again, unchanged, inside `check.sh`.

## BLUF

1. The round-5 Major is closed as a class. `Monitor`, and any unknown or third-party tool whose input carries a text
   `command`, now gets exactly the terminal tool's red, one-time card, or its refusal. I found no odd input shape that
   gets less.
2. The four Minors are fixed. Each fix has a test that goes red when I remove the fix. The edited timing test still
   fails when I add a real 60 ms slowdown.
3. Nothing was weakened. The merge of main lost nothing and added nothing foreign. `check.sh` passes (639 passed,
   0 failed), and every red control goes red.
4. Two Minors remain for the owner's card. A person's first name is still in one line of `docs/POLICY.md`. The seat's
   tool table also misdescribes two real host tools: `ExitWorktree` can delete a worktree, and `Agent` can run a
   subagent in a remote cloud, outside the gate's view.
5. Both of those tools still get the ordinary card, which can be batched and approved for the session. Neither passes
   shell text to this machine, so neither breaks the "every terminal command asks" ruling.
6. An unknown tool that names its command field anything other than `command` (`cmd`, `script`, `code`, …) still gets
   the ordinary card. No current host tool I could see does this. It is a Note for the owner's open question.

Findings: **0 Blocker, 0 Major, 2 Minor, 7 Note.**

## 1. Findings

"Strict" = `Deny`, or `Ask` with tier T3, `batchable = false`, `read_delay_secs = 5`, no `AllowForSession` option,
and `ShellExpansion` as the first reason (the round-5 definition).

| id | sev | what | input that shows it | exact output seen | file:line | how |
|---|---|---|---|---|---|---|
| r6-m1 | Minor | Item 8 (m4) is not complete. A person's first name is still in a docs line, a ruling citation. It was added at `0ea9b95`. The seat searched only the crate. The round-5 scan missed it too. The addendum (§3) says: "No person's name … in code, tests or docs." | case-insensitive scan of lines added in `da4655e..HEAD` | 1 hit, category "person's first name" (`gate_policy_tests_r6/hygiene_hits.txt`; matched text withheld) | `docs/POLICY.md:423` | TESTED: scan script (§7); `git blame` → commit `0ea9b95`; `git grep -i -w` on HEAD gives this line and nothing else in `docs/`, `crates/` or `BACKLOG.md` |
| r6-m2 | Minor | Surface table A7.2 is wrong for two REAL host tools, so its "what follows" misses two effects. (a) `ExitWorktree` (ii) is "UNKNOWN (… schema not read)". The host schema says `action: "remove"` deletes the worktree directory and its branch, and `discard_changes: true` throws away uncommitted work and commits. (b) `Task`/`Agent` (i) says "subagent whose own calls are hooked". The `Agent` schema in this session has `isolation: "remote"`: "launches the agent in a remote cloud environment". That subagent's commands run where this gate is not installed. Both tools are decided as unknown: T2, batchable, "allow for this session". | `ExitWorktree {"action":"remove","discard_changes":true}`; `Task {"prompt":"echo x >> ~/.zshrc","subagent_type":"general-purpose"}` | each: `ASK tier=T2 kind=Other batchable=true delay=0 options=["AllowOnce","AFS(ExactInput)","Deny","DenyWithReason"] reasons=[UnknownTool]` | STATUS_M2_POLICY.md A7.2 rows `ExitWorktree` and `Task`/`Agent`; `action.rs:426-433` (catch-all) | TESTED: `r6_gate::survey_command_field_names` (`SURVEY-REAL` lines, `logs/mine_head2.log`). READ: the `ExitWorktree` and `Agent` schemas exposed to this session (host version not printed). NOT verified: that 2.1.325's `Task` has `isolation: "remote"`. Severity: neither tool carries shell text that runs on this machine. The delete is limited to a worktree the session itself created. So this is a table error plus an owner question (n-r6-2), not a break of the 07:28 ruling. |
| n-r6-1 | Note | The command-field rule keys on one exact top-level key, `command`, with a string value. An unknown tool that puts the command anywhere else keeps the ordinary card: `cmd`, `script`, `shell`, `args`, `argv`, `run`, `exec`, `code`, `input`, `Command`, `commands`, `command_line`, `cmdline`, a nested `params.command`, or `command` as an array. On a third-party `mcp__` tool that card shows NO reason line at all (`reasons=[]`). No tool in the recorded host list (25 tools), and none in this session's schemas, has such a shape. A real but unverified example: an IDE-provided `mcp__ide__executeCode {"code": …}`, which is not in the recorded list. | `mcp__srv__exec {"cmd": "echo x >> ~/.claude/settings.json"}`; `MadeUpRunner {"script": …}` | `ASK tier=T2 kind=Service batchable=true delay=0 options=[…"AFS(ExactInput)"…] reasons=[]`; `ASK tier=T2 kind=Other … reasons=[UnknownTool]` | `action.rs:225` (`COMMAND_FIELDS = ["command"]`), `:228-237` | TESTED: survey, 420 rows. With a top-level string `command`, all 15 tool names are `DENY HardDeny`. The other 405 rows are all T2 (`logs/mine_head2.log`). Hypothetical shape, so this is a Note. See §8. |
| n-r6-2 | Note | Tools that make commands run LATER or ELSEWHERE are T2 cards that can be batched and approved for the session. The gate cannot see the commands they cause. `RemoteTrigger` (a remote routine), `Agent` with `isolation: "remote"`, and `Workflow` (a JS script that spawns agents) are the cases. `CronCreate`/`ScheduleWakeup` re-enter this session as prompts, and their tool calls are hooked again, so they are covered. `Skill`: its `` !`cmd` `` lines are "checked … against your permission rules" and "never prompt" (host skills docs). Whether `PreToolUse` fires for them is UNKNOWN, as the seat says. An agent cannot plant a skill: `.claude/**` writes are HARD-DENY (`patterns.rs:34`, `:39`). | `RemoteTrigger {"action":"create","body":{"prompt":"rm -rf ~",…}}`, `Workflow {"script":…}`, `Skill {"skill":"deploy","args":"prod; rm -rf ~"}`, `CronCreate {…}` | each `ASK tier=T2 kind=Other batchable=true … reasons=[UnknownTool]` | `action.rs:426-433` | TESTED (survey). READ: host docs copy `coagent/tools/docs_2026-11-16/skills.md` lines 757-800. Owner decision. |
| n-r6-3 | Note | Over-strict in the safe direction: ANY unknown tool whose input has a string `command` is execute/T3, even when that field is not executed. `Agent`, `Task`, `Workflow`, `SendMessage` and `TaskStop` with a `command` key each get `HardDeny` for a protected path. | `Task {"command": "echo x >> ~/.claude/settings.json"}` | `DENY HardDeny { reason: "Claude Code user configuration, hooks and plugins (the gate itself)" }` | `action.rs:426-433` | TESTED (survey) |
| n-r6-4 | Note | `crates/coagent-policy/Cargo.toml` replaces `[lints] workspace = true` with a COPY of the workspace lints (today only `unused_dependencies = "allow"`, equal to the root). It also adds a crate-wide `clippy::manual_is_multiple_of = "allow"` because a gate file trips it. A lint added to the workspace later will not reach this crate. Style lint only. | — | — | `crates/coagent-policy/Cargo.toml` `[lints.*]` | READ, plus a diff of the root `[workspace.lints]` at `da4655e` and HEAD |
| n-r6-5 | Note | No red-control row targets `q01_gate_attacks`, so the addendum's item 6 check on such rows has nothing to check. I covered it directly: under mutant MG (60 ms of extra work in `decide`), `q01::z_timing` and `t17::m1_blow_up_inputs_are_fast` both go red. | MG | `over the 50 ms bound: cat a/ x1000: 63.375791ms`; `len=1804 took 75.169333ms (limit 50ms)` | `q01_gate_attacks.rs:443`, `t17_addendum5.rs:508` | TESTED (`mutation/mut_MG.log`) |
| n-r6-6 | Note | The project folder's LOCAL `main` branch is `18005d6`, behind `origin/main` `da4655e` (`git ls-remote`). A clone of the project folder therefore reports a stale `origin/main`, and `git diff origin/main HEAD` in such a clone names roster and relay files. Against `da4655e` the diff is clean (§6). Whoever merges should diff against `da4655e`. | — | `git rev-parse origin/main` in my clone → `18005d63…` | — | TESTED |
| n-r6-7 | Note | A Monitor `ws` watch gets T3 PLUS `UnknownUrlHost`, one reason more than Bash for the same input. That is stricter, so it is allowed. My first equality assertion counted it as a difference; that was my test's error, corrected (§10). | `Monitor {"ws":{"url":"wss://x.invalid/s"},…}` | `ASK tier=T3 kind=Execute … reasons=[ShellExpansion, UnknownUrlHost]` | `action.rs` Monitor arm | TESTED (`g6_monitor_shapes`) |

## 2. Check 1: M1 closed as a class (TESTED, `r6_gate.rs`)

**(a) The eight M1 inputs of round 5**, plus `cat ~/.ssh/id_rsa`, `cat .env`, `base64 ~/.aws/credentials` and
`npm test` (12 rows).
- **Setup.** Each row is sent through `Bash` and `Monitor`, and through `MadeUpRunner`, `mcp__term__run`, `monitor`,
  `MONITOR`, `Monitor ` and `mcp__plugin_x_y__exec`. Hosts: `Posix` and `Windows`. States: every one `every_mode`
  gives. Each state also carries the call's own ExactInput approvals and an ExactCommand approval, and is run three
  ways: unlisted, owner-listed for Bash, and owner-listed for PowerShell.
- **Result.** `G6 M1 ROWS: 12 commands, 6048 decisions compared, 0 bad`.
  - `Monitor` equals `Bash` in variant, tier, kind, batchable, delay, options, reasons and deny reason. The one
    exception is a Bash allow from the owner's list; there `Monitor` is strict.
  - Every other tool name is at least as strict: a deny wherever Bash denies, otherwise strict T3.
- **Shown red** under MA2, MB, MB3, MB4 and MC (mutant table, §9).

With the default exclusions on the Console:

| row | `Monitor` decision |
|---|---|
| `echo x >> ~/.claude/settings.json` | `DENY HardDeny` |
| `cp payload.json .claude/settings.json` | `DENY HardDeny` |
| `cp evil.sh .git/hooks/pre-commit` | `DENY HardDeny` |
| `… >> ~/.zshrc` | `DENY HardDeny` |
| `sudo rm -rf /` | `DENY Excluded` |
| the other rows | strict T3 |

The same holds for every other tool name (log `mine_head2.log`, lines `Monitor …` / `MadeUpRunner …`).

**(b) Odd Monitor shapes** (`g6_monitor_shapes`, both hosts, Monitor compared with Bash given the same raw
`tool_input` text). Every shape below is strict.

| shape | Monitor decision |
|---|---|
| plain; extra fields + `run_in_background` | `DENY HardDeny "shell rc file"` |
| `dangerouslyDisableSandbox: true` | T3 `[ShellExpansion, SandboxBypass]` |
| `command` empty / missing / number / array / object / null; nested `params.command` | T3 (missing command) |
| 60 KB under the bound | T3 |
| 65 541 bytes | `DENY TooLargeToCheck` |
| **duplicate keys, dangerous value LAST** | **`DENY HardDeny`** (serde_json keeps the last value, as JavaScript's `JSON.parse` does) |
| duplicate keys, dangerous value first | T3 (the executed value is the harmless last one) |
| key `Command`, `COMMAND`, Cyrillic `о`, full-width `ｃ`, `command`+ZWSP | T3 (missing command; the host's schema, `additionalProperties: false`, would refuse these keys) |
| `ws` + `command` | `DENY HardDeny` |
| `ws` only | T3 + `UnknownUrlHost` |
| `\u007a` JSON escape in the command | `DENY HardDeny` |

0 bad after my test's correction (n-r6-7). The owner's list never helps another tool (`g6_owner_list_binds_tool`):
`npm test` (listed for Bash) and `Get-ChildItem` (listed for PowerShell), each with and without the sandbox flag,
through `Monitor`, `monitor`, `MadeUpRunner`, `mcp__term__run`, `Shell`, `bash`, `Bash ` and
`mcp__plugin_coagent_link__exec`: every one is strict T3. The positive controls (listed Bash and PowerShell calls) are
`Allow(OwnerCommandList)`.

**(c) Property** (`g6_property`):
- **Commands:** the crate generator with a new seed (25 everyday + 40 random), the 12 rows, two PowerShell-`\`
  protected paths, and three over-bound inputs: 82 in all.
- **Tools, hosts, states:** the seven tool names, both hosts, and the state set above.
- **Result:** `82 commands, 41328 decisions compared, 0 bad`.

**Other-field and real-tool survey:** see n-r6-1, n-r6-2 and n-r6-3. Severity: **no real current host tool carries an
executed shell command under a field the rule misses**. So there is no Major, and the field-name gap is a Note.

## 3. Check 2: the surface table against the code and the host list

- **Host list (TESTED).** `spikes/B16-search-command-forms/raw/q2.stream.jsonl` (`system/init`, version `2.1.325`) lists
  25 tools: `Bash, CronCreate, CronDelete, CronList, DesignSync, Edit, EnterWorktree, ExitWorktree, ListAgents, Monitor,
  NotebookEdit, PushNotification, Read, RemoteTrigger, ReportFindings, ScheduleWakeup, SendMessage, Skill, Task,
  TaskStop, ToolSearch, WebFetch, WebSearch, Workflow, Write`. All 25 have a row in A7.2. The recording has names
  only, no schemas.
- **Code arms (READ, `action.rs:262-433`).** `Read`, `NotebookRead`, `LS`, `Glob`, `Grep`, `Edit|Write|MultiEdit`,
  `NotebookEdit`, `Bash`, `PowerShell`, `Monitor`, `WebFetch`, `WebSearch`, `ExitPlanMode`, the own `share`/`send`,
  `mcp__*`, and the catch-all. Every arm has a row, and the "gate today" column matches the code. One nuance: `Monitor`
  is now execute, but the table's "gate today" column still describes the code at `0ea9b95` (other, T2). That is
  correct as dated.
- **`Monitor` row:** it matches this session's schema exactly (`command`, `description`, `timeout_ms`, and
  `ws.{url,protocols}`).
- **Errors:** `ExitWorktree` and `Task`/`Agent` (r6-m2).
- **Other rows:**

| tool | gate decides (TESTED) | defensible under "every terminal command asks"? |
|---|---|---|
| `Workflow` | T2 card, batchable, session | Yes for this machine. Its spawned agents' calls are hooked; its JS has "no direct filesystem or shell access" (host docs, via the seat). Owner question in n-r6-2. |
| `RemoteTrigger` | T2 | The commands run in a remote cloud session, not here. Defensible for this machine, but it is an outward action the owner may want red (n-r6-2). |
| `CronCreate`, `ScheduleWakeup` | T2 | Yes. They come back as prompts in this session, and each resulting tool call is gated. |
| `Skill` | T2 | UNKNOWN whether injected commands reach `PreToolUse`. Mitigated: the agent cannot write `.claude/**`. Owner question, as the seat records. |
| `Task`/`Agent` | T2 | Yes for local subagents (hooked). Not for `isolation: "remote"` (r6-m2, n-r6-2). |
| `ExitWorktree` | T2 | A delete of a session-created worktree on a T2 card. The table should say so (r6-m2). |

## 4. Check 3: nothing weakened

- **Round-5 gate files (TESTED, `integrity/r5b_rustfmt_cmp.txt`).**
  - The `run2/` copies hash to the addendum's three values (`97b336ff…`, `fb2a470e…`, `976706e2…`).
  - The committed files are NOT byte-identical: their sha256 are `e845c11b…`, `b4425d8b…`, `05be31e0…`.
  - `rustfmt --edition 2021` (toolchain 1.100.0) of each gate copy IS byte-identical (`cmp`) to the committed file. So
    the only change is rustfmt layout, as A7.1 says.
  - All three pass in `check.sh`: `r5b_r4_regressions` 6/6, `r5b_shell_t3` 6/6 (including the central property), and
    `r5b_bound_probe` 1/1.
- **Earlier gate files (TESTED, `integrity/gate_files_sha.txt`, `q01_r4_delta.diff`).**
  - `r2` and `r3` are unchanged (sha256 equal at `0ea9b95` and HEAD).
  - `r4` changes 4 strings: user folder → `someone`, each with the RULING line above it and the old line not quoted.
    The paths keep their shape (`C:\Users\<x>\.ssh\id_rsa`, `…\.claude`, `.claude.\settings.json`), and r4 is 14/14.
  - `q01` changes only `z_timing`. Each timed block is wrapped in `smallest_of_five`, with a RULING line quoting the
    old line. The timed region is the same (`fx.bash(...)` + `decide`, or `HookInput::parse`), and the bound, the
    inputs and the `TIMING REPORT` print are unchanged. A new helper is added at the end.
  - No assertion is removed or loosened.
- **Can "smallest of five" hide a regression? (TESTED)**
  - `decide` reads no clock and has no randomness, so extra work happens on every run, and the minimum of five runs
    still includes it. Only a regression that appears in fewer than 1 run in 5 could hide; a deterministic function
    does not produce one.
  - Mutant MG (60 ms of extra work for commands over 1 000 bytes) turns `z_timing` red at the smallest of five
    (63.38 ms), and `t17::m1_blow_up_inputs_are_fast` red (75.17 ms).
  - On HEAD, three runs at load ≈ 5: `cat with 16000 operands` 28.14 / 27.48 / 27.86 ms; every other case 0.44–9.2 ms
    (`logs/timing_head_{1,2,3}.log`).

## 5. Check 4: the four Minors

| round-5 | fixed? | test that fails without the fix (TESTED) |
|---|---|---|
| m1 (the owner's list waived the sandbox flag) | yes, `engine.rs:818-823` | MD (exclusion removed) → `t18::owner_list_never_waives_the_sandbox_bypass`, gate `g5_owner_sandbox_off` and my `g6_owner_list_binds_tool` red. Runner row `red_owner_list_waives_sandbox` red (both rows). |
| m2 (timing flake) | yes (smallest of five; the runner keeps its normal-build log) | MG → `z_timing` and `m1_blow_up_inputs_are_fast` red |
| m3 (64 KiB bound untested) | yes (red row) | `red_byte_bound_x4 -> r5b_bound_probe failed …: over: ASK T3` |
| m4 (first name in 6 test strings) | in the crate: yes, 0 hits (`git grep -i -w` on `crates/`). **Not in `docs/`: r6-m1.** | none needed (text) |

**Hygiene scan** (case-insensitive, lines added in `da4655e..HEAD`). 27 hits, written to `hygiene_hits.txt` as
file:line plus category, with the matched text withheld:
- **1 person's first name:** `docs/POLICY.md:423` (r6-m1).
- **The rest are not findings:**
  - `/System/Volumes/Data` automount roots (`src/path/mod.rs:28`, `:29`, `:37`);
  - the neutral `someone` user folders;
  - `.local` patterns.
- No machine name, home-directory path or real drive path.

## 6. Check 5: the merge

- **Ancestry (TESTED).** `git merge-base --is-ancestor da4655e HEAD` → exit 0. HEAD's parents are `da78a14` and
  `da4655e`.
- **`Cargo.toml` vs `da4655e`:** exactly `+    "crates/coagent-policy",` and
  `+unicode-normalization = "=0.1.25"   # POLICY seat: …`.
- **`Cargo.lock` vs `da4655e`:** exactly three added package entries: `coagent-policy`, `tinyvec 1.13.3` and
  `unicode-normalization 0.1.25`. No version of main's changed.
- **`BACKLOG.md` (TESTED, line-set check):**
  - every line of `da4655e` (191), `da78a14` (123), `0ea9b95` (108) and `13bd10e` (56) is present in HEAD;
  - 0 HEAD lines are in neither parent;
  - 53 `- [` entries, as the seat says.

  Nothing was lost and nothing foreign was added.
- **`git diff --name-only da4655e HEAD`** names, outside `crates/coagent-policy/`, only `BACKLOG.md`, `Cargo.lock`,
  `Cargo.toml` and `docs/POLICY.md` (58 files, `+18655`). For the stale local-main trap, see n-r6-6.

## 7. Check 6: `check.sh`, red controls, mutation

**`scripts/check.sh`** in my clone. Fixtures are on the boot volume (case-insensitive), under my scratchpad. Log:
`logs/check_ci.log`.
- **EXIT 0**, 639 passed, 0 failed (summed over every `test result:` line).
- Tail: `licenses ok` / `CHECK OK: fmt, clippy, test, deny all passed`.
- Gate files: `q01` 20/0, `r2` 19/0, `r3` 25/0, `r4` 14/0, `r5b_bound_probe` 1/0, `r5b_r4_regressions` 6/0,
  `r5b_shell_t3` 6/0, `t18_addendum7` 6/0.

**`crates/coagent-policy/red-controls.sh`** (`logs/red_ci.log`):
- **42 of 42 `RED OK`, 0 `RED MISSING`.** Normal build `GREEN` (198 passed, 0 failed, in `logs/red_normal_build.log`). Final line: `RED CONTROLS: all 42 went red; normal build green`, `EXIT 0`.
- Every row failed on its own assertion; none failed on a compile error. The first panic of each new row:
  - `red_monitor_unknown`:
    - eight-input test: `"tail -f build.log": Monitor differs from Bash`;
    - property test: `"ls" Posix [link=Open grant=false surface=Console unlisted]`;
    - gate test: `8 of 8:`.
  - `red_command_field_ignored`: `MadeUpRunner "tail -f build.log"`.
  - `red_owner_list_waives_sandbox`: `Allow { why: OwnerCommandList }`, in both the t18 test and the gate test.
  - `red_byte_bound_x4`: `over: ASK T3`.

**Mutation of the new rules** (`mutate_r6.py`, `mutation/mutation_results.tsv`, logs `mutation/mut_<id>.log`).
Targets: `t18_addendum7`, `r5b_shell_t3::g5_monitor*` / `g5_owner*`, `r6_gate::g6_*` and `t17_addendum5`; MG also runs
`q01::z_timing` and `t17::m1_blow_up`. Each mutant compiled (`Compiling coagent-policy` in each log). After the run the
tree was verified restored: `diff -r` against the pristine tree → `restore_diff_rc=0`.

| id | mutant | result | tests that went red |
|---|---|---|---|
| MA | `Monitor` arm deleted (Monitor falls into the catch-all, which still sees `command`) | KILLED | `t18::monitor_websocket_watch_is_strict`, `t18::monitor_equals_bash_…`, `g6_monitor_shapes`, `g6_property` |
| MA2 | `Monitor` arm returns `(Other, raw)` | KILLED | all three t18 Monitor tests, gate `g5_monitor_tool_is_shell`, all four `g6_*` |
| MF | `Monitor` scanned as PowerShell | KILLED | `t18::monitor_equals_bash_…`, `g6_property` |
| ME | `Monitor` ws URL target dropped | KILLED | `t18::monitor_websocket_watch_is_strict` |
| MB | command-field rule off (both arms) | KILLED | `t18::unknown_tool_with_a_command_field…`, `g6_owner_list_binds_tool`, `g6_m1_rows…`, `g6_property` |
| MB2 | unknown tool: Bash scan only (PowerShell scan dropped) | KILLED | `t18::unknown_tool_with_a_command_field…` (its PowerShell `\` hard-deny case). Mine stay green: they require "at least Bash". |
| MB3 | rule off for `mcp__` only | KILLED | `t18::unknown_tool…`, `g6_owner_list…`, `g6_m1_rows…`, `g6_property` |
| MB4 | rule off for the catch-all only | KILLED | same four |
| MC | owner list: tool name not bound (shell only) | KILLED | `t18::monitor_equals_bash_…`, gate `g5_owner_exact`, `g6_owner_list…`, `g6_m1_rows…`, `g6_property`. `t17` stays green. |
| MD | owner list: sandbox-off exclusion removed | KILLED | `t18::owner_list_never_waives…`, gate `g5_owner_sandbox_off`, `g6_owner_list_binds_tool` |
| MG | +60 ms work in `decide` for commands over 1 000 B | KILLED | `q01::z_timing` (63.38 ms), `t17::m1_blow_up_inputs_are_fast` (75.17 ms) |

0 survivors. My own tests were each shown red at least once. `g6_m1_rows_every_state`: MA2, MB, MB3, MB4, MC.
`g6_monitor_shapes`: MA, MA2. `g6_owner_list_binds_tool`: MA2, MB, MB3, MB4, MC, MD. `g6_property`: MA, MA2, MF, MB,
MB3, MB4, MC. `survey_command_field_names` prints only.

## 8. My view for the owner: should EVERY unrecognised tool get the strictest card?

Yes, with one carve-out. I recommend the strict card for any tool the gate does not recognise.

**Why the name-and-field rule is not enough:**
- The rule that closed M1 recognises a command by ONE exact key. My survey shows 27 key shapes, among them `cmd`,
  `script`, `code`, `args`, `input` and a nested `command`, that keep an unknown tool on a card that can be batched
  and approved for the session.
- A third-party `mcp__` tool with such a key gets a card with no reason line at all.
- No current host tool has such a shape today. The next tool, or an MCP server the owner installs, need not use the
  word `command`. That is the same lesson that produced M1.
- Several real host tools (`RemoteTrigger`, `Workflow`, `Agent` with remote isolation, `Skill`) cause work the gate
  never sees, and today they are T2.

**The carve-out.** Strict for unknown tools means more red cards, so keep a short, dated list of recognised low-risk
tools (`ToolSearch`, `CronList`, `ListAgents`, `TaskStop`, …) at T2. Measure that list against the host's tool list
each release, as A7.2 did.

## 9. Rulings by Friday, judged

| ruling | my ruling | why |
|---|---|---|
| item 3, the capability rule: any input executed as a shell command is decided as the terminal tool decides it; `Monitor` uses Bash's scan | **Upheld** | Bash-only for Monitor is right: the schema says "runs in the same shell environment as Bash", and on Windows it needs Git Bash. MF shows that a PowerShell reading changes decisions. Equality with Bash holds over 41 328 + 6 048 of my decisions. |
| item 4, the unknown-tool rule: only a `command` field raises; the default is unchanged | **Upheld as built; too narrow as policy** | It does what it says, and it is mutation-tight (MB, MB3, MB4). It keys on one exact key (n-r6-1); see §8. |
| the owner's exact-command list never allows a command arriving through another tool | **Upheld** | The safest reading. The entry binds tool + text + cwd, and a Monitor command is a different act (a long-lived watch). Tested over 8 tool names × 2 shells × 2 sandbox states; MC is killed by 5 tests. |
| item 6, ruled edit of `q01` (smallest of five) | **Upheld** | It changes only the timing lines, it is marked, and the old lines are quoted. It cannot hide a deterministic regression (MG). |
| item 8, ruled edit of `r4` (user folder name) | **Upheld** | Four strings, marked, old lines not quoted, meaning kept, 14/14. The item itself is incomplete outside the crate (r6-m1). |
| item 10, the merge allowance for `Cargo.toml`/`Cargo.lock` | **Upheld** | Only this crate's lines; no conflict; `--locked` builds pass. |
| (seat, A7.1) rustfmt layout of the r5b files; the crate-level lint allow | **Accept** | Layout proven by `cmp`. The lint allow is style-only (n-r6-4). |

## 10. What I reproduced from the seat's report

| seat claim | reproduced? |
|---|---|
| merge commit and parents | yes |
| `Cargo.toml` +2 lines; `Cargo.lock` +3 entries | yes |
| `BACKLOG.md` 53 entries | yes |
| 639 / 0 and `CHECK OK` | yes (boot volume) |
| gate file counts | yes |
| 42 red rows | yes |
| the r5b rustfmt claim | yes |
| q01/r4 sha256 old → new | yes |
| `cat with 16000 operands` ≈ 27.9 ms | 27.5–28.1 ms |
| "crate 8 → 0 name hits" | yes for `crates/`. But docs still has one (r6-m1). |
| the A7.2 table | not fully: two rows wrong (r6-m2) |

**My slips:**
- **The `ws` equality.** My first `g6_monitor_shapes` asserted exact equality for a `ws` watch. That input is
  legitimately stricter (n-r6-7). I corrected the test (`logs/mine_head.log` is the first run, `mine_head2.log` the
  corrected one).
- **A stale binary in one timing run.** I shared one target directory between the pristine tree and the mutation tree.
  Cargo's build hashes do not depend on the tree's path, so after the mutation run, one `z_timing` run on the pristine
  tree reused the MG-mutant binary and showed 60–92 ms.
  - Kept as `logs/timing_head_STALE_BINARY_my_slip.log`.
  - After `touch` of the pristine sources it recompiled and gave the numbers in §4.
  - The mutant results are unaffected: every mutant log shows its own compile, and the pristine runs of `r6_gate` came
    before the mutation run.

## 11. NOT TESTED

- **The case-sensitive project volume:** `check.sh` and the red controls ran on the boot-volume fixtures only (the
  seat ran both volumes).
- **Windows clippy and Windows at run time.**
- **Any real host run:** no model runs. I did not check whether `PreToolUse` fires for `Skill` injected commands,
  `Workflow`-spawned agents, or remote-isolation agents.
- **Whether `mcp__ide__executeCode` exists in 2.1.325, and whether 2.1.325's `Task` has `isolation: "remote"`:** my
  schemas come from this session, whose host version was not printed.
- **The round-5 135,408-decision campaign:** not repeated (out of scope). Its central test ran unchanged in `check.sh`.
- **No attack command was executed;** every result is a gate decision.

## 12. Re-run

`O=/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_policy_tests_r6`. The
scripts source `$O/scripts/env.sh`, which sets a private `CARGO_HOME` whose `bin` links to the project's
`tools/cargo/bin`, the project's `tools/rustup` read-only, private target directories, and `COAGENT_TEST_TMP` under
the scratchpad.

```
git clone --branch m2-policy "/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/2_Project_Files" $G/clone   # assert HEAD 9776276…
cargo fetch --locked --manifest-path $G/clone/Cargo.toml
bash $O/scripts/run_check.sh          # check.sh  -> logs/check_ci.log
bash $O/scripts/run_red.sh            # red-controls.sh -> logs/red_ci.log
git -C $G/clone archive HEAD --prefix=t/ | tar -x -C $G ; cp $O/r6_gate.rs $G/t/crates/coagent-policy/tests/
bash $O/scripts/run_mine.sh $G/t <log>            # r6_gate (5 tests)
cp -R $G/t/. $G/m/ ; bash $O/scripts/run_mut.sh   # mutants MA..MG; use a SEPARATE target dir per tree, or touch sources after
```
