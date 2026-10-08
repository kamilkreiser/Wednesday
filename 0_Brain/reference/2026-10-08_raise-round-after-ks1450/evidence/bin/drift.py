"""For each item: every touched file that EXISTS at the Spark tip -- is its blob unchanged at develop?
A changed blob means git apply relied on offset/fuzz-free context search: the landing must be
verified by content, not by rc."""
import json, subprocess, sys
S = "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ba10491f-d904-4eb7-a83b-e46c1bc8cc8e/scratchpad/raise18"
CLONE = S + "/clone"
RUNS = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs"
DEV = sys.argv[1]
m = json.load(open(S + "/measure_0a6177.json"))


def blob(rev, path):
    p = subprocess.run(["git", "-C", CLONE, "ls-tree", rev, "--", path], capture_output=True, text=True)
    if p.returncode != 0:
        return "ERR:" + p.stderr.strip()[:60]
    return p.stdout.split()[2][:12] if p.stdout.strip() else "absent"


for run, r in m.items():
    if "files" not in r:
        continue
    tip = json.load(open(f"{RUNS}/spark_secuura_{run}/input.json"))["tip"]
    p = subprocess.run(["git", "-C", CLONE, "cat-file", "-t", tip], capture_output=True, text=True)
    if p.stdout.strip() != "commit":
        print(run, "TIP NOT PRESENT", tip[:12]); continue
    out = []
    for f in r["files"]:
        a, b = blob(tip, f), blob(DEV, f)
        if a == "absent" and b == "absent":
            continue
        out.append(("same" if a == b else f"CHANGED {a}->{b}") + " " + f.split("/")[-1])
    print(run, tip[:12], "|", "; ".join(out) if out else "all new files")
