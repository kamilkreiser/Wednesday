#!/usr/bin/env python3
"""make_readme_gate29.py <scratchpad> — writes README.md for gate29 (the directory this script lives in). Every SHA, tree, count and control
tally is READ from the kit's own files (pins_gate29.json, stopcounts_gate29.json, gh_read_1.out, keyscan_1.out, controls_1/2.out + .rc, fill_1.out,
launcher_check_1.out, repin_dryrun_1.out, routing_check_1.out, predict_1.out, predict_sim_*.out, final_lsremote_1.out) at the moment of writing —
never typed. The prose is the drafter's. Shape copied from gate28's make_readme_gate28.py."""
import json, os, re, sys
D = os.path.dirname(os.path.abspath(__file__)); SP = sys.argv[1]
K = json.load(open(D + '/kit.json')); kit = K['kit']
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit)))
gh = open(D + '/gh_read_1.out').read()
def rd(f):
    p = os.path.join(D, f); return open(p).read() if os.path.exists(p) else ''
def ctl(f):
    t = rd(f); m = re.search(r'^SUMMARY .*$', t, re.M); n = re.search(r'SUMMARY \S+: (\d+) controls, OK (\d+), MISMATCH (\d+)', t)
    return (m.group(0) if m else '?'), (n.groups() if n else ('?', '?', '?')), rd(f.replace('.out', '.rc')).strip() or '?'
(s1, c1, rc1), (s2, c2, rc2) = ctl('controls_1.out'), ctl('controls_2.out')
mism1 = [l.strip() for l in rd('controls_1.out').splitlines() if l.startswith('  MISMATCH')]
ok2 = [l.strip() for l in rd('controls_2.out').splitlines() if l.startswith('  OK')]
wrong = [l.strip() for l in rd('controls_1.out').splitlines() if re.match(r'^  OK +(C3|O2|H\d+) ', l)]
chk = rd('launcher_check_1.out').splitlines()[:1]
dry = [l for l in rd('repin_dryrun_1.out').splitlines() if l.startswith('DRY RUN COMPLETE') or 'REFUS' in l or l.startswith('rc ')]
fill = [l for l in rd('fill_1.out').splitlines() if l.startswith('key scan') or l.startswith('seat items')]
rout = rd('routing_check_1.out').splitlines()
ks = [l for l in rd('keyscan_1.out').splitlines() if l.startswith('#')]
fin = rd('final_lsremote_1.out').strip().splitlines()
sims = []
for f in sorted(os.listdir(D)):
    m = re.match(r'predict_sim_(\w+)\.out$', f)
    if m: sims.append('%s -> %s' % (m.group(1), (rd(f).strip().splitlines() or ['?'])[-1].split(' ->')[0]))
def subj(n):
    m = re.search(r'=== #%s head.*?\ntitle \((\d+) chars.*?= (\d+) chars' % n, gh, re.S); return m.group(2) if m else '?'
def probe(n, key):
    for l in rd('predict_1.out').splitlines():
        if l.startswith('  #%s %s' % (n, key)): return l.strip()[len('#%s ' % n):]
    return '(not in predict_1.out)'
L = os.path.join(D, K['launcher']); R = os.path.join(D, 'repin_and_launch_%s.sh' % kit)
WHY = {
 '1290': '**T1** — originate webhooks.ts: what the WRITE routes (PATCH, DELETE, rotate-secret) answer on a 500 (information exposure; DELETE and rotate-secret MEASURED leaking in production by KS-1341). Part B of 3. Local-model patch (Spark).',
 '1291': '**T2** — tooling: systemTest/performance runner/cli.ts `fileURLToPath` + one vitest cell. No Blockchain/Dev path, so NO platform preflight ran; the gate runs the package\'s own lint + unit suite. 1 of 3 sites; DoD 2 approximated (disclosed).',
}
rows = ['| #%s | %s | %s | `%s` | %d on `%s` | %s | %s |' % (n, ' + '.join(K['prs'][n]['keys']), K['prs'][n]['tier'], P['prs'][n]['head'], len(P['prs'][n]['commits']), P['prs'][n]['merge_base'][:12], subj(n), WHY[n]) for n in sorted(K['prs'])]
stop = []
for n in sorted(K['prs']):
    s = S[n]
    stop.append('#%s %s' % (n, ('%s · %s · %s · %s' % (s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['shell_suites'].split(',')[0].replace(' passed', '') + ' of 60')) if s['preflight_ran'] else 'NOT APPLICABLE (no preflight: format gate only; every suite header NOT FOUND, %d lines)' % s['lines']))
launch = '%s %s %s' % (R, L, SP)
go = re.search(r"GO='(`GO: merge [^`]*`)'", open(D + '/fill_%s.py' % kit).read()).group(1)
out = []; A = out.append
A('# Gateset 2026-09-26_%s — README for Wednesday' % kit); A('')
A('The drafter launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing, pushed nothing, posted nothing, deleted nothing and wrote nothing inside any project folder or /Volumes/DevMASTER/WEDNESDAY.')
A('It wrote only under `%s/` — the kit, the scratch clone `g29_sp/clone.git` (a `git clone --bare --no-local` of the checkout, NO alternates, then a fetch FROM ORIGIN into it; the drafter\'s own merge-tree / hash-object / apply --cached writes only), the control workdirs `g29_controls_*` and the dry-run reads `repin_gate29_dry_*`.' % D)
A('The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, `clone --no-local` as a source). GitHub: REST GET only (Secuura GH_TOKEN read by name, never printed). Linear: queries only. The routing conf was READ (grep), never written.'); A('')
A('**gate29 = TWO PRs, tiers 1 and 2, one kit, no sibling.** Heads Wednesday relayed (ls-remote 19:1x AEST) re-read here by TWO instruments at the pin (ls-remote AND the PULLS API, and fetched): all agree; re-read once more by ls-remote as this README was written (§1).'); A('')
A('| PR | ticket | tier | head (READ: API == ls-remote pull/head == branch == fetched) | commits on merge-base | squash subject chars | why this tier (from the DIFF) |')
A('|---|---|---|---|---|---|---|'); out.extend(rows); A('')
A('Routing `%s` (you add the line — §4). GO string %s (or the subset). The GO goes to **Seat B 31st**, which raised both PRs and merges its own two (your staged answer to B31, `briefs_staged/2026-09-26_answer_seatB31_stay-live-for-gate29.md`).' % (K['pane'], go)); A('')
A('## 1. BLUF')
A('- **Kit: READY to launch** once you add the routing line (§4). Launcher `--check` rc 0 (`%s`); repin `--dry-run` rc 0.' % (chk[0].strip() if chk else 'launcher_check_1.out'))
A('- **Controls, both ways (controls_%s.sh):**' % kit)
A('  - normal (controls_1.out, rc %s): `%s`' % (rc1, s1))
A('  - `--invert` (controls_2.out, rc %s): `%s`' % (rc2, s2))
flip = lambda h: h[:-1] + ('0' if h[-1] != '0' else '1')   # the controls' own flip() rule
wl = []
for n in sorted(K['prs']):
    h = P['prs'][n]['head']; f = flip(h)
    wl.append('#%s real `%s` -> wrong `%s` (same length %s, differs in %d digit, contains the real head: %s)' % (n, h, f, len(f) == len(h), sum(x != y for x, y in zip(h, f)), h in f))
used = sorted(set(re.findall(r'^  OK +((?:C3|O2|H1\d{3})) ', rd('controls_1.out'), re.M)))
A('  - Wrong-head controls (%s, all OK both ways) change ONE hex digit and never contain the real head (doctor() refuses rc 98 on a superset, rc 97 if the original survives): %s' % (', '.join(used), '; '.join(wl)))
A('- **Pinned over develop `%s`** (tree `%s`) — read by ls-remote AND fetched AND the API compare agrees: it is the `179a4f32ec06` you named (#1289\'s squash, the last of gate28\'s three GOs over e080174c86c6). Its tree equals gate28\'s END_TREE `80a3d6968f67` exactly.' % (P['develop'], P['develop_tree']))
A('  - **END_TREE `%s`** (%s), identical in all %d orders (%d merge-tree calls). No sibling kit, so END_TREE_WITH_SIBLING == END_TREE (measured).' % (P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls']))
A('  - Final re-read by `ls-remote` as this README was written (final_lsremote_1.out): %s' % ' | '.join(fin))
A('- **OVERLAPS — pairwise, measured:** the kit pair disjoint; every kit path disjoint from ALL %d other open PRs (PULLS API census, incl. dead-open #1268/#1278/#1245/#1241, Seat L5\'s #1250/#1253, #995 on originate, #989 on the pre-suite step, dependabot); NOT STACKED; no dead-open overlap to declare.' % len(P['inflight']))
A('- **#1290 KS-1341 part B, T1 (READ PREDICTIONS; the gate measures):**')
for k in ('LEAK SITES', 'CONVERTED-THREE', 'UNCONVERTED-TWO', 'SECRET-PATH', 'UNTOUCHED BODIES', 'ARM-R3 ANCHOR', 'DOCBLOCK-STILL-FALSE', 'PATCH-400-BRANCH', 'GOLDEN', 'TEST FILE'):
    A('  - %s' % probe('1290', k)[:900])
A('  - **The gate owes, by name:** its OWN probe through the real router on all three routes x four NODE_ENVs (incl. UNSET) x Error/string/object throws, REACHED asserted PER ENVIRONMENT (logger cleared per run), a merge-base control that must leak; **Arm R3 run by the gate** with the brief\'s bytes (all three B1 rows red at `development`, B2 + controls green) and the same tamper under its own probe; rotate-secret driven both by `encryptField` and by a rejected UPDATE, with the generated `whsec_` value shown absent from the body AND every logger call.')
A('- **#1291 KS-1337, T2 (READ PREDICTIONS; the gate measures):**')
for k in ('PRODUCT DIFF', 'SPAWN UNCHANGED', 'NOT-COVERED SWEEP', 'DOD2-BOUNDARY', 'GOLDEN + FORMATTER DELTA', 'PACKAGE SCRIPTS', 'PROGRAMS'):
    A('  - %s' % probe('1291', k)[:900])
A('  - **NOT-COVERED disclosure: TRUE by READ.** Both named sites exist at develop exactly as the PR says (preSuiteSetup.ts:36, global-setup.ts:42), the sweep reads 3 at develop and 2 at head, and the cell has 0 spawn/exec calls (it cannot cross the CLI process boundary, so "DoD 2 approximated, not met" is accurate). **But the ticket\'s DoD 3 says "Measured today: 1 occurrence"** — the ticket undercounts; §6.3.')
A('  - **The gate owes, by name:** the package\'s own `npm ci`, `npm run lint` (tsc x2 + eslint), `format:check` and `test:unit` at develop / head / END_TREE (the push ran NO platform preflight), the red at develop + green at head, a wrong-but-unencoded-path arm, the formatter delta proven formatting-only, and a unit run FROM A SPACED PATH (the harness\'s `1114 failed=1` hypothesis).')
A('- **Fleet STOP (READ, bounded region, NOT-FOUND control):** %s. After this merge: 28/0 · 6/0 · 49/0 · 60 of 60 (no PR adds, removes or renames a `*.test.sh`).' % '; '.join(stop))
A('- **Linear: both PRs link `contributes`; NONE `closes`** (linear_reads_1.out). KS-1341 and KS-1337 In Progress; KS-1344 / KS-1345 / KS-1343 Backlog. Neither ticket closes on this merge (KS-1341 part B of 3; KS-1337 1 of 3 sites + DoD 2 approximated).')
A('- **SQUASH-BODY KEY SCAN (MG-3; keyscan_1.out + fill_1.out, READ):** only the PR\'s own key may stay hyphenated — **KS-1341 for #1290, KS-1337 for #1291.**')
for l in ks: A('  - %s' % l)
A('  - **#1290:** no foreign HYPHENATED key anywhere; its body names KS1344 and KS1345 and its commit message KS1344 **already un-hyphenated** — if the merger quotes either, they stay `KS1344` / `KS1345`.')
A('  - **#1291:** its PR BODY carries the foreign hyphenated **`KS-991`** (the pre-push hook line it quotes). If the squash body quotes that line it must read **`KS991`**; the commit message carries only `KS-1337`. The mandated minimum blocks carry only the own key (%s).' % (fill[0] if fill else 'fill_1.out'))
A('- **MG-11:** `<title> (#n)` = %s / %s chars (<= 92); no SHORT subject needed.' % (subj('1290'), subj('1291'))); A('')
A('## 2. Pins — predict_1.out (rc 0)')
for n in sorted(K['prs']):
    pr = P['prs'][n]
    A('- #%s: %d commit(s) %s over `%s`; %d behind develop; merged tree `%s`; every merged blob == its head blob; numstat equal %s; no mode change; move ∩ own paths EMPTY.' % (n, len(pr['commits']), ', '.join('`%s`' % c[:12] for c in pr['commits']), pr['merge_base'], pr['behind'], pr['merged_tree'], pr['numstat']))
A('- Simulations: %s. `moved` = develop + one unrelated synthetic commit (must PASS); `foreign<n>` = develop + a foreign edit of that PR\'s first own file (must REFUSE). No OLDER develop can host #1290 (it calls part A\'s fail500), so the base-invariance simulation is `--simulate moved`; `predev` (e080174c86c6, gate28\'s pin) is the moved-develop pin in controls D / RC / RD.' % '; '.join(sims))
A('- Superseded runs are kept, never deleted: `predict_superseded_probefix.out` (the first pinned run: same pins and FAIL=0; three READ probes were fixed after it — the function-body slicer, the spawn-line anchor and the tsconfig.node.json read).'); A('')
A('## 3. What the gate owes')
A('- Prompt `%s` (%d bytes) — #1290\'s T1 RUNTIME PROBE through the real router (three routes, four NODE_ENVs incl. UNSET, three throw types, REACHED per environment, a merge-base control that must leak), ARM R3 run by the gate, the rotate-secret SECRET-PATH section, the declared two; #1291\'s red design + disclosure grading and the package\'s own lint / format / unit gates; the MANDATED SQUASH TEXT blocks and the MG-3 key-set table.' % (K['prompt'], os.path.getsize(os.path.join(D, K['prompt']))))
A('- Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/%s/`; mail subject as in the prompt, FROM coagent@ TO wednesday-agent@.' % K['report']); A('')
A('## 4. Routing line to add (the drafter did NOT write it)')
A('`%s|coagent@agentmail.to|yes` → `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`. Absent at drafting (routing_check_1.out: %s). Also in PROPOSED_inbox_routing_line.txt.' % (K['pane'], ' · '.join(rout[1:5]))); A('')
A('## 5. The ONE launch command'); A('```'); A(launch); A('```')
A('- Dry run (`--dry-run` appended): repin_dryrun_1.out → %s' % ' / '.join(dry))
A('- If develop moves first, step 3b re-pins in the same action; a move onto an own path, a stack or a pairwise overlap refuses rc 10 (controls RD / RE).')
A('- If you copy the kit into `gatesets/2026-09-26_gate29/`, pass the copied paths: step 0b re-measures and re-fills there.'); A('')
A('## 6. Questions for Wednesday (each with the drafter\'s recommendation)')
A('1. **Merge authority — the author merges its own two.** gate28 wrote "never by an author"; per your staged answer, Seat B 31st (the author of both) is the merge seat, and the prompt says so (`MERGE_AUTH`, guarded by control A2). *Recommend:* keep — it is your ruling and the GO is sha-pinned and blob-gated either way; say so in the GO mail so the merge seat does not trip on gate28\'s wording.')
A('2. **Audit fuse `2026-09-30T00:00Z`** (B31 handover): from then every `Blockchain/Dev` push AND merge is refused. #1290 is a Blockchain/Dev path; #1291 is `systemTest/` (whether the fuse covers it: UNMEASURED). *Recommend:* launch now; the GO has ~3 days of slack.')
A('3. **KS-1337 DoD 3 undercounts.** The ticket says "Measured today: **1** occurrence"; the drafter\'s sweep (`git grep -nE "import\\.meta\\.url\\)\\.pathname" -- systemTest/`) reads **3** at develop — the PR\'s disclosure is right, the ticket is stale. *Recommend:* after the gate, a one-line ticket comment correcting DoD 3 to name the two remaining sites (a board write — yours to authorise; the gate files nothing).')
A('4. **#1290 docblock still false at part B** ("the only place in this router…", 2 sites remain). gate28 ruled it non-blocking at part A (N-1288-1). *Recommend:* same ruling; brief-C converts the last two and makes it true — note brief-C.md\'s tip line still reads `e080174c86c6` (READ), so it needs its own rev before queueing.')
A('5. **Arm R3 bytes.** The seat\'s armR3.py planted a BRACED variant of the brief\'s tamper; the prompt tells the gate to run the brief\'s own bytes and say whether the variant is equivalent. *Recommend:* accept that framing.')
A('6. **#1291 formatter delta** (Wednesday\'s ruling (b)): READ as +9/-6 golden → head on the test file only, cli.ts golden-EXACT. The gate proves formatting-only. *Recommend:* no action unless the gate finds a non-formatting byte.')
A('7. **READY mails NOT read** (no message id reached the drafter; a listing marks mail seen). Seat claims come from the PR bodies, the commit messages, HANDOVER-seatB31 and B31\'s red/green/arm/lint outputs (the capture).'); A('')
A('## 7. Controls: `controls_%s.sh <scratchpad> [--invert]`' % kit)
A('- **controls_1.out:** `%s` (rc %s).%s' % (s1, rc1, (' MISMATCHES: ' + '; '.join(mism1)) if mism1 else ''))
A('- **controls_2.out (`--invert`):** `%s` (rc %s, by design). Every control can fail.%s' % (s2, rc2, (' Controls that did NOT flip: ' + '; '.join(ok2)) if ok2 else ''))
A('- Every mutation is independent of the original: doctor() refuses a replacement that contains the text it replaces (rc 98) and refuses when the original still occurs after the plant (rc 97); every wrong head is the real head with ONE hex digit changed (same length, never a superset); the launcher\'s head guard is whole-field.')
A('- Doctored arms are pinned to the launcher\'s own develop. RD runs the REAL re-pin (predict → fill) from a launcher pinned at predev `e080174c86c6` in a MOVED copy; RE lists a kit PR in the (empty) sibling set too and must refuse rc 10. PS1 is `--simulate foreign1291`; PS2 is `--simulate moved`; PF1 fills from SIM pins and must refuse. Every kit rule (exits 35, 37 NOT APPLICABLE, 40-44, 46, 47, 49) has its own SPLIT control.')
A('- Not controlled: exit 16 (needs a TTY), repin steps 4-6 (usage gate, cockpit add), a `mergeable=False` refusal.'); A('')
A('## 8. Files')
A('- Kit: kit.json · COMMISSION.md (the drafter\'s READ predictions table) · PROPOSED_inbox_routing_line.txt + routing_check_1.out · make_commission_gate29.py / make_readme_gate29.py')
A('- Pins: predict_gate29.py → predict_1.out, predict_sim_*.out, pins_gate29.json (+ .SIM-*.json); predict_superseded_probefix.out · keyscan_1.out · final_lsremote_1.out')
A('- Reads: gh_read_gate29.py → gh_read_1.out, gh_body_*.md, gh_comments_*.md · linear_reads_gate29.py → linear_reads_1.out, linear_KS-*.md · capture_mail_gate29.py → capture_1.out, mail_gate29_ready.md, stopcounts_gate29.json')
A('- Prompt/launcher: prompt_gate29.TEMPLATE.txt, launcher_gate29.TEMPLATE.sh.txt, fill_gate29.py → %s + %s (fill_1.out), launcher_check_1.out' % (K['prompt'], K['launcher']))
A('- Repin/controls: repin_and_launch_gate29.sh (repin_dryrun_1.out), controls_gate29.sh (controls_1/2.out + .rc)')
A('- Drafting scratch kept (never deleted): `_probes29.txt` (the probe block spliced into predict_gate29.py), `_final_lsremote_1.tabs-normalised.bak` (an identical copy of final_lsremote_1.out), `__pycache__/`.'); A('')
A('## 9. NOT done / NOT measured by the drafter')
A('- No launch, mail, tap, merge, commit, push, comment, routing write, container or port bind. No inbox read. No write in any project folder or in /Volumes/DevMASTER/WEDNESDAY. No file deleted.')
A('- **UNMEASURED (#1290):** every runtime behaviour — the probe under four NODE_ENVs, the merge-base leak control, non-Error throws, Arm R3 (the seat\'s armR3.out is a claim), the brief\'s DELETE tamper arm, the secret-absent-from-logs probe, the two unconverted sites still leaking at runtime; the seat\'s 6/5/11 red and 11/11 green; originate 951 → 962; tsc with `exclude: []`; lint 22 warnings; the ks860 / ks879 guards over the new cell; the OpenAPI 500 schema. Every #1290 line above is READ (git show / diff / hash-object).')
A('- **UNMEASURED (#1291):** the red at develop and green at head; `npm run lint`, `format:check`, `test:unit` (1114 → 1117) at any tree; the formatter delta being formatting-only (only its numstat +9/-6 is READ); the spaced-path unit run; the real CLI from a spaced copy.')
A('- **UNMEASURED (all):** prettier; every suite on END_TREE; the usage gate and launch steps 4-6; whether the 2026-09-30 audit fuse covers `systemTest/` paths.')
open(D + '/README.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/README.md', len(out), 'lines')
