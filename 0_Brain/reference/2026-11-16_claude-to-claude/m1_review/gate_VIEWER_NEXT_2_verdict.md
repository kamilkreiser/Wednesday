VERDICT: GO — head bc771535cff36b74cfbf0d187fa6c06a257e21e9

# QA-VIEWER-NEXT-2: the check of branch `viewer-next-2` (closes m-1 of the VIEWER-NEXT check)

Date 2026-11-25. Checker: QA-VIEWER-NEXT-2 seat. Nothing in the project was written, nothing deployed, no model run.
Work dir `/private/tmp/claude-501/qvx2` (clone, own cargo home, one empty target dir per run). Scripts, plant diffs and logs: `gate_viewer_next_2_tests/` beside this file.
Tags: TESTED = I ran it; READ = I read it.

## BLUF
1. **The gap is closed.** A viewer that prints one extra trailing entry (or two) passes `la_fields_narrow` at the base and fails at the head on the new assertion (`one printed entry per daemon line`, left 24, right 23). A dropped entry, and an entry added in the middle, also fail on it at the head.
2. **The new assertion is not flaky.** It was green on a clean run at the head 25 times in a row (5 + 20), and the whole `la_wrap` file was green once (10 of 10). Every entry the viewer prints starts with `#<digits> `; the header, notice and restart lines do not.
3. **Nothing else changed.** Three files, 14 added lines, 0 removed. Every other crate and `crates/coagent-daemon/src` are byte-identical by tree id. The two record entries are appended and nothing earlier is edited. The byte scan of the 14 added lines found nothing; its two controls were found.

No Blocker, no Major, no Minor. Two Notes below.

## 1. Proofs (TESTED)
- `git ls-remote` against the GitHub remote, fetched with the deploy key (2026-11-25):
  `bc771535cff36b74cfbf0d187fa6c06a257e21e9 refs/heads/viewer-next-2`, `debbb4442fc90b1d5c1f04f123a665dcd8cf381f refs/heads/main`.
- `git rev-list --parents -n1 bc77153…` prints the head and ONE parent, `debbb44…`. `git rev-list --count debbb44..bc77153` = 1. `merge-base --is-ancestor debbb44 gh/main` exit 0 (main has not moved).
- Builder's STATUS: 72 lines; the last two lines are `bc771535cff36b74cfbf0d187fa6c06a257e21e9` and `READY FOR QA VIEWER-NEXT-2`. As the brief says.

## 2. Item 1: head, base, scope (TESTED)
- `git diff --name-only debbb44 bc77153`: `BACKLOG.md`, `crates/coagent-daemon/tests/la_wrap.rs`, `docs/M0-OUTCOMES.md`. Exactly those three.
- `--numstat`: `6 0 BACKLOG.md`, `5 0 …/la_wrap.rs`, `3 0 docs/M0-OUTCOMES.md`. `--shortstat`: 3 files, 14 insertions, 0 deletions. The whole diff is in `gate_viewer_next_2_tests/branch.diff`; every hunk is added lines only (`@@ -1519,3 +1519,9 @@`, `@@ -899,6 +899,11 @@`, `@@ -189,3 +189,6 @@`).
- Tree ids, base against head: `crates/coagent-daemon/src` `ceabd083ad2c…` = `ceabd083ad2c…`; `crates/coagent-daemon/tests/la_support` `fa17b154…` = `fa17b154…`; `scripts` `6c75b616…` = `6c75b616…`; and every one of the other 12 crates (`audit-host, audit, cli, crypto, hook, ipc, mcp, policy, proto, relay, roster, scanner`) EQUAL. **Control that differs:** `crates/coagent-daemon` (whole) and `crates/coagent-daemon/tests` (`18deac1f…` vs `14653f83…`) differ, as they must.
- `git diff-tree -r --name-status`: three `M` entries and nothing else: no source file, no other test, no script, no `Cargo.toml`/`Cargo.lock`.

## 3. Item 2: the assertion, read (READ)
The head text (`la_wrap.rs:902-907`):
```
    let (all, _) = lines(&dh);
    assert_eq!(
        printed_entries(&t).len(),
        all.len(),
        "one printed entry per daemon line"
    );
```
- `wait_for("every entry", 20 s, |t| activity_lines(t).len() == cases.len())` (`la_support/mod.rs:108-122`, `:161-173`) polls the viewer's output every 50 ms and returns when exactly `cases.len()` output rows start with `#`; it panics after 20 s. Then `v.stop()` kills the viewer and `v.text()` is read.
- `lines(&dh)` (`la_support/mod.rs:40-54`) counts every `activity` line the daemon holds, all pages. `printed_entries(&t)` (`la_wrap.rs:652-665`) counts the output rows that satisfy `entry_head` (`#`, one or more digits, a space; `la_support/mod.rs:176-182`); continuation rows (starting with the fixed `    | ` mark) join the last entry and are not counted.
- Can the two legitimately differ on a correct run? **No.** The viewer's own non-entry rows (`src/watch.rs`) are the notice (`Only you see this…`), the header (`CoAgent mode: APPROVE…`), the mark note, the cut note, the cut-scope note, the restart text (`coagentd watch: the daemon restarted…`) and `N older lines dropped`; none starts with `#<digits> `, and none is counted. The notice repeats every 20 entries and is not counted. A restart line cannot occur here (one daemon, no restart) and a `dropped` line cannot occur at 23 lines. The viewer prints one entry per daemon line (`entry_rows` for each line of the answer, `shown += 1`).
- Late line: after `wait_for` returns, the daemon holds exactly the lines it had (the decisions are all made before the viewer starts), so no new head can appear. The only thing that can still arrive after `wait_for` is the continuation rows of the last entry (the viewer prints row by row); those are not counted by the new assertion (they would matter to `join_rows` and `:908`'s later checks, exactly as before this lane).
- So `printed_entries(&t).len() == all.len()` is the right measure for "one printed entry per daemon line", and with the unchanged `entries.len() == cases.len()` they hold exactly when printed entries = daemon lines = cases. The measured value is 23 on every run.
- Placement: right after `let (all, _) = lines(&dh);` and before the `zip`, so it sees the printed entries, not the `min`.

## 4. Item 3: my own plants (TESTED)
Method: each copy is `git archive` of the SHA, its `.rs` files given a new mtime, its OWN empty target dir, `cargo build --workspace --bins --locked`, then `cargo test -p coagent-daemon --locked --test la_wrap -- --exact la_fields_narrow`. Every run log shows exactly one `Compiling coagent-daemon` line. The plant text (`plant.py`, mine, not the builder's) changes only `let t = v.text();` of `la_fields_narrow`: `extra` appends a copy of the last printed entry's rows; `extra2` appends it twice; `drop` cuts the text at the last entry's head row; `mid` repeats entry 5's rows right after themselves.

| plant | at BASE `debbb44` | at HEAD `bc77153` |
|---|---|---|
| (a)/(b) `extra`: one extra trailing entry | **PASSES** (`test la_fields_narrow ... ok`): the gap exists | **FAILS**, first panic: `la_wrap.rs:907:5: assertion `left == right` failed: one printed entry per daemon line`, `left: 24`, `right: 23` |
| (c) `drop`: last entry dropped | FAILS on the old count: `la_wrap.rs:914:5: assertion `left == right` failed`, `left: 22`, `right: 23` (`assert_eq!(entries.len(), cases.len())`) | FAILS first on the new one: `la_wrap.rs:908:5 … one printed entry per daemon line`, `left: 22`, `right: 23` |
| (d1) `extra2`: two extra trailing entries | PASSES | FAILS: `la_wrap.rs:909:5 … one printed entry per daemon line`, `left: 25`, `right: 23` |
| (d2) `mid`: one extra entry in the middle | FAILS, but only later and for another reason: `la_wrap.rs:929:5: 2 entries whose head is not one field each` (the entries after the copy are misaligned with the daemon lines; the old count `:908` did not see it: `min(23,24)`) | FAILS first on the new assertion: `la_wrap.rs:911:5 … one printed entry per daemon line`, `left: 24`, `right: 23` |

(The line numbers differ between rows only because each plant adds lines before the assertion.) The only differences between base and head in these plants are: `extra` and `extra2` pass at the base and fail at the head; `drop` and `mid` fail at both but at the new assertion at the head. Every one is the new assertion.
- **Clean test at the head, 25 of 25 green:** five runs in a fresh empty target dir (`run1..5.log`, 1.1-2.0 s each, `Compiling coagent-daemon` in run 1), then 20 more (`extra1..20.log`), then the whole file `la_wrap`: `test result: ok. 10 passed; 0 failed`. Heavy-run count read before building: 2 (`heavy_runs.sh`); every run was short (seconds), no run over five minutes.

## 5. Item 4: records (READ + TESTED)
- Earlier lines unchanged: the first 1521 lines of `BACKLOG.md` at the head hash to the same value as the whole file at the base (`af53c404…`), the first 191 lines of `docs/M0-OUTCOMES.md` likewise (`f725e673…`). Both files end with a newline after the appended lines. Appended at the end: `BACKLOG.md` lines 1522-1527 (6), `M0-OUTCOMES.md` lines 192-194 (3).
- `BACKLOG.md` entry: `- [x]` with Where / Symptom / Why deferred / Discovered / Resolved, in the file's own shape. It says what the verdict found (`zip` makes the count `min(daemon lines, printed entries)`), that a trailing extra entry passed (my plant (a) shows it did) and that the fix is one assertion before the `zip`. True to what was done. "Why deferred: n/a (fixed by the next viewer lane, as ruled)" is accurate for an entry written closed.
- Outcomes paragraph: "one assertion added before the `zip`, no other line of the test, no daemon source and no binary changed". Test part TESTED (numstat, tree ids). "No binary changed" is REASONED: every crate tree and `Cargo.lock`/manifests are identical, so the inputs of the four binaries are identical (I did not rebuild both and compare sha256; see the table).

## 6. Item 5: names and ids (TESTED)
- `git diff -U0 debbb44 bc77153`, the 14 `+` lines only, written to a scratch file; `scan.py` (mine, outside the project, words only on the command line at run time, never in a file): 21 words (the account and host names of this machine, the home path, the owner's name and mail domain, the coordinator names, the workspace and project-folder names, client names, the mail service) in plain, JSON/backslash-escaped, URL-encoded and slug spellings = 33 patterns, plus session/tool/request/message id shapes, UUIDs and mail addresses. **Result: 14 added lines, hits 0.**
- Controls: the same lines plus one planted line holding the home path and the host name: hits 8; a planted binary (random bytes around NUL/0xFF and the host name): hits 3. Both found.
- Context only (not the branch's lines): `BACKLOG.md` has 45 hits and `M0-OUTCOMES.md` 1 at the head and the SAME counts at the base (earlier lanes' text, mostly client names, not touched by this branch); `la_wrap.rs` 0 at both.

## 7. Findings
No Blocker, no Major, no Minor.
| id | severity | note |
|---|---|---|
| N-1 | Note | The assertion is exact equality of printed entries and daemon lines, so it relies on `decide_fields` making all decisions before the viewer starts (true today, `la_wrap.rs:886-896`). A future change that lets the daemon log more lines while the viewer runs would need this assertion read again. No action now. |
| N-2 | Note | An entry added in the middle was already refused at the base, but only by the later head-parse check at `:929`, not by the count. After this lane the count refuses it first. This is the same defence, not a gap. |

Reproduction of the central result (my scratch): `bash gate_viewer_next_2_tests/mkcopy.sh plant-extra-head bc771535cff36b74cfbf0d187fa6c06a257e21e9`, then `python3 -B gate_viewer_next_2_tests/plant.py <copy>/src/crates/coagent-daemon/tests/la_wrap.rs extra`, then `bash gate_viewer_next_2_tests/build_test.sh plant-extra-head 1` (same with the base SHA for the pass).

## 8. What was NOT checked
| not checked | why |
|---|---|
| `scripts/check.sh`, the whole red script, `scripts/test-p1p.sh`, the builder's red subset (LA-VN-1 and the 19 other LA rows) | brief: Friday's merge check runs `check.sh` and the red script; the red subset was not repeated because no item gave a reason |
| the four binaries' sha256, base against head | not repeated; the source trees, manifests and lock file are identical, so it is REASONED; builds in different copies embed different paths and cannot be compared byte for byte without the same path |
| clippy and fmt at the head | builder's claim, not re-run (the change is five lines of plain `assert_eq!`; the whole `la_wrap` file compiled and ran) |
| the other `la_*` test files and the lib tests | not re-run by me; only `la_wrap` was run whole, once |
| a real terminal, Windows, characters a real host sends, long sequence numbers | out of the lane (ruling R-6) |
| the correctness of `docs/DAEMON.md` §8 | not touched by the branch; not read |
| whether main moves after 2026-11-25 | the head and main were read once, at the start |
| pushing, merging, any deploy | not done; none was part of this check |

Left behind: no process of mine is running; nothing outside `/private/tmp/claude-501/qvx2`, `gate_viewer_next_2_tests/`, this file and `coagent/5_Project_History/STATUS_QA_VIEWER_NEXT_2.md`. Nothing deleted.
