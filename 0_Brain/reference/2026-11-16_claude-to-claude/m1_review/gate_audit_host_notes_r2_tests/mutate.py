# QA-AUDIT-HOST-NOTES-R2 item 7: one mutation of docs/AUDIT-HOST.md per copy (raw bytes).
# Usage: python3 -B -I mutate.py <copy root> <name> <a0379be doc>
import sys
root, name, a0 = sys.argv[1], sys.argv[2], sys.argv[3]
p = root + "/docs/AUDIT-HOST.md"
s = open(p, "rb").read()
lines = s.split(b"\n")
def idx(prefix):
    hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    assert len(hits) == 1, (prefix, hits)
    return hits[0]
if name == "row15_removed":
    del lines[idx(b"  | A seal call refused before it started")]
elif name == "row14_old":
    old = [l for l in open(a0, "rb").read().split(b"\n") if l.startswith(b"  | A seal whose step 1 or 2 failed")]
    assert len(old) == 1
    lines[idx(b"  | A seal whose step 1 or 2 failed")] = old[0]
elif name == "sentence_removed":
    i = idx(b"  Two seal answers have no row:")
    assert lines[i - 1] == b"" and lines[i + 3].endswith(b'(\xc2\xa76, "The window").')
    del lines[i - 1:i + 4]
elif name == "oldrow_byte":
    i = idx(b"  | UNKNOWN: the re-open failed")
    lines[i] = lines[i].replace(b"Nothing blind", b"Nothing blinD", 1)
elif name == "row16_added":
    i = idx(b"  | A seal call refused before it started")
    lines.insert(i + 1, b"  | An extra case | `Ok` | Anything |")
elif name == "oldrow_space":
    i = idx(b"  | UNKNOWN: the re-open failed")
    lines[i] = lines[i].replace(b"Nothing blind", b"Nothing  blind", 1)
else:
    sys.exit("unknown mutation")
open(p, "wb").write(b"\n".join(lines))
