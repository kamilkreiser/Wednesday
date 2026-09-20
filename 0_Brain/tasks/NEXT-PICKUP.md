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

### FLOOR at 15:3x Sun 20 (refreshed at the 70% checkpoint)
`%0` wednesday · `%1` monitor — **no agent pane live**. Two SUBAGENTS in flight (Agent tool, background): the **Seat B 9th raise-brief drafter** (2 held fixes → 2 PRs) and the **Ornith round-20 search-and-brief** (widening over the board; up to 3 fits; rejection table to `candidates_rounds.md`). develop `e470198783bcb1ef0eac94780f87579974051423`, tree `706de830` (#1097-#1099 merged 19:56Z, verified at source).
**KAM, panel 15:25:26 +10:00, verbatim:** *"how is it going?  do you need anything from me?  Please continue with the tickets.  close, archive merge and deploy anything that's ready.  then continue with both claude and local agents"* — receipted within the minute; card `wed-allowance-pace-before-week-away` RULED `spend-to-90` on those words (stated to him). **Both lanes are open again: Claude seats AND the local model.** Usage 79% at 15:3x (renews Fri 25 Sep 8am; the 90% cut is his standing rule).
**Held for the NEXT raise: 2** — KS-1230-N97-1 (ks1230 file, tier 2) · KS-1282-N99-1 (ks1215 file, AUTH test-only, tier 1). **Deploy: nothing owed** — every merge since kintsugi's f9c28a8b8 deploy is test-only, 0 product bytes.
**With Kam:** KS-1282's completeness (asked 15:2x; all 13 guards pinned). Nothing else is waiting on him.

### 🔴 FIRST ACTS for whoever holds this seat next
1. `kam_rulings_today.sh` + `reconcile_rulings.py`; **every wake turn starts with `ornith_status.py`**; every queue append carries a background verdict waiter in the SAME action; a mail lower bound = the send's printed time minus a margin.
2. **When the raise drafter returns:** read the staged brief WHOLE, re-derive its counts (ledger 09-20: a drafted count passed unread, twice), send via `send_brief.sh`, verify at `secuura-blockchain@` BEFORE launching, `cockpit.sh launch "Secuura/Blockchain"`, confirm rung 5 from the pane's OWN words (not the prompt's echoed template — the 05:01 weak hit), answer its plan, then READY → ONE batch gate → completion check → signed GO → merges → verify at source → score → close the pane.
3. **When the round-20 search returns:** verify each input against its brief (expected_plus, tampers, 0 backslash, 0 non-ASCII), queue with a verdict waiter, hold each PASS after a source read with a CONTENT control (not the path-level crossed control — ledger 09-20 R-1).
4. **Kam's 15:25 instruction also asks to close and archive what is ready:** a board pass is owed as its own lane (no file overlap with the raise). True duplicates and finished work are closed and archived by us, no external review (his 2026-09-14 standing rule).
5. The WEEK-INSTRUCTION lapses at the END of today: on Mon 21 set `status: lapsed`, stop acting on its authority, card Kam, and bring him the Monday list.
6. Ledger rows dated 09-17 pass the 3-day line on 09-21 → rule 3c at the next wrap/rotation after midnight.

### Reallocated to a Claude seat (Kam's 09-16 counter; do NOT queue at the local model)
KS-1168, KS-1163, KS-998, KS-866 (from 09-16/17) · the KS-871 remnant (`services/api-gateway/src/middleware/audit.ts:333` logs `path: req.path` on a failed audit write; KS-871 In Progress) · KS-1279 / N62-3 (preflight leg-1 accounting; a product fix).

**Commission rule (ledger 2026-09-20, w=3):** a commission that forbids a port or service names the READ-ONLY control instrument (`lsof -nP -iTCP:<port> -sTCP:LISTEN`) and forbids `nc`/`curl`/any client against it BY NAME.

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
18. A Wednesday brief-writing subagent (round 19) made three brief contacts with the live local Postgres on :5432 (two port probes and one stray connection, closed by the server) while proving its isolation; no test reached it. Whose database that is on the Studio is unmeasured. Disclosed, and the commission rule is fixed.
17. Gate records R-2/R-3 (pre-existing): `run-shell-suites.sh` reaches registry.npmjs.org (174 HTTPS per pass) and tries localhost:6882/:6982/:7082 despite the env overrides; clone-to-tenant's tenant-provisioning lookup carries no Authorization; six platform routes (tenant-key ×3, templates ×3) are missing from the published OpenAPI spec. No tickets filed.

### OWED (tooling, mine, none urgent)
`brief_and_launch.sh` prints "launched" after cockpit SKIPS a same-name pane (needs `--pane-name` + rc 1 on skip) · `cockpit.sh say %<id>` fails silently (use the NAME form) · `inbox_digest.sh` shows Datasec previews in the wednesday-agent@ section · a wake-turn Ornith print · `note_entry.sh` warn on a typed clock later than its stamp · a UTC-bound helper for commissions · a rung-5 helper that refuses to count a match on the commission's own prompt text (today's 05:01 weak hit).
