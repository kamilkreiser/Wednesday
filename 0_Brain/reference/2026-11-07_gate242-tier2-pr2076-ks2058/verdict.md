GO WITH NOTES
Head 8ce56b0f9a86686266c95598b149782d92611556 (PR 2076), develop b27f5fb30f4a912ec2b4b78f5c27281d11e47a87. Both re-read by `git ls-remote` at start and at end: unchanged, and equal to the READY's.

# Gate 242: PR 2076 (KS-2058 follow-up), tier 2, round 1 of 2

## BLUF
The stop line is not crossed. Neither product file changes a statement: compiled with comments removed, base 44ee04cb and head 8ce56b0f give byte-identical output for both `db.ts` and `governanceService.ts`. The new cell R3 does what its name says, can fail, and dies on the seat's own K24 mutant. Five notes follow, all about words in comments and fragments, none a promise-keeping failure in code. I found nothing that needs a tier 1 Opus gate.

## Findings

### H1 Low, words: the db.ts limit comment is true only when no row holds the wallet yet
`db.ts:236-237` (new lines). FOUND: "with one disabled holder and one live one, the admin's request binds the live one." That holds on the owner-read path, which `registerParticipant` reaches only when `dbGetParticipantByAddress` finds no row (`governanceService.ts:~630-637`). If the disabled holder already has a participant row for the wallet, the request lands on that row and the owner read never runs. The enclosing docstring scopes itself to "a new row", so the sentence is not false in context, but it stands alone as a "Stated limit". TESTED: read of the code only. HOW: reading `registerParticipant` beside the comment. The cheat fragment's "What to know" is scoped to "wallet with no row", so it is fine.

### H2 Low, words: a fragment says "In nature it is vanishingly rare" and uses "my driver"
Flow fragment, "The retry's own save" row (the diff line replacing "Read from the gate's note; not reproduced..."). FOUND: "In nature it is vanishingly rare" is a frequency claim; the only measurement behind it is forced timing (10 of 10 under forced interleaving). No rate in nature was measured. "my driver reproduces that" is first person in a document a Secuura reader sees, and names a tool that is not in the PR. A reader may take "vanishingly rare" as a measured bound. Suggest dropping it or saying "not measured outside forced timing". TESTED: read. I could not re-run the seat's real-PostgreSQL driver (no PostgreSQL, see below).

### H3 Low, words: the cheat fragment omits the two limits the flow fragment and the docstring now state
Cheat fragment, "Not measured here" row. FOUND: it gains the G1 limit but not "the 201 can differ from the row on the did" or "an omitted flag is written from the default, which can lose a flag or grant one". Its "What to know" row says "An omitted did keeps what the row holds when the write lands", which a reader can take as covering the response body too. The flow fragment and the `registerParticipant` docstring do state both. TESTED: read of both fragments against the code (`asStored`, lines 640-649; upsert lines 182-197: `is_drep`/`is_constitutional_committee` are written from EXCLUDED).

### H4 Low, test: R3 asserts the row only, not the 201 body
Test file, new cell at the end (about line 551-565). FOUND: the cell checks `status 201` and the row's did. The comment in the code says the 201 can name the older did; R3 therefore pins the fix (row keeps the newer did) and says nothing about the stated limit (response names the older). Not wrong, but the "state the limit" half of the PR has no cell. My own planted defect (below) shows other cells cover the re-read of the holder.

### H5 Info, words: "keeps its vote power" is ambiguous in the registerParticipant docstring
`governanceService.ts:606-607` (new). "A row an erased user already holds still takes the admin's stake here and keeps its vote power". The code recomputes `votePower` from the new stake and writes it; the row's power does not stay as it was, it stays counted. Gate 232's G7 asked that the docstring not say "not touched"; that is fixed. The ambiguity is cosmetic.

## Answers to the commission

**Q1.** Confirmed by my own diff, two ways. (a) `git diff -U0 44ee04cb..pr2076` on the two files: every changed line begins with `*`, `/*` or `//` (non-comment filter gave 0 lines). (b) TypeScript `transpileModule` with `removeComments: true`, base vs head: identical for both files (db.ts 7126 chars each, governanceService.ts 36751 each). Positive control: changing `LIMIT 2` to `LIMIT 3` in db.ts makes the two outputs differ. Each changed comment against the code: the db.ts sentence is true on the no-row path (H1). The `registerParticipant` docstring: "can omit one, name an older one, or name one another request cleared" matches `asStored(holder)` at the retry plus `didOmitted` keeping the row's did; "an omitted flag is written from the default rather than kept, which can lose a flag or grant one" matches `stored?.isDRep ?? (stakedAmount >= 1000)` and the upsert writing EXCLUDED flags. "(KS-2060)" and "still takes the admin's stake" match the code (no status check on the existing-row path).

**Q2.** Gate 232 notes, as the seat claims:
- G1: stated limit. Present in db.ts, flow and cheat fragments. Closed as a stated limit (H1 for the scope of the db.ts words).
- G2: routed to KS-2060 by the seat's notes; not in this diff. Open, as ruled. Not graded.
- G3, G4 (count SQL): not in this diff; the READY says cleared to D 59th. Open here, as the commission lets it.
- G5: closed by cell R3, which I tested (Q3).
- G6: routed to KS-2059/KS-2060. Open, as ruled.
- G7: closed (docstring no longer says "not touched"; H5 is a cosmetic residue).
- G8: closed for the three words points (flag limit "lose or grant", the did "older/cleared" case, "Not reproduced on real PostgreSQL" replaced). Remaining: H2 and H3.

**Q3.** The cell `control ks2058 R3 the did changes between the holder read and the retry's save: the newer did stays`. Passes at head: 30 of 30 in the file. Red proof on the seat's mutant: line 666 `dbSaveParticipant(participant, didOmitted)` changed to `false` gives exactly one failure, R3 (29 of 30). Planted defect of my own: remove the retry's `participant = asStored(holder)` (line 664). The file's 30 cells all pass (the cell does not pin that), but the full suite fails ks1951 R1c, so another cell covers it. The cell reaches the retry: the first hook sets the older did and a 23505; the second hook sets the newer did only if the retry ran, so a skipped retry would leave the older did and fail. It is labelled "control", honestly, since it passes at PR 2051's head.

**Q4.** The two fragments state what the code does, apart from H2 and H3. Figures I could reproduce: 30 cells (10 labelled RED, 20 labelled control, counted from the run), 367 tests in 20 files (see caveat), docs-fragments check OK (the two ADVISORY lines are the pre-existing ones the READY names). Figures I could not reproduce: 24 of 24 mutants, 32 of 32 real-PostgreSQL checks, "PR 2039's product fails 13 checks". A reader at Secuura could take "vanishingly rare" (H2) as a measurement.

**Q5.** `git merge-tree --write-tree origin/develop pr2076`: rc 0, no conflicts, at develop b27f5fb3. Develop moved 16 files from the base; 0 under services/governance or the KS-2058 fragments. Open-PR overlap: NOT tested (see below).

## What I did NOT test
- Open PRs sharing the five paths. That needs `gh` or the API, and the commission allowed network only for git fetch. `ls-remote` shows 1998 pull refs and 1372 branches; I did not scan them.
- Real PostgreSQL, the seat's mutants K1 to K23, the 32 proof checks, 10-of-10 and 25-of-25 forced-timing figures. No PostgreSQL started (commission). READ ONLY.
- Node 24, tsc, eslint, check:openapi, the hook legs. I did not run tsc or eslint.
- The suite at the head with the lockfile's dependencies. **Caveat on my own run:** the read-only checkout's `node_modules` holds zod 3.25.76, but the repo wants zod ^4.6.7. I built `packages/shared` in my clone (tsc reported zod type errors but emitted), mapped `zod` to `zod/v4` through a jest config of mine, and ran ts-jest with diagnostics off. Result: 363 of 367 pass. The 4 failures are all in `ks1725-governance-zod-catches-keep-zod3-details`, a test of zod 4's exact error body, which my zod shim cannot reproduce. They are in files this PR does not touch, and they fail the same way with or without the planted defect. So the 367 of 367 claim is not confirmed by me; the 30 of 30 in the PR's file is.
- Merge simulation was a tree merge only; I did not run the suites on the merged tree.

## Own conduct
- Clone: `/private/tmp/g242`, partial (blobless) clone of the remote read from the read-only checkout, using its deploy key through `core.sshCommand` set in MY clone. I fetched `refs/pull/2076/head` and `develop` there. I did not fetch or write in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`.
- In the clone I symlinked the read-only checkout's `node_modules` entries (read only; `@secuura` links point into my clone) and wrote `jest.g242.config.js`, `run.sh`, scratch `a.ts b.ts c.ts`, `svc.orig`. I edited `governanceService.ts` for mutants and restored it from `svc.orig` after each; final sha256 equals the first reading (5cfcd9ce...b97836). No commit made. Built `packages/shared/dist` in the clone.
- Two hook refusals: a `rm` of a symlink via `$D` (redone with a literal path) and a `git fetch` through `$G` (redone with a literal path). No other attempt to work around a hook.
- Nothing posted, no box, no docker, no PostgreSQL. Network: `git clone`, `git fetch`, `git ls-remote` only.
- Clone removal: see the last line of this file.

Clone /private/tmp/g242 removed at the end (rm -rf of literal path; the symlinked node_modules in the read-only checkout still has its 986 entries intact).
