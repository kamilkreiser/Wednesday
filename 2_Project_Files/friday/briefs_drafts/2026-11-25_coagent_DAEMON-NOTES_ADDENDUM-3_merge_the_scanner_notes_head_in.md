This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. It belongs to the brief `2026-11-24_coagent_DAEMON-NOTES_brief.md`. Seat DAEMON-NOTES only. Report under "## ADDENDUM 3 (merge the scanner-notes head in)" in your STATUS file.

If your context was compacted: re-read your brief, addenda 1 to 3 and your STATUS file WHOLE before doing anything.

# DAEMON-NOTES ADDENDUM 3: one more small merge, by Friday's decision, so that your lane lands without waiting a second time

## 1. Why
Your merged head `379daffd598f3a5ffc4945d51b76b351f9d483c5` holds main `9145840f24f23aff5b589044ce8aa8776283bdac`: thank you. Another lane, the scanner follow-up, lands BEFORE yours: its merge check is the short one (about an hour and a half) and is running now on its merged head `1b1ac447041ea3df56384cd4547561ec076a3130` (= its checked head plus main `9145840`). Your merge check takes about three hours. So that both checks can run side by side, each on the exact commit that will land, you merge that one commit into your branch now. When the scanner follow-up has landed, main IS `1b1ac44`, and your head lands after it by fast-forward. If its check fails, this merge is void and Friday sends new steps: nothing of yours is lost.

By Friday's own `git diff --name-only 9145840 1b1ac44` in her clone, that commit differs from main in 11 files: `BACKLOG.md`, files under `crates/coagent-scanner/`, `docs/SCANNER.md` and `scripts/red-controls-scanner.sh`. No file under `crates/coagent-daemon/` or `crates/coagent-mcp/`, no `Cargo.toml`, no `Cargo.lock`, not `docs/M0-OUTCOMES.md`. The two sides share ONLY `BACKLOG.md`, where its side appends 5 lines.

## 2. What to do (a closed list; anything else is a `STOP Q<n>`)
1. `git fetch origin`; confirm `git ls-remote origin scanner-notes` is `1b1ac447041ea3df56384cd4547561ec076a3130`, `git ls-remote origin main` is `9145840f24f23aff5b589044ce8aa8776283bdac`, and your branch is `379daffd598f3a5ffc4945d51b76b351f9d483c5` with a clean worktree. If any differs, STOP and say so.
2. `git merge 1b1ac447041ea3df56384cd4547561ec076a3130` into `daemon-notes` (a merge commit, by that exact SHA; never a rebase, never a force push). A conflict is expected ONLY in `BACKLOG.md`: keep BOTH sides whole (the other side's lines, your eight ticked boxes with their `Resolved:` lines, your added lines). A conflict anywhere else is a `STOP Q<n>`.
3. Prove the merge by program and quote it in STATUS: (a) `BACKLOG.md`: every line of `1b1ac44:BACKLOG.md` that is not one of your eight flipped boxes is present in yours, in its order, and what remains is exactly your lane's lines as they stood at `379daff`; (b) `git diff 379daff HEAD --name-only` lists exactly the 11 files of `git diff --name-only 9145840 1b1ac44` (compare the two lists by program); (c) `git diff 1b1ac44 HEAD --name-only` lists exactly your lane's 17 paths; (d) for each of your 16 paths other than `BACKLOG.md`, the blob at HEAD equals the blob at `379daff`; (e) for each of the 10 other-side files other than `BACKLOG.md`, the blob at HEAD equals the blob at `1b1ac44`; (f) the merge commit's two parents are exactly `379daff…` and `1b1ac44…`.
4. Run only: `cargo fmt --all --check` and `cargo build --workspace --bins --locked`. Do NOT re-run the daemon tests: no file the daemon or the tool server builds from changed in this merge, and Friday's clean-clone merge check runs `check.sh` and the daemon red script on this head.
5. Push only `daemon-notes`. Record `git ls-remote origin daemon-notes scanner-notes main`.
6. The last line of STATUS, exactly: `READY FOR MERGE CHECK DAEMON-NOTES r2` with the new head SHA in the line above it. Then wait for the merge GO addendum naming that one SHA; it comes only after the scanner follow-up has landed.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
