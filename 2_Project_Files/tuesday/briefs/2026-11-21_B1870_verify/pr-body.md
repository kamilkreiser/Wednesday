## What this adds

One commit. Two new libraries and their two test projects for work package WP1.1 (the part that needs no printer):

- `src/Datasec.Suite.Devices`: the device model and its value rules (serial, address, DNS name, platform, panel
  class, registration state, health, firmware and model text, store references, capability snapshot, defect-table
  match), the registry interface `IDeviceRegistry`, and the clock check behind two interfaces (`IReferenceClock`,
  `IDeviceClockReader`). No package reference and no project reference.
- `src/Datasec.Suite.Data`: one EF Core model (`SuiteDbContext`) for devices, store references, capability
  snapshots, defect-table matches and an audit log; two derived contexts, one per provider, each with its own
  migration set (`Initial`) for PostgreSQL and for SQL Server, scaffolded by a scratch program and not edited by
  hand; the EF-backed registry `EfDeviceRegistry`; the audit log `EfAuditLog`; `AddSuiteData` for a later host.
- Tests: 144 new (92 and 52) on SQLite in memory; each provider's idempotent script is committed as a test snapshot
  and compared with a fresh script on every run.
- Four solution lines and three package lines (`Microsoft.EntityFrameworkCore.SqlServer` and
  `Microsoft.EntityFrameworkCore.Sqlite` at 10.0.15, `Npgsql.EntityFrameworkCore.PostgreSQL` at 10.0.4). No
  workflow, build-script or existing lock-file change. The server does not reference either library yet.

## What the rules are

- A serial is 1 to 64 of `A-Z`, `a-z`, `0-9` and `-`; the fallback literal `NoSerial` is refused in any case. The
  key is the serial upper-cased by the invariant culture; a second device that differs only by case is refused by
  the registry and by the database key.
- An address is a canonical IPv4 or IPv6 address (IPv6 stored lower case); forms such as `1234`, `0x7f.0.0.1`,
  leading zeros, a port, a scheme or a zone id are refused. A DNS name is stored lower case, labels of 1 to 63, at
  most 253 in all, never an IP literal.
- A device holds at most one store reference per kind (`oxpd1-admin-password`, `oxpd2-solution-refresh-token`,
  `callback-credential`); a reference is a NAME that follows the secret store's name rule, never a value. There is
  no kind and no column for an OXPd 2 admin password.
- A capability snapshot is a JSON object of at most 262,144 UTF-8 bytes; every snapshot is kept and the newest is
  returned. A stale update (an old `Version`) saves nothing. Every stored time is UTC.
- The clock check returns `within`, `outside` or `unknown`; tolerance 300 seconds, inclusive; a source that answers
  nothing or throws gives `unknown`, never `within`.
- The audit log only grows through the library: saving a changed or removed audit entry is refused and saves
  nothing. Unknown stored vocabulary text makes a read fail; it is never read as a default.

## Limits

- No run against a real PostgreSQL or SQL Server yet: each migration set is checked against the model and each
  script against its snapshot, offline. Applying a script twice to a real database is not measured.
- The SQLite schema of the tests comes from the model, not from either migration set.
- The audit log is append-only in the library only: `ExecuteUpdate`, `ExecuteDelete` and raw SQL bypass it, and
  there is no grant or trigger in either database (the tests assert each limit).
- The reference clock and the device clock read are interfaces only (no NTP client, no device call).
- A reference value that happens to follow the name rule cannot be told from a name.
- No sessions, jobs or Universal Print tables; no host wiring and no migrate-at-start.
- The SQL Server provider brings Microsoft.Data.SqlClient and, through it, Azure.Identity, Azure.Core and the
  Microsoft.Identity.Client and IdentityModel packages into this library's dependency graph (listed in the lock
  file). Whether they may stay in the server's graph is an open question; the server does not reference this
  library yet.

## The packages: one recorded fetch

The EF Core and Npgsql packages were not in the project's package cache. They came in by ONE supervised restore from
nuget.org (74 package versions: 59 reached through the lock files, 15 resolver lower bounds that no lock file names).
Every later restore ran offline from that cache, against the lock files. The record (every package, its lock-file
content hash and its file hash) is kept outside the repository at
`1_Project_Definition/Briefs/2026-11-21_B1856_FETCH-RECORD.md` in the project folder; every one of its 74 file
hashes was compared with the package hash nuget.org publishes and all 74 are equal. The hosted legs restore in
locked mode against the lock files' content hashes.

Every serial, address, name and connection string in the tests is synthetic; connection strings point at hosts under
`.invalid` with no password. Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
