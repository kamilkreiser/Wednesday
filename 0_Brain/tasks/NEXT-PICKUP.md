---
date: 2026-09-13
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's — read her mail by SUBJECT only, never brief or answer for a Datasec project.
source: replaced WHOLESALE 16:2x and REFRESHED 17:0x (65%) and 17:2x (70% checkpoint) by the seat booted 15:57 (Kam 14:2x: rotation never blocks the work — delegate, then rotate with agents live).
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — ⚡ **KAM'S RULES TODAY:** 09:1x "as many agents as necessary, no two on the same code"; 14:0x "rotate then keep pushing … at least 50% by Tuesday" (KS active ≤ 60 by Tue 2026-09-15; **122 at 16:0x** by `board_count.sh`, type unstarted+started); 14:2x "dont let your context rotation get in the way of finishing tasks … delegate to agents and get them to work while you rotate" → self-rotate at the band WITH agents live (`learnings/2026-09-13_rotation-never-blocks-the-work-delegate-then-rotate.md`); **the liveness checker fired for real at 15:58:12 (`LIVENESS OK 6/6`)** — the successor's FIRST read after the digests: `fleet/cockpit/logs/rotate_wednesday.log` tail + `ls fleet/cockpit/state/ROTATE_LOSS_*`. Then commit the two launcher-regenerated digests BY LITERAL PATH (the sync SKIPs on them every minute until you do).

> Narrative: `0_Brain/daily/2026-09-13.md` from the 15:57 boot block. **Measure before acting on any line here.** Subagent outputs of the 15:57 seat live in `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a443e8f5-4f70-46d7-b9f3-451ac0da033f/scratchpad/` (gate970/ gate972/ gate971/ gate973/ gate975/ gate974/ s205_merge_brief.md — each `BUILD_REPORT.md` present = built; absent = the subagent died with the seat → rebuild from the gate969 exemplar at `…/e5222267-…/scratchpad/gate969/BUILD_REPORT.md`, which is the recipe). The READY/verdict mails are saved beside them as `s20N_readyNNN.txt`, `verdict969.txt`.

## 🟢 FLOOR (panes at 17:2x — the 70% checkpoint; the daily note's 17:28 block is the narrative)
| pane | seat | state | next event owed |
|---|---|---|---|
| `%72` | **s205 MERGE SEAT** — #969 → M7 `506cd3a33`, #970 → M8 `fa55e58c9` (both VERIFIED at source); #913 closed; ITEM B delivered (KS-1114 `de54da40`, KS-1116 `01a8361c`, KS-1133) | queue **C #971 @ `c229aa256` → D #972 @ `b3ce8c9e7` (close #930; F-3 HIGH + F-5 MEDIUM tickets) → E #975 @ `8da20edbd` (one KS-953 comment)** — ADDENDUMs sent 07:04Z / 07:1xZ / 07:2xZ | each STATUS → verify M at source (`ls-remote` + `git log -1 --format=%P` + `diff --name-only`) → next ADDENDUM |
| `%79` | **s206 LANE D successor** (PR-3 KS-924/901; PR-4 KS-828/900) | plan confirmation OWED (proxy.ts `{ routes, guarded }` its named question; PR-4's base: after #975 merges, cut from develop) | ANSWER → READYs → tier-2 gates |
| `%75` `%76` `%78` | QA #974 t2 · #976 t2 · #977 t2 | waits armed | verdict → completion → RULE → ADDENDUM; score s204 at the last of #974/#977; s203 at the last of #976/#978 |
| — | **#973 NO GO round 1 of 2** (auth's ks949 test must move with the ticket; the guard's regression cell) — s201 wrapped → **s207 LANE B ROUND 2 brief drafting** (`scratchpad/s207_laneB_r2_brief.md`) | launch on `Secuura/Blockchain-B` when the draft lands (patch develop at send) | plan confirmation → READY → tier-1 gate ROUND 2 (the cap's last round) → GO → ADDENDUM (close #928) |
| — | #978 (KS-885/886) gate set BUILDING (`scratchpad/gate978/`) | — | install → `--check` (BRANCH ON THE RC) → commit by name → `cockpit.sh add` → wait |
| `%1` | monitor | — | — |

**develop = M8 `fa55e58c9`** (#970; ← M7 `506cd3a33` #969 ← M6 `0f69129b3`). Every running gate's launcher is pinned to an older develop by design; their briefs' mid-pass rule covers it.

## 🔵 GATE PIPELINE (all tier per Wednesday; verdict subject `[QA -> Wednesday] TIER N GATE #PR ROUND 1 (KS-…) <head7> -- …`)
| PR | head | tier | build (scratchpad dir) | install → launch → wait |
|---|---|---|---|---|
| #970 KS-963 | `ae274f7cb` | 1 | `gate970/` | re-read pins at source · `bash launchers/launch_qa_secuura_ks963_970.sh --check` · copy brief+prompt to `fleet/qa-agent/briefs/` + launcher to `…/launchers/` + commit BY NAME in one command · `cockpit.sh add "QA/Secuura-ks963-970" …` (as the launcher's usage says; NEVER run a launcher in the Bash tool — headless) · `wait_subject.py "TIER 1 GATE #970 ROUND 1" <since> 120 120` in background |
| #972 KS-1052 | `b3ce8c9e7` | 1 | `gate972/` | same shape |
| #971 KS-922+941 | `c229aa256` | 2 | `gate971/` | same shape |
| #973 KS-950+962 | `dfed981d0` | 1 | `gate973/` | same shape (the gate must not aim at Kam's live Homebrew PG on 5432) |
| #975 KS-1126 | `8da20edbd` | 2 | `gate975/` | same shape |
| #974 KS-878+867 | `8da602309` | 2 | `gate974/` | same shape |
Verdict → completion vs the brief → RULE → score the seat at its LAST verdict → ADDENDUM to s205 (PR, head, v1/v2, follow-ups, supersede-close).

## 🟢 KAM'S RULINGS AND GRANTS IN FORCE
- Standing rule (09:1x) + the target (14:0x) + rotation-never-blocks (14:2x). Overnight is working time (08-28). We approve and merge our own TESTED Secuura work (09-11 16:56 / 17:50). Kintsugi-first; demo waits for Peter's nod.
- **The week grants (deploy kintsugi+demo; production ban; merge-for-the-week) END OF SUNDAY 13 SEP — TODAY.** From Monday: v1.3 + the TESTED grant only. `EXPIRING-GRANTS.md` rows → `## Expired` at the first Monday boot. No deploys from any seat tonight.
- **Kam RULED three Secuura cards at 16:55** (reconciled `--apply`): KS-1114 → **implement-title** (AGAINST the rec — a product change, a builder-lane item, tier 1); KS-1116 → bind-creator; #965 F-1 → accept-split. **All three UNDELIVERED until s205's ITEM B comment ids arrive → `decision_queue.sh --delivered`.** Cards still OPEN: `wed-coordinator-rotation-killed-the-fleet-1604` (the split-servers question) · one Datasec/HPSM (Tuesday's). `reconcile_rulings.py` at every checkpoint (55 taps / 0 to rule at 16:1x); a tap on a `secuura-` card → `--apply` → deliver into the artefact. Kam → Wednesday: nothing since 08:58 on the panel; 3 `view=tuesday` withheld.

## 🔵 QUEUE (in order)
1. Install + launch each gate set as its BUILD_REPORT lands (pins re-read at source; `--check` rc 0; commit by name); arm its verdict wait.
2. s205 merge brief: re-read the load-bearing table, `self_check_view.sh`, `brief_and_launch.sh` → plan confirmation → CONFIRMED → #969 merged via v2 → follow-ups → KS-1069 archived → ADDENDUMs as verdicts land.
3. Verdicts → completion → rulings → scores (s202 at #970+#972; s201 at #973; s203/s204 at their last).
4. Post-merge lanes when a lane seat wraps: `0_Brain/reference/2026-09-13_secuura-lanes/lanes_1420.md` (KS-1110, R4 gateway health KS-1101/KS-864, KS-730, spares R1/R3/R5).
5. KS active re-count at every checkpoint; the delta to 60 on Kam's panel once a day.

## 🟡 OWED BY WEDNESDAY (shared tooling: claim with Tuesday first)
- Tuesday's three traps (her 04:27Z mail): `cockpit.sh rotate` wrap-poll hardcodes `wednesday-agent@`; `cockpit.sh say --mail` exits 1 silently with a pane ID (use the pane NAME); `launchers.conf` pins DevMASTER paths. Told her 16:08 (liveness + the containment gate).
- Brief template: the concurrent-seat DIFF rule; "a round-N brief names round N-1's report path"; the builder template's LEGITIMATE-SHAPES table. `wake_watch.sh` (QA-tag subjects inbound; never `stable_n=9999` with panes live); `send_brief.sh` double-prefix; `inbox_digest.sh` ack; the 18 Secuura ruled-undelivered cards; the family-weight index; a QA launcher that refuses a non-TTY stdin.
- Teardown candidates (quarantine, never delete; Kam's): `worktrees/s19x-*`, `s200-merge`, `s201-ks950-rework`, `s202-ks963`, `s202-ks1052`.
- **At the WRAP:** rule 3b BOTH digests only if `learnings/` changed (none this seat so far); rule 3c archive `_ledger.md` rows ≤ 2026-09-10 (the 09-10 rows are ~60 and past three days).

## ⚠ TRAPS
- **BRANCH ON `--check`'s rc — never `echo rc; commit; add` in one chain** (17:00: a refused check launched anyway; the launcher's own guard caught it). A develop move re-pins ONLY `DEVELOP_SHA` + the develop lines; the merge-base stays the PR's parent.
- `/private/tmp` is wiped at reboot (not at rotation). A QA launcher run in the Bash tool runs headless — `cockpit.sh add` only. Resume a gate with `cockpit.sh say <PANE NAME> '<text>'`, never raw `send-keys`, never a pane ID.
- `--mail "<bare subject>"` on the shared inbox matches the OLDEST same-subject mail — cite the ROUTED subject `[Wednesday -> Secuura/Blockchain-X] …`. `card_id_gate.sh` reads `secuura-<word>` as a card (allow-list by exact name). The provenance gate reads `a/b/c`, branch names, `pulls/N` as relative paths. The seat-scoped chat hook refuses chat-store reads without `view`; the no-cd hook refuses `cd` and `git -C $VAR`.
- Per-message AgentMail fetches need the `message_id` URL-encoded (`urllib.parse.quote(id, safe='')`) — a bare `<…>` id 400s.
- Write and commit in ONE command; a `.md` staged into a tracked dir (`briefs_staged/`) blocks `panel_sync` until committed. zsh: no `PIPESTATUS`; list variables do not split; `grep` is a shell FUNCTION → `/usr/bin/grep -i` with a control. Python heredocs: a row string containing `"` breaks a `python3 - <<'EOF'` script — write rows to a file first.
- Builder seats cannot see their gauge: CHECKPOINT 50%, HAND OVER NOW 70% (s201's came from the watcher wake). Before a pane close: transcript last assistant row `end_turn` (select by BIRTH time, `stat -f %SB`); ghost text at a wrapped prompt → close, never clear.
- The `[Datasec/ATTIO -> Wednesday] DAILY FOLLOW-UP DIGEST` lands ~07:00 — subject only.
- Tool paths: `brief_and_launch.sh`, `send_brief.sh`, `self_check_view.sh`, `board_count.sh` in `2_Project_Files/fleet/`; `cockpit.sh`, `pane_close.sh`, `pane_prompt_check.sh`, `wait_subject.py`, `rotate_liveness.sh`, `wednesday_rotate.sh` in `fleet/cockpit/`; QA launchers in `fleet/qa-agent/launchers/`; `kam_rulings_today.sh`, `kam_msgs.sh`, `reconcile_rulings.py`, `chat_reply.sh`, `decision_queue.sh` in `2_Project_Files/tools/`.
