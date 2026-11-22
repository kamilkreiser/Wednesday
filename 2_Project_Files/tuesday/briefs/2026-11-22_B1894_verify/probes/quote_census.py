"""B1894: in a workflow, outside block scalars (check_spellings' walk), count lines holding a quote character and
lines where a quote appears that is NOT the first character of a value (after ': ' or '- ' or at the line's first
non-blank). Prints counts and line numbers only, never a line. usage: python3 -I quote_census.py <tree> [<file>]"""
import sys, re
sys.path.insert(0, sys.argv[1] + "/build")
import repo_rules as rr
path = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1] + "/.github/workflows/ci.yml"
lines = open(path, "rb").read().decode("latin-1").splitlines()
VALUE_START = re.compile(r"""^\s*(?:-\s+)*(?:[^'"\s:#][^:#]*?:\s+)?(['"])""")
bk = bi = None; outside = with_q = other = 0; nums = []
for n, line in enumerate(lines, 1):
    if bk is not None:
        if not line.strip(" "): continue
        if bi is None and rr.indent_of(line) > bk: bi = rr.indent_of(line)
        if bi is not None and rr.indent_of(line) >= bi: continue
        bk = bi = None
    outside += 1
    s = rr.yaml_structure(rr.R6_EXPRESSION.sub("", line))
    if "'" in line or '"' in line:
        with_q += 1
        m = VALUE_START.match(line)
        first = min(i for i, c in enumerate(line) if c in "'\"")
        if not m or m.start(1) != first:
            other += 1; nums.append(n)
    if rr.R6_BLOCK_START.search(s): bk = len(line) - len(line.lstrip(" -"))
print("lines outside a block", outside, "| holding a quote", with_q, "| first quote not at a value start", other, nums)
