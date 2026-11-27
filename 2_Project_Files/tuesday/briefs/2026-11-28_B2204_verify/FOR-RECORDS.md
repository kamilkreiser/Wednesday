# FOR RECORDS: lane AZ-1 round 2, the Bicep of the mock client environment's foundation, gate round 1 of 2 (kit B2191, seat X99), head 14896ed0 (gate B2204: see VERDICT.md line 1)

For the records lane only, AFTER a landing of this gated head (its squash on main); nothing here is written into a
project file by the gate. Who decided every choice of this lane: the coordinator (Tuesday), as coordinator, never the
product owner (kit B2191 THE AUTHORITY; stamp S4 states Q1 to Q4 "a" in words). The az rule and the A$120 grant row
are quoted as the product owner's (OXPd CLAUDE.md:59-60; EXPIRING-GRANTS line 9). Nothing was deployed; what-if only;
the gate ran no az command.

## Plan lane AZ-1: DONE as a template of what exists (on this squash)
(RELAYED from the kit's FOR RECORDS; CHECKED by the gate from the seat's saved answers: every judge line re-run and
byte-equal; resources and deployments unchanged.)
- `deploy/azure/main.bicep` declares the mock client foundation that the agent login built by CLI in `oxpd2-dev-rg`
  (13 declared resources). Checked by `az deployment group what-if` (Incremental, FullResourcePayloads) under the agent
  login: 10 declared resources `NoChange`, 3 `Modify` only on six listed values Azure sets itself, 2 undeclared
  resources `Ignore`; five planted differences each seen; the group's resource list byte-equal before and after, its
  deployment list empty before and after. A$0 spent; no resource made, changed or deleted.
- Deviations to record: the resources came first (by CLI) and the template second; round 1 (seat X98) stopped on the
  six Azure-set values and the judge gained a closed list of them; the deployment-specific values are a parameters file
  kept outside the repository; the compiled JSON is not committed; the namespace's own `RootManageSharedAccessKey`
  rule, the vault's public network access and its missing purge protection are stated as known differences, not
  changed.

## THE NOISE LIST AND ITS LIFE (a later Azure lane inherits it)
The six tuples (type, name, path, change, before, after), from the saved answer of 2026-11-28 (X98's, saved before it stopped at
00:59 AEDT, and byte-equal again at 03:01 in X99's run):
- N1 `microsoft.network/privateendpoints` `oxpd2-mock-pe-relay` `properties.ipVersionType` Delete, before `"IPv4"`.
- N2 to N5 `microsoft.network/privateendpoints/privatednszonegroups` `oxpd2-mock-pe-relay/default`
  `properties.privateDnsZoneConfigs.0.` `etag` / `id` / `properties.provisioningState` / `type`, each Delete.
- N6 `microsoft.relay/namespaces` `oxpd2-mock-relay` `properties.privateEndpointConnections` Delete, before ONE
  connection (group `namespace`, endpoint `oxpd2-mock-pe-relay`, `Auto-Approved` / `Approved`).
**Each tuple holds only while a fresh what-if answer still prints it exactly.** N2's etag changes whenever the zone
group is written; N6 changes if a second endpoint connection appears or its state changes; N1 retires if a later lane
moves the endpoint to an API version that states `ipVersionType` (Q3 b). A changed value is NOT noise: the judge prints
it as a PROTECTED DELTA and FAILS (conservative; the gate's look-alike probes confirm). A later lane that changes any of
these resources re-derives its NOISE from its own fresh answer under its own kit; it never widens the list to a rule.
**What a real deployment does to these six values is UNMEASURED** (what-if predicts `Delete` for each; N6 is the
namespace's only network path). The first lane that runs a `create` from this file over an existing group proves N6
survives first (VERDICT.md I3).

## For later lanes (gate findings; grades and evidence in VERDICT.md)
- **The server lane (the first compute in snet-server), F1 MAJOR:** the NSG keeps Azure's default outbound rules
  (`AllowVnetOutBound` 65000, `AllowInternetOutBound` 65001; MEASURED in X92's create answer), so outbound is NOT limited
  to the private endpoint subnet as README lines 6-7 and main.bicep line 47 say. Add a deny-all-outbound rule (a change
  to what exists: its own what-if, then a create under its brief) or reword both texts to what exists.
- **The rewording lane, F2 and F3 MINOR:** the README's check sentence (no `Modify`) is stricter than the check that
  passed (NoEffect-only and NOISE-only `Modify` accepted); the README's known differences omit the log store's public
  ingestion and query (`Enabled`).
- **Security of what the template describes (each a later lane's decision; never this commit's):** S1 the Relay
  namespace's `RootManageSharedAccessKey` (Listen, Manage, Send) with no `disableLocalAuth` at API 2021-11-01 (a newer
  API UNMEASURED); S2 the key vault's public network access with no `networkAcls`, no purge protection (enabling it is
  irreversible: approval-class) and the minimum 7-day soft delete; S3 the log store's public ingestion and query.
- **The Marketplace mainTemplate lane (kit NOT DECIDED 1):** no Marketplace template test has run; the address defaults
  (`10.232.0.0/24`, `/26`, `10.232.0.64/28`) and the "mock client environment" comments are this environment's; the
  template holds no subscription, tenant or object id and no public address (gate point c).
- **Judge limits for the next copy of `whatif2189.py`:** a `NoChange` row is passed without reading its delta (I1); the
  mDenyInbound expected row is matched by a path prefix, so a second change on the NSG beside it still MATCHes (I2); the
  log store's `features.enableLogAccessUsingOnlyResourcePermissions` reads `NoEffect` with `before null`, so its live
  value is UNMEASURED (I4).
- **CodeQL does not read Bicep** (I5): the PR's Analyze rows are actions, csharp, python.

## GATE SCANS OF THE LANDING TEXTS (measured 03:22 to 03:24 AEDT in the gate's scratch)
- `squash_scan.py` (the head's `build/squash_scan.py`, in the gate's scratch clone) over squash-subject.txt with `#64`
  in place of `#PRNUM` (238 bytes) and squash-body.txt: `SQUASH-SCAN: control ... rc 1, found 2`, `message: rc 0,
  found 0`, `SQUASH-SCAN: clean`.
- `words.py` (lane copy) over the subject with `#64`, squash-body.txt and pr-title.txt: `WORDS: clean (3 files)`. The
  body's first draft counted 1 ("auto-approved"); it was reworded before this scan. pr-body.md is NOT a repository text
  and is not words-clean by design (it names the coordinator's choices and the product owner, as the form asks; its
  only non-ASCII bytes are the generated-by line's emoji).

## Records-lane checklist after the landing
- The squash on main: one parent, tree equal to the head's (`0f84e8d9...` when main is `d9f89115`); `deploy/azure`
  holds exactly README.md and main.bicep; main's push run `HOSTED <sha>: PASS` at the step-3 numbers.
- Plan r2 lane AZ-1 marked done (template of what exists, what-if proven); F1 to the server lane's kit; F2, F3, S1 to
  S3 to the rewording / security lane; I3 to the first deploying lane.
- The lane folder `<project>/.tools/b2191-x99/` holds the saved answers (the evidence of this record): keep it.
