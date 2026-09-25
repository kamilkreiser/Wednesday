# CAPTURE for gate25T2 (QA/Secuura-batch1268) — 2026-09-25T20:43:59Z

NO READY MESSAGE ID reached the drafter for any PR of this kit (the seat records carry none; a listing would mark mail seen). Each PR's seat
claims are captured from its PR BODY, its head COMMIT MESSAGE and the seat HANDOVER files below, each verbatim with its TEXT_SHA256.

## #1268 KS-1318 + KS-1142 + KS-1316 (Seat L7, T2) — head a8e0fca70ed41ef061cc99a325b610d27f08c7fb

#1268 ticket line: #1268 is KS-1318 + KS-1142 + KS-1316.

### PR BODY (gh_body_1268.md) TEXT_SHA256 456475eb6d5a7e144a7cc16006fcf23ed86ad2eaced4b56b6a06ecd1e18fc6a2

#1268 KS-1318 + KS-1142 + KS-1316: ks781 tag set, corpus containment, guard reachability
head a8e0fca70ed41ef061cc99a325b610d27f08c7fb

## BLUF

**Test-only, three findings, one PR** — KS-1318 and KS-1316 are the same file and KS-1142 reads it, so sequential PRs would each need a merged-blob equality target on a file all three touch. Every claim below is measured; the interesting results are that **the old KS-1318 cell was green under a permutation of the whole file**, and that **KS-1316's own control caught a defect in my first walk**.

`Refs KS-1318` · `Refs KS-1142` · `Refs KS-1316`

---

## KS-1318 — the combined cell asserts the set of tags, not the count

`toHaveLength(3)` is green under any permutation and under any relabelling that keeps the cardinality. Replaced with `toEqual` of the three tags **in source order** — the order confirmed by measurement, not assumed.

| arm | with the new assertion | with `toHaveLength(3)` |
|---|---|---|
| **A** — `return shapes.slice().sort()` | **1 red — the combined cell ALONE**, 0 per-shape rows | **0 red — the whole file green** |
| **B** — the `export default function` branch emitting another branch's tag | 2 red — combined cell **and** 1 per-shape row | 1 red — per-shape row only; **the combined cell stayed GREEN** |

Arm B is the finding verbatim: *"it would pass if two shapes were detected under one another's name."* Arm A is the stronger one — it is the case where **only** the combined cell can see the change, because the per-shape rows are fed one shape each and cannot see order at all.

---

## KS-1142 — one literal, two readers

K1's 27-package literal is hoisted to module scope. The new **K1b** cell in `entrypoint-corpus.test.ts` reads ks781's `CORPUS` **from source text** — ks781 is a test file, and importing it would execute its suites — locates it **by symbol** (`const CORPUS = [`), and asserts its package set is a **subset** of K1's.

**Subset, not equality, and the cell says why.** `CORPUS` is a FILE list and K1 a PACKAGE list; `services/blockchain` and `services/shared` are guarded by K1 alone. An equality assertion would red at the tip for that reason and would push someone to "fix" it by widening `CORPUS` — the opposite of the pin. **R-2 is kept and named in the cell title: K1 still reds on ordinary growth by design.**

| arm | result |
|---|---|
| swap one `CORPUS` path's package for one K1 does not list | **K1b reds** |
| rename the `CORPUS` symbol so the parse finds nothing | **K1b reds** |
| restored | 0 red |

The second arm is not decoration: `[]` is a subset of everything, so both sides assert non-empty first or the containment passes vacuously.

---

## KS-1316 — the gate's syntactic fix, not a recorded limitation

A guard **defined** inside the parser continuation but never **called** read `guarded: true`. That over-reports, which is the unsafe direction.

**Why this is decidable, having first argued it was not.** General reachability is control flow and a text-level walk cannot decide it. But the finding is narrower: whether a **nested function expression** is invoked *in the continuation's own body* is syntactic — it is immediately invoked, handed to a call, or bound to a name that is called there. The walk no longer descends into an uninvoked nested function expression. The continuation itself is always entered, because the parser invokes it.

| cell | shape | reads |
|---|---|---|
| **W9 🔴** | `const later = () => g(req,res,next); next();` | `guarded: false` (was `true`) |
| W10 CONTROL | the same arrow, `later();` | `guarded: true` |
| W11 CONTROL | `(() => { g(...); })();` | `guarded: true` |
| W12 CONTROL | `[1].forEach(() => { g(...); });` | `guarded: true` |
| W13 | `if (false) { g(...); }` | `guarded: true` — **STILL NOT DECIDED**, pinned as such |

**Under develop's walk with these cells present: exactly ONE red, W9.** Every control is green at **both** ends, so none of them is satisfied by a walk that merely stopped entering nested arrows.

**W11 caught a real defect in my first version of the walk.** An IIFE parses as a call whose callee is a `ParenthesizedExpression`, so the `invoked` flag did not survive the parentheses and the arrow read as a definition. **W9 alone would have passed over it** — which is the whole argument for building the controls rather than only the red cell.

**What is NOT closed:** W13's class. Reachability of a *statement* is control flow. KS-1143's indirect-invocation false negative is the opposite direction and stays out of scope, as ruled.

---

## Test Evidence

**Touched**
- `packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts` — the J2 combined assertion, the LEG F guard walk, and cells W9–W13.
- `packages/shared/src/__tests__/entrypoint-corpus.test.ts` — K1's literal hoisted, cell K1b added.

**No product file is touched.** Both files are under `src/__tests__`.

**Ran**
- `packages/shared`: **941/941 bare → 947/947 patched**, 48 files, **+6 = exactly these cells** (W9–W13 and K1b). `npx vitest run --no-file-parallelism` in `s-l7-ks781`, at develop `4db87c3e4b98`, load average **17.67** bare / **10.00** patched. Baseline taken before any edit on a clean tree.
- `npx tsc -p . --noEmit` → **rc 0**. `npm run build` → rc 0.
- Every arm above, each asserting its anchor was found **and** that bytes changed, so a tamper that did not apply could not read as a clean pass.
- **Push gate:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` — legs 3, 4, 8, local stack not up. Not quoted as a pass.
  Fleet STOP count with `packages/shared` **built**: `pre_push_hook_base` **28/0** · `fixture_guard` **6/0** · `run_shell_suites` **49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)**.

**NOT run**
- Legs 3, 4 and 8 — local stack not up, per the standing verdict.
- **The LEG F walk change is exercised by fixtures, not by a running Express app.** W9–W13 are source strings fed to `routerParserSites`; nothing here proves runtime behaviour of any route.
- **No product behaviour changes.** The guard walk is a test-side analyser; tightening it changes what the leg *reports*, not what any service does.
- W13's class (statement reachability) and KS-1143's indirect-invocation false negative are open by design.
- KS-1318 arm A uses `.sort()` as the permutation vehicle; no other permutation was enumerated.

**Migrations + config**
- **None.** No migration, schema, runtime config, `package.json`, lockfile, Dockerfile, route or OpenAPI surface.

## Note for the reviewer

If the gate NO-GOes one of the three, the other two are held with it — that is the accepted cost of the one-PR vehicle, agreed before building.



### HEAD COMMIT MESSAGE TEXT_SHA256 38c66fd9222c86433466d765b0d66c421640b1b5df9102ccb3e31d1746abd259

KS-1318 + KS-1142 + KS-1316: ks781 tag set, corpus containment, guard reachability

Three findings in one PR because KS-1318 and KS-1316 are the same file and
KS-1142 reads it; sequential PRs would each need a merged-blob equality
target on a file all three touch.

KS-1318 -- the combined default-shapes control asserted toHaveLength(3),
green under any permutation and under any relabelling that keeps the
cardinality. Now toEqual of the three tags in source order, the order
confirmed by measurement rather than assumed.

  ARM A, `return shapes.slice().sort()`:
    with the new assertion   1 red -- the combined cell ALONE
    with toHaveLength(3)     0 red -- the whole file green
  ARM B, the `export default function` branch emitting another tag:
    with the new assertion   2 red -- combined cell AND one per-shape row
    with toHaveLength(3)     1 red -- the combined cell stayed GREEN

Arm B is the finding verbatim: two shapes detected under one another's
name passed the old cell.

KS-1142 -- the same walk was pinned by two hand-maintained literals in
two files. K1's 27-package literal is hoisted to module scope and the new
K1b cell reads ks781's CORPUS from SOURCE TEXT (ks781 is a test file;
importing it would execute its suites), asserting its package set is a
SUBSET of K1's. Subset and not equality is deliberate and the cell says
why: CORPUS is a FILE list, K1 a PACKAGE list, and services/blockchain
and services/shared are guarded by K1 alone. Equality would red at the
tip and push someone to widen CORPUS, which is the opposite of the pin.
R-2 is kept and named in the cell title: K1 still reds on ordinary
growth by design.

  swap one CORPUS path's package for one K1 does not list -> K1b reds
  rename the CORPUS symbol so the parse finds nothing     -> K1b reds
  restored                                                -> 0 red

The second arm matters because [] is a subset of everything; both sides
assert non-empty first.

KS-1316 -- a guard DEFINED inside the parser continuation but never
CALLED read guarded: true. That over-reports, the unsafe direction.
Built as the gate's syntactic fix, NOT as a recorded limitation: whether
a nested FUNCTION EXPRESSION is invoked in the continuation's own body is
syntactic, even though general reachability is not. The walk no longer
descends into an uninvoked nested function expression.

  W9  guard in an uninvoked nested arrow      -> guarded false (was true)
  W10 the same arrow invoked by name          -> guarded true
  W11 an immediately-invoked arrow            -> guarded true
  W12 an arrow handed to a call               -> guarded true
  W13 a guard in a branch that never runs     -> guarded true, STILL NOT
      DECIDED and pinned as such

Under develop's walk with these cells present: exactly ONE red, W9. Every
control is green at both ends, so none is satisfied by a walk that merely
stopped entering nested arrows.

W11 caught a real defect in the first version of the walk: an IIFE parses
as a call whose callee is a PARENTHESIZED expression, so the invoked flag
did not survive the parentheses and the arrow read as a definition. W9
alone would have passed over it.

packages/shared 941/941 bare -> 947/947 patched (48 files, +6 = exactly
these cells), vitest run --no-file-parallelism in s-l7-ks781, at develop
4db87c3e4b98, load 17.67 bare / 10.00 patched. tsc -p . --noEmit rc 0.
No product file is touched; both files are under src/__tests__.

Refs KS-1318
Refs KS-1142
Refs KS-1316

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL7/raise/s-l7-ks781-a8e0fca70ed4-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL7/raise/s-l7-ks781-a8e0fca70ed4-push.out",
 "lines": 1300,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE \u2014 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-25T19:03:48Z PUSH START",
 "end": "2026-09-25T19:10:44Z push rc=0"
}
```

## #1270 KS-1275 (Seat B 29th, T3) — head 448b8b7fdd87a145acc895c4138811f34aa53c59

#1270 ticket line: #1270 is KS-1275.

### PR BODY (gh_body_1270.md) TEXT_SHA256 d436651b11933966dcd1d9da1294bae15843b7a5cc1b9fa5fc6fa8ffd5ac32f0

#1270 KS-1275: point the lifecycle verb prose at LIFECYCLE_EVENT_ACTIONS
head 448b8b7fdd87a145acc895c4138811f34aa53c59

## What

The two comment sites #1252 left behind on KS-1275. Both hand-enumerated the accepted lifecycle verbs and both had drifted; they now point at the same two sources of truth the published description does, and name no verb at all.

- `services/originate/src/repositories/lifecycleEventRepo.ts:5-8` — named four verbs plus the KS-389 mapping, and omitted `share-attach-consent` (KS-534), `protect`/`unprotect` (KS-556) and the KS-1172/KS-1173 additions.
- `services/originate/src/routes/documents.ts:2428-2432` — named those four **plus** the KS-415/PS-235 share-edit four.

So the two prose sites had drifted apart from **each other**, not only from the enum. Pointing both at `LIFECYCLE_EVENT_ACTIONS` and `docs/VOCABULARY.md` closes both drifts at once, as #1252 did for the published description.

`migrations/037` is an applied migration and is untouched.

## Test Evidence

**Touched:** `services/originate/src/repositories/lifecycleEventRepo.ts`, `services/originate/src/routes/documents.ts`. Comment lines only.

**Ran** — all in `worktrees/s-b29-ks1275` at develop `4db87c3e4b98`, `packages/shared` BUILT (88 dist files), `npx jest --runInBand` in `services/originate`:

| arm | result |
|---|---|
| originate BARE (pre-edit files restored, sha256-verified) | **878 passed / 878, 74 suites**, rc 0 |
| originate PATCHED (this commit, sha256-verified restore) | **878 passed / 878, 74 suites**, rc 0 |
| `tsc --noEmit` BARE | rc 0 |
| `tsc --noEmit` PATCHED | rc 0 |

Identical readings either side, which is what a comment-only change must produce — and the BARE arm is what makes that a measurement rather than an assumption. Both restores were asserted by sha256 against the pre-tamper hashes, by content, never `git checkout`.

**AST-equivalence, with a control that fires.** Both files transpiled with `removeComments: true` (typescript 5.9.3) and the emitted JavaScript compared:

```
EQUIVALENT  emit 3155 vs 3155 bytes   diag 0/0  lifecycleEventRepo.ts
EQUIVALENT  emit 89849 vs 89849 bytes diag 0/0  documents.ts
```

CONTROL: a **one-character** change to a numeric literal inside a template literal (`LIMIT 1` -> `LIMIT 9`) reads `DIFFERENT` **at an identical emit size of 3155 bytes**, and the tool names the divergent line. So "EQUIVALENT at the same byte count" is not a vacuous pass — this is precisely the case a raw token scan misses, because it swallows comments into one template-literal token.

**Also asserted:** none of the seven removed verb names survives in either file (7 x 2 greps, all 0), against a control showing `LIFECYCLE_EVENT_ACTIONS` present 4 times in `documents.ts` so the greps work.

**NOT run / NOT covered:**
- **Legs 3, 4 and 8 NOT run** (local stack not up). `11/15 ran; legs 3, 4, 8 NOT run (local stack not up)`. No spec moves in this PR, so there is no LEG-8-PORT reading to give.
- `packages/shared` was run on the sibling head in this batch, not separately here; this PR touches no source its text-scanning guards read differently (comments only).
- No runtime behaviour is exercised, because none changes. The claim this PR makes is exactly "the emitted JavaScript is unchanged", and that is the thing measured.

Refs KS-1275

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Base attribution for the counts above (per the 19:30Z fleet correction)

develop moved to `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9` at 19:20Z, **after** this PR was built and pushed. **This worktree does not contain it** — the object is not present in the checkout at all, because no fetch was taken: `git cat-file -t d7cdecf1d2ee` fails here, against a positive control where `git cat-file -t 4db87c3e4b98` returns `commit`. The worktree base is `4db87c3e4b98` (`HEAD~1`).

So every count in this PR measures **`4db87c3e4b98` + this change**. The push gate read `pre_push_hook_base` **28/0**, `fixture_guard` **6/0**, `run_shell_suites` **49/0**, shell suites **60 passed / 0 failed of 60**, `^FIXTURE BUILD FAILED` **0** — the same quadruple the fleet declaration names for `d7cdecf1`, but **this is not a confirmation of it**: a pre-merge worktree reading the old quadruple is the old tree agreeing with itself.

Nothing about the comment-only claim depends on the base: the AST-equivalence proof is about the two files' emitted output.


### HEAD COMMIT MESSAGE TEXT_SHA256 10289813e0f83e0f2cb2bebed4e2657cb9f5604e287591421f79d569a8593add

KS-1275: point the lifecycle verb prose at LIFECYCLE_EVENT_ACTIONS

The two comment sites #1252 left behind. Both hand-enumerated the accepted
lifecycle verbs and both had drifted; they now point at the same two sources of
truth the published description does, and name no verb at all.

lifecycleEventRepo.ts named four verbs plus the KS-389 mapping and omitted
share-attach-consent (KS-534), protect/unprotect (KS-556) and the KS-1172/KS-1173
additions. The documents.ts route header named those four plus the KS-415/PS-235
share-edit four, so the two prose sites had also drifted apart from each other,
not only from the enum. Pointing both at LIFECYCLE_EVENT_ACTIONS and
docs/VOCABULARY.md closes both drifts at once.

Comment-only. Proven by emitting both files with removeComments and comparing:
EQUIVALENT at 3155 and 89849 bytes, 0 diagnostics. The control fires — a
one-character change inside a template literal reads DIFFERENT at an identical
emit size, which is the case a raw token scan misses.

migrations/037 is an applied migration and is untouched.

Refs KS-1275

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-29th/raise/s-b29-ks1275-448b8b7fdd87-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-29th/raise/s-b29-ks1275-448b8b7fdd87-push.out",
 "lines": 1300,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE \u2014 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-25T19:17:59Z PUSH START",
 "end": "2026-09-25T19:24:44Z push rc=0"
}
```

## #1271 KS-1164 (Seat L7, T2) — head c9ea1dc1705f10f4b40ccc786604da6768a2c2fb

#1271 ticket line: #1271 is KS-1164.

### PR BODY (gh_body_1271.md) TEXT_SHA256 0572784f369ef606173cf759b33511d07d4fb72b4f8dc9b2ac523b54128016e2

#1271 KS-1164: refuse the gate report when it would overwrite its own input, and the k6-log sibling
head c9ea1dc1705f10f4b40ccc786604da6768a2c2fb

## BLUF

`#1200` closed KS-1164's original class by deriving `reportPath` from the directory plus the scenario. **One input still collided with its own output:** a `--summary` whose basename already **is** `<scenario>-gate-report.json`. The derivation then reconstructs the input path exactly and the write destroys the run's only raw record — **with the log line still saying "Gate report written"**. Refused now, and the `k6_docker.ts` sibling is **handled, not recorded as accepted**.

`Refs KS-1164`

## The harm, measured both ways on a disposable temp dir

| | `threw` | input preserved | sha256 | keys afterwards |
|---|---|---|---|---|
| **unguarded** | `null` | **false** | `b87e0456d90c` → `b1f666f7967c` | `scenario,slot,slotTag,gatewayPort,runLabel,timestamp,passed,results` — **the `metrics` map is gone** |
| **guarded** | the named error | **true** | `b87e0456d90c` unchanged | `metrics` |

**Refusal rather than a suffix.** This is the by-hand re-gate path; a silent suffix writes a file nobody is looking for, and a throw cannot be mistaken for success. Both sides are `path.resolve()`d, so a non-canonical spelling of the same file is caught too.

## The sibling is handled, and the extraction is why it can be pinned

`runner/k6_docker.ts` derived the k6 log path with the same `.replace(/-summary\.json$/, …)`, a **no-op** on a non-conforming name, so the log path collapsed onto the summary mount and k6 would write its log over the summary it was producing.

The derivation is extracted to an exported `k6LogMountFor(summaryMount)`. **Calling `runK6` to test the guard is not an option:** the path that does *not* throw continues to `spawnSync('docker', …)`, and a unit suite must not start a container — my holds forbid it outright. A guard nothing can exercise is a guard a later edit removes silently.

## Red-proof, re-run against the FINAL bytes

The first proofs ran before three lint fixes changed these files, so they were re-run afterwards rather than quoted from the draft.

| arm | result |
|---|---|
| `gate/report.ts` guard removed | **S1 RED · S2 RED** · S3 green · both pre-existing cells green |
| `k6_docker.ts` guard removed | **L1 RED · L3 RED** · L2 green |

Both products restored **byte-identical** after each arm (`diff -q`).

**S3 and L2 exist because a refusal-only proof is indistinguishable from a function that always throws** — each asserts the guard still lets a legitimate call through.

## Three things lint caught that I had not

1. The extracted helper landed **between `runK6`'s JSDoc and `runK6`**, leaving `runK6` undocumented and the helper carrying two doc blocks. Moved above.
2. `writeGateReport`'s JSDoc had no `@throws` for the new refusal.
3. Three arrow shorthands returning a void expression in the test file.

## And one my own fixture caught

S2's "non-canonical" path was built with `path.join`, which **normalises** — so it came out byte-equal to the plain path and the cell would have proved nothing. Its own precondition assertion failed rather than passing vacuously. Rebuilt by concatenation.

## Test Evidence

**Touched**
- `systemTest/performance/gate/report.ts` — the SAMEPATH refusal + `@throws`.
- `systemTest/performance/runner/k6_docker.ts` — `k6LogMountFor` extracted and guarded.
- `tests/unit/gate/ks1164-write-gate-report-never-overwrites-its-input.test.ts` — cells S1–S3.
- `tests/unit/runner/ks1164-k6-log-mount-never-collides.test.ts` — **new**, cells L1–L3.

**Ran**
- `npm run test:unit` in `s-l7-ks1164/systemTest/performance`, at develop `4db87c3e4b98`: **1104/1104 bare → 1110/1110 patched**, 64 files, **+6 = exactly S1–S3 and L1–L3**. Load **12.38** bare / **7.10** patched. Baseline before any edit on a clean tree.
- `npm run lint` → **rc 0**: `tsc -p tsconfig.json`, `tsc -p tsconfig.node.json`, and `eslint`.
- Both red-proof arms above, each asserting the guard text was actually removed before running.

**NOT run**
- **No preflight.** `systemTest/` path, and the hook gates on `^Blockchain/Dev/` — the push took 12 s and only the format gate ran (1 package, 0 failed). **The fleet STOP count was never executed and none is quoted.**
- **No k6 run and no docker run of the k6 image** — that is precisely why `k6LogMountFor` was extracted rather than tested through `runK6`.
- **`runK6`'s own call site is not exercised.** L1–L3 pin the helper; that the helper is *wired into* `runK6` is asserted by nothing here beyond the type checker. Stated rather than left implicit.
- The original `-summary.json`-suffix class is `#1200`'s and is untouched; its two cells still pass.

**Migrations + config**
- **None.** No migration, schema, runtime config, `package.json`, lockfile, Dockerfile, route or OpenAPI surface.

## Note for the reviewer

The refusal is a **behaviour change on a documented CLI flag**: `--summary <dir>/<scenario>-gate-report.json` used to "work" and now throws. It was silently destroying its input, so the old behaviour has no users worth preserving — but it is a change, not only a test addition, and it belongs in the release note rather than being discovered.



### HEAD COMMIT MESSAGE TEXT_SHA256 dbe001888e8256da8f0f5bade31b87b702bc814e62eec961fd14cfc52ce1ed48

KS-1164: refuse the gate report when it would overwrite its own input, and the k6-log sibling

#1200 derived reportPath from the directory plus the scenario instead of
from the summary basename, which closed the original class. One input
still collided with its own output: a --summary whose basename already IS
`<scenario>-gate-report.json`. The derivation then reconstructs the input
path exactly.

MEASURED, both ways, on a disposable temp dir:

  unguarded  threw null | preserved FALSE | sha b87e0456d90c -> b1f666f7967c
             keys become scenario,slot,slotTag,... -- the metrics map is
             GONE, and stdout still says "Gate report written"
  guarded    throws the named error | preserved TRUE | sha unchanged
             keys still `metrics`

Refusal rather than a suffix: this is the by-hand re-gate path, a silent
suffix writes a file nobody is looking for, and a throw cannot be
mistaken for success. Both sides are path.resolve()d, so a non-canonical
spelling of the same file is caught too.

THE SIBLING IS HANDLED, NOT RECORDED AS ACCEPTED. runner/k6_docker.ts
derived the k6 log path with the same `.replace(/-summary\.json$/, ...)`,
a NO-OP on a non-conforming name, so the log collapsed onto the summary
mount. The derivation is EXTRACTED to an exported `k6LogMountFor` so the
guard can be pinned at all: calling runK6 to test it is not an option,
because the path that does NOT throw continues to spawnSync('docker'),
and a unit suite must not start a container. A guard nothing can
exercise is a guard a later edit removes silently.

Red-proof, re-run against the FINAL bytes after the lint fixes, not only
against the first draft:

  guard removed, gate      S1 RED  S2 RED  S3 green, both older cells green
  guard removed, sibling   L1 RED  L3 RED  L2 green

Both products restored byte-identical after each arm.

Three things lint caught that I had not:
  - the extracted helper landed BETWEEN runK6's JSDoc and runK6, leaving
    runK6 undocumented and the helper with two doc blocks. Moved above.
  - writeGateReport's JSDoc had no @throws for the new refusal.
  - three arrow shorthands returning a void expression in the test file.

And one my own fixture caught: S2's "non-canonical" path was built with
path.join, which NORMALISES, so it came out byte-equal to the plain path
and the cell proved nothing. Its own precondition assertion failed rather
than passing vacuously. Built by concatenation instead.

systemTest/performance 1104/1104 bare -> 1110/1110 patched (64 files, +6
= S1-S3 and L1-L3), `npm run test:unit` in s-l7-ks1164, at develop
4db87c3e4b98, load 12.38 bare / 7.10 patched. `npm run lint` rc 0 -- both
tsconfigs and eslint.

Refs KS-1164

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL7/raise/s-l7-ks1164-c9ea1dc1705f-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL7/raise/s-l7-ks1164-c9ea1dc1705f-push.out",
 "lines": 11,
 "pre_push_hook_base": "NOT FOUND",
 "fixture_guard": "NOT FOUND",
 "run_shell_suites_region": "NOT FOUND",
 "run_shell_suites_prefixed": "NOT FOUND",
 "shell_suites": "NOT FOUND",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "NONE",
 "preflight_ran": false,
 "rc": "0",
 "start": "2026-09-25T19:32:17Z PUSH START",
 "end": "2026-09-25T19:32:29Z push rc=0"
}
```

## #1273 KS-1321 (Seat B 29th, T2) — head b800791a3295f048b40f920435b080a270c65106

#1273 ticket line: #1273 is KS-1321.

### PR BODY (gh_body_1273.md) TEXT_SHA256 5115d6777e3f5a7e8fa6c4da8b0346b297bd8448b7e0c218afac6d1b823ac1d5

#1273 KS-1321: match the description verb on a word boundary, not a bare includes
head b800791a3295f048b40f920435b080a270c65106

## What

`DESCRIPTIONPOINTSATSOURCE` (landed by #1252) forbade a dedicated-route verb appearing in the published `LifecycleEventRequest.action` description by **substring** match: `dedicatedVerbs.filter((verb) => description.includes(verb))`. Several of those verbs are ordinary English words — `anchor`, `revoke`, `share`, `verify`, `version` — so the check could refuse innocent prose while proving nothing about a real relabel.

**Measured on the three descriptions the ticket names**, and this is in the GREEN cell as its own conjunct: `"a new version of this list"`, a back-quoted `` `version` ``, and a slash-delimited `/version` all return `["version"]` from the bare `includes()`. **All three, identically** — so the old check could not discriminate them at all. It reds today on nothing, because the live description happens to contain no verb substring; the widening was latent.

## The rule, and why each branch is the width it is

- a **hyphenated** verb (`sig-json`, `sign-cert`, `sign-wallet`, `transfer-custody`) cannot occur as ordinary English, so a word-boundary match is enough and nothing is given up;
- a **single-word** verb counts only in **route-token** form: back-quoted, or slash-delimited on either side.

**The `verb/` form is in that rule because of a measurement, not by symmetry.** With only `/verb`, the historical inline list `share/transfer-custody/revoke` returned `['revoke','transfer-custody']` and **missed `share`** — the one term with no slash in front of it. The list still reddened the cell, so the guard was working; but a rule that can only see the tail of a list is not describing the shape it refuses. An arm of mine whose *expected value* was wrong is what surfaced it, and the expectation was the wrong thing to correct.

**What the rule still does NOT catch is stated in the code, not left implied:** a single-word verb written as bare prose with no delimiter (`"share must use its own route"`). That is inherent to the fix the ticket asks for — `version` in "a new version" is the same string as the verb, and only the delimiter tells them apart. The hyphenated verbs have no such ambiguity, which is why their branch exists.

## Test Evidence

**Touched:** `services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts` (test-only).

**Ran** — `worktrees/s-b29-ks1321` at develop `4db87c3e4b98`, `packages/shared` BUILT (88 dist files):

| arm | result |
|---|---|
| originate BARE, `npx jest --runInBand` in `services/originate` | **878 passed / 878, 74 suites**, rc 0 |
| originate PATCHED, same command | **880 passed / 880, 74 suites**, rc 0 (+2 cells) |
| `ks978` file alone, BARE | 13 passed / 13 |
| `ks978` file alone, PATCHED | 15 passed / 15 |
| `packages/shared`, `npx vitest run` | **941 passed / 941, 48 files**, rc 0 |
| `tsc --noEmit` in `services/originate` | rc 0 |

`packages/shared` is run because its guard suites read originate sources by TEXT. Both restores between arms were asserted by sha256.

**Red-proved one conjunct per arm, six arms, each reddening EXACTLY the named cell (14 passed / 1 failed each):**

| arm | conjunct falsified | cell that reds |
|---|---|---|
| C1 | the helper reverts to the bare `includes` | ORDINARYWORDSTAYSGREEN |
| C2 | the `verb/` alternative dropped (the list's FIRST term) | ROUTETOKENSTILLREDS |
| C3 | the back-quoted alternative dropped | ROUTETOKENSTILLREDS |
| C4 | the `/verb` alternative dropped | ROUTETOKENSTILLREDS |
| C5 | the hyphenated branch removed | ROUTETOKENSTILLREDS |
| C6 | the non-vacuity conjunct: the registry read yields NO verbs | ORDINARYWORDSTAYSGREEN |

Three instrument rules in the runner, each from a recorded failure: every tamper asserts its anchor is **unique** and stops the run otherwise; every arm names the cell it expects and FAILS if a different cell reds **or none does**; verdicts are read from `--json` `fullName`, never the console line.

**Two defects in my own runner, found by running it:**
1. **`C5` applied and was INERT.** Removing the hyphenated branch changed nothing, because every fixture's hyphenated verb was *also* slash-delimited and the single-word rule already caught it. A tamper that finds nothing is a statement about the fixtures, not the product — so a discriminating fixture was added (`"A transfer-custody must use its own route."`, hyphenated in **bare prose**), which is the only case that branch is needed for. C5 is now a real arm and the branch is proven load-bearing.
2. **`C6` returned 0 passed / 0 failed** — the suite never compiled (an unused parameter), which reds nothing and is indistinguishable from an inert tamper if only the failed set is read. The runner now treats `0 passed and 0 failed` as its own `LOADFAIL` verdict rather than a silent miss.

**NOT run / NOT covered:**
- **Legs 3, 4 and 8 NOT run** (local stack not up): `11/15 ran; legs 3, 4, 8 NOT run (local stack not up)`. No spec moves in this PR, so there is no LEG-8-PORT reading.
- The ticket's title says `ks1293/ks978`; the `ks1293` file is #1261's and is not on develop, so **only `ks978` is touched** here.
- The rule's uncaught case (a bare, undelimited single-word verb) is **not** covered by a cell, because no fixture can distinguish it from prose. It is recorded in the code instead.

Refs KS-1321

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Base attribution for the counts above (per the 19:30Z fleet correction)

**This worktree does NOT contain develop `d7cdecf1d2ee`**, and the object is not even present in the checkout — no fetch was taken. Measured: `git cat-file -t d7cdecf1d2ee` fails here, against a positive control where `git cat-file -t 4db87c3e4b98` returns `commit`. The worktree base is `4db87c3e4b98` (`HEAD~1`).

So every count in this PR measures **`4db87c3e4b98` + this change**, not the combined tree with `d7cdecf1d2ee`. The push gate read `pre_push_hook_base` **28/0**, `fixture_guard` **6/0**, `run_shell_suites` **49/0**, shell suites **60 passed / 0 failed of 60**, and `^FIXTURE BUILD FAILED` **0 times** — the same quadruple the fleet declaration names for `d7cdecf1`, but **this is not a confirmation of it**: a pre-merge worktree reading the old quadruple is the old tree agreeing with itself. Stated as attribution, not as evidence about develop.



### HEAD COMMIT MESSAGE TEXT_SHA256 b51fb489c51399f58aa6933eec12eb640ea085758c673b91d6ade683e95826d3

KS-1321: match the description verb on a word boundary, not a bare includes

DESCRIPTIONPOINTSATSOURCE forbade a dedicated-route verb in the published
LifecycleEventRequest.action description by substring match. Several of those
verbs are ordinary English words — anchor, revoke, share, verify, version — so
the check could refuse innocent prose while proving nothing about a real relabel.

Measured on the three descriptions the ticket names: "a new version of this
list", a back-quoted `version`, and a slash-delimited /version. The bare
includes() returns ["version"] for ALL THREE, so it could not discriminate them
at all. That measurement is in the GREEN cell as its third conjunct.

The rule now has two branches, each as wide as it can honestly be. A hyphenated
verb cannot occur as ordinary English, so a word boundary is enough. A
single-word verb counts only in route-token form: back-quoted, or slash-delimited
on either side.

The verb/ form is in that rule because of a measurement, not by symmetry. With
only /verb, the historical inline list share/transfer-custody/revoke returned
['revoke','transfer-custody'] and missed share — the one term with no slash in
front of it. The list still reddened the cell, so the guard was working, but a
rule that can only see the tail of a list is not describing the shape it
refuses. An arm of mine whose expected value was wrong found it; the expectation
was the wrong thing to correct.

What the rule still does NOT catch is stated in the code rather than left
implied: a single-word verb as bare prose with no delimiter. That is inherent to
the fix the ticket asks for — "version" in "a new version" is the same string as
the verb, and only the delimiter tells them apart.

Both done-when arms are cells. originate 878 -> 880, one cell each.

Refs KS-1321

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-29th/raise/s-b29-ks1321-b800791a3295-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-29th/raise/s-b29-ks1321-b800791a3295-push.out",
 "lines": 1300,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE \u2014 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-25T19:32:34Z PUSH START",
 "end": "2026-09-25T19:40:16Z push rc=0"
}
```

## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatL8-2026-09-26.md TEXT_SHA256 cb7e9abe4a735acdf95b8e33017e30235137e99c714c7b11d9768f8272830584

# HANDOVER — Seat L8, pane `Secuura/Blockchain-D`, round 25 (small-services lane)

**Written to be read COLD.** Lane: `services/vc-issuer`, `services/kyc`, `services/demo-service`,
`services/m365-integration` — four services no other round-25 seat touches.

**Nothing merged by me. Nothing deployed. No ticket state moved.**

---

## 1. Where things stand

| # | Ticket | PR | Head | State |
|---|---|---|---|---|
| 1 | KS-1281 | **#1264** | `2e95121dfc475a09c81d61d61f9a81148b6bb0b9` | READY FOR QA |
| 2 | KS-1120 | **#1266** | `952f4329de97cd7f94ab6363e670248c456d0a54` | READY FOR QA |
| 3 | KS-1295 | **#1267** | `71f6f4d73cbde5b32f1564c9171eb1b705f77880` | READY FOR QA |
| 4 | KS-1182 | **#1269** | `df21c6fd159f2a707d698e418946911f019ca9a0` | READY FOR QA |
| 5 | KS-849  | (see §6) | `34980b8e9ee22a36c658a03d9d763c48caeb9064` | pushed / PR per §6 |
| 6 | KS-934  | (see §6) | `1a37bde12d55563f77e192519ca7db62461dbf6f` | committed, push per §6 |

**Filed:** **KS-1327** (KS-849 residual — the whole-row read-modify-write class) and **KS-1328**
(kyc `db.retry.test.ts` exceeding vitest's 5 s default under fleet load). Both Backlog, both with
the board searched first and controls that fire.

**Every ticket left In Progress / Backlog as found.** I moved no ticket state.

---

## 2. The base, and why the figures still stand

All figures were measured at develop **`4db87c3e4b98`**. develop has since moved to
**`d7cdecf1d2ee`** (Seat M1's merges). Measured via the compare API rather than a fetch, so no ref
write was made in the shared checkout: **5 commits, 6 files, ZERO in my lane**, against a control
prefix that fires. `packages/shared` also untouched.

So the figures remain true of what they measured, and the PR bodies name `4db87c3e4b98` honestly.
**They are not restated as current.** If a gate wants them on the new tip, they must be re-run.

⚠ **Two of those six files are preflight shell suites**
(`scripts/__tests__/run_migrations_failure_exit_code.test.sh`,
`scripts/__tests__/no_tracked_credentials_root.test.sh`). My first four pushes all read
`run_shell_suites` **49/0** and shell suites **60/0 of 60** — measured BEFORE that merge. A seat that
now sees different numbers should check this cause before calling a STOP; the brief already says the
coordinator re-declares the count after such a merge.

---

## 3. What each change is, in one line

1. **KS-1281** — comment-only. `credentialRepo.ts:8`/`:24` no longer claim the table is
   "auto-created"; #1231 removed the runtime DDL. AST-equivalence proven with a control.
2. **KS-1120** — two test cells (X1, X2) pinning the memory PREFIX class and the DB-miss to
   memory-get fallback. Test-only; no product file touched.
3. **KS-1295** — a WARN when `store()` keeps a credential in memory because the database is
   unavailable. `loadFromDb`'s identical early return is untouched; bare silent returns 2 -> 1.
4. **KS-1182** — the demo-service error handler: `headersSent` delegation, a 400-599 integer bound,
   `err.headers`, `expose`.
5. **KS-849** — both kyc mock timers re-read the verification before mutating it.
6. **KS-934** — `POST /api/teams/notify` gets a LIMIT, an aggregate deadline, and a per-call timeout
   no larger than the budget remaining; the un-attempted remainder is reported.

---

## 4. The four things I would most want the next seat to have

**A green suite is silent about files its corpus does not contain.** `packages/shared` read 941/941
on all six of my heads — which says nothing about my NEW test files until you prove the guard sees
them. I tampered my own file to bind `0.0.0.0`; the ks860 guard went red and named it by path and
line, then green again on restore. Only then was the 941/941 a statement about my work.

**A containment proof can pass by writing nothing at all.** My first merge25.py proof put both arms
in ONE scratch repo, uncontained first — so the object already existed, `merge-tree` wrote nothing
ANYWHERE, and shared delta 0 AND contained delta 0 both "passed". One FRESH repo per arm gives the
real answer: uncontained **+1**, contained **0 shared / +1 contained**, same predicted tree. This is
B 28th's recorded trap arriving in a different costume, which is the point: **knowing the lesson did
not stop me reproducing it.**

**A default that makes a factual claim is a hardcoded claim.** `merge24.py`'s `merge_note` DEFAULT
still asserted *"the author had already wrapped, so this is not the author merging their own PR"* —
false whenever a build seat merges its own PR, and it lands on develop permanently. B 28th NAMED
this class and closed only the seat-name half. Fixed in `merge25.py`: the default now states only
what the run itself verifies, and authorship must come from the addendum.

**A flat grep can miss a count that is right there.** `pre_push_hook_base` and `fixture_guard` read
"NOT FOUND" on my first pass because the summary line is INDENTED beneath a `=== <path> ===` header.
Re-anchoring on the headers found all four STOP counts. Parse by the header, never by a bare prefix.

---

## 5. Instruments and where they live

`5_Project_History/2026-09-26_seatL8/`
- `raise/` — `lock25.sh` (**proven 21/21**), `push25.sh` (**19/19**), `merge25.py` (re-keyed;
  containment proven two-sided, see `measurements/merge25-containment-proof.md`), `ast_equiv.cjs`,
  the two proof harnesses, `tamper_ks1120.py`, and every push log **named by head sha** (KS-1323).
- `measurements/` — every suite run, both arms of every red proof, the tamper JSON.

`push25.sh` re-keys that mattered: its two lock calls pointed at `lock24.sh` (would have dangled AT
THE LOCK TAKE); `PUSH24_*` -> `PUSH25_*`; logs named `$TAG-$HEAD_SHA-*` per KS-1323.

**`merge25.py` has never been used to merge.** It is proven for containment only.

---

## 6. Live at handover — read this before acting

**Five PRs are READY FOR QA. None is merged. Nothing is deployed.**

| PR | ticket | head | note |
|---|---|---|---|
| **#1264** | KS-1281 | `2e95121dfc475a09c81d61d61f9a81148b6bb0b9` | comment-only |
| **#1266** | KS-1120 | `952f4329de97cd7f94ab6363e670248c456d0a54` | test-only |
| **#1267** | KS-1295 | `71f6f4d73cbde5b32f1564c9171eb1b705f77880` | |
| **#1269** | KS-1182 | `df21c6fd159f2a707d698e418946911f019ca9a0` | |
| **#1272** | KS-849 | `34980b8e9ee22a36c658a03d9d763c48caeb9064` | |

**KS-934** is committed at `1a37bde12d55563f77e192519ca7db62461dbf6f` in `worktrees/s-l8-ks934`,
pushing at handover time. If its push did not complete, the branch is
`feature/ks-934-teams-notify-request-path-bound-l8r25-6` and it needs: push -> PR -> ticket comment.
Its PR body content is in the KS-934 commit message, which is written to carry it.

All five PRs verified `linkKind='contributes'` in Linear, so **none closes its ticket on merge**, and
every ticket reads In Progress or Backlog as found.

### The one outstanding job that is NOT mine but was accepted from the coordinator

Wednesday asked (19:30Z, DKIM verified) for the **fleet's d7cdecf1 preflight measurement**, because
her earlier "the first seat to push over it is the measurement" was wrong — a push measures its own
WORKTREE's base. The job, in order:

1. `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9` is **NOT present in the local object store** (verified,
   with a control). So it needs **one `git fetch origin develop` in `2_Project_Files`, taken under
   `.push-lock-25`** — the only ref write the brief permits there.
2. A throwaway worktree **detached** at that sha.
3. `npm ci` **and** `npm run build -w packages/shared` in it — a fresh worktree has no deps and the
   preflight's leg 1 refuses without them.
4. `bash scripts/preflight/preflight.sh`, **without pushing**.
5. Mail the four numbers **with `merge-base --is-ancestor d7cdecf1d2ee HEAD` stated**.
6. `git worktree remove` it — it holds no work.

**Expected (an expectation, NOT a measurement):** `pre_push_hook_base` 28/0 ·
`pre_push_hook_base_fixture_guard` 6/0 · `run_shell_suites` 49/0 · shell suites 60 of 60.
Corroborated two ways (gate24T2c's report; and all six changed files are `modified`, none `added`,
and none is a counted suite's own file). **If the measurement differs, that is news — do not explain
it away with the merge.**
For comparison, from my PRE-merge tree: `no_tracked_credentials_root.test.sh` **15/0** and
`run_migrations_failure_exit_code.test.sh` **5/0**; the merge added +31 and +77 lines to those files,
so both should read higher on d7cdecf1 while the four named counts hold.

### State of the shared checkout, measured at handover
`2_Project_Files` HEAD **`3bad652d17cf`**, **17 untracked / 0 modified** — byte-identical to boot.
I never pulled, fetched, committed or checked out there; the only writes were `worktree add` in my
own `s-l8-*` namespace, each measured at **0 lines of change to the shared `.git/config`**.

### Parse push logs by BOUNDED REGION, not by prefix
A push log carries **two** summary forms — prefixed (`run_shell_suites: 49 passed, 0 failed`, 28
occurrences) and indented under a `=== <path> ===` header (26 occurrences). A parser anchored on
either alone under-reports, and an under-reported STOP count reads as a missing gate rather than a
parser bug. Bound each suite's region **between consecutive `=== … ===` headers** and take the
summary inside it; that is form-agnostic and immune to the neighbouring-summary trap.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL8/measurements/fleet-measurement-RESULT-d7cdecf1.md TEXT_SHA256 a4c421c21ef366bfca8c8c580c187edd16433d0f2bf2d5e306d162fe6de7f576

# FLEET MEASUREMENT — preflight on the COMBINED tree d7cdecf1 (Seat L8, 2026-09-26)

Run at Wednesday's request (19:30Z ANSWER), because her 19:27Z declaration's line
"the first seat to push over it is the measurement" was wrong — a push measures its own
WORKTREE's base. This is the first tree that actually contains the merge.

**Base, stated per the new rule:** `merge-base --is-ancestor d7cdecf1d2ee HEAD` = **YES**.
HEAD = `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`, detached, throwaway worktree, **no push**.

## The four named counts — ALL MATCH the declaration

| count | measured | declared | |
|---|---|---|---|
| `pre_push_hook_base` | **28 / 0** | 28/0 | MATCH |
| `pre_push_hook_base_fixture_guard` | **6 / 0** | 6/0 | MATCH |
| `run_shell_suites` | **49 / 0** | 49/0 | MATCH |
| shell suites | **60 passed, 0 failed, 0 skipped (of 60)** | 60 of 60 | MATCH |

Zero lines starting `FIXTURE BUILD FAILED`. Preflight rc **0**;
`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` (legs 3, 4, 8 — local stack
not up). That verdict is not a pass and is not quoted as one.

**The expectation is now a measurement.**

## The tree is proven to be the combined one, not a stale checkout

Three independent signs, each measured rather than assumed:

1. `merge-base --is-ancestor d7cdecf1d2ee HEAD` = YES.
2. The two suites the merge modified are the POST-merge copies:
   `run_migrations_failure_exit_code.test.sh` **180 lines** (105 pre-merge) and
   `no_tracked_credentials_root.test.sh` **352 lines** (324 pre-merge) — matching the compare's
   +77 and +31 exactly.
3. Their CELL counts moved with the content — **both of them**:
   `run_migrations_failure_exit_code` **5/0 -> 7/0** (+2 cells, from +77 lines) and
   `no_tracked_credentials_root` **15/0 -> 16/0** (+1 cell, from +31 lines).
   So the new content really RAN; the suites were not merely present in the tree.

That third point is what makes the four unchanged counts meaningful rather than vacuous: the
preflight demonstrably executed changed content and still produced the same quadruple.

## Method notes
- `d7cdecf1` was ABSENT locally, so one `git fetch origin develop` was taken **under
  `.push-lock-25`** — the lock honoured this seat's own 90 s cool-off first, and was held
  **3 seconds** (19:48:39Z -> 19:48:42Z).
- The fetch disturbed nothing another session owns: shared checkout HEAD and the **local `develop`
  branch both still `3bad652d17cf`** (only `origin/develop`, a remote-tracking ref, advanced);
  working tree still 17 untracked / 0 modified; shared `.git/config` sha unchanged.
- Counts read by **bounded region** between consecutive `=== <path> ===` headers, because the log
  carries two summary forms and either parser alone under-reports.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatL7-2026-09-26.md TEXT_SHA256 9e6169ace278af641bb1a92ce34161a371c573e4712b17dbddd3d2252d78119b

# HANDOVER — Seat L7 (2026-09-26, round 25). Written to be read COLD.

## 1. WHERE THINGS STAND

**Queue COMPLETE: 7 of 7 items, 7 PRs, all READY FOR QA. Nothing merged. Nothing deployed. No ticket state moved by me.**

| PR | key(s) | head | family | gate |
|---|---|---|---|---|
| #1263 | KS-1140 | `3c33f936fe39` | packages/shared | preflight 12/15 · STOP 28/0 6/0 49/0 60/60 |
| #1265 | KS-1315 | `87ef6a1b0887` | systemTest/performance | **no preflight** · format gate only |
| #1268 | KS-1318 + KS-1142 + KS-1316 | `a8e0fca70ed4` | packages/shared | preflight 12/15 · STOP all match |
| #1271 | KS-1164 | `c9ea1dc1705f` | systemTest/performance | **no preflight** |
| #1275 | KS-1179 | `d852e56b912f` | packages/shared | preflight 12/15 · STOP all match |
| #1277 | KS-1319 | `702171eaadbe` | packages/shared | preflight 12/15 · STOP all match |
| #1278 | KS-1314 | `c321bcce2a9a` | systemTest/performance | **no preflight** |

**Every one is branched from `4db87c3e4b98`.** develop is `d7cdecf1d2ee` and no worktree of mine contains it, so **every STOP count above describes `4db87c3e4b98` + that change** — not the combined tree. Mailed as COUNT ATTRIBUTION 19:4xZ.

**Ticket filed: KS-1329** — "packages/shared does not type-check `src/__tests__`, hiding 10 errors". Carries the full error table, the probe method, every control note, and the three ks781 errors marked "after #1268 merges".

**Shared checkout `2_Project_Files`: HEAD `3bad652d17cf`, 17 `??` / 0 non-`??` at boot AND at wrap, byte-identical.** No pull, no fetch, no commit there all session. Shared `.git/config` carries **0** lines with my token `l7r25`.

## 2. THE THING TO INHERIT — my harness failed the same way the code does, four times

Every one was caught by a control, never by reading the code. **The pattern: an arm that can only come out red proves nothing. You need the arm that comes out GREEN.**

1. **A control that reds for the wrong reason.** KS-1319's second arm was meant to show the OLD wiring check stayed green under a comment-out. I left my new assertions in the cell beside the old ones, so it reddened either way. Re-run isolated, the old check was **7/7 fully green** — which is the entire finding.
2. **An instrument that cannot see its subject.** A regex extracting "string literals" matched backticks **inside comments**, reporting 138 -> 155 literals for a comment-only edit. Replaced by an emit comparison (`removeComments`, compare bytes).
3. **A probe whose config invented the answer.** The typecheck probe reported 24 errors, then 2, then 10 across three configs. Only a **planted** error settled which was real — and my first read of that control grepped for the VARIABLE NAME when tsc prints the FILE and LINE.
4. **A control that never fired.** A `sed`-based syntax check used GNU syntax on BSD sed, so the tamper never applied and "rc 0" meant nothing.

## 3. A GUARD THAT COULD NOT FAIL, AND HOW IT LOOKED FINE

KS-1319's wiring cell read the config's **source text** for `setupFiles`. `//` does not remove a string. The budget could be unhooked entirely and the cell stayed green. It now **imports** the config and reads the resolved value.

**The general shape: any check that reads source TEXT for a setting is satisfied by that setting commented out.** Grep the repo for `toContain('` against a config file and you will find the next one.

## 4. MEASURE BEFORE BUILDING — three tickets were wrong about their own subject

- **KS-1179 / F-5:** the ticket and the ruling both asked me to correct a docblock. **It was already correct**, fixed in an earlier round with the record left in the file. I changed nothing.
- **KS-1179 / N1:** a comment claimed an `isIP` throw made a cleanup path "live". **`net.isIP` does not throw** — `'x'`, `''`, `null`, `undefined`, `123` all return 0. The path is reachable only under a mock.
- **KS-1314 / item 1:** my first "wrapped import" fixture was 99 characters and **prettier left it on one line**. `printWidth` here is 120. A hand-written wrapped import pins a shape prettier never emits — capture it.

## 5. WHAT I RECORDED INSTEAD OF FIXING, AND WHY

- **TS2349 in `ssrf-guard.ts`.** Four shapes measured, each **relocated** the error: no cast -> TS2349; cast the callee -> TS2769; cast at the call site -> clean but the **emit changes**; assertion on the declaration -> TS2352. Only `as unknown as https.Agent` remained. **Refused:** in an SSRF guard a type the compiler stops checking is the risk to avoid. On KS-1329.
- **TS1343** (`import.meta`): 9 across the package, 4 in one other file. Fixing it here alone would drop `import.meta` in one file while eight keep it. On KS-1329.
- **The canary's per-run spawn** (KS-1314): **193 ms of the file's 220 ms**, and each alternative is worse — in-process needs a computed specifier (evading the suite's own guard to test it), a captured fixture stops being a live witness, and dropping the raw half leaves half a comparative claim.

## 6. THE CROSS-LANE CATCH

KS-1179's F-5 wanted the deadline error text at `ssrf-guard.ts:605` changed. Repo-wide search found **three** hits; two are **exact-string assertions in Seat B 29th's lane** (`services/originate/src/__tests__/ks914-deliver-webhook-blocked-vs-failed.test.ts:76` and `:86`). Changing it would have reddened another seat's suite mid-round. Ruled (c): docblock only, runtime string byte-identical.

**The proof that it stayed identical is the emit comparison, not a diff read:** pristine vs head **12,137 vs 12,137 bytes, 0 diagnostics**, with a control that reds on **one character** of that string. ks914's own cells: **16/16 green at my head**.

## 7. FOR WHOEVER SITS HERE NEXT

- **`ast_equiv.cjs` (copied from B 28th's folder) is the right instrument for "type-only" or "comment-only".** Type assertions and annotations erase at emit, so byte-identical output proves no runtime change AND no string change at once. Its control must red at an **identical emit size** — that is the case a token counter misses.
- **Re-run red-proofs after lint/prettier touches your files.** I had to on KS-1164 and KS-1314; the first pass was against bytes that no longer shipped.
- **`git merge-base --is-ancestor <sha> HEAD` fails identically for "not an ancestor" and "object not in the store".** If the sha is not local, the sound argument is the absence itself.
- **A `?? Blockchain/Dev/packages/shared/None/` directory** came from a python arm reading `os.environ.get('R')` with no default: `None` became a plausible PATH rather than an error. Check `git status` after any scripted run that writes a report.
- **Tools:** `2026-09-26_seatL7/raise/` — `lock25.sh` (10/10), `push25.sh` (8/8), `push25_ff.sh` (18/18), `seatreq25.sh` (8/8, my own LOCK_SEAT change), `containproof25.sh` (7/7, both sides + the read-back), `merge25.py` (never used — no GO arrived).
- **`merge25.py`'s `merge_note` is now REQUIRED** with no default. B 28th made `--seat` required and left the note optional, then omitted it and the inherited default asserted the opposite of their case. **A parameter whose default makes a factual claim is a hardcoded claim with extra steps.**

## 8. 🔴 THE FUSE — unchanged, and it is Kam's alone

**Both audit rows lapse `2026-09-30T00:00Z`, four days out.** From then `audit:gate` and `audit:locks` refuse **every** `Blockchain/Dev` push, from every author — that is #1263, #1268, #1275 and #1277 of mine. Legs 6 and 7 passed on all four. **It needs Kam's own word** — his typed line or mail with `dmarc=pass header.from=me.com`. A relay does not substitute. No open PR names KS-729. Nothing this round averted it.

## 9. RECORDS

`5_Project_History/2026-09-26_seatL7/raise/` — every tool, proof matrix, tamper arm, captured output, push log (named by head sha per KS-1323) and probe config.


