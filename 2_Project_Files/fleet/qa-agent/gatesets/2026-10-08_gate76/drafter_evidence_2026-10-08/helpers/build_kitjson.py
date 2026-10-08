#!/usr/bin/env python3
"""build_kitjson.py — the gate76 drafter's generator: every PR-specific number in kit.json is READ here from the drafter's scratch clone
(read verbs only) and the PR API files saved by pr_probe.py, never typed. Usage: build_kitjson.py <clone> <api-dir> <out kit.json> [<old kit.json>]
The prose fields (kind, NOTEs, rulings pointers) are literal; script_sha256 is carried from <old kit.json> when given (filled by pin_kit.py)."""
import hashlib, json, os, re, subprocess, sys

CL, API, OUT = sys.argv[1:4]
OLD = json.load(open(sys.argv[4])) if len(sys.argv) > 4 and os.path.exists(sys.argv[4]) else {}
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D0 = '0a6177ea5482227e83d5045b68b8577a56326ffc'
FLOW = 'Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html'
CHEAT = 'Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html'


def g(*a): return subprocess.run(['git', '-C', CL] + list(a), capture_output=True, text=True, check=True).stdout
def gb(rev, p): return subprocess.run(['git', '-C', CL, 'show', '%s:%s' % (rev, p)], capture_output=True, check=True).stdout
def obj(rev, p):
    f = g('ls-tree', rev, '--', p).split(); return f[2] if len(f) >= 3 else ''
def mode(rev, p):
    f = g('ls-tree', rev, '--', p).split(); return f[0] if len(f) >= 3 else ''


src = open(os.path.join(HERE, 'composee5_copy.py'), encoding='utf-8').read().split('\n')
def rx(ln):
    m = re.search(r"re\.findall\(r'(.+?)', \"\\n\"\.join\(lines\), (re\.S \| re\.I)\)", src[ln - 1]); return re.compile(m.group(1), re.S | re.I)
FRX = rx(66); CRX = re.compile(rx(82).pattern.replace('&mdash;', '(?:&mdash;|\u2014)'), re.S | re.I)
fnums = lambda t: [int(x) for x in FRX.findall(t)]
ckeys = lambda t: [re.findall(r'(?:&mdash;|\u2014)\s*(KS-\d+)', m)[-1] for m in re.findall(r'<h2\b[^>]*>(.*?)</h2>', t, re.S | re.I)]  # per heading (lib_gate76.cheat_key_pos)

ROWDEF = {
    '1427': dict(ticket='KS-1274', flow_num=35, cheat_key='KS-1274', author_seat='Seat R 18th', lane='R',
                 branch='feature/ks-1274-trivy-bare-object-guard-ra18-1', head='2b6da5f561b05a820bbe1ab5e891bff9f4f531c8',
                 ready='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-08_seatR18_READY.txt',
                 wrap='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-08_seatR18_WRAP.txt',
                 handover='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatR18-2026-10-08.md',
                 runtime_change=True, kind='CI job (Blockchain/Testing/jobs/04-container-trivy.sh) + its three stubbed shell suites'),
    '1428': dict(ticket='KS-593', flow_num=39, cheat_key='KS-593', author_seat='Seat G 4th', lane='G',
                 branch='feature/ks-593-not-a-server-error-originate-three-passes-g4-1', head='64eafead891e81f5adb4e46aaa94ff6a6ace1998',
                 ready='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-08_seatG4_READY.txt',
                 wrap=None,
                 handover='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatG4-2026-10-08.md',
                 runtime_change=True, kind='runtime product change in services/originate (adminConfig, documents share, signatories) + jest suites'),
}
rows = {}
for r, d in ROWDEF.items():
    h = d['head']
    par = g('log', '-1', '--format=%P', h).split()
    ns = {}
    for l in g('diff', '--numstat', D0, h).strip().split('\n'):
        a, dl, p = l.split('\t', 2); ns[p] = [int(a), int(dl)]
    modes = {p: [mode(D0, p), mode(h, p)] for p in ns if not p.startswith('Projects Documents/')}
    msg = g('log', '-1', '--format=%B', h)
    subj = g('log', '-1', '--format=%s', h).rstrip('\n')
    api = json.load(open(os.path.join(API, 'pr_%s.json' % r)))
    body = open(os.path.join(API, 'body_%s.md' % r), 'rb').read()
    hb = {}
    for doc, p in (('flow', FLOW), ('cheat', CHEAT)): hb[doc] = obj(h, p)
    hand = d['handover']
    hs = hashlib.sha256(open(hand, 'rb').read()).hexdigest()[:16] if os.path.exists(hand) else None
    rows[r] = {
        'pr': r, 'ticket': d['ticket'], 'own_keys_default': [d['ticket']], 'keys_hyphenated_allowed': [d['ticket']],
        'tier': 'T2', 'kind': d['kind'], 'author_seat': d['author_seat'], 'author_lane': d['lane'], 'branch': d['branch'],
        'head_expected': h, 'end_tree': g('rev-parse', h + '^{tree}').strip(), 'parent_count': len(par), 'parents': par,
        'subject': subj, 'subject_len': len(subj), 'subject_ascii': subj.isascii(),
        'pr_title': api['title'], 'pr_title_len': len(api['title']), 'pr_title_ascii': api['title'].isascii(),
        'branch_trailer_bytes': len(g('log', '-1', '--format=%(trailers)', h).encode()),
        'branch_coauthor_lines': len(re.findall(r'(?im)^co-authored-by:', msg)),
        'branch_keys_hyphenated': sorted(set(re.findall(r'\bKS-\d+\b', msg))),
        'branch_closing_adjacency': re.findall(r'(?i)\b(?:clos(?:e|es|ed)|fix(?:es|ed)?|resolv(?:e|es|ed))\s+KS-\d+', msg),
        'pr_body_keys_hyphenated': sorted(set(re.findall(r'\bKS-\d+\b', api['title'] + '\n' + (api.get('body') or '')))),
        'pr_body_refs': sorted(set(re.findall(r'Refs:?\s+(KS-\d+)\b', api.get('body') or ''))),
        'body_sha256_16_at_draft': hashlib.sha256(body).hexdigest()[:16], 'body_bytes_at_draft': len(body),
        'body_generated_with_lines': len(re.findall(r'(?im)^.*generated with \[claude code\]', body.decode())),
        'numstat': ns, 'modes': modes, 'flow_num': d['flow_num'], 'cheat_key': d['cheat_key'],
        'flow_blob_head': hb['flow'], 'cheat_blob_head': hb['cheat'],
        'ready': d['ready'], 'wrap': d['wrap'], 'handover': hand, 'handover_sha256_16': hs,
        'runtime_change': d['runtime_change'], 'live_sweep_owed': True,
        'api_at_draft': {'state': api['state'], 'merged': api.get('merged'), 'commits': api['commits'], 'changed_files': api['changed_files'],
                         'additions': api['additions'], 'deletions': api['deletions'], 'mergeable_state': api.get('mergeable_state')},
    }

fd, cd = gb(D0, FLOW).decode(), gb(D0, CHEAT).decode()
K = {
    'kit': 'gate76',
    'kind': 'BATCHED T2 gate over TWO Secuura/Blockchain PRs, each with its OWN verdict: #1427 KS-1274 (Seat R 18th): job 04 records a trivy run that exits 0 with a bare `{}` (neither Results nor ArtifactName) as scan-failed and exits 1; the three trivy suites move their clean stub to `{"Results":[]}`. #1428 KS-593 (Seat G 4th): three originate routes turn a raw 500 into the route\'s existing 400 (adminConfig negative offset x2 routes, documents share non-object recipient [SECURITY-ADJACENT], signatories non-uuid id x2 routes). File-disjoint EXCEPT the two platform docs, which BOTH PRs append to at the same tail: the second lander needs a docs-only KEEP-BOTH merge-in (composed docs VERBATIM, gate73 shape).',
    'drafted': '2026-10-08 18:27-AEDT (07:27Z-) by one Wednesday kit-drafting subagent; built and dry-run only, NOT launched',
    'NOTE_pins': 'Every PR-specific value below is the DRAFTER\'S pin, read by drafter_evidence_2026-10-08/helpers/build_kitjson.py. The repin script and every check script take live values as REQUIRED arguments and compare them with these; nothing defaults to them.',
    'client_project': 'Secuura/Blockchain',
    'tier': 'T2 per row (Wednesday): #1427 a CI-job product change with a red-proof re-run by the gate; #1428 a runtime product change (three routes), the share route SECURITY-ADJACENT (read through-code by Wednesday: no authorisation decision moves). The drafter found no reason to go up.',
    'round': '1',
    'routing': '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf',
    'pane': 'QA/Secuura-gate76',
    'routing_line': 'QA/Secuura-gate76|coagent@agentmail.to|yes',
    'report_dir': '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-08-gate76',
    'report_dir_name': '2026-10-08-gate76',
    'verdict_subject': '[QA -> Wednesday] GATE76 (T2 x2): #1427 KS-1274 trivy bare-object guard + #1428 KS-593 originate 500->400',
    'no_go_template': 'NO GO (gate76): <1427|1428> at <head 12-hex> \u2014 <N-<pr>-n: the blocker, one line>',
    'develop_at_draft': D0,
    'develop_tree_at_draft': g('rev-parse', D0 + '^{tree}').strip(),
    'develop_tree_NOTE': 'calibration: develop 0a6177ea5482 IS the #1426 squash (Seat R 17th) and its tree 5f456a0128fe IS gate75\'s predicted_squash.tree: the lineage\'s last prediction landed byte for byte.',
    'base': D0,
    'base_NOTE': 'Both heads have ONE parent and it IS develop at draft (base == develop). Each PR ALONE squashes to its own END_TREE; the SECOND lander needs a docs-only keep-both merge-in (merge-tree of the two heads: rc 1 on exactly the two docs).',
    'checkout': '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files',
    'forbidden_root': '/Volumes/DevMASTER/!CODING',
    'secuura_env': '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env',
    'gh_repo': 'Secuura/Distributed_Secuura',
    'github_url': 'git@github.com:Secuura/Distributed_Secuura.git',
    'qa_dir': '/Volumes/DevMASTER/!CODING/Testing Agent MAIN',
    'charter': '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md',
    'usage_gate': '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh',
    'usage_stop': '100',
    'usage_authority': '/Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-08_new-account-push-merge-test-as-much-as-possible.md',
    'usage_authority_card': 'secuura-raise-backlog-at-99pct-1008',
    'usage_NOTE': 'The gauge read 91% at draft (usage_gate.sh --check rc 3 at the default 90 cut, 07:27:47Z). Kam\'s new-account grant (status: live, card secuura-raise-backlog-at-99pct-1008 = a, clauses raise / GATE / merge) sets the stop to 100. The repin exports WED_USAGE_STOP=100 for its OWN usage check AND for `cockpit.sh add` (gate75\'s first real run refused at cockpit add, rc 3 at 97%, because only the --check carried it) ONLY after reading the grant file. Expiry is an EVENT: the account renewal (~Fri 9 Oct morning), an account switch, or Kam\'s word.',
    'cockpit': '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/cockpit/cockpit.sh',
    'prompt': 'prompt_gate76.txt', 'launcher': 'launch_qa_secuura_gate76.sh', 'repin': 'repin_and_launch_gate76.sh',
    'trailer_control': 'bf277eead26897bb648c801f92308681dbdaffdc',
    'trailer_control_raw_bytes': len(g('log', '-1', '--format=%(trailers)', 'bf277eead26897bb648c801f92308681dbdaffdc').encode()),
    'closing_rx': '\\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\\b\\s*:?\\s*KS-\\d+',
    'closing_rx_broad': '(?i)\\b(?:clos(?:e|es|ed|ing)|fix(?:es|ed|ing)?|resolv(?:e|es|ed|ing)|complete[sd]?)[\\s:,\u2014-]*KS-\\d+',
    'squash_max': 92,
    'merge_order_default': ['1428', '1427'],
    'merge_order_NOTE': 'RULINGS Q-ORDER76 default: #1428 FIRST (no merge-in: its squash tree == its END_TREE, the security-adjacent code lands exactly as gated), then #1427 with a docs-only keep-both merge-in on ITS OWN R-lane branch (no cross-lane branch adoption for an R merge seat). The reverse order is predicted too (predicted_chain.orders).',
    'merge_seat': None,
    'merge_seat_ordinal': None,
    'merge_seat_NOTE': 'RULINGS Q-SEAT76 is OPEN on purpose: the R pane is held by Seat R 19th (a RAISE seat, launched 2026-10-08) and the G pane is G 4th -> G 5th. Neither author (Seat R 18th, Seat G 4th) may merge. The launcher and repin refuse rc 8 until kit.json names a lane + ordinal; the GO string is rendered from it.',
    'author_seats': ['Seat R 18th', 'Seat G 4th'],
    'docs': {
        'flow': FLOW, 'cheat': CHEAT,
        'guard_suite': 'systemTest/__tests__/html_docs_matrix.test.sh',
        'guard_checker': 'systemTest/__tests__/support/html_docs_check.mjs',
        'close_tag_rx': '^\\s*</body>\\s*$',
        'flow_blob_base': obj(D0, FLOW), 'cheat_blob_base': obj(D0, CHEAT),
        'flow_seq_base': fnums(fd), 'cheat_seq_base': ckeys(cd),
        'rule': 'SKILL \u00a74 (same commit, both files, reflects what changed) + gate71/73 Q-06N carried: each PR appends ONE flow block (h2 `N. \u2026 (KS-n)`) and ONE cheat section (h2 `\u2026 \u2014 KS-n`) immediately before `</body>`; flow numbers UNIQUE (ascending NOT asserted: develop already reads `\u2026 30 31 26` by design); KEEP-BOTH: the second lander\'s block goes AFTER the first lander\'s, each byte-identical to its head\'s block. NEVER `git merge-file --union`, never a hand edit of git\'s conflict hunk (gate73 Q-UNION, BINDING). html_docs_matrix 12/0 is NOT tag-balance evidence (STANDING_LINES :439): count open/close per tag, `<code(\\s[^>]*)?>` attribute-aware.',
    },
    'reader_source': {'copy': 'composee5_copy.py', 'copied_from': '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-07_gate73/composee5_copy.py',
                      'sha256': hashlib.sha256(open(os.path.join(HERE, 'composee5_copy.py'), 'rb').read()).hexdigest(), 'flow_num_line': 66, 'cheat_key_line': 82},
    'old_sameline_rx': '<h2[^>]*>(\\d+)\\.',
    'merge_tree_control': {'NOTE': 'a pair KNOWN to conflict on the two docs (gate73 #1407 and #1409 heads): merge-tree must read rc 1 naming both docs, or a clean read proves nothing',
                           'ours': '3be1a5317735c11b377b89fa98e1ac5595f84ef0', 'theirs': 'c8899a95dc445fd3ac87ec3db33835f5acb1e155', 'files': [FLOW, CHEAT]},
    'neighbour_1383': {'pr': '1383', 'ticket': 'KS-1401', 'head_at_draft': '32e8459bc0f51d1af492aae7c0b3d9754f78c9bf',
                       'NOTE': 'HELD, not ours. It edits both docs; REPORT only; never merged by the merge seat.'},
    'tooling_paths': OLD.get('tooling_paths') or [
        '.githooks/pre-push', '.claude/skills/secuura-test-discipline/SKILL.md', 'systemTest/CLAUDE.md',
        'Blockchain/Dev/scripts/preflight/preflight.sh', 'Blockchain/Dev/scripts/run-shell-suites.sh',
        'Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh', 'Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh',
        'systemTest/scripts/check-package-format.sh', 'systemTest/__tests__/html_docs_matrix.test.sh', 'systemTest/__tests__/support/html_docs_check.mjs',
        'systemTest/__tests__/no_hardcoded_slot_literals.test.sh', 'systemTest/schemathesis/config/schemathesis-baseline.json', '.github/workflows',
        'Blockchain/Dev/services/originate/jest.config.js', 'Blockchain/Dev/services/originate/package.json', 'Blockchain/Dev/package-lock.json',
        'Blockchain/Testing/ci/orchestrate.sh', 'Blockchain/Testing/jobs/09-aggregate-report.sh',
        'Blockchain/Dev/services/originate/src/middleware/auth.ts', 'Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts'],
    'tooling_changed_by_row': {'1427': [], '1428': ['Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts']},
    'tooling_NOTE': 'P10 NO-NEW-LEG: the PR changes EXACTLY its declared tooling paths and no other (the hook, the preflight, the shell-suite runner, the format gate, the doc guard, the skill, CI workflows, originate jest config / package.json / lockfile, the trivy job\'s consumers 09-aggregate + orchestrate, the originate auth middleware). #1428 declares ONE: the KS-1293 hermetic manifest gains ONE SUBJECTS line.',
    'preexisting_mismatch': {'files': {p: obj(D0, p)[:12] for p in ('Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh', 'Blockchain/Dev/scripts/run-shell-suites.sh', 'Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh')},
                             'ruling': 'Carried from gate73 R3: `VERDICT: MISMATCH \u2014 STOP` inside green runs is BASE-STATE (G 4th traced it to the F-925-3 fixture arm of preflight_deps.test.sh); the gate confirms the three files byte-identical base == head == develop.'},
    'actions': {
        'predicate': 'SUBSET (never equality): each head\'s failing-job set per workflow must be a SUBSET of the comparator\'s failing set; any red outside the three classes is a NO GO finding for THAT row',
        'classes': {
            '1': {'workflow': 'Security Scanning', 'allowed_failing_jobs': ['Dependency Audit'], 'needles': ['expected exit 0 (clean), got 1'],
                  'failed_step_prefix': 'Audit-contract suites', 'comparator': 'history: develop runs no Security Scanning on push',
                  'wording': 'the ADVISORY-FREEZE class (KS-1148): pre-existing, fails on every recent head'},
            '2': {'workflow': 'PR Security Gates (KS-168)', 'comparator': 'the comparator\'s own run; head failing set SUBSET of it'},
            '3': {'workflow': 'pr', 'comparator': 'the comparator\'s own run of `pr`'}},
        'false_zero_observed_gate74': 'a 0-runs comparator read is RE-READ before it is believed (gate74: 0 then 2 within a minute).'},
    'actions_comparator': 'base',
    'actions_comparator_NOTE': 'base == develop == 0a6177ea5482 at draft for BOTH rows, so develop / base / union are ONE sha; the comparator stays `base` (each PR\'s own parent: like-for-like) if develop moves, and the gate prints all three. For the SECOND lander\'s merge-in commit M, the merge seat reads Actions on M against M\'s develop parent; that is the merge seat\'s ADDENDUM input, not this gate\'s.',
    'platform_suites_unmeasured': ['Schemathesis', 'Akto', 'Playwright', 'Performance (k6)'],
    'rows': rows,
}
json.dump(K, open(OUT, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('wrote', OUT, 'rows', list(rows), 'flow tail', K['docs']['flow_seq_base'][-4:], 'cheat tail', K['docs']['cheat_seq_base'][-3:])
for r, R in rows.items():
    print(r, R['end_tree'][:12], R['parents'], R['subject_len'], R['branch_trailer_bytes'], R['branch_keys_hyphenated'], R['branch_closing_adjacency'],
          R['pr_body_refs'], R['body_bytes_at_draft'], R['body_sha256_16_at_draft'], R['body_generated_with_lines'], R['handover_sha256_16'], R['modes'])
