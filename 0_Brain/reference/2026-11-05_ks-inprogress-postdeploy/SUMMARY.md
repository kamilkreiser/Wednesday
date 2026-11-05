# KS In Progress post-deploy census, 2026-11-05 (read-only)

## BLUF
Linear returned **205** KS tickets in "In Progress" (9 pages of 25, hasNextPage false on page 9; exact, not a cap). 13 live-seat keys excluded as instructed (all 13 were in the set), leaving **192** classified. Both boxes are at develop 07a2d62be6a0. **6 close candidates** (DEPLOYED-NOW-CLOSE-CANDIDATE), 8 LIVE-CHECK-OWED, 1 NOT-DEPLOYED: 15 rows in candidates.tsv.

| Class (primary) | n |
|---|---|
| SCOPE-REMAINS | 91 |
| HUMAN-OWNED (assignee or creator is Peter or Stuart; never candidates) | 31 |
| KAM-DECISION | 17 |
| OPEN-PR | 13 |
| FINDING-FILED | 12 |
| LIVE-CHECK-OWED | 8 |
| NO-COMMENT | 8 |
| DEPLOYED-NOW-CLOSE-CANDIDATE | 6 |
| NEEDS-DISPOSABLE-STACK | 3 |
| NOT-DEPLOYED | 1 |
| OBS-PARTIAL | 1 |
| CANNOT-RUN-SAFELY | 1 |
| Total | 192 |

HUMAN-OWNED takes precedence over every other class. Underlying class of those 31 is kept in column `underlying_class` (9 SCOPE-REMAINS, 6 NEEDS-DISPOSABLE-STACK, 5 FINDING-FILED, 5 KAM-DECISION, 2 LIVE-CHECK-OWED, 2 already HUMAN-OWNED, 1 NO-COMMENT). Peter is creator of 25 of the 205 and Stuart creator of 5 plus assignee of 1; the 11-04 census counted only 3 because it checked assignee only.

Candidates (all PRs merged, all ancestors of 07a2d62be6a0, newest comment's only remaining step is a read-only box check):
KS-1335 (demo read of svc_teams_webhooks.last_attempted_at), KS-1860 (demo read of MULTI_TENANCY_ENABLED and tenant counts), KS-1230 (demo stored-settings read), KS-1584 (provisioning-key row organization_id NULL on kintsugi and demo-pk), KS-1612 (migration 050/051 census per box), KS-1031 (048 applied / processed_by text per DB). Closing evidence is the read output pasted on the ticket, not the deploy alone. The last three (KS-1584, KS-1612, KS-1031) say "on each box"; kintsugi and demo-pk reads must both be shown.

Not candidates despite being deployed: KS-1378 (needs real-mail send, deploy hold on KS-1379), KS-1375 (partial, carried by KS-1383), KS-1205 (F-5 not in PR), KS-1187 (needs a POST), KS-1731 (0 rows in vc_credentials_store, reclassified CANNOT-RUN-SAFELY), KS-844 (NOT-DEPLOYED: no demo-service container on kintsugi; demo not checked).

## FOUND / TESTED / HOW
- HOW: GraphQL (read only) `issues(filter team KS, state name "In Progress")`, first:25, `comments(first:50)` per issue sorted client-side by createdAt, further comment pages followed (max 84 comments on one ticket). Key read inside the python process from the Blockchain `.env` (variable LINEAR_API_KEY); never in argv or output. PR numbers from attachment URLs (`/pull/N`). Ancestry: `git log 07a2d62be6a0 --grep '(#N)' -F` for a squash subject ending (#N), then fall back to the squash SHA the ticket's own comments name ("PR N merged as <sha>"), verified with `cat-file -e` and `merge-base --is-ancestor <sha> 07a2d62be6a0`. Source of each resolution is in `pr_resolution` (`PR:state:sha:git-subject|comment-claimed-sha`).
- FOUND: 205 now vs 238 on 11-04: 38 left the state, 5 entered (KS-1958, 1959, 1986, 1990 all excluded seat keys, plus KS-1981, no comment, PR 1997). Assignees among the 192: 160 board account, 31 unassigned, 1 Stuart. PR ancestry: 135 tickets have every attached PR resolved as an ancestor, 54 have at least one unresolved PR, 3 have no PR. 261 PR links resolved (196 by subject, 65 by comment-claimed SHA), 68 unresolved, 0 resolved-but-not-ancestor.
- Class method: 182 of 192 had an unchanged newest-comment date since 11-04, so their 11-04 class was carried; 9 changed plus KS-1981 were re-read by hand (KS-1600, 1499, 1460, 1407, 1343, 1262, 1539, 1087, 844). All LIVE-CHECK-OWED / NOT-DEPLOYED / OPEN-PR / OBS-PARTIAL / NEEDS-DISPOSABLE-STACK rows whose PRs are all ancestors were re-read by hand against the newest comment, plus every "Left open" line of the other all-ancestor tickets. Hand overrides (15): KS-1568, 1460, 1600, 1407, 1343, 1262, 1462, 1539, 1087 to SCOPE-REMAINS; KS-1622 to OPEN-PR; KS-1499 to KAM-DECISION; KS-1152 to FINDING-FILED; KS-1731 to CANNOT-RUN-SAFELY; KS-1198 to NEEDS-DISPOSABLE-STACK; KS-1981 NO-COMMENT. Six candidates promoted from OBS-PARTIAL/LIVE-CHECK-OWED/SCOPE-REMAINS.
- Control, positive (re-read raw JSON, one per class): KS-1335 (candidate): newest comment 2026-11-04, 150-char quote byte-equal to the tsv; KS-1378 (LIVE-CHECK-OWED): 2026-11-02, quote equal; KS-844 (NOT-DEPLOYED): 2026-11-04, quote equal. No hasNextPage on any of the three.
- Control, git: `merge-base --is-ancestor 07a2d62be6a0~5 07a2d62be6a0` rc 0; reverse direction rc 1; PR 1328 squash 0d156d12cc0f rc 0. HEAD of the checkout read 07a2d62be6a09c9cd504864d1cf1906543d55317.

## UNMEASURED
- Merge state of the 68 unresolved PR links is unknown: GitHub is not available (`gh` not logged in) and many squash subjects carry no (#N). Some are merged (my comment-SHA regex missed phrasings such as "merged as #1628 (develop `390cc0a317c9`)": that one is an ancestor, found by hand) and some are open or closed. Tickets with an unresolved PR can never be candidates here; that errs conservative.
- The "claimed SHA" resolutions trust the comment's PR-to-SHA pairing; only ancestry of that SHA is measured. I did not check the squash actually belongs to that PR.
- "Both boxes" at 07a2d62be6a0 is taken from the brief; I did not contact the boxes. Whether a container (e.g. demo-service on demo) is actually running was not checked. Develop tip 5fc5569ed96a is not in the local checkout (no fetch), so PR 2006 and anything after 07a2d62 is invisible.
- Classes remain keyword-plus-hand inference, not a full human read of 192 comments; expect misfiles near the SCOPE-REMAINS/LIVE-CHECK-OWED edge (about 10%). The 6 candidates are judgement picks from the newest comment only; older comments on those tickets were not read for further scope.
- Linear priority sort in candidates.tsv uses the numeric priority (1 urgent to 4 low, 0 none last).
