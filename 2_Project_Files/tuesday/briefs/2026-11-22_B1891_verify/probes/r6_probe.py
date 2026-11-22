import sys, json, os, subprocess
sys.path.insert(0, sys.argv[1] + "/build")
import repo_rules as rr
base = open(sys.argv[1] + "/.github/workflows/ci.yml", encoding="utf-8").read()
cases = {}
# 1 a comment line ending ': |' opens a phantom block; deeper YAML after it is not judged
cases["comment-opens-block"] = base.replace("  rules:\n    name: rules\n", "  rules:\n    # note: |\n      \"name\": rules\n      env: {X: y}\n      if: \"a\\x62\"\n", 1).replace("\n    runs-on: ubuntu-latest\n    defaults:\n      run:\n        shell: bash\n    steps:\n      - name: checkout\n        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1\n        with:\n          persist-credentials: false\n      - name: planted controls", "\n      runs-on: ubuntu-latest\n      defaults:\n        run:\n          shell: bash\n      steps:\n        - name: checkout\n          uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1\n          with:\n            persist-credentials: false\n        - name: planted controls")
# 2 a flow sequence holding a single-pair mapping with a quoted key
cases["flow-seq-quoted-key"] = base + "  extra:\n    runs-on: ubuntu-latest\n    steps: [ \"uses\": \"actions/checkout@main\" ]\n"
# 3 the same, unquoted (R4 should catch)
cases["flow-seq-bare-key"] = base + "  extra:\n    runs-on: ubuntu-latest\n    steps: [ uses: actions/checkout@main ]\n"
# 4 single-quoted key with a doubled quote
cases["sq-key-doubled-quote"] = base.replace("\nenv:\n", "\nenv:\n  'X''Y': one\n", 1)
# 5 BASH_ENV built in shell inside a run block
cases["bash-env-split-in-shell"] = base.replace("          FLOOR=108\n", "          FLOOR=108\n          echo \"BASH\"\"_ENV=/tmp/x\" >> \"$GITHUB_ENV\"\n", 1)
# 6 a NEL (U+0085) in a comment followed by a block key
cases["nel-in-comment"] = base.replace("\nenv:\n", "\nenv: # c\u0085x: |\n  \"Q\": one\n", 1)
# 7 trailing comment that ends ': >'
cases["trailing-comment-block"] = base.replace("    name: rules\n", "    name: rules # see: >\n", 1)
for label, text in cases.items():
    lines = text.encode("utf-8").decode("latin-1").splitlines()
    f = rr.check_spellings(lines)
    open("/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/724d1912-1eaf-4390-bead-8e0f615c00cd/scratchpad/b1891/r6/%s.yml" % label, "w", encoding="utf-8").write(text)
    print("%-26s R6 findings %s" % (label, f))
