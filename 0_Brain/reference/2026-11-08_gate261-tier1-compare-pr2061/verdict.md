VERDICT: GO WITH NOTES. PR 2061 (KS-1536 3b) at head 29a732c8e9367e6758663188580f08123a149196. This is a compare against gate 244, not a re-gate.

| PR | Head | Verdict |
|---|---|---|
| 2061, KS-1536 3b | 29a732c8e9367e6758663188580f08123a149196 | GO WITH NOTES |

## First: develop moved during the gate. The PR head did not.

| Reading (origin, ls-remote) | develop | 2061 | 2075 | 2066 |
|---|---|---|---|---|
| Commission pin, 23:23:19 AEDT | abd044f63a9d | 29a732c8e936 | (none given) | (none given) |
| Start, 12:24:13Z | abd044f63a9d | 29a732c8e936 | 32aa0d06bc0a | baf577c78e7f |
| End-1, 12:33:57Z | **765701307eb3** | 29a732c8e936 | 32aa0d06bc0a | baf577c78e7f |
| End-2, 12:34:44Z | 765701307eb3 | 29a732c8e936 | 32aa0d06bc0a | baf577c78e7f |

- The 2061 head never moved, so this verdict stands for 29a732c8e936.
- Develop gained one commit: 765701307 "Refs KS-2081: the transfer write doors refuse a non-user principal" (committed 12:27:12Z). It touches 8 paths: the transfer service, `docs/openapi/secuura-api.yaml` and two KS-2081 fragments. None of them is one of 2061's 8 paths.
- I re-measured Q3 on it. The merge-tree of the head on 765701307eb3 is rc 0, tree 7918853260452b16009469d2691482901b09c207. Guard 97 of 97 and auth cells 133 of 133 pass on that merged tree.
- The commit adds no platform-role list. Its added lines test `connector` / `api_key` only. Control: the same grep sees 607 added lines in its transfer diff.

Severity is mine. Priority is not.

### Notes

- **N1, Note.** Develop moved again while the gate ran (above). No paths are shared and the merge is clean. Re-read origin at merge time.
- **N2, Minor, carried from gate 244's F9.** The guard's slack is still there, and it is wider than "can come down by 2". MEASURED AT RUNTIME:
  - Counts at the head: `users.ts` 9 against a baseline of 11, and `oauth.ts` 1 against a baseline of 2. That is 3 lists of slack.
  - My plant of one new platform-role list in `services/auth/src/routes/oauth.ts` passes G2 (97 of 97 green). Two new lists turn G2 red.
  - The READY says F9 is not in this push, so this is not new. The PR body says the baseline "can come down by 2". By my recount it is 3: users.ts 2 plus oauth.ts 1.
  - Fix-shape: lower both baseline entries after merge.
- **N3, Note.** Gate 244's F7, F8, F10 and its Ask 1 (the `admin` loss, Kam's to see) are unchanged by this merge. The READY says they are deferred to B 98th at merge. I did not re-test them.

---

## Q1. Gate 244's four conditions at the new head

**Condition 1: HOLDS.** Test: `git diff edcb42e7ae99 <head>` minus what develop brought must be that one doc only.

Merge base of the two parents: c5c26b2835df.

- (a) The paths where the head differs from edcb42e7 are exactly the 126 paths develop changed from the merge base to cfb6c1573ba9. I diffed the two sorted lists: rc 0, identical.
- (b) The paths where the head differs from cfb6c1573ba9 are exactly 3b's 8 paths (merge base to edcb42e7).
- (c) Only one path differs from both parents: `Blockchain/Dev/docs/security/ROLES-AND-AUTHORIZATION-INVENTORY.md`. So 3b's other 7 paths hold edcb42e7's blobs, and every other path holds develop's blob.
- Control: the instrument can see a change. `git diff edcb42e7 <head> -- services/auth` is 14554 bytes. It is all develop-side test files plus the 3a guard files, and none of them is in 3b's set.

**Condition 2: HOLDS.** Lines 197–198 of the doc at the head name `PLATFORM_ADMIN_ROLES` or `PLATFORM_SCOPE_ROLES` 0 times, and the whole doc names them 0 times.
- Positive controls: the same count at :197–198 is 1 in edcb42e7, 1 in cfb6c1573ba9 and 1 in abd044f63a9d.
- `git grep -i` over the head finds neither symbol in any product file. The only hits are test assertions that they are absent.
- The doc's new wording matches the code: `admin.ts` calls `isPlatformRole` (2 hits) and `runWithPlatformScope` (6), and `adminConfig.ts` calls `runWithPlatformScope` (21).

**Condition 3: HOLDS.** Develop must not have gained a change to `routes/users.ts`, `routes/oauth.ts` or `isPlatformRole` in between.
- `git log b27f5fb30f4a..abd044f63a9d -- users.ts oauth.ts`: no commits. Positive control: the last develop commit on `users.ts` is found, 3f9f9a081 (KS-1968).
- `-G isPlatformRole` over the same range finds only cfb6c1573 (3a itself). The new develop commit 765701307 does not touch auth or shared at all.
- The 3a squash is exactly the gated 3a:
  - `patch-id --stable` of cfb6c1573^..cfb6c1573 equals that of c5c26b2835df..796ea55fb8eb: e15dbc99b68b on both, 34 files each.
  - `keyRevokePolicy.ts` is byte-equal between cfb6c1573 and 796ea55fb8eb (0 bytes of diff). Control: b27f5fb30f4a against cfb6c1573 is 33 lines.
- KS-2083 (PR 2075) has not landed: it is still open at 32aa0d06bc0a.

**Condition 4: HOLDS.** MEASURED AT RUNTIME at the head in my clone. Shared `dist` was built from the merged source, and its `keyRevokePolicy.js` sha256 is 9705e718951c…, byte-equal to the seat's rebuilt file.

| Suite | Result |
|---|---|
| `packages/shared` `ks1536-one-role-vocabulary` (G1–G7 each named and passed) | 97 of 97 |
| auth `ks1536-*` (3 files) + `ks1210-*` (2 files) | 133 of 133. Same as gate 244 and the READY |
| api-gateway `ks1536` | 103 of 103 |

Each condition's control is listed inline above.

## Q2. The merge-in commit itself

Head 29a732c8e936. Parents: edcb42e7ae99423740da3b1e87d6d4b60559c0fd and cfb6c1573ba9c948ebbe898fb2aec283bb9954ab. I verified both with `cat-file`.

`git merge-tree --write-tree edcb42e7ae99 cfb6c1573ba9` returned rc 1, with a conflict only in `ROLES-AND-AUTHORIZATION-INVENTORY.md`, in tree 18ecc89f620b. The diff of that mechanical tree against the head tree is **1 file, 5 deletions, 0 insertions**. The deleted lines are the conflict markers and the two losing lines:

- `<<<<<<< edcb42e7ae99` (marker)
- 3b's old :198, `path (\`PLATFORM_SCOPE_ROLES\` / runWithPlatformScope …admin.ts…)`. This is the stale line, and it is dropped.
- `=======` (marker)
- 3a's old :197, `confinement (\`PLATFORM_ADMIN_ROLES\`/\`isPlatformAdmin\` …users.ts…)`. This is the stale line, and it is dropped.
- `>>>>>>> cfb6c1573ba9` (marker)

What is kept: 3b's :197 (`isPlatformAdmin`, which asks the shared `isPlatformRole`) and 3a's :198 (`isPlatformRole` / `runWithPlatformScope` in `admin.ts`). So both PRs' rows are kept and the merge commit changes nothing else. Every other path in the head tree is identical to the mechanical merge.

Control: the same diff instrument shows a non-empty difference, the 5 lines, so it is not blind.

## Q3. Develop moved to abd044f63a9d (PR 2058), and since then to 765701307eb3

- **abd044f63a9d:** merge-tree with the head is rc 0, tree a15b9022262cb15a9e8684868fcdf57850271d3d. That is the tree the READY reports.
  - abd044f63's parent is cfb6c1573ba9. It changes 7 paths: frontend/admin Settings, `api.ts`, `settingsSavePayload.ts`, two ks1231 script tests and two fragments.
  - These are the same 7 paths as PR 2058's own diff from its merge base. The PR 2058 head 527d67b1852e is a pre-squash branch, so its whole-tree diff against the squash is not comparable.
  - Paths shared with 2061's 8: **0**. Control: the same `comm` of 2061 against itself gives 8.
  - The head tree and the merged tree differ in exactly 7 paths, which are 2058's.
- **765701307eb3 (new, KS-2081):** merge-tree rc 0, tree 7918853260452b16009469d2691482901b09c207, 0 shared paths. On a trial commit of that tree: guard 97 of 97 and auth cells 133 of 133. Details are at the top.

## Q4. 3b cells and 3a guard cells on the merged tree, with my own plants

The runs at the head are listed under condition 4. My plants were each restored with `git checkout --`, and the clone read 0 modified tracked files after each one:

| Plant | Suite | Result |
|---|---|---|
| A. `users.ts` `isPlatformAdmin` replaced with an exact-case list `SYSTEM_ADMIN \| SUPER_ADMIN \| super_admin` (no shared predicate) | auth users file | 1 of 55 red, only the source cell "isPlatformAdmin answers by asking the shared predicate". This is an equivalent mutant at runtime: the file's own header (:32) and cell list (:160) show the case variants are refused by the outer ADMIN_ROLES lists before the predicate runs. So the behaviour cells are right to stay green. Not a defect |
| B. `oauth.ts` `isOauthPlatformAdmin` also admits `ORG_ADMIN` | auth oauth + ks1210 | 4 of 64 red (B2 ORG_ADMIN 403, drift E1, 3b ORG_ADMIN control, source cell) |
| C. Shared `PLATFORM_ROLES` gains `ADMIN` (`admin` folds into it). dist rebuilt, then auth run | auth users + oauth | 18 of 94 red (every "bare admin loses …" cell). **This proves the auth cells run against the merged 3a shared module, not a stale one.** Restored and rebuilt, and the dist sha is back to 9705e718951c |
| D1. One new platform-role list in `oauth.ts` | shared guard | **green, 97 of 97.** This is N2, the baseline slack |
| D2. Two new lists in `oauth.ts` | shared guard | 1 red, G2 only |
| D3. `'Platform_Admin'` literal in `oauth.ts` | shared guard | 1 red, G1 only |

No cell passed for the wrong reason, except that plant A's survival is by design (above), and D1 shows a slack gate 244 already knew about.

## Q5. Open PRs 2075 and 2066 against the new head

| PR | merge-tree with 29a732c8e936 | Runtime on a trial merge commit of that tree |
|---|---|---|
| 2075 (KS-2083, `users.ts`), head 32aa0d06bc0a | rc 0, tree 8e1c7fbd77f18b47424917ca25c9347c7a5a184e (= READY) | guard 97 of 97; auth `ks1536-*` + `ks1210-*` + `ks2083-*` **162 of 162**. The 29 extra cells are 2075's own. Control: `roleChanged` count is 3 in the merged `users.ts` and 0 at the head |
| 2066 (KS-2032, inventory doc + `keyRevokePolicy.ts` + security), head baf577c78e7f | rc 0, tree bb13e172190bc6edd5b95cabfc22d4396dd9ddd0 (= READY) | shared guard + `ks1570` + `ks2032` 131 of 131; auth ks1536/ks1210 133 of 133; security unit `ks1585-…503`, `ks2032-…liveness-read`, `ks578-ks643` 41 of 41 |

- READ ONLY: 2075 changes the session-revoke branch at `users.ts`:835–848 and uses no symbol 3b removed. 2066 changes `adminIsLive` plumbing in `keyRevokePolicy.ts`, and adds no role list and no change to `PLATFORM_ROLES` or `isPlatformRole`. 2066's doc edit is the KS-1533 paragraph, away from :197–198.
- Answer: **landing 2061 first breaks neither** on these measures. Both are 11 and 15 commits behind develop respectively, so each needs its own refresh whatever the order.

## Controls (summary)

- Every merge-tree rc 0 sits beside an rc 1 on the parents' trial merge, so the instrument does report conflicts.
- Every "0 shared paths" sits beside a self-comm of 8.
- Every grep zero has a parent or develop doc reading 1.
- The diff-of-trees has a non-empty control.
- Each suite had at least one plant that turned it red: shared guard (D2, D3), auth users (A, C), auth oauth (B, C).
- The shared-dist dependency was shown live by plant C.

## NOT TESTED

- Auth, gateway and originate whole suites at the head. The READY ran auth whole; I did not, because several auth cells read `process.cwd()` and I ran under a no-cd rule.
- Originate `ks1536` (jest).
- tsc, eslint, the test-file ratchet and the docs-fragments check at the head or on any trial merge.
- Security integration tests in 2066 (`*.integration.test.ts`, 2 files). The vitest config excluded them, so the 41 is 3 unit files only.
- 2058's own cells (frontend/admin, scripts). KS-2081's own cells.
- Any box, stack, docker, real login or decoded token. Gate 244's F7, F8, F10 and Ask 1, and the demo or Kintsugi role counts.
- PR body and ticket comment text: not re-read. The READY says neither was edited.
- Open-PR census: no `gh` was used, so only 2075 and 2066 (named) were checked. Other open PRs sharing 2061's paths were not enumerated.
- Node LTS: my runs used the same node and dependencies as the seat (symlinked from Y's `worktrees/s-y6-ks1536b`, read only). This is the seat's dependency substrate, not a clean install.

## My own conduct

- Findings only. Nothing was posted, no box and no docker. Network: ls-remote, clone and fetch only, with the Blockchain deploy key named in its `core.sshCommand`.
- **Clone: /private/tmp/g261, 1.7G at the end. Not removed (no-rm per this commission).**
  - It holds three trial worktrees (`wt75`, `wt66`, `wtdev`) on three local commit-tree commits: 0560484ff541, da0f036108f6 and fa924cf02d15.
  - node_modules are real dirs of symlinks into Y's `s-y6-ks1536b` (read only). `.vite` and `.cache` were kept local so that no runner wrote into Y's tree.
  - The shared `dist` was built in my trees only.
  - Vitest's G3 cell writes a `ks1536-*` temp dir under the system tmpdir each run. That is the suite's own behaviour, and it is not cleaned.
- **Writes outside my folder and clone:** `/private/tmp/g261_clone.log` and `/private/tmp/g261_fetch.log`, the clone and fetch logs, which I wrote beside the clone instead of into my scratchpad. They are left in place (no rm). Everything else went to the session scratchpad.
- **cd:** twice I put a `cd` into a child shell, once as a no-op `( cd … ; true )` subshell and once inside `bash -c`. The second failed before running anything (tsc not found there). After that I used absolute paths only (`tsc -p`, `vitest --root`). The session shell's cwd never changed.
- `/Volumes/DevMASTER/!CODING/` was read only: `git -C` read verbs, `cat`, `ls`. I made no write and no fetch there.
- **Load:** it was 9.4–13.4 from other sessions at my start, and 11.9 right after my clone. I held every test run until load1 was under 8. Run-time readings were 4.8–7.3.
- **Disk:** DevMASTER had 24–25 GiB free throughout. The clone is on the boot volume (300 GiB free).
