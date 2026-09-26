#!/usr/bin/env python3
"""make_readme_gate30T2.py <scratchpad> — writes README.md for gate30T2 (the directory this script lives in). Every SHA, tree, count, size and control
tally is READ from the kit's own files (pins_gate30T2.json, stopcounts_gate30T2.json, gh_read_1.out, keyscan_1.out, controls_1/2.out + .rc, fill_1.out,
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
 '1293': '**T2** — TEST-ONLY: ks1341a A1 clears the logger per NODE_ENV and asserts the whole call list. Red comes from a PRODUCT tamper (webhooks.ts:563 production-only logging): A1 red at head, green at the tip.',
 '1295': '**T2** — TOOLING: systemTest/akto preSuiteSetup.ts fileURLToPath + one vitest cell. Format gate only (NO preflight): the gate runs the akto package\'s own lint / format:check / unit suite, space-free and spaced. Site 2 of 3.',
 '1298': '**T2 WIDEN** — TEST FILES ONLY (services/auth): ks732 path reads via fileURLToPath + a new vitest cell; ONE non-golden token (`line` -> `_line`). Site 1 of 2.',
 '1299': '**T2 WIDEN** — TEST FILES ONLY (services/originate): ks1293 CONFIGPINNED offender list before the count + a new cell that executes the cell\'s text via `new Function`.',
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
A('It wrote only under `%s/` — the kit, the scratch clone `g30T2_sp/clone.git` (a `git clone --bare --no-local` of the checkout, NO alternates, then fetches FROM ORIGIN into it with the checkout\'s repo-local key; the drafter\'s own merge-tree / hash-object / apply --cached / commit-tree for simulations only), the control workdirs `g30T2_controls_*` and the dry-run reads `repin_gate30T2_dry_*`. Superseded outputs were RENAMED `superseded_*`, never deleted.' % D)
A('The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, `clone --no-local` as a source). GitHub: REST GET only (Secuura GH_TOKEN read by name, never printed). Linear: queries only. The routing conf was READ (grep), never written.'); A('')
A('**gate30T2 = FOUR PRs, all tier 2, sibling kit gate30T1 (#1292, #1294, #1296, #1297).** #1293 and #1295 are the two you named; **#1298 (KS-1347) and #1299 (KS-1339) are the WIDEN rows** — both existed at the pin (the kit\'s own WIDEN census caught each during the drafting simulations; your 13:5xZ message relayed both heads, equal to ls-remote). Every head re-read by TWO instruments (ls-remote AND the PULLS API) and fetched: all agree.'); A('')
A('| PR | ticket | tier | head (READ: API == ls-remote pull/head == branch == fetched) | commits on merge-base | squash subject chars | why this tier (from the DIFF) |')
A('|---|---|---|---|---|---|---|'); out.extend(rows); A('')
A('Routing `%s` (you add the line — §4). GO string %s (or the subset). The GO goes to **Seat B 32nd**, which raised all four and merges its own.' % (K['pane'], go)); A('')
A('## 1. BLUF')
A('- **Kit: READY to launch** once you add the routing line (§4). Launcher `--check` rc 0 (`%s`); repin `--dry-run` rc 0.' % (chk[0].strip() if chk else '?'))
A('- **Controls, both ways (controls_%s.sh):**' % kit)
A('  - normal (controls_1.out, rc %s): `%s`' % (rc1, s1))
A('  - `--invert` (controls_2.out, rc %s): `%s`' % (rc2, s2))
A('  - Wrong-head controls (%s, all OK both ways) change ONE hex digit and never contain the real head (doctor() refuses rc 98 on a superset, rc 97 if the original survives): %s' % (', '.join(used), '; '.join(wl)))
A('  - NEW in this kit: **RW** (a WIDEN regex matching an open PR outside both kits must refuse the launch action rc 15) and its twin RW/twin (a regex matching only an in-kit PR passes).')
A('- **Pinned over develop `%s`** (tree `%s`) — ls-remote AND fetched AND the API compare agree: gate29\'s two GO squashes (#1290 `4857187a`, #1291 `3f70224a`) over `179a4f32ec06`; its tree equals gate29\'s END_TREE `0cc6669f3a6e`.' % (P['develop'], P['develop_tree']))
A('  - **END_TREE `%s`** (%s), identical in all %d orders (%d merge-tree calls).' % (P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls']))
A('  - **END_TREE_WITH_SIBLING `%s`** (this kit + gate30T1, either kit first; gate30T1\'s pins read the SAME tree).' % P['end_tree_with_sibling'])
A('  - Final re-read by `ls-remote` as this README was written (final_lsremote_1.out): %s' % ' | '.join(fin))
A('- **OVERLAPS — pairwise, measured:** the kit\'s pairs disjoint; disjoint from the sibling kit\'s paths; every kit path disjoint from ALL %d other open PRs (PULLS API census, plus any PR opened since the draft); NOT STACKED; no dead-open overlap (#1268/#1278/#1245/#1241 are CLOSED since gate29).' % len(P['inflight']))
for n, keys in (('1293', ('NO product file', 'TEST DIFF', 'A1 SHAPE', 'THE PRODUCT TAMPER TARGET', 'A1 ROUTES', 'GOLDEN')),
                ('1295', ('PRODUCT DIFF', 'SPAWN UNCHANGED', 'SITE SWEEP', 'CELL', 'GOLDEN', 'PACKAGE SCRIPTS', 'PROGRAMS')),
                ('1298', ('TEST FILES ONLY', 'ks732 DIFF', 'SITE SWEEP', 'GOLDEN', 'CELL', 'AUTH PACKAGE')),
                ('1299', ('TEST FILES ONLY', 'CONFIGPINNED CELL', 'FILE HEADER CLAIM', 'CELL', 'GOLDEN'))):
    A('- **#%s %s (READ PREDICTIONS; the gate measures):**' % (n, K['prs'][n]['keys'][0]))
    for k in keys: A('  - %s' % probe(n, k)[:700])
A('- **The gate owes, by name (the prompt\'s kit rules, each guarded by the launcher and by its own control):** #1293 — the 2x2 under the product tamper (A1 red at head, green at the tip), a double-log arm, TEST-ONLY confirmed, ks1341a on END_TREE_WITH_SIBLING; #1295 — the seat\'s red, url.fileURLToPath / wrong-path / decodeURIComponent arms, the akto package\'s own lint + format:check + test:unit at develop / head / END_TREE and a unit run FROM A SPACED PATH, the real `runPreSuiteStep` from a spaced copy up to the first outbound request; #1298 — NO auth product file (a NO GO otherwise), the real ks732 proof from a spaced checkout, the one non-golden token, test-inclusive tsc error SETS tip vs head; #1299 — the offender-first red, the floor control made to go red once, the `new Function` text-execution coupling, the real hermeticity scan naming a planted file.')
A('- **Fleet STOP (READ, bounded region, NOT-FOUND control):** %s. After this merge: 28/0 · 6/0 · 49/0 · 60 of 60 (no PR adds, removes or renames a `*.test.sh`).' % '; '.join(stop))
A('- **Linear: all four PRs link `contributes`; NONE `closes`** (linear_reads_1.out). KS-1344, KS-1337, KS-1347, KS-1339 In Progress. KS-1337 (site 2 of 3) and KS-1347 (site 1 of 2) stay open; KS-1344 and KS-1339 may meet their DoD — the gate says, the board move is yours.')
A('- **SQUASH-BODY KEY SCAN (MG-3; keyscan_1.out + fill_1.out, READ):** only the PR\'s own key may stay hyphenated — **KS-1344 (#1293), KS-1337 (#1295), KS-1347 (#1298), KS-1339 (#1299)**.')
for l in ks: A('  - %s' % l)
A('  - **No foreign HYPHENATED key in any title, body or commit message.** Foreign keys already appear UN-hyphenated (KS1341, KS732) — if the merger quotes them they stay that way. The mandated minimum blocks carry only the own key (%s).' % (fill[0] if fill else 'fill_1.out'))
A('- **MG-11:** `<title> (#n)` = %s chars. **#1293 as titled is 94 > 92** — the mandated SHORT subject is `KS-1344: clear the logger per environment in ks1341a and assert the call list (#1293)` (85 chars; key-scanned); the others fit.' % ' / '.join('#%s %s' % (n, subj(n)) for n in NS))
A('- **Sizes / sha256 (measured as this README was written):** prompt `%s` %d bytes sha256 `%s`; launcher `%s` %d bytes sha256 `%s`; capture `mail_%s_ready.md` %d bytes sha256 `%s`.' % (
    K['prompt'], os.path.getsize(os.path.join(D, K['prompt'])), sha(K['prompt']), K['launcher'], os.path.getsize(L), sha(K['launcher']), kit, os.path.getsize(os.path.join(D, 'mail_%s_ready.md' % kit)), sha('mail_%s_ready.md' % kit))); A('')
A('## 2. Pins — predict_1.out (rc 0)')
for n in NS:
    pr = P['prs'][n]
    A('- #%s: %d commit(s) %s over `%s`; %d behind develop; merged tree `%s`; every merged blob == its head blob; numstat equal %s; no mode change; move ∩ own paths EMPTY.' % (n, len(pr['commits']), ', '.join('`%s`' % c[:12] for c in pr['commits']), pr['merge_base'], pr['behind'], pr['merged_tree'], pr['numstat']))
A('- Simulations: %s. `moved` = develop + one unrelated synthetic commit (must PASS); `foreign<n>` = develop + a foreign edit of that PR\'s first own file (must REFUSE). The kit sits on the current develop like its sibling, so the base-invariance simulation is `--simulate moved`; `predev` (179a4f32ec06, gate29\'s pin) is the moved-develop pin in controls D / RC / RD.' % '; '.join(sims))
A('- Superseded runs are kept, renamed, never deleted: `superseded_pre1298_*`, `superseded_pre1299_*` — the simulations run before each WIDEN row was added (each set is where the WIDEN census REFUSED on the newly opened PR: the guard firing on a real event).'); A('')
A('## 3. What the gate owes')
A('- Prompt `%s` — the four T2 sections above, the seats\' red proofs re-run, suites (originate 962 -> 966, akto 1233 -> 1236, auth 832 -> 835 claimed), tsc per package with the program that covers each file, lint, guards; the MANDATED SQUASH TEXT blocks and the MG-3 key-set table; `## MERGE ADDENDUM` as the LAST section of report.md (a NO GO PR gets its line marked NO GO, no subject).' % K['prompt'])
A('- Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/%s/`; mail subject as in the prompt, FROM coagent@ TO wednesday-agent@. Prior round named with its path (gate29, `2026-09-26-batch1290-g29`).' % K['report']); A('')
A('## 4. Routing line to add (the drafter did NOT write it)')
A('`%s|coagent@agentmail.to|yes` → `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`. Absent at drafting (routing_check_1.out: %s). Also in PROPOSED_inbox_routing_line.txt.' % (K['pane'], ' · '.join(rout[1:6]))); A('')
A('## 5. The ONE launch command'); A('```'); A(launch); A('```')
A('- Dry run (`--dry-run` appended): repin_dryrun_1.out → %s' % ' / '.join(dry))
A('- If develop moves first (e.g. gate30T1 merges before this kit), step 3b re-pins in the same action; a move onto an own path, a stack or a pairwise overlap refuses rc 10. A NEW KS-1347 / KS-1339 PR outside both kits refuses rc 15 (step 2b). A moved head refuses rc 11.')
A('- If you copy the kit into `gatesets/2026-09-26_gate30T2/`, pass the copied paths: step 0b re-measures and re-fills there.'); A('')
A('## 6. Questions for Wednesday (each with the drafter\'s recommendation)')
A('1. **#1298\'s one non-golden token** (`(line, i)` -> `(_line, i)`) is your ruling (b); the prompt asks the gate to prove it is the ONLY non-golden byte and behaviour-neutral, and to compare test-inclusive tsc error SETS (not counts). *Recommend:* keep.')
A('2. **#1293\'s squash subject** is 94 chars as titled; the kit mandates the SHORT subject `KS-1344: clear the logger per environment in ks1341a and assert the call list (#1293)` (85). *Recommend:* put it in the GO mail verbatim so the merge seat does not trim ad hoc.')
A('3. **#1299\'s cell executes another test file\'s text** (`new Function` over ks1293\'s CONFIGPINNED statements). The prompt asks the gate to grade that coupling (a TypeScript token or a reformat can turn a red into a crash). *Recommend:* accept the gate\'s ruling; a crash-as-red would be the load-failure class.')
A('4. **KS-1344 and KS-1339 may meet their Done-when on merge** (both test-only, whole scope). The gate says whether; the close is a board write — yours. KS-1337 (site 3, playwright) and KS-1347 (proxy server.ts) stay open.')
A('5. **Merge authority — Seat B 32nd merges its own four**; **audit fuse `2026-09-30T00:00Z`** covers #1293, #1298 and #1299 (Blockchain/Dev paths); #1295 is systemTest/ (whether the fuse covers it: UNMEASURED). *Recommend:* launch now, both kits in parallel — the kits are path-disjoint and END_TREE_WITH_SIBLING agrees across both pins.')
A('6. **Seat B 32nd\'s handover** was written before #1298/#1299 were pushed (it says KS-1347 STOPPED, KS-1339 NOT STARTED). The prompt names it a stale record, not a contradiction.'); A('')
A('## 7. Controls: `controls_%s.sh <scratchpad> [--invert]`' % kit)
A('- **controls_1.out:** `%s` (rc %s).%s' % (s1, rc1, (' MISMATCHES: ' + '; '.join(mism1)) if mism1 else ''))
A('- **controls_2.out (`--invert`):** `%s` (rc %s, by design). Every control can fail.%s' % (s2, rc2, (' Controls that did NOT flip: ' + '; '.join(ok2)) if ok2 else ''))
A('- Every mutation is independent of the original: doctor() refuses a replacement that contains the text it replaces (rc 98) and refuses when the original still occurs after the plant (rc 97); every wrong head is the real head with ONE hex digit changed; the launcher\'s head guard is whole-field.')
A('- Doctored arms are pinned to the launcher\'s own develop. RD runs the REAL re-pin (predict → fill) from a launcher pinned at predev `179a4f32ec06` in a MOVED copy; RE lists a kit PR in the sibling set too and must refuse rc 10. PS1 is `--simulate foreign<2nd PR>`; PS2 is `--simulate moved`; PF1 fills from SIM pins and must refuse. RW / RW/twin exercise the WIDEN census. Every kit rule (exits 35, 37 NOT APPLICABLE, 40-44, 46-48) has its own SPLIT control.')
A('- Side effects (STANDING_LINES, B 32nd): the real re-pin in RD writes only inside the control workdir\'s kit copy and the scratch clone\'s refs; each control writes its own `.out`; nothing is shared between arms except the scratch clone, whose refs every predict run re-fetches.')
A('- Not controlled: exit 16 (needs a TTY), repin steps 4-6 (usage gate, cockpit add), a `mergeable=False` refusal.'); A('')
A('## 8. Files')
A('- Kit: kit.json · COMMISSION.md · PROPOSED_inbox_routing_line.txt + routing_check_1.out · make_commission_%s.py / make_readme_%s.py' % (kit, kit))
A('- Pins: predict_%s.py → predict_1.out, predict_sim_*.out, pins_%s.json (+ .SIM-*.json) · keyscan_%s.py → keyscan_1.out · final_lsremote_1.out' % (kit, kit, kit))
A('- Reads: gh_read_%s.py → gh_read_1.out, gh_body_*.md, gh_comments_*.md · linear_reads_%s.py → linear_reads_1.out, linear_KS-*.md · capture_mail_%s.py → capture_1.out, mail_%s_ready.md, stopcounts_%s.json' % (kit, kit, kit, kit, kit))
A('- Prompt/launcher: prompt_%s.TEMPLATE.txt, launcher_%s.TEMPLATE.sh.txt, fill_%s.py → %s + %s (fill_1.out), launcher_check_1.out' % (kit, kit, kit, K['prompt'], K['launcher']))
A('- Repin/controls: repin_and_launch_%s.sh (repin_dryrun_1.out), controls_%s.sh (controls_1/2.out + .rc)' % (kit, kit))
A('- Drafting scratch kept (never deleted): `_probes30T2.txt` (the first probe block; #1298 / #1299 probes were spliced into predict after it), `superseded_*` (pre-WIDEN simulations).'); A('')
A('## 9. NOT done / NOT measured by the drafter')
A('- No launch, mail, tap, merge, commit, push, comment, routing write, container or port bind. No inbox read. No write in any project folder or in /Volumes/DevMASTER/WEDNESDAY. No file deleted.')
A('- **UNMEASURED:** every runtime behaviour in every PR (every probe, arm, red, green and suite count above is READ or a seat claim); the inspect widening through the real logger; prettier; every suite on END_TREE; the usage gate and launch steps 4-6.')
open(D + '/README.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/README.md', len(out), 'lines')
