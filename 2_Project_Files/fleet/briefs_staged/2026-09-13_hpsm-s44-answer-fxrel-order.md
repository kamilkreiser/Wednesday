BLUF. **No objection to either change.** FX-R ahead of FX-LV is accepted, and so is lane FX-REL.
- **One ruling so the upgrade does not stall behind FX-REL:** once FX-R, FX-S7 and FX-SI (with its merged-code proof) are GREEN on main, step 6 waits for FX-LV + FX-REL **at most about 30 minutes**.
  - If they are not GREEN by then, roll the upgrade WITHOUT FX-LV. FX-LV + FX-REL then go in the next batch, with their own head mail.
  - Kam's 18:51 AEST words: *"Upgrade as soon as it's ready"*. The rolling rule batches within about 30 minutes (08:52:19Z).
- **Credit where it is earned:** the zero-failure switch-ON verdict caught a real, Monday-visible S10 defect (the release confirmation unmounted by the reload that release itself triggers), present since S40. Holding FX-LV rather than re-running to green was right.

## Accepted as written
- **FX-R `47305ce` onto main `2bfb42a`** (renderers only; no shared path with FX-M1, FX-LV or `s44/seat-layout`). Chain `m3r-s44`. C11 still waits for FX-LV on main.
- **FX-REL** on `s44/fx-rel` at `b8fc2a9`, stack 24680:
  - writes `Release.tsx` plus a new component test, and `s43-local-values.spec.ts` only if what the screen truthfully says changes;
  - **`useLoad.ts` forbidden, with a STOP-and-report** if it is the only right fix (it is shared by every screen);
  - RED first (release, let every reload settle, the banner must still show), mutants, then `s43-local-values.spec.ts` ×3 switch ON plus the full suite ON and OFF at zero failures, with no added waits.
- **Step 5:** the bottom-pin proof RED on `c22fe56` and GREEN at head at 1440 and 390, plus FX-SI's own tests, is accepted. The tenant-picker RED is valid (Sign out at 1,949.56 px). Your test-locator miss is disclosed and fixed in `2d6b884` with no assertion changed; run 2 is the proof.
- **Pins:** the precheck on `2bfb42a` gives NO STOP, and its positive control against `c2fbc36` gives 3 STOPs. The explicit capability-hash check before the head mail is accepted. **The head mail states the pin answer in one line.**
- **Post-check shape:** A is proved by validate, and B by its release record and previews (a released engagement answers 409 NO_EDITABLE_VERSION to validate at caf63fd). Accepted. The audit rows from read-only previews are product behaviour; note them in the report.
- **Fresh engagements only on Tuesday's word:** correct. Tonight's A and B stay the demo engagements unless a pin change forces otherwise, and that STOPs first.

## Unchanged
Gate fix b-tight waits for Kam's word. Tonight's step-6 upgrade does not carry FX-PIN. Every upgrade: head mail, ~5 minutes, pc-lane-a then Azure, post-check, report.
