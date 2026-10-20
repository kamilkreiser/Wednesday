# B329 DRAFTER REPORT · HPSM-POC SEAT-M1 · SM 3.16 Policy Editor measurement (Composer L9-a + L9-c) · 2026-10-20 (clock 14:00 to 14:22 AEDT)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-20_B329_SEAT-M1_hpsmpoc-sm316-policy-editor-measure-L9a.md` (97 lines). It has one stamp slot, the launch time (`/usr/bin/grep -c -E '@SLOT:[A-Z0-9_]+''@'` → 1). Last line `READ-WHOLE-BY-TUESDAY: PENDING`. Pane `Datasec/HPSM-POC-M1`. Model Opus 5.5 (`BRIEF_SEAT_LEVEL=opus`), routing row C3 by analogy. Launch line uses `WED_USAGE_STOP=100`.
Fence kept: read-only file reads; no az, no HTTP to the VM, no git, gh, Jira, mail or publish. `.env` was read for variable NAMES only (`grep -o '^NAME='`).

## Read whole
- Composer `SRO-VIC_BUILD_PLAN.md` (159 lines) and gap analysis §4 to §6 (`:335-402`).
- HPSM-POC: B306 brief, its ADDENDUM-1 and STATUS (118 lines); B161 STATUS (166); B108 STATUS (134); B106 STATUS `:20-129`; B316 brief (the structure template); `CLAUDE.md`.
- B161's kit `ps/10_cdp_survey.ps1`, `12_wrapper.ps1` and the head of `11_survey_task.ps1`.
- `model-routing.md` (154 lines) and `brief_seat.sh` `:1-45`.

## Measured facts
- **K-B161-1 found:** `HPSM-POC/1_Project_Definition/Briefs/2026-10-06_B161_STATUS.md:87`. It asks for a **54-item Datasec baseline policy plus an Assess-only task once devices exist**, which is more than K8 (a) allows (a synthetic policy only, no devices). The brief answers only the "can a seat create a policy, and how" half and keeps the rest open.
- **How a seat reaches SM:** by run-command, then a scheduled task as the VM admin, then headless Edge on the VM, driven by the DevTools protocol against `https://localhost:7637`. B161 proved this with no human. Its XHR hook records method, URL, status and length; the brief extends it to record request and response bodies, with redaction.
  - Creating a policy through the editor's widgets headlessly is UNMEASURED: B161 only navigated.
  - API: the same origin, port 7637, with an OAuth password grant at `api/v1/signin`.
  - RDP is closed, and Bastion needs a human.
- **Identity, from HPSM-POC records:** `kamil@datasec-rd.com`, tenant `ec01829b-fdcb-4503-9834-eb2ffbd99169`, subscription `a6b8fe11-d1b5-4293-8727-b34aba08a705` (B306:20, B161:41, B108:12; C-07). This is Kam's login under the project's `AZURE_CONFIG_DIR`. The project's service principal `hpsm-poc-deploy` is scoped to `hpsm-poc-rg` only, not the SM resource group. The brief does not assert which Datasec environment this is.
- **Credential names in `.env`:** `HPSM_SM_VM_ADMIN_USER/_PASSWORD`, `HPSM_SM_USER_KAM/_PASSWORD`, `HPSM_SM_USER_PAUL/_PASSWORD`. `AGENTMAIL_API_KEY` is absent (0 hits; the control `JIRA_API_TOKEN` gives 1).
- **SM client JS:** `.tools/b106/js/LS_app.min.js` is present. Term counts: `createPolicy` 19, `savePolicy` 3, `policyConfigItems` 9, `passPhrase` 66, `policies/Import` 1. The control `ScheduledReports` gives 16.
- **B108 catalogue:** the two copies are sha256-equal (`e6f49f2a…`). The root checkout has no `Content/hpsm-sm-3.16/`, so the stale-root caveat applies.
- **HPSM-POC `CLAUDE.md:40`** forbids reading other project folders at run time. The brief therefore quotes the Composer plan and gap analysis, and tells the seat not to open them.

## Open questions (each with a recommendation)
1. **Can a seat drive SM without Kam's hands?** Yes, by B161's on-VM route. The open choice is the route. Use route A (on the VM). Do not use laptop Playwright against the public IP, because that sends the admin password over the internet to a self-signed endpoint.
2. **Which SM account?** Use `hpsmadmin` (the VM admin; B108 precedent). Not Kam's login, and never Paul's. Its SM role is unmeasured, so the seat stops if it is not Administrator or Analyst.
3. **What if the VM is deallocated?** The seat stops, and Tuesday asks Kam. Do not pre-authorise a VM start.
4. **Should Kam tell Paul that two `ZZ-DATASEC` test policies will appear?** Yes, briefly, before launch.
5. **Should the encrypted `.xml` export go into records?** Keep it in local evidence only, with its sha256 recorded, until Kam rules.
6. **Who commits the shape file and STATUS?** Tuesday's next HPSM-POC records seat. The seat itself commits nothing.
7. **`WED_USAGE_STOP=100`:** no earlier brief uses it, and the drafter did not check where `cockpit.sh` reads it (outside the fence). Confirm it before launch.
