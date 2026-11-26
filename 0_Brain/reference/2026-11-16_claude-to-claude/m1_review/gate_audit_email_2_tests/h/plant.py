# QA-AUDIT-EMAIL-2 source plants: ONE edit to crates/coagent-audit/src/redact.rs of a copy. Usage: python3 -B plant.py <copy dir> <name>
import sys
D, N = sys.argv[1], sys.argv[2]; P = D + '/crates/coagent-audit/src/redact.rs'; s = open(P).read()
E = {
 'p7':    ('                r.push((s, e));\n', '                r.push((s, (e + 1).min(b.len())));\n'),
 'pq':    (".position(|&c| matches!(c, b'/' | b'?' | b'#'))", ".position(|&c| c == b'/')"),
 'pnoq':  (".position(|&c| matches!(c, b'/' | b'?' | b'#'))", ".position(|&c| matches!(c, b'/' | b'#'))"),
 'pnoh':  (".position(|&c| matches!(c, b'/' | b'?' | b'#'))", ".position(|&c| matches!(c, b'/' | b'?'))"),
 'pg':    ("if after.first() == Some(&b'~') || slash < tok_end || after.ends_with(b\".git\") {", "if after.first() == Some(&b'~') || slash < tok_end {"),
 'pt':    ("if after.first() == Some(&b'~') || slash < tok_end || after.ends_with(b\".git\") {", "if slash < tok_end || after.ends_with(b\".git\") {"),
 'pstop': ("            c.is_ascii_whitespace() || matches!(c, b'\"' | b'\\'' | b'<' | b'>' | b'`') || c >= 0x80\n", "            c.is_ascii_whitespace()\n"),
 'p80':   ("            c.is_ascii_whitespace() || matches!(c, b'\"' | b'\\'' | b'<' | b'>' | b'`') || c >= 0x80\n", "            c.is_ascii_whitespace() || matches!(c, b'\"' | b'\\'' | b'<' | b'>' | b'`')\n"),
 'pcl0':  ('                && closed >= 1\n', '                && closed >= 0\n'),
 'pemp':  ('                && !empty\n', ''),
 'pdash': ("            if c != b'-'\n                && !empty", "            if !empty"),
 'plen1': ('((letters && label.len() >= 2) || email_xn(label))', '((letters && label.len() >= 1) || email_xn(label))'),
 'pstale': ('                    slash = slash.max(q);\n', ''),
 'pb0':   ("if after.first() == Some(&b'~') || slash < tok_end || after.ends_with(b\".git\") {", "if after.is_empty() || after.first() == Some(&b'~') || slash < tok_end || after.ends_with(b\".git\") {"),
 'pquad': ('                    tok_end = tok_end.max(q);\n', '                    tok_end = q;\n                    slash = q;\n'),
}
a, b = E[N]
assert s.count(a) == 1, (N, s.count(a))
open(P, 'w').write(s.replace(a, b))
print(N, 'planted in', P)
