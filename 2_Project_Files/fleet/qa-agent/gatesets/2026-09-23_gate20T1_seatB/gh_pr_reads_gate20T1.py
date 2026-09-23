#!/usr/bin/env python3
"""gh_pr_reads_gate20T1.py — READ-ONLY GitHub GETs for the round-20 TIER-1 seven (round20T1): head sha vs the READY / origin, base develop@BASE, the
files API (the changed set == the declared files EXACTLY; +/- == the READY), the TIER READ FROM THE FILES (a product/script path -> tier 1), Refs lines,
closing / completeness detectors, archived / foreign keys in title + branch + subject, the scanner `ks-\\d+` on the branch names, the compare against the
CURRENT develop (merge_base == BASE / ahead 1 / behind == the develop move / files), subjects <= 92 ASCII, the per-PR BODY MARKERS the commission names
(#1208 the generated-spec sentence; #1209 the design change + exit 2 + push reach; #1210 the dangling-comment FINDING; #1211 the cross-tenant NOT
measured sentence + Part B out), the tier-2 four (merged? merge commit on develop), the priors (#1185 KS-1033), other open PRs on develop since 04:52Z,
ruleset 18499832. Never prints a body, never prints the token (GH_TOKEN by NAME from the Secuura .env). Writes nothing (stdout). The gate20T2 script
re-keyed; PR 11 is read only once its READY pins it."""
import json, os, re, urllib.request, sys, subprocess
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round20T1 as R
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
print('date', now(), '| PR11_PENDING', R.PR11_PENDING)
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
REPO = 'https://api.github.com/repos/Secuura/Distributed_Secuura/'; API = REPO + 'pulls/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
CLOSING = re.compile(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?|complete[sd]?)\s+#?KS-\d+', re.I)
COMPLETE = re.compile(r'\b(complete[sd]?|completeness|fully pins|now complete|closes the ticket|entire scope|all of KS-\d+)\b', re.I)
assert CLOSING.search('Completes KS-1282') and not CLOSING.search('PREFLIGHT INCOMPLETE — 12/15'), 'closing detector controls'
SCAN = re.compile(r'ks-\d+')
assert SCAN.findall('feature/ks-1257-after-platform-settings-r16-threehunks-1') == ['ks-1257', 'ks-1'], 'scanner control (two keys)'
MARK = {'1208': [('generated', r'generat'), ('Wednesday ruling', r'Wednesday'), ('secuura-api.yaml', r'secuura-api\.yaml'), ('unchanged pass', r'unchanged')],
        '1209': [('design change', r'design change'), ('exit 2', r'exit(s)? 2|exit code 2|`2`'), ('fail-closed', r'fail[- ]closed'), ('push reach', r'push'), ('stderr', r'stderr')],
        '1210': [('FINDING', r'FINDING'), ('platform.ts:204', r'platform\.ts:204'), ('ks1215', r'ks1215'), ('ks1238', r'ks1238'), ('dangl', r'dangl'), ('not fixed/filed', r'(not|nothing) (fixed|filed)|touched none|NOT fixed')],
        '1211': [('cross-tenant', r'cross-tenant'), ('NOT measured', r'not measured|NOT measured|is not measured'), ('Part B', r'Part B'), ('/api/batch', r'/api/batch'), ('P0', r'\bP0\b'), ('closed (the ruled sentence)', r'calls the P0 closed')],
        '1204': [('source-text matcher', r'source-text|source text'), ('QUOTEDWRITE', r'QUOTEDWRITE'), ('--recount', r'--recount|recount')],
        '1207': [('degraded', r'degraded'), ('SMOKE_BASE_URL', r'SMOKE_BASE_URL')]}
opens = get(REPO + 'pulls?state=open&per_page=100&sort=created&direction=desc'); print('open PRs listed', len(opens), '| numbers', sorted(p['number'] for p in opens))
cur_dev = get(REPO + 'branches/develop')['commit']['sha']; print('develop via the branches API:', cur_dev)
def tier_by_files(paths):
    prod = [x for x in paths if '__tests__' not in x and '/tests/' not in x and not x.endswith('.md')]
    return (1 if prod else 2), prod
table = []
for p_ in R.PUSH:
    pr = R.PRS[p_]
    if not pr['n']: print('PR %s %s: PENDING (no READY 11 captured) — not read' % (p_, pr['key'])); continue
    n = int(pr['n']); want = sorted(f['path'] for f in pr['files'])
    p = get(API + str(n)); files = get(API + str(n) + '/files?per_page=100'); commits = get(API + str(n) + '/commits?per_page=100')
    b = p.get('body') or ''; ti = p.get('title') or ''; br = p['head']['ref']; cm = '\n'.join(c['commit']['message'] for c in commits); subj = cm.splitlines()[0] if cm else ''
    refs = re.findall(r'^\s*Refs?:?\s+(KS-\d+)\s*$', b, re.M | re.I); crefs = re.findall(r'^\s*Refs?:?\s+(KS-\d+)\s*$', cm, re.M | re.I)
    paths = sorted(f['filename'] for f in files); adds = sum(f['additions'] for f in files); dels = sum(f['deletions'] for f in files)
    tf, prod = tier_by_files(paths); table.append((n, pr['key'], paths, tf, prod))
    cmp_ = get(REPO + 'compare/' + cur_dev + '...' + p['head']['sha'])
    kb = sorted(set(re.findall(r'KS-\d+', b))); kc = sorted(set(re.findall(r'KS-\d+', cm)))
    print('#%d PR %s %s %s head %s == READY %s | base %s@%s (== BASE %s) state %s mergeable %s/%s commits %d created %s | closing t/b/c %d/%d/%d completeness %d/%d/%d | Refs body %s == %s: %s | commit Refs %s: %s | every KS key in body %s / commit %s' % (
        n, p_, pr['key'], pr['kind'], p['head']['sha'][:12], p['head']['sha'] == pr['head'], p['base']['ref'], p['base']['sha'][:9], p['base']['sha'] == R.BASE, p['state'], p.get('mergeable'), p.get('mergeable_state'), p['commits'], p['created_at'],
        len(CLOSING.findall(ti)), len(CLOSING.findall(b)), len(CLOSING.findall(cm)), len(COMPLETE.findall(ti)), len(COMPLETE.findall(b)), len(COMPLETE.findall(cm)), refs, pr['keys'], sorted(refs) == sorted(pr['keys']), crefs, sorted(crefs) == sorted(pr['keys']), kb, kc))
    print('    title (%d chars, ascii %s) | %s' % (len(ti), ti.isascii(), ti))
    print('    branch %s == round20T1 %s | scanner %s (own %s) | foreign/archived in branch: %s' % (br, ('refs/heads/' + br) == pr['branch'], SCAN.findall(br), [k.lower() for k in pr['keys']], [x for x in SCAN.findall(br) if x.upper() not in pr['keys']] or 'NONE'))
    print('    commit subject (%d chars, ascii %s, <= 92 %s, == READY length %s): %s' % (len(subj), subj.isascii(), len(subj) <= 92, len(subj) == pr.get('subject_len'), subj))
    for f in files: print('    %-8s +%-4d -%-4d %s' % (f['status'], f['additions'], f['deletions'], f['filename']))
    print('    files API == round20T1: %s | +%d/-%d == READY %s | TIER BY FILES ALONE %d (product/script %s) | READY/ruling T1' % (paths == want, adds, dels, (adds, dels) == (pr['adds'], pr['dels']), tf, [x.split('/')[-1] for x in prod] or 'none'))
    mk = MARK.get(str(n), [])
    print('    body markers: %s | body length %d' % (' | '.join('%s %s' % (lab, bool(re.search(rx, b, re.I if lab not in ('FINDING', 'NOT measured', 'P0') else 0))) for lab, rx in mk) or 'none named', len(b)))
    print('    compare develop(now %s)...head: merge_base %s (== BASE %s) ahead %d behind %d files %d (want %d)' % (cur_dev[:9], cmp_['merge_base_commit']['sha'][:9], cmp_['merge_base_commit']['sha'] == R.BASE, cmp_['ahead_by'], cmp_['behind_by'], len(cmp_['files']), len(want)))
print('--- TIER TABLE (per PR: files -> tier by the files alone | the READY / Wednesday 05:12:13Z ruling: T1 x7)')
for n, key, paths, tf, prod in table: print('  #%d %-8s %s -> files-alone T%d | ruled T1 | %s' % (n, key, [x.split('/')[-1] for x in paths], tf, 'AGREE' if tf == 1 else 'FILES SAY T2 — T1 by ruling (a test-only pin on a PII surface: KS-851) — the gate states both'))
print('--- the tier-2 four (GO 07:36:38Z): merged?')
for n, (k, h) in sorted(R.T2_PRS.items()):
    p = get(API + n); print('  #%s %s state %s merged %s merged_at %s merge_commit %s | head %s == the GO head %s' % (n, k, p['state'], p.get('merged'), p.get('merged_at'), (p.get('merge_commit_sha') or '')[:12], p['head']['sha'][:9], p['head']['sha'] == h))
print('--- priors: #1185 (KS-1033, round 19)')
for n in ('1185',):
    p = get(API + n); fp = sorted(f['filename'] for f in get(API + n + '/files?per_page=100'))
    print('  #%s state %s merged %s merged_at %s title %s | files %s' % (n, p['state'], p.get('merged'), p.get('merged_at'), (p.get('title') or '')[:70], [x.split('/')[-1] for x in fp]))
print('--- other open PRs on develop created since 04:52Z')
ours = [R.PRS[q]['n'] for q in R.PUSH if R.PRS[q]['n']]; ALLP = set(R.all_paths())
for p in opens:
    if str(p['number']) in ours or p['base']['ref'] != 'develop' or p['created_at'] < '2026-09-23T04:52:00Z': continue
    fp = sorted(f['filename'] for f in get(API + str(p['number']) + '/files?per_page=100'))
    print('  #%d %s by %s head %s base %s: files %s | ∩ our paths: %s' % (p['number'], p['title'][:60], p['user']['login'], p['head']['sha'][:9], p['base']['sha'][:9], [x.split('/')[-1] for x in fp], sorted(set(fp) & ALLP) or 'NONE'))
try:
    rs = get(REPO + 'rulesets/18499832'); print('--- ruleset 18499832 %s enforcement %s updated %s rules %s' % (rs['name'], rs['enforcement'], rs['updated_at'], [r['type'] for r in rs['rules']]))
except Exception as e: print('ruleset read failed', e)
print('done', now())
