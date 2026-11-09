PR 2138: GO WITH NOTES

# Gate 294, tier 1 (Opus), fix round 1 of 2 (compare): PR 2138, Refs KS-590, Seat G 32nd. Findings only.

| PR | head | verdict |
|---|---|---|
| 2138 | fdf80425e9d5c4f99f0a7b5c5c7521b0f7a39ec1 | GO WITH NOTES |

## BLUF
- **The delta changes no product behaviour.** d769c05d0a9b..fdf80425e9d5 is 4 files, +43/-13. In `verification.ts` the only change is 6 comment lines. When both versions are compiled with comments stripped, the output is byte-identical. A planted one-token code change makes the output differ.
- **The three new cells are real kills.** Each is red on develop by assertion. Each is red under my own re-implementation of gate 292's X1 and X2b, and under a new v2 mutant (X7). Each mutant reddens exactly that one cell across the whole suite of 2,618.
- **Wording.** All four G292-1 places now name migration 011. Nothing in the PR's files still credits 039. The body names card 1102 = a and carries the Stuart deploy line.
- **Gates.** Whole suite 2,618 of 2,618. tsc and eslint are identical to develop, each with a planted control. The merge onto d0b4825cc244 is clean, with a planted conflict control. 0 of 67 other PRs share a path, with a planted control.
- **One LOW text finding (G294-1).** The PR body's "What changed" line misstates the verification.ts line count. It has done so since round 0. It needs a body edit, not a code round.
- Nothing needs Kam.

## Pins (read at start and end)
- Start, 22:06:42 AEDT: develop d0b4825cc24493213f82b609670a4a0fa521a4b9 and PR head fdf80425e9d5c4f99f0a7b5c5c7521b0f7a39ec1. Both match the commission. The head's parent is d769c05d0a9b (round 0), so this is a fast-forward of one commit.
- End, 22:17:51 AEDT: both unchanged.

## FOUND / TESTED / HOW

**Instrument.**
- My own blobless clone, sparse, at /private/tmp/g294: `repo` is the head, and `dev` is a worktree at develop d0b4825c.
- node_modules are symlinked read-only from the seat's s-g32-ks590 tree. Nothing was written there.
- Node v26.8.1 and jest 29.7.0, with jest's cache in /private/tmp/g294/jestcache.

### Q1. The delta changes no product behaviour
- `git diff --name-only d769c05d0a9b fdf80425e9d5` lists 4 paths:
  - the ks590 test file;
  - `verification.ts`;
  - the cheat and flow KS-590 fragments.
- `verificationV2.ts`, `docs/VERIFICATION.md` and the three changed cells are untouched. The shortstat is 4 files, +43/-13.
- In verification.ts, `diff -U0` shows 6 changed lines. All 6 are `//` comments (3 out, 3 in) and 0 are non-comment lines.
- **Control:** I compiled both versions with TypeScript `transpileModule` and `removeComments: true`:
  - r0 sha256 6fe17f466d5a7afc;
  - r1 sha256 6fe17f466d5a7afc, so the two are identical;
  - a planted copy of r1 with `if (!rowTenant) return true` changed to `false` gives bb2f85e46a79288b. The diff shows exactly that line, so the instrument sees a one-token code change.
- The whole suite agrees (Q5): head 2,618 = round 0's 2,615 + 3 new cells, with 0 changed results against develop's common cells.

### Q2. G292-2 and G292-3: the new cells, each under my own mutant
Red-first: I put the head's ks590 file into the develop tree. Develop's route files are byte-identical to f98afb11's.
- **19 of 26 RED**, exactly the declared set, which includes G1-F, G1-V and G2-C2. The 7 controls are GREEN: G2-E, G2-F, G4-C, G4-D, C-1, C-2 and C-5.
- All three new cells fail by assertion:
  - G1-F at :305: `certifierOrganizationId` received ORG_UUID;
  - G1-V at :241 via `expectWithheld`: org id received;
  - G2-C2 at :363: `onChainMetadata` received the whole metadata, identity block included.
- At the head: 26 of 26.

My own mutants, written fresh from the gate 292 verdict's descriptions (/private/tmp/g294/mut/mutate.py). Each was planted alone on the head tree and run against the WHOLE originate suite:

| Mutant | What it does | Whole-suite red |
|---|---|---|
| X1 (gap 1, G292-2) | `scopeTenantFields` nulls `certifierOrganizationId` only when the certification carries a `certifiedBy` (a name) | **1 of 2,618: G1-F only** (assertion :305, org id received). Round 0: 0, survived. |
| X2 (gap 2, /verify) | /verify chain-first scope argument `true` -> `!callerTenantOf(req)` | 1: G2-C (as at round 0) |
| X2b (G292-3a) | verify-file chain-first scope argument `true` -> `!callerTenantOf(req)` | **1: G2-C2 only** (assertion :363). Round 0: 0, survived. |
| X7 (G292-3b, new) | v2 `buildMatch` cross-tenant branch scopes, then restores `certification.certifierOrganizationId` | **1: G1-V only** (assertion :241) |

- Site check: the X2 and X2b mutants each hit their own `}, true));` (:1021 is verify-file and :1588 is /verify). I printed both sites after each mutation.
- Restore: after the mutants, verification.ts has sha256 c29880e63e608a64, equal to the saved head copy, and `git status -uno` in my clone is clean.
- Wrong-reason check:
  - G1-F checks its own input: the chain was asked once and the certification id is CHAIN_CERT_ID. Its metadata carries `issuerOrgId` and no `issuerName`, the post-KS-238 shape.
  - G2-C2 sends the tenant header, and with an empty table it checks that the chain was asked once.
  - G1-V checks that the row shown is the other tenant's (`documentId` ROW_EXT) and `fieldsWithheld: true`.
  - None of the three passes vacuously.
- The seat's summary_r1.txt (M1b reddens G1-F only, M2g reddens G2-C2 only, DEV reddens 19) agrees with my own runs. I did not re-run the seat's 12 mutants. Round 0's 10 cover code that this delta does not change.

### Q3. G292-1 and G292-5
- **Migration 011 at develop:** `011_documents_tenant_id.sql:139` reads `ALTER TABLE documents ALTER COLUMN tenant_id SET NOT NULL`, after a backfill and a zero-NULL assertion (:132-136).
- **The code comment, verification.ts:458-460 at the head**, now says "Migration 011 made documents.tenant_id NOT NULL ...".
- **Grep for "039" in every one of the 9 PR files at the head (case-insensitive): 0 in all 9.**
  - Control: the same grep on round 0's verification.ts gives 1.
  - "migration 011" / "011 made": 1 in verification.ts and 1 in the flow fragment.
- **Flow fragment:** it names migration 011. The Not-measured line no longer lists RLS or the demo/kintsugi role question. The cheat's Not-measured line dropped "real PostgreSQL row-level security". The cheat never credited 039.
- **PR body** (seat draft pr_body_r1.md; the seat's PATCH read-back says "body equal: True"):
  - Gap 3 names migration 011 and the gate's PG15 measurement.
  - The NOT-run line says untenanted rows are moot where 011 ran.
  - "039" appears only as the disclosed correction: "Round 1 corrected this line: it credited migration 039's RLS ...". The G292-1 bullet reads "now name migration 011, not 039". Neither credits 039.
  - Control: round 0's pr_body.md has 2 hits for "039".
- **Comment 845cb0df** (seat draft comment_ks590_r1.md, plus evidence/comment_r1_real.out: "update success: True | read back equal: True", the same comment id, 2430 -> 3139 chars):
  - It names migration 011.
  - 039 appears only as the disclosed correction.
  - It carries the "_Edited 2026-11-09 for fix round 1 ..._" note.
  - Control: round 0's comment_ks590_final.md has 1 hit for "039".
- **G292-5:** `services/originate/src/originate.openapi.ts` is NOT among the PR's 9 paths (grep -ic openapi over the path list = 0). At the head, :674-677 still reads "title, issuer, certifiedBy ... because the registration belongs to a different tenant". The body names it under "Named follow-ups", with the "different tenant" wording. Left and named, as the fix-round brief allowed.

### Q4. The PR body: card 1102 and the deploy line
- Card read with `decision_queue.sh show`: `secuura-ks590-verify-disclosure-four-questions-1102`, status ruled, choice 'a', ruled_ts 2026-11-02T12:44:16+11:00. Option a reads "Strict: no tenant-owned naming incl. org UUID on all four paths (changes live verify)". Its detail reads "Verifiers incl. Platform S stop seeing the org id; confirm with Stuart first."
- The body names it beside card 1109 = a and pack row 16, quotes it exactly, and links it to G292-4 as settled.
- The body says: "**Deploy:** a DEPLOY of this change needs Kam's word to Stuart first ('confirm with Stuart first'). The merge to develop does not, and demo is frozen anyway."
- The ticket comment carries the same deploy line.

### Q5. Whole suite, tsc, eslint, merge tree, census
- **Whole originate suite:**
  - head: 2,618 of 2,618 in 221 suites;
  - develop: 2,592 of 2,592 in 220 suites.
  - Compared by suite and cell name: 2,591 common, 0 changed result. The head has 27 cells develop lacks: the 26 ks590 cells plus the relabelled ks584 cell. The one develop-only cell is the old ks584 label.
- **tsc** over src INCLUDING tests (my temporary tsconfig.g294.json extends the service's, with noEmit):
  - head 4 and develop 4, an identical list (ks1937 and ks488 duplicate `EmailModule` and `saved`) apart from the tree prefix;
  - planted control: a src file assigning a string to a number makes it 5. I then moved it out, and the count is 4 again.
- **eslint** through the ESLint API with cwd = Blockchain/Dev (the CLI refused the path as outside its base, and I may not cd):
  - head 312 files, 0 errors, 29 warnings; develop 311 files, 0 errors, 29 warnings;
  - per-file counts are identical, and the one new file (ks590 test) has 0 and 0;
  - planted control: a file with an `any` and an unused local makes it 30 warnings. I then moved it out.
- **Merge tree:**
  - `git merge-tree --write-tree develop pr2138` gives rc 0, tree 63954b8e. Against develop it is 9 files, +568/-21. Its path list equals the PR's 9 paths.
  - Merge tree vs PR head: only develop's two moved files since the base (the ks1534 originate test and the ks1505 api-gateway test).
  - Planted control: a commit on develop that edits the `if (!rowTenant) return false;` line the PR rewrites. merge-tree gives rc 1 with CONFLICT (content) in verification.ts.
  - A first planted edit, two lines away, did NOT conflict. Expected, but noted so the control's design is visible.
- **Census** (git-based, not the GitHub API):
  - The set: gate 292's copy of the seat's open list (59) plus every pull ref from 2136 to 2144 except 2138, 67 PRs. Each PR's files = `git diff --name-only $(merge-base develop head) head`.
  - **Overlap with the PR's 9 paths: 0.** No PR touches VERIFICATION.md or a KS-590 fragment.
  - Only PR 2087 touches `originate/src/routes/` (adminConfig.ts).
  - The originate `__tests__/` prefix fires on 2052, 2087, 2093, 2094, 2099, 2100, 2101 and 2141. PR 2141's three files are ks1868 init/redis tests, none shared.
  - Planted control: a fake row with the PR's own verification.ts path is matched, 1 of 1.

## NOT TESTED
- **The PR body and the Linear comment as stored.** No GitHub or Linear API was used. I read both from the seat's drafts plus its read-back evidence (body equal: True; comment read back equal: True). The "6 comments before and after" claim was not re-read.
- **Open/closed state of the census set.** It was not re-read: a PR closed since then only over-includes, and a reopened old PR would be missed.
- **DB-gated integration suites.** Not re-run. Round 0's gate ran KS 1114 T9 and KS 1119 on PG15, and this delta changes no product code (Q1). KS 1557 and KS 1662 are still UNMEASURED.
- **Other checks:** the platform suites, Node 24, a live chain-first answer, and services outside originate.
- **The seat's 12 mutants.** Not re-implemented. I ran my own 4 (above).

## Findings

**G294-1 (LOW, accuracy of client-facing PR text).** The PR body's "What changed" line says "`verification.ts` +34/-14".
- Measured with `git diff --numstat`, verification.ts is **+26/-13**. That holds develop...head, f98afb11..d769c05d (round 0) and with `-w`.
- The +4/-1 (verificationV2.ts) and +4/-2 (VERIFICATION.md) figures beside it are correct.
- The wrong figure was already in round 0's pr_body.md, and gate 292 did not catch it. Round 1 touched only comment lines (3 for 3), so the count is unchanged.
- Fix: a body edit only. No code, and no new round needed for it.

## G292 findings, status at fdf80425e9d5

| Finding | Status | Evidence |
|---|---|---|
| G292-1 (LOW, 039 credited) | **CLOSED** | 011 named in the code comment, the flow fragment, the body and comment 845cb0df (edited in place, with an edit note). 0 "039" hits in the 9 PR files; 039 appears in the body and comment only as the disclosed correction. |
| G292-2 (LOW, gap-1 mutant survived) | **CLOSED** | G1-F: red on develop; my X1 reddens it and only it across 2,618 cells; green at the head. |
| G292-3 (LOW, two unpinned scrubs) | **CLOSED** | (a) G2-C2: red on develop; my X2b reddens it and only it. (b) G1-V: red on develop; my X7 (v2 cross-tenant org id kept) reddens it and only it. Both green at the head. |
| G292-4 (NOTE, scope for every caller) | **SETTLED** | Kam's card 1102 = a (2026-11-02 12:44), read with `decision_queue.sh show`. The decision that it covers the chain-first and v2 chain-only answers for every caller is Wednesday's reading of that card, not Kam's words. The reading is sound: that branch runs only when the caller's tenant holds no row. The body records it as settled. |
| G292-5 (INFO, openapi wording) | **OPEN** (left by design, named) | `originate.openapi.ts:674-677` is unchanged and outside the PR's paths. It is named in the body's follow-ups with the "different tenant" wording. It needs a follow-up ticket. |

## Conduct
- I never ran cd. The only git write verbs I ran were in my own clone /private/tmp/g294: sparse-checkout, checkout, worktree add, fetch of pull refs, merge-tree, and plumbing for the control commit under a separate GIT_INDEX_FILE. One `git -C $R checkout` was refused by the hook because it used a variable; I reran it with the literal path.
- In !CODING I ran only ls-remote, and read files with cat. I ran no other git verb there.
- I posted and mailed nothing. No docker, no box, no rm. My planted files were moved out of the tree with mv to /private/tmp/g294/hold, and the clone is clean (`git status -uno` empty).
- **Load.** load1 was 8.32 at the checkout and peaked at 9.10 between my whole-suite mutant runs (jest -w 3). Other seats contribute to it. I dropped back below 8 before the tsc and eslint runs, and the end reading was 4.74.
- **Disk.** Clone /private/tmp/g294 is 320 MB, left in place (no rm). DevMASTER showed 101 GiB free at start and end.
