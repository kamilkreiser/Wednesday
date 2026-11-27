# minors.py — the first verdict's m3, m4, m5 re-attacked on round 3.
# m4 needs a tree that is NOT under a temp directory: one is made inside my own output folder (nontemp_tree/WEDNESDAY), holding copies of the
# tools; only that tree could be written by these calls, and each call is expected to be REFUSED before it writes.
import os, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
import qlib
OUT = R + "/0_Brain/reference/2026-11-27_qa-wake-r3"
print("## m4. test seams on a tree that is not under a temp directory")
nt = os.path.join(OUT, "nontemp_tree", "WEDNESDAY")
for rel in ("tools/seat_note.sh", "fleet/cockpit/seat_resolve.sh"):
    d = os.path.join(nt, "2_Project_Files", rel); os.makedirs(os.path.dirname(d), exist_ok=True); shutil.copy(os.path.join(REAL, rel), d)
os.makedirs(os.path.join(nt, "2_Project_Files/wake"), exist_ok=True); os.makedirs(os.path.join(nt, "0_Brain/tasks"), exist_ok=True)
for f in ("handover.sh", "handover_core.py"): shutil.copy(os.path.join(LANE, f), os.path.join(nt, "2_Project_Files/wake", f))
sh = os.path.join(nt, "2_Project_Files/wake/handover.sh"); core = os.path.join(nt, "2_Project_Files/wake/handover_core.py")


def run(cmd, data=b"", env=None):
    p = subprocess.run(cmd, input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV(env)); return p.returncode, p.stdout.decode(), p.stderr.decode()


def ls(): return sorted(os.listdir(os.path.join(nt, "0_Brain/tasks")))


rc, o, e = run(["/bin/bash", sh, "--where"]); print("- control, no seam variable, --where on the non-temp tree: rc %d (seat line: %s)" % (rc, o.split("\n")[0]))
link = os.path.join(BASE, "link_to_nontemp");
if not os.path.islink(link): os.symlink(nt, link)
scr = mk("seamscratch", "minors")
for label, cmd, env, data in (
    ("HANDOVER_TEST_STAMP alone, write --stdin", ["/bin/bash", sh, "write", "--stdin"], {"HANDOVER_TEST_STAMP": "TYPED-CLOCK"}, blk("X")),
    ("HANDOVER_TEST_BREAK alone, write --stdin --dry", ["/bin/bash", sh, "write", "--stdin", "--dry"], {"HANDOVER_TEST_BREAK": "archive-truncate"}, blk("X")),
    ("HANDOVER_TREE naming the non-temp tree itself", ["/bin/bash", sh, "--where"], {"HANDOVER_TREE": nt}, b""),
    ("HANDOVER_TREE = a SYMLINK under the temp directory that points at the non-temp tree", ["/bin/bash", sh, "write", "--stdin"], {"HANDOVER_TREE": link}, blk("X")),
    ("the scratch (temp) copy of the tool pointed at the non-temp tree by HANDOVER_TREE", ["/bin/bash", os.path.join(scr, "2_Project_Files/wake/handover.sh"), "write", "--stdin"], {"HANDOVER_TREE": nt}, blk("X")),
    ("TMPDIR set to the non-temp tree's parent, HANDOVER_TEST_STAMP set", ["/bin/bash", sh, "write", "--stdin"], {"TMPDIR": os.path.dirname(nt), "HANDOVER_TEST_STAMP": "TYPED"}, blk("X")),
    ("the ENGINE called directly with HANDOVER_TEST_BREAK", [sys.executable, core, "write", "--seat", "wednesday", "--tasks-dir", os.path.join(nt, "0_Brain/tasks"), "--stamp", "X", "--dry"], {"HANDOVER_TEST_BREAK": "archive-truncate"}, blk("X")),
    ("the ENGINE called directly with --seat tuesday for this tree", [sys.executable, core, "write", "--seat", "tuesday", "--tasks-dir", os.path.join(nt, "0_Brain/tasks"), "--stamp", "X"], None, blk("X")),
    ("the ENGINE called directly with a TYPED --stamp (no seam variable; the engine cannot know)", [sys.executable, core, "write", "--seat", "wednesday", "--tasks-dir", os.path.join(nt, "0_Brain/tasks"), "--stamp", "TYPED-11:4x", "--dry"], None, blk("X")),
):
    rc, o, e = run(cmd, data, env)
    print("- %-88s rc %d; tasks dir now %s | %s" % (label, rc, ls(), (e.strip().split("\n")[0] if e.strip() else o.strip().split("\n")[-1])[:120]))
rc, o, e = run(["/bin/bash", os.path.join(scr, "2_Project_Files/wake/handover.sh"), "write", "--stdin"], blk("OK"), {"HANDOVER_TEST_STAMP": "SEAM-OK"})
print("- must-succeed beside them: HANDOVER_TEST_STAMP on a tree under the temp directory: rc %d; stamp honoured: %s" % (rc, b"written: SEAM-OK" in (rd(st(scr)) or b"")))

print("## m5. headings inside a block (--dry, a scratch tree). REFUSED is what m5 asks for; ACCEPTED is listed for judgement")
r = mk("headings", "minors")
B = "## FLOOR\nf\n## FIRST WORK\nw\n## OWED\no\n## OPEN CARDS\nc\n## GRANTS IN PLAY\ng\n"
cases = [("control: the five parts", B, False), ("'### sub'", B + "### sub\nx\n", True), ("'# top'", B + "# CHECKPOINT 2\nx\n", True), ("indented '  ## x'", B + "  ## SECOND\nx\n", True),
         ("tab-indented '\\t## x'", B + "\t## SECOND\nx\n", True), ("zero-width space before ##", B + "​## HIDDEN\nx\n", True), ("'## FLOOR (4 seats)'", B.replace("## FLOOR\n", "## FLOOR (4 seats)\n"), True),
         ("'## floor' lower case", B.replace("## FLOOR\n", "## floor\n"), True), ("'##  FLOOR' two spaces", B.replace("## FLOOR\n", "##  FLOOR\n"), True),
         ("'## FLOOR ##' closing hashes", B.replace("## FLOOR\n", "## FLOOR ##\n"), True), ("non-breaking space after ##", B + "## SECOND\nx\n", True),
         ("SETEXT heading (a line underlined with ---: Markdown reads an h2)", B + "\nCHECKPOINT 70% 14:00 a second dated block\n---\n- FLOOR: stacked\n- OWED: stacked\n", True),
         ("SETEXT heading underlined with ===", B + "\nSECOND BLOCK\n===\nstacked\n", True),
         ("heading inside a blockquote '> ## x'", B + "> ## SECOND BLOCK\n> stacked\n", True), ("heading inside a list item '- ## x'", B + "- ## SECOND BLOCK\n  stacked\n", True),
         ("HTML heading <h2>", B + "<h2>SECOND BLOCK</h2>\nstacked\n", True), ("'##' inside a code fence", B + "```\n## not a heading\n```\n", True),
         ("a bold line as a sub-title (must be accepted)", B + "**sub-title**\n- x\n", False), ("'#123' and 'C# code' (must be accepted)", B + "#123 ticket; C# code; issue #4\n", False)]
acc = []
for label, data, want_refused in cases:
    rc, o, e = ho(r, "write", "--stdin", "--dry", data=data.encode("utf-8"))
    res = "REFUSED" if rc == 3 else ("ACCEPTED" if rc == 0 else "rc %d" % rc)
    flag = "ok" if (rc == 3) == want_refused else "<<< accepted although a Markdown reader sees a heading" if want_refused else "<<< refused although it must be accepted"
    if flag != "ok": acc.append(label)
    print("- %-66s %-8s %s" % (label, res, flag))
print("heading forms still accepted: %d %s" % (len(acc), acc))

print("## m3. unreadable files: a refusal naming the path, or a traceback?")
r = mk_real("unread", "minors"); ho(r, "write", "--stdin", data=blk("one")); ho(r, "write", "--stdin", data=blk("two"))
for label, path, verb in (("state file mode 000, write", st(r), ("write", "--stdin")), ("archive mode 000, write", ar(r), ("write", "--stdin")), ("state file mode 000, show", st(r), ("show",)),
                          ("state file mode 000, check", st(r), ("check",)), ("state file is a DIRECTORY, write", "DIR", ("write", "--stdin")), ("tasks dir read-only, write", "RO", ("write", "--stdin"))):
    if path == "DIR":
        r2 = mk("unread_dir", "minors"); os.mkdir(st(r2)); rc, o, e = ho(r2, *verb, data=blk("x"))
    elif path == "RO":
        os.chmod(T(r), 0o555); rc, o, e = ho(r, *verb, data=blk("three")); os.chmod(T(r), 0o755)
    else:
        os.chmod(path, 0); rc, o, e = ho(r, *verb, data=blk("three")); os.chmod(path, 0o644)
    print("- %-36s rc %d; traceback %s; names the path %s | %s" % (label, rc, "YES" if "Traceback" in e else "no", ("STATE-wednesday" in e) or ("tasks" in e), (e.strip().split("\n")[-1] if e.strip() else o.strip())[:150]))
print("  after all of it: state is still 'two' %s; lock directory left behind: %s; temp files: %s" % (body(r) == blk("two"), os.path.exists(lockd(r)), [f for f in os.listdir(T(r)) if ".tmp." in f]))
