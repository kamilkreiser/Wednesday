---
date: 2026-09-13
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's — read her mail by SUBJECT only, never brief or answer for a Datasec project.
source: replaced WHOLESALE at 2026-09-13 12:5x AEST by the seat booted 08:39 (Kam-launched), at ctx ~82%, handing over to a KAM-LAUNCHED successor (no self-rotation while agents are live — card `wed-coordinator-rotation-killed-the-fleet-1604`, default).
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — ⚡ 13:1x. **UNPROCESSED at the handover: the #967+#968 STACK VERDICT landed 03:08:15Z — `GO WITH FINDINGS` per its subject; body NOT read by the 08:39 seat (at its ceiling). Read it whole first, completion vs the brief's asks, score s199 (with #969's gate still owed), close `%10` after `end_turn`.** FLOOR = four QA gates + one builder. **FIRST ACTS:** (1) commit the launcher's digests by literal path · (2) `kam_msgs.sh --brief` (his rulings first) · (3) **re-arm ONE verdict wait (#966)** (`python3 2_Project_Files/fleet/cockpit/wait_subject.py "<needle>" "<since ISO>" 120 120`, run_in_background, one per gate — needle: `TIER 1 GATE #966 ROUND 1`; since `2026-09-13T02:00:00Z`) — the watcher's mail leg cannot see a QA verdict · (4) do NOT run `wednesday_rotate.sh --self` while agents are live.

> Narrative: `0_Brain/daily/2026-09-13.md` from the 08:39 boot block (the 12:05 handover block + everything after). **Measure before acting on any line here.**

## 🟢 FLOOR (panes read 12:4x)
| pane | seat | state | next event owed |
|---|---|---|---|
| `%4` | ✅ **QA #963 — GO WITH FINDINGS 02:45:36Z (2 Polish); s192 0.90, s195 0.95, QA 1.00; CLOSED 12:5x.** **#963 GO to squash-merge** (QA-963-1 rides KS-1110; QA-963-2 → one Low ticket, BOM strip; O-1 noted on KS-1110) | — | the merge seat: a merge seat squashes #963 with the durable script (`5_Project_History/merge-protocol/merge_squash.sh` sha `9f9860ad…`), EXPECT_T/EXPECT_TREE; **T-move caution: #963's files are under `systemTest/performance/`, which #961 changed — if the gate's merged tree predates `21c74dd2a`, re-run that unit suite on the merged tree first** |
| `%8` | ✅ **QA #965 — GO WITH FINDINGS 02:52:01Z (3 Minor, 2 Info, 1 brief error, O-1 class note); s197 0.90, QA 1.00; CLOSED 12:5x.** **RULED: #965 GO to squash-merge at `d63b27ab3` as gated.** F-2 (the `{documentHash:A, hash:B}` pin cell) + F-3 (narrow the `:739-740` comment and test header `:15-17`) → ONE Low follow-up ticket, related KS-1103, filed by the merge seat (not a re-gate). **F-1 (v1 hash-LAST vs v2 hash-FIRST) is Kam's — goes on the Secuura contract card with KS-1114 + KS-1116.** **O-1 → its own ticket** (crossTenantLookup by-id fallback + `hashMatch=true`: dormant single-tenant, Major if multi-tenancy is enabled; READ ONLY; a live multi-tenant probe settles it) — filed by the merge seat with the gate's report path. F-5: whichever of #931/#965 merges second converts the mock. F-4(i): the brief template's caller list corrected (prelaunch spec hits `/api/documents/verify` + `/api/verify`). | — | the merge seat |
| `%9` | **QA #966** (KS-1020 item 1 @ `1f0d08841`, tier 1) | launched 12:40; ctx 13% | verdict → completion vs 8 asks → **score s198** → close → on GO: merge; KS-1116 to Kam as above |
| `%10` | **QA #967+#968 stack** (KS-1071 @ `51e74ea7a`, KS-1070 @ `1b7c03a22`, tier 2) | launched 12:44; ctx 6% | verdict (per-PR mergeability in order) → completion → **score s199** (after its wrap) → close → on GO: merge #967 then #968 (then the KS-1069 PR when its gate passes) |
| `%7` | ✅ **s199 WRAPPED 02:48:19Z, CLOSED 12:5x** — **KS-1069 READY as PR #969 @ `fb23ca6aa`** (parent `1b7c03a22` = #968's head; stacks on #968 → #967; body names only KS-1069; verified at source 12:5x). Handover `HANDOVER-s199-ks1071-ks1070-ks1069.md` + history on disk. | — | **a tier-2 gate on #969** (the three-PR stack head; template `launch_qa_secuura_ks1071_1070_967_968.sh`; asks: E1-E7 rows, strict height, the placeholder regex mirroring anchoring's, item 4's widened ks1057 cell; the JSONB round-trip NOT covered) → **score s199 after BOTH the stack verdict and #969's** |
| `%1` | monitor | — | — |

**develop = `721b333a6`** (#962) ← `21c74dd2a` (#961) ← `b1cb8466f` (#926). **PRs of ours: #963 GO + #965 GO (merges owed, one merge seat: #963 first (systemTest) then #965 (originate), EXPECT gates each, KS-754-style census, the durable script) · #966, #967+#968 under gates · #969 needs its gate.** **#928 HELD** (KS-962 reverted shape + Peter's review hold; rework = loader half + KS-962's ratified shape, then re-gate). **#913** needs rebase + re-gate.

## 🟢 KAM'S RULINGS AND GRANTS IN FORCE
- **STANDING RULE (2026-09-13 09:1x, terminal, verbatim in `learnings/2026-09-13_as-many-agents-as-possible-partitioned-by-code.md`):** as many agents as possible on every project, the only limit is collision on the code base. Partition by directory; one worktree per seat; the shared-inbox warning in every brief. Seats registered: `Secuura/Blockchain`, `-B`, `-C`, `-D`, `-E` (routing + launchers + the send gate's DQ_PREFIX).
- Keep the pace (2026-09-12 13:51/13:55) — stop at tickets cleared / KS active < 100 / allowance out. KS active read 121 at 08:4x (re-count before quoting).
- We approve and merge our own TESTED Secuura work (2026-09-11 16:56 / 17:50:39). Kintsugi deploys: v1.3 + kintsugi-first (2026-09-10 13:22). Demo waits for Peter's nod.
- **Week grants (deploy to kintsugi AND demo; production ban lifted; merge-for-the-week) END OF SUNDAY 13 SEP — today. Nothing queued relies on them; from Monday only v1.3 + the TESTED grant stand.**
- Card OPEN: `wed-coordinator-rotation-killed-the-fleet-1604` (rec split-servers; default: no self-rotation while agents live + build the check-only half). His 08:58 hypothesis (credits) is on the card; the measurement says the tmux session died as a unit.

## 🔵 QUEUE (in order)
1. The four verdicts → scores → merges (the merge seat: brief from the s196 pattern — `fleet/briefs_staged/2026-09-13_s196_finish-961-merge.md` + the two addenda; EXPECT_T/EXPECT_TREE + DRYRUN controls per PR; KS-754-style census around each PUT).
2. s199's KS-1069 READY → gate on the stack head → wrap → score.
3. **ONE card for Kam (a Secuura contract sitting), after #966's verdict:** KS-1114 (title strategy vs remove `title` from the spec) · KS-1116 (who owns a presentation/credential) · **#965 F-1 (v1 hash-LAST vs v2 hash-FIRST — one order, or the split accepted in writing)**. Build it from the three tickets + the #965 report; options + Wednesday's rec + a default each.
4. New lanes under the standing rule (re-sweep first — `0_Brain/reference/2026-09-12_secuura-lanes/secuura_lanes.md` reserve lanes; a classification list is a representation): KS-1110 (QA-960-2, after #963 merges — same package), KS-1076 (P1, may already be fixed by #896 — verify), the reserve lanes R1-R5.
5. #928 rework + #913 rebase (builder seats). Runtime gates on #872/#896/#728/#808 on kintsugi (tier 1; QA login keys in the Secuura `.env`).

## 🟡 OWED BY WEDNESDAY (shared tooling: claim with Tuesday first)
- **`panel_sync` has no re-arming** (launcher 0 lines; doctor blind) — it died 16:26 yesterday and was restarted by hand 08:45. Doctor FAIL check + launcher arming.
- The rotation card's check-only half (post-respawn liveness check + auto-rebuild in `wednesday_rotate.sh`; the watcher treats "no fleet session" as a rebuild wake).
- QA launchers exec `claude` directly: launch ONLY via `cockpit.sh add`; guard candidate: refuse when stdin is not a TTY. **Resume a QA gate with `cockpit.sh say <pane> '<short text>'` (pane read-back), never raw `send-keys`** (12:01 → 12:44 loss).
- Brief template: the concurrent-seat DIFF rule (a DIFF whose only moved refs are another live seat's branch/tracking ref/worktree HEAD is expected; anything else STOPs) + "a round-N brief names round N-1's report path" + the LEGITIMATE-SHAPES table for checkers.
- `wake_watch.sh` fixes (QA-tag subjects inbound; never `stable_n=9999` with panes live; frozen/idle legs vs a seat waiting on its own background shell).
- `wait_subject.py` doctor line; `send_brief.sh` double-prefix; `inbox_digest.sh` ack; `reconcile_rulings.py` in the watcher; the launcher committing its digests; 18 Secuura ruled-undelivered cards; the family-weight index.
- **Teardown candidates (quarantine, never delete; Kam's):** `worktrees/s194-merge`, `s196-merge`, `s190-ks1099`, `s191-ks1098`, `s192-ks1109`, `s193-ks1029`, `s197-ks1103`, `s198-ks1020`.
- **At the WRAP:** rule 3b BOTH digests (ledger +9 rows today, learning +1); rule 3c archive rows ≤ 2026-09-10.

## ⚠ TRAPS
- `/private/tmp` is wiped at reboot — nothing a successor needs lives only in a scratchpad.
- A QA launcher run in the Bash tool runs headless (pane only). A raw `send-keys` tap may not submit.
- The provenance gate reads `a/b/c` (e.g. `spf/dkim/dmarc`), branch names and `pulls/N` as relative paths.
- The seat-scoped chat hook refuses chat-store reads without `view`; the no-cd hook refuses `git -C $VAR` (literal paths) and any write verb outside WEDNESDAY.
- A `python3 -c "…"` in double quotes executes backticks; a `&`-detached wait has no wake path (use run_in_background); compose no sentence in the same command whose output holds the fact (two topology slips today).
- Linear's branchName can carry ANOTHER ticket's id (KS-754); a ticket's OWN PR walks it to In Progress (leave it); collateral walks are restored with CAS.
- The `[Datasec/ATTIO -> Wednesday] DAILY FOLLOW-UP DIGEST` lands ~07:00 — subject only.
- Peter's untested PS-831 branch — never a base. Peter merges his own PRs at night.
- Builder seats cannot see their gauge: CHECKPOINT 50%, HAND OVER NOW 70%.
- Before a pane close, read the transcript's last assistant row for `end_turn`; ghost text at a wrapped prompt → close, never clear.
- Write and commit in ONE command. zsh: no `PIPESTATUS`; list variables do not split; `grep` is a shell FUNCTION — `/usr/bin/grep` with a same-file control.
- Tool paths: `brief_and_launch.sh`, `send_brief.sh`, `self_check_view.sh` in `2_Project_Files/fleet/`; `cockpit.sh`, `pane_close.sh`, `pane_prompt_check.sh`, `wait_subject.py` in `fleet/cockpit/`; QA launchers in `fleet/qa-agent/launchers/` (newest: `launch_qa_secuura_ks1071_1070_967_968.sh`).
