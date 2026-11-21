# FOR RECORDS: second reader B1839 (token broker lane, round 1)

Decided by nobody; each item is for Tuesday to route.

1. **Fix round (finding 1, Major):** the bound of D5 must cover the refresher's synchronous part. The fix shape probed: `Task.Run` around the refresher call. A cell is needed for a refresher that blocks before it returns its task. F09's immediate `Calls == 1` assertion must become an eventual wait. Alternative (Tuesday's call): put "must not block before returning" into the `ITokenRefresher` contract for WP1.4 and name it as a limit. Cost of the alternative: the broker's property then rests on another component.
2. **Test holes (findings 2 and 3):** add a cell for the waiter's still-current re-check. U03 should also assert no `NewToken` event and no store write of another subject's answer.
3. **README `## Limits` lines owed:**
   - single-flight holds only within `RefreshTimeout`: a refresher that ignores cancellation can overlap with the next call of the same session (measured, 2 in flight)
   - a blocking `SessionEvent` handler blocks the callers of that refresh
4. **For Tuesday (D10 by TIME, reader B1838's item):** should a waiter re-check idle after a long refresh? Today, a token is handed out and activity renewed after the idle deadline passed during the refresh (measured in the race runs).
5. **WP1.4 question (UNMEASURED):** can the Microsoft-library refresher block before its first await (for example, a token cache's synchronous hooks)? This sets how urgent item 1 is in practice.
6. My adversarial tests are kept at `tests/B1839AdversarialTests.cs` beside this file, never in the project. A fix round may copy any of them into the lane as cells.
