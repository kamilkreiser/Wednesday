# QA-AUDIT-EMAIL-2 corpus generator (new; not the builder's ae2_corpus.py, not the first check's qa_corpus.py).
# Usage: python3 -B qa2_corpus.py <seed> <out prefix>
# Writes <out>.hex (one hex UTF-8 input per line) and <out>.meta.jsonl ({sec, tpl, planted:[addresses]}).
import random, json, sys
SEED = int(sys.argv[1], 0); OUT = sys.argv[2]; R = random.Random(SEED)
LOC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._%+-'
LAB = 'abcdefghijklmnopqrstuvwxyz0123456789'
SUF = ['example.com', 'example.org', 'example.net', 'test', 'invalid', 'example']
def anycase(s):
    k = R.randrange(4)
    return [s, s.upper(), s.capitalize(), ''.join(c.upper() if R.random() < .5 else c for c in s)][k]
def mk_local():
    n = R.choice([1, 1, R.randint(2, 8), R.randint(2, 8), R.randint(9, 40), R.randint(41, 300)])
    k = R.random()
    if k < .3: s = ''.join(R.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(n))
    elif k < .45: s = 'first.last'[:max(1, n)] if n < 11 else 'f' * (n // 2) + '.' + 'l' * (n - n // 2)
    elif k < .55: s = 'a' * max(1, n // 2) + '+tag' + str(R.randint(0, 99))
    else: s = ''.join(R.choice(LOC) for _ in range(n))
    s = s.lstrip('.')
    return s or 'q'
def mk_domain():
    if R.random() < .08:   # the lane's own made-up label (the coordinator's ruling 8 exception), every case
        return 'shop.example.' + R.choice(['xn--qae0', 'XN--QAE0', 'Xn--qae0', 'xN--qae0'])
    suf = anycase(R.choice(SUF)); have = suf.count('.') + 1
    nlab = R.randint(max(0, 2 - have), max(0, 6 - have))
    labs = []
    for _ in range(nlab):
        l = ''.join(R.choice(LAB + '-') for _ in range(R.randint(1, 15))).strip('-') or 'm'
        labs.append(l)
    return '.'.join(labs + [suf])
def A(short=False):
    if short: return R.choice(['a', 'b', 'x9']) + '@' + R.choice(['b.test', 'q.example', 'z.invalid'])
    return mk_local() + '@' + mk_domain()
items = []
def add(sec, tpl, text, planted=()):
    items.append({'sec': sec, 'tpl': tpl, 'text': text, 'planted': list(planted)})
# ---- (P) the first check's 70 placements, rebuilt from its verdict's list (:60-76), my own wording where free
P1 = [
 ('prose-mid', 'Please ask {a} about the release.'), ('prose-end', 'The author is {a}'), ('prose-start', '{a} sent the patch'),
 ('alone', '{a}'), ('json', '{{"email":"{a}"}}'), ('json-nested', '{{"u": {{"n": "P", "email": "{a}"}}, "id": 3}}'),
 ('json-key', '{{"{a}": {{"role": "dev"}}}}'), ('json-array', '["{a}", "{b}"]'), ('yaml', 'email: {a}\nname: P'),
 ('toml', 'email = "{a}"'), ('csv', 'id,name,email\n3,P,{a}'), ('tsv', '3\tP\t{a}\ton'),
 ('git-config', 'git config user.email {a}'), ('git-config-q', 'git config --global user.email "{a}"'),
 ('git-author', 'git commit --author="P Q <{a}>" -m x'), ('curl-u', 'curl -u {a}:x https://api.example.com/'),
 ('curl-u-pw', 'curl -u {a}:t0pS3cret https://api.example.com/'), ('ssh', 'ssh {a}'), ('mail', 'mail -s "hi" {a} < b.txt'),
 ('flag-eq', 'tool --email={a} -v'), ('h-from', 'From: {a}'), ('h-to', 'To: {a}'), ('h-reply', 'Reply-To: {a}'),
 ('h-cc', 'Cc: {a}, {b}'), ('h-from-name', 'From: "P Q" <{a}>'), ('h-to-list', 'To: A <{a}>, B <{b}>'),
 ('t-coauth', 'Co-authored-by: P Q <{a}>'), ('t-sob', 'Signed-off-by: P Q <{a}>'), ('log-kv', 'user={a} action=login'),
 ('log-ts', '2026-11-27T01:00:00Z INFO ok user={a} ip=192.0.2.7'), ('log-br', '[{a}] logged in'),
 ('log-colon-key', 'user:{a}:profile'), ('log-pipe', 'login|{a}|ok'), ('log-q', 'msg="sent to {a}" status=200'),
 ('gitlog-ae-s', '{a}:fix the build'), ('gitlog-h-ae-s', '1a2b3c4 {a}:fix the build'), ('gitlog-an-ae', 'P Q <{a}>'),
 ('url-query', 'https://x.example.com/c?to={a}'), ('url-query-port', 'https://x.example.com:8443/c?to={a}'),
 ('url-path', 'https://x.example.com/u/{a}/profile'), ('url-glued-comma', 'see https://x.example.com/a,{a}'),
 ('url-glued-paren', '(see https://x.example.com/a){a}'), ('mailto', 'mailto:{a}'), ('mailto-html', '<a href="mailto:{a}">{a}</a>'),
 ('md-link', '[{a}](mailto:{a})'), ('stack-js', '    at F ({a})'), ('stack-py', '  File "{a}", line 3, in run'),
 ('sql', "SELECT id FROM u WHERE email = '{a}';"), ('angle', '<{a}>'), ('parens', '({a})'), ('end-dot', 'write to {a}.'),
 ('end-comma', '{a}, then'), ('end-semi', '{a}; then'), ('end-excl', 'ping {a}!'), ('end-q', 'is it {a}?'),
 ('colon-space', 'mail {a}: thanks'), ('colon-end', 'to {a}:'), ('nl-after', '{a}\nnext'), ('tab-after', '{a}\tnext'),
 ('crlf', 'To: {a}\r\nSubject: hi'), ('slash-after', '{a}/inbox'), ('hash-after', '{a}#frag'), ('amp-after', '{a}&x=1'),
 ('us-after', '{a}_old'), ('star', '*{a}*'), ('backtick', '`{a}`'), ('squote', "'{a}'"), ('env', 'EMAIL={a}'), ('env-lower', 'contact={a}'),
]
# ---- (L) this lane's placements
P2 = [
 # links: none of / ? # after the host (W-3), a CSV row with a bare link column
 ('w3-comma', 'https://x.example.com,{a}'), ('w3-semi', 'see https://x.example.com;{a}'), ('w3-paren', 'https://x.example.com){a}'),
 ('w3-csv', 'id,link,email\n3,https://x.example.com,{a}'), ('w3-csv2', 'https://x.example.com,{a},{b}'),
 ('w3-pipe', 'https://x.example.com|{a}'), ('w3-bracket', '[https://x.example.com]{a}'), ('w3-noscheme', 'see ://{a}'),
 ('w3-port-comma', 'https://x.example.com:8443,{a}'),
 # links with a path, query, fragment, port, user-info
 ('l-query-nopath', 'https://x.example.com?to={a}'), ('l-frag-nopath', 'https://x.example.com#{a}'), ('l-frag', 'https://x.example.com/p#{a}'),
 ('l-port-path', 'https://x.example.com:8443/u/{a}'), ('l-userinfo-q', 'https://u:pw99@x.example.com/?to={a}'),
 ('l-user-q', 'https://bob@x.example.com/?to={a}'), ('l-mailto-in', 'https://x.example.com/r?u=mailto:{a}'),
 ('l-next', 'https://x.example.com/r?next=https://{a}'), ('l-next-path', 'https://x.example.com/login?next=https://y.example.com/{a}'),
 ('l-two-tok', 'https://x.example.com/a {a} https://y.example.com/?b={b}'), ('l-unsub', 'unsubscribe: https://x.example.com/u?email={a}&t=1'),
 ('l-comma-q', 'https://x.example.com/?a=1,{a},{b}'),
 # passwords holding / ? # (the coordinator's ruling 1): the host is an address-like
 ('pw-slash', 'git clone https://bob:pa/ss@{d}/r'), ('pw-q', 'git clone https://bob:pa?ss@{d}/r'), ('pw-hash', 'git clone https://bob:pa#ss@{d}/r'),
 # colon forms (W-4 and the coordinator's ruling 2)
 ('c-gitlog-path', '{a}:src/lib.rs: fix the build'), ('c-key-path', 'key:{a}:x/y'), ('c-date-path', '{a}:2026-11-27/notes'),
 ('c-comma-path', '{a}:fix,see/notes'), ('c-profile-v2', 'user:{a}:profile/v2'), ('c-tilde', '{a}:~'), ('c-tilde-user', '{a}:~user'),
 ('c-git', '{a}:repo.git'), ('c-GIT', '{a}:repo.GIT'), ('c-git-comma', '{a}:repo.git,'), ('c-git-paren', '({a}:repo.git)'),
 ('c-port', '{a}:8443'), ('c-file', 'scp {a}:file.txt .'), ('c-secret', '{a}:secret'), ('c-url-later', '{a}:login,ref=https://x.example.com/p'),
 ('c-json-later', 'user={a}:ok,url=http://x.example.com/'), ('c-vt', '{a}:\x0bx/y'), ('c-nbsp', '{a}:\u00a0x/y'), ('c-quote-slash', '{a}:"x/y"'),
 ('c-lt-slash', '{a}:<x/y>'), ('c-bt', '{a}:`a/b`'), ('c-ws-later', '{a}:x y/z'),
 # glued forms of every kind of (c)
 ('g-hash', '{a}9f86d081884c7d659a2feaa0c55ad015'), ('g-year', '{a}2026'), ('g-dash1', '{a}-1'), ('g-backup', '{a}-backup2'),
 ('g-dot1', '{a}.1'), ('g-flag', '{a}--password'), ('g-pem', '{a}-----BEGIN PRIVATE KEY-----\nab/cd\n-----END PRIVATE KEY-----'),
 ('g-url', '{a}https://x.example.com/p'), ('g-uuid', '{a}550e8400-e29b-41d4-a716-446655440000'), ('g-b64', '{a}dXNlcjpwYXNzd29yZA'),
 ('g-old', '{a}-old'), ('g-dash-colon', '{a}-1:8080'), ('g-dot-dash', '{a}.-x'), ('g-dotdot', '{a}..x'),
]
for _ in range(80):
    for t, tp in P1 + P2:
        a = A(); b = A(); d = mk_domain()
        pl = [a] + ([b] if '{b}' in tp else []) + (['bob:pa' + t[3:4] + 'ss@' + d] if False else [])
        add('P' if (t, tp) in P1 else 'L', t, tp.format(a=a, b=b, d=d), pl if '{a}' in tp else [])
for t, tp in P1[:12]:
    for _ in range(10):
        a = A(short=True); add('S', t + '-short', tp.format(a=a, b=a), [a])
# ---- (H) hostile: the two forward-only indexes and the headline promise
FR = [lambda: A(), lambda: ':', lambda: ': ', lambda: ':/x', lambda: '/', lambda: '~', lambda: '.git', lambda: '.GIT', lambda: ' ',
      lambda: '"', lambda: ',', lambda: ';', lambda: ')', lambda: '|', lambda: '://', lambda: 'https://', lambda: '?', lambda: '#', lambda: 'x',
      lambda: '@', lambda: '\u00e9', lambda: '\x0b', lambda: '\t', lambda: '<', lambda: '`', lambda: "'", lambda: 'a@b.example', lambda: '-', lambda: '.', lambda: '9']
for _ in range(6000):
    add('H', 'frag', ''.join(R.choice(FR)() for _ in range(R.randint(2, 14))))
for _ in range(1500):
    a, b, c = A(), A(), A()
    tp = R.choice(['{a}: x {b}:/x', '{a}: {b}:/x', '{a}:\n{b}:/x', '{a}:', '{a}:{b}:{c}:/x', '{a}:x{b}:y/z', '{a}:x {b}:y {c}:/z',
                   'L' * R.randint(1, 3000) + ' {a}: x', '{a}: ' + 'tok' * R.randint(1, 50) + ' {b}:q/w', 'https://h.example/{a} {b}:z',
                   '{a}:x"{b}:/y', '{a}:~ {b}:x', '{a}:x.git{b}:y', 'u:{a}:v:{b}:w/x', '{a}:é/x {b}:y'])
    add('H', 'idx', tp.format(a=a, b=b, c=c), [x for x, k in ((a, '{a}'), (b, '{b}'), (c, '{c}')) if k in tp])
# ---- (E) edge strings over a lane alphabet, and long inputs
EDGE = 'aZ9._%+-@:/~?#,;)|"\'<>` \n\tx\u00e9\u00a0\u200b\x0b'
for _ in range(3000):
    add('E', 'edge', ''.join(R.choice(EDGE) for _ in range(R.randint(1, 90))))
for _ in range(30):
    n = R.randint(65600, 70000); body = ''.join(R.choice('ab c:/1\n@.') for _ in range(n)); p = R.randint(65000, 65600)
    a = A(); add('E', 'long', body[:p] + ' ' + a + ':x ' + body[p:], [a])
for _ in range(10):
    a = A(); add('E', 'long-colon', 'a@b.example:' * 6000 + a + ':fix', [a])
with open(OUT + '.hex', 'w') as h, open(OUT + '.meta.jsonl', 'w') as m:
    for it in items:
        h.write(it['text'].encode().hex() + '\n'); x = dict(it); x.pop('text'); m.write(json.dumps(x) + '\n')
from collections import Counter
print('seed', hex(SEED), 'inputs', len(items), dict(Counter(i['sec'] for i in items)), 'over 65536 bytes', sum(len(i['text'].encode()) > 65536 for i in items))
