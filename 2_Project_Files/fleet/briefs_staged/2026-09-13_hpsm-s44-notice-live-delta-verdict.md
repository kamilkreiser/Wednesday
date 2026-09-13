BLUF. **The live-only delta gate at 87c0026 returned DELIVERABLES (LIVE): GO WITH FINDINGS · SECURITY (LIVE): GO WITH FINDINGS.** Verdict mail 12:17:51Z (DKIM pass); Tuesday read the report whole. **No question: this is for your queue and records.**
- Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-87c0026-live-delta-after-gate-fix-tier1/report.md`
- Live head constant 11:29Z-12:11Z (api 0.13.2, bundle `index-GroKuQ3K.js`), so every result belongs to 87c0026. Your step-8 roll lands after its END reading.

## Confirmed on LIVE (credit to your round)
- **D-B1 RESOLVED:** b-tight holds. A bearer alone reaches the API; 9/9 Basic paths challenge; every traversal toward `/idp`, `/objects`, `/mail` and openapi challenges; no disclosure.
- **Full walk-through to release 1.0.0** in the QA Harness tenant, with Export PDF and stored outputs (OUT-4 fields, no email, "Not signed").
- **W5-M1 CLOSED** (422 APPROVER_NOT_A_TENANT_MEMBER, then a linked approver approves).
- **W5-M2 resolved** (LOCAL_VALUE_NOT_DEFINED is explicit and definable; release reachable).
- **W6-M1 / renderers:** every output kind renders.
- **Security probes 1/2/3/5/7/9/11/13/15/17 PASS with firing controls:** no cross-tenant success, 404 byte-identical.

## Still present (already queued, no new work)
- **D-M1 (MAJOR):** released with 0/26 discovery answers while `all_required_discovery_complete: true` (`validate.ts:274`, the tester's citation). It is on your engine queue.
- **D-M2 (MAJOR):** 24/24 exceptions with no compensating control or evidence → 201 → approved → released (`inputs.ts:61-75`). It is on your engine queue.
- **W4B-m3 / A-m1:** 4 of 8 credential shapes accepted in free text. Credential round.
- **W4B-m1:** `urn:uuid:` → 500 on live 87c0026. FX-ID closes it at the step-8 roll; the post-check may confirm it.
- **S-m1, S-m2, S-p1:** unchanged. BACKLOG as the one post-round edge commit.

## NEW — S-p2 (POLISH, no disclosure)
- A **trailing** `/api/…%5c` (e.g. `/api/openapi.json%5c`, `/api/x%5cy/openapi.json`) reaches the API's public 404 instead of the Basic challenge.
- Nothing is served, and any real route still needs a bearer: the documented b-tight trade-off.
- It deviates only from the literal claim "every `%5c` stays behind Basic".
- **Routing:** BACKLOG it beside S-m1/S-m2 under the durable gate redesign (the Caddy gate is VM-only state with no repo record). **No live gate change tonight;** any change to the live Caddyfile still needs Kam's word.

## NOT TESTED on live (no browser) — owed
- The rendered web fixes FX-SI, FX-REL and W5-M3.
- The probe-12 negative half.
- W4B-m2.
- **The local half at the newer head is owed as ONE delta tier-1 gate after your READY FOR QA** (Q + W + fixes on 09c1591..<fix head>).
