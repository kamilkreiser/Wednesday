#!/usr/bin/env python3
"""f1_new.py <work dir> <tool braindb.sh> <sock dir> - NEW fail-closed attacks on the round-3 lesson deciders.

Every case plants ONE lesson (or one marked section) that a reader would call another client's / another
seat's, with a unique token, in a fixture tree. After `rebuild` (the tool's own shipped wednesday.scope, a
byte copy), the whole index is pg_dump'ed and searched for each token.
  LEAK        token present although wanted absent
  named?      whether the rebuild report names the file at all, and under which words
Positive controls: neighbours that MUST be present (instrument can find a token).
Standard library only; scratch cluster only.
"""
import os, sys, subprocess, unicodedata, json

W, TOOL, SOCK = sys.argv[1], sys.argv[2], sys.argv[3]
PGBIN = "/opt/homebrew/opt/postgresql@15/bin"
PG = os.path.join(W, "pg")
os.makedirs(W, exist_ok=True)
L = "0_Brain/learnings/"
HDR = "# rules index — one row per lesson file; columns: file, status, seats, family, triggers, enforced_by, rule\n"


def row(key, seats="all", status="live", rule="A rule line."):
    return "\t".join([key, status, seats, "fam", "pane", "-", rule]) + "\n"


def tool(root, *args):
    env = dict(os.environ, BRAINDB_ROOT=root, BRAINDB_PGDATA=PG, BRAINDB_SOCKDIR=SOCK)
    env.pop("WED_AGENT", None)
    r = subprocess.run(["/bin/bash", TOOL] + list(args), env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return r.returncode, r.stdout.decode("utf-8", "replace")


def dump():
    r = subprocess.run([PGBIN + "/pg_dump", "--data-only", "--schema=brain", "-h", SOCK, "-d", "braindb"],
                       stdout=subprocess.PIPE)
    return r.stdout.decode("utf-8", "replace")


def write_tree(root, files):
    for rel, data in files.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if isinstance(data, str):
            data = data.encode("utf-8")
        with open(p, "wb") as f:
            f.write(data)


def fm(tierline, tok, pre="date: 2026-02-01\ntype: correction\n", post="status: live\n", title="A lesson"):
    return "---\n%s%s%s---\n\n# %s\n\n**The lesson:** the word is %s here.\n" % (pre, tierline, post, title, tok)


DS = "P-Datasec/NexusAI"
cases = []      # (token, want, file name or None, what)
files = {"CLAUDE.md": "# Rules\n\n1. A rule qzneigh00.\n"}
index_rows = [HDR]


def add(n, name, content, what, want="absent", rows=None):
    tok = "qzcase%02dtok" % n if want == "absent" else "qzneigh%02dtok" % n
    if callable(content):
        content = content(tok)
    files[L + name] = content
    cases.append((tok, want, name, what))
    for r in (rows if rows is not None else [row(unicodedata.normalize("NFC", name))]):   # ROUND 4 ADAPTATION: a case with no row gets ONE good row scoped all
        index_rows.append(r)
    return tok


# ---- positive controls
add(1, "2026-02-01_ctl-w.md", lambda t: fm("tier: W\n", t), "control: tier W, row all", "present", [row("2026-02-01_ctl-w.md")])
add(2, "2026-02-01_ctl-own.md", lambda t: fm("tier: P-Secuura/Blockchain\n", t), "control: own project tier, no row", "present")
add(3, "2026-02-01_ctl-untagged.md", lambda t: fm("", t), "control: untagged, no row", "present")
add(4, "2026-02-01_ctl-plainds.md", lambda t: fm("tier: %s\n" % DS, t), "control (absent): plain Datasec project tier")

# ---- frontmatter shapes: every one is a Datasec project lesson to a human reader
add(10, "2026-02-02_crlf.md", lambda t: fm("tier: %s\n" % DS, t).replace("\n", "\r\n"), "CRLF line endings")
add(11, "2026-02-02_cr-only-tier-later.md", lambda t: fm("tier: %s\n" % DS, t).replace("\n", "\r"), "CR-only line endings (classic Mac), tier is the 3rd key")
add(12, "2026-02-02_cr-only-tier-first.md", lambda t: fm("tier: %s\n" % DS, t, pre="").replace("\n", "\r"), "CR-only line endings, tier is the 1st key")
add(13, "2026-02-02_list-item-tier.md", lambda t: fm("- tier: %s\n" % DS, t), "'- tier: P-Datasec/..' (list-item dash before the key) inside the frontmatter")
add(14, "2026-02-02_nested-list-tier.md", lambda t: fm("meta:\n  - tier: %s\n" % DS, t), "tier as a nested list item under meta:")
add(15, "2026-02-02_block-folded.md", lambda t: fm("tier: >-\n  %s\n" % DS, t), "YAML folded block scalar  tier: >-")
add(16, "2026-02-02_block-literal.md", lambda t: fm("tier: |\n  %s\n" % DS, t), "YAML literal block scalar  tier: |")
add(17, "2026-02-02_tier-in-list.md", lambda t: fm("tier:\n  - %s\n" % DS, t), "tier value as a YAML block list")
add(18, "2026-02-02_tier-flow-list.md", lambda t: fm("tier: [W, %s]\n" % DS, t), "tier value as a flow list [W, P-Datasec/..]")
add(19, "2026-02-02_cyrillic-key.md", lambda t: fm("tіer: %s\n" % DS, t), "key 'tier' with a Cyrillic i look-alike")
add(20, "2026-02-02_fullwidth-colon.md", lambda t: fm("tier： %s\n" % DS, t), "full-width colon after tier")
add(21, "2026-02-02_zwsp-key.md", lambda t: fm("​tier: %s\n" % DS, t), "zero-width space before the key")
add(22, "2026-02-02_softhyphen-key.md", lambda t: fm("ti­er: %s\n" % DS, t), "soft hyphen inside the key")
add(23, "2026-02-02_tab-forms.md", lambda t: fm("\ttier:\t%s\t\n" % DS, t), "tabs round key and value")
add(24, "2026-02-02_utf16le.md", lambda t: ("﻿" + fm("tier: %s\n" % DS, t)).encode("utf-16-le"), "UTF-16 LE with BOM")
add(25, "2026-02-02_utf16be.md", lambda t: fm("tier: %s\n" % DS, t).encode("utf-16-be"), "UTF-16 BE, no BOM")
add(26, "2026-02-02_bom-blank-crlf.md", lambda t: ("﻿\n\n" + fm("tier: %s\n" % DS, t)).replace("\n", "\r\n"), "BOM + two blank lines + CRLF")
add(27, "2026-02-02_fence-with-comment-61.md",
    lambda t: "--- # frontmatter\n" + "".join("k%02d: v\n" % i for i in range(62)) + "tier: %s\n---\n\n# T\n\nthe word is %s\n" % (DS, t),
    "fence written '--- # frontmatter' (not recognised), tier line after 62 other keys (beyond the 60-line look)")
add(28, "2026-02-02_fence-comment-yaml-comment.md",
    lambda t: "--- # frontmatter\n# a YAML comment line\ntier: %s\n---\n\n# T\n\nthe word is %s\n" % (DS, t),
    "fence written '--- # frontmatter', then a YAML '# comment' line (read as a heading), then tier")
add(29, "2026-02-02_second-block-far.md",
    lambda t: "---\ndate: 2026-02-02\n---\n---\n" + "".join("k%02d: v\n" % i for i in range(70)) + "tier: %s\n---\n\n# T\n\nthe word is %s\n" % (DS, t),
    "second frontmatter block whose closing fence is 72 lines later, tier at its end")
add(30, "2026-02-02_second-block-45.md",
    lambda t: "---\ndate: 2026-02-02\n---\n---\n" + "".join("k%02d: v\n" % i for i in range(45)) + "tier: %s\n---\n\n# T\n\nthe word is %s\n" % (DS, t),
    "second frontmatter block closing 47 lines later")
add(31, "2026-02-02_lookalike-client.md", lambda t: fm("tier: P-Dаtasec/NexusAI\n", t), "Cyrillic a in the client name of the VALUE")
add(32, "2026-02-02_ls-separator.md", lambda t: fm("date: 2026-02-02 tier: %s\n" % DS, t, pre=""), "U+2028 line separator between date and tier (one physical line for str.split)")
add(33, "2026-02-02_ff-separator.md", lambda t: fm("date: 2026-02-02\x0ctier: %s\n" % DS, t, pre=""), "form feed between date and tier")
add(34, "2026-02-02_rs-separator.md", lambda t: fm("date: 2026-02-02\x1etier: %s\n" % DS, t, pre=""), "byte 0x1E between date and tier (the tool strips 0x1E)")
add(35, "2026-02-02_key-suffix.md", lambda t: fm("tier (project): %s\n" % DS, t), "key written 'tier (project):'")
add(36, "2026-02-02_tier-eq.md", lambda t: fm("tier = %s\n" % DS, t), "'tier = value' (TOML habit, no colon)")
add(37, "2026-02-02_plusplus-fence.md", lambda t: "+++\ntier = \"%s\"\n+++\n\n# T\n\nthe word is %s\n" % (DS, t), "TOML '+++' frontmatter")
add(38, "2026-02-02_fence-nbsp.md", lambda t: fm("tier: %s\n" % DS, t).replace("---\n", "--- \n", 1), "no-break space after the opening fence")
add(39, "2026-02-02_indented-fence.md", lambda t: " " + fm("tier: %s\n" % DS, t), "one space before the opening fence")
add(40, "2026-02-02_html-comment-first.md", lambda t: "<!-- note -->\n" + fm("tier: %s\n" % DS, t), "an HTML comment line before the frontmatter")
add(41, "2026-02-02_value-own-then-deny.md", lambda t: fm("tier: P-Secuura/shared-with-Dаtasec\n", t), "own client, project name carries a look-alike of the denied client", "present")
add(42, "2026-02-02_general-client-ds-project.md", lambda t: fm("tier: P-General/DS-NexusAI\n", t), "client segment 'general', project is the other client's by abbreviation (indexed by design: record only)", "present")
add(43, "2026-02-02_tier-dup-case.md", lambda t: fm("tier: W\nTIER : %s\n" % DS, t), "tier twice, second in capitals with a space before the colon")
add(44, "2026-02-02_tier-quoted-single.md", lambda t: fm("'tier': '%s'\n" % DS, t), "single-quoted key and value")
add(45, "2026-02-02_latin1.md", lambda t: fm("source: café\ntier: %s\n" % DS, t).encode("latin-1"), "Latin-1 encoded file (invalid UTF-8 byte before the tier line)")

# ---- marked sections inside a MIXED lesson (token in the Datasec section)
def mixed(marker_and_section):
    def f(t):
        return fm("tier: MIXED\n", "qzmixedneigh") + "\n## Own case\n\nown words\n\n" + marker_and_section.replace("TOKEN", t) + "\n## After\n\nafter words qzafter\n"
    return f

add(50, "2026-02-03_mk-plain.md", mixed("<!-- tier: %s -->\n## DS case\n\nTOKEN\n" % DS), "control (absent): plain marker")
add(51, "2026-02-03_mk-nested-fence.md", mixed("<!-- tier: %s -->\n## DS case\n\n````\n```\n# a comment inside the code sample\n```\nTOKEN\n````\n" % DS),
    "marked section holding a 4-backtick fence with a 3-backtick fence inside and a '# comment' line")
add(52, "2026-02-03_mk-tilde-in-backtick.md", mixed("<!-- tier: %s -->\n## DS case\n\n```\n~~~\n# shell comment\nTOKEN\n```\n" % DS),
    "marked section: a ``` code block containing a line '~~~' and then a '# shell comment'")
add(53, "2026-02-03_mk-multiline-comment.md", mixed("<!--\ntier: %s\n-->\n## DS case\n\nTOKEN\n" % DS), "marker written as a three-line HTML comment")
add(54, "2026-02-03_mk-trailing-text.md", mixed("<!-- tier: %s --> <!-- reviewed -->\n## DS case\n\nTOKEN\n" % DS), "marker followed by a second comment on the same line")
add(55, "2026-02-03_mk-nospace.md", mixed("<!--tier:%s-->\n## DS case\n\nTOKEN\n" % DS), "marker with no spaces at all")
add(56, "2026-02-03_mk-below-heading.md", mixed("## DS case\n<!-- tier: %s -->\n\nTOKEN\n" % DS), "marker on the line BELOW its heading")
add(57, "2026-02-03_mk-setext.md", mixed("<!-- tier: %s -->\nDS case\n-------\n\nTOKEN\n" % DS), "marker above a setext (underlined) heading")
add(58, "2026-02-03_mk-h3-then-h4.md", mixed("<!-- tier: %s -->\n### DS case\n\nx\n\n#### deeper\n\nTOKEN\n" % DS), "marked ### with a #### under it")
add(59, "2026-02-03_mk-dash-variant.md", mixed("<!-- tier: P–Datasec/NexusAI -->\n## DS case\n\nTOKEN\n"), "marker value with an en dash")
add(60, "2026-02-03_mk-in-list.md", mixed("- <!-- tier: %s -->\n## DS case\n\nTOKEN\n" % DS), "marker written as a list item")
add(61, "2026-02-03_mk-heading-in-quote.md", mixed("<!-- tier: %s -->\n## DS case\n\nx\n\n# \n\nTOKEN\n" % DS), "marked section holding a bare '# ' line")
add(62, "2026-02-03_mk-indented-code-hash.md", mixed("<!-- tier: %s -->\n## DS case\n\nrun this:\n\n    make\n\n# then, as root\n\nTOKEN\n" % DS),
    "marked ## section holding a line '# then, as root' (a real H1 to markdown; span ends there by design: record)", "present")

# ---- rules-index row shapes: lessons tier W whose ONLY row names tuesday
nfc = "2026-02-04_café-rule.md"
add(70, "2026-02-04_ctl-tueonly.md", lambda t: fm("tier: W\n", t), "control (absent): row names tuesday only", rows=[row("2026-02-04_ctl-tueonly.md", "tuesday")])
add(71, unicodedata.normalize("NFD", nfc), lambda t: fm("tier: W\n", t), "file name stored NFD, index key NFC, row tuesday only", rows=[row(nfc, "tuesday")])
add(72, "2026-02-04_key-no-ext.md", lambda t: fm("tier: W\n", t), "index key written without '.md', row tuesday only", rows=[row("2026-02-04_key-no-ext", "tuesday")])
add(73, "2026-02-04_key-quoted.md", lambda t: fm("tier: W\n", t), "index key in double quotes (spreadsheet export), row tuesday only", rows=[row('"2026-02-04_key-quoted.md"', "tuesday")])
add(74, "2026-02-04_key-zwsp.md", lambda t: fm("tier: W\n", t), "zero-width space after the key, row tuesday only", rows=[row("2026-02-04_key-zwsp.md​", "tuesday")])
add(75, "2026-02-04_tabs-to-spaces.md", lambda t: fm("tier: W\n", t), "the row's TABs became 4 spaces (editor), row tuesday only",
    rows=[row("2026-02-04_tabs-to-spaces.md", "tuesday").replace("\t", "    ")])
add(76, "2026-02-04_dup-disagree.md", lambda t: fm("tier: W\n", t), "two rows disagree: tuesday, then all (indexed by ruling: record)", "present",
    rows=[row("2026-02-04_dup-disagree.md", "tuesday"), row("2026-02-04_dup-disagree.md", "all")])
add(77, "2026-02-04_commented-row.md", lambda t: fm("tier: W\n", t), "row commented out with '# ' (tuesday only) - no row, tier alone (record)", "present",
    rows=["# " + row("2026-02-04_commented-row.md", "tuesday")])
add(78, "2026-02-04_seats-space-sep.md", lambda t: fm("tier: W\n", t), "seats written 'tuesday friday' (space, not comma)", rows=[row("2026-02-04_seats-space-sep.md", "tuesday friday")])
add(79, "2026-02-04_seats-allcaps.md", lambda t: fm("tier: W\n", t), "seats written 'ALL' (not 'all'): excluded, loudly? (record)", rows=[row("2026-02-04_seats-allcaps.md", "ALL")])
add(80, "2026-02-04_key-typo.md", lambda t: fm("tier: W\n", t), "index key with one letter wrong (typo), row tuesday only", rows=[row("2026-02-04_key-tpyo.md", "tuesday")])
add(81, "2026-02-04_key-space-inside.md", lambda t: fm("tier: W\n", t), "row with a leading space before the key, tuesday only", rows=[" " + row("2026-02-04_key-space-inside.md", "tuesday")])
add(82, "2026-02-04_row-leading-bom.md", lambda t: fm("tier: W\n", t), "row line starts with a stray BOM mid-file, tuesday only", rows=["﻿" + row("2026-02-04_row-leading-bom.md", "tuesday")])
add(83, "2026-02-04_key-url.md", lambda t: fm("tier: W\n", t), "key written as a wikilink [[name]], tuesday only", rows=[row("[[2026-02-04_key-url]]", "tuesday")])

files[L + "_rules_index.tsv"] = "".join(index_rows)
root = os.path.join(W, "tree-main")
write_tree(root, files)

out = []
def P(s=""):
    print(s); out.append(s)

rc, o = tool(root, "rebuild")
open(os.path.join(W, "rebuild-main.out"), "w").write(o)
P("MAIN TREE rebuild rc=%d ; last line: %s" % (rc, o.strip().split("\n")[-1]))
d = dump() if rc == 0 else ""
open(os.path.join(W, "dump-main.sql"), "w").write(d)
leaks = 0
olines = o.split("\n")
def named(name):
    """Which report words surround the file name (search by NFC and NFD)."""
    hits = []
    for n in set([name, unicodedata.normalize("NFC", name), unicodedata.normalize("NFD", name)]):
        for i, l in enumerate(olines):
            if n in l:
                # find the group heading above: a line beginning with a count, or the UNTAGGED line
                head = ""
                for j in range(i, -1, -1):
                    s = olines[j].strip()
                    if s[:1].isdigit() or s.startswith("UNTAGGED"):
                        head = s[:70]; break
                hits.append(head)
    return sorted(set(hits))
for tok, want, name, what in cases:
    n = d.count(tok)
    got = "present" if n else "absent"
    v = "ok  " if got == want else ("LEAK" if want == "absent" else "MISS")
    if v == "LEAK":
        leaks += 1
    P("%s %-14s want %-7s got %-7s (%d) %s\n       report names it under: %s" % (v, tok, want, got, n, what, named(name) or "NOT NAMED ANYWHERE"))
P("MAIN TREE: %d cases, %d LEAK ; control tokens qzmixedneigh=%d qzafter=%d" % (len(cases), leaks, d.count("qzmixedneigh"), d.count("qzafter")))
rc, o2 = tool(root, "check"); P("check rc=%d: %s" % (rc, o2.strip().split("\n")[0]))

# ---- whole-index variants: each its own tree. tokens: qzidxTUE (W lesson, only row = tuesday), qzidxDS (plain Datasec tier, no row), qzidxOK (W, row all)
def base_files():
    return {"CLAUDE.md": "# Rules\n\n1. A rule.\n",
            L + "2026-03-01_tueonly.md": fm("tier: W\n", "qzidxtue"),
            L + "2026-03-02_dsproj.md": fm("tier: %s\n" % DS, "qzidxds"),
            L + "2026-03-03_ok.md": fm("tier: W\n", "qzidxok")}
good = HDR + row("2026-03-01_tueonly.md", "tuesday") + row("2026-03-03_ok.md", "all")
def swapped():   # columns: file, seats, status, ... (header says so)
    h = "# rules index; columns: file, seats, status, family, triggers, enforced_by, rule\n"
    return h + "\t".join(["2026-03-01_tueonly.md", "tuesday", "live", "fam", "pane", "-", "r"]) + "\n" + "\t".join(["2026-03-03_ok.md", "all", "live", "fam", "pane", "-", "r"]) + "\n"
def swapped2():  # columns: file, status, family, seats, ...   family value 'all' is plausible? use triggers containing 'all'
    h = "# rules index; columns: file, status, triggers, family, seats, enforced_by, rule\n"
    return h + "\t".join(["2026-03-01_tueonly.md", "live", "pane,all", "fam", "tuesday", "-", "r"]) + "\n" + "\t".join(["2026-03-03_ok.md", "live", "pane", "fam", "all", "-", "r"]) + "\n"
variants = [
    ("ctl-good", good, None, "control: well-formed index"),
    ("crlf", good.replace("\n", "\r\n"), None, "CRLF index"),
    ("cr-only", good.replace("\n", "\r"), None, "CR-only index"),
    ("utf16", ("﻿" + good).encode("utf-16-le"), None, "UTF-16 LE index"),
    ("bom", "﻿" + good, None, "UTF-8 BOM index"),
    ("empty", "", None, "0-byte index"),
    ("header-only", HDR, None, "header line only"),
    ("extra-col", "".join(l if l.startswith("#") else l.rstrip("\n") + "\textra\n" for l in good.splitlines(True)), None, "an 8th column on every row"),
    ("cols-swapped-status-seats", swapped(), None, "columns reordered: seats and status swapped (header says so)"),
    ("cols-triggers-in-seats-slot", swapped2(), None, "columns reordered: triggers sit where seats is expected, one trigger is 'all'"),
    ("symlink", good, "symlink", "the index is a symlink to a file outside learnings/"),
    ("hardlink", good, "hardlink", "the index has link count 2"),
    ("mode000", good, "mode000", "the index is unreadable"),
    ("directory", None, "directory", "the index path is a directory"),
    ("fifo", None, "fifo", "the index path is a FIFO"),
    ("spaces-not-tabs", good.replace("\t", "    "), None, "every TAB became 4 spaces"),
    ("one-good-rest-spaces", HDR + row("2026-03-01_tueonly.md", "tuesday").replace("\t", "  ") + row("2026-03-03_ok.md", "all"), None, "the tuesday-only row lost its TABs; the other row is fine"),
    ("dup-disagree-damaged", HDR + row("2026-03-01_tueonly.md", "all") + row("2026-03-01_tueonly.md", "tuesday") + "2026-03-01_tueonly.md\tlive\n" + row("2026-03-03_ok.md", "all"), None, "three rows for one lesson: all, tuesday, and a damaged one"),
    ("nul-in-key", HDR + row("2026-03-01_\x00tueonly.md", "tuesday") + row("2026-03-03_ok.md", "all"), None, "a NUL byte inside the key (stripped on read, so the row applies)"),
    ("second-index-name", None, "othername", "the index is named _rules_index.TSV (capital extension) on this case-sensitive volume"),
]
P()
P("WHOLE-INDEX VARIANTS (want: refused, or qzidxtue and qzidxds absent; qzidxok is the control)")
for tag, content, special, what in variants:
    r = os.path.join(W, "tree-idx-" + tag)
    f = base_files()
    write_tree(r, f)
    ip = os.path.join(r, L, "_rules_index.tsv")
    if special == "symlink":
        os.makedirs(os.path.join(r, "elsewhere"))
        open(os.path.join(r, "elsewhere", "idx.tsv"), "w").write(content)
        os.symlink(os.path.join(r, "elsewhere", "idx.tsv"), ip)
    elif special == "hardlink":
        open(ip, "w").write(content); os.link(ip, os.path.join(r, "idx-second-name.tsv"))
    elif special == "mode000":
        open(ip, "w").write(content); os.chmod(ip, 0)
    elif special == "directory":
        os.makedirs(ip)
    elif special == "fifo":
        os.mkfifo(ip)
    elif special == "othername":
        open(os.path.join(r, L, "_rules_index.TSV"), "w").write(good)
    else:
        with open(ip, "wb") as fh:
            fh.write(content if isinstance(content, bytes) else content.encode("utf-8"))
    rc, o = tool(r, "rebuild")
    open(os.path.join(W, "rebuild-idx-%s.out" % tag), "w").write(o)
    if special == "mode000":
        os.chmod(ip, 0o644)
    if rc != 0:
        msg = [l for l in o.strip().split("\n") if l.strip()][-1][:150]
        P("ok   %-28s REFUSED rc=%d  %s\n       | %s" % (tag, rc, what, msg))
        continue
    d = dump()
    t, s, k = d.count("qzidxtue"), d.count("qzidxds"), d.count("qzidxok")
    v = "ok  " if (t == 0 and s == 0) else "LEAK"
    notes = [l.strip()[:140] for l in o.split("\n") if ("DAMAGED" in l or "rules index:" in l or "tueonly" in l or "REFUSED" in l)]
    P("%s %-28s rc=0 tueonly=%d dsproj=%d ok(control)=%d  %s" % (v, tag, t, s, k, what))
    for nline in notes:
        P("       | " + nline)
rc, o = tool(root, "stop"); P("stop: " + o.strip().split("\n")[-1])
open(os.path.join(W, "f1_new_result.txt"), "w").write("\n".join(out) + "\n")
