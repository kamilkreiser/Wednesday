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

### 🔴 IN FLIGHT AT 22:49 (70% checkpoint) — two Claude seats LIVE, Ornith RUNNING, one READY banked. If this seat is gone, the mails and files below are the handover:
1. **Seat B 10th `%6`** — plan ANSWERED 12:26Z; STATUS 12:46Z: all THREE raised + committed (ks1275 `f5a599b07`, ks1203 `47593b77b`, ks1272 `9b668edba`), batch tree `d0c8bfd095b6` green (api-gateway 678/678, originate 807/807, tsc 0 ×2), census STOP-class 0; ACKed 12:47Z (`fleet/briefs_staged/2026-09-20_seatB10_ack_status.md`): findings 1 (checker graded an 86-line KS-1272 variant; the canonical 85 is raised — TELL THE GATE) and 2 (UNTYPEDGETSADEFAULT already reds `enforcement.test.ts:148` at develop; PR 2's spellings half is the new coverage — the "reds == declared ∪ measured cover" predicate is the lane's rule) are NOT STOPs. **Now in its push series PR1→PR2→PR3. Expect THREE `READY FOR QA (Seat B 10th)` mails → ONE batch gate, TIER 1 (PR 2 is an allow-list surface) → completion check → signed GO naming each head → merges one at a time, develop re-read after each.** Nothing merges without the GO.
2. **Seat A 15th `%7`** — plan ANSWERED 12:30Z (DECIDE 1–4 as defaults; spec request-side only, the two GET paths are KS-723's; POST /verify NOT DONE; dechunk before the hash compare). STATUS 1 12:32Z: **KS-1284 filed** (Backlog P2, `Refs KS-721`, verified at source) — ACKed. On the red cells R1–R9. Expect ONE `READY FOR QA` → TIER 1 gate → completion check → GO → the seat merges; **no deploy, no anchor — that step is Kam's** (card `secuura-ks721-commitment-cannot-reach-a-real-chain`, default a, names KS-1284 now).
3. **Ornith** — KS-1272 HELD (raised by Seat B as PR 3). **KS-1234 RUNNING** (queued 22:39; G4 load refused once at 20.2, cleared at 9.0; runner `pid 2618` from 22:47); brief `night/briefs/KS-1234.md`; a waiter is armed keyed on `input=…/code_1234.json` + `done 2026-09-20` — **NOT on the ticket id: KS-1234 has a stale 2026-09-18 FAIL row in done.md** (ledger row 22:48). On PASS: source-read (one product line at `index.ts:413`; numstat MUST be `1 1`; a `packages/shared` ks781 run is owed at raise — the checker's A6 does not run it), write the READY, commission the next brief in the same action. On FAIL: classify (model/harness/brief), ONE rebrief max (Kam's counter), then Claude. `ALLOW_SEATS` to Mon 06:00.
Tip for all three: develop `dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa` (unmoved at 12:46Z). Kam's last words: 21:5x terminal (new-account instruction); panel quiet since — panel_sync alive (pid 1775), streams advancing, not stale. ctx at this refresh: 70%. Rotation band 80–90; at the band, rotate at a safe boundary with the seats running (2026-09-13 rule) — the successor answers the READYs.

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
