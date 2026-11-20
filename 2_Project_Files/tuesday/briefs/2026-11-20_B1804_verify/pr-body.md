## What this adds

A logging library, `src/Datasec.Suite.Logging`, and its tests, `tests/Datasec.Suite.Logging.Tests` (191 test cells; the solution now runs 192 tests).

**The host does not log through this library yet. Until a later change wires the host to it, the deny-list protects nothing, and the log scanner is a library call that nothing runs.**

## The deny-list

- One public way to build a logger. Every sink sits behind the list. No setting switches it off.
- Six classes (token, session handle, card string, mail content, file name, password) with 34 name stems, as data in one file. A property name is on the list when, in lower case and without separators, it contains a stem. Its value is replaced by the fixed text `[removed:<class>]`.
- Two more rules, for a value that stands beside its name and not under it:
  1. Inside one object or one list: when one value is itself a listed name (a pair with the key `Password` and a value), every other value of that object or list is replaced.
  2. A text that holds a listed name, then `=`, `:` or `,`, then more text (a pair printed as one string, a JSON text, a query string, a header line) is replaced whole.
- A value of an unknown kind, or nested deeper than 32 levels, is left out.

## What the list does not stop

Named in the comment of the sink:

- a value in the text of a message template, in the message of an exception or of an inner exception, in an exception logged as a property, or used as a dictionary key;
- a value under a name that holds no stem and with no listed name beside it: a value alone in a list, a byte array, a positional placeholder, a tuple with element names;
- a name in look-alike, full-width or another script's characters;
- a name and its value logged as two properties of one event, or as two values of one dictionary, or with the name one level deeper than the value;
- a text in which the name and the value are joined by anything but `=`, `:` or `,` (a space, a tab, an arrow, XML tags, a scheme word before a value), in which the value comes first, or which was escaped a second time;
- a structure's type tag.

Measured in review and not yet named in that comment (each passes its value):

- a pair whose key member itself has a listed name (a member called `SecretName` that holds the name, beside a member called `Value`);
- a type named after what it holds (a record called `Password` with one member);
- names and values in two parallel lists (a header row and a data row);
- the name written in the template text beside a placeholder under an unlisted name.

## What the two rules cost

They remove harmless values too. Measured in review on 230 sample log events of a server of this kind that hold no secret (request lines, errors with context objects, configuration dumps, counters, timings): 108 events lose at least one value, 223 of 1210 values in all. 64 events are hit by the first 21 stems alone; 63 by what the later 13 stems and the first rule add (35 by the new stems, 28 by the first rule; the second rule hit none of the sample). The names that cause most of it: `token`, `body`, `cookie`, `handle`, `otp`, `subject`, `sessionid` inside ordinary names such as a body length, a handle count, an idle timeout of a session, a root path.

Two effects a reader of a log should know:

- A replaced neighbour reads `[removed:password]` (or another class) although no password stood there. In some of the shapes the list does not stop, that text stands beside a value that was not removed.
- A text that a user chooses (a user name, a file name) and that holds a stem removes the other values of the same object or list. Values logged as separate properties of the event, or as entries of a plain dictionary with text keys, are not affected.

## The log scanner

- Reads every file of a folder and of its real sub-folders and reports each known value (as it is, JSON-escaped, percent-encoded, base64, URL-safe base64) and every string in the compact form of a JSON Web Token. An empty list of known values is refused.
- A scan that read nothing is not clean; a file it cannot read is a finding.
- A finding never repeats the value or the line. It carries a path relative to the scanned folder; a path that itself holds a known value or a token-shaped string is searched, reported and withheld (`[path withheld: entry n]`). The folder's own path is never printed.
- A symbolic link is reported and never opened or followed.

Not seen or not handled, as the comments name them: a value split over two lines; compressed files; hexadecimal and other encodings; another letter case; base64 of a longer text unless the value starts at a byte offset that is a multiple of 3; a token-shaped string glued to letters, digits, hyphens or underscores before it; a hostile file can make the list of findings large.

**A named pipe in the scanned folder: the scan waits until something opens the pipe for writing.** Measured in review and not in the comment: once that happens the scan ends with an error of the run time and gives no result. Also measured and not in the comment: the name of an entry is printed as it is, line feeds included; a folder that is given as a link is read through the link.

## Packages

`Serilog` `[4.4.0]` and `Serilog.Sinks.File` `[7.0.0]`, pinned exactly and locked by content hash; each declares Apache-2.0 in its own metadata.

## Shared files

Two lines added to `Datasec.Suite.slnx` and two to `Directory.Packages.props`. The root README lists are updated in a later change.

## Not tested

- Logs of a real sign-in, a printer, a simulator or a tenant.
- The packages against known vulnerabilities (the restore's own audit is the only check).
- The scanner on Windows; whether the link test ran on the Windows leg (it passes without running where the system lets a test make no link).
- A device file in a scanned folder.

Every choice inside this change was made by the build's coordinator or by the builder; none is a product decision. Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
