| # | Case (relay: real `coagent relay` / stand-in exit 3) | Base exit | Head exit | Relay gone (base / head) | stderr kept-reader bytes base vs head (normalised: `<n> ms`, relay timestamp/port, thread id) | Judgement |
|---|---|---|---|---|---|---|
| 1 | real eoi reader-closed | 101 | 0 | True / True | (reader closed) | F1 (closed reader: base panics 101; head returns 0, end of input) |
| 2 | real eoi reader-kept | 0 | 0 | True / True | identical: `b'<ts> relay listening on 127.0.0.1:<port> (certificate sha256:<fp>)\nrelay-guard: end of input; the relay was stopped and reaped in <n> ms; exiting\n…` | identical |
| 3 | real self(SIGKILL) reader-closed | 101 | 1 | True / True | (reader closed) | F1 (closed reader: base panics 101; head returns the relay's code 1) |
| 4 | real self(SIGKILL) reader-kept | 1 | 1 | True / True | identical: `b'<ts> relay listening on 127.0.0.1:<port> (certificate sha256:<fp>)\nrelay-guard: the relay exited by itself (code None); exiting\n'` | identical |
| 5 | real self(SIGTERM) reader-closed | 101 | 101 | True / True | (reader closed) | identical — 101 here is the RELAY's own exit (it panicked writing "terminate received" to the dead pipe; pre-existing, relay crate) |
| 6 | real self(SIGTERM) reader-kept | 0 | 0 | True / True | identical: `b'<ts> relay listening on 127.0.0.1:<port> (certificate sha256:<fp>)\ncoagent relay: terminate received; stopping\n<ts> relay stopped\nrelay-guard: th…` | identical |
| 7 | stand eoi reader-closed | 101 | 0 | True / True | (reader closed) | F1 (closed reader: base panics 101; head returns 0, end of input) |
| 8 | stand eoi reader-kept | 0 | 0 | True / True | identical: `b'relay-guard: end of input; the relay was stopped and reaped in <n> ms; exiting\n'` | identical |
| 9 | stand self(3) reader-closed | 101 | 3 | True / True | (reader closed) | F1 (closed reader: base panics 101; head returns the relay's code 3) |
| 10 | stand self(3) reader-kept | 3 | 3 | True / True | identical: `b'relay-guard: the relay exited by itself (code Some(3)); exiting\n'` | identical |
| 11 | H1 real reader closed before the frame, eoi | 101 | 0 | True / True | (reader closed) | F1 (closed reader: base panics 101; head returns 0, end of input) |
| 12 | H1 real reader closed before the frame, self | 101 | 1 | True / True | (reader closed) | F1 (closed reader: base panics 101; head returns the relay's code 1) |
| 13 | H2 real reader closed right after the pid line, eoi | 101 | 0 | True / True | (reader closed) | F1 (closed reader: base panics 101; head returns 0, end of input) |
| 14 | H2 real reader closed right after the pid line, self | 101 | 1 | True / True | (reader closed) | F1 (closed reader: base panics 101; head returns the relay's code 1) |
| 15 | H3 real reader closed in the same instant as eoi | 101 | 0 | True / True | (reader closed) | F1 (closed reader: base panics 101; head returns 0, end of input) |
| 16 | H4 real stdout+stderr readers closed after pid, eoi | 101 | 101 | True / True | (reader closed) | identical — the real relay panics writing to the closed stdout (101) before the event; the guard returns its code; pre-existing |
| 17 | H4 real stdout+stderr readers closed after pid, self | 101 | 101 | True / True | (reader closed) | identical — the real relay panics writing to the closed stdout (101) before the event; the guard returns its code; pre-existing |
| 18 | H4b real stdout closed after pid, stderr kept, eoi | 101 | 101 | True / True | identical: `b"<ts> relay listening on 127.0.0.1:<port> (certificate sha256:<fp>)\n\nthread 'main' (<tid>) panicked at /rustc/0ef1bc386059596dada8fb65b50425aab2ea6…` | identical — the real relay panics writing to the closed stdout (101) before the event; the guard returns its code; pre-existing |
| 19 | H5 real fd 2 closed altogether, eoi | 0 | 0 | True / True | (fd 2 closed) | identical |
| 20 | H5 real fd 2 closed altogether, self | 1 | 1 | True / True | (fd 2 closed) | identical |
| 21 | H6 real SIGPIPE ignored, reader closed, eoi | 101 | 0 | True / True | (reader closed) | F1 (closed reader: base panics 101; head returns 0, end of input) |
| 22 | H6 real SIGPIPE ignored, reader closed, self | 101 | 1 | True / True | (reader closed) | F1 (closed reader: base panics 101; head returns the relay's code 1) |
| 23 | H6 real SIGPIPE ignored, reader kept, eoi | 0 | 0 | True / True | identical: `b'<ts> relay listening on 127.0.0.1:<port> (certificate sha256:<fp>)\nrelay-guard: end of input; the relay was stopped and reaped in <n> ms; exiting\n…` | identical |
| 24 | P1 real stdout closed BEFORE the pid line, stderr kept, eoi | 101 | 101 | not found by pid (guard died before the pid line); final pgrep: none / same | identical: `b"\nthread 'main' (<tid>) panicked at /rustc/0ef1bc386059596dada8fb65b50425aab2ea637a/library/std/src/io/stdio.rs:1209:9:\nfailed printing to stdout: …` | identical — pre-existing (R-2): the guard's `println!` of the relay pid panics; the relay is killed by kill_on_drop during the unwind (no process left) |
| 25 | P1 real stdout closed BEFORE the pid line, stderr closed, eoi | 101 | 101 | not found by pid (guard died before the pid line); final pgrep: none / same | (reader closed) | identical — pre-existing (R-2): the guard's `println!` of the relay pid panics; the relay is killed by kill_on_drop during the unwind (no process left) |
| 26 | H1 stand reader closed before the frame, eoi | 101 | 0 | True / True | (reader closed) | F1 (closed reader: base panics 101; head returns 0, end of input) |
| 27 | H1 stand reader closed before the frame, self | 101 | 3 | True / True | (reader closed) | F1 (closed reader: base panics 101; head returns the relay's code 3) |
| 28 | H2 stand reader closed right after the pid line, eoi | 101 | 0 | True / True | (reader closed) | F1 (closed reader: base panics 101; head returns 0, end of input) |
| 29 | H2 stand reader closed right after the pid line, self | 101 | 3 | True / True | (reader closed) | F1 (closed reader: base panics 101; head returns the relay's code 3) |
| 30 | H3 stand reader closed in the same instant as eoi | 101 | 0 | True / True | (reader closed) | F1 (closed reader: base panics 101; head returns 0, end of input) |
| 31 | H4 stand stdout+stderr readers closed after pid, eoi | 101 | 0 | True / True | (reader closed) | F1 (closed reader: base panics 101; head returns 0, end of input) |
| 32 | H4 stand stdout+stderr readers closed after pid, self | 101 | 3 | True / True | (reader closed) | F1 (closed reader: base panics 101; head returns the relay's code 3) |
| 33 | H4b stand stdout closed after pid, stderr kept, eoi | 0 | 0 | True / True | identical: `b'relay-guard: end of input; the relay was stopped and reaped in <n> ms; exiting\n'` | identical |
| 34 | H5 stand fd 2 closed altogether, eoi | 0 | 0 | True / True | (fd 2 closed) | identical |
| 35 | H5 stand fd 2 closed altogether, self | 3 | 3 | True / True | (fd 2 closed) | identical |
| 36 | H6 stand SIGPIPE ignored, reader closed, eoi | 101 | 0 | True / True | (reader closed) | F1 (closed reader: base panics 101; head returns 0, end of input) |
| 37 | H6 stand SIGPIPE ignored, reader closed, self | 101 | 3 | True / True | (reader closed) | F1 (closed reader: base panics 101; head returns the relay's code 3) |
| 38 | H6 stand SIGPIPE ignored, reader kept, eoi | 0 | 0 | True / True | identical: `b'relay-guard: end of input; the relay was stopped and reaped in <n> ms; exiting\n'` | identical |
| 39 | P1 stand stdout closed BEFORE the pid line, stderr kept, eoi | 101 | 101 | not found by pid (guard died before the pid line); final pgrep: none / same | identical: `b"\nthread 'main' (<tid>) panicked at /rustc/0ef1bc386059596dada8fb65b50425aab2ea637a/library/std/src/io/stdio.rs:1209:9:\nfailed printing to stdout: …` | identical — pre-existing (R-2): the guard's `println!` of the relay pid panics; the relay is killed by kill_on_drop during the unwind (no process left) |
| 40 | P1 stand stdout closed BEFORE the pid line, stderr closed, eoi | 101 | 101 | not found by pid (guard died before the pid line); final pgrep: none / same | (reader closed) | identical — pre-existing (R-2): the guard's `println!` of the relay pid panics; the relay is killed by kill_on_drop during the unwind (no process left) |
