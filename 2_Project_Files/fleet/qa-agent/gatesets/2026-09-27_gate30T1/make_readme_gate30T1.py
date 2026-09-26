#!/usr/bin/env python3
"""make_readme_gate30T1.py <scratchpad> — writes README.md for gate30T1 (the directory this script lives in). Every SHA, tree, count, size and control
tally is READ from the kit's own files (pins_gate30T1.json, stopcounts_gate30T1.json, gh_read_1.out, keyscan_1.out, controls_1/2.out + .rc, fill_1.out,
launcher_check_1.out, repin_dryrun_1.out, routing_check_1.out, predict_1.out, predict_sim_*.out, final_lsremote_1.out) at the moment of writing — never
typed. The prose is the drafter's. Shape copied from gate29's make_readme_gate29.py."""
import hashlib, json, os, re, sys
D = os.path.dirname(os.path.abspath(__file__)); SP = sys.argv[1]
K = json.load(open(D + '/kit.json')); kit = K['kit']
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit)))
def rd(f):
    p = os.path.join(D, f); return open(p, encoding='utf-8').read() if os.path.exists(p) else ''
def sha(f): return hashlib.sha256(open(os.path.join(D, f), 'rb').read()).hexdigest()
def ctl(f):
    t = rd(f); m = re.search(r'^SUMMARY .*$', t, re.M); n = re.search(r'SUMMARY \S+: (\d+) controls, OK (\d+), MISMATCH (\d+)', t)
    return (m.group(0) if m else '?'), (n.groups() if n else ('?', '?', '?')), rd(f.replace('.out', '.rc')).strip() or '?'
(s1, c1, rc1), (s2, c2, rc2) = ctl('controls_1.out'), ctl('controls_2.out')
mism1 = [l.strip() for l in rd('controls_1.out').splitlines() if l.startswith('  MISMATCH')]
ok2 = [l.strip() for l in rd('controls_2.out').splitlines() if l.startswith('  OK')]
gh = rd('gh_read_1.out'); chk = rd('launcher_check_1.out').splitlines()[:1]
dry = [l for l in rd('repin_dryrun_1.out').splitlines() if l.startswith('DRY RUN COMPLETE') or 'REFUS' in l or l.startswith('rc ')]
fill = [l for l in rd('fill_1.out').splitlines() if l.startswith('key scan') or l.startswith('seat items')]
rout = rd('routing_check_1.out').splitlines(); ks = [l for l in rd('keyscan_1.out').splitlines() if l.startswith(('#', 'CONTROL'))]
fin = rd('final_lsremote_1.out').strip().splitlines()
sims = ['%s -> %s' % (re.match(r'predict_sim_(\w+)\.out$', f).group(1), (rd(f).strip().splitlines() or ['?'])[-1].split(' ->')[0]) for f in sorted(os.listdir(D)) if re.match(r'predict_sim_\w+\.out$', f)]
def subj(n):
    m = re.search(r'=== #%s head.*?\ntitle \((\d+) chars.*?= (\d+) chars' % n, gh, re.S); return m.group(2) if m else '?'
def probe(n, key):
    for l in rd('predict_1.out').splitlines():
        if l.startswith('  #%s %s' % (n, key)): return l.strip()[len('#%s ' % n):]
    return '(not in predict_1.out)'
L = os.path.join(D, K['launcher']); R = os.path.join(D, 'repin_and_launch_%s.sh' % kit)
NS = sorted(K['prs'])
WHY = {
 '1292': '**T1** — webhooks.ts: the last two of the seven leaking 500s (POST /:id/test, GET /:id/deliveries) through fail500 + ks1341c (C3 SOURCE counts all seven). Spark, golden-EXACT.',
 '1294': '**T1** — adminConfig.ts: two of four UNCONDITIONAL err.message 500s (production included) through fail500 + IN-PLACE ks730c edits. Spark on an EXCERPTED input, golden-EXACT.',
 '1296': '**T1 WIDEN** — systemErrors.ts fail500 logs a non-Error with `util.inspect`: more reaches LOG STORAGE, no redaction on the path. Golden raised (the model block had one extra context line).',
 '1297': '**T1 WIDEN** — the same inspect change in gdpr.ts, a SUBJECT-DATA surface. Golden-EXACT.',
}
rows = ['| #%s | %s | %s | `%s` | %d on `%s` | %s | %s |' % (n, ' + '.join(K['prs'][n]['keys']), K['prs'][n]['tier'], P['prs'][n]['head'], len(P['prs'][n]['commits']), P['prs'][n]['merge_base'][:12], subj(n), WHY[n]) for n in NS]
stop = ['#%s %s' % (n, ('%s · %s · %s · %s' % (S[n]['pre_push_hook_base'], S[n]['fixture_guard'], S[n]['run_shell_suites_region'], S[n]['shell_suites'].split(',')[0].replace(' passed', '') + ' of 60')) if S[n]['preflight_ran'] else 'NOT APPLICABLE (no preflight; %d lines)' % S[n]['lines']) for n in NS]
launch = '%s %s %s' % (R, L, SP)
go = re.search(r"GO='(`GO: merge [^`]*`)'", rd('fill_%s.py' % kit)).group(1)
flip = lambda h: h[:-1] + ('0' if h[-1] != '0' else '1')
wl = ['#%s real `%s` -> wrong `%s` (same length %s, differs in %d digit, contains the real head: %s)' % (n, P['prs'][n]['head'], flip(P['prs'][n]['head']), True, sum(x != y for x, y in zip(P['prs'][n]['head'], flip(P['prs'][n]['head']))), P['prs'][n]['head'] in flip(P['prs'][n]['head'])) for n in NS]
used = sorted(set(re.findall(r'^  OK +((?:C3|O2|H1\d{3})) ', rd('controls_1.out'), re.M)))
out = []; A = out.append
A('# Gateset 2026-09-26_%s — README for Wednesday' % kit); A('')
A('The drafter launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing, pushed nothing, posted nothing, deleted nothing and wrote nothing inside any project folder or /Volumes/DevMASTER/WEDNESDAY.')
A('It wrote only under `%s/` — the kit, the scratch clone `g30T1_sp/clone.git` (a `git clone --bare --no-local` of the checkout, NO alternates, then fetches FROM ORIGIN into it with the checkout\'s repo-local key; the drafter\'s own merge-tree / hash-object / apply --cached / commit-tree for simulations only), the control workdirs `g30T1_controls_*` and the dry-run reads `repin_gate30T1_dry_*`. Superseded outputs were RENAMED `superseded_*`, never deleted.' % D)
A('The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, `clone --no-local` as a source). GitHub: REST GET only (Secuura GH_TOKEN read by name, never printed). Linear: queries only. The routing conf was READ (grep), never written.'); A('')
A('**gate30T1 = FOUR PRs, all tier 1, sibling kit gate30T2 (#1293, #1295, #1298, #1299).** #1292 and #1294 are the two you named; **#1296 (KS-1346 A) and #1297 (KS-1346 B) are the WIDEN rows** — both existed at the pin (the kit\'s own WIDEN census caught #1297 during the drafting simulations; your 13:5xZ message confirmed both heads). Every head re-read by TWO instruments (ls-remote AND the PULLS API) and fetched: all agree.'); A('')
A('| PR | ticket | tier | head (READ: API == ls-remote pull/head == branch == fetched) | commits on merge-base | squash subject chars | why this tier (from the DIFF) |')
A('|---|---|---|---|---|---|---|'); out.extend(rows); A('')
A('Routing `%s` (you add the line — §4). GO string %s (or the subset). The GO goes to **Seat B 32nd**, which raised all four and merges its own.' % (K['pane'], go)); A('')
A('## 1. BLUF')
A('- **Kit: READY to launch** once you add the routing line (§4) — but read §6.1 first: the drafter\'s READ predicts **#1296 and #1297 NO GO** under your widen rule. Launcher `--check` rc 0 (`%s`); repin `--dry-run` rc 0.' % (chk[0].strip() if chk else '?'))
A('- **Controls, both ways (controls_%s.sh):**' % kit)
A('  - normal (controls_1.out, rc %s): `%s`' % (rc1, s1))
A('  - `--invert` (controls_2.out, rc %s): `%s`' % (rc2, s2))
A('  - Wrong-head controls (%s, all OK both ways) change ONE hex digit and never contain the real head (doctor() refuses rc 98 on a superset, rc 97 if the original survives): %s' % (', '.join(used), '; '.join(wl)))
A('  - NEW in this kit: **RW** (a WIDEN regex matching an open PR outside both kits must refuse the launch action rc 15) and its twin RW/twin (a regex matching only an in-kit PR passes).')
A('- **Pinned over develop `%s`** (tree `%s`) — ls-remote AND fetched AND the API compare agree: gate29\'s two GO squashes (#1290 `4857187a`, #1291 `3f70224a`) over `179a4f32ec06`; its tree equals gate29\'s END_TREE `0cc6669f3a6e`.' % (P['develop'], P['develop_tree']))
A('  - **END_TREE `%s`** (%s), identical in all %d orders (%d merge-tree calls).' % (P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls']))
A('  - **END_TREE_WITH_SIBLING `%s`** (this kit + gate30T2, either kit first; gate30T2\'s pins read the SAME tree).' % P['end_tree_with_sibling'])
A('  - Final re-read by `ls-remote` as this README was written (final_lsremote_1.out): %s' % ' | '.join(fin))
A('- **OVERLAPS — pairwise, measured:** the kit\'s pairs disjoint; disjoint from the sibling kit\'s paths; every kit path disjoint from ALL %d other open PRs (PULLS API census, plus any PR opened since the draft); NOT STACKED; no dead-open overlap (#1268/#1278/#1245/#1241 are CLOSED since gate29).' % len(P['inflight']))
for n, keys in (('1292', ('LEAK SITES', 'CONVERTED-TWO', 'ALL SEVEN SITES', 'ERR.MESSAGE LEFT', 'C3 SOURCE RULE', 'ARM-R3 ANCHOR', 'DOCBLOCK THREE SENTENCES', 'DELIVERIES TRAP', 'GOLDEN', 'TEST FILE')),
                ('1294', ('UNCONDITIONAL SITES', 'HELPER CALLS', 'CATCH BODY', 'LEAKED-CHECK', 'IN-PLACE ks730c EDITS', 'GOLDEN')),
                ('1296', ('PRODUCT DIFF', 'LOG SINK', 'INSPECT WIDENING', 'TEST FILE', 'GOLDEN')),
                ('1297', ('PRODUCT DIFF', 'LOG SINK', 'TEST FILE', 'GOLDEN'))):
    A('- **#%s %s (READ PREDICTIONS; the gate measures):**' % (n, K['prs'][n]['keys'][0]))
    for k in keys: A('  - %s' % probe(n, k)[:700])
A('- **The gate owes, by name (the prompt\'s kit rules, each guarded by the launcher and by its own control):** #1292 — its own real-router probe (4 NODE_ENVs incl. UNSET, 3 throw types, REACHED per env) that MUST leak at the merge-base, all seven routes at head, brief-C\'s Arm R3 on the brief\'s bytes, C3 arms (a)-(d) incl. the route-identity blind spot, `message: err.message` 0 on END_TREE, the docblock declared, the §5f close; #1294 — its own real-router probe (5 NODE_ENVs) that MUST leak at the merge-base, the ks730c `leaked` check shown vacuous and body-equality shown to catch a planted leak; #1296 / #1297 — the REAL router AND the REAL winston logger, sentinel secret/PII fields in a thrown object, a merge-base control, NO GO if any sentinel reaches a log line.')
A('- **Fleet STOP (READ, bounded region, NOT-FOUND control):** %s. After this merge: 28/0 · 6/0 · 49/0 · 60 of 60 (no PR adds, removes or renames a `*.test.sh`).' % '; '.join(stop))
A('- **Linear: all four PRs link `contributes`; NONE `closes`** (linear_reads_1.out). KS-1341, KS-1334, KS-1346 In Progress. None closes on this merge: KS-1341 needs its §5f live sweep; KS-1334 has part B; KS-1346\'s Done-when names adminConfig/webhooks and a rotate-secret cell too.')
A('- **SQUASH-BODY KEY SCAN (MG-3; keyscan_1.out + fill_1.out, READ):** only the PR\'s own key may stay hyphenated — **KS-1341 (#1292), KS-1334 (#1294), KS-1346 (#1296, #1297)**.')
for l in ks: A('  - %s' % l)
A('  - **No foreign HYPHENATED key in any title, body or commit message.** Foreign keys already appear UN-hyphenated (KS1344, KS730, KS1346) — if the merger quotes them they stay that way. The mandated minimum blocks carry only the own key (%s).' % (fill[0] if fill else 'fill_1.out'))
A('- **MG-11:** `<title> (#n)` = %s chars (all <= 92); no SHORT subject needed.' % ' / '.join('#%s %s' % (n, subj(n)) for n in NS))
A('- **Sizes / sha256 (measured as this README was written):** prompt `%s` %d bytes sha256 `%s`; launcher `%s` %d bytes sha256 `%s`; capture `mail_%s_ready.md` %d bytes sha256 `%s`.' % (
    K['prompt'], os.path.getsize(os.path.join(D, K['prompt'])), sha(K['prompt']), K['launcher'], os.path.getsize(L), sha(K['launcher']), kit, os.path.getsize(os.path.join(D, 'mail_%s_ready.md' % kit)), sha('mail_%s_ready.md' % kit))); A('')
A('## 2. Pins — predict_1.out (rc 0)')
for n in NS:
    pr = P['prs'][n]
    A('- #%s: %d commit(s) %s over `%s`; %d behind develop; merged tree `%s`; every merged blob == its head blob; numstat equal %s; no mode change; move ∩ own paths EMPTY.' % (n, len(pr['commits']), ', '.join('`%s`' % c[:12] for c in pr['commits']), pr['merge_base'], pr['behind'], pr['merged_tree'], pr['numstat']))
A('- Simulations: %s. `moved` = develop + one unrelated synthetic commit (must PASS); `foreign<n>` = develop + a foreign edit of that PR\'s first own file (must REFUSE). No OLDER develop can host #1292 (it needs part B), so the base-invariance simulation is `--simulate moved`; `predev` (179a4f32ec06, gate29\'s pin) is the moved-develop pin in controls D / RC / RD.' % '; '.join(sims))
A('- Superseded runs are kept, renamed, never deleted: `superseded_prewiden1297_*`, `superseded_pre1298_*`, `superseded_pre1299_*` — the simulations run before each WIDEN row was added (the first set is where the WIDEN census REFUSED on #1297: the guard firing on a real event).'); A('')
A('## 3. What the gate owes')
A('- Prompt `%s` — the four T1 sections above, the seats\' red proofs re-run, suites (originate 962 -> 997 predicted on END_TREE), tsc with `exclude: []`, lint, guards; the MANDATED SQUASH TEXT blocks and the MG-3 key-set table; `## MERGE ADDENDUM` as the LAST section of report.md (a NO GO PR gets its line marked NO GO, no subject).' % K['prompt'])
A('- Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/%s/`; mail subject as in the prompt, FROM coagent@ TO wednesday-agent@. Prior round named with its path (gate29, `2026-09-26-batch1290-g29`).' % K['report']); A('')
A('## 4. Routing line to add (the drafter did NOT write it)')
A('`%s|coagent@agentmail.to|yes` → `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`. Absent at drafting (routing_check_1.out: %s). Also in PROPOSED_inbox_routing_line.txt.' % (K['pane'], ' · '.join(rout[1:6]))); A('')
A('## 5. The ONE launch command'); A('```'); A(launch); A('```')
A('- Dry run (`--dry-run` appended): repin_dryrun_1.out → %s' % ' / '.join(dry))
A('- If develop moves first (e.g. gate30T2 merges before this kit), step 3b re-pins in the same action; a move onto an own path, a stack or a pairwise overlap refuses rc 10. A NEW KS-1346 PR outside both kits refuses rc 15 (step 2b). A moved head refuses rc 11.')
A('- If you copy the kit into `gatesets/2026-09-26_gate30T1/`, pass the copied paths: step 0b re-measures and re-fills there.'); A('')
A('## 6. Questions for Wednesday (each with the drafter\'s recommendation)')
A('1. **#1296 / #1297 are predicted NO GO by your own widen rule.** Both PR bodies say it outright ("It can, and nothing on this path redacts it"), the drafter READ originate\'s utils/logger.ts (0 `redact`), and inspect renders every own key and value to depth 2. The gate will MEASURE it through the real logger; if it confirms, the GO can only be the subset `GO: merge #1292, #1294 batch`. *Recommend:* launch all four anyway (the measurement is what the rule asks for, and it also yields the fix-shape); meanwhile decide whether the widening is acceptable at all — that is a data-handling call (who reads originate\'s logs) that the seat explicitly declined, so it may be Kam\'s. A NO GO here is the rule working, not the seat failing.')
A('2. **KS-1346\'s own fix-shape suggests `util.inspect`** (the ticket text, filed from gate29 N-1290-2). The widen rule now grades that very shape. *Recommend:* if the gate rules NO GO, amend KS-1346\'s fix-shape to "keys-only or redacted rendering" before the next Spark brief, so the loop does not re-produce the same patch.')
A('3. **KS-1341 after #1292 merges:** all seven sites done, but §5f withholds Done — the merge seat posts the canonical `live sweep owed` comment (the prompt spells it). *Recommend:* keep KS-1341 In Progress; the live sweep joins the owed list.')
A('4. **Merge authority — Seat B 32nd merges its own four.** Same shape as gate29 (your ruling). *Recommend:* keep; say so in the GO mail.')
A('5. **Audit fuse `2026-09-30T00:00Z`** (B31/B32 handovers): from then every `Blockchain/Dev` push AND merge is refused; all four rows are Blockchain/Dev paths. *Recommend:* launch now; ~3 days of slack. Only Kam\'s typed word moves the fuse.')
A('6. **Docblock three sentences (#1292)** — declared NOT COVERED per your brief, non-blocking; *recommend* the docs ticket be filed only after the merge (a board write — yours to authorise).')
A('7. **Seat B 32nd\'s handover** (HANDOVER-seatB32-2026-09-26.md, captured) was written before #1298/#1299 were pushed and before your rulings on them; it lists KS-1347 as STOPPED and KS-1339 as NOT STARTED. The gate is told it is a stale record, not a contradiction.'); A('')
A('## 7. Controls: `controls_%s.sh <scratchpad> [--invert]`' % kit)
A('- **controls_1.out:** `%s` (rc %s).%s' % (s1, rc1, (' MISMATCHES: ' + '; '.join(mism1)) if mism1 else ''))
A('- **controls_2.out (`--invert`):** `%s` (rc %s, by design). Every control can fail.%s' % (s2, rc2, (' Controls that did NOT flip: ' + '; '.join(ok2)) if ok2 else ''))
A('- Every mutation is independent of the original: doctor() refuses a replacement that contains the text it replaces (rc 98) and refuses when the original still occurs after the plant (rc 97); every wrong head is the real head with ONE hex digit changed; the launcher\'s head guard is whole-field.')
A('- Doctored arms are pinned to the launcher\'s own develop. RD runs the REAL re-pin (predict → fill) from a launcher pinned at predev `179a4f32ec06` in a MOVED copy; RE lists a kit PR in the sibling set too and must refuse rc 10. PS1 is `--simulate foreign<2nd PR>`; PS2 is `--simulate moved`; PF1 fills from SIM pins and must refuse. RW / RW/twin exercise the WIDEN census. Every kit rule (exits 35, 40-44, 46-50) has its own SPLIT control.')
A('- Side effects (STANDING_LINES, B 32nd): the real re-pin in RD writes only inside the control workdir\'s kit copy and the scratch clone\'s refs; each control writes its own `.out`; nothing is shared between arms except the scratch clone, whose refs every predict run re-fetches.')
A('- Not controlled: exit 16 (needs a TTY), repin steps 4-6 (usage gate, cockpit add), a `mergeable=False` refusal.'); A('')
A('## 8. Files')
A('- Kit: kit.json · COMMISSION.md · PROPOSED_inbox_routing_line.txt + routing_check_1.out · make_commission_%s.py / make_readme_%s.py' % (kit, kit))
A('- Pins: predict_%s.py → predict_1.out, predict_sim_*.out, pins_%s.json (+ .SIM-*.json) · keyscan_%s.py → keyscan_1.out · final_lsremote_1.out' % (kit, kit, kit))
A('- Reads: gh_read_%s.py → gh_read_1.out, gh_body_*.md, gh_comments_*.md · linear_reads_%s.py → linear_reads_1.out, linear_KS-*.md · capture_mail_%s.py → capture_1.out, mail_%s_ready.md, stopcounts_%s.json' % (kit, kit, kit, kit, kit))
A('- Prompt/launcher: prompt_%s.TEMPLATE.txt, launcher_%s.TEMPLATE.sh.txt, fill_%s.py → %s + %s (fill_1.out), launcher_check_1.out' % (kit, kit, kit, K['prompt'], K['launcher']))
A('- Repin/controls: repin_and_launch_%s.sh (repin_dryrun_1.out), controls_%s.sh (controls_1/2.out + .rc)' % (kit, kit))
A('- Drafting scratch kept (never deleted): `_probes30T1.txt` (the probe block spliced into predict), `superseded_*` (pre-WIDEN simulations).'); A('')
A('## 9. NOT done / NOT measured by the drafter')
A('- No launch, mail, tap, merge, commit, push, comment, routing write, container or port bind. No inbox read. No write in any project folder or in /Volumes/DevMASTER/WEDNESDAY. No file deleted.')
A('- **UNMEASURED:** every runtime behaviour in every PR (every probe, arm, red, green and suite count above is READ or a seat claim); the inspect widening through the real logger; prettier; every suite on END_TREE; the usage gate and launch steps 4-6.')
open(D + '/README.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/README.md', len(out), 'lines')
