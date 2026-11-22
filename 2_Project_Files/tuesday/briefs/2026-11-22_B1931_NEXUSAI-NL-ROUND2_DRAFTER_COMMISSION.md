# B1931 DRAFTER COMMISSION (Opus, in-session, READ-ONLY) -- Datasec / NexusAI: lane N-L ROUND 2 (fix round after gate B1925 NO GO), one build kit for seat Datasec/NexusAI-N163

Re-commission if the kit or report is absent (one Agent call, model opus: "read that commission whole and do it"). Commissioned by Tuesday (s311), written at 2026-11-22 22:41:21 +1100. Return a 10-line summary with `STARTABLE: YES` or `NO` as line 1.

## WHAT IS ESTABLISHED (read each at source)
- Round 1: kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1911_SEAT-N162_nexusai-lane-nl.md` (its Stamp's Q-ANSWERS), the seat's STATUS `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-22_B1911_STATUS.md`, branch `b1911/nexusai-lane-nl-brand-contrast` at `081f4221f442bbd7ee68be6475f5f64280d558d5` (PUSHED: a fix round never rebases; ONE fast-forward commit on top; main 8858e5d1 unmoved at the gate).
- The gate: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1925_verify/VERDICT.md` (read WHOLE) and its screenshots. **Major F-1:** the light chip text `#212529` is not a brand token (0 hits in `docs/BRAND.md`, `tokens.css`, `derive-brand-tokens.js`; `index-styles.css:1459` and `:1472` reject it by name for `#333333`); cell C1 accepts any hex. Minor F-2 (the dark track `#313131` hides the black toner fill, 1.18 to 1.40), Minor F-3 (BRAND.md R5's stale "#00719f is never text"), Minor F-4 (no cell for the drop zone's drag-over and file-chosen states).

## THE KIT (Tuesday's decisions as coordinator)
1. **F-1 is fixed by a BRAND TOKEN, never a new colour.** Default: `#333333`, the token the stylesheet's own comments name (12.635:1), with whatever its pinned count and the generated `tokens.css` need, IF `derive-brand-tokens.js` regenerates it and the change is measured; otherwise the next token the gate listed that needs no generated file. Say which and why with the BRAND.md line. **C1 is tightened so an off-guide hex fails** (red first: C1 red against round 1's `#212529`).
2. **F-2:** the dark toner fill must be visible against its track by the repo's own contrast rule for non-text UI (find the rule; 3:1 if the repo names WCAG 1.4.11): choose a TOKEN for the track or the fill, red-first cell, both modes rendered.
3. **F-3:** BRAND.md R5's stale sentence corrected to what RD-251 and C-258 made true (a docs line; who decided: the product owner's rulings as quoted in CLARIFICATIONS, verbatim, never paraphrased into a new rule).
4. **F-4:** cells for the drag-over and file-chosen states.
5. The rest of round 1 stands; no other path; the e2e suite stays untouched (owed).
Gate after: tier 1 again with a rendered leg in both modes (round 2 of 2: a NO GO after this goes to the product owner as a card).

## FORM AND RULES
- FORM: round 1's kit (B1911) and its form kit B1771 (find it in briefs/), its lock, chain, worktree-slot, mutation and verify rules; `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/DRAFTER_RULES.md` binds you (red-first, every frozen literal measured in a `.measured` sidecar, `stamp_check.py <kit>` exits 0, PRIOR-WORK CHECK, the seat's read load in bytes, the stamp section with `____` slots and last line `READ-WHOLE-BY-TUESDAY: ____`).
- Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1931_SEAT-N163_nexusai-lane-nl-round2.md`, sidecar, report `2026-11-22_B1931_DRAFTER-REPORT.md`, scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s311/d1931/`.
- READ-ONLY toward NexusAI, Jira and GitHub (`gh api -X GET` only under `GH_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config'`, repository `datasecau/Reporting_Dashboard_Au`); prototypes only in your own scratch copy (never the project's worktrees, never `.tools/b1911/`); no `cd`; never delete; `python3 -I`; nothing to any human; no deploy (C-224).
