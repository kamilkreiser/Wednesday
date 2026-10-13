# Gate brief: Secuura Platform K pull request 1547 (ticket KS-1594, originate POST /api/admin/api-keys, the fifth piece of the KS-1570 round), OPUS tier 1 (an authorisation boundary: who may mint a provisioning-capable key, and for which organisation)

Commissioned by the Wednesday seat. 0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/; project paths under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

## Kam's rulings this sits under (verbatim, from his live board 2026-10-13, AEDT)
- 11:47 card secuura-ks1570-admin-role-bound-shape-1013 = b: "Give each ADMIN an explicit organisation scope"
- 12:55 card secuura-provisioning-scope-escapes-the-org-bound = b: "Allow it, but bound the provisioning key to the minting admin's own scope"
- 09:53 card secuura-ks1533-admin-role-unbounded-by-org-arm-1013 = a: "Leave ADMIN unbounded for now" | note: "keep a note that this needs to be changed before deployment"
- Wednesday's ruling to the author (not Kam's): item (c), bounding an ORG_ADMIN's body organizationId to its own organisation, PRE-RULED YES subject to a caller survey. Wednesday's reading of the ORG_ADMIN bound ruling, not his word. The author's survey found no in-repo caller that sends organizationId.

## What you are gating
- Head a897f57eba3d39afd8fd19e2895cb0e83188ab58 (Wednesday's own ls-remote of refs/pull/1547/head = the author's), ONE commit on develop 026c2d1614065c79fc8d96007ac0d80f19fb9363 (Wednesday's ls-remote, unmoved at commission). Two files: services/originate/src/routes/adminConfig.ts (+49/-5) and a new 16-cell integration file ks1594-admin-mint-provisioning-and-org-bound.integration.test.ts.
- Author's description (NOT evidence): (a) isProvisioningCapable(requested) && !isPlatformRole(caller) -> 403 before key generation; (b) normaliseOrgId on the body value and the claim before any compare or write; (c) a non-platform caller naming a different organisation -> 403. Shared predicates from packages/shared/src/index.ts :229, :239, :243 (dist said to be current, not rebuilt). Cells red-first in both tenancy modes (11 failed / 3 passed pre-fix, 16/16 post-fix); mutants 6/6 (T5 "(c) disabled" reds c6 only). c3 survives T1/T2 by design (both rules refuse it). Author's deliberate choice to judge: an ORG_ADMIN sending a blank organizationId gets a key BOUNDED to its own organisation (c9b), while a platform caller sending '   ' stores NULL (c9). c12 asserts svc_api_keys.organization_id is_nullable from information_schema (migration 018's ALTER sits in an EXCEPTION WHEN others block).
- Author's caller survey (NOT evidence): five in-repo minting callers, none sends organizationId; the admin frontend calls /api/security/keys, not this route; the route is in no OpenAPI spec.
- Author's NOT RUN: Schemathesis, Akto, Playwright, k6 and preflight legs 3/4/8. The Docker daemon is down. Wednesday ruled this round does not start Docker, and the Test Evidence NOT-run line stands. Do not start Docker either.

## How to get the code (READ-ONLY on the project)
git clone --shared of 2_Project_Files into YOUR scratchpad, push URLs disabled; fetch refs/pull/1547/head and develop with the project's core.sshCommand; assert the shas. No git write verb in the project folder; no push; no GitHub or Linear write; no remote box; no Docker. Never write inside !CODING. Postgres: use your OWN port; do not touch 55413, 55414, 55418, 55419, 55436 or the ports the other two running gates (1545, 1546) chose. The originate worktree may need `npm run generate` for the Prisma client (KS-1305): a red that is a 500 from a missing client proves nothing.
TOOLING RULE: never run a command that deletes files, never put rm inside bash -c or sh -c; never cd; absolute paths only.

## What to attack
1. Re-run the 16 cells on the head AND on develop, both tenancy modes, with a control each harness can fail; the originate unit suite and tsc.
2. Re-derive the caller survey yourself (whole repo, every spelling of the route, controls both ways), and say whether anything outside the repo is plausibly affected.
3. THE BOUNDARY: every role the route admits (requireRole at :38) x provisioning-capable vs not x organizationId absent / own / own-mixed-case / own-with-whitespace / foreign / blank / NBSP / null / a non-string (number, array, object) x tenancy mode. Look for a FALSE PASS (a non-platform caller minting a provisioning-capable key, or a key bound to a foreign organisation) and a FALSE REFUSAL (a legitimate same-organisation mint refused). Read isProvisioningCapable, isPlatformRole and normaliseOrgId at the head yourself: does hasScope treat wildcards ('*', 'organizations:*', case variants, whitespace in a scope string) the way the cells assume?
4. Does any OTHER route in originate or the security service mint into svc_api_keys without these checks (a sibling door)? Enumerate writers of svc_api_keys; report, do not fix.
5. Judge the c9b choice against Kam's rulings above, and say whether ADMIN (unbounded by his 09:53 ruling) is handled consistently with that note.
6. Mutants: re-derive the author's six, add at least FIVE of your own (e.g. hasScope replaced with an exact match; the platform check on the wrong principal field; normaliseOrgId on one side only of (c); the 403 moved after the INSERT; (c) applied only when MULTI_TENANCY_ENABLED is true). Report by cell name; include a comment-only control.
7. Scope: diff --stat vs develop is exactly the two files; PR body vs code; "Refs KS-1594" with no closing keyword; the Linear attachment's linkKind (read only, if you can; report it, do not change it).
8. Say plainly what you could not test and whether it could hide a Major.

## Output
0_Brain/reference/2026-10-13_gate-pr1547/verdict.md (this folder only, plus your scratchpad; raw outputs under evidence/, never a directory named out). Head under test; every number with its instrument and a control; FOUND / TESTED / HOW; NOT tested; severities with file:line, reproducing shape and minimal fix. VERDICT (GO / GO WITH NOTE / NO GO) and sha256/16 of the report on LINE 2 (delete that one line, sha256 the rest, first 16 hex). This change deploys only in the KS-1570 deploy round (0_Brain/tasks/DEPLOY-BLOCKERS.md), never on its own. Merge only on Wednesday's head-bound GO.
