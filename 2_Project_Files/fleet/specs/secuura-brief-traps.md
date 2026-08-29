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
