The Bicep template of the mock client environment's foundation. One commit, `14896ed0`, on `main` `d9f89115` (behind 0,
ahead 1). Two files, both added: `deploy/azure/main.bicep` and `deploy/azure/README.md`. No other path, no workflow, no
code, no test.

## Why

The mock client environment was built in its resource group by the Azure CLI. This change writes it down as a Bicep
template that describes exactly what exists, the shape a Marketplace `mainTemplate` will later take, and proves the
description by what-if: deploying it over the existing group would change nothing that matters.

## What changed

- **`deploy/azure/main.bicep`** (13 declared resources): the server subnet's network security group (inbound deny at
  4096; outbound allow to the private endpoint subnet on 443 and 9400-9599), the virtual network and its two subnets, the
  Relay namespace (Standard, public network access `Disabled`) with its hybrid connections (`requiresClientAuthorization:
  true`, names from a parameter), the private DNS zone `privatelink.servicebus.windows.net` and its link, the private
  endpoint and its DNS zone group, the key vault (Azure RBAC, soft delete, no access policies), the Log Analytics
  workspace (daily cap) and the public DNS zone. API versions are pinned. No subscription, tenant or object id and no
  address but the private-range parameter defaults; the vault's tenant is `subscription().tenantId`.
- **`deploy/azure/README.md`**: what the template holds, how it is checked, and its known differences.

## What proves it

- Compiled with the Bicep CLI 0.48.1 (pinned by hash): 0 warnings.
- `az deployment group what-if --mode Incremental --result-format FullResourcePayloads` against the existing group:
  10 declared resources `NoChange`; 3 `Modify` rows whose only effective leaves are six listed values Azure sets
  itself (the endpoint's default `ipVersionType`; the zone config's `etag`, `id`, `type` and `provisioningState`; the
  namespace's auto-approved private endpoint connection), each matched exactly in type, name, path, change, before and
  after; 2 resources the template does not own read `Ignore` (the endpoint's network interface and an unrelated
  network); `potentialChanges` 0, diagnostics 0. The answer was byte-equal to the earlier attempt's, two hours apart.
- Five planted differences, each its own what-if, each seen as exactly the change planted: Relay public access
  `Enabled`, client authorization `false` (three rows), the inbound deny rule's priority, the vault's RBAC switch, one
  more hybrid connection (`Create`).
- The group's resource list byte-equal before and after; its deployment list empty before and after.
- Repository rules `RULES: clean (764 files)`; unit floor 117; secret scan clean (planted control found 25 of 25);
  both build legs `total: 2539`, `failed: 0` (no test added).

## Still open

- **The NSG keeps Azure's default outbound rules** (`AllowVnetOutBound`, `AllowInternetOutBound`): outbound from the
  server subnet is not restricted to the private endpoint subnet, though the README and a comment say it is. No compute
  is in that subnet yet; the lane that adds the server decides between a deny-all-outbound rule and a reworded README.
- The README's check sentence says no resource reads `Modify`; the check run accepts `Modify` rows whose effective
  leaves are only the six listed Azure-set values. A later change rewords it.
- Known differences kept as they exist: the key vault's public network access and missing purge protection; the log
  store's public ingestion and query; the Relay namespace's own `RootManageSharedAccessKey` rule (not declared, not
  removed).
- What a real deployment does with the six Azure-set values (what-if predicts `Delete` for each, the namespace's only
  endpoint connection among them) is not measured: nothing was deployed.
- CodeQL does not analyse Bicep; the pull request's code scanning covers the repository's code languages only.
- Whether the Marketplace `mainTemplate` is produced from this file is not decided; no Marketplace validation ran.

## Who decides

The coordinator chose, as coordinator, this change and every choice in it (describe what exists only; the closed list
of six Azure-set values; deployment-specific values in a parameters file outside the repository; the compiled JSON not
committed; the pinned API versions; the five planted differences). No choice in this change is the product owner's.

Nothing was deployed; what-if only. No resource was made, changed or deleted.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
