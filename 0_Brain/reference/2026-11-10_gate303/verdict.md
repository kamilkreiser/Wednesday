PR 2156: GO WITH NOTES
PR 2154: GO WITH NOTES
PR 2155: GO WITH NOTES
PR 2160: GO WITH NOTES

# Gate 303, tier 1 (Opus). Verdicts for 4 PRs.

## Common to all four PRs

**Pins.** Read by ls-remote at the start (13:37 AEDT) and again at the end (13:59). Nothing moved between the two reads.

| Ref | Commit |
|---|---|
| develop | d3e663692a8f414f16610236259cab14b27ff0f7 |
| PR 2154 | 75e8295d8508fd49fba7672472b61f0124797c6d |
| PR 2155 | ad404a5a87bb87743e76bd5473ca2539820e013a |
| PR 2156 | af9e8967b3519dab03babe067e3a0bd3c48aa83f |
| PR 2160 | b02bd2716cc2176cd6d2acd6b75885781f6c58d4 |

Each head equals the head its READY mail names. A verdict here covers only these heads.

**Merges.**
- All four PRs are built on 0d286210f98b.
- develop moved by 3 commits since then (KS-2131, KS-2129, KS-2138) and 5 files. None of the 5 is a file of any PR here.
- `git merge-tree` onto develop is clean for each PR alone. The three R 93rd PRs are also clean together (one tree).
- No path is shared between any two of the four PRs.

**Method.**
- Everything ran in a scratch repo inside this session's scratchpad, with worktrees at `w56` (PR 2156 head) and `wdev` (develop). Objects were borrowed from the shared checkout through alternates, and the fetch used that checkout's sshCommand.
- In !CODING I used only ls-remote and reads. I never ran cd.
- GitHub and Linear were read with GET requests only. Nothing was posted, pushed or mailed.
- No real secrets file was opened. Fixtures are fake (`FAKE-NOT-A-SECRET`) or the tracked templates.

**Load.**
- load1 went above 8 during the R 93rd originate whole-suite run on develop: it started at 7.91 and peaked at 11.03.
- My KS-915 suite runs started at 5.1 and ended at 10.9, which was shared with other seats.
- Breach noted.

---

PR 2156: GO WITH NOTES

## FOUND / TESTED / HOW

**(1) Touched set.**
- 3 commits and 14 files. Round 1 is 3d9f64d4 and 81091a34; round 2 is af9e8967.
- Round 2 is exactly the 10 files stated, +516/-8. It does not touch settings.json, .gitignore, restore_local_secrets.test.sh or the wrapper (`git diff --stat 81091a34 af9e8967`).
- The three `.env.example` edits are comments only.

**(2) Cells and red-first, re-run.**
- **Head:** 341 of 341 under Python 3.14.9 and under /usr/bin/python3 3.9.6.
- **R0** (round 1's hook from 81091a34, with no viewer): 65 red, matching the seat's 65.
- **R0b** (an allow-all stub of my own, run in a develop worktree with the head's test): 277 red (270 failures and 7 errors), matching the seat's 277.

**My own mutants on round 2** (`scratchpad/mut/run.py`). 16 mutants, 12 of them killed:

| Mutant | Change | Named cells red |
|---|---|---|
| V1 | double-quote multi-line block off | 1, `C2V_multiline_quote_withheld` |
| V2 | CR strip off | 1, `C2V_crlf` |
| V3 | repo-relative path accepted from any cwd | 1, `C2R_repo_relative_from_wrong_cwd` |
| V4 | SALT dropped from the class | 1, `C2V_class_SALT` |
| V7 | mask leaks the value's first character | 27 |
| V8 | inline comment printed raw | 2 |
| V10 | realpath check off | 1, `C2R_symlinked_folder` |
| K1 | exemption regex without its end anchor | 5 C2H cells |
| K2 | exemption ignores the cwd | 1 |
| K3 | any python accepted | 1, `C2H_usr_bin_python3` |
| K4 | any viewer path accepted | 2 |
| K5 | Read tool exempted | 16, C1 and C2D Read cells |

The four survivors are in G303-2156-8.

**My own mutants on round 1.** 6 mutants, all killed:

| Mutant | Change | Named cells red |
|---|---|---|
| R1_S6_keys_off | key and certificate class off | 4 |
| R1_grep_tool_glob_off | Grep tool glob check off | 2 |
| R1_compose_config_off | compose config check off | 2 |
| R1_fail_open | errors allowed instead of refused | 7, C8 |
| R1_heredoc_scan_off | heredoc scan off | 1 |
| R1_symlink_resolve_off | symlink resolution off | 2 |

**Hook-exemption probes** (`scratchpad/probe/hook.py`). These are exactly as stated:
- **Refused:** a double slash in the path, a trailing `#c`, a trailing backslash, `python3.9`, and `cp` or `mv` of a secret onto a viewable path.
- **Allowed:** the absolute form with extra spaces.
- **Trailing NBSP:** the hook lets it through the round-1 rules because the word is not a secret name. The viewer then refuses the argument, so nothing prints.

**(3) PR body.** Read live by GET.
- Title: "Refs KS-1785: Claude Code sessions refuse to print a secrets file, with a masked viewer for the three systemTest env files". The ruled title change is done.
- The body states that the design is Wednesday's ruling and not Kam's.
- It states that CLASSES and NAMES are copied from the specs and no platform-s code was read.
- It carries the stated residual word for word, plus R-b and R-c.
- It names the follow-ups: the permissions.deny Read list, platform-s parity, and both secrets.example.yml comments.
- It keeps round 1's residuals: @-references, the onFailure version, unmeasured machines, the restart, and the KS 915 disclosure with its check-ignore table.
- KS-1785 comment 9568f77a was read by GraphQL. It is edited in place, carries the "Edited" note, and claims no more than the diff. The ticket is In Progress and was not moved.

**The residual, tested against the three real templates** (`scratchpad/probe/tpl.py`, the tracked `.example` files fed through the viewer as the real file names). The counts match the seat:

| File | In clear | Masked |
|---|---|---|
| docker.env | 13 | 6 |
| akto/.env | 5 | 0 |
| playwright/.env | 0 | 0 |

- The 6 masked names in docker.env are AKTO_ADMIN_PASSWORD, AKTO_MONGO_CONN, MONGO_INITDB_ROOT_PASSWORD, ME_CONFIG_MONGODB_URL, ME_CONFIG_BASICAUTH_USERNAME and ME_CONFIG_BASICAUTH_PASSWORD.
- With every commented `NAME=` line uncommented, as a user following the templates would:
  - **akto/.env:** GRAFANA_ADMIN_USER prints in clear; GRAFANA_ADMIN_PASSWORD is masked.
  - **playwright/.env:** TEST_ADMIN_EMAIL prints in clear; TEST_ADMIN_PASSWORD and API_TOKEN are masked. AUTH_TOKEN_PATH, AUTH_STATE_PATH and REDACT_SECRETS are also masked, which is harmless over-masking.
- No template password printed in any variant.
- The one material point is in G303-2156-5.

**(4) Other behaviour.**
- Round 2 adds one call in `decide`. It applies only to Bash, and only to a whole command that is exactly the viewer command. Round 1's rules are unchanged; I read the round-2 diff of `block_secret_reads.py`.
- KS-915 suite `restore_local_secrets.test.sh`, with node_modules borrowed by symlink from s-g33-ks1785: 421 passed, 0 failed at the head, and 421 passed, 0 failed at develop. The head shows the re-pointed control `ks915-control.txt` as NOT ignored.
- develop's KS-2129 closed-pipe scanner reads a fixed list of 7 files and does not include the new wrapper, so the merge does not interact with it.

**(5) Closing words.** None in closing form in the title, the body, the 3 commit messages or the 1 PR comment (the Linear linkback). The pattern was proved against a planted "Fixes KS-1785", which it matched.

**(6) Census.**
- Contract test: 341 at the head against 0 at develop, where the file does not exist.
- KS-915 suite: 421 against 421.
- Open-PR census, GET over 80 open PRs: each of the 14 paths hits PR 2156 only. The method sees other PRs' env and .claude files (PRs 2148, 2067 and 2052 are listed), which serves as the positive control.
- The planted control `adminConfig.ts` hit nothing. The PRs the seat named for it (2087 and 2158) no longer list that file, cause not checked.

## NOT TESTED
- Preflight leg 14 whole, 124 suites. Only its KS-915 and contract members were run.
- Leg 9.
- docs-fragments.
- The real Claude Code hook invocation, and Peter's and Stuart's machines.
- compose-go's own .env parser. The viewer was compared with dotenv 18.0.9 only, the version both runners load. docker.env is also read by compose `env_file`.
- My probes ran under 3.14.9 only. The contract test ran under both Pythons.

## Findings

**G303-2156-1 (Minor; recommend a small fix commit). A password prints in clear when a file uses a lone CR as its line separator.**
- The viewer splits lines on `\n` only and strips one trailing `\r`.
- dotenv 18 turns `\r\n?` into `\n`. So for `HOST_A=x\rDB_PASSWORD=<v>`, the loader sees two variables, and the second is a class-named password.
- The viewer prints `HOST_A=x\rDB_PASSWORD=<v>` in clear (probe P1).
- No cell covers it: C2V_crlf tests CRLF only.
- Fix: split on `\r\n|\r|\n`, or withhold any line that still holds a `\r` or another control character.
- It is unlikely on a Mac-edited file, but it breaks "every password masked" under the loader's own parse.

**G303-2156-2 (Minor). The quoting model is narrower than dotenv's, so lines inside a multi-line value print.**
- The viewer withholds a multi-line value only when it opens with `'` or `"` immediately after the `=`. dotenv also accepts:
  - backticks (P2)
  - whitespace before the quote, as in `NOTE= "a` (P3)
  - the escape `\'` inside single quotes (P5)
  - a different escape reading inside double quotes, `\\"` (P6)
- In each case the inner lines that look like `NAME=value` print in clear.
- By the loader's parse those lines belong to a non-class name, so this is inside the stated residual by name.
- But the body and CLAUDE.md say "multi-line quoted values" are withheld, which is not true for these spellings.
- A base64 tail line such as `Ab12cd==` inside a backtick PEM would print as `NAME=value`.

**G303-2156-3 (Note). Not every inline comment is withheld.**
- dotenv ends an unquoted value at any `#`. The viewer splits only at a space or tab followed by `#`.
- So `HOST=x#text` prints `#text`, which the loader treats as a comment (P4).
- The body says "any inline comment" is withheld.

**G303-2156-4 (Minor). The .gitignore residual is understated in the body.**
- The eight lines leave SIX names unignored: `.env.e`, `.env.le`, `.env.ple`, `.env.mple`, `.env.ample` and `.env.xample` (`git check-ignore --no-index`, with core.ignorecase both true and false). The body names only `.env.e` and `.env.xample`.
- On macOS, where core.ignorecase is true, `.env.EXAMPLE` and `.env.Example` are also unignored. This agrees with the hook, which treats them as templates.
- The hook still refuses reads of all six names (S2).

**G303-2156-5 (Minor; Wednesday or Kam to judge). Two of docker.env's 13 clear-text names are written from Azure Key Vault.**
- `systemTest/akto/scripts/sync-secrets.sh` lines 67 and 70 write AKTO_ADMIN_EMAIL and MONGO_INITDB_ROOT_USERNAME from the vault secrets akto-admin-email and akto-mongo-root-user.
- So in a vault-synced docker.env the viewer prints these vault-held identities in clear.
- The template's own comment says AKTO_ADMIN_EMAIL reuses the Secuura issuer account's email.
- The residual's words ("a user name or an email address") cover this. That these two values come from the vault is not stated.
- A USER/EMAIL class word, or a name list taken from sync-secrets, would close it.

**G303-2156-6 (Note; R-c). CONN, CONNECTION and DSN are not in the class, and a secret in a value with no userinfo prints in clear.**
- R-c is confirmed by probe: `DB_CONN=...;Password=<v>`, `AZURE_STORAGE_CONNECTION_STRING=...;AccountKey=<v>`, a DSN carrying `?sentry_key=<v>`, and `MONGO_URL=...?password=<v>` all print in clear (P9, P9b, P10).
- None of these names is in the three templates today.
- The body states the CONN/DSN case. The decision is still Wednesday's open R-c.

**G303-2156-7 (Minor; a round-1 gap that round 2 inherits). `ln` is in NAME_ONLY.**
- `ln <any secret> <name>` is allowed (probe):
  - `ln Blockchain/Dev/.env /tmp/x.txt` followed by `cat /tmp/x.txt` reads that secret RAW. A hard link is not a symlink, so the realpath check does not see it.
  - After `rm systemTest/akto/docker.env; ln Blockchain/Dev/.env systemTest/akto/docker.env`, the viewer shows that other secrets file masked (it passes realpath, O_NOFOLLOW and S_ISREG).
- It is a deliberate two-step, so it is outside the stated "accidental reads" model, but it costs very little to close: check `ln`'s source operands the way the copiers' are checked.

**G303-2156-8 (Note). Four of my round-2 mutants survive with every cell green.**
- V5: a tab before `#` is not split as an inline comment.
- V6: no backslash escape inside double quotes.
- V9: O_NOFOLLOW off. The realpath check covers this, as defence in depth.
- V11: output written incrementally instead of built in memory and written once.
- So the claims "output is built in memory and written once" and "tab inline comment withheld" are not pinned by any cell.

**G303-2156-9 (Note). The mask prints the value's length** (`<masked: N chars>`). This is documented. It is a small disclosure for short passwords.

---

PR 2154: GO WITH NOTES

## FOUND / TESTED / HOW

**(1) Touched set:** exactly `services/originate/src/events.ts` (+5/-2) and the new ks2094 test (+109).

The change lines equal the held o121 Spark patch per file and in order, 7 and 109 lines. A copy with one planted difference reads not equal.

**(2) Red-first and mutants.**
- On develop's events.ts the new file gives 3 red (R1, R2, R3) and 2 green (C1, C2). At the head, 5 of 5.

My own mutants:

| Mutant | Change | Result |
|---|---|---|
| A1 | remove the inner try | R3 red |
| A2 | drop `type` from the warn | R1 and R3 red |
| A3 | rethrow after the log | R1, R2 and R3 red |
| A4 | warn becomes info | R1 red |
| A5 | change the constant | R3 red |
| A6 | log in the no-client branch | C2 red |
| A7 | add the payload to the log | **0 red** (G303-2154-3) |

**(3) Required statements in the live PR body:** all present and true as measured.
- the tier-1 line
- "ADDS a log line and changes no control flow"
- the NOT-done list
- the caller count, 7 non-test call sites in 3 files (counted 1 + 5 + 1), with runtime volume UNMEASURED

**(4) Other behaviour.**
- The catch still swallows, so `publishEvent` resolves.
- The `!redis` branch is untouched.
- The log carries only the type and the reason, not the payload.

**(5) Closing words:** none in closing form in the title, body or commit.

**(6) Whole originate suite.**
- develop: 220 suites, 2,592 passed, 0 failed.
- One merged tree of 2154 and 2160: 222 suites, 2,601 passed, 0 failed (2,592 + 5 + 4).
- R 93rd's "baseline reds did not reproduce" holds.

**eslint:** 0 errors and 2 warnings, both an unused `no-require-imports` disable directive, at lines 51 and 78 of the new test. R 93rd's flag is confirmed.

## NOT TESTED
- tsc with test files.
- A real Redis.
- Linear comment 1049d72b.

## Findings
- **G303-2154-1 (Minor):** cell R2 is titled "logs one warning naming the type and the message" but asserts neither the level nor the type. Mutants A2 and A4 both leave R2 green. R1 and R3 do catch them, so coverage holds; the label claims more than the cell checks.
- **G303-2154-2 (Note):** the two unused eslint-disable directives are confirmed.
- **G303-2154-3 (Note):** no cell pins the payload out of the log. With A7, `userId` on `user.erased` would be logged and every cell stays green. The product as written does not log it.
- **G303-2154-4 (Note):** the body says the commit between d0b4825cc244 and 0d286210f98b "changes one api-gateway test". It changes an auth test, ks1858. The path is unrelated, so this is a wording slip.

---

PR 2155: GO WITH NOTES

## FOUND / TESTED / HOW

**(1) Touched set:** exactly `services/nft-certificate/src/services/minting.service.ts` (+4/-4) and the new ks1984 test (+114).

The change lines equal the held patch, 8 and 114 lines, with a planted-difference control.

**Read sites.** `JSON.parse(row.public_fields` appears exactly 4 times, at lines 123, 505, 592 and 678. A control grep reads 0. There is no fifth read site.

**(2) Red-first and mutants.**
- On develop's product, 5 red (R1 to R5) and 2 green (C1, C2). At the head, 7 of 7.

My own mutants, each reverting one site:

| Mutant | Change | Result |
|---|---|---|
| C1 | revert line 123 | R5 red |
| C2 | revert line 505 | R1 and R2 red |
| C3 | revert line 592 | R3 red |
| C4 | revert line 678 | R4 red |
| C5 | null fallback becomes 'null' | control C1 red |

Every site is pinned by its own named cell.

**(3) Required statements in the body:** all present.
- the tier-1 line
- the row type still `string`
- the pg JSONB return read from migration 002 and the ticket, not run
- the NOT-measured list

**(4) Other behaviour (read).**
- NULL or empty still gives `'[]'`.
- JSON text is still parsed.
- A JSONB object or scalar string still throws, as on develop.

**(5) Closing words:** none in closing form. The only hits for the bare word are "fix shape (a)", twice.

**(6) Whole nft-certificate suite.**
- develop: 38 files, 241 passed, 0 failed.
- head: 39 files, 248 passed, 0 failed.
- The baseline red did not reproduce, which agrees with R 93rd.

**eslint:** 0 problems.

## NOT TESTED
- tsc with test files. Vitest does not typecheck.
- A real Postgres or the real driver.
- Linear comment 40fa5183.

## Findings
- **G303-2155-1 (Minor):** the body's file counts, "84 files" before and "86 files" after, are wrong. The measured counts are 38 → 39. The cell counts, 241 → 248, are right.
- **G303-2155-2 (Note):** the row type is still `public_fields: string` while the code now accepts an array. This is stated in the body and was out of scope by ruling.

---

PR 2160: GO WITH NOTES

## FOUND / TESTED / HOW

**(1) Touched set:** exactly `services/originate/src/routes/certifications.ts` (+7/-1, at line 935 on develop) and the new ks2017 test (+173).

The change lines equal the held patch, 8 and 173 lines, with a planted-difference control.

**(2) Red-first and mutants.**
- On develop's product, R1 and R2 fail by the 3 s timeout (no answer) and C1 and C2 pass. At the head, 4 of 4.

My own mutants:

| Mutant | Change | Result |
|---|---|---|
| B2 | change the constant | R1 and R2 red |
| B3 | non-Error branch becomes 'x' | C2, R1 and R2 red |
| B4 | Error branch becomes 'x' | C1 red |
| B1 | remove the try | did not compile, so not a valid mutant |

develop's original line serves as the remove-the-try mutant, and it reddens R1 and R2.

**(3) Required statements in the body:** all present.
- the tier-1 line
- no charge, reservation or anchoring call is touched, with counts (0 against 34 mentions of "charge")
- the revoked-Proxy case not done and the ticket left open
- the KS 2008 file-neighbour note

**(4) Other behaviour.**
- In probe P4, a failing issue makes 0 charge and 0 reserve calls, at the head and at develop.

My own probes:

| Probe | Head | develop |
|---|---|---|
| P1, revoked Proxy | no answer | no answer |
| P2, Error whose `message` getter throws | no answer | no answer |
| P3, Error with a non-string `message` | 500 | no answer |

- P1 matches the stated residual.
- P3 is better at the head than develop: develop never answered.

**(5) Closing words:** none in closing form.

**(6) Whole originate suite:** develop 2,592 / 0 failed; the merged tree 2,601 / 0 failed.

**eslint:** 0 problems.

## NOT TESTED
- tsc with test files.
- A live certification issue.
- Linear comment ee39668b.

## Findings
- **G303-2160-1 (Note):** the body's "one observable difference" sentence undersells the change. It says the logged msg is now a string where before it was the raw value. In fact, on develop that request never got an answer, because `msg.includes` threw. At the head it answers 500 (P3). This is an improvement the body under-describes, not a regression.
- **G303-2160-2 (Note):** an Error whose `message` getter throws still gets no answer at both develop and the head (P2). It is not claimed by this PR and is a candidate for KS-2017's open remainder, next to the revoked Proxy.

---

**Evidence and workspace.** Evidence is in this session's scratchpad, `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/15181365-5e12-4b94-a706-b81bce923a5c/scratchpad/`:

| Path | Contents |
|---|---|
| `r0/` | R0 and R0b runs, the KS-915 suite runs |
| `mut/` | my mutants for PR 2156 |
| `probe/` | the viewer, template and hook probes |
| `census2156.txt` | the open-PR census for PR 2156 |
| `pr2156_body.md` | PR 2156's live body |
| `out/`, `tools/` | the R 93rd batch |

- The scratchpad totals 2.8 GB.
- DevMASTER had 92 GiB free at the start and at the end.
- No rm was run outside the scratchpad.
