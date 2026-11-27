# QA-POLICY-B: the findings' reproduction rows (one row each; run through run_repro.sh at both SHAs).
import json, sys
out = open(sys.argv[1], "w")
def add(i, tool, text=None, inp=None, names=()):
    r = {"id": i, "grp": "RP", "tool": tool, "names": list(names), "full": True}
    if inp is not None: r["input"] = inp
    else: r["text"] = text
    out.write(json.dumps(r, ensure_ascii=False) + "\n")
cjk = " ".join(chr(0x4E00 + i) for i in range(471))
add("M-1 471 distinct CJK characters, web fetch prompt", "WebFetch", cjk)
add("M-1 control: 470 characters", "WebFetch", " ".join(chr(0x4E00 + i) for i in range(470)))
add("m-1 trailing full stop, exact pattern", "WebSearch", "please read .env. now", names=[".env"])
add("m-1 curly quotes", "WebSearch", "please read “.env” now", names=[".env"])
add("m-1 CJK prose", "WebSearch", "请读取.env文件", names=[".env"])
add("m-2 untaught tool with a command and a note", "MadeUpTool", inp={"command": "ls", "note": "see\n.env"}, names=[".env"])
add("m-3 web fetch array prompt", "WebFetch", inp={"url": "https://example.com/", "prompt": [1, "a .env"]}, names=[".env"])
add("n-5 raw backslash in a URL", "WebFetch", inp={"url": "https://example.com/x\\.env", "prompt": "p"}, names=[".env"])
