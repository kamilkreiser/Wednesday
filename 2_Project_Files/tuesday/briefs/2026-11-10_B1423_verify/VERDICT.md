GATE B1423: GO WITH FINDINGS @ f94e05d on main a54250f

Independent tier-2 gate of the builder branch `b1423/composer-discovery-typed-subanswer` (Security Composer, lane C4, PCOMP-12). Run 07:11 to 07:19 AEDT 2026-11-10. No security-shaped issue found. No Blocker, no Major; four Minors (below).

All work was done in the gate's own clone under the session scratchpad
(`/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/00755d0b-17ed-4742-8f90-5ae73a7a41a9/scratchpad/g/clone`, push URL set to `DISABLED`, never pushed). Network: only `git ls-remote` / `git fetch` over SSH through the project deploy key. No HTTP to any hosted host, no `gh`, no Jira, no mail, no `az`, no PR. The heavy lock `.tools/composer-heavy.lock` was read before each docker job (absent each time). The gate did not take it, because it writes only into this folder.

## 1. Ref, lane containment, overlap

| Check | Instrument | Result | Control |
|---|---|---|---|
| Branch head | `git ls-remote origin` | `f94e05d31402b0893989ae598e67a46890082269 refs/heads/b1423/composer-discovery-typed-subanswer` = READY sha | the same call printed main `a54250f4...` and `b1249/...` `d5f7c1fc` |
| Main | `git ls-remote` at 07:12 and again at 07:18 | `a54250f48f41b693ab73163531e7ca82425fce69`, unmoved, equal to the kit stamp | - |
| Parent | `git log -1 --format=%P` | `a54250f4...`, one commit, merge-base = main | - |
| Paths in the lane | `git diff --name-only main head` against the OWNS regex `^(apps/web/src/screens/Discovery\.tsx\|apps/web/src/screens/LaneC4[^/]*\.test\.tsx)$` | **2 of 2** in the lane | - |
| Open PR overlap | `refs/pull/{85,86,91}/head` fetched; `diff --name-only merge-base..pr` then `comm -12` with the lane | #85: 57 files, 0 overlap. #86: 2 files, 0. #91: 2 files, 0 | #85 lists `packages/renderers/src/document-pdf.ts` at line 44 |
| Sibling C90 (kit B1420) | its PARTITION's three OWNS paths (no `b1420*` ref on origin yet) | 0 overlap | the same `comm` against #85 finds 1 (`pdf-fit.ts`, the overlap the C90 kit records) |

## 2. Merge

- `git merge-tree --write-tree main head`: rc 0, tree `5121782b219d5fbc6cb8114da5dbce8efd1ab49d`. This equals head's own tree (head is a direct child of main).
- `commit-tree` (env identity `gate`) gave `523856dda5a396534d4d5224c60b45905f585048`. `diff --name-only main merge` lists exactly the 2 lane paths. `git diff --quiet head merge` rc 0. Both lane blobs are byte-equal to head.
- **Control:** a loose commit that rewrites line 272 of `Discovery.tsx` makes `merge-tree` exit 1.
- The trees exported by `git archive` give `diff -r` empty for head against merge. So every result measured at head below is also the merge's result (same bytes).

## 3. CI predicates

- **No `.github` path at head** (`ls-tree`: 0 entries; control: `scripts/ci.sh` 1 entry). The project's CI is `scripts/ci.sh`. Its node step is `npm run ci:node` = lint, format:check, typecheck, build, test, run with `--network none`.
- **Image.** My own `docker build --network=none --target ci` failed at `npm ci`: the layer was not cached, and the gate may not reach the registry. So the chain ran in the existing image `pc-b1420-node:base`, read-only, every run `--rm --network none`. Its `/repo/package-lock.json` and `package.json` sha256 equal main's (`f3e4197f...`, `942de7e8...`). Its node is v22.23.2.
- **Isolation.** Each run wipes `/repo` except `node_modules` and copies in the exported tree from a read-only mount.

| Step | main | head (= merge) |
|---|---|---|
| lint | rc 0 | rc 0 |
| format:check | rc 0 | rc 0 |
| typecheck (incl. `tsc -p apps/web/tsconfig.json`) | rc 0 | rc 0 |
| build | rc 0 | rc 0 |
| test (vitest JSON) | 311 files, 3,120 rows: 3,117 passed / 2 failed / 1 skipped | 312 files, 3,125 rows: 3,122 / 2 / 1 |

- **Program comparison** of the (file, full name, status) sets: **lost 0, added 5**. All 5 added rows are in `LaneC4-discovery-typed-subanswer.test.tsx`, all passed.
- **The red set is identical at both:** the 2 rows of `packages/content/src/citations.test.ts`, which need the withheld E8 SOW text (never mounted).
- **Comparator control:** a row dropped from a copy of head reads `lost 1`.
- **Repo-wide scans** (run whatever paths changed):
  - Cf (format) characters over every `ls-tree` text file: main 966 files / 6 with Cf; head 967 / 6. Same files; the new file is clean. The control string with U+200B counts 1.
  - gitleaks 8.30.1 with `scripts/gitleaks.toml`: head working tree rc 0; commit range `main..head` rc 0. Control: a planted token file gives rc 1.
- **NOT RUN:**
  - The db suite (`scripts/test-db.sh`; needs postgres; no lane path is a db test).
  - The bridge and compose stack steps of `ci.sh`.
  - The pinned-image secret scan (`scripts/secret-scan.sh`; the host gitleaks with the same config stood in).
  - CodeQL (hosted only).
- Hosted CodeQL on the PR is the proof for those.

## 4. New tests red with the fix removed (copies only)

| Row | fix removed (main's Discovery.tsx) | M1 all groups, not in-scope | M2 scope ignored | M3 draft groupId null | head |
|---|---|---|---|---|---|
| 1 keyed by first group's id | **RED** "the device group the answered draft is keyed by: expected null to be '...c40a1'" | green | green | **RED** (same message) | green |
| 2 two groups independent | **RED** "expected [ 'Print protocols that are needed' ] to deeply equal [ ...(2) ]" | **RED** (3 sets vs 2) | green | **RED** | green |
| 3 stored per-group shows in own set only | **RED** "expected one the D-013.print.required_protocols set keyed for group ...c40a2, found 0" | green | green | green | green |
| 4 out-of-scope group has no set | green (guard) | **RED** | green | green | green |
| 5 engagement-level still engagement | green (guard) | green | **RED** "expected one D-013's words box, found 2" | green | green |

- The fix removed turns 3 of 5 rows red, for the stated reason.
- Every row goes red under at least one mutation, so **no vacuous row**.
- Each mutation has anchor count 1 and changes 4 diff lines. The host tree was untouched.

## 5. On-main lines re-verified at main, by program

- **Defect present at main.** `Discovery.tsx:271-273` has `typedDraftFor` with `draftKey(answerKey, null)` / `stored(answerKey, null)`. The typed block at `:991-992` has `stored(answerKey, null)` and `draftKey(answerKey, null)`. Shown by `grep -n`; control: `:723` `typedDraftFor={typedDraftFor}` is found by the same grep.
- **Line counts and pointers:**
  - `Discovery.tsx` is 1,230 lines at main and 1,245 at head.
  - `:232` `groups`, `:934` prop type, `:945` `isTypedQuestion`, `:997` `typedDraftFor(spec, answerKey)`: all as stated.
- **Shipped content:**
  - release-demo and release-draft each have 26 discovery questions, with sub-answer scopes `{engagement: 45}` and `device_group` 0. The engagement count is the control.
  - The two releases' `discovery` arrays are equal (True).
- **API contract:**
  - `packages/api-contract/src/document.ts:765` is the device_group_id description: null means engagement, a group means that group, the other is refused 400.
  - `:808` is `scope: enumOf(["engagement", "device_group"])`.
- **Other facts:**
  - `apps/web/tsconfig.json:15` include is `["src", "vite.config.ts"]`.
  - `packages/engine/test/fixtures/content.ts:338-348` is D-013 `required_protocols`, `set_enum`, `scope: "device_group"`.
  - The last main change to `Discovery.tsx` is `230f9fab` 2026-10-16 (#79).

## 6. Adversarial probes

- **P-b re-run independently, with the builder's harness run unmodified in the gate's copies:**
  - pb-main = pb-head = pb-head(second run) = sha256 `5f90325859350bee8c7b5788496afee6b0aa6bfd534359f5a832cdcad72aad2f`. This reproduces the builder's hash and shows a stable, deterministic output order.
  - The `answered` -> `Answered` plant gives `c9cdd846...` (reproduced). It differs from base in 2 of 30 records (4 serialised fields).
  - Coverage reproduced: 568 / 568 / 448 controls, 7 / 7 / 9 PUTs, 60 / 60 / 82 answers.
- **Every sub-answer forced to `device_group`** (gate probe, head; 2 shapes x 10 sections):
  - Every typed write carries an in-scope group id (G1 20, G2 20). There are 0 writes for the out-of-scope group and 0 `INVALID_REQUEST` on the page.
  - A null-keyed stored value of a device_group sub-answer is listed under the legacy list with Remove.
  - The only null-keyed writes are the set-up prefills `D-001.answer` / `D-003.answer` (`Discovery.tsx:203`). These are only reachable when a prefilled question is declared device_group, which no release does. The builder disclosed this (FOR TUESDAY item 3).
- **No in-scope group** (all three groups `in_scope: false`): a device_group sub-answer renders no box (0 ids for any group) and sends nothing. The builder disclosed this (item 2).
- **Out-of-scope stored typed answer:** shown nowhere (0 ids for GOUT; not in the legacy list). The builder disclosed this (item 1).
- **Engagement-scope path unchanged:**
  - The `cells` value for a non-device_group spec is `[null]`.
  - The spec object is passed through unchanged when `groupId === null`.
  - The draft spread adds `groupId: null`, which `typedDraftFrom` already set.
  - The P-b byte equality covers this path.

## 7. Names, secrets, hosts, Cf

- **Name scan.** The pattern `(?<![A-Za-z])<name>(?![a-z])` (python `re`, IGNORECASE) ran over the 490 added lines and the commit message. Names: the brief's 9-name ban list plus the kit's widened 3 coordinator-seat names (12 in all). Result: **0** in both.
  - Control: a planted `_by_<name>_` fires 1 for each of three ban-list names.
  - Negative control: ordinary words that contain a ban-list name as a prefix (for example "waiter", "inches") fire 0.
- **Ban grep** `B[0-9]{3,4}|PCOMP` over the message and the added lines: 0. Trailer `Co-Authored-By:` count is 1.
- **Hosts and URLs** in added lines and the message: none.
- **Secret-shaped patterns:** 0. gitleaks is covered in section 3.
- **Non-ASCII in added lines:** 2 U+00B7 and 1 U+2026, all in test comments and selectors. They mirror the screen's existing "D-013 <middot> ..." heading. There are 0 Cf characters.
- **Commit author/committer** is the repo's GitHub noreply identity read from main's last commit, as the kit directs. The underscore-aware pattern does not fire on it. Recorded for awareness only.

## 8. Builder STATUS claims graded

| Claim | Grade |
|---|---|
| Defect at main `Discovery.tsx:271-273`, typed block `:986-993` | true |
| 1,230 lines at main; pointers 232/271-273/275/723/934/945/992/997 | true |
| Releases 26 questions, `{engagement: 45}`, device_group 0; discovery arrays equal | true |
| Contract `document.ts:765`, `:808`; tsconfig include; engine fixture `:338-348` | true |
| Web workspace at base 178 files, 1,475 rows all passed | true |
| Existing Discovery tests 7 files, 51 rows (web) | true |
| Base whole: 311 files, 3,120 rows, 3,117/2/1; red = 2 SOW rows | true |
| Head whole: 3,125 rows, 3,122/2/1; lost 0, added 5 | true |
| lint, format:check, typecheck, build rc 0 at both | true |
| 3 of 5 rows red at base with the quoted messages | true (messages byte-match) |
| Plant engagement key back -> rows 1, 2 red | true (gate M3) |
| Plant group id pinned -> only the independence row red | not shown (the gate ran different mutations) |
| P-b base = head sha256 `5f903258...` | true (reproduced) |
| Control plant `c9cdd846...` "differs from base in 4 records" | false as worded: 2 records (4 serialised fields) |
| Coverage 568/568/448 controls, 7/7/9 PUTs, 60/60/82 answers | true |
| `git diff --stat` Discovery +48 -33; commit +490 -33 | true |
| "E1 name scan over the 461 added lines" | off: 490 added lines, of which 461 are non-blank |
| One trailer; ban grep 0; name scan 0 | true |
| gitleaks "~17437 bytes ... no leaks found" | true (same range, same count) |
| Main never moved | true (a54250f4 at 07:18) |
| PRs #91/#86/#85 2/2/57 files, 0 hits | true |
| `b1249/...` ref still present | true |
| Last change to Discovery.tsx `230f9fab` 2026-10-16 (#79) | true |
| Jira text, ticket status Backlog, 0 comments | not shown (the gate's fence bars Jira) |
| `npm ci` layer built fresh at 06:35 | not shown (image removed; consistent with the gate's uncached offline build failing) |

## Findings

- **MINOR-1 (process, disclosed by the builder).** The kit said: "the cached `npm ci` layer, else STOP". The builder continued and let `npm ci` fetch from the npm registry during its image build.
  - No branch content depends on it: the gate reproduced every number with no network.
  - It is a fence deviation for the coordinator to rule on, not a defect in the change.
- **MINOR-2.** The STATUS P-b control line says the plant "differs from base in 4 records". The measured difference is 2 records (4 serialised fields).
- **MINOR-3.** The STATUS says "461 added lines". The diff adds 490 lines, of which 461 are non-blank.
- **MINOR-4 (latent, disclosed, out of the lane).** These are not regressions on any shipped shape; they belong in a follow-up ticket if a release ever declares a device_group sub-answer:
  - an out-of-scope stored typed device_group answer is shown nowhere;
  - a device_group sub-answer with no in-scope groups renders nothing;
  - set-up prefills stay engagement-level.

## Landing

Per C-101 (`CLARIFICATIONS.md:1799`): the coordinator opens the PR, re-reads CodeQL and the checks, then squash-merges it pinned to head f94e05d. Nothing is deployed: Composer deploys only on the product owner's card. Files: `pr-title.txt`, `pr-body.txt`, `squash-subject.txt`, `squash-body.txt`, `landing.txt`.
