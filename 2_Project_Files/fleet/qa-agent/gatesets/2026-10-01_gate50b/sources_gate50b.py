#!/usr/bin/env python3
"""sources_gate50b.py — the drafter's READ of the sources behind ITEM 4 (the charge_events ticket text) and ITEM 5 (the KS-1397 comment), in the
SCRATCH clone (git show / cat-file only) and from the seat records (read-only). It rules nothing; it prints what each cited line says, each read beside a
control that fires. No database, no SSH, no Linear (the gate reads Linear itself, X5).
  I0  the saved ticket files: bytes + sha256 prefix == the seat's mail (kit.json item4); the mail's fenced title/description == the files.
  I1  the cited runner lines at develop AND at the cited commit 91a8f6b721bc: run-migrations.sh:118-122 (skip), startup-migrations.ts:137-141 (skip).
  I2  039_rls_fail_closed.sql lists charge_events; its two skip NOTICEs; the commits that touched 039 (the "since KS 458" claim).
  I3  038a exists at develop; its charge_events DDL carries tenant_id; its header names the four tables.
  I4  B 50th's recorded readings: probe_rls.out (before) and the handover's after-table (:90-:136, sha256 printed) — charge_events rls false / 8 rows.
  I5  vocabulary sweep of the ticket text and of the KS-1397 draft (internal words) with a positive control; hyphenated keys per text.
  N1  nginx.conf :24 / :142 at develop; the two sibling configs (demo, production): server_tokens and `proxy_hide_header Server` counts,
      case-insensitive, with server_tokens as the positive control in each.
Options (controls): --title-file F --desc-file F --draft F --tree SHA. Usage: sources_gate50b.py <scratchpad> [options]"""
import json, os, re, subprocess, sys, hashlib, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8')); I4 = K['item4']; KB = K['ks1397']
A = sys.argv[1:]; SP = A[0]; CL = os.path.join(SP, 'g50b_sp', 'clone')
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
P = json.load(open(os.path.join(G, 'pins_gate50b.json'), encoding='utf-8')); DEV = opt('--tree', P['develop'])
def git(*a, check=True):
    r = subprocess.run(['git', '-C', CL] + list(a), capture_output=True, text=True)
    if check and r.returncode: raise SystemExit('REFUSING: git %s rc %d: %s' % (' '.join(a), r.returncode, r.stderr.strip()[:200]))
    return r.stdout
def lines(t, p, a, b): return git('show', '%s:%s' % (t, p)).split('\n')[a - 1:b]
fails = []; n = 0
def chk(tag, ok, msg):
    global n; n += 1; print('%s %s: %s' % ('READ' if ok else 'FAIL', tag, msg))
    if not ok: fails.append(tag)
sha = lambda b: hashlib.sha256(b).hexdigest()
print('sources_gate50b %s | develop %s | clone %s' % (datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), DEV[:12], CL))
tf = opt('--title-file', os.path.join(I4['dir'], I4['title_file'])); df = opt('--desc-file', os.path.join(I4['dir'], I4['description_file']))
tb, db = open(tf, 'rb').read(), open(df, 'rb').read()
mail = open(os.path.join(G, I4['mail']), encoding='utf-8').read()
fences = re.findall(r'```\n(.*?)\n```', mail, re.S)
tin = any(f.strip() == tb.decode().strip() for f in fences); din = any(f.strip() == db.decode().strip() for f in fences)
chk('I0', len(tb) == I4['title_bytes'] and sha(tb).startswith(I4['title_sha256_prefix']) and len(db) == I4['description_bytes'] and sha(db).startswith(I4['description_sha256_prefix']) and tin and din,
    'title %d B sha256 %s (mail: %d B %s) | description %d B sha256 %s (mail: %d B %s) | the mail\'s fenced title == file: %s, description == file: %s (control: %d fenced blocks read)' % (
        len(tb), sha(tb)[:16], I4['title_bytes'], I4['title_sha256_prefix'], len(db), sha(db)[:16], I4['description_bytes'], I4['description_sha256_prefix'], tin, din, len(fences)))
cc = git('rev-parse', I4['cited_commit'] + '^{commit}').strip()
for tag, p, a, b, needle in (('I1a', 'Blockchain/Dev/scripts/run-migrations.sh', 118, 122, "SELECT 1 FROM _secuura_migrations WHERE filename"),
                             ('I1b', 'Blockchain/Dev/services/api-gateway/src/startup-migrations.ts', 137, 141, "SELECT 1 FROM _secuura_migrations WHERE filename = $1 LIMIT 1")):
    ld, lc = lines(DEV, p, a, b), lines(cc, p, a, b)
    ctrl = lines(DEV, p, 1, 3)
    chk(tag, any(needle in x for x in ld) and ld == lc, '%s:%d-%d at develop == at %s: %s | carries %r: %s | lines: %s | CONTROL :1-3 does not carry it: %s' % (
        p.split('/')[-1], a, b, cc[:12], ld == lc, needle[:40], any(needle in x for x in ld), ' / '.join(x.strip() for x in ld)[:230], not any(needle in x for x in ctrl)))
m39 = 'Blockchain/Dev/migrations/039_rls_fail_closed.sql'; t39 = git('show', '%s:%s' % (DEV, m39))
lg = git('log', '--format=%h %ad %s', '--date=short', DEV, '--', m39).strip().split('\n')
pick = git('log', '--format=%h', '-S', "'charge_events'", DEV, '--', m39).split()
chk('I2', "'charge_events'" in t39 and 'table does not exist on this DB' in t39 and 'no tenant_id column' in t39,
    '039 lists charge_events: %s | skip NOTICEs (missing table / no tenant_id): %s / %s | commits touching 039: %s | pickaxe -S charge_events introduced by: %s | CONTROL a table 039 does not list (\'no_such_table_g50b\'): %s' % (
        "'charge_events'" in t39, 'table does not exist on this DB' in t39, 'no tenant_id column' in t39, lg, pick, "'no_such_table_g50b'" in t39))
m38 = 'Blockchain/Dev/migrations/038a_ks1054_core_tables_before_039.sql'; t38 = git('show', '%s:%s' % (DEV, m38))
ddl = re.search(r'CREATE TABLE IF NOT EXISTS charge_events \((.*?)\);', t38, re.S)
chk('I3', ddl is not None and 'tenant_id UUID' in ddl.group(1), '038a at develop blob %s | charge_events DDL has `tenant_id UUID`: %s | header names oauth_apps/svc_webhooks/certifications/charge_events: %s | CONTROL the DDL has no column `g50b_col`: %s' % (
    git('rev-parse', '%s:%s' % (DEV, m38)).strip()[:12], bool(ddl and 'tenant_id UUID' in ddl.group(1)), all(x in t38[:1500] for x in ('oauth_apps', 'svc_webhooks', 'certifications', 'charge_events')), bool(ddl) and 'g50b_col' not in ddl.group(1)))
pr = open(I4['probe'], encoding='utf-8').read(); ho = open(I4['handover'], encoding='utf-8').read().split('\n')
a, b = [int(x) for x in I4['handover_lines'].split('-')]; seg = '\n'.join(ho[a - 1:b])
ce_b = re.search(r'charge_events relrowsecurity=(\w+) relforcerowsecurity=(\w+) policies=(\d+)', pr); rows_b = re.search(r'charge_events: (\d+)', pr)
ce_a = re.search(r'\| charge_events \| (\w+) \| (\d+) \(=\d+\) \| (\d+) \(=(\d+)\) \| (\w+) \| (\w+) \| (\d+) \|', seg)
chk('I4', bool(ce_b and rows_b and ce_a), 'probe_rls.out (before): charge_events rls=%s force=%s policies=%s rows=%s | handover :%d-:%d (sha256 of the whole file %s) after-table: charge_events %s | CONTROL users line in probe: %s' % (
    ce_b and ce_b.group(1), ce_b and ce_b.group(2), ce_b and ce_b.group(3), rows_b and rows_b.group(1), a, b, sha(open(I4['handover'], 'rb').read())[:16],
    ce_a and 'exists %s cols %s rows %s rls %s force %s policies %s' % (ce_a.group(1), ce_a.group(2), ce_a.group(3), ce_a.group(5), ce_a.group(6), ce_a.group(7)), bool(re.search(r'users relrowsecurity=true policies=2', pr))))
dr = open(opt('--draft', os.path.join(G, KB['draft'])), encoding='utf-8').read()
VOC = ['seat', 'pane', 'fleet', 'Wednesday', 'tmux', 'Claude', 'agent', 'Kam', 'Stuart', 'Peter', 'worktree', 'gate', 'QA', 'Datasec', 'DRAFT']
for tag, name, txt in (('I5a', 'ticket title+description', tb.decode() + '\n' + db.decode()), ('I5b', 'KS-1397 draft', dr)):
    hits = {w: len(re.findall(r'(?i)\b%s\b' % w, txt)) for w in VOC}; hot = {w: c for w, c in hits.items() if c}
    keys = sorted(set(re.findall(r'\bKS-\d+\b', txt))); dek = sorted(set(re.findall(r'\bKS \d+\b', txt)))
    print('READ %s: %s internal-vocabulary hits %s | hyphenated keys %s | de-hyphenated %s | CONTROL the word \'database\'/\'nginx\' counts %d' % (
        tag, name, hot or 'NONE', keys, dek, len(re.findall(r'(?i)database|nginx', txt)))); n += 1
C = KB['conf']; cl = git('show', '%s:%s' % (DEV, C)).split('\n')
l24, l142 = cl[KB['lines'][0] - 1].strip(), cl[KB['lines'][1] - 1].strip()
chk('N1', l24 == 'server_tokens off;' and l142 == 'proxy_hide_header Server;', '%s :%d %r | :%d %r' % (C.split('/')[-1], KB['lines'][0], l24, KB['lines'][1], l142))
for p in [C] + KB['siblings']:
    t = git('show', '%s:%s' % (DEV, p))
    print('READ N2 %s: server_tokens off (control) %d | proxy_hide_header Server %d | proxy_hide_header (any) %d | more_clear_headers %d' % (
        p.split('/')[-1], len(re.findall(r'(?i)server_tokens\s+off', t)), len(re.findall(r'(?i)proxy_hide_header\s+server\b', t)), len(re.findall(r'(?i)proxy_hide_header', t)), len(re.findall(r'(?i)more_clear_headers', t)))); n += 1
print('%s: %d FAIL of %d reads | develop %s | cited commit %s' % ('SOURCES READ' if not fails else 'SOURCES FAIL', len(fails), n, DEV[:12], cc[:12]))
sys.exit(1 if fails else 0)
