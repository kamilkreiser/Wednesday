This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat POLICY-MODE only. It changes what brief section 5 item 1 makes you re-run after TODAY's move of main, and nothing else. Report under "## ADDENDUM 2 (after main moved)" in your STATUS file.

# POLICY-MODE — ADDENDUM 2: after your merge of main (fc7acfc), re-run check.sh only

What Friday read: your line says main moved, you merged it as `fc7acfc`, and you queued check.sh, the red-controls run and t24 again. Main moved today from `32beb56…` to `d57f3a2ab6714acac3bb1bae7fbd58496adfbb20` by the phase 1 preview: the daemon crate, a new `coagent-hook` crate, `preview/`, docs and scripts. Friday read the diff: nothing under `crates/coagent-policy` and nothing in `docs/POLICY.md`. The policy crate's own dependencies are outside crates from the workspace table, unchanged.

What DID change for you: `crates/coagent-daemon` and `crates/coagent-hook` now depend on `coagent-policy` (their `Cargo.toml`). So on the merged tree your changed crate is built into the daemon and the hook for the first time, and the daemon's gate tests call `decide`.

The ruling (it SUPERSEDES "Re-run everything below on the merged tree" in brief section 5 item 1 for this one merge):
1. Show that your crate is the same in both heads: `git diff --stat 8204180 fc7acfc -- crates/coagent-policy docs/POLICY.md` must print nothing. Record the command and its (empty) output with a positive control (the same diff without the path filter prints the preview's files). If it prints anything: this addendum does not apply; re-run everything as the brief says.
2. With item 1 empty: your `crates/coagent-policy/red-controls.sh` run (58 of 58 RED OK, normal build green) and your t24 property run at `8204180` STAND for `fc7acfc`. Say so in STATUS, each with the head it ran on. Do not queue them again.
3. On `fc7acfc` you DO run, once: `scripts/check.sh` (the whole workspace, so the daemon and hook build and test against your crate). Record totals start against end; the start figure on the new main is Friday's clean-clone 1,206 passed / 0 failed / 20 ignored at `b7e8da4` plus whatever your crate adds. Any failure in a daemon or hook test: quote it and STOP (do not edit those crates).
4. Then section 5 items 5 to 9 on `fc7acfc` as written: protected hashes; `git diff --stat origin/main...HEAD` inside your owned paths; the dark check (`git grep -n "BypassView\|decide_with_mode" -- crates` lists files under `crates/coagent-policy/` only: on this tree that now also proves the daemon and the hook do not name them); the name scan with its control; push; ls-remote; ancestor; re-read main.
5. If main moves AGAIN before your READY: merge it; if `git diff --stat <old main> <new main> -- crates/coagent-policy docs/POLICY.md` is empty, repeat items 3 and 4 only.

Heavy-run rules and the HEAVY-SLOT PRIORITY addendum are unchanged. Last line when all is done, exactly: `READY FOR QA POLICY-MODE`.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
