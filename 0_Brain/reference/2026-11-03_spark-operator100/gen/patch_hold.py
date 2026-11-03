import re,sys
src=open('/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/hold_ready.py',encoding='utf-8').read()
def sub1(a,b):
    global src
    assert src.count(a)==1,(a,src.count(a)); src=src.replace(a,b)
# 1. ticket id: the doc_only / test_only_input inputs carry ticket={'id':..}
sub1("ticket = inp['ticket']['identifier'] if isinstance(inp.get('ticket'), dict) else str(inp.get('ticket'))",
     "ticket = (inp['ticket'].get('identifier') or inp['ticket'].get('id')) if isinstance(inp.get('ticket'), dict) else str(inp.get('ticket'))  # 2026-11-03 op100: spark tiers carry ticket={'id':..}")
# 2. kind flag + guards
sub1("IS_CODE_PATCH = (not IS_BASH_PATCH) and (not IS_DOC_PATCH) and (not IS_BASH_PATCH2) and (",
     "# 2026-11-03 (operator 100): the Spark tier doc_only (spark/tiers) had NO hold kind - hold_ready crashed on ticket['identifier']. Detected from input.json tier AND round.json tier (must agree).\nIS_DOC_ONLY = (inp.get('tier') == 'doc_only') and (_round_tier() in (None, 'doc_only')) and (not IS_BASH_PATCH) and (not IS_DOC_PATCH)\nIS_CODE_PATCH = (not IS_BASH_PATCH) and (not IS_DOC_PATCH) and (not IS_BASH_PATCH2) and (not IS_DOC_ONLY) and (")
sub1("if model_tag != 'ornith35b-q4' and not (IS_CODE_PATCH or IS_BASH_PATCH or IS_BASH_PATCH2):",
     "if model_tag != 'ornith35b-q4' and not (IS_CODE_PATCH or IS_BASH_PATCH or IS_BASH_PATCH2 or IS_DOC_ONLY):")
sub1("if not IS_BASH_PATCH and not IS_DOC_PATCH and not IS_CODE_PATCH and not IS_BASH_PATCH2 and 'test_file' not in inp:",
     "if not IS_BASH_PATCH and not IS_DOC_PATCH and not IS_CODE_PATCH and not IS_BASH_PATCH2 and not IS_DOC_ONLY and 'test_file' not in inp:")
# 3. the hold function + dispatch
func = r'''
# ================================================================== doc_only (Spark tier, 2026-11-03 operator 100)
# Every clause is copied from the run's own artefacts (checker.out A-legs, round.json, out.md.checker/patch.diff, input.json); the
# expectations are RE-MEASURED here on a scratch copy of the tip files (git apply -p1, strict). Refuses anything not strict.
def hold_doc_only():
    import hashlib, tempfile, shutil
    tip = inp['tip']; decl = list(inp.get('doc_files') or [])
    if not decl: die("doc_only input.json has no doc_files")
    if inp.get('new_doc_files'): die(f"doc_only hold does not handle new_doc_files {inp.get('new_doc_files')}")
    co = _read(os.path.join(run, 'checker.out'), 'checker.out'); co_lines = [l.rstrip() for l in co.splitlines()]
    m = re.search(r'^RESULT: PASS \(tier doc_only\)', co, re.M)
    if not m: die(f"checker.out RESULT is not 'PASS (tier doc_only)': {next((l for l in co_lines if l.startswith('RESULT:')), 'absent')}; FAIL lines: {[l for l in co_lines if l.startswith('FAIL ')][:3]}")
    if any(l.startswith('FAIL ') for l in co_lines): die(f"RESULT says PASS but checker.out carries FAIL line(s): {[l for l in co_lines if l.startswith('FAIL ')][:3]}")
    legs = [l for l in co_lines if l.startswith('PASS A')]
    need = ('A1', 'A2', 'A2a', 'A3', 'A4', 'A3d', 'A5', 'A7', 'A8')
    byleg = {}
    for l in legs: byleg.setdefault(l.split()[1], l)
    miss = [k for k in need if k not in byleg]
    if miss: die(f"checker.out lacks PASS line(s) for {miss}")
    if not byleg['A2'].endswith('(strict)'): die(f"A2 line is not '(strict)': {byleg['A2']}")
    passed = len(legs)
    patch_path = os.path.join(chk, 'patch.diff'); patch_text = _read(patch_path, 'patch.diff')
    patch_sha = hashlib.sha256(open(patch_path, 'rb').read()).hexdigest()[:16]; patch_bytes = os.path.getsize(patch_path)
    out_md = _read(os.path.join(run, 'out.md'), 'out.md')
    blocks = re.findall(r"```diff\n(.*?)\n```", out_md, re.S)
    if len(blocks) != 1: die(f"out.md holds {len(blocks)} ```diff block(s) - contradicts PASS A1")
    if blocks[0].rstrip('\n') + '\n' != patch_text: die("patch.diff is not byte-equal to the out.md fence")
    paths = [p[2:] if p.startswith('b/') else p for p in re.findall(r'^\+\+\+ (\S+)', patch_text, re.M)]
    if sorted(paths) != sorted(decl): die(f"patch.diff's +++ headers {paths} != the declared doc_files {decl}")
    plus = [l[1:] for l in patch_text.splitlines() if l.startswith('+') and not l.startswith('+++')]
    minus = [l[1:] for l in patch_text.splitlines() if l.startswith('-') and not l.startswith('---')]
    nonascii = sum(1 for l in plus for c in l if ord(c) > 127)
    # re-measure the expectations on a scratch copy of the tip files
    files = inp.get('files') or {}
    td = tempfile.mkdtemp(prefix='hold_doc_only_', dir=os.environ.get('CLAUDE_SCRATCHPAD') or None)
    try:
        for p in decl:
            if files.get(p) is None: die(f"input.json files[{p}] is null/missing")
            fp = os.path.join(td, p); os.makedirs(os.path.dirname(fp), exist_ok=True); open(fp, 'w', encoding='utf-8', newline='').write(files[p])
        r = subprocess.run(['git', 'init', '-q', td], capture_output=True, text=True)
        r = subprocess.run(['git', '-C', td, 'apply', '-p1', patch_path], capture_output=True, text=True)
        if r.returncode != 0: die(f"patch.diff does not re-apply strictly to the tip files: {r.stderr.strip()[:200]}")
        after = {p: open(os.path.join(td, p), encoding='utf-8', newline='').read() for p in decl}
    finally:
        shutil.rmtree(td, ignore_errors=True)
    exps = inp.get('expect') or []
    if isinstance(exps, str): die("input.json expect is a string, not a list")
    exp_rows = []
    for e in exps:
        scope = [e['path']] if e.get('path') else decl
        in_before = any(e['text'] in files[p] for p in scope); in_after = any(e['text'] in after[p] for p in scope)
        if e['kind'] == 'absent' and not (in_before and not in_after): die(f"expect_absent {e['text'][:60]!r}: before={in_before} after={in_after} (want True/False)")
        if e['kind'] == 'present' and not (not in_before and in_after): die(f"expect_present {e['text'][:60]!r}: before={in_before} after={in_after} (want False/True)")
        exp_rows.append(f"- expect_{e['kind']} `{e['text']}`" + (f" in `{e['path']}`" if e.get('path') else '') + f" - re-measured on a scratch copy of the tip file(s): before {'present' if in_before else 'absent'}, after {'present' if in_after else 'absent'}")
    rj = json.load(open(os.path.join(run, 'round.json'))) if os.path.exists(os.path.join(run, 'round.json')) else {}
    gverdict = rj.get('golden', 'not recorded')
    golden_clause = f"golden comparison [round.json, verbatim]: {gverdict}"
    if gverdict not in ('BYTE-IDENTICAL', 'TREE-IDENTICAL'): golden_clause += ' - read the diff against the brief before raising'
    now = datetime.datetime.now(); stamp = now.strftime('%H:%M %Y-%m-%d'); day = now.strftime('%Y-%m-%d')
    fname = f"READY_{ticket}-{rowid}_{model_tag}_BRIEFED-DOCONLY-{title}-PASS-{passed}of{passed}_{day}.diff.md"
    out = os.path.join(NIGHT_DIR, fname)
    if os.path.exists(out) and not dry: die(f"READY already exists: {out}")
    brief_clause = f"Brief: `{brief_given}`" if brief_given else 'Brief: not given (--brief)'
    legs_txt = '\n'.join(f"  - `{l}`" for l in legs)
    body = f"""# READY - {ticket}-{rowid} ({model_label}, briefed, doc_only, markdown) - PASS {passed}/{passed} - HELD for QA

> CANONICAL PATCH = `{patch_path}` (from `ls` at {stamp}; sha256[:16] {patch_sha}, {patch_bytes} B; byte-equal to the out.md fence). Checker A2 (verbatim): `{byleg['A2']}`; {golden_clause}.

**Held {stamp} by {seat} after a source read (hold_ready.py, doc_only path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `{chk}`; the expectations were RE-MEASURED here.** Tip `{tip}`. {brief_clause}
- Touched set [patch.diff `+++` headers == input.json doc_files]: {paths}; `+` lines {len(plus)} ({'ASCII' if nonascii == 0 else str(nonascii) + ' NON-ASCII chars'}), `-` lines {len(minus)}.
- Checker legs [checker.out, verbatim]:
{legs_txt}
- RESULT [checker.out]: `RESULT: PASS (tier doc_only)`
- Expectations:
{chr(10).join(exp_rows)}

**PR NOTES for the raise seat:** DOC_ONLY - documentation prose only, zero code bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The model wrote the prose given in the brief; Wednesday read it against the brief before this hold. No markdown link check was run.

```diff
{patch_text.rstrip()}
```
"""
    if dry:
        print(f"DRY-RUN OK -> {fname}\n  {golden_clause}\n  touched={paths} plus={len(plus)} minus={len(minus)} legs={passed} expectations={len(exp_rows)}")
        sys.exit(0)
    open(out, 'w').write(body)
    print(f"HELD -> {out}\n  golden: {gverdict}; touched={paths} plus={len(plus)} minus={len(minus)} legs={passed} expectations={len(exp_rows)}")
    sys.exit(0)

'''
sub1("if IS_BASH_PATCH2: hold_bash_patch2()\n", func+"if IS_DOC_ONLY: hold_doc_only()\n\nif IS_BASH_PATCH2: hold_bash_patch2()\n")
open(sys.argv[1],'w',encoding='utf-8').write(src)
print('ok')
