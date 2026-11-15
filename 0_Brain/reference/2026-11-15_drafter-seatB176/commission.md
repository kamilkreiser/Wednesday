# Commission: DRAFTER for Seat B 176th (Secuura/Blockchain merge seat, lane -B), 2026-11-15 14:0x AEDT

Commissioned by Wednesday (the 11:0x seat). Read-only drafter: write ONLY the brief path below and notes.md in THIS folder (a clone inside this folder is allowed). Nothing merged, pushed, closed, posted, mailed or written to Linear or GitHub. Never write inside any `!CODING` checkout (read verbs only there). GitHub reads read-only with GH_CONFIG_DIR="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config" (confirm kksecura first); repo Secuura/Distributed_Secuura. No `cd` (a hook refuses it); zsh has no PIPESTATUS; never delete (a hook refuses rm; quarantine instead); bound every listing with `| head -N`. Linear comments: `first:50`, sort client-side, positive control (never `last:N`). Scratch git trees go in a folder whose name contains `_work` (gitignored).

## Produce
1. `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-15_seatB176_merge.md`: under 60 KB; carry B 175th's brief by REFERENCE where unchanged. The heading must read exactly `## RULED BY KAM, NOT YET IN AN ARTEFACT`. PROVENANCE lines in the form `- <fact> | <absolute source path / URL / ticket / command> | read YYYY-MM-DD` (relative paths are REFUSED by the send gate unless the owner is named). Every ticket the brief queues gets its own provenance line with its state and newest comment time. End with `SELF-CHECK: re-read end-to-end for contradictions | YYYY-MM-DD HH:MM` (machine clock, after your re-read).
2. `notes.md` here, ending with a section headed 'UNMEASURED'.

## Copy-and-change
- Template commission: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB175/commission.md` (WHOLE).
- Template brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-13_seatB175_merge.md` (its STAMP rulings CARRY) and Wednesday's mails to B 175th: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-13_B175_*.md` (answer_plan, go_2095, addendum_2228, addendum2_2090, go_2090).
- B 175th's record: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-13_seatB-175th/HANDOVER.md` (FINAL BLOCK 'FOR SEAT B 176th' first and whole; B 175th wrapped 2026-11-13 03:27Z). Its queue said "PR 2228 FIRST": **that is SUPERSEDED by Kam's ruling below.**

## Kam's rulings since B 175th (verbatim, live board / terminal, 2026-11-15)
- 13:48:44 card `secuura-ks1699-verify-audience-1113` = **c** "Leave verify open to any signed-in caller" (option detail: "The guard is reverted before 2225 deploys; KS-1699 is closed as intended behaviour.").
- Terminal ~14:0x, after Wednesday recommended closing PR 2228 rather than merging and reverting it: **"yes, close 2228 and launch the merge seat"**.
- 13:48:18 card `wed-morning-plan-1115` = a "Carry on as planned".

## Queue (Wednesday's ruling; re-pin every head by ls-remote and drop any that moved)
develop = 48883ba5976b76a5e28e4de69618853ba5d29a20 (PR 2090's squash; Wednesday ls-remote 2026-11-15 13:1x; re-read it). Nothing merged since 2026-11-13 03:24Z.
- **ROW 0 (no merge): CLOSE PR 2228 UNMERGED** (KS-1699, Seat R 118th's verify guard, head 4383051cafcf). Steps for the seat: a PR comment quoting Kam's card c and "closed unmerged on Kam's 2026-11-15 ruling; verify stays open to any signed-in caller", then `gh pr close 2228` (no branch delete); read the PR state back. Then a KS-1699 ticket comment (BLUF, no at-sign, `--dry` then `--real`, read back, 0 mention nodes) and the state move that means "closed as intended behaviour" on THIS board: MEASURE the Secuura team's workflow states and name the exact state (e.g. Canceled vs Done) in notes.md and the brief; the brief tells the seat which. PR 2228 is also attached to KS-1695 by branch name: a comment there only if the close changes what KS-1695 shows (measure; do not move KS-1695). R 118th's worktree `worktrees/s-r118-ks1699` is LEFT in place (Wednesday rules on it later).
- ROW 1 onward: PR 2098 (whole auth suite), 2089 (real run REQUIRED), 2079 (tier 1), 2220, 2221, 2222, 2223 (tier 2), 2224 (tier 1, last) — gate lines and squash forms from the B 175th brief and its STAMP; recompute every tree on develop 48883ba5976b.
- NOT in the queue: PR 2225 (held; its deploy question G348-2225-1 is still Wednesday's, and card c now also governs it), 2099, 2073, 2131, 2135, 2136, 2075, 2052, 887.

## Must-checks for notes.md
- Floor (cockpit.sh status): %0 Wednesday, %1 fleet-monitor, %2 Seat AA 6th (Secuura/Blockchain-AA, Opus, diagnosing a demo-pk anchoring failure; its paths `Blockchain/Dev/services/anchoring/**`). Confirm no queued row intersects `services/anchoring`.
- Open PRs touching each row's paths (GitHub pulls API file lists); the push queue (`ls /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/.push-queue | head`).
- Matcher figure for 176 derived by you (method stated); 176th takes `th`.
- The ordinal check: `^## .*Seat B 176th` expecting 0 in the project history.md, control `^## .*Seat B 175th` expecting 1.
- The board-seat filing list carried from B 175th's wrap (its 'FOR THE BOARD SEAT' block).
- The Spark is GONE (returned to HP 2026-11-15): no Spark filler, no Spark line anywhere in the brief.
- Model for the seat: claude-sonnet-5-5 (`/Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/models_latest.json` levels.sonnet.model_id; routing row C5 of `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/model-routing.md`).

Model: Sonnet. Return a 10-line summary.
