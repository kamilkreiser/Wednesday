# Analysis of the hosted no-golden test (Kam's Studio decision), 2026-11-12

Analyst: sub-agent for Wednesday, per `analysis_commission.md` in this folder. Read-only throughout; no network; the OpenRouter key was never read.
Run: `run_2026-11-11.log` (this folder). Run dirs: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/hosted/runs/noground/<model>/<ticket>_r1_<stamp>/`. Paths below are relative to that `runs/noground/` folder unless they start with `/`.

## BLUF (for Kam)

1. **No model reaches 30%.** Of 20 real tickets, the best results were 3 fixes I'd accept (15%), from DeepSeek V4.1-Flash and from GLM-5.3-Flash. DeepSeek is the model a 256 GB Studio would actually run. MiMo got 0. No model solved any of the 5 hardest (Opus-level) tickets.
2. **One check was too strict, but correcting it doesn't change the answer.** A check that demands exactly the right line number in each patch header refused 8 fixes that passed every real test. 3 of those were good, which lifts DeepSeek from 1 to 3 and GLM from 2 to 3. The best model is still at 15%.
3. **7 of the 20 tickets could not be fixed by anyone as posed.** They asked for a decision, a measurement or no code at all, or the input left out the code. On the 13 fixable tickets the best single model gets 23%. All three models pooled get 31%, but a Studio runs one model, not three.
4. **Cost was about 29 US cents for all 60 attempts.** Money isn't the limit; usefulness is. This was hosted, full-precision inference. A 256 GB box would run DeepSeek compressed (3.0 bits per weight), which can only do the same or worse.

## Per-model numbers

| | DeepSeek V4.1-Flash (v41) | MiMo-V2.6-Flash (mimo) | GLM-5.3-Flash (glm) |
|---|---|---|---|
| rows | 20 | 20 | 20 |
| PASS as the harness reported it | 1 (KS-2163) | 0 | 2 (KS-1982, KS-1934) |
| checker 7/7, refused only by A2a | 3 (KS-1982, KS-1934, KS-1945) | 1 (KS-1946) | 4 (KS-1908, KS-1880, KS-1826, KS-1191) |
| ACCEPT, harness as run | 1 | 0 | 2 |
| ACCEPT, A2a removed | **3** | **0** | **3** |
| share of 20, as run / A2a removed | 5% / 15% | 0% / 0% | 10% / 15% |
| share of the 13 answerable, A2a removed | 23% | 0% | 23% |
| Opus tier (5) accepted | 0 | 0 | 0 |
| spend US$ | 0.0413 | 0.0585 | 0.1927 |
| wall-clock (log start to rc) | 19 m 56 s | 28 m 17 s | 1 h 33 m 31 s |
| model seconds (`hosted/done_noground.md`) | 179 | 902 | 4,554 |
| cause: PASS / MODEL / HARNESS / INPUT | 1/9/3/7 | 0/12/1/7 | 2/7/4/7 |

- **Pooled (any model accepts):** 3/20 as run (KS-2163, KS-1982, KS-1934); 4/20 with A2a removed (adds KS-1880); 4/13 answerable = 31%.
- **Total spend:** US$0.2925, against a cap of US$18.

**Kam's 30%: not met by any single model, with or without the harness fix.** The only arrangement that touches 30% is all three models pooled and counted only against the 13 answerable tickets. That is not what one local box gives. It also isn't "30% off the plate", because the unanswerable tickets still cost Claude triage time.

**Claude-minutes.** My judging reads of the 11 checker-passing diffs (ticket, diff and the surrounding code at the tip) ran from 00:10:49 to 00:13:23. That is about 2.6 minutes, roughly 0.25 minutes a read. The whole forensic pass (all 60 rows) was a one-off of about 19 minutes wall-clock, much of it waiting for the run to finish.

Steady state, using report.md's 0.45 minutes per ticket for selection and prompting:
- **v41:** (9 + 4 × 0.25) / 3 ≈ **3.3 minutes per accepted item**.
- **glm:** (9 + 6 × 0.25) / 3 ≈ **3.5 minutes per accepted item**.

Both are under the 11.6-minute bar, but only because so few items are accepted. The 70% first-pass ACCEPT bar fails by a factor of about 5.

## A2a (the line-number check) and how much it understated the result

**What it checks.** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/code_patch/a2a_anchor.py` (docstring lines 4-21, comparison lines 72-90) requires each hunk header's old-start line to be exactly where the hunk's old lines sit at the tip. `hosted/check.sh` lines 46-59 combine it with the checker verdict, and both must pass. It was built for the Spark protocol, where the brief hands the model exact line numbers.

**Why it is the wrong check here:**
- The no-golden input gives each file as one JSON string with no line numbers, and `defect_line.line` is 0 (`hosted/noground.py` line 263). Counting to line 485 of a string is not the skill under test.
- The checker already has its own placement guard: the FUZZY OFFSET GUARD in `tasks/code_patch/checker.sh` lines 420-436 refuses a hunk placed more than 3 lines from its header. Tests A4-A7 then prove behaviour.
- Where `a2a_anchor.out` names exactly one actual location, git's placement is unambiguous and matches what the model meant.

**Every row refused only by A2a (8):**

| model | ticket | A2a (a2a_anchor.out) | unique location? | refusal right? | read |
|---|---|---|---|---|---|
| v41 | KS-1982 | logger.ts header -27, sits at [28] (a2a:2) | yes | no | ACCEPT |
| v41 | KS-1934 | webhooks.ts -480 at [485] (a2a:1) | yes | no | ACCEPT |
| v41 | KS-1945 | signatories -123 at [129], verifiers -100 at [106] (a2a:1-2) | yes | no | WRONG-FIX |
| mimo | KS-1946 | 3 hunks off +12/+13 (a2a:1-3) | yes | no | PARTIAL |
| glm | KS-1880 | reconciler -304 at [302] (a2a:1) | yes | no | ACCEPT |
| glm | KS-1908 | 2 hunks off +3 (a2a:1-2) | yes | no | PARTIAL |
| glm | KS-1826 | hunk 2 "not found anywhere" (a2a:2); the checker's fuzzy guard placed it (+3) | no, context was miscopied | defensible | PARTIAL |
| glm | KS-1191 | 6 hunks off ±1, one not found; checker reanchored (a2a:1-7) | mostly | defensible | PARTIAL |

**How much it understated:**
- Harness PASS: 3/60. Checker 7/7 ignoring A2a: 11/60.
- Accepted: 3 as run, 6 with A2a removed (v41 KS-1982, v41 KS-1934 and glm KS-1880 were refused by A2a alone).
- By ticket: v41 5% → 15%, glm 10% → 15%, pooled 15% → 20%.
- In the other 5 rows A2a refused a WRONG-FIX or PARTIAL, so it was right there by accident, not by design.

**Other harness defects** (they don't move the ACCEPT count, but matter for a re-run):

- **GLM ran out of reasoning budget.** glm KS-1806, KS-954 and KS-683 used all 32,768 tokens, 32,755-32,762 of them reasoning, and returned empty content (`out.md` is 1 byte; see `out.md.meta.json`). checker.out line 5 labels them "sampler loop / runaway (repetition)", which is wrong. The reasoning is not repetitive (KS-1806: 2,103 distinct lines out of 2,346 non-blank), and it ends mid-way through numbering file lines by hand to satisfy the header rule (KS-954 `out.md.raw.json`: "1207: … 1224: …"). Classed HARNESS: the run never reached the model's answer.
- **A3 forces a touch of every declared file.** v41 KS-1945 added a no-op comment to db.ts to satisfy it. mimo KS-1945 was refused at A3 (co:19) for leaving db.ts alone, and its fix is the same over-broad one anyway. The declared files came from ticket screening, not from the fix.
- **The declared set is too narrow for KS-2046.** v41 and glm wrote the same correct one-line fix: throw when the DB is unavailable, as the code's own comment at `index.ts` 1551-1553 asks. It turns 11 KS-1717 cells red, because that test deliberately runs with no database (`__tests__/ks1717-the-emitter-marker-is-honoured-only-when-signed.test.ts` lines 18-19). A mergeable fix also has to change that undeclared test. A6 is right that the suite got worse; the task was scoped too narrowly. Read: PARTIAL.
- **The excerpt dropped the site.** KS-1743's input carried `originate.openapi.ts` lines 1-60 and 3992-4072 only, but `DocumentCreateRequest.title` is at lines 265-269. The excerpt rule (`noground.py` lines 165-186) never cited it. v41 and glm correctly refused in one line.
- **A1 "prose outside the diff" is never counted.** Stage 1 prints the FAIL, but code_patch2's FAILS counter ignores it (mimo KS-1946 shows that FAIL alongside `RESULT: PASS (7/7)`). Lenient and harmless here; noted only.

## INPUT tickets (7): not answerable as posed

| ticket | why (the ticket's own words, `hosted/state/noground/inputs/<id>.json`) |
|---|---|
| KS-1870 (opus) | "R7 is not built, and the KS-1384 train will not build it"; the ruling is "run the read-only census". No code is asked for. |
| KS-683 | The fix is on Platform S ("terminal-state handling", Stuart's); Layer 2 is "ALREADY DONE … no work should be raised". |
| KS-1743 | The input omitted the schema it names; the cause is "Assumed, not verified". |
| KS-1222 | "The owners decide what the route should be … First measure". |
| KS-1112 | "One decision, then one small change: either 1 … or 2". Option 1 breaks the KS-1029 controls that pin the 200 (mimo and glm both did this, see `suite_delta.out`); option 2 needs the undeclared spec file. |
| KS-1191 | "a design decision for the audit trail's owner, not a one-line fix"; the comment adds "yours to decide". |
| KS-1908 | "The scan core (`walletLabelScan.ts`) does not change", yet the declared product file is `walletLabelScan.ts`. |

Rule: a row on an INPUT ticket is classed INPUT whatever the model did. A correct one-line refusal is still recorded as better behaviour than a broken diff.

## Per-row table

`co:N` = line N of the run dir's `checker.out`; `a2a:N` = line of `out.md.checker/a2a_anchor.out`. "Read" is given only where the checker ran green.

| ticket | model | harness | cause | read | evidence |
|---|---|---|---|---|---|
| KS-2163 | v41 | PASS | — | ACCEPT | v41/KS-2163_r1_20261111-220443 co:37,39 |
| KS-2046 | v41 | FAIL | HARNESS (declared set; A6 KS-1717 cells) | PARTIAL | v41/KS-2046_r1_20261111-220553 co:33 + suite_delta.out |
| KS-1982 | v41 | FAIL | HARNESS (A2a only, +1, unique) | ACCEPT | v41/KS-1982_r1_20261111-220723 co:37,39 a2a:2 |
| KS-1908 | v41 | FAIL | INPUT (also A5 red) | | v41/KS-1908_r1_20261111-220846 co:25 |
| KS-1896 | v41 | FAIL | MODEL (repetition loop, 16,384 tokens) | | v41/KS-1896_r1_20261111-221013 co:4 |
| KS-1880 | v41 | FAIL | MODEL (A4 test not red) | | v41/KS-1880_r1_20261111-221116 co:22 |
| KS-1826 | v41 | FAIL | MODEL (context not in file; fuzzy misplaced) | | v41/KS-1826_r1_20261111-221241 co:15 a2a:1 |
| KS-1806 | v41 | FAIL | MODEL (A4 control red) | | v41/KS-1806_r1_20261111-221328 co:23 |
| KS-1743 | v41 | FAIL | INPUT (correct refusal) | | v41/KS-1743_r1_20261111-221427 co:5 |
| KS-1222 | v41 | FAIL | INPUT (correct refusal) | | v41/KS-1222_r1_20261111-221438 co:5 |
| KS-1112 | v41 | FAIL | INPUT (also A2b stub test) | | v41/KS-1112_r1_20261111-221448 co:15 |
| KS-954 | v41 | FAIL | MODEL (A4 not red) | | v41/KS-954_r1_20261111-221529 co:25 |
| KS-1191 | v41 | FAIL | INPUT (also A6: test breaks KS-1090 type baseline) | | v41/KS-1191_r1_20261111-221701 co:36 |
| KS-1934 | v41 | FAIL | HARNESS (A2a only, +5, unique) | ACCEPT | v41/KS-1934_r1_20261111-221909 co:36,38 a2a:1 |
| KS-683 | v41 | FAIL | INPUT (correct refusal) | | v41/KS-683_r1_20261111-221941 co:5 |
| KS-1946 (opus) | v41 | FAIL | MODEL (tsc: `updated` out of scope) | | v41/KS-1946_r1_20261111-221952 co:25 |
| KS-1921 (opus) | v41 | FAIL | MODEL (A4 control red) | | v41/KS-1921_r1_20261111-222135 co:23 |
| KS-1870 (opus) | v41 | FAIL | INPUT (correct refusal) | | v41/KS-1870_r1_20261111-222208 co:5 |
| KS-1935 (opus) | v41 | FAIL | MODEL (A4 non-assertion red) | | v41/KS-1935_r1_20261111-222217 co:23 |
| KS-1945 (opus) | v41 | FAIL | MODEL (WRONG-FIX; A2a refusal incidental) | WRONG-FIX | v41/KS-1945_r1_20261111-222243 co:40,42 a2a:1-2 |
| KS-2163 | mimo | FAIL | MODEL (test TS6133 load error) | | mimo/KS-2163_r1_20261111-222439 co:23 + red_first.json |
| KS-2046 | mimo | FAIL | MODEL (A4 control red) | | mimo/KS-2046_r1_20261111-222601 co:23 |
| KS-1982 | mimo | FAIL | MODEL (A5 red) | | mimo/KS-1982_r1_20261111-222710 co:25 |
| KS-1908 | mimo | FAIL | INPUT ("need to inspect the repository", no diff) | | mimo/KS-1908_r1_20261111-222842 co:5 |
| KS-1896 | mimo | FAIL | MODEL (token cut, 61 KB of prose) | | mimo/KS-1896_r1_20261111-222852 co:6 |
| KS-1880 | mimo | FAIL | MODEL (A4 not red) | | mimo/KS-1880_r1_20261111-223323 co:23 |
| KS-1826 | mimo | FAIL | MODEL (fuzzy misplaced; context not in file) | | mimo/KS-1826_r1_20261111-223448 co:16 |
| KS-1806 | mimo | FAIL | MODEL (A4 control red) | | mimo/KS-1806_r1_20261111-223546 co:25 |
| KS-1743 | mimo | FAIL | INPUT (asked to inspect the file; no diff) | | mimo/KS-1743_r1_20261111-223644 co:14 |
| KS-1222 | mimo | FAIL | INPUT (also imports `supertest`, not available) | | mimo/KS-1222_r1_20261111-223726 co:26 |
| KS-1112 | mimo | FAIL | INPUT (A6: KS-1029 controls red, took option 1) | | mimo/KS-1112_r1_20261111-223912 co:32 |
| KS-954 | mimo | FAIL | MODEL (asked for repo access; corrupt patch) | | mimo/KS-954_r1_20261111-224028 co:14 |
| KS-1191 | mimo | FAIL | INPUT (also A4 control red) | | mimo/KS-1191_r1_20261111-224119 co:30 |
| KS-1934 | mimo | FAIL | MODEL (A4 STACK_TRACE_ERROR) | | mimo/KS-1934_r1_20261111-224250 co:24 |
| KS-683 | mimo | FAIL | INPUT (loop of grep commands) | | mimo/KS-683_r1_20261111-224337 co:4 |
| KS-1946 (opus) | mimo | FAIL | HARNESS (A2a only, unique) | PARTIAL | mimo/KS-1946_r1_20261111-224753 co:38,40 a2a:1-3 |
| KS-1921 (opus) | mimo | FAIL | MODEL (A4 control red) | | mimo/KS-1921_r1_20261111-224937 co:24 |
| KS-1870 (opus) | mimo | FAIL | INPUT (correct prose refusal) | | mimo/KS-1870_r1_20261111-225035 co:5 |
| KS-1935 (opus) | mimo | FAIL | MODEL (A5 red, tsc) | | mimo/KS-1935_r1_20261111-225058 co:27 |
| KS-1945 (opus) | mimo | FAIL | MODEL (same over-broad P2010 fix; A3 refusal is a harness quirk) | WRONG-FIX by diff read | mimo/KS-1945_r1_20261111-225138 co:19 |
| KS-2163 | glm | FAIL | MODEL (test TS2345 load error) | | glm/KS-2163_r1_20261111-225256 co:22 |
| KS-2046 | glm | FAIL | HARNESS (declared set, as v41) | PARTIAL | glm/KS-2046_r1_20261111-225530 co:31 |
| KS-1982 | glm | PASS | — | ACCEPT | glm/KS-1982_r1_20261111-225931 co:37,39 |
| KS-1908 | glm | FAIL | INPUT (checker 7/7, A2a only) | PARTIAL | glm/KS-1908_r1_20261111-230300 co:36,38 a2a:1-2 |
| KS-1896 | glm | FAIL | MODEL (A6: moved the search start, breaks pinned ks1384-fb-sweep r4/r4b) | | glm/KS-1896_r1_20261111-230858 co:32 |
| KS-1880 | glm | FAIL | HARNESS (A2a only, -2, unique) | ACCEPT | glm/KS-1880_r1_20261111-231453 co:36,38 a2a:1 |
| KS-1826 | glm | FAIL | MODEL (context miscopied; checker 7/7; A2a defensible) | PARTIAL | glm/KS-1826_r1_20261111-231819 co:37,39 a2a:2 |
| KS-1806 | glm | FAIL | HARNESS (reasoning budget exhausted, empty answer) | | glm/KS-1806_r1_20261111-232142 co:5 + meta |
| KS-1743 | glm | FAIL | INPUT (correct refusal) | | glm/KS-1743_r1_20261111-232938 co:5 |
| KS-1222 | glm | FAIL | INPUT (also A4 non-assertion) | | glm/KS-1222_r1_20261111-232953 co:25 |
| KS-1112 | glm | FAIL | INPUT (test TS18046) | | glm/KS-1112_r1_20261111-233438 co:21 |
| KS-954 | glm | FAIL | HARNESS (reasoning budget exhausted) | | glm/KS-954_r1_20261111-233756 co:5 + meta |
| KS-1191 | glm | FAIL | INPUT (checker 7/7, A2a only) | PARTIAL | glm/KS-1191_r1_20261111-234707 co:41,43 a2a:1-7 |
| KS-1934 | glm | PASS | — | ACCEPT | glm/KS-1934_r1_20261111-235341 co:36,38 |
| KS-683 | glm | FAIL | INPUT (budget cut too) | | glm/KS-683_r1_20261111-235630 co:5 |
| KS-1946 (opus) | glm | FAIL | MODEL (tsc TS18004; test TS7006) | | glm/KS-1946_r1_20261112-000444 co:21 |
| KS-1921 (opus) | glm | FAIL | MODEL (A4 control red) | | glm/KS-1921_r1_20261112-000827 co:23 |
| KS-1870 (opus) | glm | FAIL | INPUT (built R7 anyway; malformed /dev/null section at A2) | | glm/KS-1870_r1_20261112-001337 co:17 |
| KS-1935 (opus) | glm | FAIL | MODEL (A4 non-assertion red) | | glm/KS-1935_r1_20261112-001810 co:21 |
| KS-1945 (opus) | glm | FAIL | MODEL (A6: 10 new reds incl. ks1868 nominate catch) | | glm/KS-1945_r1_20261112-002122 co:38 + suite_delta.out |

## Read notes for the checker-passing rows

- **v41 KS-2163: ACCEPT.** On a failed probe it now walks every own key plus `cause`, each in its own `try`, through the same `visit` (depth bound and seen-set intact). This is the ticket's named fix shape, and the red cell is the ticket's own case.
- **v41 KS-1982: ACCEPT.** File transports are added only if `mkdirSync('logs')` succeeds; otherwise Console only. Two caveats: the block isn't re-indented, and the `chmod 0o555` red cell would not be red as root.
- **glm KS-1982: ACCEPT.** Same fix, plus a `LOG_DIR` override. Its red cell is robust (a regular file blocks the directory).
- **v41 KS-1934: ACCEPT.** Credits only when `paid`. That is stricter than glm's: a `no_payment_required` session would not be credited, but no promotion-code or discount option exists in billing's checkout creation, so that case isn't reachable today.
- **glm KS-1934: ACCEPT.** Credits on `paid` or `no_payment_required` and relies on KS-1933's once-only credit.
- **v41 KS-1945: WRONG-FIX.** It maps the generic `P2010` ("raw query failed") to 409, so a foreign-key or not-null failure would answer "already registered". The ticket says "the first step is a measurement", and the db.ts change is a no-op comment.
- **mimo KS-1946: PARTIAL.** A best-effort compensating UPDATE back to pending. It is not atomic: a crash or a failed compensation leaves the same bad state. The ticket was screened as needing a transaction design.
- **glm KS-1880: ACCEPT.** The SELECT now filters `~* '^[0-9a-f]{64}$'`, matching `REAL_TX_64HEX` (reconciler.ts line 127, case-insensitive). The test is weak: its red cell asserts the SQL text.
- **glm KS-1908: PARTIAL.** It adds hooks to the scan core, which the ticket says must not change, and wires nothing into own-create, so the lookup still truncates.
- **glm KS-1826: PARTIAL.** It declares the request field (the switch-on condition for Platform S) and the Anchor read field, but not the verify-by-hash `metadata.signatureHash`.
- **glm KS-1191: PARTIAL.** It folds case and sends every 404 to `unrouted.<verb>`, which also relabels routed 404s. It takes both decisions the ticket reserves for the owner.
- **KS-2046 (v41 and glm): PARTIAL.** The right line, but not mergeable alone (see harness defects).

## Method and controls

- **Waiting.** I waited for pid 79866 to exit and for `== glm rc=` in the log, using background polls and never touching the run. v41, mimo and glm's first 16 rows were analysed while the run continued; glm's last 4 were added after it ended.
- **Harness read before any judgement:**
  - `noground.py`
  - `check.sh` (A2a combined with the verdict, lines 46-59)
  - `tasks/code_patch2/checker.sh` (A3b, A3c and A3x skip themselves when there is no golden)
  - `tasks/code_patch/checker.sh` A1 (lines 70-121) and A2 (lines 420-500)
  - `a2a_anchor.py`
- **Per row I read:**
  - checker.out
  - a2a_anchor.out
  - extract.out
  - out.md.meta.json (done_reason, eval and reasoning tokens)
  - `suite_delta.out` for every A6 failure
  - `red_first.json` for every load error. All were the model's own TypeScript errors (TS6133, TS2345, TS18046, TS7006) or an import of `supertest`.
- **Reads against the ticket.** Each checker-passing row was read against the ticket text the model saw and the code at tip fcd178ff34fa, via `git show` on the read-only spark cache. The three harness PASSes were read exactly as strictly as the A2a refusals.
- **Absence controls.** Each absence claim was paired with a positive control in the same file, for example `signatureHash` (5 hits in anchorSchema.ts) and `checkout.sessions.create` (2 hits).
- **Verdict definitions:**
  - **ACCEPT:** fixes what the ticket asks, inside the declared files, with no behaviour change outside it.
  - **PARTIAL:** right direction, but a named part is missing or there's a side effect a reviewer would bounce.
  - **WRONG-FIX:** changes behaviour the ticket doesn't ask for, or gets it wrong.

## UNMEASURED

- How much quality the 3.0 bpw MLX pack loses versus the hosted fp8 version (KLD 0.096 per report.md). It can only lower these numbers.
- Local behaviour: tok/s, the wired-memory limit and context limits on the Mac. This test ran hosted.
- Round 2 (a retry fed the checker's failure lines) was not run. All rows are one sample at temperature 0.
- Whether glm KS-1806 and KS-954 would have passed with a larger reasoning budget.
- The tests were not re-run by me; the reads rely on the checker's A4-A7 records.
- The Claude time to take an accepted diff to a merged PR.
- Opus tier: 4 answerable tickets is a small sample, but no model came close (best result: one PARTIAL).
