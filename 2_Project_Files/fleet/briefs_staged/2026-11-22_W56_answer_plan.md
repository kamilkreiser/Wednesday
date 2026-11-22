Seat W 56th

ANSWER: plan confirmation. BUILD RELEASED AS PLANNED, with the rulings below. Your item 3 (a bypass-only unit deletes zero rights holders, silently, and the organisation delete then orphans them) is the finding of this round: thank you, and it is why Q4b is IN.

Q1 the 409: CONFIRMED as written. Lock the organisation row FOR UPDATE, count users, 409 with this file's CONFLICT shape (adminConfig.ts:305), zero deletes. The absent-organisation deviation (nothing deleted, today's 200 'Not found') is ACCEPTED: state it in the PR body as a behaviour change. The compose-built window (no users FK, a concurrent insert between count and delete) is a named residual in the PR, not built.

Q2 the unit: CONFIRMED as written. runWithPlatformScope(() => withPlatformScopeTransaction(tx => ...)), every statement on tx, set_config('app.tenant_id', orgId, true) before the rights_holders delete, db.ts unchanged. The 5000 ms timeout is a named residual in the PR.

Q3: (a) the 'dependent records' 409 wording: LISTED in the PR's residuals, not built (unruled wording). (b) the docker/init vs migrations FK drift: FILE IT. Search the board first (by symbol, path and the words 'docker/init' and 'foreign key'), state the search in the ticket; if nothing matches, file ONE ticket, Medium, facts only (your item 5 and its evidence path, 'read, not run', and that the 409 count in KS-2306 protects users on both kinds of database). No build, no migration. If a match exists, add your evidence to it instead. Name the ticket in your READY.

Q4: CONFIRMED, cells C1-C5, the ks2302 P1 rewrite and its mock, the ~12 mutants as listed.

Q4b: YES, outside the PR. A throwaway local Postgres container you start yourself (postgres:15, a name carrying w56), app role non-owner, policies 027 and 039, probes (i)-(iii). Evidence into your REC. When done, stop and remove ONLY the container you started, by that name, and say so in the READY with `docker ps -a` before and after. No volume, image or other container is touched. Nothing deployed is read or touched.

Paths: adminConfig.ts, ks2302's test file (P1 + mock only), the new test file, two fragments. TIER 1. Branch as named, from D 302361a30209.

Faults noted (the boot cd, the noisy grep): accepted. The ruling stamp: the store records ruled_ts 18:49:24 for card secuura-org-delete-with-users-ks2306-1120; quote that one.
