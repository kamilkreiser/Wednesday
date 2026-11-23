# OXPd: creating OXPd's own Azure login (Datasec/OXPd), for Kam

**I need you to do the steps below once, in a fresh Terminal window, when it suits you.** This creates only an empty resource group and a login for OXPd's agent, confined to that group. **Nothing is created that costs money:** the test VM itself waits until the M577's first read works at home and the small echo command is built.

Where this comes from: your answer "Create it as designed" (board, 2026-11-23 20:56). The design is section 2.3 of `tuesday/briefs/2026-11-23_B2001_OXPD-AZURE-PATH-TEST_DESIGN.md`. One change is mine: step 4 checks whether Azure's compute service is switched on before turning it on. I couldn't check that without this login.

Checked by Tuesday in the command just before this file was written: OXPd's Azure folder `OXPd_2/4_Credentials/.azure` exists and is empty, and OXPd's launcher sets `AZURE_CONFIG_DIR` to that folder (`Launch_Claude.command` line 39).

---

**Step 1.** Open a new Terminal window and point Azure at OXPd's own folder (single quotes matter, because of the `!`):

```
export AZURE_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/4_Credentials/.azure'
```

**Step 2.** Check it took (it must print the OXPd path above):

```
echo "$AZURE_CONFIG_DIR"
```

**Step 3.** Log in to the agent-controllable environment, choose Azure subscription 1, and check (it shows a code to enter in the browser):

```
az login --tenant d500ebad-cf53-4f2a-a501-f831289e67fc --use-device-code
```

```
az account set --subscription 0c57ab37-349c-47ae-a10f-e284a380bbb9
```

```
az account show --query '{tenant:tenantId, sub:id, user:user.name}' -o table
```

The tenant must read `d500ebad-...` and the subscription `0c57ab37-...`. Anything else: stop and tell me.

**Step 4.** Check whether the compute service is switched on:

```
az provider show --namespace Microsoft.Compute --query registrationState -o tsv
```

If it prints `Registered`, go to step 5. If it prints `NotRegistered`, run this once (it takes a minute or two):

```
az provider register --namespace Microsoft.Compute --wait
```

**Step 5.** Create the empty resource group (no cost):

```
az group create -n oxpd2-s14-path-test-rg -l australiaeast --tags project=OXPd_2 purpose=S14-path-test owner=kam
```

**Step 6.** Create OXPd's agent login, allowed into this group only. Its secret goes straight into a private file and never appears on screen. Run the two lines one after the other:

```
umask 077
```

```
az ad sp create-for-rbac --name oxpd2-claude-deploy --role Contributor --scopes /subscriptions/0c57ab37-349c-47ae-a10f-e284a380bbb9/resourceGroups/oxpd2-s14-path-test-rg > '/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/4_Credentials/oxpd2-claude-deploy.sp.json'
```

**Step 7.** Check it, without showing the secret. It must list exactly one line: `Contributor` on `.../resourceGroups/oxpd2-s14-path-test-rg`:

```
az role assignment list --all --assignee "$(python3 -c 'import json;print(json.load(open("/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/4_Credentials/oxpd2-claude-deploy.sp.json"))["appId"])')" --query '[].{role:roleDefinitionName, scope:scope}' -o table
```

**Step 8.** Tell me on the board: "OXPd login done".

---

**What happens next (no action from you):**
- The OXPd agent logs in as that login and proves its boundary first. It can see the new group. It must be refused on the sales portal's production group: that refusal is the boundary working, and is never worked around.
- No VM exists until both gates pass:
  - The M577's first read at home works (this waits on the admin password).
  - The echo command is built.
- When both pass, the test runs for at most 8 hours and is deleted the same day. The design's measured cost is about 23 cents.
