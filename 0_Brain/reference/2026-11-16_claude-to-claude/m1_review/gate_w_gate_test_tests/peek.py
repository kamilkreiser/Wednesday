import sys, json
sys.path.insert(0, "/private/tmp/claude-501/qwg/t")
from extract import blocks, parse
for b in blocks(sys.argv[2:]):
    p, o, rest = parse(b)
    if p.endswith("verdict.json") and o["case"] in sys.argv[1].split(","):
        print("==", o["case"], "pm=", o["permissionMode"], "rc=", o["rc"], "el=", o["elapsed_s"], "note=", repr(o.get("note")), "canary=", o.get("canary_files"))
        for r in o["tool_results_whole"]:
            print("   R", r["is_error"], r["text"][:700])
        print("   FINAL", (o.get("final_text") or "")[:200])
        print("   keys", sorted(o.keys()))
