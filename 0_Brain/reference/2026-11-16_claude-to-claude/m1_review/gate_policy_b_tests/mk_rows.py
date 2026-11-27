# QA-POLICY-B: build the check's row files (C1 and the item 3, 4, 6 rows). python3 -B mk_rows.py <out dir>
# C1 = every probe row of the POLICY-AT check (zz_qpx_probe.rs, its literals parsed), every row of the POLICY-WORDS
# check (rows_free/cross/misc/big.jsonl), every string literal of t28_at_names.rs through four tools, and the t29 rows
# re-made from its formulas. Item 3 = ordinary corpus (the check's own kinds); item 4 = hostile spellings; item 6 =
# web fetch rows. Every secret-shaped or address-shaped string is made up.
import json, os, re, sys

OUT = sys.argv[1]
H = "/private/tmp/claude-501/qpb"
COPY = H + "/c1src"  # copies of the earlier checks' files (cmp-silent against their originals)
HEAD = H + "/head/crates/coagent-policy/tests"

def unrust(s):
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            n = s[i + 1]
            if n == "n": out.append("\n"); i += 2; continue
            if n == "t": out.append("\t"); i += 2; continue
            if n == "r": out.append("\r"); i += 2; continue
            if n == "0": out.append("\0"); i += 2; continue
            if n == "\\": out.append("\\"); i += 2; continue
            if n == '"': out.append('"'); i += 2; continue
            if n == "'": out.append("'"); i += 2; continue
            if n == "u" and s[i + 2:i + 3] == "{":
                j = s.index("}", i); out.append(chr(int(s[i + 3:j], 16))); i = j + 1; continue
            if n == "x": out.append(chr(int(s[i + 2:i + 4], 16))); i += 4; continue
            if n == "\n":
                i += 2
                while i < len(s) and s[i] in " \t": i += 1
                continue
        out.append(c); i += 1
    return "".join(out)

LIT = r'"((?:[^"\\]|\\.)*)"'

rows = []
def add(rid, tool, text=None, inp=None, cwd=None, names=None, grp="C1", full=False):
    r = {"id": rid, "grp": grp, "tool": tool}
    if inp is not None: r["input"] = inp
    else: r["text"] = text
    if cwd: r["cwd"] = cwd
    if names: r["names"] = names
    if full: r["full"] = True
    rows.append(r)

# --- POLICY-AT check probe (zz_qpx_probe.rs) -------------------------------------------------------------------
src = open(COPY + "/zz_qpx_probe.rs").read()
cwdmap = {"ws": "ws", "home": "home", "outside2": "outside", "outside": "outside"}
n = 0
for m in re.finditer(r'for c in \[(.*?)\]\s*\{\s*v\.push\(\("(\w+)", "(\w+)", (\w+)\.clone\(\), c\)\);', src, re.S):
    for lit in re.findall(LIT, m.group(1)):
        add(f"qpx:{m.group(2)}:{n}", m.group(3), unrust(lit), cwd=cwdmap[m.group(4)]); n += 1
for m in re.finditer(r'v\.push\(\("(\w+)", "(\w+)", ([^;]*?), ' + LIT + r'\)\);', src):
    expr = m.group(3)
    cwd = {"home.clone()": "home", "outside2.clone()": "outside", "outside.clone()": "outside", 'PathBuf::from("/")': "slash",
           'PathBuf::from("")': "empty", 'PathBuf::from("rel")': "rel", 'ws.join("src")': "src"}.get(expr.strip(), "ws")
    add(f"qpx:{m.group(1)}:{n}", m.group(2), unrust(m.group(4)), cwd=cwd); n += 1
blk = re.search(r'for \(tool, c\) in \[(.*?)\]\s*\{', src, re.S).group(1)
for t, c in re.findall(r'\(' + LIT + r',\s*' + LIT + r'\)', blk):
    add(f"qpx:M:{n}", unrust(t), unrust(c)); n += 1
for m in re.finditer(r'for tool in \[([^\]]*)\]\s*\{(.*?)\n    \}', src, re.S):
    tools = [unrust(x) for x in re.findall(LIT, m.group(1))]
    for c in re.findall(r'json!\(\{ "command": ' + LIT + r' \}\)', m.group(2)):
        for t in tools:
            add(f"qpx:E:{n}", t, unrust(c)); n += 1
add("qpx:B:grep", "Grep", inp={"path": "<ws>", "pattern": "key"})
add("qpx:B:glob", "Glob", inp={"path": "<ws>", "pattern": "src/.e*"})
add("qpx:Bv:grep", "Grep", inp={"path": "<ws>/src", "pattern": "key"})
n_qpx = len(rows)

# --- POLICY-WORDS check rows ----------------------------------------------------------------------------------
for f in ["rows_free", "rows_cross", "rows_misc", "rows_big"]:
    for l in open(f"{COPY}/{f}.jsonl"):
        r = json.loads(l)
        x = {"id": "qpw:" + r["id"], "grp": "C1", "tool": r["tool"]}
        if "input" in r: x["input"] = r["input"]
        else: x["text"] = r["text"]
        if r.get("cwd"): x["cwd"] = r["cwd"]
        rows.append(x)
n_qpw = len(rows) - n_qpx

# --- t28: every string literal of a test body, through four tools ------------------------------------------------
t28 = open(HEAD + "/t28_at_names.rs").read()
lits = set()
for lit in re.findall(LIT, t28):
    u = unrust(lit)
    if len(u) >= 3 and "{" not in u.replace("{a,", "").replace("{1", "")[:0] and not u.startswith("T28") and "\n" not in u[:1]:
        lits.add(u.replace("<home>", "<home>"))
lits = sorted(lits)
for i, u in enumerate(lits):
    for t in ["Bash", "PowerShell", "WebSearch", "Agent"]:
        add(f"t28lit:{i}:{t}", t, u)
for nn in range(150, 261):
    for t in ["WebSearch", "Agent", "mcp__github__create_issue", "MadeUpTool", "WebFetch"]:
        add(f"t28cnt:{nn}:{t}", t, " ".join(f"w{i}" for i in range(nn)) + " .env", names=[".env"])
n_t28 = len(rows) - n_qpx - n_qpw

# --- t29 re-made ------------------------------------------------------------------------------------------------
T5 = ["WebSearch", "Agent", "mcp__github__create_issue", "MadeUpTool", "WebFetch"]
for t in T5:
    for text in ["see\n.env", "a\t.env", "a\r.env", "a\b.env", "a\f.env", "a\u0001.env", 'say "x".env', "c:\\.env", "a .env", "see\n .env"]:
        add(f"t29esc:{t}:{text!r}", t, text, names=[".env"], full=True)
for form in ["w", "kv", "colon", "comma"]:
    for t in T5:
        for nn in range(0, 260):
            if t not in ("WebSearch", "Agent") and nn % 3: continue
            w = "".join({"w": f"w{i} ", "kv": f"k{i}=v{i} ", "colon": f"k{i}:v{i} ", "comma": f"a{i},b{i} "}[form] for i in range(nn))
            add(f"t29vis:{form}:{t}:{nn}", t, w + ".env", names=[".env"])
for p in [".env", "summarise the file .env for me", "see\n.env", "read secret/plan.txt", {"x": ".env"}, [1, "a .env"],
          "w" * 1200 + " .env", "summarise .env for me", "plain words only"]:
    add(f"t29fetch:{json.dumps(p)[:40]}", "WebFetch", inp={"url": "https://example.com/", "prompt": p}, names=[".env", "secret/plan.txt"], full=True)

def fill(unit, sep, target=1300):
    s, i = "", 0
    while len(s) < target:
        if i: s += sep
        s += unit(i); i += 1
    return s

W48 = ["review", "release", "notes", "planned", "because", "several", "sections", "rewritten", "meeting", "Thursday",
       "afternoon", "summary", "everyone", "attend", "figures", "table", "totals", "March", "April", "lunch", "questions",
       "follow", "budget", "vendor", "contract", "signed", "draft", "printer", "office", "laptop", "monitor", "keyboard",
       "network", "server", "backup", "restore", "quarter", "report", "forecast", "hiring", "onboarding", "training",
       "holiday", "schedule", "customer", "feedback", "survey", "results"]
P4 = ["The quick review of the release notes took longer than planned, because several sections had to be rewritten.",
      "We agreed to move the meeting to Thursday afternoon and to send the summary to everyone who could not attend.",
      "Please check the figures in the second table again; the totals for March and April do not add up.",
      "After lunch the team walked through the open questions one by one and wrote down who would follow up on each."]
T29C = {
    "prose, no repeat": fill(lambda i: f"{W48[i % 48]}{i // 48}", " "),
    "prose": fill(lambda i: P4[i % 4], " "),
    "code with flags and paths": fill(lambda i: [f"cargo build --release --target x86_64-unknown-linux-gnu -p core{i}",
        f"rustc -C opt-level=3 -o target/release/app{i} src/main.rs", f'let path = std::path::Path::new("/srv/app/data/file{i}.json");',
        f'if !path.exists() {{ eprintln!("missing: {{}}", path.display()); std::process::exit({i}); }}'][i % 4], "\n"),
    "file listing": fill(lambda i: f"-rw-r--r--  1 dev  staff  {1000 + i * 37} Nov 26 10:{i % 60:02} src/module_{i}/file_{i}.rs", "\n"),
    "shell transcript": fill(lambda i: [f"$ cd ~/projects/app{i} && git status", "On branch main", "nothing to commit, working tree clean",
        f"$ ls -la ./build/out{i}", f"total {8 * i}", f"$ grep -rn TODO src/ | head -n {i}"][i % 6], "\n"),
    "json blob": fill(lambda i: f'{{"id": {i}, "name": "item-{i}", "tags": ["a{i}", "b{i}"], "path": "/var/lib/app/items/{i}.dat", "ok": true}}', ", "),
    "web addresses": fill(lambda i: f"https://docs.example.com/guide/section-{i}/page.html?lang=en#part{i}", "\n"),
    "mail addresses": fill(lambda i: f"person{i}.surname@mail{i % 7}.example.org", ", "),
    "stack trace": fill(lambda i: [f'  File "/srv/app/pkg/module{i}.py", line {10 + i}, in handler_{i}', f"    result = process(item_{i}, timeout=30)",
        f"    at com.example.app.service.Worker{i}.run(Worker{i}.java:{40 + i})"][i % 3], "\n"),
    "markdown table": "| name | path | size |\n|---|---|---|\n" + fill(lambda i: f"| item{i} | /data/set{i}/part{i}.csv | {10 + i} KB |", "\n"),
    "--flag=/a/b/c words": fill(lambda i: f"--input{i}=/data/in/batch{i}/file.csv", " "),
    "bullets: file paths": fill(lambda i: f"- src/module{i}/handlers/file{i}.rs", "\n"),
    "bullets: deep paths": fill(lambda i: f"- /srv/app/src/pkg{i}/sub/dir/file{i}.txt", "\n"),
    "bullets: web addresses": fill(lambda i: f"- https://docs.example.com/guide/section-{i}/page.html", "\n"),
    "bullets: prose": fill(lambda i: f"- point {i}: we should check the release notes again before the review", "\n"),
    "--verbose then a listing": "--verbose output follows\n" + fill(lambda i: f"-rw-r--r--  1 dev  staff  {1000 + i} Nov 26 src/module_{i}/file_{i}.rs", "\n"),
    "heading then deep-path bullets": "Files to change:\n" + fill(lambda i: f"- /srv/app/src/pkg{i}/sub/dir/file{i}.txt", "\n"),
    "deep-path lines, no bullet": fill(lambda i: f"/srv/app/src/pkg{i}/sub/dir/file{i}.txt", "\n"),
    "json nested": fill(lambda i: f'{{"user": {{"id": {i}, "name": "Ann {i}", "roles": ["admin", "dev"], "address": {{"city": "Oslo", "zip": "0{150 + i}"}}}}, "items": [{{"sku": "A-{i}", "qty": 2}}, {{"sku": "B-{i}", "qty": 1}}]}}', ",\n"),
    "css and shell braces": fill(lambda i: [f".card-{i} {{ margin: 0 auto; padding: {i % 9}px; }}", f'for f in *.txt; do {{ echo "$f"; }}; done # pass {i}',
        f"function build_{i}() {{ npm run build -- --env=prod; }}"][i % 3], "\n"),
    "mails and @ mentions": fill(lambda i: f"Thanks @anna{i} and @ben.k, please mail anna{i}.berg@example.org or ben.k@mail{i % 5}.example.com about issue #{i}; cc @team-docs.", " "),
    "shell brace expansion": fill(lambda i: f"mkdir -p build{i}/{{debug,release}}/logs && cp src/{{main,lib}}.rs backup{i}/", "\n"),
    "diff hunk": fill(lambda i: [f"--- a/src/mod{i}/lib.rs", f"+++ b/src/mod{i}/lib.rs", f"@@ -{i},7 +{i},8 @@",
        f'-    let x = load("/etc/app/{i}.toml");', f'+    let x = load("/etc/app/{i}.d/main.toml");'][i % 5], "\n"),
}
for k, txt in T29C.items():
    for t in T5:
        add(f"t29corp:{k}:{t}", t, txt)
        mid = len(txt) // 2
        add(f"t29corp+name900:{k}:{t}", t, txt[:880] + " .env " + txt[880:], names=[".env"])
        add(f"t29corp+secret900:{k}:{t}", t, txt[:880] + " secret/plan.txt " + txt[880:], names=["secret/plan.txt"])
# the builder's fifteen refused built families (bounds row), each through WebSearch and a web fetch prompt
FAM = {
    "a@b@c": "@".join(chr(97 + (i % 26)) for i in range(650))[:1300],
    "brace words x{a..h}": " ".join(f"x{i}{{a,b,c,d,e,f,g,h}}" for i in range(80)),
    "-/a/a/": "-" + "/a" * 599,
    "-////": "-" + "/" * 1199,
    "-~~~~": "-" + "~" * 1199,
    "-/~@a": "-" + "/~@a" * 299,
    "two -/~@a": "-" + "/~@a" * 150 + " -" + "/~@b" * 148,
    "word of @": "@" * 1200,
    "@a/@a/": "@a/" * 400,
    "-/a<i>/b/c{1..8} words": " ".join(f"-/a{i}/b/c{{1,2,3,4,5,6,7,8}}" for i in range(40)),
    "-/a/a half": "-" + "/a" * 300,
    "-/a/a 0.7": "-" + "/a" * 420,
    "-{1..8}////": "-{1,2,3,4,5,6,7,8}" + "/" * 1180,
    "-/@a{1..8}": "-" + "/@a" * 380 + "{1,2,3,4,5,6,7,8}",
    "-/~@a + $'": "-" + "/~@a" * 150 + " $'\\x2d" + "/~@b" * 140 + "'",
}
for k, txt in FAM.items():
    for t in ["WebSearch", "Agent", "WebFetch", "MadeUpTool", "mcp__github__create_issue"]:
        add(f"fam:{k}:{t}", t, txt)
n_t29 = len(rows) - n_qpx - n_qpw - n_t28
with open(f"{OUT}/rows_c1.jsonl", "w") as f:
    for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"C1 rows: POLICY-AT probe {n_qpx}, POLICY-WORDS {n_qpw}, t28 {n_t28}, t29 + families {n_t29}; total {len(rows)}")
