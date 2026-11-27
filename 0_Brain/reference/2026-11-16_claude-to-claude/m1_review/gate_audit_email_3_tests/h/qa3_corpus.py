# QA-AUDIT-EMAIL-3 corpus generator (new; not the builder's ae3_corpus.py, not the earlier checks').
# Usage: python3 -B qa3_corpus.py <seed> <out prefix>
# Writes <out>.hex (one hex UTF-8 input per line) and <out>.meta.jsonl ({sec, tpl, planted:[addresses]}).
import random, json, sys
SEED = int(sys.argv[1], 0); OUT = sys.argv[2]; R = random.Random(SEED)
LOC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._%+-'
LAB = 'abcdefghijklmnopqrstuvwxyz0123456789'
SUF = ['example.com', 'example.org', 'example.net', 'test', 'invalid', 'example']
def anycase(s):
    return R.choice([s, s.upper(), s.capitalize(), ''.join(c.upper() if R.random() < .5 else c for c in s)])
def mk_local(lo=1):
    n = R.choice([1, R.randint(2, 8), R.randint(2, 8), R.randint(2, 8), R.randint(9, 40), R.randint(41, 300)])
    n = max(n, lo)
    k = R.random()
    if k < .35: s = ''.join(R.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(n))
    elif k < .5: s = ('first.last' if n < 11 else 'f' * (n // 2) + '.' + 'l' * (n - n // 2))[:n]
    elif k < .6: s = 'a' * max(1, n // 2) + '+tag' + str(R.randint(0, 99))
    else: s = ''.join(R.choice(LOC) for _ in range(n))
    s = s.lstrip('.')
    return s or 'q'
def mk_domain():
    if R.random() < .06:   # the carried `xn--qae0` label under shop.example. only, every letter case
        return 'shop.example.' + R.choice(['xn--qae0', 'XN--QAE0', 'Xn--qae0', 'xN--QaE0'])
    suf = anycase(R.choice(SUF)); have = suf.count('.') + 1
    nlab = R.randint(max(0, 2 - have), max(0, 6 - have))
    labs = [(''.join(R.choice(LAB + '-') for _ in range(R.randint(1, 15))).strip('-') or 'm') for _ in range(nlab)]
    return '.'.join(labs + [suf])
def A(local=None): return (local if local is not None else mk_local()) + '@' + mk_domain()
items = []
def add(sec, tpl, text, planted=()):
    items.append({'sec': sec, 'tpl': tpl, 'text': text, 'planted': [p for p in planted if '@' in p]})
def fill(tp, **kw):
    a = A(); b = A(); c = A(); d = mk_domain()
    v = dict(a=a, b=b, c=c, d=d); v.update(kw)
    txt = tp.format(**v)
    return txt, [v[k] for k in ('a', 'b', 'c') if '{' + k + '}' in tp]
# ---- J: RULING 1, every join between a path-less link and an address, five placements (16 inputs each)
J = [chr(c) for c in range(0x20, 0x7f)] + [''] + [chr(c) for c in list(range(0x00, 0x20)) + [0x7f]]
J += ['\\n', '\\t', '\\r', '\\u0026', '%0A', '%2C', '\u00a0', '\u3000', '\uff0c', '\u3001', '\u2028']
J += ['\u00ad', '\u180e'] + [chr(c) for c in range(0x200b, 0x2010)] + [chr(c) for c in range(0x202a, 0x202f)] + [chr(c) for c in range(0x2060, 0x2065)] + ['\ufeff']
JP = [('plain', 'https://x.example.com{J}{a}'), ('port', 'https://x.example.com:8443{J}{a}'),
      ('csv', 'id,link,email\n3,https://x.example.com{J}{a},ok'), ('kv', 'ts=1 url=https://api.example.com{J}{a} status=200'),
      ('json', '{{"text":"https://x.example.com{J}{a}"}}')]
for j in J:
    name = 'U+%04X' % ord(j) if len(j) == 1 else ('empty' if j == '' else j)
    for pn, tp in JP:
        for _ in range(16):
            t, pl = fill(tp.replace('{J}', j.replace('{', '{{').replace('}', '}}')))
            add('J', f'j-{pn}-{name}', t, pl)
# ---- U: RULING 1, other link forms (80 each)
UT = [
 ('u-userinfo-is-addr', 'see https://{a}'), ('u-userinfo-is-addr-path', 'see https://{a}/r'), ('u-ssh', 'ssh://{a}/r'),
 ('u-mailto-in-link', 'https://x.example.com,mailto:{a}'), ('u-mailto-query', 'https://x.example.com/?u=mailto:{a}'),
 ('u-enc-user', 'git clone https://alice%40example.org@{d}/repo.git'), ('u-offset0', '://{a}'), ('u-offset0-rest', '://{a} done'),
 ('u-unopened-then-link', 'x=://z,https://{a}/r'), ('u-unopened-then-pw', 'x=://z,https://bob:pw99@{d}/r'),
 ('u-unopened-sp', 'see ://z https://x.example.com,{a}'), ('u-next', 'https://x.example.com/r?next=https://{a}'),
 ('u-two-links', 'https://x.example.com/a {a} https://y.example.com,{b}'), ('u-port-path-comma', 'https://x.example.com:8443/p,{a}'),
 ('u-scheme-digit', 'h2://x.example.com,{a}'), ('u-scheme-plus', 'git+ssh://x.example.com,{a}'), ('u-scheme-one', 'x://{a}'),
 ('u-vt', 'https://x.example.com\x0b{a}'), ('u-chain', 'https://x.example.com,{a},{b}'), ('u-pw-plain', 'https://bob:pw99@{d}/r'),
]
for t, tp in UT:
    for _ in range(80):
        tx, pl = fill(tp); add('U', t, tx, pl)
# the newly hidden host: a password or user name holding each end byte (80 each)
for e in '/?#,;)]}|&([{\x0b':
    nm = 'U+000B' if e == '\x0b' else e
    for _ in range(80):
        d = mk_domain(); add('W', f'w-pw-{nm}', f'git clone https://bob:p{e}ss99@{d}/r', [])
    for _ in range(80):
        d = mk_domain(); add('W', f'w-user-{nm}', f'git clone https://bo{e}b@{d}/r', [])
# a `://` after each non-scheme printable byte (16 each)
for c in range(0x21, 0x7f):
    ch = chr(c)
    if ch.isalnum() or ch in '+.-': continue
    for _ in range(16):
        tx, pl = fill('see ' + ch.replace('{', '{{').replace('}', '}}') + '://{a}'); add('S', f's-after-{ch}', tx, pl)
# ---- C: RULING 2 (80 each)
CT = [
 ('b1-gitlog-abs', '{a}:/etc/hosts: fix typo'), ('b1-access', '{a}:/api/v1/users 200'), ('b1-prompt', 'alice@host.example.com:/var/log# ls'),
 ('b1-scp-abs', 'scp notes.txt {a}:/srv/notes/'), ('b2-tilde', '{a}:~'), ('b2-tilde-user', '{a}:~bob/x'),
 ('b2-prompt', 'alice@host.example.com:~/src$ make'),
 ('b3-git-mailbox', 'git@{d}:security/report'), ('b3-GIT', 'GIT@{d}:x/y'), ('b3-Git', 'Git@{d}:x/y'), ('b3-dotgit', '.git@{d}:x/y'),
 ('b3-dotdotgit', '..git@{d}:x/y'), ('b3-xgit', 'xgit@{d}:x/y'), ('b3-git-quote', 'git@{d}:x"y'), ('b3-git-noslash', 'git@{d}:xy'),
 ('b3-git-space', 'git@{d}:fix the build'), ('b3-git-dotgit-tok', 'git@{d}:repo.git'),
 ('b4-notes', '{a}:notes.git'), ('b4-team', '{a}:team/project.git'), ('b4-GIT', '{a}:repo.GIT'), ('b4-paren', '{a}:repo.git)'),
 ('b4-comma', '{a}:repo.git,'), ('b4-wrapped', '({a}:repo.git)'),
 ('ch-abs', '{a}:{b}:/x'), ('ch-rel', '{a}:{b}:x/y'), ('ch-git', 'git@host.example:{a}:/x'), ('ch-three', '{a}:{b}:{c}:/x'),
 ('r-deploy', 'rsync -av deploy@host.example.com:backup/ .'), ('r-module', 'rsync -av {a}::module/ .'), ('r-win', 'scp f {a}:C:/x'),
 ('r-gitea', 'git clone gitea@{d}:org/repo'), ('r-releases', '{a}:releases/v2/'), ('r-port', '{a}:22'), ('r-file', 'scp {a}:file.txt .'),
 ('k1', '{a}:net/ipv4: fix the checksum'), ('k2', 'user={a}:ok,url=http://x.example.com/'), ('k3', '{a}:2026-11-27/notes'),
 ('k4', '{a}:fix,see/notes'), ('k5', '{a}:src/lib.rs: fix'), ('k7', 'id:{a}:x/y'), ('k8', 'user:{a}:profile/v2'),
]
for t, tp in CT:
    for _ in range(80):
        tx, pl = fill(tp)
        if t.startswith('b3-') or not pl:
            loc = tx.split('@')[0].split()[-1]; dom = tp  # planted: the whole address as written
            at = tx.index('@'); s = at
            while s > 0 and (tx[s - 1].isalnum() or tx[s - 1] in '._%+-'): s -= 1
            e = at + 1
            while e < len(tx) and (tx[e].isalnum() or tx[e] in '.-'): e += 1
            pl = [tx[s:e].lstrip('.')]
        add('C', t, tx, pl)
# stop bytes under a `git` local part (80 each)
for sb in ['"', "'", '<', '>', '`', ' ', '\t', '\n', '\r', '\x0c', '\u00e9', '\x0b', ',', ';', ')', ']', '}', '|']:
    nm = 'U+%04X' % ord(sb)
    for _ in range(80):
        d = mk_domain(); add('T', f't-git-stop-{nm}', f'git@{d}:x{sb}/y', ['git@' + d])
# ---- H: hostile mixes for the headline promise (4,000)
FR = [lambda: A(), lambda: A('git'), lambda: A('.git'), lambda: ':', lambda: ': ', lambda: ':/x', lambda: ':~', lambda: '/', lambda: '~',
      lambda: '.git', lambda: '.GIT', lambda: ' ', lambda: '"', lambda: ',', lambda: ';', lambda: ')', lambda: '|', lambda: '&', lambda: '(',
      lambda: '[', lambda: '{', lambda: '://', lambda: 'https://', lambda: 'x://', lambda: '=://', lambda: '?', lambda: '#', lambda: 'x', lambda: '@',
      lambda: '\u00e9', lambda: '\x0b', lambda: '\t', lambda: '<', lambda: '`', lambda: "'", lambda: 'a@b.example', lambda: 'git@b.example',
      lambda: '-', lambda: '.', lambda: '9', lambda: 'https://x.example.com', lambda: ':8443', lambda: 'bob:p,w@']
for _ in range(4000):
    add('H', 'frag', ''.join(R.choice(FR)() for _ in range(R.randint(2, 16))))
# ---- E: long inputs (over 65,536 bytes)
for _ in range(20):
    n = R.randint(65600, 70000); body = ''.join(R.choice('ab c:/1\n@.,') for _ in range(n)); p = R.randint(65000, 65600)
    a = A(); add('E', 'long', body[:p] + ' https://x.example.com,' + a + ' ' + body[p:], [a])
for _ in range(10):
    a = A(); add('E', 'long-colon', 'git@b.example:' * 5000 + a + ':x/y', [a])
for _ in range(10):
    a = A(); add('E', 'long-link', 'https://x.example.com,' + 'a@b.example,' * 6000 + a, [a])
with open(OUT + '.hex', 'w') as h, open(OUT + '.meta.jsonl', 'w') as m:
    for it in items:
        h.write(it['text'].encode().hex() + '\n'); x = dict(it); x.pop('text'); m.write(json.dumps(x) + '\n')
from collections import Counter
print('seed', hex(SEED), 'inputs', len(items), dict(Counter(i['sec'] for i in items)), 'templates', len(set(i['tpl'] for i in items)),
      'over 65536 bytes', sum(len(i['text'].encode()) > 65536 for i in items))
