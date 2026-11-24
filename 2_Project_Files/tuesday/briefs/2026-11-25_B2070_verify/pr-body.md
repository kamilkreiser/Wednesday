The OXPd 1.x echo verb, built and tested against stubs only, before any run against a device. One commit, `de8f2a47`,
on `main` `217286f3` (behind 0, ahead 1). Twelve files: four added, eight changed, all under
`src/Datasec.Suite.Adapters.Oxpd1/`, `src/Datasec.Suite.Lab/Commands/Oxpd1/` and the two matching test folders. No
package, no lock file, no project file, no `Datasec.Suite.slnx` line, no workflow, no file under `contracts/`.

## Why

- The path test needs to prove that a device can answer the Test service's echo and call a listener back. HP's Test
  service has two string echoes (`SyncEchoString`, `AsyncEchoString`); each "requires the caller to supply either guest
  or device administrator credentials", so the echo is sent as `guest` and never needs the admin password.

## What changed

- **The client.** `Oxpd1Echo` with the closed enum `Oxpd1EchoKind` and a two-row catalogue read back from the committed
  binding; `Oxpd1EchoCall` with HP's bounds (message 1 to 8192 characters, delay 0 to 60000 ms, an `http` or `https`
  callback with no `@`, at most 256 characters); ONE request per call through the new internal `SendGuestAsync` (HTTP
  Basic `guest`, the same pinned handler, time-out, answer bounds and record as a read). A sync answer is read by
  `ReadTextAnswer`: no attribute on the response but a namespace declaration, nothing beside the result but white-space
  text, the result text-only, attribute-free and not empty. `CallbackMessage` reads a callback body.
- **The lab.** `oxpd1 echo` (exits 12 and 13 are new): the run folder rule, then the credentials file's names (any name
  holding `ADMIN`: exit 12, no value read, no folder, no connection), then the guest value, then the run folder. Sync:
  exit 0 only when the answer's text is the message sent. Async: a plain HTTP/1.1 listener starts first (127.0.0.1 by
  default), the device is sent `http://<callback-host>:<port>/oxpd1-echo/<32 hex>`, and only a POST to that path whose
  body holds the message passes (exit 13 when none arrives within the wait).
- **Text.** Both READMEs: the echo rows, the verb's section, its exit codes and its Limits.

## What proves it

- Red first: 23 cases fail by assertion on a permissive first shape (adapter `Total: 70, Failed: 8`; lab `Total: 254,
  Failed: 15`). Green: 2261 / 0 / 2257 / 4 locally; the branch's push run 45411074875: linux 2257 succeeded, windows
  2240 succeeded, rules 675 files, `Ran 117 tests`, secret scan clean.
- 11 mutants, each red on exactly its cells, none surviving (guest sent as admin; an admin name taken by option or by
  file; another message, text beside, an attribute on the response, a child element or attribute on the result, an
  empty result taken; the callback's path or message ignored; no callback passing).
- Against stubs on 127.0.0.1: the admin name refused by option (exit 2) and in the file in either case (exit 12) with
  no folder and 0 connections; the Test service off (exit 8, the switch named); a refused guest credential (exit 6
  after one request); a callback with another message, on another path or by GET (exit 13, each listed).

## Still open

- No TLS listener: the callback address is plain `http`. Whether the M577 answers either echo as guest, calls an `http`
  address back across its networks, sends a `Content-Length`, and what it expects in answer: not measured. The LAN run
  (the M577 calling the lab machine) is a separate step after this lands.
- The admin-name refusal reads names, not values: an admin password stored under a name without `ADMIN` is not seen.
- The callback reader accepts some bodies HP's schema refuses (text or an attribute beside `message`), and the sync
  reader takes non-ASCII white space beside the result; a callback host whose address would exceed 256 characters
  ends the run with an unhandled error after the run folder is made; a delay longer than the wait or the time-out ends
  exit 13 or 8 with words that blame the path; `--callback-bind 0.0.0.0` listens on every interface; the listener reads
  one connection at a time, so idle connections can use up the wait. None reaches a device or a secret.
- Known from the Test service change, not changed here: five `IsServiceEnabled` answers HP's schema refuses are still
  read, and a run folder behind a relative link through another link can land inside a work tree.
- Local CodeQL cannot run on this machine; the code scanning of this pull request is the CodeQL read.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it (a plain HTTP listener in the lab bound to
loopback by default; the guest user with both admin-name refusals; a new strict sync reader beside the landed one;
exits 12 and 13; the run's own message; the landed literal and the stub's four lines; the strict callback reader; no
local CodeQL). No choice in this change is the product owner's.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
