GATE B1496: GO WITH FINDINGS @ 40217c1 on main 009421a

Tier 2 (pure string helper plus one initial value on the customer roadmap register; no auth, store shape or deploy surface). No security-shaped finding. No Blocker, no Major.
Gate clone: /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s268/gate1496/repo (own --no-hardlinks clone, push URL invalid://no-push-gate; node_modules by `npm ci --offline` from the local cache, no network). Logs and scripts sit beside it.

## Refs, merge, lane
- ls-remote: branch = 40217c1947f7d3b5d8e480658472cd3321b6b8b4 (equals READY); main = 009421a28616c8b31dde86b59d4c4ca674c288fa (re-read 18:1x, unchanged). Head's parent is main.
- 4 files, +82/-3, all four in the lane's OWNS (4 of 4): remediation-store.ts, remediation-store.test.ts, RoadmapScreen.tsx, RoadmapScreen.register.test.tsx. Nothing under api/, infra/, .github/, web/e2e, web/src/server. Open PR overlap: builder read #309 (11 files) and #310 (one csproj), none shared; not re-read by me (no gh call made).
- `git merge-tree --write-tree main head` rc 0, tree a2c6e032649e = head's own tree (main plus the head blobs).
- Identity: one commit, author and committer equal (a users.noreply address). Message plain ASCII, no B-number, name or seat id.

## (a) startingOwner against the spec: PASS
Source read: undefined -> ""; `trimmed.length <= OWNER_MAX` -> returns `owner` (the original, untrimmed); else for-of over code points stopping when cut.length + ch.length > OWNER_MAX, then trimEnd. Uses the store's own OWNER_MAX (100); checkEntry, parseRegister, stored shape and maxLength untouched.
My own probe (8 vitest rows plus a 30000-case seeded fuzz over a pool of a, spaces, tab, nbsp, astral, e+combining acute, ZWJ, high and low surrogate halves), all green at head: exactly 100 with two spaces each side returned byte for byte; 101 units as 50 astral + "a" -> 50 astral; 49 astral + "aaa" -> 49 astral + "aa"; combining marks (60 x e+U+0301 -> 50 pairs, 100 units; 99 a + e+U+0301 -> 99 a + e, the mark is dropped with the cut, no lone surrogate); ZWJ family emoji x20 -> <= 100 units, no lone surrogate, checkEntry ok; nbsp and ideographic space before the cut end-trimmed; tab/newline lead trimmed; "" and spaces-only returned unchanged; a trailing lone high surrogate on the input dropped. Fuzz invariants: fits -> byte-equal; else length <= 100, end-trimmed, a prefix of the trimmed input, checkEntry ok, no lone surrogate introduced, maximal. Probe control: with `ch.length` mutated to `1` the probe went red (2 rows failed: ZWJ, fuzz).

## (b) R1/R2/R3 red at main source, green at head: PASS
Both test files (head's) run against main's two source files in my clone: 9 failed, 138 passed (147): R3 x7 (`startingOwner` does not exist at main) and R1, R2 (render). At head: 147 passed, 0 failed. The existing "Network team" and empty owner row is among the 138 and stays green.

## (c) Deviation: PASS
RoadmapScreen.tsx changes exactly two lines: the import list (gains `startingOwner`) and line 99 (`startingOwner(action.owner ?? undefined)`). The import is the only extra changed line. `OWNER_MAX` at RoadmapScreen.tsx:72 and every maxLength stay.

## (d) No user-facing word added: PASS
Added string literals in the two product files: two empty strings (`return ""`, `let cut = ""`), one `""` removed. Added lines, JSX text: none. Name scan (underscore-aware, Kam Kamil Kreiser Steve Peter Paul Blanchard Inch Waite Friday Tuesday Wednesday Pete) over 82 added lines and the commit message: 0 hits, planted `_by_Kam_y` and `_by_Inch_` both fire. Cf characters: 0 (planted U+200B found); non-ASCII: 0. Secrets, hosts, tenant ids: 0 (the only match is the noreply attribution address). CodeQL pre-scan over all added lines including tests: `new RegExp(` 0, hand-escaped replace 0, innerHTML 0, child_process 0 (control: `new RegExp(x)` fires). The tests use regex literals only.

## (e) Closed lines: PASS
- HPSMPOC-228 N-5: at main `entra.ts:312` `const renewing = new Map<string, Promise<Renewal>>()`, `:380` `export const renewalsInFlight`; join at :359. `refresh-fanout.test.ts` has 5 `it(` rows (lines 78, 92, 104, 121, 139). 192c0a94 is an ancestor of main (rc 0). I ran the file myself at head: 1 file, 5 passed. Mutation control I ran: `let renewal = renewing.get(key);` -> `let renewal: Promise<Renewal> | undefined;` (waiting calls run their own renewal): same file RED, 4 failed, 1 passed (the one-after-another control). Reverted; clone clean. Matches the builder's numbers exactly.
- HPSMPOC-436: re-read at main, `ReportingEndpoints.cs:186-187` guard returns `narrative.no-findings`, the test class holds 2 `[Fact]`, `ContractTests.cs:183` names the code; 856d15d1 is an ancestor of main (rc 0). Taken as the builder's, NOT re-run by me: the SQLite and SQL Server dotnet runs and the mutation (no dotnet or docker started by me).
- Whole vitest (web/, `npm --prefix web test`): head 289 files, 4225 passed, 0 failed; main source with main tests 289 files, 4216 passed, 0 failed; delta +9 = the 9 new rows. These ran in the same invocation shape as CI (working directory web/).

## (f) test_hidden_characters.py not run by CI: CONFIRMED at source
`git grep -n -i -F hidden_characters` at head: hits only inside the test file itself (lines 101, 153). ci.yml has no `infra/tests`, `pytest`, `unittest discover` or `test_` step; the only `python3` steps are TRX summaries, `deploy-package.py` and the e2e plan. `infra/scripts/validate.sh:21` runs only `tests/test_security_baseline.py`. So the builder's finding is true. I ran the file directly at head: "Ran 14 tests ... OK". It walks tracked files, so it covers this diff. Pointer for the records seat, not for this PR.

## Other CI-shaped checks at head
- `npm run lint` rc 0 (eslint --max-warnings=0). `npm run typecheck` rc 0, 0 `error TS`. `npm run build` rc 0 (check-client-bundle: none of 39 markers). `node scripts/e2e.mjs --check-shards` OK ("every test in exactly one shard").
- e2e shard journey-and-prototype, ports 9671-9674 (all four variables), run twice. Run 2: timed journey 2 passed, desktop 1/2 182 passed, hosted 14 passed, 0 failed. Run 1 had two failures, see finding 1. Timed journey also alone twice: 2 passed each (roadmap span 282-790 ms, budget 1000).
- Hosted deploy: ci.yml has no deploy job (header lines 1-3: build and test only; packages kept from main, deployed by a runbook step). Merging triggers the ci.yml push run on main only; no `deploy-demo.yml` exists in this repo.
- Claims in the builder's STATUS graded true: refs, change list +82/-3, R rows and counts (9 red/138 green at main source, 147 green at head), vitest whole 4216 -> 4225, lint/typecheck/build/audit predicates as printed, hidden-characters 14 OK, new-words 0, names 0, 228 mutation 4 failed/1 passed. Not shown by me: npm audit results, audit-dev, 436 runs, tablet-1 shard (see NOT RUN).

## Findings
| # | Severity | Finding |
|---|---|---|
| 1 | Minor | First run of the e2e shard on a loaded machine (load 20-30) failed two specs, both timing: the timed journey tablet read "Remediation roadmap: 1140 ms >= 1000 ms" and desktop `a11y.spec.ts:39` hit its 30 s test timeout inside axe. Re-run: shard fully green; journey alone green twice; a11y passed at 29.4 s, close to its 30 s limit. Cause is machine load, not the diff (the roadmap change is one string helper per row; budget margin 3x at 282-412 ms normally). I did not run the same shard at main, so "not caused by this branch" is shown by green re-runs and source reading, not by a main comparison. Hosted CI is the proof. |
| 2 | Minor | `startingOwner` cuts at code points, as specified, not graphemes: a ZWJ sequence cut mid-way can leave a dangling U+200D (probe: three-person family emoji x20 -> 99 units ending with a ZWJ), and a combining mark is dropped from its base. The result is valid (no lone surrogate, passes checkEntry, Save accepted); cosmetic only and outside the kit's spec. No action needed. |
| 3 | Minor | Builder's STATUS disclosed it set the clone's user.name/email to the project repo's identity because a fresh clone had none; the commit's identity is the project's noreply address. Informational. |
| 4 | Minor | ci.yml never runs `infra/tests/test_hidden_characters.py` (confirmed, section f). Pre-existing at main; a pointer for the records seat and lane H-D, not this PR. |

## NOT RUN
- The 436 closure runs (dotnet on SQLite and on SQL Server, the guard-removal mutation): taken as the builder's; static re-read of the guard and test class only. No docker or dotnet started by me. The `api` and `api on SQL Server` CI jobs: hosted CI is the proof (the diff touches no api/ path).
- e2e shard prototype-tablet-1 (builder reports 181 passed, 1 skipped by design) and shards prototype-desktop-2, prototype-tablet-2, playbook-desktop-1/2, playbook-mobile-1/2. Not run at main either (no main e2e comparison).
- `npm audit --omit=dev` and `node scripts/audit-dev.mjs` (need the registry; no hosted HTTP): builder's numbers only.
- Hosted CodeQL and hosted CI: the proof at landing. No real-browser look at the screen (R1 and R2 are jsdom).
- Open-PR overlap was not re-read by me (no gh call); the builder's read is #309 and #310, neither touches these four files, and the kit's lane partition names them disjoint.
- Cleanup: 0 listeners in 9670-9679 at the end; every server was started by the e2e harness and stopped by it; my probe file moved to .../gate1496/_quarantine/ (no deletion).
