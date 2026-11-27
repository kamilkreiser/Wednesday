# QA-POLICY-B-R2, the short second check of the POLICY-B fix round (`cd7b6fd..8051c84`)

Drafted 2026-11-28 by Friday's brief drafter; the coordinator's rulings are in section 8. Nothing in this draft was run by the drafter: no cargo, no `ls-remote`, no harness, no timing. The drafter read with git read verbs only (`log`, `show`, `diff`, `grep`, `rev-parse`, `merge-base`, `ls-tree`, `cat-file`), in the project repository's own object store (`/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/2_Project_Files`; `git cat-file -t 8051c84…` = `commit`; the worktrees folder was not needed). Every expected answer, count and code line below is **the drafter's reading, unverified**; figures from the builder are **the builder's figure**; from the first verdict **the first check's figure**; every figure not measured by anybody is marked **unmeasured**.

## WHAT THE STATUS DOES NOT SAY
The drafter's own reading of `git diff cd7b6fd 8051c84` (numstat: `BACKLOG.md` 19 0, `Cargo.toml` 2 0, `red-controls.sh` 2 0, `src/action.rs` 15 3, `src/shell/mod.rs` 25 2, `tests/t29_free_text.rs` 253 9, `docs/POLICY.md` 2 2), set against the builder's STATUS lines 362-542 (read whole) and its section 8 (lines 341-347). Line numbers are at `8051c84` unless marked. Each point is a lead for the check to confirm or refute, not a finding.

- **W-1. STATUS section 8, which the coordinator reads to the owner, was not rewritten, and the STATUS says less than commit 1 did.** Addendum 5 ordered W-1 (d) (§8 (i) becomes the first check's sentence), W-2 (a) (§8 (iii)) and W-4 (§8 (v), (vi)). STATUS lines 342-347 still read "anywhere in the part the approval card can show … is now checked" (i), "Terminal commands: nothing changed … 2 × 17 260+ command rows" (iii), "the 23 kinds … the largest at 2 406 units" (v) and "about half a second … debug build" (vi). The fix-round section names neither the rewrite nor its absence: its commit 1 line (STATUS 412) and its "Fixed" line (534) say "W-1 c, W-2, W-5", and "NOT DONE" (530) does not list W-1 (d), W-2 (a) or W-4. Conversely, commit `a64c6ae` also carries W-1 (a) (`docs/POLICY.md:648`), W-1 (b) (the doc comment, `shell/mod.rs:476`) and W-6 (`docs/POLICY.md:931`), which the STATUS commit line does not name (the commit message does).
- **W-2. The short weight is not a web fetch change: it lowers the guard for scan B in every tool.** `piece_work` (`shell/mod.rs:416-425`) returns `SHORT_WORK` for any piece `is_short_word` accepts (`:438-440`), and it is called from `add_piece` (`:135`) for every scan B window of every call (URL windows, `Raw`/`Query` windows of `WebSearch`, `Agent`, `mcp__…`, untaught tools, a `Monitor` `ws.url`, the command-field carriers). Commands are untouched only because `Sink::command()` has `max_work: None` (`:117-124`, `:131-137`). So calls through other tools that `cd7b6fd` denied as too large may now be admitted. STATUS speaks of "a web fetch instruction", and the BACKLOG `[x]` entry does too. STATUS gives the builder's `cd7b6fd`→HEAD figures "L→base 4 048 / 4 213" (seed 1 / seed 2, STATUS 454, 469) without splitting them by tool or by row kind.
- **W-3. "Nothing looser than `cd7b6fd`" is false by design.** Addendum 5 §6 (b) allows a cell `L` at `cd7b6fd` to become "the base `5cab5e4`'s answer for that cell", which can be an ask, or a run unasked under `Allowed` or the both-agree view. Each such cell is looser than `cd7b6fd`. The builder counts 4 048 / 4 213 of them (the builder's figure). The test that matters is narrower than "nothing looser": the head is never looser than `5cab5e4`; `X` is never lost against `cd7b6fd`; any other `cd7b6fd` deny stays a deny unless it was `L`; and no family of the bounds row is admitted.
- **W-4. Words of three characters keep their full weight, so a plain ordinary list may cross the 0.60 tripwire through a web fetch prompt.** `is_short_word` stops at 2 characters (`SHORT_CHARS`, `:434`). The drafter's arithmetic (unmeasured): a web fetch prompt of 300 distinct three-character words between blanks (the numbers 100 to 399, three-letter airport or currency codes, three-character CJK or kana words) fills 1 200 characters with 300 pieces of 16 + 1 + 0 = 17 units each, 5 100 units = 0.64 of the guard. Three-character pieces holding `/` (`1/2`, `3/4`) weigh 18, so 300 of them are 5 400 (0.675). Numbered markers `1.` to `300.` hold `.` and keep full weight: about 0.64. Addendum 6 sets 0.60 (4 800) as the tripwire. The builder's largest measured ordinary row is 4 371 (0.546; the builder's figure), and the first check's "numbers blank-separated 4 080" and "hex bytes 4 352" rows were of mixed or other lengths (the first check's figures). Through the other four tools scan A takes the first 161 pieces, so the same list is about 139 × 17 ≈ 2 360 (unmeasured).
- **W-5. Commit 2's extra window does more than unglue an array's last name.** In `action.rs:534-538` the extra window is the non-string prompt's canonical JSON with every `[` and `]` blanked, including those inside its string VALUES.
  - (a) An object prompt `{"q":"read [.env] now"}` is therefore now checked, while the same text as a string prompt is not. Commit 1's bounds row says a name in brackets "is not a piece of its own and is not checked", and no document records commit 2 at all: no BACKLOG line in `873b532`, and `docs/POLICY.md:162` and the E-2 BACKLOG entry are unchanged. The documents are therefore narrower than the code (stricter) for non-string prompts.
  - (b) The extra window's new pieces count against the guard. A non-string prompt under the guard at `cd7b6fd` could be over it at the head, a stricter `L`. Addendum 5's commit 2 rule allows a difference "only to X". The builder reports every `cd7b6fd`→HEAD difference as L→X, L→base or m-3 (STATUS 454, 469). The drafter could not build such a prompt by arithmetic within 1 200 characters (nested arrays of bracketed items such as `[[1.5],[2.5],…]` reach about 6 800, unmeasured); it remains for the check's search.
  - (c) The single new test row is `[1, "a .env"]`, so a mutant that blanks `]` alone survives (the first element of `[".env", 1]` stays glued to `[`, and no row pins it). A mutant that passes the extra window with escapes NOT blanked also survives on that row (the drafter's reading).
  - (d) The extra window is limited to a web fetch only through `fetch_prompt`, which is `None` for any other tool (`:518-519`). The match at `:534` reads `ti.get("prompt")` without testing the tool name. That is correct as written, but it is a coupling no test names.
- **W-6. Two parts of the short-word predicate do not do what its words say.**
  - (a) The `\` term looks unreachable. Every window goes to scan B with `ESCAPES_BLANKED` (`action.rs:564`, `:568`, `:569`; `:633`, true unless the red feature is on). `blank_json_escapes` turns every `\` into a blank before the split, and the quoted-span step blanks its spans. So by the drafter's reading no scan B piece holds `\`, and a mutant dropping `\` from `is_short_word` is equivalent.
  - (b) The test counts the RAW piece's characters, before folding (`glob::fold_name`, NFKC). U+FF0E `．` folds to `.`. U+2100 `℀` folds to `a/c`. Arabic presentation ligatures and squared CJK (U+3300-33FF) fold to 3 or more characters, and U+FDFA to 18. Each of these still weighs 6 as a one- or two-character piece. Matching does not change: every piece is still pushed and checked. But the per-piece check may cost more than for the single CJK character behind the builder's structural figure. K1max (161 scan A + 1 024 scan B pieces, +77.9 ms release with the LONG list; the builder's figure, BACKLOG m-4 entry) was built of CJK characters only.
- **W-7. The new tests do not pin the predicate from both sides.**
  - (a) The unit test asserts `piece_work("一") == SHORT_WORK` (`shell/mod.rs:639-640`), so it follows the constant. `SHORT_WORK` moved is caught only by `short_word_list_is_admitted`'s literals (2 628 / 2 587 / 2 633 / 2 633 / 3 600, `t29:1254`).
  - (b) Those literals come from the test's own `b_scan` (`t29:138-152`), a rewiring of `classify` that omits commit 2's window and would panic on a non-string prompt (`input["prompt"].as_str().unwrap()`, `:148`). Its doc comment still says "as `classify` wires it".
  - (c) `SHORT_CHARS` 2 → 3 and `<=` → `<` are caught only by the unit test (`piece_work("abc")`, `piece_work("ab")`), not by any `t29` row.
  - (d) The builder's measurement shows that a wider predicate admits the brace-group family `x<i>{a,…,h}` (n = 8, STATUS 401). By the drafter's `git grep` of `t29`, no committed row pins that family `L L L L` (one `{a,b` hit, `:253`, a delimiter list). Criterion (ii), the fifteen families, rests on the builder's rows, not on a committed test (unverified: search `t28` and the other tests too).
- **W-8. The two commit 3 tests touch nothing of commit 4, and one of the new reds is a timing red.**
  - (a) `guard_boundary_is_exact` builds every piece with `/` "so that … none is a short dotless piece" (`t29:1181-1182`), so it pins nothing of commit 4.
  - (b) Under L3 (`MAX_FREE_WORK = u64::MAX`) the builder's red for `scan_b_cost_is_bounded` is the existing 100 ms TIME assert ("`T29-COST: deep option word took 1.246803666s`", STATUS 424). The new 120 s assert (`:986`, `:999-1004`) did not fire. L3's non-timing red is `guard_boundary_is_exact`'s 8 001 literal.
- **W-9. The committed W-3 figures are not the committed head's.** The BACKLOG line says "At the fix round's head … +18.2 / +5.2 / +46.4 ms … debug 66 cells (+120.9) … 97 (+317.2)". STATUS 429-432 says those were measured on the scratch tree `h4` before the commit. At the committed head, STATUS 520 gives +17.7 / +5.1 / +44.8 ms and debug 61 / 0 / 97 cells (+118.3 / +33.2 / +310.1), and calls them "within noise". In debug, 66 against 61 cells is outside the A/A noise the builder reports (unmeasured as a noise figure for debug cell counts).
- **W-10. The oracle-limit paragraph (STATUS 494-495) is narrower than the class it leaves out.**
  - (a) It says the uncovered class is a RELATIVE working folder, because "with an EMPTY folder the joined path starts with `/`" (STATUS 474). That is the builder's comparer's join. The engine's `lexical_only` (`action.rs:642-657`) does `cwd.join(raw)`, and `Path::new("").join("secret/plan.txt")` is the RELATIVE `secret/plan.txt` (the drafter's reading of std, unverified). Empty-folder rows therefore sit in the oracle's absolute branch and the engine's relative branch.
  - (b) The first check's own twin (`gate_policy_b_tests/zz_qpb.rs:309-320`, `as_intext`) is a copy of `lexical_only`, so it reproduces the engine's join and cannot see a join gap either.
  - (c) The first check's generated free text (C3, `zz_qpb.rs:749`) all ran with the working folder `<ws>`. Empty folders occur only in C2 (`cwd_pick`, 1 in 12, `:693-700`), and `rel` / `empty` only in hand rows (`:822-830`).
- **W-11. "Checked, not refused" is written without its bound.** The bounds row (`docs/POLICY.md:648`) and the appended line "The owner's ruling (2026-11-27): a web fetch instruction that is a long list of distinct short words is not refused as too large; it is checked" carry no limit. The limit is 1 024 scan B pieces per call: the builder's K1max refuses a web fetch at 594 prompt words beside 590 URL words (STATUS 406, the builder's figure). A prompt alone (at most 600 one-character words in 1 200 characters) stays under it. The sentence is therefore true of the prompt and wider for a call whose other window also holds such a list (a built shape).
- **W-12. Small.** The changed doc comment (`shell/mod.rs:476`, 174 characters) now reads "… then at the shell's punctuation. The window is split at blanks (and control characters) into words FIRST …", saying the split twice. The `MAX_FREE_WORK` comment (`action.rs:220-227`) says "every ordinary text is admitted" of a named corpus, without a ratio.

---

*(The brief proper starts here; the section above is the drafter's leads, which section 1 tells you to read.)*

This brief is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. You are a NEW seat, QA-POLICY-B-R2, on Opus: the SHORT second independent check of the branch `policy-b` (the policy crate `crates/coagent-policy`). The first check said NO GO for ONE Major, M-1: a web fetch instruction of 471 or more distinct one-character words between blanks was refused as too large. The builder did one fix round of five commits. You check ONLY that round, in one sitting. You did not make it. A merge to main rides on your verdict; this is the lane's SECOND and LAST check, so a NO GO goes to the owner. You have no mailbox. The project folder is READ-ONLY to you.

# QA-POLICY-B-R2: is the owner's ruling met (such a list checked, not refused), is nothing looser than the base, do the built shapes stay refused, can the new tests fail, and do the words say only what was measured?

The owner's ruling this round serves (his words on the board, 2026-11-27 16:40:41): "Fix it so such a list is not refused". In the repository's words (the appended BACKLOG line): "a web fetch instruction that is a long list of distinct short words is not refused as too large; it is checked." Call it "the owner's ruling". Never write a board or card id in your verdict.

## 0. First acts
1. Create the verdict file FIRST with the single line `IN PROGRESS`: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_POLICY_B_R2_verdict.md`. Write it section by section. At the end replace line 1 with exactly one of `VERDICT: GO`, `VERDICT: GO WITH NOTES`, `VERDICT: NO GO`, then a space, the long dash COPIED from line 1 of `gate_POLICY_B_verdict.md` beside it (do not retype it), a space and `head <full sha>`: the same form as that line.
2. Status file: `coagent/5_Project_History/STATUS_QA_POLICY_B_R2.md` (in `/Volumes/Laptop-DEV/!CODING/Claude to Claude/`); last line always `IN PROGRESS: <what>` or, at the end, `VERDICT WRITTEN: <the verdict's first line>`. Refresh it at least every 20 minutes. The only file you write in the project folder.
3. The head: `8051c844fdd9c2df5838b3da83dda1e783d93410`. It is FIVE commits whose parents run in a line from the first check's head `cd7b6fdd1a4b2de5937795b052a68d793146eb6d`: `a64c6ae` (words), `873b532` (m-3), `be1e309` (test rows), `9e49839` (row (d) respelled), `8051c84` (M-1). The lane's base is `5cab5e42df6cb3db05f3d38c7ba973beafd044b2`, the merge base of the head and main by the drafter's `git merge-base`. Main is `627431877d5fa3b86f91ec23d0dc2879c800eb33` by the builder's `ls-remote` (STATUS 537-539) and the local `origin/main`. **If main has moved, do not merge it and do not judge it.** Confirm both SHAs with `git ls-remote` against the GitHub remote; `git log --format='%H %P' cd7b6fd..8051c84` five lines, each parent the one before. The builder's STATUS (`coagent/5_Project_History/STATUS_POLICY_B.md`, 542 lines when this was written) must end `READY FOR QA POLICY-B r2` with `Head SHA: 8051c844fdd9c2df5838b3da83dda1e783d93410` in the line above it; if anything differs, write that and stop. The coordinator accepted the five commits in place of four (addendum 7, A-6 (a)).

## 1. Read WHOLE before anything else
- The first verdict `m1_review/gate_POLICY_B_verdict.md` (370 lines): BLUF (7-11), item 3 (80-107), item 4 (109-128), item 2's comparer and plants (130-201), item 7 (242-266), item 5 (268-290), the owner paragraphs (316-319), "Findings against the coordinator's rulings" (328-336), Findings (338-353) and "What was NOT checked" (355-369). Its harness folder `gate_policy_b_tests/` beside it (`zz_qpb.rs`, `cmp_qpb.py`, `adapter_base/`, `adapter_head/`, `time_drive.py`, `tab_time.py`, `mk_items.py`, `mk_sliding.py`, `plant.py`, `rows/`): copy and reuse what serves you. Its scripts have `W=/private/tmp/claude-501/qpb` written in (`build.sh:3`, `chain_*.sh`): change the path in YOUR copies, and never run anything from, or write into, that folder.
- The coordinator's orders for this round, in Friday's `briefs_drafts`: `2026-11-27_coagent_POLICY-B_ADDENDUM-5_fix_round.md` (204 lines; note the file `…_ADDENDUM-5_fix_round_DRAFT.md` beside it is a draft, NOT the order), `…_ADDENDUM-6_answer_Q7.md`, `…_ADDENDUM-7_answer_Q8.md`, `…_ADDENDUM-8_answer_Q9.md`. **The criteria as they stand** (addendum 6 §2, restating addendum 5 §3.4):
  - (i) Every ordinary text is admitted through five tools, with its late name `X X X X`. The largest B work is printed per tool, and a row over 0.60 of the guard (4 800 units) is a tripwire.
  - (ii) The fifteen families of the bounds row are `L L L L` through five tools.
  - (iii) Nothing is looser, by the two differentials, with the dotless short names of addendum 5 §3.3.
  - (iv) T-1 in RELEASE with three lists. For ordinary rows: no window more than 60 ms slower than at `5cab5e4`. For built shapes: no 60 ms line; the bound is structural, the piece counts.
  - Withdrawn by name: addendum 5's "B work at most 4 000" and its T-1 over every window; addendum 5's revert proof (addendum 6); addendum 7's control (a) (addendum 8); the comparer's by-name tail rule (addendum 8).
  - The coordinator's rulings are not yours to reopen as lane findings. Where you think one is wrong, write it in the section "Findings against the coordinator's rulings" (section 5) with evidence.
- The builder's STATUS from `## ADDENDUM 5 (fix round)` (line 362) to the end, WHOLE, and its section 8 (lines 341-347). Its statements are CLAIMS. Above all the heading "What the differential's oracle does not cover" (line 494).
- The whole diff `git diff cd7b6fd 8051c84`, every line. Above all `src/shell/mod.rs:412-440` (`piece_work`, `SHORT_CHARS`, `SHORT_WORK`, `is_short_word`), `:131-137` (`add_piece`, where work is counted), `:480-560` (`scan_free_text`), `src/action.rs:510-575` (the prompt windows, commit 2's extra window, scan B's call), `:642-657` (`lexical_only`), and `tests/t29_free_text.rs:130-160` and `:1076-1293`.
- The section above this brief, "WHAT THE STATUS DOES NOT SAY" (W-1 to W-12): the drafter's leads, to confirm or refute.

## 2. Where you work
Section 2 of the first check's brief (`2026-11-27_coagent_QA-POLICY-B_check_brief.md`) applies word for word, with these names: work dir `/private/tmp/claude-501/qpb2` (new). Use your own clone, GitHub remote and deploy-key fetch of `policy-b main` as written there, and your own EMPTY target dirs and cargo home, with the toolchain linked as `coagent_merge_check.sh` does. For EVERY cargo run set `CARGO_TARGET_DIR`, `RED_CONTROLS_LOG` and `COAGENT_TEST_TMP` to folders of your own under the work dir and quote them in STATUS. Network: `cargo fetch --locked` only. Never touch the builder's worktree, targets or scratch (`coagent/tools/tmp/pob/b3a4b7/`, `r2/` within it), nor the first check's work dir `/private/tmp/claude-501/qpb`. You may READ the builder's fix-round comparers and harness (`<scratch>/r2/dh/cmp_r2.py`, `cmp_r2_next.py`, `cmp_r2_final.py`, `scan_b_port_r2.py`, `zz_r2diff.rs`, `ctl_a_rows.jsonl`) to say what they did. Your differential, comparer, oracle and rows are your own (task C). **Heavy runs** as written there: before any run over five minutes `bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh` must print a number below 3 (no number = FULL: wait and look again every few minutes, say so in STATUS); one heavy run of yours at a time. Heavy here: a cold build of a tree (release or debug); each tree's run of your differential; a timing run of more than a few rows. Short: one `--test` target on a built tree, each mutant run of one target once its tree is built, your probe of one small row file, git read verbs, Python helpers. **Do NOT run** the whole red script, `scripts/check.sh`, the whole `cargo test -p coagent-policy --locked` or `cargo clippy` (Friday's merge check runs them; the builder's red-script run: 82 `RED OK`, 299 passed, STATUS 514). **NO model run and no Claude Code session of your own.** Copies of every script and test you write: `m1_review/gate_policy_b_r2_tests/`. Harness files never inside a tree whose whole suite you run. No deploy, push, merge, fix or edit in the project. Never `cd` in a shell command. In zsh write `"${SHA}:path"`. Python with `-B` (`-I` on recorded files). Never delete (move). No person's, machine's or account's name in the verdict; every secret- or address-shaped string you write is made up.

## 3. Scope, and NO GO only for a Blocker or Major
Only the round `cd7b6fd..8051c84`. Everything the first check confirmed at `cd7b6fd` stands unless the round's diff touches it. NO GO only for:
- **M-1 not closed.** The first check's M-1 list (650 code points U+4E00 on, between blanks) as a web fetch prompt is denied as too large at the head, or a listed name inside such a list (`.env`, or a dotless short name of task A) is not denied as excluded in all four columns.
- **Looser than the base.** Any cell where the head answers looser than `5cab5e4`.
- **A `cd7b6fd` difference outside the allowed classes.** The allowed classes are: `L` → `X`; `L` → the base's answer, where YOUR arithmetic puts the call under the guard; the m-3 array rows → `X`. In particular: an `X` lost, or any other deny lost.
- **A built family admitted.** Any family of the bounds row admitted through any of the five tools.
- **An ordinary text refused** that a person would write.
- **Commands changed.** Any `Bash`, `PowerShell` or `Monitor` command whose answer or scan differs from `cd7b6fd`.
- **Out of scope or protected.** Any byte of `src/engine.rs` or of another file outside the seven of the numstat above; a protected test file changed.
- **A test weakened.** A removed or weakened assertion, or a test that can no longer fail.
- **False words.** A sentence that says something false about the gate that the owner or a later lane would act on wrongly. A word merely loose or wider than its measurement is a Note or Minor by its effect.

## 4. What to check, in this order (TESTED = you ran it; READ = you read it)
**F. Scope (TESTED, first; short).**
- `git diff --name-only cd7b6fd 8051c84` gives exactly the seven paths, with a control range that differs elsewhere.
- Blob ids under `crates/coagent-policy/src` at both SHAs: only `action.rs` and `shell/mod.rs` differ (the drafter: 19 entries at `cd7b6fd`). `src/engine.rs`, root `Cargo.toml`, `Cargo.lock` and `rust-toolchain.toml` are blob-equal at `5cab5e4`, `cd7b6fd` and the head.
- The 17 protected test files: sha256 equal to the build brief's table at all three SHAs.
- `BACKLOG.md` at `cd7b6fd` is a byte prefix of the head's (the drafter: 0 removed lines in BACKLOG; `docs/POLICY.md` 2 changed lines, `:648` and `:931`).
- `MAX_FREE_PIECES` 1024 and `MAX_FREE_WORK` 8_000 are unchanged. The `Cargo.toml` and `red-controls.sh` lines are only the two new red features and rows.
- No test `fn` is gone: `--list` at both heads, 296 → 299 by the builder.
- The 36 pinned `t25` phrases are each found once at the head (by program).
- A byte scan of the round's added lines and five commit messages, with your own word list on the command line, a planted line and a planted binary as controls.

**A. M-1 closed (TESTED; the heart).**
- **The list.** Through all five tools of `t29::TOOLS` (`WebSearch`, `Agent`, `mcp__github__create_issue`, an untaught tool's raw input, a web fetch prompt), four columns, with the default list, `**/.env*` and the LONG list, at `5cab5e4`, `cd7b6fd` and the head, run the first check's M-1 row, its 470 control, and lists of 471, 500, 600 and 650 distinct one-character words. Also run two-character words (expected at most 400 in 1 200 characters; addendum 5 RULING 9), and mixed lists. Expected: admitted at the head, with your own work figure (`Σ` over B's pieces of 6 for a piece of at most two characters holding none of `.`, `/`, `\`, otherwise 16 + components + characters other than `/` and `\` divided by 8, written from the docs' bounds row, never by calling `piece_work`). By the drafter's reading the web fetch figure of the 650 list is 600 × 6 = 3 600, as the builder's literal says.
- **The listed name inside.** In each list, ` .env ` placed to end by character 1 000, and each dotless short name of addendum 5 §3.3, early and late: `x` with `**/x`, `hr` with the LONG list, `id_rsa` with the default list, `secret` with `<ws>/secret/**`, `．env` (U+FF0E) with `**/.env*`, `x` with `**/?`. Expected `X X X X` at the head. The opposite case: the same rows at `cd7b6fd` show `L L L L` for the web fetch lists, so a pass at the head is not a prompt left unread.
- **Boundary rows of your own.**
  - (a) Around the piece bound: a call with exactly 1 024 and 1 025 scan B pieces of short words. By the drafter's reading only a web fetch with lists in BOTH its URL and its prompt can get there (one 1 200-character window holds at most about 600 one-character words, and scan A takes 161 of a non-prompt window). Find the call shape with the most windows per tool (READ the arms in `action.rs` and the `free_text` collection at `:539-547`), and if no other shape reaches 1 025, say so with what you read. Expected: 1 024 admitted, 1 025 denied as too large; the builder's figure is K1max 590 + 593 admitted, 594 refused.
  - (b) Around 8 000 units with short and full-weight pieces mixed: rows at 8 000 and 8 001 by your own arithmetic. Expected: admitted, refused.
  - (c) A piece of exactly two characters, and of three, each without and with a `.` or `/`.
  - The opposite case for each: the row one unit or one piece inside the bound must be admitted. If both sides read the same, your row does not sit on the bound.

**B. The picked design against the four criteria as RESTATED (TESTED).**
- **(i) Ordinary text.** Re-run the first check's ordinary corpus (`rows_items.jsonl` `ord:*`, 49 kinds natural and filled, five tools) and the sliding corpus (`mk_sliding.py` over the head's tree, web fetch prompt and `WebSearch` at least) at the head. Report the largest B work per tool and its ratio. **Then W-4:** build lists of 300 distinct three-character words (the numbers 100 to 399; three-letter codes), three-character tokens with `/` (`1/2` …) and numbered markers (`1.` … `300.`), as a web fetch prompt and through the four other tools. The drafter's arithmetic (unmeasured): about 0.64 to 0.68 through a web fetch prompt. Any ordinary row over 0.60 is a finding; say whether it is ordinary, with the opposite case (the same list through `WebSearch` should be about half that, since scan A takes 161 pieces).
- **(ii) Built families.** The fifteen families of the bounds row are `L L L L` through five tools at the head. Add the brace-group family re-spelled with variants of exactly three characters (`x<i>{a,…,h}` with one-digit `i`) and with two-character variants (`{ab,cd,…}`): say which are refused. The builder chose n = 2 because n = 8 admitted the family; nothing pins n by a family row (W-7 (d)).
- **(iii) Nothing looser:** task C.
- **(iv) Time.** In RELEASE, interleaved base and head, smallest of five, with the A/A control on the same rows: re-measure ONE ordinary row (the M-1 650 list as a web fetch prompt, the LONG list; the builder's +44.8 ms at the head) and ONE built row (K1max, the LONG list; the builder's +76.9 ms). Add ONE row of your own for W-6 (b): K1max built from distinct characters that fold to three or more characters (squared CJK U+3300-33FF, Arabic presentation ligatures). If it costs more than K1max beyond your A/A noise, the "bounded by the piece counts" sentence (addendum 6 §2 (iv)(b), the BACKLOG m-4 entry) holds for the count but not for the time figure: say so. Do not re-make the builder's table.

**C. "Nothing looser", by YOUR comparer and differential, and the attack on what the builder's oracle no longer judges (TESTED).**
- **Harness.** Your harness is the first check's `zz_qpb.rs` (allowed), the SAME file compiled release at `5cab5e4`, `cd7b6fd` and the head, each in its own empty target dir, `cmp` silent between the copies, one fixture root of fixed length. Two changes:
  - Your head adapter must give scan B the windows `classify` gives it, commit 2's extra window included (otherwise "adapter B ≠ action B" fires on every non-string web fetch prompt, the drafter's reading).
  - Your comparer's work arithmetic gets the short weight from the docs' bounds row.
- **Never the builder's comparer.** Its oracle was corrected twice during the round and its by-name tail rule removed (STATUS 456-458, 470, 485-489).
- **Corpus (RULING 1 of section 8 sets its size).** The first check's C1 and item rows, the rows of tasks A and B, and the rows below.
- **Rules.**
  - Against `5cab5e4`: 0 looser, 0 command differences, the base's `InText` list a prefix of the head's.
  - Against `cd7b6fd`: every differing cell must be one of `L` → `X`, `L` → the base's answer with your arithmetic under the guard, or a non-string web fetch prompt → `X`. Count each class per tool and row kind (W-2, W-3), and list every `L` → non-deny row by kind.
  - **The `cd7b6fd` prefix invariant** (the drafter's reading: weights only move the stop point, and commit 2 appends a window at the end): `cd7b6fd`'s `InText` list is a prefix of the head's on every row. On every row admitted at both SHAs, the two lists are EQUAL except for non-string web fetch prompts. Any other row breaking this is a finding.
  - Search for a non-string prompt under the guard at `cd7b6fd` and over it at the head (W-5 (b)). If none exists, say so with the search.
- **The attack on the oracle's blind class (STATUS "What the differential's oracle does not cover").**
  - (1) **Relative AND empty working folders** (W-10). Your comparer must state how it joins a text word to a relative or empty folder. If that join is the engine's own (`lexical_only`, or the first check's copy `as_intext`), it cannot see a join gap: say so. Add an oracle that does not depend on the join: for one name and one working folder, an EARLY name (scan A's pieces) and a LATE name (scan B's, after 200 words) must answer the same, and the base's early answer must equal the head's late one.
    - Rows: `secret/plan.txt`, `secret`, `.env`, `~/.ssh/id_rsa`, `/etc/hosts`.
    - Working folders: `rel`, `""`, `/`, `<ws>`, `<ws>/src`.
    - Patterns: `<ws>/secret/**`, `~/.ssh/**`, `/etc/**`, `**/secret/**`, `**/.env*`.
    - Five tools; all three trees.
    - Report every cell where the three trees differ and every early/late pair that differs.
    - The opposite case: a row with the working folder `<ws>` and `<ws>/secret/**` must read `X` early and late, so your oracle is shown able to say "same and checked".
  - (2) **Names glued to zero-width or other ignorable characters** (the builder's 77 `OLD-GAP` cells per seed). Build the rows yourself: U+200B, U+200C, U+200D, U+2060, U+FEFF, U+00AD, U+202E glued before, after and on both sides of `.env`, `.ENV` and `secret/plan.txt`; early and late; five tools; three trees. Establish that every such cell is identical at `5cab5e4`, `cd7b6fd` and the head, and that the head is never looser. If a cell differs, it is not an "old gap".
  - (3) **Dotless short excluded names inside a long list of short words.** `x`, `hr` (LONG list), a two-letter name of your own on the list (`**/ab`), `id_rsa`, `secret`, each placed early, in the middle and late (ending by character 1 000) inside the 650 list, through five tools. The low weight must not let a listed short name through: expected `X X X X`. The opposite case: the same list without the name is admitted.
- **Planted loosenings, to show your comparer can fail** (each a tree at the head plus one plant, its own empty target dir, one seed or the targeted rows; each comparison must FAIL with its counts quoted; the unplanted head must PASS):
  - PL-a: short pieces not pushed as targets (D2 as a skip).
  - PL-b: `SHORT_WORK` = 0 together with `MAX_FREE_PIECES` raised to `usize::MAX` (a guard that never stops a short list).
  - PL-c: commit 2's window dropped.
  - PL-d: the first check's L-1 (scan A's `InText` targets not pushed).

**D. The new tests: can each fail, and is its red an honest guard (TESTED + READ).**
- `late_spellings_are_read` and `guard_boundary_is_exact` pass at `cd7b6fd` by design (addendum 7, A-6 (b), accepted). Their reds are the builder's by-hand mutants M3, M4, M5, M13, M14, M8, M7, M10 and L3 (STATUS 415-424).
- Re-make TWO of them yourself (the drafter suggests M13 on `9e49839`'s row `x'@.env'x`, and M7), each in its own tree and target dir, first panic quoted. Say for each row whether its red names its own fault or a neighbour's.
- Confirm or refute W-8: is L3's red in `scan_b_cost_is_bounded` the timing assert, and is `guard_boundary_is_exact`'s 8 001 literal a non-timing red for L3?
- Then one mutant per new branch of commits 2 and 4 (RULING 2 of section 8: five built, the rest READ), each in its own tree, its own target dir, targets `t29_free_text` and the unit tests (`shell::tests`). The drafter's expectations, unverified:

| mutant | expected |
|---|---|
| `SHORT_WORK` 6 → 0 (the constant) | the unit test green (it follows the constant); `short_word_list_is_admitted` red on its literal |
| `SHORT_CHARS` 2 → 3 | unit test `piece_work("abc")` red; no `t29` row red |
| `<=` → `<` | unit `piece_work("ab")` red only |
| `.` dropped from the predicate | unit `piece_work(".e")` red |
| `/` dropped | `guard_boundary_is_exact` red, if its `/a`, `/t` suffix pieces are two characters (unverified) |
| `\` dropped | equivalent (W-6 (a)): show it by reading, or find a scan B piece holding `\` |
| `chars().count()` → `len()` | `short_word_list_is_admitted` red |
| commit 2 blanking `]` only | survives (W-5 (c)) |
| commit 2 blanking `[` only | the `T29-FETCH` array row red |
| commit 2's window with escapes not blanked | survives |
| commit 2's window before the canonical one | no test red; your prefix invariant of task C must catch it |

  A survivor on a branch the owner's ruling or addendum 5 names as pinned is a finding; on another branch, a Note naming the missing row.

**E. m-1 to m-4 and the words (READ + TESTED against your rows).** Check each changed sentence of commit 1 and commit 4 against what the code does: `docs/POLICY.md:648` (both of its changes), `:931`, the doc comments `shell/mod.rs:476` and `action.rs:220-227`, `SHORT_CHARS`'s comment (`shell/mod.rs:429-433`), and the five appended BACKLOG lines and entries.
- **m-1 ("every piece").** Is the new list of unsplit spellings true by your task C (2) rows and the first check's item 4 table? Is it now WIDER than the code for brackets in a non-string web fetch prompt (W-5 (a))?
- **m-2 ("terminal commands: nothing changed").** The BACKLOG correction is true by your command rows. STATUS §8 (iii) still says it (W-1): say so, since that is the line the coordinator tells the owner.
- **m-3.** No document records it (W-5 (a)).
- **m-4.** Is the W-3 line's "At the fix round's head" true of its figures (W-9)?
- **The bounds sentences.** "Checked, not refused" without the 1 024-piece bound (W-11). "None of `.`, `/`, `\`" with a dead `\` (W-6 (a)). "Every ordinary text … admitted, the largest at 4 371" against your task B (i) rows.

**G. The two sections the owner and the coordinator read (written in the verdict, from tasks A to E).**
- **"For the owner, in plain words".** What is now admitted (the long lists of short words, through which tools, with the commonest example). What is still refused (the built shapes; a call over 1 024 short pieces; text after 1 200 characters). What it costs in time in the build he runs (your release figures). Facts about the product, not his choice.
- **"Findings against the coordinator's own rulings (addenda 5 to 8)"**, apart from the lane's findings. Candidates for you to test, not findings:
  - the 0.60 tripwire against three-character lists (W-4);
  - addendum 5's commit 2 differential rule "only to X" against a stricter `L` (W-5 (b));
  - addendum 6 §2 (iv)(b)'s structural bound measured on CJK only (W-6 (b));
  - addendum 7 A-2's `OLD-GAP` exemption;
  - addendum 8's removal of the tail rule and its oracle limit, against relative AND empty folders (W-10);
  - addendum 5's W-1 (d) / W-2 (a) / W-4, whose STATUS rewrites were not made (W-1);
  - addendum 5's commit 2 asking for no words.
  
  **A Major there goes FIRST in the BLUF.**

**H. Not in this check.** The whole suite, `cargo clippy`, `scripts/check.sh` and the red script: the coordinator's merge check runs them. Say so under "What was NOT checked", with the builder's figures marked as the builder's (82 `RED OK`, 299 passed, clippy exit 0; STATUS 514, 524-525).

### Every evidence: what it reads in the opposite case
| evidence | fix works | fix absent (opposite) | another fault that reads the same, and how you tell them apart |
|---|---|---|---|
| M-1 list admitted | `a2 U U B`, your work ≤ 8 000 | `L L L L` | the prompt not read at all also reads admitted: told apart by the same list with `.env` and with a dotless name late (`X X X X`) |
| your work = the code's | equal on every row | differs | your arithmetic and the code sharing a fault: yours is written from the docs' definition, never from `piece_work` |
| families `L L L L` | refused | admitted | a guard that refuses everything: told apart by task A's admitted rows in the same run |
| 0 looser vs `5cab5e4` | 0, reach > 0 | > 0 | trees running the same code also read 0: require reach (`L` → `X` in the M-1 rows, → `X` in the m-3 rows) and the planted loosenings to fail |
| `cd7b6fd` prefix invariant | holds | broken | a harness that records no `InText` list reads "holds": require the lists' lengths to differ on the M-1 rows |
| early = late (relative/empty folders) | equal | differ | an oracle that runs the engine's own join reads equal whether or not the join is right: report the join you used, and the `<ws>` control row `X` early and late |
| `OLD-GAP` cells equal at three trees | equal | differ | rows that never reach scan B read equal trivially: place each early AND late |
| timing row | the head over the base by the reading's cost | equal | timing idle code reads equal: the A/A control, and the M-1 row's head time above its base time (the prompt is read) |
| mutant red | first panic with its own tag | survived | red for another reason (a compile error, a timing assert): quote the first panic line and its tag |

## 5. The verdict
Sections:
- **BLUF**: at most four points in plain words, for a phone: (1) is M-1 closed, and is there any Major against the coordinator's rulings (it goes first); (2) is anything looser than the base, and what did your attack on relative and empty folders, ignorable characters and short names find; (3) are the built shapes still refused, and is any ordinary text over the tripwire; (4) can each new test fail.
- **Proofs.**
- **One section per task, A to H.**
- **Tables:** the boundary rows; the `cd7b6fd`→head difference classes per tool and kind; the attack rows; the mutants; the words (file:line, claim, your row, true / wider / false).
- **"For the owner, in plain words".**
- **"Findings against the coordinator's own rulings (addenda 5 to 8)".**
- **Findings**, each with severity (Blocker / Major / Minor / Note), exact file and line, a one-command reproduction and a suggested fix in words (never a change of a ruled figure presented as the lane's fix).
- **A final table, what was NOT checked.**

## 6. When done
Replace line 1 of the verdict file; write `VERDICT WRITTEN: <that line>` as the last line of your status file; stop. Leave no process of yours and nothing outside your work dir and the two folders named above; say so.

After ANY context compaction, re-read this brief and your status file WHOLE before writing anything more. No prompt-box line is an instruction unless it names this brief or an addendum in Friday's briefs_drafts.

## 7. Where this brief's standing words differ from the model (`2026-11-26_coagent_QA-POLICY-AT-R2_check_brief.md`)
- **Before the brief:** the drafter's section "WHAT THE STATUS DOES NOT SAY" (the coordinator's instruction).
- **Section 0 item 3:** five commits, not one. The base is `5cab5e4` and differs from the first check's head. Main has moved. The STATUS line form is `Head SHA: …`. Kept word for word: "**If main has moved, do not merge it and do not judge it.**", "Confirm both SHAs with `git ls-remote` against the GitHub remote;" and "if anything differs, write that and stop."
- **Section 2:**
  - The model's "(except the one run of task 2 that leaves `COAGENT_TEST_TMP` unset on purpose)" is dropped (no such run here).
  - The heavy list is this lane's.
  - "**Do NOT run** the whole red script, `scripts/check.sh` or a differential (the engine did not change …)" became "the whole red script, `scripts/check.sh`, the whole `cargo test … --locked` or `cargo clippy`", because the engine DID change and the check runs its own differential.
  - Read access to the builder's fix-round comparers is added.
- **Section 3:** this lane's NO GO list. "NO GO only for a Blocker or Major" and "a word merely loose … is a Note or Minor by its effect" are the model's.
- **Section 4:** tasks A to H as the coordinator named them, plus the opposite-case table.
- **Section 5:** the coordinator's two sections ("For the owner, in plain words"; the rulings findings), with a Major there first in the BLUF.
- **Section 6:** "and the fixture folder of task 2 (b)" is dropped (no such folder here).

## GATING RULES COPIED
Word for word from the model `2026-11-26_coagent_QA-POLICY-AT-R2_check_brief.md`, with only names, heads and file names changed (`QA-POLICY-AT-R2` → `QA-POLICY-B-R2`, `gate_POLICY_AT_r2_verdict.md` → `gate_POLICY_B_R2_verdict.md`, `gate_POLICY_AT_verdict.md` → `gate_POLICY_B_verdict.md`, `STATUS_QA_POLICY_AT_R2.md` → `STATUS_QA_POLICY_B_R2.md`, `qpa2` → `qpb2`, `qpa` → `qpb`, `policy-at` → `policy-b`, `pat/0a8cdc/` → `pob/b3a4b7/`, `gate_policy_at_r2_tests/` → `gate_policy_b_r2_tests/`):
- **Model line 6** (the verdict's first-line rule: `IN PROGRESS` first, the three verdict lines, the dash copied, `head <full sha>`): section 0 item 1, whole.
- **Model line 7** (the STATUS heartbeat: last line, refresh every 20 minutes, the only file written in the project folder): section 0 item 2, whole.
- **Model line 8** (main moved: not merged, not judged; `ls-remote`; write and stop): three sentences of section 0 item 3, as listed in section 7.
- **Model line 19** (own folders; heavy-run counter rule; no model run; copies of scripts; harness outside a whole-suite tree; no deploy, push, merge, fix or edit; never `cd`; zsh form; Python flags; never delete, move instead; names and redaction): section 2. Word for word except the three changes named in section 7.
- **Model lines 21-22** (NO GO only for a Blocker or Major; "a word merely loose …"): section 3, heading and last sentence.
- **Model line 46** (when done; nothing outside your own folders): section 6, first paragraph, with the fixture-folder clause dropped (section 7).
- **Model line 48** (compaction re-read; prompt-box lines): section 6, second paragraph, whole.

## 8. RULINGS (the coordinator's, on the drafter's six open points; nothing in this brief was run by the coordinator or the drafter)
1. **Size of your differential (task C):** the targeted rows (the first check's C1 and item rows, the rows of tasks A to C) plus ONE seed of the generated C2/C3 at a fifth, at three trees, release. Durations unmeasured. If time is short, the targeted rows and the attack rows of task C (1) to (3) come first and the generated fifth last; say what was cut.
2. **Mutants (task D):** the two re-made builder's reds plus FIVE built mutants: `SHORT_WORK` to 0, `SHORT_CHARS` to 3, `/` dropped from the predicate, commit 2 blanking `[` only, commit 2 blanking `]` only. The other rows of the table are READ and marked so.
3. **An ordinary text over the 0.60 tripwire (W-4):** not a lane finding by severity of yours. The 0.60 line is the coordinator's own margin (addendum 6), unmeasured when it was set. Report every such row in "Findings against the coordinator's own rulings" with its ratio, whether a person would write it, and how far it is from a refusal (the units left to 8 000). An ordinary text that is REFUSED stays a NO GO reason (section 3).
4. **The `cd7b6fd` to head rule (W-3):** addendum 5 section 6 (b)'s allowed classes are the measure, as section 3 and task C state them. Every `L` to non-deny row is listed by tool and kind. "Nothing looser than `cd7b6fd`" is not required literally: the owner's ruling makes such a list admitted.
5. **STATUS section 8 not rewritten (W-1):** you report it as a Note against addendum 5. The coordinator writes the landing sentences for the owner herself, from the first verdict and yours; so your "For the owner, in plain words" section must be complete by itself and must not lean on the builder's section 8.
6. **Built trees:** three new cold builds in your own work dir; nothing copied from the first check's targets.

## WHAT THE DRAFTER COULD NOT CHECK
- Nothing was run.
- Not read whole: the rest of `t29_free_text.rs` at the head (only `:86-160`, `:870-1050` in part and `:1076-1293`), `src/engine.rs`, `glob::fold_name`, `hash::canonical_json`, `path::lexical_clean`, the first check's `cmp_qpb.py` and `zz_qpb.rs` (only the lines cited), the builder's fix-round comparers and harness, and STATUS lines 1-361 beyond section 8.
- Not established:
  - whether `Path::new("").join(…)` is relative in this toolchain (W-10, read from std's documented behaviour);
  - whether any `t28` or other test pins the brace family (W-7 (d));
  - the window count per tool (task A (a));
  - every arithmetic figure in W-4, W-5 (b) and W-6 (b), all unmeasured.
