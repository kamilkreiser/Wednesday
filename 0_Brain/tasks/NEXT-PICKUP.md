---
date: 2026-09-08
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Kam ruled the name 11:56). Read Datasec mail by SUBJECT only.
source: replaced WHOLESALE at 18:2x by s151 at its 50% checkpoint (rhythm §2 — NOT a rotation; Kam's band is 80-90%)
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — s151 (Studio) LIVE at 50%. Secuura seat working. Nothing is blocked and nothing waits on Kam.

## 🟢 WHAT HAPPENED SINCE THE 16:01 SHUTDOWN
Kam wrapped the previous seat at 16:01, rebooted the Studio at 17:13, relaunched at 17:46.
**T9 is unplugged and gone to Tuesday's new machine. Tuesday has NOT booted yet.**

## 🟢 SECUURA STATE — re-read from origin by the seat, not copied
    develop  4f612d462   (5c6777658 -> 4f612d462 via #909 this evening)
    main     54b2a5c26   unchanged — negative control run, it did not move
    demo VM  400517aaf   untouched. Nothing deployed this evening.
    next     KS-597, then down the P2 In Review queue by identifier

**#909 MERGED — and this is the evening's finding.** The seat's opening measurement pass found that
**today's own #793 merge (`0e706a57f`, a conflict resolution that took the old side) had REVERTED two
of Kam's audit-baseline rulings** — three advisory expiries rolled 2026-09-24 → 2026-09-10, plus four
dead fast-uri rows resurrected — **re-arming a push gate that would have blocked every author on
Thursday 2026-09-10.** #909 restores exactly what was reverted: key-set identity-checked against
`bf0a4ab99` (the commit before the reverting merge), red-proofed both directions, merge verified by
re-deriving the tree from the COMMIT OBJECT and matching the prediction.

## 🟢 THE KS-577 / KS-843 INTERACTION — RESOLVED, no code, Kam's ruling intact
Kam's 2026-09-06 `logged grace` ruling depended on an overlap that only existed BECAUSE of the KS-577
defect. #880 removes it, so rotating Platform S's key would 401 it instantly — **above the scope gate,
so every S endpoint, not just erasures** — and option A's trigger (*"once the log shows S on the new
key"*) becomes unobservable at the ruled default `grace = 0`.
**Remedy needs no code and no decision from Kam:** set `API_KEY_ROTATION_GRACE_SECONDS` for the
window, or mint with `rotate: false` and retire after the log shows S migrated. **Both ship in #880
already.** Delivered as CROSS-LINKED comments — **KS-843 `82de36ad`, KS-577 `868d1211`**, each naming
the other. **#880's `grace = 0` default is NOT challenged; it is what he ruled.**
Lesson filed M-tier: `2026-09-08_a-ruling-can-be-voided-by-removing-its-precondition`.

## 🟢 THE THREE-SEAT CASCADE DEBT IS CLOSED — ANSWERED, NOT FILED
Measured: **7 open tickets archived as collateral, ALL `Backlog`, FOUR separate archive events, and 7
at every window from 2s to 1h** (the total swings 28→93; the open subset does not).
**Kam had already ruled the class** — `secuura-61-archived-while-still-open` => `three` at 14:00,
unarchive only the In Progress. So all seven stay archived and **no card was filed.**
**Awaiting from the seat:** confirmation that all seven fall inside the 61 he ruled on (his count was
KS-only excluding Duplicate; the seat's population was KS+PS). **If any does not, that one gets carded.**
**Commissioned:** cross-reference comments on KS-489 / KS-488 for **KS-774 and KS-633** — security-review
children reading as defects, which his work-state reasoning did not consider. Findable without unarchiving.

## 🔴 WITH KAM — all have safe defaults, nothing blocks
- `secuura-ks963-widen-to-preauth` (Secuura — default: ships as ruled, which it did)
- `hpsm-credential-bearing-prd-outside-every-snapshot` · `secrev-live-pass-blocked-on-tenant` ·
  `nexusai-rd369-round3-or-ship-at-the-cap` — **all three are TUESDAY's, not this seat's.**
- **PS #783 unreadable:** the PAT 404s on the whole `Secuura/platform-s` repo (control run — not a
  missing PR). Needs platform-s scope on the token. **Kam's.**
- **KS-227 / Peter adjacency, carried not acted on:** KS-227 (Schemathesis no-test-cases gate) is the
  same subject as Peter's open extranet to-do about inline examples on 329 operations. Not urgent.

## 🔴 CLOSED THIS SEAT — do not re-raise
- **F-02 SSH preflight is a FALSE ALARM here and does NOT go to Kam.** Proven: `push --dry-run` then a
  real push, both exit 0; repo-local `core.sshCommand` does the work. **The same instruction was given
  to Kam once on 2026-08-06 and was wrong then too.**
- **The Stuart cutover card was DROPPED, not overridden** — he ruled it 2026-09-06 (`logged grace`,
  chosen *because* it needs no window with Stuart). Do not re-card it.

## 🔴 WEDNESDAY'S OWN ERRORS THIS SEAT — all in `_ledger.md` (223 rows)
A W-tier lesson filed this morning rested on an **unmeasured 200K window** and would have made every
seat under-read its own ledger — corrected by measurement, digests regenerated. Then: a **causal
inference from two numbers taken with different filters** (39 vs 40 In Review), agent-caught in four
minutes. Then: telling Kam an interaction was one **"nobody is watching"** when KS-843's author had
written it down explicitly — an absence-of-attention claim made from a partial read.

## 🟢 BOOT NUMBERS (WED-139) — and the boot spec is FINE
digest 311,130 B / 4,129 lines read WHOLE · ledger 09-08 + 09-07 whole, 09-06 as headlines ·
**ctx 7% → 21% after the digest → 36% at end of boot.** The whole boot fits comfortably; the
"it no longer fits" lesson was wrong and is corrected.

## STANDING (unchanged)
18,609-line hold on #896/#899/#900, **#899 before #900**. Actions dead 19 days — treat every check as
UNAVAILABLE, never as failing; billing is Kam's access alone. Nobody messages Peter or Stuart outside
ticket comments. No merge that makes an external commitment. Never delete — quarantine.
**Kam's writing rules, both from today:** the panel speaks the WHOLE message, and **the ASK goes
FIRST as literal pasteable steps** — or "no action needed" in the first line.
