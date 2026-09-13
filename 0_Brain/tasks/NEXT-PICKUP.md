---
date: 2026-09-13
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's — read her mail by SUBJECT only, never brief or answer for a Datasec project.
source: replaced WHOLESALE 17:4x by the seat booted 15:57 at ctx 78%, ahead of its rotation inside the 80-90 band (Kam 14:2x: rotation never blocks the work — agents run through it).
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — ⚡ **KAM'S RULES TODAY:** 09:1x "as many agents as necessary, no two on the same code"; 14:0x "at least 50% by Tuesday" (KS active ≤ 60 by Tue 2026-09-15; 122 at 16:0x by `board_count.sh` — re-count at boot; s205's read 129–132 = lane tickets walking on PR attach, absorbed at merge); 14:2x "dont let your context rotation get in the way … delegate … while you rotate". **16:55: three cards RULED and DELIVERED** (KS-1114 implement-title — AGAINST the rec, a product change for a builder lane, tier 1; KS-1116 bind-creator; #965 F-1 accept-split → KS-1133). **First reads after the digests:** `fleet/cockpit/logs/rotate_wednesday.log` tail (`LIVENESS OK`), `ls fleet/cockpit/state/ROTATE_LOSS_*`, then commit the two launcher-regenerated digests BY LITERAL PATH.

> Narrative: `0_Brain/daily/2026-09-13.md` from the 15:57 boot block (the 17:28 handover block is the summary). **Measure before acting on any line here.** Subagent outputs of the 15:57 seat: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a443e8f5-4f70-46d7-b9f3-451ac0da033f/scratchpad/` — `gate980/` (BUILD_REPORT.md present = built; absent = the subagent died with the seat → rebuild from `gate978/` as the exemplar, its disjointness-checked develop guard), `s208_laneE_r2_brief.md` (+ `s208_loadbearing.md`; absent = re-commission from the s204 brief + `verdict977.txt`). Verdicts saved as `verdictNNN.txt`; READYs as `s20N_readyNNN.txt`.

## 🟢 FLOOR (at 17:4x)
| pane | seat | state | next event owed |
|---|---|---|---|
| `%72` | **s205 MERGE SEAT** — M7 `506cd3a33` (#969) · M8 `fa55e58c9` (#970) · M9 `50b729d69` (#971) all VERIFIED at source; #913 closed; KS-1069/963/941 archived; KS-1129–1135 filed; CHECKPOINT 50% sent 17:5x | **ITEM D #972 on v3** (`merge_squash_v3.sh` sha `460c4e78…` CONFIRMED by hash 17:4x — `GEQ_SHARED` = `userRepo.ts`; close #930; F-3 HIGH + F-5 MEDIUM tickets) → E #975 → F #974 → G #976, each only if it fits under 70% | its STATUS → verify M at source (`ls-remote`, `git log -1 --format=%P`, `diff --name-only`) → at 70% HAND OVER NOW → successor merge seat s209 from its handover (the three scripts by path + hash: v1 plain · v2 stacked · v3 shared-path) |
| `%79` | **s206 LANE D** — CONFIRMED 17:3x; **#980 @ `9c620f890` READY** (PR-3, KS-924/901; plain PR → v1) | on PR-4 (ks781: KS-828/900; base = #975's head if still open at its cut → v2, else develop → v1) | READY → tier-2 gate; CHECKPOINT/HAND OVER NOW mails |
| `%80` | **s207 LANE B ROUND 2** — launched 17:52; the #973 fix (auth's ks949 test moves with the ticket + the guard's regression cell, NEW commit on #973's branch from a `--detach` worktree) | plan confirmation OWED | ANSWER → READY → **tier-1 gate ROUND 2 of 2** (the cap's last round; a NO GO ships nothing, tickets the residue) → GO → ADDENDUM to the merge seat (close #928) |
| `%81` | QA #978 t2 (KS-885/886 @ `13b767a7f`; wait detached `gate978/wait978.out`) | running | verdict → completion → RULE → ADDENDUM; **s203's score at this verdict** (its last) |
| — | **#977 GO WITH FINDINGS + F1 MAJOR** (the deliverable suite RED on CI: `((RUNNING++))` under bash ≥ 4.1 `set -e`) — **NOT merged; ROUND 2** → **s208 LANE E ROUND 2** brief drafting (`scratchpad/s208_laneE_r2_brief.md`) | launch on `Secuura/Blockchain-E` when the draft lands (patch develop at send; **BRANCH ON `--check`/brief_and_launch rc**) | plan confirmation → READY → tier-2 gate ROUND 2 → GO → ADDENDUM |
| — | **#980** gate set BUILDING (`scratchpad/gate980/`) | install → `--check` (branch on rc) → commit by name → `cockpit.sh add` → wait detached | verdict → RULE → ADDENDUM; s206's score at its last |
| `%1` | monitor | — | — |

**develop = M9 `50b729d69`** (#971; ← M8 `fa55e58c9` #970 ← M7 `506cd3a33` #969 ← M6 `0f69129b3`) at 17:4x — s205's ITEM D will move it. **Supersede-closes:** #913 ✓ · #930 with #972 (s205 D) · #928 only with #973's ROUND-2 GO.

## 🔵 VERDICTS PROCESSED THIS SEAT (all COMPLETE vs their briefs; QA 1.00 ×10)
#969 GO WF (F1 the E7 premise — KS-1129/1130) · #970 GO WF (KS-1131/1132) · #971 GO WF (KS-1134/1135) · #972 GO WF (F-3 HIGH MFA-disable retains secret; F-5 MEDIUM oauth unscoped; live-039 leg owed) · #975 GO WF (one KS-953 comment) · #974 GO WF (R-2+R-3 Medium; F-2+F-4 Low) · #976 GO WF (body counts only) · **#973 NO GO r1** (auth test + guard cell → s207) · **#977 GO WF + F1 Major** (→ s208) · seat scores: s199 0.90 · s202 0.90 · s201 0.80 · s204 0.80; s203 at #978; s206/s207/s208 at their lasts.

## 🟢 KAM'S RULINGS AND GRANTS IN FORCE
- Standing rule (09:1x) + the target (14:0x) + rotation-never-blocks (14:2x). Overnight is working time (08-28). We approve and merge our own TESTED Secuura work (09-11 16:56 / 17:50). Kintsugi-first; demo waits for Peter's nod.
- **The week grants (deploy kintsugi+demo; production ban; merge-for-the-week) END OF SUNDAY 13 SEP — TONIGHT.** From Monday: v1.3 + the TESTED grant only. `EXPIRING-GRANTS.md` rows → `## Expired` at the first Monday boot. No deploys tonight.
- Cards OPEN: `wed-coordinator-rotation-killed-the-fleet-1604` (the split-servers question) · one Datasec/HPSM (Tuesday's). `reconcile_rulings.py` at every checkpoint. Kam → Wednesday: nothing since 16:55.

## 🔵 QUEUE (in order)
1. Verdict #978 → RULE → ADDENDUM; score s203. Install + launch #980 when built. Launch s208 when drafted. Answer s207's plan confirmation.
2. s205's STATUS mails (D → E → F → G) → verify each M at source; at its HAND OVER NOW → s209 merge seat from its handover.
3. Round-2 gates for #973 (tier 1) and #977 (tier 2) at their READYs — the cap's last rounds.
4. Post-merge lanes: `0_Brain/reference/2026-09-13_secuura-lanes/lanes_1420.md` (KS-1110, R4 gateway health KS-1101/KS-864, KS-730, spares R1/R3/R5) + **KS-1114 implement-title (Kam's ruling, a product change, tier 1)** + KS-1116 bind-creator + KS-1129 (Medium, the raw-BIGINT root) as builder lanes — machine load the limit (s203 saw suite timeouts at load ~20).
5. KS active re-count at every checkpoint; the delta to 60 on Kam's panel once a day (the merges + archives today: KS-1109/1103/1020/1071/1070/1062/1069/963/941 = 9 archived; 20+ follow-ups filed).

## 🟡 OWED BY WEDNESDAY (shared tooling: claim with Tuesday first)
- **CARD CANDIDATE for Kam (credential grant): a read-scoped GitHub + Linear token exported into the QA launcher's ENVIRONMENT** (never a `.env` path) — asked by three gates (#969 PAT 403s; #974 item 4; #976 item 3); until then gates read via the machine's global gh (kksecura) read-only.
- The QA-gate brief template's §4 positive-control line must be re-derived per subject (the #975 carried-control ledger row); the gate-set install check greps each control token at the head SHA before `--check` (candidate for `gen_launcher_from_template.py`).
- Tuesday's three traps (her 04:27Z mail): `cockpit.sh rotate` wrap-poll hardcodes `wednesday-agent@`; `cockpit.sh say --mail` exits 1 silently with a pane ID; `launchers.conf` pins DevMASTER paths. `wake_watch.sh` (QA-tag subjects inbound); `send_brief.sh` double-prefix; `inbox_digest.sh` ack; the 18 Secuura ruled-undelivered cards; the family-weight index; a QA launcher that refuses a non-TTY stdin.
- Teardown candidates (quarantine, never delete; Kam's): `worktrees/s19x-*`, `s200-merge`, `s201-ks950-rework`, `s202-ks963`, `s202-ks1052`, `s203-laneD`, `s204-pr1/2/3`, `s205-merge`.
- **At the WRAP:** rule 3b digests NOT owed (no lesson FILE changed this seat — ledger rows only; verify with `git log -- 0_Brain/learnings/2026-*` before deciding); rule 3c archive `_ledger.md` rows ≤ 2026-09-10 (~60 rows) with conservation asserted.

## ⚠ TRAPS
- **BRANCH ON `--check`'s rc — never `echo rc; commit; add` in one chain** (17:00: a refused check launched anyway; the launcher's own guard caught it). A develop move re-pins ONLY `DEVELOP_SHA` + the develop lines; the merge-base stays the PR's parent (the #978/#980 launchers check disjointness instead).
- `decision_queue.sh --delivered ID ARTEFACT` (ID first). Per-message AgentMail ids need URL-encoding. A `"` inside a python heredoc row string breaks it — write rows to a file. Two gates launched in one minute share a birth-time window — discriminate transcripts by token weight. `pane_close.sh`'s listener count rises transiently under running gates. A detached `wait_subject.py` has no notification path — the pane-idle wake is the signal; read `gateNNN/waitNNN.out`.
- `/private/tmp` is wiped at reboot (not at rotation). A QA launcher run in the Bash tool runs headless — `cockpit.sh add` only. Resume a gate with `cockpit.sh say <PANE NAME>`, never raw `send-keys`, never a pane ID. `--mail "<bare subject>"` on the shared inbox matches the OLDEST same-subject mail — cite the ROUTED subject.
- Write and commit in ONE command; a `.md` in a tracked dir blocks `panel_sync` until committed. zsh: no `PIPESTATUS`; list variables do not split; `grep` is a shell FUNCTION → `/usr/bin/grep -i` with a control. The seat-scoped chat hook refuses chat-store reads without `view`; the no-cd hook refuses `cd` and `git -C $VAR`.
- Builder seats cannot see their gauge: CHECKPOINT 50%, HAND OVER NOW 70% (the watcher wakes name the pane). Before a pane close: transcript last assistant row `end_turn` (select by BIRTH time, `stat -f %SB`); ghost text at a wrapped prompt → close, never clear.
- The `[Datasec/ATTIO -> Wednesday] DAILY FOLLOW-UP DIGEST` lands ~07:00 — subject only.
- Tool paths: `brief_and_launch.sh`, `send_brief.sh`, `self_check_view.sh`, `board_count.sh` in `2_Project_Files/fleet/`; `cockpit.sh`, `pane_close.sh`, `pane_prompt_check.sh`, `wait_subject.py`, `rotate_liveness.sh`, `wednesday_rotate.sh` in `fleet/cockpit/`; QA launchers in `fleet/qa-agent/launchers/` (newest: `launch_qa_secuura_ks885_886_978.sh` — the disjointness-checked template); `kam_rulings_today.sh`, `kam_msgs.sh`, `reconcile_rulings.py`, `chat_reply.sh`, `decision_queue.sh` in `2_Project_Files/tools/`.
