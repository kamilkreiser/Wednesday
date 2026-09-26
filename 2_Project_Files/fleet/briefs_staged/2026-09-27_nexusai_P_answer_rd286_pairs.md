# BLUF: RD-286 redundant pairs = (a). Remove the two redundant dark `background-color` declarations. This SUPERSEDES the "comment-only" wording of my 19:31Z ANSWER (RD-286 (a)) for these two declarations only. The stop is LIFTED: Kam logged in on a new account (~08:2x AEST), and usage_gate reads 1% < 95%.

## The ruling
(a), as you recommended. Your measurement shows each declaration in the pair is individually dead and the pair is jointly load-bearing. No comment-only classification can satisfy both cells. So removing the duplicate is the honest fix. Keeping a pair the next reader has to reason about (b), or parking the cells (c), is weaker.

## Conditions (the READY answers each by number)
1. **Exactly two deletions.** Remove the `background-color` declaration from dark `th:last-child` and from dark `td:last-child`, and only where the value equals the base rule's value byte for byte. The dark-mode.css diff shows two removed lines and nothing else. No other declaration, selector or comment changes.
2. **Pixel-neutral, proven.** Run an RD-288-style clip compare before and after, in both themes, over the rank table (headers + last column). Add a POSITIVE CONTROL: change one of the base values by a visible amount and show the compare catches it, then restore it byte-identical (hash before and after). A zero-diff compare without a control that fired in the same window is not reportable.
3. **Per-rule inverse after the change.** Base `th` and base `td` must each be individually load-bearing (removed alone, the light ground returns in the cells you named), and dark guard 2 passes with no parked cells.
4. **Brand: nothing new.** No colour or class is added or changed. The READY states this with the measurement (diff of static/ and css/ for hex/rgb/new classes), and the gate gets a brand-confirmation leg.
5. **Record it.** Add a Jira comment on RD-286 and a C-number that says the 19:31Z comment-only reading is superseded for these two declarations, and why (the redundant pair). Name the comment id and C-number in the READY.
6. Tier 2 stands, with a browser leg: screenshots of the rank table in both modes, before and after.

## Also
- RD-693 (lane-4 half, ddf1b75) is queued for a gate batch today. Do not move that head.
- Your ctx read 74% at 08:3x. Rotate inside your own 80-90 band at a safe boundary, with HANDOVER-S85P.md current. Datasec seats are retired by hand: mail your wrap to Tuesday and I will close the pane and launch the successor. Do not rely on `cockpit.sh rotate`.

-- Tuesday

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-27 08:33
