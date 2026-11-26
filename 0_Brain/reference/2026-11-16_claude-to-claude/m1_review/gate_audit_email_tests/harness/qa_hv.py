import sys
from collections import Counter
sys.argv = ['x', '/private/tmp/claude-501/qae/corp/c1', '/private/tmp/claude-501/qae/corp/c1.head.out', '/private/tmp/claude-501/qae/corp/c1.pv.out']
exec(open('/private/tmp/claude-501/qae/h/qa_analyze.py').read().split('# ---- survivors ----')[0])
c = Counter(); notaddr_changed = []
NA = ['scp build.tar user@host.example.com:/tmp/x', 'git@git.example.com:org/repo.git', 'git clone https://bob@example.com/r', 'thanks @alice for the review', '@Override', '@app.route("/")', 'npm install pkg@1.2.3', 'npm install @types/node@18.0.0', 'a@b', 'ssh user@localhost', 'a@[192.0.2.1]', 'bob@example..com', 'bob@example.c', 'a @ b', 'https://example.com/users/@alice:profile']
for raw, m, h, v in zip(raws, meta, old, new):
    if h['redact'] != v['redact'] or h['preview'] != v['preview']:
        c[m['section']] += 1
        if raw in NA: notaddr_changed.append(raw)
        # each variant span not in head must be a span whose whole run failed the domain test at head
print('head vs variant differing inputs by section:', dict(c), 'listed not-an-address texts changed:', notaddr_changed)
# lane's literal not-an-address samples (ae_email.rs) through both: from the corpus 'lit' section ae_email.rs#0
for raw, m, h, v in zip(raws, meta, old, new):
    if m['section'] == 'lit' and m['template'] == 'ae_email.rs#0' and h['preview'] != v['preview']: print('  ae_email literal changed:', repr(raw[:80]), repr(h['preview'][:60]), repr(v['preview'][:60]))
