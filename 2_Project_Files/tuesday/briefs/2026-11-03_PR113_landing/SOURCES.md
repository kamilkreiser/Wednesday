# SOURCES, PR #113 landing text (drafted Tue 03 Nov 2026 06:43:31 AEDT)

Paths: E = /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_evidence ; S = /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_STATUS.md ; patch files = /private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/b6404be7-7dc9-4eec-9a83-b75139a48267/scratchpad/pr113-ts.patch and pr113-test.patch (PR files[0].patch and files[1].patch, saved by gh api -X GET, line numbers are within the patch) ; PR body = /private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/b6404be7-7dc9-4eec-9a83-b75139a48267/scratchpad/pr113-body.txt

## PR #113, read now (gh api -X GET, project GH_CONFIG_DIR)
head sha40: 92d6b647c66a62f0e166890c97c8882a3a9bf735
base sha40: 01bc16e4e9f27d5d23d4eb0cbc9ee0cbdfecbc17
state: open merged: false base ref: main head ref: b1140/composer-pcomp23-change-report-footer
changed_files: 2 additions: 530 deletions: 2
current title (placeholder): Change report footer keeps the hash line on the page (change report only; the policy PDF is not changed)
file list:
  modified packages/renderers/src/change-report.ts +109 -1
  modified packages/renderers/test/change-report.test.ts +421 -1
commits:
  57ecad389b677ec41cf8176c7ab57f845adcc33c PCOMP-23: change report footer line budget, so the manifest hash line stays on the page (change-report half; the policy PDF half is not done)
  92d6b647c66a62f0e166890c97c8882a3a9bf735 change report: hold the footer's first line to the rendered lines that fit above the manifest line (PCOMP-23, change-report half; the policy PDF half is not done)

## Sentence -> source (each line is grep -n output: file:line:text)

### Fingerprint line / three dots / what it does
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_evidence/card-input.txt:
    1:What changes: on the change report (PDF and Word), the small grey line at the foot of every page that reads "Datasec Policy Designer | <policy name>: change report" ends in three dots when it would not fit; nothing else is added.
- /private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/b6404be7-7dc9-4eec-9a83-b75139a48267/scratchpad/pr113-ts.patch:
    128:+    footer: `${footerFirstLine(`${brand.company_name} ${brand.product_name} | ${title}`)}\nmanifest ${report.to.manifest_hash}`,
- /private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/b6404be7-7dc9-4eec-9a83-b75139a48267/scratchpad/pr113-ts.patch:
    14:+ * The footer's first line (company, product and title) is held to what the PDF footer can print above the hash line.

### Change report only, policy PDF not changed
- /private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/b6404be7-7dc9-4eec-9a83-b75139a48267/scratchpad/pr113-body.txt:
    1:The change report's footer: a length budget on its first line so the manifest hash line stays on the page. This is the change-report half only; the policy PDF has the same defect, is not changed here, and the ticket stays open.
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_STATUS.md:
    159:- Overlap: #91 0, #86 0, #85 0 shared paths (control: #85 lists `document-pdf.ts`). `document-pdf.ts` not in this diff.

### Two files; one new test file rows
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_STATUS.md:
    166:| :7 | one commit on 57ecad38, two paths, +371 -26; +530 -2 vs main | RE-MEASURED true |
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_STATUS.md:
    71:- (iv) Whole `vitest run` (the `test` part of `ci:node` = `npm run lint && npm run format:check && npm run typecheck && npm run build && npm run test`, `package.json:21`; `scripts/ci.sh:117` runs it `--network none` with the SOW text copied in; pass predica

### What it buys: 1,999 of 9,397 at main; kept in all but 18
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_evidence/residue.md:
    21:- Today's main loses the fingerprint line in 1,999 of the 9,397 test cells that render (1,449 of round 1's 4,125); the change keeps it in all of those but 18.
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_STATUS.md:
    99:ALL    9508          0      0     151162      9379    9379  18    1999  0        25          83       647      26        598    58     26      0       0           0           5935     0        2           4

### R1..R10 test names (what it pins)
- /private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/b6404be7-7dc9-4eec-9a83-b75139a48267/scratchpad/pr113-test.patch:
    72:+  it("R1: every page of the PDF carries the `manifest <hash>` footer line inside the page", async () => {
- /private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/b6404be7-7dc9-4eec-9a83-b75139a48267/scratchpad/pr113-test.patch:
    91:+  it("R2: the footer ends in exactly the `manifest <hash>` line, and what is above it is within the budget and the lines that fit", () => {
- /private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/b6404be7-7dc9-4eec-9a83-b75139a48267/scratchpad/pr113-test.patch:
    112:+  it("R3: the DOCX footer still carries the hash line", () => {
- /private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/b6404be7-7dc9-4eec-9a83-b75139a48267/scratchpad/pr113-test.patch:
    122:+  it("R4: a short name gives the footer string the old template gives, byte for byte", () => {
- /private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/b6404be7-7dc9-4eec-9a83-b75139a48267/scratchpad/pr113-test.patch:
    131:+  it("R5: a draft keeps the hash line inside every page and keeps its DRAFT header", async () => {
- /private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/b6404be7-7dc9-4eec-9a83-b75139a48267/scratchpad/pr113-test.patch:
    151:+  it("R6: a first line exactly at the budget is not clipped; one character over is clipped to the budget with three dots", () => {
- /private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/b6404be7-7dc9-4eec-9a83-b75139a48267/scratchpad/pr113-test.patch:
    259:+  it("R7: a name with a long unbroken run of wide letters keeps the hash line on every page, released and draft", async () => {
- /private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/b6404be7-7dc9-4eec-9a83-b75139a48267/scratchpad/pr113-test.patch:
    274:+  it("R8: a name with line breaks keeps the hash line on every page, released and draft", async () => {
- /private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/b6404be7-7dc9-4eec-9a83-b75139a48267/scratchpad/pr113-test.patch:
    283:+  it("R9: a name with one line feed, and a name of ordinary words that fits, give the old template byte for byte", async () => {
- /private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/b6404be7-7dc9-4eec-9a83-b75139a48267/scratchpad/pr113-test.patch:
    374:+  it("R10: the real render never needs more lines than the footer model says, and keeps the hash line and the page label whole, at one page and at four-digit page labels", async () => {

### Bytes: no PDF/JSON bytes differ in the frame; byte for byte
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_STATUS.md:
    110:- **Bytes:** PDF bytes equal main's for every unchanged first line (0 differ, no stamp needed); `renderChangeReportJson` bytes equal in every route-A cell (0 differ); page counts equal head/main in every cell.
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_STATUS.md:
    1:GATE VERDICT B1161: branch b1140/composer-pcomp23-change-report-footer NO GO ROUND 2 OF 2 (the cap; class "a length budget on a footer line keeps the hash line on the page for every name, glyph, page count and brand, and costs no customer-visible text beyond

### Limit: model counts a break at every space; writer's breaker refuses some; 2 lines modelled, 3 rendered
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_evidence/residue.md:
    4:- Class: the footer model counts a line break at every space, but the PDF writer's line breaker (the Unicode line-breaking rules) refuses some of those breaks: after an opening bracket followed by a space, and before a closing mark across a space. A first li
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_STATUS.md:
    186:- **B1161-1 Major, class (G-2: a model-short cell; a frame cell whose head PDF lacks the hash run, within 122).** `packages/renderers/src/change-report.ts:556` (the model splits words at U+0020 only) and its comment `:536-539` (false: "never takes fewer th

### Limit: 18 of 9,508; 12 change reports and 6 long documents; 9 to 1,000 pages; within 122, unclipped
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_evidence/residue.md:
    5:- Count, frame "all 9,508 test cells" (round 1's 4,128 plus 216, this round's 4,438 + 480 + 246): 18 cells lose the fingerprint line at the change, 12 change reports and 6 long documents (9 to 1,000 pages, every page, 2,217 pages). All 18 are within the 122-
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_STATUS.md:
    104:- **OUT at the head: 18 cells, all also OUT at main (head never worse):** 9 Y3b (`op-at12` L088, L090; `op-at38` L078-L090), 3 Y8 targets (`glue` at 80, every customer), **6 Y7 writer-direct documents (`opat38` at 9, 10, 99, 100, 999, 1,000 pages: the hash

### Limit: example two runs of 38 @ each followed by '( '
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_evidence/residue.md:
    8:- Example cell: Y3b-op-at38-L080 (a synthetic name of two runs of 38 "@" each followed by "( ").

### Limit: same 18 lose it at main; never worse than main
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_evidence/residue.md:
    9:- At today's main: the same 18 cells lose the line too. The change is never worse than main on any of the 9,508 cells.
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_STATUS.md:
    103:- **Round-1 frame + X at the head: 0 OUT, 0 model-short, every label whole, 0 prefix violations, 0 bytes changed** (the builder's replay re-derived: in the round-1 frame 1449 of 4125 evaluable cells lose the hash line at main and 0 at the head; 0 cells IN 

### Limit: unlikely in operation; needs opening bracket + space in long wide-letter runs
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_evidence/residue.md:
    16:- The 18 cells above still lose the fingerprint line (as they do today); a reader sees the footer without the hash line. Likelihood in operation: low; it needs an opening bracket followed by a space inside long runs of wide letters (the realistic shapes tri

### Three dots: from 82 chars (81 whole); wide letters from about 70
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_evidence/card-input.txt:
    2:From which length: with the standard brand, from a policy name of 82 characters for ordinary words (81 prints whole); names made of a long run of wide letters with no space are cut from about 70 characters.

### Three dots: 3,311 reports, 1,366 shorter, 28 whole today, none ordinary words
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_evidence/card-input.txt:
    3:Measured on 3,311 test change reports: 1,366 now show a shorter footer than today (1,338 with the earlier version of this change); 28 of them are names that print whole today within the old 122-character limit, all long runs of wide letters, none ordinary wo
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_STATUS.md:
    116:- **S2 = 1,366 of 3,311** (round 1 at 57ecad38: 1,338 of the same 3,311; delta +28). Per axis: 1-name 436, 2-glyph 442, 1-target 171, 5-draft 196, 3-brand 119, 2-control 2.

### Reader loses end of name and some/all of ': change report'; full title on page 1; no footer only dots; only three dots, no word
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_evidence/card-input.txt:
    4:What a reader loses: the end of the policy name and some or all of ": change report"; the full title stays on page 1. No footer becomes only the dots.
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_evidence/card-input.txt:
    10:The clipping adds only three dots and no word.

### Also open: 40+ tabs, 8 cells, fingerprint line kept
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_evidence/residue.md:
    6:- A second, milder shape: a name with a run of 40 or more tab characters renders on two lines where the model says one (8 cells); the fingerprint line is kept.
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_STATUS.md:
    187:- **B1161-2 Major, class (G-2: model-short; hash kept).** Same file, the model's width for TAB. 8 cells (`Y4-tab8-x6-L118`, `Z-tab40-L075`..`L081`): model 1 row, render 2; the render draws a tab run 6.45 pt a tab. 0 lose the hash line in 246 + 51 tab cells

### Also open: q7 plant leaves every row green
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_evidence/residue.md:
    10:- Also: one test plant (the model stops counting trailing spaces) leaves every test row green: a gap in the new tests.
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_STATUS.md:
    188:- **B1161-3 Major (G-4: a plant leaving every row green).** q7: `const size = width(word) + (piece.length - word.length) * width(" ");` -> `const size = width(word);` (trailing spaces no longer counted): 17 of 17 green. Fix-shape: a row whose name has runs

### CodeQL scanned, 3 success, 0 alerts at the gate
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_STATUS.md:
    55:- `commits/92d6b647/check-runs`: total 3: `CodeQL` success 12:38:19Z, `Analyze (javascript-typescript)` success 12:39:52Z, `Analyze (csharp)` success 12:38:37Z. Alerts: `refs/pull/113/head` open 0 / all 0; `refs/pull/113/merge` all 0; branch ref all 0; cont
    158:- Start (00:31:50) and verdict (01:39:25): `commits/92d6b647/check-runs` total 3, all completed/success; alerts `refs/pull/113/head` open 0 / all 0, branch ref all 0; control `refs/heads/main` all 20 (open 0). **Scanned and clean.** PR #113 open, head 92d6

### Merge is not a deploy; Composer deploys only on the product owner's card; coordinator reads checks before landing
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_STATUS.md:
    161:- Landing rule (re-read, control `PR #88` 33 hits): `CLARIFICATIONS.md:1799` "[the coordinator] squash-merges PR #88 pinned to head 2da99cab after re-reading CodeQL and the checks. Nothing is deployed (Composer deploys only on your card)." and `:2032`. Not
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_STATUS.md:
    161:- Landing rule (re-read, control `PR #88` 33 hits): `CLARIFICATIONS.md:1799` "[the coordinator] squash-merges PR #88 pinned to head 2da99cab after re-reading CodeQL and the checks. Nothing is deployed (Composer deploys only on your card)." and `:2032`. Not

### Landing text must not say the line is kept unscoped / state measured limit
- /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_STATUS.md:
    200:- **Landing checklist (for the record; no landing after a NO GO):** head still `92d6b64`; main still `01bc16e`; PR #113 open at that head; CodeQL scanned and clean (3 success, 0 alerts); disjoint from #91, #86, #85; nothing deployed. If the product owner r

### Ticketed under the product owner's ruling
- Not in a file: the task brief quotes the live-board ruling of 2026-11-03 06:39:31, 'a - Land it; ticket the open case'. The text cites it as 'the product owner's 2026-11-03 ruling' (no card id, no name; DRAFTER_RULES.md fence 7). Option text: /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-02_B1161_evidence/residue.md:
    24:- Land it with the open case recorded and ticketed (cost: section 3).

### Checks on the four files
- subject chars:       85; non-ASCII bytes in the four files: 0 (python3 -I count above); trailer lines: 1.
- UNTRACED: none beyond the ruling above, whose source is the task brief.
