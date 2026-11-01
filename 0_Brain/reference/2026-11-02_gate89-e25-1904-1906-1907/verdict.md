# QA GATE 89 (tier 2, batched): PR 1904 / 1906 / 1907 (Seat E 25th, Spark passes)

Reviewer: independent (Wednesday's gate). Workdir: this folder. Spark shadow skipped (allowance). Nothing pushed, commented, written to tickets or mailed.

## BLUF

| PR | Ticket | Verdict | Fix-before-merge |
|---|---|---|---|
| 1904 | KS-1898 vc-issuer, test-only | **GO** | none |
| 1906 | KS-1868 billing replay catch | **GO** | none |
| 1907 | KS-1841 api-gateway Dockerfile | **GO WITH NOTES** | Recommended (small, not a blocker): restore C3's coverage of chained `rm` lines, see G89-1907-F1 |

## Heads (start == expected == end; ls-remote at end: logs/heads_end.log)

- develop 3281db323e528da5b036ade647a82edd2e8487ec
- 1904 cd128d245389ded73fe7a9d1ce9b5dae28a23efe (1 commit on 8afcf256)
- 1906 12c458f3eb10e820ef0ca419b93b400573b9d7ea (1 commit on 8afcf256)
- 1907 6262b895eab508d13b83e03880a055659d49bff1 (1 commit on 8afcf256)

## FINDINGS

- G89-1907-F1 (note, recommended fix): the narrowing of ks1823 C3 from `/\brm\b/` to `startsWith('RUN rm')` loses a realistic catch. Measured, all 13 cells (ks1823 + ks1841) stay GREEN for: `RUN npm run build && rm ./docs/openapi/secuura-api.yaml` (Mk; the OLD C3 regex caught this one), and for an added separate line `RUN find ./docs/openapi -delete` (Mc), `RUN find ./docs/openapi -name secuura-api.yaml -delete` (Mb), `RUN find ./docs -name secuura-api.yaml -exec rm -f {} +` (Mh). The old C3 would not have caught Mb/Mc/Mh either, so the net loss versus base is Mk-type lines; Mb/Mc/Mh are a gap that was always there but now matters more because a `find ... -exec rm` form is the sanctioned idiom. The narrowing itself was forced (the old predicate would reject the legitimate line, which contains `rm -rf` + `docs/openapi` + `! -name secuura-api.yaml`). Cheap fix: in C3, loop over every `RUN` line other than `RM_LINE` that matches `/(\brm\b|\bunlink\b|-delete\b)/` and `/docs|secuura-api\.yaml/`, and keep the two `not` assertions. Simulated on the Dockerfile text (logs/c3_proposal.log): 0 hits at head, 1 hit for each of Ma, Mb, Mc, Md, Mh, Mk. A `mv` of the spec is still uncovered (Mm); nobody would cover that with text matching, accept it.
- G89-1907-F2 (info): files other than the spec that the old line left in the image and the new line removes: `docs/openapi/WORKFLOWS.md` and `TRACK2_OPENAPI_MIGRATION.md` (both tracked). The gateway reads only `secuura-api.yaml` (src/index.ts:590-592, 692 serves that one file; no other reference in services/api-gateway/src or Dockerfile). Intended by the PR; say so in the body.
- G89-1907-F3 (info, environment): api-gateway full suite at head shows 1 failure, ks1090 (type-check baseline), caused by two TS2345 errors in the untouched `ks815-...test.ts` (Buffer types from the borrowed hoisted `@types/node`). Identical at base (logs/g_base_ks1090.log, g_full_base.log). Not attributable to the PR.
- G89-1906-F1 (info, out of scope): the same unguarded `error instanceof Error ? error.message : String(error)` shape remains at webhooks.ts:166 (`String(error)`), :184, :215. They sit on the Stripe-webhook path, not the admin replay route; a hostile thrown value there has the same hole. Not a defect of this PR; worth a card if not already carded.
- G89-1904-F1 (info): `expectNothingLoggedForTheRefusal` watches vc-issuer's own logger only (its comment says so); the shared error handler's single error line per refusal is not observed. Acceptable and disclosed in the test.

---

## PR 1904 (KS-1898): GO

**Diff (three-dot, 3 files, +71/-4):** `services/vc-issuer/src/__tests__/ks1851-credential-revoke-bound-to-the-creator.test.ts` plus two fragment HTML files. No product file changed (checked: the only non-test, non-fragment file list is empty).

**Cells say what they claim.** V8b-g (6) and V9 x3 now assert, besides 404 and NO UPDATE: `expectNothingLoggedForTheRefusal()` (no `REASON` marker and no `Credential revoked` in the logger mock) and `expectByteIdentical(refused, revoke(unknown id))` (status plus `JSON.stringify(body)`). New V14a-d (memory path, owner-less row via `repo.store` with the default owner): OWNER, ORG_ADMIN, SYSTEM_ADMIN, SUPER_ADMIN of tenant 1, each asserts 404, nothing logged, row JSON unchanged before/after, `revoked` not true, byte-identical to an unknown id. 6 + 3 + 4 = 13 new/changed cells. The memory path owner-less row has no tenant, so even a SUPER_ADMIN of tenant 1 is refused (`ownerlessCredentialReadable` needs a non-null row tenant); consistent with titles.

**Tamper proof, reproduced** (script logs/tamper1904.py, summary logs/tamper1904.summary; mutations applied only to the owner-less refusal branch of `routes/credentials.ts`, restored after each run, worktree clean):

| Mutant | BASE test file (32 cells) | HEAD test file (36 cells) |
|---|---|---|
| M0 none | 32 pass | 36 pass |
| M1 refusal logs the reason | 32 pass (not caught) | 13 fail |
| M2 extra body field (`details`) on the owner-less refusal | 32 pass (not caught) | 13 fail |
| M3 owner-less message differs | 9 fail | 13 fail |
| M4 owner-less answers 403 | 9 fail | 13 fail |
| M5 owner-less allowed (guard off) | 27 fail | 31 fail |

M1 and M2 pass every OLD cell and fail exactly the 13 new/changed cells at head, as claimed. (My first M1/M2 attempt logged/leaked on all refusals, which the old foreign-caller cells already catch; restricted to owner-less rows it matches the author's table.)

**Suite:** vc-issuer at head 23 files, **714/714** pass (logs/vc_full_head.log); base = 714 - 4 new cells = 710 (base test file runs 32 cells, head 36). tsc `-p tsconfig.test.json` rc 0 (logs/vc_tsc_test.log); `tsc -p tsconfig.json` rc 0; eslint on the changed file rc 0 (logs/vc_eslint.log).
Note on environment: the first full run showed 14 ks1906 Unicode-fold failures because the borrowed hoisted node_modules resolved `@secuura/shared` to a stale dist in another tree; I rebuilt `packages/shared` in this clone and re-linked workspace packages inside my own node_modules (logs/mknm.py, shared_build.log). After that, all green. Not a PR issue.

**Notes for the PR body:** state that no product file changed, the tamper table with the base/head columns above, and that the log observation covers vc-issuer's logger only.

---

## PR 1906 (KS-1868): GO

**Hunk is exactly the guard** (webhooks.ts, `+7/-1` in the catch): a `let reason: string; try { reason = error instanceof Error ? error.message : String(error); } catch { reason = 'unreadable thrown value'; }`, then the original `logger.error('Replay failed', { eventId, error: reason })`. Level (`error`), message (`Replay failed`), key (`error`) and the `res.status(500).json({ success:false, error:{ code:'INTERNAL_ERROR', message:'Replay failed' } })` line are byte-unchanged. `instanceof` is inside the try, so a revoked Proxy (instanceof throws) is covered, as is a throwing `message` getter.

**Response never carries thrown text:** the 500 body is a literal in the source; `reason` reaches only the logger. Both RED cells assert the whole body with `toEqual` against the constant, so any added field fails (mutant M5 below).

**Callers:** the catch belongs to the `POST /replay` handler (role-gated by `authenticate()` + `requireRole('SYSTEM_ADMIN','SUPER_ADMIN')`, per the PR's own fragment); no function callers of the changed code. Before the PR a hostile throw left the request unanswered (async handler, Express 4); after, constant 500.

**Red-first by assertion** (logs/b_base_new.log): at base product with the head test, 2 of 3 fail, both `expected undefined to be 500` (R1 revoked Proxy, R2 message-getter), control C1 passes. At head 3/3 (logs/b_head_new.log).

**Mutants** (script logs/mut1906.py, summary logs/mut1906.summary; file restored after, worktree clean):

| Mutant | Cells failing |
|---|---|
| M1 rethrow only the unreadable value | R1, R2 |
| M2 other constant text | R1, R2 |
| M3 level warn | C1, R1, R2 |
| M4 key renamed | C1, R1, R2 |
| M5 response adds `detail: reason` | C1, R1, R2 |
| M6 `instanceof` hoisted outside the try | R1 (R2 still passes; the getter is inside the try) |
| M7 `return` inside the guard (no response) | R1, R2 |
| M8 status 503 | C1, R1, R2 |
All killed (8 here; the author lists 6).

**Suite:** billing at head 14 files, **331/331** (logs/b_full_head.log); base 328 + 3 = 331. `tsc -p tsconfig.json` rc 0; with tests included (custom config, module esnext, logs/tsc_tests.json) the only error is in the untouched webhooks-replay-auth test (`json` unknown, line 106), none in the new test (logs/b_tsc_tests.log). eslint on webhooks.ts and the new test rc 0.

**Money path:** not touched. The diff changes only how the failure reason is computed for a log line. `handleWebhookEvent` and its credit-then-UPDATE ordering are unchanged (the new test stubs `query` to reject).

**Notes for the PR body:** mention F1 (sibling unguarded sites on the Stripe path) as a possible follow-up; include the mutant table.

---

## PR 1907 (KS-1841): GO WITH NOTES

**Diff (5 files, +134/-9):** Dockerfile line 35 swapped as claimed (`RUN find ./docs/openapi -mindepth 1 -maxdepth 1 ! -name secuura-api.yaml -exec rm -rf {} +`), ks1823 test edited (R1/R2 redefined, `RM_LINE` updated, C3 narrowed), new ks1841 test (5 cells: R1-R3, C1, C2), two fragments.

**Red-first** (logs/g_base_newtests.log): base Dockerfile with head tests: **6 of 13 fail** (ks1823 R1/R2/R3, ks1841 R1/R2/R3), assertion failures; head 13/13 (logs/g_head_new.log).

**The line, executed.** Docker daemon available; `node:24-alpine` present locally (linux/arm64, logs/docker_inspect.log). Ran the exact line from the Dockerfile with `--network none --pull never`, mounting disposable fixture trees (scratchpad), script logs/fx.sh, output logs/fx.log:
- Case 1: spec + `.bak`, a file literally named `-rf`, a name with a space, a dotfile, a folder `old-copies/` (containing a nested `secuura-api.yaml`), a symlinked directory and a symlinked file pointing at `../../outside`. Exit 0; only `secuura-api.yaml` remained; `outside/keep.txt` and the sibling `docs/other/keep.txt` untouched. So no escape through symlinks (find does not follow, `rm -rf` removes the link only), leading-dash names are safe (`./` prefix), nothing outside `docs/openapi` is touched.
- Case 2: `secuura-api.yaml` is a symlink: kept (find sees the name), target not touched.
- Case 3: a DIRECTORY named `secuura-api.yaml`: kept with its contents (the name test wins). A build context that did that would produce a spec that is a directory; not realistic (tracked file in the repo).
- Case 4: empty `docs/openapi`: exit 0.
`-mindepth 1` is load-bearing: without it find lists `./docs/openapi` itself (name differs) and `rm -rf` deletes the directory and the spec; mutant Me is caught by ks1823 R3, ks1841 R2, R3.

**Does anything else read `docs/openapi`?** Gateway reads only `secuura-api.yaml` (index.ts:590-592, 692). The runtime stage copies the pruned builder directory (`COPY --from=builder /app/docs/openapi`). See F2 for the two tracked .md files that now stay out of the image.

**C3 narrowing:** forced by the new line, but see F1 for the measured gap and a one-paragraph fix. The author's mutant (an added `RUN rm` of the spec reddens C3) is reproduced (Ma, Md: C3 fails), and ks1841 R2/R3 + ks1823 R1/R3 kill the realistic edits to the sanctioned line itself: Me drop `-mindepth`, Mf invert `! -name`, Mg files-only, Mi/Mj chained `; rm` / `&& rm` onto the same line (all in logs/mut1907.summary). Not caught: Mb/Mc/Mh/Mk (F1). I rate this GO WITH NOTES: none of those is a known edit path today, but Mk used to be caught and is cheap to catch again.

**Suite:** api-gateway at head 134 files, 1372/1373 pass; the 1 failure is ks1090, environmental and identical at base (1367/1368; head - base = +5 = the five ks1841 cells) (F3). `tsc -p tsconfig.json` rc 0 and the repo's own test-type baseline only complains about the untouched ks815 file. eslint on both changed tests rc 0 (logs/g_eslint.log).

**Notes for the PR body:** add F2 (the two .md files leave the image), the Docker run evidence above, and either apply the F1 C3 tweak or record it as a follow-up.

---

## Cross-PR merge checks (logs/merge_tree.log)

`git merge-tree --write-tree` of each onto develop 3281db32: all three rc 0, no conflicts. Pairwise 1904+1906, 1904+1907, 1906+1907: all rc 0. No file is shared between the three (empty intersection of the changed-file lists), as expected.

## Method / limits

Clone is blobless; node deps are the hoisted Blockchain `node_modules` linked read-only, rebuilt `@secuura/*` links and `packages/shared/dist` inside this clone. Mutants edited files only inside this clone and were restored (status clean at the end except the untracked node_modules link dir). No `npm ci` run (read-only reuse of the existing install). Spark shadow skipped by instruction. No docker pull/build; only `docker run` of a local image, `--network none`.
