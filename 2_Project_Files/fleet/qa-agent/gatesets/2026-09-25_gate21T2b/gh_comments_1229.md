--- comment 5827026819 by linear[bot] at 2026-09-25T04:59:32Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-865/check-no-latest-tagssh-silently-skips-a-missing-input-it-scans-5-of">KS-865 check-no-latest-tags.sh silently skips a missing input — it scans 5 of the 6 files it advertises and still prints OK</a></summary>
<p>

## BLUF

`Blockchain/Dev/scripts/check-no-latest-tags.sh` **cannot fail on one of the six files it claims to check**, and says nothing about it. A check that cannot fail is indistinguishable from a check that passed.

Found by the KS-490 (3) tier-2 gate on PR #852 — the same gate this script was used as evidence in, which is what makes it worth fixing.

## Mechanism

`CHECK_FILES` lists `.github/workflows/deploy-staging.yml`. The script `cd`s to `Blockchain/Dev`, where that path **does not exist** (the workflows live at the **repo root**). Line 42's `[ -f "$f" ] || continue` skips it **silently**, and the gate prints `OK`.

**Scanned: 5 of the 6 advertised.**

## Why it matters here specifically

This script is on the push preflight and was cited as passing evidence on #852 — where its pass *was* meaningful, because the file under test (`main.parameters.json`) is one of the five it really reads. But the sixth has been unchecked for as long as the list has been wrong, and nothing in its output says so.

## Acceptance

A listed input that is missing is an **error**, not a skip — or the path is corrected to the repo root and the file is actually scanned. Either way the script **reports how many of the advertised files it examined**, so an examined-nothing run cannot read as clean. Same shape as KS-676, where a `mapfile` under bash 3.2 made a CVE scan examine 0 of 34 images and report clean.
</p>
</details>
<details>
<summary><a href="https://linear.app/secuura/issue/KS-808/run-migrationssh-exits-0-even-when-a-migration-failed-and-appliedn">KS-808 run-migrations.sh exits 0 even when a migration failed, and applied=N counts skips — the summary line cannot be trusted</a></summary>
<p>

## BLUF

`scripts/run-migrations.sh` **exits 0 unconditionally, so docker-compose's** `service_completed_successfully` **is satisfied by a run in which a migration FAILED — and** `applied=N` **counts skips as applications. The only honest field in the summary line is** `failed=`**.**

This matters right now because KS-796's migration 046 ships with a deploy note that says "verify the constraint directly after the rebuild — the runner's exit is not evidence". That note is correct, and this ticket is why it has to exist.

**Three findings, and the first two are already known and deliberate — the third is not.**

## Recommendation

Split them. (1) and (2) are a design decision with a written rationale; (3) is a plain defect.

1. **Keep or change the unconditional** `exit 0` **— a decision, not a bug.** The rationale is in the script (`:147-155`): a partial failure must not block `--force-recreate`, because dependent services gate on `service_completed_successfully`. Changing it without replacing that mechanism turns a known-tolerable state into an outage. If it changes, the replacement is a distinction between *expected* drift failures and *unexpected* ones, not a bare `exit 1`.
2. **Fix** `applied_count` **regardless.** It is free and it is what makes the summary lie.
3. **Restore the tracker the script cites.** One line.

## Detail — measured at `2ddca095d`

**(1) The exit is unconditional and deliberate.** `scripts/run-migrations.sh:158` is a bare `exit 0`, and `:147-155` prints a WARN explaining why:

> *"Exiting 0 so docker compose dependent services can recreate; otherwise* `--force-recreate` *would block on migrations* `service_completed_successfully` *condition. (BACKLOG #6 — partial-failure exit semantics.)"*

So this is a recorded trade-off, not an oversight. Worth saying plainly, because a ticket that reads it as sloppiness will get the fix wrong.

**(2)** `applied=N` **counts skips.** `apply_one` (`:88`) returns **0** on the already-applied path:

```
already_applied=$(psql … "SELECT 1 FROM _secuura_migrations WHERE filename = '$fname' …")
if [ "$already_applied" = "1" ]; then
  echo "[$TARGET_NAME] Skipping $fname (already applied)"
  return 0          # <- indistinguishable from "applied it"
fi
```

and the caller (`:138`) increments `applied_count` on any zero return. A run that applies nothing and skips forty files reports `applied=40 failed=0`. Combined with (1), **both** fields in `Summary: applied=N failed=M` can be read as success when neither is.

**(3) The tracker the script points at does not exist.** `BACKLOG #6` is cited in the code as the home of this decision. `BACKLOG.md` at this head has **28** open entries and **not one** mentions the migration runner, partial-failure exits, or exit semantics — searched for `partial-failure`, `exit semantics`, `run-migrations` and `migration runner`, all zero, against a control (`grep -c "Where:"` → **35**) proving the search works on that file.

So the reasoning for a deliberate deviation now lives only in a shell comment pointing at a reference that has gone. That is the failure mode worth fixing first: a deferral outlives its tracker, and the next person to read `exit 0` has nothing to read.

## Why it is not higher than Medium

Nothing is currently mis-deploying because of it — the KS-796 deploy note routes around it by verifying the constraint directly, and the app's `startup-migrations.ts` has its own retry path. The risk is that a future deploy trusts the summary line. Priority is Kam's / Wednesday's call.

## Provenance

* Raised as **F-8 (MINOR, pre-existing)** by the KS-796 Q1+Q3 gate, PR #819 @ `ba6c60e35`, report §2.
* Every line number, the `apply_one` return path, the BACKLOG search and its control measured independently in this session at `2ddca095d` before filing.
* Related: **KS-796** (migration 046 and its deploy note), **KS-800**.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-865-examinedcount-ks-808-3-trackercite-a-missing-listed-input-is-an-ce891d7f31fd">Review in Linear</a></p>

