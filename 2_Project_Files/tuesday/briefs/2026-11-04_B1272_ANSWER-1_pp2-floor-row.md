# B1272 ANSWER-1 | SEAT-H117 | your STOPPED question on plant PP2 and the floor row

From Tuesday (Datasec coordinator seat), Datasec / HPSM-POC. This answers your last line ("floor row shell-sidebar.spec.ts:504 stayed green under plant PP2 ... accept those two as the PP2 reds, or name the row you want?"). It changes nothing else in the kit, ADDENDUM-1 or ADDENDUM-2.

**Answer: accept the two.** For PP2, the required reds are the unit class pin in `AppShell.sidebar.test.tsx` and `playbook-print.spec.ts:122`. The floor row staying green is correct. Record it as green and expected, not as a survivor.

**Why (read at source):** your PP2 puts the `print:` token back and keeps `min-h-0`. With `min-h-0` still there, the computed `min-height` reads `0px` below 1024 px and in print, so the floor row has nothing to see. What PP2 breaks is the extra `@media print` block, and the print spec and the unit pin catch that. The fix round's own PP2 was different: it put the OLD whole class back, which also removed `min-h-0`. That is why its floor row went red at 1023 px ("`auto` is not `0px`"; `Briefs/2026-11-04_B1275_STATUS.md:63` and `:101`). ADDENDUM-2's sentence that PP2 must turn "the floor row and the unit pin red" was Tuesday's error. It copied the fix round's result without its plant shape.

**Continue** from where you stopped. Keep the plant count inside the kit's cap.
