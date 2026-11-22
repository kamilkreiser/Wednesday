#!/usr/bin/env python3
"""QA-WIN-FOLLOWUP names scan: every ADDED line of `git diff <base>...<head>` (or the files given with --files),
case-insensitive, for person, machine, account, network, client and path names. Patterns base64-encoded.
Usage: names_scan.py <repo> <base> <head> | names_scan.py --files f1 f2 ...   [--control]"""
import base64, re, subprocess, sys
PATS = [re.compile(base64.b64decode(e).decode(), re.I) for e in ['c21hc2hob21l', 'XGJrcmVpcw==', 'a3JlaXNlcg==', 'XGJrYW1pbA==', 'XGJrYW1cYg==', 'Y2FtZWxsaWE=', 'MTkyXC4xNjhcLg==', 'MTBcLjBcLjBcLjFcYg==', 'YzpcXCtjMmM=', 'YzovYzJj', 'YzpcXCt3ZlsxMl1cYg==', 'YzpcXCt3ZGM3', 'YzpcXCt3ZGp0', 'YzpcXCt3ZGNj', 'YzpcXCtxYVsxMl1cYg==', 'bGFwdG9wLWRldg==', 'L3ZvbHVtZXMv', 'L3ByaXZhdGUvdG1w', 'L3VzZXJzL1thLXpd', 'YzpcXCt1c2Vyc1xcKyg/IWFublxifGFublxcfGFubnh8Ym9ifGFubmF8w6lsYW580LTQvtC8fHByb2Yp', 'ZnJpZGF5', 'ZGF0YXNlYw==', 'c2VjdXVyYQ==', 'YWdlbnRtYWls', 'QFthLXowLTktXStcLihjb218b3JnfGF1fHRvKVxi', 'bm9yZXBseQ==', 'dHVlc2RheQ==', 'd2VkbmVzZGF5', 'XGJ0OVxi', 'b25lZHJpdmU=', 'aWNsb3Vk']]
args = [a for a in sys.argv[1:] if a != "--control"]
lines = []
if args and args[0] == "--files":
    for f in args[1:]:
        for i, l in enumerate(open(f, encoding="utf-8", errors="replace"), 1):
            lines.append((f"{f.rsplit('/',1)[-1]}:{i}", l.rstrip("\n")))
else:
    repo, base, head = args
    d = subprocess.run(["git", "-C", repo, "diff", "-U0", f"{base}...{head}"], capture_output=True, text=True).stdout
    cur = "?"
    for l in d.splitlines():
        if l.startswith("+++ "):
            cur = l[6:]
        elif l.startswith("+") and not l.startswith("+++"):
            lines.append((cur, l[1:]))
if "--control" in sys.argv:
    for e in ['c21hc2hob21l', 'XGJrcmVpcw==', 'a3JlaXNlcg==', 'XGJrYW1pbA==', 'XGJrYW1cYg==', 'Y2FtZWxsaWE=', 'MTkyXC4xNjhcLg==', 'MTBcLjBcLjBcLjFcYg==', 'YzpcXCtjMmM=', 'YzovYzJj', 'YzpcXCt3ZlsxMl1cYg==', 'YzpcXCt3ZGM3', 'YzpcXCt3ZGp0', 'YzpcXCt3ZGNj', 'YzpcXCtxYVsxMl1cYg==', 'bGFwdG9wLWRldg==', 'L3ZvbHVtZXMv', 'L3ByaXZhdGUvdG1w', 'L3VzZXJzL1thLXpd', 'YzpcXCt1c2Vyc1xcKyg/IWFublxifGFublxcfGFubnh8Ym9ifGFubmF8w6lsYW580LTQvtC8fHByb2Yp', 'ZnJpZGF5', 'ZGF0YXNlYw==', 'c2VjdXVyYQ==', 'YWdlbnRtYWls', 'QFthLXowLTktXStcLihjb218b3JnfGF1fHRvKVxi', 'bm9yZXBseQ==', 'dHVlc2RheQ==', 'd2VkbmVzZGF5', 'XGJ0OVxi', 'b25lZHJpdmU=', 'aWNsb3Vk']:
        pass
    lines.append(("CONTROL", base64.b64decode("cGxhbnRlZDogU01BU0hIT01FIEM6XFVzZXJzXGtyZWlzXHggL1ZvbHVtZXMvTGFwdG9wLURFViBrYW1pbC5rcmVpc2VyIEM6XGMyY1xmMSAxOTIuMTY4LjQuMjM=").decode()))
hits = 0
for where, l in lines:
    for p in PATS:
        m = p.search(l)
        if m:
            hits += 1
            print(f"HIT {where}: pattern #{PATS.index(p)} matched {len(m.group(0))} chars")
            break
print(f"scanned {len(lines)} lines, {hits} hits")
