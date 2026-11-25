# QA-POLICY-AT item 8 (n-6): (1) the head t27's 42 new asserts, parsed BY PROGRAM, against the parent check's own case
# file (cases.json: texts) and its cargo answers (cargo.txt): text for text, and `want` = cargo's answer except the four
# pinned false positives N5, N6, N7, N8; (2) the base and head `depends_on_policy` extracted VERBATIM by program into a
# scratch Rust file and run over the 42 texts plus the check's own extra texts (the head must accept every text the base
# accepts that cargo calls a dependent, and must not accept the root member line).
# usage: python3 -B -I n6_check.py <t27 base> <t27 head> <cases.json> <cargo.txt> <workdir>
import sys, re, json, os, subprocess
t27b, t27h, casesf, cargof, work = sys.argv[1:6]
os.makedirs(work, exist_ok=True)

def unesc(s):
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == '\\':
            n = s[i + 1]
            out.append({'n': '\n', 't': '\t', '\\': '\\', '"': '"', "'": "'"}[n]); i += 2; continue
        out.append(c); i += 1
    return ''.join(out)

head = open(t27h).read()
blk = head[head.index('// POLICY-AT item 3 (n-6): the check\'s 42 manifest texts'):]
blk = blk[:blk.index('] {')]
asserts = [(unesc(m.group(1)), m.group(2) == 'true') for m in re.finditer(r'\(\s*"((?:[^"\\]|\\.)*)",\s*(true|false)\s*\)', blk)]
cases = json.load(open(casesf))
cargo = {}
for l in open(cargof):
    p = l.rstrip('\n').split('\t')
    if len(p) >= 3 and p[0] == 'CARGO':
        cargo[p[1]] = p[2]
print("asserts parsed:", len(asserts), "cases:", len(cases))
bad = 0
for (cid, kind, text), (atext, want) in zip(cases, asserts):
    dep = cargo[cid].startswith('DEPENDS')
    exp = dep or cid.split('-')[0] in ('N5', 'N6', 'N7', 'N8')
    ok = (text == atext) and (want == exp)
    if not ok:
        bad += 1
        print("MISMATCH", cid, repr(text)[:80], repr(atext)[:80], want, exp)
print(f"(1) text and answer equal to the parent's table + cargo, FPs N5-N8 pinned true: {len(asserts) - bad} of {len(asserts)}; mismatches {bad}")

def extract(src):
    i = src.index('fn depends_on_policy(manifest: &str) -> bool {')
    j = src.index('\n}\n', i)
    return src[i:j + 3]
fb = extract(open(t27b).read()).replace('fn depends_on_policy', 'fn dep_base', 1)
fh = extract(open(t27h).read()).replace('fn depends_on_policy', 'fn dep_head', 1)
EXTRA = [
    ("X1-header-bracket-comment", "pos", "[dependencies.coagent-policy] # ] x\npath = \"../coagent-policy\""),
    ("X2-dotted-after-header", "neg", "[package]\nname = \"x2\"\nversion = \"0.0.0\"\nedition = \"2021\"\ndependencies.coagent-policy.path = \"../coagent-policy\""),
    ("X3-top-build-dotted", "pos-top", "build-dependencies.coagent-policy = { path = \"../coagent-policy\" }"),
    ("X4-top-target-quoted-dev", "pos-top", "target.\"cfg(unix)\".dev-dependencies.coagent-policy.path = \"../coagent-policy\""),
    ("X5-quoted-package-tight", "pos", "[dependencies]\npolicy = {\"package\"=\"coagent-policy\",path=\"../coagent-policy\"}"),
    ("X6-literal-triple", "pos", "[dependencies.p]\npackage = '''coagent-policy'''\npath = \"../coagent-policy\""),
    ("X7-cfg-bracket-quote", "pos", "[target.'cfg(target_os = \"]\")'.dependencies.coagent-policy]\npath = \"../coagent-policy\""),
    ("X8-top-quoted-table", "pos-top", "\"dependencies\".coagent-policy.path = \"../coagent-policy\""),
    ("X9-single-quoted-key", "pos", "[dependencies]\n'coagent-policy' = { path = \"../coagent-policy\" }"),
    ("X10-members-inline", "ws-root", "members = [\"crates/coagent-policy\"]"),
    ("X11-top-inline-table", "pos-top", "dependencies = { coagent-policy = { path = \"../coagent-policy\" } }"),
    ("X12-version-only", "pos", "[dependencies]\ncoagent-policy = { version = \"0.0.1\", path = \"../coagent-policy\" }"),
    ("X13-header-target-dev-quoted-escape", "pos", "[target.\"cfg(target_os = \\\"a]b\\\")\".dev-dependencies.coagent-policy]\npath = \"../coagent-policy\""),
    ("X14-top-dev-underscore", "pos-top", "dev_dependencies.coagent-policy.path = \"../coagent-policy\""),
    ("X15-comment-before-header", "pos-top", "# comment\ndependencies.coagent-policy.path = \"../coagent-policy\""),
]
allc = [(c[0], c[1], c[2]) for c in cases] + EXTRA
json.dump(EXTRA, open(os.path.join(work, 'extra_cases.json'), 'w'), indent=0)
rs = os.path.join(work, 'deptab_at.rs')
with open(rs, 'w') as f:
    f.write("// QA-POLICY-AT n-6 scratch: the base and head depends_on_policy, extracted verbatim by program.\n#![allow(dead_code)]\n")
    f.write(fb + "\n" + fh + "\n")
    f.write("fn main() {\n    let s = std::fs::read_to_string(std::env::args().nth(1).unwrap()).unwrap();\n"
            "    for c in s.split('\\u{1e}') { if c.is_empty() { continue; } println!(\"{}\\t{}\", dep_base(c), dep_head(c)); }\n}\n")
with open(os.path.join(work, 'texts.bin'), 'w') as f:
    for _, _, t in allc:
        f.write(t + '\x1e')
r = subprocess.run(['rustc', '--edition', '2021', '-O', '-o', os.path.join(work, 'deptab_at'), rs], capture_output=True, text=True)
assert r.returncode == 0, r.stderr
out = subprocess.run([os.path.join(work, 'deptab_at'), os.path.join(work, 'texts.bin')], capture_output=True, text=True).stdout.split('\n')
rows = []
for (cid, kind, text), l in zip(allc, out):
    b, h = l.split('\t')
    rows.append((cid, kind, text, b == 'true', h == 'true'))
json.dump(rows, open(os.path.join(work, 'deptab_at.json'), 'w'), indent=0)
lost = [r[0] for r in rows if r[3] and not r[4]]
print("(2) texts", len(rows), "; base true -> head false:", lost)
print("    root member line N1 head:", [r[4] for r in rows if r[0].startswith('N1')], " X10 head:", [r[4] for r in rows if r[0].startswith('X10')])
for r in rows:
    print(f"    {r[0]:40s} base={str(r[3]):5s} head={str(r[4]):5s}")
