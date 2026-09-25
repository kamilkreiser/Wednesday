--- comment 5833291505 by linear[bot] at 2026-09-25T13:34:37Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1111/k6-echo-mask-reads-one-argument-of-lookbehind-a-flag-value-that-looks">KS-1111 k6 echo mask reads one argument of lookbehind — a flag value that looks like an env flag prints the next env assignment in clear (QA-961-1..3; two regressions from #961)</a></summary>
<p>

## BLUF

PR #961 (KS-1098) masks every single env spelling docker and k6 accept: 51 of 51 rows, 27 of which printed in clear at base. Its tier-2 QA gate (GO WITH FINDINGS at `644965d9095a962e783bd3d16fef588301c1ede6`) found three latent gaps in `systemTest/performance/runner/k6_docker.ts`, all in one function and fixable in one pass.

* **All three need an argv that no caller builds today:** `cli.ts:221` hard-codes `extraFlags: []`, and `buildEnvFlags()` (`env_flags.ts:143`) emits only `-e NAME=VALUE` pairs.
* **Two of QA-961-1's seven leaking argvs (L02 and L03) were masked at base and print in clear at head.** They are latent regressions introduced by #961.
* **The JSDoc claim at** `k6_docker.ts:141` ("read the way docker and k6 read flags") does not hold for these argvs.

## Recommendation

One fix in `runner/k6_docker.ts` plus its test rows, proven by one pass of the unit suite with the new rows red first:

1. **QA-961-1.** When the lookbehind branch matches, also apply the `--env=` and attached-short-flag masks to the current argument if `maskEnvAssignment` leaves it unchanged. That is the gate's fix-shape (a), recorded here as the gate's proposal, not a ruling. The alternative is (b): narrow the JSDoc. Either way, add the gate's three rows.
2. **QA-961-2.** Add rows for `-Pe NAME=VALUE` and `-diteNAME=VALUE`. Add one row asserting that `-l SECRET_NAME=VALUE` prints in clear, or drop that JSDoc line.
3. **QA-961-3.** Add to the JSDoc's does-NOT-cover list: a token docker or k6 rejects is printed verbatim by the tool itself.

## Detail

**Source:** `Testing Agent MAIN/projects/secuura/reports/2026-09-12-ks1098-961-644965d90-tier2-r1/report.md` (FINDINGS, COVERAGE MAP, NOT TESTED).

### QA-961-1 · Minor (latent)

* **Where:**
  * `runner/k6_docker.ts:171-172` — the lookbehind branch returns `maskEnvAssignment(arg)` and never tries the one-argument forms;
  * `:97` — `ENV_SHORT_FLAG_TWO_ARG`;
  * the JSDoc claim at `:141`.
* **Mechanism:**
  * The previous argument (`-e`, `-one`, `-qe`) is really the VALUE of `--label`, `-a` or `-u` to the real parser.
  * But it matches `ENV_SHORT_FLAG_TWO_ARG`, so the current argument goes to `maskEnvAssignment()` whole.
  * The "name" it reads is then `--env`, `-qe`, `-e` or `-eKEY`, which no clause of `SECRET_ENV_NAME` matches, so the value prints.
* **Measured** against docker CLI 28.4.0 (a loopback create-recorder) and `k6 archive` v1.6.1:

| row | argv tokens | accepted by | echo at head | echo at base |
| -- | -- | -- | -- | -- |
| L01 | `--label -e --env=NAME=VALUE` | docker | clear | clear |
| L02 | `--label -one --env=NAME=VALUE` | docker | clear | masked (regressed) |
| L03 | `--label -qe -eKEY=VALUE` | docker | clear | masked (regressed) |
| L04 | `-e -e -eKEY=VALUE` | docker | clear | clear |
| L05 | `--label -one -qe=NAME=VALUE` | docker | clear | clear |
| L07 | `-a -e --env=NAME=VALUE` | k6 | clear | clear |
| L08 | `-u -qe -e=NAME=VALUE` | docker | clear | clear |

* **Control:** L06 (`--label -one -e NAME=VALUE`) is masked on both sides.
* **The gate's fix-shapes:**
  * (a) mask every interpretation of the argument, not only the first;
  * (b) narrow the JSDoc;
  * (c) structural — pass bare `-e NAME` and give `spawnSync` an `env` carrying the values (the #958 gate's O-1).
* **The gate's regression rows:** `['--label', '-one', '--env=NAME=VALUE']`, `['--label', '-qe', '-eKEY=VALUE']` and `['-u', '-qe', '-e=NAME=VALUE']`. Each asserts that the echo lacks the value and the argv keeps it.

### QA-961-2 · Polish

Three shapes the code covers have no pinning row. Each of the gate's tampers Q1–Q3 left 1027/1027 green while the echo measurably changed:

* **Q1** narrowed the two-argument cluster, so `-Pe`, `-dite` and `-qqe` printed in clear.
* **Q2** narrowed the attached cluster, so `-Pe…` and `-qPe=…` printed in clear.
* **Q3** made every short flag's value masked, which masks a secret-named `-l` label. That contradicts "Does NOT cover: non-env arguments".

### QA-961-3 · Polish (latent)

* **The leak:** when docker or k6 REJECTS a token, its own error output prints the token verbatim to the inherited terminal (`stdio: 'inherit'`). That bypasses both the mask and the run-log tee.
* **Measured:** 12 docker rows and 7 k6 rows. In 11 of them, the runner's echo had masked the value.
* **Control:** on every row where a tool ACCEPTED a secret-named env assignment, its output carried the value 0 times.
* **The structural fix** is QA-961-1 (c).

### Not covered by the gate

* a live k6 or docker run, or dockerd itself;
* the k6 2.1.0 image's flag set;
* node ≥24.11.0, and Linux;
* process-table exposure of the argv values.

### Dedupe, before filing

Searched this board by symbol and path:

* `maskEnvAssignment`, `extraFlags` and `k6DockerRedaction`: KS-1098 only.
* `lookbehind`, `QA-961` and `ENV_SHORT_FLAG`: 0 hits.
* `k6_docker.ts`: KS-1098, plus five slot-isolation tickets (KS-1066, KS-971, KS-687, KS-1056 and KS-706), none of them about the mask.

**Related:** KS-1098 (PR #961) and KS-1094.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1111-echomask-mask-every-interpretation-of-an-argument-behind-a-193de3cdb3a6">Review in Linear</a></p>

