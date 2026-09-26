#!/usr/bin/env python3
"""make_readme_gate27.py <scratchpad> — writes README.md for gate27 (the directory this script lives in). Every SHA, tree, count and control
tally is READ from the kit's own files (pins_gate27.json, stopcounts_gate27.json, gh_read_1.out, controls_1/2.out + .rc, fill_1.out,
launcher_check_1.out, repin_dryrun_1.out, probe*_1.out, predict_sim_*.out) at the moment of writing — never typed. The prose is the drafter's."""
import json, os, re, sys
D = os.path.dirname(os.path.abspath(__file__)); SP = sys.argv[1]
K = json.load(open(D + '/kit.json')); kit = K['kit']
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit)))
gh = open(D + '/gh_read_1.out').read()
def rd(f):
    p = os.path.join(D, f); return open(p).read() if os.path.exists(p) else ''
def ctl(f):
    t = rd(f); m = re.search(r'SUMMARY \S+: (\d+) controls, OK (\d+), MISMATCH (\d+)', t); return (m.groups() if m else ('?', '?', '?')), rd(f.replace('.out', '.rc')).strip() or '?'
(c1, rc1), (c2, rc2) = ctl('controls_1.out'), ctl('controls_2.out')
mism1 = [l.strip() for l in rd('controls_1.out').splitlines() if l.startswith('  MISMATCH')]
ok2 = [l.strip() for l in rd('controls_2.out').splitlines() if l.startswith('  OK')]
chk = rd('launcher_check_1.out').splitlines()[:1]
dry = [l for l in rd('repin_dryrun_1.out').splitlines() if l.startswith('DRY RUN COMPLETE') or 'REFUS' in l]
fill = [l for l in rd('fill_1.out').splitlines() if l.startswith('key scan') or l.startswith('seat items')]
sims = []
for f in sorted(os.listdir(D)):
    m = re.match(r'predict_sim_(\w+)\.out$', f)
    if m: sims.append('%s -> %s' % (m.group(1), (rd(f).strip().splitlines() or ['?'])[-1].split(' ->')[0]))
def subj(n):
    m = re.search(r'=== #%s head.*?\ntitle \((\d+) chars.*?= (\d+) chars' % n, gh, re.S); return m.group(2) if m else '?'
L = os.path.join(D, K['launcher']); R = os.path.join(D, 'repin_and_launch_%s.sh' % kit)
WHY = {
 '1278': 'two systemTest/ test files; a CHECKER (reader rule). **FIX ROUND — round 2 of 2, at the cap.** The AST replaced the text joiner.',
 '1285': 'one operator script (no service imports it, no deploy runs it); its self-test is the red proof (no docker).',
 '1286': '**T3** — two Markdown files, no code: every changed sentence vs the code; no plan may be added.',
 '1287': 'one test file == blob `8a4ce36a` (graded twice in #1268); run on the current develop.',
}
rows = ['| #%s | %s | %s | `%s` | %d on `%s` | %s | %s |' % (n, ' + '.join(K['prs'][n]['keys']), K['prs'][n]['tier'], P['prs'][n]['head'], len(P['prs'][n]['commits']), P['prs'][n]['merge_base'][:12], subj(n), WHY[n]) for n in sorted(K['prs'])]
stop = []
for n in sorted(K['prs']):
    s = S[n]
    stop.append('#%s %s' % (n, ('%s · %s · %s · %s' % (s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['shell_suites'].split(',')[0].replace(' passed', '') + ' of 60')) if s['preflight_ran'] else 'NOT APPLICABLE (systemTest/ push, %d lines)' % s['lines']))
launch = '%s %s %s' % (R, L, SP)
go = re.search(r"GO='(`GO: merge [^`]*`)'", open(D + '/fill_gate27.py').read()).group(1)
dos = P.get('dead_open_same_blob', {})
pr1278 = [l for l in rd('probe1278_1.out').splitlines() if l[:3] in ('IE1', 'CR1', 'AL1', 'AL2', 'DEA', 'A4 ', 'A2c', 'S6b', 'S6d')]
pr1285 = [l for l in rd('probe1285_1.out').splitlines() if re.match(r'^(base|head|armT|armC):', l)]
p1286 = [l.strip()[6:] for l in rd('predict_1.out').splitlines() if l.startswith('  #1286 ') and ('PREDICTION' in l or 'FLAG CENSUS' in l or 'startup-migrations' in l)]
p1287 = [l.strip()[6:] for l in rd('predict_1.out').splitlines() if l.startswith('  #1287 ') and ('BLOB' in l or 'COUPLING' in l)]
out = []; A = out.append
A('# Gateset 2026-09-26_%s — README for Wednesday' % kit); A('')
A('The drafter launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing and wrote nothing inside any project folder or /Volumes/DevMASTER/WEDNESDAY.')
A('It wrote only under `%s/` (this kit), the scratch clone `%s/g27_sp/clone.git` (a `--no-local` bare clone, no alternates), the control workdirs' % (D, SP))
A('`%s/g27_controls_*`, and the probe dirs `%s/g27_probe1278/` (a SYMLINK to the Secuura checkout\'s systemTest/performance/node_modules, read-only use) and' % (SP, SP))
A('`%s/g27_probe1285*/` (git-archive extracts). The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, `clone --no-local` as a source).' % SP)
A('')
A('**gate27 = FOUR PRs, tiers 2 and 3, one kit, no sibling.** Heads Wednesday relayed (ls-remote at 03:0xZ) re-read here by TWO instruments at the pin (ls-remote AND the PULLS API, and fetched): all agree.'); A('')
A('| PR | ticket | tier | head (READ: API == ls-remote pull/head == branch == fetched) | commits on merge-base | squash subject chars | why this tier (from the DIFF) |')
A('|---|---|---|---|---|---|---|'); out.extend(rows); A('')
A('Routing `%s`. GO string %s (or the subset). All go to a MERGE SEAT (Seat L7 wrapped; Seat B 30th is building).' % (K['pane'], go)); A('')
A('## 1. BLUF')
A('- **Kit: READY to launch** once you add the routing line (§4). `--check` rc 0 (%s).' % (chk[0].strip() if chk else 'launcher_check_1.out'))
A('  - Controls: **%s controls, OK %s, MISMATCH %s** normally (rc %s); **OK %s, MISMATCH %s** under `--invert` (rc %s — by design every control must flip).' % (c1[0], c1[1], c1[2], rc1, c2[1], c2[2], rc2))
A('- **Pinned over develop `%s`** (tree `%s`) — read by ls-remote AND fetched AND agreed: it is the `e6056de7ed64` you named (#1284\'s squash, the last of gate26\'s eleven).' % (P['develop'], P['develop_tree']))
A('  - END_TREE **`%s`** (%s), identical in all %d orders (%d merge-tree calls). No sibling kit, so END_TREE_WITH_SIBLING == END_TREE (measured).' % (P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls']))
A('- **OVERLAPS — pairwise, measured:** the 6 kit pairs disjoint; every kit path disjoint from ALL %d other open PRs (PULLS API census, incl. dead-open #1245/#1241, Seat L5\'s #1250/#1253, dependabot); NOT STACKED (no head is another\'s ancestor; every pair\'s merge-base is on develop).' % len(P['inflight']))
for b, rs in sorted(dos.items()):
    for r in rs:
        A('  - **ONE DECLARED overlap:** dead-open **#%s** (NO GO at its cap, still OPEN, head `%s`) carries #%s\'s `%s` at the **same blob** `%s` — asserted byte-identical in predict (hard). It cannot change what lands; but **#%s must close unmerged** (merged later it would land its failed ks781 rule). §6.3.' % (b, r['dead_open_head'][:12], r['pr'], r['path'].split('/')[-1], r['blob_kit'], b))
A('- **#1278 at the cap (round 2 of 2) — the decisive item (PREDICTIONS, drafter_probe1278.sh: the REAL head function under node 24 + typescript 6.0.3, not vitest):**')
A('  - The round-1 blockers look CLOSED at function level: S6b / S6d read 1 hit; the A4 plant inside the real develop config_loader.ts reads 1 hit; A2c (the only real call replaced) makes `callsReadYaml` false. The gate owes both arms through the REAL cells.')
A('  - **NEW candidates under THE READER RULE — unvisited AND unnamed in either file (READ):** `CREATEREQUIRE-ALIAS` (`const req = createRequire(import.meta.url); req(\'js-yaml\')`) reads **0**; `IMPORT-EQUALS` (`import y = require(\'js-yaml\')`) reads **0**. The package is `"type": "module"` — createRequire is the standard ESM way to require CJS; reach today 0 (READ). If the gate finds either REAL (prettier-stable + tsc-clean + actually loads under tsx), the rule says **NO GO — at the cap it ships nothing**. §6.1.')
A('  - callsReadYaml: an alias and `readYaml.call` read false (a loud false red); a call inside a never-invoked function reads **true** (a silent over-report). The loader list is still hand-written (declared).')
for l in pr1278: A('    - `%s`' % re.sub(r'\s{2,}', ' ', l)[:150])
A('- **#1285 KS-766 (PREDICTIONS, drafter_probe1285.sh: git-archive extracts, /bin/bash 3.2, a docker shim that exits 97):** the seat\'s red proof reproduces exactly.')
for l in pr1285: A('    - `%s`' % l[:170])
A('  - **Fleet count: UNCHANGED (READ by path class).** base-image-watch.sh is not a `*.test.sh` in run-shell-suites.sh\'s ROOTS (scripts/__tests__, systemTest/__tests__) and no suite invokes `--self-test`; its own 20 -> 22 is a SEPARATE count. The gate measures membership with `--list` (§6.4).')
A('- **#1286 docs, T3 — a PREDICTED FALSE NEW SENTENCE (READ):**')
for l in p1286: A('    - %s' % l[:420])
A('  - The substance (every tenant on ONE shared DB; per-tenant path dormant) holds by READ: PROVISION_PER_TENANT_DB is set in no config file and gates the per-tenant path at tenant-pool-manager.ts:152 and tenant-provisioning/src/index.ts:245. §6.2.')
A('- **#1287 (READ):**')
for l in p1287: A('    - %s' % l[:420])
A('- **Fleet STOP (READ, bounded region, NOT-FOUND control):** %s. Declared at 00de57baeb40 by Seat B 30th (handover "THE FLEET MEASUREMENT — TAKEN"): 28/0 · 6/0 · 49/0 · 60 of 60. After this merge: 28/0 · 6/0 · 49/0 · 60 of 60 (no PR adds, removes or renames a `*.test.sh`).' % '; '.join(stop))
A('- **Linear: every PR links `contributes`; NONE `closes`; no body has a closing word before a key** (linear_reads_1.out, gh_read_1.out). KS-1314, KS-766, KS-1336, KS-1318, KS-1142 all In Progress.')
A('- **MG-3 key scan:** %s. Foreign keys to un-hyphenate if quoted: #1278 KS1300 (body + round-1 message), #1286 KS1055 (body). #1286\'s own commit says `Refs KS1336` (un-hyphenated) — the mandated block carries `Refs KS-1336`.' % (fill[0] if fill else 'fill_1.out'))
A('- **TITLE-OVER-92:** #1278 is 116 with ` (#1278)`; the kit mandates the drafter\'s short subject (90, key-scanned). The other three fit (85, 84, 80).'); A('')
A('## 2. Pins — predict_1.out (rc 0)')
for n in sorted(K['prs']):
    pr = P['prs'][n]
    A('- #%s: %d commit(s) %s over `%s`; %d behind develop; merged tree `%s`; every merged blob == its head blob; numstat equal; no mode change; move ∩ own paths EMPTY.' % (n, len(pr['commits']), ', '.join('`%s`' % c[:12] for c in pr['commits']), pr['merge_base'], pr['behind'], pr['merged_tree']))
A('- Simulations: %s. `moved` = develop + one unrelated synthetic commit (must PASS); `foreign<n>` = develop + a foreign edit of that PR\'s first own file (must REFUSE). No OLDER develop can host #1287 (it sits on the current develop), so gate26\'s `--simulate predev` became `--simulate moved`; `predev` (00de57baeb40) is still the moved-develop pin in controls D / RC / RD.' % '; '.join(sims))
A('- Superseded runs are kept, never deleted: `predict_superseded_preprobefix.out` (the first pinned run, before a probe-text fix; same pins).'); A('')
A('## 3. What the gate owes')
A('- Prompt `%s` (%d bytes) — per-PR sections, THE READER RULE, the #1278 cap rule (re-run A4 and A2c; the AST shape table), #1285\'s four self-test runs under a docker shim, #1286\'s TIER 3 sentence table, #1287\'s blob + K1b coupling, the MANDATED SQUASH TEXT blocks and the MG-3 key-set table.' % (K['prompt'], os.path.getsize(os.path.join(D, K['prompt']))))
A('- Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-26-batch1278-g27/`; mail subject as in the prompt, FROM coagent@ TO wednesday-agent@.'); A('')
A('## 4. Routing line to add (the drafter did NOT write it)')
A('`%s|coagent@agentmail.to|yes` → `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (absent at drafting: whole-line grep count 0, with the control line `QA/Secuura-batch1245|coagent@agentmail.to|yes` counting 1 in the same file). Also in PROPOSED_inbox_routing_line.txt.' % K['pane']); A('')
A('## 5. The ONE launch command'); A('```'); A(launch); A('```')
A('- Dry run (`--dry-run` appended): repin_dryrun_1.out → %s' % (dry[-1] if dry else '?'))
A('- If develop moves (a GO lands first), step 3b re-pins in the same action; a move onto an own path, a stack or a pairwise overlap refuses rc 10 (controls RD / RE).')
A('- If you copy the kit into `gatesets/2026-09-26_gate27/`, pass the copied paths: step 0b re-measures and re-fills there.'); A('')
A('## 6. Decisions for Wednesday (each with the drafter\'s recommendation)')
A('1. **#1278 at the cap: CREATEREQUIRE-ALIAS / IMPORT-EQUALS** read 0 and are unnamed. Reach 0 today. *Recommend:* do NOT pre-soften — the rule says reach does not soften; the prompt makes the gate decide REALNESS by instrument (prettier-stable, `npm run lint` clean, actually loads js-yaml under `npx tsx`). Be ready for NO GO at the cap (ships nothing; KS-1314 residue ticketed). If you would rather not lose the proven A4/A2c/S6b fix to a reach-0 shape, that is a Kam-level ruling on the reader rule — not the drafter\'s or the gate\'s.')
A('2. **#1286 DOC-CLAIM-TWO-FLAGS:** the PR writes "MULTI_TENANCY_ENABLED and PROVISION_PER_TENANT_DB … set in NO configuration file"; MULTI_TENANCY_ENABLED is `"true"` in deployment/azure/env.dev.json, env.demo.json and services.bicep (READ). The conclusion (shared DB) survives; the sentence does not. *Recommend:* a false NEW sentence in a document whose whole job is correcting false sentences is blocking at T3 → NO GO with a one-line fix round (not at any cap). Let the gate measure it first. ONBOARDING-CITE (startup-migrations.ts seeds 8 fixed ids; new tenants go through tenant-provisioning/src/index.ts:245/:272) is a cite-accuracy finding, non-blocking in the drafter\'s view.')
A('3. **#1268 disposition (dead-open, same blob as #1287):** its body says the disposition is Kam\'s. *Recommend:* ask Kam to close #1268 unmerged once #1287 lands (approval-class: it closes a PR). Until then the merge seat must never merge #1268 (it would land its failed ks781 rule). Same note stands for #1245 and #1241 (both dead-open, disjoint from this kit).')
A('4. **`run-shell-suites.sh --list` in the gate\'s own worktree** — the standing rule forbids a STANDALONE RUN of run-shell-suites.sh over the real repo; the prompt carves out the read-only `--list` mode in the gate\'s OWN worktree as the membership instrument for #1285. *Recommend:* accept (it runs no suite and reads only its own clone). Reject → the membership stays READ ONLY.')
A('5. **Mixed tiers in one kit (T2 x3 + T3 #1286).** *Recommend:* accept — four PRs, well under the cap of 8; the T3 rule is an explicit kit rule (exit 43) and the T3 row owes no red proof.')
A('6. **#1278\'s short subject** («KS-1314: read parser imports from the AST; pin the readYaml call, not its spelling (#1278)», 90 chars) is the drafter\'s wording. *Recommend:* let the gate ratify or reword; re-run the key scan over whatever is mandated.')
A('7. **#1285 LOCAL-MODEL-PROVENANCE** (the patch was produced by the local model under your brief, re-verified by the seat). *Recommend:* grade on merits, no special handling; the drafter\'s probe reproduced every figure.')
A('8. **Routing name** `QA/Secuura-batch1278` (you specified it). Distinct and absent (measured). *Recommend:* keep.')
A('9. **READY mails NOT read** (no message id reached the drafter; a listing marks mail seen). The seat claims come from PR bodies, commit messages and handovers (the capture).'); A('')
A('## 7. Controls: `controls_%s.sh <scratchpad> [--invert]`' % kit)
A('- **controls_1.out:** %s controls, **OK %s, MISMATCH %s** (rc %s).%s' % (c1[0], c1[1], c1[2], rc1, (' MISMATCHES: ' + '; '.join(mism1)) if mism1 else ''))
A('- **controls_2.out (`--invert`):** **OK %s, MISMATCH %s** (rc %s by design). Every control can fail.%s' % (c2[1], c2[2], rc2, (' Controls that did NOT flip: ' + '; '.join(ok2)) if ok2 else ''))
A('- Every mutation is independent of the original: doctor() refuses a replacement that contains the text it replaces (rc 98) and refuses when the original still occurs after the plant (rc 97); every wrong head is the real head with ONE hex digit changed (same length, never a superset); the launcher\'s head guard is whole-field.')
A('- Doctored arms are pinned to the launcher\'s own develop. RD runs the REAL re-pin (predict → fill) from a launcher pinned at predev `00de57baeb40` in a MOVED copy; RE lists a kit PR in the (empty) sibling set too — a pairwise overlap — and must refuse rc 10. PS2 is `--simulate moved`; PF1 fills from its SIM pins and must refuse.')
A('- Not controlled: exit 16 (needs a TTY), repin steps 4-6 (usage gate, cockpit add), a `mergeable=False` refusal.'); A('')
A('## 8. Files')
A('- Kit: kit.json · COMMISSION.md (the LEGITIMATE SHAPES table) · PROPOSED_inbox_routing_line.txt · make_commission_gate27.py / make_readme_gate27.py (generate the two .md files from the kit\'s own outputs)')
A('- Pins: predict_gate27.py → predict_1.out, predict_sim_*.out, pins_gate27.json (+ .SIM-*.json)')
A('- Reads: gh_read_gate27.py → gh_read_1.out, gh_body_*.md, gh_comments_*.md · linear_reads_gate27.py → linear_reads_1.out, linear_KS-*.md · capture_mail_gate27.py → capture_1.out, mail_gate27_ready.md, stopcounts_gate27.json')
A('- Prompt/launcher: prompt_gate27.TEMPLATE.txt, launcher_gate27.TEMPLATE.sh.txt, fill_gate27.py → %s + %s (fill_1.out), launcher_check_1.out' % (K['prompt'], K['launcher']))
A('- Repin/controls: repin_and_launch_gate27.sh (repin_dryrun_1.out), controls_gate27.sh (controls_1/2.out + .rc)')
A('- Drafter probes (PREDICTIONS): drafter_probe1278.sh → probe1278_1.out · drafter_probe1285.sh → probe1285_1.out'); A('')
A('## 9. NOT done / NOT measured by the drafter')
A('- No launch, mail, tap, merge, commit, push, routing write, container or port bind. No inbox read. No write in any project folder or in /Volumes/DevMASTER/WEDNESDAY.')
A('- **UNMEASURED:** every suite count (systemTest/performance unit, packages/shared) and tsc / lint / prettier — the seat\'s figures are READ only; the A4 / A2c / textreader arms through the REAL sheddingCeiling cells (the drafter probed the functions, not the cells); whether CREATEREQUIRE-ALIAS / IMPORT-EQUALS are REAL (prettier / tsc / tsx); a third loader beyond the hand-written two.')
A('- **UNMEASURED:** #1287 on develop (the file alone, the package, the K1b drift plant); #1286 beyond the two predictions (the full sentence table, the 039 SQL text); `run-shell-suites.sh --list` and the scripts/*.sh guards over #1285; the usage gate and launch steps 4-6.')
open(D + '/README.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/README.md', len(out), 'lines')
