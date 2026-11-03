---
date: 2026-11-03
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Mac mini).
status: live
supersede: REPLACED WHOLESALE 13:45 AEDT 2026-11-03 by the 13:3x rotation-successor seat. Previous kept as NEXT-PICKUP.md.pre-1103-1345 (its 11:2x / 10:24 / 09:41 blocks are history). Replace wholesale; never stack.
---

# NEXT PICKUP — Tue 3 Nov 2026, 13:45 AEDT (13:3x successor seat, ctx 56%)

## 🔴 FIRST WORK, in order
0. **Seat S 15th (Opus fix seat: KS-1961 api-gateway fail-closed, then KS-1962 anchor-trust fail-closed; Kam cards 1970 = a 10:57:31, 1976 = a 11:18:59).** Brief `2_Project_Files/fleet/briefs_staged/2026-11-03_seatS15_failclosed_ks1961_ks1962.md` (read WHOLE, edited, SELF-CHECK 13:42, dry run rc 0). Launches by WAITER `s15_waiter.sh` pid 17920 (ppid 1) in THIS session's scratchpad `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4ec9c7d5-cdda-43d5-80ba-6e7d6ebf97a4/scratchpad/` (log `s15_waiter.log`) at the first ROOM. If the waiter is dead and no S pane exists: re-arm from the same brief (capacity line read first). Its plan confirmation is DESIGN-FIRST with 5 questions (malformed rateLimit; Redis-not-connected fallback; KS-616 degrade stays; registry missing-table case; 503 contract). Answer them; then gate 168/169 = Opus T1 per PR. When briefed + building: `decision_queue.sh rule ... --delivered` on cards secuura-pr1970-gateway-failopen-1103 and secuura-pr1976-anchor-trust-failopen-1103 naming the brief.
1. **Merge lane B is EMPTY** (B 83rd wrapped 13:42, scored 0.94, pane %105 closed). **Seat B 84th brief** is being drafted (Sonnet subagent of THIS seat; output `2_Project_Files/fleet/briefs_staged/2026-11-03_seatB84_merge_queue.md`). If missing after rotation, re-commission from B 83rd's brief + `.../5_Project_History/2026-11-03_seatB-83rd/HANDOVER.md`. Read whole, dry run, CAPACITY, waiter. Its queue starts EMPTY; QUEUE each PR only after its gate. GO subject: `GO: merge PR <n> at <head12> on develop <pin12> (Seat B 84th)`. Pre-GO every time: no un-MERGED GO, `gate_stray_check.sh` rc 0, `push_queue.sh list`, ls-remote both pins, READ THE READY WHOLE (Read tool, never `cut`).
2. **PR 1982 (E 30th %103, KS-915 restore-local-secrets.sh for Peter):** round-2 fixes committed 0a984b64, develop merged in 87c9e748, suite 137/0, mutants 22/22; forward push driver pid 1334 queued behind F 26th. At its READY FOR GATE round 2: **GATE 166 = Opus T1 DELTA** on G165-F1..F6, F9, F11 + the 33 forms that held (round 2 of 2 = the cap: a NO GO ships nothing and goes to Kam as a card). Brief the gate with `2_Project_Files/fleet/qa-agent/gate_common.md` pasted whole + the specific part; **name the one round-1 control the F2 ruling flips: `postgres:///x?host=/tmp` is now REFUSED by design.** Gate 165's verdict: `0_Brain/reference/2026-11-03_gate165-ks915-pr1982/verdict.md`. When 1982 MERGES: tell Kam on the panel Peter's script landed (he holds the WhatsApp line bf-30443c2ca7a6; he was told 13:2x "not yet").
3. **Seat F 26th %106 (Opus, KS-1572 /referrals/apply referee = token caller):** built on 1e6df0b6, commit 68897dda, push driver pid 45177 in the hook (02:34Z). At its READY: **GATE 167 = Opus T1** (cells: other id 403 / no principal 403 / platform role for another id 403 / upper-case id 403 / padded id 400 / own id 201 with no ip/device / wallet failure 500; 0 applyCode calls on refusal; blank fraud-log ip as a stated consequence). Candidate it named (not filed): referral pool-error test control C1 timed out 2/7 at load 8-12 (= G153-F8).
4. **R lane EMPTY:** a raise seat (Sonnet) owed for held passes O91 x11, O92 x10 (P3/P9 unblocked: 1980 merged), O93/O94 holds, + R 78th's open ITEM 4a-c (its HANDOVER). After S 15th and B 84th, at ROOM.
5. **Spark:** operator 94's detached loops (loop94.sh pid 13858, holdloop94.sh pid 13859, ppid 1) bounded ~14:12; a background waiter of THIS seat fires on 13858's exit. Then re-commission an operator from operator 92/93/94's records (workdir `0_Brain/reference/2026-11-03_spark-operator94/`; never grep -r runs/ night/). Round LIVE, queue 4-6 at 13:4x.

## KAM
- Cards OPEN (3, Secuura): `secuura-auth-lockout-failopen-redis-down-1103` (default a ~15:40: a seat files the ticket + queues the fail-closed fix AFTER KS-1961/1962 → add to S 15th's queue by ANSWER); `secuura-hibp-breach-check-never-runs-1103` (24 h: ticket, nothing built); `secuura-pr1979-ambassador-bonus-starts-paying-1103` (nothing merges). KS-1966 (gateway rotated:true) fail-closed remedy = REVISITING a Peter-reviewed design (KS-1152 R-880-1): bring to Kam with the other fail-closed rulings, not yet carded.
- Kam silent since 11:17:59. Panel status posted 13:3x (bf-15a14259a5b8).

## TODAY'S MERGES (Wednesday GOs, this afternoon chain): 1972-1977, 1970, 1980, 1978, 1981 = 10. develop 27fe5476526c (ls-remote 13:41:16). PR 1968 HELD. PR 1979 on Kam's card.

## RULES IN FORCE (today's ledger)
- Seat launch = its own call AFTER reading the dry run's CAPACITY line; FULL -> waiter, its armed line read in the next call.
- Never grep -r / find over the WEDNESDAY tree or local-model runs/ night/; a call auto-backgrounded at timeout is stopped or justified the same turn.
- Read every READY / mail body untruncated (Read tool or full sed), never through `cut`.
- A note is its own tool call, after the act's output is on screen; quote the act's own success line.
- No credential in argv (WED-155): headers via `curl -H @file` (0600, blanked after).

## OWED (not first-work)
- WED-155 (inbox_digest.sh lines 57/69 pass the AgentMail key in argv). gate_common.md now TRACKED at `2_Project_Files/fleet/qa-agent/gate_common.md` (claim OPEN in WED-OWNERSHIP: release after gate 166 uses it). board_count BOARD_COUNT_ZERO_OK accepts a refused control line (shared tooling, claim first). INDEX.md refresh. Ticket candidates for a board seat: G139-F1, G145-F3, G146-F2, G149-F4/F5, G154-F1, pool-listener C1 timeout. Regenerate BOTH digests at wrap if learnings/ changed.
