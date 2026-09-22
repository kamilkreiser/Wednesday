#!/usr/bin/env python3
"""gh_pr_reads_gate19C.py — READ-ONLY GitHub GETs for Seat C 19th's twelve PRs (round19C): head sha vs the READY / origin, base develop 3bad652d1, the
files API (the changed set == the declared files EXACTLY; +/- == the READY), the TIER ASSIGNED FROM THE FILES by the commission's rule (item 1:
.githooks/pre-push, preflight.sh, run-migrations.sh, check-stack-safety.sh, bootstrap-env.sh, Start_Up/start-secuura.sh -> tier 1; the three docs
-> tier 2) vs the READY's proposal, Refs lines (#1187 TWO), closing / completeness detectors, archived / foreign keys in title + branch + subject,
the scanner `ks-\\d+` on the twelve names, the compare develop...head (merge_base / ahead / behind / files), subjects <= 92 ASCII, #1189 (CLOSED,
never merged; its close comment id 5772145479 facts-only, 0 @mentions), Seat B 19th/20th's captured PRs (heads, files ∩ ours), ruleset 18499832.
Never prints a body, never prints the token (GH_TOKEN by NAME from the Secuura .env). Writes nothing (stdout)."""
import glob, json, os, re, urllib.request, urllib.error, sys, subprocess
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round19C as R
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
for f in sorted(glob.glob(os.path.join(G, 'mail_seatC19_ready*_pr*_*.md'))):
    m = re.search(R.ready_regex(), open(f, encoding='utf-8').read())
    if m: READY[m.group(1)] = (int(m.group(3)), m.group(4))
print('READYs parsed:', len(READY), '| == round19C heads:', all(READY[p][1] == R.PRS[p]['head'] and READY[p][0] == int(R.PRS[p]['n']) for p in R.PUSH))
FOREIGN = R.SEATB_KEYS + ['KS-763', 'KS-775', 'KS-1201', 'KS-256', 'KS-485', 'KS-772', 'KS-1230', 'KS-1213', 'KS-932', 'KS-1206', 'KS-1285', 'KS-1175', 'KS-1250', 'KS-1280', 'KS-692', 'KS-1195', 'KS-1265', 'KS-910']
opens = get(REPO + 'pulls?state=open&per_page=100&sort=created&direction=desc')
print('open PRs listed', len(opens), '| numbers', sorted(p['number'] for p in opens))
tier_table = []
for p_ in R.PUSH:
    pr = R.PRS[p_]; n = int(pr['n']); want_paths = sorted(f['path'] for f in pr['files'])
    p = get(API + str(n)); files = get(API + str(n) + '/files?per_page=100'); commits = get(API + str(n) + '/commits?per_page=100')
    b = p.get('body') or ''; ti = p.get('title') or ''; br = p['head']['ref']; cm = '\n'.join(c['commit']['message'] for c in commits); subj = cm.splitlines()[0] if cm else ''
    refs = re.findall(r'^\s*Refs?:?\s+(KS-\d+)\s*$', b, re.M | re.I); crefs = re.findall(r'^\s*Refs?:?\s+(KS-\d+)\s*$', cm, re.M | re.I)
    paths = sorted(f['filename'] for f in files); adds = sum(f['additions'] for f in files); dels = sum(f['deletions'] for f in files)
    tier_rule = 1 if any(x in R.TIER1_SCRIPTS for x in paths) else 2
    tier_table.append((n, pr['key'], paths, tier_rule, pr['tier_ready']))
    cmp_ = get(REPO + 'compare/develop...' + p['head']['sha'])
    print('#%d PR %s %s %s head %s == READY %s | base %s@%s (== DEV %s) state %s mergeable %s/%s commits %d created %s author %s | closing t/b/c %d/%d/%d completeness %d/%d/%d | Refs body %s == %s: %s | commit Refs %s: %s' % (
        n, p_, pr['key'], pr['kind'], p['head']['sha'][:12], p['head']['sha'] == pr['head'], p['base']['ref'], p['base']['sha'][:9], p['base']['sha'] == R.DEV, p['state'], p.get('mergeable'), p.get('mergeable_state'), p['commits'], p['created_at'], p['user']['login'],
        len(CLOSING.findall(ti)), len(CLOSING.findall(b)), len(CLOSING.findall(cm)), len(COMPLETE.findall(ti)), len(COMPLETE.findall(b)), len(COMPLETE.findall(cm)), refs, pr['keys'], sorted(refs) == sorted(pr['keys']), crefs, sorted(crefs) == sorted(pr['keys'])))
    print('    title (%d chars, ascii %s) == round19C %s | %s' % (len(ti), ti.isascii(), ti == pr['title'], ti))
    print('    branch %s == round19C %s | scanner %s (own %s) | archived/foreign in branch: %s' % (br, 'refs/heads/' + br == pr['branch'], SCAN.findall(br), [k.lower() for k in pr['keys']], [k for k in R.ARCHIVED + FOREIGN if re.search(k.lower().replace('-', '-?') + r'(?!\d)', br.lower()) and k not in pr['keys']] or 'NONE'))
    print('    commit subject (%d chars, ascii %s, <= 92 %s): %s | subject keys %s | archived in title/subject: %s' % (len(subj), subj.isascii(), len(subj) <= 92, subj, re.findall(r'KS-\d+', subj), [k for k in R.ARCHIVED if k in ti or k in subj] or 'NONE'))
    for f in files: print('    %-8s +%-4d -%-4d %s' % (f['status'], f['additions'], f['deletions'], f['filename']))
    print('    files API == round19C: %s | +%d/-%d == READY %s | TIER by FILE RULE %d vs READY proposal %d -> %s | body carries --pair-blob %s / 5772145479 %s / #1189 %s' % (paths == want_paths, adds, dels, (adds, dels) == (pr['adds'], pr['dels']), tier_rule, pr['tier_ready'], 'AGREE' if tier_rule == pr['tier_ready'] else 'DISAGREE (the gate grades)', '--pair-blob' in b, '5772145479' in b, '#1189' in b))
    print('    compare develop...head: merge_base %s (== DEV %s) ahead %d behind %d files %d (want %d)' % (cmp_['merge_base_commit']['sha'][:9], cmp_['merge_base_commit']['sha'] == R.DEV, cmp_['ahead_by'], cmp_['behind_by'], len(cmp_['files']), len(want_paths)))
print('--- TIER TABLE (per PR: files touched -> tier by the commission FILE rule vs the READY proposal)')
for n, key, paths, tr, ty in tier_table: print('  #%d %-8s %s -> rule tier %d | READY tier %d | %s' % (n, key, [x.split('/')[-1] for x in paths], tr, ty, 'AGREE' if tr == ty else 'DISAGREE'))
p1189 = get(API + '1189'); print('--- #1189: state %s merged %s merged_at %s head %s == #1190 head %s | branch %s | closed_at %s' % (p1189['state'], p1189.get('merged'), p1189.get('merged_at'), p1189['head']['sha'][:9], p1189['head']['sha'] == R.PRS['7']['head'], p1189['head']['ref'], p1189.get('closed_at')))
cmts = get(REPO + 'issues/1189/comments?per_page=100')
for c in cmts: print('    comment id %s by %s at %s: %d chars, @mentions %d, == pinned id %s, closing-phrase hits %d' % (c['id'], c['user']['login'], c['created_at'], len(c['body']), len(re.findall(r'(?<![\w/])@[A-Za-z0-9-]+', c['body'])), str(c['id']) == R.PRS['7']['close_comment_id'], len(CLOSING.findall(c['body']))))
print('--- Seat B captured PRs (context)')
ALLP = set(R.all_paths())
for n, key, head, paths in R.SEATB:
    p = get(API + n); files = get(API + n + '/files?per_page=100'); fp = sorted(f['filename'] for f in files)
    print('  #%s %s head %s == captured %s state %s base %s@%s | files %d == captured %s | ∩ our 21: %s | under its dirs: %s' % (n, key, p['head']['sha'][:9], p['head']['sha'] == head, p['state'], p['base']['ref'], p['base']['sha'][:9], len(fp), fp == sorted(paths), sorted(set(fp) & ALLP) or 'NONE', all(any(x.startswith(d) for d in R.SEATB_DIRS) for x in fp)))
others = [p for p in opens if str(p['number']) not in [R.PRS[q]['n'] for q in R.PUSH] and p['base']['ref'] == 'develop' and p['created_at'] >= '2026-09-22T04:00:00Z']
for p in others:
    files = get(API + str(p['number']) + '/files?per_page=100'); fp = sorted(f['filename'] for f in files)
    print('  other open PR since 04:00Z #%d %s by %s head %s: files %d ∩ our 21: %s' % (p['number'], p['title'][:60], p['user']['login'], p['head']['sha'][:9], len(fp), sorted(set(fp) & ALLP) or 'NONE'))
try:
    rs = get(REPO + 'rulesets/18499832'); print('--- ruleset 18499832 %s enforcement %s updated %s rules %s' % (rs['name'], rs['enforcement'], rs['updated_at'], [r['type'] for r in rs['rules']]))
except Exception as e: print('ruleset read failed', e)
print('done', subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip())
