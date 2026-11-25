VERDICT: GO WITH NOTES — head e049cec8f69d9e2cda4f0f4fcdb63ebd64068785

# QA-AUDIT-WIRE-R2: the second and last check of branch `audit-wire` (the fix round `510124b..e049cec` only)

Checked head `e049cec8f69d9e2cda4f0f4fcdb63ebd64068785` against the first check's head `510124b30aa62a493b91ace76b9d56ab7adffc04`. Brief: `briefs_drafts/2026-11-26_coagent_QA-AUDIT-WIRE-R2_check_brief.md` (read whole). Also read whole: the first verdict `gate_AUDIT_WIRE_verdict.md` (433 lines), Friday's fix list `2026-11-26_coagent_AUDIT-WIRE_ADDENDUM-2_fix_round.md`, sections 2 and 3 of the first check's brief, the builder's STATUS from `## ADDENDUM 2 (fix round)` (line 148) to the end (line 230), and every line of `git diff 510124b e049cec` (`audit.rs`, `aw_answers.rs`, `aw_round2.rs`, `build.rs`, the red script, `BACKLOG.md`, `docs/M0-OUTCOMES.md`). Also read: the audit host's source at `bcaf119` (`host.rs` `reopen`, `member_ref`/`member`, `apply`/`apply_now`/the P-4 path, `seal`/`seal_begin`/`begin_steps`/`plan_and_file`/`seal_finish`, `status`; `error.rs`), and the error types an item-D reason can print (`AuditError`, `StoreError`, `ProtoError`, `describe`).

Work dir `/private/tmp/claude-501/qaw2`: my own clone `c` (head), worktree `o` (`510124b`), scratch worktrees `a` (head plus my harness) and `p` (`510124b` plus the new `aw_round2.rs`); my own tools folder (links, as Friday's merge check); my own empty target dirs `t`, `to`, `ta`, `tp`, `tr`. Every script and test file I wrote, with its logs: `gate_audit_wire_r2_tests/` beside this file. TESTED = I ran it; READ = I read it. Figures of the builder's are re-made by me or marked as its claim.

## BLUF (for a phone)

- **The false "sealed" is gone.** The first check's own run, reused unchanged, now gets "not sealed" (row 7), the log's segment and seal count are unchanged, and the next command seals for real. The same run against the old head still shows the false "sealed". My answer harness: 798 seal answers with the segment unknown, 0 "sealed", 0 seal calls.
- **The round changed nothing else.** My before/after run of the same scripted session (switch off and switch on, two runs per build) differs only by item B's new "nothing could be filed" text (and the random invitation, as in round 1), which by Friday's design also appears when the store is healthy (and is true there). The decision functions are byte-identical. Scope: exactly the seven paths, no byte of the audit host crate, protected files unchanged. Red rows: 12 of 12 red (the new one on F-1's own false "sealed"), the final clean run green (335 passed).
- **Still open for the next audit lane** (all in BACKLOG, true to the first verdict): F-2 (a message refused after its record landed stays in the log), F-4 (any reply id is charged to the peer), F-6 (the creation failure's reason is lost), Notes N-1 to N-9. New Notes here are small (section Findings).

## Proofs (section 0)

- TESTED `git ls-remote` against the GitHub remote (fetched with the project's deploy key into my clone): `e049cec8f69d9e2cda4f0f4fcdb63ebd64068785 refs/heads/audit-wire`, `184b35ef17cf9865c4f9b20c721f9647233f8b98 refs/heads/main`.
- TESTED `git log --format='%H %P' 510124b..e049cec`: 2 lines, `e049cec8… ← ed14cce331867d1611d78bec53805a40565a8614 ← 510124b30aa62a493b91ace76b9d56ab7adffc04`.
- TESTED `git merge-base gh/audit-wire gh/main` → `bcaf1194ea268508cf92f135a60fe18076824a0f`. Main is not merged in; not merged and not judged by me.
- READ the builder's STATUS: 230 lines; line 229 `Head: \`e049cec8f69d9e2cda4f0f4fcdb63ebd64068785\``, line 230 `READY FOR QA AUDIT-WIRE r2`. As the brief requires.
- TESTED `git diff --numstat 510124b e049cec` = Friday's figures: `BACKLOG.md` 29 0, `build.rs` 1 0, `src/audit.rs` 104 33, `tests/aw_answers.rs` 51 9, `tests/aw_round2.rs` 215 0 (new), `docs/M0-OUTCOMES.md` 10 0, `scripts/red-controls-daemon.sh` 2 0. `src/engine.rs` not touched.
- Clean builds (TESTED, empty target dirs, heavy counter 0 before, no other red/check run): head into `qaw2/t`, `510124b` into `qaw2/to`, `cargo build --workspace --bins --locked` and `cargo test -p coagent-daemon --locked --no-run`, exit 0 all four (117 `Compiling` lines in each bins log). No compiler wrapper in the environment. The two `coagentd` differ (sha256 `84d7d080…` head, `1c70e005…` old); the head's alone contains the new row text `segment before the seal could not be read` (strings: 1 vs 0).
- One slip, said here: my first git setup command began with a `cd /private/tmp` (not into any clone or project folder; the shell reset it). Every later command used absolute paths and the wrapper `qaw2/r.sh`.

## Task 1: F-1 is closed (TESTED; the heart)

**The first check's reproduction, reused unchanged** (`python3 -B qa_causes2.py <bin> <new dir> iii2`, its file byte-identical to `gate_audit_wire_tests/qa_causes2.py`; logs `iii2_head.jsonl`, `iii2_old.jsonl`):

| Step | Head `e049cec` (`qaw2/t`) | `510124b` (`qaw2/to`, the control) |
|---|---|---|
| first seal | `ok`, sealed, segment 1 | same |
| `archive/` 0500, seal | `13 or 14`, not sealed | same |
| status before | segment 1, seals 1, own seq 3 | same |
| `store/` 0500 + root 0300: **SEAL_UNDER_TEST** | `{"action":"not sealed: give the command again","calls":1,"limits":null,"row":"7","sealed":false,"segment":null}` | `{"action":"sealed: the log was filed away and continues","calls":1,"limits":null,"row":"7 (the commit landed)","sealed":true,"segment":null}` **(the false "sealed", reproduced)** |
| `status.audit` during | `state "unavailable"`, reason `the log's status could not be read (Dir(Io { what: "list", name: "root", kind: PermissionDenied }))`, `last_seal` row `7`, sealed false | `state "on"`, every field null, `last_seal` sealed **true** |
| status after rights restored | segment **1**, seals **1** (unchanged), `last_seal.sealed` false | segment 1, seals 1, `last_seal.sealed` **true** |
| the owner's next command | `ok`, sealed, segment 2; status segment 2, seals 2 | same |

Both runs left the same orphan `seg-00000000000000000001-0000.bundle` from the failed commit (the host's documented behaviour; round 1 saw it too). Every process stopped (`left: []`).

Why it closed (READ): the head reads the segment before the seal as `host.member().ok().map(|m| m.segment())` (`audit.rs:779`), an in-memory figure. `member()` at `bcaf119` (`host.rs:1116-1123`):
```
fn member_ref(&self) -> Result<&SessionAudit<AuditDir>, HostError> {
    self.member.as_ref().ok_or(HostError::Closed)
}
/// The member, read-only (export, outgoing, anchor, status, usage, …).
pub fn member(&self) -> Result<&SessionAudit<AuditDir>, HostError> {
    self.member_ref()
}
```
It can fail for no reason but `Closed` (no I/O, no listing). In my run it was readable (1), the commit failed, the host re-opened at 1, and `1 == 1` reads "not moved": row 7, not sealed.

**My harness over the head's public functions** (`qa_alpha2.rs` = the first check's `qa_alpha.rs` adapted to `drive_seal(segment_before: Option<u64>, seal_once)`, `audit.rs:380`, plus three new tests; scratch worktree `qaw2/a` at `e049cec`, own empty target `qaw2/ta`; 5 passed; logs `qa_alpha2_b.log`, `out_alpha2.tsv`, `out_r2_seg.tsv`):
- **Segment before UNKNOWN** (`drive_seal(None, …)`): every seal answer of the alphabet, built around segments 0, 1 and 3 (the first check's 89 answers plus commit errors at k-1 and k+2, bare, inside one and inside two `LimitsChanged`), host open and closed after: `798 seal answers driven …, 0 sealed, 0 seal calls`. Every one: row `none (the segment before the seal could not be read)`, no re-open, no read, no `call_again`, no limits report.
- **Segment KNOWN** (0, 1, 3): `drive_seal(Some(k), …)` equals `act_on_seal(…, Around{segment_before: k, …})` for every answer, one call each. Row 7 (66 lines, bare and wrapped): sealed for `segment_now` ≠ k, not sealed for `segment_now` = k, at every k. Done only for `Ok` or a moved commit; m-2 never done.
- The first check's own table and rules, unchanged, still hold (89 seal and 92 record answers × open/closed; `253 owner commands, 253 seal calls`). Its `HAZARD` line still shows that `act_on_seal` given a fallen-back 0 says "sealed"; that is the pure function given a wrong input, and no caller can now give it one (task 2).
- `segment_before_for_seal(None)` is `None` and `Some(4)` stays `Some(4)` in a normal build.

A small observation, not a finding: row 7 calls a commit "landed" when `segment_now` merely DIFFERS from the segment before, so a lower `segment_now` would also read as sealed. The host cannot produce that (after a commit error the re-opened member is at k or k+1, first verdict task 1 (ii)); unchanged since `510124b`.

## Task 2: no path treats an unknown segment as a number (READ, then TESTED)

`git grep -n -F` at `e049cec` in `crates/coagent-daemon/src/audit.rs` (positive control: `unwrap_or(0)` at `510124b` hits `:366` and `:729`, the F-1 line):

| Pattern | Hits at the head | What each does when the figure is unknown |
|---|---|---|
| `segment_before` | `:74` (the `Around` field), `:319` (row 7's comparison), `:359-362` (`segment_before_for_seal` and its red comment), `:373`, `:381`, `:384`, `:392` (`drive_seal`), `:659`, `:665` (`around`), `:703` (comment), `:780` | `:384`: `None` returns `segment_unknown()` with 0 calls before any `Around` is built, so `:319` is reached only with a read figure. `:780` keeps the same `Option` for row 4. |
| `unwrap_or(0)` | `:361` (comment), `:363` (inside `if cfg!(coagent_red = "segment_before_falls_back")`, the red control only), `:407` (`now()`: the clock, not a segment) | false cfg in every normal build (no red variable). |
| `around(` | `:659` (definition), `:704` (`self.around(0)` on the record path) | the placeholder: see below. |
| `map_or(0` | 0 | (the member's own `segment()` is `map_or(0, …)` in `coagent-audit`, `session.rs:2157`: 0 there is the real segment of a log never sealed, not an unknown) |

**The record path's placeholder `self.around(0)` (`:704`).** READ `act_on_err` (`:204-354`), every arm, for `call == Record`: `around` is read at exactly one place, row 7 (`:319`), and the `SealCommitFailed` arm returns `action("none (not an answer to a record)", T_REFUSED)` at `:309-311` before reaching it when `rec`. The `LimitsChanged` arm recurses with the same `call`. `record_ok` takes no `around`. `around.closed_after` is read only in `act_on_seal`'s `Ok` arm. TESTED (`qa_r2_record_placeholder`): every record answer (the 6 outcomes and every error, `SealCommitFailed` at 0, 1, 2, 7 and `u64::MAX`, bare, inside one and two `LimitsChanged`), placeholder 0 against `u64::MAX`, both `closed_after`: `141 answers x 2 closed_after = 282 pairs, 0 differing actions`. The builder's REASONED claim (STATUS line 165) holds.

**The "guard" (`None` path).** `member()` fails only with `Closed` (quoted in task 1). **Can the seal path still reach `act_on_err`'s `Closed` arm (`:240-250`)?** No, as wired (READ). `owner_seal` calls `seal` only after `member()` succeeded in the same engine step. Inside `seal` (`host.rs:1520-1528`), `Closed` comes from `member_ref()?` at `seal_begin` (`:1543`, the member is there), after step 0 (`:1564`), in `plan_and_file` (`:1592`) and in `seal_finish` (`:1651`). Step 0's `mutate` leaves the member gone only when its re-open failed, and then it answers `LandedUnknown`, which `begin_steps` returns as it is (`:1559-1563`) before `:1564`. A `Reopened` answer means the re-open succeeded (member present). So `Err(Closed)` from `seal` cannot come; the seal path's `Closed` arm is now dead code in a normal build.

**Can the daemon hold a host whose member is gone when a seal comes?** READ: the host clears its member only in `reopen` (`host.rs:1051-1072`: `self.member = None`, and only a failure of the store open or `resolve` (`res?`) leaves it `None`). Its callers:
- `:1258` (`apply`'s P-4 path): a failed re-open answers `LandedUnknown`;
- `:1734` (`seal_finish`'s commit error): the same;
- `:1683` (`seal_finish`'s `Ok` path): a failed re-open is dropped, the seal answers `Ok` with the host closed (row 11);
- `:1383` (release): the daemon never releases.

The daemon answers each of these with a re-open:
- `LandedUnknown`, record or seal (`act_on_err` `:279-299`, `reopen: true`), at `audit.rs:706-716` (record) and `:789-814` (seal);
- row 11 by `closed_after` (`act_on_seal`, `reopen: around.closed_after`).

`open_now` either puts a freshly opened host (which always has its member) or sets `self.host = None` (`:601-641`). So after every engine step the daemon holds either no host or a host with its member. `ensure_open` (`:644-648`) re-opens only when there is no host, which is then the only case that arises. **Not reachable as wired.** No run or harness can make it without a change to the host. Judgement:
- **Note R2-N1.** If a later host change ever let the daemon keep a member-less host, `audit_seal` would answer `none (the segment before the seal could not be read)` / "give the command again" on every command and never re-open by itself; at `510124b` the `Closed` arm re-opened.
- Only a `send` would recover it (its `apply` answers `Closed`, whose arm re-opens), and `status.audit` would say `unavailable`, `the log's status could not be read (Closed)` (item D).
- It never says "sealed". Not a finding today.

## Task 3: row 4 after a re-open (TESTED + READ)

**Same number for a healthy host (READ + TESTED).** `HostStatus.segment` is `m.segment()` of the same member (`host.rs:1867`, inside `status()` `:1829`, AFTER its listings `:1835-1864`). `member()?.segment()` is that same call, without the listings. TESTED (`qa_r2_status_segment_equals_member_segment`, a real `AuditHost` in my work dir): `(status, member)` = `(0,0)` new, `(1,1)` after one seal, `(2,2)` after two, `(2,2)` after a fresh `AuditHost::open`. The two reads differ only when `status()` fails. Then `510124b` kept its row-4 text, not done; the head reads the member's segment and decides, never "sealed" against an unknown figure (`:805-811`, `(Some(s), Some(b)) if s != b`).

**By the first check's cases, reused unchanged** (`qa_causes2.py lu_seal lu_record moved_running`, head and `510124b`; logs `t3_head.jsonl`, `t3_old.jsonl`):

| Case | Head `e049cec` | `510124b` |
|---|---|---|
| `lu_seal` (`store/` 0300): seal | `{"action":"not sealed: the audit log could not be opened again; see status.audit","calls":1,"limits":null,"row":"4","sealed":false,"segment":null}` | `"the audit log was opened again and its segment read: sealed only if the segment moved"` (F-5) |
| `lu_seal`: status during and after | `unavailable`, reason `the log could not be opened (Dir(Io { what: "sync the directory", name: "store", kind: PermissionDenied }))`, `last_seal.action` = the new text | same state, old text |
| `lu_seal`: rights back, next seal | `ok`, sealed, segment 1 | same |
| `lu_record`: send 1 | `state_not_saved` / `not sent: the audit log could not be opened again; see status.audit`; log `coagentd: audit: a send was refused: row 4: not sent: the audit log could not be opened again; see status.audit` | `…could not record this message…`; log `row 4: not recorded: the message was refused and not queued; the audit log was opened again` (F-5) |
| `lu_record`: send 2 (no host) | R-6 text `not sent: the audit log could not record this message (see status.audit); nothing was queued` (true: no host to record with) | same |
| `lu_record`: rights back | next send ok, delivered, own seq 3 | same |
| `moved_running`: send | refused, R-6 text, not queued, peer did not get it | same |
| `moved_running`: `status.audit` | `state "unavailable"`, reason `the log's status could not be read (Dir(Io { what: "list", name: "archive", kind: NotFound }))` | `state "on"`, every field null, reason null (F-7) |
| `moved_running` + restart | `unavailable`, "missing or empty; never created again" | same |

- **A re-open that SUCCEEDS** after row 4 (same segment → not sealed; moved → sealed) is not reachable by a run with folder rights: the rights that fail the host's in-call re-open also fail the daemon's `open_now` (the host's `reopen` opens a subset of what `AuditHost::open` checks). The first check found the same. It rests on the READ of `:792-811` and the equality above.
- **Status after a failed re-open.** `state` is `unavailable` with the OPEN's reason (`set_unavailable`, `:630-639`), not item D's: after a failed re-open the daemon holds no host. Item D's reason appears when a host is held but its `status()` fails (`moved_running`, and task 1's run during the seal). Both are true.
- **Log lines on the seal path:** none says "opened again". The only lines are `audit log unavailable: the log could not be opened (…); every send is refused until it opens` (true) and, after the rights came back, `audit log opened (Current; segment 0; …)`. The builder added no seal log line (none existed); the existing unavailable line already tells the truth.
- **Item D's reason, path or content (READ):** it is `format!("the log's status could not be read ({e:?})")` of the `HostError` that `status()` returns. That is one of:
  - `Closed`;
  - `Audit(Store(Unavailable(&'static str)))`;
  - `normalise`'s `AuditError`. Its only free text is `ProtoError::Malformed(String)`, built from fixed words plus a line and column (`canonical.rs:37-50` `describe`; the input-echoing form is a red control only) or a fixed type name (`bytes.rs:31-45`);
  - `Dir(…)` from the archive, anchors or root listing, with names relative to the host's root (`error.rs:1-3`, `DirError::Io{name}`).

  **It holds no absolute path and no message content.** My two TESTED values name `root` and `archive` only.

## Task 4: nothing else changed (TESTED + READ)

**Differential, `510124b` against `e049cec`** (the first check's `qa_diff.py` and `qa_cmp.py`, unchanged; two runs of each build, each mode; the same scripted session of 110 recorded answers; logs `diff/`):

| Mode | Result | Attribution |
|---|---|---|
| switch absent (both daemons) | **109 of 110 the same**; the 1: `invited: a invite` | the invitation is random (volatile in both builds): same keys `{expires_in_s, line, link}`, `expires_in_s` 600, `line` starting `coagent join `, `link` starting `coagent://join#` in all 8 runs. **Unattributed: 0.** |
| switch on (`--audit-a`) | **104 of 110 the same**; the 6: the invite (as above) and 5 places holding `NothingToSeal`'s text: `paired: a audit_seal {}` and `null`, `save failed: a audit_seal {}` and `null`, and `save failed: a status`'s `audit.last_seal.action` | **item B**: `"not sealed: nothing new to file since the last seal"` → `"not sealed: nothing could be filed (nothing new since the last filed point, or the log could not write)"`; row, `sealed`, `calls`, `segment` equal. **Unattributed: 0.** |

**Item B's text with a healthy store, confirmed by run:**
- Each of those 5 places is a second seal with nothing new (store writable).
- The wording is **TRUE** there: its first alternative ("nothing new since the last filed point") is what happened.
- It no longer says WHICH alternative. That is Friday's wording, chosen to claim no more than the daemon knows (Note R2-N3).
- The addendum's item E asked for "0 differences at all" with a healthy store; that cannot hold literally once item B applies to every `NothingToSeal`. The builder said so (its session made no second seal); mine shows it.

**Every removed line of `git diff -U0 510124b e049cec -- crates/coagent-daemon/src/audit.rs`: 33, all classified:**

| Old lines | n | Class |
|---|---|---|
| `:72` `Around` doc "(`status()?.segment`)" | 1 | the read (its doc) |
| `:109` `T_NOTHING` | 1 | a text of B |
| `:343-346` `drive_seal` doc | 4 | the `drive_seal` signature and doc |
| `:348` `seal_once` closure type | 1 | the signature |
| `:353` `let (answer, around) = seal_once();` | 1 | the signature (the closure now returns `closed_after`; `Around` built from the read figure) |
| `:666-667` record `if a.reopen { let _ = self.open_now(me);` | 2 | the re-open blocks (item C, send) |
| `:727-729` `let mut segment_before = 0;`, the `drive_seal(||` call, **the `unwrap_or(0)` read** | 3 | the read |
| `:732-738` the closure's `(answer, Around{segment_before, closed_after})` tuple | 7 | the signature (closure return reshaped) |
| `:744-753` seal `open_now` and the row-4 `status()` block | 10 | the re-open blocks (item C, seal; row 4 now on `member().segment()`) |
| `:773-774` `status`'s `st` and `state` lines | 2 | `status`'s first lines (item D) |
| `:781` `"reason": …` | 1 | `status`'s first lines (item D) |

**Other: 0.** `act_on_seal`, `act_on_err`, `record_ok`, `act_on_record` and `action` are **byte-identical** at both SHAs (extracted by program; sha256 of each body equal: `6c31c9646609`, `fc3d9fc32a97`, `d860289c0426`, `c0d740d356a7`, `b8b12e2c075c`). Only their line numbers moved by 13.

The record path's one behavioural change (READ, `:708-716`): a re-open is now tried before the `done` check, and a failed one returns item C's text and log line. No record action has both `reopen` and `done` (`done` only for `Recorded`, whose actions never set `reopen`). So a landed record still goes out exactly as before, and a successful re-open still ends in the old refusal and log line.

**`aw_answers.rs`, 9 removed lines:** 1 doc line (`//! \`seal_err_retried\`.` extended with AW-5b), 8 lines of the existing `drive_seal(|| { calls += 1; (all[pick].clone(), Around{…}) })` call reshaped to `drive_seal(Some(before), || { calls += 1; (all[pick].clone(), closed_after) })`. **No assertion removed or changed**; the 50 added lines append the unknown-segment pass after the existing property's last assertion.

## Task 5: the red rows (TESTED)

- **`build.rs` and the red script, READ by diff:** `build.rs` `1 0`: `"segment_before_falls_back",` appended as the last entry of `AW_RED` (after `seal_error_ends_the_engine`), nothing else. Red script `2 0`: one comment line (`# Lane AUDIT-WIRE addendum 2 (fix round, item A: F-1, the segment before a seal).`) and one row, `COAGENT_RED_AW|segment_before_falls_back|coagent-daemon|aw_answers|every_answer_the_host_can_give_has_one_action_and_it_obeys_its_row|AW-5b`, appended after AW-7's row, in the block's six-field form, the same as the round-1 AW comment-plus-rows form. **0 removed lines in either file.** Rows: 198 at `510124b`, 199 at the head.
- **The builder's regex (STATUS line 188), counted by program over `ROWS`: it selects 12 rows of 199**, one per variant: AW-1, AW-2, AW-3, AW-3b, AW-4, the four AW-5, AW-6, AW-7, AW-5b. No other lane's row uses any of the 12 names; AW-3/3b share a test, the four AW-5 rows share one too.
- **Run:**
  - Command: `RED_ONLY='^(audit_always_on|…|segment_before_falls_back)$' bash scripts/red-controls-daemon.sh`, through my wrapper.
  - Tree: my clone at `e049cec`, clean `git status`.
  - Settings: `COAGENT_TOOLS=/private/tmp/claude-501/qaw2/tools`, own empty target `qaw2/tr`.
  - Before the start: heavy counter 0, no other `red-controls`, `check.sh`, `test-p1p` or `test-daemon` run.
  - Time: 2026-11-26 06:24:41 to 06:54:41, exit 0.
  - My logs (`qaw2/tools/tmp/m1-daemon-red/`, 13 files) name only `qaw2/c` and `qaw2/tr`; 0 name the builder's worktree or target.

| Row | Variant | First panic line (my run) | Its own reason? |
|---|---|---|---|
| AW-1 | `audit_always_on` | `assertion \`left == right\` failed: status key paths, idle` | yes (as round 1) |
| AW-2 | `recreate_on_restore` | `… failed: a log was created over a session that existed: {"anchor_saved":true,…` | yes |
| AW-3 | `record_causer_always_local` | `… failed: the reply's record is charged to the peer's requested allowance: [PartStatus { used: (0, 0), …` | yes |
| AW-3b | `record_full_raw` | `… failed: the stored full tier is the redacted preview` | yes |
| AW-4 | `nothing_to_seal_retried` | `… failed: NothingToSeal is never retried` | yes |
| AW-5 | `limits_changed_read_as_done` | `case 26 (seed 00a0d17e5ea10001, call Seal): seal: LimitsChanged { answer: Ok(..) } read as done (m-2)` | yes |
| AW-5 | `landed_unknown_retried` | `case 18 (…): seal: the daemon seals again by itself for Err(LandedUnknown { … })` | yes |
| AW-5 | `commit_failed_retried_blind` | `case 88 (…): seal: the daemon seals again by itself for Err(LimitsChanged { … })` | yes |
| AW-5 | `seal_err_retried` | `case 6 (…): seal: the daemon seals again by itself for Err(LimitsChanged { … })` | yes |
| AW-6 | `seal_on_peer_message` | `… failed: a peer message caused a filed log` | yes |
| AW-7 | `seal_error_ends_the_engine` | `ctl inbox_read: no response` | as round 1 (its N-10: red through the helper's time-out) |
| **AW-5b** | **`segment_before_falls_back`** | `aw_answers.rs:637:21`: `seal: reported sealed with the segment before unknown (row 7 (the commit landed), "sealed: the log was filed away and continues") for Err(SealCommitFailed { cause: Store(Unavailable("disk")), segment_now: 1 })` | **yes: F-1's own false "sealed"** (a commit that failed with the store at segment 1, read against the fallen-back 0). Its log shows `RED CONTROL BUILD: coagent_red="segment_before_falls_back"` and `coagent-daemon` compiling. |

- Result: **12 of 12 `RED (as required)`**, 0 `STILL GREEN`, 0 harness errors; the 11 older AW rows red for the same reasons as round 1.
- **Final clean run:**
  - The script's line: `final clean run: green (77 test binaries; ignored under rulings: 2)`.
  - My sum of its `test result` lines: 77 lines, **335 passed, 0 failed, 2 ignored**, the builder's figures (331 of round 1 plus the 4 `aw_round2` tests, all four `ok` in that log).
  - The two ignored tests are the project's own, older ones; their ignore text, printed in the log, carries a seat's name, from old code.
- **The four `aw_round2` tests:**
  - At the head (`qaw2/t`): 4 passed.
  - At `510124b`: scratch worktree `qaw2/p`, the head's `aw_round2.rs` copied in (its helper `aw_util.rs` exists at `510124b`). Own empty target `qaw2/tp`; the build log and the test log each show `Compiling coagent-daemon … (/private/tmp/claude-501/qaw2/p/…)`. Result: **4 failed**, each for its own reason:

| Test | Red at `510124b` on | Its own reason |
|---|---|---|
| `a_seal_whose_listing_fails_is_never_reported_sealed` | `:81` `a commit that did not land is reported sealed (F-1): {…"row":"7 (the commit landed)","sealed":true…}` (`left: Bool(true)`) | item A: F-1 |
| `nothing_to_seal_with_the_store_unwritable_claims_no_more_than_it_knows` | `:130` `left: String("not sealed: nothing new to file since the last seal")` | item B: the old text |
| `a_failed_reopen_is_never_called_opened_again` | `:152` `left: String("the audit log was opened again and its segment read: sealed only if the segment moved")` | item C: the old row-4 text |
| `status_says_unavailable_when_the_logs_status_cannot_be_read` | `:189` `left: String("on")` | item D: the old state |

## Task 6: the texts (TESTED)

Each new or changed text of the builder's STATUS lines 211 to 217, re-made and compared byte for byte by program with the builder's bold quote:

| Text | Re-made by | Byte-equal | True as worded? |
|---|---|---|---|
| `not sealed: nothing could be filed (nothing new since the last filed point, or the log could not write)` (row `10/14 (NothingToSeal)`) | runs: `moved_running` (folder away), the differential (healthy store), `aw_round2` B (`store/` 0500) | yes (6 exact) | **yes** in all three: the log could not write (two), nothing new (healthy). |
| row `none (the segment before the seal could not be read)` + `not sealed: the log's segment could not be read, so the seal was not called; give the command again` | **harness only** (no run reaches it: task 2), 798 drives | yes (1 distinct row, 1 distinct text) | **yes** (0 calls in every drive). "give the command again" would not help while such a state lasted (Note R2-N1). |
| `not sealed: the audit log could not be opened again; see status.audit` (row `4`) | run `lu_seal`, and `aw_round2` C | yes | **yes**: state `unavailable`, reason given. |
| the same text for row `4 or 11 (closed earlier)` | READ only (`:792-795`; the seal's `Closed` arm is unreachable, task 2) | (the same constant) | yes where it could apply |
| `not sent: the audit log could not be opened again; see status.audit` (send, `state_not_saved`) | run `lu_record`, and `aw_round2` C | yes | **yes**, and truer than the old "could not record": in my run the record HAD landed (its text found in the store, `store_files_with_send1_text: 1`, F-2). |
| log `audit: a send was refused: row <row>: not sent: the audit log could not be opened again; see status.audit` | run `lu_record` (`row 4`) | yes, after the `coagentd: ` prefix | yes |
| `status.audit` `state "unavailable"`, reason `the log's status could not be read (<host answer>)` | runs `moved_running`, `iii2`, `aw_round2` A and D | yes (template; two host answers) | yes; no path, no content (task 3) |

Unchanged and still chosen before its re-open (not in the closed list; the builder recorded it under F-5's BACKLOG line): row 11's `sealed: the log was filed away; the audit log was opened again` when that re-open fails. The seal did land, so "sealed" is true; "opened again" would be false (Note R2-N2).

## Task 7: scope and records (TESTED)

- `git diff --name-only 510124b e049cec`: exactly the seven paths (`BACKLOG.md`, `crates/coagent-daemon/build.rs`, `src/audit.rs`, `tests/aw_answers.rs`, `tests/aw_round2.rs`, `docs/M0-OUTCOMES.md`, `scripts/red-controls-daemon.sh`). Controls: `510124b..184b35e` lists 24 paths (main's lanes), `bcaf119..510124b` 19 (round 1's), `bcaf119...e049cec` 20.
- The 13 protected and 3 kept files, sha256 (first 16) at `bcaf119` / `510124b` / `e049cec`: **all equal at all three** and equal to the first check's values. Protected: `gate_attacks.rs` b0f8d6b2bc2869a4, `gr2.rs` caee212babc8072b, `gr3.rs` eddd91ae98da52dc, `gr4.rs` bf8f2999dc657817, `gate_hostile/mod.rs` fa18b0bd9501b4e9, `gate_r2.rs` a1944e0c65afb1c3, `gate_r3.rs` 17cfcca984130c79, `gate_r4.rs` a2ca92a68cc5e433, `gate_r5_model.rs` 022f47049bce6688, `gate_r6_model.rs` 755820e391466664, `gate_r6_model_wrapper.rs` 2fb203a07390d43c, `gate_return.rs` d2ca677d7409133b, `common/mod.rs` 08ed3f585cf09a22. Kept: `release_audit.rs` 1ee5785a1412318d, `ipc.rs` 7ae8babc5d652f68, `dn_help.rs` 2cd8ee5f41e8c1b3.
- `crates/coagent-audit-host` tree `7808b4ddc5414b6a3f592a7d647ee54a9de130e7`, `src` `a0d4ef99e8c0b2b654575592fb578bf790f512b7`: the same at all three SHAs.
- `BACKLOG.md` (29 0) and `docs/M0-OUTCOMES.md` (10 0): **0 removed lines, and the `510124b` file is a byte prefix of the head's** (272,805 → 278,982 and 22,681 → 23,567 bytes): appended at the end only.
- BACKLOG entries, each READ against the first verdict:
  - `[x]` with a dated `Fixed:` line and its pinning test: F-1, F-3, F-5 (with row 11 named as not changed), F-7.
  - `[ ]` open, each with where / symptom / why deferred / discovered:
    - F-2: the three ways, "needs a design", "the owner will be told", open for the next audit lane;
    - F-4: R-2 stands as written, a known difference, "needs the received ids kept", open for the next audit lane;
    - F-6: open;
    - one entry for N-1 to N-9, all nine named, N-3 (the `state_not_saved` code's documented meaning) and N-6 (email addresses not masked, a limit of the audit crate) spelled out with "The owner will be told".
  - **All true to the first verdict.** The first verdict's red-table Note N-10 (AW-7 goes red through the helper's time-out) is not in BACKLOG; the addendum asked only for N-1 to N-9 (Note R2-N4).
- `docs/M0-OUTCOMES.md`: one paragraph `## 2026-11-26 — AUDIT-WIRE fix round (addendum 2)`, true as written.
- **Names and ids** (`qa_scan.py`, the first check's scanner, unchanged; words passed on the command line only, assembled from the environment at run time):
  - The word list: the owner's names and handle, mail domain, this machine's user and host names (short and full), the home path, the drive and workspace path parts, the brain, key and credential folders, the client names, the coordinator seats' names (whole words), the mail-agent inbox names, the commit identity's domain, this session's id (whole and first 8). Plus the scanner's id and UUID patterns.
  - Scanned: the round's 412 added lines and the two commit messages (`510124b..e049cec`, 17 lines). Result: **0 hits.**
  - The seven files WHOLE at the head: 94 hits, all one coordinator's name as a whole word (counted twice, two spellings of one case-insensitive word): `BACKLOG.md` 45, `M0-OUTCOMES.md` 1, the red script 1, all in lines older than the round (the added lines have 0).
  - Controls: a copy of `aw_round2.rs` with one planted line → 5 hits; a planted binary (NUL and 0xff around two planted words) → 4 hits. Both caught.
  - The builder's first-pass hit (a seat's name in its F-4 line, reworded in `e049cec`): the head's F-4 line reads "the coordinator's ruling R-2" (READ).

## Findings

No Blocker, no Major, no Minor. F-1 is closed by run and by harness; the round did exactly its list (items A to F), touched only its seven paths, removed no assertion, and kept every decision function byte for byte.

Each Note below has a reproduction and a suggested fix in words; none is required for the merge.

**R2-N1 — Note — the seal path can no longer re-open a host whose member is gone; not reachable as wired.**
- **Where:** `crates/coagent-daemon/src/audit.rs:779` (`host.member().ok()…` → `None`) and `:384` (`segment_unknown()`, 0 calls, no `reopen`).
- **What:** if the daemon ever held a member-less host, `audit_seal` would answer `none (the segment before the seal could not be read)` / "give the command again" every time and never re-open by itself. At `510124b` the seal's `Closed` arm re-opened. A `send` would still recover it (its `Closed` arm re-opens). Never "sealed". Unreachable today: every host answer that clears the member is answered by a re-open (task 2).
- **Reproduction:** none by run (not reachable); READ `host.rs:1051-1072` at `bcaf119`, and `audit.rs:706-716`, `:789-814`, `:601-648` at the head.
- **Fix in words:** in `owner_seal`, when `member()` answers `Closed`, call `open_now` first and read the segment from the re-opened host (still never sealing against an unknown figure); or set `reopen` on the segment-unknown action.

**R2-N2 — Note (pre-existing, recorded by the builder) — row 11's text says "the audit log was opened again" when that re-open fails.**
- **Where:** `audit.rs:180` / `:792-795` (`!reopened && !a.done` excludes row 11).
- **Reproduction:** none by folder rights (row 11 needs a poisoned store after a landed commit); READ.
- **Fix in words:** for a done action whose re-open failed, use "sealed: the log was filed away; the audit log could not be opened again; see status.audit".

**R2-N3 — Note — item B's `NothingToSeal` text no longer says which of its two causes applies.**
- **Where:** `audit.rs:112`.
- **What:** with a healthy store (a second seal with nothing new) it now reads "nothing could be filed (nothing new since the last filed point, or the log could not write)". True, but the owner cannot tell a full disk from a quiet log. This is Friday's chosen wording. The addendum's item E "0 differences at all with a healthy store" cannot hold literally with it.
- **Reproduction:** `python3 -B qa_diff.py <head bin> <new dir> out.json --audit-a`, labels `paired: a audit_seal {}`.
- **Fix in words (optional, later lane):** choose between the two halves by comparing `status().own_seq` with the last stored checkpoint, as the first verdict's F-3 suggested.

**R2-N4 — Note — the first verdict's N-10 (AW-7 goes red through the helper's time-out, not its own `alive(pid)` assertion) is not in BACKLOG.**
- **Where:** `BACKLOG.md` (the N-1 to N-9 entry).
- **What:** the addendum asked only for N-1 to N-9, so not a defect of the round.
- **Reproduction:** `grep -n 'N-10' BACKLOG.md` at `e049cec`: 0 hits.
- **Fix in words:** one line under the Notes entry at the next audit lane.

Carried, unchanged, for the next audit lane (BACKLOG, true to the first verdict): F-2, F-4, F-6, N-1 to N-9.

## What was NOT checked

| Not checked | Why / where it rests |
|---|---|
| A row-4 re-open that SUCCEEDS (same segment → not sealed, moved → sealed) by a run | Folder rights that fail the host's in-call re-open also fail the daemon's `open_now` (as round 1 found). Rests on READ of `audit.rs:792-811` and the TESTED equality of `status().segment` and `member().segment()` on a real host. |
| The segment-unknown reply by a run | Not reachable while the daemon holds a host (task 2). Harness only (798 drives). |
| Row 11 with a failed re-open, the seal's `Closed` arm by a run | Unreachable / needs a poisoned store after a landed commit; READ only. |
| The whole red script, `scripts/test-daemon.sh`, `scripts/check.sh`, the Windows kit, `cargo fmt`/`clippy` | Not run by the brief's rule (Friday's merge check runs them on the merged head). The daemon suite ran green as the `RED_ONLY` run's final clean run (77 binaries). |
| Main's `184b35e` merged into the branch | Not merged, not judged (the brief's rule). |
| Anything the first check confirmed at `510124b` and the round does not touch (content kept, peer-caused seals, lifecycle, switch-absent base, engine hunks) | Stands by the first verdict; the round's diff touches none of it (task 4: `engine.rs` untouched, decision functions byte-identical, differential 0 unattributed). |
| Windows | No Windows run; the round changes no Windows path. |
| The builder's own heavy-counter and scan discipline | Not graded; my own figures are above. |

Nothing of mine is left running: every daemon, relay and test binary was stopped by its harness (`left: []` in every run), and a process check at the end found no `coagentd`, `coagent relay` or `coagent-mcp` and nothing under `qaw2`. Everything I made is under `/private/tmp/claude-501/qaw2` and the two named folders (this verdict and `gate_audit_wire_r2_tests/`); in the project I wrote only my STATUS file. Nothing was deleted.
