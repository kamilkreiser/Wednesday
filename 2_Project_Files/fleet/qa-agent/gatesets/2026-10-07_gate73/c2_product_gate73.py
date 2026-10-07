#!/usr/bin/env python3
r"""c2_product_gate73.py — THE CHANGES AS SHIPPED, per row, read and DRIVEN. The head is an argument; nothing defaults.

MODES (all: --repo <YOUR clone>)
  static   --pr R --head H        the product diff read against the kit's description, per row:
           1407  S1 ONE line `grep -qx "$full"` -> `grep -qxF "$full"`, nothing else in the script;  S2 the sibling class: every OTHER grep in
                 the head script that reads a VARIABLE as a pattern (INFO, residue);  S3 §5d: a KS-998 WHY comment within 3 lines of the
                 changed line (CONTROL: the same reader finds a KS key near a line that has one).
           1409  S1 the old summary-line regex present at base, ABSENT at head;  S2 `--reporter=json` + `--outputFile.json=` in the spawn;
                 S3 endedNormally refuses error / signal / status not in {0,1};  S4 0 reads of result.stdout / result.stderr (CONTROL: the
                 same grep counts countsFromSpawn > 0);  S5 INFO the named hole: status 1 is also vitest's UNHANDLED-ERROR exit.
           1408  S1 ONE added line `signature: z.string().optional(),` INSIDE `const rejectTransferSchema = z.object({`;  S2 the reject
                 handler still parses the body with rejectTransferSchema first;  S3 the PUBLISHED TransferRejectRequest.signature is
                 `type: string`, NOT nullable, NOT required (so null -> 400 is spec-consistent; a NAMED behaviour change);  S4 §5d comment;
                 S5 INFO the sibling class: every OTHER z.object schema in transfer/src/index.ts, its keys, for the gate to compare with the spec.
           1410  S1 ONE line `.uuid()` added to TransferCustodyRequestSchema.newHolderId;  S2 the YAML diff is ONE line `format: uuid` under
                 components.schemas.TransferCustodyRequest.properties.newHolderId;  S3 the schema is NOT parsed at runtime: 0
                 `TransferCustodyRequestSchema.(safe)parse(` in originate/src (CONTROL: `.parse(` / `.safeParse(` on other schemas > 0);
                 S4 the runtime handler routes/documents.ts byte-identical base == head and carries its own UUID check;  S5 §5d comment.
  labels998 --head H --out DIR    THE GATE'S OWN INSTRUMENT for #1407 (no deps: fixture packages, the same method as the suite):
           L1 the head suite with the head script 8/0 rc 0;  L2 RED-FIRST the head suite with the BASE script (PACKAGE_FORMAT_GATE_SH):
           rc 1, 5/3, the 3 reds are the dotted / bracket label cells, the 5 CONTROLS green;  L3 ARM NOANCHOR `grep -qxF` -> `grep -qF`
           (tamper asserted landed): which cells red — 0 means NO cell pins the anchoring (a named gap);  L4 the label MATRIX, base vs head
           script: red file `src/a<m>b.ts` for m in . [id] + * ? (x) {1} ^ $, pushed EXACT -> `(in this push)`, pushed a LOOKALIKE ->
           `(NOT in this push`; head right on all, base wrong on some (CONTROL); plus the anchoring probe (push `a.ts` vs red `a.tsx`);
           L5 the sibling suite package_format_gate.test.sh with the head script 33/0 and with the base script 33/0 (unchanged);
           L6 the verdict line and exit code identical base vs head on every matrix shape (the label is the only thing that changes).
  drive1435 --wt W --label base|head --out DIR    THE IN-PROCESS DRIVE Wednesday ruled for #1408. Generates
           <W>/Blockchain/Dev/services/transfer/src/__tests__/gate73_ks1435_drive.test.ts = W's OWN transfer.test.ts harness + ONE
           `GATE73` describe of RECORD-ONLY cells (observations to a JSONL file; the verdict is decided HERE, one parser for base and head),
           runs `npx vitest run <that file> -t GATE73` in W's services/transfer, then MOVES the generated file into DIR (W is left as found;
           sha asserted). Cells G1-G11 (see CELLS). W must have deps installed (X1). `--compare BASEDIR HEADDIR` prints the table + verdict.
rc 0 PASS / 1 FAIL / 2 refused."""
import json, os, re, shutil, subprocess, sys, tempfile, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate73 import K, ROWS, BASE, Tally, git, git_bytes, refuse_absent, opt, obj_at, row_arg


def diff_lines(repo, a, b, path):
    out = git(repo, 'diff', '-U0', a, b, '--', path)
    return [l for l in out.split('\n') if l and l[0] in '+-' and not l.startswith(('+++', '---'))]


def why_near(text, needle_line_no, key, span=3):
    L = text.split('\n'); lo = max(0, needle_line_no - 1 - span); hi = min(len(L), needle_line_no + span)
    return any(key in l for l in L[lo:hi])


def line_no(text, sub):
    hits = [i + 1 for i, l in enumerate(text.split('\n')) if sub in l]
    return hits


def static(repo, r, head):
    t = Tally(); R = ROWS[r]
    if r == '1407':
        p = 'systemTest/scripts/check-package-format.sh'; dl = diff_lines(repo, BASE, head, p)
        t.check('S1', dl == ['-        if [ "$MODE" != "all" ] && printf \'%s\\n\' "$changed_paths" | grep -qx "$full"; then',
                             '+        if [ "$MODE" != "all" ] && printf \'%s\\n\' "$changed_paths" | grep -qxF "$full"; then'],
                'the script diff is exactly ONE line -x -> -xF: %d +/- line(s)' % len(dl))
        ht = git_bytes(repo, head, p).decode()
        sib = [(i + 1, l.strip()) for i, l in enumerate(ht.split('\n')) if re.search(r'\bgrep\b[^|]*"[^"]*\$', l) and '-qxF' not in l and not l.lstrip().startswith('#')]
        t.info('S2', 'sibling greps reading a VARIABLE as a regex pattern at the head (residue, not this PR\'s): %s' % sib)
        n = line_no(ht, 'grep -qxF "$full"')
        hit = bool(n) and why_near(ht, n[0], 'KS-998'); ctl_n = line_no(ht, 'KS-1063'); ctl = bool(ctl_n) and why_near(ht, ctl_n[0], 'KS-1063')
        t.check('S3', hit, '§5d: a `KS-998` WHY comment within 3 lines of the changed line :%s: %s | CONTROL the same reader finds KS-1063 near :%s: %s%s' % (
            n[:1], hit, ctl_n[:1], ctl, '' if hit else ' => FINDING (§5d MUST: "Every changed line carries a comment saying WHY it changed and the Linear ticket number")'))
    elif r == '1409':
        p = 'systemTest/performance/tests/unit/utils/unitSuiteSlotIndependence.test.ts'
        bt, ht = git_bytes(repo, BASE, p).decode(), git_bytes(repo, head, p).decode()
        old = r'Tests\s+(?:(\d+) failed \| )?(\d+) passed'
        t.check('S1', old in bt and old not in ht, 'the summary-line regex at base %s, at head %s' % (old in bt, old not in ht and 'ABSENT' or 'PRESENT'))
        t.check('S2', "'--reporter=json'" in ht and '--outputFile.json=' in ht, '--reporter=json %s, --outputFile.json= %s' % ("'--reporter=json'" in ht, '--outputFile.json=' in ht))
        m = re.search(r'function endedNormally\(spawn: ChildSpawn\): boolean \{\s*return (.*?);\s*\}', ht, re.S)
        body = m.group(1) if m else ''
        t.check('S3', body == 'spawn.error === undefined && spawn.signal === null && (spawn.status === 0 || spawn.status === 1)', 'endedNormally: %r' % body)
        rs = len(re.findall(r'result\.(stdout|stderr)', ht)); cs = len(re.findall(r'countsFromSpawn', ht))
        t.check('S4', rs == 0 and cs > 0, 'result.stdout|stderr reads %d | CONTROL countsFromSpawn occurrences %d' % (rs, cs))
        t.info('S5', 'NAMED HOLE (the author\'s follow-up, not a regression): status 1 is also vitest\'s UNHANDLED-ERROR exit; a child that died that way while writing numFailedTests 0 is accepted')
    elif r == '1408':
        p = 'Blockchain/Dev/services/transfer/src/index.ts'; dl = diff_lines(repo, BASE, head, p); ht = git_bytes(repo, head, p).decode()
        m = re.search(r'const rejectTransferSchema = z\.object\(\{(.*?)\n\}\);', ht, re.S)
        t.check('S1', dl == ['+  signature: z.string().optional(),'] and m is not None and 'signature: z.string().optional(),' in m.group(1),
                'ONE added line inside rejectTransferSchema: %s | schema keys %s' % (dl, re.findall(r'^\s+(\w+):', m.group(1), re.M) if m else None))
        hm = re.search(r"app\.post\('/api/transfers/:id/reject'.*?\{\s*try \{\s*const data = rejectTransferSchema\.parse\(req\.body\);", ht, re.S)
        zm = re.search(r"app\.post\('/api/transfers/:id/reject'.*?error instanceof z\.ZodError\) \{\s*return res\.status\(400\)", ht, re.S)
        t.check('S2', hm is not None and zm is not None, 'the reject handler parses with rejectTransferSchema FIRST %s; a ZodError answers 400 %s' % (hm is not None, zm is not None))
        y = git_bytes(repo, head, 'Blockchain/Dev/docs/openapi/secuura-api.yaml').decode()
        sm = re.search(r'\n    TransferRejectRequest:\n(.*?)\n    \S', y, re.S); blk = sm.group(1) if sm else ''
        sig = re.search(r'\n        signature:\n((?:          .*\n?)+)', blk)
        req = re.search(r'\n      required:\n((?:        - .*\n?)+)', blk)
        sigtxt = sig.group(1) if sig else ''
        t.check('S3', 'type: string' in sigtxt and 'nullable' not in sigtxt and (req is None or 'signature' not in req.group(1)),
                'published TransferRejectRequest.signature: %r; required %s => a string, OPTIONAL, NOT nullable: null -> 400 at the head is spec-consistent (a NAMED behaviour change: base answered 200)' % (
                    sigtxt.strip().split('\n')[:2], re.findall(r'- (\w+)', req.group(1)) if req else None))
        n = line_no(ht, 'signature: z.string().optional(),')
        hit = bool(n) and why_near(ht, n[0], 'KS-1435'); ctl_n = [i + 1 for i, l in enumerate(ht.split('\n')) if re.search(r'KS-\d+', l)]
        t.check('S4', hit, '§5d: a `KS-1435` WHY comment within 3 lines of :%s: %s | CONTROL the file carries %d KS-keyed line(s), so the reader can see one%s' % (
            n[:1], hit, len(ctl_n), '' if hit else ' => FINDING (§5d MUST)'))
        sch = {mm.group(1): re.findall(r'^  (\w+):', mm.group(2), re.M) for mm in re.finditer(r'const (\w+Schema) = z\.object\(\{(.*?)\n\}\)', ht, re.S)}
        t.info('S5', 'sibling class (KS-1435 is a narrowing; no other schema audited by the author): %d z.object schemas in transfer/src/index.ts: %s' % (len(sch), sch))
        # S6 THE CLASS, measured: every transfer body schema vs its PUBLISHED request schema. A published property the zod schema does
        # not declare is the KS-518 / KS-1435 class (zod strips it, so a wrong-typed value is DISCARDED, not refused). CONTROL: the
        # same comparison at the BASE finds `signature` missing from rejectTransferSchema (the instance this PR closes).
        def props(ytext, name):
            mm = re.search(r'\n    %s:\n(.*?)\n    \S' % name, ytext, re.S)
            pm = re.search(r'\n      properties:\n((?:        .*\n?)+)', mm.group(1) + '\n') if mm else None
            return re.findall(r'^        (\w+):', pm.group(1), re.M) if pm else None
        MAP = {'initiateTransferSchema': 'TransferInitiateRequest', 'approveTransferSchema': 'TransferApproveRequest', 'rejectTransferSchema': 'TransferRejectRequest'}
        bt = git_bytes(repo, BASE, p).decode(); by = git_bytes(repo, BASE, 'Blockchain/Dev/docs/openapi/secuura-api.yaml').decode()
        bsch = {mm.group(1): re.findall(r'^  (\w+):', mm.group(2), re.M) for mm in re.finditer(r'const (\w+Schema) = z\.object\(\{(.*?)\n\}\)', bt, re.S)}
        gap_h = {z: sorted(set(props(y, s) or []) - set(sch.get(z, []))) for z, s in MAP.items()}
        gap_b = {z: sorted(set(props(by, s) or []) - set(bsch.get(z, []))) for z, s in MAP.items()}
        read_ok = all(props(y, s) for s in MAP.values())
        t.check('S6', read_ok and 'signature' in gap_b['rejectTransferSchema'] and 'signature' not in gap_h['rejectTransferSchema'],
                'CLASS AUDIT published-but-undeclared properties at the HEAD %s | CONTROL at the BASE %s (rejectTransferSchema.signature present at base, closed at head)%s' % (
                    gap_h, gap_b, ' => SIBLING INSTANCES REMAIN (residue for KS-1435\'s register, not this PR\'s blocker)' if any(gap_h.values()) else ''))
    elif r == '1410':
        p = 'Blockchain/Dev/services/originate/src/originate.openapi.ts'; dl = diff_lines(repo, BASE, head, p)
        t.check('S1', len(dl) == 2 and dl[0].replace('z.string().optional()', 'z.string().uuid().optional()').replace('-', '+', 1) == dl[1] and 'newHolderId' in dl[0],
                'ONE line, `.uuid()` inserted on newHolderId: %s' % [x[:110] for x in dl])
        yl = diff_lines(repo, BASE, head, 'Blockchain/Dev/docs/openapi/secuura-api.yaml')
        y = git_bytes(repo, head, 'Blockchain/Dev/docs/openapi/secuura-api.yaml').decode()
        sm = re.search(r'\n    TransferCustodyRequest:\n(.*?)\n    \S', y, re.S)
        nh = re.search(r'\n        newHolderId:\n((?:          .*\n?)+)', sm.group(1) if sm else '')
        t.check('S2', yl == ['+          format: uuid'] and nh is not None and 'format: uuid' in nh.group(1),
                'YAML diff %s; under TransferCustodyRequest.properties.newHolderId: %s' % (yl, nh.group(1).strip().split('\n') if nh else None))
        g = lambda pat: git(repo, 'grep', '-n', '-E', pat, head, '--', 'Blockchain/Dev/services/originate/src', check=False)[1]
        uses = [l for l in g(r'TransferCustodyRequestSchema').split('\n') if l]
        parsed = [l for l in g(r'TransferCustodyRequestSchema\.(safe)?[pP]arse').split('\n') if l]
        ctl = [l for l in g(r'\.(safeParse|parse)\(').split('\n') if l]
        t.check('S3', not parsed and len(ctl) > 0, 'TransferCustodyRequestSchema references %d (%s) | runtime (safe)parse of it %d | CONTROL `.parse(`/`.safeParse(` elsewhere in originate/src %d' % (
            len(uses), [u.split(':')[1] + ':' + u.split(':')[2] for u in uses], len(parsed), len(ctl)))
        dp = 'Blockchain/Dev/services/originate/src/routes/documents.ts'
        same = obj_at(repo, BASE, dp) == obj_at(repo, head, dp); dt = git_bytes(repo, head, dp).decode()
        t.check('S4', same and 'newHolderId must be a valid UUID' in dt, 'the runtime handler %s byte-identical base == head %s; carries its own UUID refusal %s => the spec now states what the handler ALREADY enforced (no runtime branch moves)' % (
            os.path.basename(dp), same, 'newHolderId must be a valid UUID' in dt))
        ht = git_bytes(repo, head, p).decode(); n = line_no(ht, 'newHolderId: z.string().uuid()')
        hit = bool(n) and why_near(ht, n[0], 'KS-591'); ctl_n = line_no(ht, 'KS-665')
        t.check('S5', hit, '§5d: a `KS-591` WHY comment within 3 lines of :%s: %s | CONTROL the same reader finds KS-665 near :%s: %s%s' % (
            n[:1], hit, ctl_n[:1], bool(ctl_n) and why_near(ht, ctl_n[0], 'KS-665'), '' if hit else ' => FINDING (§5d MUST)'))
    return t.end()


# ---------------- labels998 ----------------
SUITE = 'systemTest/__tests__/ks998_format_gate_push_label_is_literal.test.sh'
SIB = 'systemTest/__tests__/package_format_gate.test.sh'
SCRIPT = 'systemTest/scripts/check-package-format.sh'


def sh(cmd, env=None, inp=None, cwd=None):
    p = subprocess.run(cmd, capture_output=True, env=dict(os.environ, **(env or {})), input=inp, cwd=cwd)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def suite_counts(text, name):
    m = re.search(r'^%s: (\d+) passed, (\d+) failed\s*$' % re.escape(name), text, re.M)
    return (int(m.group(1)), int(m.group(2))) if m else None


def mk_fixture(root, script_bytes, pkgs):
    os.makedirs(os.path.join(root, 'systemTest', 'scripts'))
    g = os.path.join(root, 'systemTest', 'scripts', 'check-package-format.sh'); open(g, 'wb').write(script_bytes)
    for name, warn in pkgs:
        d = os.path.join(root, 'systemTest', name); os.makedirs(os.path.join(d, 'node_modules', '.bin'))
        json.dump({'name': 'fixture-' + name, 'version': '0.0.0', 'scripts': {'format:check': "echo '[warn] %s'; exit 1" % warn}}, open(os.path.join(d, 'package.json'), 'w'))
        pp = os.path.join(d, 'node_modules', '.bin', 'prettier'); open(pp, 'w').write('#!/bin/sh\nexit 0\n'); os.chmod(pp, 0o755)
    return g


METAS = [('dot', '.', 'X'), ('bracket', '[id]', 'i'), ('plus', '+', 'aa'), ('star', '*', ''), ('q', '?', ''), ('paren', '(x)', 'x'),
         ('brace', '{1}', ''), ('caret', '^', ''), ('dollar', '$', '')]


def labels998(repo, head, out):
    t = Tally(); os.makedirs(out, exist_ok=True); tmp = os.path.join(out, 'tmp'); os.makedirs(tmp, exist_ok=True)
    hs, bs = git_bytes(repo, head, SCRIPT), git_bytes(repo, BASE, SCRIPT)
    for nm, b in (('suite_head.test.sh', git_bytes(repo, head, SUITE)), ('sib_head.test.sh', git_bytes(repo, head, SIB)),
                  ('script_head.sh', hs), ('script_base.sh', bs)):
        open(os.path.join(out, nm), 'wb').write(b)
    noanchor = hs.replace(b'grep -qxF "$full"', b'grep -qF "$full"', 1)
    open(os.path.join(out, 'script_ARM_noanchor.sh'), 'wb').write(noanchor)
    landed = hs.count(b'grep -qxF "$full"') == 1 and noanchor.count(b'grep -qF "$full"') == 1 and hashlib.sha256(noanchor).digest() != hashlib.sha256(hs).digest()
    rcn, _, _ = sh(['bash', '-n', os.path.join(out, 'script_ARM_noanchor.sh')])
    t.check('L0', landed and rcn == 0, 'ARM NOANCHOR tamper LANDED (anchor count 1 -> 1 replaced, sha changed) %s; bash -n rc %d' % (landed, rcn))
    def run_suite(script, name, suite='suite_head.test.sh', sname='ks998_format_gate_push_label_is_literal'):
        rc, o, e = sh(['bash', os.path.join(out, suite)], env={'PACKAGE_FORMAT_GATE_SH': os.path.join(out, script), 'TMPDIR': tmp})
        open(os.path.join(out, name + '.out'), 'w').write(o + '\n--- stderr\n' + e)
        fails = [l[5:].strip() for l in o.split('\n') if l.startswith('FAIL ')]
        return rc, suite_counts(o, sname), fails
    rc, c, f = run_suite('script_head.sh', 'L1_head')
    t.check('L1', rc == 0 and c == (8, 0), 'head suite x head script: rc %d %s' % (rc, c))
    rc, c, f = run_suite('script_base.sh', 'L2_redfirst_base')
    ctl_red = [x for x in f if x.startswith('CONTROL')]
    t.check('L2', rc == 1 and c == (5, 3) and not ctl_red and len(f) == 3 and sum('a.b.ts' in x for x in f) == 1 and sum('[id].ts' in x for x in f) == 1,
            'RED-FIRST head suite x BASE script: rc %d %s; reds %s; CONTROL cells red %d' % (rc, c, f, len(ctl_red)))
    rc, c, f = run_suite('script_ARM_noanchor.sh', 'L3_arm_noanchor')
    t.check('L3', c is not None and c[0] + c[1] == 8, 'ARM NOANCHOR (-qF, literal but UNANCHORED): rc %d %s reds %s%s' % (
        rc, c, f, ' => NO cell pins the -x anchoring (a NAMED GAP in the suite, not a defect in the product line)' if c == (8, 0) else ''))
    # L4 matrix + L6 verdict invariance
    rows = []; head_ok = True; base_wrong = 0; noanchor_caught = 0; verdict_same = True
    for tag, m, look in METAS + [('anchor', None, None)]:
        if tag == 'anchor': red, lk = 'src/a.ts', 'src/a.tsx'
        else: red, lk = 'src/a%sb.ts' % m, 'src/a%sb.ts' % look
        for which, script in (('base', bs), ('head', hs), ('noanchor', noanchor)):
            for case, pushed, want in (('exact', red, '(in this push)'), ('lookalike', lk, '(NOT in this push')):
                if tag == 'anchor' and case == 'exact': continue
                if case == 'lookalike' and pushed == red: continue
                root = tempfile.mkdtemp(prefix='l4.', dir=tmp)
                g = mk_fixture(root, script, [('p', red)])
                rc, o, e = sh(['bash', g], inp=('systemTest/p/%s\n' % pushed).encode(), env={'TMPDIR': tmp})
                full = 'systemTest/p/%s' % red
                lab = [l for l in e.split('\n') if full + '   (' in l]
                got = 'in' if any('(in this push)' in l for l in lab) else ('NOT' if any('(NOT in this push' in l for l in lab) else 'NONE')
                right = (got == 'in') == (want == '(in this push)') and got != 'NONE'
                verdict = [l for l in (o + e).split('\n') if 'package(s) checked' in l]
                rows.append((tag, which, case, got, right, rc, verdict))
                if which == 'head': head_ok &= right
                elif which == 'base' and not right: base_wrong += 1
                elif which == 'noanchor' and tag == 'anchor' and not right: noanchor_caught += 1
    for tag in [x[0] for x in METAS] + ['anchor']:
        b = [r for r in rows if r[0] == tag and r[1] == 'base']; h = [r for r in rows if r[0] == tag and r[1] == 'head']
        verdict_same &= [(r[5], r[6]) for r in b] == [(r[5], r[6]) for r in h]
    open(os.path.join(out, 'L4_matrix.json'), 'w').write(json.dumps(rows, indent=0))
    for r_ in rows: print('   L4 %-8s %-4s %-9s label=%-4s right=%s rc=%d %s' % (r_[0], r_[1], r_[2], r_[3], r_[4], r_[5], r_[6]))
    t.check('L4', head_ok and base_wrong > 0 and noanchor_caught == 1, 'LABEL MATRIX: head right on all %d shapes: %s | CONTROL base wrong on %d shape(s) | CONTROL the anchoring probe (red src/a.ts, push src/a.tsx) catches the NOANCHOR arm: %s' % (
        len([r for r in rows if r[1] == 'head']), head_ok, base_wrong, noanchor_caught == 1))
    t.check('L6', verdict_same, 'the verdict line and the exit code are identical base vs head on every shape (only the label moves): %s' % verdict_same)
    for which in ('head', 'base'):
        rc, c, f = run_suite('script_%s.sh' % which, 'L5_sib_%s' % which, suite='sib_head.test.sh', sname='package_format_gate')
        t.check('L5-%s' % which, rc == 0 and c == (33, 0), 'sibling package_format_gate.test.sh x %s script: rc %d %s' % (which, rc, c))
    rc, c, f = run_suite('script_head.sh', 'L1_head_rerun')
    t.check('L7', rc == 0 and c == (8, 0), 'determinism: a re-run agrees: rc %d %s' % (rc, c))
    return t.end()


# ---------------- drive1435 ----------------
CELLS = [
    ('G1', 'object signature', {'signature': {}}, 400, 200),
    ('G2', 'numeric signature', {'signature': 42}, 400, 200),
    ('G3', 'array signature', {'signature': []}, 400, 200),
    ('G4', 'boolean signature', {'signature': True}, 400, 200),
    ('G5', 'null signature (spec: string, not nullable)', {'signature': None}, 400, 200),
    ('G6', 'string signature', {'signature': '0xabc123'}, 200, 200),
    ('G7', 'absent signature', {}, 200, 200),
    ('G8', 'empty-string signature', {'signature': ''}, 200, 200),
    ('G9', 'absent signature + an unknown key (stripped, unchanged)', {'foo': {'x': 1}}, 200, 200),
    ('G10', 'object signature AND a non-uuid rejectorId (already 400)', {'signature': {}, '_rejectorId': 'not-a-uuid'}, 400, 400),
]
GEN_NAME = 'gate73_ks1435_drive.test.ts'


def gen_block():
    cells = json.dumps([[c[0], c[1], c[2]] for c in CELLS])
    return """
  // ---- GATE73 (QA gate, generated in the gate's OWN worktree; never committed) ----
  describe('GATE73 KS-1435 reject signature drive', () => {
    const GATE73_CELLS: Array<[string, string, Record<string, unknown>]> = %s;
    for (const [id, name, extra] of GATE73_CELLS) {
      it(`GATE73 ${id} ${name}`, async () => {
        const fs = await import('node:fs');
        const createRes = await httpReq('POST', '/api/transfers', validTransferBody());
        const tid = createRes.data?.data?.id;
        const body: Record<string, unknown> = { rejectorId: uuid(), rejectorRole: 'new_owner', reason: 'gate73 ' + id };
        for (const [k, v] of Object.entries(extra)) {
          if (k === '_rejectorId') body.rejectorId = v; else body[k] = v;
        }
        const res = await httpReq('POST', `/api/transfers/${tid}/reject`, body);
        const after = await httpReq('GET', `/api/transfers/${tid}`);
        fs.appendFileSync(process.env.GATE73_OUT as string, JSON.stringify({
          id, created: createRes.status, status: res.status, code: res.data?.error?.code ?? null,
          paths: (res.data?.error?.details ?? []).map((d: any) => (d.path ?? []).join('.')),
          after: after.data?.data?.status ?? null, sent: Object.keys(body).sort(),
        }) + '\\n');
        expect(typeof res.status).toBe('number');
      });
    }
  });
""" % cells


def drive1435(wt, label, out):
    os.makedirs(out, exist_ok=True)
    tdir = os.path.join(wt, 'Blockchain/Dev/services/transfer/src/__tests__'); src = os.path.join(tdir, 'transfer.test.ts'); gen = os.path.join(tdir, GEN_NAME)
    if os.path.exists(gen): print('REFUSED: %s already exists (a previous run did not clean up?)' % gen); return 2
    txt = open(src, encoding='utf-8').read(); L = txt.rstrip('\n').split('\n')
    if L[-1] != '});' or txt.count("describe('Transfer Service — HTTP API'") != 1:
        print('REFUSED: the harness shape is not as drafted (last line %r, HTTP describe x%d)' % (L[-1], txt.count("describe('Transfer Service — HTTP API'"))); return 2
    g = '\n'.join(L[:-1]) + gen_block() + '});\n'
    open(gen, 'w', encoding='utf-8').write(g)
    landed = open(gen, encoding='utf-8').read().count("describe('GATE73 KS-1435 reject signature drive'") == 1
    jl = os.path.join(out, 'drive_%s.jsonl' % label); open(jl, 'w').close()
    tmp = os.path.join(out, 'tmp'); os.makedirs(tmp, exist_ok=True)
    rc, o, e = sh(['npx', '--no-install', 'vitest', 'run', 'src/__tests__/' + GEN_NAME, '-t', 'GATE73'],
                  env={'GATE73_OUT': jl, 'TMPDIR': tmp, 'CI': '1'}, cwd=os.path.join(wt, 'Blockchain/Dev/services/transfer'))
    open(os.path.join(out, 'drive_%s.vitest.out' % label), 'w').write(o + '\n--- stderr\n' + e + '\nrc %d\n' % rc)
    shutil.move(gen, os.path.join(out, 'drive_%s.%s' % (label, GEN_NAME)))
    gone = not os.path.exists(gen)
    recs = [json.loads(l) for l in open(jl) if l.strip()]
    print('DRIVE %s: generated file landed %s; vitest rc %d; %d/%d cells recorded; generated file moved out of the worktree %s' % (label, landed, rc, len(recs), len(CELLS), gone))
    return 0 if landed and gone and len(recs) == len(CELLS) else 1


def compare1435(bdir, hdir):
    t = Tally()
    B = {r['id']: r for r in map(json.loads, filter(str.strip, open(os.path.join(bdir, 'drive_base.jsonl'))))}
    H = {r['id']: r for r in map(json.loads, filter(str.strip, open(os.path.join(hdir, 'drive_head.jsonl'))))}
    t.check('G0', len(B) == len(H) == len(CELLS), 'cells recorded base %d head %d of %d (a 0 is a LOAD FAILURE, never a pass)' % (len(B), len(H), len(CELLS)))
    for cid, name, extra, want_h, want_b in CELLS:
        b, h = B.get(cid, {}), H.get(cid, {})
        ok = b.get('status') == want_b and h.get('status') == want_h
        if want_h == 400 and want_b == 200:
            ok &= h.get('after') == 'pending_approval' and b.get('after') == 'rejected' and ('signature' in h.get('paths', []))
        elif want_h == 200:
            ok &= h.get('after') == 'rejected' == b.get('after')
        t.check(cid, ok, '%-52s base %s/%s -> head %s/%s (want base %d, head %d)%s' % (
            name, b.get('status'), b.get('after'), h.get('status'), h.get('after'), want_b, want_h,
            ' | head 400 names %s' % h.get('paths') if h.get('status') == 400 else ''))
    return t.end()


def main():
    A = sys.argv[1:]; mode = A[0] if A else ''
    if mode == 'compare1435': return compare1435(opt(A, '--base-dir'), opt(A, '--head-dir'))
    if mode == 'drive1435':
        wt, lab, out = opt(A, '--wt'), opt(A, '--label'), opt(A, '--out')
        if not (wt and lab in ('base', 'head') and out): print(__doc__); return 2
        return drive1435(wt, lab, out)
    repo = opt(A, '--repo')
    if not repo: print(__doc__); return 2
    if mode == 'static':
        r = row_arg(); h = opt(A, '--head'); return refuse_absent(repo, [('--head', h)]) or static(repo, r, h)
    if mode == 'labels998':
        h, out = opt(A, '--head'), opt(A, '--out')
        if not out: print('REFUSED: --out DIR required'); return 2
        return refuse_absent(repo, [('--head', h)]) or labels998(repo, h, out)
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
