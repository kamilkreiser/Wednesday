# OXPd: creating OXPd's own Azure login in the HPSM-POC directory (Datasec/OXPd), for Kam, v2

**Why v2:** the first version logged you in to the agent-controllable directory (`d500ebad-...`, "Default Directory"), where `kamil@datasec-rd.com` has no account. That is the error in your screenshot. You asked for the same directory as HPSM-POC, so every step below points there.

**HPSM-POC's directory, as its own record has it** (HPSM-POC `CLARIFICATIONS.md` C-07, measured 2026-09-23 from your login): tenant `kamildatasecrd.onmicrosoft.com` (`ec01829b-fdcb-4503-9834-eb2ffbd99169`), subscription "Azure subscription 1" (`a6b8fe11-d1b5-4293-8727-b34aba08a705`), you as **Owner**, signed in as `kamil@datasec-rd.com` (a guest there). That record is two months old, so step 3 checks it live before anything is created.

**Two things to know before you start:**
- **The cost lands on the HPSM-POC subscription.** Your C-07 words: its credits fund that project. The test VM is about 23 cents for a day, and nothing in these steps costs money.
- **OXPd's login is confined to its own new group.** It cannot reach any HPSM-POC resource. When OXPd's agent first logs in, it proves this: it must be refused on HPSM-POC's groups, and that refusal is never worked around. Nothing of HPSM-POC is touched (its hold until 10 December stands).

**I need you to do the steps below once, in a fresh Terminal window.** OXPd keeps its own Azure folder, so this login never mixes with HPSM-POC's or anyone else's.

---

**Step 1.** Open a new Terminal window and point Azure at OXPd's own folder. The single quotes matter, because of the `!`:

```
export AZURE_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/4_Credentials/.azure'
```

**Step 2.** Check it took. It must print the OXPd path above:

```
echo "$AZURE_CONFIG_DIR"
```

**Step 3.** Log in to the HPSM-POC directory. It shows a code to enter in the browser; pick `kamil@datasec-rd.com`:

```
az login --tenant ec01829b-fdcb-4503-9834-eb2ffbd99169 --use-device-code
```

Then select the subscription:

```
az account set --subscription a6b8fe11-d1b5-4293-8727-b34aba08a705
```

Then check:

```
az account show --query '{tenant:tenantId, sub:id, user:user.name}' -o table
```

The tenant must read `ec01829b-...`, the subscription `a6b8fe11-...` and the user `kamil@datasec-rd.com`. Anything else: stop and tell me.

**Step 4.** Check whether the compute service is switched on:

```
az provider show --namespace Microsoft.Compute --query registrationState -o tsv
```

If it prints `Registered`, go to step 5. If it prints `NotRegistered`, run this once (it takes a minute or two):

```
az provider register --namespace Microsoft.Compute --wait
```

**Step 5.** Create OXPd's empty resource group (no cost):

```
az group create -n oxpd2-s14-path-test-rg -l australiaeast --tags project=OXPd_2 purpose=S14-path-test owner=kam
```

**Step 6.** Create OXPd's agent login, allowed into this group only. Its secret goes straight into a private file and never appears on screen. Run the two lines one after the other:

```
umask 077
```

```
az ad sp create-for-rbac --name oxpd2-claude-deploy --role Contributor --scopes /subscriptions/a6b8fe11-d1b5-4293-8727-b34aba08a705/resourceGroups/oxpd2-s14-path-test-rg > '/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/4_Credentials/oxpd2-claude-deploy.sp.json'
```

**If step 6 says you lack privileges** (likely to be "Insufficient privileges"): you are a guest in this directory, and the directory may stop guests creating app logins. Stop there and tell me the message. I'll card the options; one is that the directory's admin account runs step 6. Nothing is half-made: the empty group from step 5 costs nothing.

**Step 7.** Check it, without showing the secret. It must list exactly one line, `Contributor` on `.../resourceGroups/oxpd2-s14-path-test-rg`:

```
az role assignment list --all --assignee "$(python3 -c 'import json;print(json.load(open("/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/4_Credentials/oxpd2-claude-deploy.sp.json"))["appId"])')" --query '[].{role:roleDefinitionName, scope:scope}' -o table
```

**Step 8.** Tell me on the board: "OXPd login done".

---

**What happens next (no action from you):** the OXPd agent logs in as that login and proves its boundary: it can see the new group, and it must be refused on HPSM-POC's groups. No VM exists until the M577's first read works at home and the echo command is built; then the test runs at most 8 hours and is deleted the same day.

**What I could not check:** whether your login still holds Owner on that subscription today (step 3 shows it), and whether the directory lets a guest create an app login (step 6 shows it).
