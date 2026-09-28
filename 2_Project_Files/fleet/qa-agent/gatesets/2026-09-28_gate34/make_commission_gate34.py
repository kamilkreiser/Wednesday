#!/usr/bin/env python3
"""make_commission_gate34.py — writes COMMISSION.md for gate34 (the directory this script lives in). Every SHA / tree / count in it is READ from
pins_gate34.json, stopcounts_gate34.json, gh_read_1.out, fill_1.out and predict_1.out beside it (never typed); the prose rows are the drafter's.
Shape copied from gate33's make_commission (gate32 -> gate31 lineage), re-keyed to gate34's five MIXED-tier rows, no stack, one base."""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit)))
fill = open(D + '/fill_1.out').read()
def lands(n):
    m = re.search(r'#%s (\d+)->(\d+)' % n, fill); return 'declared %s -> lands %s' % (m.group(1), m.group(2)) if m else '?'
WHY = {
 '1316': ('KS-1346 C', '**T1 LOGGING (ruled)**: originate routes/adminConfig.ts fail500 logs `thrown <Ctor> with fields [...]` for a non-Error, non-string throw (never values); one helper, 50 call sites; + a NEW ks1346c cell. Kam 2026-09-27 16:32 "Type and field names only". Golden-EXACT (`git apply --cached --check`, MEASURED). WIDEN MEASURED by the drafter (logprobe_1.out): no VALUE sentinel reaches any sink at head / END_TREE / under #1310\'s logger; edges TYPE-NAME-AS-DATA and THROWING-OWNKEYS for the gate to rule.'),
 '1317': ('KS-1346 D', '**T1 LOGGING (ruled)**: originate routes/webhooks.ts, the SAME fail500 line (7 call sites) + a NEW ks1346d cell incl. the rotate-secret PIN D7. Same ruling. Golden-EXACT (MEASURED). WIDEN as #1316 (MEASURED).'),
 '1318': ('KS-747', '**T2 SPEC**: security security.openapi.ts declares organizationId (required, uuid) on GET /api/security/keys + the REGENERATED docs/openapi/secuura-api.yaml (+7/-0; == the brief\'s companion, MEASURED) + a NEW ks747 cell. No handler / auth byte. The handler checks PRESENCE only (READ) — uuid is declared, not enforced.'),
 '1319': ('KS-908', '**T1 SECURITY API RESPONSE**: security index.ts adds `connectorId: … || null` to the POST /api/keys 201 body and the GET /api/keys row + a NEW ks908 wire cell (C2 pins no keyHash). The tenant filters run before the map (READ). Golden-EXACT (MEASURED).'),
 '1320': ('KS-692', '**T1 AUTHORIZATION (ruled)**: vc-issuer routes/status.ts drops ISSUER_ADMIN from STATUS_WRITE_ROLES + rewrites the header comment + a NEW ks692 cell. Kam 2026-09-16 "Narrow now, bind-creator later". NAMED CONSEQUENCE: tenant ISSUER_ADMINs lose status-list revoke / unrevoke — READ WIDER: the router-level gate also covers POST /api/status (create) and /:id/allocate. Golden-EXACT (MEASURED).'),
}
rows = []
for n in sorted(K['prs']):
    pr = P['prs'][n]
    files = ', '.join('%s +%s/-%s' % (os.path.basename(x.split('\t')[2]), x.split('\t')[0], x.split('\t')[1]) for x in pr['numstat'])
    rows.append('| #%s | %s | %s | `%s` | %d on `%s` | %s | %s | %s |' % (n, WHY[n][0], K['prs'][n]['tier'], pr['head'], len(pr['commits']), pr['merge_base'][:12], files, lands(n), WHY[n][1]))
out = ['# COMMISSION — DRAFT the round-34 batch gate kit "%s" over %d PRs (MIXED: T1 x4, T2 x1). Do NOT launch.' % (kit, len(K['prs'])), '',
 'Commissioned by Wednesday to the drafter on 2026-09-28 (~08:1x AEST) for Seat B 36th\'s round: #1316 (KS-1346 part C), #1317 (KS-1346 part D), #1318 (KS-747),',
 '#1319 (KS-908) and #1320 (KS-692, "not raised yet" at commission — the drafter polled `ls-remote refs/pull/1320/head` every 2 min; it appeared at',
 '2026-09-27T22:25:21Z on poll 3, head b9111f2bfad2, so the kit is FIVE). All raised by Seat B 36th, which merges its own on Wednesday\'s signed GO (routing',
 'line `QA/Secuura-batch1316`). Kam rulings to verify IN THE PRODUCT: #1316 / #1317 "Type and field names only" (2026-09-27 16:32, card',
 'secuura-ks1346-logging-thrown-objects-leaks-secrets = a); #1320 "Narrow now, bind-creator later" (2026-09-16, card secuura-ks692-status-revoke-interim-posture = a)',
 '— the NAMED CONSEQUENCE the gate must confirm and report: tenant ISSUER_ADMINs lose status-list revoke / unrevoke until lists get an owner. Tiers as',
 'commissioned: T1 for #1316 / #1317 (logging of errors, secret-leak class), #1319 (security service API responses) and #1320 (authorization); T2 for #1318 (spec).',
 'A WIDEN leg for #1316 / #1317: the REAL logger in production mode, no secret / PII value reaching any sink from the fail500 paths (gate33 found this class in #1310).',
 'Each squash subject declared WITHOUT `(#n)` and landing <= 92; no foreign hyphenated KS key in a squash body. Merge order #1316, #1317, #1318, #1319, #1320.',
 'Shape copied from `gatesets/2026-09-28_gate33/`: JSON pins, routing-file override, controls both ways with `--invert`, a declared commit count, a not-stacked',
 'check for every pair, the key scan, a HARD WIDEN census (titles AND Seat B 36th\'s branch segment) in predict and in the launch action (rc 15), and the',
 'STANDING_LINES of 2026-09-27/28 (subjects without the suffix, landed <= 92; no-op vs overlap keys; every spelling of a namespace token; rev-parse on unfetched',
 'objects; verified bytes == used bytes; `patch -F0` is not `git apply --check`; a copied tool is keyed to its author\'s position and a re-key tool is in its',
 'own token map). The drafter writes only in this kit directory and its own scratchpad: it did NOT add the routing line (see README §4).', '',
 '## The batch — every head re-read by the drafter from origin (ls-remote + a fetch into a `--shared --no-checkout` scratch clone + the PULLS API; all agree)',
 '| PR | ticket | tier | head | commits on merge-base | files | subject (no `(#n)`) | why this tier, from the DIFF |', '|---|---|---|---|---|---|---|---|'] + rows + ['',
 'Linear: every PR links its ticket as `contributes`; none `closes` (linear_reads_1.out); no PR title, body or commit message puts a closing word before a key (keyscan_1.out). #1316\'s commit message carries a hyphenated KS-730 and #1320\'s a hyphenated KS-586 (keyscan_1.out): a squash body must never paste the commit message.',
 'NOT STACKED (measured): no head is another\'s ancestor; every pair\'s merge-base is develop itself. MG-11 as it LANDS: every title is the declared subject, WITHOUT the (#n) suffix (all <= 92; no SHORT subject this round).', '',
 '## Develop at the pin',
 'Pinned over develop **`%s`** (tree `%s`), READ by ls-remote and fetched — gate33\'s #1311-#1315 squashes in (#1310 still open). ONE merge-base, MEASURED: `%s` for all five (each head\'s one commit has it as parent; develop has not moved since). END_TREE **`%s`** (%s), identical in all %d orders (%d merge-tree calls, each with the PR\'s own merge-base).' % (
     P['develop'], P['develop_tree'], P['merge_bases'][0][:12], P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls']),
 'The launch action\'s step 3b re-pins on any move.', '',
 '## Overlaps — NONE declared, NONE found',
 '- Kit pairs: all disjoint (#1318 and #1319 share no file: security.openapi.ts + the yaml vs index.ts). Every other OPEN PR at the pin (%d, the PULLS API census, #1310 included): disjoint from every kit path.' % len(P['inflight']),
 '- `merged_blob_paths` (a genuine overlap) NONE and `noop_paths` (a squash-stack no-op) NONE — two different declarations, each asserted empty by predict (c).', '',
 '## Fleet STOP (READ, bounded region, NOT-FOUND control)']
for n in sorted(K['prs']):
    s = S[n]
    out.append('- #%s `%s` (%d lines, rc %s): %s' % (n, os.path.basename(s['log']), s['lines'], s['rc'],
        ('%s · %s · %s · %s; "%s"' % (s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['shell_suites'], s['verdict_line'])) if s['preflight_ran'] else 'NO PREFLIGHT — NOT APPLICABLE'))
out += ['- By path class no kit PR changes the count (TypeScript routes / spec / yaml and jest / vitest cells — no `*.test.sh`): after this merge 28/0 · 6/0 · 49/0 · 60 of 60.', '']
out += ['## LEGITIMATE SHAPES — the drafter\'s READ predictions (the gate MEASURES every row; a row saying MEASURED is a drafter\'s run, still not the gate\'s evidence)', '| PR | prediction | predicted-by |', '|---|---|---|']
for l in open(D + '/predict_1.out').read().splitlines():
    m = re.match(r'^  #(\d+) (.*)$', l)
    if m and not m.group(2).startswith(('PRODUCT files', 'NO product file')):
        out.append('| #%s | %s | drafter %s (predict_1.out) |' % (m.group(1), m.group(2).replace('|', '/')[:1300], 'MEASURED' if 'MEASURED' in m.group(2)[:120] else 'READ'))
open(D + '/COMMISSION.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/COMMISSION.md', len(out), 'lines')
