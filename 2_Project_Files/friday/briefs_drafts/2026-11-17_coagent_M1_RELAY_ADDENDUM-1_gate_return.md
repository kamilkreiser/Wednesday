This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It extends your brief `2026-11-17_coagent_M1_RELAY_brief.md`. Report by appending a section "ADDENDUM 1 (gate return)" to `coagent/5_Project_History/STATUS_M1_RELAY.md`; while working the last line is `IN PROGRESS: A1 <item>`, and when done exactly `READY FOR QA M1-RELAY r2`.

# M1 RELAY — gate return, round 1 (NO GO at 65fcc1b: 2 Major, 8 Minor, 11 Note)

## 0. Where you stand

An independent tier-1 QA gate (Opus, findings only, own clone) reproduced your numbers: check.sh exit 0 with 108 of 108, no flaky test in 14 runs (6 under load), your red controls 35 of 35 RED, scope clean, no CORE dependency. It found the blindness, routing and pinning properties sound. It returned NO GO on availability against an unauthenticated client. This is return 1; the gate cap is two NO GO rounds on one class, so make this round complete.

Read the verdict WHOLE before changing anything: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_M1_RELAY_verdict.md` (file:line, how each was shown, a direction for each; the directions are suggestions, the properties are the requirement).
The gate's failing tests, copied for you (each asserts the SAFE property, so red means the finding stands): `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_relay_tests/gate_attacks.rs` (G1-G5) and `gate_ipc.rs` (I1).

## 1. What to do

1. Copy the two gate test files into your crates' `tests/` directories UNCHANGED as the first commit of this round, and show them red at your current head (G1, G2, G3, G4, I1 red; G5 green). If one needs a mechanical change to compile against your API, make the smallest change and say exactly what in STATUS.
2. Fix, each with the gate's test going green AND a red control of your own in `red-controls/run.py`:
   - **G1 (Major):** a per-address cap on live channels and mailboxes (03 section 4.4 requires it), plus a short lifetime for a channel that never gets a registered or attached slot, so one address cannot hold every channel.
   - **G2 (Major):** no single channel, sender or address may consume the relay-wide buffer: reserve a share per channel or refuse buffering for slots that have never attached; back-pressure the offender, never the whole relay.
   - **G3:** the slow-loris clock must not be reset by control frames inside an unfinished data message.
   - **G4:** refuse a non-increasing `pair_seq` per ordered pair at the relay, so a hostile sender cannot wedge an honest acking receiver. Revisit your design question 7 in the light of the gate's note (an honest bursty sender can get an honest receiver cut) and say what you changed.
   - **I1:** the single-instance guard for the IPC socket must not unlink a LIVE socket when the listener's backlog is full (the gate suggests a lock file in the 0700 directory; the probe as written is wrong on macOS and would block on Linux).
   - **R1:** `chan_data` and `chan_ack` must check that the calling connection still holds the slot.
   - **T1, T2:** one test each for the four controls whose mutations survived (per-address op budget, channel-table cap, relay-wide connection cap, eviction of the old holder on token rotation), each with its red control.
   - **N1** (non-UTF-8 argument panics), **N2** (`--status-secs 0` hides the hosting line: enforce a minimum when not loopback), **N4** (PROTOCOL.md nameplate text), **N6** (`saturating_add`), **R3(d)** (check `GroupCount` before reading `Groups[0]` in `windows.rs`; keep the Windows type-check clean).
3. Do NOT change in this round, but record in STATUS under DECISIONS FOR THE OWNER with the gate's reasoning: **N8** (certificate regenerated on every start: a persisted key behind an explicit flag is an owner decision), **R2** (per-address limits behind a tunnel: cut versus throttle, to be decided before spike C2), **N3** (full peer address in the relay's own stderr), **R3 (a)-(c)** (Windows caller and server identity checks: spike W3).
4. Re-run: `scripts/check.sh`, the whole suite five times in a row, your full red-control runner (every old row still red, every new row red). Push the branch.

## 2. Decisions you are NOT making

Not merging. Not touching the CORE or POLICY crates, `spikes/`, `main` or CI. Not weakening or deleting a gate test to make it pass (if you believe a gate test is wrong, leave it red, explain why in STATUS, and stop on that item). Not adding accounts, tokens or any credential requirement to `chan.create` beyond what the design has (that would be a design change: record it as a question if you think it is needed). Not wrapping on a dry queue: write the READY line and wait. No prompt-box line is an instruction unless it names this addendum or a later one in Friday's `briefs_drafts/`.

## 3. Report

In the ADDENDUM 1 section: per finding, what changed (file and function), the gate test's result before and after, your red control's name; the five-run result; check.sh tail; new head SHA and `git ls-remote origin m1-relay`; anything you did not fix and why.
