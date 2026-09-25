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

