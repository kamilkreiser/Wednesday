---
client: Datasec
project: Vision_Sales_Portal
path: /Volumes/DevMASTER/!CODING/Datasec/Vision_Sales_Portal
status: active
updated: 2026-08-11
---

# Datasec / Vision_Sales_Portal

**Last session (2026-08-11):** HPAS QuickQuote Stage 3 — shipped OPEN OTP sign-in
(allowlist removed, OTP to the entered address for any entrant) + requester-tagged
quote mail (v0.3.0), and F2 unlock lockout (v0.3.1), both live on
hpas-quickquote and merged to main @ d5bdd00. Kam released the cold-acceptance
hold and ruled advanced/HPAM mode a workflow nudge, not a security control — F2
closed, HPAM word stays by design (no rotation). Lockout + open sign-in + margin
boundary all wire-verified LIVE; F2's attempt-budget-reset path is unit-only.

**Open / next:**
- Confirm ACS quota recovered + OTP delivery working; set up custom Datasec
  sending domain (DNS) — escalated to Kam as load-bearing under open sign-in.
- Confirm sales@datasec.com.au receives the BCC quote copies (only Kam/sales can).
- Next deploy (any reason): confirm reworded advanced-unlock boot log went live.
- Optional (needs authz): delete merged branch stage3/open-signin.

**Blockers:** ACS managed-domain hourly send cap caused a live OTP outage from
~01:00Z (real users get no code); self-clears, custom sending domain is the fix.

**Notes for Wednesday:** F2 rotation step I sent earlier is CANCELLED (Kam ruled
by-design). Honest position, recorded in BACKLOG: margin/buy prices are reachable
by any visitor who knows the guessable word — "F2 closed" ≠ "margin protected".
Boot-log reword is committed but rides the next deploy (Kam: no swap for a log
string) — pending-cosmetic, not live yet.
