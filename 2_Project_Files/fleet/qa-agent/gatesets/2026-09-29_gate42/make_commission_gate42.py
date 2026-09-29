#!/usr/bin/env python3
"""make_commission_gate42.py — writes COMMISSION.md for gate42 (the directory this script lives in). Every SHA / tree / count in it is READ from
pins_gate42.json, stopcounts_gate42.json, installprobe_gate42.json, fill_1.out and predict_1.out beside it (never typed); the prose rows are the
drafter's. Shape copied from gate41's make_commission (gate40 -> gate39 lineage), re-keyed to gate42's ONE row (T1, #1339 ROUND 2 OF 2 — the LAST round
under the Tier-1 cap), no stack, one merge-base, carrying Wednesday's SEVEN gate42 requirements each BY NAME, the prior round's (gate41) findings as a
checklist, and requirement 5's test-file list read from the pins."""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit))); IP = json.load(open('%s/installprobe_%s.json' % (D, kit)))
fill = open(D + '/fill_1.out').read(); pred = open(D + '/predict_1.out').read()
CH, CD = 'fa93ff88f47e', '8af6ab821600'   # the values Wednesday's gate42 commission named (prefixes, "re-read it by `git ls-remote` before you trust it")
def lands(n):
    m = re.search(r'#%s (\d+)->(\d+)' % n, fill); return 'declared %s -> lands %s' % (m.group(1), m.group(2)) if m else '?'
def pl(rx):
    m = [l.strip() for l in pred.splitlines() if re.search(rx, l)]; return re.sub(r'^(PASS )?#1339 ', '', m[-1]) if m else 'ABSENT'
def j(x): return json.dumps(x, ensure_ascii=False, default=str)
rp = lambda x: x[len('Blockchain/Dev/'):] if x.startswith('Blockchain/Dev/') else x
n = '1339'; pr = P['prs'][n]; SU = IP['_summary']; CZ = P['measured'][n]['census']; R1 = K['round1_head']
files = '%d files (14 package.json + 14 package-lock.json from round 1; 2 email.ts from round 2)' % len(pr['paths'])
WHY = ('KS-1378 + KS-729', '**T1 DEPENDENCY BUMP REACHING SHIPPED SERVICES + SECURITY FIX, ROUND 2 OF 2**: nodemailer 9 -> 10 (a MAJOR; GHSA-6vj9-mwq6-2f5v) in auth, originate and the root; morgan ^1.12.1 in ten services; ip-address ^10.5.1 overrides; undici ^7.29.1 scoped under jsdom. Each service Dockerfile runs `npm ci --ignore-scripts` on its OWN lock and then `npm run build`; round 2 edits product SOURCE in two shipped services (a type-only import + two annotations).')
row = '| #%s | %s | %s | `%s` | %d on `%s` (round 1 `%s`, round 2 `%s`) | %s | %s | %s |' % (n, WHY[0], K['prs'][n]['tier'], pr['head'], len(pr['commits']), pr['merge_base'][:12], pr['commits'][0][:12], pr['commits'][-1][:12], files, lands(n), WHY[1])
DOS = K.get('dead_open_declared', {})
tsc = SU['tsc']; st = SU['standalone_suites']; rc_ = SU['runtime_copies']
def mv(key, sfx): return [v for p_, v in rc_[key] if p_.endswith(sfx)]
out = ['# COMMISSION — DRAFT the round-42 batch gate kit "%s" over ONE PR (T1), #1339 ROUND 2 OF 2 — the LAST round under the Tier-1 cap. Do NOT launch.' % kit, '',
 'Commissioned by Wednesday to the drafter on 2026-09-29 (after Seat B 44th\'s round-2 READY of 04:09:25Z) for #1339 KS-1378 "bump four advisory packages", the advisory',
 'bump Kam ruled (a) on card `secuura-five-new-advisories-block-every-push-0929`. Round 1 (`%s`, Seat B 43rd) was graded NO GO by gate41 on N-1339-1 (auth +' % R1,
 'originate `tsc` rc 2, TS2503 on nodemailer 10 — no image builds). Round 2 (Seat B 44th, which adopted Seat B 43rd\'s branches) adds ONE commit. Head %s (the' % pr['head'],
 'commission\'s `%s…`: %s; re-read by ls-remote AND the PULLS API AND the fetch at the pin), base develop %s (the commission\'s `%s…`: %s). A NO GO here ships nothing' % (
     CH, 'EQUAL' if pr['head'].startswith(CH) else 'DIFFERENT', P['develop'], CD, 'EQUAL' if P['develop'].startswith(CD) else 'DIFFERENT'),
 'and goes to Kam. The round-2 READY mail is captured by id (mail_gate42_ready.md). Routing token `%s` (Wednesday adds the inbox_routing line; the drafter did' % K['pane'],
 'not). GO string `GO (Seat B 44th): merge 1339 on gate42`; the addendum one line (`- #1339 · head <sha12> · …`).', '',
 '**DISK:** the QA agent\'s clones, worktrees, `npm ci` trees, npm cache and builds go on the Data volume (its session scratchpad under /private/tmp/claude-501/);',
 'long-running output is written in the scratchpad and copied in when done; the report dir holds TEXT only; it STOPS on any ENOSPC (kit rule 55).', '',
 '## The batch — the head re-read by the drafter from origin (ls-remote + a fetch into a `--shared --no-checkout` scratch clone + the PULLS API; all agree)',
 '| PR | tickets | tier | head | commits on merge-base | files | subject (no `(#n)`) | why this tier, from the DIFF |', '|---|---|---|---|---|---|---|---|', row, '',
 'Tiers per 0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md: a dependency bump reaching shipped services and fixing advisories is T1; round 2 adds product source in two shipped services. **Class round 2 of 2: this is the LAST round** (gate41 was the first NO GO).',
 'Linear: #1339 links KS-1378 AND KS-729 as `contributes`, not `closes`; KS-1379 (the ticketed N-1339-2) is Backlog and NOT linked (linear_reads_1.out); no title, body or commit message carries a closing word or a FOREIGN hyphenated key (keyscan_1.out).',
 'MG-11 as it LANDS: the PR title is 75 chars and lands at 83; fill_gate42.py SHORT declares it verbatim (%s), without `(#n)` (Wednesday\'s Q5: title and Refs unchanged); the mandated body carries `Refs KS-1378` and `Refs KS-729`.' % lands(n), '',
 '## THE SEVEN REQUIREMENTS (Wednesday\'s gate42 commission), each BY NAME — in the filled prompt as kit rules 40-44 / 46-47, refused by the launcher if absent, split by the R<exit> controls',
 '1. 🔴 **A CLEAN INSTALL, `tsc` rc 0 ON auth AND originate (THE DOCKERFILE BUILD PATH), AND BOTH SUITES (kit rule 40; CLEAN-INSTALL-NODEMAILER-10, TSC-AUTH-ON-10, TSC-ORIGINATE-ON-10, DOCKERFILE-BUILD-PATH, AUTH-SUITE-ON-10, ORIGINATE-SUITE-IS-JEST)** — a clean `npm ci` resolving nodemailer 10.0.x; `tsc` rc 0 on auth AND originate on a faithful host mirror of each Dockerfile\'s shared-builder + builder stages; both suites whole (originate is JEST). Drafter MEASURED (installprobe_1.out, npm %s / node %s, controls %d/%d PASS): `npm run build` %s; resolved nodemailer %s; tsc at the head reads nodemailer declaration files %s. **CT8 is the control that can fail: the REAL round-1 code reds with exactly the TS2503 pair** (%s). The drafter did NOT run the root install or either suite: the seat\'s "77 / 836" and "89 / 1058" on 10.0.12 are claims.' % (
     IP['npm'], IP['node'], sum(IP['controls'].values()), len(IP['controls']), j({k: 'rc %s, %s error(s)' % (v['build_rc'], v['n_errors']) for k, v in tsc.items()}),
     j({k: (v['nodemailer'], v['entry']) for k, v in SU['nodemailer_probe'].items()}), j(SU['tsc_reads']),
     '; '.join('%s: %s' % (s, IP['tsc']['r1_%s' % s]['errors']) for s in ('auth', 'originate'))),
 '2. **EVERYTHING THAT HELD IN gate41 STILL HOLDS (kit rule 41; LEGS-6-7-RED-AT-BASE, LEGS-6-7-GREEN-AT-HEAD, BASELINE-BYTE-IDENTICAL, MORGAN-QUOTE-ESCAPED, UNDICI-SCOPED-TO-JSDOM, IP-ADDRESS-NO-9X)** — audit legs 6 and 7 red at the base and green at the head; the audit baseline byte-identical to develop. Drafter READ: %s | %s | %s | %s. MEASURED (standalone auth installs): base morgan %s escaped %s, head morgan %s escaped %s. The legs call the npm advisory API (the drafter made no advisory call). **The fuse:** rows frvp (KS 530) and mwp4 (KS 729) expire 2026-09-30; Kam\'s signed re-date is a SEPARATE PR (requirement 6) — a leg-6 red at the head AFTER 2026-09-30T00:00Z is the lapse, not the bump, and the gate proves which.' % (
     pl(r'AUDIT BASELINE'), pl(r'ROUND 2 MOVED NO LOCK'), pl(r'UNDICI override SCOPED')[:260], pl(r'IP-ADDRESS: a 9.x copy'),
     SU['nodemailer_probe']['base_auth']['morgan'], SU['nodemailer_probe']['base_auth']['morgan_planted_quote_escaped'], SU['nodemailer_probe']['head_auth']['morgan'], SU['nodemailer_probe']['head_auth']['morgan_planted_quote_escaped']),
 '3. **CLEAN STANDALONE INSTALLS + SUITES FOR THE RUNTIME-MOVED SERVICES (kit rule 42; RUNTIME-MOVED-QUEUE-MSGPACKR-2, RUNTIME-MOVED-MSAL-NODE-6, STANDALONE-SUITES-RUNTIME-MOVED, KS-1379-CONDITION)** — Wednesday\'s condition (ANSWER 03:54:40Z) for merging with KS-1379 open: queue (bullmq -> msgpackr 2) and m365-integration / packages/shared (@azure/identity -> msal-node 6) get a clean standalone `npm ci` + their own suite here. Drafter READ (the locks): %s. Drafter MEASURED (standalone installs, installprobe_rt_gate42.cjs load smokes ALL ok): queue msgpackr %s -> %s; m365 identity-nested msal-node %s -> %s; shared msal-node %s -> %s; own suites %s. **packages/shared\'s suite did NOT START standalone** (its lock carries no vitest; its config imports `vitest/config`): the gate closes that gap or marks it NOT TESTED with what else exercises shared\'s msal-node 6.' % (
     pl(r'THE RUNTIME-MOVED SERVICES'), mv('base_queue', '/msgpackr'), mv('head_queue', '/msgpackr'), mv('base_m365-integration', 'identity/node_modules/@azure/msal-node'), mv('head_m365-integration', 'identity/node_modules/@azure/msal-node'),
     mv('base_shared', '/@azure/msal-node'), mv('head_shared', '/@azure/msal-node'), j({k: v['summary'] for k, v in st.items()})),
 '4. **THE ROUND-2 DIFF, LINE BY LINE AGAINST N-1339-1 (kit rule 43; ROUND2-DIFF-LINE-BY-LINE, ROUND2-NO-SCOPE-CREEP, VALUE-USES-UNCHANGED, TYPE-ONLY-IMPORT-ELIDED)** — `git diff %s <head>` read whole. Drafter READ: %s | %s | %s | %s. gate41\'s fix-shape was an inline `{ type Transporter }` specifier; the seat wrote a separate `import type` line — the gate says whether the two are equivalent under this tsconfig and reads the EMITTED email.js.' % (
     R1[:12], pl(r'ROUND 2 SHAPE'), pl(r'ROUND 2 SCOPE'), pl(r'services/auth email.ts ROUND-2 DIFF')[:900], pl(r'services/originate email.ts ROUND-2 DIFF')[:400]),
 '5. **EVERY TEST FILE THAT REFERENCES A CHANGED PATH IS RUN (kit rule 44; TEST-FILES-BY-PATH, EMAIL-IMPORTERS-RUN, CROSS-PACKAGE-GUARDS, LOCK-DISCOVERY-CONTRACT)** — `git grep -l \'<path>\' -- \'*.test.ts\' \'*.test.js\'` over the whole monorepo (also .mjs / .sh / __tests__/*.sh, full / Blockchain/Dev-relative / src-relative spellings) and, for the two email.ts, the module spelling `services/email`. THE LIST (predict (e), READ at the pin — paths under Blockchain/Dev/ unless they start with another repo root):']
for k in sorted(CZ['exact']):
    out.append('   - by path `%s`: %s' % (k, ', '.join('`%s`' % rp(x) for x in CZ['exact'][k])))
out.append('   - naming any `package-lock.json`: %s' % ', '.join('`%s`' % rp(x) for x in CZ['broad']))
for s in ('services/auth', 'services/originate'):
    out.append('   - importing `%s/src/services/email.ts` (module spelling `services/email`, %d): %s' % (s, len(CZ['email_importers'][s]), ', '.join('`%s`' % rp(x) for x in CZ['email_importers'][s])))
out.append('   - plus `npm run audit:contract` (baseline-contract, lock-discovery, gate-exit-codes). The `.test.sh` files among these are counted in the fleet STOP (run-shell-suites) — READ, never run standalone over the real repo.')
out += [
 '6. **THE GO STRING, THE SUBJECT AND THE MERGE ORDER (kit rule 46; GO-STRING-SEAT-B-44TH, SUBJECT-LANDS-AT, REFS-TWO-KEYS, MERGE-ORDER-1339-FIRST, REDATE-PR-OUT-OF-KIT; + 51 the key scan)** — on pass the gate emits `GO (Seat B 44th): merge 1339 on gate42` (launcher exit 26); routing pane `%s`; subject %s, Refs KS-1378 + KS-729. **Merge order: #1339 ALONE, FIRST** — before Seat B 44th\'s six held branches (KS-1371, KS-1359, KS-1369, KS-1360, KS-1375, KS-1054) and before its separate audit-baseline RE-DATE PR. The re-date PR is NOT in this kit. It will carry a `-b44-<n>` branch, which the WIDEN census would refuse; kit.json `widen_disjoint_rule` makes ONE measured class DISJOINT-OUT-OF-KIT: an open WIDEN PR whose ENTIRE file list is `scripts/audit/audit-baseline.json` (predict (a) and the launch action\'s step 2b; controls RWD / RWD-twin prove both ways). At drafting no such PR was open (the rule is dormant; predict did not need it).' % (K['pane'], lands(n)),
 '7. **TIER 1, ROUND 2 OF 2 — THE LAST ROUND (kit rule 47; TIER1-CAP-ROUND-2, LAST-ROUND, TIERING)** — a second NO GO ends the lane and goes to Kam; the gate separates BLOCKS from SHIPS-WITH with the most care, and never inflates or softens either because this is the last round.', '',
 '## The prior round\'s findings (gate41 report, READ) — the gate re-checks each (kit rule 48; GATE41-FINDINGS-RECHECKED)',
 '| id | gate41 (round 1) | round 2, per the seat (a claim) | the drafter\'s prediction |', '|---|---|---|---|',
 '| N-1339-1 | Blocker: auth + originate tsc rc 2 TS2503; originate jest 2 suites / 11 red | FIXED: type-only `Transporter` import; tsc rc 0 both; 77/836, 89/1058 | CLOSED by the build-path mirror (CT8 red at round 1, CT9 green at head, MEASURED); suites NOT run by the drafter |',
 '| N-1339-2 | Major: ~1,000 collateral standalone-lock moves | TICKETED as KS-1379 (Wednesday Q3 (c)) with the gate42 condition | STILL OPEN (ticket); its condition is requirement 3 — queue and m365 standalone suites green both sides (MEASURED), shared DID NOT START standalone |',
 '| N-1339-3 | Minor: mobile undici 6.28.0 in GHSA-3wwx range | wording now "in scope" (READY) | READ the PR body for the wording |',
 '| N-1339-4 | Minor: root undici 5.29.0 in 12 baselined ranges; stale `// overrides` comment | not addressed | STILL OPEN, Polish |',
 '| N-1339-5 | Minor: `npm ls ip-address --all` ELSPROBLEMS at head | not addressed (locks unchanged) | STILL OPEN (the locks are byte-identical to round 1) |',
 '| N-1339-6 | Minor: seat evidence faults | the round-2 READY discloses `--no-verify` on `git commit` (no commit hook exists, measured by the seat) | the gate grades the disclosure |',
 '| N-1339-7 | Polish: @types/nodemailer unused by tsc under 10 | not addressed | the drafter\'s --listFilesOnly at the head reads BOTH the bundled dist/cjs declarations and @types/nodemailer files (%s) — the gate says whether @types is still load-bearing |' % j(SU['tsc_reads'].get('head_auth')), '',
 '## Develop at the pin',
 'Pinned over develop **`%s`** (tree `%s`), READ by ls-remote and fetched. Merge-base MEASURED: `%s` (develop itself: the develop move since it is EMPTY). END_TREE **`%s`** (%s), %d merge-tree call(s).' % (
     P['develop'], P['develop_tree'], pr['merge_base'][:12], P['end_tree'], P['end_shortstat'], P['merge_tree_calls']),
 'The launch action\'s step 3b re-pins on any further move.', '',
 '## Overlaps — `merged_blob_paths` NONE, `noop_paths` NONE; ELEVEN OPEN PRs DECLARED as overlapping (kit.json `dead_open_declared`, mode open_manifest_overlap)',
 '- Every other OPEN PR at the pin that is not declared (%d, the PULLS API census): disjoint from every kit path (the round-2 email.ts included).' % len(P['inflight']),
 '- DECLARED, each measured EQUAL by predict (c): %s. None is in this kit, none is merged by it; after #1339 lands each conflicts on those manifests / locks. If any MERGES FIRST, develop moves over #1339\'s own paths and the launch action\'s re-pin refuses rc 10.' % '; '.join(
     '#%s (%s) %s' % (b, (P['dead_open_declared'].get(b, {}).get('title') or '')[:48], [rp(x) for x in v['paths']]) for b, v in sorted(DOS.items(), key=lambda x: -int(x[0]))),
 '- `merged_blob_paths` NONE and `noop_paths` NONE — two different declarations, each asserted empty by predict (c).', '',
 '## The drafter\'s measurements (installprobe_1.out; controls %s)' % ('ALL PASS' if all(IP['controls'].values()) else j(IP['controls'])),
 '- Controls: %s.' % j(IP['controls']),
 '- Summary: %s.' % j(SU),
 '- NOT measured by the drafter: the ROOT workspace install and require.resolve from each service dir; the auth / originate / other lock-touched / issuer suites; the census-named tests; eslint; the audit legs and contract (network: npm advisory API); the SMTP sink through the emitted JS; the seat\'s arms; packages/shared\'s suite on its standalone install (did not start).', '',
 '## Fleet STOP (READ, bounded region, NOT-FOUND control)']
s = S[n]
out.append('- #%s `%s` (%d lines, %s): pre_push_hook_base %s · fixture_guard %s · run_shell_suites %s · %s; "%s"' % (n, os.path.basename(s['log']), s['lines'], s.get('rc'), s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['shell_suites'], s['verdict_line']))
out += ['- By path class #1339 changes no `*.test.sh`, script or migration (manifests, locks and two service source files). After this merge 28/0 · 6/0 · 49/0 · 60 of 60.', '']
out += ['## LEGITIMATE SHAPES — the drafter\'s predictions (the gate MEASURES every row; a row saying MEASURED is a drafter\'s run, still not the gate\'s evidence)', '| PR | prediction | predicted-by |', '|---|---|---|']
for l in pred.splitlines():
    m = re.match(r'^  #(\d+) (.*)$', l)
    if m:
        out.append('| #%s | %s | drafter %s (predict_1.out) |' % (m.group(1), m.group(2).replace('|', '/')[:1500], 'MEASURED' if 'MEASURED' in m.group(2)[:160] else 'READ'))
open(D + '/COMMISSION.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/COMMISSION.md', len(out), 'lines')
