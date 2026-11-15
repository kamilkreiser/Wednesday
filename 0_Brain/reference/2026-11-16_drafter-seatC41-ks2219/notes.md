# Drafter notes, Seat C 41st, KS-2219 (2026-11-16 04:2x AEDT)

Brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-16_seatC41_ks2219_billing_byemail.md (31,416 bytes, STAMP blank, model claude-sonnet-5-5, tier 2 / G2).

## Measured (read-only, GitHub API and Linear GraphQL; nothing run)
- develop 42e242166f892e44b71c9f05d386215e3d7cf06a (2026-11-15T17:12:15Z), unchanged at 04:23:17 AEDT; PR 2245 (C 40th) merged 17:12:16Z. The commission's "develop 42e242166f89" matches.
- KS-2219: Backlog, priority 4 (Low), 0 comments, no labels, created and updated 2026-11-15T11:56:44Z. Output in _work/ks2219.txt (key read in-process, never printed).
- Route at develop: by-email handler reads `req.query.email as string`, `!email` check only; catch answers 500 with no classifier call; classifier at line 53, wired in 7 other places plus POST /customers. billing.openapi.ts already declares 400 and 503 for the operation (no openapi change).
- Open PRs: 68 (352 file rows, 0 errors). services/billing only in Dependabot 575 and 649 (package.json). Control services/transfer = 4 rows. PR 2093 touches originate only. K 32nd staged brief absent at read.
- Prior work: no commit gave by-email an error mapping or input check (git -S on the stale shared checkout plus commits API at the pin). No existing cell among ks445, ks431, payment-methods mentions by-email or "Failed to find customer"; ks1888 mentions by-email 7 times (table row, KS-1911 E0 to E3), none asserting a 500 (read by grep, not whole file).
- Ordinals in history.md: C 41st 0, C 40th 1, C 39th 2 headings. load1 3.25 at 04:24.

## Differences from the commission worth Wednesday's eye
- The commission said "Low": Linear priority 4 is Low (consistent).
- The shared checkout (2_Project_Files) is stale (origin/develop 0e6479d7b6c0, 2026-11-10): prior-work -S there is partial; the API commits list covers the gap. No scratch clone was made (API reads sufficed); _work/ holds the fetched files.
- Design stated in the brief: non-string email (array or object) -> 400 before the provider; classifier three-argument form in the catch.
- Gate row: I named G2 (mechanism = KS-431/445 classifier, already gated); the commission said "tier 2". Wednesday's stamp confirms.
- A docs-fragment pair is left as a seat MEASUREMENT (not asserted either way).

## UNMEASURED
Every suite count and every red/green label (predictions from reading); whether tsconfig for billing excludes tests; whether check:test-types lists billing; whether the docs check demands a pair; other billing routes with bare `as string` casts; real Stripe behaviour; K 32nd's merge queue content (brief absent); full content of ks1888 beyond the grepped lines and the table/E-cells read.
