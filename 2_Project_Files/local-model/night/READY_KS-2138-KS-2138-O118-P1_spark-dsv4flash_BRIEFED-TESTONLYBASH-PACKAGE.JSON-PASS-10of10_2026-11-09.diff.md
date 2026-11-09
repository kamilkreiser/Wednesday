# READY - KS-2138-KS-2138-O118-P1 (Spark (DeepSeek V4 Flash), briefed, test_only_bash/plant) - PASS 10/10 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2138_o118_p1_react_router_portals_suite_misses_bundledependencies_and_name_at_range_override/out.md.checker/patch.diff` (from `ls` at 18:18 2026-11-09; sha256[:16] d9736df55cf0e122, 2325 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 18:18 2026-11-09 by Wednesday after a source read (hold_ready.py, test_only_bash path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2138_o118_p1_react_router_portals_suite_misses_bundledependencies_and_name_at_range_override/out.md.checker`; product and plant-file bytes were RE-MEASURED here.** Tip `e8d23ce366e292ed6ca13f296cc2cfb2a3796496`. Brief: not given (--brief) and not located
- Touched set [patch.diff `+++` headers == sections.json == `git apply --numstat` == input.json test_files; no product or plant file named]: ['Blockchain/Dev/scripts/__tests__/react_router_v7_portals.test.sh']; `+` lines 8 (ASCII), `-` lines 1.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/frontend/admin/package.json` blob 4f830f220c28, `Blockchain/Dev/frontend/verifier/package.json` blob d014d0d80c36; plant file(s) also unchanged.
- Red cells [input.json]:
  - `real tree: R0-R4 and G1-G5 all hold`
- Red evidence under the plant [red_with_plant__*.out, the suite's own FAIL line per red cell, verbatim]:
  - `FAIL real tree: R0-R4 and G1-G5 all hold`
- Plant file(s) [input.json plant_diff / plant; applied in the checker's clone only]: ['Blockchain/Dev/frontend/admin/package.json', 'Blockchain/Dev/frontend/verifier/package.json']
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/scripts/__tests__/react_router_v7_portals.test.sh)`
  - `PASS A3p the plant applies at the tip (golden_red.diff)`
  - `PASS A3s every patched suite parses (bash -n)`
  - `PASS A4 GREEN WITHOUT PLANT: 1 named cell(s) exist and pass on the unmodified product; declared suites 27 cells, 0 red, rc [0]`
  - `PASS A6 WHOLE SUITE no worse: declared cells 25 -> 27 (none lost); 8 sibling suite(s) 233 -> 233 cells, FAIL lines 0 -> 0`
  - `PASS A5 RED WITH PLANT: 1 named cell(s) print the suite's own FAIL line under the plant (Blockchain/Dev/frontend/admin/package.json, Blockchain/Dev/frontend/verifier/package.json) and pass without it; rc [1]; e.g. react_router_v7_portals.test.sh: FAIL real tree: R0-R4 and G1-G5 all hold`
  - `PASS A8 RESTORE: 3 watched file(s) back at their tip sha256; tracked tree clean`
- Checker INFO lines [checker.out, verbatim]:
  - `INFO baseline at the tip: declared suites 25 cell(s), 0 FAIL line(s), rc {'Blockchain/Dev/scripts/__tests__/react_router_v7_portals.test.sh': 0}; 8 sibling suite(s) 233 cell(s), 0 FAIL line(s)`
  - `INFO named cell(s) already present at the tip (changed in place, or the gap is already pinned): ['react_router_v7_portals.test.sh :: real tree: R0-R4 and G1-G5 all hold (SCANNED files=168 locks=4)']`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_bash)`

**PR NOTES for the raise seat:** TEST_ONLY_BASH (plant shape) - bash suite bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief plant (checker clone only), not a change in the PR. DOES NOT PROVE the plant is the regression that matters, or that a cell catches a different fault; an INFO line above is the checker's own note and is not a leg. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/scripts/__tests__/react_router_v7_portals.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/react_router_v7_portals.test.sh
@@ -70,7 +70,8 @@
   // dependency map and every key of overrides at any depth. (The react-router floor check below keeps reading deps, as before.)
   const okeys = (o, acc = []) => { for (const [k, v] of Object.entries(o || {})) { acc.push(k); if (v && typeof v === 'object') okeys(v, acc); } return acc; };
   const domIn = ['dependencies', 'devDependencies', 'optionalDependencies', 'peerDependencies'].filter((m) => 'react-router-dom' in (pj[m] || {})).map((m) => `${m} ${pj[m]['react-router-dom']}`);
-  if (okeys(pj.overrides).includes('react-router-dom')) domIn.push('overrides');
+  if (okeys(pj.overrides).some((k) => k === 'react-router-dom' || k.startsWith('react-router-dom@'))) domIn.push('overrides');   // KS-2138 item 3 (gate 260): npm accepts a name@range key
+  if ([].concat(pj.bundleDependencies || [], pj.bundledDependencies || []).includes('react-router-dom')) domIn.push('bundleDependencies');   // KS-2138 item 4 (gate 260): a bundled dependency is a dependency
   if (domIn.length) out.push(`R2 ${a}: package.json still names react-router-dom in ${domIn.join(', ')}`);
   if (!floorOk(parse(deps['react-router']))) out.push(`R2 ${a}: react-router spec ${JSON.stringify(deps['react-router'])} is not in [7.18.2, 8)`);
 }
@@ -199,6 +200,12 @@
 mutant "R1 a .cjs file requires react-router-dom"           R1 m_cjs
 mutant "R1 a .cts file imports react-router-dom"            R1 m_cts
 
+# KS-2138 items 3 and 4 (gate 260): two plants the checker above did not see. Each cell fails ("mutant left R2 green") until the checker reads them.
+m_bundle()    { jsonmut "$1/frontend/verifier/package.json" 'd.bundleDependencies=["react-router-dom"]'; }
+m_overat()    { jsonmut "$1/frontend/admin/package.json" 'd.overrides={"react-router-dom@6":"^6.30.4"}'; }
+mutant "R2 react-router-dom listed under bundleDependencies"   R2 m_bundle
+mutant "R2 react-router-dom as a name@range overrides key"     R2 m_overat
+
 # ---- GREEN-before pins: proven only by a named mutant -------------------------------------------
 g1() { textmut "$1/frontend/admin/src/App.tsx" ' basename="/admin"' ''; }
 g2() { textmut "$1/frontend/verifier/src/App.tsx" ' basename="/verify"' ''; }
```
