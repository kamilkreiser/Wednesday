PR 2247: GO WITH NOTES (at head c4edaa734aba5da0aa8557573c6f6213e6b1ad30; tier 1)

# QA GATE 372, tier 1: PR 2247 (KS-1600 follow-up: the originate admin API-key mint refuses `permissions: null` with 400)

Gate: Opus 5.5, findings only. Nothing was fixed, posted, pushed, merged or written to Linear or GitHub. All work is in `scratch/` of this folder. No database of any kind was used (jest mock-database harness only).

## Pins (gh api, GH_CONFIG_DIR = Blockchain/4_Credentials/.gh-config)
- First measurement, 20:45:45Z: PR 2247 head `c4edaa734aba5da0aa8557573c6f6213e6b1ad30`, open, not merged, 1 commit, 7 files, +202 -11, parent `9942bae93563`. Develop `6185f0f1ace8344efa81df091d2e5dd718e7f9e4`.
- Before this verdict, 21:00:21Z: the same head (open, not merged, 1 commit), the same develop, and the PR body byte-identical to the one I read.
- My clone: `scratch/repo`, cloned locally from the seat's `s-c42-base` (read only). Every sha listed above resolves to a commit object, and the commit ids are content hashes. Head checked out at `c4edaa73`. The develop worktree is `scratch/dev` at `6185f0f1`.
- Deps: `npm ci --ignore-scripts` at `Blockchain/Dev` in my clone, rc 0. That gave 33 node_modules trees: root, packages/shared, 25 services and 6 frontends. Then `fix-libsodium-symlink.js` rc 0 and the `packages/shared` build rc 0. The develop tree got APFS clones of the same trees and of shared/dist; no package file differs between `6185f0f1` and the head. Node v26.8.1. TMPDIR `/private/tmp/g372t`.

## Q1: does null get the same 400, before the organisation decisions and before the INSERT? YES
- At the head, the handler (adminConfig.ts lines 1026-1029) runs this check BEFORE the `organizationId` shape check, the decisions at (a) and (c) (both 403) and `$queryRaw`:
  - the condition is `d.permissions !== undefined && !(Array.isArray(...) && every string)`;
  - the answer is 400 `{success:false,error:{code:'BAD_REQUEST',message:'permissions must be an array of strings'}}`, the one literal that every malformed value shares.
  - `null` now takes that path. An omitted key (`undefined`) does not.
- Cells pinning it, by caller class:
  - N1, platform caller;
  - N2, ORG_ADMIN;
  - N3, ORG_ADMIN with null plus a FOREIGN organisation: 400, not 403;
  - N4, the literal wire body;
  - C6, the null body `toEqual` the bare-string body, with the key sets fixed.
- The not-called assertion is proven. Mutant m8 (null refused AFTER the INSERT) turns N1 to N4 red. N1 and N2 go red on `mockQueryRaw toHaveBeenCalledTimes(0)`, N3 and N4 on `inserts 0`. My own g15 (refused after the organisation decisions but before the INSERT) is caught by N3.
- Controls behave as on develop, green at develop and at the head:
  - omitted (C1), `[]` (C2), a valid array (C3), a missing name (C4);
  - the falsy rows `''`, `0` and `false` (C5).
- The whole originate suite is green both ways, so the KS-1206, KS-1594 (unit), forged-tenant and KS-764 mint cells are unchanged.

## Q2: is anything widened? NO
- The diff touches 7 files and only ONE product file: `services/originate/src/routes/adminConfig.ts`. It is one hunk inside the `POST /api-keys` handler: the comment rewritten, and `&& d.permissions !== null` deleted. No other route, `requestedScopes`, the org or provisioning logic, the security service, the gateway, packages/shared or any package.json changed.
- On who can mint what, this only NARROWS:
  - a null body no longer mints a `['read']` key, for any caller class;
  - no caller can now mint something it could not mint before;
  - omitted and `[]` still mint `['read']`.
- Builder's candidate (1) is PRE-EXISTING, confirmed by reading develop `6185f0f1`:
  - At originate, `requestedScopes = Array.isArray(p) && p.length > 0 ? p : ['read']`. That line is unchanged by the PR, so `[]` is stored as `['read']`.
  - At the security service, `createApiKeySchema.scopes = z.array(z.string()).default(['read'])` (line 718), the route parses at line 1268, and the INSERT stores `scopes: data.scopes` (line 1483), so `[]` is stored as `[]`.
  - The ZodError catch answers 400 "Validation failed" at line 1551. The PR changes no security file.

## Q3: is the edit to the existing 2087 cell honest? YES (one note)
- In `ks1600-malformed-permissions-refused-at-the-admin-mint.test.ts`, only two things changed:
  - the file-header sentence that said null stays (1 line became 4);
  - the ONE "null keeps the fall-back" cell, now expecting `[400,'BAD_REQUEST',0]` and the message, with a 2-line comment above it.
  - No other cell changed: the diff is 2 hunks. Its 16 other cells are green at both pins.
- In the two 2087 fragments, the four null statements are corrected in place: 1 in the cheat, 3 in the flow ("Unchanged on purpose...", "two small differences" became "one", "Leaving null and [] as they are" became "Leaving [] as it is" plus one sentence). Each now says what the head does, and no other line in those files changed (word-diff read).
- The new pair is also correct: the flow fragment for this change and its cheat-sheet fragment.
- NOTE N3, Info: the ANSWER said "title kept", but the cell title was REWRITTEN. It now reads `RED KS-1600 follow-up: null is refused 400 before the INSERT (was: null keeps the fall-back to ["read"])`, which keeps the old title inside "(was: ...)". The "RED" prefix matches that file's own red-first naming. Harmless.

## Q4: are the tests honest? YES. I planted 16 mutants and 16 were killed.
Runner: `scratch/mutants.py`. Each mutant was planted in MY clone and checked by count (old text occurs exactly once). Each run covered the two KS-1600 files plus ks1206, the forged-tenant file and ks764: 63 cells. The file was restored by content after every run, and its sha256 `55c62198649394a0...` is equal after all 16 (the same sha as the builder's `adminConfig.ts.fixed`). Every red is a matcher AssertionError: no load errors, no TypeErrors.
- Baseline 63/63. The control m0 (a different "name is required" message) turns C4 red: it fires.
- m1, the fix reverted. This equals develop's product code with the final cells, and develop's adminConfig.ts differs from the head only in this condition and its comment. Red: N1, N2, N3, N4, C6 and the flipped 2087 cell (6). This is the builder's red-first set: 5 failed / 7 passed in the new file, all AssertionError.
- m2, a truthiness test: N1-N4, C6, C5 x3 and the flipped cell (9).
- m3, null coalesced to undefined: N1-N4, C6 and the flipped cell (6).
- m4, the refusal moved after the organisation decisions: N3 and the 2087 "validation comes first" cell (2).
- m5, an omitted key refused: C1, the 2087 absent control, and 3 KS-1206 mint controls (5 over my wider set; the builder's 2 were over two files).
- m6, `[]` refused: C2 and the 2087 `[]` control (2).
- m7, null refused with another message: N1-N4, C6 and the flipped cell (6).
- m8, null refused after the INSERT: N1-N4 and the flipped cell (5). C6 stays green, as the builder said.
- The gate's own mutants:
  - g9, 422 with the same body: 6 red.
  - g10, an extra `details` field: C6 only.
  - g11, null refused for platform callers only: N2 and N3.
  - g12, refused for ORG_ADMIN only: N1, N4, C6 and the flipped cell.
  - g13, another error code: 6 red.
  - g14, refused only when no organizationId is sent: N3.
  - g15, refused after the 403 decisions but before the INSERT: N3.
- Every changed branch is covered. Is the not-called assertion enough for m8? YES. C6 does not need it, because N1 to N4 carry the INSERT check. g10 shows that C6 is the cell guarding the BODY shape, so each cell has its own job.

## Q5: does the PR body meet the rules? YES (two notes)
- Closing words: the BRIEF's list `resolves|closes|fixes` occurs 0 times. A wider pattern hits only "the fix reverted" and "unclosed `<div>`", which are not closing words followed by an issue reference. Positive control: the same scan counts 1 "Test Evidence".
- No self-hold sentence: `do not merge|don't merge|until the pre-merge` occurs 0 times (card `secuura-premerge-block-nine-prs-1113` = c).
- The Test Evidence block names what was NOT run:
  - legs 3, 4 and 8 (named, with the hook's final line verbatim);
  - the four platform suites (Schemathesis, Akto, Playwright, k6);
  - a running stack and real PostgreSQL or Redis;
  - callers outside the repository and live traffic.
- NOTE N1, Info: the literal `Refs KS-1600` is in the PR TITLE and the commit subject. The body carries only `Ticket: https://linear.app/secuura/issue/KS-1600` and 2 KS-1600 mentions, with no "Refs KS-1600" line.
- NOTE N2, Minor (honesty of the record): the body's "NOT run" list includes `npm run check:test-types`. The same body, and the READY, say the ratchet (hook leg 14, which is check:test-types) read 0 new errors in all five services. It WAS run, through the hook and by the seat; it just does not cover originate. I ran it too: 0 new in auth (41 in the baseline), api-gateway (25), vc-issuer, security and m365-integration. The body contradicts itself here.

## Also measured
- **Whole originate suite, interleaved (load1 at each start):**

  | Run | Tree | Suites | Tests | load1 |
  |---|---|---|---|---|
  | B1 | head | 226 | 2708 | 6.37 |
  | A1 | develop 6185f0f1 | 225 | 2696 | 7.64 |
  | B2 | head | 226 | 2708 | 6.92 |
  | A2 | develop 6185f0f1 | 225 | 2696 | 5.77 |

  Every run had all tests passing and an empty failure set. The difference is +1 suite and +12 tests, which is the new file. These equal the builder's figures.
- **Merge-tree** with develop `6185f0f1`, both orders: rc 0, the same tree `7fcb4483...`. The merged tree differs from develop by exactly the 7 PR files, and from the head by exactly develop's 5 move files. Planted control: a commit that edits the carve-out line on develop, merged with the head, gives rc 1 with CONFLICT in adminConfig.ts.
- **tsc:**
  - originate's own tsconfig (src only; it excludes `src/__tests__`): rc 0 at both head and develop.
  - The test-inclusive config (`scratch/tsconfig.tests_*.json`; 260 `__tests__` files, the three PR files confirmed in the program by `--listFiles`): 4 errors at the head, identical at develop. They are TS2300 `EmailModule` and TS2451 `saved` in ks1937-... and ks488-smtp-opt-in. The PR's files have 0 errors.
  - Planted TS2322: reported.
- **eslint** (the repo's flat config, by absolute path) on the 3 changed TS files: 0 errors and 0 warnings each. A planted `var` gives rc 1 `no-var`, and the file was restored byte-identical.
- **Docs:** `docs-fragments.mjs check --root` gives OK rc 0 at both head and develop, with the same 2 ADVISORY lines on each (the committed pages lag the fragments). A planted unclosed `<div>` in the new flow fragment gave FAIL rc 1, "tags are not balanced"; the file was restored and its sha256 is equal.
- **Callers in the repo:** no non-test file sends `permissions: null`. The schemathesis setup, the e2e specs and the playwright client send string arrays. A `git grep` over the head for `permissions: null|None` hits only the two KS-1600 test files and the new fragments.
- **GitHub checks on the head:** every Actions job failed or was skipped because "The job was not started because recent account payments have failed or your spending limit". This is the same on merged PRs 2246, 2158 and 2087 (Linear ticket present, Secret Detection, Dependency Audit all failed). It is a property of the account, not of this PR. NOTE N4, Info: CI gives no signal here.

## Findings
- N2, Minor: the PR body lists check:test-types as NOT run while also saying the ratchet read 0 new. Fix the line in place, or leave it; not blocking.
- N1, Info: no `Refs KS-1600` line in the body (it is in the title and the commit).
- N3, Info: the flipped 2087 cell's title was rewritten, where the ANSWER said "title kept" (the old title is kept inside "(was: ...)").
- N4, Info: GitHub Actions did not run (billing), the same as on every recent PR.
- No Major or Blocker findings. No mutant survived the suite as a whole.

## For Kam (credential-minting route)
- Who can mint what: this PR only NARROWS. `permissions: null` used to mint a read-only key for ANY caller, and now it is a 400 for every caller class. Nothing new can be minted by anyone. Omitted and `[]` are unchanged.
- The one behaviour change any external caller would see: a client that sends `permissions: null` now gets a 400 where it used to get a read-only key. There are 0 such callers in the repo; customer scripts and live traffic are UNMEASURED. This sits inside card `secuura-ks1600-originate-malformed-permissions-1106` = a.
- Still open and NOT in this PR: `[]` is stored as `['read']` at originate and as `[]` at the security service. This is the builder's candidate (1), and it is pre-existing.

## Not measured by this gate
- A real database or a running stack; legs 3, 4 and 8; the platform suites.
- The security service RUN on null. Its behaviour was read, not executed.
- Callers outside the repository, and Node LTS status.
