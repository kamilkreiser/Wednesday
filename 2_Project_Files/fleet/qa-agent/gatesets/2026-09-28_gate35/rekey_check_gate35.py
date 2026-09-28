#!/usr/bin/env python3
r"""rekey_check_gate35.py [<dir>] [--plant <spelling>] — the kit's RE-KEY / NAMESPACE check (STANDING_LINES 2026-09-27: "a namespace check greps EVERY
spelling of the seat token"; "a copied tool is re-keyed for PATHS and ENVIRONMENT-VARIABLE NAMES as well as seat names"; "a re-key checker classifies
prose by SYNTAX, never by how a line reads"; "a re-key checks EVERY predecessor generation a file names"; 2026-09-28: "a tool copied forward is keyed to
its AUTHOR's position ... and a re-key tool must be in its own token map").
gate35's tools were copied from the previous kit (gate34), whose tools were copied from the kit before it (gate33), so the token map below carries BOTH
predecessor generations: their scratch-clone dirs, ref namespaces, workdir prefixes, env-var prefixes, panes, seat tokens (branch segment, seat-record
prefix, seat folder, the bare token as a word, the seat's name in prose, the upper-case tag) and EVERY tool name (the predecessor's re-key tool INCLUDED).
  FORBIDDEN anywhere (a live predecessor name would point a gate35 tool at a predecessor's state).
  LINEAGE-ONLY: allowed ONLY on a line whose SYNTAX marks it as lineage (one of the MARK patterns on the same line): the bare predecessor kit words, the
  predecessor PR numbers that are NOT this kit's subjects (#1316-#1320: gate34's merged rows; #1311-#1315: gate33's), and the predecessor-only tickets.
  (#1310 is NOT lineage-only: it is logprobe's FILE-LEAK control revision and the PR #1321 replaces; its pane and its seat's branch segment stay FORBIDDEN.
  KS-1346 / KS-908 are NOT lineage-only either: they are this kit's carry-forward keys — the W-3 remainder and #1322's merged co-file.)
Scans every *.py, *.sh, *.js, *TEMPLATE* file, the filled prompt and launcher and kit.json in <dir> (default: this script's directory), skipping only
superseded_*, .pre-* copies and _quarantine/. THIS FILE IS SCANNED TOO — only the lines between the two `rekey-token-map` markers below are exempt
(they ARE the map); a predecessor name anywhere else in this file is a hit like any other. --plant <spelling> appends `# rekey control plant: <spelling>`
to an in-memory copy of predict_gate35.py (nothing on disk) and must be caught: that is the per-spelling CONTROL. The ONE syntactic exemption: a
possessive `<predecessor kit>'s <name>` naming the predecessor's file is read as lineage, never as use. rc 0 clean, rc 1 on any hit."""
import os, re, sys
D = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; PLANT = None
if '--plant' in args: i = args.index('--plant'); PLANT = args[i + 1]; args = args[:i] + args[i + 2:]
if args: D = args[0]
# rekey-token-map BEGIN
FORBID = [r'\bg34_sp\b', r'refs/g34/', r'\bg34_controls', r'\bg34_logprobe', r'\bG34_', r'\bQAB34_', r'QA/Secuura-batch1316\b', r'-b36-', r'\bs-b36-', r'seatB-36th',
          r'\bb36\b', r'\bB 36th\b', r'\bB36\b', r'predict_gate34\.py', r'fill_gate34\.py', r'repin_and_launch_gate34\.sh', r'controls_gate34\.sh', r'capture_mail_gate34\.py',
          r'gh_read_gate34\.py', r'keyscan_gate34\.py', r'linear_reads_gate34\.py', r'logprobe_gate34', r'rekey_check_gate34', r'make_readme_gate34', r'make_commission_gate34',
          r'_api_peek_gate34', r'launch_qa_secuura_batch1316', r'mail_gate34_ready', r'pins_gate34', r'stopcounts_gate34', r'prompt_gate34', r'launcher_gate34',
          r'\bg33_sp\b', r'refs/g33/', r'\bg33_controls', r'\bg33_logprobe', r'\bG33_', r'\bQAB33_', r'QA/Secuura-batch1310\b', r'-b35-', r'\bs-b35-', r'seatB-35th',
          r'\bb35\b', r'\bB 35th\b', r'\bB35\b', r'predict_gate33\.py', r'fill_gate33\.py', r'repin_and_launch_gate33\.sh', r'controls_gate33\.sh', r'capture_mail_gate33\.py',
          r'gh_read_gate33\.py', r'keyscan_gate33\.py', r'linear_reads_gate33\.py', r'logprobe_gate33', r'rekey_check_gate33', r'make_readme_gate33', r'make_commission_gate33',
          r'_api_peek_gate33', r'launch_qa_secuura_batch1310', r'mail_gate33_ready', r'pins_gate33']
LINEAGE = [r'\bgate34\b', r'\bgate33\b', r'#131[1-9]\b', r'#1320\b', r'\bKS-(747|692|586|730|1121|1221|1220|1351)\b']
MARK = re.compile(r"copied from gate3[34]|gate3[34]\\?'s|gate3[34] (lineage|->|found|held|gated|measured|W-\d)|-> gate3[23]|\(gate3[34]|round 3[34]|in gate3[34]\b|gate3[34] at |lineage|"
                  r"PRIOR ROUND|prior round|predecessor|re-key|rekey|the previous kit|RELATED|the related|MERGED|merged rows|held (it |#1310 )?NO GO|NO GO (on|under)|CLOSED")
# rekey-token-map END
files = sorted(f for f in os.listdir(D) if (f.endswith(('.py', '.sh', '.js')) or 'TEMPLATE' in f or f.endswith('.prompt.txt') or f == 'kit.json')
               and not f.startswith('superseded_') and '.pre-' not in f)
hits, allowed, n_lines = [], 0, 0
for f in files:
    L = open(os.path.join(D, f), encoding='utf-8', errors='replace').read().split('\n')
    if PLANT and f == 'predict_gate35.py': L = L + ['# rekey control plant: %s' % PLANT]
    inmap = False
    for i, l in enumerate(L):
        n_lines += 1
        if f == os.path.basename(__file__):
            if l.strip() == '# rekey-token-map BEGIN': inmap = True; continue
            if l.strip() == '# rekey-token-map END': inmap = False; continue
            if inmap: continue   # SYNTAX: the token map itself, delimited by its two markers
        if f.startswith('controls_') and l.rstrip().endswith('rekey_check exempts ONLY a line carrying this marker)') and '# rekey-plant-list' in l: continue   # SYNTAX: the NS controls' plant list
        lx = re.sub(r"gate3[34]\\?'s [\w.]+", "<predecessor>'s <lineage>", l)   # SYNTAX: a possessive names the predecessor's file, it does not use it
        for rx in FORBID:
            if re.search(rx, lx): hits.append('%s:%d FORBIDDEN %s | %s' % (f, i + 1, rx, l.strip()[:140]))
        for rx in LINEAGE:
            if re.search(rx, l):
                if MARK.search(l) and not (PLANT and 'control plant' in l): allowed += 1
                else: hits.append('%s:%d LINEAGE-ONLY %s without a lineage marker | %s' % (f, i + 1, rx, l.strip()[:140]))
print('rekey_check_gate35 | dir %s | %d file(s), %d line(s) | %d forbidden spelling(s), %d lineage-only | %d lineage hit(s) ALLOWED by marker%s' % (
    D, len(files), n_lines, len(FORBID), len(LINEAGE), allowed, (' | PLANTED %r' % PLANT) if PLANT else ''))
for h in hits: print('  ' + h)
print('RESULT %s: %d hit(s)' % ('CLEAN' if not hits else 'HITS', len(hits)))
sys.exit(1 if hits else 0)
