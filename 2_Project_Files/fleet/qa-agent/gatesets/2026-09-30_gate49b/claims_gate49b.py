#!/usr/bin/env python3
"""claims_gate49b.py — the drafter's READ of the CLIENT-FACING TEXT in this batch (the part a client human reads), for the gate to rule LINE BY
LINE. A PREDICTION, never evidence; it judges no truth. Reads mail_gate49b_ready.md (the capture), gh_read_1.json (the PR bodies), pins, and the
scratch clone (<scratchpad>/g49b_sp/clone). Writes drafts_gate49b.md.
  C1 RULING VERBATIM: Kam's card (the capture's `decision_queue.sh show` block): option [a]'s label and its detail must each appear in #1357's PR
     body VERBATIM after normalising only whitespace and blockquote `> ` markers (the body joins them with " — "). CONTROL: the same test on a
     copy of the body with ONE word of the detail changed ("stopped" -> "restarted") must FAIL.
  C2 DRAFTS: every DRAFTED ticket comment in the three READYs, extracted verbatim — #1357's KS-1054 draft, #1359's KS-1054 draft, #1358's
     KS-1395 / KS-1387 / KS-1380 drafts — split into numbered sentences D-<ticket>-<pr>-<n>. Each sentence carries the drafter's LEXICAL tag:
     INSTRUMENT-NAMED (it names a sha, an rc, a command, a file:line, a count with its unit, a runner, or says measured / unmeasured / not
     covered) or NO-INSTRUMENT-WORD (the gate must find its instrument or rule it unmeasured). The tag is a word match, NOT a ruling.
     CONTROL: the extractor must find >= 1 sentence in every draft, and a draft-free text yields 0.
  C3 ANCHORS: every `<script>.sh:<line>` cited in the drafts, the PR bodies or the ruling card is resolved at develop, at the owning PR's head
     and at END: the line's text printed at each, so the gate can say whether each citation still points at what it names.
     CONTROL: deploy.sh at develop has >= 800 lines (the reader reads a real file).
  C4 BODY NUMBERS: each PR body's per-file "+a/−d" claims compared with the pinned numstat (e.g. `deploy.sh` (100755, +2/−2)).
rc 0 CLAIMS READ (every control fired and C1 holds) / rc 1. G49B_DRAFTS_OUT (controls): write the table elsewhere. Usage: claims_gate49b.py <scratchpad> [--prbody-1357 <file>]"""
import json, os, re, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
P = json.load(open(os.path.join(G, 'pins_gate49b.json'), encoding='utf-8')); GH = json.load(open(os.path.join(G, 'gh_read_1.json'), encoding='utf-8'))
CAP = open(os.path.join(G, 'mail_gate49b_ready.md'), encoding='utf-8').read(); CL = os.path.join(SP, 'g49b_sp', 'clone')
def git(*a): return subprocess.run(['git', '-C', CL] + list(a), capture_output=True, text=True).stdout
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
bad = []; out = ['# gate49b DRAFTS — every client-facing drafted comment, sentence by sentence (claims_gate49b.py, %s)' % now, '',
                 'Source: the READYs VERBATIM in mail_gate49b_ready.md. Tag = the drafter\'s LEXICAL read (a word match), never a ruling: the gate rules each sentence TRUE (with its instrument) / FALSE / UNMEASURED, and each draft POST AS-IS / AMENDED / DO NOT POST.', '']
print('claims_gate49b %s | develop %s | END %s' % (now, P['develop'][:12], P['end_tree'][:12]))
# ---- C1 ----
cb = re.search(r"## KAM'S RULING CARD .*?```\n(.*?)```", CAP, re.S); card = cb.group(1) if cb else ''
m = re.search(r'\[a\]\s+(.*?)\n\s+detail:\s+(.*?)\n\s+\[b\]', card, re.S)
lab, det = (m.group(1).strip(), re.sub(r'\s+', ' ', m.group(2)).strip()) if m else ('', '')
def norm(t): return re.sub(r'\s+', ' ', re.sub(r'(?m)^>\s?', '', t)).strip()
pb = open(A[A.index('--prbody-1357') + 1]).read() if '--prbody-1357' in A else GH['prs']['1357']['body']
nb = norm(pb); c1 = bool(lab) and bool(det) and lab in nb and det in nb
ctl = det.replace('stopped', 'restarted'); c1c = ctl != det and ctl not in norm(pb)
print('C1 RULING VERBATIM: card option [a] label %r (%d chars) in #1357 body: %s | detail (%d chars) in body: %s | joined as "[a] <label> — <detail>": %s' % (
    lab, len(lab), lab in nb, len(det), det in nb, ('[a] %s — %s' % (lab, det)) in nb))
print('C1 CONTROL one word changed in the detail ("stopped" -> "restarted") is found: %s (must be False)' % (not c1c))
if not c1: bad.append('C1: the ruling (a) is not verbatim in #1357\'s body')
if not c1c: bad.append('C1 control did not fire')
out += ['## C1 — Kam\'s ruling (a) in #1357\'s body', '', '- label: `%s` — present verbatim: %s' % (lab, lab in nb), '- detail: `%s` — present verbatim: %s' % (det, det in nb), '']
# ---- C2 ----
def ready(n):
    mm = re.search(r'## CLAIM \(the READY for #%s,.*?\n```\n(.*?)\n```\n' % n, CAP, re.S); return mm.group(1) if mm else ''
def drafts(n, t):
    d = {}
    if n in ('1357', '1359'):
        mm = re.search(r'## DRAFTED TICKET COMMENT.*?\n((?:>.*\n?)+)', t)
        if mm: d['KS-1054'] = '\n'.join(re.sub(r'^>\s?', '', l) for l in mm.group(1).splitlines())
    else:
        for mm in re.finditer(r'--- DRAFT for (KS-\d+)[^\n]*---\n(.*?)(?=\n--- DRAFT for |\n== WHAT I HAVE NOT DONE|\Z)', t, re.S): d[mm.group(1)] = mm.group(2).strip()
    return d
IRX = re.compile(r'\b[0-9a-f]{7,40}\b|\brc \d|`[^`]+`|\b\w[\w.-]*\.(?:sh|ts|mjs|json|yml|py):\d+|\b(?:measured|unmeasured|not measured|not covered|Not covered|Measured)\b|'
                 r'python:3\.12-slim|macOS|npm run|docker|tsc|grep|cmp|\b\d+ (?:passed|failed|locks?|entries|services|of \d+)|\bline \d+|\bat (?:develop|\d)', re.I)
def sents(t):
    t = re.sub(r'\s*\n\s*', ' ', t.strip())
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+(?=[A-Z0-9"`(])', t) if s.strip()]
AU = K.get('post_merge_audit'); DR = K['order'] + ([AU['pr']] if AU else [])   # #1358's drafts are the POST-MERGE AUDIT's (merged 07:28:02Z, unposted)
PRX = lambda n: K['prs'][n] if n in K['prs'] else AU
tot = 0; noi = 0
for n in DR:
    r = ready(n); ds = drafts(n, r)
    if not r: bad.append('C2: no READY text for #%s in the capture' % n); continue
    want = sorted(PRX(n)['drafted_comments'])
    if sorted(ds) != want: bad.append('C2: #%s drafts found %s, kit expects %s' % (n, sorted(ds), want))
    for tk, body in ds.items():
        ss = sents(body)
        if not ss: bad.append('C2: the %s draft in #%s has 0 sentences' % (tk, n))
        out += ['## D-%s-%s — %s\'s drafted %s comment (%d sentences; from the READY for #%s)' % (tk, n, PRX(n)['seat'], tk, len(ss), n), '', '| id | sentence (verbatim) | drafter\'s lexical tag | gate: TRUE / FALSE / UNMEASURED + instrument |', '|---|---|---|---|']
        for i, s in enumerate(ss, 1):
            tag = 'INSTRUMENT-NAMED' if IRX.search(s) else 'NO-INSTRUMENT-WORD'; noi += tag.startswith('NO'); tot += 1
            out.append('| D-%s-%s-%d | %s | %s | |' % (tk, n, i, s.replace('|', '\\|'), tag))
        out += ['', '**Verdict for this draft (the gate):** POST AS-IS / AMENDED (give the amended text) / DO NOT POST — and whether it repeats or contradicts %s.' % (
            PRX(n)['drafted_comments'][tk].get('must_not_contradict') or 'any other comment on the ticket'), '']
        print('C2 D-%s-%s: %d sentence(s), %d with no instrument word | first: %s' % (tk, n, len(ss), sum(1 for s in ss if not IRX.search(s)), ss[0][:90] if ss else ''))
z = sum(len(sents(b)) for b in drafts('1358', 'no drafts here').values())
print('C2 CONTROL a draft-free text yields %d sentence(s) (must be 0) | TOTAL %d sentence(s) across %d draft(s), %d NO-INSTRUMENT-WORD' % (z, tot, sum(len(drafts(n, ready(n))) for n in DR), noi))
if z: bad.append('C2 control fired on a draft-free text')
# ---- C3 ----
FMAP = {'deploy.sh': 'Blockchain/Dev/deployment/azure/deploy.sh', 'deploy-all.sh': 'Blockchain/Dev/deployment/azure/deploy-all.sh',
        'check-startup-migrations.sh': 'Blockchain/Dev/deployment/azure/check-startup-migrations.sh', 'run-migrations.sh': None}
own = {p: n for n in K['order'] for p in K['prs'][n]['files']}
srcs = [('READY #%s' % n, ready(n)) for n in DR] + [('PR body #%s' % n, GH['prs'][n]['body']) for n in K['order']] + [('ruling card', card)]
cites = sorted(set((f, int(l)) for _, t in srcs for f, l in re.findall(r'\b([\w-]+\.sh):(\d+)', t)))
out += ['## C3 — every `<script>.sh:<line>` cited, resolved at develop / the owning PR head / END', '', '| cite | cited in | develop | PR head | END |', '|---|---|---|---|---|']
dl = len(git('show', '%s:%s' % (P['develop'], FMAP['deploy.sh'])).splitlines())
print('C3 CONTROL deploy.sh at develop has %d lines (>= 800: %s)' % (dl, dl >= 800))
if dl < 800: bad.append('C3 control: deploy.sh at develop read %d lines' % dl)
for f, l in cites:
    path = FMAP.get(f); where = sorted(set(lab for lab, t in srcs if re.search(r'\b%s:%d\b' % (re.escape(f), l), t)))
    if not path: print('C3 %s:%d — not resolved (no path mapping; the gate reads it) | cited in %s' % (f, l, where)); out.append('| %s:%d | %s | (unmapped) | | |' % (f, l, ', '.join(where))); continue
    ph = P['prs'][own[path]]['head'] if path in own else None
    def ln(t):
        ls = git('show', '%s:%s' % (t, path)).splitlines(); return ls[l - 1].strip() if 0 < l <= len(ls) else '(beyond EOF: %d lines)' % len(ls)
    a, b, c = ln(P['develop']), (ln(ph) if ph else '(no kit PR touches it)'), ln(P['end_tree'])
    print('C3 %s:%d | cited in %s | develop: %s | PR head: %s | END: %s' % (f, l, where, a[:80], b[:80], c[:80]))
    out.append('| %s:%d | %s | `%s` | `%s` | `%s` |' % (f, l, ', '.join(where), a.replace('|', '\\|')[:110], b.replace('|', '\\|')[:110], c.replace('|', '\\|')[:110]))
out.append('')
# ---- C4 ----
out += ['## C4 — per-file +a/−d claims in the PR bodies vs the pinned numstat', '']
for n in K['order']:
    ns = {x.split('\t')[2]: (int(x.split('\t')[0]), int(x.split('\t')[1])) for x in P['prs'][n]['numstat']}
    for mm in re.finditer(r'`([\w./-]+)`\s*\((?:[^)]*?,\s*)?\+(\d+)/[−-](\d+)\)', GH['prs'][n]['body']):
        f, a_, d_ = mm.group(1), int(mm.group(2)), int(mm.group(3)); full = [p for p in ns if p.endswith('/' + f.split('/')[-1])]
        got = ns[full[0]] if full else None; v = 'MATCH' if got == (a_, d_) else 'DIFFERS'
        print('C4 #%s body claims %s +%d/-%d | numstat %s | %s' % (n, f, a_, d_, ('+%d/-%d' % got) if got else 'n/a', v)); out.append('- #%s `%s`: body +%d/−%d | numstat %s | **%s**' % (n, f, a_, d_, ('+%d/-%d' % got) if got else 'n/a', v))
    for mm in re.finditer(r'the predicate \(\+(\d+)/[−-](\d+)\)|suite \(\+(\d+)\)', GH['prs'][n]['body']): print('C4 #%s body phrase %r (the gate compares it to the numstat: %s)' % (n, mm.group(0), '; '.join('%s +%d/-%d' % (os.path.basename(p), *v) for p, v in ns.items())))
open(os.environ.get('G49B_DRAFTS_OUT') or os.path.join(G, 'drafts_gate49b.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
for b in bad: print('PROBLEM: ' + b)
print('CLAIMS %s: C1 ruling verbatim %s | %d draft sentence(s) (%d NO-INSTRUMENT-WORD) | %d anchor(s) | %d problem(s) -> drafts_gate49b.md' % ('READ' if not bad else 'FAILED', c1, tot, noi, len(cites), len(bad)))
raise SystemExit(1 if bad else 0)
