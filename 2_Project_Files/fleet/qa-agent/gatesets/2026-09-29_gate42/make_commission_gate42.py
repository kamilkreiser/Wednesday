#!/usr/bin/env python3
"""make_commission_gate42.py — writes COMMISSION.md for gate42 (the directory this script lives in). Every SHA / tree / count in it is READ from
pins_gate42.json, stopcounts_gate42.json, installprobe_gate42.json, fill_1.out and predict_1.out beside it (never typed); the prose rows are the
drafter's. Shape copied from gate40's make_commission (gate39 -> gate38 lineage), re-keyed to gate42's ONE row (T1), no stack, one merge-base, and
carrying Wednesday's NINE requirements each BY NAME."""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit))); IP = json.load(open('%s/installprobe_%s.json' % (D, kit)))
fill = open(D + '/fill_1.out').read(); pred = open(D + '/predict_1.out').read()
CH, CD = '8c1b25b24782d851817f8c7bb1c02d390fe750d7', '8af6ab8216007462e596daed6b0adcd1e87e34ee'   # the values Wednesday's commission named (ls-remote 12:0x AEST)
def lands(n):
    m = re.search(r'#%s (\d+)->(\d+)' % n, fill); return 'declared %s -> lands %s' % (m.group(1), m.group(2)) if m else '?'
def pl(rx):
    m = [l.strip() for l in pred.splitlines() if re.search(rx, l)]; return re.sub(r'^(PASS )?#1339 ', '', m[-1]) if m else 'ABSENT'
def j(x): return json.dumps(x, ensure_ascii=False, default=str)
n = '1339'; pr = P['prs'][n]; SU = IP['_summary']
files = '%d files (%s)' % (len(pr['paths']), '14 package.json + 14 package-lock.json')
WHY = ('KS-1378 + KS-729', '**T1 DEPENDENCY BUMP REACHING SHIPPED SERVICES + SECURITY FIX**: nodemailer 9 -> 10 (a MAJOR; the cross-tenant SMTP credential disclosure GHSA-6vj9-mwq6-2f5v) in services/auth, services/originate and the root; morgan ^1.12.1 in ten services (log injection); ip-address ^10.5.1 overrides; undici ^7.29.1 scoped under jsdom. Each service Dockerfile runs `npm ci --ignore-scripts` on its OWN lock, so a lock line IS what ships. ZERO source files (MEASURED, predict (e)).')
row = '| #%s | %s | %s | `%s` | %d on `%s` | %s | %s | %s |' % (n, WHY[0], K['prs'][n]['tier'], pr['head'], len(pr['commits']), pr['merge_base'][:12], files, lands(n), WHY[1])
DOS = K.get('dead_open_declared', {})
out = ['# COMMISSION — DRAFT the round-41 batch gate kit "%s" over ONE PR (T1). Do NOT launch.' % kit, '',
 'Commissioned by Wednesday to the drafter on 2026-09-29 (~12:10 AEST) for Seat B 43rd\'s one raised PR (Secuura/Blockchain): #1339 KS-1378 "bump four advisory packages",',
 'the advisory bump Kam ruled (a) on card `secuura-five-new-advisories-block-every-push-0929` at 11:43 AEST, TIER 1. Head %s (the commission\'s value %s,' % (pr['head'], CH),
 're-read by ls-remote AND the PULLS API at the pin: %s), base develop %s (the commission\'s %s: %s). Author Seat B 43rd, WRAPPED; its READY mail' % ('EQUAL' if pr['head'] == CH else 'DIFFERENT', P['develop'], CD, 'EQUAL' if P['develop'] == CD else 'DIFFERENT'),
 'captured by id (mail_gate42_ready.md). Routing token `QA/Secuura-batch1339` (Wednesday adds the inbox_routing line). GO string `GO (Seat B 44th): merge 1339 on gate42`',
 '— it names the SUCCESSOR merge seat (not yet launched); the addendum one line (`- #1339 · head <sha12> · …`).', '',
 '**DISK:** the QA agent\'s clones, worktrees, `npm ci` trees, npm cache and builds go on the Data volume (its session scratchpad under /private/tmp/claude-501/);',
 'long-running output is written in the scratchpad and copied in when done; the report dir holds TEXT only; it STOPS on any ENOSPC (kit rule 55).', '',
 '## The batch — the head re-read by the drafter from origin (ls-remote + a fetch into a `--shared --no-checkout` scratch clone + the PULLS API; all agree)',
 '| PR | tickets | tier | head | commits on merge-base | files | subject (no `(#n)`) | why this tier, from the DIFF |', '|---|---|---|---|---|---|---|---|', row, '',
 'Tiers per 0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md: T1 = security surfaces, data destruction and erasure, anything deploying to dev / demo; a dependency bump reaching shipped services and fixing advisories is T1.',
 'Linear: #1339 links KS-1378 AND KS-729 as `contributes`, not `closes` (linear_reads_1.out); no title, body or commit message carries a closing word or a FOREIGN hyphenated key (keyscan_1.out).',
 'MG-11 as it LANDS: the PR title is 75 chars and lands at 83; fill_gate42.py SHORT declares it verbatim (%s), without `(#n)`; the mandated body carries `Refs KS-1378` and `Refs KS-729`.' % lands(n), '',
 '## THE NINE REQUIREMENTS (Wednesday\'s commission), each BY NAME — in the filled prompt as kit rules 40-44 / 46-49 (+ 50 the Tier-1 cap), refused by the launcher if absent, split by the R<exit> controls',
 '1. 🔴 **A CLEAN INSTALL (kit rule 40; CLEAN-INSTALL, NODEMAILER-10-RUNS, EOVERRIDE-GOTCHA, ROOT-AND-STANDALONE-INSTALL)** — `npm ci` per affected lock, never an incremental install, so nodemailer 10.0.x is what actually runs, proved by printing the RESOLVED version from node_modules; the author\'s suites ran against 9.1.1 because of the EOVERRIDE install gotcha (its harness printed "install rc=0" after "npm error code EOVERRIDE"); a gate that repeats it has not tested the bump. The ROOT workspace install (what the suites run from) AND the STANDALONE service install (what each Dockerfile ships) are both owed. Drafter MEASURED the standalone one (installprobe_1.out, npm %s / node %s, controls %s): %s.' % (
     IP['npm'], IP['node'], 'ALL PASS' if all(IP['controls'].values()) else j(IP['controls']), j({k: (v['nodemailer'], v['nodemailer_entry']) for k, v in SU.items()})),
 '2. **services/auth AND services/originate SUITES GREEN ON NODEMAILER 10 (kit rule 41; AUTH-SUITE-ON-10, ORIGINATE-SUITE-ON-10, ORIGINATE-PRE-EXISTING-AT-BASE, ORIGINATE-RUNNER-IS-JEST)** — the author\'s originate suite does not load (`Cannot find module \'../routes/anchors\'`), claimed PRE-EXISTING: the gate proves it at the BASE 8af6ab82 or finds it is the bump\'s. Drafter READ: %s.' % pl(r"ORIGINATE '../routes/anchors'")[:700],
 '3. **NODEMAILER 9 -> 10 BREAKING CHANGES (kit rule 42; NODEMAILER-CHANGELOG-9-TO-10, CALL-SITES-PER-SERVICE, TYPES-BUNDLED-VS-AT-TYPES, ESM-CJS-DUAL-BUILD)** — the changelog for 9 -> 10 against our two call sites per service (transport creation, sendMail options). Drafter READ 10.0.0 "⚠ BREAKING CHANGES: Node.js 20 or newer is required" + "migrate to TypeScript with ES module and CommonJS builds"; `"type": "module"`, exports import -> dist/esm, require -> dist/cjs; MEASURED the CJS entry exposes createTransport directly and on `.default`, and both call-site shapes build on 10.0.12 (installprobe). %s | %s | %s.' % (
     pl(r'services/auth email.ts BYTE-IDENTICAL'), pl(r'services/originate email.ts BYTE-IDENTICAL'), pl(r'^  #1339 TYPES')),
 '4. **AUDIT LEGS 6 AND 7 PASS AT THE HEAD (kit rule 43; AUDIT-LEG-6, AUDIT-LEG-7, BASELINE-UNTOUCHED, CLEANUP-ROWS-NAMED, OUT-OF-SCOPE-LOCKS)** — the gate re-runs the repo\'s own audit scripts (legs 6 `audit:gate` and 7 `audit:locks`, plus `audit:contract`) at base (RED: 5 NEW) and head / END_TREE (GREEN), confirms no baseline row was added or edited, and names the two CLEANUP rows the leg now advises removing (GHSA-v2v4-37r5-5v8g, GHSA-mwp4-54f8-5fhr) without acting on them. Drafter READ: %s | %s | %s.' % (
     pl(r'AUDIT BASELINE'), pl(r'across the \d+ IN-SCOPE locks'), pl(r'OUT-OF-SCOPE LOCKS')[:520]),
 '5. **MORGAN 1.12.1 (kit rule 44; MORGAN-COMBINED-LOGS, MORGAN-QUOTE-ESCAPED)** — the \'combined\' format still logs, and a planted double quote in User-Agent is escaped in the log line. Drafter MEASURED (installprobe, services/auth standalone installs): base morgan %s escaped %s | head morgan %s escaped %s (control line logged on both). %s.' % (
     SU['base_auth']['morgan'], SU['base_auth']['morgan_planted_quote_escaped'], SU['head_auth']['morgan'], SU['head_auth']['morgan_planted_quote_escaped'], pl(r'MORGAN CALL SITES')[:300]),
 '6. **THE UNDICI OVERRIDE IS SCOPED TO jsdom (kit rule 46; UNDICI-SCOPED-TO-JSDOM, ROOT-UNDICI-UNTOUCHED, IP-ADDRESS-NO-9X, CARDANO-NESTED-OVERRIDDEN)** — the root undici 5.29.0 untouched and not vulnerable per the author; ip-address\'s `@cardano-sdk` nested copies overridden and no 9.x copy remains. Drafter READ: %s | %s | %s | %s.' % (
     pl(r'UNDICI override SCOPED'), pl(r'UNDICI root copy'), pl(r'IP-ADDRESS: a 9.x copy'), pl(r'^  #1339 IP-ADDRESS \(READ\)')),
 '7. **EVERY SUITE TOUCHED BY A CHANGED LOCKFILE (kit rule 47; LOCK-SUITES-BEFORE-AFTER)** — all 10 morgan services, packages/shared, frontend/issuer, anchoring (+ originate) run with before/after counts; a lock change can break a service without touching its code. Drafter READ: %s.' % pl(r'SUITES OWED')[:600],
 '8. **CROSS-PACKAGE GUARDS (kit rule 48; CROSS-PACKAGE-GUARDS, LOCK-DISCOVERY-CONTRACT)** — as in gate40: `git grep -l` for any test referencing a changed path, plus the audit contract suites. Drafter READ: %s.' % pl(r'CROSS-PACKAGE CENSUS')[:700],
 '9. **THE GO STRING AND THE SUBJECT (kit rule 49; SUBJECT-LANDS-AT, REFS-TWO-KEYS, NO-FOREIGN-KEY; + 51 the key scan)** — the GO string `GO (Seat B 44th): merge 1339 on gate42` (launcher exit 26); the squash subject declared WITHOUT `(#n)` and checked as declared + " (#1339)" <= 92 (%s); Refs KS-1378 and Refs KS-729 (one line each); the key scanner over the mandated body (keyscan_1.out, fill_1.out). The Tier-1 cap is kit rule 50 (TIER1-CAP-ROUND-1: round 1 for this class).' % lands(n), '',
 '## Develop at the pin',
 'Pinned over develop **`%s`** (tree `%s`), READ by ls-remote and fetched. Merge-base MEASURED: `%s` (develop itself: the develop move since it is EMPTY). END_TREE **`%s`** (%s), %d merge-tree call(s).' % (
     P['develop'], P['develop_tree'], pr['merge_base'][:12], P['end_tree'], P['end_shortstat'], P['merge_tree_calls']),
 'The launch action\'s step 3b re-pins on any further move.', '',
 '## Overlaps — `merged_blob_paths` NONE, `noop_paths` NONE; ELEVEN OPEN PRs DECLARED as overlapping (kit.json `dead_open_declared`, mode open_manifest_overlap)',
 '- Every other OPEN PR at the pin that is not declared (%d, the PULLS API census): disjoint from every kit path.' % len(P['inflight']),
 '- DECLARED, each measured EQUAL by predict (c): %s. None is in this kit, none is merged by it; after #1339 lands each conflicts on those manifests / locks (dependabot rebases its own; #920 KS-734 needs its owner). If any of them MERGES FIRST, develop moves over #1339\'s own paths and the launch action\'s re-pin refuses rc 10.' % '; '.join(
     '#%s (%s) %s' % (b, (P['dead_open_declared'].get(b, {}).get('title') or '')[:48], [x.replace('Blockchain/Dev/', '') for x in v['paths']]) for b, v in sorted(DOS.items(), key=lambda x: -int(x[0]))),
 '- `merged_blob_paths` NONE and `noop_paths` NONE — two different declarations, each asserted empty by predict (c).', '',
 '## The drafter\'s clean installs (installprobe_1.out; standalone `npm ci --ignore-scripts` per service lock; controls %s)' % ('ALL PASS' if all(IP['controls'].values()) else j(IP['controls'])),
 '- Per install: %s.' % j(SU),
 '- Controls: %s.' % j(IP['controls']),
 '- NOT measured by the drafter: the ROOT workspace install and require.resolve from each service dir, any vitest / jest suite, tsc, the audit legs (network: npm advisory API), a real SMTP exchange, the other nine services\' installs.', '',
 '## Fleet STOP (READ, bounded region, NOT-FOUND control)']
s = S[n]
out.append('- #%s `%s` (%d lines, %s): pre_push_hook_base %s · fixture_guard %s · run_shell_suites %s · %s; "%s"' % (n, os.path.basename(s['log']), s['lines'], s.get('rc_line'), s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['shell_suites'], s['verdict_line']))
out += ['- By path class #1339 changes no `*.test.sh`, script or migration (manifests and locks only). After this merge 28/0 · 6/0 · 49/0 · 60 of 60.', '']
out += ['## LEGITIMATE SHAPES — the drafter\'s predictions (the gate MEASURES every row; a row saying MEASURED is a drafter\'s run, still not the gate\'s evidence)', '| PR | prediction | predicted-by |', '|---|---|---|']
for l in pred.splitlines():
    m = re.match(r'^  #(\d+) (.*)$', l)
    if m:
        out.append('| #%s | %s | drafter %s (predict_1.out) |' % (m.group(1), m.group(2).replace('|', '/')[:1500], 'MEASURED' if 'MEASURED' in m.group(2)[:160] else 'READ'))
open(D + '/COMMISSION.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/COMMISSION.md', len(out), 'lines')
