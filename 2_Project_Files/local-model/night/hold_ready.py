#!/usr/bin/env python3
"""hold_ready.py — Wednesday's source-read + HOLD writer for a PASSING Ornith test_only OR code_patch run.

Built 2026-09-21 04:5x by the 04:3x Wednesday seat, closing the OWED item from ledger 2026-09-21 03:3x:
a READY was written saying "BYTE-IDENTICAL to the golden (cmp)" while the same action's output said
`patch==golden: False` — the sentence was templated from the previous READYs, not from the check.
This script MEASURES first and builds every provenance clause FROM the measurement's boolean; it
REFUSES (rc 2) to write a READY when any load-bearing check fails, and it never emits the
byte-identical clause unless its own `cmp` said so. Read verbs only; writes ONE file under night/.

2026-09-22 03:5x (Wednesday's tooling drafter): the script now also understands a CODE_PATCH run. It died with
`KeyError: 'test_file'` on runs/2026-09-22_ks1265-ornith35b-night (PASS 7/7) because that input has no test_file.
The task type is DETECTED FROM THE RUN'S ARTEFACTS, never guessed: a code_patch input.json has `product_file` +
`suggested_test_file` and no `test_file`; its checker.out starts `mode: code_patch` and carries `PASS A1..A7`
lines; its out.md.checker/ holds sections.json, section_<k>.diff, section_<k>.opts (line 1 = the file the checker
applied, line 2 = its git-apply options — empty means strict), apply_check_strict_<k>.out (non-empty = the strict
apply's ERROR, so the checker passed A2 only with an accommodation and the word 'strict' may not be claimed),
numstat.out, hunk_audit.out, red_first.json, green_after.json, baseline_suite.json, after_suite.json, suite_delta.out.
The code_patch golden comparison is CONTENT, not bytes (the golden differs in `@@` hunk-header context): change
lines, body lines and hunk headers are compared separately and the sentence names each result; then BOTH patches
are applied (`git apply -p1`, strict) to the tip's file content carried in input.json['files'] inside a scratch
tempdir and the resulting files are compared by bytes. Nothing under the run dir is written. The test_only path
below is UNCHANGED (arm: --dry-run output byte-identical before/after, clock line excepted).

Usage: hold_ready.py <run-dir> <golden-run-dir-or-'-'> <ROWID> <short-title-caps> [--seat '<who>'] [--dry-run]
  run-dir     the runner's run directory (holds input.json, out.md.checker/, checker.out)
  golden      the drafter's precheck directory whose out.md.checker/patch.diff is the golden, or '-' (none)
  ROWID       e.g. LIVETENANTDEFAULT-1 (goes into the READY filename)
  title       e.g. LIVE-ROWTOAPIKEY-DEFAULT-TENANT (caps, dashes; goes into the filename)
"""
import json, os, subprocess, sys, datetime, re

def die(msg, rc=2):
    print(f"hold_ready: REFUSE — {msg}", file=sys.stderr); sys.exit(rc)

args = sys.argv[1:]
dry = '--dry-run' in args; args = [a for a in args if a != '--dry-run']
seat = 'Wednesday'
if '--seat' in args:
    i = args.index('--seat'); seat = args[i+1]; del args[i:i+2]
if len(args) != 4: die(f"expected 4 positional args (run-dir golden ROWID title), got {len(args)}: {args}", 1)
run, golden, rowid, title = args
chk = os.path.join(run, 'out.md.checker')
if not os.path.isdir(chk): die(f"no checker dir at {chk}")

inp = json.load(open(os.path.join(run, 'input.json')))
ticket = inp['ticket']['identifier'] if isinstance(inp.get('ticket'), dict) else str(inp.get('ticket'))
NIGHT_DIR = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night'

# ------------------------------------------------------------------ task type, from the run's own input
# test_only inputs carry `test_file` (+ tampers); code_patch inputs carry `product_file` + `suggested_test_file` and
# no `test_file`. Anything else is refused — the READY's sentences would have no artefact to be built from.
IS_CODE_PATCH = ('test_file' not in inp and 'product_file' in inp and 'suggested_test_file' in inp)
if not IS_CODE_PATCH and 'test_file' not in inp:
    die(f"input.json is neither test_only (test_file) nor code_patch (product_file + suggested_test_file): keys {sorted(inp)}")

def _read(path, what):
    """Read an artefact the READY will quote; a missing one is a refusal, never a blank."""
    if not os.path.exists(path): die(f"{what} is missing: {path}")
    return open(path, errors='replace').read()

def _line(text, prefix, what):
    l = next((l.rstrip() for l in text.splitlines() if l.startswith(prefix)), '')
    if not l: die(f"checker.out has no line starting {prefix!r} — {what} cannot be asserted")
    return l

def _split_sections(lines):
    """[(hdr_minus, hdr_plus, [(hunk_header, [body lines])...])] from a unified diff's lines."""
    secs = []; i = 0
    while i < len(lines):
        if lines[i].startswith('--- ') and i + 1 < len(lines) and lines[i+1].startswith('+++ '):
            secs.append((lines[i], lines[i+1], [])); i += 2; continue
        if lines[i].startswith('@@'):
            if not secs: die(f"hunk header before any file header in patch: {lines[i]!r}")
            secs[-1][2].append((lines[i], [])); i += 1; continue
        if secs and secs[-1][2] and lines[i] != '':
            secs[-1][2][-1][1].append(lines[i])
        i += 1
    return secs

def _apply_to_tip(patch_file, files_at_tip, scratch_parent):
    """git apply -p1 (strict) of patch_file onto the tip's file content from input.json['files'], in a tempdir.
    Returns (rc, stderr, {path: sha256 of the file after}). The tempdir is removed afterwards."""
    import tempfile, hashlib, shutil
    td = tempfile.mkdtemp(prefix='hold_ready_apply_', dir=scratch_parent)
    try:
        for path, content in files_at_tip.items():
            fp = os.path.join(td, path); os.makedirs(os.path.dirname(fp), exist_ok=True)
            open(fp, 'w').write(content)
        r = subprocess.run(['git', 'apply', '-p1', patch_file], cwd=td, capture_output=True, text=True)
        digests = {p: hashlib.sha256(open(os.path.join(td, p), 'rb').read()).hexdigest() for p in files_at_tip}
        return r.returncode, r.stderr.strip(), digests
    finally:
        shutil.rmtree(td, ignore_errors=True)

def hold_code_patch():
    tip = inp['tip']; product_file = inp['product_file']; test_file = inp['suggested_test_file']
    runner = (inp.get('repo') or {}).get('test_runner', '').split(' ')[0] or inp.get('runner') or '?'
    co = _read(os.path.join(run, 'checker.out'), 'checker.out')
    if not re.search(r'^mode: code_patch', co, re.M): die("checker.out has no 'mode: code_patch' line — the input says code_patch but the checker did not run it as one")

    # 1. verdict — from checker.out
    m = re.search(r'^RESULT: (PASS|FAIL) \((\d+)/(\d+)\)', co, re.M)
    if not m or m.group(1) != 'PASS':
        fails = [l.strip() for l in co.splitlines() if l.startswith('FAIL ')]
        die(f"checker.out RESULT is not PASS: {m.group(0) if m else next((l for l in co.splitlines() if l.startswith('RESULT:')), 'absent')}; FAIL lines: {fails[:3]}")
    passed, total = m.group(2), m.group(3)
    a_lines = {k: _line(co, f'PASS {k} ', k) for k in ('A1', 'A2', 'A3', 'A3c', 'A4', 'A5', 'A6', 'A7')}
    summary_line = _line(co, 'SUMMARY ', 'SUMMARY')
    a3i_line = next((l.rstrip() for l in co.splitlines() if l.startswith('A3i:')), '')

    # 2. the patch and its sections — every file the READY names must exist
    patch_path = os.path.join(chk, 'patch.diff'); patch_text = _read(patch_path, 'patch.diff')
    sections = json.loads(_read(os.path.join(chk, 'sections.json'), 'sections.json'))
    if not sections: die("sections.json is empty")
    hunk_audit = _read(os.path.join(chk, 'hunk_audit.out'), 'hunk_audit.out').strip().splitlines()
    hunk_audit_line = hunk_audit[0] if hunk_audit else die("hunk_audit.out is empty")
    sec_rows = []; strict_errors = []; any_recount = False
    for s in sections:
        k = s['n']; sf = s['file']
        _read(sf, f'section_{k}.diff')
        opts = _read(os.path.join(chk, f'section_{k}.opts'), f'section_{k}.opts').splitlines()
        applied_file = opts[0].strip() if opts else ''; apply_opts = opts[1].strip() if len(opts) > 1 else ''
        strict_out = _read(os.path.join(chk, f'apply_check_strict_{k}.out'), f'apply_check_strict_{k}.out').strip()
        if strict_out: strict_errors.append((k, s['path'], strict_out.splitlines()[0][:160]))
        if '--recount' in apply_opts or applied_file != sf: any_recount = True
        sec_rows.append((k, s['path'], sf, applied_file, apply_opts, s.get('hunks'), s.get('miscount'), strict_out))
    a2_line = a_lines['A2']
    strict_claimed = ('strict git apply --check' in a2_line and 'accommodation' not in a2_line)
    if (strict_errors or any_recount) and strict_claimed:
        die(f"apply_check_strict_*.out non-empty / opts carry an accommodation ({strict_errors}, recount={any_recount}) but the A2 line claims strict: {a2_line}")
    if strict_claimed and any(r[4] != '' for r in sec_rows): die(f"A2 claims strict but a section's opts are not empty: {[(r[0], r[4]) for r in sec_rows]}")
    strict_ok = strict_claimed and not strict_errors and not any_recount
    cat_ok = (subprocess.run('cat ' + ' '.join("'" + r[2] + "'" for r in sec_rows) + " | cmp -s - '" + patch_path + "'", shell=True).returncode == 0)

    # 3. touched set — numstat.out (the checker's own) must equal the declared {product_file, suggested_test_file}
    numstat = _read(os.path.join(chk, 'numstat.out'), 'numstat.out').strip()
    ns_rows = [l.split('\t') for l in numstat.splitlines() if l.strip()]
    touched = sorted({r[2] for r in ns_rows if len(r) == 3})
    declared = sorted({product_file, test_file})
    if touched != declared: die(f"touched {touched} != declared {declared} (input.json product_file + suggested_test_file)")
    adds = {r[2]: r[0] for r in ns_rows if len(r) == 3}; dels = {r[2]: r[1] for r in ns_rows if len(r) == 3}

    # 4. product hunk '+' lines vs the brief's expected_plus (whitespace-stripped ordered equality; A3i covers bytes)
    exp = (inp.get('defect_line') or {}).get('expected_plus') or inp.get('expected_plus') or []
    if isinstance(exp, str): exp = exp.split('\n')
    prod_sec = next((s for s in sections if s['path'] == product_file or s['path'].endswith('/' + product_file) or product_file.endswith('/' + s['path'])), None)
    if prod_sec is None: die(f"no section in sections.json for the product file {product_file}")
    prod_lines = open(prod_sec['file'], errors='replace').read().split('\n')
    prod_plus = [l[1:] for l in prod_lines if l.startswith('+') and not l.startswith('+++')]
    prod_minus = [l[1:] for l in prod_lines if l.startswith('-') and not l.startswith('---')]
    plus_ok = ([l.strip() for l in prod_plus] == [l.strip() for l in exp if l != '']) if exp else None
    if plus_ok is False: die(f"product hunk '+' lines ({len(prod_plus)}) are not ordered-equal (stripped) to the brief's expected_plus ({len([l for l in exp if l])})")
    nonascii = sum(1 for l in prod_plus for c in l if ord(c) > 127)
    a3i_out = open(os.path.join(chk, 'a3i_indent.out'), errors='replace').read().strip() if os.path.exists(os.path.join(chk, 'a3i_indent.out')) else ''

    # 5. RED-FIRST / GREEN-AFTER — the A4/A5 lines verbatim, cross-checked against the jest json each came from
    rf = json.loads(_read(os.path.join(chk, 'red_first.json'), 'red_first.json'))
    ga = json.loads(_read(os.path.join(chk, 'green_after.json'), 'green_after.json'))
    if rf.get('numFailedTests', 0) < 1 or rf.get('numTotalTests', 0) < 1: die(f"red_first.json is not red: failed={rf.get('numFailedTests')} total={rf.get('numTotalTests')}")
    if ga.get('numFailedTests', 1) != 0 or not ga.get('success') or ga.get('numTotalTests', 0) < 1: die(f"green_after.json is not all-green: failed={ga.get('numFailedTests')} total={ga.get('numTotalTests')} success={ga.get('success')}")
    red_names = [a['fullName'] for t in rf.get('testResults', []) for a in t.get('assertionResults', []) if a.get('status') == 'failed']

    # 6. whole suite — suite_delta.out's own lines, cross-checked against the two jest json files
    bs = json.loads(_read(os.path.join(chk, 'baseline_suite.json'), 'baseline_suite.json'))
    af = json.loads(_read(os.path.join(chk, 'after_suite.json'), 'after_suite.json'))
    sd = _read(os.path.join(chk, 'suite_delta.out'), 'suite_delta.out').strip().splitlines()
    totals_line = next((l for l in sd if l.startswith('baseline: total=')), '')
    newreds_line = next((l for l in sd if l.startswith('NEW reds:')), '')
    if not totals_line or not newreds_line: die(f"suite_delta.out lacks the totals / NEW reds lines: {sd[:3]}")
    mt = re.search(r'baseline: total=(\d+) failed=(\d+) \| after: total=(\d+) failed=(\d+)', totals_line)
    if not mt or (int(mt.group(1)), int(mt.group(2)), int(mt.group(3)), int(mt.group(4))) != (bs['numTotalTests'], bs['numFailedTests'], af['numTotalTests'], af['numFailedTests']):
        die(f"suite_delta.out totals {totals_line!r} disagree with baseline_suite.json/after_suite.json ({bs['numTotalTests']}/{bs['numFailedTests']} vs {af['numTotalTests']}/{af['numFailedTests']})")
    if newreds_line.strip() != 'NEW reds: []': die(f"suite_delta.out reports new reds: {newreds_line}")

    # 7. the golden — CONTENT compared, each measurement its own clause; never a byte-identity claim unless cmp said so
    golden_clause = "golden not located — no identity claim is made"; same_bytes = None; applied_same = None
    if golden != '-':
        gpath = os.path.join(golden, 'out.md.checker', 'patch.diff')
        if not os.path.exists(gpath):
            golden_clause = f"golden path `{gpath}` does not exist — no identity claim is made"
        else:
            same_bytes = (subprocess.run(['cmp', '-s', patch_path, gpath]).returncode == 0)
            if same_bytes:
                golden_clause = f"the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s {patch_path} {gpath}` rc 0, {seat})"
            else:
                rs = _split_sections(patch_text.split('\n')); gs = _split_sections(open(gpath, errors='replace').read().split('\n'))
                parts = [f"CONTENT-compared against the drafter's golden `{gpath}` (bytes DIFFER: `cmp` rc 1)"]
                if [ (a, b) for a, b, _ in rs ] != [ (a, b) for a, b, _ in gs ]:
                    parts.append(f"file headers DIFFER (run {[b for _, b, _ in rs]} vs golden {[b for _, b, _ in gs]})")
                else:
                    ch_same = []; body_same = []; hdr_diff = []
                    for (_, hp, rh), (_, _, gh) in zip(rs, gs):
                        name = hp[4:].split('/')[-1]
                        rchg = [l for _, b in rh for l in b if l[:1] in '+-']; gchg = [l for _, b in gh for l in b if l[:1] in '+-']
                        rbody = [l for _, b in rh for l in b]; gbody = [l for _, b in gh for l in b]
                        ch_same.append((name, rchg == gchg)); body_same.append((name, rbody == gbody, len(rbody), len(gbody)))
                        for (rhh, _), (ghh, _) in zip(rh, gh):
                            if rhh != ghh: hdr_diff.append(f"{name}: golden `{ghh}` vs run `{rhh}`")
                        if len(rh) != len(gh): hdr_diff.append(f"{name}: hunk COUNT differs (run {len(rh)} vs golden {len(gh)})")
                    parts.append("change lines (`+`/`-`, ordered) " + ("IDENTICAL in every file" if all(v for _, v in ch_same) else "DIFFER in " + ', '.join(n for n, v in ch_same if not v)))
                    parts.append("body lines (context included) " + ("identical in every file" if all(v for _, v, _, _ in body_same) else "DIFFER in " + ', '.join(f"{n} (run {rn} vs golden {gn} body lines — context, since the change lines are equal)" if rn != gn else n for n, v, rn, gn in body_same if not v) + (" (identical in " + ', '.join(n for n, v, _, _ in body_same if v) + ")" if any(v for _, v, _, _ in body_same) else "")))
                    parts.append("hunk headers " + ("identical" if not hdr_diff else "differ (" + '; '.join(hdr_diff) + ")"))
                files_at_tip = inp.get('files') or {}
                if all(p in files_at_tip for p in touched):
                    scratch = os.environ.get('CLAUDE_SCRATCHPAD') or None
                    rc_r, err_r, dg_r = _apply_to_tip(patch_path, files_at_tip, scratch)
                    rc_g, err_g, dg_g = _apply_to_tip(gpath, files_at_tip, scratch)
                    if rc_r != 0: die(f"the run's patch does not apply strictly (git apply -p1) to the tip content in input.json['files']: {err_r[:200]}")
                    if rc_g != 0:
                        parts.append(f"APPLIED RESULT not compared: the golden does not apply strictly to the tip content in input.json['files'] ({err_g[:120]})")
                    else:
                        applied_same = all(dg_r[p] == dg_g[p] for p in touched)
                        parts.append(("APPLIED RESULT IDENTICAL: both patches applied strictly (`git apply -p1`, scratch tempdir) to the tip content carried in input.json['files'] yield byte-identical files (" + '/'.join(p.split('/')[-1] for p in touched) + ", sha256 equal)") if applied_same
                                     else "APPLIED RESULT DIFFERS: the two patches yield different files for " + ', '.join(p.split('/')[-1] for p in touched if dg_r[p] != dg_g[p]) + " — read the diff before raising")
                else:
                    parts.append("APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content)")
                golden_clause = '; '.join(parts)

    # 8. the brief — LOCATED on disk, never a path built from the ROWID (the first code_patch READY cited
    #    briefs/KS-1265-EARLYGUARD-R16.md; the file is briefs/KS-1265-R16-EARLYGUARD.md)
    briefs_dir = os.path.join(NIGHT_DIR, 'briefs'); brief_clause = 'brief NOT LOCATED under night/briefs/ (no claim made)'
    cands = [os.path.join(briefs_dir, f) for f in (sorted(os.listdir(briefs_dir)) if os.path.isdir(briefs_dir) else [])
             if f.startswith(ticket + '-') and f.endswith('.md') and all(tok.lower() in f.lower() for tok in rowid.split('-'))]
    if len(cands) == 1: brief_clause = f"Brief (located by ticket + ROWID tokens under night/briefs/): `{cands[0]}`"
    elif cands: brief_clause = f"brief AMBIGUOUS under night/briefs/ ({len(cands)} match the ticket + ROWID tokens): " + ', '.join('`' + c + '`' for c in cands)

    now = datetime.datetime.now()
    stamp = now.strftime('%H:%M %Y-%m-%d'); day = now.strftime('%Y-%m-%d')
    fname = f"READY_{ticket}-{rowid}_ornith35b-q4_BRIEFED-CODEPATCH-{title}-PASS-{passed}of{total}_{day}.diff.md"
    out = os.path.join(NIGHT_DIR, fname)
    if os.path.exists(out) and not dry: die(f"READY already exists: {out}")

    sec_lines = '\n'.join(
        f"- section {k} `{os.path.basename(sf)}` → `{path}` (hunks={hunks}, miscount={mis}; applied file per `section_{k}.opts`: `{os.path.basename(applied)}`, git-apply options: `{opts or '(none — strict)'}`; `apply_check_strict_{k}.out`: {'EMPTY (strict apply --check clean)' if not so else 'NON-EMPTY: `' + so.splitlines()[0][:160] + '`'})"
        for k, path, sf, applied, opts, hunks, mis, so in sec_rows)
    plus_clause = ((f" — product section `+` lines {len(prod_plus)} ordered-equal (whitespace-stripped) to the brief's `expected_plus` "
                    f"({'ASCII' if nonascii == 0 else str(nonascii) + ' NON-ASCII chars'}); `-` lines {len(prod_minus)}") if plus_ok
                   else ' — no expected_plus in the input; not re-measured here')
    apply_steps = '; '.join((f"section {k} `{os.path.basename(applied)}`: `git apply -p1 {opts}`" if opts else f"section {k} `{os.path.basename(applied)}`: `git apply -p1` (strict)")
                            for k, _, _, applied, opts, _, _, _ in sec_rows)
    strict_note = ('' if strict_ok else ' — STRICT APPLY NOT CLAIMED: ' + ('; '.join(f"section {k} ({p}): `{e}`" for k, p, e in strict_errors) or 'the checker applied a rewritten/accommodated section (see section_<k>.opts)') + ' (apply with the options recorded in section_<k>.opts; the raise seat states which)')
    body = f"""# READY — {ticket}-{rowid} (Ornith, briefed, code_patch, {runner}) — PASS {passed}/{total} — HELD for QA

> ⚠ **CANONICAL PATCH = `{patch_path}`** (from `ls` at {stamp}; it is `cat` of the section files in order: {'`cmp` rc 0' if cat_ok else 'NOTE — `cat section_*.diff | cmp patch.diff` rc 1, the sections are the applied units'}: {', '.join('`' + r[2] + '`' for r in sec_rows)}). Checker A2 (verbatim from checker.out): `{a2_line}`{strict_note}; {golden_clause}.

**Held {stamp} by {seat} after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `{chk}`, not typed; the artefact each came from is named in brackets).** Tip `{tip}`.
- Touched-file set [checker.out A3, verbatim]: `{a_lines['A3']}`
- Declared set [input.json product_file + suggested_test_file]: `{product_file}` (product) and `{test_file}` (test) — equal to numstat.out's set ({len(touched)} files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
{numstat}
```
- Product hunk `+` count [checker.out A3c, verbatim]: `{a_lines['A3c']}`{plus_clause}.
{('- Byte-exactness [checker.out A3i, verbatim]: `' + a3i_line + '`' + (' [a3i_indent.out: `' + a3i_out + '`]' if a3i_out else '')) if a3i_line else '- A3i line absent from checker.out (not claimed)'}
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `{hunk_audit_line}`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
{sec_lines}
- RED-FIRST [checker.out A4, verbatim]: `{a_lines['A4']}` [red_first.json: failed={rf['numFailedTests']} of total={rf['numTotalTests']}; red cell(s): {red_names}]
- GREEN-AFTER [checker.out A5, verbatim]: `{a_lines['A5']}` [green_after.json: failed={ga['numFailedTests']} of total={ga['numTotalTests']}, success={ga['success']}]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `{totals_line}` · `{newreds_line}` [baseline_suite.json total={bs['numTotalTests']} failed={bs['numFailedTests']}; after_suite.json total={af['numTotalTests']} failed={af['numFailedTests']}]
- A6 [verbatim]: `{a_lines['A6']}` · A7 [verbatim]: `{a_lines['A7']}`
- SUMMARY [checker.out, verbatim]: `{summary_line}`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `{product_file}` (+{adds.get(product_file, '?')}/-{dels.get(product_file, '?')} per numstat.out) and the test file `{test_file}` (+{adds.get(test_file, '?')}/-{dels.get(test_file, '?')}); two files. Apply PER SECTION with the checker's apply mode — {apply_steps} — at the tip `{tip}` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `{os.path.join(run, 'input.json')}`. {brief_clause}. Verdict source: `{os.path.join(run, 'checker.out')}`.

```diff
{patch_text.rstrip()}
```
"""
    gsum = ('BYTE-IDENTICAL' if same_bytes else ('bytes differ; applied result ' + ('IDENTICAL' if applied_same else ('DIFFERS' if applied_same is False else 'not compared')) if same_bytes is False else 'not compared'))
    if dry:
        print(f"DRY-RUN OK → {fname}\n  golden: {golden_clause}\n  touched={touched} product_plus={len(prod_plus)} product_minus={len(prod_minus)} red={rf['numFailedTests']}/{rf['numTotalTests']} green={ga['numPassedTests']}/{ga['numTotalTests']} suite={bs['numTotalTests']}->{af['numTotalTests']} strict={strict_ok} nonascii={nonascii}\n  header: {body.splitlines()[2]}\n  prnote: {[l for l in body.splitlines() if l.startswith('**PR NOTES')][0][:400]}")
        sys.exit(0)
    open(out, 'w').write(body)
    print(f"HELD → {out}\n  golden: {gsum}; touched={len(touched)} product_plus={len(prod_plus)} product_minus={len(prod_minus)} red={rf['numFailedTests']}/{rf['numTotalTests']} green={ga['numPassedTests']}/{ga['numTotalTests']} suite={bs['numTotalTests']}->{af['numTotalTests']} strict={strict_ok}")
    sys.exit(0)

if IS_CODE_PATCH: hold_code_patch()

# ================================================================== test_only path (unchanged below, 2026-09-21)
tip = inp['tip']; test_file = inp['test_file']; mode = inp.get('test_mode'); runner = inp.get('runner')

# 1. verdict from checker.out (the run's own artefact, never done.md)
co = open(os.path.join(run, 'checker.out'), errors='replace').read()
m = re.search(r'^RESULT: (PASS|FAIL) \((\d+)/(\d+)\)', co, re.M)
if not m or m.group(1) != 'PASS':
    # 2026-09-22 03:5x: name the FAIL (a `RESULT: FAIL (1 failed)` line does not match the PASS regex and used to print 'absent')
    die(f"checker.out RESULT is not PASS: {m.group(0) if m else next((l.strip() for l in co.splitlines() if l.startswith('RESULT:')), 'absent')}; FAIL lines: {[l.strip() for l in co.splitlines() if l.startswith('FAIL ')][:3]}")
passed, total = m.group(2), m.group(3)

# 2. touched files == {test_file}
touched = json.load(open(os.path.join(chk, 'touched.json')))['touched']
if touched != [test_file]: die(f"touched {touched} != [{test_file}]")

# 3. '+' lines of the run's patch, ordered, vs the brief's expected_plus
patch_path = os.path.join(chk, 'patch.diff')
patch = open(patch_path).read().split('\n')
plus = [l[1:] for l in patch if l.startswith('+') and not l.startswith('+++')]
minus = [l[1:] for l in patch if l.startswith('-') and not l.startswith('---')]
exp = inp.get('expected_plus') or []
if isinstance(exp, str): exp = exp.split('\n')
plus_ok = (plus == exp)
if not plus_ok:
    # tolerate the builder storing expected_plus without a trailing empty element
    plus_ok = ([l for l in plus if l != ''] == [l for l in exp if l != ''])
if not plus_ok: die(f"'+' lines ({len(plus)}) are not ordered-equal to expected_plus ({len(exp)})")
nonascii = sum(1 for l in plus for c in l if ord(c) > 127)
must_remove = inp.get('must_remove') or []
minus_ok = (sorted(minus) == sorted(must_remove))
if not minus_ok: die(f"'-' lines {minus} != must_remove {must_remove}")

# 4. strict apply at the tip (T3) from its own artefact
t3 = open(os.path.join(chk, 'apply_strict.out')).read() if os.path.exists(os.path.join(chk, 'apply_strict.out')) else ''
strict_ok = ('PASS T3' in co)
# 2026-09-21 16:5x (ledger 16:14 row): the T3 sentence is COPIED from checker.out, never templated. A non-empty
# apply_strict.out is the strict apply's ERROR (e.g. 'corrupt patch at line 7'); then the checker passed T3 only
# with an accommodation (--recount) and the word 'strict' may not be emitted as a claim.
t3_line = next((l.strip() for l in co.splitlines() if l.strip().startswith(('PASS T3', 'FAIL T3'))), '')
if not t3_line: die("checker.out has no 'PASS T3'/'FAIL T3' line — T3 cannot be asserted")
strict_failed = (t3.strip() != '')
if strict_failed and 'accommodation' not in t3_line: die(f"apply_strict.out is non-empty ({t3.strip()[:80]}) but the T3 line names no accommodation: {t3_line}")
if strict_failed: strict_ok = False

# 5. tampers: red set == declared, controls green — from each verdict file
tampers = []
for f in sorted(os.listdir(chk)):
    if f.startswith('tamper_') and f.endswith('.verdict.out'):
        v = json.load(open(os.path.join(chk, f)))
        tid = f[len('tamper_'):-len('.verdict.out')]
        ok = (sorted(v.get('red', [])) == sorted(v.get('declared', [])) and not v.get('problems') and not v.get('ctrl_bad'))
        if not ok: die(f"tamper {tid}: red {v.get('red')} declared {v.get('declared')} problems {v.get('problems')} ctrl_bad {v.get('ctrl_bad')}")
        tampers.append((tid, v.get('declared', [])))
if not tampers: die("no tamper verdict files")

# 6. green at the tip: cells present
gt = open(os.path.join(chk, 't5.out')).read().strip().split('\n')[0] if os.path.exists(os.path.join(chk, 't5.out')) else ''
mg = re.search(r'total=(\d+) passed=(\d+) failed=(\d+)', gt)
if not mg or mg.group(3) != '0' or mg.group(1) != mg.group(2): die(f"green_tip line not all-green: {gt!r}")
cells_total = mg.group(1)

# 7. the golden comparison — MEASURED, and the sentence is built from the result
golden_clause = "golden not located — no byte-identity claim is made"
same = None
if golden != '-':
    gpath = os.path.join(golden, 'out.md.checker', 'patch.diff')
    if os.path.exists(gpath):
        same = (subprocess.run(['cmp', '-s', patch_path, gpath]).returncode == 0)
        golden_clause = (f"the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s {patch_path} {gpath}` rc 0, {seat})" if same
                         else f"the run's patch DIFFERS from the drafter's golden at `{gpath}` (`cmp` rc 1) — read the diff before raising")
    else:
        golden_clause = f"golden path `{gpath}` does not exist — no byte-identity claim is made"

now = datetime.datetime.now()
stamp = now.strftime('%H:%M %Y-%m-%d'); day = now.strftime('%Y-%m-%d')
num = ticket.split('-')[1]
fname = f"READY_{ticket}-{rowid}_ornith35b-q4_BRIEFED-TESTONLY-{title}-PASS-{passed}of{total}_{day}.diff.md"
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'night', fname) if False else os.path.join('/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night', fname)
if os.path.exists(out) and not dry: die(f"READY already exists: {out}")

tamper_lines = '\n'.join(f"- `{tid}` → red exactly {decl}" for tid, decl in tampers)
body = f"""# READY — {ticket}-{rowid} (Ornith, briefed, test_only, {mode} · {runner}) — PASS {passed}/{total} — HELD for QA

> ⚠ **CANONICAL PATCH = `{patch_path}`** (from `ls` at {stamp}). Checker T3 (verbatim from checker.out): `{t3_line}`{' — STRICT APPLY REFUSED: `' + t3.strip() + '` (apply with --recount or rewrite the header; the raise seat states which)' if strict_failed else ''}; {golden_clause}.

**Held {stamp} by {seat} after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `{chk}`, not typed).** Tip `{tip}`. Touches ONE file: `{test_file}` ({mode}). `+` lines {len(plus)} ordered-equal to the brief's `expected_plus` ({'ASCII' if nonascii == 0 else str(nonascii) + ' NON-ASCII chars'}); `-` lines {len(minus)} == `must_remove`. Green at the tip: {cells_total}/{cells_total} cells. Tampers ({len(tampers)}), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
{tamper_lines}

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` {'WITH --recount (strict apply refuses: miscounted hunk header — every line byte-exact per the T3 line) — or rewrite the header and assert the blob equals the --recount result' if strict_failed else 'strictly'} at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `{os.path.join(run, 'input.json')}`. Brief: `night/briefs/{ticket}-{rowid}.md`. Verdict source: `{os.path.join(run, 'checker.out')}`.

```diff
{open(patch_path).read().rstrip()}
```
"""
if dry:
    print(f"DRY-RUN OK → {fname}\n  golden: {golden_clause}\n  plus={len(plus)} minus={len(minus)} cells={cells_total} tampers={len(tampers)} nonascii={nonascii}\n  header: {body.splitlines()[2]}\n  prnote: {[l for l in body.splitlines() if l.startswith('**PR NOTES')][0][:220]}")
    sys.exit(0)
open(out, 'w').write(body)
print(f"HELD → {out}\n  golden: {'BYTE-IDENTICAL' if same else ('DIFFERS' if same is False else 'not compared')}; plus={len(plus)} minus={len(minus)} cells={cells_total} tampers={len(tampers)}")
