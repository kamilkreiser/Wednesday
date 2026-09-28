#!/usr/bin/env python3
"""make_commission_gate35.py — writes COMMISSION.md for gate35 (the directory this script lives in). Every SHA / tree / count in it is READ from
pins_gate35.json, stopcounts_gate35.json, logprobe_gate35.json, fill_1.out and predict_1.out beside it (never typed); the prose rows are the drafter's.
Shape copied from gate34's make_commission (gate33 -> gate32 lineage), re-keyed to gate35's two T1 rows, no stack, one base."""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit))); LP = json.load(open('%s/logprobe_%s.json' % (D, kit)))
fill = open(D + '/fill_1.out').read()
def lands(n):
    m = re.search(r'#%s (\d+)->(\d+)' % n, fill); return 'declared %s -> lands %s' % (m.group(1), m.group(2)) if m else '?'
W = LP['_widen']
WHY = {
 '1321': ('KS-1348 r3', '**T1 LOGGING (ruled)**: originate utils/logger.ts keeps r2\'s Console redaction and adds a `keepFileFields` allow-list on BOTH production File transports (timestamp, level, service, message, requestId, method, path, statusCode; `error` only when a string) + a NEW ks1348 cell. Kam 2026-09-28 06:58 "Third attempt: allow-list the file format". REPLACES the CLOSED #1310 (gate33 NO GO, LOG-FILE WIDEN). Golden-EXACT (`git apply --cached --check`, MEASURED). WIDEN MEASURED by the drafter (logprobe_1.out): VALUE sentinels in a file at the head %s; message + error text kept %s; userId / documentId / ip / stack %s; stdout still carries the nested-Error / toJSON / unnamed-key values, NEW vs develop: %s.' % (
     W['head_files'], W['head_text_kept'], W['head_loss'], W['stdout_new_vs_develop'])),
 '1322': ('KS-888 mint', '**T1 SECURITY (ruled)**: security index.ts — `dbSaveApiKey(k, { rethrow })` opt-in; POST /api/keys drops the unsaved key and answers 503 SERVICE_UNAVAILABLE (SQLSTATE 08/53/57, socket / pool faults) or 500 INTERNAL_ERROR, no key material + a NEW ks888 cell. Kam 2026-09-28 06:58 "Fix all three routes" (card secuura-ks888-failed-key-save-design = b) — this PR is the MINT ONLY; revoke / validate UNCHANGED, pending the OPEN card secuura-ks888-revoke-validate-on-failed-save. Golden-EXACT (MEASURED; the golden\'s three blank-line -/+ pairs net out). READ: only the mint opts in; a failed save returns before the rotate revoke (KS-577 order kept); the memory-only mint still answers 201; the spec ALREADY declares 503 on the mint (a seat prediction slip).'),
}
rows = []
for n in sorted(K['prs']):
    pr = P['prs'][n]
    files = ', '.join('%s +%s/-%s' % (os.path.basename(x.split('\t')[2]), x.split('\t')[0], x.split('\t')[1]) for x in pr['numstat'])
    rows.append('| #%s | %s | %s | `%s` | %d on `%s` | %s | %s | %s |' % (n, WHY[n][0], K['prs'][n]['tier'], pr['head'], len(pr['commits']), pr['merge_base'][:12], files, lands(n), WHY[n][1]))
out = ['# COMMISSION — DRAFT the round-35 batch gate kit "%s" over %d PRs (T1 x2). Do NOT launch.' % (kit, len(K['prs'])), '',
 'Commissioned by Wednesday to the drafter on 2026-09-28 (~14:10 AEST) for Seat B 37th\'s round: #1321 (KS-1348 r3) and #1322 (KS-888 mint), both on Secuura\'s',
 '`develop` 54f37d6399bd (read by ls-remote when the commission was written; re-read at pin). Both raised by Seat B 37th, which merges its own on Wednesday\'s',
 'signed GO — the GO SUBJECT must name "Seat B 37th" (routing line `QA/Secuura-batch1321`). Kam rulings to verify IN THE PRODUCT: #1321 "Third attempt: allow-list',
 'the file format" (2026-09-28 06:58, card secuura-ks1348-r2-files-still-leak-allowlist = a); #1322 "Fix all three routes" (2026-09-28 06:58, card',
 'secuura-ks888-failed-key-save-design = b) — this PR is the MINT route only; revoke and validate are UNCHANGED (still log-only; a separate card is pending).',
 'The gate MUST repeat gate33\'s LOG-FILE WIDEN measurement through the REAL logger at NODE_ENV=production (a nested Error with config.headers.Authorization and a',
 'response token, toJSON, and the unnamed secret / PII keys secretKey, privateKey, passwordHash, mnemonic, phone, email_address, userEmails[], ip), confirm no value',
 'reaches either file or stdout, and that the message and error text still reach the files; it states the disclosed loss (userId, documentId, ip, stack no longer',
 'in the files) as a consequence. For #1322 it verifies at runtime: no `sk_` in any refused body; the unsaved key is not listed and does not validate; revoke and',
 'validate answer as before under a failing INSERT (no unhandled rejection, no process exit); the no-database memory-only mint still answers 201; the KS-577 order',
 '(mint first, then revoke) still holds on the rotate path. Each squash subject declared WITHOUT `(#n)` and landing <= 92; no foreign hyphenated KS key in a squash',
 'body. Merge order #1321, then #1322. Shape copied from `gatesets/2026-09-28_gate34/`: JSON pins, routing-file override, controls both ways with `--invert`, a declared',
 'commit count, a not-stacked check for the pair, the key scan, a HARD WIDEN census (titles AND Seat B 37th\'s branch segment) in predict and in the launch action',
 '(rc 15), and the STANDING_LINES of 2026-09-27/28. The drafter writes only in this kit directory and its own scratchpad: it did NOT add the routing line (README §4).', '',
 '## The batch — every head re-read by the drafter from origin (ls-remote + a fetch into a `--shared --no-checkout` scratch clone + the PULLS API; all agree)',
 '| PR | ticket | tier | head | commits on merge-base | files | subject (no `(#n)`) | why this tier, from the DIFF |', '|---|---|---|---|---|---|---|---|'] + rows + ['',
 'Linear: both PRs link their ticket as `contributes`; none `closes` (linear_reads_1.out); no PR title, body or commit message puts a closing word before a key, and none carries a FOREIGN hyphenated key (keyscan_1.out) — no commit message must be withheld on MG-3 grounds; the merger still composes each squash body.',
 'NOT STACKED (measured): neither head is the other\'s ancestor; their merge-base is develop itself. MG-11 as it LANDS: each title is the declared subject, WITHOUT the (#n) suffix (both <= 92; no SHORT subject this round).', '',
 '## Develop at the pin',
 'Pinned over develop **`%s`** (tree `%s`), READ by ls-remote and fetched — gate34\'s #1316-#1320 squashes in; #1310 CLOSED unmerged. ONE merge-base, MEASURED: `%s` for both (each head\'s one commit has it as parent; develop has not moved since). END_TREE **`%s`** (%s), identical in all %d orders (%d merge-tree calls, each with the PR\'s own merge-base).' % (
     P['develop'], P['develop_tree'], P['merge_bases'][0][:12], P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls']),
 'The launch action\'s step 3b re-pins on any move.', '',
 '## Overlaps — NONE declared, NONE found',
 '- Kit pair: disjoint (originate logger.ts + its cell vs security index.ts + its cell). Every other OPEN PR at the pin (%d, the PULLS API census): disjoint from every kit path. #1322\'s index.ts co-file #1319 is MERGED (in the base).' % len(P['inflight']),
 '- `merged_blob_paths` (a genuine overlap) NONE and `noop_paths` (a squash-stack no-op) NONE — two different declarations, each asserted empty by predict (c).', '',
 '## Fleet STOP (READ, bounded region, NOT-FOUND control)']
for n in sorted(K['prs']):
    s = S[n]
    out.append('- #%s `%s` (%d lines, rc %s): %s' % (n, os.path.basename(s['log']), s['lines'], s['rc'],
        ('%s · %s · %s · %s; "%s"' % (s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['shell_suites'], s['verdict_line'])) if s['preflight_ran'] else 'NO PREFLIGHT — NOT APPLICABLE'))
out += ['- By path class neither kit PR changes the count (a TypeScript util / route and a jest / vitest cell — no `*.test.sh`): after this merge 28/0 · 6/0 · 49/0 · 60 of 60.', '']
out += ['## LEGITIMATE SHAPES — the drafter\'s READ predictions (the gate MEASURES every row; a row saying MEASURED is a drafter\'s run, still not the gate\'s evidence)', '| PR | prediction | predicted-by |', '|---|---|---|']
for l in open(D + '/predict_1.out').read().splitlines():
    m = re.match(r'^  #(\d+) (.*)$', l)
    if m and not m.group(2).startswith(('PRODUCT files', 'NO product file')):
        out.append('| #%s | %s | drafter %s (predict_1.out) |' % (m.group(1), m.group(2).replace('|', '/')[:1300], 'MEASURED' if 'MEASURED' in m.group(2)[:120] else 'READ'))
open(D + '/COMMISSION.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/COMMISSION.md', len(out), 'lines')
