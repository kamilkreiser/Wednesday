---
date: 2026-09-20
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's. Datasec mail by subject only.
source: replaced WHOLESALE at 05:30 2026-09-20 by the 03:3x Sunday seat at the 05:30 shift change (previous copy NEXT-PICKUP.md.pre-0920-0530; older blocks in NEXT-PICKUP-archive.md).
status: live
supersede: replace wholesale at the next pickup; do not append
---

# NEXT PICKUP

## ONE block (the 03:3x Sunday seat, handed over at the 05:30 shift change) — replace it, never append

**Kam is AWAY until Monday 21.** `tasks/WEEK-INSTRUCTION.md` is LIVE to the END of TODAY, Sun 2026-09-20: merge on Wednesday's signed GO after a QA gate (Secuura CLAUDE.md merge section: "Wednesday's GO, naming the head SHA, is the approval"); deploy KINTSUGI ONLY; NOT demo; the signature classes still pause (KS-1250, KS-1175; money; external comms beyond rule-7); auth last. He leaves again MONDAY NIGHT 2026-09-21. `fleet/USAGE_STOP` = 90; **gauge 75% at 05:30** (renews **Fri 25 Sep 8am AEST**, read from Claude's own pane banner). `local-model/night/ALLOW_SEATS` armed to Sun 2026-09-20 23:00 (epoch 1789909200).

### FLOOR at 05:5x Sun 20 (tmux list-panes; updated in place after the gate verdict)
`%0` wednesday · **`%121` Seat B 8th MERGING on Wednesday's signed GO** (sent 19:50:59Z: #1097 → #1098 → #1099 last) · `%1` monitor. The gate pane `%122` is CLOSED (verdict 19:48:39Z, no NO GO, **KS-1238 COMPLETE by name**; scored 1.00). develop was `c87458bdd` at the GO; after the three squashes its tree must be `706de83052728ddfe4c581e378f708fec2338b80` (step trees `dff1aafa3581` → `752b889c6313` → `706de830`).
**Held for the NEXT raise: 0.** The Ornith feed is READY TO BRIEF once #1097-#1099 merge, at the post-merge tip: the gate's NOT-PINNED rows N97-1 ×2 (KS-1230: LASTOF2NULLMIXED, LASTOF4NULL at admin.ts:1132, ks1230 file) and N99-1 (KS-1282: SUPERROLESWIDEN at platform.ts:64, a role-ADMIN JWT refused 403 on GET /api/platform/tenants, ks1215 file). The gate wrote each proposed cell in its report's NOT-PINNED section.

### 🔴 FIRST ACTS for whoever holds this seat next
1. `kam_rulings_today.sh` + `reconcile_rulings.py` (0 panel lines on 09-19 or 09-20 so far). **Every wake turn starts with `python3 2_Project_Files/fleet/ornith_status.py`.** Every queue append is followed IN THE SAME ACTION by a background verdict waiter. A mail-check lower bound is the send's printed time minus a margin.
2. **GO SENT 19:50:59Z** (`fleet/briefs_staged/2026-09-20_seatB8_go_1097-1099.md`). **Wake = Seat B 8th's MERGED STATUS**: verify at source (`ls-remote` develop; `rev-parse <develop>^{tree}` = `706de830…`; read-only `git log c87458bdd..<develop>` shows three squashes, #1099 last); check KS-1238 Done + archived with the gate's facts comment read back, KS-1282 Backlog with NO comment → then its wrap: verify handover + history on disk → detector → `pane_close.sh %121` → score the seat → brief the Ornith round (N97-1 ×2, N99-1) at the new tip with a verdict waiter.
3. **Merge cut-off: 23:00 AEST today (13:00Z).** No GO by then → the seat hands over holding (its brief says so).
4. **Pace card** `wed-allowance-pace-before-week-away` (rec + default `pace-reserve`): after THIS raise lands, launch NO new Claude seat or gate until Kam is back Monday, unless he rules otherwise. Ornith continues on whatever can be briefed cheaply.
5. The WEEK-INSTRUCTION lapses at the END of today: on Mon 21 set `status: lapsed`, stop acting on its authority, card Kam, and bring him the Monday list below; he may give a new week instruction before he leaves Monday night.
6. Ledger: rows dated 09-17 pass the 3-day line on 09-21 → rule 3c at the next wrap/rotation after midnight (this seat archived 09-16: 55 rows, conserved 1104 = 1104).

### Reallocated to a Claude seat (Kam's 09-16 counter; do NOT queue at the local model)
KS-1168, KS-1163, KS-998, KS-866 (from 09-16/17) · the KS-871 remnant (`services/api-gateway/src/middleware/audit.ts:333` logs `path: req.path` on a failed audit write; KS-871 In Progress) · KS-1279 / N62-3 (preflight leg-1 accounting; a product fix).

### HOLDS
KS-1250, KS-1175 Kam's · nothing to demo · no contact with Peter/Stuart beyond rule-7 facts · auth last · never delete · Tuesday owns Datasec.

### ROUTE TO KAM (Monday 21) — one list
1. Peter's two KS-1195 questions (per-key rateLimit for S connector keys; KS-1206 "429 forever"; PS-928 Stuart Urgent) — unanswered by design.
2. Peter's KS-593 addition: fuzzed wallet authenticate/verify → 500 where 400 belongs.
3. Kintsugi has NO connector allow-list configured (measured by seat A 12th).
4. Kintsugi disk: 25 G free after seat A 14th's deploy; budget the TRANSIENT per-service build cost (~3.8 G seen), not the image size.
5. KS-1262 (High) test-token severity check: unowned.
6. The drive sync keeps making `(conflict_on_…)` copies (untracked in WEDNESDAY, making panel_sync SKIP its rebase every cycle; 9 in the vault); not removed.
7. From 09-18: seat A's launcher F-02 (no keychain SSH identity; inert — repo-local core.sshCommand works), the open card `wed-boot-read-exceeds-the-context-window`, O-1 (CI jobs never start), the NSG's dynamic IP.
8. report-796 F-01/F-03 (`scripts/audit/*.mjs`): a ruling, not a local-model ticket.
9. KS-1269-U + N84-1: should `/unrevoke` refuse `index < 0`, and should its index check sit before its 404 as /revoke's does? KS-662 lists `/unrevoke {index:-1} → 200` as NON-RULED.
10. **Wednesday's reading to confirm:** auth surfaces opened to TEST-ONLY local-model work (zero product bytes) under 'auth product EDITS stay out'. Default: continues unless he says auth means tests too.
11. Ruleset 18499832 carries `require_extra_approval_for_unattributed_changes: true` (unchanged since 2026-09-10 per two seats); blocked nothing.
12. The audit-baseline.json fuse expires 2026-09-24 (rows :180, :187).
13. O-1: admin.ts `requireAdmin` routes do no session check — a REVOKED admin session JWT gets 200 on POST /api/users/admin/create and PATCH /api/users/admin/:id in-process; KS-689's `authenticateToken(true)` routes at proxy.ts:472/:504 are shadowed by them. (#1099's N95-1 pins the connector-key-alone 401 only; it says nothing about O-1.)
14. KS-1282: with #1099 merged, all 11 previously-unpinned requireSuperAdmin guards carry a cell (plus :222/:239 from #1096/#1091). Is the ticket complete? His call.
15. **The allowance pace** (card `wed-allowance-pace-before-week-away`): ~1.3 points/hour over the weekend; renewal Fri 25 Sep 8am; what he wants for his week away.
16. KS-1238: ruled COMPLETE by the #1097-#1099 gate (Done + archived after #1099 merges). For KS-1282 the gate offered OPTIONAL facts text (13 of 13 guards pinned; a role widening reds 0 of 671, row N99-1), in its report's BY-NAME 6. Wednesday did NOT post it: that ticket is his call.
17. Gate records R-2/R-3 (pre-existing): `run-shell-suites.sh` reaches registry.npmjs.org (174 HTTPS per pass) and tries localhost:6882/:6982/:7082 despite the env overrides; clone-to-tenant's tenant-provisioning lookup carries no Authorization; six platform routes (tenant-key ×3, templates ×3) are missing from the published OpenAPI spec. No tickets filed.

### OWED (tooling, mine, none urgent)
`brief_and_launch.sh` prints "launched" after cockpit SKIPS a same-name pane (needs `--pane-name` + rc 1 on skip) · `cockpit.sh say %<id>` fails silently (use the NAME form) · `inbox_digest.sh` shows Datasec previews in the wednesday-agent@ section · a wake-turn Ornith print · `note_entry.sh` warn on a typed clock later than its stamp · a UTC-bound helper for commissions · a rung-5 helper that refuses to count a match on the commission's own prompt text (today's 05:01 weak hit).
