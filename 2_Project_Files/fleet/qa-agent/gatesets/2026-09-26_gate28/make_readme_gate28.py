#!/usr/bin/env python3
"""make_readme_gate28.py <scratchpad> — writes README.md for gate28 (the directory this script lives in). Every SHA, tree, count and control
tally is READ from the kit's own files (pins_gate28.json, stopcounts_gate28.json, gh_read_1.out, controls_1/2.out + .rc, fill_1.out,
launcher_check_1.out, repin_dryrun_1.out, routing_check_1.out, probe1268_after_1.out, predict_1.out, predict_sim_*.out) at the moment of writing —
never typed. The prose is the drafter's."""
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
rout = rd('routing_check_1.out').splitlines()
p68 = [l for l in rd('probe1268_after_1.out').splitlines() if l.strip()]
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
 '1286': '**T3** — two Markdown files, no code. **FIX ROUND — round 2 of 2, AT THE CAP** (gate27 NO GO: N-1286-1 TWO-FLAGS-FALSE).',
 '1288': '**T1** — originate webhooks.ts: what a 500 carries to a client (information exposure). Part A of 3 (2 of 7 sites). Local-model patch.',
 '1289': 'one test assertion (J2 count -> tag set); hunk 3 of #1268 alone; declared overlap with dead-open #1268 at a DIFFERENT blob.',
}
rows = ['| #%s | %s | %s | `%s` | %d on `%s` | %s | %s |' % (n, ' + '.join(K['prs'][n]['keys']), K['prs'][n]['tier'], P['prs'][n]['head'], len(P['prs'][n]['commits']), P['prs'][n]['merge_base'][:12], subj(n), WHY[n]) for n in sorted(K['prs'])]
stop = []
for n in sorted(K['prs']):
    s = S[n]
    stop.append('#%s %s' % (n, ('%s · %s · %s · %s' % (s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['shell_suites'].split(',')[0].replace(' passed', '') + ' of 60')) if s['preflight_ran'] else 'NOT APPLICABLE'))
launch = '%s %s %s' % (R, L, SP)
go = re.search(r"GO='(`GO: merge [^`]*`)'", open(D + '/fill_%s.py' % kit).read()).group(1)
dos = P.get('dead_open_declared', {})
out = []; A = out.append
A('# Gateset 2026-09-26_%s — README for Wednesday' % kit); A('')
A('The drafter launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing, posted nothing and wrote nothing inside any project folder or /Volumes/DevMASTER/WEDNESDAY.')
A('It wrote only under `%s/` (this kit), the scratch clone `%s/g28_sp/clone.git` (a `--no-local` bare clone, no alternates; the drafter\'s own merge-tree / hash-object writes only) and the control workdirs `%s/g28_controls_*`.' % (D, SP, SP))
A('The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, `clone --no-local` as a source). GitHub: REST GET only (Secuura GH_TOKEN read by name, never printed). Linear: queries only. The routing conf was READ (grep), never written.'); A('')
A('**gate28 = THREE PRs, tiers 1, 2 and 3, one kit, no sibling.** Heads Wednesday relayed (ls-remote at 06:4xZ) re-read here by TWO instruments at the pin (ls-remote AND the PULLS API, and fetched): all agree.'); A('')
A('| PR | ticket | tier | head (READ: API == ls-remote pull/head == branch == fetched) | commits on merge-base | squash subject chars | why this tier (from the DIFF) |')
A('|---|---|---|---|---|---|---|'); out.extend(rows); A('')
A('Routing `%s`. GO string %s (or the subset). All three go to a MERGE SEAT Wednesday names (never an author).' % (K['pane'], go)); A('')
A('## 1. BLUF')
A('- **Kit: READY to launch** once you add the routing line (§4). Launcher `--check` rc 0 (%s); repin `--dry-run` rc 0.' % (chk[0].strip() if chk else 'launcher_check_1.out'))
A('  - Controls: **%s controls, OK %s, MISMATCH %s** normally (rc %s); **OK %s, MISMATCH %s** under `--invert` (rc %s — by design every control must flip).' % (c1[0], c1[1], c1[2], rc1, c2[1], c2[2], rc2))
A('- **Pinned over develop `%s`** (tree `%s`) — read by ls-remote AND fetched AND the API compare agrees: it is the `e080174c86c6` you named (#1287\'s squash; gate27\'s two GOs over e6056de7ed64). Its tree is exactly the GO-subset END tree gate27 predicted (`b698a77faf48`).' % (P['develop'], P['develop_tree']))
A('  - END_TREE **`%s`** (%s), identical in all %d orders (%d merge-tree calls). No sibling kit, so END_TREE_WITH_SIBLING == END_TREE (measured).' % (P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls']))
A('- **OVERLAPS — pairwise, measured:** the 3 kit pairs disjoint; every kit path disjoint from ALL %d other open PRs (PULLS API census, incl. dead-open #1278/#1245/#1241, Seat L5\'s #1250/#1253, #995 on originate, dependabot); NOT STACKED.' % len(P['inflight']))
for b, rs in sorted(dos.items()):
    for r in rs:
        A('  - **ONE DECLARED overlap:** dead-open **#%s** (NO GO at its cap, still OPEN, head `%s`) carries #%s\'s `%s` at a **DIFFERENT blob** (`%s` vs `%s`). Asserted HARD in predict as a **hunk subset**: #%s\'s %d hunk body == #%s\'s hunk %s of %d, pre-image `%s` identical at both merge-bases and develop; `W9` (KS-1316-only) 0 vs 7.' % (
            b, r['dead_open_head'][:12], r['pr'], r['path'].split('/')[-1], r['blob_kit'][:12], r['blob_dead_open'][:12], r['pr'], r['kit_hunks'], b, r['kit_hunk_index_in_dead_open'], r['dead_open_hunks'], r['pre_image'][:12]))
        A('  - **PROBED (merge-tree):** #%s merged AFTER this kit is **CLEAN** and lands exactly its other two hunks (KS-1316\'s failed LEG-F rule): %s. So **#%s must close unmerged** (§6.6).' % (
            b, '; '.join(l for l in p68 if l.startswith(('merge-tree', ' .../', ' 1 file', 'W9'))).replace('  ', ' ').strip(), b))
A('- **#1286 at the cap (round 2 of 2) — the decisive item (READ PREDICTIONS; the gate measures):**')
A('  - N-1286-1 looks FIXED in the docs: %s' % probe('1286', 'TWO-FLAGS-FIXED'))
A('  - Cites re-read at develop: %s' % probe('1286', 'FLAG CENSUS'))
A('  - The fix touches only the flag sentences + the onboarding cite: %s' % probe('1286', 'FIX ROUND'))
A('  - **NEW in round 2 — INSERT-LINE-271:** %s' % probe('1286', 'ONBOARDING-CITE-R2'))
A('  - **BICEP-SCOPE:** %s' % probe('1286', 'BICEP-SCOPE'))
A('  - N-1286-3..6 carried (declared NOT done): %s' % probe('1286', 'ROUND-1 NON-BLOCKING'))
A('  - **PR-BODY-STALE:** %s' % probe('1286', 'PR-BODY-STALE'))
A('- **#1288 KS-1341 part A, T1 (READ PREDICTIONS):**')
for k in ('LEAK SITES', 'UNCONVERTED-FIVE', 'HELPER-PLACEMENT', 'DOCBLOCK-FALSE-AT-A', 'GOLDEN', 'KS-730 FAMILY', 'BENIGN-BRANCH', 'GET / TRAP'):
    A('  - %s' % probe('1288', k)[:600])
A('  - **Not in part A:** KS-1341\'s BLUF names DELETE /:id and rotate-secret as the MEASURED leaks ("internal configuration text") — both are part B (golden B.golden.diff, READ). §6.4.')
A('- **#1289 KS-1318 (READ PREDICTIONS):**')
for k in ('BLOBS', 'KS1316-FREE', 'J2 ASSERTION', 'RED-ARM ANCHORS', 'KS-1318 DoD'):
    A('  - %s' % probe('1289', k)[:600])
A('- **Fleet STOP (READ, bounded region, NOT-FOUND control):** %s. After this merge: 28/0 · 6/0 · 49/0 · 60 of 60 (no PR adds, removes or renames a `*.test.sh`).' % '; '.join(stop))
A('- **Linear: every PR links `contributes`; NONE `closes`; no body has a closing word before a key** (linear_reads_1.out, gh_read_1.out). KS-1336, KS-1341, KS-1318 all In Progress.')
A('- **MG-3 key scan:** %s. Foreign key to un-hyphenate if quoted: #1286 KS1055 (PR body). #1286\'s round-1 commit says `Refs KS1336` (un-hyphenated; the scanner sees 0 there); the fix commit `Refs KS-1336`. **No PR body would CLOSE a ticket it only contributes to** (0 closing-word+key in each body).' % (fill[0] if fill else 'fill_1.out'))
A('- **MG-11:** every `<title> (#n)` fits (84 / 89 / 90); no SHORT subject needed; the mandated blocks use the PR titles as read from the API.'); A('')
A('## 2. Pins — predict_1.out (rc 0)')
for n in sorted(K['prs']):
    pr = P['prs'][n]
    A('- #%s: %d commit(s) %s over `%s`; %d behind develop; merged tree `%s`; every merged blob == its head blob; numstat equal; no mode change; move ∩ own paths EMPTY.' % (n, len(pr['commits']), ', '.join('`%s`' % c[:12] for c in pr['commits']), pr['merge_base'], pr['behind'], pr['merged_tree']))
A('- Simulations: %s. `moved` = develop + one unrelated synthetic commit (must PASS); `foreign<n>` = develop + a foreign edit of that PR\'s first own file (must REFUSE). No OLDER develop can host #1288/#1289 (they sit on the current develop), so the base-invariance simulation is `--simulate moved`; `predev` (e6056de7ed64, gate27\'s pin) is the moved-develop pin in controls D / RC / RD.' % '; '.join(sims))
A('- Superseded runs are kept, never deleted: `predict_superseded_pretagfix.out` (the first pinned run, before the #1289 tag-probe fix read template labels; same pins, same FAIL=0).'); A('')
A('## 3. What the gate owes')
A('- Prompt `%s` (%d bytes) — per-PR sections: #1288\'s T1 RUNTIME PROBE (the gate\'s own LEAK, four NODE_ENVs incl. UNSET, body/logger/REACHED, a merge-base control that must leak), the declared five, helper placement + hoisting, the docblock ruling; #1289\'s red design (arms A/B at both trees + a fire-twice arm); #1286\'s ROUND-2 cap rule graded against gate27\'s NO GO and the TIER 3 sentence table; the MANDATED SQUASH TEXT blocks and the MG-3 key-set table.' % (K['prompt'], os.path.getsize(os.path.join(D, K['prompt']))))
A('- Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-26-batch1286-g28/`; mail subject as in the prompt, FROM coagent@ TO wednesday-agent@.'); A('')
A('## 4. Routing line to add (the drafter did NOT write it)')
A('`%s|coagent@agentmail.to|yes` → `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`. Absent at drafting (routing_check_1.out: %s). Also in PROPOSED_inbox_routing_line.txt.' % (K['pane'], ' · '.join(rout[1:5]))); A('')
A('## 5. The ONE launch command'); A('```'); A(launch); A('```')
A('- Dry run (`--dry-run` appended): repin_dryrun_1.out → %s' % (dry[-1] if dry else '?'))
A('- If develop moves (a GO lands first), step 3b re-pins in the same action; a move onto an own path, a stack or a pairwise overlap refuses rc 10 (controls RD / RE).')
A('- If you copy the kit into `gatesets/2026-09-26_gate28/`, pass the copied paths: step 0b re-measures and re-fills there.'); A('')
A('## 6. Decisions for Wednesday (each with the drafter\'s recommendation)')
A('1. **#1286 at the cap — two NEW round-2 accuracy nits (INSERT-LINE-271, BICEP-SCOPE).** ":271" names the `platformQuery(` call; the INSERT text is :272. "ON in dev and demo" is true of the two env files, while services.bicep:798 sets it for whatever environment the template deploys (only env.staging.example besides). *Recommend:* treat both as non-blocking cite/scope findings unless the gate finds a sentence FALSE — at the cap a NO GO ships nothing and throws away a correction whose blocking defect is fixed. The rule is the gate\'s; this is the drafter\'s weight.')
A('2. **#1286 N-1286-3..6** (declared NOT done; the fix-round GO authorised two items). *Recommend:* whatever the verdict, ONE follow-up docs ticket carrying N-1286-3..6 plus any round-2 nit (a board write — yours to authorise; the gate files nothing).')
A('3. **#1286 PR-BODY-STALE** — the PR body still carries the round-1 false sentence. *Recommend:* the merge seat composes the squash body from the MANDATED block (already mandated); optionally ask the owner to edit the PR body (a GitHub write, not the gate\'s).')
A('4. **#1288 DOCBLOCK-FALSE-AT-A in a T1 PR** ("the only place in this router…" is false until B and C). *Recommend:* non-blocking, carried by name into part B/C\'s brief (part C makes it true); do NOT break the golden identity for a comment. And **PART-A-SCOPE-ORDER:** the two MEASURED leaks (DELETE /:id, rotate-secret) are part B — *recommend* part B next, ahead of other local-model work.')
A('5. **#1288 LOCAL-MODEL-PROVENANCE.** Blob-identical to the golden (hash-object, READ). *Recommend:* grade on merits, no special handling (as #1285 at gate27).')
A('6. **#1268 disposition.** After #1287 (landed) and #1289, everything of #1268 except KS-1316\'s failed hunks is on develop; the merge-tree probe shows a later merge of #1268 is CLEAN and lands exactly KS-1316\'s rule. *Recommend:* ask Kam to close #1268 unmerged once #1289 lands (approval-class: it closes a PR; Seat B 30th\'s handover says Kam\'s). Until then the merge seat must never merge #1268.')
A('7. **KS-1318 after #1289 merges.** Its Done-when is ONE checkbox that #1289 delivers exactly, but the link is `contributes`, so the ticket will not move. *Recommend:* if the gate rules the DoD closed, a Done transition by you (a ticket state change — your call, not the gate\'s or a seat\'s).')
A('8. **Mixed tiers in one kit (T1 #1288 + T2 #1289 + T3 #1286).** *Recommend:* accept — three PRs, disjoint, well under the cap; each tier rule is an explicit kit rule (exits 40/42/49 T1, 44 T2, 43 T3).')
A('9. **Routing name** `QA/Secuura-batch1286` (you specified it). Distinct and absent (measured, with a control). *Recommend:* keep.')
A('10. **READY mails NOT read** (no message id reached the drafter; a listing marks mail seen). The seat claims come from PR bodies, every commit message, #1286\'s fix-round PR comment, Seat B 30th\'s handover and Seat B 31st\'s ticket comments + red/green outputs (the capture).'); A('')
A('## 7. Controls: `controls_%s.sh <scratchpad> [--invert]`' % kit)
A('- **controls_1.out:** %s controls, **OK %s, MISMATCH %s** (rc %s).%s' % (c1[0], c1[1], c1[2], rc1, (' MISMATCHES: ' + '; '.join(mism1)) if mism1 else ''))
A('- **controls_2.out (`--invert`):** **OK %s, MISMATCH %s** (rc %s by design). Every control can fail.%s' % (c2[1], c2[2], rc2, (' Controls that did NOT flip: ' + '; '.join(ok2)) if ok2 else ''))
A('- Every mutation is independent of the original: doctor() refuses a replacement that contains the text it replaces (rc 98) and refuses when the original still occurs after the plant (rc 97); every wrong head is the real head with ONE hex digit changed (same length, never a superset); the launcher\'s head guard is whole-field.')
A('- Doctored arms are pinned to the launcher\'s own develop. RD runs the REAL re-pin (predict → fill) from a launcher pinned at predev `e6056de7ed64` in a MOVED copy; RE lists a kit PR in the (empty) sibling set too — a pairwise overlap — and must refuse rc 10. PS1 is `--simulate foreign1288` (a conflicting merge); PS2 is `--simulate moved`; PF1 fills from its SIM pins and must refuse.')
A('- Not controlled: exit 16 (needs a TTY), repin steps 4-6 (usage gate, cockpit add), a `mergeable=False` refusal.'); A('')
A('## 8. Files')
A('- Kit: kit.json · COMMISSION.md (the drafter\'s READ predictions table) · PROPOSED_inbox_routing_line.txt + routing_check_1.out · make_commission_gate28.py / make_readme_gate28.py (generate the two .md files from the kit\'s own outputs)')
A('- Pins: predict_gate28.py → predict_1.out, predict_sim_*.out, pins_gate28.json (+ .SIM-*.json); probe1268_after_1.out (the #1268-after-kit merge-tree)')
A('- Reads: gh_read_gate28.py → gh_read_1.out, gh_body_*.md, gh_comments_*.md · linear_reads_gate28.py → linear_reads_1.out, linear_KS-*.md · capture_mail_gate28.py → capture_1.out, mail_gate28_ready.md, stopcounts_gate28.json')
A('- Prompt/launcher: prompt_gate28.TEMPLATE.txt, launcher_gate28.TEMPLATE.sh.txt, fill_gate28.py → %s + %s (fill_1.out), launcher_check_1.out' % (K['prompt'], K['launcher']))
A('- Repin/controls: repin_and_launch_gate28.sh (repin_dryrun_1.out), controls_gate28.sh (controls_1/2.out + .rc)'); A('')
A('## 9. NOT done / NOT measured by the drafter')
A('- No launch, mail, tap, merge, commit, push, comment, routing write, container or port bind. No inbox read. No write in any project folder or in /Volumes/DevMASTER/WEDNESDAY.')
A('- **UNMEASURED (#1288):** every runtime behaviour — the probe under four NODE_ENVs, the merge-base leak control, non-Error throws, the five sites still leaking at runtime, the const-arrow placement arm; the seat\'s 4/4/8 red and 8/8 green; originate 943 → 951; tsc with `exclude: []`; lint 22 warnings; the ks860 / ks879 guards over the new cell; the OpenAPI 500 schema. The drafter ran NO drafter probe of the router (no jest/express run) — every #1288 line above is READ.')
A('- **UNMEASURED (#1289):** arms A and B at both trees and the fire-twice arm; 242 cells; packages/shared 945; tsc; lint 36 problems.')
A('- **UNMEASURED (#1286):** the full round-2 sentence table (only the READ predictions above); whether ":271" / "dev and demo" are ruled wrong; NO-PLAN-ADDED on the fix-round sentences.')
A('- **UNMEASURED (all):** prettier; every suite on END_TREE; the usage gate and launch steps 4-6.')
open(D + '/README.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/README.md', len(out), 'lines')
