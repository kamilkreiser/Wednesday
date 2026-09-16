#!/usr/bin/env python3
# anchor_restore.py <input.json> <patch.diff> <tip-file> <out.diff> — the doc twin of bash_patch's B3c repair.
# 2026-09-16 22:2x (KS-890 r2, runs/2026-09-16_ks890-ornith35b-night2): the model's stable "insert-after deletes its anchor"
# dialect — asked to insert after a named line, it writes that line with a '-' marker (there: `- Ops notes:`, one extra
# leading space) instead of as context. D2 could not apply it; had the bytes been exact it would have applied and DELETED
# the anchor (D9 red). This turns that ONE mis-marked line back into a context line carrying the TIP's exact bytes.
# It never changes a '+' line, never touches any other '-' line, and refuses (leaves the patch as written) unless ALL hold:
#   - the input names an insert-after anchor (defect_line.insert_after, read from "Insert AFTER line N" at build time)
#   - the anchor line is not blank and, whitespace-normalised, occurs EXACTLY once in the tip file
#   - the anchor is not one of the input's must-remove lines (whitespace-normalised)
#   - exactly one hunk has a '-' line equal to the anchor (normalised), that hunk has exactly ONE '-' line,
#     and no '+' line in that hunk re-adds it (normalised)
# rc 0 RESTORED (out.diff written; stdout line 1 names it) · 3 not applicable (silent in the verdict) · 4 REFUSED (stdout
# line 1 says why) · 1 instrument error.
import json, sys

def norm(b):
    return " ".join(b.decode("utf-8", "replace").split())

def main():
    if len(sys.argv) != 5:
        print("usage: anchor_restore.py <input.json> <patch.diff> <tip-file> <out.diff>"); return 1
    inp_p, patch_p, tip_p, out_p = sys.argv[1:5]
    dl = (json.load(open(inp_p, encoding="utf-8")).get("defect_line") or {})
    ia = dl.get("insert_after")
    if not ia:
        print("not applicable: the input names no insert_after anchor"); return 3
    tip = open(tip_p, "rb").read().split(b"\n")
    patch = open(patch_p, "rb").read().split(b"\n")
    # hunks: (start index of '@@', [indices of body lines]); a '--- ' line followed by '+++ ' is a file header, not a removal
    hunks = []; cur = None; i = 0
    while i < len(patch):
        l = patch[i]
        if l.startswith(b"--- ") and i + 1 < len(patch) and patch[i + 1].startswith(b"+++ "):
            cur = None; i += 2; continue
        if l.startswith(b"@@"):
            cur = []; hunks.append(cur)
        elif cur is not None and l[:1] in (b"-", b"+", b" "):
            cur.append(i)
        i += 1
    if not (0 < ia <= len(tip)):
        print(f"REFUSED: insert_after={ia} is outside the tip file ({len(tip)} lines)"); return 4
    anchor = tip[ia - 1]; an = norm(anchor)
    cand = [h for h in hunks if any(patch[j][:1] == b"-" and norm(patch[j][1:]) == an for j in h)]
    if not cand:
        print(f"not applicable: no '-' line equals the anchor (tip line {ia})"); return 3
    shown = anchor.decode("utf-8", "replace")[:60]
    if not an:
        print(f"REFUSED: the anchor (tip line {ia}) is blank — a blank '-' line cannot be identified as the anchor"); return 4
    hits = [k + 1 for k, t in enumerate(tip) if norm(t) == an]
    if len(hits) != 1:
        print(f"REFUSED: the '-' line equal to the anchor {shown!r} matches {len(hits)} tip lines {hits[:5]} (not exactly one) — ambiguous, kept as written"); return 4
    mr = [" ".join(str(m).split()) for m in (dl.get("must_remove") or [])]
    if an in mr:
        print(f"REFUSED: the anchor {shown!r} (tip line {ia}) is one of the input's must-remove lines — its '-' is intended, kept as written"); return 4
    if len(cand) != 1:
        print(f"REFUSED: {len(cand)} hunks mark the anchor {shown!r} as '-' (expected one) — kept as written"); return 4
    h = cand[0]
    minus = [j for j in h if patch[j][:1] == b"-"]
    plus = [j for j in h if patch[j][:1] == b"+"]
    if len(minus) != 1:
        print(f"REFUSED: the hunk that marks the anchor {shown!r} as '-' carries {len(minus)} '-' lines (not exactly one) — a replacement, kept as written"); return 4
    if any(norm(patch[j][1:]) == an for j in plus):
        print(f"REFUSED: the anchor {shown!r} is '-' AND re-added as '+' in the same hunk — a rewrite of that line, not the dialect; kept as written"); return 4
    j = minus[0]
    as_written = patch[j][1:].decode("utf-8", "replace")
    patch[j] = b" " + anchor
    open(out_p, "wb").write(b"\n".join(patch))
    exact = "byte-exact" if as_written.encode("utf-8") == anchor else f"written {as_written[:60]!r}"
    print(f"RESTORED: the model marked the insert-after anchor (tip line {ia}: {shown!r}) as '-' ({exact}); rewritten as a context line with the tip's exact bytes (patch line {j + 1})")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # an instrument error is never a silent pass
        print(f"instrument error: {type(e).__name__}: {e}"); sys.exit(1)
