#!/usr/bin/env python3
"""drafter_pools_table_1032r2.py — prints the pool-routing rows (out/rows_pools_mt{off,on}_<tree>_test.json) per tree."""
import json
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-18_gate1032r2'
for mt in ('off', 'on'):
    for t in ('head', 'r1', 'dev'):
        d = json.load(open('%s/out/rows_pools_mt%s_%s_test.json' % (GS, mt, t)))
        print('MT=%s TREE=%s SETUP %s' % (mt, t, d['setup']))
        for r in d['rows']:
            print('  ROW %-34s %s' % (r['id'], {k: r['armInfo'].get(k) for k in ('tenantManager', 'getPoolTENANT')} if t == 'head' else ''))
            print('     approve %s "%s" | after approve: request %s level %s' % (r['status'], r['message'][:60], r['afterApprove']['request'], r['afterApprove']['level']))
            if t == 'head': print('     seq', ' > '.join(r['seq']))
            print('     errors', [e[:90] for e in r['errorLines']], '| warns', [w[:60] for w in r['warnLines']])
            print('     then reject %s "%s" | request %s level %s' % (r['thenReject']['status'], r['thenReject']['message'], r['thenReject']['request'], r['thenReject']['level']))
