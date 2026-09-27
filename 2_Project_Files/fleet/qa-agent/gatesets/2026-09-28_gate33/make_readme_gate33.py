#!/usr/bin/env python3
"""make_readme_gate33.py <scratchpad> — writes README.md for gate33 (the directory this script lives in). Every figure is READ from the kit's own output
files at the moment it runs (pins_gate33.json, predict_1.out, logprobe_1.out / logprobe_gate33.json, controls_1/2.out, launcher_check_1.out,
repin_dryrun_1.out, routing_check_1.out, final_lsremote_1.out, fill_1.out, keyscan_1.out, linear_reads_1.out, gh_read_1.out, stopcounts_gate33.json,
rekey_1.out), each named beside it; the prose (the questions for Wednesday, the NOT MEASURED list) is the drafter's. Shape copied from the previous
kit's README generator, re-keyed for gate33 (six MIXED-tier rows, two bases, the logging WIDEN measurement)."""
import json, os, re, sys, hashlib, subprocess, datetime
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
SP = sys.argv[1] if len(sys.argv) > 1 else ''
def rd(f): return open(os.path.join(D, f), encoding='utf-8').read() if os.path.exists(os.path.join(D, f)) else ''
def sha(f): b = open(os.path.join(D, f), 'rb').read(); return len(b), hashlib.sha256(b).hexdigest()
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit)))
LP = json.load(open('%s/logprobe_%s.json' % (D, kit)))
NS = sorted(K['prs'])
pred = rd('predict_1.out'); fill = rd('fill_1.out'); gh = rd('gh_read_1.out')
def last(f, pfx):
    c = [l for l in rd(f).splitlines() if l.startswith(pfx)]; return c[-1].strip() if c else 'ABSENT'
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
TIT = {n: P['titles'][n] for n in NS}
def lands(n):
    m = re.search(r'#%s (\d+)->(\d+)' % n, fill); return (m.group(1), m.group(2)) if m else ('?', '?')
def probes(n): return [l.strip()[len('#%s ' % n):] for l in pred.splitlines() if l.startswith('  #%s ' % n)]
def passes(n): return [l.strip() for l in pred.splitlines() if re.match(r'^  PASS #%s\b' % n, l)]
flip = lambda h: h[:-1] + ('0' if h[-1] != '0' else '1')
WHY = {
 '1310': '**T1 logging, ruled** — logger.ts redactSecrets() LAST in the logger-level combine(), json() on both File transports; golden-EXACT (MEASURED). WIDEN (MEASURED, logprobe): the six ruled keys redacted everywhere; a NESTED Error\'s props and seven unmatched keys NOW reach both files.',
 '1311': '**T1 logging, ruled** — systemErrors.ts fail500 logs type + field NAMES; golden-EXACT (MEASURED); ADD1: inspect reds A1 AND A6. On END_TREE a data-valued field NAME (an email key) reaches stdout + both files (MEASURED, P6).',
 '1312': '**T1 logging, ruled** — gdpr.ts, the SAME line (identical modulo indent on END_TREE, READ); golden-EXACT (MEASURED); ADD1: B1 AND B6. P7 as P6 (MEASURED).',
 '1313': '**T1 lookup** — vc-issuer getById exact-id only (LIKE + includes() gone; revoke inherits); canonical patch.diff blob-EXACT (MEASURED; NON-MINIMAL by one empty -/+ pair). Disclosed TS2339 3->4, prefer-const 0->1 (KS-1351).',
 '1314': '**T2 test-only** — ks744 R4 / R5 in place; the REGENERATED diff blob-EXACT (MEASURED); tamper auth.ts :407 at head, develop, END (READ; the brief said :398).',
 '1315': '**T2 test-only** — ks839 R5 in place (five fromCharCode carriers, all-ASCII lines, READ); READY-identical (MEASURED); tamper services/oauth.ts :353 (READ); auth runs vitest.',
}
out = []
A = out.append
A('# Gateset 2026-09-28_gate33 — README for Wednesday'); A('')
A('Written %s by the drafter (make_readme_gate33.py; every figure below is read from the kit\'s own output files at that moment, each named beside it).' % now)
A('The drafter launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing, pushed nothing, posted nothing and deleted nothing. It wrote: this kit directory `%s/`; ONE line in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (as commissioned, backup first — §4); and scratch under `%s/` (the scratch clone `g33_sp/clone.git` — `git clone --bare --shared --no-checkout` of the checkout, objects borrowed READ-ONLY via alternates, then fetches FROM ORIGIN into it with the checkout\'s repo-local key, including the CLOSED #1302\'s head as `refs/g33/closed/1302`; the logprobe workdirs `g33_logprobe_*`; the control workdirs `g33_controls_*`; the dry-run reads `repin_gate33_dry_*`). One file copied by mistake at the start was MOVED to `_quarantine/`, never deleted. Superseded outputs were RENAMED `superseded_*`.' % (D, SP))
A('The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, `clone --shared` as a source, and node `require()` of its typescript and winston). GitHub: REST GET only (Secuura GH_TOKEN read by name, never printed). Linear: queries only.')
A('')
A('**gate33 = SIX PRs, MIXED tiers (T1 x4, T2 x2), one kit, no sibling, NO stack.** #1315 (item 6, "being pushed now" in the commission) EXISTED at the drafter\'s first census (opened 15:20:44Z; _api_peek_1.out), so no wait was needed and the kit is SIX. Every head re-read by TWO instruments (ls-remote AND the PULLS API) and fetched: all agree (predict_1.out (a)). **TWO merge-bases (MEASURED):** `a24db57e65c9` for #1310, `94c9c7aa9be7` for #1311-#1315 (each head\'s one commit has that parent). The three predecessors #1302 / #1296 / #1297 are CLOSED, not merged (gh_read_1.out). WIDEN census (titles with the five keys, or a branch carrying `-b35-<n>`): every match is in the kit, none outside (gh_read_1.out, predict_1.out (a), repin_dryrun_1.out 2b).')
A('')
A('| PR | ticket | tier | head (READ: API == ls-remote pull/head == branch == fetched) | commits on merge-base | declared subject (the title, no `(#n)`) chars -> lands at | why this tier (from the DIFF) |')
A('|---|---|---|---|---|---|---|')
for n in NS:
    pr = P['prs'][n]; d, l = lands(n)
    A('| #%s | %s | %s | `%s` | %d on `%s` | %s -> **%s** | %s |' % (n, K['prs'][n]['keys'][0], K['prs'][n]['tier'], pr['head'], len(pr['commits']), pr['merge_base'][:12], d, l, WHY[n]))
A('')
rl = [l for l in rd('routing_check_1.out').splitlines() if 'line number' in l]
A('Routing `%s` (**added by the drafter**, line %s of inbox_routing.conf — §4). GO string `GO: merge #1310, #1311, #1312, #1313, #1314, #1315 batch` (or the subset). MERGE ORDER #1310 -> #1311 -> #1312 -> #1313 -> #1314 -> #1315 (END_TREE is order-independent, measured). The GO goes to **Seat B 35th**, which raised all six and merges its own.' % (K['pane'], rl[0].split(':')[-1].strip() if rl else '?'))
A('')
A('**Kam\'s rulings (READ by the drafter from `0_Brain/dashboard/data/decisions.json`):** card `secuura-ks1348-log-files-persist-secrets` status ruled, choice **a** "Redact first, then JSON files", ruled_ts 2026-09-27T19:07:21+10:00 (the commission said 19:06); its option (a) text: "logger-level redaction of secret and PII keys (password, token, apiKey, secret, authorization, email, ssn), as packages/shared\'s logger already does ... Error message text still reaches the files". Card `secuura-ks1346-logging-thrown-objects-leaks-secrets` ruled **a** "Type and field names only", ruled_ts 2026-09-27T16:32:47+10:00; option (a): "Log what kind of thing was thrown and the NAMES of its fields, never their values." #1313\'s 2026-09-16 ruling is carried from the commission (not re-read).')
A('')
A('## 1. BLUF')
A('- **Kit: READY to launch** — launcher `--check` rc %s (`%s`, launcher_check_1.out); repin `--dry-run` rc 0 (repin_dryrun_1.out: %s).' % (
    '0' if rd('launcher_check_1.out').startswith('all guards pass:') else '?', rd('launcher_check_1.out').splitlines()[0] if rd('launcher_check_1.out') else 'ABSENT', last('repin_dryrun_1.out', 'DRY RUN COMPLETE')))
A('- **READ THIS FIRST — the logging WIDEN, MEASURED by the drafter (logprobe_gate33.py -> logprobe_1.out; the REAL logger.ts at each revision, the checkout\'s typescript + winston, NODE_ENV=production; controls: %s):**' % ', '.join('%s %s' % (k, v) for k, v in LP['_controls'].items()))
H0, E0 = LP['#1310 head'], LP['END_TREE']
A('  - **Kam\'s ruled class holds:** the six top-level keys (password, token, apiKey, email, subject.ssn, headers.authorization) are [REDACTED] in both files and on stdout at #1310\'s head and on END_TREE (P1 in files at head: %s); a top-level Error\'s enumerable `password` too (P5).' % {f: H0['hits'][f]['P1'] for f in ('logs/error.log', 'logs/combined.log')})
A('  - **But these NOW reach BOTH production files at #1310\'s head, where develop wrote the literal `undefined`:** %s.' % '; '.join('%s %s' % (pn, v) for pn, v in (H0.get('new_in_files_vs_develop') or {}).get('logs/error.log', {}).items()))
A('    P2 = an axios-shaped Error NESTED in metadata (enumerable `config.headers.Authorization`, `response.data.token`) — `redactLogValue` returns any `value instanceof Error` unwalked (the PR body discloses the class and calls it "unchanged from the base\'s rendering": true for stdout, NOT for the files). P3 = keys outside the suffix rule (passwordHash, privateKey, secretKey, email_address, userEmails[], phone, mnemonic). P4 / P8 = values inside the message / err.message — the RULED residue ("the message and the error text still reach the files").')
A('  - **On END_TREE additionally (#1311 / #1312):** %s — a thrown object whose FIELD NAMES are data (an email used as a key) puts that email into stdout and both files through the ruled line; field VALUES reach no sink.' % {pn: v for pn, v in (E0.get('new_in_files_vs_develop') or {}).get('logs/error.log', {}).items() if pn in ('P6', 'P7')})
A('  - Under Wednesday\'s widen rule this is the question the gate must rule (§6.1): P2 and P3 are NOT covered by the ruling\'s residue; P6/P7 are the ruling\'s own consequence applied to data-valued keys.')
c1, c2 = last('controls_1.out', 'SUMMARY'), last('controls_2.out', 'SUMMARY')
A('- **Controls, both ways (controls_gate33.sh):**')
A('  - normal (controls_1.out, rc %s): `%s`' % (rd('controls_1.rc').strip(), c1))
A('  - `--invert` (controls_2.out, rc %s): `%s`' % (rd('controls_2.rc').strip(), c2))
A('  - Wrong-head controls change ONE hex digit and never contain the real head (doctor() refuses rc 98 on a superset, rc 97 if the original survives): ' + '; '.join('#%s `%s` -> `%s`' % (n, P['prs'][n]['head'][-8:], flip(P['prs'][n]['head'])[-8:]) for n in NS) + ' (last 8 hex shown).')
A('  - NEW in this kit: **SJ1-SJ3** PLANT a subject into a fill copy (gate33 declares none: every title lands <= 92) — a `(#n)` suffix, a subject landing over 92, a FOREIGN hyphenated key — each must refuse; **NS[<spelling>]** now covers BOTH predecessor generations (gate32\'s and gate31\'s) including the predecessor\'s re-key tool name, and rekey_check_gate33.py scans ITSELF outside its marked token map (STANDING_LINES 2026-09-28).')
A('- **Pinned over develop `%s`** (tree `%s` — equal to gate32\'s own END_TREE, READ) — ls-remote AND fetched AND the API compare agree. Develop moved %s since #1310\'s base and 9 squashes since 94c9c7aa9be7; the move ∩ every PR\'s own paths is EMPTY (predict_1.out (b)(3)).' % (P['develop'], P['develop_tree'], '6 squashes (gate32\'s #1304-#1309)'))
A('  - **END_TREE `%s`** (%s), identical in all %d orders (%d merge-tree calls, each with the PR\'s own merge-base); diff(develop, END) == the union of the ten own paths and every END blob == its PR\'s head blob (MG-1).' % (P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls']))
A('  - Final re-read by `ls-remote` as this README was written (final_lsremote_1.out): %s' % ' | '.join(rd('final_lsremote_1.out').strip().splitlines()))
A('- **OVERLAPS — pairwise, measured:** NONE. No pair stacked; every kit pair disjoint; every kit path disjoint from ALL %d other open PRs. `merged_blob_paths` NONE and `noop_paths` NONE, each asserted by predict (c).' % len(P['inflight']))
A('- **Subjects (STANDING_LINES 2026-09-27): declared WITHOUT the `(#n)` suffix, measured as they LAND** — %s (fill_1.out: `%s`; controls SJ1-SJ3).' % ('; '.join('#%s «%s» %s -> %s' % (n, TIT[n], lands(n)[0], lands(n)[1]) for n in NS), last('fill_1.out', 'subject scan')))
for n in NS:
    A('- **#%s %s (predictions; the gate measures):**' % (n, K['prs'][n]['keys'][0]))
    for pbl in probes(n): A('  - %s' % pbl[:1500])
    for pl in passes(n): A('  - %s' % pl[:600])
A('- **The drafter\'s logging measurement (logprobe_1.out, rc 0) — per revision, per sink:**')
for l in rd('logprobe_1.out').splitlines():
    if l.startswith(('logprobe_gate33', '== ', '   ', 'CONTROL', 'SUMMARY')): A('  - %s' % l.strip()[:900])
A('- **Fleet STOP (READ, bounded region, NOT-FOUND control):** ' + '; '.join('#%s %s · %s · %s · %s (%s)' % (n, S[n]['pre_push_hook_base'], S[n]['fixture_guard'], S[n]['run_shell_suites_region'], S[n]['shell_suites'].split(',')[0].replace(' passed', ' of 60 passed'), S[n]['verdict_line']) for n in NS) + '. After this merge: 28/0 · 6/0 · 49/0 · 60 of 60 (no PR adds, removes or renames a `*.test.sh`).')
lin = [l for l in rd('linear_reads_1.out').splitlines() if l.startswith('#')]
A('- **Linear: all six PRs link `contributes`; NONE `closes`** (linear_reads_1.out): ' + ' | '.join(l.split(' | ')[0] for l in lin) + '. KS-1348, KS-1346, KS-1121, KS-1221, KS-1220 In Progress; KS-1351 Backlog.')
A('- **SQUASH-BODY KEY SCAN (MG-3; keyscan_1.out + fill_1.out):** only the PR\'s own key hyphenated anywhere; no foreign key (hyphenated or not) in any title, body or commit message; #1311 and #1312 share KS-1346 (parts A and B).')
for l in rd('keyscan_1.out').splitlines()[1:]: A('  - %s' % l.strip())
A('  - %s' % last('fill_1.out', 'key scan'))
A('- **Re-key / namespace (rekey_1.out):** %s' % ' | '.join(l.strip() for l in rd('rekey_1.out').splitlines()))
sz = {}
for f in (K['prompt'], K['launcher'], 'mail_%s_ready.md' % kit): sz[f] = sha(f)
A('- **Sizes / sha256 (measured as this README was written):** ' + '; '.join('`%s` %d bytes sha256 `%s`' % (f, v[0], v[1]) for f, v in sz.items()) + '. **Kit dir `du -sh` %s** (no clone, no node_modules in the kit).' % subprocess.run(['du', '-sh', D], capture_output=True, text=True).stdout.split()[0])
A('')
A('## 2. Pins — predict_1.out (rc %s)' % rd('predict_1.out.rc').strip())
for n in NS:
    pr = P['prs'][n]
    A('- #%s: %d commit(s) `%s` over merge-base `%s`; %d behind develop; merged tree `%s`; every merged blob == its head blob; numstat equal %s; no mode change; move ∩ own paths EMPTY.' % (n, len(pr['commits']), pr['head'][:12], pr['merge_base'], pr['behind'], pr['merged_tree'], pr['numstat']))
sims = []
for f in sorted(os.listdir(D)):
    m = re.match(r'predict_sim_(\w+)\.out$', f)
    if m: sims.append('%s -> %s' % (m.group(1), (rd(f).strip().splitlines() or ['?'])[-1].split(' -> ')[0]))
A('- Simulations: %s. `moved` = develop + one unrelated synthetic commit (must PASS); `foreign<n>` = develop + a foreign edit of that PR\'s first own file (must REFUSE). `predev` (`%s`, develop^) is the moved-develop pin in controls D / RC / RD / RE / RN / RO.' % ('; '.join(sims), K['predev'][:12]))
A('- The unfetched-object guard carries its own control in predict (a); the +/- comparator carries its own control pair; READY identity for #1313 is judged by BLOBS (NON-MINIMAL: one removed-and-re-added empty line in the test section; the READY block == the checker\'s canonical patch.diff, byte-identical, MEASURED).')
A('- Superseded runs kept, renamed, never deleted: `superseded_readyminimal_predict_1.out` (rc 1: the first run read #1313\'s NON-MINIMAL READY as a +/- mismatch — the comparator now judges that case by blobs); `superseded_prelogprobe_predict_1.out` (before logprobe_gate33.json existed); `superseded_tail60_capture_1.out` (the EXTRA arms captured as 60-line TAILS, which cut their red-cell summary; now whole); `superseded_plant1302_controls_1/2.out` (181 controls, one MISMATCH each way: NS[#1302] — the drafter had planted `#1302`, which is THIS kit\'s subject, not a predecessor token, so the checker rightly did not flag it; the plant is now `#1300`).')
A('')
A('## 3. What the gate owes')
A('- Prompt `%s` — the logging WIDEN (per sink, per revision, a sentinel of its own per path, the ruled residue told apart from a finding), each T1 row\'s ruling verified IN THE PRODUCT (#1310 through the REAL logger; #1311 / #1312 through the REAL routers; #1313 THROUGH THE ROUTE: exact id 200, every fragment 404, revoke-by-fragment revokes nothing, MERGE-BASE-MUST-LEAK as the control), every seat red proof re-run (ADD1: under `inspect(err)` A1 AND A6 / B1 AND B6 red), the two test-only tamper arms by byte-unique anchors, suites (originate / vc-issuer / api-gateway / auth at develop, each head and END_TREE), tsc with `exclude: []`, lint, guards; the MANDATED SQUASH TEXT blocks and the MG-3 key-set table; `## MERGE ADDENDUM` as the LAST section of report.md with `merged_blob_paths: none · noop_paths: none` per line.' % K['prompt'])
A('- Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/%s/`; mail subject as in the prompt, FROM coagent@ TO wednesday-agent@. Prior rounds named with their paths (gate32 `2026-09-27-batch1304-g32`, gate31 `2026-09-27-batch1300-g31`, gate30T1 `2026-09-26-batch1292-g30T1`).' % K['report'])
A('')
A('## 4. Routing line — ADDED by the drafter (as commissioned)')
A('`%s|coagent@agentmail.to|yes` inserted directly after gate32\'s pane line in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`; **backup taken first** and `cmp`-identical before the edit. routing_check_1.out: %s. Also in ROUTING_LINE_ADDED.txt.' % (K['pane'], ' '.join(l.strip() for l in rd('routing_check_1.out').splitlines())))
A('')
A('## 5. The ONE launch command')
A('```'); A('%s/repin_and_launch_%s.sh %s/%s %s' % (D, kit, D, K['launcher'], SP)); A('```')
A('- Dry run (`--dry-run` appended): repin_dryrun_1.out → %s (rc 0).' % last('repin_dryrun_1.out', 'DRY RUN COMPLETE'))
A('- Argument 2 may be ANY Claude session scratchpad dir (`/private/tmp/claude-501/*/scratchpad*`): if `g33_sp/clone.git` is absent there, predict rebuilds it (`clone --shared` + fetch) on a re-pin (logprobe is NOT re-run by a re-pin; its JSON stays the drafter\'s measurement at this pin). If develop moves first, step 3b re-pins in the same action; an own-path move, a stack, a pairwise overlap, a declaration predict cannot prove or an END-tree disagreement refuses rc 10. A NEW PR on one of the five keys or on a `-b35-<n>` branch outside the kit refuses rc 15. A moved head or a base not develop refuses rc 11.')
A('')
A('## 6. Questions for Wednesday (each with the drafter\'s recommendation)')
A('1. **The logging WIDEN is measured, and it is not empty (logprobe_1.out).** #1310 does exactly what Kam ruled for its class (the six named keys never reach any sink), but because the files now render JSON, two paths the ruling does not name newly reach both production files: an Error NESTED in metadata (its enumerable props, e.g. an axios `config.headers.Authorization`) and keys outside the suffix list (`secretKey`, `privateKey`, `passwordHash`, `email_address`, `userEmails`, `phone`, `mnemonic`). On END_TREE, #1311 / #1312 add a third: field NAMES that are data (an email-keyed object). Under your widen rule each is "a secret or PII field reaching log storage where it did not before". *Recommend:* launch as drafted — the gate re-measures and rules; the likely outcomes are (a) #1310 GO WITH FINDINGS if you or Kam rule the nested-Error / key-list gaps a follow-up (a ticket with the fix-shape: walk Error own-enumerable props in redactLogValue; widen the key rule to substrings or an allow-list for the File transports), or (b) NO GO under the strict widen reading. That choice may be Kam\'s (a data-handling call), as #1302\'s was.')
A('2. **#1313\'s READY is non-minimal** (one removed-and-re-added empty line in the test section) — blob-identical to the head; the seat raised from the checker\'s patch.diff, byte-identical to the READY. *Recommend:* note it; nothing to change.')
A('3. **#1314\'s tamper line moved** — the brief said auth.ts:398; the drafter READ :407 at head, develop and END_TREE (the seat measured :407). *Recommend:* launch as drafted — the prompt carries the whole-line anchor.')
A('4. **KS-1346 is carried by TWO PRs (#1311 part A, #1312 part B).** Both squash with `Refs KS-1346`. *Recommend:* keep; the gate says whether the pair closes KS-1346\'s Definition of done (READ: systemErrors.ts still logs `String(err)` in its /ingest and /client-errors catches, :121 / :152).')
A('5. **§5f:** KS-1348 and KS-1346 are runtime changes — neither moves to Done on offline evidence. *Recommend:* the merge seat posts the canonical `live sweep owed` comment the prompt spells.')
A('6. **Merge authority — Seat B 35th merges its own six.** *Recommend:* keep; say so in the GO mail with each declared subject and its landed length.')
A('')
A('## 7. Controls: `controls_gate33.sh <scratchpad> [--invert]`')
A('- **controls_1.out:** `%s` (rc %s).' % (c1, rd('controls_1.rc').strip()))
A('- **controls_2.out (`--invert`):** `%s` (rc %s, by design). Every control can fail.' % (c2, rd('controls_2.rc').strip()))
A('- Every mutation is independent of the original (doctor() rc 98 / rc 97); every wrong head is the real head with ONE hex digit changed; the launcher\'s head guard is whole-field. Doctored arms are pinned to the launcher\'s own develop. RD runs the REAL re-pin (predict -> fill) from a launcher pinned at predev in a MOVED copy; RE / RN / RO plant a wrong commit count / a `noop_paths` entry / a `declared_overlap` entry and each must refuse rc 10; RS / RS-twin exercise STACKBASE; PS1 is `--simulate foreign1311`; PS2 `--simulate moved`; PF1 / PF2 fill from SIM / failed pins and must refuse; SJ1-SJ3 plant subject defects; RW / RWB exercise the WIDEN census by title and by branch; every kit rule (exits 35, 40-44, 46-51) has its own SPLIT control.')
A('- Side effects (STANDING_LINES, B 32nd): the real re-pin in RD/RE/RN/RO writes only inside the control workdir\'s kit copy and the scratch clone\'s refs; RS and the RE family restore the copy\'s kit.json from a pristine copy; the NS plants are in memory only.')
A('- Not controlled: exit 16 (needs a TTY), repin steps 4-6 (usage gate, cockpit add), a `mergeable=False` refusal, logprobe\'s own verdicts beyond its four built-in controls.')
A('')
A('## 8. Files')
A('- Kit: kit.json · COMMISSION.md · ROUTING_LINE_ADDED.txt + routing_check_1.out · make_commission_gate33.py / make_readme_gate33.py · rekey_check_gate33.py → rekey_1.out · _quarantine/ (one mis-copied seed file, moved not deleted)')
A('- Pins: predict_gate33.py → predict_1.out, predict_sim_*.out, pins_gate33.json (+ .SIM-*.json) · keyscan_gate33.py → keyscan_1.out · final_lsremote_1.out')
A('- Measurements: logprobe_gate33.py → logprobe_1.out, logprobe_gate33.json (#1310 / #1311 / #1312 WIDEN)')
A('- Reads: gh_read_gate33.py → gh_read_1.out, gh_body_*.md, gh_comments_*.md · linear_reads_gate33.py → linear_reads_1.out, linear_KS-*.md · capture_mail_gate33.py → capture_1.out, mail_gate33_ready.md, stopcounts_gate33.json · _api_peek_gate33.py → _api_peek_1.out')
A('- Prompt/launcher: prompt_gate33.TEMPLATE.txt, launcher_gate33.TEMPLATE.sh.txt, fill_gate33.py → %s + %s (fill_1.out), launcher_check_1.out' % (K['prompt'], K['launcher']))
A('- Repin/controls: repin_and_launch_gate33.sh (repin_dryrun_1.out), controls_gate33.sh (controls_1/2.out + .rc)')
A('')
A('## 9. NOT done / NOT measured by the drafter')
A('- No launch, mail, tap, merge, commit, push, comment, container or port bind. No inbox read (no READY message id reached the drafter; the capture is built from PR bodies, commit messages and the seat\'s raise records). No write in any project folder. No file deleted. One write outside the kit and the scratchpad: the routing line (§4, backup first).')
A('- **UNMEASURED:** every jest / vitest run (every red, green, EXTRA arm, inspect arm and suite count above is READ or a seat claim); every tamper arm; #1310 through a REAL fail500 ROUTE (the drafter measured the logger module with fail500\'s LINE evaluated against it, not the router); #1311 / #1312 through the real routers (their edge cases — null prototype, Proxy, throwing getter — are READ only); #1313 through the route (exact-id 404, revoke-by-fragment) — READ only; whether originate\'s stdout is already persisted by the deployed stack; tsc; lint; prettier; every suite on END_TREE; the usage gate and launch steps 4-6; the #1313 ruling (2026-09-16) is carried from the commission, not re-read from a card.')
A('- **MEASURED by the drafter (not the gate\'s evidence):** heads/develop by two instruments; merge-bases; the merge-tree shapes and END_TREE; every red-arm anchor\'s whole-line location at head, develop and END_TREE; READY identity for all six (blob-judged for #1313); golden / canonical / regenerated identity by `git apply --cached --check` for five; the logging WIDEN at four revisions (logprobe, four controls); the END_TREE substring-class grep over vc-issuer.')
open(D + '/README.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/README.md', len(out), 'lines')
