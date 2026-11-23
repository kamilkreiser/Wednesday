VERDICT: GO WITH NOTES — head 20785c3e9389ac2275cdfda2ec7fb55eb1176425

# QA-ALLOW-MEASURE-R3: short independent check of round 3 of branch `allow-measure` (fix round after the r2 NO GO)

Seat: QA-ALLOW-MEASURE-R3, 2026-11-23. Brief: `2_Project_Files/friday/briefs_drafts/2026-11-23_coagent_QA-ALLOW-MEASURE-R3_check_brief.md` (Friday).
Held to: Friday's ADDENDUM 2 (closed fix list) and the r2 verdict's F-A to F-D and N-1 to N-5.
Tags: TESTED = I ran it; READ = I read it. My scripts and outputs: `m1_review/gate_allow_measure_r3_tests/` (listed at the end).
Only round 3 (`379ceaa..20785c3`) was checked. No model run and no Claude Code session of my own were made.

## BLUF (for the phone)
1. **The compiled file is gone, and it will not come back through an ordinary commit.** It is absent from the head's tree. It is still in `379ceaa`'s tree, where my own byte scan finds it. The spike folder now ignores `__pycache__/` and `*.pyc`, and every script that imports `redact.py` turns bytecode writing off. It could come back only through a forced `git add -f`, or through a `.pyc` outside the spike folder.
2. **No text still claims more about the reviewer than was measured.** Every phrase of the old M9 claim is gone at the head; they were found on `379ceaa`, my positive control. The two M9 rows now tag the review and the order REASONED, not MEASURED. Their times and record counts match the committed captures, and Friday's sentence stands in all four places. A few older lines elsewhere still read the undocumented records by their names. That is a Note, not M9.
3. **The round changed nothing it was not asked to.** Exactly the 12 paths the builder lists changed. 0 raw files changed (233 of 233 have the same blob id). `runs.log` is still 17 lines. The four runner files differ ONLY by the added `-B` / no-bytecode setting, byte for byte. Product paths: 0 bytes. Both documents are still pure appends to main's.

One Minor finding (M-1): the new RESULT line "scan_bytes.py … 0 hits" is narrower than it reads. One plain path stays in two files by Friday's N-5 ruling, flagged below so Friday can confirm.

## Head, previous head and base proofs (TESTED)
- `git ls-remote` against the GitHub remote, with the project deploy key:
  - `20785c3e9389ac2275cdfda2ec7fb55eb1176425 refs/heads/allow-measure`
  - `3768a67d1d41b47439776657afbc114bd14bc439 refs/heads/main`
- `merge-base --is-ancestor 379ceaa 20785c3`: yes, so this is a fast-forward and no history was rewritten. `merge-base main head` = `3768a67`.
- The branch has three commits: `d76a83b`, `379ceaa` and `20785c3`.
- The builder's STATUS ends `20785c3e9389ac2275cdfda2ec7fb55eb1176425` and then `READY FOR QA ALLOW-MEASURE r3`.
- Every comparison is by SHA, in my clone `/private/tmp/claude-501/qam3/clone` (checked out detached at the head). In the project repo I used only `git --no-optional-locks remote get-url`.
- I did not open or move anything of the builder's. I only listed the scratch folder: `_side_effects/spike__pycache__from_379ceaa/redact.cpython-314.pyc` is there, 13386 bytes, the same size as the blob in `379ceaa`.

## 1. Scope (TESTED)
- `git diff --name-status 379ceaa..head` shows exactly the builder's 12 paths:
  - M `BACKLOG.md`
  - M `docs/M0-OUTCOMES.md`
  - A `.gitignore`
  - M `RESULT.md`
  - D `__pycache__/redact.cpython-314.pyc`
  - M `am.sh`
  - M `cases.md`
  - M `collect.sh`
  - M `meaning_check.py`
  - A `review_map.py`
  - M `run.sh`
  - A `scan_bytes.py`

  All but the two documents are under `spikes/U-B1-hook-allow-silent/`. Totals: 141 insertions and 28 deletions.
- `base...head`: 247 A + 2 M = 249 paths. The only paths outside the spike folder are `BACKLOG.md` (+40/-0) and `docs/M0-OUTCOMES.md` (+26/-0).
- Product paths: `git diff base...head -- crates scripts preview Cargo.toml Cargo.lock` is 0 bytes. 0 matching names appear in either name list.
- **Pure append** (`prefix_check_r3.sh`, a Python byte-prefix test adapted from the r2 check's):
  - `BACKLOG.md`: main's 194018 bytes are a prefix of the head's 202116.
  - `docs/M0-OUTCOMES.md`: main's 7359 are a prefix of the head's 10208.
  - Control: a copy of main with 1 byte flipped is detected as NOT a prefix, for both files.
  - Inside the appended part, round 3 rewrote only the lane's own lines (BACKLOG 8/3, M0-OUTCOMES 8/6), which the addendum allows.

## 2. F-A, the compiled file (TESTED)
- **Gone at the head, present before:**
  - `ls-tree -r` at the head has 0 `__pycache__` / `.pyc` paths.
  - At `379ceaa` it has `spikes/U-B1-hook-allow-silent/__pycache__/redact.cpython-314.pyc` (blob `8636f4f…`, 13386 bytes).
  - The BACKLOG entry that defers the old commit to the pre-publication sweep is present (`BACKLOG.md:1226-1230`).
- **Ignore rules:**
  - `spikes/U-B1-hook-allow-silent/.gitignore` = `__pycache__/` and `*.pyc`. `git check-ignore -v` confirms it catches `__pycache__/redact.cpython-314.pyc` and a loose `foo.pyc` in the folder.
  - The root `.gitignore` is unchanged: 0 diff bytes against main and against `379ceaa`. It has no `.pyc` rule, so the protection is folder-local.
  - Only `meaning_check.py` and `scan_bytes.py` import a local module (`redact.py`), and both set `sys.dont_write_bytecode` before the import. Running my checks with `-B` left 0 `__pycache__` in my clone.
- **My own byte scan** (`qa3_scan.py`):
  - **Method.** It is adapted from the r2 check's `qa2_scan.py`: same classes, same five forms (as is, ANSI removed, backslashes removed, URL-decoded, control bytes and NUL removed). It reads blobs straight from git (`ls-tree -r -z` + `cat-file blob`), binaries included.
  - **Extra classes.** `volume_path` catches any `/Volumes/<name>` spelling and its slug. `tmp_user_dir` catches the `claude-<uid>` scratch spelling.
  - **Workspace roots.** The project folder, the coordinator folder, the volume root and the config dir, passed in at run time and never written.
  - **Controls.** Selftest PASS: every class hits a planted line, the workspace arms hit plain, shell-escaped, URL-encoded, slug and NUL-framed forms, and a placeholder-only negative control gives 0. The planted BINARY (`planted_control.bin`, 128 bytes with NULs) hits account name 6, home 2, machine 1, workspace 2 and volume 1.
  - **At `379ceaa` (must find the `.pyc`):** `HIT __pycache__/redact.cpython-314.pyc {email 1, workspace_path 2, volume_path 1, token 3, session_uuid 1, request_id 1, message_id 1}`. 245 files, **1 binary**.
  - **At the head:** 247 committed files, **0 binary**. The 26 files with a hit are all classified by their masked shape (`qa3_scan.head.out.txt`):
    - 36 token hits: 16 sha256 values in the 4 settings-checksum files, 7 thinking-block signatures in stream files, 5 path segments, 4 long runs of text with no spaces in `pane.bytes`, and 4 synthetic selftest literals.
    - Email, uuid, `req_` and `msg_`: only the synthetic selftest literals in `redact.py:92-94` and `scan_bytes.py:26-27`.
    - `tmp_user_dir` 14: `/private/tmp/claude-501/-RUN--<case>-cwd/<ID-1>/…` in hook stdin and in M5's output path, plus RESULT.md:49. The run-folder slug and the id are already placeholders; only the uid 501 is left.
    - **workspace_path / volume_path:** `am.sh:11` and `cases.md:8`, the coordinator's `models_latest.json` path in plain form. This is r2's N-5, which Friday ruled "NOT to be done". The lines are unchanged since `d76a83b`: the same line hash at `d76a83b` and at the head, and no round-3 hunk touches them. See Note N-a.
    - account name, home path, machine name: **0**.
    - **Nothing of the `.pyc` kind is left, and nothing new was added by this round.**
- **The builder's `scan_bytes.py` (READ + TESTED):**
  - **It can see a binary.** It reads git blobs as bytes in five forms. Run from my clone, it reports `379ceaa`: "245 files (1 binary), files with a hit: 10", with the `.pyc`'s email, token, id and workspace hits.
  - **Can the synthetic-literal stripping hide a real hit?** (`strip_test.sh`, plants in copies of `redact.py`) Only for a value that CONTAINS one of the six literals:
    - A real-shaped mail (`planted.qa3@example.net`) and the config-dir path planted into a file named `redact.py` are still found.
    - `alex@example.org` and `msg_01ABCDEFGHIJKLMNtail9` are hidden. Alone in a file named `redact.py` they give `{}`; in a file with any other name they are found.
    - Real values do not contain those reserved/synthetic strings, so the practical risk is small. But the strip is keyed on the BASENAME, so it would also apply to any file named `redact.py` or `scan_bytes.py` anywhere in the folder (Note N-b).
  - **Its workspace class is narrower than the RESULT line implies.** It is `redact.py`'s: the folder four levels above the script, plus the config dir. In the builder's worktree that is the project folder. From my clone it is `/private/tmp/claude-501`: it then flags 9 files of `-RUN-` tmp paths and exits 1. It never covers the coordinator folder or the volume root, which is why it reports 0 where my scan finds `am.sh:11` / `cases.md:8` (Minor M-1).

## 3. F-B, the M9 over-claim (READ + TESTED)
- **The four times and the record counts, re-read from the committed `debug.excerpt.log` and `review_map.txt` files:**

| Run | Debug (permission lines) | `permissionDecisionMs` (Bash) | `review_map.txt` |
|---|---|---|---|
| M9-fresh-ctl | no "Skipping" line, no hook line, no positive review line | **331** | request on both assistant messages (2); context 1, for the Bash message |
| M9-fresh-hook | "Hook approved tool use for Bash, bypassing permission prompt" | **4** | request on the Bash message (and on the other one, 2); context **0** |
| M1-fresh-ctl | "Skipping auto mode classifier for Bash: would be allowed in acceptEdits mode" | **758** | context for the Bash message (1) |
| M8-fresh-ctl | same Skipping line | **532** | context for the Bash message (1) |
| M1-fresh-hook | hook approved ×2 | 6 / 7 | context 0 |
| M8-fresh-ask | hook ask ×2 | 15097 / 15307 | context for the Bash message (1) |

  Every number and record count in the two M9 rows matches. Among the auto sessions, the context record is absent exactly in the two hook-allow runs. It is also absent in the default-mode runs, where no record of either kind exists (Note N-e on "only").
- **The two M9 rows** (`RESULT.md:38-39`) are reworded as the addendum asked:
  - MEASURED is kept for the debug lines, the times, the record counts, "no dialog" and the file.
  - "that the reviewer examined this call" and "that the hook decided before any reviewer" are marked "REASONED, not measured", and both rows' Tag columns say so.
  - The rows also state that the context record follows skipped calls, and that the request record is on the hook case's message too. No dialog and the created B9.txt are as recorded in r2.
- **Friday's sentence**, "M9 shows our allow decides Claude Code's local permission step in the auto mode; whether it outranks the server-side reviewer is unmeasured, for a reviewer that approves as for one that would refuse":
  - **verbatim** in the M9-hook row (`RESULT.md:39`), in R9 (`RESULT.md:79`) and in BACKLOG entry 5 (`BACKLOG.md:1214`);
  - in **substance** in `docs/M0-OUTCOMES.md:104-106`: "M9: our allow decided Claude Code's local permission step in the auto mode (…); whether it outranks the server-side reviewer is unmeasured, for a reviewer that approves as for one that would refuse" (Note N-d);
  - UNVERIFIED item 1 (`RESULT.md:61`) is its second half.
- **Grep of the whole head** (`overclaim_grep.sh`: 19 phrases, case-insensitive, over the spike folder and both documents), with `379ceaa` as positive control:
  - On `379ceaa` the phrases are found: "approved it in the control" 2, "decided before the reviewer" 1, "Reviewed, then allowed" 1, "does review" 2, "decided first" 5, "reviewer approved" 2, "for a reviewed call" 1, "review context was sent" 5, "no review context" 5, "beats a" 3, "server reviews inside" 1, …
  - At the head they are all **0**, except four hits. I read each in its sentence:
    - `RESULT.md:22` (M1-fresh-hook, round 1): "no 'Skipping auto mode classifier' line (the hook decided first)". It is about M1's local step and names no reviewer. Note N-c.
    - `RESULT.md:37` (M8-fresh-ask, round 2, confirmed and "not to be touched" by Friday): "a server review context was sent for the Bash call (`review_map.txt`)". This is not M9, but it reads the same undocumented record by its name. Note N-c.
    - `RESULT.md:39`: "REASONED, not measured: that the hook decided before any reviewer". Correct.
    - `run.sh:208`: the comment "M9: ONE call the auto reviewer does not skip". This is the runner's pre-run intent, in a runner file that may only gain `-B`. Note N-c.
  - Also read: every other line mentioning review at the head (RESULT 13, 21, 57, 58, 61, 62, 79; M0-OUTCOMES 90, 106). None states that a reviewer examined or approved the M9 call. RESULT:62 keeps "read here as 'marked for server review' / 'review context sent'" inside UNVERIFIED. RESULT:57 ("marks every assistant message for a server review") is the same name-reading (N-c). Its count holds: every assistant record of the six auto runs has `serverClassifierRequest=yes`.
- **`review_map.py` committed:**
  - It reads a session transcript `.jsonl`. **No committed raw folder holds one**: the only committed files with the record names are the maps themselves and two `transcript_review_keys.txt`. So it cannot be re-run from committed files alone (a Note, as the brief says, N-f).
  - What I could test: transcripts of the SHAPE that `transcript_review_keys.txt` shows (`review_map_synthetic.py`, no real content). They give output identical in format and counts to the committed `M9-fresh-ctl` and `M9-fresh-hook` maps.
  - READ: one edge case. A context record with no `request` key would mark an assistant record that has no request as "context_sent_for_it=yes". No committed map shows that pattern, so no committed count is affected (N-f). Its docstring says honestly that it was run in sitting 2 as plain `python3 review_map.py`.

## 4. F-C, F-D, N-1, N-3, N-4 (READ + TESTED)
Every OLD/NEW pair in the builder's STATUS matches the diff `379ceaa..head`. Every hunk of RESULT (5), BACKLOG (2, including the new entry), M0-OUTCOMES (2) and cases.md (1) is accounted for, and the diff has no hunk without a pair.

| Item | At the head | Verdict |
|---|---|---|
| F-C | RESULT "facts met on the way" (`:58`): "no LOCAL classifier request … Whether the server-side reviewer looked at them is not shown (see M9 and its limit)". M0-OUTCOMES `:89-91` "skipped its LOCAL classifier … unmeasured (see M9 below and its limit)", `:101-102` "(no LOCAL classifier request in these runs)". BACKLOG 5 title "whether a hook allow outranks the server-side reviewer is not measured (U-B1 M1, M9)" and symptom "made no LOCAL classifier request … say nothing about the server-side reviewer; see M9 and its limit" | DONE |
| F-D | RESULT `:51` "4 to 6 builtin plugin modules per session … N = 6 in 9 runs, 5 in 4 runs, 4 in 4 runs … the same N within each case and control pair (M1, M8, M9: 6 and 6)". **My own count** (`fd_count.sh`, one "Registered 0 hooks from N plugins" line in each of the 17 committed excerpts): 6 ×9, 5 ×4 (M3-hl, M5-hl, M7-hl, M10), 4 ×4 (M3-int-r2, M6-hl, M7-int, M7-agentpane). The pairs M1-default, M1-fresh, M8 and M9 are 6 and 6. **The builder's 17-row table equals mine row for row** (diff empty) | DONE, TESTED |
| N-1 | "233 files at the addendum-2 head". I count 233 raw files at the head (and 233 at `379ceaa`) | DONE, TESTED |
| N-3 | cases.md `:60`: "under the sandbox the probe's own `ls` was refused (`other.out`: `mode=ls:`), so the target's mode bits come from the runner's `tty_record.txt`". Committed: `other.out:4` `agent-cmd target=/dev/ttys006 mode=ls:`; `tty_record.txt` `pane_tty=/dev/ttys006 mode=crw--w----` | DONE, TESTED |
| N-4 | R10 (`RESULT.md:80`) "closes that one route; other routes were not tried"; M0-OUTCOMES `:107-108` "…('Operation not permitted'); other routes were not tried" | DONE |
| N-5 | not done, as ruled | as ruled (see N-a) |

## 5. The runner files (READ + TESTED)
- READ, every hunk of `379ceaa..head`:
  - `am.sh`: 4 hunks, each `python3 -I` → `python3 -I -B` or `python3 -c` → `python3 -B -c` (`model_id`, `settings`, `allow_out`, the sampler's clock).
  - `run.sh`: 3 hunks (`m3_hook`, `ask_out`, `m10`).
  - `collect.sh`: 3 hunks (the frame cutter, `redact.py redact`, `redact.py scan`).
  - `meaning_check.py`: 1 added line, `sys.dont_write_bytecode = True`.
- TESTED (`runner_undo_B.py`): removing only those additions from each head file gives **byte-for-byte** the `379ceaa` file, for all four.
- Nothing a run does or records is altered. The two `python3` calls left without `-B` are the stub's launch line written into each `settings.json` (`am.sh:43`), where `-B` would make the rig differ from what the committed `settings.json` files record, and the M9 prompt text (`run.sh:212`), which is measured content. Both are as the builder says. `hook_stub.py` imports only standard modules, so a top-level run of it writes no `.pyc`.
- The committed captures were made by the earlier revision, and the texts say nothing to the contrary. The `.gitignore` comment "Scripts here run python3 -B" describes the scripts from now on.

## 6. Nothing else moved (TESTED)
- Raw files: `ls-tree -r` of `raw/` at `379ceaa` and at the head, as path + blob id, are **identical**: 233 = 233, and 20 raw folders at both. No new raw folder.
- `runs.log`: 17 lines, 0 diff bytes since `379ceaa`. **No model run in this round.**
- Meaning check: with every raw blob identical, "233 compared, 233 unchanged, 0 verdict-carrying lines changed" against `379ceaa` follows from blob identity alone. The `d76a83b` comparison ("14 changed only by the new rules") was confirmed by r2 and is untouched by this round (no raw file changed).

## Findings
| ID | Severity | Finding (exact place) | Suggested fix, in words |
|---|---|---|---|
| M-1 | Minor | `RESULT.md:52` (new line, N-1): "Every committed file of this folder, read as bytes with binaries included: `scan_bytes.py` (addendum 2), 0 hits." The count is literally that tool's output, but its workspace class is only "four folders above the script" plus the config dir. It does not cover the coordinator folder or the volume root. My scan finds the coordinator's plain `models_latest.json` path at `am.sh:11` and `cases.md:8`. The class also changes with where the script sits: from my clone it flags `/private/tmp/claude-501` paths and exits 1. So "0 hits" can be read as "no path of the owner's in any file", which is not so. Not a Major: the sentence names its tool, and the two hits are N-5, left by ruling | When next touched, add: "its path classes cover the project folder and the config dir only; `am.sh:11` and `cases.md:8` keep the coordinator's `models_latest.json` path (r2 N-5, left by Friday's ruling)". Give `scan_bytes.py` explicit roots, as `qa3_scan.py` does, instead of a path relative to itself |
| N-a | Note (flag for Friday) | `am.sh:11` and `cases.md:8` hold the coordinator's `models_latest.json` path in plain form (`qa3_scan.head.out.txt`). Taken literally, the brief's NO GO list ("a workspace path in any spelling … in ANY committed file at the head") catches this. I rate it a Note because Friday ruled r2's N-5 "NOT to be done" after reading it, the lines are byte-identical since `d76a83b` (the round the first check passed), this round did not touch them, and main carries the same kind of path | Friday to confirm the N-5 ruling covers the merge; otherwise put the path in an environment variable in a later round (a runner-file change, so it needs its own ruling) |
| N-b | Note | `scan_bytes.py:40-41` strips the six synthetic literals from any file whose BASENAME is `redact.py` or `scan_bytes.py`. That hides a value that contains a literal (`alex@example.org`, `msg_01ABCDEFGHIJKLMN…`; `strip_test.out.txt`), and it would apply to such a name anywhere in the folder | Match the two files by path, and strip whole literals only where they stand as quoted strings |
| N-c | Note | Lines outside M9 still read the undocumented records by their names, or speak of order: `RESULT.md:37` (M8: "a server review context was sent for the Bash call"), `RESULT.md:57` ("marks every assistant message for a server review"), `RESULT.md:22` (M1-fresh-hook: "(the hook decided first)", about the missing local "Skipping" line), `run.sh:208` (comment "ONE call the auto reviewer does not skip"). None claims that the M9 call was reviewed or approved. M8 was "not to be touched", and `run.sh` may only gain `-B` | In a later words round: "a `serverClassifierContext` record follows the Bash call" (M8); "marks … with `serverClassifierRequest`" (:57); "the hook decided the local step" (:22). Leave `run.sh:208` (runner) |
| N-d | Note | `docs/M0-OUTCOMES.md:104-106` carries Friday's sentence in substance, not word for word ("our allow decided …" with a parenthesis), while STATUS says it "stands" in the four places | Use the exact sentence if Friday wants it verbatim |
| N-e | Note | `RESULT.md:38`: the context record "is absent only under a hook allow". This is true among the auto sessions. In the default-mode runs it is absent with no hook too (0 records of either kind) | "among the auto sessions, absent only under a hook allow" |
| N-f | Note | `review_map.py` cannot be re-run from committed files (no transcript is committed). And `"yes" if q in ctx` would mark a record with no request as "context sent" when a context lacks its `request` key, though no committed map shows that | State the transcript dependency in its docstring; test `q` before the membership check |
| N-g | Note | 88 lines in 35 committed raw files carry Claude Code `toolu_…` tool-use ids (e.g. the debug excerpts). They are in no redaction class, the same kind of API-issued id as the `msg_` ids redacted in round 2. They are unchanged in this round (the raw blobs are identical) and are not in the brief's list (token, session, request, message id) | Decide in the pre-publication sweep whether `toolu_` joins the redaction classes |

**No Blocker and no Major.** The round did exactly its closed list, and nothing else changed.

## What was NOT checked
| Item | Why | Who could check it |
|---|---|---|
| Whether our allow outranks the server-side reviewer (approve or refuse) | Unmeasured by design; this round made no run | A design round, then a builder seat |
| `review_map.py` on the real transcripts | They are not committed; they are in the config dir and the builder's scratch folder, which I may not open | The builder, or a seat cleared to read the transcripts |
| That the moved `.pyc` in scratch is byte-identical to the `379ceaa` blob | I may only list the scratch folder; only the size was compared (13386 = 13386) | The builder (its STATUS gives sha256 `f908cf65…` before = after) |
| `redact.py selftest` and the settings checksums at this head | Not re-run: `redact.py` is unchanged since `379ceaa` and no run was made; the r2 check ran its own scan | - |
| The documentation quotes in RESULT | Not fetched; unchanged in this round | Any seat with web access |
| Round-1 and round-2 measurements that the earlier checks confirmed (M1-M8, M10, the re-redaction) | Out of this brief's scope; their raw blobs are unchanged | - |
| What the meaning of `serverClassifierRequest` / `serverClassifierContext` is | Undocumented | Anthropic documentation |

## Side effects (mine)
- No model run, no Claude Code session, no tmux, no process left running.
- Everything I made is in my work dir `/private/tmp/claude-501/qam3/`: the clone, `ctl/planted_control.bin`, `striptest/`, `rmap/` (synthetic transcripts), and the small `raw_P.txt` / `raw_H.txt` / `fd_*.txt` lists. Nothing was deleted.
- My scripts and outputs are in `m1_review/gate_allow_measure_r3_tests/`. In the project folder I wrote only `coagent/5_Project_History/STATUS_QA_ALLOW_MEASURE_R3.md`. I used no `cd`, and every Python call ran with `-B`.

## Files of this check (`m1_review/gate_allow_measure_r3_tests/`)
- **Scope:** `prefix_check_r3.sh` (+ `.out.txt`).
- **Byte scan (F-A):** `qa3_scan.py` (+ `qa3_scan.selftest.out.txt`, `qa3_scan.control.out.txt`, `qa3_scan.379ceaa.out.txt`, `qa3_scan.head.out.txt`, all masked).
- **The builder's scan:** `strip_test.sh` (+ `.out.txt`) and `scan_bytes_from_clone.out.txt`.
- **F-B:** `overclaim_grep.sh` (+ `.out.txt`) and `review_map_synthetic.py` (+ `.out.txt`).
- **F-D:** `fd_count.sh` (+ `.out.txt`).
- **Runner files:** `runner_undo_B.py` (+ `.out.txt`).
