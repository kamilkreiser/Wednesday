#1303 KS-1350: correct the three stale sentences in the webhooks fail500 docblock
head 0103e2dd5ab6d6d211d84602c47b937edfba2430

## What this changes

**COMMENTS ONLY.** The docblock above `fail500` carried three sentences that were stale or only-now-true:

1. It said seven catch blocks **"put"** the thrown error's own text in the 500 body — present tense — when
   KS1341 parts A, B and C (#1288, #1290, #1292) had already routed all seven through this helper. It now
   reads as history, and states plainly that all seven call it.
2. It said the helper is declared **"at the END of the file"**, which stopped being true once the default
   export moved below it. It now names where the helper actually sits: after every route, immediately above
   the default export.
3. The tense of the placement rationale followed suit ("left every line above it where it was").

One file, **+11 / -8**, every changed line inside `services/originate/src/routes/webhooks.ts:549-561`.
`Refs KS-1350`.

## The proof is TOKEN EQUIVALENCE, not red/green

A comment has no behaviour to red, so the claim to prove is that **no code changed**. Measured with the
TypeScript 5.9.3 parser: **2789 parser leaves before, 2789 after, identical**, walking `getChildren()` and
**excluding the JSDoc kind range** (310–352).

**Four controls, each driven — two that must break equivalence and two that must preserve it:**

| control | expected | got |
|---|---|---|
| **A** one-token code change (`fail500` → `fail501`) | breaks | rc 1 ✓ |
| **B** JSDoc comment edit | **preserves** | rc 0 ✓ |
| **C** string-literal change (`'Internal server error'` → `…ERROR'`) | breaks | rc 1 ✓, diverging at leaf 2779 on exactly that literal |
| **D** non-JSDoc block comment edit | **preserves** | rc 0 ✓ |

**Two earlier versions of this instrument were wrong, and control B is what caught both.** A raw
`ts.createScanner` mis-lexes the first backtick — without the parser driving `reScanTemplateToken` it
swallows the rest of the file, comments included, into a single token (783 "tokens"). Parser leaves taken
without the JSDoc filter also fail, because **TypeScript parses JSDoc into the AST**, so `/** … */` blocks
arrive as leaf nodes (kind 321, `JSDocComment`) and a comment edit reads as a code difference. Only the
third version is sound, and a control that must *pass* is the reason I know it. Control C was also run
once **vacuously** — its anchor had a quoting error, so it tested a stale file — and was redone.

## Provenance

Produced by the local model (Spark) under a Wednesday brief, **re-verified by this seat**. Byte-identical
to the brief's golden (`cmp` rc 0, **sha1 `d3fa0a25e1c8`**, matching the READY's stated value), which is
itself `cmp` rc 0 against the run's canonical `patch.diff`. Applied **strictly** (`git apply --check -p1`,
rc 0) at develop `94c9c7aa9be7`, with a hunk-count tamper (`+549,999`) git refused (rc 128). The hunk's
old side is lines **549..561**, equal to the declared window. Of the 19 `+`/`-` lines, **zero are
non-comment-shaped**. After applying, the file is **byte-identical (`cmp` rc 0) to the golden's own
`webhooks.fixed.ts`**, with a control proving `cmp` discriminates.

## Test Evidence

**Touched:** `services/originate/src/routes/webhooks.ts` (comments only)

**Ran** — worktree detached at develop `94c9c7aa9be7`; `npm ci` 1936 packages; `packages/shared` BUILT.

| check | result |
|---|---|
| token equivalence, JSDoc excluded | **2789 leaves both sides, IDENTICAL** |
| the four controls above | **4/4 behaved** (A rc 1, B rc 0, C rc 1, D rc 0) |
| originate suite | 84 suites, **979 passed / 979**, rc 0 — unchanged from the tip, as a comment change must be |
| `tsc --noEmit` (package program) | rc 0, **0 errors** |
| `eslint src` | rc 0, **0 errors** (22 warnings, none on this file) |
| numstat | **11 / 8**, one file, all inside `:549-561` |

**Gate lines THIS push printed** (`s-b33-ks1350-0103e2dd5ab6-push.out`, per suite block by exact basename):
`pre_push_hook_base.test.sh` **28/0** · `..._fixture_guard.test.sh` **6/0** · `run_shell_suites.test.sh`
**49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)** · `^FIXTURE BUILD FAILED` **0** ·
`OK — 13 code guards passed.` · `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`
Push rc 0; 0 orphaned `login_stub` pids.

**Migrations + config:** none. No migration, no `package.json`, no lockfile, no test file. Exactly **1 file
staged**. The token-equivalence script lives in my record folder outside `2_Project_Files` and is not
committed.

**NOT run / NOT covered:**
- **Nothing deployed.** No behaviour is claimed or tested here; the suite run is a negative check that
  nothing moved.
- **No widened, test-inclusive `tsc`** was run for this item: the change touches no test file and adds no
  cell, so the package program already covers the only file involved. Stated rather than implied.
- The integration suite was not run (needs a live stack); preflight legs 3, 4 and 8 do not run without one.
- The docblock's factual claims about parts A/B/C and about the export position were verified **by reading
  the file at this tip**, not by re-running the 2026-09-26 gate that originally measured the leak.

Refs KS-1350

