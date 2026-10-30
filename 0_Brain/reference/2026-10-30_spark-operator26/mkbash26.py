import sys, os
OP24 = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_spark-operator24'
W = os.path.dirname(os.path.abspath(__file__))
os.environ['GEN_SRC'] = W + '/clone'
os.environ['GEN_BRIEFS'] = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
os.environ['GEN_TIP'] = '85cd24d81cb97e30e08fdc054d1ba4b65ea8b558'
sys.path.insert(0, OP24)
import mk24
import importlib.util
spec = importlib.util.spec_from_file_location('apply_fix', W + '/apply_fix.py')
af = importlib.util.module_from_spec(spec); spec.loader.exec_module(af)

REF = 'Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh'
SC = 'Blockchain/Dev/scripts/'
SPECS = {
 'p1': dict(D='scripts_akto_names_docker_flags', test='check_akto_container_names_flags.test.sh',
   title="check-akto-container-names.sh: `docker exec -it akto-mongo` and other flagged docker verbs pass the gate (found by operator 26, no ticket; RUNG 2, bash_patch: one product line spelled, plus a new real-tools suite given whole)",
   wrong="""`check-akto-container-names.sh:82` builds the first alternative of the gate's pattern as `docker[[:space:]]+(exec|logs|inspect|cp|kill|stop|rm|restart)[[:space:]]+[\"'\`]?akto-[a-z0-9-]+`: only whitespace may sit between the verb and the container name. The everyday forms put option flags there (`docker exec -it akto-mongo mongosh`, `docker logs --tail=50 akto-testing`), and those pass the gate (exit 0, no output) although they target slot 1 whatever slot the run is aimed at, which is the exact defect the gate exists for (KS-666 / KS-687 F2). The fix is one line: allow any number of `-flag` words between the verb and the name, `([[:space:]]+-[^[:space:]]+)*`.""",
   where=":82 - **must change** (the one `PATTERN=` line). Every other line stays.", gl=82,
   reds=["docker exec -it akto-mongo is flagged", "docker logs --tail=50 \"akto-testing\" is flagged", "docker exec -i -t akto-mongo is flagged"],
   cells="""- RED CELL 1 `docker exec -it akto-mongo is flagged` - red at the tip (exit 0), green with the hunk.
- RED CELL 2 `docker logs --tail=50 "akto-testing" is flagged` - red at the tip.
- RED CELL 3 `docker exec -i -t akto-mongo is flagged` - red at the tip.
- green CELL 4 `CONTROL docker exec akto-mongo is still flagged`.
- green CELL 5 `CONTROL docker exec -it with the AKTO_PREFIX form is clean` - the fix shape stays clean.
- green CELL 6 `CONTROL docker exec -it other-container is clean`.""",
   measured="the suite at the tip is `3 passed, 3 failed` (CELLS 1-3) and with the edited script `6 passed, 0 failed`, on macOS bash 3.2; the existing sibling suite check_akto_container_names.test.sh is unchanged by the edit, and the edited script still exits 0 on the real systemTest/akto tree",
   prem="At `85cd24d81cb9` line 82 is the quoted pattern line; planted in a scratch package (src/, bin/, scripts/ each with a file), `docker exec -it akto-mongo mongosh`, `docker exec -i \"akto-mongo\" mongosh` and `docker logs --tail 5 akto-testing` each exited 0 with empty output, while `docker exec akto-mongo mongosh` exited 1. The repo's own docs write the `-it` form (systemTest/akto/docs/quick-start.md:422, with the derived name). The sibling suite has no flagged-verb case (grep of its docker lines)."),
}

def main(key):
    sp = SPECS[key]
    fname, edits = af.FIX[key]
    PROD = SC + fname
    TEST = SC + '__tests__/' + sp['test']
    old = mk24.rd(PROD); new = old
    for o, n in edits:
        assert new.count(o) == 1, (key, o[:40]); new = new.replace(o, n)
    test = open(W + f'/suites/{key}.sh', encoding='utf-8').read()
    pd = mk24.udiff(PROD, old, new); td = mk24.udiff(TEST, '', test, True)
    d = mk24.BR + sp['D']
    if os.path.exists(d + '/golden.diff') and not os.environ.get('GEN_OVERWRITE'): sys.exit('exists')
    os.makedirs(d, exist_ok=True)
    open(d + '/golden.diff', 'w', encoding='utf-8').write(pd + td)
    open(d + '/spark.pins', 'w').write(f"# bash_patch, new test file; ref = a sibling suite; operator 25 guard-script screen, no ticket.\ntier=bash_patch\nref={REF}\ntest_file={TEST}\nline={sp['gl']}\n")
    n = len(test.splitlines())
    body = pd.split(f'+++ b/{PROD}\n', 1)[1]
    nh = body.count('\n@@') + (1 if body.startswith('@@') else 0)
    reds = '\n'.join('- ' + r for r in sp['reds'])
    md = f"""# KS-0 {sp['title']}

DRAFT by Spark operator 25 for Wednesday, 2026-10-30 AEDT. Secuura (Blockchain/Dev/scripts) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: operator 25's screen of the sibling check-*.sh guards (plant a real violation in a scratch tree, run the script; method of operator 24). No Linear ticket exists; the raise seat files one on the board account or links the filing.

File: `{PROD}`  (product, modified in place: {nh} hunk{'s' if nh != 1 else ''})
Test file: `{TEST}`  (NEW, {n} lines)
Tip: `{mk24.TIP}` (develop, read with `git show`-equivalent in a clone at exactly this sha on 2026-10-30)
Runner: `bash` (bash 3.2, `bash {TEST}` from the repo root)
Tier: `bash_patch`
Rung: **{3 if nh > 1 else 2}** ({nh} product hunk{'s' if nh != 1 else ''} given byte-exact; the test is copied whole)

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 files, in this order:
1. `{PROD}` - modified in place, EXACTLY the {nh} hunk{'s' if nh != 1 else ''} under "The exact change", byte for byte.
2. `{TEST}` - a NEW file: `--- /dev/null` then `+++ b/{TEST}`, ONE hunk `@@ -0,0 +1,{n} @@`, every line `+`.

You never touch any other file. The sibling `check_no_latest_tags.test.sh` is shape reference only - do NOT touch it.

## What is wrong (one paragraph)

{sp['wrong']}

## Where

- {sp['where']}

## The exact change

{nh} hunk{'s' if nh != 1 else ''}.

```diff
{body}```

**Do NOT touch** any other line of the script.

## The test

File: `{TEST}`
The shape is the sibling suite `{REF}` (a fixture root with `scripts/<subject>`, the subject resolving its own root).

Emit this text as the new-file hunk `@@ -0,0 +1,{n} @@`, every line prefixed `+`, nothing added or dropped (blank lines in it are `+` lines with nothing after the `+`):

```bash
{test}```

## Red cells
{reds}

## Cells and controls

{sp['cells']}

## The failing case (the "tamper")

Product fix, no tamper. Measured in a scratch tree (the tip's script copied out, the suite pointed at it with its `CHECK_..._SH` variable): {sp['measured']}.

## Premises (each one measured, with where)

- {sp['prem']}
- The suite resolves the subject through an environment variable (default: the script beside `__tests__/`); nothing in it touches the real tree.

## UNMEASURED - stated rather than glossed

- The drafter ran the suite by hand against the tip and the edited script (results above) but did NOT run `round.sh --dry-run`/`--control` before this text was written; that run is the proof.
- Whether CI runs `__tests__/*.test.sh` automatically is not measured here.

## Scope

**Refs the filing (no ticket); never a close-word.** Only the line(s) named above; nothing else in the script.

## Output

Exactly ONE fenced ```diff block, nothing outside it:
1. the product file (`--- a/{PROD}` / `+++ b/{PROD}`) with the hunk{'s' if nh != 1 else ''} given under "The exact change";
2. the new test file (`--- /dev/null` / `+++ b/{TEST}`, `@@ -0,0 +1,{n} @@`), every line `+`.
Every `+` line on its own physical line. Every context line keeps its leading space.
"""
    open(d + '/KS-0.md', 'w', encoding='utf-8').write(md)
    print('wrote', d)

main(sys.argv[1])
