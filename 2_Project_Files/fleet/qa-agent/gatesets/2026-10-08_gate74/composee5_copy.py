#!/usr/bin/env python3
"""Compose #1385's two doc resolutions IN SCRATCH and assert them there, HAND-WRITTEN, Seat E 5th.

Nothing here touches the real worktree or the shared object store. The resolutions are built from
develop's own file plus #1385's own block, byte-for-byte, so no third text is invented.

The rule (Q-DOC20, ruled by Wednesday): FLOW block `20.` goes AFTER `19.` and before `  </body>`;
CHEAT's KS-938 section goes LAST, after the KS-1005 section, before `  </body>`. Both reduce to
"immediately before the close tag", which is what makes the uniqueness proof below sufficient.
"""
import re, sys, os, subprocess, hashlib

B = "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-05_seatE-5th/boot"
OUT = "/private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/4f79978a-d3ed-44bc-b6e5-dd8c0f31a324/scratchpad/compose"
fails = []
def ok(c, msg):
    print(("  OK   " if c else "  FAIL ") + msg)
    if not c: fails.append(msg)

def read(p): return open(os.path.join(B, p), encoding="utf-8").read().split("\n")

JOBS = [
 # label, develop file, #1385 file, block first/last line in #1385 (1-based, inclusive), out name
 ("FLOW",  "flow_d784b613.html",  "flow_1385.html",  2067, 2127, "flow.resolved.html"),
 ("CHEAT", "cheat_d784b613.html", "cheat_1385.html", 3812, 3838, "cheat.resolved.html"),
]
CLOSE = "  </body>"

for label, dfile, hfile, a, b, outname in JOBS:
    print("\n=== %s ===" % label)
    D, H = read(dfile), read(hfile)

    # --- the anchor must be UNIQUE in develop's file ---
    n = sum(1 for l in D if l == CLOSE)
    ok(n == 1, "anchor %r occurs exactly once in develop's %s (got %d)" % (CLOSE, label, n))
    idx = D.index(CLOSE)                      # 0-based
    ok(True, "anchor at develop line :%d" % (idx + 1))

    # --- the block ---
    blk = H[a - 1:b]
    ok(len(blk) == b - a + 1, "block is %d lines, #1385 :%d-:%d" % (len(blk), a, b))
    h2 = [l for l in blk if re.search(r'<h2[^>]*>', l, re.I)]
    ok(len(h2) == 1, "the block holds EXACTLY ONE <h2> (got %d): %s" % (len(h2), h2[0].strip()[:90] if h2 else "-"))
    ok(blk[-1].strip() in ("</div>", "</p>", "</pre>", "</table>") or blk[-1].rstrip().endswith(("</code></pre>", "</div>")),
       "the block's last line closes cleanly: %r" % blk[-1].strip()[:60])
    # the block must not already be in develop
    ok(h2[0] not in D, "develop does NOT already carry this block's <h2> (no double insert)")

    # --- compose: develop, with the block immediately BEFORE the close tag ---
    R = D[:idx] + blk + D[idx:]
    ok(len(R) == len(D) + len(blk), "composed line count = develop %d + block %d = %d" % (len(D), len(blk), len(R)))

    # --- the composed file keeps develop's own close tag byte-identical, still unique ---
    ok(sum(1 for l in R if l == CLOSE) == 1, "the close tag is still unique and byte-identical in the result")
    ok(R[R.index(CLOSE) - 1] == blk[-1], "the block's last line sits IMMEDIATELY before the close tag")

    # --- div balance: my insertion must not change the open/close delta ---
    def delta(lines):
        t = "\n".join(lines)
        return len(re.findall(r'<div\b', t)) - len(re.findall(r'</div>', t))
    ok(delta(R) == delta(D), "div open/close delta unchanged by the insertion (%d)" % delta(D))

    # --- the ORDER predicate, and its INVERTED control ---
    if label == "FLOW":
        def nums(lines):
            return [int(x) for x in re.findall(r'<h2[^>]*>\s*(\d+)\.', "\n".join(lines), re.S | re.I)]
        got = nums(R)
        ok(got == sorted(got), "FLOW block numbers are ASCENDING: %s" % " ".join(str(x) + "." for x in got))
        ok(got[-1] == 20 and got[-2] == 19, "20. lands immediately after 19.")
        # INVERTED CONTROL: the same block placed on the WRONG side of the anchor
        W = D[:idx + 1] + blk + D[idx + 1:]
        wn = nums(W)
        after = "\n".join(W).index("\n".join(blk)) > "\n".join(W).index(CLOSE)
        ok(after, "INVERTED CONTROL: the block really is after the close tag in the bad composition")
        # the predicate that must detect it: the block must precede the close tag
        ok(W[W.index(CLOSE) - 1] != blk[-1],
           "INVERTED CONTROL DETECTED: the 'immediately before the close tag' predicate says NO on the wrong side")
        ok(wn == got, "(and the ascending-number reader ALONE does NOT catch it: %s -- which is why the"
                      " position predicate is the one that matters)" % (wn == got))
    else:
        def keys(lines):
            return re.findall(r'<h2[^>]*>.*?&mdash;\s*(KS-\d+)\s*</h2>', "\n".join(lines), re.S | re.I)
        gk = keys(R)
        ok(gk[-1] == "KS-938", "CHEAT keys end with KS-938: %s" % " ".join(gk))
        ok(gk[-2] == "KS-1005", "KS-938 sits immediately after the KS-1005 section")
        anchor_h2 = [l for l in D if re.search(r'&mdash;\s*KS-1005\s*</h2>', l)]
        ok(len(anchor_h2) == 1, "the KS-1005 heading line is UNIQUE in develop (the ruled anchor)")
        W = D[:idx + 1] + blk + D[idx + 1:]
        ok(W[W.index(CLOSE) - 1] != blk[-1], "INVERTED CONTROL DETECTED: wrong side of the close tag says NO")

    open(os.path.join(OUT, outname), "w", encoding="utf-8").write("\n".join(R))
    print("  wrote %s  (%d lines, sha256 %s)" % (
        outname, len(R), hashlib.sha256("\n".join(R).encode()).hexdigest()[:16]))

print("\nASSERTIONS FAILED: %d" % len(fails))
for f in fails: print("  -", f)
sys.exit(1 if fails else 0)
