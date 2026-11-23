Lab tool, the `oxpd1` command (first-run step 1 for an OXPd 1.x device, and a lab certificate for steps 3 to 5). One
commit, `f0cd57a3`, on `main` `57e9042a` (behind 0, ahead 1). Eight files are added (`src/Datasec.Suite.Lab/Commands/Oxpd1/`
four, `tests/Datasec.Suite.Lab.Tests/Oxpd1/` three, `tests/Datasec.Suite.Adapters.Oxpd1.Tests/AddressingTests.cs`) and
eleven change (four of the OXPd 1.x client, the command table, the Lab `.csproj`, the Lab README, the two Lab lock files,
one line each of `ProbeTests.cs` and `Print/PrintTests.cs`). No package, no `Datasec.Suite.slnx` line, no workflow, no
`Directory.*` file.

## Why

- The read client of `src/Datasec.Suite.Adapters.Oxpd1` was on `main` but the lab tool could not call it.
- An OXPd 1.x device locks its admin account after five wrong passwords, so the read sends the password at most once per
  run and stops on any refusal.
- Which WS-Addressing version a FutureSmart 5 device accepts is not known; the other one is one option away.
- An OXPd 1.x device refuses a server named by an IP address, so the lab server needs a host-name certificate.

## What changed

- `oxpd1 read <host> --run <new folder> --credentials-file <file> [--pin <sha256>]... [--read] [--addressing 2005|2004]`:
  without `--pin`, a first contact through the lab channel (`DeviceChannel`, no pin): each port's certificate printed,
  every handshake refused, nothing sent. With pins: the password from the credentials file only (exit 7 before any
  connection when absent), the discovery tree with no credentials, then ONE read with HTTP Basic `admin`; 401/403 exit
  6 with the lockout message, any other end exit 8; nothing retried.
- `oxpd1 lab-cert <host name> --run <new folder> [--days 30]`: a development CA (key never written) and one server
  certificate for the name (SAN = the name only, server authentication); `server.key` owner-only on macOS and Linux.
- Both verbs refuse a run folder inside a git work tree (exit 9).
- `Oxpd1ClientOptions.Addressing` (public): `Version200508` default, `Version200408` writes the four headers in
  `http://schemas.xmlsoap.org/ws/2004/08/addressing` with `ReplyTo` `.../role/anonymous`; an undefined value is refused.
- Cells P13 and R11 pin the registry list exactly, so each gains `"oxpd1"` (one line each).

## What proves it

- Red first on `main` + the test files and a permissive first shape: Lab 95 / 15 failed, client 27 / 1 failed, the 16
  planted cases only. Green: 2007 / 0 / 2003 / 4. 15 mutants, each red on exactly its cells, none surviving.
- Against a stub on 127.0.0.1, on one port and on two ports: a 401, a 403, a 401 with a challenge, a 307, a SOAP fault,
  a time-out, a dropped connection and a connection closed after the tree each give exactly one request carrying the
  password; none of them puts the password or its Basic token in the output or the run folder.
- The branch's push run 45139381044: linux 2003 succeeded, windows 1986 succeeded, rules 643 files, secret scan clean.

## Still open

- No device has been reached: the addressing version, the endpoint, the answer, the certificates on 7627 and 443, and
  whether the device accepts the written certificate are not measured.
- The attempt count is per run; nothing remembers a refusal across runs.
- A password typed on the command line as `--password=<value>` or as a stray word is echoed in the usage error (exit 2,
  nothing sent). The README says the password is never printed.
- An unreadable or dangling-link credentials file, or a blank `--run` or `--credentials-file`, ends in an unhandled
  exception rather than exit 7 or 2 (nothing sent).
- A run folder reached through a symbolic link into a work tree is not refused (a stated limit).
- `DeviceChannel.cs:37` still calls the channel "The probe's ONE way to a device"; `oxpd1` now uses it and the client.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it (one command with two verbs, the
credentials file, the per-run count, the client option, RSA 2048 with no CA key, the run-folder refusal, the two
registry lines). No choice in this change is the product owner's.

Nothing is deployed; nothing was sent.
