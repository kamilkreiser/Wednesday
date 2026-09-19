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

### FLOOR at 15:5x
`%0` wednesday · `%114` **seat A 14th** (pane `Secuura/Blockchain`), launched 15:41: a SCOPED kintsugi deploy 3c447abc7 → develop **f9c28a8b8** (#1061-#1076 merged today, both batches verified at source: develop tree bc4d0ed7f). Brief `fleet/briefs_staged/2026-09-19_raise_seat_A_successor14.md`. Its plan confirmation is due (a QUESTION mail). · `%1` monitor. Seat B 3rd and 4th both wrapped and scored 1.00; gates #1061-1069 and #1070-1076 scored 1.00; all panes closed. KS-1276 Done + archived; KS-1279 + KS-1280 filed today.

### 🔴 FIRST ACTS for whoever holds this seat next
1. `kam_rulings_today.sh` + `reconcile_rulings.py` (0 panel lines today as of 15:5x). **Every wake turn starts with `python3 2_Project_Files/fleet/ornith_status.py`** (ledger 09-19 w=10).
2. **Seat A 14th's plan confirmation:** rule api-gateway IN or OUT (the default is IN: its image bakes 7 changed test files, and nothing it RUNS changes); check the measured service set (expected originate + vc-issuer), the disk numbers against the transient budget (27 G free, originate dip ~3.8 G, 4000 MB guard), and that V1/V2 are no-write. Then receipt its STATUS mails; on DEPLOY COMPLETE, a completion check against the brief, then accept, rule-7 and wrap; verify the wrap at source, score it, close the pane.
3. **Ornith:** round 13 (the #1070-1076 gate's NOT-PINNED; -1 on /unrevoke deliberately NOT pinned) is running as a subagent → source-read each brief, then queue. **Held for the NEXT raise: 4** — `READY_KS-1258-N68-1`, `READY_KS-1258-N68-2` (graded by a checker re-run after today's harness fix), `READY_KS-1062-N67-1` (archived → NO Refs), `READY_KS-1260-N62`. When round 13's passes land, raise them all as ONE batch (a Seat B 5th brief from `briefs_staged/2026-09-19_raise_seatB_successor4.md`), then ONE gate.
4. **Owed harness extension:** the `tasks/test_only` builder cannot pin the runner for vc-issuer (its package.json lists jest + ts-jest + vitest) → brief `night/briefs/KS-1269-N71-1.md` (the null index; hand-measured 0/119 → 1/121) waits on a `runner=` override in the builder. Small; claim before touching (`wed_claim.sh`).
5. Harness fixed today: `local-model/tasks/test_only/checker.sh` restores a previous run's modified test file (IMPROVEMENTS row).

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
10. **Wednesday's reading to confirm:** with the non-auth pool exhausted (rounds 8-9), round 10 opened AUTH surfaces to TEST-ONLY local-model work (tamper-pinned cells, zero product bytes changed), on the recorded rule 'auth product EDITS stay out'. Default: it continues unless he says auth means tests too.

### OWED (tooling, mine, none urgent)
`brief_and_launch.sh` prints "launched" after cockpit SKIPS a same-name pane (false receipt; ledger 09-19) — needs `--pane-name` + rc 1 on skip · `cockpit.sh say %<id>` fails silently (use the NAME form) · `inbox_digest.sh` shows Datasec previews in the wednesday-agent@ section · a wake-turn Ornith print · `note_entry.sh` warn on a typed clock later than its stamp · a UTC-bound helper for commissions (ledger 09-19, the one-day-late cutoff).
