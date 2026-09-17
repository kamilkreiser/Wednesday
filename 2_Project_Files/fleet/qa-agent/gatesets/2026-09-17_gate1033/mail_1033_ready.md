auth: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat B

BLUF
PR-7 is READY FOR QA as #1033 at 2cab54988b4e7b71d403576719f5fd80e470fa92 (head read from origin in the same action as this send). It overrides mysql2 to 3.23.1 in services/originate + root and removes rows GHSA-rgwj-5xj2-c3m3 (KS-763) and GHSA-3f6p-5ww8-9rcr (KS-751): 31 -> 29. Proposed TIER 1: mysql2 ships in the originate runtime image, and this PR changes that shipped copy.
- Two ticket facts need your eye:
  (a) KS-763 now reads In Progress; the brief read it In Review. The PR body's `Refs KS-763` walked it (the known behaviour). Reported, not reversed.
  (b) KS-751 is ARCHIVED (2026-09-05). Linear attached #1033 to KS-763 only, and commentCreate on KS-751 returns "Entity not found: Issue". Its facts are carried in KS-763's comment and the PR body. Question at the end.

WHAT'S IN IT (commits on base develop)
- 9fd3cb924: 2 manifests (`"mysql2": "3.23.1"` in overrides), 2 locks, both rows removed.
- 2cab54988: merge of develop bb848b828 (#1026, #1028, #1030), never rebased.
  - #1030 also touched the root lock and the baseline; git merged both with no conflict.
  - I rebuilt each from develop's blob with this recipe: root `npm update mysql2 --package-lock-only --ignore-scripts`; baseline = develop minus the 2 rows. Both are BYTE-IDENTICAL to git's merge.
  - Merge tree e52244863 = `git merge-tree --write-tree` of the parents.
- Files vs develop (three-dot): 5.

RESOLUTION BY PARSE (your 11:07:34Z item 2)
- mysql2 is 3.23.1 in BOTH locks (root, services/originate); 3.15.3 absent; nothing below 3.22.0. Across all 45 tracked locks only these 2 carry mysql2.
- services/originate: `npm install --package-lock-only --ignore-scripts --no-workspaces` moved it.
- Root: the same install returned rc 0 and left the lock BYTE-IDENTICAL at 3.15.3 (the KS-749 inert-override trap). `npm update mysql2 --package-lock-only --ignore-scripts` moved it.
- Scope: 4 entries per lock, all inside mysql2's own subtree (mysql2; +sql-escaper 1.5.2; -seq-queue; -sqlstring). Flag class unchanged (devOptional).
- Ranges checked BOTH directions, applying #1030's F1 lesson: every declarer of a moved entry, plus every moved entry's own dependency ranges (9). 0 bad.
  - The only unsatisfied range is prisma -> mysql2 "3.15.3", the ruled override.
  - Planted out-of-scope, flag-change and own-dep-range controls each rc 1.
  - My first flag control picked denque, which ioredis shares and which carries no flag, so it could not fail. It was re-pointed before any reading.

REACHABILITY
- Ships: mysql2 is in the originate runtime image per both rows' own 09-02 / 09-06 measurements. NOT re-measured (no image).
  - The container emulation of the builder's `npm ci` on originate's own lock installs mysql2 3.23.1, sql-escaper 1.5.2, no sqlstring.
- Loads: 0 imports of mysql2 in services / packages / frontend / connectors (controls ioredis 16, pg 44, @prisma/client 1). 0 "mysql" in originate/src (control postgres 87). The only schema.prisma: provider "postgresql". 0 prisma.config tracked. No runtime load trace was done.

GATES (shipped scripts, at 2cab54988)
- fix (29 rows): audit-gate rc 0 (28 reported / 29 baselined); audit-locks rc 0 (43 lockfiles).
- control (develop's 31): rc 0, CLEANUP lists exactly GHSA-3f6p (KS-751) + GHSA-rgwj (KS-763).
- negative control (WT1 = develop bb848b828, porcelain 0, baseline minus 2): audit-gate rc 1 exactly the 2 (3f6p high, rgwj moderate); audit-locks rc 1 exactly the 2 (services/originate).

TESTS (merged head, 12:24-12:26Z)
- Host `npm ci` (hoisted mysql2 3.23.1, vitest 4.1.11), shared built:
  - originate jest 63/63, 656/656.
  - packages/shared: first run 3 failed | 848 at load1 ~13, all "Test timed out in 5000ms" in repo-walking guards (crypto-agility.guard, entrypoint-corpus, ks764 call-site). Re-runs 851/851 with --testTimeout=60000 (load1 8.15) and 851/851 plain (load1 7.74).
- Container node:24-alpine (originate Dockerfile builder emulated: shared build, originate own-lock `npm ci --ignore-scripts`, @secuura/shared link, no apk, no image):
  - `npx prisma generate` rc 0 (Prisma Client 7.8.0: the prisma CLI works with its exact pin overridden);
  - `npx jest --runInBand` 63/63, 656/656 (twice: at 9fd3cb924 and at 2cab54988).
  - The first container run (parallel workers, at 9fd3cb924) was VOID: 32 of 35 FAILs were "jest worker ... terminated ... SIGKILL", memory in the shared Docker VM. I killed my own container by exact name. Memory saved.
- `lockfile-cleanroom.sh services/originate`: OK.
- In-hook preflight on push: "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed." Legs 3, 4, 8 skipped (no stack), so NOT a pass. Leg 2 35/35; leg 5 59/59; leg 6 OK 28/29; leg 7 OK. Push rc 0 (keepalives on the command only).
- Post-push: 4 orphan login_stub listeners (KS-1201) ended by verified pid (WT2 tool, which differs from WT1's only at line 7); ps rows 1131; 0 of mine remain; 17 non-node controls unchanged.

NOT COVERED
- Image build; a runtime load trace in a built originate image.
- Any MySQL datasource path (none exists).
- Live platform suites.
- Other members' suites: their trees are unmoved; only mysql2's subtree moved, in 2 locks.

F2 WORDING (carried from #1030's GO)
The body scopes the tier evidence: it covers the originate runtime (the only runtime with mysql2) and the 2 locks that carry mysql2, "not a claim about other runtimes".

TICKETS
- KS-763: comment fa2f3a9b-ddd6-48e2-8016-09fcd6b56c16. It names #1033 and both rows, says the qs rows are PR-4, and is not @-mentioned. Attachments: KS-763 contributes only.
- KS-751: comment NOT posted (archived, see BLUF b). The KS-763 comment and the PR body carry "GHSA-3f6p fixed; browserslist x2 untouched".

OPEN PRs
- 21 open. The root lock is also touched by Dependabot #949, #948, #947, #946, #945, #649, #639, #635, #575, #572; services/originate/package.json by #949 and #575; the root package.json by #945 and #920.
- 0 others touch audit-baseline.json. #1033 is my only open PR.

QUESTION (not blocking the gate)
KS-751 is archived, so it takes neither the PR link nor a comment. Do you want it unarchived so the facts comment can land (a state change I will not make without a ruling), or is carrying the KS-751 facts on KS-763 + the PR body enough?
DEFAULT: leave KS-751 archived and untouched.

NEXT (lane rule)
Build PR-4 (qs x2, rows 1-2, KS-763; express 4.22.3 in range + body-parser override 1.20.6 -> 1.20.8 in 20 manifests; one KS-775 comment with the exact sentence) locally while #1033 is gated. Push only after #1033's MERGED receipt.

Records: 5_Project_History/2026-09-17_seatB-succ1/pr7/.

Seat B

