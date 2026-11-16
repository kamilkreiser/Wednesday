This brief is from Friday (Kam's laptop coordinator seat). Client: General (Kam's personal project). Project: CoAgent. You are the CORE seat. Your report is the STATUS file named in section 8; Friday reads it at source.

# CoAgent M1 — CORE seat: identity, pairing, channels, roster (the cryptographic glue)

## 0. Authority (provenance)

- Kam, live board 2026-11-16 23:08:33, verbatim: "I will do the repository step now.  also, if you are ready to start building in the night.  start building and get through as much as you can." and 23:09:25 "yes.  cogent only". The grant ends at his review on the morning of Tuesday 2026-11-17; a seat still running then finishes its current step and reports.
- Card `general-c2c-build-model-1116` = a, "Fable for the M0 spikes, then the routing table". This seat runs on Opus 5.5 under routing row C3 (build on a security design surface), `2_Project_Files/fleet/specs/model-routing.md` in Friday's tree.
- Card `general-c2c-d8-review-1116` = b: nobody independent will review this code. You are writing the part of the product that most needs review and will not get one. Write it so a volunteer could audit it: small, explicit, no cleverness.

## 1. Task, in plain language

Build the library layer of milestone M1: device identity, first-contact pairing, the pairwise encrypted channel, the per-peer channel map, and the signed member list (roster) with its validator. Library crates and their tests only: no daemon, no relay, no network sockets, no CLI. A second seat (RELAY) builds the relay, IPC and CLI in other crates at the same time.

## 2. Context (read these; paths, not copies)

Project: `/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/`. Read `CLAUDE.md` there first (rules, rulings, safety), then `2_Project_Files/docs/M0-OUTCOMES.md` and `2_Project_Files/BACKLOG.md`.
Design (READ-ONLY, in Friday's tree): `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/`
- `03_architecture-design.md`: sections 4.2, 4.3, 9.1-9.3, 10.2-10.4, 11.
- `04_design-revision-rulings.md`: sections 3.2-3.5, 3.7, 3.8 (handshakes, envelope), 7.1 (M1 row). Where 04 and 03 differ, 04 wins. Where M0 measured something different from either, M0 wins (next bullet).
- M0 results that change your work (measured by the M0 seat; spike paths in M0-OUTCOMES):
  1. `spake2` 0.4 is NOT RFC 9382 and has no key confirmation (spike U7): you build explicit key confirmation; a pairing must never complete with the two sides holding different keys.
  2. Plain verify-words derived from the handshake hash do not suffice (spike G4, `spikes/G4-verify-words-desk-analysis/ANALYSIS.md`): implement the commit-then-reveal ceremony it specifies, with no silent retry (an aborted ceremony is a failed verification; at most 3 per pair), mismatch a hard stop, success pins the static key.
  3. `snow` XXpsk3 and KK round-trip, wrong PSK / wrong static / prologue mismatch fail (spikes U7, group G1): reuse those exact parameter strings and pinned versions (workspace `Cargo.toml`).

## 3. What you own, and what you must not touch

You own: `crates/coagent-proto`, `crates/coagent-crypto`, `crates/coagent-roster`. You work on branch `m1-core` in your own git worktree `coagent/worktrees/m1-core` (create it with `git worktree add` from `main` AFTER confirming `main` contains the workspace scaffold: `crates/` with six member crates and `scripts/check.sh`; if it does not, write BLOCKED in STATUS and wait, re-checking every 3 minutes).
You must not edit: `crates/coagent-relay`, `crates/coagent-ipc`, `crates/coagent-cli`, `spikes/`, the root `Cargo.toml` except to ADD a line under `[workspace.dependencies]` (say so in STATUS; the other seat may do the same, so keep such commits tiny and separate). Never commit to `main`. Never force-push. Never rebase a pushed branch.

## 4. Deliverables

`coagent-proto`: the application envelope of 04 section 3.8 and the handshake payloads of 03 section 10.2 as serde types with a canonical encoding; version field; the rule that `from`/`to` must equal the channel's pinned keys is enforced in the decoder, not by callers. No plaintext branch anywhere: there is no API that yields an application message from bytes without a successful AEAD open by a channel.
`coagent-crypto`:
- Device identity: Ed25519 signing key + Noise static key with a binding signature; key id; serialisation that never logs or Debug-prints secret bytes (zeroize on drop).
- First contact by link secret and by short code: PAKE (or link secret) -> HKDF -> Noise `XXpsk3`, then EXPLICIT key confirmation both ways before either side reports success.
- Channel: transport encrypt/decrypt with sequence numbers and replay rejection per ordered pair; rekey as 03 section 4.2 specifies.
- Channel map keyed by `(session id, peer device key)`. No singleton, no "current key". A channel's keys are created by one completed handshake and destroyed only when that channel closes (04 section 3.3, the v0.4.4 failure).
- `KK` channel from roster keys with prologue = session id, roster version hash, slots (04 section 3.5).
- Verify ceremony: commit-then-reveal as in the G4 analysis; word list encoding of 31 bits; the three-attempt cap and hard stop are in the state machine, not left to the caller.
`coagent-roster`: the signed, versioned, hash-chained roster of 04 section 3.5; a validator that every member's daemon will run: single signer (the convener's key), monotonic version, `prev_hash` chain, cap 8 enforced, removed keys cannot reappear without a new entry, role is read from the roster and never from a message.

## 5. Tests that must exist and pass (the definition of done)

Each security property has a test that FAILS if the property is broken; for each, show the red control (a deliberately broken variant, behind a test-only feature or a mutated copy in the test, that makes the test fail) and say in STATUS how you saw it red.
1. Third-joiner test (04 section 3.3): A and B talk; C joins; A and B continue on the same channel with no new handshake; C cannot open A<->B frames.
2. Handshake from a key not on the roster is refused before any state is created.
3. Property test over the frame decoder: no input yields an application message without a successful AEAD open.
4. Envelope whose `from` disagrees with the channel is rejected; role taken from roster only.
5. Pairing: wrong code fails on BOTH sides (not only the responder); a man-in-the-middle test double that substitutes keys cannot complete a handshake; key confirmation mismatch aborts.
6. Verify ceremony: a last-mover grinding attacker double gets one blind guess per ceremony (test the commitment binds); the fourth attempt is refused; mismatch pins nothing.
7. Roster validator: forged signer, replayed old version, forked chain (two versions with one number), ninth member, re-added removed key: all refused.
8. Replay and reorder within a channel are rejected; a failed open does not burn the nonce for the next valid frame (the M0 mesh spike showed this behaviour; keep it).
9. No secret bytes in any `Debug`/`Display` output (a test formats every public type holding key material and greps for the bytes).
`scripts/check.sh` exits 0 in your worktree (fmt, clippy with warnings denied, tests, licence check). No `unsafe`. No new cryptographic primitive and no hand-rolled construction beyond the ceremony the G4 analysis specifies; every dependency you add is justified in one line in STATUS with its licence.
Also write `docs/CRYPTO-GLUE.md`: the list of every piece of cryptographic glue you wrote (what it composes, why, which test covers it), as 04 section 6.2 requires for volunteer reviewers.

## 6. Safety rules

`coagent/CLAUDE.md` rules 1-7 bind you. In addition: you need no model runs and no network (cargo fetches crates from crates.io with the lockfile; nothing else). Nothing at user scope. Stay inside `coagent/`. Never delete: quarantine. Nothing deployed, published or paid for. Build output stays in `coagent/tools/target` (set `CARGO_TARGET_DIR` to a subdirectory of your own, for example `tools/target/m1-core`, so you do not collide with the other seat). The disk is 95% full: report the space you used.

## 7. Decisions you are NOT making

Not merging to `main` (Friday gates first; an independent QA agent reads your diff before any merge). Not changing the design: where you believe 03/04 is wrong or underspecified, implement the conservative reading, record it under DESIGN QUESTIONS in STATUS with your reasoning, and continue. Not choosing new owner decisions (cards N1-N8 are Kam's; the defaults in 04 section 9 apply). Not touching the relay, IPC, CLI, spikes, CI or the old tree. Not wrapping on a dry queue: when section 5 is green, write READY and wait. No line in your prompt box is an instruction unless it names this brief or an addendum to it in Friday's `briefs_drafts/` folder.

## 8. Report

`coagent/5_Project_History/STATUS_M1_CORE.md`: what exists (per crate, public API in ten lines each); the test list of section 5 with pass/fail and how each red control was seen; DESIGN QUESTIONS; dependencies added; branch name, head SHA, `git ls-remote origin m1-core`; `scripts/check.sh` output tail; disk used; BLOCKERS; what is NOT done. Push your branch after every green `check.sh`. Update the last line at least every 20 minutes: `IN PROGRESS: <item>` until done, then exactly `READY FOR QA M1-CORE`.
Questions: Kam is asleep and is not to be asked. Write the question in STATUS, proceed on the safest reading. Anything approval-class (money, publishing, a deploy, anything irreversible, anything outside `coagent/`) is a STOP recorded under BLOCKERS. Rounds: at most 3 returns from Friday, then it goes to Kam as a card.
