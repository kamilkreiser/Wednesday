VERDICT: GO WITH NOTE at head 5c6daf6ae83e934d2e3655bf1abe452603fa9c59 (tier 1 delta, round 2 of 2; landing tree 48f08c661e686bd23adbbc5e3da5f4d73fa33e92 on develop 115797747cb60009e781d80e9059dbbed69e1ac3; 0 blockers, 5 notes)

Gate AN1, PR #1622 (KS-1641 finding 2) delta, Opus, round 2 of 2. Clone: /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/08573273-0b69-4d9e-abf5-9b213ac8c2f2/scratchpad/an1/repo (cloned from the AM1 clone, then heads fetched from origin). Heads re-read by ls-remote at the start and again before this verdict: develop 115797747cb6, refs/pull/1622/head 5c6daf6ae83e. Both unchanged. Node v24.7.0, express 4.22.3, qs 6.16.0. packages/shared built first (rc 0).

AM1 B1 is CLOSED on the real process. Nothing in this delta blocks. N1 is a separate unauthenticated crash on this same route. It is NOT introduced by this PR: develop dies on the same inputs. It needs its own ticket now.

## Questions

Q1. B1 closed on the real process (tsx src/index.ts, NODE_ENV=development, FRONTEND_URL http://frontend.test). Driver: /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/08573273-0b69-4d9e-abf5-9b213ac8c2f2/scratchpad/an1/live.js, which sends raw-socket requests so the wire bytes are exact.
- Landing tree 48f08c66, AM1's kill input ('A'*199 + U+1F600 + 'zz'):
  - Result: 302, Location 270. The message is 'A'*199 + U+1F600, which is 200 code points with the emoji whole.
  - Afterwards /health gives 200 and the child is alive.
  - Aligned control ('A'*198 + emoji + 'zz'): 302, Location 270.
  - Measured four separate times (each live run starts with it).
- Fuzz: 1000 strings (seed 11) plus 300 (seed 5) on the landing tree.
  - Alphabet: ASCII including % & # = + ? / space CRLF; BMP (U+00E9, U+0800, U+4E2D, U+FEFF, U+FFFD); astral pairs (U+1F600, U+1D11E, U+10FFFF); lone highs and lone lows.
  - Lengths: 198 to 202 code points, plus 400 and 1000. Sent as error_description, or as error (15%).
  - Lone surrogates were put on the wire three ways: CESU/WTF-8 percent bytes, %uXXXX, and raw bytes.
- Fuzz results, seed 11:
  - cesu 200/200, pctu 200/200, raw-special 200/200 and well-formed 200/200 all OK. OK means 302, host frontend.test, path /admin/integrations, keys exactly [m365,message], m365=error, empty hash, message of 200 code points or fewer.
  - Of the well-formed error_description cases, 174/174 decoded exactly to the first 200 code points of the input.
  - Raw-byte mode: 200/200 got a 400 from Node's parser before the handler (non-ASCII bytes in the request-target), so these are not handler answers.
  - Zero process deaths, /health 200 after every 50 requests and at the end, 0 URIError lines in server output.
- Long cases (Location length):
  - astral x1000: 2459
  - U+0800 x1000: 1859
  - '%' x3000: 659
  - ASCII x10000: 259
- MAXIMUM Location measured: 2459 (astral). This equals the author's figure.
- Positive control for the zero: mutant M0 (both defences off). The kill input dropped the socket, /health was refused, the child exited with code 1, the server output had 1 URIError, and the fuzz died at request 1.

Q2. Defence 1 (`capCodePoints`, index.ts:473-475) is correct as a cap for every shape I tried. I pulled its body out of the source text and called it directly, because importing index.ts starts the server.
- It yields exactly 200 code points for: astral x300, the split input, lone highs x300, lone lows x300 and 'A'*199 + lone high. Empty, number and array inputs also work.
- It does NOT remove a lone surrogate that is already in the INPUT. It passes it through: capped lone-high input is not well-formed, and plain encodeURIComponent throws on it.
- On this route that string goes only to the guarded `encodeReflectedText` at :514 (guardedOK in every case) and to the JSON.stringify log, which does not throw (measured: it escapes the surrogate as \ud83d).
- Over HTTP a lone surrogate cannot reach the handler at all:
  - qs decodes through decodeURIComponent and falls back to the literal text. For example `error=%ED%A0%BD` reflects as `%25ED%25A0%25BD`.
  - %uXXXX is not decoded in utf-8 mode.
  - Raw bytes get a 400 from Node.
- The other encodeURIComponent calls on this route are pre-existing and outside this diff: :557 (Graph tenantName, inside try, so caught) and :564 (MSAL err.message, inside the catch, NOT guarded). Both need a server-issued `state`. See N5.

Q3. Defence 2 (`encodeReflectedText`, :485-495), checked by mutation in the clone. index.ts was restored by checkout after every mutant (sha256 a504a66bfd53f763 before and after, git status 0 lines). Every run counted 10 tests, so none was a load failure.
- Defence 1 removed (cap back to code units), guard kept (M1):
  - Kill input on the live process: 302, message 'A'*199 + U+FFFD, alive; fuzz 300 with zero deaths.
  - In-suite: E5 and E8 red, E6 GREEN. So E6 is the request-level cell that exercises defence 2 when defence 1 is wrong.
- Defence 2 removed at the call site (:514 back to bare encodeURIComponent), cap kept (M2):
  - Live kill input 302 and alive; fuzz 300 with zero deaths and max Location 2459.
  - So defence 1 alone is enough over HTTP. This matches the author's "unreachable over HTTP" claim.
- Regex, called directly on 10 shapes: the output equals String.prototype.toWellFormed in 10/10. The shapes:
  - a valid pair kept;
  - lone high at the end;
  - lone low at the start;
  - low then high;
  - high-high-low (the first high is replaced, the pair kept);
  - high-low-low;
  - a pair followed by a lone high;
  - lows only;
  - U+10FFFF;
  - a mixed string.
- On well-formed text the guard is byte-identical to encodeURIComponent in 5000/5000 cases.

Q4. N2/N3 logs:
- Both are now capped by code point: :511-512 (error and description) and :525 (connectionId). They are pinned by E9 and E10 (mutants M4 and M5 each red exactly one of them).
- Neither can throw on a lone surrogate. Array.from does not throw, and JSON.stringify escapes the surrogate (measured), so no encoding is needed.
- Both CAN throw on an object whose own `toString` is a string. See N1: on the landing tree the death moves from the redirect to this log line, at :474 via :511.

Q5. Cells can fail. Results on the landing tree, ks1641 file, verbose reporter:

| mutant | red |
|---|---|
| head | none (10/10) |
| M0 both off | E5, E6, E8 |
| M1 code-unit cap, guard kept | E5, E8 |
| M2 guard bypassed at :514 | none |
| M3 naive `/[\uD800-\uDFFF]/g` | E7 |
| M4 :511-512 log uncapped | E9 |
| M5 :525 log uncapped | E10 |
| M6 helper no cap | E1, E2, E5, E8, E9, E10 |
| gate M7 cap 201 | E1, E2, E5, E8, E9, E10 |
| gate M8 fallback returns '' | E7 |
| gate M10 regex replaces highs only | none (10/10 green, see N2) |

E5 through E10 each red on a mutant named for it. E1 through E4 are unchanged from round 1 (the diff e065dc9..5c6daf6 removes exactly one test-file line, the `import('../index')` in beforeAll, and adds only E5-E10 and helpers), and they red under M6 and M7. E3 and E4 stayed green under every mutant, as no-change controls should.

Q6. The exports add no side effects at import. The diff to index.ts adds only a const, two function declarations and the three call-site edits. A grep of the +/- lines for listen, require, connect, init and setInterval hits only comments and the existing `process.env` redirect lines. Importing index.ts already did these things on develop (ks934 uses the same pattern):
- calls `app.listen` at :1636 (mocked in the test);
- runs `startUserErasedSubscriber`, a no-op without REDIS_URL;
- runs the PII keyring block, which calls process.exit(1) only when NODE_ENV is production, staging or demo; the test sets 'test'.

Q7. Landing:
- merge-tree --write-tree of origin/develop and origin/pr1622: 48f08c661e686bd23adbbc5e3da5f4d73fa33e92, rc 0. A real `merge --no-ff` in the clone gave the same tree. Both equal the author's prediction.
- Merge-base is 6ec1b7ba. The three-dot diff lists exactly the PR's 2 files (+223/-3).
- m365 vitest on the landing tree: 74/74 in 10 files, rc 0. At develop: 64/64 in 9 files, rc 0.
- Type-check including the test file: scratch /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/08573273-0b69-4d9e-abf5-9b213ac8c2f2/scratchpad/an1/tsconfig.an1.json with exclude [].
  - listFilesOnly: ks1641 = 1 under that config, 0 under the service's own tsconfig.
  - Result: rc 0, no output.
  - Positive control: a planted TS2322 in the test file gives rc 2. The file was restored and git status is 0 lines.

## Notes

N1. PRE-EXISTING, unauthenticated, not introduced or worsened by this PR, needs its own ticket now. One GET kills m365 on develop AND on the landing tree.
- Express 4.22.3's query parser calls qs with `allowPrototypes: true` (node_modules/express/lib/utils.js:290). So `?error[toString]=x`, `?error=a&error_description[toString]=x` and `?code=x&state[toString]=y` make objects whose `toString` is a string.
- `String()` on such an object throws `TypeError: Cannot convert object to primitive value` inside the async handler. That is the same unhandled-rejection path as B1.
- Measured on fresh processes, each case: socket dropped, /health refused, exit code 1.
  - develop: thrown at index.ts:465:140 and :472:24;
  - landing: thrown at index.ts:474:21 (String(value) in capCodePoints, called from the :511 log) and :521.
- Controls: `error_description[valueOf]=x`, `[a][b]=c`, `[]=p&[]=q`, `error=a&error=b` and `state[]=a&state[]=b` all get a 302 and the process stays alive.
- Not measured through api-gateway or the deployed image.

N2. E7 pins only the lone-HIGH arm of the regex. Gate mutant M10 (regex replaces highs only, so a lone low would throw a second time inside the catch) is 10/10 green. The regex itself is correct (Q3), so this is a cell gap, not a defect.

N3. The author's mutant table is inexact in places:
- M1 reds E5 AND E8, not "E5 only". E8's first assertion is the code-point unit, so a code-unit cap fails it.
- Bypassing the guard at the call site (gate M2) is 10/10 green. E7 pins the helper, not its use at :514. That follows from the guard being unreachable, which the author disclosed, but the table's "M2 -> E7" reads as if E7 guards the route.

N4. The bound is now 2459, up from 1859 (measured, matches the author). Code points vs code units is the author's open question and a Kam/Wednesday call. Both options are bounded and E8 pins either; I would not hold the merge on it.

N5. :564 sits inside the catch and calls encodeURIComponent on MSAL `err.message` with no guard. A lone surrogate in provider error text would be an unhandled throw there. It needs a valid server-issued state and is pre-existing. It belongs with the N4/N5 follow-up ticket the author plans. :557 is inside the try, so it is caught.

## NOT run

- No Docker, DB, Redis or stack; no deployed environment; not tested through api-gateway; not tested with the built dist under the production Dockerfile.
- Preflight legs not run; other services' suites not run; the four platform suites not run.
- Linear, the KS-1641 ticket and the GitHub PR body not read.
- Lone-surrogate fuzz over HTTP cannot deliver a real lone surrogate to the handler (Q2), so defence 2's lone-surrogate behaviour was proven by direct call and by mutant M1 only.
- All server processes I started were stopped. pgrep for the clone's index.ts gives 0 matches; positive control: a decoy process with that name was matched, rc 0.
sha256 6a61aba9711c9b9f28ebbe7b8b2ec536692f6e80dbe59de1316cef2d1bd0846d
