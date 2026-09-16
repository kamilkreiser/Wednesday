#!/usr/bin/env python3
"""probe_table.py — tabulate probe_rows_{head,base,merged}.json (drafter probe, recording only)."""
import json, sys
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1010'
for t in ('head', 'base', 'merged'):
    for r in json.load(open(G + '/probe_rows_%s.json' % t)):
        if r['id'] == 'EXPORT': print(t, 'EXPORT ORIGINATE_FORWARD_TIMEOUT_MS =', r.get('ORIGINATE_FORWARD_TIMEOUT_MS', 'ABSENT')); continue
        f = r['first']; s = r.get('second')
        print('%-6s %-36s b=%-20s -> %-11s %5dms hitsA %d delA %d | hitsF %d delF %d created %d kept %s inst %s | 2nd %s | err %s | unh %s | census %s' % (t, r['id'], r['bound'], f['status'], f['ms'], r['hitsAtAnswer'], r['deletesAtAnswer'], r['hitsFinal'], r['deletesFinal'], r['created'], r['pendingKept'], r['instance'], (s['status'], s['body'][:50]) if s else '-', [(e['dtFromCall'], (e['err'] or '')[:45]) for e in r['errorLogs']], r['unhandled'], {k: v for k, v in r['censusAfter'].items() if k != 'PipeWrap'}))
        if f['status'] == 502 and 'MARKER' in f['body']: print('   !! 502 body carries originate marker')
