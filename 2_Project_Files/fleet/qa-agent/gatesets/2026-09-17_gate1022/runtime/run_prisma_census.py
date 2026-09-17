#!/usr/bin/env python3
"""run_prisma_census.py — originate RUNTIME install (npm ci --omit=dev, head, drafter scratch): does the prisma CLI shipped there load hono?
`prisma --version` and `prisma migrate --help` with the census preload (no DB, no network expected). Control: `node -e import('hono')` same census."""
import os, subprocess, datetime
CL = open('/private/tmp/claude-501/drafter1022/CLONE_PATH').read().strip(); RT = os.path.dirname(os.path.abspath(__file__))
d = CL + '/orig-omitdev'; cli = d + '/node_modules/prisma/build/index.js'
for tag, args in (('version', [cli, '--version']), ('migrate_help', [cli, 'migrate', '--help']), ('dev_help', [cli, 'dev', '--help']), ('control_import_hono', ['--input-type=module', '-e', "await import('hono')"])):
    census = RT + '/out/census_prisma_%s.txt' % tag; open(census, 'w').close()
    env = dict(os.environ, CENSUS_OUT=census, PRISMA_HIDE_UPDATE_MESSAGE='1', CHECKPOINT_DISABLE='1'); env.pop('NODE_OPTIONS', None)
    t0 = datetime.datetime.now().astimezone().strftime('%H:%M:%S')
    p = subprocess.run(['node', '--import', RT + '/census.mjs'] + args, cwd=d, env=env, capture_output=True, text=True, timeout=90)
    lines = [l for l in open(census).read().splitlines() if not l.startswith('#')]
    print('%s rc %d %s | census urls %d | hono %d | @hono/node-server %d | @prisma/dev %d | prisma/build %d | out: %s' % (tag, p.returncode, t0, len(lines),
          sum('/node_modules/hono/' in l for l in lines), sum('/@hono/node-server/' in l for l in lines), sum('/@prisma/dev/' in l for l in lines),
          sum('/prisma/build/' in l for l in lines), (p.stdout + p.stderr).strip().replace('\n', ' | ')[:160]))
