# QA-POLICY-NEXT item 5: cargo's own verdict per manifest text. Builds scratch packages under qpx/mf/pk/<id> (and a
# workspace for the `workspace = true` forms), runs `cargo metadata --offline --no-deps`, and says whether any package
# declares a dependency on the package named coagent-policy. usage: python3 -B -I cargo_verdict.py <cases.json> <outdir>
import json, os, subprocess, sys, re
cases = json.load(open(sys.argv[1])); out = sys.argv[2]
pk = os.path.join(out, 'pk'); os.makedirs(pk, exist_ok=True)
def w(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w').write(s)
w(os.path.join(pk, 'coagent-policy', 'Cargo.toml'), '[package]\nname = "coagent-policy"\nversion = "0.0.1"\nedition = "2021"\n')
w(os.path.join(pk, 'coagent-policy', 'src', 'lib.rs'), '')
w(os.path.join(pk, 'coagent-policy-extra', 'Cargo.toml'), '[package]\nname = "coagent-policy-extra"\nversion = "0.0.1"\nedition = "2021"\n')
w(os.path.join(pk, 'coagent-policy-extra', 'src', 'lib.rs'), '')
def meta(manifest):
    r = subprocess.run(['cargo', 'metadata', '--offline', '--no-deps', '--format-version', '1', '--manifest-path', manifest],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return 'cargo ERROR: ' + ' '.join(r.stderr.strip().splitlines()[:2])[:160]
    m = json.loads(r.stdout)
    hits = []
    for p in m['packages']:
        for d in p['dependencies']:
            if d['name'] == 'coagent-policy':
                hits.append('%s:%s%s%s' % (p['name'], d['kind'] or 'normal', (' as ' + d['rename']) if d.get('rename') else '', (' target ' + d['target']) if d.get('target') else ''))
    return ('DEPENDS ' + '; '.join(hits)) if hits else ('no dependency (packages: %s)' % ','.join(p['name'] for p in m['packages']))
for cid, kind, text in cases:
    name = re.sub(r'[^a-z0-9]+', '-', cid.lower()).strip('-')
    pkg = '[package]\nname = "%s"\nversion = "0.0.0"\nedition = "2021"\n' % name
    d = os.path.join(pk, cid)
    if cid.startswith('N1'):
        print('CARGO\t%s\tn/a (a line of the root manifest: the root is a virtual manifest; cargo reads it as a workspace member path, never a dependency)' % cid); continue
    if kind == 'pos-ws':
        root = os.path.join(out, 'pkws_' + cid)
        w(os.path.join(root, 'Cargo.toml'), '[workspace]\nresolver = "2"\nmembers = ["m"]\n[workspace.dependencies]\ncoagent-policy = { path = "../pk/coagent-policy" }\n')
        w(os.path.join(root, 'm', 'Cargo.toml'), pkg + '\n' + text + '\n'); w(os.path.join(root, 'm', 'src', 'lib.rs'), '')
        print('CARGO\t%s\t%s' % (cid, meta(os.path.join(root, 'Cargo.toml')))); continue
    if kind == 'ws-root':
        w(os.path.join(d, 'Cargo.toml'), '[workspace]\nresolver = "2"\nmembers = []\n' + text + '\n')
        print('CARGO\t%s\t%s' % (cid, meta(os.path.join(d, 'Cargo.toml')))); continue
    if kind == 'pos-top':
        body = text + '\n' + pkg
    elif text.startswith('[package]'):
        body = text + '\n'
    else:
        body = pkg + '\n' + text + '\n'
    w(os.path.join(d, 'Cargo.toml'), body); w(os.path.join(d, 'src', 'lib.rs'), '')
    print('CARGO\t%s\t%s' % (cid, meta(os.path.join(d, 'Cargo.toml'))))
