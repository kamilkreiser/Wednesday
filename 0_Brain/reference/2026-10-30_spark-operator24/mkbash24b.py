import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mk24
W = os.path.dirname(os.path.abspath(__file__))
PROD = 'Blockchain/Dev/scripts/check-no-sql-injection.sh'
TEST = 'Blockchain/Dev/scripts/__tests__/check_no_sql_injection_reports_the_hit.test.sh'
REF = 'Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh'
D = 'filing_sqlinj_p2_report_the_hit'
OLD = 'injection risk — $queryRawUnsafe / $executeRawUnsafe used'
NEW = 'injection risk — \\$queryRawUnsafe / \\$executeRawUnsafe used'
old = mk24.rd(PROD); assert old.count(OLD) == 1
new = old.replace(OLD, NEW)
test = open(W + '/bash1/test2.sh', encoding='utf-8').read()
pd = mk24.udiff(PROD, old, new); td = mk24.udiff(TEST, '', test, True)
d = mk24.BR + D
if os.path.exists(d + '/golden.diff') and not os.environ.get('GEN_OVERWRITE'): sys.exit('exists')
os.makedirs(d, exist_ok=True)
open(d + '/golden.diff', 'w', encoding='utf-8').write(pd + td)
open(d + '/spark.pins', 'w').write(f"# bash_patch, new test file; ref = a sibling suite; filing-list item, no ticket (Backlog check: none).\ntier=bash_patch\nref={REF}\ntest_file={TEST}\nline=28\n")
n = len(test.splitlines())
body = pd.split(f'+++ b/{PROD}\n', 1)[1]
md = f"""# KS-0 check-no-sql-injection.sh: the failure headline expands two unset variables, so under set -u a real hit aborts the script before the hit list is printed (found by operator 24, no ticket; RUNG 2, bash_patch: one product line spelled, plus a new stub-PATH suite given whole)

DRAFT by Spark operator 24 for Wednesday, 2026-10-30 AEDT. Secuura (Blockchain/Dev/scripts) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: found by operator 24 while testing the exclude-dir filing item (no Linear ticket exists; the raise seat files one on the board account or links the filing). `check-no-sql-injection.sh:35` echoes `::error::SQL injection risk - $queryRawUnsafe / $executeRawUnsafe used ...` inside double quotes and the script runs under `set -euo pipefail`, so the shell aborts with `queryRawUnsafe: unbound variable` (exit 1) before the hit list and the Fix hints are printed: the gate fails but names nothing. The sibling lines 39 and 41 already escape their dollar signs.

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

At `check-no-sql-injection.sh:35` the headline is `echo "::error::SQL injection risk — $queryRawUnsafe / $executeRawUnsafe used with template-literal interpolation:"`. Both `$queryRawUnsafe` and `$executeRawUnsafe` are meant as literal text but are unset shell variables, and `set -u` makes the expansion fatal. The fix is to escape the two dollar signs with a backslash, exactly as lines 39 and 41 do: `\\$queryRawUnsafe / \\$executeRawUnsafe`.

## Where

- `:35` - **must change**: the `echo "::error::..."` headline - the two dollar signs before `queryRawUnsafe` and `executeRawUnsafe` each gain a backslash.
- `:28` (the scan grep) and every other line - (correct) stays unchanged; `:36`-`:41` are context.

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
- a hit prints the error headline naming both Unsafe calls
- a hit prints the offending file and line

## Cells and controls

- RED CELL 1 `a hit prints the error headline naming both Unsafe calls` - red at the tip (the script aborts at the headline with an unbound variable), green with the product hunk.
- RED CELL 2 `a hit prints the offending file and line` - red at the tip for the same reason.
- green CELL 3 `CONTROL a hit exits 1 and a clean scan exits 0 with the OK line` - the exit codes are untouched.
- green CELL 4 `CONTROL a hit under node_modules is still filtered out` - the script's own `grep -v` filter stays.

## The failing case (the "tamper")

Product fix, no tamper. Measured in a scratch tree (the tip's script written out with `git show`, the suite pointed at it with `CHECK_NO_SQL_INJECTION_SH=`), bash 3.2: the suite at the tip is `2 passed, 2 failed` (the two FAILs are CELL 1 and CELL 2) and with the edited script `4 passed, 0 failed`.

## Premises (each one measured, with where)

- `{PROD}` at `{mk24.TIP[:12]}`: the script runs under `set -euo pipefail`; line 35 is the headline quoted above; lines 39 and 41 escape their dollar signs (`\\$executeRawUnsafe`, `\\$queryRaw`).
- Measured in the scratch tree: with a planted hit the tip prints only `scripts/check-no-sql-injection.sh: line 35: queryRawUnsafe: unbound variable` and exits 1.
- The suite resolves the subject through `CHECK_NO_SQL_INJECTION_SH` (default: the script beside `__tests__/`); nothing in it touches the real tree. A sibling brief (filing_sqlinj_p1) edits line 28 of the same script: disjoint hunks.

## UNMEASURED - stated rather than glossed

- The drafter ran the suite by hand against the tip and the edited script (results above) but did NOT run `round.sh --dry-run`/`--control` before this text was written; that run is the proof.
- Whether the script's stdout is read by anything that parses it is not measured.

## Scope

**Refs the filing list item (no ticket); never a close-word.** The headline escaping at `:35` only; the scan at `:28` is the sibling brief's.

## Output

Exactly ONE fenced ```diff block, nothing outside it:
1. the product file (`--- a/{PROD}` / `+++ b/{PROD}`) with the single hunk given under "The exact change";
2. the new test file (`--- /dev/null` / `+++ b/{TEST}`, `@@ -0,0 +1,{n} @@`), every line `+`.
Every `+` line on its own physical line. Every context line keeps its leading space.
"""
open(d + '/KS-0.md', 'w', encoding='utf-8').write(md)
print('wrote', d)
