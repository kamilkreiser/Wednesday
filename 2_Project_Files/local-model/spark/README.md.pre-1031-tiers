# spark/ — the durable Spark round runner (2026-10-05)

Runs Secuura briefs through the Spark (DeepSeek V4 Flash, `http://127.0.0.1:47788`, OpenAI-compatible, ONE request at a
time, thinking OFF) without any session scratchpad, so it survives seat rotation. It replaces the scratch
`mksrc.sh` / `linknm.sh` / `mkclone.sh` / `precheck.sh` (CONTROL half) / `ap.sh` that were rebuilt at every rotation
(IMPROVEMENTS 2026-09-27 19:22, 2026-10-04 19:0x, 2026-10-05 02:3x). It reimplements no builder and no checker: it
sequences `night/build_input.sh`, `tasks/bash_patch/build_bash_input.sh`, `tasks/code_patch/prepare_clone.sh`,
`local_model_task.sh` (LM_BACKEND=spark), `tasks/code_patch/spark_checker.sh`, `tasks/bash_patch/checker.sh` and
`tasks/code_patch/a2a_anchor.py`.

| file | what |
|---|---|
| `round.sh <brief_dir> [--dry-run\|--control] [pin=value ...]` | one round for one brief; prints ONE `SPARK ROUND <tag>: ...` verdict line last |
| `queue.sh [--max N]` | drains `queue.md` one round at a time, appends a row per round to `done.md`, exits when empty |
| `brief_lint.py` | the brief gate round.sh runs first |
| `queue.md` / `done.md` | the queue (format in its header) / the results (`done.md` is created by the first drain) |
| `tests/arms.sh` | refusal, endpoint-down, dry-run, busy, queue and ONE real round |
| `tests/code_patch2_arms.sh` · `tests/bash_patch2_arms.sh` | the multi-file tiers (rung 3): red-proof arms, synthetic repos in scratch |
| `tests/test_only_arms.sh` | tier test_only (2026-10-18): ks_1614_p1 control PASS, tampered goldens FAIL, product-touching briefs REFUSED, old-vs-new lint + dry-run regression |
| `cache/` (gitignored) | `src/` = the durable cache clone of the Secuura repo; `work/<run-id>/clone` = per-round clones |
| `state/` (gitignored) | `round.lock`, `queue.lock`, `dry/` inputs, `last_round.json`, `queue.log`, `stale_locks/` |

## Queue a brief

1. The brief dir holds exactly one `KS-<n>.md` in the kit-03 shape (`File:`, `Tip:`, `Runner:` header lines; `## The mode`,
   `## What is wrong`, `## The exact change`, `## The test` or `## Self-testing`, `## UNMEASURED`, `## Scope`, `## Output`),
   optionally `golden.diff` (compared byte for byte with the model's patch) and `spark.pins`.
2. Pins the builder needs go in `<brief_dir>/spark.pins` (or on the queue line): e.g. bash_patch needs
   `ref=<an existing *.test.sh>`; code_patch usually `ref=`, `test_file=` (in-place test), `line=`. `product=` defaults to the
   brief's `File:` line. Round-only pins: `tier=code_patch|bash_patch` (else from `Tier:` / `Runner:`), `allow_drift=1`.
3. Prove it builds: `bash local-model/spark/round.sh <brief_dir> --dry-run [pins]` (no model call). Prove the golden passes the
   checker: `round.sh <brief_dir> --control [pins]` (no model call; run dir `..._<tag>-control`).
4. Append `<brief_dir> [pins]` to `queue.md` (a relative dir resolves against `local-model/night/briefs/`).

## Run the loop

    nohup bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/queue.sh \
      >> /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/state/queue.log 2>&1 &

One drainer at a time (`state/queue.lock`); one round at a time (`state/round.lock`, also taken by a hand-run
`round.sh` — the queue waits for it). It stops, leaving the line queued and printing `!!!!! SPARK QUEUE STOPPED`, when the
endpoint is down (round.sh rc 4) or free space on the runs volume is under `SPARK_MIN_FREE_GB` (20).

## Read results

- `done.md`: `| when | tag | verdict | round s | model s | tokens | golden | run dir | queue line |`.
- The run dir `local-model/runs/spark_secuura_<date>_<tag>[-rN]` has the 10-05 shape: `input.json`, `out.md`
  (+`.meta.json`, `.raw.json`), `run.log`, `checker.out` (ends `RESULT:` then `SPARK RESULT:`), `out.md.checker/`
  (`patch.diff`, `section_*.diff`, `a2a_anchor.out`, ...), `prepare_clone.out` (code_patch), plus `build_input.out` and
  `round.json` (verdict, tip, golden, walls, tokens, work dir).
- bash_patch now gets the A2a anchor leg automatically (`sections_with_n.json` + `a2a_anchor.py`, as done by hand 09-30/10-05).
- Exit codes: 0 PASS · 1 FAIL · 2 REFUSED · 3 BUSY · 4 ENDPOINT DOWN · 5 HARNESS (not a model verdict) · 64 usage.

## What it refuses

- a brief dir without exactly one `KS-<n>.md`, or missing a required header line / heading;
- a brief naming a client other than Secuura (`Client:` line, a `!CODING/<other>/` path, another client's name);
- a tier other than code_patch / code_patch2 / bash_patch / bash_patch2 / test_only (2026-10-18; see Tiers — the
  separate tasks/test_only/ builder, `## Tampers` with `### <ID>` entries, is still NOT wired here);
- a STALE brief: a file it names changed between its `Tip:` and today's develop (override `allow_drift=1`);
- anything the builders refuse (rc 2), and a code_patch input that did not use the brief as the prompt;
- a round when the endpoint is down, or another round holds the lock.

## What it does NOT do

It never raises a PR, pushes, merges, posts to Linear/GitHub, or writes a READY. A local PASS is a candidate: Wednesday
reads the diff against the brief and holds it (`night/hold_ready.py`), and a Claude seat raises it. It never restarts the
tunnel or the box. It never writes under `!CODING/` (git read verbs there; the cache is a `--no-hardlinks` copy and
node_modules are symlinked FROM the Secuura checkout INTO the cache). It never deletes: per-round clones (~335 MB each)
accumulate in `cache/work/`; quarantine old ones by hand (`mv cache/work/<old> <dated quarantine>`), the queue stops
before the disk fills.

## Tiers

- `code_patch` — 1 product + 1 test (tasks/code_patch). `bash_patch` — tasks/bash_patch.
- `code_patch2` (2026-10-05, rung 3) — 1-3 products + 1-2 tests (new or modified), declared by the brief header's
  `File:` and `Test …:` lines. Select with `tier=code_patch2` or `Tier: \`code_patch2\``. Input: tasks/code_patch2/
  build_input2.sh (night/build_input.sh for the first product, then the declared set). Task text: code_patch's task.md
  with rules 3/4 replaced at run time (make_task.py, written into the run dir). Checker: tasks/code_patch2/checker.sh —
  code_patch's checker runs unchanged through A2, then A3 = the declared set exactly, A4 = all test sections with no
  product section must red by assertion, A5 = all product sections green, A6/A7 as code_patch; the predicates are read
  out of code_patch/checker.sh at run time, not copied. Arms: tests/code_patch2_arms.sh.
  Since 2026-10-07 it also has **A3x** (tasks/code_patch2/brief_bytes.py): per declared file, its '+' lines equal the
  brief's byte for byte, in order — a NEW test given whole under `## The test` included (A3c's stripped multiset and
  A3i could not see a one-byte change there; the KS-1278 r3 review byte-compared it by hand). Arms C6/C7.
- `bash_patch2` (2026-10-07, rung 3) — 1-3 scripts + 1-4 `*.test.sh` suites. The brief HEADER declares them: `File:`
  lines = products; `Test …:` lines each say `NEW|MODIFIED` and `RED|SUPPORT` (RED = fails with the test edits alone,
  passes after; SUPPORT = an existing suite edited to the new contract, green both ways; >= 1 RED; a NEW suite is RED).
  Product hunks go under `## The exact change`, test hunks under `## The test`, every fence line attributable by its
  `+++ b/<path>`. Select with `Tier: \`bash_patch2\`` or `tier=bash_patch2`; `ref=` is still required (any existing suite
  in the tests' dir; it may be a declared one). Input: tasks/bash_patch2/build_bash_input2.sh (bash_patch's builder
  unchanged for the first product + first RED test, then the declared set). Task: bash_patch's task.md with the
  one-script clauses replaced (tasks/bash_patch2/make_task.py, into the run dir). Checker: tasks/bash_patch2/checker.sh —
  bash_patch's checker unchanged through B2 (a sentinel test stops it at B3 before anything applies), then B3 = the
  declared set exactly, B3b sites/A3c/A3d over the products, B3x byte identity, B4 every RED red + every SUPPORT green
  with all test sections and no product, B5 all green with every product, B6 undeclared suites naming a product's STEM no
  worse (before/after counts), B7 shellcheck info. Arms: tests/bash_patch2_arms.sh (22). First brief: KS-1274.
- `test_only` (2026-10-18) — code_patch's TEST-ONLY mode, nothing new: the code is right at the tip and a pin is owed.
  Header: `File:` = the product (the tamper target, NOT modified) + exactly one `Test file:`; the brief carries ONE
  `## Tamper` block (`line: N` / from: `` `<tip line>` `` / to: `` `<line>` ``, + `statement_ok:` when mid-statement) and
  `## Red cells`; `## The test` is not required. Select with `tier=test_only` (or `Tier: \`test_only\``, or a
  `## Tamper` heading with no Tier line). Input: night/build_input.sh (as code_patch; round.sh REFUSES if it parsed no
  tamper). Task: tasks/code_patch/task.md. Checker: tasks/code_patch/spark_checker.sh, which runs checker.sh in
  MODE=test_only (A3 the one test only, A4 red under the planted tamper, A5 green at the untouched tip). Lint refuses
  a diff file header naming any other file (the product above all) in `## The exact change` fences or golden.diff.
  Arms: tests/test_only_arms.sh. First brief: night/briefs/ks_1614_p1.
- A brief whose header says NOT RUNNABLE is refused unless pinned `override_not_runnable=<reason>` (recorded in
  round.json); a header declaring more files than the tier's contract is refused.
- `golden` in round.json / done.md: `BYTE-IDENTICAL` (cmp), else `TREE-IDENTICAL` (2026-10-07: both diffs applied
  strictly to a temporary index of the tip give the same tree — a differently written but equal diff, e.g. a git-form
  golden), else `DIFFERS`.

## Base and node_modules

The base is develop as `git -C <Secuura checkout> ls-remote origin refs/heads/develop` reads it (override `SPARK_TIP`).
The cache's origin is set to the checkout's own GitHub origin + `core.sshCommand`, so the builders' own `ls-remote origin`
agrees with it (the 09-29 / 10-01 stale-origin fault). Every first-level `node_modules` under `Blockchain/Dev` in the
checkout is symlinked into the cache except `SPARK_NM_EXCLUDE` (default `services/billing`: its own lock's modules make
tsc fail, IMPROVEMENTS 2026-10-01). Whether a service's own lock is right for a given tip is per-service and measured,
not assumed (nft-certificate needed its own on 10-01).
