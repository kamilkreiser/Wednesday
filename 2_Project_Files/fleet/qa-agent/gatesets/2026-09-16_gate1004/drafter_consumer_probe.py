#!/usr/bin/env python3
"""drafter_consumer_probe.py — run qa1004-drafter-consumer.test.ts SOLO in the clone's originate, then quarantine it by rename."""
import json, os, shutil, subprocess, datetime
SCR = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/9aed5a67-2729-4892-b685-13ab87142a58/scratchpad'
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-16_gate1004'
P = json.load(open(SCR + '/gate1004_draft_paths.json')); C = P['C']; O = C + '/Blockchain/Dev/services/originate'
dst = O + '/src/__tests__/qa1004-drafter-consumer.test.ts'; shutil.copyfile(G + '/qa1004-drafter-consumer.test.ts', dst)
e = dict(os.environ); e['QA1004_OUT'] = G + '/consumer_probe_head.json'
print(datetime.datetime.now().astimezone().strftime('%H:%M:%S'), 'start')
p = subprocess.run(['npx', 'jest', 'src/__tests__/qa1004-drafter-consumer.test.ts'], cwd=O, env=e, capture_output=True, text=True, timeout=300)
print(datetime.datetime.now().astimezone().strftime('%H:%M:%S'), 'rc', p.returncode); print(p.stderr[-1500:])
os.rename(dst, dst + '.quarantined')
print(open(G + '/consumer_probe_head.json').read() if os.path.exists(G + '/consumer_probe_head.json') else 'NO OUTPUT')
