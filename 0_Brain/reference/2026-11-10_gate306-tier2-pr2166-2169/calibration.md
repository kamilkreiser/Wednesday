# Spark shadow of gate 306 (PRs 2166, 2168, 2167, 2169), 2026-11-10 ~18:1x
Method: blind (the Spark ran after verdict.md was written; I did not read its output first). Tunnel: DOWN at my first two checks (18:03 and 18:06, `spark_status.py` printed `tunnel DOWN (TimeoutError)`, queue 0, drainer not running; I did NOT run tunnel.sh and did not touch the box), UP at 18:08 and from then on. Tool: spark_gate.sh (deterministic half, exit 0 on all four) then spark_review.py, base ref `develop` = 0b55401ad5dc. The tool needs a clone whose `origin` serves `refs/pull/<n>/head`; I made a scratch bare repo (`fake.git`) holding develop and the four PR heads pushed from my scratch clone, and cloned it as `sparkrepo` (no network, nothing in !CODING touched). Inputs pre-fetched read-only: ticket text from Linear (description only, no seat comment), PR body from the GitHub API; no .env passed to the tool. `--node-modules` = my copied Dev/node_modules. Spark: deepseek-v4-flash-0731, one attempt each, valid JSON, no repetition, 31 to 49 s, 7.8k to 13.5k prompt tokens.

## Spark shadow PR 2166: verdict GO WITH NOTES (mine GO; one step more cautious, not a contradiction); recall 1/1 of G306-2166 findings; FP 2 of 11 (rest padding Notes)
Deterministic half: head 4/4, base 4/4 (test-only PR: base == head by design, mine: the hook suite 4/4 and mutants). Matches mine.
| id | Spark | note |
|---|---|---|
| G306-2166-1 (exit code value not pinned, refusal only) | FOUND (Spark 11: "does not assert that the hook's exit code is non-zero") | |
Spark findings at source: 11 Notes, all severity Note, most restate the design or the body ("test-only", "cleanup trap safe", "stub is a controlled double", "not the real preflight"). (2) "red proof not in facts.json": TRUE and fair (facts carry no mutant). (6) "relies on exact output string": TRUE, low value (the cell is the announce pin on purpose). (7) "does not cover preflight skipped": TRUE and outside the ticket. (10) PUSH-LANDED via ls-remote "may not reflect success": misreads (it is the right test of landing); FP. (1) and (8) are non-findings (FP, padding). The Spark found nothing that I did not, and nothing wrong that matters.

## Spark shadow PR 2168: verdict GO WITH NOTES (mine GO WITH NOTES, match); recall 0/5 of G306-2168 findings; FP 3 of 4
Deterministic half: head 6/0, BASE product code with the PR's test 2 passed 4 failed. Matches mine exactly (R1-R4 red).
| id | Spark | note |
|---|---|---|
| G306-2168-1 (new logger.warn failure path: failed row not saved, unhandled rejection) | MISSED | needs a run with a throwing logger; the Spark cannot run code |
| G306-2168-2 (issuer ExportDialog shows "Error: Export failed") | MISSED | context outside the diff |
| G306-2168-3 (real text only in the log; record cannot diagnose) | MISSED | |
| G306-2168-4 (throwing message getter unchanged) | MISSED | needs a run |
| G306-2168-5 (RED in permanent cell names) | MISSED | |
Spark findings at source: (1) "log line only asserted in a mock": TRUE, and my G306-2168-1 is the nearby real point, but the Spark's version is a restatement of not_run; low value. (2) "test mocks analyticsService so scope claim not proven": FP (the change is one catch; the mock is the harness). (3) "R4 does not assert the type name is absent from the log": FP (the real text, name included, SHOULD be in the log). (4) "description says product bytes change but test file not in scope line": FP, incoherent (the body names both files).

## Spark shadow PR 2167: verdict GO WITH NOTES (mine GO WITH NOTES, match); recall 1/3 of G306-2167 findings (-2 found, -1 and -3 missed); FP 2 of 6
Deterministic half: head 6/0, base product code with the PR's test 3 passed 3 failed. Matches mine exactly (R1-R3 red).
| id | Spark | note |
|---|---|---|
| G306-2167-1 (METERING-USAGE-API.md line 26 goes false after merge) | MISSED | outside the diff |
| G306-2167-2 (what later pieces owe; `[x]` residual) | FOUND (Spark 1 and 2) | restates the body, but correct |
| G306-2167-3 (single-element array and `from=&from=` also 400) | MISSED | needs a run |
Spark findings at source: (1) TRUE (body says so). (2) TRUE (body says so). (3) and (6) are the same non-finding twice ("read-only... so this is consistent"): padding FP x2. (4) "READY recorded 11 failed; cause unmeasured": TRUE, restates the body, low value. (5) "108 lines identical not verified by facts": TRUE, and I verified it (cmp.py), low value.

## Spark shadow PR 2169: verdict GO WITH NOTES (mine GO WITH NOTES, match); recall 0.5/4 of G306-2169 findings (-4 partly; -1, -2, -3 missed); FP 2 of 4
Deterministic half: head 11/0, base product code with the PR's test 3 passed 8 failed. Matches mine exactly (R1-R3 red).
| id | Spark | note |
|---|---|---|
| G306-2169-1 (OpenAPI already declares the regex and a 400; piece 2 undefined) | MISSED, and the Spark states the OPPOSITE | see FP (1) |
| G306-2169-2 (400 text says "format" for a well-shaped impossible day) | MISSED | |
| G306-2169-3 (regex clause redundant; mutant stays green) | MISSED | needs a run |
| G306-2169-4 (live contract change; callers outside repo unmeasured) | PARTLY (Spark 4: the caller search is not in facts.json) | |
Spark findings at source: (1) "the spec and route remain inconsistent... the ticket's acceptance (spec declares regex) is not fully met": FALSE. At the PR head `api-gateway.openapi.ts` lines 629-630 already carry `z.string().regex(/^\d{4}-\d{2}-\d{2}$/)` and the operation declares a 400; the route now MATCHES the spec. It repeated the body's framing without opening the file (the prompt did not include it). FP, and the only finding of the four that asserts a wrong fact. (2) states there is no discrepancy: padding FP. (3) restates the body's NOT run list: TRUE, low value. (4) TRUE, restates the body.

## What the tool or checklist should change
1. The 305 tool gap (a fresh worktree has no built `packages/shared/dist`) did NOT hit these four: with `--node-modules` pointing at a full Dev/node_modules the vitest, jest and bash legs all ran and agreed with mine to the digit (4/4; 6 and 2/4; 6 and 3/3; 11 and 3/8). So the earlier fix recommendation stands only for suites that import `packages/shared` (the ks949 bash suite); say in the checklist that the Dev/node_modules (with built shared) must be passed for services.
2. Product PRs that are LIVE API contract changes: the Spark cannot see callers, the OpenAPI declaration or the docs a changed line makes false. Context builder should add (a) the OpenAPI/spec stanza for the changed route (grep of the route path), (b) the `docs/*.md` lines that name the changed behaviour (the METERING-USAGE-API.md sentence), (c) grep hits for the route string across frontends. Without them the Spark restates the body (and in 2169 asserts a wrong fact about the spec).
3. spark_review.py: a "no discrepancy / consistent" Note is padding; drop findings whose own test_or_reason says there is no issue (2169 #2, 2167 #3 and #6, 2166 #1/#4/#8/#9).
4. The tool needs `origin` to serve `refs/pull/<n>/head`; a one-line `--origin-from-local` or a documented fake-bare recipe would let a gate run it with no network (this run used `fake.git`).
5. Throwing-logger / unhandled-rejection class (G306-2168-1) needs a run; no change possible for the LLM half, but a probe template ("stub the logger to throw") could be added to the deterministic half for catch-block changes.
Conduct: nothing written under !CODING; no push, post, comment, mail; the Secuura .env was read by in-process scripts only for the GitHub and Linear reads, no value printed. The tunnel was only observed, never started. Scratchpad: repo 2.0G (with copied node_modules), spark 2.1G, fake.git 275M, total 7.1G.
