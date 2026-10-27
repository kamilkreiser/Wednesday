DRAFT, for Kam to post (or not) under his own account on PR #1756. Reviewed at head 5d42cbd45 against develop 8894c7486.

---

Thanks Peter, this is a careful piece of work. **I'm approving with notes.** The fix is right, and I'd like it in the next deploy rather than later, for the reason in point 1.

**1. The secret is not unset everywhere. Kintsugi and demo have both had `GATEWAY_VOUCH_SECRET` set (same value on api-gateway and originate) since 19–20 Oct, when we closed KS-1032, and originate boots `ACTIVE` on both.** That means the R2-1 defect this PR fixes is live on both boxes today. A `POST /api/documents` through the gateway, from anyone acting in a non-default tenant, is saved under `DEFAULT_TENANT_ID` and then 404s for its owner. Signatories and third-party-verifiers reads also fall back to the default tenant for those callers. That's my fault for not recording the arming on KS-1083. Could you:
- correct the two sentences in the description ("hidden only because the secret is unset everywhere" / "nothing here touches deployed environments"); the diff doesn't touch deployments, but deploying it will change behaviour on both boxes, for the better;
- leave the data side with me: I'll check whether any documents were actually mis-filed since 19 Oct and decide on a repair separately.

**2. "Every" is a little too strong in three places.** `ENVIRONMENT-VARIABLES.md:138`, `originateForward.ts:20` and the `gatewayProvenance.ts:91` comment say every gateway → originate call now carries the vouch. Four hand-built calls still don't: `batch.ts` (certifications, verify), `platform.ts` (refresh-tenants) and `checkDocumentExists` in `verification.ts`. None of them sends trust headers, so leaving them unvouched is correct. Could the wording say "the five forwards that carry trust headers", so nobody assumes a future one is covered? Separately, and not for this PR: batch certifications forwards no `x-tenant-id` at all, so it files under the default tenant either way (KS-1084 family). Worth a ticket if one doesn't exist.

**3. Workflow-approve has no tenant to keep.** That forward sends `x-user-id` and now the vouch, but no `x-tenant-id`, so once KS-1087 gives it a Bearer it will still save under the default tenant. Fine to leave here; a line on KS-1087 would stop it getting lost.

**4. Optional, small:** two of the five forwards (upload and workflow-approve) aren't exercised by the unit test. A static check that each hand-built originate request sits beside a `vouchHeaderFor('originate')` call would stop a quiet regression. Also, `.env` comes out of `bootstrap-env.sh` as mode 644. That isn't new, but a `chmod 600` would suit a file that now holds this secret.

What I checked:
- The new gateway test is 3 red on develop and green on the head, and the bootstrap test is 4 red and 7/7 green. Both match your numbers.
- The full api-gateway unit suite passes on a local merge with today's develop (1255/1255), and `tsc` is clean.
- `merge-tree` is clean. Today's `verification.ts` change (#1767) is in a separate hunk.
- The vouch goes to originate only, is stripped at the edge, and is compared in constant time on originate's side.
- The `/health/ready` correction is accurate.

I haven't run the new live cell; I read it and it tests the right thing.
