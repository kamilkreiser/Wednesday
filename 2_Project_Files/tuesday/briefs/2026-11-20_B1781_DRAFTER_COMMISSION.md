# B1781 drafter commission -- MPS records pass for PR 222 (MPSCALC-426, part codes in the unpriced documents; both review rounds) (SEAT-R284)
Commissioned by Tuesday (s298), 2026-11-20. Drafter model: Sonnet (routing row C8). You DRAFT a kit; you write no Jira and no record.

Draft ONE records kit `2_Project_Files/tuesday/briefs/2026-11-20_B1781_SEAT-R284_mps-records-222.md` (+ `.measured`; ALSO save your
drafter report as `2026-11-20_B1781_DRAFTER-REPORT.md` beside it and return its head as TEXT) in the FORM of today's stamped MPS
records kit `2026-11-20_B1766_SEAT-R283_mps-records-221.md` (read it whole, as STAMPED, with `2026-11-20_B1766_RECUT_ADDENDUM.md`)
with the lessons of its STATUS folded in by name:
`!CODING/Datasec/Datasec MPS Commercial Calculator/1_Project_Definition/Briefs/2026-11-20_B1766_STATUS.md` (Deviations and
Corrections first). The commission that produced that kit, `2026-11-20_B1766_DRAFTER_COMMISSION.md`, still binds in shape
(read it whole): no text filled with PREDICTED ticket keys; the seat reads its sources whole BEFORE the Jira writes; every count
re-measured by program. Follow `2_Project_Files/tuesday/DRAFTER_RULES.md` whole. All paths are under /Volumes/Datasec_DEV/TUESDAY or
/Volumes/Datasec_DEV/!CODING/Datasec. Every path named in this commission was listed by Tuesday (`ls -d`) at 16:19:00 AEDT.

Facts to re-measure at source (repo datasecau/MPS-Commercial-Calculator, MPS GH_CONFIG_DIR, GET only; Tuesday's reads are dated
2026-11-20 16:19 AEDT and are pointers, not facts):
- PR 222 squash -> MPS main debb5e28f7bbd4e0f641a829eb353ac356afdd81, ONE parent 565ba142d4d07b183099eee42c1b73f94242489b, tree
  8c9375709a375ce6c0ee25f35ce74dc6e16f3214, merged_at 2026-11-20T04:55:54Z, reviewed head b1c0e4b9ad18ad9abb3228b2b80e468639eb9999
  (the earlier seat of Tuesday recorded: 12 files, the new main's tree equal to the head's tree, nine hosted checks on the head all
  success: re-read each). On the merge commit Tuesday read 8 check runs, each completed success (package, four Analyze jobs, python,
  dotnet, web). NOT deployed: read the runs on the merge commit and say what ran; MPS hosted is a card per deploy.
- The builder kits and STATUS files: `tuesday/briefs/2026-11-20_B1767_SEAT-M167_mps-unpriced-part-codes.md` and
  `.../Briefs/2026-11-20_B1767_STATUS.md` (round 1, head fa71fc87); `tuesday/briefs/2026-11-20_B1775_SEAT-M168_mps-part-codes-round2-oracle-boundary.md`
  and `.../Briefs/2026-11-20_B1775_STATUS.md` (round 2); the word-pack addendum
  `.../Briefs/2026-11-20_B1767_WORD-PACK-ADDENDUM.md`.
- The two independent reviews: `tuesday/briefs/2026-11-20_B1770_verify/` (round 1, NO GO at fa71fc8, one Major in the committed
  no-price check) and `tuesday/briefs/2026-11-20_B1777_verify/` (round 2, GO WITH FINDINGS at b1c0e4b; its `squash-body.txt` is the
  landed commit's body). Read both VERDICT.md and both FOR-RECORDS.md WHOLE (Tuesday read the two FOR-RECORDS files whole, not the
  verdicts); every sentence in a frozen Jira or records text that says what a review found is matched against the VERDICT row it
  rests on, by its own words.

What the kit records (each decision below is Tuesday's as coordinator, never the product owner's; write it that way):
1. MPSCALC-426 (the part-code follow-up): ONE comment: what landed, its acceptance check judged line by line as the round-2
   FOR-RECORDS does (including the two lines that are NOT YET: the word pack to the product owner, and that nothing is on the
   hosted site), both review rounds named. Its state after: read the ticket and the board's convention and propose it in a Stamp
   slot; do not predict a transition.
2. MPSCALC-278: ONE comment (the part codes now print; clause 1 MET for the two purchase documents with its open limits; clause 3
   still MPSCALC-424); it STAYS OPEN.
3. New tickets on MPSCALC (search each first by symbol, path and phrase, with a control; a true duplicate is commented, not
   created): NEW A the long-code layout (measure real catalogue code lengths first, without reading any price); NEW B the check's
   residual (the cascade case, the U+0001 case, the missing cell for a figure split across two text nodes: test file only);
   the optional U10 cell is a line in NEW B or a records sentence, your call, said plainly.
4. Two records corrections, each a file edit by the seat, each proven by a before-copy and `cmp` of the untouched part:
   (a) NEW C: the addendum gains ONE sentence with the page counts round 1 printed, and its section 6 bullet that says the lane
   printed no PDF is made true (quote the verdict's own figures; nothing predicted);
   (b) the first round's STATUS count "24" (reads 26): a pointer line or a correction, as the round-2 FOR-RECORDS item 4 says.
   The addendum goes to the product owner later as a document: after the seat's edit it must name nothing internal (no B-number,
   no seat, no finding id) in its customer-facing lines; say which lines those are.
5. Root records: one CLARIFICATIONS entry (the next C-number, computed by the seat from the file) for the landing and both reviews,
   BACKLOG and JIRA records as B1766 did, the history line; fast-forward of the root records repository as B1766 did.
6. For Tuesday's deploy card (NOT the seat's to post): a section FOR TUESDAY in the STATUS that lists, from the round-2
   FOR-RECORDS section "What the deploy card must tell the product owner", each item with the file and line that proves it, plus
   the two information items and the rental question MPSCALC-425 that entry C-186 handed to the next deploy card (read C-186).
Who decided: the product owner's only words on this change are his answer on card `mps-278-unpriced-option-three-words-1120`
(entry C-186 quotes it). The six sites, the separator, the boundary rule of the check, the rental documents and what "recorded"
means are the coordinator's defaults. Do not read the card store; a Stamp slot carries any card state.
Slots for Tuesday's stamp: JIRA WRITE or DRY; which creates run; RECORDS WRITE; base facts; hard stop.
Every count by program; every prose list recounted; selectors checked against the names they must match; no predicted number.

HOW: read-only everywhere except your three files and scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s298/d1781/`.
Jira GET only (credentials by name, in-process, from the MPS project's `4_Credentials/.env`, never printed). Git read verbs only in
the project. No `cd` (a hook refuses it); zsh; absolute single-quoted paths; no unquoted word starting with `=`. Clocks from
`date` in the same command. Never delete. Write the kit to disk as you go; temp file then os.replace; ASCII; `stamp_check.py`
exits 0 with the slots unfilled. NO HPSM-POC anything; nothing of any other project.
First line of your reply: `STARTABLE: YES|NO - why`. Then: files, recommended slots, the searches for each create, corrections to
this commission, UNMEASURED.
