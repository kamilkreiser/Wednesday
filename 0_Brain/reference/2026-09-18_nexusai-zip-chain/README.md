---
date: 2026-09-18
type: reference
source: Datasec/NexusAI S65, measured answer to Tuesday's commission (mail 2026-09-18T00:19:54Z -> reply 00:2xZ, DKIM spf/dkim/dmarc pass)
status: live
---

# The chain to the NexusAI marketplace ZIP — measured, not estimated

**Why this file exists:** Kam asked to be told when the zip is ready. It is not close, and the reason
is a dependency chain with one of his own steps in the middle. This is the measured state at 2026-09-18 10:23 AEST,
not a card and not a recollection.

## The two facts that decide everything

1. **The release registry `nexusaireleaseacr` is EMPTY.** `az acr repository list` returns `[]` as
   SP a71b85e7. **Positive control in the same action:** the same command against the dev registry
   returns `["nexusai","nexusai-inspect"]`, so the instrument can see repositories when they exist.
   This is a measured "no", not a "cannot see". *(Tuesday's own earlier anonymous `_catalog` probe
   returned 401 — and so did the control against a registry known to require auth, so that probe
   proved nothing and was not used.)*
2. **The package build still REFUSES** at package head `9eee3ff`: "BUILD FAILED: 8 of 18 checks
   failed. No upload file was written under its final name." So no zip can exist today under any
   arrangement.

## The chain, in dependency order

| # | Step | State measured today | Whose |
|---|---|---|---|
| 1 | RD-436+452+501+499 + RD-535 @ `0b910a2` | re-gate RUNNING; verify PASS 3363/183 | OURS |
| 2 | RD-486 + RD-523 @ `2d83967` | re-gate RUNNING; verify PASS 3275/179 | OURS |
| 3 | RD-464 round 3 | builder RUNNING; rebase owed after step 2 | OURS |
| 4 | RD-503 + 442 round 2 | built, verify QUEUED on the lock | OURS |
| 5 | RD-505 removal (package branch) | builder RUNNING on `9eee3ff` | OURS |
| 6 | RD-516 — anonymous SSRF via ai-test | **NOT STARTED**; blocker; starts after step 2 merges | OURS |
| 7 | RD-518 — KEYVAULT_NAME vs KEY_VAULT_NAME | built, unverified; serial after step 1 merges | OURS |
| 8 | RD-524 / 525 / 531 | not started, ticketed | OURS |
| 9 | The long tail (RD-495, 497, 510, 492, 519, 537, 471/472/475/487/457/438) | not started | OURS |
| 10 | Merge the checklist into main, in the ruled order | pending 1–9 | OURS |
| 11 | Release-gate preconditions: main merged into the package branch; the dev scripts stop passing the removed registry parameters; listing folds; RD-526..529 fixed | NOT DONE | OURS |
| 12 | **Push the release image to `nexusaireleaseacr`** | **cannot start until 10–11; registry empty** | **KAM'S** |
| 13 | Set the real digest in `mainTemplate.json:116` + `release-policy.json:4` | pending 12 | OURS |
| 14 | Run the package build for real + the release gate | pending 13 | **THE ZIP EXISTS HERE** |
| 15 | Upload and submit in Partner Center | pending 14 | **KAM'S** |
| 16 | Preview / test deploy after approval | pending 15 | **KAM'S** |

## The longest pole

**The digest — and it is behind RD-516.** Nothing produces a zip until Kam pushes an image; he cannot
push until the checklist merges; RD-516 is a blocker that has not started and waits on RD-486's merge.
So: RD-516 plus the merge chain behind it, then one round trip through Kam.

## The minimum set — what MUST be in the zip for a customer to deploy and use it

Each is deploy- or use-blocking, with its reason:

- **The package itself + the RD-505 removal** — otherwise a customer needs a token we will not give,
  or picks an option that cannot deploy.
- **The real digest** — the package cannot be built without it.
- **RD-436/452/501/499 + RD-535** — a restore reopens a *configured* deployment to anonymous takeover.
  Measured on the LIVE 2.1.1 code too.
- **RD-486 + RD-523** — the stored Azure OpenAI key can be sent to a caller-named host, and to a
  redirect target.
- **RD-516** — anonymous SSRF through ai-test. Same class as RD-486; shipping one without the other
  leaves the hole half-closed.
- **RD-518** — the template sets `KEYVAULT_NAME` while the app reads `KEY_VAULT_NAME`, so Key Vault
  silently does nothing in **every** Marketplace deployment. This is "in the store and not usable" in
  its plainest form.
- **RD-503 + 442** — SUPPORT.md's only fix for AI settings does nothing on a real deployment, so the
  customer-visible repair instructions are wrong.
- **The listing folds** (RD-465 O-4, RD-454 O-4) — the listing text contradicts the product's
  behaviour without them.

**Merely open** — real, ticketed, NOT load-bearing for a deployable submission: RD-524, 525, 531, 537
(privacy/alarm completeness — Kam's Monday review covers the claims), RD-495, RD-497 (admin routes
refuse admins: annoying, not deploy-blocking), RD-510, 492, 519, 471/472/475/487/457/438, lock v3,
the HISTORY entries.

**Between the two:** RD-464 round 3 (a hang and a false "ready" on the AI health check). Kam approved
the round and it is already built, so S65 keeps it in — **and it is the first candidate to drop if the
chain must be shortened, never RD-516 or RD-518.**

## A finding, recorded so nobody diagnoses the wrong thing

The build's refusal is **right in effect and misleading in its reason.** The template's own comment
says it fails while the digest placeholder is in place, but the checker never names the placeholder:
its image checks still resolve through `parameters('containerImage')`, while C-58 made
`containerImage` a **variable**. A reader would chase the wrong cause.
