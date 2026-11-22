Adds the job service of the OXPd 2 server without the converter (work package WP1.7, in part), in three commits and
two merge commits of main: the service, a fix commit (cancellation, blocking callers, a refused file), and a test-only
commit that makes one test deterministic. The host does not use the library yet: nothing is wired to an endpoint,
nothing calls `Sweep` or `WipeSession`, and the server's published output is unchanged (release guard 10 and 11
files).

## What it does

- `JobSpool`: an encrypted spool of job files on local disk. Each job has its own 32-byte key, held only in memory
  and cleared when the job is wiped. A file is a 5-byte header and AES-256-GCM chunks (16-byte tag; the nonce is the
  file number and chunk number; the associated data binds the job, the file, the chunk and a final flag). A reader
  checks a chunk's tag before it hands out a byte of it, and refuses a changed byte, a cut or extended file, chunks
  out of place and a file from another job with `SpoolCorrupt`; a reader that refused once refuses every later read.
  A job is wiped by `WipeJob`, `WipeSession`, on a touch after its lifetime (60 minutes), by `Sweep`, and with
  everything under the root when a new spool starts. Caps count the plaintext actually written and are reserved
  across all jobs before a chunk reaches the disk: 512 MiB per file, 1 GiB per job, 500 files per job, 20 GiB per
  spool.
- `ScanReceiver`: `OpenScan` makes a job and a 32-byte scan secret (43 base64url characters, returned once); only its
  SHA-256 is kept and it is compared in fixed time. An unknown job, a wrong secret, a closed scan, a passed window and
  a wiped or expired job all end `JobNotFound`. `ReceiveAsync` streams one multipart upload into the job, one file per
  part, within the caps, the header limits and `ReceiveTimeout` (10 minutes); a failed upload wipes the whole job.
  One upload per job at a time (`JobBusy`).
- `PrintJobSender`: `SendAsync` builds a Print-Job request from the IPP library's public types, writes it and the
  document through an `IIppTransport`, and accepts only a valid answer to that request (its request id, a success
  status, one `job-id` and one `job-state`); `TrackAsync` polls Get-Job-Attributes until the state is final or
  `TrackTimeout` passes. The send is bounded by `SendTimeout` and the answer's read by `ResponseTimeout`.
- Every refusal is a `JobServiceException` with one of 18 reasons and a fixed message; it never carries a document
  byte, a secret, a file name, a session id, a job id or an address. The other exceptions that leave the library are
  the caller's own cancellation and `ObjectDisposedException` from the members of a disposed spool the README names.

## The fix commit

- An answer stream or a transport that throws its own cancellation (the caller's token not cancelled) ends
  `TransportFailed`, never a raw cancellation.
- Every bound is armed before a caller's code runs: a receive copies the body, and a send or a poll runs its exchange
  and reads the answer, on a thread of the pool, so a body, a transport or an answer stream that blocks its thread
  ends at its bound (`ReceiveTimedOut`, `ResponseTimedOut`).
- A reader that refused its file stays refused; a receive whose spool is disposed ends `JobNotFound`.

## The test-only commit

- One test checks that the receiver does not keep the scan secret's text by walking every object reachable from the
  receiver. The walk now never enters a clock, a task, a cancellation token, source or registration, or an execution
  context. Before, it could follow a pending timer on the test clock into the cancellation token all tests share and
  on into other running tests' receivers, whose collections changed under it (an intermittent `Collection was
  modified`). The walk still reaches every object of the receiver and its spool it reached before. No product file
  changed in this commit.

## Limits, stated plainly

- Deleting a file does not overwrite its blocks; the guarantee is that no key for those bytes exists any more. The key
  lives in process memory (swap or a crash dump can hold it).
- No timer: an expired job's files stay until the next call that touches it or the host's `Sweep`.
- A bound returns to the caller; it cannot free a thread. A body, transport or answer stream that blocks for ever keeps
  a thread of the pool blocked after the call has ended.
- A good answer whose stream's close never completes ends `ResponseTimedOut` at the send bound (30 minutes); a caller
  that retries may print twice.
- A caller's body whose read throws `ObjectDisposedException` ends `JobNotFound`; no test pins that row yet.
- The test that looks for the secret's text does not see text kept as the state of an object it never enters: a
  clock, a task, a cancellation token, source or registration, or an execution context (for example the text inside a
  completed task, or as the state of a callback registered on a job's cancellation source). The library keeps no such
  text: no field of it holds a task outside an async method's own state, it registers no callback of its own on a
  cancellation token, and it has no static field and no async-local or thread-local value.
- One process per root. On Windows the root's access lists are the installer's to set.
- The real transport (HTTPS to the device) is not here; the only `IIppTransport` is a fake in the tests. What the
  devices send in a scan upload, and whether a given printer accepts the Print-Job as built, are not measured.
- No converter, no thumbnails, no PDF reading, no Print-URI, no priority print.

## Tests

120 tests in `tests/Datasec.Suite.Jobs.Tests`. Whole solution on this branch (main merged): 1524 tests, 0 failed,
4 skipped on linux and 19 on windows (the secret store's operating-system tests). No package version, workflow or
build file changes; the solution file gains the two job-service lines. Nothing is deployed; nothing was sent.
