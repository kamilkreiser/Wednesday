import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mk24
W = os.path.dirname(os.path.abspath(__file__))
PROD = 'Blockchain/Dev/scripts/check-no-sql-injection.sh'
TEST = 'Blockchain/Dev/scripts/__tests__/check_no_sql_injection_skips_node_modules.test.sh'
REF = 'Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh'
D = 'filing_sqlinj_p1_exclude_node_modules'
OLD = "hits=$(grep -rEn --include='*.ts' --include='*.tsx' --include='*.js' \\\n"
NEW = "hits=$(grep -rEn --exclude-dir=node_modules --include='*.ts' --include='*.tsx' --include='*.js' \\\n"
old = mk24.rd(PROD); assert old.count(OLD) == 1
new = old.replace(OLD, NEW)
test = open(W + '/bash1/test.sh', encoding='utf-8').read()
pd = mk24.udiff(PROD, old, new); td = mk24.udiff(TEST, '', test, True)
d = mk24.BR + D
if os.path.exists(d + '/golden.diff') and not os.environ.get('GEN_OVERWRITE'): sys.exit('exists')
os.makedirs(d, exist_ok=True)
open(d + '/golden.diff', 'w', encoding='utf-8').write(pd + td)
open(d + '/spark.pins', 'w').write(f"# bash_patch, new test file; ref = a sibling suite; filing-list item, no ticket (Backlog check: none).\ntier=bash_patch\nref={REF}\ntest_file={TEST}\nline=28\n")
n = len(test.splitlines())
body = pd.split(f'+++ b/{PROD}\n', 1)[1]
md = f"""# KS-0 check-no-sql-injection.sh: pass --exclude-dir=node_modules to the scan grep, as every sibling check-no-*.sh does (filing-list item, no ticket; RUNG 2, bash_patch: one product line spelled, plus a new stub-PATH suite given whole)

DRAFT by Spark operator 24 for Wednesday, 2026-10-30 AEDT. Secuura (Blockchain/Dev/scripts) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: Wednesday's filing list (no Linear ticket exists; the raise seat files one on the board account or links the filing). The scan in `check-no-sql-injection.sh` reads every installed package under `services/` and `packages/` and only afterwards drops the hits whose path names node_modules; `check-no-default-passwords.sh`, `check-no-math-random.sh` and `check-no-trust-header-reads.sh` already pass `--exclude-dir=node_modules` to grep itself. Behaviour of the gate is unchanged (the later filter stays); the cost is.

File: `{PROD}`  (product, modified in place: 1 hunk)
Test file: `{TEST}`  (NEW, {n} lines)
Tip: `{mk24.TIP}` (develop, read with `git show` in a clone at exactly this sha on 2026-10-30; the script is 51 lines)
Runner: `bash` (bash 3.2, `bash {TEST}` from the repo root; grep is a stub on a private PATH)
Tier: `bash_patch`
Rung: **2** (one product line given byte-exact; the test is copied whole)

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 files, in this order:
1. `{PROD}` - modified in place, EXACTLY the 1 hunk under "The exact change", byte for byte.
2. `{TEST}` - a NEW file: `--- /dev/null` then `+++ b/{TEST}`, ONE hunk `@@ -0,0 +1,{n} @@`, every line `+`.

You never touch any other file. The sibling `check_no_latest_tags.test.sh` is shape reference only - do NOT touch it.

## What is wrong (one paragraph)

`check-no-sql-injection.sh:28` runs `grep -rEn --include='*.ts' --include='*.tsx' --include='*.js' ... services/ packages/` and pipes it through `grep -v 'node_modules\\|/dist/\\|...'`. The recursive scan therefore walks every `node_modules` tree first. The fix is one added grep option, `--exclude-dir=node_modules`, right after `-rEn`; the `grep -v` filter stays as it is.

## Where

- `:28` - **must change**: `hits=$(grep -rEn --include='*.ts' --include='*.tsx' --include='*.js' \\` - gains `--exclude-dir=node_modules ` between `-rEn` and `--include='*.ts'`.
- `:29`-`:31` and everything else - (correct) stays unchanged.

## The exact change

1 hunk. One line replaced by one.

```diff
{body}```

**Do NOT touch** any other line of the script.

## The test

File: `{TEST}`
The shape is the sibling suite `Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh` (a fixture root with `scripts/<subject>`, the subject resolving its own root) with a stub `grep` on a private `PATH`.

Emit this text as the new-file hunk `@@ -0,0 +1,{n} @@`, every line prefixed `+`, nothing added or dropped (blank lines in it are `+` lines with nothing after the `+`):

```bash
{test}```

## Red cells
- the scan call carries --exclude-dir=node_modules

## Cells and controls

- RED CELL 1 `the scan call carries --exclude-dir=node_modules` - red at the tip (the logged scan call is `-rEn --include=*.ts ...` with no exclude), green with the product hunk.
- green CELL 2 `CONTROL the scan still reads .ts, .tsx and .js under services/ and packages/` - the three includes and both roots survive the edit.
- green CELL 3 `CONTROL a clean scan exits 0 and a hit in service source exits 1` - the gate's exit codes are untouched.
- green CELL 4 `CONTROL a hit under node_modules is still filtered out` - the script's own `grep -v` filter stays.

## The failing case (the "tamper")

Product fix, no tamper. Measured in a scratch tree (the tip's script written out with `git show`, the suite pointed at it with `CHECK_NO_SQL_INJECTION_SH=`), bash 3.2: the suite at the tip is `3 passed, 1 failed` (the one FAIL is CELL 1) and with the edited script `4 passed, 0 failed`.

## Premises (each one measured, with where)

- `{PROD}` at `{mk24.TIP[:12]}` line 28 is the grep line quoted above; the three sibling scripts carry `--exclude-dir=node_modules` at `check-no-default-passwords.sh:29`, `check-no-math-random.sh:26`, `check-no-trust-header-reads.sh:36`.
- Under `set -u` the script's error echo at `:35` expands `$queryRawUnsafe` as an unset variable (the backslash is missing), so a REAL hit makes the script die with `queryRawUnsafe: unbound variable` (still exit 1) instead of printing its message. That is a separate defect, NOT part of this task: the suite asserts only the exit code for the hit case, and the edit must not touch `:35`.
- The suite resolves the subject through `CHECK_NO_SQL_INJECTION_SH` (default: the script beside `__tests__/`); nothing in it touches the real tree.

## UNMEASURED - stated rather than glossed

- The drafter ran the suite by hand against the tip and the edited script (results above) but did NOT run `round.sh --dry-run`/`--control` before this text was written; that run is the proof.
- Whether `run-code-guards.sh` or preflight run `__tests__/*.test.sh` automatically is not measured here.
- The unbound-variable defect at `:35` is filed, not fixed.

## Scope

**Refs the filing list item (no ticket); never a close-word.** One option added to one grep call; `:35` untouched.

## Output

Exactly ONE fenced ```diff block, nothing outside it:
1. the product file (`--- a/{PROD}` / `+++ b/{PROD}`) with the single hunk given under "The exact change";
2. the new test file (`--- /dev/null` / `+++ b/{TEST}`, `@@ -0,0 +1,{n} @@`), every line `+`.
Every `+` line on its own physical line. Every context line keeps its leading space.
"""
open(d + '/KS-0.md', 'w', encoding='utf-8').write(md)
print('wrote', d)
