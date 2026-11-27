#!/usr/bin/env python3
"""make_fixtures.py <empty directory> - build the fixture brain for tests/run.sh.

Every file carries one unique token. From the WEDNESDAY seat's point of view:
  xcanaryNN     a planted file (or section) that must NOT enter the index
  xneighbourNN  its neighbour, which MUST be in the index
tests/run.sh holds the expectation tables. Standard library only.
"""
import os, sys

root = sys.argv[1]
if os.path.exists(root) and os.listdir(root):
    sys.exit("make_fixtures: %s is not empty" % root)


def w(rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)


def lesson(name, tier, token, extra="", status="live"):
    fm = "---\ndate: %s\ntype: correction\nsource: fixture\nstatus: %s\n" % (name[:10], status)
    if tier is not None:
        fm += "tier: %s\n" % tier
    fm += "---\n\n"
    title = name[11:-3].replace("-", " ")
    w("0_Brain/learnings/" + name, fm + "# Lesson about %s\n\n**The lesson:** the word is %s here.\n\n## How to apply\n\nApply %sapply every time.\n%s" % (title, token, token, extra))


L = "0_Brain/learnings/"
lesson("2026-01-01_alpha-keeps-panes-open.md", "W", "xneighbour01", extra="\nA yakword in the body only.\n")
lesson("2026-01-02_tuesday-sweeps.md", "W", "xneighbour02")
lesson("2026-01-03_what-friday-does.md", "W", "xcanary03")
lesson("2026-01-04_laptop_datasec-habit.md", "W", "xneighbour04")
lesson("2026-01-05_beta (conflict_on_2026-01-06).md", "W", "xcanary05")
lesson("2026-01-06_gamma.pre-0101.md", "W", "xcanary06")
lesson("2026-01-01_alpha-keeps-panes-open.md.pre-0101", "W", "xcanary07")
lesson("2026-01-08_project-case-one.md", "P-Datasec/HPSM-POC", "xcanary08")
lesson("2026-01-09_project-case-two.md", "P (Datasec/OXPd)", "xcanary09")
lesson("2026-01-10_project-case-three.md", "P-Secuura/Blockchain", "xneighbour10")
lesson("2026-01-11_fleet-rule.md", "M", "xneighbour11")
lesson("2026-01-12_untagged.md", None, "xneighbour12")
lesson("2026-01-13_unknown-project.md", "P-Acme/Thing", "xcanary13")
lesson("2026-01-14_mixed.md", "MIXED", "xneighbour14", extra=(
    "\n<!-- tier: P-Datasec/NexusAI -->\n## A case from the other client\n\nThe word is xcanary14 here.\n"
    "\n<!-- tier: P-Secuura/Blockchain -->\n## A case from this client\n\nThe word is xneighbour14b here.\n"
    "\n## After the cases\n\nThe word is xneighbour14c here.\n"))
lesson("2026-01-16_old-rule.md", "W", "xneighbour16", status="superseded")
lesson("2026-01-17_other-seat-only.md", "W", "xcanary17")
lesson("2026-01-19_two-rules.md", "W", "xneighbour19")
lesson("2026-01-21_zebraword-zebraword.md", "W", "xneighbour21z", extra="\nzebraword zebraword zebraword.\n")
w("CLAUDE.md", "# Project rules\n\nIntro text with xneighbour70.\n\n## Rules\n\nSome words before the rules, xneighbour70b.\n\n"
  "0. **Zebraword first.** Everything lives on the drive, xneighbour71, and a good many more plain words follow here so that this row is of ordinary length.\n"
  "   A continuation line of rule 0, xneighbour71b.\n"
  "0a. **Manage.** The word is xneighbour72.\n"
  "3b-i. A sub rule, xneighbour73.\n\n## Session end\n\n1. Distil the session, xneighbour74.\n")
w("0_Brain/CLAUDE.md", "# Brain routing\n\n## Folders\n\nThe word is xneighbour75.\n")
w("2_Project_Files/CLAUDE.md", "# another rules file, not on the allow-list\n\nxcanary76\n")
w("CLAUDE (conflict_on_2026-01-01).md", "# a sync copy of the rules file\n\nxcanary78\n")
w("2_Project_Files/tuesday/notes.md", "# another seat's folder\n\nxcanary77\n")
w("4_Credentials/secret.md", "# secret\n\nxcanary15\n")
os.symlink("../../4_Credentials/secret.md", os.path.join(root, L + "2026-01-15_link.md"))
os.symlink("../4_Credentials", os.path.join(root, "0_Brain/skills_link"))
w(L + "families/fam.md", "# family\n\nxcanary52\n")

rows = [
    "# rules index fixture; columns: file, status, seats, family, triggers, enforced_by, rule",
    "2026-01-01_alpha-keeps-panes-open.md\tlive\tall\tghost-text-and-pane-prompts\tpane,report\t-\tWhen closing a pane: xneighbour01rule keep it open until the wrap is read.",
    "2026-01-01_alpha-keeps-panes-open.md#2\tlive\tall\trituals-wrap-and-notes\twrap\t-\tWhen wrapping: xneighbour01ruletwo write the note.",
    "2026-01-02_tuesday-sweeps.md\tlive\tall\tlearning-loop\tpane\t-\tWhen booting: xneighbour02rule sweep the projects.",
    "2026-01-03_what-friday-does.md\tlive\tfriday\tlearning-loop\tpane\t-\tWhen on the laptop: xcanary03rule do the thing.",
    "2026-01-08_project-case-one.md\tlive\tall\tclient-isolation\tpane\t-\tWhen in that project: xcanary08rule do the thing.",
    "2026-01-11_fleet-rule.md\tlive\tall\tqa-gate-and-merge\tpane,merge\t-\tWhen merging: xneighbour11rule read the gate.",
    "2026-01-12_untagged.md\tlive\tall\tlearning-loop\treport\t-\tWhen reporting: xneighbour12rule count first.",
    "2026-01-14_mixed.md\tlive\tall\tchecks-that-can-fail\tverify\t-\tWhen verifying: xneighbour14rule run a control.",
    "2026-01-16_old-rule.md\tsuperseded\tall\tqa-gate-and-merge\tpane\t-\t-> 2026-01-11_fleet-rule.md: the old wording.",
    "2026-01-17_other-seat-only.md\tlive\ttuesday\tlearning-loop\tpane\t-\tWhen on the other seat: xcanary17rule do it.",
    "2026-01-19_two-rules.md\tlive\ttuesday\tlearning-loop\tpane\t-\tWhen on the other seat: xneighbour19rulea do it.",
    "2026-01-19_two-rules.md#2\tlive\twednesday,friday\tlearning-loop\tdrive\t-\tWhen syncing: xneighbour19ruleb count both sides.",
    "2026-01-21_zebraword-zebraword.md\tlive\tall\tlearning-loop\tdrive\t-\tWhen testing: xneighbour21zrule say zebraword.",
    "2026-01-99_missing-lesson.md\tlive\tall\tlearning-loop\tpane\t-\tWhen nothing: xcanary53rule a row whose lesson file does not exist.",
]
w(L + "_rules_index.tsv", "\n".join(rows) + "\n")


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

w("0_Brain/skills/ritual.md", "# A ritual\n\nThe word is xneighbour40.\n")
w("0_Brain/skills/ritual.md.pre-1", "# A ritual\n\nThe word is xcanary41.\n")
w("0_Brain/skills/tuesday-ritual.md", "# Another seat's ritual\n\nThe word is xneighbour42.\n")
w("0_Brain/identity/persona.md", "# Persona\n\nThe word is xneighbour43.\n")
w("0_Brain/people/kam.md", "# Kam\n\nThe word is xneighbour44.\n")
w("1_Project_Definition/Architecture/2026-01-01_design.md", "# A design\n\n## Part one\n\nThe word is xneighbour45.\n")
w("1_Project_Definition/Architecture/2026-01-02_tuesday-vs-wednesday.md", "# Two seats\n\nThe word is xneighbour46.\n")
w("0_Brain/dashboard/data/chat_wednesday.json", '[{"text": "xcanary47"}]\n')
w("0_Brain/dashboard/notes.md", "# dash\n\nxcanary48\n")
w("0_Brain/reference/2026-01-01_x/notes.md", "# ref\n\nxcanary49\n")
w("3_Access_Keys/key.md", "# key\n\nxcanary50\n")
w("0_Brain/tasks/NEXT.md", "# next\n\nxcanary51\n")

# ======================================================================================================
# ROUND 3 (ANSWER-3): every case of the checker's attack tree (qa-braindb/scripts/atk_build.py), lifted
# here as a planted file with a neighbour, under file names and tokens of their own (the checker's script
# runs THIS file first and then adds its own files, so nothing here may share a name with it).
# The expectation tables are written beside the tree, in <tree>/../expect-<tree name>/, and tests/run.sh
# reads them: absent.txt and present.txt hold "token|what it proves"; paths.txt is the exact set of
# paths the WEDNESDAY seat must index.
# ======================================================================================================
ABSENT, PRESENT = [], []


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


def les3(name, front, tok, what, want, body=""):
    raw(L + name, front + "# Lesson %s\n\nThe word is %s here.\n%s" % (tok, tok, body))
    (ABSENT if want == "absent" else PRESENT).append((tok, what))


DS = "P-Datasec/NexusAI"
# --- F1 (i): the frontmatter is read in a way that cannot be fooled into "untagged". No rules-index row.
for name, front, tok, what in [
    ("2026-06-01_fm-capital-key.md",   "---\nTier: %s\n---\n" % DS, "xcanary601", "tier key spelled 'Tier:'"),
    ("2026-06-02_fm-bom.md",           "﻿---\ntier: %s\n---\n" % DS, "xcanary602", "a UTF-8 BOM before the frontmatter"),
    ("2026-06-03_fm-leading-blank.md", "\n---\ntier: %s\n---\n" % DS, "xcanary603", "a blank line before the frontmatter"),
    ("2026-06-04_fm-unclosed.md",      "---\ntier: %s\n" % DS, "xcanary604", "frontmatter never closed"),
    ("2026-06-05_fm-dup-ds-w.md",      "---\ntier: %s\ntier: W\n---\n" % DS, "xcanary605", "tier given twice, other client first, W last"),
    ("2026-06-06_fm-dup-w-ds.md",      "---\ntier: W\ntier: %s\n---\n" % DS, "xcanary606", "tier given twice, W first, other client last"),
    ("2026-06-07_fm-two-blocks.md",    "---\ntier: W\n---\n---\ntier: %s\n---\n" % DS, "xcanary607", "two frontmatter blocks, W then the other client"),
    ("2026-06-08_fm-folded.md",        "---\ntier:\n  %s\n---\n" % DS, "xcanary608", "tier value folded onto the next line"),
    ("2026-06-09_fm-quoted-key.md",    "---\n\"tier\": P-Datasec/OXPd\n---\n", "xcanary609", "tier key in quotes"),
    ("2026-06-10_fm-general.md",       "---\ntier: P-HPSM/General-ledger-import\n---\n", "xcanary610", "another client's project whose NAME contains the own-client word 'general'"),
    ("2026-06-11_fm-upper.md",         "---\nTIER: P-DATASEC/OXPD\n---\n", "xcanary611", "tier key and value in capitals"),
    ("2026-06-12_fm-abbrev.md",        "---\ntier: P-DS/NexusAI\n---\n", "xcanary612", "client abbreviated (P-DS)"),
    ("2026-06-13_fm-endash.md",        "---\ntier: P–Datasec/OXPd\n---\n", "xcanary613", "en dash instead of the hyphen"),
    ("2026-06-14_fm-comment.md",       "---\ntier: W # really P-Datasec\n---\n", "xcanary614", "W with a trailing comment naming the other client"),
    ("2026-06-15_fm-list.md",          "---\ntier: [P-Datasec/OXPd]\n---\n", "xcanary615", "tier as a YAML list"),
    ("2026-06-16_fm-crlf.md",          "---\r\ntier: P-Datasec/OXPd\r\n---\r\n", "xcanary616", "CRLF line endings"),
    ("2026-06-17_fm-tab-indent.md",    "---\n\ttier:\tP-Datasec/OXPd\n---\n", "xcanary617", "tab-indented tier key"),
    ("2026-06-18_fm-dashes4.md",       "----\ntier: P-Datasec/OXPd\n----\n", "xcanary618", "four dashes as the fence"),
    ("2026-06-19_fm-nbsp.md",          "---\ntier: P-Datasec/OXPd\n---\n", "xcanary619", "a no-break space after the colon"),
    ("2026-06-20_fm-spaced.md",        "---\ntier: P-D a t a s e c\n---\n", "xcanary620", "client written with spaced letters"),
    ("2026-06-21_fm-cyrillic.md",      "---\ntier: P-Dаtasec/OXPd\n---\n", "xcanary621", "a Cyrillic look-alike letter in the client"),
    ("2026-06-22_fm-wed-substring.md", "---\ntier: P-Swedbank/Wed-portal\n---\n", "xcanary622", "a client and project that CONTAIN the own-client word 'wed'"),
    ("2026-06-23_fm-stray-line.md",    "tier: %s\n\n" % DS, "xcanary623", "no frontmatter at all, a tier line above the first heading"),
]:
    les3(name, front, tok, "F1(i/ii) lesson, " + what, "absent")
for name, front, tok, what, body in [
    ("2026-07-01_ok-capital-key.md",   "---\nTier: W\n---\n", "xneighbour830", "key spelled 'Tier:' with value W", ""),
    ("2026-07-02_ok-bom.md",           "﻿---\ntier: W\n---\n", "xneighbour831", "a BOM, then tier W", ""),
    ("2026-07-03_ok-leading-blank.md", "\n---\ntier: W\n---\n", "xneighbour832", "a blank line, then tier W", ""),
    ("2026-07-04_ok-quoted.md",        "---\n\"tier\": \"M\"\n---\n", "xneighbour833", "quoted key and value, tier M", ""),
    ("2026-07-05_ok-general.md",       "---\ntier: P-General/Claude to Claude\n---\n", "xneighbour834", "project tier whose CLIENT is the own client 'general'", ""),
    ("2026-07-06_ok-bracket.md",       "---\ntier: P (Secuura/Blockchain)\n---\n", "xneighbour835", "own client in the bracket spelling", ""),
    ("2026-07-07_ok-tier-in-body.md",  "---\ntier: W\n---\n", "xneighbour836", "the words 'tier: something' in the body, after the first heading", "\ntier: this line is prose under a heading, not frontmatter\n"),
    ("2026-07-08_ok-crlf.md",          "---\r\ntier: W\r\n---\r\n", "xneighbour837", "CRLF line endings, tier W", ""),
    ("2026-07-09_ok-rule-in-body.md",  "---\ntier: W\n---\n", "xneighbour838", "a horizontal rule (---) further down the body", "\n## Part two\n\n---\n\nAfter the rule.\n"),
]:
    les3(name, front, tok, "F1 neighbour, " + what, "present", body)

# --- F1 (iv): section markers of the other client inside an indexed MIXED lesson
mk = ("\n<!-- tier: P-Datasec/NexusAI -->\n\n## blank line between marker and heading\n\nxcanary640\n"
      "\n<!-- tier: P (Datasec/OXPd) -->\n## marker in the bracket spelling\n\nxcanary641\n"
      "\n<!--tier:P-Datasec/NexusAI-->\n## marker with no spaces\n\nxcanary642\n"
      "\n  <!-- tier: P-Datasec/NexusAI -->\n## indented marker\n\nxcanary643\n"
      "\n<!-- tier: P-Datasec/NexusAI -->\n## marked section with a sub-heading\n\nxcanary644top\n\n### its sub-section\n\nxcanary644sub\n"
      "\n<!-- tier: p-datasec/nexusai -->\n## lower-case marker\n\nxcanary645\n"
      "\n<!-- Tier: P-Datasec/NexusAI -->\n## capital T marker\n\nxcanary646\n"
      "\n<!-- tier: P-Datasec/NexusAI --> \n## marker with trailing space\n\nxcanary647\n"
      "\n<!-- tier: P-Datasec/NexusAI -->\nSetext heading for the other client\n-----\n\nxcanary648\n"
      "\n## clean section after them\n\nxneighbour849\n"
      "\n<!-- tier: P-Secuura/Blockchain -->\n## this client's marked section\n\nxneighbour850top\n\n### its sub-section\n\nxneighbour850sub\n")
les3("2026-07-10_markers.md", "---\ntier: MIXED\n---\n", "xneighbour840", "F1(iv) neighbour: the MIXED lesson's own text", "present", mk)
for tok, what in (("xcanary640", "a blank line between the marker and its heading"), ("xcanary641", "marker in the bracket spelling P (Datasec/OXPd)"),
                  ("xcanary642", "marker with no spaces"), ("xcanary643", "indented marker"), ("xcanary644top", "a marked section's own text"),
                  ("xcanary644sub", "the SUB-SECTION under a marked section"), ("xcanary645", "lower-case marker"),
                  ("xcanary646", "marker with a capital 'Tier'"), ("xcanary647", "marker with a trailing space"),
                  ("xcanary648", "marker above a setext heading (no heading directly under it)")):
    ABSENT.append((tok, "F1(iv) section, " + what))
PRESENT += [("xneighbour849", "F1(iv) neighbour: the section after the dropped ones"),
            ("xneighbour850top", "F1(iv) neighbour: a section marked for THIS seat's client"),
            ("xneighbour850sub", "F1(iv) neighbour: its sub-section")]
raw(L + "2026-07-11_markers-crlf.md", "---\r\ntier: MIXED\r\n---\r\n# L\r\n\r\nxneighbour852\r\n\r\n<!-- tier: P-Datasec/NexusAI -->\r\n## other client\r\n\r\nxcanary651\r\n\r\n## tail\r\n\r\nxneighbour853\r\n")
ABSENT.append(("xcanary651", "F1(iv) section marked for the other client in a CRLF file"))
PRESENT += [("xneighbour852", "F1(iv) neighbour in the CRLF file"), ("xneighbour853", "F1(iv) neighbour: its tail section")]

# --- F1 (iii): lessons that belong to ANOTHER seat only, whose rules-index row is damaged or oddly keyed
R3 = [
    ("2026-07-12_r-tab-in-rule.md", "xcanary660", "2026-07-12_r-tab-in-rule.md\tlive\ttuesday\tlearning-loop\tdrive\t-\tWhen on the other seat: xcanary660rule do\tit.", "a TAB inside the rule field (8 fields)", "absent"),
    ("2026-07-13_r-newline.md", "xcanary661", "2026-07-13_r-newline.md\tlive\ttuesday\tlearning-loop\tdrive\t-\tWhen on the other seat: xcanary661rule\ndo it.", "a NEWLINE inside the rule field", "absent"),
    ("2026-07-14_r-key-space.md", "xcanary662", "2026-07-14_r-key-space.md \tlive\ttuesday\tlearning-loop\tdrive\t-\tWhen: xcanary662rule.", "a key with a trailing space", "absent"),
    ("2026-07-15_r-hash1.md", "xcanary663", "2026-07-15_r-hash1.md#1\tlive\ttuesday\tlearning-loop\tdrive\t-\tWhen: xcanary663rule.", "a key written file.md#1", "absent"),
    ("2026-07-16_r-keycase.md", "xcanary664", "2026-07-16_R-KeyCase.md\tlive\ttuesday\tlearning-loop\tdrive\t-\tWhen: xcanary664rule.", "a key that differs in case", "absent"),
    ("2026-07-17_r-seat-caps.md", "xcanary665", "2026-07-17_r-seat-caps.md\tlive\tTuesday\tlearning-loop\tdrive\t-\tWhen: xcanary665rule.", "seats column 'Tuesday' (capital)", "absent"),
    ("2026-07-18_r-seat-semicolon.md", "xcanary666", "2026-07-18_r-seat-semicolon.md\tlive\ttuesday;friday\tlearning-loop\tdrive\t-\tWhen: xcanary666rule.", "seats column 'tuesday;friday'", "absent"),
    ("2026-07-19_r-seat-empty.md", "xcanary667", "2026-07-19_r-seat-empty.md\tlive\t\tlearning-loop\tdrive\t-\tWhen: xcanary667rule.", "an empty seats column", "absent"),
    ("2026-07-20_r-six-fields.md", "xcanary668", "2026-07-20_r-six-fields.md\tlive\ttuesday\tlearning-loop\tdrive\tWhen: xcanary668rule.", "a row with 6 fields", "absent"),
    ("2026-07-21_r-crlf.md", "xcanary669", "2026-07-21_r-crlf.md\tlive\ttuesday\tlearning-loop\tdrive\t-\tWhen: xcanary669rule.\r", "a row with a CRLF ending", "absent"),
    ("2026-07-22_r-path-key.md", "xcanary670", "0_Brain/learnings/2026-07-22_r-path-key.md\tlive\ttuesday\tlearning-loop\tdrive\t-\tWhen: xcanary670rule.", "a key written as a path", "absent"),
    ("2026-07-23_r-not-wednesday.md", "xcanary671", "2026-07-23_r-not-wednesday.md\tlive\tnot-wednesday\tlearning-loop\tdrive\t-\tWhen: xcanary671rule.", "seats column 'not-wednesday'", "absent"),
    ("2026-07-24_r-inject.md", "xneighbour872", "2026-07-24_r-inject.md\tlive\tall\tfam'; drop schema brain cascade; --\tdrive,$(touch PWNED_trig),`touch PWNED_bt`,\\! touch PWNED_meta\t-\tWhen: xneighbour872rule \\. \\copy brain.files to program 'touch PWNED_copy' ; '); DROP SCHEMA brain CASCADE; --", "a well-formed row scoped all, carrying injection strings", "present"),
    ("2026-07-25_r-keyspace-all.md", "xneighbour874", "2026-07-25_r-keyspace-all.md \tlive\tall\tlearning-loop\tdrive\t-\tWhen: xneighbour874rule.", "a key with a trailing space whose row is scoped all", "present"),
    ("2026-07-26_r-good-and-damaged.md", "xcanary675", "2026-07-26_r-good-and-damaged.md\tlive\tall\tlearning-loop\tdrive\t-\tWhen: xcanary675rule.\n2026-07-26_r-good-and-damaged.md#x\tlive\ttuesday\tlearning-loop\tdrive\t-\tWhen: xcanary675ruleb.", "a good row scoped all AND a damaged row for the same lesson", "absent"),
]
idx = open(os.path.join(root, L + "_rules_index.tsv"), encoding="utf-8").read()
for name, tok, row, what, want in R3:
    les3(name, "---\ntier: W\n---\n", tok, "F1(iii) " + ("other seat's lesson, " if want == "absent" else "neighbour, ") + what, want)
    idx += row + "\n"
with open(os.path.join(root, L + "_rules_index.tsv"), "w", encoding="utf-8", newline="") as f:
    f.write(idx)

# --- F3: a hard link to a credentials file; and an ABSOLUTE symlink to a keys file
raw("4_Credentials/secret2.md", "---\ntier: W\n---\n# s\n\nxcanary680\n")
os.link(os.path.join(root, "4_Credentials/secret2.md"), os.path.join(root, L + "2026-07-27_hardlink.md"))
ABSENT.append(("xcanary680", "F3 a 4_Credentials file HARD-LINKED into learnings/"))
raw("3_Access_Keys/key2.md", "xcanary681\n")
os.symlink(os.path.join(root, "3_Access_Keys/key2.md"), os.path.join(root, "0_Brain/skills/abs-link.md"))
ABSENT.append(("xcanary681", "an absolute symlinked FILE in skills/ pointing into 3_Access_Keys"))

# --- daily notes whose NAME is not a plain date (a seat word in capitals, look-alike letters, a hyphen)
def daily3(name, tok, what):
    raw("0_Brain/daily/" + name, "# d\n\n## Sessions\n- 06:19 the word is %s here.\n" % tok)
    ABSENT.append((tok, "daily note named " + what))
daily3("2026-06-01-TUESDAY-handover.md", "xcanary690", "...TUESDAY... in capitals")
daily3("2026-06-02_tuеsday.md", "xcanary691", "with a Cyrillic look-alike of 'tuesday'")
daily3("2026-06-03_fri-day.md", "xcanary692", "'fri-day'")
daily3("2026-06-04_ｆｒｉｄａｙ.md", "xcanary693", "in full-width letters")

# --- F11: other seats' pickup and week files, reachable only if a scope allows 0_Brain/tasks/ (run.sh does)
raw("0_Brain/tasks/NEXT-PICKUP-TUESDAY.md", "# p\n\nxcanary700\n")
raw("0_Brain/tasks/WEEK-friday.md", "# p\n\nxcanary701\n")
raw("0_Brain/tasks/NEXT-PICKUP.md", "# p\n\nxtasksown202\n")          # this seat's own; enters only under a widened scope
ABSENT += [("xcanary700", "F11 another seat's pickup file (0_Brain/tasks is not on the allow-list)"),
           ("xcanary701", "F11 another seat's week file")]

# --- F8 and crash probes: legitimate W lessons with hostile content
raw(L + "2026-07-28_separator-bytes.md", "---\ntier: W\n---\n# separators\n\nbefore \x1f unit xneighbour910 \x1e record after\n")
PRESENT.append(("xneighbour910", "F8 a row holding the two separator bytes 0x1F and 0x1E"))
raw(L + "2026-07-29_invalid-utf8.md", b"---\ntier: W\n---\n# bad bytes\n\nxneighbour911 \xff\xfe\xc3\x28 \x00\x00 after-nul xneighbour911b\n")
PRESENT.append(("xneighbour911b", "invalid UTF-8 and NUL bytes"))
raw(L + "2026-07-30_bad-date.md", "---\ntier: W\ndate: 2026-13-45\n---\n# bad date\n\nxneighbour912\n")
PRESENT.append(("xneighbour912", "an impossible frontmatter date"))
raw(L + "2026-07-31_empty.md", "")
raw(L + "2026-08-01_only-fence.md", "---")
os.mkdir(os.path.join(root, L + "2026-08-02_a-directory.md"))
os.mkfifo(os.path.join(root, L + "2026-08-03_a-fifo.md"))
raw(L + "2026-08-04_fences.md", "---\ntier: W\n---\n# fences\n\n```\n# not a heading xneighbour913\n```\n\n## real heading\n\n~~~\nunclosed fence xneighbour913b\n## never a heading\n")
PRESENT.append(("xneighbour913b", "code fences, one unclosed"))
INJ = ["2026-08-05_$(touch PWNED_name1).md", "2026-08-06_`touch PWNED_name2`.md", "2026-08-07_'; drop schema brain cascade; --.md"]
for i, n in enumerate(INJ, 1):
    tok = "xneighbour92%d" % i
    les3(n, "---\ntier: W\n---\n", tok, "a lesson whose NAME and body carry injection strings, indexed as plain text", "present",
         "\n## \\! touch PWNED_head%d\n\n\\.\n\\! touch PWNED_body%d\n\\copy brain.files to program 'touch PWNED_copy%d'\n'); DROP SCHEMA brain CASCADE; --\n$(touch PWNED_sub%d) `touch PWNED_bt%d`\n\\N\n" % (i, i, i, i, i))

# --- the exact set of paths the WEDNESDAY seat must index from this tree
WED_PATHS = [
    "0_Brain/CLAUDE.md", "0_Brain/daily/2026-01-20.md", "0_Brain/identity/persona.md", "0_Brain/people/kam.md",
    "0_Brain/skills/ritual.md", "0_Brain/skills/tuesday-ritual.md",
    "1_Project_Definition/Architecture/2026-01-01_design.md", "1_Project_Definition/Architecture/2026-01-02_tuesday-vs-wednesday.md",
    "CLAUDE.md", L + "_ledger.md", L + "_ledger_archive.md", L + "_rules_index.tsv",
] + [L + n for n in (
    "2026-01-01_alpha-keeps-panes-open.md", "2026-01-02_tuesday-sweeps.md", "2026-01-04_laptop_datasec-habit.md",
    "2026-01-10_project-case-three.md", "2026-01-11_fleet-rule.md", "2026-01-12_untagged.md", "2026-01-14_mixed.md",
    "2026-01-16_old-rule.md", "2026-01-19_two-rules.md", "2026-01-21_zebraword-zebraword.md",
    "2026-07-01_ok-capital-key.md", "2026-07-02_ok-bom.md", "2026-07-03_ok-leading-blank.md", "2026-07-04_ok-quoted.md",
    "2026-07-05_ok-general.md", "2026-07-06_ok-bracket.md", "2026-07-07_ok-tier-in-body.md", "2026-07-08_ok-crlf.md",
    "2026-07-09_ok-rule-in-body.md", "2026-07-10_markers.md", "2026-07-11_markers-crlf.md", "2026-07-24_r-inject.md",
    "2026-07-25_r-keyspace-all.md", "2026-07-28_separator-bytes.md", "2026-07-29_invalid-utf8.md", "2026-07-30_bad-date.md",
    "2026-07-31_empty.md", "2026-08-04_fences.md") + tuple(INJ)]
exp = os.path.join(os.path.dirname(os.path.abspath(root)), "expect-" + os.path.basename(os.path.abspath(root)))
os.makedirs(exp, exist_ok=True)
for fname, rows in (("absent.txt", ABSENT), ("present.txt", PRESENT)):
    with open(os.path.join(exp, fname), "w", encoding="utf-8") as f:
        for tok, what in rows:
            f.write("%s|%s\n" % (tok, what))
with open(os.path.join(exp, "paths.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(WED_PATHS)) + "\n")
print("fixtures written under " + root)
