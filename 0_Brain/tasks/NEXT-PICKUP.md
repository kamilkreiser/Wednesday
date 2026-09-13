---
date: 2026-09-13
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's — read her mail by SUBJECT only, never brief or answer for a Datasec project.
source: replaced WHOLESALE at 2026-09-13 15:1x AEST by the seat booted 14:08 (Kam's "rotate then keep pushing"), at ctx ~68%, ahead of its own self-rotation inside the 80-90 band (Kam 14:2x: rotation never blocks the work — agents run through it).
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — ⚡ **KAM'S RULES TODAY:** 09:1x "as many agents as necessary, no two on the same code"; 14:0x "rotate then keep pushing … at least 50% by Tuesday" (KS active ≤ 60 by Tue 2026-09-15; **125 at 14:1x**, −2 since: KS-1109, KS-1103 archived); **14:2x "dont let your context rotation get in the way of finishing tasks. You can always delegate to agents and get them to work while you rotate."** → self-rotate at the band WITH agents live (`learnings/2026-09-13_rotation-never-blocks-the-work-delegate-then-rotate.md`); the liveness checker `fleet/cockpit/rotate_liveness.sh` (shipped `7f773e62`) fires ~25 s after the respawn — **the successor's FIRST read after the digests: `fleet/cockpit/logs/rotate_wednesday.log` tail for `LIVENESS OK` / `LIVENESS FAIL`, and `ls fleet/cockpit/state/ROTATE_LOSS_*` (doctor warns too).**

> Narrative: `0_Brain/daily/2026-09-13.md` from the 14:11 boot block. **Measure before acting on any line here.** Subagent outputs of the 14:08 seat live in `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/e5222267-e2e4-4da3-810e-36fbfdd35651/scratchpad/` (wiped at reboot; briefs already sent are in `fleet/briefs_staged/`).

## 🟢 FLOOR (panes at 15:1x)
| pane | seat | state | next event owed |
|---|---|---|---|
| `%11` | **s200 MERGE seat** (`Secuura/Blockchain`) — plan CONFIRMED 04:50Z; **#963 → `99525196c` and #965 → `0dcd81d5d` merged + VERIFIED at source**; KS-1109, KS-1103 archived; KS-1117/1118/1119 filed | on ITEM 3 (#966), then #967, then #968 | each STATUS → verify at source (one parent == T, tree == prediction, T..M == files) → note · **ITEM 4 STATUS carries the v2 script hash + GitHub's #968 files count → Wednesday sends ONE further CONFIRMED naming the hash before #968 is PUT** (Q1 ruling) · CHECKPOINT 50% / HAND OVER NOW 70% mails (read its statusline at every wake) · wrap → score s200 |
| `%63` | **QA #932 tier 1** (KS-1062 @ `c72607d58`, merge-base `d4cf7e3cf`, gated ALONE) | launched 15:0x; session-side wait armed 10 min at a time (re-arm: `python3 fleet/cockpit/wait_subject.py "TIER 1 GATE #932 ROUND 1" 2026-09-13T04:55:00Z 120 120`, run_in_background) | verdict → completion vs 9 asks → on GO, #932 joins the merge queue (s200 successor or a merge seat) → then lane B's reworked #928 stacks on it |
| `%64` | **s202 LANE C** (`-C`): rebase #913 (KS-963 Urgent) as a NEW PR superseding it + Peter's fifth-caller cell → READY FOR QA (tier 1); #930 (KS-1052) only below ~55% | launched 15:07; plan confirmation owed (rung 5 poll running) | ANSWER (check: new branch/PR, no force push; the f3 branch's commits carried or not — by measurement; KS-1050 does NOT close with #930) → READY → tier-1 gate (template `fleet/qa-agent/launchers/launch_qa_secuura_ks1062_932.sh` + its generator `scratchpad/gate932/gen_launcher_932.py` — copy the generator to a tracked home) |
| `%65` | **s204 LANE E** (`-E`): KS-922/941/878/867/877 as three PRs (orchestrate · Testing/jobs · docker-build) | launched 15:1x; plan confirmation owed | ANSWER → three READYs → tier-2 gates |
| — | **s201 LANE B** (`-B`, NOT launched): #928 rework STACKED on #932's branch (loader half dropped; seed half → KS-962's ratified shape; the ks949 suite — a real Postgres without a stack is the plan-confirmation question) | brief drafting: `scratchpad/s201_laneB_brief.md` + loadbearing (subagent running at the handover) | re-read the table → patch develop (`0dcd81d5d` or later) → `self_check_view.sh` → `brief_and_launch.sh --to Secuura/Blockchain-B` |
| — | **s203 LANE D** (`-D`, NOT launched): ten `packages/shared/src/__tests__/` tickets (ks860 ×4, ks879 ×2, ks781-p3-3 ×3, entrypoint-corpus ×1), one PR per file | brief drafting: `scratchpad/s203_laneD_brief.md` | same send path, pane `-D` |
| `%1` | monitor | — | — |

**develop = `0dcd81d5d`** (#965) ← `99525196c` (#963) ← `721b333a6` (#962). **#969 (KS-1069 @ `fb23ca6aa`, stacked on #968) needs its tier-2 gate AFTER #968 merges** (template = the stack launcher `launch_qa_secuura_ks1071_1070_967_968.sh`; asks in the 12:5x note line) → **then score s199** (deferred: a round is scored at its last verdict). **#928 HELD** (lane B reworks it). **#913** superseded by s202's new PR (close #913 once it exists).

## 🟢 KAM'S RULINGS AND GRANTS IN FORCE
- Standing rule (09:1x) + the target (14:0x) + rotation-never-blocks (14:2x) — above. Overnight is working time (08-28). We approve and merge our own TESTED Secuura work (09-11 16:56 / 17:50). Kintsugi-first; demo waits for Peter's nod.
- **The week grants (deploy kintsugi+demo; production ban lifted; merge-for-the-week) END OF SUNDAY 13 SEP — TODAY.** From Monday: v1.3 + the TESTED grant only. `EXPIRING-GRANTS.md` rows to move under `## Expired` at the first Monday boot.
- **Cards OPEN on his panel (do not re-list to him):** `secuura-ks1114-verify-title-strategy` (rec remove-title) · `secuura-ks1116-presentation-credential-ownership-model` (rec bind-creator) · `secuura-965-f1-verify-hash-precedence-v1-vs-v2` (rec accept-split) · `wed-coordinator-rotation-killed-the-fleet-1604` (AMENDED 14:2x: default = self-rotate with agents live + the checker; the split-servers question still his) · one Datasec/HPSM card (Tuesday's). `reconcile_rulings.py` at every checkpoint; a tap on a `secuura-` card → `--apply` → deliver into the artefact.

## 🔵 QUEUE (in order)
1. s200's remaining merges (#966 → #967 → #968 with the v2 CONFIRMED step) → #969's gate → s199's score → s200's wrap + score.
2. Launch s201 (B) and s203 (D) from the drafts; answer the four plan confirmations; gates on every READY (tier per the seat's reading, ruled by Wednesday).
3. #932 verdict → merge (+ #928 rework merge after its gate) → KS-1062/950/962 close.
4. Post-merge lanes (after s200 finishes): KS-1110 (imports `readYaml`), R4 gateway health/status (KS-1101, KS-864), KS-730 (both `verification.ts` files); spares R1 frontend (KS-1104/1105/1106), R3 akto (KS-1108, KS-755), R5 kyc (KS-849, KS-848) — `0_Brain/reference/2026-09-12_secuura-lanes/` + `scratchpad/lanes_1420.md` (copy it to `0_Brain/reference/2026-09-13_secuura-lanes/` — owed).
5. KS active re-count at every checkpoint (`board_count.sh`, type `unstarted`+`started`) and the delta to 60 on Kam's panel once a day, not per merge.

## 🟡 OWED BY WEDNESDAY (shared tooling: claim with Tuesday first)
- **Tuesday's three measured traps in Wednesday's tools (her 04:27Z mail):** (1) `cockpit.sh rotate` polls only `wednesday-agent@` for the wrap and taps the pane to mail there — a Datasec seat wraps to `tuesday-agent@`, so rotate force-kills it at the 10-min timeout (route by the seat's coordinator; longer default for seats with lanes); (2) `cockpit.sh say <pane> --mail` EXITS 1 WITH NO OUTPUT when the pane has no `inbox_routing.conf` row — **met on this seat too with a pane ID (`%11`); the pane NAME works** → print a refusal naming the missing row; (3) `launchers.conf` pins DevMASTER paths (her Mac mini has no DevMASTER). Tell Tuesday the liveness checker shipped (she holds `--self` until she sees it fire).
- Copy `scratchpad/gate932/gen_launcher_932.py` (the launcher generator, re-implemented) to a tracked home under `fleet/qa-agent/`; copy `lanes_1420.md` to `0_Brain/reference/`.
- The brief template: the concurrent-seat DIFF rule; "a round-N brief names round N-1's report path"; the LEGITIMATE-SHAPES table for checkers (done in the qa-agent template 09-11; the builder template still owes it).
- `wake_watch.sh` fixes (QA-tag subjects inbound; never `stable_n=9999` with panes live — the runner re-arms itself after each wake, so the gap is only a wake-less stretch); `send_brief.sh` double-prefix; `inbox_digest.sh` ack; the 18 Secuura ruled-undelivered cards; the family-weight index.
- Teardown candidates (quarantine, never delete; Kam's): `worktrees/s190-ks1099`, `s191-ks1098`, `s192-ks1109`, `s193-ks1029`, `s194-merge`, `s196-merge`, `s197-ks1103`, `s198-ks1020`, `s199-ks1071` (+ `s200-merge` after its wrap).
- **At the WRAP:** rule 3b BOTH digests (learnings +1 today: the rotation grant; ledger +3 rows); rule 3c archive rows ≤ 2026-09-10.

## ⚠ TRAPS
- `/private/tmp` is wiped at reboot. A QA launcher run in the Bash tool runs headless — `cockpit.sh add` only. Resume a gate with `cockpit.sh say <PANE NAME> '<text>'`, never raw `send-keys`, never a pane ID.
- `card_id_gate.sh` reads any `secuura-<word>` token as a card claim — file names go in `fleet/card_id_gate.allow` with a dated reason (`secuura-brief-traps` added 15:0x).
- The provenance gate reads `a/b/c`, branch names and `pulls/N` as relative paths. The seat-scoped chat hook refuses chat-store reads without `view`; the no-cd hook refuses `cd` and `git -C $VAR` (literal paths; three refusals this seat).
- Compose no sentence in the same command whose output holds the fact. Linear's branchName can carry ANOTHER ticket's id (KS-754; KS-922/941 carry ks-868/ks-923). A stacked PR's GitHub files list keeps the ORIGINAL merge-base after the parent squashes (s200's (f) measurement — the v2 script exists for it).
- Builder seats cannot see their gauge: CHECKPOINT 50%, HAND OVER NOW 70%. Before a pane close: transcript last assistant row `end_turn`; ghost text at a wrapped prompt → close, never clear.
- Write and commit in ONE command (uncommitted non-derived files block `panel_sync` — twice this seat, minutes each). zsh: no `PIPESTATUS`; list variables do not split; `grep` is a shell FUNCTION → `/usr/bin/grep` with a control.
- The `[Datasec/ATTIO -> Wednesday] DAILY FOLLOW-UP DIGEST` lands ~07:00 — subject only. Peter merges his own PRs at night; his untested PS-831 branch is never a base.
- Tool paths: `brief_and_launch.sh`, `send_brief.sh`, `self_check_view.sh` in `2_Project_Files/fleet/`; `cockpit.sh`, `pane_close.sh`, `pane_prompt_check.sh`, `wait_subject.py`, `rotate_liveness.sh`, `wednesday_rotate.sh` in `fleet/cockpit/`; QA launchers in `fleet/qa-agent/launchers/` (newest: `launch_qa_secuura_ks1062_932.sh`).
