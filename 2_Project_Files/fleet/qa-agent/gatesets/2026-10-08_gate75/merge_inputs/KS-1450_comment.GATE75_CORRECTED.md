**BLUF: fixed and merged as `<SQUASH-SHA>`: preflight leg 14 is green on `develop` again.** At the head the gate tested, the guard went from **8 passed / 1 failed (rc 1)** on `develop` to **11 passed / 0 failed (rc 0)**. CI's own run of the guard on a Linux runner agrees. Peter, for lines 10 and 11 Kam chose **exempt the recorded provenance inside the guard** rather than renaming the ids. Here is what that looks like, where its edges are, and where you may want to reshape it.

## What changed

**Your marker, for the six lines that can carry it.** Lines 854, 859, 864, 869, 874 and 879 are `reason` prose. Each one now ends with `slot-literal-ok: names the sweep's slot, not a target` inside the string. Nothing else in the file changed: `$generated` (including `from_runs`) is byte-for-byte the same as parsed JSON.

**A narrow exemption for the two lines that cannot.** One extra filter stage in `scan()` drops a line only when it is a **lone JSON string element** of the exact shape the baseline writes (`"(full|pre-merge)-…-slot<N>"`). It also requires the scan's output line to contain `/schemathesis/config/schemathesis-baseline.json:<n>:`. It is not a file exclusion and not an extension exclusion. A `"key": "value"` line, a `"reason":` line and a run id of any other shape are still reported.

**A cell that checks it.** A new cell takes the value of every line the stage drops and requires it to be one of the real baseline's `$generated.from_runs` ids (`jq`, which is now required). A non-vacuity control plants a novel id in a different array and requires the cell to catch it. Novel ids are caught wherever they sit: in another array, inside an entry, or in another file.

**Where its edges are (measured, not yet fixed).** The check is by **value**, not by position, and the path test is an unanchored **suffix** of the scanner's output line. So a copy of one of the two recorded slot-2 run ids passes silently in three places:
- in another array of the baseline;
- in a new file whose path ends `schemathesis/config/schemathesis-baseline.json`;
- on any scanned line whose own text carries that `path:<n>:` prefix.

What can escape is only an id already recorded in `from_runs`, never a typed port or target. The doc clause's "in that one file" / "really is a `from_runs` member" says more than this. We will anchor the path and bound the check by position in the KS-1451 change, and correct the clause there.

## How to reshape it, if you want to

The exemption is two named constants (`PROVENANCE_FILE`, `PROVENANCE_LINE_RE`), one `grep -vE` stage in `scan()`, a mirror function that lists what the stage drops, and two cells: membership and its control. Removing the stage reds exactly **2** lines (10 and 11), which proves the stage is load-bearing.

## One thing you should know (pre-existing, raised separately)

**A bare `slot-literal-ok:` marker DOES exempt a quoted value**, which contradicts `systemTest/CLAUDE.md:1169` ("a bare marker exempts nothing"). The marker test is "one non-whitespace character after the colon", and on a JSON line the value's own closing quote supplies it:

```
  "reason": "x 6982 slot-literal-ok:",      -> EXEMPTED   (the reason is empty)
const p = 6982; // slot-literal-ok:          -> reported   (correct)
```

It is **pre-existing**: the baseline carried zero markers before this change and the marker test is unchanged, so nothing regressed. The same class is in the other harness guards:
- the literal `\s*\S` test in the Akto and Playwright guards;
- a non-empty-remainder test in the Schemathesis guard;
- no reason test at all in the Performance guard (`line.includes(MARKER)`), which also has no bare-marker control.

Fixing one guard alone would leave them disagreeing, so it is one change across all of them under KS-1451. Under the predicate "marker followed by a quote or a comma", exactly 2 existing marker lines repo-wide would be affected, and neither needs its exemption.

## Evidence

All RED and GREEN results were measured in real worktrees at the tested head:
- **Arms that red the guard, each on its own cell, each restored to the head's bytes afterwards:** a slot value in another key, a run id of another shape, a literal in an ordinary file or in a brand-new file, a novel id in another array or another file, the marker removed, and the exemption stage removed.
- **`jq` broken:** reds on the two `jq`-dependent cells (9 passed / 2 failed).
- **`jq` absent:** reds with "jq is required".
- The suite's own 54-literal positive control and all five original negative controls still pass.

**Full preflight at the tested head:** `shell suites: 71 passed, 0 failed, 0 skipped (of 71)`, and `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` Legs 3, 4 and 8 skipped because the local stack was not up. That is **not** a pass. On CI, the shell suites went from 64 passed / 7 failed on `develop` to 65 passed / 6 failed. The six remaining failures are identical on both and pre-date this change.

**Not run:** the Schemathesis package's pytest suite (`requires-python = ">=3.14.8"`; the host is 3.14.5), and the four platform suites (local stack down). The baseline's real consumer, `scripts/runner/baseline_gate.py`, was run instead. It reads 171 entries before and after, with an identical key set and exactly 6 entries differing, and only in `reason`.

Both platform HTML docs carry the same one clause about the exemption, in the same commit, per the test-discipline skill §4. Its two overstatements are named above.
