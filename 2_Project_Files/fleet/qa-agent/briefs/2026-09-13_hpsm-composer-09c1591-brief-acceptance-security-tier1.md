# QA GATE, TIER 1: Datasec/HPSM Policy Composer - ACCEPTANCE vs THE ORIGINAL BRIEF + SECURITY @ 09c1591 (new class, round 1) — LIVE SITE + LOCAL STACKS

**Commission.** Kam, 2026-09-13 17:00 AEST: *"...test the platform from a security perspective as well as from a deliverables perspective against the original brief. Include links or the paths to the original briefing documents so that the testing agent can reference these during its testing."* He reviews the platform Monday 2026-09-14.

**Head:** `09c15918fadfee8a9bd590a1282113637f44515d`, local `main` of `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer`.
- `afc10e9..09c1591` is 249 commits, NOT pushed; HPSM-light `origin/main` = `afc10e98c51505be1f1943335370cf2de3b47d44`.
- The launcher refuses unless the head is reachable from `refs/heads/main`.
- **Your verdicts are about 09c1591 only. Main may move; a later head needs a delta pass.**
- **TWO verdicts, each GO / GO WITH FINDINGS / NO GO: `DELIVERABLES` and `SECURITY`.**

## Charter (read first, in full)
- **Charter:** `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`. Rule 1 (FAIL condition first) and Rule 2 (NOT TESTED is output) govern every row.
- **Deliverables:** walk the build against the original spec, requirement by requirement, looking for anything missing, partial or falsely claimed.
- **Security:** attack it as a hostile tenant, a hostile role and a careless consultant, looking for isolation, secret, integrity and disclosure failures.

## 1. Target
- **Clone** into your own `mktemp -d`, check out the head, run `scripts/install-hooks.sh`. Never write into the original repo or its `.git`.
- **Your stacks,** 127.0.0.1 only, free at briefing:
  - `policy-composer-qa-bas-on`, edge **21480**, demo switch ON: api + migrate `PC_CONTENT_RELEASE_DIR=/repo/content/release-demo`; api `PC_SYNTHETIC_RELEASE_ENABLED=true`.
  - `policy-composer-qa-bas-off`, edge **21580**, compose defaults (switch OFF).
  - Clean-clone CI: `PC_CI_EDGE_PORT=21495`, `PC_E8_SOW_TEXT` = the SOW path in §2.
- **Browser:** local `mcr.microsoft.com/playwright:v1.63.0-noble`. **Environment:** local compose, synthetic tenants, non-prod (architecture §5.1).
- **LEAVE ALONE** (never stop, recreate, exec into, send traffic to, or remove volumes of):
  - `pc-lane-a` (18580);
  - the combined gates `policy-composer-qa-c-{a,b,c}` (21080-21295);
  - the merge seat (20480-20980);
  - `pc-s4*-*`, `pc-dbtest-*`, `qa-gateb-*`, and any `pc-ci-*` you did not start.
- **Shared daemon:**
  - count volumes at START (108 at briefing) and at END;
  - rebuild images only under `lockf -k /private/tmp/claude-501/-Volumes-KK-T9-External-HDD--CODING-Datasec-HPSM/dc13ed6b-f206-4b51-b117-ff3f2723cf9b/scratchpad/docker.lock <cmd>`.
- **LIVE Azure demo — A TARGET.** Kam, 2026-09-13 18:20 AEST, verbatim: *"Please revise the testing harness documents so they test the live site."*
  - **LIVE DEMO RULING: APPROVED by Kam 2026-09-13 18:20** (scope exactly as below; nothing beyond it).
  - **URL:** `https://hpsm-composer-demo.australiaeast.cloudapp.azure.com`. HTTP basic auth on every request, synthetic data only. **It is Kam's demo for his Monday review.**
  - **Credential:** read ONLY `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/4_Credentials/hpsm-demo-site.txt`, into memory.
    - Never print, copy, log, screenshot or mail its value.
    - Before mailing, grep your whole evidence folder and report for it, and record that the grep ran with a positive control.
  - **Head:** record what the live site runs at START and END (whatever version or health information the app shows after sign-in), and compare it with the head named in Tuesday's launch prompt, if any.
    - A difference is RECORDED and named in the BLUF.
    - If the site is mid-upgrade (version flipping, repeated 5xx), STOP the live pass and say so.
  - **Your own tenant, and only yours:** create ONE synthetic tenant named `QA Harness (synthetic) <YYYY-MM-DD HH:MM>` through the product's own admin flow, and do ALL mutating work inside it: engagements, discovery, generate, validate, exceptions, both approvals, release on a zero-device-group engagement if release is reachable at that head, Export PDF, stored outputs.
    - **NEVER create, edit, approve, release, export or delete anything in any other tenant.** That includes "Synthetic Customer B (demo content)" and the fresh engagements prepared for Kam's release walk-through.
    - Cross-tenant probes against those are READ or WRITE attempts that must FAIL (expect 404). **The first one that unexpectedly succeeds stops that probe at once; report it as a Blocker, with what changed.**
  - **Allowed on LIVE:** the full deliverables walk-through inside your tenant, and security probes **1, 2, 3, 5, 7, 8, 9, 11, 12, 13, 15, 17**, confined to your tenant or run as must-fail cross-tenant attempts.
  - **LOCAL STACKS ONLY, never live:** probes **4** (DB/RLS as pc_app), **6** (superuser audit tamper), **10** (repo/dependency scanning), **14** (size/rate/flood) and **16** (egress), plus any mutant, fixture, seed or DB script.
  - **Limits on LIVE:**
    - sequential requests only, ≤ 1 request/second sustained;
    - no body over 1 MB except ONE attachment probe at the product's own stated limit;
    - at most 3 wrong-credential attempts in the whole run;
    - no path brute-forcing (a fixed list of ≤ 30 paths);
    - no ssh, no `az`, nothing on the VM itself.
  - **STOP the live pass and report at once** if any request returns 5xx twice in a row, the site stops answering, or response time exceeds 10 s on 3 consecutive requests.
  - **Cleanup on LIVE:** delete nothing, never by DB. Leave your QA tenant in place and list EVERYTHING you created there (names, ids, times) in the report, so Kam can see it.
  - **Evidence class:** live results are MEASURED AT RUNTIME (LIVE). Local results are MEASURED AT RUNTIME (LOCAL). The matrix says which for every row.

## 2. Spec / DoD - REFERENCE DOCUMENTS (read-only; every row cites document + § + line)
- **AUTHORITATIVE, the original brief:**
  - `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/Datasec_HPSM_Cloud_Policy_Composer_Detailed_Scoping_Design_Specification_v1_1.docx`
  - Text: `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/_extracted/spec.md`
  - Lines: §3 L173, §5 L227, §7.1 L283, §8 L316-478, §9 L479, §10 L512, §12-§17 L606-794, §18 L796, §19 L809, §20 L824, §21 L863, §22 L880-917, §23 L919-947.
- **AUTHORITATIVE, Kam's commission and four scoping answers:** `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-09-10_hpsm-phase1-architecture.md` L8-29.
- **LAYOUT/STYLE TARGET (A-54):** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/HPSM Policy Composer - Screens.pptx`
- **FORMAT ONLY, not values (A-02):** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/Policy Preview.pdf` (text: `_extracted/policy_preview.txt`).
- **CONTEXT ONLY, not the brief (A-06):** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/_extracted/sow_e8.md`
- **RULINGS THAT CHANGED THE SPEC.** An intentional change is not a gap; contradicting a ruling is a finding. All under `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer/`:
  - `README.md`
  - `2026-09-10_policy-composer_ARCHITECTURE.md`: A-01..A-54 L54-131; Q-01..Q-20 L149-168; §2.4 L607; §2.5 L614; §2.6 L619; §3.2-3.3 L665-721; §4 L747; §5.1 L764; §6.1 L826; §6.3 L855.
  - `2026-09-10_source-measurements.md` §7 L193-208: the spec's own contradictions, as handled.
  - `2026-09-10_screens-MEASURED.md`
  - `2026-09-10_seed-data-CONTRACT.md`
  - `2026-09-13_output-export-request-S40.md`: Export PDF and stored per-client outputs.
  - `qa-wp4/README.md` L20-27 (WP4 DoD), L31-61 (rulings (a)-(h)).
- **NOT THE BRIEF, never test against:**
  - the HP SOW-01 Security Playbook `.docx` files at the root of `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/`;
  - `Source_Documents/HP Playbook Project/Shared with HP/`.
- **Suites** (run on YOUR stacks or clone): `scripts/ci.sh`, `test-db.sh`, `stack-rls-test.sh`, `stack-api-isolation.mjs`, `egress-test.sh`, `secret-scan.sh`, and `apps/web/e2e/run.sh`.
- **Edge config:** `docker/edge.nginx.conf`. **Builder evidence** under `qa-*` is a claim, not evidence.

## 2a. LEGITIMATE SHAPES
Not a checker. Pair every refusal probe with the ordinary input that must pass. A guard that refuses ordinary use is a finding.

## 3. Scope
### 3.1 DELIVERABLES - traceability matrix
- **Row:** `ID | requirement | source §+line | status | evidence path | evidence class`.
- **Status:**
  - MET / PARTIAL / NOT MET;
  - **RULED OUT** — cite the ruling's path + line;
  - **OUT OF MVP A** — spec §23 L924-927, architecture §6.3. MVP B / Bridge and Release 1/2 are marked, never failed;
  - **NOT TESTABLE LOCALLY** — say why.

**Minimum rows:**
1. **Acceptance tables:**
   - §22.1, all 12 scenarios (the passphrase x2 and round-trip rows are OUT OF MVP A);
   - §22.2, all 9 (ISO lineage and E8 ML3 hinge on Q-19 L167 and WP9 L839: cite the ruling, do not assume);
   - §23.1, all 9 (the Bridge bullet is OUT OF MVP A).
2. **One policy per engagement** at UI, API and DB (§3 L182, §7.1 L285-309); the forbidden route (§20 L856) answers 405.
3. **S1-S10 against §8.1-8.10**, with architecture §4's overrides; layout judged against the deck.
4. **Frameworks and content:**
   - five frameworks deduplicate; a conflict blocks until a manual decision;
   - 26 questions with required_when/show_when (§9);
   - 123 controls, each exactly once, across 22 categories.
5. **Engine:** 8-layer precedence (§12), the §12.1 cycle, the §13 table, ENGAGEMENT_SPLIT_REQUIRED.
6. **The §14.1 release gate:** make each of the 11 terms false on its own; each must block.
7. **Governance:**
   - §15 exceptions;
   - approvals bound to the manifest hash (A-28 L101, A-48 L109) — change the hash and they must void;
   - §16 versioning, clone and content impact.
8. **Outputs:** §17.1 plus the HP-format Preview (architecture §3.2-3.3). S32-B's unsigned refusals are RULED OUT.
9. **API:** every §20 route and §2.6 addition exists; each §21 code reachable in MVP A has a triggering probe.
10. **§19 NFRs measurable locally:**
    - p95 interactive < 3 s; generation < 30 s; determinism;
    - WCAG 2.2 AA (axe + keyboard);
    - correlation IDs, redacted logs, health endpoints.
    - Availability, RPO/RTO, retention and fidelity are NOT TESTABLE LOCALLY.
11. **Kam's answers:**
    - a brand swap leaves the manifest hash unchanged (A-36 L115);
    - every output is present;
    - no HP marks (Q-03 L151);
    - Export PDF and stored per-client outputs (S40).

**MET needs runtime evidence.** A repo test counts only after you watch it FAIL on a planted defect. READ ONLY cannot carry MET alone.

### 3.2 SECURITY - attack plan (spec §18 L798-807, §19 L816; architecture §2.4-§2.5)
**Every probe states FAIL first and has a POSITIVE CONTROL proving the instrument fires.**

| # | Attack | FAIL if | Control |
|---|---|---|---|
| 1 | AuthN: no token, expired token, wrong aud/iss, alg:none, expired membership | any 2xx or data | a valid token gets 200 |
| 2 | Roles: 7 x every op (qa-wp4 L25). platform_admin never approves (L36); self-approval only with `allow_self_approval`; auditor read-only | a denied cell succeeds server-side | the permitted role succeeds |
| 3 | API isolation: every id-taking op incl. stored outputs, links, audit search, directory, Admin, id case variants, cross-tenant clone (A-29) | anything but a 404 identical to a nonexistent id | own tenant gets 200 |
| 4 | DB isolation as pc_app: RLS FORCED on every tenant table; composite tenant FKs; GUC unset or garbage | a row crosses; a table is unforced; a cross-tenant FK commits | the same statement in-tenant succeeds |
| 5 | Secrets: a raw value in a secret field (SECRET_VALUE_ENTERED_IN_CLOUD); credential-shaped text in EVERY free-text field (ruling (a), 422). Grep the DB dump, logs, audit and every output for the marker | the marker persists or is echoed | `{value_ref}` and ordinary prose pass |
| 6 | Audit: append-only for pc_app; the chain verifies; a superuser tamper breaks it; every §18 event class present | it verifies after tamper; a class is missing | the untampered chain verifies |
| 7 | Integrity: same inputs give the same hash; a change after approval voids it; released rows immutable. Q2/S32-B: no signing key; 503 for manifest_jws, evidence ZIP, package manifest; "Not signed" | a signed/approved/released claim on a draft or unsigned artefact | a released synthetic version shows its true approvals |
| 8 | Edge: CSP, nosniff, frame-ancestors, Referrer-Policy, Cache-Control on JSON and downloads, `Origin: evil`, banner | a control is missing (justify severity) | the checker sees a header known to be present |
| 9 | Files: every intake (§8.9 evidence, §18 malware scan); Content-Disposition injection; link expiry and user+tenant binding; replay; key traversal | a link works for another principal or after expiry; a key escapes its tenant; a required intake is absent | your own link works and its sha256 matches |
| 10 | Scanning: `secret-scan.sh` over tree and history; `npm audit --omit=dev` | a live secret; a critical/high runtime advisory | a planted fake key in YOUR clone fires |
| 11 | Injection, XSS, CSRF-equivalent: payloads in text, filters, sort; XSS in the web and PDFs; tokens in cookies or URLs; state-changing GET; credentialed CORS | a payload executes, SQL leaks, a GET mutates, a token leaks | a benign value round-trips |
| 12 | Synthetic fence: ON/OFF x real/synthetic x create/clone/release. `True`, `1` and `"true "` count as OFF; the API refuses `synthetic=true` | a real tenant gets synthetic content; a non-exact value turns ON; a mark is missing | exact `true` turns ON |
| 13 | Platform tenant (Q9, D1): 3 fields, platform_admin only, platform-chain audit; excluded from lists; refuses sessions (incl. case variants); api refuses to start without the row | an extra field; the tenant is listed or a session accepted; the api starts | admin gets exactly the 3 fields |
| 14 | Size/rate: oversize body, deep nesting, 2048+ character strings, at most 50 rapid generate/export calls | a 500, a hang over 30 s, a crash, unbounded growth | a normal request succeeds |
| 15 | Error leakage, every error class | a stack trace, SQL, path, host, secret, or other-tenant existence | a known 404's body is recorded |
| 16 | Egress: `egress-test.sh` | a container reaches out | its control network sees egress |
| 17 | LIVE edge (§1): without credentials every path challenges (incl. `/api/*`, `/idp/*`, health, static); TLS versions and certificate; security headers; error-page leakage | a path answers without the challenge; TLS below 1.2; a leak; a missing header (justify severity) | a `-tls1_2` handshake succeeds, and a signed-in request to your own tenant succeeds |

## 4. Credentials (pointer only)
- **Personas:** the idp-mock's seeded users, 7 roles (`apps/idp-mock/src/app.ts` L9-53), plus a second tenant. Generate stack passwords per run (`scripts/ci.sh` L13-17).
- **Read NOTHING under `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/4_Credentials/` except `hpsm-demo-site.txt`, and only for the LIVE pass (§1), under §1's credential rules.** Its identity dirs are exported only for isolation. Run no `az`, no `gh`.

## 5. State-mutation & cleanup
- **Sanctioned:** your own clone, projects and volumes. Tear down only what you created; list volumes before and after.
- **LIVE sanctioned:** ONLY your own `QA Harness (synthetic) …` tenant and what you create inside it (§1). Nothing is deleted on live.
- **Reachable:** draft, generated, validated, review, approved, released synthetic (switch ON, zero device groups), a second version, a clone.
- **Gaps:** released with a device group (KNOWN); Imported/Verified (MVP B).
- **Never `rm`:** a new `mktemp -d` per attempt; quarantine, never removal; `${X:?}` on every expansion.

## 6. Output boundary / 6a. Evidence class
- **Findings, reports and recommendations ONLY** (Kam, 2026-08-11). Describe the fix-shape and the regression test in prose.
- **Evidence class on every finding and every row:** MEASURED AT RUNTIME / PROBED / READ ONLY.
- **Build the schema the product deploys** (compose `migrate`). If a suite builds a different one, that is a finding; do not reconcile.

## 7. Known-fragile / known-changed
**RULINGS IN FORCE** — copied from `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_hpsm-composer-09c1591-combined-tier1.md` L46-60. A mismatch is a finding.
- **Kam's cards:**
  - `demo-content`: fenced synthetic content, synthetic tenants only, ONE default-OFF switch;
  - `build-c12`: C12 mapping plus fenced synthetic adapter rows.
- **Q2(a):** no signing key. **S32-B:** no unsigned released ZIP, package manifest or JWS; outputs say "Not signed".
- **Q5-Q8:** outputs carry client, engagement, generated-by name and role; **no email**.
- **Q9:** platform_admin sees id, name, created_at only; platform-chain audit; the platform tenant is excluded and refuses sessions.
- **Q10/Q10-A:** an unserved id is CRITICAL; served but untyped gives DISCOVERY_ANSWER_UNTYPED.
- **Promoted fixes:** server-set `generated_at`; names derived from rows.
- **Directory role:** NOLOGIN, no pc_owner, no SET ROLE.
- **D1.**
- **The one intentional switch-ON e2e failure:** "S7 and S6 say what each count and issue means, before and after Generate".
- **Also in force:** WP4 rulings (a)-(h) (qa-wp4 L33-46) and the A-/Q- rows in §2.

**KNOWN** — combined brief L62-74; `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/5_Project_History/BACKLOG-candidates_s42_seat-hpsm-3e04.md`; `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/BACKLOG.md`.
- **From the combined brief:**
  - F6: "provisional", not "synthetic".
  - D2 is absent.
  - No re-pin (409 CONTENT_VERSION_CHANGED).
  - Release blocked with a device group; C11 unmapped; C11 contract mismatch.
  - Root MinIO credential.
  - The e2e refused-tenant probe.
  - The platform id is a literal.
  - The seed fails closed, untested.
  - Directory constant-folding.
  - "Unknown" support raises no issue.
- **From the s42 file:**
  - orphaned object on commit failure (L29);
  - per-process link key (L35);
  - credential-shaped display name gives 500 (L41);
  - storeOutput has no idempotency key (L47);
  - no C12 validator checks (L53).

**Known-open:**
- **W3-M6:** an unassessed high_impact is treated as not high-impact. `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-12-composer-0523193-wp3-tier1/report.md` L427; awaits an owner ruling.
- **Kam's open cards,** not decided: `hpsm-composer-demo-release-with-device-groups`, `hpsm-composer-live-demo-upgrade-after-c12`.

**Still owed:** a KNOWN item that silently gives a WRONG RESULT, or a security gap reachable in MVP A, IS a finding. Mark it "KNOWN, re-rated" with its backlog line.

## 8. Logistics
- **One session.** Order: the LIVE deliverables walk-through + LIVE probes 17, 3, 2, 5, 7 FIRST (it is the version Kam will show) -> local security 4, 6 -> §22.1 -> §23.1 -> §22.2 -> the rest. Anything unfinished is NOT TESTED, with the reason.
- **Head readings** of the original repo at start, mid and end: SHA + branch + time.
- **Siblings:** `reports/2026-09-13-composer-09c1591-combined-{a-engine-content,b-api-db,c-web-renderers}-tier1/`. Cite a finished one as PROBED (sibling); do not redo their mutation work.
- **Report:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-09c1591-brief-acceptance-security-tier1/report.md`, in this order:
  - **BLUF:** both verdicts + severity counts;
  - **findings:** FOUND / TESTED / HOW, oracle, evidence class, Blocker / Major / Minor / Polish with justification (priority is the humans' call);
  - the matrix;
  - the security table with each control's result;
  - **NOT TESTED**;
  - the docker ledger; the head readings.
- **Findings-only:** never fix, commit or file tickets. Long commands in the FOREGROUND; never end a turn waiting on a background notice.
- **No inbox:**
  - where the brief is silent, take the safest reading and record it;
  - approval-class work (live demo beyond §1, money, external comms, anything irreversible) is not done; list it under NOT TESTED.
- **MAIL YOUR VERDICT** to `tuesday-agent@agentmail.to`:
  - subject `[QA/Datasec-HPSM -> Tuesday] GATE VERDICT — Policy Composer acceptance vs original brief + security @ 09c1591 (tier 1)`;
  - first line `DELIVERABLES: <verdict> · SECURITY: <verdict>`.
  - **Never `wednesday-agent@`.**

## PRIOR GATES (context only; round 1 of a new class, no carry-forward)
- **Location:** under `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/` (counts are Blocker/Major/Minor/Polish).
- a06ada3 r1: NO GO 0/4/6/3
- 0c3078e r2: NO GO 0/1/5/0
- 55160dd r3: NO GO 0/1/2/0
- afc10e9 r4: GO WITH FINDINGS 0/0/2/2
- 0523193 WP3: NO GO 0/7/5/3
- 1a6b68d WP3 r2: NO GO 0/2/3/0
- 1a6b68d WP4+WP5: GO WITH FINDINGS on both
- 09c1591 combined A/B/C: in flight.
- **This codebase has repeatedly shipped tests that could not fail.**

PROVENANCE:
- Kam's instruction, 17:00 AEST | Tuesday's commission to the drafter | read 2026-09-13
- head, range 249, origin afc10e9, main clean | `git --no-optional-locks` rev-parse/merge-base/rev-list/status | read 2026-09-13 17:09
- reference paths exist; spec, architecture and qa-wp4 lines | test -e; grep -n; reads of ARCHITECTURE L40-174, L590-867 | read 2026-09-13
- rulings, KNOWN, W3-M6 | combined brief L46-74; s42 candidates L1-100; 0523193 report L427 | read 2026-09-13
- ports 21480/21495/21580 free; 108 volumes; Playwright image present | lsof, docker volume ls, docker image inspect | read 2026-09-13 17:05-17:15
- live demo facts | HANDOVER-S40.md L27; combined brief L13 | read 2026-09-13
- live site in scope | Kam's terminal instruction verbatim at 2026-09-13 18:20, read by Tuesday s12; scope and limits are Tuesday's reading, told to Kam on the panel | 2026-09-13

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 17:25
