import subprocess, sys, re, json
C = '/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/b2a618d7-1441-4958-8d80-03e5c5e61cdb/scratchpad/clone'
SRC = C + '/src/Datasec.Suite.Sessions/TokenBroker.cs'
G = '/private/tmp/b1853-gate'
D = '/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/.tools/dotnet/dotnet'
H = ['python3', '-I', G + '/gate/heavy.py', G, 'B1853 second reader (gate round 2)']
M = {
 'mStaleWaiter': ('            else if (state!.Ended || !IsCurrentLocked(state))\n', '            else if (state!.Id.Length < 0)\n'),
 'mSubjAnswer': ('            if (!string.Equals(answer.Subject, state.SessionUser, StringComparison.Ordinal))\n', '            if (answer.Subject.Length < 0)\n'),
 'mTimeout': ('answer = await call.WaitAsync(_refreshTimeout, _time, CancellationToken.None).ConfigureAwait(false);', 'answer = await call.ConfigureAwait(false);'),
 'mRace': ('                if (state.Refresh is null)\n', '                if (true)\n'),
 'mSyncBlock': ('call = Task.Run(() => _refresher.RefreshAsync(key, renewal, user, token));', 'call = _refresher.RefreshAsync(key, renewal, user, token);'),
 'mLate': ('                if (_disposed || state.Ended || !IsCurrentLocked(state))\n', '                if (_disposed)\n'),
 'mIdleAfter': ('            else if (IdlePassed(state, _time.GetUtcNow(), _time.GetTimestamp()))\n            {\n                // D23', '            else if (state.Id.Length < 0 && IdlePassed(state, _time.GetUtcNow(), _time.GetTimestamp()))\n            {\n                // D23'),
}
names = sys.argv[1:] or list(M)
orig = open(SRC).read()
out = {}
for n in names:
    a, b = M[n]
    assert orig.count(a) == 1, (n, orig.count(a))
    open(SRC, 'w').write(orig.replace(a, b))
    try:
        cmd = "'%s' build tests/Datasec.Suite.Sessions.Tests -c Release --no-restore && '%s' test --project tests/Datasec.Suite.Sessions.Tests -c Release --no-build" % (D, D)
        r = subprocess.run(H + ['mut-' + n, C, 'TIMEOUT=900', '--', '/bin/bash', '-c', cmd], capture_output=True, text=True)
        print(r.stdout.strip())
        log = open(G + '/logs/mut-%s.log' % n).read()
        if ' 0 Error(s)' not in log:
            out[n] = 'BUILD FAILED'; print(n, 'BUILD FAILED'); continue
        failed = sorted(set(m.split('.')[-1].split('_')[0] for m in re.findall(r'^failed (\S+)', log, re.M)))
        tot = re.findall(r'^\s*(total|failed): (\d+)', log, re.M)
        out[n] = {'red': failed, 'counts': tot}
        print(n, 'RED:' if failed else 'GREEN (hole)', failed, tot)
    finally:
        open(SRC, 'w').write(orig)
        d = subprocess.run(['git', '-C', C, 'diff', '--quiet', '--', 'src/Datasec.Suite.Sessions/TokenBroker.cs']).returncode
        print(n, 'undone, git diff --quiet rc', d)
json.dump(out, open(G + '/mutants.json', 'w'), indent=1)
