# QA gate 6 (tier 2, batch, round 1 of 2): Secuura #1787 (KS-1779), #1789 (KS-1113)

- **Gate model:** Claude Sonnet 5.5 (claude-sonnet-5-5), G2 tier-2 batch gate, subagent of Wednesday. Spark review model: deepseek-v4-flash-0731 via the tunnel (UP at start, pid 52462). Routing receipt as commissioned: claude-sonnet-5-5, G2 tier-2 batch gate, gauge 81%.
- **Pushed / merged / commented / edited / mailed / Linear-written:** nothing. Linear was NOT read by me; the Spark review script read the ticket text (KS-1779, KS-1113) with the Secuura key (never printed). `gh` was not used, so the PR bodies were NOT read; each PR's own Flow-doc block stood in. Writes were confined to my scratch dir and this folder.
- **Clone:** `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fccaae68-37b3-43d1-9466-4e52087c3d4f/scratchpad/gate6/repo` (did not exist; created with `git init`; `git rev-parse --show-toplevel` asserted equal to that path before the first fetch and again at the end; origin = Secuura/Distributed_Secuura, deploy key via GIT_SSH_COMMAND with `IdentitiesOnly=yes`). It is outside WEDNESDAY, so spark_gate.sh accepted its work dirs (`gate6/w1787`, `gate6/w1789`). Scratch worktrees (`w1787/head`, `b1787` = merge-base, `w1789h`) were NOT removed (no-delete rule). Two scratch `node_modules` symlinks I had made were moved to `gate6/_quarantine/`. Evidence under `gate6/out/`.
- **node_modules:** read-only symlinks from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/` for every run. Because the shared tree's `packages/shared/dist` is stale (it lacks `isProvisioningCapable`, `signEmitterHop`; the same fact gate 3 recorded), in `w1787/head` and `w1789h` I made the root `node_modules` a real directory of per-entry symlinks into the shared tree, with `@secuura/shared` pointing at the worktree's own `packages/shared`, and built that package in the worktree (`tsc`). The shared tree was not written (the symlinked entries are read-only for my runs; no Prisma client was generated). Node v26.8.1 (not the repo's LTS 24) on every run.
- **Load:** one heavy run (the first `spark_gate.sh`, #1787, 76 s) started with load1 **13.23**; I did not wait the 15 minutes the brief asks for (miss, recorded). Every other heavy run started at load1 5.2 to 11.5. Spark queue lock clear.

## Pins (git ls-remote)

| ref | start (22:52) | end (23:09) |
|---|---|---|
| develop | b67a1c8d3a52038cb5f4e6135dfb59f0249eac6e | same |
| refs/pull/1787/head | 919a8008a6ca923298c9c9e4850ac6b330f487dc | same |
| refs/pull/1789/head | 8a42e55d357d9efbfadc37f50a57cd5fbd4ab9ba | same |

Both heads equal the prefixes in the READY mails; develop equals the 22:2x pin. Both PRs have merge-base bd6697e079fc with develop.

## BLUF

| PR | Ticket | Verdict | One line |
|---|---|---|---|
| #1787 | KS-1779 | **GO WITH NOTES** | The two eslint warnings are gone (adminConfig.ts: 2 to 0; originate `src`: 26 to 24), behaviour is unchanged (both edits are semantically inert; originate suite 143 files / 1702 cells, 0 failed, matching the doc; `tsc` rc 0), and the PR's added lines and test file are byte-identical to the canonical Spark patch (test sha256 99ea6fea... equal; product +/- lines `cmp` rc 0). Eight of nine own mutants killed; one survives (counter hoisted out of the loop) because the test reads source text. Notes: textual test, the recorded fuzz apply, merge-order dependency on KS-1780, docs section. |
| #1789 | KS-1113 | **GO WITH NOTES** | The two cells pass (2/2) against the REAL `routes/gdpr.ts` router on a real HTTP port; develop's spec goes red with the doc's own message (spec sha256s equal the doc's 571abb382f7b and 8d202a125a31); 5 of 5 service mutants and 7 of 7 route mutants are killed by the predicted assertion. Caveat: the stack is mine (real router, in-memory service, stub auth), not the author's three-process stack; the gateway and PUT 405 claims are unmeasured. Spark's NO GO is not borne out. |

**Merge order:** independent (no shared code file; see Merge-tree). Suggested **#1787 then #1789** (the doc for #1787 names KS-1780 part 2 as needing to land after it; #1789 has no such dependency). Either order merges clean in code; only the two docs files conflict.

**Docs sections now carried** (not assigned here; chain already holds 87 to 95, so these need 96+): develop's highest `<h2>` is **86** at b67a1c8d3a52. **#1787** carries `<h2>84.` with `<h3>84.1`, `84.2`, `84.3` in the Flow doc, and an unnumbered `<h2>` plus unnumbered `<h3>`s in the cheat sheet. **#1789** carries `<h2>84.` with `<h3>84.1` to `84.5` in the Flow doc, and an unnumbered `<h2>` in the cheat sheet. Both therefore collide with develop's own 84 (and with each other). At assignment the sub-headings `84.x` inside each block (and any in-text "84.x") need rewriting; the cheat-sheet headings are unnumbered. Each head's two html files are a pure insertion into base bd6697e079fc (checked: head == base[:i] + block + base[i:], 4 of 4, one `</body>` each).

---

## Spark shadow (run FIRST, per PR; `out/p1787/`, `out/p1789/`)

Method: `spark_gate.sh` per PR (clone and work dirs under the scratchpad because the script refuses WEDNESDAY), `--node-modules` = the Dev root `node_modules`. Then `spark_review.py` with `facts_spark.json` = facts with the two Projects Documents html files removed from `touched_files` (the first attempt sent them: touched-file text was 1.22 MB and the Spark answered HTTP 400; the html docs were dropped and the prompt fell to 42.7k tokens for #1787 and 18.8k for #1789; their diff hunks stay in the DIFF section), plus HARNESS LIMIT lines in `not_run`. No PR body was supplied. No ticket-provided comment draft.

| PR | spark_gate (head / base product code) | Spark review |
|---|---|---|
| #1787 | ks1779 test: **4 pass / 0 fail** ; **2 pass / 2 fail** on base product code (R1 and R2 red, as the PR says) | GO WITH NOTES, 10 Notes (0 Major, 0 Minor); 82.0 s, 42,661 prompt tokens, one attempt valid |
| #1789 | **VACUOUS**: a Playwright e2e spec run under the harness's vitest path gives a collection error, 0 passed / 0 failed on BOTH sides (log: "test.describe ... at gdpr-compliance.prelaunch.spec.ts:81"). Not a result; flagged in the facts the Spark saw. | NO GO, 3 Major 2 Minor 1 Note; 60.3 s, 18,830 prompt tokens, one attempt valid |

The #1787 product hunk: the READY file records that the strict check of the product section fails at `adminConfig.ts:2178` and that the section was applied with `git apply -p1 --recount --ignore-whitespace -C1`. I did not re-apply the patch; I compared outputs (below). The PR head was what the gate ran.

### Spark findings judged

**#1787 (all ten are Notes):** (1) test reads source text and cannot catch behavioural regressions: TRUE, disclosed (docs 84.2) and the reason for my M7 survivor. (2) R2 regex needs the exact comment `// Count even if conflict`: **CONFIRMED by plant** (M8, a reworded comment turns R2 red with no behaviour change; brittleness, Low). (3) C1's exact `copied.docTypes++` count is fragile to a refactor: TRUE, same brittleness, Low (M9 and M5 show it does what it is for). (4) "does not verify the catch still increments": WRONG (C1 does, M4 and M5 are killed by C1); its own evidence quote was not found in the input. (5) `...copied` only checked by presence: PARTLY TRUE (M6 is killed, a spread of a different object would not be). (6) "does not verify the const is in the right scope": **TRUE and CONFIRMED by plant** (M7 hoists `const copied` out of the loop, a real semantic change, and 4/4 stays green). (7) C0 could match another route: not a defect, the slice starts at the route's own `adminConfigRouter.post('/migrate-tenant-data'` anchor and ends at the next `adminConfigRouter.` (read). (8) test not in tsconfig: WRONG, tsconfig `exclude` was addressed in the PR doc and `tsc --noEmit` rc 0 here. (9) "PR doc claims the fuzz applied but facts show head": a misread (the doc says exactly that the head was tested and the Spark patch fuzzed); not a defect. (10) duplicate of (4), also unfound quote. Net: **no defect; two Notes confirmed by one mutant each.**

**#1789 (3 Major, 2 Minor, 1 Note):**
- Major 1 (15.2.5 mutates a real DB row that persists): TRUE as a description, NOT a defect: it is an e2e cell against a seeded test stack and the sibling cells in the file already create data (consent, other DSRs). The PR doc states the one row left (processed_by `e2e-prelaunch-...`). Low. Evidence quote not found in the input.
- Major 2 (5b not backed by a mutant): the doc says so itself (84.4); **my route mutant R1 (route accepts "processed") turns 15.2.5b red with "got 200"**. NOT REPRODUCED as a gap.
- Major 3 (the harness could not run the spec, so the claimed red/green is unreproducible): TRUE as a harness fact (vacuous row above), and the reason this gate ran the spec itself. I reproduced the doc's red and green (below); the spec sha256s match the doc's. Process finding, not a PR defect.
- Minor 1 (read-back shape not pinned to the route): **REFUTED**, R7 (GET answers the DSR at top level with no `request` key) turns 15.2.5 red.
- Minor 2 (5b depends on the validation order): **TRUE, CONFIRMED by plant** R5 (route looks the DSR up before validating the body: absent id answers 404): 5b red "got 404". The cell's own comment states the dependency ("the body is checked before the id") and the route does check the body first (`gdpr.ts:391-409`), so it is a coupling, not a false claim. Low.
- Note (one stack, Node 26): TRUE, disclosed in the doc (84.3, 84.4).
Net: **no defect confirmed; the NO GO is a false NO GO** (see calibration).

---

## #1787 (KS-1779, migrate-tenant-data loop lint warnings): GO WITH NOTES

Head 919a8008a6ca. Diff vs merge-base: `services/originate/src/routes/adminConfig.ts` (+2/-2), new test (37 lines, 4 cells), two docs.

### Lint, type and behaviour
| Check | Result |
|---|---|
| `eslint src/routes/adminConfig.ts` (own worktrees, eslint from the shared tree) | base (bd6697e): **2 warnings** (2181:13 `'copied' is never reassigned`, 2221:20 `'e' is defined but never used`); head: **0 output** |
| `eslint src` (whole originate service) | base 26 warnings, head **24**; the two removed are exactly the two above |
| The two edits | `let copied = {...}` to `const copied = {...}`: the object is never rebound (read the loop body, lines 2177 to 2262: only `copied.docTypes++`, `copied.orgs++`, `...copied`); `catch (e: any) {` to `catch {`: the block never read `e`. tsconfig target is ES2022 (optional catch binding is valid). Both are semantically inert. |
| `tsc --noEmit -p tsconfig.json` at head | rc **0** (with `packages/shared` built in the worktree; against the shared tree's stale dist it shows the two unrelated `@secuura/shared` export errors that also exist at base) |
| Whole originate jest suite at head (`out/suite1787.json`) | **143 files / 1702 cells, 0 failed** (the doc claims 143 / 1702 at head; base 142 / 1698 was not re-run by me). The two neighbouring route tests that exercise this loop, `ks730c-adminconfig-500-...` and `ks1772-originate-log-line-describers-...`, pass (65 cells with the new test). |

### Lenient-apply sections against the canonical Spark patch
Canonical: `local-model/runs/spark_secuura_2026-10-28_ks_1779_p1/out.md.checker/` (`section_1.diff`, `section_1.opts` = `--recount --ignore-whitespace -C1`; `section_2.diff`).
- **Product (lenient):** the `+`/`-` content lines of the PR's diff for `adminConfig.ts` (`git diff -U0`, headers excluded) and of `section_1.diff` are **`cmp` identical** (rc 0): `-let copied`, `+const copied`, `-} catch (e: any) {`, `+} catch {`. Hunk positions differ only in the context the fuzz tolerates (the canonical hunk header reads `-2178,4`, the PR's real change sits at lines 2181 and 2221). The PR's product blob at head is `26ae37f0b204` and the worktree at head hashes to the same.
- **Test (strict):** the PR's test file (`git show refs/pr/1787:...ks1779-...test.ts`) equals the `+` lines of `section_2.diff` **byte for byte** (`cmp` rc 0, sha256 99ea6fea15f5bb67004d8c72a1e4872d5e09e08293693717312505f34fd93d88 on both).
So both sections are byte-correct against the canonical patch; the product section's fuzz is the recorded one and changes nothing but hunk offsets.

### Mutants of my own on `adminConfig.ts` (own worktree, rewritten from the head blob and restored by sha256 compare; `out/mut1787.txt`; 4 cells: C0 R1 R2 C1)
| mutant | result | red |
|---|---|---|
| M0 head | 4 / 0 | none |
| M1 `let copied` (revert const) | 3 / 1 | R1 |
| M2 `catch (e: any)` (revert) | 3 / 1 | R2 |
| M3 `catch (e)` unused binding | 3 / 1 | R2 |
| M4 catch no longer counts | 2 / 2 | R2, C1 |
| M5 catch counts orgs instead | 2 / 2 | R2, C1 |
| M6 result row drops `...copied` | 3 / 1 | C1 |
| M7 `const copied` hoisted out of the loop (counter shared by every tenant) | **4 / 0, SURVIVES** | none |
| M8 catch comment reworded, behaviour identical | 3 / 1 | R2 (false red) |
| M9 catch counts twice | 2 / 2 | R2, C1 |

### Findings
| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1787-1 | Low | **M7 survives.** The test is a source-text check; a change that keeps the text `const copied = { docTypes: 0, orgs: 0 };` somewhere inside the route but changes its scope would not be seen. The PR says this (docs 84.2) and claims no more. The ks1772 and ks730c behavioural cells around the loop stay green too. | TESTED (M7). |
| 1787-2 | Low | R2 is pinned to the exact trailing comment text (M8 turns it red with no behaviour change), and C1 to the exact `copied.docTypes++` spelling. A harmless reword breaks the test. Spark Notes 2 and 3. | TESTED (M8, M9). |
| 1787-3 | Info (merge-time) | The PR doc says KS-1780 part 2 edits the catches of the same file and "must merge after this one"; that PR is outside this batch and not checked here. | FOUND in the docs; not tested. |
| 1787-4 | Low (merge-time) | Docs carry section 84; see BLUF. | |

---

## #1789 (KS-1113, e2e DSR process cell): GO WITH NOTES

Head 8a42e55d357d. Diff: `Blockchain/Dev/tests/e2e/tests/gdpr-compliance.prelaunch.spec.ts` (+99/-33, one file of code), two docs. Test-only.

### How I ran it (the stack is mine, not the author's)
The author measured on a throwaway three-process stack (api-gateway, auth, originate, Postgres, Redis, Chromium). I did not rebuild that. I built the nearest honest stand-in: a jest harness in my scratch worktree (`services/originate/src/__tests__/zz-gate6-dsr-harness.test.ts`, untracked, not part of the PR) that mounts the **real** `routes/gdpr.ts` router (its zod schemas, `DSR_STATUSES`, UUID guard, 400/404 shapes, `'DSR updated'` message) on a real HTTP port over an **in-memory** `gdprService` (create, get, update modelled from `gdprService.ts:336-407`: `completedAt` set only for `completed`, `processedBy` stored, FK failure on an unknown user), with stub `/api/auth/login` and `/api/auth/me` (`data.id`, matching `users.ts` `meHandler` which returns `data.id`), then runs the PR's own spec with Playwright 1.61.1 (`pw.gate6.config.ts`, no global setup, no browser) against it with `GATEWAY_URL`. **Harness assumption H1:** the spec's `findDsrEndpoint` accepts any non-404/403 from `GET /api/gdpr/dsr`; the router has no such route, so my server answers 405 there. The author's stack evidently did the same; I did not measure it.

### Does it run, and does it go red (out/e2e1789/)
| run | result |
|---|---|
| Head spec, cells `15.2.5` and `15.2.5b`, stack as above (M0) | **2 passed**, 0 failed |
| Develop's spec (blob read from develop, sha256 **8d202a125a31...**, equal to the doc's), same stack | cell 15.2.5 **FAILS**: "NOT-IMPLEMENTED: Could not create DSR to test processing", no PATCH sent: the doc's RED, reproduced |
| Head spec file sha256 | **571abb382f7b...**, equal to the doc's |
| `playwright test --list` on the head spec | **18 tests in 1 file** (doc: 17 to 18; develop has 17 `test(` lines, head 18; the header counts "(18 tests)" and "(8 tests)" match) |

### Planted defects (the PR's spec as the instrument; `out/e2e1789/S_*`, `R*`, `out/mut1789.txt`; files restored by sha256 compare)
In the in-memory service:
| plant | result | red cell and assertion |
|---|---|---|
| S1 update answers 200 but stores nothing | 15.2.5 red | "the DSR should read back as completed" |
| S2 `completedAt` never set | 15.2.5 red | "a completed DSR should carry a completedAt" |
| S3 `processedBy` never stored | 15.2.5 red | "read back with the processedBy the update sent" |
| S4 stores `processing` instead of the sent status | 15.2.5 red | "read back as completed" |
| S5 create returns the id as `requestId` inside `request` (no `request.id`) | 15.2.5 red | "DSR created but no ID returned" (the new fail-on-missing-id, which the old cell silently skipped) |

In the real route file `routes/gdpr.ts`:
| plant | result | red |
|---|---|---|
| R1 route accepts `processed` (status list widened) | **15.2.5b red** (got 200); 15.2.5 green | the PR's own named gap, now killed |
| R2 success message reworded | 15.2.5 red | "should say it updated the DSR" |
| R3 body-validation code `BAD_REQUEST` not `VALIDATION_ERROR` | 15.2.5b red | "the 400 should be the body-validation error" |
| R4 success flag inverted on PATCH | 15.2.5 red | "should report success" |
| R5 PATCH looks the DSR up before validating the body (absent id answers 404) | 15.2.5b red (got 404) | the spec depends on the route's body-before-id order (stated in its comment) |
| R6 PATCH answers 201 | 15.2.5 red | "should answer 200 (got 201 ...)" |
| R7 GET `/dsr/:id` answers the DSR at top level (no `request` key) | 15.2.5 red | read-back |
All twelve killed by the cell and assertion I predicted. No plant survived.

### Docs-section claims against the spec and the code
| Claim in the PR's doc block | Verdict | Line read |
|---|---|---|
| The create route takes `type, userId, email, notes` and answers `201 { success, request: { id } }` | **MATCHES** | `gdpr.ts:321-343` (`dsrBodySchema` at 70-75; `res.status(201).json({ success: true, request: dsr })`) |
| The old body (`subjectEmail`, `reason`) is refused with 400 "type, userId, and email are required" | **MATCHES** | `gdpr.ts:324-326` (`!userId` is true for the old body) |
| PATCH takes `status, processedBy, notes`; status is one of pending, processing, completed, denied, extended; `processed` answers 400 `VALIDATION_ERROR` | **MATCHES** | `gdpr.ts:82, 90-94, 116-121` |
| `processed` with no `processedBy` answers 400 `BAD_REQUEST` | **MATCHES** | `gdpr.ts:393-395` |
| `completed` answers 200 `{ success: true, message: 'DSR updated' }`; an unknown uuid answers 200 `{ success: false, 'DSR not found' }` | **MATCHES** | `gdpr.ts:412-413` |
| A later GET shows `completed`, `processedBy`, `completedAt` | **MATCHES** | `gdprService.ts:352-354` (writes) and `:406-407` (reads, `mapDsrRow`) |
| `processed_by` is text, so `e2e-prelaunch-...` is storable | **MATCHES** | migration `048_ks754_widen_processed_by_to_text.sql` (001 had `UUID REFERENCES users(id)`) |
| The body is checked before the id ("any well-formed uuid reaches the same 400") | **MATCHES** | `gdpr.ts:399-409` (parse first, UUID check after) |
| `userId` from `GET /api/auth/me`; "a real user's uuid (FK)" | **MATCHES** | `users.ts` `meHandler` returns `data.id`; `gdpr.ts:337-342` UUID guard, FK 23503 mapped to 404 at `:127-130` |
| The route allows GET and PATCH only; PUT answers 405 | **NOT MEASURED** | the router has no PUT and no 405 handler of its own; the 405 is the gateway's or a middleware's. The spec's removal of the PUT fallback is consistent with the route (no PUT route in `gdpr.ts`), the 405 answer was not driven. |
| Cells 15.2.2 and 15.2.3 send the same old create body and are "KS 1786" | **MATCHES** the body, not run by me | `git grep` at head: only the two cells (2 hits of `15.2.5` in the spec; no other file in `tests/e2e` names the cell) |
| Measured run: 2 passed in 2.1 s; 1 DSR row left behind | not reproducible on my stack (in-memory) | the `processed_by` column text type is the migration above |

### Findings
| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1789-1 | Low | **15.2.5b depends on the route validating the body before looking the DSR up** (R5). It is stated in the cell's comment and true today; a route that checked existence first would turn 5b red for a reason unrelated to the status vocabulary. Spark Minor 2. | TESTED (R5). |
| 1789-2 | Low | The cell leaves one `completed` DSR for the admin user in a real database (the PR says so); no cleanup. Spark Major 1 is this fact. | FOUND (reading; the doc 84.2 states it). |
| 1789-3 | Info | `findDsrEndpoint` is unchanged and its first candidates are routes that do not exist in this router (`GET /api/gdpr/dsr`); whether the live gateway makes the helper find a path is the author's measurement, not mine (H1). A gateway that answers 404 for all seven candidates turns both cells into the "NOT-IMPLEMENTED" fail. | FOUND by reading `gdpr.ts` route list; not tested against a gateway. |
| 1789-4 | Low (merge-time) | Docs carry section 84, colliding with develop's 84 and with #1787; see BLUF. | |

---

## Merge-tree (job 2; `git merge-tree --write-tree --name-only` in my clone, SHAs, develop = b67a1c8d3a52)

| merge | rc | result |
|---|---|---|
| develop + #1787 | 1 | conflicts in **exactly the two Projects Documents html files**, nothing else |
| develop + #1789 | 1 | same two files only |
| #1787 vs #1789, either order | 1 | same two files only; **no code conflict** |

Code files touched: #1787 = `adminConfig.ts` and its new test; #1789 = the e2e spec. **No shared code file.** The html conflicts are the usual "both appended before `</body>`" shape (pure insertions at base, checked above); I did not resolve or renumber.

---

## What I did NOT test

- Any other service's suite, the four platform suites (Schemathesis, Akto, Playwright, Performance/k6), a running real stack or gateway, any deploy, Node 24 (host has only v26.8.1), CI itself.
- #1787: the migration against a database (the product edit is inert by reading and the neighbouring behavioural suites pass; the route itself was not driven); originate's baseline suite count at base (142 / 1698 is the doc's figure, not mine); a re-application of the Spark patch in strict or lenient mode (I compared the resulting lines and files byte for byte instead); KS-1780 part 2.
- #1789: the author's real three-service stack and a real Postgres (my stack runs the real router over an in-memory service, so the SQL in `updateDSRStatus`/`getDSR` and the DB round trip were not exercised; the `processed_by` text type is read from the migration); the gateway or any proxy in front of originate; `PUT` 405; `findDsrEndpoint` against a real gateway (H1); the other 16 cells of the spec (the harness ran `--grep 15[.]2[.]5`, I only listed the rest); cells 15.2.2 and 15.2.3; Chromium (not needed by these cells).
- PR bodies (gh not used); doc accuracy beyond heading structure, insertion shape and the figures and claims re-measured above; the doc html checkers named in earlier gate verdicts.
- The Spark gate's result for #1789: by construction it has none (vacuous, see above).

## Spark calibration rows (one per PR)

| PR | Spark verdict | This check | Defects Spark found that stand | Real findings Spark missed | Verdict of the verdict |
|---|---|---|---|---|---|
| #1787 | GO WITH NOTES (10 Notes) | GO WITH NOTES | 0 Major (none raised). 2 of 10 Notes confirmed by a mutant (reword brittleness M8, no scope check M7); 3 Notes wrong or unfounded (catch counting, tsconfig, fuzz misread), 2 with evidence quotes not found in the input | none that I found beyond what it listed; it did not measure the lint count (2 to 0) nor the byte comparison with the canonical patch | **Right verdict, thin evidence**, same shape as gate 3's #1778: ten generic Notes, one useful (M7 scope). Cost to confirm each real Note was one mutant. |
| #1789 | NO GO (3 Major, 2 Minor, 1 Note) | GO WITH NOTES | 0. Major 1 is a disclosed side effect; Major 2 is refuted by one route mutant (R1); Major 3 is a true harness fact but it is the harness, not the PR. Minor 1 refuted (R7). Minor 2 TRUE as a coupling (R5), Low. | 1789-3 (`findDsrEndpoint` depends on the gateway); the whole set of killed plants | **False NO GO** on a PR the harness could not run (vacuous 0/0): the same pattern as gate 3's three NO GOs, "a Spark NO GO on a PR the harness cannot run is a prompt to run the mutant, not a defect signal". One of its six items (Minor 2) turned out to be real at Low. Note it had been told the harness result was vacuous and still raised "the claims are unreproducible" as a Major. |

Reading: two reviews, one GO WITH NOTES that agrees with this check and one NO GO with zero confirmed defects; the NO GO again lands on the PR whose real evidence is outside the harness (an e2e spec needing a stack). Pattern unchanged from gates 2 and 3. A harness improvement the facts point at: spark_gate has no Playwright path (it runs `*.spec.ts` under vitest and returns a collection error as 0/0); the 400 at first spark_review attempt was the 1.22 MB prompt from the html docs (gate 3 had the same instruction, it was not automated).

## Evidence locations
`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fccaae68-37b3-43d1-9466-4e52087c3d4f/scratchpad/gate6/`: `out/p1787`, `out/p1789` (facts, diff, `spark/review.json`, `prompt_user.txt`), `out/mut1787.txt`, `out/mut1789.txt`, `out/e2e1789/` (per-run Playwright json, jest logs, `.pw.log`), `out/suite1787.json`, `out/mergetree.txt`, `mut1787.py`, `mut1789.py`, `run1789.sh`, `mt.sh`, `pins_start.txt`; harness files in the scratch worktree `w1789h` (`zz-gate6-dsr-harness.test.ts`, `tests/e2e/pw.gate6.config.ts`). No container or background process was started by this gate (the Spark tunnel and the playwright child processes ended with their runs).
