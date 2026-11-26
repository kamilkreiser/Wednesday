# QA-POLICY-WORDS property (e): parse the one phrase array of t25::docs_name_the_owner_origin, unescape, compare, count.
# usage: python3 -B -I phr.py            (base vs head from git)
#        python3 -B -I phr.py <t25 file>  (control: compare a scratch t25 against the head's array)
import subprocess, sys, re
C = "/private/tmp/claude-501/qpw/clone"
B, H = "2004a04ebba7e1d031dfa341da26f76693345aff", "821cae22525785e0771f0d2deb7bed4b24b2a4af"
def show(sha, p): return subprocess.run(["git", "-C", C, "show", f"{sha}:{p}"], capture_output=True, check=True).stdout.decode()
def unescape(s):
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c != "\\": out.append(c); i += 1; continue
        n = s[i + 1]
        if n == "\n":                      # line continuation: skip newline and leading whitespace
            i += 2
            while i < len(s) and s[i] in " \t\n\r": i += 1
            continue
        m = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", '"': '"', "'": "'", "0": "\0"}
        if n in m: out.append(m[n]); i += 2; continue
        if n == "u":
            j = s.index("}", i); out.append(chr(int(s[i + 3:j], 16))); i = j + 1; continue
        raise ValueError("unknown escape " + n)
    return "".join(out)
def phrases(src):
    f = src.index("fn docs_name_the_owner_origin")
    a = src.index("for phrase in [", f) + len("for phrase in [")
    e = src.index("] {", a)
    body = src[a:e]
    lits, i = [], 0
    while i < len(body):
        c = body[i]
        if c == '"':
            j = i + 1
            while body[j] != '"':
                j += 2 if body[j] == "\\" else 1
            lits.append(unescape(body[i + 1:j])); i = j + 1
        elif body.startswith("//", i):
            i = body.index("\n", i)
        else:
            if c not in " \t\n\r,": raise ValueError(f"unexpected {c!r} at {i}")
            i += 1
    return lits
T25 = "crates/coagent-policy/tests/t25_owner_allow.rs"
if len(sys.argv) > 1:
    pb, ph = phrases(show(H, T25)), phrases(open(sys.argv[1]).read())
    print("CONTROL len", len(pb), len(ph), "differing positions (1-based):", [i + 1 for i in range(len(pb)) if pb[i] != ph[i]])
    sys.exit()
pb, ph = phrases(show(B, T25)), phrases(show(H, T25))
db, dh = show(B, "docs/POLICY.md"), show(H, "docs/POLICY.md")
print("array length base", len(pb), "head", len(ph))
diff = [i for i in range(max(len(pb), len(ph))) if pb[i] != ph[i]]
print("differing positions (1-based):", [i + 1 for i in diff])
for i in range(len(ph)):
    flag = "" if pb[i] == ph[i] else "  <-- CHANGED"
    print(f"{i+1:2d} base_in_base={db.count(pb[i])} head_in_head={dh.count(ph[i])} base_phrase_in_head={dh.count(pb[i])}{flag}")
for i in diff:
    print("OLD", repr(pb[i])); print("NEW", repr(ph[i]))
    k = dh.index(ph[i]); ln = dh[:k].count("\n") + 1
    print(f"NEW found at head POLICY.md line {ln}; context lines {ln-3}..{ln+2}:")
    print("\n".join(dh.splitlines()[ln-4:ln+2]))
