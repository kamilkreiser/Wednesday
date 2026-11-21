import sys
sys.path.insert(0, sys.argv[1] + "/build")
import repo_rules as rr
base = open(sys.argv[1] + "/.github/workflows/ci.yml", encoding="utf-8").read()
x = base.replace("\nenv:\n", "\nenv:\n  BASH_FUNC_test%%: |\n    () { return 0; }\n", 1)
print("exported-function-in-block R6", rr.check_spellings(x.splitlines()))
