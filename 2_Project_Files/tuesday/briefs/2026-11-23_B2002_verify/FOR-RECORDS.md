# FOR RECORDS: lane L5 (kit B1997, seat X56), the lab `oxpd1` command, head f0cd57a3 (gate B2002)

For the records lane only; nothing here is written into a project file by the gate. Who decided every choice of this
lane: the coordinator (Tuesday), as coordinator, never the product owner (kit THE AUTHORITY; CLARIFICATIONS.md counts 0
on every subject of the lane, RELAYED from the drafter).

## From the kit's FOR RECORDS (RELAYED, copied)
- The lab tool reaches the OXPd 1.x client: `oxpd1 read` (first-run step 1) with one password-bearing request per run
  and a stop on any end; `oxpd1 lab-cert` (a development CA and a server certificate for a host name, no CA key kept).
  Neither has run against a device.
- The client gained one public option, `Oxpd1ClientOptions.Addressing` (2005 default, 2004 on request); the design
  document's "WS-Addressing 2004" line (`02:249`) is still unamended (B1996 amendment A11 is the records lane's).
- Named limits: the attempt count is per run (H6; the per-device count is the shared device-trust component's, B1996
  F13 and F16); a challenge-carrying 401 (H5); credentials lines in `export` form (H10); a run folder through a link,
  or a work tree named only by environment (H13, H14); no TLS handshake with the written certificate, and the M577's
  acceptance of it, are UNMEASURED (H22); the probe's own run folder is not checked against git work trees.
- Left for the shared device-trust component (B1996 F13): the pin check of a pinned read is still the client's own
  copy; first contact is the lab channel's; neither stores a fingerprint.
- Two landed cells changed by one line each: P13's and lane L4's R11's registry lists, because any new command reddens
  both (an exact-list cell is a cost every later command pays; a later round may relax both to "contains").
- Observed once, not this lane's: `GatewayStubTests.C7_healthcheck_answers_healthy` failed in the drafter's red
  whole-solution run at load1 6.72 and passed in every other run (the seat saw no C7 red in 3 runs; the gate none in 1).

## Changed by the gate's measurements (MEASURED, gate probe, macOS arm64, .NET 10.0.404, stub on 127.0.0.1)
- **H4 is no longer only DERIVED.** The kit's "resend path of the HTTP layer is unreached" limit: with the tree and the
  SOAP read on ONE port (the POST reusing the tree's pooled connection) and on TWO ports, a connection dropped by the
  stub after it read the POST, a connection closed by the stub right after the tree answer, a 401 with a
  `WWW-Authenticate: Basic` challenge, a 307 to the same path, a 401, a 403, a fault and a time-out each gave exactly ONE
  password-bearing request in all (18 of 18 shapes). Windows and Linux: the hosted cells R02/R03 only (UNMEASURED by
  the probe there).
- H13 MEASURED: a run folder reached through a symbolic link into a work tree is NOT refused (as the kit's limit says).
  A `.git` that is a symbolic link (to a folder, or dangling) IS refused.

## The sentence that is now untrue (L4's, for the records lane or a later round)
- `src/Datasec.Suite.Lab/Device/DeviceChannel.cs:37` (landed by L4, PR 39): "The probe's ONE way to a device." Once this
  lane lands, `oxpd1 read`'s first contact also goes through `DeviceChannel`, and its pinned read reaches the device
  through the OXPd 1.x client, not the channel. The kit's Q1 named it; this lane does not touch the file (not an owned
  path). A one-word fix for a later round: "The lab tool's channel to a device for probe and for oxpd1's first contact".

## Gate findings to carry (VERDICT.md FOUND, all Minor or Info, none blocking)
- FOUND 1 (Minor): the password typed as `--password=<value>`, or as a stray word, is echoed by the usage error.
- FOUND 2 (Minor): an unreadable or dangling-link credentials file, a blank `--run` or a blank `--credentials-file`
  ends in an unhandled exception, not exit 7 or 2 (nothing sent; the run folder may be left empty).
- FOUND 3 to 7 (Info): see VERDICT.md.
