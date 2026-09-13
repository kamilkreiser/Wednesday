---
date: 2026-09-13
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's — read her mail by SUBJECT only, never brief or answer for a Datasec project.
source: replaced WHOLESALE 16:2x by the seat booted 15:57 at its 50% checkpoint (Kam 14:2x: rotation never blocks the work — delegate, then rotate with agents live).
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — ⚡ **KAM'S RULES TODAY:** 09:1x "as many agents as necessary, no two on the same code"; 14:0x "rotate then keep pushing … at least 50% by Tuesday" (KS active ≤ 60 by Tue 2026-09-15; **122 at 16:0x** by `board_count.sh`, type unstarted+started); 14:2x "dont let your context rotation get in the way of finishing tasks … delegate to agents and get them to work while you rotate" → self-rotate at the band WITH agents live (`learnings/2026-09-13_rotation-never-blocks-the-work-delegate-then-rotate.md`); **the liveness checker fired for real at 15:58:12 (`LIVENESS OK 6/6`)** — the successor's FIRST read after the digests: `fleet/cockpit/logs/rotate_wednesday.log` tail + `ls fleet/cockpit/state/ROTATE_LOSS_*`. Then commit the two launcher-regenerated digests BY LITERAL PATH (the sync SKIPs on them every minute until you do).

> Narrative: `0_Brain/daily/2026-09-13.md` from the 15:57 boot block. **Measure before acting on any line here.** Subagent outputs of the 15:57 seat live in `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a443e8f5-4f70-46d7-b9f3-451ac0da033f/scratchpad/` (gate970/ gate972/ gate971/ gate973/ gate975/ gate974/ s205_merge_brief.md — each `BUILD_REPORT.md` present = built; absent = the subagent died with the seat → rebuild from the gate969 exemplar at `…/e5222267-…/scratchpad/gate969/BUILD_REPORT.md`, which is the recipe). The READY/verdict mails are saved beside them as `s20N_readyNNN.txt`, `verdict969.txt`.

## 🟢 FLOOR (panes at 16:2x)
| pane | seat | state | next event owed |
|---|---|---|---|
| `%67` | **s203 LANE D** (`packages/shared/src/__tests__/`) — CONFIRMED 16:02 (PR-0 first under KS-1126; Q1 yes; Q2 (i); T6 not built; tier 2 ×5) | **#975 @ `8da20edbd` READY** (PR-0, KS-1126); on PR-1 (ks860, KS-876/891/894/895) | READYs → tier-2 gates; its 50% CHECKPOINT / 70% HAND OVER NOW mails (read the gauge at every wake) |
| `%65` | **s204 LANE E** (`scripts/`) — CONFIRMED 05:2xZ | **#971 @ `c229aa256` READY** (PR-1, KS-922+941) · **#974 @ `8da602309` READY** (PR-2, KS-878+867); on PR-3 (KS-877 + KS-922's comment items) | READY → tier-2 gate; CHECKPOINT/HAND OVER NOW mails |
| — | s202 lane C WRAPPED 05:59Z, `%64` closed — **#970 @ `ae274f7cb` (KS-963, supersedes #913)** and **#972 @ `b3ce8c9e7` (KS-1052, supersedes #930)** READY, both tier 1; score deferred to their verdicts | — | gates → GO → merge seat closes #913 / #930 |
| — | s201 lane B WRAPPED 06:11Z, `%66` closed — **#973 @ `dfed981d0` (KS-950/962, supersedes #928)** READY, tier 1; KS-1127 + KS-1128 filed; score deferred | — | gate → GO → merge seat closes #928 (HELD since 09-12) |
| — | QA #969 tier 2 **GO WITH FINDINGS @ `fb23ca6aa`** (`%68` closed) — RULED, see the 16:24 note line: v2 merge, body-only fix, ONE Medium (F1 root + O1 + JSONB) + ONE Low (F2 twins + P2/P3) | — | **s205 MERGE SEAT** — brief drafting in a subagent → re-read load-bearing table → `brief_and_launch.sh` on pane `Secuura/Blockchain` → plan confirmation → merge |
| `%1` | monitor | — | — |

**develop = M6 `0f69129b3`** (#932) — relayed from the 14:08 seat's 15:3x source read; the #969 gate read it unmoved at 16:17. Re-read before any merge brief.

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
- **Cards OPEN on his panel (do not re-list):** `secuura-ks1114-verify-title-strategy` · `secuura-ks1116-presentation-credential-ownership-model` · `secuura-965-f1-verify-hash-precedence-v1-vs-v2` · `wed-coordinator-rotation-killed-the-fleet-1604` (the split-servers question) · one Datasec/HPSM (Tuesday's). `reconcile_rulings.py` at every checkpoint (55 taps / 0 to rule at 16:1x); a tap on a `secuura-` card → `--apply` → deliver into the artefact. Kam → Wednesday: nothing since 08:58 on the panel; 3 `view=tuesday` withheld.

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
- `/private/tmp` is wiped at reboot (not at rotation). A QA launcher run in the Bash tool runs headless — `cockpit.sh add` only. Resume a gate with `cockpit.sh say <PANE NAME> '<text>'`, never raw `send-keys`, never a pane ID.
- `--mail "<bare subject>"` on the shared inbox matches the OLDEST same-subject mail — cite the ROUTED subject `[Wednesday -> Secuura/Blockchain-X] …`. `card_id_gate.sh` reads `secuura-<word>` as a card (allow-list by exact name). The provenance gate reads `a/b/c`, branch names, `pulls/N` as relative paths. The seat-scoped chat hook refuses chat-store reads without `view`; the no-cd hook refuses `cd` and `git -C $VAR`.
- Per-message AgentMail fetches need the `message_id` URL-encoded (`urllib.parse.quote(id, safe='')`) — a bare `<…>` id 400s.
- Write and commit in ONE command; a `.md` staged into a tracked dir (`briefs_staged/`) blocks `panel_sync` until committed. zsh: no `PIPESTATUS`; list variables do not split; `grep` is a shell FUNCTION → `/usr/bin/grep -i` with a control. Python heredocs: a row string containing `"` breaks a `python3 - <<'EOF'` script — write rows to a file first.
- Builder seats cannot see their gauge: CHECKPOINT 50%, HAND OVER NOW 70% (s201's came from the watcher wake). Before a pane close: transcript last assistant row `end_turn` (select by BIRTH time, `stat -f %SB`); ghost text at a wrapped prompt → close, never clear.
- The `[Datasec/ATTIO -> Wednesday] DAILY FOLLOW-UP DIGEST` lands ~07:00 — subject only.
- Tool paths: `brief_and_launch.sh`, `send_brief.sh`, `self_check_view.sh`, `board_count.sh` in `2_Project_Files/fleet/`; `cockpit.sh`, `pane_close.sh`, `pane_prompt_check.sh`, `wait_subject.py`, `rotate_liveness.sh`, `wednesday_rotate.sh` in `fleet/cockpit/`; QA launchers in `fleet/qa-agent/launchers/`; `kam_rulings_today.sh`, `kam_msgs.sh`, `reconcile_rulings.py`, `chat_reply.sh`, `decision_queue.sh` in `2_Project_Files/tools/`.
