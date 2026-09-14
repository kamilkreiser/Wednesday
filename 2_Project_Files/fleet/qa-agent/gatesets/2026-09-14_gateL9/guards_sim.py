#!/usr/bin/env python3
"""guards_sim.py — the drafter's re-derivation of every prediction in the L9 brief, from the HEAD bytes: extracts the three
checkers' scripts out of the YAML files under model/ (yaml.safe_load — so a `shell:` key that fails to parse is caught
here first), runs each under the shell the workflow names AND under the shell a tamper would name, with stub commands on
PATH (stub npm / stub node / stub npx), and prints observed vs predicted per cell. Every row in the brief's 2a table that
says `predicted-by: drafter` was derived by this script. Nothing here touches the Secuura checkout; /bin/bash is 3.2."""
import os, subprocess, sys, tempfile, yaml, textwrap, hashlib
G = sys.argv[1]
W = tempfile.mkdtemp(prefix='l9sim.', dir=G)
fails = 0
def ck(cond, msg):
    global fails
    print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond: fails += 1
def step(path, job, name_sub):
    d = yaml.safe_load(open(path, encoding='utf-8'))
    steps = d['jobs'][job]['steps']
    s = [x for x in steps if name_sub in x.get('name', '')]
    assert len(s) == 1, (path, name_sub, len(s))
    return s[0], len(d['jobs']), len(steps)
def run(script, shell_argv, stubdir, cwd, extra_env=None):
    sp = os.path.join(W, 'step_%s.sh' % hashlib.sha256((script + str(shell_argv) + stubdir).encode()).hexdigest()[:8])
    open(sp, 'w').write(script)
    env = {'PATH': stubdir + ':/usr/bin:/bin', 'HOME': W}
    if extra_env: env.update(extra_env)
    p = subprocess.run(shell_argv + [sp], cwd=cwd, env=env, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr
def stub(dirname, name, body):
    d = os.path.join(W, dirname); os.makedirs(d, exist_ok=True)
    p = os.path.join(d, name); open(p, 'w').write('#!/bin/bash\n' + body); os.chmod(p, 0o755); return d

print('== YAML parse + job/step census (the parse cell)')
for f, job, sub in [('security-scan.yml.8861e6216', 'dependency-audit', 'Audit-contract'), ('security-scan.yml.1aa708be9', 'dependency-audit', 'Audit-contract'), ('security-scan.yml.d105e07a8', 'dependency-audit', 'Audit-contract'), ('security-scan.yml.940+941', 'dependency-audit', 'Audit-contract'), ('pr-security-gates.yml.8861e6216', 'code-security-gates', 'All shell test suites'), ('pr-security-gates.yml.53b9c3cc1', 'code-security-gates', 'All shell test suites')]:
    s, nj, ns = step(f'{G}/model/{f}', job, sub)
    print(f'   {f}: jobs={nj} steps[{job}]={ns} shell={s.get("shell")!r} step={s["name"][:40]!r}')

print('== #940: the audit-contract step script, byte-identical develop vs head? (only shell: differs)')
s_dev, _, _ = step(f'{G}/model/security-scan.yml.8861e6216', 'dependency-audit', 'Audit-contract')
s_940, _, _ = step(f'{G}/model/security-scan.yml.1aa708be9', 'dependency-audit', 'Audit-contract')
s_941, _, _ = step(f'{G}/model/security-scan.yml.d105e07a8', 'dependency-audit', 'Audit-contract')
s_both, _, _ = step(f'{G}/model/security-scan.yml.940+941', 'dependency-audit', 'Audit-contract')
ck(s_dev['run'] == s_940['run'] == s_941['run'] == s_both['run'], 'the `run:` block of the audit-contract step is byte-identical at develop, #940, #941 and the #940x#941 merge (only `shell:` differs)')
ck(s_dev.get('shell') is None and s_940.get('shell') == 'bash {0}' and s_941.get('shell') is None and s_both.get('shell') == 'bash {0}', 'shell: develop=None (GitHub default `bash -e {0}`), #940=`bash {0}`, #941=None (the head does NOT carry #940\'s line), #940x#941 merged=`bash {0}`')
ck(s_940['working-directory'] == 'Blockchain/Dev', 'working-directory Blockchain/Dev')
# the four cases, under the default shell (-e) and the PR's shell (no -e), with a stub npm
cwd = os.path.join(W, 'wd'); os.makedirs(os.path.join(cwd, 'scripts', 'audit'), exist_ok=True)
open(os.path.join(cwd, 'scripts', 'audit', 'expected-case-count'), 'w').write('59\n')
RED = stub('npm_red', 'npm', 'printf "%s\\n" "✖ audit-locks: an unreadable BOUND is refused (3)" "ℹ tests 59" "ℹ pass 52" "ℹ fail 7"; exit 1\n')
GREEN = stub('npm_green', 'npm', 'printf "%s\\n" "ℹ tests 59" "ℹ pass 59" "ℹ fail 0"; exit 0\n')
FEWER = stub('npm_fewer', 'npm', 'printf "%s\\n" "ℹ tests 40" "ℹ pass 40" "ℹ fail 0"; exit 0\n')
SILENT = stub('npm_silent', 'npm', 'exit 0\n')
DEFAULT = ['/bin/bash', '-e']; PR = ['/bin/bash']
print('== #940 CASE table (stub npm; the step\'s own `run:` bytes from the head file)')
rc, out, err = run(s_940['run'], DEFAULT, RED, cwd); ck(rc == 1 and out.strip() == '' , f'CASE A under the DEFAULT shell (bash -e): suites red -> exit {rc}, stdout {len(out.splitlines())} lines (the swallow: nothing printed)')
rc, out, err = run(s_940['run'], PR, RED, cwd); ck(rc == 1 and out.splitlines()[-1] == 'audit-contract suites are red' and 'ℹ fail 7' in out, f'CASE A under the PR shell (bash {{0}}): suites red -> exit {rc}, {len(out.splitlines())} lines, last = {out.splitlines()[-1]!r} (the reason printed)')
for sh, lab in [(DEFAULT, 'bash -e'), (PR, 'bash {0}')]:
    rc, out, err = run(s_940['run'], sh, GREEN, cwd); ck(rc == 0 and out.splitlines()[-1] == 'OK — 59 audit-contract cases pass (expected 59)', f'CASE B ({lab}): green 59 -> exit {rc}, last {out.splitlines()[-1]!r}')
    rc, out, err = run(s_940['run'], sh, FEWER, cwd); ck(rc == 1 and 'ran 40 cases, expected 59' in out, f'CASE C ({lab}): 40 cases -> exit {rc}, the count line printed')
    rc, out, err = run(s_940['run'], sh, SILENT, cwd)
    if sh is DEFAULT: ck(rc == 1 and out.strip() == '', f'CASE D ({lab}): silent exit-0 npm -> exit {rc}, {len(out.splitlines())} lines — a SECOND swallow: `cases=$(… | grep …)` is a failing pipeline under pipefail, so -e aborts before "no case count reported" can print (drafter finding — the PR body names only CASE A)')
    else: ck(rc == 1 and 'no case count reported' in out, f'CASE D ({lab}): silent exit-0 npm -> exit {rc}, "no case count reported" printed')
# a wrong shell: line = the through-code red: `shell: bash` (GitHub: bash --noprofile --norc -eo pipefail {0}) swallows again
rc, out, err = run(s_940['run'], ['/bin/bash', '--noprofile', '--norc', '-eo', 'pipefail'], RED, cwd); ck(rc == 1 and out.strip() == '', f'TAMPER T-940a `shell: bash` (= bash -eo pipefail): CASE A prints nothing again -> exit {rc}, 0 lines (the behaviour cell REDS)')
# the YAML tamper: a mis-indented shell: line -> the parse cell
txt = open(f'{G}/model/security-scan.yml.1aa708be9', encoding='utf-8').read()
assert txt.count('        shell: bash {0}\n') == 1
bad = txt.replace('        shell: bash {0}\n', '      shell: bash {0}\n')
try:
    d = yaml.safe_load(bad); ok = False; print('   parse of the mis-indented file:', 'parsed?!', type(d))
except Exception as e:
    ok = True; print('   parse of the mis-indented file raises:', type(e).__name__)
ck(ok, 'TAMPER T-940b `shell:` mis-indented by 2 -> yaml.safe_load raises (the parse cell REDS)')
bad2 = txt.replace('        shell: bash {0}\n', '        shell: bash {0}\n        shell: bash {0}\n')
try:
    d = yaml.safe_load(bad2); dup_ok = False
    st = [x for x in d['jobs']['dependency-audit']['steps'] if 'Audit-contract' in x.get('name', '')][0]
    print('   duplicate key: PyYAML silently keeps the last (', st.get('shell'), ') — say so: a duplicate-key tamper is NOT caught by yaml.safe_load; the GitHub runner rejects it at workflow validation')
except Exception as e:
    dup_ok = True; print('   duplicate key raises:', type(e).__name__)
print('   (T-940c duplicate `shell:` key: not a parse red under PyYAML — record, do not score)')
# the deletion tamper: shell: line removed -> the file == develop's? (byte compare after removing the 18 comment lines too is out of scope; the key is gone)
gone = txt.replace('        shell: bash {0}\n', '')
d = yaml.safe_load(gone); ck(step_ := [x for x in d['jobs']['dependency-audit']['steps'] if 'Audit-contract' in x['name']][0].get('shell') is None, 'TAMPER T-940d `shell:` line deleted -> the step has no shell key (parses; the BEHAVIOUR cell reds by CASE A under the default shell)')

print('== #941: the SCA step script — the exit-code table with a stub node, under bash {0} and under the -e tamper')
sca, _, _ = step(f'{G}/model/security-scan.yml.d105e07a8', 'dependency-audit', 'SCA gate')
sca_dev, _, _ = step(f'{G}/model/security-scan.yml.8861e6216', 'dependency-audit', 'SCA gate')
ck(sca['name'] == 'SCA gate — npm audit vs the triaged baseline (warn-first)' and sca_dev['name'] == 'SCA gate — npm audit vs allow-list (warn-first)', 'step renamed: allow-list -> the triaged baseline')
ck(sca.get('continue-on-error') == "${{ github.event_name == 'pull_request' }}" and sca_dev.get('continue-on-error') == sca.get('continue-on-error'), 'continue-on-error kept: ${{ github.event_name == \'pull_request\' }} (warn-first on PRs, blocking on push)')
ck(sca.get('shell') == 'bash {0}' and 'node scripts/audit/audit-gate.mjs' in sca['run'] and sca_dev['run'].strip() == 'node scripts/check-npm-audit.mjs npm-audit.json .security/exceptions.yml', 'SCA run: develop = check-npm-audit.mjs vs exceptions.yml (one line); head = audit-gate.mjs + the case table under shell bash {0}')
expect = {0: (0, 'OK — no advisories outside the triaged baseline'), 1: (1, 'FAIL — new or lapsed advisories; triage them (fix, or a reasoned baseline entry with a ticket)'), 2: (0, 'SKIP (advisory) — npm audit could not run (offline / registry unreachable)'), 3: (1, 'FAIL — the audit gate REFUSED to report a verdict (see its line above)'), 7: (1, 'FAIL — new or lapsed advisories; triage them (fix, or a reasoned baseline entry with a ticket)')}
for code, (erc, eline) in expect.items():
    N = stub(f'node_{code}', 'node', f'echo "audit-gate: stub exit {code}"; exit {code}\n')
    rc, out, err = run(sca['run'], PR, N, cwd); ck(rc == erc and out.splitlines()[-1] == eline, f'SCA table under bash {{0}}: gate exit {code} -> step exit {rc}, last line {out.splitlines()[-1]!r}')
    rc, out, err = run(sca['run'], DEFAULT, N, cwd)
    if code == 0: ck(rc == 0, f'   the -e tamper, gate exit 0 -> step exit {rc} (same)')
    else: ck(rc == code and (out.splitlines()[-1] if out.strip() else '') != eline, f'   TAMPER T-941a `shell:` removed (bash -e): gate exit {code} -> step aborts at the node line with exit {rc}, NO case-table line (exit 2 becomes a FAILURE instead of SKIP; exit 3 loses its REFUSED message)')

print('== #942: the probe guard clause on the MERGED bytes (:66-67), three stub arms + the T1 (2>&1) tamper, run from a scratch dir')
sh = open(f'{G}/model/manifest_quarantine.test.sh.53b9c3cc1', encoding='utf-8').read()
L = sh.splitlines()
ck(L[65].startswith('if ! probe="$(cd "$FIXTURES" && env -u SECUURA_STACK_SLOT -u STACK_SLOT -u SECUURA_ARTIFACT_SUFFIX npx tsx ') and L[65].endswith('2>"$TMP/probe.err")" \\') and L[66] == '   || [ "$probe" != "NULL" ]; then', 'merged :66-67 = develop\'s env -u prefix + this PR\'s 2>"$TMP/probe.err" redirect + the != "NULL" disjunct')
live = [i + 1 for i, l in enumerate(L) if '2>&1' in l and not l.lstrip().startswith('#')]
ck(live == [], f'live 2>&1 outside comments in the merged suite: {live} (total mentions incl. comments: {sum(1 for l in L if "2>&1" in l)})')
guard = '\n'.join(L[65:72]) + '\n'
guard_t1 = guard.replace('2>"$TMP/probe.err")"', '2>&1)"')
assert guard.count('2>"$TMP/probe.err")"') == 1
guard_t2 = guard.replace(' \\\n   || [ "$probe" != "NULL" ]; then', '; then')
assert guard_t2 != guard
fx = os.path.join(W, 'fixtures'); os.makedirs(fx, exist_ok=True)
pre = 'set -u\nFIXTURES="%s"\nTMP="%s"\n' % (fx, W)
post = 'echo GUARD-PASSED\n'
ARM1 = stub('npx_arm1', 'npx', 'echo "npm warn exec The following package was not found and will be installed: tsx@4.23.13" >&2\nprintf NULL\nexit 0\n')
ARM2A = stub('npx_arm2a', 'npx', 'echo "npx: launch failure (stub)" >&2\nprintf NULL\nexit 7\n')
ARM2B = stub('npx_arm2b', 'npx', 'printf not-the-answer\nexit 0\n')
for lab, g in [('merged', guard), ('T1 2>&1 restored', guard_t1), ('T2 disjunct dropped', guard_t2)]:
    for arm, S, want_pass in [('arm1 stderr noise + NULL', ARM1, True), ('arm2a npx non-zero', ARM2A, False), ('arm2b wrong stdout', ARM2B, False)]:
        if lab.startswith('T1') and arm.startswith('arm1'): want_pass = False   # the defect: noise folds into the value
        if lab.startswith('T2') and arm.startswith('arm2b'): want_pass = True    # the guard loosened: wrong stdout passes
        rc, out, err = run(pre + g + post, ['/bin/bash'], S, W)
        passed = 'GUARD-PASSED' in out
        ck(passed == want_pass, f'{lab:20} {arm:26} -> {"guard passed" if passed else "FAIL harness (rc " + str(rc) + ")"}; predicted {"pass" if want_pass else "fire"}' + ('' if passed else ' | ' + ' / '.join(l.strip() for l in out.splitlines()[1:3])))
print('== the pin step')
pin, nj, ns = step(f'{G}/model/pr-security-gates.yml.53b9c3cc1', 'code-security-gates', 'Pin tsx')
ck(pin['run'] == 'npm install --global --no-audit --no-fund tsx@4.23.12' and nj == 1, f'pin step run = {pin["run"]!r}; jobs={nj}; steps={ns} (develop: {step(f"{G}/model/pr-security-gates.yml.8861e6216", "code-security-gates", "All shell")[2]})')
steps = yaml.safe_load(open(f'{G}/model/pr-security-gates.yml.53b9c3cc1'))['jobs']['code-security-gates']['steps']
names = [s.get('name', '') for s in steps]
ck(names.index('Pin tsx for the shell suites (KS-1078 — no registry fetch mid-test)') + 1 == names.index('All shell test suites (KS-666 / KS-731 — globbed, not listed)'), 'the pin step is the step immediately BEFORE the shell suites')
print('work dir (kept):', W)
print('FAILS=%d' % fails)
sys.exit(1 if fails else 0)
