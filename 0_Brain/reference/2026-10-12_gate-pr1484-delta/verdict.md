# DELTA GATE PR #1484 (KS-695 ask 3 part i): verdict GO WITH NOTE

Head `c9b384943148534d0a4743ffac93554b2fe89f85`. Bundles checked: full sha256/16 2f70d1c231aee945 and delta e55edf784557410f both match. The delta bundle needs 59158be2 and its parent is 59158be205a6, so the head is exactly one commit on top of the previous gate's head.
For the predicted merge I used develop tip `aa9ca9de9ebcfdcc9040bfc3881fda9983dd3050` (origin/develop in worktree s-f17-ks1405, 2026-10-12 20:04 +1100, 13 commits past base 524db0ce6). The merge is clean (yaml and gateway index.ts auto-merged). Merged sha in my scratch clone: 28cea003.

## The delta is exactly the claimed fix (4 files, +17/-7)
- originate.openapi.ts:3673 now reads "The API key id" where it said `svc_api_keys`. The yaml line 12720 was regenerated to match.
- proxy.ts:849-856 comment rewritten. It now admits the unauthenticated `/originate/` passthrough, says the same holds for `/api/gdpr/erasures`, says nginx answers 404, and says originate re-checks.
- One new cell at ks695-ask3-erase-connector-refusals.test.ts:152-157 (mixed-case key organisation leads to 501 and nothing written).
- No product code changed.

## Major class re-verified: fixed
- packages/shared IN FULL: 49 files, 949/949 on both head and merged.
- Running the ks764 guard alone: 15/15. Control: putting the old word back turns it RED (1 failed / 14), and the file was restored byte-identical by sha.
- No file in the delta mentions both `svc_api_keys` and `is_active` outside the test.

## Previous minors
- Minor 2 (comment): fixed and true. My probes confirm the passthrough still exists (see below).
- Minor 4 (test gap): fixed. Control 27/27. Mutant M11 (drop normaliseOrgId on key.organization_id, connectorOrganisationErasure.ts:109) gives 1 failed / 26, and that failure is the new cell. File restored by sha.
- Minor 3 (403 vs 200 envelope): no code change, by design. I could not check the PR text because there is no gh, GitHub, or network access. So "stated in the PR" is UNVERIFIED by me. The question of whether S treats 403 as final remains open.

## Notes (not defects)
1. proxy.ts:851 says the passthrough is "about line 1219"; it is actually at proxy.ts:1222. The comment hedges with "about", so this is cosmetic.
2. The previous gate's notes still stand: 501 is a 5xx, so S retries; do not deploy before part (ii) and Q1. The `/originate/` passthrough also needs a ticket before KS-843 enforcement.

## Suites (my runs, head | merged)
| Check | Head | Merged |
|---|---|---|
| originate jest | 1134/1134 (98) | 1148/1148 (99) |
| gateway vitest | 973/973 (105) | 1032/1032 (109) |
| shared vitest | 949/949 | 949/949 |
| tsc (originate, gateway, shared) | 0 | 0 |
| eslint originate | 0 errors | 0 errors |
| eslint gateway | 0 errors | 0 errors |
| check:openapi | exit 0 | exit 0 |

## Battery re-run against the new head
- Door: the previous gate's 16-spelling probe, plus the positive control and the grace check, run on head and on merged. Output is IDENTICAL to the prior run's door_probe_head.txt, line for line, and the 6 door cells are green.
  - Absolute-form and `#frag` give 403 and nothing upstream.
  - `;x=1`, `%2D`, `%2F`, `./`, `x/../` and `%00` give 404.
  - `..` and `%2e%2e` give 400.
  - The `/originate/...` passthrough still gives 200 and reaches upstream. This is the known, now-documented case.
- Writes nothing: the only db access in connectorOrganisationErasure.ts and platformOrganizations.ts is one `$queryRaw` SELECT from svc_api_keys (line 101) plus the pre-existing read getOrganizationExternalRef. There are no execute/create/update/delete calls. The new cell asserts wroteNothing() and is green.
- Auth rule: the delta does not touch product code, so the previous gate's attack results still hold. The PR's 27 cells are green on head.

Caveat: node_modules were symlinked from worktree s-f17-ks1317, except @secuura, which points at each tree's own packages (shared was built per tree).
Evidence in this folder: suites_*.txt, ks764_guard_and_control.txt, m11_mutant.txt, door_probe_head.txt, delta_stat.txt.
