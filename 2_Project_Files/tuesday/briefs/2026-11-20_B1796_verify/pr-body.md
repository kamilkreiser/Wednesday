## What this adds

A logging library, `src/Datasec.Suite.Logging`, and its tests, `tests/Datasec.Suite.Logging.Tests` (42 test cells; the solution now runs 43 tests on both legs).

**The host does not log through this library yet. Until a later change wires the host to it, the deny-list protects nothing: every line the server writes today goes through the host's default logging.**

## The deny-list

- One public way to build a logger, `SuiteLoggerFactory.Create`. It writes one JSON event per line to a file. Every sink (the file and any sink the caller adds) sits behind the deny-list. No setting, level or environment variable switches the list off.
- The list is data in one file: six classes (token, session handle, card string, mail content, file name, password) with 21 name stems. A property name is put in lower case, every character that is not a letter or a digit is dropped, and the name is on the list when what is left contains a stem.
- The value of a listed name is replaced by a fixed text, `[removed:<class>]`. The name stays.
- The list is applied to each property of an event and to the members of objects, the entries of dictionaries and the elements of sequences inside it, and so to the rendered message and the JSON line made from them.
- A harmless property whose name holds a stem loses its value too (`TokenCount`, `Handler`, `BodyLength`). That is the accepted cost of the rule.
- A value of a kind the cleaning step does not know, or nested deeper than 32 levels, is left out of the event, with no marker in its place.

### What the deny-list does not stop

As the code comments name it:

- a value typed into the text of a message template;
- a value inside the message of an exception;
- a value used as a dictionary key;
- a value under a name that holds no stem.

Measured in review and not yet named in the code comments:

- An entry under a listed key is removed only when the logging package captured the collection as a dictionary, which it did in review for the plain generic dictionary with text or enumeration keys and for its read-only wrapper. For other key and value collections (a concurrent, sorted or immutable dictionary, a hash table, a list of key and value pairs, request headers logged with their structure) the value under a listed key reaches every sink.
- An object logged as one string (its own text form) under a name that holds no stem arrives whole, with every member it prints.
- A positional placeholder has a number for a name, so its value is never on the list.
- A name spelled with look-alike or full-width characters, or in another script, is not on the list.
- Common names that hold no stem are not on the list, for example `ApiKey`, `Credential`, `Cookie`, `Bearer`, `Pin`, `CardNo`, `SessionId`, `Path` and `JobName`.

## The log scanner

- `LogScanner.Scan(folder, knownValues)` reads every file of a folder and of its sub-folders. It reports each known value it finds as it is, JSON-escaped, percent-encoded, and as standard or URL-safe base64, and it reports every string in the compact form of a JSON Web Token (RFC 7519). It holds no regular expression.
- A scan that read nothing is not clean. A folder that is missing or empty, and a file that cannot be opened, is not valid UTF-8 or holds a NUL character, is each a finding.
- A finding names the file, the line, the column, the rule, the index of the value and the form. It does not repeat the value or the text of the line. It prints the path of the file as it is, so a path that itself holds a known value is repeated in the report, and a known value in a file's name alone is not a finding.
- A known value shorter than 8 characters is refused with an error.
- The scan does not see (as the code comments name it): a value split over two lines; a compressed file (reported unreadable, not read); base64 of a longer text that holds the value at another byte offset; hexadecimal and other encodings; an escape that encodes more characters than the spellings searched; a value nobody listed, unless it is token-shaped; a file too large to hold in one array (reported unreadable).
- Measured in review: base64 of a longer text that STARTS with the value is also missed unless the value's length is a multiple of three bytes; a named pipe in the folder makes the scan wait without end; a link to a folder is followed.
- The scanner is a library call. Nothing runs it over real logs yet.

## Packages

The first third-party packages of this repository, both pinned to one exact version and locked by content hash:

- `Serilog` `[4.4.0]`
- `Serilog.Sinks.File` `[7.0.0]`

Each declares the Apache-2.0 licence in its own package metadata. The library references no other package. The test project adds none beyond the test framework already on `main`.

## Shared files

- `Datasec.Suite.slnx`: two lines added.
- `Directory.Packages.props`: two lines added.
- Nothing else changes outside the two new folders. The Layout and Reserved names lists of the root `README.md` are not updated here; one pass updates them after the related changes have landed.

## Who chose what

Every choice inside this change (the classes, the stems, the matching rule, the replacement text, the two packages and their versions, the forms the scanner searches) was made by the build's coordinator or by the builder. None is a product decision, and each can be changed. The replacement text is a word an administrator may read in a log; it has not been reviewed as a customer-facing word.

## Not tested

- No log of a real sign-in, a printer, a simulator or a tenant has been scanned.
- The review did not check the two packages against any list of known vulnerabilities. The only check is the audit that the package restore itself runs on the pipeline.
- Code scanning has not read this C# code before this pull request; it could not be run on the review machine.
- The Windows leg ran on the hosted runner only.

Nothing is deployed. Nothing was sent to anyone.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
