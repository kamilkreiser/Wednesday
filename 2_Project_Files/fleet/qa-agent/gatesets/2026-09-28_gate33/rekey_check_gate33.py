#!/usr/bin/env python3
r"""rekey_check_gate33.py [<dir>] [--plant <spelling>] — the kit's RE-KEY / NAMESPACE check (STANDING_LINES 2026-09-27: "a namespace check greps EVERY
spelling of the seat token"; "a copied tool is re-keyed for PATHS and ENVIRONMENT-VARIABLE NAMES as well as seat names"; "a re-key checker classifies
prose by SYNTAX, never by how a line reads"; "a re-key checks EVERY predecessor generation a file names"; 2026-09-28: "a tool copied forward is keyed to
its AUTHOR's position ... and a re-key tool must be in its own token map").
gate33's tools were copied from the previous kit, whose tools were copied from the kit before it, so the token map below carries BOTH predecessor
generations: their scratch-clone dirs, ref namespaces, workdir prefixes, env-var prefixes, panes, seat tokens (branch segment, seat-record prefix, seat
folder, the bare token as a word, the seat's name in prose, the upper-case tag) and EVERY tool name (the predecessor's re-key tool INCLUDED).
  FORBIDDEN anywhere (a live predecessor name would point a gate33 tool at a predecessor's state).
  LINEAGE-ONLY: allowed ONLY on a line whose SYNTAX marks it as lineage (one of the MARK patterns on the same line): the bare predecessor kit words, the
  predecessor PR numbers that are NOT this kit's subjects, and the predecessor tickets. (The closed #1302 / #1296 / #1297 are THIS kit's subjects — the
  PRs its rows replace — so they are not lineage-only; KS-1348 is this kit's own key.)
Scans every *.py, *.sh, *.js, *TEMPLATE* file, the filled prompt and launcher and kit.json in <dir> (default: this script's directory), skipping only
superseded_*, .pre-* copies and _quarantine/. THIS FILE IS SCANNED TOO — only the lines between the two `rekey-token-map` markers below are exempt
(they ARE the map); a predecessor name anywhere else in this file is a hit like any other. --plant <spelling> appends `# rekey control plant: <spelling>`
to an in-memory copy of predict_gate33.py (nothing on disk) and must be caught: that is the per-spelling CONTROL. The ONE syntactic exemption: a
possessive `<predecessor kit>'s <name>` naming the predecessor's file is read as lineage, never as use. rc 0 clean, rc 1 on any hit."""
import os, re, sys
D = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; PLANT = None
if '--plant' in args: i = args.index('--plant'); PLANT = args[i + 1]; args = args[:i] + args[i + 2:]
if args: D = args[0]
# rekey-token-map BEGIN
FORBID = [r'\bg32_sp\b', r'refs/g32/', r'\bg32_controls', r'\bg32_aktolint', r'\bG32_', r'\bQAB32_', r'QA/Secuura-batch1304\b', r'-b34-', r'\bs-b34-', r'seatB-34th',
          r'\bb34\b', r'\bB 34th\b', r'\bB34\b', r'predict_gate32\.py', r'fill_gate32\.py', r'repin_and_launch_gate32\.sh', r'controls_gate32\.sh', r'capture_mail_gate32\.py',
          r'gh_read_gate32\.py', r'keyscan_gate32\.py', r'linear_reads_gate32\.py', r'aktolint_gate32', r'rekey_check_gate32', r'make_readme_gate32', r'make_commission_gate32',
          r'_api_peek_gate32', r'launch_qa_secuura_batch1304',
          r'\bg31_sp\b', r'refs/g31/', r'\bg31_controls', r'\bg31_logprobe', r'\bG31_', r'\bQAB31_', r'QA/Secuura-batch1300\b', r'-b33-', r'\bs-b33-', r'seatB-33rd',
          r'\bb33\b', r'\bB 33rd\b', r'\bB33\b', r'predict_gate31\.py', r'fill_gate31\.py', r'repin_and_launch_gate31\.sh', r'controls_gate31\.sh', r'capture_mail_gate31\.py',
          r'gh_read_gate31\.py', r'keyscan_gate31\.py', r'linear_reads_gate31\.py', r'tokeq_gate31\.js', r'logprobe_gate31', r'rekey_check_gate31', r'launch_qa_secuura_batch1300']
LINEAGE = [r'\bgate32\b', r'\bgate31\b', r'#130[013-9]\b', r'\bKS-(1227|1090|1205|1212|1108|1196|1334|1349|1350)\b']
MARK = re.compile(r"copied from gate3[12]|gate3[12]\\?'s|gate3[12] (lineage|->)|-> gate3[01]|\(gate3[12]|round 3[12]|in gate3[12]\b|gate3[12] at |gate3[12] declared|lineage|"
                  r"PRIOR ROUND|prior round|predecessor|re-key|rekey|the previous kit|gate32's six squashes|the develop move|held (it )?NO GO|NO GO (on|under)")
# rekey-token-map END
files = sorted(f for f in os.listdir(D) if (f.endswith(('.py', '.sh', '.js')) or 'TEMPLATE' in f or f.endswith('.prompt.txt') or f == 'kit.json')
               and not f.startswith('superseded_') and '.pre-' not in f)
hits, allowed, n_lines = [], 0, 0
for f in files:
    L = open(os.path.join(D, f), encoding='utf-8', errors='replace').read().split('\n')
    if PLANT and f == 'predict_gate33.py': L = L + ['# rekey control plant: %s' % PLANT]
    inmap = False
    for i, l in enumerate(L):
        n_lines += 1
        if f == os.path.basename(__file__):
            if l.strip() == '# rekey-token-map BEGIN': inmap = True; continue
            if l.strip() == '# rekey-token-map END': inmap = False; continue
            if inmap: continue   # SYNTAX: the token map itself, delimited by its two markers
        if f.startswith('controls_') and l.rstrip().endswith('rekey_check exempts ONLY a line carrying this marker)') and '# rekey-plant-list' in l: continue   # SYNTAX: the NS controls' plant list
        lx = re.sub(r"gate3[12]\\?'s [\w.]+", "<predecessor>'s <lineage>", l)   # SYNTAX: a possessive names the predecessor's file, it does not use it
        for rx in FORBID:
            if re.search(rx, lx): hits.append('%s:%d FORBIDDEN %s | %s' % (f, i + 1, rx, l.strip()[:140]))
        for rx in LINEAGE:
            if re.search(rx, l):
                if MARK.search(l) and not (PLANT and 'control plant' in l): allowed += 1
                else: hits.append('%s:%d LINEAGE-ONLY %s without a lineage marker | %s' % (f, i + 1, rx, l.strip()[:140]))
print('rekey_check_gate33 | dir %s | %d file(s), %d line(s) | %d forbidden spelling(s), %d lineage-only | %d lineage hit(s) ALLOWED by marker%s' % (
    D, len(files), n_lines, len(FORBID), len(LINEAGE), allowed, (' | PLANTED %r' % PLANT) if PLANT else ''))
for h in hits: print('  ' + h)
print('RESULT %s: %d hit(s)' % ('CLEAN' if not hits else 'HITS', len(hits)))
sys.exit(1 if hits else 0)
