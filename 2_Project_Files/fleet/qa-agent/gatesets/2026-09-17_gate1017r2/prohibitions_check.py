#!/usr/bin/env python3
"""prohibitions_check.py — every standing-prohibition phrase of the #1017 ROUND-1 prompt, checked in the round-1 prompt (CONTROL: each must be present there)
AND in the round-2 prompt. The list = the round-1 set's 53 phrases (its prohibitions_check.py, imported by reading, not retyped) + the round-1 prompt's
gate-specific holds added for #1017 (Redis, listeners, KS-1187, UNHANDLED_REJECTION_MODE, index.ts pins, zsh modifier). Whitespace normalised.
A negative control: the same check on a copy of the round-2 prompt with one phrase removed must report exactly that phrase missing."""
import re, subprocess
B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/'
R1CHK = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1017/prohibitions_check.py'
n = lambda t: re.sub(r'\s+', ' ', t)
src = open(R1CHK).read(); i = src.index('PH = ['); j = src.index("]\nprint('prohibitions_check'")
ns = {}; exec(src[i:j + 1], ns); PH = list(ns['PH'])
EXTRA = ['NO real Redis, not even in-process', 'a vi.mock\'d getRedisClient returning an in-process async fake is allowed as a LABELLED substitute',
 'ANY LISTENER YOUR RUNS START, YOU END: identify it by port + cwd, SIGTERM that pid, never a pattern kill', 'quote an lsof TCP LISTEN census at start and close',
 'Do NOT probe absolute-form request targets (KS-1187 is a Kam-held card).', 'Set UNHANDLED_REJECTION_MODE=survive before importing',
 'Never edit index.ts for a probe (its line numbers are pinned by packages/shared); mount probes on a bare app.', '`"$VAR:path"` applies history modifiers (write `"${VAR}:path"`)',
 'Node runs only with cwd inside your clone', 'RSA keys, sk_ strings and JWTs in your probe are THROWAWAY, generated per run.',
 'if refs/pull/1017/head moves, STOP', 'Build the body from a template file with no shell interpolation and assert the backtick spans survived.',
 'NOT-TESTED.written-first.md written FIRST, BEFORE any run', 'the verdict MAIL is the END STATE']
PH = PH + EXTRA
r1 = n(open(B + '2026-09-17_secuura-1017-ks1195-tier1.prompt.txt').read()); r2raw = open(B + '2026-09-17_secuura-1017r2-ks1195-tier1.prompt.txt').read(); r2 = n(r2raw)
print('prohibitions_check', subprocess.run(['date', '+%Y-%m-%d %H:%M:%S %Z'], capture_output=True, text=True).stdout.strip(), '| phrases', len(PH), '(round-1 list', len(ns['PH']), '+ extra', len(EXTRA), ')')
miss1 = [x for x in PH if n(x) not in r1]; miss2 = [x for x in PH if n(x) not in r2]
print('CONTROL absent from the ROUND-1 prompt (must be []):', miss1)
print('absent from the ROUND-2 prompt (must be []):', miss2)
neg = r2.replace(n('never enter any seat'), 'enter what you need', 1)
print('negative control (one phrase removed from a copy): reported missing =', [x for x in PH if n(x) not in neg])
print('round-2 subject exact:', '[QA -> Wednesday] TIER 1 GATE #1017 ROUND 2 (KS-1195) a067d4e3e — <GO | GO WITH FINDINGS | NO GO>' in r2raw, '| first line ultrathink:', r2raw.split('\n')[0] == 'ultrathink', '| round-1 subject absent:', '(KS-1195) cbe29597d —' not in r2raw)
