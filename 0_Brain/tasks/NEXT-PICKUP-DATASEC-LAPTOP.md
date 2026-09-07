---
date: 2026-09-07
type: pickup
scope: DATASEC ONLY — laptop seat. Secuura belongs to the Studio seat; do not touch it.
source: replaced wholesale at the 70% checkpoint
status: live
supersede: replace wholesale at the next pickup; do not append
---

# NEXT PICKUP — Datasec laptop seat, ~17:0x AEST Monday 2026-09-07 (rotated at 80%)

## 🔴 READ THESE FOUR FIRST — they change conclusions already given to Kam
1. **THE CI SECRET GATE MAY BE DECORATIVE.** All 25 `gitleaks.yml` workflows pin
   `actions/checkout@v7` — a major that does not exist. Wednesday verified: v4×35, **v7×25**, v2×8,
   v3×3, v5×1, **no v6**; all 25 v7 files are gitleaks workflows, zero non-gitleaks use v7. A workflow
   whose checkout cannot resolve **fails before the scanner runs**. Corroborated: `terraform.tfstate.backup`
   still carries F-16 credentials in a repo whose gitleaks nominally runs on every push. **SUSPECTED,
   high confidence — one look at Actions run history settles it; now the top item of the live pass.**
   This RETRACTS the one improvement credited all day.
2. **KEYCLOAK IS WIRED AND LOAD-BEARING** in all four production regions (5-step chain proven; positive
   control: pdf-api modules DO carry `count = 0`, so disabled is detectable). **Not documentation debt —
   a live legacy dependency.** `04_Keycloak_Retirement_Attestation` is now CONTRADICTED, not merely
   unevidenced.
3. **A LICENSING DECISION CAN BE FORGED WITHOUT THE ROOT KEY** — new Critical. The `valid:true` token is
   signed by a per-tenant key that travels inside every licence file, JWE-wrapped to a committed key, and
   binds nothing (no iss/aud/exp/tenant; cert has no extensions). **F-11's root rotation does NOT fix it.**
4. **TWO REMEDIATIONS MUST NOT BE RUN AS WRITTEN:** (a) rotating the root CA **wipes the licence table** —
   `TenantLicenseService.cs:50-54` deletes on validation failure, on the default page render; fix that
   first. (b) Deleting the committed `.key` files does NOT remove the root key — `LicenseGenerator.exe`
   is committed and CONTAINS it; no text scanner sees it.

# (previous header) Datasec laptop seat

**TWO WEDNESDAYS LIVE.** Studio owns **Secuura**; this seat owns **Datasec**. One repo, one dashboard,
one chat panel, **ONE USAGE LIMIT**. Do not write the shared files (`NEXT-PICKUP.md`, daily note,
`_ledger.md`) — hers this session. Panel messages open `[LAPTOP / Datasec]`.

## ⚠️ THREE THINGS THAT WILL BITE YOU
1. **`git -C $VARIABLE <writeverb>` is REFUSED** — the hook matches literal text and cannot resolve a
   shell variable, so it fails closed. **Write git paths literally.** It also fires on a commit
   message that merely *describes* a git command → write the message to a file, use `-F`.
2. **Max 3 concurrent agents.** The shared session limit was exhausted at 11:17 by 21 agents in
   90 min, 12 concurrent (~3.0M tokens across the 12 that finished). Weekly is fine (22%); the
   SESSION RATE is what breaks. Neither seat can see the other's usage.
3. **Ghost text has appeared TWICE at the NexusAI prompt.** Run `pane_prompt_check.sh` BEFORE reading
   anything at a prompt. The second instance named something already authorised — **a ghost line that
   coincides with a real authorisation is more corrosive than one that doesn't, because it gets
   reinforced rather than corrected.** The test is never "is this correct" but "does this have an author".

## FLEET — 2 live
- **RD-361 round-2 TIER-1 RE-GATE running** (launched 17:0x). **Round 2 of 2 under Kam's cap** — a NO GO
  ships what is closed and tickets the residue; no round 3 without his word.
- **`Datasec/NexusAI` `%2`** at ~52% ctx, ran its own checkpoint, `HANDOVER-S43.md` written. Working
  **RD-362 then RD-329** (Wednesday RULED the reorder: the round's Marketplace objective outranks
  priority-then-identifier). **Do not close that pane.**
- **DELTA BATCH 1 COMPLETE — all 7 components reported.** BATCH 2 STILL TO LAUNCH (4): CypherOneDrive +
  Teams (gate INTACT — the control group for F-13) · CommonValueLibraryCypher · Cyphercard-Enrolment-App.
- **GATE QUEUE, IN ORDER: (1) RD-361 r2 tier-1 RUNNING → (2) SEC-07/RD-363 @ `b0dec96` tier 2 →
  (3) RD-148 @ `aea410c` (`rd-148-scim-revoke-ui-s43`, 2164/2164).** Fire 2 and 3 as slots free.
- **RD-50 was MISCLASSIFIED as category 1 by the agent and is category 2** — its execution lives in the
  Feedback System and Lead Bot folders, which a NexusAI seat cannot write to (hard rule 1). The agent
  caught it, audited all 97 for the class, and owes the corrected count — **the cat-1 number Kam is
  held to is not final until that lands.** General rule for the handover: *a ticket's category is a
  claim read from its scope note, not inferred from its board state.*
- **SEC-07 / RD-363 @ `b0dec96` QUEUED for a tier-2 gate.** Do not "fix" its deliberate omission of
  `networkAcls Deny` — it would brick every customer deployment; the reason is pinned in a test cell.

## RD-361 HISTORY — NO GO round 1, round 2 built
Round 1 was NO GO: the fix closed **1 of 4** failure modes and **the Azure Files case named in its own
rationale survived**. Also mutation-proven: 3 of 5 sites had no regression protection; a **sixth site**
existed (`entraProvisioning.js:107`, fails closed). 503-over-401 **endorsed**, but the builder's
reasoning was inverted (503 is what HTTP machinery retries).
Round 2 closed F-1 using two pre-existing unused signals (`dataDirFallbackActive`,
`persistenceSentinelPreexisting`), re-derived the gate's table on its own round-1 worktree, and
**named what it does NOT close**: a persistent volume wiped between deploys is byte-identical to a
genuine first deploy, and denying there would brick every legitimate first deployment. Routed to
RD-363/platform layer. **Wednesday ACKNOWLEDGED and CREDITED round 2 but did NOT ratify it** — the
design reasoning lives in the mail and is ratifiable; the product claim goes to the gate.

## SECURITY REVIEW — STEP 1 COMPLETE, step 2 awaiting Kam
**219 findings: 31 June (27 unremediated, ZERO fixed) + 188 new. NOW 16 new Criticals, not 15.**

**STEP 1 (verify): all 10 files written. Wednesday has READ 4.**
Read: HP-AuthSuite (12 conf/1 UPGRADED) · Cryptix (28 conf/1 down, all 4 Criticals stand) · HPSA
(16 conf/2 down) · infra-admin-portal (6 conf/1 down/**1 UPGRADED**/1 unverif/**+6 new**).
**Across the 4 read: 62 findings re-derived, ZERO refuted.**
**UNREAD, written but not yet read by the coordinator — NEXT TASK, cheap:** OneTimePad · myPKI ·
SecurePDF · pdf-api · OXPd1 · Reporting Dashboard, all in `_Working/verification-2026-09/`.

**THE THIRD CRITICAL (INFRA-03, High 7.5 → ~9.3):** the admin portal's committed encryption key is
**AES-ECB** (no IV, no auth, deterministic, raw-UTF-8 key, no KDF) over **customer tenants' Entra
app-registration credentials**. A customer-credential vault whose master key is in the repo.
Also: the unauthenticated webhook endpoints are worse than the seed said — `onboarding-cleanup`
irreversibly null-writes credentials on **every** row older than 7 days; `saas-refresh` lets an
anonymous caller trigger **outbound customer email**. **No compensating control at any layer**
(proven three ways). dev ≡ staging on all three Entra secrets; **production separate on all nine**.

**STEP 2 (delta on the 19 June components): 8 done, 11 COMMISSIONED.** Wednesday recommended dropping
them; **Kam overruled — "yes, queue the eleven three at a time."** He was right and the register says
so: the gap sits exactly in the class scanners cannot see, which is where every Critical came from.
Register §7.1 rewritten from "named gap accepted" to "commissioned, in flight" — **do not let the
in-flight state harden into a claim of completeness.**

## WEDNESDAY'S OWN ERRORS TODAY — 4, all corrected in the open
1. Consolidation ruled backwards ("keep earliest"); the agent had the better rule (keep **the ticket
   that represents the work**). Corrected 15:52 and executed.
2. "18 findings" relayed without counting — it was 17.
3. Vision called "live production" from a stored note; Kam says pre-production.
4. **"23-key inventory" of production.tfvar — it is 33.** My awk excluded values <15 chars: a floor
   presented as a count. **All four are the same axis: a claim composed from an artefact, or an
   instrument whose scope did not match the question. Six instances today.**

## DELIVERABLES — current, `.md` + branded `.docx`
`12_Rerun_Delta_2026-09` · `13_Consolidated_Findings_Register_2026-09` (now carries **§2.1 the
verification pass**) · `11_Assurance_Pack_Index` (rows 1–19 flagged as understating the estate) ·
13 component summaries · `_Working/{findings-seed,verification,delta-review}-2026-09/` ·
`scan-artifacts-2026-09/` (argv recorded per tool) · `_Working/2026-09-07_{METHOD_IMPROVEMENTS,RERUN_DISCOVERY,VISION_PARKED}.md`

## OPEN FOR KAM
1. **RD-18** — the Australian Privacy Act package. The real Marketplace exposure; on hold, untouched.
2. Re-issue June deliverables 00/03/04/09/10 against 219, or let 12+13 stand as authoritative?
3. Live GitHub/Azure/Entra pass still open; tenant conflict `fc05dcdd` vs `0c57ab37` unresolved
   before any `az`.
4. **Vision PARKED** by his 10:44 ruling (`_Working/2026-09-07_VISION_PARKED.md`).

## FIXED TODAY (mechanisms, not intentions)
- **`pretooluse_no_cd.sh` root is now self-locating** (`cb646a4a`) — it was hardcoded to DevMASTER and
  blocked **every commit** from this seat. Both branches exercised.
- **`/api/speak` autoplay is seat-scoped** — the Studio's Secuura messages were being voiced here.
- **`chat_reply.sh` self-heals a conflicted chat log** (`1fec3378`) — recovers BOTH seats' entries,
  dedupes, re-sorts. It had corrupted 3× today and I was repairing it by hand.
- **Studio seat MAILED** with all of the above + the hook's three known limits.

## HALF-BUILT — DO NOT ASSUME IT WORKS
`chat.html` edited, **UNCOMMITTED/UNVERIFIED** — the per-project chat filter (Kam's 11:12 ask) was
half-built when the limit hit. Backups `*.pre-0907-filter`.

## STANDING
No `cd`. Quote every grep glob. Every negative claim needs a positive control. `send_brief.sh` wants
literal `^PROVENANCE:` + `- <fact> | <source> | read YYYY-MM-DD` and `SELF-CHECK: re-read end-to-end
for contradictions | YYYY-MM-DD HH:MM`. Taps ≤200 chars, pointer only, mail first, verify BODY by
`preview` non-null. `<<'EOF'` for every brief. Never delete — quarantine. Band **80–90%**, 90 ceiling.
