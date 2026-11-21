This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat W-KIT only. Report under "## ADDENDUM 4 (notes, then merge main)" in your STATUS file.

# W-KIT — ADDENDUM 4: the check's notes, then hold for the relay lane's merge

## 0. The authority
The independent check: `VERDICT: GO WITH NOTES — head c7aabcd3808233ae36ee7dc99ea76ef217afe464` (`/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_W_KIT_verdict.md`, READ-ONLY; read it WHOLE). No Blocker or Major. The list below is the coordinator's ruling on its notes; it is CLOSED and stays inside your owned paths (`scripts/windows/**`, `preview/demo/windows.md`, `BACKLOG.md`).

## 1. What to do now
1. **Note 4 (the `--offline` guard):** the script's offline check must also require the tool's own completion marker, `<cache>/xwin/DONE` (READ `cargo-xwin` `clang_cl.rs` around lines 256-280 at the version you installed and quote the exact marker path it tests). A cache without it refuses with exit 3 and a plain reason, as an empty cache does today. Test it with a scratch copy of the cache folder's top level that lacks the marker (no network; no change to the granted cache).
2. **Note 2 (build paths inside the programs):** make the built programs carry no folder path of this machine. In `build.sh`, pass `--remap-path-prefix` through `RUSTFLAGS` (or `CARGO_ENCODED_RUSTFLAGS`) for the cargo home / registry folder and the repository root, mapped to neutral names (for example `/cargo` and `/src`). Read the rustc documentation page for the flag first and cite its URL in a comment. Then show it worked: `strings` (or a byte search) over each built `.exe` for the tools root path, the repository path and the drive name: 0 hits, with a positive control (the same search over one of the earlier outputs in quarantine, which must find them). If the flag cannot remove a class of path, say which and why, and write it as a README limit instead.
3. **Note 3:** one README sentence: the tool itself re-makes four small entries in the cache on every build (name them); that is the tool's housekeeping.
4. **Note 1:** nothing to do (different build folders give different bytes; say so in README if not already).
5. Run `build.sh` from a clean state, then again with `--offline`: exit codes, the four result lines, `file` on each output, `shasum -c`. Count heavy jobs first (`bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh` below 3). Commit, push.

## 2. Then HOLD for the relay lane
Last line while holding, exactly: `IN PROGRESS: notes done at <sha>; holding for MERGED RELAY-RECONNECT`. Nothing merges to main before the relay lane: the owner is waiting on it, and any main move before it costs that lane about four hours of re-runs. Watch `git ls-remote origin main` every 5 minutes, or wait for Friday's pointer.
When `main` has moved off `16e83fbe5592658ddcda769d7827895941eca678`:
1. Merge `origin/main` INTO the branch (never rebase). Expected conflict: `BACKLOG.md` only, both sides kept. `Cargo.lock` must stay byte-identical to your start value; if main changed it, STOP.
2. Run `build.sh` from a clean state once on the merged head (heavy count first), plus the `file` lines and `shasum -c`.
3. Your brief's section 6 final checks (scope with control, protected hashes, nothing under the repository's `target/`, names scan with control (still exactly the one ruled constant), push, ls-remote, ancestor, re-read main).

Last line when all is done, exactly: `READY FOR MERGE CHECK W-KIT r2`.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
