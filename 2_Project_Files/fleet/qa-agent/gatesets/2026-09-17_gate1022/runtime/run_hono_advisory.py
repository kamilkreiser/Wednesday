#!/usr/bin/env python3
"""run_hono_advisory.py — runs probe_hono_advisory.mjs (a copy inside img-<tree>/prod) on base then head; bounded 60 s each; compares."""
import json, os, subprocess, datetime
RT = os.path.dirname(os.path.abspath(__file__)); CL = open('/private/tmp/claude-501/drafter1022/CLONE_PATH').read().strip()
for tree in ('base', 'head'):
    cwd = CL + '/img-%s/prod' % tree; local = cwd + '/.qa1022_probe_hono_advisory.mjs'
    open(local, 'w').write(open(RT + '/probe_hono_advisory.mjs').read())
    out = RT + '/out/probe_D_%s.json' % tree
    t0 = datetime.datetime.now().astimezone().strftime('%H:%M:%S')
    p = subprocess.run(['node', local], cwd=cwd, env=dict(os.environ, OUT=out), capture_output=True, text=True, timeout=60)
    os.rename(local, local + '.ran')
    print('probe D', tree, 'rc', p.returncode, t0, p.stderr[-800:])
    if os.path.exists(out): print(json.dumps(json.load(open(out)), indent=1))
