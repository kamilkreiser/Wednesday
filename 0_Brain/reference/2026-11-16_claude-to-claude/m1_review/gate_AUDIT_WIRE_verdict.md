VERDICT: NO GO — head 510124b30aa62a493b91ace76b9d56ab7adffc04

# QA-AUDIT-WIRE — the one independent check of branch `audit-wire`

Checked head `510124b30aa62a493b91ace76b9d56ab7adffc04` (ten commits on base `bcaf1194ea268508cf92f135a60fe18076824a0f`). Brief: `briefs_drafts/2026-11-26_coagent_QA-AUDIT-WIRE_check_brief.md` (read whole), the lane brief and its ADDENDUM 1 (read whole), the builder's STATUS (147 lines, read whole), the whole diff `bcaf119..510124b` and `1257ca7..510124b`, CLARIFICATIONS C-13 to C-16, `docs/AUDIT-HOST.md` §3 at `bcaf119`, and the host's source at `bcaf119` (`host.rs` `apply`/`mutate`/`seal`/`seal_begin`/`begin_steps`/`plan_and_file`/`seal_finish`/`reopen`/`open`/`layout`/`status`, `error.rs` whole). Work dir `/private/tmp/claude-501/qaw` (own clone, own tools folder, own target dirs). Every script and test file I wrote, with its logs: `gate_audit_wire_tests/` beside this file. TESTED = I ran it; READ = I read it. Every figure of the builder's below is re-made by me or marked as its claim.

## BLUF (for a phone)

- **With the log switch off, the daemon is exactly as before except for one refusal.** My own base-against-head run (110 recorded answers, two runs of each build) found only `audit_seal`'s new refusal (7 forms of the word, at 7 points in a session, including a daemon whose saves fail) and the 6 added help lines. Nothing else differed.
- **With the switch on, a message that cannot be recorded never left**, for every cause I could make (9 kinds, including a full log after 2,776 sends). Only a short masked preview of this device's own text is kept: no raw line, no peer text, no gate decision, nothing in the daemon's log or status. Two limits apply: an email address is not masked (the crate's pattern list), and the log can hold a record of a message that was then NOT sent (three ways, shown).
- **One Major: the daemon can answer "sealed" for a seal that did not happen.** Shown by a run. The cause is one line (`audit.rs:729`): when the status read before a seal fails, the "segment before" becomes 0, and a failed commit then looks as if it "moved". The fix is one line. Every other answer of the audit host gets an action its row allows, and the daemon never seals by itself (253 commands, 253 calls).
- **Nothing but the owner's command can file the log.** No peer message did, in my own hostile stream of 150 inbound steps of every kind. Not covered: Windows (built only by the builder), rows 2/3, 8, 11 and 12, `ArchiveMismatch` and `ExportTooLarge` by a real run (only by my own answer harness), and a lying or full disk.

**Verdict: NO GO, for one Major (F-1, a false "sealed").** It is a one-line fix in `audit.rs`, plus a test and a red row. Everything else holds:
- my whole red run at the head: 198/198 red, the final clean run green, 331 passed;
- scope: exactly the 19 owned paths, no byte of the audit host crate, the protected files unchanged;
- the two differentials: 0 unattributed differences.

Five Minors (F-2 to F-6) and the Notes are for the next round or for Friday's ruling (F-4 is section 1a (5)).

## Proofs (section 0)

- TESTED `git ls-remote` on the GitHub remote (fetched with the project's deploy key into my clone): `510124b30aa62a493b91ace76b9d56ab7adffc04 refs/heads/audit-wire`, `184b35ef17cf9865c4f9b20c721f9647233f8b98 refs/heads/main`. `git merge-base gh/audit-wire gh/main` → `bcaf1194ea268508cf92f135a60fe18076824a0f`. Main's move is not merged and not judged (Friday's rule).
- TESTED `git log --format='%H %P' bcaf119..510124b`: 10 lines, a linear chain: `510124b←1257ca7←87753f5←fd67f01←5f98f14←19df720←223982e←a4cde04←8cbe23e←83e4d55`, and `83e4d556…`'s parent is `bcaf1194ea268508cf92f135a60fe18076824a0f`.
- READ the builder's STATUS: 147 lines; line 146 `Head: \`510124b30aa62a493b91ace76b9d56ab7adffc04\``, line 147 `READY FOR QA AUDIT-WIRE`. As the brief requires.
- Clean builds (TESTED, empty target dirs): head into `qaw/t`, base into `qaw/tb`: `cargo build --workspace --bins --locked`, exit 0 both (`coagent-daemon` compiled in both logs).

## Section 1a: the builder's own calls, judged

| # | Call | Judgement |
|---|---|---|
| 1 | `--audit` refused on Windows by `engine::audit_refusal`, applied in `run` right after the gate rule | **Accepted.** READ `engine.rs:371-384`: the gate rule is `run`'s first statement, `audit_refusal` the second, and nothing before `:380` opens a folder (`DataDir::open` is at `:382-384`). TESTED `cargo test --test dn_help` at the head: 3 passed. |
| 2 | Switch absent: `audit_seal` answered in `on_ipc` before the activity time, the save check and the flush; arguments checked only with the switch on | **Accepted.** TESTED (task 5): every form (no args, `{}`, `null`, `{"x":1}`, a string, a list, a number) gets the one `audit_off` answer, at idle, invited, paired (both daemons), with a's state save failing, and after the end (both daemons). One connection carrying `audit_seal` then `status` gets `[false, true]` at base and head: the connection is kept open as the base keeps it. |
| 3 | `ensure_dir` refuses an `audit/` that is not a real 0700 directory of this user | **Accepted, with Note N-1.** TESTED: at session creation, an `audit/` that is 0755 or a plain file makes the log unavailable and every send refused (R-6 text). The check runs only at creation: an `audit/` made 0755 mid-session or before a restart is accepted (records land). |
| 4 | A restored session is opened only when not ended; `ensure_open` re-opens and never creates | **Accepted.** TESTED: 27 SIGKILL restarts (two runs) and three removed-folder cases: the log line `audit log created` appears once per data folder (at pairing), never after a restart. The removed folder stays absent; the reason is "this session's log is missing or empty; it is never created again…". |
| 5 | Causer `Member(peer)` whenever the item has a `re` | **NOT accepted as worded: established by run (Finding F-4).** All three replies were charged to the peer's requested allowance (`requested[1].used` = 3 records): one naming the peer's request, one whose `re` names nothing (`zzzzQAWnothing0000`), and one naming the daemon's OWN request. After 396 replies naming nothing, the peer's allowance is full (row 10). From then on, a reply to the peer's REAL request is refused (`not sent: the audit log could not record this message…`) until a seal. Chats still go. For Friday to rule. |
| 6 | The `send` refusal reuses `state_not_saved` | **Note N-3.** The code's documented meaning ("A state file could not be saved; state-changing commands are refused until one is", `ipc.rs:80`) is false after an audit refusal. TESTED: while sends were refused, receiving, the inbox and `audit_seal` all worked, and the next send worked once the cause was removed. `coagent-mcp` does not map codes (no `state_not_saved` in `crates/coagent-mcp/src`), so an agent sees the daemon's own true text. |
| 7 | Record-side labels: `AnchorNotSaved`/`Dir` from `apply` = "1 (… unwritten)", `Reopened{landed:true}` = "2", refused | **Accepted.** TESTED: `anchors/` unwritable: the first send lands and goes out (row 1: landed, its anchor save failed, `anchor_saved:false`), and the next send is refused "row 1 (the anchor of the last change is unwritten)". That is row 1's retry column (the next change is refused until a save succeeds). READ `host.rs:1272-1287`: a landed record with seq+1 is answered `Ok(Recorded)`; `Reopened{landed:true}` comes only when the anchor moved without own seq +1, which I could not make. |
| 8 | `Anchor`, `NotCreated`, `AlreadyCreated`, `Settings` = "none (open-time refusal)" | **Accepted.** READ at `bcaf119`: `Anchor` is built only in `resolve` (`host.rs:792-815`), reached from `open` and `reopen`; `reopen`'s error reaches `apply`/`seal` only inside `LandedUnknown{reopen}` (`:1258-1266`, `:1734-1744`), and is dropped in `seal_finish`'s Ok path (`:1683`). `NotCreated` comes only from `layout`/`open` (`:627`, `:658`, `:666`, `:896`). `AlreadyCreated` only from `create` (`:844`). `Settings` only from `SealSettings::parse` (`settings.rs:86`), which the daemon never calls. |
| 9 | R-8: every value of the alphabet constructible; no mirror | **Accepted.** My own alphabet (task 1) is built from public fields, plus a SignedHead, SegmentInfo and Bundle taken from a real `AuditHost` in a temp folder. It compiles and runs. |
| 10 | `status.audit` carries `reason`, `seals`, `last_seal.sealed` | **Accepted.** `reason` is either fixed text or fixed text plus `{e:?}` of a `HostError` from `create`/`open` (`audit.rs:516`, `:596`). `error.rs:1-3`: "No variant carries record content, tier text, key material or a full path"; names are relative to the host's root. TESTED value: `the log could not be opened (Dir(Io { what: "sync the directory", name: "store", kind: PermissionDenied }))`. No planted value ever appeared in any `status` answer (task 4). See F-6 on `reason` being overwritten. |
| 11 | The "unavailable" seal reply has no `limits` key | **Accepted; Note N-5.** TESTED: `{"action":"not sealed: the audit log is unavailable (see status.audit)","calls":0,"row":"unavailable","sealed":false,"segment":null}`. |
| 12 | R-9 reach: rows 4, 3/2, 8, 11, 12, `ArchiveMismatch`, `ExportTooLarge` not reached by the write bit | **Accepted for the lane.** My task 1 rests on my own enumeration. My own means (the READ bit) reached row 4 on a record and on a seal (`store/` 0300). Also reached by run: row 7 (moved and not moved, the false one included), 13, "13 or 14", 10 and LogFull. Not reached by any run of mine: 2/3, 8, 11, 12, `ArchiveMismatch`, `ExportTooLarge`. |
| 13 | AW-2's branch corrected at `510124b` after the whole run at `1257ca7` | Judged in task 8 (my whole run is of `510124b`). |
| 14 | AW-7 goes red on `ctl inbox_read: no response` | Judged in task 8. |
| 15 | `tests/aw_util.rs` built as a target with no test | **Accepted.** |
| 16 | The builder's differential method | **Accepted as its method only.** Mine is in task 5, every dropped value named. |
| 17 | Open (a): a record lands, then the daemon's state save fails | **Established by run (Finding F-2).** See task 3. |
| 18 | Open (b): `store/` unwritable, `audit_seal` says "nothing new to file" | **Established by run (Finding F-3).** See task 3. |
| 19 | Windows built only | **Accepted; not re-run by me** (no Windows run in this check). |
| 20 | 95 scan hits, all in older lines | **Accepted.** My scan: 0 hits in added lines and in the ten commit messages (task 10). |

## Task 1: every answer, by the table (TESTED + READ)

**My enumeration, from the host's source at `bcaf119`** (before reading the r2 verdict's §11):

`apply(Input::Record)` (`host.rs:1177-1292`) can answer:
- `Err(Closed)` (`member_ref`, `:1183`, `:1243`);
- `Ok(Queued)` / `Err(Busy)` only while a seal window is open (`:1186-1203`). The window is never open between engine steps: `seal` = `seal_begin` then `seal_finish` in one call, and `seal_finish` takes the window first (`:1630`). So these are not reachable.
- `Err(AnchorNotSaved)` (`ensure_anchor` → `save_current`, `:1148-1151`), or `Err(Dir(..))` from the `anchors/limits` write (`save_limits`, `:984-995`);
- `Ok(Recorded(n))` (`run`, `:529-543`; a landed record also after a P-4 re-open, `:1277-1279`);
- `Err(Audit(e))` (store not poisoned, `:1290`; `LogFull` among them);
- `Err(LandedUnknown{..})` (re-open failed, `:1261-1266`);
- `Err(Reopened{landed})` (`:1274`);
- `Err(LimitsChanged{answer: Ok(Recorded) | Err(Reopened{..})})` (`with_limits_res`, `:1288`, `:1102-1114`).

`seal(.., OwnerCommand, ..)` (`:1520-1528`) can answer:
- `Err(Closed)` (`:1543`, `:1564`, `:1592`, `:1651`);
- `SealInProgress` (`:1545`) and `NoSealInProgress` (`:1630`): not reachable (one call);
- `TriggerOff`/`NotDue`: not for `OwnerCommand` (`admit`, `:1454`);
- `Err(AnchorNotSaved)` / `Err(Dir(..))` from `ensure_anchor` before and after step 0 (`:1557`, `:1569`);
- from step 0 (`mutate(Checkpoint)`), `Err(LandedUnknown)` or `Err(LimitsChanged{Ok(Checkpoint) | Err(Reopened{..})})`, returned as they are (`:1559-1563`). That is m-2: the seal did not run.
- from step 1 (`seal_export`), `Err(Audit(NothingToSeal | other))` (`:1594`), and `Err(Audit(ExportTooLarge))` (`:1603`, `:1412-1414`);
- from `write_archive`, `Err(Dir(..))` (list, write, read back) or `Err(ArchiveMismatch)` (`:1416-1437`), and `Dir(Bounds)` (`:1422`);
- `Err(Dir(..))` from the pending anchor (`:1609`);
- `Ok(SealReport{limits: None | Some})`, the host possibly closed after (`:1679-1698`);
- `Err(SealStaleTwice)` and a stale re-plan's errors: not reachable (`SealStale` needs a change in the window; test hook only);
- `Err(LandedUnknown)` from the commit (`:1739-1744`);
- `Err(SealCommitFailed{segment_now})`, possibly wrapped `LimitsChanged{Err(SealCommitFailed)}` (`:1751-1758`).

**"The plan's segment" (task 1 (ii)).** READ `begin_steps`/`plan_and_file`: `SealBegun::segment = plan.segment`, and `seal_export` sets the new Segment record's `segment` to `self.segment() + 1` (`session.rs` `seal_export`, `SegmentRecord{segment: self.segment().saturating_add(1)}`). After a commit error the host re-opens from disk, pending anchor first, and `segment_now` is the re-opened member's segment (`host.rs:1751`). It can only be k (not landed) or k+1 (landed). So "segment_now = the plan's segment (k+1)" and "segment_now moved from the segment read before the call (k)" agree, **provided the segment before is really k.** See (iii).

**Task 1 (iii): MAJOR (F-1), established by a run.** `owner_seal` reads `segment_before = host.status().map(|s| s.segment).unwrap_or(0)` (`audit.rs:729`). `status()` fails whenever listing the store, the archive, `anchors/` or the host's root fails (`host.rs:1835-1838`, `:1848`, `:1859-1864`). A seal can still run to its commit while one of those listings fails: the root only needs search (x), not read, for every write. My harness over the head's public `act_on_seal`: `SealCommitFailed{segment_now: 2}` with `segment_before: 0` → `row "7 (the commit landed)", done=true, "sealed: the log was filed away and continues"`; the control with `segment_before: 2` → `row "7", done=false`. My run (`qa_causes2.py iii2`, head binaries, `--audit`):
1. send; `audit_seal` → `ok`, segment 1.
2. two sends; `archive/` made 0500; `audit_seal` → "13 or 14". Its step 0 left a stored own checkpoint newer than the last seal.
3. `archive/` back to 0700; `store/` 0500 and the session root 0300 (search only); `audit_seal` →
   `{"action":"sealed: the log was filed away and continues","calls":1,"limits":null,"row":"7 (the commit landed)","sealed":true,"segment":null}`.
4. Rights restored: `status.audit` → `segment: 1`, `seals: 1`, `last_seal: {"row":"7 (the commit landed)","sealed":true}`. **The commit did not land.** The segment never moved, the host's own seal count stayed 1, and an orphan `seg-00000000000000000001-0000.bundle` was left. The next `audit_seal` sealed for real (segment 2, `seals` 2).

The same unknown `segment_before` also drives row 4's read after a re-open (`audit.rs:749`). I could not make that path reach "sealed" by a run: the conditions that fail the read before the seal also fail the re-open after it.

**The answer table (my alphabet, run through the head's public functions; `qa_alpha.rs`, 89 seal answers × {open, closed after}, 92 record answers × 2; full table `logs/out_alpha.tsv`).** Grouped (the full per-value table is the log):

| Answer | From | Row | Action as built | Allowed? |
|---|---|---|---|---|
| `Ok(SealReport{limits:None})` | seal | ok / 11 when closed after | done; re-open if closed | yes |
| `Ok(SealReport{limits:Some})` | seal | 12 / "12 and 11" | done; report kept in `status.audit.limits` | yes |
| `Err(Dir(any of 15 DirError values))` | seal | "13 or 14" | not sealed, no call again | yes (addendum 1) |
| `Err(AnchorNotSaved)` | seal | 13 | not sealed, no call again | yes |
| `Err(Audit(NothingToSeal))` | seal | 10/14 | not sealed, never retried | yes |
| `Err(Audit(other: LogFull, ExportTooLarge, Store, SealStale, FieldLimit, TooLarge))` | seal | 14 | not sealed | yes |
| `Err(ArchiveMismatch)` | seal | 14 | not sealed | yes |
| `Err(SealCommitFailed{not moved})` | seal | 7 | not sealed, owner's next command only | yes |
| `Err(SealCommitFailed{moved})` | seal | "7 (the commit landed)" | done | yes, **if** the segment before is true; **F-1** when it fell back to 0 |
| `Err(LandedUnknown)` | seal | 4 | re-open, read the segment, done only if moved | yes (same F-1 caveat) |
| `Err(Closed)` | seal | "4 or 11" | re-open, not sealed | yes |
| `Err(LimitsChanged{Ok(any of 6 Outcomes)})` | seal | "8 (m-2)" | **not done**, report kept | yes (m-2) |
| `Err(LimitsChanged{Err(Reopened{..})})` | seal | "2 or 3 (the seal did not run)" | not sealed, report kept | yes |
| `Err(LimitsChanged{Err(SealCommitFailed)})` | seal | 7 / "7 (the commit landed)" | by the segment | yes |
| `Err(LimitsChanged{Err(LimitsChanged{Ok(Checkpoint)})})` | seal | 8 | not done | yes |
| `Err(Busy/SealInProgress/NoSealInProgress/TriggerOff/NotDue)` | seal | "15 (not reachable as wired)" | reported, no retry | yes |
| `Err(SealStaleTwice)` | seal | "none (the sentence under the table)" | reported, no retry | yes |
| `Err(Anchor/NotCreated/AlreadyCreated/Settings)` | seal | "none (open-time)" | reported, no retry | yes (not answers of `seal`, see 1a (8)) |
| `Ok(Recorded(n))`, also inside `LimitsChanged` | record | 1 | the send goes out, number kept | yes |
| `Ok(Checkpoint/Evidence/Released/Kept/Queued)` | record | "none" | send refused | yes (fail closed) |
| `Err(Dir(..))` | record | "1 (a write of the last change is unwritten)" | send refused | yes |
| `Err(AnchorNotSaved)` | record | "1 (anchor unwritten)" | send refused | yes |
| `Err(Audit(any))` | record | 10 | send refused | yes |
| `Err(Reopened{landed:false})` | record | 3 | send refused, not re-sent | yes |
| `Err(Reopened{landed:true})` | record | 2 | send refused | yes (but see F-2: something landed) |
| `Err(LandedUnknown)` | record | 4 | re-open, send refused | yes (see F-2: TESTED, the record had landed) |
| `Err(Closed)` | record | "4 or 11" | re-open, send refused | yes |
| every other `Err` | record | "15"/"none" | send refused | yes |

My checker's rules held for every answer and both values of "closed after": no `call_again`; done only for `Ok` or a moved commit; m-2 never done; `LandedUnknown`/`Closed` always re-open; `NothingToSeal` never retried; a `LimitsChanged` report never dropped; a record is "done" only for `Recorded` (bare or wrapped), its number kept. **No wildcard** (TESTED in a scratch copy `qaw/p1`, own target `qaw/tp1`):
- with a scratch variant `QaScratch` added to `HostError` (`error.rs`, after `SealStaleTwice`): `error[E0004]: non-exhaustive patterns: \`&HostError::QaScratch\` not covered --> crates/coagent-daemon/src/audit.rs:193:11`;
- with one added to `Outcome`: `error[E0004]: non-exhaustive patterns: \`&coagent_audit_host::Outcome::QaScratch\` not covered --> crates/coagent-daemon/src/audit.rs:140:11`;
- control: the copy with both files restored compiles (`Compiling coagent-audit-host`, `Compiling coagent-daemon`, `Finished`).

The host crate itself compiled with each scratch variant, so the E0004 is the daemon's own match. Lane's `aw_answers` at the head: 1 passed (0.08 s).

**Compared with the r2 verdict's §11 (read only after mine was written).** I found no answer it has that I lack. Two differences of emphasis:
- I list `Err(Reopened{landed:true})` from `apply(Record)` as producible in principle (`:1274` with `landed` true and own seq not +1). The daemon refuses the send although something landed.
- I list the `status()` failure before a seal as an input to row 7's reading. The r2 verdict's table, being about the host, does not have the daemon's `segment_before`.

## Task 2: the daemon never seals by itself (READ + TESTED)

READ by `git grep -n -F` at `510124b` under `crates/coagent-daemon/src`:
- `seal_begin(`: 0 hits; `seal_finish(`: 0. Control: 6 hits in `crates/coagent-audit-host/src`.
- `SealTrigger::`: 3 hits, all `OwnerCommand` (two doc comments, and `audit.rs:730`).
- `due(`: 5 hits: one doc comment and the relay-retry timer (`engine.rs:2991`, `relay_child.rs:265`, `:813`, `:820`); none of the audit host.
- `.seal(`: 6 hits. The host's is only `audit.rs:730` (`host.seal(me, SealTrigger::OwnerCommand, now())`); the other five are the channel's crypto sealing (`engine.rs:2432`, `:3339`, `:3342`, `recovery.rs:1475`, `:1825`), older than the lane.
- `owner_seal(` is called from `seal_command` (`audit.rs:702`) and `red_seal` (`:764`). `seal_command` is called only by `on_ipc` for `Command::AuditSeal` (`engine.rs:1219` switch off, which returns at `audit.rs:685-686` before any host call; `:1314` switch on). `red_seal` is called only at `engine.rs:2816`, inside `if cfg!(coagent_red = "seal_on_peer_message")`. That is false in every build without the red variable (build.rs emits the cfg only when `COAGENT_RED_AW` is set; TESTED: a plain build prints 0 `RED CONTROL BUILD` lines).

`red_seal` is a `pub fn` compiled into every build. A library caller could call it, but no received input reaches it: **Note N-2**, acceptable.

TESTED (`qa_alpha.rs::qa_n_commands_n_calls`): 253 owner commands through `drive_seal`, each answered from my alphabet in turn (82 answers: `Ok`, every `HostError` bare and inside `LimitsChanged`, m-2's `Ok(Checkpoint)`) → **253 `seal` calls, 1 per command.** The four AW-5 red controls: see task 8.

## Task 3: fail closed (R-6), every cause (TESTED)

Head binaries; `a` = convener with `--audit`, `b` = joiner without. Each row: one send that lands, then the cause, a send under test, a probe (b sends to a; a's inbox, `status`, `audit_seal`), the cause removed, one more send. Logs: `logs/causes1.jsonl`, `c2a`, `c2b`, `c2c`, `full_*`.

| Cause | `send` answer | outbox (`send_next`; text in `outbox.json`) / peer got it | receiving / inbox / status / `audit_seal` while it holds | after the cause removed |
|---|---|---|---|---|
| `store/` 0500 | `state_not_saved`, R-6 text; log `row 10` | 2→2; no / no | yes / yes / ok / "10/14 (NothingToSeal)" (**F-3**: a record was pending) | next send ok, own seq +1, delivered |
| `anchors/` 0500, 1st send | **ok** (row 1: landed, anchor save failed; `anchor_saved:false`) | 2→3; yes / yes | — | — |
| `anchors/` 0500, 2nd send | `state_not_saved`, R-6; log "row 1 (the anchor of the last change is unwritten)" | 3→3; no / no | yes / yes / ok / "13" | ok, delivered, `anchor_saved:true` |
| `archive/` 0500 | **ok**: records still land (expected) | yes | yes / yes / ok / "13 or 14" | ok |
| `audit/` 0755 at session creation | `state_not_saved`, R-6 | 1→1; no / no | yes / yes / ok (`unavailable`) / "unavailable" | not tried (the session never gets a log: F-6) |
| `audit/` a plain file at creation | same | same | same | same |
| `audit/` 0755 mid-session | **ok** (no check after creation, N-1) | — | `audit_seal` sealed | — |
| session root 0755 mid-session | **ok** (the host checks rights at open) | — | sealed | — |
| session folder moved away while running | `state_not_saved`, R-6; row 10 | 2→2; no / no | yes / yes / `state "on"`, every field null, `reason null` (**F-7**) / "nothing new to file" (F-3) | not restored. After a restart: `unavailable`, reason "missing or empty; never created again", folder still absent, no `created` line, send refused |
| folder moved away, then restart | `state_not_saved`, R-6 | 2→2; no / no | yes / yes / ok (`unavailable`) / "unavailable" | — |
| log full (LogFull, default limits) | after **2,776** accepted local sends: `state_not_saved`, R-6; row 10 | not queued | yes / yes / ok / **sealed** (seal and continue works) | a reply (peer's allowance) still went out |
| host closed (`LandedUnknown`, `store/` 0300) | `state_not_saved`, R-6; log "row 4 … the audit log was opened again" (**false**: it was not, F-5) | 2→2; no / no | yes / yes / ok (`unavailable`, reason `Dir(Io{sync the directory, store, PermissionDenied})`) / "unavailable" | `store/` restored: next send ok, opened (`Current`), own seq +2 (**the refused send's record had landed**, F-2) |

**Open (a), TESTED (F-2).** The data folder was made 0500 between sends (the audit folders stay writable). The send was answered `state_not_saved` / "state could not be saved"; the message was not in `outbox.json` and the peer never got it. **But own seq went 1 → 2: the log holds a record of a message that was never queued.** Folder restored, the same text given again: ok, delivered, own seq 3. **One message sent once is now recorded twice**, and the log's claim "this device sent X" is false for the first record. The owner sees the "state could not be saved" error in the reply and the log, and nothing in `status.audit` says a record was kept. The same class TESTED twice more:
- the row-4 case above: the R-6 text says "could not record this message" but the record had landed;
- a SIGKILL between a record and its reply (task 6: own seq after the restart one above the last acknowledged record, e.g. kill 4: 13 vs 12).

**Open (b), TESTED (F-3).** With `store/` 0500 and one unfiled record (own seq 1, segment 0, no seal ever made), `audit_seal` answered `not sealed: nothing new to file since the last seal`. **False as worded:** there was something new (own seq 1), and there had been no "last seal". Step 0's checkpoint failed, and `seal_export` cuts at the latest STORED own checkpoint (host §6). The owner reading it would think the log is filed up to now and not repeat the command once the disk is fixed. Nothing is lost (the record stays and is filed by the next seal), and the same moment's sends are refused, pointing to `status.audit`. Same text, same falsehood, with the folder removed while running.

**`audit_seal` when the DAEMON's state save failed.** TESTED both ways:
- with a peer message arriving while the data folder is unwritable (dirty state): `audit_seal` → `state_not_saved` / "state could not be saved" (the base's pre-check, `engine.rs:1230-1238`);
- with nothing dirty (task 5's "save failed" phase): it **sealed** (the pre-check's flush has nothing to write).

R-6's "`audit_seal` keeps working" is written for the state where a RECORD cannot be made, and there it works (every row above). In the daemon's own unsaved state, every state-changing command is refused by the base rule, and `audit_seal` is classed as one. **Note N-4**, not a finding. READ: after a seal that landed, a failing post-reply flush replaces the reply with "state could not be saved" (`engine.rs:1333-1337`, base code), so the owner can be told a failure for a seal that happened (same Note).

## Task 4: what is recorded (TESTED)

`qa_content.py` (head; logs `content1.jsonl`): one 6-line, 300+ character send with nine made-up secret-shaped values in lines 1-3 (an API-key shape, a bearer header, a password assignment, an OpenSSH private-key header, a 64-hex string, a JWT shape, a URL with a password, a cloud-key shape, an email address), a unique raw line 4, nine one-line sends each holding one value, a request, and three replies (re = the peer's request; re = a name of nothing; re = the daemon's own request). The peer sent a request and a chat with a unique marker. Daemon stopped, data folder COPIED, the copy opened by my inspector (`qa_inspect.rs`, a fresh `AuditHost` on the copy).
- **Stored full tier = `coagent_audit::redact::preview(&PatternRedactor, text)`** for the long send and for all nine one-line sends (equal strings). The long send's stored tier: `"line one: key [REDACTED] auth Bearer [REDACTED]\nline two: [REDACTED] [REDACTED]"` (79 characters, 2 lines: the private-key pattern masks to the end of the window, line 3 included).
- **No summary tier:** `summary` is `None` on all 14 stored events. Kinds are the IPC kinds (`chat` ×10, `request`, `reply` ×3). The header holds session, author, own number, time, previous hash, kind, and a salted commitment to the preview only (no raw length, no raw hash).
- **Byte greps** (each planted value, the dropped raw line and the peer's marker):
  - audit folder: 0 hits for 8 of the 9 values, the dropped line and the peer marker. **The email address is kept** (in the store file of its own send): the crate's `PatternRedactor` does not mask email addresses. That is a limit of the crate, not of this lane (Note N-6).
  - daemon log: 0 hits for all; `status` answers: 0 hits for all.
  - whole live data folder: only the email (audit store) and the peer marker in `inbox.json` (the base's inbox, not the audit).
  - control (a file holding the text): every needle hits.
- **Gate decisions are not recorded** (`qa_gate.py`): a daemon with `--audit --gate --workspace <ws>`, two gate decisions (`ask` for Glob and Read, both in `activity`). The audit folder's files and their sha256 are identical before and after, and own seq is unchanged (1).
- **Causer:** the member's status shows the free part used by 11 records (10 chats + 1 request: `LocalHuman`) and the peer's requested allowance (`requested[1]`) by 3 records: all three replies, including the one naming nothing and the one naming the daemon's own message. This is section 1a (5), F-4.

## Task 5: switch absent is the base, ONE attributed difference (TESTED)

My own script (`qa_diff.py`; I did not run the builder's). Per build, two runs: `bcaf119` from `qaw/tb`, the head from `qaw/t`, `coagentd` and `coagent-mcp` of the same build. One session: `--help` (stdout, stderr, exit); idle (11 commands on a); `audit_seal` in 7 forms; one connection with two requests; status key paths of both; data folder listings; invite; join; both connected; sends (chat, request, bad kind, reply without `re`); b reads, replies (re = the request), acks; a reads and waits; gate, activity, verify_start, an unknown command; `audit_seal` forms on a and b; `coagent-mcp` `initialize`, `tools/list` and one call of each of its three tools; outbox files; a's data folder made unwritable (send, `audit_seal` forms, status); `end`; then after the end and after the stop. 110 recorded answers per run. Normalisation (named): hex runs of 8+ → `<hex>`, RFC 3339 times → `<ts>`. A label whose value differs between the two runs of ONE build is volatile and is compared with digits as `<n>`. Three were volatile:
- `idle: a status` (pid);
- `save failed: a status` (pids, ports, counters);
- `invited: a invite` (the invitation is random base64). Both builds give `expires_in_s` 600, keys `{expires_in_s, line, link}`, `line` starting `coagent join `, `link` starting `coagent://join#`.

| Compared | Result |
|---|---|
| **switch absent, base vs head** | **51 different of 110:** `audit_seal` × 7 forms × 7 call points (idle a, invited a, paired a, paired b, save failed a, ended a, ended b) = 49, each `unknown_command`/`unknown command` → `audit_off`/`the audit log is off: coagentd was not started with --audit`; `--help` stdout (exactly 6 lines added, 0 removed: `[--audit]` after the `--keep-relay-identity` line, and the 5-line paragraph after `read content or pair.`); the invite (volatile, random, same shape). **Unattributed: 0.** Same: every answer of the 12 commands in every state, every status key path in every state, both listings in every state (no `audit/`), the one-connection test (`[false, true]` both), both outboxes, `coagent-mcp`'s `tools/list` and its three calls, the sends' refusals while unsaved. |
| **switch ON at a (head) vs base (off)** | **62 different of 110**, every one attributed: `audit_seal`'s answers (no session → `no_session`; in a session → sealed / NothingToSeal; arguments → `bad_args`; b, head without the switch → `audit_off`); `status.audit` key paths on a (idle, invited, paired, ended) and its value in `idle: a status` / `save failed: a status`; a's listings gain `audit/<session>/{lock, store/…, anchors/{current,limits}, archive/seg-…}` (paired, ended, stopped); the one-connection test `[true, true]` (the seal answers ok); `--help`; the invite (volatile). **Unattributed: 0.** Every send answer, b's received texts (`QAD chat one`, `QAD request two`, the mcp send), a's received reply, and both `outbox.json`: identical to the base. |

The lane's `aw_off` at the head: 1 passed (3.9 s).

## Task 6: no peer input causes a seal, and the lifecycle (TESTED)

**My hostile stream** (`qa_peer.rs`, in my scratch copy; `tests/gate/gate_hostile/mod.rs` included read-only by `#[path]`, unchanged). Victim = convener with `--audit` and an outside relay; seed `0x5eed0a0a7777`, 150 steps, interleaved with the victim's own sends. Reach:
- chat in order 29; duplicate number 10; number out of order 10; oversize text (70,000 characters) 15; a type never delivered 14; raw garbage 9;
- fresh key exchange 14; replayed key exchange 6; reply naming the victim's message 17; request 18;
- own send 8.

Result: archive files `[]` → `[]`, `seals` 0 → 0, `segment` 0 → 0, own seq 0 → 8 = the 8 accepted own sends. The victim answered throughout; 1 passed (9.8 s).

**SIGKILL and restart** (`qa_kill.py`, `--audit --keep-relay-identity`, 27 kills in two runs):
- Run 1 (mixed, 15 kills): 1 inside a seal (an anchor temp file present at the kill), 5 between a record and its reply, 9 idle.
- Run 2 (seals, 12 kills): 7 inside a seal. Kill 7 had the segment file `archive/seg-00000000000000000000-0000.bundle` already written at the kill (after step 2, before the commit). Others had anchor or archive temp files.
- After EVERY restart: `status.audit.state` `on` (`audit log opened (Current; segment 0; …)`); own seq never lower than the last acknowledged record; `audit log created` appears once in the whole stderr, at pairing.
- At the end, one owner seal, then the inspector over a copy:
  - run 1: `verify_segments` Ok (`segments: [(0, 1, 43), (1, 44, 43)]`), own numbers 1..43, no gap, **signed twice 0**;
  - run 2: Ok (`[(0, 1, 24), (0, 1, 35), (1, 36, 35)]`: kill 7's orphan segment file verifies as an ordinary valid export), 1..35, no gap, **signed twice 0**.
- The host's leftover temp files grow by about one per kill inside a write (8 after 12 kills, never deleted, host P-5; at 64 in one folder the host refuses to open). With `--audit` that would make every send refused until the owner moves them away (Note N-8; the host's documented behaviour).

The lane's tests at the head (short, timed): `aw_peer` 2 passed (10.9 s); `aw_lifecycle` 3 passed (12.8 s); also `aw_seal` 1 (3.1 s), `aw_record` 1 (1.9 s), `aw_disk` 1 (29.5 s).

## Task 7: the texts a person reads (TESTED + READ)

Each text re-made by my runs, compared byte for byte with the builder's quotes (STATUS `:43-60`).

| Text (as built) | Where | Re-made? | Equal to the builder's quote | True as worded? |
|---|---|---|---|---|
| `audit_off` / `the audit log is off: coagentd was not started with --audit` | `audit_seal`, switch absent | TESTED (49 call points) | yes | yes |
| `state_not_saved` / `not sent: the audit log could not record this message (see status.audit); nothing was queued` | a refused send | TESTED (every cause in task 3) | yes | "nothing was queued": true in every case. **"could not record" is false when the record LANDED** (row 4, `LandedUnknown`; F-2). The code's documented meaning does not fit (N-3). |
| `coagentd: --audit is not supported on Windows yet: the audit log's folder checks are Unix-only. Start without --audit` | Windows, exit 2 | READ only (`audit.rs:55`; `main.rs:134-142` prints it and returns 2; `run` returns it as `Err`) | yes | yes (the host refuses every open off Unix, `docs/AUDIT-HOST.md` §1) |
| the 6 USAGE lines | `--help` | TESTED (diff of both builds' `--help`) | yes, and placed after `[--keep-relay-identity]` and after its paragraph | see the three rows below |
| "A message that cannot be recorded is not sent." | USAGE | TESTED | — | **True** for every cause I made. The converse does not hold: a message NOT sent can still be recorded (F-2). |
| "filed logs of up to 64 MiB each are kept and never deleted" | USAGE | READ | — | **True.** `write_archive` refuses a bundle above `MAX_BUNDLE_BYTES` = 64 × 1024 × 1024 (`host.rs:1412-1414`, `bundle.rs:56`). The archive is written under a never-taken name and "nothing in the archive is ever replaced or deleted" (`:1404-1405`). No `remove` of an archive file in the host or the daemon (grep). Failed seals also leave orphan segment files, which are kept (TESTED, task 6). |
| "at most 240 characters or 3 lines" | USAGE | TESTED + READ | — | **True** (strictly "whichever comes first"). `truncate` counts the mask text and every line break inside the 240 and stops at the third line break (`redact.rs:67-91`). Stored previews TESTED: 79 characters / 2 lines; the one-line sends equal the crate's preview. |
| "for each message this device sends, its kind and a short redacted preview of its text" | USAGE | TESTED | — | **Loose (Note N-7):** each record also keeps its time, own number, previous hash and signature (no content). No raw length or raw hash is kept. |
| `sealed: the log was filed away and continues` (`ok`, `12`, `7 (the commit landed)`) | seal reply | TESTED `ok`; `7 (the commit landed)` | yes | **False once, TESTED: F-1** (row 7 read against a segment that fell back to 0). |
| `not sealed: nothing new to file since the last seal` (`10/14 (NothingToSeal)`) | seal reply | TESTED | yes | **False** with `store/` unwritable or the folder removed: a record was pending and there had been no seal (F-3). |
| `not sealed: give the command again` (`13`, `13 or 14`, `14`, `7`, `8`, `2 or 3`) | seal reply | TESTED `13`, `13 or 14`; READ the rest (`audit.rs:102-115`) | yes | True as advice. Given again at once it fails again while the cause lasts (TESTED: `archive/` unwritable). It does not say "after the cause is fixed" (N-7). |
| `the audit log was opened again and its segment read: sealed only if the segment moved` (row `4`) | seal reply | TESTED (`store/` 0300) | (the builder quotes only the two final forms) | **False as worded when the re-open failed** (the state was `unavailable`, no segment read) (F-5). |
| `not sealed: the audit log was opened again; give the command again` / `…; the audit log was opened again` | seal reply / log line | READ, and the log line TESTED | yes | **False** when the re-open failed: TESTED log line "row 4: … the audit log was opened again" right after "audit log unavailable" (F-5). |
| `not done: an answer the daemon never asks for (reported, not retried)` / `not done: an open-time refusal (reported, not retried)` | seal reply | READ (my harness only) | yes | yes |
| `not sealed: the audit log is unavailable (see status.audit)` | seal reply | TESTED | yes | yes |
| `status.audit` fields | status | TESTED; shape equal to the builder's quote | yes | `state "on"` with every field null and `reason null` while every send is refused (folder removed while running): misleading (F-7). |
| `audit log created for this session` | daemon log | TESTED | yes | yes |
| `audit log opened (Current; segment 0; pending promoted false; leftovers 1)` | daemon log | TESTED | yes | yes |
| `audit log unavailable: <reason>; every send is refused until it opens` | daemon log | TESTED, three reasons | yes | yes |
| `audit: a send was refused: row <row>: <action>` | daemon log | TESTED rows 10, 1, 4 | yes | row 4's action text is false (F-5). "not recorded" is false when the row-4 record landed (F-2). |
| reasons: `audit/ is not a directory of this user with mode 0700` / `this session's log is missing or empty; it is never created again for a session that existed` / `the log could not be opened (<host answer>)` | status, log | TESTED all three; `the log could not be created (…)` READ | yes | The second **replaces** the first in `status` after the first send of a session whose log was refused at creation. The session "existed" only in that sense, and the true cause is then only in the log (F-6). |

Texts the owner has not ruled: none beyond the lane's own fixed texts (the lane brief names them for the owner at the landing). The preview rule (240/3) is still "PROPOSED, NOT RULED" in the crate (`redact.rs:14-18`), as the builder says.

**For the owner, in plain words.** When `coagentd` is started with the new `--audit` switch, it keeps a signed log of the messages this computer sends, in a folder inside its own data folder (one sub-folder per session). For each message it keeps the kind (chat, request, reply), the time, and a short preview: at most 240 characters or 3 lines, with things that look like passwords or keys blanked out. Email addresses are not blanked. It never keeps the full text, never keeps what the other person sends, never keeps the gate's decisions, and nothing is ever sent anywhere. If a message cannot be written into the log (a disk problem, a full log, a missing folder), the message is not sent and you get a "not sent" answer; receiving, reading and status keep working. The log is filed away only when you give the command (`audit_seal`); nobody else and no timer can do it. Filed parts of up to 64 MiB each are kept and never deleted, so they add up over time. It does not work on Windows yet.

Four things to know:
- After certain disk problems the log can hold a message that was in fact not sent. If you then send it again, it appears twice.
- One rare disk fault can make the filing command say "sealed" when it was not (F-1, to be fixed before merging).
- "Nothing new to file" can be wrong while the disk is failing.
- After many crashes, leftover temporary files pile up; at 64 in one folder the log stops opening and messages are refused until they are moved away.

## Task 8 (scope part): scope, files, build script, classification (TESTED + READ)

- `git diff --name-only bcaf119...510124b`: exactly the 19 owned paths (`BACKLOG.md`, `Cargo.lock`, `crates/coagent-daemon/Cargo.toml`, `build.rs`, `src/{audit,engine,ipc,lib,main}.rs`, `tests/aw_{answers,disk,lifecycle,off,peer,record,seal,util}.rs`, `docs/M0-OUTCOMES.md`, `scripts/red-controls-daemon.sh`). Control range `bcaf119...184b35e` (main's lane): `BACKLOG.md`, four policy test files, `docs/M0-OUTCOMES.md`, `docs/POLICY.md`, a different set.
- The 13 protected and the 3 kept files, sha256 (first 16) at base / head, ALL EQUAL and equal to the builder's `:114`:
  - `gate_attacks.rs` b0f8d6b2bc2869a4; `gr2.rs` caee212babc8072b; `gr3.rs` eddd91ae98da52dc; `gr4.rs` bf8f2999dc657817; `gate_hostile/mod.rs` fa18b0bd9501b4e9;
  - `gate_r2.rs` a1944e0c65afb1c3; `gate_r3.rs` 17cfcca984130c79; `gate_r4.rs` a2ca92a68cc5e433; `gate_r5_model.rs` 022f47049bce6688; `gate_r6_model.rs` 755820e391466664;
  - `gate_r6_model_wrapper.rs` 2fb203a07390d43c; `gate_return.rs` d2ca677d7409133b; `common/mod.rs` 08ed3f585cf09a22;
  - kept: `release_audit.rs` 1ee5785a1412318d; `ipc.rs` 7ae8babc5d652f68; `dn_help.rs` 2cd8ee5f41e8c1b3.
- Every one of the 80 existing files under `crates/coagent-daemon/tests` and `crates/coagent-mcp/tests` at the base: blob-identical at the head (0 differing).
- `crates/coagent-audit-host/` tree `7808b4ddc5414b6a3f592a7d647ee54a9de130e7` and `src` `a0d4ef99e8c0b2b654575592fb578bf790f512b7` at both SHAs (= the builder's). `git diff --stat` over root `Cargo.toml`, `crates/coagent-mcp`, `crates/coagent-audit`, `docs/AUDIT-HOST.md`, `docs/DAEMON.md`: empty (0 bytes).
- `Cargo.lock`: `[[package]]` 164 → 164; the only change is `+ "coagent-audit"`, `+ "coagent-audit-host"` in `coagent-daemon`'s dependency list.
- Added lines: no `unsafe`, none of `OwnerAllow`, `decide_with_owner_allow`, `TerminalCommands`, `BypassView`, `decide_with_mode` (control: `unsafe` is found by the same grep in `coagent-audit/src/lib.rs`).
- `BACKLOG.md` `37 0` and `docs/M0-OUTCOMES.md` `13 0` (0 removed). `M0-OUTCOMES.md` at the base is a byte prefix of the head's. **`BACKLOG.md` is NOT a byte prefix:** item 9 requires dated lines UNDER existing entries, so they are inserted in the middle (9 places). Every base line is kept, in order (0 removed). Note N-9: the check's prefix test does not fit item 9's form; not a finding.
- `build.rs` `46 0`, red script `12 0`. The diff has two hunks in `build.rs`, the list `AW_RED` after `DN_RED` and the block at the end of `main`. No existing line moved or changed (a diff with 0 removed lines). The AW block is the DN block's form line by line (`rerun-if-env-changed`, `rustc-check-cfg`, name check, "cannot be set together" naming DAEMON, P1P, RR, WD, LA, DN, release refusal, warning, cfg).
- TESTED, short (own target `qaw/tp2`):
  - `COAGENT_RED_AW=no_such_name` → `panicked at crates/coagent-daemon/build.rs:376:9: COAGENT_RED_AW=no_such_name is not a known red control`;
  - `COAGENT_RED_AW=audit_always_on COAGENT_RED_DN=refill_keeps_spent_clock` → `build.rs:380:9: COAGENT_RED_AW cannot be set together with COAGENT_RED_DAEMON, …, COAGENT_RED_LA or COAGENT_RED_DN`;
  - `--release` with `COAGENT_RED_AW=audit_always_on` → `build.rs:389:9: COAGENT_RED_AW is for test builds only`;
  - control, no red variable: exit 0, no `RED CONTROL BUILD` warning.
- READ, no red variable: every `cfg!(coagent_red = …)` in `audit.rs` (`:183`, `:211`, `:269`, `:300`, `:330`, `:374`, `:541`, `:650`) and in the engine hunks (`:464-466`, `:1321`, `:2815`) is `false`, so each takes the correct arm. The removed `Action::Wake => self.wake_waiter(),` became `Action::Wake => { if cfg!(coagent_red = "seal_on_peer_message") { self.audit.red_seal(&self.id); } self.wake_waiter() }` (`engine.rs:2812-2819`). With the cfg false, that is the base's line verbatim in behaviour (the same call, unit value).

**Every changed line of `engine.rs`, `ipc.rs`, `main.rs`, `lib.rs`, classified** (`git diff -U0`, hunk by hunk; 81 + 14 + 17 + 1 added, 2 removed):

| File:lines (head) | Added | Class |
|---|---|---|
| engine `:107-113` `audit_refusal` | 7 | switch |
| engine `:162-165` `DaemonConfig::audit` | 4 | switch |
| engine `:210` `audit: false` | 1 | switch |
| engine `:338-339` `Engine::audit` field | 2 | lifecycle (holder) |
| engine `:377-379` `audit_refusal` in `run` | 3 | switch |
| engine `:463-468` `Audit::new(cfg.audit \|\| cfg!(red))` + red comment | 6 | switch; the `\|\| cfg!` and its 2 comment lines red branch |
| engine `:503` `audit,` | 1 | lifecycle |
| engine `:969-972` `restored` when not ended | 4 | lifecycle (open) |
| engine `:1216-1223` switch-absent `audit_seal` refusal | 8 | `audit_seal` |
| engine `:1311-1325` `AuditSeal` arms (incl. `seal_error_ends_the_engine` 3 lines + 2 comment lines) | 15 | `audit_seal`; 5 lines red branch |
| engine `:1520-1523` `status.audit` | 4 | status |
| engine `:1881-1890` record before the queue | 10 | record (R-6) |
| engine `:2188` `audit.close()` in `end_session` | 1 | lifecycle (close) |
| engine `:2446-2447` `created` (convener) | 2 | lifecycle (create) |
| engine `:2593-2596` `created` (joiner) | 4 | lifecycle (create) |
| engine `:2812-2819` (replacing 1 line) | 8 | red branch only (+ the base call kept) |
| engine `:3068` `audit.close()` in `shutdown` | 1 | lifecycle (close) |
| ipc `:32` `COMMANDS: [&str; 13]` (replacing `12`) | 1 | `audit_seal` |
| ipc `:45` `"audit_seal",` | 1 | `audit_seal` |
| ipc `:58-59` `AUDIT_OFF` | 2 | `audit_seal` |
| ipc `:151-157` `Command::AuditSeal` | 7 | `audit_seal` |
| ipc `:264-266` parse arm | 3 | `audit_seal` |
| lib `:26` `pub mod audit;` | 1 | switch (module) |
| main `:27`, `:50-54` USAGE | 6 | switch |
| main `:108`, `:134-142`, `:200` flag | 11 | switch |

**"Other" (= finding): 0 lines.**

## Task 9: the owner's rulings carried (TESTED + READ)

- TESTED by program (`python3 -I -B`): each of the four `- Card …` bullets of the lane brief's section 8 compared with the `> ` line under C-13 … C-16 of `CLARIFICATIONS.md`: **equal ×4** (sha256 prefixes `7d65bc5fd3c4cfdf`, `615334fdadc9e14d`, `889c7161ff5eb4a2`, `5891299d24d3f021`, the builder's). The C-numbers are 1..16, each once, and C-12 was the highest below C-13.
- The file before the append: I hashed the file's bytes `[0, 7677)`, everything before the blank line that precedes `## C-13` (that blank line and the rest are the append): sha256 `cc1d966de43340f1…` = **the builder's "old sha"**. For the record, bytes `[0, 7678)` (up to `## C-13`, the blank line included) give `beff8ce52ffcdbaf…`. The builder's figure is the file as it ended with its last C-12 line and one newline.
- Against the built code:
  - only the owner's command files the log (I-S1; task 2);
  - nothing a peer does can (I-S6; task 6);
  - the log keeps previews, not full text (D12; task 4);
  - the D12 card's option detail **"Full capture switched on per session" is NOT built** (no full tier other than the preview; BACKLOG's full-capture entry stays open, with the lane's dated line under it).
- BACKLOG lines of item 9 and addendum 1, each present once:
  - the three D-S lines (one under each of D-S1/2/3); the D5 line; the full-capture line; the m-2 line; the N-b line; the queue and timer lines;
  - N-r2-1, -3, -4, -5 and -6 entries, 1 each (N-r2-7: 0, R-11);
  - the G53 line 1; the 64 MiB line 1; addendum 1's line ("…never retries a seal by itself (AUDIT-WIRE addendum 1)") 1.

## Task 10: names and ids (TESTED)

`qa_scan.py` (copied from the last daemon check). My word list was passed only on the command line: the owner's names and handle, mail domains, this machine's user and host names (short and full), the home path, the drive and workspace path parts, the brain and key folders, the client names, the coordinator seats' names (as whole words), the mail-agent inbox names, the commit identity's domain, and this session's id (whole and its first 8 hex). Plus the scanner's id and UUID patterns.
- The 19 files at the head, WHOLE: 50 hits, **all in lines older than the lane**, all one coordinator's name as a whole word: `BACKLOG.md` 45, `engine.rs` 3, `M0-OUTCOMES.md` 1, `red-controls-daemon.sh` 1. Listed, not graded.
- The added lines alone (3,228 lines): **0 hits.** The ten commit messages: **0 hits.**
- Controls: a scratch copy of `aw_off.rs` with one planted line → 4 hits; a planted binary (NUL and 0xff around two planted words) → 3 hits. Both caught.
- Secret-shaped values in added lines: one, `format!("AKIA{}", "Q7".repeat(10))` (`aw_record.rs`), built at run time and made up. Every value I planted (task 4) is made up.

## Findings

Reproductions run from a copy of `gate_audit_wire_tests/` (the `.py` files side by side), with `<bin>` = a head build's `target/debug` and `<new dir>` a new short path. The scripts need loopback only.

**F-1 — MAJOR — an owner seal is answered "sealed" when the commit did not land.**
- **Where:** `crates/coagent-daemon/src/audit.rs:727-729` (`segment_before = host.status().map(|s| s.segment).unwrap_or(0)`), read by `act_on_err` at `:306` (row 7) and by `owner_seal` at `:749` (row 4).
- **What happens:** `status()` fails on any failing listing (store, archive, anchors, the session root). The seal can still reach its commit (writes need search rights, not read). A commit error then re-opens the store at the SAME segment k ≥ 1, and `k != 0` reads as "moved": the reply is row `7 (the commit landed)`, `sealed: true`, "sealed: the log was filed away and continues", and `status.audit.last_seal` says the same. In my run the segment stayed 1 and the host's `seals` stayed 1. This is the brief's NO GO class "reported 'sealed' … when the seal did not run" (section 3).
- **Reproduction:** `python3 -B qa_causes2.py <bin> <new dir> iii2` (look at `SEAL_UNDER_TEST` and `audit_after_restore`). Harness form: `qa_alpha.rs`, the `HAZARD` line.
- **Fix in words:** take the segment before the call from a read that cannot fail for a listing (the member's own `segment()`, through `host.member()`, which fails only with `Closed`). If it cannot be read, do not seal (answer "not sealed: give the command again") or report row 7/4 as "not known" (never "sealed"). Add an `aw_answers` case with an unknown segment before, and a red control.

**F-2 — Minor — the log can hold a record of a message that was not sent; a resend records it twice; two texts then say "not recorded".**
- **Where:** `engine.rs:1884-1902` (record, then queue, then `save_failed` → `Unqueue`); `audit.rs:661-674` (row 4: refused although the record landed); the SIGKILL window between the record and the outbox write.
- **What happens (three ways, TESTED):** (a) the data folder unwritable: the send is refused "state could not be saved", the message is not queued and never delivered, own seq +1; given again, own seq +1 again. (b) `LandedUnknown` on a record: refused with "could not record this message" and log "not recorded", but the record had landed (own seq +2 after the cause was removed). (c) kill between record and reply.
- **Impact:** the owner's log says this device sent a message it did not send; R-6 (nothing leaves without a record) holds.
- **Reproduction:** `python3 -B qa_causes2.py <bin> <new dir> open_a lu_record`.
- **Fix in words (needs a ruling, the order "record before queue" was ruled):** record a withdrawal event when the send is taken back or refused after a landed record, or word the replies "may have been recorded"; at least say so in `status.audit` and in the owner text.

**F-3 — Minor — "not sealed: nothing new to file since the last seal" is false while the store cannot be written.**
- **Where:** `audit.rs:207-213`, `T_NOTHING` (`:109`).
- **What happens:** step 0's checkpoint fails, `seal_export` cuts at the last stored checkpoint, and the answer is `NothingToSeal` with a record pending and no seal ever made (TESTED with `store/` 0500, and with the session folder removed while running).
- **Reproduction:** `python3 -B qa_causes.py <bin> <new dir> store_unwritable` (`probe.a_audit_seal`).
- **Fix in words:** word it "not sealed: nothing could be filed (nothing new since the last filed point, or the log could not write)", or compare `status().own_seq` with the last checkpoint before choosing the text.

**F-4 — Minor (for Friday to rule; section 1a (5)) — any reply with an id-shaped `re` is charged to the peer.**
- **Where:** `engine.rs:1886` (`item.re.as_ref().map(|_| s.rec.peer)`), against R-2 "when the send's `re` names that peer's message".
- **What happens (TESTED):** replies naming nothing and naming the daemon's OWN message are charged to the peer's requested allowance. 396 such replies fill it (row 10). After that, replies to the peer's real requests are refused until the owner seals. A local agent (through `coagent-mcp`'s `send`) can do this by mistake or on purpose; the peer cannot.
- **Reproduction:** `python3 -B qa_full.py <bin> <new dir> peer`; `qa_content.py` for the charge.
- **Fix in words:** charge the peer only when `re` names a message received from that peer (the daemon knows the received request ids while they are in its inbox; it would need to keep them after the ack), else `LocalHuman`; or rule the built behaviour.

**F-5 — Minor — the row-4 / Closed texts say "the audit log was opened again" when the re-open failed.**
- **Where:** `audit.rs:110-113` (`T_NOT_SEALED_REOPEN`, `T_LANDED_UNKNOWN`), `:104-105` (`T_REFUSED_REOPEN`), chosen at `:227-237` and `:275-286` before `open_now`'s result is known. `owner_seal` keeps the row-4 text when no status could be read (`:746-756`).
- **What happens (TESTED):** with `store/` 0300 the seal reply was "the audit log was opened again and its segment read: sealed only if the segment moved", while the state was `unavailable` and nothing was read. The log line "row 4: … the audit log was opened again" came right after "audit log unavailable".
- **Reproduction:** `python3 -B qa_causes2.py <bin> <new dir> lu_seal lu_record`.
- **Fix in words:** choose the text after `open_now`; when it fails say "not sealed (or not recorded): the audit log could not be opened again; see status.audit".

**F-6 — Minor — `status.audit.reason` loses the real cause, and a session whose log failed at creation can never get one.**
- **Where:** `audit.rs:499-501` then `:589-593` (`ensure_open` → `open_now` → `NotCreated` overwrites the reason).
- **What happens (TESTED):** `audit/` 0755 (or a file) when the session is set up gives the reason "audit/ is not a directory of this user with mode 0700". After the first send, `status` says "this session's log is missing or empty; it is never created again for a session that existed". The owner reading that may think a log was removed. Fixing `audit/` does not help: the session never gets a log (never created), so every send of this session is refused until it ends.
- **Reproduction:** `python3 -B qa_causes.py <bin> <new dir> auditdir_0755_at_create`.
- **Fix in words:** keep the creation failure's reason, and say "end this session and pair again to keep a log" (the daemon may also retry `create` within the same process while it has never created this session's log, since nothing was ever signed).

**F-7 — Note — `status.audit` says `state: "on"` with every field null and no reason while every send is refused** (the session folder removed while the daemon runs: the host object stays, its calls fail).
- **Where:** `audit.rs:769-791`.
- **Reproduction:** `qa_causes2.py … moved_running`.
- **Fix in words:** report `unavailable` with a reason when `host.status()` fails.

**Notes (no action required for the merge):**
- **N-1:** the 0700 check on `audit/` runs only when a session's log is created, not at a restart or mid-session (`audit.rs:499`). The host checks its own folders.
- **N-2:** `Audit::red_seal` is a `pub fn` compiled into every build (`audit.rs:761`); only a red build calls it.
- **N-3:** `state_not_saved`'s documented meaning (`ipc.rs:80`) does not fit the audit refusal (section 1a (6)). A dedicated code (or a doc line) would avoid a wrong reading.
- **N-4:** with the daemon's OWN state unsaved and dirty, `audit_seal` is refused by the base pre-check. A seal that landed can be answered "state could not be saved" if the post-reply flush fails (`engine.rs:1333-1337`, base code).
- **N-5:** the "unavailable" seal reply has no `limits` key.
- **N-6:** email addresses are not masked by `PatternRedactor` (a limit of `coagent-audit`): a preview can keep one.
- **N-7:** USAGE "its kind and a short redacted preview" leaves out the time and own number; "give the command again" does not say "after the cause is fixed".
- **N-8:** leftover temp files from stops accumulate (host P-5). At 64 in one folder the host refuses to open, and with `--audit` every send is then refused.
- **N-9:** `BACKLOG.md` cannot be a byte prefix by item 9's own form; 0 removed lines.

## Task 8 (red part): the whole red script at the head (TESTED)

- Rows counted (lines starting `  "COAGENT_RED` inside `ROWS=(`): **187 at `bcaf119`, 198 at `510124b`.** The 11 new rows: AW-1 `audit_always_on`, AW-2 `recreate_on_restore`, AW-3 `record_causer_always_local`, AW-3b `record_full_raw`, AW-4 `nothing_to_seal_retried`, AW-5 `limits_changed_read_as_done`, `landed_unknown_retried`, `commit_failed_retried_blind`, `seal_err_retried`, AW-6 `seal_on_peer_message`, AW-7 `seal_error_ends_the_engine`.
- Run: `bash scripts/red-controls-daemon.sh`, WHOLE (no `RED_ONLY`), from my clone's root at `510124b` (clean `git status`), `COAGENT_TOOLS=/private/tmp/claude-501/qaw/tools`, own empty target `qaw/tr`. Heavy counter before the start: 0, and no other `red-controls-daemon.sh` running. From 2026-11-26 03:31:56 to 2026-11-26 04:52:21. During it I ran only short runs (Python harnesses against built binaries, single test targets).
- Result: **198 of 198 `RED (as required)`, 0 `STILL GREEN`, 0 harness errors; `final clean run: green (76 test binaries; ignored under rulings: 2)`**; my sum of its `test result` lines: 331 passed, 0 failed, 2 ignored (= the builder's figures); exit 0. Every existing row (187) is red as before. My logs (`qaw/tools/tmp/m1-daemon-red/`, 199 files) name only my clone's path (528 path mentions, all `/private/tmp/claude-501/qaw/c`); none names the builder's worktree or target.

| Row | Variant | First panic line (my run) | Its own reason? |
|---|---|---|---|
| AW-1 | `audit_always_on` | `assertion \`left == right\` failed: status key paths, idle` | yes: with the switch absent the forced log adds the `audit` key |
| AW-2 | `recreate_on_restore` (at `510124b`, the corrected branch) | `… failed: a log was created over a session that existed: {"anchor_saved":true,…}` | yes: the rule it breaks, not a log-line count (the builder's correction holds) |
| AW-3 | `record_causer_always_local` | `… failed: the reply's record is charged to the peer's requested allowance: [PartStatus { used: (0, 0), …` | yes |
| AW-3b | `record_full_raw` | `… failed: the stored full tier is the redacted preview` | yes |
| AW-4 | `nothing_to_seal_retried` | `… failed: NothingToSeal is never retried` | yes (a second call) |
| AW-5 | `limits_changed_read_as_done` | `case 26 (seed 00a0d17e5ea10001, call Seal): seal: LimitsChanged { answer: Ok(..) } read as done (m-2)` | yes (m-2 read as done) |
| AW-5 | `landed_unknown_retried` | `case 18 (…): seal: the daemon seals again by itself for Err(LandedUnknown { … })` | yes (a second call) |
| AW-5 | `commit_failed_retried_blind` | `case 88 (…): seal: the daemon seals again by itself for Err(LimitsChanged { … SealCommitFailed … })` | yes (a second call) |
| AW-5 | `seal_err_retried` | `case 6 (…): seal: the daemon seals again by itself for Err(LimitsChanged { … })` | yes (a second call) |
| AW-6 | `seal_on_peer_message` | `… failed: a peer message caused a filed log` | yes |
| AW-7 | `seal_error_ends_the_engine` | `ctl inbox_read: no response` (`tests/common/mod.rs:625:43`, the helper, before the test's `alive(pid)` assertion) | **red for the right effect, named by the helper** (Note N-10). A variant that HANGS the IPC without stopping the daemon would also go red here, through the helper's time-out. Both break R-6 ("keeps answering"), so the row does guard what R-6 needs. It does not prove "the engine ended" as its name says; asserting the pid and an answer separately before the inbox read would. |

The four AW-5 rows each name the broken behaviour (a second `seal` call, or m-2 read as done), not a side effect. This answers task 2's last point.

## What was NOT checked

| Not checked | Why / where it rests |
|---|---|
| Anything of `--audit` on Windows | No Windows run in this check; the builder built `coagentd.exe` only. The Windows refusal text is READ only. |
| Rows 2/3 (`Reopened`), 8 and 12 (`LimitsChanged` / limits report), 11 (seal `Ok` with the host closed after), `ArchiveMismatch`, `ExportTooLarge`, `SealStaleTwice` by a real run | My rights-based means cannot make them (they need a poisoned store whose re-open succeeds with changed limits, a lying read-back, or a 64 MiB bundle). They rest on my own enumeration plus my harness over the head's public functions (task 1). |
| F-1's row-4 form (a `LandedUnknown` seal read against a fallen-back segment) by a run | The conditions that fail the read before also fail the re-open after. Harness only. |
| A disk that lies about a sync, a full disk, a slow disk, a power loss below the filesystem | Out of reach without a disk image (R-9 binds the lane; I used folder rights only). |
| `scripts/check.sh`, the Windows kit, `scripts/test-daemon.sh 3`, `scripts/test-p1p.sh`, `scripts/red-controls-audit-host.sh`, the whole three-crate `cargo test`, `cargo fmt`/`clippy` | Not run by ruling, or not required (Friday's merge check runs `check.sh` on the merged head). The daemon suite ran green as the red script's final clean run (76 binaries). |
| Main's `184b35e` merged into the branch | Not merged, not judged (Friday's rule). |
| The builder's `:104` heavy-counter discipline | Not graded (the builder's own discipline): its counter was not printed at the head test's start. |
| A second peer, a removed key, `session.end`/`leave` inside the hostile stream | A two-member session; ending would stop recording. |
| The 240/3 preview limits as a ruling | Still "PROPOSED, NOT RULED" in the crate; the owner's later call. |

Nothing of mine is left running: every daemon, relay and guard was stopped by its harness (each run's `left` list is `[]`), and a process check at the end found none of mine. Everything I made is under `/private/tmp/claude-501/qaw` and the two named folders; nothing in the project was written except my STATUS file.
