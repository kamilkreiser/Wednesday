# Secuura open-PR census — `Secuura/Distributed_Secuura`, base `develop` — 2026-09-12 (seat 14:50)

READ-ONLY census. No writes to any repo, ticket or PR.

## BLUF

- **Open PRs on `develop`: 49.** Pagination exhausted: 1 page at per_page=100, no `rel="next"`. All 49 open PRs in the repo target `develop`.
- **Per class:** TESTED-AT-HEAD 4 · NO-GO-AT-HEAD 1 · GATED-OLDER-HEAD 5 · UNGATED 24 · WORKFLOW 4 · NOT-OURS 11 · AMBIGUOUS 0.
- **TESTED-AT-HEAD (merge candidates now):**
  - **#960** head `0e70ed1c77e1f832a4ab165152e024926be509a0` (mergeable_state `unstable`)
  - **#928** head `e28d64b8d0bb4ee354c7790bafa24db22c0f9471` (mergeable_state `clean`)
  - **#926** head `542492c41f551086d81acdc0817ce4d48e8a14fb` (mergeable_state `clean`)
  - **#913** head `fdd8af79d5daaddef54f5bc73fb3e2845290f94e` (mergeable_state `clean`)
- **Positive controls:** (a) #960 → TESTED-AT-HEAD at `0e70ed1c77e1f832a4ab165152e024926be509a0`, GO WITH FINDINGS, report dir `2026-09-12-ks1099-960-0e70ed1c7-tier2-r1` — **PASS**. (b) #961 → UNGATED (the only record is the builder's "READY FOR QA … The QA gate runs next" Linear note) — **PASS**. #958 is absent from the open list (merged), as expected.
- **Caveats for the merge decision (not class criteria):**
  - #913, #926 and #928 were gated on 2026-09-09 and have not moved since (1 commit each, no force-push). `develop` has moved since, so the gate did not see today's base.
  - #926's gate report says it branched from `b6884888d`, which is behind develop.
  - #960's `mergeable_state` is `unstable`: a required or non-required check is not green.
- **NO-GO-AT-HEAD:** #912.
- **GATED-OLDER-HEAD:** #930, #927, #925, #924, #799. All gated verdicts predate a later push:
  - #930's NO GO was answered by a round-2 push that has no gate yet;
  - #924, #925 and #927 each got a GO WITH FINDINGS and were then pushed with fixes.
- **WORKFLOW (Kam merges):** #942, #941, #940, #887.
- **NOT-OURS:** #959, #949, #948, #947, #946, #945, #649, #639, #635, #575, #572.

## Table

| PR | author | head | class | verdict @ SHA · tier · date · where | tickets | Test Evidence | mergeable_state | files | reviews (count — latest decisive per reviewer @ commit) |
|---|---|---|---|---|---|---|---|---|---|
| #961 | kksecura | `644965d90` | **UNGATED** | none found | KS-1098 | y | unstable | 2 | 0 — - |
| #960 | kksecura | `0e70ed1c7` | **TESTED-AT-HEAD** | GO WITH FINDINGS @ `0e70ed1c7` (= HEAD) · T2 r1 · 2026-09-12 · Testing Agent MAIN/projects/secuura/reports/2026-09-12-ks1099-960-0e70ed1c7-tier2-r1/report.md | KS-1099 | y | unstable | 3 | 0 — - |
| #959 | PeterObeden | `c7b6a2475` | **NOT-OURS** | none found | KS-1016, KS-1096, KS-256, KS-666, KS-972 | y | unstable | 4 | 0 — - | draft
| #949 | dependabot[bot] | `7ee1a26e6` | **NOT-OURS** | none found | - | n | unstable | 2 | 0 — - |
| #948 | dependabot[bot] | `0e8221a8c` | **NOT-OURS** | none found | - | n | unstable | 10 | 0 — - |
| #947 | dependabot[bot] | `d68b9d79e` | **NOT-OURS** | none found | - | n | unstable | 2 | 0 — - |
| #946 | dependabot[bot] | `41cc5209a` | **NOT-OURS** | none found | - | n | unstable | 2 | 0 — - |
| #945 | dependabot[bot] | `264098fce` | **NOT-OURS** | none found | - | n | unstable | 2 | 0 — - |
| #943 | kksecura | `4e1bd16ec` | **UNGATED** | none found | KS-1041, KS-535, KS-601 | y | unstable | 2 | 0 — - |
| #942 | kksecura | `c1676269d` | **WORKFLOW** | none found | KS-1075, KS-1078 | y | dirty | 3 (WF: .github/workflows/pr-security-gates.yml) | 0 — - |
| #941 | kksecura | `d105e07a8` | **WORKFLOW** | none found | KS-1046, KS-1075, KS-1077 | y | unstable | 2 (WF: .github/workflows/security-scan.yml) | 0 — - |
| #940 | kksecura | `1aa708be9` | **WORKFLOW** | none found | KS-1046, KS-1075 | y | unstable | 1 (WF: .github/workflows/security-scan.yml) | 0 — - |
| #939 | kksecura | `481e0267f` | **UNGATED** | none found | KS-1046, KS-1058, KS-1067, KS-1068, KS-1074, KS-927 | y | unstable | 3 | 0 — - |
| #937 | kksecura | `cf8b23366` | **UNGATED** | none found | KS-1059, KS-1067, KS-444, KS-587 | y | unstable | 4 | 0 — - |
| #932 | kksecura | `c72607d58` | **UNGATED** | none found | KS-1055, KS-1062, KS-667 | y | clean | 1 | 0 — - |
| #931 | kksecura | `f2e0cb3c1` | **UNGATED** | none found | KS-1051, KS-1061, KS-444, KS-563, KS-584, KS-927 | y | clean | 12 | 0 — - |
| #930 | kksecura | `7e5ae31d8` | **GATED-OLDER-HEAD** | NO GO @ `d491c72c1` (older head) · T1 r1 · 2026-09-09 · Testing Agent MAIN/projects/secuura-blockchain-auth/reports/2026-09-09-pr930-ks1052-tier1/report.md (round 2 pushed as 7e5ae31d8 at 14:14Z per KS-1052 builder comment; no round-2 gate found) | KS-1050, KS-1052, KS-781, KS-963 | y | dirty | 8 | 0 — - |
| #928 | kksecura | `e28d64b8d` | **TESTED-AT-HEAD** | GO WITH FINDINGS @ `e28d64b8d` (= HEAD) · T1 r1 · 2026-09-09 · Testing Agent MAIN/projects/secuura-blockchain/reports/2026-09-09-s161-batch-six-prs/report.md (pins table + §1) | KS-1046, KS-773, KS-950 | y | clean | 1 | 0 — - |
| #927 | kksecura | `1041d2d32` | **GATED-OLDER-HEAD** | GO WITH FINDINGS @ `63e955e0f` (older head) · T2 r1 · 2026-09-09 · Testing Agent MAIN/projects/secuura-blockchain/reports/2026-09-09-s161-batch-six-prs/report.md | KS-1027, KS-992 | y | clean | 2 | 1 — PeterObeden: APPROVED@63e955e0f |
| #926 | kksecura | `542492c41` | **TESTED-AT-HEAD** | GO WITH FINDINGS @ `542492c41` (= HEAD) · T2 r1 · 2026-09-09 · Testing Agent MAIN/projects/secuura-blockchain/reports/2026-09-09-s161-batch-six-prs/report.md (pins table + §1) | KS-444, KS-927 | y | clean | 1 | 0 — - |
| #925 | kksecura | `8a5aff863` | **GATED-OLDER-HEAD** | GO WITH FINDINGS @ `0956c3dbe` (older head) · T2 r1 · 2026-09-09 · Testing Agent MAIN/projects/secuura-blockchain/reports/2026-09-09-s161-batch-six-prs/report.md | KS-1046, KS-773 | y | dirty | 1 | 0 — - |
| #924 | kksecura | `b85f1db24` | **GATED-OLDER-HEAD** | GO WITH FINDINGS @ `1497b39de` (older head) · T2 r1 · 2026-09-09 · Testing Agent MAIN/projects/secuura-blockchain/reports/2026-09-09-s161-batch-six-prs/report.md | KS-773 | y | clean | 1 | 0 — - |
| #923 | kksecura | `d127dc7d4` | **UNGATED** | none found | KS-570, KS-719, KS-736 | y | clean | 1 | 0 — - |
| #922 | kksecura | `2b5075e9f` | **UNGATED** | none found | KS-256, KS-679, KS-705 | y | clean | 5 | 0 — - |
| #920 | kksecura | `2112a99e3` | **UNGATED** | none found | KS-1038, KS-1039, KS-1040, KS-473, KS-734 | y | clean | 7 | 0 — - |
| #919 | kksecura | `d0aff46d4` | **UNGATED** | none found | KS-444, KS-536, KS-739, KS-74 | y | clean | 4 | 0 — - |
| #918 | kksecura | `ed954f09e` | **UNGATED** | none found | KS-1032, KS-1033, KS-1034, KS-666, KS-771, KS-926 | y | dirty | 3 | 1 — PeterObeden: COMMENTED@ed954f09e |
| #916 | kksecura | `584b12ba1` | **UNGATED** | none found | KS-1024, KS-1026, KS-993 | y | dirty | 3 | 0 — - |
| #913 | kksecura | `fdd8af79d` | **TESTED-AT-HEAD** | GO WITH FINDINGS @ `fdd8af79d` (= HEAD) · T1 r1 · 2026-09-09 · Testing Agent MAIN/projects/secuura-blockchain/reports/2026-09-09-ks963-pr913-tier1/report.md | KS-963 | y | clean | 2 | 1 — PeterObeden: COMMENTED@fdd8af79d |
| #912 | kksecura | `ae8751f38` | **NO-GO-AT-HEAD** | NO GO @ `ae8751f38` (= HEAD) · T1 r1 · 2026-09-09 · WEDNESDAY/2_Project_Files/fleet/qa-agent/reports/2026-09-09_secuura-ks1004-912-tier1-VERDICT.md; transcribed to Linear KS-1004 comment 2026-09-09T06:55Z and GitHub #912 issue comment 2026-09-09T06:55Z (both name no SHA; the report names ae8751f38) | KS-1004, KS-1017, KS-1019, KS-444, KS-520, KS-535, KS-587 | y | dirty | 3 | 0 — - |
| #905 | kksecura | `c38040bd1` | **UNGATED** | none found | KS-968, KS-991 | y | clean | 1 | 0 — - |
| #903 | kksecura | `a70f92d7c` | **UNGATED** | none found | KS-882, KS-991 | y | clean | 2 | 0 — - |
| #887 | kksecura | `cb7a3e3be` | **WORKFLOW** | none found | KS-444, KS-961 | n | blocked | 2 (WF: .github/workflows/pr-platform-suites.yml) | 3 — PeterObeden: CHANGES_REQUESTED@bb0502c80 |
| #881 | kksecura | `787771b97` | **UNGATED** | none found | KS-781, KS-797, KS-798, KS-799, KS-804, KS-819, KS-820, KS-822, KS-841 | n | blocked | 5 | 1 — PeterObeden: CHANGES_REQUESTED@787771b97 |
| #880 | kksecura | `85f8263c2` | **UNGATED** | none found | KS-458, KS-480, KS-577, KS-869 | y | clean | 3 | 2 — PeterObeden: COMMENTED@85f8263c2 |
| #879 | kksecura | `79f1fcb48` | **UNGATED** | none found | KS-926, KS-930, KS-945, KS-948 | y | clean | 2 | 1 — PeterObeden: APPROVED@79f1fcb48 |
| #874 | kksecura | `6f7885602` | **UNGATED** | none found | KS-796, KS-911, KS-912, KS-921, KS-926, KS-927, KS-928, KS-930, KS-933, KS-937, KS-942 | y | clean | 1 | 0 — - |
| #873 | kksecura | `7d8a3f0e4` | **UNGATED** | none found | KS-256, KS-914, KS-931, KS-933 | y | clean | 2 | 0 — - |
| #813 | kksecura | `54225cbbd` | **UNGATED** | none found | KS-388, KS-439, KS-663, KS-791, KS-794 | y | clean | 4 | 2 — PeterObeden: APPROVED@54225cbbd |
| #811 | kksecura | `6200833ff` | **UNGATED** | none found | - | y | clean | 1 | 1 — PeterObeden: COMMENTED@6200833ff |
| #809 | kksecura | `aa2270fe1` | **UNGATED** | none found | KS-693, KS-788 | y | clean | 2 | 0 — - |
| #805 | kksecura | `97e2161fa` | **UNGATED** | none found | KS-281, KS-319, KS-535, KS-584, KS-587, KS-705, KS-726, KS-774 | y | clean | 9 | 0 — - |
| #799 | kksecura | `38f6377b9` | **GATED-OLDER-HEAD** | PASS WITH FINDINGS (s118 SUMMARY) @ `124e98192` (older head) · through-code · 2026-09-03 · Testing Agent MAIN/projects/secuura/reports/2026-09-03-s118-four-heads/SUMMARY.md<br>unlabelled (3 Majors remain) @ `b36757f7a` (older head) · through-code · 2026-09-04 · Testing Agent MAIN/projects/secuura-blockchain/reports/2026-09-04-799-majors-landing-through-code/SUMMARY.md | KS-444, KS-643, KS-650, KS-742, KS-764, KS-779, KS-780 | y | unstable | 12 | 5 — PeterObeden: COMMENTED@7dfc7ebca |
| #720 | kksecura | `fcc611d29` | **UNGATED** | none found | KS-380, KS-444, KS-487, KS-649, KS-652, KS-657, KS-658, KS-660, KS-685 | y | clean | 2 | 0 — - |
| #649 | dependabot[bot] | `1d9198ac7` | **NOT-OURS** | none found | - | n | unstable | 22 | 0 — - |
| #639 | dependabot[bot] | `2069d852e` | **NOT-OURS** | none found | - | n | unstable | 3 | 0 — - |
| #635 | dependabot[bot] | `6cbc298f4` | **NOT-OURS** | none found | - | n | unstable | 2 | 0 — - |
| #575 | dependabot[bot] | `7d32d8ae4` | **NOT-OURS** | none found | - | n | unstable | 21 | 0 — - |
| #572 | dependabot[bot] | `c9a0598df` | **NOT-OURS** | none found | - | n | unstable | 2 | 0 — - |

## METHOD

### GitHub REST (Bearer token from the Blockchain `.env`, read in-process, never printed)

**Endpoints.** Every call returned HTTP 200 (0 non-200s) and needed exactly 1 page:
- `GET /repos/Secuura/Distributed_Secuura/pulls?state=open&base=develop&per_page=100` → 49 PRs.
- The same call without `base` → 49.
- Per PR:
  - `GET /pulls/N` for `mergeable`/`mergeable_state`, retried once after 3 s if null;
  - `/pulls/N/files`;
  - `/pulls/N/reviews`;
  - `/issues/N/comments`;
  - `/pulls/N/comments`.
- Per `kksecura` PR: `/pulls/N/commits` and `/issues/N/timeline`, for `head_ref_force_pushed` events.
- **Only #720 has force-push events (2).** The API returned null before/after SHAs for them, so SHAs pushed away from #720 are unknown.
- #720 has no gate record at any known commit either way.

**Field checks.**
- **Test Evidence:** regex `^\s*##\s*test evidence\b` (case-insensitive, multiline) on the PR body.
- **Workflow file:** any changed path starting `.github/workflows/`.
- **Tickets:** `(KS|PS)[-_ ]?\d+` over the title, body and head branch name. Note that bodies cite related tickets, so the ticket lists are wider than each PR's own ticket.

**GitHub gate search.** `QA GATE` over all issue comments and review bodies of all 49 PRs.
- Hits: 1 (the #912 NO GO transcription).
- That hit is also the instrument's positive control.

### Linear GraphQL (raw key, no Bearer)

- Query: `issue(id) { comments(first: 50, after) }`, paginated on `pageInfo.hasNextPage` and sorted client-side by `createdAt`.
- Coverage: 116 ticket ids, all HTTP 200, 0 errors. Every ticket fit in one page (max 42 comments, on KS-256).
- **Search 1:** `QA GATE|GO WITH FINDINGS|NO GO`.
- **Search 2 (broader):** `verdict|gate` together with `#N` or `pull/N`.
- **SHA-to-commit matching:** every 7–40-hex token in each comment was matched against every commit the PR carries.

**Hits read by hand:**
- **Gate records:** only KS-1004 (#912 NO GO, transcription). KS-1058 and KS-1041 carry gate verdicts for **#936** (merged) and **#951**, not for #939 or #943.
- **Not gates:**
  - builder READY FOR QA notes (#920, #922, #923, #916, #928, #960, #961, #881);
  - Peter's reviews (#799, #813, #873, #879, #880, #887, #903, #912, #913, #918, #919, #922, #927, #928);
  - the KS-1052 builder "round 2 pushed" note on #930, which quotes the earlier NO GO but is not a verdict at `7e5ae31d8`.

### Report directories

- `find ".../Testing Agent MAIN/projects" -type d -name reports` returned 7 directories. The 6 `secuura*` ones were scanned:
  - `secuura`: 100 subdirectories;
  - `secuura-blockchain`: 18;
  - `secuura-platform-k`: 4;
  - `secuura-blockchain-auth`, `secuura-blockchain-systemtest` and `secuura-ks969-892`: 1 each.
- `nexusai/reports` was **deliberately not read**: it belongs to Datasec, and reading it would be cross-client.
- Also scanned: `WEDNESDAY/2_Project_Files/fleet/qa-agent/reports/` (2 files).
- Total: 262 `*.md` files.

**Matching.** For each PR, a report was flagged on any of:
- the PR number in the folder or file name;
- `PR #N`, `#N` or `pull/N` in the text;
- any 7–40-hex token that is a prefix of any commit the PR carries;
- a folder name carrying one of the PR's linked ticket numbers.

Every flagged report was then read in context.

**Hits that were NOT gates of that PR:**
- **#932 `c72607d58`:** the builder checkout HEAD recorded in the #930 and #935 reports.
- **#873 `7d8a3f0e4`:** the checkout HEAD in the #889, #892 and #894 reports.
- **#813 `54225cbbd`:** the builder working tree, noted in the s125 KS-781 report.
- **#937 `cd8509faf`:** a shared KS-1067 lock commit examined by the #935 gate. The verdict is #935's.
- **#879 and #813:** named in the push-protocol and #953 reports as future pushes.
- **Ticket-folder matches** on KS-781, 796, 797, 804, 819, 820, 822, 869, 882, 914, 921 and 1041: gates of those tickets' OTHER PRs (#812, #815, #821, #835, #854, #861, #868, #870, #951). None names #874, #880, #881, #903 or #943.

**#799 attribution.**
- Through-code passes at `124e98192` (s118, PASS WITH FINDINGS), `04e9ef23d` (s119) and `b36757f7a` (majors-landing, no GO/NO GO label: "three Major findings remain").
- The head is now `38f6377b9`. Peter re-reviewed at `7dfc7ebca` (not a QA gate).

### Positive controls

- (a) #960 found in the report tree with its folder name, full head SHA and `## VERDICT: GO WITH FINDINGS`. The Linear builder note names `0e70ed1c7`. Result: TESTED-AT-HEAD. **PASS.**
- (b) #961 has no report and no verdict comment. Result: UNGATED. **PASS.**
- The instrument also found the #912 NO GO in all three locations (report, Linear, GitHub), which positively controls the search in each location.

### Not checked or limits

- **Gate reports outside the searched trees:** a verdict held only in a mail inbox, a session transcript or another path would be missed. AgentMail was not searched.
- **Report verdict wording is not uniform** (PASS, GO-with-findings, unlabelled). Attribution was made by reading, not by regex alone.
- **`mergeable_state` is a point-in-time GitHub computation** (read 2026-09-12 ~04:5xZ).
- **#720:** force-pushed-away SHAs were not recoverable from the timeline (null before/after).
- **Batch-report scope:** the s161 verdicts rest on its pins table. It asserts `refs/pull/N/head` matched at open and close. I did not re-derive that, but the SHAs equal today's heads for #926 and #928.
