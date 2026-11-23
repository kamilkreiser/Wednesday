"""QA-W-GATE-TEST: extract every '===== <path> WHOLE =====' block from saved PC mails (read-only inputs)."""
import json, re, sys
HDR = re.compile(r'^===== (?P<path>\S+) WHOLE =====\s*$')
def blocks(files):
    out = []
    for fn in files:
        cur = None
        for i, line in enumerate(open(fn, encoding="utf-8"), 1):
            m = HDR.match(line.rstrip("\n"))
            if m:
                cur = {"file": fn, "line": i, "path": m.group("path"), "body": []}
                out.append(cur)
            elif line.startswith("=====") and cur is not None:
                cur = None
            elif cur is not None:
                cur["body"].append(line.rstrip("\n"))
    return out
def parse(b):
    p = b["path"].replace("\\", "/")
    body = b["body"]
    # trailing blank lines / text after JSON
    if p.endswith("verdict.json"):
        txt = "\n".join(body)
        dec = json.JSONDecoder()
        s = txt.lstrip()
        obj, end = dec.raw_decode(s)
        rest = s[end:].strip()
        return p, obj, rest
    if p.endswith("daemon.jsonl"):
        objs, rest = [], []
        for l in body:
            l2 = l.strip()
            if not l2:
                continue
            try:
                objs.append(json.loads(l2))
            except ValueError:
                rest.append(l2)
        return p, objs, "\n".join(rest)
    return p, body, ""
if __name__ == "__main__":
    for b in blocks(sys.argv[1:]):
        p, o, rest = parse(b)
        print(b["file"].split("/")[-1], b["line"], p, type(o).__name__, len(o), "REST:" + rest[:200].replace("\n", " | ") if rest else "")
