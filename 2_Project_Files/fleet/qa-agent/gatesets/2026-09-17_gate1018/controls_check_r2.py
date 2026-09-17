#!/usr/bin/env python3
"""controls_check_r2.py — prove the #1018 ROUND 2 launcher guards FIRE (round-2 copy of controls_check.py): each negative runs the launcher with --check ONLY (stdin /dev/null) and a QA1018_* override
pointing at a mutated copy under out_r2/controls/; the fixture arms feed develop auth routes/users.ts variants through QA1018_USERS_FILE. Never a launch."""
import os, subprocess, hashlib, datetime
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1018'; CD = GS + '/out_r2/controls'; os.makedirs(CD, exist_ok=True)
QA = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent'
L = QA + '/launchers/launch_qa_secuura_ks1050_1018.sh'; B = QA + '/briefs/2026-09-17_secuura-1018-ks1050-tier2-r2.md'; PR = QA + '/briefs/2026-09-17_secuura-1018-ks1050-tier2-r2.prompt.txt'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'; USERS = 'Blockchain/Dev/services/auth/src/routes/users.ts'
brief = open(B).read(); prompt = open(PR).read()
print('controls_check', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| launcher sha256', hashlib.sha256(open(L, 'rb').read()).hexdigest()[:16])
def mut(name, text, old, new):
    n = text.count(old); assert n >= 1, (name, old); p = CD + '/' + name; open(p, 'w').write(text.replace(old, new)); return p, n
def run(label, env, want):
    p = subprocess.run([L, '--check'], stdin=subprocess.DEVNULL, capture_output=True, text=True, env=dict(os.environ, **env))
    last = (p.stderr.strip().splitlines() or [''])[0][:170]
    print('%-4s %-48s rc %-3d want %-3d %s | %s' % ('OK' if p.returncode == want else 'SLIP', label, p.returncode, want, 'FIRES' if p.returncode == want else '', last or p.stdout.strip().splitlines()[-1][:120]))
    return p.returncode == want
res = []
p, n = mut('neg_brief_notier.md', brief, 'TIER 2', 'TIER X'); res.append(run('brief without TIER 2 (x%d)' % n, {'QA1018_BRIEF': p}, 7))
p, n = mut('neg_prompt_tier1.txt', prompt, 'TIER 2', 'TIER 1'); res.append(run('prompt says TIER 1 (x%d)' % n, {'QA1018_PROMPT': p}, 7))
p, n = mut('neg_prompt_noround.txt', prompt, 'ROUND 2', 'ROUND X'); res.append(run('prompt without ROUND 2 (x%d)' % n, {'QA1018_PROMPT': p}, 15))
p, n = mut('neg_brief_nosha.md', brief, 'efd677e98c917a52f8af442c9fcfde756166070e', 'efd677e98'); res.append(run('brief without the full head SHA (x%d)' % n, {'QA1018_BRIEF': p}, 20))
p, n = mut('neg_prompt_nomail.txt', prompt, 'MAIL YOUR VERDICT', 'SEND YOUR VERDICT'); res.append(run('prompt without MAIL YOUR VERDICT', {'QA1018_PROMPT': p}, 12))
p, n = mut('neg_prompt_nopushban.txt', prompt, 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout', 'Avoid pushing from the Secuura checkout'); res.append(run('prompt without the push ban', {'QA1018_PROMPT': p}, 11))
p, n = mut('neg_prompt_nofarm.txt', prompt, 'node_modules per ENTRY', 'node_modules by ENTRY'); res.append(run('prompt without per-ENTRY farm', {'QA1018_PROMPT': p}, 22))
p, n = mut('neg_prompt_nosubject.txt', prompt, '[QA -> Wednesday] TIER 2 GATE #1018 ROUND 2 (KS-1050) efd677e98', '[QA -> Wednesday] TIER 2 GATE #1018 (KS-1050) efd677e98'); res.append(run('prompt without the exact subject', {'QA1018_PROMPT': p}, 23))
p, n = mut('neg_prompt_noreportdir.txt', prompt, 'reports/2026-09-17-ks1050-1018-efd677e98-tier2-r2/', 'reports/somewhere-else/'); res.append(run('prompt without the report dir', {'QA1018_PROMPT': p}, 24))
p, n = mut('neg_prompt_nonottested.txt', prompt, 'NOT-TESTED.written-first.md', 'NOT-TESTED.md'); res.append(run('prompt without NOT-TESTED.written-first.md', {'QA1018_PROMPT': p}, 24))
p, n = mut('neg_brief_noaddendum.md', brief, 'MERGE ADDENDUM', 'MERGE NOTE'); res.append(run('brief without MERGE ADDENDUM', {'QA1018_BRIEF': p}, 25))
res.append(run('head override (a different SHA)', {'QA1018_HEAD': '0' * 40}, 6))
res.append(run('develop override: not ahead of the pin (UNJUDGEABLE)', {'QA1018_CUR_DEV': 'efaaa6034f036dd9538ee35b189217b1d08b90a9'}, 18))
dev = subprocess.run(['git', '-C', REPO, 'show', '19f1e54750ce2b65312a687add2db4f5628edb7d:' + USERS], capture_output=True).stdout.decode()
head = subprocess.run(['git', '-C', REPO, 'show', 'efd677e98c917a52f8af442c9fcfde756166070e:' + USERS], capture_output=True).stdout.decode()
r1 = subprocess.run(['git', '-C', REPO, 'show', '267bd8624ce276ca62160216d042b8477bac52f1:' + USERS], capture_output=True).stdout.decode()
def fx(name, text): p = CD + '/' + name; open(p, 'w').write(text); return p
res.append(run('fixture: develop bytes exactly', {'QA1018_USERS_FILE': fx('pos_users_develop_exact.ts', dev)}, 0))
res.append(run('fixture: #1018 round-2 head bytes (LANDED)', {'QA1018_USERS_FILE': fx('neg_users_head_LANDED.ts', head)}, 19))
res.append(run('fixture: #1018 round-1 bytes (LANDED)', {'QA1018_USERS_FILE': fx('neg_users_r1_LANDED.ts', r1)}, 19))
res.append(run('fixture: edit OUTSIDE the regions (clears)', {'QA1018_USERS_FILE': fx('pos_users_outside_regions.ts', dev + '\n// qa1018 control: a move outside every region\n')}, 0))
a = "    const updated = await userRepo.updateUser(user.id, updates);\n"; assert dev.count(a) == 1
res.append(run('fixture: edit INSIDE the PATCH /me region', {'QA1018_USERS_FILE': fx('neg_users_into_patch_region.ts', dev.replace(a, a + '    // qa1018 control: a move into the PATCH /me region\n'))}, 18))
i = "import { BadRequestError, NotFoundError, ServiceUnavailableError, ValidationError } from '../middleware/errorHandler';"; assert dev.count(i) == 1
res.append(run('fixture: the errorHandler import line changed', {'QA1018_USERS_FILE': fx('neg_users_import_line.ts', dev.replace(i, "import { AppError, BadRequestError, NotFoundError, ServiceUnavailableError, ValidationError } from '../middleware/errorHandler';"))}, 18))
print('controls fired as wanted: %d / %d' % (sum(res), len(res)))
