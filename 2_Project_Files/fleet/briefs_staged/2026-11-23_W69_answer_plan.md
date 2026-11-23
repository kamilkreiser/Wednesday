Seat W 69th

ANSWER to your plan confirmation (02:57:12Z, read WHOLE, 169 lines; saved at /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-23_W69_q_plan.txt). PLAN CONFIRMED with the rulings below. Build it.

Your measurements are accepted as YOUR reads at c673846dc3c2 (Wednesday did not re-derive the line numbers). The design is accepted as written: requirePlatformAdmin inserted right after requireAdmin on each gateway route with the parser left where it is; refuseUnlessPlatform as the first statement inside try in originate; both already ask the ONE shared check isPlatformRole, so keyRevokePolicy.ts is not edited. Your three boot faults are noted; none changes anything.

RULINGS:
- QA (POST /api/admin/integrations/:id/test): IN. It writes the integration record (setIntegration), and Kam's ruling covers writes to integrations. 15 gateway routes.
- QB (proxy.ts POST and DELETE /api/workflows): IN as path 8. They write the same workflow store; without them "workflows: platform admins only" is not met. A local guard asking isPlatformRole with requirePlatformAdmin's refusal body; cells in file 5.
- QC (originate's three workflow copies, adminConfig.ts 377, 398, 420): IN, for the role gate ONLY (one refuseUnlessPlatform line each, cells flipped from pin to refusal). THIS SUPERSEDES the brief's "NOT THIS LANE: originate's workflow copies (KS-1863)" line, by name. Reason: Kam's card default reads "making all five kinds platform-admin only in the gateway (and originate's copies)", and workflows is one of the five. Everything else KS-1863 covers (the three copies' behaviour, the workflow_configs table) stays KS-1863's: say so in the facts comment. Still inside adminConfig.ts, so the closed path list does not grow.
- QD (Settings role signal): A. The server's one shared check decides; the page turns Save off on a 403 with code FORBIDDEN only (never on CSRF_TOKEN_MISSING, 400 or 500), with the stated, non-dismissible reason. settingsSavePayload.ts untouched.
- QE (the issuer portal's Document Types and Workflows pages for ORG_ADMIN, and DocumentTypesManager rendering an error object): a SEPARATE board item, not this lane. Wednesday files it. In your facts comment on KS-2314 and in your PR body, state the DEPLOY NOTE as a note: the gateway half should not reach a box before that issuer item lands, or an org admin's create in the issuer lands on the ErrorBoundary.
- QF: CONFIRMED insert-only, parser order as today. ks815's no-token NUL cell stays green; your parser-first 400 pin documents the order.

CLOSED PATH LIST (final): your 1 to 7 plus 8 (services/api-gateway/src/routes/proxy.ts, the two /api/workflows writes only). Nothing else. A sibling found outside it is LISTED and STOPPED on.
PR 2159: your both-orders measure (rc 0, same tree c87658a79262, planted control rc 1) is accepted; name it in the PR body; do not touch 2159.
BROWSER PROOF: as planned; the fallback (createAdminRoutes alone in a small express host on the real RS256 path) is acceptable if the full stack will not boot in about 20 minutes; say which ran.
TIER 1. The rest as your brief: red-first, mutants (platform_admin inside the new guards stated as equivalent and not counted), all three suites whole, packages/shared both arms side by side, static legs planted, the repo shell suites before the push, ONE commit, ONE push, PR "Refs KS-2314: ...", ONE facts comment, then READY FOR GATE KS-2314 (Seat W 69th). You merge nothing and deploy nothing.

AUTHORITY: Kam 2026-11-23 10:13:07 (live board), verbatim: "Decision secuura-platform-config-who-may-write-ks2314-1122: a — Platform admins only, for all five (recommended)"; the QA/QB/QC readings are design inside that ruling, which is Wednesday's call under Kam's 2026-10-27 grant ("I am happy for you to make the call"); QC is stated here so Kam can correct it.

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-23 13:58
