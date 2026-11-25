# QA-POLICY-AT-R2 task 1: the engine is untouched (git only). usage: python3 -B task1.py <repo>
import subprocess, sys, hashlib
R = sys.argv[1]
def g(*a, b=False):
    out = subprocess.run(['git', '-C', R] + list(a), capture_output=True, check=True).stdout
    return out if b else out.decode()
B, O, H = '184b35ef17cf9865c4f9b20c721f9647233f8b98', 'a8d910f98215410b59715b8cbacb0d203edf081e', '85565bd7283f94345c71f95c65a85d981b8f3726'
ENG = ['crates/coagent-policy/src', 'crates/coagent-policy/Cargo.toml', 'crates/coagent-policy/red-controls.sh']
for x, y in [(O, H), (B, H), (B, O)]:
    print(f'diff {x[:7]}..{y[:7]} over engine paths: {len(g("diff", x, y, "--", *ENG, b=True))} bytes')
def tree(sha, path):
    d = {}
    for line in g('ls-tree', '-r', sha, '--', path).splitlines():
        meta, name = line.split('\t', 1); d[name] = meta.split()[2]
    return d
to, th, tb = tree(O, 'crates/coagent-policy/src'), tree(H, 'crates/coagent-policy/src'), tree(B, 'crates/coagent-policy/src')
print(f'src entries: a8d910f {len(to)}, head {len(th)}, base {len(tb)}; names equal a8d910f/head: {sorted(to)==sorted(th)}')
print('differing blobs a8d910f vs head:', [n for n in sorted(set(to)|set(th)) if to.get(n)!=th.get(n)])
print('differing blobs base vs head (control):', [(n, tb.get(n,'-')[:7], th.get(n,'-')[:7]) for n in sorted(set(tb)|set(th)) if tb.get(n)!=th.get(n)])
for f in ['crates/coagent-policy/Cargo.toml', 'crates/coagent-policy/red-controls.sh', 'Cargo.lock']:
    print(f, 'blob a8d910f', g('rev-parse', f'{O}:{f}').strip()[:12], 'head', g('rev-parse', f'{H}:{f}').strip()[:12])
TABLE = {
 'q01_gate_attacks.rs':'368fe3eea6426af4e4550bc25d3cfdacde921ea65b0cb591efbe1aa745451550',
 'r2_gate_attacks.rs':'2169c25ac8b057b5acdddc1c404b394bc81bc4bdb00b5e02b3552bbba50ab50d',
 'r3_gate_attacks.rs':'2e3f799ed40ab505597d8df9f8ac587b6402612738fa144a297f26ad32a3f71f',
 'r4_gate_attacks.rs':'89b48198c8b1758d8ab947a216937c606fc46ee0579cb5c85bd0d1f5085a02cf',
 'r5b_bound_probe.rs':'05be31e0d9f426236eff245d660faa2021f634d03e074135da22d21c2ea44ab8',
 'r5b_r4_regressions.rs':'e845c11b50a5ccd617549be1728b141619703d223cb30b7bee588ba08b75203f',
 'r5b_shell_t3.rs':'b4425d8b1b0e6306106b1071da03953a39a8121381934a3682e517868e1fbddd',
 'qa_strict.rs':'75b80cad8f671e9b1c5263b4f77113d5550a7b0a48ebab4e972f763bf2dc7f6b',
 'qa_strict_m2/qa_strict.rs':'694d07c672b3dde3ebd6f7675d9a48168b72924b4d19cca86e6db56cd584bfb3',
 'qa_strict_m2/common/mod.rs':'1670356301cfdaed77bbc67114645de68aed5440348d9fee66f50f02d1338c4c',
 'common/mod.rs':'e4b20635c03ebebd578dae741c64d58825e51536d8b607859b55fd8599f3fc59',
 'bypass_common/mod.rs':'043477832f4ad1c9720251487eef8b3c757ed6e16b65175eebad84861c5178e1',
 't21_bypass_refusals.rs':'ee597d751ffd8d45b99041b3240a0aa7de1392c1e1d9bca630b32f74906ef25f',
 't12_docs.rs':'359f9ef6d9b07c408496cc8fb275e7b1dadfa881821887dcec0b1c111dcfc17d',
 't26_owner_property.rs':'bd765aeb852df9550d814fa5493a24a0d83627b6c9c6c03b0330fad786b1db4e'}
EMPTY = hashlib.sha256(b'').hexdigest()
ok = True
for f, want in TABLE.items():
    hs = [hashlib.sha256(g('show', f'{s}:crates/coagent-policy/tests/{f}', b=True)).hexdigest() for s in (B, O, H)]
    same = hs[0] == hs[1] == hs[2] == want and want != EMPTY
    ok &= same
    print(f'{f:30} base {hs[0][:12]} a8d910f {hs[1][:12]} head {hs[2][:12]} table {want[:12]} {"EQUAL" if same else "DIFFER"}')
print('15 protected equal at all three and the table:', ok, '; count', len(TABLE))
for f in ['t26_owner_property.rs', 't27_owner_dark.rs']:
    a = g('show', f'{O}:crates/coagent-policy/tests/{f}', b=True); b = g('show', f'{H}:crates/coagent-policy/tests/{f}', b=True)
    print(f, 'byte-identical a8d910f/head:', a == b, len(a), 'bytes, sha256', hashlib.sha256(b).hexdigest()[:12])
# control for the hash method: a file the round changed
a = g('show', f'{O}:crates/coagent-policy/tests/t28_at_names.rs', b=True); b = g('show', f'{H}:crates/coagent-policy/tests/t28_at_names.rs', b=True)
print('control t28 a8d910f/head sha256', hashlib.sha256(a).hexdigest()[:12], hashlib.sha256(b).hexdigest()[:12], 'equal:', a == b)
