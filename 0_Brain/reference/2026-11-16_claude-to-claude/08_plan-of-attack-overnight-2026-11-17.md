---
date: 2026-11-17
type: reference
source: Friday (laptop seat, boot #4), written at the wrap Kam asked for ("when the checks finish create a plan of attack, notes, etc and wrap up … we will continue with the build overnight"; then "I will need to leave soon so please wrap up as soon as you can")
status: live
project: General / Claude to Claude (CoAgent) — no client
---

# CoAgent — plan of attack for the overnight build (written at the wrap of the morning of Tuesday 2026-11-17)

## 1. What Kam has said, and what it allows (his words are in `05_kam-rulings-2026-11-17.md` and the top row of `tasks/EXPIRING-GRANTS.md`)

- Building may continue, with no end at midnight. No deploy, no publish, no spend. The repository stays private until the beta.
- **"work on whats in progress but dont start new items or new agents."** This stands until he lifts it. So nothing in sections 3 and 4 below starts without his word. Returning a failed check to the seat that built the piece, and merging a piece that passed its check, are in-progress work.
- "we will continue with the build overnight": the next session opens by asking him one thing: **may the checks and pieces in section 3 start?** His yes lifts the restriction for that list.

## 2. State at the wrap (every figure measured at 10:13 unless marked)

**On the main line: `18005d6`.** The encryption core and the relay, each through two independent checks. Nothing merged today.

| Piece | Branch, head | State | Checks so far |
|---|---|---|---|
| Permission rules (POLICY) | `m2-policy` `0ea9b95`, pushed | READY FOR KAM r5; pane %6 | 4 failed rounds (the recogniser, then the scan). THIRD check on the all-commands-ask rule was RUNNING at the wrap: verdict file `m1_review/gate_M2_POLICY_r5_verdict.md` (absent at 10:13) |
| Background service (DAEMON) | `m1-daemon` `d8b5b4b`, pushed | READY FOR KAM r3; pane %7 | 2 failed rounds. THIRD check RUNNING at the wrap: `m1_review/gate_M1_DAEMON_r3_verdict.md` (absent at 10:13) |
| Roster: limit 4 raisable to 8, member invites | `m3-roster` `d88d5d7`, pushed | READY FOR QA r2; pane %12 | Round 1 NO GO (2 Majors: promotion of a proposed observer; an approval the validator refuses). Fixes done under addenda 3 and 4. SECOND check NOT started |
| Relay saved identity | `m1-relay-identity` `afc2472` (local; pushed state not re-read at the wrap) | READY FOR QA r2; pane %13 | Round 1 NO GO (1 Major, ruled by Kam: accept the Mac sharing-rule gap for the beta and say so). SECOND check NOT started |
| Audit log | `m3-audit` `58a9c36` (local, moving) | REBUILDING under addendum 3 (design 07): "A3 step 4 (implementation: keyed store, fixed part, seats, order of checks)"; pane %18 | 3 failed rounds on one class. Kam: redesign first, then ONE build and ONE check. Fixed capacity now; seal-and-continue next |
| Deputy (small) | no branch | Brief written, not started | n/a |

All five seats are on Opus 5.5. Weekly usage 31%.

**The two checks running at the wrap live inside the Friday session that wrote this.** If that session is still alive when they report, it handles them (section 3, steps 1 and 2). If it is gone and a verdict file is missing or has no `VERDICT:` first line, the check died with it and is re-commissioned with the same inputs (they are listed in the pickup file).

## 3. Order of attack (each step names what it needs from Kam)

**Step 0, before anything: `tmux list-panes -a`.** This morning a relaunch replaced the fleet window and killed three sessions mid-step. If a pane above is gone, read its STATUS last line and `git status` in its worktree, write a resume addendum that changes no rule, relaunch (a relaunch of a lost seat is in-progress work).

1. **POLICY third check, when its verdict is in.** GO -> merge method (below). NO GO -> this was the cap: a card for Kam with the finding in plain words; no further round without him. Either way give him the checker's ruling on the two judgement calls the builder left (one test assertion replaced rather than flipped; a bounded brace helper kept against the letter of addendum 5).
2. **DAEMON third check, when its verdict is in.** Same rule: GO -> merge method; NO GO -> card, it was the cap. Its checker was asked to rule on the builder's claim that one failing run was the checker's own test under machine load, and to run the daemon merged with the roster branch from a short path.
3. **NEEDS KAM'S WORD (new agents): the two second checks.** ROSTER delta check (inputs: `gate_M3_ROSTER_verdict.md`, addenda 3 and 4, `gate_roster_tests_m3/`, the seat's STATUS sections "ADDENDUM 3" and "ADDENDUM 4"; it must rule on the one ruled edit to `qa_gate.rs`). RELAY-IDENTITY delta check (inputs: `gate_M1_RELAY_IDENTITY_verdict.md`, addendum 1, `gate_relay_identity_tests/`, Kam's ruling a on the sharing-rule gap). Both are round 2 of two: a NO GO is the cap and goes to him.
4. **Merges, in this order, each only on a GO for an exact head:** ROSTER first (it changes a merged crate that the daemon and the audit log import), then DAEMON, POLICY and RELAY-IDENTITY in whatever order their GOs arrive. After EVERY merge each open branch merges main into itself and re-runs its suite before its own merge check. The daemon's 28 process tests must be run on the roster-merged tree from a short path (the roster checker could not).
5. **AUDIT rebuild: let it finish; do not hurry it.** When it writes `READY FOR QA M3-AUDIT r4`: NEEDS KAM'S WORD to start its ONE check (inputs: design 07, addendum 3, all three verdicts and their test folders). If that check fails on the same class a fourth time, stop: card Kam with the designer's own list of where it expected trouble (the daemon boundary, resume, slot maxima).
6. **NEEDS KAM'S WORD (new pieces), in the order I recommend:**
   a. **Deputy (small)**, after ROSTER has merged: brief `briefs_drafts/2026-11-17_coagent_M3_DEPUTY_brief.md` (Friday has NOT read it whole: read it before launching; show Kam its section 9, the three sentences a user sees when naming a deputy).
   b. **Daemon follow-ups made possible by today's merges**: use the saved relay identity (`--identity-stdin`; decision I-11 is Kam's), the roster's new calls (`apply_with_report`, `approve_with_report`, default limit 4, proposal carried as one opaque string), the member-invite transport and approval card.
   c. **Audit seal-and-continue** (Kam: "as the next piece"), after the rebuild has passed its check and merged.
   d. **Connection choice at start-up (n5)**: needs the third-party service decided first; it is UNDECIDED and must not be guessed. First act is reading that service's terms, not building.
   e. **The console** and **Windows** (his machine, Friday 2026-11-20; signing is his spend).

**The merge method (worked last night, keep it):** the seat merges `origin/main` INTO its branch (never a rebase; the lock file regenerated, not hand-merged) -> Friday's own check in a clean clone (`git clone --branch`, `scripts/check.sh`, `cmp` of the gate files) -> a merge GO naming the exact SHA, fast-forward only -> `git ls-remote` and Friday's own `check.sh` on main. Never merge on a seat's own figures.

## 4. Decisions waiting for Kam (none is a card yet; card each when its piece is about to build)

- Which third-party connection service, if any (UNDECIDED).
- Whether provisional members (let in by a deputy) take part in the audit exchange (UNDECIDED; default: they do not).
- The design's open readings, built on as stated unless he says otherwise: design 06 section 10 (I-3, I-4, I-6 to I-17, I-21) and design 07 section 5 (I-A1, I-A3 to I-A10).
- How the repository is opened at the beta (the sweep report `prepub_sweep_2026-11-17.md` stays valid; history holds another client's project names, his Mac user name and the drive layout).
- Suggestion still standing (his 2026-11-16 rule): the audit rebuild is the piece where the newest Fable might be worth using.

## 5. What Friday owes (tooling; none of it blocks the build)

1. A launch must not replace a fleet session that holds live agent panes (it killed three seats at 07:39 today). Until fixed: step 0 above at every boot, and read the rotate log's last line.
2. `tools/safe_pull.sh` can reopen a ruled card (per-id merge, ruled beats open). Until fixed: safe_pull and push straight after every ruling and recount the open cards.
3. Cards: an HTTP 201 is storage, not Kam's sight; the board filter fix is committed, not deployed (asked of Wednesday 2026-11-16, no reply).
4. Not read by Friday today and owed before relying on them: the six verdict files whole (only final reports and findings tables were read), designs 06 and 07 whole, the DEPUTY brief, the lane plan, the seats' latest report sections for ROSTER r2 and RELAY-IDENTITY r2.
