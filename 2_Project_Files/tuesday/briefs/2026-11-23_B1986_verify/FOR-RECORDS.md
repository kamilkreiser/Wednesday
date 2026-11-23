# FOR RECORDS: Server host composition v0 (lane H), gate G1 round 2 of 2 of lane H, reader B1986

Not repository text. For the next OXPd records pass; nothing here was written into the project. No person is named.
Who decided: the coordinator (Tuesday), as coordinator: lane H, its widening (sweep B1969), every choice of round 1
(kit B1974 D1 to D7, S4) and of round 2 (kit B1985 D1 to D5, S4: merge then fix, both slnx lines, H14/H15 as patched,
the README Limits line and no host filter, root README lines 14-15 only), and the HOLD of round 1's pull request
until the solution-line round. Nothing here says the product owner decided, ruled or approved anything about the
routes, the statuses, the solution lines or the host.

## Round 1 (kit B1974, seat X48, head 685d72b6, gate B1981 GO WITH FINDINGS @ 685d72b on main da8d64a)

- The host maps its first routes: `GET /health`, `POST /oxpd2/devices/{serial}/{target}/{operation}` (the five OXPd 2
  callbacks) and `POST /oxpd2/devices/{serial}/notifications`; HTTPS only on the two OXPd 2 routes; the status table
  of D3; owed item 45's binding (`IDeviceSecretVault` to `ISecretStore`) made by the host (the records lane ticks it
  when this lands). 13 cells, macOS only (the test project was not in the solution).
- Gate B1981 FOUND 1 to 3 (all Minor): the one-header rule untested on both routes; the log property overstated at
  Debug for a malformed header line; root `README.md:14-15` stale. INFO 3 to 6 carried for wave 2 (below).

## Round 2 (kit B1985, seat X51, head 0c65be47, gate B1986: see VERDICT.md line 1)

- Shape: ONE merge commit `4c415f9a` of main `cad65b86` (tree `765182d5` = `merge-tree`'s, no hand edit), then ONE fix
  commit `0c65be47` of 5 paths, all `M` (tree `a17719c2`, = `3-round2.diff` applied to the merge, replayed by the
  gate). No product `.cs`, `.csproj` or lock line changed after round 1 (the 8 product files of
  `src/Datasec.Suite.Server/` byte-equal to round 1's).
- `Datasec.Suite.slnx` gains the Server test project and `src/Datasec.Suite.Jobs.Transport`. The 15 cells ran on
  both hosted legs for the first time (push run 45101722950: linux 1919 / 1915 / 4, windows 1919 / 1898 / 21; the
  Server test assembly `passed` on each leg). **Gate B1983 FOUND 1 is CLOSED**: the transport builds under
  `bin/Release` in the solution build (MEASURED locally and on both legs; control: at the merge commit alone the same
  build prints it under `bin/Debug`, total 1904, no Server test line).
- Gate B1981 FOUND 1: CLOSED by H14 (callback) and H15 (notification): two `Authorization` lines in three shapes are
  401 with a one-line 200 control; the two survivors (`Count == 1` to `Count >= 1` on each route) are now red on H14
  and H15 alone (MEASURED by the seat and independently by this gate: 14 of 14 MATCH).
- Gate B1981 FOUND 2: NARROWED, not fixed in code: the Server README Limits names
  `Microsoft.AspNetCore.Server.Kestrel.BadRequests` at `Debug` (the host sets no level for it). A host-side filter is
  NOT built (kit B1985 Q4): **owed to the logging lane**.
- Gate B1981 FOUND 3: CLOSED for root `README.md:14-15` (true at the head). The rest of the root layout list is still
  behind main (it lists only the Core test project): **owed, one README pass by the records lane.**

## From this gate (for the backlog)

1. **Owed, Minor (VERDICT FOUND 1): the Server README's one-header-line sentence (`README.md:21`-`:23`) says the
   answer is `401` with none or two or more lines; with a vault that throws it is `503`** (MEASURED by a gate probe:
   a host with no `Secrets` configuration answers 503 to none, one and two lines on both routes). Fail closed; the
   same README says 503 for a vault that throws (`:43`, `:52`). Owed: one clause ("while the vault answers"). The
   re-cut squash body already carries the clause.
2. **Info: shapes of the one-line rule measured by the gate probe at the head (scratch only, quarantined):** three
   lines 401 on both routes; an empty `Authorization:` line 401 on both; the credential then an empty line 401; one
   comma-joined line on the notification route 401; the sinks held only the two one-line controls; no captured log
   line (205 at Trace) held the issued value or the junk value across those requests.
3. **Info: lane X1 round 2** (head 8f5813bf) and lane H both add two slnx lines; `merge-tree` of the two heads: rc 0,
   no conflict, tree `7ad207ef`, and on that tree locally 1940 / 0 / 1936 / 4, RULES 628. Whichever lands second can
   land on the pull request's merge ref without a new branch commit (landing.txt MAIN MOVES (B)).
4. **Info: the Server README** has one new 209-character line (`README.md:25`, a rewrap left undone in the callback
   paragraph). Cosmetic; no rule reads it.
5. **Carried for wave 2, not built (gate B1981 INFO 3 to 6, RELAYED):** the install sequencer registers
   `https://<host>/oxpd2/devices/<serial>/<target>` with `<target>` spelled exactly `Authentication` or
   `UsbAccessories` (ordinal, `Oxpd2CallbackHandler.cs:249`) and `.../notifications`, and issues credentials through
   the host's own `CallbackCredentials` singleton (a rotation by another process is not seen by a host that cached the
   old hash, DERIVED); `IOxpd2NotificationSink` is internal to the Server (`Sinks.cs:6`); the sign-in lane replaces
   `NotWiredCallbackSink` (`ServerHost.cs:40`); device behaviour on any non-200 is UNMEASURED; an unauthenticated
   request with a rule-valid uncached serial costs one secret-store read and the host has no rate limit (hardening,
   later).
6. **Named limits carried:** round 1's Required Section H10 to H14 (TLS-terminating proxy refused 403; HTTP/2 not run
   by a cell; serial case and percent-encoding; declared-over-bound read vs unread; the Windows event log provider)
   and the Server README's Limits (device behaviour UNMEASURED; notification body unparsed and unbounded in time; the
   callback options are the adapter's defaults; answer bytes not zeroed after the write; `ISolutionTokenEndpoint` not
   bound; the Kestrel BadRequests Debug line).
7. **For kit templates (RELAYED from seat X51's DEVIATIONS 1 and 3, the gate agrees):** a restore at a merge commit
   does not restore a project the patch then adds to the solution (a second locked restore is needed before a
   `--no-restore` build); a referencing test assembly is not recompiled by a product-only change, so "the test dll
   later than the newest source" is the wrong check after mutants (the product dll's time and a green run are).
8. **UNMEASURED:** CodeQL on the pull request (no Analyze row on a branch push); the pull request's merge ref after
   any main other than cad65b86; what an OXPd 2 device sends to these routes and does with each status (the M577 is
   OXPd 1.x and will never call them, RELAYED).
