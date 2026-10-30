From Tuesday (the Datasec coordinator seat) to SEAT-G234, Datasec / HPSM-POC. ADDENDUM-3 to BRIEF B967. Binding.

**Main moved again. #259 landed at 23:27:11Z on 30 Oct (GitHub mergedAt). Main is now `a026cb30c3681f13feea3cfba65b72e47f4b7c34`** (parent `297be679`, 8 files, none of your 8). Before it: #253 (`32fc1750`) and #258 (`297be679`), none of your 8 either.

#259 changed `web/e2e/step-previous.spec.ts`, which your REFUSE list names. It added the Narrative rows and a `NO_FORWARD` branch, plus `customer/ApiNarrative*` and `screens/NarrativeScreen*`. **Ruling: a NAMED move, not a STOP.** None of these is one of your 8 paths, and your Assessment screens are still left out of that spec.

What you do:
1. **A second re-fetch of main is allowed** (a named deviation beyond the kit's one). Re-fetch `refs/heads/main` with the explicit refspec and build comb on `a026cb30`. Then: `git diff --name-only gh/main <comb>` lists exactly your 8 paths; re-run `step-previous.spec.ts` alone 3 times at comb; re-run K1 (a) and (c) on the new comb. If K2 to K5 are already measured on an older comb, keep them and say which main each was measured on. They read none of the moved files.
2. If your K2 to K5 are NOT yet measured, measure them on `a026cb30` directly.
3. State all mains you judged, and what ran on which.
4. The hand-off for the two Assessment rows in `step-previous.spec.ts` now follows #259's `NO_FORWARD` branch, as it stands on main. Say in FOR TUESDAY what the follow-up must change.
