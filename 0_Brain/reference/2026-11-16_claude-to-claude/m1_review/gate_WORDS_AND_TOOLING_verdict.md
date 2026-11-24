VERDICT: GO WITH NOTES — head cf541edfee9a08a703af0b2a5fbf3a8764e6fec4
# Independent check: branch `words-and-tooling`

Head `cf541edfee9a08a703af0b2a5fbf3a8764e6fec4`, base `039b9875b69918c2a83e95d84f7f8169358b59d5`. Checked in my own clone; nothing in the project was changed. No model run, no cargo suite.

## BLUF
- Every changed line (121 added, 49 removed over 12 files) is listed below; every after-sentence I opened is TRUE at the head, and the README's every path exists and says what the README says of it.
- `rustenv.sh` finds the toolchain from the main tree and from a worktree, in bash and zsh, with `set -u`/`set -e`, with a space in the path; the base file fails in the worktree position (red control). `setup.sh` changed printed text and one header comment only (run, diffed). The two helper scripts are stricter or equal, never weaker.
- BACKLOG: the only removed lines are nine `[ ]` to `[x]` flips, each with a `Resolved:` sub-line; `docs/M0-OUTCOMES.md` is a pure append. Forbidden paths differ by 0 bytes (control 1065).
- No NO GO condition found. Notes only (one Minor: symlinked source path; one Note on the word "follows").

## Proofs (what I ran)
| What | Result |
|---|---|
| `git ls-remote` on the GitHub remote | `refs/heads/main` = base, `refs/heads/words-and-tooling` = head (TESTED) |
| `merge-base --is-ancestor base head` | yes (TESTED) |
| scripts of mine | `gate_words_and_tooling_tests/`: `t_rustenv.sh`, `t_envsh.sh`, `t_setup.sh`, `t_scan.sh`, `t_review.sh`, `t_bytescan.py`, `summ.py`; outputs `out_rustenv_head.txt`, `out_rustenv_base.txt` |

## 1. Scope (TESTED)
- `git diff --name-status base head`: 12 files, all `M`: BACKLOG.md, README.md, docs/M0-OUTCOMES.md, preview/BACKLOG-PREVIEW.md, preview/demo/{lan.md,one-mac.md,setup.sh}, spikes/U-B1-hook-allow-silent/{RESULT.md,review_map.py,scan_bytes.py}, spikes/W1-windows-exec-hook/RESULT.md, spikes/lib/rustenv.sh. Exactly the STATUS list; all in the brief's owned set. No mode change (`--summary` empty), `diff --check` clean, no `__pycache__`.
- Forbidden paths (`spikes/*/raw` and `raw/**`, `crates`, `scripts`, `preview/make-plugin.sh`, `preview/lib`, `preview/plugin-template*`, `preview/replay`, `Cargo.toml`, `Cargo.lock`, `docs` except M0-OUTCOMES): `diff | wc -c` = **0**. Control, same command on `docs/M0-OUTCOMES.md`: **1065**.
- Runner files: 43 files under `spikes/` matching the brief's runner names (a superset of the brief's list: includes every spike's run.sh and main.rs); `rev-parse base:f` equals `rev-parse head:f` for all 43. `scripts/env.sh` is not in the diff.

## 2. Every changed line
Full diff read line by line (121 + lines). The builder's table lists all of them except: the five `Pointer` lines are listed as one row (fine); I found NO changed line the table omits. See the table in "Every changed line" below.
- README: all 24 paths it names exist at the head (`cat-file -t` per path: blobs and trees; scripts/env.sh, scripts/check.sh also exist). Line 3 is byte-identical to the base (`cmp`), so "Private, pre-alpha, unreviewed." is byte for byte. Claims checked against their paths (READ): MCP tools `send`, `inbox_read`, `wait` = `crates/coagent-mcp/src/main.rs:92,107,112` (exactly three in `tools()`); relay "content-blind ... can read nothing" = `crates/coagent-relay/README.md`; `coagentd --gate` = main.rs:98; `coagentd watch --data-dir` = main.rs:28,76; DAEMON.md headings `## 8. Gate mode` (:757), `### Local activity` (:889), `## 6a. Windows` (:536) exist; policy decides allow/ask/deny (coagent-policy lib.rs:4) and the daemon depends on it and calls it (`gate.rs`); "the daemon does not write yet" the audit log: no `coagent_audit` use in daemon, mcp or hook sources and no dependency (docs/AUDIT-HOST.md:3-4 agrees); an ask goes to Claude Code's own prompt = DAEMON.md section 8 "Decisions"; check.sh does fmt, clippy, test, deny licenses. No mode name (grep for mode/approve/trust/controlled/grant: only "gate mode", a DAEMON.md heading term, and the decision word "allow"), no date, no person, machine, account or local path (byte scan, item 7).
- Spike RESULT sentences (READ the raw maps around each): `:37`/M8 row "an undocumented `serverClassifierContext` record follows the Bash call": `raw/M8-fresh-ask/review_map.txt` shows the Bash message `context_sent_for_it=yes` (1 context record). TRUE except the word "follows", an order the program does not test (Note N1). `:57` "every assistant message carries ... `serverClassifierRequest`": every assistant line in all six auto maps (M1-fresh-ctl/hook, M8-fresh-ask/ctl, M9-fresh-ctl/hook) is `=yes`; the two non-auto maps are `=no`. TRUE. `:38` "among the auto sessions, absent only under a hook allow": context records are 1 in the three no-hook maps and the hook-ask map, 0 in M1-fresh-hook and M9-fresh-hook. TRUE. `:22` "consistent with the hook deciding first; the order was not measured": claims less than before. TRUE. `:52` "0 hits over its classes ... run from another checkout it can flag scratch paths": I ran the scan from another location: 9 files hit class `workspace_path`, exactly BACKLOG M-1's symptom. TRUE.
- W1 figure 4,030: line 190 of `raw/stageC_WO-19.txt` is the init event (`"subtype":"init"`, tools list holds Bash and PowerShell); 4030 characters at `ce7276c` and at the head (`wc -c` 4031 with newline; Python length 4030 both). `ce7276c` is "the stream init events' own uuid -> <event-uuid>", so "after the session-id and event-uuid placeholders" is TRUE.

## 3. BACKLOG.md and docs/M0-OUTCOMES.md (TESTED)
- Removed lines: 9, each a pure `- [ ]` to `- [x]` flip (Python check: 0 non-flip removals): the `scripts/env.sh` worktree entry, F11 headings, sign-in sentence, `rustenv.sh`, N-b, N-d, N-e, N-f, W-GATE-TEST r2 m1. Each has a `Resolved:` sub-line. All other added lines (15) are `  - ` sub-lines or the flipped line itself. Entries left open (M-1, N-c, :712 design half, F-umask/`mkdir` code half, n2, n3) got `Partly resolved`/`Note`/`Left by ruling`/`Amended` sub-lines only; n3's old text is untouched.
- Each closed entry is really resolved: env.sh (below), headings 1..10 (item 5), sign-in sentence (one-mac.md step 6 and setup.sh), rustenv.sh (item 4), N-b/N-f (item 6), N-d (the coordinator's ruling FR-1; M9 lines 104-106 untouched), N-e and m1 (sentences present).
- `scripts/env.sh` at the head, read: walks up from the checkout to the nearest folder holding `tools/cargo/bin/cargo`. My fixture (`t_envsh.sh`): main-tree and worktree positions, bash and zsh: `CARGO_HOME=<proj>/tools/cargo`, `CARGO_TARGET_DIR=<proj>/tools/target/workspace`, `cargo 1.100.0`. So it does find the toolchain from a worktree; entry correctly closed.
- `docs/M0-OUTCOMES.md`: base is 146 lines, the diff is `+147..151` only. The paragraph's two claims are true (see item 2).

## 4. `spikes/lib/rustenv.sh` (read whole, TESTED)
Logic: picks its own path from `BASH_SOURCE`, else zsh `%x` (via `eval`), else `$0`; walks up the logical parents until a folder holds `tools/rustup` and an executable `tools/cargo/bin/cargo`; exports three variables and PATH; else prints one line to stderr; unsets its temporaries.
My fixture (`t_rustenv.sh`, `env -i`): `proj/tools` symlink to the real tools; file copied to `proj/2_Project_Files/spikes/lib` and `proj/worktrees/x/spikes/lib`, plus a copy under a path with a space.
| Case (bash and zsh, each plain / `set -u` / `set -e` / `set -eu`) | head | base (red control) |
|---|---|---|
| main-tree position | OK, `cargo 1.100.0` | OK |
| worktree position | OK | FAIL (`worktrees/tools`, "command not found") |
| path with a space | OK | FAIL |
| via a symlink to the project folder | OK | FAIL |
| via a symlinked FILE or DIRECTORY living outside the project | prints the one line, exports nothing (Minor M1) | same |
| no toolchain above | one line on stderr, rc 0, 3 variables empty, PATH unchanged, no `_coagent*` leak, in bash and zsh | exports `<neg>/tools/...` and prepends a missing folder to PATH |
The 24 positive head cases with a real cargo all pass; the base fails every worktree-position case.

## 5. `preview/demo/setup.sh` (TESTED)
- Diff: line 12 gains one header comment line (true: `mkdir -m 700 "$ROOT"` at :31, refusal at :27); nine `## n.` heading lines renumbered inside the `cat <<EOF` text; one printed `# Before starting each one ...` line added inside the heredoc (no `$` or backtick in it, so no expansion). `--numstat` 11/9 matches. No code line changed.
- Ran base and head (`t_setup.sh`) with four `#!/bin/sh` stubs into scratch roots: both exit 0, root mode 700. Headings base `1 3..11`, head `1..10`. `diff` of the two normalised `COMMANDS.txt`: only the nine heading lines and the one added sign-in line (the same as the builder's).

## 6. `scan_bytes.py` and `review_map.py` (READ and TESTED)
- scan_bytes.py: docstring; new `OWN` set of two paths; `scan_bytes(name, b, own)` strips only `"lit"` / `'lit'` of the six synthetic literals and only when `own`; both call sites pass `abspath(...) in OWN`. That is N-b exactly (path, whole quoted literals). It strips LESS than the base, so it cannot miss more. 
- Tests (`t_scan.sh`, base scanner beside the head's redact.py): a planted file with mail, `sk-ant-...`, `req_...`, uuid: base and head both find email, token, session_id, request_id. Same planted text in a file named `redact.py` elsewhere: both find it. A file named `scan_bytes.py` elsewhere holding only a quoted synthetic literal: base `{}` (hidden), head finds it (red control for N-b). Bare synthetic literal in a normal file: both find. Adjacent real mail next to a quoted synthetic: both find 2. Head's own `redact.py` and `scan_bytes.py` with `--control`: `{}` (no false hit). `--planted` binary: head finds 5 classes. Full `--rev` scan of the head tree from a scratch repo: byte-identical output to the base scanner over the same tree (9 files, class `workspace_path`, the M-1 effect, not a regression).
- review_map.py: docstring line (N-f first half) and `q is not None and q in ctx`. Test (`t_review.sh`): a context record without `request` and an assistant record without request: base says `context_sent_for_it=yes`, head `no`; two other synthetic transcripts give the same output at base and head. Only FR-3's two allowed changes.

## 7. Byte scan of the 121 added lines (TESTED)
`t_bytescan.py`; needles passed on the command line at run time (account name, full name and its parts, host names, home path, volume and user path roots, drive and workspace words, mail-service words, the client names, plus four forms: raw, backslash-stripped, URL-decoded, slug), plus built-in classes: uuid, `toolu_`, `req_`, `msg_`, mail address, `/Users|/home|/Volumes` path.
- Result: 4 hits, all one needle (the coordinator's role name) in one line: the flipped N-d line "carries the coordinator's M9 sentence", which already existed at the base (36 mentions in the base BACKLOG.md); the added content is only the `[x]`. No person, account, machine, mail, path, uuid, `toolu_`, `req_` or `msg_` in any added line.
- Control: one planted line (account name, `/Users/..` path, uuid, `toolu_`) appended to a copy: 31 hits, found.

## Every changed line
| File | Before | After | True at head? |
|---|---|---|---|
| README.md 5-13 | CONTROLLED / APPROVED TRUST paragraph; "Nothing here is product code yet. `crates/` holds empty placeholder crates" | "What exists today" list (6 bullets) + "Open work ... `BACKLOG.md`" | TRUE; paths and claims opened (item 2); `:1`, `:3`, `:15-18` kept |
| RESULT (U-B1) M1-fresh-hook | "(the hook decided first)" | "(consistent with the hook deciding first; the order was not measured)" | TRUE (weaker claim) |
| same, M8-fresh-ask | "a server review context was sent for the Bash call" | "an undocumented `serverClassifierContext` record follows the Bash call" | TRUE; "follows" order not tested (N1) |
| same, M9-fresh-ctl | "and it is absent only under a hook allow" | "and, among the auto sessions, it is absent only under a hook allow" | TRUE |
| same, redaction line | "`scan_bytes.py` (addendum 2), 0 hits." | "... 0 hits over its classes: redact.py's names and the workspace paths it knows; run from another checkout it can flag scratch paths (third check, M-1)." | TRUE (ran it) |
| same, auto facts | "it marks every assistant message for a server review (`serverClassifierRequest`)" | "every assistant message carries an undocumented `serverClassifierRequest` record" | TRUE (6 of 6 auto maps) |
| RESULT (W1) :135 | "and 4,054 again now that the session id is `<session-id>`" | "and 4,030 at `ce7276c`, after the session-id and event-uuid placeholders" | TRUE (counted) |
| setup.sh header | (none) | one comment line: makes the root, mode 700, do not mkdir | TRUE |
| setup.sh printed headings (9) | `## 3.`..`## 11.` | `## 2.`..`## 10.` | TRUE (run) |
| setup.sh printed | (none) | one `# Before starting each one, check ... signed in ...` line under `## 4. Sessions` | TRUE; same fact as `lan.md` 72-75 (for the host's session) |
| one-mac.md step 6 | "...Accept the folder-trust dialog |" | "...dialog. Before starting each one, check ... signed in ... (on the day, a session did not start working until it was) |" | TRUE |
| lan.md step 2 | "...The guest half it builds goes unused here." | adds "It makes `<root>` itself and refuses one that exists: do not `mkdir` it first." | TRUE (setup.sh:27,31) |
| BACKLOG-PREVIEW.md :3 | "...these move there when the preview merges." | "The preview has merged; of these items only the witness one is also in `BACKLOG.md` (...). The others stay here until a lane moves them." | TRUE (quoted title found in BACKLOG.md) |
| BACKLOG-PREVIEW.md (5 entries) | none | one `Pointer` line each | TRUE (no model run, no behaviour change) |
| rustenv.sh | root = three folders above | walk-up; bash/zsh; one line when none | TRUE (item 4) |
| scan_bytes.py (4 hunks) | basename match, substring strip | path match, whole quoted literals | as FR-3 allows (item 6) |
| review_map.py (2 hunks) | no docstring warning; `q in ctx` | docstring line; `q is not None and q in ctx` | as FR-3 allows |
| BACKLOG.md | 9 `[ ]` entries | 9 `[x]` + 15 sub-lines | each Resolved/Partly/Note line is accurate (item 3) |
| M0-OUTCOMES.md | (end at 146) | 5 appended lines | TRUE |

## Findings
| ID | Severity | File, line | Finding | Fix in words |
|---|---|---|---|---|
| M1 | Minor | spikes/lib/rustenv.sh:338-345 | The walk uses the logical path. Sourced through a symlinked file or directory that lives outside the project folder, it finds no toolchain: prints the one line, exports nothing (safe; same as base). | Resolve the file's real location (`pwd -P` or a readlink loop) before walking, or state the limit in the header comment. |
| N1 | Note | spikes/U-B1-hook-allow-silent/RESULT.md (M8-fresh-ask row) | "follows the Bash call" asserts an order; `review_map.py` matches context to request and never tests order. The old text for M1/M8-ctl uses the same word. | Say "is present for the Bash call". |
| N2 | Note | preview/BACKLOG-PREVIEW.md:7-13 | The first entry (the witness) has no Pointer; it is also in `BACKLOG.md`. The builder's table says 5 entries; brief said each entry. Reasonable, but the file does not say why. | One words line on that entry, or say so in line 3. |
| N3 | Note | README.md:14,20 | "allow, ask or deny", "gate mode", "phase 1" are the code's and DAEMON.md's own terms, not the owner's modes; fine under FR-7 but a reader could take them for modes. README says Windows "as a guest only" without saying no Claude Code session runs there (windows.md title says "no Claude Code"). | Optional: add "(no Claude Code session)". |
| N4 | Note | STATUS_WORDS_AND_TOOLING.md property 2 | The builder's check output shows `INSERTION` placeholders for six inserted-text pairs, so those pairs were not machine-checked; I checked them by diff and by hand. | None needed; all true. |
| N5 | Note | BACKLOG.md (N-d line) | The flipped line contains the coordinator's role name; it is old text, only the checkbox changed. | None. |
| N6 | Note | scan_bytes.py | From any other checkout the scan hits 9 raw files on `workspace_path` (M-1, open). Identical at base. | M-1's explicit roots, a later lane. |

## NOT checked
| Item | Why |
|---|---|
| Any cargo build, test, or the real main-tree checkout | out of scope; no cargo suite |
| Whether `docs/DAEMON.md` text claims "encrypted" in so many words | README's "encrypted" rests on the crypto crate and the "sealed" frames of DAEMON.md; I read the dependency and sealed-frame text, not the crypto code |
| Content of other spikes' raw files for names | forbidden paths are byte-identical to the base; only added lines were scanned |
| zsh option variants (e.g. `setopt` changes to function-arg-zero) | tested default zsh only |
| The builder's own scan tool and its 23-needle claim | I ran my own scan instead |
| `scripts/check.sh` actually running | not run |
