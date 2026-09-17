#!/usr/bin/env python3
"""controls_check.py — prove the #1024 launcher guards FIRE: each negative runs the launcher with --check ONLY (stdin /dev/null) and a QA1024_* override
pointing at a mutated copy under out/controls/; the fixture arms feed develop documents.ts variants through QA1024_DOCS_FILE. Never a launch."""
import os, subprocess, hashlib, datetime
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1024'; CD = GS + '/out/controls'; os.makedirs(CD, exist_ok=True)
QA = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent'
L = QA + '/launchers/launch_qa_secuura_ks1202_1024.sh'; B = QA + '/briefs/2026-09-17_secuura-1024-ks1202-tier1.md'; PR = QA + '/briefs/2026-09-17_secuura-1024-ks1202-tier1.prompt.txt'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'; DOCS = 'Blockchain/Dev/services/originate/src/routes/documents.ts'
brief = open(B).read(); prompt = open(PR).read()
print('controls_check', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| launcher sha256', hashlib.sha256(open(L, 'rb').read()).hexdigest()[:16])
def mut(name, text, old, new):
    n = text.count(old); assert n >= 1, (name, old); p = CD + '/' + name; open(p, 'w').write(text.replace(old, new)); return p, n
def run(label, env, want):
    p = subprocess.run([L, '--check'], stdin=subprocess.DEVNULL, capture_output=True, text=True, env=dict(os.environ, **env))
    last = (p.stderr.strip().splitlines() or [''])[0][:170]
    print('%-4s %-44s rc %-3d want %-3d %s | %s' % ('OK' if p.returncode == want else 'SLIP', label, p.returncode, want, 'FIRES' if p.returncode == want else '', last or p.stdout.strip().splitlines()[-1][:120]))
    return p.returncode == want
res = []
p, n = mut('neg_brief_notier.md', brief, 'TIER 1', 'TIER X'); res.append(run('brief without TIER 1 (x%d)' % n, {'QA1024_BRIEF': p}, 7))
p, n = mut('neg_prompt_noround.txt', prompt, 'ROUND 1', 'ROUND X'); res.append(run('prompt without ROUND 1 (x%d)' % n, {'QA1024_PROMPT': p}, 15))
p, n = mut('neg_brief_nosha.md', brief, 'd1a3280880d85ff31fd409aa1b5a16c428c4bb9a', 'd1a328088'); res.append(run('brief without the full head SHA (x%d)' % n, {'QA1024_BRIEF': p}, 20))
p, n = mut('neg_prompt_nomail.txt', prompt, 'MAIL YOUR VERDICT', 'SEND YOUR VERDICT'); res.append(run('prompt without MAIL YOUR VERDICT', {'QA1024_PROMPT': p}, 12))
p, n = mut('neg_prompt_nofarm.txt', prompt, 'node_modules per ENTRY', 'node_modules by ENTRY'); res.append(run('prompt without per-ENTRY farm', {'QA1024_PROMPT': p}, 22))
p, n = mut('neg_prompt_nosubject.txt', prompt, '[QA -> Wednesday] TIER 1 GATE #1024 (KS-1202) d1a328088', '[QA -> Wednesday] TIER 1 GATE #1024 (KS-1202)'); res.append(run('prompt without the exact subject', {'QA1024_PROMPT': p}, 23))
p, n = mut('neg_prompt_noreportdir.txt', prompt, 'reports/2026-09-17-ks1202-1024-d1a328088-tier1-r1/', 'reports/somewhere-else/'); res.append(run('prompt without the report dir', {'QA1024_PROMPT': p}, 24))
p, n = mut('neg_prompt_nonottested.txt', prompt, 'NOT-TESTED.written-first.md', 'NOT-TESTED.md'); res.append(run('prompt without NOT-TESTED.written-first.md', {'QA1024_PROMPT': p}, 24))
p, n = mut('neg_brief_noaddendum.md', brief, 'MERGE ADDENDUM', 'MERGE NOTE'); res.append(run('brief without MERGE ADDENDUM', {'QA1024_BRIEF': p}, 25))
res.append(run('head override (a different SHA)', {'QA1024_HEAD': '0' * 40}, 6))
dev = subprocess.run(['git', '-C', REPO, 'show', '581c9db0db4201c42cbbf702f339b750989acdb1:' + DOCS], capture_output=True).stdout.decode()
head = subprocess.run(['git', '-C', REPO, 'show', 'd1a3280880d85ff31fd409aa1b5a16c428c4bb9a:' + DOCS], capture_output=True).stdout.decode()
def fx(name, text): p = CD + '/' + name; open(p, 'w').write(text); return p
res.append(run('fixture: develop bytes exactly', {'QA1024_DOCS_FILE': fx('pos_docs_develop_exact.ts', dev)}, 0))
res.append(run('fixture: #1024 head bytes (LANDED)', {'QA1024_DOCS_FILE': fx('neg_docs_head_LANDED.ts', head)}, 19))
res.append(run('fixture: edit OUTSIDE the regions (clears)', {'QA1024_DOCS_FILE': fx('pos_docs_outside_regions.ts', dev + '\n// qa1024 control: a move outside every region\n')}, 0))
a = "      const docType: string = documentType || rawType || 'DOCUMENT';\n"; assert dev.count(a) == 1
res.append(run('fixture: edit INSIDE the create region', {'QA1024_DOCS_FILE': fx('neg_docs_into_create_region.ts', dev.replace(a, a + '      // qa1024 control: a move into the create region\n'))}, 18))
v = "const ALLOWED_VERSION_ACTIONS = ["; assert dev.count(v) == 1; vi = dev.index(v); w = dev.index("      const metadata = (req.body.metadata", vi)
res.append(run('fixture: edit INSIDE the /version writer region', {'QA1024_DOCS_FILE': fx('neg_docs_into_version_region.ts', dev[:w] + '      // qa1024 control: a move into the version writer\n' + dev[w:])}, 18))
g = "          documentType: (d.data?.documentType as string) || d.type,\n"; assert dev.count(g) == 1
res.append(run('fixture: the list reader changed', {'QA1024_DOCS_FILE': fx('neg_docs_list_reader.ts', dev.replace(g, "          documentType: d.type,\n"))}, 18))
print('controls fired as wanted: %d / %d' % (sum(res), len(res)))
