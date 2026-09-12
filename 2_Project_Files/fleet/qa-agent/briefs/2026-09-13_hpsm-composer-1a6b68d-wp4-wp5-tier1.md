# QA GATE — TIER 1, round 1 — Datasec / HPSM — Policy Composer WP4 API + WP5 website @ 1a6b68d (TWO VERDICTS, one session)

**The commission.** Kam, 2026-09-12 15:24:26 AEST: *"build the full website and fully functioning engine"*. At session 40's prompt, 2026-09-13 08:39: *"keep working on the HPSM project to get it ready for a full review"*. **He reviews the platform on Monday 2026-09-14. You are the test gate between that build and his review.**

**Head under test:** `1a6b68d793b60dbbfa227f35464725790714f42b` on local `main` of `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer`. `afc10e9..1a6b68d` is 69 commits (27 first-parent) and includes WP3/WP1 work gated separately. **NOT pushed**; HPSM-light `main` is `afc10e98c51505be1f1943335370cf2de3b47d44`.

**Give TWO verdicts in one report and one mail:**
- **WP4** — the API, `packages/api-contract`, `packages/db` 0007–0011, `apps/api`, `apps/worker`, `apps/idp-mock`, and the compose `migrate` service;
- **WP5** — the website, `apps/web`.

PRIOR ROUND: none on WP4 or WP5. The last Composer gate (WP3 round 1, NO GO 0/7/5/3) is at `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-12-composer-0523193-wp3-tier1/report.md`. The WP2 database gate (round 4) is at `…/2026-09-12-composer-afc10e9-tier1r4/report.md`. Read both reports' findings sections: this codebase has repeatedly shipped tests that could not fail.
Carried forward: none.

## Target, how to reach it, the shared daemon
- **Clone** into your own `mktemp -d` and check out `1a6b68d…`, plus `afc10e9…` for red controls. Run `scripts/install-hooks.sh`.
- **Your own stack:** compose project `policy-composer-qa-wp45`, edge port **18880**. Clean-clone CI needs `PC_E8_SOW_TEXT=/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/_extracted/sow_e8.md` set explicitly.
- **Browser:** drive it for real. The builder used `mcr.microsoft.com/playwright:v1.63.0-noble` (present locally) on the stack's internal network. Use it, or Claude-in-Chrome against 127.0.0.1:18880 **after fingerprinting that the browser runs on THIS machine**.
- **🔴 LEAVE `pc-lane-a` ALONE** (the builder's integration stack on 127.0.0.1:18580, 8 containers). Kam may click through it for Monday. Never stop, recreate or exec into it; never remove its volumes.
- **The daemon is shared.** Count volumes at START and END; never stop a container or remove a volume you did not create.
- **Builder evidence** (a claim, not evidence you rely on): `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer/qa-wp4/README.md` and `…/qa-wp5/` (`deck-tokens-MEASURED.json`, `evidence/integration/`).
- **The spec:** the architecture `…/2026-09-10_policy-composer/2026-09-10_policy-composer_ARCHITECTURE.md`, especially §2 (object model, tenant isolation, secrets, API), §4 plus `2026-09-10_screens-MEASURED.md` (screens), §5.1 and §6.1's WP4 and WP5 rows.

## THE BUILDER'S CLAIMS — verify each, relay none (session 40 wrap 2026-09-12T23:02:21Z, spf/dkim/dmarc pass; lane B README)
**WP4**
1. OpenAPI 3.1 contract 0.6.0: 44 operations, 7/7 contract tests; every API response in the suite is validated against the document.
2. RLS in force in the RUNNING stack: `migrate` alone holds the superuser password; api/worker connect as `pc_api`/`pc_worker` (not superuser, no BYPASSRLS, SET ROLE refused).
3. AuthZ matrix per role, written from spec §5 and the screens table, not copied from `authz.ts`.
4. Tenant isolation: 35 probes (read, search, download, write by id → 404, identical body), plus stack RLS part 4 through the running API, 9/9.
5. The §22.1 API scenarios on synthetic fixture content. DB suite 137–141/141, API DB suite 106–109/109, clean-clone CI green on lane B's head and on `047b1ed`.
6. Tuesday's rulings (a)–(h) as applied (README "Rulings"):
   - (a) credential-shaped text gives 422;
   - (c) attribute overrides give 422 `ATTRIBUTE_OVERRIDE_NOT_BUILT` and store nothing;
   - (d) platform_admin cannot approve;
   - (e) a clone carries the source pins, with the spec lines cited;
   - (f) migration 0010 makes `decided_at` server-set;
   - (g) `migrate` registers the provisional releases.
7. The README's new departures 1–8 (one ETag per draft, 403 sub-codes, EXCEPTION_NOT_REQUIRED, a blocked release commits its evidence, …).
8. Idempotency-Key replays only the identical request (0011); UNSUPPORTED_HPSM_VERSION reaches the device profile.

**WP5**
9. Every screen built: S1–S10, the engagements list, Admin, sign-in. No stub.
10. 26 colour tokens MEASURED from the Screens deck (A-54), each cited. Departure WP5-D1: seven deck text colours fail WCAG AA and are darkened within hue. No HP marks (Q-03). No create-policy route.
11. Ruling (c): S6/S7 override controls are disabled, with the reason shown.
12. The browser suite: axe WCAG 2.2 AA on 13 routes with a planted-violation control; the single-policy e2e with a planted control; 15/15 across runs 2–4.
13. A click-through S1→S10 on the integration stack. Fixed on the way: 401 ends the session (`99519a1`), top bar and rail layout (`c807fca`).
14. **Declared gaps, no placeholder data** (A-05): no item labels, framework lineage or supported-version data from the API (C12 empty, so every version reads "unsupported for package generation"); no stored validation-run or approval-history reads.

## 🔴 WHAT TO ATTACK FIRST
1. **Tenant isolation through the RUNNING API on YOUR stack**, as an attacker with a valid token in tenant B: every operation that takes an id, including list and search filters, dashboard aggregates, audit search, the manifest download, the change report and bridge sessions. Also check response timing and error-body differences that would reveal existence.
2. **AuthZ by role, adversarially:**
   - a role that may read but not write;
   - a customer approver approving for an engagement where they are NOT listed;
   - a security reviewer approving their own change (segregation);
   - platform_admin reaching tenant data;
   - an idp-mock token with a forged `tid` or `roles`, `alg:none`, the wrong audience, or expired.
3. **The release path (§2.3 in one transaction):** release without both approvals bound to the CURRENT manifest hash; approve, then change a draft input, then release; a concurrent double release; `decided_at` forgery (0010); RELEASE_BLOCKED committing its evidence.
4. **Secrets (§2.5 and ruling (a)):** credential-shaped text in every free-text field and sub-answer, through the API AND typed in the UI. Is any secret stored, logged, echoed in an error body, placed in an audit event, or shown by the website?
5. **Idempotency and ETags:** replay with a different body; a stale If-Match on every draft edit; lost-update races.
6. **The website as Kam will use it Monday:**
   - sign in as the consultant;
   - S2 create → S3 frameworks → S4 devices → S5 questionnaire → S6/S7 controls → S8 validate → S9 submit/approve → S10;
   - does every screen show what the API holds?
   - any dead control, broken navigation or console error?
   - what happens after a stack restart (the 401 fix)?

   **Screenshots of every screen in both themes if the app has two.** Judge the layout against the Screens deck: `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/` (read-only).
7. **The guards that guard the tests:**
   - plant a cross-tenant leak and show the isolation suite fails;
   - plant an axe violation and a create-policy control and show the browser suite fails;
   - check that the contract test fails on an undocumented status.
8. **Clean-clone CI at head.**

## KNOWN — do NOT report as new (BACKLOG)
- **WP3 engine findings** W3-M7, W3-m2…m5, and the 52-mutant rerun (gated separately in a parallel session).
- **WP6** Preview not built (S10 shows previews-only, the Preview is 503).
- **Declared WP5 gaps:** claim 14.
- **Lane B's nine BACKLOG candidates:** the redact path, per-item owner acceptance, attribute overrides, stored bridge sessions, the move-to-new-release action, bridge/HPSM-instance registration, clone residue, listControls size, setup-draft reads.
- **The edge proxy pins upstream IPs** at start (recreate edge after a partial rebuild).
- **Database residue:** R4-m1/m2/p1/f1 · U-0005 · S3-F1/F3/F5 · R2-m3/m5 · R3-m1.
- **W3-M6** is ruled (fail closed), not open.

**What you still owe on that list:** a KNOWN item that produces a WRONG RESULT silently, or a security gap on inputs MVP A can reach, IS a finding.

## Output, controls, logistics
- **Findings-only.** Every finding carries FOUND / TESTED / HOW plus an evidence class (MEASURED AT RUNTIME · PROBED · READ ONLY). Every zero gets a control. Never `rm`.
- **Head readings at start, mid and end.**
- **Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.**
- **Report:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-1a6b68d-wp4-wp5-tier1/report.md`, with SEPARATE WP4 and WP5 verdict sections.
- **MAIL YOUR VERDICT** to `tuesday-agent@agentmail.to`, subject `[QA/Datasec-HPSM -> Tuesday] GATE VERDICT — Policy Composer WP4 API + WP5 website @ 1a6b68d (tier 1)`. The first line carries BOTH verdicts, e.g. `WP4: GO WITH FINDINGS · WP5: NO GO`. **Never `wednesday-agent@`.** You have no inbox.

PROVENANCE:
- Kam's commission (15:24:26) and his 08:39 line | panel relay mail 2026-09-12 15:24:26 and the Datasec/HPSM S40 transcript row 2026-09-12T22:39:29Z, read by Tuesday s11 | read 2026-09-13
- head 1a6b68d, 69 commits (27 first-parent) on afc10e9, 13 named SHAs ancestors, tree clean, origin afc10e9 | git rev-parse / rev-list / merge-base / ls-remote in Datasec/HPSM 6_Policy_Composer, run by Tuesday s11 09:04 | read 2026-09-13
- claims 1-14, declared gaps, the edge-proxy defect, ports in use | Datasec/HPSM session 40 wrap mail 2026-09-12T23:02:21Z, spf/dkim/dmarc pass | read 2026-09-13
- lane B result table, DoD proofs, rulings as applied, departures 1-8 | Datasec/HPSM qa-wp4/README.md lines 1-60, read by Tuesday s11 | read 2026-09-13
- pc-lane-a running on 127.0.0.1:18580 (8 containers); ports 18880/18980 free; playwright v1.63.0-noble image present; E8 SOW text present | docker ps + lsof + docker images + ls, run by Tuesday s11 09:04 | read 2026-09-13

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 09:09
