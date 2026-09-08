---
date: 2026-09-08
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Kam ruled the name 11:56). Read Datasec mail by SUBJECT only.
source: replaced WHOLESALE at 19:4x by s151 at its 66% checkpoint (band is 80-90, Kam 2026-09-07 — NOT a rotation)
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — s151 (Studio) LIVE. Secuura seat working. Nothing blocked, nothing waiting on Kam.

## 🟢 SECUURA STATE — re-read from origin before trusting ANY of it; Peter is live tonight
    origin/develop   811a82253    (5c6777658 -> 4f612d462 via #909, -> 811a82253 via Peter's #802)
    origin/main      54b2a5c26    demo VM 400517aaf — NOTHING deployed this session
    P2 In Review     20           (was 27 at boot)
    branches pushed  #806 d38284a1c (clean) · #785 3611f60c4 (preflight passed)

**⚠ PETER MERGED #802 MID-SESSION AT 08:45Z.** Standing: re-read `develop` from origin immediately
before any merge, and treat any state figure older than your last read as stale. A merge by someone
else is exactly when a previously-verified fact stops being verified.

## 🟢 DONE THIS SESSION
- **#909 merged** — today's own #793 merge (`0e706a57f`) had REVERTED two of Kam's audit-baseline
  rulings and re-armed a push-gate fuse dated **2026-09-10**. Restored, key-set identity-checked
  against `bf0a4ab99`, red-proofed both directions. **Thursday is clear.**
- **KS-577/KS-843 interaction resolved, NO code, Kam's ruling intact.** #880 would have killed Platform
  S's key instantly (401 above the scope gate) and made option A's trigger unobservable. Remedy is
  config that #880 already ships. Cross-linked comments **KS-843 `82de36ad` · KS-577 `868d1211`**.
- **KS-823**: a live High defect parked In Review by a phrase Wednesday accidentally invented (see
  errors). Now **Todo P2, a defect to fix**. Reachable unauthenticated but needs a valid refresh
  token — **token-binding weakness, not an open door.** NO probe was made and none is authorised.
- **KS-1003** filed (P3): `/api/oauth/` sits OUTSIDE the credential-stuffing rate-limit zone.
- **KS-677, KS-854 → Done**; KS-597/722/860/970 → Deployed to UAT; KS-854 → the column convention is
  written on it. **Ruling: never park a ticket in a column whose exit condition cannot occur.**
- **#785**: Peter's blocker fixed, reformat reverted (AST 1612 vs 1612, zero differing).

## 🔴 THE TENTH INSTANCE REACHED A CLIENT HUMAN — corrected, verify it stays corrected
At 05:08 a seat told Peter on #785 *"the action on this one is yours."* **It was ours** — his review of
09-03 held approval at a commit still the head. **Corrected in BOTH directions:** `5582820263` leads
with the correction and links back; **`5579579360` (the false comment) now carries a forward banner**
with its original body preserved verbatim. **Do not let either be tidied away.**

## 🔴 OPEN / NEXT
1. **The remaining P2 In Review queue**, dispositions first, by identifier.
2. **#806 and #785 both await Peter's review.** His approval on #806 is VOID (`commit_id != head.sha`)
   and that is stated on KS-731 as a warning block, not a table row.
3. **#792 is PETER'S OWN PR**, approved by us at head, clean, stalled on him. Ticket carries the fact,
   asks nothing. **Kam has the optional two-line nudge text; default is the comment stands.**
4. **PS #783 unreadable** — the PAT 404s on the whole `Secuura/platform-s` repo (control run). Needs
   platform-s scope on the token. **Kam's.**
5. **KS-907 / KS-788** sit in `Tested Not Deployed` and are the same class as KS-854 — other seats'
   tickets, named on KS-854 so the next pass decides deliberately.

## 🔴 WITH KAM — all have safe defaults
`secuura-ks963-widen-to-preauth` · and three that are **TUESDAY's, not this seat's**:
`hpsm-credential-bearing-prd-outside-every-snapshot` · `secrev-live-pass-blocked-on-tenant` ·
`nexusai-rd369-round3-or-ship-at-the-cap`. **Tuesday has not booted yet.**

## 🔴 DO NOT RE-RAISE — settled this session
- **F-02 SSH preflight is a FALSE ALARM.** Push proven twice (dry-run + real, both exit 0). The same
  instruction was wrongly given to Kam on 2026-08-06. It does not go to him.
- **The Stuart cutover** — he ruled it 2026-09-06 (`logged grace`, chosen *because* it needs no window
  with Stuart).
- **The archive-cascade card** — CLOSED, no card filed. 7 tickets, all Backlog, all inside the 61 he
  ruled `three` on at 14:00.

## 🔴 WEDNESDAY'S ERRORS THIS SESSION — `_ledger.md` (234 rows), and three are about ITS OWN RULES
1. **A W-tier lesson filed this morning rested on an unmeasured 200K window** — corrected by
   measurement; the boot fits comfortably (7% → 21% → 36%).
2. **A phantom ruling of Wednesday's own making**: it compressed a builder's *"filed only — not in
   this session's queue"* into *"KS-823 (High, file-only)"*, and four readers inherited it faithfully
   for three days. **Discharged.**
3. **A FALSE rule reached the brief path in ten minutes** — a seat's self-reported mechanism promoted
   to standing practice without verification; retracted by that seat 14 minutes later. **The brief
   path now demands an EVIDENCE BASIS on every new section.**
4. **A four-rule correction checklist met its exception in one hour** — rule 5 (a correction must be
   reachable FROM the error) was missing and the seat found it in a throwaway sentence of the brief.
5. Also: a causal inference from two numbers taken with different filters; *"nobody is watching"* when
   the ticket's author had written it down; and a remedy commissioned onto archived parents.

## STANDING (unchanged)
18,609-line hold on #896/#899/#900, **#899 before #900**. Actions dead 19 days — every check is
UNAVAILABLE, never failing; billing is Kam's. Nobody messages Peter or Stuart outside ticket comments.
No merge that makes an external commitment. Never delete — quarantine.
**Kam's writing rules:** the panel speaks the WHOLE message; the **ASK goes FIRST as literal steps**,
or *"no action needed"* in the first line.
