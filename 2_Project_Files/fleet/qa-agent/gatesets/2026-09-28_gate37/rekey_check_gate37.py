#!/usr/bin/env python3
r"""rekey_check_gate37.py [<dir>] [--plant <spelling>] — the kit's RE-KEY / NAMESPACE check (STANDING_LINES 2026-09-27: "a namespace check greps EVERY
spelling of the seat token"; "a copied tool is re-keyed for PATHS and ENVIRONMENT-VARIABLE NAMES as well as seat names"; "a re-key checker classifies
prose by SYNTAX, never by how a line reads"; "a re-key checks EVERY predecessor generation a file names"; 2026-09-28: "a tool copied forward is keyed to
its AUTHOR's position ... and a re-key tool must be in its own token map").
gate37's tools were copied from the previous kit (gate36), whose tools were copied from the kit before it (gate35), so the token map below carries BOTH
predecessor generations: their scratch-clone dirs, ref namespaces, workdir prefixes, env-var prefixes, panes, seat tokens (branch segment, seat-record
prefix, seat folder, the bare token as a word, the seat's name in prose, the upper-case tag) and EVERY tool name (the predecessor's re-key tool INCLUDED;
gate36's emit probe included — gate37 carries a pgprobe instead).
  FORBIDDEN anywhere (a live predecessor name would point a gate37 tool at a predecessor's state).
  LINEAGE-ONLY: allowed ONLY on a line whose SYNTAX marks it as lineage (one of the MARK patterns on the same line): the bare predecessor kit words, the
  predecessor PR numbers that are NOT this kit's subjects (#1323-#1326: gate36's merged rows — the develop below; #1321 / #1322: gate35's — #1322 is
  KS-888's MINT half, named in gate37 as RELATED / MERGED), and the predecessor-only tickets (KS-1129 / KS-1124 / KS-1227 / KS-1351 of gate36, KS-1348 of
  gate35). KS-888 is NOT lineage-only: it is #1327's own key this round.
Scans every *.py, *.sh, *.js, *.mjs, *TEMPLATE* file, the filled prompt and launcher and kit.json in <dir> (default: this script's directory), skipping only
superseded_*, .pre-* copies and _quarantine/. THIS FILE IS SCANNED TOO — only the lines between the two `rekey-token-map` markers below are exempt
(they ARE the map); a predecessor name anywhere else in this file is a hit like any other. --plant <spelling> appends `# rekey control plant: <spelling>`
to an in-memory copy of predict_gate37.py (nothing on disk) and must be caught: that is the per-spelling CONTROL. The ONE syntactic exemption: a
possessive `<predecessor kit>'s <name>` naming the predecessor's file is read as lineage, never as use. rc 0 clean, rc 1 on any hit."""
import os, re, sys
D = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; PLANT = None
if '--plant' in args: i = args.index('--plant'); PLANT = args[i + 1]; args = args[:i] + args[i + 2:]
if args: D = args[0]
# rekey-token-map BEGIN
FORBID = [r'\bg36_sp\b', r'refs/g36/', r'\bg36_controls', r'\bg36_emitprobe', r'\bG36_', r'\bQAB36_', r'QA/Secuura-batch1323\b', r'-b38-', r'\bs-b38-', r'seatB-38th',
          r'\bb38\b', r'\bB 38th\b', r'\bB38\b', r'predict_gate36\.py', r'fill_gate36\.py', r'repin_and_launch_gate36\.sh', r'controls_gate36\.sh', r'capture_mail_gate36\.py',
          r'gh_read_gate36\.py', r'keyscan_gate36\.py', r'linear_reads_gate36\.py', r'emitprobe_gate36', r'rekey_check_gate36', r'make_readme_gate36', r'make_commission_gate36',
          r'_api_peek_gate36', r'launch_qa_secuura_batch1323', r'mail_gate36_ready', r'pins_gate36', r'stopcounts_gate36', r'prompt_gate36', r'launcher_gate36',
          r'\bg35_sp\b', r'refs/g35/', r'\bg35_controls', r'\bg35_logprobe', r'\bG35_', r'\bQAB35_', r'QA/Secuura-batch1321\b', r'-b37-', r'\bs-b37-', r'seatB-37th',
          r'\bb37\b', r'\bB 37th\b', r'\bB37\b', r'predict_gate35\.py', r'fill_gate35\.py', r'repin_and_launch_gate35\.sh', r'controls_gate35\.sh', r'capture_mail_gate35\.py',
          r'gh_read_gate35\.py', r'keyscan_gate35\.py', r'linear_reads_gate35\.py', r'logprobe_gate35', r'rekey_check_gate35', r'make_readme_gate35', r'make_commission_gate35',
          r'_api_peek_gate35', r'launch_qa_secuura_batch1321', r'mail_gate35_ready', r'pins_gate35']
LINEAGE = [r'\bgate36\b', r'\bgate35\b', r'#132[1-6]\b', r'\bKS-(1129|1124|1227|1351|1348)\b']
MARK = re.compile(r"copied from gate3[56]|gate3[56]\\?'s|gate3[56] (lineage|->|found|held|gated|measured|W-\d)|-> gate3[45]|\(gate3[56]|round 3[56]|in gate3[56]\b|gate3[56] at |lineage|"
                  r"PRIOR ROUND|prior round|predecessor|re-key|rekey|the previous kit|RELATED|the related|MERGED|merged rows|held (it |#1310 )?NO GO|NO GO (on|under)|CLOSED")
# rekey-token-map END
files = sorted(f for f in os.listdir(D) if (f.endswith(('.py', '.sh', '.js', '.mjs')) or 'TEMPLATE' in f or f.endswith('.prompt.txt') or f == 'kit.json')
               and not f.startswith('superseded_') and '.pre-' not in f)
hits, allowed, n_lines = [], 0, 0
for f in files:
    L = open(os.path.join(D, f), encoding='utf-8', errors='replace').read().split('\n')
    if PLANT and f == 'predict_gate37.py': L = L + ['# rekey control plant: %s' % PLANT]
    inmap = False
    for i, l in enumerate(L):
        n_lines += 1
        if f == os.path.basename(__file__):
            if l.strip() == '# rekey-token-map BEGIN': inmap = True; continue
            if l.strip() == '# rekey-token-map END': inmap = False; continue
            if inmap: continue   # SYNTAX: the token map itself, delimited by its two markers
        if f.startswith('controls_') and l.rstrip().endswith('rekey_check exempts ONLY a line carrying this marker)') and '# rekey-plant-list' in l: continue   # SYNTAX: the NS controls' plant list
        lx = re.sub(r"gate3[56]\\?'s [\w.]+", "<predecessor>'s <lineage>", l)   # SYNTAX: a possessive names the predecessor's file, it does not use it
        for rx in FORBID:
            if re.search(rx, lx): hits.append('%s:%d FORBIDDEN %s | %s' % (f, i + 1, rx, l.strip()[:140]))
        for rx in LINEAGE:
            if re.search(rx, l):
                if MARK.search(l) and not (PLANT and 'control plant' in l): allowed += 1
                else: hits.append('%s:%d LINEAGE-ONLY %s without a lineage marker | %s' % (f, i + 1, rx, l.strip()[:140]))
print('rekey_check_gate37 | dir %s | %d file(s), %d line(s) | %d forbidden spelling(s), %d lineage-only | %d lineage hit(s) ALLOWED by marker%s' % (
    D, len(files), n_lines, len(FORBID), len(LINEAGE), allowed, (' | PLANTED %r' % PLANT) if PLANT else ''))
for h in hits: print('  ' + h)
print('RESULT %s: %d hit(s)' % ('CLEAN' if not hits else 'HITS', len(hits)))
sys.exit(1 if hits else 0)
