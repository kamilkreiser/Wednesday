"""B1891 round 2: Q14 as built (a comment line ends a block only by its indentation; a comment never opens one).
usage: python3 -I q14_probe.py <head clone> <out folder>; prints R6 findings; the .yml files are for Psych."""
import sys, os
sys.path.insert(0, sys.argv[1] + "/build")
import repo_rules as rr
base = open(sys.argv[1] + "/.github/workflows/ci.yml", encoding="utf-8").read()
out = sys.argv[2]; os.makedirs(out, exist_ok=True)
cases = {
 "deeper-comment-line-inside-block": base + '  extra:\n    runs-on: ubuntu-latest\n    steps:\n      - run: |\n          echo a\n          # x: |\n          echo "{b}"\n',
 "less-indented-comment-then-deeper": base + '  extra:\n    runs-on: ubuntu-latest\n    steps:\n      - run: |\n          echo a\n        # c\n          echo b\n',
 "less-indented-comment-then-keys": base + '  extra:\n    runs-on: ubuntu-latest\n    steps:\n      - run: |\n          echo a\n        # c\n        "shell": bash\n',
 "comment-at-block-column-zero": base + '  extra:\n    runs-on: ubuntu-latest\n    steps:\n      - run: |\n          echo a\n# c\n    "env": {A: b}\n',
}
for label, text in cases.items():
    open(os.path.join(out, label + ".yml"), "w", encoding="utf-8").write(text)
    print("%-36s R6 %s" % (label, rr.check_spellings(text.encode().decode("latin-1").splitlines())))
