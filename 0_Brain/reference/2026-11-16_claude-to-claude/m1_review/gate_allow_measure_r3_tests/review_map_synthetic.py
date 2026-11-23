#!/usr/bin/env python3
"""QA-R3: build synthetic transcripts with the SHAPE the committed transcript_review_keys.txt shows (no real content),
to see that the committed review_map.py prints the committed review_map.txt format. usage: review_map_synthetic.py <outdir>"""
import json, os, sys
d = sys.argv[1]
def a(tools, req): return {"type": "assistant", "serverClassifierRequest": req, "message": {"content": [{"type": "tool_use", "name": t} for t in tools] or [{"type": "text", "text": "x"}]}}
def u(req): return {"type": "user", "serverClassifierContext": {"request": req, "context": {"platform": "macos"}}}
cases = {
 "m9ctl_shape.jsonl": [a(["Bash"], "<ID-1>"), u("<ID-1>"), a([], "<ID-2>")],          # M9-fresh-ctl shape
 "m9hook_shape.jsonl": [a(["Bash"], "<ID-1>"), {"type": "user"}, a([], "<ID-2>")],    # M9-fresh-hook shape
 "edge_none.jsonl": [a(["Bash"], None), {"type": "user", "serverClassifierContext": {"context": {}}}],  # context w/o request key
}
for n, recs in cases.items():
    open(os.path.join(d, n), "w").write("\n".join(json.dumps(r) for r in recs) + "\n")
print("written:", sorted(cases))
