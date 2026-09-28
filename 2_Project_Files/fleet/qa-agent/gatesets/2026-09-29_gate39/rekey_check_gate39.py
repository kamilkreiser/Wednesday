#!/usr/bin/env python3
r"""rekey_check_gate39.py [<dir>] [--plant <spelling>] — the kit's RE-KEY / NAMESPACE check (STANDING_LINES 2026-09-27: "a namespace check greps EVERY
spelling of the seat token"; "a copied tool is re-keyed for PATHS and ENVIRONMENT-VARIABLE NAMES as well as seat names"; "a re-key checker classifies
prose by SYNTAX, never by how a line reads"; "a re-key checks EVERY predecessor generation a file names"; 2026-09-28: "a tool copied forward is keyed to
its AUTHOR's position ... and a re-key tool must be in its own token map").
gate39's tools were copied from the previous kit (gate38), whose tools were copied from the kit before it (gate37), so the token map below carries BOTH
predecessor generations: their scratch-clone dirs, ref namespaces, workdir prefixes, env-var prefixes, panes, socket-dir prefixes, seat tokens (branch
segment, seat-record prefix, seat folder, the bare token as a word, the seat's name in prose, the upper-case tag) and EVERY tool name (the predecessor's
re-key tool INCLUDED; gate38's and gate37's pgprobe included — gate39 carries its own pgprobe_gate39).
  FORBIDDEN anywhere (a live predecessor name would point a gate39 tool at a predecessor's state).
  LINEAGE-ONLY: allowed ONLY on a line whose SYNTAX marks it as lineage (one of the MARK patterns on the same line): the bare predecessor kit words, the
  predecessor PR numbers that are NOT this kit's subjects (#1330 / #1333 / #1334: gate38's merged rows; #1327 / #1328: gate37's — #1327 is the change
  that reddened the KS-764 guard, #1328 the merge-base 0d156d12cc0f), gate37's predecessor-only ticket KS-1335, and Seat B 40th's name in prose.
  #1332 is NOT lineage-only: it is this kit's own row (round 2 of 2). KS-888 and KS-1054 are this kit's own keys.
ONE SYNTACTIC EXEMPTION FOR A LIVE NAME: #1332 keeps the branch Seat B 40th opened in round 1 (`…-startup-migration-failure-on-health-b40-2`, READ from
GitHub); that exact branch string is masked before the scan, so Seat B 40th's branch segment anywhere ELSE is still a hit.
Scans every *.py, *.sh, *.js, *.mjs, *.ts, *TEMPLATE* file, the filled prompt and launcher and kit.json in <dir> (default: this script's directory), skipping
only superseded_*, .pre-* copies and _quarantine/. THIS FILE IS SCANNED TOO — only the lines between the two `rekey-token-map` markers below are exempt
(they ARE the map); a predecessor name anywhere else in this file is a hit like any other. --plant <spelling> appends `# rekey control plant: <spelling>`
to an in-memory copy of predict_gate39.py (nothing on disk) and must be caught: that is the per-spelling CONTROL. The possessive exemption: a possessive
`<predecessor kit>'s <name>` naming the predecessor's file is read as lineage, never as use. rc 0 clean, rc 1 on any hit."""
import os, re, sys
D = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; PLANT = None
if '--plant' in args: i = args.index('--plant'); PLANT = args[i + 1]; args = args[:i] + args[i + 2:]
if args: D = args[0]
# rekey-token-map BEGIN
FORBID = [r'\bg38_sp\b', r'refs/g38/', r'\bg38_controls', r'\bg38_pg\b', r'\bG38_', r'\bQAB38_', r'QA/Secuura-batch1330\b', r'-b40-', r'\bs-b40-', r'seatB-40th',
          r'\bb40\b', r'\bB40\b', r'/tmp/q38\.', r'predict_gate38\.py', r'fill_gate38\.py', r'repin_and_launch_gate38\.sh', r'controls_gate38\.sh', r'capture_mail_gate38\.py',
          r'gh_read_gate38\.py', r'keyscan_gate38\.py', r'linear_reads_gate38\.py', r'pgprobe_gate38', r'rekey_check_gate38', r'make_readme_gate38', r'make_commission_gate38',
          r'_api_peek_gate38', r'launch_qa_secuura_batch1330', r'mail_gate38_ready', r'pins_gate38', r'stopcounts_gate38', r'prompt_gate38', r'launcher_gate38',
          r'\bg37_sp\b', r'refs/g37/', r'\bg37_controls', r'\bg37_pgfeas', r'\bG37_', r'\bQAB37_', r'QA/Secuura-batch1327\b', r'-b39-', r'\bs-b39-', r'seatB-39th',
          r'\bb39\b', r'\bB 39th\b', r'\bB39\b', r'predict_gate37\.py', r'fill_gate37\.py', r'repin_and_launch_gate37\.sh', r'controls_gate37\.sh', r'capture_mail_gate37\.py',
          r'gh_read_gate37\.py', r'keyscan_gate37\.py', r'linear_reads_gate37\.py', r'pgprobe_gate37', r'rekey_check_gate37', r'make_readme_gate37', r'make_commission_gate37',
          r'_api_peek_gate37', r'launch_qa_secuura_batch1327', r'mail_gate37_ready', r'pins_gate37']
LINEAGE = [r'\bgate38\b', r'\bgate37\b', r'#13(2[78]|3[034])\b', r'\bKS-1335\b', r'\bB 40th\b']
MARK = re.compile(r"copied from gate3[78]|gate3[78]\\?'s|gate3[78] (lineage|->|found|held|gated|measured|MEASURED|READ|ruled|was|report|W-\d|N-)|-> gate3[67]|\(gate3[78]|round 3[78]|in gate3[78]\b|gate3[78] at |lineage|"
                  r"PRIOR ROUND|prior round|predecessor|re-key|rekey|the previous kit|RELATED|the related|MERGED|merged rows|since #1327|held (it )?NO GO|NO GO|CLOSED|"
                  r"round 1|ROUND 2|round 2|Seat B 40th's|N-1332|N-DEV|first NO GO|STILL OPEN")
BRANCH_1332 = 'startup-migration-failure-on-health-b40-2'   # #1332's own round-1 branch (READ from GitHub): masked, never a hit
# rekey-token-map END
files = sorted(f for f in os.listdir(D) if (f.endswith(('.py', '.sh', '.js', '.mjs', '.ts')) or 'TEMPLATE' in f or f.endswith('.prompt.txt') or f == 'kit.json')
               and not f.startswith('superseded_') and '.pre-' not in f)
hits, allowed, n_lines, masked = [], 0, 0, 0
for f in files:
    L = open(os.path.join(D, f), encoding='utf-8', errors='replace').read().split('\n')
    if PLANT and f == 'predict_gate39.py': L = L + ['# rekey control plant: %s' % PLANT]
    inmap = False
    for i, l in enumerate(L):
        n_lines += 1
        if f == os.path.basename(__file__):
            if l.strip() == '# rekey-token-map BEGIN': inmap = True; continue
            if l.strip() == '# rekey-token-map END': inmap = False; continue
            if inmap: continue   # SYNTAX: the token map itself, delimited by its two markers
        if f.startswith('controls_') and l.rstrip().endswith('rekey_check exempts ONLY a line carrying this marker)') and '# rekey-plant-list' in l: continue   # SYNTAX: the NS controls' plant list
        if BRANCH_1332 in l: masked += l.count(BRANCH_1332); l = l.replace(BRANCH_1332, '<#1332-branch>')
        lx = re.sub(r"gate3[78]\\?'s [\w.]+", "<predecessor>'s <lineage>", l)   # SYNTAX: a possessive names the predecessor's file, it does not use it
        for rx in FORBID:
            if re.search(rx, lx): hits.append('%s:%d FORBIDDEN %s | %s' % (f, i + 1, rx, l.strip()[:140]))
        for rx in LINEAGE:
            if re.search(rx, l):
                if MARK.search(l) and not (PLANT and 'control plant' in l): allowed += 1
                else: hits.append('%s:%d LINEAGE-ONLY %s without a lineage marker | %s' % (f, i + 1, rx, l.strip()[:140]))
print('rekey_check_gate39 | dir %s | %d file(s), %d line(s) | %d forbidden spelling(s), %d lineage-only | %d lineage hit(s) ALLOWED by marker | #1332 branch masked %d time(s)%s' % (
    D, len(files), n_lines, len(FORBID), len(LINEAGE), allowed, masked, (' | PLANTED %r' % PLANT) if PLANT else ''))
for h in hits: print('  ' + h)
print('RESULT %s: %d hit(s)' % ('CLEAN' if not hits else 'HITS', len(hits)))
sys.exit(1 if hits else 0)
