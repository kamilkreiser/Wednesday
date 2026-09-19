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

### FLOOR at 10:5x
`%0` wednesday · `%110` **Seat B 3rd** (pane name `Secuura/Blockchain-B`; brief `2_Project_Files/fleet/briefs_staged/2026-09-19_raise_seatB_successor3.md`) · `%1` monitor. Seat B 3rd STATUS 00:44:29Z: all nine RAISE OK at develop 3c447abc7; the local all-nine tree `275cff9ff` is green on every affected suite; push series 00:43:46Z → ETA ~01:40Z (~11:40 AEST), then PRs → ONE READY. It is HOLDING by design (idle wake acked with `wake_ack.sh %110`). develop = 3c447abc7 (`ls-remote` 10:2x). Kintsugi = 3c447abc7 (seat A 13th, V1-V9).

### 🔴 FIRST ACTS for whoever holds this seat next
1. `kam_rulings_today.sh` + `reconcile_rulings.py` (0 panel lines today as of 10:5x).
2. **On Seat B 3rd's READY:** draft ONE batch gate over the nine PRs (model: `fleet/qa-agent/gatesets/2026-09-19_gate1050to1060/` + its generator); tier 1 = KS-1260 (pre-push gate) and KS-1206 (the null/0 → 400 caller question); re-pin by `ls-remote` + `--check` IMMEDIATELY before launch; then GO per head; the seat merges one at a time, re-reading develop after each.
3. **Ornith: queue EMPTY WITH A MEASURED REASON.** Search rounds 8 (2 fits) and 9 (0 fits, 30 read) are in `local-model/night/candidates.md`; the pool is exhausted at grep depth. Its next feed is the NOT-PINNED list from that batch gate's report. Brief from it the moment the report lands. **First feed, already identified (the drafter's lead): after #1061 merges, a test_only brief adding `rateLimit: null` and `rateLimit: 0` cells (→ 400) to the KS-1206 test file**. Those are the two values the change is about, and the file's 6 cells send neither. It is not briefable before the merge, because the file does not exist at develop.
4. **Held for the NEXT raise (after the nine): 3** — `READY_KS-1276` (doc: VOCABULARY.md PII caveat; premise re-measured by Wednesday at 3c447abc7) · `READY_KS-1269` (vc-issuer `/revoke` rejects a non-integer `index`; `/unrevoke` residual; KS-662's -1 allowance covers /revoke — read by the KS-1269-U subagent) · **`READY_KS-1269-U`** (held 11:3x; raise in ONE PR with KS-1269) (the `/unrevoke` twin, same file 62 lines lower, both orders apply clean; pins nothing about -1). All raise as **Refs**.

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
