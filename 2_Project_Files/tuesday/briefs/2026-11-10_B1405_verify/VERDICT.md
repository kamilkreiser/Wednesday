GATE B1405: NO GO @ 2c7d5c2 on main 089a639

Tier: G1 (product code), per kit S8. Project MPS Calculator, repo datasecau/MPS-Commercial-Calculator.
Branch b1405/mps-feedback-backend = 2c7d5c28863f7cad79497258e3c5c8940f725caa (git ls-remote 08:00:56 and again 08:23:43 AEDT) = READY sha.
Main now 089a63939c5b787168264862b35919e895b0211d (S2 base 31234f5f plus #167 docs/IMPORTER.md and #168 TemplateIsolationTests.cs; neither touches a Feedback path).
Verifier clone: session scratchpad v1405/clone, push URL no-push://invalid, never pushed. No gh API, no Jira, no az, no HTTP to a hosted host (git over SSH with the deploy key, read only: ls-remote and fetch). Restore from the local package cache only (--source ~/.nuget/packages).

Why NO GO, in one line: the MPSCALC-124 commit (4f61a22) lets concurrent uploads write attachment files that the hourly limit and the idempotency key then refuse, and those files are never deleted. Measured: 16 concurrent uploads under a limit of 1 leave 16 attachment folders (128 MiB) for 1 stored item at head, against 1 folder (8 MiB) at main. That is a storage bound any signed-in caller can bypass, and it contradicts docs/API.md (a 429 "nothing is stored"). The other four commits pass every check.

## Results by step

| # | Check | Instrument | Control | Result |
|---|---|---|---|---|
| 1 | Branch = READY | git ls-remote origin (twice) | refs/heads/main read in the same call | 2c7d5c28 = READY; PASS |
| 1 | Paths in OWNS | git diff --name-only 31234f5f..head; fnmatch on src/MpsCalc.Api/Feedback/**, tests/MpsCalc.Api.Tests/Feedback*.cs | planted web/x.ts falls outside: True | 10 of 10 in OWNS, 0 outside; PASS |
| 1 | Overlap with sibling lanes | fnmatch of the 10 paths over the 36 globs of M1-M5, M8-M11; grep of the 10 sibling kits for the Feedback paths | LaneM4x.cs matches LaneM4*.cs: True | 0 overlaps. Sibling kits name the Feedback paths only in their PARTITION or "NOT yours" rows; PASS |
| 1 | Overlap with open PRs / pushed branches | fetched refs/pull/*/head (168) and origin b14* refs; diff from merge-base for Feedback paths | - | PR heads touching Feedback paths: #32, #39, #94, #96, #125, #128, #130, #131, all squashed onto main ("(#n)" in the main log, 1 each). #167 and #168 are main's two new commits. b1402 and b1406 do not touch Feedback paths. 0 overlap. Open state NOT read (no API) |
| 2 | Merge | git merge-tree --write-tree main head | stale PR #152 head vs main: rc 1 | rc 0, tree b26d95b2. Merge vs main differs in exactly the 10 lane files, each = the head blob. Merge vs head differs in exactly docs/IMPORTER.md and TemplateIsolationTests.cs, each = the main blob. Clean; PASS |
| 3 | CI job dotnet at main / head / merge | SDK 10.0.401 (global.json 10.0.100, latestFeature); dotnet build MpsCalc.slnx -c Release; dotnet test --no-build; counts by program from trx | - | build rc 0, 0 Warning(s), 0 Error(s) at all three. trx all Passed: main Engine 743, Import 196, Api 3382; head 743 / 196 / 3394; merge 743 / 196 / 3409. main to merge: lost 0, gained 27 (the lane's 27 rows). head to merge: lost 0, gained 15 (main's #168 rows). main to head shows 15 "lost": the #168 rows, which the older head base does not contain; the merge has them all. PASS |
| 3 | Other CI jobs (web, python, package) | read ci.yml at head; git grep of tools/demo/test, infra/tests, scripts/tests, web/scripts, web/src for the changed paths | - | none reads a changed file. package runs dotnet publish of src/MpsCalc.Api, which the Release build covers. Not run (see NOT RUN) |
| 3 | Repo-wide hidden characters (tracked text files) | own python walk, Unicode Cf, main / head / merge | planted U+200B counts 1 | 680 / 686 / 686 files; 21 Cf hits in the same 7 pre-existing files at all three; delta 0; PASS |
| 3 | Link check | - | - | the repo has no link-check job; NOT RUN |
| 4 | Red without the fix | throw-away tree from head: src of the 97, 122 and 125 commits reverse-applied; 102 mutant = RequeueTicket with the read and the write in two lock scopes (main's shape) and the seam between them; 124 mutant = the whole Submit under one lock (main's shape) with the seam kept; Api.Tests filtered to Feedback* | runner exits 1 | build rc 0, 0 warnings; 276 run, 21 failed, rc 1. The 21 reds are exactly the 27 new rows minus their 6 controls (2 overlap controls, DevStub 200, hosted 200, Both_items_stay_stored_and_listed, the retry control); reason lines match the builder's. All 249 earlier Feedback tests green. Not vacuous; PASS |
| 5 | Closed lines | grep -n at main 089a6393 | - | No ALREADY-ON-MAIN line in STATUS (all five WORK). The PRIOR WORK "main does not fix it" pointers hold at main: FeedbackEndpoints.cs:376 StateOf, :385 SaveTicket, :427 headers after the refusals; FeedbackStore.cs:237 RealPath, :291 last-wins _byKey, :445 lock over the writes. main moved no Feedback path since S2 |
| 6 | Probe: MPSCALC-124 storage vs the hourly limit | probe Theory in a throw-away copy of head and of main: 16 concurrent multipart uploads, 2 x 4 MiB PNG each, released together | same probe at main | head, distinct keys, PerHour=1: 201x1, 429x15, items 1, attachment folders 16, 134,217,728 bytes. main: 201x1, 429x15, items 1, folders 1, 8,388,608 bytes. FAIL (finding F1) |
| 6 | Probe: MPSCALC-124 same key, same body | as above | same probe at main | head: 201x1, 200x15, items 1, folders 7, 58,720,256 bytes. main: folders 1, 8,388,608 bytes. Six replays (200) each left 8 MiB on disk. FAIL (F1) |
| 6 | Probe: MPSCALC-124 deterministic | head seam BeforeAttachmentRename holds upload 1; upload 2 (another key) is stored under PerHour=1; upload 1 released | - | upload 1 answers 429 FEEDBACK_RATE_LIMITED, but its attachment folder and file stay on disk (folders 2, items 1). A 429 now stores files. FAIL (F1) |
| 6 | Probe: MPSCALC-102 | read of RequeueTicket, the worker's AttemptAsync and StateOf | - | Read and write are one lock scope; the retry answers the state it read, which equals StateOf with Jira on (sidecar state, else pending). With Jira off nothing is written, as before. A worker save of failed or pending after the retry's pending write is the pre-existing order, not in this ticket. PASS |
| 6 | Probe: MPSCALC-122 | read of Download; DevStub and hosted rows | - | headers set before the role check; ApiProblem bodies and status codes unchanged; Content-Disposition only on the 200; hosted Referrer-Policy kept. PASS |
| 6 | Probe: MPSCALC-125 | read of Load; key validity at load (FeedbackStore.cs:529 requires a non-empty key) | - | grouping is by (SubmittedBy, IdempotencyKey) with the same ordinal compare as _byKey; null keys cannot reach it; the log line carries ids only (row asserts it). PASS |
| 6 | Probe: MPSCALC-97 | read of RefuseOverlap, Spellings, RefuseLinkedOverlap, FeedbackPathIdentity | - | stat layouts match macOS (stat$INODE64 on x64, stat on arm64) and Linux x64/arm64 (st_dev at 0, st_ino at 8); a missing entry point falls back to the name compare. A dangling reference link now refuses a DevStub start too (builder discloses it). PASS |
| 6 | Code-fact sentences | docs/API.md at head, Attachments and Rate limit paragraphs | - | docs/API.md:725 "...nothing is stored" (429) and :749-750 "under the store's lock the idempotency check, the attachments, and the item file last" are false at head. docs/API.md is lane M11's path, so the builder could not change it (F2) |
| 7 | Name scan, added lines (930) and the 5 commit messages | python `(?<![A-Za-z])<name>(?![a-z])`, case-insensitive; ban list plus Friday, Tuesday, Wednesday | a planted _by_<name>_ control fires | 0 and 0; PASS |
| 7 | Secrets, GUIDs, hosts, B-numbers, seat ids, Cf / non-ASCII | regexes over the same text; gitleaks 8.30.1 git over 31234f5f..2c7d5c28 | random ghp_ canary dir rc 1; a planted B-number, U+200B and ghp_ fire | 0 secrets, 0 B-numbers, 0 seat ids, 0 non-ASCII. Hits: two synthetic GUIDs (0000...a1, ffff...a1) and syn-site.atlassian.net, which already appears in 3 test files on main. gitleaks rc 0; PASS |
| 8 | Builder claims | below | | |
| 9 | Tier | S8: G1 | | security-shaped issue found on a G1 lane (F1): NO GO |

## Builder STATUS claims graded

| Claim | Grade |
|---|---|
| Base 31234f5f = S2, 5 commits, ahead 5 behind 2 at push, files exactly the 10 lane paths | true |
| main moved to 089a6393 by docs/IMPORTER.md and TemplateIsolationTests.cs only | true |
| Baseline 4306 passed (Engine 743, Import 196, Api 3367) | true by derivation (main 089a6393 Api 3382 = 3367 + #168's 15) |
| Head 4333 passed, Api 3394, 0 warnings; lost 0; gained exactly 27 | true |
| 27 rows = Overlap 9, RetryRace 2, DownloadHeader 11, UploadLock 2, DuplicateKey 3 | true (by trx names and the source) |
| Red run: 7 + 9 + 2 reds for 97, 122, 125 with the quoted reason lines | true (reproduced by reverting the fix) |
| Seam-only reds for 102 (1) and 124 (2) | true (reproduced with main-shaped mutants) |
| Run C: each commit alone builds and passes Feedback* | not shown (not re-run) |
| Planted fault: 124 re-check removed turns the two-upload row red | not shown (not re-run) |
| Properties: 930 added lines, 0 non-ASCII, 0 names, 0 ids; gitleaks range rc 0 | true |
| PRIOR WORK pointers (:376, :385, :404-429, :445, :291, :229-255) | true at main 089a6393 |
| Jira states and comments; merged PR read #1 to #166 | not shown (Jira and API not read by this gate) |
| RESIDUE 124: a lost race leaves an orphan folder; "not new behaviour for the store ... a new way to reach it" | false in effect: the measured orphan volume is bounded only by concurrency, not by the hourly limit, and a 429 now leaves files. Not disclosed: the rate-limit case and the docs/API.md contradiction |
| FOR TUESDAY 3(b): the only client-visible 124 change is 201 / 200 in a same-key race | incomplete: a 429 or 422 refusal can now leave stored files (status codes unchanged) |
| NuGet restore read api.nuget.org (FOR TUESDAY 1) | self-reported; the two packages are now in the machine cache, so this gate restored offline |

## Findings

| # | Severity | Finding |
|---|---|---|
| F1 | Major (security-shaped, tier G1): NO GO | MPSCALC-124 (commit 4f61a22, FeedbackStore.Submit): the attachment files are written between two lock scopes, so every concurrent request that passes the first check writes up to 15 MiB of files even when the second check then refuses it (429 rate limit, 200 replay, 422 key reuse). Those folders are never deleted, never counted toward the hourly limit, and only named at the next start. Measured: 16 concurrent uploads under PerHour=1 left 16 folders, 128 MiB, for 1 stored item (main: 1 folder, 8 MiB). Same key and same body: 7 folders, 56 MiB (main: 1). Any signed-in caller can fill the feedback disk past the limit, at a rate set by how many requests they can keep open at once. Suggested shape for a fix round, inside the lane: reserve the (caller, key) and an hourly-limit slot under the first lock (an in-flight set counted by Settled), so a second same-key or over-limit request is answered before it writes anything. Release the reservation on commit or failure. The existing seam rows plus a 429 row (the deterministic probe above) would pin it. Alternatives (remove the lost race's own new folder) touch the "never deleted" rule and are the product owner's call |
| F2 | Major (follows F1) | docs/API.md at head (lane M11's path, not editable here): :725 says a 429 stores nothing, and :749-750 says the attachments are written under the store's lock. Both are false at head. Whatever lands for 124 needs a docs/API.md change in the same landing order (M11's lane, or a follow-up ticket) |
| F3 | Minor | Builder RESIDUE and FOR TUESDAY 3(b) understate F1 (see claims) |
| F4 | Minor | Unshown: run C, the planted re-check fault, Jira text and states, open-PR state |
| F5 | Info | Commits 2a86f71 (97), 232bd42 (102), 09f43e3 (122) and 2c7d5c2 (125) pass every check here. Commit 5 is built on commit 4's file, so landing 1-3 and 5 without 4 needs a new branch with 4 left out (not a gate action). Author/committer is the repo-local identity, as on earlier seat branches |
| F6 | Info | MPSCALC-122 changes what a refusal carries (nosniff, no-store, sandbox CSP); docs/api/openapi.json lists those headers on the 200 only (M11's path). The contract test passes as is |

Deploy: ci.yml has no deploy job ("NO deploy job" header). A squash onto main would run ci on main, and the package job would keep a 7-day artifact. That artifact is not a deploy (deploying is a manual runbook step). A merge triggers no deploy.

## NOT RUN
- Hosted CI (dotnet, web, python, package) and CodeQL: NOT RUN here; hosted CI and CodeQL on a PR are the proof.
- web, python and package jobs locally: NOT RUN (no test in them reads a changed file; python needs `az bicep install`, which this gate may not run; package needs the web build).
- Open-PR state and Jira through the API: NOT RUN (fence). Overlap was shown from fetched refs/pull heads.
- Run C (each commit alone), the builder's planted re-check fault: NOT RUN.
- The NFD rows' Linux (ext4) branch: NOT RUN here (APFS); CI only.
- Link check: no such job in the repo.
- No PR files were written (NO GO).
