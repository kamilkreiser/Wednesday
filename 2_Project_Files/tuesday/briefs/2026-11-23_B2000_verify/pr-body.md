Lab tool, the `print` command (spike S6's print path). One commit, `26f4b57a`, on `d804de5e`; `main` is now
`86473f8a` (pull request 38), which shares no path with this branch (`git merge-tree --write-tree` rc 0, tree
`9611a597`). Six files are added (`src/Datasec.Suite.Lab/Commands/Print/` three, `tests/Datasec.Suite.Lab.Tests/Print/`
three) and seven Lab files change. No package, no `Datasec.Suite.slnx` line, no workflow, no `Directory.*` file.

## Why

- Spike S6 needs an IPP Print-Job from a lab machine on either printer generation, on 631 or 443, up to a 600-page PDF.
  The transport (`HttpIppTransport`) and the sender (`PrintJobSender`) are on `main`; nothing drove them.
- The command is the lab tool's first that writes to a device, so it is a dry run unless `--execute` is given.

## What changed

- `print <host> --run <new folder> --pin <sha256> --port <631 or 443> [--path /ipp/print] [--pages 1]
  [--timeout-seconds 300] [--execute]`. The options are parsed before any folder or connection; the pin (64 hex
  characters) and the port are required; pages 1 to 600; time-out 1 to 3600 s.
- Without `--execute`: the document is made and described (pages, length, SHA-256, `ipps://` address); the transport is
  never constructed. With it: ONE `PrintJobSender.SendAsync` over `HttpIppTransport`, `requesting-user-name` `lab`,
  `document-format` `application/pdf`; a refusal or a busy answer is reported and not sent again.
- Exit codes: 0 accepted (or a dry run), 2 usage, 4 TLS refused, 5 run folder exists, 6 refused or busy, 7 any other
  failure. `summary.txt` holds exactly the printed lines.
- `SyntheticPdf.cs`: an in-memory PDF 1.4, A4, one Helvetica text line per page, a true cross-reference table.
- Six paths beyond the Print folders and the registry line, each needed: the Lab project's reference to the transport
  (without it: CS0234 and CS0246), its two lock files (the restore writes them), cell P13's registry list (with the new
  registry line and the old list: P13 red), one word of `DeviceChannel.cs`'s comment and the Lab README (sentences that
  would otherwise say the probe's rules are the tool's).

## What proves it

- Red first (macOS arm64): every test file and a permissive first shape of the command at `d804de5e`: 1968 total, 8
  failed (R01, R04, R05, R06, R08 twice, R09, R10), each by its own assertion. With the command: 1968 / 0 / 1964 / 4.
- 14 mutants, each red on exactly its cells, none surviving.
- A stub printer on 127.0.0.1 (Kestrel, a throwaway certificate made in the test): the dry run makes 0 TCP connections;
  `--execute` makes one connection and one request, whose bytes after the IPP header equal the document; 600 pages in a
  chunked body; a wrong pin, a busy printer and a silent printer each one connection, never a second.
- The synthetic PDF opens in two independent readers (poppler 26.11 and Apple PDFKit) with no repair: 1, 2 and 600
  pages, A4, the right text on the first and last page.
- The branch's push run 45131837251: linux 1964 succeeded, windows 1947 succeeded, rules 634 files, secret scan clean.
  On `main` `86473f8a` plus this commit (tree `9611a597`), locally: 1971 / 0 / 1967 / 4, rules 635 files.

## Still open

- No printer has been reached: the port, the path, a chunked body, HTTP authentication and the PDF's rendering on any
  real printer are not measured.
- The Print README says no pin is printed; a pin typed where an option name belongs is echoed by the usage error
  ("unknown option ..."). A pin is a certificate fingerprint, not a secret.
- A blank `--run` value, or a run folder the tool cannot create, leaves the command as an unhandled exception, not exit
  2 or 7 (the same helper `probe` uses). Nothing is sent in either case.
- The sender's 60 s answer-read bound is not set by `--timeout-seconds`; above 60 s an answer that stalls after its
  headers ends at 60 s.
- `CommandRegistry.cs:19` still says a command needs one line there "and nothing else"; this one needed more.
- Print-URI, job tracking and a PDF from a file are not built.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it: the six extra paths, the dry run, the
required pin and port, the synthetic document, the reason wrapper. No choice in this change is the product owner's.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
