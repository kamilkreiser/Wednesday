---
date: 2026-09-13
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's — read her mail by SUBJECT only, never brief or answer for a Datasec project.
source: replaced WHOLESALE 20:30, floor + queue refreshed 20:53 at the 70% checkpoint by the seat booted 17:48 ( rotation inside the 80-90 band with agents live — Kam 14:2x: rotation never blocks the work).
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — ⚡ **KAM'S RULES TODAY:** 09:1x "as many agents as necessary, no two on the same code"; 14:0x "at least 50% by Tuesday" (KS active ≤ 60 by Tue 2026-09-15; **132** at 17:5x by `board_count.sh` — re-count at boot; it rises when lanes attach PRs and falls at merge+archive: 11 archived tonight); 14:2x "dont let your context rotation get in the way … delegate … while you rotate". **16:55: three cards RULED and DELIVERED** (KS-1114 `de54da40` · KS-1116 `01a8361c` · #965 F-1 → KS-1133). **Kam's 18:17 question answered 19:11+19:2x** (In Review ≠ the merge queue; census in `scratchpad/inreview_census/census.md` of the 17:48 seat — copy it to `0_Brain/reference/` at the next quiet moment, it is in `/private/tmp`). **Kam RULED 20:42:08:** the eight merged-but-In-Review tickets (KS-643/661/754/800/804/992/1024/1057) → **Done + archive** — routed to s211 ITEM 0b. **First reads after the digests:** `fleet/cockpit/logs/rotate_wednesday.log` tail (`LIVENESS OK`), `ls fleet/cockpit/state/ROTATE_LOSS_*`, commit the two launcher-regenerated digests BY LITERAL PATH.

> Narrative: `0_Brain/daily/2026-09-13.md` from the 17:58 boot block. **Measure before acting on any line here.** The 17:48 seat's scratchpad: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/0f8f9fa8-eada-40b6-ad2d-8c8120bb3b2f/scratchpad/` — verdicts `verdict978/980/981.txt`, rules `rule978.md`, gate sets `gate980/ gate981/ gate973r2/ gate977r2/`, briefs `s209/ s208/ s210/`, the census. (`/private/tmp` is wiped at REBOOT, not at rotation.)

## 🟢 THE SESSION LIMIT (18:11 → 19:10): the account's limit froze Wednesday, every subagent and s207 for an hour. Kam's 18:17 sat 54 min. If it fires again: receipt Kam first, resume seats by MAIL + verified tap, re-send subagent commissions (SendMessage to the dead agent id resumes it with its brief intact).

## 🟢 FLOOR (at 20:53)
| pane | seat | state | next event owed |
|---|---|---|---|
| `%87` | **s210 LANE D** — #980 fix DONE: new head **`103c235b4`** READY round 2 (10:50:34Z; one line `:235` → `app.listen(0, '127.0.0.1');`; merged-tree 813/813 on M15, guard 23/23, red-first 812/813; 4/4 tampers; PROTOCOL-CLEAN) | wrapping | wrap mail → close `%87` (detector first) → **score at the delta verdict** |
| — | **#980 ROUND 2 DELTA gate set** BUILDING (`scratchpad/gate980r2/`, head `103c235b4`) | subagent | install → controls_check → `--check` (BRANCH ON rc) → commit by name → `cockpit.sh add` → wait on the verdict MAIL → RULE → s210 score → ADDENDUM to s211 (ITEM L) |
| `%88` | **QA #977 tier-2 ROUND 2** (`aede93117`; launcher `launch_qa_secuura_ks877_977_r2.sh`; wait task `bn2ssuyd4` keyed on the verdict MAIL `[QA -> Wednesday] TIER 2 GATE #977 ROUND 2` — a successor re-arms its own) | running since 20:48 | verdict → RULE → **s208's score** → on GO: ADDENDUM to s211 (ITEM M) |
| — | **s211 MERGE SEAT brief** BUILDING (`scratchpad/s211/`): ITEM 0b = Kam's 20:42 ruling (the eight → Done + archive) · ITEM K = #973 @ `ca2a9109c` GO (`rule973.md`; close #928) · L/M by ADDENDUM | subagent | stage → SELF-CHECK restamp → `brief_and_launch.sh --to Secuura/Blockchain` (freshness gate: every id needs a state line) → plan confirmation → CONFIRM |
| `%1` | monitor | — | — |

**develop = M15 `1c38077ba`** (#981) ← M14 `6b62ae446` (#978) ← M13 `3370ef661` (#976) ← M12 `3fc158c39` (#974) ← M11 `a2257e502` (#975) ← M10 `e91eb5bda` — **all five verified by Wednesday via ls-remote + the commits API** (one parent, file set, tree). Archived tonight: KS-1126/878/867/876/891/894/895/885/886/828/900 (11). Filed: KS-1136 (Med) 1137 1140 **1141 (QUESTION — the #978 R2 scope ruling: whether ks727's "first-party runtime source" and crypto-agility's "under services/ or packages/" are INTENDED now that ks879 walks the whole tree — Wednesday rules on a builder's measurement; not urgent)** 1142 1143 (Med) 1144; s208's KS-1138 (C3 CI red on develop) + KS-1139 (the `((x++))` class residue). **Supersede-closes:** #928 only with #973 r2's GO.

## 🔵 SCORES this seat: s203 0.95 · s206 0.90 · s209 1.00. Owed at their last verdicts: s207 (#973 r2), s208 (#977 r2). QA gates 1.00 ×3 (#978, #980, #981) — all three found things the builders' tampers could not.

## 🟢 KAM'S RULINGS AND GRANTS IN FORCE
- Standing rule (09:1x) + the target (14:0x) + rotation-never-blocks (14:2x). Overnight is working time. We approve/merge our own TESTED Secuura work (09-11). Kintsugi-first; demo waits for Peter's nod.
- **The week grants (deploy kintsugi+demo; production ban lifted; merge-for-the-week) END OF SUNDAY 13 SEP — TONIGHT.** From Monday: v1.3 + the TESTED grant only. `EXPIRING-GRANTS.md` rows → `## Expired` at the first Monday boot. **No deploys tonight.**
- Cards: `secuura-inreview-eight-merged-tickets-target-state` **RULED 20:42:08 → done** (Kam's choice over the rec; reconciled; delivered by s211 ITEM 0b — mark `--delivered` at its STATUS) · `wed-coordinator-rotation-killed-the-fleet-1604` (split-servers question) · Datasec/HPSM ones (Tuesday's). `reconcile_rulings.py` at every checkpoint (0 to rule at 20:30). Kam → Wednesday: nothing since 18:17.

## 🔵 QUEUE (in order)
1. s211 brief → launch → plan confirmation → ITEM 0b (the eight) → ITEM K (#973 → M16, close #928). #980 delta gate → verdict → RULE → ADDENDUM L. #977 r2 verdict (`%88`) → RULE → s208 score → ADDENDUM M. s210 wrap → close → score at L's verdict.
2. s211 merge seat as soon as one GO exists (E-shape brief; one seat, one PUT at a time).
3. **Lanes from the census** (`census.md`): class B (11 need a gate: #809 #920 #923 #931 #937 #939 #942 never gated; #924 #925 #927 gated on older heads; #973 in flight) and class C (10 Peter fix rounds: KS-577 657 679 739 791 799 931 945 961 1043 — KS-791/#813 and KS-945/#879 have fixes built locally under the LEG-14 push hold) — partition by directory, as many lanes as the code allows, each with a brief + a gate. Class G (4) and the card's 8 are Kam's/Peter's.
4. KS active re-count at every checkpoint; the delta to 60 on Kam's panel once a day.

## 🟡 OWED BY WEDNESDAY (shared tooling: claim with Tuesday first — WED-OWNERSHIP.md)
- **CLAIMED 19:14: seat-name resolver unification** (`wednesday_rotate.sh` / `wake_watch.sh` / `arm_wake_watch.sh` disagree; a dead Tuesday seat cannot respawn — her 08:57Z mail; shape (b)+(a) + a per-seat scratch test of `--self` and `--dead`). Promised to her tonight with a sha + test output before she needs to rotate on it. **BUILT + STAGED at `59ec89ddf` (`fleet/cockpit/staged/resolver-20260913/`, 22/22 scratch test); NOT installed — the successor installs at boot BEFORE the launcher arms the watcher (stop watcher → copy `seat_resolve.sh` + the three → re-arm → `resolver_test.sh` again). Second half NOT built: `cockpit.sh` :90/:389 + `Launch_Cockpit.command:104` literal `wednesday` (hunk proposed in `DIFF.md`). Tuesday told 20:4x with the sha.**
- Tuesday's 07:40Z proposal: `statusline_publish.sh` skips the write when the published minute is unchanged (or panel_sync treats `usage_*.json` as derived).
- QA brief template: a `predicted-by` column on tamper tables (drafter / Wednesday-read) — five prediction slips in two briefs tonight; the gate-set install check greps §4 tokens at head (built into `controls_check.sh` per set — make it the template's).
- Pathguard: `cp SRC DST` judged by DST only (false positive on a read tonight). Subject-line rule: `STOP`/`HOLD`/`HAND OVER NOW`/`CHECKPOINT` appear in a subject ONLY as the instruction itself.
- The QA verdict record spans TWO report trees (`Testing Agent MAIN/projects/secuura/` and `projects/secuura-blockchain/`); only 11/119 dirs in tree 1 carry `mail-subject.txt` — a census over one tree is over the wrong frame.
- Teardown candidates (quarantine, never delete; Kam's): `worktrees/s19x-*`, `s200-merge`… `s209-merge`, `s206-laneD`, `s207-ks950-r2`, `s208-ks877-r2`.
- **#973 r2 RULE also names:** a Low for the preflight's missing auth-vitest leg (14 legs, 0 hits for services/auth — the KS-1046/1051 class); KS-962 stays OPEN until F-973-3's rolbypassrls precondition is verified on a deployed box.
- **At the WRAP:** rule 3b digests NOT owed unless a lesson FILE changed (none this seat so far — ledger rows only; verify with `git log -- 0_Brain/learnings/2026-*`); rule 3c archive `_ledger.md` rows ≤ 2026-09-10 (~60 rows) with conservation asserted; copy the census to `0_Brain/reference/2026-09-13_secuura-inreview-census/`.

## ⚠ TRAPS
- **BRANCH ON `--check`'s rc — three actions, never one chain.** A develop move re-pins ONLY the develop lines; the merge-base stays the PR's parent. The stacked-PR shape (#981) judged by BLOB, not file name.
- `decision_queue.sh add --json < file` (stdin; `_override_prior` in the JSON for a word-level prior-rulings match — state the measurement in the BLUF). The freshness gate refuses ANY ticket id in a brief without a state line — archived ids need `includeArchived:true` (a default Linear query returns 0 for them).
- A QA launcher run in the Bash tool runs headless — `cockpit.sh add` only. Resume a seat by MAIL + `cockpit.sh say <PANE NAME> … --mail`, never raw `send-keys`. TYPED-UNSENT text at a prompt: record, clear only if moot, never Enter; ghost text at a wrapped prompt → close the pane.
- Write and commit in ONE command; zsh: no `PIPESTATUS`, list vars do not split, `grep` is a shell FUNCTION → `/usr/bin/grep -i` with a control. The no-cd hook refuses `cd` and `git -C $VAR` (literal paths only); the pathguard refuses `cp` FROM another tree (use `cat >`).
- Suite timeouts at load ~20+: launch gates one at a time; a tier-1 Postgres gate waits for load < 16.
- The `[Datasec/ATTIO -> Wednesday] DAILY FOLLOW-UP DIGEST` lands ~07:00 — subject only. Kam's HPSM card rulings arrive in Tuesday's tab — hers.
- Tool paths: `brief_and_launch.sh`, `send_brief.sh`, `self_check_view.sh`, `board_count.sh` in `2_Project_Files/fleet/`; `cockpit.sh`, `pane_close.sh`, `pane_prompt_check.sh`, `wednesday_rotate.sh` in `fleet/cockpit/`; QA launchers in `fleet/qa-agent/launchers/` (newest: `…973_r2.sh`, `…981.sh`, `…980.sh`); `kam_rulings_today.sh`, `kam_msgs.sh`, `reconcile_rulings.py`, `chat_reply.sh`, `decision_queue.sh` in `2_Project_Files/tools/`.
