The OXPd 1.x adapter's first device-write code: `Oxpd1Writer`, the register and unregister of a test sign-in agent (first-run
step 5). One commit, `f039956d`, on `main` `2e2feae8` (behind 0, ahead 1). Two files are added
(`src/Datasec.Suite.Adapters.Oxpd1/Oxpd1Writer.cs`, `tests/Datasec.Suite.Adapters.Oxpd1.Tests/WriteTests.cs`) and four change
(`Oxpd1Client.cs`, `Oxpd1Soap.cs`, the adapter README, the stub `StubDevice.cs`). No package, no lock file, no project file,
no `Datasec.Suite.slnx` line, no workflow, no `Directory.*` file, no Lab file.

## Why

- The first-run list's step 5 registers a test sign-in agent on the older printer and removes it again; the read client on
  `main` could not write.
- A write to a printer must be undoable and must not happen by accident, so every call is a dry run unless asked, and the
  register hands back its undo whenever it may have taken effect.
- The printer locks its admin account after five wrong passwords, so an executed call sends one request and never retries.

## What changed

- `Oxpd1Writer.WriteAsync(Oxpd1WriteCall)`: the closed list `Oxpd1WriteKind` (`RegisterSignInAgent`,
  `UnregisterSignInAgent`) and a two-row write catalogue, `RegisterAuthenticationAgent` and `UnregisterAuthenticationAgent`
  of the committed Authentication binding.
- `Oxpd1WriteCall.Execute` is false unless set (`with { Execute = true }`): a dry run reads no setting, opens no connection
  and returns the envelope, the URL and the action.
- An executed call goes through the client's new internal `SendWriteAsync`, which calls the client's one `SendAsync` (the
  same pinned handler, time-out, answer bounds and record as a read). `SendAsync`'s private signature now takes the action
  and an answer reader; the reads' envelopes are unchanged byte for byte.
- `Applied`: `Yes` on the empty response element; `No` on no setting, a refused pin, 401 and 403; `Unknown` on every other
  end. The register's undo (the unregister of the same id, itself a dry run) is returned on `Yes` and `Unknown`.
- `Oxpd1SignInAgent`: id, a name of 1 to 100 characters (also its en-US display name and description), the agent service
  (`Soap12`) and the prompt page (`Plain`), each absolute `https` without user information and at most 256 characters,
  time-outs 1 to 300 seconds (5 by default), no credentials.
- The client's record line reads `OXPd 1.x call` for reads and writes.

## What proves it

- Red first on `main` plus the cells and a permissive first writer: the client's tests 40 / 9 failed, the 9 planted cases
  only, each by an assertion. Green: 2020 / 0 / 2016 / 4. 11 mutants, each red on exactly its cells, none surviving.
- Both request bodies validate against HP's committed schema; a planted `Soap11` binding does not.
- Against a stub on 127.0.0.1, on a fresh and on a reused connection: an answer, a 401, a 401 with a challenge, a 403, a
  fault (also one carrying the password in its code), a 200 fault, a 500 or a 200 that is not the response element, a 307,
  a 302, an oversized answer, a time-out after the write, a connection reset, a connection closed after the request (TLS
  and TCP), and a broken status line each gave exactly ONE request carrying the password; none put the password or its
  Basic token in a result, a fault code or the record. Twelve dry-run shapes (a call set and unset, the undo, a disposed
  client, a setting reader that throws, an unresolvable host, a cancelled token, 20 at once) opened no connection and
  read no setting.
- `Oxpd1Client`'s public members are the same four as on `main` (compared by reflection).
- The branch's push run 45159822038: linux 2016 succeeded, windows 1999 succeeded, rules 645 files, secret scan clean.

## Still open

- No device has been reached: the endpoint, the answer, the fault subcodes, whether the device applies a write before it
  refuses the credentials, and whether it accepts the record are not measured.
- The undo leaves the device as it was only when the id was not registered before: a register replaces a record of the
  same id, and its undo removes that id. Nothing reads the device's records first.
- An address written `https://@host/...` (empty user information) is taken by the record, and its register body then fails
  HP's schema. A name with a control character is taken by the record, and the call then throws before anything is sent.
- The writer counts nothing across calls; stopping a run after a refused password is the caller's (the lab wiring, a later
  change). Steps 2, 3 and 4 are not built: their operations are in no committed file under `contracts/oxpd1/`.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it (step 5's pair only, the dry-run default,
the three-valued `Applied`, the undo rule, the record, no guard in the adapter, the record word). No choice in this change
is the product owner's.

Nothing is deployed; nothing was sent.
