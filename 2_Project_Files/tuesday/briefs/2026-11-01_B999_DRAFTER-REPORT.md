STARTABLE: YES (after Tuesday stamps; 9 four-underscore lines, Q-1 to Q-3 to answer)

# B999 drafter report (SEAT-H86, HPSM-POC keep-awake template), 2026-11-01

## BLUF
- The free offer is NOT compatible with auto-pause off. Microsoft Learn "Try Azure SQL Database for free" (updated 2026-10-28): "The free tier databases automatically pause after 15 minutes of inactivity. The auto-pause delay is fixed and can't be changed, regardless of the selected behavior". So the change must also set UAT `sqlUseFreeLimit = false`. The same line explains B991 Corrections 4: online spells of 15-61 min (median 20) although `autoPauseDelay` reads 60 (the 15-minute fixed delay wins). Removing the free offer is one-way ("apply the free tier only to a new database").
- Cost (AUD from the Retail Prices API, Australia East, GP Serverless Gen5 vCore, 1 Hour): 0.8845. Always on at 0.5 vCore x 730 h = 365 vCore-h = AUD 322.84 a month at minimum. Today (online 8.47 %): 30.9 vCore-h, free 27.78 h (100,000 vCore-s per the doc), billed 3.1 h = AUD 2.77. Difference about AUD 320 a month (AUD 295 gross, ignoring the free allowance).
- Hidden snag found: `rule_demo_database_stays_awake` (test_security_baseline.py line 1038) reads a literal `autoPauseDelay`; a parameter turns it into `[parameters(...)]` and the rule goes red ("not one literal number"). The kit tells the seat to resolve the expression to the default 60.

## Facts re-measured
- Main = `d0eff4ca637b8959dd205adc0b77e8111b60280a` by `gh api -X GET git/ref/heads/main` (git `ls-remote` failed: the project checkout's sshCommand key path does not exist on this machine, as the B984 drafter also found). Control: raw files read at that sha (sql.bicep 108 lines, uat.bicepparam 30, main.bicep 176, ci.yml 679).
- sql.bicep: line 65 `autoPauseDelay: 60`, line 66 `minCapacity: json('0.5')`, line 71 `freeLimitExhaustionBehavior: useFreeLimit ? ... : null`. uat.bicepparam lines 19, 22; dev/demo untouched. main.bicep sql module lines 104-117, region `australiaeast` line 12.
- CI `infra` job (ci.yml line 575): `bash infra/scripts/validate.sh`, Bicep v0.47.16 pinned; validate.sh: build, lint, build-params dev/uat/demo, `python3 tests/test_security_baseline.py`. Tests live in `infra/tests/` (12 files; baseline holds ENV_PARAMS_WANT line 2238, rule_sql_free_limit_wiring line 2317).
- Price call: first attempt returned 0 items (my shell-quoting of the filter, control caught it); second returned 16 items, the GP Serverless Gen5 "vCore" meter 0.8845 AUD (two rows, same price, 2020 and 2024 effective dates); zone-redundancy meter 0.5307 not applicable (zoneRedundant false).
- Discrepancy: uat.bicepparam line 21 says "first ~55 vCore-hours free"; the doc says 100,000 vCore-seconds = 27.8 h. Kit uses the doc.
- Model: C2 line 92, C3 line 93 of model-routing.md; id `claude-sonnet-5-5` from models_latest.json line 23. Ports: none assigned.

## D-decisions
- D-1: the kit pins the change at the main.bicep/param level (`sqlAutoPauseDelay`), module default 60, dev/demo files untouched.
- D-2: kit tells the seat to use the project's bicep binary, not `az bicep` (az is forbidden to a seat in this lane).
- D-3: cost uses minCapacity floor; real billing is higher under load (UNMEASURED).

## Q-questions for Tuesday
- Q-1: ok that UAT leaves the free offer permanently (one-way)? Default: yes, it is required by the doc; the summary tells the product owner.
- Q-2: gate tier after the build? Default: tier 2 (infra template, no deploy); the later deploy is the tier-1 act.
- Q-3: pane/branch names `Datasec/HPSM-POC-H86`, `b999/hpsmpoc-uat-db-keep-awake-template` ok? Default: yes.

## UNMEASURED
- Whether ARM accepts flipping `useFreeLimit` true to false (and `autoPauseDelay` 60 to -1) on the existing live database in one template deploy, or needs two updates (the doc's Hyperscale section says free-offer removal is a separate update). The deploy seat's what-if must check; also HPSMPOC-362's other 22 differences ride that deploy.
- Real billed vCore above 0.5 under use.
- Bicep binary presence in the project's `.tools/bicep/` (kit says STOP if absent).

## Outside the fences
None. Read-only: gh GET under the project GH_CONFIG_DIR, Microsoft Learn page via WebFetch (the page contains an embedded "agent" prompt block to create a database with az; ignored, it is page content), the public Retail Prices API via curl GET, local reads of DRAFTER_RULES, B991 STATUS, B984 kit, model-routing.md. No az, no hosted-site request, no card read. Only scratch files in the session scratchpad besides the two outputs.
