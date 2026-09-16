#!/usr/bin/env python3
"""drafter_setup.py — build a scratch clone at the #1004 head for the drafter's feasibility probes.
Write verbs ONLY inside a fresh mktemp -d under the drafting scratchpad. The Secuura checkout gets `git clone --shared` (a read).
node_modules farm: per-ENTRY symlinks FROM the checkout, EXCEPT @secuura, which is a real dir whose links point INTO THE CLONE
(the checkout's @secuura/shared -> ../../packages/shared would otherwise resolve to the CHECKOUT's stale dist)."""
import os, subprocess, sys, tempfile, datetime, json
SRC = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H = '6d077d3fe35cd5f3c09d394553d320e97b1abe32'
SCR = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/9aed5a67-2729-4892-b685-13ab87142a58/scratchpad'
now = lambda: datetime.datetime.now().astimezone().strftime('%H:%M:%S')
W = tempfile.mkdtemp(prefix='gate1004_draft_', dir=SCR); C = W + '/clone'
def run(cmd, cwd=None, env=None):
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    print(now(), 'rc', p.returncode, ' '.join(cmd)[:160]); 
    if p.returncode: print(p.stdout[-2000:], p.stderr[-2000:])
    return p
print(now(), 'workdir', W)
run(['git', 'clone', '--shared', '--no-checkout', '-q', SRC, C])
run(['git', '-C', C, 'checkout', '-q', '--detach', H])
print('clone HEAD', run(['git', '-C', C, 'rev-parse', 'HEAD']).stdout.strip())
SD = SRC + '/Blockchain/Dev'; CD = C + '/Blockchain/Dev'
os.makedirs(CD + '/node_modules')
n = 0
for e in os.listdir(SD + '/node_modules'):
    if e == '@secuura': continue
    os.symlink(SD + '/node_modules/' + e, CD + '/node_modules/' + e); n += 1
os.makedirs(CD + '/node_modules/@secuura')
for e in os.listdir(SD + '/node_modules/@secuura'):
    os.symlink(os.readlink(SD + '/node_modules/@secuura/' + e), CD + '/node_modules/@secuura/' + e)
print('farmed', n, 'entries; @secuura relinked into the clone:', len(os.listdir(CD + '/node_modules/@secuura')))
for sub in ['packages/shared', 'services/originate', 'services/m365-integration', 'services/api-gateway']:
    if os.path.isdir(SD + '/' + sub + '/node_modules'):
        os.symlink(SD + '/' + sub + '/node_modules', CD + '/' + sub + '/node_modules')
p = run(['node', '-e', "console.log(require('fs').realpathSync(require.resolve('@secuura/shared')))"], cwd=CD + '/services/originate')
print('resolve @secuura/shared from clone originate ->', p.stdout.strip(), '| inside clone:', p.stdout.strip().startswith(C))
p = run(['npx', 'tsc', '-p', 'packages/shared'], cwd=CD)
print('dist ssrf-guard.js exists', os.path.exists(CD + '/packages/shared/dist/security/ssrf-guard.js'),
      'contains Promise.race', 'Promise.race' in open(CD + '/packages/shared/dist/security/ssrf-guard.js').read())
json.dump({'W': W, 'C': C}, open(SCR + '/gate1004_draft_paths.json', 'w'))
