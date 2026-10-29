# operator-14 mutant measurement in the private clone: apply golden, plant ONE mutant, run the test file, restore by content. usage: mut14.py
import subprocess, os, re, sys, json
C = os.environ.get('MUT_CLONE') or '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/7fe6fe98-e251-41b8-83ea-c831f0aa2549/scratchpad/op14/src'
B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
def run(svc, runner, tf):
    if runner == 'vitest':
        cmd = ['npx', 'vitest', 'run', tf, '--reporter=json']
    else:
        cmd = ['npx', 'jest', tf, '--json']
    p = subprocess.run(cmd, cwd=f'{C}/Blockchain/Dev/services/{svc}', capture_output=True, text=True, timeout=900)
    out = p.stdout
    try:
        j = json.loads(out[out.index('{'):out.rindex('}') + 1])
    except Exception as e:
        return dict(err=str(e), tail=(p.stdout + p.stderr)[-600:])
    failed = []
    for f in j['testResults']:
        for a in f.get('assertionResults', f.get('tests', [])):
            if a['status'] == 'failed': failed.append(a['title'] if 'title' in a else a['fullName'])
    return dict(total=j['numTotalTests'], failed=len(failed), names=failed, rc=p.returncode)
SPEC = {'ks_1830_p2_charclass_sweep': 'spec1830b', 'ks_1815_p3_trailing_comment': 'spec1815b', 'ks_1816_p1_message_less': 'spec1816b'}
def _edits(brief):
    import importlib.util
    sp = importlib.util.spec_from_file_location('s', os.path.join(os.path.dirname(os.path.abspath(__file__)), SPEC[brief] + '.py')); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    e = m.T['edit']; return m.T['test'], ([e] if isinstance(e, tuple) else e)
def apply(brief):
    # apply the golden by its source edits (the golden's hunks are trimmed of trailing context, which patch(1)/git apply read as end-of-file anchors)
    t, es = _edits(brief); fp = f'{C}/{t}'; s = open(fp, encoding='utf-8').read()
    for o, n in es:
        assert s.count(o) == 1; s = s.replace(o, n)
    open(fp, 'w', encoding='utf-8').write(s)
def revert(brief):
    subprocess.run(['git', '-C', C, 'checkout', '--', _edits(brief)[0]], check=True)
def mutate(path, old, new, fn):
    fp = f'{C}/{path}'; orig = open(fp, encoding='utf-8').read()
    assert orig.count(old) == 1, (path, old)
    open(fp, 'w', encoding='utf-8').write(orig.replace(old, new))
    try: return fn()
    finally:
        open(fp, 'w', encoding='utf-8').write(orig)
        assert open(fp, encoding='utf-8').read() == orig
which = sys.argv[1]
res = {}
if which == '1830':
    P = 'Blockchain/Dev/services/anchoring/src/anchorSchema.ts'
    TF = 'src/__tests__/ks1175-identity-anchoring.test.ts'
    old = '[A-Za-z0-9._:%-]+$/'
    f = lambda: run('anchoring', 'vitest', TF)
    res['baseline_before_golden'] = f()
    apply('ks_1830_p2_charclass_sweep')
    res['baseline_golden'] = f()
    for name, new in [('bang', '[A-Za-z0-9._:%!-]+$/'), ('star', '[A-Za-z0-9._:%*-]+$/'), ('at', '[A-Za-z0-9._:%@-]+$/'), ('hash', '[A-Za-z0-9._:%#-]+$/'),
                      ('A-z', '[A-z0-9._:%-]+$/'), ('endplus', '[A-Za-z0-9._:%-]+\\+?$/'), ('combined', '[A-z0-9._:%!*@#-]+\\+?$/'),
                      ('ctrl_plus_class', '[A-Za-z0-9._:%+-]+$/'), ('ctrl_slash_class', '[A-Za-z0-9._:%/-]+$/')]:
        res['mut_' + name] = mutate(P, old, new, f)
    revert('ks_1830_p2_charclass_sweep')
elif which == '1815':
    P = 'Blockchain/Dev/services/anchoring/src/index.ts'
    TF = 'src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts'
    L = '    ...anchorSignatureHashView((anchor.metadataPayload as any)?.secuura),'
    f = lambda: run('anchoring', 'vitest', TF)
    res['baseline_before_golden'] = f()
    res['X16c_before_golden'] = mutate(P, L, '    ...{}, // ...anchorSignatureHashView((anchor.metadataPayload as any)?.secuura),', f)
    apply('ks_1815_p3_trailing_comment')
    res['baseline_golden'] = f()
    for name, new in [('X16c', '    ...{}, // ...anchorSignatureHashView((anchor.metadataPayload as any)?.secuura),'), ('X16_wholeline', '    // ...anchorSignatureHashView((anchor.metadataPayload as any)?.secuura),'),
                      ('X16b_block', '    /* ...anchorSignatureHashView((anchor.metadataPayload as any)?.secuura), */'), ('X15_removed', '')]:
        res['mut_' + name] = mutate(P, L, new, f)
    revert('ks_1815_p3_trailing_comment')
elif which == '1816':
    P = 'Blockchain/Dev/services/originate/src/routes/adminConfig.ts'
    TF = 'src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts'
    L = '    return err?.message;'
    f = lambda: run('originate', 'jest', TF)
    res['baseline_before_golden'] = f()
    apply('ks_1816_p1_message_less')
    res['baseline_golden'] = f()
    for name, new in [('Y7_String', '    return String(err?.message);'), ('Y10_String_err', '    return err?.message ?? String(err);'), ('X3_catch_undefined_ctrl', '    return err?.message;')]:
        if name == 'X3_catch_undefined_ctrl':
            res['mut_' + name] = mutate(P, "    return 'thrown value that could not be described';", '    return undefined;', f)
        else: res['mut_' + name] = mutate(P, L, new, f)
    revert('ks_1816_p1_message_less')
print(json.dumps(res, indent=1))
