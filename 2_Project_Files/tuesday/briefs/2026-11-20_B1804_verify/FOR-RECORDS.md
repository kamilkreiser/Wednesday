# FOR RECORDS: the logging lane (WP1.10), gate B1804 (round 2 of 2), head 6bcd02e on main 7bf3752

What a records pass must file. The gate wrote none of it anywhere: no ticket, no backlog line, no runbook line, no README line.
State at the time of writing: **NO GO on one finding (a code-scanning alert on one line of test code; VERDICT.md, finding 1).
Everything the first verdict required is closed. Nothing below about the product code changes with the one-line fix.**
Sources: VERDICT.md and CODEQL-FIRST-PR.md of this folder; the builder's STATUS (FOR TUESDAY); the first review's FOR-RECORDS.md,
whose sections 2, 3, 5 and 7 stand unless a line below replaces them.

## 1. Ticket states (changing a ticket is the coordinator's)

- `OXPD2-15` ([WP1.10] Logging deny-list): NOT done. Built and reviewed twice; the head cannot land as it is. After the merge it
  still stays open for the scan of logs from a real sign-in (exit test E1.8), which needs a printer.
- The fix of finding 1: one line (two to be safe) in one test file, and a check of that one commit. It is a third commit on a
  lane whose second round was the last: **the product owner's card, by the round rule.**
- Still owed from the first review: wire the host to the library; one README pass after the wave.

## 2. The master list `OXPD2-1`: the builder's six items and the gate's, each DECIDED BY NOBODY

The builder's six (its STATUS, FOR THE MASTER LIST), each confirmed by the gate's own run:
1. **The named pipe is not closed.** Confirmed and extended (section 4).
2. A name and its value as two VALUES of one dictionary pass (`{ Field = Password, Value = x }`; a list of form fields read
   from JSON has this shape). Reproduced in 6 of 10 rows; a JSON object node is closed by accident of its text form.
3. A name one level deeper than its value passes. Reproduced, 8 of 8 rows (an XML element among them).
4. A text outside the three separators passes. Reproduced, 30 of 40 rows: a space, a tab, an arrow, a bar, a semicolon, XML
   tags, brackets, a slash, a command line (`--password x`), percent-encoded or escaped separators, a scheme word before a value
   (`Bearer x`, `Basic x`), full-width separators, the value first, a twice-escaped JSON text.
5. The 22 plain names that still pass their values (`Passwort`, `Pass`, `Key`, `Auth`, `AuthHeader`, `Pin`, `Code`, `AuthCode`,
   `Card`, `CardValue`, `Pan`, `Session`, `Path`, `FullPath`, `File`, `Attachment`, `DocumentTitle`, `JobName`, `Content`,
   `Message`, `Email`, `UserName`): confirmed by the first review's own name rows at this head (46 of 78 listed, 32 not).
6. The accidental hits of `otp`, `cardno` and `sessionid`: confirmed and MEASURED as a cost (section 3).

The gate's (new; none is named in the comment of the sink):
7. **A pair whose KEY member itself has a listed name passes its value.** `{ SecretName = "ApiKey", Value = x }`,
   `{ TokenType = "Bearer", Value = x }`, `{ CredentialType = "Password", Data = x }`, `{ CookieName = "auth_token", Value = x }`,
   an array of such objects: with `@` the value arrives (5 of 5 rows) and the KEY is what reads `[removed:token]`. The rule's
   own sentence says it (the other member must itself not be under a listed name); the list of limits does not. Rule shape: a
   member under a listed name counts as a name too when its text is on the list (it costs neighbours when a real secret under
   a listed name happens to hold a stem; the two existing cells whose synthetic values hold a stem need other values).
8. **A type named after what it holds passes its value in both forms:** `record Password(Value)`, `ApiKey`, `SessionId`,
   `AccessToken`, a list of them (10 of 10 rows). The type name is not looked up; without `@` the text is
   `Password { Value = x }` and the brace is no separator. Rule shape: look the type tag up as a name; count `{` and `(` after a
   listed name as separators.
9. **Names and values in two parallel lists pass** (a header row and a data row; `Names` beside `Values`): 4 of 6 rows.
10. **The name written in the template text beside a placeholder passes:** `"Password={V}"`, `"password: {P}"`,
    `"Authorization: Bearer {Value}"`: 4 of 4 rows. The written line reads exactly like the text the second rule removes.
    For the kits of the lanes that log: the placeholder itself carries the listed name.
11. The two rules do not agree on what a name is: the list's rule drops every character that is not a letter or a digit
    inside a name; the text rule ends a name at any character but a letter, a digit, an underscore, a hyphen or a dot. A key
    with a space or an invisible character inside the stem is removed in a pair with `@` and passes in the same pair without.
12. **The cost of the fix and what a reader sees (section 3):** the numbers; a replaced neighbour reads `[removed:password]`
    where no password stood; in the shapes of items 2 to 4 and 7 to 10 that text can stand BESIDE the value that was not
    removed (measured: a process start object whose `Arguments` holds `--password x` keeps `Arguments` and replaces its
    other members; a pair `{ SecretName, Value }` replaces the name and keeps the value).
13. **A text a user chooses can remove other fields of the same event (section 3).** A rule for the lanes that log, and a
    design point: whether an audit line may ever be logged as one object.
14. Whether a replaced NEIGHBOUR should read differently from a replaced VALUE (a new word of the same kind as the six
    replacement texts).
15. The words a reader of a scan report or of a log will see that nobody has decided (the builder's item 11, confirmed at the
    head): `[path withheld: entry <n>]`; `.` for the scanned folder; the three rule names `KnownValueInPath`,
    `TokenShapeInPath`, `NotARegularFile`; the message `The list of known values is empty; a scan with no value to search for
    is refused.`; the six `[removed:<class>]` texts now also under names such as `Value`, `Error`, `Outcome`.
16. From the first review, still open and unchanged: whether a left-out value leaves a marker; whether a user's e-mail
    address may be logged; the third package a host bridge needs; a deny-list or an allow-list (every item above is a
    consequence of listing what to remove).

## 3. The cost of the fix, measured (for the master list, with its numbers)

How the events were chosen: 46 event shapes written by the gate BEFORE any was run against the list, five variants of each
(230 events), in five families (request logging 50, errors with context objects 50, configuration dumps 55, counters 40,
timings 35). Property names follow what a .NET server of this kind logs (the web server's own request fields and limits, the
options of cookie, bearer and session set-up, run-time counters, phase timings); the error texts are the run time's and the
platform's own messages. No event holds a token, a session handle, a card string, mail content, a file name or a password, so
every removal is a harmless value lost. Each event was logged once through a plain logger and once through the library, and
the two property trees compared leaf by leaf (`/private/tmp/b1804-gate/logs/attack2-cost.log`).

- **108 of 230 events lose at least one harmless value (47 in 100); 223 of 1210 values (18 in 100).** The rendered message
  changed in the same 108.
- By family: configuration dumps 50 of 55; counters 22 of 40; errors 15 of 50; timings 11 of 35; request logging 10 of 50.
- By cause (events): a name that holds one of the first 21 stems 64; a name that holds one of the 13 added stems 35; the
  sibling rule 28; the text rule 0. Hit by something this fix added: 63 events (19 of them also by an old stem); 45 by old
  stems alone.
- By cause (values): old stems 89; added stems 45; the sibling rule 89.
- The names: `BodyLength`, `MaxRequestBodySize`, `MaxBodyBytes`, `RequestBodyMs`, `ResponseBodyMs` (`body`);
  `HasAuthorization`; `HandlerName`, `HandleLegacyDevices`, `HandleCount` (`handle`); `SaveToken`, `TokenRefreshes`,
  `TokenCacheEntries`, a metric and a stage called `token...` (`token`); `MaxFileNameLength`, `MaxSubjectLength`;
  and by the added stems `HasCookies`, `CookieName`, `CookieHttpOnly`, `CookiesIssued` (`cookie`); `OtpSignIn`,
  `OtpChallenges`, `RootPath` (`otp`); `SessionIdleTimeoutMinutes`, the key `Session:IdleTimeout` (`sessionid`).
- The sibling rule, by the neighbour VALUE that set it off: a configuration key `Session:IdleTimeout` in a list of pairs
  printed as strings (the other five pairs of the list are removed: 25 values); a stage or operation called `token.acquire`;
  the error texts `IDX10223: Lifetime validation failed. The token is expired.`, `Job was not processed: queue paused`,
  `Cannot print: toner low`, `Could not parse the job ticket: unexpected end of data.` (each holds `otp` across two words:
  "not processed", "not print", "not parse"), `An unhandled exception has occurred while executing the request.` (`handle`),
  an error code `InvalidAuthenticationToken`. In each, the text that set the rule off STAYS and its neighbours (code, status,
  request id, retry count) are replaced.

**Can a value an attacker controls remove other fields of the same event: YES, inside one object or one list; NO across the
event's own properties or the entries of a plain dictionary.** Measured (`attack2-blind.log`): an audit object
`{ User, Outcome, Station, Attempts }` logged with `@` keeps all four fields for the user `alice.m`; for the users `nobody`,
`r.chandler`, `a.peabody`, `secretary`, `cookie.monster`, `j.subject`, `otp`, `pwd`, `token` the three other fields read
`[removed:<class>]` and the user name stays. The same fields as separate properties of the event, or as a plain dictionary:
the other fields stay visible for every one of the 12 names tried. As a list of pairs with `@`: only the pair's own label `User` is replaced. A file
name (`handle.pdf`, `nobody.docx`) in a job object does the same. The line is still written and still says who; it no longer
says what happened or where. **A rule for the lanes that log, until someone decides otherwise: an audit fact is a property of
the event with a name of its own, never a member of a logged object or an element of a logged list that also holds text a
user chose.**

## 4. The scanner: what stays open (for the backlog and for the lane that gives the scanner an entry point)

1. **A named pipe.** The comment's sentence is true and one clause short. Measured with the gate's own time bound: with no
   writer the scan gives no result (8 s and 20 s waited); the moment a writer opens the pipe the scan ends with
   `System.NotSupportedException` ("Stream does not support seeking.") thrown out of `LogScanner.Scan`, whatever the writer
   writes: no result for the good files of the folder either, and an exception that `Scan`'s own comment does not list. The
   message holds no path and no value. Never a clean result. A socket file is reported unreadable and the scan goes on. A
   device file: not tested (no privilege to make one). **The builder's length-0 proposal: its premise is wrong in one point
   (the scanner does not get "no text" from a pipe: asking the stream for its length is what throws), and its rule is still
   the right small fix:** an entry that reports length 0 is counted as an empty file and never opened (a pipe and a socket
   both report length 0 here), together with the stream error added to the errors that make a file unreadable. It costs: an
   empty file that cannot be opened is no longer a finding; a pipe is counted as a file read with no line. **Condition for the
   master list: closed before the scanner is given a shell or a pipeline entry point, or before any person is told to run it.**
2. The name of an entry is printed as it is. A file whose name holds a line feed puts lines of its own into the report
   (measured: one unreadable file gave a report of 5 lines, one of them a forged summary line). A file named like the withheld
   text cannot be told from a withheld one. Rule shape: print control characters of a name escaped.
3. The folder the caller gives is read through when it is itself a link (measured). Only entries INSIDE it are never followed.
4. What kind an entry is, is read once at the listing; an entry swapped for a link between the listing and the read is opened
   (DERIVED from the code; not run).
5. On Windows every reparse point is "not a regular file" (the builder's choice (g); UNMEASURED there): files on a volume
   with data deduplication and cloud placeholder files carry that mark. Such a folder would give a finding per file and read
   nothing: never clean, and never useful. The server of this product runs on Windows.
6. The link cell passes without running where the system lets a test make no link; the hosted Windows log shows no output of
   a passing test (`skipped: 0`, 0 lines naming the cell). Whether it ran there cannot be known from the log. Rule shape: the
   cell reports itself as skipped, so that the summary line says so.
7. Carried from the first review and unchanged: a hostile file can make the list of findings very large; nothing can point
   the scanner at a folder from a shell or a pipeline step; the scanner on Windows is untested.

## 5. Controls that are still missing (4 of the gate's 36 valid new mutants leave all 192 tests green)

- N04: in a SEQUENCE only a scalar neighbour of a name is replaced (the structure half has its cell; a tuple of a name and an
  object has none).
- N16: in the text rule only a space counts as white space (no cell puts a tab or a line end between the name, the quotation
  mark and the separator).
- P06: the path of a LINK is not searched (no cell names a link with a known value; the product does search it: measured).
- P13: a path that holds two known values gives a finding for the first only (no cell).
The first review's 52 mutants: 50 killed, 2 no longer apply (`G16`: the listing was rewritten, the builder's stand-in mutant
kills S12 and S14; `G22`: the lines are gone and CR LF files still give their findings). 0 survive.

## 6. Rules for the lanes that log (for their kits; replaces the list of the first review where they differ)

- never put a value, or the NAME of a value, into the template text: the placeholder carries the listed name;
- log a set of named values as a plain generic dictionary with text keys, or as a list of pairs, or as an object with `@`;
  a pair type of your own names its key member `Key` or `Name` and nothing that holds a stem;
- never a name and its value as two values of one dictionary, two properties of one event, or two parallel lists;
- never a type named after a secret as a logged value; never an object without `@` unless its text is known;
- a text that joins a name and a value uses `=`, `:` or `,`; a header value is logged under the header's own listed name;
- an audit fact is a property of the event (section 3);
- name every property from the list of names that ARE listed (46 of the 78 the first review tried, at this head); a harmless
  number carries no stem in its name (section 3 lists what was lost);
- **CodeQL, C#, test code included: no method call with a constant argument that holds `password` or `passwd` whose result
  reaches a logger, a file write or a trace call; no variable, parameter, field or method so named passed to one.**

## 7. Process, for the runbook and the next kits

- **The C# extractor of the local CodeQL runs on this machine** through its managed program under the project's own arm64
  run time (CODEQL-FIRST-PR.md, last section). The gate standard's sentence that it cannot is out of date: the launcher
  cannot, the program can. Every C# lane of this project can be checked before a pull request exists.
- Build processes that outlive a job (the builder's finding): the gate ran every job with node reuse off, the build server
  off and the shared compiler off (three environment settings of its runner) and found 0 processes of its own alive at the
  end of 220 jobs. One compiler server of ANOTHER seat's home was alive at 20:36. The compiler server is found by a name made
  from the user and the compiler's folder, and every lane uses the same folder, so one lane's server can compile another
  lane's code (DERIVED; not proved by a run). Put the three settings into the kits' environment line.
- The wave's lock: taken and released 220 times by the gate's runner, never waited for; highest load at a start 5.02.
- The first review's probe holds its scratch path in three places; a later review changes those three strings and nothing
  else (done here; the file's hash before the change is in VERDICT.md).

## 8. What was not tested (carry forward)

The hosted code-scanning check itself (no pull request exists); the scanner, the links and the instrument on Windows and on
Linux; a device file; an entry swapped between listing and read; peak memory of a scan; known vulnerabilities and signatures
of the two packages; the two publishes, the release guard and the container on this machine (the hosted lines were read); the
hash half of rule R5; any log of a real sign-in; the branch of the secret-store lane (it appeared after the gate's fetch).
