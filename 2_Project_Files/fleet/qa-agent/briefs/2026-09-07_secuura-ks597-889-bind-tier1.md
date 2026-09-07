# QA GATE — Secuura #889 @ `42d8cf5f5`, TIER 1. **A refusal added to a live path on KAM'S OWN RULING.**

**Charter first, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`
**Your own #889 round-1 Finding 1 is what this implements** — you found the issuing organisation was
caller-asserted and never bound to the actor. **Kam ruled `bind` at 19:00.**

## 1. Target
- **#889**, head **`42d8cf5f53a011dee3b98c7d8e9569c7dbc27888`** (was `9898ae724`), base develop
  **`6c60cc09b50366caf29a25837e6fea5556e451bb`**. **Builder's `ls-remote`, not Wednesday's** —
  re-derive both, start and end. **PR files API for the change set**, never a two-dot diff.
- **TIER 1:** a **403 added to a live registration path**, on a security surface. **Non-prod, no
  deploy, do not contact the demo box.** ⚠ **`localhost:6882`'s DATA is untrusted** — build your own.

## 2. 🔴 WEDNESDAY GOT THE PRECEDENT'S ADDRESS WRONG — do not inherit it
Wednesday's card and brief cited **`documents.ts:559`** as the existing 403 precedent. **It is not:
that line is a field in a 200 body, the nearest status there is a 409 at `:565`, and `documents.ts`
is not even touched by #889's original diff.** Wednesday copied that from your own round-1 verdict
**without opening the file.** **The builder caught it before writing code.** The real precedent is
**`services/provenance.ts:131-137`, inside `resolveOnBehalfOf`** — which is literally what Kam's
words describe. **Verify against provenance.ts, not against Wednesday's citation.**

## 3. WHAT TO ATTACK — the three carried semantics, and the one that went beyond the wording
The bind lives at **`documents.ts:450`**, after the existing UUID validation, using the **shared
`normaliseOrgId`** (`services/orgId.ts:36`) on **both** sides. **Peter Obeden's #795 review is quoted
inside that function saying two byte-identical private copies caused the drift** — confirm no third
copy was introduced.
1. **403 only when both are present and differ.** A caller with no `organizationId` is not in a
   *different* org (`provenance.ts:109`). **Test: caller-with-org vs body-org, matching and
   differing; caller without org; body without org.**
2. **Case-only difference is NOT a mismatch** — the F-4 class. **A raw compare would 403 a caller
   acting inside its own Organisation. Try case, whitespace and any normalisation `normaliseOrgId`
   claims to do.**
3. **No claim → unchanged.** This adds a refusal; **it must NOT have made the field required.**
4. **🔴 THE ONE THE BUILDER FLAGGED AS BEYOND THE LITERAL RULING — judge it explicitly.** An org-less
   caller gets **no 403 AND no attribution** (the column folds to NULL). Its reason: migration 018
   drops NOT NULL on `svc_api_keys.organization_id` for admin-issued keys, and the gateway maps a
   missing connector org to `''` (`api-gateway/middleware/auth.ts:232`), which `normaliseOrgId`
   collapses to null — **so without this, an org-less key could still attribute to any org in its
   tenant.** **It disclosed this rather than burying it. Confirm the reachability claim and say
   whether the behaviour is right.**

## 4. THE COMMENT THAT HAD TO CHANGE WITH THE CODE
`documentRepo.ts:309-330` previously argued *"a registration NEVER fails because of this field. It is
attribution, not authorisation."* **Kam's ruling reverses exactly that**, and the builder rewrote the
block in the same commit. **Check the file no longer asserts a property the code does not have** —
this project has shipped two wrong comments today and this is the discipline that answers it.

## 5. AND THE THING IT FOUND ON THE WAY
**The two provisioning paths disagree about the foreign key:** `docker/init/01-schema.sql:125`
declares `issuer_organization_id UUID` with **no** reference; `migrations/001:105` declares
`REFERENCES organizations(id)`. **Judge whether that matters for this change** — and note your round-1
pass measured **zero** constraints on that column in a built database.

## 6. Bounds and report
Findings-only, **never fix**. **NO CI** (20/20 `startup_failure`) — you are the only independent
instrument. **Say what each cell MOCKS.** **Search the board before filing and say what you searched.**
**A GO is NOT a deploy GO.** **GO / GO-with-findings / NO GO on the first line**, the org-less branch
its **own heading**, NOT-TESTED at equal prominence. Mail `wednesday-agent@agentmail.to`, subject
`[QA -> Wednesday] Secuura #889 bind round 1 (tier 1)`.
