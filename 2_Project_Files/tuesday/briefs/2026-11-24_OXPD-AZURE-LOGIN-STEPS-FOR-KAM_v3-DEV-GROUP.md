# OXPd: a development resource group the agents fully control, under kamil@datasec-rd.com (Datasec/OXPd), for Kam, v3

**Why v3:** your note on the Azure card (board, 10:32): "create a new resource group under kamil@datasec-rd.com. issue new steps so agents have full control to spin up and create services/ vms etc". This replaces v2. If you already ran v2's steps, tell me; nothing in v3 conflicts with them, and v2's group can stay or go on your word.

**One choice is yours, in step 3:** which subscription the group lives in. Your login can see one or more subscriptions; step 3 lists them, and you pick. **My recommendation:** the subscription where your account is Owner. HPSM-POC's record has one: "Azure subscription 1", `a6b8fe11-...`, two months old. **I can't see which you mean:** your card said "keep the agent-controllable environment", but your login doesn't exist there (this morning's error). So the list decides.

**What "full control" means here:** OXPd's agent login gets **Contributor on this one group**. It can create, change and delete any service or VM inside the group, and nothing outside it. It cannot hand out access (that needs Owner, which stays yours). **Cost:** what the agents create in the group is billed to the subscription you pick. My reading of your note: each resource is reported on the board when it's created, and anything over about A$50 a month is carded to you first. Your word changes that.

---

**Step 1.** In a fresh Terminal window, point Azure at OXPd's own folder (the single quotes matter):

```
export AZURE_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/4_Credentials/.azure'
```

**Step 2.** Log in as kamil@datasec-rd.com. It shows a code to enter in the browser:

```
az login --use-device-code
```

**Step 3.** List what your login can see, and pick the subscription:

```
az account list --query '[].{name:name, sub:id, tenant:tenantId}' -o table
```

Then set the one you pick, pasting its `sub` value in place of `<SUB>`:

```
az account set --subscription <SUB>
```

Then check:

```
az account show --query '{tenant:tenantId, sub:id, user:user.name}' -o table
```

The user must read `kamil@datasec-rd.com`. Tell me the tenant and subscription it shows (they are ids, not secrets).

**Step 4.** Check the compute service is on. If it prints `NotRegistered`, run the second line once:

```
az provider show --namespace Microsoft.Compute --query registrationState -o tsv
```

```
az provider register --namespace Microsoft.Compute --wait
```

**Step 5.** Create OXPd's development group (no cost on its own):

```
az group create -n oxpd2-dev-rg -l australiaeast --tags project=OXPd_2 purpose=development owner=kam
```

**Step 6.** Create OXPd's agent login with Contributor on that group only. Its secret goes straight into a private file and never appears on screen. Run the three lines one after the other:

```
umask 077
```

```
SUB=$(az account show --query id -o tsv)
```

```
az ad sp create-for-rbac --name oxpd2-claude-deploy --role Contributor --scopes "/subscriptions/$SUB/resourceGroups/oxpd2-dev-rg" > '/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/4_Credentials/oxpd2-claude-deploy.sp.json'
```

**If step 6 says you lack privileges** (likely "Insufficient privileges"): your account may be a guest in that directory. Stop and send me the message. The empty group costs nothing.

**If v2's step 6 already made `oxpd2-claude-deploy`:** step 6 adds this group to the same login. That's fine.

**Step 7.** Check it, without showing the secret. It must list `Contributor` on `.../resourceGroups/oxpd2-dev-rg`:

```
az role assignment list --all --assignee "$(python3 -c 'import json;print(json.load(open("/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/4_Credentials/oxpd2-claude-deploy.sp.json"))["appId"])')" --query '[].{role:roleDefinitionName, scope:scope}' -o table
```

**Step 8.** Tell me on the board: "OXPd login done", with the tenant and subscription from step 3.

---

**What happens next (no action from you):**
- The OXPd agent logs in and proves its boundary: it can create in `oxpd2-dev-rg`, and it is refused everywhere else.
- Everything it creates is tagged `project=OXPd_2` and reported on the board.
- Nothing of HPSM-POC is touched; its hold stands.
