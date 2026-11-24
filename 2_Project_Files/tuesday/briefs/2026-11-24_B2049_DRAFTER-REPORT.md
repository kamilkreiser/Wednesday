STARTABLE: YES (Q1 and Q2 must be answered "a" in words at the stamp: Q1 refuse a non-`/` device root; Q2 the chain policy beside the landed revocation mode, proved through the internal seam `TlsOptions`)

# B2049 DRAFTER REPORT: lane L2 (owed 79, 87, 83, 84 parts 1 and 3), seat Datasec/OXPd2-X64

Drafter B2049 (Opus, in-session, read-only toward the project and GitHub), 2026-11-24 15:27 to about 15:55 AEDT. Lane L2 only; nothing of lane L1 (B2048) touched.
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2049_SEAT-X64_oxpd2-l2-library-followups.md`.
- Sidecar: `.measured` beside it (`stamp_check.py`: 189 claims, 189 measured, rc 0).
- Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s323/d2049/` (below `<d>`); seat tools in `<d>/seat-tools/`.
- Gate tier G1, round 1 of 2 of lane L2.

## BLUF
- **BASE** is main `e2a20aefda7d4356af2b264576a7e3faaf0bce2c` (PR 45). Its hosted run, read by `hosted3.py`: `HOSTED e2a20aef...: PASS` at `--total 2112 --rules 657` (run 45284683760; linux 2108, windows 2091 succeeded; guards 14 and 15).
- **What is built** (frozen in `1-red.diff` + `2-fix.diff`; seven paths, all M, no file added):
  - **Owed 79 (code):**
    - `DeviceTokenClient` refuses a device root whose `AbsolutePath` is not `/` with `InvalidArgument`, before any connection (default a of Q1: refuse, not "state the rule").
    - It adds `CertificateChainPolicy { RevocationMode = NoCheck, DisableCertificateDownloads = true }` beside the landed `CertificateRevocationCheckMode = NoCheck`.
    - Doc comments on the client and on `DeviceAuthOptions.DeviceRoot` updated.
  - **The proof that fails on main:** cell DA18 reads the handler's own `SslOptions` through a new `internal` property `TlsOptions`. `1-red.diff` adds that seam with main's settings byte for byte, so the red is main's own configuration (`policy set False`). DA18 also makes one pinned call (with the issuer never sent) to show the policy does not break the pin. DA17 holds the root rule (5 refused paths, 0 connections, and 2 taken roots as the control).
  - **Owed 87:** one bullet in the adapter README's "Limits of the generated reading" covering the other exceptions a caller meets, `ResponseHeadersRead` so that only the caller's token bounds the body read, and the drained non-success body. `Generated/` is untouched.
  - **Owed 83:** the `ConnectFailed` doc comment, plus two transport README sentences:
    - a handshake past `ConnectTimeout` ends as `Failed`;
    - the caller's cancellation leaves as `OperationCanceledException`;
    - and, my widening, a call after `Dispose` or with a null argument throws `ObjectDisposedException` or `ArgumentNullException`, read at `HttpIppTransport.cs:53-55`.
  - **Owed 84 (1) and (3):** "`401` while the vault answers", plus the `503` sentence and the rewrap of the 209-character line (word sequence equal, by program). Part (2) is untouched, so item 84 stays open.
- **Measured in a fresh `<d>/clone6` with the frozen patches:**
  - RED: the OXPd 2 test executable `Total: 88, Errors: 0, Failed: 2` (DA17 and DA18, each `Assert.Equal() Failure`).
  - GREEN: `total: 2114`, `failed: 0`, `succeeded: 2110`, `skipped: 4`.
  - Mutants: `MUTANTS: 4 of 4 MATCH, 4 of 4 undone equal`.
  - Chain: locks 34 of 34 equal, build 0/0, test 2114/0, guards 14/15, `Ran 111 tests` OK, `RULES: clean (657 files)`.
  - `CHECKS: 8 of 8 PASS`, `WORDS: clean (2 files)`, `B2[0-9]{3}` 0/0.
  - gitleaks: control rc 1; clone rc 0; 12 neutral files rc 0.
- **PREDICTED hosted:** `--total 2114 --rules 657` (linux 2110, windows 2093).
- **Partition from L1:** this lane writes only the seven owned paths. `checks_l2.py` check 3 proves L1's four folders, `contracts` and `Generated` unchanged (rc 0, control rc 1).

## Facts re-measured (instrument)
- Origin `main` = `e2a20aef...` (`gh api -X GET`, 15:27:23, Datasec account). Open PRs: 0. `matching-refs/heads/b2049`: 0 (control `b20`: 5). `.tools/b2049` and `.tools/b2048`: absent.
- R316 (B2045) has ENDED: its STATUS last line is `READY B2045: 4c9f8d39...`. No records write meets this lane.
- Toolchain: dotnet `10.0.404`, gitleaks `8.30.1`.
- `CLARIFICATIONS.md` (1114 lines, newest C-84): every subject word counts 0; controls `C-63` 1 and `OXPd` 183. No product-owner word touches this lane.
- **Seat X64 is free:** 0 seat-id hits across 209 non-`.pre-` SEAT kits from 11-17 to 11-24. The one textual hit is `ELF_X64`, a constant in kit B1705. Control: X62 hits in B2044, B2042 and B2045. No `Datasec/OXPd2` pane is live.
- **Local CodeQL is NOT runnable here:**
  - CodeQL 2.27.4's C# autobuild/extractor binaries (`csharp/tools/osx64/*`, 19 files) are all x86_64.
  - `codeql database create --language=csharp` fails with `Bad CPU type in executable`.
  - `arch -x86_64 /usr/bin/true` fails the same way, so Rosetta is not installed.

## D-decisions (Tuesday's as coordinator; each is a Q in the kit)
- D1: refuse a non-`/` root (Q1).
- D2: add the chain policy and keep the landed mode (Q2).
- D3: an internal seam for the proof (Q2/Q3).
- D4: a new cell DA17, not a row inside landed DA14 (Q3; owed 79 said "one more DA14 row").
- D5: owed 87 as README text only.
- D6: owed 83 as text only, no remapping to `ConnectFailed` (Q5).
- D7: owed 84 parts (1) and (3) only.
- D8: platform words are marked "measured on macOS arm64" (the earlier reviewers' probes, RELAYED) or UNMEASURED.
- D9: no local CodeQL (Q4).
- D10: one commit, one push.

## Q-questions for Tuesday (each with its default)
- **Q1 (STOP-CLASS):**
  - a (built): refuse.
  - b: state the rule only.
  - c: honour the path.
- **Q2 (STOP-CLASS):**
  - a (built): policy + landed mode + seam-read cell + pinned call.
  - b: a behavioural AIA-fetch cell (cannot go red on macOS).
  - c: drop the landed `CertificateRevocationCheckMode` line.
- **Q3:** DA17 as a new cell (default) vs rows inside DA14.
- **Q4:** no local CodeQL (default); code scanning on the PR is read before landing. The alternative, installing Rosetta, is a machine change and is Kam's.
- **Q5:** text only (default) vs map the handshake timeout to `ConnectFailed` with a cell (a new kit; `HttpIppTransport.cs` is outside this kit).
- **Q6:** platform words marked (default).
- **Q7:** Opus, READY at Step 0 + 120, push at Step 0 + 90, pane X64, G1 round 1 of 2. **S7 is yours:** the hard stop against tonight's meeting.
- **Q8:** either landing order with L1.
- **Q9:** 84(2) is not this lane's.
- **Commission divergence to note:** it asked for "local CodeQL and gitleaks per the form". The form kits B2011 and B2021 carry gitleaks only; neither ran local CodeQL. I tried it and measured it not runnable, so the kit replaces it with Step 6 (d), a printed NOT RUNNABLE line.

## UNMEASURED / NEVER RUN
- Both hosted legs for this head. DA18's handshake with the policy has not run on Linux or Windows.
- What any platform fetches with the policy set (H8). macOS without the policy: 0 fetches (probe P07, RELAYED).
- Kit H3 and H4 (`//`, `/./`, a backslash, IPv6 roots) are DERIVED from `Uri.AbsolutePath` and not run.
- The seat's own steps: the seat-mode clone, the commit, `run_step.py`'s neutral scan on a commit, the push, the read-back, `hosted3.py` on a head of this lane, and the rebase.

## Disclosure (no fence crossed; the edges)
- **First frozen set discarded:**
  - Midway I widened the transport README sentence (the disposed and null-argument throws, found while writing the item-11 frame).
  - I stopped the first frozen run with TaskStop during a load wait, before the mutants. No lock was held and no heavy process was left (both checked).
  - Its clones, patches and gate copy are in `<d>/_quarantine/v1/`. Every number in the kit comes from the second set (`<d>/clone5` cut, `<d>/clone6` run).
  - Its logs reused the `c4-` labels, so `<d>/logs/c4-*` hold the second set's output, except `c4-cq-*`, which are the first set's CodeQL attempt.
- **One stray stdin wait:** a `sha256sum` with no argument waited on stdin. I stopped it with TaskStop; it wrote nothing.
- **Hook refusals:**
  - `pretooluse_no_cd.sh` refused two calls, once for `cd` and once for a `cd /` in a heredoc. Both were re-issued without `cd`.
  - `pretooluse_zsh_wordsplit.sh` refused two calls (`=====`, and an unquoted `$H`). Both were re-run under `bash`.
  - A `sleep 60` was blocked and replaced by an until-loop.
- **Git use:** draft clones only (push URL `invalid://no-push`). Staging and applies happened in my scratch clones only. No commit, no ref, no push. GitHub only by `gh api -X GET` under the project's `GH_CONFIG_DIR`; `hosted3.py` read BASE's run.
- **Heavy jobs:** every dotnet job and test executable went through `heavy.py` and the wave lock. Lock waits were 0 to 5, and the runner waited on load1 ≥ 7 once (load reached 10.45). The CodeQL attempt also ran through `heavy.py` and failed at once.
- **Not touched:** Source_Documents, key folders, the NAS library, credentials files (only `gh` read its own config), any records file, X62's clone. No Jira, printer, Azure or message.
