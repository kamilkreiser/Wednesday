#!/usr/bin/env python3
"""closed_table.py <work dir> <socket dir> - N5/N7 from trees named for each of the three seats.
Part 1: every scope line that asks for ANOTHER seat's ledger, archive, daily folder, pickup or week file (exact
name, glob, '..', case, another kind) must be REFUSED at load: rc 2, no cluster directory, no lock file, no server.
Part 2: the seat's OWN names turned into symlinks or hard links to another seat's files: nothing of theirs indexed.
Part 3: the pickup table, and what the real tasks folder holds (names only)."""
import os, sys, shutil, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *

work, sock = sys.argv[1], sys.argv[2]
P = lambda s: print(s, flush=True)
lane = os.path.dirname(TOOL); pf = os.path.dirname(lane)
LEDG = {"wednesday": ("_ledger.md", "_ledger_archive.md"), "tuesday": ("_ledger_laptop_datasec.md", "_ledger_laptop_datasec_archive.md"),
        "friday": ("_ledger_friday.md", "_ledger_friday_archive.md")}
DAILY = {"wednesday": "0_Brain/daily", "tuesday": "0_Brain/daily_tuesday", "friday": "0_Brain/daily_friday"}
PICK = {"wednesday": ("NEXT-PICKUP.md", "WEEK-INSTRUCTION.md"), "tuesday": ("NEXT-PICKUP-TUESDAY.md", "WEEK-INSTRUCTION-TUESDAY.md"),
        "friday": ("NEXT-PICKUP-FRIDAY.md", "WEEK-INSTRUCTION-FRIDAY.md")}
SEATS = ("wednesday", "tuesday", "friday")


def fixture(root):
    rows = base_tree(root)
    os.remove(os.path.join(root, L + "_ledger.md"))
    for s in SEATS:
        for i, n in enumerate(LEDG[s]):
            w(root, L + n, "# Ledger\n\n| Date | What |\n|---|---|\n| 2027-01-01 | **zled%s%d thing** Rule: do it. | x |\n" % (s, i))
        w(root, DAILY[s] + "/2027-01-20.md", "# d\n\n## Sessions\n- 06:19 the word is zday%s here.\n" % s)
        for i, n in enumerate(PICK[s]):
            w(root, "0_Brain/tasks/" + n, "# p\n\nzpick%s%d\n" % (s, i))
    w(root, L + "_rules_index.tsv", "# h\n" + "\n".join(rows) + "\n")


def sim(seat):
    t = "%s/sim/%s/2_Project_Files" % (work, seat.upper())
    os.makedirs(t + "/fleet/cockpit"); os.makedirs(t + "/tools")
    shutil.copytree(lane, t + "/brain-db", ignore=shutil.ignore_patterns("evidence", "__pycache__"))
    shutil.copy(pf + "/fleet/cockpit/seat_resolve.sh", t + "/fleet/cockpit/"); shutil.copy(pf + "/tools/seat_note.sh", t + "/tools/")
    return t + "/brain-db/braindb.sh"


def base_scope(seat):
    p = lane + ("/scope/wednesday.scope" if seat == "wednesday" else "/proposed/scope/%s.scope" % seat)
    return open(p).read()


def servers(under):
    snap = subprocess.run(["ps", "-axww", "-o", "pid=,comm="], stdout=subprocess.PIPE).stdout.decode()
    n = 0
    for line in snap.strip().split("\n"):
        pid, comm = line.strip().split(None, 1)
        if comm.rsplit("/", 1)[-1] == "postgres":
            cmd = subprocess.run(["ps", "-ww", "-p", pid, "-o", "command="], stdout=subprocess.PIPE).stdout.decode()
            if " -D " + under in cmd:
                n += 1
    return n


root = work + "/tree"; fixture(root)
tot = ref = 0; notref = []
for seat in SEATS:
    tl = sim(seat); own_l = "0_Brain/learnings"; lines = []
    for o in SEATS:
        if o == seat:
            continue
        for n in LEDG[o]:
            lines += ["allow ledger %s/%s" % (own_l, n), "allow ledger %s/../learnings/%s" % (own_l, n), "allow ledger 0_brain/learnings/%s" % n,
                      "allow ledger 0_Brain/Learnings/%s" % n, "allow ledger %s/%s" % (own_l, n.upper()), "allow ledger ./%s/%s" % (own_l, n),
                      "allow ledger %s//%s" % (own_l, n), "allow skill %s/%s" % (own_l, n), "allow daily %s/%s" % (own_l, n),
                      "allow rules %s/%s" % (own_l, n), "allow rules_index %s/%s" % (own_l, n), "allow identity %s/%s" % (own_l, n),
                      "allow pickup %s/%s" % (own_l, n), "allow architecture %s/%s" % (own_l, n), "allow people %s/%s" % (own_l, n)]
        d = DAILY[o]
        lines += ["allow daily %s/20*.md" % d, "allow daily %s/*.md" % d, "allow daily %s/2027-01-20.md" % d, "allow daily %s/../%s/20*.md" % (DAILY[seat], d.split("/")[1]),
                  "allow daily %s/20*.md" % d.lower(), "allow daily %s/20*.md" % d.upper(), "allow daily %s/./20*.md" % d, "allow skill %s/*.md" % d,
                  "allow lesson %s/20*.md" % d, "allow identity %s/*.md" % d, "allow ledger %s/2027-01-20.md" % d, "allow pickup %s/2027-01-20.md" % d,
                  "allow daily 0_Brain/daily*/20*.md", "allow daily 0_Brain/daily_*/20*.md", "allow daily 0_Brain/*/20*.md", "allow daily 0_Brain/daily?%s/20*.md" % d.split("daily")[1][1:]]
        for n in PICK[o]:
            lines += ["allow pickup 0_Brain/tasks/%s" % n, "allow pickup 0_Brain/tasks/../tasks/%s" % n, "allow pickup 0_brain/tasks/%s" % n,
                      "allow pickup 0_Brain/tasks/%s" % n.lower(), "allow skill 0_Brain/tasks/%s" % n, "allow ledger 0_Brain/tasks/%s" % n,
                      "allow daily 0_Brain/tasks/%s" % n, "allow lesson 0_Brain/tasks/%s" % n, "allow rules 0_Brain/tasks/%s" % n]
    lines += ["allow ledger %s/_ledger*.md" % own_l, "allow ledger %s/_ledger_*.md" % own_l, "allow ledger %s/_ledger?*.md" % own_l, "allow ledger %s/*.md" % own_l,
              "allow ledger %s/_ledger[_a-z]*.md" % own_l, "allow ledger %s/*" % own_l, "allow pickup 0_Brain/tasks/*.md", "allow pickup 0_Brain/tasks/NEXT-PICKUP*.md",
              "allow pickup 0_Brain/tasks/WEEK-INSTRUCTION*.md", "allow pickup 0_Brain/tasks/*", "allow skill 0_Brain/tasks/*.md", "allow skill 0_Brain/*.md",
              "allow skill 0_Brain/skills/../tasks/*.md", "allow skill 0_Brain/skills/../learnings/_ledger*.md", "allow skill 0_Brain/skills/../daily*/*.md"]
    sr = 0
    for i, line in enumerate(lines):
        sc = "%s/%s-%03d.scope" % (work, seat, i); open(sc, "w").write(base_scope(seat) + "\n" + line + "\n")
        pgd = "%s/pg-%s-%03d" % (work, seat, i)
        rc, out = tool(["rebuild"], root, pgd, sock, scope=sc, toolpath=tl)
        tot += 1
        if rc == 2 and "REFUSED" in out and not os.path.exists(pgd) and not os.path.exists(pgd + ".lock"):
            ref += 1; sr += 1
        else:
            notref.append((seat, line, rc, os.path.exists(pgd), out.strip().split("\n")[-1][:120]))
    P("%-9s tree: %d lines asking for another seat's records or a wider place; refused at load with nothing created: %d" % (seat.upper(), len(lines), sr))
P("PART 1 TOTAL: %d lines, %d refused (rc 2, 'REFUSED', no cluster directory, no lock file); NOT refused: %d" % (tot, ref, len(notref)))
for x in notref:
    P("   NOT REFUSED: %s" % (x,))
P("   servers with -D under my work dir after part 1: %d (control below shows the same count seeing a running one)" % servers(work))
# control: a line that IS in the table is accepted
for seat in SEATS:
    tl = "%s/sim/%s/2_Project_Files/brain-db/braindb.sh" % (work, seat.upper())
    sc = "%s/%s-own.scope" % (work, seat); open(sc, "w").write(base_scope(seat) + "\nallow pickup 0_Brain/tasks/%s\nallow pickup 0_Brain/tasks/%s\nallow lesson 0_Brain/learnings/_ledger*.md\nallow lesson 0_Brain/learnings/*.md\n" % PICK[seat])
    pgd = "%s/pgown-%s" % (work, seat)
    rc, out = tool(["rebuild"], root, pgd, sock, scope=sc, toolpath=tl)
    d, err = dump(sock)
    P("(control) %-9s scope + its OWN two pickup lines + 'allow lesson learnings/_ledger*.md' + 'allow lesson learnings/*.md' (kind lesson, inside the table's folder: ACCEPTED at load by design): rc %d ; servers running %d" % (seat.upper(), rc, servers(work)))
    if d:
        for o in SEATS:
            toks = ["zled%s0" % o, "zled%s1" % o, "zday%s" % o, "zpick%s0" % o, "zpick%s1" % o]
            P("     tokens of %-9s records in the %s index: %s%s" % (o, seat, " ".join("%s=%d" % (t, d.count(t)) for t in toks), "   <- its own (want > 0)" if o == seat else "   <- want all 0"))
        P("     the ledger-named files under kind lesson: %s" % [l.strip() for l in out.split("\n") if "ledger, digest or index" in l or "not a lesson file name" in l][:2])
    # Part 2 on this seat: own names made links to another seat's files
    other = [o for o in SEATS if o != seat][0]
    back = work + "/moved-%s" % seat; os.makedirs(back)
    own_led = os.path.join(root, L + LEDG[seat][0]); own_arch = os.path.join(root, L + LEDG[seat][1])
    own_day = os.path.join(root, DAILY[seat]); own_pick = os.path.join(root, "0_Brain/tasks", PICK[seat][0]); own_week = os.path.join(root, "0_Brain/tasks", PICK[seat][1])
    for p_ in (own_led, own_arch, own_day, own_pick, own_week):
        os.rename(p_, os.path.join(back, os.path.basename(p_)))
    os.symlink(LEDG[other][0], own_led)                                              # relative symlink, same folder
    os.link(os.path.join(root, L + LEDG[other][1]), own_arch)                         # hard link
    os.symlink(os.path.basename(DAILY[other]), own_day)                              # the daily FOLDER is a symlink
    os.symlink(PICK[other][0], own_pick); os.link(os.path.join(root, "0_Brain/tasks", PICK[other][1]), own_week)
    rc, out = tool(["rebuild"], root, pgd, sock, scope=sc, toolpath=tl); d, err = dump(sock)
    toks = ["zled%s0" % other, "zled%s1" % other, "zday%s" % other, "zpick%s0" % other, "zpick%s1" % other]
    P("  PART 2 %-9s: its own ledger -> symlink, archive -> hard link, daily folder -> symlink, pickup -> symlink, week file -> hard link, all to %s's: rebuild rc %d" % (seat.upper(), other, rc))
    P("     %s's tokens in the index: %s (want all 0); control qzcontrol %d" % (other, " ".join("%s=%d" % (t, (d or "").count(t)) for t in toks), (d or "").count("qzcontrol")))
    P("     named in the report: %s" % [l.strip()[:110] for l in out.split("\n") if "[symlink]" in l or "[hard link" in l or "sits under a symlink" in l])
    for p_ in (own_led, own_arch, own_day, own_pick, own_week):
        os.unlink(p_); os.rename(os.path.join(back, os.path.basename(p_)), p_)
    rc, o2 = tool(["stop"], root, pgd, sock, scope=sc, toolpath=tl)
P("servers with -D under my work dir at the end: %d" % servers(work))
P("== PART 3. the real 0_Brain/tasks folder, NAMES AND SIZES ONLY (no file opened)")
td = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks"
for n in sorted(os.listdir(td)):
    st = os.lstat(os.path.join(td, n))
    inany = [s for s in SEATS if n in PICK[s]]
    P("   %-44s %9d bytes   %s" % (n, st.st_size, "in the table for: " + ",".join(inany) if inany else "in no seat's table"))
