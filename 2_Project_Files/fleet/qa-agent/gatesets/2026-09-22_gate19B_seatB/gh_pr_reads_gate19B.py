#!/usr/bin/env python3
"""gh_pr_reads_gate19B.py — READ-ONLY GitHub GETs for Seat B 19th/20th's nine PRs (round19B): head sha vs the READY / origin, base develop 3bad652d1,
the files API (the changed set == the declared files EXACTLY; +/- == the READY), the TIER ASSIGNED FROM THE FILES by the commission's rule (item 1:
product/tooling bytes or an auth-adjacent surface (security/src/index.ts, requestSchemas.ts; the ssrf-guard tamper) -> tier 1; KS-1229 test-only
cells on existing behaviour -> tier 2) vs the READY's proposal, Refs lines, closing / completeness detectors, archived / foreign keys in title +
branch + subject, the scanner `ks-\\d+` on the nine names, the compare develop...head (merge_base / ahead / behind / files), subjects <= 92 ASCII,
the provenance sentence on the Claude-written rows (#1199, #1201) and the AMENDMENT declaration on #1200, Seat C 19th's twelve (heads, files ∩ ours),
KS-1229's prior #1155 and KS-1179's prior #1157 (merged), ruleset 18499832. Never prints a body, never prints the token (GH_TOKEN by NAME from the
Secuura .env). Writes nothing (stdout). The gate19C script re-keyed."""
import glob, json, os, re, urllib.request, urllib.error, sys, subprocess
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round19B as R
sys.path.insert(0, R.SIBLING_GATE_DIR); import round19C as C
print('date', subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip())
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
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatB19_ready0*_pr*_*.md'))) + sorted(glob.glob(os.path.join(G, 'mail_seatB20_ready0*_pr*_*.md'))):
    m = re.search(R.ready_regex(), open(f, encoding='utf-8').read())
    if m: READY[m.group(1)] = (int(m.group(3)), m.group(4))
print('READYs parsed:', len(READY), '| == round19B heads:', all(READY[p][1] == R.PRS[p]['head'] and READY[p][0] == int(R.PRS[p]['n']) for p in R.PUSH))
FOREIGN = C.OWN + ['KS-763', 'KS-775', 'KS-1201', 'KS-256', 'KS-485', 'KS-772', 'KS-1230', 'KS-1213', 'KS-932', 'KS-1206', 'KS-1285', 'KS-1175', 'KS-1250', 'KS-1280', 'KS-692', 'KS-1195', 'KS-1265', 'KS-910']
opens = get(REPO + 'pulls?state=open&per_page=100&sort=created&direction=desc')
print('open PRs listed', len(opens), '| numbers', sorted(p['number'] for p in opens))
tier_table = []
def tier_by_rule(paths):
    prod = [x for x in paths if '__tests__' not in x and '/tests/' not in x]
    auth = [x for x in paths if x in R.AUTH_ADJACENT]
    return (1 if (prod or auth) else 2), prod, auth
for p_ in R.PUSH:
    pr = R.PRS[p_]; n = int(pr['n']); want_paths = sorted(f['path'] for f in pr['files'])
    p = get(API + str(n)); files = get(API + str(n) + '/files?per_page=100'); commits = get(API + str(n) + '/commits?per_page=100')
    b = p.get('body') or ''; ti = p.get('title') or ''; br = p['head']['ref']; cm = '\n'.join(c['commit']['message'] for c in commits); subj = cm.splitlines()[0] if cm else ''
    refs = re.findall(r'^\s*Refs?:?\s+(KS-\d+)\s*$', b, re.M | re.I); crefs = re.findall(r'^\s*Refs?:?\s+(KS-\d+)\s*$', cm, re.M | re.I)
    paths = sorted(f['filename'] for f in files); adds = sum(f['additions'] for f in files); dels = sum(f['deletions'] for f in files)
    tr, prod, auth = tier_by_rule(paths)
    if p_ == '9': tr = 1; auth = ['(tamper on ' + pr['tamper_file'] + ' — the 2026-09-05 tiering rule; the READY\'s words, NOT measured from the files API)']
    tier_table.append((n, pr['key'], paths, tr, pr['tier_ready'], prod, auth))
    cmp_ = get(REPO + 'compare/develop...' + p['head']['sha'])
    print('#%d PR %s %s %s head %s == READY %s | base %s@%s (== DEV %s) state %s mergeable %s/%s commits %d created %s author %s | closing t/b/c %d/%d/%d completeness %d/%d/%d | Refs body %s == %s: %s | commit Refs %s: %s' % (
        n, p_, pr['key'], pr['kind'], p['head']['sha'][:12], p['head']['sha'] == pr['head'], p['base']['ref'], p['base']['sha'][:9], p['base']['sha'] == R.DEV, p['state'], p.get('mergeable'), p.get('mergeable_state'), p['commits'], p['created_at'], p['user']['login'],
        len(CLOSING.findall(ti)), len(CLOSING.findall(b)), len(CLOSING.findall(cm)), len(COMPLETE.findall(ti)), len(COMPLETE.findall(b)), len(COMPLETE.findall(cm)), refs, pr['keys'], sorted(refs) == sorted(pr['keys']), crefs, sorted(crefs) == sorted(pr['keys'])))
    print('    title (%d chars, ascii %s) == round19B %s | %s' % (len(ti), ti.isascii(), ti == pr['title'], ti))
    print('    branch %s == round19B %s | scanner %s (own %s) | archived/foreign in branch: %s' % (br, 'refs/heads/' + br == pr['branch'], SCAN.findall(br), [k.lower() for k in pr['keys']], [k for k in R.ARCHIVED + FOREIGN if re.search(k.lower().replace('-', '-?') + r'(?!\d)', br.lower()) and k not in pr['keys']] or 'NONE'))
    print('    commit subject (%d chars, ascii %s, <= 92 %s): %s | subject keys %s | archived in title/subject: %s' % (len(subj), subj.isascii(), len(subj) <= 92, subj, re.findall(r'KS-\d+', subj), [k for k in R.ARCHIVED if k in ti or k in subj] or 'NONE'))
    for f in files: print('    %-8s +%-4d -%-4d %s' % (f['status'], f['additions'], f['deletions'], f['filename']))
    print('    files API == round19B: %s | +%d/-%d == READY %s | TIER by FILE RULE %d (product/tooling %s; auth-adjacent %s) vs READY proposal %d -> %s' % (paths == want_paths, adds, dels, (adds, dels) == (pr['adds'], pr['dels']), tr, [x.split('/')[-1] for x in prod] or 'none', [x.split('/')[-1] if x.startswith('Blockchain') else x for x in auth] or 'none', pr['tier_ready'], 'AGREE' if tr == pr['tier_ready'] else 'DISAGREE (the gate grades)'))
    print('    body: Claude-written/provenance %s | --pair-blob %s | AMEND/rewrap %s | "In Progress" %s | KS-1213 (content path token) %s | KS-932 (content token) %s' % (bool(re.search(r'Claude-written|Claude-authored', b)), '--pair-blob' in b, bool(re.search(r'[Aa]mend|rewrap', b)), 'In Progress' in b, 'KS-1213' in b, 'KS-932' in b))
    print('    compare develop...head: merge_base %s (== DEV %s) ahead %d behind %d files %d (want %d)' % (cmp_['merge_base_commit']['sha'][:9], cmp_['merge_base_commit']['sha'] == R.DEV, cmp_['ahead_by'], cmp_['behind_by'], len(cmp_['files']), len(want_paths)))
print('--- TIER TABLE (per PR: files touched -> tier by the commission FILE rule vs the READY proposal)')
for n, key, paths, tr, ty, prod, auth in tier_table: print('  #%d %-8s %s -> rule tier %d | READY tier %d | %s' % (n, key, [x.split('/')[-1] for x in paths], tr, ty, 'AGREE' if tr == ty else 'DISAGREE'))
print('--- priors: #1155 (KS-1229) and #1157 (KS-1179)')
for n in ('1155', '1157'):
    p = get(API + n); print('  #%s state %s merged %s merged_at %s title %s' % (n, p['state'], p.get('merged'), p.get('merged_at'), (p.get('title') or '')[:70]))
print('--- Seat C 19th\'s twelve (context: the sibling gate; 0 overlap expected)')
ALLP = set(R.all_paths())
for q in C.PUSH:
    n = C.PRS[q]['n']; p = get(API + n); files = get(API + n + '/files?per_page=100'); fp = sorted(f['filename'] for f in files)
    print('  #%s %s head %s == round19C %s state %s base %s@%s | files %d == round19C %s | ∩ our 17: %s' % (n, C.PRS[q]['key'], p['head']['sha'][:9], p['head']['sha'] == C.PRS[q]['head'], p['state'], p['base']['ref'], p['base']['sha'][:9], len(fp), fp == sorted(f['path'] for f in C.PRS[q]['files']), sorted(set(fp) & ALLP) or 'NONE'))
ours = [R.PRS[q]['n'] for q in R.PUSH] + [C.PRS[q]['n'] for q in C.PUSH]
others = [p for p in opens if str(p['number']) not in ours and p['base']['ref'] == 'develop' and p['created_at'] >= '2026-09-22T04:00:00Z']
for p in others:
    files = get(API + str(p['number']) + '/files?per_page=100'); fp = sorted(f['filename'] for f in files)
    print('  other open PR since 04:00Z #%d %s by %s head %s: files %d ∩ our 17: %s' % (p['number'], p['title'][:60], p['user']['login'], p['head']['sha'][:9], len(fp), sorted(set(fp) & ALLP) or 'NONE'))
try:
    rs = get(REPO + 'rulesets/18499832'); print('--- ruleset 18499832 %s enforcement %s updated %s rules %s' % (rs['name'], rs['enforcement'], rs['updated_at'], [r['type'] for r in rs['rules']]))
except Exception as e: print('ruleset read failed', e)
print('done', subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip())
