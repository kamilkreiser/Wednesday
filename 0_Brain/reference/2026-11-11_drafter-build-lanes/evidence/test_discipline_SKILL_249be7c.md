---
name: secuura-test-discipline
description: Planning, environment, build/teardown, documentation and done-criteria rules for Distributed_Secuura (platform-k) and platform-s. Use before planning any change, before running any test suite, before rebuilding any Docker stack, and before reporting any work as done or moving a ticket to Done.
---

# Secuura test discipline

Governs **where** work runs, **how** an environment is rebuilt, **whose review
wins**, and **what "done" means**. Check the relevant section before acting.

---

## 1. Plan before you touch anything

**Every change starts with a detailed written plan.** No edits, no rebuilds, no
suite runs until the plan exists and has been checked against the sources below.

Ground the plan against all of these:

1. **The Linear ticket(s)** — the KS ticket, its parent/umbrella, and the project
   register. Team Secuura-PK, key KS.
2. **Reviewer comments** — see the authority rule below.
3. **The `.md` files and docs** in the repo, including `CLAUDE.md` and
   `systemTest/CLAUDE.md`.
4. **The code itself** — verify the claim, don't trust the doc. Docs go stale; a
   `file:line` you have actually read is evidence, a doc sentence is a lead.

Where these disagree, say so in the plan rather than silently picking one.

### Review authority — whose comments take precedence

- **platform-k base code → Kamil's comments take precedence.**
- **platform-s code → Stuart's comments take precedence.**
- **`systemTest/` on BOTH platforms → Peter's comments take precedence.** He owns
  the test estate on either side (KS-492 G on platform-k; the platform-s suite),
  so on test code, harness design, gate logic and reporting his call decides.

**But their input on the tests is actively wanted, not merely tolerated.** Kamil
and Stuart know the behaviour under test better than the harness does, and a test
that contradicts the platform owner's model of the system is usually the test
that is wrong. So:

- **Seek their input before settling a test's expectations**, not after — a ruling
  that arrives at review costs a rewrite.
- **Quote the ruling verbatim beside the assertion** it justifies (systemTest MUST
  #15), with the ticket. A paraphrase drifts; the quote is the record.
- **Where Peter overrides an owner's comment on test code, say so explicitly and
  why**, in the ticket — never silently. The precedence settles who decides, it
  does not licence dropping their objection unrecorded.

Review comments outrank docs, tickets, and your own reading of the code. If you
are about to do something that contradicts a comment from the reviewer with
authority over that area, stop and surface the conflict — do not proceed on the
assumption the comment is outdated.

Ownership boundaries: Kamil owns platform-k security work-streams A–F + H
(KS-486…KS-491, KS-493); Peter owns all systemTest security work (KS-492). File
new work into the correct work-stream — never loose in the backlog.

### Secrets — report the problem, never solve it

**Applies to both platforms, in planning and in execution.**

- **Never open, read, quote or edit a secrets file in a session.** That includes
  the restored `appsettings.Development.json` and `restore-local-secrets.sh`
  output (platform-s), `.env` / `.env.local` (platform-k), rendered
  `Docker.appsettings.*` configs, and anything pulled from Secrets Manager or a
  Key Vault.
- **When an issue involves secrets, report it and stop.** Name the file and the
  symptom, say which *key* a person should check and what value shape is
  expected, then let them make the change. Naming a key is fine; opening the
  file to see its values is not — no patch, no worked example, no "just set it
  to…".
- **Why:** on PS-309 a secrets file was read in-session and every platform-s
  secret had to be rotated. Stuart's instruction: *"For issues such as these
  that involve secrets just report the problem, don't provide a solution."* The
  cost is the team-wide rotation, not the disclosure alone.
- If a diagnosis dead-ends at that boundary, **say so explicitly** and hand the
  step to Peter. An unfinished diagnosis is the correct outcome here, not a
  reason to look.

---

## 2. Environment separation — run it where the result means something

**Individual host setups are each developer's own business.** This skill states no
requirement about which machine anyone works on. What it does require is that a result
is *evidence*.

- **Before running anything, state which host/environment you are on and why it is the
  right one for this suite.** One line. If you cannot justify it, stop.
- **A result from an unrepresentative environment is not evidence.** Judge that per
  suite, and state the gap you are accepting alongside the result. The measured gaps on
  an Apple Silicon Docker Desktop host (checked 2026-09-01, `docker info`): the daemon
  reports `aarch64/linux` and runs arm64 images **natively**, so an arch-sensitive
  failure surfaces on amd64 CI rather than locally; and bind-mount uid/gid is
  virtualised, so a permissions-shaped failure can reproduce on one and not the other.
  Both are directional caveats to quote with a result — neither makes a local pass
  uninformative.
  *(Corrected 2026-09-01. This bullet previously claimed Docker Desktop "emulates amd64
  via Rosetta" and concluded a Mac-local platform-k pass was uninformative. `docker info`
  disproves the premise — Rosetta engages only for explicitly-amd64 images, which on this
  estate means just `phpmyadmin/phpmyadmin:5.2`, a platform-s dev dependency and never a
  product path. The conclusion fell with it.)*
- **Two stacks of the same platform on one host no longer collide — use the slots.**
  platform-k namespaces every published port, compose project, volume and network off
  `SECUURA_STACK_SLOT` (KS-666, PR #729); platform-s does the same off `STACK_SLOT`
  (PS-622). The numbering is shared, so platform-s slot N targets platform-k slot N with
  no extra configuration, and slot 1 keeps every historic port. platform-k's own gate
  asserts the isolation — `node Blockchain/Dev/scripts/check-port-crossover.mjs` reports
  *102 allocations across 3 platforms (platform-k=15, platform-s=8, observability=10)
  disjoint for slots 1-4* (re-run 2026-09-02). Pair each slot with its own worktree.
  **Four is the ceiling, and it is enforced, not conventional** — `stack_env.sh` sets
  `SECUURA_MAX_STACK_SLOT=4` and slot 5 exits 2 with *"exceeds the supported maximum of
  4"*; a non-integer or `0` is refused outright rather than defaulted to 1, because a
  silent fallback would aim the command at another ticket's stack. Four is a deliberate
  choice, not the arithmetic limit: the two platforms' allocations first collide at
  **platform-s slot 9**, where its PMA proxy (8081) meets platform-k's tokenomics port
  (8881), and Docker Desktop's allocation runs out well before that. Bases live in
  `Blockchain/Dev/scripts/port-allocations.json` — edit them there, never in isolation in
  a compose file.
  *(Corrected 2026-09-01. This bullet previously said a second platform-k stack "fights
  all of" 6090-6094, 6379, 6432 and 6882 — true before KS-666, false since.)*
  *(Corrected 2026-09-02. It also said "slot 5 lands on the CI integration block", which
  is not the reason and is not what happens — `stack_env.sh` refuses slot 5 before any
  port is allocated. Verified by running it for slots 1, 2, 4, 5, 0 and `abc`.)*
  Two **different** platforms on one host were never a port conflict (verified
  2026-08-19), but the blast-radius judgement stands and now applies between slots too:
  a blanket teardown still reaches another slot's volumes, which is why the teardown in
  §3 is scoped rather than global.
- **Slots isolate containers, and — per clone — database credentials (KS-731, Done
  2026-09-13; fixed by #800 on 2026-09-04).** The reachability rule stands: confirmed with
  an own-slot positive control, **a service is reachable cross-slot iff it publishes a host
  port** — one that publishes nothing is unreachable, because Docker blocks inter-bridge
  traffic. A default stack with the tokenomics overlay and Akto up publishes eight
  (`postgres`, `redis`, `pgbouncer`, `nginx-gateway`, `website-frontend`,
  `tokenomics-website`, `akto-dashboard`, `akto-mongo`), and profile-gated publishers
  (`cardano-mock`, `cardano-devnet`, `ollama`) only appear when their profile is rendered —
  `systemTest/CLAUDE.md` holds the per-compose-file table.
  What changed is what a cross-slot connection can DO. `scripts/bootstrap-env.sh` now
  generates `POSTGRES_PASSWORD` and `REDIS_PASSWORD` per clone (and rebuilds `DATABASE_URL` /
  `REDIS_URL` with them), so a connection that reaches another clone's published port **fails
  authentication** — Postgres `password authentication failed`, Redis `WRONGPASS` — where
  on 2026-09-01 it read, wrote and DROPped as superuser. Classify Redis on the output, not
  the rc: `redis-cli` exits 0 on `WRONGPASS`.
  **Existing clones are NOT fixed by pulling**: the generator only fills blank values and
  Postgres honours `POSTGRES_PASSWORD` only on first init, so blank the two passwords and
  both URLs in `.env`, re-run `bootstrap-env.sh`, then tear each slot down **with
  `--remove-volumes`** and bring it back up.
  **Four slots from ONE worktree still share a single `.env` and can never be
  credential-isolated** — one worktree per slot is the precondition.
  **No suite result was ever in question** — services reach their DB by compose name inside
  their own network, cross-slot DNS fails 12/12, and `systemTest` hardcodes no DB port.
  `start-environment.sh` and `start-local.sh` now print the slot's own
  `localhost:${POSTGRES_EXTERNAL_PORT:-6432}`; anything else of yours that defaults to
  `localhost:6432` still hits slot 1 whichever slot you meant.
  *(Corrected 2026-09-28 under KS-1365. This bullet was headed "KS-731, OPEN" and said a
  cross-slot connection authenticates and can read, write and DROP another slot's Postgres —
  true on 2026-09-01, false since #800. It also listed six publishers, missing Akto's two,
  and said both start scripts print `localhost:6432` regardless of slot. It carried its own
  instruction to be rewritten, not dropped, when KS-731 closed; this is that rewrite, matching
  `systemTest/CLAUDE.md` → What slots DO and do NOT isolate.)*
- **`APP_DB_PASSWORD` keeps its compose defaults — KS-762 (2026-09-03):** "KEEP THE DEFAULTS".
  No `:?required` switch; the `${APP_DB_PASSWORD:-<literal>}` fallbacks stay so no local stack or
  fresh clone breaks. `scripts/check-app-db-password-default.sh` reports that held state; the
  switch is re-raised only after the rotation, with notice to Peter and Stuart. (KS-731's slot-1
  destructive grant of 2026-09-03 was a one-off, not this ruling.)
- **Once rate limiting appears, wait 15 minutes before starting ANY further tests** —
  not just the run that tripped it, and not just the live integration gate. The
  limiter's window has to drain; starting again inside it produces a second
  uninformative run and pushes the window out further, so the fifteen minutes are
  cheaper than the retry.
  **This applies to every harness, not just Schemathesis** — Akto, Schemathesis, Playwright
  and the performance suite all authenticate through the same gateway as the same
  personas, so any of them can trip the limiter and any of them can be starved by
  another. Schemathesis is simply where it was first seen, because its report names the
  cause; the others surface it as login failures, empty result sets or timeouts, which are
  easier to misread as product bugs.

  Rate limiting shows up in two shapes, and only one of them is an HTTP status:
  - **429s** from the platform;
  - **`login for persona=… is rate-limited`** in a harness's own errors. This one is
    easy to miss because the run often still reports **PASSED** — the operations were
    never exercised, so nothing could fail — and the errors may be filed as *engine*
    errors, reading as a harness fault rather than the platform's limiter working.
  Treat either as the same signal: stop, wait fifteen minutes, then start.
- **Run one suite at a time against a given stack.** The platform's login limiter is
  per-IP, and every local suite shares one IP, so two harnesses against one stack
  multiply the login rate and starve each other of sessions. Schemathesis was
  previously recorded here as exempt because it self-throttles — that holds only when
  it runs ALONE. Measured 2026-08-20 with Playwright, Schemathesis and k6 together on
  one stack: Schemathesis produced **300 engine errors across 289 operations**, all
  `login for persona=super_admin is rate-limited`, and still headed its report
  **PASSED** — the operations were never exercised, so nothing could fail. A run that
  tests almost nothing and reports success is worse than a red one.
  On platform-k use `systemTest/run-in-slot.sh <slot> <command>`, which holds an
  exclusive per-slot lock; slots still run in parallel with each other.
  **All four harnesses are isolated per slot, Playwright included (KS-682)** — gateway,
  report, per-test output directory, `latest` pointer, auth token, HAR and the report
  server's own host port all carry the slot, so running the same suite on several slots
  at once is safe and their artefacts cannot overwrite each other. That is the opposite
  of permission to run two suites against ONE slot, which is what this rule forbids: the
  limiter, the gateway and the auth directory are per stack, not per suite. Per-slot
  values and what each one prevents: `systemTest/CLAUDE.md`, beside the Akto statement.
  **That lock is machine-scoped and keyed by slot alone (KS-688).** It used to live under
  `$REPO_ROOT`, so two worktrees aiming at the same slot each took their *own* lock, both
  acquired, and both suites ran against one stack — the exact collision slots exist to
  prevent. Its test could not catch it either: the "second suite on the SAME slot is
  refused" case invoked the runner twice from one path, so one `REPO_ROOT`, one lock. The
  test shared the defect's assumption and returned a confident green.
  **Four concurrent sweeps have never been measured** — on any harness, at any scale. Four
  stacks *running* is measured (KS-666); four suites *executing* is not, and Docker Desktop
  on the Mac where it was measured is allocated 8 CPUs (`docker info`, 2026-09-28 — the
  allocation is per-machine, so quote it with its host). For a correctness suite like Schemathesis contention should not change verdicts,
  but it can manufacture timeouts, and a harness timeout that reads as a platform failure
  is the KS-435 / KS-610 shape. Quote no timing from a run that shared the machine.
  *(Corrected 2026-09-28 under KS-1365. This said "Docker has 6 CPUs" — stale; `docker info`
  measured 8 on 2026-09-28, matching the 8 `systemTest/CLAUDE.md` recorded on 2026-09-04.)*

All paths in this skill are **relative to the repo root** of the platform in question,
unless written with a `~` (a host home directory).

> Individual developers' host layouts — which machines they use, and their per-ticket
> worktree and stack conventions — are deliberately **not** here. They belong in a
> personal, machine-local skill outside these repos, because they bind only that
> developer's sessions.

---

> **A LOCAL run must name its slot (KS-1016, 2026-09-11).** Every harness — Schemathesis, k6,
> Playwright, Akto and the shared provisioning step — refuses to start against a **local** target
> (`localhost`, `127.0.0.1`, `[::1]`, `host.docker.internal`) when neither `SECUURA_STACK_SLOT` nor
> the platform-s alias `STACK_SLOT` is set, and prints the command to run instead:
>
> ```text
> No stack slot named. Every LOCAL system-test run must say which Docker stack it targets.
>   SECUURA_STACK_SLOT=2 python3 scripts/run.py pr
>   or: systemTest/run-in-slot.sh 2 python3 scripts/run.py pr
> ```
>
> **Local only.** A remote target (demo, a tunnel) carries no slot and is left alone, and CI is
> exempt because its isolated per-suite stacks are local by construction and deliberately unslotted
> (GitHub Actions sets `CI=true`; the exemption is a convention, not a lock). Before this rule an
> unset slot meant slot 1 silently — another ticket's stack on a shared machine.

## 3. Build and rebuild

### The build commands

**platform-k** — from the repo root, on whichever host you run platform-k:

```bash
./Start_Up/start-secuura.sh --rebuild
```

**platform-s** — from `ssd/dep-ssd-local/` in the repo root:

```bash
./dock_run --reset --rebuild
```

Use these scripts. Do not hand-roll `docker compose up` — they carry ordering and
env setup a bare compose invocation skips.

### Teardown before rebuild — full, every time

**Rebuilding on top of existing Docker state is not a rebuild.** Stale images,
cached layers and surviving volumes have repeatedly produced results that
describe code nobody is running. Tear the environment down completely on the host
you are rebuilding, before invoking the build script.

Order matters — containers, then images, then volumes, then build cache:

```bash
docker compose down --volumes --rmi all --remove-orphans
```

```bash
docker container prune -f && docker image prune -a -f && docker builder prune -a -f
```

Volumes — **scoped, never blanket** (see the standing-infrastructure exception):

```bash
docker volume ls -q | grep -v 'portainer' | xargs -r docker volume rm
```

Verify the teardown actually happened before rebuilding — `docker ps -a`,
`docker images`, `docker volume ls`. **Do not trust a command's exit code as
proof it removed anything.** (The Container Apps teardown on 2026-07-08 exited
clean, deleted nothing, and billed ~$12.4/day for 23 days.)

### The one exception: standing infrastructure (e.g. Portainer)

**A teardown removes the stack, never the tooling around it.** Where a host runs
Portainer, its container, image and data volume survive every teardown. The same
protection applies to anything else you keep permanently on a host.

- **Never run `docker system prune -a --volumes`.** It takes everything not
  attached to a running container, including any standing tooling. Use the scoped
  commands above instead — always.
- Where such tooling exists, keep it **up to date**: pull the current image and
  recreate its container as part of the rebuild, preserving its data volume.
- Confirm the actual volume name on the host (`docker volume ls`) before pruning.
  A project-prefixed name will not match a naive filter, and deleting it is
  exactly the failure this section exists to prevent.

### After every build: verify all containers are up

The build script exiting 0 is not evidence the stack is healthy.

```bash
docker compose ps
```

- **Every expected service present, `Up`, not restarting.** Count them against the
  compose file — a missing service does not appear as an error.
- Any container with a healthcheck must be **healthy**, not merely running.
- Investigate any `Restarting`, `Exited` or `unhealthy` container before running a
  single test. Results from a partially-up stack are worse than no results.
- Where the host runs management tooling (e.g. Portainer), confirm it is still up —
  a teardown should never have touched it.
- Report the count explicitly: "N of N services up, all healthy" — or name the
  ones that are not.

### The first suite run on a fresh stack decides the actors for every run after it

platform-k only. All four harnesses provision their generated actors through
`systemTest/fixtures/provision-actors.ts` — Schemathesis via `scripts/run.py` as
much as the three TypeScript suites — and the FIRST provisioning on a fresh stack
**creates** the five actors. It needs a bootstrap admin to assign roles:

- Export **`BOOTSTRAP_ADMIN_PASSWORD`** (the value seeded through
  `ADMIN_USER_PASSWORD` in `Blockchain/Dev/.env`) in the shell of **every** suite
  run, from the very first one. Not only the TypeScript suites; Schemathesis too.
- Without it, provisioning logs `bootstrap admin: UNAVAILABLE` and creates every
  actor as `OWNER` by self-service registration. Every later run — with the
  variable set or not — finds those actors already existing, cannot change an
  existing account's role, and reports DEGRADED (`re-run with a fresh --seed`);
  Playwright then fails at `auth-setup` with a `400` because its admin password
  comes from the provisioned actor (KS-966) and there is none.
- A retry does not fix it. Reset that slot's database (`--fresh-db` on the same
  slot) or provision with a new `--seed`, then run the series with the variable
  exported from the start. A correct first run prints
  `bootstrap admin: authenticated` and `+ … role=ISSUER_ADMIN` etc.

Measured 2026-09-11 on slot 4 during the KS-1016 verification: one Schemathesis
run launched without the variable cost the k6 and Playwright runs that followed
it, and a database reset.

### Rebuild traps that survive a teardown

- **Migrations are baked into an image.** `migrations/*.sql` ships inside the
  image built from `services/originate/Dockerfile`. Rsyncing a `.sql` does
  nothing. Rebuild the `migrations` service, then **verify the schema changed
  directly** — the runner prints `applied=N failed=0` even when it never saw the
  new file. A correct run prints an explicit `Applying 0NN_….sql`.
- **The OpenAPI spec is bind-mounted, not baked** — there a rebuild is the thing
  that does nothing. But the api-gateway image *bundles*
  `docs/openapi/secuura-api.yaml` for `/api/docs` and its spec-auth gate, so spec
  changes still need api-gateway rebuilt on both targets.

---

## 4. Documentation that must move with the code

**Every test change updates its platform's two HTML docs, in the same commit —
not a follow-up.** "Test change" means backend unit, integration, *or* systemTest.

**platform-k** test change → add one **fragment** to each of the two pages, in the same
commit. Do **not** edit the pages themselves (KS-1887): two PRs that each appended a numbered
section to them conflicted on every merge (measured 2026-10-31: 28 of 44 open PRs DIRTY on those
two files alone). The pages, relative to the repo root, are
- `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` (the Flow page, numbered sections)
- `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html` (the Cheat Sheet, unnumbered)

  and they are built from the small files under `Projects Documents/fragments/flow/` and
  `Projects Documents/fragments/cheat/`.

  Note the **space in `Projects Documents`** — quote the path in every shell
  command, or the glob silently resolves to nothing and the "update" is a no-op.

  **How to add your entry** (worked example: ticket KS-1234, slug `login-lockout`):
  1. Create `Projects Documents/fragments/flow/KS-1234-login-lockout.html`. It holds your entry as you
     would have written it in the page (a Topic | Detail table; no prose outside a table), with one
     difference: never type a section number. Write `<!--n-->` where the number goes. The first line
     is `<h2><!--n-->. The lockout now counts failed logins (KS-1234)</h2>`, and a sub-heading is
     `<h3><!--n-->.1 Red against develop</h3>`. To point at another new entry, write
     `<!--ref:KS-1235-other-slug-->` and the build puts that entry's number there. One `<h2>` per file.
  2. Create `Projects Documents/fragments/cheat/KS-1234-login-lockout.html`: your Cheat Sheet entry,
     starting `<h2>The lockout now counts failed logins &mdash; KS-1234</h2>`. No tokens: the Cheat
     Sheet has no numbers.
  3. Run `node Blockchain/Dev/scripts/docs-fragments.mjs check`. It must end in `OK`; quote it in the
     PR's Test Evidence. Leg 14 of the pre-push gate runs it for any push that changes
     `Blockchain/Dev`, but a push that touches only `Projects Documents/` skips that gate, so run it
     yourself before you push.
  4. Commit the two fragment files. Do not edit either page and do not run `build`.

  The name is the ticket key plus a lowercase slug (letters, digits, hyphens) and must be unique in
  its directory. The key alone is not enough: a ticket can have several entries or several PRs, so give
  each entry its own slug. A PR with two entries adds two files per page.

  **What a reviewer sees.** The PR diff shows two small files in plain HTML, not a change inside a
  6,000-line page. To read the rendered result, run
  `node Blockchain/Dev/scripts/docs-fragments.mjs build --out "$TMPDIR/preview"` and open the two files
  it writes (a section number is provisional until the PR merges; it follows merge order).

  **Who brings the pages up to date.** Whoever merges the PRs runs the refresh after each batch of
  merges: read develop's sha with `git ls-remote origin refs/heads/develop`, pull that develop, run
  `node Blockchain/Dev/scripts/docs-fragments.mjs build --base <that sha>`, commit just the two pages and
  push. That push touches only `Projects Documents/`, so it skips the pre-push gate. Between refreshes
  the pages lag the fragments; `check` says by how many entries.

  **If a page is edited by hand** (an entry appended straight to it): nothing breaks. `check` prints an
  ADVISORY and the push goes through. At the next refresh the person running it first runs
  `node Blockchain/Dev/scripts/docs-fragments.mjs adopt`, which turns the appended entry into a
  fragment (and prints the section number it will render as), then runs `build`.

  **A PR that already carries a hand-written entry** (written before this change) is brought across once,
  at merge prep, in the PR's own worktree with a clean tree. `$D` is develop's sha, from
  `git ls-remote origin refs/heads/develop`, fetched:

  ```bash
  OLD=$(git rev-parse HEAD)                  # your PR head, before the merge
  git merge --no-edit "$D"                   # conflicts are expected, and only in the two pages
  git checkout "$D" -- "Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html" "Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html"
  node Blockchain/Dev/scripts/docs-fragments.mjs adopt --from-ref "$OLD" --against "$D"
  node Blockchain/Dev/scripts/docs-fragments.mjs check          # must end in OK
  git add "Projects Documents" && git commit                    # finishes the merge
  ```

  If the merge stops in any file other than the two pages, stop and ask. `adopt` prints each fragment it
  wrote and the section number it will render as: the number follows merge order, so it can differ from
  the one you wrote (entries added by one commit are numbered in file-name order). If `adopt` refuses, your
  change to the pages is more than an appended entry (it edited text, or extended an existing entry), and you
  convert it by hand: put the added text in a fragment of its own, under an `<h2>`.

**platform-s** test change → update both, relative to the repo root:
- `docs/platform_s_testing_architecture_flow_diagrams.html`
- `docs/platform_s_testing_cheat_sheet.html`

Rules:

- **Both fragments, every time** (platform-s: both files). The flow diagram and the cheat sheet answer
  different questions; updating one leaves the other actively misleading.
- **MANDATORY — the HTML docs carry the TIMINGS, and stale timings are a defect.** Every
  per-tier / per-suite wall-clock figure and time budget stated in `CLAUDE.md`,
  `systemTest/CLAUDE.md` or this skill **must also appear in both HTML docs, and must agree**.
  When a test change alters what a tier runs, the timing moves with it in the same commit —
  the number is not decoration, it is what people plan CI around.
  - **Quote a measurement, never an estimate.** State the figure, the date it was measured, and
    the host it was measured on. On this platform CI runs at **8.65 Akto results/s** while a local
    dev host measured **~291 results/s** — **~34x** (KS-441), so a figure without a host is
    meaningless. That local figure was taken on a machine no longer in use: **re-measure
    before planning around it.** "~7-8 min" sat in these docs for a year while the real CI figure was
    **16.1 min**, and it was the stated justification for a whole tier design.
  - **Akto tier budgets — the budget column is the MUST, the measurements are a dated snapshot.**
    They record what each tier ran at the last code change that touched it: evidence of what the
    budget bought, not a live figure. If the scope has moved since, they are stale by definition.
    Same figures must appear in both HTML docs and agree (scan step only; last measured
    2026-08-13, CI):

    | Tier | Budget | Measured | Ceiling | Ratio |
    | --- | --- | --- | --- | --- |
    | PR | <= 5 min | 11 ids · ~2,340 results · **~4.5 min** (projected) | `PR_TIMEOUT_MS` 15 min · job 40 min | 3.3x |
    | pre-merge | <= 20 min | 62 ids · ~9,400 results · **~18.1 min** | `PRE_MERGE_TIMEOUT_MS` 30 min | 1.7x |
    | nightly full | to completion | 207 ids · ~47,700 results · **~92-107 min** | `FULL_SCAN_TIMEOUT_MS` 5 h | 2.8x |

    A broad template costs ~334 result rows ≈ **~39 s of CI scan**. Check a new template against
    the remaining budget before enabling it; a bump that blows a ceiling reports a harness
    TIMEOUT as a security failure.
  - **State the ceiling as a multiple of the measurement.** A ceiling near 1x the runtime turns
    ordinary variance into a harness TIMEOUT reported as a security failure. That is KS-435, and
    then KS-610 when it recurred at **1.25x** (963 s scan under a 1,200 s ceiling). Target ~2x and
    record the multiple.
  - **If you changed which tests run, you changed a timing.** Re-measure, or say explicitly that
    the figure is a projection and from what. A doc that keeps the old number after the scope
    moved is the same defect class as a check that cannot fail (MUST #13 rule 6).
- The update reflects **what actually changed** — a new probe, a changed gate, a
  renamed outcome category, a moved file. Re-syncing a timestamp is not an update.
- **Never cross platforms.** platform-k changes never touch the platform-s docs
  and vice versa.
- If a change genuinely does not affect either doc, **say so explicitly and why** —
  do not silently skip.

---

## 5. Done criteria

Work is not done until all of these hold. Check them in the diff, not from memory
of having intended them.

### 5a. Three-way parity: console = results.json = HTML report

**results.json is the source of truth. Console and HTML are renderings of it.** If
the console computes a number the JSON does not carry, the console is wrong.

- Every outcome category appears in **all three** surfaces, same label, same
  count: PASS / FAIL / UNVERIFIED / OUT OF SCOPE / SKIPPED.
- The taxonomy is **closed and shared**. Adding a category is three edits plus the
  HTML legend/tooltip. A category that only makes sense in one surface is a design
  error. (`out_of_scope` existed in the gate logic and reached results.json only
  after being chased — KS-519.)
- **Counts reconcile:** category counts sum to the run total, and the exit code
  follows from the same numbers a human reads. A green exit beside a non-zero FAIL
  row is the failure this catches.
- **Verify mechanically, not by eye.** The durable form is a parity assertion in
  the suite; if none exists for a surface you changed, say so.

### 5b. Tests for the tests

- **systemTest changes carry unit tests where appropriate** — helpers, parsers,
  gate logic, report builders, anything with branching. A change to test
  infrastructure is production code for the purposes of coverage.
- "Where appropriate" excludes pure scenario wiring with no logic; it does not
  excuse an untested helper.
- **Every fix is proven by a test that was red on the broken code and green
  after.** No skips, no report-only, no "greener".

### 5c. No god files

Applies to files you create or edit under `systemTest/`. Not licence to refactor
untouched code. **Scope: systemTest only** — on platform-k these standards
explicitly do not govern `services/`, `frontend/`, `packages/`, or `contracts/`.

Structure by **responsibility**, and split **before** the limit, never after.

**The file cap is 400 lines, on both platforms** — counted **excluding blank lines
and comments**, i.e. the lint `max-lines` rule with `skipBlankLines: true,
skipComments: true`, which both platforms enforce through oxlint (platform-s
`systemTest/.oxlintrc.json` since PS-990; platform-k per suite since KS-1396). Docstrings and JSDoc never count against the
budget; the cap measures logic. 400 is the ceiling, not the target — split well
before it. A file you are editing that crosses 400 gets split
before the change lands. A 1,000-line file is a defect to fix, not a thing to
extend.

Companion caps:

- **Function:** target < ~20 lines. Ceiling **90** where lint sets one
  (platform-s `max-lines-per-function`, off in `*.spec.ts` where a linear test
  body may legitimately run long; platform-k `systemTest/performance` the same).
- **Complexity 10 · nesting depth 4 · params 5.**
- **Class:** ~10 methods / ~300 lines. A 900-line class is a defect. **platform-s
  POMs < 300 lines** — split a large page into `*_handler.ts` / `*_flow.ts`.

On **platform-s these are lint-enforced (oxlint): a breach fails the gate exactly like a
failing test.** On platform-k treat 400 as equally binding even where the
per-project lint config is looser.

Decompose along real seams, which differ by platform:

- **platform-k:** parsing / rendering / orchestration / config / logging (Python);
  client / fixture / helper (Playwright API suite). The named anti-pattern is
  pre-refactor `complete_report_generator.py` at 2,565 lines and `scripts/run.py`
  at 2,041 (fixed 2026-06-25).
- **platform-s:** POM (selectors + actions) / handler (sub-flows) / flow
  (multi-page journey) / interaction-util / factory (test data) / reporting.
  **Assertions never live in a POM — they live in specs.**

Both platforms:

- **Keep cohesive state together.** Split god *files* freely; split a *class* only
  along a real responsibility boundary — never shatter a class whose methods
  genuinely share instance state just to hit a line target.
- **DRY and typed.** One home per helper/constant; remove duplicates rather than
  aliasing them. Model structured data with `TypedDict`/dataclass or
  interfaces/types — no `Any`/loose-dict blobs except at genuine external/JSON
  parse boundaries, and say why.
- **Refactors are behaviour-preserving and verified.**
- Splitting a file is a structural change — flag it, do not smuggle it into an
  unrelated diff.

### 5d. References on every change

- **Every changed line carries a comment saying WHY it changed and the Linear
  ticket number** (e.g. KS-519), stating the prior behaviour so the diff explains
  itself later.
- Cite `file:line` for findings, and the ticket URL in PR summaries
  (`https://linear.app/secuura/issue/KS-NNN`).
- New finding / bug / CVE / dep-drift → add it to the matching project register
  and keep the umbrella's sequencing current. Append a comment rather than
  rewriting someone else's register. Never retitle a ticket someone else authored.

### 5e. CLAUDE.md diff audit

Walk the actual diff against this list:

- `pip3`, never `pip`.
- Python targets **3.14+**: `X | None`, `dict[K, V]`, `list[T]`, `tuple[A, B]`. No
  `Optional`, no `from __future__ import annotations`, no `typing_extensions`
  shims. Check `python3 --version` before running Python in-sandbox.
- `docker compose` (v2), never `docker-compose`.
- Language boundary: everything under `Blockchain/Dev` is TS/.mjs/JSON. Python
  belongs only to `systemTest/schemathesis`.
- UTC: `getUTCFullYear/Month/Date`, the `utcDate.ts` boundary helpers. Never
  `toLocaleDateString`/`toLocaleString` in persisted, anchored or on-chain paths.
- Zod: `.trim()` **before** `.min()`/`.max()`/`.email()`; never trim passwords,
  tokens, hashes, API keys, Base64 or free-form metadata; `.regex()` not
  `.refine()` on base string schemas.
- systemTest documentation changes go in `systemTest/CLAUDE.md`, never root.
- No `.env` / `.env.local` staged — and no secrets file read or edited at all
  (§1, Secrets).
- No branches created, no merges performed, no MD files or Linear tickets created,
  unless explicitly instructed.

### 5f. Evidence

- **A runtime-behaviour change is not done — and the ticket does not move to Done —
  on offline quality-gate green alone.** It needs a live sweep on the correct host
  (§2), against a fully torn-down and rebuilt environment (§3), with all containers
  verified up.
- **Report numbers, not adjectives:** "9 of 324 failed", not "the suite failed".
  Separate observation from inference. Suspect your own tooling before blaming
  another team's code.
- If any part was skipped, blocked or unverified, **say so explicitly and name what
  is unverified.** Do not round up to done.

### 5g. Done = tested + works + deployed

A ticket is **Done only when it is tested, it works, and it is deployed.** The rule
is dated 2026-10-12 15:26 and is applied on KS-766, KS-1006, KS-1127, KS-1252,
KS-1272, KS-1319 and KS-1330 (all 2026-10-12); it is confirmed as applying from 2026-10-19
(KS-1668). The wording in those tickets is "Done = tested + works + deployed".

- **A ticket that is not Done under this rule needs approval** before it moves to
  Done or is closed. A merged runtime fix is not Done until it is deployed (KS-1006, 2026-10-12).
- **Where the running surface is the repo itself** (tooling, a template, a test
  runner), "deployed" is read as "on `develop`" (KS-1127 and KS-1252, 2026-10-12).
- Provenance: the original message is not quoted in any ticket; the tickets above
  carry the rule. If the original wording turns up, record it here under its own
  KS number and date.

---

## 6. Tool updates — harvest the new coverage, don't just bump the number

Applies to **every** test tool: Akto, Schemathesis, Playwright, and anything added
later. A version bump is not a version bump until all three sweeps below are done.
**A tool that ships new capability and lands with none of it enabled is a
regression disguised as an upgrade.**

### 6a. New tests — find them and enable them

- After any bump, **regenerate the tool's test/check catalog and diff it against
  what is actually enabled.** New test types, templates, checks or phases are the
  point of the upgrade.
- **Enable everything applicable.** Anything left disabled needs a stated reason
  and a Linear ticket, recorded where the selection lives — never a silent
  omission.
- **Report the delta explicitly:** "N new tests available, M enabled, K deferred
  (reason + ticket)". A bump that yields zero new tests is a valid outcome — say
  so, and say how you established it.
- Then **run them** on the correct host and confirm they execute rather than
  silently no-op. A newly-enabled test that never runs is worse than one that is
  honestly disabled.

**Akto specifics** (full procedure in `systemTest/CLAUDE.md`):

- `npm run update-images` prints the latest *paired* version (it reads up to five
  pages of tags per image and warns when it stops early — KS-1609). Set
  `config.aktoImageVersion` in `systemTest/akto/package.json` (the canonical
  record) and both `docker-compose.yml` fallbacks; `AKTO_IMAGE_VERSION` in
  `systemTest/akto/.env` only if that `.env` names one (Compose `${...}`
  interpolation reads `.env`/shell, never `docker.env`'s `env_file:`). The unit
  suite names every copy left behind (`aktoPinMirrors.test.ts`,
  `aktoPinDocMirrors.test.ts`).
- **The pin is also the minimum (KS-1609):** `npm run start` refuses an
  `AKTO_IMAGE_VERSION` / `AKTO_DASHBOARD_VERSION` / `AKTO_TESTING_VERSION` below it,
  and every npm range's floor is the installed version (`dependencyFloors.test.ts`).
- Then `npm run load-templates && npm run generate-test-ids`, and commit the
  regenerated `src/core/aktoUpgradeTestIdCatalog.generated.ts` (renamed from
  `testIdCatalog.generated.ts` under KS-710). **A stale catalog now blocks
  scanning** (KS-1609): the three tiers run `check-test-ids` first and
  `npm run start` exits 1 at its end, so a template or category a new Akto adds
  cannot go unscanned.
- **Start the bump from a clean library.** `bin/load-templates.ts` reuses
  `output/tests-library` when it exists, and since PR #1559 (KS-1447) it loads only
  the ids Akto does not already hold — so a template whose id is unchanged but whose
  content changed is not reloaded. A bump must `rm -rf output/tests-library` **and**
  drop the account's `yaml_templates` collection (or use a fresh Akto volume) first —
  otherwise the "regenerated" catalog is silently the *old* library. (This used to
  cite a skip at ≥80 templates; that count guard was removed by PR #1559.)
- **Re-validate the skip-bucket classifier.** Akto's skip/error message strings
  drift between versions and `src/report/skipBuckets.ts` matches on them. Run one
  scan and confirm `otherError` is ~0. A spike means a marker regex needs updating
  (2.8.5 changed the authz marker to `MEMBER  config` with two spaces, silently
  dumping 660 authz skips into `otherError`).
- Stable tags are `X.Y.Z_local` — ignore `latest`/`local`/`a-####-merge` and the
  separate `X.Y.Z_latest` cloud line.

### 6b. New result data and output artifacts

- **Diff the raw result fields after every bump.** Tools add fields silently, and
  a report only surfaces what it explicitly parses — so a silently-added field is
  a silently-missed enrichment. For Akto: `npm run scan:result-fields` unions the
  DOC (result-level) and RES (per-attempt) field names across **all** result docs
  and diffs them against `scripts/result-fields.baseline.txt`. A `>` line is a new
  field. Decide whether it improves the report, parse it if so, then re-baseline
  with `-- --update` and commit.
- **Check for additional output artifacts the tool can now emit** — JUnit XML,
  JSON, SARIF, HAR/cassettes, coverage, structured logs. If an artifact adds
  signal a human or CI would use, **generate it**, write it to the run's results
  directory, and document it. If it adds nothing, say why you skipped it.
- Verify a newly-parsed field's **shape** before relying on it (epoch seconds vs
  ms, 0–100 int vs 0–1 float, string enum vs boolean) and record the expected
  shape alongside the baseline.

### 6c. Always improve the HTML report — make it easy for the human

**The HTML report is the deliverable a person actually reads. Any new result data
that helps them must reach it — storing it is not surfacing it.**

- New field or artifact worth having → **it appears in the HTML report**, not just
  in `results.json`. Precedent: Akto 2.9.2's `validationReason` /
  `percentageMatch` / per-attempt `confidence`, and 2.9.9's `workflowTest` /
  `executionOrder` / `nodeResultMap` surfaced as the finding card's multi-step
  **WORKFLOW STEPS** trace.
- **Write for the reader, not the parser.** Every surfaced item answers: what
  happened, why it matters, what to do next. No raw JSON blobs, no bare ids, no
  unexplained enum strings. Expand or tooltip anything a newcomer would have to
  look up.
- **Scannable first, deep on demand** — summary and counts at the top, detail
  behind expanders. The reader should get the verdict without scrolling.
- **Legends and tooltips are part of the change.** A new category, badge or column
  ships with its explanation in the same commit.
- **Parity is mandatory** — any change here obeys §5a: console, `results.json` and
  the HTML report carry the same categories, labels and counts.
- Improving the report is **in scope by default** on any tool update; it is not a
  separate ticket to defer.

### 6d. Every tool update finishes like any other change

§4 (both HTML docs updated), §5a (three-way parity), §5b (unit tests where
appropriate), §5d (why + ticket reference on each change), and §5f (live run on
the correct host, numbers not adjectives) all apply. Record the bump and the
coverage delta on the tool's Linear project register.


### 6e. Runtime versions — LTS only

**Always run, build and test on Long-Term-Support versions (Peter, 2026-10-06).** Node: an even-numbered
LTS line (24 today), never an odd-numbered "Current" release. Java: the latest LTS JDK. Ubuntu: an LTS
release. Docker base images: pin an LTS tag (`node:24-alpine`). Anything else: its own vendor's
long-term/stable line.

- **Python has no LTS programme** — the rule is the newest patch release of the supported minor. The
  harness pins that as a floor (`systemTest/schemathesis/scripts/python_pin.py`, `REQUIRED_PYTHON`,
  currently 3.14.8) and refuses an older interpreter with an actionable message. That is the documented
  exception, not a second rule.
- **Verify LTS status when you bump** — from the vendor's schedule, not memory. A tool that forces a
  non-LTS runtime is a time-boxed bridge with a ticket (precedent: KS-422), never a quiet default.
- **A tool's own requirement picks the line; LTS picks within it (Peter, KS-1615, 2026-10-15).** When a
  tool ships a supporting runtime, take the line the TOOL's own source specifies, then the newest patch
  on that line — provided the vendor still supports it. Akto is the worked case: Akto v2.38.5's own
  `docker-compose.yml` pins `mongo:7.0.x` (still so at v2.41.6, KS-1608, 2026-10-27, and at v2.42.6, KS-1609, 2026-10-30), so the harness runs the newest 7.0 patch (7.0.45), not the
  newest MongoDB major (9.0, which Akto does not ship) and not the 6.0 line it used to ship (EOL
  2025-07-31). **When the tool or the vendor says move to another version, move — and update
  `systemTest/CLAUDE.md` and this skill in the same change.** A line the tool needs but the vendor no
  longer supports is a time-boxed bridge with a ticket, as above.
- **It changes no test and no result.** Quote every measurement as taken on LTS versions; if one was
  not, say so in the Test Evidence block rather than letting the number imply it.
