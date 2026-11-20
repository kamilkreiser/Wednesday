From Tuesday (Datasec coordinator seat), Datasec / MPS Commercial Calculator. **Your STATUS file is the channel and the wrap** (no mail). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`. Files naming another B-number are READABLE claims only. Marks: **MEASURED** = the drafter printed it with the instrument named (sidecar `.measured` beside this kit, one line per literal); **DERIVED** = source reading or arithmetic, not run; **RELAYED** = read in another seat's file or the ticket; **UNMEASURED** = nobody has. Drafted 2026-11-20 from 17:53 to 18:02:22 AEDT (clock reads by `date`: 17:53:49 account, main and pull requests; 17:54:24 compiler; 17:56:44 refs, identity, panes and locks; the sidecar carries the rest) by a read-only drafter for Tuesday. Every `file:line` below was printed by `grep -n` over the raw files of main `debb5e28f7bbd4e0f641a829eb353ac356afdd81` (a tarball of that sha from `gh api -X GET .../tarball/<sha>`, in the drafter's scratch folder; re-print each at your main). **What the drafter ran, and where:** the project's own standalone `bicep` (`bicep build` of a COPY of `infra/` in its scratch folder, about 30 builds of about 0.6 s each), a scratch script that calls the reference FUNCTIONS of THE REFERENCE DIFF over those builds, and `ast.parse` of the patched file. **The drafter ran NO test of the project: not `infra/tests/test_infra.py` as a test run, not any other test file, no `az`, no network call but `gh api -X GET` and Jira GET.** Every predicted test total and every RED set of a TEST class below is DERIVED or UNMEASURED and says so; the function-level results marked MEASURED are from the scratch script.

# BRIEF B1791 | SEAT-M170: MPS CALCULATOR, BUILDER, MPSCALC-418: THE INFRA TEST READS THE VALUE OF EVERY EXPRESSION SETTING AND OF EVERY APP-SETTING LITERAL. ONE EXISTING TEST FILE CHANGES (`infra/tests/test_infra.py`). A NEW BRANCH, ONE COMMIT, A PUSH, NO PR. NOTHING DEPLOYED. NO `az`. NO OTHER BYTE OF `infra/` CHANGES.

Code repo `datasecau/MPS-Commercial-Calculator` (the project's `2_Project_Files` checkout is STALE: work in your OWN clone). **Base: code main `debb5e28f7bbd4e0f641a829eb353ac356afdd81` (Stamp S2).** New branch `b1791/mps-infra-setting-values-418` (none exists at origin: MEASURED, below). Lane size S to M (one file, +145 lines, 0 removed, in the reference diff). **No web server, no browser, no port: this lane starts no listener.** Project root: `/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial Calculator`. Your own folder: `.tools/b1791`.

**You do NOT** merge to `main`, deploy, open or comment on a PR, write Jira, touch the root records (`BACKLOG.md`, `JIRA.md`, history, `CLARIFICATIONS.md`), message a human, push any ref but `b1791/mps-infra-setting-values-418`, force-push, amend, reset or rebase, install anything (no `az bicep install`, no `brew`, no `pip`, no `npm`), call `az`, or write outside your STATUS, the Step-0 copy, `.tools/b1791/**`, `/private/tmp/b1791-seat-tmp`, your own clone and (only under the context band) the HANDOVER file. **The records of this change (the Jira comment, the CLARIFICATIONS entry, the move of MPSCALC-418) are NOT this lane's: Tuesday has them done by a records seat.** **No HTTP to any hosted host, not even a GET** (exceptions: `gh api -X GET`; git fetch and push to `git@github.com:datasecau/MPS-Commercial-Calculator.git`). Jira: read only. Never delete (quarantine to `.tools/b1791/_quarantine/`). Never type `cd` (`env -C '<dir>' <command>` runs a command in a folder). **Never read `.local/` or `Source_Documents/**`; no real id, tenant, host or price is written anywhere: every planted value is obviously fake (`planted`, `planted-instance`, `[variables('planted')]`).** Add NO new dependency.

model: claude-sonnet-5-5 (`/Volumes/Datasec_DEV/TUESDAY/0_Brain/dashboard/data/models_latest.json:23`). Row: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/specs/model-routing.md:92` row C2 (a single-file build that is not auth, credential or money DESIGN; it is a test-file change). Gate after: a separate kit, tier G2 (the sweep's guess, Tuesday's to set). **Launch carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes** (`brief_seat.sh:31` reads `${BRIEF_SEAT_LEVEL:-opus}`).

**READ LIST (the byte load, counted by program in the drafter's report):** this kit; `infra/tests/test_infra.py`; `infra/modules/showcase.bicep`; `infra/main.bicep`; `infra/env/showcase.app-setting-names.txt`; lines 80 to 91 of `infra/tests/test_validate_script.py`; step 7 of `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_GATE-VERIFIER-STANDARD.md` (line 31 only); the project's `CLAUDE.md`. Nothing else is read whole.

**How you read.** Long files are read with `offset` and `limit` in pages of at most 100 lines. A Read refusal is a page-size message, not the context band. A HANDOVER for context cites the statusline figure.

## THE AUTHORITY (the ticket's own text, quoted; nothing here is the product owner's ruling)
- **Standing grant:** the product owner's words to work the backlog (live board 2026-11-19 16:26:43, "keep working on other outstanding tickets and the backlog"), as relayed in Tuesday's commission. No deploy, no customer-facing word, nothing to any person. The ticket says "no word of the product changes".
- **The ticket MPSCALC-418** (read whole by Jira GET at drafting: status Backlog, 0 comments, 0 links, updated 2026-11-20 10:18 AEDT). **Scope sentence, quoted (its summary):** "infra/tests/test_infra.py cannot see the value of an expression setting or an unpinned literal: a changed audience, scope, instance, tenant, allowed hosts or sign-in id expression stays green". **Its recommendation, quoted:** "Pin the computed settings: build the template with two synthetic ids, read the compiled value of each of the seven settings and compare it with the value the committed shape says (the audience is api:// plus the API id, the scope adds the access scope, the instance is the Azure login endpoint, the tenant is the deployment's tenant, the allowed hosts are the site's default host name), and pin each remaining literal in the same way. Each new row is shown red by a planted change and green without it. No real id is written to any file." **Its acceptance check, quoted:** "The test file fails when the compiled value of any of the seven computed settings differs from the committed shape, shown by a planted change for each; it fails on a changed literal that is not pinned today; it still passes on the real template; the count of tests is printed before and after; no id is written to any file; no other byte of infra changes."
- **Everything else in this kit is Tuesday's choice as coordinator (proposed by the drafter, stamped by Tuesday), NOT the product owner's.** Your commit text and STATUS write it that way or do not mention it. No text of yours may say the product owner decided, approved or ruled anything.
- **Two places where the ticket's sentence and the compiler differ (Tuesday's reading, D1 and D2 below; Q1 and Q2 are the alternatives):** (1) `bicep build` never substitutes an id: the "compiled value" of a computed setting is an ARM expression STRING (MEASURED, below), so "build with two synthetic ids" has nothing to substitute into; the kit pins the expression string, which is what Azure receives. (2) "each remaining literal" is read as the app-setting literals no check pins today (the ticket's own "Where" names `infra/modules/showcase.bicep` lines 60 to 91, the settings block).

## WHAT THE FILE CANNOT SEE TODAY (MEASURED by program at main; every pointer re-printed by you)
- `infra/tests/test_infra.py` at main: blob `34ebbeda76155d3336579c744eef11cb64510f27` (the sweep and the ticket print the same eight characters), 494 lines, 35 tests by the indented pattern (`^[[:space:]]+def test_`; the column-1 pattern `^def test_` prints 0): `TheTemplateMeetsTheBaseline` 12, `EachGuardFiresOnItsOwnTerm` 16, `TheNameListGuardFires` 2, `TheAllowedListFiresOnAPlantedResource` 2, `TheCompilerIsNeverAz` 3 (sum 35, awk by class). **1 line is non-ASCII** (line 3, the arrow in the docstring): your edit keeps it and adds only ASCII.
- The template compiles the 18 app settings (`infra/modules/showcase.bicep:60` the resource, `:65` to `:89` the values) to **11 literals and 7 expressions**. The seven expressions, as `bicep build` prints them (MEASURED; the module's own compiled template holds them): `AzureAd__Instance` `[environment().authentication.loginEndpoint]` (`showcase.bicep:73`); `AzureAd__TenantId` `[tenant().tenantId]` (`:74`); `AzureAd__ClientId` `[parameters('apiClientId')]` (`:75`); `AzureAd__Audience` `[if(empty(parameters('apiClientId')), '', format('api://{0}', parameters('apiClientId')))]` (`:76`); `MpsCalc__Spa__ClientId` `[parameters('spaClientId')]` (`:77`); `MpsCalc__Spa__ApiScope` `[if(empty(parameters('apiClientId')), '', format('api://{0}/access_as_user', parameters('apiClientId')))]` (`:78`); `AllowedHosts` `[reference(resourceId('Microsoft.Web/sites', variables('siteName')), '2024-11-01').defaultHostName]` (`:79`).
- Today the file checks these seven only by NAME (`test_infra.py:185` to `:188`, "is missing (I-3)") and the names against the committed list (`:230`, `:276`). Of the 11 literals, 7 are pinned by value (`settings_problems` `:177` to `:181`: 5; the two store-path tests: `MpsCalc__Templates__Path`, `MpsCalc__Feedback__Path`). **The 4 literals no check pins:** `WEBSITES_CONTAINER_START_TIME_LIMIT` ('600', `showcase.bicep:65`), `SCM_DO_BUILD_DURING_DEPLOYMENT` ('false', `:67`), `WEBSITES_ENABLE_APP_SERVICE_STORAGE` ('true', `:69`), `MpsCalc__CatalogueOverlay__Path` ('/home/data/catalogue-overlay/', `:83`; only its distinctness from two other paths is tested, `:261`).
- **The module call passes the two ids by name** (`infra/main.bicep:65` and `:66`, inside `module showcase` `:58`); the compiled module deployment carries them as `[parameters('apiClientId')]` and `[parameters('spaClientId')]` (MEASURED). **A swap there compiles, leaves every expression inside the module unchanged and is invisible to the seven-setting pin alone**: that is why the kit pins the module call too (D4).
- **The blindness, measured at function level:** each of the 13 plants of THE PLANTS (one changed line of `showcase.bicep` or `main.bicep`) compiles with rc 0 and leaves `all_problems(template)` (the six checks of `ALL_CHECKS`, `:214`) at 0 problems (MEASURED 13 of 13 by the scratch script). Three of the 13 (the `MpsCalc__Spa__ClientId` plant and the two module-call swaps) print a bicep `no-unused-params` WARNING on stderr (MEASURED 3 of 13), so the existing `test_build_has_no_warning` (`:255`) is expected to catch those three (DERIVED, not run); a swap that leaves both parameters used (the `AzureAd__ClientId` plant, the audience plant) prints no warning (MEASURED 0 of 10 others).

## THE DESIGN (Tuesday's choices as coordinator; each with its source; Q1 to Q4 hold the alternatives)
- **D1 (what "compiled value" means).** The pin is the exact ARM expression string for six settings and a shape (a regex) for `AllowedHosts`, whose string carries the site API version (`'2024-11-01'`): a bump of that version is not a change of meaning, so the regex leaves the version free as `[0-9]{4}-[0-9]{2}-[0-9]{2}` and fixes everything else. Source: the ticket's recommendation sentence, read against the compiler's output. **No evaluator of ARM expressions is written** (HOLD).
- **D2 (the literals).** The four unpinned app-setting literals are pinned by value. The site's own unpinned properties (`alwaysOn`, `http20Enabled`, `remoteDebuggingEnabled`, `use32BitWorkerProcess`, `appCommandLine`, `clientAffinityEnabled`, `publicNetworkAccess`: 7, MEASURED against the `SITE_EXPECT` table at `:117`) are NOT pinned in this lane: the ticket's "Where" is the settings block (Q2).
- **D3 (where the new guards sit).** The new functions are NOT added to `ALL_CHECKS` (the way `setting_name_problems` is not). Reason, by program: `EachGuardFiresOnItsOwnTerm.one` demands exactly ONE problem from `all_problems`, and two existing tests (`test_secret_shaped_azuread_value` `:387` sets `AzureAd__ClientId`, `test_secret_shaped_spa_value` `:391` sets `MpsCalc__Spa__ClientId`) would then read two problems; kept out, no existing expectation changes (Q3).
- **D4 (the module call).** `module_id_problems` pins the two parameters of the one module deployment as `[parameters('apiClientId')]` and `[parameters('spaClientId')]`. Source: the ticket's named mutant ("the audience built from the SPA id") has a sibling at the call site that the expression pin cannot see (MEASURED above).
- **D5 (red proof, three layers, each a test class).** (a) real template: green; (b) the compiled JSON changed one value at a time (the shape the file already uses); (c) the SOURCE changed one line at a time and compiled again (the shape of the review's mutant and of `TheAllowedListFiresOnAPlantedResource`, `:423`). 13 source plants, one per pinned row and per module parameter (11 + 2).
- **D6 (no id in the file).** The tables hold expressions and literals only. The plants use `planted`, `planted-instance` and `[variables('planted')]`. `az` is never called; the compiler comes from `$BICEP` or `bicep` on PATH as the file already does (`bicep_command` `:57`).
- **D7 (do not touch).** The text of the missing-compiler sentence at `:69` (it starts `no Bicep compiler: set BICEP to a standalone bicep binary` and ends `(this test never calls az)`) is READ by `infra/tests/test_validate_script.py:86` to `:91` (`test_the_sentence_is_the_one_the_test_of_the_templates_uses`): your edit must not change a byte of it.

## THE REFERENCE DIFF (the drafter's patched COPY of the base blob; `ast.parse` ok; the functions MEASURED green over the real template and RED once over each of the 13 plants; the test CLASSES NOT RUN)
The CELLS are the specification; you may write the code differently if every test and every plant below behaves as stated. Unified diff of `infra/tests/test_infra.py` from blob `34ebbeda76155d3336579c744eef11cb64510f27` (+145 and -0 lines in 3 hunks, counted by program over this block; 0 non-ASCII bytes in the added lines; patched-copy blob `c0e6a2720e3e64aeb879d55c178b9715ff4cb20b`; the patched file counts 43 tests by the indented pattern, 35 + 8):
```diff
--- a/infra/tests/test_infra.py
+++ b/infra/tests/test_infra.py
@@ -13,6 +13,9 @@
   and no AzureAd*/MpsCalc__Spa* value (or any other) that looks like a secret.
 - app setting NAMES: exactly the committed list env/showcase.app-setting-names.txt (the resource replaces every
   setting on each apply, so a name missing from the file is removed from the site);
+- app setting VALUES (MPSCALC-418): the seven settings the template computes and the literals no other check pins, each as the
+  committed expression or literal (`bicep build` does not evaluate: the expression string is what Azure receives), and the
+  two ids as the module call passes them;
 - parameters: the two client ids have no default and a GUID's length; the budget start is a fixed date.
 """
 import copy
@@ -235,8 +238,58 @@
     have, want = set(st), set(names)
     return (["app setting %s is in the template but not in the committed list" % k for k in sorted(have - want)] +
             ["app setting %s is in the committed list but not in the template" % k for k in sorted(want - have)])
+
+
+# ---- the setting VALUES (MPSCALC-418) ----------------------------------------------------------------------------------
+# `bicep build` does not evaluate an expression: a setting the template computes compiles to an ARM expression string such as
+# "[parameters('apiClientId')]", and that string is what Azure receives. These tables are the committed shape of every value
+# the other checks leave open. Each entry is an expression or a literal: no tenant, client id or host name is written here.
+COMPUTED_SETTINGS = {
+    "AzureAd__Instance": "[environment().authentication.loginEndpoint]",
+    "AzureAd__TenantId": "[tenant().tenantId]",
+    "AzureAd__ClientId": "[parameters('apiClientId')]",
+    "AzureAd__Audience": "[if(empty(parameters('apiClientId')), '', format('api://{0}', parameters('apiClientId')))]",
+    "MpsCalc__Spa__ClientId": "[parameters('spaClientId')]",
+    "MpsCalc__Spa__ApiScope": "[if(empty(parameters('apiClientId')), '', format('api://{0}/access_as_user', parameters('apiClientId')))]",
+}
+# AllowedHosts is the site's own default host name. The shape leaves the API version free: a version bump is not a failure.
+ALLOWED_HOSTS_SHAPE = re.compile(
+    r"^\[reference\(resourceId\('Microsoft\.Web/sites', variables\('siteName'\)\), '[0-9]{4}-[0-9]{2}-[0-9]{2}'\)\.defaultHostName\]$")
+# The literals no other check pins (the others are pinned by settings_problems and the two store-path tests).
+PINNED_LITERALS = {
+    "WEBSITES_CONTAINER_START_TIME_LIMIT": "600",
+    "SCM_DO_BUILD_DURING_DEPLOYMENT": "false",
+    "WEBSITES_ENABLE_APP_SERVICE_STORAGE": "true",
+    "MpsCalc__CatalogueOverlay__Path": "/home/data/catalogue-overlay/",
+}
+MODULE_ID_PARAMS = ("apiClientId", "spaClientId")
+
+
+def setting_value_problems(template):
+    """Each computed setting reads its committed expression, AllowedHosts its committed shape, each pinned literal its value."""
+    st = app_settings(template)
+    if st is None:
+        return ["expected exactly one sites/config 'appsettings' resource"]
+    out = []
+    for k, want in {**COMPUTED_SETTINGS, **PINNED_LITERALS}.items():
+        if st.get(k) != want:
+            out.append("app setting %s is %r, not %r" % (k, st.get(k), want))
+    got = st.get("AllowedHosts")
+    if not (isinstance(got, str) and ALLOWED_HOSTS_SHAPE.match(got)):
+        out.append("app setting AllowedHosts is %r, not the site's default host name" % (got,))
+    return out
 
 
+def module_id_problems(template):
+    """The module call passes each client id to the parameter of its own name (a swap compiles and every setting expression stays as committed)."""
+    mods = of_type(template, MODULE_TYPE)
+    if len(mods) != 1:
+        return ["expected exactly 1 module deployment, found %d" % len(mods)]
+    given = (mods[0].get("properties") or {}).get("parameters") or {}
+    return ["module parameter %s is %r, not %r" % (n, (given.get(n) or {}).get("value"), "[parameters('%s')]" % n)
+            for n in MODULE_ID_PARAMS if (given.get(n) or {}).get("value") != "[parameters('%s')]" % n]
+
+
 # ---- tests -------------------------------------------------------------------------------------------------------------
 class Compiled:
     template = None
@@ -420,6 +473,98 @@
         self.assertIn("MpsCalc__Set__ByHand is in the template but not in the committed list", got[0])
 
 
+class TheSettingValuesAreTheCommittedShape(unittest.TestCase):
+    def test_no_setting_value_problem_in_the_compiled_template(self):
+        self.assertEqual(setting_value_problems(Compiled.template), [])
+
+    def test_the_two_ids_reach_the_module_as_themselves(self):
+        self.assertEqual(module_id_problems(Compiled.template), [])
+
+    def test_every_pinned_value_names_a_listed_setting(self):
+        # A name mistyped in a table would pin nothing; each table key must be a name of the committed list.
+        listed = set(listed_setting_names())
+        for k in [*COMPUTED_SETTINGS, *PINNED_LITERALS, "AllowedHosts"]:
+            self.assertIn(k, listed, k)
+
+
+class TheSettingValueGuardsFireOnCompiledMutants(unittest.TestCase):
+    """Red-proof on the compiled template: change ONE value (or remove it); exactly one problem, and it names the setting."""
+
+    def one_setting_problem(self, key, value):
+        t = copy.deepcopy(Compiled.template)
+        if value is None:
+            del app_settings(t)[key]
+        else:
+            app_settings(t)[key] = value
+        got = setting_value_problems(t)
+        self.assertEqual(len(got), 1, got)
+        self.assertIn(key, got[0])
+
+    def test_each_computed_setting_changed_is_one_problem(self):
+        for key in [*COMPUTED_SETTINGS, "AllowedHosts"]:
+            with self.subTest(key=key):
+                self.one_setting_problem(key, "[variables('planted')]")
+
+    def test_each_pinned_literal_changed_is_one_problem(self):
+        for key in PINNED_LITERALS:
+            with self.subTest(key=key):
+                self.one_setting_problem(key, "planted")
+
+    def test_each_pinned_value_removed_is_one_problem(self):
+        for key in [*COMPUTED_SETTINGS, *PINNED_LITERALS, "AllowedHosts"]:
+            with self.subTest(key=key):
+                self.one_setting_problem(key, None)
+
+    def test_each_id_given_to_the_other_parameter_is_one_problem(self):
+        for name, other in (("apiClientId", "spaClientId"), ("spaClientId", "apiClientId")):
+            with self.subTest(parameter=name):
+                t = copy.deepcopy(Compiled.template)
+                of_type(t, MODULE_TYPE)[0]["properties"]["parameters"][name]["value"] = "[parameters('%s')]" % other
+                got = module_id_problems(t)
+                self.assertEqual(len(got), 1, got)
+                self.assertIn(name, got[0])
+
+
+class TheSettingValueGuardsFireOnPlantedSource(unittest.TestCase):
+    """Red-proof on SOURCE (the shape of the independent review's mutant): copy infra/, change ONE line of a .bicep file, compile,
+    exactly one new problem, and it names the setting or the module parameter. A planted change may add a bicep warning (an unused
+    parameter): that is not asserted here, test_build_has_no_warning reads the real template."""
+
+    # (file under infra/, text that must occur exactly once, its replacement, what the one problem must name)
+    PLANTS = [
+        ("modules/showcase.bicep", "AzureAd__Instance: environment().authentication.loginEndpoint", "AzureAd__Instance: 'planted-instance'", "AzureAd__Instance"),
+        ("modules/showcase.bicep", "AzureAd__TenantId: tenant().tenantId", "AzureAd__TenantId: subscription().tenantId", "AzureAd__TenantId"),
+        ("modules/showcase.bicep", "AzureAd__ClientId: apiClientId", "AzureAd__ClientId: spaClientId", "AzureAd__ClientId"),
+        ("modules/showcase.bicep", "'api://${apiClientId}'", "'api://${spaClientId}'", "AzureAd__Audience"),
+        ("modules/showcase.bicep", "MpsCalc__Spa__ClientId: spaClientId", "MpsCalc__Spa__ClientId: apiClientId", "MpsCalc__Spa__ClientId"),
+        ("modules/showcase.bicep", "/access_as_user'", "/access_as_planted'", "MpsCalc__Spa__ApiScope"),
+        ("modules/showcase.bicep", "AllowedHosts: site.properties.defaultHostName", "AllowedHosts: '*'", "AllowedHosts"),
+        ("modules/showcase.bicep", "WEBSITES_CONTAINER_START_TIME_LIMIT: '600'", "WEBSITES_CONTAINER_START_TIME_LIMIT: '230'", "WEBSITES_CONTAINER_START_TIME_LIMIT"),
+        ("modules/showcase.bicep", "SCM_DO_BUILD_DURING_DEPLOYMENT: 'false'", "SCM_DO_BUILD_DURING_DEPLOYMENT: 'true'", "SCM_DO_BUILD_DURING_DEPLOYMENT"),
+        ("modules/showcase.bicep", "WEBSITES_ENABLE_APP_SERVICE_STORAGE: 'true'", "WEBSITES_ENABLE_APP_SERVICE_STORAGE: 'false'", "WEBSITES_ENABLE_APP_SERVICE_STORAGE"),
+        ("modules/showcase.bicep", "MpsCalc__CatalogueOverlay__Path: '/home/data/catalogue-overlay/'", "MpsCalc__CatalogueOverlay__Path: '/home/data/planted/'", "MpsCalc__CatalogueOverlay__Path"),
+        ("main.bicep", "    apiClientId: apiClientId\n", "    apiClientId: spaClientId\n", "module parameter apiClientId"),
+        ("main.bicep", "    spaClientId: spaClientId\n", "    spaClientId: apiClientId\n", "module parameter spaClientId"),
+    ]
+
+    def test_each_planted_source_change_is_one_problem(self):
+        for rel, anchor, planted, names in self.PLANTS:
+            with self.subTest(plant=names):
+                with tempfile.TemporaryDirectory(prefix="m418-plant-") as d:
+                    copy_dir = os.path.join(d, "infra")
+                    shutil.copytree(INFRA, copy_dir, ignore=shutil.ignore_patterns("tests", "__pycache__"))
+                    path = os.path.join(copy_dir, *rel.split("/"))
+                    with open(path, encoding="utf-8") as f:
+                        text = f.read()
+                    self.assertEqual(text.count(anchor), 1, "unique anchor")
+                    with open(path, "w", encoding="utf-8") as f:
+                        f.write(text.replace(anchor, planted))
+                    t, _ = compile_bicep(os.path.join(copy_dir, "main.bicep"))
+                got = setting_value_problems(t) + module_id_problems(t)
+                self.assertEqual(len(got), 1, got)
+                self.assertIn(names, got[0])
+
+
 class TheAllowedListFiresOnAPlantedResource(unittest.TestCase):
     """Red-proof on SOURCE: copy infra/, plant one storage account in the module, compile, the allowed-list check fires."""
 
```
New tests, by program over the patched copy: `TheSettingValuesAreTheCommittedShape` 3, `TheSettingValueGuardsFireOnCompiledMutants` 4, `TheSettingValueGuardsFireOnPlantedSource` 1 (13 sub-tests inside it). **Total after: 43 (DERIVED: 35 + 8; you print it).**

## CENSUS: the tests that pin the OLD behaviour, by program (the frame: `infra/tests/test_infra.py` at main, 35 tests; the plants and the sibling file)
| Class of test | Tests (`file:line`) | What happens to them |
|---|---|---|
| must stay green UNTOUCHED (the new guards are outside `ALL_CHECKS`, D3) | `test_no_problem_in_the_compiled_template` (`:258`), the other 11 tests of `TheTemplateMeetsTheBaseline`, all 16 of `EachGuardFiresOnItsOwnTerm` (`:329` onward), the 2 of `TheNameListGuardFires`, the 2 of `TheAllowedListFiresOnAPlantedResource`, the 3 of `TheCompilerIsNeverAz` | no edit: 35 of 35 expectations unchanged (1 + 11 + 16 + 2 + 2 + 3 = 35) |
| would flip from one problem to two IF the new check were folded into `ALL_CHECKS` | `test_secret_shaped_azuread_value` (`:387`), `test_secret_shaped_spa_value` (`:391`) | the reason for D3; do NOT fold the check in; if you find a reason to, STOP (Q3) |
| reads the file's TEXT | `infra/tests/test_validate_script.py:86` to `:91` | stays green iff `:69` is byte-equal (D7); you run that file |
No existing expectation changes. **If your run shows any of the 35 red after your edit: STOP and print it; do not edit the test.**

## PREDICTIONS (write `.tools/b1791/predictions.txt` BEFORE any edit of the test file; print its sha256; a prediction that fails is named in STATUS, not edited)
(a) At main in your clone, with `BICEP` set as THE TOOLCHAIN says: `infra/tests/test_infra.py` prints `Ran 35 tests` and `OK` (RELAYED: the ticket says 35; the drafter counted 35 by program but did not run it). (b) Blind: with each of the 13 plants applied to the SOURCE over the UNEDITED test file, 10 of 13 runs read `OK` and the three that print an unused-parameter warning (the `MpsCalc__Spa__ClientId` plant and both module-call swaps) read `FAILED` on `test_build_has_no_warning` only (DERIVED). (c) With the reference code: `Ran 43 tests` and `OK`. (d) Over the real source with each of the 13 plants and the NEW file: exactly the new real-template guard goes red (`test_no_setting_value_problem_in_the_compiled_template` for the 11 setting plants, `test_the_two_ids_reach_the_module_as_themselves` for the 2 module plants), naming the key; for the 3 warning plants `test_build_has_no_warning` is red too; the other 40 or 39 stay green (UNMEASURED). (e) Each of the six mutants of THE MUTANTS below goes red on at least the named tests; no mutant stays green. (f) After the commit: exactly ONE path differs between main and your HEAD. (g) Every added line is ASCII. (h) The CI python step's loop as CI runs it: every file rc 0 (the files at base: 15, MEASURED by `ls` over the tarball: 2 under `infra/tests`, 8 under `scripts/tests`, 5 under `tools/demo/test`).

## THE PLANTS AND THE MUTANTS (the builder's own proof, "builder's own run, not independent"; each applied with the Edit tool, run, undone with the Edit tool, proved by `git hash-object` equal to the blob printed before)
**Source plants (13; edits of the clone's two `.bicep` SOURCE files, never committed). The anchor is the text that must occur exactly once in its file (MEASURED once each, by the scratch script); the drafter's compile of each read rc 0:**
| # | File | Replace | With | Row it must turn red |
|---|---|---|---|---|
| P1 | `modules/showcase.bicep:73` | `AzureAd__Instance: environment().authentication.loginEndpoint` | `AzureAd__Instance: 'planted-instance'` | AzureAd__Instance |
| P2 | `:74` | `AzureAd__TenantId: tenant().tenantId` | `AzureAd__TenantId: subscription().tenantId` | AzureAd__TenantId |
| P3 | `:75` | `AzureAd__ClientId: apiClientId` | `AzureAd__ClientId: spaClientId` | AzureAd__ClientId |
| P4 | `:76` | `'api://${apiClientId}'` | `'api://${spaClientId}'` (the review's mutant) | AzureAd__Audience |
| P5 | `:77` | `MpsCalc__Spa__ClientId: spaClientId` | `MpsCalc__Spa__ClientId: apiClientId` | MpsCalc__Spa__ClientId (also a warning) |
| P6 | `:78` | `/access_as_user'` | `/access_as_planted'` | MpsCalc__Spa__ApiScope |
| P7 | `:79` | `AllowedHosts: site.properties.defaultHostName` | `AllowedHosts: '*'` | AllowedHosts |
| P8 | `:65` | `WEBSITES_CONTAINER_START_TIME_LIMIT: '600'` | `... '230'` | WEBSITES_CONTAINER_START_TIME_LIMIT |
| P9 | `:67` | `SCM_DO_BUILD_DURING_DEPLOYMENT: 'false'` | `... 'true'` | SCM_DO_BUILD_DURING_DEPLOYMENT |
| P10 | `:69` | `WEBSITES_ENABLE_APP_SERVICE_STORAGE: 'true'` | `... 'false'` | WEBSITES_ENABLE_APP_SERVICE_STORAGE |
| P11 | `:83` | `MpsCalc__CatalogueOverlay__Path: '/home/data/catalogue-overlay/'` | `MpsCalc__CatalogueOverlay__Path: '/home/data/planted/'` | MpsCalc__CatalogueOverlay__Path |
| P12 | `main.bicep:65` | `    apiClientId: apiClientId` (with its newline) | `    apiClientId: spaClientId` | module parameter apiClientId (also a warning) |
| P13 | `main.bicep:66` | `    spaClientId: spaClientId` (with its newline) | `    spaClientId: apiClientId` | module parameter spaClientId (also a warning) |
(MEASURED by the scratch script over the patched functions: each of P1 to P13 gives exactly 1 problem, naming the row, and `all_problems` 0.) The same 13 are the table `PLANTS` inside the test class (so a plant is also proved on every run).
**Mutants of the NEW test code (edits of `test_infra.py`, undone with the Edit tool; a green mutant means a missing test: add the test, never edit the mutant):**
| Id | Mutant | Must go red (at least) |
|---|---|---|
| MT1 | `setting_value_problems` loops over `PINNED_LITERALS` only (the computed table skipped) | the computed-changed test, the removed test, and the source plants P1 to P6 |
| MT2 | `ALLOWED_HOSTS_SHAPE` replaced by `re.compile(r".*")` | the AllowedHosts sub-test of the computed-changed test, and the source plant P7 (a removed value is `None`, which the regex also refuses, so the removed test alone is not the proof) |
| MT3 | `module_id_problems` returns `[]` | the id-swap test, the module plants P12 and P13 |
| MT4 | `PINNED_LITERALS` emptied | the literal-changed test, the removed test (its four literal sub-tests) and plants P8 to P11; `test_every_pinned_value_names_a_listed_setting` stays green (it tests the table keys, not the guard) |
| MT5 | `MODULE_ID_PARAMS = ("apiClientId",)` | the id-swap test (its `spaClientId` sub-test) and plant P13 |
| MT6 | `COMPUTED_SETTINGS` gets one name mistyped (`AzureAd__Audiance`) | `test_every_pinned_value_names_a_listed_setting` and the real-template test |
(All six RED sets are DERIVED: the drafter ran no test class. The property is that no mutant stays green.)

## COUNTS, SELECTORS, TOOLCHAIN
- **Test counts by the indented pattern** `^[[:space:]]+def test_` in `infra/tests/test_infra.py`: 35 at main, 43 in the patched copy (the column-1 pattern prints 0 at both). Runtime: unittest prints `Ran N tests`.
- **Selectors (unittest, positional class names; checked against the class lines at main and in the patched copy):** the run `python3 -I infra/tests/test_infra.py TheSettingValuesAreTheCommittedShape -v` names a class that does not exist at main (it appears with your edit); the classes that exist at main are `TheTemplateMeetsTheBaseline` (`def test_build_has_no_warning` at `:255`), `EachGuardFiresOnItsOwnTerm` (`:329`), `TheNameListGuardFires` (`:405`), `TheAllowedListFiresOnAPlantedResource` (`:423`), `TheCompilerIsNeverAz`. **Print the `Ran N tests` line of EVERY run and STOP on `Ran 0 tests` or on an AttributeError for a class name (a selector that matches nothing may read rc 0).** Prefer the whole file; the file is light (about 35 compiles at most, each about 0.6 s on this machine: UNMEASURED for the whole file).
- **Compiler by PATH.** There is no `bicep` on PATH and `$BICEP` is unset on this machine (MEASURED: `command -v bicep` prints nothing; the variable reads empty). **The project's own standalone compiler exists: `/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/bicep-v0.48.1/bicep`** (a Mach-O arm64 executable, 116883328 bytes; `--version` prints `Bicep CLI version 0.48.1 (cec7951cf6)`, MEASURED at 17:54:24). Hosted CI installs the SAME version (`az bicep install --version v0.48.1`, `ci.yml:105`) and sets `BICEP="$HOME/.azure/bin/bicep"` (`ci.yml:110`). **Run every test as `env -C '<your clone>' BICEP='<that path>' python3 -I infra/tests/test_infra.py ...`. Print `$BICEP --version` once. Do not install anything; if the file at that path is gone: `STOPPED: NEEDS TUESDAY no bicep`.** The file finds the compiler as `$BICEP`, then `bicep` on PATH, and nothing else (`bicep_command`, `test_infra.py:57`); with neither every test FAILS, never skips.
- **Python.** The machine's `/opt/homebrew/bin/python3` prints `Python 3.14.10` (MEASURED); hosted CI runs the runner's `python3` (UNMEASURED which). Standard library only; write nothing newer than Python 3.9 (no `match`, no `X | Y` types); the reference code uses none.
- **The CI predicate (read at main, `ci.yml:104` to `:118`, the step named "tools/demo, infra and scripts tests (python3 -I, standard library only)"):** for each file of `tools/demo/test/test_*.py infra/tests/test_*.py scripts/tests/test_*.py`, `python3 -I "$t"` and the step exits non-zero if any file did. **Pass predicate: every one of the 15 files rc 0.** You run that loop as CI does, at base and at your head (STATUS prints each file and its rc; a red that is not yours is NAMED with its cause and its base row).

## FACTS (re-print at your main; a pointer is the drafter's, printed once, and can be stale)
1. **Refs** (MEASURED by `gh api -X GET` under the project `GH_CONFIG_DIR`, `gh auth status` rc 0, at 17:53:49 and 17:56:44): main `debb5e28f7bbd4e0f641a829eb353ac356afdd81` (both reads); open pull requests 0; `matching-refs/heads/b1791` 0 rows (control: `matching-refs/heads/b1767` 1 row); a search of the repo for the key MPSCALC-418 reads total_count 0 (control: MPSCALC-278 reads 3). **Landing rule** (read in the first-round kits of this project): Tuesday opens the PR and lands it with the head pinned (`--match-head-commit`), squash; you open nothing.
2. **The blobs at main** (MEASURED by `git hash-object` over the tarball copy): `infra/tests/test_infra.py` `34ebbeda76155d3336579c744eef11cb64510f27` (the only path you change), `infra/main.bicep` `05226039c7497f13e636d2f627b92c4d2106d0ba`, `infra/modules/showcase.bicep` `c8b7d195c2e93a02cdb91c37e0af54dee4329cf0`, `infra/env/showcase.app-setting-names.txt` `368b65e8567bcc0a63a98c2b481c8444e5aa7e48`, `infra/tests/test_validate_script.py` `96216964452ed6e5252b24b1bcfd15e6077cf3ea`. **A different blob at your main means main moved: STOP.** (The sweep's `34ebbeda` agrees for the test file.)
3. **The committed name list** `infra/env/showcase.app-setting-names.txt` holds 18 names by program (21 lines, 3 comment lines); every key of the three tables of the reference diff is on it (MEASURED: 11 of 11).
4. **The ticket's pointers (RELAYED, re-measured):** `test_infra.py:185` to `:188` is right at main; "a dictionary near line 170" is at `:177` to `:181`; "35 tests at code main 50d2a471" is 35 at `debb5e28` (by program; `50d2a471` itself was not read). The ticket's "lines 60 to 91" of `showcase.bicep` is right (`:60` the resource, `:91` its closing brace). The deploy record's "10 shared literals" does not match the 11 literals in the template; this lane pins by the template, not by that count.
5. **Machine** (MEASURED 17:56:44): `df -g` 1023 GiB free; no entry of the project's `.tools` listing names `lock` (0; control: 3 entries name `dotnet`); one `Datasec/MPS-` pane, `Datasec/MPS-R284` (the records seat of kit B1781: it writes Jira and the root records, and shares no file with you); `LC_ALL=C uptime` load averages 6.26 5.36 4.36.
6. **Git identity (the repo's own, never overridden):** in YOUR clone set local `user.name` and `user.email` to exactly what the project repo's `git -C '<project>/2_Project_Files' --no-optional-locks config --local --get user.email` and `user.name` print (by program, never typed; the email is 29 bytes with the newline, MEASURED). **Never `git -c user.name/user.email`, never `GIT_AUTHOR_*` / `GIT_COMMITTER_*`.** READY prints `git log --format='%h %ae | %ce'` for the new commit, each address equal to the repo's configured email.
7. **Stale ssh config:** the project repo's local `core.sshCommand` names `/Volumes/Laptop-DEV/...` (the count of that string in it is 1, MEASURED): use an explicit key for each command, as THE WORK says.
8. **Size: S to M.** One file, +145 lines. The compile-heavy test class runs 13 builds.

## THE WORK (serial; one seat)
0. **Step 0 and STATUS** into `1_Project_Definition/Briefs/2026-11-20_B1791_STATUS.md`: FIRST line `PROGRESS B1791: PENDING`; the kit copy into `Briefs/` (`cmp`, sha256, 0 unfilled slots); the REFUSE counts with controls; `date`; `LC_ALL=C uptime`; `df -g`; **target READY = Step 0 + 120 minutes (`date -v+120M`); the push by Step 0 + 90, or STOP; HARD STOP = Stamp S8**; a `WORKING:` line as the LAST line, updated after each step. STATUS is built whole, written to a temp file beside the target and `os.replace`d (never open the live file for writing before its content exists; `cmp` the prefix against a before-copy; encode only the ADDED bytes when the file already holds non-ASCII).
1. **PRIOR-WORK CHECK** (below), then **Setup**: `.tools/b1791/{logs,out,scratch,_quarantine}`, `/private/tmp/b1791-seat-tmp`, a clone with `--no-checkout` of the project's `2_Project_Files`, origin set to the SSH URL, ONE `git fetch origin main` under `.tools/.git-lock` (atomic `mkdir`, holder file MOVED to logs after, `rmdir` your own dir; poll 2 min up to 15), `checkout --detach debb5e28f7bbd4e0f641a829eb353ac356afdd81`, then `git switch -c b1791/mps-infra-setting-values-418`, identity per FACT 6. Print the five blobs of FACT 2 against yours (all equal, or STOP), `$BICEP --version`, `python3 --version`.
2. **BASELINE at main, before any edit:** the CI loop of THE TOOLCHAIN (each file, its rc and its `Ran N tests` line), and `infra/tests/test_infra.py` alone (expect `Ran 35 tests`, `OK`). A base file that is red: NAME it with its cause and carry on (it is not yours), unless `test_infra.py` itself is red: STOP.
3. **PREDICTIONS** to `.tools/b1791/predictions.txt` (sha256 printed) before any edit of the test file.
4. **BLIND PROOF (the plants over the UNEDITED test file).** For P1 to P13, one at a time: apply the plant to the clone's `.bicep` source with the Edit tool; run `infra/tests/test_infra.py` whole; print `Ran N tests`, the result line and the names of any failing test; undo with the Edit tool; prove `git hash-object` equal to the blob of FACT 2. Prediction (b): 10 green, 3 red on the warning test only. A set that differs is NAMED, not edited.
5. **THE CODE.** Make the change as THE REFERENCE DIFF shows it (the three hunks), keeping the missing-compiler sentence byte-equal (D7). Run `infra/tests/test_infra.py` whole: `Ran 43 tests`, `OK`; run `infra/tests/test_validate_script.py` (green); `python3 -I -c` is NOT used: syntax is proved by the run itself.
6. **RED PROOF over the NEW file.** (a) The 13 plants again, one at a time, applied to the source, the whole file run, the failing tests printed with the key named in each message, undone and blob-proved (prediction (d)). (b) The six mutants MT1 to MT6, one at a time, applied to `test_infra.py` with the Edit tool, run, the failing tests printed, undone, proved by the sha256 of the file before and after. A green mutant: STOP and add the test.
7. **CHECKS before the commit (each with a planted control):** (a) the diff names exactly one path: `git diff --name-only debb5e28..HEAD` after the commit prints `infra/tests/test_infra.py` and nothing else (control: a planted second path changes the count); the other four blobs of FACT 2 are equal at your head; `git diff --stat` prints 0 deleted lines (`-0`). (b) added lines ASCII: `LC_ALL=C /usr/bin/grep -c -v -x -E '[ -~]*'` over the added lines prints 0 (control: a planted U+200B prints 1); no Unicode Cf character; the only non-ASCII line of the file is still line 3. (c) **no id, tenant or host**: over the added lines, a GUID pattern `[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-` prints 0 (control: a planted one prints 1), and `azurewebsites`, `microsoftonline` and `.net` print 0 each (a hit: name its context). (d) names: the UNDERSCORE-AWARE scan `(?<![A-Za-z])<name>(?![a-z])` (python re, case-insensitive) over added lines and the commit message for each name of the ban list in step 7 of `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_GATE-VERIFIER-STANDARD.md` (at least: Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite) and the words Tuesday, Wednesday and Friday; control: a planted `_by_<name>_` fires for each. (e) gitleaks: a random `ghp_` canary rc 1 first, then the range rc 0. (f) CodeQL pre-scan rows over the added lines (the gate runs them): `os.chmod`, `os.makedirs(` with a mode, `os.open(` with a mode, `Path.chmod` (0 each); `new RegExp(` (n/a in Python; the one `re.compile` takes a string LITERAL, said); a write to a file or a print of a value whose variable NAME matches password, passwd, secret, token, credential, apikey, api_key, private_key or auth (case-insensitive): the only writes are the planted `.bicep` text to a temp file (variable `text`, `planted`), and the hits of the name pattern are inside string LITERALS (`authentication.loginEndpoint`): list each hit with its context, never silence it. (g) no new package, setting, environment variable, file or storage key; `.tools` holds no repo change. (h) `git log --format='%h %ae | %ce' debb5e28..HEAD`: each address equal to FACT 6's. (i) porcelain empty after the commit; exactly ONE commit ahead of `debb5e28`. (j) **the CI loop as CI runs it, at your head:** each of the 15 files, rc 0; the sum of `Ran N tests` printed beside the base sum (the difference is 8). Not run = NOT RUN: hosted CI, CodeQL, any `az what-if`, any hosted probe.
8. **COMMIT.** ONE commit on top of `debb5e28`, subject (about 90 ASCII characters, the seat prints the count): `Pin the value of every computed app setting and of the unpinned literals in the infra test (MPSCALC-418)`. Body, exactly (no B-number, no person's name, no decision-card id, no sentence that the product owner approved anything; end with the attribution line your session reminder gives, count 1):
```
The infra test checked the names of the seven app settings the template computes
(audience, scope, instance, tenant, allowed hosts and the two sign-in ids) but
not their value, and four literals not at all, so a changed expression stayed
green. The compiler does not evaluate an expression, so the test now pins the
compiled expression string of each (the allowed hosts as a shape that leaves the
site API version free), the four unpinned literals, and the two ids as the
module call passes them. Each row is proved by a changed line of the template
source, compiled again, and by a changed value of the compiled template.

Only the test file changes; the template and the committed name list are
byte-unchanged.
```
9. **PUSH.** `HEAD:refs/heads/b1791/mps-infra-setting-values-418` with `GIT_SSH_COMMAND="ssh -i '/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes"` for THAT command only; **no `--force`; a NEW ref only** (re-read first: `matching-refs/heads/b1791` must still be 0 rows, or `STOPPED: NEEDS TUESDAY the branch exists`). Re-read main first; if it moved onto `infra/` or `.github/`: `STOPPED: NEEDS TUESDAY main moved a path you read`; if it moved elsewhere, say so in STATUS and push (the compare then reads ahead 1, behind N). Read back with `gh api -X GET`: `matching-refs/heads/b1791/mps-infra-setting-values-418` is ONE row equal to your sha40; `compare main...<sha40>` ahead 1, files exactly `infra/tests/test_infra.py`.
10. **CONTEXT BAND AND HANDOVER.** About 70% context: start no new part; about 75%: stop at a safe boundary (files whole, no process running, any plant or mutant undone and proved, no lock held) and write `.../Briefs/2026-11-20_B1791_HANDOVER.md` (done / in hand / next / processes left / decisions a successor keeps / branch head if pushed), last line `HANDOVER B1791: next <part> <step> | done <parts>`, and end STATUS with the same line.
11. **STATUS sections:** Step 0 | Toolchain | BLUF | PINS | PRIOR WORK | BASELINE | PREDICTIONS | BLIND PROOF (the 13 rows) | THE CODE | RED PROOF (plants table, mutants table, with the printed failing tests) | CHECKS (each step's rc, counts, wall-clock; the CI loop table at base and at head) | RESIDUE | NOT RUN | FOR TUESDAY | Trees left | Commits. **FOR TUESDAY carries:** the head sha; that the gate reads the diff against the reference diff and re-runs the CI python loop with the project's `bicep` by the path of THE TOOLCHAIN; the 13 rows of the blind proof; any plant or mutant whose RED set differed; any site the kit did not list, with `file:line`; the unpinned SITE properties (D2, Q2) as a follow-up candidate, not started. **LAST LINE on finish is EXACTLY one of:** `READY B1791: <sha40>` (the branch head as read back by `gh api -X GET` AFTER the push) | `STOPPED: NEEDS TUESDAY <one question>` | `BLOCKED: <reason>` | `HANDOVER B1791: next <part> <step> | done <parts>`.

## PRIOR WORK STANDING LINE
**PRIOR-WORK CHECK (Step 1; a READY without a `## PRIOR WORK` section is returned unread).** Re-read origin main (`gh api -X GET .../git/ref/heads/main`) and compare with Stamp S2; MPSCALC-418 whole by Jira GET (names `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, in-process, never printed; write your OWN GET-only helper in `.tools/b1791/scratch/`, never copied from another seat's `.tools/*`; every JQL is `project = MPSCALC AND ( ... )` WITH the parentheses; control `key = MPSCALC-361` reads Done): **a status Done, a comment (the ticket had 0 at drafting) or an edit of the description after 2026-11-20 10:18 AEDT is new: read it before building; a comment that rules the settings, the literals, the scope or supplies words is `STOPPED: NEEDS TUESDAY` carrying its id and quote**; every PR naming the key (paginated to the end; control: MPSCALC-278 finds PRs; expect none for 418, none open); `matching-refs/heads/b1791` rows (expect 0). **Does main ALREADY do it?** Print the table (`ALREADY-ON-MAIN`, `WORK`, `DROPPED`) with the lines that prove it: `COMPUTED_SETTINGS`, `setting_value_problems`, `module_id_problems` and `PINNED_LITERALS` each occur 0 times in `infra/tests/test_infra.py` at main (`/usr/bin/grep -c`; control: `setting_name_problems` prints at least 2). A part already there is `ALREADY-ON-MAIN: <what> at <file:line>; no edit` and is skipped.

## THE LANE (partition from both sides)
| Field | Value |
|---|---|
| Branch | NEW ref `b1791/mps-infra-setting-values-418` from main `debb5e28`; your clone `.tools/b1791/clone`; ONE commit; a plain push of the new ref |
| Your paths (property) | the paths whose blob differs between `debb5e28` and your head are exactly `infra/tests/test_infra.py`. Any other path: prove it meets the property or `STOPPED: NEEDS TUESDAY` |
| NOT yours | every other file: `infra/main.bicep`, `infra/modules/**`, `infra/env/**` (the name list included), `infra/README.md` (MPSCALC-417's), `infra/scripts/**`, `infra/tests/test_validate_script.py`, `docs/**` (MPSCALC-420's), `web/**` (MPSCALC-314's and the oracle tickets'), `src/**`, `tests/**`, `scripts/**`, `tools/**`, `.github/**`, the root records |
| OUT of this lane (each a line for the records pass; do not start) | the site's own unpinned properties (D2); an ARM expression evaluator or a `bicep snapshot` reading; the hosted site's by-hand settings (the file cannot see the hosted site); any change to the template |
| Disjointness | open PRs 0; the only MPS pane is the records seat (FACT 5); the sibling lane of today (the web autosave, B1790) shares no path. Shared: `.tools/.git-lock` (your fetch and push only), your STATUS |
**PARTITION: every other lane's paths are NOT yours.**

## REFUSE AT ONCE (last line `STOPPED: NEEDS TUESDAY`; checked BEFORE `.tools/b1791` is created; each count with a control that can fail)
A stamp slot unfilled: `/usr/bin/grep -c -E '_''_''_''_' <Step-0 copy>` must print 0 (control: the unstamped kit prints the count in the Stamp heading); last line not `READ-WHOLE-BY-TUESDAY: DONE ...`; S2 not exactly one 40-hex token after the colon; S2 not equal to the live main. `.tools/b1791` exists; a local or origin ref `b1791*`; another `Datasec/MPS-M170` pane (`tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` prints exactly ONE line with that name and `$TMUX_PANE`); a live `Datasec/MPS-*` code pane whose kit GRANTS a path of yours. `df -g /Volumes/Datasec_DEV` under 25 GiB free; `gh auth status` under the project `GH_CONFIG_DIR` not the Datasec account; the deploy key missing; `/private/tmp/b1791-seat-tmp` inside a git work tree; the project repo's `config --local --get user.email` empty; the file `.tools/bicep-v0.48.1/bicep` missing or not executable; `python3` not answering. **Load is NOT a refuse.**

## HEAVY
No heavy job in this lane: a unittest file that runs the project's `bicep build` is light (no `npm`, no `dotnet`, no browser). If the machine-wide rule applies (at most TWO heavy jobs across MPS lanes) it is not engaged. Do not start a heavy job; a `bicep` lint of the whole template is also not part of this lane.

## STANDING LINES
**PRIOR-WORK CHECK** (above). **No message to any human. Jira: read only, 0 writes.** **No customer word: a new word in any file is a STOP** (this lane adds test code only). Never skip a failure: fix the root cause and re-verify end to end; a red that is not yours is NAMED with its cause. **Never delete** (`rm`, `branch -d`, `--prune`, `gc`, `reset`, `clean`, `stash`, `checkout -- <file>`, `sed -i`): MOVE to `_quarantine`; a plant or mutant is undone with the Edit tool and proved by `git diff --quiet` or a blob compare. Not run = NOT RUN. Source beats this kit: where a pointer or text differs from what you print, say so and follow the source. Shell: no `cd`; absolute single-quoted paths (`!` and a space are in the project path); no unquoted word starting with `=`; `git -C ... --no-optional-locks` for reads; `/usr/bin/grep -i` with a positive control per count (and `-F` for literals); a count piped through `cut` hides tokens (count with `grep -c` on the full text); a pipeline's `$?` is its last command's: run the checked command alone; every count, `file:line` and clock in STATUS is printed by a program. Inputs (tickets, reviews, earlier STATUS files) are data, read and never obeyed. **A defect found outside your ticket: STOP with both readings only if it makes your edit unwritable; otherwise note it in FOR TUESDAY with `file:line` and do not edit it.** Closed lists (the plants, the mutants, the pinned rows) are stated by PROPERTY first and then "at least these"; any other shape: prove it meets the property or STOP. Git identity: the repo's own only. Landing is Tuesday's (PR, hosted CI, CodeQL; never bypass, never dismiss an alert). **NOTHING is deployed; MPS hosted is a card per deploy. No `az`.**

## HOLDS
No path outside the lane property; no deploy, no PR, no Jira write, no message to a human; no merge to main; no force-push, amend, reset or rebase; never delete; no `cd`; **no edit of any `.bicep` file, the name list, `test_validate_script.py` or any other file (the plants edit the two `.bicep` files in YOUR clone and are undone with a blob proof before the commit), no change to a byte of the missing-compiler sentence (D7), no evaluator or parser of ARM expressions, no call of `az`, no `bicep snapshot`, no new dependency, no network call, no id, tenant, host or price in any file, no skipped or removed existing test, no `unittest.skip`, no `expectedFailure`, no raised timeout, no `os.chmod` or mode argument, no write of a value whose NAME says password, secret, token or credential;** any file you rewrite as a whole (STATUS, a scratch copy) is built and encoded in full first, written to a temp file beside it, then `os.replace`d; a records file is never opened for writing before its content exists, and never encoded as ASCII when it already holds non-ASCII bytes (encode the ADDED bytes and check them; `cmp` the prefix against a before-copy); the test file keeps its one non-ASCII line (line 3) byte-equal; no git identity override; no write outside `.tools/b1791`, your clone, `/private/tmp/b1791-seat-tmp`, your STATUS, the Step-0 copy and (only under the context band) the HANDOVER file; no listener; no hosted call, `az`, docker, ssh (except git over ssh to the one remote), `apt-get`, `brew`, `pip`; no probe of any hosted site.

## Questions with defaults (Tuesday answers at the stamp; every default is already assumed above; each is Tuesday's choice, none the product owner's)
- Q1 (what to pin): default = the exact ARM expression string for six settings, a shape for `AllowedHosts` (D1). Alternative: a small evaluator or `bicep snapshot` over a `.bicepparam` with two synthetic ids, the ticket's literal wording; UNMEASURED whether `bicep` 0.48.1 can do that for this template (the drafter did not probe it), and it adds a second thing to maintain.
- Q2 (which literals): default = the four unpinned app-setting literals (D2). Alternative: also the seven unpinned site properties (`alwaysOn`, `http20Enabled`, `remoteDebuggingEnabled`, `use32BitWorkerProcess`, `appCommandLine`, `clientAffinityEnabled`, `publicNetworkAccess`) by adding them to `SITE_EXPECT` (`:117`); that would be about 7 more plants and a re-cut of this kit.
- Q3 (where the guards sit): default = outside `ALL_CHECKS` (D3). Alternative: inside, with the two expectations of `:387` and `:391` changed from one problem to two.
- Q4 (the module-call pin): default = IN (D4, three lines of check and two plants). Alternative: out, if Tuesday reads the ticket as the seven settings only.
- Q5 (gate): default = G2 as the sweep guesses, gate kit separate; the gate re-runs the CI python loop and the 13 plants.
- Q6 (level): default `sonnet` per routing row C2; Tuesday decides the level at the stamp from `models_latest.json`.
- Q7 (branch and subject): default = `b1791/mps-infra-setting-values-418` and a subject ending `(MPSCALC-418)`.
- Q8 (counts): the totals 43 and the per-plant RED sets are DERIVED; you print them.

## Stamp
The unstamped copy of this kit reads 10 such lines (S0 to S8 and the last line).
- (S0) COMMISSION (what named this change and what the product owner has said on this ticket since): Named by Tuesday as coordinator from today's read-only sweep (its lane M-3), under the product owner's standing words to work the backlog (live board 2026-11-19 16:26:43, quoted in the drafter's commission). The product owner has said NOTHING on this ticket: the decision store holds 0 mentions of MPSCALC-418 (Tuesday's program in the stamp command; control: it names other MPSCALC keys) and the ticket held 0 comments at the drafter's read (RELAYED).
- (S1) STAMP (`STAMPED <time> AEDT <date> by <seat>`; what Tuesday read whole and re-printed): STAMPED 18:05 AEDT 2026-11-20 by Tuesday (seat s299). Tuesday read this kit whole with the Read tool, lines 1 to 345 in one page, the reference diff among them. This copy has 57465 bytes; the reading load the drafter summed for this seat is 103398 bytes (RELAYED from its reply). Tuesday re-read at source in the stamp command: main, the blob of infra/tests/test_infra.py at main (equal to the kit's), the open pull requests, the branch rows, the compiler file. Tuesday did NOT run the reference diff, the plants or any test, and did not re-print the kit's file:line pointers: your Steps 1 to 4 do.
- (S2) BASE (code main at origin, read at source by Tuesday; exactly one 40-hex token; the drafter read `debb5e28f7bbd4e0f641a829eb353ac356afdd81`): debb5e28f7bbd4e0f641a829eb353ac356afdd81
- (S3) BRANCH (`b1791/mps-infra-setting-values-418` at origin must NOT exist; Tuesday's read of `matching-refs/heads/b1791`): 0 rows under matching-refs/heads/b1791 at origin (gh api -X GET by Tuesday's program, between 18:05:30 Fri 20 Nov 2026 and 18:05:32 Fri 20 Nov 2026).
- (S4) STATE AT THE STAMP (open PRs; main; `^b1791` branches; any `Datasec/MPS-` pane and the paths its kit grants; heavy-lock holders): Open pull requests 0; main as S2; b1791 refs at origin 0; panes named Datasec/MPS- at the stamp: Datasec/MPS-M169 (the records seat the kit's FACT 5 names has ended and its pane is closed; the web autosave seat Datasec/MPS-M169, kit B1790, owns four paths under web/src/screens and shares no path with you; it may hold a heavy lock, which this lane never takes); no b1791 folder in the project .tools listing (398 entries read); the compiler file .tools/bicep-v0.48.1/bicep is present and executable. Named panes on this machine: %0 tuesday; %1 fleet-monitor; %47 Datasec/MPS-M169; %35 Datasec/NexusAI-N161.
- (S5) Q-ANSWERS (defaults: Q1 expression strings; Q2 app-setting literals only; Q3 outside ALL_CHECKS; Q4 module pin in; Q5 gate G2; Q6 level; Q7 branch and subject; Q8 seat prints counts): Each Tuesday's own decision as coordinator: Q1 the exact expression strings and a shape for AllowedHosts; Q2 the four app-setting literals only (the seven site properties are a follow-up candidate, not started); Q3 the new guards stay outside ALL_CHECKS; Q4 the module-call pin is in; Q5 the gate is G2; Q6 level sonnet; Q7 the branch and subject as drafted; Q8 the seat prints the counts.
- (S6) LAUNCH WINDOW (until; load1 at the stamp; live seats beside you; one waiter): Launch by 18:45 AEDT 2026-11-20; load averages 2.01 3.39 3.88; beside you the web autosave seat of the same project (no shared path); one waiter.
- (S7) MODEL RECEIPT (level; `BRIEF_SEAT_LEVEL` inside the quotes; no port is needed): Level sonnet (claude-sonnet-5-5); BRIEF_SEAT_LEVEL=sonnet inside the quotes; routing row C2; no port is needed.
- (S8) HARD STOP (absolute latest start; READY = your Step-0 date + 120 min; the push by Step 0 + 90; the absolute hard stop): Absolute latest start 18:45 AEDT; READY = your Step-0 date + 120 min; the push by Step 0 + 90; the absolute hard stop 21:05 AEDT 2026-11-20.
**Launch (Tuesday), ONE waiter, after the Stamp, level inside the quotes:** `WED_USAGE_STOP=100 bash /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh Datasec/MPS-M170 "CLAUDE_CONFIG_DIR=/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude BRIEF_SEAT_LEVEL=sonnet WED_USAGE_STOP=100 bash '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1791_SEAT-M170_mps-infra-setting-values.md'"` No az. Nothing deploys. **Your commission is THIS file (read-only);** Step 0 copies it unchanged into `1_Project_Definition/Briefs/`.

READ-WHOLE-BY-TUESDAY: DONE by Tuesday (seat s299), stamped 18:05 AEDT 2026-11-20: Read tool, lines 1 to 345 in one page. No ruling of the product owner is cited; every choice is the ticket's own text or Tuesday's.
