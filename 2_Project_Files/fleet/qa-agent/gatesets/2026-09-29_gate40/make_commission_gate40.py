#!/usr/bin/env python3
"""make_commission_gate40.py — writes COMMISSION.md for gate40 (the directory this script lives in). Every SHA / tree / count in it is READ from
pins_gate40.json, stopcounts_gate40.json, pgprobe_gate40.json, fill_1.out and predict_1.out beside it (never typed); the prose rows are the drafter's.
Shape copied from gate39's make_commission (gate38 -> gate37 lineage), re-keyed to gate40's ONE row (T1), no stack, one merge-base, and carrying
Wednesday's TEN requirements each BY NAME."""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit))); PG = json.load(open('%s/pgprobe_%s.json' % (D, kit)))
fill = open(D + '/fill_1.out').read()
def lands(n):
    m = re.search(r'#%s (\d+)->(\d+)' % n, fill); return 'declared %s -> lands %s' % (m.group(1), m.group(2)) if m else '?'
SUM = PG['_summary']; R = PG['runs']
def scen(key, prefix):
    for k, v in ((R.get(key) or {}).get('scen') or {}).items():
        if k.startswith(prefix): return v
    return None
def j(x): return json.dumps(x, ensure_ascii=False, default=str)
n = '1338'; pr = P['prs'][n]
files = ', '.join('%s +%s/-%s' % (os.path.basename(x.split('\t')[2]), x.split('\t')[0], x.split('\t')[1]) for x in pr['numstat'])
WHY = ('KS-1370 both halves', '**T1 SECURITY**: the ONE route every sk_ API key authenticates through (the gateway calls it per x-api-key request). Half (i): validate\'s usage write is the usage-only `dbRecordApiKeyUsage` UPDATE; half (ii): on a cache HIT the stored row is re-read through the SECURITY DEFINER carve-out and decides — sticky revoke both ways, vanished row evicted, failed read with a DB configured -> 503, memory-only answers from memory. dbSaveApiKey and the revoke route are BYTE-IDENTICAL base -> head (MEASURED, predict (e)).')
row = '| #%s | %s | %s | `%s` | %d on `%s` | %s | %s | %s |' % (n, WHY[0], K['prs'][n]['tier'], pr['head'], len(pr['commits']), pr['merge_base'][:12], files, lands(n), WHY[1])
h = SUM.get('head', {}); b = SUM.get('base', {})
out = ['# COMMISSION — DRAFT the round-40 batch gate kit "%s" over ONE PR (T1). Do NOT launch.' % kit, '',
 'Commissioned by Wednesday to the drafter on 2026-09-29 (~08:45 AEST) for Seat B 42nd\'s queue (Secuura/Blockchain): #1338 KS-1370 "validate reads the stored',
 'revoke", BOTH halves, per Kam\'s ruling (a) on card `secuura-ks1370-revoke-undone-by-stale-process` plus his (a) on `secuura-ks1370-validate-when-the-revoke-check-cannot-read`,',
 'TIER 1 (security). Head %s (the commission\'s value 42f8a5abc65ef9a6bc20c07797786089f2b9cd93, re-read by ls-remote AND the PULLS API at the pin: %s), base develop' % (pr['head'], 'EQUAL' if pr['head'] == '42f8a5abc65ef9a6bc20c07797786089f2b9cd93' else 'DIFFERENT'),
 '%s (the commission\'s 0de108577e6199de3c9402c0643a2944d86aee97: %s). Author Seat B 42nd; its READY mail captured by id (mail_gate40_ready.md). Routing token' % (P['develop'], 'EQUAL' if P['develop'] == '0de108577e6199de3c9402c0643a2944d86aee97' else 'DIFFERENT'),
 '`QA/Secuura-batch1338` (Wednesday adds the inbox_routing line). GO string `GO (Seat B 42nd): merge 1338 on gate40`; the addendum one line (`- #1338 · head <sha12> · …`).', '',
 '**DISK (Wednesday):** /Volumes/DevMASTER is FULL (~1.5 GiB free). The QA agent\'s clones, worktrees, `npm ci`, builds and Postgres data dirs go on the Data volume',
 '(its session scratchpad under /private/tmp/claude-501/), socket dirs a short `/tmp/q40g.*`; long-running output is written in the scratchpad and copied in when done;',
 'the report dir holds TEXT only; it STOPS on any ENOSPC (kit rule 55).', '',
 '## The batch — the head re-read by the drafter from origin (ls-remote + a fetch into a `--shared --no-checkout` scratch clone + the PULLS API; all agree)',
 '| PR | ticket | tier | head | commits on merge-base | files | subject (no `(#n)`) | why this tier, from the DIFF |', '|---|---|---|---|---|---|---|---|', row, '',
 'Tiers per 0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md: T1 = security surfaces, data destruction and erasure, anything deploying to dev / demo.',
 'Linear: #1338 links KS-1370 as `contributes`, not `closes` (linear_reads_1.out); no title, body or commit message carries a closing word or a FOREIGN hyphenated key (keyscan_1.out).',
 'MG-11 as it LANDS: the PR title is 85 chars and lands at 93 — OVER 92 — so the kit MANDATES the declared subject in fill_gate40.py SHORT (%s), without `(#n)`.' % lands(n), '',
 '## THE TEN REQUIREMENTS (Wednesday\'s commission), each BY NAME — in the filled prompt as kit rules 40-44 / 46-50, refused by the launcher if absent, split by the R<exit> controls',
 '1. **REAL-POSTGRES-DRILL (kit rule 40)** — a REAL PostgreSQL (unix socket, no TCP, not Docker) drill of KS-1370 at the base (RED: a stale instance says valid AND its usage write sets is_active back to true) and at the head (GREEN), with controls both ways; Seat B 42nd\'s and Seat B 41st\'s drill method is in the capture; the gate re-derives, it does not trust. Drafter MEASURED (as secuura_app): R2 base %s | head %s; R3 (booted after the revoke) %s / %s.' % (
     j(b.get('R2 stale instance after the stored revoke: answer / row after')), j(h.get('R2 stale instance after the stored revoke: answer / row after')), j((scen('base as secuura_app', 'R3') or {}).get('answer')), j((scen('head as secuura_app', 'R3') or {}).get('answer'))),
 '2. 🔴 **NON-SUPERUSER-ROLE (kit rule 41)** — the stored read MUST be driven as a NON-superuser application role (the builder\'s drill ran as `postgres` with rolbypassrls, so it could not show whether the SECURITY DEFINER carve-out `svc_api_keys_auth_lookup` / `security_find_api_key_by_hash` returns the row under FORCE RLS). A gate that repeats the superuser drill has not tested the premise. Drafter MEASURED the premise as secuura_app (provisioned by the REAL runStartupMigrations with APP_DB_PASSWORD): %s; as the superuser: %s.' % (
     j(SUM.get('premise as secuura_app (head)')), j(SUM.get('premise as postgres (head)'))),
 '3. **STICKY-BOTH-WAYS / VANISHED-ROW-EVICTED (kit rule 42)** — both Wednesday-confirmed design calls, each with a discriminating arm: (a) revoked if EITHER the in-memory copy or the stored row says revoked, KS-888 cell R2 passes unchanged — A1 head %s, arm (a) %s; (b) a vanished row answers `Key not found` and evicts — D1 head %s, arm (b) %s; base %s (the base\'s upsert RE-CREATES the deleted row). Each half load-bearing: arm C %s (revived), arm D %s.' % (
     j(h.get('A1 cached-revoked stored-active: answer / store')), j(SUM.get('armA_nosticky', {}).get('A1 cached-revoked stored-active: answer / store')), j(h.get('D1 vanished: answer / evicted / row re-created?')),
     j(SUM.get('armB_noevict', {}).get('D1 vanished: answer / evicted / row re-created?')), j(b.get('D1 vanished: answer / evicted / row re-created?')),
     j(SUM.get('armC_revive', {}).get('R2 stale instance after the stored revoke: answer / row after')), j(SUM.get('armD_half1only', {}).get('R2 stale instance after the stored revoke: answer / row after'))),
 '4. **FAILED-READ-503 / MEMORY-ONLY-FROM-MEMORY (kit rule 43)** — Kam\'s split: a configured database whose read fails -> 503 \'Unable to verify key\'; memory-only mode (isDbAvailable false) answers from memory and still refuses an in-memory revoke. F1 (EXECUTE on the carve-out revoked from secuura_app) base %s | head %s; F2 cache-MISS head %s; M1 head %s.' % (
     j(b.get('F1 stored read fails (EXECUTE revoked): status / message')), j(h.get('F1 stored read fails (EXECUTE revoked): status / message')), j((scen('head as secuura_app', 'F2') or {}).get('answer')), j(h.get('M1 memory-only: avail / active / revoked'))),
 '5. **USAGE-WRITE-LOG-ONLY / NO-KEY-NO-HASH-IN-LOGS / V2-PINS-UNTOUCHED (kit rule 44)** — Kam\'s KS-888 ruling kept: a failed usage write is logged once, never refused, no key or hash in any log (#1334\'s V2 pins untouched). U1 (UPDATE revoked from secuura_app) [status, valid, error lines, key lines, hash lines] base %s | head %s.' % (
     j(b.get('U1 usage write fails: status / valid / error lines / key lines / hash lines')), j(h.get('U1 usage write fails: status / valid / error lines / key lines / hash lines'))),
 '6. **REPIN-LINE-BY-LINE / WEAKENED-PIN-BLOCKER (kit rule 46)** — #1334\'s re-pin: the 5 declarations / 7 cases that changed (R2, C3, V1 x3, V2, V3 per the seat) are read line by line and judged — fixture made more faithful, or a pin weakened? Any weakened pin is a BLOCKER. Drafter READ: only V1 and V3 carry TEXT edits (`state.inserts` -> `state.usageWrites`) plus the mock; R2 / C3 / V2 went green by the mock alone (predict_1.out).',
 '7. **CROSS-PACKAGE-GUARDS / KS764-GUARD-CALL-SITE (kit rule 47)** — every test file that references a changed file\'s path across the monorepo (`git grep -l \'<changed path>\' -- \'*.test.ts\'`) plus the packages/shared KS 764 revoke call-site guard, run in the gate. Drafter READ: packages/shared ks764-key-revoke-call-site-guard.test.ts and ks781-p3-3-body-parser-order.test.ts read security index.ts; the guard\'s two revoke patterns EMULATED 1/1 at base and head.',
 '8. **GATEWAY-REFUSAL-CACHE / SECURITY-DB-FAULT-END-TO-END (kit rule 48)** — the gateway\'s 30 s refusal cache (api-gateway auth.ts :220 cached return, :228-:229 `!resp.ok` 30 s, :235 `!data?.valid` 30 s, :247 VALID 60 s, :180 connector bearer 8 min — READ) is read, and the gate states what a security-DB fault now does end to end (prediction: 503 -> 30 s cached refusal -> 401 for the fault + 30 s; the PR body\'s "at most once per key per 30 s" is a slip candidate: VALID answers are cached 60 s).',
 '9. **TIER1-CAP-ROUND-1 (kit rule 49)** — Tier-1 gate, and the two-NO-GO cap: this is ROUND 1 for this class.',
 '10. **SUBJECT-LANDS-AT / TITLE-LANDS-93 / NO-FOREIGN-KEY (kit rule 50, + 51 the key scan)** — the GO string `GO (Seat B 42nd): merge 1338 on gate40` (launcher exit 26); the squash subject declared WITHOUT `(#n)` and checked as declared + " (#1338)" <= 92 (%s; the title itself lands at 93 and fill REFUSES it — control SJ4); the key scanner over the mandated body (keyscan_1.out, fill_1.out).' % lands(n), '',
 '## Develop at the pin',
 'Pinned over develop **`%s`** (tree `%s`), READ by ls-remote and fetched. Merge-base MEASURED: `%s` (develop itself: the develop move since it is EMPTY). END_TREE **`%s`** (%s), %d merge-tree call(s).' % (
     P['develop'], P['develop_tree'], pr['merge_base'][:12], P['end_tree'], P['end_shortstat'], P['merge_tree_calls']),
 'The launch action\'s step 3b re-pins on any further move.', '',
 '## Overlaps — NONE declared, NONE found',
 '- Every other OPEN PR at the pin (%d, the PULLS API census): disjoint from every kit path.' % len(P['inflight']),
 '- `merged_blob_paths` NONE and `noop_paths` NONE — two different declarations, each asserted empty by predict (c).', '',
 '## The drafter\'s real-Postgres drill (pgprobe_1.out, %s; unix socket only; controls %s)' % (PG.get('engine', '?')[:40], 'ALL PASS' if all(v is True for v in PG['controls'].values()) else PG['controls']),
 '- Sides: base (develop), head, and four ARMS of head (armA_nosticky, armB_noevict, armC_revive, armD_half1only), each a COPY with asserted edits (%s).' % j({k: v['edits'] for k, v in PG.get('arms', {}).items()}),
 '- secuura_app as provisioned, read back per side (boot 2): %s.' % j({s: (v[-1].get('db') or {}).get('secuura_app') for s, v in PG.get('boots', {}).items()}),
 '- Per side (as secuura_app): %s.' % j({s: v for s, v in SUM.items() if s in ('base', 'head') or s.startswith('arm')}),
 '- NOT measured by the drafter: two OS processes (two module instances, as the seat), the REAL revoke route (a row UPDATE, as the seat), vitest / tsc / eslint / prettier (no npm ci), the gateway end to end, a deployed database\'s grants.', '',
 '## Fleet STOP (READ, bounded region, NOT-FOUND control)']
s = S[n]
out.append('- #%s `%s` (%d lines, rc %s): pre_push_hook_base %s · fixture_guard %s · run_shell_suites %s · %s; "%s"' % (n, os.path.basename(s['log']), s['lines'], s['rc'], s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['shell_suites'], s['verdict_line']))
out += ['- By path class #1338 changes no `*.test.sh`, script or migration. After this merge 28/0 · 6/0 · 49/0 · 60 of 60.', '']
out += ['## LEGITIMATE SHAPES — the drafter\'s READ predictions (the gate MEASURES every row; a row saying MEASURED is a drafter\'s run, still not the gate\'s evidence)', '| PR | prediction | predicted-by |', '|---|---|---|']
for l in open(D + '/predict_1.out').read().splitlines():
    m = re.match(r'^  #(\d+) (.*)$', l)
    if m:
        out.append('| #%s | %s | drafter %s (predict_1.out) |' % (m.group(1), m.group(2).replace('|', '/')[:1500], 'MEASURED' if 'MEASURED' in m.group(2)[:160] else 'READ'))
open(D + '/COMMISSION.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/COMMISSION.md', len(out), 'lines')
