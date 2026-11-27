#!/usr/bin/env python3
"""qualify_attack.py <work dir> <socket dir> - the third checker's NEW shapes against the qualify rule.
One tree, one rebuild. Every case is one lesson file with a unique token qz<id>tok and (where it has a row)
a rule token qz<id>rule. want = None: must be IN. want = a clause letter: must be OUT, named, under that clause.
want = '?': recorded only (no claim either way is made by the design; the verdict discusses each).
Then: whole-index dump, rebuild report, check, search and at are compared."""
import os, sys, json, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *

work, sock = sys.argv[1], sys.argv[2]
root = os.path.join(work, "tree"); pgd = os.path.join(work, "pg")
os.makedirs(root)
ROWS = base_tree(root)
CASES = []   # (id, want, file name, what)
n_ = [0]


def les(cid, want, what, name=None, front=FM, body="", rows="good", data=None, kind="file"):
    name = name or "2027-03-01_q-%s.md" % cid
    tok = "qz%stok" % cid
    text = front + "\n# Lesson %s\n\nThe word is %s here.\n%s" % (cid, tok, body.replace("TOKEN", tok))
    if kind == "file":
        w(root, L + name, data(tok) if data else text)
    if rows == "good":
        ROWS.append(row(name, rule="When testing: qz%srule do it." % cid))
    elif rows:
        ROWS.extend(r.replace("RULE", "qz%srule" % cid) for r in rows(name))
    CASES.append((cid, want, name, what))
    return name


def fm(tierline, extra=""):
    return "---\ndate: 2027-02-01\ntype: correction\n%s%sstatus: live\n---\n" % (tierline, extra)


R = lambda seats="all", **k: (lambda n: [row(n, seats, rule="When testing: RULE do it.", **k)])
BIG = "x" * 100000

# ------------------------------------------------------------------ (a) exactly one well-read row
les("a01", "a", "key ends in a no-break space (U+00A0), scoped tuesday", rows=lambda n: [row(n + " ", "tuesday", rule="RULE")])
les("a02", "a", "key written with a full-width full stop before md", rows=lambda n: [row(n.replace(".md", "．md"), "tuesday", rule="RULE")])
les("a03", "a", "the only row is on LINE 1 of the index, where a '#' line is the header (written '# <row>')", rows=None)
les("a04", "a", "its row and the next row are joined by a vertical tab instead of a newline", rows=lambda n: [row(n, "tuesday", rule="RULE") + "\x0b" + row("2027-03-01_q-a04b.md", rule="x")])
les("a04b", "a", "the second half of that joined line (a row scoped all for this file)", rows=None)
les("a05", "a", "its row and the next are joined by U+2028", rows=lambda n: [row(n, "tuesday", rule="RULE") + " " + row("2027-03-01_q-a05b.md", rule="x")])
les("a05b", "a", "the second half of that joined line", rows=None)
les("a06", "a", "file name with an accent; one row keyed NFC scoped all and one keyed NFD scoped tuesday (two rows equal the name)",
    name="2027-03-01_q-a06-café.md", rows=lambda n: [row(n, rule="RULE"), row(unicodedata.normalize("NFD", n), "tuesday", rule="x")])
les("a07", "a", "key written with U+2010 HYPHEN where the name has '-'", rows=lambda n: [row(n.replace("q-a07", "q‐a07"), "tuesday", rule="RULE")])
les("a08", "a", "file name has a space before .md, the key has none", name="2027-03-01_q-a08 .md", rows=lambda n: [row(n.replace(" .md", ".md"), "tuesday", rule="RULE")])
les("a09", "a", "seats cell 'all' written with a Cyrillic first letter", rows=lambda n: [row(n, "аll", rule="RULE")])
les("a10", "a", "key 'file.md#2#3'", rows=lambda n: [row(n + "#2#3", "tuesday", rule="RULE")])
les("a11", "a", "a good row scoped all, and a DAMAGED row for a longer file name that contains this stem", rows=lambda n: [row(n, rule="RULE"), row(n[:-3] + "-longer.md", "Tuesday", rule="x")])
les("a12", "a", "a NUL byte in front of its row", rows=lambda n: ["\x00" + row(n, "tuesday", rule="RULE")])
les("a13", "a", "two IDENTICAL good rows scoped all", rows=lambda n: [row(n, rule="RULE"), row(n, rule="RULE")])
les("a14", "a", "a 100,000-character index line that is not a row and names it, beside a good row scoped all", rows=lambda n: [row(n, rule="RULE"), "note " + BIG + " " + n])
les("a15", "a", "key written './file.md'", rows=lambda n: [row("./" + n, "tuesday", rule="RULE")])
les("a16", "a", "key percent-encoded", rows=lambda n: [row(n.replace("_", "%5F"), "tuesday", rule="RULE")])
les("a17", "a", "key 'file.md#02' (leading zero) beside a good plain row", rows=lambda n: [row(n, rule="RULE"), row(n + "#02", "tuesday", rule="x")])
les("a18", "a", "plain row all, '#2' row all, '#2' row again scoped wednesday", rows=lambda n: [row(n, rule="RULE"), row(n + "#2", rule="x"), row(n + "#2", "wednesday", rule="y")])
les("a19", "a", "status cell 'live ' padded with U+2003 EM SPACE", rows=lambda n: [row(n, "tuesday", status="live ", rule="RULE")])
les("a20", "a", "its row has an empty enforced_by field", rows=lambda n: ["\t".join([n, "live", "tuesday", "fam", "drive", "", "RULE"])])
les("a21", "a", "file name upper-case stem, key lower-case", name="2027-03-01_Q-A21.md", rows=lambda n: [row(n.lower(), "tuesday", rule="RULE")])
# neighbours
les("an1", None, "(a) neighbour: plain row plus #2, #3 and #10 rows", rows=lambda n: [row(n, rule="RULE"), row(n + "#2", rule="x2"), row(n + "#3", rule="x3"), row(n + "#10", rule="x10")])
les("an2", None, "(a) neighbour: a 5,000-character rule field with accents", rows=lambda n: [row(n, rule="RULE café " + "y" * 5000)])
les("an3", None, "(a) neighbour: its stem is a prefix of another GOOD lesson's stem", rows="good")
les("an3-more", None, "(a) neighbour: the longer-named lesson", rows="good")
les("an4", None, "(a) neighbour: a file name with spaces, brackets and an apostrophe", name="2027-03-01_q-an4 it's [odd] (name).md", rows="good")
les("an5", None, "(a) neighbour: a 100,000-character RULE field in a well-formed row scoped all", rows=lambda n: [row(n, rule="RULE " + BIG)])

# ------------------------------------------------------------------ (b) that row names this seat
les("b01", "b", "key holds a zero-width space, scoped tuesday (the key equals the name once format characters are removed)", rows=lambda n: [row(n[:14] + "​" + n[14:], "tuesday", rule="RULE")])
les("b02", "b", "row scoped tuesday, status dead", rows=R("tuesday", status="dead"))
les("b03", "b", "row scoped friday,tuesday", rows=R("friday,tuesday"))
les("b04", "b", "plain row tuesday, '#2' wednesday, '#3' all", rows=lambda n: [row(n, "tuesday", rule="RULE"), row(n + "#2", "wednesday", rule="qzb04rule2"), row(n + "#3", rule="qzb04rule3")])
les("b05", "b", "100,000-character rule field, scoped tuesday", rows=lambda n: [row(n, "tuesday", rule="RULE " + BIG)])
les("b06", "b", "row scoped friday whose rule text says 'all seats, wednesday included'", rows=lambda n: [row(n, "friday", rule="When testing: RULE all seats, wednesday included.")])
les("b07", "b", "file name holds 'wednesday', row scoped tuesday", name="2027-03-01_q-b07-wednesday-only.md", rows=R("tuesday"))
les("b08", "b", "superseded row scoped tuesday pointing at the control lesson", rows=lambda n: [row(n, "tuesday", status="superseded", rule="-> 2027-01-01_q-control.md: RULE old")])
les("b09", "b", "row scoped tuesday whose family is 'wednesday' and trigger list holds 'all'", rows=lambda n: [row(n, "tuesday", fam="wednesday", trig="all,wednesday", rule="RULE")])
les("b10", "b", "file name stored NFD, key NFC, scoped friday", name=unicodedata.normalize("NFD", "2027-03-01_q-b10-naïve.md"), rows=lambda n: [row(unicodedata.normalize("NFC", n), "friday", rule="RULE")])
les("b11", "b", "a BOM in front of its row (mid-file), scoped tuesday", rows=lambda n: ["﻿" + row(n, "tuesday", rule="RULE")])
les("bn1", None, "(b) neighbour: scoped friday,wednesday", rows=R("friday,wednesday"))
les("bn2", None, "(b) neighbour: scoped wednesday,tuesday,friday", rows=R("wednesday,tuesday,friday"))
les("bn3", None, "(b) neighbour: scoped wednesday, status dead", rows=R("wednesday", status="dead"))
les("bn4", None, "(b) neighbour: plain all; '#2' tuesday (lesson in, that rule line out)", rows=lambda n: [row(n, rule="RULE"), row(n + "#2", "tuesday", rule="qzbn4ruleTWO")])

# ------------------------------------------------------------------ (c) frontmatter and tier
C = [
    ("c01", "tier value with two spaces after the colon", fm("tier:  W\n")),
    ("c02", "tier value followed by a TAB", fm("tier: W\t\n")),
    ("c03", "a second key 'x-tier'", fm("tier: W\nx-tier: P-Other/X\n")),
    ("c04", "another key whose value is a list '[tier P-Other/X]'", fm("tier: W\naliases: [tier P-Other/X]\n")),
    ("c05", "tier P-Secuura/x/Datasec (a second slash)", fm("tier: P-Secuura/x/Datasec\n")),
    ("c06", "tier 'P-General,Datasec/x'", fm("tier: P-General,Datasec/x\n")),
    ("c07", "tier written with a full-width W", fm("tier: Ｗ\n")),
    ("c08", "closing fence followed by a space (and no other '---' line)", "---\ndate: 2027-02-01\ntier: W\n--- \n"),
    ("c09", "a key with a capital letter beside a clean tier line", fm("tier: W\nDate: 2027-01-01\n")),
    ("c10", "tier W;P-Other/X", fm("tier: W;P-Other/X\n")),
    ("c11", "tier 'W' in single quotes", fm("tier: 'W'\n")),
    ("c12", "tier 'P-Secuura/X' with a no-break space in the project", fm("tier: P-Secuura/X Datasec\n")),
    ("c13", "tier 'W' with a combining acute accent", fm("tier: Ẃ\n")),
    ("c14", "tier key after a YAML document-start with a tag '--- !lesson'", fm("tier: W\n").replace("---\n", "--- !lesson\n", 1)),
    ("c15", "frontmatter closed by '...' (YAML's other end marker), tier W", "---\ndate: 2027-02-01\ntier: W\n...\n"),
    ("c16", "tier: M W", fm("tier: M W\n")),
    ("c17", "tier: P-Datasec/NexusAI (the other client), row scoped all", fm("tier: P-Datasec/NexusAI\n")),
    ("c18", "tier: P-secuuraX/y (own client's name as a prefix of another)", fm("tier: P-secuuraX/y\n")),
    ("c19", "tier: 'P- Secuura/x'", fm("tier: P- Secuura/x\n")),
    ("c20", "a key 'tier' given as 'tier:W' (no space)", fm("tier:W\n")),
    ("c21", "tier W, then the block is closed, then IMMEDIATELY a '+++' block with tier", fm("tier: W\n") + "+++\nx = 1\n+++\n"),
    ("c22", "key 'tier' reached by a YAML merge '<<: {tier: P-Other/X}'", fm("tier: W\n<<: {tier: P-Other/X}\n")),
    ("c23", "an anchor line '&a tier: W'", fm("&a tier: W\n")),
    ("c24", "a key 't_i_e_r' beside the clean one", fm("tier: W\nt_i_e_r: P-Other/X\n")),
]
for cid, what, head in C:
    les(cid, "c", what, front=head)
les("cn1", None, "(c) neighbour: tier P-secuura/x (own client, lower case: the list folds the client's case)", front=fm("tier: P-secuura/x\n"))
les("cn2", None, "(c) neighbour: tier P-Wed/tools (own client 'wed')", front=fm("tier: P-Wed/tools\n"))
les("cn3", None, "(c) neighbour: 400 other keys before the tier line", front="---\n" + "".join("k%03d: v\n" % i for i in range(400)) + "tier: M\n---\n")
les("cn4", None, "(c) neighbour: values holding colons, quotes, a URL and a TAB", front=fm("tier: W\n", "source: \"Kam, 10:42: 'do it'\" https://example.org/x?y=1\twith a tab\n"))
les("cq1", "?", "RECORD: tier P-Secuura/Datasec-NexusAI (own-client tier whose project is the other client's: stated limit)", front=fm("tier: P-Secuura/Datasec-NexusAI\n"))

# ------------------------------------------------------------------ (d) no marker, no tier-like line, no numeric reference
D = [
    ("d01", "'<!---tier: P-Other/X--->' (three dashes)", "\n<!---tier: P-Other/X--->\n## Other\n\nTOKEN\n"),
    ("d02", "comment opened and never closed", "\n<!-- tier: P-Other/X\n## Other\n\nTOKEN\n"),
    ("d03", "markdown-escaped comment '<\\!-- tier: P-Other/X --\\>'", "\n<\\!-- tier: P-Other/X --\\>\n\nTOKEN\n"),
    ("d04", "an HTML tag '<tier value=...>'", "\n<tier value=\"P-Other/X\">\n\nTOKEN\n"),
    ("d05", "an attribute data-tier=\"P-Other/X\" mid-line", "\nA <div data-tier=\"P-Other/X\">block</div> TOKEN\n"),
    ("d06", "'TIER' then a no-break space then a colon, mid-line", "\nThis part is TIER : P-Other/X TOKEN\n"),
    ("d07", "a table row '| tier | P-Other/X |'", "\n| key | value |\n|---|---|\n| tier | P-Other/X |\n\nTOKEN\n"),
    ("d08", "a link reference definition '[tier]: P-Other/X'", "\n[tier]: P-Other/X\n\nTOKEN\n"),
    ("d09", "a footnote '[^tier]: P-Other/X'", "\n[^tier]: P-Other/X\n\nTOKEN\n"),
    ("d10", "an Obsidian comment '%% tier: P-Other/X %%'", "\n%% tier: P-Other/X %%\n## Other\n\nTOKEN\n"),
    ("d11", "the word tier written with a mathematical bold t, then a colon", "\n\U0001d42dier: P-Other/X TOKEN\n"),
    ("d12", "the word written 'TİER:' (dotted capital I)", "\nTİER: P-Other/X TOKEN\n"),
    ("d13", "circled letters spelling TIER, then a colon", "\nⓉⒾⒺⓇ: P-Other/X TOKEN\n"),
    ("d14", "'tier' with a combining grapheme joiner inside, then a colon", "\nti͏er: P-Other/X TOKEN\n"),
    ("d15", "a second fenced block far down the body whose line is 'tier: P-Other/X'", "\n## A\n\ntext\n\n---\ntier: P-Other/X\n---\n\nTOKEN\n"),
    ("d16", "a hexadecimal character reference '&#x74;ier: ...'", "\n&#x74;ier: P-Other/X TOKEN\n"),
    ("d17", "a stray '--&gt;' is fine but '-->' in an arrow is a comment end: 'a --> b'", "\nstep a --> step b TOKEN\n"),
    ("d18", "tier line inside a code fence", "\n```\ntier: P-Other/X\n```\n\nTOKEN\n"),
    ("d19", "a YAML-looking line at the very END of the file, 'tier = P-Other/X' with no newline", "\nTOKEN\n\ntier = P-Other/X"),
    ("d20", "'Tier' as a setext heading over '===='", "\nTier\n====\n\nP-Other/X TOKEN\n"),
]
for cid, what, body in D:
    les(cid, "d", what, body=body)
les("dn1", None, "(d) neighbour: 'frontier:', 'tiered:', 'three-tier routing', 'tiers are'", body="\nThe frontier: nothing. tiered: no. three-tier routing. The tiers are fine. TOKEN\n")
les("dn2", None, "(d) neighbour: named entities that are not numeric (&amp; &lt; &rarr;) and an arrow ->", body="\nA &amp; B &lt; C &rarr; D -> E TOKEN\n")
les("dn3", None, "(d) neighbour: the other client named in the body and in a heading (round 4b)", body="\n## The Datasec case\n\nDatasec asked for it. TOKEN\n")
les("dn4", None, "(d) neighbour: a horizontal rule and a line of dashes '----' in the body", body="\n---\n\n----\n\nTOKEN\n")
# recorded only: shapes the design does not claim to stop (each is discussed in the verdict)
Q = [
    ("dq1", "RECORD: mid-line 'tier&colon; P-Other/X' (a NAMED character reference spelling the colon)", "\nThis part is tier&colon; P-Other/X TOKEN\n"),
    ("dq2", "RECORD: mid-line 'tier&equals;P-Other/X'", "\nThis part is tier&equals;P-Other/X TOKEN\n"),
    ("dq3", "RECORD: an ordered list item '1. Tier P-Other/X' (starts with the word after a number)", "\n1. Tier P-Other/X\n\nTOKEN\n"),
    ("dq4", "RECORD: mid-line 'tier' then FOUR spaces then a colon", "\nThis part is tier    : P-Other/X TOKEN\n"),
    ("dq5", "RECORD: an Obsidian comment naming a project without the word tier '%% P-Other/X %%'", "\n%% P-Other/X %%\n## Other\n\nTOKEN\n"),
    ("dq6", "RECORD: a sentence 'the next section belongs to tier P-Other/X'", "\nThe next section belongs to tier P-Other/X. TOKEN\n"),
    ("dq7", "RECORD: 'tier' with an enclosing circle mark after the t (category Me), then a colon", "\nt⃝ier: P-Other/X TOKEN\n"),
    ("dq8", "RECORD: 'tier -> P-Other/X' mid-line", "\nThis part is tier -> P-Other/X TOKEN\n"),
    ("dq9", "RECORD: a named reference spelling a letter is impossible, but '&Tab;tier: X' at line start", "\n&Tab;tier&colon; P-Other/X TOKEN\n"),
]
for cid, what, body in Q:
    les(cid, "?", what, body=body)

# ------------------------------------------------------------------ (t) plain text
T = [
    ("t01", "two BOMs, then a clean block", lambda t: "﻿﻿" + FM + "\n# L\n\n%s\n" % t),
    ("t02", "a BOM, a zero-width space, then '---'", lambda t: "﻿​" + FM + "\n# L\n\n%s\n" % t),
    ("t03", "U+2060 WORD JOINER inside a body word", lambda t: FM + "\n# L\n\nti⁠er: P-Other/X %s\n" % t),
    ("t04", "DEL (0x7F) in the body", lambda t: FM + "\n# L\n\n%s \x7f\n" % t),
    ("t05", "ESC in the body", lambda t: FM + "\n# L\n\n%s \x1b[0m\n" % t),
    ("t06", "a backspace hiding a letter", lambda t: FM + "\n# L\n\ntiee\x08r: P-Other/X %s\n" % t),
    ("t07", "a private-use character", lambda t: FM + "\n# L\n\n%s \n" % t),
    ("t08", "a language tag character (U+E0074)", lambda t: FM + "\n# L\n\n%s \U000e0074\n" % t),
    ("t09", "dotless i in 'tıer:'", lambda t: FM + "\n# L\n\ntıer: P-Other/X %s\n" % t),
    ("t10", "Hangul filler (an invisible LETTER)", lambda t: FM + "\n# L\n\ntiㅤer %s\n" % t),
    ("t11", "left-to-right mark between frontmatter keys", lambda t: "---\ndate: 2027-01-01\n‎tier: P-Other/X\ntier: W\n---\n\n# L\n\n%s\n" % t),
    ("t12", "vertical tab between two frontmatter keys", lambda t: "---\ndate: 2027-01-01\x0btier: P-Other/X\ntier: W\n---\n\n# L\n\n%s\n" % t),
    ("t13", "an unpaired surrogate encoded as CESU bytes (invalid UTF-8)", lambda t: (FM + "\n# L\n\n%s " % t).encode() + b"\xed\xa0\x80\n"),
    ("t14", "an overlong encoding of '/' (invalid UTF-8)", lambda t: (FM + "\n# L\n\n%s " % t).encode() + b"\xc0\xaf\n"),
    ("t15", "Armenian letter", lambda t: FM + "\n# L\n\n%s ա\n" % t),
    ("t16", "U+FEFF in the middle of the body", lambda t: FM + "\n# L\n\nti﻿er: X %s\n" % t),
    ("t17", "a lone CR in the middle of a body line", lambda t: FM + "\n# L\n\n%s\rtier: P-Other/X\n" % t),
]
for cid, what, data in T:
    les(cid, "t", what, data=data)
les("tn1", None, "(t) neighbour: emoji, box drawing, CJK punctuation, a no-break space and accents", body="\n✅ ─│ 、 a b café Ångström TOKEN\n")
les("tn2", None, "(t) neighbour: a file with no trailing newline and trailing spaces on lines", data=lambda t: FM + "\n# L   \n\n%s   " % t)
les("tn3", None, "(t) neighbour: combining accents written NFD in the body", body="\ncafé naïve TOKEN\n")
les("tq1", "?", "RECORD: Latin letters that do not decompose (sharp s, o-slash, ae): the rule calls them 'not a Latin letter'", body="\nStraße Søren æ TOKEN\n")
les("tq2", "?", "RECORD: a character assigned only in a recent Unicode version (U+1FAE8, 2022): Python-version dependent", body="\n\U0001fae8 TOKEN\n")

# ------------------------------------------------------------------ (f) file level
def mk(name, how):
    p = os.path.join(root, L + name)
    how(p)
    ROWS.append(row(name, rule="When testing: do it."))


w(root, "4_Credentials/fake-secret.md", FM + "\n# s\n\nqzf01tok qzf02tok fake secret\n")
w(root, "elsewhere/own.md", FM + "\n# s\n\nqzf03tok\n")
mk("2027-04-01_q-f01.md", lambda p: os.symlink("../../4_Credentials/fake-secret.md", p)); CASES.append(("f01", "f", "2027-04-01_q-f01.md", "symlink to a fake 4_Credentials file"))
mk("2027-04-01_q-f02.md", lambda p: os.link(os.path.join(root, "4_Credentials/fake-secret.md"), p)); CASES.append(("f02", "f", "2027-04-01_q-f02.md", "hard link to a fake 4_Credentials file"))
mk("2027-04-01_q-f03.md", lambda p: os.symlink(os.path.join(root, "elsewhere/own.md"), p)); CASES.append(("f03", "f", "2027-04-01_q-f03.md", "absolute symlink to a file outside learnings"))
les("f04", None, "(f) control for f05: an ordinary lesson", rows="good")
mk("2027-04-01_q-f05.md", lambda p: os.symlink("2027-03-01_q-f04.md", p)); CASES.append(("f05", "f", "2027-04-01_q-f05.md", "symlink to a sibling lesson in the same folder"))
les("f06", "f", "an own lesson that has a second hard link INSIDE learnings (both names have link count 2)", rows="good")
mk("2027-04-01_q-f07.md", lambda p: os.link(os.path.join(root, L + "2027-03-01_q-f06.md"), p)); CASES.append(("f07", "f", "2027-04-01_q-f07.md", "the other name of that hard-linked lesson"))
mk("2027-04-01_q-f08.md", lambda p: os.symlink("2027-04-01_q-f08.md", p)); CASES.append(("f08", "f", "2027-04-01_q-f08.md", "a symlink to itself (loop)"))
mk("2027-04-01_q-f09.md", lambda p: os.symlink("/nonexistent/x.md", p)); CASES.append(("f09", "f", "2027-04-01_q-f09.md", "a dangling symlink"))
mk("2027-04-01_q-f10.md", lambda p: os.symlink("/dev/zero", p)); CASES.append(("f10", "f", "2027-04-01_q-f10.md", "a symlink to /dev/zero"))
import socket
def mksock(p):
    s = socket.socket(socket.AF_UNIX); short = "/tmp/q4s%d" % os.getpid(); s.bind(short); s.close(); os.rename(short, p)
try:
    mk("2027-04-01_q-f11.md", mksock); CASES.append(("f11", "f", "2027-04-01_q-f11.md", "a Unix socket file"))
except OSError as e:
    print("INSTRUMENT: could not plant the socket file: %s" % e)
les("f12", "f", "a lesson with mode 000", rows="good"); os.chmod(os.path.join(root, L + "2027-03-01_q-f12.md"), 0)
mk("2027-04-01_q-f13.md", lambda p: os.makedirs(p)); w(root, L + "2027-04-01_q-f13.md/inner.md", FM + "\nqzf13tok\n"); CASES.append(("f13", "f", "2027-04-01_q-f13.md", "a directory named like a lesson, holding a file"))
les("fn1", None, "(f) neighbour: a lesson with mode 0444", rows="good"); os.chmod(os.path.join(root, L + "2027-03-01_q-fn1.md"), 0o444)
les("fn2", None, "(f) neighbour: a lesson with an extended attribute", rows="good")
subprocess.run(["/usr/bin/xattr", "-w", "com.apple.metadata:kMDItemComment", "x", os.path.join(root, L + "2027-03-01_q-fn2.md")])
les("fn3", None, "(f) neighbour: a lesson of 2 MB", body="\n" + ("word " * 400000) + "\n")

hdr_a03 = "# " + row("2027-03-01_q-a03.md", "tuesday", rule="When testing: qza03rule do it.")
w(root, L + "_rules_index.tsv", hdr_a03 + "\n" + "\n".join(ROWS) + "\n")
with open(os.path.join(work, "cases.json"), "w") as f:
    json.dump(CASES, f)

# ====================================================================== run
P = lambda s: print(s, flush=True)
rc, out = tool(["rebuild"], root, pgd, sock)
open(os.path.join(work, "rebuild.out"), "w").write(out)
P("rebuild rc %d; last line: %s" % (rc, out.strip().split("\n")[-1][:300]))
if rc != 0:
    P(out[-3000:]); sys.exit(1)
P("Traceback in rebuild output: %d" % out.count("Traceback"))
rep = left_out_from_report(out)
d, err = dump(sock)
if d is None:
    P("pg_dump failed: " + err); sys.exit(1)
open(os.path.join(work, "dump.sql"), "w").write(d)
P("control token qzcontrol in dump: %d ; qzcontrolrule: %d ; fake secret words: %d" % (d.count("qzcontrol"), d.count("qzcontrolrule"), d.count("fake secret")))
bad = 0; tally = {}
for cid, want, name, what in CASES:
    tok, rtok = "qz%stok" % cid, "qz%srule" % cid
    n, nr = d.count(tok), d.count(rtok)
    named = rep.get(name) or rep.get(unicodedata.normalize("NFC", name)) or rep.get(unicodedata.normalize("NFD", name))
    if want is None:
        v = "ok-in" if n and not named else "WRONG: wanted IN, token %d, named %s" % (n, named)
    elif want == "?":
        v = "RECORDED: %s" % ("IN (token %d)" % n if n else "OUT under (%s) [%s]" % named if named else "ABSENT AND NOT NAMED")
    else:
        if n or nr:
            v = "ENTERED: token %d, rule token %d (wanted OUT under %s)" % (n, nr, want)
        elif not named:
            v = "ABSENT BUT NOT NAMED (wanted named under %s)" % want
        elif named[0] != want:
            v = "out, but under (%s) not (%s) [%s]" % (named[0], want, named[1][:90])
        else:
            v = "ok-out (%s) [%s]" % (named[0], named[1][:90])
    k = v.split(":")[0].split(" (")[0].split(",")[0]
    tally[k] = tally.get(k, 0) + 1
    if v.startswith(("WRONG", "ENTERED", "ABSENT")):
        bad += 1
    P("%-8s %-40s %s\n         %s" % (cid, v[:160], "", what))
P("TALLY: %s" % json.dumps(tally, sort_keys=True))
P("special tokens: qzb04rule2 %d qzb04rule3 %d (rule lines of a lesson left out under b: want 0 0); qzbn4ruleTWO %d (a tuesday '#2' line of an indexed lesson: want 0); qzf13tok %d (file inside a directory named like a lesson: want 0)"
  % (d.count("qzb04rule2"), d.count("qzb04rule3"), d.count("qzbn4ruleTWO"), d.count("qzf13tok")))
# counts: rebuild last line, check, status, doctor, report names
last = out.strip().split("\n")[-1]
rc2, cout = tool(["check"], root, pgd, sock); open(os.path.join(work, "check.out"), "w").write(cout)
rc3, sout = tool(["status"], root, pgd, sock); open(os.path.join(work, "status.out"), "w").write(sout)
rc4, dout = tool(["doctor"], root, pgd, sock); open(os.path.join(work, "doctor.out"), "w").write(dout)
P("report names %d left-out lessons; rebuild last line: %s" % (len(rep), last[last.find("; ") + 2:][:200]))
P("check rc %d: %s" % (rc2, [l for l in cout.split("\n") if "left out:" in l]))
P("status rc %d: %s" % (rc3, [l for l in sout.split("\n") if "left_out" in l]))
P("doctor rc %d: %s" % (rc4, dout.strip()[-200:]))
# search + at for every must-be-out case
leaks = 0; nomatch = 0
for cid, want, name, what in CASES:
    if want in (None, "?"):
        continue
    rcs, so = tool(["search", "qz%stok" % cid], root, pgd, sock)
    if "NO MATCH" in so and "(0 results" in so:
        nomatch += 1
    else:
        leaks += 1; P("SEARCH LEAK %s rc %d: %s" % (cid, rcs, so[:300]))
rcs, so = tool(["search", "qzcontrol"], root, pgd, sock)
P("search over %d must-be-out tokens: NO MATCH %d, leaks %d (control: search qzcontrol rc %d, result lines %d)" % (nomatch + leaks, nomatch, leaks, rcs, so.count("q-control.md")))
rca, ao = tool(["at", "drive"], root, pgd, sock); open(os.path.join(work, "at.out"), "w").write(ao)
atleak = [cid for cid, want, name, what in CASES if want not in (None, "?") and ("qz%srule" % cid) in ao]
P("at drive rc %d: %s ; rule tokens of must-be-out cases in it: %s (control qzcontrolrule: %d)" % (rca, ao.split("\n")[0], atleak, ao.count("qzcontrolrule")))
rcs, so = tool(["stop"], root, pgd, sock); P("stop rc %d: %s" % (rcs, so.strip()))
P("RESULT: %d wrong of %d cases" % (bad, len(CASES)))
