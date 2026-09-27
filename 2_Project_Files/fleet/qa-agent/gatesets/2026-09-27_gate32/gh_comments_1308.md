--- comment 5854786691 by linear[bot] at 2026-09-27T09:47:34Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1108/akto-harness-loadsecretsyml-parses-configsecretsyml-with-no-catch-the">KS-1108 Akto harness: loadSecretsYml() parses config/secrets.yml with no catch — the KS-1099 shape, whole-file print not yet measured in this package</a></summary>
<p>

## BLUF

* The Akto harness has the same unguarded YAML load that KS-1099 fixes in the k6 runner. `systemTest/akto/src/config/secrets.ts:40`, inside `loadSecretsYml()`, returns `loadYaml(fs.readFileSync(filePath, 'utf-8'))` with no catch.
* In the k6 runner that shape printed the **whole** secrets file when the YAML was malformed. js-yaml's `YAMLException` holds the entire source in `err.mark.buffer`, and Node's uncaught-exception print inspects the error. For an unquoted value that starts with `!` or `*`, `err.reason` carries the value itself. Measured by s190 on sentinel fixtures (js-yaml 5.2.3, node v24.7.0).
* **The whole-file print is NOT measured in this package.** Akto's js-yaml version is unread, `loadSecretsYml()`'s callers are not traced, and nothing was run under `systemTest/akto`. The exposure is likely, not established.

## Recommendation

Measure first in this package: the installed js-yaml version, and what an uncaught parse failure of `config/secrets.yml` prints. Then apply the KS-1099 shape: sanitise where the file is parsed, name only the path, line and column (never `err.reason`, `err.message`, `mark` or `cause`), and pin it with a sentinel-fixture unit test that asserts on `util.inspect(err)`, which is what Node prints.

## Detail

* **Separate fix, separate ticket.** Kam, 2026-09-07 13:23: "The only reason to create multiple tickets is if they relate to separate workloads or separate fixes." This is another package, with its own suite.
* **How it was found.** s190's KS-1099 ITEM 0 mapped every YAML load under `systemTest/performance/`. The same shape turned up here, outside that package. Filed on Wednesday's ruling (ANSWER to the s190 plan confirmation, 2026-09-12). Not fixed in that round.
* **Dedupe before filing.** Searched titles, descriptions and comments, archived included, for `loadSecretsYml`, `akto/src/config/secrets.ts` and `SECRETS_FILE_RELATIVE`: 0 hits for `loadSecretsYml` and for `akto/src/config/secrets.ts`. `SECRETS_FILE_RELATIVE` hit only KS-494 (Done, archived), the `findRepoRoot()` path-doubling defect, whose description does not mention a parse failure. Controls: `config_loader.ts` and `YAMLException` each returned KS-1099.
* No credential value appears here.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1108-name-the-file-and-position-when-aktos-secretsyml-will-not-c232831c8da9">Review in Linear</a></p>

