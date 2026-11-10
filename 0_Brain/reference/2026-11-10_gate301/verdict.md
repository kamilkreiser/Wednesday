PR 2159: GO WITH NOTES
PR 2162: GO WITH NOTES
PR 2157: GO WITH NOTES

# Gate 301, TIER 1 (Opus): PRs 2159 (KS-2111), 2162 (KS-2122), 2157 (KS-1952)

## Pins: ls-remote at start (02:37:29Z) and at end (03:02:51Z), the same both times
- develop d3e663692a8f414f16610236259cab14b27ff0f7
- PR 2159 7b54e7cbb6f0082a32b496c1773aa2e43bfe3ea2 (parent 0115269abd11)
- PR 2162 30048d8b295e6be51540b015033aa4bb20ca5fe4 (parent 0115269abd11)
- PR 2157 1a8e6dd8ef9703cfe08fd18fb75e136cc6cb737b (parent 0d286210f98b)
- PR 2149 d9b899f268a6 (the one open PR named on a shared file)

These heads match the READYs. This verdict covers only these heads.

## Method
- **Clone.** A blobless bare clone sits in my scratchpad (`.../scratchpad/r.git`), with the PR heads fetched to `refs/p/<n>`. It uses the project deploy key by path; no value was printed. It has six worktrees: `w/dev`, `w/2159`, `w/2162`, `w/2157`, and `w/union` (develop plus all three PRs, merged in my clone only).
- **Install.** `node_modules` is symlinked read-only from `worktrees/s-y13-ks1998`, whose install is at develop d3e663692a8f.
- **Runs.** Node v26.8.1 (not an LTS line), vitest 4.1.12. vitest runs only started when load1 was under 8; they were niced.
- **What I did in !CODING.** Only `ls-remote` and file reads. I did not fetch, write, `cd`, post or mail there.
- **Faults of mine.** One Bash call contained a `cd`. The hook refused it and nothing ran. One `rm` named a `$VAR` path; the hook refused it, and I re-ran it with the literal path of my own scratch file.
- **Load.** My first whole-suite pass ran on too narrow a sparse checkout: 39 to 42 cells failed with ENOENT (docs/, migrations/, docker/ were missing). I stopped it, widened the checkout to `Blockchain/Dev` plus `Projects Documents`, and re-ran everything. Only the re-runs are counted below. Load1 reached 12.6 at my last run, which was started under 8.

## Shared-path checks (all three PRs)
- **The three file sets are disjoint.** This is measured by `git diff --numstat` of each commit, and the totals equal the READYs:
  - 2159: 6 files, +297/-0. They are settingsSavePayload.ts, ks1231 cells, the ks2111 test, routes/admin.ts, and two KS-2111 fragments.
  - 2162: 5 files, +309/-2. They are notifications.ts, the ks2122 test, the ks1448 test, and two KS-2122 fragments.
  - 2157: 3 files, +126/-1. They are routes/verification.ts, the ks466 test and the ks1952 test.
  - No path is shared among the three.
- **No overlap with develop.**
  - Develop's commits since each base: 2159 and 2162 (base 0115269abd11) get 3 files: ks570 test plus two KS-2131 fragments. 2157 (base 0d286210f98b) gets 5 files: the same 3 plus ks1728 test.sh and a KS-528 fragment.
  - None of these is a PR path.
  - `merge-tree --write-tree` onto develop is clean for each PR: 2159 tree 307152db, 2162 c2a1eeac, 2157 75375e28.
  - Merging all three in sequence is clean: 2a9f9b5d, 14 files.
- **Open-PR census, by git rather than the API.**
  - I fetched the heads of all 212 PRs numbered 1950 or above.
  - I merge-treed every non-ancestor head onto develop. I counted a hit only if the merge would change one of the 14 paths, or the planted control `api-gateway/src/index.ts`.
  - The control hit PR 2125, as expected.
  - PR 2149 hits the ks1448 test only. 2162 merged with 2149 gives tree 07407095e8ca, which equals the seat's figure.
  - PR 2001 (an old KS-1256 head) would change admin.ts and verification.ts, but it conflicts with develop and is absent from the seat's API census of open PRs. I take it as not open; its open or closed state is UNMEASURED by me.
  - No other PR touches any of the paths.

## Whole api-gateway vitest suite, before and after (mine)

| Tree | Files | Cells |
|---|---|---|
| develop d3e663692a8f | 168 | 1886, all pass |
| union (develop + all three) | 171 | 1918, all pass (+3 files, +32 = 7 + 20 + 5) |
| PR 2159 alone (at its base) | 169 | 1889, all pass (equals the claim) |
| PR 2162 alone | 169 | 1902, all pass (equals the claim) |
| PR 2157 alone | 169 | 1887, all pass (equals the claim) |

The 1882 baseline at 0115269 and 0d286210 is implied: develop's ks570 commit added the 4 cells that make 1886.

---

## PR 2159 (KS-2111): GO WITH NOTES

FOUND / TESTED / HOW

**(1) The diff is exactly the six stated files.** Gateway: an own-key check by exact name for the three names, first in the PUT handler, before the KS-1230 validation, the read, the merge, the write and the refresh. Page: `FORBIDDEN_NAMES` is skipped in `flattenSettings` (as a category and as a field), and in `buildSettingsUpdate` such a key goes into `refused`.

**(2a) Page cells.** The ks1231 runner gives 48/48 at head (the claim is 39 before, 48 after).
- Red-first: with `SETTINGS_PAYLOAD_TS` set to develop's module, 41 pass and 7 fail (Q1, Q1b, Q2, Q3, Q4, Q6, Q7). Q0 and Q5 are pins. This equals the claim of 7 red and 2 pins.
- My mutants, with the cell that caught each:

| Mutant | Caught by |
|---|---|
| FM1: the build-side refusal removed | Q1b, Q2, Q3, Q4 |
| FM2: the flatten category skip removed | Q6, Q7 |
| FM3: the flatten field skip removed | Q6, Q7 |
| FM4: exact name replaced by substring | Q5 |
| FM5: only the category checked at build | Q4 |

All 5 were caught.

**(2b) Gateway cells.** The ks2111 test gives 7/7 at head. With develop's admin.ts it has 4 red (G1×3, G7) and 3 green (G0, G4, G5). This equals the claim of 4 red and 3 pins.

| Mutant | Caught by |
|---|---|
| GM1: refusal removed | G1×3, G7 |
| GM2: the whole refusal moved after the write and refresh | G1×3, G7 |
| GM3: `name in body` instead of the own-key test | G1 constructor and prototype, G4, G5, G7 |
| GM4: only `__proto__` refused | G1 constructor and prototype |

All 4 were caught.

**(3) Wednesday's D2 statements are in the PR body.**
- The narrowing is stated: a nested field is not checked at the PUT, and a stored key is not cleaned.
- The `prototype` cell is "red on the refusal only".
- The behaviour-change sentence is the brief's.
- The ticket comment 45a767a5 (from the seat's draft, sha1 recorded) says the same.

**(4) No other behaviour change in the gateway.** Lookalike names still store (G5, Q5). A normal body still stores with 200 (G4).

**(5) No closing words.** The closing-form regex reads 0 on the title, body, commit and ticket comment, and a planted positive reads 2. The only hyphenated key is KS-2111 (KS 1998 is spaced).

**(6) Census:** see the table above.

FINDINGS
- **G301-2159-1 (MEDIUM; same defect class, outside the ruled three names): the page still mutates shared built-ins for any other name that `Object.prototype` inherits.**
  - How: `buildSettingsUpdate` still does `const target = (updates[category] ??= {})`. For a category named `toString`, `hasOwnProperty`, `valueOf`, `__defineGetter__` or any other inherited name, `??=` finds the inherited function, and `target[field] = value` writes onto it.
  - Measured with a tsx probe of the head module. A stored document `{"general":{...},"toString":{"y12polluted":"yes"}}`, loaded then saved through `prepareSave(flattenSettings(...))`, gives `ok: true`, and `({}).toString.y12polluted === 'yes'` afterwards. The same holds for the other three names.
  - Stored `{"toString":{"call":1}}` makes `Object.prototype.toString.call([])` throw "is not a function" in that browser after a save. The same works with `hasOwnProperty`.
  - The gateway PUT stores such a category: a scratch cell sent the PUT `{"toString":{"call":1}}` and got 200, with the key in the Redis write.
  - So the KS-2111 vector (one tenant admin plants a category, every admin's browser is hit on Save) remains open for every inherited name except the three.
  - The PR does what D2 ruled, and its body claims only the three names. But a code comment in the PR is false at head: "refused by name before anything is grouped, so the assignment below can never reach an inherited property".
  - A one-line fix closes the class: an own-property check (`Object.hasOwn(updates, category) ? … : (updates[category] = {})`) or `Object.create(null)` for `updates` and the targets. The verifier's ROUTE already named the second.
  - Wednesday's call: a fix round on this branch, or a follow-up ticket. Either way, the false comment should not merge as written.
- **G301-2159-2 (INFO):** the body says of the page cells "Each cell reads a control before the run and cleans up after it". Q0, Q5 and Q6 do not use the `leak()` wrapper. They plant nothing, so nothing is lost; the sentence is just slightly too strong.

NOT TESTED: the real Settings page in a browser; `tsc` and eslint for the gateway and admin portal (CARRIED); docs-fragments; GitHub PR comments (no API read); the live PR body (I read the seat's draft, whose sha1 equals the create read-back's `body_sha1`).

---

## PR 2162 (KS-2122): GO WITH NOTES

FOUND / TESTED / HOW

**(1) The diff is exactly the five stated files.**
- `isConnectorPrincipal` (four signals) plus `refuseConnectorPrincipal` is the first statement of list, unread/count, `:id/read`, read-all and `:id`, before the 401 check and before any store read.
- POST is untouched.
- In ks1448, the C1 connector row is removed and C1b is added (201 then 403 FORBIDDEN).

**(2) Cells.** ks2122, ks1448 and notifications.test together give 55/55 at head.
- Red-first: with develop's notifications.ts, 18 fail. That is 17 of the 20 new ks2122 cells (N1×5, N2×5, N3×5, N4, N8) plus C1b. The 3 pins (N5, N6×2) stay green. This equals the claim of 17 red and 3 pins.
- My mutants, with the cells that caught each:

| Mutant | Caught by |
|---|---|
| refusal removed from list | N1/N2 list, N3×5, N4, N8, C1b |
| refusal removed from unread | N1/N2 unread, N3×5, N4 |
| refusal removed from mark-read | N1/N2 mark-read, N3×5, N4 |
| refusal removed from read-all | N1/N2 read-all, N3×5 |
| refusal removed from delete | N1/N2 delete, N3×5, N4, N8 |
| delete refusal moved after the 404 | N2 delete, N3×5, N4 |
| match loosened to `=== 'connector:api-key'` | 12 cells |
| role signal dropped | N3 role |
| verificationLevel signal dropped | N3 level |
| authMethod signal dropped | N3 method |
| prefix arm dropped | N3 prefix ×2 |
| prefix made to refuse only lower-case ids | N3 case-different |

All 12 were caught. One extra mutant survived; see G301-2162-2.

**(3) Wednesday's required statements are in the body, true at the strength measured.**
- The ruling wording: "Wednesday's ruling, by the precedent of Kam's KS 2038 card …; Kam has not ruled on notifications". It never says Kam ruled.
- (a) the KS 1448 C1 to C1b contract change by name, and that KS-1448's file is touched with approval.
- (b) the asymmetry: create 201, read-back 403, left as found.
- (c) the residue: `platform_admins.role` 'connector' fails closed; the Azure CHECK is unverified. I read transferAccess.ts 108-120 and it says this.
- (d) Node v26.8.1, not LTS.
- The D4 condition holds, by my own grep of non-test source in services, packages and frontend at develop:
  - In the gateway, the four signals are set only in middleware/auth.ts 572-577 (the key block).
  - Elsewhere they are set only on connector or key paths: auth jwt.ts 289-294, originate metering.ts:81.
  - None is set for a person.
  - The person paths are auth.ts:634 (test token) and :684 (verified JWT), as the body says.
- The OpenAPI spec already lists 403 on all five routes.

**(4) No other change.** POST is unchanged (N5). A person with a GUID or non-GUID id is unchanged on all five routes (N6). The router is mounted only at index.ts:844.

**(5) No closing words.** Closing-form 0 on the title, body, commit and comment. The body and comment space the other keys.

**(6) Census:** see the table above.

FINDINGS
- **G301-2162-1 (LOW): another ticket's key is hyphenated in the commit message and both fragments.** The commit says "The KS-1448 cell that read a connector key's row back…", and both fragment files carry "KS-1448". The PR body spaces it as "KS 1448". The Y brief's rule names PR text; the commit message travels with the PR, and Linear's integration may link KS-1448 on merge. UNMEASURED whether it will. Report only. Changing the message now would need a new commit or a rebase, which is ruled out.
- **G301-2162-2 (INFO): N4's title says "it reads no store", which is stronger than what it can see.** One mutant survived: the delete refusal placed after the lookup but before the 404. It answers the same, so the answer-equality property holds. The no-read property itself is pinned by no cell.

NOT TESTED: a real API key against a live security service (N8 stubs fetch); tsc, test-types and eslint (CARRIED); docs-fragments; GitHub PR comments; any outside integration caller (UNMEASURED, as the body says).

---

## PR 2157 (KS-1952): GO WITH NOTES

FOUND / TESTED / HOW

**(1) The diff is exactly the three stated files.**
- verification.ts +7: `(body.documentType || body.type) && !redisService.isRedisAvailable()` gives 503 SERVICE_UNAVAILABLE, placed after the connector allow-list block and before `enforceDocumentTypeRules`.
- ks466: the fixture gets `isRedisAvailable: () => true`.
- New 5-cell file.
- enforcement.ts is untouched.

**(2) Cells.** The ks1952 and ks466 files give 9/9 at head. With develop's verification.ts, 2 fail (R1, R2) and 7 pass. This equals the claim of "2 of 5, then 9 of 9".

| Mutant | Caught by |
|---|---|
| KM1: check removed | R1, R2 |
| KM2: `documentType` only (legacy `type` dropped) | R2 |
| KM3: keyed on an empty catalogue instead of availability | C1, C3, and 2 ks466 cells |
| KM4: untyped creates refused too | C2 |
| KM5: check moved after enforcement | R1, R2 |

All 5 were caught.

**(3) Kam's card is option a, and the body says so.** The LIVE behaviour change comes first in the body, the site deviation is stated with its reason, and flag (c) is UNMEASURED with the search listed. U 22nd's D1(b) is honoured: no seat name in the PR text.

**(4) Other behaviour.** A typed create with Redis up is unchanged (C1, C3). An untyped create with Redis down is unchanged (C2). See G301-2157-2 for the one unstated change.

**(5) No closing words.** Closing-form 0 on the title, body, commit and comment. Only KS-1952 appears hyphenated.

**(6) Census:** see the table above.

FINDINGS
- **G301-2157-1 (LOW): "the catalogue reads EMPTY while Redis is unavailable" is stated as a fact, and is too strong.** It appears in the code comment, the test header, the commit and the PR body.
  - `redis.ts` 546-558: `getAllDocumentTypes` reads an in-process fallback Map when `isRedisAvailable()` is false.
  - `setDocumentType` writes that Map in fallback mode (redis.ts 525-533), and so do the admin document-type CRUD and the demo seed (admin.ts 663-670, 726, 741, 767).
  - So the catalogue is empty only when nothing was written into the Map during the outage. That is likely for a production mid-run drop; production refuses to start without Redis (redis.ts 129-134).
  - Consequence: a dev, local or E2E gateway that boots without Redis (fallback is "dev/test only") had working enforcement over types created in that process. It now 503s every typed create. This sharpens flag (c), which stays UNMEASURED for real runs.
  - It matches card a as worded ("refused 503 while Redis is unavailable"). Report only.
- **G301-2157-2 (LOW, unstated change):** during an outage, a typed create with a non-string `documentType` (e.g. 123) used to get enforcement's 400 VALIDATION_ERROR (enforcement.ts 106-115). It now gets 503. The body says "names a documentType … answers 503", which covers it literally, but the 400-to-503 change for caller-error input is not named. Read in code; no cell.
- **G301-2157-3 (LOW):** the body's suite figures "(502 files)" before and "(504 files)" after do not reproduce. I measured 168 files before and 169 after (1882 to 1887 cells, which matches). The cell counts are right; the file counts are not, cause UNMEASURED.

NOT TESTED: a real Redis or ioredis client and fallback-mode transitions; tsc and lint (CARRIED); any E2E or local run without Redis; the live PR body (I read `push/pr_body_ks1952.final.md`, the file the chain created from; its equality with the live body was not re-read at the API); GitHub PR comments.

---

## NOT TESTED (all three)
- The GitHub API: PR state, live bodies, PR comments, the open-PR list by API (I used a git census).
- Linear: the ticket comments are read from the seats' drafts and records.
- Schemathesis, Akto, Playwright, k6, any live stack, demo or kintsugi.
- The pre-push hook output (quoted by the seats, not re-read by me).

## Scratch
Kept in place under `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/15181365-5e12-4b94-a706-b81bce923a5c/scratchpad/`: `r.git`, `w/*`, `runs/`, `mut2159/`, `probe/`. Every mutated file in the worktrees was restored with `git checkout`, and `git status` is clean apart from the node_modules symlinks.
