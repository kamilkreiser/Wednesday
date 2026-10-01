## BLUF

**`GHSA-mwp4-54f8-5fhr` (ip-address) is reported by neither audit leg at this base, so its baseline row is dead weight.** Removing it takes the `accepted` rows from **26 to 25** and the 2026-10-09 expiry cohort from **4 rows to 3**. Two stale statements are corrected in the same pass. **No `GRANDFATHERED_NO_EXPIRY` line removed, no third file, and the contract floor is not lowered.**

## What changed — two files, +2/−9

1. **`scripts/audit/audit-baseline.json`** — `GHSA-mwp4-54f8-5fhr` removed; `GHSA-r53p-7pc4-xj5r`'s `reason` replaced.
2. **`scripts/audit/baseline-contract.mjs`** — one docstring line: "The 17 entries" → "The 18 entries", because `GRANDFATHERED_NO_EXPIRY` holds 18.

`GHSA-r53p-7pc4-xj5r` **keeps** its row and its grandfathered line. Its `reason` still claimed "build and suites UNMEASURED", which stopped being true once that work was measured. The replacement is byte-for-byte from the extracted record (1948 B), not retyped. Its `package`, `ticket` and `decidedAt` are untouched and it still carries no `expires`.

## How the removable set was established

Leg 7's own CLEANUP block **cannot** see these rows: it filters on `e?.scope === 'standalone-locks'` (`audit-locks.mjs:299`) and **no** baseline row carries a `scope` field, so that block is empty by construction. Reading it would have produced a confident wrong answer. Its `reported` map was read instead, by a throwaway probe removed afterwards, with a positive control proving the probe can see rows.

* leg 6 `audit:gate` CLEANUP lists **15** entries no longer reported
* leg 7 `audit:locks` reports **18** ids — **none** of those 15 among them
* **15 − 0 still-reported − 14 grandfathered = `{GHSA-mwp4-54f8-5fhr}`**, and 14 + 1 = 15 exactly

## Test Evidence

**Touched:** two files. `git diff --numstat` = `1 8` and `1 1`. Nothing else: `expected-case-count` and `baseline-contract.test.mjs` are both untouched, confirmed by name and by blob.

**Ran, at head on base `723dc0722b68` (Darwin arm64, node v24.7.0):**

* `npm run audit:gate` — **rc 0**. Reads `11 distinct advisories reported, 25 baselined` (25, down from 26). Its CLEANUP list is now **14** entries and **no longer names `GHSA-mwp4-54f8-5fhr`**; the 14 are 13 undici plus `GHSA-v2v4-37r5-5v8g`.
* `npm run audit:locks` — **rc 0**, `6 advisories match, 6 already baselined`.
* `npm run audit:contract` — **rc 0**, 59 tests pass, 0 fail.

**Proved by parsing both blobs, not by reading the diff:**

* rows 26 → 25; removed set exactly `{GHSA-mwp4-54f8-5fhr}`, added set empty;
* the only surviving row that differs from the base is `GHSA-r53p-7pc4-xj5r`, and the only field of it that differs is `reason`;
* its new `reason` is character-identical to the 1948 B extracted file; the stale clause is present before and absent after;
* **nothing re-dated**: the three surviving 2026-10-09 rows keep that value byte-equal, and **no** row's `expires` changed anywhere in the file;
* `GRANDFATHERED_NO_EXPIRY` is **byte-equal** and still holds **18** ids;
* `baseline-contract.mjs` differs on **exactly one line** (`:44`), line count unchanged at 228;
* `baseline-contract.test.mjs` is blob-identical (`2379c0aeee6e`), so the `> 20` floor at `:217` is **not** lowered — and 25 rows keeps it true.

**A refusal control per gate, each restored by byte copy with `cmp` rc 0 afterwards:**

* **leg 6 + leg 7, baseline emptied** → both **rc 1**, each enumerating the ids it reports (11 and 6).
* **leg 6 + leg 7, one still-reported row removed** (`GHSA-337j-9hxr-rhxg`) → both **rc 1**, each naming that exact id; leg 6 prints `FAIL — 1 NEW advisory not in the baseline: - GHSA-337j-9hxr-rhxg`.
* **`audit:contract`, a no-expiry row planted outside `GRANDFATHERED_NO_EXPIRY`** → **rc 1**, 6 tests failing with `the committed audit-baseline.json is malformed: GHSA-b51c-0nt-rol01 (expires)`.

So all three gates are green here **and** each is demonstrably able to go red.

**NOT run:**

* No service suite, no image build: this touches only `scripts/audit/`, which ships in no image and is consumed by no service at runtime.
* No Schemathesis, Akto, Playwright or k6 — none reads the baseline.
* No deploy anywhere.
* The 14 grandfathered dead rows are **not** removed here (see Residue).

**Migrations + config:** none.

## Residue, unchanged by this PR

The 14 grandfathered dead rows (13 undici plus `GHSA-v2v4-37r5-5v8g`) that leg 6's cleanup names on every run are dead grandfathered rows; removal needs the contract floor revisited; Wednesday's to propose.

## Fuse

The 2026-10-09 cohort goes from 4 rows to **3**: `GHSA-frvp-7c67-39w9` (KS 530), `GHSA-wrjc-x8rr-h8h6` and `GHSA-337j-9hxr-rhxg` (KS 528). The date itself is unchanged, and the real fixes stay on those tickets. Related work sits on KS 470, KS 559 and KS 1378.

Refs KS-729
