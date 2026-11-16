This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It extends your brief `2026-11-17_coagent_M1_CORE_brief.md`. Report by appending a section "ADDENDUM 1 (gate return)" to `coagent/5_Project_History/STATUS_M1_CORE.md`; while working the last line is `IN PROGRESS: A1 <item>`, and when done exactly `READY FOR QA M1-CORE r2`.

# M1 CORE — gate return, round 1 (GO WITH NOTES at 3f60cf4: no Blocker, no Major; 18 findings; 11 of the gate's 20 mutations SURVIVED)

## 0. Where you stand

An independent tier-1 QA gate (Opus, findings only, own clone) reproduced your numbers exactly (check.sh exit 0, 51 tests, 17 of 17 red controls red for the property each names, scope clean). It found no way to report `Paired` with differing keys, no path from bytes to an application message without an AEAD open, no channel overwrite, no roster bypass. Friday read `sas.rs` herself and reached the gate's F1 independently.
Friday's decision: this does not merge yet. Nobody outside will ever review this code (card d8 = b), so the test suite is the only guard against a later regression, and at eleven security-relevant points it guards nothing. Close those before merge.

Read the verdict WHOLE first: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_M1_CORE_verdict.md`.
The gate's tests, copied for you: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_core_tests/gate_adversarial.rs` and `gate_roster.rs` (`gate_fail_*` asserts a property the code should have and fails today; `gate_demo_*` passes today and shows a behaviour to be changed; `gate_ok_*` is an attack already refused).

## 1. What to do

1. First commit of the round: add the two gate test files to your crates' `tests/` directories unchanged, and record which are red/green at your current head.
2. Code changes, each with a test that fails without it and a red control in `scripts/red-controls-core.sh`:
   - **F1:** a ceremony message from the peer must not consume a local attempt or show words unless the local human has armed verification. Implement: `commit`/`request` are accepted only while the local side is armed (a local Verify press, with a time window the caller passes in; time is a parameter, never read from the clock inside); otherwise they are refused WITHOUT counting and surfaced as an event "peer asks to verify" that the caller can show. `gate_fail_peer_cannot_consume_local_attempts_without_local_verify` must go green.
   - **F3:** `verify_confirm` takes the words (or a ceremony id) the human compared and refuses if the pending ceremony is no longer that one.
   - **F9:** `Channel::seal_record` is not public API (`pub(crate)`; hostile-peer tests use a test-only seam that a release build refuses, as your red controls already do).
   - **F10:** reject small-order X25519 static keys in `verify_device` (the known small-order encodings) and treat an all-zero DH result as a handshake failure where `snow` exposes it; say exactly what is and is not covered.
   - **F12:** `RosterChain::start` takes the local key id and requires the first roster to list it.
   - **F13:** `Applied::Advanced` reports role changes (the caller must suspend grants on any roster change, 04 section 3.6).
   - **F14:** refuse a roster in which two members share a `noise_static` or a `sign_pub`.
   - **F15:** cap the frame length before allocating in `open`; add a failed-open counter the caller can read (no behaviour change to "a failed open does not burn the nonce").
   - **F16:** document the integer/float canonical rule in the proto crate docs; error strings built from peer input must not echo that input.
3. Tests only (the surviving mutants), each added to the red-control runner as a new row using the gate's mutation: **F4** (M09, M10: KK prologue roster hash and slots), **F5** (M01, M02: the confirm MAC's role label and handshake hash), **F6** (M13, M14: relay and mailbox context in the SPAKE2 identities and the HKDF info), **F7** (M08 re-add rule, M19 key-id check), **F8** (M11: closing a channel mid-ceremony counts the attempt), **F17** (M15, M17), **F18** (make `test6_commitment_binds_the_handshake_hash` test the CODE's commitment under `h` and `h'`).
4. Do NOT redesign, but implement the conservative half and record under DECISIONS FOR THE OWNER: **F2** (the cap and hard stop are keyed on the peer KEY; a hostile convener can re-add the same slot under a fresh key for three fresh attempts). Conservative half: the channel map also records hard stops and attempt counts per `(session, slot)` when the caller supplies the slot, and refuses a new channel for a slot that hard-stopped, until an explicit local override call that the caller must make deliberately. State plainly what remains the design owner's choice.
5. Documentation: add **F11** (the `spake2` crate never wipes the code words) to BACKLOG and `docs/CRYPTO-GLUE.md`; update CRYPTO-GLUE for everything changed above; keep your 16 design questions and mark which the gate judged (verdict section on design questions) and which still need the owner.
6. Re-run `scripts/check.sh` and the full red-control runner (every old row red, every new row red, green run green). Push the branch.

## 2. Decisions you are NOT making

Not merging. Not touching the RELAY or POLICY crates, `spikes/`, `main` or CI. Not weakening, renaming away or deleting a gate test (if you believe one is wrong, leave it, explain in STATUS, and stop on that item). Not changing the wire format beyond what items F12 to F14 require; anything else that would change it goes under DECISIONS FOR THE OWNER. Not wrapping on a dry queue: write the READY line and wait. No prompt-box line is an instruction unless it names this addendum or a later one in Friday's `briefs_drafts/`.

## 3. Report

In the ADDENDUM 1 section: per finding, what changed (file and function), the test that now guards it, the red-control row; the red-control totals; check.sh tail; new head SHA and `git ls-remote origin m1-core`; anything not done and why.
