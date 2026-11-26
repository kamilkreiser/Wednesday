# QA-AUDIT-EMAIL corpus generator (own; not the builder's gen_corpus.py).
# Usage: python3 -B qa_corpus.py <seed> <out prefix> <test-literal files...>
# Writes <out>.hex (one hex UTF-8 input per line) and <out>.meta.jsonl (section, template, planted).
import random, json, sys, re
SEED = int(sys.argv[1], 0); OUT = sys.argv[2]; LITFILES = sys.argv[3:]
rnd = random.Random(SEED)
LOCAL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._%+-'
ALNUM = 'abcdefghijklmnopqrstuvwxyz0123456789'
def case(s):
    k = rnd.random()
    return s if k < .6 else s.upper() if k < .75 else ''.join(c.upper() if rnd.random() < .5 else c for c in s)
def local():
    k = rnd.random()
    if k < .05: n = 1
    elif k < .45: n = rnd.randint(2, 8)
    elif k < .85: n = rnd.randint(9, 64)
    else: n = rnd.randint(65, 300)
    k = rnd.random()
    if k < .25: s = ''.join(rnd.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(max(1, n)))
    elif k < .4: a = ''.join(rnd.choice('abcdefghij') for _ in range(rnd.randint(1, 8))); s = a + '.' + ''.join(rnd.choice('klmnopqrst') for _ in range(rnd.randint(1, 8)))
    elif k < .5: s = ''.join(rnd.choice('abcdefgh') for _ in range(rnd.randint(1, 8))) + '+' + ''.join(rnd.choice('xyz019') for _ in range(rnd.randint(1, 8)))
    else: s = ''.join(rnd.choice(LOCAL) for _ in range(n))
    s = s.lstrip('.')
    return s or 'a'
RES = ['example.com', 'example.org', 'example.net', 'test', 'invalid', 'example']
def domain(xn_ok=True):
    k = rnd.random()
    if xn_ok and k < .12:
        tld = rnd.choice(['xn--', 'XN--', 'Xn--', 'xN--']) + ''.join(rnd.choice(ALNUM) for _ in range(rnd.randint(1, 10)))
        labels = [''.join(rnd.choice(ALNUM + '-') for _ in range(rnd.randint(1, 20))) for _ in range(rnd.randint(1, 5))]
        return '.'.join(labels + [tld]), True
    suf = case(rnd.choice(RES))
    nsuf = suf.count('.') + 1
    lo = 1 if nsuf == 1 else 0
    labels = [''.join(rnd.choice(ALNUM + '-') for _ in range(rnd.randint(1, 20))).strip('-') or 'm' for _ in range(rnd.randint(lo, max(lo, 6 - nsuf)))]
    return '.'.join(labels + [suf]), False
def addr(xn_ok=True, short=False):
    if short: return rnd.choice(['a', 'bo', 'x1']) + '@' + rnd.choice(['b.test', 'e.example', 'x.invalid']), False
    d, xn = domain(xn_ok); return local() + '@' + d, xn
items = []
def add(section, template, text, planted=(), **kw):
    items.append(dict(section=section, template=template, text=text, planted=list(planted), **kw))

# ---------------- (b) placements -----------------------------------------------------------
B = [
 ('prose', 'Please contact {a} about the build.'),
 ('prose-end', 'The owner of this change is {a}'),
 ('prose-start', '{a} wrote the patch'),
 ('alone', '{a}'),
 ('json-value', '{{"email":"{a}"}}'),
 ('json-value-sp', '{{"user": {{"name": "A Person", "email": "{a}"}}, "id": 7}}'),
 ('json-key', '{{"{a}": {{"role": "admin"}}}}'),
 ('json-array', '["{a}", "{a2}"]'),
 ('yaml', 'email: {a}\nname: A Person'),
 ('toml', 'email = "{a}"'),
 ('csv', 'id,name,email\n7,A Person,{a}'),
 ('tsv', '7\tA Person\t{a}\tactive'),
 ('sh-git-config', 'git config user.email {a}'),
 ('sh-git-config-q', 'git config --global user.email "{a}"'),
 ('sh-git-author', 'git commit --author="A Person <{a}>" -m fix'),
 ('sh-curl-u', 'curl -u {a}:x https://api.example.com/v1/me'),
 ('sh-curl-u-pw', 'curl -u {a}:s3cretValue https://api.example.com/v1/me'),
 ('sh-ssh', 'ssh {a}'),
 ('sh-mail', 'mail -s "hi" {a} < body.txt'),
 ('sh-email-eq', 'tool --email={a} --verbose'),
 ('hdr-from', 'From: {a}'),
 ('hdr-to', 'To: {a}'),
 ('hdr-replyto', 'Reply-To: {a}'),
 ('hdr-cc', 'Cc: {a}, {a2}'),
 ('hdr-from-name', 'From: "A Person" <{a}>'),
 ('hdr-to-list', 'To: A <{a}>, B <{a2}>'),
 ('trailer-cab', 'Co-authored-by: A Person <{a}>'),
 ('trailer-sob', 'Signed-off-by: A Person <{a}>'),
 ('log-kv', 'user={a} action=login'),
 ('log-kv-ts', '2026-11-26T10:00:00Z INFO auth ok user={a} ip=192.0.2.1'),
 ('log-bracket', '[{a}] logged in'),
 ('log-colon-key', 'user:{a}:profile'),
 ('log-pipe', 'login|{a}|ok'),
 ('log-quoted', 'msg="sent to {a}" status=200'),
 ('gitlog-ae-s', '{a}:fix the build'),
 ('gitlog-h-ae-s', 'abc1234 {a}:fix the build'),
 ('gitlog-an-ae', 'A Person <{a}>'),
 ('url-query', 'https://x.example.com/c?to={a}'),
 ('url-query-port', 'https://x.example.com:8443/c?to={a}'),
 ('url-path', 'https://x.example.com/u/{a}/profile'),
 ('url-glued-comma', 'see https://x.example.com/a,{a}'),
 ('url-glued-paren', '(see https://x.example.com/a){a}'),
 ('mailto', 'mailto:{a}'),
 ('mailto-html', '<a href="mailto:{a}">{a}</a>'),
 ('markdown-link', '[{a}](mailto:{a})'),
 ('stack-js', '    at Foo ({a})'),
 ('stack-py', '  File "{a}", line 3, in run'),
 ('sql', "SELECT id FROM users WHERE email = '{a}';"),
 ('angle', '<{a}>'),
 ('parens', '({a})'),
 ('end-period', 'write to {a}.'),
 ('end-comma', '{a}, then'),
 ('end-semicolon', '{a}; then'),
 ('end-excl', 'ping {a}!'),
 ('end-q', 'is it {a}?'),
 ('colon-space', 'mail {a}: thanks'),
 ('colon-end', 'to {a}:'),
 ('newline-after', '{a}\nnext line'),
 ('tab-after', '{a}\tnext'),
 ('crlf', 'To: {a}\r\nSubject: hi'),
 ('slash-after', '{a}/inbox'),
 ('hash-after', '{a}#frag'),
 ('amp-after', '{a}&x=1'),
 ('underscore-after', '{a}_old'),
 ('star-after', '*{a}*'),
 ('backtick', '`{a}`'),
 ('quote-single', "'{a}'"),
 ('env', 'EMAIL={a}'),
 ('env-lower', 'contact={a}'),
]
NEIGH = [('bearer', 'Bearer Zm9vYmFyYmF6cXV4MTIz'), ('authz', 'Authorization: Basic dXNlcjpwYXNzd29yZA=='),
 ('assign', 'API_KEY=q8Fz21xPLm90aa'), ('pwflag', '--password s3cr3tValue'), ('prefix', 'ghp_16C7e42F292c6912E7710c838347Ae178B4a'),
 ('hex', '9f86d081884c7d659a2feaa0c55ad015'), ('urlpw', 'https://admin:Pa55w0rdX@db.example.net/app'),
 ('pem', '-----BEGIN PRIVATE KEY-----\nab/cd.ef/gh_ij\n-----END PRIVATE KEY-----'), ('name-eq', 'TOKEN=abc')]
JOIN = [' ', '', ':', '=']
for _ in range(60):
    for tid, tpl in B:
        a, xn = addr(); a2, _ = addr(xn_ok=False)
        txt = tpl.format(a=a, a2=a2)
        pl = [a] + ([a2] if '{a2}' in tpl else [])
        add('b', tid, txt, pl, xn=xn)
for _ in range(25):
    for nid, n in NEIGH:
        for j in JOIN:
            for side in ('before', 'after'):
                a, xn = addr()
                txt = (n + j + a) if side == 'before' else (a + j + n)
                add('b', f'neigh-{nid}-{side}-{j!r}', 'x ' + txt + ' y', [a], xn=xn)
                add('b', f'neigh-{nid}-{side}-{j!r}-edge', txt, [a], xn=xn)
# window: address straddling / just before / just after 65,536 bytes; also after a collapsing masked run
for _ in range(40):
    a, _x = addr(xn_ok=False)
    for off in (-len(a) - 1, -len(a) // 2, -3, 0, 5):
        pre = 'w ' * ((65536 + off) // 2)
        pre = pre[:65536 + off]
        add('b', f'window-plain-{off if off in (0,5,-3) else "x"}', pre + a + ' tail', [a], window=True)
    pre = 'a1' * 32761
    add('b', 'window-after-mask', pre + ' ' + a + ' tail', [a], window=True)
# short addresses (< 8 bytes)
for tid, tpl in B[:12]:
    a, _x = addr(short=True); add('b', tid + '-short', tpl.format(a=a, a2=a), [a])
# summaries: the same placements go through the chain's summary (all inputs do; see probe)

# ---------------- (c) glued-after -------------------------------------------------------------
C = [
 ('glued-hash', '{a}9f86d081884c7d659a2feaa0c55ad015', 'cache key: address + hex digest (a common keying idiom: md5/sha of an address appended)'),
 ('glued-digits', '{a}2026', 'address followed by a year/number with no space'),
 ('glued-dash-digit', '{a}-1', 'address + "-1" suffix (backup/rotation name)'),
 ('glued-dash-word-digit', '{a}-backup2', 'address + "-backup2"'),
 ('glued-dot-digits', '{a}.1', 'address then ".1" (rotation)'),
 ('glued-flag', '{a}--password', 'two arguments run together'),
 ('glued-pem', '{a}-----BEGIN PRIVATE KEY-----\nab/cd\n-----END PRIVATE KEY-----', 'address before a PEM block, newline lost'),
 ('glued-url', '{a}https://x.example.com/p', 'address glued to a URL'),
 ('glued-kv-nospace', 'user={a}action=login', 'key=value pairs joined by nothing (letters glued: masked more)'),
 ('glued-kv-digit', 'user={a}id=42', 'key=value pairs joined by nothing'),
 ('glued-cache-colon', 'cache:{a}:v2', 'colon-keyed cache key (redis style)'),
 ('glued-cache-colon-num', 'session:{a}:1732600000', 'colon-keyed key with a timestamp'),
 ('glued-curl-u', 'curl -u {a}:hunter2pw https://api.example.com', 'curl -u user:password (curl man page form)'),
 ('glued-gitlog', '{a}:Fix flaky test', 'git log --format=%ae:%s'),
 ('glued-gitlog2', 'e31b29a {a}:Mask emails', 'git log --format="%h %ae:%s"'),
 ('glued-colon-nbsp', '{a}:\u00a0thanks', 'colon then a no-break space'),
 ('glued-colon-paren', '({a}:)', 'colon then ")"'),
 ('glued-colon-comma', '{a}:,', 'colon then ","'),
 ('glued-colon-quote', '"{a}:"', 'colon then a double quote'),
 ('glued-colon-vt', '{a}:\u000bx', 'colon then U+000B'),
 ('glued-colon-cjk', '{a}:\u8c22\u8c22', 'colon then a CJK character'),
 ('glued-uuid', '{a}550e8400-e29b-41d4-a716-446655440000', 'address + uuid'),
 ('glued-b64', '{a}dXNlcjpwYXNzd29yZA', 'address + base64'),
 ('glued-port', '{a}:8080', 'host:port style after an address'),
 ('glued-hyphen-letters', '{a}-old', 'address + "-old" (letters after hyphen: last label not letters only)'),
]
for _ in range(80):
    for tid, tpl, why in C:
        a, xn = addr(xn_ok=False)
        add('c', tid, tpl.format(a=a), [a], why=why)

# ---------------- (d) not-caught / over-masking / S-1..S-3 forms (single literals) ------------
D = [
 ('quoted-local', '"john doe"@example.com', '"john doe"@example.com'),
 ('nonascii-domain-first', 'alice@b\u00fccher.example', 'alice@b\u00fccher.example'),
 ('nonascii-local', 'j\u00f6rg@example.com', 'j\u00f6rg@example.com'),
 ('nonascii-later-label', 'alice@mail.ex\u00e4mple.com', 'alice@mail.ex\u00e4mple.com'),
 ('pct40', 'alice%40example.com', 'alice%40example.com'),
 ('html-entity', 'alice&#64;example.com', 'alice&#64;example.com'),
 ('spelled', 'alice at example dot com', 'alice at example dot com'),
 ('split-newline', 'alice@\nexample.com', 'alice@\nexample.com'),
 ('split-space', 'alice @ example.com', 'alice @ example.com'),
 ('single-label', 'a@localhost', 'a@localhost'),
 ('numeric', 'a@[192.0.2.1]', 'a@[192.0.2.1]'),
 ('url-user-nopw', 'https://user@host.example/', 'https://user@host.example/'),
 ('scp', 'user@host.example.com:/path', 'user@host.example.com:/path'),
 ('overmask-file', 'name@file.rs', 'name@file.rs'),
 ('overmask-py', 'y = x@self.weight', 'x@self.weight'),
 ('alldots-local', '...@example.com', '...@example.com'),
 ('dots-then-local', '..a@example.com', 'a@example.com'),
 ('trailing-dash-domain', 'a@b.example-', 'a@b.example'),
 ('trailing-dash-xn', 'a@b.xn--', 'a@b.xn'),
 ('upper-xn', 'a@b.XN--ZCKZAH', 'a@b.XN--ZCKZAH'),
 ('glued-hash-doc', 'alice@example.com9f86d081884c7d659a2feaa0c55ad015', 'alice@example.com'),
 ('glued-flag-doc', 'alice@example.com--flag', 'alice@example.com'),
 ('glued-pem-doc', 'alice@example.com-----BEGIN PRIVATE KEY-----', 'alice@example.com'),
 ('glued-url-doc', 'alice@example.comhttps://x.example/p', 'alice@example.com'),
 ('colon-nbsp', 'alice@example.com:\u00a0x', 'alice@example.com'),
 ('colon-paren', 'alice@example.com:)', 'alice@example.com'),
 ('colon-comma', 'alice@example.com:,', 'alice@example.com'),
 ('colon-quote', 'alice@example.com:"', 'alice@example.com'),
 ('colon-vt', 'alice@example.com:\u000bx', 'alice@example.com'),
 ('colon-cjk', 'alice@example.com:\u8c22', 'alice@example.com'),
 ('colon-key', 'user:alice@example.com:profile', 'alice@example.com'),
 ('gitlog', 'alice@example.com:fix the build', 'alice@example.com'),
 ('curl-u', 'curl -u alice@example.com:secret', 'alice@example.com'),
 ('mail-colon', 'mail alice@example.com:thanks', 'alice@example.com'),
 ('query', 'https://x.example/c?to=alice@example.org', 'alice@example.org'),
 ('query-port', 'https://x.example:8443/c?to=alice@example.org', 'alice@example.org'),
 ('url-comma', 'see https://x.example/a,alice@example.org', 'alice@example.org'),
 ('url-paren', 'see https://x.example/a)alice@example.org', 'alice@example.org'),
 ('url-semicolon', 'see https://x.example/a;alice@example.org', 'alice@example.org'),
 ('url-pw', 'https://bob:pw1234@host.example/r', 'pw1234'),
 ('url-pw-lane', 'git clone https://bob:hunter2pw@example.com/r', 'hunter2pw'),
]
for ch, nm in [('\u2066', 'U+2066'), ('\u2067', 'U+2067'), ('\u2068', 'U+2068'), ('\u2069', 'U+2069'), ('\ufe0f', 'U+FE0F'), ('\u034f', 'U+034F'), ('\u200b', 'U+200B(stripped)'), ('\u00ad', 'U+00AD(stripped)')]:
    D.append((f'invis-{nm}-before-at', f'alice{ch}@example.com', 'alice@example.com'))
    D.append((f'invis-{nm}-in-domain', f'alice@exam{ch}ple.com', 'alice@example.com'))
    D.append((f'invis-{nm}-in-local', f'al{ch}ice@example.com', 'alice@example.com'))
for tid, txt, a in D:
    add('d', tid, txt, [a])

# ---------------- (e) differential-only material ----------------------------------------------
def cred():
    k = rnd.randrange(9)
    tok = ''.join(rnd.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for _ in range(rnd.randint(8, 48)))
    return [f'Bearer {tok}', f'Authorization: token {tok}', f'SECRET_KEY={tok}', f'password: {tok}', f'--token {tok}',
            f'sk-ant-{tok}xxxxxxxxxxxxxxxxxxxx', f'https://u:{tok}@h.example.org/x', ''.join(rnd.choice('0123456789abcdef') for _ in range(rnd.randint(10, 70))),
            f'-----BEGIN RSA PRIVATE KEY-----\n{tok}\n{tok}\n-----END RSA PRIVATE KEY-----'][k]
NOTADDR = ['scp build.tar user@host.example.com:/tmp/x', 'git@git.example.com:org/repo.git', 'git clone https://bob@example.com/r',
 'thanks @alice for the review', '@Override\npublic void run()', '@app.route("/")', 'npm install pkg@1.2.3', 'npm install @types/node@18.0.0',
 'a@b', 'ssh user@localhost', 'a@[192.0.2.1]', 'bob@example..com', 'bob@example.c', 'a @ b', 'https://example.com/users/@alice:profile']
EDGE = 'aZ9._%+-@:/ "\'<>`\n\txé\u200b\u00a0\u2066-'
for i in range(4000): add('e', 'cred', cred())
for i in range(3000):
    parts = []
    for _ in range(rnd.randint(1, 5)):
        k = rnd.random()
        if k < .3: parts.append(addr()[0])
        elif k < .6: parts.append(cred())
        elif k < .8: parts.append(rnd.choice(NOTADDR))
        else: parts.append(''.join(rnd.choice('abcdefghij ') for _ in range(rnd.randint(1, 30))))
    add('e', 'mix', rnd.choice([' ', '', ':', '=', '\n', '\t', ',']).join(parts))
for i in range(4000): add('e', 'edge', ''.join(rnd.choice(EDGE) for _ in range(rnd.randint(1, 80))))
for i in range(2000):
    # S-1..S-4 edges: address then a random tail byte class
    a = addr()[0]; tail = rnd.choice([':', ':x', ': ', ':\u00a0', ':)', '-', '--', '.', '..', '9', '-9', '.9', 'x', '\u00e9', '-----BEGIN', 'https://a', ':/', '@', '@b.example'])
    pre = rnd.choice(['', 'x', 'https://h.example/', 'mailto:', 'user:', '<', '"', 'TOKEN=', '\u00e9'])
    add('e', 'edges', pre + a + tail)
UNI = [(0x20, 0x7e), (0xa0, 0x24f), (0x370, 0x3ff), (0x4e00, 0x4e80), (0x1f600, 0x1f64f), (0x200b, 0x200f), (0x2060, 0x2069), (0xfe00, 0xfe0f)]
for i in range(3000):
    s = ''.join(chr(rnd.randint(*rnd.choice(UNI))) for _ in range(rnd.randint(0, 300)))
    if rnd.random() < .3:
        p = rnd.randint(0, len(s)); s = s[:p] + addr()[0] + s[p:]
    add('e', 'unicode', s)
for i in range(40):
    n = rnd.randint(65000, 70000); body = ''.join(rnd.choice('abc 1\n') for _ in range(n))
    p = rnd.randint(65300, 65600); a = addr(xn_ok=False)[0]
    add('e', 'long', body[:p] + ' ' + a + ' ' + cred() + ' ' + body[p:])
# literals of the crate's tests
lit = re.compile(r'(?<![A-Za-z0-9_])(r#*)?"((?:[^"\\]|\\.)*)"', re.S)
def unesc(s):
    try: return bytes(s, 'utf-8').decode('unicode_escape').encode('latin-1').decode('utf-8')
    except Exception: return None
nlit = 0
seen = set()
for f in LITFILES:
    src = open(f, encoding='utf-8').read()
    for m in lit.finditer(src):
        v = m.group(2) if m.group(1) else unesc(re.sub(r'\\u\{([0-9a-fA-F]+)\}', lambda x: '\\U%08x' % int(x.group(1), 16), m.group(2)))
        if v is None or v in seen: continue
        seen.add(v); nlit += 1
        for k, t in enumerate([v, 'word ' * 40 + v, 'line one\nline two ' + v + ' trailing', 'prefix text (' + v + ') suffix', v + '\n' + v]):
            add('lit', f.split('/')[-1] + f'#{k}', t)
with open(OUT + '.hex', 'w') as h, open(OUT + '.meta.jsonl', 'w') as m:
    for it in items:
        h.write(it['text'].encode('utf-8').hex() + '\n')
        it2 = dict(it); it2.pop('text'); m.write(json.dumps(it2) + '\n')
from collections import Counter
print('seed', hex(SEED), 'inputs', len(items), dict(Counter(i['section'] for i in items)), 'distinct literals', nlit)
