# QA Gate 115 verdict: Secuura/Distributed_Secuura PR 1933 (KS-1725, @azure/identity ^4.14.1 -> msal-node 7.1.2; GHSA-xcx6-jx8p-x3h5 baseline row deleted), TIER 1

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.**
- **The advisory leaves.** At head, `audit:gate` gives rc 0 (9 reported, 9 baselined). `audit:locks` gives rc 0 over 44 standalone locks (7 match, 7 baselined). `audit:contract` passes 59/59. The id GHSA-xcx6-jx8p-x3h5 appears 0 times in either log and 0 times anywhere in the tree (`git grep` rc 1; the zod id is the control, 2 hits).
- **The control goes red.** Base locks with the PR's baseline make both gates exit 1 and name GHSA-xcx6-jx8p-x3h5. `audit:gate` finds it in the root lock; `audit:locks` finds 6.0.1 in packages/shared and services/m365-integration.
- **An independent scan agrees.** I read every `@azure/msal-node` entry in all 46 tracked locks with semver: base 3 vulnerable of 5 copies, head 0 of 5, current develop 3 of 5.
- **The lock diffs stay inside @azure/identity's closure.** The only packages added or moved are @azure/identity, its msal-node and msal-common, and the `open` subtree. No install script was added. No resolved URL points off registry.npmjs.org.
- **The baseline change is only the msal row.** Exactly that row is deleted (7 lines, 0 added). The other 9 rows are deep-equal and in the same order, and none is re-dated.
- **Suites and tsc re-measure equal at base and head.** m365 is 280/280 at both. packages/shared is 1152/1153 at both (KS 1727 red at both). tsc gives the same error set at base and head.
- **merge-tree is clean.** It is clean on develop `bc8558db` (develop moved during the gate; the PR head did not) and changes exactly the PR's 6 paths with byte-identical blobs.
- **New measurement on the production path.** The production consumer is auth's JWT key load from Key Vault through a Container Apps managed identity. I ran it against a stand-in, and msal 7.1.2 behaves exactly as 6.0.1 does (G115-F1). That narrows the author's UNMEASURED item; it does not close it.

## Heads
- START (logs/head_start.log, 07:54:42Z): PR head `750da5097e6ba79c0c8c624da4de0f5e2acd4a9d` (matches), parent = merge-base `8f313815f415c65849210f5d3e30cae44d15a516` (matches), develop `466a0d6c4c55b110bdb0384bf8c2d6c864b8a1d1` (matches). One commit, author kksecura, subject 89 bytes, starting "KS-1725:".
- END (logs/head_end.log, 08:08:02Z): PR head unchanged. **Develop moved to `bc8558db6b664967192dba55df844d73fcfe7cc6`** (one commit, KS-1868 auth catches). 466a0d6c is an ancestor of it. Re-checked: see Q6.
- Diffstat (logs/diffstat.log): 6 files, +197/-69, exactly as claimed. Root lock +81/-18, the two standalone locks +57/-21 each, the two package.json files +1/-1 each, baseline -7.
- **PR body not read directly** (no `gh` for the Secuura account in this session). I used the commit message plus the author's BUILT AND PROVEN and READY FOR GATE mails (evidence/). Body wording I could not see is NOT verified.
- Node v26.8.1, npm 11.19.0. **Nothing was measured on Node 24.**

## FINDINGS
- **G115-F1 (INFO, recommended for the PR body; measured)**
  - **Who uses the msal-7 copy in production.** The auth service: `services/auth/src/services/jwt.ts:109` `initJwtKeys` -> `getSecretsManager` -> `packages/shared/src/vault/key-vault.ts:190` `new DefaultAzureCredential()`.
  - **How it is deployed.** On Azure Container Apps with a SystemAssigned identity, and `AZURE_KEY_VAULT_URL` set when `keyVaultName` is passed (`deployment/azure/services.bicep:760-761, :943-949`).
  - **Which msal it gets.** The images install packages/shared from its standalone lock (`services/*/Dockerfile` shared-builder stage: `COPY packages/shared/package*.json` then `npm ci`). That is msal-node 7.1.2 at head.
  - **Which credential runs.** In that environment the chain lands on ManagedIdentityCredential. identity 4.14.1 builds it on msal-node's `ManagedIdentityApplication` (`dist/commonjs/credentials/managedIdentityCredential/index.js:24, :84`).
  - **The probe.** scripts/mi_probe.cjs uses exactly the no-options constructor. It strips every AZURE_/IDENTITY_/MSI_ variable, then sets `IDENTITY_ENDPOINT` (a 127.0.0.1 stand-in) and `IDENTITY_HEADER`, the Container Apps shape.
  - **Result.** It gets the same result at base (identity 4.13.3 / msal 6.0.1) and head (4.14.1 / 7.1.2), both through the standalone install and through the root workspace install (7.1.2):
    - one `GET /msi/token?api-version=2019-08-01&resource=https%3A%2F%2Fvault.azure.net`, with the `x-identity-header` set;
    - the stand-in token is returned (its token matches; it expires in about 3600 s);
    - a second call is served from cache (same token, no second request).
    - Logs: logs/mi_probe_{base,head,head_root}.log.
  - **If it failed, auth still starts.** A failure here falls back to `JWT_PRIVATE_KEY` (jwt.ts:107-118, bicep :939), so auth would start, but silently off the vault.
  - **Still unmeasured:** the real Container Apps endpoint, the Key Vault `SecretClient` challenge/`getSecret` round trip, and the EnvironmentCredential no-options path at msal 7 (G115-F7).
- **G115-F2 (INFO, measured; this is part (b), the closure question)** The full lock diff is in logs/lockdiff.log (scripts/lockdiff.py).
  - **Version moves.** Every entry whose resolved version moved has only dependents inside @azure/identity's closure:
    - root: identity 4.13.1 -> 4.14.1; nested msal-node 5.3.1 -> 7.1.2 and msal-common 16.11.0 -> 16.15.0; open 10.2.0 -> 11.0.4; wsl-utils 0.1.0 -> 1.0.1; default-browser 5.5.0 -> 5.5.1 (required by open 11's `^5.5.1`); bundle-name 4.1.0 -> 4.1.1 (its only dependent is default-browser).
    - standalone locks: identity 4.13.3 -> 4.14.1; msal-node 6.0.1 -> 7.1.2; open; wsl-utils.
  - **New packages** (all MIT, all from registry.npmjs.org, none with an install script):
    - `@azure/core-process` 1.0.0 (root only; the standalone locks already had it);
    - `is-in-ssh` 1.0.0;
    - `powershell-utils` 0.2.1;
    - nested `@azure/msal-common` 16.15.0 entries.
  - **Install scripts.** The `hasInstallScript` count is unchanged at 12/2/2. Non-registry `resolved` count: 0 at base and 0 at head, in all three locks.
  - **Normalisation only.** Six root entries gained `resolved` and `integrity` with no version change: default-browser-id, define-lazy-prop, is-docker, is-inside-container, is-wsl, run-applescript. This is npm normalising the entries it re-reified. No other package moved.
  - **Advisories on the new versions.** The registry bulk-advisory read (logs/bulk_advisory.json) finds no advisory for any of the new or moved versions. For msal-node it returns only GHSA-xcx6 with range `>=5.0.0-beta.0 <7.1.0`, so 7.1.2 and 3.8.10 are both outside it.
- **G115-F3 (INFO, measured)** The root-lock entry for @azure/identity now declares `engines.node >=22` (it was >=20), and @azure/core-process also needs >=22. The standalone locks already required >=22 at base. Every Node Dockerfile in the tree is `node:24-alpine` (75 FROM lines; none on node 20 or 22), and `npm ci` printed 0 EBADENGINE warnings. No impact. Recorded for anyone running services on Node 20 locally.
- **G115-F4 (INFO, follow-up, not this PR)** The uuid row GHSA-w5hq-g745-h8pq still says "The v5.x msal-node copy under @azure/identity resolves uuid outside the vulnerable range". That copy no longer exists at head. The row itself is still needed: uuid is still reported (9 reported, 9 baselined), through m365's msal-node 3.8.10 path. The brief forbids touching other rows, so this is reason-text drift for whoever next edits the file.
- **G115-F5 (INFO, follow-up)** services/m365-integration declares `@azure/identity`, but no m365 source imports it. `git grep` finds only `token-manager.ts:17`, which imports `@azure/msal-node`; it does find the key-vault.ts import, which serves as the control. The m365 bump is lock hygiene. Dropping the unused dependency would remove one lock carrier of this whole subtree.
- **G115-F6 (INFO, how the PR's numbers are worded)**
  - "7/7 locks over 44" is really "7 advisories match, 7 baselined, over 44 standalone locks" (plus the workspace root through audit:gate). It is a count of advisories, not of locks.
  - packages/shared: my base run was 1152/1153, not 1151/1153; the KS 1155 timeout did not recur. So "1151 -> 1152" is a flake, not an effect of this PR. The ratio is unchanged by the PR.
  - tsc for packages/shared: my scratch tsconfig (evidence/tsconfig.gate115.json, src including `__tests__`) gives 24 = 24, the identical sorted error set. The author's 23 = 23 used a different scratch config. The invariant holds: base equals head.
- **G115-F7 (INFO, partly read and partly run)** msal-node 6 -> 7 breaking changes (logs/msal_node_CHANGELOG.md):
  - 6.0.0 and 7.0.0 only change `acquireTokenInteractive` responseMode and loopback. That API has 0 call sites.
  - 7.0.2/7.1.0 "sanitize authorization code payloads and reject unsupported instance-aware inputs for confidential clients". The repo's own ConfidentialClientApplication (`token-manager.ts`, the `acquireTokenByCode` path) resolves msal-node **3.8.10 at base and head** (logs/resolve_*.log), so this PR does not change it.
  - Inside identity, msal 7's confidential client is used only by EnvironmentCredential/WorkloadIdentity (client credentials). The author's stand-in measured that path equal, with `disableInstanceDiscovery`. The no-options form stays UNMEASURED (I did not run it).
  - The managed-identity form, the one production uses, is measured equal (F1).

## Q1. The advisory leaves (part a)
| cell (scripts/control.sh; logs/ctl_*.log; sha256 restore asserted after each, all OK) | audit:gate rc / names xcx6 | audit:locks rc / names xcx6 |
|---|---|---|
| head (real) | 0 / 0 (9 reported, 9 baselined) | 0 / 0 (44 locks, 7 match, 7 baselined) |
| C3 base (real) | 0 (10/10) | 0 (8/8) |
| C1 base locks + head baseline | **1 / names it** | **1 / names it (6.0.1 in packages/shared, services/m365-integration)** |
| C2 head locks, zod row also removed | 1, names only GHSA-mrhx (zod) | 1, names only GHSA-mrhx |
| C4 head locks + base baseline | 0, prints `CLEANUP ... GHSA-xcx6-jx8p-x3h5 (@azure/msal-node, KS-1725)` | 0 |
- Locks checked: 46 tracked. audit:gate covers the workspace root `Blockchain/Dev/package-lock.json`; audit:locks covers the other 44; 1 is out of scope (mobile/secuura-app, KS-769). My independent scan (scripts/msal_scan.mjs, logs/msal_scan.log) read all 46 and found msal-node only in the root, packages/shared and m365-integration locks.
- `audit:contract`: 59/59 at head (logs/head_audit_contract.log).

## Q2. Callers and behaviour (part c) (logs/resolve_head.log, resolve_head_after_rootci.log, resolve_base_rootci.log)
- **token-manager.ts** (`ConfidentialClientApplication`, `acquireTokenByCode`): resolves msal-node **3.8.10** at base and at head, under both the standalone and the workspace-root install. Unchanged.
- **key-vault.ts** (`DefaultAzureCredential`):
  - standalone: identity 4.13.3 / msal 6.0.1 -> 4.14.1 / **7.1.2**;
  - workspace root: identity 4.13.1 / msal 5.3.1 -> 4.14.1 / 7.1.2.
  - The production consumer and the managed-identity probe are in G115-F1.
- No other product file imports @azure/identity or msal-node. The two test files in `tests/connectors` hold the import only in comments.

## Q3. Suites and tsc (part d) (scripts/base_run.sh)
| | base | head |
|---|---|---|
| m365-integration vitest (root `npm ci` + shared build) | 280/280 (29 files) | 280/280 (29 files) |
| packages/shared vitest | 1152/1153 (wallet-signature, KS 1727) | 1152/1153 (same cell) |
| m365 tsc -p tsconfig.test.json | 0 | 0 |
| packages/shared tsc (scratch, including tests) | 24 | 24 (identical sorted set) |
| `npm ci --ignore-scripts` | root rc 0 | root rc 0 (1798 packages), packages/shared rc 0, m365 rc 0 |
- Instrument note: my first m365 run (a standalone install only) failed 17 files on `@secuura/shared` and pglite resolution (logs/head_test_m365*.log). That was a fault of my setup, not of the PR. I re-ran with the root install and a shared build.

## Q4. Baseline file (part e) (logs/baseline_check.log)
- The rows go from 10 to 9. The only row removed is GHSA-xcx6-jx8p-x3h5, and nothing was added.
- Row order is kept, and the other 9 rows are deep-equal. `$comment` is unchanged.
- The text diff is 7 deleted lines and 0 added. The zod row keeps `expires 2026-11-09`, and the three 11-30 rows and the others keep their dates.

## Q5. Mutants / red-first
Not applicable: the PR adds no tests and no product code. The control cells C1 and C2 stand in for them (each must go red, and does).

## Q6. merge-tree (part f) (logs/merge_tree.log, merge_tree_end.log)
- **onto 466a0d6c:** clean. 6 files, +197/-69, and every blob equals the PR head's blob.
- **onto bc8558db** (develop at END, re-fetched): clean, 6 files, +197/-69.
- **Shared paths since the base:** 37 paths changed between 8f313815 and bc8558db, and 0 of them are the PR's 6. 0 of the 37 contain "package"; for comparison, 17 are .ts files. No merged PR touched a lock or a manifest.

## Notes for the PR body
1. G115-F1: the managed-identity token path (production's) is measured equal at msal 6.0.1 and 7.1.2 against a stand-in. Recommended: add it, and narrow the UNMEASURED line to the EnvironmentCredential no-options path and the real Azure endpoint.
2. G115-F6: wording. "7 advisories / 44 locks"; shared 1151 at base was a flake.
3. G115-F4 and F5: follow-ups (stale uuid reason text; m365's unused identity dependency). Neither belongs to this PR.
No FIX-BEFORE-MERGE item.

## NOT TESTED
- Node 24 (host is v26.8.1).
- A real Azure tenant, Container Apps identity endpoint, IMDS or Key Vault. The `SecretClient.getSecret` round trip with a 7.1.2 credential.
- The EnvironmentCredential / no-options token path at msal 7 (the author's stand-in only; I did not re-run it).
- The m365 OAuth callback against Microsoft (its msal stays 3.8.10).
- An image build, a service boot, the pre-push hook legs, Schemathesis/Akto/Playwright.
- The PR body itself (not readable here; the mails were used instead).
- Docs fragments: the PR adds no tests or fragments, so the fragment check was not run.

Artefacts: scripts/ (lockdiff.py, msal_scan.mjs, control.sh, resolve.cjs, mi_probe.cjs, base_run.sh), logs/, evidence/. The clone at repo/ was left at head `750da509`, with only the untracked scratch tsconfig. Its push URL is disabled.
