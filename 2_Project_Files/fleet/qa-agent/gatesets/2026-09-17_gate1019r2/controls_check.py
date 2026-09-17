#!/usr/bin/env python3
"""controls_check.py — NEGATIVE and POSITIVE FIXTURES for launch_qa_secuura_ks1187_1019r2.sh, every run with --check ONLY (never a launch; stdin /dev/null).
Derived from round 1's controls_check.py. Test inputs are written into this gate set (neg_* / pos_*); the launcher reads them through its QA1019R2_* overrides.
Each brief/prompt replacement asserts its anchor count (>= 1, all occurrences replaced) and its absence after. The proxy.ts fixtures start from develop's own
blob (src/D.routes_proxy.ts, git blob b99f45a4c asserted) with ONE asserted edit (anchor count == 1). Rows run 4 at a time; each row's rc is printed on its own
line, with the first refusal / clearance line."""
import subprocess, os, datetime, hashlib, concurrent.futures
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1019r2'
B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1019r2-ks1187-tier1'
L = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1187_1019r2.sh'
H = '82f09c8bd1bfab28e4d23c180cbaffea251685be'
SUBJ = '[QA -> Wednesday] TIER 1 GATE #1019 ROUND 2 (KS-1187) 82f09c8bd'
RD = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1187-1019r2-82f09c8bd-tier1-r2/'
R1 = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1187-1019-8b8996f8b-tier1-r1/'
prompt = open(B + '.prompt.txt').read(); brief = open(B + '.md').read()
def neg(name, text, old, new):
    n = text.count(old); assert n >= 1, (name, old, n); out = text.replace(old, new); assert old not in out; open(G + '/' + name, 'w').write(out); return n
def gitblob(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()
def pfix(name, old, new):
    raw = open(G + '/src/D.routes_proxy.ts', 'rb').read(); assert gitblob(raw).startswith('b99f45a4c'), gitblob(raw)
    s = raw.decode(); assert s.count(old) == 1, (name, s.count(old)); out = s.replace(old, new); open(G + '/' + name, 'w').write(out); return gitblob(out.encode())[:9]
print('controls_check', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| launcher sha256', hashlib.sha256(open(L, 'rb').read()).hexdigest()[:16])
print('brief/prompt replacements:', {
    'nosubject': neg('neg_prompt_nosubject.txt', prompt, SUBJ, '[QA -> Wednesday] GATE #1019 82f09c8bd'),
    'notier': neg('neg_brief_notier.md', brief, 'TIER 1', 'TIER X'),
    'nosha': neg('neg_brief_nosha.md', brief, H, 'HEAD-SHA-REMOVED'),
    'nomail': neg('neg_prompt_nomail.txt', prompt, 'MAIL YOUR VERDICT', 'SEND YOUR RESULT'),
    'nofarm': neg('neg_prompt_nofarm.txt', prompt, 'node_modules per ENTRY', 'node_modules as needed'),
    'noreportdir': neg('neg_prompt_noreportdir.txt', prompt, RD, '<the report directory>'),
    'nonottested': neg('neg_prompt_nonottested.txt', prompt, 'NOT-TESTED.written-first.md', 'a NOT-TESTED file'),
    'nor1report prompt': neg('neg_prompt_nor1report.txt', prompt, R1, '<the round-1 report>'),
    'nor1report brief': neg('neg_brief_nor1report.md', brief, R1, '<the round-1 report>'),
    'noaddendum': neg('neg_brief_noaddendum.md', brief, 'MERGE ADDENDUM', 'merge note'),
    'nodisposition': neg('neg_brief_nodisposition.md', brief, 'CLOSED / STILL OPEN / NEW', 'per-finding status'),
    'noround2': neg('neg_brief_noround2.md', brief, 'ROUND 2', 'ROUND X'),
})
print('proxy.ts fixtures (git blob):', {
    'INTO the door region (the door chain)': pfix('neg_proxy_into_door_region.ts', '    requireScopeOrRole(ERASURE_SCOPE, ERASURE_GRACE_ROLES, ERASURE_ENFORCE_FLAG),\n', '    requireScopeOrRole(ERASURE_SCOPE, ERASURE_GRACE_ROLES, ERASURE_ENFORCE_FLAG), // QA fixture\n'),
    'INTO the import-to-Factory region (a comment line)': pfix('neg_proxy_into_import_region.ts', '// KS-1041 Step 2 — the shared secret that proves a request came through this\n', '// KS-1041 Step 2 — the shared secret that proves a request came through this (QA fixture)\n'),
    'a region anchor duplicated (anchor count 2)': pfix('neg_proxy_anchor_duplicated.ts', '  // ANCHORING\n', '  // ANCHORING\n  // (QA fixture)   const erasureDoor = Router();\n'),
    'OUTSIDE both regions (the ANCHORING banner)': pfix('pos_proxy_outside_regions.ts', '  // ANCHORING\n', '  // ANCHORING (QA fixture: a comment outside both regions)\n'),
})
for name, src in (('pos_proxy_r2_blob_LANDED.ts', 'H.routes_proxy.ts'), ('pos_proxy_r1_blob_LANDED.ts', 'R1.routes_proxy.ts')):
    open(G + '/' + name, 'wb').write(open(G + '/src/' + src, 'rb').read()); print(name, 'git blob', gitblob(open(G + '/' + name, 'rb').read())[:9])
rows = [('N1 missing subject: prompt without the exact ROUND 2 verdict subject', {'QA1019R2_PROMPT': G + '/neg_prompt_nosubject.txt'}, 23, None),
        ('N2 missing tier: brief without TIER 1', {'QA1019R2_BRIEF': G + '/neg_brief_notier.md'}, 7, None),
        ('N3 missing SHA: brief without the head SHA', {'QA1019R2_BRIEF': G + '/neg_brief_nosha.md'}, 20, None),
        ('N4 missing mail step: prompt without MAIL YOUR VERDICT', {'QA1019R2_PROMPT': G + '/neg_prompt_nomail.txt'}, 12, None),
        ('N5 missing per-entry farm: prompt without node_modules per ENTRY', {'QA1019R2_PROMPT': G + '/neg_prompt_nofarm.txt'}, 22, None),
        ('N6 head override = 4d551f104 (the round-2 commit, not the branch head)', {'QA1019R2_HEAD': '4d551f1046b55209b9ca5e4281e2cb9a868f67c2'}, 6, None),
        ('N7 develop = the #1019 head itself (proxy.ts 795ae7ca3 LANDED)', {'QA1019R2_CUR_DEV': H}, 19, 'has landed'),
        ('N8 develop = 4d551f104, the round-2 commit (proxy.ts 795ae7ca3 LANDED)', {'QA1019R2_CUR_DEV': '4d551f1046b55209b9ca5e4281e2cb9a868f67c2'}, 19, 'round-2 own'),
        ('N9 develop = 8b8996f8b, the round-1 head (proxy.ts db1534753 LANDED)', {'QA1019R2_CUR_DEV': '8b8996f8b290ef55c35721c30f8671f982fa5a91'}, 19, 'round-1 own'),
        ('N10 develop = fa887f382, round 1 develop (auth.ts 20311010d: a blob nobody pinned)', {'QA1019R2_CUR_DEV': 'fa887f382b212b8da4a0a4a556bacb05ea34daaa'}, 18, 'nobody pinned'),
        ('N11 develop = d7e95cd9f, #1017 squash before #1020 (every blob passes; compare f8c7aaa39...d7e95cd9f is not ahead)', {'QA1019R2_CUR_DEV': 'd7e95cd9f153e9036ed77935a73c93504fa6e3dc'}, 18, 'UNJUDGEABLE'),
        ('N12 develop proxy.ts moved INTO the door region (fixture)', {'QA1019R2_PROXY_FILE': G + '/neg_proxy_into_door_region.ts'}, 18, 'region changed'),
        ('N13 develop proxy.ts moved INTO the import-to-Factory region (fixture)', {'QA1019R2_PROXY_FILE': G + '/neg_proxy_into_import_region.ts'}, 18, 'region changed'),
        ('N14 develop proxy.ts with a region anchor duplicated (fixture)', {'QA1019R2_PROXY_FILE': G + '/neg_proxy_anchor_duplicated.ts'}, 18, 'anchor-count-2'),
        ('N15 develop proxy.ts = the round-2 blob (fixture) LANDED', {'QA1019R2_PROXY_FILE': G + '/pos_proxy_r2_blob_LANDED.ts'}, 19, 'round-2 own'),
        ('N16 develop proxy.ts = the round-1 blob (fixture) LANDED', {'QA1019R2_PROXY_FILE': G + '/pos_proxy_r1_blob_LANDED.ts'}, 19, 'round-1 own'),
        ('P17 POSITIVE: develop proxy.ts moved OUTSIDE both regions (fixture) must PASS', {'QA1019R2_PROXY_FILE': G + '/pos_proxy_outside_regions.ts'}, 0, 'moved OUTSIDE'),
        ('N18 prompt without the report directory', {'QA1019R2_PROMPT': G + '/neg_prompt_noreportdir.txt'}, 24, None),
        ('N19 prompt without NOT-TESTED.written-first.md', {'QA1019R2_PROMPT': G + '/neg_prompt_nonottested.txt'}, 24, None),
        ('N20 prompt without the ROUND-1 REPORT path', {'QA1019R2_PROMPT': G + '/neg_prompt_nor1report.txt'}, 24, None),
        ('N21 brief without the ROUND-1 REPORT path', {'QA1019R2_BRIEF': G + '/neg_brief_nor1report.md'}, 24, None),
        ('N22 brief without the MERGE ADDENDUM', {'QA1019R2_BRIEF': G + '/neg_brief_noaddendum.md'}, 25, None),
        ('N23 brief without CLOSED / STILL OPEN / NEW', {'QA1019R2_BRIEF': G + '/neg_brief_nodisposition.md'}, 25, None),
        ('N24 brief without ROUND 2', {'QA1019R2_BRIEF': G + '/neg_brief_noround2.md'}, 15, None)]
def run(row):
    label, env, want, needle = row
    e = dict(os.environ); e.update(env)
    p = subprocess.run([L, '--check'], env=e, stdin=subprocess.DEVNULL, capture_output=True, text=True)
    return row, p
bad = 0
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    results = list(ex.map(run, rows))
for (label, env, want, needle), p in results:
    line = (p.stderr.strip().splitlines() or [''])[0] if p.returncode else next((l for l in p.stdout.splitlines() if 'origin develop' in l), '')
    if not p.returncode and needle:
        seg = [x for x in line.split('; ') if needle in x or 'OUTSIDE' in x]; line = ' ... '.join(seg)[:420] or line[:420]
    print(label, '| ' + ('stderr' if p.returncode else 'stdout') + ':', line[:520])
    print('rc=%d' % p.returncode)
    ok = p.returncode == want and (needle is None or needle in (p.stderr + p.stdout)); bad += (not ok)
    print('expected %d%s: %s' % (want, (" + text '" + needle + "'") if needle else '', 'OK' if ok else 'UNEXPECTED'))
print('unexpected rows', bad, 'of', len(rows))
print('end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
