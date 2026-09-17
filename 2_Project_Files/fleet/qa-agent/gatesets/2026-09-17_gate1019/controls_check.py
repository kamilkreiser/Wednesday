#!/usr/bin/env python3
"""controls_check.py — NEGATIVE and POSITIVE FIXTURES for launch_qa_secuura_ks1187_1019.sh, every run with --check ONLY (never a launch; stdin /dev/null).
Derived from the #1017 set's controls_check.py. Test inputs are written into this gate set (neg_* / pos_*); the launcher reads them through its QA1019_*
overrides. Each brief/prompt replacement asserts its anchor count (>= 1, all occurrences replaced) and its absence after. The proxy.ts fixtures start from
develop's own base blob (src/B.routes_proxy.ts, git blob asserted) with ONE asserted edit (anchor count == 1). Rows run 4 at a time; each row's rc is printed
on its own line, with the first refusal / clearance line."""
import subprocess, os, datetime, hashlib, concurrent.futures
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1019'
B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1019-ks1187-tier1'
L = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1187_1019.sh'
H = '8b8996f8b290ef55c35721c30f8671f982fa5a91'
SUBJ = '[QA -> Wednesday] TIER 1 GATE #1019 (KS-1187) 8b8996f8b'
RD = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1187-1019-8b8996f8b-tier1-r1/'
prompt = open(B + '.prompt.txt').read(); brief = open(B + '.md').read()
def neg(name, text, old, new):
    n = text.count(old); assert n >= 1, (name, old, n); out = text.replace(old, new); assert old not in out; open(G + '/' + name, 'w').write(out); return n
def gitblob(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()
def pfix(name, old, new):
    raw = open(G + '/src/B.routes_proxy.ts', 'rb').read(); assert gitblob(raw).startswith('b99f45a4c'), gitblob(raw)
    s = raw.decode(); assert s.count(old) == 1, (name, s.count(old)); out = s.replace(old, new); open(G + '/' + name, 'w').write(out); return gitblob(out.encode())[:9]
print('controls_check', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| launcher sha256', hashlib.sha256(open(L, 'rb').read()).hexdigest()[:16])
print('brief/prompt replacements:', {
    'nosubject': neg('neg_prompt_nosubject.txt', prompt, SUBJ, '[QA -> Wednesday] GATE #1019 8b8996f8b'),
    'notier': neg('neg_brief_notier.md', brief, 'TIER 1', 'TIER X'),
    'nosha': neg('neg_brief_nosha.md', brief, H, 'HEAD-SHA-REMOVED'),
    'nomail': neg('neg_prompt_nomail.txt', prompt, 'MAIL YOUR VERDICT', 'SEND YOUR RESULT'),
    'nofarm': neg('neg_prompt_nofarm.txt', prompt, 'node_modules per ENTRY', 'node_modules as needed'),
    'noreportdir': neg('neg_prompt_noreportdir.txt', prompt, RD, '<the report directory>'),
    'nonottested': neg('neg_prompt_nonottested.txt', prompt, 'NOT-TESTED.written-first.md', 'a NOT-TESTED file'),
    'noaddendum': neg('neg_brief_noaddendum.md', brief, 'MERGE ADDENDUM', 'merge note'),
    'noround1': neg('neg_brief_noround1.md', brief, 'ROUND 1', 'ROUND X'),
})
print('proxy.ts fixtures (git blob):', {
    'INTO the door region (the door chain)': pfix('neg_proxy_into_door_region.ts', '    requireScopeOrRole(ERASURE_SCOPE, ERASURE_GRACE_ROLES, ERASURE_ENFORCE_FLAG),\n', '    requireScopeOrRole(ERASURE_SCOPE, ERASURE_GRACE_ROLES, ERASURE_ENFORCE_FLAG), // QA fixture\n'),
    'INTO the import-to-Factory region (a comment line)': pfix('neg_proxy_into_import_region.ts', '// KS-1041 Step 2 — the shared secret that proves a request came through this\n', '// KS-1041 Step 2 — the shared secret that proves a request came through this (QA fixture)\n'),
    'a region anchor duplicated (anchor count 2)': pfix('neg_proxy_anchor_duplicated.ts', '  // ANCHORING\n', '  // ANCHORING\n  // (QA fixture)   const erasureDoor = Router();\n'),
    'OUTSIDE both regions (the ANCHORING banner)': pfix('pos_proxy_outside_regions.ts', '  // ANCHORING\n', '  // ANCHORING (QA fixture: a comment outside both regions)\n'),
})
open(G + '/pos_proxy_head_blob_LANDED.ts', 'wb').write(open(G + '/src/H.routes_proxy.ts', 'rb').read()); print('head proxy.ts copied as a fixture, git blob', gitblob(open(G + '/pos_proxy_head_blob_LANDED.ts', 'rb').read())[:9])
rows = [('N1 missing subject: prompt without the exact verdict subject', {'QA1019_PROMPT': G + '/neg_prompt_nosubject.txt'}, 23, None),
        ('N2 missing tier: brief without TIER 1', {'QA1019_BRIEF': G + '/neg_brief_notier.md'}, 7, None),
        ('N3 missing SHA: brief without the head SHA', {'QA1019_BRIEF': G + '/neg_brief_nosha.md'}, 20, None),
        ('N4 missing mail step: prompt without MAIL YOUR VERDICT', {'QA1019_PROMPT': G + '/neg_prompt_nomail.txt'}, 12, None),
        ('N5 missing per-entry farm: prompt without node_modules per ENTRY', {'QA1019_PROMPT': G + '/neg_prompt_nofarm.txt'}, 22, None),
        ('N6 head override = 50a4b749a (the product commit, not the head)', {'QA1019_HEAD': '50a4b749ad83bac865dd4216d56b19dd7bdf50b5'}, 6, None),
        ('N7 develop = the #1019 head itself (proxy.ts db1534753 LANDED)', {'QA1019_CUR_DEV': H}, 19, 'has landed'),
        ('N8 develop = 50a4b749a, #1019 first commit (proxy.ts db1534753 LANDED)', {'QA1019_CUR_DEV': '50a4b749ad83bac865dd4216d56b19dd7bdf50b5'}, 19, 'has landed'),
        ('N9 develop = 7e89318bc, the pre-#1014 develop (compare fa887f382...7e89318bc is not ahead)', {'QA1019_CUR_DEV': '7e89318bcedbc9a35757d4298ace54a6a23020bd'}, 18, None),
        ('N10 develop = #1017 head cbe29597d (its blobs ACCEPTED by the blob arm; the compare is diverged, not ahead -> refuse)', {'QA1019_CUR_DEV': 'cbe29597d11e59f2e1a14519e9ba3dbf6de9a756'}, 18, 'UNJUDGEABLE'),
        ('N10b develop = #1017 round-2 head a067d4e3e (round-2 blobs ACCEPTED by the blob arm; compare diverged -> refuse)', {'QA1019_CUR_DEV': 'a067d4e3e80f0e31c1aecb278f06c4f6df4b1c66'}, 18, 'UNJUDGEABLE'),
        ('N10c develop = #1017 first commit 973eb49ef (auth.ts 8fbe102eb pinned, but the ks781 test at ca1fe34a7 / index db127dbfa: blob arm passes; compare diverged -> refuse)', {'QA1019_CUR_DEV': '973eb49ef602ceee4bf2134ddb9405e00663e86f'}, 18, None),
        ('N11 develop proxy.ts moved INTO the door region (fixture)', {'QA1019_PROXY_FILE': G + '/neg_proxy_into_door_region.ts'}, 18, 'region changed'),
        ('N12 develop proxy.ts moved INTO the import-to-Factory region (fixture)', {'QA1019_PROXY_FILE': G + '/neg_proxy_into_import_region.ts'}, 18, 'region changed'),
        ('N13 develop proxy.ts with a region anchor duplicated (fixture)', {'QA1019_PROXY_FILE': G + '/neg_proxy_anchor_duplicated.ts'}, 18, 'anchor-count-2'),
        ('N14 develop proxy.ts = the #1019 head blob (fixture) LANDED', {'QA1019_PROXY_FILE': G + '/pos_proxy_head_blob_LANDED.ts'}, 19, 'has landed'),
        ('P15 POSITIVE: develop proxy.ts moved OUTSIDE both regions (fixture) must PASS', {'QA1019_PROXY_FILE': G + '/pos_proxy_outside_regions.ts'}, 0, 'moved OUTSIDE'),
        ('N16 prompt without the report directory', {'QA1019_PROMPT': G + '/neg_prompt_noreportdir.txt'}, 24, None),
        ('N17 prompt without NOT-TESTED.written-first.md', {'QA1019_PROMPT': G + '/neg_prompt_nonottested.txt'}, 24, None),
        ('N18 brief without the MERGE ADDENDUM', {'QA1019_BRIEF': G + '/neg_brief_noaddendum.md'}, 25, None),
        ('N19 brief without ROUND 1', {'QA1019_BRIEF': G + '/neg_brief_noround1.md'}, 15, None)]
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
