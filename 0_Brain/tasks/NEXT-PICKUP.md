---
date: 2026-09-25
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: replace wholesale at the next pickup; do not append
---

# NEXT PICKUP

## ⏩ 2026-09-25 ~10:00 — the morning seat at its 50% checkpoint (previous copy: the newest `.pre-0925-*-checkpoint` beside this file)

**ACCOUNT:** Kam signed into a NEW account at ~09:39 (user email now the hpauthsuite one). Statusline 7d:0%, and `usage_gate.sh` OK. Launches are open again under the 90% rule.
**Kam today:** terminal only. 0 rows on the Wednesday tab. Every message is receipted on the panel. He is travelling? UNKNOWN today. He is at the Studio and plugged a Spark in "using a cable".
**Tuesday:** BACK (her mail 23:35Z; wake_wednesday.sh alarm change f4ed4d47d pulled). **Friday:** live on the laptop and driving Datasec seats.

### LIVE RIGHT NOW
**UPDATE at the 66% checkpoint (Wednesday seat, 2026-09-25 ~11:1x):** **Seat B 25th is LIVE on Secuura/Blockchain** (the pane NAME `Secuura/Blockchain`; `cockpit.sh say` wants the NAME, `pane_close.sh` wants the %id). Brief `fleet/briefs_staged/2026-09-25_seatB25_raise-round21-auditrows.md`. Plan CONFIRMED (tier 1 ×3, one batch). Audit rows RULED by Wednesday's ANSWER: BUILD three fixes, one PR each, BEFORE the Ornith PRs: frvp standalone legs (mcp-server lock, originate override; KS-530); jjmj four locks to 6.30.6 + REMOVE its baseline row (the only authorised baseline edit; KS-528); mwp4 issuer override (KS-729). The ROOT-lock residue (hoisted ip-address 9.0.5 HIGH + @prisma/dev-nested hono 1.19.11) is Kam's card `secuura-audit-root-lock-residue-0930` (rec c; default: the seat attempts a full re-resolution; no renewal without his word). The seat MEASURES the re-resolution only, pushes nothing from it. **Round end: 6 PRs READY → ONE tier-1 batch gate → Wednesday's signed GO → merges one at a time. No deploy.** The PR 1 gate must red-prove F-A's relaxation of property 2, or record it as a KS-1131 residual. **FUSE: audit rows lapse 2026-09-30T00:00Z (Wed 10:00 AEST); after that, every push is refused.** Ornith: queue empty BY MEASUREMENT (the why-line is in queue.md). Spark: waiting on Kam's NVIDIA Sync sign-in (Studio sees it at zgx-15d5.local = 192.168.7.113; ssh key refused; scope card ruled c).
**UPDATE ~10:1x:** Seat B 24th WRAPPED, scored 0.98, and its pane is closed. The five cards are delivered (Secuura undelivered 25). **Floor clear.** 🔴 **DATED: audit-baseline.json has three rows expiring 2026-09-30 (Seat B 24th measured it; not re-read by Wednesday; the old "09-24 fuse" was wrong).** A Secuura round must renew or fix them before Wednesday 30 Sep, or pushes block. Ornith KS-1131 F-A PASS HELD (`night/READY_KS-1131-…PASS-7of7_2026-09-25.diff.md`). A drafter is writing the F-B/F-C briefs (it returns text; Wednesday saves, verifies, queues with `test_file=<product>`). Spark: waiting on Kam's NVIDIA Sync sign-in, then a client-neutral check only (no password taken).
1. **Seat B 24th — Secuura/Blockchain, pane `Secuura/Blockchain` (%2).** Brief `fleet/briefs_staged/2026-09-25_seatB24_fetch-close-rulings.md`. ITEM 0 DONE (develop 6ab9d5021 fetched; Wednesday verified `cat-file` = commit). Plan CONFIRMED by ANSWER 23:57Z with rulings. DONE: KS-1019, KS-1245, KS-1287, KS-1239 (+ residue comment). STAYS: KS-965, KS-851, KS-1081, KS-1139, KS-1033, KS-1084, KS-1143. No duplicate for 2.1 (KS-1243 exists): comments on KS-1084 and KS-1243. File 3a LEGD-BYTEXT and 3b `.dockerignore` (path `Blockchain/Dev/.dockerignore:13`). 3c stops (tooling outside the repo). **NEXT for the successor: read its WRAP mail; `decision_queue.sh rule/--delivered` the five cards (ks1084-part-b, ks974, ks1163, ks998, ks789) FROM its comment ids; score; `pane_close.sh` in the same action.**
2. **Ornith: KS-1131 F-A.** Round 1 (R20) FAILED A3c. The cause was a HARNESS fault, not the model: `tasks/code_patch/task.md:113` told the model to prefix red cells with 🔴, which contradicts the brief's exact `it(` line. Fixed (backup `task.md.pre-0925-redprefix`; IMPROVEMENTS row 09:5x). Re-queued the SAME input as a harness-fault resume, so **the one rebrief is still unspent.** Read-back: `night/done.md` second KS-1131 row → `runs/2026-09-25_ks1131-ornith35b-night*` → on PASS, `hold_ready.py`. KS-1131 items 2-4 (F-B :206, F-C :256, P2 wallet slice) are the next briefs. They need a `test_file=<product>` pin: a self-testing brief whose `## The test` names an EXISTING file is refused without it.

### DONE THIS SEAT
- **Live-board wake (Kam 09:34 via Friday):** `Launch_Wednesday.command` arms `live_chat_poll.sh --seat $AGENT` before the doctor preflight (tuesday with `tap_tuesday.sh`), and `doctor.sh` FAILS on a down or FAILING poller. Commit 09b28c3b6. Studio poller running (started 09:42 by the arm test). Friday re-tested on the laptop: PASS. Tuesday told. **OWED (c):** a per-seat tap label (cockpit's `[Wednesday tap]` prefix is what agents and the rung-10 detector recognise, so change it with care).
- Morning receipt + corrections on the panel. Ledger +1 (weekday/seat-name slip; an inference sat under a "measured" heading).

### SPARK (Friday owns the box and the kit)
Kam: "I have added a spark to this machine connected using a cable." **The Studio sees NO link** on any wired interface (en0, en2-7, en8-13, bridge0). `zgx-15d5.local` does not resolve, `.33` gets no answer, and there is no mDNS entry. Kam has been asked to check power and plug the Spark's RJ45 into the Studio's Ethernet port. Friday: there is no known direct-cable setup, the wired NIC has no IP (a sudo change, Kam's hands), and the proven path is the office Wi-Fi. The box was likely shut down 09-24. **Kam ruled Friday's scope card `c` 09:49: "Not yet: I'll decide after the Studio can connect."** So nothing client-scoped goes to it. Next once it is visible: the Studio needs its own login on the box (NVIDIA Sync, Kam's hands). Handout: `0_Brain/reference/2026-09-22_spark-deepseek-v4-flash/STUDIO_HANDOUT_2026-09-25.md`.

### CARRY (unchanged)
- KS-1143 indirect-invocation FN and KS-1084 P0 stay open. `decision_queue.sh list ruled --undelivered` = 75, read as a LIST. Also ruled and undelivered: `secuura-ks789` (in this round) and `wed-ornith-pool-thin-widen-the-harness` (a, 09-23).
- The pickup's former OWED list is below (items 1-7 still owed).

### What FRIDAY is (do not re-derive)
Third coordinator seat, Kam's laptop, BOTH clients. Launcher `Launch_Friday.command` (refuses outside a FRIDAY tree) → `2_Project_Files/friday/first_run.sh` once → shared `Launch_Wednesday.command` with `WED_AGENT=friday`. Inbox `friday-laptop-agent@agentmail.to`. Live-board partition `Friday` (Entra `friday-seat` be8404ab-…). Per-client identity via `friday/friday_as.sh`. Claims every project with `wed_claim.sh` before driving it. Reports: `fleet/REPORT_2026-09-23_friday-seat-tools.md`, `dashboard-cloud/REPORT_2026-09-23_friday-seat.md`. Brain: `tasks/FIRST-BOOT-FRIDAY.md`.
**⚠ The Friday certificate ALSO sits on the Studio (`4_Credentials/dashboard-cloud/friday-seat.pem`) — this machine can act as Friday while it does. Never use it from this seat except to verify.**

### OWED (mine; none blocks Kam; all are Wednesday-only tooling, doable under the 90% cut)
1. `dashboard-cloud/seat/publish_usage.sh:30` → accept `friday`. It is RUNNING (pid 9380 at 11:5x): stop the loop, edit, run once, re-arm (never edit a running bash script).
2. doctor.sh warns "Launch_Wednesday.command has no recognisable --model line" — stale since Tuesday's e402c5bc7 (10:35, Kam 09:33 on HER tab: launchers follow the configured default). The PREVIOUS pickup's claim that the launcher pins `--model claude-opus-5-5 --fallback-model opus` is FALSE — it was unpinned. Fix the check to accept "no pin"; read Kam's 09:33 words on the Tuesday tab first.
3. `get_kam_messages.py --json` does not filter synthetic rows (text output does).
4. No `fleet/USAGE_STOP.friday` — Friday inherits Wednesday's cut. Ask Kam only if it bites.
5. Friday cannot read the 3 pre-existing ALL rows until `migrate_rewrap.py` (changes live rows — it was not run).
6. Literal "wednesday" pane names in cockpit.sh:90,460 · pane_close.sh:72 · pane_prompt_check.sh:29 · monitor.sh:213 · tap_wednesday.sh:78 (Tuesday has the same gap).
7. Carried from before: `hold_ready.py` cannot carry a card ruling; `night_run.sh:403` discards G7 alert stderr (stop job → edit → --once → re-arm); code_patch builder should refuse `product_file` under `__tests__/` (KS-1143 is ONE round, rebrief as test_only is its last local round); `checker.sh:660` `2>/dev/null` on a3c_plus.
8. ✅ **DONE 2026-09-24 00:40 (rc 0, 534,663 files / 44 GB; Kam told on the panel) — do not re-run.** Was: **OWED 0 (dated today):** after the 03:30 NAS leg of 09-23 FINISHES (`scheduler/state/nas_sync_last_wednesday.txt` shows 09-23; the leg ran 7h20m+ at 10:50 — an outlier; if still running near 03:30 on 09-24 two legs overlap) run `5_Project_History/2026-09-21_portable_blind_copy_KK_DEV_Local.sh` with `/Volumes/KK_DEV_Local` mounted, then tell Kam total + rc. Do NOT `tail` the unison log (`\r` progress, MB in "4 lines").

### Ornith
See the KS-1143 block at the top (HELD 17:23). The OWED item 7 line about rebriefing KS-1143 as test_only is SUPERSEDED — it went through the new self-testing mode instead.

### RULED BY KAM, NOT YET IN AN ARTEFACT (Secuura) — unchanged from the previous pickup, carry into the next Secuura brief
`secuura-ks998-…-prettier` (a + "and install it also" — note, not machine-readable) · `secuura-ks1163-…` (a; Claude's, at the counter) · `secuura-ks974-…` (a; correct the record on KS-974) · `secuura-ks1084-part-b-…` (a). And read `decision_queue.sh list ruled --undelivered` as a LIST, not a number.

### STANDING RULES (carry)
`safe_push.sh "<message>" <paths…>` — first arg is the MESSAGE; a path list from a variable needs `${=VAR}` (zsh). `cd` REFUSED (even `cd /dev/null`). The live board's hide `--reason` accepts only `[A-Za-z0-9 ._:/()+'-]`, ≤160 chars. Builder subagents CANNOT write report files (harness) — have them return the report as text and save it yourself. A "local" dashboard matrix hits the REAL store unless the new guard stops it (`LIVE_STORE_MATRIX_OK=1` only on purpose). Read any tool output you are about to assert to Kam WHOLE, never through `tail`.
