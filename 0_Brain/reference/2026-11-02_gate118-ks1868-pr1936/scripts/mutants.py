import hashlib, json, subprocess, re
G = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate118-ks1868-pr1936'
S = G + '/repo/Blockchain/Dev/services/originate/src'
T = [S + '/__tests__/ks1868-signatories-nominate-catch-o77p2-unreadable-throw.test.ts',
     S + '/__tests__/ks1868-third-party-verifiers-register-approve-catches-o77p3-unreadable-throw.test.ts']
SITES = {'S1_nominate': (S + '/routes/signatories.ts', 'Failed to nominate signatory'),
         'S2_register': (S + '/routes/thirdPartyVerifiers.ts', 'Failed to register verifier'),
         'S3_approve': (S + '/routes/thirdPartyVerifiers.ts', 'Failed to approve verifier')}
CODE_TRY = "      let code: unknown;\n      try {\n        code = error.code;\n      } catch {\n        code = undefined;\n      }\n"
RSN_TRY = "      let reason: string;\n      try {\n        reason = String(error);\n      } catch {\n        reason = 'unreadable thrown value';\n      }\n"
def block(src, msg):
    i = src.index("logger.error('%s', { error: reason });" % msg)
    j = src.rindex('} catch (error', 0, i)
    k = src.index('\n    }\n', i)
    return j, k
def mut(src, site, m):
    msg = SITES[site][1]; j, k = block(src, msg); b = src[j:k]
    has_code = CODE_TRY in b
    assert RSN_TRY in b, site
    if m.startswith('Mc') and not has_code: return None
    if m == 'M0_revert':
        b = b.replace(CODE_TRY, '').replace("if (code === '23505')", "if (error.code === '23505')").replace(RSN_TRY, '').replace('{ error: reason }', '{ error: String(error) }')
    elif m == 'Mc1_no_code_try': b = b.replace(CODE_TRY, "      const code: unknown = error.code;\n")
    elif m == 'Mc2_unreadable_code_is_23505': b = b.replace('code = undefined;', "code = '23505';")
    elif m == 'Mc3_code_catch_rethrow': b = b.replace('code = undefined;', 'throw error;')
    elif m == 'Mc4_409_check_removed': b = b.replace("if (code === '23505')", "if (code === 'never')")
    elif m == 'Mr1_no_reason_try': b = b.replace(RSN_TRY, "      const reason = String(error);\n")
    elif m == 'Mr2_fallback_String': b = b.replace("reason = 'unreadable thrown value';", 'reason = String(error);')
    elif m == 'Mr3_rethrow_unreadable': b = b.replace("reason = 'unreadable thrown value';", 'throw error;')
    elif m == 'Mr4_constant_always': b = b.replace('reason = String(error);', "reason = 'unreadable thrown value';")
    elif m == 'Mr5_readable_x': b = b.replace('reason = String(error);', "reason = 'x';")
    elif m == 'M7_log_removed': b = b.replace("logger.error('%s', { error: reason });" % msg, 'void reason;')
    elif m == 'M8_no_500': b = b.replace("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: '%s' } });" % msg, 'return;')
    else: raise SystemExit(m)
    out = src[:j] + b + src[k:]
    assert out != src, (site, m)
    return out
MS = ['M0_revert', 'Mc1_no_code_try', 'Mc2_unreadable_code_is_23505', 'Mc3_code_catch_rethrow', 'Mc4_409_check_removed', 'Mr1_no_reason_try', 'Mr2_fallback_String', 'Mr3_rethrow_unreadable', 'Mr4_constant_always', 'Mr5_readable_x', 'M7_log_removed', 'M8_no_500']
rows = []
for site, (P, _) in SITES.items():
    orig = open(P).read(); H = hashlib.sha256(orig.encode()).hexdigest()
    for m in MS:
        new = mut(orig, site, m)
        if new is None: continue
        open(P, 'w').write(new)
        log = f'{G}/logs/mut_{site}__{m}'
        rc = subprocess.run(['bash', G + '/scripts/run.sh', log, '--runTestsByPath'] + T).returncode
        open(P, 'w').write(orig)
        ok = hashlib.sha256(open(P).read().encode()).hexdigest() == H
        failed = []; files = set(); kind = '?'
        try:
            j = json.load(open(log + '.json'))
            fm = ''
            for tr in j['testResults']:
                for a in tr['assertionResults']:
                    if a['status'] != 'passed':
                        t = a['title']; mm = re.search(r'\b(R\d|C\d)\b ([^:]+):', t)
                        failed.append((mm.group(1) + '@' + mm.group(2)) if mm else t[:40]); files.add('nominate' if 'signatories' in tr['name'] else 'verifiers')
                        fm += ' '.join(a.get('failureMessages', []))
                if tr.get('message') and not tr['assertionResults']: kind = 'suite-error'
            if failed: kind = 'assertion' if 'expect(' in fm else 'other'
            elif kind == '?': kind = 'none'
        except Exception as e:
            kind = 'nojson:' + str(e)[:60]
        rows.append(f"{site} | {m} | rc={rc} | {'KILLED' if failed else 'SURVIVED'} {','.join(failed)} | files={sorted(files)} | {kind} | restore {ok}")
        print(rows[-1], flush=True)
open(G + '/logs/mutants_table.log', 'w').write('\n'.join(rows) + '\n')
