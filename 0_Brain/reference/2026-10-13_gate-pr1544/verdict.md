# Gate verdict: Secuura Platform K PR #1544 (KS-1453, drop unused handlebars from originate; two lockfiles)
Report sha256/16: 2fe9d1a532cfbf3d
Gate: independent QA, Sonnet through-code tier 2. Findings only; nothing fixed, merged, pushed or written to GitHub/Linear/!CODING.

**Head under test: `2d604c089bf5f9524781230873866141a0b861e2`** (tree `cf394f9697be50a64cdd523e58fb30a42e9d62a0`), one commit, parent `29bb45342e6a65c047ed902aafeae6525529f150`.
Instrument for identity: `git ls-remote` on the project origin (read verb) and `git rev-parse` in my own scratchpad clone fetched from `git@github.com:Secuura/Distributed_Secuura.git refs/pull/1544/head`. Both shas and the tree matched the brief exactly.
**LIVE develop has moved** since the brief: it is now `49a41f3cb4a41d233671190b86f08c33627cd0a7` (2 newer commits, KS-1570 PR B and KS-759). See check 7.

## VERDICT: GO (no Major, 1 Minor). Bound to head 2d604c089bf5f9524781230873866141a0b861e2 only.

## Findings
- Major: none.
- Minor 1 (unreconciled number, harmless): the author's "root `npm ci --ignore-scripts` 1937 packages" did not reproduce. My count on the head's root lock: `added 1834 packages` (npm output) and 1866 entries in `node_modules/.package-lock.json`; rc=0. The 103/71 gap is most plausibly a different counting instrument (e.g. audited total incl. workspace links); I cannot tell which. It does not change any verdict-relevant fact (rc 0; handlebars present as dev). Fix: none needed; the PR body could name its instrument. Evidence: evidence/05_root_ci.log, 05_root_ci2.log.

## 1. Diff shape: FOUND / TESTED / HOW
- `git diff origin/develop...pr1544` (base 29bb453, the PR's own parent): exactly 3 files, `12 insertions(+), 3 deletions(-)`; numstat 6/1 + 6/1 + 0/1. No source file. Note actual paths are under `Blockchain/Dev/` (brief omitted that prefix): `Blockchain/Dev/package-lock.json`, `Blockchain/Dev/services/originate/package-lock.json`, `Blockchain/Dev/services/originate/package.json`.
- package.json change is exactly the one line `-    "handlebars": "^4.7.9",` (services/originate/package.json:26 on develop). Evidence: evidence/01_diff.txt, 01_fulldiff.patch.
- Control that can fail: I independently removed that line from develop's file with a regex (28 bytes removed) and `cmp`'d to the head's package.json: byte-identical.

## 2. Lock diff by parse
Instrument: my own node script (`lockdiff.js` in scratchpad/tools) that JSON-parses both locks and compares `packages` entry by entry. Output: evidence/02_lockparse.txt.
| lock | entries before/after | added | removed | version/resolved/integrity changes | flag changes |
|---|---|---|---|---|---|
| member `Blockchain/Dev/services/originate/package-lock.json` | 700/700 | 0 | 0 | 0 | 6 |
| root `Blockchain/Dev/package-lock.json` | 1970/1970 | 0 | 0 | 0 | 6 |
Flag changes (before -> after), all absent -> value:
- member: handlebars dev, minimist dev, neo-async dev, source-map dev, uglify-js dev (optional retained), wordwrap dev.
- root: same, except source-map `devOptional` (not `dev`).
Only other change: the dependency map of the originate package entry (`""` in member, `services/originate` in root) loses `handlebars`. This matches the author's list exactly.
Controls: (a) planted lock (express version changed, zod integrity changed, helmet flagged dev, ioredis deleted, a new package added) -> script reported all five (1 added, 1 removed, 2 value changes, 1 flag change); (b) a lock diffed against itself -> all zeros.

## 3. Rebuild the claim (byte-for-byte)
Instrument: `npx npm@11.19.0 install --package-lock-only --ignore-scripts` (npm reported 11.19.0) in isolated scratchpad copies, starting from develop (29bb453) with the one line removed (done independently, see check 1).
- Member lock regenerated in a standalone dir (package.json + lock only): `cmp` against head's member lock = IDENTICAL (sha256 e1a892aa...1594fb).
- Root lock regenerated in a full copy of the Blockchain/Dev tree: `cmp` against head's root lock = IDENTICAL (sha256 74045076...e9de).
- Controls: (a) unedited develop trees regenerated with the same command stay byte-identical to develop's own locks (idempotent, so the instrument is not rewriting churn); (b) the regenerated outputs differ from develop's (diff 14 lines in root), so the command did change something and `cmp` is capable of reporting a difference.
- JUDGEMENT on the two flags that differ from the plan wording: both are what npm itself writes (byte-identical to npm 11.19.0 output). `uglify-js` = `dev` + `optional`: the same pair appears in sibling locks (services/governance and services/originate, evidence/06_sibling_flags.txt). Root `source-map` = `devOptional`: the root workspace tree has a terser optional path; npm writes it, and a hand-written literal `dev` would be rewritten on the next install. Harmless to the image: the runner uses the member lock, where source-map is `dev`, and `--omit=dev` removes it (check 4).
- Not covered: other npm versions (only 11.19.0 tried; the Dockerfile base is node:24-alpine whose bundled npm I did not test).

## 4. Image reach
Instrument: `npm ci --ignore-scripts --omit=dev` (npm 11.19.0) from each member lock + package.json in separate dirs (matches Dockerfile line 79 `RUN npm ci --ignore-scripts --omit=dev`, services/originate/Dockerfile:79).
- develop lock (control): 343 packages; head lock: 337. Counted from `node_modules/.package-lock.json` keys.
- Exact set difference (`comm -3`): handlebars, minimist, neo-async, source-map, uglify-js, wordwrap. Nothing else. (evidence/04_setdiff.txt)
- Directory presence by `find` (any nesting): develop tree has all six (plus handlebars' own lib/dist dirs); head tree has none, so no nested copies.
- Dependency edges to the six from any remaining prod package: scanned 579 package.json files in the head prod tree for dependencies/optionalDependencies/peerDependencies naming any of the six: 0 edges. Control: same scan on the develop prod tree finds 5 edges (handlebars -> minimist, neo-async, wordwrap, source-map, optional uglify-js). (A plain text grep first showed 3 hits in validator/typescript/ipaddr.js; those are devDependencies or script text, not install edges.) No `require('handlebars')` / `from 'handlebars'` string in any file of the head prod tree.
- Runtime load: compiled originate with `tsc` from the head (rc 0), scanned all 53 compiled JS files: 17 distinct external packages required, handlebars among them? no. All resolve in the head's prod-only node_modules except `@secuura/shared`, which the Dockerfile symlinks to /shared (Dockerfile:88-89; same in the develop tree). Control: a planted `require('handlebars')` is reported missing against the head tree and found against the develop tree.
- Originate unit suite on the head (jest, in the root-installed workspace copy): Test Suites 105 passed / 105, Tests 1321 passed / 1321 (matches the author). Caveat: handlebars is present (dev) in that tree, so the suite does not itself prove absence; the prod-tree resolve scan above does that.
Evidence: 04_*.

## 5. Other consumers
- Root workspace `npm ci --ignore-scripts` from the head's root lock: rc 0 (run twice), handlebars installed as `dev:true`, required by ts-jest.
- Clean-room `npm ci --dry-run --ignore-scripts` of originate's standalone lock: rc 0. Control: a package.json with a planted extra dependency fails `npm ci` (rc 1, ETARGET), so the check can fail.
- `npm run audit:gate` (root, after building packages/shared): rc 0, "no advisories outside the triaged baseline", 7 baselined advisories listed.
- `npm run audit:locks` (run in a git work tree of the head, it needs one): rc 0, 43 standalone lockfiles, 7 advisories match, 7 baselined. (My first run outside a git tree failed rc 3 on `git rev-parse`; that is my setup, not the PR.)
- `npm run audit:contract` (the gate's own 59 tests incl. red-proofs): 59 pass, 0 fail. I did not plant a new advisory to see the gate go red myself; I rely on those red-proof tests.
- Not run: `check:openapi`, preflight legs (author reports 13/16 ran, 3 skipped, which is not a pass; I did not re-run preflight), shell suites.

## 6. Other references to handlebars
- `git grep -i handlebars` on the head over all tracked files except lockfiles: 0 hits (on develop: the single declaration line). So no overrides/resolutions entry, no Dockerfile, no doc, no audit-baseline.json mention, no KS-1452/KS-1453 text outside the commit. 0 `*.hbs`/`*.handlebars` files. Non-literal require/import in originate src: the grep returned two COMMENT lines only (uuid-cjs.ts:8, and a test comment at ks1402...test.ts:83). Control: express is imported in 91 originate files (grep instrument works).
- Other standalone locks (governance, referral, vc-issuer, originate, root) all now show handlebars `dev:true` required only by ts-jest, i.e. originate is now consistent with its siblings (evidence/06_handlebars_other_locks.txt).

## 7. Merge and commit message
- `git merge-tree --write-tree` of the head against LIVE develop 49a41f3: rc 0, clean (result tree ff25719e13920523bc31bd0ff27f06ca7ca1ab8f). Control: a commit that edits the same package.json line differently conflicts (rc 1, stage 1/2/3 entries listed).
- Live develop advanced 29bb453 -> 49a41f3 (2 commits, 7 files). It touches none of the 3 PR files, adds no handlebars reference, and changes no import/require line under originate/src (diff grep empty). My install/regen tests were run against the 29bb453 base; given those facts I judge that a safe extrapolation but it was not re-run on the new base.
- Commit message: ends `Refs KS-1453`; closing-keyword grep (close/fix/resolve + #/KS-) = 0. Its claims (343 to 337, the six packages, no version/integrity/entry changes, "deploy: image must be rebuilt") all reproduced above. Linear and GitHub untouched by me.

## NOT tested
- The real Docker image build and any deploy (Docker not started, as ordered). The runner stage's copy of builder node_modules plus Prisma `.prisma` copy-back (Dockerfile:79-86) was not exercised.
- The PR body text on GitHub (not fetched; only the commit message was compared).
- Registry/auth behaviour inside CI, npm versions other than 11.19.0, Alpine/musl.
- Preflight, check:openapi, shell suites, integration tests.
- Merge result was not built or tested on the new develop tip.
- Root `npm ci` package count vs the author's 1937 (Minor 1).

## Evidence
`0_Brain/reference/2026-10-13_gate-pr1544/evidence/` (01_diff.txt, 01_fulldiff.patch, 02_lockparse.txt, 03_regen_*, 04_*, 05_*, 06_*, 07_*). Scratch trees under the session scratchpad.
