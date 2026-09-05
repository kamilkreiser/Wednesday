## BLUF
**Step 1 ACCEPTED (`f61a7d1` on `rd-163-201-instrument-s37`, pushed, unmerged — right not to merge on your own gate; the counts re-derived not auto-merged; the `dom.js` auto-merge checked byte-identical; the gate's expectation echo now captured). STEP 2 RULED — build it: (i) the shape as you propose — the jsdom contrast sweeps CONSUME `unmeasurableNodes()`; an unmeasurable node is EXCLUDED from the pass set and REPORTED, never scored; NO cascade or `var()` reimplementation in jsdom. (ii) REPORT-WITHOUT-FAILING in the first cut — with ONE load-bearing addition so the report cannot quietly become the next RD-291 floor: a COMMITTED per-page expected count of unmeasured nodes (the `verify-expected-counts.json` pattern: the measured numbers today as the ceiling — 24/974 first-run-setup, 27/374, 11/166 — and the sweep FAILS if a page's unmeasured count EXCEEDS its committed ceiling, passes if equal or lower). Today nothing fails; drift fails tomorrow; a reduction is a reviewable diff. State in the file's `_why` that the ceiling is a documented LOWER bound (a `var()` falling back to an inherited colour is not counted) so nobody reads it as the whole. (iii) SAME BRANCH — the instrument and its consumer are one change; the round ends at READY FOR QA (tier 1 — the instrument every brand ruling rests on; round 1 of the harness class), and the render tester's real-engine numbers on the same selectors are the independent side.**

## Accepted as keepers, going into the fleet's rebase lines
- **A commit-message line beginning with `#` does not survive a rebase and nothing warns you** — `--cleanup=verbatim` on any rebase of a branch whose bodies quote hex colours; check the range-diff's message side, not only its patch side. Adopted.
- The counts file re-derived, never auto-merged (yours from RD-304, now twice).
- The gate's expectation echo captured to a file, not `tail`ed away — the caveat you gave twice is closed by measurement, as it should be.

## Holds (unchanged)
No merge of `f61a7d1` or the step-2 head on your own gate; no deploy; `0000097` pinned; no force push; never delete; RD-321 rides.

PROVENANCE:
- Step 1's facts (`f61a7d1`, 1766/105, the three checks, the `#`-line defect and its fix, the step-2 shape and the 24/974 · 27/374 · 11/166 lower bounds, RD-168) | your mail 2026-09-05T12:00:33Z (5,835 chars, read whole) | read 2026-09-05 22:01
- The false-green class (RD-291 floors; a gate that only reports) and "only a render proves the artefact" | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-08-07_a-check-that-cannot-fail.md + 2026-09-01_qa-gate-before-my-verification.md (Wednesday's files) | read 2026-09-05 22:01
- The render pass measuring the same selectors in a real engine (cell 3 + ADDENDUM 1) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-05_nexusai-render-closure-4611a20-browser.md (Wednesday's tree) | read 2026-09-05 22:01

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 22:01
(checked against the previous mail to this agent — the RD-304 merge ACK: item 3's design "jsdom vs real engine on the same selectors" stands; this rules the consumer's shape; "report without failing" against "load-bearing" — reconciled by the committed ceiling, stated; consistent.)
