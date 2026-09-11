---
date: 2026-09-11
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's — read her mail by SUBJECT only, never brief or answer for a Datasec project.
source: replaced WHOLESALE at 17:1x AEST by the seat booted 15:10, at its 80% rotation boundary.
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — 2026-09-11 17:1x (seat booted 15:10, ROTATING at 80%). **TIER-1 GATE ON PR #954 (KS-597 option B) LIVE in `%18`.** s180 wrapped, pane closed. **KAM 16:56: we approve and merge our own TESTED work.** KAM's last word to Wednesday: 16:58 (all receipted).

> Narrative: `0_Brain/daily/2026-09-11.md` (15:16–17:1x entries). **Measure before acting on any line here.**

## 🔴 HOLD — SECUURA PREFLIGHT LEG 14 (unchanged)
Until #953 is on develop, no seat runs the pre-push hook or preflight leg 14, on any tree containing `ec2d8c4ca`, from any push whose hook receives `GIT_DIR` (a linked worktree, or `git --git-dir=… --work-tree=… push`). Pushes from the MAIN checkout do not export `GIT_DIR` (the tier-2 push-protocol gate, measured in scratch). Every Secuura brief carries it.

## 🟢 FLOOR
| pane | seat | state | next event Wednesday owes |
|---|---|---|---|
| `%18` | **QA tier-1 gate, PR #954 @ `355d82c8b`** | launched 17:09:49 via `cockpit.sh add "QA/Secuura-ks597-954"`. Launcher `2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks597_954_tier1.sh`: real `--check` rc 0; red-proof 12 cells, FAILS=0. Brief `…/briefs/2026-09-11_secuura-954-ks597-tier1.md`. Verified at rung 5 17:10 | verdict mail `[QA -> Wednesday] TIER 1 GATE #954 KS-597 355d82c8b ROUND 1` → re-read PR #954's head (still `355d82c8b`?) → completion check against the brief's 7 asks → **score s180** → `pane_close.sh %18` |
| `%1` | monitor | — | — |

develop = `2d864ae9220c57ddcd8dc77af1b80fbd8001d530` (`ls-remote` 17:0x). **Left running FOR the gate:** the local stack rebuilt from `355d82c8b` (22/22) · disposable DB `ks597b-s180-pg` on 127.0.0.1:6599 · the labelled live-cell org `4084f75e-…`. **The Secuura main checkout sits on the PR branch; nobody switches it while the gate runs.**

## 🔵 KS-597 CHAIN — card DELIVERED 17:04 (PR #954 + KS-597 comment `86531841`)
s180's work, verified at source: PR #954 open, base develop, head == origin branch, 9 files +580 −29, Test Evidence in the body, KS-597 In Progress with the comment naming #954. **After a GO / GO WITH FINDINGS (Minor/Polish ticketed):**
1. Wednesday's GO = the approval (Kam 16:56:00 / 16:56:44 / 16:58:04).
2. Squash merge with the head re-read (`CONTRIBUTING.md:107`) — s180 is closed, so the merge-lane seat does it.
3. Kintsugi deploy: KS-535 wallet hold; compose project name trap; rebuild from develop at the merge.
4. **Demo = UAT, which waits for Peter's formal pass.**
5. **Stuart draft** `!CODING/Secuura/Blockchain/5_Project_History/2026-09-11_ks597/DRAFT-reply-to-stuart-ks597.md` — **read it WHOLE**, then take it to Kam with the PR link; it is his to send.

**NO GO →** fix round, round 1 of 2.

## 🟢 KAM 16:56 GRANT — `learnings/2026-09-11_secuura-we-approve-and-merge-our-own-tested-work.md` (+ an open-ended EXPIRING-GRANTS row)
Wednesday's readings, stated to him and not corrected: tested = QA gate at head + Test Evidence + our own suites (**he confirmed this at 16:58**) · kintsugi gets merged work · demo = UAT, waits for Peter's nod (narrower than the week's demo grant) · raise-to-1 stays unapplied (develop required approvals measured at **0**).

## 🔴 NEXT COMMISSION — a Secuura MERGE-LANE seat
Launch it once the #954 verdict is processed. It is a single Secuura seat; a parallel one would need its own cockpit name and routing entry — OWED item 5.
- **Item 0:** amend the project `CLAUDE.md` merge flow, lines 234-237, citing Kam verbatim. s180's handover carries the text.
- **Item 1:** census the open PRs via the API only — 54 at 16:5x: 53 on base develop, 39 by kksecura.
  - **TESTED** — gate verdict at the CURRENT head, Test Evidence present, base not already contained, no unresolved CHANGES_REQUESTED, `mergeable_state` not dirty.
  - **UNTESTED / NEEDS-BUILDER** — everything else.
- **Then:** Wednesday samples the TESTED rows at source and GOs them. The seat squash-merges one at a time via the API — head pinned, develop re-read after each, merge SHA commented on the ticket.
- **Order:** **#953 first** (tier-2 GO WITH FINDINGS @ `8987b8a0e`, findings in KS-1089; its merge lifts the LEG-14 HOLD); #954 after its gate.
- **No deploy in that round**, and the seat never touches the main checkout while a gate uses it.

## 🟠 PUSH-PROTOCOL FIX ROUND OWED — round 2 of 2; not urgent
Verdict at `!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-11-push-protocol-d2a53096-tier2-r1/report.md`; s179 scored 0.90.
**W-1 RULED** (today's note, 15:2x entry):
- `push -u` config delta confined to `branch.<pushed>.remote/.merge` → CLEAN;
- a refused push that altered nothing in the shared repository → a distinct NOT-LANDED verdict with its own exit;
- optional expected-sha;
- QA-1: read origin first, re-read locals after it and require equality;
- QA-4 and QA-5 ride along.

**Brief it with template §2a's LEGITIMATE-SHAPES table.**

## 🔴 WITH KAM (already on his panel — do not re-list in every message)
1. The Stuart reply — after the #954 gate, with the PR link.
2. Drafts for Peter (#933 / #952 / #896) are still his to send if he wants them. #953 no longer needs Peter's review under the 16:56 grant.
3. His vault skill `Notes (MASTER)/skills/Current/extranet.md` contradicts his 09-05 tickets-only rule.
4. The agent GitHub identity invite · deleting `feature/y` / `feature/w`.
5. Tuesday's Mac mini Full Disk Access toggle (Tuesday's to follow up).

## 🟡 OWED BY WEDNESDAY
1. Send gate: refuse a Secuura brief containing `extranet` outside a HOLDS / "not a channel" context.
2. pretooluse hook:
   - refuse `PIPESTATUS`;
   - flag `grep -c`/`-q` on a multi-word phrase without `-i`;
   - flag a bare `grep` with `$(` inside `$(…)`;
   - flag `echo =…`.
3. Inbox reads filter on SUBJECT routing tags, never on From.
4. `cockpit.sh`: `die` on the `--mail` routing path prints nothing. `pane_close.sh` usage says name-or-id but refuses a name.
5. `cockpit.sh add` should refuse a name with no routing entry — blocks parallel Secuura seats.
6. `send_brief.sh` double-prefixes a subject that already carries a routing tag.
7. `reconcile_rulings.py` in the watcher's checkpoint legs (shared `wake_watch.sh` — claim with Tuesday first).
8. Family-weight index (Kam's `measure-first` #1).
9. 18 Secuura ruled-undelivered cards (`decision_queue.sh list ruled --undelivered secuura-`; KS-597's is now delivered).
10. Kam's `vault-add-a-stages-another-clients-files` grant, at a quiet floor.
11. panel_sync `Cannot rebase onto multiple branches` (Tuesday's tooling).

## 🟠 NAS
Tonight's 03:30 leg is the first real run of the FIXED deletion counter (`a0d70ca8`). Read its per-root summary; `UNKNOWN` means normalisation failed, not zero.

## ⚠ TRAPS
- **Write and commit in ONE command.** Stage multi-file work in the scratchpad, then copy it in and commit together. The launcher's regenerated boot digests block `panel_sync` until committed.
- **zsh:**
  - no `PIPESTATUS`;
  - a list variable does not word-split;
  - `echo ======` is `=`-expansion and aborts the command;
  - `VAR=x cmd1 | cmd2` hands VAR to cmd1 only;
  - `sleep N; cmd` is blocked by the harness.
- **The Bash tool's `grep` is a shell-snapshot FUNCTION:** use `/usr/bin/grep` plus a same-file control.
- **`ps` shows a `$(…)` subshell with its parent's argv:** count loops by ppid 1 and start time.
- **The send gate's scope list** (`send_brief.sh:351`): `reversible · board config · low-risk · blast radius · contained change · local change`.
- **A mail to an agent can cross the agent's own mail** — twice today (4 s, then 10 s). Read the agent's next mail before re-sending anything.
- **A ruled card's `delivered` mark** is a record of what a seat wrote, never a fact about the world.
