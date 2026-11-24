STARTABLE: YES (only with Q1 and Q2 answered in words at the stamp, S4; the kit is written for the defaults Q1 "b" and Q2 "a")

# B2031 DRAFTER REPORT: the Azure boundary proof of OXPd's agent login, seat Datasec/OXPd2-Z1

Drafter B2031 (Opus, in-session, read-only), 2026-11-24 11:05 to about 11:20 AEDT. Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2031_SEAT-Z1_oxpd2-azure-boundary.md`. Its sidecar `.measured` sits beside it (`stamp_check.py`: 66 claims, 66 measured, rc 0). Scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s321/b2031/` (below `<d>`). Seat tools are in `<d>/seat-tools/`. **No Azure login, and no az command but `az version` and `--help` pages, all under a scratch config folder `<d>/logs/azcfg-help-only`.**

## BLUF
- **The seat's job:** it proves the five things the commission names, in 9 steps.
- **Every az call goes through ONE tool, `az1.py`.** It does five things:
  - fixes the state folder;
  - refuses anything not on the kit's list, before az starts;
  - strips `AZURE_*` from the environment;
  - finds the secret in every output byte and replaces it before printing or saving;
  - masks e-mail addresses.
- **Every result is judged by `checks_b2031.py`.**
- **Both tools pass their selftests,** and their controls fire:
  - `az1.py --selftest` (it runs against a stub az, never the real one): `SELFTEST: 27 of 27 PASS`. A mutant with the replacement removed scores `25 of 27`.
  - `checks_b2031.py --selftest`: `26 of 26 PASS`, with 15 bad inputs each failing.
- **The resource is an empty virtual network, not an NSG.** Microsoft's pricing page says "Virtual Network in Azure is free of charge." (I fetched it at drafting.) The two NSG pages I read state no price, so an NSG's cost is UNMEASURED.
  - Name, address space and tags: `oxpd2-boundary-proof-vnet`, `10.231.0.0/24`, with the commission's four tags.
  - No subnet, peering or DDoS plan. `az1.py` refuses `--subnet*` and `--ddos*`.
- **Three findings from the installed CLI's source (2.92.0) changed the design:**
  1. **`az role assignment list --assignee <appId>` gives a FALSE ZERO when Graph is refused.**
     - An app login has no directory read by default.
     - `role/custom.py:1884-1886` then logs "Assuming %s as an object ID." and filters on the appId as if it were the principal id.
     - So the commission's form counts only when it shows rows. The proof is the group's own list: `--resource-group oxpd2-dev-rg --include-inherited --fill-principal-name false`.
     - Pass condition: exactly ONE service-principal row, Contributor at the group, and none above it.
     - The tie of that row to THIS login is then DERIVED, and the kit says so.
  2. **The product owner's own sign-in is cached in `<project>/4_Credentials/.azure`.** I checked this by existence test only: `azureProfile.json` and `msal_token_cache.json` are present; `service_principal_entries.json` is absent.
     - `az login` merges profiles keyed by subscription id ONLY (`core/_profile.py:237`, `:505-530`).
     - So the seat's login in that folder would REPLACE his entry for subscription `a6b8fe11`.
     - Its logout would then leave that subscription gone from his profile there (`:309-326`).
     - Any az call made there before the login runs as the subscription's Owner.
     - **That is Q1. The default is a NEW folder, `.azure-oxpd2-sp`.**
  3. **On macOS the CLI keeps a service principal's secret in plain text** in `<azcfg>/service_principal_entries.json` until logout (`core/util.py:1626-1634`). So every STOP after the login runs the logout first.
- **Subscription:** the full id `a6b8fe11-d1b5-4293-8727-b34aba08a705` is RELAYED from `CLARIFICATIONS.md:226` and from the v2 steps' line 72. The seat measures it and STOPs on a mismatch.
- **The outside probes:**
  - A write: `group create oxpd2-boundary-probe-outside` must be refused (`AuthorizationFailed`). If it succeeds: STOP, delete nothing.
  - READ-only `group show` of `hpsm-poc-rg` (HPSM-POC's group, RELAYED from `HPSM-POC/SETUP_RUNBOOK.md:12`).
  - READ-only `group show` of `oxpd2-s14-path-test-rg` (the v2 group). If v2 was also run, Step 5 shows two groups, which is the "wider" STOP.
- **Gitignore proof:**
  - `git check-ignore` cannot run, because `<project>` is not a repository (rc 128, measured).
  - The kit has the seat print that, plus the only repository's toplevel and `<project>/.gitignore:4`, which reads `4_Credentials/`.

## Facts re-measured (instrument)
- **The card,** read with `decision_queue.sh show datasec-oxpd-kd1-azure-hpsm-subscription-1124` into `<d>/logs/card.out` (13 lines; the id appears once):
  - choice `b`, ruled at `10:32:56`;
  - delivered mark: "Kam ran the v3 steps 2026-11-24 ~10:49: group oxpd2-dev-rg in subscription a6b8fe11 (tenant ec01829b) ...".
  - `show` does NOT print the note.
- **The note,** from `kam_rulings_today.sh` (`<d>/logs/rulings.out`, 16 rows):
  - I gave it a read marker of my own (`KAM_READ_MARKER=<d>/logs/kam_read_marker_drafter`), so Tuesday's marker did NOT move.
  - The note, verbatim and twice at 10:32: "create a new resource group under kamil@datase-rd.com. issue new steps so agents have full control to spin up and create services/ vms etc". Note the address typo, "datase-rd".
- **The login file,** `<sp>`:
  - `-rw-------`, 204 bytes, 24 Nov 10:49:23.
  - Keys: appId, displayName, password, tenant.
  - `tenant` = `ec01829b-fdcb-4503-9834-eb2ffbd99169`; `displayName` = `oxpd2-claude-deploy`.
  - I read only those two fields, by program. The appId was never printed by me.
- **The OXPd `CLAUDE.md`:**
  - `:7` (Opus) and `:58-59` ("any Azure resource (no `az` command without a brief that quotes his word for it)") were printed by `awk`.
  - It is not yet updated for the 10:32 word.
- **The grant row** is `EXPIRING-GRANTS.md:9`.
- **PRIOR WORK:**
  - At about 11:10 there were 0 hits for the group, the login, `az login` and `service principal` across history, BACKLOG and CLARIFICATIONS, with controls.
  - At 11:17 `CLARIFICATIONS.md` had grown to 978 lines. Line 978 (in C-81) names the group and the login: this is the records seat B2030 recording the ruling, which is expected and not a STOP.
  - The kit says this.
- **The az CLI:** `/opt/homebrew/bin/az` points to Caskroom 2.92.0. `az version` shows `"azure-cli": "2.92.0"` with no extensions. A different version is a STOP before the login.
- **The only form for a client secret is `--password`** (from `az login --help`). It is on the argv for the seconds of the login (DERIVED), and the kit says to run nothing else meanwhile.
- **Model:** `claude-opus-5-5` (`levels.opus.model_id`).

## D-decisions (Tuesday's as coordinator)
- **D1:** one az call per Bash call, always through `az1.py`. There is a closed allowlist, and `--debug`/`--verbose` are refused (debug logs can print a request body).
- **D2:** a virtual network rather than an NSG, because only the virtual network's price is cited.
- **D3:** the role-assignment proof is the group-scope list. The `--assignee` form is recorded and counts only when it shows rows.
- **D4:** identity is re-checked before each write-class call (`acct-2`, `acct-3`).
- **D5:** every STOP after the login runs the logout first.
- **D6:** the seat writes nothing in the project's records. Its STATUS carries FOR RECORDS.

## Q-questions for Tuesday (each with its default)
- **Q1 (STOP-CLASS): which Azure state folder.**
  - **Default b:** a new `<project>/4_Credentials/.azure-oxpd2-sp`, mode 700, gitignored by `4_Credentials/`. The owner's sign-in is never touched.
  - **Alternative a:** the commission's `.azure`. This has the profile side effect of finding 2 above.
- **Q2 (STOP-CLASS): the resource and the probes.**
  - **Default a:** the free virtual network, plus read-only probes of `hpsm-poc-rg` and the v2 name.
  - **b:** an NSG (price UNMEASURED).
  - **c:** no read probe of `hpsm-poc-rg`.
- **Q3:** Opus, READY by Step 0 + 45 minutes, pane `Datasec/OXPd2-Z1`, hard stop S7.
- **Q4:** the network stays (the commission).
- **Q5 (not blocking; for the board):** the owner's tap was option b, "keep the agent-controllable environment", but the group sits in HPSM-POC's subscription `a6b8fe11` (tenant `ec01829b`), which he picked in his own step 3.
  - **Default:** proceed. The commission and the grant row already read it this way.
  - Say it plainly on the board with the result.
- **Q6 (not blocking):** the product owner's cached sign-in in `<project>/4_Credentials/.azure` means any OXPd seat launched by the launcher (which exports that folder) can act as subscription Owner. The proof covers the agent login, not that folder.
  - **Default:** card him that he can log his account out of that folder in his own terminal.
- **Q7 (the naming rule):** the kit quotes three things verbatim, as the commission asks:
  - the 10:32 note, including his address;
  - two RELAYED quotes containing "Kam" (the delivered mark and the grant row).
  - This seat makes no commit and no comment. The kit's HOLDS keep his name and address out of STATUS, and `az1.py` masks e-mails.
  - **Default:** keep the quotes verbatim.

## UNMEASURED / NEVER RUN
- Every Azure answer, including:
  - the login;
  - `AuthorizationFailed` and `ResourceGroupNotFound` (Azure's documented codes, never seen for this login);
  - whether `Microsoft.Network` is registered on the subscription (if not: `MissingSubscriptionRegistration`, a STOP);
  - the JSON shape of `az resource show` for a virtual network, which `checks_b2031.py vnet` reads;
  - whether the subscription-scope `--all --assignee` list is allowed at all for a group-scoped login.
- The checks have been run on synthetic inputs only. The kit marks a FAIL traceable to a missing field as `STOPPED: NEEDS TUESDAY`.

## Disclosure (no fence crossed; the edges)
- **Web reads:** I made three WebFetch reads of public Microsoft pages: the pricing page, the Virtual Network FAQ and the NSG overview. These are not project hosts. The harness saved one result under `/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude/projects/.../tool-results/` (its own location, not my write).
- **Folders in the project's `4_Credentials` and `.azure`:**
  - I made existence tests only (`test -e` / `test -d`), plus one `stat` of the `.azure` folder (mode and date).
  - Nothing was opened or listed. No file of `.azure` was read.
- **`az version`, `az ... --help` and the `az1.py` allowlist checks** ran under `<d>/logs/azcfg-help-only`, which az created. I never set the OXPd `.azure` as the config folder.
- **Hook advisories:** one refusal, of a `=====` separator; I re-issued the command with Read. There were also advisories on case-sensitive greps; the counts that matter were re-run with `-i` or `-F` and controls.
- **The read of `HPSM-POC/SETUP_RUNBOOK.md`:** one grep, for resource-group names (line 12). It is a Datasec project, read-only, and nothing else of HPSM-POC was read.
- **Not touched:** git state, Jira, mail, the board's read marker, the NAS, Source_Documents, and every other project.
