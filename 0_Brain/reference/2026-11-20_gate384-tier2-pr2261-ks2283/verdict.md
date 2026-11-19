PR 2261: GO WITH NOTES (at head 6a71bf74c614686d268a186630a343b7649015f9; tier 2)

# Gate 384, tier 2 (Opus), PR 2261 (KS-2283), 2026-11-20 ~04:52 AEDT

## Pins
I pinned with gh api twice: at 04:4x before the first measurement, and at 04:52 just before writing this verdict.
- Head: 6a71bf74c614, open, not merged, not draft, updated_at 2026-11-19T17:38:22Z, 1 commit, 1 file, +6 -2.
- Develop: 2ad55ceceb7c both times.
- The head's only parent is 2ad55ceceb7c, and merge-base(develop, head) = develop. So the merged state is a fast-forward and equals the head tree.
- `git diff --stat`: one file, the test file, +6 -2.
- admin.ts blob c817ec2f9b39 at both commits; sha256 00814053d343eef8.
- package.json and package-lock.json are identical at both commits.

## How I measured
- My own `--shared --no-checkout` clone at `_work/g`, made from s-w43-base's .git. I only read that repo.
- Worktrees: `_work/h` at the head, `_work/d` at develop.
- node_modules were APFS-cloned from s-w43-ks2283, which I only read.
  - In both of my copies, the absolute self-link `node_modules/node_modules` pointed into s-w43-ks2283. I moved it aside to `_work/_quarantine/{h,d}`.
  - Foreign absolute links left afterwards: 0. Control: 112 relative links remain.
- I built packages/shared in each tree. TMPDIR was /private/tmp/g384t, Node v26.8.1, express 4.22.3, body-parser 1.20.9, finalhandler 1.3.2.
- After every mutant I restored admin.ts and checked it by sha256 (00814053d343eef8).

## Q1. Does the new cell fail under G12, L1 and G12R, and pass at head? YES, reproduced myself
Evidence: `_work/evidence/mutants_{head,headprod,dev}.out` and `.json`. Script: `_work/mutants_g384.py`. My mutant strings are my own; they match the builder's in meaning.

| mutant | old cell (develop d), NODE_ENV test | new cell (head h), NODE_ENV test | new cell (head h), NODE_ENV production |
|---|---|---|---|
| BASE | 14/14 | 14/14 | 14/14 |
| L1: lenient parser alone | 14/14, survives | 1 fail: `expected [Function] to throw an error` | 1 fail, same assertion |
| G12: lenient parser + gate after it | 14/14, survives | 1 fail, same assertion | 1 fail |
| G12R: G12 + the handler's code renamed INVALID_LEVEL | 14/14, survives | 1 fail, same assertion | 1 fail |

- Every new-cell failure is the malformed-body cell, at the new `JSON.parse ... toThrow()` line.
- The production arm really ran under production. A probe recorded NODE_ENV=production and the parser's reply as `<pre>Bad Request</pre>` HTML. Under test, the reply was the SyntaxError HTML. See `_work/evidence/probe_{test,production}.json`.

## Q2. M6 and M8 still die by their own cells, and the other cells keep their meaning. CONFIRMED
At head (test arm):

| mutant | result | failing cells |
|---|---|---|
| M0: pre-fix admin.ts, 70a0d984ac70^ | 7 fail | 5 tenant cells, plus malformed `expected 400 to be 403`, plus header `expected 200 to be 403` |
| M1 | 7 fail | same 7 |
| M2 | 7 fail | same 7 |
| M3 | 7 fail | 4 by `expected [..] to have a length of +0 but got 1`; 2 by `400 to be 403`; malformed `400 to be 403` |
| M6 | 1 fail | malformed-body cell, `expected 400 to be 403`, the stated reason, not the new line |
| M8 | 1 fail | header cell, `expected 200 to be 403` |

- M6 and M8 give the same result under production.
- The other 12 cells are byte-identical to develop. The diff touches lines 108-113 only.

## Q3. Can the new assertion go vacuous or fail falsely in ways the builder did not name? Mostly no, with F1 and one INFO
Mutants of my own, all at head:
- **Q1raw** (G12 shape, but the parse error leaves a string body): killed by the new line.
- **Q4jsonerr** (the parser's error answered with a JSON 400, gate still first): the malformed-body cell fails at the new line. This is a false fail on correct gating. It is the builder's named loud mode.
- **Q5jsonerrM6** (the same, plus the gate after the parser): fails at the new line.

### Empty body and missing content-type
A probe shows these turn the platform reply into the handler's JSON BAD_REQUEST, in both test and production:
- empty body `''`;
- `text/plain` with the broken body;
- `{}`.

So, if a future edit changed `broken` or the content-type, the new line catches it loudly. Before this PR it would have been silent.

### INFO: the handler's 400 turned non-JSON
- **Q2text** (G12 + the handler's 400 sent as text/plain) and **Q3empty** (G12 + the handler's 400 as an empty body) do make the malformed-body cell vacuous: it PASSES under both.
- Both are killed only incidentally, by the control cell "a platform role sending an unknown level gets 400". That cell's `res.json()` throws a SyntaxError. Q3empty was checked under production too.
- The file as a whole still kills them, but the cell itself rests on "the handler's 400 is JSON". The builder did not name that dependency.
- The scenario is contrived; it is not a merge blocker.

### F1 (LOW, wording and record; no code fault): the cell's HTML-versus-JSON split exists only in the test harness
- The real gateway already has a JSON error handler: `services/api-gateway/src/index.ts:1195 app.use(errorHandler)`.
- For any 4xx it answers `{success:false,error:{code: codeForStatus(400) = 'BAD_REQUEST', message: err.message}}`. See `middleware/errorHandler.ts:51-93`.
- The harness mounts the admin router on a bare express app, with no error handler, so Express's finalhandler HTML is what makes the parser's refusal non-JSON.
- I measured this: the same 14-cell file with only `app.use(errorHandler)` added to the harness gives 13/14. The malformed-body cell fails at `expected [Function] to throw an error`. Evidence: `_work/evidence/probe_errorhandler.out`; the probe file is in `_work/_quarantine/g384-eh.test.ts`.
- Consequences:
  1. The PR body and the comment both say "If someone later adds a JSON error handler for body-parse errors". One already exists in the product. The loud failure fires the day the harness is made more production-like by mounting it, not only if a new handler is written.
  2. The stated remedy, "assert that handler's error code instead", would NOT work with the existing handler. Its code for a 400 is BAD_REQUEST, the same as the route handler's own refusal, so G12 would go vacuous again. A working discriminator would be the message, or a parser-specific code.
  3. The test comment "The parser's refusal is an error page" is true of this harness, not of the deployed gateway.
- None of this makes the cell wrong today. It pins the router-level order: gate, then parser, then handler.

### UNMEASURED
- A body-parser or express upgrade (for example express 5 with finalhandler 2.x).
- Node 24.
- A booted gateway.

By reading only: finalhandler renders HTML in every version I know of, so the cell's JSON-ness test should hold. I did not measure that.

## Q4. Whole suite on the merged state, tsc, ratchet. CLEAN
Evidence: `_work/evidence/suite_{d,h}.json`, `failnames_{d,h}.txt`, `suites_g384.log`.
- The whole api-gateway vitest suite was run sequentially and load-gated; it waited through a load spike of up to 18.
  - develop: 2,071 of 2,071 passed in 181 files, rc 0, 34 s.
  - merged (= head): 2,071 of 2,071 in 181 files, rc 0, 31 s.
  - The failure-name sets are equal (both empty, compared with `cmp`).
  - The ks1936 file passes 14/14 in both arms.
- **Test-type ratchet**, api-gateway:
  - d and h: rc 0; 219 files, 181 under `__tests__`; 15 errors, 15 baselined, 0 new, 0 stale.
  - Planted control (a type error appended to the PR's test file): rc 1, "2 new". Restored by sha256.
- **tsc**, api-gateway on h: rc 0, 0 lines.
  - Planted control in admin.ts: rc 2, naming `admin.ts(1727,7)`. Restored by sha256.

## Q5. The PR body and the KS-2283 facts comment 5847a0bb. TRUE, apart from F1
Read-only checks: the PR body via gh api (6,684 bytes) and the comment via Linear GraphQL (3,264 chars, read back).

### Checked and true
- Title "Refs KS-2283 ..."; closing keywords: 0 (control "Closes KS-2283" fires).
- One file, +6 -2, lines 108-109 become 108-113, still 14 cells.
- admin.ts and both fragments untouched.
- Develop is 2ad55ceceb7c; the express and body-parser versions match.
- The matrix table and the production column match my own measurements, cell for cell.
- Under production, "contains SyntaxError" would false-fail: the production reply is `Bad Request` only (measured).
- The suite figure of 2,071/2,071 in 181 files matches.
- Ratchet: 15 baselined, 0 new.
- The acknowledgment boxes are unticked, and the body says why.
- Comment: "line 109" is the old precondition assertion line at develop (verified).
- Comment F2: proxy.ts line 1282 is `router.use('/originate/',` and line 911 is the "unauthenticated `/originate/` passthrough" comment, both at develop.
- Comment wording note: "No sentence here or in the fragments describes any other route" has 0 hits in develop. Control: "What it does not cover" hits 54 files.
- Branch `feature/ks-2283-ks-1936-follow-ups-malformed-body-cell`.
- KS-2283 is In Progress, with one comment (this one).

### Not verified
- "1,286 characters": the length of the HTML page depends on the stack paths, so it varies by tree. UNMEASURED as a fixed figure; immaterial.
- The four other shapes "measured on a scratch tree": the body names two. I took this as the builder's record and did not re-measure the not-chosen shapes, apart from the production SyntaxError text above.

### Does not hold
- The two sentences under F1: "later adds a JSON error handler" and "assert that handler's error code".

### NOTE only: the Linear attachment
- KS-1936 lists PR 2261 as a github attachment, created 2026-11-19T17:38:18.060Z, beside PR 2260's.
- KS-1936's state is In Progress, with 3 comments, all from before 17:00Z. None came from this PR, and the state is unchanged.
- The body mentions KS-1936 once. The branch name carries ks-1936.

## INFO for Wednesday (not the PR)
- The builder's tree `worktrees/s-w43-ks2283/Blockchain/Dev/node_modules/node_modules` is AGAIN an absolute self-link, mtime 04:30. That is the same recurrence gate 383 reported for s-w42.
- The READY says it was moved aside. Something re-creates it, the push's deps step being the likely suspect.

## Slips (mine)
- One command accidentally ran a recursive grep over `_work/../../../../2_Project_Files`. That resolves to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files`, not the reference folder, and the output was piped to `head -0`, so nothing was used.
- I stopped it by task id, after about 2 minutes. It was read-only, and no process was killed by name.

## Hard limits kept
- Nothing was written to GitHub or Linear: GET and GraphQL queries only.
- No mail, no launch, no database, no container.
- No `cd`, no `rm`: probes were moved to `_work/_quarantine`.
- No write in any !CODING path: write verbs ran only in my clone under `_work`.
- `git status` in h is clean after every run.
