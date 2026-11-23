This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. It belongs to the brief `2026-11-23_coagent_VIEWER-NOTES_brief.md`. Seat VIEWER-NOTES only.

# VIEWER-NOTES ADDENDUM 1: the independent check said NO GO for ONE Major (a first row can end on a whole, real-looking tool or mode while the real value goes on); a fix round; then a short second check

**Read the verdict WHOLE first:** `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_VIEWER_NOTES_verdict.md` (READ-ONLY; first line `VERDICT: NO GO — head b898a7c349a9f4094da56b5c0e3bf2a3a55c5440`; 152 lines; its scripts and outputs are in `m1_review/gate_viewer_notes_tests/`: you may read and copy them, above all `vn_first.py`, `vn_wrap.py`, `vn_aim.py` and `forge2_qvn.py`). Friday has read it whole.

**What it CONFIRMED, and what is therefore not to be reopened:** real names print unchanged (32 tools, 6 modes); your six rewritten assertions are exact and none is weaker; no look-alike bar, second decision phrase or second label reaches a first row; no escape is ever split; the flapping restart prints 4 lines where main printed 27,326; every fixed line fits 72 columns; the gate is byte-identical (257 records, 0 differing, plant 2); nothing leaks (66 markers, 0 hits); 18 of 18 red rows red, the clean run green; the `la_*` tests passed three times; names and ids clean. That is nearly the whole lane, and it stood. The one finding is the question Friday herself put to the check from your screen; you had shown that row openly in STATUS. Thank you for that.

## RULED BY FRIDAY: the fix list (CLOSED; anything else you think needs changing is a `STOP Q1`, not an edit)

**MJ-1 (Major), `watch.rs` `wrap` with `render`.** Because a unit now moves whole to the next row, a first row can end exactly where a real-looking name ends: `… | tool Read | Claude Code mode: default` for the mode `default | Claude Code mode: plan`, identical (at sequence numbers 10 to 99 byte for byte) to the honest row. A row that ends without ` |` is no sign today, because honest rows end that way too.

The rule Friday rules (the shape is hers; the exact characters are yours, within it):
1. **A tool value or a mode value is COMPLETE on a row only when its closing ` |` stands on the SAME row, directly after its last character.** The viewer never ends a row between a value's last character and its closing ` |`.
2. **A tool or mode value that does not end on the row is CUT VISIBLY:** that row ends with ONE fixed cut mark, a constant, made only of ASCII characters OUTSIDE the field set of FR-B1 (so no tool or mode value can print it raw), and the value goes on after the continuation mark on the next row. Whenever the value plus its closing ` |` does not fit in the room left, the value is cut earlier, at a unit start, to leave room for the cut mark. Rows stay within 72 columns, cut mark included, by the same conservative count.
3. So the reader's rule is one sentence, and the viewer says it: a line under the header (fixed product text, Friday's wording for now, within 72 columns) that says what the cut mark means; `docs/DAEMON.md` §8 says the same and drops the sentence the check calls an over-claim.
4. Nothing else about the wrap changes: escapes whole, the continuation mark, the notice, the header, the reason's rows. The decision word stays first and true.

**Tests (yours to add; each named in STATUS):**
- The check's twin pair as a test: the mode `default | Claude Code mode: plan` and the honest `default`, at a one-digit and at a two-digit sequence number: the two first rows DIFFER, the hostile one ends with the cut mark, the honest one shows `default |`.
- The check's other aimed cases (`auto | Claude Code mode: plan`; `plan` followed by U+10FFFD, by U+2028 and an entry head, by 30 combining marks; the tools `mcp__plugin_coagent_link__send | CoAgent allowed`, `mcp__github__list_issues` + U+10FFFD, `mcp__plugin_coagent_link__share` + U+FF5C + `x`).
- A generated property over tool and mode values (real names, each followed by nothing, by one character outside the set, by a long hostile rest; lengths that put the value's end at every column from 60 to 72; sequence numbers of 1 to 6 digits): on EVERY first row, each of the two values either is followed by ` |` on that row, or the row ends with the cut mark; never anything else. And: an honest value that fits is never given a cut mark.
- A value that begins a row or fills several rows (the 300-character name): every row of it but the last ends with the cut mark.
- The cut mark cannot be forged from inside a field: a tool and a mode that contain its characters print them escaped.
- ONE new red control row (a `COAGENT_RED_LA` variant that leaves the cut mark out), red at the twin test; the 18 existing rows still red; the clean run green.
- Re-run on the new head: every wrap rule of the brief's property 7 at widths 72 to 200; the gate differential (`diff_gate.py`, `cmp.py`: 0 differing, plant 2); the leak test; the `la_*` tests.

**Existing assertions.** An assertion in the lane's own `la_*` files or in `watch.rs`'s test module whose expected string changes ONLY because of rules 1 to 3 may be rewritten to the exact new string, never loosened; quote EACH before and after in STATUS with the reason. An assertion that would have to change for any other reason, or one outside those files, is a `STOP Q1`.

**The four Notes.** N-2: correct the sentence in `docs/DAEMON.md` §8 as the verdict words it, and make `la_fields_narrow` assert on decision phrases, not on the bare word. N-4: correct the figure in STATUS (72, not 71). N-1: nothing. N-3 (two red rows write one log file): do NOT edit the script's naming here; one BACKLOG entry.

**One measurement, no model run:** the check could not establish which characters real Claude Code can put in a tool name or a permission mode. Do not run a model. If the hook's input schema or any document already in this repository says it, quote the path and line in STATUS; if not, write NOT ESTABLISHED and a BACKLOG entry. The fix above does not depend on the answer.

## Then
- All of the brief's section "Final" again on the new head, plus the new tests and the new red row. Merge `origin/main` into the branch first if it moved (it had not when this was sent: main `039b9875b69918c2a83e95d84f7f8169358b59d5`).
- STATUS: a new section "ADDENDUM 1", the cut mark and the new header line quoted, the new first rows of the check's table shown as printed, every changed assertion before and after.
- This is the lane's ONE fix round. A short second check follows; a NO GO there goes to the owner as a card.
- The last line, when all of it is done, exactly: `READY FOR QA VIEWER-NOTES r2` with the head SHA in the line above it. A question: `STOP Q1`.
