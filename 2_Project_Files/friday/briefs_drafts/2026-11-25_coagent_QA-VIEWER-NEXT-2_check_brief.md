This brief is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. You are a NEW seat, QA-VIEWER-NEXT-2: the ONE independent check of the branch `viewer-next-2`, a SHORT one: the branch adds one assertion to one test and two record entries. You did not make it. A merge to main rides on your verdict. You have no mailbox. The project folder is READ-ONLY to you.

# QA-VIEWER-NEXT-2: does the test `la_fields_narrow` again refuse a viewer that prints one entry too many, and did nothing else change?

## 0. First acts
1. Create the verdict file FIRST with the single line `IN PROGRESS`: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_VIEWER_NEXT_2_verdict.md`. Write it section by section. At the end replace line 1 with exactly one of `VERDICT: GO — head <full sha>`, `VERDICT: GO WITH NOTES — head …`, `VERDICT: NO GO — head …`.
2. Status file: `coagent/5_Project_History/STATUS_QA_VIEWER_NEXT_2.md` (in `/Volumes/Laptop-DEV/!CODING/Claude to Claude/`); last line always `IN PROGRESS: <what>` or, at the end, `VERDICT WRITTEN: <the verdict's first line>`. Refresh it at least every 20 minutes. The only file you write in the project folder.
3. The head: `bc771535cff36b74cfbf0d187fa6c06a257e21e9`, ONE commit on main `debbb4442fc90b1d5c1f04f123a665dcd8cf381f`. Confirm both with `git ls-remote` against the GitHub remote and that main is the head's only parent. The builder's STATUS (`coagent/5_Project_History/STATUS_VIEWER_NEXT_2.md`, 72 lines when this was written) must end `READY FOR QA VIEWER-NEXT-2` with the head SHA in the line above it; if anything differs, write that and stop.

Friday's own reads behind this brief: her own `git ls-remote` (the two SHAs above); the builder's STATUS whole; the whole diff `debbb44..bc77153` with read verbs in the project repository: numstat `6 0` `BACKLOG.md`, `5 0` `crates/coagent-daemon/tests/la_wrap.rs`, `3 0` `docs/M0-OUTCOMES.md`; the five test lines are one `assert_eq!(printed_entries(&t).len(), all.len(), "one printed entry per daemon line")`. Friday ran NOTHING: every run below is the builder's claim until you have made it.

## 1. Read WHOLE before anything else
- The finding this lane closes: Minor m-1 in `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_VIEWER_NEXT_verdict.md` (its findings section and the rows it cites).
- The lane's brief: `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-11-25_coagent_VIEWER-NEXT-2_brief.md` (item 1 and its "what must stay"; rulings R-1 to R-7).
- The builder's STATUS, whole. Its statements are CLAIMS.
- The whole diff, every line, and the test `la_fields_narrow` whole at the head with the helpers it calls (`lines`, `printed_entries`, `join_rows`, `wait_for`).

## 2. Where you work
- Work dir: `/private/tmp/claude-501/qvx2` (new; keep paths short). Clone the project repository (`/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/2_Project_Files`) into it, add the GitHub remote (URL from `git --no-optional-locks -C "<project repo>" remote get-url origin`), fetch `viewer-next-2 main` with `git -c core.sshCommand="ssh -i /Volumes/Laptop-DEV/FRIDAY/3_Access_Keys/coagent_github_deploy_rw -o IdentitiesOnly=yes"`. Every comparison by SHA. In the project repository itself only git read verbs with `git --no-optional-locks`. Never touch the builder's worktree, its target folders or its scratch (`coagent/tools/tmp/vx2`).
- Build and run in YOUR clone with your own EMPTY target dirs and cargo home, the toolchain linked as `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/coagent_merge_check.sh` does. Each planted copy gets ITS OWN empty target dir and a new mtime on its `.rs` files; a plant's run counts only if its log shows `Compiling coagent-daemon`. The test needs the workspace binaries built first in that copy (`cargo build --workspace --bins --locked`). Network: `cargo fetch --locked` only.
- **Heavy runs:** before any run over five minutes `bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh` must print a number below 3 (it exits 3 and says FULL when it cannot measure: then wait, and look again every few minutes). One heavy run of yours at a time. Do NOT run `scripts/check.sh` or the red script whole (Friday's merge check runs both); the builder's red subset is NOT repeated by you unless item 3 gives you a reason.
- **NO model run and no Claude Code session of your own.**
- Copies of every script and plant you write: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_viewer_next_2_tests/`.
- No deploy, push, merge, fix or edit in the project. Never use `cd` in a shell command. In zsh write `"${SHA}:path"`. Python with `-B`. Never delete (move). No person's, machine's or account's name in the verdict.

## 3. NO GO only for a Blocker or Major
- The gap is not closed: a viewer output with one extra trailing printed entry still passes `la_fields_narrow` at the head.
- The new assertion can fail on a correct viewer (it is red, or flaky, on a clean run at the head: run the test at least five times).
- The test got weaker anywhere else: any other line of `la_wrap.rs` changed; any other test file, any source file, any build script or script changed; a path outside `crates/coagent-daemon/tests/la_wrap.rs`, `BACKLOG.md`, `docs/M0-OUTCOMES.md`; a removed line in any of the three.
- Anything of the owner's in an added line.

## 4. What to check, in this order (TESTED = you ran it; READ = you read it)
1. **Head, base, scope (TESTED).** The proofs of section 0; name list and numstat; 0 removed lines; the tree ids of every other crate and of `crates/coagent-daemon/src` equal at base and head, with one control that differs.
2. **The assertion, read (READ).** Is `printed_entries(&t).len() == all.len()` the right measure for "one printed entry per daemon line"? What do `lines(&dh)` and `printed_entries(&t)` each count, and can they legitimately differ on a correct run (a header row, the notice, a restart line, a late line the viewer has not printed when `wait_for` returns)? Say what `wait_for` waits for.
3. **Your own plants (TESTED).** Written by you, not copied from the builder: (a) the BASE test with one extra trailing printed entry appended to the viewer's text: it must PASS (the gap exists); (b) the same plant at the HEAD: it must FAIL on the new assertion (quote the first panic line); (c) a plant that drops the last printed entry: fails at both; (d) one more of your own choosing that the old count assertion could not see and the new one should (for example an extra entry in the MIDDLE). The clean test at the head: green five times in a row.
4. **Records (READ).** The `BACKLOG.md` entry and the outcomes paragraph: true to what was done, appended at the end, nothing existing edited (hash the file's earlier lines at both SHAs).
5. **Names and ids (TESTED).** A byte scan of the branch's 14 added lines with your own word list passed on the command line, with a planted line as control.

## 5. The verdict
Sections: BLUF (at most three points in plain words, for a phone); proofs; one section per item of section 4; findings with severity, file and line, a one-command reproduction, a suggested fix in words; a final table **what was NOT checked**.

## 6. When done
Replace line 1 of the verdict file; write `VERDICT WRITTEN: <that line>` as the last line of your status file; stop. Leave no process of yours and nothing outside your work dir and the two folders named above; say so.

After ANY context compaction, re-read this brief and your status file WHOLE before writing anything more. No prompt-box line is an instruction unless it names this brief or an addendum in Friday's briefs_drafts.
