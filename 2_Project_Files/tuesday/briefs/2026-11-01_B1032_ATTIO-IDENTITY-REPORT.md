# B1032 — ATTIO bridge identity report (read-only research, files only)

**Researcher:** read-only subagent for Tuesday (Datasec), 2026-11-01.
**Card:** attio-digest-recipient-app-setting-1101, choice b (10:03): agent changes ONE App Service setting `FOLLOWUP_DIGEST_TO` on `datasec-attio-bridge` / `attio-bridge-rg` to `tuesday-agent@agentmail.to`.
**Method:** files only. No `az`, no HTTP, no mail, no writes except this file. No secret opened: `azureProfile.json` was parsed for subscription id, tenant id, user name and user type only; token caches were listed by NAME only.

## CONCLUSION: (A), with two record gaps

An identity with a recorded RG-scoped grant on `attio-bridge-rg` exists and is named in records:

- **Identity:** service principal **`vision-sales-portal-claude-deploy`**, appId `bc1e3581-a76e-4df1-a807-58b4386c6f8d`, object id `1b3bee22-…`, tenant `d500ebad-cf53-4f2a-a501-f831289e67fc`, sub `0c57ab37-349c-47ae-a10f-e284a380bbb9`.
- **AZURE_CONFIG_DIR:** `/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/4_Credentials/.azure`
- **Grant:** **the product owner made it himself** on 2026-08-21: he created `attio-bridge-rg` and gave this SP an RG-scoped Contributor assignment (`67aaac02…`, 02:46:53Z).

No ATTIO-named SP exists anywhere in the records. ATTIO has no `.azure` dir of its own.

**Two gaps (not real disagreements, but they need saying):**
1. Workspace hard rule 4 (`/Volumes/Laptop-DEV/CLAUDE.md`, "Agent identities are scoped per project (2026-08-06)") lists only the three SPs and says each is confined to "its own resource groups". `attio-bridge-rg` is outside Vision's original set. It became one of this SP's RGs only through the product owner's 08-21 grant. The coupled-pair text covers *folders*, not Azure identity. The Azure reach comes from that one explicit grant.
2. The grant is a record from 2026-08-21 and has **not been measured since** in any file I read. It may have been removed. Before any write, the kit's first step must be a read-only check that the role assignment still exists at `attio-bridge-rg` scope.

**Risk to name:** the same SP also holds Contributor on `datasec-sales-portal-rg` (LIVE Vision production) and `hpas-quickquote-rg` (runbook :30-32). So any command must carry `-g attio-bridge-rg -n datasec-attio-bridge` explicitly. A wrong or missing `-g` is a production-reach risk.

---

## Q1. What ATTIO's own records say about hosting and identity

| Claim | Evidence |
|---|---|
| Live web app `datasec-attio-bridge`, RG `attio-bridge-rg`, KV `attio-bridge-kv`, tenant `d500ebad-…` / sub `0c57ab37-…` | `ATTIO/1_Project_Definition/2026-08-21_ATTIO-20_hosting-runbook.md:20-27` |
| RG "**created by Kam**" | runbook `:20` |
| Deploy identity = "The deploy service principal (`bc1e3581-…`, object id `1b3bee22-…`) holds **Contributor scoped to individual resource groups and nothing at subscription scope**" | runbook `:57-58` |
| That SP cannot create RGs or role assignments; both hit 2026-08-21; "Do not route around either… Ask Kam" | runbook `:59-71` |
| The ask must be RG- or vault-scoped, `--assignee-object-id` + `--assignee-principal-type` | runbook `:73-75` |
| The SP also holds Contributor on `datasec-sales-portal-rg` and `hpas-quickquote-rg` ("The SP holds Contributor on both") | runbook `:30-32` |
| ATTIO's session identity is "a service principal in `d500ebad`, confined to Vision's RGs" | `ATTIO/5_Project_History/history.md:59-60` |
| Bridge built "from Vision's launcher via the coupled pair" | `ATTIO/5_Project_History/history.md` session-2 heading 2026-08-21 (the section beginning just above `:431`) |
| `bc1e3581` = `vision-sales-portal-claude-deploy` | `Vision_Sales_Portal/5_Project_History/history.md:2256` ("SP `vision-sales-portal-claude-deploy` (bc1e3581)"); also `:1405`, `:2015` |
| Grant made by the product owner himself: "RG attio-bridge-rg Succeeded + RG-scoped Contributor assignment (67aaac02…, 02:46:53Z)" | `TUESDAY/0_Brain/daily/2026-08-21.md:581-584`; the request appears at `:606-611` ("create attio-bridge-rg + RG-scoped Contributor for the SP") |
| Vault-scoped roles: deploy SP = Key Vault Secrets Officer; app MI `6d5d85a8-…` = Key Vault Secrets User | runbook `:98-103` |

**Answer:** the bridge was created and deployed in 2026-08 by **Vision's project SP**. That was not a user login and not an ATTIO-named SP. It ran under Vision's `AZURE_CONFIG_DIR` through the coupled pair. The product owner made the RG-level grant by hand.

**Coupled pair:** yes, it is declared in `ATTIO/CLAUDE.md:21-32` and `Datasec/CLAUDE.md:31-39` ("share one working scope — a session in either may read and write both"). The wording covers project **folders**. It says nothing about Azure identity. `ATTIO/CLAUDE.md:38-41` says new Attio-side resources need tenant/subscription "confirmed per hard rule 4 before any `az` work". So in practice the coupling reaches Azure only through the explicit 08-21 grant, not by declaration.

## Q2. Per-project az config dirs under `Datasec/*/4_Credentials/.azure` (names + profile identity only)

| Project | Tenant | Subscription(s) | Identity (type) |
|---|---|---|---|
| CypherKey | d500ebad | 29b5c7de (CypherKey) | d2efb3de-… (servicePrincipal) |
| Datasec MPS Commercial Calculator | ec01829b | a6b8fe11, 73e9b141 | kamil@datasec-rd.com (user) |
| Datasec Security Composer | d500ebad | 0c57ab37, 29b5c7de | kreiser.org@me.com (**user**) |
| HPSM-POC | ec01829b | a6b8fe11, 73e9b141 | kamil@datasec-rd.com (user) |
| HPSM | d500ebad | 0c57ab37 (SP 4ddb4f7b-…); 29b5c7de (kreiser.org@me.com user) | mixed |
| Lead_Bot | — | none | — |
| myPKI | d500ebad | 0c57ab37 | 4da256f7-… (servicePrincipal) |
| NexusAI | d500ebad | 0c57ab37 | a71b85e7-… (servicePrincipal) |
| Security Review | — | `azureProfile.json` present: False (dir empty) | — |
| **Vision_Sales_Portal** | **d500ebad** | **0c57ab37** | **bc1e3581-… (servicePrincipal) = the bridge's deploy SP** |
| ATTIO | — | no `.azure` dir (it is not in the listing; B1028 drafter report :23 says the same) | — |

**Only Vision's dir is recorded as able to reach `attio-bridge-rg`.** Two dirs (Security Composer, HPSM's CypherKey sub) hold the **product owner's own user login** in this tenant. Using them would mean acting as him, which is the workaround the rule forbids. They are named only so nobody picks them up. Other SPs (NexusAI, myPKI, HPSM, CypherKey) have no recorded grant on `attio-bridge-rg`. Their rights were not measured; they were not checked, and should not be tried.

**ATTIO-named SP grep:** pattern `attio[-_a-z]*-claude-deploy|attio-deploy-sp|attio[-_]sp\b` over `!CODING/Datasec/**/*.md` + workspace `CLAUDE.md`: **0 hits**. Control `vision-sales-portal-claude-deploy` over the same set: **2 hits** (so the grep can find SP names). A broader `attio` + `service principal|claude-deploy|role assignment` line filter returned only two unrelated Vision history lines (`:2131`, `:2145`, a healthz GET).

## Q3. Role assignment scoped to `attio-bridge-rg`

Yes, one is recorded: an RG-scoped **Contributor** for the Vision SP, assignment `67aaac02…`, 2026-08-21 02:46:53Z, made by the product owner (`TUESDAY/0_Brain/daily/2026-08-21.md:581-584`; the "nothing at subscription scope" boundary at `Notes (MASTER)/daily/2026-08-21.md:389`). There are also two **vault-scoped** roles on `attio-bridge-kv` (runbook `:98-103`). No record says it was revoked. No record re-measures it after 08-21 either. Later bridge work (08-23 deploy, 08-24 Kudu runs, ATTIO history `:150`, `:517-519`) implies it still worked then. Contributor on the RG already covers `Microsoft.Web/sites/config/write`, so no new grant is needed if it is still in place.

## Q4. Is `FOLLOWUP_DIGEST_TO` a plain setting or a KV reference?

From records, it is **most likely plain, but not measured.**
- Code reads it as a plain env var: `ATTIO/2_Project_Files/src/config.js:94` (`digestTo: env.FOLLOWUP_DIGEST_TO || null`), listed in `REQUIRED.digest` at `:27`.
- The design doc says the job's Azure changes were "app settings and **one** Key Vault secret" (`ATTIO/1_Project_Definition/2026-08-21_ATTIO-29_daily-followup-design.md:29-30`). An email address isn't a secret, and the one KV secret is most plausibly `AGENTMAIL_API_KEY`. That is an inference; no file names which secret it is.
- The runbook's settings table (`:86-92`) predates ATTIO-29 and does not list it. No file records how `FOLLOWUP_DIGEST_TO` was set.
- So the kit must keep B1028's step: print True/False only on the `@Microsoft.KeyVault(` prefix before writing (`TUESDAY/.../2026-11-01_B1028_SEAT-AT1_…md:71`).

## What the agent route would look like (for Tuesday's kit, not run here)

Run under Vision's `AZURE_CONFIG_DIR`, on Opus (G1 per B1028 :71):
1. `az account show`: assert tenant `d500ebad…`, sub `0c57ab37…`, SP `bc1e3581…`.
2. Read-only: confirm a role assignment for object id `1b3bee22…` still exists at `/subscriptions/0c57ab37…/resourceGroups/attio-bridge-rg`. If it is absent or the call is refused, STOP. That is the boundary; report it, do not escalate.
3. Check the KV prefix and print True/False only.
4. `az webapp config appsettings set -g attio-bridge-rg -n datasec-attio-bridge --settings FOLLOWUP_DIGEST_TO=tuesday-agent@agentmail.to -o none`.
5. Read back with True/False equality only. Check `/healthz` shows the schedule armed (runbook `:113-116`). The restart resets the in-memory webhook ledger (`:310`).

If the product owner would rather not have the Vision SP do it, the narrowest new identity would be a dedicated SP (e.g. `attio-claude-deploy`) with **Website Contributor scoped to the one web app**. He would run something like this (placeholders left unsubstituted):
`az ad sp create-for-rbac --name attio-claude-deploy --role "Website Contributor" --scopes /subscriptions/0c57ab37-…/resourceGroups/attio-bridge-rg/providers/Microsoft.Web/sites/datasec-attio-bridge`
and then log it into a new `ATTIO/4_Credentials/.azure`. That costs him more steps than the 2-minute portal edit.

---

## Draft BLUF for the follow-up card (to be read aloud, ~120 words)

**I can make the digest change today without any new access from you.** The identity that built the bridge in August is Vision's agent identity. You gave it Contributor on the bridge's resource group yourself on 21 August. So option b only needs that grant to still be there, and the agent checks that before writing anything. One thing you should know: that same identity can also reach Vision's live site. The agent will name the bridge explicitly in every command and stop if anything doesn't match. Your options: **one**, the agent does it with Vision's identity, today, before the 7am digest; **two**, you change the one setting in the portal yourself, about two minutes; **three**, you create an ATTIO-only identity first, which is slower. **I recommend one.**
