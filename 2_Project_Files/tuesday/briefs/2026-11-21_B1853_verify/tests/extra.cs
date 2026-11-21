
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
