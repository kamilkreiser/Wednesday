# Operator 46 brief generator (bash_patch). Helpers (rd, udiff, trim) from operator 24's mk24; the brief shape is operator 26's mkbash26.
import sys, os, importlib.util
OP24='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_spark-operator24'
O='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_spark-operator46'
sys.path.insert(0, OP24)
os.environ.pop('GEN_SRC', None)
import mk24
mk24.SRC='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src/'
TIP=mk24.TIP='d7691f35312ea158f043e87a3227e477cccb183d'
BR=mk24.BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
exec(open(O+'/gen/fixes46.py').read())
SC='Blockchain/Dev/scripts/'
PRSCAN="the 19 open PRs read 2026-11-01 through the GitHub REST API (108 file entries; planted positive control: the same scan finds services/auth in 7 entries); none touches the script or its suite"

SPECS = {
 'p1': dict(D='o46_p1_ks1903_dockerfile_non_root_user_group_case', ticket='KS-1903', mode='modify',
   test=SC+'__tests__/check_dockerfile_non_root_reports_root.test.sh', ref=SC+'__tests__/check_no_latest_tags.test.sh',
   title="check-dockerfile-non-root.sh: a final USER of root:root, 0:0 or ROOT passes the non-root guard (RUNG 3, bash_patch: one product hunk given byte-exact, plus cells added to the existing suite)",
   wrong="""`check-dockerfile-non-root.sh:27` reads the last `USER` value of each Dockerfile and `:32` tests it with `= "root"` or `= "0"` only. So a final `USER root:root`, `USER 0:0` or `USER ROOT` is read as `root:root`, `0:0` or `ROOT`, matches neither, and the gate prints `OK` for a container that runs as root. Measured in the ticket with the real script: `USER root` rc 1 (reported), `USER app` rc 0, but `root:root`, `0:0` and `ROOT` all rc 0 `OK`. The fix is two lines after the line that reads the value: drop any `:group` suffix, then lowercase it, so every spelling reaches the existing comparison as `root` or `0`.""",
   wline=27,
   reds="""- `a final USER root:root exits 1 and is named`
- `a final USER 0:0 exits 1 and is named`
- `a final USER ROOT exits 1 and is named`""",
   cells="""- RED CELL 5 `a final USER root:root exits 1 and is named` - red at the tip (rc 0, OK), green with the hunk.
- RED CELL 6 `a final USER 0:0 exits 1 and is named` - red at the tip.
- RED CELL 7 `a final USER ROOT exits 1 and is named` - red at the tip.
- green CELL 8 `CONTROL USER app:app exits 0` - a non-root user:group still passes.
- green CELL 9 `CONTROL USER 1000:1000 exits 0` - a numeric non-root uid:gid still passes.
The four existing cells 1-4 are untouched; only the closing `PASS -eq 4` becomes `PASS -eq 9`.""",
   measured="the edited suite at the tip is `6 passed, 3 failed` (CELLS 5-7 red) and with the edited script `9 passed, 0 failed`, on macOS bash 3.2",
   prem="At `d7691f35312e` line 27 reads the value and line 32 is `elif [ \"$last_user\" = \"root\" ] || [ \"$last_user\" = \"0\" ]; then`; the suite has 4 cells and ends `[[ \"$FAIL\" -eq 0 && \"$PASS\" -eq 4 ]]`. The BSD `\\s` fault of the same line was already fixed on develop (operator 25's pass), so the suite runs the real script on macOS."),
 'p2': dict(D='o46_p2_ks1902_akto_names_flag_value_token', ticket='KS-1902', mode='modify',
   test=SC+'__tests__/check_akto_container_names_flags.test.sh', ref=SC+'__tests__/check_akto_container_names.test.sh',
   title="check-akto-container-names.sh: a docker flag that takes a value (-u root, -e FOO=1) before an akto container name still passes the guard (RUNG 2, bash_patch: one product hunk of pure additions given byte-exact, plus cells added to the existing suite)",
   wrong="""`check-akto-container-names.sh:82` flags `docker <verb> -flag ... akto-<role>` where every `-flag` is ONE dash-token, so a flag that takes a separate value word (`-u root`, `-e FOO=1`, `--tail 5`) breaks the chain between the verb and the name and the line passes (exit 0, nothing printed) although it targets slot 1. The fix ADDS one more alternative to the pattern (line 82 stays exactly as it is): the same verb group, then one or more `-flag` tokens each optionally followed by ONE value word (`[^-[:space:]][^[:space:]]*`), then the name. Quoted names with a backtick are not covered by the new alternative (stated gap; the existing alternative still covers the no-value forms).""",
   wline=87,
   reds="""- `docker exec -u root akto-mongo is flagged`
- `docker exec -e FOO=1 akto-mongo is flagged`
- `docker exec -it -u root akto-mongo is flagged`
- `docker logs --tail 5 akto-testing is flagged`
- `docker exec -u root "akto-mongo" is flagged`""",
   cells="""- RED CELL 7 `docker exec -u root akto-mongo is flagged` - red at the tip (exit 0), green with the hunk.
- RED CELL 8 `docker exec -e FOO=1 akto-mongo is flagged` - red at the tip.
- RED CELL 9 `docker exec -it -u root akto-mongo is flagged` - red at the tip.
- RED CELL 10 `docker logs --tail 5 akto-testing is flagged` - red at the tip.
- RED CELL 11 `docker exec -u root "akto-mongo" is flagged` - red at the tip.
- green CELL 12 `CONTROL docker exec -u root other-mongo is clean`.
- green CELL 13 `CONTROL docker exec -u root with the AKTO_PREFIX form is clean`.
The six existing cells 1-6 are untouched.""",
   measured="the edited suite at the tip is `8 passed, 5 failed` (CELLS 7-11 red) and with the edited script `13 passed, 0 failed`, on macOS bash 3.2 and BSD grep",
   prem="At `d7691f35312e` line 82 is the `PATTERN=` line and lines 83-85 are the three `PATTERN+=` lines; line 86 is blank and line 87 is `hits=$(`. Planted with the real script in a scratch package, `docker exec -u root akto-mongo mongosh`, `docker exec -e FOO=1 akto-mongo mongosh` and `docker logs --tail 5 akto-testing` each exited 0 with no output (the ticket measured the same). No line of lines 82-85 is part of the diff: the hunk adds after the blank line 86."),
 'p3': dict(D='o46_p3_ks1884_readers_agree_driver_stderr', ticket='KS-1884', mode='new',
   test='systemTest/__tests__/manifest_readers_agree_stderr.test.sh', ref='systemTest/__tests__/manifest_path.test.sh',
   title="manifest_readers_agree.test.sh: the drivers discard stderr, so a tool failure reads as a reader disagreement and its reason is lost (RUNG 3, bash_patch: three product hunks given byte-exact, plus a NEW suite given whole)",
   wrong="""`systemTest/__tests__/manifest_readers_agree.test.sh` runs four driver functions (writer, playwright, performance, schemathesis); each ends `2>/dev/null | tail -1`. A driver that fails to start prints nothing, `case_` then reports `FAIL ... writer='' ...` as if the readers disagreed, and the reason is gone (KS-1884: one pre-push failure whose cause could not be measured). The fix sends each driver's stderr to its own file in a private temp dir (`$ERR_DIR/<driver>`, replaced on every call so it always belongs to the current case) and `case_` prints each non-empty one under its FAIL line. The stdout handling, the answers and the exit status are unchanged.""",
   wline=43,
   reds="""- `a driver's stderr is printed on a FAIL (npx)`
- `a driver's stderr is printed on a FAIL (python3)`""",
   cells="""- RED CELL 1 `a driver's stderr is printed on a FAIL (npx)` - red at the tip (the stub's noise is discarded), green with the hunks.
- RED CELL 2 `a driver's stderr is printed on a FAIL (python3)` - red at the tip (the schemathesis driver).
- green CELL 3 `CONTROL silent drivers still fail the suite with FAIL lines`.
- green CELL 4 `CONTROL an ok line never carries driver stderr`.""",
   measured="with the suite in a tree beside the tip subject it is `2 passed, 2 failed` (CELLS 1-2 red) and beside the edited subject `4 passed, 0 failed`, on macOS bash 3.2; each run takes about 3 s (stubs, no tsx)",
   prem="At `d7691f35312e` the four driver functions end at lines 46, 51, 56 and 66 with `2>/dev/null | tail -1 )`; `case_` is lines 70-79 and its FAIL echo is line 77. The subject sources `support/slot-expect.sh`, which reads the slot ceiling from `Blockchain/Dev/scripts/stack_env.sh`, so the new suite copies those two files into its fixture tree. Run with a stub `npx` and `python3` that print a marker on stderr and nothing on stdout, the tip subject prints no marker at all; the edited one prints it under each FAIL line."),
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

- :{sp['wline']} - the hunk below sits here; it only adds (and, for the closing count or the driver redirects, rewrites) the lines shown. Every other line stays.

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
