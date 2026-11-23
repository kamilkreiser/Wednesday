# FOR RECORDS: Server host composition v0 (lane H, kit B1974, seat X48), gate G1 round 1 of 2 of lane H, reader B1981

Not repository text. For the next OXPd records pass; nothing here was written into the project. No person is named.
Who decided: the coordinator (Tuesday), as coordinator: this lane's widening beyond the twelve packages (the sweep
B1969), every choice inside it (kit B1974 D1 to D7; Q1 = a in words at stamp S4), and HOLDING the pull request until the
solution-line round after L1 (S4, Q2 overruled to the alternative). Nothing here says the product owner decided, ruled
or approved anything about the routes, the statuses or the host (kit B1974's CLARIFICATIONS greps for those subject
words counted 0, RELAYED).

## State at this gate

- Verdict GO WITH FINDINGS at `685d72b` on main `da8d64a` (round 1 of 2 of lane H). HELD: lands only after L1 and lane
  H's solution-line round (round 2), with round 2's numbers (landing.txt in this folder).
- The host maps its first routes: `GET /health`, `POST /oxpd2/devices/{serial}/{target}/{operation}` (the five OXPd 2
  callbacks) and `POST /oxpd2/devices/{serial}/notifications`, HTTPS only on the two OXPd 2 routes, the status table of
  D3; owed item 45's binding (`IDeviceSecretVault` to `ISecretStore`) is made by the host (the records lane ticks it when
  this lands) (RELAYED from the kit's FOR RECORDS).
- The 13 cells ran on macOS only (the seat's run and this gate's own run); the hosted legs build, publish and guard the
  Server but run none of the cells until the solution line (this gate counted the Server test assembly in both hosted
  legs' logs: 0 and 0).

## From this gate (for the backlog)

1. **Owed, Minor (VERDICT FOUND 1): the one-`Authorization`-header rule has no cell on either route.** Two survivors:
   `Count == 1` to `Count >= 1` at `CallbackEndpoint.cs:27` (the kit's `mFirstOfTwoHeaders`) and at
   `NotificationEndpoint.cs:29` (not named by the kit). MEASURED by a gate probe with a raw TLS client: two header
   lines are reachable in production and refused 401 at the head; under either mutant a good-first pair is 200 while
   the 13 cells stay green. Not a Blocker (the credential is still required). Round 2: one raw-socket cell per route.
2. **Owed, Minor (VERDICT FOUND 2): the kit's "no presented credential reaches a log line" does not hold at Debug.**
   MEASURED: Kestrel's `Microsoft.AspNetCore.Server.Kestrel.BadRequests` category logs, at Debug, the text of a
   malformed header line (`Invalid request header: 'Authorization Bearer <value>\r\n'`). Framework behaviour; a
   well-formed header never reaches it. Round 2 or the logging lane (Q5): a README Limits line and/or a category
   filter (the coordinator's product choice).
3. **Owed, Minor (VERDICT FOUND 3): root `README.md:14-15` describe the Server before this lane** ("references Core",
   "maps NO route, reads NO configuration secret; never started by any test"). The kit forbade the root README. One
   README pass after landing, or round 2 with the coordinator's leave.
4. **Info for the install sequencer (wave 2):** register `https://<host>/oxpd2/devices/<serial>/<target>` with the
   target spelled exactly `Authentication` or `UsbAccessories` (ordinal, `Oxpd2CallbackHandler.cs:249`), and
   `.../notifications`; issue credentials through the host's own `CallbackCredentials` singleton (a rotation by another
   process is not seen by a host that cached the old hash, DERIVED from `CallbackCredentials.cs:165-199`);
   `IOxpd2NotificationSink` is internal to the Server.
5. **Info for the sign-in lane:** it replaces `NotWiredCallbackSink` (`ServerHost.cs:40`); 14 of 14 outcomes map; device
   behaviour on non-200 is UNMEASURED.
6. **Info (hardening, later):** an unauthenticated request with any rule-valid uncached serial costs one secret-store
   read (the adapter's named limit); no rate limit in the host.
7. **Carried named limits (RELAYED from kit B1974):** the Required Section's H10 to H14 (TLS-terminating proxy refused
   403; HTTP/2 not run by a cell; serial case and percent-encoding; declared-over-bound read vs unread; the Windows
   event log provider), and the Server README's Limits (device behaviour UNMEASURED; notification body unspecified and
   unparsed; the callback options are the adapter's defaults; answer bytes not zeroed after the write;
   `ISolutionTokenEndpoint` not bound). Not in this lane: migrate-at-start, the admin API, Universal Print, sign-in, the
   logging library (Q5), `ISolutionTokenEndpoint` (TA's, wave 2).
8. **UNMEASURED:** every cell on Linux and Windows (Windows PEM certificate load; H08's store under DPAPI-NG); the hosted
   legs of any merge with a main after L1; CodeQL on the pull request; what an OXPd 2 device sends to these routes and
   does with each status (the M577 is OXPd 1.x and will never call them, RELAYED from the kit).
