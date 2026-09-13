---
date: 2026-09-13
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's — read her mail by SUBJECT only, never brief or answer for a Datasec project.
source: replaced WHOLESALE 15:1x and PATCHED IN PLACE at 15:4x by the seat booted 14:08, at ctx ~79%, at its self-rotation inside the 80-90 band (Kam 14:2x: agents run through it) (Kam 14:2x: rotation never blocks the work — agents run through it).
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — ⚡ **KAM'S RULES TODAY:** 09:1x "as many agents as necessary, no two on the same code"; 14:0x "rotate then keep pushing … at least 50% by Tuesday" (KS active ≤ 60 by Tue 2026-09-15; **125 at 14:1x**; six archived since: KS-1109, KS-1103, KS-1020, KS-1071, KS-1070, KS-1062 — re-count at boot); **14:2x "dont let your context rotation get in the way of finishing tasks. You can always delegate to agents and get them to work while you rotate."** → self-rotate at the band WITH agents live (`learnings/2026-09-13_rotation-never-blocks-the-work-delegate-then-rotate.md`); the liveness checker `fleet/cockpit/rotate_liveness.sh` (shipped `7f773e62`) fires ~25 s after the respawn — **the successor's FIRST read after the digests: `fleet/cockpit/logs/rotate_wednesday.log` tail for `LIVENESS OK` / `LIVENESS FAIL`, and `ls fleet/cockpit/state/ROTATE_LOSS_*` (doctor warns too).**

> Narrative: `0_Brain/daily/2026-09-13.md` from the 14:11 boot block. **Measure before acting on any line here.** Subagent outputs of the 14:08 seat live in `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/e5222267-e2e4-4da3-810e-36fbfdd35651/scratchpad/` (wiped at reboot; briefs already sent are in `fleet/briefs_staged/`).

## 🟢 FLOOR (panes at 15:4x — the rotating seat's last read)
| pane | seat | state | next event owed |
|---|---|---|---|
| — | ✅ **s200 MERGE seat WRAPPED 05:40:42Z, SCORED 1.00, `%11` CLOSED** — six PRs merged + verified (#963 `99525196c` · #965 `0dcd81d5d` · #966 `5c3c4ec98` · #967 `163ca2c74` · #968 `6696c6681` on v2 · #932 `0f69129b3`), six tickets archived, KS-1117–KS-1125 filed; handover `HANDOVER-s200-merge-963-968-932.md` + history `:24` on disk | — | nothing; `worktrees/s200-merge` = teardown candidate (Kam's) |
| `%64` | **s202 LANE C** — **READY: PR #970 @ `ae274f7cb` (KS-963, supersedes #913; verified by Wednesday at source: open, 2 files +376 −10, 0 `@`)**; now on ITEM 2 (#930 → a superseding PR, KS-1052; conflict hunk `userRepo.ts:845-856` keep-both as ruled) | ctx 42% at 15:4x | **the #970 TIER-1 gate set is drafting** (`scratchpad/gate970/` — install: re-read pins, `--check`, `cockpit.sh add "QA/Secuura-ks963-970" …`, arm `wait_subject.py "TIER 1 GATE #970 ROUND 1" <since> 120 120`) · s202's 50% CHECKPOINT / 70% HAND OVER NOW mails · its ITEM 2 READY → tier-1 gate · then close #913 (and #930 when superseded) — Wednesday's, via a merge/admin seat, never by a lane seat |
| `%65` | **s204 LANE E** — plan CONFIRMED 05:2xZ (Q1 b, Q2 widen, tier 2 ×3); three PRs in order | ctx 37% | READYs → tier-2 gates (template: the tracked generator + the #932 set as the tier-1 shape / the stack set as tier 2) |
| `%66` | **s201 LANE B** — plan CONFIRMED 05:4xZ (the UPDATE…FROM VALUES shape with the guard; real PG 15 on a socket; exit 0 + SKIP; the loader half in the suite; two Low tickets to file: the runner's skip tally, the platform seed's debug catch) | ctx 38% | READY → tier-1 gate (its PR carries the #968 shape vs M6 → **`merge_squash_v2.sh` sha `d1ba1fc5…` for the merge**) |
| `%67` | **s203 LANE D** — launched 15:26; plan confirmation OWED (three traps to rule: the ks860 self-scan, KS-885's regression clause, KS-828's T6 target; KS-924's pin shape) | ctx 32% | ANSWER → four READYs → tier-2 gates |
| `%68` | **QA #969 (KS-1069 @ `fb23ca6aa`, tier 2, develop pin `0f69129b3`)** | LAUNCHED 15:5x; **verdict wait NOT armed — arm it first:** `python3 fleet/cockpit/wait_subject.py "TIER 2 GATE #969 ROUND 1" 2026-09-13T05:55:00Z 120 120` (run_in_background, re-arm every 10 min) | verdict → completion vs the brief → **score s199** (deferred since 12:5x) → merge on GO by a merge seat (true delta vs develop = 3 files incl. the ks1057 test; GitHub lists 5 → v2 `GEQ_PR`) |
| `%1` | monitor | — | — |

**develop = M6 `0f69129b3`** (#932) ← `6696c6681` (#968) ← `163ca2c74` (#967) ← `5c3c4ec98` (#966) ← `0dcd81d5d` (#965) ← `99525196c` (#963) ← `721b333a6`. **#928 HELD** (s201 supersedes it). **#913 superseded by #970** — close #913 with a comment naming #970 (Wednesday's; a merge seat's hands).

## 🟢 KAM'S RULINGS AND GRANTS IN FORCE
- Standing rule (09:1x) + the target (14:0x) + rotation-never-blocks (14:2x) — above. Overnight is working time (08-28). We approve and merge our own TESTED Secuura work (09-11 16:56 / 17:50). Kintsugi-first; demo waits for Peter's nod.
- **The week grants (deploy kintsugi+demo; production ban lifted; merge-for-the-week) END OF SUNDAY 13 SEP — TODAY.** From Monday: v1.3 + the TESTED grant only. `EXPIRING-GRANTS.md` rows to move under `## Expired` at the first Monday boot.
- **Cards OPEN on his panel (do not re-list to him):** `secuura-ks1114-verify-title-strategy` (rec remove-title) · `secuura-ks1116-presentation-credential-ownership-model` (rec bind-creator) · `secuura-965-f1-verify-hash-precedence-v1-vs-v2` (rec accept-split) · `wed-coordinator-rotation-killed-the-fleet-1604` (AMENDED 14:2x: default = self-rotate with agents live + the checker; the split-servers question still his) · one Datasec/HPSM card (Tuesday's). `reconcile_rulings.py` at every checkpoint; a tap on a `secuura-` card → `--apply` → deliver into the artefact.

## 🔵 QUEUE (in order)
1. Arm the #969 verdict wait; install + launch the #970 (tier 1) gate set from the scratchpad draft; answer s203's plan confirmation; CHECKPOINT/HAND OVER NOW mails per seat (read every gauge at every wake).
2. Gates on every READY (s201 ×1, s202 ITEM 2, s203 ×4, s204 ×3); on GO, ONE merge seat (s205, the s200 brief as template; v2 for stacked shapes) merges in order and closes #913/#928.
3. #969's verdict → score s199; s202/s201/s203/s204 scored at their last verdicts.
4. Post-merge lanes (after s200 finishes): KS-1110 (imports `readYaml`), R4 gateway health/status (KS-1101, KS-864), KS-730 (both `verification.ts` files); spares R1 frontend (KS-1104/1105/1106), R3 akto (KS-1108, KS-755), R5 kyc (KS-849, KS-848) — `0_Brain/reference/2026-09-12_secuura-lanes/` + `scratchpad/lanes_1420.md` (copy it to `0_Brain/reference/2026-09-13_secuura-lanes/` — owed).
5. KS active re-count at every checkpoint (`board_count.sh`, type `unstarted`+`started`) and the delta to 60 on Kam's panel once a day, not per merge.

## 🟡 OWED BY WEDNESDAY (shared tooling: claim with Tuesday first)
- **Tell Tuesday the liveness checker shipped `7f773e62`** (she holds `--self` until she sees it fire — this seat's 15:4x rotation is the first production run: quote the `LIVENESS` log line to her).
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
