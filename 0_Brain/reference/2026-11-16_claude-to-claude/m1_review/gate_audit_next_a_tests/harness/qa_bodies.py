# Extract fn bodies (from the `fn name` line to its matching brace; strings, chars, comments skipped)
# at base and head; sha256[:16]. usage: python3 -B qa_bodies.py <clone> <path> name...
import hashlib, re, subprocess, sys
C, P = sys.argv[1], sys.argv[2]; names = sys.argv[3:]
B = "5e11609cee1cb483bd006547e9092d49522691cc"; H = "d79ae1ca194fbe354ca8be594b9c76325f1b6eb0"
def src(sha): return subprocess.run(["git","-C",C,"show",f"{sha}:{P}"],capture_output=True,check=True).stdout.decode()
def body(s, name):
    m = list(re.finditer(r"(?m)^[ \t]*(pub(\([a-z]+\))? )?fn " + re.escape(name) + r"\b", s))
    if len(m) != 1: return None, f"{len(m)} defs"
    i = m[0].start(); j = s.index("{", m[0].end()); depth = 0; k = j
    while k < len(s):
        c = s[k]
        if s.startswith("//", k): k = s.index("\n", k); continue
        if s.startswith("/*", k): k = s.index("*/", k) + 2; continue
        if c == '"':
            k += 1
            while s[k] != '"':
                k += 2 if s[k] == "\\" else 1
            k += 1; continue
        if c == "'" and re.match(r"'(\\.|[^\\'])'", s[k:k+4]):
            k = s.index("'", k+2) + 1 if s[k+1] != "\\" else s.index("'", k+3) + 1; continue
        if c == "{": depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0: return s[i:k+1], None
        k += 1
    return None, "unclosed"
sb, sh = src(B), src(H)
for n in names:
    b, eb = body(sb, n); h, eh = body(sh, n)
    if b is None or h is None: print(f"{n}: ERROR base={eb} head={eh}"); continue
    hb = hashlib.sha256(b.encode()).hexdigest()[:16]; hh = hashlib.sha256(h.encode()).hexdigest()[:16]
    print(f"{'SAME' if b == h else 'DIFF'} {n}: base {hb} ({b.count(chr(10))+1} lines) head {hh} ({h.count(chr(10))+1} lines)")
