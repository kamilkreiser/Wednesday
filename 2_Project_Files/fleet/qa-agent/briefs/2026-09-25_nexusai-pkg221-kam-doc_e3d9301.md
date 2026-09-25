# NexusAI 2.2.1 — Marketplace package handover (for Kam)

**Version: 2.2.1.** Built 2026-09-25 by seat S83L (Datasec/NexusAI-L) on Tuesday's GO (ANSWER 2026-09-25T08:10:12Z), after Kam ruled "Fix it now and resubmit" (live board 17:52:13 AEST, CLARIFICATIONS C-158). **This is a document, not a submission.** Nothing here has been uploaded; the upload and the submission are yours alone (C-23).

## BLUF

- **What changed from 2.2.0:** one thing. The telemetry availability test is now a Standard test instead of a classic URL ping test.
- **Why:** on the live 2.2.0 listing, a customer who chooses "Application telemetry: Enabled" gets **Deployment failed**. Azure rejects the ping test ("Value cannot be null. Parameter name: format"), and Microsoft retires URL ping tests on **30 September 2026**. Measured in the customer test on 2026-09-25 (RD-665).
- **Proven on real Azure:** the fixed template deployed the Standard test and its alert, and 6 of 6 real availability checks of `/api/health` passed from Australia East, Central US and West Europe.
- **Customer image: unchanged.** Same digest as 2.2.0; nothing was rebuilt or pushed.
- **What you do:** upload the plan zip below as the new version of the plan's deployment package, and submit. The listing images are unchanged.

## 1. What a customer sees

| | 2.2.0 (live now) | 2.2.1 |
|---|---|---|
| Telemetry **Disabled** (the default) | deploys | deploys, identical |
| Telemetry **Enabled** | **Deployment failed** (the availability test is rejected; the app itself still deploys) | deploys; the availability test checks `/api/health` every 5 minutes from 3 regions and alerts on failure |
| Existing ping tests after 30 Sep 2026 | Microsoft removes them | n/a (none created) |

Standard tests are billed per run (Microsoft's list price about US$0.0007 a run, so about US$18 a month for this test's 3 regions every 5 minutes). That cost only applies to customers who choose telemetry Enabled.

## 2. The files

Built by `scripts/marketplace-package-build.sh` (the only build path) into `marketplace-submission-2026-09-25-2.2.1/`, beside the repo:

| File | sha256 | Goes to |
|---|---|---|
| `NexusAI_plan-managed-ai_2.2.1_3f79e9c.zip` | `5fb547893535ecd891b8147cf117c83f83b2f05dfc68f28f7732383aaf1172dd` | the plan's Technical configuration → Deployment package |
| `NexusAI_listing-assets_2.2.1_3f79e9c.zip` | `ba29c1890df2bb1b9c1edcd884eecdf2151db9a71211badf807156b355b9a7e7` | not needed: the same 7 images as 2.2.0, byte for byte |
| `MANIFEST-2.2.1_3f79e9c.txt` | `75ae0aa7283652b6d69696414fb864c4f13a28b2ac7364de184abce53ab58100` | your record; its last line reads `MANIFEST COMPLETE: 32 checks, 0 failed` |

Inside the plan zip, compared with the 2.2.0 plan zip: `createUiDefinition.json` and `viewDefinition.json` are byte-identical; `mainTemplate.json` differs in exactly one resource, the webtest. Its sha256 (`f91ee8f1006e76e1…`) is the same file that passed the real-Azure proof in section 3.

## 3. Commits and proof

- **Package commit:** `3f79e9cb8ed8834e08a1744af8bbbd5823d4303a` on branch `rd-665-standard-webtest-s83l`, built on the 2.2.0 package line (`mkt-release-2.2.0-s81j` @ `c5da4d4`):
  - `d14a975`: the fix (the webtest) and its test.
  - `3f79e9c`: `release-policy.json` records that 2.2.1 ships the 2.2.0 image. **The zips are built from this commit.**
  - After it, tests and this document only (`bd42973`: cells pinning the 2.2.1 image; then this handover). The shipped files (`azure-marketplace/`) are identical at the branch head and at `3f79e9c`.
- **Customer image:** `nexusaireleaseacr.azurecr.io/nexusai@sha256:fdda33098c36a484b50a9a761660bb69bc53f5ed238ffceeb1bd038c8eb77f66`, the 2.2.0 image built from main `0677388` (C-149). **Not rebuilt.** The build checked an unauthenticated pull of it: HTTP 200.
- **Checks:** arm-ttk 49/49 on `3f79e9c` (18 wizard tests run); `npm run verify` **VERDICT: PASS, 4127/4127 tests across 242 suites** (with the two 2.2.1 cells; SESSION_SECRET unset); a new test fails if a ping test ever returns (it fails on 2.2.0's template and passes on 2.2.1's).
- **Real-Azure proof** (2026-09-25, the customer-test subscription, not Datasec's): the fixed template deployed with telemetry Enabled → **Succeeded**; the availability test was read back as a Standard test aimed at `/api/health`; its alert points at it; 6/6 availability runs passed from 3 regions. The test was then disabled to stop its cost. The 2.2.0 template failed at exactly this step in the same subscription the same day.

## 3a. Version numbers

| Where | 2.2.0 | 2.2.1 | Must it change? |
|---|---|---|---|
| **Partner Center plan Version** (Technical configuration) | 2.2.0 | **2.2.1** | **Yes.** Microsoft: "Increment this version each time you publish a change to this page. The version number must be in the format: integer.integer.integer." (Learn, *Configure a solution template plan*, "Assign a version number for the package") |
| `mainTemplate.json` `contentVersion` | 1.3.0.0 | 1.3.0.0 (unchanged) | **No.** Microsoft: "You can provide any value for this element. Use this value to document significant changes in your template." (Learn, *Template structure and syntax*). It has been 1.3.0.0 since `6d47b2a` (2026-04-23), through every package from 2.0.0 to 2.2.0. Left unchanged so the only difference in the template is the fix |
| `createUiDefinition.json` `version` | 0.1.2-preview | 0.1.2-preview (unchanged) | **No.** It names the wizard schema's format version, not our release |

## 4. Your steps

1. [Partner Center → Marketplace offers](https://partner.microsoft.com/dashboard/marketplace-offers/overview) → the NexusAI offer → plan **reporting-dashboard-hpam** → **Technical configuration**.
2. Version: **2.2.1**. Upload `NexusAI_plan-managed-ai_2.2.1_3f79e9c.zip`.
3. Check the file name against `MANIFEST-2.2.1_3f79e9c.txt` (last line: `MANIFEST COMPLETE: 32 checks, 0 failed`).
4. Review and publish, as for 2.2.0.

## 5. What 2.2.1 does NOT change or prove

- Everything in the 2.2.0 handover's residual list (`docs/resubmission/2026-09-22_resubmission-handover-for-kam.md`, section 4) still applies, except the telemetry failure this fixes.
- The portal wizard screens are being clicked through by you in the customer test (field sheet on `s83l-customer-test-plan`); 2.2.1 does not change them.
- The listing text is unchanged: its plan summary still names App Service and Redis (RD-663, your text to change if you want).
- Customers on subscriptions without GPT-4.1 quota in their region (RD-664) are unaffected by this release.

## PRIOR WORK

The ping test came in `8f4e959` (2026-04-25, "Architectural items E + C + A + B + D") and had no other change since. Kept: its name, target, 200 rule, frequency, timeout, regions and retries, and the alert wired to it. Replaced: only the retired ping form. The 2.2.0 handover doc is the model for this one and is not changed.
