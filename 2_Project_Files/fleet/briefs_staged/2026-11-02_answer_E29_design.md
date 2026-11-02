Seat E 29th

ANSWER: plan confirmation = DESIGN APPROVED. BUILD (ITEM 3), one PR on develop 0e3a9b65cdd6 or later.

Q1 = YES. The mechanism as proposed: a new add-only export `withPlatformScopeTransaction(fn)` in originate src/db.ts (refuses before any statement unless isPlatformScope(); multi-tenant = one checked-out client, BEGIN, applyTenantGuc, fn(createPoolProxy(client)), COMMIT, ROLLBACK + rethrow on throw, release in finally, mirroring withTenant's pool branch; single-tenant = getPrismaClient().$transaction with the bypass set_config as the unit's first statement), and enforceRetentionImpl's per-policy unit on `tx` with byte-identical statement text, values and order, `logs.push` AFTER the unit resolves. Your PARTITION gains `Blockchain/Dev/services/originate/src/db.ts`, ADD-ONLY: wrapPrismaWithTenantGuc, createPoolProxy, withTenant and the `prisma` object stay byte-identical (a cell or a blob compare proves it).
Q2 = keep Prisma's default 5000 ms. Today's DELETE already runs inside the proxy's per-statement $transaction under the same default, so a slow unit rolls back no worse than today's DELETE alone fails. STATE IN THE BODY: a unit that times out deletes NOTHING for that policy (fail closed), and a policy whose DELETE regularly exceeds 5 s would then never progress; whether any live table is that large is UNMEASURED (no box read). Name it as a follow-up candidate, file nothing.
Q3 = KS-1944 OUT of this PR (the spec edit and the open contract are a separate decision). KS-1944 stays open; one line on it naming your PR as related is fine.
Q4 = evidence-only real-PG harness, as proposed (failure-injection triggers do not belong in a committed test that could run against a teammate's DB). Keep the probe and its outputs in your record folder and cite them in the body; the gate will re-run them.

ALSO:
- Your correction is accepted and goes in the body: gate 117's G117-F2 said "three autocommit statements, no transaction"; the real mechanism is three separate transactions (the proxy's per-statement $transaction / queryWithTenantGuc). Same defect.
- The B6 vacuous first run you caught and fixed: keep both runs in evidence, as you have.
- Mutants: your seven, plus one: the helper granting the bypass when called OUTSIDE the platform scope (the refusal removed AND the set_config kept) must be caught by H1.
- Commit subject and PR title start with "Refs KS-1943: " (house form); TIER 1, Opus gate at READY.
- Your container s-e29-pg: keep it for the build, remove it at wrap with a `docker ps -a` reading in the same action.

Wednesday
