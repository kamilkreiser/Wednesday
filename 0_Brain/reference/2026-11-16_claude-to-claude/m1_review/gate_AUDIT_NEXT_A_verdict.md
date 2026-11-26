VERDICT: NO GO — head d79ae1ca194fbe354ca8be594b9c76325f1b6eb0

# QA-AUDIT-NEXT-A: the one independent check of branch `audit-next-a`

Checked head `d79ae1ca194fbe354ca8be594b9c76325f1b6eb0` (one commit) against the base `5e11609cee1cb483bd006547e9092d49522691cc` (the AUDIT-WIRE merged head). Main (`1c025c443a0b18ebf85349bc8ced6d0633da2e64`) was not merged and not judged. Brief: `briefs_drafts/2026-11-26_coagent_QA-AUDIT-NEXT-A_check_brief.md`, read whole. Also read whole: the lane brief (`2026-11-26_coagent_AUDIT-NEXT-A_brief.md`); the builder's STATUS (131 lines); every line of `git diff 5e11609 d79ae1c`; the four new test files, with `an_after.rs` lines 47-317 checked by program; the first verdict's findings, Notes, red table and NOT-checked table; the second verdict's tasks 2, 3 and 5, R2-N1 to R2-N4 and "Carried"; `CLARIFICATIONS.md` C-17 to C-19.

Work dir `/private/tmp/claude-501/qana`:
- My own clone `c` (head) and worktree `b` (base).
- My own tools folder (links, as Friday's merge check uses).
- Empty target dirs: `t` (head), `tb` (base), `tr` (red run), `ts` (my harness copy `s`), `tp1`..`tp10` (one per plant `p1`..`p10`), `t7` (AW-7 reruns), `tf`/`tf2` (build-script runs).

Every script, harness and planted diff, with its logs: `gate_audit_next_a_tests/` beside this file. TESTED means I ran it; READ means I read it. The builder's figures are either re-made by me or marked CLAIM.

## BLUF (for a phone)

- **With the log switch off the daemon is exactly as before.** My before/after run of every command in every state (two runs per build) shows 0 differences except the random invitation. No line of the daemon's source outside `src/audit.rs` changed, and no byte of either audit crate.
- **Every product fix is closed by my own runs, and each goes red when reverted.** That covers the kept creation reason, the re-open before the seal, the row-11 text, the two "nothing to seal" texts (checked against the store itself), `limits: null` and the three "fix the cause" texts: seven reverts, seven reds on the builder's own assertions.
- **One given item is NOT reliably closed: AW-7 (N-10/R2-N4).** In my red run, AW-7 again went red through the helper (`ctl inbox_read: no response`), not the new message; in 8 reruns, 3 more times. The new check accepts the quitting daemon's "daemon stopping" error reply as an answer. By the brief's section 3 this is a Major, so **NO GO**. The fix is one line in a test; the product is not affected.
- **The new texts are true where they speak, with two wording gaps and one paraphrase:**
  - "fix the cause (see status.audit)" points to a `status.audit` that shows `state: "on"` and no reason in every case I made (Minor).
  - "end it and pair again to keep one" fails while the cause is still there (Note).
  - "never created twice (the owner's ruling)" is a different rule from the owner's words (Minor).
  - No changed older test checks less.

## Proofs (each TESTED unless marked)

| Proof | Result |
|---|---|
| Section 0 | `ls-remote`: `audit-next-a` = `d79ae1ca…`, main = `1c025c44…`; `git log --format='%H %P' 5e11609..d79ae1c` = one line `d79ae1ca… 5e11609c…`; merge base of head and main = `5e11609`; builder STATUS 131 lines, ends `Head: d79ae1ca194fbe354ca8be594b9c76325f1b6eb0` / `READY FOR QA AUDIT-NEXT-A` |
| Scope | 0 paths outside the eleven (control with one exclusion dropped: 1); numstat 11 paths, 1380 added, 48 removed (= coordinator's) |
| Daemon source outside `audit.rs` | `git diff … -- crates/coagent-daemon/src ':(exclude)…audit.rs' \| wc -c` = 0 (control 16136) |
| Audit crates | trees `7808b4dd…` and `c90e44c2…` (and host `src` `a0d4ef99…`) equal at both SHAs |
| Switch absent, old vs new | 122 labels, 121 same, 1 different = `invited: a invite` (random secret and port; differs between two runs of ONE build) |
| Reverts (b) | 7 of 7 red on the builder's own assertion, each plant's log shows `coagent-daemon` compiling |
| Red run (16 rows) | 16 `RED (as required)`, 0 `STILL GREEN`, final clean run green (81 binaries, 341 passed, 0 failed, 2 ignored); **AW-7's first panic line was the helper's** |
| Own enumeration of `owner_seal_steps` | 76,608 cases, 0 failures |
| Run grid (h) | 72 cases, 0 failures; crash sweep 18 cases, 0 failures |
| Full suite | see (j) |

## Section 1a: the drafter's S-points, judged

| S | Judgement (where shown) |
|---|---|
| S-1 | TRUE. Own seq can never be below the last own checkpoint. READ at the base: `commit_head` refuses a head unless `author_seq == seq()` (`chain.rs:448-463`). `restore` pushes a head only if its event is held (`chain.rs:515-550`). `seq()` only grows (`chain.rs:179-181`). With unreadable figures no seal is called (`drive_seal`). So `_ => T_NOTHING` (`audit.rs:513`) is unreachable in production. My harness drives it (seq < checkpoint: 324 cases, old text). BACKLOG's "the old text stays when neither can be read", M0's "keeps the old wording when it cannot tell" and the commit message's "when they show neither" describe a case that never produces `NothingToSeal`. Note N-1. |
| S-2 | TRUE and measured. After rows 13 (`anchors/` 0500) and "13 or 14" (`archive/` 0500), `status.audit` is `state: "on"`, `reason: null`: 18 of 18 such replies in the grid, plus runs n_vi and n_vii. The could-not-write text (n_ii) likewise. Minor m-1. |
| S-3 | TRUE, unreachable as wired. My harness: a `seal_once` answering `(Err(Closed), true)` gives row `4 or 11 (closed earlier)` and `calls: 1` with 0 real seals. Its text is "opened again; fix the cause…" or "could not be opened again" by the re-open. READ: `seal_once` runs only after a figures read succeeded on a present host, and the host is `None` only after a failed `open_now`, whose following read fails first. Not a finding (coordinator's ruling 3). Note N-3. |
| S-4 | TRUE, unreachable as wired. The pre-seal `open_now` logs, clears `unavailable` and may set `status.audit.limits`. In my enumeration the `limits` closure was called after the answer and before any re-open in all 39,024 cases where it was called. Note N-4. |
| S-5 | TRUE of the builder's model. My enumeration draws re-open before and after separately: "member-less, opened before, failed after" 504 cases, 0 failures. It keeps "no member" and "segment unknown" one state. Note N-4. |
| S-6 | TRUE and worse than stated: part of Major M-1 (the race) and (d). |
| S-7 | Closed by my run (iii), `chflags uchg`: reason `the log could not be created (Dir(Io { what: "create the directory", name: "root", kind: PermissionDenied }))` + the sentence, every time. No lane test reaches this branch. Note N-5. |
| S-8 | TRUE. With the cause still there, pairing again gives the same failure and the same sentence. With it removed: `state: "on"`, a created log and a landed seal. Note N-2. |
| S-9 | TRUE. A seal right after pairing (own seq 0, no checkpoint at all) says "nothing new since the last filed point" (run n_iii; also every grid case with `store/` 0500 from pairing on). Note N-1. |
| S-10 | The claim is TRUE in that run. My store read of the same case (n_ii) shows own seq 1 and checkpoints `[]`, so no checkpoint was written at own seq. The test itself does not read the store. Note N-6. |
| S-11 | `pub struct Figures` (the `figures` closure's value type, needed by items 2 and 3) and `Audit::new`'s one field line (Rust needs the new field initialised) are the only items outside the list. Both are needed (coordinator's ruling 4). |
| S-12 | TRUE. C-17 not appended again (stated openly); no BACKLOG line for C-19. Accepted (coordinator's ruling 5). Note N-7. |

## (a) Scope (TESTED)

- Name-only diff with the eleven exclusions: **0**; control (last exclusion dropped): **1**.
- Each of the eleven paths against the lane brief's section 3 "Owned" line:

  | Path | Owned line | Limit kept? |
  |---|---|---|
  | `src/audit.rs` | yes | see S-11 (two needed extras) |
  | `build.rs` | appends only | every base line kept in order; base 1-398 = head 1-398 byte for byte; 31 lines inside `main` + 9 after it |
  | `red-controls-daemon.sh` | rows + one comment | 5 added in one run before `)`; 0 removed |
  | the four `tests/an_*.rs` | NEW | yes |
  | `aw_disk.rs` | added lines only | 11 added in one run (`:174-184`) before `peer_got += inbox(…)` |
  | `aw_round2.rs` | `:27`, `:130`, `:132` | exactly those three lines differ (program) |
  | `BACKLOG.md` | appended | every base line kept in order; 22 added in two runs: `:1678` (under F-6) and `:1685-1705` (after the N-1..N-9 entry's last line) |
  | `docs/M0-OUTCOMES.md` | appended | base is a byte prefix of the head |

- **Protected, kept and unowned `aw_*` files:** 23 rows, sha256[:16] base = head = the lane brief's value, 0 bad. The empty hash `e3b0c442…` is in no row; `an_after.rs` at the base is reported as missing, not hashed.
- **Bodies (my own extractor, which skips strings and comments):** these eleven are SAME at both SHAs:
  - `record` fc6da583, `act_on_seal` 6c31c964, `act_on_err` fc3d9fc3, `record_ok` d860289c, `act_on_record` c0d740d3, `action` b8b12e2c;
  - `drive_seal` 6f130ea1, `segment_before_for_seal` 4886cef6, `open_now` 2422786c, `restored` 20d4566b, `red_seal` 5f3643da.
  - Control: `owner_seal`, `ensure_open`, `created`, `close`, `status` and `seal_command` are reported DIFF.
- **S-11, items a hunk touches:**
  - In the list: the constants (`T_SEALED_NOT_REOPENED`, `T_NOT_SEALED`, `T_NOTHING` comment, `T_NOTHING_UNWRITTEN`, `T_NOTHING_NEW`, `T_NOT_SEALED_REOPEN`, `T_SEGMENT_UNKNOWN`, `T_CREATION_FAILED`); `owner_seal_steps` (with its nested `nothing_to_seal`); the field `creation_failed`; `created`, `ensure_open` (and its doc comment), `close`, `seal_command`, `owner_seal`, `status`.
  - Outside it: `Figures`, `Audit::new`.
- **`unsafe` and dark-audit names in added lines:** 0. Control: a line planted into a scratch copy of the diff is found (1).

## (b) The commissioned items: own attack, then revert (TESTED)

**1. F-6.** Own two-daemon runs, `--audit` on `a` (`qa_an.py`, `logs/an_runs.jsonl`):

| Case | `status.audit.reason` after pairing, after send, after `audit_seal`, twice more, after a second send | sends | `audit_seal` | log lines |
|---|---|---|---|---|
| (i) `audit/` 0755 | `audit/ is not a directory of this user with mode 0700; this session has no audit log: end it and pair again to keep one`, all six times | both refused, `state_not_saved`, the fixed text; outbox `items: []` | `unavailable`, `calls: 0`, keys incl. `limits: null` | only `audit log unavailable: audit/ is not …`; no "missing or empty", no "audit log created" |
| (ii) `audit/` a plain file | the same | the same | the same | the same |
| (iii) `audit/` 0700 + `chflags uchg` | `the log could not be created (Dir(Io { what: "create the directory", name: "root", kind: PermissionDenied })); this session has no audit log: …`, all six times | the same | the same | only the creation line |

- **(iii) reached `AuditHost::create`'s `Err` branch.** The host's `SafeDir::open(root, "root", create)` answered "create the directory … PermissionDenied". The flag was cleared after the run: `ls -lO` shows `-`.
- **Restart after the failure:** the reason is exactly `this session's log is missing or empty; it is never created again for a session that existed` (no sentence), sends refused, the seal `unavailable`, `audit log created` 0 times.
- **Source grep:** `git grep -n 'AuditHost::create'` gives head `audit.rs:665`, `:711` and base `:543`, `:585`.
- **S-8.** (1) End, then pair again with the cause still there: the same reason and sentence, the send refused. (2) End, cause removed (0755 → 0700 / file moved aside / flag cleared), pair again: `state: "on"`, own seq 0, the send lands, the seal `ok` / `sealed: true`, `audit log created` once.
- **Reverts:**

| Item | Plant (`plants/p*.diff`) | Builder's test | First panic line | On its own assertion? |
|---|---|---|---|---|
| 1 | p1: `ensure_open`'s condition back to the base's | `an_create::a_creation_failure_keeps_its_reason` | `an_create.rs:33:5`: `after the first send: the creation's reason was not kept: {… "reason":"this session's log is missing or empty; …` | yes |
| 1 | p2: `status` reason without the sentence | the same | `an_create.rs:37:5`: `after pairing: the reason does not say what to do: {… "reason":"audit/ is not a directory of this user with mode 0700" …` | yes |
| 2 | p3: the base's `!a.done` condition | `an_after::…` | `an_after.rs:614:5`: `36 of 6000 draws broke the after-seal step; the first: says opened again without a successful re-open: …` | yes |
| 2 | p3 | `an_texts::the_seal_texts_say_what_to_do` | `an_texts.rs:138:5`: `assertion left == right failed` (the row-11 failed re-open case) | yes |
| 2 | p4: no re-open before the seal | `an_after::…` | `an_after.rs:614:5`: `3027 of 6000 draws …: a member-less host was opened again 0 times before the seal` | yes |
| 3 | p5: the old text always | `an_nothing::nothing_to_seal_says_what_it_knows` | `an_nothing.rs:42:5`: `… "action":"not sealed: nothing could be filed (…)" …` | yes |
| 3 | p5 | `aw_round2::nothing_to_seal_with_the_store_unwritable_claims_no_more_than_it_knows` | `aw_round2.rs:130:5`: `… "action":"not sealed: nothing could be filed (…)" …` | yes |
| 4 | p6: `"limits": null` removed | `an_texts::every_seal_reply_has_the_same_keys_and_a_not_sealed_row_says_what_to_do` | `an_texts.rs:211:5`: `assertion left == right failed: the unavailable reply's keys` | yes |
| 5 | p7: the three old texts back | `an_texts` (both tests) | `an_texts.rs:95:5` (the "13 or 14" text) and `an_texts.rs:192:5`: `… "action":"not sealed: give the command again" …` | yes |

Each plant is `git archive d79ae1c` plus one change to `src/audit.rs` only, built into its own fresh target dir (its `p*_bins.log` shows `Compiling coagent-daemon`).

Two earlier passes of the run-based plants were void: the tests stopped at `common/mod.rs:48` (`…/coagent not built`) because I had not built the plant's binaries. Their logs are kept under `logs/plants/void_no_bins*/` and their target dirs moved to `qana/quarantine/`. The table above is the third pass, from fresh empty target dirs.

**2. R2-N1, R2-N2.** My own harness `qa_steps.rs`, compiled against the head in the scratch copy `s`:
- Alphabet: the r2 check's builders (every `HostError` variant at least once; `Ok` with and without limits; every error and every `Outcome` inside one `LimitsChanged`, every error inside two). ENUMERATED: k ∈ {0,1,5} × up to 134 answers × member at start (yes/no) × re-open BEFORE ok/failed × re-open AFTER ok/failed × closed after (yes/no) × after-segment (k / k+1 / no member) × figures (seq = cp, seq > cp, seq < cp, 0 = 0) = **76,608 cases, 0 failures**.
- Counts: "says opened again" 1,512 (all after a successful re-open); "could not be opened again" 1,512 (all after a failed one); `sealed: true` 4,536 (all `Ok`, or a moved segment against a known one); member-less at start 38,304 (exactly one re-open before any successful read and before the seal); member at start 38,304 (no re-open before the seal); `calls` = `seal_once` calls in every case (0: 19,152, all `segment_unknown`; 1: 57,456); `limits` reported 39,024 (all after the answer, before any re-open after it); row 11 / "12 and 11" with a failed re-open 216; row 4 re-open ok after k / k+1 / no member 216 each; row 4 re-open failed 648.
- READ `owner_seal` (`:905-942`):
  - `figures` reads the member's `segment()`, `own().seq()` and `own().checkpoints().last()`'s `head.author_seq` (0 when none);
  - `reopen` = `open_now(me).is_ok()`;
  - `seal_once` makes exactly one `host.seal(me, SealTrigger::OwnerCommand, now())`.
- **The copied alphabet:** the 12 items of `an_after.rs` 47-317 that are alphabet (`Rng` and its impl, `Real`, `real`, `limits_report`, `dir_errors`, `audit_errors`, `triggers`, `plain_errors`, `outcomes`, `seal_report`, `seal_answers`) are byte-identical to `aw_answers.rs`'s. The 13th item, `enum Ev` (`:309-316`), is the model's own. Control: one planted byte in `Rng` is reported as DIFF.
- `an_after` runs:
  - Builder's seed `00a0a17e5ea10002`, 6000 draws: reach equals the STATUS's exactly (`member-less, re-open failed: 1546, … ok: 1426, row 11 failed: 14, 12 and 11 failed: 22, row 4 failed: 98, k,k 55, k,k+1 44, k,unreadable 62`; other 2733).
  - The same seed at 9000, and my seeds `5eed0f0c0ffee001` (9000) and `0123456789abcdef` (12000): all green, every reach line made (e.g. 12000: 3018 / 2936 / 52 / 48 / 237 / 99 / 100 / 103).
- Reverts: p3 and p4 above.

**3. R2-N3.** Own runs; after each, with rights back, a COPY of the session folder read by the audit crate (`qa_store.rs`, `aw_util::open_copy`):

| Run | Reply | Store (own seq, own checkpoints, segment) | Text true of the store? |
|---|---|---|---|
| (i) send, seal, seal | `ok`; then `10/14`, "nothing new since the last filed point" | 1, [1], 1 | yes |
| (ii) send, `store/` 0500, refused send, seal | `10/14`, "the log could not write its checkpoint; …" | 1, [] (no checkpoint at own seq), 0 | yes |
| (iii) seal right after pairing, no send (S-9) | `10/14`, "nothing new since the last filed point" (twice) | 0, [], 0 | nothing new: yes; "the last filed point" does not exist (Note N-1) |
| (iv) send, seal, restart, seal | `10/14`, "nothing new …" | 1, [1], 1 | yes |
| (v) `store/` 0500 with no send since the last seal | `10/14`, "nothing new …" | 1, [1], 1 | yes |
| (vi) `anchors/` 0500 before a seal after a send | row `13`, "not sealed: fix the cause (see status.audit), then give the command again"; `status.audit` on, reason null | 1, [1], 0 (step 0's checkpoint landed, the seal did not) | not a `NothingToSeal`; S-2 |
| (vii) `archive/` 0500, the same | row `13 or 14`, the same text; `status.audit` on, reason null | 1, [1], 0 | not a `NothingToSeal`; S-2 |

S-1, READ: answered in section 1a (unreachable). Reverts: p5 above.

**4. N-5.** Own runs: the `unavailable` reply has keys `action, calls, limits, row, sealed, segment` (`limits: null`), the same set as a landed seal's in the same harness (S-8(2)). Revert: p6.

**5. N-7, the seal replies' half.**
- At the base, `git grep -n -F 'give the command again'` finds `audit.rs:109`, `:114` and `:124`.
- At the head, every code string ends `fix the cause (see status.audit), then give the command again`: `:114`, `:122` (the new could-not-write text), `:128`, `:138`. The other hits are a comment (`:112`), test constants and M0 prose.
- S-2: section 1a.
- Revert: p7.

**6. N-10 / R2-N4:** see (d). **7. Records:** see (g) and (k).

## (c) `src/audit.rs`, and old head against new head (READ + TESTED)

**Hunks:** `git diff -U0` gives 21 hunks, 45 lines starting `-` and 180 starting `+` (= the drafter's). Every removed line:

| Removed (base) | Where its job went |
|---|---|
| `:109` `T_NOT_SEALED` old text | `:113-114` new text (item 5) |
| `:114` `T_NOT_SEALED_REOPEN` old text | `:128` (item 5) |
| `:124` `T_SEGMENT_UNKNOWN` old text | `:138` (item 5) |
| `:557` `Err(e) => self.set_unavailable(…)` | `:680-683`: the same call plus `creation_failed = true` (item 1) |
| `:643` doc of `ensure_open` | `:769-770`, extended (item 1) |
| `:645` `if self.host.is_none() && self.bound.is_some() {` | `:775-778`, plus `&& !creation_failed` (red AN-1 in the cfg) (item 1) |
| `:772` `let Some(host) = self.host.as_mut() else {` | `:906` `if self.host.is_none() {` (the host is taken inside the closures) |
| `:774` `};` | `:908` `}` |
| `:777-800` (24 lines: comment tail, the segment read, `before`, `drive_seal` call with the inline seal, limits, the re-open block and its text choice) | `owner_seal_steps` (`:448-517`: read, (a) re-open, `before`, `drive_seal`, limits, re-open after, (b) the text, row 4) and `owner_seal`'s closures (`:911-941`) |
| `:803-811` (9 lines: the row-4 `now_seg` read and `match`) | `owner_seal_steps` `:487-499` (same match on `figures(cx).map(segment)`) |
| `:813-815` (3 lines: closing braces, `(a, calls, was_err)`) | the function's return (`:516`) / closure ends |
| `:846` `unreadable.or_else(\|\| self.unavailable.clone())` | `:972-981`, plus the sentence when `creation_failed` (item 1) |

**Two-way match:** every behaviour change the STATUS names (`:13-27`, `:30-34`) is in these hunks, and every hunk is named by the STATUS, with four exceptions it does not mention, each investigated:
- the fake `Closed` (`:938`, S-3);
- the pre-seal `open_now` side effects (S-4);
- `Audit::new` (`:592`);
- `owner_seal`'s no-host return now uses `T_NOT_SEALED` (`:907`). Unreachable: `seal_command` returns `unavailable` before it. `red_seal` reaches it only in a red build.

None changes a reply a run can make.

**Shape of the pure function (builder `:16`, REASONED):** sound. The function receives every host step as a closure, so the property drives it without a host, and `owner_seal` keeps exactly one `seal` per `seal_once`. Note at most: the pre-seal re-open lives inside a function called "after seal" by its brief.

**Differential** (`qa_diff.py`, the r2 check's session plus full `status` values, `status.audit`, and one more `audit_seal` after the forms; two runs per build; `qa_cmp.py`; folder-rights cases by `qa_an.py`; `qa_cdiff.py`):

| Mode | Labels | Different | Volatile values dropped (why) | Attributed |
|---|---|---|---|---|
| switch absent (both daemons) | 122 | 1: `invited: a invite` | the invitation (random secret and relay port); `status` values in each state (pids, ports, times: compared with digits masked, then equal) | — (0 differences beyond the volatile invitation) |
| `--audit` on `a`, healthy | 128 | 11 | the same | all item 3: every `NothingToSeal` after a real seal now "nothing new since the last filed point" (`paired: a audit_seal {}`, `null`, `again`; `save failed: a audit_seal {}`, `null`; four `status`/`status.audit` copies of `last_seal`); 0 unattributed |
| `audit/` 0755 at creation, `store/` 0500, `archive/` 0500, healthy second seal | 64 | 19 | none (no label differed between two runs of one build) | item 1: the reason and sentence (8 labels), one fewer "missing or empty" log line at the first send (3); item 4: `limits: null` (2); item 3 (4); item 5 (2); 0 unattributed. Store reads equal at both SHAs. |

`coagent-mcp`'s `tools/list` and every MCP call, `--help` (stdout, stderr, rc), the data folder listings, outbox and inbox shapes: equal in both modes.

## (d) The two changed older tests (READ + TESTED)

| File:line | Before (base) | After (head) | Strength |
|---|---|---|---|
| `aw_round2.rs:27` | `const NOTHING_TEXT` = the old text | `const UNWRITTEN_TEXT` = the could-not-write text | used only by `:130`, `:132` at both SHAs (grep) |
| `:130` | `assert_eq!(seal["result"]["action"], NOTHING_TEXT, …)` | `assert_eq!(…, UNWRITTEN_TEXT, …)` | the same path, the same exact equality |
| `:132` | `assert_eq!(audit(&mut run, a)["last_seal"]["action"], NOTHING_TEXT)` | `… UNWRITTEN_TEXT` | the same |
| `aw_disk.rs:174-184` | — | one `ctl_raw(status)` asserted `is_some()` with the new message, then `assert!(alive(pid), …)` | added only; base lines all kept, in order (program) |

- **`aw_round2`:** the other 213 lines are byte-identical. R-3 allows exactly this. S-10: the new claim is true in that run (my store read, b3 (ii)).
- **`aw_disk`:** reach at the head equals the builder's line exactly (`steps 261; … {"10/14 (NothingToSeal)": 19, "13": 6, "13 or 14": 11, "7": 1, "ok": 12}; refused sends 30 …; acknowledged sends 52; peer messages 29 sent, 29 received`).
- **S-6, three broken daemons of my own** (plants of `engine.rs`'s AW-7 line, each in its own target):

| Plant | First panic line | Which message |
|---|---|---|
| p8: EXITS 0.3 s after answering a seal that erred | `aw_disk.rs:180:9: the daemon stopped answering after a disk failure (R-6)` | the new message |
| p9: the engine ends, the process stays (sleeps) | `common/mod.rs:608:17: coagentd ctl status on a did not answer within 60 s` | the helper's time-out |
| p10: answers the seal, then HANGS its next IPC request | `common/mod.rs:608:17: coagentd ctl status on a did not answer within 60 s` | the helper's time-out |
| AW-7's own variant (engine quits), my red run | `common/mod.rs:625:43: ctl inbox_read: no response` | **the helper** |
| AW-7's own variant, 8 direct reruns (`logs/aw7/run1-8.log`) | 5 × `aw_disk.rs:180:9: the daemon stopped answering …`; 3 × `common/mod.rs:625:43: ctl inbox_read: no response` | racy |

Why: the quitting engine drops a pending request, and the connection task then answers `{"ok":false,"error":{"code":"internal","message":"daemon stopping"}}` (`engine.rs:715-723`, READ). `ctl_raw` returns `Some` for that. The pid is still alive while the process exits, so both new assertions pass, and the helper fails at the inbox read.

So the row can never tell "exited" from "stopped answering" (the `alive` check never fires first in any of my variants). It goes red on the helper whenever the stopping reply wins. **Major M-1.**

## (e) The red script and the red run (TESTED)

- **Rows by program:** 199 at the base, 203 at the head. The 199 are byte-identical and in order. The four new rows are the lane brief's AN-1, AN-2, AN-2b and AN-3, each with six fields.
- **Run:**
  - Command: the builder's regex (copied from STATUS `:57` by program), which selects **16 rows, one per variant**.
  - Tree: my clone at `d79ae1c`, clean `git status`; `COAGENT_TOOLS=qana/tools`, own empty target `qana/tr`.
  - Before the start: heavy counter 1. The only other heavy job was Friday's merge check in its own folder.
  - Time: 2026-11-26 12:36:19 to 13:08:37, exit 0.
  - Logs name only `qana/c` (46) and `qana/tr` (96).

| Row | Variant | First panic line (my run) | Its own reason? |
|---|---|---|---|
| AW-1 | `audit_always_on` | `status key paths, idle` | yes (as r2) |
| AW-2 | `recreate_on_restore` | `a log was created over a session that existed: {"anchor_saved":true,…` | yes |
| AW-3 | `record_causer_always_local` | `the reply's record is charged to the peer's requested allowance: …` | yes |
| AW-3b | `record_full_raw` | `the stored full tier is the redacted preview` | yes |
| AW-4 | `nothing_to_seal_retried` | `NothingToSeal is never retried` | yes |
| AW-5 ×4 | `limits_changed_read_as_done`, `landed_unknown_retried`, `commit_failed_retried_blind`, `seal_err_retried` | `case 26 … read as done (m-2)`; `case 18 … seals again by itself for Err(LandedUnknown…)`; `case 88 …`; `case 6 …` | yes (as r2) |
| AW-6 | `seal_on_peer_message` | `a peer message caused a filed log` | yes |
| AW-7 | `seal_error_ends_the_engine` | **`ctl inbox_read: no response` (`common/mod.rs:625:43`)** | red, but **through the helper**: item 6 not met (M-1) |
| AW-5b | `segment_before_falls_back` | `seal: reported sealed with the segment before unknown …` | yes |
| AN-1 | `creation_reason_overwritten` | `an_create.rs:33:5: after the first send: the creation's reason was not kept: {… "reason":"this session's log is missing or empty; …; this session has no audit log: …"` | yes: the re-open after the failure replaced the reason |
| AN-2 | `row11_text_before_reopen` | `an_after.rs:614:5: 36 of 6000 draws …: says opened again without a successful re-open` | yes |
| AN-2b | `member_less_never_reopened` | `an_after.rs:614:5: 3027 of 6000 draws …: a member-less host was opened again 0 times before the seal` | yes |
| AN-3 | `nothing_text_guessed` | `an_nothing.rs:42:5: … "action":"not sealed: nothing new since the last filed point" … "segment":0` (case (b)) | yes: the F-3 falsehood |

- **The four AN logs:** each shows `RED CONTROL BUILD: coagent_red="<name>"` and `Compiling coagent-daemon` (twice: bins and test).
- **Result:** 16 `RED (as required)`, 0 `STILL GREEN`, 0 harness errors; `final clean run: green (81 test binaries; ignored under rulings: 2)`. My sum of its 81 `test result` lines: **341 passed, 0 failed, 2 ignored** (= the builder's test-daemon count).
- **Build-script refusals** (`logs/buildrs/`):
  - `COAGENT_RED_AN=no_such_name`: `build.rs:407:9 … is not a known red control`.
  - `COAGENT_RED_AN` together with `COAGENT_RED_AW=audit_always_on`: `build.rs:411:9 COAGENT_RED_AN cannot be set together with …`. The AN block's own assertion fires, because the AW block's list (`:388`) does not name `COAGENT_RED_AN`.
  - `--release` with `COAGENT_RED_AN`: `build.rs:421:9 COAGENT_RED_AN is for test builds only`.
  - All exit 101. The release refusal was the builder's UNVERIFIED item; it is now TESTED.

## (f) `build.rs`, 40 added (READ + TESTED)

- **What it does:** every build prints `cargo::rerun-if-env-changed=COAGENT_RED_AN` and a `rustc-check-cfg` line for the four names. Only when `COAGENT_RED_AN` is set does it check the name, refuse the seven other variables and a release `PROFILE`, warn, and print `rustc-cfg`.
- **What ships:** a `-vv` build of the head with no red variable (fresh target `tf`) printed only 8 `rerun-if-env-changed` lines and 8 `rustc-check-cfg` lines: **0 `rustc-cfg`, `rustc-env` or `rustc-link-*`**. Control: with `COAGENT_RED_AN=nothing_text_guessed` it printed `cargo::warning=RED CONTROL BUILD…` and `cargo::rustc-cfg=coagent_red="nothing_text_guessed"`.
- **Inputs:** the added lines read only `COAGENT_RED_AN`, the seven other red variables and `PROFILE`. The whole file has 0 `std::fs`, `File::`, `SystemTime`, `Instant`, `net::`, `process::Command` or `include_` (grep).
- **Form:** base lines 1-398 = head lines 1-398 byte for byte. The `AN_RED` list sits after `main` (`AW_RED` sits before it): a form difference, no Note needed.

## (g) The owner's three answers (READ + TESTED)

- **C-17** at `:162`, **C-18** at `:170`, **C-19** at `:178` (= the drafter's lines).
- **Each quoted text** is equal, character for character, to the lane brief's section 11 text:

  | Entry | Length | sha256[:16] |
  |---|---|---|
  | C-17 | 80 | `e417b649bbbd8785` |
  | C-18 | 88 | `d5a318a0382b556d` |
  | C-19 | 93 | `1ada44d227535ac6` |

- **Context lines:** C-17's says AUDIT-EMAIL recorded it; C-18's and C-19's say this lane did.
- **Prefix:** I hashed bytes 0 to 10,642 of the file, i.e. up to and excluding the newline before `## C-18`. These bytes end `…Yes, blank email addresses\n`, and their sha256[:16] is `d98ee38b8087859a` (= the builder's "old sha256").
- **C-18 ("a — No: end the session and pair again") against what the lane wrote:**
  - The fixed sentence (`audit.rs:140-141`, "end it and pair again to keep one") and BACKLOG's F-6 line ("Creating the log again in the same process is not built") match it. The sentence's "to keep one" is wider than the measurement while the cause remains (S-8, Note N-2).
  - The M0 paragraph ("the log is still never created twice in one session (the owner's ruling)") and the commit message ("never created twice, the owner's ruling") name the owner's ruling by a different rule. He was asked whether the log is created again after a creation that FAILED, when nothing had been created at all. A retry after a failure creates the log once, not twice. So "never created twice" does not state what he refused, and it attributes to him the older never-create-over-an-existing-session rule, which is not his. **Minor m-2** (coordinator's ruling 7: by effect).
- **C-17 against BACKLOG's N-6 line** ("the owner's ruling of 2026-11-26 is to blank email addresses in a preview"): equal in substance to "a — Yes, blank email addresses".
- **S-12:** C-19 has no BACKLOG line from this lane. The email answer was not appended a second time, which the STATUS says openly. Section 11 asked only that the answers be recorded in CLARIFICATIONS and nothing built, so it is answered for C-18 and C-19. C-17's entry already exists from another lane. Note N-7 (accepted by the coordinator's ruling 5).

## (h) Hostile parties (TESTED)

- **`aw_peer` at the head:** 2 passed. No item of this lane reads peer input (READ of the diff).
- **ENUMERATED run property** (`qa_grid.py`, `logs/grid.jsonl`):
  - Grid: 6 causes (none / `store/` 0500 / `anchors/` 0500 / `archive/` 0500 / `audit/` 0755 at creation / `audit/` immutable at creation) × sends 0, 1, 3 × seals 1, 2 × restart before the seal no/yes = **72 cases, 0 failures**.
  - Checked in every case: no `sealed: true` without a moved segment; every refused send not queued (`send_next` unchanged); calls ≤ 1; the last `NothingToSeal` text true of the store read with rights back; no `audit log created` after a restart; no number signed twice; the daemon answering at the end.
  - Distinct (row, text) pairs: `unavailable | not sealed: the audit log is unavailable (see status.audit)` 45; `10/14 (NothingToSeal) | not sealed: nothing new since the last filed point` 37; `13 or 14 | not sealed: fix the cause (see status.audit), then give the command again` 12; `ok | sealed: the log was filed away and continues` 8; `13 | not sealed: fix the cause …` 6.
  - With `store/` 0500 from pairing on, every send is refused and own seq stays 0, so the could-not-write text never appears in the grid. It appears only when a record landed before the store went read-only (b3 (ii)).
  - All 18 "fix the cause (see status.audit)" replies came with `status.audit` `state: "on"`, `reason: null` (S-2).
- **A crash between two writes** (`qa_kill.py`, SIGKILL at 0, 1, 2, 3, 5, 8, 12, 20 and 40 ms after the request, inside a seal and inside a send; 18 cases, 0 failures):
  - Kills inside a seal left `anchors/.tmp.*` (12 ms) or `archive/.tmp.*` (40 ms) and no landed seal. After the restart the first seal landed, and the following one said "nothing new", true of the store (own seq 3, checkpoints [3]).
  - Kills inside a send at ≥ 8 ms left the record landed with no reply: F-2's window, the later lane's. The text after the restart was again true of the store.
- **Can a kill separate the checkpoint write from its commit?** `session.rs:1662-1666` writes the record, then commits the head in memory. A kill between the two loses only the in-memory commit. The process is gone, and a restart rebuilds the checkpoints from the store (`session.rs:447-481`). So no running daemon can see "written, not committed", and the text after a restart reads the store's figures. TESTED indirectly: every restart case above.
- **S-3, S-4:** no input reaches either as wired (section 1a).
- **Long or odd text:** the lane adds no handling of message text. The creation reason carries a host error's `Debug` form. In my runs it held `name: "root"` and no path; the `ensure_dir` reasons are fixed strings. No reason I made held a path of any kind (my work dir's included). It now stays for the whole session.

## (i) Names, ids, fixtures (TESTED)

- **Byte scan** (`qa_scan.py`, outside the repository; 37 words plus 3 whole-word ones, given on the command line at run time, never written to a file):
  - Words: the coordinator seats' names, the owner's names and account names, this machine's host and user names, the mail domains, the home path, the drive and workspace path parts, and every other client and project folder name under the workspace's coding folder (taken at run time). Each in plain, backslash-escaped, URL-encoded and slug spellings, any case.
  - **The lane's 1,380 added lines: 0 hits.**
  - **The commit message: 1 hit**, at byte 866. That is the required attribution trailer `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`, which contains a word equal to one of the workspace's folder names. It is the tool's mandated trailer, not a project name: not graded.
  - The eleven files whole: hits only in older lines (BACKLOG 45 + 66, M0 1 + 21, red script 1; a coordinator's name and the product word), listed, not graded.
  - Controls: a scratch copy of `an_nothing.rs` with one planted line gives 7 hits; a planted binary gives 2. Both found.
- **Card ids** in the lane's added lines: 0. Control: 6 in the base `BACKLOG.md`; a made-up id planted in a scratch copy of the diff is found.
- **Commit author field:** it holds a person's name with a GitHub no-reply address. The base's own commits (`5e11609`, `e049cec`, `ed14cce`) carry the same field. A fact for the coordinator, not a finding.
- **Fixtures:** no added line holds an absolute path (`/users/|/volumes/|/private/|~/`: 0). The brief's control (the builder's STATUS) also gave 0, because the STATUS uses relative paths. My control, a line planted in a scratch copy of the diff, is found (1). The eleven paths hold no data file. The tests build their trees at run time (`tests/common`; `an_after`'s `real()` is a `MemStore`, as the alphabet compare shows).

## (j) Suite, clippy, fmt (TESTED)

- `cargo fmt --all --check`: exit 0, no output.
- `cargo clippy -p coagent-daemon -p coagent-mcp --all-targets --locked -- -D warnings`: exit 0. Only the workspace's known manifest warning `unused workspace dependency rand_core`.
- Every `an_*` and `aw_*` target once at the head: an_after 1, an_create 2, an_nothing 1, an_texts 2, aw_answers 1, aw_disk 1 (41 s), aw_lifecycle 3, aw_off 1, aw_peer 2, aw_record 1, aw_round2 4, aw_seal 1: all passed.
- Full suite: `cargo build --workspace --bins --locked`, then `cargo test -p coagent-daemon -p coagent-mcp -p coagent-audit-host --locked --no-fail-fast` at the head, 13:22:02 to 14:01:32 (heavy counter 2 at the start; my red run had ended). My sum of its `test result` lines: **92 lines, 413 passed, 0 failed, 2 ignored**, exit 0. This equals the builder's head figures. The builder's base figures (88 / 407 / 0 / 2) were not re-run: CLAIM. Log: `logs/full_test.log`.

## (k) Every claim sentence the lane wrote (TESTED)

Search words: "is stopped", "is refused", "is not sent", "cannot", "could not", "is sealed", "is recorded", "never", "not re-opened", "unchanged", "exactly", "only", "keeps", "says so" (case-insensitive), over the lane's added lines in M0, BACKLOG and the comments it added in `audit.rs`: 21 sentences, plus the drafter's candidates.

| File:line | Claim | My run | Verdict |
|---|---|---|---|
| M0 `:255` | with `--audit` absent the daemon behaves exactly as before | (c) switch-absent differential | true |
| M0 `:256-257` | keeps that failure's reason … instead of "missing or empty" at the first send | (b1) | true |
| M0 `:257-258` | the log is still never created twice in one session (the owner's ruling) | (g) | names the owner's ruling by another rule (m-2) |
| M0 `:259` | a host left without its member is opened again once before the seal gives up | (b2) harness | true (model; unreachable by run) |
| M0 `:259-260` | a seal that landed but could not reopen the log now says so | (b2) harness, p3 | true (model) |
| M0 `:261` | keeps the old wording when it cannot tell | S-1 | wider: the daemon can always tell when it gets `NothingToSeal` (N-1) |
| M0 `:262-263` | AW-7 now fails on its own message | (d), (e) | **false in 4 of 9 runs** (M-1) |
| BACKLOG `:1678` | the reason is kept with what to do; the log is not re-opened after it in the same process | (b1) | true |
| BACKLOG `:1685` | N-5: same keys; no value changed | (b4), (c) | true |
| BACKLOG `:1686` | the three texts end "fix the cause …"; constants and rows unchanged | (b5), grep | true (S-2 is about what the words promise) |
| BACKLOG `:1687` | N-10: aw_disk asserts an answer and the process before the inbox read | (d) | true as worded; the assertion accepts an error reply (M-1) |
| BACKLOG `:1697` | R2-N1: … only if that read also fails is the answer "segment unknown"; unreachable with folder rights | (b2); grid: 0 `segment_unknown` in 144 seals | true |
| BACKLOG `:1699` | R2-N2: the text is chosen after the re-open | (b2), p3 | true |
| BACKLOG `:1701` | R2-N3: equal = nothing new ("an own checkpoint is listed only after it is stored") | (b3) store reads; READ `checkpoint_now`/`commit_head` | true |
| BACKLOG `:1701` | the old text stays when neither can be read | S-1 | wider: no `NothingToSeal` comes then (N-1) |
| BACKLOG `:1701` | row, calls and the never-retried rule unchanged | (b3), AW-4 red | true |
| BACKLOG `:1689-1695` | N-1..N-9 record-only reasons (e.g. "no received input reaches" `red_seal`) | not re-run (reasons of the lane brief's table) | stated as the coordinator's rulings |
| `audit.rs:117` | the old text whenever the daemon cannot tell | S-1 | wider (N-1) |
| `audit.rs:120-126` | a stored checkpoint would have moved the own cut; an own checkpoint enters `checkpoints()` only after it is stored | READ `session.rs:1662-1666`, `chain.rs:448-463`; (b3) | true |
| `audit.rs:575-578`, `:769-770` | while `creation_failed`, the log is not opened again | (b1), p1 | true |
| `audit.rs:936-937` | `seal_once` without a host is not reachable | READ, S-3 | true |

## For the owner (plain words)

**What this lane changed in what you see:**
- When a session's audit log cannot be made, `status` now keeps the real reason all session long and adds "end it and pair again to keep one". Before, it was replaced by a misleading "missing or empty" after your first message. Fix the folder problem first: if the cause is still there, pairing again fails the same way.
- A second "file the log" with nothing new now says "nothing new since the last filed point". When the disk could not write, it says "the log could not write its checkpoint; fix the cause…". Both are true of what is on disk. The first one also appears for a session that never filed anything.
- Three "not sealed" replies now say "fix the cause (see status.audit), then give the command again". In the cases I could make, `status.audit` then says "on" with no reason, so it will not show you the cause.
- With the log switch off, nothing at all changed.

**Still open:** F-2 (a message that was refused can still be in the log), F-4, N-3, and blanking email addresses (your ruling, for a later lane).

## Findings

**M-1 — Major (by the brief's section 3: a finding the lane was given that is not closed by my attack) — AW-7 still goes red through the helper; item 6 (N-10/R2-N4) is not reliably closed.**
- **Where:** `crates/coagent-daemon/tests/aw_disk.rs:176-183`.
  - `ctl_raw(…).is_some()` accepts the quitting daemon's `{"ok":false,"error":{"code":"internal","message":"daemon stopping"}}` (`engine.rs:715-723`).
  - `alive(pid)` passes while the process is still exiting.
- **What happens:**
  - In my `RED_ONLY` run AW-7's first panic line was `ctl inbox_read: no response` (`common/mod.rs:625:43`). In 8 reruns of the same variant: new message 5, helper 3.
  - With a daemon whose engine stops while the process stays, or one that hangs its IPC, the first line is the helper's `did not answer within 60 s` (`common/mod.rs:608`).
  - So the row still cannot tell "exited" from "stopped answering".
  - The builder's STATUS (`:25`, `:68`) and M0 (`:262-263`, "AW-7 now fails on its own message") claim more than holds.
- **Effect:** on the red control's naming only. The row stays red every time, and no product behaviour is involved.
- **Reproduction:** `COAGENT_RED_AW=seal_error_ends_the_engine cargo build --workspace --bins --locked`, then `cargo test --locked -p coagent-daemon --test aw_disk -- --exact every_disk_failure_gets_a_row_and_nothing_is_recorded_twice`, several times (logs `gate_audit_next_a_tests/logs/aw7/`).
- **Fix in words:** assert an answer that is `ok: true` (e.g. `answer.as_ref().is_some_and(|v| v["ok"] == true)`, or that it carries `result`), with the same message. Optionally check `alive(pid)` FIRST, after a short wait, so an exit is named as an exit. Then re-run AW-7 several times and quote each first line.

**m-1 — Minor — "fix the cause (see status.audit)" sends the owner to a `status.audit` that names no cause.**
- **Where:** `audit.rs:113-114`, `:122`, `:127-128`, `:137-138`. The ending is the text the lane brief proposed (item 5); the lane built it as proposed.
- **What happens:** after row 13 (`anchors/` 0500), "13 or 14" (`archive/` 0500) and the could-not-write `NothingToSeal` (`store/` 0500), `status.audit` is `state: "on"`, `reason: null`, and `last_seal` repeats the same text. In 18 of 18 grid replies and in runs n_ii, n_vi and n_vii, no place the owner can see names the cause.
- **Reproduction:** `python3 -B qa_an.py <head bin> <new dir> <qa_store binary> out.jsonl n_vii`.
- **Fix in words:** keep the host's error in `status.audit` after a not-sealed seal (e.g. `last_seal.cause`, a fixed description plus the `Debug` form, as `reason` does), or end those texts "fix the cause, then give the command again" without the pointer.

**m-2 — Minor (coordinator's ruling 7, by effect) — "never created twice (the owner's ruling)" names the owner's answer by a different rule.**
- **Where:** `docs/M0-OUTCOMES.md:257-258`; the commit message's F-6 line.
- **What:** the owner answered "a — No: end the session and pair again" to whether the log is created again after a FAILED creation. A retry after a failure would create it once, not twice. The phrase states the older never-create-over-an-existing-session rule and attributes it to him.
- **Effect:** a later lane could read the owner's ruling as being about duplicates only.
- **Fix in words:** "no second attempt to create it in the same session (the owner's ruling of 2026-11-26: 'No: end the session and pair again')".

**Notes:**
- **N-1:** three wording points about the `NothingToSeal` texts.
  - The fallback `_ => T_NOTHING` (`audit.rs:513`) is unreachable in production (S-1). The sentences "the old text stays when neither can be read" (BACKLOG `:1701`), "keeps the old wording when it cannot tell" (M0 `:261`), the commit message's "when they show neither" and the comment `audit.rs:117` describe a case that never produces `NothingToSeal`.
  - "nothing new since the last filed point" is also given when nothing was ever filed (S-9, run n_iii).
  - Fix in words: say the fallback is defensive; for own seq 0 with no checkpoint, say "nothing to file yet".
- **N-2:** the F-6 sentence "end it and pair again to keep one" holds only once the cause is fixed (S-8 (1) measured). The reason before it does name the cause. Fix in words: "fix the cause, then end it and pair again to keep one".
- **N-3:** `owner_seal`'s `seal_once` answers a fake `(Err(Closed), true)` with no host (`audit.rs:938`). Unreachable as wired. If reached, it would report `calls: 1` with no seal made (my harness). Coordinator's ruling 3: not a finding.
- **N-4:** the builder's model cannot draw the states S-4 and S-5 name. My enumeration covers both, with 0 failures.
- **N-5:** no lane test reaches `AuditHost::create`'s `Err` branch (S-7). My `chflags uchg` run does, and the branch behaves as built.
- **N-6:** `aw_round2`'s changed assertion is true in its run (my store read). The test does not read the store itself.
- **N-7:** C-19 has no BACKLOG line, and C-17 was not appended again (accepted by the coordinator's ruling 5).
- **N-8 (about this brief, not the lane):**
  - the absolute-path control "the same grep over the builder's STATUS finds hits" finds 0, because the STATUS uses relative paths; I used a planted control instead;
  - `an_after.rs` 47-317 includes the model's `enum Ev` (`:309-316`), which is not part of the copy;
  - the lane brief has 159 lines by `wc -l` (said by the coordinator's ruling 9).
- **N-9 (older, not this lane's):** after a restart, the restore reason ("missing or empty; never created again") replaces the creation's real cause and carries no "what to do" sentence. This is base behaviour, kept as the lane brief required. A later lane may add the sentence there too.

## What was NOT checked

| Not checked | Why / where it rests |
|---|---|
| Anything on Windows | `--audit` is refused there; no Windows run (builder `:96`) |
| The whole red script, `scripts/check.sh`, `scripts/test-p1p.sh`, `scripts/test-daemon.sh`, the Windows kit | by the brief (Friday's merge check runs them on the merged head; ruling 6) |
| Item 2's states (member-less host at a seal; row 11 with a failed re-open) by a run | unreachable with folder rights (READ, r2 verdict; 0 `segment_unknown` replies in my 144 grid seals). They rest on my 76,608-case enumeration and the lane's property. |
| A full disk, a lying disk, power loss below the filesystem | folder rights, `chflags uchg` and SIGKILL only (coordinator's rulings 2 and 8) |
| Main `1c025c4` merged into the branch | not merged, not judged (the brief) |
| The N-1..N-9 record-only reasons as facts | they restate the lane brief's table (coordinator's rulings); not re-measured |
| The builder's heavy-counter and scan discipline | not graded; my own figures are above |

**File flags I set, and how they were cleared:**
- `chflags uchg` on `qana/w2/create_uchg/a/audit` (b1 iii), cleared by `chflags nouchg` in the harness. `ls -lOd` shows `-`.
- `chflags uchg` on `qana/wg/61..72/a/audit` (the grid's immutable cause), each cleared by `chflags nouchg` before the store read. `ls -lOd` of all twelve shows `-`.

No flag was set outside my work dir.

**Processes and files:** No daemon, relay, test binary or cargo process of mine is left. The last process check found two `cargo test` runs: one from Friday's merge check (`mcpw1`) and one from another seat's `audit-email` worktree (its working folder, by `lsof`); neither is mine. No file flag is set: `find qana -flags uchg` finds none. Everything I made is under `/private/tmp/claude-501/qana` and the two named folders (this verdict and `gate_audit_next_a_tests/`). In the project I wrote only my STATUS file. Nothing was deleted: void target dirs were moved to `qana/quarantine/`, void logs to `void_*` folders, and case (ii)'s plain `audit` file was moved aside to `audit.moved`.
