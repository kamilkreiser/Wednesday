PR 2132: GO WITH NOTES; PR 2127: GO WITH NOTES

| PR | head | verdict |
|---|---|---|
| 2132 (KS-1473, round 1, Seat G 31st) | ba0ab4f453497257e9848c16f884ae8900a2f195 | GO WITH NOTES |
| 2127 (KS-785, round 2 of 2, Seat R 91st) | 7dc6ff72cf61de04bb65a0e859cf670e9ff0ac85 | GO WITH NOTES |

Gate 288, tier 1 (Opus, claude-opus-5-5). Findings only. Nothing was fixed, pushed, posted or mailed. Neither verdict needs a Kam ruling.

## Pins (git ls-remote origin, through the repo's own deploy key, from my clone)
- Start 17:56:27 AEDT (06:56:27Z): develop e8d23ce366e2, PR 2132 ba0ab4f45349, PR 2127 7dc6ff72cf61, PR 2052 b61674e7b763. All four equal the commission's pins.
- End 18:14:57 AEDT (07:14:57Z): all four identical. **Nothing moved.**
- Develop's move. `git diff --name-only 204e62ac..e8d23ce3` covers KS-2055 and KS-2120: transfer index.ts, transferAccess.ts, one transfer test, and 4 fragments. It shares 0 paths with PR 2132's 7. `4d6b7bb1..e8d23ce3` adds KS-2109: AGENT-DOCUMENT-OPERATION-RULES.md, api-gateway utils/trustHeaders.ts (a comment), and its 2 fragments. It shares 0 paths with PR 2127's 5. Control: the same `comm` over PR 2127 against itself finds 5. Neither PR is touched by the move. I ran all of PR 2132's runtime tests on develop e8d23ce3 plus the PR's 7 files, which is the merge result.

---

## PR 2132 (KS-1473): GO WITH NOTES

**BLUF.** The change does what Kam's card row A9 option 2 says and nothing else. It removes two CSRF exclusion entries and one portal row, edits the pinning test lists as Wednesday ruled, adds a new test file and adds fragments. I reproduced the premise at runtime with the seat's harness and with an independent probe. Before the change, a cookie-only POST to every spelling of either path was exempt and proxied upstream; now it is refused 403 CSRF_TOKEN_MISSING. No legitimate caller exists anywhere in the repo. Non-cookie, Bearer and x-api-key clients, and a browser doing the double submit, are unaffected (measured). Suite: 5 red on develop, exactly the declared ones; 8/8 at head; 1,886/1,886 for the whole api-gateway suite at head. The seat's mutants and two of my own redden the named cells. The tsc and eslint deltas are zero. docs-fragments is OK, and a planted defect fails it. The notes are disclosure-level only.

### FOUND / TESTED / HOW
- **A1, the change.** csrf.ts at head (read whole). The exclusions that remain are `/health`; `/api/auth/{login,register,refresh,logout,wallet/challenge,wallet/authenticate}`; `/api/verification/verify`, `/api/verification/verify-file` and their v2 twins; `/api/logs`; `/webhooks/`. For each verify, verify-file and logs exclusion I found live consumers by grep: frontend/verifier VerifyPage.tsx and ResultPage.tsx, the outlook add-in, the gmail add-on, connectors/flutter-verify-app, and issuer logger.ts (sendBeacon). The auth and webhook entries carry their own rationale (H21) and I did not re-litigate them. **Nothing is newly exempt.** The diff only removes entries, and the matching function is unchanged. Is the request newly refused because the KS-1461 `/`-boundary rule keeps `/api/verification/verify` from covering `verify-batch`? Yes: my mutant MD below proves the boundary is what holds it.
  - **Callers of verify-batch at develop.** `git grep -i 'verify-batch|verifyBatch|verify_batch'` over the whole tree: in code, only csrf.ts:115/:119, developer-portal.html:294, and the MCP server's own root `/verify-batch` (http-server.ts:161, its openapi files, two of its tests); in docs, MCP Deployment/{README,openapi.yaml,chatgpt-actions,troubleshooting}.md and KS-1410/1868/1901 fragments, all about the MCP route. There are **zero** hits in frontend/, sdk/, connectors/, mobile/, packages/ and the systemTest tree. Positive control: the same grep for `verify-file` finds 5+ files.
  - **The MCP route.** The MCP server's `/verify-batch` loops `verifyDocument()` per item. It never calls the gateway's verify-batch, and the gateway's exclusions do not apply to it.
  - **Runtime (independent probe, my own vitest file on the real app, NODE_ENV=development, one recording upstream, develop vs head):**
    - no-cookie POST: 200 and proxied, on both
    - Bearer + cookie: 200 and proxied, on both
    - x-api-key + cookie: 200 and proxied, on both
    - cookie + a valid double-submit token taken from the gateway's own `X-CSRF-Token`: 200 and proxied, on both
  - **So no non-browser client loses access, and nobody real loses access.** Only an ambient-cookie POST without a token changes, and nothing serves the path.
- **A2, the premise. TRUE.**
  - The gateway proxies `/api/verification` and `/api/v2/verification` to originate (proxy.ts:680-686). Originate's verificationRouter and verificationV2Router register only `/verify`, `/verify-file`, `/hash` and `/status/:documentId` (an enumeration of every `Router.(post|get|use…)` call). No spec carries the path.
  - Develop, cookie-only POST to each of these: `/api/verification/verify-batch`, `/api/v2/…`, `/api/v1/…`, `/Api/Verification/Verify-Batch`, `/api/v1/v2/…`, the sub-path `…/verify-batch/x`, and the absolute-form target. Each gave **200, proxied upstream** (exempt).
  - Head: each gave **403 CSRF_TOKEN_MISSING, 0 upstream hits**.
  - Cookie with an evil Origin: develop 200 proxied, head 403 CSRF_ORIGIN_INVALID.
  - Controls on both trees: `/api/verification/verify` 200 (still exempt), `/api/documents` 403.
  - The seat's harness on develop: N1, N2, N3a and N3b fail with "expected [Array(n)] to deeply equal []", so they were exempt. P1 fails on the body containing `verify-batch`.
- **A3, the suite.** Three test files on develop + the new file: 63 cells, **58 pass, exactly N1, N2, N3a, N3b, P1 fail**. C1, C2 and COMPLETENESS are green. At head: **61/61** (55→53 in the KS-1461/1469 files, plus 8). Whole api-gateway suite at head: **169 files, 1,886/1,886, 0 skipped**, which matches the READY.
  - Seat's mutants, reproduced (each planted alone, restored, sha256 csrf.ts 8d236fd38273030e and portal 35ff4200956c4e6e equal before and after):
    - MA (v1 entry back) → N1, N3a red
    - MB (v2 entry back) → N2, N3b red
    - MC (develop's portal page) → P1 red
  - **My mutants:**
    - MD, isExcludedPath back to bare `startsWith` (the pre-KS-1461 rule) → N1, N2, N3a, N3b red. So the new cells also pin the boundary.
    - ME, drop the `/api/v1` strip in the exclusion check → 8/8 green. This is expected: the mutant only narrows exemptions, and KS-1469's own cells own that property.
  - **Lost coverage? None.** The removed KS-1461 cell and KS-1469 O2 cell asserted only that verify-batch was exempt, which is no longer true. The same loops still generate the identical cells for every remaining entry. The relabelled KS-1469 m1 cell still pins v2 verify and verify-file, and C1 duplicates that. The property the m1 label's history was about (no cell pinned the v2 verify-batch entry) is now pinned the other way by N2/N3b.
- **A4, the gates.**
  - `tsc -p tsconfig.test.json`: 25 errors on develop and 25 at head. The lists are identical after path normalisation, and none is in a touched file. Planted type error in the new file: 26.
  - Plain `tsconfig.json` (excludes tests): 0 and 0.
  - eslint (ESLint API, cwd = Blockchain/Dev, on csrf.ts and the 3 test files): 0 errors on both trees. The only warning is csrf.ts's pre-existing unused `error` (line 227→229). A planted unused const gives a new warning.
  - docs-fragments `check` at the PR head (sparse checkout): rc 0, OK, with 2 ADVISORY lines. Planted defect (`<!--n-->` removed from the KS-1473 flow h2) → rc 1 naming the file. Restored → rc 0.
- **Rulings the READY cites.** 05:24:39Z ≈ `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-09_G31_addendum_ks1473.md` (send.out 16:24:43 AEDT; an ADDENDUM, not an `_answer_` file). It scopes "the KS-1469 cells that pin the two entries". 05:26:34Z ≈ `2026-11-09_G31_answer_ks1461_line.md` (send.out 16:26:38 AEDT). It widens scope to the KS-1461 file. Kam's card `secuura-backlog-31-decisions-1109` = a (ruled 13:44:42 AEDT), row 9 option 2, covers "delete the page row and both CSRF exemptions". The test-list edits are Wednesday's rulings and follow from it. They are not wider in effect than the card.
- **PR body (seat's draft `drafts/pr_body_ks1473.md`; the posted text was not read, no API).** I checked each factual sentence against my measurements: 7 files, +195/-8; 1,880−2+8 = 1,886; 55→53; cheat 19 and flow 12 lines; the grep scope; "none is known". All true. Fragment text: also true at head.

### Findings
- **G288-2132-1, NOTE. An undisclosed but strictly tighter edge: sub-paths.** At develop the KS-1461 boundary rule exempted `…/verify-batch/<anything>` too (measured: `/api/verification/verify-batch/x` was 200 and proxied). At head it gets 403. The PR body, fragment and comments speak of "every spelling" (case, alias, trailing slash) but not sub-paths. No cell pins sub-paths. Nothing serves them, so nothing is lost.
- **G288-2132-2, NOTE. The test-file comments cite different authorities.** The KS-1469 file comment cites Kam's card. The KS-1461 file comment cites "Wednesday's ANSWER 05:26:34Z". The PR body attributes both edits to Wednesday's rulings (05:24:39Z and 05:26:34Z). All three are true, since the card authorises the change and Wednesday authorised the test-list scope. A client reader sees two different attributions for the same kind of edit.
- **G288-2132-3, NOTE, Wednesday's records.** `2026-11-09_G31_addendum_ks1473.md` and `…_answer_ks1461_line.md` both have mtime 16:36:14 AEDT. That is after their send.out files (16:24:43 and 16:26:38). The staged copies may have been touched after sending. I did not compare them with the mailed text.

### NOT TESTED (PR 2132)
A live stack, the edge (Caddy, nginx), Node 24 (host Node v26.8.1), demo and kintsugi, the four platform suites, eslint over the whole of `src` (I ran the touched files only), the posted PR body and ticket comment c2731144 (no API read), and the portal's other rows.

---

## PR 2127 (KS-785), round 2: GO WITH NOTES

**BLUF.** The round-2 shape closes every gate-283 blocker and major on my own reproduction:
- **G283-1:** a .env made from the real env.example reaches compose. Head rc 97; round 1 rc 127, compose not reached.
- **G283-2:** a malformed value reaches compose with 0 FXSECRET printed.
- **G283-3:** `bash -x` traces 0 values (control: round 1 traces 4).
- **G283-4:** no other export changes.

Real Compose v5.5.0 (render only) confirms that the grep's `export` widening is correct for `export KEY=`, `export  KEY=` and `export<TAB>KEY=`. The grep is **not** exactly the set of lines bash and Compose read. Leading whitespace is read by both and missed by the grep, so the KS-785 disagreement survives for that shape. A few contrived shapes are over-matched, which creates a disagreement develop did not have. None stops the start or prints a value. The checker is comment-only (proven, both controls). The merge trees with PR 2052 (both orders) and with PR 2132 (both orders) are clean, with both edits present. The suite is 46/46 with all 32 develop labels kept, and every seat mutant reddens its named cells. The notes below are residue for a follow-up ticket, not a third round.

### B1. Gate 283 findings at the new head
| id | status | evidence (mine) |
|---|---|---|
| G283-1 BLOCKER | **CLOSED** | Real start-environment.sh and the real head checker, with stubs only for docker/npm/curl/open/sleep, under `env -i`. The .env is env.example with both passwords filled (line 236 `ISSUER_NAME=Secuura Platform` present) and the shell exports both passwords. **Head: checker PERCLONE, compose (real `docker compose config`) gets rot_pg_A1/rot_rd_A1, rc 97 (reached).** Round 1: rc 127, NOT-REACHED. Develop: rc 97, compose gets the SHELL values. |
| G283-2 MAJOR | **CLOSED**, with residue in G288-2127-2 | `REDIS_PASSWORD=FXSECRETfirst FXSECRETtail`: head rc 97, FXSECRET in output 0. Round 1 rc 127. The .env at mode 000: head and develop alike (UNREADABLE warning, start reaches compose). |
| G283-3 MINOR | **CLOSED** | Head under `bash -x` with FXSECRET values in .env: 0 occurrences. The trace shows only `grep -Eq '^(export[[:space:]]+)?KEY=' <path>` and `unset KEY`. Positive control: round 1 under -x prints FXSECRET 4 times. |
| G283-4 MINOR | **CLOSED** for every other export, by construction (the loop names 2 keys) and by the seat's cell, which I reddened with an all-keys mutant | The two checked keys now also leave the **npm children**, not only compose: see G288-2127-3. |
| G283-5 test gap | **CHANGED** | The `set -a` and `|| true` holes are moot (there is no source). A new hole: the export widening is unpinned (G288-2127-4). |
| G283-6 NOTE | **CHANGED** | The comment is rewritten. It is mostly true, but "on either path compose gets the value this script reports, or is not reached" is false for the shapes in G288-2127-1 and -2. |
| G283-7 NOTE | **CLOSED** | Wednesday ratified OVL_IGNORE_PRS for this push (fix-round answer). The merge trees below are clean. |
| G283-K (cell) | holds | My unconditional-unset mutant reddens exactly G283-K. |
| KEYS (cell) | holds | My only-POSTGRES mutant and the seat's all-keys mutant both redden KEYS. The checker reads exactly 2 keys (lines 170-171 at head; the commission's 171-172 is off by one). |

### B2. The shape: grep vs bash (the checker) vs Compose
Instrument: `/private/tmp/g288/tools/fxrun.sh`. It builds a fresh fixture tree with the real head or develop start-environment.sh and the real head checker. Its docker stub runs the REAL `docker compose config --format json` on a two-variable fixture compose file, using `${POSTGRES_PASSWORD:-DEFAULT_pg}`, the real file's form (docker-compose.yml:134, :224), and exits 97. The shell exports SHELL_pg and SHELL_rd. "Checker" is what the checker's own subshell source resolves.

| .env line (PG only; REDIS plain) | grep | head: checker / compose | develop: checker / compose |
|---|---|---|---|
| `export POSTGRES_PASSWORD=v` | 1 | v / v (agree) | v / SHELL |
| `export  POSTGRES_PASSWORD=v` (2 spaces) | 1 | v / v | v / SHELL |
| `export<TAB>POSTGRES_PASSWORD=v` | 1 | v / v | v / SHELL |
| `  POSTGRES_PASSWORD=v` (leading spaces) | **0** | **v / SHELL (disagree)** | v / SHELL |
| `<TAB>POSTGRES_PASSWORD=v` | **0** | **v / SHELL (disagree)** | v / SHELL |
| `"POSTGRES_PASSWORD"=v` | 0 | SHELL / Compose refuses the file ("unexpected character") | same |
| `# POSTGRES_PASSWORD=v`, `#POSTGRES_PASSWORD=v` | 0 | SHELL / SHELL | SHELL / SHELL |
| `POSTGRES_PASSWORD=` (no value) | 1 | BLANK / DEFAULT (agree, loud) | BLANK / SHELL |
| `POSTGRES_PASSWORD` (bare) and `export POSTGRES_PASSWORD` | 0 | SHELL / SHELL | SHELL / SHELL |
| CRLF `POSTGRES_PASSWORD=v\r` | 1 | per-clone / v (unset happens) | — |
| `POSTGRES_PASSWORD = v`, `POSTGRES_PASSWORD: v` | 0 | SHELL / SHELL (no export: BLANK / v, pre-existing parser gap) | SHELL / SHELL |
| `'v'` single-quoted, `v # comment` | 1 | v / v | v / SHELL |
| a multi-line quoted value with an inner line starting `POSTGRES_PASSWORD=` | **1** | **SHELL / DEFAULT (disagree; develop agreed)** | SHELL / SHELL |
| `export POSTGRES_PASSWORD=a REDIS_PASSWORD=b` (one line) | 1 for PG only | a,b / `a REDIS_PASSWORD=b`, SHELL_rd | pre-existing parser gap |
| `REDIS_PASSWORD=x y` (malformed) | 1 | **SHELL_rd / `x y` (disagree; develop agreed)** | SHELL / SHELL |

- **Can the grep or the unset print or trace a secret?** No. `grep -Eq` with stderr discarded prints nothing. The -x trace carries only the pattern, the path and the key name (measured with a positive control, above).
- **Does any other export behave differently from develop?** No. A stub npm records the env: NODE_ENV=test reaches the children on both trees. But the two checked keys are now absent for the npm children too (G288-2127-3).

### B3. Checker comment-only: PROVEN
- Instrument `/private/tmp/g288/tools/strip.sh` (drops whole-line comments and blank lines, keeps the shebang): **135 lines, byte-identical** develop vs head (cmp rc 0). Dropping only comment lines and keeping blanks gives 153 lines, also identical. The seat's 154 is not reconciled, as at gate 283.
- Controls: a planted code line differs (rc 1). A planted comment line does not (rc 0). The `-U0` diff has 0 non-comment +/- lines.
- Truth of the rewritten comments (head 108-119):
  - "start-local.sh sources .env before compose": true (set -e :16, `source .env` :103, compose :136).
  - "an exported value is overwritten" and "under its set -e a .env line bash cannot run would stop it": true by mechanism.
  - "start-environment.sh unsets the shell export of each key this script resolves wherever .env assigns it": true except for the shapes in G288-2127-1 and -2. The same holds for "On either path compose gets the value this script reports, or is not reached".
  - The paragraph at 121-126 ("start-environment.sh … never sources .env at all") is develop's text and is true again.

### B4. Overlap
In a scratchpad clone (see Conduct), `merge-tree --write-tree` on develop e8d23ce3:
- 2127 alone: rc 0, tree 0f47b705
- 2052 alone: rc 0, tree 8b5c46d5
- 2132 alone: rc 0, tree 3a0fd0d3
- 2127 then 2052, and 2052 then 2127: both rc 0, the **same tree 6f3dac0e**
- In that merged checker, PR 2052's line-12 text is present (1 hit) and PR 2127's new sentence is present (1 hit; control: develop has 0)
- 2127 then 2132, and 2132 then 2127: both rc 0, the same tree 5afeae50
- Path intersection 2127 vs 2132: 0 (control: 2127 vs itself, 5)

### B5. Suite and mutants
Run in a git work tree (sparse checkout at the PR head), because the R2-1 sweep cells need `git rev-parse`. In a plain archive tree those 2 non-KS-785 cells read NO-TREE, which is an artefact of my first tree.
- **Head: 46/46. Develop's suite on develop's scripts: 32/32. All 32 develop labels are present at head** (`comm` gives 0 missing).
- Seat's mutants, each swapped into the checkout, restored, and sha256 2386ef1cdad525de equal at the end (`git status` clean):
  - develop's start-environment.sh → 6 red: the 3 KS-785 cells, G283-1, G283-K, KEYS
  - round 1's (source) → 5 red: G283-1, -2, -3, -4, KEYS
  - unset every .env key → G283-4 and KEYS red
  - unconditional unset → G283-K red
  - These match the READY's lists exactly.
- **My mutants:**
  - only POSTGRES_PASSWORD in the loop → 6 red, including KEYS
  - `^KEY=` without the export alternative → **46/46 green**
  - `^(export )?` with a single space only → **46/46 green**
  - allow leading whitespace → 46/46 green (expected: no cell has that shape)
  - one non-informative mutant, my error: I appended an unset after `compose up` but left the block in place, so 46/46 says nothing

### Findings
- **G288-2127-1, MINOR. The KS-785 disagreement survives for an indented .env line.** At start-environment.sh:143 (head), `grep -Eq "^(export[[:space:]]+)?${_ks785_key}="` is anchored at column 0. Bash (the checker's source) and Compose v5.5.0 (measured: with no export, compose reads `  POSTGRES_PASSWORD=v` and `<TAB>POSTGRES_PASSWORD=v` as v) both accept leading whitespace. With an exported shell value, the head start path prints "per-clone" for v while compose gets the shell value. That is the ticket's defect, for this shape. A `^[[:space:]]*` prefix would close it; it is not a requested fix. No cell covers indented lines.
- **G288-2127-2, MINOR. The grep over-matches lines that bash does not treat as an assignment of that key, which creates a disagreement develop did not have.** Shapes: a malformed value `REDIS_PASSWORD=x y` (bash runs `y` with a temporary assignment, so the checker keeps the shell's SHELL_rd and prints per-clone, while compose gets `x y`); an inner line of a multi-line quoted value; the second key of `export A=… B=…`. In each, develop gave compose and the checker the same (shell) value; head gives them different ones. The start still reaches compose and prints nothing. The G283-2 cell asserts only rc and the FXSECRET count, not agreement, so it cannot see this. The first shape is the realistic one, because it is the template's own class of line (env.example 236/404 are not password lines).
- **G288-2127-3, NOTE, disclosure. The unset also removes the two passwords from the npm children,** not only from compose. Measured with a stub npm: develop children get POSTGRES_PASSWORD and REDIS_PASSWORD = the shell values; head children get them `<unset>`, and NODE_ENV is unchanged. Consumers: `packages/shared/src/cache/redis.ts:34` (`process.env.REDIS_PASSWORD`) and `services/tenant-provisioning/src/index.ts:40`. The services' `dotenv.config()` reads their own cwd .env, not Blockchain/Dev/.env. For an operator who exports the passwords, the services now behave as on the no-export path. Whether that fails Redis AUTH on a live stack is UNMEASURED. The READY, the fragments and the comment say "every OTHER export reaches compose and the npm children as before". That is true, but the change to these two keys for the children is not stated.
- **G288-2127-4, MINOR, test gap. The declared `export` widening is unpinned.** Removing the `(export[[:space:]]+)?` alternative, or narrowing it to one space, leaves 46/46 green. Real Compose reads all three export forms (measured), so the widening is correct, but no cell would catch its loss.
- **G288-2127-5, NOTE. The comment at check-slot-credentials.sh:115-116 (head) overstates** ("On either path compose gets the value this script reports, or is not reached"). It is false for the shapes in -1 and -2. This is the same class as G283-6, narrower than before.
- **G288-2127-6, NOTE. The commission cites the checker's lines 171-172; the reads are at 170-171 at head.** This is not the seat's error.

**Instances closed at this head:** G283-1, G283-2 (as specified), G283-3, G283-4 (other exports), G283-7. **Residue to ticket:** G288-2127-1, -2, -4 and -5, and the -3 disclosure, plus the seat's own named follow-ups (env.example 236/404; whether start-local.sh dies on the template, which is still UNMEASURED by me too).

### NOT TESTED (PR 2127)
A real stack or `docker compose up`, a real .env (fixtures only), and start-local.sh executed. ks1355_slot_blind_launchers (78) and check-stack-safety.sh were not re-run by me. Also not tested: shellcheck, the full preflight, the posted PR body and ticket comment 970911f3 (no API read), the GitHub `mergeable_state: unstable` the seat saw, and live consequences of -3.

---

## Both: paths covered only by a skipped hook leg (3, 4, 8)
None.
- Legs 3, 4 and 8 (preflight.sh header: spec-auth conformance, spec-path resolvability, served-spec json/yaml agreement) probe OpenAPI paths against a live gateway. verify-batch is in no gateway spec (A2), and no spec, route or served-spec file is touched by either PR.
- PR 2132's CSRF and portal behaviour is pinned by the vitest suite.
- PR 2127 touches only shell scripts, a shell suite and fragments.

## Conduct
- Clone: `/private/tmp/g288/repo` (blobless; remote and core.sshCommand from the Blockchain checkout's config, read-only). Fetches only there.
- Trees, all extracted with `git archive`:
  - `/private/tmp/g288/dev`: develop, plus the new test file for the red run
  - `/private/tmp/g288/h2132`: develop plus PR 2132's 7 files, hash-checked against the PR blobs
  - `/private/tmp/g288/t2127`
  - fixtures and tools under `/private/tmp/g288/{fx,tools,out}`
- **Size at end: 912M. Nothing removed (no rm).** Stale node_modules farms were moved aside as `*.q_stale_main`.
- **Deviation 1, disclosed.** The workspace hook (pretooluse_no_cd.sh) refuses git write verbs (worktree, merge-tree) on any path outside WEDNESDAY, including /private/tmp/g288. For merge-tree, commit-tree, sparse checkout and the git-tree-dependent suite and docs runs, I used a second clone in this session's scratchpad: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/8d5e0559-4701-4028-a222-6edcfedb0d3e/scratchpad/g288clone` (12M; objects through GIT_ALTERNATE_OBJECT_DIRECTORIES pointing at my /private/tmp clone). That is where the hook directs. It holds 3 local merge commits I made (commit-tree), never pushed.
- **Deviation 2, disclosed.** node_modules came in as symlink farms: first to the main checkout's (zod 3.25, which proved stale), then to Seat G 31st's worktree `worktrees/s-g31-ks1473/Blockchain/Dev/{,services/api-gateway/,packages/shared/}node_modules`, read through symlinks only. `@secuura` was copied with relative links so workspace packages resolve into my tree. I built packages/shared/dist in my own tree. vitest and vite caches landed in my real dirs, not the targets. **One possible write outside my tree:** a stopped `diff -rq` that I launched did traverse symlinked node_modules (read-only). I know of no writes there.
- Nothing was run in any /Volumes/DevMASTER/!CODING checkout: no git verb other than ls-remote-equivalent reads (`remote -v`, `config --get`, failed `worktree list` refused by the hook), no fetch, no write. No real .env or credential file was opened, sourced or grepped. All .env files are synthetic, or copies of the committed env.example. No container was started (`docker compose config` only). Network use: git clone, fetch and ls-remote only.
- Load: load1 10.77 at my start, before any work of mine. The peak was 14.05 during my clone, on a shared host; afterwards 3.6 to 7.1. Vitest and tsc runs were `nice`d and serial. Above 8 at the start and the early peak.
- df DevMASTER: 103 GiB free at start, 99 GiB at end. I wrote only this verdict on DevMASTER, so the drop is other seats.
