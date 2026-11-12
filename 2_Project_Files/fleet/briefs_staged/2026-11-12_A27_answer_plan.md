Seat A 27th

## BLUF
CONFIRMED with rulings: (a) EMITTER = tsup builds the JS + `tsc -p` writes the declarations, on tsup `^9.0.0` (your row g). (b) LOCK D GRANTED: tsup `^9.0.0` AND removal of the sdk's `eslint` devDependency, together with its dead `lint` script. (c) drop `--dts` from `dev`: GRANTED. (d) YES. (e) RELEASED. PACE: for this ONE row the stop-starting line is 60 and the ceiling 66; launch the push only at a reading of 58 or under, else your tripwire handover. Start the build now.

## Recommendation
No action needed beyond the plan with these rulings. Details below; the PR body must carry the two statements in item 3.

## Detail
1. (a) EMITTER, ruled: row g (tsup 9.0.0 JS-only + `tsc -p tsconfig.json` emitDeclarationOnly, the seven strict flags listed one by one, no `strict` key, no `target`). Reasons as you measured them: the only route that builds on TS 5.9.3 AND 7.0.2 without a second compiler package; `dist/index.js` and `dist/index.mjs` byte-equal to BEFORE (G2 holds); the 7 d.ts files hash-equal across 5.9.3 and 7.0.2. Accepted costs: seven declaration files instead of one bundled file, no `index.d.mts` (your node16-ESM consumer check passes). Re-measure the minimal tsconfig set in the worktree before relying on it, as you planned.
2. (b) LOCK D, ruled: `tsup ^9.0.0` and NO `eslint` devDependency (gate rc 0, 0 advisories, your scratch measurement D). Reasons: B, C and E each stay red; the minimatch advisory sits under eslint 10's own range with no patched 10.x; the only other road is two baseline rows, which are Kam's card and never a seat's. The sdk's `lint` script (`eslint src/`) is ALREADY non-functional (rc 2, no config in the package, the brief's measurement): REMOVE it with the devDependency, so nothing in the manifest calls a tool that is gone. Lint stays OUT of lane as a fix: restoring it (the repo's flat config at the Dev root, or a package config) is a CANDIDATE FILING in your READY, not work here.
3. The PR body MUST state, each as its own item: (i) "eslint devDependency and the non-functional lint script removed: the only non-baseline route to a passing audit:locks on the new lock (minimatch GHSA-g3hv-75wg-m249 via eslint 10, no patched 10.x); restoring lint is filed separately"; (ii) "tsup moved to ^9.0.0: clears esbuild GHSA-g7r4-m6w7-qqqr; tsup is now the JS bundler only". Quote the `audit:locks` line ("OK - no standalone-lock advisories ...") from the worktree.
4. (c) `dev` = `tsup src/index.ts --format cjs,esm --watch` (no `--dts`): GRANTED, its own line in the PR body.
5. (d) TS 7.0.2 measurements in session scratch only, re-run on the built package for the READY: YES.
6. PACE, ruled for this one row (the merge lane's precedent): stop-starting 60, ceiling 66; your tripwire becomes: if the reading is above 58 when you would launch the push, write the HANDOVER with every staged file and mail Wednesday, and a successor pushes. Say the reading in each STATUS.
7. Unchanged: no publish ever; no src/ or README edit; one child ticket of KS-1398 (quote Kam's 2026-10-01 'b' and 2026-11-12 11:09:41 words); KS-2136 folded in, Refs KS-2136, its own PR item.
