# QA GATE, TIER 1: Datasec/HPSM Policy Composer — ACCEPTANCE vs THE ORIGINAL BRIEF + SECURITY, LIVE-ONLY DELTA AFTER THE GATE FIX @ caf63fd (new class, round 1) — LIVE SITE ONLY

**Commission.** Tuesday, 2026-09-13, relaying Kam. The caf63fd gate (2026-09-13) returned **DELIVERABLES: NO GO · SECURITY: GO WITH FINDINGS**, blocked on the live demo by **D-B1**: the Caddy gate required HTTP Basic in `Authorization` on every path, the API and SPA send only `Authorization: Bearer`, so nothing after sign-in worked through the public URL. The builder reports a gate-config fix ("b-tight"). This gate re-runs on LIVE only the half that D-B1 blocked, and verifies the fix itself. Kam reviews the platform Monday 2026-09-14 and is testing it himself tonight.

**Head:** live Composer `caf63fd54c3ad95384bcb7bc32d4e7b9e4a6f5c4` (web bundle `index-DL3hPt3N.js`, api `0.13.2`), local `main` of `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer`.
- **A rolling upgrade to a newer head is expected tonight.** Tuesday re-points the launcher's HEAD_SHA / EXPECTED head / REPORT_DIR / SUBJECT before launch; the launcher refuses unless HEAD_SHA is reachable from `refs/heads/main` and prints the four variables under `--check`.
- **Your verdicts are about the head the LIVE site actually runs.** Record START/MID/END live head readings; if the head changes mid-run, say which results belong to which head.
- **TWO verdicts, each GO / GO WITH FINDINGS / NO GO: `DELIVERABLES (LIVE)` and `SECURITY (LIVE)`.**

## Prior gate (this is a delta, not a fresh gate)
- **PRIOR ROUND:** the caf63fd gate (new class "acceptance vs brief + security", round 1) returned **DELIVERABLES: NO GO · SECURITY: GO WITH FINDINGS** (1 Blocker · 2 Major · 10 Minor · 4 Polish / 0 · 0 · 3 · 1).
- **ITS REPORT IS ON DISK AT:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-caf63fd-brief-acceptance-security-tier1/report.md` — read it first: BLUF, D-B1, the SECURITY attack-plan table, "Detail: the LIVE pass", and "NOT TESTED → On LIVE — blocked by D-B1" define exactly what this delta must now run.
- **Carried forward, to re-check on live (present or changed, NOT re-litigated):** D-B1 (the fix), D-M1, D-M2, S-m1, S-m2, S-p1.

## Charter (read first, in full)
- **Charter:** `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`. Rule 1 (FAIL condition first) and Rule 2 (NOT TESTED is output) govern every row.
- **Deliverables:** walk the build against the original spec, requirement by requirement, on the LIVE site, looking for anything missing, partial or falsely claimed.
- **Security:** attack the live site as a hostile tenant, a hostile role and a careless consultant, looking for isolation, secret, integrity and disclosure failures.

## 1. Target — LIVE ONLY
- **URL:** `https://hpsm-composer-demo.australiaeast.cloudapp.azure.com`. HTTP Basic auth on the gate, synthetic data only. **It is Kam's demo for his Monday review, and KAM IS TESTING IT HIMSELF TONIGHT.**
- **LIVE DEMO RULING: APPROVED by Kam 2026-09-13 18:20** (scope exactly as below; nothing beyond it).
- **Environment:** live Azure demo, synthetic tenants, non-prod product data. No local stacks, no clone, no docker in scope this pass (all local-only work is out of scope — see below).
- **The builder's b-tight claims (2026-09-13 10:51:00Z REPORT mail, relayed by Tuesday) — these are CLAIMS TO VERIFY, not facts:**
  - The Caddy gate now runs config "b-tight": HTTP Basic stays on **every** path EXCEPT `/api/*` paths that contain no `..`, `%2e`, `%2f`, `%5c` or backslash (case-insensitive).
  - `/api/healthz`, `/api/openapi.json`, `/idp/*`, `/`, the web app, `/mail/`, `/objects/`, `/worker/` **stay behind Basic**.
  - The app's `/api` calls carry `Authorization: Bearer` and pass the gate to the API's own bearer check.
  - Applied live at 10:49:58Z; live head still caf63fd. Builder measured on the public URL: a real browser signs in and loads the dashboard and one engagement; 26 unauthenticated curl rows.
- **The site may be upgraded while you test** (rolling fix upgrades tonight, each with a few minutes' restart). On repeated 5xx or refused connections, pause ≤ 15 min and re-check before stopping the live pass; **record every head change (START/MID/END heads) and say which results belong to which head.**
- **Head readings:** record what the live site runs at START and END (version/health after sign-in, plus the content-hashed bundle name and `/api/healthz` version), and compare with the head Tuesday's launch prompt names. A difference is RECORDED and named in the BLUF. If mid-upgrade (version flipping, repeated 5xx), STOP the live pass and say so.
- **Your own tenants, and only yours:** create ONE synthetic tenant `QA Harness (synthetic) <YYYY-MM-DD HH:MM>` through the product's own admin flow, and do ALL mutating work inside it. For the cross-tenant must-fail probes, create a SECOND harness tenant `QA Harness B (synthetic) <YYYY-MM-DD HH:MM>` and attack ids it created **using the first harness tenant's own sessions** — never Kam's tenant or engagements.
- **KAM'S TENANT IS NEVER TOUCHED.** "Synthetic Customer B (demo content)" and every engagement in it (including `3bb6fcb2…`, `a9101d3f…`) are NEVER read-probed, edited, approved, released or exported. Cross-tenant attempts run only against your OWN second harness tenant's ids. The first cross-tenant read/write that unexpectedly SUCCEEDS stops that probe at once; report it as a Blocker with what changed.
- **Cleanup on LIVE:** delete nothing, never by DB. Leave both QA tenants in place and list EVERYTHING you created (names, ids, times) in the report, so Kam can see it.
- **Evidence class:** live results are MEASURED AT RUNTIME (LIVE); an adjacent call is PROBED; source/config/docs is READ ONLY. Every row and finding carries its class.

### Limits on LIVE (unchanged from the original)
- Sequential requests only, ≥ 1.1 s apart (≤ 1 request/second sustained).
- No body over 1 MB except ONE attachment probe at the product's own stated limit.
- At most **3 wrong-credential attempts in the whole run**.
- No path brute-forcing: a fixed list of ≤ 30 paths.
- No ssh, no `az`, nothing on the VM itself.
- **STOP the live pass and report at once** if any request returns 5xx twice in a row, the site stops answering, or response time exceeds 10 s on 3 consecutive requests.

## 2. Spec / DoD — REFERENCE DOCUMENTS (read-only; every row cites document + § + line)
- **AUTHORITATIVE, the original brief (spec v1.1):**
  - `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/Datasec_HPSM_Cloud_Policy_Composer_Detailed_Scoping_Design_Specification_v1_1.docx`
  - Text: `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/_extracted/spec.md`
  - Lines: §3 L173, §5 L227, §7.1 L283, §8 L316-478, §9 L479, §10 L512, §12-§17 L606-794, §18 L796, §19 L809, §20 L824, §21 L863, §22 L880-917, §23 L919-947.
- **AUTHORITATIVE, Kam's commission and four scoping answers:** `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-09-10_hpsm-phase1-architecture.md` L8-29.
- **LAYOUT/STYLE TARGET (A-54):** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/HPSM Policy Composer - Screens.pptx`
- **FORMAT ONLY, not values (A-02):** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/Policy Preview.pdf`
- **CONTEXT ONLY, not the brief (A-06):** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/_extracted/sow_e8.md`
- **RULINGS THAT CHANGED THE SPEC.** An intentional change is not a gap; contradicting a ruling is a finding. All under `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer/`:
  - `README.md`
  - `2026-09-10_policy-composer_ARCHITECTURE.md`: A-01..A-54 L54-131; Q-01..Q-20 L149-168; §2.4 L607; §2.5 L614; §2.6 L619; §3.2-3.3 L665-721; §4 L747; §5.1 L764; §6.1 L826; §6.3 L855.
  - `2026-09-10_source-measurements.md` §7 L193-208.
  - `2026-09-10_screens-MEASURED.md`
  - `2026-09-10_seed-data-CONTRACT.md`
  - `2026-09-13_output-export-request-S40.md`: Export PDF and stored per-client outputs.
  - `qa-wp4/README.md` L20-27 (WP4 DoD), L31-61 (rulings (a)-(h)).
- **NOT THE BRIEF, never test against:** the HP SOW-01 Security Playbook `.docx` at the root of `.../Source_Documents/`; `Source_Documents/HP Playbook Project/Shared with HP/`.

## 2a. LEGITIMATE SHAPES
Not a checker. Pair every refusal probe with the ordinary input that must pass. A guard that refuses ordinary use is a finding. The b-tight gate IS such a guard: for every Basic-protected path you probe, also prove the ordinary signed-in flow through it still works.

## 3. Scope — a LIVE-ONLY DELTA (new class "acceptance vs brief + security, LIVE half", round 1)
Run in this order.

### 3.1 Verify the gate fix itself on LIVE (FIRST)
The builder's b-tight claims above, clause by clause. FAIL first, with controls.
- **Positive control:** a signed-in request to your OWN harness tenant succeeds (200 with your data) — the D-B1 collision is gone.
- **Negative controls:** every Basic-protected path challenges without credentials (`/`, the web app, `/api/healthz`, `/api/openapi.json`, `/idp/*`, `/mail/`, `/objects/`, `/worker/`); traversal variants (`..`, `%2e`, `%2f`, `%5c`, backslash, mixed case) aimed at `/idp/*` and `/api/openapi.json` challenge (do NOT let a traversal skip Basic); `/api/*` without a bearer answers the **API's own 401 Bearer**, not data.
- **FAIL if:** any Basic-protected path answers without the challenge; a traversal variant bypasses Basic; `/api/*` without a bearer returns data instead of the API 401; or the signed-in positive control fails (D-B1 not actually fixed).

### 3.2 The deliverables walk-through on LIVE that D-B1 blocked
Inside `QA Harness (synthetic)` only, through the product's own flows, exactly as the original brief §1 described: engagement create, discovery, generate, validate, exceptions, both approvals, release (on a zero-device-group engagement if release is reachable at the live head), **Export PDF and stored outputs**. Confirm one policy per engagement; the forbidden route answers 405. **Measured workaround for a live release (gate C, KNOWN in flight):** link the approvers through the API, and define the 8 local values through S6 decisions (W5-M1, W5-M2).

### 3.3 The security probes that needed a signed-in request, on LIVE
Confined to your own harness tenant, or run as must-fail cross-tenant attempts against your SECOND harness tenant:
- **1** — AuthN bearer classes (no/expired/wrong aud-iss/alg:none/expired membership); control: a valid token 200.
- **2** — roles: 7 × ops; platform_admin never approves; self-approval only with the flag; auditor read-only.
- **3** — API isolation: every id-taking op incl. stored outputs, links, audit search, directory, Admin, id case variants, cross-tenant clone (A-29) → anything but a 404 identical to a nonexistent id is a FAIL.
- **5** — secrets: `SECRET_VALUE_ENTERED_IN_CLOUD`; credential-shaped text in every free-text field (ruling (a), 422); grep every reachable output for the marker.
- **7** — integrity: same inputs → same hash; a change after approval voids it; released rows immutable; 503 for JWS/evidence ZIP/package manifest; "Not signed".
- **9** — files: intake, Content-Disposition injection, link expiry and user+tenant binding, replay, key traversal.
- **11** — injection/XSS/CSRF-equivalent: payloads in text/filters/sort; XSS in web and PDFs; tokens in cookies/URLs; state-changing GET; credentialed CORS.
- **12** — synthetic fence: ON/OFF × real/synthetic × create/clone/release; only exact `true` turns ON.
- **13** — platform tenant: 3 fields, platform_admin only, excluded from lists, refuses sessions (incl. case variants).
- **15** — error leakage: the AUTHENTICATED error classes (the unauthenticated ones were done at caf63fd; do the signed-in ones now).
- **17** — the SECOND control only: "a signed-in request to your own tenant succeeds" (unmeetable at caf63fd; meetable now if the fix holds).

### 3.4 Re-check on LIVE the original findings live can show
Confirmed present or changed, **not re-litigated**:
- **D-M1** — a policy releases with 0 of 26 discovery answers while the gate records `all_required_discovery_complete: true`.
- **D-M2** — an exception with no compensating control and no evidence is accepted/approved/released (read-only confirmation on the harness tenant; do not create governed risk in Kam's tenant).
- **S-m1** — browser security headers missing at the live edge (nosniff, frame-ancestors/XFO, HSTS, JSON no-store); CSP is KNOWN.
- **S-m2** — internal services on the public edge (Mailpit UI/API, MinIO S3 API, worker health, idp issuer).
- **S-p1** — idp-mock error internals; `/favicon.ico` serves the HTML shell.

### Out of scope (local-only in the original — do NOT run this pass)
Probes 4 (DB/RLS as pc_app), 6 (superuser audit tamper), 8's local edge half, 10 (repo/dependency scanning), 14 (size/rate/flood), 16 (egress); clean-clone CI; any mutant, fixture, seed or DB script. The local half stands from the caf63fd report FOR caf63fd ONLY. If the live head you record is newer than caf63fd (a rolling upgrade is expected tonight), the local half at that newer head is NOT covered by this pass or by the caf63fd report: Tuesday commissions it as a separate delta gate. Record it under NOT TESTED as out of scope, never as passed.

## 4. Credentials (POINTER ONLY — these ARE the credentials; nothing is missing)
Kam, tonight: *"make sure that you include the credentials in the testing document harness."* They exist and are named here by PATH only.
- **The gate credential (HTTP Basic for the Caddy gate):** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/4_Credentials/hpsm-demo-site.txt` — read into process memory ONLY. Never print, copy, log, screenshot or mail its value.
- **The public browser-check env:** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/4_Credentials/gate-check-public.env` — may be read into memory the same way, same rules.
- **Synthetic personas:** the idp-mock's seeded users, the seven spec roles plus `consultant-2`, `customer-approver-a`, `customer-approver-b` (`apps/idp-mock/src/app.ts`); tokens come from the gated `/idp/token`. These are the login identities for the deliverables walk-through and the role matrix.
- **Read NOTHING else** under `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/4_Credentials/`. The identity dirs there are exported only for isolation. Run no `az`, no `gh`.
- **Before mailing:** grep your WHOLE report folder (report + evidence) for the gate credential's value, with TWO positive controls (the in-memory matcher fires on a buffer holding the value; the file walker finds a non-secret marker in a real file), and record that the grep ran. Values never recorded.

## 5. State-mutation & cleanup
- **LIVE sanctioned:** ONLY your two `QA Harness (synthetic) …` / `QA Harness B (synthetic) …` tenants and what you create inside them. Nothing is deleted on live.
- **Reachable on live (harness tenants):** draft, generated, validated, review, approved, released synthetic (zero device groups), a second version, a clone.
- **Never `rm`.** Quarantine, never removal. `${X:?}` on every expansion. Any scratch state goes in a fresh `mktemp -d`.

## 6. Output boundary / 6a. Evidence class
- **Findings, reports and recommendations ONLY.** Describe the fix-shape and the regression test in prose. Never fix, commit or file tickets.
- **Evidence class on every finding and every row:** MEASURED AT RUNTIME (LIVE) / PROBED / READ ONLY. A recommendation with no evidence class is incomplete.

## 7. Known-fragile / known-changed (a mismatch is a finding; a KNOWN item is not re-reported as new)
- **KNOWN, fix in flight (gate C/B round 1; present at caf63fd):** W5-M1 (website-created engagement cannot be customer-approved — approver user_id null); W5-M2 (demo release silently blocked until 8 local values are defined); W6-M1; W4B-m1 (`urn:uuid:` → 500); W4B-m2 (stale-pinned engagement accepts a customer approval); W4B-m3 / A-m1 (credential-shape residue in free text). Report these as "KNOWN, fix in flight" with the gate id; if a later upgrade closed one, VERIFY it closed.
- **KNOWN (do not flag as new):** F6 "provisional" not "synthetic"; release blocked with a device group (build-c11, NOT deployed before Monday); root MinIO credential; no CSP anywhere; storeOutput has no idempotency key; per-process link key; no re-pin (409 CONTENT_VERSION_CHANGED); the platform id is a literal.
- **Rulings in force:** Q2(a) no signing key; S32-B no unsigned released ZIP/manifest/JWS ("Not signed"); Q5-Q8 outputs carry client, engagement, generated-by name+role, no email; Q9 platform_admin sees id/name/created_at only; WP4 rulings (a)-(h).
- **Still owed:** a KNOWN item that silently gives a WRONG RESULT, or a security gap reachable in MVP A, IS a finding — mark it "KNOWN, re-rated" with its backlog line.

## 8. Logistics
- **One session, one tmux pane.** `cockpit.sh add 'QA/HPSM-live-delta' "bash '<launcher>'"`, never nohup. Never end a turn waiting on a background notice: a turn that ends to wait is the end of your session. Long commands in the FOREGROUND.
- **Order:** verify the gate fix (§3.1) → deliverables walk-through (§3.2) → signed-in security probes (§3.3) → re-check carried findings (§3.4). Anything unfinished is NOT TESTED, with the reason.
- **Head readings** of the live site at START, MID and END: version/health + bundle hash + time; and of the original repo (SHA + branch + time). If the head changes, say which results belong to which head.
- **No inbox.** Where the brief is silent, take the safest reading and record it. Approval-class work (live demo beyond §1, money, external comms, anything irreversible) is not done; list it under NOT TESTED.
- **Report:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-<head7>-live-delta-after-gate-fix-tier1/report.md`, in the original report's structure: **BLUF** (both verdicts + severity counts); **Frame**; **findings** (FOUND / TESTED / HOW, oracle, evidence class, Blocker/Major/Minor/Polish with justification — priority is the humans' call); the traceability for the LIVE rows; the security table with each control's result; **NOT TESTED**; **Corrections**; head readings START/MID/END.
- **INTERIM mail** for any Blocker at once (e.g. the fix did not hold, or a cross-tenant attempt succeeded).
- **MAIL YOUR VERDICT** to `tuesday-agent@agentmail.to`:
  - subject `[QA/Datasec-HPSM -> Tuesday] GATE VERDICT — Policy Composer LIVE delta after gate fix @ caf63fd (tier 1)`;
  - first line `DELIVERABLES (LIVE): <GO | GO WITH FINDINGS | NO GO> · SECURITY (LIVE): <GO | GO WITH FINDINGS | NO GO>`.
  - **Datasec's coordinator is TUESDAY. Never `wednesday-agent@`.**

PROVENANCE:
- Kam's commission + credential instruction | Tuesday, 2026-09-13, relaying Kam | read 2026-09-13
- builder's b-tight claims + apply time 10:49:58Z, live head caf63fd | builder REPORT mail 2026-09-13 10:51:00Z, relayed by Tuesday | read 2026-09-13
- D-B1 and the carried findings, live-pass shape, NOT-TESTED-on-live list | caf63fd report `.../2026-09-13-composer-caf63fd-brief-acceptance-security-tier1/report.md` | read 2026-09-13
- reference paths, rulings, KNOWN | original brief `.../2026-09-13_hpsm-composer-09c1591-brief-acceptance-security-tier1.md`; combined brief L46-74 | read 2026-09-13
- personas (7 roles + consultant-2 + customer-approver-a/b) | `6_Policy_Composer` @ caf63fd `apps/idp-mock/src/app.ts` | read 2026-09-13
- live head reachable from main; credential files present by name | `git merge-base --is-ancestor`; `ls 4_Credentials/` | read 2026-09-13

SELF-CHECK: re-read end-to-end for contradictions; scope is LIVE-only, local probes explicitly out | 2026-09-13
