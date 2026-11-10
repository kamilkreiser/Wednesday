GATE B1405: GO WITH FINDINGS @ 6c30d69 on main 97cf7a9

Round 2 of 2. Tier G1 (product code), per kit S8. Project MPS Calculator, repo datasecau/MPS-Commercial-Calculator.
Branch b1405/mps-feedback-backend = 6c30d691fb5a131eb34d9c38821f6d7ae9600fe4 (git ls-remote over SSH, 09:20:42 AEDT) = READY sha.
Main now 97cf7a9af9dfd6cf20e66fc8d0bc19454a4d9e4b (since round 1: 8d665e3f infra/scripts and 97cf7a9a Sources; neither touches a Feedback path).
Verifier clone and worktrees: this gate's session scratchpad (v2/clone), push URL no-push://invalid, never pushed. No gh API, no Jira, no az, no HTTP to a hosted host (git over SSH with the deploy key, read only: ls-remote and fetch). Restore offline from the machine package cache only. Test suites run serially; no listener opened (all tests in-process).

Why GO WITH FINDINGS, in one line: the round-1 blocker is fixed. A refused upload (429, 200 replay, 422 key reuse) now writes nothing, measured with the builder's rows, the gate's own probes and real (unheld) races, and every other check passes at head and at the merge with today's main. What remains is a docs sentence on another lane's file and two small client-visible notes.

## Round-1 findings, re-verified at 6c30d69

| R1 # | Round-1 finding | Re-check (instrument) | Now |
|---|---|---|---|
| F1 | Concurrent uploads wrote files the limit/key then refused; 16 uploads at limit 1 left 16 folders, 128 MiB | (a) the builder's 3 new rows at head: green; same rows on 2c7d5c2 product code: red ("collection contained 16 items" x2, "Collections differ"). (b) gate probe P3, no seams, real races, 3 rounds: 32 distinct-key uploads at limit 4 -> 201 x4, 429 x28, items 4, folders 4; 32 same-key uploads -> 201 x1, 200 x31, items 1, folders 1. Same at main. Under a gate mutant (reservations not counted, in-flight key not waited for) the same probe gives 8-17 folders: the probe can fail. (c) P2: a 429 caused by an in-flight upload: folders while held 1, after 1 (the stored item's) | FIXED |
| F2 | docs/API.md (lane M11's) contradicted by the 124 change | read at main 97cf7a9 with awk NR | PARTLY: :725 ("nothing is stored" on 429) and :745 ("Any refusal stores nothing") are true again. :749-750 ("under the store's lock ... the attachments, and the item file last") is still false (attachments are written outside the lock by design). :722-723 ("counted from stored items") is now incomplete (in-flight uploads count too). Not editable in this lane. Finding N1 below |
| F3 | Builder RESIDUE and handoff note understated F1 | STATUS read | The ADDENDUM-1 section is accurate; the earlier RESIDUE line "a submit that loses a same-key (or hourly-limit) race ... leaves an orphan attachments folder" and handoff note 3(b) were left in place and now describe behaviour that no longer exists (superseded, not corrected). Minor N4 |
| F4 | Unshown: run C, planted re-check fault, Jira, open PRs | - | Planted fault for the new code reproduced by the gate (mutant B below). Run C at the new head: not claimed by the builder, NOT RUN here. Jira and open-PR state: still not readable by this gate (fence) |
| F5 | Landing note: 125 built on 124's file | commit list | Still true (124 is now commits 4 and 6). A squash lands all six as one; no action |
| F6 | 122 headers on refusals; openapi lists them on 200 only | contract test in the full run | Unchanged; contract test green at head and merge. Info |

## Results by step (new head)

| # | Check | Instrument | Control | Result |
|---|---|---|---|---|
| 1 | Branch = READY | git ls-remote origin | main read in the same call | 6c30d691 = READY; PASS |
| 1 | Paths in OWNS | git diff --name-only 31234f5f..head | - | 10 paths, all under src/MpsCalc.Api/Feedback/** or tests/MpsCalc.Api.Tests/Feedback*.cs; 2c7d5c2..head touches 2 of them (FeedbackStore.cs, FeedbackUploadLockTests.cs); PASS |
| 1 | Forward commits only | merge-base --is-ancestor 2c7d5c28 head | - | rc 0 (fast-forward of round 1); 6 commits over S2; PASS |
| 1 | Overlap: sibling branches and PR heads | fetched origin b140* / b14/* and refs/pull/*/head; diff from merge-base for Feedback paths | own branch counts 10 | b1402, b1403, b1404, b1406, b1407, b14/infra-ci-deploy-demo: 0 Feedback paths. PR heads touching Feedback paths (#32, #39, #94, #96, #125, #128, #130, #131) are each squashed onto main ("(#n)" 1 each). Main's new commits 8d665e3f and 97cf7a9a: 0 Feedback paths, and no Feedback file names a Sources type (git grep, 0). 0 overlap. Open state NOT read (no API) |
| 2 | Merge | git merge-tree --write-tree main head | stale PR #152 head vs main: rc 1 | rc 0, tree 64f2909d. Merge vs main = exactly the 10 lane files, each = head blob; merge vs head = exactly main's 12 files since S2, each = main blob. Clean; PASS |
| 3 | CI job dotnet at main / head / merge | SDK 10.0.401 (global.json 10.0.100 latestFeature); dotnet build MpsCalc.slnx -c Release; dotnet test --no-build; trx counts by program | - | build rc 0, 0 Warning(s), 0 Error(s) at all three. main: Engine 743, Import 196, Api 3398 = 4337. head: 743/196/3399 = 4338. merge: 743/196/3430 = 4369. main -> merge: lost 0, gained 32 = exactly the lane's rows (Overlap 9, RetryRace 2, DownloadHeader 11, DuplicateKey 3, UploadLock 7). head -> merge: lost 0, gained 31 (main's #168 15 + #170 16). main -> head "lost" 1 TemplateIsolation row: a main row the older base lacks; present and green at the merge. PASS |
| 3 | Other CI jobs (web, python, package) | ci.yml at head (identical to main); none reads a changed path | - | NOT RUN (see below) |
| 3 | Repo-wide hidden characters | own python walk of tracked text files, Unicode Cf, main/head/merge | planted U+200B counts 1 | 682/686/688 files; 21 hits in the same 7 pre-existing files at all three; delta 0; PASS |
| 3 | Link check | - | - | no such job in the repo; NOT RUN |
| 4 | Red without the fix, new rows | 2c7d5c2 product code + head test file, FeedbackUploadLockTests | runner rc 1 | 7 run, 4 red: Sixteen distinct (16 folders), Sixteen same-key (16 folders), 429 row (Collections differ), Two-uploads row ("did not wait"). Green: the JSON/list row and both release rows (no reservation exists to leak at 2c7d5c2, as the builder says). PASS |
| 4 | Red without the fix, release rows | mutant B: head with the reservation removal deleted; --blame-hang-timeout 90s | - | both A_write_that_fails_midway rows red, "System.TimeoutException". Not vacuous; PASS |
| 4 | Red without the fix, the 21 earlier rows | mutant m21: head with src of 97, 122, 125 reverse-applied, 102 split into two lock scopes around its seam, 124 attachment writes put back under the lock | runner rc 1 | build 0 warnings; Feedback* 281 run, 20 red: 97 x7, 122 x9, 125 x2, 102 x1, 124 JSON/list x1 (the 21st round-1 red was the replaced round-1 row). All other Feedback rows green, i.e. the 249 earlier Feedback tests stay green. PASS |
| 4 | Gate mutant A (reservations not counted in the limit; in-flight same key not waited for) | head + mutation | - | 9 red: the 4 new rows above plus probes P1, P2, P3 x3. The new rows pin both halves of the fix. PASS |
| 5 | Closed lines | - | - | No ALREADY-ON-MAIN line in STATUS. Main 97cf7a9 still holds the pre-fix shapes (Submit under one lock; no Feedback path changed since S2) |
| 6 | Probe P1: JSON submit, same key, other body, during a held upload | probe Fact, throw-away tree | mutant A: answered at once with 201, 2 items | head: waits (not answered in 3 s while held), then 422 IDEMPOTENCY_KEY_REUSED; items 1, folders 1. PASS |
| 6 | Probe P2: limit 2, 1 stored, upload A held, upload B (other key) | probe Fact | mutant A: B 201, 2 folders while held | head: B 429 at once, folders while held 1 (A's), after 1; Retry-After on B = 1; then C after A commits: 429, Retry-After 3600. Behaviour PASS; Retry-After 1 is finding N2 |
| 6 | Probe P3: real races, no seams, 3 rounds | probe Theory | mutant A: 8-17 folders | head = main: 4 items / 4 folders of 32 distinct at limit 4; 1 item / 1 folder of 32 same-key. PASS |
| 6 | Probe P4: false 429 from the commit-to-release window | 300 pairs of concurrent distinct-key uploads per fresh caller at limit 2 | - | head 0 false 429 (main 0). The window exists by reading (the item is stored in one lock scope, the reservation dropped in the next, so for an instant one item counts twice); not observed. Info N5 |
| 6 | Read of the new Submit | source | - | Replay/key-reuse check, then reservation, both under the first lock acquisition; ArgumentException for a files mismatch is thrown before any reservation; the finally releases the reservation and completes its signal on success, IOException/UnauthorizedAccessException and any other exception; a waiter re-checks after the signal (replay, KeyReused, or reserves after a failed first). No path writes before reserving. Same-key waiters block a thread on Task.Wait (Info N3) |
| 6 | Code-fact sentences | docs/API.md at main | - | see F2 row above (N1) |
| 7 | Name scan, added lines (1066) and the 6 commit messages; also 2c7d5c2..head (200 lines, 1 message) | python `(?<![A-Za-z])<name>(?![a-z])`, case-insensitive; ban list plus the three coordinator names | planted _by_<name>_ controls fire (two names) | 0 and 0; PASS |
| 7 | Secrets, ids, hosts, B-numbers, seat ids, Cf / non-ASCII | regexes over the same text; gitleaks git over 31234f5f..head | random ghp_ canary rc 1; planted B-number, U+200B, ghp_ fire | gitleaks rc 0; 0 secrets, 0 B-numbers, 0 seat ids, 0 non-ASCII. Only the synthetic GUIDs ...a1 and the synthetic atlassian test host from round 1 (already on main in other tests); the new commit adds none. PASS |
| 9 | Tier | S8: G1 | | the round-1 security-shaped issue is closed by measurement; no new one found |

## Builder STATUS claims (ADDENDUM-1 section) graded

| Claim | Grade |
|---|---|
| One forward commit 6c30d691 on 2c7d5c2; no amend, rebase or force | true |
| Reserve under the first lock before any byte; replay/limit answered before writing; release on every path; deleting shape not used | true (source read; probes P1-P3; mutant B) |
| New rows red at 2c7d5c2 with the quoted reasons, green at head | true (4 red, reasons match; release rows green at 2c7d5c2 as disclosed) |
| Planted fault: removal deleted -> both release rows TimeoutException | true (reproduced) |
| Head: build 0 warnings; 4338 passed (Api 3399) | true |
| Merge with 089a6393: 4353 passed | not re-run at 089a6393; consistent with this gate's merge at 97cf7a9 (4369 = 4353 + #170's 16) |
| 30 removed test lines, all inside the replaced unlanded round-1 row; 0 existing test files modified vs S2 | true (numstat; the only removed test method is that row; 0 modified test files vs S2) |
| Proof 3: earlier rows still red without their fixes | builder NOT RUN; gate ran it: true (20 = 21 minus the replaced row) |
| docs/API.md :725 true again, :749-750 still false, :722-723 incomplete | true |
| Push: ahead 6, behind 3, 10 files | true at 09:01 (main has since moved once more: behind 4) |
| Properties over 2c7d5c2..head and the whole branch (1066 lines, 0 non-ASCII, 0 names/ids, gitleaks rc 0) | true |
| Flaky red (git check-ignore child killed, exit 137) seen once in a filtered run | not shown here: 0 reds in this gate's head and merge full runs |
| Self-reported slips (compare read after the push; `git checkout -- .` in a throw-away tree) | self-reported; no effect found on the branch |

## Findings

| # | Severity | Finding |
|---|---|---|
| N1 | Minor (landing condition) | docs/API.md (lane M11's path, not editable here): :749-750 says the attachments are written under the store's lock; at head they are written outside it, after a reservation. :722-723 says the limit counts stored items; at head it also counts the caller's uploads still being written. Neither misleads a client about what is stored (:725 and :745 are true again). Needs a docs change by M11 or a follow-up ticket, in the same landing order |
| N2 | Minor | When a 429 is caused by the caller's own upload still being written, Retry-After is 1 (measured, P2); a retry after A commits then gets 429 with Retry-After 3600. The client is told "1 second" when the real wait may be up to an hour. Not a storage or security issue; a ticket-sized follow-up (count reservations in RetryAfterSeconds, or document it) |
| N3 | Info | Same-key requests that arrive while an upload of that key is being written wait with a blocking Task.Wait (one thread each, for one write's duration). Main held every submit on the lock, so this is not worse than main; it is the opposite direction from main's #170 ("waits hold no thread") |
| N4 | Minor | Builder STATUS: the round-1 RESIDUE 124 line and handoff note 3(b) still describe the replaced behaviour (orphan folder after a lost race; 201/200 "whichever arrived first"); the ADDENDUM-1 section is the accurate record |
| N5 | Info | By reading only: between the item commit and the reservation release, one item counts twice for an instant, so a concurrent other-key request could get a false 429 near the limit. Fails closed; 0 in 300 measured pairs |
| N6 | Info | Commits 1-3 and 5 unchanged since round 1 and pass every check again (m21 reds; full runs). Author/committer is the repo's noreply identity |

Deploy: ci.yml has no deploy job ("NO deploy job" header). A squash onto main runs ci on main; the package job keeps a 7-day artifact, which is not a deploy (deploying is a manual runbook step). A merge triggers no deploy.

## NOT RUN
- Hosted CI (dotnet, web, python, package) and CodeQL: hosted CI and CodeQL on the PR are the proof.
- web, python and package jobs locally: no test in them reads a changed file (ci.yml identical to main); python needs `az bicep install`, which this gate may not run; package needs the web build.
- Open-PR state and Jira through the API (fence); overlap shown from fetched refs.
- Run C (each commit alone) at the new head.
- The merge at 089a6393 (the builder's merge); this gate's merge is at current main 97cf7a9.
- The NFD rows' Linux (ext4) branch: APFS here; CI only.
- Link check: no such job in the repo.
