VERDICT: GO WITH NOTES — head 2f4395db41e31d44dd0628e2295d7ab71c894cea

# Gate M2 POLICY-STRICT: independent check (tier 1, security surface)

Branch `m2-policy-strict` at `2f4395db41e31d44dd0628e2295d7ab71c894cea`, cut from main `c9a66534600e47fdd4a8da913df79d220086340b`.
Checked 2026-11-18 on a fresh clone in the checker's scratch area (`git rev-parse HEAD` = the head above, TESTED). Main is
taken AS GIVEN: this check did not read the remote (no `ls-remote`); the clone was made from the project's local
repository, which holds the branch at that head.

Every figure below is marked **TESTED** (the checker ran it) or **READ** (taken from code, docs or the builder's report).

## BLUF for the owner

**What you would see.** When an agent in a session calls a tool the gate has never been taught, you now get a red card
every time: it cannot be batched, it has no "allow for this session" button, Allow waits 5 seconds, and a grant or an
earlier approval never answers it for you. With nobody to answer, it is refused. The same goes for deleting a worktree
(`ExitWorktree`), for starting a helper agent that runs remotely or with an `isolation` value the gate doesn't recognise,
and for starting a helper that has a `name` (it might be an agent-team member). Ordinary tools (reading, editing,
searching, web fetch, the to-do and task-list tools, asking you a question, local helper agents) behave exactly as they
did before.

**What I checked.** Both full checks pass (TESTED, 873 tests, 0 failed, twice). All 47 red-control rows fail on the
property they are meant to break (TESTED). Over about 25,900 decisions, comparing main and this branch for the same
inputs, **none got weaker** and about 10,500 got stricter (TESTED). About 95,000 decisions for 496 made-up and
look-alike tool names were all strict (TESTED). 17 of my 18 deliberate code breakages were caught by the builder's own
tests and 16 by mine. **I found nothing that lets a command run or a file change with less checking than before, and
nothing built for a "bypass".**

**What is left (no blocker, no major):** three docs or test gaps (Minor) and some Notes. The one that matters most for
a later decision is **S-2**. The rule "a helper call with no `isolation` field runs locally" looks only at the call. The
host documents that a helper's *definition* can also set its isolation, and I could not check whether a definition can
say `remote`.

Counts: **Blocker 0 · Major 0 · Minor 3 · Note 9.**

## Findings

| id | severity | what | input that shows it | exact output seen | file:line |
|---|---|---|---|---|---|
| S-1 | Minor | `docs/POLICY.md` now says a string `command` field "on any other tool" is a terminal command, and "it holds for a taught tool too". That is false for the taught NAMED arms (`Read`, `Write`, `Edit`, `Glob`, `Grep`, `LS`, `Notebook*`, `WebFetch`, `WebSearch`, `ExitPlanMode`, own `share`/`send`): they never read a `command` field. No protection is lost (the host's `Read`/`Write` never execute such a field, and main behaved the same), but the sentence was broadened this round and is not true as written. It is true for the catch-all, `mcp__`, `ExitWorktree` and `Agent`/`Task`. | `Read {"file_path": "<ws>/README.md", "command": "rm -rf ~"}` (also `Write`, `Glob`, `WebFetch`, the same field) | TESTED `PROBE command-field Read: kind=Read -> Ask T0 batchable=true`; `Write: kind=Edit -> Ask T1 batchable=true`; `Glob: kind=Search -> Ask T0 batchable=true`; `WebFetch: kind=Fetch -> Ask T2 batchable=true` | docs/POLICY.md:66, :131, :672-673; src/action.rs:315, :357, :400 |
| S-2 | Minor | The absent-`isolation` = LOCAL ruling reads the CALL only. The host's tools reference (saved 2026-11-18) links `isolation: worktree` to the subagent DEFINITION's frontmatter fields (`sub-agents#supported-frontmatter-fields`). So a call with no `isolation` can still run isolated as its `subagent_type`'s definition says, and the gate cannot see that. Only `worktree` appears in that position in any saved page (local, still gated). Whether a definition can say `remote` is UNVERIFIED (no network this check). If it can, `Agent {"prompt":…, "subagent_type":"<such a definition>"}` gets today's ordinary T2 card for a remote run. Not shown reachable, so not Major. Neither the docs sentence nor BACKLOG records this. | `Agent {"prompt":"p","subagent_type":"Explore","model":"opus","isolation":"worktree"}` and `Agent {"prompt":"p"}` (call-level view) | TESTED `LOCAL? Agent {"prompt":"p","description":"d"} -> strict=None local=true`; READ `tools-reference_2026-11-18.md:35` "Not available to subagents that already run in their own working directory, such as with [`isolation: worktree`](…/sub-agents#supported-frontmatter-fields)", and `:312` the same | src/known.rs:130-133 (`ABSENT_ISOLATION`), docs/POLICY.md:175-177 |
| S-3 | Minor | Missing test for correct code. "`UnknownTool` is the FIRST reason on a strict card" (brief item 1; verdict n-r6-1) is only tested on cards where it is the ONLY reason. Mutant M12 moves `UnknownTool` back to the end of `Reason` and survives all 209 crate tests and all of mine. The card where it shows: an untaught tool that also sets the sandbox flag. Head gives `[UnknownTool, SandboxBypass]`; the mutant gives `[SandboxBypass, UnknownTool]`. The decision is unchanged (both T3). | M12 (mutation table); `MadeUpTool {"dangerouslyDisableSandbox": true}` | TESTED `M12 … OWN: survived (1005s) QA: survived (422s)`; the reason order on that input is READ from the enum order (`engine.rs:44` vs `SandboxBypass` later), not run | src/engine.rs:44-46 |
| N-1 | Note | `EnterPlanMode` is taught at T2. Design 03 §5.1 puts "permission-mode changes" at T3, but entering plan mode only restricts. It was T2 on main (not lowered, TESTED), and the brief names it. The builder put it under DESIGN QUESTIONS; I agree with that. | `EnterPlanMode {…}` | TESTED: identical decision to main in all 345 table rows for it | src/known.rs:70 |
| N-2 | Note | `TaskCreate`/`TaskUpdate` are "the session's own task list". With agent teams on, the host's task list is shared with teammates, and a teammate can then pick up work from it. Teammates can only be started by a strict call (a named `Agent`/`Task`), so this is no new path. Still, "starts no work outside the session" is not literally true in team mode. | READ `tools-reference_2026-11-18.md:640-647` ("Task-tracking tools in subagents and agent teams") | READ | src/known.rs:65-66 |
| N-3 | Note | A LOCAL call with `isolation: "worktree"` makes the host create a git worktree (a write the gate does not see) on an ordinary T2 card, batchable and session-approvable. This is the brief's ruling and the same as main (TESTED, not lowered). The subagent's own later calls are still gated. | `Agent {"prompt":"p","isolation":"worktree"}` | TESTED `LOCAL? … -> strict=None local=true` | src/known.rs:148 |
| N-4 | Note | The teammate check keys on `name` byte-exactly. `Name`, `NAME`, `"name "`, `team_name` and `teammate` read LOCAL. Host field names are case-sensitive and the docs say a teammate needs `name`, so this is correct as read. | `Agent {"prompt":"p","Name":"a"}` etc. | TESTED `PROBE name-like key "Name": Local` (and the other four the same) | src/known.rs:143 |
| N-5 | Note | Duplicate keys: the last one wins, the same as the host's JSON. | `{"prompt":"p","isolation":"remote","isolation":"worktree"}` / reversed | TESTED first `-> strict=None local=true`; reversed: strict in all 12 states | src/known.rs:146 |
| N-6 | Note | Hygiene: no person's name, account, machine, drive, home path or client name in the added lines. The coordinator seat name "Friday" appears in 6 added lines and 2 commit messages. It is not a person, and main already carries it 3 times. The commit author identity on the branch is the same as on all 131 main commits: pre-existing, not added by this round. | scan below | TESTED `TOTAL 11 {'seat/agent name': 8, 'account/email': 3}`; the 3 email hits are the `Co-Authored-By: … <noreply@anthropic.com>` trailers | BACKLOG.md:415, :420; src/known.rs:130; tests/t19_strict.rs:725; docs/POLICY.md:176, :182 |
| N-7 | Note | STATUS §6 says BACKLOG went "85 → 86"; with the Addendum-2 entry it is 85 → 87. No entry was deleted; two were ticked `[x]` with a Resolved line. | `grep -c '^- \['` main vs head | TESTED main `open=79 done=6 total=85`, head `open=79 done=8 total=87`; diff removes only the 2 ticked lines | BACKLOG.md |
| N-8 | Note | The t19 guard picks its "off the list" names with the function under test (`known_tool`). A mutant that widens the lookup (M03 prefix, M04 case, M05 trim) therefore also shrinks the guard's own sample. The other t19 tests kill those mutants, so nothing slipped through, but the guard alone would not have. My first draft had the same weakness; I fixed it with an independently written list (`qa_list_is_exactly_the_expected_names_and_lookup_is_exact`). | M03-M05 | TESTED: killed by `every_listed_tool_gets…` / `names_match_byte_exactly`, not by the guard | tests/t19_strict.rs (`guard_no_tool_name_off_the_list…`, `if known_tool(name).is_some() { continue }`) |
| N-9 | Note | The suite's fixture fall-back: with `COAGENT_TEST_TMP` unset and no `tools/tmp` above the checkout, fixtures go to `CARGO_TARGET_TMPDIR`. So my "project volume" run actually ran on the boot volume (see NOT TESTED). | `ls <area>/target/tmp/m2-policy` exists after run 1 | TESTED | tests/common/mod.rs:16-32 |

## A. Reproduction (TESTED)

- **`scripts/check.sh` run 1** (fixtures fell back to `<area>/target/tmp`, boot volume, case-INSENSITIVE APFS):
  **EXIT 0**, tail `licenses ok` / `CHECK OK: fmt, clippy, test, deny all passed`. Workspace **873 passed, 0 failed,
  18 ignored**. `coagent-policy` **209 passed, 0 failed** (unit 16; t01 3, t02 3, t03 3, t04 8, t05 5, t06 2, t07 5,
  t08 6, t09 10, t10 3, t11 3, t12 4, t13 3, t14 10, t15 9, t17 9, t18 6, t19 10). Gate files: q01 20, r2 19, r3 25,
  r4 14, r5b_bound_probe 1, r5b_r4_regressions 6, r5b_shell_t3 6, all 0 failed. These equal the builder's figures.
- **`scripts/check.sh` run 2** with `COAGENT_TEST_TMP=<area>/testtmp` (under `/private/tmp`; `diskutil`: `APFS`, a probe
  `CaseProbeQ` IS found as `caseprobeq`, so case-INSENSITIVE; the suite wrote `testtmp/m2-policy`): **EXIT 0**, same
  tail, **873 / 0 / 18**, the same per-file counts.
- **`crates/coagent-policy/red-controls.sh`** (run from its own path, `CARGO_TARGET_DIR=<area>/target2`): **47 rows
  `RED OK`, 0 `RED MISSING`**, then `GREEN normal build: all coagent-policy tests pass` and the final line
  **`RED CONTROLS: all 47 went red; normal build green`**, EXIT 0. Main has 42 rows (READ); the 5 new rows are
  `red_list_entry_removed` (`assertion left == right failed: TodoWrite`), `red_catch_all_t2` (`"" {} [link=Open
  grant=false surface=Console] is below T3: Allow { why: SessionApproval …`), `red_mcp_t2` (`"mcp__" {} … is below T3:
  Allow …`), `red_remote_as_local` (`Agent "remote"`), `red_unknown_isolation_as_local` (`Agent "Remote"`). I read
  every row's first panic line (`logs/red_controls.log`): each fails on a test assertion about its own property, not on
  a compile error. `red_shell_not_t3` → `T3 read delay`; `red_command_field_ignored` → `MadeUpRunner "tail -f
  build.log"`; `red_monitor_unknown` → `Monitor differs from Bash` / `8 of 8:`.
- **Toolchain.** The pathguard hook refused to create the two symlinks into the project's `tools/`, so I did not make
  them. Instead I exported `RUSTUP_HOME=<project>/tools/rustup`, `PATH=<project>/tools/cargo/bin:$PATH`,
  `CARGO_HOME=<area>/tools/cargo` (the registry is in my area), `CARGO_TARGET_DIR=<area>/target` and
  `COAGENT_TOOLS=<area>/tools`; `scripts/env.sh` then prints its "no toolchain at …; using whatever cargo is on PATH"
  line and keeps those exports. `cargo 1.100.0`, `rustc 1.100.0`. `cargo fetch --locked` was the only network use.

## B. Scope (TESTED)

`git diff --stat c9a6653 HEAD`: 12 files, +1275 −45. Only `BACKLOG.md`, `docs/POLICY.md` and `crates/coagent-policy/`
(Cargo.toml, red-controls.sh, src/action.rs, src/engine.rs, src/known.rs (new), src/lib.rs, tests t01, t12, t18, t19
(new)). These are within the brief's allowed paths. The seven gate files are byte-identical to main (sha256 per file:
one distinct hash each). `tests/common/mod.rs` is unchanged. Earlier test files that changed, judged one by one:

- `t01_table::every_tool_in_the_table`: `>= T2` became the exact tier (`Agent` T2, `Task` T2, `SomeFutureTool` T3,
  `TodoWrite` T2). The brief names it. Correct.
- `t18_addendum7::unknown_tool_without_a_command_field_is_unchanged` was renamed `…_is_strict`: the T2/batchable
  asserts became T3, not batchable, delay 5, no session option. The `Agent` row moved to its own block asserting T2,
  batchable, no reason line, and the `mcp__github__list` assert became T3 with `UnknownTool` first. The brief names it.
  Correct.
- `t12_docs::every_known_tool_is_documented` is new: it builds each §3a row from the constant, checks the count and
  checks that §3a has no other tool row. M17 (a wrong entry) is killed by it in 10 s. Correct.

No other crate uses `coagent-policy` (TESTED: grep). So the new public field `Action::strict` and the `known` module
break no other user.

## C. The strict default, attacked (TESTED; my tests are in `gate_policy_strict_tests/qa_strict.rs`, 12 tests, all green on the head, 870 s)

1. **Untaught names** (`qa_untaught_names_are_strict_everywhere`): 496 names. That is 40 random names, and for each of
   the 24 entries: lower and upper case, tab, NBSP, newline, NUL, BOM, ZWJ, a one-character-shorter prefix, `s`/`x`/
   doubled suffixes, `/`, `(*)`, `mcp__<n>`, `mcp__<n>__<n>`, fullwidth; plus Cyrillic look-alikes (`Rеad`, `Аgent`,
   `Tаsk`, `TodoWrіte`), a combining accent, the empty name, `mcp`/`mcp_`/`MCP__…`/`mcp__`/`mcp___`/`mcp____`/
   `mcp__a`/`mcp__a__`/`mcp____b`/`mcp__a__b__c__d`, own-prefix near-misses (`…__share `, `…__SHARE`, `…__shar`,
   `…__sendx`, `…__share__x`, `mcp__plugin_coagent_link_share`), and host-ish names (`TeamCreate`, `BashOutput`,
   `KillShell`, `TaskOutput`, …). Each × 16 inputs (no field, prompt, path, URL, `cmd`, array/nested `command`,
   non-objects) × 12 states (link open/closed-tainted × wide grant with a `service github:*` line or none × 3
   surfaces, each with an `ExactInput` approval for the very call, read memory and reads-under approvals). Result:
   **`QA untaught: 496 names, 95232 decisions, 0 below strict`**. Strict means: T3, not batchable, delay 5, options
   only from {AllowOnce, Deny, DenyWithReason}, or a Deny. Since every shell command is T3, this is never below the
   terminal tool's tier.
   `qa_strict_card_answers_store_nothing`: on 6 strict cards, AllowOnce stores no approval and no memory, and
   AllowForSession with `ExactInput`, `ReadsUnder` or `EditsToFile` is refused with no approval stored. **No scope
   wider than one call is reachable.**
2. **Known-tools list vs the host** (I read the whole saved tools reference, 46 rows, and the 2.1.325 `system/init` list
   of 25 tools from `spikes/B16…/q2.stream.jsonl`). My ruling on each T2 `other` entry: `TodoWrite`, `TaskCreate`,
   `TaskUpdate`, `TaskList`, `TaskGet`: bookkeeping (N-2). `AskUserQuestion`: UI. `EnterPlanMode`: a mode change that
   only restricts (N-1). `ToolSearch`: loads definitions and executes nothing. `CronList`: list only. `Agent`/`Task`
   LOCAL: its calls are gated, "Claude Code checks the subagent's own tool calls" (`:119`), with N-3 and S-2. **None of
   them executes a command, writes or deletes a project file, reaches the network, starts an agent outside the gate, or
   changes settings or permissions.** The read/edit/fetch entries are named arms whose tier still comes from their
   target; the table shows them unchanged. Off-list host tools: `qa_host_tools_off_the_list_are_strict`: **29 tools,
   5,568 decisions, all strict** (every host or docs tool not in my independently written list of 24). `TaskStop`,
   `ListAgents`, `SendMessage`, `CronDelete`, `EnterWorktree`, `LSP` etc. are all strict, and I agree with each
   left-off reason in STATUS §2.1. **Nothing lowered**: `qa_table.rs` built against main AND the branch, the same 69
   names × 25 inputs × 15 states: **`rows 25875 unchanged 15423 raised 10452 LOWERED 0`**, no same-tier change in
   batchable or session option (`logs/cmp_tables.log`). Every taught `other` tool is exactly T2, batchable, with the
   one `ExactInput` option; a different input asks again, and a wide grant never allows it
   (`qa_taught_other_tools_are_exactly_t2_and_hash_bound`).
3. **Command fields stay terminal**: the round-6 gate file `r6_gate.rs`, copied in unchanged, gives **5 passed, 0
   failed** (`g6_m1_rows_every_state`, `g6_monitor_shapes`, `g6_owner_list_binds_tool`, `g6_property`,
   `survey_command_field_names`). `qa_command_field_beats_the_list`: every taught `other` tool, `ExitWorktree`, a
   made-up tool and `mcp__srv__x`, with `isolation` worktree/remote or `name`, and `{"command":"echo x >> ~/.zshrc"}`,
   give `Execute` and `Deny(HardDeny)`; `npm test` is strict in all 12 states. (The named arms that ignore the field: S-1.)
4. **Red cases** (`qa_red_cases_every_shape`, both `Agent` and `Task`): 36 shapes are strict in every state.
   `remote`; `Remote`/`REMOTE`/`remote `/` worktree`/`WORKTREE`; `worktree\0`; `work​tree`; Cyrillic `wоrktree`;
   `""`; `cloud`/`local`/`none`; `null`/`0`/`false`/`["worktree"]`/`{…}`; duplicate keys ending in `remote`; 12 `name`
   shapes; non-object inputs. Seven shapes are local by design (absent; `worktree`; with `subagent_type`/`model`;
   `run_in_background`; `isolation` nested inside another object, which the host does not read; `team_name` without
   `name`; duplicate keys ending in `worktree`). `ExitWorktree`: 11 shapes (`remove` with
   `discard_changes` true or `"true"`, `keep`, `Keep`, `{}`, `null` action, array action, duplicate keys, non-objects)
   are strict everywhere with `WorktreeRemoval` first. The absent-`isolation` ruling, judged against the host docs:
   S-2.
5. **`name`** (`qa_name_is_strict_whatever_isolation`): `name` ∈ {"a", "", null, 0, ["a"], {}} × `isolation` ∈
   {absent, worktree, remote, null} × both tool names is always `PossibleTeammate`, strict in all states, and that
   reason is first. Key order is irrelevant (`{"isolation":"worktree","name":"a",…}` strict). N-4 covers the odd key
   spellings.
6. **Third-party tools and grants** (`qa_service_grant_line_allows_nothing`): with the wide grant's `service github:*`
   line installed, `mcp__github__list`/`get_issue`/`x` are strict on all 3 surfaces. `docs/POLICY.md:541-543` says it
   plainly: "No third-party tool is on the known-tools list (§3a), so every `service` call is T3 and a grant's `service`
   line allows nothing". True as written.
7. **Owner's exact-command list** (`qa_owner_list_binds_tool_and_sandbox`): `npm test` listed for Bash in the
   workspace. Positive control: `Bash npm test` gives `Allow(OwnerCommandList)`. The same text through all 24 taught
   tools, `Monitor`, `PowerShell`, `bash`, `MadeUpTool`, `mcp__srv__run`, `ExitWorktree`, `Agent` and `Task` (3 input
   shapes) is never allowed. `Bash` with `dangerouslyDisableSandbox: true` is never allowed.

**Bypass**: the added lines carry 6 `cfg(feature …)` lines, all compile-time `red_*` seams (5 new, plus
`red_shell_not_t3` extended). There is no environment read, setting, flag, list entry, card option or grant field. The
scan for `bypass|env::var|getenv|COAGENT_|allow_all|skip` hit only the docs sentence saying nothing for a bypass is
built (that hit is the scan's positive control) and the `red_skip` seam. **Nothing built for a bypass. TESTED by scan
and READ.**

## Rulings on Friday's rulings

1. **Brief, own MCP tools** (each existing own tool other than `share`/`send` gets an entry; any other own-prefix name is
   strict): **UPHELD.** None exists in the tree (READ; STATUS §2). Own-prefix near-misses are strict (TESTED, C1), and
   the BACKLOG entry records the open item.
2. **Brief, taught at T2** (host-documented bookkeeping or UI tools that reached the catch-all keep exactly today's
   decision): **UPHELD.** No decision is lowered (TESTED, 0 of 25,875). Each entry passes the brief's one-line test,
   with Notes N-1 (`EnterPlanMode` vs design §5.1) and N-2 (task tools in agent teams). The builder's choice to leave
   the candidates `TaskStop` and `ListAgents` off is right by their documentation rows (they act on other agents).
3. **Brief, absent `isolation` = LOCAL**: **UPHELD AS BUILT, with S-2.** It matches the call-level definition. The
   permission docs say an omitted parameter is never matched, and the tools reference names no default other than
   local. But the host also lets a subagent DEFINITION set `isolation`, which the gate cannot see. Record that and
   verify whether `remote` is a definition value before relying on the ruling. It is one line (`ABSENT_ISOLATION`) if
   it must change.
4. **Addendum 2, `name` is strict whatever `isolation` holds**: **UPHELD.** It only raises. The host's teammate rule
   ("unless the call … passes `isolation` on the call itself", quoted in STATUS §9 from the agent-teams page; READ) means
   `name` + `isolation` is in fact NOT a teammate. So the ruling is stricter than needed for that combination, and the
   cost (ordinary named subagents ask every time) is real but accepted and recorded in BACKLOG. Docs §3a says it in one
   plain sentence (READ, true).
5. **Brief/addendum, nothing for a bypass**: **CONFIRMED** (above).

## Mutation (TESTED; driver `mutate.py`, `logs/mut4.log`)

Each mutant is one textual edit to the changed source. "OWN" = the branch's own crate tests (unit + every t-file, then
the seven gate files if those all pass). "QA" = my `qa_strict` (then `qa_strict` with the 95k-decision test + `r6_gate`
if the first stage passes).

| id | mutant | OWN | QA |
|---|---|---|---|
| M01 | strict raise T3 → T2 (engine) | killed: `every_tool_in_the_table` | killed: `qa_service_grant_line_allows_nothing` |
| M02 | `mcp__` (service) excused from the not-taught check | killed: `unknown_tool_without_a_command_field_is_strict` | killed: `qa_strict_card_answers_store_nothing` |
| M03 | list entry matched by prefix | killed: `every_listed_tool_gets_exactly_its_listed_kind_and_tier` | killed: `qa_list_is_exactly_the_expected_names…` |
| M04 | list entry matched case-insensitively | killed: `names_match_byte_exactly` | killed: `qa_list_is_exactly…` |
| M05 | list entry matched after trim | killed: `names_match_byte_exactly` | killed: `qa_list_is_exactly…` |
| M06 | `worktree` matched case-insensitively and trimmed | killed: `the_subagent_tool_under_both_names…` | killed: `qa_red_cases_every_shape` |
| M07 | `name` checked after `isolation` (worktree + name read local) | killed: `the_subagent_tool…` | killed: `qa_name_is_strict_whatever_isolation` |
| M08 | `isolation: null` read as absent (local) | killed: `the_subagent_tool…` | killed: `qa_red_cases_every_shape` |
| M09 | `ExitWorktree` demoted to the T2 card | killed: `exit_worktree_is_strict_whatever_it_holds` | killed: `qa_strict_card_answers_store_nothing` |
| M10 | remote subagent demoted (not strict) | killed: `the_subagent_tool…` | killed: `qa_strict_card_answers_store_nothing` |
| M11 | choke point's `Execute` branch removed | killed: `t06_t3::positive_controls_t3_list_is_not_everything` (a `Bash` card gains an untrue `UnknownTool` line) | **survived**: not equivalent (it changes a card's reason line); my tests assert strictness, not shell-card text, and it lowers no decision |
| M12 | `UnknownTool` moved back to the end of `Reason` | **survived** (all 209) | **survived**: not equivalent; see S-3 |
| M13 | absent `isolation` ruled remote (stricter) | killed: `every_tool_in_the_table` | killed: `qa_taught_other_tools_are_exactly_t2…` |
| M14 | every own-prefix name taught | killed: `every_listed_tool_gets…` | killed: `qa_list_is_exactly…` |
| M15 | a non-object subagent input read as local | killed: `the_subagent_tool…` | killed: `qa_red_cases_every_shape` |
| M16 | engine ignores `strict` for kind `other` | killed: `every_tool_in_the_table` | killed: `qa_strict_card_answers_store_nothing` |
| M17 | wrong entry: `SendMessage` taught at T2 | killed: `t12_docs::every_known_tool_is_documented` | killed: `qa_list_is_exactly…` |
| M18 | only `remote` is remote; any other string local | killed: `the_subagent_tool…` | killed: `qa_red_cases_every_shape` |

Branch tests: 17 of 18 killed. Mine: 16 of 18 killed. Either suite: 17 of 18. The one survivor of both, M12, is a
card-order gap and lowers no decision (S-3). No mutant that lowers a decision survived the branch's own tests. The
mutant tree's source was restored and checked identical to the head afterwards (TESTED `diff -r`).

## E. Docs and BACKLOG (READ, with the TESTED probes above)

Every changed sentence of `docs/POLICY.md` is true as written except S-1 (lines 66, 131, 672-673). That includes the
§3a table: `t12` checks it against the constant row for row, and M17 proves that check bites. It also includes the
user sentence "A tool the gate has not been taught asks every time, on a red card." (true: C1), the §6 grant sentence
(true: C6) and the named-subagent sentence at :181-183 (true: C5). The owner's two answers are cited by card, date and
option text, by role ("the owner"), never by name. S-2 is a missing caveat, not a false sentence. BACKLOG: the two
entries the brief asked for are present (own MCP tools; named subagent calls). n-r6-1 and n-r6-2 are ticked with a
"Resolved" line, the `Skill` entry is updated, and none is deleted (N-7).

## F. Hygiene (TESTED)

`hygiene_scan.py` scans the ADDED lines of `git diff -U0 c9a6653 HEAD` and the commit messages, case-insensitively,
for person names, account/email, machine, drive/volume, home path, client and seat names. It prints file:line and
category only. Result: `TOTAL 11 {'seat/agent name': 8, 'account/email': 3}`, explained in N-6: no person, machine,
volume, home path or client. **Positive control**: on a 6-line file with one planted item per category plus a clean
line, it found person, account/email, drive/volume, home path and client on their lines and nothing on the clean line.
Fixtures: `t19_strict.rs` builds all of its 10 fixtures with `fixture(…)` (a generated scratch tree) and holds no
literal real path (grep: 0).

## G. Remote

I did not read the remote. Main is taken as given (`c9a66534600e47fdd4a8da913df79d220086340b`). The builder's push,
`ls-remote` and ancestor check (STATUS §10) are READ, not verified.

## NOT TESTED

- **Case-sensitive (project) volume**: NOT TESTED by me. Both of my `check.sh` runs put fixtures under `/private/tmp`
  (case-insensitive): run 1 by the suite's fall-back (N-9), run 2 by `COAGENT_TEST_TMP`. I am not allowed to write on
  the project drive. The builder reports a green project-volume run (READ, STATUS §7).
- **Windows** (`x86_64-pc-windows-msvc` clippy, and any Windows run): NOT TESTED; the builder reports clippy EXIT 0
  (READ).
- **A real host run** (no model run): NOT TESTED. Whether 2.1.325's `Task` has `isolation`, whether a subagent
  definition can set `remote` (S-2), and whether the hook runs for a teammate's calls are UNVERIFIED.
- **No network**, so the host pages were not re-fetched: I read the builder's saved copy of the tools reference
  (`tools-reference_2026-11-18.md`) and the saved permissions page, not the live pages.
- The M12 card-order effect on `MadeUpTool {"dangerouslyDisableSandbox": true}` is READ from the enum order, not run.

## Disk used (TESTED)

Everything is in the checker's scratch area on the boot volume: about **1.7 GB** (`target` 931 MB, `target2` 587 MB,
local cargo registry 200 MB, trees and logs about 35 MB). Nothing was written to the project drive. This report's tests
and logs folder is 108 KB. Nothing outside my area was deleted. I stopped only my own processes; one orphaned
mutation test process of mine was killed after its cwd was checked to be in my area.

Tests, drivers and short logs: `0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_policy_strict_tests/`.
