PR 2156: GO WITH NOTES

# Gate 304, tier 1 (Opus), compare round. PR 2156 (Refs KS-1785), delta af9e8967b351..5df9c6b42fa7

**Pins.** Read by ls-remote at the start (14:39 AEDT) and again at the end (14:49). Nothing moved between the two reads.

| Ref | Commit |
|---|---|
| develop | 0e6479d7b6c06b6f8a77aae1cbad167afbdaa089 |
| refs/pull/2156/head | 5df9c6b42fa71d84784fd08e550007f9ce1a05dd |

Both match the commission and the READY. This verdict covers only head 5df9c6b42fa7.

**Method.**
- I worked in my own scratch repo at `.../68f5fba5-.../scratchpad/gate304/repo`, borrowing objects from the shared checkout through alternates. The fetch used the checkout's sshCommand.
- Worktrees: `wpr` is the head, `wold` is af9e8967, and `wmerge` is a merge commit I built from `merge-tree`.
- In !CODING I used only ls-remote and config/read verbs. I never ran cd.
- GitHub (REST) and Linear (GraphQL query) were read only. Nothing was posted, pushed, commented or mailed.
- Fixtures are fake (`FAKE-NOT-A-SECRET`). No real secrets file was opened.
- load1 stayed between 4.2 and 6.0 throughout, under the limit of 8.

## FOUND / TESTED / HOW

**(1) The delta is exactly as stated.**
- It is ONE commit, 5df9c6b4 (parent af9e8967), touching 4 files, +14/-8 (`git diff --numstat`):

  | File | Change |
  |---|---|
  | show_env_masked.py | +7/-5 |
  | test_block_secret_reads.py | +4/-0 |
  | cheat fragment | +1/-1 |
  | flow fragment | +2/-2 |

- The code change is one new constant, `LINE_BREAK = re.compile(r"\r\n|\r|\n")`, and `view()` now splits on it in place of `split("\n")` plus stripping one trailing `\r`.
- The test change is two cells, `C2V_lone_cr_is_a_line_break` and `C2V_lone_cr_file`.
- Everything else is wording:
  - The docstring now says that only a value opening with `'` or `"` straight after the `=` is withheld as a multi-line block, and that an inline comment counts only after a space or tab (G303-2156-2 and -3, at the measured strength).
  - Both fragments now say "every comment line withheld".
  - The flow Proof row now reads 343 / 106 / 279 / 67 / 27 / 25.
- Nothing else changed. The commit message has no closing word.

**(2) G303-2156-1 is CLOSED.** I ran everything under both 3.14.9 (`/opt/homebrew/bin/python3`) and 3.9.6 (`/usr/bin/python3`).

*Red-first, re-run.* The head's test against the round-2 viewer from af9e8967 (`SECRET_GUARD_VIEWER`) gives exactly 2 red, `test_C2V_lone_cr_file` and `test_C2V_lone_cr_is_a_line_break`, under both Pythons.

*Head.* 343 of 343, OK, under both.

*My own mutants on the new code:*

| Mutant | Change | Result |
|---|---|---|
| G1 | the exact pre-fix split restored: `split("\n")` plus strip one trailing `\r` | exactly the 2 named cells red |
| G2 | `\r?\n` (the author's M27 form) | exactly the 2 named cells red |
| G3 | `\n` only (my replacement for gate 303's V2, whose anchor no longer exists) | 3 red: the 2 new cells plus `C2V_crlf` |
| G4 | alternation reordered to `\r\|\n\|\r\n` | 0 red. This is equivalent in output: a CRLF yields one extra empty line, and empty lines are withheld. It is not a gap. |

*Probe against the loader.* I compared the viewer's output with dotenv's parse for P1 and 10 new lone-CR shapes, under both dotenv versions the harnesses pin: akto 18.0.9 and playwright 18.0.8. Both versions apply `replace(/\r\n?/g, "\n")` in both of their parse paths (I read dist/index.cjs).
- At af9e8967:
  - P1 leaked.
  - Q3 (a lone `\r` inside a double-quoted multi-line value) also leaked: the whole line printed in clear.
- At the head, all 11 CR shapes print no fixture:

  | Shape | What it is |
  |---|---|
  | P1 | the gate 303 probe |
  | Q1 | `\r\r\n` |
  | Q2 | `\n\r` |
  | Q3 | `\r` inside a double-quoted block |
  | Q4 | `\r` closing a single-quoted value |
  | Q5 | `\r` after a comment |
  | Q6 | `\r` after a class name |
  | Q7 | `\r` after an inline comment |
  | Q8 | `\r` after an export line |
  | Q9 | `\r` before userinfo |
  | Q10 | a trailing `\r` at end of file |

- Each class-named value or userinfo value is masked, and the split agrees with dotenv's variable list in every case.
- Evidence: `scratchpad/gate304/probe/probe304.out`.

**(3) No other behaviour changed.**

*Gate 303 mutants re-run at the head* (`mut/run304.py`, the same anchors), identical under both Pythons:
- V1, V3, V4, V8, V10 and K1 to K5 redden exactly the cells they reddened at gate 303.
- V7 reddens 29 cells against 27 before. The +2 are exactly the two new lone-CR cells, because their password is masked. Against af9e8967's test file it reddens 27.
- The survivors are unchanged: V5, V6, V9 and V11 (G303-2156-8).
- V2 is not applicable at the head (its anchor was removed); G3 replaces it.
- The hook file `block_secret_reads.py` is not in the delta (`git diff` shows 0 lines). The K mutants confirm the exemption behaves as it did.

*Display change.* Three shapes that the round-2 viewer withheld whole now print a masked line, because the `\r` now starts a new line:
- `\n\r` followed by NAME=value (Q2)
- a `\r` after a comment (Q5)
- a `\r` after an export line (Q8)

Each now prints `DB_PASSWORD=<masked: N chars>`. This agrees with the loader, and no value prints in clear.

*Unchanged residual.* U+2028, VT and NUL inside a line (P12, P13, P14) still print raw. dotenv reads each of these as ONE value under a non-class name, so all three stay inside the stated residual, as at gate 303.

*Other legs at the head:*
- Leg 9 (`no-tracked-credentials.sh`, root derived from the script's own path, which is wpr): OK.
- docs-fragments check: OK, with the same two ADVISORY lines.

**(4) PR body corrections.** Body read live by GET at 14:4x; it was updated 03:36:57Z. The title is unchanged and has no closing word.
- **-4** is present and true. The body names SIX unignored names. I re-measured them with `git check-ignore --no-index` against the head's .gitignore:
  - `.env.e`, `.le`, `.ple`, `.mple`, `.ample` and `.xample` are all NOT ignored, under `core.ignorecase` false and true.
  - Positive controls: `.env.stripe`, `.env.mxample` and `.env.eample` are ignored. Under ignorecase=true, `.env.EXAMPLE` and `.env.Example` are not ignored, as the body states.
  - "The hook still refuses reads of all six" is carried from gate 303 (S2). I did not re-probe it, because the hook is not in the delta.
- **-5** is present and true. `sync-secrets.sh` at the head:
  - line 67 is `set_from_kv akto-admin-email AKTO_ADMIN_EMAIL`
  - line 70 is `set_from_kv akto-mongo-root-user MONGO_INITDB_ROOT_USERNAME`

  The body says both print in clear by the stated residual.
- **-6** is present and true at the probed strength. It names `;Password=`, `;AccountKey=`, `?password=` and a DSN with `?sentry_key=`. I re-probed P9, P9b and P10 at the head: still in clear, as the body says. Widening the class is stated as Wednesday's open decision (R-c).
- **Residue.** -2, -3, -7 ("the board seat tickets it after the merge"), -8 and -9 are each listed under "Gate 303 findings NOT fixed in this PR", at gate 303's strength. -2 and -3 also agree with the narrowed docstring.

**(5) No closing word in closing form.** I searched the title, body, all 4 commit messages (0d286210..head), the 1 PR comment (the Linear linkback) and Linear comment 9568f77a with `(close|fix|resolve)…(#|KS-|linear URL)`, case-insensitive: 0 hits. A planted control ("Fixes KS-1785", "resolves #12") gives 2 hits. "Refs KS-1785 (a reference only…)" is the only reference form. KS-1785 is In Progress and was not moved. Comment 9568f77a was edited 03:37:10Z for the fix head and the new counts.

**(6) Merge onto develop 0e6479d7b6c0, recomputed.**
- merge-base is 0d286210f98b.
- develop moved by 4 commits and 9 files since then: KS-2138, KS-2129, KS-2131 and KS-2127 (0e6479d7, new since gate 303).
- Shared paths with the PR's 14 files: **0** (`comm -12`; a self-intersection control gives 14).
- `git merge-tree --write-tree` is clean, giving tree 9b76bfcc.
- On the merged tree:
  - the contract test passes 343 of 343 under both Pythons
  - the wrapper `ks1785_secret_guard_contract.test.sh` returns rc 0
  - KS-2127's new suite `ks2127_pre_push_failing_diff.test.sh` passes 12 of 12
  - docs-fragments is OK
- Open-PR census (GET over 79 open PRs, every file page): the 14 paths hit PR 2156 only. The method's positive control is PR 2156 itself, listed with all 14 of its paths. A second control path, `.githooks/pre-push`, has no open PR now, which agrees with KS-2127 having merged.

## NOT TESTED
- Preflight leg 14 whole (124 suites, about 1,000 s). Load allowed it, but I skipped it as out of compare scope: the delta touches no shell suite, no .gitignore and no KS-915 file. The KS-915 suite was not re-run. Both rest on the author's 124 of 124 and 421 of 421 and on gate 303's 421 of 421.
- The author's own 27 mutants, R0 (67) and R0b (279) were not re-run. My own mutants G1 to G4, the red-first run, and gate 303's mutant set at the head stand in for them.
- compose-go's env_file parser. docker.env is also read by compose, and its line-break rules were not compared.
- A live Claude Code session, and Peter's and Stuart's machines.
- The hook's refusal of the six unignored names was not re-probed (the hook is not in the delta).

## Findings

**G304-2156-1 (Note). A body line is stale after the develop move.**
- "NOT covered" says wiring into `.githooks/pre-push` was not done "because another open PR holds that file".
- KS-2127 (0e6479d7) has since merged that file into develop, and no open PR touches it now (census).
- Also, "Touched in round 2 (this commit)" now sits above a fix commit.
- Wording only. Not blocking.

**G304-2156-2 (Note). The Linear comment was not narrowed with the body.**
- KS-1785 comment 9568f77a still says "Passwords, keys, tokens, secrets and URL credentials are masked; comments … are withheld".
- It does not carry the -6 caveat (a password in a connection string without userinfo prints in clear) or the -3 caveat (`x#text`).
- It defers to the PR body for follow-ups. The ruling required the body corrections only, which are done.

**G304-2156-3 (Note). A correction to gate 303's own record.**
- Gate 303 said dotenv 18.0.9 is "the version both runners load". In fact playwright's lockfile pins 18.0.8; akto pins 18.0.9.
- Both versions treat `\r\n?` the same way. I probed under both, so the G303-2156-1 closure holds for both harnesses.

**G304-2156-4 (Note). An equivalent mutant survives.**
- G4 (alternation order) survives because its output is identical: empty lines are withheld.
- No cell is needed. It is recorded so that it is not read as a gap.

No Minor or higher finding. G303-2156-1 is closed by the fix, red-first, under both Pythons and both dotenv versions. The residue -2, -3, -7, -8 and -9 and R-c stay open as the body states.

**Evidence** is in `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/68f5fba5-8c81-4b54-b6e9-607f5097de61/scratchpad/gate304/`:

| Path | Contents |
|---|---|
| `mut/results.txt` | the mutant runs |
| `redfirst_bin.out` | the red-first run |
| `head_bin.out` | the head run |
| `merge_*.out` | the merged-tree runs |
| `probe/probe304.out` | the lone-CR probes against dotenv |
| `pr2156.json`, `pr2156_body.md` | the PR and its live body |
| `lin_9568.md` | Linear comment 9568f77a |
| `ci/` | the check-ignore repo |

The scratchpad totals 1.0 GB. No rm was run outside the scratchpad.
