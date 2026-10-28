# QA gate 9 (TIER 1, batch, round 1 of 2): Secuura #1796 (KS-1458), #1798 (KS-1459 item 2), #1797 (KS-1219), #1799 (KS-1467 services/auth half)

- **Gate model:** Claude Opus 5.5 (claude-opus-5-5), G1 tier-1 gate (auth surfaces), subagent of Wednesday. Spark review model: deepseek-v4-flash via the tunnel. Routing receipt as commissioned: claude-opus-5-5, G1 tier-1 gate (auth surfaces), gauge ~85%.
- **Pushed / merged / commented / edited / mailed / Linear-written:** nothing.
  - Linear was read only: KS-1458, KS-1219, KS-1459 and KS-1467, each with comments first:100, through my own reader `gatework9/linear_read.py` (a GraphQL query, no mutation; copied from gate 7). The key was never printed. spark_review read the same four tickets with its own reader.
  - **`gh` is not authenticated in this shell ("You are not logged into any GitHub hosts"), so the PR bodies were NOT read.** Each head's commit message, plus the author's READY comment on the Linear ticket, stood in for the body. The commit message went to Spark as the PR description, flagged as such.
- **Clone:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate9-tier1/repo`.
  - The path did not exist (`ls`: No such file); I made it with `git clone --shared .../spark/cache/src`, then set origin to `git@github.com:Secuura/Distributed_Secuura.git`.
  - `git -C <path> rev-parse --show-toplevel` was asserted equal to the path before the first fetch, before the end-of-gate fetch, and inside every Python driver that wrote objects. Re-read at the end: same.
  - The deploy key went through GIT_SSH_COMMAND (`!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw`, `-o ServerAliveInterval=30 -o IdentitiesOnly=yes`), the mechanism gate 7 recorded (`gatework9/env.sh`).
- **Worktrees**, all under `/private/tmp/claude-501/gatework9/`. None was removed (no-delete rule).

  | worktree | sha | role |
  |---|---|---|
  | `w1796` | 8f022984 | #1796 head |
  | `wb1796` | bf681065 | #1796 merge-base |
  | `w1798` | acdb4822 | #1798 head |
  | `wb1798` | 8fbda28e | #1798 merge-base |
  | `w1797` | 0b3cac50 | #1797 head |
  | `w1799` | e14baaa3 | #1799 head |
  | `wb1797` | bd6697e0 | the shared merge-base of #1797 and #1799 |
  | `wmerge9698` | scratch commit ee705fda | develop d4fc0b8 + #1796 + #1798 (docs html left conflicted; code merged clean) |

  - Every probe and mutant ran from `gatework9/quarantine/` and was moved back out after the run. Every mutated product file was restored from `git show HEAD:`.
  - Final `git status --short` in all eight shows only the two node_modules symlinks, plus my `tsconfig.gate9.json` in `w1796` and `wb1796` (the copy with the test exclude cleared).
- **node_modules:** read-only symlinks made with `os.symlink`.
  - `Blockchain/Dev/node_modules` points at the shared tree's `Blockchain/Dev/node_modules`.
  - **`services/auth/node_modules` points at the shared tree's `services/auth/node_modules`. This is a deliberate change from gate 7's layout, which pointed it at the Dev root; see "Harness finding" below.**
  - Nothing was installed and nothing was written into the shared tree. packages/shared did not need building. Node v26.8.1 (not the repo's LTS 24).
- **Docker / Postgres / ports:** none needed and none started. The only ports bound were the 127.0.0.1 ephemeral listeners inside vitest runs.
- **Load:** `uptime` / `vm.loadavg` before every heavy run (`out/load.txt`). load1 ran 3.7 to 10.1. **No run started at load1 >= 12, so there were no waits.**
- **Spark queue:** `tunnel.sh check` answered UP (`127.0.0.1:47788/v1/models` 200, ssh pid 52462). Before each review the driver checked `pgrep -f spark_review.py` and found none running. The four reviews ran one after the other.
- **Processes:** I stopped none. All of mine were foreground or background drivers that exited on their own. At the end, `pgrep -fl "vitest|spark_review"` found nothing.

## Pins (git ls-remote)

| ref | start (01:35) | end (01:52) |
|---|---|---|
| develop | **d4fc0b8f26415014a31d2b2da73ae2dfdedbc4ac** (= brief) | **cc262c1b6d189457c1ca100c94d06789472f9d9d: MOVED** (#1784 KS-1537 merged at 01:51:55, mid-gate) |
| refs/pull/1796/head | **8f022984aa7477fa16399475cbc0167dcdd06185** (= brief) | same |
| refs/pull/1797/head | **0b3cac5026e33faf64f5e2ffc8e2ca63797d7cb9** (= brief) | same |
| refs/pull/1798/head | **acdb4822304fdf2d6da3d21c38d2ad92e98ef854** (= brief) | same |
| refs/pull/1799/head | **e14baaa37c6996126ad6743aab82af342d018adc** (= brief) | same |

- **Develop's move is immaterial to this gate.** #1784 touches originate, the API yaml and the two Projects Documents html files. It shares **no code file** with any of the four PRs.
- merge-tree against cc262c1 gives the same answer as against d4fc0b8: #1798 rc 0, and the other three rc 1 on exactly the two docs html files (`out/mergetree.txt`).
- Merge-bases: #1796 bf681065 (2 behind develop), #1798 8fbda28e (1 behind), #1797 and #1799 bd6697e0 (7 behind). Code files shared with develop's commits since each merge-base: **0 for every PR.**

## BLUF

| PR | Ticket | Verdict | One line |
|---|---|---|---|
| #1796 | KS-1458 items 1, 2, 4 | **GO WITH NOTES** | **Every claim reproduced.** users.ts is **comment-only** (0 non-comment changed lines). With the test exclude cleared, tsc goes **44 → 43 errors at base vs head; the multiset differs by exactly the one TS1192**, with 0 new. The ratchet is **rc 0 at head** (41 errors, 41 in the baseline, 0 new, 0 stale). Replaying `check.cjs --update` from the base baseline reproduces the head's baseline-auth.txt **byte for byte** (one line deleted, the floor stays 105). The users.ts sentences match `mfa.ts:352-376` (a password account needs only its password; the passwordless branch needs a valid TOTP or backup code, and TOTP is impossible with no secret). The header sentences match `userRepo.ts:173-189` (undefined for a null or empty column `:174`, for no DEK `:179-181`, and for a decrypt throw `:186-188`). The namespace import still reaches live spies: the mock spreads the named exports, and the POSITIVE cell asserts the write once. Suite 1205/1205 on both sides. Note: docs provisional **97** (merge-time renumber). |
| #1798 | KS-1459 item 2 | **GO WITH NOTES** | **Behaviour-neutral for every input the code can see.** My own truth table (9 × 9 pairs × 2 sites = 162 rows): **142 identical and 20 differing, with 0 differing for any target the zod schema admits** (STANDARD, ENHANCED, HIGH, GOVERNMENT). All 20 differing rows have a target of NONE, SOCIAL or BASIC (listed below). The submit route cannot write those targets: `z.enum(['STANDARD','ENHANCED','HIGH','GOVERNMENT'])` at `users.ts:160`, `saveVerificationRequest` is the only writer of `verification_upgrade_requests` in the repo, and its `ON CONFLICT` never updates `target_level`. **The auth copy and the shared copy are element-identical** (`types/index.ts:26` = `policy-engine.ts:22`, 7 of 7, same order). The head binds the constant exactly as claimed, and the six comparison lines are byte-identical to base. Suite 1205/1205 on both sides; tsc build rc 0; ratchet rc 0. Notes are Info only. |
| #1797 | KS-1219 | **GO WITH NOTES** | **The ruled change does what it says, through the real route, on all three carriers.** Arrays, nested arrays, objects, `[]`, `true` and `1` went from **500 server_error** to **400 invalid_request** on GET, on JSON deny and approve, and on form approve. JSON `null` / `0` / `false` went from **302** to **400** (approve **minted a code with the full allow-list** at base; that widening is now closed). **The controls are unchanged:** the GET consent page, the deny 302, and the approve 302 with a code `[openid profile]`, on all three carriers. **No refusal leaks:** every head refusal is the same fixed 148-byte body. The empty string and a 2.6 MB string behave as at base. The PR's 6 cells are 6/0 at head and 3/3 at base (reproduced). Suite 1200 → 1206, 0 failed on both sides. Notes: the null/0/false edge has no PR cell (my A3 to A5 rows measure it); repeated `state` and `code_challenge` still answer 500 (the ticket's "same shape" siblings, not in this PR); scope is neither deduplicated nor bounded (pre-existing); docs carry **84**. |
| #1799 | KS-1467 auth half | **GO WITH NOTES** | **instanceof is fixed for all 19 subclasses plus AppError,** and the wire changes **only for a ValidationError with truthy `details`**. In the handler that is exactly the three weak-password sites (`auth.ts:204`, `:822`, `users.ts:993`). `auth.ts:173` has no details and is unchanged. **Every other branch answers byte-identically, base vs head:** 22 other class rows, ZodError, plain Error, TypeError, a statusCode look-alike, a thrown string and malformed JSON. **N1 really fails on an echo:** the author's echo mutant and a 4-char partial echo both kill it. Through the real change-password route, at head, no candidate is echoed. Suite 1200 → 1235, 0 failed on both sides. **Main note (1799-1, Medium, contract):** the published 422 schema that register and reset reference declares `details` as a **ZodIssue array**, but these 422s now send an **object** `{feedback:[...]}`. KS-1467 itself said "check the published 422 shape first", and the PR does not mention it. Also: there is no route-level cell, and a route-site echo (K3) survives the PR's file; docs carry **84**. |

**Merge order.**

*The K pair (#1796, #1798):*
- **They merge in either order.** users.ts auto-merges (disjoint hunks, `:1177` vs `:13` / `:1373` / `:1488`), and develop → +#1796 → +#1798 gives **byte-identical** users.ts to develop → +#1798 → +#1796, with both hunks present.
- On the merged tree (develop d4fc0b8 + both): tsc build rc 0, ratchet rc 0 (41 / 41 / 0 / 0), and the **auth suite 1205/1205**.
- develop + #1798 is rc 0. Every other pair conflicts only on the two docs html files.

*The R pair (#1797, #1799):*
- They share no code file (oauth.ts vs errorHandler.ts and passwordLoginGate.ts), so they are independent.

**Docs.**
- #1797 and #1799 **both carry 84**, which collides with develop's 84 and with each other.
- #1796 carries **97**, provisional. #1798 has no docs (the escape clause: no cell added).
- Develop's Architecture doc now tops out at **90** (#1784 added it). I did not assign numbers; Wednesday holds the chain.

**Round cap:** none of the four is a NO GO, so round 2 is optional per PR.

---

## Spark shadow (run FIRST; `out/p1796/`, `out/p1797/`, `out/p1798/`, `out/p1799/`)

Method:
- `spark_gate.sh` per PR, **base = `develop`** (never a superseded round sha). Work dirs: `.../scratchpad/gate9/sg<n>`. `--node-modules`: the Dev root.
- Then `spark_review.py`, one request at a time, with `facts_spark.json` = facts minus the two Projects Documents html files, plus HARNESS LIMIT lines (`out/harness_<n>.txt`).
- **#1798 adds no test**, so its run used two EXISTING suites that drive the submit and review routes: `ks1236-approve-never-lowers...` and `ks1194-part2-mfa-auto-approve...`. A 14/14 on both sides is therefore a neutrality signal, not a fix proof, and Spark was told so.

| PR | spark_gate head ; base product code | merge_base recorded | note |
|---|---|---|---|
| #1796 | 5 / 0 ; 5 / 0 (7 s of 32 s) | bf681065 | **Not a fix proof:** the product change is comment-only, so equal is expected. Non-vacuous: product_files is populated. |
| #1797 | **6 / 0 ; 3 pass / 3 fail** | bd6697e0 | Matches R's claim exactly. |
| #1798 | 14 / 0 ; 14 / 0 | 8fbda28e | Existing suites; equal is the expected neutral result. |
| #1799 | **35 / 0 ; 13 pass / 22 fail** | bd6697e0 | Matches R's claim exactly (Spark's 34 cells + N1). |

No suite kind read 0/0.

| PR | Spark review | tokens / time |
|---|---|---|
| #1796 | **GO WITH NOTES**, 6 Notes | 33,801 prompt, 64.6 s, 1 attempt, valid |
| #1797 | **NO GO**, 2 Major, 2 Minor, 2 Note | 36,186 prompt, 60.4 s, 1 attempt, valid |
| #1798 | **GO WITH NOTES**, 5 Notes | 27,618 prompt, 49.4 s, 1 attempt, valid |
| #1799 | **NO GO**, 3 Major, 3 Minor, 2 Note | 21,820 prompt, 61.2 s, 1 attempt, valid |

### Spark Majors checked at source

**#1797:**
- **Major 1** ("null / 0 / false rejected with no test coverage; may break clients relying on the default allow-list"):
  - **TRUE as a test gap.** The author says so too: "read from the guard and is not exercised by a cell". My rows A3 to A5 (deny and approve) measure it: base 302 (approve **mints with the full allow-list**), head 400.
  - **FALSE as a defect.** It is the ruled tightening, and it closes a widening: a JSON `false` scope was granting everything the app may hold.
  - Kept as note 1797-1.
- **Major 2** ("Wednesday's acceptance is unverified"): **FALSE as a defect.** The brief records it as RULED. Spark had no ruling record in its prompt; that is a harness limit.
- **Minors:**
  - "the same mocks as ks804" is unverifiable: immaterial.
  - "R3 asserts only not-called": the claim itself concedes that the assertion is sufficient.

**#1799:**
- **Major 1** ("no test drives the routes; N1 calls the handler directly"):
  - **TRUE as a test gap.** My mutant K3 (users.ts:993 puts the new password into `details`) **survives the PR's 35 cells** and is killed only by my route probe.
  - Not a defect at head: no route echoes.
  - Kept as note 1799-2.
- **Major 2** ("the shared half is unfixed"): **FALSE as a defect.** That is sanctioned narrowing; the shared half is PR #1775 (the KS-1467 comment of 06:22Z).
- **Major 3** ("visible 422 change with no OpenAPI / client compatibility check"):
  - **Directionally TRUE, and it led to the real finding 1799-1.** The published `ValidationErrorResponse.details` is `ZodIssue[]`, and the new body is `{feedback: string[]}`.
  - Spark did not measure the mismatch; it only noticed that no spec check exists.
- **Minors:**
  - The fake `res` is minimal: true, and immaterial. My real-express wire rows agree with N1.
  - S1 and S2 depend on `process.cwd()`: **TRUE**. My mutation runner started vitest outside services/auth and got 33/2 at the unmutated head, with S1 and S2 red. Info, 1799-3.
  - N1 tries only three candidates: **FALSE as a gap in the claim.** At source (`password.ts:171-213`) every feedback string is a literal; only `minLength` is interpolated.

## Spark calibration rows

| PR | Spark verdict | This gate | Spark defects that stand | Real findings Spark missed | Verdict of the verdict |
|---|---|---|---|---|---|
| #1796 | GO WITH NOTES (6 Notes) | GO WITH NOTES | n/a (Notes restate the change) | the ratchet's node_modules dependence (harness), docs 97 | **Right.** 33.8k tokens. Non-vacuous run, but the arms are equal by design (comment-only). |
| #1797 | NO GO (2 Major) | GO WITH NOTES | 0 defects; Major 1 is a true test gap | sibling params still 500 (1797-2); unbounded, undeduplicated scope (1797-3); docs 84 collision | **False NO GO.** It treated a ruled behaviour change as unapproved, and an untested edge as a defect. 36.2k tokens. Non-vacuous: 3 red at base. |
| #1798 | GO WITH NOTES (5 Notes) | GO WITH NOTES | n/a | none material | **Right.** 27.6k tokens. The run used existing suites (no PR test). |
| #1799 | NO GO (3 Major) | GO WITH NOTES | 0 defects; Major 1 true as a test gap (K3); **Major 3 pointed at the real contract finding** but did not measure it | the 422 schema mismatch itself (measured here), K6/K7 survivors (Info), docs 84 | **False NO GO, with one useful Major.** 21.8k tokens. Non-vacuous: 22 red at base. |

---

## ITEM 1: #1796 (KS-1458 items 1, 2, 4), Seat K 13th

Files:
- `routes/users.ts` (+3 / -2, one hunk);
- `ks1006-...test.ts` (header + import);
- `scripts/typecheck-tests/baseline-auth.txt` (-1);
- the two docs html files (section 97).

| check | result | instrument |
|---|---|---|
| users.ts is comment-only | **yes.** `git diff -U0`, filtered to changed lines that do not start with `//`: **0 lines** | `out/diff1796.patch` |
| The test file changes only the header comment and the import | **yes.** The only non-` *` changed lines are the import pair | same |
| TS1192 is gone, with no new tsc errors (test exclude cleared, in my own copy `tsconfig.gate9.json`) | base **42** errors (TS1192 = 1) → head **41** (TS1192 = 0). The normalised error multiset differs by **exactly the one TS1192 line**: 0 added, 0 other removed. The build config `tsc -p tsconfig.json` is rc 0 on both sides. | `out/tsc_tests2_{wb1796,w1796}.txt` |
| Ratchet | **rc 0 at head** ("41 errors: 41 in the baseline, 0 new; 0 stale"). rc 0 at base too (42 / 42). Head code against the base baseline: rc 1 with exactly 1 stale entry (the TS1192), as the author describes. | `out/ratchet2_*.txt` |
| baseline loses exactly one line, by `check.cjs --update` | **Reproduced.** I copied the base baseline to scratch and ran head's `check.cjs --update --baseline <copy>`: rc 0, "baseline lowered to 41 errors in 26 entries (1 stale entry dropped); examined-test-files 105 -> 105". The result is **byte-identical** to the head's committed file. | `out/ratchet2_update1796.txt` |
| users.ts sentence vs `mfa.ts:352-376` | **Matches.** `:352-363`: a password account passes on `verifyPassword` alone ("its password is enough"); a supplied wrong TOTP still fails. `:364-376`: no password means `totpOk \|\| backupOk` is required, and `totpOk` needs `user.mfaSecret`, which this state lacks, so only a backup code remains ("one with none can use neither route"). The route is mounted at `/api/auth/mfa` (`index.ts:114`), path `/disable` (`mfa.ts:313`). | read at head |
| Header sentence vs `userRepo.ts:172-189` | **Matches.** `:174` null or empty → undefined; `:179-181` subject-DEK ciphertext with no DEK → undefined; `:186-188` decrypt throw → undefined (also `?? undefined` at `:183` / `:185`). The read path is `mapRow` `:233`, through `getUserById` at `users.ts:1164`. | read at head |
| The namespace import still exercises the mocks | **yes.** The factory returns `{ default: repoMock, __esModule: true, ...repoMock }`, and the POSITIVE cell asserts `updateUserOrThrow` called once (the spies are live, not vacuous). ks1006 is 5/5 on both sides. | read + spark_gate |
| Suite (`--testTimeout=30000`) | wb1796 105 files / **1205 / 0 failed**; w1796 105 / **1205 / 0 failed**; 0 vanished. ks1000 99/99 at head. | `out/suite/` |

Findings:
- **1796-1 (merge-time):** docs carry the provisional **97**; renumber.
- **1796-2 (Info, carried):** item 3 (should such an account have a way to turn MFA off) is a ruling and is not built, as stated.

**Verdict for #1796: GO WITH NOTES** (the docs number only).

---

## ITEM 2: #1798 (KS-1459 item 2), Seat K 13th

One file, `routes/users.ts` +14 / -8:
- the import gains `VERIFICATION_LEVEL_ORDER`;
- the 5-level literal becomes `const LEVEL_ORDER: readonly string[] = VERIFICATION_LEVEL_ORDER;`;
- two comments are rewritten.

### Lists

| list | elements |
|---|---|
| OLD (base `users.ts`) | BASIC, STANDARD, ENHANCED, HIGH, GOVERNMENT |
| NEW = auth `types/index.ts:26` | NONE, BASIC, SOCIAL, STANDARD, ENHANCED, HIGH, GOVERNMENT |
| shared `packages/shared/src/verification/policy-engine.ts:22` | NONE, BASIC, SOCIAL, STANDARD, ENHANCED, HIGH, GOVERNMENT |

- **auth == shared: element-identical, same order** (parsed from source by `gatework9/tt1798.js`).
- The six comparison lines (`indexOf` x4, `targetIndex <= currentIndex`, `targetIndex !== -1 && currentIndex > targetIndex`) are **byte-identical** base vs head.
- Nothing in services/auth mutates `VERIFICATION_LEVEL_ORDER` (grep for push / splice / sort / reverse / fill / index-assign: 0 hits).

### My truth table (old list vs new list, each site's code exactly as written; `out/truthtable1798.txt`)

- **Values:** the 7 levels, plus `PLATINUM` (unknown) and `standard` (lowercase), for both current and target: 81 pairs per site, 162 rows.
- **Submit site** (`users.ts:1389-1392`): no case-folding, `targetIndex <= currentIndex` refuses.
- **Review site** (`:1494-1497`): both sides upper-cased, refuse iff `targetIndex !== -1 && currentIndex > targetIndex`.

**Result: 162 rows, 142 identical, 20 differing, and 0 differing where the target is zod-admitted (STANDARD, ENHANCED, HIGH, GOVERNMENT).** This reproduces the author's figures exactly.

All 20 differing rows (A = allow / approve, R = refuse):

| site | current | target | old | new |
|---|---|---|---|---|
| submit | NONE | SOCIAL | R | A |
| submit | BASIC | SOCIAL | R | A |
| submit | SOCIAL | BASIC | A | R |
| submit | PLATINUM | NONE | R | A |
| submit | PLATINUM | SOCIAL | R | A |
| submit | standard | NONE | R | A |
| submit | standard | SOCIAL | R | A |
| review | BASIC | NONE | A | R |
| review | SOCIAL | NONE | A | R |
| review | SOCIAL | BASIC | A | R |
| review | STANDARD | NONE | A | R |
| review | STANDARD | SOCIAL | A | R |
| review | ENHANCED | NONE | A | R |
| review | ENHANCED | SOCIAL | A | R |
| review | HIGH | NONE | A | R |
| review | HIGH | SOCIAL | A | R |
| review | GOVERNMENT | NONE | A | R |
| review | GOVERNMENT | SOCIAL | A | R |
| review | standard | NONE | A | R |
| review | standard | SOCIAL | A | R |

Every target is NONE, SOCIAL or BASIC. Full 9 × 9 matrices for both sites are in `out/truthtable1798.txt`.

**Why the submit route cannot write those targets:**
- the zod enum at `users.ts:160`, `['STANDARD','ENHANCED','HIGH','GOVERNMENT']`, parses the body first (`:1386`);
- `saveVerificationRequest` (`:1251`) is the **only** writer of `verification_upgrade_requests` in the repo (`git grep`: users.ts only; the schema files are DDL);
- its four call sites are submit (`:1426`, zod-typed) and three re-saves of a looked-up request (`:1508`, `:1549`, `:1574`, spreading `...request`);
- its `ON CONFLICT (id) DO UPDATE` sets status / reviewed_at / reviewed_by / rejection_reason only, **never `target_level`**.

So a NONE / SOCIAL / BASIC target can only come from a row written outside the service. Every review-site change in that case is toward **refusing** a downgrade-direction approve, which is the KS-1236 intent.

### Other checks

- spark_gate (existing route suites): 14/14 on both sides.
- Suite: wb1798 105 / **1205 / 0 failed**; w1798 105 / **1205 / 0**; 0 vanished. Matches the author's 1205/1205.
- `tsc -p tsconfig.json --noEmit` rc 0 at head (the `readonly string[]` binding compiles); ratchet rc 0 (42 / 42 / 0 / 0).

Findings (all Info or ticket):
- **1798-1 (Info):** `LEVEL_ORDER` aliases a **mutable** exported array. `readonly` protects only users.ts's view. Nothing mutates it today (grep).
- **1798-2 (ticket, carried):** the "use the shared one" half stays open. The shared root does not export the order, so the auth copy at `types/index.ts:26` and `policy-engine.ts:22` remain two copies (identical today).
- **1798-3 (Info, pre-existing, both sides):** the submit site does not case-fold. A stored lowercase level (`standard`) ranks -1, so its holder may request STANDARD again (A/A in the matrix). This PR does not change it.

**Verdict for #1798: GO WITH NOTES** (all notes non-blocking).

---

## ITEM 3: #1797 (KS-1219), Seat R 6th: a RULED behaviour change

- `oauth.ts` +10 (a 3-line comment and a 7-line guard in `resolveAuthorizeClient`, before `parseScopeString`).
- The new test (6 cells, the real `oauthRouter` on a loopback listener, services mocked).
- Docs (84).
- **First line:** I could not read the PR body (gh unauthenticated). The commit subject says "authorize refuses a non-string scope with 400 (JSON null, 0, false too)". The commit body and the Linear READY comment both open with **"Behaviour change:"**.

### Attack rows: the real authorize route, base (bd6697e0) vs head (0b3cac50)

**Method.**
- My probe (`gatework9/quarantine/gate9-probe-1797.test.ts`) reuses the PR's own mock set, but mounts **production's parsers**: `express.json({limit:'10mb'})` and `express.urlencoded({extended:true})`, as `index.ts:85-86`. Express 4.22.2, with qs extended parsing on both query and form.
- Each row records: status, `error.message` / `description`, Location, the consent page's scope list, whether `createAuthorizationCode` was called and with what scope, and a leak regex over the body (`split|TypeError|stack|/src/|.ts:|parseScopeString|node_modules|...`).
- Raw data: `out/probe1797_{wb1797,w1797}.json`; table: `out/attack1797.txt`.

GET (query string):

| row | payload | base | head |
|---|---|---|---|
| G1 | `?scope=openid&scope=profile` (array) | **500** server_error | **400** invalid_request ("scope must be a single space- or comma-separated string") |
| G6 | `?scope[]=openid` (array, bracket form) | **500** | **400** |
| G2 | `?scope[0][0]=openid` (**nested array**) | **500** | **400** |
| G3 | `?scope[a]=openid` (**object**) | **500** | **400** |
| G4 | `?scope=` (**empty string**) | 200 consent [openid profile] (allow-list default) | **same** (unchanged: `''` is a string; KS-822 F-4 "absent" semantics) |
| G5 | `?scope=` + 6.3 KB string | 200 consent, `openid` listed **900 times** | **same** (see 1797-3) |
| GC | **CONTROL** `?scope=openid%20profile` | 200 consent [openid profile] | **200, same** |

POST JSON, deny (`action: 'deny'`) and approve (valid credentials). Cells read deny / approve:

| row | scope | base deny / approve | head deny / approve |
|---|---|---|---|
| A1 | `['openid','profile']` (array) | 500 / 500 | **400 / 400**, minted 0 |
| A2 | `[['openid'],['profile']]` (**nested array**) | 500 / 500 | **400 / 400**, minted 0 |
| A3 | **`null`** | 302 access_denied / **302 with a code, minted [openid profile]** (allow-list default) | **400 / 400**, minted 0 |
| A4 | **`0`** | 302 / **302 with a code, minted [openid profile]** | **400 / 400**, minted 0 |
| A5 | **`false`** | 302 / **302 with a code, minted [openid profile]** | **400 / 400**, minted 0 |
| A6 | `{a:'openid'}` (**object**) | 500 / 500 | **400 / 400** |
| A7 | `''` (**empty string**) | 302 / 302, minted [openid profile] | **same** |
| A8 | **very long string** (~2.6 MB, 200,000 tokens) | 302 / 302, **minted a scope of 200,000 entries** (openid x100000, profile x100000) | **same** (see 1797-3) |
| A9 | `true` | 500 / 500 | **400 / 400** |
| A10 | `1` | 500 / 500 | **400 / 400** |
| A11 | `[]` | 500 / 500 | **400 / 400** |
| C0 | **CONTROL** `'openid profile'` | 302 access_denied / 302 with a code, minted [openid profile] | **same** |

POST form (urlencoded, extended), approve:

| row | payload | base | head |
|---|---|---|---|
| F1 | `scope=openid&scope=profile` | 500 | **400**, minted 0 |
| F2 | `scope[a]=openid` | 500 | **400**, minted 0 |
| FC | **CONTROL** `scope=openid+profile` | 302 with a code [openid profile] | **same** |

- **The controls pass on all three carriers.** Every non-string scope is 400 at head, and on approve **nothing is minted**: the guard runs inside the resolver, before any credential check or mint.
- **No refusal leaks internals.** Every head refusal is the identical 148-byte body `{"success":false,"error":{"code":"BAD_REQUEST","message":"invalid_request","description":"scope must be a single space- or comma-separated string"}}`. The base's 500s were the generic `server_error` body, with no leak either. The leak regex fired only on the 200 HTML consent page (identical 5,662 bytes on both sides), which is a success page, not a refusal.

**Siblings (head only, `out/sib1797_w1797.json`; the ticket's "any other non-string authorize parameter"):**

| param | result at head |
|---|---|
| `response_type` repeated | 400 unsupported_response_type |
| `redirect_uri` repeated (GET), or an array (POST) | 400 invalid_redirect_uri |
| `client_id` repeated | 400 invalid_client |
| **`state` repeated (GET)** | **500 server_error** |
| **`code_challenge` repeated (GET)** | **500 server_error** |
| `state` as a JSON object on deny | 302 `...&state=%5Bobject+Object%5D` |

None of these leaks.

### Tests

- spark_gate: 6/0 at head, 3/3 at base (R1 to R3 red), as claimed.
- Suite (`--testTimeout=30000`): wb1797 105 / **1200 / 0 failed**; w1797 106 / **1206 / 0 failed**; 0 vanished. The author's "2 failed" were ks949 at the 5 s default; they did not recur at 30 s.
- tsc build rc 0; ratchet rc 0 (42 / 42; 106 test files examined, floor 105).

### Findings

| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1797-1 | Low (test gap, disclosed by the author) | The JSON `null` / `0` / `false` edge, the half of the ruled change that **closes a widening** (base approve minted the full allow-list for `scope:false`), has no cell in the PR. Lifting A3a / A5a (approve, minted 0) into the file would pin it. | TESTED, rows A3 to A5 (Spark Major 1 agrees as a gap). |
| 1797-2 | Low (ticket scope, not this PR) | **Repeated `state` or `code_challenge` on GET still answers 500**, and an object `state` is reflected as `[object Object]`. KS-1219's recommendation names "any other non-string authorize parameter". The PR covers `scope` only, so KS-1219 should stay open for the rest, or get a sibling ticket. | TESTED, sibling probe. |
| 1797-3 | Low (pre-existing, both sides) | `validateScopes` (`services/oauth.ts:352-355`) filters but neither deduplicates nor bounds. A 2.6 MB scope string minted a code carrying 200,000 scope entries, and the GET consent page lists `openid` 900 times for a 6.3 KB query. The 10 MB JSON limit is the only bound. Suggest dedupe + a length cap in the resolver. | TESTED, A8 / G5. |
| 1797-4 | Info | The empty string still means "absent → allow-list default" (G4, A7), while `null` / `0` / `false` now refuse. That is consistent with KS-822 F-4's no-scope semantics, but it is a seam worth one sentence in the docs. | TESTED. |
| 1797-5 | merge-time | Docs carry **84** / 84.1-84.3, colliding with develop and with #1799. Renumber. | grep. |

**Verdict for #1797: GO WITH NOTES.**

---

## ITEM 4: #1799 (KS-1467 services/auth half), Seat R 6th

Files:
- `errorHandler.ts` +1 / -1: `Object.setPrototypeOf(this, new.target.prototype)` at `:25`;
- `passwordLoginGate.ts` comment-only: the 2 changed lines both start with `//` (`:287-288`);
- the new test (Spark's 34 cells + R's N1);
- docs (84).

### Subclass enumeration: every class the handler maps (`out/subclass1799.txt`)

`errorHandler.ts` declares AppError plus **19 subclasses**:
- 13 direct: BadRequest, Unauthorized, Forbidden, NotFound, Conflict, Validation, TooManyRequests, ServiceUnavailable, MfaRequired, SocialSignInRefused, OAuthStateInvalid, OAuthProvider, SocialEmailUnavailable;
- two-level via UnauthorizedError: InvalidCredentials, TokenExpired, InvalidToken;
- two-level via ForbiddenError: EmailNotVerified, AccountSuspended, InsufficientVerification.

No other `extends <X>Error` of these exists in services/auth: `IssuerCertError extends Error` is unrelated, and the grep used `-P` after a `\b` false zero under `-E`. The **only `instanceof <AppError family>` sites in services/auth product code are `errorHandler.ts:290` (`AppError`) and `:296` (`ValidationError`).** There are no `constructor.name` or `getPrototypeOf` checks. So the instanceof fix can change behaviour only at `:296`.

My probe (`quarantine/gate9-probe-1799.test.ts`) imports the real module and runs on a real express app with the real `errorHandler`, base bd6697e0 vs head e14baaa3:

| class | `instanceof` own class base → head | `instanceof` intermediate parent base → head | `getPrototypeOf === Class.prototype` base → head | status / code (same both sides) |
|---|---|---|---|---|
| AppError | true → true | n/a | true → true | 418 TEAPOT (custom) |
| BadRequestError | **false → true** | n/a | false → true | 400 BAD_REQUEST |
| UnauthorizedError | **false → true** | n/a | false → true | 401 UNAUTHORIZED |
| ForbiddenError | **false → true** | n/a | false → true | 403 FORBIDDEN |
| NotFoundError | **false → true** | n/a | false → true | 404 NOT_FOUND |
| ConflictError | **false → true** | n/a | false → true | 409 CONFLICT |
| ValidationError | **false → true** | n/a | false → true | 422 VALIDATION_ERROR |
| TooManyRequestsError | **false → true** | n/a | false → true | 429 RATE_LIMIT_EXCEEDED |
| ServiceUnavailableError | **false → true** | n/a | false → true | 503 SERVICE_UNAVAILABLE |
| InvalidCredentialsError | **false → true** | Unauthorized **false → true** | false → true | 401 UNAUTHORIZED |
| TokenExpiredError | **false → true** | Unauthorized **false → true** | false → true | 401 UNAUTHORIZED |
| InvalidTokenError | **false → true** | Unauthorized **false → true** | false → true | 401 UNAUTHORIZED |
| MfaRequiredError | **false → true** | n/a | false → true | 403 MFA_REQUIRED |
| SocialSignInRefusedError | **false → true** | n/a | false → true | 403 SOCIAL_SIGN_IN_REFUSED |
| OAuthStateInvalidError | **false → true** | n/a | false → true | 403 OAUTH_STATE_INVALID |
| OAuthProviderError | **false → true** | n/a | false → true | 400 OAUTH_PROVIDER_ERROR |
| SocialEmailUnavailableError | **false → true** | n/a | false → true | 403 SOCIAL_EMAIL_UNAVAILABLE |
| EmailNotVerifiedError | **false → true** | Forbidden **false → true** | false → true | 403 FORBIDDEN |
| AccountSuspendedError | **false → true** | Forbidden **false → true** | false → true | 403 FORBIDDEN |
| InsufficientVerificationError | **false → true** | Forbidden **false → true** | false → true | 403 FORBIDDEN |

- On both sides: `instanceof AppError` and `instanceof Error` are true, and `name` is `'Error'`. statusCode, code and message are unchanged for every class.
- The PR's own P1 / P2 cover 9 of the 19 subclasses, and P3 one two-level class; this table covers all 19.

### Response shapes, base vs head (real express + the real handler; full bodies in `out/subclass1799.txt`)

- **The same bytes on both sides** for all 22 rows that are not a ValidationError with truthy details. That is every class above, plus ValidationError with no details / `null` / `0` (no `details` key on either side).
- **Differs (the intended change only):**
  - `ValidationError('Password is too weak', {feedback:[...]})`: base `{"code":"VALIDATION_ERROR","message":"Password is too weak"}` → head adds `"details":{"feedback":[...]}`.
  - `ValidationError('x', {})`: head adds `"details":{}` (truthy empty object; no product site throws it).
- **The handler's other branches answer identically on both sides:**

  | branch | status | body |
  |---|---|---|
  | malformed JSON (`entity.parse.failed`) | 400 | INVALID_JSON |
  | ZodError | 400 | VALIDATION_ERROR with the ZodIssue array |
  | plain Error carrying `password=hunter2 at /src/x.ts:1` | 500 | generic (no echo) |
  | TypeError | 500 | generic |
  | **a non-AppError with `statusCode: 503`** | **500** | generic (the look-alike is not promoted) |
  | a thrown string | 500 | generic |

- **The product throw sites with details** (`git grep "new ValidationError("`):
  - `auth.ts:204` (register) and `:822` (reset): `{feedback}`;
  - `users.ts:993` (change-password): `{feedback}`;
  - `auth.ts:173`: **no details**, so it is unchanged.
  - This is exactly what the PR body claims.

**Through the real change-password route** (`quarantine/gate9-route-1799.test.ts`, the ks1407 harness: the real route, userRepo, password service and handler):

| candidate | base | head |
|---|---|---|
| `aaaaaaaaaaaaaaaaaaaa` | 422, no details | 422, details.feedback = 5 fixed strings |
| `zqkvnxyplmwtrdfgh` | 422, no details | 422, details.feedback = 4 fixed strings |
| `qwertyzqkvnx<script>` | 422, no details | 422, details.feedback = 4 fixed strings |
| `Zk9Q` | 400 (zod min 8; never reaches the strength check) | same |
| `P4ssword-Secret-hunter2` | 200 | 200 |

**No candidate appears in any body, on either side.** At source (`password.ts:171-213`) every feedback string is a literal; only `minLength` is interpolated (`:171`).

### N1, and mutants (`gatework9/mut1799.py`; PR file 35 cells + my route probe; `out/mut1799/`)

My runner launched vitest from outside services/auth, so the PR's S1 and S2 (which `readFileSync(process.cwd()/src/...)`) are red in **every** row, K0 included (Info, 1799-3). The table counts the other 33.

| mutant | PR file, excluding S1 / S2 | route probe echo | read |
|---|---|---|---|
| K0 head | 33 / 0 | none | baseline |
| K1 `checkPasswordStrength` pushes the password (the author's mutant) | **N1 RED** | **echo in 3 of 5 rows** | killed by both |
| K2 partial echo: the first 4 chars in feedback | **N1 RED** (via the `'Zk9Q'` candidate, whose 4-char prefix is the whole thing) | none (my candidates are 8+ chars) | killed by N1 |
| **K3 route echo: `users.ts:993` details carry `data.newPassword`** | **33 / 0, SURVIVES** | **echo in 3 of 5 rows** | the PR file cannot see a route-site echo; see 1799-2 |
| K4 base line (`AppError.prototype`) | **21 red** (P1 x9, P2 x9, P3, H1, N1) | none | the fix is pinned |
| K5 no `setPrototypeOf` at all | 33 / 0 | none | **equivalent** (native ES2022 class semantics); the new line is correct and harmless |
| K6 handler drops `&& err.details` | 33 / 0, survives | none | equivalent on the wire, except `details: null` would appear for `ValidationError('x', null)`; no product site does that |
| K7 handler sends details for ANY AppError that has one | 33 / 0, survives | none | equivalent today: no other subclass carries `details` |

**N1 really fails on an echo** (K1, K2). It cannot fail on an echo added at a route site (K3); only a route-level cell can.

### Tests

- spark_gate: 35/0 at head, 13 pass / 22 fail at base, as claimed.
- Suite (`--testTimeout=30000`): wb1797 105 / **1200 / 0**; w1799 106 / **1235 / 0**; 0 vanished. Matches the author.
- tsc build rc 0; ratchet rc 0.

### Findings

| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| **1799-1** | **Medium (published contract; the ticket asked for this check first)** | The published 422 for register (`auth.openapi.ts:747`) and reset (`:815`) is `commonErrorResponses[422]` → `ValidationErrorResponseSchema` (`packages/shared/src/openapi/responses.ts:84-110`). It declares `error.details` as an optional **array of `{code, path, message}`** ("the ZodIssue array"). At head these 422s send `details` as an **object**, `{feedback: string[]}`. Before the PR there was no `details`, which conformed. The spec never mentions `feedback` (0 hits). Change-password's spec lists weak password under **400** (`:1012`), though the route answers 422 on both sides (pre-existing drift). Schemathesis (`api-contract-tests.yml`, `--checks all` incl. response_schema_conformance) is `workflow_dispatch` only, so **this does not block a PR today**, but its `full` tier would flag it. KS-1467's own recommendation: "decide deliberately that 422 responses now carry `details` (a visible response change; check the published 422 shape first)". The PR body (as far as the commit message shows) and the Linear comment do not mention the schema. **Fix:** give the three ops a 422 schema whose `details` is `{feedback: string[]}` (and correct change-password's 400 to 422), in this PR or as a ticket. **Wednesday rules:** I did not make it a NO GO, because the visible change itself is ruled and nothing enforces conformance today. | FOUND by read (Spark Major 3 pointed here); wire shape TESTED (route probe). Conformance run NOT TESTED. |
| 1799-2 | Low (test gap) | No route-level cell. N1 composes the helper, class and handler, so an echo added at a throw site (K3, `users.ts:993` `{..., attempted: data.newPassword}`) **survives the PR's 35 cells**. My route probe (the ks1407 harness, 5 candidates) kills it. Optional: lift that one route cell into the file. | TESTED, mutant K3 (Spark Major 1 agrees). |
| 1799-3 | Info | S1 / S2 locate `passwordLoginGate.ts` via `process.cwd()`, so they go red when vitest starts outside services/auth (measured: 33 / 2 at the unmutated head). `import.meta.url` / `__dirname` would make them location-proof. | TESTED (Spark Minor agrees). |
| 1799-4 | Info | K5 shows `setPrototypeOf` is now redundant (ES2022 classes); K6 and K7 survive as equivalents today. Neither is a defect. | TESTED. |
| 1799-5 | merge-time | Docs carry **84** / 84.1-84.3, colliding with develop and with #1797. Renumber. | grep. |
| 1799-6 | Info (carried) | The `packages/shared` half is PR #1775 (KS-1467 comment 06:22Z). The shared handler serves 12 services and is out of this PR. | Linear read. |

**Verdict for #1799: GO WITH NOTES**, with 1799-1 for Wednesday to rule: this PR, or a ticket.

---

## Harness finding for Wednesday (affects every services/auth gate since at least gate 5)

**`services/auth` has its own lockfile-pinned `node_modules`.** The lockfile has `services/auth/node_modules/@types/node` = **20.19.43**, against the root's 26.1.0, plus `ioredis`, `jsonwebtoken` and others, and the shared tree has that directory. Gate 7's recorded layout symlinked `services/auth/node_modules` to the **Dev root**, which hides it.

Measured here, with that layout:
- the ratchet is **rc 1 on both base and head**, with 2 phantom "new" errors: `jwks.test.ts` TS2694 (`crypto.JsonWebKey`) and `ks820-821...` TS2345 (`NonSharedBuffer`), both @types/node 26 artefacts;
- tsc with the tests included sees 44 / 43 errors, against 42 / 41 with the faithful layout.

With `services/auth/node_modules` → the shared tree's `services/auth/node_modules`:
- the ratchet is **rc 0** on both sides;
- **`ks1000 ... REAL: services/auth against the committed baseline passes` passes (99/99)**. That is the cell gate 7 recorded as "environmental" on both sides; this is very likely its cause.

spark_gate's `--node-modules` takes one directory and links it only into the package dir, so its typecheck-sensitive arms would carry the same distortion. Its runtime cells were unaffected here. Recommend: link the service-local directory when it exists, and the Dev root above it.

## Method

- **Copied from gate 7:**
  - clone at a fresh path, with the toplevel assertion;
  - read-only node_modules symlinks (corrected as above);
  - Spark half first: spark_gate with base = develop, then spark_review on facts minus the docs html, with HARNESS LIMIT lines, one request at a time;
  - my own worktrees, mutants rewritten from `git show HEAD:` and restored, and `git status` read back clean;
  - full suites on both sides, compared by failing (file, title) plus vanished cells;
  - merge-tree; pins at start and end.
- **The whole auth suite ran with `--testTimeout=30000` for every before/after comparison** (the ks949 tree-walk flake at about 5 s, KS-1053 / KS-1155). At 30 s, **0 failures in all 8 suite runs**, so ks949 did not flake.
- **#1796:** tsc with the exclude cleared, in a copy `tsconfig.gate9.json` (`compilerOptions.noEmit`, `exclude: [node_modules, dist]`), with the error multiset diffed after path normalisation. Ratchet at base and head, plus a replay of `--update` into a scratch copy of the base baseline.
- **#1798:** my own truth table, from lists parsed out of the three source files at the head and the base (`gatework9/tt1798.js`), plus a writer census of `verification_upgrade_requests`.
- **#1797:** a production-parser HTTP probe on all three carriers, base vs head, with mint tracking and a leak regex. Plus a sibling-parameter probe at head.
- **#1799:** a whole-family enumeration on a real express app with the real handler, base vs head; a real-route weak-password probe; 8 mutants against the PR file and the route probe.
- **K pair:** two-order merge simulation (scratch commits in my clone), then tsc, ratchet and the full suite on the merged tree.
- **Drivers** (all under `/private/tmp/claude-501/gatework9/`): `env.sh`, `run_sg.sh`, `run_rev.sh`, `prep_facts.py` (from gate 7), `linear_read.py` (from gate 7), `tt1798.js`, `mut1799.py`, `run_suites.py`, `cmp_suites.py`, plus probes in `quarantine/`.

## NOT TESTED

- **General:**
  - PR bodies (`gh` unauthenticated);
  - Node 24 LTS;
  - a real database, Redis, a running stack, the gateway (CSRF / XSRF on authorize POST), Docker, CI, the pre-push hook, ESLint, `audit:gate`, `audit:locks`;
  - the four platform suites;
  - the suites of develop cc262c1 (it moved mid-gate; no code overlap).
- **#1796:** item 3 (a ruling); the real `decryptMfaSecret` fault paths (read only).
- **#1798:** item 1 (the non-atomic approve) and item 3, both out of scope; a row written outside the service with a NONE / SOCIAL / BASIC target (reasoned from the writer census, not driven).
- **#1797:**
  - a real `getAppByClientId`, so the repeated `client_id` was not meaningful under the mock;
  - the NUL guard (`rejectNulBytes`, not mounted in my probe);
  - the consent page's rendering of duplicate scopes beyond counting them;
  - the stored size of the 200,000-entry code in Postgres.
- **#1799:**
  - register and reset weak-password over HTTP (change-password only; the two auth.ts sites were read, and they build the same object);
  - an actual Schemathesis conformance run (1799-1 is read, not run);
  - whether the front end shows `details`;
  - the `packages/shared` half (#1775) and the 12 services that mount it.

## Evidence locations

- **Run outputs:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate9-tier1/out/`
  - `p1796/` `p1797/` `p1798/` `p1799/`: facts, `facts_spark.json`, diff, `spark/review.json`, raw attempt, `pr_body_from_commit.txt`
  - `sg*.log`, `sg_rc.txt`, `rev_rc.txt`, `harness_*.txt`
  - `truthtable1798.txt`
  - `probe1797_{wb1797,w1797}.json`, `attack1797.txt`, `sib1797_w1797.json`
  - `gate9-probe-1799_{wb1797,w1799}.json`, `gate9-route-1799_*.json`, `subclass1799.txt`, `mut1799/`, `mut1799.json`
  - `tsc_tests2_*.txt`, `tsc_build*.txt`, `ratchet2_*.txt`, `ratchet_*.txt` (the first-layout runs are kept as `tsc_tests_*.txt` / `ratchet_head1796.txt` / `ratchet_base1796.txt`)
  - `suite/` (8 json), `suite_compare.txt`, `suite_rc.txt`
  - `mergetree.txt`, `diff179{6,7,8,9}.patch`, `msg179{6,7,8,9}.txt`
  - `ticket_KS-{1458,1219,1459,1467}.txt`
  - `pins_start.txt`, `pins_end.txt`, `load.txt`
- **Scratch:** `/private/tmp/claude-501/gatework9/` (drivers, worktrees, and `quarantine/` with every probe and test copy) and `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fccaae68-37b3-43d1-9466-4e52087c3d4f/scratchpad/gate9/` (spark_gate work dirs `sg1796` to `sg1799`).
