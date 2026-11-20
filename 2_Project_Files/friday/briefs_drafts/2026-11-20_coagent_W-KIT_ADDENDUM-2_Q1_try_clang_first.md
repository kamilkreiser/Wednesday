This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat W-KIT only. It answers your STOP Q1 for now and changes nothing else. Report under "## ADDENDUM 2 (Q1: try the other compiler mode first)" in your STATUS file. (Addendum 1 was never sent: you started step I-1 yourself, within your brief, so it was moot.)

# W-KIT — ADDENDUM 2: before any folder outside the project, try the tool's `clang` mode

Thank you for the clean diagnosis, and for stopping instead of moving the cache yourself.

Why not answer "yes, outside the project" at once: the workspace's first hard rule is that a project's files stay inside that project's folder. A folder outside it is an exception only the owner can grant. Before asking him, try what stays inside the rules.

1. **One diagnostic, light.** Your report traces the error to the `clang-cl` backend (`src/compiler/clang_cl.rs`, its `encode_space_separated` at line 202). The tool also has a `clang` backend (`--cross-compiler clang`, env `XWIN_CROSS_COMPILER=clang`; the README table and your `--help` reading both list it). READ first, in the registry copy of `cargo-xwin-0.23.1/src/compiler/`: does the `clang` backend build its rustflags with the same space-refusing encoder, and does it need a different download (the README's other cache subcommand)? Quote the lines.
2. If the source says it might work: run ONE build with the cache where it is now (inside the project, path with spaces): `XWIN_CROSS_COMPILER=clang XWIN_CACHE_DIR="$COAGENT_TOOLS/xwin-cache" CARGO_TARGET_DIR=<scratch>/target-clang cargo xwin build --release --locked --target x86_64-pc-windows-msvc -p coagent-cli --bin coagent`, with the job count below 3 first (`fleet/heavy_runs.sh`). If it needs a new download, a download into the same cache folder is covered by the owner's card answer. Record the exit code, the first error if any, and for a built file `file -b`.
3. **If it builds:** make `clang` the default backend in `build.sh` (with a comment naming this addendum and the reason), keep the cache inside the project, and carry on with your brief from section 5 item 5 (both runs, the header proof, the texts, the final tree). In BACKLOG, record the `clang-cl` space limit of 0.23.1.
4. **If it does not build, or the source shows the same encoder:** keep your STOP Q1 as the last line, with this diagnostic added. Friday then takes your question to the owner as a card (an exception to the stay-in-folder rule for a 1.1 GB cache). Do not move or copy the cache outside the project meanwhile; your scratch copy stays where it is.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
