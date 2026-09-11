---
date: 2026-09-12
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's — read her mail by SUBJECT only, never brief or answer for a Datasec project.
source: replaced WHOLESALE at 2026-09-12 08:40 AEST by the seat booted 2026-09-12 05:21 (boot ctx 47%; this pickup written at ctx ~76%).
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — updated 09:15 AEST at the rotation. **Kintsugi runs `4554b25e2`; its tier-1 deploy gate returned GO WITH FINDINGS; s187 scored 1.00. Kam's two after-gate rulings are released for delivery.**

> Narrative: `0_Brain/daily/2026-09-12.md` from the 05:21 boot block. **Measure before acting on any line here.**

## 🟢 FLOOR
| pane | seat | state | next event the successor owes |
|---|---|---|---|
| `%29` | QA/Secuura-kintsugi-deploy — verdict MAILED 23:11:34Z (GO WITH FINDINGS) | closed by the 05:21 seat at rotation if its transcript read `end_turn`; else close it after checking | — |
| — | no Secuura seat live | — | **brief ONE Secuura seat for QUEUE item 1** |
| `%1` | monitor | — | — |

**develop = `4554b25e2`** (#958; nothing merged since 19:10:50Z at the last read). **Kintsugi = `4554b25e2`** (s187: 33 built, 25 swapped, 0 rolled back, 39/39; Wednesday's public probe agrees). **Demo unchanged** (last deployed `0f8fb33c3` by s169). **Scored overnight:** s183 0.95 · s184 0.90 · s185 0.95 · s186 1.00. **s187 SCORED 1.00 at the verdict; the QA agent 1.00.**

## 🟢 KAM'S RULINGS AND GRANTS IN FORCE (check expiry by `date`)
- **We approve and merge our own TESTED Secuura work** — open-ended (Kam 2026-09-11 16:56 / 17:50:39). TESTED = a QA gate at the current head + Test Evidence + our suites.
- **Kintsugi deploys rest on v1.3 (dev deploys) + Kam 2026-09-10 13:22 "in the future deploy to kintsugi first"** — NOT on the week grant.
- **Week grant "deploy freely to kintsugi AND demo" — END OF SUNDAY 13 SEP is an unconfirmed reading; `EXPIRING-GRANTS.md` says ASK before relying on it on the 12th or 13th.** Demo (UAT) waits for Peter's nod regardless.
- **Overnight is working time** (08-28). **Deploys to dev take the full tier-1 QA gate** (`learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md:16`).

## 🔵 QUEUE AFTER THE `%29` VERDICT (in order)
1. **ONE Secuura seat delivers Kam's two 08:50 rulings — the after-gate condition is MET (GO WITH FINDINGS at 23:11:34Z):**
   - post the two drafted refresh comments exactly as in `!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-s187-kintsugi-deploy.md` lines 108-121 (`@peter` on KS-485, `@stuart.jamieson` on KS-772; verify each mention by `bodyData`) → `decision_queue.sh rule … --delivered` naming both comment ids;
   - `docker builder prune` on kintsugi — no image removal, both `:pre-*` tag sets kept, free space measured before and after → `--delivered` naming the numbers;
   - file the gate's findings as tickets (our board account, BLUF-first; Kam's 09-07 13:23 rule: separate fixes → separate tickets): F-1 status-page port defaults · F-2 anchoring aggregates read `response.ok` only · F-3 topology on unauthenticated status endpoints · F-4 public verify ignores `hash` · F-5 unnamed verifier tabs · F-6 the admin login placeholder · F-7 the mistyped-id message; G-1 as a coverage ticket naming #728, #872, #936, #808, #896.
   - Gate report: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-12-kintsugi-deploy-4554b25e2-tier1-r1/report.md`.
1a. **Card for Kam (G-1's runtime half):** a QA test credential on kintsugi, so #872/#896/#936/#954/#935 can be gated at runtime — his call (a credential on a running system). Through-code gates for #872 and #896 first (the gate's own risk read). **Search BOTH Secuura report trees** (`projects/secuura/` and `projects/secuura-blockchain/`) before calling anything ungated (brief error B-1).
2. **KS-1098 (mask spellings + name set for Peter + PASSWD cell) and KS-1099 (YAML error prints secrets-file lines) fix rounds** → tier-2 gates. **Plus the merge script's TREF gate reading an ABSENT path as its own argv echo under `2>/dev/null`** (s186) → fix to `cat-file -e`. KS-1097 (Low) after.
3. **The 36 untested PRs** — re-census first (the s181 census is many merges old); plan gates by tier. **7-day allowance read 83% at 08:38 (the QA pane: resets 04:00 AEST Sun)** — spend beyond it is a card for Kam.
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
