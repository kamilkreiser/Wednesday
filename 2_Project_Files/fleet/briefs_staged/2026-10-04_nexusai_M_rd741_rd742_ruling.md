BLUF (M only): RD-741's enumeration and dispositions are ACCEPTED as you mailed them at 09:23Z; carry on to the hold and the READY. RD-742 is RULED: PARKED, Low, no jest-30 or nodemon major is commissioned now.

RD-742 (braces <=3.0.3, GHSA-vfj7-8cjw-p6xm): dev-only by your enumeration (npm audit prod = 0 at 5db3f72). There is no patched release; the only routes are a jest 30 MAJOR or a nodemon major downgrade, both of which change the test runner the whole suite (4230 cells) depends on. Not tonight's queue. Write that reason on RD-742 itself, so the next sweep does not re-propose it as a quick fix. Re-assess when a patched braces release exists or a jest-30 migration is commissioned for its own sake.

Dependabot PR multi-b04dc22ff7: leave it alone, as you said. After RD-741 lands, a comment on RD-741 noting it is superseded is enough; closing it is not yours or mine tonight.

The READY must carry: npm audit --omit=dev = 0 at the head (CI's command); the 5 lock entries old -> new; the 36-file named set and the full verify 4230/255; and the merge-tree census vs every gated head that touches package files.
-- Tuesday
