# B2000 FOR RECORDS (gate G1, round 1 of 2 of lane L4; kit B1992, seat X53; head 26f4b57a)

Who decided: every choice of lane L4 (D1 to D7, Q1 to Q8: the 13 paths, the dry run unless `--execute`, the required
pin and port, one port per run, the synthetic document only, the reason wrapper, the registry comment left for the
records, the gate raised to G1) is the coordinator's (Tuesday's) as coordinator; none is the product owner's. The
word to build tooling that drives the printer is C-71 (his 10:10 message and his 11:07 tap, "Agents drive it"); no
clarification entry rules on a print command (the kit's counts, MEASURED by its drafter). Nothing here is a
customer-facing word.

## From the kit (RELAYED, kit B1992 FOR RECORDS; the gate re-measured each where marked)
- The lab tool's `print` command: one IPP Print-Job of a synthetic PDF through the landed transport and sender, a dry
  run unless `--execute`; the lab tool's first command that is not read-only. Gate: `new HttpIppTransport(` occurs
  once in `src/Datasec.Suite.Lab` (`PrintCommand.cs:218`, inside `SendAsync`, called only from the `--execute` branch
  at `:204`); a dry run makes 0 TCP connections (R01, and the gate's probe A2).
- The lane needed six paths beyond the commission's (D1): the Lab project's reference to the transport and its two lock
  files, cell P13's registry list, one word of the probe channel's doc comment, and the Lab README. Gate: NOREF
  re-run (build rc 1, CS0234 and CS0246) and P13 re-run (`Total: 63, Failed: 1`, only
  `ProbeTests.P13_an_unknown_command_lists_the_registry`, `Collections differ`), each undone and proved.
- `CommandRegistry.cs:19` says "A later command adds its folder under Commands/ and one line here, nothing else." It
  was not true at BASE (P13 pins the list) and is not true of this lane (the reference, the lock files); left
  unchanged (the commission's ONE registry line); a later round's one-line fix (Q6). Gate: the line reads so at the
  head (`awk NR==19`).
- Named limits: a real printer's port, path, chunked bodies, authentication and rendering are unmeasured (H15);
  Print-URI, priority print, job tracking and a PDF from a file are not built (H14); R06's refused connection and R07's
  bound on Windows ran there for the first time on push run 45131837251 and passed (gate: `failed Datasec.` 0 on
  both legs, `Datasec.Suite.Lab.Tests.dll` 4 lines on each).
- Carried, not in this lane: L1's first-run rule (gate B1982 FOUND 1: `probe` with `--plain-discovery-tree` and no
  `--pin`), untouched: this command never calls the probe.

## Deviations of the seat (RELAYED, seat STATUS; the gate agrees with each)
- DEVIATIONS 1: the mutants run and the hosted wait each ran as ONE unchanged call in the background of the shell tool.
- DEVIATIONS 2: two hand-typed clock slips in STATUS and `predictions.txt`, corrected in STATUS, the file left as
  written.
- The seat's H16 (DERIVED, now read by the gate in the source): the sender's `ResponseTimeout` (60 s,
  `PrintJobTypes.cs:26`) is not set by the command; an IPv6 literal host is a usage error (gate: MEASURED, probe B10);
  a repeated option takes its later value (gate: MEASURED for `--pin` and `--port`, probes B4, B5, B6).

## The gate's own, for the records seat (owed items; none filed by the gate)
1. FOUND 1 (Minor): the Print README's "No document byte and no pin is written or printed" is false on one shape: a pin
   typed where an option name is expected is echoed by the usage error `print: unknown option <word>` (probe B1,
   MEASURED: exit 2, 0 TCP connections, the pin in the output). A pin is the SHA-256 of a device's public certificate,
   not a secret. Owed: the parser names an unknown word without echoing a 64-hex-character one, or the sentence is
   scoped to the values the command parsed.
2. FOUND 2 (Minor): the README's exit-code list ("7 any other failure") does not hold for a failure outside the send:
   a blank `--run` value leaves `RunAsync` as an unhandled `System.ArgumentException` (probe B8, MEASURED in-process,
   0 TCP connections), from `RunRecorder.Create` (`ArgumentException.ThrowIfNullOrWhiteSpace`, landed with L1 and used
   the same way by `probe`); a run folder the tool cannot create (permissions, a read-only volume) takes the same path
   (DERIVED). Nothing is sent in either case. Owed: the parser refuses a blank `--run` as usage (2), and the helper's
   I/O failure is caught or named in both READMEs.
3. Named limit (DERIVED): with `--timeout-seconds` above 60, an answer that stalls after its HTTP headers ends at the
   sender's 60 s `ResponseTimeout`, not at the option; the README's "bounds the whole send" holds as an upper bound.
4. Named limit (DERIVED): with `--timeout-seconds` at 15 or below, the connect bound and the send bound are equal, so
   a connection that times out may read `failed: ResponseTimedOut, transport none` rather than `ConnectFailed` (the
   two bounds race); the silent-printer probe C3 read `transport none` at 2 s.
5. MEASURED by the gate (probes, never committed): the dry run holds under every argument order tried: `--execute` as
   the value of `--run` gives a dry run with a run folder named `--execute` (A2, 0 TCP); as the value of `--pages`,
   `--path` or `--pin`, before the host, as `--Execute`, `-execute` or `--execute=true`: exit 2, 0 TCP (A4 to A10);
   `--execute` twice: one send (A3). Every send path makes ONE TCP connection and at most ONE request: accepted (A1,
   C4 600 pages), wrong pin (C1, 0 requests), busy (C2), silent (C3). An upper-case pin is accepted (B3); `localhost`
   is accepted (B9); a host with a path and `--port +631` are refused (B11, B7); a percent-escaped path is sent (B12).
6. MEASURED by the gate: the synthetic PDF (1, 2 and 600 pages, written by the probe) opens in poppler 26.11
   (`pdfinfo`, `pdftotext`: 0 error or warning lines, A4, the page counts, "lab synthetic page 600 of 600") and in
   Apple PDFKit (page counts, every MediaBox 595 x 842, first and last page text) with no repair. Helvetica is not
   embedded (a standard Type 1 font, `pdffonts`); whether a printer renders it is UNMEASURED.
7. Cosmetic: the Lab README's re-flowed Trust and run-folder lines are 177 and 128 characters (`README.md:23` and
   `:29` at the head), past the file's 120-column wrap.
8. Runbook candidate: L5's frozen patches (kit B1997) apply on L4's head tree and on the FK + L4 merge tree
   (`git apply --check` rc 0 for both, in order) and fail at `d804de5e` (rc 1): L5 must land after L4, as ordered.
