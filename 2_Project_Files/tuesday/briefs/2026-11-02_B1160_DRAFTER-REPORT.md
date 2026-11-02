STARTABLE: YES, with one condition. The kit is complete and every pointer was printed by a program at the pinned sha; the only unmeasured premise is that a line-count model built on pdf-fit.ts's `textWidth` never predicts fewer lines than pdfmake renders. The kit makes the builder measure that (Step 2c, row R10, plant P7) and STOP if it fails, so it is a builder gate, not a launch blocker. Launch the kit only after Tuesday stamps the slots. Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-02_B1160_SEAT-C82_composer-pcomp23-footer-round2.md` (27 KB, under 40 KB; 8 four-underscore slots, last line `READ-WHOLE-BY-TUESDAY: ____`).

## Contradictions with this commission
1. The commission says the gate files are at `Briefs/2026-11-02_B1151_STATUS.md` and `Briefs/2026-11-02_B1151_evidence/`. They are at `P/1_Project_Definition/Briefs/...` (project-relative `Briefs/` does not exist). The kit uses the real paths.
2. `document-pdf.ts:249` and `document-docx.ts:181` are right at the head (57ecad38), but `document-pdf.ts:248` is a comment and `:249` is the only `spec.footer` use; confirmed.
3. The commission says option (b) "check whether it collides with #85's files". It does: see Q-1. Option (b) cannot be done inside the two-file partition.
4. The commission suggests "pdfmake's own text measurement, if the renderer exposes it". It does: `pdf-fit.ts:38` `export function textWidth`, and #85's head keeps the same signature at `pdf-fit.ts:38`. No renderer change is needed for the measurement.
5. The B1140 template's "READ-WHOLE last line" and the commission agree. The template's ports line named a block; this commission names none, so the kit says "ports: none". Scan: `lsof -nP -iTCP:9995-9996 -sTCP:LISTEN` rc 1; a word-boundary scan of today's and yesterday's SEAT kits for 9995/9996 hit one file, `B1100_SEAT-A1_nexusai-sqlite3-successor-assessment.md` (not a Composer kit; irrelevant because the kit uses no port).

## BLUF
The class is "the footer's first line takes more rendered lines than the footer has room for". Three lines fit (RELAYED from the gate, to be re-measured in kit Step 2a), the hash line is the third, so the first line may take at most two rendered lines. Round 1 bounded a proxy (code points); a code-point count cannot see width or line breaks. Recommended round-2 fix, entirely in `change-report.ts`: keep the 122 code-point ceiling and add a conservative rendered-line-count model built on the writer's own `textWidth`; clip (prefix plus the existing `...`) to the longest prefix that satisfies ceiling, <= 2 modelled lines and no token wider than the left column; a first line that fits both is byte-identical to today. The kit makes the model earn trust through a real-render oracle (R10, seeded fuzz of at least 60 cases), a replay of the gate's 268 OUT cells (expect 0 OUT after) and eight plants. This closes the class for the change report without touching a file #85 holds. The structural fix (hash line as its own element) belongs in the policy-PDF half, after #85, and would retire the model.

## Facts re-measured (instrument, time)
| fact | instrument | time AEDT | control |
|---|---|---|---|
| branch head `57ecad389b677ec41cf8176c7ab57f845adcc33c`; main `01bc16e4e9f27d5d23d4eb0cbc9ee0cbdfecbc17` | `gh api -X GET .../git/ref/heads/...` under the project `GH_CONFIG_DIR` | 22:25 | both equal the gate's pins |
| open PRs #113, #91, #86, #85 (#85 draft, head 851057291ffb..., 57 files, base 308b7aa6, mergeable_state clean) | `gh api -X GET .../pulls`, `pulls/85` | 22:25-22:28 | #85 list prints `document-pdf.ts` |
| #113 files = `change-report.ts`, `change-report.test.ts` only | `pulls/113/files` | 22:25 | two paths printed |
| #85 changes `document-pdf.ts`, `document.ts`, `pdf-fit.ts`, `policy-document.ts` (+53 others); none is `change-report*` | `pulls/85/files --paginate --jq .[].filename` | 22:25 | `document-pdf.ts` printed |
| `change-report.ts` 572 lines: budget comment `:484-492`, constant `:493`, `footerFirstLine` `:496-501`, `changeReportSpec` `:503`, title `:508`, footer string `:551` | `sed -n ... \| awk NR+offset` on raw `contents?ref=57ecad38` | 22:26 | `:551` matches the gate's `:551` |
| `document-pdf.ts` 256 lines: footer row `:179-189` (columns, `columnGap: 12`, `fontSize: 6.5`), `MARGIN_X = 40` `:17`, `PAGE_WIDTH = 595.28` `:15`, page margins `:197`, `spec.footer` use `:249`; `document-docx.ts:181` | `grep -n` / `awk NR` | 22:26 | constants unexported (grep for `export` on them: none in the footer block) |
| `pdf-fit.ts:38` `textWidth(text, size, bold)`, `:104` `breakLongTokens`; at #85 head `:38` and `:124` | `grep -n '^export function'` on both refs | 22:28 | both refs print the same signature |
| #85's footer row unchanged in substance (`document-pdf.ts:187-193`, margins `:205`, footer `:257`) | `grep -n` on #85 head | 22:28 | the 8-line shift matches the added lines |
| test file 480 lines: `describe` `:323`, `BUDGET` `:325`, the real-organisation sample line `:338`, `named` `:352`, R1 `:360`, R2 `:379` (asserts length-2 split), R3 `:394`, R4 `:404`, R5 `:413`, R6 `:433` | `awk NR+offset` | 22:26 | `:338` matches the gate's `:338` |
| gate frame: 4,128 cells, sha256 begins `6788ec958ac8f3cd` (kinds hpsm 3,844 / target 284); control cells exist: `A1-ATtok-L076`, `A1-Wtok-L077`, `A2c-nl1/2/5/5-long` | `shasum -a 256`, python JSON read | 22:28 | prefix equals the gate's `frame.sha256` line in its STATUS |
| model rows: C2 `model-routing.md:92`, C8 `:98`, G1 `:108`, G-cap `:111`; Sonnet id `claude-sonnet-5-5` | `grep -n` of the table, `models_latest.json` lines 23, 38 | 22:27 | ids match |
| no `.tools/b1160`, no `composer-heavy.lock`; `.tools/b879/scripts` present with the 8 files; load1 6.44 | `ls -d`, `ls`, `uptime` | 22:27 | `.tools` lists 479 entries |
| round count: gate STATUS line 1 "NO GO round 1 of 2" on the class named in the kit | read of line 1 | 22:2x | the kit quotes it |

## Fix-shape options (class: first line wraps to more lines than fit)
| shape | closes class? | files | customer-visible | verdict |
|---|---|---|---|---|
| (a1) normalise CR/LF/TAB to a space, then a per-token hard cut or width cap | wide tokens yes, line breaks yes, but only by changing how a name with a line feed prints | `change-report.ts` | changes a name that fits TODAY (1 line feed now prints a break; the gate's `A2c-nl1` is IN). That is a layout change, so a Q with default no | not recommended as the primary; kept as the fallback in Q-3 |
| **(a2) RECOMMENDED: rendered-line-count fit.** Keep the 122 ceiling; model lines with the writer's own `textWidth` (conservative: breaks at U+0020 only, every line-break code point a hard break, a token wider than the left column is cut); clip to the longest prefix + `...` that satisfies all three; one line feed that fits stays untouched | yes: bounds the actual quantity that drops the hash (lines), for any glyph the font has, any page count up to a four-digit label, any break character | `change-report.ts`, test | only the three dots; wide-letter names may clip earlier than 122 (counted, listed as a Q) | recommended. Risk: the model could under-predict; mitigated by the real-render oracle R10 and plant P7. Duplicates four layout constants from `document-pdf.ts`; R10 is the drift guard |
| (a3) provable inequality (total width <= 2(Lcol - widest token)) | yes, sound without simulating | `change-report.ts` | far more clipping (a 444 pt token forces the whole line to a few characters) | rejected: over-clips ordinary names that the gate's regression count already worried about |
| (b) hash line as its own footer element that cannot be pushed off | yes, structurally; also fixes the policy PDF and the label-cell cut | `document-pdf.ts` AND `document.ts` (the spec's `footer: string` type, `document.ts:56`) | changes the footer layout (two elements); a layout change is the product owner's | COLLIDES with #85 (both files are in #85's list, draft HOLD K6). Not this round: Q-1 |
| (c) put the hash line first | yes | `change-report.ts` | reorders the footer; R2/P4a pin the order | layout change: no |
| (d) taller bottom margin or smaller font | partly | `document-pdf.ts` | layout | collides with #85 and is a layout change: no |

Why (a2): the gate's own recommendation (B1151 STATUS :208) offers three routes: bound the line in points with the font's metrics (this is (a2)), give break opportunities (a layout change), or the structural fix in `document-pdf.ts`. (a2) is the only one inside the two-file partition that adds no word and leaves every footer that fits today unchanged.

## D-decisions (mine, for Tuesday to confirm or reverse)
- D-1: kept the 122 ceiling beside the new model, so the product owner's pending description (82 code points, 1,338 of 3,311 documents) stays an upper bound and the PDF/DOCX/JSON bytes within the ceiling stay byte-equal for shapes the model passes.
- D-2: the model counts the widest page label (`Page 9999 of 9999`), not the real one-digit label, because the gate measured 1,000-page writer-direct documents. This may clip some wide-letter names that the head leaves whole; the kit forces a regression count and lists such cells as a Q.
- D-3: the kit keeps B1151-6 (label cut) out of scope except where the "no token wider than the left column" rule fixes it on the first line for free; table cells and titles are listed, not folded.
- D-4: the squash text must be true: the kit requires counts printed in the same body for any "protected" claim, and bans "always/never drops/every name" without them (closes B1151-4).
- D-5: B1151-3 fixed by synthetic sample text; the real organisation name is deliberately not repeated in the kit (the seat copies kit text into commits).
- D-6: the kit renames the describe title to drop the ticket key (B1151-7); B1151-8 (tests not type-checked) and B1151-11 are listed, not folded.

## Q-questions for Tuesday (each with a default)
- Q-1 (structural fix): do you want the policy-PDF half and the structural footer (shape b) done after #85 lands, as a separate lane that retires the model? Default: yes, after #85; this round stays in the two files. It is not decided here.
- Q-2: may the width model replace the code-point ceiling for wide-letter names, i.e. clip them earlier than 122 when two lines are exceeded? Default: yes (the ceiling stays; the model only adds clipping where the page cannot print the text; the card text gets an updated count from the builder's regression number).
- Q-3: should a name with a single line feed print as today (default) or be flattened to a space? Default: print as today; flattening changes how a footer that fits looks, which is the product owner's. If the model is hard to make sound across line-break code points, the builder STOPs and asks; (a1) is the fallback only on the product owner's word.
- Q-4: replay cost. The gate's 268 OUT cells plus about 150 IN cells are about 420 renders; expected a few minutes under the heavy lock. Default: run it; if the lock wait exceeds the kit's 40 minutes, STOP.
- Q-5: the CV-1 card text (`card-input.txt`, 11 lines) states "from 82 characters" and "1,338 of 3,311". After this round the number of clipped documents can only be the same or higher for wide-letter names. Default: the builder reports the new count; Tuesday updates the card before it goes to the product owner.

## UNMEASURED
- Whether `textWidth` reproduces pdfmake's wrap decisions for every glyph (the model is conservative by construction; R10 and the replay are the evidence, none was run by me).
- Whether pdfmake splits a token wider than the column (RELAYED: it does not; the gate saw it pushed to the page edge); the kit makes the builder re-measure this in Step 2c.
- How pdfmake treats CR, TAB, NBSP, U+2028/2029, U+0085, VT, FF (kit Step 2b measures; the gate measured LF, CRLF, TAB and NBSP only).
- The cost and runtime of the replay and the fuzz.
- Word's own footer wrapping (DOCX): the gate left it UNMEASURED too; Word grows the footer upward, so the hash line is not expected to be lost, not verified.
- No render, test, build or container was run by me. The OUT-cell count 268 is the gate's; my own grep of `report-matrix.txt` did not reproduce a count (the file's per-cell format differs from my pattern), so the kit tells the builder to derive it with the gate's programs and treat 268 as the control.
- Policy-target (`kind: target`) cells (284): the kit sends them through the spec-level model only, since the real render needs a content release.

## Outside-the-fences disclosure
- Wrote exactly two files: the kit and this report. Scratch copies of raw GitHub contents (change-report.ts, test, document-pdf.ts, document-docx.ts, pdf-fit.ts, #85's document-pdf.ts and pdf-fit.ts) went to the session scratchpad only.
- Read: the project's gate STATUS and evidence (`card-input.txt`, `frame.json`, `report-matrix.txt` headers, `B1140_STATUS.md` first 30 lines); the B1140 kit and DRAFTER_RULES; `model-routing.md` rows. No decision-queue, no `briefs_staged`, no scoreboard, no `_ledger.md`, no other client's material.
- `gh api -X GET` only, under the project `GH_CONFIG_DIR` (one `pulls/85` read printed the whole PR JSON to my console, including the PR body of a held draft; nothing from it is used except head sha, base sha, file count and mergeable state). No git write verb, no HTTP to any hosted host.
- Shell hooks fired advisories on three of my commands (case-sensitive greps, a `$?` after a pipeline); the affected greps were paired with positive controls by reading the printed lines; the one `echo rc=$?` after a pipeline carried no conclusion.
- One tool-result (the frame.json dump) overflowed to the harness's persisted-output file; nothing was written by me there.
