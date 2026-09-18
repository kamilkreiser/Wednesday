---
date: 2026-09-19
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's. Datasec mail by subject only.
source: replaced WHOLESALE at 09:12 2026-09-19 by the 06:0x Saturday seat (previous copy NEXT-PICKUP.md.pre-0919-0912; the 09-18 blocks are in NEXT-PICKUP-archive.md).
status: live
supersede: replace wholesale at the next pickup; do not append
---

# NEXT PICKUP

## ONE block (the 06:0x Saturday seat) — replace it, never append

**Kam is AWAY Sat 19 + Sun 20.** `tasks/WEEK-INSTRUCTION.md` is LIVE to the end of Sun 2026-09-20: merge on Wednesday's signed GO after a QA gate (Secuura CLAUDE.md line 238: "Wednesday's GO, naming the head SHA, is the approval"); deploy KINTSUGI ONLY; NOT demo; the signature classes still pause (KS-1250, KS-1175; money; external comms beyond rule-7); auth last. He leaves again MONDAY NIGHT 2026-09-21. `fleet/USAGE_STOP` = 90; gauge 47% at 08:1x. `local-model/night/ALLOW_SEATS` is armed to Sun 2026-09-20 23:00 (epoch 1789909200).

### FLOOR at 09:12
`%0` wednesday · `%107` **Seat B 2nd** (Secuura, pane name `Secuura/Blockchain-B`; HOLDING for GOs until ~23:28Z = 09:28 AEST, then wraps) · `%108` **QA gate #1050-#1060** (TIER 1 floor, round 1 of 2; report dir `!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1050-1060-tier1-r1/`) · `%1` monitor. Seat A 12th is WRAPPED + retired + scored 1.00.

### 🔴 FIRST ACTS for whoever holds this seat next
1. **The gate verdict (#1050-#1060).** When it lands: completion check against Seat B's READY (21:56:17Z) and the gate prompt `fleet/qa-agent/briefs/2026-09-19_secuura-batch1050-1060.prompt.txt`; then SIGNED GOs, one per head, to "Seat B 2nd" (or its successor if it wrapped), naming each head:
   #1050 KS-1261 6f6c6ed30 · #1051 KS-1136 item1 58e2fb66b · #1052 KS-1267 Q1 cd791b821 · #1053 KS-1258 N44-1 baf651460 · #1054 KS-1230 N45-5 1ea5c7b7e · #1055 KS-1202 N-B 31d55923d · #1056 KS-1153 R-918-A 7eb4dbad5 · #1057 KS-1209 N41-3 b3b90db4d · #1058 KS-1134 2e212047d · #1059 KS-1172+1173 f22ec785e (TIER 1) · #1060 KS-1264 3743e57ea (TIER 1). Predicted all-eleven tree cb7860d61.
   **Ticket states after merge (Seat B's proposal, accept):** ONLY KS-1134 → Done; all others stay In Progress (§5f, or the named halves still open).
   **Feed the gate's NOT-PINNED list to Ornith** (a round-6 search commission from it).
2. **After #1059 merges: a small kintsugi follow-up deploy** of KS-1172/1173 (the flow verbs a 09-15 board comment promised Stuart "Sunday with a kintsugi deploy"). **A DISK RULING comes first**: kintsugi has 24 G free (81%); a warm rebuild used ~19 G. A service-scoped swap (originate + anchoring + api-gateway for the yaml) may fit; measure before starting. Rollback stamp LITERAL (the box clock is UTC). No message to Stuart from us beyond rule-7 facts; a promise is Kam's.
3. **The next raise (7 held local-model READYs, all 2026-09-19, `local-model/night/READY_*`):** KS-1206 (code_patch, adminConfig.ts; GATE Q: null/0 now 400; sequence vs held KS-730-B, same file) · KS-1101 N-3 · KS-864 R-1 · KS-991 R-1 (the pre-push hook suite) · KS-739 F1 (tamper line −12 after #1060) · KS-1062 F-1. One batch gate. Plus the older 09-15..17 READYs still to reconcile against develop (a census job).
4. **The test_only header-field fix** (claimed via wed_claim 09:0x; a tooling subagent is building it with 5 arms). On its report: re-check the arms yourself, release the claim, then validate with a MODEL run of the ORIGINAL KS-739 r1 brief (`night/briefs/KS-739-F1.md.pre-0919-r2headers`).

### TODAY'S RECORD (verified at source)
- **Kintsugi REBUILT** to develop 59412d057 (from a105cd32b): 29 new, 0 failed, verified by behaviour; #1038 key ABSENT (TTL −2/−2), nothing written; #1045 ABSENT; KS-1272 (Low) filed; rule-7 KS-485 `e38cba4c` / KS-772 `db776515`.
- **Local model: 8 tickets, 8 held** (KS-1264 → #1060; KS-739 on its one rebrief). 5 search rounds read 98 for 7 fits; the gate-tamper seam is thinning.
- panel_sync restarted on Tuesday's FETCH_HEAD fix 4fc780e24 (pid 42360).

### HOLDS
KS-1250, KS-1175 Kam's · nothing to demo · no contact with Peter/Stuart beyond rule-7 facts · auth last · never delete · Tuesday owns Datasec (the ATTIO digest mis-lands in wednesday-agent@ daily; already told her 09-17).

### ROUTE TO KAM (Monday 21) — one list
1. Peter's two KS-1195 questions (per-key rateLimit for S connector keys; KS-1206 "429 forever"; PS-928 Stuart Urgent) — unanswered by design.
2. Peter's KS-593 addition: fuzzed wallet authenticate/verify → 500 where 400 belongs.
3. Kintsugi has NO connector allow-list configured (measured by seat A 12th).
4. Kintsugi disk: 24 G free; the next rebuild needs a space ruling.
5. KS-1262 (High) test-token severity check: unowned.
6. The drive sync keeps making `(conflict_on_…)` copies: 27 untracked in WEDNESDAY (they make panel_sync SKIP its rebase every cycle), 9 in the vault; not removed.
7. From 09-18: seat A's launcher F-02 (no keychain SSH identity), the open card `wed-boot-read-exceeds-the-context-window`, O-1 (CI jobs never start), the NSG's dynamic IP.

### OWED (tooling, mine, none urgent)
`brief_and_launch.sh` prints "launched" after cockpit SKIPS a same-name pane (false receipt; ledger 09-19) — needs `--pane-name` + rc 1 on skip · `cockpit.sh say %<id>` fails silently (use the NAME form) · `inbox_digest.sh` shows Datasec previews in the wednesday-agent@ section · a wake-turn Ornith print (the 06:41 unheld PASS) · `note_entry.sh` warn on a typed clock later than its stamp.
