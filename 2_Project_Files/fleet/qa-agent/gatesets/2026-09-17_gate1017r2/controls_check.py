#!/usr/bin/env python3
"""controls_check.py — NEGATIVE and POSITIVE FIXTURES for launch_qa_secuura_ks1195_1017r2.sh, every run with --check ONLY (never a launch; stdin /dev/null).
Derived from the round-1 set's controls_check.py. Test inputs are written into this gate set (neg_* / pos_*); the launcher reads them through its QA1017R2_*
overrides. Each brief/prompt replacement asserts its anchor count (>= 1, all occurrences replaced) and its absence after. Product-file fixtures start from
develop's own base blobs (round 1's R1GS/src/B.*, git blob asserted) with ONE asserted edit, or are the round-2 head's own auth.ts (blob 7c985bdce asserted:
the LANDED arm). Rows run 4 at a time; each row's rc is printed on its own line with the first refusal / clearance line."""
import subprocess, os, hashlib, concurrent.futures
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1017r2'
R1S = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1017/src/'
B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1017r2-ks1195-tier1'
L = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1195_1017r2.sh'
H = 'a067d4e3e80f0e31c1aecb278f06c4f6df4b1c66'
SUBJ = '[QA -> Wednesday] TIER 1 GATE #1017 ROUND 2 (KS-1195) a067d4e3e'
RD = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1195-1017r2-a067d4e3e-tier1-r2/'
R1 = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1195-1017-cbe29597d-tier1-r1/'
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
prompt = open(B + '.prompt.txt').read(); brief = open(B + '.md').read()
def neg(name, text, old, new):
    n = text.count(old); assert n >= 1, (name, old, n); out = text.replace(old, new); assert old not in out; open(G + '/' + name, 'w').write(out); return n
def gitblob(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()
BASE = {'auth': ('B.middleware_auth.ts', '20311010d'), 'rle': ('B.middleware_rateLimitEnforce.ts', 'fc5c5a4d9'), 'index': ('B.index.ts', '6f38c819e')}
def pfix(name, which, old, new):
    raw = open(R1S + BASE[which][0], 'rb').read(); assert gitblob(raw).startswith(BASE[which][1]), (which, gitblob(raw))
    s = raw.decode(); assert s.count(old) == 1, (name, s.count(old)); out = s.replace(old, new); open(G + '/' + name, 'w').write(out); return gitblob(out.encode())[:9]
print('controls_check', now(), '| launcher sha256', hashlib.sha256(open(L, 'rb').read()).hexdigest()[:16])
print('brief/prompt replacements:', {
    'nosubject': neg('neg_prompt_nosubject.txt', prompt, SUBJ, '[QA -> Wednesday] GATE #1017 a067d4e3e'),
    'notier': neg('neg_brief_notier.md', brief, 'TIER 1', 'TIER X'),
    'nosha': neg('neg_brief_nosha.md', brief, H, 'HEAD-SHA-REMOVED'),
    'nomail': neg('neg_prompt_nomail.txt', prompt, 'MAIL YOUR VERDICT', 'SEND YOUR RESULT'),
    'nofarm': neg('neg_prompt_nofarm.txt', prompt, 'node_modules per ENTRY', 'node_modules as needed'),
    'noreportdir': neg('neg_prompt_noreportdir.txt', prompt, RD, '<the report directory>'),
    'nonottested': neg('neg_prompt_nonottested.txt', prompt, 'NOT-TESTED.written-first.md', 'a NOT-TESTED file'),
    'nor1report_prompt': neg('neg_prompt_nor1report.txt', prompt, R1, '<the round-1 report>'),
    'nor1report_brief': neg('neg_brief_nor1report.md', brief, R1, '<the round-1 report>'),
    'noaddendum': neg('neg_brief_noaddendum.md', brief, 'MERGE ADDENDUM', 'merge note'),
    'nodisposition': neg('neg_brief_nodisposition.md', brief, 'CLOSED / STILL OPEN / NEW', 'closed or open'),
    'noround2': neg('neg_brief_noround2.md', brief, 'ROUND 2', 'ROUND X'),
})
hraw = open(G + '/src/H.middleware_auth.ts', 'rb').read(); assert gitblob(hraw) == '7c985bdcefc26293815bfbe0cbf315f929b48835'
print('LANDED fixture: the round-2 head auth.ts, git blob', gitblob(hraw)[:9])
print('product-file fixtures (git blob):', {
    'auth INTO region (API-key branch continuation)': pfix('neg_auth_into_region.ts', 'auth', 'runWithTenantId(meta.tenantId, next);', 'runWithTenantId(meta.tenantId || undefined, next);'),
    'auth OUTSIDE region (header doc comment)': pfix('pos_auth_outside_region.ts', 'auth', ' * - API key validation via the Security Service\n', ' * - API key validation via the Security Service\n * (QA fixture: a header-comment line outside the region)\n'),
    'rle INTO region (the bucket line)': pfix('neg_rle_into_region.ts', 'rle', "const clientId = user.connectorId || user.userId || 'unknown';", "const clientId = user.userId || user.connectorId || 'unknown';"),
    'rle OUTSIDE region (header doc comment)': pfix('pos_rle_outside_region.ts', 'rle', ' * Enforces rate limits defined in API key / OAuth app metadata.\n', ' * Enforces rate limits defined in API key / OAuth app metadata.\n * (QA fixture: a header-comment line outside the region)\n'),
    'index INTO region (global limiter max)': pfix('neg_index_into_limiter_region.ts', 'index', "(isNonProd ? '10000' : '300')", "(isNonProd ? '10000' : '301')"),
    'index ABOVE the pins, outside region': pfix('neg_index_pins_shifted.ts', 'index', "import { errorHandler, payloadTooLargeErrorHandler } from './middleware/errorHandler';\n", "// QA fixture: one line above the ks781 pins\nimport { errorHandler, payloadTooLargeErrorHandler } from './middleware/errorHandler';\n"),
})
raw = open(R1S + 'B.index.ts', 'rb').read(); out = raw + b'\n// QA fixture: a trailing line after the platform mount and the pins\n'
open(G + '/pos_index_outside_region_after_pins.ts', 'wb').write(out); print('index OUTSIDE region, after the pins (appended line) git blob', gitblob(out)[:9])
E = 'QA1017R2_'
rows = [('N1 prompt without the exact ROUND 2 verdict subject', {E + 'PROMPT': G + '/neg_prompt_nosubject.txt'}, 23, None),
        ('N2 brief without TIER 1', {E + 'BRIEF': G + '/neg_brief_notier.md'}, 7, None),
        ('N3 brief without the head SHA', {E + 'BRIEF': G + '/neg_brief_nosha.md'}, 20, None),
        ('N4 prompt without MAIL YOUR VERDICT', {E + 'PROMPT': G + '/neg_prompt_nomail.txt'}, 12, None),
        ('N5 prompt without node_modules per ENTRY', {E + 'PROMPT': G + '/neg_prompt_nofarm.txt'}, 22, None),
        ('N6 head override = cbe29597d (the round-1 head)', {E + 'HEAD': 'cbe29597d11e59f2e1a14519e9ba3dbf6de9a756'}, 6, None),
        ('N7 develop = the round-2 head (auth.ts 7c985bdce LANDED)', {E + 'CUR_DEV': H}, 19, 'round-2 own'),
        ('N8 develop = cbe29597d, the round-1 head (auth.ts 8fbe102eb LANDED)', {E + 'CUR_DEV': 'cbe29597d11e59f2e1a14519e9ba3dbf6de9a756'}, 19, 'round-1 own'),
        ('N9 develop = 7e89318bc, pre-#1014 (verification.ts nobody pinned)', {E + 'CUR_DEV': '7e89318bcedbc9a35757d4298ace54a6a23020bd'}, 18, 'verification.ts'),
        ('N10 develop auth.ts moved INTO its region (fixture)', {E + 'AUTH_FILE': G + '/neg_auth_into_region.ts'}, 18, 'region changed'),
        ('N11 develop rateLimitEnforce.ts: the bucket line moved (fixture)', {E + 'RLE_FILE': G + '/neg_rle_into_region.ts'}, 18, 'region changed'),
        ('N12 develop index.ts moved INTO the limiter region (fixture)', {E + 'INDEX_FILE': G + '/neg_index_into_limiter_region.ts'}, 18, 'region changed'),
        ('N13 develop index.ts gained one line ABOVE the ks781 pins (fixture)', {E + 'INDEX_FILE': G + '/neg_index_pins_shifted.ts'}, 18, 'pin lines moved'),
        ('N14 develop auth.ts = the round-2 head bytes (fixture, LANDED arm)', {E + 'AUTH_FILE': G + '/src/H.middleware_auth.ts'}, 19, 'round-2 own'),
        ('P15 POSITIVE: develop auth.ts moved OUTSIDE its region must PASS', {E + 'AUTH_FILE': G + '/pos_auth_outside_region.ts'}, 0, 'moved OUTSIDE'),
        ('P16 POSITIVE: develop rateLimitEnforce.ts moved OUTSIDE its region must PASS', {E + 'RLE_FILE': G + '/pos_rle_outside_region.ts'}, 0, 'moved OUTSIDE'),
        ('P17 POSITIVE: develop index.ts moved OUTSIDE the region AFTER the pins must PASS', {E + 'INDEX_FILE': G + '/pos_index_outside_region_after_pins.ts'}, 0, 'pins 846/859/892 hold'),
        ('N18 prompt without the round-2 report directory', {E + 'PROMPT': G + '/neg_prompt_noreportdir.txt'}, 24, None),
        ('N19 prompt without NOT-TESTED.written-first.md', {E + 'PROMPT': G + '/neg_prompt_nonottested.txt'}, 24, None),
        ('N20 prompt without the ROUND-1 REPORT path', {E + 'PROMPT': G + '/neg_prompt_nor1report.txt'}, 24, None),
        ('N21 brief without the ROUND-1 REPORT path', {E + 'BRIEF': G + '/neg_brief_nor1report.md'}, 24, None),
        ('N22 brief without the MERGE ADDENDUM', {E + 'BRIEF': G + '/neg_brief_noaddendum.md'}, 25, None),
        ('N23 brief without CLOSED / STILL OPEN / NEW', {E + 'BRIEF': G + '/neg_brief_nodisposition.md'}, 25, None),
        ('N24 brief without ROUND 2', {E + 'BRIEF': G + '/neg_brief_noround2.md'}, 15, None),
        ('N25 round-1 override name QA1017_CUR_DEV = the head is IGNORED (the renamed hook must not honour the old name) -> PASS', {'QA1017_CUR_DEV': H}, 0, 'origin develop still')]
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
print('end', now('+%H:%M:%S %Z'))
