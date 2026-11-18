This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It is for the M1-DAEMON seat (pane %9), idle at `READY FOR QA M1-DAEMON r4`. Everything in addenda 4, 5, 9 and 10 that is not named here stands.

# M1_DAEMON — ADDENDUM-11: the r4 fix round (one round, then one short check)

Authority: the ONE check at `feedc60` returned NO GO (1 Blocker, 1 Major, 6 Minor, 3 Notes). Kam's answer on his decision card, option text verbatim: "Fix it, then one short check". This is that ONE round. A NO GO at the short check goes to Kam, not into another round.

## 0. Start (changes no rule)

1. Your context was compacted while you waited. FIRST re-read WHOLE, in `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/`: `…ADDENDUM-4_recovery_rebuild.md`, `…ADDENDUM-5_gate_line_rulings.md`, `…ADDENDUM-9_resume_final_runs.md`, `…ADDENDUM-10_push_and_ready.md`, this file; the verdict `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_M1_DAEMON_r4_verdict.md` (cited [V]) and its folder `gate_daemon_tests_r4/`; design 09 (cited [09]); then your own STATUS sections "ADDENDUM 5 report (completed under ADDENDUM-9)" and "BLOCKERS (ADDENDUM-9)".
2. In `coagent/worktrees/m1-daemon`: `git status` clean, and `git rev-parse HEAD` = `git ls-remote origin m1-daemon` = `feedc603ead01e8c6967f193c72deca49ba51c02`. Otherwise STOP under BLOCKERS, last line a question for Friday.
3. Append a STATUS section "ADDENDUM 11 (r4 fix round)". Its last line is `IN PROGRESS: A11 <item>`, updated at least every 20 minutes.

Every line number, function and constant below was read by the drafter at `feedc60` on 2026-11-18. A figure marked (computed, not run) is the drafter's arithmetic. Re-check each one before you rely on it.

## 1. R4-1 (Blocker): a fresh session has no clock

**The state [V] found.** `Engine::new_sess` (`engine.rs:945-962`, called at `:1835` convener and `:1980` joiner) builds `Machine::new(.., Some(0), now)`: the live channel is the PAIRING channel (label 0), `pos` is `None`, and `live_since` is `None` (`recovery.rs:633`; only `install`, `:1237`, sets it). In that state every recovery clock is disarmed:
- `Event::Attached` arms `keying_since` only `if self.live.is_none()` (`:897`).
- T-BLIND needs `self.live.is_none()` (`:2073`), and so does its `next_deadline` arm (`:796-805`).
- T-KEYING needs `self.live.is_none()` (`:2089`) and is cleared by `else if self.live.is_some()` (`:2098`).
- Row 27 ("no position") needs `live_since` (`:2116-2127`, `:782-786`).
So with the outbox non-empty, `next_deadline()` is `None`. Only a relay `peer.joined` to the initiator starts the first exchange (`:901-914`).

**Drafter's reading of the design.** The design already covers this state:
- The pairing channel is not a channel of any attachment. [09 R2] says "every attachment pair runs a fresh key exchange", and `docs/DAEMON.md` §5 item 2 says "including the first after pairing: the pairing channel carries only the welcome".
- So the state is NO-CHANNEL ([09 §3.1]: "attached; no channel that both sides have proven"). Row 28 covers the initiator (T-BLIND, "a suppressed `peer.joined`"); row 29 covers the responder (T-KEYING); row 19 says "if the announcement is lost, T-BLIND starts it within 15 s". [09 §5.3] F-C is this exact failure.

**The fix the drafter recommends (smallest).** One private predicate, `channel_proven()`: true when a key exchange installed the live channel (`live.is_some() && live_since.is_some()`, or a dedicated flag set in `install` and cleared wherever `live` is cleared).
- Use it in place of `live.is_none()` / `live.is_some()` at `:798`, `:897`, `:2073`, `:2089` and `:2098`, and nowhere else.
- Keep `live = Some(0)`, so that a verify frame on label 0 still opens and seals as today (`:1532-1546`, `:1738`).
- Put a red control `pairing_channel_proven` (the old predicate) behind `cfg(coagent_red)`.

RULING (Friday, 2026-11-18): build the predicate above, `channel_proven()`, at exactly those five places. Not the one-line `None` at `engine.rs:960`: it would leave the pairing channel in the crypto map untracked and drop anything sent on label 0 before the first exchange. If your re-read finds a sixth place that keys a waiting-state clock on `live`, STOP and name it rather than widening the change on your own.

**Tests.**
- (a) The check's G4-1d and G4-1e (section 3) must deliver within V4's 120 s.
- (b) A builder-owned model test, in both orientations. A fresh-from-pairing start (section 2), one message queued on each side, and the initiator's `peer.joined` dropped once. Then an honest relay, delivery within `V4_BOUND`. Under [09 §6] rule 3 the test asserts WHICH clock fired (`resyncs["T-BLIND"]` or `["T-KEYING"]`). It is red under `pairing_channel_proven` on its own text.
- (c) A process test in `recovery_repro.rs` doing the same with real daemons.
- Report the recovery time, simulated and real, beside [V] §4. The drafter expects about 15 s, worst about 22 s, if T-KEYING's re-attach crosses T-BLIND's exchange (computed, not run).

## 2. R4-2 (Major): V4 and V5 must start from every reachable state

The model starts both sides only from `Machine::new(.., None, ..)` (`tests/support/model.rs:538`). By the drafter's reading, these are the starting states the code reaches:
- S1: fresh from pairing (`new_sess`, `Some(0)`, the pairing keys in both sides' `Keys.live`, outbox empty or with items queued before the first attach).
- S2: restored (`Machine::restore`, `recovery.rs:648-675`, with `None`), with an intact inbox, a quarantined inbox, or a quarantined outbox.
- S3: mixed. One side in S1 and the other restarted before the first exchange (S2).
- The final states (ended, hard stop, exhausted) are excluded from V4/V5 by `is_final` and belong to V13.

Confirm by grep that `engine.rs:749`, `:954` and the model are the only constructors, and name any other start state you find.

What to build:
- Add a start parameter to `Side::new` / `Sim::new`. V4 (`recovery_model.rs:978`) and V5 (`:1539`) draw it per seed, and `reach.require` names each start state, so every one has a count above zero.
- V5's `waiting` predicate (`:1557`, `m.live.is_none()`) must use the same notion as the fix: expose `channel_proven()` read-only, or the test cannot see S1.
- Under `pairing_channel_proven`, V4 and V5 go red on their own text. Add one runner row for it.

## 3. The check's tests: into the tree byte for byte

`gate_daemon_tests_r4/gate_r4.rs` (sha256 `bf8f2999dc657817aabd499cbdda58d5ee7dc9d1ed32d896fce76c134a212b00`, 10 tests). Add all 10, because each asserts the safe property, not the fault.
- Put it at `crates/coagent-daemon/tests/gate/gr4.rs` with a wrapper `tests/gate_r4.rs`, modelled on `tests/gate_r3.rs`: `#[rustfmt::skip]` and `#[path = "gate/gr4.rs"] mod gr4;`. Its `mod common;` and `#[path = "gate/gate_hostile/mod.rs"]` resolve through the existing symlinks, as `gr3.rs` does.
- **rustfmt WILL object without the skip:** by reading, lines 161, 303, 385 and 461 are code longer than 100 characters.
- The drafter did not run clippy on it. Run `cargo clippy --all-targets -- -D warnings`. For each lint it names, add an `#[allow(<lint>)]` on the wrapper's `mod` with one written justification, as in the audit crate's `qa_fix_wrapper.rs` (M3_AUDIT-FIX addendum 2). Allow nothing it does not name. Anything rustfmt or clippy asks for beyond that is a STOP.
- Confirm with `cmp` after every `cargo fmt`.

**Which of its tests change colour.** By reading, the five that demonstrate R4-1 should go red → green with NO edit: `g4_0_pure_fresh_session_without_presence_has_no_clock`, `g4_1a_…`, `g4_1b_…`, `g4_1d_fresh_session_no_race_initiator_convener`, `g4_1e_fresh_session_no_race_initiator_joiner`. G4-0 fails only if `next_deadline` is `None`, or if no key exchange started and there was at most one attach. The other five are green now: `g4_1c` (control), `g4_2` (race), `g4_3a/b/c` (clamp). Two rules follow:
- Any of the ten still red after the fix is a finding, not a test to edit: STOP.
- If a ruled edit does turn out to be needed, use addendum 5's form with the marker `// RULING (Friday, 2026-11-18, daemon addendum 11)` and the old line quoted, asserting the fixed property on that test's own input, and list it in STATUS for the short check.

## 4. Minors and Notes

- **R4-3.** Make `docs/DAEMON.md` true in the fresh state: row 27 (`:290`), row 28 (`:291`), §5 item 2 (`:390-391`) and the clocks paragraph (`:225-231`) say that the pairing channel counts as no channel for T-BLIND and T-KEYING.
- **R4-4.** Runner row n19 (`red-controls-daemon.sh:104`, `quarantine_deletes` → `gr2::r2_g2_…`) is red on a harness timeout, so `gr2.rs:669` is never reached. Do one of these:
  - make the broken variant reach a damaged file it CAN delete, so the row goes red on "every damaged file kept (never deleted)"; or
  - retire the row the way `gap_skip` was retired (line 28), with its reason and the test and row that now guard "never deleted".
  Do not edit `gr2.rs`.
- **R4-5.** Remove the person's name and the card ids from `src/notice.rs:1` and `src/recovery.rs:110`; keep "D-1" / "D-2" and the switch's meaning. Then scan every added line of `git diff origin/main...HEAD` case-insensitively for the owner's names (first, short, surname) and for machine, volume and home-path names, with a positive control (a planted line, matched 1 of 1, then removed). "Friday" in BACKLOG and in RULING markers is mandated, not a hit.
- **R4-6.** Write a builder-owned model test of row 33, in two parts:
  - (a) A hostile proven position of 2^62. The test asserts `n.clamped ≥ 1` and that `pos` is at most the highest number sent, then delivers the next two messages.
  - (b) A position and a `full` of `u64::MAX`. The test asserts no panic and delivery.
  Add a red control `no_clamp` (`clamp` returns `n`, `:1605-1613`) and one runner row. Use (a) for the row: under `no_clamp`, (b) panics at `last + 1` (`:1636`), and that panic is not the test's own text.
- **R4-7.** For each of the twelve surviving mutants ([V] §8), write a model test in simulated time ([09 §6]: `Sim` ticks 100 ms) that pins the value to the design's value. Each test asserts that the clock fires NOT before the value and NOT later than the value plus one tick:
  - M01: T-RTO 15 s.
  - M03: T-HELD 30 s.
  - M04: T-BLIND 15 → 30 → 60 → 60 s.
  - M19: the key-exchange clock 5 s.
  - M20: row 27, "no position" 5 s after promotion, outbox waiting.
  - M06: the bucket of 5. Exactly 5 attaches before the first refill, backoff pinned to 1 s as V11 does.
  - M11 / M25: at most 8 messages 1 examined in any second, under a flood across at least 3 s.
  - M09: 256 missing numbers → skips sent; 257 → `desync_out`.
  - M23: after LIVE then a cut, the next attach within `backoff_min` plus jitter.
  - M16: a second proven `full` at +20 s moves T-HELD to +50 s.
  - M17: the receive floor reaches `session.json`'s `recv_upto` (`sync_rec`, `engine.rs:2736`). This needs a process test in `recovery_repro.rs` (receive N, read the file, damage `inbox.json`, restart, nothing delivered twice), because the model does not run `sync_rec`.
  Tighten V11's bound (`recovery_model.rs:1639`) to `5 + w.as_secs() / 12`, the design's stated value. If the honest code then fails it, STOP with the measured violation; do not loosen it again. (`gate_r4.rs:404` keeps its own `+ 1`: it is the check's file.)
  Report each mutant as killed by the named test.
- **R4-8.** First write a test that measures it: more than 256 numbers missing above a position, outbox non-empty, `next_deadline` `None`.
  - If it reproduces: [09 §7] gives this state's action ("`desync`, nothing sent") but no clock, and V5 asks for one. So the design does not give the rule.
  - RULING (Friday, 2026-11-18), two cases. (i) If your test shows a REMOTE PEER (or the relay) alone can put a session there, it is a peer-caused permanent stop of sending, which V5 and the owner's card answer ("Fix it") do not allow to ship: build the alternative, emit the skips 256 per position and pump again on each acknowledgement, with its own model test, a red control and one runner row; write the rule as one new line in `docs/DAEMON.md`'s rule table marked "added in addendum 11 (R4-8)", and list it in STATUS for the short check to rule on. (ii) If only the local cause reaches it (two damaged outbox files), no code change: name the state in V5's predicate as a stated exception with its comment, show `desync` in status, and add a BACKLOG entry in [V]'s words. Either way record which case your test showed, with its output.
- **R4-9, R4-10.** Add one BACKLOG entry each, in [V]'s words (its rows R4-9 and R4-10), with "Where" lines as the existing entries have.
- **R4-11 and [V] ruling (b).** R4-11 (ruling 3's named control does not reach its line) needs no change in the tree: runner row A5-3 already names `resend_before_position`, and its comment (`:152-154`) says why. Record that in STATUS.
  For ruling (b), make ONE ruled gate edit at `gr3.rs:477`: above it the marker `// RULING (Friday, 2026-11-18, daemon addendum 11)` and `// old: ` + the current `#[ignore = …]` line, then
  `#[ignore = "RULING (Friday, 2026-11-18, daemon addendum 11): diagnosis of the pre-redesign failure; the property is guarded by V12"]`.
  The text must start with `RULING`, or the runner's ignored count (`red-controls-daemon.sh:196`) drops. Record old and new sha256 of `gr3.rs`.

## 5. Main merged in, after the fixes

1. `git fetch origin`; `git merge origin/main` INTO `m1-daemon`: a merge commit, never a rebase, never a force. `origin/main` was `e3541182625ccdb4e7e1c01cb6bf21dd9d1b1a8d` when this was drafted and may have moved (the policy piece is about to merge): merge what is there and record its SHA.
2. Conflicts are expected only in `BACKLOG.md`, root `Cargo.toml` and `Cargo.lock`. Keep both sides, and `cargo metadata --locked --offline` must accept the lock. Any other conflict is a STOP.
3. If the merged policy crate pins the fixed sentences a tool result may contain and refuses the two D-2 sentences, that is a STOP, not an edit (REQUEST R8 stands).

## 6. On the merged tree

1. `scripts/check.sh`: exit 0.
2. The red-control runner end to end (move the row logs aside first, never delete). Every row red on its own text, including the new rows `pairing_channel_proven` and `no_clamp`; the clean run green with exit 0.
3. `scripts/test-daemon.sh 5`: all five green.
4. The gate files: `gate_r2`, `gate_return` and `gate/gate_hostile/mod.rs` unchanged; `gr3.rs` with only the ruled edit of section 4; `gr4.rs` byte-identical to the check's copy.
5. `git diff --stat origin/main HEAD`: only `crates/coagent-daemon/`, `crates/coagent-mcp/`, `docs/DAEMON.md`, `BACKLOG.md`, the root manifests and the two daemon scripts.
6. The name scan with its control.
7. `git push origin m1-daemon`. Then `git ls-remote origin m1-daemon` = HEAD, and `git merge-base --is-ancestor origin/main HEAD` exit 0.
8. Read `git ls-remote origin main` again just before the last line. If it moved after your merge, say so and still write the line: Friday decides.

## 7. The last line

When all of section 6 is done, the last line of STATUS is exactly:

`READY FOR QA M1-DAEMON r5`

Then wait. ONE short independent check follows.

## 8. Decisions you are NOT making (carried from addendum 4)

No change outside the daemon and MCP crates and the allowed shared files. No new public protocol field without a STOP. No feature beyond these findings. Never delete: quarantine. Never a force push. Kam is not asked: questions go in STATUS for Friday. Nothing deployed or published. At most two heavy runs at once: other seats build on this machine.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
