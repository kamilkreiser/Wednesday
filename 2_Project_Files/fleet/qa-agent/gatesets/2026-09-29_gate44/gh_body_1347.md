`Refs KS-1374`

## Why
Kam's instruction, verbatim (live board, relayed):

> **16:17:55** "Peter has responded to KS-1374 on WhatsApp. can you please make the change"
> **16:18:57** "his reply was for us to implement the change"

"The change" is our own comment's option 2 plus one guard: raise `RATE_LIMIT_MAX_REQUESTS` on **LOCAL
stacks only**, leave demo and production as deployed, and add one limiter test at the demo's limit.

## Part A — one api-gateway cell pinning the global limiter at the demo figure
New file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1374-global-limiter-at-demo-limit.test.ts`
(116 lines, **no product line changed**). Wiring cells read `index.ts` as text (the KS 733 shape: no
gateway test boots it); behaviour cells drive `express-rate-limit` with the same options and the REAL
skip predicate over a local socket.

- **7/7 green** at the untouched tip and at the PR head.
- **The bytes committed ARE the bytes that were verified.** Applying the held golden
  (sha256 `165c0ab871bd90b4`) to a clean checkout of the base produces a file byte-identical to the
  committed blob: 4,987 B, sha256 `330e6349133475c7`, `cmp` rc 0. A one-byte mutation of the committed
  copy `cmp`-differs, so the test discriminates.
  ⚠ Comparing `git diff base head -- <file>` against the golden directly does **not** match, and that
  is formatting rather than content: `git diff` emits `diff --git` / `new file mode` / `index` header
  lines that the golden (a bare unified diff opening at `--- /dev/null`) does not carry. The file-bytes
  comparison above is the real test.
- **Six tamper arms, each RED ALONE on exactly the named cell**, each 6 passed / 1 failed, each restored
  by byte copy with sha256 proof and a clean tree afterwards:
  | arm | tamper | red cell |
  |---|---|---|
  | MAIN | `max:` reads a different environment variable | W1 |
  | A1 | `max:` hard-coded to 10000 | W1 |
  | A2 | a 15-minute window instead of 60 s | W2 |
  | A3 | the compose fallback raised to `:-10000` | D1 |
  | A4 | `/health` removed from the read-only skip list | B3 |
  | A5 | `demo` added to the test-token bypass envs | B4 |
  A 0-passed-AND-0-failed result would have been reported as a load failure, not as an inert tamper;
  none occurred. The tamper anchor was proved unique before use (1 occurrence).
- **api-gateway whole suite: 90 files / 805 tests → 91 / 812, 0 failed** (this file's 7 cells), measured
  at base `bd740147c3d8`.
- The hold on this READY **was done by hand** (the automated holder refused on its known
  test-only/code-patch gap). Canonical patch:
  `WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1374/KS-1374.golden.diff`.

## Part B — the two local env templates
`Blockchain/Dev/env.example` and `Blockchain/Dev/.env.example` set `RATE_LIMIT_MAX_REQUESTS=10000`.
The stale note above the first (which claimed a 2000/min ceiling for Schemathesis and that "demo stays
at its 100/min default") is rewritten to say what is now true.

- **`docker-compose.yml` keeps its `${RATE_LIMIT_MAX_REQUESTS:-2000}` fallback deliberately.** The demo
  VM runs that compose file with its own `.env`, so the fallback is what the demo inherits — cell D1
  pins it, and arm A3 proves D1 reddens if it moves.
- `deployment/azure/services.bicep` is untouched (2000 for `dev`, 100 for every other Azure env).
- **A template only seeds a NEW `.env`.** `scripts/bootstrap-env.sh` leaves an existing one alone, so
  **each operator raising an existing local stack makes the same one-line edit by hand.** No `.env` file
  was edited here — they are gitignored and may hold secrets.
- Both templates get the edit: `env.example` is canonical (KS 1081), and `.env.example` is still a full
  327-line template at the base.
- A template value cannot go red on its own, so Part B's proof is Part C's cell reading the value plus a
  direct read of both lines, with a control that finds the compose `:-2000` unchanged.

## Part C — the Akto harness reads the platform limit instead of hard-coding it
`systemTest/akto/src/setup/aktoRateLimit.ts` hard-coded `PLATFORM_REQUESTS_PER_MINUTE = 2000`, and
`derivedRateLimit()` returned `floor(2000 × 0.75)` = 1,500/min whatever the stack allowed.
`tierPacing.ts` feeds that to the pre-merge and security tiers, **so Part B on its own would not have
sped the Akto scans up at all.**

New `platformRequestsPerMinute()` reads `RATE_LIMIT_MAX_REQUESTS`, defaulting to the exported 2000.
`derivedRateLimit()` now uses it. The in-repo precedent is Schemathesis, which already reads the same
variable with the same default (`systemTest/schemathesis/scripts/runner/config.py`).

- **`PLATFORM_REQUESTS_PER_MINUTE` stays an exported `const` at 2000**, so every existing import and the
  existing unit cells keep working untouched. Nothing became lazy or function-shaped.
- **It reads through `env()` from `../config/env`, not `process.env`.** This package confines
  `process.env` to `src/config/**` and enforces it with a lint rule — **eslint refused my first version
  for exactly that reason**, which is the boundary working rather than a rule to suppress.
- **Junk falls back to 2000 and warns; it never paces faster.** Absent, empty, whitespace, non-numeric,
  zero, negative, fractional, and beyond `MAX_SAFE_INTEGER` (so `1e21` is refused although it is
  numeric) all return the default. It does not refuse loudly: this runs unattended in a gate, and a typo
  in an operator's `.env` should slow a scan, never fail it. Falling back can never pace faster than the
  default, which is the property that matters.
- A **lower** limit is honoured, so an Azure-style 100/min paces slower rather than faster.
- **Red-first, on a develop-compatible probe:** at develop the assertion fails `expected 1500 to be
  7500` — a real red with the module loading normally. ⚠ The shipped cell file **cannot** be run at
  develop, because it imports `platformRequestsPerMinute`, which develop does not export; that would
  give 0 passed AND 0 failed, which is a load failure and proves nothing. The probe imports only
  symbols develop has, and it was deleted rather than committed.
- **akto unit suite: 92 files / 1632 tests → 93 / 1643, 0 failed** (11 new cells: E1, E2, E3, E4 ×7, E5).
  The existing `aktoRateLimit.test.ts` cells still pass (0 failures naming that file).
- `tsc -p tsconfig.json --noEmit` rc 0. **It caught a real defect first** (TS4111: an index-signature
  property needs bracket access), now fixed.
- **Stale comment corrected:** the `@example` read "→ 1800 while the platform allows 2000/min", which was
  already wrong on develop — the headroom is 0.75, so 2000 gives 1500. The 1800 is a leftover from a 0.90
  headroom. Never a behaviour defect, only a false comment, corrected because this function changed.
- The log line now reports the live budget rather than the 2000 constant.

## Test Evidence
**Touched:** 5 files, +300 / −14 — two env templates, one new api-gateway test, `aktoRateLimit.ts`, one
new akto unit test. **No platform runtime change:** the gateway's code, the compose fallback and the
bicep are untouched.

**Ran** (base `bd740147c3d8`, head `2c4b98253b1f`): the two suites above with before/after counts; the
six tamper arms; the red-first probe both ways; `tsc` for `systemTest/akto` rc 0; eslint rc 0 on both
changed files.
**eslint control, both directions on the SAME command and the SAME files:** before these fixes it
printed 1,190 bytes and **6 rule violations** (`jsdoc/require-example`, `no-restricted-properties`,
`curly` ×2, `jsdoc/require-param`, `@typescript-eslint/no-dynamic-delete`); after, 0 bytes. A silent
clean is only evidence when the same command has been shown to print.
**Push preflight: 12/15 legs ran, 3 SKIPPED — legs 3, 4 and 8, "local stack not up". Nothing failed.**
That is the hook's own wording and **it is not a pass**; stated as a ratio.

**NOT run / NOT covered:**
1. **The live demo's real limit was never read.** The VM's `.env` is off-repo. The "demo figure" of 2000
   in Part A's cells comes from our own comment and the templates, not from a read of the demo. And
   `deployment/azure/services.bicep` sets this variable to **2000 for `dev` and 100 for every other
   Azure environment** — so which figure the live demo actually runs is **unmeasured**, and this PR does
   not resolve it.
2. **Part A's behaviour cells drive their own `express-rate-limit` instance** with the same options, not
   `index.ts`'s inline instance. What is proved is the option set's behaviour plus the real skip
   predicate, not that `index.ts` wires it — the wiring cells cover that separately, by reading the
   source text.
3. **Each operator's existing `.env` needs the same one-line edit by hand.** Nothing here changes a
   running stack.
4. **How the Akto harness receives its environment, measured** (your brief listed this unmeasured):
   `aktoRateLimit.ts` does **not** itself load any `.env`; it reads `process.env` through `config/env`.
   `systemTest/akto/src/config/env.ts` and `src/config/index.ts` DO load `Blockchain/Dev/.env` and
   `.env.local` via dotenv for other configuration. **Whether that loader has run before
   `platformRequestsPerMinute()` is called in a real scan is NOT pinned by this PR** — in the unit cells
   the variable is set explicitly. So on a real local scan the value may come from the shell rather than
   from `Blockchain/Dev/.env`, and an operator should export it or confirm the loader ordering.
5. **`systemTest/akto` needs its own `npm ci`** — it has its own `package-lock.json` (252,142 B) and its
   `node_modules` was absent; the pushing worktree's root install does not cover it. 413 packages, rc 0.
6. No scan was run against any environment. Nothing was deployed.

Foreign ticket keys are de-hyphenated so this PR attaches only its own: KS 206, KS 733, KS 1081,
KS 709, KS 1286, KS 618.
