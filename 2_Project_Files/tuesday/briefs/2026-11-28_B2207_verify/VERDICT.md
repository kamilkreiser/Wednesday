GATE B2207: GO WITH FINDINGS @ 2bcac02 on main 7ca5e4c

Gate G1, ROUND 1 OF 2 of lane L1 slice 1 (the OXPd 1.x authentication agent on the server: GetPrePromptResult,
GetPostPromptResult, SignOutNotification), one Opus reader (claude-opus-5-5), in-session, read-only, for Tuesday s338.
Kit B2197 (seat X100; S4: Q1 "a" and Q3 "a" IN WORDS; S8 the counting runner 89223aca; every choice the
coordinator's). Head `2bcac02fb4a2889156b6870cb9a029ad33a19ae2` on `b2197/x100-l1-agent-auth`, ONE commit, one parent
`7ca5e4cefb315f57f4490ce245e1fb762dbf9f6d` (PR 65), tree `4699fcbe52ff56a936d8594536f5906b88dfb01c`, 784 files;
`diff --name-status 7ca5e4ce 2bcac02f`: exactly 2 rows, both `A` (Oxpd1AuthenticationAgent.cs +553,
AuthenticationAgentTests.cs +505); author and committer the repository's own identity (masked `k***@datasec.com.au`).
Origin re-measured by gh api GET at 04:42:45 and 04:57:41 AEDT: main 7ca5e4ce both times (did NOT move), open pull
requests 0, `matching-refs/heads/b2197` one row = the head, compare ahead 1 behind 0, open code-scanning alerts 0.
Measured 04:42 to 05:00 AEDT in scratch `fleet/state/s338/g2207/` (`clone`: clone.py draft mode, push URL
`invalid://no-push`, no identity, detached at the head; every mutant and probe ran there and was undone or moved out:
clone porcelain 0 rows at the end). Every heavy job through my copy of the kit's `heavy.py` (8 of 8 tool hashes equal
THE TOOLS; heavy.py 89223aca = S8) under the OXPd wave lock, one holder at a time; no `owner.txt` of anyone else touched;
lock free and 0 processes naming my clone at the end. Nothing to any printer, device, tenant, Azure, Microsoft host or
HP (the only socket was a listener on 127.0.0.1 inside the probe's test process); no Jira; no write to the project
checkout, the seat's lane or GitHub.

## Grades (round 1 of 2): Blocker 0, Major 0, Minor 1, Info 4. Nothing blocks landing; no fix round.

**F1 MINOR (Tuesday's (b)/(c); kit D6 as written): a cancellation thrown by the HANDLER escapes `AnswerAsync` as an
exception even when the request was not cancelled, carrying the handler's exception text to the host.** The filter
`catch (Exception ex) when (ex is not OperationCanceledException)` (`Oxpd1AuthenticationAgent.cs:385`) passes EVERY
cancellation, not only the request's abort that D6 names as its reason. MEASURED (probe P4, request token not
cancelled): a handler throwing `TaskCanceledException("GATEPROBE-detail-0001")` (what an HttpClient time-out inside a
handler throws) -> `THREW TaskCanceledException`, message holds the detail True; `OperationCanceledException` of an
unrelated token -> the same; an `AggregateException` wrapping one -> Receiver fault (caught). Fails CLOSED (no answer,
never Succeeded); the risk is a host that does not catch it: a non-SOAP 500 or a dropped exchange for the device, and
the handler's text in the host's log. Fix shape (one line): `when (ex is not OperationCanceledException ||
!cancellationToken.IsCancellationRequested)`; or L3b catches it (FOR-RECORDS). Gate mutant `gCancelCaught` proves G07's
`handler-canceled` row pins today's behaviour.

**F2 INFO (Tuesday's (a), entity expansion): `MaxCharactersFromEntities = 0` means NO LIMIT in .NET, not "no
expansion".** MEASURED (probe P2 instrument, the same settings with the DTD let through on purpose, NOT the endpoint):
setting 0 -> a 4-level entity expanded to 20,000,000 characters; the default (10,000,000) -> `XmlException ... exceeded
a limit set by MaxCharactersFromEntities`. The endpoint is safe because `DtdProcessing.Prohibit` declares no entity at
all (MEASURED: internal subset, billion laughs, DOCTYPE SYSTEM, an undeclared entity each -> 400 `the request is not a
SOAP 1.2 envelope`, handler 0); `mDtdAllowed` kills the loss of that line. The doc comment "no entity expansion" rests on
Prohibit alone. The same line is in the landed `Oxpd1Soap.cs:104`. Optional: drop it or set a small positive value.

**F3 INFO (Tuesday's (c)): the request's MessageID is echoed as `RelatesTo` in every answer and in every fault after
step 6** (MEASURED in every probe row; G02/G04 assert it). That is a request value in a fault, by the kit's own design
(THE CODE step 6, WS-Addressing's reply rule). It is never the context id or the server context id: MEASURED over 67
probe replies and every `ToString`: the context id, server context id and exception detail appear 0 times; the
`ArgumentException` of `Failed(<1025 chars>)` carries no value (fixed text plus the parameter name).

**F4 INFO (cells): four properties the code holds that no cell pins** (gate mutants, `evidence-mutants.txt`, 13 rows,
8 MATCH): `gBodyTextLost` (text beside the operation in the SOAP body), `gMuOneOnly` (`mustUnderstand="1"`),
`gLeafChildAllowed` (a child element inside a value: `Value` would concatenate it) each SURVIVE with Total 44 Failed 0,
while the probe shows today's code refuses each shape (400 `the body does not hold exactly one element`; 500
MustUnderstand; the leaf rule by read). `gServerCarriedLost` survives as the kit's named R16 limit says. `gOrderLost`
survives as an equivalent mutant (the language and server positions still fix the order; not a gap). The eight that
match: depth pass, message-id bound, server bound, mixed addressing, cancellation filter, content type, text beside the
values, envelope namespace.

**F5 INFO (Tuesday's (a), shapes outside HP's schema and SOAP 1.2; MEASURED, probe P2/P3; none carries a value outside
HP's schema to the handler):** reach the handler: attributes on value elements (`xsi:type`, a foreign one), an element
after the SOAP body, a `mustUnderstand="TRUE"` (not an xs:boolean) or a SOAP 1.1 `mustUnderstand`, an `Action` split by
a child element, two `Action` blocks (the first is read), a content type `action=` naming another operation, a comment,
PI or CDATA inside or between values (each yields the same schema value). Encodings: UTF-8 BOM, UTF-16 LE/BE, UTF-32 and
no-BOM UTF-16 are read; a UTF-8 BOM with `encoding="utf-16"`, UTF-8 bytes declaring utf-16, UTF-16 declaring utf-8, an
unknown encoding and an invalid UTF-8 byte are each refused 400; `encoding="iso-8859-1"` over UTF-8 bytes is read BY THE
DECLARATION (the handler saw a 22-character server context id for 20 sent characters: a mojibake value that is still of
the schema). Refused: an `Action` with white space around it (xs:anyURI would collapse it; how a device writes it is
UNMEASURED: for L1d). Lookalikes all refused: an operation in no namespace, in the agent namespace plus `/`, a
lower-case name, children in no namespace, `xsi:nil` server id, a MessageID in a `wsa/` lookalike namespace marked
mustUnderstand (500).

## The kit's gate list (line 217), each answered

- **`<BASE>..<head>` read whole:** both files read whole by the gate (Read tool). The code follows THE CODE's twelve
  steps in order; the nine frozen texts are present once each (gate script against the kit's literals: old/new/cells
  equal for 9 of 9 rows of the seat's `mutants_l1a.json`, sha256 96a27de3 = STATUS). Seat deviations D-1 to D-8 read and
  accepted (D-3's `UnderstoodNames[0]/[1]` reads behave as named; D-4 eleven texts; D-5 `Operation` null on faults; D-6
  no RelatesTo on the message-id fault, MEASURED).
- **The pin run and each mutant's reds (the gate's own runs):** restore (locked, CI=true) rc 0; build `0 Warning(s)`
  `0 Error(s)`; agent executable `Total: 44, Errors: 0, Failed: 0`; whole solution `total: 2607`, `failed: 0`,
  `succeeded: 2603`, `skipped: 4` (1m12s, no bound reached). Kit mutants: `MUTANTS: 9 of 9 MATCH, 9 of 9 undone equal`
  (reds identical to the seat's lines, incl. mLanguageUnchecked also turning G09 red, inside the listed cells).
- **Any request outside HP's schema reaching the handler:** no value outside the schema does (G06 11 rows; probe 67
  shapes; F5 lists the ignored non-value markup). Boundaries MEASURED: context id 31 refused (cell), 32 and 128
  accepted, 129 refused (cell); server id 256 accepted, 257 refused; a context id holding U+0663 refused; language
  `en-GB` accepted, fullwidth `e` refused; a sign-out carrying a language refused.
- **Resolve anything, expand an entity, read past 64 KiB or 64 levels:** no (F2; 0 connections to a loopback listener
  after DOCTYPE SYSTEM, xml-stylesheet PI, xi:include in and as the body, xml:base, xsi:schemaLocation). Size: 65535 and
  65536 bytes -> 200; 65537 and 70000 -> 400 `too large`; a UTF-8 BOM counts (BOM+65533 = 65536 -> 200, BOM+65534 ->
  400). Depth (XmlReader.Depth, Envelope 0): 63 and 64 -> 200, 65 -> 400 `not a SOAP 1.2 envelope`, in a header block and
  inside the operation. A stream giving 1 or 7 bytes per read -> 200 (752 reads for 751 bytes); an endless stream ->
  400 after exactly 65537 bytes served.
- **Any answer `Succeeded`:** no path. Public static members `Continued, Canceled, Failed` / `Canceled, Failed`, private
  constructors, sealed types; the compiled Agents assembly holds no `Succeeded` string (ASCII or UTF-16); 0 of 87 reply
  bodies hold it (control: `Continued` in 38). A throw, a faulted task, a null task or a null answer -> Receiver 500.
- **Any fault or `ToString` carrying a request value, an id or an exception's text:** F3 (MessageID by design) and F1
  (the handler's own cancellation text escapes as an exception, not in a fault). Otherwise 0, MEASURED.
- **A comment asserting a device behaviour as fact:** none. Every HP quotation was found verbatim in the committed
  descriptions by program (12 of 12); device framing, status codes and time-outs are marked UNMEASURED.
- **The hosted run on both legs (the gate's read, hosted3.py):** `HOSTED 2bcac02f...: PASS` at 2607 / 784, linux
  2603+4, windows 2586+21, guards 28 / 29; the Agents test dll `passed` on linux (1 s) and windows (4 s); `failed
  Datasec.` 0 lines on each. Main's push run `HOSTED 7ca5e4ce...: PASS` at 2564 / 782 / 28 / 29 (re-read, not taken
  from the commission).
- **words.py and gitleaks:** `CONTROL FIRED: 13 of 13`; `WORDS: clean (2 files)` over the added lines and the message;
  `B2[0-9]{3}` and `x100` counts 0 and 0 (control: the kit copy holds 27 B-numbers); gitleaks 8.30.1 control rc 1
  (2 found, the planted file moved to `g2207/_quarantine/gl-control/`), then the two blobs, the message and the added
  lines rc 0 `no leaks found`, and `gitleaks git` over 7ca5e4ce..2bcac02f rc 0. `checks_l1a.py` over the head:
  `CHECKS: 9 of 9 PASS`, every control FIRED. `repo_rules.py` `RULES: clean (784 files)` rc 0.
- **CodeQL:** not run locally (kit FACTS 6); the pull request's own run is the check (landing.txt step 3).

## Tuesday's own points

- **(a) untrusted XML:** answered above (F2, F5, bounds one under / at / one over each).
- **(b) no Succeeded by ANY path, incl. an exception inside the handler:** holds; F1 is the one exception shape that is
  not turned into a fault (it is thrown, never answered).
- **(c) faults, logs, ToString:** the class writes no log line; F3 and F1 as graded.
- **(d) state across requests:** none. Instance fields: one `readonly` handler; statics: `readonly` `Rows` and
  `UnderstoodNames` (never written) and the compiler's lambda caches. MEASURED: two requests held inside the handler at
  once each got their own RelatesTo and code; 64 concurrent requests on one endpoint: 64 of 64 own RelatesTo, 64 of 64
  own values reached the handler.
- **(e) the seat's D-7:** `predictions.txt` sha256 `995f1892...` equals STATUS, last written 03:45:29 (after the rows
  append, before the mutant run 03:53 and the rebase 04:14); it still reads the BASE numbers 2582 / 776 (not edited to
  the new main). The rebased numbers are measured, not carried: the seat's `r2-test.log` reads 2607 / 2603 / 4 with its
  own duration (1m11s vs green-whole's 1m03s); its hosted run and the gate's own whole-solution run both read 2607.

## Not run / limits of this gate

No device, tenant or HP host (the call shapes stay UNMEASURED). CodeQL local. No Windows local run (the hosted windows
leg is the evidence). The gate's probe is in `evidence-probe-source.cs.txt` (never committed). Evidence files in this
folder: `evidence-pin-and-whole.txt`, `evidence-mutants.txt`, `evidence-gate-mutant-rows.json`, `evidence-probes.txt`,
`evidence-hosted-head.txt`, `evidence-checks-and-scans.txt`. The pr-body's own words (`coordinator`, the attribution
line) are the form's; the squash subject, body and title are `WORDS: clean (3 files)` and `SQUASH-SCAN: clean` (#66).
