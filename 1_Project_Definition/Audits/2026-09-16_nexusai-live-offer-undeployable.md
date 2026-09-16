---
date: 2026-09-16
type: audit
subject: Is the LIVE NexusAI marketplace offer deployable by a third party?
answer: CORRECTED 2026-09-16 22:3x — NOT unaided; it deploys with a Datasec-supplied pull token
---

# The live offer cannot be deployed UNAIDED

> ## ⚠ CORRECTION, 2026-09-16 22:3x — this file's original conclusion was WRONG
>
> It said no third party can deploy the live offer. **The accurate statement: no third party can
> deploy it UNAIDED.** The submitted wizard has two REQUIRED fields this audit never read —
> `acrUsername` (TextBox, required, no default, *"Datasec-supplied scope-map token name with pull
> access"*) and `acrPassword` (PasswordBox, required, no default) — which mainTemplate passes to the
> Container App as registry credentials. The registry is private **by design**, with an enabled
> pull-only customer token (`nexusai-customer`) scoped to that one repository; a customer-path pull
> with it returns **HTTP 200** on the 2.1.0 manifest. Caught by the NexusAI agent, verified here by
> enumerating every field in the submitted `createUiDefinition.json`.
>
> **The error was method, not data:** two registry default lines were measured carefully and a
> conclusion drawn about the whole wizard, when the fields that decided it sat four lines below.
> Everything else below is accurate; read the conclusion as "not self-service" rather than "broken".
>
> **What survives:** the offer is publicly listed and **not self-service**. A customer who finds it,
> clicks deploy and has no token cannot proceed, and nothing in the listing or the wizard says where
> to get one. That is a commercial defect, and a smaller and far more fixable one.

**Original answer, as written and now qualified above: no.** Every link in the chain was read directly. Nothing below is inferred.

## The chain, each link measured

1. **The offer is LIVE.** Partner Center → Marketplace offers → *Reporting Dashboard Azure App*
   (`reporting_dashboard-app`, offer id `c8c0cb53-f392-4340-9fd8-204ca38cb25f`), status **Live**,
   last modified Sep 15 2026. Its overview reads *"Live and Preview versions are the same"*, with
   Automated validation, Preview creation, Publisher signoff, **Certification (Sep 15, 11:45:28 UTC)**
   and **Publish (Sep 15, 11:51:30 UTC)** all Completed.
2. **The live plan** is *Reporting Dashboard for HP MFD Productivity Suite*, plan id
   `reporting-dashboard-hpam`, **Solution template**, **Public**, **Live**. (The other plan,
   *Standard Plan* / `standard`, a Managed application, is **"Not available in marketplaces"**.)
3. **The live plan's package file is `NexusAI_plan-managed-ai_2.1.1_6fb497d.zip`** — read from the
   plan's Technical configuration page.
4. **That package, on disk at**
   `!CODING/Datasec/NexusAI/marketplace-submission-2026-09-15-r2/NexusAI_plan-managed-ai_2.1.1_6fb497d.zip`
   (15,321 B, sha256 `f17a0c3d461ff3c4e9283fbecb626a5a39a271efdc74045042d128123033dd93`), sets in
   `createUiDefinition.json`:
   - line 59 `"defaultValue": "nexusaidevacrfa39.azurecr.io/nexusai:2.1.0"`
   - line 71 `"defaultValue": "nexusaidevacrfa39.azurecr.io"`
   with the tooltip *"leave the default unless Datasec has given you a different tag."*
5. **That registry refuses anonymous clients.** An `oauth2/token` request scoped
   `repository:nexusai:pull`, sent with no credentials exactly as a customer's container client would,
   returns `UNAUTHORIZED — authentication required`. **Positive control:** the identical method against
   `mcr.microsoft.com` returns HTTP 200, so the refusal belongs to the registry and not to the method.

**Therefore a customer deploying the live offer fails at image pull.** Not an old build — no build.
There is no self-service route around it: the field is editable, but the customer has neither access
to the registry nor a copy of the image.

## Three other things seen while confirming it

- **A real deadline: Partner Center warns that previously published packages will no longer be
  accessible after 24 September 2026.** Anything needed from earlier versions must be downloaded
  before then.
- **A 2.1.1 package ships a 2.1.0 image tag.** Deliberate or a build slip; the project will know.
  Nothing currently asserts that a package's version matches the image it points at.
- The live plan is a **Solution template** while its package is named `plan-managed-ai`. Cosmetic,
  but it invites exactly the confusion it caused here — the file name suggests the other plan type.

## The finding underneath all of it

The 2026-09-15 build manifest **recorded** `wizard default containerImage =
nexusaidevacrfa39.azurecr.io/nexusai:2.1.0` at build time. The defect that makes the offer
undeployable was written into our own evidence, and the package shipped anyway, through certification.
**A fact written into evidence that nothing asserts on is not a check.** That gate is the one worth
building before any resubmission.
