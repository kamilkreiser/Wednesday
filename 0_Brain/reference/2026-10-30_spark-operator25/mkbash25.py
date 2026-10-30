import sys, os
OP24 = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_spark-operator24'
W = os.path.dirname(os.path.abspath(__file__))
os.environ['GEN_SRC'] = W + '/clone'
os.environ['GEN_TIP'] = '85cd24d81cb97e30e08fdc054d1ba4b65ea8b558'
sys.path.insert(0, OP24)
import mk24
import importlib.util
spec = importlib.util.spec_from_file_location('apply_fix', W + '/apply_fix.py')
af = importlib.util.module_from_spec(spec); spec.loader.exec_module(af)

REF = 'Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh'
SC = 'Blockchain/Dev/scripts/'
SPECS = {
 'p1': dict(D='scripts_dockerfile_non_root_reports_root', test='check_dockerfile_non_root_reports_root.test.sh',
   title="check-dockerfile-non-root.sh: a Dockerfile with no USER dies silently, and under BSD sed a final USER root is read as USERroot and passes (found by operator 25, no ticket; RUNG 2, bash_patch: one product line spelled, plus a new real-tools suite given whole)",
   wrong="""`check-dockerfile-non-root.sh:27` reads the last USER with `grep -E '^\\s*USER\\s+' "$f" | tail -1 | sed -E 's/^\\s*USER\\s+//; s/[#].*$//' | tr -d '[:space:]'` inside `$( )`, under `set -euo pipefail`. Two faults. (1) A Dockerfile with NO USER makes `grep` exit 1, `pipefail` fails the substitution and `set -e` ends the script silently: exit 1, no message, so the gate's own `has NO USER directive` branch (`:30`) is unreachable. (2) `\\s` is not understood by BSD `sed -E` (macOS, the evidence host per KS-666), so `USER root` becomes `USERroot`, never equals `root` or `0`, and the gate prints OK for a root container. The fix is one line: POSIX classes in the grep and the sed, and `|| true` after the last pipe stage.""",
   where=":27 - **must change** (the whole `last_user=$(...)` line). Every other line stays.", gl=27,
   reds=["a Dockerfile with no USER directive exits 1 and is named", "a final USER root exits 1 and is named"],
   cells="""- RED CELL 1 `a Dockerfile with no USER directive exits 1 and is named` - red at the tip (exit 1 but no output at all), green with the hunk.
- RED CELL 2 `a final USER root exits 1 and is named` - red at the tip on a BSD userland (macOS), where the script prints OK for it; on a GNU userland it is green both ways.
- green CELL 3 `CONTROL USER app exits 0 with the OK line`.
- green CELL 4 `CONTROL a root build stage with a non-root final USER exits 0` - the last USER wins, as before.""",
   measured="the suite at the tip is `2 passed, 2 failed` (CELLS 1 and 2) and with the edited script `4 passed, 0 failed`, on macOS bash 3.2 with BSD sed",
   prem="At `85cd24d81cb9` the script is 43 lines; planted in a scratch tree, a Dockerfile with no USER exited 1 with empty output, and `USER root`, `USER 0` both printed `OK - all 1 Dockerfile(s) drop root for runtime` (rc 0). `printf 'USER root\\n' | sed -E 's/^\\s*USER\\s+//'` prints `USER root` unchanged on this Mac. The script is run by `run-code-guards.sh:79`."),
 'p2': dict(D='scripts_strictness_patches_skips_node_modules', test='check_no_strictness_patches_skips_node_modules.test.sh',
   title="check-no-strictness-patches.sh: pass --exclude-dir=node_modules to the scan grep (found by operator 25, no ticket; RUNG 2, bash_patch: one product line spelled, plus a new real-tools suite given whole)",
   wrong="""`check-no-strictness-patches.sh:46` runs `grep -rEn --include='Dockerfile*' --include='*.sh' --include='*.yml' ... services frontend scripts deployment` once per pattern with no `--exclude-dir` and no later node_modules filter, so every installed package under those roots is read six times per run, and a vendored package that mentions `noUnusedLocals = false` fails the gate for code the repo does not own. `check-no-default-passwords.sh`, `check-no-math-random.sh` and `check-no-trust-header-reads.sh` already pass `--exclude-dir=node_modules`. The fix is one added grep option after `-rEn`.""",
   where=":46 - **must change**: gains `--exclude-dir=node_modules ` between `-rEn` and `--include='Dockerfile*'`. Every other line stays.", gl=46,
   reds=["a flip that exists only under node_modules is ignored", "only the repo's own hit is printed"],
   cells="""- RED CELL 1 `a flip that exists only under node_modules is ignored` - red at the tip (exit 1), green with the hunk.
- RED CELL 2 `only the repo's own hit is printed` - red at the tip (the node_modules path is printed too).
- green CELL 3 `CONTROL a real flip exits 1 and is printed`.
- green CELL 4 `CONTROL a clean tree exits 0`.""",
   measured="the suite at the tip is `2 passed, 2 failed` (CELLS 1 and 2) and with the edited script `4 passed, 0 failed`",
   prem="At `85cd24d81cb9` the grep call is the one quoted; planted in a scratch tree, a flip only in `services/s/node_modules/dep/ci.yml` made the script exit 1 and print that path."),
 'p3': dict(D='scripts_connector_xss_skips_node_modules', test='check_connector_xss_skips_node_modules.test.sh',
   title="check-connector-xss.sh: pass --exclude-dir=node_modules to the scan grep (found by operator 25, no ticket; RUNG 2, bash_patch: one product line spelled, plus a new stub-PATH suite given whole)",
   wrong="""`check-connector-xss.sh:23` runs `grep -rEn "(^|[[:space:]<])on[a-z]+=['\\"]" connectors/ --include=...` and only afterwards drops hits whose path names node_modules (`:26`), so the recursive scan reads every installed package under `connectors/` first. `check-no-default-passwords.sh`, `check-no-math-random.sh` and `check-no-trust-header-reads.sh` pass `--exclude-dir=node_modules` to grep itself. Gate behaviour is unchanged (the later filter stays); the cost is.""",
   where=":23 - **must change**: gains `--exclude-dir=node_modules ` between `-rEn` and the quoted pattern. `:24`-`:27` and everything else stay.", gl=23,
   reds=["the scan call carries --exclude-dir=node_modules"],
   cells="""- RED CELL 1 `the scan call carries --exclude-dir=node_modules` - red at the tip (the logged scan call has no exclude), green with the hunk.
- green CELL 2 `CONTROL the scan still reads .js, .ts, .jsx and .tsx under connectors/`.
- green CELL 3 `CONTROL a hit exits 1 and is printed; a clean scan exits 0`.
- green CELL 4 `CONTROL a hit under node_modules is still filtered out` - the script's own filter stays.""",
   measured="the suite at the tip is `3 passed, 1 failed` (CELL 1) and with the edited script `4 passed, 0 failed`",
   prem="At `85cd24d81cb9` line 23 is the grep call quoted; planted in a scratch tree a real inline handler exits 1 and prints the line, and a hit only under `connectors/c/node_modules/` exits 0 (the post-filter works; only the walk is wasted)."),
 'p4': dict(D='scripts_no_pii_store_untracked_leg', test='check_no_pii_store_untracked_leg.test.sh',
   title="check-no-pii-store.sh: the untracked-file leg never fires (invalid git option) and, once it does, would end the script early on a warning (found by operator 25, no ticket; RUNG 3, bash_patch: two product lines spelled in two hunks, plus a new real-git suite given whole)",
   wrong="""Two faults in the second leg. (1) `:56` runs `git ls-files --others --exclude-standard=false ...`; `--exclude-standard` takes no value, so git exits 129 with `option exclude-standard takes no value`, `|| true` hides it, and `UNTRACKED` is always empty: an untracked, not-ignored `pii-data.local.json` (a variant the header names) is never reported. The fix is `--exclude-standard`. (2) `:64` is `{ [ -n "$UNTRACKED" ] && echo ...; [ -n "$FOUND" ] && echo ...; } | sed ...`: when only UNTRACKED is set the group ends on a failing test, `pipefail` + `set -e` exit the script with 1 in the middle of a block that says `(Warning, not a failure.)`. The fix is a final `true;` in the group. Both edits are needed; either alone leaves a visible fault.""",
   where=":56 - **must change** (`--exclude-standard=false` becomes `--exclude-standard`). :64 - **must change** (a `true;` is added before the closing brace). Everything else stays.", gl=56,
   reds=["an untracked pii-data.local.json is reported", "the untracked-file report exits 0 and prints its full block"],
   cells="""- RED CELL 1 `an untracked pii-data.local.json is reported` - red at the tip (the leg is dead), green with the hunks.
- RED CELL 2 `the untracked-file report exits 0 and prints its full block` - red at the tip; it is also what keeps edit 2 honest (with edit 1 alone it stays red).
- green CELL 3 `CONTROL a tracked pii file exits 1 with the git rm hint`.
- green CELL 4 `CONTROL a clean repo exits 0 with no warning`.
- green CELL 5 `CONTROL an ignored ks256 store is still warned about, exit 0` - the filesystem leg.""",
   measured="the suite at the tip is `3 passed, 2 failed` (CELLS 1 and 2) and with the edited script `5 passed, 0 failed`; real git, bash 3.2",
   prem="At `85cd24d81cb9` `git ls-files --others --exclude-standard=false '*pii*.json'` prints `error: option exclude-standard takes no value` and exits 129 (measured here); a scratch repo with an untracked `pii-data.local.json` printed only the OK line at the tip. The script is run by `run-code-guards.sh:84`."),
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
