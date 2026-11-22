import sys
sys.path.insert(0, sys.argv[1] + "/build")
import repo_rules as rr
base = open(sys.argv[1] + "/.github/workflows/ci.yml", encoding="utf-8").read()
body = '      "runs-on": ubuntu-latest\n      env: {A: b}\n      steps:\n        - "uses": actions/checkout@main\n        - run: echo "\\x41"\n'
cases = {
 "full-line-comment": base + "  extra:\n    # note: |\n" + body,
 "trailing-comment":  base + "  extra: # note: |\n" + body,
 "control-no-comment": base + "  extra:\n" + body,
}
for label, text in cases.items():
    p = "/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/724d1912-1eaf-4390-bead-8e0f615c00cd/scratchpad/b1891/r6/%s.yml" % label
    open(p, "w", encoding="utf-8").write(text)
    lines = text.splitlines()
    print("%-20s R6 %s" % (label, rr.check_spellings(lines)))
