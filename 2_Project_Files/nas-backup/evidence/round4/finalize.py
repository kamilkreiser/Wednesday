#!/usr/bin/env python3
# finalize.py — after the final pass: copy its outputs into evidence/round4, run the claims program, fill the
# ROUND 4 section and put it on top of STATUS.md. Prints what it did. Writes only inside the lane.
import os, re, shutil, subprocess, sys, time
SP = os.path.dirname(os.path.abspath(__file__))
L = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/nas-backup"
E = L + "/evidence/round4"
PY = "/opt/homebrew/bin/python3"


def sh(argv):
    r = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    return r.returncode, r.stdout


mut = open(SP + "/final_mutants.txt", encoding="utf-8", errors="replace").read()
m = re.search(r"=== (\d+) mutants caught, (\d+) survived or broken \(of (\d+)\)", mut)
assert m, "the mutant run has no summary line"
caught, bad, total = int(m.group(1)), int(m.group(2)), int(m.group(3))
mut_name = "mutants_round4_final_%d_of_%d.txt" % (caught, total)
shutil.copyfile(SP + "/final_mutants.txt", E + "/" + mut_name)
shutil.copyfile(SP + "/final_suite.txt", E + "/tests_run_round4_final_694.txt")
for f in ("final_pass_times.txt", "final_pass_sha_check_after.txt", "disk_guard.log", "disk_guard2.sh", "final_pass2.sh", "finalize.py"):
    if os.path.exists(SP + "/" + f):
        shutil.copyfile(SP + "/" + f, E + "/" + f)
times = open(SP + "/final_pass_times.txt").read()
sha_after = open(SP + "/final_pass_sha_check_after.txt").read().strip()
# the lane's files against the snapshot the pass ran from
lines = []
same_all = True
for ln in open(SP + "/final2/sha256_of_the_snapshot.txt"):
    h, rel = ln.strip().split(None, 1)
    relp = rel.split("WEDNESDAY/2_Project_Files/nas-backup/", 1)[1]
    rc, o = sh(["/usr/bin/shasum", "-a", "256", L + "/" + relp])
    same = o.split()[0] == h
    same_all = same_all and same
    lines.append("%s  %s  %s" % (h, relp, "same in the lane now" if same else "DIFFERS IN THE LANE NOW"))
open(E + "/final_pass_lane_against_the_snapshot_after.txt", "w").write(
    "written %s\n" % time.strftime("%Y-%m-%d %H:%M:%S %Z") + "\n".join(lines) + "\n")
rc_claims, out_claims = sh([PY, L + "/tests/claims_check.py", E + "/tests_run_round4_final_694.txt", E + "/" + mut_name])
open(E + "/claims_check.out", "w").write(out_claims + "rc=%d\n" % rc_claims)
cm = re.search(r"=== (\d+) claims checked, (\d+) NOT SUPPORTED ===", out_claims)
claims_n, claims_bad = (int(cm.group(1)), int(cm.group(2))) if cm else (0, -1)
r4_n = sum(1 for ln in open(L + "/tests/claims.tsv", encoding="utf-8") if ln.startswith("r4-"))
tl = [x for x in times.split("\n") if re.match(r"^\d{4}-\d\d-\d\d ", x)]
t_suite0, t_mut0, t_mut1 = (tl + ["?", "?", "?"])[:3]
free_kb = int(sh(["/bin/df", "-k", "/"])[1].strip().split("\n")[-1].split()[3])
scratch_kb = int([x for x in sh(["/usr/bin/du", "-sk", SP])[1].strip().split("\n") if x[:1].isdigit()][-1].split()[0])
not_caught = [ln.strip()[:160] for ln in mut.split("\n") if ln.startswith("  SURVIVED") or ln.startswith("  BROKEN")]

def size(rel):
    return format(os.path.getsize(L + "/" + rel), ",")

def tree(rel):
    n = b = 0
    for dp, dn, fn in os.walk(L + "/" + rel):
        for f in fn:
            n += 1
            b += os.path.getsize(os.path.join(dp, f))
    return "%d files, %s bytes" % (n, format(b, ","))

unchanged = []
for a, b in (("nas_backup_watch.sh", "round3/nas_backup_watch.sh.round3"), ("seats/wednesday.conf", "round3/wednesday.conf.round3"),
             ("tests/claims_check.py", "round3/claims_check.py.round3"), ("tests/scan_dry_lists.py", "round3/scan_dry_lists.py.round3"),
             ("proposed/doctor_nasbackup_block.sh", "round3/doctor_nasbackup_block.sh.round3")):
    unchanged.append((a, open(L + "/" + a, "rb").read() == open(L + "/" + b, "rb").read()))
gs = sh(["/usr/bin/git", "-C", "/Volumes/DevMASTER/WEDNESDAY", "status", "--short", "--", "2_Project_Files/nas-backup"])[1]
files = ("`nb_core.py` %s (was 145,042) · `tests/run.sh` %s (was 114,480) · `tests/mutants.sh` %s (was 29,499) · `tests/claims.tsv` %s (was 12,552) · "
         "`README.md` %s (was 22,736) · `RESULT-quarantine-erase.md` %s (new) · `evidence/quarantine-erase/` (new: %s) · `evidence/round4/` (new: %s) · "
         "`round3/` (new: round 3's engine, suite, mutants, claims, README and four more, as they were).\n\n"
         "Unchanged, compared byte for byte with the copies in `round3/`: %s. Unchanged by `git status` (not listed as modified): `nas_backup.sh`, "
         "`nas_backup_nightly.sh`, `nb_common.sh`, `jobs/nasbackup.plist.template`, everything in `proposed/`, `seats/wednesday.tokens`, the HOLD files, "
         "`CENSUS.md`, `BRIEF.md`, the ANSWER files, the two earlier RESULT files. `git status` of the lane at the end:\n\n```\n%s```\n\n"
         "Run state on the drive, git-ignored, written by the one dry run and one held `--run`: `logs/wednesday/` (the dry run's lists), "
         "`manifests/wednesday/` (its manifest, its symlink lists and the 15 names lists), `state/wednesday.json` (one more `held` record)."
         % (size("nb_core.py"), size("tests/run.sh"), size("tests/mutants.sh"), size("tests/claims.tsv"), size("README.md"),
            size("RESULT-quarantine-erase.md"), tree("evidence/quarantine-erase"), tree("evidence/round4"),
            ", ".join("`%s`%s" % (a, "" if ok else " (DIFFERS)") for a, ok in unchanged), gs))
if bad == 0:
    mut_summary = "%d of %d caught, 0 survived or broken" % (caught, total)
else:
    mut_summary = "%d of %d caught, %d NOT caught" % (caught, total, bad)
mut_detail = ("%s (`evidence/round4/%s`). The pass: suite from %s, mutants from %s to %s, eight at a time. The ten files it ran are listed with "
              "their sha256 in `evidence/round4/final_pass_snapshot_sha256_before.txt`; hashed again after the pass: %s; and the lane's own "
              "files against that list afterwards: %s (`final_pass_lane_against_the_snapshot_after.txt`).%s"
              % (mut_summary, mut_name, t_suite0[11:19], t_mut0[11:19], t_mut1[11:19],
                 "identical" if sha_after == "" else "DIFFERENT (%s)" % sha_after[:120],
                 "all ten the same" if same_all else "NOT all the same: see the file",
                 "" if not not_caught else " NOT CAUGHT: " + " | ".join(not_caught)))
claims_detail = ("%d claims checked, %d NOT SUPPORTED, exit %d (`evidence/round4/claims_check.out`). %d of them are round 4's (ids `r4-`); the other %d "
                 "are round 3's, re-checked against tonight's outputs, with the two totals updated to 694 and 143."
                 % (claims_n, claims_bad, rc_claims, r4_n, claims_n - r4_n))
s = open(SP + "/STATUS_r4.md", encoding="utf-8").read()
rep = {"@@END@@": time.strftime("%H:%M"), "@@MUT_SUMMARY@@": mut_summary, "@@MUT_DETAIL@@": mut_detail,
       "@@CLAIMS@@": "%d claims, %d not supported" % (claims_n, claims_bad), "@@CLAIMS_DETAIL@@": claims_detail,
       "@@DISK@@": "%.0f GiB" % (free_kb / 1048576.0), "@@SCRATCH@@": "%.1f GB" % (scratch_kb / 1048576.0), "@@FILES@@": files}
for k, v in rep.items():
    assert k in s, k
    s = s.replace(k, v)
assert "@@" not in s
old = open(L + "/STATUS.md", encoding="utf-8").read()
cut = old.index("---\n\n(ROUND 3's status follows")
rest = old[cut:].split("\n", 3)[3]          # drop the separator, the blank line and the "(ROUND 3's status follows" line
assert rest.lstrip().startswith("READY FOR QA"), rest[:60]
if "--write" in sys.argv:
    open(L + "/STATUS.md", "w", encoding="utf-8").write(s + rest.lstrip("\n"))
    print("STATUS.md written")
else:
    open(SP + "/STATUS_preview.md", "w", encoding="utf-8").write(s + rest.lstrip("\n"))
    print("preview written (pass --write to put it in the lane)")
print("mutants:", mut_summary, "| claims:", claims_n, claims_bad, rc_claims, "| lane same as snapshot:", same_all, "| sha after:", repr(sha_after[:80]))
print("not caught:", not_caught)
