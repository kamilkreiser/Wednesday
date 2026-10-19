VERDICT: GO WITH NOTE at head bd07a37757e4c22e2bf5d0ff6b76bfa116106d80 (tier 1 delta, round 2 of 2; landing tree 346c5104f2a756f1fdd7e97aefaeea91d9eaa4d1 on develop c66b834ed4511e77ec4059abe1f46a4bc4e72de6; 0 blockers, 5 notes)

## BLUF

Both round-1 blockers are closed, and I measured each one at the landing tree.

- **B1 is closed.** I used a browser cookie-jar model (tough-cookie 6.0.1) with the REAL `Set-Cookie` that express emits for init's options. The redirect host was read from the landing tree's own `services.bicep` and `env.dev.json`. With init on the admin host and the callback at the configured redirect, the cookie is **present** on both configs. **Control:** develop's config sends the callback to the API host, and the cookie is **absent** on both.
- **B2 is closed.**
  - BG-M7 (one fixed verifier) is killed by R19 only.
  - BG-M11b (MSAL never gets the verifier) is killed by E1 only.
  - E2 is a real control. My mutant BI-M3 (always send a `codeVerifier` key) is killed by E2 and by nothing else.
- **N1, N2, N4, N5 and N6 are closed.**
  - An encrypt-under-develop / decrypt-under-landing round trip works for access and refresh tokens, in both directions.
  - The AAD-enforcement control refuses a wrong column, a wrong row and the verifier label.
  - The delta's changes to the shared crypto files are a 3-line comment (`encryptedField.ts`) plus the verifier label (`tokenCrypto.ts`), and nothing else.

**Landing checks:**
- `merge-tree` = `346c5104…`, rc 0.
- m365 suite: develop 15 files / 148 cells → landing 20 / 201, 0 failed. Exactly 2 cells vanished, both renames (E10 and A6); 55 are new.
- `tsc` rc 0 on m365 and api-gateway. The control (a planted TS2322) gives rc 2.
- Gateway startup-migrations: 7 files, 38/38 on both sides, cell names identical.

**Five notes, none blocking:**
- Three of my own mutants survive the whole suite (NB1, NB2).
- A custom-domain admin topology is outside the author's table (NB3).
- One stale line citation (NB4).
- One process disclosure (NB5).

## Findings: blockers

None.

## Findings: notes

**NB1. The PKCE verifier's SECRECY is unpinned. Two compile-safe mutants survive all 207 cells (201 author cells + my 6).**
- **BI-M1:** `const codeVerifier = state;`. The verifier then rides in the authorization URL and the callback URL, which nginx logs (round-1 N10). tsc rc 0, 0 red.
- **BI-M5:** `const codeVerifier = sha256Hex(connectionId);`. That is deterministic and derivable from an id that init returns. tsc rc 0, 0 red.
- **Why they survive:**
  - R11 checks S256(verifier) == challenge within one sign-in.
  - R19 checks that two sign-ins differ, and both mutants still differ per sign-in.
  - R18 checks the cookie, not the verifier.
- **Impact is low.** The client is confidential, so redeeming a code still needs `ENTRA_CLIENT_SECRET`, and PKCE is defence in depth here. Round 1's stated B2 condition (a fixed verifier, or none, must red) is now met, so this is not B2 reopened.
- **Suggested cell:** for every value in init's response, the authorization URL's params and the cookie, assert that S256(value) != challenge. That kills BI-M1. BI-M5 needs a "verifier is random" property: one cell that inits twice for the SAME connection, or a stubbed `randomBytes`.

**NB2. H1 matches the bicep TEXT and does not evaluate it. BI-M4 survives.**
- **BI-M4:** `empty(apiPublicUrl) ? '' : …` changed to `!empty(apiPublicUrl) ? '' : …`. The deployed redirect then becomes `''`, and the service falls back to `OAUTH_REDIRECT_URI` or `localhost:6882`. 0 red.
- H1's regex still finds the `https://…-admin…/api/m365/callback` literal in the false branch.
- **Control:** BI-M6 (FRONTEND_URL and the redirect both moved to the API host) IS killed by H1, through its `-admin.` assertion. H-M1 and H-M1e are killed by H1 and H2.
- Low. The bicep was not compiled (no Bicep CLI, by the author's account and mine).

**NB3. A fifth topology, not in the author's table: a custom admin domain via `deployment/azure/configure-domain.sh`.**
- That script binds `admin.secuura.io` to `${PROJECT_PREFIX}-admin` (`:362-374`; it targets `secuura-staging-rg`). On such a deployment the admin answers on two hosts.
- The bicep redirect is fixed to the default-domain admin host.
- **Jar model:** init on `admin.secuura.io`, then callback at the bicep redirect: cookie **absent**. **Control:** init on the default admin host: cookie **present**.
- **Not new:**
  - FRONTEND_URL was already on the default domain.
  - Before this PR the redirect went to the API host, which failed either way.
  - Nothing in that script points the redirect at the API host.
- **Ask:** the deploy precondition on KS-1677 should say one of two things. Either users must reach the admin at the host named in `ENTRA_REDIRECT_URI`, or a custom-domain deployment must set the redirect (and the Entra registration) to its custom admin host.

**NB4. A stale citation in the shared crypto header.** `encryptedField.ts:61` still cites `tokenCrypto.ts:24` for `tokenAad`, which is now at `:28`. Its helper row still lists only `svc_m365_connections.{access_token,refresh_token}`, with the verifier covered only by the new addendum (`:129-131`). The header already disclaims its line numbers ("measured at develop b0373773b"), so this is cosmetic. Nothing in the repo pins the 22/23 pair count; the census found only the header itself and an unrelated "23 pairs" in a schemathesis doc.

**NB5. Process disclosure (mine).**
- My first gateway startup-migrations run passed the seven file filters as one unquoted zsh variable. zsh does not word-split, so vitest matched **0 files / 0 tests on both sides**, and a `diff` of the two empty name lists printed "names-identical".
- I caught it on the zero (0 files is impossible for a 7-file set), confirmed with a single-filter run (2 files / 14 tests), and re-ran with literal arguments: 7 / 38 / 0 failed on both sides, names identical.
- The 38 is the only figure I report.
- My m365 and mutant runs used Python argument lists, so they were not affected.

## Round-1 items

- **B1: CLOSED.** The cookie is present at the landing tree's redirect on both bicep and env.dev.json, and absent on develop (control).
  - `services.bicep:1625` and `env.dev.json:107` agree: both give `https://secuura02-demo-admin.kindtree-935b2ded…/api/m365/callback`, derived the same way FRONTEND_URL is (`:1632`).
  - Admin nginx proxies `/api/` with `$request_uri` to the admin app's `API_UPSTREAM` (bicep `:1767`), and the gateway mounts `/api/m365/callback` unauthenticated (`proxy.ts:937`).
  - VMs: compose default `localhost:6882`, a single Caddy host (`deployment/caddy/Caddyfile:33-34`), unaffected.
  - Census: no k8s, helm or terraform in the repo. `docker-compose.production.yml` inherits the base compose default. Staging compose, e2e and dev-debug carry no ENTRA vars (control: production compose has 5 entra and 2 m365 hits). `env.demo.json`, `main.parameters.json` and `services.parameters.json` have 0 m365/entra/redirect hits (control: env.dev.json has 5/3/1 by the same count).
  - Only the admin wizard starts a sign-in (control: issuer and outlook do reference m365, but never `connections/init` or `authorizationUrl`).
  - Residual topology: NB3.
- **B2: CLOSED.** BG-M7 → R19, BG-M11b → E1; each is the only red, at full-suite scale, tsc rc 0. E1 reds on develop; E2 passes on develop and is killed by BI-M3. Residual: NB1.
- **N1: CLOSED.** BG-M4 (a DB miss falls back to memory) → R17, the only red.
- **N2: CLOSED.** BG-M3 (binding = state) → R18, the only red.
- **N4: CLOSED (relabel accepted; A6 is NOT vacuous).**
  - A6-U (`/complete` re-added with no org binding): A6 and R10 both red.
  - A6-B (re-added WITH an org-bound 404): only R10 reds.
  - So A6 discriminates the org-binding property. R10 alone owns the removal.
  - Unmutated baseline: 207/207.
- **N5: CLOSED in the READY.** My own YAML parse (the repo's `yaml` package):
  - develop c66b834 = 312 paths / 347 ops (the one non-`/api/` path is `/webhooks/stripe`);
  - landing = 311 / 346;
  - removed exactly `POST /api/m365/connections/complete` and schema `M365CompleteConnectionRequest`; nothing added.
  - Control: a line grep `^  /` gives 312 / 311.
  - The PR body was not read (no GitHub API reads).
- **N6: CLOSED.**
  - SETUP.md step 4 is rewritten.
  - The baseline's two keys are gone (`accepted` 171 → 169; the author's 177 → 175 counts `accepted` plus the 6 in `$generated`; the delta is the same).
  - Inventory addendum present.
  - Verifier label `svc_m365_oauth_states.code_verifier.<id>`; the token labels are byte-identical to develop's (cell BI1-N6f).
  - Round trip (scratch cell `gatebi1-aad-roundtrip`, which imports develop's and landing's `tokenCrypto` side by side): access and refresh decrypt in both directions.
  - Control BI1-N6e: wrong column, wrong row and the verifier label all fail to open a token.
  - Positive control for the cells: BI-M2 (relabel the tokens too) reds BI1-N6b/c/d/f and the existing `tokenCrypto` "binds the context" cell.
  - The `f9f425582bb2` verifier label differs, but that head was never merged or deployed, and states live 10 minutes.
  - Left on purpose (historical): `known-issues-and-baseline.md:697`, the KS-693 reviewer comment, and the `ks1478` fixture. These were read; none of them loads the baseline in a way the removal could change.

## FOUND / TESTED / HOW

**Setup**
- Heads by `ls-remote` (read-only), at start and again before the verdict:
  - develop `c66b834ed451…`;
  - `refs/pull/1647/head` = the branch = `bd07a37757e4…`;
  - `f9f425582bb2` is an ancestor (fast-forward).
- Clone: `git clone --shared` of the spark cache (`refs/wed/pr1647r2`) into `scratchpad/gate_bi1/repo`.
- Local landing commit = tree `346c5104…` (parents develop, head; not pushed). Worktrees: `dev` = c66b834, and `r1` = f9f42 (unused).
- `npm ci --ignore-scripts` into the clone; `packages/shared` built.
- Every node, npm, tsc and vitest call ran through `scripts/inrepo.py`, which sets the subprocess cwd INSIDE the clone (asserted). No `npm exec`/`npx`, no `cd`.

**Delta (Q4)**
- 10 files, +150/−26, matching the author's list.
- `packages/shared` diff from develop to landing = 3 comment lines.
- `tokenCrypto.ts` = comments plus the conditional label. The `TokenColumn` type is unchanged since f9f42.
- Baseline:
  - `POST /api/m365/connections/complete` is absent from the landing spec (YAML parse).
  - `systemTest` census: develop has 2 hits in the baseline; landing has 0 in the baseline and leaves only docs and the fixture.
  - The traceability assertions (all 5) were run by a stdlib runner, because the venv cannot run pytest (KS-571): all pass at landing and on develop. **Control:** an injected entry citing closed KS-592 fails 2 of the 5.
  - `baseline_gate` only REPORTS a listed pair that did not fire, so the removed keys were dead.

**Topology (Q1)**
- `scripts/jar.cjs`: the real express `Set-Cookie`, then the tree's own config:
  - landing: present / present;
  - develop control: absent / absent.
- `scripts/jar_custom.cjs`: NB3.

**Mutants (Q2, Q3, Q6)**
- `scripts/mutants.py` and `mutants_a6.py`. For each mutant: tsc on m365 (rc 0 for every one), then the FULL m365 suite plus my gate cell file, and a byte-identical restore was asserted afterwards.
- Clone `git status` after all runs: only my scratch cell file.

| mutant | result |
| -- | -- |
| BG-M7 | killed by R19 |
| BG-M11b | killed by E1 |
| BG-M3 | killed by R18 |
| BG-M4 | killed by R17 |
| H-M1 | killed by H1 |
| H-M1e (env.dev.json to the API host) | killed by H2 |
| BI-M2 | killed by tokenCrypto + BI1-N6 |
| BI-M3 | killed by E2 |
| BI-M6 | killed by H1 |
| A6-U | killed by A6 + R10 |
| A6-B | killed by R10 |
| BI-M1 | **survived** (NB1) |
| BI-M4 | **survived** (NB2) |
| BI-M5 | **survived** (NB1) |

- "Mine, not the author's" (BI-M1…M6, A6-U, A6-B) is judged from the READY's list, not from the PR body's table.

**Landing (Q5)**
- m365 suite by cell name: develop 148 → landing 201. Vanished: KS-1641 E10 and KS-1673 A6, both renames. New: 55.
- The new cells red on develop c66b834: H1, H2 and E1 red; E2 passes, as a control should.
- `tsc` rc 0 for m365 and api-gateway. The 4 delta-touched test files also type-check in their own program, rc 0 (planted TS2322 control: rc 2).
- Gateway: 7 files / 38 on both sides.
- Migrations: 053 and 054 are both present. `run-migrations.sh:149` loops over `migrations/*.sql` in lex order, and `:118` skips a file by FILENAME membership in `_secuura_migrations`, so 053 applies on a DB that already has 054. 053 (the m365 oauth-states table) and 054 (vc-issuer) are independent. `init.sql` merges clean (+17 lines from develop).

## NOT RUN

- No Bicep compile and no `az` (neither is present).
- No real Microsoft sign-in, no browser end-to-end on Azure, no live custom-domain check. B1 and NB3 rest on the cookie-jar model plus source.
- No Docker and no stack, so the preflight legs 3, 4 and 8, schemathesis and the migrations runner image were not run.
- 053 was not re-applied on real PG this round. Round 1's result stands: the delta does not touch 053, the consume SQL or the leaked-state refusals.
- `check:openapi` was not re-run: the delta touches neither the spec nor `m365-integration.openapi.ts`.
- The traceability suite was not run under pytest (venv 3.14.5 vs the required 3.14.8). Its assertions were run by my stdlib runner instead.
- PR body and Linear: not read.

## Wall-clock

21:28Z → 21:46Z (2026-10-19 UTC; 08:28 → 08:46 AEDT 2026-10-20). Heads re-read at 21:43Z: unchanged (develop `c66b834ed451`, head `bd07a37757e4`, landing `346c5104f2a7`). `git -C /Volumes/DevMASTER/WEDNESDAY status --short`: no untracked paths outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/ and 2_Project_Files/fleet/briefs_staged/. The modified dashboard and scoreboard files are not mine.
b24f65f3b5d37255b23277b589c167e8c0c1140765f3b46832179654ad2c5c2a
