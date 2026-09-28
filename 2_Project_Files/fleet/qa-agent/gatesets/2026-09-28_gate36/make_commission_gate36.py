#!/usr/bin/env python3
"""make_commission_gate36.py — writes COMMISSION.md for gate36 (the directory this script lives in). Every SHA / tree / count in it is READ from
pins_gate36.json, stopcounts_gate36.json, emitprobe_gate36.json, fill_1.out and predict_1.out beside it (never typed); the prose rows are the drafter's.
Shape copied from gate35's make_commission (gate34 -> gate33 lineage), re-keyed to gate36's four rows (T1 x2, T2 x2), no stack, one base."""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit))); EP = json.load(open('%s/emitprobe_%s.json' % (D, kit)))
fill = open(D + '/fill_1.out').read()
def lands(n):
    m = re.search(r'#%s (\d+)->(\d+)' % n, fill); return 'declared %s -> lands %s' % (m.group(1), m.group(2)) if m else '?'
WHY = {
 '1323': ('KS-1129 item 4 LIVESCAN', '**T1 VERIFY-CLAIM**: api-gateway routes/verification.ts — the LIVE chain-scan read (anchoring\'s GET /api/anchors/verify/:hash) gets the three shape guards KS-1069 gave the persisted read: `j.verified === true && !j.simulated`; a string txHash without the tx_sim_ / mock_tx_ / tx_ prefixes; a positive integer height, a numeric string refused. It changes what a verifier is TOLD (`verified`, `verificationConfidence`, the on-chain badge). Spark READY; golden strict-apply blob-exact (MEASURED); the +/- lines SLIDE-EQUAL to the READY (an insertion slide in the test file). READ: the guards only narrow; a hash-passes / height-refused reply echoes `source: cardano-live` beside a persisted height (MIXED-ECHO); "held surface" (09-25 comment) unresolved.'),
 '1324': ('KS-1124 O1 MINTMERGE', '**T1 BLOB-WRITE (data-destruction class)**: originate routes/documents.ts — the thread-token cache write at document create re-reads the document (`getDocument(...).catch(() => null)`) and spreads the blob AS PERSISTED, not the create-time copy, so an anchor accept persisted first keeps txHash / status / anchorId. It NARROWS the race and does not close it: (R1) the read-then-write window; (R2) the MIRROR — the create-path anchor-accept and anchor_failed writes still replace the column wholesale and erase a threadToken that landed first; (R3) a rejecting read falls back to the create-time copy. Flag-gated (STATE_THREAD_NFT_ENABLED). Spark READY; golden strict-apply blob-exact (MEASURED); SLIDE-EQUAL to the READY.'),
 '1325': ('KS-1227 witness', '**T2 TEST-ONLY**: the ks1072 anchor-store witness keeps "count every stub request" (fails closed), a comment records the decision, and its message says ASKED; R1\'s toContain follows it (a shorter prefix). Seat-written (no READY). Cell count 8 -> 8 (READ). The try/finally detach and R2 are already at develop.'),
 '1326': ('KS-1351 item 1 (+ item 2)', '**T2 TYPES-ONLY**: packages/shared vc/types.ts declares `revoked` / `revokedAt` / `revocationReason` (optional) on a NEW SecuuraCredentialStatus extends VCCredentialStatus and narrows SecuuraCredential.credentialStatus to it; vc-issuer credentialRepo.ts:95 `let` -> `const`. Seat-written (no READY). The EMIT, MEASURED by the drafter (emitprobe_1.out): %s — controls %s. The gate owes TS2339 4 -> 0 with packages/shared REBUILT, and nothing new in any consumer.' % (EP['_summary'][:220], 'all behaved' if all(EP['_controls'].values()) else EP['_controls'])),
}
rows = []
for n in sorted(K['prs']):
    pr = P['prs'][n]
    files = ', '.join('%s +%s/-%s' % (os.path.basename(x.split('\t')[2]), x.split('\t')[0], x.split('\t')[1]) for x in pr['numstat'])
    rows.append('| #%s | %s | %s | `%s` | %d on `%s` | %s | %s | %s |' % (n, WHY[n][0], K['prs'][n]['tier'], pr['head'], len(pr['commits']), pr['merge_base'][:12], files, lands(n), WHY[n][1]))
out = ['# COMMISSION — DRAFT the round-36 batch gate kit "%s" over %d PRs (T1 x2 + T2 x2). Do NOT launch.' % (kit, len(K['prs'])), '',
 'Commissioned by Wednesday to the drafter on 2026-09-28 (~18:00 AEST) for Seat B 38th\'s round: #1323 (KS-1129 livescan), #1324 (KS-1124 mintmerge), #1325',
 '(KS-1227) and #1326 (KS-1351 item 1), all on Secuura\'s `develop` d9ce1403d158 (read by ls-remote at 18:00 AEST; re-read at pin). All four raised by Seat B',
 '38th, which merges its own on Wednesday\'s signed GO — the GO SUBJECT must name "Seat B 38th", with no `#` before the PR numbers (routing line',
 '`QA/Secuura-batch1323`). #1323 changes what a verifier is TOLD — propose T1 unless the tiers lesson says otherwise; runtime-check it through the real route',
 'with simulated, mock and string-height replies. #1324 narrows the overwrite race and does NOT close it — the gate says what remains; tier per the lesson.',
 '#1325 is test-only. #1326 is type-only: it must show the TS2339 errors gone and nothing new, and no runtime change. Merge order #1323 -> #1324 -> #1325 ->',
 '#1326. Compute END_TREE in the drafter\'s own clone (all orders if feasible). Controls both ways (normal all OK; inverted all MISMATCH). Subjects declared',
 'WITHOUT `(#n)`, each landing <= 92 (declared + 8), own key only; name any commit messages that must not be pasted. Shape copied from',
 '`gatesets/2026-09-28_gate35/`: JSON pins, routing-file override, controls both ways with `--invert`, a declared commit count, a not-stacked check, the key',
 'scan, a HARD WIDEN census (titles AND Seat B 38th\'s branch segment) in predict and in the launch action (rc 15), and the STANDING_LINES of 2026-09-27/28.',
 'The drafter writes only in this kit directory and its own scratchpad: it did NOT add the routing line (README §4).', '',
 '## The batch — every head re-read by the drafter from origin (ls-remote + a fetch into a `--shared --no-checkout` scratch clone + the PULLS API; all agree)',
 '| PR | ticket | tier | head | commits on merge-base | files | subject (no `(#n)`) | why this tier, from the DIFF |', '|---|---|---|---|---|---|---|---|'] + rows + ['',
 'Tiers per 0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md: T1 = security surfaces, data destruction and erasure, anything deploying to dev / demo; T2 = tests-only, docs, config/CI, follow-ups of a gated mechanism, style. #1323 is a verification-claim surface the demo\'s badge reads (T1); #1324\'s defect ERASED persisted anchor fields (data destruction, T1); #1325 tests-only (T2); #1326 types-only, T2 ON CONDITION that no runtime change is measured (it types a revocation field; key revocation is a T1 surface).',
 'Linear: all four PRs link their ticket as `contributes`; none `closes` (linear_reads_1.out); no PR title, body or commit message puts a closing word before a key, and none carries a FOREIGN hyphenated key (keyscan_1.out) — no commit message must be withheld on MG-3 grounds; the merger still composes each squash body (all four messages end in a Co-Authored-By trailer; #1325\'s test file carries a hyphenated KS-1180 as content).',
 'NOT STACKED (measured): no head is another\'s ancestor; every pair\'s merge-base is develop itself. MG-11 as it LANDS: each title is the declared subject, WITHOUT the (#n) suffix (all <= 92; no SHORT subject this round).', '',
 '## Develop at the pin',
 'Pinned over develop **`%s`** (tree `%s`), READ by ls-remote and fetched — gate35\'s #1321 / #1322 squashes in (MERGED). ONE merge-base, MEASURED: `%s` for all four (each head\'s one commit has it as parent; develop has not moved since). END_TREE **`%s`** (%s), identical in all %d orders (%d merge-tree calls, each with the PR\'s own merge-base).' % (
     P['develop'], P['develop_tree'], P['merge_bases'][0][:12], P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls']),
 'The launch action\'s step 3b re-pins on any move.', '',
 '## Overlaps — NONE declared, NONE found',
 '- Kit: four disjoint path sets (#1323 and #1325 share the api-gateway SERVICE, not a file — the gate runs the api-gateway suite on END_TREE). Every other OPEN PR at the pin (%d, the PULLS API census): disjoint from every kit path.' % len(P['inflight']),
 '- `merged_blob_paths` (a genuine overlap) NONE and `noop_paths` (a squash-stack no-op) NONE — two different declarations, each asserted empty by predict (c).', '',
 '## Fleet STOP (READ, bounded region, NOT-FOUND control)']
for n in sorted(K['prs']):
    s = S[n]
    out.append('- #%s `%s` (%d lines, rc %s): %s' % (n, os.path.basename(s['log']), s['lines'], s['rc'],
        ('%s · %s · %s · %s; "%s"' % (s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['shell_suites'], s['verdict_line'])) if s['preflight_ran'] else 'NO PREFLIGHT — NOT APPLICABLE'))
out += ['- By path class no kit PR changes the count (TypeScript routes / a type / a repository and vitest / jest cell files — no `*.test.sh`): after this merge 28/0 · 6/0 · 49/0 · 60 of 60.', '']
out += ['## LEGITIMATE SHAPES — the drafter\'s READ predictions (the gate MEASURES every row; a row saying MEASURED is a drafter\'s run, still not the gate\'s evidence)', '| PR | prediction | predicted-by |', '|---|---|---|']
for l in open(D + '/predict_1.out').read().splitlines():
    m = re.match(r'^  #(\d+) (.*)$', l)
    if m and not m.group(2).startswith(('PRODUCT files', 'NO product file')):
        out.append('| #%s | %s | drafter %s (predict_1.out) |' % (m.group(1), m.group(2).replace('|', '/')[:1300], 'MEASURED' if 'MEASURED' in m.group(2)[:120] else 'READ'))
open(D + '/COMMISSION.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/COMMISSION.md', len(out), 'lines')
