import subprocess, sys, re, json
C = '/private/tmp/b1839-gate/clone'
SRC = C + '/src/Datasec.Suite.Sessions/TokenBroker.cs'
H = ['python3', '-I', '/private/tmp/b1839-gate/gate/heavy.py', '/private/tmp/b1839-gate', 'B1839 second reader']
M = {
 'mRace': ('                if (state.Refresh is null)\n', '                if (true)\n'),
 'mLate': ('                if (_disposed || state.Ended || !IsCurrentLocked(state))\n', '                if (_disposed)\n'),
 'mSubj': ('        if (!string.Equals(state.Grant.Subject, state.SessionUser, StringComparison.Ordinal))\n        {\n            EndLocked(state, SignOutReason.SubjectMismatch, events);\n            return null;\n',
           '        if (state.Grant.Subject.Length < 0)\n        {\n            EndLocked(state, SignOutReason.SubjectMismatch, events);\n            return null;\n'),
 'mSubjAnswer': ('            if (!string.Equals(answer.Subject, state.SessionUser, StringComparison.Ordinal))\n', '            if (answer.Subject.Length < 0)\n'),
 'mStaleWaiter': ('            else if (state!.Ended || !IsCurrentLocked(state))\n', '            else if (state!.Id.Length < 0)\n'),
 'mTimeout': ('answer = await call.WaitAsync(_refreshTimeout, _time, CancellationToken.None).ConfigureAwait(false);', 'answer = await call.ConfigureAwait(false);'),
 'fixSyncBlock': ('call = _refresher.RefreshAsync(state.Key, renewal, state.SessionUser, cancellation.Token);',
                  'var token = cancellation.Token; var user = state.SessionUser; var key = state.Key; call = Task.Run(() => _refresher.RefreshAsync(key, renewal, user, token));'),
}
names = sys.argv[1:] or list(M)
orig = open(SRC).read()
out = {}
for n in names:
    a, b = M[n]
    assert orig.count(a) == 1, (n, orig.count(a))
    open(SRC, 'w').write(orig.replace(a, b))
    try:
        r = subprocess.run(H + ['mut-build-' + n, C, '--', 'dotnet', 'build', 'tests/Datasec.Suite.Sessions.Tests', '-c', 'Release', '--no-restore'], capture_output=True, text=True)
        print(r.stdout.strip())
        if r.returncode != 0:
            out[n] = 'BUILD FAILED'; continue
        r = subprocess.run(H + ['mut-test-' + n, C, 'TIMEOUT=900', '--', 'dotnet', 'test', '--project', 'tests/Datasec.Suite.Sessions.Tests', '-c', 'Release', '--no-build'], capture_output=True, text=True)
        print(r.stdout.strip())
        log = open('/private/tmp/b1839-gate/logs/mut-test-%s.log' % n).read()
        failed = sorted(set(m.split('.')[-1].split(' ')[0] for m in re.findall(r'^failed (\S+)', log, re.M)))
        tot = re.findall(r'total: (\d+)|failed: (\d+)', log)
        out[n] = failed
        print(n, 'RED:' if failed else 'GREEN (hole)', failed)
    finally:
        open(SRC, 'w').write(orig)
        d = subprocess.run(['git', '-C', C, 'diff', '--quiet', '--', 'src/Datasec.Suite.Sessions/TokenBroker.cs']).returncode
        print(n, 'undone, git diff --quiet rc', d)
json.dump(out, open('/private/tmp/b1839-gate/mutants.json', 'w'), indent=1)
