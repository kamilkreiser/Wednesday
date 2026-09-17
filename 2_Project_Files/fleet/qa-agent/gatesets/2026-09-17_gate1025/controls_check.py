#!/usr/bin/env python3
"""controls_check.py — negative controls for launch_qa_secuura_ks528_1025.sh, --check ONLY (never a bare launch).
Each control plants one defect through the launcher's own test overrides (QA1025_HEAD / QA1025_BRIEF / QA1025_PROMPT), or, for the TTY guard,
a mutated COPY in the session scratchpad run with --check. Every planted file asserts its anchor was removed before it is used."""
import os, subprocess, datetime
Q = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent'
GS = Q + '/gatesets/2026-09-17_gate1025'
L = Q + '/launchers/launch_qa_secuura_ks528_1025.sh'
SCR = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/430a6175-31ee-4c21-bf1d-f73226d5ecde/scratchpad'
BRIEF = Q + '/briefs/2026-09-17_secuura-1025-ks528-tier2.md'
PROMPT = Q + '/briefs/2026-09-17_secuura-1025-ks528-tier2.prompt.txt'
HEAD = '9954a7069a16987da140654337555c9a13268b1f'
SUBJECT = '[QA -> Wednesday] TIER 2 GATE #1025 (KS-528) 9954a7069 — <GO | GO WITH FINDINGS | NO GO>'

def plant(src, dst, old, new=''):
    s = open(src, encoding='utf-8').read()
    assert old in s, 'anchor absent: %r' % old[:40]
    t = s.replace(old, new)
    assert old not in t, 'anchor survived: %r' % old[:40]
    open(dst, 'w', encoding='utf-8').write(t)
    return dst

p_nosubj = plant(PROMPT, GS + '/neg_prompt_nosubject.txt', SUBJECT, '[QA -> Wednesday] TIER 2 GATE #1025 — <GO>')
p_nont = plant(PROMPT, GS + '/neg_prompt_nonottested.txt', 'NOT-TESTED.written-first.md', 'a not-tested file')
p_noadd = plant(PROMPT, GS + '/neg_prompt_noaddendum.txt', 'MERGE ADDENDUM', 'merge note')
p_nomail = plant(PROMPT, GS + '/neg_prompt_nomail.txt', 'MAIL YOUR VERDICT', 'Report your verdict')
b_nosha = plant(BRIEF, GS + '/neg_brief_nosha.md', HEAD, '9954a7069')
b_notier = plant(BRIEF, GS + '/neg_brief_notier2.md', 'TIER 2', 'TIER two')
s = open(L, encoding='utf-8').read()
tty = [l for l in s.split('\n') if l.startswith('[ -t 0 ] || ')]
assert len(tty) == 1
notty = SCR + '/neg_launcher_notty_1025.sh'
open(notty, 'w', encoding='utf-8').write(s.replace(tty[0] + '\n', ''))
assert '[ -t 0 ]' not in open(notty, encoding='utf-8').read()

cases = [
    ('head override', L, {'QA1025_HEAD': '0' * 40}, 6),
    ('prompt without the exact subject', L, {'QA1025_PROMPT': p_nosubj}, 23),
    ('prompt without NOT-TESTED.written-first.md', L, {'QA1025_PROMPT': p_nont}, 23),
    ('prompt without MERGE ADDENDUM', L, {'QA1025_PROMPT': p_noadd}, 23),
    ('prompt without MAIL YOUR VERDICT', L, {'QA1025_PROMPT': p_nomail}, 12),
    ('brief without the full head SHA', L, {'QA1025_BRIEF': b_nosha}, 20),
    ('brief without TIER 2', L, {'QA1025_BRIEF': b_notier}, 7),
    ('launcher copy without the TTY guard', notty, {}, 22),
]
print(datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'), 'controls, --check only')
allok = True
for name, launcher, env, want in cases:
    p = subprocess.run(['bash', launcher, '--check'], env=dict(os.environ, **env), capture_output=True, text=True, stdin=subprocess.DEVNULL)
    ref = [l for l in p.stderr.splitlines() if l.startswith('REFUSING')]
    ok = p.returncode == want
    allok &= ok
    print('%-45s exit %2d (want %d) %s | %s' % (name, p.returncode, want, 'OK' if ok else 'MISMATCH', (ref[0] if ref else p.stderr.strip()[:120])[:150]))
print('all controls as expected:', allok)
print(datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
