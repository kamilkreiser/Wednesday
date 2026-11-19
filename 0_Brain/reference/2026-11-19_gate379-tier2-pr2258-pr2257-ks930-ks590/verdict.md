PR 2258: GO WITH NOTES (at head e8f1b607b3d1252eee4315334c90c58e92b64d01; tier 2)
PR 2257: GO WITH NOTES (at head f4c372d24aabd115dc2cc5d48a0abdf445d93c17; tier 2)

Gate 379, QA gate, Sonnet, 2026-11-19 ~19:3x AEDT. Findings only; nothing posted, merged, pushed or written outside this folder.
Pins re-read by `gh api` (account kksecura verified) at the start AND again just before this verdict: PR 2258 head e8f1b607b3d1, PR 2257 head f4c372d24aab, develop 06328efa1770 (unmoved). Both PRs are open, not draft, base develop, one commit each.
Load gate: load1 read before every suite and mutant batch: 3.2 to 4.8, one start at 6.3 (the develop tier run); all under 8.
Work tree: scratch clone `scratch/clone` plus worktrees `w2258`, `w2257`, `wdev` (develop). The Secuura project was only read (one local `git clone` source).

## PR 2258 (KS-930), at e8f1b607b3d1

### Q1 diff. MEASURED (git diff --numstat origin/develop...pr2258): 4 files. `check-shared-relink.sh` 90/36, `check_shared_relink.test.sh` 235/0, fragment pair cheat 3/0 and flow 4/0. No other product file, no Dockerfile. The other three suites are untouched (the PR says the guard is the only product file; confirmed).

### Q4 THE CONTROLLING CHECK. MEASURED (script `q4.sh`): guard of develop vs guard of head, each over its own real tree, default mode and SHARED_RELINK_STRICT=1: all four rc 0, output byte-identical between develop and head in BOTH modes (diff printed IDENTICAL twice): `OK - 25 Dockerfile(s) ... derived: 4 copy a builder's node_modules, 21 re-install their own. dev-tree (KS-490): 25 of 25 clean.` No real Dockerfile is newly blocked. (The positive control that the guard can block at all: probe fixtures B4..B7 block rc 1 through the same guard.)

### Q3 suites at head. MEASURED (script `q3.sh`, full clone with history, load1 3.7): check_shared_relink 140 passed, 0 failed, 0 skipped; _case 6/0/0; _derived_claims 17/0; _tooling_tokens 6/0. All four rc 0.

### Q2 cells meaningful. MEASURED (script `allmut.sh`, one counted change each, guard sha256 b09f725d7b34aca5 equal before and after every run, restored by git checkout):
- m1 token scan reverted to leading-word only (my change keeps the JSON normalisation): 17 red = the absolute path, env, exec, time, nice, nohup, command, xargs, sudo -u, ./node_modules/.bin, corepack yarn, corepack pnpm, if, for, braces, sh -c, echo with backticks. Matches the builder's 17. JSON cell green.
- m2 left boundary dropped: 1 red (the existing KS-945 `mynpm i` cell). Matches.
- m7 printer exemption removed: 2 red (echo, printf controls). Matches.
- m9 backtick switch-off removed: 1 red (echo with backticks control). Matches.
- m6 heredoc arm removed (extra): 1 red (the heredoc-after-re-link cell).
- My own aimed at the token-scan boundary and the printer exemption (guard restored each time):
  - o1 drop `.` from the boundary class: 0 red (SURVIVES, 140 passed).
  - o2 drop `-` from the boundary class: 0 red (SURVIVES).
  - o3 drop the end anchor `$` of the manager regex: 0 red (SURVIVES).
  - o4 printer exemption widened from "leading word is echo/printf" to "any word of the segment is echo/printf": 0 red (SURVIVES). This is the dangerous direction (it would make `RUN npm install echo` read clean; the product today blocks it, probe B7).
  - o5 trailing-argument rule removed: 3 red (KS-945 argument cell, F-6 cell, R2 row 1b). Pinned.
  m3, m4, m5, m8 were NOT reproduced by me (the commission named m1, m2, m7, m9).

### Q6 awk quoting. MEASURED: `bash -n` on the head guard rc 0; zero apostrophes on the 126 added lines (count 0; positive control: the whole file holds 23 apostrophes outside the new lines, and a planted apostrophe in a copy made `bash -n` fail rc 2, "unexpected EOF while looking for matching"); the suites and the real-tree runs execute the awk program. Backticks inside the comments sit inside single quotes and are inert.

### Q5 adversarial. MEASURED (script `probe.sh`: canonical skeleton, spelling placed after the re-link, SHARED_RELINK_STRICT=1, develop vs head; rc 1 = blocked):
Should block, my own spellings (not in the builder's list):
- `RUN timeout 300 npm ci` develop 0, head 1 BLOCKED
- `RUN su node -c "yarn install"` 0 -> 1 BLOCKED
- `RUN ["/bin/sh","-c","pnpm install"]` 0 -> 1 BLOCKED
- `RUN setsid npm ci` 0 -> 1 BLOCKED
- `RUN /bin/sh -lc "yarn install --frozen-lockfile"` 0 -> 1 BLOCKED
- `RUN eval "npm ci"` 0 -> 1 BLOCKED
- `RUN printf "%s" x && /usr/bin/env -S npm ci` 0 -> 1 BLOCKED
- `RUN npm install echo` 1 -> 1 blocked (the printer exemption does not swallow an argument named echo)
- `RUN npm --prefix . ci`, `RUN echo ok | tee /tmp/x && yarn` blocked both.
STILL FALSE CLEAN at head (all also clean on develop, so not regressions):
- `RUN $(which npm) ci` rc 0
- `RUN npx npm@10 ci` rc 0
- `RUN node /usr/local/lib/node_modules/npm/bin/npm-cli.js ci` rc 0
- `RUN corepack yarn@4.1.0 install` rc 0 (a version-pinned corepack word does not END in yarn)
- `RUN pm=npm; $pm ci` rc 0, `RUN exec "$(command -v npm)" ci` rc 0
- `RUN corepack yarn` and `RUN echo npm ci | sh` rc 0 (both named in the PR residue).
Should stay clean, all rc 0 at head: `echo "installing npm ci later" > /tmp/note`, `printf "yarn install\n" > /tmp/x`, `touch yarn.lock`, `npm cache verify` (develop 1, head 0: the intended R4 fix), `npm config set update-notifier false`, `chown -R node:node /app`, `apk add --no-cache nodejs npm`, `npm-run-all --version`, `rm -rf /root/.npm /tmp/x`, `echo $HOME`.
NEW FALSE BLOCKS at head (develop 0, head 1):
- `RUN mkdir -p /opt/yarn /opt/x`
- `RUN ln -s /usr/bin/yarn /usr/bin/y`
- `RUN chown node /usr/local/lib/node_modules/npm /x`
- `RUN apk add --no-cache nodejs npm yarn`
Still false block both: `RUN npm pkg get name` (the builder's named open item, reproduced).

### Q7 residue vs measured. The PR body names: heredoc that contains the re-link, non-final runtime stage, `echo npm ci | sh`, bare `corepack yarn`, `apk add nodejs npm curl` plus a harmless heredoc, `npm pkg get`. All reproduce where I tried them (`corepack yarn`, `echo|sh`, `pkg`, apk-class). The PR body is NOT complete: the path-argument false blocks (F1 to F3) and the versioned and indirect false cleans below are not named. No closing keyword (count 0, control 1); title starts `Refs KS-930:`; Test Evidence and the verbatim "NOT a pass" block are present. The builder's hook figures (13 of 16 legs, 832 s) are the builder's, not re-measured.

### Q8 merge-tree. MEASURED (script `mt.sh`, `git merge-tree --write-tree`): develop+pr2258 and pr2258+develop both rc 0, same tree 088c9442815d. Also pr2258+pr2257 both orders rc 0 (3ede90b89c67). Planted-conflict control (a commit editing the same guard lines) rc 1 with a conflict listed.

### Findings 2258
- G379-2258-1 LOW (test gap, no product defect): four boundary and exemption mutants survive all 140 cells (o1 dot, o2 dash, o3 end anchor, o4 exemption-anywhere). o4 is the one that matters: only the leading-word form of the exemption is pinned, so a later widening that makes `RUN npm install echo` read clean (a false clean after the re-link) would pass the suite. Fix: one cell `RUN npm install echo` expects rc 1, one cell each for a `.npm`-style path argument and `npm-run-all` word if the boundary is meant to be pinned.
- G379-2258-2 LOW (friction direction, reach zero on the 25 real files): the whole-word scan newly false-blocks any word that merely ENDS in npm/yarn/pnpm after a `/` and is followed by another word (mkdir, ln -s, chown paths), where develop was clean. Real tree unaffected (identical in both modes). PR residue names only the apk class. Fix: add to the PR "known false blocks", or skip a manager word whose next word is not a verb-like token for non-wrapper leading words.
- G379-2258-3 LOW-MEDIUM (false-clean direction, pre-existing, reach: 0 of 25 files): versioned and indirect spellings still certified clean: `corepack yarn@4.1.0 install`, `npx npm@10 ci`, `$(which npm) ci`, `node .../npm-cli.js ci`, `$pm ci`. Not regressions and not claimed by the PR (it claims twelve spellings), but the versioned corepack form is the shape a real Dockerfile would use. Residue for KS-930, not a block for this PR.
Why not NO GO: no newly blocked real Dockerfile, no regression against develop on any spelling I tried, 140/140 and three sibling suites green, the builder's m1/m2/m7/m9 reproduced exactly, merge clean. Why not plain GO: findings 1 to 3.

## PR 2257 (KS-590), at f4c372d24aab

### Q1 diff. MEASURED (numstat): 7 new files, 0 deletions (+1708): `tests/support/verify_public_view.py` 403, `tests/test_verify_public_view.py` 404, `tests/unit/support/test_verify_public_view.py` 351, `tests/unit/support/test_verify_public_view_drives.py` 339, `tests/integration/test_verify_certify_keeps_anchor.py` 197, plus NEW fragment pair `KS-590-systemtest-public-verify-view-regression.html` (cheat 9, flow 5). The PR 2249 pair is not in the diff. (The line counts include blanks and docstrings; the repo cap is 400 logical lines, the builder says the largest is 210, not re-measured.)

### Q2 predicates vs Kam's rules. Read whole: `verify_public_view.py`. The rules are the three quotes, verbatim in the module docstring and beside assertions. A null title is a violation (the reversed withholding), a null issuer is allowed, `fieldsWithheld` true is a violation, `certifierOrganizationId` must be null with the key kept, a company name containing an at-sign is a violation. The ticket's older withholding is not written. MEASURED leak probe (`leakprobe.py`, 15 planted answers, forbidden map = email, local part, user id):
- CAUGHT: certifiedBy equal to the local part; certifierOrganizationId = user id; an email anywhere (the at-sign scan, including inside lists and onChainMetadata); local part or user id as an exact string anywhere including inside lists and under an unknown key; upper-case local part; issuer equal to the user id.
- PASSED (the predicate returned no violation on an answer that leaks): the local part EMBEDDED in a longer string (`jane.doe (Acme Pty)`); the user id embedded (`Acme Pty ref u-4f2a91`); a numeric user id (int) under an extra key; and, with `forbidden=None`, an issuer equal to the bare local part (the check exists only through the caller's forbidden map).
These are G379-2257-1 and -2 below.

### Q3 mutants. MEASURED (script `mut57.sh`; control: 69 passed; predicate sha256 f78b8debd0a9d36f equal before and after):
- m1 local part ignored: 2 red (U2 email-local-part; row-4 drive "another tenant sees a local part"). m3 null title accepted: 1 red (U1 withholding shape). m4 pair equality ignores one-sided keys: 1 red (U3 richer same-tenant answer). All three match the builder.
- m2 (org id ignored): 1 red (U2 certifier-org-id). m5 (count never compared): 1 red (U4).
- Own, aimed at paths the builder did not pin: o1 at-sign scan off: 1 red; o2 onChainMetadata check off: 2 red; o4 user-id label off: 1 red; o5 missing-key check off: 1 red; o6 `matches[-1]` for `matches[0]`: 3 red; o7 `exact` count off: 1 red; o8 issuer/certifiedBy check reduced to a type test: 1 red.
- **o3 SURVIVES (0 red, 69 passed): removing the list branch of the string scan** (a person-derived value inside any list nested in an answer, e.g. a history or lineage array, would then pass). The product code scans lists correctly (my probe L3 and L4 caught); no cell pins it. G379-2257-3.

### Q4 unit and functional tier, head vs develop. MEASURED (script `tier.sh`; `pytest tests/unit/ tests/functional/ -q -rfE --continue-on-collection-errors`, load1 6.3 and 4.9). Venv: the shared copy at worktrees/s-t25-stack (Python 3.14.10, schemathesis 4.32.1, pytest 9.1.1, ruff 0.17.1, mypy 2.4.0), the builder's choice, run through its python binary against my trees (`src` resolves to the tree under test). No venv on this machine meets the pins (schemathesis ==4.33.4, pytest >=9.2.0, ruff >=0.17.5, mypy >=2.4.1) and I installed nothing. Without `--continue-on-collection-errors` the run stops at 3 collection errors, on both trees. Develop 44 failed, 4437 passed, 4 skipped, 65 errors. Head 44 failed, 4506 passed, 4 skipped, 65 errors. DIFFERENCE: +69 passed, and the sorted list of 109 failed/error ids is IDENTICAL on both (diff empty): 0 new, 0 gone. (The builder says 43 failed and 108; my 44 and 109 are the same on both trees, one flaky id under load, so the difference is unaffected.) Causes of the shared red: IgnoredAuth / AuthScenario import errors against schemathesis 4.32.1 and the venv-pin parity tripwire.

### Q5 live cells refuse a remote before any write. Read: autouse module-scoped fixture `_local_slot_only` calls `pytest.fail` unless `is_local_gateway_url(api_base_url)`; it is the same pattern as the sibling `test_tenant_isolation_gateway_create.py` (line 36 to 46) and the module docstring says a refusal is an ERROR, not a skip. Autouse module scope runs before `isolation_tenant_a` (which may create a tenant). Row 1 (`test_verify_certify_keeps_anchor.py`): `skip_unless_real_anchoring(api_base_url)` is called after the scenario is registered and BEFORE `create_document`, so a local mock target creates nothing and is excluded by design (not run on a local target). On a remote target row 1 DOES write (demo, testnet ADA): by design, held. MEASURED only by reading; the live cells were not run.

### Q6 ruff and mypy on the 5 files. MEASURED (script `lint.sh`): `ruff format --check`: 5 files already formatted; `ruff check`: all checks passed; `mypy --ignore-missing-imports --explicit-package-bases`: success, no issues in 5 files. Planted controls (a copy outside the tree with an unused variable and a wrong return type): ruff F841 reported 1 error, mypy reported 1 error. Note: the package's own mypy gate (quality_gate.py) covers `src/html_report`, `scripts` and `config`, NOT `tests/`; mypy on these files is an extra, not the repo gate. Pinned ruff/mypy versions differ from the venv's (ruff 0.17.1 vs >=0.17.5, mypy 2.4.0 vs >=2.4.1).

### Q7 merge-tree. MEASURED: develop+pr2257 and pr2257+develop both rc 0, same tree ccf511a3a3de; pr2257+pr2258 both orders rc 0; planted-conflict control rc 1.

### Findings 2257
- G379-2257-1 MEDIUM: the leak predicates match by EXACT equality against a caller-supplied forbidden map. A local part or a user id embedded in a longer string passes (`jane.doe (Acme Pty)`, `Acme Pty ref <id>`), a numeric id passes, and with no map the local part passes. Emails are caught everywhere (at-sign). Under the commission's wording ("a predicate that would PASS an answer leaking a local part or user id") the embedded case is reached; I graded it Medium rather than NO GO because the shapes Kam named and PR 2249's pre-fix shape (the bare local part, the bare user id as `certifiedBy` / `certifierOrganizationId`) are caught, and a substring match risks false reds on company names. Wednesday may re-grade. Fix: match the local part (>= 4 chars) and the user id as substrings, case-folded, and add cells for the embedded forms and for an int id.
- G379-2257-2 MEDIUM: `forbidden_for` returns an EMPTY map when the bearer token has no decodable claims, and the live row-4 cell does not assert the map is non-empty. The local-part and user-id checks then vanish silently while the cell reads green (systemTest MUST 13 rule 6: a check whose input is missing must go red). Live NOT RUN, so whether the claims carry email and sub is UNMEASURED. Fix: assert `forbidden` holds the email, local part and a user id before running row 4.
- G379-2257-3 LOW: mutant o3 (list scan removed) survives all 69 cells; add a cell with a person value inside a nested list.
- G379-2257-4 LOW: "another tenant's signed-in caller" and "own tenant" are the same SYSTEM_ADMIN account with `X-Tenant-Override` (the builder's declared recipe, accepted in Wednesday's ANSWER). Rows 4 and 5 therefore show the answer does not vary with the tenant context of a super-admin, not that an ordinary tenant-B user receives the anonymous answer. Row 5 on its own compares two answers for equality and cannot detect a leak both receive; row 4 carries the leak check.
- G379-2257-5 INFO: the builder's own list holds; systemTest/CLAUDE.md narrative lists not edited (declared deviation 3), one extra unit file (deviation 1), the push hook printed nothing (builder's inference, not measured by me).

## Plainly: every live cell is NOT RUN (L2 to L5, row 1 and the live row 2 to 5 bodies). The MockTransport drives only show the predicates and bodies can fail and pass; whether the platform answers as the stand-in does is unmeasured. Whether two registrations can share a content_hash through the public API is unmeasured. Chain-first answers are unreachable on a mock stack.

## NOT COVERED
PR 2258: the hook run (13 of 16 legs) and the builder's 39-fixture probe and census of 125 leading manager words are the builder's, not reproduced; m3, m4, m5, m8 not reproduced; shellcheck not run; no run inside the repo's real pre-push hook; heredoc-contains-re-link and non-final-stage residue not re-measured; the fragment pair's `docs-fragments.mjs check` not run.
PR 2257: every live cell (NOT RUN, no stack, no slot, no remote target); row 1 on a real-anchoring target; the `quality` command and the 90% coverage gate not run; docs-fragments check not run; the hook's silence not measured; the 400-logical-line cap not re-counted; node, ruff and mypy are not at the repo pins; the unit-tier red ids are venv-dependent, only the DIFFERENCE is claimed.
