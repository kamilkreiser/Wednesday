#!/usr/bin/env python3
"""controls_check.py — NEGATIVE and POSITIVE FIXTURES for launch_qa_secuura_ks1195_1017.sh, every run with --check ONLY (never a launch; stdin /dev/null).
Test inputs are written into this gate set (neg_* / pos_*); the launcher reads them through its QA1017_* overrides. Each brief/prompt replacement asserts its
anchor count (>= 1, all occurrences replaced) and its absence after. The product-file fixtures start from develop's own base blobs (src/B.*, git blob asserted)
with ONE asserted edit (anchor count == 1). Rows run 4 at a time; each row's rc is printed on its own line, with the first refusal / clearance line."""
import subprocess, os, datetime, hashlib, concurrent.futures
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1017'
B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1017-ks1195-tier1'
L = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1195_1017.sh'
H = 'cbe29597d11e59f2e1a14519e9ba3dbf6de9a756'
SUBJ = '[QA -> Wednesday] TIER 1 GATE #1017 (KS-1195) cbe29597d'
RD = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1195-1017-cbe29597d-tier1-r1/'
prompt = open(B + '.prompt.txt').read(); brief = open(B + '.md').read()
def neg(name, text, old, new):
    n = text.count(old); assert n >= 1, (name, old, n); out = text.replace(old, new); assert old not in out; open(G + '/' + name, 'w').write(out); return n
def gitblob(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()
BASE = {'auth': ('B.middleware_auth.ts', '20311010d'), 'rle': ('B.middleware_rateLimitEnforce.ts', 'fc5c5a4d9'), 'index': ('B.index.ts', '6f38c819e')}
def pfix(name, which, old, new):
    raw = open(G + '/src/' + BASE[which][0], 'rb').read(); assert gitblob(raw).startswith(BASE[which][1]), (which, gitblob(raw))
    s = raw.decode(); assert s.count(old) == 1, (name, s.count(old)); out = s.replace(old, new); open(G + '/' + name, 'w').write(out); return gitblob(out.encode())[:9]
print('controls_check', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| launcher sha256', hashlib.sha256(open(L, 'rb').read()).hexdigest()[:16])
print('brief/prompt replacements:', {
    'nosubject': neg('neg_prompt_nosubject.txt', prompt, SUBJ, '[QA -> Wednesday] GATE #1017 cbe29597d'),
    'notier': neg('neg_brief_notier.md', brief, 'TIER 1', 'TIER X'),
    'nosha': neg('neg_brief_nosha.md', brief, H, 'HEAD-SHA-REMOVED'),
    'nomail': neg('neg_prompt_nomail.txt', prompt, 'MAIL YOUR VERDICT', 'SEND YOUR RESULT'),
    'nofarm': neg('neg_prompt_nofarm.txt', prompt, 'node_modules per ENTRY', 'node_modules as needed'),
    'noreportdir': neg('neg_prompt_noreportdir.txt', prompt, RD, '<the report directory>'),
    'nonottested': neg('neg_prompt_nonottested.txt', prompt, 'NOT-TESTED.written-first.md', 'a NOT-TESTED file'),
    'noaddendum': neg('neg_brief_noaddendum.md', brief, 'MERGE ADDENDUM', 'merge note'),
    'noround1': neg('neg_brief_noround1.md', brief, 'ROUND 1', 'ROUND X'),
})
print('product-file fixtures (git blob):', {
    'auth INTO region (API-key branch continuation)': pfix('neg_auth_into_region.ts', 'auth', 'runWithTenantId(meta.tenantId, next);', 'runWithTenantId(meta.tenantId || undefined, next);'),
    'auth OUTSIDE region (header doc comment)': pfix('pos_auth_outside_region.ts', 'auth', ' * - API key validation via the Security Service\n', ' * - API key validation via the Security Service\n * (QA fixture: a header-comment line outside the region)\n'),
    'rle INTO region (machine set)': pfix('neg_rle_into_region.ts', 'rle', "const MACHINE_AUTH_METHODS = new Set(['api_key', 'oauth_app']);", "const MACHINE_AUTH_METHODS = new Set(['api_key', 'oauth_app', 'oauth']);"),
    'rle OUTSIDE region (header doc comment)': pfix('pos_rle_outside_region.ts', 'rle', ' * Enforces rate limits defined in API key / OAuth app metadata.\n', ' * Enforces rate limits defined in API key / OAuth app metadata.\n * (QA fixture: a header-comment line outside the region)\n'),
    'index INTO region (global limiter max)': pfix('neg_index_into_limiter_region.ts', 'index', "(isNonProd ? '10000' : '300')", "(isNonProd ? '10000' : '301')"),
    'index ABOVE the pins, outside region (one import-area line)': pfix('neg_index_pins_shifted.ts', 'index', "import { errorHandler, payloadTooLargeErrorHandler } from './middleware/errorHandler';\n", "// QA fixture: one line above the ks781 pins\nimport { errorHandler, payloadTooLargeErrorHandler } from './middleware/errorHandler';\n"),
})
raw = open(G + '/src/B.index.ts', 'rb').read(); out = raw + b'\n// QA fixture: a trailing line after the platform mount and the pins\n'
open(G + '/pos_index_outside_region_after_pins.ts', 'wb').write(out); print('index OUTSIDE region, after the pins (appended line) git blob', gitblob(out)[:9])
rows = [('N1 missing subject: prompt without the exact verdict subject', {'QA1017_PROMPT': G + '/neg_prompt_nosubject.txt'}, 23, None),
        ('N2 missing tier: brief without TIER 1', {'QA1017_BRIEF': G + '/neg_brief_notier.md'}, 7, None),
        ('N3 missing SHA: brief without the head SHA', {'QA1017_BRIEF': G + '/neg_brief_nosha.md'}, 20, None),
        ('N4 missing mail step: prompt without MAIL YOUR VERDICT', {'QA1017_PROMPT': G + '/neg_prompt_nomail.txt'}, 12, None),
        ('N5 missing per-entry farm: prompt without node_modules per ENTRY', {'QA1017_PROMPT': G + '/neg_prompt_nofarm.txt'}, 22, None),
        ('N6 head override = 973eb49ef (the product commit, not the head)', {'QA1017_HEAD': '973eb49ef602ceee4bf2134ddb9405e00663e86f'}, 6, None),
        ('N7 develop = the #1017 head itself (auth.ts 8fbe102eb LANDED)', {'QA1017_CUR_DEV': H}, 19, 'has landed'),
        ('N8 develop = 7e89318bc, the pre-#1014 develop (verification.ts a7a6d4605 nobody pinned)', {'QA1017_CUR_DEV': '7e89318bcedbc9a35757d4298ace54a6a23020bd'}, 18, 'verification.ts'),
        ('N9 develop = 9ba0caf78, #1014 branch head (audit.ts a7be8626f / verification.ts 6bd095f62 nobody pinned)', {'QA1017_CUR_DEV': '9ba0caf78b8ddb737541df38303b776c982521d2'}, 18, 'nobody pinned'),
        ('N10 develop auth.ts moved INTO its region (fixture)', {'QA1017_AUTH_FILE': G + '/neg_auth_into_region.ts'}, 18, 'region changed'),
        ('N11 develop rateLimitEnforce.ts moved INTO its region (fixture)', {'QA1017_RLE_FILE': G + '/neg_rle_into_region.ts'}, 18, 'region changed'),
        ('N12 develop index.ts moved INTO the limiter region (fixture)', {'QA1017_INDEX_FILE': G + '/neg_index_into_limiter_region.ts'}, 18, 'region changed'),
        ('N13 develop index.ts gained one line ABOVE the ks781 pins, outside the region (fixture)', {'QA1017_INDEX_FILE': G + '/neg_index_pins_shifted.ts'}, 18, 'pin lines moved'),
        ('P14 POSITIVE: develop auth.ts moved OUTSIDE its region (fixture) must PASS', {'QA1017_AUTH_FILE': G + '/pos_auth_outside_region.ts'}, 0, 'moved OUTSIDE'),
        ('P15 POSITIVE: develop rateLimitEnforce.ts moved OUTSIDE its region (fixture) must PASS', {'QA1017_RLE_FILE': G + '/pos_rle_outside_region.ts'}, 0, 'moved OUTSIDE'),
        ('P16 POSITIVE: develop index.ts moved OUTSIDE the region AFTER the pins (fixture) must PASS', {'QA1017_INDEX_FILE': G + '/pos_index_outside_region_after_pins.ts'}, 0, 'pins 846/859/892 hold'),
        ('N17 prompt without the report directory', {'QA1017_PROMPT': G + '/neg_prompt_noreportdir.txt'}, 24, None),
        ('N18 prompt without NOT-TESTED.written-first.md', {'QA1017_PROMPT': G + '/neg_prompt_nonottested.txt'}, 24, None),
        ('N19 brief without the MERGE ADDENDUM', {'QA1017_BRIEF': G + '/neg_brief_noaddendum.md'}, 25, None),
        ('N20 brief without ROUND 1', {'QA1017_BRIEF': G + '/neg_brief_noround1.md'}, 15, None)]
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
    print(label, '| ' + ('stderr' if p.returncode else 'stdout') + ':', line[:420])
    print('rc=%d' % p.returncode)
    ok = p.returncode == want and (needle is None or needle in (p.stderr + p.stdout)); bad += (not ok)
    print('expected %d%s: %s' % (want, (" + text '" + needle + "'") if needle else '', 'OK' if ok else 'UNEXPECTED'))
print('unexpected rows', bad, 'of', len(rows))
print('end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
