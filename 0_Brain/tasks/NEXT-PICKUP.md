---
date: 2026-09-19
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's. Datasec mail by subject only.
source: replaced WHOLESALE at 10:5x 2026-09-19 by the 10:2x Saturday seat (previous copy NEXT-PICKUP.md.pre-0919-1050; the 09-18 blocks are in NEXT-PICKUP-archive.md).
status: live
supersede: replace wholesale at the next pickup; do not append
---

# NEXT PICKUP

## ONE block (the 10:2x Saturday seat) — replace it, never append

**Kam is AWAY Sat 19 + Sun 20.** `tasks/WEEK-INSTRUCTION.md` is LIVE to the end of Sun 2026-09-20: merge on Wednesday's signed GO after a QA gate (Secuura CLAUDE.md merge section: "Wednesday's GO, naming the head SHA, is the approval"); deploy KINTSUGI ONLY; NOT demo; the signature classes still pause (KS-1250, KS-1175; money; external comms beyond rule-7); auth last. He leaves again MONDAY NIGHT 2026-09-21. `fleet/USAGE_STOP` = 90; gauge 51% at 10:23. `local-model/night/ALLOW_SEATS` is armed to Sun 2026-09-20 23:00 (epoch 1789909200).

### FLOOR at 18:0x (🔄 ROTATION HANDOVER from the 10:2x seat, ctx ~80%)
`%0` wednesday · `%115` **Seat B 5th** HOLDING for the GO (READY 07:48:28Z: #1077-#1083, all test-only, all-seven tree 993718b84 over f9c28a8b8; receipted 07:5x) · `%116` **QA gate #1077-#1083** RUNNING, launched ~18:04 (launcher `fleet/qa-agent/launchers/launch_qa_secuura_batch1077_1083.sh`, prompt `fleet/qa-agent/briefs/2026-09-19_secuura-batch1077-1083.prompt.txt`, gateset `fleet/qa-agent/gatesets/2026-09-19_gate1077to1083/`, report `Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1077-1083-tier1-r1/`). Re-pinned by Wednesday at 08:04:32Z: develop f9c28a8b8 and #1083 head 5f3280e9c = the READY; `--check` rc 0; usage 62%. Rung 5: the pane lists its own report dir. · `%1` monitor. **Your wake = the gate's verdict mail** → completion check → ONE signed GO (the #1070 GO mail is the template: `2026-09-19_seatB-4th/mail/in-GO-052812.json` in the Secuura history, or today's note ~15:28) → merges → verify develop's tree at source → score the seat + gate → close panes after wraps. **KS-1238 goes Done + archived ONLY if the gate rules COMPLETE by name.** No kintsugi deploy after (test-only).

### 🔴 FIRST ACTS for whoever holds this seat next
1. `kam_rulings_today.sh` + `reconcile_rulings.py` (0 panel lines today). **Every wake turn starts with `python3 2_Project_Files/fleet/ornith_status.py`.**
2. **Seat B 5th READY ARRIVED 07:48:28Z (pass): #1077-#1083**, all-seven tree 993718b84 over f9c28a8b8, all test-only; RECEIPTED 07:5x (ANSWER + tap: no GO yet, #1083 tier 1). **A gate DRAFTER is running** (→ `fleet/qa-agent/gatesets/2026-09-19_gate1077to1083/`, prompt `briefs/2026-09-19_secuura-batch1077-1083.prompt.txt`, launcher `launchers/launch_qa_secuura_batch1077_1083.sh`). When it reports: re-pin + `--check` + usage → `cockpit.sh add "QA/Secuura-1077" <launcher>` → rung 5. The rest of this item still applies: receipt it (ANSWER + a `cockpit.sh say … --mail` pointer), then commission ONE batch-gate drafter in the #1070 shape (model `fleet/qa-agent/gatesets/2026-09-19_gate1070to1076/` + its generator; the drafter prompt is in today's note ~14:32). Tier 1 = the KS-1238 N76-1 PR, tier 2 the rest. Put **KS-1238 by NAME** to the gate: is (v) pinned, and is the ask complete ((i)/(ii)/(iv) pinned, (iii) closeable)? Done + archived ONLY on that; else Backlog. Re-pin by `ls-remote` + `--check` IMMEDIATELY before launch; confirm rung 5 by a phrase only the gate writes. Then: verdict → completion check → ONE signed GO naming each head in the gate's order → merges → verify develop's tree at source → score → close panes after wraps. **No kintsugi deploy after this batch** (test-only; no running image changes).
3. **Ornith:** queue empty with a reason; the next feed = that gate's NOT-PINNED list (brief via a subagent in the round-13 shape; every briefable row goes through `night/briefs/`; never brief-less). **Held for the batch AFTER Seat B 5th's: 1** — `READY_KS-1269-N71-1` (the null index; the first run on today's runner pin).
4. **Ornith WIDENING owed (the next harness job, if the pool is dry again):** the test_only builder takes ONE-LINE tampers only, so the #1070-1076 gate's two /revoke guard-ORDERING rows (the guard moved below the 404, or below the KS-440 reason check: 4-line block moves) are unbriefable. Extend the tamper format to a multi-line `From:`/`To:` block (a subagent, arms with the old builder as the negative; the runner-pin job's shape). The KS-1101 N3SKIPPED row is a test-file tamper → a Claude seat, not the model.
5. Harness fixed today: `tasks/test_only/checker.sh` (restores a previous run's modified test file) and `tasks/test_only/build_test_only_input.sh` (runner pin; arms `local-model/tests/test_only_runner_pin_arms.sh` 6/6). Both have IMPROVEMENTS rows.

### Reallocated to a Claude seat (Kam's 09-16 counter; do NOT queue at the local model)
KS-1168, KS-1163, KS-998, KS-866 (from 09-16/17) · **the KS-871 remnant** (round 9): `services/api-gateway/src/middleware/audit.ts:333` still logs `path: req.path` on a failed audit write (on a refused erasure that is the trimmed `/`); KS-871 is In Progress, so the builder refuses it → a line for whichever seat next takes KS-871.

### HOLDS
KS-1250, KS-1175 Kam's · nothing to demo · no contact with Peter/Stuart beyond rule-7 facts · auth last · never delete · Tuesday owns Datasec.

### ROUTE TO KAM (Monday 21) — one list
1. Peter's two KS-1195 questions (per-key rateLimit for S connector keys; KS-1206 "429 forever"; PS-928 Stuart Urgent) — unanswered by design.
2. Peter's KS-593 addition: fuzzed wallet authenticate/verify → 500 where 400 belongs.
3. Kintsugi has NO connector allow-list configured (measured by seat A 12th).
4. Kintsugi disk: 27 G free after seat A 13th's deploy; budget the TRANSIENT per-service build cost (~3.8 G seen), not the image size.
5. KS-1262 (High) test-token severity check: unowned.
6. The drive sync keeps making `(conflict_on_…)` copies (27 untracked in WEDNESDAY; they make panel_sync SKIP its rebase every cycle), 9 in the vault; not removed.
7. From 09-18: seat A's launcher F-02 (no keychain SSH identity), the open card `wed-boot-read-exceeds-the-context-window`, O-1 (CI jobs never start), the NSG's dynamic IP.
8. report-796 F-01/F-03 (`scripts/audit/*.mjs`): open at the tip; F-01 needs a new env seam and F-03 contradicts the code's own SKIP comment → a ruling, not a local-model ticket.
9. KS-1269-U: should `/unrevoke` refuse `index < 0`? KS-662 lists `/unrevoke {index:-1} → 200` as NON-RULED; the held fix leaves it unchanged.
11. Ruleset 18499832 (develop) carries `require_extra_approval_for_unattributed_changes: true` — seen by Seat B 5th 2026-09-19; it blocked nothing; whether it is new is unmeasured.
10. **Wednesday's reading to confirm:** with the non-auth pool exhausted (rounds 8-9), round 10 opened AUTH surfaces to TEST-ONLY local-model work (tamper-pinned cells, zero product bytes changed), on the recorded rule 'auth product EDITS stay out'. Default: it continues unless he says auth means tests too.

### OWED (tooling, mine, none urgent)
`brief_and_launch.sh` prints "launched" after cockpit SKIPS a same-name pane (false receipt; ledger 09-19) — needs `--pane-name` + rc 1 on skip · `cockpit.sh say %<id>` fails silently (use the NAME form) · `inbox_digest.sh` shows Datasec previews in the wednesday-agent@ section · a wake-turn Ornith print · `note_entry.sh` warn on a typed clock later than its stamp · a UTC-bound helper for commissions (ledger 09-19, the one-day-late cutoff).
