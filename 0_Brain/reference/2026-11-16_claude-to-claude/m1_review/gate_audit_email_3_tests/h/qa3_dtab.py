# QA-AUDIT-EMAIL-3 (c)/(d) literal inputs with the answer each document states (None = no stated answer).
# Writes corp/dtab.hex + meta.jsonl. Usage: python3 -B qa3_dtab.py
import json, runpy
Q = '/private/tmp/claude-501/qae3/corp/dtab'
K = 'KEPT'
R = []
def add(g, t, want=None, src=''): R.append((g, t, want, src))
# ---- (d) the doc comment of emails, redact.rs:696-788 at the head
for t, w, s in [
 ('...@example.com', K, ':707'), ('alice@example.com-1', '[REDACTED]-1', ':714'), ('alice@example.com2026', '[REDACTED]2026', ':714'),
 ('alice@example.com--flag', '[REDACTED]--flag', ':714'), ('<a@b.example>', '<[REDACTED]>', ':717'), ('mailto:a@b.example', 'mailto:[REDACTED]', ':718'),
 ('https://x.example/c?to=a@b.example', 'https://x.example/c?to=[REDACTED]', ':719'), ('a@b.example:8080', '[REDACTED]:8080', ':721'),
 ('key:a@b.example:profile', None, ':721 (another rule masks key: values)'), ('a@b.example:fix the build', '[REDACTED]:fix the build', ':721'),
 ('a@b.example:net/ipv4: fix', '[REDACTED]:net/ipv4: fix', ':722'), ('https://x.example.com,a@b.example', 'https://x.example.com,[REDACTED]', ':723'),
 ('see ://a@b.example', 'see ://[REDACTED]', ':731'), ('https://user:pw@host.example/', 'https://[REDACTED]@host.example/', ':732'),
 ('https://user@host.example/', K, ':733'), ('https://alice@example.org', K, ':734'), ('ssh://git@host.example.com/r', K, ':735'),
 ('https://alice%40example.org@git.example.com/repo.git', K, ':736'),
 ('https://x.example.com=a@b.example', K, ':737'), ('https://x.example.com+a@b.example', K, ':737'), ('https://x.example.com-a@b.example', K, ':738'),
 ('https://x.example.com.a@b.example', K, ':738'), ('https://x.example.com_a@b.example', K, ':738'), ('https://x.example.com~a@b.example', K, ':738'),
 ('https://x.example.com%a@b.example', K, ':738'), ('https://x.example.com!a@b.example', K, ':738'), ('https://x.example.com*a@b.example', K, ':738'),
 ('https://x.example.com@a@b.example', K, ':738'), ('https://x.example.com:a@b.example', 'https://[REDACTED]@b.example', ':738 (`:` then the URL rule)'),
 ('https://x.example.com:8443=a@b.example', 'https://[REDACTED]@b.example', ':738-739 after a port'),
 ('x://a@b.example', K, ':739'), ('https://bob:p,w@host.example.com/r', 'https://[REDACTED]/r', ':741'),
 ('user@host.example.com:/tmp/x', K, ':747'), ('user@host.example.com:~/x', K, ':747'), ('git@host.example:org/repo', K, ':747'),
 ('git@host.example:repo.git', K, ':748'), ('a@b.example:/etc/hosts: fix typo', K, ':749'), ('a@b.example:~', K, ':749'), ('a@b.example:~bob/x', K, ':750'),
 ('git@example.org:security/report', K, ':751'), ('a@b.example:notes.git', K, ':752'), ('user@host.example.com:rel/path', '[REDACTED]:rel/path', ':753'),
 ('thanks @name', K, ':756'), ('@app.route("/")', K, ':756'), ('pkg@1.2.3', K, ':757'), ('a@b', K, ':758'), ('user@localhost', K, ':758'),
 ('"john doe"@example.com', K, ':760'), ('alice@b\u00fccher.example', K, ':762'), ('j\u00f6rg@example.com', 'j\u00f6[REDACTED]', ':763'),
 ('alice@mail.ex\u00e4mple.test', '[REDACTED]\u00e4mple.test', ':763'), ('alice%40example.com', K, ':767'), ('alice&#64;example.com', K, ':767'),
 ('alice at example dot com', K, ':768'), ('a@localhost', K, ':769'), ('a@[192.0.2.1]', K, ':769'), ('a@b.examplehttps://x.example/p', K, ':771'),
 ('name@file.rs', '[REDACTED]', ':775'), ('x@self.weight', '[REDACTED]', ':776'), ('pkg@2.0.0.beta1', '[REDACTED]1', ':777'),
 ('torch@2.1.0.dev20231001', '[REDACTED]20231001', ':777'), ('user@host.example.com:22', '[REDACTED]:22', ':778'),
 ('user@host.example.com:file.txt', '[REDACTED]:file.txt', ':779'), ('git@host.example:Repo.GIT', '[REDACTED]:Repo.GIT', ':779'),
 ('(git@host.example:repo.git)', '([REDACTED]:repo.git)', ':780'), ('git@host.example:repo.git,', '[REDACTED]:repo.git,', ':780 (by rule)'),
 ('deploy@host.example.com:backup/', '[REDACTED]:backup/', ':781'), ('user@host.example.com:releases/v2/', '[REDACTED]:releases/v2/', ':782'),
 ('user@host.example.com::module/', '[REDACTED]::module/', ':782'), ('user@host.example.com:C:/x', '[REDACTED]:C:/x', ':783'),
]: add('doc', t, w, 'redact.rs' + s)
# ---- docs/AUDIT.md :37-44, :681-705; BACKLOG :1855; M0 :350-368
for t, w, s in [
 ('git clone https://bob:pa/ss@host.example.com/r', 'git clone https://[REDACTED]/r', 'AUDIT.md:690 (`/` in a password)'),
 ('https://bob:p?w@host.example.com/r', 'https://[REDACTED]/r', 'AUDIT.md:690'), ('https://bob:p#w@host.example.com/r', 'https://[REDACTED]/r', 'AUDIT.md:690'),
 ('https://bo,b@host.example.com/r', 'https://[REDACTED]/r', 'AUDIT.md:690 (user name)'),
 ('https://x.example/u/a@b.example/p', 'https://x.example/u/[REDACTED]/p', 'AUDIT.md:701'), ('https://x.example/p#a@b.example', 'https://x.example/p#[REDACTED]', 'AUDIT.md:701'),
 ('scp a@b.example:file.txt .', 'scp [REDACTED]:file.txt .', 'AUDIT.md:701'), ('alice@example.com9f86d0', '[REDACTED]9f86d0', 'AUDIT.md:704 glued'),
 ('see ://a@b.example', 'see ://[REDACTED]', 'BACKLOG:1855, M0:353'),
]: add('audit', t, w, s)
# ---- the build brief's item 0 samples (lines 56-60), at base and head
for t in ['https://x.example.com,alice@example.org', 'see https://x.example.com;alice@example.org', 'see ://alice@example.org',
          'https://x.example.com\u000balice@example.org', 'https://x.example.com:8443,alice@example.org', 'alice@example.com:src/lib.rs',
          'user:alice@example.com:profile/v2', 'alice@example.com:fix,see/notes', 'alice@example.com:2026-11-27/notes', 'a@b.example:x/y', 'a@b.example:~',
          'alice@example.org:net/ipv4: fix the checksum', 'rsync -av deploy@host.example.com:backup/ .', 'rsync -av user@host.example.com::backup/ .',
          'git@host.example:Repo.GIT', '(git@host.example:repo.git)', 'git@host.example:repo.git,', 'pkg@2.0.0.beta1', 'pip install torch@2.1.0.dev20231001',
          'a@b.example:x"/y', 'a@b.example:x\u00e9/y']:
    add('item0', t)
# ---- R-1 control
add('R-1', 'https://bob:pw1234@host.example/r', 'https://[REDACTED]@host.example/r', 'R-1'); add('R-1', 'git clone https://bob:hunter2pw@example.com/r', 'git clone https://[REDACTED]@example.com/r', 'R-1')
# ---- (c)1 RULING 1: each end byte before the @, after it, in the password, in the user name
for e in '/?#,;)]}|&([{\x0b':
    n = 'U+000B' if e == '\x0b' else e
    add('c1-end', f'https://bob:pw{e}@host.example.com/r', None, f'before @ {n}')
    add('c1-end', f'https://bob:pw@{e}host.example.com/r', None, f'after @ {n}')
    add('c1-end', f'https://bob:p{e}w@host.example.com/r', None, f'in password {n}')
    add('c1-end', f'https://b{e}ob@host.example.com/r', None, f'in user name {n}')
# the scheme byte: every byte value that can stand before `://` in UTF-8 text
for c in list(range(0x00, 0x80)) + list(range(0x80, 0xc0)):
    ch = chr(c)   # U+0080..U+00BF encode as C2 80..C2 BF: the byte before :// is 0x80-0xBF
    add('c1-scheme', 'go' + ch + '://alice@example.org', None, 'byte 0x%02x before ://' % (ch.encode()[-1]))
add('c1-scheme', '://alice@example.org', None, 'offset 0'); add('c1-scheme', '://alice@example.org/r', None, 'offset 0, path')
add('c1-w5b', 'x=://a,https://bob@host.example.com/r', None, 'W-5 (2): unopened token then a link with a user')
add('c1-w5b', 'x=://a,https://bob:pw99@host.example.com/r', None, 'W-5 (2): unopened then user:pw')
add('c1-w5b', 'see =://x https://bob@host.example.com/r', None, 'W-5 (2) control: a space ends the unopened token')
add('c1-w5b', 'https://x.example/r?next=https://alice@example.org', None, 'inner :// in an opened token')
# ---- (c)2 RULING 2: each sub-clause alone with (a), and one byte changed so (b) fails
for t, s in [('alice@example.org:/x', 'b1+a'), ('alice@example.org:x/', 'b1 changed: a, no b'), ('alice@example.org:~x', 'b2+a'),
             ('alice@example.org:x~', 'b2 changed: neither'), ('git@example.org:x/y', 'b3+a'), ('gix@example.org:x/y', 'b3 changed: a, no b'),
             ('alice@example.org:x.git', 'b4+a'), ('alice@example.org:x.gix', 'b4 changed: neither'), ('alice@example.org:x/y', 'a without b'),
             ('git@example.org:xy', 'b without a'), ('git@example.org:', 'b3, empty token'), ('git@example.org: x/y', 'b3, space after :'),
             ('.git@example.org:x/y', 'b3 after the dot trim'), ('..git@example.org:x/y', 'b3 after the dot trim'), ('GIT@example.org:x/y', 'b3 case'),
             ('Git@example.org:x/y', 'b3 case'), ('x.git@example.org:x/y', 'local x.git'), ('git.@example.org:x/y', 'local git.'),
             ('git@example.org:x.GIT', 'b4 case, b3'), ('a@b.example:x.GIT', 'b4 case'), ('a@b.example:~/x.git', 'b2+b4'),
             ('git@example.org:repo.git)', 'b3, token ends )'), ('a@b.example:repo.git)', 'b4 fails: token ends )'),
             ('a@b.example:c@d.example:/x', 'chain'), ('git@host.example:alice@example.org:/x', 'chain git'), ('a@b.example:git@d.example:x/y', 'chain: git second'),
             ('git@d.example:a@b.example:x/y', 'chain: git first')]:
    add('c2', t, None, s)
for sb in ['"', "'", '<', '>', '`', ' ', '\t', '\n', '\r', '\x0c', '\u00e9', '\x0b', ',', ';', ')', ']', '}', '|', '&', '(', '[', '{', '#', '?']:
    add('c2-stop', 'git@host.example:x' + sb + '/y', None, 'stop byte U+%04X under git' % ord(sb))
# ---- the last check's (d)/(c) rows, re-run at the head
src = open('/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_audit_email_2_tests/h/qa2_dtab.py').read()
D = eval(src[src.index('D = [') + 4: src.index('\nwith open')])
for g, t in D: add('last-' + g, t, None, 'last check')
with open(Q + '.hex', 'w') as h, open(Q + '.meta.jsonl', 'w') as m:
    for g, t, w, s in R:
        h.write(t.encode().hex() + '\n'); m.write(json.dumps({'sec': g, 'tpl': g, 'want': w, 'src': s, 'planted': []}) + '\n')
print(len(R))
