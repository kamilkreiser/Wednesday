---
date: 2026-09-06
type: pickup
source: replaced wholesale at the 2026-09-06 09:5x rotation (seat 08:5x); the 09:1x version's items are either actioned or carried below
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — fleet OPEN, two fresh seats + two gates running, SEAT B owed (2026-09-06 09:5x)

**The 2026-08-28 run-until-empty grant is in force, and Kam's 09:42 grant adds a SECOND Secuura seat in parallel this weekend.** Live: NexusAI S41 (`%72`, launched 09:42, HOLDING for the RD-340 round-3 re-check `%71` on `9401f6f`), Secuura s138 seat A (`%74`, launched 09:47 on the amended brief), the KS-386 tier-1 tester `%73` on `8b91ab0ae` (~45 min from 09:42). **Their state lives in today's daily note** (the 09:29 checkpoint block, the 09:5x rotation block and every line after) — this file is only the pointer.

## The successor Wednesday's FIRST ACTS (in order)
0. `tools/kam_rulings_today.sh` (THREE messages today: 09:36 the Backlog-project idea; 09:42 reassign-all + aggregate + a second seat; 09:45 aggregation WITHDRAWN + the Linear plan UPGRADED) + `decision_queue.sh list open` (= 0). The panel replies stand; nothing owed to Kam.
1. **s138's plan confirmation** (if not already answered by the rotating seat) — confirm against `briefs_staged/s138_successor_brief.md` (items 0(a) reassign every Platform K ticket to us with the human exceptions listed; 0(b) FILE the five unfiled tickets as five; 0(c) nothing — aggregation withdrawn; hold #839).
2. **SEAT B — `s138b`, the harness partition:** write its brief (pattern: `s138_successor_brief.md`'s PARTITION section — `__tests__/`, `systemTest/`, `tests/`, `scripts/`; queue: the KS-833 residue PR (F-2/F-3/F-4/F-6 + F-7 from the KS-833 gate report `2026-09-06-s137-ks833-838-pass1-04830344e/`), then KS-842, then the bare-listen ticket once s138 files it; its OWN `git worktree` at `2_Project_Files/../worktrees/seat-b` off `develop` re-read at boot; one PR per ticket, Peter requested, HELD; merges only on Wednesday's GO re-derived against the develop tip — two seats move develop under each other). Send through the gate (KS-833 TND + KS-842 Backlog P3 ticket-state lines are in `s138_successor_brief.md`'s provenance; re-read them). Launch: the Secuura launcher launches into `2_Project_Files` — seat B must `git worktree add` FIRST THING and `cd` into it for all work; name the pane `Secuura/Blockchain-B` (check `cockpit.sh` routing — `send_brief.sh --to` needs a routing entry for a second Secuura seat, or the mail goes to the same inbox `secuura-blockchain@` with `[SEAT B]` in the subject and both seats told which mails are theirs — the cheaper path; decide, say which).
3. **The RD-340 round-3 verdict** (`%71`, ~10:00) → PASS: GO to S41 to merge `9401f6f` explicitly `--no-ff` into `05606f5` (re-read), RD-340 Release Ready; NO GO: the findings as a fix round (the class's first NO GO). Score the QA + S40's round 3 (S40 is wrapped — the round score goes on its session row's notes). `pane_close.sh %71 47787 6882 3001 8731`.
4. **The KS-386 tier-1 verdict** (`%73`, ~10:30) → PASS with the behavioural proof DRIVEN: GO to s138 to merge #839 sha-asserted against the develop tip re-read, KS-386 → TND; "PASS but the proof still owed": NOT a merge GO — rule the owed leg first; NO GO: fix round r2/2. `pane_close.sh %73 …`.
5. **Owed by Wednesday, not started:** the Secuura category-1 LIST (from the board with the WHO predicate → `projects_index/entries/Secuura__Blockchain.md`, quoted in the next briefs — both seats select from it); the 13 NexusAI ruled cards' `--delivered` marks from S40's comment ids (37168–37174 + the seven prior records — a per-card Jira read, bounded); the `coagent@`-sender line into the other QA prompt templates; the watcher `HOLDING until <event>` candidate (FILE or DISCARD at the retro).

## Still Kam's (carried honestly; nothing blocked on him)
1. **Peter and Stuart must be told not to fix KS-790 in isolation** until KS-781's authorize fix lands — external comms, Kam's alone.
2. **RD-303 ruling** (untrack the six `4_Credentials/.azure/` files — committed history) and **RD-75** (the authorisation-chain gap) — both owed a card, neither carded.
3. **`Secuura/Blockchain/4_Credentials/Secuura-git.rtf`** — second live copy of the rotated token; quarantine on his word.
4. **WED-48 overdue** — CypherKey Twilio token rotation (due 09-04).
5. **Five Secuura ruled cards that are his own acts:** `agent-github-identity` (ruled 08-26, NOT built — the agent still authors PRs as kksecura, so every PR needs Peter's or Stuart's approval), `ps-759-760-merge-owner` (two clicks on the PS repo), `ks229-disclosure-mailbox`, `ci-billing`, `dependabot-triage`.
6. **The reassignment exceptions** s138 will list (Peter's/Stuart's tickets whose newest comment names them) — Kam says whether they move too.
7. **On his panel with defaults:** KS-835, KS-841, the RD-333 pairs (NO deploy without his word), the demo-service stack-trace finding (now being filed as a ticket).

## Standing operational notes
See the 09-04 note's §9 list in `0_Brain/daily/2026-09-04.md`. `board_count.sh linear LINEAR_API_KEY '<GraphQL object, unquoted keys>'`. The inbox is listed WHOLE, never tailed. `send_brief.sh --kind brief` refuses a brief whose QUEUE names a ticket without a `- <ticket> state (…) | Linear/Jira ticket <id> | read <date>` provenance line, and refuses a SELF-CHECK whose stamp is not the clock's (`$(date +'%Y-%m-%d %H:%M')`) — both fired this seat, both right. The Bash tool REFUSES a command carrying a raw control character (the NUL escape typed literally) — write "backslash-u-0000" in words. `git grep -a` for every repo-wide sweep in the Secuura tree (a raw NUL in `ks431-oauth-app-update.test.ts` makes plain grep skip it silently). The Secuura seats run on Opus 5 by their launcher's fallback (Kam 2026-09-05). `2_Project_Files/fleet/state/` is gitignored. An untracked `.claude/settings.local (conflict_on_2026-09-04).json` sits in the tree (a sync conflict copy — reported, never removed). New tooling this seat: `decision_queue.sh show <id>`; `send_brief.sh --subject-file <path>`.
