# A3b line-number keying + KS-1186 brief — report (2026-09-17 12:45 AEST, stamp from `date`)

## BLUF
- **BUILT and INSTALLED (12:36:35, runner idle):** checker A3b/A3e now grade a site by LINE NUMBER + text when its input entry carries `key: "line+text"`. The builder writes that key only when the brief's heading reads `## Where (line-keyed …)`. Every existing input and brief has no key and keeps the old TEXT match (the fallback), unchanged.
- **Arms: 19/19** on the installed files, run through the REAL `checker.sh` under `sandbox-exec`. The old checker fails the new arms (the negative controls), and legacy verdicts are identical (KS-744, KS-1199, plus 312 predicate comparisons over `runs/`). The existing A3e arms are 5/5.
- **Row 411 item (2), the owed "A3e line+text" fix, is the SAME defect** (sites identified by text alone). It is closed for line-keyed briefs: a stays line with the same text as a must_change line no longer causes a false A3e FAIL, and it is still refused when edited. Legacy inputs keep the old A3e.
- **KS-1186: FITS.** Brief `night/briefs/KS-1186.md` and input `night/inputs/code_1186.json` cover all five sites, one test, one gate. Proven at develop `d7e95cd9f` (re-read by `ls-remote` from the scratch clone at 12:15:10, 12:42:01 and 12:43:49): golden **PASS 7/7 strict**; dropping :627 or :446 → **FAIL A3b by line number**. NOT queued.
- **Two judgements for Wednesday:**
  1. Five edits in one task breaks the "> 3 edits → split" brief rule. The commission asked for five; my reasons and a fallback split are below.
  2. The night runner (pid 30501) stopped at 12:28:57 on **gate G4-load** (1-min load 14.92 ≥ 14), 57 s after my arm run started loading vitest at 12:28:00. My load is the likely trigger. KS-1156 itself had already PASSED 7/7 and moved to done.md (12:27:57); only tickets queued behind it did not run, so re-kick the runner if any are queued.

## FOUND
1. **The defect, measured.** At the tip, `    if (result.rows.length > 0) return fromRow(result.rows[0]);` occurs 4× in `userRepo.ts` (446, 512, 585, 627; python exact count). The old A3b builds the set of removed TEXTS, so one removed duplicate satisfies every same-text site. The OLD checker passes A3b on a diff that drops the :627 hunk (arm A2), and on a diff that edits :512+:585 when the sites are :446+:512 (arm A).
2. **Same root in A3e (IMPROVEMENTS row 411 item 2).** The old A3e flags a stays site whose text is in the `-` set. With a stays :512 that has the same text as a must_change :446, a CORRECT diff that edits only :446 gets a false FAIL naming :512 (arm F0). One mechanism now closes both.
3. **Design (a choice within the commission: extend the brief path with an opt-in).** Sites ALREADY carried `line` (`text_at_tip` read at that line); the checker ignored it. An opt-in keeps legacy briefs and inputs byte-for-byte on the old path:
   - **Brief:** `## Where (line-keyed …)` heading. Each bullet's FIRST backtick span after `:NNN` is the exact line (the new_brief.sh skeleton format).
   - **Builder:** refuses (rc 2) when a quote differs from the tip line at that number; otherwise writes `key` + `text_in_brief`.
   - **Checker:** `a3b_line.py` applies the product section, with the opts A2 recorded (strict / `--recount` / `-C1` / the reanchored file), to a temp copy of the tip OUTSIDE any repo. `git diff --no-index -U0` then gives the removed tip line numbers. The model's hunk headers are never trusted.
   - **Checker verdicts:** a site whose brief text does not match the tip line → `FAIL A3b SITE TEXT MISMATCH`. Its RESULT line says "stopped at the site-text check", NOT "stopped at A3b", so RETRY-ONCE does not burn a model round on a brief defect.
   - **Unchanged:** the PARTIAL FIX message format (`:NNN \`text\``), so the runner's RETRY-ONCE builder carries the missed line (checked: `missed_sites=[{line: 627}]` from the real omit627 checker.out, with the accepted test section kept).
4. **Stated consequences of the design:**
   - A byte-identical `-x`/`+x` re-emit of a site is NOT counted as an edit.
   - Where two same-text lines are ADJACENT, `git diff`'s attribution between them is inherent ambiguity; KS-1186's duplicates are 60+ lines apart.
   - A3e still runs only when must_change sites exist (the existing gate, unchanged).
5. **KS-1186 is exactly five sites.** The ticket, its #1013-gate comment and the tip agree; `:1040` (`Promise.all`, outside `try`) is out of scope per the ticket. The ticket reads Medium in Linear (the commission's "P3" = Linear priority 3).
6. **Judgement 1: five edits vs the "> 3 → split" rule.** I kept five, as commissioned, because the measurement does not show five is wrong:
   - Each edit is one word in its own hunk, and each has its own red (omit-one runs: exactly R1…R5).
   - A partial output is now named by line number, and the retry carries that line.
   - A split would separate `getUserByEmail`'s two arms or give one half no test pass, and the ticket asks for one pass.
   - Fallback if the model drops a hunk twice: Part A = :446 :512, Part B = :585 :594 :627. This is in the brief's raise notes.
7. **Brief shaping found by measurement:**
   - Hunk 5 is trimmed to `@@ -624,6 +624,6 @@` because line 630 carries an em dash. The whole golden diff has 0 non-ASCII characters, and strict apply is rc 0.
   - The test path uses the builder's own slug (`ks1186-userrepo-ts-five-sibling-reads-still.test.ts`), so there is no suggested_test_file mismatch.
   - With a trailing comment stripped, the `+` line equals `:410` (KS-999's line). A3d exempts brief lines; this is disclosed in P2.
8. **Judgement 2: runner interference.** `night/log/night_2026-09-17.log`: `12:28:57 STOP after KS-1156: gate G4-load failed (a seat may have launched)`. My first arm run started at 12:28:00, with the old checker plus vitest in my own clone. KS-1156 had already finished: `12:27:57 TICKET KS-1156 verdict: RESULT: PASS (7/7)`, moved to done.md. The 60 s settle then hit `GATE G4 load: 1-min 14.92 >= 14 — REFUSE`, so the runner stopped before any further ticket. I did not touch `queue.md` or the runner.

## TESTED (and NOT tested)
**Arms output, verbatim** (`tests/a3b_line_number_arms.sh`, installed files, `f8c474ea6a8b`):
```
a3b line-number arms 2026-09-17 12:36:42 · checker /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/code_patch/checker.sh (2f0003a87b31) · old /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/code_patch/checker.sh.pre-0917-a3bline (553aafe0ea7a)
fixtures written
--- (a) negative controls: the OLD checker
  .. A_old_wrongsite start 12:36:42
  .. A_old_wrongsite end 12:36:58 rc=1 :: PASS A3b every must_change site the ticket names is changed by the product hunk (2 site(s))|RESULT: FAIL (2 failed)|
  ok   A  OLD checker PASSES A3b on the wrong-site diff (edits :512+:585, sites :446+:512) — it cannot tell the duplicates apart
  .. A2_old_omit627 start 12:36:58
  .. A2_old_omit627 end 12:37:14 rc=1 :: PASS A3b every must_change site the ticket names is changed by the product hunk (5 site(s))|RESULT: FAIL (2 failed)|
  ok   A2 OLD checker PASSES A3b on the KS-1186 diff with the :627 hunk dropped
--- (b) golden
  .. B_new_golden start 12:37:14
  .. B_new_golden end 12:37:29 rc=0 :: PASS A3b every must_change site the ticket names is changed by the product hunk (5 site(s); 7 line-keyed site(s), must_change and stays, matched by LINE NUMBER + text; the rest by text)|RESULT: PASS (7/7)|
  ok   B  NEW checker: golden → PASS A3b (5 must_change, 7 line-keyed, removed lines 446,512,585,594,627) and RESULT: PASS (7/7)
--- (c) wrong site
  .. C_new_wrongsite start 12:37:29
  .. C_new_wrongsite end 12:37:36 rc=1 :: FAIL A3b PARTIAL FIX — the product hunk leaves 1 of 2 named site(s) untouched: :446 `if (result.rows.length > 0) return fromRow(result.rows[0]);`|RESULT: FAIL (1 failed) — stopped at A3b (a partial fix; the tests are not run)|
  ok   C  NEW checker: wrong-site diff → FAIL A3b naming :446 (and not :512), stopped at A3b
  .. C2_new_omit627 start 12:37:36
  .. C2_new_omit627 end 12:37:43 rc=1 :: FAIL A3b PARTIAL FIX — the product hunk leaves 1 of 5 named site(s) untouched: :627 `if (result.rows.length > 0) return fromRow(result.rows[0]);`|RESULT: FAIL (1 failed) — stopped at A3b (a partial fix; the tests are not run)|
  ok   C2 NEW checker: KS-1186 with the :627 hunk dropped → FAIL A3b naming :627 only
--- (d) legacy text-keyed inputs: unchanged verdicts
  .. D1_new_ks744 start 12:37:44
  .. D1_new_ks744 end 12:38:05 rc=0 :: PASS A3b every must_change site the ticket names is changed by the product hunk (2 site(s))|RESULT: PASS (7/7)|
  ok   D1 KS-744 (legacy, 2 must_change by text): 10 PASS/FAIL/RESULT lines identical to the 12:05 fin2 run; the line-keyed path not entered
  .. D2_new_ks1199 start 12:38:05
  .. D2_new_ks1199 end 12:38:27 rc=0 :: RESULT: PASS (7/7)|
  ok   D2 KS-1199 (legacy, test-only, held): 8 PASS/FAIL/RESULT lines identical to its night run
  ok   D3 census over runs/: compared=312 differing=0 nonempty_old_outputs=24 skipped=46 inputs_with_key=0
--- (e) a line number whose tip text disagrees with the brief
  .. E_new_mismatch start 12:38:49
  .. E_new_mismatch end 12:38:56 rc=1 :: FAIL A3b SITE TEXT MISMATCH — a line-keyed site's text in the brief is NOT the tip's line at that number: :513 must_change brief=`if (result.rows.length > 0) return fromRow(result.rows[0]);` tip=`return null;`· — the brief or its |RESULT: FAIL (1 failed) — stopped at the site-text check (a brief/tip defect, not a model slip; the tests are not run)|
  ok   E  NEW checker: :512 renumbered :513 → FAIL A3b SITE TEXT MISMATCH naming :513 (tip `return null;`), no PASS A3b, RESULT does not trigger RETRY-ONCE
  .. E0_old_mismatch start 12:38:56
  .. E0_old_mismatch end 12:39:12 rc=0 :: PASS A3b every must_change site the ticket names is changed by the product hunk (5 site(s))|RESULT: PASS (7/7)|
  ok   E0 OLD checker on the same input → PASS A3b (the silent pass the new arm refuses)
--- A3e line-keyed (the owed 'A3e line+text' fix, IMPROVEMENTS row 411 item 2)
  .. F_new_446only start 12:39:12
  .. F_new_446only end 12:39:27 rc=1 :: PASS A3b every must_change site the ticket names is changed by the product hunk (1 site(s); 2 line-keyed site(s), must_change and stays, matched by LINE NUMBER + text; the rest by text)|RESULT: FAIL (2 failed)|
  ok   F  NEW checker: stays :512 has the SAME text as must_change :446; diff edits :446 only → PASS A3b, no A3e refusal
  .. F0_old_446only start 12:39:28
  .. F0_old_446only end 12:39:34 rc=1 :: PASS A3b every must_change site the ticket names is changed by the product hunk (1 site(s))|FAIL A3e a line the brief says STAYS was REMOVED by the product hunk ('-' with no '+'): :512 `if (result.rows.length > 0) return fromRow(result.rows[0]);`|RESULT: FAIL (1 failed) — stopped at A3e (a stays-line removed; the tests are not run)|
  ok   F0 OLD checker on the same → FAIL A3e naming :512 (a false refusal: :512 was never touched)
  .. G_new_446_512 start 12:39:34
  .. G_new_446_512 end 12:39:41 rc=1 :: PASS A3b every must_change site the ticket names is changed by the product hunk (1 site(s); 2 line-keyed site(s), must_change and stays, matched by LINE NUMBER + text; the rest by text)|FAIL A3e a line the brief says STAYS was REMOVED by the product hunk ('-' with no '+'): :512 `if (result.rows.length > 0) return fromRow(result.rows[0]);`|RESULT: FAIL (1 failed) — stopped at A3e (a stays-line removed; the tests are not run)|
  ok   G  NEW checker: diff edits :446 AND the stays :512 → FAIL A3e naming :512
--- the line measure under NON-strict apply opts (the section file / opts the checker recorded)
  .. I_new_lenient start 12:39:41
  .. I_new_lenient end 12:39:57 rc=0 :: PASS A3b every must_change site the ticket names is changed by the product hunk (5 site(s); 7 line-keyed site(s), must_change and stays, matched by LINE NUMBER + text; the rest by text)|RESULT: PASS (7/7)|
  ok   I  NEW checker: drifted header + miscounted hunk → A2 lenient, line measure still 446,512,585,594,627, PASS A3b
  .. J_new_reanchor start 12:39:57
  .. J_new_reanchor end 12:40:13 rc=1 :: PASS A3b every must_change site the ticket names is changed by the product hunk (1 site(s); 1 line-keyed site(s), must_change and stays, matched by LINE NUMBER + text; the rest by text)|RESULT: FAIL (2 failed)|
  ok   J  NEW checker: context the file lacks → A2 REANCHORED, the measure reads the reanchored file: REMOVED_LINES 446, PASS A3b
--- builder: the brief opt-in (reads Linear + git show on the source checkout; no writes outside /private/tmp/claude-501/night/a3bline_0917/arms)
  ok   H1 NEW builder + line-keyed brief → rc 0, 7 sites, 7 keyed line+text, every text_in_brief == text_at_tip
  ok   H2 NEW builder + :512 renumbered :513 → rc 2 REFUSED naming :513, no input written
  ok   H3 NEW builder + the brief WITHOUT 'line-keyed' in the heading → rc 0, 7 sites, 0 keyed (legacy shape)
  ok   H0 OLD builder + the line-keyed brief → 7 sites, 0 keyed (negative control)
a3b line-number arms: 19 passed, 0 failed (12:40:44)
arms rc=0
```
**Existing A3e arms on the installed checker** (`A3E_SCRATCH` pointed at my scratch dir):
```
  ok   ARM1 KS-1121 r2 retry → nothing removed
  ok   ARM2 KS-975 item 2 → nothing removed
  ok   ARM3 synthetic removal of :235 → REMOVED: :235 `const credential = await getById(id);`
  ok   ARM4 removed AND re-added → nothing removed
  ok   ARM5 the OLD checker has no A3e; the new one does
a3e arms: 5 passed, 0 failed
```
**KS-1186 through the real checker on the PLACED input** (`night/inputs/code_1186.json`, clone at `d7e95cd9f`, sandboxed).

Golden, 12:43:19–12:43:35, rc 0:
```
mode: code_patch
PASS A1 output is exactly one fenced ```diff block, nothing outside it
PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)
PASS A3 touched-file set == { Blockchain/Dev/services/auth/src/repositories/userRepo.ts , Blockchain/Dev/services/auth/src/__tests__/ks1186-userrepo-ts-five-sibling-reads-still.test.ts }
A3b line-keyed: 7 site(s) graded by LINE NUMBER + text (rc=0): REMOVED_LINES 446,512,585,594,627
PASS A3b every must_change site the ticket names is changed by the product hunk (5 site(s); 7 line-keyed site(s), must_change and stays, matched by LINE NUMBER + text; the rest by text)
PASS A3c every '+' line the brief adds is in the product hunk (5 line(s)), and no tip line is re-added as a '+' (A3d)
PASS A4 RED-FIRST: src/__tests__/ks1186-userrepo-ts-five-sibling-reads-still.test.ts fails at the untouched tip (5 failed / 7 run; controls green; assertion reds)
PASS A5 GREEN-AFTER: src/__tests__/ks1186-userrepo-ts-five-sibling-reads-still.test.ts passes with the product hunk (7 passed / 7 run)
PASS A6 whole services/auth suite: no NEW red vs the untouched tip
PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)
SUMMARY files=2 +129/-5 test=src/__tests__/ks1186-userrepo-ts-five-sibling-reads-still.test.ts red_first=yes apply_mode=strict
RESULT: PASS (7/7)
```
Wrong-site variant 1 (the :627 hunk dropped; its text is still removed at :446/:512/:585), 12:43:35–12:43:42, rc 1:
```
mode: code_patch
PASS A1 output is exactly one fenced ```diff block, nothing outside it
PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)
PASS A3 touched-file set == { Blockchain/Dev/services/auth/src/repositories/userRepo.ts , Blockchain/Dev/services/auth/src/__tests__/ks1186-userrepo-ts-five-sibling-reads-still.test.ts }
A3b line-keyed: 7 site(s) graded by LINE NUMBER + text (rc=1): REMOVED_LINES 446,512,585,594
FAIL A3b PARTIAL FIX — the product hunk leaves 1 of 5 named site(s) untouched: :627 `if (result.rows.length > 0) return fromRow(result.rows[0]);`
RESULT: FAIL (1 failed) — stopped at A3b (a partial fix; the tests are not run)
```
Wrong-site variant 2 (the :446 hunk dropped), 12:43:42–12:43:49, rc 1:
```
mode: code_patch
PASS A1 output is exactly one fenced ```diff block, nothing outside it
PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)
PASS A3 touched-file set == { Blockchain/Dev/services/auth/src/repositories/userRepo.ts , Blockchain/Dev/services/auth/src/__tests__/ks1186-userrepo-ts-five-sibling-reads-still.test.ts }
A3b line-keyed: 7 site(s) graded by LINE NUMBER + text (rc=1): REMOVED_LINES 512,585,594,627
FAIL A3b PARTIAL FIX — the product hunk leaves 1 of 5 named site(s) untouched: :446 `if (result.rows.length > 0) return fromRow(result.rows[0]);`
RESULT: FAIL (1 failed) — stopped at A3b (a partial fix; the tests are not run)
```

**NOT tested:**
- No Ornith model round: nothing queued, by instruction.
- The `-C1` FUZZY apply mode through the line measure (strict, lenient and reanchored were armed).
- Adjacent same-text duplicates.
- A line-keyed brief in TEST-ONLY mode (no product section; the helper would report LINE MEASURE ERROR if a line-keyed must_change site existed there).
- The bash_patch / doc_patch tiers (their B3b/B3c/D gates are separate and still text-keyed).
- Which HTTP routes reach each KS-1186 function end to end: out of the brief's scope, and named in its raise notes.
- `task.md`'s NAMED-SITE CHECKLIST text is unchanged. The model learns about line keying only through the input's `sites_rule` suffix and each site's `key`.

## HOW (commands and controls)
- **Lock / liveness:**
  - 12:12 and 12:15: `night/log/.night_run.lock/pid` was absent and `pgrep -x night_run.sh` gave rc 1 (control: `pgrep -x bash` rc 0).
  - The lock appeared at 12:26 (pid 30501), so I did NOT install then; I armed the `.new` files instead.
  - The runner ended at 12:28:58. Before `mv` (12:36:35): lock absent, `pgrep -x` rc 1, `ps` showed no night_run process.
- **Scratch clones:** `git clone --shared` of the Secuura checkout into `/private/tmp/claude-501/night/a3bline_0917/clone` (at `d7e95cd9f`) and `clone_fa887` (at `fa887f382`, for KS-1199). Checkout ran from script files there (`checkout.sh`, `mkclone2.sh`); farming was `prepare_clone.sh` (rc 0 ×3). No git write verb ever pointed into `!CODING`; the source porcelain was 0 at 12:19:33, 12:42:01 and 12:43:49.
- **Tip:** `git -C <scratch clone> -c core.sshCommand=<the source's> ls-remote <the source's origin URL> refs/heads/develop` at 12:15:10, 12:42:01 and 12:43:49, all `d7e95cd9f153…`.
- **Test measurements:** `runvt.sh` (sandboxed vitest, json reporter; verbose reporter for the diff text). Tip: 5 assertion reds + CONTROL + COMPLETENESS green (12:21:14). Golden 7/7. Omit-one ×5 → exactly its own red (12:21:45–49). Completeness arm → `expected +0 to be 6` (12:41:51).
- **Arms:** every rc via `> out 2>&1; rc=$?`. Every checker arm pairs a new-checker expectation with an OLD-checker negative control (A/A2/E0/F0), or a legacy identity check (D1/D2), or a census with a non-vacuity control (D3: 24 non-empty old outputs, 312 comparisons, 0 inputs already keyed). The builder arms carry an OLD-builder negative control (H0). Arms I/J were read to confirm the lenient and reanchored modes actually fired (`section_1.opts` = ` --recount --ignore-whitespace` / `section_1.reanchored.diff`).
- **Partition:**
  - Linear GraphQL read, 12:17:10.
  - GitHub REST GET (`gh_prs1186.py`, token by name from the Secuura .env, never printed), 12:41:03: 20 open PRs / 102 paths. 0 name `repositories/userRepo.ts` or `ks1186` (controls: `services/auth/src` 2, `package.json` 60).
  - READYs: 107. Two mention userRepo.ts: KS-999 (merged, `e0f41a8fa` #1013) and KS-960 (a test-only tamper at :688, product untouched). Control: 11 mention `services/auth/`.
  - `queue.md`: 0 KS-1186 lines (control: 77 `KS-` lines).
- **Brief rules checked:**
  - nothing a cell reads lives in prose (every declaration is above the first cell);
  - `+` lines are absent at the tip, exact and stripped;
  - no context lines in the fences (the fences equal the golden's `-`/`+` lines, python True);
  - 0 backslashes in the whole brief, and 0 non-ASCII in the diff and the test;
  - reds are declared under `## Red cells` (ASCII titles), with one CONTROL;
  - `## Premises (measured)`, with the instrument named per premise;
  - the clock is stamped by `date` (12:42) at placement.

## Files changed (backups)
| file (under `2_Project_Files/local-model/`) | backup | what |
|---|---|---|
| `tasks/code_patch/checker.sh` | `tasks/code_patch/checker.sh.pre-0917-a3bline` | A3b block: line-keyed sites graded by a3b_line.py; PY3B/PY3E skip keyed sites; SITE TEXT MISMATCH / LINE MEASURE ERROR stops |
| `night/build_input.sh` | `night/build_input.sh.pre-0917-a3bline` | `## Where (line-keyed …)` opt-in: quote == tip line or REFUSE; `key`, `text_in_brief`; sites_rule suffix only when keyed |
| `tasks/code_patch/a3b_line.py` | (new file) | the line measure |
| `tests/a3b_line_number_arms.sh` | (new file) | 19 arms |
| `tests/fixtures/a3b_line/` | (new dir) | KS-1186 draft-brief input, golden product + test sections, KS-744 fin2 out.md + checker.out (copied from the 12:05 session scratchpad), draft line-keyed brief, nonet.sb |
| `IMPROVEMENTS.md` | `IMPROVEMENTS.md.pre-0917-a3bline` | one row appended (stamp from `date`) |
| `night/briefs/KS-1186.md` | (new file) | the brief |
| `night/inputs/code_1186.json` | (new file) | the input |

sha256:
- `checker.sh` `2f0003a87b314feb911fbd02d53f69db4f634f9b6c4510123b55af23e54ccafd` (old `553aafe0ea7a…`)
- `build_input.sh` `e6609410f7d218b1eb59e409f53b8443366c4adbe0496b7ff6979df97f66d4b5` (old `79f475c77af4…`)
- `a3b_line.py` `c6e7e65005c97f3d313367e86d0927a6dae2462cb6baaa8967d5b7caa8b81309`

## KS-1186: FITS
- Brief `night/briefs/KS-1186.md`: sha256 `e4e005e32d1d3161eb05edb42b783ba38865b701de27e8cf28611451f7d0b527`.
- Input `night/inputs/code_1186.json`: sha256 `f1bc9048ed39dd39b9a5f841f40796c4fbfb23adfc8822e8361b3c1bcd68f4b3`. Built rc 0 at 12:43:03 by the installed builder: 7 sites, all line-keyed (5 must_change), 5 expected `+`, 5 red cells, ~30.6K prompt tokens.
- Proven at tip `d7e95cd9f153e9036ed77935a73c93504fa6e3dc`. Golden `out.md` sha256 `9a1632ba1813dc5b9c2c095725a02bc13fcedd09a5bc51be1bfba7cc58a43740` (in `/private/tmp/claude-501/night/a3bline_0917/fin/`).
- The queue line, NOT added:
```
KS-1186 input=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/code_1186.json task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/code_patch/task.md ctx=65536
```
- Rebuild pins: `ref=services/auth/src/__tests__/ks999-getuserbyid-awaits-fromrow.test.ts line=446 ctx=65536` (with `NIGHT_BRIEFS_DIR` at the default briefs dir).
- Not touched: `queue.md`, `done.md`, `candidates.md` (its SEARCH 17e row still records the KS-1186 rejection; Wednesday may want to mark it unblocked), `task.md`, `night_run.sh`. No Linear/GitHub writes, no mail, no commits.
