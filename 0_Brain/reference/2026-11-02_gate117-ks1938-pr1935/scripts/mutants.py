import hashlib, json, subprocess, sys, re
G = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate117-ks1938-pr1935'
P = G + '/repo/Blockchain/Dev/services/originate/src/services/gdprService.ts'
T = G + '/repo/Blockchain/Dev/services/originate/src/__tests__/ks1938-gdpr-retention-sweep-catches-unreadable-throw.test.ts'
orig = open(P).read(); H = hashlib.sha256(orig.encode()).hexdigest()
lines = orig.split('\n')
# site blocks (0-based): inner catch body 498..504 (file lines 499..505), outer 508..514 (file 509..515)
SITES = {'S1_inner': (498, 'Retention enforcement failed'), 'S2_outer': (508, 'Retention enforcement error')}
EXPR = 'err instanceof Error ? err.message : String(err)'
def mut(site, m):
    L = list(lines); s, msg = SITES[site]
    blk = L[s:s + 7]
    assert blk[0].strip() == 'let reason: string;' and msg in blk[6], (site, blk)
    ind = blk[0][:len(blk[0]) - len(blk[0].lstrip())]
    if m == 'M0_revert': blk = [blk[6].replace('error: reason', 'error: ' + EXPR)]
    elif m == 'M1_no_inner_try': blk = [ind + 'const reason = ' + EXPR + ';', blk[6]]
    elif m == 'M2_catch_String': blk[4] = blk[4].replace("'unreadable thrown value'", 'String(err)')
    elif m == 'M3_rethrow_unreadable': blk[4] = blk[4].replace("reason = 'unreadable thrown value';", 'throw err;')
    elif m == 'M4_constant_always': blk[2] = blk[2].replace(EXPR, "'unreadable thrown value'")
    elif m == 'M5_rethrow_all_after_log': blk[6] = blk[6] + ' throw err;'
    elif m == 'M6_nonError_x': blk[2] = blk[2].replace('String(err)', "'x'")
    elif m == 'M7_log_removed': blk[6] = ind + 'void reason;'
    elif m == 'M8_stop_sweep_after_unreadable': blk[4] = blk[4] + ' return logs;'
    else: raise SystemExit(m)
    L[s:s + 7] = blk
    return '\n'.join(L)
MS = ['M0_revert', 'M1_no_inner_try', 'M2_catch_String', 'M3_rethrow_unreadable', 'M4_constant_always', 'M5_rethrow_all_after_log', 'M6_nonError_x', 'M7_log_removed', 'M8_stop_sweep_after_unreadable']
rows = []
for site in SITES:
    for m in MS:
        open(P, 'w').write(mut(site, m))
        log = f'{G}/logs/mut_{site}__{m}'
        rc = subprocess.run(['bash', G + '/scripts/run.sh', log, '--runTestsByPath', T]).returncode
        open(P, 'w').write(orig)
        ok = hashlib.sha256(open(P).read().encode()).hexdigest() == H
        failed = []
        try:
            j = json.load(open(log + '.json'))
            for tr in j['testResults']:
                for a in tr['assertionResults']:
                    if a['status'] != 'passed': failed.append(re.sub(r'^.*?(C\d|R\d).*$', r'\1', a['title']))
            fmsgs = ' '.join(' '.join(a.get('failureMessages', [])) for tr in j['testResults'] for a in tr['assertionResults'])
            kind = 'assertion' if ('expect(' in fmsgs or 'toEqual' in fmsgs) else ('none' if not failed else 'other')
        except Exception as e:
            kind = 'nojson:' + str(e)[:60]
        rows.append(f"{site} | {m} | rc={rc} | {'KILLED' if failed else 'SURVIVED'} {','.join(failed)} | {kind} | restore {ok}")
        print(rows[-1], flush=True)
open(G + '/logs/mutants_table.log', 'w').write('\n'.join(rows) + '\n')
