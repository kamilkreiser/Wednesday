---
date: 2026-10-05
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE 2026-10-05 22:5x by seat 9a78af86 (53% checkpoint). Replace wholesale again; never stack.
---

# NEXT PICKUP

## 🔴 FIRST ACTS (rotation handover 23:5x AEDT 2026-10-05, seat 9a78af86 at ~78%)
0. `kam_rulings_today.sh` + `reconcile_rulings.py`. Kam silent since 20:07 (a KS-1256 reading was posted to his panel 23:3x with a correction offer: Redis DOWN = 503, Redis up + unset = no restriction).
1. Read `inbox_digest.sh --inbound` WHOLE; bodies via `inbox_digest.sh full <inbox> '<id>'`.
2. **develop = d784b613c81e** (#1388 squash, verified at source). ABSENT from the shared store at 23:3x; seats bring it in by the STANDING_LINES objects-only route.
3. **E 5th (%45)**: #1385 (KS-938) tree **04fa3e0d1b48 CONFIRMED** by an independent verifier; merge-in + push RELEASED 12:5xZ. Expect its READY → **commission a gate kit for #1385 at its merge-in head M** (tier 1: MFA disable nulls the seed), then GO `GO (Seat E 5th): merge 1385 on gate<NN>`. Then E 5th's KS-1256 (ruling 7: thrown read → 503; Redis unavailable → 503 except deliberate no-Redis config, measured first; unset with Redis up → no restriction).
4. **B 64th (%46)**: plan ANSWERED 12:5xZ, PR C (KS-723 anchors-tx) building. Expect its READY → gate kit (tier 1). Also holds #1393's merge on gate65's GO.
5. **gate65 (pane `QA/Secuura-ks1278-1393`) LAUNCHED 12:48:43Z** on #1393 at 4a1620588819 over d784b613c81e. Rung 5 NOT yet checked. Kit doubt D1: revoking by UUID may now answer 400 (UPDATE matches external_id only) — likely NO GO material. On GO: `GO (Seat B 64th): merge 1393 on gate65` with the gate's key-anchored merge-in tree (predicted 6e5de2a1395b on d784b613c81e). On NO GO: a fix round for B lane.
6. **F 4th (%47)** launched 12:40:04Z: ITEM 0 owed. Rule Q-AKTO yes (npm ci in systemTest/akto, not under the lock), Q-1376 leave. Its merge-in tree needs an INDEPENDENT prediction before the push GO (drafter predicted 10c5716a4663 on d784b613c81e; copy tonight's predict_1385 verifier commission shape). Merge only on `GO (Seat F 4th): merge 1383 on gate61`.
7. **G lane**: gate64 GO on #1389 (report sha256 995ca420033e0c04; squash subject + five sentences the body must NOT carry in the verdict). **Seat G 2nd brief drafter was running at rotation** → `fleet/briefs_staged/2026-10-05_seatG2_merge_1389.md`. If absent/partial: re-commission (gate64 verdict saved in the previous seat's scratchpad will be gone — re-read the verdict mail from wednesday-agent@ by subject `GATE64 #1389`). Read WHOLE before `brief_and_launch.sh` (run BARE, not under `script`).
8. **Spark**: queue empty; HOLDs awaiting a raise seat: KS-998, KS-1136, KS-1164, KS-1305, KS-1313 (REVIEW.md in each run dir). Tunnel: check /health first.
9. Send-gate format for briefs: every PROVENANCE line `- Pn fact | instrument | read YYYY-MM-DD` on ONE line, absolute paths, a Linear line per QUEUE ticket. Pane ctx: `tmux resize-pane -t %NN -y 16` then `tmux select-pane -t %0`.

## SECUURA LANES
| lane | seat / pane | state | next |
|---|---|---|---|
| B | B 64th %46 | PR C building | READY → gate; #1393 merge on gate65 GO |
| D | none | idle | C6 image proof at next kintsugi deploy; N-1388-2 doc sentence |
| E | E 5th %45 | #1385 merge-in released | READY → gate → GO; KS-1256 |
| F | F 4th %47 | ITEM 0 | merge-in (independent tree check) → GO |
| G | none | #1389 gate64 GO | G 2nd (brief drafting) |
Scored this seat: E 4th 0.93 · B 63rd 0.95 · D 9th 0.95 · gate64 1.0. STANDING_LINES added tonight: worktree object store; inherited tools fail closed; scratch-clone origin trap; trap-4 forward half.

## OWED (added this seat)
- Gate-kit defect (D 9th's finding): `c4_docs_gate63.py predict` on an ABSENT develop returns None for every blob → a false M6 "re-gate" refusal. predict must refuse "develop unresolvable" by name; carry into every new kit.
## RULES LEARNED TONIGHT (in STANDING_LINES / the ledger)
- Doc merge-ins: the cheat sheet has NO readable ordering invariant. **The target tree from a gate's key-anchored prediction is the authority**, never a div-anchored M1.
- A push is judged by the push tool's `.rc` file + `ls-remote`. rc 141 = KS-1149: retry under the lock, no transport change. A first push uses the seat's first-push tool.
- `git fetch --dry-run` writes the shared store; signal harnesses run in the FOREGROUND.
- A conditional GO states its act and no-act branches as two separate lines. Before sending, read the BLUF's order against the numbered list's (w=2 tonight).
- Name a seat's tool or flag only from its brief or `--help` (w=2 tonight).
- Gate-kit drafters' `_scratch/` dirs are now gitignored (gate63 left 1.4 GB).

## OWED
- Kam's three 20:06-20:07 rulings → tickets via a board seat (DECISIONS-24, last section; the #1245/#1278 pairing was corrected 20:3x).
- DECISIONS-24 queue (17 items: 4 Spark briefs, 12 Claude lanes, 1 board pass). Spark queue EMPTY; Kam's target is 50/day.
- Stale "Actions is retired" premise in Secuura's project CLAUDE.md (CI live and red; KS-1148 is Kam's). Tell Kam in ONE line next time he is on the panel.
- Tooling: the idle leg cannot tell an API-error stall from a waiting seat (two today); cockpit `say` with a pane id is a silent no-op; cockpit launch should tell a seat its pane name; 1-row panes defeat ctx reads.
- 136 ruled-but-undelivered cards (board-pass backlog). Ornith paused to 06:00; Ollama DOWN.
- Gate kits gate61r2 / gate62 / gate63 are untracked in git: commit them WITHOUT `_scratch/` (now ignored). Check `git status` sizes first.

## WITH KAM
Nothing waiting on him. The October deploy grant (kintsugi + demo) and the week instruction (to Sun 11 Oct) are live.
