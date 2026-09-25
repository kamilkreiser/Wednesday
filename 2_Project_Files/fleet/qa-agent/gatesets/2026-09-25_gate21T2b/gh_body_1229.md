#1229 KS-865 EXAMINEDCOUNT + KS-808 (3) TRACKERCITE: a missing listed input is an error and the gate says how many it examined; the migration runner cites keys, not a phantom BACKLOG entry
head ed85bd81d0acb137c89e1257d05ef9c72855086b

## What and why

Two scripts, two defects of the same family — **a check that reports on work it did not do**, and **a
deferral whose tracker does not exist**. One PR because both are small, both are in `scripts/`, and
neither has a runtime surface.

**KS-865** (`099f9fb6b`) — `check-no-latest-tags.sh` advertised **six** files and could only ever read
**five**. It `cd`s to `Blockchain/Dev`, so its `.github/workflows/deploy-staging.yml` entry resolved to
`Blockchain/Dev/.github/workflows/deploy-staging.yml`, and `[ -f "$f" ] || continue` skipped it in
silence while the gate printed `OK`. This script is on the push preflight and was cited as passing
evidence on #852.

**KS-808 defect (3)** (`ed85bd81d`) — `run-migrations.sh` cited `BACKLOG #6` as the home of its
deliberate exit-0 trade-off. Since the ticket was filed, KS-1031 rewrote the block and the defect got
**worse, not stale**: the script no longer merely cites a missing entry, it **asserts a fact about a
file**, in two lines it prints.

## KS-865: the ticket's other fix option does not exist

The Acceptance offers *"or the path is corrected to the repo root and the file is actually scanned"*.
**Measured: `git ls-tree -r` at develop `6ab9d5021e96` finds NO file named `deploy-staging.yml`
anywhere.** It existed at **both** paths and both were deleted:

| path | added | deleted |
| --- | --- | --- |
| `Blockchain/Dev/.github/workflows/deploy-staging.yml` — what the script actually looked for | `4d908483f` | **`b2c70381a`**, *"chore(midnight): scrub residual Midnight references (KS-318) (#332)"*, **2026-06-25** |
| `.github/workflows/deploy-staging.yml` — the repo root | `1e3600359` *"Move GitHub workflows to repository root for Actions discovery"* | `da98e25aa` |

Control: the same query for `.github/workflows/ci.yml` returns commits, so the instrument works. So the
entry is **not mis-rooted — its target is gone**, and Wednesday's (i)+(ii)+(iii) is the only shape left.
The other five entries all resolve at this tip.

**Net effect is stricter.** The only loosening is removing an entry that could never be read; every
readable input is now mandatory, and the count makes an examined-nothing run impossible to misread.

## KS-808 (3): the claim is false, measured

The two lines the script printed:

> *"The BACKLOG #6 reason for exiting 0 (migrations 002/005 failing every boot) was itself fixed and
> **BACKLOG.md marks it resolved**, so a failure here is a real failure."*

Against `BACKLOG.md` at this tip (1,234 lines), case-insensitive fixed strings:

| term | hits |
| --- | --- |
| `BACKLOG #6` · `run-migrations` · `migration runner` | 0 · 0 · 0 |
| `partial-failure` · `partial failure` · `exit semantics` · `service_completed_successfully` | 0 · 0 · 0 · 0 |
| **control** `Where:` | **41** |
| **control** a nonsense term | 0 |

The search discriminates, so the claim is false. Those lines now cite **KS-1031** (which made the
`exit 3` change) and **KS-808** (which still carries the `applied=N` counts-skips defect). A Linear key
is a tracker a reader can always resolve; a BACKLOG heading is not — which is the general shape of this
defect. Verified: the script's `echo` lines name BACKLOG **0** times at this head and **2** at base; the
one remaining mention is inside a `#` comment recording what was removed.

**Scope, per Wednesday's ruling (option b):** `scripts/run-migrations.sh` only. **`BACKLOG.md` is not
edited** — it is in no seat's lane this round. Defect (1) is already changed by KS-1031. Defect (2) —
`apply_one` returning 0 on the skip path, so `applied=N` counts skips — is **live and out of scope by the
brief**; KS-808 stays open for it.

## RED-PROOF

New suite `Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh`, 7 cells, run against both
trees under `/bin/bash` 3.2.57:

| tree | result | which cells |
| --- | --- | --- |
| base `6ab9d5021e96` | **3 passed, 4 failed** (rc 1) | both defect cells, the count-varies control, and the list control — the last naming **line 7 of `CHECK_FILES`** |
| this head `ed85bd81d` | **7 passed, 0 failed** (rc 0) | — |

| cell | pins |
| --- | --- |
| 1 | a complete tree: rc 0, `examined 5 of 5`, the OK line |
| 2 | **the regression** — one listed file deleted: non-zero rc, an `::error::` naming it, `examined 4 of 5`, **no OK line**. At base this read rc 0 and `OK` |
| 3 | **the count VARIES** with the tree (5, then 4) — so `examined N of M` cannot be a hard-coded string |
| 4 | CONTROL: a real `:latest` still reds the gate and names the file |
| 5 | CONTROL: a `:latest` on a comment line is still ignored — so cell 4 cannot pass by the filter breaking |
| 6 | CONTROL: `deploy-staging.yml` is absent from `CHECK_FILES` **and** its removal is explained in a comment |
| 7 | CONTROL: the subject parses under bash 3.2.57 |

The suite's own `build_fixture` applies KS-897's lesson from the start: a fixture that cannot be built
aborts with a named error and `exit 2` rather than letting the cells assert against a tree that is not
there.

**Disclosed: cell 6's first version was wrong and the cell caught it.** It grepped the **whole** subject
for `deploy-staging.yml` and reddened on the explanatory comment I had just added. The comment is the
point — it stops the next reader restoring a dead entry — so the cell now asserts about the
`CHECK_FILES` **block** and additionally *requires* the comment. The narrower claim is the one that was
meant.

**KS-808 has no cell, and that is stated rather than implied.** Its fix is a comment and two `echo`
strings; the check that matters is the measurement above, which is a property of `BACKLOG.md` rather
than of the runner. A cell asserting "the runner does not print the word BACKLOG" would pin a spelling,
not a defect.

## Test Evidence

**Touched:** `Blockchain/Dev/scripts/check-no-latest-tags.sh`, `Blockchain/Dev/scripts/run-migrations.sh`,
and a new `Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh`. No service, no route, no spec,
no runtime config, no migration file, no `package.json`, no lockfile, **no `BACKLOG.md`**, nothing under
`scripts/audit/` or `scripts/preflight/`, nothing in `packages/shared`.

**Ran:** the two-tree suite matrix above; `scripts/check-script-portability.sh` **rc 0 — "7 portability
rules hold across 102 shell scripts"**; `scripts/preflight/deps-present.sh` rc 0;
`scripts/run-shell-suites.sh`. Ratios in the READY.

**NOT run:** preflight **legs 3, 4 and 8** — they need the local platform stack on `:6882`, which by
Wednesday's coordination of 02:44:51Z comes up once at the batch QA gate and is not started mid-round.
**Neither script has a route, spec, served-spec or runtime-config surface**, so those legs have no
subject here and nothing is owed at the gate. Not "gate green": 12 of 15 legs run, three with nothing to
test.

**`run-migrations.sh` is not exercised by any suite in this round.** It needs a live PostgreSQL and a
compose stack. The change is two `echo` strings and a comment, with no control-flow edit — `bash -n`
passes and `exit 3` is untouched — and that limit is stated here rather than papered over.

**Effect on leg 14's tally:** this PR **adds one suite**, so the reached count rises by exactly one.
`ks949_main_seed_idempotence.test.sh` is untouched and its verdict is unchanged.

**Migrations + config:** none.

Refs KS-865
Refs KS-808

🤖 Generated with [Claude Code](https://claude.com/claude-code)

