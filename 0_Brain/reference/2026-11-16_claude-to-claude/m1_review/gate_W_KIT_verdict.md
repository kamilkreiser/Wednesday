VERDICT: GO WITH NOTES — head c7aabcd3808233ae36ee7dc99ea76ef217afe464

# QA-W-KIT verdict (2026-11-21), branch `w-kit`, main `16e83fbe5592658ddcda769d7827895941eca678` merged in

## BLUF
1. **Yes.** One command on the Mac (`bash scripts/windows/build.sh`) produced `coagent.exe`, `coagent-hook.exe`, `coagent-mcp.exe`, each a Windows x86-64 program by its header, from a clean state, in my own root. `coagentd.exe` is NOT built, and the script says so plainly (`NOT BUILT coagentd error[E0425]: cannot find value `uid``).
2. **Nothing outside the project is touched beyond the granted cache folder.** The script writes only inside `$COAGENT_TOOLS` and that cache. In the cache, cargo-xwin itself re-makes 4 entries on each build (one link, two small helper files, the folder's own date) with identical content. The cache is otherwise unchanged.
3. **Still needs the real Windows machine:** everything. No program has been run. Both texts say NEVER RUN on every Windows line, and `coagentd.exe` is stated as NOT YET.
4. **Notes, none blocking:** my files are not byte-equal to the builder's (sizes differ because each file embeds its build folder path; section 3); the `--offline` guard is weaker than the tool's own test (note 4); the built files carry the build machine's folder paths inside them (note 2).

## 1. Scope and protected files (TESTED)
- `git diff --stat origin/main...c7aabcd`: 4 files, 465 insertions, 0 deletions: `BACKLOG.md` (+30), `preview/demo/windows.md` (+116), `scripts/windows/README.md` (+100), `scripts/windows/build.sh` (+219). With the path filter (`scripts/windows preview/demo/windows.md BACKLOG.md`) the same 4 files. `git diff --name-status` main..head: `M BACKLOG.md`, `A` three. Nothing else.
- sha256 at the head, equal to the builder's section 1: Cargo.toml a0b39c45…d26, Cargo.lock 0c013986…bc, rust-toolchain.toml 6b1cf834…25d, deny.toml 4ce01609…b44, scripts/check.sh 5e4349e0…ce1, scripts/env.sh 27f8f5ed…14c, preview/demo/lan.md 640bd9d9…e99. All equal.

## 2. `build.sh` read whole (READ, at the head)
- Write targets: `mkdir -p` of `$LOGS` and `$OUT`; `> $LOGS/*.log`; `: > case_aliases.list`; `ln -s` only inside the cache and only when neither the name nor a link of that name exists (`[ ! -e ] && [ ! -L ]`); `cp -f` of its own freshly built `.exe` into `$OUT`; `shasum > SHA256SUMS.txt` in `$OUT`. There is NO `rm`, `mv`, `rmdir`, `-delete`, `sudo`, `curl`, `wget` or `brew` anywhere. Overwrites are only of the script's own outputs (`windows-out/*.exe`, `SHA256SUMS.txt`, logs).
- `cd`: line 43 (to the repo root, `|| exit 3`) and the `( cd "$OUT" && … )` subshell. `COAGENT_TOOLS` is checked non-empty (line 50) before anything is built from it, so no path starts with an empty variable. No `rm -rf "$X/"` exists.
- Space guard (line 63): refuses a cache path with a space, exit 3, before any write.
- Exit codes as documented: 0 / 1 / 2 / 3 (all seen below).
- bash 3.2: `/bin/bash` is 3.2.57; `bash -n` exit 0; no `declare -A`, `mapfile`, `readarray`, `${x,,}`, `|&`. `shellcheck` is not on this Mac; not installed (nothing installed by me).
- Header check is in the script: BUILT is printed only when cargo exits 0, the file exists and `file -b` says `PE32+ … x86-64`; otherwise NOT BUILT. A stale `.exe` from an earlier run is reported `STALE`, never listed in `SHA256SUMS.txt`.

## 3. Runs from a clean state in my own root (TESTED; logs in `gate_w_kit_tests/logs/`)
My root has `cargo/bin`, `rustup`, `xwin-kit` as links to the project's, and my own `target`, `windows-out` and cargo registry. Heavy count before each run: 1 (below 3), no higher seat showed `waiting for a heavy slot`.
- **Run 1** (online, clean): exit 0, 42 s. `BUILT coagent 2849792 809e5db9…`, `BUILT coagent-hook 582144 6f69e82a…`, `BUILT coagent-mcp 848896 2ee2a79c…`, `NOT BUILT coagentd error[E0425]: cannot find value `uid` in this scope` + the NOTE line, `WROTE SHA256SUMS.txt`.
- **Run 2** (`--offline`, same state, incremental): exit 0, 5 s, same four lines, same hashes as run 1.
- **Run 3** (`--offline` from a CLEAN state; my addition because run 2 is incremental): exit 0, 35 s, same four lines, same SIZES, different hashes (`1f5e1a90…`, `37807de5…`, `2e233ccd…`).
- `file -b` on each of the three: `PE32+ executable (console) x86-64, for MS Windows`. `shasum -a 256 -c SHA256SUMS.txt`: all three OK (after runs 1, 2 and 3).
- **Against the builder's final pair: NOT equal in hash, and the sizes also differ** (builder 2857984 / 583680 / 850944; mine 2849792 / 582144 / 848896; differences 8192 / 1536 / 2048). Cause found, not just assumed: each `.exe` embeds the cargo registry path of the build (my coagent.exe holds 234 such strings, all my root's registry path); my root's path is much shorter than the project's, so mine are smaller. REASONED from that; the sizes of my own clean runs 1 and 3 are equal to each other. Two clean builds in one place also differ in hash, so a byte-equal match across builds is not to be expected. Not a fault.
- Nothing under the clone's `target/` (`ls` said no such file); clone `git status` clean.

## 4. Network on `--offline` (TESTED)
- Case-insensitive `grep -c` for `download` and `http` over run 1, run 2 and run 3 stdout: 0 and 0 each. Over run 3's `_logs/*`: `download` 0; `http` 6 lines, all non-network: 4 lines are Windows library file names (`httpapi.lib`, `winhttp.lib`, in the link line) and 2 are `Compiling httparse` / `Compiling http` (crate names).
- **Positive control:** the builder's first-download log, still readable in the project's quarantine (`_quarantine_2026-11-21/w-kit_run1_failed_state/target_windows/_logs/coagent.log`): `download` 2 ("Downloading MSVC CRT…", "Downloaded MSVC CRT in 29s."). So the search finds a download when one happened. Honest limit: I did not capture packets; the evidence is the logs, the cache folder being unchanged apart from note 3, and the script's own `--offline` handling (cargo `--offline`, `CARGO_NET_OFFLINE=true`).
- **Empty cache + `--offline`** (`XWIN_CACHE_DIR` = an empty folder of mine, a fresh tools root): exit **3**, message "--offline but the cache folder is empty"; nothing written in the tools root or the cache; no build started (probe `p1_hostile.sh`).

## 5. Hostile inputs (TESTED)
- `XWIN_CACHE_DIR` with a space (with and without `--offline`): exit 3, reason printed, the folder was not created, nothing written.
- `COAGENT_TOOLS` unset and set to the empty string, in an isolated copy of the two scripts whose parent folders hold no tools folder (probe `p2_tools_unset.sh`): `env.sh` falls back to `<repo parent>/tools`, then the tool check prints `MISSING TOOL: …` and exits **2**; nothing written under the isolated tree and nothing created at `/tools`, `/target`, `/windows-out`. (In a clone that does have a tools folder as an ancestor, as mine does, `env.sh` finds it; that is the designed behaviour, not a refusal.)
- Lower-case name already present: my work disk is case-INSENSITIVE, so I made a 20 MB case-sensitive scratch image in my work dir (`hdiutil`, mounted at a scratch path, unmounted after; nothing installed) and ran the `add_case_aliases` function text, extracted from `build.sh` at the head, on a fake cache (probe `p3_case_alias.sh`): an existing `kernel32.lib` with different content (hash, inode and size unchanged), an existing dangling `userenv.lib` link, a lower-case-only `dbghelp.lib`: all untouched. It added links only for `Advapi32.Lib` and a name with a space (`Ws2 32.Lib`); a second call made 0. On the case-insensitive disk it made none. The function was tested extracted, not by a full run on the fake cache, because a full run on a fake cache would reach the tool and the network.

## 6. The texts (READ + checked at the head)
- `scripts/windows/README.md` and `preview/demo/windows.md`: no sentence says a Windows program ran. `windows.md` header: "written for the day `coagentd.exe` exists. It does NOT exist yet"; every Windows command line is tagged `NEVER RUN` (daemon, join, status, send, inbox_read, inbox_ack, stop); UNVERIFIED tags on the quotes, shell syntax, SHA tool, reachability tool, unsigned warning. README says BUILT here, never RUN, and `coagentd` NOT YET.
- Cited lines checked at the head (more than the ten asked): `lan.md` 3-6, 15, 21-22, 33-48, 42, 44, 46-48, 52-56, 61, 62, 64, 65, 67-70, 81; `main.rs` 20-21, 23, 113, 181-185, 190; plan 15 sections 2.4, Q3, Q6 (headings exist at those numbers). All say what the text says they do.
- Removal steps: folders are moved into `_quarantine_<date>/` ("it is only a cache"); the only delete-type commands are the tool's own `cargo uninstall` and `rustup component remove`, written as the removals the brief's table named, for the coordinator.
- No person, machine, drive or client name in either text; the host address is `<LAN_IP>`.

## 7. BACKLOG (READ)
`git diff main..head -- BACKLOG.md`: one hunk, 30 lines added, 0 removed, six entries each in the file's form (Where / Symptom / Why deferred / Discovered): coagentd not producible; programs never run; cache folder outside the project; case-sensitive limit; licence step; hosted build machine. No other line changed.

## 8. Names scan (TESTED)
465 added lines, case-insensitive for `/Users/`, `/Volumes/`, `/private/`, `/home/`, `C:\Users`, `kamil`, `kreiser`, `Secuura`, `Datasec`: **1 hit**, the ruled constant `XWIN_CACHE_DEFAULT` (build.sh line 15; line 261 of the added-lines file). Extra words (`Friday|Wednesday|Tuesday|Kam`): 0. Positive control (a planted line added to the same set): 2 hits.

## Notes (not blocking)
1. **Hashes not byte-equal to the builder's** and sizes differ; cause in section 3 (embedded build path). Not a fault.
2. **The built `.exe` files embed the build machine's folder paths** (cargo registry path; the builder's carry the project folder path). If a file is handed to another person, it carries those folder names inside it. Nothing in the texts says so; Friday may want a line in the hand-over.
3. **The tool re-makes four entries in the cache folder on every build** (the `clang-cl` link, `cmake/clang-cl/override.cmake`, `cmake/clang-cl/x86_64-pc-windows-msvc-toolchain.cmake`, and the folder's own date): same link target, same sizes, same sha256 on the two cmake files before and after. This is cargo-xwin's own housekeeping, not script code, and it happens on any build with that tool. The rest of the cache, compared by name, type, size and link target before and after, is unchanged.
4. **The `--offline` guard tests only that `xwin/crt` and `xwin/sdk` exist.** The tool decides by its `DONE` marker (`clang_cl.rs` around lines 256-280, READ). A half-filled cache without `DONE` would pass the script's guard and the tool could then try to download. Not run (network is not allowed here). The real cache has `DONE`. A one-line addition (also test `xwin/DONE`) would close it.
5. The shared state moved while I worked (other seats' runs touched the project's `tools/` and `.git/objects`); my runs used my own cargo home, target and output, and I attribute none of those to me (REASONED).
6. `shellcheck` not available; not installed.

## What I used and left
- Heavy builds: 3 (runs 1, 2, 3; count 1 before each). Network: only run 1's `cargo fetch --locked` and the `git fetch`. No model runs. No deploy, push or merge; the project folder was written only at `5_Project_History/STATUS_QA_W_KIT.md`. The only write in the cache folder was cargo-xwin's own, note 3.
- Work dir `/private/tmp/claude-501/qwk` (clone, my tools root, quarantined outputs, a 20 MB scratch image, unmounted) and `/private/tmp/claude-501/qwk_iso` remain; nothing deleted. Probes and logs copied to `gate_w_kit_tests/`. No process of mine is running and nothing of mine is mounted.
