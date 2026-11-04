GO WITH NOTES — MERGE (no HOLD-FOR-KAM)
# QA Gate 183 (Tier 2, round 1): PR 1998 / KS-1234 production-mode 307 regression test (Secuura/Distributed_Secuura)

Merge tree for the merge seat: `git merge-tree --write-tree 5c1ca287ed74 6bbe967acdda` = rc 0, tree `718951921dc6800b2f6d05c92f0375171dae4767` (clean, no conflicts), measured at start-of-gate and again at end.

## Subject block
| | start (16:46 AEDT) | end (16:55 AEDT) |
|---|---|---|
| PR 1998 head (refs/pull/1998/head) | 6bbe967acdda4273470abfe08af55b48fb678ff7 | 6bbe967acdda4273470abfe08af55b48fb678ff7 |
| develop | 5c1ca287ed74b6353423a8c09e253abf3129233a | 5c1ca287ed74b6353423a8c09e253abf3129233a |

Neither moved. Pins also saved as `pin_start.txt` / `pin_end.txt`.
Host: Apple Silicon Mac, Node v26.8.1 (NOT an LTS line, so nothing here is an LTS measurement), vitest and zod as installed from the head's lock (zod 4.6.7 confirmed in the clone's node_modules). Load average 5-6 during the runs.

Method: `git clone --shared` of the read-only checkout into `repo/`, the PR ref and develop fetched into that clone only (origin repointed to the GitHub URL, checkout's core.sshCommand copied). `npm ci --prefix` on the clone's Blockchain/Dev (rc 0, 1798 packages), `@secuura/shared` built (rc 0). Every runner anchored (`--root`, `--prefix`, `-C`), run under `env -i` with HOME and TMPDIR inside the workdir. Mutants by `mut.py` (this folder): anchor must occur exactly once, mutated file PARSED (TypeScript transpile diagnostics = 0) before each run, restored by `git checkout`, sha256 compared before/after.

## Findings

### G183-F1 — LOW: the "production check removed" mutant, taken literally, SURVIVES; the PR's "0 of 3" is for a different mutant than its name says
**FOUND:** Removing the `process.env.NODE_ENV === 'production' &&` term from versioning.ts (so the redirect fires in every mode) leaves the new file 3 of 3 green. That is expected and equivalent for a test that only boots in production: the term only changes non-production behaviour. The builder's "M3: 0/3" is reproduced only by forcing the check FALSE (the redirect never fires), which I ran as M3b (0/3, all three cells red). So the table's label "production check removed" (also in the fragment and commit text: "no production check") misdescribes the mutant that was run.
**TESTED:** both forms against the committed test bytes in my clone. Not tested: a cell proving that a NODE_ENV=test boot does NOT redirect (the file does not claim it; the sibling ks1234 file boots in test mode and T1 below shows this file's cells all fail there, which is the contrast the builder calls T1).
**HOW:** `mut.py`; raw outputs `scratch/mut_M3.out`, `scratch/mut_M3b.out`. Control: the same harness turned M3b red and M1/M2/M4/M5/M6 red in the same run, so the instrument fires.
**Effect on verdict:** wording only; the test does what the card asks. Not FIX-BEFORE-MERGE. Optional: say "production check forced false" in the fragment.

### G183-F2 — INFO: PR body not read by this gate
**FOUND:** question 6 asks for the body to quote the card id and contain no close-word. I could not read the PR body: the gate's gh config has no login for this repo (rc 4, "gh auth login"), and I did not go looking for another credential. What I did measure: the title (the head commit's subject, 89 characters, counted with `wc`, starts "Refs KS-1234: "), and the head COMMIT message: contains the card id `secuura-ks1234-production-307-1104` once, 0 close-words (regex close/fix/resolve), only KS-1234.
**TESTED:** commit message only. PR body: UNMEASURED by me. The builder reports its own body guard passed (check_body_ks_t10.py, 12,030 chars); I did not re-run it.
**HOW:** `git log -1 --format=%B`, saved as `scratch/commitmsg.txt`. Wednesday can read the body with the project's gh login if she wants it closed.

### G183-F3 — INFO (UNMEASURED cause): ks1054 did not fail
**FOUND:** ks1054-startup-migration-failure-on-health.test.ts passed in all three full-suite runs I made (see Q3). I could not reproduce the builder's earlier 2-of-2 failure, so I cannot say whether the new file plausibly causes it. Reading: the new file adds about 4.4 s of CPU in its own worker (production boot of the real app, three fetches) and ks1054's 5000/10000 ms limits are tight on a loaded host (builder candidate a), so a load-only cause is plausible, but nothing I ran separates the two. UNMEASURED; not a blocker.
**TESTED:** 3 runs at load average ~6. Not tested: a run at load 7-12, a run with the new file deleted.

### G183-F4 — INFO, PRE-EXISTING (base = head): the api-gateway suite writes a relative `logs/` into the runner's cwd
**FOUND:** my two text-reporter suite runs and the json run appended 201 lines to `/Volumes/DevMASTER/WEDNESDAY/logs/combined.log` (an existing, gitignored file in Wednesday's root; the shell cwd was Wednesday's tree even though `--root` was set). The writers are existing production-boot tests (the last line is the ks871 production-erasure test), not the new file: the new file chdirs into a temp dir, so it did not write there. I did not delete the lines (the file is not mine, and trimming it would be an edit outside my workdir). Reported to Wednesday as a stray-file effect.
**HOW:** `grep -c` on the 16:4x timestamps (201 lines, all api-gateway) and the tail of the file.

## What passed (measured)
- **Q1 Scope:** `git diff --name-status 5c1ca287ed74..6bbe967acdda` = 3 lines, all `A`: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1234-production-mode-307.test.ts` and `Projects Documents/fragments/{cheat,flow}/KS-1234-production-mode-307-then-the-v1-alias-reaches-originate.html`; +178/-0; 0 product files; neither shared page edited. Author/committer on the head commit: Kam Kreiser.
- **Q2 Red-proof, raw table (cells passing out of 3, committed bytes, my clone, each parsed first, each restored with sha256 equal: versioning.ts badf9acf9b8d7547, index.ts bd66c980e691626e both before and after):**

| mutant | passing | red cells |
|---|---|---|
| M1 307 -> 302 | 1/3 | hop 1, query |
| M2 query dropped | 2/3 | query only |
| M3 literal: production term removed | 3/3 (SURVIVOR, equivalent for a production-only test, see F1) | none |
| M3b production term forced false | 0/3 | hop 1, hop 2, query |
| M4 Location /api/v2/ | 0/3 | all three |
| M5 /api/v1 rewrite switched off | 2/3 | hop 2 ONLY |
| M6 original KS-1234 parser order restored | 2/3 | hop 2 ONLY |
| T1 copy booted with NODE_ENV=test | 0/3 | all three |

  My raw count: 7 mutants run (M1, M2, M3, M3b, M4, M5, M6), 6 killed, 1 survivor (M3 literal, equivalent); plus T1 contrast 0/3. The builder's six (with its "M3" read as my M3b) match my table cell for cell (1, 2, 0, 0, 2, 2 of 3). Headline = table. After the runs `git status --porcelain` in the clone was empty (all restores byte-equal).
- **Q3 Suite** (`vitest run --root .../services/api-gateway --maxWorkers=3`, clone, load 6.0-6.3): run 1 rc 0, 151 files / 1573 tests passed, 39.7 s; run 2 rc 0, 151 / 1573, 36.9 s; run 3 (json reporter) rc 0, 1573 passed / 0 failed / 1573, ks1054 file status passed (10 cells) and ks1234-production-mode-307 passed (3), ks1234-v1-documents-json-create passed (7). Runs 1 and 2 passed 151 of 151 files, so ks1054 passed both times (the text reporter does not list per-file lines; I confirmed the file by name in run 3). The new file alone: 3 of 3, rc 0. Matches the builder's 151 / 1573.
- **Q4 Overlap:** ks1461 lines 171-173 (the "RED KS-1461 production 307" cell, boots `NODE_ENV: 'production'`) assert only status 307 and `Location: /api/v1/documents` for the canonical path plus four case variants. Cell 1 of the new file duplicates status and Location, as the builder says, and adds: the connector-keyed body, `forwarded: []` (no upstream hit on hop 1). Cells 2 and 3 are fully new: hop 2 upstream count and body (the "hangs" half of KS-1234, which is what M5 and M6 are red on and ks1461 cannot see) and the query string (M2 red only here). Note, not a blocker: cell 1's marginal value is small but it costs one cell; it is also the only cell asserting `forwarded: []` on hop 1.
- **Q5 Fragments:** `node Blockchain/Dev/scripts/docs-fragments.mjs check --root <clone>` = rc 0, "OK" ("flow 117 legacy + 143 new, cheat 112 legacy + 143 new; lint clean, render passes html_docs_check"; two ADVISORY lines about committed-page lag, as the builder says; I did not diff them against untouched develop). Planted defect in a separate shared clone at the same head (`mut/fc`): an unclosed `<div>` and a `<script>` line appended to the flow fragment gave rc 1, "tags are not balanced: <div> opened 1, closed 0", "FAIL — 1 finding(s) in the fragments"; the same copy restored with `git checkout` gave rc 0 again (control).
- **Q6 Title:** head commit subject, which the builder says equals the PR title: 89 characters (`wc -c` of the subject without newline), starts "Refs KS-1234: ", at most 92. Close-word: none in the commit message. Card id in the commit message: yes, once. PR title and body themselves: title is by the builder's report equal to the subject (not read from GitHub); body UNMEASURED (F2).
- **Q7 Merge:** rc 0, tree 718951921dc6800b2f6d05c92f0375171dae4767, develop unchanged between start and end.
- No class-bar cells (not an error-path PR); no head outcome is more permissive than base because there are zero product bytes.

## NOT tested
- The PR body on GitHub (F2); the PR title as GitHub shows it; that the PR is open, not draft, and based on develop (builder's report only).
- The pre-push hook, legs 3, 4 and 8 (need a running stack) and the other 13 legs; the four platform suites (Schemathesis, Akto, Playwright, k6); any other service's suite; a running stack; Node 24 (everything ran on Node v26.8.1, non-LTS); any deploy.
- Lint and the test-file type-check ratchet (the builder reports 0 new errors; I did not re-run them).
- Behaviour outside the in-process fake upstream: an edge or ingress in front of the gateway, a real originate service, a human caller on this route.
- Interaction with Seat E 34th's KS-1244 request-path change (no PR exists yet; not my subject).
- Whether the ks1054 flake is caused by this file (F3).
- Whether the cells stay green at load above ~6.

## Plain answer for Kam
This pull request adds a test and two documentation notes. It changes no product code. The test starts the real gateway in production mode and checks that an unversioned document-create request is sent on to its /api/v1 address and that the address then reaches the document service exactly once, which is the behaviour behind KS-1234. I broke the product on purpose six different ways (wrong redirect type, lost query string, wrong address, redirect off, versioning rewrite off, the original KS-1234 bug put back) and the test went red every time; the one change that left it green is one that cannot matter to a production-only test. The whole gateway test suite passed three times out of three, and the merge onto develop is clean. The only loose ends are that I could not read the PR description itself, and that one older test was flaky for the builder under heavy load and did not fail for me.
