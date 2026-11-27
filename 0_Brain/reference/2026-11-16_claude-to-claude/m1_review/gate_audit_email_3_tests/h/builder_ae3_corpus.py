# AUDIT-EMAIL-3 corpus (c): the seat's own generated corpus for the differential of item 5.
# Usage: python3 -B ae3_corpus.py <seed> <out prefix>
# Writes <out>.hex (one hex UTF-8 input per line) and <out>.meta.jsonl ({sec, tpl, planted:[addresses]}).
# Holds: every new end byte of RULING 1 (in a joined link, after a port, in a password), the scheme byte
# (every printable ASCII byte and a few others before `://`, and `://` at the start), T1-T6, K1-K8, item 2's
# "still kept" forms, `git`/`.git` in every letter case, chains, hostile fragments and edge strings.
import random, json, sys, re
SEED = int(sys.argv[1], 0); OUT = sys.argv[2]; R = random.Random(SEED)
LOC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._%+-'
LAB = 'abcdefghijklmnopqrstuvwxyz0123456789'
SUF = ['example.com', 'example.org', 'example.net', 'test', 'invalid', 'example']
END = [',', ';', ')', ']', '}', '|', '&', '(', '[', '{', '\x0b']
OLD_END = ['/', '?', '#']
NOT_END = ['=', '+', '-', '.', '_', '~', ':', '%', '!', '*', '$', "'", '"', '<', '>', '`', '\\', '^', '@']
GITS = ['git', 'GIT', 'Git', 'gIt', 'xgit', 'gitx', 'gi', 'g.it', '.git', '..git']
DOTGIT = ['.git', '.GIT', '.Git', '.gIT', 'git', '.gi', '.git.', '.git/']
def mk_local():
    k = R.random()
    if k < .35: return ''.join(R.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(R.randint(1, 10)))
    if k < .45: return R.choice(GITS).lstrip('.') or 'git'
    if k < .55: return 'first.last'
    s = ''.join(R.choice(LOC) for _ in range(R.randint(1, 24))).lstrip('.')
    return s or 'q'
def mk_domain():
    if R.random() < .05:
        return 'shop.example.' + R.choice(['xn--qae0', 'XN--QAE0'])
    suf = R.choice(SUF); have = suf.count('.') + 1
    labs = [(''.join(R.choice(LAB + '-') for _ in range(R.randint(1, 10))).strip('-') or 'm')
            for _ in range(R.randint(max(0, 2 - have), max(0, 4 - have)))]
    return '.'.join(labs + [suf])
def A(local=None): return (local or mk_local()) + '@' + mk_domain()
def SCHEME(): return R.choice(['https', 'http', 'ssh', 'git+ssh', 'svn+ssh', 'ftp', 'x', 'h2', 'a.b', 'a-b', '9'])
items = []
def add(sec, tpl, text, planted=()):
    items.append({'sec': sec, 'tpl': tpl, 'text': text, 'planted': [p for p in planted if '@' in p]})

# ---- (U) item 1: links joined to an address
for rep in range(40):
    for eb in END + OLD_END + NOT_END:
        a = A(); h = mk_domain(); s = SCHEME(); n = f'{ord(eb):02x}'
        add('U', f'join-{n}', f'{s}://{h}{eb}{a}', [a])
        add('U', f'join-text-{n}', f'see {s}://{h}{eb}{a} now', [a])
        add('U', f'join-port-{n}', f'{s}://{h}:{R.randint(1, 65535)}{eb}{a}', [a])
        add('U', f'join-path-after-{n}', f'{s}://{h}{eb}{a}/p?q=1', [a])
        add('U', f'join-query-before-{n}', f'{s}://{h}/p{eb}{a}', [a])
        pw = 'p' + eb + 'w' + str(R.randint(0, 99))
        d = mk_domain()
        add('U', f'pw-{n}', f'git clone {s}://bob:{pw}@{d}/r', [pw.split(eb)[-1] + '@' + d] if eb != '@' else [])
        add('U', f'user-{n}', f'{s}://bo{eb}b@{d}/r', [])
        add('U', f'pw-nopath-{n}', f'{s}://bob:{pw}@{d}', [])
        add('U', f'two-links-{n}', f'{s}://{h}{eb}{s}://{d}{eb}{a}', [a])
    # the scheme byte: every printable ASCII byte and a few others before `://`
    for c in [chr(x) for x in range(0x21, 0x7f)] + ['\x0b', '\u00e9', ' ', '\t', '\u00a0']:
        a = A(); n = f'{ord(c):02x}'
        add('U', f'scheme-byte-{n}', f'see x{c}://{a} ok', [a])
        add('U', f'scheme-byte-only-{n}', f'{c}://{a}', [a])
        add('U', f'scheme-byte-host-{n}', f'go{c}://{mk_domain()},{a}', [a])
    a = A(); add('U', 'scheme-start', f'://{a}', [a])
    a = A(); add('U', 'scheme-start-host', f'://{mk_domain()},{a}', [a])
    a = A(); add('U', 'inner-scheme', f'see ://x://{a}', [a])
    a = A(); add('U', 'inner-scheme-2', f'https://h.example/?n=x://{a}', [a])
    a = A(); add('U', 'still-user-host', f'https://{a}', [a])
    a = A(); add('U', 'still-ssh', f'ssh://{a}/r', [a])
    a = A(); add('U', 'still-encoded', f'https://{a.replace("@", "%40")}@git.example.com/repo.git', [])
    a = A(); add('U', 'still-one-letter', f'x://{a}', [a])
    a = A(); add('U', 'url-userinfo', f'git clone https://bob:hunter2pw@{mk_domain()}/r', [])

# ---- (C) item 2: the colon forms
T = [('T1', '{a}:/abs'), ('T2', '{a}:~/x'), ('T3', 'git@{d}:org/repo.git'), ('T4', '{a}:rel/path'), ('T5', '{a}:file.txt'),
     ('T6', '{a}:22'), ('K1', '{a}:net/ipv4: fix'), ('K2', 'user={a}:ok,url=http://x.example.com/'), ('K3', '{a}:2026-11-27/notes'),
     ('K4', '{a}:fix,see/notes'), ('K5', '{a}:src/lib.rs: fix'), ('K6', '{a}:~'), ('K7', 'key:{a}:x/y'), ('K8', 'user:{a}:profile/v2'),
     ('rsync-rel', 'rsync -av {a}:backup/ .'), ('rsync-daemon', 'rsync -av {a}::backup/ .'), ('win', '{a}:C:/Users/x'),
     ('forge-other', 'gitea@{d}:org/repo'), ('chain', '{a}:{b}:{c}:/x'), ('chain-rel', '{a}:{b}:x/y'),
     ('s-abs', 'scp notes.txt {a}:/srv/notes/'), ('s-subject-slash', '{a}:/etc/hosts: fix typo'), ('s-tilde', 'scp notes.txt {a}:~'),
     ('s-tilde-user', '{a}:~bob/x'), ('s-git-mailbox', 'git@{d}:security/report'), ('s-git-notes', 'git@{d}:release/notes'),
     ('s-dotgit', '{a}:notes.git'), ('s-dotgit-other', 'deploy@{d}:repo.git'), ('s-glued-link', '{a}https://x.example/p'),
     ('s-git-nopath', 'git@{d}:fix the build'), ('o-GIT', 'git@{d}:Repo.GIT'), ('o-git-paren', '(git@{d}:repo.git)'),
     ('o-git-comma', 'git@{d}:repo.git,'), ('o-releases', '{a}:releases/v2/'), ('o-module', '{a}::module/'),
     ('stop-dq', 'git@{d}:x"/y'), ('stop-sq', "git@{d}:x'/y"), ('stop-lt', 'git@{d}:x</y'), ('stop-gt', 'git@{d}:x>/y'),
     ('stop-bt', 'git@{d}:x`/y'), ('stop-hi', 'git@{d}:x\u00e9/y'), ('stop-vt', 'git@{d}:x\x0b/y'), ('stop-comma', 'git@{d}:x,/y'),
     ('a-fails-git', 'git@{d}:x"y'), ('a-fails-git2', 'git@{d}:xy'), ('gitcase-slash', '{G}@{d}:x/y'), ('gitcase-tilde', '{G}@{d}:~'),
     ('dotgit-case', '{a}:repo{DG}'), ('dotgit-case-git', 'git@{d}:repo{DG}'), ('lead-dot-git', '..git@{d}:x/y'),
     ('local-git-tail', 'xgit@{d}:x/y'), ('local-git-head', 'gitx@{d}:x/y'), ('plus-git', 'a+git@{d}:x/y'),
     ('colon-slash-git', 'git@{d}:/x'), ('colon-tilde-git', 'git@{d}:~x'), ('colon-empty', '{a}:'), ('colon-space', '{a}: x/y'),
     ('colon-nl', '{a}:\nx/y'), ('slash-later-ws', '{a}:x y/z'), ('flag-u', 'curl -u {a}:x/y https://api.example.com/'),
     ('json-colon', '{{"email":"{a}:x/y"}}')]
for rep in range(80):
    for tag, tp in T:
        a, b, c = A(), A(), A(); d = mk_domain(); G = R.choice(GITS).lstrip('.') or 'git'; DG = R.choice(DOTGIT)
        text = tp.format(a=a, b=b, c=c, d=d, G=G, DG=DG)
        pl = [a, b, c] if '{c}' in tp else [a, b] if '{b}' in tp else [a] if '{a}' in tp else []
        if '{d}' in tp:
            loc = re.search(r'([A-Za-z.+{}]*)@\{d\}', tp).group(1).format(G=G).lstrip('.')
            pl = pl + [loc + '@' + d]
        add('C', tag, text, pl)

# ---- (H) hostile fragments over both rules' bytes
FR = [lambda: A(), lambda: A('git'), lambda: A('GIT'), lambda: ':', lambda: '::', lambda: ': ', lambda: ':/', lambda: ':~', lambda: '/',
      lambda: '~', lambda: '.git', lambda: '.GIT', lambda: ' ', lambda: '"', lambda: '://', lambda: 'https://', lambda: 'x://',
      lambda: '?', lambda: '#', lambda: 'x', lambda: '@', lambda: '\u00e9', lambda: '\t', lambda: '<', lambda: '`', lambda: "'",
      lambda: 'a@b.example', lambda: 'git@b.example', lambda: '-', lambda: '.', lambda: '9', lambda: 'h.example.com',
      lambda: 'bob:pw'] + [(lambda e=e: e) for e in END]
for _ in range(6500):
    add('H', 'frag', ''.join(R.choice(FR)() for _ in range(R.randint(2, 16))))
# ---- (E) edge strings, and long inputs at the window end
EDGE = 'aZ9g._%+-@:/~?#,;)]}|&([{"\'<>` \n\tx\u00e9\u00a0\u200b\x0b'
for _ in range(3000):
    add('E', 'edge', ''.join(R.choice(EDGE) for _ in range(R.randint(1, 90))))
for _ in range(20):
    n = R.randint(65600, 70000); body = ''.join(R.choice('ab c:/1\n@.,&') for _ in range(n)); p = R.randint(65000, 65600)
    a = A(); add('E', 'long', body[:p] + ' https://x.example.com,' + a + ':x/y ' + body[p:], [a])
for _ in range(10):
    a = A(); add('E', 'long-colon', 'git@b.example:' * 5000 + a + ':fix/x', [a])
with open(OUT + '.hex', 'w') as h, open(OUT + '.meta.jsonl', 'w') as m:
    for it in items:
        h.write(it['text'].encode().hex() + '\n'); x = dict(it); x.pop('text'); m.write(json.dumps(x) + '\n')
from collections import Counter
print('seed', hex(SEED), 'inputs', len(items), dict(Counter(i['sec'] for i in items)), 'over 65536 bytes', sum(len(i['text'].encode()) > 65536 for i in items))
