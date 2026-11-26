# QA-AUDIT-EMAIL-2 (c)/(d) literal inputs: writes corp/dtab.hex + meta. Usage: python3 -B qa2_dtab.py
import json
Q = '/private/tmp/claude-501/qae2/corp/dtab'
D = [
 # (d) the doc comment of emails, :696-760
 ('doc', '...@example.com'), ('doc', 'alice@example.com-1'), ('doc', 'alice@example.com2026'), ('doc', 'alice@example.com--flag'),
 ('doc', '<a@b.example>'), ('doc', '{"to":"a@b.example"}'), ('doc', 'see mailto:a@b.example now'), ('doc', 'Signed-off-by: P Q <a@b.example>'),
 ('doc', 'https://x.example/c?to=a@b.example'), ('doc', 'write a@b.example.'), ('doc', 'a@b.example, then'), ('doc', '(a@b.example)'), ('doc', 'a@b.example: x'),
 ('doc', 'a@b.example:8080'), ('doc', 'key:a@b.example:profile'), ('doc', 'a@b.example:fix the build'),
 ('doc', 'https://user:pw@host.example/'), ('doc', 'https://user@host.example/'), ('doc', 'git clone https://bob:pa/ss@host.example.com/r'),
 ('doc', 'user@host.example.com:/tmp/x'), ('doc', 'git@host.example:org/repo'), ('doc', 'git@host.example:repo.git'), ('doc', 'user@host.example.com:file.txt'),
 ('doc', 'thanks @name'), ('doc', '@app.route("/")'), ('doc', 'pkg@1.2.3'), ('doc', 'a@b'), ('doc', 'user@localhost'),
 ('doc', '"john doe"@example.com'), ('doc', 'alice@b\u00fccher.example'), ('doc', 'j\u00f6rg@example.com'), ('doc', 'alice@mail.ex\u00e4mple.test'),
 ('doc', 'alice\u00e9@example.com'), ('doc', 'alice@ex\u00e4mple.test'), ('doc', 'alice\u2066@example.com'), ('doc', 'alice@exam\u2066ple.com'),
 ('doc', 'alice%40example.com'), ('doc', 'alice&#64;example.com'), ('doc', 'alice at example dot com'), ('doc', 'alice@\nexample.com'), ('doc', 'alice @ example.com'),
 ('doc', 'a@localhost'), ('doc', 'a@[192.0.2.1]'), ('doc', 'a@b.examplehttps://x.example/p'), ('doc', 'name@file.rs'), ('doc', 'y = x@self.weight'),
 # AUDIT.md :680-690 and M0 / BACKLOG examples
 ('audit', 'https://x.example/u/a@b.example/p'), ('audit', 'https://x.example/p#a@b.example'), ('audit', 'scp a@b.example:file.txt .'),
 # BACKLOG :1848 window figures (N-8)
 ('backlog1848', 'a1' * 32761 + ' Bearer Zm9vYmFyYmF6cXV4MTIz tail'), ('backlog1848', 'a1' * 32761 + ' 9f86d081884c7d659a2feaa0c55ad015 tail'),
 ('backlog1848', 'a1' * 32761 + ' ghp_16C7e42F292c6912E7710c838347Ae178B4a tail'),
 # W-2, W-3, W-4
 ('W-2', 'git@host.example:Repo.GIT'), ('W-2', 'git@host.example:repo.GIT'), ('W-2', 'git@host.example:repo.Git'),
 ('W-3', 'https://x.example.com,alice@example.org,bob@example.org'), ('W-3', 'see https://x.example.com;alice@example.org'),
 ('W-3', 'url=https://api.example.com,user=alice@example.org,status=200'), ('W-3', 'https://x.example.com/,alice@example.org'),
 ('W-4', 'alice@example.com:src/lib.rs'), ('W-4', 'user:alice@example.com:profile/v2'), ('W-4', 'alice@example.com:fix,see/notes'), ('W-4', 'alice@example.com:2026-11-27/notes'),
 ('W-4', 'alice@example.org:net/ipv4: fix the checksum'), ('W-4', 'alice@example.com:fix the build/tests'),
 # R-1 control and the first check's (d) rows
 ('R-1', 'https://bob:pw1234@host.example/r'), ('R-1', 'git clone https://bob:hunter2pw@example.com/r'),
 ('d1', 'alice@example.com9f86d081884c7d659a2feaa0c55ad015'), ('d1', 'alice@example.com-----BEGIN PRIVATE KEY-----'), ('d1', 'alice@example.comhttps://x.example/p'),
 ('d1', 'alice@example.com:\u00a0x'), ('d1', 'alice@example.com:)'), ('d1', 'alice@example.com:,'), ('d1', 'alice@example.com:"'), ('d1', 'alice@example.com:\u000bx'),
 ('d1', 'alice@example.com:\u8c22'), ('d1', 'user:alice@example.com:profile'), ('d1', 'curl -u alice@example.com:secret'), ('d1', 'mail alice@example.com:thanks'),
 ('d1', 'https://x.example:8443/c?to=alice@example.org'), ('d1', 'see https://x.example/a,alice@example.org'), ('d1', 'see https://x.example/a)alice@example.org'),
 ('d1', 'see https://x.example/a;alice@example.org'), ('d1', 'a@b.example-'), ('d1', 'a@b.xn--'), ('d1', 'a@b.XN--QAE0'), ('d1', '..a@example.com'),
 # (c)1 RULING 1 boundary
 ('c1', 'https://alice@example.org/x'), ('c1', 'https://x.example/alice@example.org'), ('c1', 'https://x.example?alice@example.org/p'), ('c1', 'https://x.example#alice@example.org/p'),
 ('c1', 'https://bob:p?w@host.example.com/r'), ('c1', 'https://bob:p#w@host.example.com/r'), ('c1', 'see ://alice@example.org'), ('c1', 'x://alice@example.org'),
 ('c1', 'https://x.example/r?next=https://alice@example.org'), ('c1', 'https://x.example.com/a alice@example.org https://y.example.com,bob@example.org'),
 ('c1', 'https://x.example.com"alice@example.org'), ('c1', "https://x.example.com'alice@example.org"), ('c1', 'https://x.example.com<alice@example.org'),
 ('c1', 'https://x.example.com>alice@example.org'), ('c1', 'https://x.example.com`alice@example.org'), ('c1', 'https://x.example.com alice@example.org'),
 ('c1', 'https://x.example.com\u00e9alice@example.org'), ('c1', 'https://x.example.com\talice@example.org'), ('c1', 'https://x.example.com\u000balice@example.org'),
 ('c1', 'https://x.example.com:8443,alice@example.org'), ('c1', 'mailto:alice@example.org'), ('c1', 'https://u:p@x.example.com?to=alice@example.org'),
 # (c)2 RULING 2 colon test, clause by clause
 ('c2', 'a@b.example:~'), ('c2', 'a@b.example:x~'), ('c2', 'a@b.example:x/y'), ('c2', 'a@b.example:xy'), ('c2', 'a@b.example:x.git'), ('c2', 'a@b.example:x.gi'),
 ('c2', 'a@b.example:/'), ('c2', 'a@b.example:'), ('c2', 'a@b.example: /x'),
 ('c2', 'a@b.example:x"/y'), ('c2', "a@b.example:x'/y"), ('c2', 'a@b.example:x</y'), ('c2', 'a@b.example:x>/y'), ('c2', 'a@b.example:x`/y'), ('c2', 'a@b.example:x /y'),
 ('c2', 'a@b.example:x\u00e9/y'), ('c2', 'a@b.example:x\t/y'), ('c2', 'a@b.example:x\n/y'), ('c2', 'a@b.example:x\r/y'), ('c2', 'a@b.example:x\u000c/y'), ('c2', 'a@b.example:x\u000b/y'),
 ('c2', 'a@b.example:x,/y'), ('c2', 'a@b.example:x;/y'), ('c2', 'a@b.example:x)/y'), ('c2', 'a@b.example:x]/y'), ('c2', 'a@b.example:x}/y'), ('c2', 'a@b.example:x|/y'),
 ('c2', 'a@b.example:c@d.example:e@f.example:/x'), ('c2', 'a@b.example:x c@d.example:/y'), ('c2', 'a@b.example:/x c@d.example:y'), ('c2', 'a@b.example:x/y c@d.example:z'),
 ('c2', 'c@d.example:z a@b.example:x/y'), ('c2', 'a@b.example:x.git c@d.example:y'),
 # (c)3 longest valid prefix
 ('c3', 'a@b.example..x'), ('c3', 'a@.b.example'), ('c3', 'a@b.c9'), ('c3', 'a@b.xn---'), ('c3', 'a@b.xn--9'), ('c3', 'a@b.example-.9'), ('c3', 'a@b.xn--.9'),
 ('c3', 'a@b.xn--qae0-.9'), ('c3', 'a@1.example9'), ('c3', 'a@b.example.9'), ('c3', 'a@b-.example9'), ('c3', 'a@-b.example9'), ('c3', 'a@b.e9'),
 ('c3', 'pkg@2.0.0.beta1'), ('c3', 'pip install torch@2.1.0.dev20231001'), ('c3', 'pkg@1.0.0-beta.2'), ('c3', 'pkg@1.2.3-rc1'), ('c3', 'img@sha256:9f86d081'),
 ('c3', 'user@host.example.com:22'), ('c3', 'A@B.T'), ('c3', 'x@self.weight2'), ('c3', 'v@1.2.post1'), ('c3', 'a@b.Example9-'),
]
with open(Q + '.hex', 'w') as h, open(Q + '.meta.jsonl', 'w') as m:
    for g, t in D: h.write(t.encode().hex() + '\n'); m.write(json.dumps({'sec': g, 'tpl': g, 'planted': []}) + '\n')
print(len(D))
