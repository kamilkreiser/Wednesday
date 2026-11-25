# QA-POLICY-NOTES (g): the clarifications file against the addendum and the build brief, by program.
import sys, re
F, A, B = sys.argv[1], sys.argv[2], sys.argv[3]
f = open(F, encoding="utf-8").read(); fb = open(F, "rb").read()
a = open(A, encoding="utf-8").read(); b = open(B, encoding="utf-8").read()
print("file bytes", len(fb))
# the addendum's four quoted lines (backticked), in its section 3 item 5
want = re.findall(r"`(Decision general-c2c-[^`]+)`", a)
want = list(dict.fromkeys(want))
heads = [(m.start(), m.group(0)) for m in re.finditer(r"^## C-\d+ .*$", f, re.M)]
print("headings", [h for _, h in heads])
for n, w in zip((9, 10, 11, 12), want):
    i = f.index(f"## C-{n} ")
    j = f.find("\n## C-", i + 5); j = len(f) if j < 0 else j
    body = f[i:j]
    q = [l[2:] for l in body.splitlines() if l.startswith("> ")]
    ok = q == [w]
    print(f"C-{n}: quoted {len(q)} line(s); equal to the addendum's byte for byte: {ok}; chars {len(q[0])} bytes {len(q[0].encode())}; dash U+2014 count {q[0].count(chr(0x2014))}; heading {body.splitlines()[0]}")
# the addendum's lengths and times
print("addendum quoted lines:", [(len(w), w[:40]) for w in want])
# earlier entries: C-2, C-5, C-6 words as the build brief quotes them
for cid, pat in (("C-2", r'C-2: "([^"]+)"'), ("C-5 detail", r"option a's detail: \"([^\"]+)\""), ("C-5 words", r'his words: "([^"]+)"'), ("C-6 12:34:16", r'C-6 \(12:34:16\): "([^"]+)"'), ("C-6 12:35:07", r'\(12:35:07\): "([^"]+)"')):
    m = re.search(pat, b)
    s = m.group(1)
    print(f"{cid}: brief quote {len(s)} chars; found byte for byte in the file: {s in f}")
# the first part ends cleanly after C-8: everything before '## C-9' ends with exactly one newline after C-8's text
i9 = f.index("## C-9 ")
pre = fb[: len(f[:i9].encode())]
print("prefix up to '## C-9' bytes", len(pre), "ends with", repr(pre[-120:]))
