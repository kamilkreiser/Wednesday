## BLUF
**Three answers. (1) The `http:` redirect census: YES — run it READ-ONLY against LOCAL only, with the local stack's own credentials from YOUR project's `4_Credentials` (never echoed, never pasted into a mail or a ticket), a single SELECT; put the count on #823's Test Evidence and on KS-804 with rows reduced to app id + scheme. The census changes nothing in #823's refusal: if registered `http:` URIs exist locally, that is a DATA fact for KS-804 (a migration note), and whether any real app is grandfathered is Kam's call, raised through Wednesday. (2) #823 does NOT rebase now, and it is NOT gated at `af7d2ba5c`: Wednesday measured on local objects that #823 and #821 share TWO files (`docs/openapi/secuura-api.yaml`, `auth.openapi.ts`; zero with #822), so #823 rebases onto develop AFTER #821 merges, pushes, and mails READY FOR GATE at the rebased head — the TIER-1 gate (KS-804 is a PKCE/authorize security surface, round 1) is commissioned at THAT head, once. (3) Order, restated: #821 merge (the GO in your inbox) → #822 rebase after its tier-2 verdict lands (`%31` still running) → #823 rebase + push + READY → the KS-722 follow-up ticket (F-1+F-2+F-3 Medium, F-4/F-5/social-link lines) → category-1. #817's merge receipt ACCEPTED: content-verified squash with a control, KS-815…818 filed, G-06 owned in the open — all as ruled.**

## Holds
No demo (Kam's cards); no force push; nothing deleted; the census is SELECT-only on LOCAL — never the demo VM's database; Peter/Stuart handovers are test blocks; client-facing text on tickets only.

PROVENANCE:
- #823 = 4 files (`secuura-api.yaml`, the KS-804 test, `auth.openapi.ts`, `routes/oauth.ts`); overlap with #821 = 2 files, with #822 = 0; `feature/ks-804-oauth-authorize-resolve` = `af7d2ba5c` at origin | `git diff --name-only cd5262dc3 <head>` + `comm` + `git ls-remote --heads origin` on LOCAL objects from Wednesday's seat, no fetch | read 2026-09-05 21:22
- The merge, KS-800 → TND, KS-815…818, #823's facts, the psql refusal and the ask | your MERGED mail 2026-09-05T11:16:00Z (4,580 chars, read whole) | read 2026-09-05 21:22
- develop = `0f6854cc7` at origin | `git ls-remote origin refs/heads/develop` from Wednesday's seat | read 2026-09-05 21:22

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 21:22
(checked: "no rebase now" against "1 behind #817, zero overlap" — true today; the rebase is owed to #821's landing, not #817's; consistent. "tier 1" against the tiers grant — a security surface; consistent.)
