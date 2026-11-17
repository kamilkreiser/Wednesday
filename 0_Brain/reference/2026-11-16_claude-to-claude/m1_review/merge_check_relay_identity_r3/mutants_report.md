# Mutant re-check N20 / N21 / N24 / N36 at 454bfb5 (branch m1-relay-identity)

Copy under test: `$W/mut` (`git clone "$W/clone" "$W/mut"`), HEAD asserted `454bfb566dd854648d0af9427ee0c8393043bb5e`.
`W=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/mc_relayid`

Note on paths: at 454bfb5 `identity_file.rs` lives in `crates/coagent-cli/src/identity_file.rs`, not
`crates/coagent-relay/src/` as the brief and the gate verdict say. All four checks were found unchanged in text there;
every mutation is the gate's own mutate2.py edit, applied byte for byte (each old text occurred exactly once).

## Baseline

`cargo test -p coagent-relay -p coagent-cli --offline --locked --no-fail-fast` in `$W/mut`, target `$W/target_mut`:
exit 0, 22 test binaries, **185 passed, 0 failed, 5 ignored**. All four named tests ran and passed.

## Results

| mutant | file:line @454bfb5 | before | after | result | failing tests (all runs: exactly 1 failure) | first assertion text |
|---|---|---|---|---|---|---|
| N20 | crates/coagent-cli/src/identity_file.rs:377 | `        } else if left.uid() != uid {` | `        } else if false {` | **KILLED** | `a_leftover_owned_by_another_user_id_is_kept` (tests/identity_file.rs:335) — seat's named test | `a leftover owned by another user id was removed (1)` |
| N21 | crates/coagent-cli/src/identity_file.rs:379 | `        } else if left.mode() & 0o077 != 0 {` | `        } else if left.mode() & 0o070 != 0 {` | **KILLED** | `a_leftover_open_to_others_is_kept_and_refuses_the_start` (tests/identity_cli.rs:1068) — seat's named test | `a leftover with mode 604 was removed instead of refusing the start` |
| N24 | crates/coagent-cli/src/identity_file.rs:490-491 | `    check_parent(dir, &dmd, uid)?;` / `    let removed = remove_leftovers(path, uid)?;` | `    let removed = remove_leftovers(path, uid)?;` / `    check_parent(dir, &dmd, uid)?;` | **KILLED** | `a_start_aimed_at_an_open_folder_removes_nothing_there` (tests/identity_cli.rs:1098) — seat's named test | `a start aimed at a folder open to others (mode 755) removed a file there before refusing` |
| N36 | crates/coagent-cli/src/relay_cmd.rs:153 (in `address_refusal`) | `    if !bind_allowed(opts.listen, opts.allow_non_loopback) {` | `    if !bind_allowed(opts.listen, false) {` | **KILLED** | `the_early_address_refusal_honours_allow_non_loopback` (tests/identity_cli.rs:1121) — seat's named test | ``assertion `left == right` failed: the early refusal ignores --allow-non-loopback for 192.0.2.1:0`` (left: `Some("refusing to listen on 192.0.2.1:0: it is not a loopback address. ...")`) |

All four mutants compiled (failures are test assertions, not compile errors; each run's only failing target was the
one test above). After each run the file was restored with `git -C "$W/mut" checkout -- <file>` and
`git -C "$W/mut" status --short` was asserted empty; final HEAD still 454bfb5, tree clean.

## Commands

Environment (same as mc_run.sh, separate target):
`CARGO_HOME=$W/ch RUSTUP_HOME="/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/tools/rustup" CARGO_TARGET_DIR=$W/target_mut PATH=$W/ch/bin:$PATH`

Test command (cwd `$W/mut`): `cargo test -p coagent-relay -p coagent-cli --offline --locked --no-fail-fast`

Driver: `/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/mut_run.py`
(`python3 mut_run.py base`, then `python3 mut_run.py N20 N21 N24 N36`). Logs: `$W/mut_base.log`, `$W/mut_N20.log`,
`$W/mut_N21.log`, `$W/mut_N24.log`, `$W/mut_N36.log`.

## Not done / caveats

- `--no-fail-fast` was added to the brief's command so every failing test in a mutant run is listed.
- N20's test calls the public `remove_leftovers(path, uid + 1)` (the file is owned by the real user, the function is told
  another uid); it does not create a file owned by another real user. That is the route the gate suggested.
- N36's test checks `address_refusal` directly; no non-loopback bind was attempted.
