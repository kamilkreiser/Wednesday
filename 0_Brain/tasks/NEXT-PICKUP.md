---
date: 2026-09-12
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's — read her mail by SUBJECT only, never brief or answer for a Datasec project.
source: replaced WHOLESALE at 2026-09-12 08:40 AEST by the seat booted 2026-09-12 05:21 (boot ctx 47%; this pickup written at ctx ~76%).
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — updated 09:15 AEST at the rotation; FLOOR + QUEUE item 1 updated 09:35 by the 09:15-rotation seat. **Kintsugi runs `4554b25e2`; its tier-1 deploy gate returned GO WITH FINDINGS; s187 scored 1.00. ✅ Kam's two after-gate rulings are DELIVERED by s188 (`%30` closed). ✅ His 11:34 `qa-login` ruling is DELIVERED (login half) by s189 — scored 0.95, `%31` CLOSED 12:28. The runtime gates on #872/#896/#728/#808 wait for the Sunday 04:00 allowance reset.** (12:3x, the 12:08-rotation seat)

> Narrative: `0_Brain/daily/2026-09-12.md` from the 05:21 boot block. **Measure before acting on any line here.**

## 🟢 FLOOR
| pane | seat | state | next event the successor owes |
|---|---|---|---|
| `%29` | QA/Secuura-kintsugi-deploy — verdict MAILED 23:11:34Z (GO WITH FINDINGS) | CLOSED 09:16 by the 05:21 seat after `end_turn` | — |
| `%30` | s188 — QUEUE item 1 | **WRAPPED 00:34:54Z, verified at source, scored 0.95; CLOSED 10:36 after `end_turn` (listeners 28 → 28)** | — |
| `%31` | **s189** — the kintsugi QA login for KS-1100 (Kam ruled `qa-login` 11:34:34) | **WRAPPED 02:24:46Z (spf/dkim/dmarc pass), VERIFIED AT SOURCE, SCORED 0.95, CLOSED 12:28 after `end_turn` 02:26:17Z (listeners 28 → 28). Account `qa-gate-ks1100-owner-4662d9` (OWNER, default tenant, no org), keys `KINTSUGI_QA_GATE_OWNER_EMAIL`/`_PASSWORD` in the Secuura `.env` (0600). KS-1100 comment `0b99860b` (0 `@`, password + full address absent — Wednesday's read). KS-1107 High. Card `--delivered` (login half). Was: plan CONFIRMED 02:07:02Z** (one OWNER account via public register; P1 SELECT-only in-container read-back; P2 A; P3 the unchecked register `organizationId` filed as its own High ticket, never exercised) — executing ITEM 1 → 3 | read its wrap or STOP mail · verify at source: the KS-1100 comment (no secret, no `@`) and the P3 ticket · `decision_queue.sh --delivered secuura-kintsugi-qa-login-for-ks1100` (login half) · score · `pane_close.sh %31` after `end_turn` · CHECKPOINT at 50%, HAND OVER NOW at 70% · the runtime gates (#872 first) after the 04:00 Sunday allowance reset |
| `%32` | **s190** — KS-1099 as PR #960 | **WRAPPED 03:28:28Z (auth pass), handover `HANDOVER-s190-ks1099-pr960.md` (8,235 B, FINAL, KS-1098 plan rows R2 / R_eq..R_pw / T_a..T_d, ITEM 3 template sha) + history `:24` verified; CLOSED 13:31 after `end_turn` 03:28:58Z (listeners 28 → 28). KS-1098 and ITEM 3 NOT started.** | **score AFTER the #960 verdict** |
| `%33` | **QA/Secuura-ks1099-960** — TIER 2 GATE #960 ROUND 1 @ `0e70ed1c7` | **LAUNCHED 13:30** (`fleet/qa-agent/launchers/launch_qa_secuura_ks1099_960.sh`, red-proof 14 cells FAILS=0, `--check` 0); **rung 5 from its transcript 13:32:24**; verdict wait armed in Wednesday's session (subject `[QA -> Wednesday] TIER 2 GATE #960 ROUND 1`, 120 s poll, ~3 h) | verdict → head re-read → completion check vs the brief's 8 asks → score s190 → GO: a merge seat squashes #960 (TESTED grant) and KS-1099 Done · NO GO: fix round from HANDOVER-s190 · `pane_close.sh %33` after `end_turn` |
| `%1` | monitor | — | — |

**develop = `4554b25e2`** (#958; nothing merged since 19:10:50Z at the last read). **Kintsugi = `4554b25e2`** (s187: 33 built, 25 swapped, 0 rolled back, 39/39; Wednesday's public probe agrees). **Demo unchanged** (last deployed `0f8fb33c3` by s169). **Scored overnight:** s183 0.95 · s184 0.90 · s185 0.95 · s186 1.00. **s187 SCORED 1.00 at the verdict; the QA agent 1.00.**

## 🟢 KAM'S RULINGS AND GRANTS IN FORCE (check expiry by `date`)
- **We approve and merge our own TESTED Secuura work** — open-ended (Kam 2026-09-11 16:56 / 17:50:39). TESTED = a QA gate at the current head + Test Evidence + our suites.
- **Kintsugi deploys rest on v1.3 (dev deploys) + Kam 2026-09-10 13:22 "in the future deploy to kintsugi first"** — NOT on the week grant.
- **Week grant "deploy freely to kintsugi AND demo" — END OF SUNDAY 13 SEP is an unconfirmed reading; `EXPIRING-GRANTS.md` says ASK before relying on it on the 12th or 13th.** Demo (UAT) waits for Peter's nod regardless.
- **Overnight is working time** (08-28). **Deploys to dev take the full tier-1 QA gate** (`learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md:16`).

## 🔵 QUEUE AFTER THE `%29` VERDICT (in order)
1. ✅ **DONE by s188 (09:30 → 10:35, scored 0.95): notice on KS-485 `6a490ad0` + KS-772 `0adb9a41`; kintsugi build cache pruned (81% → 38%); G-1 → KS-1100, F-1 → KS-864 comment `f0ed3d91`, F-2..F-7 → KS-1101..KS-1106. BOTH cards marked `--delivered`.** Original item text follows for the record: **IN FLIGHT as s188 `%30` (launched 09:30) — ONE Secuura seat delivers Kam's two 08:50 rulings — the after-gate condition is MET (GO WITH FINDINGS at 23:11:34Z):**
   - post the two drafted refresh comments exactly as in `!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-s187-kintsugi-deploy.md` lines 108-121 (`@peter` on KS-485, `@stuart.jamieson` on KS-772; verify each mention by `bodyData`) → `decision_queue.sh rule … --delivered` naming both comment ids;
   - `docker builder prune` on kintsugi — no image removal, both `:pre-*` tag sets kept, free space measured before and after → `--delivered` naming the numbers;
   - file the gate's findings as tickets (our board account, BLUF-first; Kam's 09-07 13:23 rule: separate fixes → separate tickets): F-1 status-page port defaults · F-2 anchoring aggregates read `response.ok` only · F-3 topology on unauthenticated status endpoints · F-4 public verify ignores `hash` · F-5 unnamed verifier tabs · F-6 the admin login placeholder · F-7 the mistyped-id message; G-1 as a coverage ticket naming #728, #872, #936, #808, #896.
   - Gate report: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-12-kintsugi-deploy-4554b25e2-tier1-r1/report.md`.
1a. ✅ **DONE by s189 (login half; gates owed after the Sunday 04:00 reset — per s189: #872 needs the login, password branch only; #896 no login, runtime-inert; #728 no login; #808 spec-only). RULED `qa-login` by Kam 11:34:34 → was IN FLIGHT as s189 `%31` (launched 11:38): roles measured and confirmed before any account is created; kintsugi only; the runtime gates follow after the Sunday 04:00 allowance reset.** **CARD FILED 10:4x: `secuura-kintsugi-qa-login-for-ks1100` (rec `qa-login`; default nothing created; prior-ruling gate overridden after opening all ten matches) — on Kam's panel, do not re-list.** Still owed to route: KS-671's nft-certificate `status: 'healthy'` split (unfiled).
2. ✅ **KS-1099 DONE to READY (PR #960, gate running `%33`). KS-1098 NOT STARTED — next Secuura seat builds it from `HANDOVER-s190-ks1099-pr960.md` plan rows, only if the allowance is below 95%. Was: IN FLIGHT as s190 `%32` (12:39) — QA-958-2 (name set + BASE_URL userinfo) deliberately NOT in the round; it stays open on KS-1098 as Peter's input, to go to Kam.** Was: KS-1098 (mask spellings + name set for Peter + PASSWD cell) and KS-1099 (YAML error prints secrets-file lines) fix rounds → tier-2 gates. **Plus the merge script's TREF gate reading an ABSENT path as its own argv echo under `2>/dev/null`** (s186) → fix to `cat-file -e`. KS-1097 (Low) after.
3. **The 36 untested PRs** — re-census first (the s181 census is many merges old); plan gates by tier. **7-day allowance read 83% at 08:38 (the QA pane: resets 04:00 AEST Sun)** — spend beyond it is a card for Kam. ⚠ **09:3x: SHARED with Tuesday's seats, 85% at 23:31Z, ~1.5 points/hour (Tuesday's trend) → 100% around 19:00-20:00 AEST, before the reset. Kam ruled `raise-limit` on `wed-weekly-quota-97pct` (proceed normally); both coordinators hold one line: from 95%, no new launches, live seats checkpoint and push.** Items 2-3 are the heavy spend — launch only if the rate says they fit.
4. **Teardown candidates (Kam's call; quarantine, never delete):** `worktrees/s187-kintsugi`, `worktrees/s184-ks1094`; the #954 gate's disposable artefacts.

## 🔴 WITH KAM (on his panel — do not re-list in every message)
1. ~~Card `secuura-kintsugi-refresh-notice-release`~~ **RULED after-gate 08:50:29; its gate PASSED (GO WITH FINDINGS) — delivery = QUEUE item 1.** The draft is in `!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-s187-kintsugi-deploy.md`, lines 108-121.
2. ~~Card `secuura-kintsugi-build-cache-prune`~~ **RULED cache-only 08:50:39 — delivery = QUEUE item 1.** Kintsugi is at 81% disk, 24.5 GB free.
3. Carried: the Stuart reply for KS-597 · `Notes (MASTER)/skills/Current/extranet.md` vs his tickets-only rule · the agent GitHub identity invite + deleting `feature/y` / `feature/w` · **measure first:** KS-775's lapsed window · the vault's `daily/2026-09-11.md` uncommitted lines · develop's CI reds (KS-1075, already told).

## 🟡 OWED BY WEDNESDAY
1. **`wake_watch.sh` fix (SHARED with Tuesday — claim first):** QA-tag subjects count as inbound for the mail leg · **never arm `stable_n=9999` while any cockpit pane is live** (hit again 08:32 → 08:38) · the frozen/idle legs cannot tell a seat waiting on its own named background shell from a stall (9 false wakes during s187's build).
2a. **`panel_sync.sh` RECOVER detector (Tuesday's measurement 2026-09-12 08:46-08:47 on her tree):** twice it logged `rebase --continue failed with nothing conflicted, aborting` while a `CONFLICT (content)` on a derived JSON was live — the unmerged-path check read empty; it self-recovered on the third cycle. Read the detector against a planted content conflict before changing anything (the 09-10 detector-keyed-on-remedy-text lesson).
2. **WED-148: `wed_claim.sh` pulls `--rebase --autostash` on EVERY verb** — it left a stopped rebase at the 05:21 boot. **Until fixed: no `wed_claim.sh` verb while `panel_sync` is live; read `0_Brain/tasks/WED-OWNERSHIP.md` directly.**
3. The QA charter line (no memory maintenance in a gate) · the QA agent's own memory notes (a non-gate session) · the send gate refusing `extranet` in a Secuura brief outside HOLDS · the pretooluse hook items (`PIPESTATUS`; `grep -c` without `-i`; bare `grep` with `$(`; `2>/dev/null` on a composed path) · `inbox_digest.sh` acking only what it printed · `send_brief.sh` double-prefixing · `reconcile_rulings.py` in the watcher · the launcher committing its digests · 18 Secuura ruled-undelivered cards · Kam's `vault-add-a-stages-another-clients-files` grant · the family-weight index.
4. **At the next WRAP, rule 3b:** `learnings/_ledger.md` changed today (2 rows) → regenerate BOTH digests. **Rule 3c:** archive ledger rows older than ~3 days (09-09's 112 rows, ~293 KB), with conservation asserted.

## 🟠 NAS
The 2026-09-12 03:30 leg: rc 2 (source files changed mid-sync) · 8 deletions, all Secuura working-tree paths from a branch switch in that checkout · **all 4 source/test paths verified ON develop** (GitHub contents API, nonexistent-path control 404).

## ⚠ TRAPS
- **Peter's untested build-script branch (Kam relayed 2026-09-12 11:58):** Peter pushed a branch he tests on Monday 2026-09-14, pointing at PS-831 (platform-s #814, slot isolation; platform-k side KS-1096 `start-secuura.sh`). **Before any kintsugi rebuild or local-stack run, read PS-831 + KS-1096 and ask whether Peter's branch has landed; never build from his untested branch.** The branch itself is unmeasured by Wednesday.
- **FIRST WRITE OF THE BOOT: commit the launcher's regenerated digests** by path — **not** via `wed_claim.sh`.
- **The `[Datasec/ATTIO -> Wednesday] DAILY FOLLOW-UP DIGEST` lands in `wednesday-agent@` ~07:00 AEST daily** until Tuesday re-routes it — SUBJECT ONLY. **Every inbox reader filters on the expected routing tag BEFORE touching a body.**
- **The 05:30 shift-change tap says "wrap"; `wake_wednesday.sh` case 3 means a live seat IS the morning seat and continues.**
- **GitHub's compare API caps at 300 files** (a real 308 hid 8). A file census comes from an uncapped `git diff` in a clone.
- **The provenance gate reads a branch name or `pulls/N` as a relative path** — describe remote reads in words.
- **The prior-ruling gate refuses on shared words:** open EVERY match, then override in the JSON key `_override_prior` with the measurement.
- **Python heredocs inside an `if` block break on indentation** — write the script to a file, then run it.
- **Peter merges his own PRs at night.** Every Secuura merge brief STOPs on a moved develop unless the brief rules the exact base and tree.
- **Builder seats cannot see their own gauge:** CHECKPOINT at 50%, HAND OVER NOW at 70%; read their statusline at every wake.
- **Before a pane close, read the transcript's last assistant row for `end_turn`** (`~/.claude/projects/<project>/<session>.jsonl`).
- **Write and commit in ONE command.** zsh: no `PIPESTATUS`; a list variable does not word-split; `echo ======` aborts. The Bash tool's `grep` is a shell FUNCTION — use `/usr/bin/grep` with a same-file control.
- **Tool paths:** `brief_and_launch.sh`, `send_brief.sh` in `2_Project_Files/fleet/`; `cockpit.sh`, `pane_close.sh`, `pane_prompt_check.sh`, `wednesday_rotate.sh`, `wake_watch.sh` in `fleet/cockpit/`; QA launchers in `fleet/qa-agent/launchers/` (latest: `launch_qa_secuura_kintsugi_4554b25e2.sh`, the first deploy gate, red-proof 16 cells).
