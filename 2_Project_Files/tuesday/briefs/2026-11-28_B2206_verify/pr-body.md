The Bicep template of the mock client environment's foundation and its README. Two commits on the branch,
`14896ed0` (the template) and `24e94ef2` (text only: the README and one comment made true to the template), on
`main` `d9f89115`. Two files, both added against main: `deploy/azure/main.bicep` and `deploy/azure/README.md`. No
other path, no workflow, no code, no test.

## Why

The mock client environment was built in its resource group by the Azure CLI. This change writes it down as a Bicep
template that describes exactly what exists, the shape a Marketplace `mainTemplate` will later take, and proves the
description by what-if: deploying it over the existing group would change nothing that matters. The README states
what the template does not restrict, so the base of a client-facing template carries no security claim it does not
meet.

## What changed

- **`deploy/azure/main.bicep`** (13 declared resources): the server subnet's network security group (an explicit
  inbound deny at 4096; two outbound allow rules to the private endpoint subnet on 443 and 9400-9599; no outbound
  deny rule), the virtual network and its two subnets, the Relay namespace (Standard, public network access
  `Disabled`) with its hybrid connections (`requiresClientAuthorization: true`, names from a parameter), the private
  DNS zone `privatelink.servicebus.windows.net` and its link, the private endpoint and its DNS zone group, the key
  vault (Azure RBAC, soft delete, no access policies), the Log Analytics workspace (daily cap) and the public DNS
  zone. API versions are pinned. No subscription, tenant or object id and no address but the private-range parameter
  defaults; the vault's tenant is `subscription().tenantId`.
- **`deploy/azure/README.md`**: what the template holds, how it is checked (NoChange, or `Modify` only on `NoEffect`
  properties and six listed values Azure sets itself), and its known differences.

## What proves it

- Compiled with the Bicep CLI 0.48.1 (pinned by hash): 0 warnings. The text-only commit compiles to the same
  `main.json` byte for byte (sha256 `ba7a31d7...8546`); a changed `@description` text, as a control, changes it.
- `az deployment group what-if --mode Incremental --result-format FullResourcePayloads` against the existing group:
  10 declared resources `NoChange`; 3 `Modify` rows whose only effective leaves are six listed values Azure sets
  itself (the endpoint's default `ipVersionType`; the zone config's `etag`, `id`, `type` and `provisioningState`; the
  namespace's private endpoint connection), each matched exactly in type, name, path, change, before and after; 2
  resources the template does not own read `Ignore`; `potentialChanges` 0, diagnostics 0.
- Five planted differences, each its own what-if, each seen as exactly the change planted: Relay public access
  `Enabled`, client authorization `false` (three rows), the inbound deny rule's priority, the vault's RBAC switch, one
  more hybrid connection (`Create`).
- The group's resource list byte-equal before and after; its deployment list empty before and after.
- Both branch pushes: repository rules clean, unit floor 117, secret scan clean (planted control found 25 of 25),
  both build legs `failed: 0` (no test added).

## Still open (stated in the README's known differences)

- **Outbound from the server subnet is not restricted.** The network security group keeps Azure's default rules
  (`AllowVnetOutBound`, `AllowInternetOutBound`); its two allow rules add nothing yet. A rule that denies all other
  outbound traffic is owed by the change that first puts compute in the server subnet (its own what-if first). No
  compute is in that subnet today.
- The Relay namespace keeps the shared access rule Azure creates with it (`RootManageSharedAccessKey`: Listen,
  Manage, Send); key-based access is not turned off.
- The key vault keeps public network access with no network rules, no purge protection (enabling it cannot be
  undone) and the 7-day soft-delete default.
- The log store keeps public network access for ingestion and query.
- What a real deployment does with the six Azure-set values (what-if predicts `Delete` for each, the namespace's only
  endpoint connection among them) is not measured: nothing was deployed. A change that first deploys this template
  over an existing group proves that connection survives first.
- CodeQL does not analyse Bicep or Markdown; the pull request's code scanning covers the repository's code languages
  only.
- Whether the Marketplace `mainTemplate` is produced from this file is not settled; no Marketplace validation ran.

Nothing was deployed; what-if only. No resource was made, changed or deleted.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
