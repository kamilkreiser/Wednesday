import sys
src = '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1839_verify/tests/B1839AdversarialTests.cs'
out = sys.argv[1]
t = open(src).read()
def rep(a, b):
    global t
    assert t.count(a) == 1, (a[:60], t.count(a))
    t = t.replace(a, b)
# D20 moved the moment a refresher call starts (thread-pool hop): wait for the call before reading counts.
rep('            Assert.True(refresher.Calls == (refreshing ? 1 : 0), "seed " + seed + ": calls " + refresher.Calls + " before release");',
    '            if (refreshing)\n            {\n                await R.Eventually(() => refresher.Calls >= 1, "seed " + seed + " call entered");\n            }\n\n            Assert.True(refresher.Calls == (refreshing ? 1 : 0), "seed " + seed + ": calls " + refresher.Calls + " before release");')
rep('            Assert.Equal(1, refresher.Calls);\n            var newUser = "next" + user;',
    '            await R.Eventually(() => refresher.Calls >= 1, "seed " + seed + " call entered");\n            Assert.Equal(1, refresher.Calls);\n            var newUser = "next" + user;')
rep('            Assert.Equal(1, refresher.Calls);\n            cancelSome.Cancel();',
    '            await R.Eventually(() => refresher.Calls >= 1, "seed " + seed + " call entered");\n            Assert.Equal(1, refresher.Calls);\n            cancelSome.Cancel();')
rep('        var first = broker.GetNewTokenAsync(key, R.Ct);\n        clock.Advance(TimeSpan.FromSeconds(31));',
    '        var first = broker.GetNewTokenAsync(key, R.Ct);\n        await R.Eventually(() => refresher.Calls == 1 && clock.Timers == 1, "S13 first call entered");\n        clock.Advance(TimeSpan.FromSeconds(31));')
rep('        var second = broker.GetNewTokenAsync(key, R.Ct);\n        var overlap = refresher.MaxInFlight;',
    '        var second = broker.GetNewTokenAsync(key, R.Ct);\n        await R.Eventually(() => refresher.Calls == 2, "S13 second call entered");\n        var overlap = refresher.MaxInFlight;')
extra = open('/private/tmp/b1853-gate/scripts/extra.cs').read()
i = t.rstrip().rfind('}')
t = t[:i] + extra + '}\n'
t = t.replace('// Second reader\'s adversarial tests (gate of the token broker lane).', '// Second reader\'s adversarial tests (gate of the token broker lane), round-2 delta copy.', 1)
open(out, 'w').write(t)
print('written', out, t.count('[Fact]'), 'facts')
