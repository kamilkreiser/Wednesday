--- comment 5844829788 by linear[bot] at 2026-09-26T09:03:37Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1337/k6-runner-the-pre-suite-path-is-taken-from-urlpathname-so-a-checkout">KS-1337 k6 runner: the pre-suite path is taken from URL.pathname, so a checkout directory containing a space fails ERR_MODULE_NOT_FOUND</a></summary>
<p>

## BLUF

`systemTest/performance/runner/cli.ts:162` resolves the pre-suite step with
`new URL('../../fixtures/pre-suite.ts', import.meta.url).pathname`. `URL.pathname` **is**
**percent-encoded.** A checkout whose directory contains a space yields `.../Testing%20Agent%20MAIN/...`,
which is passed to the spawn as a literal path, and the run dies with
`ERR_MODULE_NOT_FOUND … %2520 …` (the `%25` is the second round of encoding).

**This is not hypothetical on this fleet.** The QA gate's own checkout lives at
`/Volumes/DevMASTER/!CODING/Testing Agent MAIN/` — a path with **two spaces**. Any performance run
driven from a checkout like that cannot start its pre-suite step.

Found as a develop-own finding during the tier-2 gate on #1268 (report lines 214-219). **Not built**
**there**, and not built here: it is develop's, not that PR's.

## Measured at `00de57baeb405d0081fe8b6f192bd40d35acef61`

```
$ node -e "const u=new URL('../../fixtures/pre-suite.ts','file:///Volumes/Dev/Testing%20Agent%20MAIN/x/runner/cli.ts');
           console.log(u.pathname); console.log(require('url').fileURLToPath(u));"
/Volumes/Dev/Testing%20Agent%20MAIN/fixtures/pre-suite.ts     <- .pathname, what the code uses
/Volumes/Dev/Testing Agent MAIN/fixtures/pre-suite.ts         <- fileURLToPath, correct
```

`cli.ts:162` **is the only** `.pathname` **use of an** `import.meta.url` **URL in the package.** The fix-shape
already has precedent **in the same directory**, so this is a consistency fix rather than a new idea:

* `runner/actor_manifest.ts:60` — `dirname(fileURLToPath(import.meta.url))`
* `runner/paths.ts:12` — `path.dirname(url.fileURLToPath(import.meta.url))`
* `gate/cli.ts:31` — the same

## Done means

1. `cli.ts:162` uses `fileURLToPath(new URL('../../fixtures/pre-suite.ts', import.meta.url))`.
2. **A regression cell in the gate's own shape: run the CLI from a copy of the tree whose path**
   **contains a space**, and assert the pre-suite step resolves and spawns. A cell that only asserts
   the string has no `%20` would pass for a path that is wrong in some other way.
3. A sweep for any other `.pathname` on an `import.meta.url` URL across `systemTest/`, so the fix is
   the class and not the one line. Measured today: **1** occurrence, this one.

## Why it was not fixed in the round that found it

It is **develop's own defect**, not #1268's. #1268 touches `packages/shared`; folding an unrelated
`systemTest/performance` fix into it would widen a fix round past its declared scope and past the
files its gate reviewed.

## Search before filing

`searchIssues`, KS team, `includeArchived: true`, every page literal-matched client-side:
`preSuiteStep` **0**, `cli.ts:162` **0**, `%2520` **0**. `ERR_MODULE_NOT_FOUND` returns 3 (KS-691,
KS-149, KS-1148 — all unrelated: worktree preflight, vc-issuer tooling, CI-runner gaps).
`pre-suite.ts` returns 7, all about the step's own behaviour rather than path encoding.
Controls: `performance` **37** literal hits and `runner` **44** (the matcher fires); a nonce token
never written anywhere **0**.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1337-take-the-k6-pre-suite-path-with-fileurltopath-not-urlpathname-4f49698ead8a">Review in Linear</a></p>

