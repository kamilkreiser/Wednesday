## What this adds

One commit: a new library `src/Datasec.Suite.Sessions` (the session and token broker, component C6, work package
WP1.5), its test project `tests/Datasec.Suite.Sessions.Tests` (53 tests), and two lines of `Datasec.Suite.slnx`. No
package, no workflow line, no build file, and no file of the secret store changes.

## What the broker does

- **Holds and hands out tokens another component obtained.** A caller signs a session in with a key (device serial,
  platform, platform session id), the session user, an idle timeout and a grant (access token bytes, renewal state
  bytes, the subject the grant states, the stated expiry). The broker copies the bytes and hands out a copy of the
  access token to a caller that names a live session of that device.
- **One live session per device.** A new sign-in on a device ends the earlier session and erases its record.
- **OXPd 1.x handles.** An OXPd 1.x session gets a 32-byte random handle (43 characters of base64url). Only its SHA-256
  is kept; a lookup by handle also needs the device serial beside it. Every failed lookup is the same refusal.
- **Refresh only through `ITokenRefresher`.** A read inside the refresh margin (5 minutes on either clock) and every
  `GetNewTokenAsync` call the refresher; one call per session at a time, bounded by 30 seconds on the broker's
  `TimeProvider`. An answer is kept only when it is a non-empty grant within the size cap, not expired on either
  clock, and for the same subject; an answer of another subject ends the session.
- **The subject check on every hand-out.** Every token that leaves goes through one method that compares the grant's
  stated subject with the session user, ordinally.
- **Expiry on two clocks.** Every deadline is held on the wall clock and the monotonic clock and passes when either
  says so. Inactivity, sign-out, a new sign-in and a restart past 10 minutes end a session; `Sweep()` ends idle
  sessions no call names.
- **Records only through the secret store.** Each live session has one record, encrypted by `ISecretStore`, under the
  name `sessions/<32 random hex>`. It is written at sign-in, at an accepted refresh and at most once a minute on
  activity, and erased when the session ends. The constructor restores the records inside the restart window and
  deletes the rest.
- **Nothing prints a secret.** Every public type prints a fixed mask; the one exception type carries a reason and a
  fixed message, no inner exception. Disposal clears the arrays it holds.

## What it does NOT do

- **No sign-in flow and no Microsoft code.** Signing in and the real refresher belong to another work package; the
  only refresher here is a test fake.
- **No token reading.** The broker never decodes, parses, inspects, alters or mints a token. The subject it compares
  is the one the grant states, so a caller that states the wrong subject for a token is not caught here.
- **No host wiring.** The server does not reference the library (the release guard counts did not move), and nothing
  calls `Sweep()` yet: the host must call it at least as often as the shortest idle timeout.
- **No timer and no background thread** in the library; expiry is enforced at each call and by `Sweep()`.

## Limits, stated

- One unreadable record of any name in the broker's partition stops the broker from starting (`StoreFailed` from the
  constructor) and changes nothing, because the secret store's listing refuses as a whole and gives no name to delete.
  The way out today is moving the partition's records folder aside, which ends every session. A listing in the secret
  store that also names records that do not open is owed work on `Datasec.Suite.Secrets`.
- A record whose delete keeps failing, followed by a restart inside the window, brings that session back for at most
  the window.
- A refresher that blocks its calling thread before it returns its task is not bounded by the 30 seconds: the bound
  applies to the task it returns.
- Across a restart only the wall clock exists: a wall clock set back while the server runs, followed by a restart
  inside the window, can restore a session with more idle time left than it really has (at most its idle timeout).
- A caller that turns the token bytes into a string makes a copy nobody can clear.
- One process per secret-store partition at a time.

## Checks

- Locally (closed proxy, locked restore, audit off): build 0 warnings, 0 errors; whole suite total 947, failed 0
  (894 on main plus 53).
- Hosted push run of the head: linux and windows total 947, failed 0 (skipped 4 and 19, the secret store's
  platform-only tests); rules `RULES: clean (325 files)`, 53 unit tests at the floor; secret scan with both planted
  controls and `no leaks found`.
- Code scanning runs on this pull request.

Nothing is deployed and nothing was sent anywhere.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
