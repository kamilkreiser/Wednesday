#!/usr/bin/env python3
"""Gate 81 mutants on routes/auth.ts (wt_head). Each mutant = list of (old,new) each of which must match exactly once.
Runs vitest on the author's 2 files + gate81-probe, records which files fail, restores by sha256."""
import hashlib, subprocess, sys, re, pathlib
W = pathlib.Path('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate81-ks1885-auth-1896')
SRC = W / 'wt_head/Blockchain/Dev/services/auth/src/routes/auth.ts'
VT = W / 'scripts/vt.sh'
CB = "logger.warn('Social callback: the provider code exchange failed', { provider: providerName,"
LK = "logger.warn('Social link: the provider code exchange failed', { provider: providerName,"
M = {
 'G1_anchors_dropped': [("/^(Apple", "/(Apple"), ("/^Failed", "/Failed"), ("no access token)\\)$/,", "no access token)\\)/,"), ("\\))?$/,", "\\))?/,")],
 'G2_m_flag': [("no access token)\\)$/,", "no access token)\\)$/m,"), ("\\))?$/,", "\\))?$/m,")],
 'G3_apperror_widened_to_Error': [("if (err instanceof AppError) return err.message;", "if (err instanceof Error) return err.message;")],
 'G4_callback_log_has_message': [(CB, CB + " message: (exchangeErr as any)?.message,")],
 'G5_link_log_has_message': [(LK, LK + " message: (exchangeErr as any)?.message,")],
 'G6_end_anchor_dropped': [("no access token)\\)$/,", "no access token)\\)/,"), ("\\))?$/,", "\\))?/,")],
 'G7_start_anchor_dropped': [("/^(Apple", "/(Apple"), ("/^Failed", "/Failed")],
 'G8_link_always_rethrows_raw': [("if (authoredExchangeText(exchangeErr) !== null) throw exchangeErr;", "throw exchangeErr;")],
 'G9_link_neutral_error_with_cause': [("throw new Error('social link: the provider code exchange failed');", "throw new Error('social link: the provider code exchange failed', { cause: exchangeErr });")],
 'G10_typeof_check_dropped': [("return typeof message === 'string' && ADAPTER_EXCHANGE_TEXTS.some((re) => re.test(message)) ? message : null;", "return ADAPTER_EXCHANGE_TEXTS.some((re) => re.test(String(message))) ? String(message) : null;")],
 'G11_errorName_unbounded': [("/^[A-Za-z][A-Za-z0-9_]{0,63}$/.test(name) ? name : 'unnamed'", "name ? name : 'unnamed'")],
 'G12_status_group_widened': [("(HTTP \\d{3}|no access token)", "(HTTP [^)]*|no access token)")],
 'G13_empty_fallback_old_text': [("${authored ?? EXCHANGE_FAILED_TEXT}", "${authored || (exchangeErr as any)?.message || 'invalid authorization code'}")],
 'G14_g_flag': [("no access token)\\)$/,", "no access token)\\)$/g,"), ("\\))?$/,", "\\))?$/g,")],
 'G15_callback_status_502': [("throw new BadRequestError(`OAuth authentication failed: ${authored ?? EXCHANGE_FAILED_TEXT}`);", "throw new AppError(`OAuth authentication failed: ${authored ?? EXCHANGE_FAILED_TEXT}`, 502, 'BAD_REQUEST');")],
 'G16_link_catch_removed_entirely': [("      if (authoredExchangeText(exchangeErr) !== null) throw exchangeErr;\n", "      throw exchangeErr;\n")],
}
FILES = ['src/__tests__/ks1885-callback-real-adapters-never-echo-an-unauthored-exchange-error.test.ts', 'src/__tests__/ks1885-exchange-error-allowlist-is-exact.test.ts', 'src/__tests__/gate81-probe.test.ts']
sel = sys.argv[1:] or list(M)
orig = SRC.read_bytes(); h0 = hashlib.sha256(orig).hexdigest()
summary = []
for name in sel:
    text = orig.decode()
    ok = True
    for old, new in M[name]:
        n = text.count(old)
        if n != 1:
            print(f'{name}: pattern matched {n} times, NOT RUN: {old!r}'); ok = False; break
        text = text.replace(old, new)
    if not ok: summary.append((name, 'NOT_RUN', '')); continue
    SRC.write_text(text)
    log = W / f'logs/mut_{name}.log'
    try:
        rc = subprocess.run([str(VT), 'head', str(log), '--reporter=verbose', *FILES]).returncode
    finally:
        SRC.write_bytes(orig)
        assert hashlib.sha256(SRC.read_bytes()).hexdigest() == h0, 'RESTORE FAILED'
    body = log.read_bytes().decode('utf-8', 'replace')
    tests = re.findall(r'Tests\s+(.*?)\n', body)
    failed_files = sorted({f.split('/')[-1].split('.test')[0] for f in re.findall(r'FAIL\s+(src/__tests__/\S+\.test\.ts)', body)})
    author_killed = any(f.startswith('ks1885') for f in failed_files)
    probe_killed = 'gate81-probe' in failed_files
    verdict = 'KILLED(author)' if author_killed else ('KILLED(probe only)' if probe_killed else ('SURVIVED' if rc == 0 else 'rc!=0 no FAIL?'))
    summary.append((name, verdict, f'rc={rc} tests: {tests[-1] if tests else "?"} failing files: {failed_files}'))
    print(name, verdict, summary[-1][2], flush=True)
print('restore sha256', hashlib.sha256(SRC.read_bytes()).hexdigest(), 'expected', h0)
print('\nSUMMARY'); [print(*s, sep=' | ') for s in summary]
