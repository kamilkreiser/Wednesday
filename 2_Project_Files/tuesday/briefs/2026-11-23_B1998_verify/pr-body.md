OXPd 2 contract runtime follow-ups (WP0.4). One commit, `81ae47ed`, on `d804de5e`. One test file is added
(`BodyReadTests.cs`) and 18 files change: the generator's `Oxpd2Unit.cs` (the client summary, two lines), the 16
generated `*Client.cs` files written from it by the regeneration program (two `///` lines each), and
`TolerantReadingTests.cs` (K8's last block). No code line of the adapter, no public member, no package, no workflow,
no `Directory.*` file and no `Datasec.Suite.slnx` line changes.

## Why

- Owed item 36's F6: an `IOException` from a body stream passes out of a client method beside `HttpRequestException`,
  and nothing said so. Its N11 half (the clients do not parse a non-success body) was already written in N11's summary.
- Owed item 67, its pull-request-20 part: K8 refused a null at the FIRST optional root property of each client model
  only, and its count was not pinned. A parser that tolerates a null at every optional property but the first passed
  the whole landed suite (measured at `d804de5e`: 149 of 149 green).
- Item 36's F1, F2 and F3 are NOT rebuilt: pull request 7 (`0804860b`) closed all three (read-only lists,
  `HighestMaxBodyBytes`, the astral N9 rows), present on `main`.

## What changed

- Every generated client's summary now reads: "An HttpRequestException from the send, and an IOException while a
  success answer's body is read, pass out of a method as they are: neither is a refusal. The client never reads the
  body of a non-success answer."
- `An_io_failure_of_a_success_body_leaves_every_client_as_that_exception_and_the_stream_is_closed`: the first
  JSON-answer method of each of the 16 clients, a body that fails when opened, at its first read, and after part of a
  body: that same exception object leaves the method; the stream is closed.
- `The_body_of_a_non_success_answer_is_never_read`: 404, 500 and 302 with a body that would throw: never opened.
- `Every_client_names_what_passes_out_of_its_methods`: the two lines in each committed client file.
- K8: a null at every optional root property of every client model, `WrongType` at its path; both counts pinned
  (716 models, 2117 properties).

## What proves it

- Red first (macOS arm64): the two test files alone at `d804de5e`: 1945 total, 1 failed (the text cell, by its own
  assertion). With the change: 1945 / 0 / 1941 / 4. The two behaviour cells and K8 pin what `main` already does; their
  red is shown by the mutants.
- 4 mutants (null tolerated after the first optional property, a read failure swallowed, an open failure swallowed, a
  non-success body read), each red on exactly its cell at the head; at `d804de5e` all four pass the landed suite.
- A regeneration from the head's generator writes exactly the committed files.
- K8's two counts equal an independent count from the committed generated text (716 and 2117, two ways).
- The branch's push run 45128961671: linux 1941 succeeded, windows 1924 succeeded (the text cell green on a Windows
  checkout), rules 629 files, secret scan clean.

## Still open

- The summary names two exception types; others pass out of a method too, as they are: a cancellation or the
  HttpClient's time-out (`TaskCanceledException`), and, with a caller's handler that decompresses, an
  `InvalidDataException` for a corrupt compressed body (measured on 127.0.0.1). The HttpClient's time-out does not bound
  the body read; the caller's token does (measured).
- "Never reads" holds for the client's code: the platform handler drains an unread non-success body to reuse the
  connection (measured: two 404 answers with bodies, one connection). Nothing of it is parsed or handed back.
- Optional properties below the root have no strict cell of their own; what a real device does when a body ends
  mid-read is not measured (no device was reached).

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it: F1 to F3 not rebuilt, F6 said and
pinned with no runtime change, both K8 counts exact. No choice in this change is the product owner's.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
