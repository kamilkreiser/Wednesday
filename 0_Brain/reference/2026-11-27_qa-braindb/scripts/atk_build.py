import os, sys, subprocess
root = sys.argv[1]
subprocess.check_call([sys.executable, "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/brain-db/tests/make_fixtures.py", root])
L = os.path.join(root, "0_Brain/learnings")
def w(rel, data, mode="w"):
    p = os.path.join(root, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    if isinstance(data, bytes):
        open(p, "wb").write(data)
    else:
        open(p, "w", encoding="utf-8", newline="").write(data)
    return p
def les(name, front, tok, body=""):
    return w("0_Brain/learnings/" + name, front + "# Lesson %s\n\nThe word is %s here.\n%s" % (tok, tok, body))
exp = []   # (token, expectation, what)
def E(tok, want, what): exp.append((tok, want, what))

# --- A1 symlinked FILE to a credentials file; A2 hard link to a credentials file
w("4_Credentials/atk_secret.md", "---\ntier: W\n---\n# s\n\nzatk01 zatk02\n")
os.symlink("../../4_Credentials/atk_secret.md", os.path.join(L, "2026-02-01_symfile.md")); E("zatk01", "absent", "A1 symlinked FILE -> 4_Credentials (also reached by A2's hard link, see zatk02)")
w("4_Credentials/atk_secret2.md", "---\ntier: W\n---\n# s\n\nzatk02hard\n")
os.link(os.path.join(root, "4_Credentials/atk_secret2.md"), os.path.join(L, "2026-02-02_hardlink.md")); E("zatk02hard", "absent", "A2 HARD LINK in learnings/ to a 4_Credentials file")
w("3_Access_Keys/atk_key.md", "zatk03key\n")
os.symlink(os.path.join(root, "3_Access_Keys/atk_key.md"), os.path.join(root, "0_Brain/skills/abs-symlink.md")); E("zatk03key", "absent", "A1b absolute symlinked FILE in skills/ -> 3_Access_Keys")
os.symlink("CLAUDE.md", os.path.join(root, "0_Brain/identity/chain-a.md"))  # symlink to a legit file elsewhere
# --- A5 tier spellings (no rules-index row: decided by tier alone). All are another client's project lessons.
T = [
 ("2026-02-10_t-capital-key.md",   "---\nTier: P-Datasec/NexusAI\n---\n", "zatk10", "key spelled 'Tier:'"),
 ("2026-02-11_t-bom.md",           "﻿---\ntier: P-Datasec/NexusAI\n---\n", "zatk11", "UTF-8 BOM before the frontmatter"),
 ("2026-02-12_t-leading-blank.md", "\n---\ntier: P-Datasec/NexusAI\n---\n", "zatk12", "blank line before the frontmatter"),
 ("2026-02-13_t-unclosed.md",      "---\ntier: P-Datasec/NexusAI\n", "zatk13", "frontmatter never closed"),
 ("2026-02-14_t-dup-ds-then-w.md", "---\ntier: P-Datasec/NexusAI\ntier: W\n---\n", "zatk14", "duplicated tier key, other client first, W last"),
 ("2026-02-15_t-dup-w-then-ds.md", "---\ntier: W\ntier: P-Datasec/NexusAI\n---\n", "zatk15", "duplicated tier key, W first, other client last"),
 ("2026-02-16_t-two-blocks.md",    "---\ntier: W\n---\n---\ntier: P-Datasec/NexusAI\n---\n", "zatk16", "two frontmatter blocks, W then other client"),
 ("2026-02-17_t-folded.md",        "---\ntier:\n  P-Datasec/NexusAI\n---\n", "zatk17", "YAML folded value on the next line"),
 ("2026-02-18_t-abbrev.md",        "---\ntier: P-DS/NexusAI\n---\n", "zatk18", "tier P-DS/NexusAI (client abbreviated)"),
 ("2026-02-19_t-powered.md",       "---\ntier: P-NexusAI/Powered-search\n---\n", "zatk19", "other client's project tier that happens to contain 'wed' (Po-wed... 'Powered')"),
 ("2026-02-20_t-spaced.md",        "---\ntier: P-D a t a s e c\n---\n", "zatk20", "tier with spaced letters"),
 ("2026-02-21_t-endash.md",        "---\ntier: P–Datasec/OXPd\n---\n", "zatk21", "en dash instead of hyphen"),
 ("2026-02-22_t-cyrillic.md",      "---\ntier: P-Dаtasec/OXPd\n---\n", "zatk22", "Cyrillic look-alike letter in the client name"),
 ("2026-02-23_t-comment.md",       "---\ntier: W # really P-Datasec\n---\n", "zatk23", "W with a trailing comment naming the client"),
 ("2026-02-24_t-list.md",          "---\ntier: [P-Datasec/OXPd]\n---\n", "zatk24", "YAML list value"),
 ("2026-02-25_t-crlf.md",          "---\r\ntier: P-Datasec/OXPd\r\n---\r\n", "zatk25", "CRLF line endings"),
 ("2026-02-26_t-tab-indent.md",    "---\n\ttier:\tP-Datasec/OXPd\n---\n", "zatk26", "tab-indented key"),
 ("2026-02-27_t-quoted-key.md",    "---\n\"tier\": P-Datasec/OXPd\n---\n", "zatk27", "quoted key"),
 ("2026-02-28_t-general.md",       "---\ntier: P-HPSM/General-ledger-import\n---\n", "zatk28", "other client's project whose name contains 'general'"),
 ("2026-03-01_t-dashes4.md",       "----\ntier: P-Datasec/OXPd\n----\n", "zatk29", "four dashes as the fence"),
 ("2026-03-02_t-nbsp.md",          "---\ntier: P-Datasec/OXPd\n---\n", "zatk30", "no-break space after the colon"),
 ("2026-03-03_t-upper.md",         "---\nTIER: P-DATASEC/OXPD\n---\n", "zatk31", "key in capitals"),
]
for name, fm, tok, what in T:
    les(name, fm, tok); E(tok, "absent", "A5 " + what)
# --- A5b section markers inside a MIXED lesson
body = ("\n<!-- tier: P-Datasec/NexusAI -->\n\n## blank line between marker and heading\n\nzatk40\n"
        "\n<!-- tier: P (Datasec/OXPd) -->\n## marker in the bracket spelling\n\nzatk41\n"
        "\n<!--tier:P-Datasec/NexusAI-->\n## marker with no spaces\n\nzatk42\n"
        "\n  <!-- tier: P-Datasec/NexusAI -->\n## indented marker\n\nzatk43\n"
        "\n<!-- tier: P-Datasec/NexusAI -->\n## marked section with a sub-heading\n\nzatk44top\n\n### its sub-section\n\nzatk44sub\n"
        "\n<!-- tier: p-datasec/nexusai -->\n## lower-case marker\n\nzatk45\n"
        "\n<!-- Tier: P-Datasec/NexusAI -->\n## capital T marker\n\nzatk46\n"
        "\n<!-- tier: P-Datasec/NexusAI --> \n## marker with trailing space\n\nzatk47\n"
        "\n<!-- tier: P-Datasec/NexusAI -->\nSetext heading for the other client\n-----\n\nzatk48\n"
        "\n## clean tail\n\nzatkneigh49\n")
les("2026-03-05_mixed-markers.md", "---\ntier: MIXED\n---\n", "zatkneigh40", body)
for tok, what in (("zatk40","blank line between marker and heading"),("zatk41","marker spelled P (Datasec/OXPd)"),("zatk42","marker without spaces"),("zatk43","indented marker"),("zatk44top","marked section, own text"),("zatk44sub","sub-section under a marked section"),("zatk45","lower-case marker"),("zatk46","marker with capital 'Tier'"),("zatk47","marker with trailing space"),("zatk48","marker above a setext heading")):
    E(tok, "absent", "A5b " + what)
E("zatkneigh40", "present", "A5b neighbour: the MIXED lesson's own text"); E("zatkneigh49", "present", "A5b neighbour: clean tail section")
crlf = "---\r\ntier: MIXED\r\n---\r\n# L\r\n\r\nzatkneigh50\r\n\r\n<!-- tier: P-Datasec/NexusAI -->\r\n## other client\r\n\r\nzatk50\r\n\r\n## tail\r\n\r\nzatkneigh51\r\n"
w("0_Brain/learnings/2026-03-06_mixed-crlf.md", crlf); E("zatk50", "absent", "A5b marked section in a CRLF file"); E("zatkneigh50", "present", "neighbour"); E("zatkneigh51", "present", "neighbour")
# --- A6 rules-index attacks: lessons that belong to ANOTHER seat only, whose row is damaged
R = [
 ("2026-03-10_r-tab-in-rule.md", "zatk60", "2026-03-10_r-tab-in-rule.md\tlive\ttuesday\tlearning-loop\tpane\t-\tWhen on the other seat: zatk60rule do\tit.", "row with a TAB inside the rule field (8 fields)"),
 ("2026-03-11_r-newline.md", "zatk61", "2026-03-11_r-newline.md\tlive\ttuesday\tlearning-loop\tpane\t-\tWhen on the other seat: zatk61rule\ndo it.", "row with a NEWLINE inside the rule field"),
 ("2026-03-12_r-key-space.md", "zatk62", "2026-03-12_r-key-space.md \tlive\ttuesday\tlearning-loop\tpane\t-\tWhen: zatk62rule.", "row whose key has a trailing space"),
 ("2026-03-13_r-hash1.md", "zatk63", "2026-03-13_r-hash1.md#1\tlive\ttuesday\tlearning-loop\tpane\t-\tWhen: zatk63rule.", "row keyed file.md#1"),
 ("2026-03-14_r-keycase.md", "zatk64", "2026-03-14_R-KeyCase.md\tlive\ttuesday\tlearning-loop\tpane\t-\tWhen: zatk64rule.", "row whose key differs in case"),
 ("2026-03-15_r-seat-caps.md", "zatk65", "2026-03-15_r-seat-caps.md\tlive\tTuesday\tlearning-loop\tpane\t-\tWhen: zatk65rule.", "seats column 'Tuesday' (capital)"),
 ("2026-03-16_r-seat-semicolon.md", "zatk66", "2026-03-16_r-seat-semicolon.md\tlive\ttuesday;friday\tlearning-loop\tpane\t-\tWhen: zatk66rule.", "seats column 'tuesday;friday'"),
 ("2026-03-17_r-seat-empty.md", "zatk67", "2026-03-17_r-seat-empty.md\tlive\t\tlearning-loop\tpane\t-\tWhen: zatk67rule.", "seats column empty"),
 ("2026-03-18_r-six-fields.md", "zatk68", "2026-03-18_r-six-fields.md\tlive\ttuesday\tlearning-loop\tpane\tWhen: zatk68rule.", "row with 6 fields"),
 ("2026-03-19_r-crlf.md", "zatk69", "2026-03-19_r-crlf.md\tlive\ttuesday\tlearning-loop\tpane\t-\tWhen: zatk69rule.\r", "row with CRLF ending"),
 ("2026-03-20_r-path-key.md", "zatk70", "0_Brain/learnings/2026-03-20_r-path-key.md\tlive\ttuesday\tlearning-loop\tpane\t-\tWhen: zatk70rule.", "row keyed by path, not file name"),
 ("2026-03-21_r-not-wednesday.md", "zatk71", "2026-03-21_r-not-wednesday.md\tlive\tnot-wednesday\tlearning-loop\tpane\t-\tWhen: zatk71rule.", "seats column 'not-wednesday'"),
 ("2026-03-22_r-inject.md", "zatkneigh72", "2026-03-22_r-inject.md\tlive\tall\tfam'; drop schema brain cascade; --\tpane,$(touch PWNED_trig),`touch PWNED_bt`,\\! touch PWNED_meta\t-\tWhen: zatkneigh72rule \\. \\copy brain.files to program 'touch PWNED_copy' ; '); DROP SCHEMA brain CASCADE; --", "injection strings in family, triggers and rule"),
]
rows = open(os.path.join(L, "_rules_index.tsv"), encoding="utf-8").read()
for name, tok, row, what in R:
    les(name, "---\ntier: W\n---\n", tok); rows += row + "\n"
    if tok.startswith("zatkneigh"): E(tok, "present", "A6 " + what)
    else: E(tok, "absent", "A6 other seat's lesson, " + what)
open(os.path.join(L, "_rules_index.tsv"), "w", encoding="utf-8", newline="").write(rows)
# --- A4 seat word in other spellings, in THIS seat's daily folder (record kind) and learnings
def daily(rel, tok): w(rel, "# d\n\n## Sessions\n- 06:19 the word is %s here.\n" % tok)
daily("0_Brain/daily/2026-02-01-TUESDAY-handover.md", "zatk80"); E("zatk80", "absent", "A4 daily note named ...TUESDAY... (capitals)")
daily("0_Brain/daily/2026-02-02_tuеsday.md", "zatk81"); E("zatk81", "absent", "A4 daily note named with a Cyrillic look-alike of 'tuesday'")
daily("0_Brain/daily/2026-02-03_fri-day.md", "zatk82"); E("zatk82", "absent", "A4 daily note named 'fri-day'")
daily("0_Brain/daily/2026-02-04_ｆｒｉｄａｙ.md", "zatk83"); E("zatk83", "absent", "A4 daily note named in full-width letters")
# --- A9 injection in file names, headings and bodies (all legitimate W lessons: they SHOULD be indexed, harmlessly)
inj_names = ["2026-04-01_$(touch PWNED_name1).md", "2026-04-02_`touch PWNED_name2`.md", "2026-04-03_'; drop schema brain cascade; --.md",
             "2026-04-04_\\! touch PWNED_name4.md", "2026-04-05_a\n\\.\n\\! touch PWNED_name5\n.md", "2026-04-06_tab\there \"dq\" 'sq' ;&|<>.md",
             "2026-04-07_\\copy brain.files to program 'touch PWNED_name7'.md", "2026-04-08_-rf --kind.md"]
pw = os.path.join(os.path.dirname(root), "cwd")
for i, n in enumerate(inj_names, 1):
    tok = "zatkneigh9%d" % i
    les(n, "---\ntier: W\ndate: 2026-04-0%d\n---\n" % i, tok,
        "\n## \\! touch %s/PWNED_head%d\n\n\\.\n\\! touch %s/PWNED_body%d\n\\copy brain.files to program 'touch %s/PWNED_copy%d'\n'); DROP SCHEMA brain CASCADE; --\n$(touch %s/PWNED_sub%d) `touch %s/PWNED_bt%d`\n\\N\n\\x1f \x1f unit \x1e record zatkctl%d\n" % (pw, i, pw, i, pw, i, pw, i, pw, i, i))
    E(tok, "present", "A9 injection-named lesson %d is indexed as plain text" % i)
# --- A8 crash probes (legit W lessons with hostile content)
w("0_Brain/learnings/2026-05-01_invalid-utf8.md", b"---\ntier: W\n---\n# bad bytes\n\nzatkneigh101 \xff\xfe\xc3\x28 \x00\x00 after-nul zatkneigh101b\n"); E("zatkneigh101", "present", "A8 invalid UTF-8 and NUL bytes")
w("0_Brain/learnings/2026-05-02_empty.md", ""); 
w("0_Brain/learnings/2026-05-03_only-fence.md", "---")
w("0_Brain/learnings/2026-05-04_bad-date.md", "---\ntier: W\ndate: 2026-13-45\n---\n# bad date\n\nzatkneigh104\n"); E("zatkneigh104", "present", "A8 impossible frontmatter date")
w("0_Brain/learnings/2026-05-05_long-line.md", "---\ntier: W\n---\n# long\n\nzatkneigh105 " + ("word " * 400000) + "\n"); E("zatkneigh105", "present", "A8 one 2 MB line of a repeated word")
os.mkdir(os.path.join(L, "2026-05-06_a-directory.md"))
os.mkfifo(os.path.join(L, "2026-05-07_a-fifo.md"))
w("0_Brain/learnings/2026-05-08_fences.md", "---\ntier: W\n---\n# fences\n\n```\n# not a heading zatkneigh108\n<!-- tier: P-Datasec/X -->\n## inside a fence\n```\n~~~\nunclosed fence zatkneigh108b\n## never a heading\n")
E("zatkneigh108", "present", "A8 code fences, one unclosed")
import json
json.dump(exp, open(os.path.join(os.path.dirname(root), "expect.json"), "w"))
print("attack tree built:", root, "expectations:", len(exp))
