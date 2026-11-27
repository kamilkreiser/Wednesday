# FOR RECORDS: lane AZ-1, the Bicep of the mock client environment's foundation, gate rounds 1 and 2 of 2 (kit B2191 seat X99, head 14896ed0, gate B2204; kit B2205 seat X104, head 24e94ef2, gate B2206: see VERDICT.md line 1)

For the records lane only, AFTER a landing of the gated head `24e94ef2a9df278d0797fadc8954a5ff4e90ede3` (its squash on
main); nothing here is written into a project file by the gate. Who decided every choice of this lane: the coordinator
(Tuesday), as coordinator, never the product owner (kit B2191 and kit B2205 THE AUTHORITY; stamps S4: B2191 Q1 to Q4
"a", B2205 Q1 to Q3 "a", each in words). Nothing was deployed; what-if only (round 1); round 2 ran no az command at
all; neither gate ran an az command. This file REPLACES `../2026-11-28_B2204_verify/FOR-RECORDS.md` for the landing
(that one pins the void head 14896ed0); its NOISE section is carried here whole.

## Plan lane AZ-1: DONE as a template of what exists, its text true to it (on this squash)
- **Round 1 (seat X99, commit `14896ed0`, gate B2204 GO WITH FINDINGS, Major 1, Minor 4, Info 8):**
  `deploy/azure/main.bicep` declares the mock client foundation that the agent login built by CLI in `oxpd2-dev-rg`
  (13 declared resources). Checked by `az deployment group what-if` (Incremental, FullResourcePayloads) under the
  agent login: 10 declared resources `NoChange`, 3 `Modify` only on six listed values Azure sets itself, 2 undeclared
  resources `Ignore`; five planted differences each seen; the group's resource list byte-equal before and after, its
  deployment list empty before and after. A$0 spent; no resource made, changed or deleted. (RELAYED from B2204,
  checked there from the seat's saved answers.)
- **Round 2 (seat X104, commit `24e94ef2`, fast-forward on `14896ed0`, gate B2206):** TEXT ONLY. The README and the
  `//` comment at main.bicep 47 (now 47-49) say what the template and the group are: the NSG denies every inbound
  flow and does NOT restrict outbound (Azure's default rules allow the virtual network and the Internet; a deny-all
  outbound rule is owed to the server lane) [F1]; the check sentence is the what-if rule that passed (NoChange, or
  Modify whose every changed property is NoEffect or one of six Azure-set values, named in words) [F2]; the known
  differences add the log store's public ingestion and query [F3], the Relay key rule's name and rights and that
  key-based access is not turned off [S1], the key vault's missing network rules and 7-day default retention [S2].
  **The compiled template is byte-equal to the what-if-proven one:** the gate re-built it from the origin's head
  file with the pinned CLI 0.48.1 (sha256 `62cd5958...`): `main.json` `ba7a31d7e6c90eb1596fe7e83b01c7044eb4c8eacf1a0adf5c67645cbade8546`,
  equal to HEAD0's own build; control (one `@description` text changed) `e22b3603...`, differs. So round 1's
  what-if proof carries to the landed head unchanged.
- Deviations to record: the resources came first (by CLI) and the template second; round 1 of seat X98 stopped on
  the six Azure-set values and the judge gained a closed list of them; the deployment-specific values are a
  parameters file kept outside the repository; the compiled JSON is not committed; the text was corrected by a second
  commit on the same branch (no rebase, no force-push) after gate B2204's F1.

## THE NOISE LIST AND ITS LIFE (a later Azure lane inherits it; carried whole from B2204)
The six tuples (type, name, path, change, before, after), from the saved answer of 2026-11-28 (X98's, byte-equal again
at 03:01 in X99's run):
- N1 `microsoft.network/privateendpoints` `oxpd2-mock-pe-relay` `properties.ipVersionType` Delete, before `"IPv4"`.
- N2 to N5 `microsoft.network/privateendpoints/privatednszonegroups` `oxpd2-mock-pe-relay/default`
  `properties.privateDnsZoneConfigs.0.` `etag` / `id` / `properties.provisioningState` / `type`, each Delete.
- N6 `microsoft.relay/namespaces` `oxpd2-mock-relay` `properties.privateEndpointConnections` Delete, before ONE
  connection (group `namespace`, endpoint `oxpd2-mock-pe-relay`, `Auto-Approved` / `Approved`).
**Each tuple holds only while a fresh what-if answer still prints it exactly.** N2's etag changes whenever the zone
group is written; N6 changes if a second endpoint connection appears or its state changes; N1 retires if a later lane
moves the endpoint to an API version that states `ipVersionType`. A changed value is NOT noise: the judge FAILS it. A
later lane re-derives its NOISE from its own fresh answer; it never widens the list to a rule. **What a real
deployment does to these six values is UNMEASURED** (what-if predicts `Delete` for each; N6 is the namespace's only
network path). The first lane that runs a `create` from this file over an existing group proves N6 survives first
(B2204 I3; the README does not state this: B2206 I2).

## For later lanes (grades and evidence in the two VERDICT.md files)
- **The server lane (the first compute in snet-server), F1 (round-1 MAJOR, its text half CLOSED by round 2):** the
  NSG keeps `AllowVnetOutBound` 65000 and `AllowInternetOutBound` 65001 (MEASURED in X92's create answer
  `.tools/b2179-x92/logs/nsg.out`, re-read by B2206). The README now says so and names the server lane as owing a
  deny-all outbound rule: its own what-if, then a create under its brief. Its brief must also list the outbound the
  server itself needs (the key vault and the log store are reached on their public endpoints in this template: no
  private endpoint for either), or the deny rule cuts them (B2206 I3, DERIVED).
- **F2, F3: CLOSED by round 2** (text). **S1, S2: their TEXT closed** (named in the README); the decisions stay
  open: S1 the Relay namespace's `RootManageSharedAccessKey` (Listen, Manage, Send; MEASURED X92 `relay-ns-sas.out`)
  with no `disableLocalAuth` at API 2021-11-01 (a newer API UNMEASURED): local auth off or key custody; S2 the vault's
  public network access with no `networkAcls`, no purge protection (enabling it is irreversible: approval-class) and
  the minimum 7-day soft delete (MEASURED X92 `console-kv-show.txt` lines 15, 22, 25, 30); S3 the log store's public
  ingestion and query.
- **The Marketplace mainTemplate lane (kit B2191 NOT DECIDED 1):** no Marketplace template test has run; the address
  defaults (`10.232.0.0/24`, `/26`, `10.232.0.64/28`) and the "mock client environment" comments are this
  environment's; the template holds no subscription, tenant or object id and no public address. The README's "owed to
  the server lane" is internal process wording a client reader cannot act on (B2206 I1 and Tuesday's point 2): the
  mainTemplate's own README must say what the deploying client does about outbound.
- **Judge limits for the next copy of `whatif2189.py`** (B2204 I1, I2, I4): a `NoChange` row is passed without reading
  its delta; the mDenyInbound expected row is matched by a path prefix; the log store's
  `features.enableLogAccessUsingOnlyResourcePermissions` live value is UNMEASURED.
- **CodeQL does not read Bicep or Markdown** (B2204 I5): the PR's Analyze rows are actions, csharp, python.

## GATE SCANS OF THE LANDING TEXTS (B2206, measured 03:59 to 04:00 AEDT in the gate's scratch `fleet/state/s337/g2206/`)
- `squash_scan.py` (the head's `build/squash_scan.py`, sha256 `d718569b...ef5c`, equal to main aa520ba5's) over
  squash-subject.txt with `#65` in place of `#PRNUM` (238 bytes) and squash-body.txt (2625 bytes): `control ... rc 1,
  found 2`, `message: rc 0, found 0`, `SQUASH-SCAN: clean`, rc 0. **A different number changes the bytes: scan again.**
- `words.py` (sha256 `6f932dc5...`) over the subject with `#65`, squash-body.txt and pr-title.txt: `WORDS: clean (3
  files)`. pr-body.md: every word class 0; its only hits are the 4 non-ASCII bytes of the generated-by line's emoji.
  B-number count 0 and seat/lane words 0 over all four.

## Records-lane checklist after the landing
- The squash on main: ONE parent (the main the landing proved), its tree = that main's files + exactly
  `deploy/azure/README.md` and `deploy/azure/main.bicep` (782 files when main is `aa520ba5`); `contents/deploy/azure`
  lists exactly those two; main's push run `HOSTED <sha>: PASS` at the step-3 numbers of landing.txt.
- Plan r2 lane AZ-1 marked DONE (template of what exists, what-if proven, text true to it; two rounds used); F1's
  rule half to the server lane's kit; S1 to S3 to the security lane; I3 (B2204) to the first deploying lane.
- Keep `<project>/.tools/b2191-x99/` (the saved what-if answers: the evidence of this record) and
  `<project>/.tools/b2205-x104/` (the text round's checks and builds).
