VERDICT: GO WITH NOTES — head 73ce645c614f98643c3500fe4f1167f0dc9ff671

# QA-AUDIT-NEXT-A-R2: the short second check of branch `audit-next-a` (the fix round only)

Checked head `73ce645c614f98643c3500fe4f1167f0dc9ff671`: one commit whose only parent is the first check's head `d79ae1ca194fbe354ca8be594b9c76325f1b6eb0`. The lane's base is `5e11609cee1cb483bd006547e9092d49522691cc`. Main (`5cab5e42df6cb3db05f3d38c7ba973beafd044b2`) was not merged in and not judged.

Brief: `briefs_drafts/2026-11-26_coagent_QA-AUDIT-NEXT-A-R2_check_brief.md`, read whole. Also read whole: the fix-round list (`…_AUDIT-NEXT-A_ADDENDUM-1_fix_round.md`, items A to E); the first verdict's lines 1-60 and 339-411 (plus its rows `:207-208` for the limit); the builder's STATUS from `## ADDENDUM 1 (fix round)` (`:132`) to the end (`:177`); and `git show 73ce645`, every line and the commit message.

**Where I worked.** Work dir `/private/tmp/claude-501/qan2`:
- my own clone `c` at the head, plus a worktree `o` at `d79ae1c`;
- my own tools folder (two links, as the coordinator's merge check makes them);
- empty target dirs `t` (head, normal), `tr` (head, AW-7 red) and `to` (`d79ae1c`, AW-7 red), plus `tsj` for a scratch program outside the project.

Every script and log is in `gate_audit_next_a_r2_tests/` beside this file. TESTED means I ran it; READ means I read it. The builder's figures are CLAIMS unless I re-made them.

## BLUF (for a phone)

- **AW-7 is now named right every time I ran it.** In 20 of 20 runs on my own red build of the head, the first failure was the lane's own message at `aw_disk.rs:180`. The same 20 runs on the old head hit the test helper once, so the control fired. The code backs this up: after the planted fault the daemon never again answers `"ok": true`, and the new check rejects every other answer.
- **The round changed nothing else.** No product byte changed, only the three allowed paths, and in `aw_disk.rs` only the one assertion. The new check accepts strictly fewer answers than the old one.
- **Still open for a later lane:** the six records the round adds (m-1, N-1, N-2, N-3, N-5, N-9), plus the limit it states (a daemon whose engine stops while the process stays, or whose IPC hangs, still fails first inside the helper). This check adds five Notes, all about wording and none about the product.

## Proofs

| Proof | Result (TESTED unless marked) |
|---|---|
| Section 0 | `ls-remote` (GitHub, deploy key): `audit-next-a` = `73ce645c…`, `main` = `5cab5e42…`. `git log --format='%H %P' d79ae1c..73ce645` = one line, `73ce645c… d79ae1ca…`. Builder STATUS 177 lines, ending `Head: 73ce645c614f98643c3500fe4f1167f0dc9ff671` / `READY FOR QA AUDIT-NEXT-A r2` (no backticks). |
| Scope (a) | Product-path diff **0** bytes (control **19495**). Name-only = the three paths (control 11). 16 protected/kept blobs equal, and each sha256 equals the lane brief's value. `aw_disk.rs` differs (`a5c3e4c` → `4974ea7`). |
| M-1 (b), head | **20 of 20** first panic lines `the daemon stopped answering after a disk failure (R-6)` at `aw_disk.rs:180:9`. 0 runs compiled `coagent-daemon`. One panic per run, all with seed `000000a0d15c0007`. |
| M-1 (b), control `d79ae1c` | 19 lane message, **1 helper line** (run 14: `common/mod.rs:625:43: ctl inbox_read: no response`). The control fired. |
| Normal build, `aw_disk` once | `1 passed` (37.77 s). Reach line byte-equal to the builder's STATUS `:151`. |
| `serde_json` (c) | `1.0.154` in `Cargo.lock` at the head. `v["ok"] == true` is true only for JSON `true` (source READ; my program over 9 cases TESTED). |
| Script row (c) | `RED (as required): the daemon stopped answering after a disk failure (R-6)` (panic at `aw_disk.rs:180:9`); `final clean run: green (81 test binaries; ignored under rulings: 2)`; exit 0, 1741 s |
| Records (e) | Quote equal to the lane brief `:154` and to C-18 (`CLARIFICATIONS.md:176`). 1 + 7 removed lines all in `d79ae1c`, 0 in the base. Against the base: 0 removed lines, every base line kept in order. Word changes only inside the three named sentences. |
| Names (g) | 0 hits in 44 added lines and in the commit message; the planted control was caught. Card ids: 0 added (BACKLOG 5 and 5). |
| fmt, clippy (h) | Both exit 0. Clippy printed only the workspace's known `unused workspace dependency rand_core` warning. |

## (a) Scope (TESTED; `harness/prop_a.sh`, `logs/prop_a.log`)

- `git diff d79ae1c 73ce645 -- crates/coagent-daemon/src crates/coagent-daemon/build.rs scripts crates/coagent-audit crates/coagent-audit-host | wc -c` = **0**. Control, the same paths over `5e11609..d79ae1c` = **19495**.
- `git diff --name-only d79ae1c 73ce645` = `BACKLOG.md`, `crates/coagent-daemon/tests/aw_disk.rs`, `docs/M0-OUTCOMES.md`. Control, `5e11609..d79ae1c`: 11 paths.
- Numstat `d79ae1c..73ce645`: `32 1`, `1 1`, `11 7`. Against `5e11609`: `53 0`, `11 0`, `16 0`. All equal to the drafter's read.
- `git rev-parse <sha>:<path>` is equal at both SHAs for each of these:
  - `tests/common/mod.rs` (`ce7e402`);
  - the 13 protected files and the 3 kept files (`release_audit.rs`, `ipc.rs`, `dn_help.rs`);
  - `src/audit.rs` (`52f03e5`).

  Each one's sha256 (first 16 hex) equals the value in the lane brief's section 3. The two audit crate trees are equal (`7808b4dd…`, `c90e44c2…`).
- Controls: `aw_disk.rs` DIFFERS; a path that does not exist is reported `MISSING`, not hashed.
- **PASS.**

## (b) M-1 closed, by my runs (TESTED; the heart; `harness/loop20.sh`, `logs/head20/`, `logs/old20/`)

**Build.** `tr` was built once with `COAGENT_RED_AW=seal_error_ends_the_engine cargo build --workspace --bins --locked`. The log shows `RED CONTROL BUILD: coagent_red="seal_error_ends_the_engine"` (`logs/build_tr.log`). Then one `--no-run` build of the test target with the same variable (`warm.log`), so that no counted run compiles anything.

**Runs.** Twenty runs, one after another, each with the variable set: `cargo test --locked -p coagent-daemon --test aw_disk -- --exact every_disk_failure_gets_a_row_and_nothing_is_recorded_twice`. Each exited 101, and 0 of the 20 logs show `coagent-daemon` compiling. The first panic line of each run:

| Run | Head `73ce645` (target `tr`) | Control `d79ae1c` (target `to`) |
|---|---|---|
| 1-13 | `aw_disk.rs:180:9: the daemon stopped answering after a disk failure (R-6)` (each run) | the same (each run) |
| 14 | `aw_disk.rs:180:9: the daemon stopped answering after a disk failure (R-6)` | **`common/mod.rs:625:43: ctl inbox_read: no response`** |
| 15-20 | `aw_disk.rs:180:9: the daemon stopped answering after a disk failure (R-6)` (each run) | `aw_disk.rs:180:9: …(R-6)` (each run) |

Each of the 40 logs carries its own line (`summary.txt` in each folder quotes each run's line). Every run used seed `000000a0d15c0007`, so runs differ only in timing.

**Head: 20 of 20 are the lane's message. PASS.**

**The control fired, at a lower rate than the first check saw.** It hit the helper in 1 of 20 runs, against 3 of 8 in the first check. At the first check's rate, twenty clean runs by luck have a chance of about 1 in 12,089. At my own control's rate (1/20), the chance is (19/20)^20 ≈ 0.36, so on this machine the twenty runs alone are weak proof. The PASS therefore also rests on this READ of the mechanism, which leaves no other route:
- The red variant sets `self.quit = true` while it answers the failing seal (`engine.rs:1319-1323`).
- The engine loop breaks right after that request (`engine.rs:543-545`) and handles no further request.
- So any later `status` gets one of two answers:
  - no answer, because the queue is closed: `ctl_raw` gives `None`;
  - the `daemon stopping` error, because the reply channel was dropped (`engine.rs:715-723`).
- The new check rejects both (property c). The only route left to a helper line is the `ctl_raw` call at `:176` hanging 60 s during shutdown. No run of mine (3-5 s each) and none of the builder's came near that.
- The builder's twelve logs (`tools/tmp/an/04c82a/r2_aw7/run1..12.log`, READ) show 12 of 12 at `aw_disk.rs:180:9` with the lane's message, so their claim holds.

**Normal build** (`t`, no RED line in its log): the test passes once (`1 passed`, 37.77 s). Its reach line, which is byte-equal to the builder's STATUS `:151` (compared by program):
`AW disk reach: steps 261; seal answers {"10/14 (NothingToSeal)": 19, "13": 6, "13 or 14": 11, "7": 1, "ok": 12}; refused sends 30 by row {"1 (the anchor of the last change is unwritten)": 9, "10": 21}; acknowledged sends 52; peer messages 29 sent, 29 received`.

## (c) The changed assertion (READ + TESTED, then one script row)

- **Lock:** `Cargo.lock:1080-1081` at the head pins `serde_json` `1.0.154` (the coordinator's ruling 4: confirmed).
- **Source** (`serde_json-1.0.154`, READ):
  - `v["ok"]` uses `Index for str`: `Value::Object(map) => map.get(self)`, anything else `None`. `ops::Index` returns `Value::Null` when there is no hit (`value/index.rs:83-89`, `:178-190`). It never panics.
  - `Value == bool` is `partialeq_numeric! { eq_bool[bool] }` → `eq_bool` = `value.as_bool() == Some(other)` (`value/partial_eq.rs:23-25`, `:97-103`).
  - `as_bool` is `Some(b)` only for `Value::Bool(b)` (`value/mod.rs:708-713`).
- **TESTED** (`sj/main.rs`, the same expression against `serde_json =1.0.154`, offline). The new check is true for `{"ok":true}` only. It is false for `{"ok":false,…"daemon stopping"}`, a missing `ok`, a non-object (`[true]`, `true`), `{"ok":"true"}`, `{"ok":1}`, `{"ok":null}` and `None`. On every one of the 9 cases, new ⇒ old held. **True exactly for a JSON boolean true: PASS.**
- **Strictly stronger:** `Option::as_ref().is_some_and(p)` implies `is_some()`. Every answer the new check accepts, the old one accepted, and the `daemon stopping` reply is now refused.
- **Nothing else changed:** `git diff -U0 d79ae1c 73ce645 -- …aw_disk.rs` shows 1 line removed and 1 added (`:180`). The `assert!(alive(pid), …)` line after it is unchanged. No wait was added.
- **Script row (TESTED, last, counter first; `logs/red_row.out`):** counter 1 before it; no other `red-controls-daemon.sh` in the process list. `RED_ONLY='^seal_error_ends_the_engine$' bash scripts/red-controls-daemon.sh` through my wrapper on `tr`, my own tools folder (so its log folder `qan2/tools/tmp/m1-daemon-red` is mine alone), 14:52:00 to 15:21:01. The row's log shows the `RED CONTROL BUILD` line and the first panic line `crates/coagent-daemon/tests/aw_disk.rs:180:9: the daemon stopped answering after a disk failure (R-6)`. Output: `AW-7 seal_error_ends_the_engine aw_disk … RED (as required): the daemon stopped answering after a disk failure (R-6)`; `final clean run: green (81 test binaries; ignored under rulings: 2)` (81 `test result: ok`, 0 `FAILED`); exit 0. The same as the builder's `r2_red.out`. **PASS.**

## (d) The limit (READ)

- **The added sentence is true as worded.** It appears in BACKLOG (the M-1 line), in M0-OUTCOMES and in the commit message: a daemon whose engine stops while its process stays, or whose IPC hangs, still fails first inside the helper with its 60 s line. That matches the first verdict's `:357` and its measured rows p9 and p10 (`:207-208`: `common/mod.rs:608:17: coagentd ctl status on a did not answer within 60 s`). `ctl_raw` lives in `tests/common/mod.rs` (the helper module, protected). **PASS.**
- **The "twelve runs" sentences** (BACKLOG, M0 and the commit message) claim twelve of twelve, which is what the builder's twelve logs show (READ above). They do not claim a rate, or anything beyond the red control. **PASS.**
- **D-1** (the comment at `aw_disk.rs:173-175` at the head; the drafter wrote 174-176): the comment says the status is asked first "so a daemon that stopped fails on this message and not inside the inbox helper". In the limit cases it fails inside `ctl_raw`'s own 60 s line, not on "this message". The comment is literally right only about the *inbox* helper. Per the coordinator's ruling 1: **Note R2-N1.**

## (e) Items B and C (TESTED by program; `harness/prop_e.py`, `logs/prop_e.log`)

- **The owner's words.** `'No: end the session and pair again'` is a character-for-character substring of the lane brief's line 154 and of `CLARIFICATIONS.md` line 176 (C-18). It is the only hit in each file. The text before it in both sources is `…retry-create-log-1126: a — `, so the quote leaves out the option letter and dash `a — ` and the card's decision prefix. That is a fair cut: the words quoted are the answer itself. The quote is in M0-OUTCOMES once, and in the commit message once (across a line wrap, by whitespace-normalised search).
- **Attribution.** "unreachable in production" is attributed to "the independent check" in both files, and it matches the first verdict's S-1 (`:44`: "`_ => T_NOTHING` … is unreachable in production").
- **Removed lines.** The 1 BACKLOG line and 7 M0-OUTCOMES lines removed `d79ae1c → head` all exist in `d79ae1c`; 0 of them exist in `5e11609`. Against `5e11609` both files show 0 removed lines. Every base line is kept in order: BACKLOG 1683 of 1683, M0 251 of 251 (by `wc -l`). The base M0 is also a byte prefix of the head's.
- **Word-level comparison** of the paragraph (old `d79ae1c:255-263`, 188 words; new `head:255-267`, 259 words; `difflib` over whitespace-split words). Every changed run:
  1. "the log is still never created twice in one session (the owner's ruling)." → "there is no second attempt to create it in the same session (the owner's ruling of 2026-11-26: 'No: end the session and pair again')." (item B sentence)
  2. "written), and keeps the old wording when it cannot tell." → "written); the old wording is kept only as a defensive fallback, which the independent check found unreachable in production." (item C sentence; the drafter's "written), and keeps" → "written);" is part of this)
  3. "AW-7 now fails on its own message." → "AW-7 now checks for a successful status answer … all twelve failed on that check's own message; a daemon whose engine stops while its process stays, or whose IPC hangs, still fails first inside the test helper with its 60 s line (the helper is a protected file)." (item C sentence)

  No change falls outside these three sentences. **PASS.**
- **D-4.** The BACKLOG R2-N3 replacement adds the reason in brackets ("own seq is never below the last own checkpoint, and with unreadable figures no seal is called"). That restates S-1 (`:44`) faithfully: `commit_head`/`restore`/`seq()` give the first half, `drive_seal` the second. It is not wider than the verdict. The STATUS (`:158`) quotes it without naming S-1 as its source, while the BACKLOG line itself attributes the finding to "the independent check". **Note R2-N3** (attribution in STATUS only; no effect).
- **Line counts.** The STATUS's "1684 of 1684 … 252 of 252 … 248 of 248" (`:159`) counts the empty element after the final newline; `wc -l` gives 1683, 251 and 247. True in substance. **Note R2-N5.**

## (f) Item D: every new sentence against the verdict (READ)

Product texts were checked against `audit.rs` at the head (blob `52f03e5`, equal to `d79ae1c`).

| Entry | Sentence (short) | Verdict line | Judgement |
|---|---|---|---|
| M-1 | AW-7 could still go red through the helper (a quitting daemon's "daemon stopping" reply counted as an answer) | `:353`, `:356` | true |
| M-1 | Fixed: asserts a status answer with `"ok": true`; twelve red runs, twelve on that message | `:362`; builder logs | true (my 20 agree) |
| M-1 | Still not covered: engine stops while process stays, or IPC hangs → helper's 60 s line; helper protected | `:357`, `:207-208` | true |
| m-1 | title: the pointer names no cause | `:364` | true |
| m-1 | Where: `T_NOT_SEALED`, `T_NOT_SEALED_REOPEN`, `T_SEGMENT_UNKNOWN`, `T_NOTHING_UNWRITTEN` | `:365` (`audit.rs:113-114`, `:122`, `:127-128`, `:137-138`) | true: the four constants sit at those lines at the head, each ending "fix the cause (see status.audit), then give the command again" |
| m-1 | Symptom: rows 13 / "13 or 14" / could-not-write with 0500 folders → `state: "on"`, `reason: null`, `last_seal` repeats; 18 of 18 | `:366` | true |
| m-1 | Why deferred: product text; the lane brief's proposal built as proposed; no product byte in the round (the coordinator's ruling) | `:365`; addendum §2 | true |
| m-1 | Two fixes: keep the host's error in `status.audit` ("a fixed description and the host's answer, as `reason` does"), or drop the pointer | `:368` | true; a paraphrase of "a fixed description plus the `Debug` form" (`reason` is `format!("…({e:?})")`, `audit.rs:682`); looser but not wrong. Note R2-N2 |
| N-1 | title: two wording points | `:377-380` | true (the third point, the fallback sentences, was fixed by item C) |
| N-1 | Where: `owner_seal_steps`; the comment above `T_NOTHING` (`:117`) | `:378` | true: `audit.rs:117` reads "It stays the text whenever the daemon cannot tell which of the two causes applies." |
| N-1 | Symptom: "nothing new" with nothing ever filed; the comment describes a case that never produces `NothingToSeal` | `:379`, S-9 (`:52`), S-1 | true |
| N-1 | Fix in words: "nothing to file yet"; fallback defensive | `:380` | true |
| N-2 | title, Where (`T_CREATION_FAILED`, `audit.rs:140-141`), Symptom measured both ways, reason names the cause, fix in words | `:381`, S-8 | true |
| N-3 | title: no host → `Closed`, one call counted | `:382` | true |
| N-3 | Where: the `None` arm of `seal_once`, `:938` | `:382` | true (`audit.rs:938` = `None => (Err(HostError::Closed), true),`) |
| N-3 | Symptom: `calls: 1` with no seal; unreachable as wired (`seal_once` only after a figures read on a present host) | `:382`, S-3 (`:46`) | true |
| N-3 | Why deferred: not a finding (the coordinator's ruling); "for a later lane: answer it without counting a call" | `:382` | first half true; **the fix is the builder's own, not the verdict's** (N-3 gives none). Note R2-N2 |
| N-5 | title; Where `created` (`Err` of `AuditHost::create`, `audit.rs:665-684`); "tests/an_create.rs reaches only the `ensure_dir` refusal" | `:384`, S-7 | true. The `an_create` clause is wider than the verdict's words, but READ true: its two prepares (`audit/` 0755, `audit/` a plain file) both fail `ensure_dir`'s check at `audit.rs:634`, and its third test is the restore path |
| N-5 | Symptom: reached by the check with an immutable folder; behaved as built | S-7 (`:50`) | true |
| N-5 | Why deferred: the round changed only its one test line (the coordinator's ruling) | addendum §2 | true |
| N-9 | title; Where `restored` → `open_now` (`NotCreated`); quote "this session's log is missing or empty; it is never created again for a session that existed" | `:391` | true (the quote is byte-equal at `audit.rs:758`) |
| N-9 | Why deferred: base behaviour kept as the lane brief required; a later lane may add the sentence | `:391` | true |

- **D-2.** The unchanged M0 sentence says "three 'give the command again' texts now say to fix the cause first", while m-1 names four. Both are true:
  - three of the four constants existed at the base (`T_NOT_SEALED`, `T_NOT_SEALED_REOPEN`, `T_SEGMENT_UNKNOWN`: one `const` line each at `5e11609`), and those three changed;
  - `T_NOTHING_UNWRITTEN` is new in this lane (0 at the base).

  A reader may still count wrong. **Note R2-N4.**
- **D-3.** The two points above: one fix that the verdict did not give, one paraphrase. Neither is false about the product. **Note R2-N2.**
- **PASS** (no `false` row).

## (g) Names and ids (TESTED; `qa_scan.py`, `logs/g_*.txt`)

- **Inputs.** The round's added lines: 44, from `git diff -U0 d79ae1c 73ce645`, `+` lines without the `+++` headers (= 32 + 1 + 11). Also the commit message.
- **Word list.** Given on the command line only: 39 words plus 4 whole-word ones. It covers:
  - coordinator seat names;
  - the owner's other clients and their projects;
  - person, machine and account names;
  - drive and temp path roots;
  - mailbox names.

  The scan's own id and UUID patterns also ran.
- **Results.**
  - Added lines: **0 hits**. Commit message: **0 hits**.
  - Control: the commit message with one planted line → 6 hits (3 shown by the tool's tail), and the planted card id was caught by the card pattern.
  - Card ids `[a-z]+-c2c-[a-z0-9-]+`: added lines 0; commit message 0; BACKLOG 5 at `d79ae1c` and 5 at the head; M0 0 and 0.
  - Rulings are named "the coordinator's ruling" / "the owner's ruling" in the added lines.
- **D-5 (a fact, not a finding):** the commit's author and committer are the owner's GitHub account (the users.noreply address), the same as the base's own commits (`5e11609`, `e049cec`, `ed14cce`; the coordinator's ruling 6). The message ends with the tool's co-author line.
- **PASS.**

## (h) fmt and clippy (TESTED, short; `logs/fmt.log`, `logs/clippy.log`)

- `cargo fmt --all --check` → exit 0, no output.
- `cargo clippy -p coagent-daemon -p coagent-mcp --all-targets --locked -- -D warnings` on `t` → exit 0. Its only warning is the workspace manifest's `unused workspace dependency rand_core` (known, as in the builder's STATUS).
- **PASS.**

## Findings

No Blocker, Major or Minor.

**R2-N1 (Note): the comment above the changed assertion still promises more than holds (D-1).**
- **Where:** `crates/coagent-daemon/tests/aw_disk.rs:173-175` at `73ce645`.
- **What:** the comment says "a daemon that stopped fails on this message". In the stated limit (engine stopped with the process alive, or IPC hung), the first line is `ctl_raw`'s own 60 s line, inside the helper. The records state the limit; the comment does not.
- **Repro:** `git -C <clone> show 73ce645:crates/coagent-daemon/tests/aw_disk.rs | sed -n 173,175p`.
- **Fix in words:** in a later lane that owns the file, add "(an exit or a 'daemon stopping' reply; a hung IPC still fails in `ctl_raw`'s 60 s line)". The coordinator's ruling 1: a Note.

**R2-N2 (Note): two record sentences go beyond the verdict's words (D-3).**
- **Where:** `BACKLOG.md` at the head: the N-3 entry's "for a later lane: answer it without counting a call", and the m-1 entry's "a fixed description and the host's answer".
- **What:**
  - The first verdict's N-3 (`:382`) gives no fix; this one is the builder's own.
  - The verdict's m-1 (`:368`) says "a fixed description plus the `Debug` form".
  - Neither sentence is false about the product.
- **Repro:** `git -C <clone> show 73ce645:BACKLOG.md | grep -n 'without counting a call\|the host.s answer'`.
- **Fix in words:** mark the N-3 fix as the lane's suggestion, and write "the `Debug` form of the host's error", when the entries are next touched.

**R2-N3 (Note): the R2-N3 bracket's source is not named in STATUS (D-4).**
- **Where:** builder STATUS `:158`.
- **What:** the bracketed reason restates S-1 (`:44`) faithfully. BACKLOG attributes it to the independent check; the STATUS quote does not say so.
- **Repro:** `sed -n 158p coagent/5_Project_History/STATUS_AUDIT_NEXT_A.md`.
- **Fix in words:** none needed in the product or the records.

**R2-N4 (Note): "three" texts vs the four named in m-1 (D-2).**
- **Where:** `docs/M0-OUTCOMES.md:263` (a sentence the round did not change; the line was re-wrapped) vs the `BACKLOG.md` m-1 entry's Where.
- **What:** both are true (three changed old texts plus one new text), but side by side they read as a contradiction.
- **Repro:** `git -C <clone> show 73ce645:docs/M0-OUTCOMES.md | grep -n 'three "give'` and `git -C <clone> show 5e11609:crates/coagent-daemon/src/audit.rs | grep -c '^const T_NOTHING_UNWRITTEN'` (→ 0).
- **Fix in words:** a later lane may write "three existing texts, and the new could-not-write text,…".

**R2-N5 (Note): the STATUS's "kept in order" counts are one higher than `wc -l`.**
- **Where:** builder STATUS `:159`.
- **What:** it says 1684, 252 and 248; `wc -l` gives 1683, 251 and 247. The trailing empty element of `split('\n')` was counted. True in substance; my own walk agrees on "all kept".
- **Repro:** `git -C <clone> show 5e11609:BACKLOG.md | wc -l`.
- **Fix in words:** none.

**Observation on the brief, not on the lane:** the twenty-run statistic assumes the first check's 3-in-8 rate. On this machine the old head hit the helper 1 time in 20, so the twenty runs carry less weight than the brief computes. Section (b) gives the READ that carries the rest.

## What was NOT checked

| Not checked | Why / where it rests |
|---|---|
| The whole suite, `scripts/test-daemon.sh`, the 16-row red run, the whole red script, `scripts/check.sh` | by the brief (the coordinator's merge check runs the check script and the whole red script on the merged head) |
| Main `5cab5e42` merged into the branch | not merged, not judged (the brief) |
| The first check's Minors and Notes (m-1, m-2's substance, N-1..N-9) as facts | not re-judged (brief §3); the new entries were judged only as restatements of the verdict (f) |
| The engine-stops-process-stays and hung-IPC cases by a run of mine | READ against the first verdict's measured p9/p10 (`:207-208`) and `ctl_raw` (`common/mod.rs:576-621`); not re-planted |
| A forty-run control | not needed: the first twenty fired (the coordinator's ruling 3) |
| The builder's heavy-counter and scan discipline | not graded; my own figures are above |
| Windows | `--audit` is refused there; no run |

**My heavy runs:** the counter read 1 before each one (build `tr`; the head's twenty; build `to` plus the control's twenty; build `t` plus the test plus clippy; the script row). One heavy run at a time.

**Process note:** one of my first shell commands contained a `cd` into my own clone, against the brief's "never `cd`". It failed to produce output, because zsh did not split a variable, and it changed nothing. The commands were re-run from a bash script with no `cd` (`harness/prop_a.sh`).

**Processes and files:** no daemon, test binary or cargo process of mine is left (process list checked after the script row). The only matching processes were a watcher of the coordinator's on my STATUS file, not mine. Everything I made is under `/private/tmp/claude-501/qan2` and the two named folders (this verdict and `gate_audit_next_a_r2_tests/`). In the project I wrote only my STATUS file, and used only git read verbs (`--no-optional-locks`) on its repository. Nothing was deleted, and no file flag was set. Nothing was deployed, pushed, merged or paid for; no model run.
