#!/bin/bash
# build_bash_input2.sh <KS-id> <out input.json> <brief.md> ref=<existing *.test.sh> [pin=value ...] — the bash_patch2
# (MULTI-FILE bash) input (2026-10-07, rung 3; Wednesday's commission "open rung 3": KS-1274 is 1 script + 3 suites).
#
# The brief HEADER (the lines before the first `## `) declares the touched set:
#   File: `<script>`                                   1-3 product files, each modified in place (first = `product_file`)
#   Test file: `<suite>.test.sh`  (MODIFIED|NEW, RED|SUPPORT …)   1-4 test files, all in ONE test dir (the ref's)
#     RED      = must FAIL with the test edits alone and PASS with the product edits on top (>= 1 RED; a NEW test is RED)
#     SUPPORT  = an existing suite edited to the new contract (e.g. a stub): must PASS with the test edits alone AND after
# and the brief's fences carry EVERY declared file's lines, attributable by `+++ b/<path>` headers: the products' hunks
# under `## The exact change` (ONLY products there), the tests' hunks under `## The test` (a NEW test may be given whole
# in a non-diff fence after a `File: \`<path>\`` line).
#
# It runs tasks/bash_patch/build_bash_input.sh UNCHANGED for the FIRST product and the FIRST RED test (test_file=), on a
# copy of the brief whose `## The exact change` keeps only the first product's file sections (that builder checks every
# fenced '-' line against ITS product's tip), then:
#   ticket.description   the WHOLE brief again (the copy is never the prompt)
#   defect_line          expected_plus = every product's '+' lines; must_remove = every product's '-' lines, each checked
#                        against THAT product's tip; the context-as-addition gate per hunk over every product;
#                        sites (`## Where`) stay the builder's = the FIRST product's line numbers
#   files[...]           every further product and every MODIFIED test, whole (refused past 160000 B)
#   task_type "bash_patch2", product_files, test_files [{path, status new|modified (measured at the tip), role}]
# REFUSES (rc 2): counts outside 1-3 / 1-4; no RED test; a NEW test that is not RED; a declared NEW test already at the
# tip / a MODIFIED one missing; tests not all in the ref's dir; a fence line under `## The exact change` / `## The test`
# not attributable to a file, or attributed to the wrong section's kind; a declared file the brief carries no lines for;
# a product '-' line absent from that product's tip; anything build_bash_input.sh refuses.
# rc 0 ok · 2 refused · 1 error. Writes only <out> and <out>.builder_brief.md. Read verbs only on the source checkout.
# bash 3.2; stderr never discarded.
set -uo pipefail
ID="${1:-}"; OUT="${2:-}"; BRIEF="${3:-}"; shift 3 2>/dev/null
[ -n "$ID" ] && [ -n "$OUT" ] && [ -f "$BRIEF" ] || { echo "usage: build_bash_input2.sh <KS-id> <out> <brief.md> ref=<path> [pin=value ...]" >&2; exit 1; }
HERE="$(cd "$(dirname "$0")" && pwd)"; LM="$(dirname "$(dirname "$HERE")")"
SRC="${NIGHT_SOURCE_CHECKOUT:-/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files}"
BB="$OUT.builder_brief.md"

# ---------------------------------------------------------------- 1. parse + validate the declared set, write the copy
DECL="$(python3 - "$BRIEF" "$BB" <<'PY'
import json, re, sys
brief, bb = sys.argv[1:3]
text = open(brief, encoding="utf-8").read()
def refuse(m): sys.stderr.write(f"build_bash_input2: REFUSED — {m}\n"); sys.exit(2)
header = re.split(r"(?m)^##\s", text, maxsplit=1)[0]
products = re.findall(r"(?m)^File:\s*`([^`]+)`", header)
tests = []
for m in re.finditer(r"(?m)^Test[^:\n`]*:\s*`([^`]+)`([^\n]*)", header):
    rest = m.group(2)
    red, sup = bool(re.search(r"\bRED\b", rest)), bool(re.search(r"\bSUPPORT\b", rest))
    if red == sup: refuse(f"header test line for {m.group(1)} must say exactly one of RED / SUPPORT (got: {rest.strip()[:80]!r})")
    new = bool(re.search(r"\bNEW\b", rest)); mod = bool(re.search(r"\b(MODIFIED|EXISTING)\b", rest))
    if new == mod: refuse(f"header test line for {m.group(1)} must say exactly one of NEW / MODIFIED")
    tests.append({"path": m.group(1), "role": "red" if red else "support", "declared": "new" if new else "modified"})
if not (1 <= len(products) <= 3): refuse(f"{len(products)} product file(s) declared (File: lines); bash_patch2 takes 1-3")
if not (1 <= len(tests) <= 4): refuse(f"{len(tests)} test file(s) declared (Test …: lines); bash_patch2 takes 1-4")
if not any(t["role"] == "red" for t in tests): refuse("no RED test declared — nothing would prove the defect")
for t in tests:
    if t["declared"] == "new" and t["role"] != "red": refuse(f"{t['path']} is NEW but SUPPORT — a new suite that is green before the fix proves nothing")
    if not t["path"].endswith(".test.sh"): refuse(f"{t['path']} is not a *.test.sh")
if len({p for p in products} | {t["path"] for t in tests}) != len(products) + len(tests): refuse("a path is declared twice")
dirs = {t["path"].rsplit("/", 1)[0] for t in tests}
if len(dirs) != 1: refuse(f"the declared tests are not in ONE directory: {sorted(dirs)}")

def region(name):
    m = re.search(r"(?m)^##+\s*" + name + r"\b[^\n]*\n", text)
    if not m: return None, None
    s = m.end(); n = re.search(r"(?m)^##\s", text[s:]); e = s + n.start() if n else len(text)
    return s, e
def norm(p): return p[2:] if p.startswith(("a/", "b/")) else p
have = {}
for name, allowed in (("The exact change", set(products)), ("The test", {t["path"] for t in tests})):
    s, e = region(name)
    if s is None: refuse(f"no `## {name}` section")
    body = text[s:e]; pos = 0; last = None
    for fm in re.finditer(r"(?ms)^```[^\n]*\n(.*?)^```[ \t]*$", body):
        for nm in re.finditer(r"(?m)^(?:Test )?[Ff]ile:\s*`([^`]+)`", body[pos:fm.start()]): last = nm.group(1)
        pos = fm.end(); lines = fm.group(1).split("\n")
        if not any(l.startswith("+++ ") for l in lines):
            if name == "The test" and last in {t["path"] for t in tests if t["declared"] == "new"}:
                have[last] = have.get(last, 0) + len([l for l in lines if l.strip()]); last = None; continue
            if any(l[:1] in "+-" and l[1:].strip() for l in lines):
                refuse(f"a fence under `## {name}` has +/- lines but no `+++ b/<path>` header — bash_patch2 attributes every line to a file")
            last = None; continue
        cur = None
        for l in lines:
            if l.startswith("+++ "):
                cur = norm(l[4:].strip())
                if cur not in allowed: refuse(f"`## {name}` carries a hunk for {cur}, which is not a declared {'product' if name == 'The exact change' else 'test'} (product hunks go under `## The exact change`, test hunks under `## The test`)")
                continue
            if l.startswith("--- "): continue
            if l[:1] in "+-" and cur is None: refuse(f"a +/- line under `## {name}` before any `+++` header")
            if l[:1] in "+-": have[cur] = have.get(cur, 0) + 1
        last = None
for p in products + [t["path"] for t in tests]:
    if not have.get(p): refuse(f"the brief carries no lines for the declared file {p} — every declared file's edit must be spelled out")

# the builder's copy: `## The exact change` keeps only the FIRST product's file sections
s, e = region("The exact change"); body = text[s:e]
def keep_first(m):
    L = m.group(1).split("\n"); out = []; keep = False
    for i, l in enumerate(L):
        # a file section starts at `--- ` immediately followed by `+++ `; it is kept iff its +++ path is product 1
        if l.startswith("--- ") and i + 1 < len(L) and L[i + 1].startswith("+++ "):
            keep = norm(L[i + 1][4:].strip()) == products[0]
        if keep: out.append(l)
    while out and out[-1] == "": out.pop()
    return "```diff\n" + "".join(x + "\n" for x in out) + "```"
body2 = re.sub(r"(?ms)^```[^\n]*\n(.*?)^```[ \t]*$", keep_first, body)
open(bb, "w", encoding="utf-8").write(text[:s] + body2 + text[e:])
red0 = next(t["path"] for t in tests if t["role"] == "red")
print(json.dumps({"products": products, "tests": tests, "first_red": red0}))
PY
)"; RC=$?
[ "$RC" -eq 0 ] || exit "$RC"
P1="$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["products"][0])' "$DECL")"
R1="$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["first_red"])' "$DECL")"

# ---------------------------------------------------------------- 2. the bash_patch builder, unchanged, on the copy
PINS=()
for a in "$@"; do case "$a" in product=*|test_file=*) echo "build_bash_input2: NOTE pin $a ignored — the header's declared set decides" >&2 ;; *) PINS+=("$a") ;; esac; done
NIGHT_SOURCE_CHECKOUT="$SRC" bash "$LM/tasks/bash_patch/build_bash_input.sh" "$ID" "$OUT" "$BB" "product=$P1" "test_file=$R1" ${PINS[@]+"${PINS[@]}"}; RC=$?
[ "$RC" -eq 0 ] || exit "$RC"

# ---------------------------------------------------------------- 3. widen the input to the declared set
python3 - "$OUT" "$BRIEF" "$DECL" <<'PY'
import json, re, subprocess, sys
out, brief, decl = sys.argv[1:4]
D = json.loads(decl); d = json.load(open(out, encoding="utf-8"))
text = open(brief, encoding="utf-8").read()
def refuse(m): sys.stderr.write(f"build_bash_input2: REFUSED — {m}\n"); sys.exit(2)
src = d["repo"]["source_checkout"]; tip = d.get("tip") or d["repo"]["tip"]
def at_tip(p): return subprocess.run(["git", "-C", src, "cat-file", "-e", f"{tip}:{p}"], capture_output=True).returncode == 0
def show(p):
    r = subprocess.run(["git", "-C", src, "show", f"{tip}:{p}"], capture_output=True, text=True)
    if r.returncode: refuse(f"{p} not readable at {tip[:12]}: {r.stderr.strip()[:120]}")
    return r.stdout
products = D["products"]; test_dir = d["test_dir"]
for p in products:
    if not at_tip(p): refuse(f"declared product {p} is not at the tip {tip[:12]}")
tlist = []
for t in D["tests"]:
    st = "modified" if at_tip(t["path"]) else "new"
    if st != t["declared"]: refuse(f"{t['path']} is declared {t['declared'].upper()} but is {'present' if st == 'modified' else 'absent'} at the tip {tip[:12]}")
    if t["path"].rsplit("/", 1)[0] != test_dir: refuse(f"{t['path']} is not in the reference's directory {test_dir}")
    tlist.append({"path": t["path"], "status": st, "role": t["role"]})
# every product's '+' / '-' lines from `## The exact change`, per file, per hunk
m = re.search(r"(?ms)^##+\s*The exact change\b[^\n]*\n(.*?)(?=^##\s|\Z)", text)
per = {}
for blk in re.findall(r"(?ms)^```[^\n]*\n(.*?)^```[ \t]*$", m.group(1)):
    cur = None
    for h in re.split(r"(?m)^(?=@@ |\+\+\+ )", blk):
        for l in h.split("\n"):
            if l.startswith("+++ "): cur = l[4:].strip(); cur = cur[2:] if cur.startswith("b/") else cur
        if cur is None: continue
        hl = [l for l in h.split("\n") if not l.startswith(("+++ ", "--- "))]
        per.setdefault(cur, []).append(([l[1:] for l in hl if l.startswith("+")], [l[1:] for l in hl if l.startswith("-")]))
expected_plus, must_remove, dup = [], [], []
for p in products:
    tipl = [l.rstrip() for l in show(p).split("\n")]
    for plus, minus in per.get(p, []):
        expected_plus += [l.strip() for l in plus if l.strip()]
        mr = [l.rstrip() for l in minus if l.strip()]
        miss = [x for x in mr if x not in tipl]
        if miss: refuse(f"{len(miss)} brief '-' line(s) for {p} do not exist at its tip: {miss[:2]}")
        must_remove += mr
        dup += [l.strip() for l in plus if l.strip() and l.strip() in {x.strip() for x in minus if x.strip()}]
if dup: refuse(f"{len(dup)} product '+' line(s) repeat a '-' line of the same hunk (context marked as addition): {dup[:3]}")
dl = d.setdefault("defect_line", {}); dl["expected_plus"] = expected_plus; dl["must_remove"] = must_remove
d["ticket"]["description"] = text            # the WHOLE brief is the prompt, never the builder's copy
files = d.setdefault("files", {})
for p in products[1:] + [t["path"] for t in tlist if t["status"] == "modified"]:
    if p in files: continue
    body = show(p)
    if len(body) > 160000: refuse(f"{p} is {len(body)} B (> 160000): bash_patch2 carries files whole")
    files[p] = body
d["task_type"] = "bash_patch2"; d["product_files"] = products; d["test_files"] = tlist
json.dump(d, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"  prompt source: WEDNESDAY BRIEF {brief} ({len(text)} chars) — the ticket description is NOT the prompt")
print(f"bash_patch2: product_files={[p.rsplit('/', 1)[-1] for p in products]} test_files={[(t['path'].rsplit('/', 1)[-1], t['status'], t['role']) for t in tlist]} expected '+' {len(expected_plus)} must_remove {len(must_remove)} -> {out}")
PY
