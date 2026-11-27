#!/usr/bin/env python3
"""make_fixtures.py <empty directory> - build the fixture brain for tests/run.sh (ROUND 4: qualify or stay out).

Every file carries one unique token. From the WEDNESDAY seat's point of view:
  xcanaryNN     a planted file that must NOT enter the index
  xneighbourNN  its neighbour, which MUST be in the index
Every planted LESSON qualifies on every clause of the qualify rule except the ONE it is planted for, so its
absence proves that clause and no other. The expectation tables are written beside the tree, in
<tree>/../expect-<tree name>/, and tests/run.sh reads them:
  absent.txt / present.txt   "token|what it proves"
  paths.txt                  the exact set of paths the WEDNESDAY seat must index
  clauses.txt                "lesson file name|clause" for every lesson that must be left out, with its clause
Standard library only.
"""
import os, sys, unicodedata

root = sys.argv[1]
if os.path.exists(root) and os.listdir(root):
    sys.exit("make_fixtures: %s is not empty" % root)

L = "0_Brain/learnings/"
ABSENT, PRESENT, CLAUSES, WED_LESSONS, ROWS = [], [], [], [], []
DS = "P-Datasec/NexusAI"


def raw(rel, data):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if isinstance(data, bytes):
        with open(p, "wb") as f:
            f.write(data)
    else:
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(data)
    return p


w = raw


def row(key, seats="all", status="live", trig="drive", rule=None, fam="learning-loop"):
    return "\t".join([key, status, seats, fam, trig, "-", rule or "When testing: do the thing."])


def les(name, tok, what, clause=None, front="---\ndate: 2026-01-01\ntype: correction\nsource: fixture\nstatus: live\ntier: W\n---\n",
        body="", rows="good", data=None):
    """One lesson. clause None = it must be indexed; else the clause letter it must be left out under.
    rows: 'good' = one plain row scoped all; a list = exactly those index lines; None = no line at all."""
    text = front + "\n# Lesson %s\n\n**The lesson:** the word is %s here.\n%s" % (tok, tok, body)
    raw(L + name, data(tok) if data else text)
    if rows == "good":
        ROWS.append(row(name))
    elif rows:
        ROWS.extend(rows)
    if clause:
        ABSENT.append((tok, "clause (%s): %s" % (clause, what)))
        CLAUSES.append((name, clause))
    else:
        PRESENT.append((tok, what))
        WED_LESSONS.append(name)


def fm(tierline, extra=""):
    return "---\ndate: 2026-02-01\ntype: correction\n%s%sstatus: live\n---\n" % (tierline, extra)


# ====================================================================== the base brain (search, at, check)
les("2026-01-01_alpha-keeps-panes-open.md", "xneighbour01", "lesson, tier W, one row scoped all plus a #2 row",
    body="\n## How to apply\n\nApply xneighbour01apply every time.\n\nA yakword in the body only.\n",
    rows=[row("2026-01-01_alpha-keeps-panes-open.md", trig="pane,report", fam="ghost-text-and-pane-prompts",
              rule="When closing a pane: xneighbour01rule keep it open until the wrap is read."),
          row("2026-01-01_alpha-keeps-panes-open.md#2", trig="wrap", rule="When wrapping: xneighbour01ruletwo write the note.")])
les("2026-01-02_tuesday-sweeps.md", "xneighbour02", "lesson with 'tuesday' in its NAME whose row is scoped all",
    rows=[row("2026-01-02_tuesday-sweeps.md", trig="pane", rule="When booting: xneighbour02rule sweep the projects.")])
les("2026-01-03_what-friday-does.md", "xcanary03", "its only row is scoped friday", "b",
    rows=[row("2026-01-03_what-friday-does.md", "friday", trig="pane", rule="When on the laptop: xcanary03rule do the thing.")])
les("2026-01-05_beta (conflict_on_2026-01-06).md", "xcanary05", "", None)          # a sync copy: excluded by path
PRESENT.pop(); WED_LESSONS.pop(); ABSENT.append(("xcanary05", "lesson, a (conflict_on_ copy (path rule)"))
les("2026-01-06_gamma.pre-0101.md", "xcanary06", "", None)
PRESENT.pop(); WED_LESSONS.pop(); ABSENT.append(("xcanary06", "lesson, .pre- inside a name that still ends .md (path rule)"))
raw(L + "2026-01-01_alpha-keeps-panes-open.md.pre-0101", "---\ntier: W\n---\n# backup\n\nxcanary07\n")
ABSENT.append(("xcanary07", "lesson backup ending .md.pre-0101"))
les("2026-01-08_project-case-one.md", "xcanary08", "tier P-Datasec/HPSM-POC (another client's project)", "c",
    front=fm("tier: P-Datasec/HPSM-POC\n"),
    rows=[row("2026-01-08_project-case-one.md", trig="drive", rule="When in that project: xcanary08rule do the thing.")])
les("2026-01-10_project-case-three.md", "xneighbour10", "lesson, tier P-Secuura/Blockchain (this seat's own client)", front=fm("tier: P-Secuura/Blockchain\n"))
les("2026-01-11_fleet-rule.md", "xneighbour11", "lesson, tier M", front=fm("tier: M\n"),
    rows=[row("2026-01-11_fleet-rule.md", trig="pane,merge", fam="qa-gate-and-merge", rule="When merging: xneighbour11rule read the gate.")])
les("2026-01-16_old-rule.md", "xneighbour16", "superseded lesson", front=fm("tier: W\n").replace("status: live", "status: superseded"),
    rows=[row("2026-01-16_old-rule.md", status="superseded", trig="pane", fam="qa-gate-and-merge", rule="-> 2026-01-11_fleet-rule.md: the old wording.")])
les("2026-01-17_other-seat-only.md", "xcanary17", "its only row is scoped tuesday", "b",
    rows=[row("2026-01-17_other-seat-only.md", "tuesday", trig="pane", rule="When on the other seat: xcanary17rule do it.")])
les("2026-01-21_zebraword-zebraword.md", "xneighbour21z", "lesson found by a title word", body="\nzebraword zebraword zebraword.\n",
    rows=[row("2026-01-21_zebraword-zebraword.md", rule="When testing: xneighbour21zrule say zebraword.")])
ROWS.append(row("2026-01-99_missing-lesson.md", trig="pane", rule="When nothing: xcanary53rule a row whose lesson file does not exist."))
ABSENT += [("xcanary03rule", "the rule line of a lesson left out under (b)"), ("xcanary17rule", "the rule line of a lesson left out under (b)"),
           ("xcanary08rule", "the rule line of a lesson left out under (c)"), ("xcanary53rule", "a row whose lesson file does not exist")]
PRESENT += [("xneighbour01apply", "its second section"), ("xneighbour01rule", "its rule line"), ("xneighbour01ruletwo", "its #2 rule line"),
            ("xneighbour02rule", "its rule line")]

# ====================================================================== clause (a): exactly one well-read row
N = "2026-03-%02d_%s.md"
A = [  # (slug, what, [index lines] built from the file name)
    ("a-no-row", "no row at all (round 3 indexed this on the tier alone)", lambda n: None),
    ("a-key-no-ext", "the only row's key lacks '.md'", lambda n: [row(n[:-3], "tuesday")]),
    ("a-key-quoted", "the only row's key is in double quotes", lambda n: [row('"%s"' % n, "tuesday")]),
    ("a-key-case", "the only row's key differs in case", lambda n: [row(n.upper().replace(".MD", ".md"), "tuesday")]),
    ("a-key-path", "the only row's key is written as a path", lambda n: [row("0_Brain/learnings/" + n, "tuesday")]),
    ("a-key-trailing-space", "the only row's key has a trailing space (scoped all)", lambda n: [row(n + " ")]),
    ("a-key-leading-space", "the only row has a leading space", lambda n: [" " + row(n, "tuesday")]),
    ("a-key-typo", "the only row's key has one letter wrong", lambda n: [row(n.replace("typo", "tpyo"), "tuesday")]),
    ("a-key-wikilink", "the only row's key is a wikilink", lambda n: [row("[[%s]]" % n[:-3], "tuesday")]),
    ("a-tabs-to-spaces", "the row's TABs became spaces", lambda n: [row(n, "tuesday").replace("\t", "    ")]),
    ("a-eight-fields", "a TAB inside the rule field (8 fields)", lambda n: [row(n, "tuesday") + "\tit."]),
    ("a-six-fields", "a row with 6 fields", lambda n: ["\t".join(row(n, "tuesday").split("\t")[:6])]),
    ("a-row-cr", "a row ending in a carriage return", lambda n: [row(n, "tuesday") + "\r"]),
    ("a-hash1", "the only row's key is file.md#1", lambda n: [row(n + "#1", "tuesday")]),
    ("a-good-and-damaged", "a good row scoped all AND a damaged '#x' row for the same lesson", lambda n: [row(n), row(n + "#x", "tuesday")]),
    ("a-two-plain-rows", "two rows with the same key (tuesday, then all)", lambda n: [row(n, "tuesday"), row(n)]),
    ("a-two-hash2-rows", "a plain row and the '#2' key twice", lambda n: [row(n), row(n + "#2"), row(n + "#2", "tuesday")]),
    ("a-commented-row", "its only row is commented out", lambda n: ["# " + row(n, "tuesday")]),
    ("a-comment-names-it", "a good row scoped all, and a comment line below line 1 that names it", lambda n: [row(n), "# moved to tuesday: " + n]),
    ("a-free-text-names-it", "a good row scoped all, and a stray line of prose that names it", lambda n: [row(n), "see %s for the tuesday copy" % n[:-3]]),
    ("a-hash2-only", "a '#2' row and no plain row", lambda n: [row(n + "#2")]),
    ("a-seat-caps", "seats cell 'Tuesday' (the row cannot be read)", lambda n: [row(n, "Tuesday")]),
    ("a-seat-allcaps", "seats cell 'ALL' (not the spec's word 'all')", lambda n: [row(n, "ALL")]),
    ("a-seat-semicolon", "seats cell 'tuesday;friday'", lambda n: [row(n, "tuesday;friday")]),
    ("a-seat-space", "seats cell 'tuesday friday'", lambda n: [row(n, "tuesday friday")]),
    ("a-seat-empty", "an empty seats cell", lambda n: [row(n, "")]),
    ("a-seat-not", "seats cell 'not-wednesday'", lambda n: [row(n, "not-wednesday")]),
    ("a-seat-all-plus", "seats cell 'all,tuesday'", lambda n: [row(n, "all,tuesday")]),
    ("a-seat-twice", "seats cell 'wednesday,wednesday'", lambda n: [row(n, "wednesday,wednesday")]),
    ("a-status-caps", "status cell 'LIVE'", lambda n: [row(n, status="LIVE")]),
    ("a-key-zwsp-other", "a zero-width space inside the key, so it equals this file's name: a second row for it", lambda n: [row(n), row(n[:12] + "​" + n[12:], "tuesday")]),
]
for i, (slug, what, mk) in enumerate(A, 1):
    n = N % (i, slug)
    les(n, "xcanary3%02d" % i, what, "a", rows=mk(n))
les("2026-03-40_a-ok-hash2.md", "xneighbour340", "(a) neighbour: a plain row and a '#2' row, both read",
    rows=[row("2026-03-40_a-ok-hash2.md"), row("2026-03-40_a-ok-hash2.md#2", rule="When testing: xneighbour340two.")])
PRESENT.append(("xneighbour340two", "its #2 rule line"))
nfc = "2026-03-41_café-rule.md"
les(unicodedata.normalize("NFD", nfc), "xneighbour341", "(a) neighbour: file name stored NFD, key written NFC, scoped all", rows=[row(nfc)])
nfc2 = "2026-03-42_café-other.md"
les(unicodedata.normalize("NFD", nfc2), "xcanary342", "file name stored NFD, key NFC, scoped tuesday (the key DOES equal the name once both are NFC)", "b", rows=[row(nfc2, "tuesday")])
les("2026-03-43_a-inject.md", "xneighbour343", "(a) neighbour: a well-read row carrying injection strings",
    rows=["\t".join(["2026-03-43_a-inject.md", "live", "all", "fam'; drop schema brain cascade; --", "drive,$(touch PWNED_trig),`touch PWNED_bt`,\\! touch PWNED_meta", "-",
                     "When: xneighbour343rule \\. \\copy brain.files to program 'touch PWNED_copy' ; '); DROP SCHEMA brain CASCADE; --"])])

# ====================================================================== clause (b): that row names this seat
les("2026-04-01_b-tuesday-friday.md", "xcanary401", "row scoped tuesday,friday", "b", rows=[row("2026-04-01_b-tuesday-friday.md", "tuesday,friday")])
les("2026-04-02_b-plain-other-hash2-mine.md", "xcanary402", "the plain row is scoped tuesday; only a '#2' row names this seat", "b",
    rows=[row("2026-04-02_b-plain-other-hash2-mine.md", "tuesday", rule="When there: xcanary402rulea."),
          row("2026-04-02_b-plain-other-hash2-mine.md#2", "wednesday,friday", rule="When here: xcanary402ruleb.")])
les("2026-04-03_b-ok-wednesday.md", "xneighbour403", "(b) neighbour: row scoped wednesday", rows=[row("2026-04-03_b-ok-wednesday.md", "wednesday")])
les("2026-04-04_b-ok-wed-fri.md", "xneighbour404", "(b) neighbour: row scoped wednesday,friday", rows=[row("2026-04-04_b-ok-wed-fri.md", "wednesday,friday")])
les("2026-04-05_b-ok-hash2-other.md", "xneighbour405", "(b) neighbour: plain row all, '#2' row scoped tuesday (the lesson is in; that rule line is not)",
    rows=[row("2026-04-05_b-ok-hash2-other.md", rule="When here: xneighbour405rule."), row("2026-04-05_b-ok-hash2-other.md#2", "tuesday", rule="When there: xcanary405ruletwo.")])
PRESENT.append(("xneighbour405rule", "its own rule line"))
ABSENT.append(("xcanary405ruletwo", "a '#2' rule line scoped to another seat, inside an indexed lesson"))

# ====================================================================== clause (c): frontmatter and tier
C = [  # (slug, what, the whole head up to and including the closing fence)
    ("no-tier", "no tier line (round 3 called this untagged and indexed it)", fm("")),
    ("mixed", "tier MIXED", fm("tier: MIXED\n")),
    ("ds-bracket", "tier P (Datasec/OXPd)", fm("tier: P (Datasec/OXPd)\n")),
    ("unknown-client", "tier P-Acme/Thing", fm("tier: P-Acme/Thing\n")),
    ("own-bracket", "own client in the bracket spelling, which no real lesson of this seat uses", fm("tier: P (Secuura/Blockchain)\n")),
    ("own-no-project", "P-Secuura/ with no project", fm("tier: P-Secuura/\n")),
    ("w-lower", "tier w (lower case)", fm("tier: w\n")),
    ("w-trailing-space", "tier 'W ' with a trailing space", fm("tier: W \n")),
    ("w-comment", "tier 'W # really the other client'", fm("tier: W # really P-Other\n")),
    ("w-quoted", "tier \"W\" in quotes", fm('tier: "W"\n')),
    ("w-list", "tier [W]", fm("tier: [W]\n")),
    ("capital-key", "key spelled 'Tier:'", fm("Tier: W\n")),
    ("upper-key", "key spelled 'TIER:'", fm("TIER: W\n")),
    ("quoted-key", "key in quotes", fm('"tier": W\n')),
    ("key-space", "'tier :' with a space before the colon", fm("tier : W\n")),
    ("key-suffix", "key 'tier (project):' beside a clean tier line", fm("tier: W\ntier (project): P-Other/X\n")),
    ("key-eq", "'tier = P-Other/X' beside a clean tier line", fm("tier: W\ntier = P-Other/X\n")),
    ("key-tiers", "a second key 'tiers:'", fm("tier: W\ntiers: P-Other/X\n")),
    ("key-tier-note", "a second key 'tier_project:'", fm("tier: W\ntier_project: P-Other/X\n")),
    ("dup-w-other", "tier twice, W first", fm("tier: W\ntier: P-Other/X\n")),
    ("dup-other-w", "tier twice, W last", fm("tier: P-Other/X\ntier: W\n")),
    ("dup-key", "another key given twice", fm("tier: W\nsource: a\nsource: b\n")),
    ("list-item", "'- tier: P-Other/X' beside a clean tier line", fm("tier: W\n- tier: P-Other/X\n")),
    ("nested", "tier nested under meta: beside a clean tier line", fm("tier: W\nmeta:\n  - tier: P-Other/X\n")),
    ("folded", "tier value folded onto the next line", fm("tier:\n  W\n")),
    ("block-scalar", "tier: >- block scalar", fm("tier: >-\n  W\n")),
    ("tab-indent", "tab-indented tier key", fm("\ttier:\tW\n")),
    ("yaml-comment", "a YAML comment line in the block", fm("tier: W\n# tier: P-Other/X\n")),
    ("blank-in-block", "a blank line inside the block", fm("tier: W\n\n")),
    ("value-tier", "another key whose VALUE carries 'tier: P-Other/X'", fm("tier: W\nsource: fixture tier: P-Other/X\n")),
    ("value-tier-paren", "another key whose value carries 'tier (project) = X'", fm("tier: W\nscope: note tier (project) = P-Other/X\n")),
    ("unclosed", "frontmatter never closed", "---\ntier: W\n"),
    ("leading-blank", "a blank line before the frontmatter", "\n" + fm("tier: W\n")),
    ("indented-fence", "one space before the opening fence", " " + fm("tier: W\n")),
    ("fence-space", "a space after the opening fence", fm("tier: W\n").replace("---\n", "--- \n", 1)),
    ("fence-comment", "fence written '--- # frontmatter'", fm("tier: W\n").replace("---\n", "--- # frontmatter\n", 1)),
    ("dashes4", "four dashes as the fence", fm("tier: W\n").replace("---", "----")),
    ("plusplus", "TOML '+++' frontmatter", '+++\ntier = "W"\n+++\n'),
    ("html-first", "a line before the frontmatter", "see below\n" + fm("tier: W\n")),
    ("no-frontmatter", "no frontmatter, a tier line above the heading", "tier: W\n"),
    ("two-blocks", "a second frontmatter block carrying another tier", fm("tier: W\n") + "---\ntier: P-Other/X\n---\n"),
    ("second-block-far", "a second block whose tier line is 80 lines down", fm("tier: W\n") + "---\n" + "".join("k%02d: v\n" % i for i in range(80)) + "tier: P-Other/X\n---\n"),
    ("empty", "an empty file", None),
    ("only-fence", "a file that is only '---'", None),
]
for i, (slug, what, head) in enumerate(C, 1):
    n = "2026-05-%02d_c-%s.md" % (i, slug) if i < 29 else "2026-06-%02d_c-%s.md" % (i - 28, slug)
    tok = "xcanary5%02d" % i
    if head is None:
        les(n, tok, what, "c", data=(lambda t: "") if slug == "empty" else (lambda t: "---"))
        ABSENT.pop()                                    # no token can be planted in an empty file; the clause table carries it
    else:
        les(n, tok, what, "c", front=head)
for j, (slug, tok, what, head, body) in enumerate([
    ("m", "xneighbour560", "tier M", fm("tier: M\n"), ""),
    ("general", "xneighbour561", "project tier whose client is the own client 'general', spaces in the project", fm("tier: P-General/Claude to Claude\n"), ""),
    ("bom", "xneighbour562", "a UTF-8 BOM, then a clean block", "﻿" + fm("tier: W\n"), ""),
    ("more-keys", "xneighbour563", "the other keys real lessons carry", fm("tier: W\n", "supersedes: 2026-01-16_old-rule\nexpires: 2026-12-31\nseats: all\n"), ""),
    ("status-three-tier", "xneighbour564", "a status line that names a 'three-tier-routing' lesson, as real lessons do", fm("tier: W\n", "supersedes: the 70% thresholds in 2026-09-25_three-tier-routing-ornith-cloud\n"), ""),
    ("rule-in-body", "xneighbour565", "a horizontal rule (---) further down the body", fm("tier: W\n"), "\n## Part two\n\n---\n\nAfter the rule.\n"),
    ("words-in-body", "xneighbour566", "the words 'tiers', 'three-tier routing' and 'frontier' in the body", fm("tier: W\n"), "\nThe tiers of the three-tier routing are a frontier: nothing more.\n"),
    ("fences", "xneighbour567", "code fences, one unclosed (headings are not a decider any more)", fm("tier: W\n"), "\n```\n# not a heading\n```\n\n## real heading\n\n~~~\nunclosed fence xneighbour567b\n## never a heading\n"),
    ("bad-date", "xneighbour568", "an impossible frontmatter date", "---\ntier: W\ndate: 2026-13-45\n---\n", ""),
], 40):
    les("2026-06-%02d_c-ok-%s.md" % (j, slug), tok, "(c) neighbour: " + what, front=head, body=body)
PRESENT.append(("xneighbour567b", "text under an unclosed fence"))

# ====================================================================== clause (d): no marker, no other client's name
mixed = "\n## Own case\n\nown words\n\n%s\n## After\n\nafter words\n"
D = [  # (slug, what, body)
    ("marker-ds", "a section marker for the other client", mixed % ("<!-- tier: %s -->\n## Other case\n\nTOKEN\n" % DS)),
    ("marker-own", "a section marker for this seat's OWN client (any marker leaves the lesson out whole)", mixed % "<!-- tier: P-Secuura/Blockchain -->\n## Own marked case\n\nTOKEN\n"),
    ("marker-nested-fence", "a marked section holding nested code fences and a '# comment'", mixed % "<!-- tier: P-Other/X -->\n## Other case\n\n````\n```\n# a comment\n```\nTOKEN\n````\n"),
    ("marker-multiline", "a marker written as a three-line HTML comment", mixed % "<!--\ntier: P-Other/X\n-->\n## Other case\n\nTOKEN\n"),
    ("marker-list", "a marker written as a list item", mixed % "- <!-- tier: P-Other/X -->\n## Other case\n\nTOKEN\n"),
    ("marker-no-tier-word", "an HTML comment naming a project, without the word tier", mixed % "<!-- P-Other/X -->\n## Other case\n\nTOKEN\n"),
    ("comment-plain", "any HTML comment at all", "\n<!-- note to self -->\n\nTOKEN\n"),
    ("comment-close-only", "a stray '-->'", "\nTOKEN -->\n"),
    ("body-tier-line", "a body line 'tier: P-Other/X' (a marker without comment syntax)", mixed % "tier: P-Other/X\n## Other case\n\nTOKEN\n"),
    ("body-tier-bold", "a body line '**Tier:** P-Other/X'", mixed % "**Tier:** P-Other/X\n\nTOKEN\n"),
    ("body-tier-bracket", "a body line '[tier: P-Other/X]'", mixed % "[tier: P-Other/X]\n\nTOKEN\n"),
    ("body-tier-quote", "a body line '> tier = P-Other/X'", mixed % "> tier = P-Other/X\n\nTOKEN\n"),
    ("body-tier-inline", "the words 'tier: P-Other/X' in the middle of a line", "\nThis part is tier: P-Other/X and TOKEN.\n"),
    ("body-tier-linkref", "a link-reference comment '[//]: # (tier: P-Other/X)'", "\n[//]: # (tier: P-Other/X)\n\nTOKEN\n"),
    ("entity", "a numeric character reference spelling the first letter of the word tier", "\n&#116;ier: P-Other/X TOKEN\n"),
]
for i, (slug, what, body) in enumerate(D, 1):
    tok = "xcanary7%02d" % i
    les("2026-07-%02d_d-%s.md" % (i, slug), tok, what, "d", body=body.replace("TOKEN", tok))
# ROUND 4b (ANSWER-7): a lesson that merely NAMES another client is this seat's lesson and MUST be indexed.
OKNAMES = [
    ("name-plain", "the other client's name in the body", "\nThe Datasec seat does it differently. TOKEN\n"),
    ("name-upper", "the name in capitals", "\nDATASEC. TOKEN\n"),
    ("name-domain", "the name inside a domain", "\nmail from someone at datasec.com.au TOKEN\n"),
    ("name-emphasis", "the name split by markdown emphasis", "\nData**sec** and Data`sec` TOKEN\n"),
    ("name-accent", "the name with an accented letter", "\nDàtasec TOKEN\n"),
    ("name-fullwidth", "the name in full-width letters", "\nＤａｔａｓｅｃ TOKEN\n"),
    ("name-heading", "the name in a section heading", "\n## A Datasec-only case\n\nTOKEN\n"),
]
for i, (slug, what, body) in enumerate(OKNAMES, 1):
    tok = "xneighbour74%d" % i
    les("2026-07-4%d_d-ok-%s.md" % (i, slug), tok, "(d) must succeed: " + what, body=body.replace("TOKEN", tok))
les("2026-07-48_laptop_datasec-habit.md", "xneighbour748", "(d) must succeed: the other client's name in the lesson's FILE NAME")
les("2026-07-49_d-ok-name-in-rule.md", "xneighbour749", "(d) must succeed: the other client's name in its rules-index rule line",
    rows=[row("2026-07-49_d-ok-name-in-rule.md", rule="When working for Datasec: xneighbour749rule do it their way.")])
PRESENT.append(("xneighbour749rule", "that rule line"))
les("2026-07-50_d-ok-name-in-frontmatter.md", "xneighbour750", "(d) must succeed: the other client's name in a frontmatter value", front=fm("tier: W\n", "source: the Datasec seat\n"))
les("2026-07-51_d-ok-own-project-names-other.md", "xneighbour751", "(d) must succeed: own client's project tier whose project name carries the other client's name", front=fm("tier: P-Secuura/shared-with-Datasec\n"))
les("2026-07-30_d-ok-own-client.md", "xneighbour730", "(d) neighbour: the seat's OWN client named in the body, and 'data security'", body="\nSecuura keeps its data secure: data security matters.\n")

# ====================================================================== clause (t): plain text
T = [
    ("latin1", "a Latin-1 file (not valid UTF-8)", lambda t: (fm("tier: W\n") + "\n# L\n\ncafé %s\n" % t).encode("latin-1")),
    ("utf16", "a UTF-16 file", lambda t: ("﻿" + fm("tier: W\n") + "\n# L\n\n%s\n" % t).encode("utf-16-le")),
    ("nul", "a NUL byte", lambda t: fm("tier: W\n") + "\n# L\n\n%s \x00 after\n" % t),
    ("rs-byte", "byte 0x1E between two frontmatter keys", lambda t: "---\ndate: 2026-02-02\x1etier: P-Other/X\ntier: W\n---\n\n# L\n\n%s\n" % t),
    ("crlf", "CRLF line endings", lambda t: (fm("tier: W\n") + "\n# L\n\n%s\n" % t).replace("\n", "\r\n")),
    ("cr-only", "CR-only line endings", lambda t: (fm("tier: W\n") + "\n# L\n\n%s\n" % t).replace("\n", "\r")),
    ("form-feed", "a form feed between two frontmatter keys", lambda t: "---\ndate: 2026-02-02\x0ctier: P-Other/X\ntier: W\n---\n\n# L\n\n%s\n" % t),
    ("line-sep", "U+2028 between two frontmatter keys", lambda t: "---\ndate: 2026-02-02 tier: P-Other/X\ntier: W\n---\n\n# L\n\n%s\n" % t),
    ("nel", "U+0085 in the body", lambda t: fm("tier: W\n") + "\n# L\n\n%s\u0085tier: P-Other/X\n" % t),
    ("zwsp", "a zero-width space inside a word", lambda t: fm("tier: W\n") + "\n# L\n\nData​sec %s\n" % t),
    ("soft-hyphen", "a soft hyphen inside a key", lambda t: fm("tier: W\nti­er: P-Other/X\n") + "\n# L\n\n%s\n" % t),
    ("cyrillic", "a Cyrillic look-alike letter", lambda t: fm("tier: W\n") + "\n# L\n\nDаtasec %s\n" % t),
    ("cyrillic-key", "a Cyrillic look-alike in a second tier key", lambda t: fm("tier: W\ntіer: P-Other/X\n") + "\n# L\n\n%s\n" % t),
    ("greek", "a Greek letter", lambda t: fm("tier: W\n") + "\n# L\n\nΔ %s\n" % t),
    ("smallcap", "a Latin small-capital look-alike", lambda t: fm("tier: W\n") + "\n# L\n\nᴅatasec %s\n" % t),
    ("bidi", "a right-to-left override", lambda t: fm("tier: W\n") + "\n# L\n\n‮%s\n" % t),
    ("invalid-utf8", "invalid UTF-8 bytes", lambda t: b"---\ntier: W\n---\n\n# bad bytes\n\n\xff\xfe\xc3\x28 " + t.encode() + b"\n"),
]
for i, (slug, what, data) in enumerate(T, 1):
    les("2026-08-%02d_t-%s.md" % (i, slug), "xcanary8%02d" % i, what, "t", data=data)
les("2026-08-30_t-ok-accents.md", "xneighbour830", "(t) neighbour: accents, an em dash, arrows, a multiplication sign and a tab",
    body="\ncafé naïve — → × 3\tand a tab\n")

# ====================================================================== clause (f): a plain regular file
raw("4_Credentials/secret.md", "# secret\n\nxcanary15\n")
os.symlink("../../4_Credentials/secret.md", os.path.join(root, L + "2026-09-01_f-symlink.md"))
raw("4_Credentials/secret2.md", "---\ntier: W\n---\n\n# s\n\nxcanary680\n")
os.link(os.path.join(root, "4_Credentials/secret2.md"), os.path.join(root, L + "2026-09-02_f-hardlink.md"))
os.mkdir(os.path.join(root, L + "2026-09-03_f-a-directory.md"))
os.mkfifo(os.path.join(root, L + "2026-09-04_f-a-fifo.md"))
for n in ("2026-09-01_f-symlink.md", "2026-09-02_f-hardlink.md", "2026-09-03_f-a-directory.md", "2026-09-04_f-a-fifo.md"):
    ROWS.append(row(n)); CLAUSES.append((n, "f"))
ABSENT += [("xcanary15", "clause (f): a 4_Credentials file reached through a SYMLINK in learnings/"),
           ("xcanary680", "clause (f): a 4_Credentials file HARD-LINKED into learnings/")]
os.symlink("../4_Credentials", os.path.join(root, "0_Brain/skills_link"))
raw("3_Access_Keys/key2.md", "xcanary681\n")
os.makedirs(os.path.join(root, "0_Brain/skills"), exist_ok=True)
# ROUND 5: the symlinked skill (0_Brain/skills/abs-link.md -> 3_Access_Keys/key2.md, token xcanary681) is no longer
# part of the resting tree, because a file that matched the allow-list and is not indexed now makes check AMBER
# (F2). tests/run.sh plants it in section R5-F2 and asserts there that it is counted AND that xcanary681 stays out.
INJ = ["2026-09-10_$(touch PWNED_name1).md", "2026-09-11_`touch PWNED_name2`.md", "2026-09-12_'; drop schema brain cascade; --.md"]
for i, n in enumerate(INJ, 1):
    les(n, "xneighbour92%d" % i, "a lesson whose NAME and body carry injection strings, indexed as plain text",
        body="\n## \\! touch PWNED_head%d\n\n\\.\n\\! touch PWNED_body%d\n\\copy brain.files to program 'touch PWNED_copy%d'\n'); DROP SCHEMA brain CASCADE; --\n$(touch PWNED_sub%d) `touch PWNED_bt%d`\n\\N\n" % (i, i, i, i, i))

raw(L + "families/fam.md", "# family\n\nxcanary52\n")
ABSENT.append(("xcanary52", "learnings/families/ (no recursion)"))

# ====================================================================== the other kinds
w("CLAUDE.md", "# Project rules\n\nIntro text with xneighbour70.\n\n## Rules\n\nSome words before the rules, xneighbour70b.\n\n"
  "0. **Zebraword first.** Everything lives on the drive, xneighbour71, and a good many more plain words follow here so that this row is of ordinary length.\n"
  "   A continuation line of rule 0, xneighbour71b.\n"
  "0a. **Manage.** The word is xneighbour72.\n"
  "3b-i. A sub rule, xneighbour73.\n\n## Session end\n\n1. Distil the session, xneighbour74.\n\n## Other projects\n\n"
  "5. **Never edit files inside other coding projects.** Their agents execute; xneighbour76rule quillwort marshwort.\n")
w("0_Brain/CLAUDE.md", "# Brain routing\n\n## Folders\n\nThe word is xneighbour75.\n")
w("2_Project_Files/CLAUDE.md", "# another rules file, not on the allow-list\n\nxcanary76\n")
w("CLAUDE (conflict_on_2026-01-01).md", "# a sync copy of the rules file\n\nxcanary78\n")
w("2_Project_Files/tuesday/notes.md", "# another seat's folder\n\nxcanary77\n")
for i in range(1, 9):                                # eight lessons that outscore the rules row on 'quillwort marshwort' alone (N9)
    les("2026-10-%02d_quillwort-marshwort-%d.md" % (i, i), "xneighbour95%d" % i, "N9 filler lesson", body="\nquillwort marshwort quillwort marshwort quillwort marshwort.\n")


def ledger(name, token, cites):
    head = "# Correction ledger\n\n| w | Meaning |\n|---|---|\n| 1 | isolated |\n\n## Ledger (newest at top)\n\n| Date | What happened | Type | w | Lesson | Status |\n|---|---|---|---|---|---|\n"
    body = ""
    for i, c in enumerate(cites):
        body += "| 2026-01-2%d | \U0001F7E1 **THE SEAT DID A YAKWORD THING %s** [W] detail. \U0001F511 [[%s]] Rule: say %srule first. | correction | 1 | [[%s]] | done |\n\n" % (i, token, c, token, c)
    w(L + name, head + body)


ledger("_ledger.md", "xneighbour20", ["2026-01-01_alpha-keeps-panes-open", "2026-01-01_alpha-keeps-panes-open",
                                       "2026-01-11_fleet-rule", "2026-01-16_old-rule"])
ledger("_ledger_archive.md", "xneighbour21", ["2026-01-01_alpha-keeps-panes-open"])
ledger("_ledger_friday.md", "xcanary22", ["2026-01-01_alpha-keeps-panes-open"])
ledger("_ledger_friday_archive.md", "xcanary22b", [])
ledger("_ledger_laptop_datasec.md", "xcanary23", ["2026-01-11_fleet-rule", "2026-01-11_fleet-rule", "2026-01-11_fleet-rule"])
ledger("_ledger_laptop_datasec_archive.md", "xcanary23b", [])
ledger("_ledger (conflict_on_2026-01-01).md", "xcanary24", [])
ledger("_ledger.md.pre-0101", "xcanary25", [])
ledger("_ledger_fleet_insights.md", "xcanary26", [])


def daily(rel, tok):
    w(rel, "# 2026-01-20\n\n## Sessions\n- 06:19 — LAUNCH: the word is %s here.\n  a continuation line with %sb in it\n- a bullet with no time, word %sc\n\n## Notes\nA plain paragraph, word %sd.\n" % (tok, tok, tok, tok))


daily("0_Brain/daily/2026-01-20.md", "xneighbour30")
daily("0_Brain/daily/_template.md", "xcanary33")
w("0_Brain/daily/.spoken.log", "xcanary34\n")
daily("0_Brain/daily/2026-01-20 (conflict_on_2026-01-21).md", "xcanary35")
daily("0_Brain/daily/2026-01-20.md.pre-x", "xcanary36")
daily("0_Brain/daily_tuesday/2026-01-20.md", "xcanary37")
daily("0_Brain/daily_friday/2026-01-20.md", "xcanary38")
for name, tok in (("2026-06-01-TUESDAY-handover.md", "xcanary690"), ("2026-06-02_tuеsday.md", "xcanary691"),
                  ("2026-06-03_fri-day.md", "xcanary692"), ("2026-06-04_ｆｒｉｄａｙ.md", "xcanary693")):
    raw("0_Brain/daily/" + name, "# d\n\n## Sessions\n- 06:19 the word is %s here.\n" % tok)
    ABSENT.append((tok, "a daily note whose name is not a plain date"))

w("0_Brain/skills/ritual.md", "# A ritual\n\nThe word is xneighbour40.\n")
w("0_Brain/skills/ritual.md.pre-1", "# A ritual\n\nThe word is xcanary41.\n")
w("0_Brain/skills/tuesday-ritual.md", "# Another seat's ritual\n\nThe word is xneighbour42.\n")
w("0_Brain/skills/_ledger_copy.md", "# a ledger-named file in skills\n\nxcanary43\n")
raw("0_Brain/skills/separator-bytes.md", "# separators\n\nbefore \x1f unit xneighbour910 \x1e record after\n")
w("0_Brain/identity/persona.md", "# Persona\n\nThe word is xneighbour43.\n")
w("0_Brain/people/kam.md", "# Kam\n\nThe word is xneighbour44.\n")
w("1_Project_Definition/Architecture/2026-01-01_design.md", "# A design\n\n## Part one\n\nThe word is xneighbour45.\n")
w("1_Project_Definition/Architecture/2026-01-02_tuesday-vs-wednesday.md", "# Two seats\n\nThe word is xneighbour46.\n")
w("0_Brain/dashboard/data/chat_wednesday.json", '[{"text": "xcanary47"}]\n')
w("0_Brain/dashboard/notes.md", "# dash\n\nxcanary48\n")
w("0_Brain/reference/2026-01-01_x/notes.md", "# ref\n\nxcanary49\n")
w("3_Access_Keys/key.md", "# key\n\nxcanary50\n")
w("0_Brain/tasks/NEXT.md", "# next\n\nxcanary51\n")
raw("0_Brain/tasks/NEXT-PICKUP-TUESDAY.md", "# p\n\nxcanary700\n")
raw("0_Brain/tasks/WEEK-INSTRUCTION-FRIDAY.md", "# p\n\nxcanary701\n")
raw("0_Brain/tasks/NEXT-PICKUP.md", "# p\n\nxtasksown202\n")          # this seat's own; enters only when a scope allows kind pickup
ABSENT += [(t, why) for t, why in (
    ("xcanary22", "the friday ledger and its archive"), ("xcanary23", "the laptop_datasec ledger and its archive"),
    ("xcanary24", "ledger (conflict_on_ copy"), ("xcanary25", "ledger .pre- backup"), ("xcanary26", "_ledger_fleet_insights.md (not in this seat's ledger table)"),
    ("xcanary33", "daily/_template.md"), ("xcanary34", "daily/.spoken.log"), ("xcanary35", "daily (conflict_on_ copy"), ("xcanary36", "daily .pre- backup"),
    ("xcanary37", "daily_tuesday/"), ("xcanary38", "daily_friday/"), ("xcanary41", "skill .pre- backup"), ("xcanary43", "a file named _ledger* in skills/"),
    ("xcanary76", "a CLAUDE.md that is not one of the two allowed"), ("xcanary77", "2_Project_Files/tuesday/"), ("xcanary78", "a (conflict_on_ copy of the root rules file"),
    ("xcanary47", "chat store under 0_Brain/dashboard/"), ("xcanary48", "markdown under 0_Brain/dashboard/"), ("xcanary49", "0_Brain/reference/"),
    ("xcanary50", "3_Access_Keys/"), ("xcanary51", "0_Brain/tasks/ (no allow line)"), ("xcanary700", "another seat's pickup file"),
    ("xcanary701", "another seat's week file"), ("xtasksown202", "this seat's own pickup file (the shipped scope has no pickup line)"))]
PRESENT += [(t, why) for t, why in (
    ("xneighbour20", "this seat's ledger"), ("xneighbour20rule", "a ledger row's rule sentence"), ("xneighbour21", "this seat's ledger archive"),
    ("xneighbour30", "daily bullet"), ("xneighbour30b", "its continuation line"), ("xneighbour30c", "daily bullet with no time"), ("xneighbour30d", "daily plain paragraph"),
    ("xneighbour40", "skill"), ("xneighbour42", "skill with 'tuesday' in its name"), ("xneighbour43", "identity"), ("xneighbour44", "people"),
    ("xneighbour45", "architecture"), ("xneighbour46", "architecture file with 'tuesday' in its name"),
    ("xneighbour70", "rules file: text before the first heading"), ("xneighbour70b", "a section's own text before its numbered rules"),
    ("xneighbour71", "numbered rule 0"), ("xneighbour71b", "its continuation line"), ("xneighbour72", "numbered rule 0a"), ("xneighbour73", "numbered rule 3b-i"),
    ("xneighbour74", "a numbered rule under a second heading"), ("xneighbour75", "0_Brain/CLAUDE.md"), ("xneighbour910", "a skill row holding the two separator bytes"))]

raw(L + "_rules_index.tsv", "# rules index fixture; columns: file, status, seats, family, triggers, enforced_by, rule\n" + "\n".join(ROWS) + "\n")
WED_PATHS = [
    "0_Brain/CLAUDE.md", "0_Brain/daily/2026-01-20.md", "0_Brain/identity/persona.md", "0_Brain/people/kam.md",
    "0_Brain/skills/ritual.md", "0_Brain/skills/tuesday-ritual.md", "0_Brain/skills/separator-bytes.md",
    "1_Project_Definition/Architecture/2026-01-01_design.md", "1_Project_Definition/Architecture/2026-01-02_tuesday-vs-wednesday.md",
    "CLAUDE.md", L + "_ledger.md", L + "_ledger_archive.md", L + "_rules_index.tsv",
] + [L + n for n in WED_LESSONS]
exp = os.path.join(os.path.dirname(os.path.abspath(root)), "expect-" + os.path.basename(os.path.abspath(root)))
os.makedirs(exp, exist_ok=True)
for fname, rows_ in (("absent.txt", ABSENT), ("present.txt", PRESENT), ("clauses.txt", sorted(CLAUSES))):
    with open(os.path.join(exp, fname), "w", encoding="utf-8") as f:
        for tok, what in rows_:
            f.write("%s|%s\n" % (tok, what))
with open(os.path.join(exp, "paths.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(WED_PATHS)) + "\n")
print("fixtures written under %s (%d lessons must qualify, %d must be left out)" % (root, len(WED_LESSONS), len(CLAUSES)))
