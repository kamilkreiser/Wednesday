# Operator 48 brief generator (bash_patch). Helpers (rd, udiff, trim) from operator 24's mk24; the brief shape is operator 26's mkbash26.
import sys, os, importlib.util
OP24='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_spark-operator24'
O='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_spark-operator48'
sys.path.insert(0, OP24)
os.environ.pop('GEN_SRC', None)
import mk24
mk24.SRC='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src/'
TIP=mk24.TIP='d7691f35312ea158f043e87a3227e477cccb183d'
BR=mk24.BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
exec(open(O+'/gen/fixes48.py').read())
SC='systemTest/__tests__/'
PRSCAN="the 19 open PRs read 2026-11-01 through the GitHub REST API (108 file entries; planted positive control: the same scan finds services/auth in 7 entries); none touches package_format_gate.test.sh, check-package-format.sh or the new suite name"

SPECS = {
 'p1': dict(D='o48_p1_ks1926_package_format_gate_dead_pid_ps', ticket='KS-1926', mode='new',
   test='systemTest/__tests__/package_format_gate_dead_pid.test.sh', ref='systemTest/__tests__/manifest_path.test.sh',
   title="package_format_gate.test.sh: cases 20 and 32 pick their dead pid with kill -0, so a live process of another user is called dead (RUNG 3, bash_patch: two one-line product hunks given byte-exact, plus a NEW suite given whole)",
   wrong="""The file `systemTest/__tests__/package_format_gate.test.sh` is the test; the gate it drives (`systemTest/scripts/check-package-format.sh:319-337`, `_sweep_dead_stages`) is correct and stays untouched. Cases 20 (line 654) and 32 (line 883) pick a "dead" pid with `dead=$((50000 + RANDOM % 9000)); while kill -0 "$dead" 2>/dev/null; do dead=$((dead + 1)); done`. On macOS `kill -0` reports EPERM (failure) for a LIVE process owned by another user, so the loop accepts such a pid as dead; the test plants a stage for it, the gate decides with `ps -p`, sees it alive and rightly leaves the stage, and the cell `a stage of a DEAD pid is swept` fails (want "no", got "yes"). Two pushes failed on it on 2026-11-01. The fix changes the loop condition at both lines to `ps -p "$dead" >/dev/null 2>&1`, the way the gate decides, and adds one comment line above each. The product here is that TEST file; the new suite pins the picker.""",
   wline=654,
   reds="""- `picker 1 skips a live pid owned by another user`
- `picker 2 skips a live pid owned by another user`""",
   cells="""- RED CELL 2 `picker 1 skips a live pid owned by another user` - red at the tip (the line returns the live pid it started on), green with the hunks.
- RED CELL 3 `picker 2 skips a live pid owned by another user` - the same for the second picker line (case 32).
- green CELL 1 `CONTROL the suite holds exactly two picker lines (cases 20 and 32)`.
- green CELLS 4-5 `CONTROL picker N keeps a free start pid` - a pid neither tool sees is kept unchanged.
Test-only seam, defaulting OFF: none is added to the product. The suite copies each picker line out of `package_format_gate.test.sh` (`grep -F`), replaces the text `50000 + RANDOM % 9000` with a chosen start pid in the COPY, and `eval`s it in a subshell. The start is a live process of another user (kill -0 fails, ps -p succeeds), taken from 50000-58999 first, else any; with none visible (root) the suite skips those two cells and expects 3 passes.""",
   measured="the new suite at the tip is `3 passed, 2 failed` (CELLS 2-3 red, start pid 58433 = a live root-owned process in 50000-58999, kill -0 rc 1, ps -p rc 0) and beside the edited file `5 passed, 0 failed`, on macOS bash 3.2",
   prem="At `d7691f35312e` lines 654 and 883 of `package_format_gate.test.sh` are the identical picker line; line 653 is `R20=\"$(fx_new case20)\"; fx_pkg_tgz \"$R20\" inst prettier` and line 882 is `R32b=\"$(fx_new tree5b)\"; fx_tree_pkg \"$R32b\" tp good; fx_commit \"$R32b\"; G32=\"$(sha_of \"$R32b\")\"`. KS-1926 (Seat R 71st) measured live root pid 54986 failing and free pid 50500 passing."),
}

def main(key):
    sp = SPECS[key]
    R2 = os.environ.get('R2') == '1'
    if R2: sp = dict(sp, D=sp['D'] + '_r2')
    PROD, edits = FIX[key]
    TEST = sp['test']
    old = mk24.rd(PROD); new = old
    for o, n in edits:
        assert new.count(o) == 1, (key, o[:40]); new = new.replace(o, n)
    pd = mk24.udiff(PROD, old, new)
    if sp['mode'] == 'new':
        test = open(O + f'/suites/{key}.sh', encoding='utf-8').read()
        td = mk24.udiff(TEST, '', test, True)
        n = len(test.splitlines())
    else:
        told = mk24.rd(TEST); tnew = open(O + '/scratch/new/' + TEST, encoding='utf-8').read()
        td = mk24.udiff(TEST, told, tnew)
    d = BR + sp['D']
    if os.path.exists(d + '/golden.diff') and not os.environ.get('GEN_OVERWRITE'): sys.exit('exists')
    os.makedirs(d, exist_ok=True)
    open(d + '/golden.diff', 'w', encoding='utf-8').write(pd + td)
    open(d + '/spark.pins', 'w').write(f"# bash_patch; {'NEW' if sp['mode']=='new' else 'MODIFY-IN-PLACE'} test file; ref = a sibling suite (shape only); operator 46.\ntier=bash_patch\nref={sp['ref']}\ntest_file={TEST}\nline={sp['wline']}\n")
    body = pd.split(f'+++ b/{PROD}\n', 1)[1]
    hdr_p = f'--- a/{PROD}\n+++ b/{PROD}\n'
    nh = body.count('\n@@') + (1 if body.startswith('@@') else 0)
    tbody = td.split(f'+++ b/{TEST}\n', 1)[1]
    hdr_t = f'--- a/{TEST}\n+++ b/{TEST}\n'
    nth = tbody.count('\n@@') + (1 if tbody.startswith('@@') else 0)
    if sp['mode'] == 'new':
        tmode = f"a NEW file: `--- /dev/null` then `+++ b/{TEST}`, ONE hunk `@@ -0,0 +1,{n} @@`, every line `+`."
        tfile = f"`{TEST}`  (NEW, {n} lines)"
        tsec = f"""File: `{TEST}`
The shape reference is the sibling suite `{sp['ref']}`; the new suite is given WHOLE. Emit this text as the new-file hunk `@@ -0,0 +1,{n} @@`, every line prefixed `+`, nothing added or dropped (blank lines in it are `+` lines with nothing after the `+`):

```bash
{test}```
"""
        outtest = f"2. the new test file (`--- /dev/null` / `+++ b/{TEST}`, `@@ -0,0 +1,{n} @@`), every line `+`."
    else:
        tmode = f"MODIFIED in place: EXACTLY the {nth} hunk{'s' if nth != 1 else ''} under \"The test\", byte for byte (the file already exists at the tip; `--- a/{TEST}` / `+++ b/{TEST}`, NEVER `/dev/null`)."
        tfile = f"`{TEST}`  (existing suite, MODIFIED in place: {nth} hunk{'s' if nth != 1 else ''})"
        tsec = f"""File: `{TEST}` (EXISTS at the tip; modify it, do not recreate it)
The shape reference is the sibling suite `{sp['ref']}`. The test change is DICTATED: {nth} hunk{'s' if nth != 1 else ''}, header lines and `@@` lines included, copy them character for character, do not recount.

```diff
{hdr_t}{tbody}```
"""
        outtest = f"2. the existing test file (`--- a/{TEST}` / `+++ b/{TEST}`) with the hunk{'s' if nth != 1 else ''} given under \"The test\"."
    WARN = ('\n**QUOTE WARNING (rebrief).** The first attempt wrote `[\\\\\\"]` (three backslashes) where the file has `[\\"]`. In the `PATTERN+=` line the quote class is exactly these five characters: `[`, ONE backslash, a double quote, a single quote, `]`. Copy that line character for character from the fence above; do not add or remove a backslash anywhere in it.\n' if R2 else '')
    md = f"""# {sp['ticket']} {sp['title']}

DRAFT by Spark operator 46 for Wednesday, 2026-11-01. Secuura (Blockchain/Dev, scripts and systemTest shell guards) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: {sp['ticket']} (Backlog), board screen 2026-11-01 21:27, Spark candidate list. No open PR touches the files: {PRSCAN}.

File: `{PROD}`  (product, modified in place: {nh} hunk{'s' if nh != 1 else ''})
Test file: {tfile}
Tip: `{TIP}` (origin develop, confirmed by fetch on 2026-11-01; every line number and quote below was read from it)
Runner: `bash` (bash 3.2, `bash {TEST}` from the repo root)
Tier: `bash_patch`
Rung: **{3 if (nh + nth) > 2 else 2}** ({nh} product hunk{'s' if nh != 1 else ''} given byte-exact; the test is {'copied whole' if sp['mode']=='new' else 'dictated hunk by hunk'})

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 files, in this order:
1. `{PROD}` - modified in place, EXACTLY the {nh} hunk{'s' if nh != 1 else ''} under "The exact change", byte for byte.
2. `{TEST}` - {tmode}

You never touch any other file. The sibling `{sp['ref']}` is shape reference only - do NOT touch it.

## What is wrong (one paragraph)

{sp['wrong']}

## Where

- :654 - **case 20 picker line: its `while` condition `kill -0 "$dead" 2>/dev/null` becomes `ps -p "$dead" >/dev/null 2>&1`; one comment line is added above it.**
- :883 - **case 32 picker line: the identical change.**
Every other line of the file stays.

## The exact change

{nh} hunk{'s' if nh != 1 else ''}. The file header lines and the `@@` lines are DICTATED: copy them character for character, do not recount. Context lines start with ONE space, removed lines with `-`, added lines with `+` (byte-exact; spaces only). Where a `+` line holds a backslash, a double quote, a single quote or a backtick, copy every character exactly.

```diff
{hdr_p}{body}```

**Do NOT touch** any other line of the script.
{WARN}

## The test

{tsec}
## Red cells
{sp['reds']}

## Cells and controls

{sp['cells']}

## The failing case (the "tamper")

Product fix, no tamper. Measured in a scratch tree (the tip's script copied out, the suite pointed at it): {sp['measured']}.

## Premises (each one measured, with where)

- {sp['prem']}
- The suite resolves the subject beside itself (or through an environment variable) and works only in a private temp dir; nothing in it touches the real tree.

## UNMEASURED - stated rather than glossed

- The drafter ran the suite by hand against the tip and the edited script (results above) but did NOT run `round.sh --dry-run`/`--control` before this text was written; that run is the proof.
- Whether CI runs the shell suites automatically, and GNU/Linux behaviour of the script (macOS BSD tools were used), are not measured here.

## Scope

**Refs {sp['ticket']}; never a close-word.** Only the line(s) named above; nothing else in the script.

## Output

Exactly ONE fenced ```diff block, nothing outside it:
1. the product file (`--- a/{PROD}` / `+++ b/{PROD}`) with the hunk{'s' if nh != 1 else ''} given under "The exact change";
{outtest}
Every `+` line on its own physical line. Every context line keeps its leading space.
"""
    open(d + '/KS-0.md', 'w', encoding='utf-8').write(md.replace('KS-0', sp['ticket']) if False else md)
    # brief file must be named KS-<n>.md
    os.replace(d + '/KS-0.md', d + '/' + sp['ticket'] + '.md')
    print('wrote', d, 'prod hunks', nh, 'test hunks', nth)

main(sys.argv[1])
