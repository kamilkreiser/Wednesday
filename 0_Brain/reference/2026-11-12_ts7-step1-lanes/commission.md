---
date: 2026-11-12
type: drafter-commission
client_project: Secuura/Blockchain (Platform K)
commissioned_by: Wednesday (11:1x rotation-successor seat)
model: sonnet (routing v1.0: drafter row)
---

# Commission: KS-1398 TypeScript 7 STEP ONE, partition into build lanes + draft lane 1's brief

## Authority (quote these, do not paraphrase)
- Kam, card `secuura-ks1398-typescript-7-move` = b, 2026-10-01 ("plan it now").
- Wednesday's plan to Kam on the panel 2026-11-12 11:06 ended: *"Nothing is built yet; say the word and I'll queue step one as build work."*
- Kam, live board 2026-11-12 11:09:41 (view=wednesday), verbatim: *"great. please go ahead"*. Receipt bf-19b1575e8d9e.
- STEP ONE = ORDER items 1-4 of `0_Brain/reference/2026-11-12_ks1398-ts7-measure-plan/report.md`: everything that ALSO works on TypeScript 5. **NO version flip (item 5) and nothing from item 6.**
- Design choice for ORDER item 2 (Wednesday's, under the 2026-10-27 design-inside-a-ruling grant): the 14 compiler-library files are **rewritten on a non-TypeScript parser** (works on TS 5, can land early). The `@typescript/typescript6` alias route is NOT taken.

## Read first, whole
1. `0_Brain/reference/2026-11-12_ks1398-ts7-measure-plan/report.md` (the plan; note its caveat: measured at 0e6479d7b, ~19 commits behind live develop).
2. The model of a stamped build brief: `0_Brain/reference/2026-11-12_drafter-seatA24/brief_A24.md` and its `commission.md` (shape, standing lines, HOLDS, provenance header).
3. `2_Project_Files/fleet/STANDING_LINES.md` and `2_Project_Files/fleet/specs/model-routing.md` (v1.0).
4. Linear KS-1398 (read-only; key from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env`, sourced in-process, never echoed): its description and EVERY comment (`comments(first:50)`, sort client-side).

## Measure at LIVE develop (read verbs only; never write into the project checkout)
- Live develop at commission: **697f422f1a39** (Wednesday's `git -C <checkout> ls-remote origin refs/heads/develop`, 11:1x). Re-read it yourself at the start; if it moved, use the new tip and say so.
- Use `git -C '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files' show <sha>:<path>` / `ls-tree` / `grep` (with the sha) for every file fact. NEVER `fetch`, `worktree add`, `checkout`, `merge-tree --write-tree` there (hard rule 1). If you need a working tree, `git clone --shared` into THIS folder's `scratch/` (gitignore it in the same action: add `0_Brain/reference/2026-11-12_ts7-step1-lanes/scratch/` to the WEDNESDAY `.gitignore` and confirm `git status` stays clean of it).
- Re-count at the live tip: the 14 compiler-library files (are they all still there; any new ones? grep for `from 'typescript'`, `require('typescript')`, `import ts`), the ts-node/ts-node-dev packages, the ts-jest users, the dead ts-jest devDependencies (referral, vc-issuer), the moduleResolution:node and baseUrl sites. Every count names its instrument and has a positive control.
- **Open PRs:** list every open PR's changed-file set (GitHub API read-only via the project's own identity is NOT yours: use `git -C <checkout> ls-remote origin 'refs/pull/*/head'` + `git -C <checkout> diff --name-only <develop>...<head>` only for heads whose objects exist locally; where they do not, say UNMEASURED and name the PR). A lane may not touch a file an open PR touches.

## Output 1: `lanes.md` (this folder)
- A partition of STEP ONE into build lanes that share NO file (and no package.json/lockfile: a lane owns a package's manifest + lock whole). For each lane: files/packages owned, the ORDER item(s) it covers, size estimate (files, lines, measured), test commands that prove it on TS 5 (green before AND after), the routing row (`model: <id from 0_Brain/dashboard/data/models_latest.json> -- <row> -- P1-P4`), and whether any part is Spark-briefable (one file, spelled-out fix, runnable test nearby, not security; the 14-file rewrite may qualify file by file).
- Suggested split to test against the measurement (change it if the files say otherwise): L1 = dead ts-jest removal (referral, vc-issuer) + ts-node/ts-node-dev -> tsx (6 packages); L2 = governance + tests/connectors -> Vitest; L3 = originate -> Vitest (largest; consider batching by directory into several rounds); L4 = the 14 compiler-library files rewritten on a non-TS parser; L5 = tsconfig cleanup (moduleResolution node16/bundler, drop baseUrl, add types) per package; L6 = oxlint beside ESLint then ESLint removal; L7 = sdk/javascript d.ts (tsconfig + lock + emitter). Order them so develop stays green and lanes that collide are sequenced, not parallel.
- A section NOT MEASURED, and a section QUESTIONS FOR WEDNESDAY (one line each).

## Output 2: `brief_L1.md` (this folder)
A complete build brief for lane L1 (or whichever lane `lanes.md` makes first), in the A24 brief's shape: addressed `Secuura/Blockchain-<LETTER>` with the lane letter left as `@LANE@` (Wednesday picks the free letter at stamping), a PROVENANCE block (every ticket key with its Linear read time and its SCOPE sentence quoted), the authority quotes above, HOLDS (no TS version change; no file outside the lane; tier-2 Sonnet QA gate then Wednesday's GO before any merge; client-facing words on tickets only; never delete — dead deps are removed from package.json by the normal edit, nothing else), the ends-at-READY-FOR-GATE line, and the test evidence required (suite counts before/after on TS 5). Ticket handling: KS-1398 is the parent; the brief tells the seat to file ONE child ticket per lane (aggregated, one logical path) unless one already exists (search first, by package name).

## Rules for you
- Read-only everywhere outside this folder. No mail, no Linear writes, no GitHub writes, no board posts.
- Never delete anything. Never run a write command to learn its usage.
- Every number carries its instrument; every absence carries a positive control.
- Finish with a 10-line summary as your final message: lanes (one line each), the first lane, what you could not measure.
