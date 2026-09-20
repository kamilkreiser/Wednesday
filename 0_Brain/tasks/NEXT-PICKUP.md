---
date: 2026-09-20
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's. Datasec mail by subject only.
source: replaced WHOLESALE at 21:54 2026-09-20 by the 21:2x seat (previous copy NEXT-PICKUP.md.pre-0920-2210; older blocks in NEXT-PICKUP-archive.md).
status: live
supersede: replace wholesale at the next pickup; do not append
---

# NEXT PICKUP

## ONE block (the 21:2x Sunday seat) — replace it, never append

**Kam is HERE, on the panel, and signed this seat into a NEW ACCOUNT at ~21:5x — statusline `7d:0% renews 6d 14h`.** His words, verbatim, after `/login`: *"keep going and once you fix the launch screen, keep going with secuura tickets using both claude and local agents"*. Receipted with Wednesday's reading (fresh allowance; Claude seats raise/gate/merge while Ornith works the backlog; merges one at a time on Wednesday's signed GO under the open-ended TESTED grant; kintsugi only, never demo; signature classes pause — KS-1250 still his; the away-week's 23:00 merge cut-off read as NOT applying now he is here). Not corrected as of 21:54. **The 90% cut is not in force on this account** — `usage_gate.sh` reads the gauge and opens by itself. Same shape as `learnings/2026-09-16_new-account-spin-up-agents-to-test-approve-merge.md` (extend that file, do not write a new one — Kam ruled `b` on the digest at 16:44: shrink the corpus).

WEEK-INSTRUCTION.md is live only to END of today; **on Mon 21 set `status: lapsed`** and bring Kam the Monday list (unchanged, below). Ledger rule 3c: rows dated 09-17 pass the 3-day line on 09-21.

### THE LAUNCH SEQUENCE — DONE (Kam's ask, 21:3x)
Analysis: `0_Brain/reference/2026-09-20_cockpit-launch-sequence/README.md` (FOUND/TESTED/HOW). Two fixes shipped with arms, both pushed, HEAD == origin:
- **D2** doctor's root check was blind to a conflict copy of the launcher (allow-list `Launch_*.command` matched it) and to directories (`[ -f ]` skipped them). Fixed; directories keyed on gitignore (a recorded decision), conflict copies tested first. Arms `2_Project_Files/tests/doctor_root_check_arms.sh` 10/10 incl. two negative controls. Commit a4433df73. The copy is quarantined at `5_Project_History/_quarantine_2026-09-20/` (gitignored by design).
- **D1** `cockpit.sh up` created pane 0 (this seat) with `new-session` directly, bypassing add_pane's rebase/merge gate while `panel_sync.sh loop` (pid 1775) rebases this repo every minute. Hoisted into `wait_tree_settled`; pane 0 waits, deliberately NOT usage-gated (reason in the code). Arms `2_Project_Files/fleet/tests/cockpit_pane0_rebase_gate_arms.sh` 5/5 incl. the negative control on the pre-fix script. Commit 1d8ce6321. **NOT yet exercised by a real boot** — the next `up` (a rotation or a Fresh) is the first live run; read `logs/rotate_wednesday.log` after it.
- Remaining from that read, unfixed: 17 conflict copies of mechanism scripts under `2_Project_Files` (none invoked by name — quarantine as a sweep only with each checked, never blind); `add_pane` skip returns 0 and `brief_and_launch` prints `launched:` on it; `cockpit.sh say --mail` silent rc 1 on an unrouted pane name; the Fresh branch kills live agent panes.

### 🔴 IN FLIGHT AT 22:27 — two Claude seats LIVE, one drafter running, one READY banked. If this seat is gone, the mails and files below are the handover:
1. **Seat B 10th `%6`** (launched 22:10, brief verified 12:10:16Z). Plan confirmation received 12:24Z and ANSWERED 12:26Z (`fleet/briefs_staged/2026-09-20_seatB10_answer_plan.md`, tapped, prompt clear): confirmed; Q2 originate census = REPORT on the baseline leg, STOP on :5432 / non-loopback ESTABLISHED; Q3 PR 1 tier 2, **PR 2 tier 1** (allow-list surface); **PR 3 ADDED = KS-1272** (the Ornith PASS held 22:1x — one product line at `startup-migrations.ts:1077`, `:473` untouched, strict apply, `Refs KS-1272`, pushed LAST; the product-byte STOP narrowed to "exactly 1/1 on that file"). Expect THREE `READY FOR QA (Seat B 10th)` mails → ONE batch gate at tier 1 → completion check → signed GO naming each head → merges one at a time.
2. **Seat A 15th `%7`** (launched 22:12, brief verified 12:12:10Z, `fleet/briefs_staged/2026-09-20_ks1175_fix_seatA.md`). KS-1175 REAL fix to a gated PR then STOP; four DECIDE points come in its plan confirmation (defaults: 400 on malformed; 400 on commitment mismatch; flat under `secuura`; the CSL 64-byte chunker IN this PR). Plan confirmation received 12:27Z and ANSWERED 12:2xZ (`fleet/briefs_staged/2026-09-20_seatA15_answer_plan.md`, tapped, prompt clear): DECIDE 1–4 ruled as the defaults; F1 = request-side spec only (the two GET paths are KS-723's, NOT DONE named); POST /verify NOT DONE; dechunk before the hash compare; the 64-byte defect is filed as **KS-1284** (Backlog P2, `Refs KS-721`, verified at source 12:3xZ; STATUS 1 ACKed). Seat A is on the red cells. Baseline 241/242 (1 pre-existing red, threadTokenMint, BACKLOG.md:155). Card `secuura-ks721-commitment-cannot-reach-a-real-chain` (default a) carries the finding to Kam.
3. **Ornith**: KS-1272 PASSED 7/7 at 22:15 and is HELD (`night/READY_KS-1272_…PASS-7of7_2026-09-20.diff.md`). Queue EMPTY; `night/PAUSE_QUEUE` reason = a drafter is writing the NEXT brief (picks the first T1 candidate disjoint from the three lanes, non-auth, in-process cell), expiry 23:02. **When the drafter returns: read its report, source-check the brief's one edit against the file at the tip, append its queue line, kick `launchctl kickstart gui/501/com.wednesday.ornith-loop`, arm a `run_in_background` waiter on `done.md` — ONE action.** If it has not returned by 23:02, write a new reason; never queue brief-less. `ALLOW_SEATS` re-armed to Mon 06:00 on Kam's 21:5x words.
Tip for all three: develop `dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa` (unmoved at 12:24Z per Seat B). Kam's last panel words: 21:5x (the new-account instruction). ctx at this refresh: 66%.

### AFTER THE SEATS ARE UP
- Each READY FOR QA → a QA gate (batch by file-disjointness per the 2026-09-18 minimise-duplication rule; tier by surface) → Wednesday's completion check → signed GO naming the head → the seat merges one at a time → develop re-read at source after each.
- Kam's 15:25 standing words still bind: *"close, archive merge and deploy anything that's ready. then continue with both claude and local agents"*. Deploy = KINTSUGI only.
- Boot digest: this session EXTENDS a learnings file (the new-account grant) → at wrap regenerate BOTH digests (`boot_digest.py --by-tier` AND bare) and commit.

### ⚠ HARNESS RULES LEARNED 2026-09-20 — dropped from this file at the 21:54 wholesale replace (my loss, found by the KS-1234 drafter); they live VERBATIM in `NEXT-PICKUP.md.pre-0920-2210` :61 and in the archive. Two more from tonight: a blank trailing-context line needs `ALLOW_BLANK_CONTEXT=1` at build (else REFUSED rc 2); and the checker's A6 never runs `packages/shared` — an extra blank `+` line PASSES the checker and reddens `ks781-p3-3` (the KS-953 class), so every api-gateway `index.ts` raise carries `git apply --numstat` = `1 1` AND a `packages/shared` run in its READY.

### OWED (mine, none blocking)
`doctor.sh` warns on a `PAUSE_QUEUE` epoch in the past (the 21:15 row's leg — it bit AGAIN at this boot, 83 min expired) · `reconcile_rulings.py` must recognise Kam's `note:` form or print UNPARSEABLE loudly (his 19:41/19:42 rulings reached no card mechanically) · `cockpit.sh say` prints WHY it refuses · `brief_and_launch.sh` treats a skip as rc 1 · `inbox_digest.sh` Datasec previews (fixed 06:4x, verify) · `note_entry.sh` typed-clock warn · `night_run.sh` refusal on task_type/task mismatch · the family-weight index.

### ROUTE TO KAM (Monday 21) — unchanged from the 16:0x seat's list
1. Two cards he ruled at 16:41 with `tuesday-` ids: one is FLEET-scoped (boot digest → `b`, being applied by this seat's discipline) and one is WED (`mini-vault` → `a`). **Ask whether his 2026-09-14 07:22 suspension of Wednesday→Tuesday messaging still stands** — Tuesday is live and mailed this seat tonight (a shared-tool change, DKIM pass).
2. `Secuura/platform-s#877` is unreadable to us — a permissions boundary, reported not worked around.
3. Four escalations turning on absent §5f runtime evidence: KS-577, KS-946, KS-1172, KS-1173.
4. `secuura-dependabot-triage` says "close the 5"; there are 10 open dependabot PRs now.
5. The rotation liveness guard: check `logs/rotate_wednesday.log` after the NEXT rotation for a verdict line.
6. Carried: Peter's two KS-1195 questions; his KS-593 addition; kintsugi has no connector allow-list; kintsugi disk 25 G free; KS-1262 severity unowned; the drive sync keeps making `(conflict_on_…)` copies (17 of them are mechanism scripts); seat A's launcher F-02; O-1 CI jobs never start; the NSG's dynamic IP; report-796 F-01/F-03; KS-1269-U/N84-1; ruleset 18499832's flag; audit-baseline.json fuse expires 2026-09-24; **O-1: `admin.ts` `requireAdmin` routes do no session check**; KS-1282 completeness; the KS-1283 coverage ticket (six NOT-PINNED role-dimension rows; `register-connector` mints a key).
7. Wednesday's reading to confirm: auth surfaces open to TEST-ONLY local-model work under "auth product EDITS stay out".
