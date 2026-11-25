# Writes a Rust module with every backtick span of docs/SCANNER.md (base and head, deduplicated),
# each also with <ESC> replaced by the ESC byte, and the 47 s5_forms_rows of the SCANNER-NOTES check.
import sys, re, subprocess
clone, out, cases = sys.argv[1], sys.argv[2], sys.argv[3]
spans = []
for sha in ("debbb4442fc90b1d5c1f04f123a665dcd8cf381f", "dd70630dd74cd1dac9261f1ac83542514562c767"):
    t = subprocess.run(["git", "-C", clone, "show", sha + ":docs/SCANNER.md"], capture_output=True, text=True, check=True).stdout
    for m in re.finditer(r"``(.+?)``|`([^`\n]+)`", t):
        s = (m.group(1) or m.group(2)).strip() if m.group(1) else m.group(2)
        for v in (s, s.replace("<ESC>", "\x1b")):
            if v not in spans: spans.append(v)
def lit(s):
    o = []
    for ch in s:
        if ch == "\\": o.append("\\\\")
        elif ch == '"': o.append('\\"')
        elif 32 <= ord(ch) < 127: o.append(ch)
        else: o.append("\\u{%x}" % ord(ch))
    return '"' + "".join(o) + '"'
src = open(cases).read()
a = src.index("let rows: &[(&str, &str)] = &[", src.index("fn s5_forms_rows"))
b = src.index("    ];", a)
rows = src[a:b].split("= &[", 1)[1]
with open(out, "w") as f:
    f.write("//! QA-SCANNER-NEXT: docs/SCANNER.md backtick spans (base and head) and the SCANNER-NOTES check's 47 rows.\n")
    f.write("pub const DOC_SPANS: &[&str] = &[\n" + "".join("    %s,\n" % lit(s) for s in spans) + "];\n")
    f.write("pub const S5_ROWS: &[(&str, &str)] = &[" + rows + "];\n")
print(len(spans), "doc spans;", rows.count("(\""), "rows")
