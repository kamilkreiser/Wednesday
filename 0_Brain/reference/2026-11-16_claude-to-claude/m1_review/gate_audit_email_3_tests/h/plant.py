# usage: python3 -B plant.py <tree> <name> : one exact replacement in <tree>/crates/coagent-audit/src/redact.rs (must match once); touches every .rs
import sys, os, pathlib
T, N = sys.argv[1:3]
E = {
 'p_comma': (b'const INFO_END: &[u8] = b"/?#,;)]}|&([{\\x0B";', b'const INFO_END: &[u8] = b"/?#;)]}|&([{\\x0B";'),
 'p_amp':   (b'const INFO_END: &[u8] = b"/?#,;)]}|&([{\\x0B";', b'const INFO_END: &[u8] = b"/?#,;)]}|([{\\x0B";'),
 'p_b1':    (b"|| matches!(b.get(q), Some(b'/' | b'~'))", b"|| matches!(b.get(q), Some(b'~'))"),
 'p_b2':    (b"|| matches!(b.get(q), Some(b'/' | b'~'))", b"|| matches!(b.get(q), Some(b'/'))"),
 'p_b3':    (b'|| &b[s..at] == b"git"', b'|| false'),
 'p_b4':    (b'|| &b[s..at] == b"git"\n                        || git;', b'|| &b[s..at] == b"git"\n                        || false;'),
 'p_a':     (b'if old_keep && led {', b'if led {'),
 'p_b3ci':  (b'|| &b[s..at] == b"git"', b'|| b[s..at].eq_ignore_ascii_case(b"git")'),
 'p7':      (b'r.push((s, e));', b'r.push((s, (e + 1).min(b.len())));'),
 'p_dash_p7': None,
 'p7b':     (b'r.push((s, e));', b'r.push((s, (e + 2).min(b.len())));'),
 'p_restart': None,
}
# source mutants of property (f): (old, new)
for i, c in enumerate(b'/?#,;)]}|&([{'):
    ch = bytes([c])
    E['m%02d' % (i + 1)] = (b'const INFO_END: &[u8] = b"/?#,;)]}|&([{\\x0B";', b'const INFO_END: &[u8] = b"' + b'/?#,;)]}|&([{'.replace(ch, b'', 1) + b'\\x0B";')
E['m14'] = (b'const INFO_END: &[u8] = b"/?#,;)]}|&([{\\x0B";', b'const INFO_END: &[u8] = b"/?#,;)]}|&([{";')
E['m15'] = (b"let scheme = p > 0\n                    && (b[p - 1].is_ascii_alphanumeric() || matches!(b[p - 1], b'+' | b'.' | b'-'));", b"let scheme = true;")
E['m16'] = (b"let scheme = p > 0\n                    && (b[p - 1]", b"let scheme = p == 0\n                    || (b[p - 1]")
E['m17'] = (b"|| matches!(b[p - 1], b'+' | b'.' | b'-'));", b"|| false);")
E['m18'] = E['p_b1']; E['m19'] = E['p_b2']; E['m20'] = E['p_b3']; E['m21'] = E['p_b4']; E['m22'] = E['p_a']; E['m23'] = E['p_b3ci']
E['m24'] = (b'|| &b[s..at] == b"git"', b'|| { let mut s0 = at; while s0 > 0 && local(b[s0 - 1]) { s0 -= 1; } &b[s0..at] == b"git" }')
E['m25'] = (b"                    urls.push((start, info));\n                }\n                i = end.max(start);", b"                    urls.push((start, info));\n                    i = end.max(start);\n                } else {\n                    i = p + 1;\n                }")
EDITS = {
 'p_dash_p7': [(b'r.push((s, e));', b'r.push((s, (e + 1).min(b.len())));')],   # with the cfg email_no_dash_trim set at build
 'p_restart': [(b'tok_end = tok_end.max(q);', b'tok_end = q;'), (b'slash = slash.max(q);', b'slash = q;')],
}
p = pathlib.Path(T) / 'crates/coagent-audit/src/redact.rs'; s = p.read_bytes()
for old, new in EDITS.get(N) or [E[N]]:
    assert s.count(old) == 1, (N, s.count(old)); s = s.replace(old, new)
p.write_bytes(s)
for f in pathlib.Path(T).rglob('*.rs'): os.utime(f)
print('planted', N)
