#!/usr/bin/env python3
"""drafter_gctrl.py — #1011 ROUND 2: the gate's CONTROL tamper G-CTRL on head, whole api-gateway suite (denominator asserted 50/417), project tsc rc,
anchor count 1 + marker, restore sha-identical. Edit: every ADMITTED row's details.path becomes '/qa-tampered'. PREDICTION: 3 red — Part A CONTROL,
real-app POST /api/logs, real-app POST /api/v1/logs (each asserts an admitted row's path)."""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drafterlib import *
G = T['head']; GWD = G + '/' + PKG['gw']; AUD = GWD + '/src/middleware/audit.ts'; AUD_REL = PKG['gw'] + '/src/middleware/audit.ts'
P('drafter_gctrl start', ts()); pa = sha(AUD)
edit(AUD, "            path: auditPath, // KS-871: was req.path, the trimmed remainder for a refused request\n",
          "            path: res.statusCode < 400 ? '/qa-tampered' : auditPath, // KS-871: was req.path, the trimmed remainder for a refused request\n", [("'/qa-tampered'", 1)])
rc = subprocess.run([G + '/Blockchain/Dev/node_modules/.bin/tsc', '--noEmit', '-p', '.'], cwd=GWD, capture_output=True, text=True).returncode
P('project tsc rc', rc)
r = vitest('r2_GCTRL', 'head', 'gw'); assert (r['files'], r['tests']) == (50, 417), (r['files'], r['tests'])
P('G-CTRL failed', r['failed'], 'pending', r['pending'])
restore('head', AUD_REL, pa)
P('drafter_gctrl end', ts())
