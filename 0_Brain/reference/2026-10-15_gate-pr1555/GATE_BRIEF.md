# Gate brief: PR #1555 (KS-1114, anonymous title lookup, one tenant), Opus TIER 1, FULL (new PR; public endpoint)

Commissioned by the Wednesday seat, 2026-10-15. Authority past the usage stop: Kam, terminal 2026-10-15 ~12:5x, "if anything needs to be pushed, merged or deployed, do that first as well". 0_Brain paths relative to /Volumes/DevMASTER/WEDNESDAY/; project paths under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

- Head c85cc28d0232e5641901bfd12ca6960a9711e783 (author's ls-remote; re-read refs/pull/1555/head yourself), base develop 53b429ed6b4bf4d23c0721bf573b9df1c858bc06. 7 files: services/originate verification.ts + originate.openapi.ts, regenerated docs/openapi/secuura-api.yaml, two new cell files + one fixture, the ks1103 test.
- KAM'S RULINGS, verbatim: card secuura-ks1114-title-lookup-needs-authentication-1013 = b "Title lookup open to anyone, one tenant" (his live-board message 2026-10-13 18:53:33); earlier 2026-09-13 he ruled to implement the title lookup. KS-1032 = a "Fail closed, deployed only after the secret is set" (a deploy condition, not this gate's).
- Author's claims (NOT evidence): no auth check on the title path (only when no documentId and no hash); tenant bound in SQL `d.tenant_id::text = callerTenantOf(req)`, no crossTenantLookup; existence-only reply (verified/hashValid/integrityVerified false); erasure sentinel refused twice; empty/whitespace title = absent (400); newest-first `created_at DESC NULLS LAST, id DESC`; sentinel not-found byte-identical to a missing title's; T9 non-title bodies byte-identical to develop (0-byte re-record, two controls); verify integration 47/47 in both MULTI_TENANCY_ENABLED modes; originate unit 108/1342; check:openapi PASS; mutation 13 at an older base (11 killed, 3 surviving by design: m1 under FORCE RLS, m6a/m6b the two sentinel lines). In-hook 88/88.

## Gate
1. Diff by hunk; classify behaviour vs spec vs test vs fixture. The yaml must equal what generate-openapi produces from the head (regenerate it yourself).
2. Does the code do exactly Kam's (b) and no more? Probe at a real Postgres of your own (free port via lsof; not 55418), through the route: anonymous title hit in the caller's tenant; a title that exists only in ANOTHER tenant (must be indistinguishable from absent); the erasure sentinel; empty/whitespace; a title with SQL/LIKE metacharacters (%, _, quotes); a very long title; documentId or hash present alongside a title (which wins); both tenancy modes. Report every reply body.
3. Information leaks beyond existence: timing difference between hit and miss (measure, many samples), error bodies, headers, any field that reveals more than existence.
4. Re-run the author's mutants at the head (especially m1, m6a, m6b, and say whether "survives by design" is honest), plus two of your own; comment-only control.
5. Caller tenant: how does callerTenantOf resolve for an ANONYMOUS caller in each tenancy mode, from source; can a header or query parameter choose the tenant?
6. Merge prediction on the live tip with overlap + a planted conflicting control. Cross-lane: do PRs #1552, #1554 or KS-1543 (R lane) touch docs/openapi/secuura-api.yaml or originate.openapi.ts? Measure from their heads (762d044b0, 3c15af569) and say whether merge order matters.

## Rules
Read-only on the project: your own clone under /private/tmp/claude-501/, fetch there. No git write verb in !CODING, no push, no GitHub/Linear writes, no Docker, no remote box. Never cd; delete nothing (no rm, rmdir, find -delete). **Every loop or multi-step command goes in a script FILE run as `/bin/bash /abs/path/script.sh args`, never inline `bash -c '...'`.** If a step truly needs a permission dialog, write evidence/BLOCKED.txt and skip it, naming it in NOT tested. Write only here and in your scratch dir.

## Output
0_Brain/reference/2026-10-15_gate-pr1555/verdict.md: VERDICT on line 1 naming the head, sha256/16 of the report on LINE 2 (delete line 2, sha256 the rest, first 16 hex), FOUND / TESTED / HOW, NOT tested, severities with file:line. Round 1 of 2. Merge only on Wednesday's head-bound GO; nothing deploys.
