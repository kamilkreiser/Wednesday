import sys; sys.argv=['x','/private/tmp/claude-501/qae/corp/c1','/private/tmp/claude-501/qae/corp/c1.base.out','/private/tmp/claude-501/qae/corp/c1.head.out']
src=open('/private/tmp/claude-501/qae/h/qa_analyze.py').read().split('# ---- survivors ----')[0]
exec(src)
i=7745; o=old[i]; nw=new[i]
print(nw['em'], oracle(nw['clean'],xn_ci=True)); print(nw['emw'], oracle(nw['cleanw'],xn_ci=True))
print(merge(nw['find'])==merge(o['find']+nw['em']), merge(nw['findw'])==merge(o['findw']+nw['emw']))
print(repr(o['summ'])[:80], repr(nw['summ'])[:80]); print(len(nw['cleanw']), repr(nw['cleanw'][-30:]))
em=nw['em']; emw=nw['emw']; u=merge(o['find']+em); uw=merge(o['findw']+emw)
print(merge(nw['find']) == u, merge(nw['findw']) == uw, nw['redact'] == apply_mask(nw['clean'], u), nw['preview'] == truncate(apply_mask(nw['cleanw'], uw)), bool(em or emw))
