# gate79 KIT REPORT — drafter to Wednesday

- **Target:** #1437 (KS-1402, Seat K 1st + K 2nd). Head `b4933a457f38fe12551839545431bba000e928fc`, tree `64d5bf0c31a3`. It has ONE parent, `81d2e5f4c415`, which is the PR's base and NOT develop. Develop at draft is `349b35c9163ac59209366adb7a4a89d8779bd6d6`.
- **The change:** 8 files, +852/-289. Originate now resolves a transfer-custody holder email itself, with one bound `$queryRaw` on `users.email_lookup_hash` and the request tenant in the WHERE. Auth is unchanged.
- **Drafted:** 2026-10-09T05:27Z–06:00Z by one Wednesday drafting subagent, shaped on the gate78 kit.
- **Built, not launched.** Nothing was merged, pushed, commented, mailed, ticketed or routed. No tmux and no cockpit. `inbox_routing.conf` is untouched (exact line count 0; control: 178 agentmail lines in the file).
- **Writes:**
  - This folder. `_scratch/` is gitignored and holds the kit clone, three SIM commits in that clone's own object store, arm fixtures and the raw KS-1402 comment bodies.
  - The session scratchpad `/private/tmp/claude-501/…/scratchpad/gate79/`: a second clone, worktree `wtHead`, the npm install, the cells / tamper / probe evidence, and the copies of the tools.
  - Nothing under `!CODING` was created or written; only git read verbs were run against the shared checkout.
  - Post-run reads confirm it:
    - `find -newer` over the K 1st and K 2nd record folders: 0 files.
    - `ls !CODING`: 0 `gate79` entries (control: 16 entries).
    - Reports dir: 0 `gate79` entries (control: 9 `gate7x`).
    - Shared store `.git/worktrees`: 0 of mine.
- **Every drafter figure below is a PREDICTION** (files in `predictions/`). The gate re-measures each one.

## 0. Bottom line

- **Kit complete.** Every self-test is green, and each has planted arms that FAIL:
  - c1 21/21, c2 17/17, c3 8/8, c4 5/5, gh 14/14.
  - **Red arms on REAL data: 14/14 MATCH.** Repin arms 27/27 MATCH. Launcher arms 30/30 MATCH.
  - **Tool-fix arms (c4): 17/17 as predicted** (0 bad).
  - **Tamper matrix: 12/12 rows MATCH the READY**, plus a HEAD row and a CONTROL row, both all green.
- **Dry run rc 0** at the final pins (`dry_run_console_final.txt`, 05:57:29Z–05:58:29Z). It ran AFTER the repin arms, which re-render the prompt with a SIM develop. Develop was read by `ls-remote` inside it: `349b35c9163a`, UNMOVED.
- **The builder's numbers that the kit re-measured HELD:**
  - BASE reds are C1 C2 C9; HEAD is 11/11.
  - ks739 goes 0/17 → 17/17; ks697 reads 16/17 with the base file against the head route.
  - 12/12 tamper rows.
  - 8 files +852/-289; auth unchanged; the hoist is a pure move; the act gate is first; the SQL is bound.
  - The three tool fixes each fail and pass as claimed.
- **Things the drafter found for the gate to RULE** (§3): the tenantless caller binds the DEFAULT tenant (D-1); RLS vs the NULL-tenant tolerance (D-2); Q-LEGACY is real at base (D-3); the commit subject and the PR title differ (D-4); CI was NOT RUN at the head (D-9); a class sibling in `certifications.ts` (D-8).
  - None is ruled a blocker by the drafter. D-1 and D-2 are the ones most likely to matter.
- **Model:** the exec line carries no `--model` (fleet convention). The prompt's MODEL-LINE says Opus 5.5 and that Wednesday switches it; the launcher refuses rc 33 without it.

**Launch command (Wednesday runs it; the drafter did NOT).** Add the routing line first, then run from a real terminal:
```
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-09_gate79/repin_and_launch_gate79.sh --pr 1437 --head b4933a457f38fe12551839545431bba000e928fc --branch feature/ks-1402-originate-resolves-holder-email-itself-k2-1 --base 81d2e5f4c4151f5291a7a9c186d93a02dc5d38d6 --parents-n 1 --end-tree 64d5bf0c31a371a968ec13474f3cdaf6b42541e9 --develop 349b35c9163ac59209366adb7a4a89d8779bd6d6
```
- **A moved head refuses rc 11** (`--head` != kit, or origin pull/head or branch != `--head`). Re-draft; never re-gate a stale pin.
- **A moved develop refuses rc 10** and prints the exact `--repin-develop <sha>`.
  - It refuses rc 13 instead if the advance touches any PR path outside the known docs / yaml overlap, or any of the 24 tooling / code-surface paths (c1 P10 / P12).
- **After the pane is up:** type `/model claude-opus-5-5` at the gate's prompt.

**Pins re-verified** (`ls-remote` with the checkout's own sshCommand, GIT_SSH_COMMAND unset):

| reading (UTC) | develop | pull/1437/head | branch |
|---|---|---|---|
| 05:23:02Z (the READY) | 349b35c9163a | b4933a457f38 | b4933a457f38 |
| 05:27:17Z (drafter, manual) | 349b35c9163a | b4933a457f38 | b4933a457f38 |
| 05:51:31Z (dry run 1) and 05:57:29Z (final dry run) | 349b35c9163a | b4933a457f38 | b4933a457f38 |

The API read (`gh_gate79.py api`, also inside the dry runs):
- open, unmerged, base develop, not draft;
- **mergeable false, `dirty`**;
- 1 commit, +852/-289, 8 files;
- title `KS 1402: originate resolves a transfer-custody holder email itself` (66);
- body sha256/16 `e7b9f5fb82820914` (7,635 chars, 7,688 B).

READY sha256/16 is `004d76879c35f8a5`.

## 1. What I carried from gate78, and what I changed

**Carried (the shape):**
- From `lib`: read-verb-only `git()` (GIT_SSH_COMMAND now always stripped), `wgit` with the `!CODING` refusal, `blob` by `ls-tree`, `req` (every pin a REQUIRED argument), the GitHub / Linear readers with tokens read by name, and `Tally`.
- c1 P1–P12 (re-keyed).
- The whole gh `actions` classifier, **verbatim**: by-path comparators, the log fetched without the auth header, the signature, the planted develop-only rule.
- The launcher: pin hashing (rc 30/31), head file (rc 7), prompt guards (rc 8/33/39/25), the TTY rule (rc 21), the override rule (rc 16), the moved-kit rule (rc 2).
- The repin flow: READY → one ls-remote → API + census → develop → kit clone + c1 → render → routing → `--check`.
- The prompt structure, MERGE ADDENDUM, REPORT-HASH-LAST, verdict format and mail.

**Dropped:** the lock / registry / legs / reach / suites machinery (`c2_locks`, `c3_registry`, `c5_legs`, `c6_reach`) and the lock-refresh checks. #1437 touches no lock.

**Built new for THIS change:**
- **c1:**
  - 8 paths, with exactly one `create mode`.
  - P7 is `len <= 92` AS DECLARED, with no `(#n)` arithmetic (STANDING_LINES :320-:322).
  - P8-FIXPREFIX counts the conventional `fix(KS-1402)` form.
  - P10 covers 24 tooling / code-surface paths, including auth's `users.ts` and `userRepo.ts`.
  - P11 requires 0 auth paths.
  - **P12 allows base..develop to touch only the known docs / yaml overlap**; anything else fails.
- **c2_code `claims`:** the commit's code claims, measured on CODE-ONLY text (comments blanked, strings and templates kept) beside the raw count.
  - D0: only 3 lines are added and 1 removed outside the handler.
  - D1: the pure-move instrument.
  - D2: the order chain.
  - D3: the bound tagged template, the unsafe-call census, and parity of the predicate text with the id path.
  - D4: the retired subjects, scoped to the HANDLER.
  - D5: schema and normalisation parity with auth.
  - D6: message bytes.
  - D7–D11: printed readings (tenantless caller, Q-LEGACY, RLS, the KS 739 titles, the patch sha).
  - **My first D4 was originate-wide and FAILED on two strings that live in OTHER routes** (`certifications.ts`). D4 was re-scoped to the handler, and the whole-src counts are printed as D4-CLASS; that output became finding D-8.
- **c3_cells:**
  - `setup` makes the worktree, runs npm ci and builds shared (dist asserted).
  - `cells` plants the route and tests from either revision, asserts each plant landed, runs jest per file and restores by sha.
  - `tamper` runs the 12 READY rows, re-implemented from their names, with block-scoped anchors (the predicate text occurs twice in the handler).
  - `probe` runs five fact-only cells appended to a COPY of the ks1402 file (P-a1 tenantless caller, P-a2 binder, P-c bytes + headers, P-d normalisation variants, P-e key absent) and quarantines the copy after.
  - **My first T5 failed to LOAD** (TS6133, unused `normalisedHolderEmail`). The tool read it TAMPER-INVALID, not red. The run is quarantined and the edit fixed.
- **c4_tools:** the three tool fixes plus pushk2.sh, run as copies in scratch. Red and pass arms, two predecessor controls, and the (59,0) re-derivation over the logs.
  - **My first run's namecheck red arms asserted only an rc.** It was re-run asserting the reason line, and is quarantined.
- **gh:**
  - `census` splits OVERLAP-CODE from OVERLAP-DOCS.
  - `prtext` checks title vs subject, the fix-prefix form, and the "14 rows" claim.
  - `linear` compares the ticket with the READY's comment state.
  - **`actions` now prints NOT RUN AT HEAD.** My first run read rc 0 on a head with only a skipped dependabot run: a green that measured nothing. It is quarantined.
- **Launcher:** the new keyword set (43), the load-failure and CODE-ONLY rule strings (rc 33), and the builder's worktree `worktrees/s-k1-ks1402` in the holds (rc 39).

## 2. Drafter predictions at head b4933a457f38 / base 81d2e5f4c415 / develop 349b35c9163a: BUILDER'S CLAIM vs DRAFTER'S READING

| Check | Instrument → file | Builder's claim | Drafter's reading |
|---|---|---|---|
| C1 | c1 → `c1_real.out` | 8 files +852/-289, 1 commit, 0 trailers | **13/13 PASS.** <br>• 8 paths exact; tree 64d5bf0c31a3. <br>• Trailers 0 content bytes; control bf277eead268 reads 53. <br>• 0 Co-Authored-By; subject 71 chars, only KS-1402 hyphenated. <br>• One `create mode`. <br>• 24 tooling paths identical at base / head / develop; 0 auth paths. <br>• base..develop has 6 paths, 2 shared (both docs). <br>• INFO: `fix(KS-1402)` form present. |
| 1 code | c2 claims → `c2_claims.out` | act gate first; pure move; bound; auth unchanged; 400 body byte-identical | **18/18 PASS.** <br>• D0: +3 / -1 outside the handler, exactly the expected lines. <br>• D1: 161 vs 161 lines identical, hoist 1/1/1 at both revisions. <br>• D2: order holds and the act gate returns 403 next. <br>• D3: interpolations [holderEmailHash, tenantId]; 0 unsafe in the block. Originate-wide `$queryRawUnsafe(` 9→9 and `$executeRawUnsafe(` 14→14, beside tagged `$queryRaw` 138→139. The predicate occurs 2× in the handler. <br>• D4: 8/8 retired subjects go base>0 → head 0 in the handler. <br>• D5: schema identical ×3; normalisation identical. <br>• D6: both messages 1→1. |
| 2 cells | c3 cells → `c3_cells_route*_tests*.out` | BASE C1 C2 C9 red; HEAD 11/11; ks739 0/17→17/17; ks697 16/17→17/17 | **All four held.** <br>• (route base, tests head): reds C1 C2 C9; ks739 0/17; ks697 17/17. <br>• (head, head): 11/11, 17/17, 17/17. <br>• (head, base tests): ks697 16/17 (`an unknown email is still 404 RECIPIENT_NOT_FOUND` red); ks739 1/25. <br>• Every plant landed and was restored by sha. |
| 3 tamper | c3 tamper → `c3_tamper.out` | 12 rows; T1+T7 one per conjunct; no all-green row | **12/12 MATCH**; HEAD and CTRL all green; porcelain clean after. |
| 4a | probe P-a1 / P-a2 → `c3_probe.out` | (the gate's question) | getReqTenantId returns `tid \|\| DEFAULT_TENANT_ID`, so the email read **never binds NULL; it binds `a0000000-…0001`**. In the mocked harness a tenantless CONNECTOR and a tenantless ISSUER_ADMIN both **resolve (201) the default-tenant user and the NULL-tenant user**, and 404 a tenant-A user. P-a2: the multi-tenancy binder `createPoolProxy` passes `undefined` as `$2`, and pg's `prepareValue(undefined)` is `null`. |
| 4c | P-c | byte-equal 404 | body equal, and every header except `date` equal (content-length 153, same etag) |
| 4d | P-d | `' Foo@X.com '` resolves | 7/8 variants (tab/CRLF, NBSP, BOM, U+2028, upper case) normalise and hash identically to auth's flow and resolve. `foo@x.com​` is refused 400 by both schemas. |
| 4e | P-e + C9 | key absent → 502 | email path 502 BAD_GATEWAY; id path 201 (unaffected); malformed still 400 |
| 4g | c2 D8 | Q-LEGACY unmeasured | **The fallback is real at base:** /lookup → getUserByEmail (users.ts:300) → on a hash miss, `auth_find_user_by_email_legacy` (userRepo.ts:591; migration 039:191, `LOWER(email) = $1 AND email NOT LIKE 'v_:%'`). Population UNMEASURED. |
| 4h | c4 → `c4_tools.out` | three fixes | **17/17 arms OK.** <br>• All 5 copy hashes equal the READY's. <br>• gatelines: real log rc 0 MATCHES (59,0); reds rc 1 ×3; NA rc 3; unreadable rc 2; the predecessor rc 0 while printing MISMATCH. <br>• pathgate: PASS real; FAIL ×4; the predecessor false-FAILs (PR0 7 files). <br>• namecheck: pass with 24/24 controls; red on `-g5-` ("POSITIVE CONTROL FIRED") and on `-e2-` forms ("BLIND on" all 4). <br>• pushk2 order OK; console `gatelinesk2 rc=0` / `RESULT: pushed, and the gate MATCHES`. <br>• **G-PIN: 44 `*-push.out` logs dated 10-06..09 → 42 (59,0) and 2 with the block absent.** The READY says 22 logs: a different corpus, so the gate rules it. |
| 5 PR text | gh prtext → `gh_prtext.out` | — | T1–T3, T5 pass; **T4: the title `KS 1402: …` (66) ≠ the commit subject `fix(KS-1402): …` (71)**; T5b 1 attribution line; T6 **"14 rows" vs 13** MISMATCH (the READY self-corrects); ks1402 11/11, ks739 17/17, ks697 17/17 OK. rc 1. |
| 5 ticket | gh linear → `gh_linear.out` | 5 comments, newest 7740c258, updatedAt 02:07:01Z | In Progress, not archived; 5 comments, newest 7740c258 (UNCHANGED). **updatedAt moved to 05:22:42.999Z**, the exact createdAt of the PR attachment c18b9579 (the integration linking #1437). 0 comments link #1437 yet (Wednesday's batch). |
| 6 Actions | gh actions → `gh_actions.out` | — | **NOT RUN AT HEAD:** security-scan / pr-security-gates / pr-platform-suites. Only a skipped dependabot run exists. A `dirty` PR has no merge ref. Develop's own push runs of the two PR workflows: failure. rc 1. |
| census | gh census → `gh_census.out` | the 8 docs overlaps | 29 others: **0 OVERLAP-CODE, 8 OVERLAP-DOCS** (#1383, #1429 (+yaml), #1430–#1434, #1436), exactly the READY's list. |

## 3. Candidate findings the drafter measured (each for the gate to rule; the drafter rules none)

- **D-1 Tenantless caller (attack a).**
  - `${tenantId}::uuid` cannot bind NULL through `getReqTenantId`, which falls back to `DEFAULT_TENANT_ID`.
  - A request with no tenant therefore resolves DEFAULT-tenant and NULL-tenant users (P-a1, mocked db). At base the auth path skipped its tenant compare for a tenantless caller, so it is narrower now, but not closed.
  - Whether such a request reaches originate in production depends on `MULTI_TENANCY_ENABLED` and `extractTenantContext`'s fallback (index.ts:218-222). The drafter did not read tenant-context.ts's fallback rule.
  - This is the READY's own "KS 1406 class not addressed", now on originate's side.
- **D-2 RLS vs the NULL-tenant tolerance (attack b / j).** Migration 039 (KS-458):
  - puts `users` under fail-closed tenant_isolation;
  - BACKFILLED NULL `users.tenant_id` to the default tenant ("NULL rows are invisible to EVERY tenant under fail-closed");
  - gives auth SECURITY DEFINER lookups (`users_auth_lookup` USING true).

  Consequences:
  - Originate reads as its own role under the request GUC, so C7's "NULL-tenant holder resolves" may describe only the mock (which has no RLS).
  - The comment at documents.ts:1756 ("tenant RLS has been inert before now (KS-160)") sits beside :1812 ("`users` is FORCE RLS fail-closed").
  - Open PR #1383 (KS-1401, "migration 049 restores tenant isolation where 039 is already …") is in the census.
  - UNMEASURED: there is no database.
- **D-3 Q-LEGACY is real at base (attack g).** A plaintext-email user with no hash resolved via auth's legacy function and 404s at head.
  - Also read the B-10 `PII_PLAINTEXT_CUTOFF` (2026-06-01, userRepo.ts:39-91): in production-like envs a plaintext row may THROW rather than resolve after it. The drafter did not trace this.
  - Population UNMEASURED.
- **D-4 Subject vs title.** The commit subject is `fix(KS-1402): …` (71) and the PR title is `KS 1402: …` (66).
  - Whether Linear's integration treats `fix(KS-1402)` as a closing word is UNMEASURED by the kit (Q-FIXPREFIX).
  - The squash subject the merge seat declares should settle it (Q-SUBJECT79).
- **D-5 "14 rows" in the PR body** vs 13 in the matrix file. The READY corrects it itself; Polish.
- **D-6 Attribution line** in the PR body (1). Polish under gate77 Q-ATTR77.
- **D-7 "patch sha256/16 ab8e9e441864e05c"** is UNREPRODUCED by four instruments (`git diff`, `git diff -- non-doc`, `git show --format=`, `--binary`). The instrument is unnamed. Polish or a question.
- **D-8 CLASS SIBLING (report only).** `routes/certifications.ts:238-246` still forwards the CALLER's Authorization to auth `POST /api/users/stub` for `holderEmail`.
  - S's connector carries `certifications:write` but not `users:read` / `users:create`.
  - D4-CLASS prints 5 caller-credential forwards in originate at the head.
  - The gate should census them and recommend a ticket.
- **D-9 CI NOT RUN at the head** (dirty PR). It is owed on the merge seat's merge-in push.
- **D-10 Deploy precondition.** `PII_LOOKUP_HMAC_KEY` must be set in originate, or every email transfer answers 502. The drafter did NOT read any deploy template (UNMEASURED).
- **D-11 G-PIN corpus:** 44 logs (42 at (59,0), 2 with the block absent) vs the READY's 22. An instrument difference, not a defect by itself.
- **D-12 namecheckk2** still adds `" (#NNNN)"` to subject lengths. Superseded by STANDING_LINES 2026-10-07; Polish.
- **Not a defect:** the KS-1402 `updatedAt` move is the PR attachment (same timestamp).

## 4. Kit files and pins

`kit.json` `script_sha256` pins 10 files. The launcher refuses rc 31 on a mismatch and rc 30 on a missing, empty or unpinned file. `kit.json`, `KIT_REPORT.md` and `RULINGS_wednesday.md` (if Wednesday writes one) are not pinned. Re-pin with `python3 _scratch/pin.py` after any edit to a pinned file.

| File | sha256/12 | What |
|---|---|---|
| `lib_gate79.py` | da80359134a5 | helpers + code_only / handler / block |
| `c1_pin_gate79.py` | b3f3e8962cac | C1 P1–P12 |
| `c2_code_gate79.py` | c5db6df0f213 | code claims D0–D11 |
| `c3_cells_gate79.py` | b478103a142d | setup / cells / tamper / probe |
| `c4_tools_gate79.py` | 4c78caa236c1 | the three tool fixes + pushk2 |
| `gh_gate79.py` | 1346aaa0e4bd | api / actions (by path, NOT RUN at head) / census / prtext / linear |
| `probe_block_gate79.ts.txt` | 8d7f2ca5fe29 | the 5 fact-only probe cells |
| `prompt_gate79.txt` | 95b292c6b682 | 56 lines; `{{HEAD}}` ×14, `{{DEVELOP}}` ×2 |
| `launch_qa_secuura_gate79.sh` | 473320c60e68 | launcher, `--check` |
| `repin_and_launch_gate79.sh` | 10ceae4e18fb | launch action, `--dry-run` |

Also in the kit:
- `ROUTING_LINE.txt`;
- `predictions/`, holding every drafter run and `selftest_*.out`;
- `arms/`, holding `arms_red.sh`, `arms_repin.sh`, `arms_launcher.sh`, their `.summary` files and every arm's `.out` / `.rc`;
- `dry_run_console_final.txt` + `dry_<HHMMSS>.*`;
- `_quarantine/`, holding the superseded runs, each named for why. Nothing was deleted.

## 5. Arms

- **Self-tests** (`PYTHONDONTWRITEBYTECODE=1 python3 <script> --selftest`), all rc 0.
  - Planted arms include:
    - a `//` inside a string and a template with `${{}}`;
    - a changed non-block handler line;
    - a changed hoist;
    - a third interpolation;
    - `$queryRawUnsafe`;
    - `+` concatenation;
    - a one-byte message change;
    - a schema without `.trim()`;
    - a suite-load failure;
    - a 2-occurrence and an absent anchor;
    - a `!CODING` write;
    - a planted auth path, a 100755 add, an extra delete;
    - develop touching documents.ts / auth;
    - a hyphenated foreign key;
    - "14 rows";
    - an unread CI log;
    - a change needle.
- **Red arms on REAL data** (`arms/arms_red.summary`), **14/14 MATCH**:
  - c1 real 0 FAIL;
  - c1 wrong end-tree → P4;
  - c1 base = develop → P2;
  - c1 parents-n 2 → P2;
  - c1 no end-tree → rc 2;
  - c1 develop = SIM touching documents.ts → P12;
  - c1 develop = SIM touching auth → P10;
  - c1 clean SIM → 0 FAIL;
  - c2 head = base → D2;
  - c2 head = develop → D4;
  - c2 no base → rc 2;
  - prtext with a planted KS-1406 → T3;
  - prtext `Fixes KS-1402` → T1;
  - the real body → CL-ROWS.
- **Repin arms 27/27 MATCH**, every one a dry run or refused before any launch step:
  - 7 × missing (rc 9);
  - 7 × wrong value, using gate78's values (rc 11);
  - short head (rc 9);
  - `--no-api` on a real launch (rc 9);
  - stale repin (rc 10);
  - head moved / branch moved / both moved (rc 11 ×3);
  - develop not a descendant / touching documents.ts / touching auth (rc 13 ×3);
  - clean SIM develop: no repin (rc 10), stale repin (rc 10), repinned (**rc 0**);
  - `G79_LSFILE` in a real launch (rc 16).
- **Launcher arms 30/30 MATCH:**
  - rendered (0);
  - bad pin (31), no pin (30), missing file (30), tampered probe block (31);
  - unrendered (8), forbidden GO (8);
  - MODEL-LINE / by-path / load-rule removed (33 ×3);
  - `!CODING` hold / builder worktree removed (39 ×2);
  - TENANTLESS-CALLER / Q-LEGACY keyword removed (33 ×2);
  - head file good (0), 8 × wrong (7), wrong develop (8);
  - ls real (0), head moved / branch moved (6 ×2), develop moved (17);
  - moved kit (2);
  - non-TTY launch (21, nothing launched).
- **Order matters:** the repin SIM arm re-renders the prompt and head file with the SIM develop. The final dry run was re-run after it; `head_at_launch.txt` is back to `D 349b35c9…`.

## 6. Routing line needed (NOT added)

Back up `inbox_routing.conf`, then add the line from `ROUTING_LINE.txt`:
```
QA/Secuura-gate79|coagent@agentmail.to|yes
```
A real launch refuses rc 1 until it is present.

## 7. Open questions for Wednesday

Each has the default the kit already assumes. Rule them in `RULINGS_wednesday.md` beside this file; the prompt tells the gate to read it, and to use these defaults if it is absent.

- **Q-SEAT79 (merge seat):** no ANSWER names one.
  - **Default:** `GO (Seat K 3rd): merge 1437 on gate79`.
  - Any other seat means editing `go_string` in kit.json and the GO lines in `prompt_gate79.txt`, then re-pinning with `_scratch/pin.py`. The launcher refuses rc 8 on a mismatch.
- **Q-SUBJECT79 / Q-FIXPREFIX:** the commit subject (`fix(KS-1402): …`, 71) and the PR title (`KS 1402: …`, 66) differ.
  - **Default / rec:** the merge seat declares `KS-1402: originate resolves a transfer-custody holder email itself` (66 as declared, key first, TRUE of the diff, no `fix(` form).
  - The gate rules it and may propose another.
- **Q-DOCSMERGE:** stands. The merge seat does the keep-both of the 2 docs (and the yaml once #1429 lands). It then re-runs ks1402 / ks739 / ks697 and `check:openapi` on the merge result.
- **Q-CI79:** CI was NOT RUN at the head (dirty).
  - **Default:** a GO may stand with "CI owed on the merge-in push, and the merge seat lands only after it classifies".
  - Say if you want CI green before landing instead.
- **Q-TENANT79 (D-1 / D-2):** the drafter offers no ruling. The gate measures, rules severity and says whether it BLOCKS.
  - **Default:** a live / DB measurement is NOT authorised in this gate (no database, no stack).
- **Q-DEPLOYKEY79 (D-10):** **default:** the gate reads deploy templates only (never a real `.env`) and names the precondition. Deploy is out of scope.
- **Q-CLASS79 (D-8):** **default:** report only, with a recommended ticket. Wednesday routes it.
- **Q-MODEL79:** as gate78. The exec line has no `--model`; you type `/model claude-opus-5-5`.
- **Q-DOCKER79:** `docker info` rc 1 at draft (drafter ran it once). The four platform suites are NOT RUN, and the gate does not start Docker.
- **Q-DISCLOSE79 — drafter reads and writes:**
  - GitHub GETs: pulls/1437, the open-PR census, actions runs.
  - A Linear read of KS-1402.
  - Read-only reads of the K 1st / K 2nd records, and copies of their tools run in scratch.
  - Tokens are read by name inside the helper and never printed.
  - Writes: this folder (`_scratch/` gitignored) and the session scratchpad: a clone, a worktree, the npm install, and the jest runs with planted files restored by sha.

## 8. Pane, report and rung 5

- **Pane:** `QA/Secuura-gate79`.
- **Report directory:** `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-09-gate79/`. The gate seat writes it; it is absent at draft.
- **Verdict mail:** FROM coagent@ TO wednesday-agent@, subject `[QA -> Wednesday] GATE79 (T1): #1437 KS-1402 originate resolves holder email`.
- **Rung 5, in the pane:**
  - #1437 / KS-1402 named;
  - the charter being read;
  - head `b4933a457f38`;
  - a `*_gate79.py --selftest`;
  - its own clone under `/private/tmp/claude-501/`, never `worktrees/s-k1-ks1402`;
  - the model switch confirmed.
- **Rung 6:** `NOT-TESTED.written-first.md`.
- **Expected duration:**

  | Step | Time |
  |---|---|
  | setup (npm ci) | ~25 s |
  | shared build | ~10 s |
  | each cells plant | ~10 s |
  | tamper | ~1.5 min |
  | probe | ~10 s |
  | the whole originate suite | ~2 min a side |

  The rest is the seat's own reading, which is heavy for this gate (RLS, tenant-context, Q-LEGACY).

## 9. UNMEASURED by the drafter

- Whether develop or the head moves before launch.
- Anything needing a database: RLS / GUC behaviour, Postgres NULL semantics live, the Q-LEGACY population, real `users` rows.
- Whether a tenantless request reaches originate in production (tenant-context.ts not traced).
- `PII_LOOKUP_HMAC_KEY` in any deployed env.
- Whether Linear treats `fix(KS-1402)` as closing.
- The whole originate suite (the READY's 97 files 1096/1096): not re-run by the drafter.
- `check:openapi`.
- K 1st's own tamper code vs the kit's re-implementation (not diffed).
- The real-launch path: the usage gate and cockpit add were not run.
