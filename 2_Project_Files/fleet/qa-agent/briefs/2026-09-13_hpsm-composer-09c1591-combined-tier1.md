# QA GATE, TIER 1: Datasec / HPSM Policy Composer COMBINED gate @ 09c1591, THREE PARALLEL GATES (A engine+content · B api+db · C web+renderers)

**The commission.**
- Kam, 2026-09-12 15:24:26 AEST: *"build the full website and fully functioning engine"*. **He reviews the platform on Monday 2026-09-14.**
- Kam, Tuesday panel 2026-09-13 09:17:37 AEST, verbatim: *"please spin up as many agents as possible to complete the task as long as multiple agents do not create a problem with development through multiple agents working on the same code base"*. That is why this gate is **three sessions on disjoint verdict areas.**
- **You are ONE of them.** Your prompt names your letter. Do your section, and read the common sections.

**Head under test:** `09c15918fadfee8a9bd590a1282113637f44515d` on local `main` of `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer`.
- **Range:** `afc10e9..09c1591` is 249 commits. **NOT pushed**; HPSM-light `origin/main` = `afc10e98c51505be1f1943335370cf2de3b47d44`.
- **Your focus is `1a6b68d..09c1591`,** the work since the last gates.
- **Local `main` may move while you work** (session 42 is building a follow-up called D2). **Your verdict is about `09c1591` only.**

**The LIVE demo** (Azure, and `pc-lane-a` on 127.0.0.1:18580) runs `c2fbc36` (an ancestor of your head) with the synthetic demo switch ON, and is **held there** pending two open Kam cards. It is NOT your target.

## PRIOR ROUNDS (read their findings sections first; this codebase has repeatedly shipped tests that could not fail)
- **WP3 engine r1** NO GO 0/7/5/3 (`…/reports/2026-09-12-composer-0523193-wp3-tier1/report.md`).
- **WP3 r2** NO GO 0/2/3/0 (`…/2026-09-13-composer-1a6b68d-wp3-tier1r2/report.md`). **Under the two-NO-GO cap the closed instances shipped, and the residue went to BACKLOG:** W3R2-M1, W3R2-M2, W3R2-m1..m3, W3-M7, W3-m2..m5.
  - **Session 41 lane A CLAIMS to have fixed that residue.** Verify it as a claim (Gate A).
- **WP4 + WP5 r1** GO WITH FINDINGS / GO WITH FINDINGS (`…/2026-09-13-composer-1a6b68d-wp4-wp5-tier1/report.md`). **W45-m1 (credential shapes) is CLAIMED fixed** (Gate B).
- **All reports are under** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/`.
- **This is round 1 of a NEW combined gate on new work.** It is not a third WP3 round.

## COMMON: target, stacks, the shared daemon
- **Clone** into your own `mktemp -d` and check out `09c1591…`, plus `1a6b68d…` / `afc10e9…` for red controls. Run `scripts/install-hooks.sh`.
  - **Never write into the original repository or its `.git`.**
- **Your own stack ONLY, named per gate:**
  - **A:** compose project `policy-composer-qa-c-a`, edge 127.0.0.1:**21080**, clean-clone CI `PC_CI_EDGE_PORT=21095`;
  - **B:** `policy-composer-qa-c-b`, edge **21180**, CI **21195**;
  - **C:** `policy-composer-qa-c-c`, edge **21280**, CI **21295**.
- **Clean-clone CI** needs `PC_E8_SOW_TEXT=/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/_extracted/sow_e8.md` set explicitly.
- **Demo switch ON** on your stack only, at `up`:
  - api + migrate: `PC_CONTENT_RELEASE_DIR=/repo/content/release-demo`;
  - api: `PC_SYNTHETIC_RELEASE_ENABLED=true`.
  - **Test both OFF and ON where your section says.**
- **Browser:** the local image `mcr.microsoft.com/playwright:v1.63.0-noble` on your stack's internal network.
- 🔴 **LEAVE ALONE:**
  - `pc-lane-a` (18580, 8 containers; Kam's live local demo) and the Azure demo host `hpsm-composer-demo.australiaeast.cloudapp.azure.com`. Never stop, recreate, exec into, or send test traffic to either, and never remove their volumes.
  - session 42's stacks and containers `pc-s42-*`, `pc-dbtest-*`, and the other two gates' projects.
- **The daemon is shared by three gates plus a builder.**
  - Count volumes at START (104 when briefed) and at END.
  - Never stop a container or remove a volume you did not create.
  - Take the shared docker lock the builders use if you rebuild images: `lockf -k /private/tmp/claude-501/-Volumes-KK-T9-External-HDD--CODING-Datasec-HPSM/dc13ed6b-f206-4b51-b117-ff3f2723cf9b/scratchpad/docker.lock <cmd>`. Never rm it.
- **The spec:** `…/1_Project_Definition/Architecture/2026-09-10_policy-composer/2026-09-10_policy-composer_ARCHITECTURE.md` (§2 object model, isolation, secrets, API; §2.3 release; §3.2 outputs; §4 + `2026-09-10_screens-MEASURED.md`; §5.1; §6.1) and the E8 SOW text above.
- **Builder evidence** (a claim, not evidence you rely on): `…/Architecture/2026-09-10_policy-composer/qa-s41/` and `…/qa-s42/` (`merge-seat/`, `on-proof/`), `…/qa-verify-s40-7135dec/`, `…/qa-switch-on-s40/`.

## RULINGS IN FORCE (verify the build matches; a mismatch is a finding)
- **Kam's cards:**
  - `demo-content`: fenced synthetic demo content, releasable for synthetic tenants only, behind ONE default-OFF switch;
  - `build-c12`: engine C12 mapping plus fenced synthetic adapter rows.
  - OPEN, do not test as decided: `hpsm-composer-demo-release-with-device-groups` and `hpsm-composer-live-demo-upgrade-after-c12`.
- **Tuesday's rulings:**
  - **Q2 (a):** no signing key in any stack.
  - **Q5–Q8:** stored per-client outputs carry client and engagement names and generated-by name and role, **no email**.
  - **Q9:** platform_admin lists tenant id, name and created_at ONLY; every call audited in the PLATFORM tenant's chain; the platform tenant is excluded from every list and refuses tenant-data sessions.
  - **Q10 / Q10-A:** an unserved question id is CRITICAL; served-but-untyped gives DISCOVERY_ANSWER_UNTYPED (warning), with the answer recorded and not used; the equivalence proof.
  - **S32-B:** §3.2, so no unsigned released evidence ZIP, package manifest or JWS; per-kind outputs say "Not signed".
  - **Promoted:** server-set `generated_at`; artefact names derived from rows.
  - **Directory role:** NOLOGIN, owned via the superuser bootstrap, NO pc_owner membership, no SET ROLE.
  - **D1:** the api refuses to start without the platform tenant row.
  - **The one intentional switch-ON e2e failure,** classified by exact title "S7 and S6 say what each count and issue means, before and after Generate" plus its switch message.

## KNOWN (do not report as new; BACKLOG `…/HPSM/5_Project_History/BACKLOG-candidates_s42_seat-hpsm-3e04.md`)
- F6: the early screens say "provisional", not "synthetic".
- D2, the running-release read, is not in this head.
- **No re-pin action after a content release change** (409 CONTENT_VERSION_CHANGED on old engagements).
- Release blocked with a device group (C11 rows absent; carded).
- Root MinIO credential (local-only).
- The e2e fixture's refused-tenant probe on switch ON.
- The platform id is a literal.
- The seed fails closed untested.
- The constant-folding dependency of the directory call.
- "Unknown" support raises no issue.
- The C11 seed-contract column mismatch.
- **What you still owe on that list:** a KNOWN item that yields a WRONG RESULT silently, or a security gap reachable in MVP A, IS a finding.

---

## GATE A: ENGINE + CONTENT (verdict: ENGINE+CONTENT)
**Paths:** `packages/engine`, `packages/canonical`, `packages/content`, `content/release-demo`, `content/release-draft`.
1. **The WP3 residue claimed fixed by session 41 lane A** (commits in `1a6b68d..14cf4d8` and after): W3-M7 (secret intake at S0, no echo, record scanned), W3-m2..m5, W3R2-M1, W3R2-M2, W3R2-m1..m3. Re-run the round-2 gate's mutants and your own. **A test that cannot fail is a finding.**
2. **C12 mapping** (`contentFromBundle` on `hpsm_adapter_metadata`):
   - strict refusals of malformed rows;
   - the SYNTHETIC fence: one row `SYNTHETIC-DEMO-ADAPTER-1` / `SYNTHETIC-DEMO-1` citing Kam's ruling, "not HP's HPSM support matrix";
   - UNSUPPORTED_HPSM_VERSION unchanged on real content;
   - `baseline_values` and `device_capabilities` still refused.
3. **`content/release-draft` byte-identical** (content:check `79364073…`); demo release `fd7db6b8…`; no releasability claim in real content; **no fabricated exceptions, approvals or reviews** anywhere in content or fixtures.
4. **The engine's switch truth table:** CONTENT_SYNTHETIC vs CONTENT_PROVISIONAL, the SYNTHETIC mark, the generation block.
5. **Answer grading** case 1 (unserved, CRITICAL) vs case 2 (`DISCOVERY_ANSWER_UNTYPED`). **The equivalence proof:** outputs identical except `input_hash` and the one warning, and every value identical.
6. **Readiness with a device group:** confirm "unknown" support blocks release **without any issue code** (known), and that nothing silently reports it as supported.
7. **Clean-clone CI at head.**

## GATE B: API + DATABASE (verdicts: WP4 API, and DB 0012–0015)
**Paths:** `packages/db` (migrations 0012–0015, `bootstrap.sql`, `src/`), `apps/api`, `apps/worker`, `apps/idp-mock`, `packages/api-contract` (0.13.0), `compose.yaml` api/migrate env.
1. **Tenant isolation + authZ regression** through the RUNNING API (the 1a6b68d gate's attack list): every id-taking operation, including stored outputs, links, the directory, and Admin.
2. **Migration 0015:**
   - REVOKE on the three derived columns (42501);
   - the BEFORE INSERT trigger (server `now()`, names from rows; **cross-tenant same-name engagement**);
   - append-only artefacts;
   - platform tenant seed "Platform", with the membership CHECK holding even for superuser;
   - `pc_tenant_directory`: NOLOGIN, owner via bootstrap, `pg_auth_members` has no pc_owner link, SET ROLE refused, the definer-function set pinned, column grants, a single policy, no other column or table.
   - **Attack:** can any pc_app or pc_owner path read beyond the three columns, or list the platform tenant?
3. **Q9** `GET /platform/tenants`: platform_admin only, exactly three fields, audited in the platform chain (the chain verifies); **no tenant-data session on the platform tenant, including case variations of the id.**
4. **Synthetic fences at the API:**
   - 422 SYNTHETIC_CONTENT_REQUIRES_SYNTHETIC_TENANT on create and clone;
   - 409 for a real tenant on synthetic content;
   - platform-only synthetic tenants (pc_app can insert synthetic=true at DB level; the API must stop it);
   - the switch is exact-"true" only;
   - compose default OFF.
5. **Stored per-client outputs (Q5–Q8):**
   - tenant-prefixed object keys; audited links bound to user and tenant; bearer + link; sha256 integrity;
   - **never sends the three derived columns**;
   - no email;
   - `Output.synthetic` from the content release;
   - `X-Output-Not-Signed`;
   - §3.2 503s for manifest_jws, evidence ZIP and package manifest on unsigned released versions.
6. **D1 startup refusal; `ensureBucket` fail-closed:** re-run the builder's rollback proof yourself (a wrong key makes the api exit 1; roll back; healthy).
7. **Upgrade path of a live stack:**
   - start at `c2fbc36`, create a synthetic engagement, upgrade to `09c1591`, and measure what the engagement does (the 409 is KNOWN; report anything worse, e.g. data loss or a 500);
   - PREFLIGHT;
   - the switch state is preserved.
8. **Secrets:** credential-shaped text in every free-text field (W45-m1 claimed fixed); nothing echoed in errors, audit or logs.
9. **Clean-clone CI at head.**

## GATE C: WEBSITE + RENDERERS + OUTPUT PROOFREAD (verdicts: WP5 web, WP6 renderers)
**Paths:** `apps/web` (incl. `e2e/`), `packages/renderers`.
1. **The website as Kam will use it Monday, switch ON, on your stack.**
   - Sign in as the consultant, then S1→S10 on a synthetic tenant.
   - Export PDF stores then downloads.
   - The stored outputs list shows client, engagement, generated by name and role, generated at, and DRAFT / Not signed / SYNTHETIC.
   - The Admin tenant list never shows the platform tenant.
   - F5: S9 approval terms as recorded now.
   - F8: breadcrumb.
   - No dead control or console error.
   - **Screenshots of every screen.**
   - Judge the layout against the Screens deck in `…/Source_Documents/HPSM_Policy_Composer_2026-09-10/` (read-only).
2. **The e2e suite on BOTH switch OFF and switch ON** on your stack:
   - the ONE intentional switch-ON failure classified exactly;
   - **plant** a second failure and show it is NOT absorbed by the classifier;
   - the **live-stack guard:** `run.sh` and the Playwright config refuse `pc-lane-a`, 18580 and the Azure host. Show it refusing, using a harmless dry target; never touch the live stacks.
3. **🔴 PROOFREAD EVERY OUTPUT KIND** for accuracy and formatting (Kam asked, in his words, whether the output *"has been proofread for accuracy and formatting"*).
   - **Render on your stack:** HP Preview, policy document, worksheet, change report, for a draft AND for a released synthetic version (release is reachable through the product workflow with ZERO device groups: record exceptions, both approvals).
   - **Open every PDF.** Check each against HP's sample Policy Preview (in the Source_Documents folder) and the spec. Report every statement that is false, contradictory, unlabelled or clipped. Cover at least:
     - **the draft/released truth table:** draft footer "Unreleased draft. Not generated from an approved policy manifest.", released footer per source, and no approval, release or signature claim on an unreleased or unsigned artefact;
     - **"UTC"** within the printable area (≥ 18 pt from the edge; builder: 20.50 pt);
     - **"Framework lineage"** vs Scope's frameworks;
     - **the posture row;**
     - **the zero-group register wording;**
     - **device group NAMES** (not UUIDs);
     - **SYNTHETIC and DRAFT / "NOT SIGNED" marks;**
     - **no mid-word header breaks;**
     - **Preview geometry vs the sample** (builder: max 0.80 pt, tolerance ±3 pt).
4. **Guards that guard the tests:** plant a violation of axe, of the geometry pin, and of the draft-footer truth table, and show each suite fails.
5. **Clean-clone CI at head.**

---

## Output, controls, logistics (all gates)
- **Findings-only:** never fix, commit or file tickets.
  - Every finding carries FOUND / TESTED / HOW plus an evidence class (MEASURED AT RUNTIME · PROBED · READ ONLY).
  - Every zero gets a control.
  - Never `rm` outside your own mktemp.
- **Head readings** at start, mid and end.
- **Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.**
- **Reports, one per gate:**
  - A: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-09c1591-combined-a-engine-content-tier1/report.md`
  - B: `…/2026-09-13-composer-09c1591-combined-b-api-db-tier1/report.md`, with separate WP4 and DB sections
  - C: `…/2026-09-13-composer-09c1591-combined-c-web-renderers-tier1/report.md`, with separate WP5 and WP6 sections and the proofread table
- **MAIL YOUR VERDICT** to `tuesday-agent@agentmail.to`. Subject `[QA/Datasec-HPSM -> Tuesday] GATE VERDICT — Policy Composer combined gate <A|B|C> <area> @ 09c1591 (tier 1)`. The first line carries your verdict(s): GO · GO WITH FINDINGS · NO GO.
  - **Never `wednesday-agent@`.** You have no inbox.

PROVENANCE:
- Kam's commission 15:24:26 and the standing agents rule 09:17:37 | panel relay mails read by Tuesday s11 | read 2026-09-13
- head 09c1591, 249 commits from afc10e9, main tree clean, origin afc10e9 | git rev-parse / rev-list / status (--no-optional-locks) in Datasec/HPSM 6_Policy_Composer, run by Tuesday s11 15:38 | read 2026-09-13
- lanes, claims, checks, decisions, gate targets, backlog list, live stacks at c2fbc36 held | Datasec/HPSM session 42 READY FOR QA mail 2026-09-13T05:36:32Z, read whole by Tuesday s11 | read 2026-09-13
- prior verdicts and the WP3 cap outcome | report.md heads in Testing Agent MAIN/projects/hpsm/reports/ + Tuesday pickup item 0004, read by Tuesday s11 | read 2026-09-13
- ports 21080/21180/21280 free, volumes 104, playwright v1.63.0-noble present, E8 SOW present, pc-lane-a 8 containers | lsof + docker volume ls + docker images + ls + docker ps, run by Tuesday s11 15:38 | read 2026-09-13
- rulings Q2, Q5-Q10-A, S32-B, promoted fixes, directory role, D1, e2e classifier; Kam cards demo-content and build-c12; open cards | Tuesday's sent mails to datasec-hpsm@ and decision_queue.sh show, read by Tuesday s11 | read 2026-09-13

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 15:40
