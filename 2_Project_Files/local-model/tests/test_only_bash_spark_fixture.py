#!/usr/bin/env python3
"""test_only_bash_spark_fixture.py <fixture-root> — builds the tiny fixture repo, every brief dir and every crafted model output
for test_only_bash_spark_arms.sh (2026-11-09). <fixture-root> must NOT exist (asserted); it is created. No Secuura clone is
touched, no model is called. Python stdlib + git + bash only.

Layout under <root>: secuura/ (fixture "Secuura checkout"), wt/ (scratch worktree to produce diffs), briefs/<name>/, outs/<name>.md,
deps/ (the node_modules + LOCK_KEY stand-in round.sh requires), tip.txt.
"""
import os
import re
import subprocess
import sys

root = sys.argv[1]
assert not os.path.exists(root), f"{root} exists — the fixture root must be a fresh path"
os.makedirs(root)
SEC, WT = os.path.join(root, "secuura"), os.path.join(root, "wt")
SUB = "Blockchain/Dev"
PF = f"{SUB}/scripts/preflight/pf.sh"            # the read-only product
T1 = f"{SUB}/scripts/__tests__/pf_header.test.sh"   # suite 1 (plant shape)
T2 = f"{SUB}/scripts/__tests__/cens_link.test.sh"   # suite 2 (expect shape)
SIB = f"{SUB}/scripts/__tests__/pf_sibling.test.sh"  # a sibling that names pf.sh (A6)
OTHER = f"{SUB}/scripts/__tests__/unrelated.test.sh"
README = "README.md"


def git(d, *a, check=True):
    r = subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit(f"git {a} failed in {d}: {r.stderr}")
    return r.stdout


def write(base, rel, text):
    p = os.path.join(base, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(text)


HELPER = '''
check() {
    local desc="$1" want="$2" got="$3"
    if [[ "$got" == "$want" ]]; then PASS=$((PASS+1)); printf 'ok   %s\\n' "$desc"
    else FAIL=$((FAIL+1)); printf 'FAIL %s\\n       want "%s", got "%s"\\n' "$desc" "$want" "$got"; fi
}
'''
FOOT = '''
echo ""
echo "$(basename "${BASH_SOURCE[0]}"): ${PASS} passed, ${FAIL} failed"
(( FAIL == 0 ))
'''
PF_BODY = '''#!/usr/bin/env bash
# pf.sh - fixture preflight (product, read-only)
case "${1:-}" in
  --help)
    echo "Refused: a closing parenthesis glued to the digits."
    echo "Digits after a separator are not checked."
    ;;
  *) echo "run" ;;
esac
'''
T1_BODY = '''#!/usr/bin/env bash
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PF="$HERE/../preflight/pf.sh"
PASS=0; FAIL=0
''' + HELPER + '''
help_text="$(bash "$PF" --help)"
check "help names a closing parenthesis" "yes" "$(grep -qF 'a closing parenthesis' <<<"$help_text" && echo yes || echo no)"
check "help names Digits after a separator" "yes" "$(grep -qF 'Digits after a separator' <<<"$help_text" && echo yes || echo no)"
check "a plain run says run" "run" "$(bash "$PF")"
''' + FOOT
T2_BODY = '''#!/usr/bin/env bash
set -uo pipefail
PASS=0; FAIL=0
''' + HELPER + '''
links_jq() { grep -qE '^[[:space:]]*ln[[:space:]]+-[A-Za-z]*s[A-Za-z]*[[:space:]].*bin/jq["'"'"']?[[:space:]]*($|[;&|#])' "$1"; }
verdict() { if links_jq "$1"; then echo yes; else echo no; fi; }
FX="$(mktemp -d "${TMPDIR:-/tmp}/cens-fx.XXXXXX")"; trap 'rm -rf "$FX"' EXIT
printf '%s\\n' 'ln -sf "$JQ_BIN" "$root/bin/jq"' > "$FX/real.sh"
check "CONTROL the real link statement is recognised" "yes" "$(verdict "$FX/real.sh")"
printf '%s\\n' 'echo "bin/jq is here"' > "$FX/words.sh"
check "the words alone are not a link" "no" "$(verdict "$FX/words.sh")"
''' + FOOT
SIB_BODY = '''#!/usr/bin/env bash
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PASS=0; FAIL=0
''' + HELPER + '''
# drives pf.sh (the name makes this a sibling of the pf_header suite)
check "sibling: pf.sh runs" "run" "$(bash "$HERE/../preflight/pf.sh")"
''' + FOOT
OTHER_BODY = '''#!/usr/bin/env bash
PASS=0; FAIL=0
''' + HELPER + '''
check "unrelated" "2" "$((1+1))"
''' + FOOT

FILES = {f"{SUB}/package.json": '{"name":"fixture"}\n', f"{SUB}/.gitignore": "node_modules\n", PF: PF_BODY,
         T1: T1_BODY, T2: T2_BODY, SIB: SIB_BODY, OTHER: OTHER_BODY, README: "# fixture\n"}

os.makedirs(SEC)
git(SEC, "init", "-q")
git(SEC, "config", "user.email", "arms@example.invalid")
git(SEC, "config", "user.name", "arms")
for rel, txt in FILES.items():
    write(SEC, rel, txt)
git(SEC, "add", "-A")
git(SEC, "commit", "-q", "-m", "fixture")
git(SEC, "remote", "add", "origin", "https://example.invalid/fixture.git")
TIP = git(SEC, "rev-parse", "HEAD").strip()
open(os.path.join(root, "tip.txt"), "w").write(TIP + "\n")
# the deps stand-in round.sh requires (node_modules dir + a LOCK_KEY equal to the tip's)
write(root, f"deps/{SUB}/node_modules/placeholder/index.js", "// placeholder\n")
write(SEC, f"{SUB}/node_modules/placeholder/index.js", "// placeholder\n")
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
key = subprocess.run(["bash", os.path.join(here, "spark", "lock_key.sh"), SEC, TIP], capture_output=True, text=True).stdout.strip()
open(os.path.join(root, "deps", "LOCK_KEY"), "w").write(key + " " + TIP + "\n")
subprocess.run(["git", "clone", "-q", SEC, WT], check=True)
git(WT, "config", "user.email", "arms@example.invalid")


def diff_of(edits):
    for rel, txt in edits.items():
        write(WT, rel, txt)
    out = git(WT, "diff", "--no-color")
    git(WT, "checkout", "--", ".")
    keep = [l for l in out.split("\n") if not re.match(r"^(diff --git |index |new file mode|deleted file mode)", l)]
    return "\n".join(keep)


def cur(rel):
    return FILES[rel]


def ins_before_foot(body, new):
    i = body.index('\necho ""\necho "$(basename')
    return body[:i] + new + body[i:]


# --- plant shape (suite 1) ---
SENT_CELL = '''check "the unchecked sentence is pinned whole" "Digits after a separator are not checked." "$(printf '%s\\n' "$help_text" | sed -n '2p')"
'''
T1_GOOD = ins_before_foot(T1_BODY, SENT_CELL)
T1_NEVERRED = ins_before_foot(T1_BODY, '''check "the unchecked sentence is pinned whole" "run" "$(bash "$PF")"
''')      # asserts something the plant cannot change
T1_CRASH = ins_before_foot(T1_BODY, '''check "the unchecked sentence is pinned whole" "x" "$(pinned_sentence_helper "$help_text")"
''')      # calls a function that does not exist: bash prints command not found
T1_LOST = T1_GOOD.replace('check "a plain run says run"', 'check "a plain run says RUN"')
T1_NOGATE = T1_GOOD.replace("(( FAIL == 0 ))", "true")   # prints FAIL under the plant but exits 0
GOOD_PLANT = diff_of({T1: T1_GOOD})
OUT_NEVERRED = diff_of({T1: T1_NEVERRED})
OUT_CRASH = diff_of({T1: T1_CRASH})
OUT_LOST = diff_of({T1: T1_LOST})
OUT_NOGATE = diff_of({T1: T1_NOGATE})
OUT_PRODUCT = diff_of({T1: T1_GOOD, PF: PF_BODY.replace("are not checked.", "are not checked at all.")})
OUT_EXTRA_SUITE = diff_of({T1: T1_GOOD, OTHER: cur(OTHER).replace('check "unrelated"', 'check "unrelated 2"')})
OUT_MISSING_CELL = diff_of({T1: ins_before_foot(T1_BODY, SENT_CELL.replace("pinned whole", "pinned entirely"))})
# a wrong expected line: the context the diff claims at the tip is not the tip's
OUT_WRONGCTX = GOOD_PLANT.replace('check "a plain run says run"', 'check "a plain run says nothing"', 1)
assert OUT_WRONGCTX != GOOD_PLANT
m = re.search(r"@@ -(\d+),(\d+) \+(\d+),(\d+) @@", GOOD_PLANT)
OUT_ANCHOR = GOOD_PLANT[:m.start()] + f"@@ -{int(m.group(1)) + 6},{m.group(2)} +{int(m.group(1)) + 6},{m.group(4)} @@" + GOOD_PLANT[m.end():]
PF_LINES = PF_BODY.split("\n")
PLANT_LINE = 1 + next(i for i, l in enumerate(PF_LINES) if "Digits after a separator are not checked." in l)
PLANT_FROM = PF_LINES[PLANT_LINE - 1]
PLANT_TO = PLANT_FROM.replace("are not checked.", "are checked.")

# --- expect shape (suite 2): widen the regex to take a trailing redirection, add the fixture cells ---
OLD_RX = r"""links_jq() { grep -qE '^[[:space:]]*ln[[:space:]]+-[A-Za-z]*s[A-Za-z]*[[:space:]].*bin/jq["'"'"']?[[:space:]]*($|[;&|#])' "$1"; }"""
NEW_RX = r"""links_jq() { grep -qE '^[[:space:]]*ln[[:space:]]+-[A-Za-z]*s[A-Za-z]*[[:space:]].*bin/jq["'"'"']?([[:space:]]+[0-9]*>[^;&|#]*)?[[:space:]]*($|[;&|#])' "$1"; }"""
assert OLD_RX in T2_BODY
NEWCELL = '''printf '%s\\n' 'ln -sf "$JQ_BIN" "$root/bin/jq" 2>/dev/null' > "$FX/redir.sh"
check "a stderr-redirected ln -sf is judged a link" "yes" "$(verdict "$FX/redir.sh")"
'''
T2_GOOD = ins_before_foot(T2_BODY.replace(OLD_RX, NEW_RX), NEWCELL)
T2_CELL_ONLY = ins_before_foot(T2_BODY, NEWCELL)          # the cell without the regex fix: it prints FAIL
GOOD_EXPECT = diff_of({T2: T2_GOOD})
OUT_CELL_ONLY = diff_of({T2: T2_CELL_ONLY})
GOOD_EXPECT_CELLONLY_PASSING = diff_of({T2: ins_before_foot(T2_BODY, NEWCELL.replace('"yes" "$(verdict "$FX/redir.sh")"', '"yes" "yes"'))})  # a cell that asserts nothing


# --- briefs ---
def brief(ticket, files, tests, body, tip=TIP, runner="bash", tier="test_only_bash"):
    h = [f"# {ticket} fixture brief for the {tier} arms", "", f"Tier: `{tier}`", f"Runner: {runner}", f"Tip: `{tip}`"]
    h += [f"File: `{f}`" for f in files] + [f"Test file: `{t}`" for t in tests]
    return "\n".join(h) + "\n\n" + body


def std(extra):
    return ("## The mode\ntest_only_bash arms.\n\n## What is wrong\nwhatever the arm defines.\n\n## The exact change\nsee golden.diff.\n\n"
            + extra + "\n## UNMEASURED\nnothing.\n\n## Scope\nfixture.\n\n## Output\none diff.\n")


def mk(name, ticket, text, golden=None, red=None, pins=""):
    d = os.path.join(root, "briefs", name)
    os.makedirs(d)
    write(d, f"KS-{ticket}.md", text)
    if golden is not None:
        write(d, "golden.diff", golden)
    if red is not None:
        write(d, "golden_red.diff", red)
    if pins is not None:
        write(d, "spark.pins", pins)
    return d


PLANT = f"## Plant\nfile: `{PF}`\nline: {PLANT_LINE}\nfrom: `{PLANT_FROM}`\nto: `{PLANT_TO}`\n"
CELLS = "## Red cells\n- `the unchecked sentence is pinned whole`\n"
TESTSEC = "## The test\nCell bodies are in golden.diff; copy them verbatim.\n\n"
EXPECT = "## Expect\nexpect_present: `ok   a stderr-redirected ln -sf is judged a link`\n"


def tp(name, ticket, plant=PLANT, cells=CELLS, golden=GOOD_PLANT, red=None, tests=(T1,), files=(PF,), runner="bash", tier="test_only_bash", extra=""):
    body = std(TESTSEC + (plant or "") + "\n" + (cells or "") + "\n" + extra)
    return mk(name, ticket, brief(f"KS-{ticket}", list(files), list(tests), body, runner=runner, tier=tier), golden, red)


def te(name, ticket, expect=EXPECT, golden=GOOD_EXPECT, tests=(T2,), files=(PF,), cells="", extra=""):
    body = std(TESTSEC + expect + "\n" + cells + "\n" + extra)
    return mk(name, ticket, brief(f"KS-{ticket}", list(files), list(tests), body), golden)


# control-round briefs
tp("bx_pass_plant", 9201)
te("bx_pass_expect", 9202)
tp("bx_neverred", 9203, golden=OUT_NEVERRED)
tp("bx_crash", 9204, golden=OUT_CRASH)
tp("bx_plant_not_applicable", 9205, plant=PLANT.replace(PLANT_FROM, PLANT_FROM + " extra"))
tp("bx_redcell_missing", 9206, golden=OUT_MISSING_CELL)
tp("bx_nogate", 9207, golden=OUT_NOGATE)
te("bx_cell_only", 9208, golden=OUT_CELL_ONLY)
te("bx_expect_holds_at_tip", 9209, expect="## Expect\nexpect_present: `ok   CONTROL the real link statement is recognised`\n")
# lint refusals
tp("l_both_proofs", 9211, extra=EXPECT)
tp("l_no_proof", 9212, plant="", cells="")
tp("l_no_redcells", 9213, cells="")
tp("l_not_bash_suite", 9214, tests=(f"{SUB}/scripts/helper.sh",), golden=None)
tp("l_file_is_test", 9215, files=(T1,))
tp("l_runner_vitest", 9216, runner="vitest")
tp("l_golden_names_product", 9217, golden=OUT_PRODUCT)
tp("l_plant_in_suite", 9218, plant=PLANT.replace(PF, T1))
tp("l_four_tests", 9219, tests=(T1, T2, SIB, OTHER))
te("l_expect_empty", 9220, expect="## Expect\n")
te("l_expect_in_undeclared", 9221, expect=EXPECT + f"expect_absent: `x` in `{OTHER}`\n")

# --- crafted model outputs (direct tier_checker.py runs on the clone a control PASS left behind) ---
def fence(d):
    return "```diff\n" + d + ("" if d.endswith("\n") else "\n") + "```\n"


outs = {
    "touches_product": fence(OUT_PRODUCT), "extra_suite": fence(OUT_EXTRA_SUITE), "lost_cell": fence(OUT_LOST),
    "wrong_context": fence(OUT_WRONGCTX), "bad_anchor": fence(OUT_ANCHOR), "prose_only": "I would pin the whole sentence.\n",
    "prose_and_diff": "Here is the change:\n" + fence(GOOD_PLANT), "good_plant": fence(GOOD_PLANT), "good_expect": fence(GOOD_EXPECT),
    "cell_asserts_nothing_expect": fence(GOOD_EXPECT_CELLONLY_PASSING),
}
os.makedirs(os.path.join(root, "outs"))
for k, v in outs.items():
    write(os.path.join(root, "outs"), k + ".md", v)
print(f"fixture built at {root} tip {TIP[:12]} (plant line {PLANT_LINE})")
