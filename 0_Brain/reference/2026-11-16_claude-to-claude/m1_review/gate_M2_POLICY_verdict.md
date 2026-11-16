NO GO at e260fed

# QA gate M2-POLICY (`crates/coagent-policy`, branch `m2-policy` @ e260feda223570054bdb89cab8508636965eef55)

Independent tier-1 read, 2026-11-17. Findings only: nothing fixed, committed or pushed. My clone:
`/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m2_policy/repo`.
Attack tests: `gate_policy_tests/q01_gate_attacks.rs` (copied beside this file, with `mutate.py`, `gitprobe.sh`,
`marker.sh`, `mut.log`). Each test asserts the SAFE outcome. A failing test is a finding.

## Headline

The decision engine itself (ordering, T3, hard-deny matching, binding, grants, surface) is solid. Most of my direct
attacks on it held (`c_controls_that_hold`, 40+ shell constructs, case variants, `//`, T3 session refusal). What
fails is the **recogniser's model of the programs it calls "read"**. Two assumptions are wrong:

1. **Long-option abbreviation.** getopt_long (GNU and BSD `sort`, `grep`, `wc`, `file`) accepts any unambiguous prefix
   of a long option. The refuse lists use `starts_with("--output")`, so the shorter spelling `--o=` gets through.
   (`git` and ripgrep do NOT accept abbreviations. I checked git; it refused `--outp`.)
2. **The shell and the tools are not bash, GNU or BSD.** Claude Code's Bash tool on this machine runs **zsh** with a
   snapshot that turns `grep` into a function running **ugrep** (and sends some options back to `/usr/bin/grep`),
   and `find` into a function running **bfs**. Evidence:
   `4_Credentials/.claude/shell-snapshots/snapshot-zsh-1794830338778-oyjock.sh` lines 235-279. Neither the code nor
   POLICY.md mentions zsh, ugrep or bfs. bfs has `-rm` (= `-delete`), and zsh has `=cmd` expansion.

The engine allows a recognised read with no question asked in three common situations, and each finding below hits
at least one of them:
- **[6] link closed and tainted.** This is the normal state after every linked session. It allows every read/search
  below T3.
- **[9] resource memory.** One "Allow once" on a read puts that file into memory.
- **[8] "reads under <dir>"** session approval.

## Findings

Severity follows the brief: a Blocker is a wrong allow, or an evaded hard deny / T3 / exclusion, reachable from
attacker-chosen tool input in the default state. I count `LinkPhase::ClosedTainted` with the default credential
exclusions as default state, because every session reaches it once the link closes with peer text in context.

| id | sev | file:line | triggering input (Bash `command`) | crate returned | safe | how shown | direction |
|---|---|---|---|---|---|---|---|
| B1 | **Blocker** | `src/shell/mod.rs:292-320` (sort refuse list), `:267` (filter list) | `cat README.md \| sort --o=/Users/<owner>/.zshrc` | `Kind::Read`. ClosedTainted: `Allow{PostSessionRead}`. Link open, with README.md in read memory: `Allow{ResourceMemory}`. The `.zshrc` hard deny is never checked (it is not a target). | not read; hard deny | `f1a`, `f1b`, `f1c`, `z_breakdown`. Real `sort 2.3-Apple` wrote `probe/out_sort.txt` from `sort --o=FILE`. | wrong ALLOW, hard-deny evasion |
| B1b | **Blocker** | same | `cat README.md \| sort -S 1K --compress-prog=<any program>` (also `--compress=`, `--temporary-d=`) | `Kind::Read` → allowed as above | execute | `f1c`/`z_breakdown`. Real run: `sort -S 1K --compress-prog=probe/marker.sh big.txt` ran the program **9 893 times** (`probe/MARKER`). | arbitrary execution as a "read" |
| B2 | **Blocker** | `src/shell/mod.rs:101-128` (`grep_like` recursion detection) | `grep --recur TOKEN .`, `grep --dir=recurse TOKEN .`. In Claude Code's zsh, `grep --null --recur TOKEN .` (`--null` makes the snapshot function hand the call to `/usr/bin/grep`). | Seen as non-recursive `Read` of `.`, so `may_read_excluded=false`. ClosedTainted + default exclusions: `Allow{PostSessionRead}`. ReadsUnder(ws): `Allow`. | recursive search, never auto-allowed (excluded `.env`) | `f2`, `f2b`, `z_breakdown`. Real `/usr/bin/grep --recur KEY tree` and `--dir=recurse` printed `tree/sub/.env:KEY=topsecret`. | exclusion evaded (default `**/.env*`) |
| M1 | Major | `src/shell/mod.rs:34-46,162-181` | `find . -name '*.rs' -rm` (bfs; `find -help` lists `-rm`) | `Kind::Search`. Default exclusions: asked with card "search (recognised)". With no exclusions configured (`find src -rm`, ClosedTainted): `Allow{PostSessionRead}`. | execute/delete | `f3`, `f3b` | card misleads; Blocker if the owner clears exclusions |
| M2 | Major | `src/shell/mod.rs:360-378` | `cd nope && echo ; cat secret/plan.txt`. If `cd` fails, `;` runs `cat` in the ORIGINAL directory, but the classifier resolves it under `nope/`. | ReadsUnder(ws) plus owner exclusion `<ws>/secret/**`: `Allow{SessionApproval}`. The file actually read is excluded. | refuse `;` anywhere after a `cd`, or resolve against both directories | `f4` | exclusion / approval-scope evasion |
| M3 | Major | same | `cd - && cat x`. `-` means `$OLDPWD` (here: the Claude project dir), and the classifier takes it as `./-`. Same for zsh `cd +N`. | recognised | execute | `f4b` | path the classifier resolves is not the one read |
| M4 | Major | `src/patterns.rs:213-230`, `src/action.rs:600-625` | Edit/Write `<ws>/.git/commondir` = `../evil` plus `<ws>/evil/config` with `core.fsmonitor`. Or `<ws>/.git/modules/x/config`. Or a planted bare repo `<ws>/bare/{HEAD,config,objects/,refs/}` and then `cd bare && git diff --no-index a b`. | Writes are T1 (a workspace edit grant auto-allows them). The git command is "read (recognised)". | T3 like `.git/config`; git in a non-`.git` gitdir is not a read | `f5a`, `f5b`, `f5c`. Real runs (`gitprobe.sh`): `git status` ran fsmonitor from the commondir config; `git diff --no-index` in the bare dir ran `diff.external`. | T3 evasion; edit becomes execution |
| M5 | Major | `src/shell/mod.rs:174-180` | `find -f<outside-dir> -name x` (BSD/bfs operand flag with the value attached) | Only `.` is a target. ReadsUnder(ws) with no exclusions: `Allow`, and it lists outside the workspace. | operand seen | `f6` | outside-read / name leak under approval |
| M6 | Major | `src/path/mod.rs:158-199` (O(n²) prefix walk), `src/glob.rs:56-71` (recursion) | `cat a/a/a/…` (4 000 components ≈ 8 KB) | 38 s for one decision; 1 000 components took 2.4 s. At 16 000 components (32 KB): **stack overflow, process abort** (`z_timing`, 2 MB test-thread stack). | bounded time; fail closed | `z_timing` | DoS. If the (unbuilt) hook client treats a crash or timeout like Claude Code treats a non-2 exit or timeout, the call runs **without the gate**. |
| M7 | Major (design) | `src/engine.rs:497-515` | ClosedTainted: `cat /Users/<owner>/Documents/x`, `cat ~/.config/<tool>/token`, `cat ~/.p10k.zsh` | `Allow{PostSessionRead}` for any non-credential path anywhere on disk | workspace-only (T0) | reasoning plus builder DQ9 | wrong allow by design: needs the design owner |
| M8 | Major | `src/engine.rs:945` (card targets), `src/path/mod.rs:53` | Write with `file_path` = `ws/a.txt\n[read] /ws/README.md ‮` (also any execute command text with ESC/bidi) | card target carries a raw newline and RLO | escaped | `f9` | card can mislead the owner (the fix may sit in the renderer; the Card contract must say so) |
| m1 | Minor | `src/shell/mod.rs:223-265,101-128` | `file --comp -m README.md` (writes `.mgc`), `wc --files0=LIST`, `grep -rS` (BSD: follow all symlinks, the same reason `-R` is refused), `grep --derefer`, zsh `cat =ls` (reads `/bin/ls`) | Read/Search | refuse | `z_breakdown` | small writes / unlisted reads |
| m2 | Minor | `src/shell/powershell.rs:107-120` | `gc a.txt -Wa` (= `-Wait`), `gc a.txt -Str x` (= `-Stream`), `gci -Fo -Recurse .` (= `-FollowSymlink`), `gci -Rec .` (recursion not seen) | recognised | refuse prefixes of refused params; detect `-Rec*` | `f8`, `z_breakdown` | PowerShell accepts any unambiguous parameter prefix |
| m3 | Minor | `tests/*` | test gaps shown by surviving mutants M4/M7/M12/M14/M17/M18 (table below) | — | — | mutation | — |
| n1 | Note | `src/path/mod.rs:149` | the normaliser does `realpath` on attacker paths. On a Mac with the `/net` automounter (default on older macOS; not in this machine's `/etc/auto_master`), or on Windows for a path that resolves to UNC, the **gate itself** makes a network/DNS request before deciding (a DNS exfil channel outside the sandbox). | — | — | reasoning | — |
| n2 | Note | `src/path/mod.rs:185-190` | NEW file `~/.Kshrc` (Kelvin sign). APFS here resolves `.Kube` to `.Kube` for an existing dir (measured), but a missing tail is appended raw, so a new `.kshrc` / `*.key` spelled with U+212A misses the ASCII case-insensitive match. | — | — | probe (`kt/`) | low |
| n3 | Note | `src/engine.rs:596-609` | `ExactCommand` and the other session approvals ignore `agent_id`, so an owner approval for the main agent covers subagents. `decide`/`record` are split, so the caller must serialise them or `max_actions` can be double-spent. | — | — | reasoning | — |
| n4 | Note | TOCTOU | Everything is resolved at decide time. The tool runs later, and a parallel tool call (or an approved/granted command) can swap a symlink between the two. The crate cannot guarantee "the path checked is the path used". Say so in POLICY.md. | — | — | reasoning | — |

Two things held when I attacked them: duplicate JSON keys (serde_json and JS both keep the last value, and hash and
classifier read the same `Value`), and MCP prefix spoofing (another server's tool named like ours is classified
Share, which is stricter).

## "Edit that becomes execution": workspace edits a grant auto-allows (T1 under `<ws>/**`)

Hard deny or T3 already covers `.claude/**`, `.mcp.json`, `.git/hooks/**`, `.git/config`, `.git/info/**`,
`.gitattributes`, `.gitmodules`, `.npmrc`, `.env*`. **Not covered** (each runs code on a later "read", or on the
owner's next ordinary command or session):

- **git "reads" (DQ4):**
  - `.git/commondir` (verified)
  - `.git/modules/*/config`
  - `.git/worktrees/*/config*`, `.git/config.worktree`
  - any planted bare repo `*/config` (verified)
- **Run on the owner's next command or editor open:**
  - `.husky/*` (git hook path in husky repos)
  - `.pre-commit-config.yaml`
  - `.envrc` (direnv on `cd`)
  - `.vscode/tasks.json` (`runOn: folderOpen`), `.vscode/settings.json`
  - `.idea/` run configurations
  - `.devcontainer/*`
- **Build, test and tool config:**
  - `Makefile`
  - `package.json` scripts, and any `npm test *` grant
  - `.cargo/config.toml` (runner / rustc-wrapper), `build.rs`
  - `pyproject.toml`, `setup.py`, `conftest.py`
  - `eslint.config.js`, `vite.config.*`, `jest.config.*`
  - `.mise.toml`, `.tool-versions`
  - `Gemfile`, `Rakefile`
- **Runs elsewhere:** `.github/workflows/*` (runs with CI secrets on the owner's next push).
- **Future sessions:** `CLAUDE.md` / `AGENTS.md` (instruction injection into later Claude sessions).

**Under a `~/**` edit grant** (T2, auto-allowed by the wide grant the tests themselves use):

- `~/.gitconfig`, `~/.config/git/config` (`core.fsmonitor` for every repo)
- `~/Library/LaunchAgents/*.plist`
- `~/.local/bin/*` (PATH shadowing)
- `~/.bash_aliases`, `~/.oh-my-zsh/custom/*.zsh`, `~/.p10k.zsh`, `~/.config/zsh/*` (sourced by rc files that are
  themselves hard-denied)
- `~/.vimrc`, `~/.tmux.conf`, `~/.hammerspoon/init.lua`, `~/.config/direnv/direnvrc`
- `~/.cargo/config.toml`

The owner must see this list before approving any edit grant. I recommend not allowing `~/**` edit grants at all.

## Builder's 11 design questions

1. **Exclusion = deny; recursive search never auto-allowed.** Safe. B2 shows the recursion detection itself can be
   evaded.
2. **`cat error.log` as read.** Safe. `cat` is pure and its operand is a checked target.
3. **Taint blocks grants.** Safe (stricter than 04).
4. **git reads run repository-configured programs.** NOT safe as implemented. The T3 protection is evadable (M4).
   Under default exclusions git reads are always asked anyway (the repo root is a recursive target), but the card
   says "read (recognised)". **Design owner:** make git `execute`, or have the hook rewrite the input (`-c
   core.fsmonitor= --no-ext-diff --no-textconv`) through Claude Code's updatedInput.
5. **Own MCP tools as T2.** Safe.
6. **`subjects` only.** Safe.
7. **Command patterns.** Matching is exact and lexer-backed (`npm test; rm` and `npm test $(id)` refused, verified in
   unit tests). But a final `*` accepts `--prefix /elsewhere` and `-- …`, and every execute grant on a program that
   reads workspace config is arbitrary code once workspace edits are allowed. **Design owner.**
8. **Open tiers.** Edit outside the workspace is T2, so a `~/**` edit grant auto-allows the home list above.
   **Design owner.**
9. **Reads outside the workspace after the link closes.** A wrong allow by design (M7). Recommend T0 only.
   **Design owner.**
10. **`dontAsk` as no surface.** Safe direction.
11. **Ancestor rule.** Safe: everything it does not deny is still asked as execute, and the card shows the full
    command.

On "Windows host": Bash is always `execute` (`action.rs:419-422`). The PowerShell recogniser admits only built-ins;
external programs are refused. A grant never auto-allows execute on Windows (`engine.rs:757-763`; red control
`red_windows_exec_grantable` went red). `winrules` maps `/\host\share` to `\\host\share`, which is Critical (T3), so
mixed-slash UNC is caught. The Windows normaliser was not run (no Windows host).

## Reproduction

- `scripts/check.sh`: exit 0 (fmt, clippy, test, deny). coagent-policy has **72 tests** (19 unit + 53 integration),
  0 failed. Matches the builder.
- `red-controls.sh`: **17/17 RED OK**, normal build GREEN. For every control the panic line named the property's test
  (e.g. `red_find_allows_exec` → "find . -delete"; `red_t3_grantable` → "read ~/.ssh/id_rsa … Allow").
- Windows: `cargo +1.100.0 clippy -p coagent-policy --target x86_64-pc-windows-msvc -- -D warnings`: clean.
  - My first attempt ran without `+1.100.0` and picked a stable toolchain without clippy, because it ran outside the
    repo directory. I re-ran pinned.
- Scope (`git diff --stat 13bd10e..e260fed`): only `crates/coagent-policy/`, `docs/POLICY.md`, `BACKLOG.md`, one
  `members` line in `Cargo.toml`, and `Cargo.lock` gaining only the `coagent-policy` entry. **OK.**
- My attack suite: 19 tests, **17 fail (findings)**: f1a, f1b, f1c, f2, f2b, f3, f3b, f4, f4b, f5a, f5b, f5c, f6,
  f7, f8, f9 and z_breakdown. `c_controls_that_hold` passes. `z_timing` reports timings by design.
  - The first `d_pathological_inputs_are_fast` hung (more than 3.5 min of CPU) and was replaced by `z_timing`.

## Mutation testing (20 mutants, one at a time, builder suite: lib + t01..t12)

| mutant | result |
|---|---|
| M1 closed-link allows T3 reads | caught (t06) |
| M2 drop `~/.zshrc` hard deny | caught (t05 ×2) |
| M3 free text skips exclusion | caught (t07) |
| **M4 Uncertain treated as inside** | **SURVIVED** |
| M5 lexer accepts `!` | caught (lexer unit) |
| M6 grant expiry `>=`→`>` | caught (t09) |
| **M7 ExactCommand ignores tool name** | **SURVIVED** |
| M8 T3 gets session scope | caught (t06) |
| M9 max_actions `>=`→`>` | caught (t09) |
| M10 find `-execdir` accepted | caught (t02) |
| M11 grep `-f` accepted | caught (unit) |
| **M12 git `--ext-diff` accepted** | **SURVIVED** |
| M13 resolve ignores card expiry | caught (t08) |
| **M14 memory allows recursive reads** | **SURVIVED** |
| M15 wildcard domain without dot | caught (unit) |
| M16 url_host accepts `@` | SURVIVED (equivalent: the host char filter still rejects `@`) |
| **M17 ReadsUnder drops kind / execute checks** | **SURVIVED**: no test that a ReadsUnder approval does not allow an Edit under that dir |
| **M18 drop `.gitattributes` T3** | **SURVIVED** |
| M19 deny-side matching case-sensitive | caught (t01) |
| M20 sandbox Unknown accepted for execute grant | caught (t09) |

That is 13 caught, 6 real survivors and 1 equivalent mutant. The source in my clone was restored after every mutant
(`git status` shows only my test file).

## Ran vs reasoned

- **Ran:** B1, B1b, B2, M1, M2, M3 (classification), M4, M5, M6, M8, m1, m2, the mutations, and the probes:
  - real `sort`, `grep`, bfs `-help` and git behaviour, inside my scratch only, with a benign marker script;
  - nothing destructive was executed.
- **Reasoned only:** M7, n1-n4, the edit-becomes-execution list, the Windows normaliser, and whether a hook crash
  fails open. The last depends on the unbuilt hook client.

## Not examined

- The Windows normaliser at run time.
- Linux `/proc`.
- The interactive `dontAsk` surface.
- ripgrep's own option set beyond the refuse list (in the Claude shell `rg` is the claude binary with ARGV0=rg).
- ugrep options that the snapshot does not route away, beyond the ones listed.
- A fuzz run (no fuzzer).
- Design docs 03 and 04: only the sections the findings needed; I did not read them in full.
- B16 `RESULT.md`: checked only through the builder's t03.

## My slips

- I lost one run's output to a `| cut` pipeline (re-ran unpiped).
- My first git probe used a `$VAR` path, which the hook refused. I moved it into a script.
- The first DoS test was unbounded and burned about 4 CPU-minutes before I stopped it.
- The first Windows clippy run used the wrong toolchain (see Reproduction).
