# DECISIONS-24 — Wednesday's proposed rulings on the 24 engineering NEEDS-KAM tickets (2026-10-05)

Written 2026-10-05 20:01 AEDT (`date`) by a drafting sub-agent for Wednesday, under Kam's 19:52 ruling (card
`secuura-tooling-32-decision-tickets-1005` = a): *"Wednesday decides the 24 engineering ones and queues them; the 8 stay with you."*
The eight Kam keeps (KS-884, 925, 939, 940, 1085, 1138, 1148, 1250) are not touched here.
Nothing was written to `!CODING`, Linear or GitHub.

**Instruments (each line below names the one it used):**
- **[L]** Linear GraphQL, read-only, `issue(id:"KS-NNNN")` with description + every comment (first:100) + relations, run 20:0x AEDT.
  Raw dumps: `scratchpad/dec24/KS-NNNN.md`. All 24 returned an open state (Backlog 16, In Progress 8). **None is closed, so none is skipped.**
- **[G]** `git show f01c1da5717f:<path> | sed -n a,b` in the Secuura checkout (READ-ONLY). Develop was confirmed with
  `git ls-remote origin refs/heads/develop` using the repo's own `core.sshCommand`, which returned `f01c1da5717fdcb80a5e1aeeaa8ff9f0f00edd80`.
  (Local `develop` is stale at `c56dd7c32`; every read below is at `f01c1da57`.)
- **[GG]** `git grep -n` at `f01c1da5717f`. **[GL]** `git log --oneline f01c1da5717f --grep/-S`. **[GA]** `git merge-base --is-ancestor <sha> f01c1da5717f`.
- GitHub PR states (#1245, #1250, #1278) were **not** read, because gh was out of scope. They are quoted from the Linear comments that record them.

---

## BLUF

| class | n | tickets |
|---|---|---|
| **DECIDE-NOW** | **19** | 785, 846, 955, 956, 964, 1000, 1033, 1036, 1051, 1081, 1088, 1141, 1290 (items 1-2), 1305, 1313, 1314, 1317, 1324, 1326 |
| **ALREADY-SETTLED** | **3** | 837 (Wednesday's own DO-NOT-BUILD ruling), 1010 (the open question is answered in code at `proxy.ts:884-891`), 1351 (items 1-2 merged, item 3 is KS-1000's class) |
| **ACTUALLY-KAM'S** | **2** | 1146 (a preflight leg = push-gate wiring), 1188 (F3 = the user-facing login response; F1/F2 already merged) |
| **NEEDS-MEASUREMENT** | **0** | none needs a run before the decision. Several builds carry a measurement step, listed below. |
| **total** | **24** | |

**Build tickets after merging.** The 19 decide-nows plus 1010 come to **17 build or board items**. KS-1313 and KS-1326 merge into one build, and KS-846 and KS-1317 into one docs PR. KS-1324 becomes a constraint inside the L1 lane, and KS-956 becomes a close-with-record.

**Spark-sized: 4 builds covering 5 tickets.**
- KS-1305: the diagnostic in `getPrismaClient`.
- KS-1313 + KS-1326: the child-verdict reader.
- KS-1141 site 1: a docblock sentence.
- KS-1088: this one only after lane L1 lands, because it edits L1's file.

Every other build fails the predicate. Each entry names the clause it fails.

**Carded to Kam out of this set.** Each card is a single sentence. None blocks a build.
1. KS-1146: whether to add the leg (Wednesday recommends no).
2. KS-1188 F3: the wording or ordering on the post-burn 503.
3. KS-1290 DoD item 3: the push-gate leg itself.
4. KS-1033: wiring the now-fixed guard 1 into the gate.
5. Disposal of capped PRs #1245 and #1278. Both are open at the cap, and "disposition sits with the repository owner".

**Wrongly in the 24.**
- **KS-1146** belongs with the eight: its whole ask is a push-gate leg.
- **KS-1188** is a product decision on the auth login path, not tooling.
- **KS-837** and **KS-1351** are already ruled or merged.
- **KS-964**'s premise is mis-measured. The real flat population is **31**, not 104. The 104 is a recursive pathspec count that includes 72 specs already inside runner paths. See its entry.

**UNMEASURED (stated, not assumed):**
1. Whether the originate, referral, staking and vc-issuer jest suites are green at `f01c1da57`. No jest run (KS-1051).
2. Today's review-stream parent coverage. No Linear count was run, and the last count is 2026-09-16 (KS-1036).
3. The `tsc`-with-tests error counts for any service at `f01c1da57`. The 25 for auth is from `133f525c8` (KS-1000).
4. The red set and walk cost of adding `connectors` to the ks727 walk (KS-1141 site 2).
5. A working `prisma generate` invocation from a dev worktree (KS-1305).
6. Whether vitest 4.1.11's `--outputFile.json` gives the counts the KS-1313/1326 build needs. This is the proposed shape, but it has not been run.
7. Whether any person runs the 31 flat specs by hand. This cannot be measured from the tree, though `tests/README.md:59` documents one manual run (KS-964).
8. Whether `start-environment.sh` runs anywhere but a laptop. The checker's own comment says no; it was not re-verified (KS-785).

---

## KS-785 — Compose resolves the SHELL over .env while the checker resolves .env over the shell — a green credential check over a stack running the shared literal

**Question** [L]: *"Two candidate shapes, neither chosen here: (a) have `start-environment.sh` source `.env` on the same path … or (b) have the checker 'be the consumer' for real: read the values the way compose does (shell first, `.env` second)."*

**Options:** (a) source `.env` in `start-environment.sh`; (b) the checker resolves shell-over-`.env`, as compose does; (c) leave it as is. The checker comment already retracts the false claim.

**PROPOSED: (b).**
- Option (b) changes only what the checker *reports*. It does not change what compose runs, so it is the reversible, no-behaviour-change choice.
- The checker is non-blocking by Kam's KS-762 ruling. `start-environment.sh:85-91` calls it under `if !` and continues [G]. A truer checker therefore cannot stop anyone's stack. It can only stop the false green.
- Option (a) changes the start path's runtime environment, which is the very path QA FR-1 named. It would also make `start-environment.sh` execute `.env` a second time.
- The checker's own comment already records the defect and points here (`check-slot-credentials.sh:102-112`, "Tracked as KS-785 — do not re-add the claim") [G].
- The blast radius is bounded by the same comment's census: developer-facing only, no workflow invokes it, and the demo VM uses neither script (`:118-125`) [G; not re-verified, see UNMEASURED 8].

**Class:** DECIDE-NOW. This is an engineering choice inside dev-laptop tooling. No production or demo path is touched.

**What it becomes:**
- One PR on `scripts/check-slot-credentials.sh`. For each checked key, an inherited non-empty shell value wins over the sourced file, matching compose. The output names which source won.
- Cells go in `scripts/__tests__/check_slot_credentials.test.sh`, using the ticket's three-way sentinel (fixture / ambient sentinel / compose default) and the no-ambient control.
- Tier guess: tier-1 (credential surface).

**Spark fit:** no. The file is a credential checker, which falls under the predicate's credential exclusion.

## KS-837 — Published prose drifts from the routes it describes and nothing detects it

**Question** [L]: three lines (1: a contract-source phrase check, sized at about half a day; 2: a repo-wide marker convention, unsized; 5: the ~306 unswept descriptions, unsized). The ticket says *"this ticket is the record, not a commission."*

**Options:** build line 1 now; re-price; keep as a record.

**PROPOSED: keep it as the record. No build.** The description carries *"Wednesday priced line 1 and ruled DO NOT BUILD IT NOW (2026-09-05T15:44:16Z) … Anyone picking it up should re-price"* [L]. Nothing since has changed that ruling. The only comment (2026-09-05T22:07Z) adds a design constraint: anchor on the claim plus its condition, never on a fragment. It does not ask for a build [L].

**Class:** ALREADY-SETTLED, by Wednesday's 2026-09-05T15:44:16Z ruling quoted in the description.

**What it becomes:** it stays in Backlog as a record. Do not close it: closing would bury the N3 design constraint. No build ticket.

**Spark fit:** no. Nothing is to be built.

## KS-846 — `@secuura/shared` `main` points at an untracked, never-built `dist/index.js`

**Question** [L]: *"Fix shapes (not chosen — whoever picks this up should): Add a `prepare` script … point `main` at `src/index.ts` … declare `exports` with a source condition."*

**Options:** (1) a `prepare` script; (2) `main` points at `src`; (3) a source export condition; (4, missing from the ticket) change nothing in the manifest and document the build step.

**PROPOSED: (4).**
- **(1) is inert by design:** `Blockchain/Dev/.npmrc:15` sets `ignore-scripts=true`, so `prepare` never runs on install [GG].
- **(2) breaks the images.** Every service Dockerfile builds `dist/` explicitly and runs from it: `services/auth/Dockerfile:8-13` runs `npm ci --ignore-scripts` then `npm run build`, and links `/shared` at `:30` [G].
- **(3) widens every consumer's resolution** for a Low-priority trap the ticket itself calls "not a defect".
- The `exports` map at `packages/shared/package.json:118+` points every subpath at `dist/` [G], so the images depend on it.
- (4) is reversible and touches no build.

**Class:** DECIDE-NOW.

**What it becomes:** one docs PR, shared with KS-1317. In `Blockchain/Dev/CONTRIBUTING.md`, directly after the `npm ci` at `:23` [GG], add:
- "then `npm run build -w @secuura/shared` — `dist/` is untracked and `.npmrc` disables install scripts, so nothing builds it for you";
- KS-1317's root-install line.

Tier guess: tier-3 docs.

**Spark fit:** no. It is a docs edit, with no runnable test near it.

## KS-955 — A fresh clone cannot run the four platform suites, and fails in a way that reads like a product regression

**Question** [L]: *"Fix shapes (not chosen): persona-login precondition … Reconcile `.env.example` with the compose default, or make bootstrap-env leave the variable unset … a documented reset for the lockout."* Peter's 2026-09-10 comment: *"'assert the persona can log in as a precondition and fail with that message' would have saved ~40 minutes."*

**Options:** (1) a persona-login precondition; (2) reconcile the seed default; (3) document a lockout reset.

**PROPOSED: (1) + (3). Explicitly not (2).**
- **(2) is overtaken.** Compose no longer defaults seeding on. `docker-compose.yml:625` and `:781` read `ALLOW_DEFAULT_SEED_PASSWORDS=${ALLOW_DEFAULT_SEED_PASSWORDS:-}` [GG]. That is default-DENY, landed in KS-949 `8a519e63a` [GL]. Reopening it would reverse a credential ruling.
- Bootstrap now reads `env.example` first (`scripts/bootstrap-env.sh:36-39`) [G], which carries no `ALLOW_DEFAULT_SEED_PASSWORDS` at all [GG count 0]. The ticket's step 1 has therefore moved, but fresh clones still do not seed.
- What remains is the diagnosis cost. A precondition turns "100% error rate" into a sentence that names the cause, at zero product risk.
- Fold in the health-probe fix: `systemTest/CLAUDE.md:1675` still documents `GET /api/health → 200` [GG]. The gateway answers `/health` (`nginx-*.conf location = /health`) [GG], and both the ticket and Peter measured `/api/health → 404` [L].

**Class:** DECIDE-NOW. It is test-harness tooling, and the seed default stays as KS-949 left it.

**What it becomes:**
- One PR. Each suite's pre-run step logs in its persona once and, on 401/429, exits with a message. The message names `ALLOW_DEFAULT_SEED_PASSWORDS`/`ADMIN_USER_PASSWORD`, the lockout, and `docker restart secuura-auth`.
- The same PR fixes the `/api/health` row in `systemTest/CLAUDE.md:1675`.
- Files: the four suites' setup modules under `systemTest/` (k6, Schemathesis, Playwright, Akto) plus `systemTest/CLAUDE.md`.
- Tier guess: tier-2.
- Interlocks with KS-969 (In Review) for the super_admin persona [L relations].

**Spark fit:** no. It spans four suites' setup files and needs a live stack.

## KS-956 — KS-930 residue: a whole app tree copied into a stage that names no JS runtime is still exempt

**Question** [L]: *"The only escapes are (a) exempting `/shared` by name … or (b) accepting that the arm can essentially never grant an exemption in this repo, which removes the arm. Both are decisions, not cleanups."*

**Options:** (a) a by-name allow-list for `/shared`; (b) remove the exemption arm; (c, missing from the ticket) accept the residue as pinned-known-open.

**PROPOSED: (c).**
- **The hole is latent.** There are **0** `COPY --from=X /app /app` lines in any Dockerfile at develop, against **46** `COPY --from=shared-builder /shared /shared` as a control [GG count].
- **It is pinned out loud.** `scripts/__tests__/check_shared_relink.test.sh:961` asserts the exempt behaviour under the name "KNOWN OPEN … (KS-956)", and `:932-960` carry the measured reasoning [G]. If behaviour changes, a cell reds.
- **The other options cost more.** (a) re-introduces the deny-list-with-a-comment shape the round removed. (b) removes nginx's exemption, which is the case the arm exists for (the 41/12 red run, per the ticket) [L].
- **The genuine remaining hole is unfixable by any Dockerfile parser.** That hole is `CMD ["/app/start.sh"]`, per the ticket and Kam's round-3 record [L].
- (c) changes nothing and stays reversible.

**Class:** DECIDE-NOW.

**What it becomes:** close as accepted residue, with a Linear comment citing the 0/46 census and the `:961` pin. The pin cell keeps the ticket id, so the record survives. No build.

**Spark fit:** no. Nothing is to be built.

## KS-964 — 104 flat spec files in Blockchain/Dev/tests are in no runner's path — quarantine and find out, do not delete

**Question** [L]: *"1. Is anything running these … 2. If not: quarantine, then remove after a quiet period. 3. If some are live, they move under a config's `testDir`."*

**Options:** quarantine (move); move live ones under a `testDir`; leave as is.

**PROPOSED: quarantine the 31 truly flat specs by `git mv` into `tests/_quarantine-ks964/`. Never delete.**

**The ticket's 104 is wrong.**
- At develop, `git ls-tree` of `Blockchain/Dev/tests/` holds **31** top-level `*.spec.ts` files [G].
- The 104 reproduces only as a *recursive* count: `git ls-files -- 'tests/*.spec.ts'` gives 104, because git pathspec `*` crosses `/`.
- By directory, those 104 are e2e 48, e2e-v2 24, helpers 1 and flat 31 [G, `ls-tree -r | awk`]. So 72 of the 104 already sit in runner paths.

**Q1 is partly answered: three of the 31 are named elsewhere** [GG for each basename, excluding the file itself]:
1. `tests/README.md:17,59` documents `npx playwright test tests/manual-issuer-portal-test.spec.ts`. That is a documented manual habit.
2. `CLI-AGENT-INSTRUCTIONS.md:282` names `issuer-portal-full.spec.ts`.
3. `packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts:276` uses `tests/admin-crud-test-robust.spec.ts` as its "tests/ is walked" control.

So a move must update those three references in the same PR, or the ks879 guard reds. A move is reversible with `git mv` back; this is the ticket's own "see who shouts".

**Class:** DECIDE-NOW.

**What it becomes:**
- One PR covering 31 `git mv`s, a quarantine `README.md` (naming KS-964 and a review date one sprint out), and the three reference updates (ks879 control path, `tests/README.md`, `CLI-AGENT-INSTRUCTIONS.md`).
- Correct the 104 → 31 on the ticket.
- Tier guess: tier-2.
- The mislabelled-branch loop (comments 2026-09-07 and 2026-09-08) is a GitHub branch deletion, which is not ours. Leave it noted.

**Spark fit:** no. It moves 31 files plus a guard-test edit, so it is not one product file.

## KS-1000 — services/auth tsconfig EXCLUDES src/__tests__ — every 'tsc: 0 errors' on a test-only change is a green that could not fail

**Question** [L]: *"1. Decide the shape. Either include `src/__tests__` in the type-check (a second `tsconfig.test.json` is the usual answer …), or state in writing that tests are deliberately unchecked and stop citing `tsc` as evidence for them."*

**Options:** (a) a per-service `tsconfig.test.json` (KS-933 also offered `vitest --typecheck` for vitest packages); (b) declare tests unchecked in writing.

**PROPOSED: (a), as an *additive, non-gating* `typecheck:tests` script per service, starting with `services/auth`. Leave `build` untouched.**
- The exclusion is live: `services/auth/tsconfig.json:19` reads `"exclude": ["node_modules", "dist", "src/__tests__"]` [G].
- It is the class, not one service: all 26 `services/*/tsconfig.json` and `packages/*/tsconfig.json` mention `__tests__` [GG count per file, 26 of 26; auth's line read at `:19`].
- Adding a second config changes no build and no image, so it is reversible.
- Declaring tests unchecked (b) would make the false "tsc 0" evidence line permanent policy.
- The 25 pre-existing auth errors (comment 2026-09-08, at `133f525c8`) [L] mean it cannot gate on day one. The first PR reports and pins; it does not block.

**Class:** DECIDE-NOW. It is a type-check instrument inside our tooling and gates nothing.

**What it becomes:**
- PR 1 (auth):
  - `services/auth/tsconfig.test.json`, which extends the base with the exclusion removed;
  - `"typecheck:tests"` in `services/auth/package.json` (a script line only, no dependency or lock change);
  - a planted-error cell with the `--listFiles | grep -c src/__tests__` control (DoD item 4);
  - a DEV-PROCESS Test Evidence line saying which `tsc` covered tests.
- Later PRs: one per service family.
- Tier guess: tier-2.
- KS-1351 item 3 (vc-issuer) folds here.

**Spark fit:** no. It touches `package.json`, it is a class across 26 configs, and its 25 pre-existing errors need judgement.

## KS-1010 — e2e: "CIP-30 API availability check" calls a route that does not exist, and its assertion passes on the 404

**Question** [L]: *"OPEN QUESTION — do not change any route until this is answered … 1. The path is a typo … 2. The route was planned and never built — `/api/wallet/status` and `/api/wallet/supported` were meant to be a `wallet-connector` service surface."*

**Options:** (1) repoint to the auth fixture `walletStatus()`; (2) `test.fixme()` as unbuilt; (3, missing from the ticket) repoint to the wallet-connector's real surface.

**PROPOSED: (3).** The open question is answered in code.
- `services/api-gateway/src/routes/proxy.ts:884-891` says *"KS-10: removed the dead `/api/wallet` (singular) mount. The wallet-connector only ever served `/api/wallets/*`; the singular prefix forwarded 1:1 and always 404'd … nothing real calls it."* [G]
- **Reading 2 is refuted.** The connector was built, under the plural prefix. It serves `GET /api/wallets/available` (`services/wallet-connector/src/server.ts:104-122`), which returns `cardano[]` with `nami`/`eternl`, behind `jwtAuthenticate` at `:101` [G].
- The gateway mounts `/api/wallets` with `authenticateToken(true)` at `proxy.ts:879-882` [G].
- The two tests at `tests/e2e/tests/recruitment/happy-path-wallet.spec.ts:253-275` hit the dead singular prefix. The second also expects a `wallets[].id` shape that no route returns [G].
- **No route changes,** so the ticket's caution holds.

**Class:** ALREADY-SETTLED, by the KS-10 comment at `proxy.ts:884-891`. A test build remains.

**What it becomes:**
- One PR on that spec file. Point both tests at `GET /api/wallets/available` with the holder token. Assert `200`, and that `cardano` contains `eternl` and `nami`. Drop the `< 500` and `if (response.ok())` guards on these two.
- The family sweep (13 `< 500`, 33 `if ok()`) stays out of scope.
- Tier guess: tier-2.
- Needs a live stack to verify.

**Spark fit:** no. Playwright needs a live stack, so there is no in-process runnable test.

## KS-1033 — KS-926 residue: the three guards that could NOT be wired

**Question** [L], guard 2: *"Fix: one of — correct the message to match the default, or make the default `warn` and the message true. Deciding which is the point."* Guard 3: *"Its home is stack start-up."* Comment 2026-09-25: the stale reason string in `run-code-guards.sh:116`.

**State at develop:**
- **Guard 1 is fixed.** `check-no-demo-mutation.sh:62` reads `BASE="origin/develop"` [G], from #1185 and #1209 [L]. It is still in the `DEFERRED` bucket at `run-code-guards.sh:116` with the stale "defaults to BASE=origin/main (line 58)" reason [G].
- **Guard 2 is unchanged.** `check-no-trust-header-reads.sh:48` reads `level="${TRUST_HEADER_LINT_MODE:-fail}"`, while `:60` still says "Set TRUST_HEADER_LINT_MODE=fail to switch this from warn" [G].
- **Guard 3 is unchanged** at `run-code-guards.sh:118` [G].

**PROPOSED:**
- **Guard 2: correct the message and keep `fail`.** The guard enforces pen-test F-04. Making it `warn` would weaken a security lint to make a sentence true. Keeping `fail` freezes nothing, because the guard is unwired (DEFERRED at `:115`). Whether to wire it warn-first is gate wiring, which belongs to Kam.
- **Guard 3:** stays DEFERRED. It gets homed at stack start-up later.
- **The `:116` reason string:** rewrite it now to "base fixed to origin/develop (#1185, #1209); wiring awaits a gate decision". The array's reasons are live bash (`:108-113`), so the new text needs no `$`, no backtick and no inner quote.

**Class:** DECIDE-NOW for the message and the reason string. Moving guard 1 from DEFERRED into the wired set changes the push gate, so it becomes a Kam card.

**What it becomes:** one PR covering `scripts/check-no-trust-header-reads.sh:57-61` (the message only) and `scripts/run-code-guards.sh:116` (the reason string only). The census cell for leg 15 must stay green. Tier guess: tier-2.

**Spark fit:** no. It touches two files, one of them a pen-test F-04 security guard (security exclusion), the other the gate's own guard runner.

## KS-1036 — The review-stream overlay covers 57 of 114 active tickets, and DEV-PROCESS still says 'nothing left over'

**Question** [L], remaining checklist: *"Parent the 22 PR-bearing tickets … Sweep the remaining unparented … Rename KS-485 so all four parents are findable by title, or name all four explicitly in the doc … Decide where the check lives."*

**State:** item 3 is done. `docs/DEV-PROCESS.md:233-239` now says the counts decayed, and gives the query instead of a number. This landed in #1136 `f37214951` [G, GL].

**PROPOSED:**
- **Do not rename KS-485.** The doc's table at `DEV-PROCESS.md:223-228` already names all four parents with links [G], which is the ticket's own alternative.
- **Parent the active unparented tickets per the existing rule** ("Every new K-side ticket that reaches Todo is parented into one of the four", `:230-231`) [G]. This executes a Kam-adopted rule; it makes no new one.
- **The check lives in Wednesday's board-disposition pass** as a read-only Linear query (unparented started/unstarted KS tickets), not in the repo. A repo gate cannot read Linear.

**Class:** DECIDE-NOW. These are board-hygiene writes under an adopted rule, with no repo or gate change.

**What it becomes:** a board task, not a PR. Run the count (UNMEASURED 2), parent each ticket in one Linear batch, and add the query line to the disposition checklist. Close KS-1036 after that. Tier: board.

**Spark fit:** no. These are Linear writes, not a product file.

## KS-1051 — develop is RED on the services/originate jest suite and NOTHING catches it

**Question** [L]: *"Kam or Wednesday to pick a fix shape (or rule that the red simply waits for #926 and no instrument changes)."* Shapes: (1) a preflight leg; (2) a periodic mainline run; (3) a baseline-diff rule in Test Evidence.

**State:** the red itself is fixed. #926 merged as `b1cb8466f` (KS-927) [GL]. The gap remains: the 15 preflight `step` legs (`preflight.sh:219-649`) include no service unit suite [GG].

**PROPOSED: (3) now.**
- The ticket calls it "probably the cheapest".
- It is docs-only and reversible.
- It mirrors the Schemathesis rule already at `DEV-PROCESS.md:42,114` [G].
- Concretely, `DEV-PROCESS.md:46` `**Unit suites (touched services):**` gains: "plus develop's own result for each suite run, so a pre-existing red is visibly pre-existing".

Shape (1) is a push-gate change, so it sits with Kam via KS-1146. Shape (2) needs a host scheduler we do not have.

**Class:** DECIDE-NOW for (3). (1) is carded with KS-1146.

**What it becomes:** one docs PR on `docs/DEV-PROCESS.md:46` (Test Evidence template) and its explanatory paragraph. Tier-3. Whether the four suites are green today is UNMEASURED 1, and the first PR using the new line will measure it.

**Spark fit:** no. It is a docs edit with no runnable test.

## KS-1081 — CONFIG DRIFT: two tracked env templates disagree by ~39 vars

**Question** [L], remaining: *"The reconciliation, and the single-source decision alongside KS-1077, are untouched."* Peter, 2026-09-28: `env.example` is missing `ADMIN_USER_PASSWORD`, `ENABLE_DEMO_SEED`, `ALLOW_DEFAULT_SEED_PASSWORDS`, `TSA_URL`, `TSA_AUTH_KEY`. He suggests adding each "with a comment and a safe local default (blank for the secret)".

**PROPOSED:**
- **`env.example` is the single source.** That is already Kam's 2026-09-16 option (a), recorded at `scripts/bootstrap-env.sh:26-35` [G].
- **Port the five keys into `env.example` with exactly the values `.env.example` holds** [G], all fail-closed:
  - `ENABLE_DEMO_SEED=false` (`:104`)
  - `ALLOW_DEFAULT_SEED_PASSWORDS=false` (`:109`)
  - `ADMIN_USER_PASSWORD=` (`:133`)
  - `TSA_URL=` (`:162`)
  - `TSA_AUTH_KEY=` (`:163`)
- Those values equal compose's own unset behaviour (`docker-compose.yml:618,625,781,1244-1245`, all `:-` empty) [GG]. Per the compose comment at `:800-806`, unset and empty behave the same.
- **This changes no stack's runtime behaviour.** It only makes the gates visible to whoever copies the template.
- **Then port every other `.env.example`-only key the same way.** The counts are 103 vs 65 `^[A-Z]…=` lines [GG count].
- **Mark `.env.example` legacy in a header and do not delete it.** Bootstrap keeps it as the named fallback at `:38`, and two scratch-clone tests rely on that (`:31-35`) [G].

**Class:** DECIDE-NOW. The single-source choice is Kam's already-made option (a). This is the reconciliation it implies.

**What it becomes:** one PR covering `Blockchain/Dev/env.example` (key ports with comments) and a `.env.example` legacy header. Run `bootstrap_env_slot_ports.test.sh` and `verify-slot-credential-isolation.sh` green. Tier-2.

**Spark fit:** no. These are seed and credential gates, which fall under the credential exclusion.

## KS-1088 — run-shell-suites.sh restores git discovery but does not isolate suites

**Question** [L]: *"Decide whether the runner should enforce isolation, or whether the fixture convention is enough."* Shapes: a fresh-temp-dir cwd per suite, or snapshot the repo's config/refs/HEADs around the loop and fail loudly.

**PROPOSED: the snapshot-and-fail shape, built once with KS-948's left-nothing-behind check.**
- The ticket itself says the overlap means "one change could close both" [L].
- It leaves every suite's cwd as is, so no existing suite can break.
- A fresh-temp-dir cwd would change the start directory of all 18 suites, which widens scope.
- There is no live defect. The ticket measured all 18 suites as isolated [L].

**Class:** DECIDE-NOW.

**What it becomes:** one PR on `scripts/run-shell-suites.sh` plus a cell in `scripts/__tests__/run_shell_suites.test.sh` (a planted `git config` write must red the run), together with KS-948. **Sequence it after lane L1** (KS-1330 → 1331 → 1325 own this file, per SCREEN.md). Tier-2.

**Spark fit:** yes, after L1 lands. It is one product file, the snapshot fix is spelled out, a shell suite runs in-process beside it, and it is not security. Not before L1, which holds the file.

## KS-1141 — QUESTION: are crypto-agility SCAN_DIRS and ks727 SCAN_ROOTS (both ['services','packages']) the INTENDED scopes?

**Question** [L]: *"For each site: (a) scope INTENDED — add one sentence to the docblock naming the excluded trees and why; or (b) widen."*

**PROPOSED: site 1 gets (a); site 2 gets (b), narrowly, adding `connectors`.**
- **Site 1:** `packages/shared/src/__tests__/crypto-agility.guard.test.ts:44` [G]. The registry is server-side (`:5-7`). A grep for `algorithms?: [RS|HS|ES|PS…` outside `services/` and `packages/` returns **0** at develop [GG]. Scope is intended, so add the sentence.
- **Site 2:** `ks727-errorhandler-class-guard.test.ts:150` [G]. Express apps outside `services/` and `packages/` exist only in `connectors/` (2 files: `connectors/whatsapp-bot/src/index.ts` and `webhook.ts`), plus a `docs/` example and one root script [GG over `from 'express'`]. `frontend/` holds none.
  - The guard's own docblock (`:149`) says it walks "trees that hold first-party runtime source", and the whatsapp-bot connector is exactly that (it ships a Dockerfile).
  - So `connectors` is a blind spot and `frontend`/`tests` are not.

**Class:** DECIDE-NOW.

**What it becomes:** two PRs.
- **Site 1:** a docblock sentence. Tier-3.
- **Site 2:** add `'connectors'` to `SCAN_ROOTS` and a docblock line excluding `frontend` and `tests` with the reason. The builder first measures the red set and walk cost (UNMEASURED 4). If it is red, the finding goes on its own ticket. Tier-2.

**Spark fit:**
- **Site 1: yes.** One test file, a comment-only edit, and the vitest suite runs in-process. It is not security.
- **Site 2: no.** It carries a measurement and possibly a finding to triage.

## KS-1146 — The push preflight has no `services/auth` unit-suite leg

**Question** [L]: *"Decide whether a service unit-suite leg belongs in the preflight (auth first …), or whether the merge gate stays the only instrument."*

**Options:** add a preflight leg; keep the merge gate as the only instrument plus KS-1051's baseline line.

**Recommendation to Kam (not decided here): no leg now.** The preflight already costs minutes per push (KS-1135 and KS-1127, per the ticket). KS-1051 shape (3) gives the evidence half at zero gate cost. The cross-service reader (`ks949-…:376-382`, reading `api-gateway/src/startup-migrations.ts`) is better caught by the touched-service rule naming the reader's service.

**Class: ACTUALLY-KAM'S.** The question is wholly whether to add a leg to `scripts/preflight/preflight.sh`, which `.githooks/pre-push` runs. That is push-gate wiring, the subject Kam kept with KS-884. KS-1290 says the same of its own leg: *"This is a gate change, so it is Kam's call."* [L]

**What it becomes:** a Kam card. If he says no, close with a cite to KS-1051's line. If he says yes, the build is one leg in `preflight.sh` plus a census cell, tier-1.

**Spark fit:** no. It is gate wiring.

## KS-1188 — #1013 gate findings (KS-999): the getUserById route-level 503 and its log line are unpinned; a burnt backup code is told to retry

**Question** [L]: F1 and F2 are test pins. *"F3 is a product decision about the order of the burn versus the wording of the 503."*

**State:** F1 and F2 are merged.
- #1163 `5548d26af` ("F1a+F1b+F2") and #1178 `a5ead4d86` [GL].
- Four `ks1188-*.test.ts` cells exist under `services/auth/src/__tests__/` [G ls-tree].

F3 is live:
- `services/passwordLoginGate.ts:267` burns via `updateUserOrThrow` [GG].
- The hedged wording ("Please retry — if you already succeeded, you may not need to.") exists at `repositories/userRepo.ts:973`, but the read-back path's 503 does not use it [GG; L].

**Recommendation to Kam:** reuse the hedged `userRepo.ts:973` wording on the post-burn read-back 503. It is the smallest, reversible change and alters no ordering. A reorder of the burn would change auth semantics.

**Class: ACTUALLY-KAM'S.** F3 changes the response text a real user sees on a failed sign-in, on the auth login path. That is a client-facing contract, and the ticket itself calls it "a product decision". It is not tooling.

**What it becomes:** a Kam card for F3. After his answer, one PR on `services/auth/src/services/passwordLoginGate.ts` (or the classifier site) plus one cell, tier-1. F1 and F2: settled by #1163 and #1178.

**Spark fit:** no. It is the auth surface.

## KS-1290 — Lockfile edits move platform discriminators silently

**Question** [L], Done when: *"`docs/DEV-PROCESS.md` carries both traps and names the two scripts … the two scripts live somewhere durable in the repo … the push-gate leg is decided by Kam."*

**PROPOSED:** do items 1 and 2 now.
- The traps are measured in the ticket.
- The two scripts (`lockresolve21.sh`, `splice_lock21.py`) are proven on KS-530 and KS-528 with added 0 / removed 0 and identical `libc`/`os`/`cpu`/`devOptional` counts [L].
- Moving them from a seat folder into the repo, unwired, changes no gate.
- `DEV-PROCESS.md` has no hit for `lockresolve`, `TRAP` or `workspace member` [SCREEN.md row].

Item 3 stays Kam's, as the ticket says.

**Class:** DECIDE-NOW for items 1-2. Item 3 is ACTUALLY-KAM'S by the ticket's own words and is carded.

**What it becomes:** one PR:
- `scripts/lockfile/lockresolve.sh` and `scripts/lockfile/splice_lock.py`, copied from `5_Project_History/2026-09-25_seatB-25th/raise/`;
- a self-test cell each, under `scripts/__tests__/`, registered with the shell-suite runner;
- a `DEV-PROCESS.md` section on the two traps.

Tier-2.

**Spark fit:** no. It adds new scripts plus docs, so it is multi-file. The lockfile surface also needs judgement.

## KS-1305 — No fresh worktree can run a withTenant integration cell in single-tenant mode

**Question** [L]: *"Fix shapes, not chosen here: 1. declare `@prisma/client` at the root, or set an explicit generator `output`. 2. Add a discoverable `generate` script. 3. Regardless of 1/2: make `getPrismaClient()` fail with a sentence naming the cause and the command."*

**PROPOSED: (3) now. Defer (1) and (2).**
- `getPrismaClient` is at `services/originate/src/db.ts:113-128`: a bare `require('@prisma/client')` with no diagnostic [G].
- (2) already half-exists. `services/originate/package.json:13` has `"generate": "prisma generate"` [G], but the only schema is `Blockchain/Dev/prisma/schema.prisma` [G ls-tree].
- The image works by copying `prisma/` beside the package and generating there (`services/originate/Dockerfile:34-38`; `.prisma` restored at `:86`) [G]. Shapes (1) and (2) therefore touch root `package.json`/lock or the schema generator, both with Docker consequences and both in KS-1290's trap territory.
- (3) is one file, behaviour-identical on success, and turns a misleading `MODULE_NOT_FOUND` into a diagnosis.

**Class:** DECIDE-NOW.

**What it becomes:**
- One PR. In `services/originate/src/db.ts`, wrap the `require` and rethrow on `MODULE_NOT_FOUND` naming `.prisma/client`. The message names the cause (`npm ci` runs with ignore-scripts, so no generate) and the working command.
- The builder measures the working command first (UNMEASURED 5).
- A jest cell mocks the module and asserts the message.
- Tier-2.

**Spark fit:** yes. One product file, a spelled-out fix, and originate's jest runs in-process. It is not auth, credential or security; it changes only the error path's message. Caveat: Spark needs the measured command handed to it in the brief.

## KS-1313 — KS-1226 residue: readSuiteCounts is null on real fail-only, skip-only and todo-only lines

**Question** [L]: the fix shape is in the description. The last comment (2026-09-26T02:41Z) says *"#1245 round 3 is NO GO at the cap … its disposition sits with the repository owner."*

**State at develop:** `readSuiteCounts` has 0 hits [GG]. `childSuiteCounts` at `systemTest/performance/tests/unit/utils/unitSuiteSlotIndependence.test.ts:89-106` still:
- joins stdout and stderr (`:100`);
- takes the *first* match of `/Tests\s+(?:(\d+) failed \| )?(\d+) passed \((\d+)\)/` (`:101`);
- never checks spawn status or signal [G].

**Options:**
1. Re-attempt human-output parsing from round 2's anchor plus an `Errors`-line allowance.
2. Use vitest's JSON reporter written to a file.
3. Wait on #1245.

**PROPOSED: (2) on a fresh branch from develop, merged with KS-1326.**
- Run the child with `--reporter=default --reporter=json --outputFile.json=<tmp>`.
- Read `numPassedTests`/`numFailedTests` from that file.
- Refuse first when `result.error`, `result.signal` or `status ∉ {0,1}` is set.

Why this shape:
- Three capped rounds show that parsing human output is an open-ended shape hunt: S17/S18/S19 lookalikes, then KILLED-AFTER-LOOKALIKE, then ERRORS-LINE-LIVE [L].
- A JSON file the tests cannot write to removes that class.
- KS-1326 lists it as a valid fix shape [L].
- The round-2 author declined it only because "a reporter file would change what the child writes" [L]. It adds a tmp file and changes nothing the parent reads.
- The round-3 gate itself read verdicts from vitest's JSON reporter [L].

Precedent for a fresh branch while a capped PR stays open: #1245 was itself raised from develop with capped #1241 left untouched (comment 2026-09-25T13:51Z) [L].

**Class:** DECIDE-NOW. The build is ours. Closing #1245 is the owner's, so it is carded to Kam and does not block the build.

**What it becomes:** one PR on `unitSuiteSlotIndependence.test.ts`. Its cells:
- a `{status:143, error:ETIMEDOUT}` result throws;
- a missing or unparsable JSON file throws;
- fail-only, skip-only and errors-line runs read correctly.

The builder first verifies the reporter fields on vitest 4.1.11 (UNMEASURED 6). The playwright copy at `systemTest/playwright/tests-unit/unit-suite-slot-independence.test.ts:139` [GG] gets a follow-up. Tier-2.

**Spark fit:** yes. One file (the reader and its cells live in the same test file), a spelled-out fix, and vitest runs in-process. It is not security. Caveat: three Claude rounds failed here on the parsing approach, so the brief must forbid human-output parsing outright.

## KS-1314 — readYaml routing cells: a multi-line import evades parserImportSites, the loaders are unpinned, and the canary pays a child spawn

**Question** [L]: the Done-when has three items. The last comment (2026-09-26T04:44Z) says *"#1278 round 2 of 2 — NO GO at the cap … closing it is not this seat's call."* The open findings are B-1278-2 (`createRequire` alias), B-1278-3 (alias and `.call` misreads, which fail loudly) and M-1278-L (lint 0 → 7).

**State at develop:** `parserImportSites` is still the line-anchored reader, at `systemTest/performance/tests/unit/support/readYamlRouting.ts:30` [GG]. #1243 `a9ae94edbed3` is an ancestor [GA]. Nothing from #1278 shipped.

**PROPOSED:** a fresh branch from develop that takes #1278's round-1 AST reader and its fixtures (items 1-3 were proven, with red arms) [L], and adds four things:
1. Track identifiers bound from `createRequire(…)` as `require` aliases (B-1278-2).
2. Make the alias and `.call` shapes read correctly, or name them in the docblock as not read (B-1278-3).
3. Fix the 7 lint errors (M-1278-L).
4. A docblock that names the unreadable residue: computed specifiers, or a helper in another module.

Item 3's canary spawn is kept as recorded (193/220 ms) [L].

This is the reversible path: it is test-support code only. "No product file is in this PR" [L].

**Class:** DECIDE-NOW. Closing #1278 is the owner's and is carded with #1245.

**What it becomes:** one PR on `systemTest/performance/tests/unit/support/readYamlRouting.ts` and its test file, with a tamper arm per finding and `npm run lint` rc 0 across both tsconfigs. Tier-2.

**Spark fit:** no. It is two files, and the AST alias-tracking needs judgement. The shape is not fully spelled out.

## KS-1317 — packages/shared runs vitest without declaring it: npm ci inside the member exits 127

**Question** [L]: *"Done when — declares the runner it invokes, or its `test` script fails with a message naming the workspace-root install, or a line in the package's README/CONTRIBUTING states that it is installed only from the workspace root."*

**PROPOSED: the CONTRIBUTING line.**
- The defect is live: `packages/shared/package.json:90` reads `"test": "vitest run"`, there is no vitest in its dependencies (`:93-117`) [G], and the root lock has one `"node_modules/vitest"` [GG count 1].
- Declaring vitest edits `package.json` plus the lock, which is KS-1290's TRAP 1 territory. That is the wrong risk for a diagnosis gap.
- A script-side message also edits `package.json`.
- The doc line is reversible and has no install consequence.
- `packages/shared` has no README [G ls-tree], so the line goes in `CONTRIBUTING.md` beside `:23` `npm ci`.

**Class:** DECIDE-NOW.

**What it becomes:** the same docs PR as KS-846. Tier-3.

**Spark fit:** no. It is docs with no runnable test.

## KS-1324 — run_shell_suites.test.sh KS-1303 cell: a `-lt 6` wall-clock margin is load-sensitive

**Question** [L]: *"Fix shapes (not chosen here): 1. Assert from the runner's own verdict plus a child-held marker … 2. keep the clock but widen the margin (for example 10 s)."*

**State:** the cell is not at develop. `git grep -c -i -E '1303|ELAPSED'` on `run_shell_suites.test.sh` returns 0 (rc 1), against a control of 49 `^check ` lines in the same file [GG]. It exists only on PR #1250's head [L].

**PROPOSED: shape 1, applied in whatever PR re-lands the KS-1303 cell.**
- It replaces a clock proxy with the property itself ("did not wait for the child").
- It keeps the deliberately unredirected child, which the ticket says must stay [L].
- Shape 2 only lowers the false-red rate.

**Class:** DECIDE-NOW. It is a design constraint, not a standalone build.

**What it becomes:** a line in lane L1's brief (KS-1330 re-land). "The T1303 cell asserts with a child-held marker, not `-lt 6`; keep the child's output unredirected." No PR of its own. Close KS-1324 when the L1 PR carrying it merges.

**Spark fit:** no. It lives inside the Claude L1 lane.

## KS-1326 — childSuiteCounts reads a child KILLED by its own 180 s spawnSync timeout as a PASS

**Question** [L]: *"Fix shapes, any one of which closes the first residue: Refuse when the spawn says so … Require vitest's trailing `Start at` / `Duration` block … Use the JSON reporter."* The 2026-09-26 comment adds ERRORS-LINE-LIVE.

**State at develop:** `unitSuiteSlotIndependence.test.ts:95-106` passes `timeout: 180_000` and never inspects `result.signal`, `result.error` or `status` [G]. The defect is live at develop, as the ticket measured at `4db87c3e4` [L].

**PROPOSED:** the spawn-status refusal plus the JSON reporter, built as one PR with KS-1313. Both tickets name the same function in the same file. The ticket's residue 2 (CALLSITE-STILL-TEXT, a pure `countsFromSpawn(result)`) is satisfied by factoring the refusal and JSON read into one pure function fed a synthetic spawn result. Residue 3 (JOINED-CLAIM) disappears, because nothing is read from joined text.

**Class:** DECIDE-NOW. This is the same build and the same carding of #1245 as KS-1313.

**What it becomes:** close it together with KS-1313's PR. The cells the ticket names, H1 → null/throw and `{status 143, ETIMEDOUT}` → throws, go in that PR.

**Spark fit:** yes, as part of the KS-1313 build (same clause).

## KS-1351 — vc-issuer: VCCredentialStatus declares no revocation fields … plus the prefer-const

**Question** [L], remaining: *"Item 3 remains open … whether the package tsconfig should stop excluding `src/__tests__`."*

**State:** items 1 and 2 merged in `63db8a38354c` (#1326) [L]. It is an ancestor of develop [GA]. `services/vc-issuer/tsconfig.json:23` still excludes `src/__tests__` [G].

**PROPOSED:** item 3 is KS-1000's class question, decided above. It does not need a separate decision. KS-1000's 2026-09-13 comment already lists `services/vc-issuer` as a class member, carried from KS-1122, "closed as Duplicate of this ticket" [L].

**Class:** ALREADY-SETTLED. Items 1-2 are settled by `63db8a38354c`. Item 3 was settled into KS-1000 by the 2026-09-13 KS-1122 duplicate ruling.

**What it becomes:** close KS-1351, citing `63db8a38354c` and KS-1000. The vc-issuer `tsconfig.test.json` arrives in KS-1000's per-service rollout.

**Spark fit:** no. Nothing is to be built here.

---

## RULED BY WEDNESDAY (2026-10-05 20:04 AEDT, under Kam's 19:52:52 card `secuura-tooling-32-decision-tickets-1005` = a)

Wednesday read this file WHOLE. **Every PROPOSED decision above is RULED as proposed**, with these three adjustments:
1. **Closes go through a board seat.** KS-956 (accepted residue: 0/46 census, `check_shared_relink.test.sh:961` pin), KS-1351 (63db8a38354c + KS-1000) and KS-1036 (after the parenting pass) are each closed with ONE facts-only comment citing the evidence above. KS-837 stays OPEN as the record. KS-964's ticket gets the 104 → 31 correction as a comment.
2. **Gate wiring = ONE grouped Kam card, not three:** KS-1146 (a service unit-suite preflight leg; rec NO), KS-1290 item 3 (the lockfile-trap leg), and KS-1033 guard 1 (wire the now-fixed demo-mutation guard). All three change what `.githooks/pre-push` runs, the KS-884 subject Kam kept.
3. **Two more Kam cards:** KS-1188 F3 (post-burn 503 wording on the auth login path; rec: reuse `userRepo.ts:973`'s hedged sentence) and the disposal of capped PRs #1245 and #1278 (rec: close both once the fresh-branch builds of KS-1313/1326 and KS-1314 merge, credited by blob).

**Queue produced (17 items):**
- **Spark (4 builds, 5 tickets):** KS-1305, KS-1313 + KS-1326 (one build; the brief FORBIDS human-output parsing), KS-1141 site 1, KS-1088 (after lane L1 lands).
- **Claude lanes:** KS-785 (tier 1), KS-955, KS-964 (31 moves + 3 refs), KS-1000 (auth first), KS-1010, KS-1033 (message + reason string), KS-1081, KS-1141 site 2, KS-1290 items 1-2, KS-1314; docs PR KS-846 + KS-1317; docs PR KS-1051.
- **Board:** KS-1036 parenting pass; the closes in adjustment 1.
- **Constraint only:** KS-1324 → a line in lane L1's brief (child-held marker, not `-lt 6`). Seat G 1st owns L1, so it goes to G 1st by addendum.
- **Kam cards:** 3 (adjustments 2-3). Each is single-subject with a default of "nothing changes".

## KAM'S RULINGS ON THE THREE CARDS (live board, verbatim, read by kam_rulings_today.sh at 20:10 AEDT by the successor seat)
- 20:06 `secuura-pushgate-three-legs-1005` = **a** — "Add none of them now (Recommended)". KS-1146, KS-1290 item 3 and KS-1033 guard 1 are NOT wired into `.githooks/pre-push`. KS-1033's lane builds the message + reason string only. Each ticket gets a facts-only comment naming the ruling (board seat).
- 20:06 `secuura-capped-prs-1245-1278-disposal-1005` = **a** — "Close each one after its replacement merges (Recommended)". #1245 (KS-1313's capped PR, this file's KS-1313 section :440) closes after the KS-1313+1326 build merges; #1278 (KS-1314's, :479; origin branch feature/ks-1314-readyaml-routing-followups-l7r25-1 per the B 62nd drafter's read) closes after the KS-1314 fresh-branch PR merges. [CORRECTED 20:3x: the first version of this line swapped the pair; drafter-caught.] Credited by blob in the closing comment. Owner of the close: the seat that merges the replacement.
- 20:07 `secuura-ks1188-burnt-backup-code-wording-1005` = **a** — "Reuse the existing gentler sentence (Recommended)". KS-1188 F3 lane reuses `userRepo.ts:973`'s hedged sentence (read at the lane's base SHA, not from this file); tier 1 (auth surface).
**Delivery:** these three land in the artefacts when the board-pass seat comments the tickets and the lane briefs quote them under RULED BY KAM; until then the cards stay undelivered.
