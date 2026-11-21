// Second reader's adversarial tests (gate of the token broker lane), round-2 delta copy. Written OUTSIDE the project and
// copied only into the reviewer's scratch clone to run. Every value is synthetic and made at run time.
// Scope: single-flight refresh and its race (F08), sign-out during a refresh (F09), the subject check on
// every hand-out path (D9, U01 to U04), and "still current" (D12: no record written after its delete).
using System.Collections.Concurrent;
using System.Diagnostics;
using System.Text;

namespace Datasec.Suite.Sessions.Tests.SecondReader;

/// <summary>An independent test clock: wall and monotonic move only when told; one-shot timers on the monotonic clock.</summary>
internal sealed class RClock : TimeProvider
{
    private readonly object _sync = new();
    private readonly List<RTimer> _timers = new();
    private DateTimeOffset _wall = new(2026, 3, 2, 8, 0, 0, TimeSpan.Zero);
    private long _ticks = TimeSpan.FromDays(10).Ticks;

    public override long TimestampFrequency => TimeSpan.TicksPerSecond;

    internal int Timers
    {
        get
        {
            lock (_sync)
            {
                return _timers.Count;
            }
        }
    }

    public override DateTimeOffset GetUtcNow()
    {
        lock (_sync)
        {
            return _wall;
        }
    }

    public override long GetTimestamp()
    {
        lock (_sync)
        {
            return _ticks;
        }
    }

    public override ITimer CreateTimer(TimerCallback callback, object? state, TimeSpan dueTime, TimeSpan period)
    {
        var t = new RTimer(this, callback, state);
        t.Change(dueTime, period);
        return t;
    }

    internal void Advance(TimeSpan by)
    {
        lock (_sync)
        {
            _wall += by;
            _ticks += by.Ticks;
        }

        while (true)
        {
            RTimer? due;
            lock (_sync)
            {
                due = _timers.Where(x => x.Due <= _ticks).OrderBy(x => x.Due).FirstOrDefault();
                if (due is null)
                {
                    return;
                }

                _timers.Remove(due);
            }

            due.Callback(due.State);
        }
    }

    private sealed class RTimer : ITimer
    {
        private readonly RClock _c;

        internal RTimer(RClock c, TimerCallback callback, object? state)
        {
            _c = c;
            Callback = callback;
            State = state;
        }

        internal TimerCallback Callback { get; }

        internal object? State { get; }

        internal long Due { get; private set; }

        public bool Change(TimeSpan dueTime, TimeSpan period)
        {
            lock (_c._sync)
            {
                _c._timers.Remove(this);
                if (dueTime == Timeout.InfiniteTimeSpan)
                {
                    return true;
                }

                Due = _c._ticks + Math.Max(0, dueTime.Ticks);
                _c._timers.Add(this);
                return true;
            }
        }

        public void Dispose()
        {
            lock (_c._sync)
            {
                _c._timers.Remove(this);
            }
        }

        public ValueTask DisposeAsync()
        {
            Dispose();
            return ValueTask.CompletedTask;
        }
    }
}

/// <summary>An in-memory record store with an operation log, optional failures and a widening delay.</summary>
internal sealed class LogStore : ISessionRecordStore
{
    private readonly object _sync = new();
    private readonly Dictionary<string, byte[]> _records = new(StringComparer.Ordinal);
    private readonly List<(string Op, string Id)> _log = new();

    internal volatile bool FailSave;
    internal volatile bool FailDelete;
    internal int SaveSpins;

    public void Save(string id, ReadOnlySpan<byte> record)
    {
        if (FailSave)
        {
            lock (_sync)
            {
                _log.Add(("save-failed", id));
            }

            throw new InvalidOperationException("planted write failure");
        }

        if (SaveSpins > 0)
        {
            Thread.SpinWait(SaveSpins);
        }

        lock (_sync)
        {
            _records[id] = record.ToArray();
            _log.Add(("save", id));
        }
    }

    public bool TryLoad(string id, out byte[]? record)
    {
        lock (_sync)
        {
            if (_records.TryGetValue(id, out var r))
            {
                record = (byte[])r.Clone();
                return true;
            }
        }

        record = null;
        return false;
    }

    public bool Delete(string id)
    {
        if (FailDelete)
        {
            lock (_sync)
            {
                _log.Add(("delete-failed", id));
            }

            throw new InvalidOperationException("planted delete failure");
        }

        lock (_sync)
        {
            _log.Add(("delete", id));
            return _records.Remove(id);
        }
    }

    public IReadOnlyList<string> ListIds()
    {
        lock (_sync)
        {
            return _records.Keys.ToList();
        }
    }

    internal int Count
    {
        get
        {
            lock (_sync)
            {
                return _records.Count;
            }
        }
    }

    internal int SavesOf(string id)
    {
        lock (_sync)
        {
            return _log.Count(e => e.Op == "save" && e.Id == id);
        }
    }

    /// <summary>Ids saved (or attempted) after a delete of the same id was attempted; must be empty (D12).</summary>
    internal List<string> SavedAfterDelete()
    {
        lock (_sync)
        {
            var deleted = new HashSet<string>(StringComparer.Ordinal);
            var bad = new List<string>();
            foreach (var (op, id) in _log)
            {
                if (op.StartsWith("delete", StringComparison.Ordinal))
                {
                    deleted.Add(id);
                }
                else if (op.StartsWith("save", StringComparison.Ordinal) && deleted.Contains(id))
                {
                    bad.Add(id);
                }
            }

            return bad;
        }
    }

    /// <summary>True when any stored record holds the needle as raw bytes or base64 (the record's own layer).</summary>
    internal bool AnyRecordHolds(byte[] needle)
    {
        var b64 = Encoding.ASCII.GetBytes(Convert.ToBase64String(needle));
        lock (_sync)
        {
            return _records.Values.Any(r => r.AsSpan().IndexOf(needle) >= 0 || r.AsSpan().IndexOf(b64) >= 0);
        }
    }
}

/// <summary>A refresher that counts calls and in-flight calls per session and runs a scripted behaviour.</summary>
internal sealed class CountingRefresher : ITokenRefresher
{
    private readonly ConcurrentDictionary<SessionKey, int> _inFlight = new();
    private int _calls;
    private int _maxInFlight;
    private int _wrongSubject;

    internal Func<SessionKey, string, CancellationToken, Task<TokenGrant>> Behaviour { get; set; } =
        (_, _, _) => Task.FromException<TokenGrant>(new InvalidOperationException("no behaviour"));

    internal Func<SessionKey, string?>? ExpectedSubject { get; set; }

    internal int Calls => Volatile.Read(ref _calls);

    internal int MaxInFlight => Volatile.Read(ref _maxInFlight);

    internal int WrongSubjectPassed => Volatile.Read(ref _wrongSubject);

    public async Task<TokenGrant> RefreshAsync(SessionKey session, ReadOnlyMemory<byte> renewalState, string subject, CancellationToken cancellationToken)
    {
        Interlocked.Increment(ref _calls);
        var expected = ExpectedSubject?.Invoke(session);
        if (expected is not null && !string.Equals(expected, subject, StringComparison.Ordinal))
        {
            Interlocked.Increment(ref _wrongSubject);
        }

        var now = _inFlight.AddOrUpdate(session, 1, (_, v) => v + 1);
        int seen;
        while ((seen = Volatile.Read(ref _maxInFlight)) < now && Interlocked.CompareExchange(ref _maxInFlight, now, seen) != seen)
        {
        }

        try
        {
            return await Behaviour(session, subject, cancellationToken).ConfigureAwait(false);
        }
        finally
        {
            _inFlight.AddOrUpdate(session, 0, (_, v) => v - 1);
        }
    }
}

/// <summary>A refresher whose synchronous part blocks before it returns a task (a contract-violating but possible implementation).</summary>
internal sealed class SyncBlockingRefresher : ITokenRefresher
{
    internal ManualResetEventSlim Entered { get; } = new();

    internal ManualResetEventSlim Release { get; } = new();

    internal TimeSpan MaxBlock { get; set; } = TimeSpan.FromSeconds(8);

    internal Func<string, TokenGrant>? Make { get; set; }

    public Task<TokenGrant> RefreshAsync(SessionKey session, ReadOnlyMemory<byte> renewalState, string subject, CancellationToken cancellationToken)
    {
        Entered.Set();
        Release.Wait(MaxBlock);
        return Task.FromResult(Make!(subject));
    }
}

internal static class R
{
    internal static CancellationToken Ct => TestContext.Current.CancellationToken;

    /// <summary>Appends a measurement line to the file named by B1839_NOTES (reviewer's scratch), never a secret.</summary>
    internal static void Note(string line)
    {
        TestContext.Current.SendDiagnosticMessage(line);
        var path = Environment.GetEnvironmentVariable("B1839_NOTES");
        if (!string.IsNullOrEmpty(path))
        {
            lock (typeof(R))
            {
                File.AppendAllText(path, line + "\n");
            }
        }
    }

    internal static byte[] Tok(string user, int gen, string part) => Encoding.UTF8.GetBytes("rdr-" + part + "|" + user + "|" + gen.ToString("D6"));

    internal static (string User, int Gen) Tag(ReadOnlySpan<byte> bytes)
    {
        var parts = Encoding.UTF8.GetString(bytes).Split('|');
        return (parts[1], int.Parse(parts[2], System.Globalization.CultureInfo.InvariantCulture));
    }

    internal static TokenGrant Grant(string user, int gen, DateTimeOffset expires, string? subject = null) =>
        new(Tok(user, gen, "a"), Tok(user, gen, "r"), subject ?? user, expires);

    internal static bool AllZero(byte[] b) => b.All(x => x == 0);

    internal static Task<AccessToken> Safe(Func<Task<AccessToken>> call)
    {
        try
        {
            return call();
        }
        catch (Exception e)
        {
            return Task.FromException<AccessToken>(e);
        }
    }

    /// <summary>Runs actions on dedicated threads released together by a barrier (real contention, no pool ramp-up).</summary>
    internal static void OnThreads(int count, Action<int> body)
    {
        using var barrier = new Barrier(count);
        var errors = new ConcurrentQueue<Exception>();
        var threads = Enumerable.Range(0, count).Select(i => new Thread(() =>
        {
            try
            {
                barrier.SignalAndWait();
                body(i);
            }
            catch (Exception e)
            {
                errors.Enqueue(e);
            }
        })).ToList();
        threads.ForEach(t => t.Start());
        threads.ForEach(t => t.Join());
        if (!errors.IsEmpty)
        {
            throw new AggregateException(errors);
        }
    }

    internal static async Task<bool> Within(Task task, TimeSpan bound)
    {
        var first = await Task.WhenAny(task, Task.Delay(bound, Ct));
        return ReferenceEquals(first, task);
    }

    internal static async Task Eventually(Func<bool> condition, string what)
    {
        var sw = Stopwatch.StartNew();
        while (!condition())
        {
            Assert.True(sw.Elapsed < TimeSpan.FromSeconds(10), what + ": 10 s guard");
            await Task.Delay(1, Ct);
        }
    }
}

public sealed class SecondReaderTests
{
    private enum Outcome
    {
        Accept,
        Throw,
        OtherSubject,
        Expired,
        Null,
        Oversize,
        TimeoutHang,
        TimeoutLate,
    }

    // ---------- F08: a storm of concurrent callers on one held refresh ----------
    [Fact]
    public async Task S01_storm_one_refresher_call_per_flight_every_outcome_only_this_subject()
    {
        long callers = 0;
        var seeds = 0;
        var perOutcome = new int[8];
        for (var seed = 1; seed <= 240; seed++)
        {
            seeds++;
            var rng = new Random(seed);
            var clock = new RClock();
            var store = new LogStore();
            var refresher = new CountingRefresher();
            using var broker = new TokenBroker(new TokenBrokerOptions(), store, refresher, clock);
            var events = new ConcurrentQueue<SessionEventArgs>();
            broker.SessionEvent += (_, e) => events.Enqueue(e);
            var user = "user" + seed.ToString("D5") + "@example.test";
            var key = new SessionKey("SER" + seed, SessionPlatform.Oxpd1, "ps" + seed);
            SignInResult signed;
            using (var g = R.Grant(user, 0, clock.GetUtcNow() + TimeSpan.FromHours(1)))
            {
                signed = broker.SignIn(key, user, TimeSpan.FromHours(2), g);
            }

            var handle = signed.Handle!.Value;
            var inMargin = rng.Next(2) == 0;
            if (inMargin)
            {
                clock.Advance(TimeSpan.FromMinutes(56));
            }

            var gate = new TaskCompletionSource(TaskCreationOptions.RunContinuationsAsynchronously);
            var late = new TaskCompletionSource(TaskCreationOptions.RunContinuationsAsynchronously);
            var outcome = (Outcome)rng.Next(8);
            perOutcome[(int)outcome]++;
            TokenGrant? lateAnswer = null;
            refresher.Behaviour = async (s, subject, ct) =>
            {
                await gate.Task.ConfigureAwait(false);
                var exp = clock.GetUtcNow() + TimeSpan.FromHours(1);
                switch (outcome)
                {
                    case Outcome.Accept:
                        return R.Grant(user, 1, exp, subject);
                    case Outcome.Throw:
                        throw new InvalidOperationException("refresher failed holding " + Encoding.UTF8.GetString(R.Tok(user, 0, "a")));
                    case Outcome.OtherSubject:
                        return R.Grant("other" + user, 1, exp);
                    case Outcome.Expired:
                        return R.Grant(user, 1, clock.GetUtcNow(), subject);
                    case Outcome.Null:
                        return null!;
                    case Outcome.Oversize:
                        return new TokenGrant(new byte[262145], R.Tok(user, 1, "r"), subject, exp);
                    case Outcome.TimeoutHang:
                        await Task.Delay(Timeout.InfiniteTimeSpan, ct).ConfigureAwait(false);
                        throw new InvalidOperationException("unreachable");
                    default:
                        await late.Task.ConfigureAwait(false);
                        lateAnswer = R.Grant(user, 1, clock.GetUtcNow() + TimeSpan.FromHours(1), subject);
                        return lateAnswer;
                }
            };

            var n = rng.Next(4) == 0 ? 1000 : rng.Next(2, 300);
            callers += n;
            var kinds = Enumerable.Range(0, n).Select(_ => rng.Next(4)).ToArray();
            var tasks = new Task<AccessToken>[n];
            var threads = Math.Min(8, n);
            R.OnThreads(threads, t =>
            {
                for (var i = t; i < n; i += threads)
                {
                    var k = kinds[i];
                    tasks[i] = k switch
                    {
                        0 => R.Safe(() => broker.GetTokenAsync(key, R.Ct)),
                        1 => R.Safe(() => broker.GetTokenAsync(handle, key.DeviceSerial, R.Ct)),
                        2 => R.Safe(() => broker.GetNewTokenAsync(key, R.Ct)),
                        _ => R.Safe(() => broker.GetNewTokenAsync(handle, key.DeviceSerial, R.Ct)),
                    };
                }
            });

            var refreshing = kinds.Any(k => k >= 2) || inMargin;
            if (refreshing)
            {
                await R.Eventually(() => refresher.Calls >= 1, "seed " + seed + " call entered");
            }

            Assert.True(refresher.Calls == (refreshing ? 1 : 0), "seed " + seed + ": calls " + refresher.Calls + " before release");
            gate.TrySetResult();
            if (refreshing && (outcome == Outcome.TimeoutHang || outcome == Outcome.TimeoutLate))
            {
                await R.Eventually(() => clock.Timers == 1, "seed " + seed + " timer");
                clock.Advance(TimeSpan.FromSeconds(31));
            }

            Assert.True(await R.Within(Task.WhenAll(tasks.Select(x => (Task)x).Select(x => x.ContinueWith(_ => { }, R.Ct, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default))), TimeSpan.FromSeconds(15)), "seed " + seed + ": callers hung");
            for (var i = 0; i < n; i++)
            {
                var fast = !inMargin && kinds[i] < 2;
                var force = kinds[i] >= 2;
                TokenBrokerError? expected = null;
                var expectedGen = 0;
                if (!fast)
                {
                    switch (outcome)
                    {
                        case Outcome.Accept:
                            expectedGen = 1;
                            break;
                        case Outcome.OtherSubject:
                            expected = TokenBrokerError.SubjectMismatch;
                            break;
                        case Outcome.Throw:
                            expected = force ? TokenBrokerError.RefreshFailed : null;
                            break;
                        case Outcome.Expired:
                        case Outcome.Null:
                            expected = force ? TokenBrokerError.RefreshAnswerRefused : null;
                            break;
                        case Outcome.Oversize:
                            expected = force ? TokenBrokerError.TokenTooLarge : null;
                            break;
                        default:
                            expected = force ? TokenBrokerError.RefreshTimedOut : null;
                            break;
                    }
                }

                var task = tasks[i];
                if (task.IsCompletedSuccessfully)
                {
                    using var token = await task;
                    var (u, gen) = R.Tag(token.AsSpan());
                    Assert.True(u == user, "seed " + seed + ": a token of another subject was handed out");
                    Assert.True(expected is null && gen == expectedGen, "seed " + seed + " caller " + i + " kind " + kinds[i] + " outcome " + outcome + ": got a token of generation " + gen);
                }
                else
                {
                    var ex = task.Exception!.InnerException!;
                    var tbe = Assert.IsType<TokenBrokerException>(ex);
                    Assert.True(expected == tbe.Reason, "seed " + seed + " caller " + i + " kind " + kinds[i] + " outcome " + outcome + ": reason " + tbe.Reason + " expected " + (expected?.ToString() ?? "a token"));
                    Assert.Null(tbe.InnerException);
                }
            }

            if (outcome == Outcome.TimeoutLate && refreshing)
            {
                late.TrySetResult();
                await R.Eventually(() => lateAnswer is not null && R.AllZero(lateAnswer.AccessBytes), "seed " + seed + " late answer disposed");
                Assert.False(store.AnyRecordHolds(R.Tok(user, 1, "a")), "seed " + seed + ": late answer stored");
            }

            Assert.True(refresher.Calls == (refreshing ? 1 : 0), "seed " + seed + ": calls after");
            var newTokens = events.Count(e => e.Kind == SessionEventKind.NewToken);
            Assert.Equal(refreshing && outcome == Outcome.Accept ? 1 : 0, newTokens);
            if (refreshing && outcome == Outcome.OtherSubject)
            {
                Assert.Equal(0, store.Count);
                Assert.Single(events, e => e.Kind == SessionEventKind.SignedOut && e.Reason == SignOutReason.SubjectMismatch);
                Assert.False(store.AnyRecordHolds(R.Tok("other" + user, 1, "a")));
            }
            else
            {
                Assert.Equal(1, store.Count);
            }

            Assert.Empty(store.SavedAfterDelete());
            late.TrySetResult();
        }

        R.Note("S01 seeds " + seeds + " callers " + callers + " outcomes " + string.Join(",", perOutcome));
        Assert.True(callers >= 1000);
    }

    // ---------- F08 + F09 + D9 + D12: free-running threads over many devices ----------
    [Fact]
    public async Task S02_free_running_threads_no_overlapping_refresh_no_foreign_token_no_save_after_delete()
    {
        long ops = 0, tokens = 0, refusals = 0;
        for (var seed = 1; seed <= 40; seed++)
        {
            var clock = new RClock();
            var store = new LogStore { SaveSpins = seed % 3 == 0 ? 2000 : 0 };
            var refresher = new CountingRefresher();
            var issued = new ConcurrentDictionary<SessionKey, (string User, SessionHandle? Handle)>();
            refresher.ExpectedSubject = k => issued.TryGetValue(k, out var v) ? v.User : null;
            var answerRng = new ThreadLocal<Random>(() => new Random(seed * 7919 + Environment.CurrentManagedThreadId));
            var gens = 0;
            refresher.Behaviour = async (s, subject, ct) =>
            {
                await Task.Yield();
                var r = answerRng.Value!.Next(100);
                var gen = Interlocked.Increment(ref gens);
                var exp = clock.GetUtcNow() + TimeSpan.FromMinutes(4);
                if (r < 5)
                {
                    return R.Grant("intruder" + gen + "@example.test", gen, exp);
                }

                if (r < 10)
                {
                    throw new InvalidOperationException("planted refresher failure");
                }

                if (r < 15)
                {
                    return R.Grant(subject, gen, clock.GetUtcNow(), subject);
                }

                return R.Grant(subject, gen, exp, subject);
            };
            using var broker = new TokenBroker(new TokenBrokerOptions(), store, refresher, clock);
            var psid = 0;
            var violations = new ConcurrentQueue<string>();
            var history = new ConcurrentBag<SessionKey>();

            void SignInOn(int device, Random rng)
            {
                var n = Interlocked.Increment(ref psid);
                var platform = rng.Next(2) == 0 ? SessionPlatform.Oxpd1 : SessionPlatform.Oxpd2;
                var key = new SessionKey("DEV" + device, platform, "p" + n);
                var user = "user" + n.ToString("D6") + "@example.test";
                issued[key] = (user, null);
                using var g = R.Grant(user, 0, clock.GetUtcNow() + TimeSpan.FromMinutes(4));
                var res = broker.SignIn(key, user, TimeSpan.FromHours(1), g);
                issued[key] = (user, res.Handle);
                history.Add(key);
            }

            for (var d = 0; d < 6; d++)
            {
                SignInOn(d, new Random(seed + d));
            }

            var pending = new ConcurrentBag<(SessionKey Key, Task<AccessToken> Task)>();
            R.OnThreads(6, t =>
            {
                var rng = new Random(seed * 1000 + t);
                for (var i = 0; i < 400; i++)
                {
                    Interlocked.Increment(ref ops);
                    var keys = history.ToArray();
                    var key = keys[rng.Next(keys.Length)];
                    var (_, handle) = issued[key];
                    var op = rng.Next(100);
                    try
                    {
                        if (op < 30)
                        {
                            pending.Add((key, handle is not null && rng.Next(2) == 0 ? R.Safe(() => broker.GetTokenAsync(handle.Value, key.DeviceSerial, R.Ct)) : R.Safe(() => broker.GetTokenAsync(key, R.Ct))));
                        }
                        else if (op < 60)
                        {
                            pending.Add((key, handle is not null && rng.Next(2) == 0 ? R.Safe(() => broker.GetNewTokenAsync(handle.Value, key.DeviceSerial, R.Ct)) : R.Safe(() => broker.GetNewTokenAsync(key, R.Ct))));
                        }
                        else if (op < 72)
                        {
                            SignInOn(rng.Next(6), rng);
                        }
                        else if (op < 84)
                        {
                            if (handle is not null && rng.Next(2) == 0)
                            {
                                broker.SignOut(handle.Value, key.DeviceSerial);
                            }
                            else
                            {
                                broker.SignOut(key);
                            }
                        }
                        else if (op < 92)
                        {
                            broker.Touch(key);
                        }
                        else
                        {
                            broker.Sweep();
                        }
                    }
                    catch (TokenBrokerException)
                    {
                        Interlocked.Increment(ref refusals);
                    }
                    catch (Exception e)
                    {
                        violations.Enqueue("untyped " + e.GetType().Name);
                    }
                }
            });

            var all = pending.ToArray();
            Assert.True(await R.Within(Task.WhenAll(all.Select(p => p.Task.ContinueWith(_ => { }, R.Ct, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default))), TimeSpan.FromSeconds(20)), "seed " + seed + ": callers hung");
            foreach (var (key, task) in all)
            {
                if (task.IsCompletedSuccessfully)
                {
                    tokens++;
                    using var token = await task;
                    var (u, _) = R.Tag(token.AsSpan());
                    if (u != issued[key].User)
                    {
                        violations.Enqueue("foreign token");
                    }
                }
                else
                {
                    refusals++;
                    if (task.Exception!.InnerException is not TokenBrokerException)
                    {
                        violations.Enqueue("untyped " + task.Exception.InnerException!.GetType().Name);
                    }
                }
            }

            foreach (var key in history.ToArray())
            {
                try
                {
                    broker.SignOut(key);
                }
                catch (TokenBrokerException)
                {
                }
            }

            Assert.True(violations.IsEmpty, "seed " + seed + ": " + string.Join("; ", violations.Distinct()));
            Assert.True(refresher.MaxInFlight <= 1, "seed " + seed + ": two refresher calls of one session overlapped: " + refresher.MaxInFlight);
            Assert.Equal(0, refresher.WrongSubjectPassed);
            Assert.Empty(store.SavedAfterDelete());
            Assert.Equal(0, store.Count);
        }

        R.Note("S02 ops " + ops + " tokens " + tokens + " refusals " + refusals);
    }

    // ---------- F09 / D12: every way a session ends, at three moments relative to a held refresh ----------
    [Fact]
    public async Task S03_session_end_during_refresh_every_trigger_every_moment_no_record_after_delete()
    {
        var runs = 0;
        var outcomes = new ConcurrentDictionary<string, int>();
        for (var seed = 1; seed <= 420; seed++)
        {
            runs++;
            var rng = new Random(seed);
            var trigger = seed % 7;
            var moment = (seed / 7) % 3;
            var clock = new RClock();
            var store = new LogStore { SaveSpins = rng.Next(0, 20000) };
            var refresher = new CountingRefresher();
            var gate = new TaskCompletionSource(TaskCreationOptions.RunContinuationsAsynchronously);
            TokenGrant? answer = null;
            var user = "user" + seed.ToString("D5") + "@example.test";
            refresher.Behaviour = async (s, subject, ct) =>
            {
                await gate.Task.ConfigureAwait(false);
                answer = R.Grant(user, 1, clock.GetUtcNow() + TimeSpan.FromHours(1), subject);
                return answer;
            };
            var broker = new TokenBroker(new TokenBrokerOptions(), store, refresher, clock);
            var events = new ConcurrentQueue<SessionEventArgs>();
            broker.SessionEvent += (_, e) => events.Enqueue(e);
            var key = new SessionKey("SER" + seed, SessionPlatform.Oxpd1, "ps" + seed);
            SignInResult signed;
            using (var g = R.Grant(user, 0, clock.GetUtcNow() + TimeSpan.FromHours(1)))
            {
                signed = broker.SignIn(key, user, TimeSpan.FromSeconds(10), g);
            }

            var oldId = signed.SessionId;
            var joiners = rng.Next(0, 50);
            var waits = new List<Task<AccessToken>> { R.Safe(() => broker.GetNewTokenAsync(key, R.Ct)) };
            for (var j = 0; j < joiners; j++)
            {
                waits.Add(R.Safe(() => broker.GetNewTokenAsync(signed.Handle!.Value, key.DeviceSerial, R.Ct)));
            }

            await R.Eventually(() => refresher.Calls >= 1, "seed " + seed + " call entered");
            Assert.Equal(1, refresher.Calls);
            var newUser = "next" + user;
            SignInResult? second = null;

            void End()
            {
                try
                {
                    switch (trigger)
                    {
                        case 0:
                            broker.SignOut(key);
                            break;
                        case 1:
                            broker.SignOut(signed.Handle!.Value, key.DeviceSerial);
                            break;
                        case 2:
                            using (var g2 = R.Grant(newUser, 0, clock.GetUtcNow() + TimeSpan.FromHours(1)))
                            {
                                second = broker.SignIn(new SessionKey(key.DeviceSerial, SessionPlatform.Oxpd2, "ps2-" + seed), newUser, TimeSpan.FromHours(1), g2);
                            }

                            break;
                        case 3:
                            clock.Advance(TimeSpan.FromSeconds(11));
                            broker.Sweep();
                            break;
                        case 4:
                            clock.Advance(TimeSpan.FromSeconds(11));
                            broker.Touch(key);
                            break;
                        case 5:
                            clock.Advance(TimeSpan.FromSeconds(11));
                            var read = broker.GetTokenAsync(key, R.Ct);
                            SpinWait.SpinUntil(() => read.IsCompleted, 10000);
                            break;
                        default:
                            broker.Dispose();
                            break;
                    }
                }
                catch (TokenBrokerException)
                {
                }
            }

            if (moment == 0)
            {
                End();
                gate.TrySetResult();
            }
            else if (moment == 1)
            {
                R.OnThreads(2, t =>
                {
                    if (t == 0)
                    {
                        gate.TrySetResult();
                    }
                    else
                    {
                        Thread.SpinWait(rng.Next(0, 5000));
                        End();
                    }
                });
            }
            else
            {
                gate.TrySetResult();
                await R.Within(Task.WhenAll(waits.Select(w => w.ContinueWith(_ => { }, R.Ct, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default))), TimeSpan.FromSeconds(10));
                End();
            }

            Assert.True(await R.Within(Task.WhenAll(waits.Select(w => w.ContinueWith(_ => { }, R.Ct, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default))), TimeSpan.FromSeconds(10)), "seed " + seed + ": waiters hung");
            await R.Eventually(() => answer is not null, "seed " + seed + " refresher answered");
            foreach (var w in waits)
            {
                string label;
                if (w.IsCompletedSuccessfully)
                {
                    using var token = await w;
                    var (u, gen) = R.Tag(token.AsSpan());
                    Assert.True(u == user && gen == 1, "seed " + seed + ": wrong token after end (gen " + gen + ")");
                    Assert.True(moment != 0, "seed " + seed + ": a token handed out after the session ended before the answer");
                    label = "token";
                }
                else
                {
                    var ex = w.Exception!.InnerException!;
                    if (trigger == 6 && ex is ObjectDisposedException)
                    {
                        label = "disposed";
                    }
                    else
                    {
                        var tbe = Assert.IsType<TokenBrokerException>(ex);
                        Assert.True(tbe.Reason is TokenBrokerError.SessionNotFound or TokenBrokerError.SessionExpired, "seed " + seed + ": reason " + tbe.Reason);
                        label = tbe.Reason.ToString();
                    }
                }

                outcomes.AddOrUpdate("t" + trigger + "m" + moment + ":" + label, 1, (_, v) => v + 1);
            }

            Assert.Equal(1, refresher.Calls);
            Assert.Empty(store.SavedAfterDelete());
            var ended = events.Any(e => e.Kind == SessionEventKind.SignedOut && e.SessionId == oldId);
            if (trigger is 0 or 1 or 2)
            {
                Assert.True(ended, "seed " + seed + ": the trigger did not end the session");
            }

            if (!ended && trigger != 6)
            {
                // only an idle trigger racing a hand-out (whose activity renews the session) may leave it live
                Assert.True(trigger is 3 or 4 or 5 && moment == 1, "seed " + seed + ": session not ended");
                outcomes.AddOrUpdate("t" + trigger + "m" + moment + ":live-after-race", 1, (_, v) => v + 1);
            }

            if (ended)
            {
                Assert.DoesNotContain(oldId, store.ListIds());
                Assert.False(store.AnyRecordHolds(R.Tok(user, 1, "a")), "seed " + seed + ": the refresh answer is in a stored record after the end");
                Assert.False(store.AnyRecordHolds(R.Tok(user, 0, "a")), "seed " + seed + ": the first grant is in a stored record after the end");
                Assert.Equal(trigger == 2 ? 1 : 0, store.Count);
                Assert.Single(events, e => e.Kind == SessionEventKind.SignedOut && e.SessionId == oldId);
            }

            if (moment == 0)
            {
                await R.Eventually(() => R.AllZero(answer!.AccessBytes) && R.AllZero(answer.RenewalBytes), "seed " + seed + " answer disposed");
                Assert.DoesNotContain(events, e => e.Kind == SessionEventKind.NewToken);
            }

            if (trigger == 2)
            {
                using var t2 = await broker.GetTokenAsync(new SessionKey(key.DeviceSerial, SessionPlatform.Oxpd2, "ps2-" + seed), R.Ct);
                Assert.True(R.Tag(t2.AsSpan()).User == newUser, "seed " + seed + ": the new session's token is not its own");
            }

            broker.Dispose();
        }

        R.Note("S03 runs " + runs + " " + string.Join(" ", outcomes.OrderBy(k => k.Key, StringComparer.Ordinal).Select(k => k.Key + "=" + k.Value)));
    }

    // ---------- F09 over the REAL secret store: raw files after an end during a refresh ----------
    [Fact]
    public async Task S04_end_during_refresh_over_the_real_store_leaves_no_byte_of_either_grant_in_any_file()
    {
        for (var seed = 1; seed <= 24; seed++)
        {
            using var root = new StoreRoot();
            using var secrets = root.Open();
            var store = new SecretStoreSessionRecordStore(secrets);
            var clock = new RClock();
            var refresher = new CountingRefresher();
            var gate = new TaskCompletionSource(TaskCreationOptions.RunContinuationsAsynchronously);
            var user = "user" + seed.ToString("D5") + "@example.test";
            refresher.Behaviour = async (s, subject, ct) =>
            {
                await gate.Task.ConfigureAwait(false);
                return R.Grant(user, 1, clock.GetUtcNow() + TimeSpan.FromHours(1), subject);
            };
            using var broker = new TokenBroker(new TokenBrokerOptions(), store, refresher, clock);
            var key = new SessionKey("SER" + seed, SessionPlatform.Oxpd1, "ps" + seed);
            SignInResult signed;
            using (var g = R.Grant(user, 0, clock.GetUtcNow() + TimeSpan.FromHours(1)))
            {
                signed = broker.SignIn(key, user, TimeSpan.FromHours(1), g);
            }

            var wait = broker.GetNewTokenAsync(key, R.Ct);
            if (seed % 2 == 0)
            {
                broker.SignOut(key);
                gate.TrySetResult();
            }
            else
            {
                R.OnThreads(2, t =>
                {
                    if (t == 0)
                    {
                        gate.TrySetResult();
                    }
                    else
                    {
                        broker.SignOut(signed.Handle!.Value, key.DeviceSerial);
                    }
                });
            }

            var done = wait.ContinueWith(_ => { }, R.Ct, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default);
            Assert.True(await R.Within(done, TimeSpan.FromSeconds(10)));
            await Task.Delay(20, R.Ct);
            Assert.DoesNotContain(secrets.ListNames(), e => e.Name.StartsWith("sessions/", StringComparison.Ordinal));
            foreach (var needle in new[] { R.Tok(user, 0, "a"), R.Tok(user, 0, "r"), R.Tok(user, 1, "a"), R.Tok(user, 1, "r"), Encoding.UTF8.GetBytes(user), Encoding.ASCII.GetBytes(signed.Handle!.Value.Value) })
            {
                foreach (var form in new[] { needle, Encoding.ASCII.GetBytes(Convert.ToBase64String(needle)), Encoding.ASCII.GetBytes(Convert.ToHexString(needle)), Encoding.ASCII.GetBytes(Convert.ToHexString(needle).ToLowerInvariant()) })
                {
                    if (Directory.Exists(root.Root))
                    {
                        foreach (var file in Directory.EnumerateFiles(root.Root, "*", SearchOption.AllDirectories))
                        {
                            Assert.True(File.ReadAllBytes(file).AsSpan().IndexOf(form) < 0, "seed " + seed + ": a grant byte found in a store file");
                        }
                    }
                }
            }
        }
    }

    // ---------- the bound: a refresher whose synchronous part blocks ----------
    [Fact]
    public async Task S05_a_refresher_that_blocks_before_returning_its_task_is_still_bounded_by_RefreshTimeout()
    {
        var clock = new RClock();
        var refresher = new SyncBlockingRefresher { Make = s => R.Grant(s, 1, clock.GetUtcNow() + TimeSpan.FromHours(1), s) };
        var store = new LogStore();
        using var broker = new TokenBroker(new TokenBrokerOptions(), store, refresher, clock);
        var key = new SessionKey("SERBLOCK", SessionPlatform.Oxpd2, "psblock");
        using (var g = R.Grant("userblock@example.test", 0, clock.GetUtcNow() + TimeSpan.FromHours(1)))
        {
            broker.SignIn(key, "userblock@example.test", TimeSpan.FromHours(1), g);
        }

        var first = Task.Run(() => broker.GetNewTokenAsync(key, R.Ct), R.Ct);
        Assert.True(refresher.Entered.Wait(TimeSpan.FromSeconds(5), R.Ct));
        var second = broker.GetNewTokenAsync(key, R.Ct);
        var timersBeforeAdvance = clock.Timers;
        clock.Advance(TimeSpan.FromSeconds(31));
        var bounded = await R.Within(Task.WhenAll(first.ContinueWith(_ => { }, R.Ct, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default), second.ContinueWith(_ => { }, R.Ct, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default)), TimeSpan.FromSeconds(3));
        refresher.Release.Set();
        await R.Within(Task.WhenAll(first.ContinueWith(_ => { }, R.Ct, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default), second.ContinueWith(_ => { }, R.Ct, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default)), TimeSpan.FromSeconds(10));
        R.Note("S05 timers before the advance " + timersBeforeAdvance + "; bounded " + bounded);
        Assert.True(bounded, "S05: with the clock 31 s past the call, both callers still waited 3 s real on a refresher blocking in its synchronous part (timers armed before the advance: " + timersBeforeAdvance + ")");
    }

    [Fact]
    public async Task S06_the_same_block_on_the_real_clock_a_200_ms_bound_against_a_2_s_block()
    {
        var refresher = new SyncBlockingRefresher { MaxBlock = TimeSpan.FromSeconds(2), Make = s => R.Grant(s, 1, DateTimeOffset.UtcNow + TimeSpan.FromHours(1), s) };
        var store = new LogStore();
        using var broker = new TokenBroker(new TokenBrokerOptions { RefreshTimeout = TimeSpan.FromMilliseconds(200) }, store, refresher, TimeProvider.System);
        var key = new SessionKey("SERREAL", SessionPlatform.Oxpd2, "psreal");
        using (var g = R.Grant("userreal@example.test", 0, DateTimeOffset.UtcNow + TimeSpan.FromHours(1)))
        {
            broker.SignIn(key, "userreal@example.test", TimeSpan.FromHours(1), g);
        }

        var sw = Stopwatch.StartNew();
        var call = Task.Run(() => broker.GetNewTokenAsync(key, R.Ct), R.Ct);
        await R.Within(call.ContinueWith(_ => { }, R.Ct, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default), TimeSpan.FromSeconds(10));
        var elapsed = sw.Elapsed;
        R.Note("S06 elapsed ms " + (long)elapsed.TotalMilliseconds + " outcome " + call.Status);
        Assert.True(elapsed < TimeSpan.FromMilliseconds(1500), "S06: a 200 ms bound took " + (long)elapsed.TotalMilliseconds + " ms");
    }

    [Fact]
    public async Task S07_control_an_async_hang_on_the_real_clock_is_bounded_near_200_ms()
    {
        var refresher = new CountingRefresher
        {
            Behaviour = async (_, _, _) =>
            {
                await Task.Delay(TimeSpan.FromSeconds(2), R.Ct).ConfigureAwait(false);
                throw new InvalidOperationException("late");
            },
        };
        using var broker = new TokenBroker(new TokenBrokerOptions { RefreshTimeout = TimeSpan.FromMilliseconds(200) }, new LogStore(), refresher, TimeProvider.System);
        var key = new SessionKey("SERCTL", SessionPlatform.Oxpd2, "psctl");
        using (var g = R.Grant("userctl@example.test", 0, DateTimeOffset.UtcNow + TimeSpan.FromHours(1)))
        {
            broker.SignIn(key, "userctl@example.test", TimeSpan.FromHours(1), g);
        }

        var sw = Stopwatch.StartNew();
        var ex = await Assert.ThrowsAsync<TokenBrokerException>(() => broker.GetNewTokenAsync(key, R.Ct));
        Assert.Equal(TokenBrokerError.RefreshTimedOut, ex.Reason);
        Assert.True(sw.Elapsed < TimeSpan.FromMilliseconds(1500), "S07 control: " + (long)sw.Elapsed.TotalMilliseconds + " ms");
    }

    // ---------- the bound with 1000 waiters, and the callers' own cancellation ----------
    [Fact]
    public async Task S08_one_thousand_waiters_on_a_refresher_that_ignores_cancellation_all_end_at_the_bound()
    {
        for (var seed = 1; seed <= 6; seed++)
        {
            var clock = new RClock();
            var never = new TaskCompletionSource<TokenGrant>(TaskCreationOptions.RunContinuationsAsynchronously);
            var refresher = new CountingRefresher { Behaviour = (_, _, _) => never.Task };
            using var broker = new TokenBroker(new TokenBrokerOptions(), new LogStore(), refresher, clock);
            var key = new SessionKey("SER" + seed, SessionPlatform.Oxpd2, "ps" + seed);
            using (var g = R.Grant("user@example.test", 0, clock.GetUtcNow() + TimeSpan.FromHours(1)))
            {
                broker.SignIn(key, "user@example.test", TimeSpan.FromHours(1), g);
            }

            using var cancelSome = CancellationTokenSource.CreateLinkedTokenSource(R.Ct);
            var calls = new Task<AccessToken>[1000];
            R.OnThreads(8, t =>
            {
                for (var i = t; i < 1000; i += 8)
                {
                    calls[i] = i % 10 == 0 ? broker.GetNewTokenAsync(key, cancelSome.Token) : broker.GetNewTokenAsync(key, R.Ct);
                }
            });
            await R.Eventually(() => refresher.Calls >= 1, "seed " + seed + " call entered");
            Assert.Equal(1, refresher.Calls);
            cancelSome.Cancel();
            Assert.True(await R.Within(Task.WhenAll(calls.Where((_, i) => i % 10 == 0).Select(c => c.ContinueWith(_ => { }, R.Ct, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default))), TimeSpan.FromSeconds(5)), "cancelled callers did not return");
            Assert.All(calls.Where((_, i) => i % 10 == 0), c => Assert.True(c.IsCanceled));
            clock.Advance(seed % 2 == 0 ? TimeSpan.FromSeconds(30) : TimeSpan.FromSeconds(29));
            if (seed % 2 == 1)
            {
                await Task.Delay(50, R.Ct);
                Assert.True(calls.Where((_, i) => i % 10 != 0).All(c => !c.IsCompleted), "a caller ended before the bound");
                clock.Advance(TimeSpan.FromSeconds(1));
            }

            Assert.True(await R.Within(Task.WhenAll(calls.Where((_, i) => i % 10 != 0).Select(c => c.ContinueWith(_ => { }, R.Ct, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default))), TimeSpan.FromSeconds(10)), "waiters hung past the bound");
            foreach (var c in calls.Where((_, i) => i % 10 != 0))
            {
                Assert.Equal(TokenBrokerError.RefreshTimedOut, Assert.IsType<TokenBrokerException>(c.Exception!.InnerException).Reason);
            }

            never.TrySetResult(R.Grant("user@example.test", 9, clock.GetUtcNow() + TimeSpan.FromHours(1)));
            Assert.Equal(1, refresher.Calls);
        }
    }

    // ---------- D9: subject variants at sign-in and in a refresh answer ----------
    [Fact]
    public async Task S09_subject_variants_never_hand_out_and_never_throw_untyped()
    {
        const string baseUser = "user0042.eé@example.test";
        var variants = new List<string>
        {
            baseUser.ToUpperInvariant(),
            "U" + baseUser.Substring(1),
            baseUser + " ",
            " " + baseUser,
            baseUser + " ",
            baseUser.Insert(4, "‍"),
            baseUser.Replace("eé", "еé", StringComparison.Ordinal),
            baseUser.Replace("é", "é", StringComparison.Ordinal),
            baseUser + "\0",
            string.Empty,
            baseUser.Substring(0, baseUser.Length - 1),
            baseUser + "\ud800",
        };
        for (var i = 0; i < baseUser.Length; i++)
        {
            var chars = baseUser.ToCharArray();
            chars[i] = (char)(chars[i] + 1);
            variants.Add(new string(chars));
        }

        var inputs = 0;
        var untyped = new List<string>();
        foreach (var v in variants)
        {
            // sign-in with the variant stated by the grant
            inputs++;
            {
                var clock = new RClock();
                var store = new LogStore();
                using var broker = new TokenBroker(new TokenBrokerOptions(), store, new CountingRefresher(), clock);
                var events = 0;
                broker.SessionEvent += (_, _) => events++;
                using var g = R.Grant(baseUser, 0, clock.GetUtcNow() + TimeSpan.FromHours(1), v);
                var ex = Assert.Throws<TokenBrokerException>(() => broker.SignIn(new SessionKey("SER", SessionPlatform.Oxpd1, "ps"), baseUser, TimeSpan.FromHours(1), g));
                Assert.Equal(TokenBrokerError.SubjectMismatch, ex.Reason);
                Assert.Equal(0, store.Count);
                Assert.Equal(0, events);
            }

            // a refresh answering the variant ends the session
            inputs++;
            {
                var clock = new RClock();
                var store = new LogStore();
                var refresher = new CountingRefresher { Behaviour = (_, _, _) => Task.FromResult(R.Grant(baseUser, 1, clock.GetUtcNow() + TimeSpan.FromHours(1), v)) };
                using var broker = new TokenBroker(new TokenBrokerOptions(), store, refresher, clock);
                var key = new SessionKey("SER", SessionPlatform.Oxpd1, "ps");
                SignInResult s;
                using (var g = R.Grant(baseUser, 0, clock.GetUtcNow() + TimeSpan.FromHours(1)))
                {
                    s = broker.SignIn(key, baseUser, TimeSpan.FromHours(1), g);
                }

                var ex = await Assert.ThrowsAsync<TokenBrokerException>(() => broker.GetNewTokenAsync(s.Handle!.Value, "SER", R.Ct));
                Assert.Equal(TokenBrokerError.SubjectMismatch, ex.Reason);
                Assert.Equal(0, store.Count);
                Assert.Equal(TokenBrokerError.SessionNotFound, (await Assert.ThrowsAsync<TokenBrokerException>(() => broker.GetTokenAsync(key, R.Ct))).Reason);
            }
        }

        // equal on both sides but unusual: a lone surrogate, a 10000-character user, a decomposed form
        foreach (var same in new[] { baseUser + "\ud800", new string('u', 10000) + "@example.test", baseUser.Replace("é", "é", StringComparison.Ordinal) })
        {
            inputs++;
            var clock = new RClock();
            var store = new LogStore();
            using var broker = new TokenBroker(new TokenBrokerOptions(), store, new CountingRefresher(), clock);
            using var g = R.Grant(baseUser, 0, clock.GetUtcNow() + TimeSpan.FromHours(1), same);
            try
            {
                broker.SignIn(new SessionKey("SER", SessionPlatform.Oxpd2, "ps"), same, TimeSpan.FromHours(1), g);
                using var t = await broker.GetTokenAsync(new SessionKey("SER", SessionPlatform.Oxpd2, "ps"), R.Ct);
                broker.Dispose();
                using var again = new TokenBroker(new TokenBrokerOptions(), store, new CountingRefresher(), clock);
                R.Note("S09 equal unusual user (length " + same.Length + ", last U+" + ((int)same[^1]).ToString("X4") + "): signed in and handed out; after a restart restored " + again.LastRestore.Restored + " unreadable " + again.LastRestore.Unreadable);
            }
            catch (TokenBrokerException)
            {
            }
            catch (Exception e)
            {
                untyped.Add(e.GetType().Name + " for a user of length " + same.Length + " ending U+" + ((int)same[^1]).ToString("X4"));
            }
        }

        R.Note("S09 inputs " + inputs + " untyped: " + string.Join("; ", untyped));
        Assert.True(untyped.Count == 0, "S09: an untyped exception left SignIn: " + string.Join("; ", untyped));
    }

    // ---------- D9: every PUBLIC hand-out site checks the subject (U04 reaches only the internal method) ----------
    [Fact]
    public async Task S10_a_held_grant_of_another_subject_is_never_handed_out_by_any_public_path()
    {
        var paths = 0;
        for (var path = 0; path < 6; path++)
        {
            paths++;
            var clock = new RClock();
            var store = new LogStore();
            var gate = new TaskCompletionSource(TaskCreationOptions.RunContinuationsAsynchronously);
            var refresher = new CountingRefresher
            {
                Behaviour = async (_, _, _) =>
                {
                    await gate.Task.ConfigureAwait(false);
                    throw new InvalidOperationException("planted");
                },
            };
            using var broker = new TokenBroker(new TokenBrokerOptions(), store, refresher, clock);
            var key = new SessionKey("SERX", SessionPlatform.Oxpd1, "psx");
            SignInResult s;
            using (var g = R.Grant("usera@example.test", 0, clock.GetUtcNow() + TimeSpan.FromHours(1)))
            {
                s = broker.SignIn(key, "usera@example.test", TimeSpan.FromHours(1), g);
            }

            void Swap()
            {
                var st = broker.StateOf(key)!;
                var old = st.Grant;
                st.Grant = new HeldGrant(R.Tok("userb@example.test", 0, "a"), R.Tok("userb@example.test", 0, "r"), "userb@example.test", old.ExpiresAt, old.ReceiptWall, old.ReceiptTimestamp);
            }

            Task<AccessToken> call;
            switch (path)
            {
                case 0:
                    Swap();
                    call = broker.GetTokenAsync(key, R.Ct);
                    break;
                case 1:
                    Swap();
                    call = broker.GetTokenAsync(s.Handle!.Value, "SERX", R.Ct);
                    break;
                case 2:
                case 3:
                    // inside the margin: the read waits on a failing refresh, then falls back to the held token
                    clock.Advance(TimeSpan.FromMinutes(56));
                    call = path == 2 ? broker.GetTokenAsync(key, R.Ct) : broker.GetTokenAsync(s.Handle!.Value, "SERX", R.Ct);
                    Swap();
                    gate.TrySetResult();
                    break;
                case 4:
                    // a timed-out refresh, then the fallback
                    clock.Advance(TimeSpan.FromMinutes(56));
                    call = broker.GetTokenAsync(key, R.Ct);
                    Swap();
                    clock.Advance(TimeSpan.FromSeconds(31));
                    break;
                default:
                    // an already running refresh joined by a read outside the margin goes the fast path
                    var renew = broker.GetNewTokenAsync(key, R.Ct);
                    Swap();
                    call = broker.GetTokenAsync(key, R.Ct);
                    gate.TrySetResult();
                    await renew.ContinueWith(_ => { }, R.Ct, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default);
                    break;
            }

            var done = await R.Within(call.ContinueWith(_ => { }, R.Ct, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default), TimeSpan.FromSeconds(10));
            Assert.True(done, "path " + path + " hung");
            Assert.False(call.IsCompletedSuccessfully, "path " + path + ": a token was handed out for a held grant of another subject");
            Assert.Equal(TokenBrokerError.SubjectMismatch, Assert.IsType<TokenBrokerException>(call.Exception!.InnerException).Reason);
            Assert.Null(broker.StateOf(key));
            Assert.Equal(0, store.Count);
            gate.TrySetResult();
        }

        R.Note("S10 public hand-out paths " + paths);
    }

    // ---------- D12 with store failures around a refresh ----------
    [Fact]
    public async Task S11_failed_delete_or_failed_write_around_a_refresh_never_writes_an_ended_session()
    {
        for (var mode = 0; mode < 4; mode++)
        {
            var clock = new RClock();
            var store = new LogStore();
            var gate = new TaskCompletionSource(TaskCreationOptions.RunContinuationsAsynchronously);
            var refresher = new CountingRefresher
            {
                Behaviour = async (_, subject, _) =>
                {
                    await gate.Task.ConfigureAwait(false);
                    return R.Grant(subject, 1, clock.GetUtcNow() + TimeSpan.FromHours(1), subject);
                },
            };
            using var broker = new TokenBroker(new TokenBrokerOptions(), store, refresher, clock);
            var key = new SessionKey("SERF", SessionPlatform.Oxpd2, "psf");
            SignInResult s;
            using (var g = R.Grant("userf@example.test", 0, clock.GetUtcNow() + TimeSpan.FromHours(1)))
            {
                s = broker.SignIn(key, "userf@example.test", TimeSpan.FromHours(1), g);
            }

            var wait = broker.GetNewTokenAsync(key, R.Ct);
            if (mode == 0)
            {
                // delete fails at sign-out while the refresh is in flight; the answer arrives
                store.FailDelete = true;
                Assert.Equal(TokenBrokerError.StoreFailed, Assert.Throws<TokenBrokerException>(() => broker.SignOut(key)).Reason);
                gate.TrySetResult();
            }
            else if (mode == 1)
            {
                // the accepted answer's write fails (stale); then sign-out succeeds
                store.FailSave = true;
                gate.TrySetResult();
                using (var t = await wait)
                {
                }

                store.FailSave = false;
                broker.SignOut(key);
            }
            else if (mode == 2)
            {
                // the accepted answer's write fails; a new sign-in on the device ends it
                store.FailSave = true;
                gate.TrySetResult();
                using (var t = await wait)
                {
                }

                store.FailSave = false;
                using var g2 = R.Grant("userg@example.test", 0, clock.GetUtcNow() + TimeSpan.FromHours(1));
                broker.SignIn(new SessionKey("SERF", SessionPlatform.Oxpd2, "psg"), "userg@example.test", TimeSpan.FromHours(1), g2);
            }
            else
            {
                // delete fails at sign-out, the answer arrives, then a new sign-in on the device while delete still fails
                store.FailDelete = true;
                Assert.Throws<TokenBrokerException>(() => broker.SignOut(key));
                gate.TrySetResult();
                using var g2 = R.Grant("userg@example.test", 0, clock.GetUtcNow() + TimeSpan.FromHours(1));
                broker.SignIn(new SessionKey("SERF", SessionPlatform.Oxpd2, "psg"), "userg@example.test", TimeSpan.FromHours(1), g2);
            }

            await wait.ContinueWith(_ => { }, R.Ct, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default);
            await Task.Delay(20, R.Ct);
            store.FailDelete = false;
            store.FailSave = false;
            try
            {
                broker.Sweep();
            }
            catch (TokenBrokerException)
            {
            }

            clock.Advance(TimeSpan.FromMinutes(2));
            try
            {
                broker.Sweep();
            }
            catch (TokenBrokerException)
            {
            }

            Assert.True(store.SavedAfterDelete().Count == 0, "mode " + mode + ": a record was written after its delete");
            Assert.DoesNotContain(s.SessionId, store.ListIds());
            Assert.False(store.AnyRecordHolds(R.Tok("userf@example.test", 1, "a")), "mode " + mode + ": the answer of an ended session is stored");
        }
    }

    // ---------- re-entrancy: the refresher signs the session out from inside its own call ----------
    [Fact]
    public async Task S12_a_refresher_that_signs_the_session_out_from_inside_its_call()
    {
        var clock = new RClock();
        var store = new LogStore();
        TokenBroker? broker = null;
        TokenGrant? answer = null;
        var key = new SessionKey("SERR", SessionPlatform.Oxpd2, "psr");
        var refresher = new CountingRefresher
        {
            Behaviour = (_, subject, _) =>
            {
                broker!.SignOut(key);
                answer = R.Grant(subject, 1, clock.GetUtcNow() + TimeSpan.FromHours(1), subject);
                return Task.FromResult(answer);
            },
        };
        broker = new TokenBroker(new TokenBrokerOptions(), store, refresher, clock);
        using (var g = R.Grant("userr@example.test", 0, clock.GetUtcNow() + TimeSpan.FromHours(1)))
        {
            broker.SignIn(key, "userr@example.test", TimeSpan.FromHours(1), g);
        }

        var call = broker.GetNewTokenAsync(key, R.Ct);
        Assert.True(await R.Within(call.ContinueWith(_ => { }, R.Ct, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default), TimeSpan.FromSeconds(10)));
        Assert.Equal(TokenBrokerError.SessionNotFound, Assert.IsType<TokenBrokerException>(call.Exception!.InnerException).Reason);
        Assert.True(R.AllZero(answer!.AccessBytes));
        Assert.Empty(store.SavedAfterDelete());
        Assert.Equal(0, store.Count);
        broker.Dispose();
    }

    // ---------- MEASURE (not a pass/fail property of the kit): after a timeout, can two refresher calls overlap? ----------
    [Fact]
    public async Task S13_measure_overlap_of_refresher_calls_after_a_timeout_when_the_refresher_ignores_cancellation()
    {
        var clock = new RClock();
        var release = new TaskCompletionSource(TaskCreationOptions.RunContinuationsAsynchronously);
        var refresher = new CountingRefresher
        {
            Behaviour = async (_, subject, _) =>
            {
                await release.Task.ConfigureAwait(false);
                return R.Grant(subject, 1, clock.GetUtcNow() + TimeSpan.FromHours(1), subject);
            },
        };
        using var broker = new TokenBroker(new TokenBrokerOptions(), new LogStore(), refresher, clock);
        var key = new SessionKey("SERO", SessionPlatform.Oxpd2, "pso");
        using (var g = R.Grant("usero@example.test", 0, clock.GetUtcNow() + TimeSpan.FromHours(1)))
        {
            broker.SignIn(key, "usero@example.test", TimeSpan.FromHours(1), g);
        }

        var first = broker.GetNewTokenAsync(key, R.Ct);
        await R.Eventually(() => refresher.Calls == 1 && clock.Timers == 1, "S13 first call entered");
        clock.Advance(TimeSpan.FromSeconds(31));
        await first.ContinueWith(_ => { }, R.Ct, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default);
        var second = broker.GetNewTokenAsync(key, R.Ct);
        await R.Eventually(() => refresher.Calls == 2, "S13 second call entered");
        var overlap = refresher.MaxInFlight;
        release.TrySetResult();
        await R.Within(second.ContinueWith(_ => { }, R.Ct, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default), TimeSpan.FromSeconds(10));
        R.Note("S13 max in-flight refresher calls of one session after a timeout: " + overlap);
        Assert.Equal(2, overlap);
    }

    // ================= round-2 delta probes (D20 and D23) =================
    private sealed class CountingSyncBlocker : ITokenRefresher
    {
        private int _calls;

        internal int Calls => Volatile.Read(ref _calls);

        internal ManualResetEventSlim Release { get; } = new();

        internal volatile bool RenewalAllZeroAtEntry;

        internal volatile bool CancelledAtEntry;

        internal Func<string, TokenGrant>? Make { get; set; }

        internal TokenGrant? Last { get; private set; }

        public Task<TokenGrant> RefreshAsync(SessionKey session, ReadOnlyMemory<byte> renewalState, string subject, CancellationToken cancellationToken)
        {
            Interlocked.Increment(ref _calls);
            RenewalAllZeroAtEntry = renewalState.Span.IndexOfAnyExcept((byte)0) < 0;
            CancelledAtEntry = cancellationToken.IsCancellationRequested;
            Release.Wait(TimeSpan.FromSeconds(8));
            Last = Make!(subject);
            return Task.FromResult(Last);
        }
    }

    [Fact]
    public async Task S14_one_thousand_callers_on_a_refresher_that_blocks_before_returning_all_end_at_the_bound()
    {
        var callers = 0;
        for (var seed = 1; seed <= 6; seed++)
        {
            var clock = new RClock();
            var user = "blk" + seed.ToString("D3") + "@example.test";
            var refresher = new CountingSyncBlocker { Make = s => R.Grant(user, 1, clock.GetUtcNow() + TimeSpan.FromHours(1), s) };
            var store = new LogStore();
            using var broker = new TokenBroker(new TokenBrokerOptions(), store, refresher, clock);
            var events = new ConcurrentQueue<SessionEventArgs>();
            broker.SessionEvent += (_, e) => events.Enqueue(e);
            var key = new SessionKey("SERB" + seed, SessionPlatform.Oxpd1, "psb" + seed);
            SignInResult signed;
            using (var g = R.Grant(user, 0, clock.GetUtcNow() + TimeSpan.FromHours(1)))
            {
                signed = broker.SignIn(key, user, TimeSpan.FromHours(1), g);
            }

            var calls = new Task<AccessToken>[1000];
            R.OnThreads(8, t =>
            {
                for (var i = t; i < 1000; i += 8)
                {
                    calls[i] = i % 2 == 0 ? R.Safe(() => broker.GetNewTokenAsync(key, R.Ct)) : R.Safe(() => broker.GetNewTokenAsync(signed.Handle!.Value, key.DeviceSerial, R.Ct));
                }
            });
            callers += calls.Length;
            await R.Eventually(() => refresher.Calls == 1 && clock.Timers == 1, "S14 seed " + seed + " call entered and bound armed");
            clock.Advance(seed % 2 == 0 ? TimeSpan.FromSeconds(30) : TimeSpan.FromSeconds(29));
            if (seed % 2 == 1)
            {
                await Task.Delay(50, R.Ct);
                Assert.True(calls.All(c => !c.IsCompleted), "S14 seed " + seed + ": a caller ended before the bound");
                clock.Advance(TimeSpan.FromSeconds(1));
            }

            Assert.True(await R.Within(Task.WhenAll(calls.Select(c => c.ContinueWith(_ => { }, R.Ct, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default))), TimeSpan.FromSeconds(3)), "S14 seed " + seed + ": callers waited past the bound while the refresher blocked");
            foreach (var c in calls)
            {
                var tbe = Assert.IsType<TokenBrokerException>(c.Exception!.InnerException);
                Assert.Equal(TokenBrokerError.RefreshTimedOut, tbe.Reason);
                Assert.Null(tbe.InnerException);
            }

            Assert.Equal(1, refresher.Calls);
            refresher.Release.Set();
            await R.Eventually(() => refresher.Last is not null && R.AllZero(refresher.Last.AccessBytes) && R.AllZero(refresher.Last.RenewalBytes), "S14 seed " + seed + " late answer disposed");
            Assert.False(store.AnyRecordHolds(R.Tok(user, 1, "a")), "S14 seed " + seed + ": late answer stored");
            Assert.DoesNotContain(events, e => e.Kind == SessionEventKind.NewToken);
            using (var held = await broker.GetTokenAsync(key, R.Ct))
            {
                Assert.True(R.Tag(held.AsSpan()) == (user, 0), "S14 seed " + seed + ": the held token changed");
            }

            Assert.Equal(1, refresher.Calls);
        }

        R.Note("S14 seeds 6 callers " + callers);
    }

    [Fact]
    public async Task S15_measure_a_refresh_that_times_out_before_the_pool_starts_the_refresher()
    {
        // Saturate the thread pool so the refresher's call is queued, not run, then pass the bound on the test clock.
        var clock = new RClock();
        var user = "pool@example.test";
        var refresher = new CountingSyncBlocker { Make = s => R.Grant(user, 1, clock.GetUtcNow() + TimeSpan.FromHours(1), s) };
        refresher.Release.Set();
        var store = new LogStore();
        using var broker = new TokenBroker(new TokenBrokerOptions(), store, refresher, clock);
        var events = new ConcurrentQueue<SessionEventArgs>();
        broker.SessionEvent += (_, e) => events.Enqueue(e);
        var key = new SessionKey("SERP", SessionPlatform.Oxpd2, "psp");
        using (var g = R.Grant(user, 0, clock.GetUtcNow() + TimeSpan.FromHours(1)))
        {
            broker.SignIn(key, user, TimeSpan.FromHours(1), g);
        }

        var hold = new ManualResetEventSlim();
        var started = 0;
        var queued = 0;
        var saturated = false;
        var sw = Stopwatch.StartNew();
        while (sw.Elapsed < TimeSpan.FromSeconds(5))
        {
            ThreadPool.UnsafeQueueUserWorkItem(_ => { Interlocked.Increment(ref started); while (!hold.IsSet) { Thread.Sleep(1); } }, null);
            queued++;
            Thread.Sleep(2);
            if (ThreadPool.PendingWorkItemCount >= 4 && Volatile.Read(ref started) <= queued - 4)
            {
                saturated = true;
                break;
            }
        }

        int callsAtBound;
        Task<AccessToken> call;
        try
        {
            call = broker.GetNewTokenAsync(key, R.Ct);
            var timers = clock.Timers;
            clock.Advance(TimeSpan.FromSeconds(31));
            callsAtBound = refresher.Calls;
            R.Note("S15 saturated " + saturated + " timers armed before the advance " + timers + " refresher calls at the bound " + callsAtBound);
        }
        finally
        {
            hold.Set();
        }

        Assert.True(await R.Within(call.ContinueWith(_ => { }, R.Ct, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default), TimeSpan.FromSeconds(10)));
        Assert.Equal(TokenBrokerError.RefreshTimedOut, Assert.IsType<TokenBrokerException>(call.Exception!.InnerException).Reason);
        await R.Eventually(() => refresher.Calls == 1 && refresher.Last is not null, "S15 the queued call ran");
        await R.Eventually(() => R.AllZero(refresher.Last!.AccessBytes), "S15 late answer disposed");
        R.Note("S15 the refresher ran after the bound: " + (callsAtBound == 0) + "; its token was cancelled at entry: " + refresher.CancelledAtEntry + "; the renewal state it received read all zero: " + refresher.RenewalAllZeroAtEntry);
        Assert.False(store.AnyRecordHolds(R.Tok(user, 1, "a")));
        Assert.DoesNotContain(events, e => e.Kind == SessionEventKind.NewToken);
        using var held = await broker.GetTokenAsync(key, R.Ct);
        Assert.True(R.Tag(held.AsSpan()) == (user, 0));
    }

    [Fact]
    public async Task S16_an_idle_deadline_passing_during_a_refresh_hands_out_nothing_for_any_outcome_and_any_joiner()
    {
        var tally = new ConcurrentDictionary<string, int>();
        for (var seed = 1; seed <= 160; seed++)
        {
            var rng = new Random(1000 + seed);
            var outcome = seed % 4; // 0 accept, 1 throw, 2 null answer, 3 hang past the bound
            var touched = (seed / 4) % 2 == 1; // a Touch at +5 s keeps the session alive
            var clock = new RClock();
            var store = new LogStore();
            var gate = new TaskCompletionSource(TaskCreationOptions.RunContinuationsAsynchronously);
            var user = "idle" + seed.ToString("D4") + "@example.test";
            TokenGrant? answer = null;
            var refresher = new CountingRefresher
            {
                Behaviour = async (_, subject, ct) =>
                {
                    if (outcome == 3)
                    {
                        await Task.Delay(Timeout.InfiniteTimeSpan, ct).ConfigureAwait(false);
                    }

                    await gate.Task.ConfigureAwait(false);
                    if (outcome == 1)
                    {
                        throw new InvalidOperationException("synthetic failure");
                    }

                    if (outcome == 2)
                    {
                        return null!;
                    }

                    answer = R.Grant(user, 1, clock.GetUtcNow() + TimeSpan.FromHours(1), subject);
                    return answer;
                },
            };
            using var broker = new TokenBroker(new TokenBrokerOptions(), store, refresher, clock);
            var events = new ConcurrentQueue<SessionEventArgs>();
            broker.SessionEvent += (_, e) => events.Enqueue(e);
            var key = new SessionKey("SERI" + seed, SessionPlatform.Oxpd1, "psi" + seed);
            SignInResult signed;
            using (var g = R.Grant(user, 0, clock.GetUtcNow() + TimeSpan.FromSeconds(90)))
            {
                signed = broker.SignIn(key, user, TimeSpan.FromSeconds(outcome == 3 ? 40 : 10), g);
            }

            var n = 1 + rng.Next(0, 50);
            var waits = new List<Task<AccessToken>>();
            var kinds = new List<int>();
            for (var j = 0; j < n; j++)
            {
                var k = rng.Next(4);
                kinds.Add(k);
                waits.Add(k switch
                {
                    0 => R.Safe(() => broker.GetTokenAsync(key, R.Ct)),
                    1 => R.Safe(() => broker.GetTokenAsync(signed.Handle!.Value, key.DeviceSerial, R.Ct)),
                    2 => R.Safe(() => broker.GetNewTokenAsync(key, R.Ct)),
                    _ => R.Safe(() => broker.GetNewTokenAsync(signed.Handle!.Value, key.DeviceSerial, R.Ct)),
                });
            }

            await R.Eventually(() => refresher.Calls == 1 && clock.Timers == 1, "S16 seed " + seed + " call entered");
            if (touched)
            {
                clock.Advance(TimeSpan.FromSeconds(5));
                broker.Touch(key);
            }

            // idle 10 s (40 s for the hang row); the hang row passes the 30 s bound and its 40 s idle deadline together
            clock.Advance(outcome == 3 ? TimeSpan.FromSeconds(touched ? 36 : 41) : TimeSpan.FromSeconds(touched ? 6 : 11));
            gate.TrySetResult();
            Assert.True(await R.Within(Task.WhenAll(waits.Select(w => w.ContinueWith(_ => { }, R.Ct, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default))), TimeSpan.FromSeconds(10)), "S16 seed " + seed + ": waiters hung");
            var handed = 0;
            for (var j = 0; j < n; j++)
            {
                var w = waits[j];
                string label;
                if (w.IsCompletedSuccessfully)
                {
                    using var token = await w;
                    Assert.True(touched, "S16 seed " + seed + ": a token was handed out after the idle deadline passed during the refresh");
                    Assert.True(R.Tag(token.AsSpan()).User == user, "S16 seed " + seed + ": wrong user");
                    handed++;
                    label = "token";
                }
                else
                {
                    var tbe = Assert.IsType<TokenBrokerException>(w.Exception!.InnerException);
                    Assert.Null(tbe.InnerException);
                    if (!touched)
                    {
                        Assert.True(tbe.Reason is TokenBrokerError.SessionExpired or TokenBrokerError.SessionNotFound, "S16 seed " + seed + ": reason " + tbe.Reason);
                    }

                    label = tbe.Reason.ToString();
                }

                tally.AddOrUpdate("o" + outcome + (touched ? "touched" : "idle") + ":" + label, 1, (_, v) => v + 1);
            }

            Assert.Equal(1, refresher.Calls);
            Assert.Empty(store.SavedAfterDelete());
            var expiredEvents = events.Count(e => e.Kind == SessionEventKind.SignedOut && e.Reason == SignOutReason.Expired);
            if (!touched)
            {
                Assert.Equal(1, expiredEvents);
                Assert.Equal(0, store.Count);
                Assert.False(store.AnyRecordHolds(R.Tok(user, 0, "a")), "S16 seed " + seed + ": the first grant is left in a record");
                Assert.False(store.AnyRecordHolds(R.Tok(user, 1, "a")), "S16 seed " + seed + ": the answer is left in a record");
                if (answer is not null)
                {
                    await R.Eventually(() => R.AllZero(answer.AccessBytes), "S16 seed " + seed + " answer cleared");
                }

                var after = await Assert.ThrowsAsync<TokenBrokerException>(() => broker.GetTokenAsync(key, R.Ct));
                Assert.Equal(TokenBrokerError.SessionNotFound, after.Reason);
            }
            else
            {
                Assert.Equal(0, expiredEvents);
                Assert.Equal(1, store.Count);
                if (outcome == 0)
                {
                    Assert.Equal(n, handed);
                }
            }
        }

        R.Note("S16 runs 160 " + string.Join(" ", tally.OrderBy(k => k.Key, StringComparer.Ordinal).Select(k => k.Key + "=" + k.Value)));
    }
}
