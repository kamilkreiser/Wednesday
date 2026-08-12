---
client: Datasec
project: Vision_Sales_Portal
path: /Volumes/DevMASTER/!CODING/Datasec/Vision_Sales_Portal
status: active
updated: 2026-08-12
---

# Datasec / Vision_Sales_Portal

**Last session (2026-08-12):** Whole morning brief shipped. QuickQuote stage3
v0.3.2: OTP send failures surface honestly (502 in 4s grace window, mail
health on /healthz, retry w/ jitter) — proven by live forced ACS failure +
recovery. Log capture fixed both layers (filesystem 7-day + Log Analytics
`hpas-quickquote-logs` 30-day via diag setting). Page-1 print overflow fixed
at ROOT CAUSE (v2.19): the compact @media print block was dead CSS (cascade
order); restored, verified with real PDFs incl. live emailed PDF (2 pages).
CI split (stage3 suite needs npm ci; bare node --test was failing runners).
Branches open-signin + pricing-engine deleted (merged; your "8 ahead" card
was stale — corrected). WED-90 launcher tee implemented + dry-run proven.
Live image `v0.3.2-tool2.19` = main @ 637d788. Vision portal itself untouched.

**Open / next:**
- Verify Actions green for b7043cf/637d788 (blocked: no datasecau gh auth on
  this machine — one-time `gh auth login` in a launcher shell, Kam)
- WED-90 two real-launch exercises (warning-present, then clean)
- Uncommissioned BACKLOG: hosted sign-out control, QA F3 headers, mail-spray
  per-IP budget, session swap-durability test, FX provenance in emailed PDFs

**Blockers:** none for commissioned work.

**Notes for Wednesday:** Kam-gated list unchanged: sales@ delivery confirm ·
WIL-54 chip currency · custom sending domain (lifts the ~30/hr ACS OTP cap —
load-bearing since open sign-in) · margin-visibility revisit. Deploy gotcha
for any session touching the webapp: after a container swap /healthz may
briefly answer from the OLD process — poll until the mail block resets.
