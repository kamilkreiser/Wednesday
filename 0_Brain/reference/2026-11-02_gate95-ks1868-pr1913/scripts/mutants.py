#!/usr/bin/env python3
# Gate 95 mutants: each mutant edits ONE site of the head product webhooks.ts, tests untouched; the three new test files
# run; the product is restored from git and sha256-checked after every run.
import hashlib, json, re, subprocess, sys

G = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate95-ks1868-pr1913'
R = G + '/repo'
P = R + '/Blockchain/Dev/services/billing/src/routes/webhooks.ts'
HEAD = subprocess.run(['git', '-C', R, 'show', 'pr1913:Blockchain/Dev/services/billing/src/routes/webhooks.ts'],
                      capture_output=True, text=True, check=True).stdout
HSHA = hashlib.sha256(HEAD.encode()).hexdigest()

P1 = """      let reason: string;
      try {
        reason = String(error);
      } catch {
        reason = 'unreadable thrown value';
      }
      logger.error('Webhook signature verification failed', { error: reason });"""
P2 = """      let reason: string;
      try {
        reason = error instanceof Error ? error.message : String(error);
      } catch {
        reason = 'unreadable thrown value';
      }
      logger.error('[Webhook] Refusing delivery — idempotency unavailable', {"""
P3 = """      let message: string;
      try {
        message = error instanceof Error ? error.message : String(error);
      } catch {
        message = 'unreadable thrown value';
      }
      logger.error(`[Webhook] Error handling ${event.type}:`, { error: message });"""
for s in (P1, P2, P3):
    assert HEAD.count(s) == 1, s[:60]

def m(site, old, new):
    assert site.count(old) == 1, (old, site[:40])
    return site.replace(old, new)

V = {'P1': 'reason', 'P2': 'reason', 'P3': 'message'}
EXPR = {'P1': 'String(error)', 'P2': 'error instanceof Error ? error.message : String(error)',
        'P3': 'error instanceof Error ? error.message : String(error)'}
SRC = {'P1': P1, 'P2': P2, 'P3': P3}

def mutants(site):
    s, v, e = SRC[site], V[site], EXPR[site]
    out = {
        'M0_drop_guard': None,
        'M2_fallback_rereads': m(s, f"{v} = 'unreadable thrown value';", f"{v} = String(error);"),
        'M3_rethrow_unreadable': m(s, f"{v} = 'unreadable thrown value';", "throw error;"),
        'M4_constant_for_all': m(s, f"{v} = {e};", f"{v} = 'unreadable thrown value';"),
        'M5_log_removed': None,
        'M7_unreadable_returns_silently': m(s, f"{v} = 'unreadable thrown value';", f"{v} = 'unreadable thrown value'; return;"),
    }
    # M0: the base expression, unguarded
    lines = s.split('\n')
    log_from = [i for i, l in enumerate(lines) if 'logger.error' in l][0]
    if site == 'P3':
        out['M0_drop_guard'] = f"      const message = {e};\n" + '\n'.join(lines[log_from:])
    else:
        out['M0_drop_guard'] = '\n'.join(lines[log_from:]).replace(f"error: {v}", f"error: {e}") if site == 'P1' else None
    if site == 'P2':
        # base shape: no guard, inline expression in the log call (the log's 'error: reason,' is outside SRC)
        out['M0_drop_guard'] = '\n'.join(lines[log_from:])  # guard lines removed; fix the later reference below
    # M5: the log call removed (P3: the template log line; P1: the single line; P2: replace call with a no-op)
    if site == 'P1':
        out['M5_log_removed'] = '\n'.join(lines[:log_from])
    elif site == 'P3':
        out['M5_log_removed'] = '\n'.join(lines[:log_from])
    else:
        out['M5_log_removed'] = '\n'.join(lines[:log_from]) + "\n      void (0 as any) && logger.error('[Webhook] Refusing delivery — idempotency unavailable', {"
    if site != 'P1':
        out['M6_nonError_branch_x'] = m(s, ": String(error);\n      } catch", ": 'x';\n      } catch")
    return out

def apply(site, name, new):
    text = HEAD.replace(SRC[site], new)
    if site == 'P2' and name == 'M0_drop_guard':
        text = text.replace("        eventType: event.type,\n        error: reason,\n",
                            "        eventType: event.type,\n        error: error instanceof Error ? error.message : String(error),\n", 1)
    assert text != HEAD
    return text

rows = []
only = sys.argv[1:]
for site in ('P1', 'P2', 'P3'):
    for name, new in mutants(site).items():
        key = f'{site}__{name}'
        if only and key not in only:
            continue
        text = apply(site, name, new)
        open(P, 'w').write(text)
        # parse check via esbuild from the clone
        pc = subprocess.run([R + '/Blockchain/Dev/node_modules/.bin/esbuild', '--loader=ts', '--log-level=error'],
                            input=text, capture_output=True, text=True)
        log = f'{G}/logs/mut_{key}.log'
        rc = subprocess.run(['bash', G + '/scripts/vt.sh', log, 'ks1868-billing-webhook-stripe']).returncode
        body = open(log).read()
        failed = sorted(set(re.findall(r'(?:×|FAIL)\s+.*?(?:> )?((?:control|RED) ks1868 [CR]\d)', body)))
        files_failed = sorted(set(re.findall(r'FAIL\s+src/__tests__/(ks1868-billing-webhook-stripe-\w+)', body)))
        assertion = 'AssertionError' in body
        open(P, 'w').write(HEAD)
        restore = hashlib.sha256(open(P, 'rb').read()).hexdigest() == HSHA
        row = dict(mutant=key, parse_rc=pc.returncode, vitest_rc=rc, verdict='KILLED' if rc != 0 else 'SURVIVED',
                   failed_cells=failed, failed_files=files_failed, assertion=assertion, restore=restore)
        rows.append(row)
        print(json.dumps(row), flush=True)
        if not restore:
            sys.exit('RESTORE FAILED')
open(G + '/logs/mutants_table.jsonl', 'a').write(''.join(json.dumps(r) + '\n' for r in rows))
