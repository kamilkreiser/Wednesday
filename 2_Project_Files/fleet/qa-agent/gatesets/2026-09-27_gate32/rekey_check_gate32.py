#!/usr/bin/env python3
r"""rekey_check_gate32.py [<dir>] [--plant <spelling>] — the kit's RE-KEY / NAMESPACE check (STANDING_LINES 2026-09-27: "a namespace check greps EVERY
spelling of the seat token"; "a copied tool is re-keyed for PATHS and ENVIRONMENT-VARIABLE NAMES as well as seat names"; "a re-key checker classifies
prose by SYNTAX, never by how a line reads"). gate32 was copied from gate31, so every spelling gate31's kit used for ITS OWN namespace is listed:
  NEVER allowed anywhere (a live gate31 name would point a gate32 tool at gate31's state): the scratch-clone dir `g31_sp`, its ref namespace `refs/g31/`,
  the control/logprobe workdir prefixes `g31_controls` / `g31_logprobe`, the env-var prefixes `G31_` and `QAB31_`, gate31's pane `QA/Secuura-batch1300`,
  gate31's seat tokens `-b33-`, `s-b33-`, `seatB-33rd`, `b33` as a word, `B 33rd`, `B33`, and gate31's tool names `predict_gate31.py`, `fill_gate31.py`,
  `repin_and_launch_gate31.sh`, `controls_gate31.sh`, `capture_mail_gate31.py`, `gh_read_gate31.py`, `keyscan_gate31.py`, `linear_reads_gate31.py`,
  `tokeq_gate31.js`, `logprobe_gate31`.
  LINEAGE-ONLY (allowed ONLY on a line whose SYNTAX marks it as lineage — one of the markers below on the same line): the bare word `gate31`, gate31's
  PR numbers `#1300`..`#1303`, and its keys KS-1334 / KS-1348 / KS-1349 / KS-1350.
Scans every *.py, *.sh, *.js, *TEMPLATE* file, the filled prompt and launcher and kit.json in <dir> (default: this script's directory), skipping only
superseded_* and .pre-* copies. --plant <spelling> appends `# rekey control plant: <spelling>` to an in-memory copy of predict_gate32.py (nothing on
disk) and must be caught: that is the per-spelling CONTROL. The ONE syntactic exemption: `gate31's <name>` (a possessive naming the predecessor's
file) is read as lineage, never as use. rc 0 clean, rc 1 on any forbidden hit or any lineage-only hit without a marker."""
import os, re, sys
D = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; PLANT = None
if '--plant' in args: i = args.index('--plant'); PLANT = args[i + 1]; args = args[:i] + args[i + 2:]
if args: D = args[0]
FORBID = [r'\bg31_sp\b', r'refs/g31/', r'\bg31_controls', r'\bg31_logprobe', r'\bG31_', r'\bQAB31_', r'QA/Secuura-batch1300\b', r'-b33-', r'\bs-b33-', r'seatB-33rd',
          r'\bb33\b', r'\bB 33rd\b', r'\bB33\b', r'predict_gate31\.py', r'fill_gate31\.py', r'repin_and_launch_gate31\.sh', r'controls_gate31\.sh', r'capture_mail_gate31\.py',
          r'gh_read_gate31\.py', r'keyscan_gate31\.py', r'linear_reads_gate31\.py', r'tokeq_gate31\.js', r'logprobe_gate31']
LINEAGE = [r'\bgate31\b', r'#130[0-3]\b', r'\bKS-13(34|48|49|50)\b']
MARK = re.compile(r"copied from gate31|gate31\\?'s|gate31 lineage|\(gate31|round 31|gate31 declared|gate31 at |in gate31\b|the gate31 kit's|rekey|re-key|FORBID|LINEAGE|MARK")
files = sorted(f for f in os.listdir(D) if (f.endswith(('.py', '.sh', '.js')) or 'TEMPLATE' in f or f.endswith('.prompt.txt') or f == 'kit.json')
               and not f.startswith('superseded_') and '.pre-' not in f)
hits, allowed, n_lines = [], 0, 0
for f in files:
    L = open(os.path.join(D, f), encoding='utf-8', errors='replace').read().split('\n')
    if PLANT and f == 'predict_gate32.py': L = L + ['# rekey control plant: %s' % PLANT]
    for i, l in enumerate(L):
        n_lines += 1
        if f == os.path.basename(__file__) and not (PLANT and 'control plant' in l): continue   # this checker names every spelling by design
        if f.startswith('controls_') and l.rstrip().endswith('rekey_check exempts ONLY a line carrying this marker)') and '# rekey-plant-list' in l: continue   # SYNTAX: the NS controls' plant list
        lx = re.sub(r"gate31\\?'s [\w.]+", "gate31's <lineage>", l)   # SYNTAX: a possessive `gate31's <tool>` names the predecessor, it does not use it
        for rx in FORBID:
            if re.search(rx, lx): hits.append('%s:%d FORBIDDEN %s | %s' % (f, i + 1, rx, l.strip()[:140]))
        for rx in LINEAGE:
            if re.search(rx, l):
                if MARK.search(l) and not (PLANT and 'control plant' in l): allowed += 1
                else: hits.append('%s:%d LINEAGE-ONLY %s without a lineage marker | %s' % (f, i + 1, rx, l.strip()[:140]))
print('rekey_check_gate32 | dir %s | %d file(s), %d line(s) | %d forbidden spelling(s), %d lineage-only | %d lineage hit(s) ALLOWED by marker%s' % (
    D, len(files), n_lines, len(FORBID), len(LINEAGE), allowed, (' | PLANTED %r' % PLANT) if PLANT else ''))
for h in hits: print('  ' + h)
print('RESULT %s: %d hit(s)' % ('CLEAN' if not hits else 'HITS', len(hits)))
sys.exit(1 if hits else 0)
