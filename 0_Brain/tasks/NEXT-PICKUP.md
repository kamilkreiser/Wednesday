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

### FLOOR at 00:1x Sun 20 (the 18:0x seat; refreshed wholesale, not appended)
`%0` wednesday · `%1` monitor · no agent live. develop = `4273adfac` (#1084-#1091 merged + verified at source; Seat B 6th wrapped, scored 1.00). Kintsugi at f9c28a8b8: every batch since is test-only, no redeploy owed. **Day 09-19: 31 PRs merged (#1061-#1091).**
**Ornith:** round 17 RUNNING (KS-1238-N83-2, KS-1238-N83-6, KS-1282-N91-2; queued 00:02 with a verdict waiter). **HELD for the next raise: 5** — KS-1230-N86-1 · KS-1062-N88-1 (archived, no Refs) · KS-739-N89-1 (archived, no Refs) · KS-1238-N91-1 · KS-1238-N90-1 (READY files in `local-model/night/`). Round 17 shares the ks1238/ks1215 test files with N90-1/N91-1; the both-order proofs are in each round-17 brief.

### 🔴 FIRST ACTS for whoever holds this seat next
1. `kam_rulings_today.sh` + `reconcile_rulings.py`. **Every wake turn starts with `python3 2_Project_Files/fleet/ornith_status.py`.** **Every queue append is followed IN THE SAME ACTION by a background waiter on the verdicts** (ledger 09-19, w=11).
2. When round 17's verdicts land: source-read each (input from night_meta.json; `+` lines vs the brief; crossed control) → READY files → **8 held** → commission a Seat B 7th raise-brief DRAFTER from `fleet/briefs_staged/2026-09-19_raise_seatB_successor6.md` (tier 1 = the KS-1238 PRs + KS-1282, auth test-only, pushed last; archived KS-1062/KS-739 get no Refs; the ks1238 and ks1215 files each carry several diffs → one PR per FILE, both-order proofs carried) → read it whole → send → verify at the inbox → `cockpit.sh launch "Secuura/Blockchain"` → rung 5 → plan confirmation → READY → batch gate drafter (model `fleet/qa-agent/gatesets/2026-09-19_gate1084to1091/`) → re-pin + `--check` → launch → verdict → ONE signed GO → merges → verify develop's tree at source → score.
3. Monday list additions from tonight: N84-1 (/unrevoke check order, with the -1 question); whether one guard pin completes KS-1282.

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
9. KS-1269-U + N84-1: should `/unrevoke` refuse `index < 0`? And its index check sits AFTER its 404 (/revoke: before) — should the order match? (the #1084-1091 gate, question only). KS-662 lists `/unrevoke {index:-1} → 200` as NON-RULED; the held fix leaves it unchanged.
12. The audit-baseline.json fuse expires 2026-09-24 (two rows, :180 and :187; Seat B 7th flagged it 2026-09-20).
11. Ruleset 18499832 (develop) carries `require_extra_approval_for_unattributed_changes: true` — seen by Seat B 5th 2026-09-19; it blocked nothing; whether it is new is unmeasured.
10. **Wednesday's reading to confirm:** with the non-auth pool exhausted (rounds 8-9), round 10 opened AUTH surfaces to TEST-ONLY local-model work (tamper-pinned cells, zero product bytes changed), on the recorded rule 'auth product EDITS stay out'. Default: it continues unless he says auth means tests too.

### OWED (tooling, mine, none urgent)
`brief_and_launch.sh` prints "launched" after cockpit SKIPS a same-name pane (false receipt; ledger 09-19) — needs `--pane-name` + rc 1 on skip · `cockpit.sh say %<id>` fails silently (use the NAME form) · `inbox_digest.sh` shows Datasec previews in the wednesday-agent@ section · a wake-turn Ornith print · `note_entry.sh` warn on a typed clock later than its stamp · a UTC-bound helper for commissions (ledger 09-19, the one-day-late cutoff).
