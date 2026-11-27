# QA-POLICY-B item 2 (no panic): fuzz rows for scan B: multi-byte text, escapes cut at the window's end, `\ud800`
# typed as text, long runs of `@`, `{`, `\`, `$'`, quotes. usage: python3 -B mk_fuzz.py <out.jsonl>
import json, random, sys
R = random.Random(0x9b17f022)
ALPH = list("ab.env/\\@{},'\"$-=:;|&<>()` \t\n\r\x01\x08\x0c") + ["é", "😀", "一", "ア", "​", "﻿", "‮", "　", "\xa0", "ß", "İ", "ﬁ", "\\u", "\\ud800", "\\u00", "$'\\x2e'", "@'", "{a,b}", "\\\""]
TOOLS = ["WebSearch", "Agent", "MadeUpTool", "WebFetch", "WebFetchURL", "MonitorWS", "mcp__x__y", "AgentCmd"]
def inp(tool, t):
    return {"WebSearch": ("WebSearch", {"query": t}), "Agent": ("Agent", {"prompt": t, "description": "d"}),
            "MadeUpTool": ("MadeUpTool", {"text": t}), "WebFetch": ("WebFetch", {"url": "https://example.com/", "prompt": t}),
            "WebFetchURL": ("WebFetch", {"url": "https://example.com/" + t, "prompt": "p"}),
            "MonitorWS": ("Monitor", {"ws": {"url": "wss://example.com/" + t}}), "mcp__x__y": ("mcp__x__y", {"q": t}),
            "AgentCmd": ("Agent", {"command": "ls", "prompt": t, "description": "d"})}[tool]
out = open(sys.argv[1], "w"); n = 0
def add(i, t):
    global n
    for tool in TOOLS:
        name, js = inp(tool, t)
        out.write(json.dumps({"id": f"fz:{i}:{tool}", "tool": name, "input": js}, ensure_ascii=False) + "\n"); n += 1
k = 0
for _ in range(400):   # random multi-byte soup, 1..2 000 characters
    L = R.choice([1, 2, 5, 50, 300, 999, 1199, 1200, 1201, 2000]); add(f"soup{k}", "".join(R.choice(ALPH) for _ in range(L))); k += 1
for pos in range(1185, 1206):   # an escape cut at the window's end, in several spellings
    for tail in ["\\", "\\u", "\\u00", "\\ud800", "\x01", "\"", "\n", "😀", "é\\", "$'\\x", "@", "{"]:
        add(f"cut{pos}:{tail.encode('unicode_escape').decode()}", "x" * pos + tail + " .env"); k += 1
for ch in ["@", "{", "}", "\\", "'", "\"", "$'", "-", "/", "@.", "{,", "\x01", "😀", "​"]:
    for L in [600, 1200, 5000]:
        add(f"run:{ch.encode('unicode_escape').decode()}:{L}", ch * L)
add("lone surrogate text", "a \\ud800 b \\udfff .env \\ud83d\\ude00")
print("fuzz rows", n)
