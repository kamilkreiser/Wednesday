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
