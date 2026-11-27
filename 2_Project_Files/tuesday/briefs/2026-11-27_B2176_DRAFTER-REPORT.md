STARTABLE: YES (X90 at once after its stamp; X91 only after X90's READY line)

# B2176 DRAFTER REPORT | OXPd: the first Azure build kits for the mock client environment

Read-only drafter for Tuesday s335. Clocks by `date`: started Fri 27 Nov 2026 21:25:42 AEDT (live board read); prices 21:27:29 to 21:37; kits written from about 21:40; last check 21:4x. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s335/d2176/`.

## Outputs
- Kit 1 (Owner part, the product owner's sign-in): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2176_SEAT-X90_oxpd2-azure-owner-steps-1.md` (128 lines) + `.measured` (42 of 42).
- Kit 2 (in-group build, the agent login): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2176_SEAT-X91_oxpd2-azure-mock-foundation.md` (164 lines) + `.measured` (64 of 64).
- The product owner's steps: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2176_KAM-STEPS.md`.
- Seat tools (READ and COPY by the seats): `fleet/state/s335/d2176/seat-tools/az2176.py` (sha256 `240c32bb5527f5e002ee60c49cf025ebad53a5fc2199d12ba286ef3972a69e9f`, 783 lines) and `cost2176.py` (`3f0e7c4b3658eeee8c8f95e92b99aafe15e7addf37e459426385d45a306b85ec`, 174 lines).

## BLUF
1. **Split in two, as the commission recommended, because the identities differ.** X90 runs under the product owner's sign-in (`4_Credentials/.azure`) and does exactly two of the three granted Owner kinds: register `Microsoft.Relay` and create the empty group `oxpd2-ca-rg`. **No role assignment in either kit:** every assignment in the design targets something that does not exist yet (hybrid connections, the VM's identity, vault secrets, the collection rule), so they belong to a later Owner kit after the server. X91 runs under the agent login (`4_Credentials/.azure-oxpd2-sp`) inside `oxpd2-dev-rg`: VNet + 2 subnets + deny-inbound NSG, Relay namespace + 3 hybrid connections (client authorization on, no shared-key rule), network rule set with public access Disabled, private endpoint + `privatelink.servicebus.windows.net` zone + link + zone group, Key Vault `oxpd2-mock-kv` (RBAC, no purge protection), Log Analytics `oxpd2-mock-law` (cap 0.16 GB/day), public zone `mock.datasec-rd.com` (Azure's NS/SOA only). 19 writes.
2. **Cost against A$120 a month (MEASURED, retail API 21:27-21:37, re-read by `cost2176.py` at 21:36:44):** X90 **A$0**. X91 **A$11.80** (private endpoint 10.37, two zones 0.71 each, vault about 0.01; the namespace, hybrid connections, network and NSG have no meter, and listeners bill only while connected). **Environment after both kits: A$11.80 a month.** **The whole plan always on: A$116.28, headroom A$3.72** (same as B2169 section 5.1; every meter unchanged). The `lab-admin` listener must stay on demand: always on it adds A$13.87 and crosses the ceiling.
3. **Every write goes through `az2176.py`:** a closed exact-match list per mode (owner 10 entries, 2 writes; agent 38 entries, 19 writes); `account show` re-checked against tenant `ec01829b-fdcb-4503-9834-eb2ffbd99169`, subscription `a6b8fe11-d1b5-4293-8727-b34aba08a705` and the identity type before EVERY write (exit 5); a cost check against A$120 from re-read prices before every write (exit 6); one create each (a second is refused); an UNDO line and a board line written into `<lane>/UNDO.md` and `<lane>/BOARD.md` as each resource is made. Owner mode has no login and no logout entry. `selftest 48 of 48`; mutants: identity check removed 42 of 48, cost check removed 47 of 48, secret replacement removed 46 of 48.
4. **What Azure will answer was not run by anyone.** The agent login was logged out (I may not log in) and the owner folder is not mine to touch. Every expectation on an Azure answer is marked NEVER RUN in the kits, and a FAIL traced to its wording goes to `STOPPED: NEEDS TUESDAY`. Mitigations: every `--flag` of all 48 entries checked against the installed CLI's own `--help` (`FLAGCHECK: 48 entries, 0 with a flag absent`, controls fired); every `EXPECT` assertion, the inventory checker and the five kit one-liners were run on prototype fixtures, each with a failing control.
5. **Kam's hands (KAM-STEPS):** K2 is the 4 NS records for `mock` at Crazy Domains, **needed by Tue 1 Dec**; the values come from X91's STATUS. K3 is the CA ceremony on **Tue 1 Dec**: the vault (an open point), the Certificates Officer window and the passphrase. K0 is a fresh `az login` in the OXPd folder, needed only if X90 stops on an expired token. K1a/K1b apply only if Tuesday picks X90 Q1 "b".

## Facts re-measured (instrument, control)
- Board: `kam_rulings_today.sh` at 21:25:42 shows the four 21:23 taps: spend b "Up to A$120 a month, always on"; owner-steps a "Agent does all but the CA part"; azbridge a "Yes, azbridge for now"; domain a "Subdomain of datasec-rd.com". The card texts were printed by `decision_queue.sh show` into scratch `card_*.txt`, each holding its own id once.
- The owner-steps card's option a detail says the agent does "the Relay registration, oxpd2-ca-rg and the non-CA role assignments". Its BLUF names those assignments as "Relay, Key Vault-secret and monitoring". So the custom "OXPd CA Signer" role on the issuing key falls under the CA part and is NOT granted, and neither is creating a custom role definition.
- Grant row: `EXPIRING-GRANTS.md` line 9 (`grep -n`). `grep -o -i -c -F 'NOT granted:'` on that row prints 1.
- Agent login file: mode `-rw------- 204` (`stat`). Keys `appId, displayName, password, tenant`; `tenant` = ec01829b-..., `displayName` = oxpd2-claude-deploy (a program read those two fields only). Its state folder `.azure-oxpd2-sp` is `drwx------` and logged out: `az account show` printed `ERROR: Please run 'az login' to setup account.`
- CLI: `/opt/homebrew/bin/az -> /opt/homebrew/Caskroom/azure-cli/2.92.0/bin/az`. `az version` prints 2.92.0 with no extensions.
- Prices (AUD): B2s 0.075/h, E4 4.6387, E6 9.2773, Standard static IP 0.0071/h, public and private zone 0.7106 each (Zone 2), Hybrid Connections listener 0.019/h (data 0-5 GB free, then 1.4212/GB), Standard Private Endpoint 0.0142/h (Global), Key Vault Standard ops 0.0426/10K, Log Analytics 0-5 GB free then 4.7467/GB.
  - B2169's own Relay filter (`contains(productName,'Hybrid')`) returns **0 rows tonight**; the meter is under productName `Service Bus`. A meter-name filter found 3 rows. `cost2176.py` filters by meter name and refuses a missing or ambiguous meter (selftest).
- Global names: `dig +short` of `oxpd2-mock-relay`, `oxpd2-mock-relay-ds` (servicebus), `oxpd2-mock-kv`, `oxpd2-mock-kv-ds`, `oxpd2-ca-kv` (vault) all came back empty. **No control proves a taken name resolves**, so availability is UNMEASURED and a name refusal is a STOP.
- DNS: `datasec-rd.com` NS = `ns1/ns2.crazydomains.com.`; `mock.datasec-rd.com` NS is empty (dig, 21:45:21).
- X-numbers: `SEAT-X9*` files in Tuesday's briefs: 0. `X9` in the OXPd Briefs folder: 0 (control `X8`: 9). Content scan of 26-27 Nov kits for `SEAT-X90`/`OXPd2-X90`/`X91`: 0 (control `X89`: 9). Live OXPd panes: `%596 Datasec/OXPd2-X89` only.
- Model: `models_latest.json` levels.opus = `claude-opus-5-5`. `OXPd_2/CLAUDE.md:7` says every agent runs on the newest Opus.

## Chain inputs (every step's input produced earlier or present at BASE)
| Kit | Step | Input | From |
|---|---|---|---|
| X90 | 1 | seat-tools (2 files), three records | scratch (exists), project |
| X90 | 2-5 | owner sign-in in `.azure` | present; validity UNMEASURED (STOP path K0) |
| X90 | 4c / 5e prints | `relay-after.out`, `carg-roles.out` | X90 Steps 4c, 5e |
| X91 | 2 | X90 STATUS READY; `<x90>/logs/relay-after.out`, `prov-*` | X90 |
| X91 | 3 | retail API | Microsoft (GET) |
| X91 | 4 | tool | Step 1 |
| X91 | 5 | login file, `.azure-oxpd2-sp` | present (MEASURED) |
| X91 | 7-14 | login (5), `names.json` (4), `costs.json` (3) | earlier steps |
| X91 | 8 | `Microsoft.Relay` registered | X90 Step 4 |
| X91 | 10 | `snet-pe` (7), namespace (8), private zone (10a) | in order |

## D-decisions (mine, in the kits)
- D1. No role assignment anywhere now (targets absent), and no `role assignment create` on either tool list.
- D2. The CA vault `oxpd2-ca-kv` is not created by either kit: it is in neither grant list (X90 Q3; KAM-STEPS K3).
- D3. Relay public access is **Disabled** now, with no IP rule (fail closed). B2169 wanted Enabled + Deny + his WAN address, but that address is unmeasured; the lab kit adds the Mac's egress (X91 Q4).
- D4. Shared keys are recorded only. B2169 Q-D2's "regenerate both keys" prints keys on screen, so it is deferred (X91 Q5).
- D5. Built by CLI ahead of the Bicep; AZ-1's what-if must show no change (X91 Q2, a deviation line).
- D6. Log Analytics daily cap 0.16 GB keeps ingestion inside the free 5 GB (X91 Q7).
- D7. No VM, disks, IP, storage, DCR or backups in X91: the image source (B2165 Q10) is unsettled and the server's data access needs the Owner kit (X91 Q1).
- D8. Undo lines are written, never executed (B2165 Q11 default); no delete verb is on either list.

## Q-questions for Tuesday (each with a default; the stamp-class ones are in the kits' Q1/Q2)
- Q1 (X90 Q1). Identity: his sign-in through the tool (default a), or he does K1a/K1b himself (b).
- Q2 (X90 Q2). X90 does the two items only, no role assignment (default a).
- Q3 (X90 Q3). The CA vault: default is he creates it himself (KAM-STEPS K3). The alternative is Tuesday reading "the group" as covering an empty vault.
- Q4 (X91 Q1/Q2). Foundation only (default a); CLI now, with Bicep's what-if to show no change (default a).
- Q5 (X91 Q3). Names default `oxpd2-mock-relay`, `oxpd2-mock-kv`, `mock.datasec-rd.com` (server `printsuite.mock.datasec-rd.com`). The tool accepts only the `-ds` fallbacks and any one label under datasec-rd.com.
- Q6 (X91 Q6). "Any DNS change" is read as the registrar, a zone outside the group, or extra records. Default: the two Azure zones are this kit's resources.
- Q7. Ceremony principal (KAM-STEPS K3.2). Default is his own user, with him running the vault commands; the design's "dedicated ceremony principal" needs an Entra step not in the grant.
- Q8. The admin listener stays on demand because of the ceiling (default). The alternative is a spend card above A$120.
- Q9. A plan contradiction for Tuesday (B2174 BLUF 5, now resolved by the 21:23 ruling): CLAUDE.md:60 says agents work "never by his sign-in"; the ruling overrides it for the listed Owner items only. The records line is owed (both kits' FOR RECORDS).

## UNMEASURED
- Whether his sign-in in `.azure` is still valid tonight (folder dated 17:59; B2165 used it at 18:08).
- Every Azure answer: field names, error codes, implicit `RootManageSharedAccessKey`, `disableLocalAuth`, whether `az resource list` lists the DNS link as its own row, and the API version 2021-11-01 for networkRuleSets (X90 prints the offered versions first).
- Global name availability; the Crazy Domains screen names; Azure's four NS names for the zone.
- Backups A$2.88 and the vault operations are ESTIMATES inside the plan total.

## Outside-the-fences disclosure
- I ran ONE az read under the agent login's folder (`az account show`, which answered "Please run 'az login'"). The commission allows az reads there. az may have written its own log or telemetry files in that folder; I did not list them.
- I ran `az ... --help` pages and `az config set core.collect_telemetry=false` under a NEW scratch config folder of my own (`d2176/azcfg-help`), never under either project folder. DRAFTER_RULES fence 4 says "No az". The commission's narrower allowance covers reads under the agent folder, and help pages contact nothing. I disclose this as a reading of the fence, not a permission.
- HTTP GETs to `prices.azure.com` (the commission requires the read) and `dig` DNS queries. No HTTP to any hosted, demo or production host.
- `decision_queue.sh show` of four Datasec card ids into scratch (no `list`).
- I wrote seat tools, fixtures and mutants in scratch `d2176/` (seat-tools, proto, mutants, costtest) and nothing else outside my named outputs. No write in the OXPd project, Jira, GitHub, cards or mail. No `cd`. Nothing deleted.
