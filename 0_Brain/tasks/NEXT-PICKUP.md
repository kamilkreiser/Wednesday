---
date: 2026-10-06
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE 2026-10-06 19:1x by the evening seat (booted 18:0x) at its 52% checkpoint. Replace wholesale again; never stack.
---

# NEXT PICKUP

## 🔴 FIRST ACTS (in order)
0. `kam_rulings_today.sh` + `reconcile_rulings.py`. Kam's rows today (all recorded): 09:37 80%-Spark; 09:57 KS-1402 = a; 10:22 KS-1256 = a; 12:03 UUID card = c; 13:15 freeze = a. **OPEN with a default: `secuura-headroom-before-90pct-stop-1006`** (filed 18:0x). Rec/default (a): Spark pipeline first. R 2nd merges #1395 + raises PRs 2-5, then one batched gate, then one deploy round (kintsugi, then demo, October grant). KS-1402 build waits for the renewal. The default fires when E 8th wraps.
1. `inbox_digest.sh --inbound` WHOLE (never through `tail`: at 19:1x the inbound view's tail cut off E 8th's STATUS, and only the `--all` read caught it) + `--all` for `[QUESTION]` rows in the last 12 h, each matched to a later ANSWER.
2. **develop = f556373b9418** (#1396 KS-1256, squashed by E 8th). VERIFIED AT SOURCE 19:15 by Wednesday's own scratch fetch: tree 1aa966ca162b, one parent f42161da3f96, 11 files, 0 trailers; KS-1256 In Progress.

## LIVE NOW (refreshed 21:5x, 70% checkpoint)
- **develop = d75bfe2deb80** (#1395 KS-1305, squashed by R 2nd). VERIFIED AT SOURCE 21:43 by Wednesday's own scratch fetch: tree c39aeeca92b9, one parent f556373b9418, 4 files; KS-1305 In Progress. **Today's merges: #1385, #1394, #1397, #1393, #1396, #1395.** All verified at source; none deployed yet.
- **Seat D 12th, the deploy seat** (pane `Secuura/Blockchain-D`, %67). **ITEM 0 answered and the subject-form GO SENT at 22:12** (`GO (Seat D 12th): deploy d75bfe2deb80 to kintsugi then demo`, verified 11:12:34Z). Kintsugi is at 46c3e20cfbd2 by content, migrations 0/0, KS-535 clean, rebuild set 30. **The disk forecast may cross the 4 GB guard:** a trip is a STOP; nothing is swapped and nothing pruned. Next from it: DEPLOYED kintsugi → sweep STATUS. Then demo's STOP 1-demo and STOP 2-demo (038a on live data), each needing an ANSWER. Report every deploy to Kam on the panel (box, SHA, rollback tag `pre-20261006`, sweep). **DISK, UPDATED 22:46: the guard is PRE-BUILD only and cannot bound originate (image 22, ~4.3 GB in-build). D 12th builds images 7-21, then makes a CONTROLLED STOP before originate by recorded pid (11:45:58Z ANSWER) unless the prune mail arrives. Image 21 is expected ~12:52Z (23:52 AEDT). At the stop: 21 built, nothing swapped, HOLD. Without the prune there is no kintsugi deploy today.** Earlier projection, superseded: the guard trips at ~image 16, ~23:20 AEDT (~550 MB/image, ~6.8 GB short). D 12th was told (11:3xZ ANSWER) to keep building and to STOP at a trip with everything held. **A prune happens ONLY on a separate Wednesday mail with the subject `ANSWER: D 12th build-cache prune allowed`**, sent after Kam taps (a) on `secuura-kintsugi-build-cache-prune-if-disk-guard-1006` (asked on his panel 22:34). Run `reconcile_rulings.py` first. If he has not tapped by the trip: re-plan without deleting anything (e.g. swap the built half first, then a second pass) and card it.
- **Seat R 3rd** (pane `Secuura/Blockchain-R`, %68). **ITEM 0 ANSWERED 22:28** (verified 11:28:32Z): proceed, no GO needed, nothing merges. Rulings: Q1 raisera1 with `--ready <run>/out.md --patch <run>/out.md.checker/patch.diff`; Q3 a required `--rec` (it defaulted to WRITING into B 65th's folder); Q2 accept NEITHER for `refs/seatra3/x`; commitra3.sh with required args. It runs the `s-ra1-ks1305` removal in its first lock window. Next from it: PR builds (STATUS mails ask for ctx reads) → ONE `READY FOR QA … -> gate71`. **On the READY:** commission a gate71 kit drafter (KS-1136 T1, the rest T2, batched), then merge seat(s) with subject-form GOs.
- R 2nd WRAPPED 0.95 (handover ac0d7ada); E 8th WRAPPED 1.0. Both panes closed.
- Ornith paused to 06:00 10-07 with its reason. The Spark queue is empty. Five newer holds (KS-1328, KS-1355 ×2, KS-1364 apigw, KS-593) wait for a raise seat after R 3rd.

## 🔴 STATE AT 01:1x 10-07 (night seat, ~74%) — newest; supersedes the 00:3x block below where they differ
- **KINTSUGI DONE:** deployed + swept clean at d75bfe2deb80 (D 12th, 0.96, wrapped, pane closed); reported to Kam on the panel.
- **D 13th (%70) LAUNCHED 14:12:08Z: DEMO deploy of d75bfe2deb80.** Brief `fleet/briefs_staged/2026-10-07_seatD13_demo_deploy.md` with Wednesday's Q1-Q8 rulings at the top. Next from it: the plan confirmation (= STOP 1-demo + ctx read). Answer with a pane reading, then send THE GO as its own mail with the exact subject `GO (Seat D 13th): deploy d75bfe2deb80 to demo`. **STOP 2-demo (038a on live data) is answered by Wednesday after reading the SQL + the measured tables: no pre-release (Q6).** Q3 (ADMIN_USER_PASSWORD could suspend admin@secuura.com) → card Kam if it fires. Q4 (GATEWAY_VOUCH_SECRET absent) → card Kam as residue after the deploy. **Hold #1383 until D 13th's DEPLOYED (Q8).**
- **R 4th (%69):** row 06 GO'd at ctx 35% (14:11:08Z); next: its ticket filing, then build → ctx-read request before the push.

## 🔴 STATE AT 00:3x 10-07 (night seat, 65% checkpoint) — read this before the plan block below
- **D 12th (%67): kintsugi SWAP RELEASED 13:28:51Z** at ctx 61% (Wednesday's pane read), 28 services, api-gateway behind the two-DB pending gate. Next from it: the sweep, then GATE 2 mail "kintsugi swept — need a ctx read for the demo decision". Answer it with a PANE READING (`tmux capture-pane -t %67`). Demo only < 55%, else D 13th takes demo from its handover. Then relay the deploy to Kam on the panel (box, SHA d75bfe2deb80, rollback `:pre-20261006`, sweep).
- **R 4th (%69) LAUNCHED 13:33:44Z**: job-06 fix FIRST (Spark pass HELD: `local-model/night/READY_KS-1136-06-TENANT-STDERR-OWN-FILE-1_spark-dsv4flash_…`), then PRs 3-5, ONE READY → gate71. Next from it: ITEM 0 plan confirmation (answer it; its proposed ticket text is for the ANSWER), then ctx-read requests at each budget line.
- **gate71 kit:** NOT launched. On R 4th's READY, re-pin and WIDEN the kit to the batch (GO_WANT → R 5th; the doc-order check → unique + keyed, not ascending; add row 06's shapes), then launch. Merge order: 06 PR → #1398 → 3-5, each on a subject-form GO to R 5th.

## 🔴 GATE71 PLAN (night seat, 10-07 00:1x)
- **#1398 (KS-1136) RAISED by R 3rd (wrapped 0.96).** gate71 KIT BUILT and RULED (`fleet/qa-agent/gatesets/2026-10-06_gate71/`, `RULINGS_wednesday.md` "RULED by Wednesday" block; routing line ADDED). **Gate NOT launched, deliberately.**
- **Why:** Q2: job 06 writes its runner's stderr into its JSON artefact (`Testing/jobs/06-tenant-isolation.sh:~71`, `2>&1`). After #1398 merges, every routine verifier→holder fallback run reads HIGH with a false cause. **#1398 does not merge until that 06 fix lands FIRST.** One batched gate71 then covers both PRs (Kam's 09-18 minimise-duplication rule), at 90% usage.
- **Route:** the 06 fix goes to the SPARK (Kam 19:30: "Spark on all tickets"). A brief drafter is running, writing the report to `0_Brain/reference/2026-10-07_spark-screen/BRIEF_06_STDERR.md` and queueing only on a passing dry-run + control. Next: read the brief whole, run the Spark queue, review + hold_ready. Then **R 4th** (staged brief NOT yet written) files or locates the ticket, raises the 06 fix + PRs 3-5 (KS-998, KS-1313 + KS 1326, KS-1164) from R 3rd's handover, and sends ONE READY. Gate71 is re-pinned and widened to the batch. Merge order: 06 fix → #1398 → 3-5.
- Usage 90% at 00:1x: launches pass `WED_USAGE_STOP=100` naming the EXPIRING-GRANTS 100% row; card (a) shape only.

## THE QUEUE, in order
1. D 12th deploy (LIVE) and R 3rd raises (drafting): see LIVE NOW.
2. One batched gate for R 2nd's raised PRs (name the gate number in the ANSWER; it is NOT gate69).
3. Deploy round: today's merges (#1385 KS-938, #1394 KS-723, #1397 KS-1425, #1393 KS-1278, #1396 KS-1256, then #1395) to kintsugi, then demo, under the October grant (EXPIRING-GRANTS). Phase 0 re-tag; KS-535 wallet rule; report each deploy on the panel.
4. Five newer Spark holds for a later raise seat (READY_ files in `local-model/night/`): KS-1328, KS-1355 stack_guard, KS-1355 dev-reload (r2, held 18:0x), KS-1364 apigw, KS-593.
5. After the renewal (~Sun 11 Oct): KS-1402 build (`fleet/briefs_staged/2026-10-06_seatK1402_build.md`, not yet read whole); B 69th residue (B 68th handover 053278f0); #1383 F 5th rebuild.
6. Spark queue empty; a brief drafter runs only if the gauge is under 87% after R 2nd launches.

## BUDGET
7d gauge 86% (20:1x); Kam 19:30 grant lifts this seat to 100% until the renewal, renews ~4d 17h. 90% = hard stop. Since 09:37: Claude launches 10 vs Spark tasks 14 (58% Spark), told to Kam 18:0x.

## OWED (Wednesday's own)
- **`safe_pull.sh` BUILT 23:0x (night seat)** — pull the WEDNESDAY repo with `bash 2_Project_Files/tools/safe_pull.sh` (commit your own files by pathspec first); a hand-typed `--autostash` is now REFUSED by the `pretooluse_no_autostash` hook. **Still owed:** `safe_push.sh:108` and `wed_claim.sh:54` run `rebase --autostash` internally (shared with Tuesday/Friday; `safe_pull` is not a drop-in for wed_claim, which pulls on an arbitrary dirty tree). Until fixed, after either tool runs, read `git stash list` for a new autostash.
- Kam 19:30 grant: this seat may spend to 100% until the renewal, shaped as card (a), with one or two deployers. **Deploy round:** brief STAGED `fleet/briefs_staged/2026-10-06_seatDeploy1_kintsugi_demo.md` (Seat D 12th; dry-run gate PASS; NOT yet read whole). Launch after #1395 merges: read it WHOLE, re-pin develop, then `brief_and_launch.sh --to "Secuura/Blockchain-D"`, clause cloud: deploy. Demo is a ~600-commit jump from 0f8fb33c3 (09-10) with migration 038a, a 039 RLS change, and two new env vars. **Before sending, grep it for completeness claims about tools ('nothing else', 'only', 'the two calls') and, for each, grep the named tool for foreign-lane literals with a count (ledger 10-06 w=4).** Rule the drafter's Q-DISK / Q-DEMO-STOP / Q-PETER-MERGES / Q-1383 / Q-SWEEP-DEMO at its ITEM 0. Recommendations are in the note's 19:4x line.

## OWED (board-pass list, unfiled)
- namecheck's +8 subject gate refuses 85-92 char subjects.
- history.md's stale D 10th handover sha (921960… vs the file's f2a0a893).
- BACKLOG.md lacks the CI findings.
- The 6 shell suites red on CI, green in-hook.
- 11 overlapping lockfile PRs.
- `dev-reload.sh:73` UTF-8 unbound variable.
- KS-729 past due.
- Signatory routes' org-membership check.
- `--no-optional-locks` stale-stat blindness.
- **Leg-6 CLEANUP advisory: 15 stale baseline rows (12 KS-470, 3 KS-559), from E 8th.**
- **E 8th's finding: a `git for-each-ref` `*` does not cross `/`. STANDING_LINES candidate.**
- Orphan watchers 12127, 31713, 41307, 89913: the lanes stop their own.
- KS-1422 stale origin/develop. Ledger w=3: a mechanism for "ruling on a seat's tool unread".

## STANDING NOTES
- Pathspec-only commits; after any pull, inspect a new autostash; decisions.json and the chat stores are STATE.
- Receipts quoting a send's output are written AFTER the output is visible.
- Close a gate's pane on reading its verdict. Quoted heredocs only.
- **Before any GO, open the brief's GO section and copy its required shape.**
- Ornith PAUSE_QUEUE renewed to 06:00 10-07 with its reason.

## WITH KAM
Card `secuura-kintsugi-build-cache-prune-if-disk-guard-1006` **RULED a 23:05:25; release SENT 12:07:01Z** (`ANSWER: D 12th build-cache prune allowed`): at the controlled stop before originate, `docker builder prune -f` ONCE, resume only at ≥ 8,600 MB free, else HOLD and card Kam (no `-a` without his word). Expect D 12th's before/after figures ~12:50Z; relay them to Kam. He was also told about the kintsugi Redis requirepass leaked into a local file (scrubbed); rotation is his call. The headroom card was RULED a at 19:30:00; his 19:30:43 grant lifts this seat to 100% (EXPIRING-GRANTS).
