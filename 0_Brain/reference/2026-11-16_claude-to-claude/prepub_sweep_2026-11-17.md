# Pre-publication sweep: kamilkreiser/coagent (2026-11-17)

**Summary (3 lines)**
1. As it stands: NO. Two client/company names (`nexusai`, `hpsm`), the owner's macOS username and the machine/volume layout sit in committed spike logs, and they are in all 74 commits of history, so deleting them on `main` is not enough.
2. After a history rewrite (or publishing a fresh squashed repo without `spikes/*/raw`) plus about 4 small fixes it is YES: no real secret was found anywhere, one author identity (a GitHub noreply address), Apache-2.0 present.
3. Internal-process references (Friday/FRIDAY paths, "coordinator", gate verdict file paths, a BACKLOG of known unfixed gaps) are lower-severity and are a policy decision for Kam.

Repo: 74 distinct commits, 6 remote branches (main, m1-core, m1-daemon, m1-relay, m2-policy, m3-audit), 470 files on main, pack 1.34 MiB. No tags.

---

## 1. Secrets
| Finding | Location | Judgement |
|---|---|---|
| No real secret found. No `.env`, `*.pem`, `*.key`, `keys/`, `credentials/`, `.ssh/` path in any commit (ls-tree on every branch plus `git log --all --name-only`). | all refs | none |
| `ghp_16C7e42F...` (GitHub example PAT shape) | `crates/coagent-audit/tests/*` (redaction tests, 14 commits) | FIXTURE: redactor test input, asserted to be masked |
| `ghp_` + `"a1".repeat(..)`, `ghp_0123456789<zero-width>abcdefghijklmnop`, `xoxb-1234-5678-abcdefghijkl`, `xoxb-123456789012-abcdefABCDEF`, `AKIAIOSFODNN7EXAMPLE` (AWS documentation example), `Bearer Zm9vYmFyYmF6cXV4MTIz` (base64 of "foobarbazqux123"), `github_pat_`/`xox*` prefix lists | `crates/coagent-audit/src/redact.rs`, `tests/redaction.rs`, `gate_r2.rs`, `gate_attacks.rs`, `no_content_in_debug.rs` | FIXTURE: synthetic redactor inputs |
| `-----BEGIN RSA PRIVATE KEY-----` with `MIIEowIBAAKCAQEAu1SU1LfV...` (2 lines, truncated, no END body), `BEGIN OPENSSH PRIVATE KEY` with `b3BlbnNzaC1rZXktdjEAAAAABG5vbmUA...` ("none" cipher header only), `BEGIN PRIVATE KEY` with `ab/cd.ef/gh_ij` | audit redaction tests (patch lines 20136, 25391-93, 32675-76) | FIXTURE: truncated, not parseable keys; they test the PEM masker |
| `Pa55w0rdXyz@db.internal`, `hunter2pw@example.com` | `crates/coagent-audit/tests/redaction.rs`, `gate_attacks.rs` | FIXTURE: URL-password masking tests |
| Session ids, `apiKeySource: none` | spike `raw/*.stream.jsonl` | not credentials; apiKeySource is `none` |

Count: 0 real secrets, about 8 distinct fixture patterns.

## 2. Personal data
| Item | Where | Count / spread |
|---|---|---|
| Owner's macOS username `kamilkreiser`: `/Users/kamilkreiser/.local/share/claude/versions/2.1.325`, `/Users/kamilkreiser/.zshrc`, `/Users/kamilkreiser/1FILES TO SYNC/HPSM-POC/...` | `spikes/U6-configchange-block/raw/{baseline-noedit,block-edit-confighook,control-edit-noconfighook}.debug.log`; `spikes/B16-search-command-forms/raw/q7,q10,q14,q18.stream.jsonl` | present in 70-72 of 74 commits, on main and all branches |
| GitHub username `kamilkreiser` and remote URL `git@github.com:kamilkreiser/coagent.git` | same debug logs (`Git remote URL: ...`) | 3 files; this is the public repo's own address, low concern |
| Volume/machine layout `/Volumes/Laptop-DEV/FRIDAY/...`, `/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/2_Project_Files/...`, `/Volumes/Laptop-DEV/WEDNESDAY/2_Project_Files/fleet/...`, `/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/...` | about 100 files under `spikes/*/raw/`, `spikes/*/output.txt`, `spikes/lib/common.sh` (line 13 default path to the coordinator's `models_latest.json`) | 68-73 commits each |
| `memory_paths.auto` = `/Volumes/Laptop-DEV/FRIDAY/4_Credentials/.claude/projects/...` and `transcript_path` | spike `*.stream.jsonl` init lines, `B16/raw/hook-events.jsonl` | reveals the credentials folder layout (no contents) |
| Local socket path `/tmp/cc-socks/54098.sock`, Claude Code version 2.1.325, tool/skill/plugin lists | spike init lines | cosmetic |
| Distinct emails in file content (all history): `git@github.com` (ssh user), `bob@example.com`, `hunter2pw@example.com`, `Pa55w0rdXyz@db.internal`, `docs.nginx.org@evil.com`, `user@evil.com`. | tests, `crates/coagent-policy/src/action.rs`, debug logs | NO personal email addresses in content |
| Commit author/committer email | `kamilkreiser@users.noreply.github.com` only | see section 6 |
| `Co-Authored-By: Claude ... <noreply@anthropic.com>` | commit messages: Opus 5.5 x52, Sonnet 5.5 x14, Fable 5.2 x7 | fine |
| Phone numbers | none | |
| IPs | only loopback, RFC1918/CGNAT/TEST-NET (`203.0.113.9`), `255.255.255.255`, test values (`6.6.6.6`, `7.7.7.7`, `8.8.8.8`, `4.4.1.1`); `2.1.325.758` is a version string | no real hosts |
| Real names other than the owner's | none found (only "Kam" in a commit and `m2-policy` quarantine README) | |
| Hostnames | none real; only generic words in `spikes/C1/C2 RESULT.md`, `docs/POLICY.md` | |

## 3. Other clients or companies
All hits are in ONE file family. Case-insensitive regex `secuura|datasec|nexusai|hpsm|kintsugi|cypherkey|mypki|vision sales` over every commit.

| Term | File | Commits | Line |
|---|---|---|---|
| `nexusai` | `spikes/B16-search-command-forms/raw/q14.stream.jsonl`, line 8 (a `find` tool_result) | 70 | `/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/nexusai/notes.md` and about 45 more `.../projects/nexusai/qa-trees/gate2x.*/.../node_modules/resolve/.claude/notes.md` |
| `hpsm` | same file and line | 70 | `/Users/kamilkreiser/1FILES TO SYNC/HPSM-POC/.tools/npm-cache/_npx/.../notes.md` |
| `secuura`, `datasec`, `kintsugi`, `cypherkey`, `mypki`, `vision sales` | none | | |

Same line also leaks the internal path `WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1030/...` (a QA agent's scratch layout).
Count: 2 distinct terms, 1 file, same line.

## 4. Internal process material
| Where | What | Branches |
|---|---|---|
| `BACKLOG.md` (main, all branches; 2 extra items on m2-policy, m3-audit) | "fix backlog" of KNOWN UNFIXED weaknesses: verify-words give no protection on introduced pairs (convener-as-relay, about 2^16.5 offline trials); `spake2` 0.4 not RFC 9382 and no key confirmation; ConfigChange hook is load-bearing and does not cover every route (hooks can be disabled mid-session); skill-frontmatter hooks lost on `--resume` (ungated); Elicitation auto-answerable by a hook; search recogniser classification gaps | main = all |
| `README.md` | says "Private, pre-alpha, unreviewed ... Nothing here is product code yet" (must be edited if going public) | main |
| `spikes/README.md`, `spikes/lib/common.sh`, `spikes/B17-smallest-model-red-tests/RESULT.md` | "the coordinator's models file / models_latest.json", "the brief named" | main |
| `crates/coagent-relay/src/gate_r2_state.rs`, `crates/coagent-*/tests/gate_*.rs`, `scripts/red-controls-core.sh` | file names and comments about review "gates", "round 2", "brief" | main |
| `crates/coagent-policy/_quarantine_2026-11-17_shell-recogniser/README.md` | cites `FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_M2_POLICY_verdict.md` and `..._r2_verdict.md` (two NO GO verdicts), "Decision (Friday, addendum 3; put to Kam on a card)", describes the shell-recogniser bypasses (symlink `cd ..`, ugrep `--include`, `"$?[PATH=7]"`, etc.) | m2-policy only (not on main) |
| `// RULING (Friday, 2026-11-17, addendum 3 ...)` comments, about 25 lines | `crates/coagent-policy/tests/{q01,r2,t01,t02,t03,t04,t07,t08,t09,t13,t14}*.rs` | m2-policy only |
| Commit messages naming "Friday", "FRIDAY/0_Brain/...", "m1_review/gate_core_tests", "brief §5", "Friday-authorised" | about 8 commit messages | all history |
| Unfixed vulnerability verdicts on main: none as documents; the BACKLOG above is the closest | | |
| TODO/FIXME describing security holes: none (the "TODO" hits are `grep TODO` test strings in spike data) | | |
| Old product credentials or download links: none | | |
| `ci/proposed-workflow.yml` | proposal only, no secrets | main |

## 5. Licence and hygiene
| Item | Result |
|---|---|
| LICENSE on main | yes, Apache License 2.0, 202 lines, standard text with no copyright-holder line; `Cargo.toml` `license = "Apache-2.0"`, `publish = false` |
| README.md | yes (root and each crate) |
| SECURITY.md / CONTRIBUTING / NOTICE | none |
| Third-party code copied in | none found (no vendor/ dir, no SPDX/Copyright headers outside LICENSE). Third-party only via Cargo.lock (6 lock files, 4 under `spikes/`). `deny.toml` present |
| Binaries | none (numstat shows no binary change in any commit) |
| Machine-generated scratch committed | YES: `spikes/*/raw/` is 84 `.jsonl`, 58 `.rc`, 58 `.err`, 10 `.log` files, about 962 KB of recorded Claude Code session streams/debug logs on main (of about 2.5 MB total tree); includes per-run `input.<ts>-<pid>.json`. No `target/` or `node_modules/` committed |
| .gitignore | `target/ node_modules/ .env* *.pem *.key .DS_Store` |

Top 15 largest blobs in history (all text; no large binaries):
| Size (bytes) | Path |
|---|---|
| 105494 | crates/coagent-daemon/src/engine.rs |
| 105306 | crates/coagent-daemon/src/engine.rs |
| 103575 | crates/coagent-daemon/src/engine.rs |
| 86276 | crates/coagent-daemon/src/engine.rs |
| 85621 | crates/coagent-daemon/src/engine.rs |
| 82761 | crates/coagent-daemon/src/engine.rs |
| 82395 | spikes/U13-licences/Cargo.lock |
| 78092 | crates/coagent-relay/src/state.rs |
| 78038 | crates/coagent-relay/src/state.rs |
| 70703 | crates/coagent-relay/src/state.rs |
| 70647 | crates/coagent-relay/src/state.rs |
| 48712 | spikes/G5-openmls-sanity/Cargo.lock |
| 48337 | crates/coagent-audit/src/bundle.rs |
| 47875 | crates/coagent-audit/src/bundle.rs |
| 47052 | crates/coagent-relay/src/state.rs |

Branch state vs main (ahead/behind): m1-core 0/16, m1-daemon 9/0, m1-relay 0/0, m2-policy 14/28, m3-audit 16/15. Unmerged branches carry extra internal material (quarantine README, RULING comments).

## 6. Commit metadata (all branches, 74 commits)
| Author | Committer | Commits |
|---|---|---|
| Kam Kreiser <kamilkreiser@users.noreply.github.com> | Kam Kreiser <kamilkreiser@users.noreply.github.com> | 74 |

One identity, a GitHub noreply address, no personal email in metadata.

---

## Blocking / fix list (summary)
1. Remove `spikes/*/raw/` (or at least `B16 q14.stream.jsonl`, the U6 `*.debug.log`, `B16 hook-events.jsonl`, all stream/hook-event/pane files) from ALL history; `git filter-repo` or publish a fresh squashed repo. A plain deletion commit leaves nexusai/hpsm/username in history.
2. Scrub `/Volumes/Laptop-DEV/...` from `spikes/*/output.txt`, `spikes/lib/common.sh` and RESULT files (non-raw files with the same layout).
3. Edit README ("Private, pre-alpha, unreviewed") and decide on BACKLOG.md (it lists known unfixed security weaknesses of a security tool) and the "Friday/FRIDAY/0_Brain/gate verdict" mentions in commit messages and on m2-policy/m3-audit.
4. Add a copyright holder line / SECURITY.md (optional hygiene).

## Method and coverage
- Clone: `git clone` with the deploy key, all branches fetched; `git branch -r` listed 6 branches plus `origin/HEAD`. No tags (`for-each-ref` shows only heads and remotes).
- Coverage: `git rev-list --all` = 74 commits; every search below passed all 74 revs explicitly (`git grep ... <all 74 revs>` via a python wrapper, run with `python3 -I`), plus `git log --all -p` dumped to a 5.9 MB patch file (74 `COMMIT` headers counted) for the secret-pattern pass. Commit metadata: `git log --all --format=%an/%ae/%cn/%ce`. Blob sizes: `git rev-list --objects --all | git cat-file --batch-check`. Per-branch greps used `git grep ... <branch>` for the 6 branches.
- Patterns: private key header, `ghp_`, `github_pat_`, `sk-`, `xox[bap]-`, `AKIA`, `Bearer`, `(password|secret|token|key)=...16+`, hex 32+ assigned to key names, `sk-ant|ANTHROPIC|OAUTH`; emails; `/Users/`, `/Volumes/`; IPv4; phone; client names; agent seat names; `vulnerab|exploit|unfixed|known gap|BLOCKER|TODO|FIXME`; hostnames.
- Positive controls: patch file `grep -c coagent` = 4262 (present); `PRIVATE` = 12 (present, and the key-header regex returned the fixture lines); client-name regex returned `hpsm`/`nexusai` in q14 (positive); `kamilkreiser` found in 4+ files; path regex found `/volumes/laptop-dev` (present); IP regex found 127.0.0.1 (8079); email regex found fixtures.
- False zeros caught and redone: `\b` is not supported by this `git grep -E` (it returned a false empty for IPs and for `friday|wednesday`); I reran without `\b` and all results above are from the rerun. An early shell variable word-splitting error on the revs list produced "File name too long" and was discarded and rerun in python.
- Zero-result items and the control that shows the command shape works: `secuura|datasec|kintsugi|cypherkey|mypki|vision sales` (same command found hpsm/nexusai); `me.com|icloud|gmail|agentmail` addresses (same email regex found `git@github.com`); hash-assignment secrets (the secret-assignment regex found `Pa55w0rdXyz` pattern files in the same run); binaries (no `-` numstat rows; `numstat` shape works on text).

## Not checked
- GitHub-side data: Issues, PRs, wikis, releases, Actions logs, forks, deleted/dangling objects on GitHub (a public flip exposes anything reachable by hash, including unreferenced commits); repo description/topics.
- Local-only unreachable objects (`git fsck --lost-found`) in the clone; only reachable history was scanned.
- Binary-content search inside packed objects (grep used `-I` to skip binary blobs; numstat shows none).
- Dependency licence compatibility in `Cargo.lock` (cargo-deny was not run; `deny.toml` exists).
- Semantic review of the 3 spike `RESULT.md` files for statements that are embarrassing but contain no keyword.
- Anything in the owner's local FRIDAY repo not pushed to this remote.
