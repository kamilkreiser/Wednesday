---
date: 2026-09-07
type: pickup
scope: DATASEC ONLY — laptop seat. Secuura belongs to the Studio seat; do not touch it.
source: replaced wholesale at the 70% checkpoint
status: live
supersede: replace wholesale at the next pickup; do not append
---

# NEXT PICKUP — Datasec laptop seat, ~16:15 AEST Monday 2026-09-07

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

## FLEET — 2 agents
- **`Datasec/NexusAI` `%2`** (ctx ~34%). Executing the sweep ruling (A/B/C/D merges, E held, F
  conditional), then back to RD-361. **Do not close that pane** — a queued tap starts a new turn.
- **RD-361 tier-1 QA gate** — running. Its verdict is the next thing that moves RD-361.

## RD-361 (SEC-01, the Critical) — BUILT, AT THE GATE
Branch `rd-361-fail-closed-unknown-s43` @ `e4d9147`, `npm run verify` 2165/2165, `rd-334` untouched.
**It found FIVE fail-open sites, not one** — incl. two admin-only query endpoints where UNKNOWN
skipped the admin-role check; neither was in the review or the ticket. It **self-caught two faulty
test cells**, incl. a tamper control that passed *vacuously* at the unfixed head.
**Open deviation for the gate, not for Wednesday:** review asked 401, it returns **503
`AUTH_STATE_UNKNOWN`**. Wednesday ratified the REASONING; the claim "the security property is
identical" is a product claim and went to the gate.

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

**STEP 2 (delta on the 19 June components): 8 of 19 done. AWAITING KAM'S STEER** — recommendation is
to DROP the remaining 11 to a named gap; it is the lowest-value work and where the budget went.

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
1. **Delta-review steer** (above).
2. **RD-18** — the Australian Privacy Act package. The real Marketplace exposure; on hold, untouched.
3. Re-issue June deliverables 00/03/04/09/10 against 219, or let 12+13 stand as authoritative?
4. Live GitHub/Azure/Entra pass still open; tenant conflict `fc05dcdd` vs `0c57ab37` unresolved
   before any `az`.
5. **Vision PARKED** by his 10:44 ruling (`_Working/2026-09-07_VISION_PARKED.md`).

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
