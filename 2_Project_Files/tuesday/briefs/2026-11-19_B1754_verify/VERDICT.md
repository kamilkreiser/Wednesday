GATE B1754: GO WITH FINDINGS @ d6c68fe on main 73eef99

Gate tier G1 (Opus), round 1 of 2. Independent read-only review of branch `b1750/mps-infra-settings-file-fix` (head
d6c68feb18dc7307c60cdc01c0ff8a64035c2424) against main 73eef991b4582beb06ce79f189813b82074a9793, MPS Commercial
Calculator. Measured 19:41 to 19:55 AEDT 2026-11-19 (clock by `date`). Blocker 0, Major 0, Minor 6.

## Findings

| # | Severity | Finding | Recommendation |
|---|---|---|---|
| F1 | Minor | The id refusal is a LENGTH rule, not an identity rule. Measured with `validate.sh`: unset, one unset, EMPTY, 35 and 37 characters are refused; 36 characters that are not a GUID, 36 spaces, the API and SPA ids SWAPPED, and the same id in both all pass (rc 0, `== validate: OK`). So the change delivers "an apply cannot BLANK the sign-in settings by an unset or empty id" and does NOT deliver "the apply cannot CHANGE them": a wrong 36-character value still rewrites four sign-in settings (AzureAd__ClientId, AzureAd__Audience, MpsCalc__Spa__ClientId, MpsCalc__Spa__ApiScope). The commit subject's "refuses blank sign-in ids" is true for empty, not for a whitespace-only value. This is the stated shape of Tuesday's Q1 reading, not a code defect. | Deploy card: before any write, compare each supplied id BY HASH with the live `AzureAd__ClientId` and `MpsCalc__Spa__ClientId` (and the derived audience and scope) and stop on any inequality. Tell the product owner in one line that "pins" was delivered as "cannot be empty", with the hash check as the rest of the pin. Optional follow-up: squash subject says "empty" (used below). |
| F2 | Minor | `infra/README.md:46` (runbook step 2, what-if pass 1) is STALE, not false: the command is unchanged and now stops at the parameter file (BCP427) unless both ids are exported. The new step-3 sentence ("this two-pass first deploy ... cannot be repeated as written on a new site") covers it by implication only. The builder's RESIDUE names it. | Follow-up docs line (not this change): mark steps 2 and 3 as the record of the first deploy, or add the export to step 2. |
| F3 | Minor | Budget literal `2026-10-01`: correct for the existing budget (record `2026-10-10_B14_STATUS.md:87` reads "start 2026-10-01"). On a FIRST create in a later month (new subscription or deleted budget), the Consumption budget API's published rule ("past start date should be selected within the timegrain period"; RELAYED from the API reference from memory, not fetched: no HTTP) refuses a past start, so the literal blocks a first deploy after October 2026. Before this change `utcNow` would have created it. The README's new paragraph says "pinned ... so an apply does not move it" and does not name this limit; the step-3 sentence names the ids only. Accepted limit, not a defect of the existing-site path. | Follow-up docs line naming the limit. Deploy card: see FOR-THE-DEPLOY-CARD item 4 (an update with a past start is UNMEASURED; a refusal there would leave the app settings applied and the deployment Failed, because the budget and the settings resource have no dependency). |
| F4 | Minor (pre-existing gap, not introduced) | `test_infra.py` cannot see a changed VALUE of the 7 expression settings or of the `WEBSITES_*`/`SCM_*` literals: my mutant m14 (AzureAd__Audience built from the SPA id) stays green, `Ran 35 tests`, OK. It also cannot see the hosted site at all (a setting set by hand). The added docs claim only "fails when the file's names and that list differ" (README) / "fails when the file and the list differ" (API.md): true, no over-claim. | Follow-up ticket if wanted: pin the expression texts in the test. The deploy card's hash comparison is the only live check. |
| F5 | Minor | The two guard rows (`TheNameListGuardFires`) start from the real compiled template, so any real names drift also turns them red, and in one case with a bare `KeyError` (m01, the feedback line removed). In every mutant at least one OTHER row names the real problem exactly (`test_the_setting_names_are_the_committed_list` prints "app setting X is in the committed list but not in the template" or the reverse). Red is never lost; the noise does not hide the cause. Acceptable as shipped. | Optional follow-up: build the guard rows from a template whose names are set equal to the list first. |
| F6 | Minor | Builder STATUS line 167: "an EMPTY id passed at apply time is refused by the template's length rule (... Error BCP333)". BCP333 is the LOCAL `build-params` compile (I measured it); refusal at apply time is ARM's `minLength` validation, which nobody has measured. Also STATUS calls the drafter's "seven anchor counts" thirteen (true: 13 OLD blocks). | Carry "apply-time refusal UNMEASURED" to the deploy card (item 3 there). |

Not findings: base `tools/demo/test/test_run_demo.py` went red (2 Ctrl-C timing rows) when run in parallel with the head
suite under load 8.4; alone it is green twice (`Ran 23`, OK). Head was green. Not touched by this change.

## Rule-on answers (measured)

1. SCOPE: PASS. `compare` ahead 1 behind 0 (merge-base = main); `git diff --numstat` exactly seven paths: API.md 8 2,
   README 12 1, names list 21 0, bicepparam 4 4, main.bicep 10 6, showcase.bicep 1 0, test_infra.py 66 0. Head blobs
   e14b1952, 55171ec9, 368b65e8, c30762fc, 05226039, c8b7d195, 34ebbeda (equal to the kit's frozen blobs). By my own
   parser of the kit's fenced blocks: 122 added lines, 0 not in a NEW block; 13 removed lines, 0 not in an OLD block
   (control: a planted line is flagged). Non-ASCII bytes base -> head: 486->486, 20->20, 0->0 (new), 0->0, 3->3, 0->0,
   3->3. Added lines + commit message: ban-list names 0 (12 names incl. Friday/Tuesday/Wednesday, each `x_by_<name>_y`
   control fires), B-number shape 0 (control fires), seat/card shapes 0 (control fires), GUID shape 0 (control fires),
   ticket key 0, Cf characters 0, hosts 0, non-ASCII 0. gitleaks over the range rc 0 (canary rc 1). The only setting
   VALUE change is the added feedback line (compiled ARM diff, item 2d). Merge: main is the parent, so the squash tree
   equals the head tree (`merge-tree --write-tree` NOT RUN: refused by the session's no-write hook outside Tuesday's
   tree; the ancestry makes it moot).
2. THE PURPOSE: with the same ids supplied, an apply of this file REMOVES nothing, BLANKS nothing and CHANGES nothing
   relative to the names and values saved on 16 November, other than ADDING `MpsCalc__Templates__Path`. It CAN still
   change four sign-in settings if a wrong 36-character id is supplied (F1), and it will remove any setting put on the
   live site by hand AFTER 16 November (the live site is not read: UNMEASURED).
   (a) Names, my own parser over the `appSettings` block vs the FIRST column of `01_pre_appsettings.tsv` (17 rows, 2
   columns, 17 distinct names): base 17 names, added `MpsCalc__Templates__Path`, removed `MpsCalc__Feedback__Path`;
   head 18, added `MpsCalc__Templates__Path`, removed none; control (head minus `MpsCalc__QuoteStore__Path`) prints it
   removed. The names list: 18 rows, unique, sorted, set-equal to the head names.
   (b) Literals, by boolean only: 11 literals at head; the 10 that are also saved are each EQUAL to the saved value
   (incl. `MpsCalc__Feedback__Path`); `MpsCalc__Templates__Path` is new. Control: the feedback value without its
   trailing slash compares unequal.
   (c) Expressions, ids taken in memory from the saved rows (never printed; each is 36 characters and GUID-shaped, the
   two differ): `AzureAd__ClientId`, `MpsCalc__Spa__ClientId`, `AzureAd__Audience` (`api://<api>`),
   `MpsCalc__Spa__ApiScope` (`api://<api>/access_as_user`) each EQUAL; `AzureAd__Instance` =
   `https://login.microsoftonline.com/` (AzureCloud loginEndpoint) EQUAL; `AzureAd__TenantId` (`tenant().tenantId`)
   EQUAL to one of the two GUIDs in `infra/README.md:3` (the tenant line), so equal while the deploy targets that
   subscription; `AllowedHosts` (`site.properties.defaultHostName`) EQUAL to `<site name recorded 13 Oct>.azurewebsites.net`.
   Controls: audience built from the SPA id unequal; instance without slash unequal. No expression differs for a reason
   other than the ids, given the same subscription and the same site.
   (d) Compiled ARM JSON, `bicep build` base vs head, full `diff`: templateHash x2 (metadata), the two id parameters lose
   `defaultValue: ""` and gain `minLength 36`/`maxLength 36` plus new descriptions, `budgetStartDate` default
   `[utcNow('yyyy-MM-01')]` -> `2026-10-01` plus description, and ONE added property
   `"MpsCalc__Feedback__Path": "/home/data/feedback/"`. Nothing else: site, plan, publishing policies, budget amount,
   notifications, tags, resource group, Log Analytics, outputs are byte-identical.
   (e) Apply-time computed defaults at head: 0 (`utcNow`/`newGuid`/`deployment()` occur only in a description string;
   base had 1). `uniqueString(rg.id)` is deterministic. Parameters with no default: exactly apiClientId, spaClientId.
3. THE REFUSAL: compiler `Bicep CLI version 0.48.1 (cec7951cf6)`; `validate.sh` on an exported head tree:
   both set (synthetic) rc 0, build/lint/lint/build-params each `OK (0 warnings)`, `Ran 35 tests`, `== validate: OK`;
   both unset rc 1, `Error BCP427` for each variable at `showcase.bicepparam(8,45)` and `(9,45)`, step
   `build-params ... FAILED`; only API set rc 1, BCP427 naming the SPA variable; only SPA set rc 1, BCP427 naming the API
   variable; API EMPTY rc 1 / SPA EMPTY rc 1, `Error BCP333 ... less than or equal to 0 ... minimum allowable length is
   36`; 35 chars rc 1 BCP333; 37 chars rc 1 `Error BCP332 ... maximum allowable length is 36`; 36 non-GUID chars rc 0;
   36 spaces rc 0; swapped rc 0; same id twice rc 0 (F1). What stops a real apply: the only apply path in the repository
   is the README runbook (`az deployment sub what-if|create -f infra/main.bicep -p infra/env/showcase.bicepparam`;
   case-insensitive search for `deployment sub|group` over every tracked file hits only `infra/README.md` and the
   `main.bicep` header comment; `scripts/` holds no template apply). That path compiles the `.bicepparam` locally first,
   so the BCP427/BCP333 refusal bites before any request (DERIVED from az's documented `.bicepparam` handling; az's own
   Bicep version UNMEASURED). An operator who bypasses the file (`-f infra/main.bicep -p apiClientId=''`, a JSON
   parameters file, the portal) meets the compiled template's `minLength: 36`/`maxLength: 36`, which ARM validates
   before any resource write (DERIVED from ARM's documented parameter validation; UNMEASURED: only a what-if or a
   create shows it). Nothing stops a wrong 36-character value (F1).
4. THE BUDGET: the record (`2026-10-10_B14_STATUS.md:87`) reads "start 2026-10-01": equal to the literal. On a FIRST
   create later than October 2026 the service rule refuses a past start (F3: accepted limit; README does not say it).
   On an UPDATE: UNMEASURED; the what-if must show NoChange on `properties.timePeriod.startDate` (see the deploy card).
5. THE GUARD: base `Ran 29 tests` OK; head `Ran 35 tests` OK; red first (head test file on the base tree):
   `Ran 35 tests`, `FAILED (failures=3, errors=3)`: FAIL feedback, budget, ids rows; ERROR names-list row and both guard
   rows (FileNotFoundError). My own mutants on copies (rows red; the row that NAMES the problem):
   m01 feedback line removed: 4 red (feedback FAIL `None != '/home/data/feedback/'`, names-list FAIL names it, guard
   "added" FAIL, guard "dropped" ERROR KeyError). m02 hand-style setting in the template: 3 red, names-list names it.
   m03 name removed from list: 3 red, named. m04 name added to list: 3 red, named. m05 duplicate: 1 red, "a name is
   listed twice". m06a real name commented `#`: 3 red, named. m06b a `# MpsCalc__...` note line: GREEN (notes are
   ignored by design: correct). m06c name with a trailing `# note`: 3 red, "the list holds names only". m06d indented
   `#` before a real name: 3 red, named. m07a list emptied (notes kept) and m07b zero bytes: 3 red, all 18 named.
   m08 budget back to `utcNow`: 1 red, budget row prints both values. m08b another literal: 1 red. m09a api default
   `''`: compile refused BCP333, `Ran 0 tests`, setUpModule ERROR naming the line (the builder's mE3 reproduced). m09b /
   m09c a 36-character default on either id: 1 red, ids row "'defaultValue' unexpectedly found". m10a decorators
   removed: 1 red `(None, None) != (36, 36)`. m10b maxLength only removed: 1 red. m10c minLength 1: 1 red. m11 a setting
   added to BOTH template and list: GREEN (the documented way to add one). m12 feedback value changed / m13 blanked:
   1 red each (feedback row). m14 audience expression changed: GREEN (F4). Builder's mutant findings (more rows red than
   predicted; mE3 unreachable by BCP333): TRUE, same mechanism reproduced. Ruling on the extra red: acceptable (F5).
   What the CI test can NOT see: anything on the hosted site, including a setting set there by hand; a changed value of
   an expression setting or of an unpinned literal; whether the ids supplied are the right ones. The docs sentences do
   not claim more.
6. OTHER SUITES at head (clone): `test_validate_script.py` `Ran 6`, OK; `test_deploy_pre1.py` `Ran 44`, OK. The CI python
   job's whole loop (tools/demo, infra, scripts tests; 12 files): base 374 tests, head 380 (+6, all in test_infra.py),
   head 0 failing files. `az bicep` in `README.md` 0, in `infra/README.md` 0 (control: `ci.yml` 1).
7. THE WORDS (each added sentence at source): TRUE: the templates row (TemplateStore.cs:133 passes the quote directory,
   the overlay path and the feedback path to `RefuseOverlap`, :181 equal/inside/containing; blank -> `InMemory()` :156;
   Program.cs:96-98 logs `PathBlank` once at start, TemplateStore.cs:483 Warning); the feedback row (FeedbackStore.cs:206-208
   blank -> `Unavailable()`; :240-258 quote store, overlay, reference directory, equal/inside/containing;
   FeedbackEndpoints.cs:610 503 `FEEDBACK_STORE_UNAVAILABLE`; FeedbackLog.cs:34); "(below)" points at "## Quote store
   rule per mode" (API.md:1023); the Hosted bullet (showcase.bicep:85 sets the value; no `Feedback__Jira` in the file);
   "a setting set on the site by hand is removed by the next apply" (the resource's full-replace semantics, module
   comment :58, and the base diff that would remove the 13 Oct hand-set: DERIVED, not applied); "cannot be repeated as
   written on a new site" (pass 1 now needs ids that do not exist until step 5: TRUE); the bicepparam comment, the
   `main.bicep` descriptions, the README "What an apply changes" paragraph and the test docstrings: TRUE of the code,
   with F1's limit on the word "blank". `infra/README.md:46`: stale, not false (F2), a follow-up, not a finding against
   this change's correctness.
8. CODEQL: `pr_codeql_check.sh --lang python` rc 0:
   ```
   VERDICT TABLE (severity rule: security-severity >= 7.0, else problem.severity == error)
     results   head 0   base 0
     KEPT      total 0   high+ 0   (post-filter: primary or any related location START line is an added line)
     NEW       total 0   high+ 0   (rule,file,primaryLocationLineHash multiset, head minus base)
     GONE      total 0
     RESULT    rc 0 PASS (KEPT high+ 0, NEW high+ 0)
   ```
   Python hand rows over the 52 non-blank added test lines: chmod/makedirs/os.open/mode literals 0 (control 1);
   sensitive-name tokens 0 (control 1); write/print/log calls 0 (control 1); regex from a variable or subprocess 0. The
   hosted CodeQL check on the landing head stays the authority.
9. TEXT: one commit, one parent, author and committer the repo identity; message plain, true (F1 wording aside),
   no key, no names, no ids, no B-number, ends "Nothing is applied or deployed by this change." and one attribution line.

## Builder STATUS claims (graded)
TRUE: scope and blobs; base 29/6/44 and head 35/6/44; red-first 3 failures + 3 errors with the six named rows; the
four `validate.sh` arms; the apply difference (base 17 removed feedback, head 18 removed none); mE1/mE3/mE4/mE5
mechanism; 122 added lines (the kit's 123 is wrong); 13 removed lines; non-ASCII unchanged; gitleaks clean.
IMPRECISE: line 167 (F6). NOT SHOWN by me: the Jira and PR prior-work searches (not re-run; read-only commission).

## FOUND / TESTED / HOW
- FOUND: F1 to F6 above; no Blocker, no Major.
- TESTED: everything under items 1 to 9, each count with a control that fired.
- NOT TESTED: any `az` (no what-if, no create, no `az bicep`), any hosted request, the live site's current settings
  (names and values), ARM's apply-time `minLength` refusal, the budget API on an update, az's own Bicep version, the
  Jira and pull-request prior-work searches, dotnet and web jobs (no file they read changed), `merge-tree` (hook-refused;
  ancestry used instead), hosted CI and hosted CodeQL.
- HOW: own clone `/private/tmp/b1754-gate/clone` (deploy key for the clone only, push URL `invalid://no-push`, never
  pushed); exported base and head trees `/private/tmp/b1754-gate/tree-*`, `/private/tmp/b1754-gate/full-base`; scripts
  `/private/tmp/b1754-gate/scripts/` (scope.py, settings.py, refusal.sh, mutants.py, ci_python.sh, export_tree.py);
  logs `/private/tmp/b1754-gate/logs/`; compiled ARM `/private/tmp/b1754-gate/arm/`; CodeQL `/private/tmp/b1754-gate/codeql/`.
  The saved settings file was read for its first column by name and its values only into memory for boolean
  comparison; no value, no client id was printed or written.
