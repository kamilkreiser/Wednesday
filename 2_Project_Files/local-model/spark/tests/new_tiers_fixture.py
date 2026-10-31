#!/usr/bin/env python3
"""new_tiers_fixture.py <fixture-root> — builds the tiny fixture repo + every brief dir + every crafted model output the
new_tiers_arms.sh arms use (2026-10-31). <fixture-root> must NOT exist (asserted); it is created. Nothing here touches a
Secuura clone. Python stdlib + git only.

Layout under <root>:
  secuura/                 the fixture "Secuura checkout" (git repo, origin = https://example.invalid/fixture.git)
  wt/                      scratch worktree used to produce the diffs
  briefs/<name>/           brief dirs (KS-<n>.md [+ golden.diff, golden_red.diff, spark.pins])
  outs/<name>.md           crafted model outputs for direct tier_checker.py runs
  tip.txt                  the fixture's commit sha
"""
import os
import re
import subprocess
import sys

root = sys.argv[1]
assert not os.path.exists(root), f"{root} exists — the fixture root must be a fresh path"
os.makedirs(root)
SEC = os.path.join(root, "secuura")
WT = os.path.join(root, "wt")
SUB = "Blockchain/Dev"
SVC = f"{SUB}/services/svc"
VERIFY = f"{SVC}/src/verify.js"
TA, TB, TO = f"{SVC}/tests/verify.test.js", f"{SVC}/tests/verify_b.test.js", f"{SVC}/tests/other.test.js"
FIX = f"{SVC}/fixtures/tx.json"
GUIDE = f"{SUB}/docs/guide.md"
FRAG = "Blockchain/Projects Documents/fragments/api.md"
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


FILES = {
    f"{SUB}/.gitignore": "node_modules\n",
    VERIFY: """'use strict';
/**
 * Verify a transaction signature.
 * Returns the old-name shape.
 */
function verifyTx(tx) {
  // reject anything that is not an object
  if (!tx || typeof tx !== 'object') throw new Error('bad tx');
  if (typeof tx.from !== 'string') throw new Error('bad from');
  return { ok: tx.sig === 'sig-' + tx.from, from: tx.from };
}

module.exports = { verifyTx };
""",
    FIX: '{"from":"a","sig":"sig-a"}\n',
    TA: """'use strict';
const test = require('node:test');
const assert = require('node:assert');
const { verifyTx } = require('../src/verify');

test('accepts a good signature', () => {
  assert.strictEqual(verifyTx({ from: 'a', sig: 'sig-a' }).ok, true);
});
""",
    TB: """'use strict';
const test = require('node:test');
const assert = require('node:assert');
const { verifyTx } = require('../src/verify');
const tx = require('../fixtures/tx.json');

test('accepts the fixture tx', () => {
  assert.strictEqual(verifyTx(tx).ok, true);
});
""",
    TO: """'use strict';
const test = require('node:test');
const assert = require('node:assert');

test('unrelated', () => {
  assert.strictEqual(1 + 1, 2);
});
""",
    GUIDE: "# Guide\n\nRun the tool with the old-name flag.\nThen check the output.\n",
    FRAG: "<!-- fragment: api -->\nThe old-name endpoint returns JSON.\n",
    f"{SUB}/scripts/docs-fragments.mjs": """import fs from 'node:fs';
import path from 'node:path';
if (process.argv[2] !== 'check') { console.error('usage: check'); process.exit(2); }
const dir = path.join(process.cwd(), 'Blockchain', 'Projects Documents', 'fragments');
let bad = 0;
for (const f of fs.readdirSync(dir)) {
  if (fs.readFileSync(path.join(dir, f), 'utf8').includes('BROKEN-FRAGMENT')) { console.log('broken: ' + f); bad++; }
}
process.exit(bad ? 1 : 0);
""",
    README: "# fixture\n",
}

os.makedirs(SEC)
git(SEC, "init", "-q")
git(SEC, "config", "user.email", "arms@example.invalid")
git(SEC, "config", "user.name", "arms")
for rel, txt in FILES.items():
    write(SEC, rel, txt)
git(SEC, "add", "-A")
git(SEC, "commit", "-q", "-m", "fixture")
os.makedirs(os.path.join(SEC, SUB, "node_modules", "placeholder"))
write(SEC, f"{SUB}/node_modules/placeholder/index.js", "// placeholder\n")
git(SEC, "remote", "add", "origin", "https://example.invalid/fixture.git")
TIP = git(SEC, "rev-parse", "HEAD").strip()
open(os.path.join(root, "tip.txt"), "w").write(TIP + "\n")
subprocess.run(["git", "clone", "-q", SEC, WT], check=True)
git(WT, "config", "user.email", "arms@example.invalid")

# ------------------------------------------------------------------ diffs
def diff_of(edits):
    """edits: {rel: new text}. -> model-style diff (no diff --git / index lines), worktree restored."""
    for rel, txt in edits.items():
        write(WT, rel, txt)
    out = git(WT, "diff", "--no-color")
    git(WT, "checkout", "--", ".")
    keep = [l for l in out.split("\n") if not re.match(r"^(diff --git |index |new file mode|deleted file mode)", l)]
    return "\n".join(keep)


def cur(rel):
    return FILES[rel]


CELL_A = """
test('rejects a forged signature', () => {
  assert.strictEqual(verifyTx({ from: 'a', sig: 'forged' }).ok, false);
});
"""
CELL_B = """
test('rejects a tampered fixture sig', () => {
  assert.strictEqual(verifyTx({ from: tx.from, sig: 'x' + tx.sig }).ok, false);
});
"""
CELL_GREEN = """
test('rejects a forged signature', () => {
  assert.strictEqual(verifyTx({ from: 'a', sig: 'sig-a' }).ok, true);
});
"""
CELL_CRASH = """
test('rejects a forged signature', () => {
  const r = verifyTx({ from: 'a', sig: 'forged' });
  if (r.ok) { null.boom; }
  assert.ok(true);
});
"""
GOOD = diff_of({TA: cur(TA) + CELL_A, TB: cur(TB) + CELL_B})
GOLD_GREEN = diff_of({TA: cur(TA) + CELL_GREEN, TB: cur(TB) + CELL_B})
GOLD_CRASH = diff_of({TA: cur(TA) + CELL_CRASH, TB: cur(TB) + CELL_B})
OUT_EXTRA_TEST = diff_of({TA: cur(TA) + CELL_A, TB: cur(TB) + CELL_B, TO: cur(TO) + CELL_A.replace("forged signature", "extra")})
OUT_PRODUCT = diff_of({TA: cur(TA) + CELL_A, TB: cur(TB) + CELL_B, VERIFY: cur(VERIFY).replace("ok: tx.sig ===", "ok: !!tx.sig && tx.sig ===")})
OUT_MISSING = diff_of({TA: cur(TA) + CELL_A})
OUT_LOST = diff_of({TA: cur(TA).replace("test('accepts a good signature'", "test('RENAMED good'") + CELL_A, TB: cur(TB) + CELL_B})
OUT_LOST_CELL = diff_of({TA: cur(TA).split("test('accepts")[0] + CELL_A.lstrip("\n"), TB: cur(TB) + CELL_B})
# wrong anchor: the hunk header names a start line the old side does not sit at
m = re.search(r"@@ -(\d+),(\d+) \+(\d+),(\d+) @@", GOOD)
OUT_ANCHOR = GOOD[:m.start()] + f"@@ -{int(m.group(1)) + 20},{m.group(2)} +{int(m.group(1)) + 20},{m.group(4)} @@" + GOOD[m.end():]
# a cell that does not exist under the declared red-cell name is the brief's `## Red cells` pointing nowhere
GOLD_TEST_ONLY_FIX = diff_of({TA: cur(TA) + CELL_A, TB: cur(TB) + CELL_B.replace("tampered fixture sig", "other name")})

FIXTURE_PLANT = diff_of({FIX: '{"from":"a","sig":"forged"}\n'})
CELL_FIX = """
test('fixture tx keeps a valid signature', () => {
  assert.strictEqual(verifyTx(tx).ok, true);
});
"""
GOLD_FIXPLANT = diff_of({TB: cur(TB) + CELL_FIX})

# doc_only diffs
G_NEW = cur(GUIDE).replace("old-name", "new-name")
F_NEW = cur(FRAG).replace("old-name", "new-name")
V_COMMENT = cur(VERIFY).replace("Returns the old-name shape.", "Returns the new-name shape.").replace("// reject anything that is not an object", "// reject anything that is not a plain object")
D_GOOD = diff_of({GUIDE: G_NEW, FRAG: F_NEW, VERIFY: V_COMMENT})
D_CODE = diff_of({GUIDE: G_NEW, FRAG: F_NEW, VERIFY: V_COMMENT.replace("throw new Error('bad tx')", "throw new Error('bad transaction')")})
D_BLANK = diff_of({GUIDE: G_NEW, FRAG: F_NEW, VERIFY: V_COMMENT.replace("function verifyTx(tx) {\n", "\nfunction verifyTx(tx) {\n")})
D_TRAIL = diff_of({GUIDE: G_NEW, FRAG: F_NEW, VERIFY: V_COMMENT.replace("throw new Error('bad from');", "throw new Error('bad from'); // reworded")})
D_EXTRA = diff_of({GUIDE: G_NEW, FRAG: F_NEW, VERIFY: V_COMMENT, README: cur(README) + "more\n"})
D_PARTIAL = diff_of({GUIDE: cur(GUIDE).replace("Run the tool with the old-name flag.", "Run the tool with the old-name flag (new-name preferred)."), FRAG: F_NEW, VERIFY: V_COMMENT})
D_BROKEN = diff_of({GUIDE: G_NEW, FRAG: F_NEW + "BROKEN-FRAGMENT\n", VERIFY: V_COMMENT})
D_MISSING = diff_of({GUIDE: G_NEW, FRAG: F_NEW})

# ------------------------------------------------------------------ briefs
def brief(ticket, tier, files, tests, body, tip=TIP, runner="node-tap", extra_header=""):
    h = [f"# {ticket} fixture brief for the {tier} arms", "", f"Tier: `{tier}`", f"Runner: {runner}", f"Tip: `{tip}`"]
    h += [f"File: `{f}`" for f in files] + [f"Test file: `{t}`" for t in tests]
    if extra_header:
        h.append(extra_header)
    return "\n".join(h) + "\n\n" + body


def std_sections(extra_test_or_expect):
    return ("## The mode\nfixture arms.\n\n## What is wrong\nsomething the arms define.\n\n## The exact change\nsee golden.diff.\n\n"
            + extra_test_or_expect + "\n## UNMEASURED\nnothing.\n\n## Scope\nfixture.\n\n## Output\none diff.\n")


PLANT_PIN = ("## Plant\nfile: `" + VERIFY + "`\nline: 10\nfrom: `  return { ok: tx.sig === 'sig-' + tx.from, from: tx.from };`\n"
             "to: `  return { ok: true, from: tx.from };`\n")
CELLS_AB = "## Red cells\n- `rejects a forged signature`\n- `rejects a tampered fixture sig`\n"
TEST_SEC = "## The test\nCells are in golden.diff.\n\n"


def mk(name, ticket, text, golden=None, red=None, pins="shared_pkg_dir=none\n"):
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


def ti(name, ticket, plant=PLANT_PIN, cells=CELLS_AB, golden=GOOD, red=None, tests=(TA, TB), files=(VERIFY,), extra_after="", pins="shared_pkg_dir=none\n"):
    body = std_sections(TEST_SEC + (plant or "") + "\n" + (cells or "") + "\n" + extra_after)
    return mk(name, ticket, brief(f"KS-{ticket}", "test_only_input", list(files), list(tests), body), golden, red, pins)


# test_only_input briefs
ti("ti_pass_pin", 9001)
ti("ti_pass_diffplant", 9002, plant="", cells="## Red cells\n- `fixture tx keeps a valid signature`\n", golden=GOLD_FIXPLANT, red=FIXTURE_PLANT, tests=(TB,))
ti("ti_green_with_plant", 9003, golden=GOLD_GREEN)
ti("ti_crash_not_assertion", 9004, golden=GOLD_CRASH)
ti("ti_plant_not_applicable", 9005, plant=PLANT_PIN.replace("sig-' + tx.from, from: tx.from };`\nto", "sig-' + tx.from, from: tx.from, extra: 1 };`\nto"))
ti("ti_redcell_missing", 9006, golden=GOLD_TEST_ONLY_FIX)
# lint refusals
ti("l_no_plant", 9011, plant="", golden=GOOD)
ti("l_both_plants", 9012, red=FIXTURE_PLANT)
ti("l_no_redcells", 9013, cells="")
ti("l_four_tests", 9014, tests=(TA, TB, TO, FIX))
ti("l_golden_names_product", 9015, golden=GOOD + "\n" + diff_of({VERIFY: cur(VERIFY).replace("ok: tx.sig", "ok: !!tx.sig && tx.sig")}))
ti("l_plant_in_declared_test", 9016, plant=PLANT_PIN.replace(VERIFY, TA))
ti("l_plant_incomplete", 9017, plant="## Plant\nfile: `" + VERIFY + "`\nline: 10\nfrom: `x`\n")

# doc_only briefs
EXPECT = "## Expect\nexpect_absent: `old-name`\nexpect_present: `new-name`\nexpect_absent: `old-name` in `" + FRAG + "`\n"


def dob(name, ticket, golden, expect=EXPECT, files=(GUIDE, FRAG, VERIFY), tests=(), checks=""):
    body = std_sections(expect + "\n" + checks)
    return mk(name, ticket, brief(f"KS-{ticket}", "doc_only", list(files), list(tests), body, runner="docs"), golden, None, pins="")


dob("d_pass", 9101, D_GOOD)
dob("d_changed_code_line", 9102, D_CODE)
dob("d_blank_line_in_code", 9103, D_BLANK)
dob("d_trailing_comment", 9104, D_TRAIL)
dob("d_expect_already_holds", 9105, D_GOOD, expect="## Expect\nexpect_absent: `no-such-text-anywhere`\n")
dob("d_partial_fix", 9106, D_PARTIAL)
dob("d_fragment_check_fails", 9107, D_BROKEN)
dob("l_d_no_expect", 9111, D_GOOD, expect="")
dob("l_d_only_present", 9112, D_GOOD, expect="## Expect\nexpect_present: `new-name`\n")
dob("l_d_test_file", 9113, D_GOOD, tests=(TA,))
dob("l_d_json_file", 9114, D_GOOD, files=(GUIDE, FIX))
dob("l_d_golden_undeclared", 9115, D_EXTRA)
dob("l_d_bad_check_cmd", 9116, D_GOOD, checks="## Doc checks\n- `curl http://x`\n")
dob("l_d_in_path_undeclared", 9117, D_GOOD, expect="## Expect\nexpect_absent: `old-name` in `" + README + "`\n")

# ------------------------------------------------------------------ crafted model outputs (direct tier_checker.py runs)
def fence(d):
    return "```diff\n" + d + ("" if d.endswith("\n") else "\n") + "```\n"


outs = {
    "ti_extra_test": fence(OUT_EXTRA_TEST), "ti_touches_product": fence(OUT_PRODUCT), "ti_missing_declared": fence(OUT_MISSING),
    "ti_lost_cell": fence(OUT_LOST_CELL), "ti_bad_anchor": fence(OUT_ANCHOR), "ti_prose_only": "I would add a test that rejects forged signatures.\n",
    "ti_prose_and_diff": "Here is the change:\n" + fence(GOOD),
    "d_extra_file": fence(D_EXTRA), "d_missing_declared": fence(D_MISSING),
}
os.makedirs(os.path.join(root, "outs"))
for k, v in outs.items():
    write(os.path.join(root, "outs"), k + ".md", v)
print(f"fixture built at {root} tip {TIP[:12]}")
