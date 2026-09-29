#!/usr/bin/env python3
r"""rekey_check_gate42.py [<dir>] [--plant <spelling>] — the kit's RE-KEY / NAMESPACE check (STANDING_LINES 2026-09-27: "a namespace check greps EVERY
spelling of the seat token"; "a copied tool is re-keyed for PATHS and ENVIRONMENT-VARIABLE NAMES as well as seat names"; "a re-key checker classifies
prose by SYNTAX, never by how a line reads"; "a re-key checks EVERY predecessor generation a file names"; 2026-09-28: "a tool copied forward is keyed to
its AUTHOR's position ... and a re-key tool must be in its own token map").
gate42's tools were copied from the previous kit (gate40), whose tools were copied from gate39, so the token map below is WIDENED to carry gate40's
namespace (Wednesday's commission: "widen any re-key checker to cover gate40's namespace") AND keeps gate39's: their scratch-clone dirs, ref
namespaces, workdir prefixes, env-var prefixes, panes, socket-dir prefixes, seat tokens (branch segment, seat-record prefix, seat folder, the bare
token as a word, the upper-case tag) and EVERY tool name (the predecessor's re-key tool INCLUDED; gate40's pgprobe family too — gate42 has no
Postgres probe, so a pgprobe name keyed to gate40 is a stale copy). gate38's generation, which gate40's map carried, is dropped: no gate42 file was copied
from a gate39 file (every copy is from gate40, READ — its lineage).
  FORBIDDEN anywhere (a live predecessor name would point a gate42 tool at a predecessor's state).
  LINEAGE-ONLY: allowed ONLY on a line whose SYNTAX marks it as lineage (one of the MARK patterns on the same line): the bare predecessor kit words
  (gate40, gate39), gate40's and gate39's PR numbers (#1338 / #1337 / #1332: MERGED rows), and Seat B 42nd's name in prose. KS-1378 / KS-729 are this
  kit's own keys.
Scans every *.py, *.sh, *.js, *.cjs, *.mjs, *.ts, *TEMPLATE* file, the filled prompt and launcher and kit.json in <dir> (default: this script's directory),
skipping only superseded_*, .pre-* copies and _quarantine*/. THIS FILE IS SCANNED TOO — only the lines between the two `rekey-token-map` markers below
are exempt (they ARE the map); a predecessor name anywhere else in this file is a hit like any other. --plant <spelling> appends `# rekey control
plant: <spelling>` to an in-memory copy of predict_gate42.py (nothing on disk) and must be caught: that is the per-spelling CONTROL. The possessive
exemption: a possessive `<predecessor kit>'s <name>` naming the predecessor's file is read as lineage, never as use. HEX GUARD (Seat B 43rd's handover,
thing 4): a seat token buried in a hex run (a SHA or a uuid) is not a token — every 7+-char hex run is masked before the scan. rc 0 clean, rc 1 on any hit."""
import os, re, sys
D = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; PLANT = None
if '--plant' in args: i = args.index('--plant'); PLANT = args[i + 1]; args = args[:i] + args[i + 2:]
if args: D = args[0]
# rekey-token-map BEGIN
FORBID = [r'\bg40_sp\b', r'refs/g40/', r'\bg40_controls', r'\bg40_pg\b', r'\bg40fin\b', r'\bG40_', r'\bQAB40_', r'QA/Secuura-batch1338\b', r'-b42-', r'\bs-b42-', r'seatB-42nd',
          r'\bb42\b', r'\bB42\b', r'/tmp/q40\.', r'/tmp/q40g\.', r'\bqa40\.', r'predict_gate40\.py', r'fill_gate40\.py', r'repin_and_launch_gate40\.sh', r'controls_gate40\.sh', r'capture_mail_gate40\.py',
          r'gh_read_gate40\.py', r'keyscan_gate40\.py', r'linear_reads_gate40\.py', r'pgprobe_gate40', r'rekey_check_gate40', r'make_readme_gate40', r'make_commission_gate40',
          r'_api_peek_gate40', r'launch_qa_secuura_batch1338', r'mail_gate40_ready', r'pins_gate40', r'stopcounts_gate40', r'prompt_gate40', r'launcher_gate40', r'batch1338\.prompt',
          r'installprobe_gate40', r'2026-09-29-batch1338-g40',
          r'\bg39_sp\b', r'refs/g39/', r'\bg39_controls', r'\bg39_pg\b', r'\bG39_', r'\bQAB39_', r'QA/Secuura-batch1337\b', r'-b41-', r'\bs-b41-', r'seatB-41st',
          r'\bb41\b', r'\bB41\b', r'/tmp/q39\.', r'predict_gate39\.py', r'fill_gate39\.py', r'repin_and_launch_gate39\.sh', r'controls_gate39\.sh', r'capture_mail_gate39\.py',
          r'gh_read_gate39\.py', r'keyscan_gate39\.py', r'linear_reads_gate39\.py', r'pgprobe_gate39', r'rekey_check_gate39', r'make_readme_gate39', r'make_commission_gate39',
          r'_api_peek_gate39', r'launch_qa_secuura_batch1337', r'mail_gate39_ready', r'pins_gate39', r'stopcounts_gate39', r'prompt_gate39', r'launcher_gate39', r'batch1337\.prompt']
LINEAGE = [r'\bgate40\b', r'\bgate39\b', r'#13(32|37|38)\b', r'\bB 42nd\b']
MARK = re.compile(r"copied from gate(39|40)|gate(39|40)\\?'s|gate(39|40) (lineage|->|found|held|gated|measured|MEASURED|READ|ruled|was|report|W-\d|N-)|-> gate3[89]|\(gate(39|40)|round (39|40)|in gate(39|40)\b|gate(39|40) at |lineage|"
                  r"PRIOR ROUND|prior round|predecessor|re-key|rekey|the previous kit|RELATED|the related|MERGED|merged rows|NO GO|CLOSED|Seat B 42nd\\?'s|STILL OPEN")
HEX = re.compile(r'(?<![0-9A-Za-z])[0-9a-f]*\d[0-9a-f]*(?:-[0-9a-f]+)*(?![0-9A-Za-z])')   # a hex run with a digit (SHA / uuid): masked before the scan when >= 7 chars
# rekey-token-map END
files = sorted(f for f in os.listdir(D) if (f.endswith(('.py', '.sh', '.js', '.cjs', '.mjs', '.ts')) or 'TEMPLATE' in f or f.endswith('.prompt.txt') or f == 'kit.json')
               and not f.startswith('superseded_') and '.pre-' not in f)
hits, allowed, n_lines, masked = [], 0, 0, 0
for f in files:
    L = open(os.path.join(D, f), encoding='utf-8', errors='replace').read().split('\n')
    if PLANT and f == 'predict_gate42.py': L = L + ['# rekey control plant: %s' % PLANT]
    inmap = False
    for i, l in enumerate(L):
        n_lines += 1
        if f == os.path.basename(__file__):
            if l.strip() == '# rekey-token-map BEGIN': inmap = True; continue
            if l.strip() == '# rekey-token-map END': inmap = False; continue
            if inmap: continue   # SYNTAX: the token map itself, delimited by its two markers
        if f.startswith('controls_') and l.rstrip().endswith('rekey_check exempts ONLY a line carrying this marker)') and '# rekey-plant-list' in l: continue   # SYNTAX: the NS controls' plant list
        _l2 = HEX.sub(lambda m: '<hex>' if len(m.group(0)) >= 7 else m.group(0), l); masked += _l2.count('<hex>') - l.count('<hex>'); l = _l2
        lx = re.sub(r"gate(39|40)\\?'s [\w.]+", "<predecessor>'s <lineage>", l)   # SYNTAX: a possessive names the predecessor's file, it does not use it
        for rx in FORBID:
            if re.search(rx, lx): hits.append('%s:%d FORBIDDEN %s | %s' % (f, i + 1, rx, l.strip()[:140]))
        for rx in LINEAGE:
            if re.search(rx, l):
                if MARK.search(l) and not (PLANT and 'control plant' in l): allowed += 1
                else: hits.append('%s:%d LINEAGE-ONLY %s without a lineage marker | %s' % (f, i + 1, rx, l.strip()[:140]))
print('rekey_check_gate42 | dir %s | %d file(s), %d line(s) | %d forbidden spelling(s), %d lineage-only | %d lineage hit(s) ALLOWED by marker | hex runs masked %d%s' % (
    D, len(files), n_lines, len(FORBID), len(LINEAGE), allowed, masked, (' | PLANTED %r' % PLANT) if PLANT else ''))
for h in hits: print('  ' + h)
print('RESULT %s: %d hit(s)' % ('CLEAN' if not hits else 'HITS', len(hits)))
sys.exit(1 if hits else 0)
