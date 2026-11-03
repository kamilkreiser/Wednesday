import sys
SRC='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/hold_ready.py'
DST=sys.argv[1]
src=open(SRC,encoding='utf-8').read()
def sub1(a,b):
    global src
    assert src.count(a)==1,(a,src.count(a)); src=src.replace(a,b)
sub1("IS_CODE_PATCH = (not IS_BASH_PATCH) and (not IS_DOC_PATCH) and (not IS_BASH_PATCH2) and (not IS_DOC_ONLY) and (",
 "# 2026-11-04 (operator 101): the Spark tier test_only_input (spark/tiers) had NO hold kind. Detected from input.json tier AND round.json tier (must agree).\nIS_TEST_ONLY_INPUT = (inp.get('tier') == 'test_only_input') and (_round_tier() in (None, 'test_only_input')) and (not IS_BASH_PATCH) and (not IS_DOC_PATCH)\nIS_CODE_PATCH = (not IS_BASH_PATCH) and (not IS_DOC_PATCH) and (not IS_BASH_PATCH2) and (not IS_DOC_ONLY) and (not IS_TEST_ONLY_INPUT) and (")
sub1("if brief_given is not None and not (IS_CODE_PATCH or IS_BASH_PATCH2 or IS_DOC_ONLY):","if brief_given is not None and not (IS_CODE_PATCH or IS_BASH_PATCH2 or IS_DOC_ONLY or IS_TEST_ONLY_INPUT):")
sub1("if model_tag != 'ornith35b-q4' and not (IS_CODE_PATCH or IS_BASH_PATCH or IS_BASH_PATCH2 or IS_DOC_ONLY):","if model_tag != 'ornith35b-q4' and not (IS_CODE_PATCH or IS_BASH_PATCH or IS_BASH_PATCH2 or IS_DOC_ONLY or IS_TEST_ONLY_INPUT):")
sub1("and not IS_BASH_PATCH2 and not IS_DOC_ONLY and 'test_file' not in inp:","and not IS_BASH_PATCH2 and not IS_DOC_ONLY and not IS_TEST_ONLY_INPUT and 'test_file' not in inp:")
func = r'''
# ================================================================== test_only_input (Spark tier, 2026-11-04 operator 101)
# Hardening tier: the product is already correct; the diff adds/strengthens test cells only; the brief's PLANT (a mutation applied in the
# checker's clone only) proves each red cell fails by assertion. Every clause is copied from checker.out; product bytes are asserted
# UNCHANGED here by applying patch.diff to a scratch index of the tip and comparing the product blobs before/after. Non-strict REFUSES.
def hold_test_only_input():
    import hashlib, tempfile, shutil
    tip = inp['tip']; tests = list(inp.get('test_files') or []); prods = list(inp.get('product_files') or [])
    if not tests: die("test_only_input input.json has no test_files")
    if not prods: die("test_only_input input.json has no product_files")
    co = _read(os.path.join(run, 'checker.out'), 'checker.out'); co_lines = [l.rstrip() for l in co.splitlines()]
    if not re.search(r'^RESULT: PASS \(', co, re.M): die(f"checker.out RESULT is not PASS: {next((l for l in co_lines if l.startswith('RESULT:')), 'absent')}; FAIL lines: {[l for l in co_lines if l.startswith('FAIL ')][:3]}")
    if any(l.startswith('FAIL ') for l in co_lines): die(f"RESULT says PASS but checker.out carries FAIL line(s): {[l for l in co_lines if l.startswith('FAIL ')][:3]}")
    if not co_lines or not co_lines[0].startswith('mode: test_only_input'): die(f"checker.out first line is not 'mode: test_only_input': {co_lines[:1]}")
    legs = [l for l in co_lines if l.startswith('PASS A')]
    need = ('A1', 'A2', 'A2a', 'A3', 'A3p', 'A4', 'A5', 'A6', 'A7')
    byleg = {}
    for l in legs: byleg.setdefault(l.split()[1], l)
    miss = [k for k in need if k not in byleg]
    if miss: die(f"checker.out lacks PASS line(s) for {miss}")
    if '--recount' in byleg['A2'] or 'accommodation' in byleg['A2'].lower() or 'not strict' in byleg['A2'].lower(): die(f"A2 line is not strict: {byleg['A2']}")
    if os.path.exists(os.path.join(chk, 'apply_strict.out')) and open(os.path.join(chk, 'apply_strict.out')).read().strip(): die("apply_strict.out is non-empty - the checker passed A2 only with an accommodation")
    passed = len(legs)
    patch_path = os.path.join(chk, 'patch.diff'); patch_text = _read(patch_path, 'patch.diff')
    patch_sha = hashlib.sha256(open(patch_path, 'rb').read()).hexdigest()[:16]; patch_bytes = os.path.getsize(patch_path)
    out_md = _read(os.path.join(run, 'out.md'), 'out.md')
    blocks = re.findall(r"```diff\n(.*?)\n```", out_md, re.S)
    if len(blocks) != 1: die(f"out.md holds {len(blocks)} ```diff block(s) - contradicts PASS A1")
    if blocks[0].rstrip('\n') + '\n' != patch_text: die("patch.diff is not byte-equal to the out.md fence")
    paths = [p[2:] if p.startswith('b/') else p for p in re.findall(r'^\+\+\+ (\S+)', patch_text, re.M)]
    apaths = [p[2:] if p.startswith('a/') else p for p in re.findall(r'^--- (\S+)', patch_text, re.M) if p != '/dev/null']
    plant_files = set(g.get('file') for g in (inp.get('plant') or []))
    if inp.get('plant_diff'): plant_files |= set(p[2:] if p.startswith('b/') else p for p in re.findall(r'^\+\+\+ (\S+)', inp['plant_diff'], re.M))
    if sorted(set(paths)) != sorted(tests): die(f"patch.diff's +++ headers {paths} != the declared test_files {tests}")
    for p in paths + apaths:
        if p in prods: die(f"PRODUCT HUNK: patch.diff names the product {p} - test_only_input must leave product bytes unchanged")
        if p in plant_files: die(f"patch.diff names the plant file {p}")
    # product sha asserted unchanged: scratch index of the tip, blob of each product before and after a STRICT cached apply
    cands = [c for c in (inp.get('source_checkout'), '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src') if c and os.path.isdir(c)]
    repo = next((c for c in cands if subprocess.run(['git', '-C', c, 'cat-file', '-e', tip + '^{commit}'], capture_output=True).returncode == 0), None)
    if repo is None: die(f"tip {tip} is in none of {cands} - cannot assert product bytes")
    td = tempfile.mkdtemp(prefix='hold_toi_', dir=os.environ.get('CLAUDE_SCRATCHPAD') or None)
    try:
        env = dict(os.environ, GIT_INDEX_FILE=os.path.join(td, 'index'))
        r = subprocess.run(['git', '-C', repo, 'read-tree', tip], capture_output=True, text=True, env=env)
        if r.returncode != 0: die(f"read-tree {tip} failed: {r.stderr.strip()[:200]}")
        def blobs(ps):
            out = {}
            for p in ps:
                r = subprocess.run(['git', '-C', repo, 'ls-files', '-s', '--', p], capture_output=True, text=True, env=env)
                out[p] = r.stdout.split()[1] if r.stdout.split() else None
            return out
        b0 = blobs(prods + sorted(plant_files)); t0 = blobs(tests)
        r = subprocess.run(['git', '-C', repo, 'apply', '--cached', '-p1', patch_path], capture_output=True, text=True, env=env)
        if r.returncode != 0: die(f"STRICT `git apply --cached -p1` of patch.diff at tip {tip[:12]} failed: {r.stderr.strip()[:200]}")
        b1 = blobs(prods + sorted(plant_files)); t1 = blobs(tests)
    finally:
        shutil.rmtree(td, ignore_errors=True)
    for p in b0:
        if b0[p] is None: die(f"product/plant file {p} is not in the tip index")
        if b0[p] != b1[p]: die(f"PRODUCT BYTES CHANGED: {p} blob {b0[p][:12]} -> {b1[p][:12]}")
    if all(t0[p] == t1[p] for p in tests): die("the patch changes no declared test file blob")
    plus = [l[1:] for l in patch_text.splitlines() if l.startswith('+') and not l.startswith('+++')]
    minus = [l[1:] for l in patch_text.splitlines() if l.startswith('-') and not l.startswith('---')]
    nonascii = sum(1 for l in plus for c in l if ord(c) > 127)
    cells = list(inp.get('red_cells') or [])
    if not cells: die("input.json has no red_cells")
    rj = json.load(open(os.path.join(run, 'round.json'))) if os.path.exists(os.path.join(run, 'round.json')) else {}
    gverdict = rj.get('golden', 'not recorded')
    golden_clause = f"golden comparison [round.json, verbatim]: {gverdict}"
    if gverdict not in ('BYTE-IDENTICAL', 'TREE-IDENTICAL'): golden_clause += ' - read the diff against the brief before raising'
    now = datetime.datetime.now(); stamp = now.strftime('%H:%M %Y-%m-%d'); day = now.strftime('%Y-%m-%d')
    fname = f"READY_{ticket}-{rowid}_{model_tag}_BRIEFED-TESTONLYINPUT-{title}-PASS-{passed}of{passed}_{day}.diff.md"
    out = os.path.join(NIGHT_DIR, fname)
    if os.path.exists(out) and not dry: die(f"READY already exists: {out}")
    brief_clause = f"Brief: `{brief_given}`" if brief_given else 'Brief: not given (--brief)'
    legs_txt = '\n'.join(f"  - `{l}`" for l in legs)
    prod_txt = ', '.join(f"`{p}` blob {b0[p][:12]}" for p in prods)
    cells_txt = '\n'.join(f"  - `{c}`" for c in cells)
    body = f"""# READY - {ticket}-{rowid} ({model_label}, briefed, test_only_input) - PASS {passed}/{passed} - HELD for QA

> CANONICAL PATCH = `{patch_path}` (from `ls` at {stamp}; sha256[:16] {patch_sha}, {patch_bytes} B; byte-equal to the out.md fence). Checker A2 (verbatim): `{byleg['A2']}`; {golden_clause}.

**Held {stamp} by {seat} after a source read (hold_ready.py, test_only_input path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `{chk}`; product bytes were RE-MEASURED here.** Tip `{tip}`. {brief_clause}
- Touched set [patch.diff `+++` headers == input.json test_files, no product or plant file named]: {paths}; `+` lines {len(plus)} ({'ASCII' if nonascii == 0 else str(nonascii) + ' NON-ASCII chars'}), `-` lines {len(minus)}.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: {prod_txt}{'; plant file(s) also unchanged' if plant_files else ''}.
- Red cells [input.json]:
{cells_txt}
- Red-first evidence [checker.out, verbatim]: A4 green without plant, A5 red under the plant by assertion.
- Checker legs [checker.out, verbatim]:
{legs_txt}
- RESULT [checker.out]: `{next(l for l in co_lines if l.startswith('RESULT:'))}`

**PR NOTES for the raise seat:** TEST_ONLY_INPUT - test bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief's plant (checker clone only), not a change in the PR. No `tsc` leg covers a vitest file; DOES NOT PROVE the plant is the regression that matters or that a cell catches a different one. Wednesday read the cells against the brief before this hold.

```diff
{patch_text.rstrip()}
```
"""
    if dry:
        print(f"DRY-RUN OK -> {fname}\n  {golden_clause}\n  touched={paths} plus={len(plus)} minus={len(minus)} legs={passed} red_cells={len(cells)} products_unchanged={len(prods)}")
        sys.exit(0)
    open(out, 'w').write(body)
    print(f"HELD -> {out}\n  golden: {gverdict}; touched={paths} plus={len(plus)} minus={len(minus)} legs={passed} red_cells={len(cells)} products_unchanged={len(prods)}")
    sys.exit(0)

if IS_TEST_ONLY_INPUT: hold_test_only_input()
'''
sub1("if IS_DOC_ONLY: hold_doc_only()\n", "if IS_DOC_ONLY: hold_doc_only()\n"+func)
open(DST,'w',encoding='utf-8').write(src)
