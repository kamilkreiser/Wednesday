# Drafter notes, Seat B 181st brief, 2026-11-15 20:36 AEDT (read-only drafter)

Scripts (scratchpad): /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/3880780d-5e8a-4784-b37a-d0016843aba4/scratchpad/w/mt181.py plants181.py census181.py matcher181.py kit181.py cmt181.py linear_read.py

## MERGE TREES + PLANTS (develop d7dc7de435ce)
DEV d7dc7de435ce devtree 4481139ec66d
ROW 1 2098 943b69fdd988 mb 7eda23b34d3b ahead 104 commits 1 files 4 rc 0 0 tree d367541f223b d367541f223b same True
ROW 2 2079 0fffdfba0f95 mb c5c26b2835df ahead 126 commits 1 files 18 rc 0 0 tree 716c76810ce6 716c76810ce6 same True
ROW 3 2223 8752357228cd mb 1dd6299bccd6 ahead 27 commits 1 files 2 rc 0 0 tree e8ca0d09e7c6 e8ca0d09e7c6 same True
ROW 4 2224 a160347eab66 mb ae5b615f4cc0 ahead 25 commits 1 files 2 rc 0 0 tree 08befde70bfb 08befde70bfb same True
ROW 5 2081 17c453253d68 mb c5c26b2835df ahead 126 commits 2 files 6 rc 0 0 tree 862f592d2c81 862f592d2c81 same True
pairs checked 28, nonclean 0
intersecting [] distinct paths 32
self-control 2224 vs itself 2
2098 Blockchain/Dev/services/auth/src/auth.openapi.ts line 5 pos rc (1, 1) neg [(2079, 0, 0), (2223, 0, 0), (2224, 0, 0), (2081, 0, 0)]
2079 Blockchain/Dev/services/shared/src/index.ts line 8 pos rc (1, 1) neg [(2098, 0, 0), (2223, 0, 0), (2224, 0, 0), (2081, 0, 0)]
2223 Blockchain/Dev/services/auth/src/routes/auth.ts line 64 pos rc (1, 1) neg [(2098, 0, 0), (2079, 0, 0), (2224, 0, 0), (2081, 0, 0)]
2224 Blockchain/Dev/services/api-gateway/src/services/enforcement.ts line 55 pos rc (1, 1) neg [(2098, 0, 0), (2079, 0, 0), (2223, 0, 0), (2081, 0, 0)]
2081 Blockchain/Dev/services/anchoring/src/anchorSubmission.ts line 217 pos rc (1, 1) neg [(2098, 0, 0), (2079, 0, 0), (2223, 0, 0), (2224, 0, 0)]
pos ok 5 of 8; neg ok 5 of 8

## CENSUS
rc 0 47840
open 82 truncated 0
rows present [2098, 2079, 2223, 2224, 2081]
touch lock: [575, 635, 639, 649, 945, 946, 947, 948, 949, 1965, 2099]
anchoring: [575, 649, 2081, 2194]
updated since 11-13T03:30: []

## MATCHER
n 740 distinct 740 head ['B 180th', 'B 179th'] tail ['B 1580th', 'B 281st', 'B 1081st', 'B 1181st', 'B 1481st', 'B 1581st'] B181 in False B180 in True B 182nd True main edits 4
b181_match_scratch.py rc 0 self-test: 749/749 as expected
b181_match_mutant.py rc 1 self-test: 749/750 as expected
  MISMATCH ('[Wednesday -> Secuura/Blockchain-B] GO: merge PR 99999 (Seat B 181st)', 'OTHER', 'MINE')
b181_match_bare.py rc 1 self-test: 742/744 as expected
  MISMATCH ('[wednesday -> secuura/blockchain-b] go: merge pr 99999 (SEAT B 180TH)', 'MINE', 'OTHER')
  MISMATCH ('[Wednesday -> Secuura/Blockchain-B] GO: merge PR 99999 (Seat B 181st)', 'OTHER', 'MINE')
bare rule: n 735 distinct 735

## KIT
tools regular files 39
evidence regular 212 evidence .py/.sh 85 aids regular 11
src_b179 (not ls recursive)  39 src_b179_evidence 54
tools files 39 files carrying b180 37 {'b180': 140, 'B 180th': 115, '180th': 140, 'REC180': 0, 'b179': 0, 'B 179th': 2}
evid files 85 files carrying b180 82 {'b180': 660, 'B 180th': 205, '180th': 294, 'REC180': 0, 'b179': 45, 'B 179th': 28}
hex/hyphen adjacency hits for b180: 11
   ('evid', 'merge_trees_plan_b180.before_pin_edit.py', '\'eat-b180", G\'')
   ('evid', 'merge_trees_plan_b180.before_pin_edit.py', "'eat-b180@inv'")
   ('evid', 'merge_trees_plan_b180.before_pin_edit.py', '\'eat-b180", G\'')
   ('evid', 'merge_trees_plan_b180.before_pin_edit.py', "'eat-b180@inv'")
   ('evid', 'merge_trees_plan_b180.py', '\'eat-b180", G\'')
   ('evid', 'merge_trees_plan_b180.py', "'eat-b180@inv'")
   ('evid', 'merge_trees_plan_b180.py', '\'eat-b180", G\'')
   ('evid', 'merge_trees_plan_b180.py', "'eat-b180@inv'")

## LINEAR
KS-2022 [In Progress/started] updatedAt 2026-11-08T14:32:51.717Z assignee kamil.kreiser@secuura.ai labels [] | auth: four comments cite stale line numbers into services/auth/src/services/passwordLogin
   comments 1 more=False oldest 2026-11-08T14:32:56 newest 2026-11-08T14:32:56 newest-author kamil.kreiser@secuura.ai
KS-657 [In Progress/started] updatedAt 2026-11-06T18:16:32.482Z assignee kamil.kreiser@secuura.ai labels [] | services/shared (@secuura/service-utils) cannot build — no tsconfig.json, so main/types po
   comments 9 more=False oldest 2026-08-17T06:32:25 newest 2026-11-06T18:16:44 newest-author kamil.kreiser@secuura.ai
KS-1776 [In Progress/started] updatedAt 2026-11-12T20:52:10.203Z assignee kamil.kreiser@secuura.ai labels [] | services/auth routes/auth.ts:62: a module-scope 2 s setTimeout calls userRepo.seedDemoUse
   comments 2 more=False oldest 2026-11-11T23:07:30 newest 2026-11-12T20:52:10 newest-author kamil.kreiser@secuura.ai
KS-1197 [In Progress/started] updatedAt 2026-11-12T22:01:56.046Z assignee kamil.kreiser@secuura.ai labels [] | A non-string verificationLevel claim: POST /api/documents answers 500 and a verifier-gate
   comments 3 more=False oldest 2026-10-12T09:41:10 newest 2026-11-12T22:01:55 newest-author kamil.kreiser@secuura.ai
KS-1171 [In Progress/started] updatedAt 2026-11-06T18:45:59.236Z assignee kamil.kreiser@secuura.ai labels [] | Guard 3's re-poll reads a MIXED window as ABSENT — one early "not found" then an unreacha
   comments 6 more=False oldest 2026-09-25T02:53:39 newest 2026-11-06T18:45:59 newest-author kamil.kreiser@secuura.ai
a6884924-e56d-4705-b181-af2deef051a3 -> {'errors': [{'message': 'Entity not found: Comment', 'path': ['comment'], 'locations': [{'line': 1, 'column': 
a6884924-e56d-4705-b177-af2deef051a3 -> {'data': {'comment': {'id': 'a6884924-e56d-4705-b177-af2deef051a3', 'createdAt': '2026-11-12T20:04:43.930Z', '
a6884924-e56d-4705-b180-af2deef051a3 -> {'errors': [{'message': 'Entity not found: Comment', 'path': ['comment'], 'locations': [{'line': 1, 'column': 
a6884924-e56d-4705-b180-af2deef051a3 -> {'errors': [{'message': 'Entity not found: Comment', 'path': ['comment'], 'locations': [{'line': 1, 'column': 

## UNMEASURED
- Every install, suite, tsc, eslint, vitest/jest run; the auth service's test script and suite size (auth package.json not read).
- The matcher on the real kit (749/749, mutant 749/750, bare rule 742/744 are scratch-copy figures); tools manifests not re-hashed.
- B 180th's FINAL block and its 2222 MERGED mail (absent at drafting); its STATE block is stale on 2222.
- Gate verdicts beyond line 1 / table lines / hex counts; K 23rd's brief beyond lines 1-6, 27-28, 44-47.
- Own-authored evidence count (31 by name-diff is approximate).
- Scripts print template labels "28 pairs" and "of 8": real set is 10 pairs and 5 rows.
