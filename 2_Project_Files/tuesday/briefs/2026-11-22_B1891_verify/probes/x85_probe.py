"""B1891 round 2: a UTF-8 character whose last byte is 0x85 (U+00C5, bytes C3 85) inside a comment. repo_rules.py reads
a workflow as data.decode("latin-1").splitlines(), and str.splitlines() breaks at U+0085, so the reader sees a new line
where YAML (UTF-8: an ordinary letter) sees none.
usage: python3 -I x85_probe.py <head clone> <out folder>. Writes one .yml per shape; prints R6 findings as judge() reads it."""
import sys, os
sys.path.insert(0, sys.argv[1] + "/build")
import repo_rules as rr
base = open(sys.argv[1] + "/.github/workflows/ci.yml", encoding="utf-8").read()
out = sys.argv[2]; os.makedirs(out, exist_ok=True)
hidden = '      "runs-on": ubuntu-latest\n      "permissions": write-all\n      env: {A: b}\n      steps:\n        - "uses": actions/checkout@main\n        - run: echo "\\x41"\n'
cases = {
 "a-ring-in-trailing-comment": base + "  extra: # \u00c5b: |\n" + hidden,
 "a-ogonek-in-full-line-comment": base + "  extra:\n    # \u0105b: |\n" + hidden,
 "control-plain-a-in-comment": base + "  extra: # Ab: |\n" + hidden,
}
for label, text in cases.items():
    open(os.path.join(out, label + ".yml"), "w", encoding="utf-8").write(text)
    lines = text.encode("utf-8").decode("latin-1").splitlines()
    print("%-32s lines %d (LF %d) R6 %s" % (label, len(lines), text.count("\n"), rr.check_spellings(lines)))
