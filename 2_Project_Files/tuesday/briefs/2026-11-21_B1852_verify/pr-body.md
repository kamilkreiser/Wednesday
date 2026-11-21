## What this adds

Two commits on one branch: a new library `src/Datasec.Suite.Sessions` (the session and token broker, component C6,
work package WP1.5), its test project `tests/Datasec.Suite.Sessions.Tests` (74 tests), and two lines of
`Datasec.Suite.slnx`. The first commit adds the broker; the second bounds a refresher that blocks before it returns,
checks idle again after a refresh, clears every record buffer the writer outgrows, removes an unused sign-out reason,
adds cells for rules that had none, and states the limits that stay open. No package, no workflow line, no build file
and no file of the secret store changes. The squash lands them as one commit.

## What the broker does

- **Holds and hands out tokens another component obtained.** A caller signs a session in with a key (device serial,
  platform, platform session id), the session user, an idle timeout and a grant (access token bytes, renewal state
  bytes, the subject the grant states, the stated expiry). The broker copies the bytes and hands out a copy of the
  access token to a caller that names a live session of that device.
- **One live session per device.** A new sign-in on a device ends the earlier session and erases its record.
- **OXPd 1.x handles.** An OXPd 1.x session gets a 32-byte random handle (43 characters of base64url). Only its SHA-256
  is kept; a lookup by handle also needs the device serial beside it. Every failed lookup is the same refusal.
- **Refresh only through `ITokenRefresher`, bounded.** A read inside the refresh margin (5 minutes on either clock) and
  every `GetNewTokenAsync` call the refresher; one call per session at a time. The call is started on the thread pool,
  so the 30-second bound on the broker's `TimeProvider` covers the whole call, also a refresher that blocks before it
  returns its task. An answer is kept only when it is a non-empty grant within the size cap, not expired on either
  clock, and for the same subject; an answer of another subject ends the session and is never written or announced.
- **Idle is checked again after a refresh.** A session whose idle deadline passed while its refresh ran ends
  (`SessionExpired`) and hands out nothing.
- **The subject check on every hand-out.** Every token that leaves goes through one method that compares the grant's
  stated subject with the session user, ordinally.
- **Expiry on two clocks.** Every deadline is held on the wall clock and the monotonic clock and passes when either
  says so. Inactivity, sign-out, a new sign-in and a restart past 10 minutes end a session; `Sweep()` ends idle
  sessions no call names. Sign-out events carry one of four reasons: `SignOut`, `NewSignIn`, `Expired`,
  `SubjectMismatch`.
- **Records only through the secret store.** Each live session has one record, encrypted by `ISecretStore`, under the
  name `sessions/<32 random hex>`. It is written at sign-in, at an accepted refresh and at most once a minute on
  activity, and erased when the session ends. The constructor restores the records whose idle time is less than both
  the session's idle timeout and the restart window, and deletes the rest. The record writer clears every buffer it
  outgrows.
- **Nothing prints a secret.** Every public type prints a fixed mask; the one exception type carries a reason and a
  fixed message, no inner exception. Disposal clears the arrays it holds.

## What it does NOT do

- **No sign-in flow and no Microsoft code.** Signing in and the real refresher belong to another work package; the
  only refreshers here are test fakes.
- **No token reading.** The broker never decodes, parses, inspects, alters or mints a token. The subject it compares
  is the one the grant states, so a caller that states the wrong subject for a token is not caught here.
- **The host does not use the broker yet.** The server does not reference the library (the release guard counts did
  not move), and nothing calls `Sweep()` yet: the host must call it at least as often as the shortest idle timeout.
- **No timer and no background thread of its own.** Expiry is enforced at each call and by `Sweep()`; the one use of
  the thread pool is the start of each refresher call.

## Limits, stated

- **After a time-out, a second call can overlap the first.** One refresh per session holds within the 30-second bound.
  A refresher that ignores cancellation can still be running when the next refresh of that session starts a second
  call: at most one more call starts per bound per session. The late answer is disposed, never stored and never
  announced. The next call receives the held renewal state, so a renewal state the late call rotated is lost; whether
  a provider's older renewal state then stops working is unmeasured.
- **A refresher that blocks past the bound keeps its pool thread** until it returns: the bound frees the callers, not
  that thread. Every refresh costs one hop to the thread pool.
- **A wall clock set back before a restart.** A wall clock set back while the server runs, followed by a restart inside
  the restart window, restores a session with more idle time than it really has: at most the size of the step, never
  more than its idle timeout from its last recorded activity by the wall clock, and only for a step smaller than the
  time since the record was last written; a larger step drops the record at restart.
- **A blocking event handler blocks the callers of that refresh.** `NewToken` is raised before the callers waiting on
  the refresh are released.
- **Unreadable records stop the start.** One unreadable record of any name in the broker's partition stops the broker
  from starting (`StoreFailed` from the constructor) and changes nothing, because the secret store's listing refuses
  as a whole and gives no name to delete. The way out today is moving the partition's records folder aside, which ends
  every session. A listing in the secret store that also names records that do not open is owed work on
  `Datasec.Suite.Secrets`.
- **A record-store read that fails at restart erases every record it hits:** a transient read error at start ends
  those sessions.
- A record whose delete keeps failing, followed by a restart inside the window, brings that session back for at most
  the window.
- A caller that turns the token bytes into a string makes a copy nobody can clear.
- One process per secret-store partition at a time.

## Checks

- Locally (closed proxy, locked restore, audit off): build 0 warnings, 0 errors; whole suite total 968, failed 0
  (894 of the branch's base plus 74). The merge with the current main, built and run locally: total 973, failed 0
  (899 plus 74); the repository rules clean (329 files) and the build tests 60 of 60.
- Hosted push run of the head: linux and windows total 968, failed 0 (skipped 4 and 19, the secret store's
  platform-only tests); rules `RULES: clean (327 files)`; secret scan with both planted controls and
  `no leaks found`.
- Code scanning runs on this pull request.

Nothing is deployed and nothing was sent anywhere.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
