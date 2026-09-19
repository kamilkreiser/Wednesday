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

### FLOOR at 02:5x Sun 20 (the 18:0x seat, pre-rotation; refreshed wholesale, not appended)
`%0` wednesday · `%1` monitor · **no agent live.** develop = `c87458bdd` (tree 458cff717). **Weekend: 36 PRs merged (#1061-#1096)**, the last two batches verified at source by `rev-parse <develop>^{tree}` + `git log` (read-only). Seat B 6th and 7th wrapped and scored 1.00; every gate 1.00. Kintsugi at f9c28a8b8: every batch since is test-only, no redeploy owed.
**Ornith:** round 18 briefs commissioned ~02:5x (a subagent; rows from the #1092-1096 gate: N95-1 ADMINSHADOW (KS-1238), N92-1 (KS-1230), N93-1 (KS-1062, archived), N96-1a/b (KS-1282, up to 11 guards)). **If you boot and it has not been queued:** look for `local-model/night/briefs/KS-1238-N95-1.md`, `KS-1230-N92-1.md`, `KS-1062-N93-1.md`, `KS-1282-N96-1a.md`, `KS-1282-N96-1b.md` + their `night/inputs/test_only_*.json`; verify each input's `+` lines and tampers are in its own brief, queue, kick `launchctl kickstart gui/$(id -u)/com.wednesday.ornith-loop`, and arm a background waiter on the verdicts IN THE SAME ACTION. Then source-read each PASS → READY. When ~8 are held: a Seat B 8th raise (model `fleet/briefs_staged/2026-09-20_raise_seatB_successor7.md`) → gate (model `fleet/qa-agent/gatesets/2026-09-20_gate1092to1096/`) → GO (model `fleet/briefs_staged/2026-09-20_seatB7_go_1092-1096.md`).

### 🔴 FIRST ACTS for whoever holds this seat next
1. `kam_rulings_today.sh` + `reconcile_rulings.py` (0 panel lines 09-19 and 09-20 so far). **Every wake turn starts with `python3 2_Project_Files/fleet/ornith_status.py`.** **Every queue append is followed IN THE SAME ACTION by a background waiter on the verdicts** (ledger 09-19 w=11). **A mail-delivery check's lower bound is taken from the send's printed time minus a margin, never a felt "now"** (ledger 09-20).
2. The ledger was edited this session (two rows) → at wrap/rotation regenerate BOTH digests: `python3 2_Project_Files/tools/boot_digest.py --by-tier` and `python3 2_Project_Files/tools/boot_digest.py`.
3. The WEEK-INSTRUCTION lapses at the END of today (Sun 2026-09-20): on Mon 21 set `status: lapsed`, stop acting on its authority, card Kam, and bring him the Monday list below; he may give a new week instruction before he leaves Monday night.

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
13. O-1 (the #1092-1096 gate): admin.ts `requireAdmin` routes do no session check — a REVOKED admin session JWT gets 200 on POST /api/users/admin/create and PATCH /api/users/admin/:id in-process; KS-689's `authenticateToken(true)` routes at proxy.ts:472/:504 are shadowed by them. Is KS-689's fix dead code? (defence-in-depth per KS-689; the auth service behind it is said to check sessions — unmeasured).
14. KS-1282: N91-2 pins :222; :239 is pinned by #1091; the other 11 guards are unpinned (measured). Is one pin enough, or should the 11 be pinned too (local-model work, test-only)?
12. The audit-baseline.json fuse expires 2026-09-24 (two rows, :180 and :187; Seat B 7th flagged it 2026-09-20).
11. Ruleset 18499832 (develop) carries `require_extra_approval_for_unattributed_changes: true` — seen by Seat B 5th 2026-09-19; it blocked nothing; whether it is new is unmeasured.
10. **Wednesday's reading to confirm:** with the non-auth pool exhausted (rounds 8-9), round 10 opened AUTH surfaces to TEST-ONLY local-model work (tamper-pinned cells, zero product bytes changed), on the recorded rule 'auth product EDITS stay out'. Default: it continues unless he says auth means tests too.

### OWED (tooling, mine, none urgent)
`brief_and_launch.sh` prints "launched" after cockpit SKIPS a same-name pane (false receipt; ledger 09-19) — needs `--pane-name` + rc 1 on skip · `cockpit.sh say %<id>` fails silently (use the NAME form) · `inbox_digest.sh` shows Datasec previews in the wednesday-agent@ section · a wake-turn Ornith print · `note_entry.sh` warn on a typed clock later than its stamp · a UTC-bound helper for commissions (ledger 09-19, the one-day-late cutoff).
