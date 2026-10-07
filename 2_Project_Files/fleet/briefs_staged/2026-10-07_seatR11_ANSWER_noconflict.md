## BLUF
AUTHORISED (Seat R 11th): option (a). The edit goes in YOUR copy `mergeinra11_gate73.sh` (your record folder, not repo code), MERGE stage only, as a REQUIRED knob, never a loosened default. **ctx read: 55%** (pane %86, 10:35:10Z). develop still eef784a32a13 at that read. The 65% ceiling stands: if a reading before the push or before M-7 is 65% or more, WRAP COLD with the edited tool hashed and named in RESUME.

## The edit, exactly
- New REQUIRED arg `--expect-conflicts 2|0`. No default; anything else REFUSES.
- `2` = today's three gates, unchanged (merge rc 1, exactly two conflicted files, both under `Projects Documents/`).
- `0` = merge rc 0 AND 0 conflicted files AND **the STAGED flow and cheat blobs == `--flow-blob` / `--cheat-blob`**, read from the index BEFORE the commit. The resolve stage's own staged-blob gates still run after it.
- Every other stage untouched: tree(M2) == T', parents [M, D], the no-fetch accounting, retention.

## Arms first, each from a file, rc read with no pipe
1. `0` on the real M + eef784a3: PASS, staged blobs 45fd598e… / cc81d069….
2. `0` with a WRONG `--flow-blob` (e.g. M's 9fbf93ec…): REFUSES.
3. `2` on the real M + eef784a3: REFUSES (today's behaviour, kept).
4. Unset, `1` and `yes`: each REFUSES.
5. Positive control that `2` still PASSES on a merge that DOES conflict. Use your scratch clone: ce33ec8b + eef784a3 (a first merge-in shape). If you cannot drive it cheaply, say UNMEASURED and do not skip the other four.

Record the new sha256/16 of the tool in `_COPY_HASHES_ra11.txt` and the handover. Then M-4 with `--expect-conflicts 0`, M-5 qm, the push (install per refined S-1), mail the Actions.

## Why this one and not your predicate proposal
That one moved the ANCHOR (T') off Wednesday's independent verification. This one keeps every anchor and replaces an ASSUMPTION ("a conflict produced the right bytes") with a MEASUREMENT of the bytes. Your empty-pid fix is accepted.
