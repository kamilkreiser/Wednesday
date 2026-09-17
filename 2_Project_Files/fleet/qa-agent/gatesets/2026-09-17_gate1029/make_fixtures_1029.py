#!/usr/bin/env python3
"""make_fixtures_1029.py — write the --check control fixtures for check_launcher_1029.sh under GS/controls/: develop / LANDED / unpinned bytes of the ks1072
test (git show from the Secuura checkout, READ verb; blob asserted) and one-mutation copies of the brief and prompt (each mutation's anchor count asserted >= 1
and the mutated text asserted to no longer carry the guarded string). Never rm."""
import hashlib, os, subprocess
GS = os.path.dirname(os.path.abspath(__file__)); CD = GS + '/controls'; os.makedirs(CD, exist_ok=True)
QA = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent'
B = QA + '/briefs/2026-09-17_secuura-1029-ks1180p1-tier2.md'; PR = QA + '/briefs/2026-09-17_secuura-1029-ks1180p1-tier2.prompt.txt'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
TF = 'Blockchain/Dev/services/api-gateway/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts'
def blob(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()
def show(ref): return subprocess.run(['git', '-C', REPO, 'show', ref + ':' + TF], capture_output=True).stdout
dev = show('75ad0e55c6335a5f34f6d0b74dfe00b334b2eb2e'); head = show('cd3580e1f7c6d00ac2ff05d2f3703460feaf34cc')
assert blob(dev) == '4ad1cdcd1e45044efdbb0b8e4e6eaf358453d780' and blob(head) == 'd9c98320ea64638c3ab5ef2f35c102aba6d1207a'
for name, data in (('pos_test_develop_4ad1cdcd1.ts', dev), ('neg_test_landed_d9c98320e.ts', head), ('neg_test_unpinned.ts', dev + b'\n// qa1029 control: a develop move of the guarded test\n')):
    open(CD + '/' + name, 'wb').write(data); print('fixture', name, blob(data)[:9])
brief = open(B).read(); prompt = open(PR).read()
def mut(name, text, old, new, gone):
    n = text.count(old); assert n >= 1, (name, old); t = text.replace(old, new); assert gone not in t, (name, 'guarded string survived')
    open(CD + '/' + name, 'w').write(t); print('mutation', name, 'x%d' % n)
S = '[QA -> Wednesday] TIER 2 GATE #1029 (KS-1180) cd3580e1f'
mut('neg_brief_notier2.md', brief, 'TIER 2', 'TIER X', 'TIER 2')
mut('neg_prompt_round2.txt', prompt, 'ROUND 1', 'ROUND 2', 'ROUND 1')
mut('neg_brief_nosha.md', brief, 'cd3580e1f7c6d00ac2ff05d2f3703460feaf34cc', 'cd3580e1f', 'cd3580e1f7c6d00ac2ff05d2f3703460feaf34cc')
mut('neg_prompt_nomail.txt', prompt, 'MAIL YOUR VERDICT', 'SEND YOUR VERDICT', 'MAIL YOUR VERDICT')
mut('neg_prompt_nofarm.txt', prompt, 'node_modules per ENTRY', 'node_modules by ENTRY', 'node_modules per ENTRY')
mut('neg_prompt_nosubject.txt', prompt, S, '[QA -> Wednesday] TIER 2 GATE #1029 cd3580e1f', S)
mut('neg_brief_nosubject.md', brief, S, '[QA -> Wednesday] TIER 2 GATE #1029 cd3580e1f', S)
mut('neg_prompt_nottestedfirst.txt', prompt, 'NOT-TESTED.written-first.md', 'NOT-TESTED.md', 'NOT-TESTED.written-first.md')
mut('neg_brief_noaddendum.md', brief, 'MERGE ADDENDUM', 'MERGE NOTE', 'MERGE ADDENDUM')
mut('neg_prompt_noprobe.txt', prompt, 'probe files OUTSIDE services/', 'probe files outside src/__tests__/', 'probe files OUTSIDE services/')
