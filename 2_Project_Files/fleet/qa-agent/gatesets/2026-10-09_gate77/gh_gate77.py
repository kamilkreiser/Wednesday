#!/usr/bin/env python3
"""gh_gate77.py — read-only GitHub REST GETs for gate77 (GH_TOKEN read BY NAME inside lib_gate77, never printed). No write of any kind.

  gh_gate77.py api --pr <n>                         the PR is open, unmerged, base develop, head == kit head, file set == kit numstat paths
  gh_gate77.py census                               every OTHER open PR touching a platform doc or any row's code path (REPORTED, rc 0)
  gh_gate77.py actions --pr <n> --develop <40-hex>  per workflow: the head's failing jobs vs the develop run's (SUBSET, never equality);
                                                    PENDING is never a pass; a workflow with NO comparator run is named, never assumed green
  gh_gate77.py selftest                             offline arms on the SUBSET predicate and the file-set comparison (no network)
rc: 0 pass, 1 a check failed, 3 API failure.
"""
import json, sys, urllib.error
import lib_gate77 as L
from lib_gate77 import K, ROWS, opt, Tally


def files_of(n):
    return sorted(f['filename'] for f in L.gh_pages('pulls/%s/files' % n, key=None))


def api(n, T):
    R = ROWS[n]; p = L.gh_get('pulls/%s' % n)
    T.check('A1', p['state'] == 'open' and not p.get('merged'), '#%s state %s merged %s' % (n, p['state'], p.get('merged')))
    T.check('A2', p['base']['ref'] == 'develop', '#%s base ref %s' % (n, p['base']['ref']))
    T.check('A3', p['head']['sha'] == R['head_expected'], '#%s API head %s == kit %s' % (n, p['head']['sha'][:12], R['head_expected'][:12]))
    T.check('A4', p['head']['ref'] == R['branch'], '#%s head ref %s == kit branch' % (n, p['head']['ref']))
    fs = files_of(n); want = sorted(R['numstat'])
    T.check('A5', fs == want, '#%s API files %d == kit %d%s' % (n, len(fs), len(want), '' if fs == want else ' DIFF %s' % sorted(set(fs) ^ set(want))))
    T.info('A6', '#%s title %r (%d chars) | mergeable_state %s (carries NO testing claim) | body %d chars' % (
        n, p['title'], len(p['title']), p.get('mergeable_state'), len(p.get('body') or '')))


def census(T):
    watch = set(L.DOC_PATHS) | {p for R in ROWS.values() for p in R['code_paths']}
    prs = L.gh_pages('pulls?state=open&base=develop', key=None); hits = []
    for p in prs:
        n = str(p['number'])
        if n in ROWS: continue
        fs = set(files_of(n)) & watch
        if fs: hits.append((n, p['head']['ref'], sorted(fs)))
    T.info('CENSUS', '%d open PRs on develop; %d OTHER PRs touch a watched path' % (len(prs), len(hits)))
    for n, ref, fs in hits:
        T.info('CENSUS', '#%s %s -> %s' % (n, ref, [f.split('/')[-1] for f in fs]))
    T.check('CENSUS-READ', len(prs) >= len(ROWS), 'the census read at least the six rows themselves (%d open)' % len(prs))


def runs_for(sha):
    out = {}
    for r in L.gh_pages('actions/runs?head_sha=%s' % sha):
        w = r['name']; out.setdefault(w, []).append(r)
    return out


def failing_jobs(run):
    return sorted(j['name'] for j in L.gh_pages('actions/runs/%s/jobs' % run['id'], key='jobs') if j.get('conclusion') == 'failure')


def subset_verdict(head_fail, comp_fail, pending):
    if pending: return False, 'PENDING (never a pass)'
    if comp_fail is None: return False, 'NO COMPARATOR RUN (named, never assumed green)'
    extra = sorted(set(head_fail) - set(comp_fail))
    return not extra, ('SUBSET' if not extra else 'NEW RED %s' % extra)


def actions(n, dev, T):
    R = ROWS[n]; H = runs_for(R['head_expected']); D = runs_for(dev)
    for w in sorted(H):
        last = sorted(H[w], key=lambda r: r['created_at'])[-1]
        pend = last['status'] != 'completed'
        hf = [] if pend else failing_jobs(last)
        dl = sorted(D.get(w, []), key=lambda r: r['created_at'])
        df = failing_jobs(dl[-1]) if dl and dl[-1]['status'] == 'completed' else None
        ok, why = subset_verdict(hf, df, pend)
        T.check('ACT-' + w[:24].replace(' ', '_'), ok, '#%s %-28s head run %s %s/%s failing %s | develop %s failing %s -> %s' % (
            n, w, last['id'], last['status'], last.get('conclusion'), hf, dl[-1]['id'] if dl else '-', df, why))


def selftest():
    T = Tally(); arms = []
    def arm(nm, got, want): f = got == want; arms.append(f); print('ARM %-36s got %s want %s %s' % (nm, got, want, 'FIRED' if f else 'DID NOT FIRE'))
    arm('subset holds', subset_verdict(['a'], ['a', 'b'], False)[0], True)
    arm('new red is caught', subset_verdict(['a', 'c'], ['a'], False)[0], False)
    arm('pending is never a pass', subset_verdict([], [], True)[0], False)
    arm('no comparator is never a pass', subset_verdict([], None, False)[0], False)
    print('SELFTEST arms %d/%d' % (sum(arms), len(arms))); return 0 if all(arms) else 1


def main():
    A = sys.argv; mode = A[1] if len(A) > 1 else ''
    if mode == 'selftest': return selftest()
    T = Tally()
    try:
        if mode == 'api': api(L.row_arg(), T)
        elif mode == 'census': census(T)
        elif mode == 'actions':
            dev = opt(A, '--develop') or ''
            if len(dev) != 40: print(__doc__); return 9
            actions(L.row_arg(), dev, T)
        else: print(__doc__); return 9
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        print('API FAILURE: %s' % e); return 3
    return T.end()


if __name__ == '__main__':
    sys.exit(main())
