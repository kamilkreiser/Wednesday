#!/usr/bin/env python3
"""gh_pr_reads_gate20T2.py — READ-ONLY GitHub GETs for Seat B 21st's TIER-2 four (round20T2): head sha vs the READY / origin, base develop 2bc5ccf63,
the files API (the changed set == the declared file EXACTLY; +/- == the READY), the TIER READ FROM THE FILES vs the READY's proposal (a .md outside
Blockchain/Dev -> docs; a product path under src/ -> product BY THE FILES ALONE — #1203's comment-only claim is what makes it tier 2, and the gate
MEASURES it by token equivalence; __tests__/*.test.sh -> test-only), Refs lines, closing / completeness detectors, archived / foreign keys in title +
branch + subject, the scanner `ks-\\d+` on the four names, the compare develop...head (merge_base / ahead / behind / files), subjects <= 92 ASCII, body
markers (#1203's placement deviation :590 vs :601; KS-547 as content in #1202), the priors #1191 (KS-1081) and #1192 (KS-1139), the tier-1 PRs at origin
(files ∩ ours), other open PRs on develop since 04:52Z, ruleset 18499832. Never prints a body, never prints the token (GH_TOKEN by NAME from the Secuura
.env). Writes nothing (stdout). The gate19B script re-keyed."""
import json, os, re, urllib.request, sys, subprocess
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round20T2 as R
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
print('date', now(), '| PR5_PENDING', R.PR5_PENDING)
if R.PR5_PENDING: print('NOTE: PR 5 is PENDING (no READY 5 captured) — it is read by its EXPECTED branch only, if present')
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
opens = get(REPO + 'pulls?state=open&per_page=100&sort=created&direction=desc')
print('open PRs listed', len(opens), '| numbers', sorted(p['number'] for p in opens))
def tier_by_files(paths):
    prod = [x for x in paths if '__tests__' not in x and '/tests/' not in x and not x.endswith('.md')]
    docs = [x for x in paths if x.endswith('.md')]
    return (1 if prod else 2), prod, docs
tier_table = []
for p_ in R.PUSH:
    pr = R.PRS[p_]
    if not pr['n']: print('PR %s %s: PENDING — skipped' % (p_, pr['key'])); continue
    n = int(pr['n']); want_paths = sorted(f['path'] for f in pr['files'])
    p = get(API + str(n)); files = get(API + str(n) + '/files?per_page=100'); commits = get(API + str(n) + '/commits?per_page=100')
    b = p.get('body') or ''; ti = p.get('title') or ''; br = p['head']['ref']; cm = '\n'.join(c['commit']['message'] for c in commits); subj = cm.splitlines()[0] if cm else ''
    refs = re.findall(r'^\s*Refs?:?\s+(KS-\d+)\s*$', b, re.M | re.I); crefs = re.findall(r'^\s*Refs?:?\s+(KS-\d+)\s*$', cm, re.M | re.I)
    paths = sorted(f['filename'] for f in files); adds = sum(f['additions'] for f in files); dels = sum(f['deletions'] for f in files)
    tf, prod, docs = tier_by_files(paths); tier_table.append((n, pr['key'], paths, tf, R.TIER_RULE[p_], pr['tier_ready'], prod, docs))
    cmp_ = get(REPO + 'compare/develop...' + p['head']['sha'])
    allkeys_b = sorted(set(re.findall(r'KS-\d+', b))); allkeys_c = sorted(set(re.findall(r'KS-\d+', cm)))
    print('#%d PR %s %s %s head %s == READY %s | base %s@%s (== DEV %s) state %s mergeable %s/%s commits %d created %s author %s | closing t/b/c %d/%d/%d completeness %d/%d/%d | Refs body %s == %s: %s | commit Refs %s: %s | every KS key in body %s / commit %s' % (
        n, p_, pr['key'], pr['kind'], p['head']['sha'][:12], p['head']['sha'] == pr['head'], p['base']['ref'], p['base']['sha'][:9], p['base']['sha'] == R.DEV, p['state'], p.get('mergeable'), p.get('mergeable_state'), p['commits'], p['created_at'], p['user']['login'],
        len(CLOSING.findall(ti)), len(CLOSING.findall(b)), len(CLOSING.findall(cm)), len(COMPLETE.findall(ti)), len(COMPLETE.findall(b)), len(COMPLETE.findall(cm)), refs, pr['keys'], sorted(refs) == sorted(pr['keys']), crefs, sorted(crefs) == sorted(pr['keys']), allkeys_b, allkeys_c))
    print('    title (%d chars, ascii %s) == round20T2 %s | %s' % (len(ti), ti.isascii(), ti == pr['title'], ti))
    print('    branch %s == round20T2 %s | scanner %s (own %s) | archived/foreign in branch: %s' % (br, 'refs/heads/' + br == pr['branch'], SCAN.findall(br), [k.lower() for k in pr['keys']], [x for x in SCAN.findall(br) if x.upper() not in pr['keys']] or 'NONE'))
    print('    commit subject (%d chars, ascii %s, <= 92 %s, == READY length %s): %s | subject keys %s' % (len(subj), subj.isascii(), len(subj) <= 92, len(subj) == pr.get('subject_len'), subj, re.findall(r'KS-\d+', subj)))
    for f in files: print('    %-8s +%-4d -%-4d %s' % (f['status'], f['additions'], f['deletions'], f['filename']))
    print('    files API == round20T2: %s | +%d/-%d == READY %s | TIER BY FILES ALONE %d (product %s; docs %s) | TIER BY THE RULE (kind %s) %d | READY %d -> %s' % (paths == want_paths, adds, dels, (adds, dels) == (pr['adds'], pr['dels']), tf, [x.split('/')[-1] for x in prod] or 'none', [x.split('/')[-1] for x in docs] or 'none', pr['kind'], R.TIER_RULE[p_], pr['tier_ready'], 'AGREE' if R.TIER_RULE[p_] == pr['tier_ready'] else 'DISAGREE (the gate grades)'))
    print('    body: "In Progress" %s | ":590" %s ":601" %s | KS-547 %s | "token" %s | "Claude-written" %s | "design change" %s' % ('In Progress' in b, '590' in b, '601' in b, 'KS-547' in b, bool(re.search(r'token', b, re.I)), bool(re.search(r'Claude-written|Claude-authored', b)), 'design change' in b.lower()))
    print('    compare develop...head: merge_base %s (== DEV %s) ahead %d behind %d files %d (want %d)' % (cmp_['merge_base_commit']['sha'][:9], cmp_['merge_base_commit']['sha'] == R.DEV, cmp_['ahead_by'], cmp_['behind_by'], len(cmp_['files']), len(want_paths)))
print('--- TIER TABLE (per PR: files touched -> tier by the files alone | tier by the commission rule (kind) | the READY proposal)')
for n, key, paths, tf, tr, ty, prod, docs in tier_table: print('  #%d %-8s %s -> files-alone T%d | rule T%d | READY T%d | %s' % (n, key, [x.split('/')[-1] for x in paths], tf, tr, ty, 'AGREE' if tr == ty else 'DISAGREE'))
print('--- priors: #1191 (KS-1081) and #1192 (KS-1139) — round 19\'s Seat C rows on the same tickets')
for n in ('1191', '1192'):
    p = get(API + n); fp = sorted(f['filename'] for f in get(API + n + '/files?per_page=100'))
    print('  #%s state %s merged %s merged_at %s title %s | files %s' % (n, p['state'], p.get('merged'), p.get('merged_at'), (p.get('title') or '')[:70], fp))
print('--- the other open PRs on develop created since 04:52Z (the tier-1 batch; anything else is named)')
ours = [R.PRS[q]['n'] for q in R.PUSH if R.PRS[q]['n']]; ALLP = set(R.all_paths())
for p in opens:
    if str(p['number']) in ours or p['base']['ref'] != 'develop' or p['created_at'] < '2026-09-23T04:52:00Z': continue
    fp = sorted(f['filename'] for f in get(API + str(p['number']) + '/files?per_page=100'))
    print('  #%d %s by %s head %s base %s: files %s | ∩ our 4: %s | ⊂ the brief\'s tier-1 paths: %s' % (p['number'], p['title'][:60], p['user']['login'], p['head']['sha'][:9], p['base']['sha'][:9], [x.split('/')[-1] for x in fp], sorted(set(fp) & ALLP) or 'NONE', all(x in R.TIER1_PATHS for x in fp)))
try:
    rs = get(REPO + 'rulesets/18499832'); print('--- ruleset 18499832 %s enforcement %s updated %s rules %s' % (rs['name'], rs['enforcement'], rs['updated_at'], [r['type'] for r in rs['rules']]))
except Exception as e: print('ruleset read failed', e)
print('done', now())
