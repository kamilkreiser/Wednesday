STARTABLE: YES - the kit is complete, its sidecar has 0 TODO lines and `stamp_check.py <kit>` exits 0; the two STOP tests of the decision were measured by reading and neither stops the lane. Tuesday must still answer Q2 (blur and page hide are NEW triggers) before the stamp.

# B1790 drafter report, lane M-1, seat M169, MPSCALC-314 (drafted 17:53 to 18:01 AEDT 2026-11-20)

Files: kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1790_SEAT-M169_mps-autosave-min-gap.md` (49,388 bytes), sidecar `...min-gap.md.measured` (106 lines), this report, scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s299/d1790/` (tarball of main, ticket text, `model.py`, `fill.py`, `jget.py`).

## BLUF
Main `debb5e28f7bbd4e0f641a829eb353ac356afdd81` (read 17:53:36, 0 open PRs, 0 `b1790` refs). Four paths change: `autosave.ts`, `QuoteScreen.tsx`, `autosave.test.ts`, `QuoteScreen.autosave.test.tsx`. Design: gap measured by a `setTimeout` (not a clock) because the existing helpers fake only `setTimeout` and `clearTimeout`.

## The two STOP tests
1. Saved mark while a change is pending in the gap: NOT true. `saveStamp.ts:29-35` returns `Unsaved changes` whenever `dirty`; `Saved <time>` only when not dirty; `save()` clears dirty only if the draft sent is the draft on screen (`QuoteScreen.tsx:250`). The kit adds cell G9 for it and makes a red G9 a STOP.
2. Tests pinning one save per quiet interval: exactly ONE changes, `QuoteScreen.autosave.test.tsx:160-175` (second save at `:171-172`). Census by program (frame: `updateDraft`/`calls[1]`/count greps over `web/src` and `web/e2e`): the refusal cell `:212-226` has two saves 20 s of fake time apart and stays green by derivation; `PurchaseBomEditor.test.tsx:184` makes two saves with two button clicks (explicit, not gated); every other cell makes at most one autosave per screen.

## Corrections (to the commission and the sweep row)
1. Blur and unload saves do not exist at main (only `beforeunload` that prompts, `:298`, and a `focus` re-read, `:222`; grep for `pagehide|visibilitychange|addEventListener(.blur` prints 0, control `beforeunload` prints 1). Tuesday's decision words them as "still fires at once"; the lane ADDS them (Q2 default: add, window `blur` and `pagehide`, non-capture).
2. `autosave.b456.test.ts` holds no timing: not edited (the commission lists it as owned).
3. The sweep's "QuoteScreen.autosave.test.tsx 60, 74, 80 pin one save per quiet interval" is wrong: those are first-save cells that stay green; the changing cell is `:160-175`.
4. The ticket's acceptance says "per quiet interval"; the decision says "per gap". Kit freezes the gap reading (G3) and quotes both.
5. The sweep's blob prefixes `dd4ae636` and `9e18e29e` agree with my `git hash-object` of the tarball.

## Model numbers (DERIVED, `d1790/model.py`, not the product)
22 edits at 2500 ms: gap 0 gives 22 saves (the ticket's 22, the control); gap 10 s gives 6 by 60 s and one trailing save at 62 s.

## Questions for Tuesday (defaults assumed in the kit)
Q1 gap starts at any request (explicit too, refused too). Q2 add blur and page hide. Q3 10 s. Q4 subject ends `(MPSCALC-314)`. Q5 G2 gate incl. both browser steps. Q6 sonnet (row C2). Q7 port block. Q8 seat prints counts.

## Byte total of the reading load
Kit 49,388 + autosave.ts, QuoteScreen.tsx (610 lines), autosave.test.ts, QuoteScreen.autosave.test.tsx, QuoteScreen.flush.test.tsx, saveStamp.ts + the project CLAUDE.md = 124,082 bytes in all (printed by `cat | wc -c`), under the 300 kB aim. The kit has no READ WHOLE list of Tuesday's own kits.

## Chain inputs (rule 4)
Every step's inputs exist at main or come from an earlier step: step 3 adds the constant (no earlier dependency) before cells that import it; step 4 needs the cells; step 5 needs the fix; step 7 needs step 6; step 8 needs the commit.

## UNMEASURED
Every RED and GREEN set, the G3 count (model only), the whole-suite and both browser step totals (RELAYED from an older gate), the `vi.getTimerCount()` of G11, real-browser blur and page-hide behaviour, whether `noBrowserPricing.test.ts` stays green, e2e behaviour (derived from greps only), the load gate's origin (carried from the B1775 kit).

## Not read / outside the fences
Not read: `Source_Documents/`, `.local/`, HPSM, any other client, `decision_queue`, the vault, `briefs_staged`. Read: the commission, DRAFTER_RULES, the B1775 kit (whole, in pages; the reference diff section 85-318 skipped on purpose as another change's), the 11-19 answers file, the sweep's JOB 2 and its M-1 row, the project CLAUDE.md, the tarball of main (not executed). Jira: one GET of MPSCALC-314 (description, 0 comments) via an in-process helper; credentials not printed. `gh`: GET only. Nothing run from the tarball; no test, no install. One tmux listing showed one `Datasec/MPS-` pane (records seat per the commission); the kit's REFUSE reads it again. The `stamp_check.py --init` wrote the sidecar; `fill.py` filled it (it first mis-measured two grep counts as 0 through quoting; both were corrected by direct grep and re-checked).

## RE-CUT 2026-11-20 (Tuesday's Q2 ruling: blur and page hide OUT)
Old kit kept at `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s299/d1790/kit.pre-recut.md`. Sections changed: THE AUTHORITY (bullet 2), CORRECTIONS item 1, THE DESIGN (property, closed list, sketch item 4 deleted, item 5 kept with its number), THE CELLS (G6, G6b, G7 deleted; G14 added; expected sets), PLANTS AND MUTANTS (M4 to M6 deleted), selectors paragraph (TEN cells in the new describe, counted by program from the id rows), step 6 (new check b2: 0 added matches of blur, pagehide, visibilitychange, addEventListener), step 7 (commit body), step 10 (FOR TUESDAY), THE STATED LIMITS (L-C replaced), HOLDS, Q2 and S5. Sidecar rebuilt: 106 claims, 106 measured. No instruction of the order was found mistaken; one note: an existing cell does reach the beforeunload prompt (`QuoteScreen.flush.test.tsx:239`) but in a file the lane does not own, so G14 asserts it again in the owned file by dispatching the event (no listener added to source).
