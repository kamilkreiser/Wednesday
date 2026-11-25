VERDICT: GO WITH NOTES — head dbc9c0a9fad3b03fff3d723bf2e66eb376ac1913

# Second independent check: CoAgent `audit-host-notes`, the fix round after M-1 (addenda 1 and 2)

Checker: QA-AUDIT-HOST-NOTES-R2 (new seat; did not build the round, did not make the first check). Work dir `/private/tmp/claude-501/qahn2`: `repo/` (own clone of the project repository, the GitHub remote added as `gh` and fetched by deploy key), detached worktrees `head/` (dbc9c0a), `h52/` (52ad858), `ha0/` (a0379be), own cargo home `tools/cargo` (bin and rustup LINKED to the project's drive-local toolchain as `coagent_merge_check.sh` does; registry its own), one EMPTY target dir per tree under `target/`. The project folder was only read (git read verbs with `--no-optional-locks`), except my STATUS file.
Copies of my tests and scripts: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_audit_host_notes_r2_tests/`.

## BLUF (for a phone)
1. **The table now names every answer a seal can give.** I listed every answer of `seal_begin`, `seal_finish` and `seal` from the code myself: each has a row, or (the two test-only ones) the new sentence. My list and the builder's agree on every row. In the first check's 8,901 fault cases, the 702 seal answers that had no row now all fall on new row 14; 0 are left without a row.
2. **What the new rows tell a caller is true and safe.** Each of the four refusals of row 15 left the folder byte for byte as it was, and the seal then worked. After every one of 10 failed step-2 writes there was no window and nothing committed (also after a restart). Retrying once gave one seal with no second checkpoint. The two test-only answers cannot happen in a real build: a planted call to the hook fails both dev and release builds. Seven wording notes, none unsafe: the closest are "retry once" on `NothingToSeal` (harmless) and row 15 not saying `seal_finish` closes your own window.
3. **Nothing else changed:** not one byte of code (same file ids). The 13 old rows are byte for byte the same and in order. The docs test is red on every broken copy the brief names. BACKLOG has 9 lines appended and nothing edited. fmt, clippy and the docs test are green. Nothing of the owner's is in a changed line.
4. **Not covered:** `ArchiveMismatch` and the too-large answers were read, not provoked; the merge with the newer `main` is Friday's next step. The daemon may be wired by this table, keeping the m-2 BACKLOG entry in mind. **Verdict: GO WITH NOTES.**

## 0. Proofs (TESTED, 2026-11-25 12:12)
- `git ls-remote gh audit-host-notes main` (deploy key, GitHub remote): `dbc9c0a9fad3b03fff3d723bf2e66eb376ac1913 refs/heads/audit-host-notes`, `1b1ac447041ea3df56384cd4547561ec076a3130 refs/heads/main`: both as briefed. Fetched by name; `rev-parse gh/audit-host-notes gh/main` give the same two; the project repository's own `origin/audit-host-notes` and `origin/main` (read with `--no-optional-locks`) are the same two.
- `cat-file -t dbc9c0a…` = `commit`. `merge-base --is-ancestor`: `52ad858` → head exit 0; `9145840` → head exit 0; `a0379be` → head exit 0; `1b1ac44` → head exit 1 (main's newer commit NOT merged in, by Friday's rule: not a finding).
- `git log --format='%H %P %s' 52ad858..dbc9c0a`: exactly TWO commits, `a0379be…` (parent `52ad858…`, "addendum 1: … (check M-1)") then `dbc9c0a…` (parent `a0379be…`, "addendum 2: … (Q1 answered)").
- The builder's STATUS (`coagent/5_Project_History/STATUS_AUDIT_HOST_NOTES.md`): 263 lines (`wc -l`); last line `READY FOR QA AUDIT-HOST-NOTES r2`, the line above it `dbc9c0a9fad3b03fff3d723bf2e66eb376ac1913`. As briefed.

## 1. Head, base, scope of the round (TESTED)
- `git diff --name-only 52ad858 dbc9c0a`: `BACKLOG.md`, `crates/coagent-audit-host/tests/notes_docs.rs`, `docs/AUDIT-HOST.md`; numstat `9 0`, `16 2`, `7 0` (32 added, 2 removed): as Friday listed. No other path; no `Cargo*` path (`git diff --name-only 52ad858 dbc9c0a -- '*Cargo*'` → 0 lines).
- `git diff --name-only 9145840 dbc9c0a` (the whole lane): 11 names, filtered against the lane's owned set (`crates/coagent-audit-host/`, `docs/AUDIT-HOST.md`, `scripts/red-controls-audit-host.sh`, `BACKLOG.md`, `docs/M0-OUTCOMES.md`): **nothing outside** (grep exit 1); control: the same filter prints a planted `crates/coagent-audit/src/x.rs` and drops `BACKLOG.md`.
- Blobs `52ad858` = head: root `Cargo.toml` 5c0f3bc3, `Cargo.lock` 0094acf1, crate `Cargo.toml` 254ec317, `rust-toolchain.toml` 63202c6f, `scripts/check.sh` 8bc02c25, `scripts/red-controls-audit-host.sh` 42ab312a. **No new dependency.**
- `git ls-tree -r` of `crates/coagent-audit-host/tests/` at both: the ONLY difference is `notes_docs.rs` b92c088b → 444daa04.

## 2. No code moved (TESTED)
- `git diff 52ad858 dbc9c0a -- crates/coagent-audit-host/src crates/coagent-audit-host/build.rs scripts/red-controls-audit-host.sh | wc -c` → **0**. Control: the same pathspec `9145840` → `52ad858` → **21393**.
- Blob ids at `52ad858` and at the head: `host.rs` b41866f6 = b41866f6; `fsio.rs` 9238e099 = 9238e099; `error.rs` 2ba132d2 = 2ba132d2; `lib.rs` 08fe932b = 08fe932b; `build.rs` c13795c0 = c13795c0; the whole `src/` tree a0d4ef99 = a0d4ef99.
- **It holds**, so the first check's runs on the code (8,901 schedules, the lib run, the red script, the hook-absence proofs) stand for this head and are not repeated (brief §4 item 2).

## 3. My own enumeration (READ at the head, `host.rs` blob b41866f6; written before I opened the builder's A1.2/A2.5 again)
`seal` (`:1520-1528`) is `seal_begin(..)?` then `seal_finish(..)`: its answers are the union, except `NoSealInProgress`, which `seal` cannot give (its `seal_finish` follows a `seal_begin` that opened the window). "Normal" means a build without `cfg(test)` and without `coagent_audit_host_red`. The full table is in section 11. In short:
- **seal_begin.** `:1543` `Closed` (normal: the host was closed by an earlier `LandedUnknown` or by row 11's failed re-open) → rows 4 and 11 ("`Closed` after"; "open the host again"). `:1545` `SealInProgress` → row 15. `admit` (`&self`, so it cannot write): `TriggerOff` `:1456`, `:1465`, `:1474`; `NotDue` `:1460`, `:1470`, `:1491` → row 15 (its `:1450` `Closed` cannot be reached after `:1543`).
- **begin_steps.**
  - `:1557` `ensure_anchor` BEFORE step 0 answers `AnchorNotSaved` (`save_current` `:1150`) or the `anchors/limits` write's own `Dir` error (`save_limits` `:986` → `write_limits` `:724-725`). Normal build: an EARLIER change left the write unwritten (mutate `:1250`, release `:1363`, a seal's step 4 `:1666`, any re-open's phase 2). The answer and the action are named by row 1's retry column ("refuses the next change (`AnchorNotSaved`, or the `anchors/limits` write's own `Dir` error) until a save succeeds; offer the next change again then"). Row 13's answer and retry columns are the same shape and give the same action, but no row's CASE says "an earlier change's write" (Note N-r2-2).
  - Step 0 `:1559-1563`: `Audit(_)`, `Reopened{..}` and any `Ok` are swallowed; returned are `LandedUnknown` (`mutate` `:1262`) → row 4, and `LimitsChanged{answer: Ok(Checkpoint) | Err(Reopened{landed})}` (`:1288`) → row 8, then row 1, 2 or 3. That is the m-2 family, already in BACKLOG by Friday's ruling and reachable only when a re-open changes the limits in force. `mutate`'s `:1243` `Closed` cannot be reached.
  - `:1564` `Closed` cannot be reached either: a swallowed `Reopened` follows a re-open that put a member in place (`:1072`).
  - `:1569` (N-d) `AnchorNotSaved` or the `anchors/limits` `Dir` error → row 13.
- **plan_and_file / write_archive** (all before `self.window = Some` at `:1573`):
  - `:1592` `Closed` cannot be reached.
  - `:1594` `seal_export` gives `Audit(..)`: `NothingToSeal`, `NotAuthor` for an `id` not the member's, store read or encode errors → row 14 (and row 10).
  - `:1603` encode → `Audit(ExportTooLarge)` → row 14.
  - `write_archive`: `:1412-1413` `Audit(ExportTooLarge)` (bound); `:1416` `archive_names` → `Dir(Io{"list the archive", name: "archive"})`; `:1421-1422` `Dir(Bounds("archive attempts for one segment"))` (10,000 files of one segment); `:1429`/`:1437` `Dir(..)` of `archive/seg-…`; `:1431` the read-back `Dir(..)`; `:1432-1433` `ArchiveMismatch("archive/seg-…")`. All → row 14. The listing and the bound name no `archive/seg-…` file, so the row covers them by its case words, not its parenthetical (Note N-r2-1).
  - `:1609` `write_anchor(PENDING)` → `Dir(..)` of `anchors/pending`, or of the directory `anchors` when its sync fails → row 14.
  - `:1580` `Ok(SealBegun)`: success.
- **seal_finish.**
  - `:1630` `NoSealInProgress` → row 15.
  - `:1651` `Closed`, `:1681` and `:1751` `member_ref` cannot be reached in a normal build. The member was in place when the window opened (`:1564`, `:1592`). In the window nothing can drop it: `apply` queues (`:1186`), `drain` (`:1767`), `set_limits` (`:1781`) and `seal_begin` (`:1544`) refuse, and every other public method takes `&self`.
  - Commit `Ok` → `:1691` `Ok(SealReport)`: success; with the host closed after (`:1683` re-open failed) → row 11; `limits: Some` → row 12.
  - Commit `Err` other than `SealStale` (including `NotAuthor` when `seal_finish` gets an `id` not the member's) → re-open: `:1740` `LandedUnknown` → row 4; `:1752-1758` `SealCommitFailed` → row 7, or `LimitsChanged{answer: Err(SealCommitFailed)}` → row 8, then row 7.
  - `SealStale` (`:1700-1717`): the re-plan's step 1 or 2 `Err` (`:1707-1710`) and `SealStaleTwice` (`:1717`) → the sentence under the table. `seal_commit` answers `SealStale` only when the member's anchor is no longer the plan's (`crates/coagent-audit/src/session.rs:2290`). `anchor()` (`session.rs:588`) reads only the member's index, which changes only through `&mut` calls, and none reaches the member between `:1594` and `:1652` in a normal build. **So unreachable as built**, except through the `cfg(test)` hook (`:1631-1649`) or the red `seal_interleaved` (`:1186`).
- **Listed apart (not in a normal build).** Red-gated branches: `:1483` (`own_seat_counts_requests`, changes only `Ok`/`NotDue`), `:1568` (`seal_plans_while_dirty`), `:1597` (`commit_before_file_durable`), `:1608` (`pending_anchor_not_saved`), `:1614-1616` (`anchor_promoted_before_commit`: a `Dir` of `anchors/current`), `:1654-1662` (`commit_before_file_durable`: `Dir`/`ExportTooLarge` of the late file), `:1680`, `:1685`, `:1722-1728`, `:1736-1738`, `:1746-1750`, and `:1186` (`seal_interleaved`, making `SealStale` reachable). `#[cfg(test)]`: `:1631-1649` (the interleave hook), `:1006-1010` (the re-offer hook inside `reopen`, test-only shapes of row 12 and of m-2).
- **Against the builder's A1.2/A2.5 (read again after the above).** Every answer the builder lists is in my list with the same row, and every answer in mine is in the builder's with the same row. No answer is missing from either side and none has a different row.
  - Differences in detail only: (a) the builder puts `archive_names` (`:1417` in its table, the call is at `:1416`) and the attempts bound (`:1423`, the `return` is `:1422`) under "`Dir(..)` of `archive/seg-…`", but they name the directory `archive` or no file. (b) A few of its line numbers are one off (`:1432` read back is `:1431`; `:1434` `ArchiveMismatch` is `:1433`). (c) I add `NotAuthor` (a wrong `id`) under rows 14 and 7. (d) I add the directory-sync shapes of `anchors/pending` and the archive file, which name `anchors` and `archive` (section 4: 131 of the 702).
  - None of these changes a row or a retry.

## 4. The first check's count, re-made (TESTED, about 12:16)
- `table.py` copied from `gate_audit_host_notes_tests/` (with `compare.py`, its loader) into `/private/tmp/claude-501/qahn2/bin/`. The ONLY change to the "original" copy is its `sys.path` line, which now points at my bin (`table_orig_path_only.py`). In the edited copy (`table_r2.py`, the diff is in the copy's header) I added rows 14 and 15 from the document's words: a seal's `Err(Dir(..))` naming `archive/seg-…` or `anchors/pending` → 14; a seal's `Err(Dir(..))` naming the directory `archive` or `anchors` → 14 (counted apart as "by the case words"); `ArchiveMismatch` → 14; `SealInProgress`, `NoSealInProgress`, `TriggerOff`, `NotDue` → 15. Seal `Err(Audit(..))` stays on row 10 as before (row 14 names it too). With `QAHN2_NO14=1`, row 14 is taken out again.
- Input: the first check's `/private/tmp/claude-501/qahn/logs/diff_head.log`, 20,306,834 bytes, sha1 9833b9c29df72182…, read only. It stands for this head because the code is the same blob (section 2).
- **Edited:** `cases 8901; answers per row: 1: 1556, 10: 1118, 11: 13, 13: 75, 14: 702, 2: 45, 4: 131, 5: 1586, 6: 455, 7: 325, 9: 1261, Ok: 1634` / `row decision differs from the harness caller's …: 0` / **`answers NO row names: 0`**. **The 702 land on row 14.**
  - Their last failed operation is in every case a step-2 write: `archive/seg-…` CreateTemp 66, Write 72, SyncFile 70, Link 79, SyncDir 62; `anchors/pending` CreateTemp 72, Write 66, SyncFile 73, Rename 73, SyncDir 69. None is `anchors/limits` or `anchors/current`, so none belongs to row 13.
  - 131 of them (`archive` 62, `anchors` 69: the directory syncs) name the DIRECTORY, not the file, so row 14 names them by its case words; its parenthetical does not quite say so (Note N-r2-1).
  - Row 14's retry column ("the seal, once") matches the harness's caller in all 702. The caller's final open found segment 1 once.
- **Control 1, the unchanged `table.py`:** the same counts without row 14, `answers NO row names: 702` (the first check's figure).
- **Control 2, my edited copy with row 14 taken out:** `answers NO row names: 702`, and its list of unnamed answers is line for line the original's (`diff` empty).
- **What the schedules never drew** (so the table rests on my reading alone there): `Closed`, `SealInProgress`, `NoSealInProgress`, `TriggerOff`, `NotDue` (row 15: my test in section 5 draws all four), `LimitsChanged` of any shape, `ArchiveMismatch`, `Audit(ExportTooLarge)`, `Dir(Bounds)`, the archive listing's `Dir`, `Audit(NotAuthor)`, `Ok` with `limits: Some` (the first check's hook test only), and the `SealStale` paths (test hook only). Of row 14's `Audit(..)` only `NothingToSeal` was drawn (291 seals, on row 10).
- Copies: `gate_audit_host_notes_r2_tests/table_r2.py`, `table_orig_path_only.py`, `logs/table_{r2,orig,no14}.txt`.

## 5. Rows 14 and 15 and the sentence, word by word (READ + TESTED, runs 12:18-12:24)
My tree `t5/` = a worktree of my clone at dbc9c0a plus, UNCOMMITTED, `src/tests/qahn2_rows.rs` (mine) and `src/tests/qahn_seal_gap.rs` (the first check's, copied unchanged), with two `mod` lines appended to `src/tests/mod.rs`. Own target `target/t5`, debug. Its log shows `Compiling coagent-audit-host … (/private/tmp/claude-501/qahn2/t5/…)`. Run: `cargo test --locked -p coagent-audit-host --lib -- tests::qahn2_rows tests::qahn_seal_gap --nocapture --test-threads 1` → `test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 32 filtered out; finished in 4.01s`.

**Row 14** (each word against the source; `host.rs` line numbers at the head)
- Each named answer has a line that gives it:
  - `Dir(..)` of `archive/seg-…`: `write_archive` `:1429`/`:1437`, read back `:1431`.
  - `Dir(..)` of `anchors/pending`: `:1609` → `write_anchor` `:692-695`.
  - `ArchiveMismatch` of that file read back: `:1432-1433`.
  - `Audit(..)` of `seal_export`: `:1594`.
  - `Audit(ExportTooLarge)`: of the encoding `:1603`, of the size bound `:1412-1413`.
  - All TRUE as named.
- "before its window opened": the window is set only at `:1573`, after `plan_and_file` returned `Ok` (`:1571`). Every one of these answers returns through `?` before it. TRUE.
- TESTED (`qahn2_row14_words`): three own records, then a seal with ONE failed operation, for each of the five operations of the archive file (CreateTemp, Write, SyncFile, Link, the `archive` SyncDir) and of `anchors/pending` (CreateTemp, Write, SyncFile, Rename, the `anchors` SyncDir). 10 of 10:
  - The answer: `Err(Dir(Io{…}))` naming `archive/seg-00000000000000000000-0000.bundle` or `anchors/pending`; at the two directory syncs it names `archive` or `anchors`.
  - `in window false`; segment 0; own checkpoints 0 → 1 (step 0's landed).
  - A FRESH open of a copy of the folder taken right then (a restart without a retry): `Ok`, segment 0, own checkpoints 1. After the open no `anchors/pending` is left, including the SyncDir case, where the renamed `pending` WAS on disk: the open refused and removed it.
  - Archive files: 0 when the archive file failed before its link; 1 (the orphan, an ordinary export) from its SyncDir on and in every pending case.
  - **"nothing committed": TRUE.**
- The retry column, "The seal, once: its step 0 makes no second checkpoint". TESTED: the retry is made in two halves so the own chain is counted inside the window, before the seal collects it.
  - In all 10: `seal_begin` `Ok`, its `SealBegun::checkpoint` IS the landed checkpoint, own checkpoints inside the window still 1 (no second), `seal_finish` `Ok(1)`, segment 1 once. **TRUE.**
  - The first check's `qahn_seal_gap`, re-run at this head unchanged: `QAHN GAP [archive file]: seal Err(Dir(Io { what: "link a temporary file", name: "archive/seg-00000000000000000000-0000.bundle", kind: Other })); segment 0; in window false; own checkpoints 1; archive files 0` / `the seal again: Ok(1); own checkpoints 1; archive files 1`; `[pending anchor]: seal Err(Dir(Io { what: "rename a temporary file", name: "anchors/pending", … })); segment 0; in window false; own checkpoints 1; archive files 1` / `the seal again: Ok(1); own checkpoints 1; archive files 2`. As at 52ad858.
  - **Wording, TESTED:** when the owner records between the failed seal and the retry, the retry's step 0 DOES make a checkpoint, of the NEW event: `seal_begin (its checkpoint's own seq) Ok(Some(4)); own checkpoints inside the window 2; seal_finish Ok(1)`. That is not a duplicate. Row 13 says it exactly ("no second checkpoint of the same events"); row 14's shorter words do not. Nothing is recorded twice or lost (Note N-r2-3).
  - **`NothingToSeal`, TESTED:** a seal right after a seal answers `Err(Audit(NothingToSeal))`, and the folder is byte for byte unchanged (own checkpoints 1 → 1). The one retry row 14 (and row 10) permits answers `NothingToSeal` again and changes nothing. It is harmless and bounded ("once"), but in this plain case the retry cannot succeed until there is something new, and §6 step 1 says `NothingToSeal` is "reported, not retried" (Note N-r2-4). In the fault schedules the same answer came from a failed step 0 and the one retry DID succeed (the first check: 291 of 291).
- `ArchiveMismatch` and `Audit(ExportTooLarge)` were not provoked (READ only; NOT checked table).

**Row 15** (TESTED, `qahn2_row15_refusals_write_nothing`; each on a host with three own records; "folder" = every file's bytes and every name under the host's root, `lock` included)
| Refusal | How | Answer | Folder changes | Window | After the condition holds |
|---|---|---|---|---|---|
| `TriggerOff` | `Timer` with the default settings (timer off); `OwnFreePartAt(10)` (not the owner's threshold); each by `seal_begin` AND `seal` | `Err(TriggerOff(Timer))`, `Err(TriggerOff(OwnFreePartAt(Percent(10))))` | `[]` | false; segment 0 → 0; own checkpoints 0 → 0 | The same folder opened with the timer turned on in the settings (`timer_ms = 1000`), then due: `seal` `Ok(1)` |
| `NotDue` | timer 60 s on; `seal_begin` at 59,999 ms and `seal` at 30,000 ms | `Err(NotDue(Timer))` both | `[]` | false; 0 → 0; 0 → 0 | at 60,000 ms: `Ok(1)` |
| `NoSealInProgress` | `seal_finish` with no window | `Err(NoSealInProgress)` | `[]` | false; 0 → 0; 0 → 0 | a whole seal after it (another time, after a record): `Ok(3)` |
| `SealInProgress` | `seal_begin` opened a window (`Ok((1, "seg-…-0000.bundle"))`), then `seal_begin` AND `seal` again | `Err(SealInProgress)` both | `[]` (against the folder with the window open) | STILL open (not closed by the refusal); segment 0 → 0; own checkpoints 1 → 1 | `seal_finish` closes it: `Ok(1)`; then a seal with no window open: `Ok(2)` |
- **Control:** the same comparison across one successful record shows `["~anchors/current", "+store/…00000000000000000002"]`.
- `problems: 0`. **"That `Err`; nothing written": TRUE for all four** (READ as well: `SealInProgress` `:1545` and `NoSealInProgress` `:1630` return before any write; `admit` takes `&self`, so `TriggerOff`/`NotDue` cannot write).
- **The builder's changed retry words** ("the trigger turned on in the owner's settings and due" for Friday's "a trigger due"): TRUE and better. `TriggerOff` comes only from the settings (`:1456`, `:1465`, `:1474`), and settings are read from `HostConfig` at open (TESTED: only an open with the timer turned on made the seal succeed). Friday's shorter words would have let a caller wait for a `TriggerOff` that waiting never clears.
- "no window open" for `SealInProgress`: true, but the row does not say that the window is the caller's own and is closed by `seal_finish` (§6's steps table does: `seal_finish` = steps 3 and 4). A caller that only waits would wait forever. A careful reader of §6 does not; Note N-r2-5.

**The sentence under the table**
- **The interleave hook is test-only.** `test_hooks` is `#[cfg(test)]` (`host.rs:1909-1912`), and its only consumer is `seal_finish`'s `#[cfg(test)]` block (`:1631-1649`). Every other path to a `SealStale` answer is in section 3: none in a normal build (the anchor compare is `session.rs:2290`; the only other path is the red `seal_interleaved`, `:1186`). So `SealStaleTwice` (`:1714-1717`) and the re-plan's `Err` (`:1707-1710`) cannot be reached as built. TRUE.
- TESTED: a `git archive` copy of dbc9c0a with ONE planted line, `test_hooks::interleave_next();` in `seal_begin` (non-test code; `logs/hookplant.diff`, `1546a1547`), own target `target/hookplant`:
  - `cargo build --locked --offline -p coagent-audit-host` → **exit 101**, `error[E0433]: cannot find module or crate 'test_hooks' in this scope --> crates/coagent-audit-host/src/host.rs:1547:9`
  - `cargo build --release …` → **exit 101**, the same error
  - control: the same copy, `cargo test --locked --offline -p coagent-audit-host --lib --no-run` → **exit 0** (`Compiling coagent-audit-host …/hookplant/…`, `Finished 'test' profile`)
- The pointer "§6, 'The window'" is TRUE: docs `:191-197` say "In the host as built a plan cannot go stale (nothing reaches the member in the window); the retry is reached in the tests through a test-only hook (`cfg(test)`, not in any build of the library)".
- One word of the sentence is wider than the code: "the `Err` of a stale re-plan's step 1 or 2 inside the window". In the code the window is already closed at that point (`self.window.take()` at `:1630`). It is "inside the seal", and it removes the pending anchor (`:1708-1709`). Harmless: it cannot occur as built (wording only, part of N-r2-1).

## 6. The 13 old rows and the rest of the document (TESTED)
- `rawrows.py` (mine) compares the table as RAW bytes, with no whitespace collapsed and the leading indentation kept, from `git show 52ad858:docs/AUDIT-HOST.md` against `git show dbc9c0a:docs/AUDIT-HOST.md`. Result: `old: table at line 80, 15 lines (13 rows); new: line 80, 17 lines (15 rows)` / **`the first 15 lines byte-identical and in order: True`**. So the header, the separator and rows 1-13 are unchanged. The two added lines are row 14 and row 15, at lines 95-96.
- Controls (copies of the head's text): one byte changed in old row 5 → `False; differing line indexes: [7]`; ONE extra space inside old row 5 → `False; [7]` (this compare catches what the builder's whitespace-collapsing test cannot, the first check's N-3).
- `git diff --numstat 52ad858 dbc9c0a -- docs/AUDIT-HOST.md` → `7 0`: **0 removed lines** (the builder's claim holds). `git diff -U0` shows one hunk, `@@ -94,0 +95,7 @@`, whose 7 added lines are row 14, row 15, one blank line, and the 4 lines of the sentence. Nothing else. Against `a0379be` the file is `7 1` (the one removed line is row 14 in its addendum-1 form; `52ad858..a0379be` is `1 0`), as the builder's A2.6 says.
- The document's own counts (§12, `:294-321`) still hold: "26 rows over 23 red names" (the red script's `ROWS` array has 26 entries over 23 distinct names, counted at the head), and the list of the lane's test files is unchanged and still true (the round added no test file). §3 states no row count. §13 "A plan cannot go stale in the host as built; the stale-retry path is exercised only by a test hook" agrees with the new sentence.

## 7. The pin (TESTED)
- `notes_docs.rs`, `git diff 52ad858 dbc9c0a` (`16 2`). The two removed lines are the `NEW_ROWS` doc comment (`/// The rows lane AUDIT-HOST-NOTES adds (items 1 (a)-(c), 4 and 5).`) and `const NEW_ROWS: [&str; 5] = [`, replaced by a 3-line comment and `[&str; 7]`. Added: rows 14 and 15 as `NEW_ROWS[5]` and `[6]`; `const TEST_ONLY` (the sentence); one `check()` clause (`!collapse(doc).contains(TEST_ONLY)` → `Err("addendum 2: …")`); one mutated case ("the test-only sentence removed"). No assertion and no older case was changed or removed.
- Extracted from the three blobs by program: `OLD_ROWS` 8 at all three heads, **byte-identical 52ad858 vs head: True**; `NEW_ROWS[0..5]` **byte-identical: True**; `NEW_ROWS[5]` differs from `a0379be`'s (the widened row 14, as addendum 2 asks). Each of the 15 pins equals its document row exactly, raw, once the 2-space indentation is taken off (15 of 15).
- **At the head** (`head/`, my clean worktree, own target `target/head`, `Compiling coagent-audit-host … /qahn2/head/…`): `cargo test --locked -p coagent-audit-host --test notes_docs -- --nocapture` → **exit 0**, `docs check: Ok(()); table rows Ok(15)`; the in-test mutated copies each `Err` (an added row removed → row 15 missing; an old row altered → `row 3 of 9145840 not kept`; moved → `row 2 …`; a row added → `the table has 16 rows, not 8 + 7`; the sentence → `addendum 2: the sentence on the two test-only seal answers is missing`; §11 → `N-b: …`); `test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.01s`.
- **My own mutated documents.** Each is a `git archive` copy of dbc9c0a with ONE change made by `mutate.py` (its `diff` against the head's document is in `logs/mut_<name>.diff`). Each has its own target `target/mut_<name>`, and each log shows `Compiling coagent-audit-host v0.0.1 (/private/tmp/claude-501/qahn2/mut/<name>/…)`. Command: `cargo test --locked --offline -p coagent-audit-host --test notes_docs -- --nocapture`.

| Mutation | Exit | First panic / result |
|---|---|---|
| row 15 removed | **101 RED** | `notes_docs.rs:108:5`, `left: Err("m-1: an added row is missing: \| A seal call refused before it started …")` |
| row 14 put back to its `a0379be` form | **101 RED** | `:108:5`, `Err("m-1: an added row is missing: \| A seal whose step 1 or 2 failed before its window opened \| … ArchiveMismatch …")` |
| the sentence removed (its 4 lines and one blank line) | **101 RED** | `:108:5`, `Err("addendum 2: the sentence on the two test-only seal answers is missing")`. The second test also fails, at `:187:9`: its own sentence mutation changes nothing on a copy that has no sentence (the test's `assert_ne!`) |
| one byte of old row 4 (`blind` → `blinD`) | **101 RED** | `:108:5`, `Err("m-1: row 4 of 9145840 not kept, byte for byte and in order: …")` |
| a sixteenth row added after row 15 | **101 RED** | `:108:5`, `Err("m-1: the table has 16 rows, not 8 + 7")` |
| ONE extra space inside old row 4 | 0, passes | `docs check: Ok(())`: the first check's N-3, unchanged and in BACKLOG (section 8). Not graded again. My raw compare (section 6) catches it |
| (mine, extra) old row 9 (a lane row of 52ad858) moved after row 15 | 0, **passes** | `docs check: Ok(()); table rows Ok(15)`. `NEW_ROWS` are checked for presence (`rows.iter().any`), not order. This was already so at 52ad858, so it is not weaker than before (Note N-r2-6) |

- **Verdict on the pin:** no older pinned row or assertion was changed or removed. It is red on every document the brief names (row 14 in its old form, row 15 removed, the sentence removed, an old row altered, an unpinned row added). It is not weaker than at 52ad858.

## 8. BACKLOG (READ, TESTED by hash)
- `git diff --numstat 52ad858 dbc9c0a -- BACKLOG.md` → `9 0`. The file was 1,474 lines at 52ad858 and is 1,483 at the head. The head's first 1,474 lines hash to the same sha1 as the whole file at 52ad858 (`b7f84067…` both), so **nothing existing was edited**. The 9 lines are appended at the end. Open boxes go from 241 to 246 (+5).
- The 9 lines:
  - **m-2**: one box with Where / Symptom / Why deferred / Discovered (5 lines). It is in the first check's words: `host.rs:1559-1563`, `LimitsChanged { answer: Ok(Checkpoint(..)) }`, segment 0 → 0, no window, re-running works, nothing twice or lost, and the check's fix in words.
  - **N-1, N-2, N-3, N-4**: one line each, each faithful to the verdict's note. N-3 names the whitespace collapse and the fix. N-4 records both wording slips, including `host.rs:1260` → `:1290`.
  - As addendum 1 item 4 asked.

## 9. Runs at the head (TESTED, own target `target/head`, clean worktree `head/`, `git status --porcelain` empty)
- `cargo fmt --all --check` → **exit 0**, empty output (0 bytes).
- `cargo clippy -p coagent-audit-host --all-targets --locked -- -D warnings` → **exit 0**; `Compiling coagent-audit-host v0.0.1 (/private/tmp/claude-501/qahn2/head/crates/coagent-audit-host)`; `warning: unused workspace dependency 'rand_core'` / `warning: workspace (manifest) generated 1 warning` (the workspace's known manifest line); `Finished 'dev' profile [unoptimized] target(s) in 5.85s`.
- `cargo test --locked -p coagent-audit-host --test notes_docs` → **exit 0**, `test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.01s` (section 7).
- The ten-minute lib run was NOT made: item 2 holds (no source byte moved). `scripts/check.sh` and the red script were not run, by the brief (Friday's merge check runs them).
- Heavy-runs counter (`fleet/heavy_runs.sh`) before each build batch: 2, 2, 2, 2 (below 3). No run of mine took over a minute.

## 10. Names and ids (TESTED)
- The first check's `bytescan.py`, unchanged, driven by my `scanrun.py`. The words come from a words file in my work dir, kept out of this verdict: the owner's first name, surname and handle; the mail domains and the mail service; the drive and the workspace roots; the three coordinators' names; the client names; the home roots and the scratch root; the tool-call, session, message and request id prefixes; the brain folder; the vault folder; the commit identity's domain. 25 words, 35 spellings.
- **The round's 32 added lines** (`git diff -U0 52ad858 dbc9c0a`, `+` lines): **0 hits.** Whole at the head, `docs/AUDIT-HOST.md` and `notes_docs.rs`: **0 hits**. The short name as a whole word: 0 in every input.
- `BACKLOG.md` whole at the head: 50 hits, ALL in lines 241-1408, which are older than this lane's appended lines (1475-1483) and unchanged by the round (section 8): a coordinator's name ×45, the scratch root ×2, the tool-call id prefix ×3. None is in a changed line; recorded, not graded (outside the round).
- Controls, same words: a copy of `notes_docs.rs` with one planted line (a workspace path and a surname), and a planted binary (NUL and 0xff bytes around a first name and the drive name) → `5 hits`, exit 1. The short name planted → 1.

## 11. The enumeration as a table (item 3; `host.rs` at dbc9c0a; "normal" = no `cfg(test)`, no red cfg)
| Where | Answer | Reachable in a normal build | Row / sentence that names it | Builder's row (A1.2/A2.5 #) | Agree |
|---|---|---|---|---|---|
| `seal_begin` `:1543` | `Err(Closed)` | yes (host closed by an earlier `LandedUnknown`, or by row 11) | rows 4 and 11 (`Closed` after; open the host again) | rows 4 and 11 (#1) | yes |
| `seal_begin` `:1545` | `Err(SealInProgress)` | yes (`seal_begin` or `seal` while the caller's own window is open; TESTED) | row 15 | row 15 (#2) | yes (N-r2-5) |
| `admit` `:1456`, `:1465`, `:1474` / `:1460`, `:1470`, `:1491` | `Err(TriggerOff(t))` / `Err(NotDue(t))` | yes (TESTED) | row 15 | row 15 (#3) | yes |
| `admit` `:1450`; `begin_steps` `:1564`; `plan_and_file` `:1592`; `mutate` `:1243` | `Err(Closed)` | no (a member is in place there) | — | "unreachable" (#1) | yes |
| `begin_steps` `:1557` (before step 0) | `Err(AnchorNotSaved)` / `Dir(..)` of `anchors/limits` (or `anchors` at its sync) | yes (an EARLIER change's unwritten write) | row 1's retry column; row 13's answer and retry by shape | row 1, same shapes as 13 (#4) | yes (N-r2-2) |
| step 0 `:1559-1562` ← `mutate` `:1262` | `Err(LandedUnknown)` | yes (drawn: in the first check's 131 row-4 answers) | row 4 | row 4 (#5) | yes |
| step 0 ← `mutate` `:1288` | `Err(LimitsChanged{answer: Ok(Checkpoint)})` | only if a re-open changes the limits in force (gate r5's N1 state) | row 8 → row 1: m-2, BACKLOG by ruling | row 8 → 1, m-2 (#6) | yes |
| step 0 ← `mutate` `:1288` | `Err(LimitsChanged{answer: Err(Reopened{landed})})` | as above | row 8 → row 3 (right: the seal again) or row 2 (the m-2 family) | row 8 → 2 or 3 (#7) | yes |
| `begin_steps` `:1569` | `Err(AnchorNotSaved)` / `Dir(..)` of `anchors/limits` | yes (drawn: 75) | row 13 | row 13 (#8) | yes |
| `plan_and_file` `:1594` | `Err(Audit(..))` of `seal_export` (`NothingToSeal`, `NotAuthor` for a wrong `id`, store or encode errors) | yes (`NothingToSeal` drawn 291; TESTED) | row 14 (and row 10) | row 14 and 10 (#9) | yes (N-r2-4) |
| `:1603`; `write_archive` `:1412-1413` | `Err(Audit(ExportTooLarge))` | yes in principle (a bundle over 64 MiB); not provoked | row 14 (parenthetical) | row 14 (#10) | yes |
| `write_archive` `:1416` (`archive_names`) | `Err(Dir(Io{"list the archive", name: "archive"}))` | yes in principle; not drawn | row 14 by its case words | row 14 as "`archive/seg-…`", line `:1417` (#11) | yes (N-r2-1, N-r2-7) |
| `write_archive` `:1421-1422` | `Err(Dir(Bounds("archive attempts for one segment")))` | only after 10,000 files of one segment | row 14 by its case words | row 14, line `:1423` (#11) | yes (N-r2-1) |
| `write_archive` `:1429`/`:1437`, `:1431` | `Err(Dir(..))` of `archive/seg-…`, or of `archive` at its sync | yes (drawn: 349; TESTED 5 ops) | row 14 (62 name the directory: by case words) | row 14 (#11) | yes |
| `write_archive` `:1432-1433` | `Err(ArchiveMismatch("archive/seg-…"))` | yes in principle (a read-back that differs); not provoked | row 14 (parenthetical) | row 14, line `:1434` (#12) | yes |
| `plan_and_file` `:1609` | `Err(Dir(..))` of `anchors/pending`, or of `anchors` at its sync | yes (drawn: 353; TESTED 5 ops) | row 14 (69 name the directory: by case words) | row 14 (#13) | yes |
| `begin_steps` `:1580` | `Ok(SealBegun)` | yes | success (the window is open) | — (#14) | yes |
| `seal_finish` `:1630` | `Err(NoSealInProgress)` | yes (TESTED); never from `seal` | row 15 | row 15 (#15) | yes |
| `seal_finish` `:1651`, `:1681`, `:1751` | `Err(Closed)` | no (nothing in a window drops the member) | — | "unreachable" (#16) | yes |
| `seal_finish` `:1691` | `Ok(SealReport{limits: None})`, host open | yes | success | success (#17) | yes |
| `seal_finish` `:1683` failed, `:1691` | `Ok(SealReport)`, host closed after | yes (drawn: 13) | row 11 | row 11 (#17) | yes |
| `seal_finish` `:1684-1687` | `Ok(SealReport{limits: Some})` | only if a re-open changes the limits in force; the first check's hook test | row 12 | row 12 (#18) | yes |
| `seal_finish` `:1740` | `Err(LandedUnknown)` | yes (drawn: 33 seals) | row 4 | row 4 (#21) | yes |
| `seal_finish` `:1752-1758` | `Err(SealCommitFailed{segment_now})` (any commit error, also `NotAuthor` for a wrong `id`) | yes (drawn: 325) | row 7 | row 7 (#22) | yes |
| `seal_finish` `:1752-1758` | `Err(LimitsChanged{answer: Err(SealCommitFailed)})` | only in the N1 state | row 8 → row 7 | row 8 → 7 (#23) | yes |
| `seal_finish` `:1707-1710` | the re-plan's step 1 or 2 `Err` after `SealStale` | **no**: test hook `:1631-1649` (`#[cfg(test)]`) or red `seal_interleaved` `:1186` only | the sentence | the sentence (#19) | yes |
| `seal_finish` `:1714-1717` | `Err(SealStaleTwice)` | **no**: as above | the sentence | the sentence (#20) | yes |
| Red-gated, listed apart: `:1483`, `:1568`, `:1597`, `:1608`, `:1614-1616`, `:1654-1662`, `:1680`, `:1685`, `:1722-1728`, `:1736-1738`, `:1746-1750`, `:1186` | the broken variants' answers | no (`build.rs` refuses a red name in a release build; no red cfg without the variable) | — | left out by the builder too | yes |
| `#[cfg(test)]`, listed apart: `:1006-1010` (re-offer hook), `:1631-1649` (interleave hook) | test-only shapes | no (TESTED for the interleave hook: E0433 in dev and release, section 5) | — | — | yes |

**Result: every answer that `seal_begin`, `seal_finish` or `seal` can give in a normal build is named by a row, by a row's answer or retry column, or (for the two test-only answers) by the sentence. The builder's enumeration and mine agree on every row.**

## 12. Findings
**No Blocker. No Major. No Minor.** Every Major criterion of the brief was checked and none holds:
- The table names every answer (sections 3, 4, 11; the schedules: 0 unnamed).
- No new word is false where following it would record a change twice, lose one, leave a seal the owner asked for unfinished, or retry something that cannot succeed. The two closest cases are N-r2-4 and N-r2-5 below, each argued.
- No old row moved (section 6, raw bytes). No code moved (section 2). The pin is not weaker and fails on every document the brief names (section 7). Nothing of the owner's is in a changed line (section 10).

Repro prefix for my tests: `COAGENT_AUDIT_HOST_SCRATCH=/private/tmp/claude-501/qahn2/scratch/t5 QA_CLONE=/private/tmp/claude-501/qahn2/t5 CARGO_TARGET_DIR=/private/tmp/claude-501/qahn2/target/t5 python3 -B /private/tmp/claude-501/qahn2/bin/run.py cargo test --locked -p coagent-audit-host --lib -- tests::qahn2_rows --nocapture --test-threads 1`. `t5/` is dbc9c0a plus my uncommitted `src/tests/qahn2_rows.rs` and its `mod` line; the copy is in the gate folder.

**Notes** (none blocks; each is a suggestion for the owner or a later lane; none is a ruling of Friday's reopened)
- **N-r2-1 (wording; row 14's parenthetical, docs `:95`).**
  - Row 14 says "`Dir(..)` of its `archive/seg-…` file or of `anchors/pending`". The two directory syncs answer with the DIRECTORY's name (`Dir(Io{"sync the directory", name: "archive"})` / `name: "anchors"`): 131 of the 702 schedule answers. So do the archive listing (`:1416`, `name: "archive"`) and the attempts bound (`:1422`, no name).
  - The row names all of them by its case words ("step 1 or 2 failed … answers that `Err`"), and its retry is right for them (TESTED, 10 of 10). A careful reader who takes the parenthetical as the whole list could not place a `Dir` naming `anchors`. Worse, that same `Dir` shape (`name: "anchors"`) is also what row 13's `anchors/limits` write gives at its directory sync. Both rows say "the seal, once", so the action is the same either way.
  - The sentence's "inside the window": at `:1707` the window is already taken (`:1630`); "inside the seal" would be exact.
  - Repro: `python3 -B -I /private/tmp/claude-501/qahn2/bin/table.py /private/tmp/claude-501/qahn/logs/diff_head.log | tail -2`.
  - Fix in words: "`Dir(..)` of its `archive/seg-…` file, of `anchors/pending`, or of the `archive` or `anchors` directory".
- **N-r2-2 (wording; older than the round).** A seal can be refused at its START (`:1557`) by an EARLIER change's unwritten anchor or limits (`AnchorNotSaved`, or the `anchors/limits` write's `Dir`). Row 1's retry column names that answer and the rule ("refuses the next change … until a save succeeds"). Row 13 gives the same answer and the right action, but its case says "step 0 left". Not drawn as a seal answer in the schedules, which start every seal clean. Fix in words: row 13's case "a seal refused before its plan because a write is unwritten (its own step 0's, or an earlier change's)".
- **N-r2-3 (wording; row 14's retry column).** "Its step 0 makes no second checkpoint" is exact only when nothing new was recorded since the failure. With a new own record in between, the retry's step 0 checkpoints the NEW event (TESTED: `seal_begin (its checkpoint's own seq) Ok(Some(4)); own checkpoints inside the window 2; seal_finish Ok(1)`). That is correct behaviour, not a duplicate. Row 13 already uses the exact words: "no second checkpoint of the same events". Repro: the test above, line `QAHN2 R14 new records between`.
- **N-r2-4 (`NothingToSeal` and "the seal, once"; argued not Major).**
  - Rows 14 and 10 permit ONE retry of a seal's `Err(Audit(..))`. For a plain `NothingToSeal` (nothing new since the last seal), that retry answers `NothingToSeal` again: TESTED, the folder byte for byte unchanged both times, own checkpoints 1 → 1.
  - §6 step 1 says "`NothingToSeal` is reported, not retried" (about the host itself).
  - Not Major: the column says what a caller MAY retry, bounded to once; the retry writes nothing, records nothing twice and loses nothing; and when `NothingToSeal` comes from a failed step 0, the one retry DID succeed (the first check: 291 of 291). The parenthetical "`Audit(..)` of `seal_export`" is addendum 1's own wording.
  - Fix in words (owner's choice): "(`NothingToSeal`: nothing to do until something new is recorded)".
- **N-r2-5 (row 15, `SealInProgress`; argued not Major).** "The seal when the condition holds (no window open …)" does not say that the open window is the caller's own, opened by its `seal_begin` and closed only by its `seal_finish` (§6's steps table says `seal_finish` = steps 3 and 4). A daemon that only waits would wait forever. A careful reader of §6, which the wiring lane must read for the window anyway, does not. TESTED: `seal_finish` then closes it (`Ok(1)`) and the next seal succeeds (`Ok(2)`). Fix in words: "(no window open: `seal_finish` closes one; …)".
- **N-r2-6 (test strength; older than the round).** `notes_docs` checks the five lane rows of 52ad858 (`NEW_ROWS[0..5]`) for PRESENCE, not order: old row 9 moved after row 15 → green (TESTED, `logs/mut_row9_moved_last.log`). It was the same at 52ad858, so not weaker; the rows ARE in order today (section 6, raw). It belongs with N-3 in BACKLOG: compare the table's raw lines, in order, against `OLD_ROWS ++ NEW_ROWS`.
- **N-r2-7 (the builder's STATUS, wording only).** In A1.2 a few line numbers are one off: `archive_names` `:1417` → `:1416`; the bound `:1423` → `:1422`; the read-back `:1432` → `:1431`; `ArchiveMismatch` `:1434` → `:1433`. The listing and the bound are grouped under "`Dir(..)` of `archive/seg-…`" although they name the directory or nothing (N-r2-1). No row changes.

**Friday's rulings held against the source** (not reopened): ruling (b) of addendum 2, the widened row 14, the sentence, and the builder's changed retry words for row 15 (section 5: the change is TRUE and better than the proposed words). m-2 and N-1 to N-4 in BACKLOG as ruled (section 8).

**May the next lane wire the daemon's seal handling by this table alone?** Yes, with one known exception: m-2 (BACKLOG). In gate r5's N1 state, a seal answered `LimitsChanged{answer: Ok(Checkpoint)}` has NOT run although rows 8 → 1 read "done", so the wiring lane must read that BACKLOG entry. Notes N-r2-1, -4 and -5 help but are not needed for safety.

## 13. What was NOT checked
| Not checked | Why / what stands instead |
|---|---|
| `ArchiveMismatch`, `Audit(ExportTooLarge)` (encode or the 64 MiB bound), `Dir(Bounds)` and the archive listing's `Dir` as live answers | Not provoked (no cheap injector for a read-back mismatch, a 64 MiB bundle or 10,000 files); READ only (sections 3, 11). Row 14 rests on my reading there |
| `LimitsChanged` of any shape from a seal; `Ok` with `limits: Some` | Not drawn by the schedules (defaults in force); the first check's hook tests stand (its sections 6, 11 m-2); gate r5's real N1 state not constructed |
| `Closed` from `seal_begin` as a live answer | READ (rows 4 and 11); not provoked in this round |
| The fault schedules re-run at this head | Not repeated by brief: the code is the same blob (section 2); the first check's head log was re-mapped (section 4) |
| `scripts/check.sh`, the red script, the crate's ten-minute lib run, `coagent-audit`'s tests | Not run by brief (no source moved; Friday's merge check runs them) |
| The merge with the moved `main` (`1b1ac44…`; `BACKLOG.md` changed on both sides) | Friday's one merge-in step after this verdict |
| A real stop or power loss; any disk but this Mac's APFS; Windows at run time | As the first check (its section 12) |
| The SealStale path's behaviour (the re-plan, `SealStaleTwice`) | Reachable only through the test hook; its absence from dev and release builds TESTED (section 5); its behaviour is the crate's own window tests' |
| Whether `seal_finish` with an `id` other than the member's really answers `SealCommitFailed{cause: NotAuthor}` | READ only (`session.rs:2286-2288` → the `Err(e)` arm) |

## 14. End state
- My processes: none left running (`ps`, 12:27: no process of mine). My files: only under `/private/tmp/claude-501/qahn2`: my clone `repo/`; its worktrees `head/`, `h52/`, `ha0/`, `t5/` (with my two uncommitted test files and their `mod` lines); `git archive` copies `hookplant/`, `hookref/`, `mut/*` (7); targets, logs, scratch, scan inputs. Also the copies in `gate_audit_host_notes_r2_tests/`, this verdict and my STATUS file. The first check's work dir was only read (its `diff_head.log` and nothing else); the builder's worktree, targets and scratch were not touched.
- The project folder: only read (git read verbs with `--no-optional-locks`; its repository's `git status --porcelain` empty at the end), plus my STATUS file.
- Nothing deleted by me. My tests do not call the crate's `scratch_done`, so their scratch folders stay under my work dir. One shell command of mine (the one that wrote `table.py`'s edit) began with `cd /private/tmp`, against the brief's "never use `cd`". It changed only the shell's directory and touched nothing.
- End, 2026-11-25 12:27, `git ls-remote gh audit-host-notes main`: `dbc9c0a9fad3b03fff3d723bf2e66eb376ac1913` (**did not move**), `main` `1b1ac447041ea3df56384cd4547561ec076a3130` (as briefed).
