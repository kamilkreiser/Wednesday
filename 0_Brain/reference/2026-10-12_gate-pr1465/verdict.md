# QA gate — Secuura Platform K PR #1465 (KS-1203 option A, tier 1)

**Head:** `765fda04e9e3a6849fc424f8b017a2ef4b84a9c5` (one commit on `f5a2402625a814313bc498eff6c0614cc0d321b6`)
**Gate:** independent Opus, read-only, 2026-10-12. Own clone: `--no-hardlinks` from the local repo, PR head + develop fetched from origin into the scratchpad clone (push URL disabled). No ref writes in the shared repo, no pushes, no comments, no board writes.

## Verdict: **GO WITH NOTE**

No Major defects. The change does what the brief says, nothing more, red on base and green on head by my own run, and it survives the merge onto the current develop tip.

## Where develop is
`ls-remote` at gate time: `refs/pull/1465/head = 765fda04…` (matches). The brief says develop is at `ba697cf3d421`, but develop has moved again: my fetch got **`db0df4540acf…` (KS-1205)**. I predicted both merges with `git merge-tree --write-tree`, and both are clean: ba697cf3d → tree `a3e76407…`, db0df4540 → tree `77df8c01…`. I ran the full suites on the db0df4540 merge, as commit `b8a8d4de…` in my clone.

## (1) Diff
There are 8 files, +316/−6, exactly as described: shared `package.json` (exports + typesVersions), `documents/defaultDocumentType.ts`, the shared test, the new gateway test, a one-line test rename in ks1176, `verification.ts`, `enforcement.ts`, and originate `documents.ts`. The diff touches nothing else and no lockfile.

## (2) Red/green and mutations (my run)
| | gateway ks1203+ks1176 | shared default-type |
|---|---|---|
| base code + head tests | **9 failed** (8 refusal cells + SOURCE) / 29 passed | **3 failed** / 1 passed (control) |
| head | 38/38 | 4/4 |
| merge onto db0df4540 | 38/38 | 4/4 |

The planted mutations were each applied on head and restored, and the tree was clean afterwards. The unmutated control was 38/38 and 4/4.
- M1 bare `'DOCUMENT'` at the gateway guard → SOURCE cell red (1).
- M2 bare at the workflow gate → SOURCE red (1).
- M3 bare at originate → SOURCE red (1).
- M4 old two lines restored (`requestedType &&` skip) → **exactly the 8 refusal cells red**.
- M5 constant set to `'DOC'` → the shared constant cell red, plus 18 gateway cells red.
- M6 typesVersions entry dropped → shared cell red, and the gateway and originate `tsc` fail with TS2307 (rc=2).
- M7 exports entry dropped → shared cell red, runtime `ERR_PACKAGE_PATH_NOT_EXPORTED`, and both gateway files fail to load.

## (3) Suites, tsc, lint, openapi
| | head | merged (db0df4540) |
|---|---|---|
| shared vitest | 949/949 (49 files) | 949/949 |
| api-gateway vitest | 896/896 (98 files) | 928/928 (101 files) |
| originate jest | 1099/1099 (97 suites) | 1103/1103 |
| tsc --noEmit shared / gateway / originate | 0 / 0 / 0 | 0 / 0 / 0 |
| eslint errors/warnings shared, gateway, originate | 1/35, 0/36, 0/23 | same |

- eslint on clean base gives the same counts (1/35, 0/36, 0/23). Control for the shared error: it is pre-existing, `packages/shared/src/middleware/index.ts:539` no-control-regex, in a file this PR does not touch.
- `npm run check:openapi` on the merge: "CHECK PASS: on-disk YAML matches generated", and 406 spec examples OK.

## (4) Semantics
- **The eight shapes** (untyped, documentType "", type "", DocumentType / document_type / Type, own `__proto__.type`, untyped data carrier) all resolve to DOCUMENT and get 403 for a list of `['SSD_DOCUMENT']`. In those cases enforcement and the workflow gate never run, and they are admitted (201) when the list contains DOCUMENT.
- **Checked type vs stored type.** The gateway forwards `rawBody`, so originate re-parses the same bytes and runs the same `documentType || type || DEFAULT` expression. I enumerated edge shapes: whitespace, case, number, array, object, null, 0, false, both empty, `""`+type, data-only. For every admitted shape, the stored type equals the checked type. Non-string types get 403 under a restricted list, and `null`/`0` documentType gets 400 at originate. No input stores a type other than the one checked.
- **403 body.** It is `FORBIDDEN … document type "DOCUMENT"`. It names only the resolved type, never the allow-list, and no audit or log line is added. The refusal path had no logging before this change either.
- **Lists that mean no restriction.** null, undefined or `[]` is still no restriction; a cell pins this. A non-array list still fails closed (KS-1204). JWT callers carry no `connectorMeta` (set only at `auth.ts:334`), so they are unaffected. A connector-less API key matches no integration entry, so it stays unrestricted.
- **Other readers.** The MCP server's register tool requires `documentType`. The behaviour change only reaches restricted connectors that relied on untyped creates. **Limit:** Platform S and other external callers are outside the repo, so I could not check whether any restricted connector sends untyped creates.

## (5) Shared export map
- `exports` and `typesVersions` both point at `dist/documents/defaultDocumentType.(js|d.ts)`. A clean `rm -rf dist && tsc` produces both.
- Runtime resolution from gateway and originate succeeds. The control is that a non-exported subpath fails with `ERR_PACKAGE_PATH_NOT_EXPORTED`.
- Both Dockerfiles build shared from `COPY packages/shared/` in a `shared-builder` stage (`npm run build`) and symlink it into `node_modules/@secuura/shared`, so the new file reaches dist. `.dockerignore` excludes only `packages/*/dist` and `node_modules`.
- I did not run a Docker build (limit).

## Defects
1. **Minor — `services/api-gateway/src/services/enforcement.ts:101`** still resolves an untyped body to `''`, so `enforceDocumentTypeRules` returns `docType: {}`.
   - The catalogue's DOCUMENT entry (seeded at `routes/admin.ts:316–336`, "the default when a creation request names no documentType") is therefore never enforced for an untyped create. That covers `isActive`, `creatorVerificationLevel`, `requireMFA`, `metadataSchema`, `requiresApproval`.
   - The constant at `enforcement.ts:264` sits in the gated branch, which an untyped body can never reach, so that site is dead for exactly the case KS-1203 targets. It is pinned only by the source-text cell.
   - The issue is pre-existing and outside the ruled option A scope. But the PR comment "the check and the stored type cannot drift apart again" is true for the allow-list only. **Recommend a follow-up ticket.**
2. **Minor — behavioural coverage of the originate site.** The originate site (`services/originate/src/routes/documents.ts:584`) and the workflow-gate site are pinned only by the regex SOURCE cell: mutations M1–M3 turn only that cell red. No cell asserts that originate stores DOCUMENT for the eight shapes. The value is identical, so there is no risk today, but nothing behavioural would catch a different default at originate.
3. **Note — `MCP Deployment/troubleshooting.md:119–123`** does not say that an untyped create is checked as DOCUMENT. Connector operators who hit the new 403 have no hint.

## Logs
Scratchpad `logs/{head,merged,base_red,base_clean,mut}/` (session 1a6144ee).
