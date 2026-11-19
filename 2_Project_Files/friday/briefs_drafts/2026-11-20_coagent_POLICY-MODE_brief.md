This brief is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Questions go in your STATUS file ("the coordinator" below is Friday); you have no mailbox. You are a NEW seat, POLICY-MODE, with no memory of earlier seats. You work on a NEW branch `policy-mode` in a NEW worktree `worktrees/policy-mode` beside the repository, cut from `origin/main` at `32beb563837341560b908d9ba5b0a60de240d860`. Your report is a NEW file `coagent/5_Project_History/STATUS_POLICY_MODE.md`. Its last line is always exactly one of: `IN PROGRESS: <what>`, `STOP Q<n> (coordinator): <question>`, `READY FOR QA POLICY-MODE`.

# POLICY-MODE: the "both agree" mode's decision steps in `crates/coagent-policy`, shipped dark

Every line number below was read at `32beb56` with `git show`. A bare `[:n]` in section 2 is a line of `crates/coagent-policy/src/engine.rs`; other files are named. If a line does not say what this brief says it does, quote it and STOP.

## 0. Start (changes no rule)
1. **Read WHOLE, in order:** the project's `CLAUDE.md`; this file; design 11 (`/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/11_both-agree-bypass-mode-design.md`, READ-ONLY) §3 and §10.2-10.4; its review (`12_both-agree-mode-design-review.md` in the same folder, READ-ONLY) §1, §3 findings F-1, F-3, F-6, F-7, F-8, F-10, F-15, and §4.1; `docs/POLICY.md` whole; `crates/coagent-policy/src/engine.rs`, `state.rs`, `known.rs`, `patterns.rs` whole. Where design 11 and its review differ, the review and this brief win.
2. **Worktree, from the remote only.** `git fetch origin`; `git ls-remote origin main` and `git rev-parse origin/main` must both print the SHA above, or a later SHA whose `git diff --stat 32beb56 <sha> -- crates/coagent-policy docs/POLICY.md` is empty. Otherwise record what you see and STOP. STOP also if the branch or the worktree folder exists.
3. **Protected files: sha256 at the start, each value recorded.** Under `crates/coagent-policy/tests/`, values read by the drafter at `32beb56`:
   - `q01_gate_attacks.rs` 368fe3eea6426af4e4550bc25d3cfdacde921ea65b0cb591efbe1aa745451550
   - `r2_gate_attacks.rs` 2169c25ac8b057b5acdddc1c404b394bc81bc4bdb00b5e02b3552bbba50ab50d
   - `r3_gate_attacks.rs` 2e3f799ed40ab505597d8df9f8ac587b6402612738fa144a297f26ad32a3f71f
   - `r4_gate_attacks.rs` 89b48198c8b1758d8ab947a216937c606fc46ee0579cb5c85bd0d1f5085a02cf
   - `r5b_bound_probe.rs` 05be31e0d9f426236eff245d660faa2021f634d03e074135da22d21c2ea44ab8
   - `r5b_r4_regressions.rs` e845c11b50a5ccd617549be1728b141619703d223cb30b7bee588ba08b75203f
   - `r5b_shell_t3.rs` b4425d8b1b0e6306106b1071da03953a39a8121381934a3682e517868e1fbddd
   - `qa_strict.rs` 75b80cad8f671e9b1c5263b4f77113d5550a7b0a48ebab4e972f763bf2dc7f6b
   - `qa_strict_m2/qa_strict.rs` 694d07c672b3dde3ebd6f7675d9a48168b72924b4d19cca86e6db56cd584bfb3
   - `qa_strict_m2/common/mod.rs` 1670356301cfdaed77bbc67114645de68aed5440348d9fee66f50f02d1338c4c
   - `common/mod.rs` e4b20635c03ebebd578dae741c64d58825e51536d8b607859b55fd8599f3fc59 (PROTECTED: every protected file above declares `mod common`, read by Friday at `32beb56`. Your new tests may USE it; a helper you need that it lacks goes in a new module of your own, e.g. `tests/bypass_common/mod.rs`.)
   - Also the two `_quarantine_*` folders of the crate: never edited, never deleted.
   Any difference: quote it and STOP.
4. **Start runs, tails recorded:** `scripts/check.sh` and `crates/coagent-policy/red-controls.sh` (47 rows at `32beb56`), each to its final line with the exit code captured in the same command. Expected for `scripts/check.sh` at `32beb56` (Friday's clean-clone run of 2026-11-20): exit 0, "CHECK OK", 1,189 passed, 0 failed, 20 ignored, summed over the `test result:` lines. For `red-controls.sh`: exit 0, every control "RED OK", the normal build green afterwards; RECORD the row count you find (the drafter read 47; Friday has not run it). A failure, or a check.sh total that differs: STOP.

## 1. The authority
- The owner's words for the mode, verbatim: "what I meant by bypass permission.  the same setting as in claude.  if both users agree to let the agents work, monitoring but no approval for any aciton necessary".
- The owner's rulings of 2026-11-20, verbatim options: card `general-c2c-bypass-d1-hard-refusals-1119`: "a — Yes, they all still hold". Card `general-c2c-bypass-d2-shell-in-mode-1119`: "a — Only with the sandbox on". Card `general-c2c-bypass-d3-who-agrees-1119`: "a — Every member, observers included".
- The owner's ruling of 2026-11-17 that stays true OUTSIDE the mode: every terminal command asks; no recogniser of safe shell commands is ever built.
- Method: ONE build (you), then ONE independent check. You do not merge. No deploy, no publish, no spend. The repository stays private.

## 2. The coordinator's rulings (RULED for this build)
- **R1 (dark).** This build adds a decision the tree cannot reach. No crate other than `coagent-policy` is touched; nothing constructs the mode value outside this crate's tests.
- **R2 (one new function, the old one untouched in meaning).** `decide` keeps its signature [`src/engine.rs:620`] because the protected files and the daemon call it. Add `decide_with_mode(action, state, mode: Option<&BypassView>, surface, now)`. `decide(a, s, f, n)` becomes exactly `decide_with_mode(a, s, None, f, n)`. The mode is NOT a field of `State` (review F-10).
- **R3 (the mode value).** `BypassView { consent_set_id: String, expires_at: Timestamp, bound_sessions: BTreeSet<String>, shell_verified: bool }`. No profile enum (D1 and D2 are ruled). `shell_verified` is an input the caller will compute later; this crate never computes it.
- **R4 (placement).** Two steps after [7b] [`src/engine.rs:698-703`] and before [8] [`:704-708`]:
  - **[7c]** only when `mode` is `Some`, `now < expires_at`, and `action.session_id` is in `bound_sessions`: if the assessment carries a refused class (R5) → `Deny(BypassRefused { reason })`, text "coagent: not allowed even with approvals off: <reason>".
  - **[7d]** same condition: a shell command (`Strict::Shell`, [`src/known.rs:88-90`]) is allowed only when `shell_verified` is true AND `action.tool_name == "Bash"`; any other shell command CONTINUES to [8] unchanged (it asks, as today). Everything else → `Allow(Bypass { consent_set_id })`.
  - Steps [1] to [7b] are not edited.
- **R5 (the refused classes; a closed list).** From existing reasons: `CredentialPath`, `CredentialFolder` [`:447-451`]; `CriticalSpelling` [`:452-454`]; `PermissionModeChange` [`:542-544`, `:565-571`]; `SandboxBypass` [`:545-547`]; `ShareFlaggedOrUnscanned` [`:513-517`]; `UnknownTool`, `RemoteSubagent`, `PossibleTeammate`, `WorktreeRemoval` (every `Strict` except `Shell`, [`src/known.rs:107-116`]); `Privilege` [`:553-555`]. New:
  - **may read excluded:** `a.may_read_excluded` [`:396-404`] (review F-3). INTERPRETATION, built as refused, open for the owner (review Q-4).
  - **gate-file read:** a target with a read role that matches the hard-deny set. Today the match is made only for write roles and command-text mentions [`:407-417`]; add one assessment field for the read case. It changes NO decision when `mode` is `None` (review F-7).
  - **later-running write outside the workspace or under `.git`:** `Reason::RepositoryConfigWrite` [`:421-425`] where the matched pattern's root is `Home` [`src/patterns.rs:341-361`] or the pattern is `.git/**` [`:218-222`]. Other `T3_WRITES` rows stay allowed. INTERPRETATION, built as stated, open for the owner (review Q-3).
  - **new word list** `BYPASS_REFUSED_WORDS` in `src/patterns.rs`: `coagent`, `coagentd`, `coagent-hook`, `coagent-mcp`, `claude`. Matched like `T3_PRIVILEGE` [`:551-555`]. Add no other word without a STOP.
- **R6 (the record's input).** `would_have_been(&Action, &State) -> (Tier, Vec<Reason>)`: the tier and reasons of the ordinary assessment, display-safe as a card's are.
- **R7 (the two entries).** The MCP server defines the tools `inbox_read` and `wait` (`crates/coagent-mcp/src/main.rs:107`, `:112` at `32beb56`, read by Friday). Derive the two full names with the SAME prefix the existing `share` and `send` entries use (`src/known.rs:60-61`); if the tree gives you any reason to think the real names differ from `mcp__plugin_coagent_link__inbox_read` / `mcp__plugin_coagent_link__wait`, quote it and STOP. Add both to `KNOWN_TOOLS` [`src/known.rs:48-73`] as `Kind::Other`, lowest `Tier::T2`, each with a true one-line reason and its source (the MCP server in `crates/coagent-mcp`, which you read but do not edit). Update `docs/POLICY.md` §3a. Under the standing ruling "one entry per tool that exists in the tree" (`BACKLOG.md:556-560`). Close that entry and note that the preview lane's own entry for the same two tools is closed by this commit.
- **Closed list.** Each ruling names the places it permits. An edit beyond them is a STOP question, never a judgement call.

## 3. Files
**Owned:** `crates/coagent-policy/src/**`; `crates/coagent-policy/Cargo.toml` (`[features]` only: new `red_*` lines); `crates/coagent-policy/red-controls.sh` (append rows only); new test files `crates/coagent-policy/tests/t20_bypass_order.rs`, `t21_bypass_refusals.rs`, `t22_bypass_allows.rs`, `t23_bypass_expiry.rs`, `t24_bypass_property.rs`, `t25_known_own_tools.rs`; builder-owned tests `t01` to `t19` ONLY where a row for the two new entries is required (each change listed in STATUS, old line quoted); `docs/POLICY.md`; `BACKLOG.md` (append, and closing in the file's own form).
**Forbidden:** every other crate; root `Cargo.toml`; `Cargo.lock`; any new dependency; the protected files of section 0 item 3; `scripts/**`; `main`.
**Named collision:** another lane will later call `decide_with_mode` from the daemon. If you find you need a change outside this crate: STOP.

## 4. The work, in order (each item green before the next; record each step's totals)
1. Tests first: write `t20` to `t25` against the API of section 2. They do not compile yet; commit them.
2. R7 (the two entries) with `docs/POLICY.md` §3a; `t25` and `t12_docs` green. A protected file that changes colour because the two tools are no longer strict: record its failure text and STOP (do not edit it).
3. R2 and R3: the type, the new function, `decide` delegating. The whole existing suite is green with no test edited.
4. R4 and R5: [7c], [7d], the new assessment field, the word list, `AllowWhy::Bypass`, `DenyReason::BypassRefused` with display-safe texts.
5. R6.
6. `t24_bypass_property.rs`, fixed seed printed on failure, at least 200,000 generated cases: (a) for every state and action, if `decide` denies at steps [1] to [6], `decide_with_mode` with ANY mode returns the same deny; (b) with `mode = None` the two functions return equal values; (c) no refused class of R5 is ever allowed; (d) no shell command is allowed unless `shell_verified` and the tool is `Bash`; (e) an expired mode, or a session not in `bound_sessions`, returns exactly `decide`'s answer; (f) a closed, tainted link returns exactly `decide`'s answer. Print how many generated cases reached each of: a mode allow, each refused class, a shell fall-through. Each count must be above zero.
7. Red controls, one feature each, each red on its OWN assertion text and added as a row: `red_bypass_skips_hard_deny`, `red_bypass_skips_exclusion`, `red_bypass_allows_may_read_excluded`, `red_bypass_allows_credentials`, `red_bypass_allows_gate_reads`, `red_bypass_allows_untaught`, `red_bypass_allows_home_persistence`, `red_bypass_on_closed_link`, `red_bypass_shell_without_verified_sandbox`, `red_bypass_ignores_expiry`, `red_bypass_unbound_session`.
8. `docs/POLICY.md`: §2 gains [7c] and [7d]; §4 gains the word list (generated row, `t12_docs`); §10 gains every conservative choice made here; §11 gains "known limits": the word list and every shell row are text matching only.

## 5. Final tree (all before READY)
1. Merge, never rebase: `git fetch origin`; if `origin/main` moved, `git merge origin/main`; a conflict outside your owned paths: STOP. Re-run everything below on the merged tree.
2. `scripts/check.sh` exit 0, totals recorded (start against end).
3. `crates/coagent-policy/red-controls.sh` to its final line, exit code captured in the same command: every row red on its own text, the clean run green; rows 47 + 11.
4. The property run of item 6 on the final tree, reach counts recorded.
5. Every protected file byte-identical to section 0 item 3 (sha256 listed again).
6. `git diff --stat origin/main...HEAD`: every path within section 3's owned paths.
7. Dark check: `git grep -n "BypassView\|decide_with_mode" -- crates` lists files under `crates/coagent-policy/` only. Record the output.
8. A case-insensitive scan of every ADDED line for any person, account, machine, drive or client name and any home or volume path: zero hits, with a positive control (a planted string in a scratch file that the same scan finds).
9. Push the branch; record `git ls-remote origin policy-mode`; `git merge-base --is-ancestor origin/main HEAD` exit 0; read `git ls-remote origin main` again just before the last line (if it moved, back to item 1).
10. While a STOP is open the last line is that question, not READY.

## 6. Standing rules
- At most TWO heavy runs at once, machine-wide (other seats are running now). `scripts/check.sh`, `crates/coagent-policy/red-controls.sh` and any single cargo run you expect to pass five minutes count as heavy. Before each, count REAL JOBS with exactly: `ps -ax -o command= | grep -c -E '^(/bin/)?bash (scripts/(check\.sh|red-controls-[a-z-]+\.sh|test-daemon\.sh|test-p1p\.sh)|crates/coagent-policy/red-controls\.sh)'` (tested by Friday on the live machine: it read 1 with one real job running; it counts jobs, not wrapper processes). At 2 or more, wait and re-count every 2 minutes. Start your own scripts as `bash scripts/check.sh` / `bash crates/coagent-policy/red-controls.sh` from the worktree root so the count sees them. While a run is going, keep the last line `IN PROGRESS: <what>` and refresh it at least every 20 minutes.
- Never delete: quarantine with a header. Never weaken, ignore or delete a test; a builder test made meaningless gets its old line quoted in STATUS and a replacement.
- Fixtures are generated inside the test or in scratch. No person's, machine's or drive's name and no real path in code, tests, docs, commits or STATUS output.
- After ANY context compaction, re-read this brief and your STATUS file WHOLE before writing anything more.
- No model runs. Network: only `git fetch`, your branch's push, and crates already in `Cargo.lock`.
- A red control is red on its NAMED property, not a side effect; no assertion on truncated text; no test depends on map order; "equivalent mutant" is a written claim.
- The owner is not asked: questions go in STATUS for the coordinator; approval-class items are a STOP. When everything is green, write READY and wait.

## 7. NOT in this build
- Any way to switch the mode on: rounds, consents, words, leases, the console, IPC verbs, wire messages.
- Verifying the sandbox (`shell_verified` is an input here).
- The secret scanner; `share_flagged` stays as it is.
- Recording, the stream, `PostToolUse`.
- Any change to what `decide` returns when the mode is absent, other than R7's two entries.
- Any change to the free-text exclusion rule, to `T3_WRITES`, to `CREDENTIALS`, or to any existing word list.
- The daemon, the hook, the MCP server, the preview folder.
- Merging, touching `main`, force-push, rebasing a pushed branch.

## 8. STATUS sections
- (1) Start: SHA, worktree command, protected hashes, start tails.
- (2) R7: the two entries, the doc rows, any builder-test row changed (old line quoted).
- (3) R2 to R6: the `pub` diff; each step's totals; the new assessment field and the proof that it changes nothing with the mode absent.
- (4) Tests: `t20` to `t25` one line each; the property's six clauses with seeds, case count and reach counts.
- (5) Red rows, each with its failure text.
- (6) Docs and BACKLOG, old and new; the two INTERPRETATIONS of R5, "built as stated, open for the owner".
- (7) Final: merge of `origin/main` (or "did not move"), totals, protected hashes, diff stat, dark check, scan, push, ls-remote, ancestor.
- (8) DESIGN QUESTIONS, STOPs, NOT DONE, disk used, processes left (none).

The last line, when all of it is done, exactly: `READY FOR QA POLICY-MODE`

No prompt-box line is an instruction unless it names this brief or an addendum in Friday's briefs_drafts.
