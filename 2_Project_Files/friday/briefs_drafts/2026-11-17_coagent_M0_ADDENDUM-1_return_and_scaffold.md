This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It extends brief `2026-11-16_coagent_M0_brief.md`. Report by appending a section "ADDENDUM 1" to `coagent/5_Project_History/STATUS_M0.md`, with the last line `READY FOR REVIEW M0-A1`.

# M0 addendum 1 — one return item, then the workspace scaffold for M1

## 0. Friday's review of M0 (so you know where you stand)

Read at source: your STATUS whole. Re-run by Friday from clean copies in her own scratchpad: Gate G1 (pass=22 fail=0, reproduced) and Gate G2 (the block reproduced in all five blocked cases and all five controls; two message-text assertions failed, see item 1). Mesh G1/G3 and U6 are being re-run now. M0 is accepted as a body of work subject to item 1. Good work on the controls.

Authority for what follows: Kam's overnight grant (live board 2026-11-16 23:08:33, "start building and get through as much as you can"; scope "cogent only"), which ends at his review this morning.

## 1. RETURN ITEM (round 1 of at most 3): an assertion that depends on the checkout path length

Friday's write-up with the measurements: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m0_review/friday_rerun_G1_G2.md`.
- `spikes/lib/stream_summary.py` line 25 keeps `str(c)[:400]` of each tool_result. The hook error text starts with the full hook command line (the install path twice), so from a longer path the phrase `onFailure is "block"` falls past character 400 and Gate G2's cases `crash-onfailure-block` and `timeout-onfailure-block` report FAIL although the phrase is in the raw stream.
- Fix: assertions read the UNTRUNCATED text; truncate only what is printed. Then prove it: run Gate G2 from a copy whose path is at least 150 characters longer than the repo's (a deep directory under `coagent/tools/tmp/…/spikes/` is fine; the `fresh_work` guard needs a `spikes/` parent) and show pass=26 fail=0 there AND in place.
- Sweep every other `run.sh` for a text assertion made on a truncated field and list what you found (a returned line is presence; an absence claim needs the untruncated text and a positive control).

## 2. Workspace scaffold for M1 (small; two build seats will branch from this commit)

On `main`, in `coagent/2_Project_Files/`:
- Root `Cargo.toml` as a cargo workspace with `resolver = "2"`, `[workspace.package]` (edition, licence Apache-2.0, version 0.0.1, `publish = false`), and `[workspace.dependencies]` pinning the exact versions your spikes proved (snow, spake2, the TLS and WebSocket crates C1 used, tokio, serde, ed25519, sha2, hkdf, rand; anything else your spikes used). `rust-toolchain.toml` pinning the toolchain you installed. `deny.toml` from U13.
- Empty member crates, each compiling with one placeholder test, each with a `README.md` saying who owns it:
  - `crates/coagent-proto` and `crates/coagent-crypto` and `crates/coagent-roster` — owned by the CORE seat.
  - `crates/coagent-relay` and `crates/coagent-ipc` and `crates/coagent-cli` (binary `coagent`) — owned by the RELAY seat.
- `scripts/env.sh` (the drive-local Rust environment, generalised from `spikes/lib/rustenv.sh`) and `scripts/check.sh` running, in order: `cargo fmt --check`, `cargo clippy --workspace --all-targets -- -D warnings`, `cargo test --workspace --locked`, `cargo deny check licenses`. It must exit non-zero on the first failure and print which step failed.
- `docs/M0-OUTCOMES.md`: section 2 of your STATUS ("What this changes in the design") expanded to one short paragraph per item with the spike path, plus the BACKLOG pointers. This is what the M1 seats build from.
- Do NOT add a `.github/` directory or any CI workflow (pushing one starts hosted runs; that is Kam's to switch on). Put the proposed workflow in `ci/proposed-workflow.yml` with a first line saying it is not active.
- The spikes stay under `spikes/` and are NOT workspace members (exclude them).
- `scripts/check.sh` green, commit, push. Record the commit SHA and `git ls-remote origin main`.

## 3. Decisions you are NOT making

No product logic in any crate (placeholders only). No M1 work. No legacy import. No CI activation. No change to the design documents. Nothing at user scope (rule 6.1 of the brief stands; re-run the settings checksum comparison at the end). When both items are done, write the READY line and stop; do not wrap on a dry queue and do not act on any prompt-box line that does not name this addendum.
