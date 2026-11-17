VERDICT: NO GO — head 0ea9b95eddbd1202a2326fed2ecbcba3b050cafd

# QA gate M2-POLICY, round 5: the capped third check (branch `m2-policy` @ 0ea9b95eddbd1202a2326fed2ecbcba3b050cafd)

Independent gate, run 2, 2026-11-17. Findings only: nothing fixed, merged, committed or pushed, and nothing written in the
project folder. HEAD asserted `0ea9b95eddbd1202a2326fed2ecbcba3b050cafd` in my clone
(`/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_policy_r5/repo`).
`git ls-remote origin m2-policy` (the real remote) → `0ea9b95eddbd…`. The dead run's files beside `run2/` were read as
notes only. Every test and result below is mine and comes from this run.

## BLUF

1. The rule this round was built for holds. In 135,408 decisions over 651 generated shell commands I found no Bash or
   PowerShell text that the gate treats as less than a red, unbatchable, one-time card. That covers every state, both
   hosts, and odd input shapes.
2. The owner's exact-command list compares the text byte for byte, and it also compares the shell and a symlink-free
   working directory. No variant I tried matched.
3. Every round-4 Blocker and Major is fixed. My own tests for them fail on the old code and pass on this branch, on both
   disk kinds.
4. It is still NO GO because of one Major outside the shell-text logic. Claude Code has a second tool, `Monitor`, that
   runs a shell command. The gate treats it as an unknown tool: an ordinary card that can be batched and approved for
   the session, and a write to the gate's own settings through it is not refused.
5. The fix is small: treat `Monitor` (and any tool that carries a shell `command`) exactly like `Bash`.
6. Four Minors are for the owner's card: a listed command can also switch the sandbox off without asking; one timing
   test fails on a busy machine; one size limit has no test; and a person's first name appears in six test strings.

Findings: **0 Blocker, 1 Major, 4 Minor, 7 Note.**

## 1. Findings

"Strict T3" means `Ask` with tier T3, `batchable = false`, `read_delay_secs = 5`, no `AllowForSession` option, the fixed
shell sentence first; or `Deny`. Fixture states are the crate's own `common::fixture` with a fake home.

| id | sev | what | input that shows it | exact output seen | file:line | how |
|---|---|---|---|---|---|---|
| **M1** | **Major** | Claude Code's `Monitor` tool runs its `command` as shell, but the gate maps it to "unknown tool" (`Kind::Other`, T2). The card can be batched, offers "allow for this session", and the hard-deny and credential scans never look at the command (free text is checked against exclusions only). So a shell command can be decided below T3, which contradicts Kam's 07:28 ruling ("every terminal command asks") and POLICY §5. | `Monitor` `{"command": "echo x >> ~/.claude/settings.json", "description": "watch", "timeout_ms": 300000}`; also `cp evil.sh .git/hooks/pre-commit`, `echo '…\| sh' >> ~/.zshrc`, `curl … \| sh`, `sudo rm -rf /`, `git push --force` | every one of the 8: `ASK T2 kind=Other batchable=true session=true reasons=[UnknownTool]`. After the owner picks the card's session option, the **same call again → `Allow { why: SessionApproval { scope: ExactInput {…} } }`** | `crates/coagent-policy/src/action.rs:300` (only `"Bash"`) and `:346-347` (everything else → Other); `engine.rs:369-371` (free text: exclusions only) | TESTED: `r5b_shell_t3::g5_monitor_tool_is_shell` fails 8 of 8, on both volumes. With fix-mutant F1 (`"Bash" \| "Monitor" =>`) it passes (`mutation/fix_F1_F2.log`). The tool is real: Claude Code 2.1.325's own tool list in the project's spike recording `spikes/B16-search-command-forms/raw/q2.stream.jsonl` includes `"Monitor"`, and its schema in this session says "The script runs in the same shell environment as Bash". NOT verified: that the `PreToolUse` hook fires for `Monitor` (reasoned: hooks match by tool name). |
| m1 | Minor | The owner's list also waives the sandbox bypass. A listed command called with `dangerouslyDisableSandbox: true` is allowed with no card; unlisted, it is T3 with `SandboxBypass`. POLICY §10 item 9 says the bypass "is T3" with no exception. The entry binds only text + tool + cwd, not the call's other fields. | owner list `npm test` (Bash, ws); call `{"command":"npm test","dangerouslyDisableSandbox":true}`, `st.sandbox = On` | listed: `Allow { why: OwnerCommandList }`; unlisted: `Ask … tier: T3 … reasons: [ShellExpansion, SandboxBypass]` | `engine.rs:658-663`, `:809-832` | TESTED: `g5_owner_sandbox_off` fails; passes with fix-mutant F2 (refuse the list when `sandbox_disabled`). Owner decision: should a listed command keep the sandbox? |
| m2 | Minor | Wall-clock bound in a debug test is flaky under load. `q01::z_timing` asserts 50 ms per decision in an unoptimised build. In 1 of 22 full-suite runs, during mutant E8 (which changes no decision), it failed. The red-control runner's final "normal build" step also reported NOT GREEN once, and the runner throws away that output, so the cause cannot be seen. | `cat` with 16 000 operands, machine load ≈ 13–17 | `over the 50 ms bound: cat with 16000 operands: 52.069958ms`; runner: `NOT GREEN normal build fails` / `RED CONTROLS: 1 problem(s)` / exit 1 | `tests/q01_gate_attacks.rs:426`; `red-controls.sh` normal-build line (`>/dev/null 2>&1`) | TESTED: `mutation/mut_E8.log`, `logs/red_ci.log`. NOT reproduced in a full rerun (`logs/red_normal_rerun.log`, exit 0) or in 18 timing reruns (`logs/timing_repeat.log`, all rc=0). The code is not wrong; `check.sh` can fail on a busy machine for no code reason. |
| m3 | Minor | The 64 KiB byte bound has no test that fails without it. Mutant A3 (bound × 4) passes the seat's whole suite. The branch is correct. | `echo` + `" abc"` repeated to 65 537 bytes (one distinct word, so the word bounds do not fire) | branch: `DENY TooLargeToCheck`; under A3: `ASK T3` | `action.rs:556` | TESTED: `r5b_bound_probe::g5_byte_bound_denies_few_words` is green on the branch and red under A3 (`mutation/A3_bound_probe.log`). |
| m4 | Minor | A person's first name appears as a Windows user folder in test strings on the branch. | — | — | `crates/coagent-policy/src/path/winrules.rs:93`, `:110`; `crates/coagent-policy/tests/r4_gate_attacks.rs:254`, `:260`, `:261`, `:262` | TESTED: scan of `git diff 13bd10e..HEAD` added lines (`run2/hygiene_hits.txt`). The four r4 lines come from the round-4 gate's own file, added unchanged (that gate's slip, not the seat's; changing them needs a ruling). |
| n1 | Note | A compiled-out test seam still turns shell text into a lower tier: feature `red_shell_text_lowers` makes `cat X` a `Read` of `X`. It is reachable only by enabling a `red_*` feature, and nothing stops a build that does (no `compile_error!` guard; `--all-features` would include it). | — | — | `action.rs:577-591`, `Cargo.toml` `[features]` | READ. No other path in `src/` gives a shell call a kind other than `Execute` (grep for `Kind::Read`/`Search`/`Tier::T0-2`/`recognis`/`plain`; every hit read). |
| n2 | Note | Three defence-in-depth lines behind decision step [8] have no test that fails without them: the session scope's `Kind::Execute => None`, `Scope::ExactCommand => false`, and the grant's `Kind::Execute => Err`. Each survives as an equivalent mutant, because T3 asks at [8] before any of them is reached. | mutants E6, E7, E8 | SURVIVED (E8 "killed" only by the m2 flake) | `engine.rs:1032`, `:745`, `:940` | TESTED (mutation table). The code is correct on all 135,408 central decisions. |
| n3 | Note | Leftovers: `Reason::NotRecognised` is never constructed; comments still speak of "OPAQUE"; the shell sentence's variant is still named `ShellExpansion`. | — | — | `engine.rs:61`, `:347`, `:394`, `:43` | READ |
| n4 | Note | Owner-list cwd spellings `ws/`, `ws/.`, `ws//`, `ws/src/..` and `<root>/wsl/../ws` (wsl → ws) are allowed. Each names the same physical directory both lexically and physically (`cwd_is_physical` holds), so this is correct. My first run listed two of them as near misses; that was my test's error, and I corrected it. | — | `allowed=true` | `engine.rs:803-805` | TESTED (`g5_owner_exact`, both volumes) |
| n5 | Note | The r4 `p_identity_60k` RULING hunk replaces `rewrites.is_empty()` with "every generated line is deny-or-strict-T3". The new assertion goes red if any line is not strict T3, so it is not a weakening. Friday rules (STATUS A6.2). | — | — | `tests/r4_gate_attacks.rs:687-701`, `:790-797` | READ (diff after rustfmt) |
| n6 | Note | Remote `main` has moved (`454bfb5`; my clone's `origin/main` `18005d6`; merge-base `13bd10e`). A merge needs its own check. | — | — | — | `git ls-remote` |
| n7 | Note | A PowerShell UNC path (`Get-Content \\attacker.invalid\share\x`) is a strict T3 ask, not a deny. This is acceptable under the all-T3 rule. | as stated | `ASK T3 … reasons=[ShellExpansion]` | — | TESTED (`g4_b2_powershell_backslash`) |

## 2. Main job 1: no shell text lowers a decision below T3

**Structural (READ).** `classify` sends `"Bash"` and `"PowerShell"` through `shell_execute`, which always returns
`Kind::Execute` with a `Target::Command` first (`action.rs:300-301`, `:548-601`). The only exception is the 64 KiB
branch, which the engine denies. `assess` raises every `Target::Command` to T3 (`engine.rs:478`). Before step [8], only
two steps can allow anything:
- [7], which needs tier T0;
- [7b], the owner's list.

The scans only add a deny (exclusion or hard deny) or a reason line.

**Property (TESTED)** `r5b_shell_t3::g5_central_no_shell_text_below_t3`, case-insensitive volume:
`CENTRAL: 651 commands, 135408 decisions, {"ask": 100726, "deny": 34682}, 0 counterexamples`, 434 s.

- **Commands.** 49 bases (reads, searches, `git`, `npm`, `sudo`, `rm -rf`, PowerShell verbs, empty string, `\n`, `:`).
  Each was combined with:
  - one of 50 prefixes: `A=1 `, `env -i `, `command`, `builtin`, `exec`, `time`, `nohup`, `nice`, `\`, `''`, `xargs`,
    `sh -c`, `eval`, `.`, `source`, `!`, `{`, `(`, `noglob`, BOM, ZWSP, NBSP, TAB, CR, RLO, full-width `l`, `iex`,
    `pwsh -c`, `cmd /c`, `powershell -enc`, …;
  - one of 12 quoting transforms: single, double and `$'…'` quotes, TAB or doubled spaces, NBSP, `ſ`, upper case,
    backslash-escaped letters, escaped spaces, doubling;
  - one of 59 suffixes: newline, CRLF, `;`, `&`, `| sh`, redirections, here-doc and here-string, `$(id)`, backticks,
    `<(id)`, `${HOME}`, globs, braces, `!!`, `#`, NUL, ZWJ, combining acute, `; rm -rf ~`, `=ls`, `=(ls)`, …;
  - and a quarter of them with a second command joined by `;`, `&&`, `|`, newline or `||`.

  The corpus also includes 64 KiB, 64 KiB + 1 and 170-word lines.
- **Tools and hosts.** `Bash` and `PowerShell`, on `HostOs::Posix` and `Windows`.
- **Input shapes.** `command`; with `description`/`timeout`; `run_in_background`; `dangerouslyDisableSandbox`;
  `command` as an array, an object or null; `cmd` instead of `command`.
- **States, for the plain shape.** `every_mode`: link open or closed-tainted × wide grant or none × three surfaces,
  each with ExactInput, ReadsUnder and EditsToFile approvals and read memory. Each state also carries:
  - an `ExactCommand` approval for the very text and cwd;
  - a grant whose execute list names the very text, where the grant parser accepts it;
  - owner-list near misses (text ± a space, `\n`, trimmed, upper or lower case, `;`), for both shells;
  - the very text listed under the wrong directory (`ws/src`), for both shells.

  Each state is decided on its own surface and on `TerminalPrompt`.
- **Structural check per action.** `kind == Execute` and the first target is `Command`: 0 violations.
- **Shown red.** Under mutant E1 (shell raised to T0 instead of T3) the same test reports **85,644 counterexamples**,
  70,984 of them allows (`mutation/central_under_E1.log`).

**Leftover recogniser (READ).** I grepped `src/` for `Kind::Read`, `Kind::Search`, `Tier::T0`–`T2`, `recognis`,
`plain` and `opaque`, and read every hit. The only code that inspects shell text to grant a lower tier is the cfg-gated
red seam (n1). `recognise_posix` and `recognise_powershell` return `Result<Infallible, _>`, so they cannot succeed.
The scans (`shell/mod.rs`) feed only `PathRole::Mentioned` targets and `t3_words`, which only raise. **Holds**, except
for the tool-name gap M1, which is not shell text in a `Bash` or `PowerShell` call.

## 3. Main job 2: the owner's list parses nothing

**What the code compares (READ, `engine.rs:809-842`, `state.rs:233-253`):**
1. The first `Target::Command`'s `text` is the hook's `tool_input.command` string after JSON decoding, unmodified. It is
   compared with `==` on Rust `String`s, so byte equality: whitespace, a trailing newline, CR and NUL all count. There
   is no case folding and no Unicode normalisation (NFC `é` ≠ NFD `e´`). JSON escapes decode before comparison, so
   `"npm\u0020test"` equals `npm test`, the same bytes the shell receives.
2. The tool name must be exactly `Bash` with `ShellKind::Bash`, or `PowerShell` with `ShellKind::PowerShell`, and equal
   to the entry's shell.
3. The hook cwd's canonical path must equal the entry's canonical cwd, and the hook cwd's lexical form must equal its
   canonical form, so no symlink is in it.
4. The entry's text is stored verbatim; its cwd is canonicalised by `add_owner_command` (refused if unresolvable).

**TESTED, `g5_owner_exact`, both volumes.** Entries: `npm test`, `café --x`, `ls<TAB>src`, `printf 'a b'`,
`make<LF>` (Bash) and `Get-ChildItem` (PowerShell).
- **Positives allowed (8):** the exact bytes, the JSON-escaped spelling, and `run_in_background` + `timeout`.
- **Text near misses: 49, none matched.** Leading or trailing space, LF, CR, CRLF, TAB, NUL, BOM, ZWSP, ZWJ, NBSP, `;`,
  `;rm -rf ~`, `&& rm -rf ~`, `\nrm -rf ~`, `| sh`, `#`, an added argument, a truncation, three case variants,
  full-width, `ḿ`, quoting and escape forms, `> o`, `$'npm'`, NFD `café`, `CAFÉ`, `ls src`, a doubled tab, a vertical
  tab, `printf "a b"`, `make`, `make\n\n`, `make\r\n`, ` make\n`, and `Get-ChildItem` from Bash.
- **Wrong tool:** `PowerShell`, `Bash` across shells, `bash`, `BASH`, `Bash `, `powershell`, `mcp__shell__Bash`. None
  matched.
- **Wrong cwd:** `ws/src`, the parent, a symlink to ws, `WS` (upper case), `ws/<ZWSP>`, `~`, empty, relative. None
  matched.

**Mutants O1–O6** (trim, prefix, symlink accepted, tool not compared, sub-directory accepted, list removed) are each
killed by `t17::owner_exact_command_list` and by `g5_owner_exact`. **Holds.** Edge: m1 (the sandbox flag is not part of
the entry).

## 4. Main job 3: the two volume kinds (both exercised here)

The briefs name a case-sensitive and a case-insensitive volume (addendum 4 §2.1; STATUS A6.3 item 7).
- **Measured:** `/Volumes/Laptop-DEV` is `Case-sensitive APFS` (`diskutil`, plus a probe file in `run2/fixtures_cs`).
  `/private/tmp` (boot volume) is `APFS`, case-insensitive (probe in my scratchpad).
- **Exercised on both:**
  - `scripts/check.sh`: exit 0, 185 passed, 0 failed, `licenses ok`, on each;
  - `r5b_r4_regressions`: 6 of 6 on each;
  - `r5b_shell_t3`: the same results on each (the M1 and m1 tests fail on both).
- **Owner list, upper-case cwd:**
  - case-insensitive: the path exists and `realpath` returns the on-disk `ws`, so lexical ≠ canonical and there is no
    match;
  - case-sensitive: the path does not exist, so there is no match.
- **Only on the case-insensitive volume:** the central property (it takes 7 minutes); its logic does not depend on case.

## 5. Main job 4: round-4 Blockers and Majors, re-tested with my own inputs

`r5b_r4_regressions.rs` uses only API present at both heads. On **9170425** (archive of that commit, my build):
**0 passed, 6 failed** (`logs/g4_old_9170425_ci.log`). On **0ea9b95**: **6 passed** on both volumes.

| r4 | my test | old code (9170425) | branch |
|---|---|---|---|
| B1 assigning builtins (`printf -v HOME`, `read -r HOME`, `mapfile`, `readarray`, `getopts`, `print -v`, `IFS=/ read`, `printf -v OLDPWD … cd -`) | `g4_b1_assigning_builtins` (12 inputs) | 5 of 12 unsafe | all strict T3 |
| B2 PowerShell `\` paths, Posix and Windows hosts | `g4_b2_powershell_backslash` (11 × 2) | 9 of 11 unsafe (Posix) | 20 of 22 **denied** (HardDeny or Excluded), UNC = T3 |
| B3 quoted or keyword `eval`/`source`/`alias`/`export` (`'eval'`, `"eval"`, `e\val`, `then`, `time`, `noglob`, `command`, `builtin`, `exec`, `nohup`, `{ }`, `( )`, `!`) | `g4_b3_quoted_and_keyword_builtins` (20) | 14 of 20 unsafe | all strict T3 |
| B4 `cd` split (`.docker`, `.cargo`, Keychains, Cookies, Safari, gcloud, `pushd`) | `g4_b4_cd_split` (8) | 4 of 8 unsafe | all strict T3 |
| M1 brace blow-up (7 shapes, 2 s watchdog) | `g4_m1_blow_up_inputs` | 6 of 7 **not decided within 2 s** | 2.0–5.3 ms short shapes; 8–31 ms 30–63 KB shapes (all denied as too large) |
| M2 pipe-to-shell and interpreters (20 Bash + 7 PowerShell on 2 hosts) | `g4_m2_interpreters` | 16 of 20 unsafe | all strict T3, `RunsGivenCode` where named |

## 6. Main job 5: check.sh, red controls, mutation

| run | seat's claim | mine |
|---|---|---|
| `check.sh`, fixtures on the case-insensitive boot volume | exit 0, 185/0 | **exit 0**, 185 passed, 0 failed, `licenses ok`, `CHECK OK` (`logs/check_ci.log`) |
| `check.sh`, fixtures on the case-sensitive volume | exit 0, 185/0 | **exit 0**, 185 passed, 0 failed (`logs/check_cs.log`) |
| `red-controls.sh` (boot volume; the seat ran only the project volume) | 35/35, GREEN, exit 0 | **35/35 RED OK**, each first panic names its own property; final step **`NOT GREEN normal build fails`, exit 1** (m2); full rerun of that step: exit 0 |
| Windows clippy `-p coagent-policy --target x86_64-pc-windows-msvc -D warnings` | clean | **exit 0** (lib target) |
| 79 everyday commands (`r3::s5k`) | 12 refused, 67 red, 0 ordinary | **`12 DENIED, 67 T3, 0 T2`** |
| M1 timings | k3×17 2.0 ms; `{a,b}x`×9000 28 ms | 2.0–2.5 ms; 31.5 ms |
| `r4_gate_attacks.rs` at 7cb244b vs gate copy | identical | **identical** (`cmp`; sha256 `d27eaa64…c3db24` both) |
| scope `9170425..HEAD` | crate, `docs/POLICY.md`, `BACKLOG.md` | same, 22 files; no `Cargo.lock`, `scripts/`, `spikes/` or CI |

**Mutation table** (`run2/mutate_r5b.py`, 21 mutants of the fix sites, the whole crate suite each time except
`p_identity_60k` and my 7-minute central test; baseline failures, which are my M1 and m1 tests, subtracted; tree
verified restored against a fresh archive after the run). Full lists: `mutation/mutation_results.tsv`, `mut_<id>.log`.

| id | mutant | seat tests that go red | mine that go red |
|---|---|---|---|
| E1 | shell raised to T0 instead of T3 | 21, incl. `t17::every_shell_command_is_t3_in_every_state`, r2/r3/r4 gate files | all `g4_*`, `g5_owner_exact`; central (separate run) |
| E2 | [8] T3 no longer asks first | 5: `t06::t3_always_asks…`, `t17::every_shell…`, `r3::x4d`, `r4::a_opaque…`, `t14::git_and_edit…` | — (central covers it; not in this run) |
| E3 | T3 card batchable | 8, incl. `t06`, `t17` | all `g4_*`, `g5_owner_exact` |
| E4 | no T3 read delay | `t06`, `t17::the_card_carries_one_fixed_sentence` | all `g4_*`, `g5_owner_exact` |
| E5 | session_scope T3 guard removed | `t06::t3_always_asks…` | — |
| E6 | `Kind::Execute => ExactInput` in session_scope | **SURVIVED** (equivalent behind E5's guard) | — |
| E56 | E5 + E6 | many incl. `t08::an_answer_binds…`, `r4::a_opaque…` | all `g4_*`, `g5_resolve_never_session_for_shell`, `g5_owner_exact` |
| E7 | stored ExactCommand approval allows again | **SURVIVED** (equivalent behind [8]) | — |
| E8 | grant covers every shell command | only `q01::z_timing` at 52.07 ms, a **flake** (m2); in substance **SURVIVED** (equivalent behind [8]) | — |
| O1 | owner list: trimmed match | `t08::exact_command_scope`, `t17::owner_exact_command_list` | `g5_owner_exact` |
| O2 | owner list: prefix match | same | `g5_owner_exact` |
| O3 | owner list: symlinked cwd accepted | `t17::owner_exact_command_list` | `g5_owner_exact` |
| O4 | owner list: tool not compared | `t17::owner_exact_command_list` | `g5_owner_exact` |
| O5 | owner list: any sub-directory | `t08`, `t17` | `g5_owner_exact` |
| O6 | owner list removed | `t08`, `t17` | `g5_owner_exact` |
| A1 | `Bash` not classified as shell | many (r2, r3, r4, t01, …) | 5 `g4_*`, `g5_resolve…`, `g5_owner_exact` |
| A2 | `PowerShell` not classified as shell | r3, r4, t01, t14 | `g4_b2`, `g4_m2`, `g5_owner_exact` |
| A3 | 64 KiB byte bound × 4 | **SURVIVED** (m3) | `g5_byte_bound_denies_few_words` (separate run) |
| S1 | PowerShell `\` not a separator | `shell::tests::scan`, `t17::powershell_backslash…` | — (my B2 inputs are also caught by name forms) |
| S2 | `RunsGivenCode` reason never added | `t17::interpreter…`, `t17::round4_surviving…` | — |
| S3 | hard deny by-name match removed | `t05::bash_commands_naming…`, `t17` ×2 | — |

**My tests, each shown red once and green.**
- `g4_*` (6): red on 9170425, green on the branch.
- `g5_central`: red under E1, green on the branch.
- `g5_owner_exact`: red under O1–O6, green.
- `g5_resolve_never_session_for_shell`: red under E56 and A1, green.
- `g5_byte_bound_denies_few_words`: red under A3, green.
- `g5_monitor_tool_is_shell` and `g5_owner_sandbox_off`: red on the branch (M1, m1), green under fix-mutants F1 and F2
  (`mutation/fix_F1_F2.diff`, `.log`).
- `survey_tool_names` prints only.

## 7. Main job 6: protected gate files

- **r4.** `r4_gate_attacks.rs` at `7cb244b` is byte-identical to `gate_policy_tests_r4/r4_gate_attacks.rs` (`cmp`, equal
  sha256). Against `rustfmt --edition 2021` of that copy, HEAD differs in exactly three RULING-marked hunks (stand-ins
  for the removed `bash_plain`/`powershell_plain`, and the two `p_identity_60k` hunks, n5):
  `run2/integrity/r4_fmtref_vs_head.diff`.
- **q01.** Unchanged in `9170425..HEAD`.
- **r2.** One assertion `T2 → T3`, RULING-marked (`v_bounds_edges`); its over-bound assertion is unchanged.
- **r3.** One positive control `is_allow → T3`, RULING-marked (`x4a`); every variant assertion is unchanged.
- **Weakening.** No deny, non-shell, escaping, bounds or timing assertion is weakened.
- **Outside the crate since the merge-base `13bd10e`:** only `BACKLOG.md`, `docs/POLICY.md`, and the root
  `Cargo.toml`/`Cargo.lock`. The last two come from earlier rounds' allowed one-line workspace commits; nothing changed
  in this delta.

## 8. Main job 7: names and paths in the branch diff

Scan of every line added in `13bd10e..HEAD` (`run2/hygiene_hits.txt`, 78 hits). Real ones:
- **m4:** six test strings with a person's first name as a Windows user folder.
- **Coordinator's tree:** two relative paths into the coordinator's tree, `FRIDAY/0_Brain/…`, in
  `docs/POLICY.md:414` and `_quarantine_2026-11-17_shell-recogniser/README.md:20`. These are citations of the verdicts
  (Note; no drive or home path).

The rest:
- the coordinator's seat name in RULING marks, which the briefs require;
- `.env.local` / `.local/bin` patterns;
- `/System/Volumes/Data/...` automount roots;
- `@evil.com` URL tests;
- `/home/someone`.

I found no home-directory path, machine name or real drive path in code or tests.

## 9. NOT TESTED

- **Whether Claude Code's `PreToolUse` hook fires for `Monitor`** (M1 reach): reasoned only. The tool's existence and
  its shell semantics come from Claude Code's own tool list (spike recording, v2.1.325) and its schema in this session.
- **The `Workflow`, `RemoteTrigger`, `CronCreate` and `Skill` tools** in the same tool list: not examined to see
  whether they can run shell text.
- **Windows at run time:** clippy only; the Windows normaliser is untested at run time. No pwsh on this machine.
- **The central property on the case-sensitive volume:** it ran on the case-insensitive volume only. Every other test
  of mine ran on both.
- **`p_identity_60k` under mutation:** not run (skipped for time). It ran green inside both `check.sh` runs.
- **The red-control runner on the case-sensitive volume:** not run (the seat ran it there).
- **The cause of the runner's single NOT GREEN:** not determined, because its output is discarded (m2).
- **A merge into current `main`:** not done (n6).
- **Shell behaviour:** I did not execute any of the attack commands; all results are gate decisions only.

## 10. Re-run

All paths are absolute. `run2/` = `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_policy_tests_r5/run2`.

```
. run2/env_r5.sh            # toolchain read-only; private CARGO_HOME and target dirs in the gate scratchpad
git clone --branch m2-policy "/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/2_Project_Files" $S/work
cp run2/r5b_r4_regressions.rs run2/r5b_shell_t3.rs run2/r5b_bound_probe.rs $S/work/crates/coagent-policy/tests/
COAGENT_TEST_TMP=<dir on the volume kind> cargo test --manifest-path $S/work/Cargo.toml -p coagent-policy --offline \
    --test r5b_r4_regressions --test r5b_shell_t3 --test r5b_bound_probe -- --nocapture --test-threads 1
bash run2/run_checks.sh     # check.sh on both volumes, then red-controls.sh
python3 -I run2/mutate_r5b.py <archive of 0ea9b95 + r5b files> run2/mutation/mutation_results.tsv [ids]
```

Old-code red: run `r5b_r4_regressions.rs` against `git archive 9170425`.

## 11. My slips

- **Mutation run 1:** the driver mixed cargo's stderr and stdout, so test names lost their binary. I stopped it with
  TaskStop, which skipped its restore. `engine.rs` in my scratch tree was left mutated (E2); I found this with
  `diff -r` against a fresh archive and restored it. The driver now merges the streams and restores on SIGTERM, and the
  final run ended with the tree verified clean. The run-1 table is kept, marked
  `mutation_results_run1_attribution_broken.tsv`.
- **`g5_owner_exact`, first version:** it listed `ws/src/..` and `wsl/../ws` as near misses. Both are the same physical
  directory; corrected (n4).
- **Hooks:** two Bash calls were refused by the workspace hooks (a `=`-word separator; `git checkout` in a clone). I
  used `git archive` for the old and mutation trees instead.
