"""B1891 round 2: a multi-line quoted scalar whose continuation line ends `: |` (less indented than the mapping).
usage: python3 -I ml_probe.py <head clone> <out folder>. Writes one .yml per shape into <out>; prints R6 findings."""
import sys, os
sys.path.insert(0, sys.argv[1] + "/build")
import repo_rules as rr
base = open(sys.argv[1] + "/.github/workflows/ci.yml", encoding="utf-8").read()
out = sys.argv[2]; os.makedirs(out, exist_ok=True)
hidden = '    "runs-on": ubuntu-latest\n    env: {A: b}\n    steps:\n      - "uses": actions/checkout@main\n      - run: echo "\\x41"\n'
cases = {
 "dq-continuation-less-indented": base + '  extra:\n    name: "a\n  b: |\n    "\n' + hidden,
 "sq-continuation-less-indented": base + "  extra:\n    name: 'a\n  b: |\n    '\n" + hidden,
 "dq-continuation-col0": base + '  extra:\n    name: "a\nb: |\n    "\n' + hidden,
 "control-closed-on-one-line": base + '  extra:\n    name: "a b: |"\n' + hidden,
}
for label, text in cases.items():
    open(os.path.join(out, label + ".yml"), "w", encoding="utf-8").write(text)
    print("%-32s R6 %s" % (label, rr.check_spellings(text.splitlines())))
