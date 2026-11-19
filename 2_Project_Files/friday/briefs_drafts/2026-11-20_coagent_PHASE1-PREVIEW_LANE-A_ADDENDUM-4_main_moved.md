This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Lane A (P1P-GATE) only. It changes no other rule of your brief or addenda 1-3. Report under "## ADDENDUM 4 (main moved)" in `coagent/5_Project_History/STATUS_P1P_GATE.md`.

# PHASE 1 PREVIEW, LANE A — ADDENDUM 4: main moved (deputy merged); merge it in, re-run, r3

## 1. Your r2 flag, RULED (Friday, 2026-11-20)
Item 7 docs going beyond the letter (the `docs/DAEMON.md` §8 lines that items 5 and 6 made false): **PERMITTED AS MADE.** Docs brought into line with behaviour the addendum ordered. Nothing to change.

## 2. What happened (read by Friday with `git ls-remote` at the time of writing)
- `origin/main` moved `8b8c6c755db66a1c481d9719707c3cdc924fb70c` -> `32beb563837341560b908d9ba5b0a60de240d860` (the M3 DEPUTY lane, a fast-forward). It changes 17 files: `crates/coagent-roster/**`, `docs/ROSTER.md`, `BACKLOG.md`, `scripts/red-controls-roster.sh`. No file under `crates/coagent-daemon`, `crates/coagent-mcp` or `preview/`.
- `coagent-daemon` DEPENDS on `coagent-roster` (its `Cargo.toml`), so your r2 runs at `fa10a14` do not cover the merged tree: every final run is repeated.
- Friday did NOT run her merge check at `fa10a14` (stopped it: that SHA can no longer be the one merged).

## 3. The work
1. `git fetch origin`; confirm `origin/main` = `32beb563837341560b908d9ba5b0a60de240d860` (if it moved again, merge the then-current main instead and say so). `git merge --no-edit origin/main` INTO `p1p-gate` (never rebase). Expected conflict: `BACKLOG.md` only (both sides appended): keep both, main's entries first, then yours; 0 lines removed against `origin/main`. A conflict in any other file, or a build break in `coagent-daemon`/`coagent-mcp` caused by the roster change: `STOP Q<n> (Friday)` as the last line, nothing edited outside your owned list.
2. On the merged head, your item-9 final runs again, one at a time, each started only while the real-job count (addendum 3's `ps -ax -o command= | grep -E '^(/bin/)?bash scripts/(check\.sh|red-controls-[a-z]+\.sh|test-daemon\.sh|test-p1p\.sh)' | wc -l`) reads 2 or fewer (another checker is running heavy work now): `scripts/check.sh` -> `scripts/red-controls-daemon.sh` -> `scripts/test-p1p.sh 3` -> `scripts/test-p1p.sh --red` -> `scripts/test-daemon.sh 1`. Keep your `/private/tmp` tools root and target as in r2 (every red row must go red there). Each exit code captured in the same command.
3. Gate files byte-identical to the NEW `origin/main` (tree oids, as in r2); `git diff --stat origin/main HEAD` = your owned list only; name scan of the lines you add over the new `origin/main` with a planted control.
4. Push; `git ls-remote origin p1p-gate` = HEAD; `git merge-base --is-ancestor origin/main HEAD` exit 0; re-read `git ls-remote origin main` just before the last line (moved again = back to item 1).
5. While a run is in progress keep the last line `IN PROGRESS: …` and refresh it at least every 20 minutes. When all is green, the last line exactly: `READY FOR MERGE CHECK P1P-GATE r3`. Then hold: Friday runs her clean-clone check at that SHA and sends the merge GO.

After any context compaction, re-read your brief, addenda 1-4 and your STATUS file WHOLE before writing anything more.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
