--- comment 5827587720 by linear[bot] at 2026-09-25T05:57:41Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1110/two-k6-unit-tests-parse-configscenariosyml-with-js-yaml-directly">KS-1110 Two k6 unit tests parse config/scenarios.yml with js-yaml directly, bypassing readYaml(), so a malformed scenarios.yml prints its lines into the test output (QA-960-2)</a></summary>
<p>

## BLUF

* **Two unit tests in** `systemTest/performance` **parse** `config/scenarios.yml` **with js-yaml directly, bypassing** `readYaml()`**, the KS-1099 sanitiser.** On a malformed `scenarios.yml`, their failure output carries the lines around the error.
* **The gate rated it Polish, because only a tracked, credential-free file is involved.** No secrets path reaches these tests.
* **It is pre-existing.** Both tests are identical at develop `4554b25e21dfd01113bf40e8f6d34573345a5f37`, before #960.
* **Found by** the tier-2 QA gate on PR #960 (KS-1099).

## Recommendation

* **Import** `readYaml` **from** `utils/yaml.ts` **in both tests.** It returns the same data: the gate measured the canonical sha of `scenarios.yml` through `readYaml` as equal to a direct js-yaml parse, at both SHAs.
* **Add a source-text guard** that js-yaml is imported only by `utils/yaml.ts`, with that import as its positive control.
* **Why a separate ticket from QA-960-1/3/4:** the files and the fix are both separate. The fix-shapes are the gate's proposals, not rulings.

## Detail

**Source:** the tier-2 gate report `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-12-ks1099-960-0e70ed1c7-tier2-r1/report.md`, verdict GO WITH FINDINGS at `0e70ed1c77e1f832a4ab165152e024926be509a0`. Line numbers are at that SHA and identical at develop `4554b25e2`.

### QA-960-2 · Polish · two unit tests bypass `readYaml()`

* **Where:**
  * `tests/unit/config/sheddingCeiling.test.ts:29` imports `* as yaml from 'js-yaml'`, and `:46` calls `yaml.load(readFileSync(join(perfRoot, 'config', 'scenarios.yml'), 'utf8'))`.
  * `tests/unit/package_scripts.test.ts:21` imports `{ load as loadYaml } from 'js-yaml'`, and `:44` calls `loadYaml(raw)`.
* **Census (PROBED):**
  * At the head, js-yaml is imported at exactly 3 sites under `systemTest/performance`: these two and `utils/yaml.ts:12`.
  * All 6 product YAML loads go through `readYaml()`:
    * `runner/cli.ts:130`, `:131` and `:132`, via `loadConfig`;
    * `runner/cli.ts:180`, via `loadSecrets`;
    * `runner/setup.ts:80`, via `loadConfig`;
    * `gate/cli.ts:48`, directly.
* **Evidence (MEASURED AT RUNTIME):** the full unit run with a malformed `config/scenarios.yml` (sentinels on lines 2, 35 and 37, bad indentation on line 36).
  * 3 files failed, and 1023 tests ran instead of 1032: `package_scripts.test.ts` fails at collection.
  * The failure messages and stderr of `sheddingCeiling.test.ts` and `package_scripts.test.ts` carried js-yaml's snippet. The near and after sentinel lines appeared 4 times each; the far one 0 times.
  * `ciGate.test.ts`'s 18 failures carried 0 sentinels, so the sanitiser works through that spawn.
* **Severity:** Polish, the gate's rating.
* **Regression test (gate proposal):** a source-text guard that js-yaml is imported only by `utils/yaml.ts`.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1110-readyaml-both-k6-unit-tests-parse-scenariosyml-through-4089fc1bf03e">Review in Linear</a></p>

