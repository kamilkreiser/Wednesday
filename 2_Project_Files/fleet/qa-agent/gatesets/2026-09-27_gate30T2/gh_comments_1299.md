--- comment 5846813740 by linear[bot] at 2026-09-26T13:52:55Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1339/ks1293-hermeticity-guard-the-count-floor-fires-before-the-offender">KS-1339 ks1293 hermeticity guard: the count floor fires before the offender list, so 6 of 9 offending subjects are never named</a></summary>
<p>

**BLUF: the guard's verdict is right and its diagnosis is not.** It asserts a count floor before it asserts the offender list, so when a subject is missing the failure prints `Expected: >= 9 / Received: 8` and **never names which file**. The file's own header claims an offender is *"NAMED BY FILE, whether the assignment was deleted, nested, or the file renamed"*. At runtime, 6 of 9 subjects are never named.

**Non-blocking, and the direction matters:** the reading is **red on every real revert**, so nothing goes unnoticed. What is missing is which file caused it. The defect is in the diagnosis, not the detection.

## Where it shows

The `CONFIGPINNED` cell prints only the count comparison. The only cells that name a file — `ks1228`, `ks1264`, `ks1213` — are the RS control cells, and they name them **incidentally**, not as the offender report.

## Fix shape (one line, per the gate)

Assert `offenders == []` **before** the count floor. The offender list then prints as the failure message, and the floor becomes a secondary assertion rather than the one that fires first.

## Why it is worth fixing rather than leaving

This guard exists to stop the subject list going stale. A failure that says only "the count is 8, expected 9" sends the next reader to count files by hand across nine subjects; a failure that names the file is actionable in one read. A guard that detects correctly but cannot say what it detected invites the next editor to work around it.

## Board search before filing

Searched over **486 open issues** on this team, matching literally against identifier + title + description: `MANIFEST-BY-NAME`, `CONFIGPINNED`, `names the offender` — **0 open hits each**. `offender` returned 3 (KS-1147, KS-1141, KS-1140), none this guard. Controls as above: fresh token **0**, `ssrf-guard` **2**.

Refs KS-1293
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1339-name-the-offending-file-before-the-count-in-the-ks1293-87628786e525">Review in Linear</a></p>

