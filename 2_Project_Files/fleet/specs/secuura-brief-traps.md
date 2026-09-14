# Secuura/Blockchain — standing traps every brief carries (consolidated 2026-08-30)

Each line is a measured fleet insight from the 08-27→08-29 sessions (ledger rows cite the
session). Paste the relevant ones into the HOLDS / DEV-PROCESS section of a Secuura brief;
do not rely on the agent remembering them across sessions.

- **Name the ref your running stack was built from** (s86/s87): app images carry no
  `org.opencontainers.image.revision`; a running container is a representation of WHICH
  ref — prove by build time + a content probe (symbol present/absent with a control), and
  rebuild from a DETACHED worktree at the target ref, never from a dirty checkout.
- **A gitignored `dist/` is invisible to `git status`** and can carry a contaminant into a
  rebuild (s87); `.dockerignore` is the only guard — check it names `services/*/dist`.
- **Compose-hash precondition before any "deploy one service"** (s85/s90): a shared
  `x-stack-labels` anchor puts every service's config hash in play; measure with
  `compose config --hash` first; deploy with `--no-deps` when only one service changed.
- **Compose SERVICE name ≠ container_name** (s87): `up -d <service>` can do nothing while a
  health poll passes on the OLD container — print the running image version after every
  deploy step.
- **Spec ≠ Akto collection** (s88/KS-725): `test:pr` never re-imports the spec, so a newly
  declared op is scanned ZERO times; "declared" is not "scanned".
- **`env | grep VAR` prints `VAR=` for an empty value** (s89): presence is not a value —
  check length with a known-set control.
- **Any diff/identity manifest needs `IDENTICAL > 0` as a control** (s90): a dead SSH leg
  reports "0 identical" exactly like a total rewrite.
- **NOAUTH is a null, not a zero** (s83/s90): an unauthenticated redis-cli scan returns
  nothing and reads as "no keys"; `dbsize` answering NOAUTH is the tell.
- **`--ignore-path` / `.prettierignore` misses `*-ks-NNN-probe` variants** (KS-702/706/711
  family): quarantine probe residue before the Prettier gate, never delete it.
- **Linear `comments(last:N)` returns the OLDEST** — `first:50` + client-side sort, always.
- **Approval instrument**: `/pulls/N/reviews` is blind to shadow-flagged reviewers; an
  approval is absent only when BOTH the reviews endpoint AND the search index say so, and
  `commit_id` must equal the head being merged.
- **A review request / comment / merge WALKS every attached Linear ticket** — census after
  every PR action and revert states on tickets you do not own.
- **Positive controls WRITE on this system** (originate auto-anchors to preview testnet;
  a POST probe can mint keys) — label the artefact, never delete it.
- **Read package.json's test script before running any suite** (s94): `npx vitest` at a
  jest service prints "N suites failed, no tests" — reads exactly like a broken service.
- **Rebuild `packages/shared` AT THE REF BEING MEASURED** (s94): a gitignored dist/
  survives branch switches and manufactures phantom cross-branch failures.


- **(2026-09-01, s97) The GitHub search index does NOT track approval staleness.** After a push over an approved head, `/pulls/N/reviews` correctly shows the APPROVED review with the OLD `commit_id` (= stale), while `search/issues?q=…review:approved` STILL lists the PR as approved. Rule: the search index is an instrument for ABSENCE only (an approval is absent when BOTH instruments say so); AT-HEAD-NESS is decided ONLY by the reviews endpoint's `commit_id == head`, re-read at merge time. A guard keyed on `review:approved` would merge on a spent signature minutes after a push.

- **(2026-09-02, s100 — recurrence of s78's 08-27 trap) `docker compose` run from `Blockchain/Dev` takes the PROJECT NAME `dev`**: `build security` prints ` security  Built`, exit 0, and builds `dev-security` while the running stack is project `2_project_files` — nothing you run afterwards uses it, and `up -d --no-deps` then collides on `container_name`. Always `-p 2_project_files` (or run from the stack's own directory), and prove the swap by grepping the changed string INSIDE the running container against the rollback image, never by the build output.

## Added 2026-09-02 04:2x from s101's wrap (Wednesday's rulings 2/3 + the session's own)
- **A control proves the harness only when it is pointed at the same defect as the claim.** (run.sh history queried on a hand-retyped path; the control was correctly prefixed so it could not fail where the claim did.)
- **Mixed-age local images:** every SET report names, per touched service, the image build time + the ref it was built from. Suites describe the running images, not the branch.
- **First attachment walks a ticket** (branch key OR first body/title mention) — HYPOTHESIS, three events, the discriminating case unobserved. Name a branch after a ticket only when the branch IS the work.
- **A completion banner is not a completion:** a wrapper printed `SET COMPLETE` rc=0 having run zero suites (`systemTest/` at the repo root). Read each suite's own totals.
- **A control that returns zero for the right reason cannot discriminate:** a swap control must be non-zero on BOTH sides of the swap.
- **`npm ls` reads `node_modules`; `--package-lock-only` does not touch it.** An override's effect is readable only in the lockfile.
- **Middleware mounted above its declaration must be a FUNCTION declaration** — a `const` arrow throws at import (`ReferenceError … before initialization`) and the suite reports N skipped, which reads like a pass.
- **A brace matcher must track comments, not only quotes** (an apostrophe in a `//` comment opened a string to EOF; 245 lines deleted, success reported — caught by diffing the edit).

## Added 2026-09-14 15:4x by Wednesday (from s220's #985 STOP, s224's five merge-ins, s223's wrap)
- **The squash-stack shape (standing since 2026-09-14 12:06, ruled by Wednesday):** develop merges are SQUASHES, so a PR stacked on another PR's branch CONFLICTS the moment its parent squashes (the content is on develop without the ancestry). Resolution: a STACK seat (or the lane seat itself) does `git merge --no-ff <develop>` INTO the PR branch — NEVER a rebase (`push_protocol.py` reads a non-fast-forward as PROTOCOL-DIFF; Peter's line-cited heads stay in history) — resolving to the PR's side region-wise (`-X ours`), never wholesale; the merge seat verifies the new head by TREE EQUALITY against the gated file set + blobs and squashes WITHOUT a re-gate. **Where develop ALSO moved a file the PR touches, the equality target is the gate's MERGED-tree blob for that file, not the PR's raw head blob** (s224's #984 catch: the raw head lacked #881's regions). Rehearse against a synthetic squash (`commit-tree` of the parent's `merge-tree` result) before the real merge-in.
- **Every root `jest.mock('@secuura/shared', …)` under `services/originate/src/__tests__/` goes through `makeSharedMock` (the helper #931/KS-1061 introduced) or the completeness guard reds** — a hand-written root factory is a guard red on develop (s223's fold of ks1103 + ks764). The guard is a TEXT scanner (single-quoted `jest.mock(` only, non-recursive `readdirSync`, blind to `jest.doMock` and double quotes — the L3b gate's F-931-G1, ticketed): a brief that adds a test file under `__tests__/` says so, and a double-quoted or nested factory is a guard hole, not a pass.
- **`packages/shared` dist trap:** `tsc --noEmit -p services/originate` is RED until `packages/shared` is rebuilt on the merged tree (`dist` is gitignored; the source's copy goes stale) — rebuild before reading a red; and that tsconfig EXCLUDES `src/__tests__` (0 test files type-checked) — a Test Evidence line citing it as type-checking the tests names the wrong instrument (F-931-G2); ts-jest type-checks at run time, or use an inclusive temp tsconfig.
- **Linear ARCHIVES a parent's non-terminal children with it (measured 2026-09-14 05:48Z: KS-487's Done + archive archived KS-801 In Progress/High, KS-629, KS-915 — s226 found it; 61 such archived-but-non-terminal issues team-wide).** Before archiving any ticket, read its `children`; archive only when every child is terminal, else leave it Done-but-unarchived and say so in the closing comment. A cascade victim vanishes from every active view, the ≤ 60 count included.
