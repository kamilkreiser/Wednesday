---
date: 2026-09-13
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's — read her mail by SUBJECT only, never brief or answer for a Datasec project.
source: replaced WHOLESALE at 2026-09-13 09:0x AEST by the seat booted 08:39 (Kam launched it; the Mac booted 05:28). Boot ctx 37%; written at ctx ~58%.
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — ⚡ 09:0x (seat 08:39). FLOOR = `%2` QA tier-2 gate on #962 (KS-1029) @ `ac6f4fa91` · `%3` s196 finishing #961's merge (plan confirmation owed) · `%1` monitor.
**FIRST ACTS for a successor:** (1) **do NOT run `wednesday_rotate.sh --self` until the 16:04 cause below is established** · (2) re-arm the #962 verdict wait (the watcher's mail leg cannot see QA verdicts; the helper lives in the seat scratchpad — re-create it if gone: poll `wednesday-agent@` for a subject needle, exit on hit) · (3) answer s196's plan confirmation · (4) install + launch the #963 gate and send the s197 brief once their drafts are re-read (QUEUE 3-4).

> Narrative: `0_Brain/daily/2026-09-13.md` from the 08:39 boot block. **Measure before acting on any line here.**

## 🔴 WHAT HAPPENED (measured 08:4x)
- **16:04:29 2026-09-12:** `wednesday_rotate.sh --self` respawned `%0` (`fleet/cockpit/logs/rotate_wednesday.log:304-305`). **s194, s195 and the #962 gate stopped in the same minute** (transcripts last written 16:04); the watcher armed 16:05:04 with `agents=0`; **no successor Wednesday booted until Kam launched one at 08:39.** Cause: **UNMEASURED** — a read-only diagnosis was commissioned at 08:5x (report: seat scratchpad `rotation_1604_diagnosis.md`; copy anything durable into `0_Brain/reference/` before relying on it).
- **`panel_sync` died 16:26:14** (cause unmeasured) and nothing re-armed it; **restarted detached 08:45** (pid 9350, ppid 1, tty `??`).
- **The Mac booted 05:28** → every `/private/tmp` scratchpad was wiped, **including s186's gated merge script** every Secuura merge brief cited.
- Nothing half-done on develop: `b1cb8466f` = #926 (s194, verified by it, re-read by Wednesday). #961 NOT merged; s194 had filed KS-1111 and posted verdict comments (KS-1098 `7e62ed7c`, PR `5644067216`).

## 🟢 FLOOR
| pane | seat | state | next event owed |
|---|---|---|---|
| `%2` | **QA/Secuura-ks1029-962** — tier-2 round 1 on #962 @ `ac6f4fa91` (relaunched 09:00:04 via `cockpit.sh add`; report dir suffix `-relaunch-20260913b`) | running | verdict mail `[QA -> Wednesday] TIER 2 GATE #962 ROUND 1 (KS-1029) ac6f4fa91` (session-side wait armed — RE-ARM after rotation) → report whole → head re-read → completion vs the brief's 8 asks → **score s193** → close after `end_turn` → on GO: a merge (EXPECT_T/EXPECT_TREE; census KS-754 after) |
| `%3` | **s196** (`Secuura/Blockchain`) — finish s194's ITEM 3: rebuild the merge script durably in `5_Project_History/merge-protocol/`, squash #961 @ `644965d90` onto `b1cb8466f`, KS-1098 closing-round + P7, history for s194 + s196 | booting (brief verified at destination 23:00:07Z) | rung 5 → **ANSWER its plan confirmation** (check: the rebuilt script's gates and three DRYRUN negative controls; EXPECT_TREE vs s194's `e377205046e0…`; KS-1111 + both comments equal to s194's drafts; KS-1098's pre-PUT state) → STATUS with M → verify at source → wrap → score (a merge of a gated PR + records: no new gate) |
| `%1` | monitor | — | — |

**develop = `b1cb8466f`** (GitHub REST 08:4x). **KS active (unstarted+started types) = 121** (`board_count.sh`, real count, 08:4x). **Kintsugi = `4554b25e2`.** Demo unchanged.

## 🟢 KAM'S RULINGS AND GRANTS IN FORCE (check expiry by `date`)
- **Keep the pace** — panel 2026-09-12 13:51 *"please run multiple secure agents if you can.  We need to get through these tickets ASAP"* · 13:55 *"peep the pace going until the tickets are cleared or below 100"*. Stop: tickets cleared / KS active < 100 (121) / allowance out (`7d:1%` at 08:44 — reset landed).
- **We approve and merge our own TESTED Secuura work** — open-ended (2026-09-11 16:56 / 17:50:39).
- **Kintsugi deploys rest on v1.3 + Kam 2026-09-10 13:22 "deploy to kintsugi first".**
- **Week grants (deploy freely to kintsugi AND demo; production ban lifted; merge-for-the-week) — END OF SUNDAY 13 SEP is a reading; `EXPIRING-GRANTS.md` says ASK before relying on them on the 13th. Nothing queued today relies on them.** Demo (UAT) waits for Peter's nod regardless.
- **Overnight is working time** (08-28). **Deploys to dev take the full tier-1 gate.**

## 🔵 QUEUE (in order)
1. **#962 verdict** → as the `%2` row.
2. **s196** → as the `%3` row.
3. **#963 (KS-1109) tier-2 gate** — the set is being drafted by a subagent in the seat scratchpad `gate963/` (launcher + brief + prompt + red-proof on scratch copies). Re-read it, install into `2_Project_Files/fleet/qa-agent/launchers/` and `…/briefs/`, real `--check`, commit, **launch ONLY via `cockpit.sh add "QA/Secuura-ks1109-963" "bash <launcher path>"`**, arm a verdict wait. #963 verified at source 08:5x: `90d7d0c75`, 2 files, ahead 1 / behind 1, merge-base `34be9c18a`, body only KS-1109. **Score s192 + s195 after its verdict.**
4. **s197 — KS-1103 then E3** (`Secuura/Blockchain-C`) — brief drafted by a subagent at the scratchpad `s197_ks1103_brief.md` + `s197_loadbearing.md`. Re-read every load-bearing line, SELF-CHECK attest, `brief_and_launch.sh --to "Secuura/Blockchain-C"`. Source: `HANDOVER-s193-ks1029-ks1103.md` (FINAL).
5. **KS-1110 (QA-960-2)** fix round — after #963 merges (same package).
6. **#928 rework** (loader half + KS-962's ratified shape, then a re-gate) and **#913** rebase + re-gate — builder seats. Before ANY merge GO from a census: read the PR's review comments and every linked ticket.
7. **Runtime gates on #872** (needs the QA login: keys `KINTSUGI_QA_GATE_OWNER_EMAIL`/`_PASSWORD` in the Secuura `.env`), **#896, #728, #808** on kintsugi — tier 1; possible now the allowance reset. Peter's PS-831 branch is not a base.
8. **Lanes 2-3** from `0_Brain/reference/2026-09-12_secuura-lanes/secuura_lanes.md` (KS-1020 item 1; KS-1071 → 1070 → 1069) — re-read before briefing.

## 🔴 WITH KAM (on his panel — do not re-list)
- Carried: the Stuart reply for KS-597 · `Notes (MASTER)/skills/Current/extranet.md` vs his tickets-only rule · the agent GitHub identity invite + raise-to-1 · deleting `feature/y` / `feature/w` · **measure first:** KS-775's lapsed window · the vault's `daily/2026-09-11.md` uncommitted lines · develop's CI reds (KS-1075).
- Today: **`/login` queued at this seat's prompt** (told on the panel 08:54).

## 🟡 OWED BY WEDNESDAY
0. **The 16:04 diagnosis → ledger row → fix or card, BEFORE any self-rotation.**
1. **`panel_sync` has no re-arming** (launcher 0 lines; doctor does not check it) → a doctor FAIL check + launcher arming; claim with Tuesday first (her launcher mirrors it).
2. **QA launchers exec `claude` directly** → run them only via `cockpit.sh add`; guard candidate: refuse when stdin is not a TTY.
3. **`wake_watch.sh` fixes (SHARED — claim first):** QA-tag subjects count as inbound · never `stable_n=9999` while panes are live · idle/frozen legs cannot tell a seat waiting on its own background shell from a stall.
4. `panel_sync` RECOVER detector (Tuesday's 09-12 measurement) · scoreboard union-merge.
5. **WED-148:** no `wed_claim.sh` verb while `panel_sync` is live — read `0_Brain/tasks/WED-OWNERSHIP.md` directly.
6. **At the WRAP:** rule 3b regenerate BOTH digests (the ledger changed today) · rule 3c archive ledger rows dated 2026-09-10 and earlier, conservation asserted.
7. Carried: QA agents' memory notes (non-gate session) · QA charter line · send gate refusing `extranet` outside HOLDS · pretooluse items · `inbox_digest.sh` ack · `send_brief.sh` double-prefix · reconcile in the watcher · 18 Secuura ruled-undelivered cards · Kam's `vault-add-a-stages-another-clients-files` grant · the family-weight index · a tracked home for the verdict-wait helper.

## ⚠ TRAPS
- **`/private/tmp` is wiped at reboot** — nothing a successor needs may live only in a scratchpad.
- **Never run a QA launcher in the Bash tool** — it runs headless and dies with the seat.
- **The provenance gate reads `a/b/c` as a relative path** (e.g. `spf/dkim/dmarc`); branch names and `pulls/N` too.
- **The seat-scoped chat hook refuses any chat-store read that never mentions `view`** — use `kam_msgs.sh`, or print `view`.
- **FIRST WRITE OF THE BOOT: commit the launcher's regenerated digests** by literal path — not via `wed_claim.sh`.
- **The `[Datasec/ATTIO -> Wednesday] DAILY FOLLOW-UP DIGEST` lands in `wednesday-agent@` ~07:00 AEST** — SUBJECT ONLY; every inbox reader filters on the expected routing tag BEFORE touching a body.
- **Linear's suggested branchName can carry ANOTHER ticket's id** (KS-1029 → KS-754 walked). Strip it before the first push; census KS-754 after #962 events.
- **Peter's untested build-script branch** (PS-831 / KS-1096) — he tests Monday 2026-09-14; never a base.
- **Peter merges his own PRs at night** — every merge brief STOPs on a moved develop unless the T-move rule clears it.
- **Builder seats cannot see their own gauge:** CHECKPOINT at 50%, HAND OVER NOW at 70%; read statuslines at every wake.
- **Before a pane close, read the transcript's last assistant row for `end_turn`.**
- **Write and commit in ONE command.** zsh: no `PIPESTATUS`; list variables do not split; `echo ======` aborts; `grep` is a shell FUNCTION — `/usr/bin/grep` with a same-file control.
- **GitHub's compare API caps at 300 files.** A file census comes from an uncapped `git diff`.
- **The prior-ruling gate refuses on shared words:** open EVERY match, then override with the measurement.
- **Tool paths:** `brief_and_launch.sh`, `send_brief.sh`, `self_check_view.sh` in `2_Project_Files/fleet/`; `cockpit.sh`, `pane_close.sh`, `pane_prompt_check.sh`, `wednesday_rotate.sh`, `wake_watch.sh` in `fleet/cockpit/`; QA launchers in `fleet/qa-agent/launchers/`.
