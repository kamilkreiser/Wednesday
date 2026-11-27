# QA-POLICY-B timing driver: per row, INTERLEAVED  X, Y, X, Y  (each process: smallest of five per list), the smaller
# of the two runs kept per (row, list, side). usage:
#   python3 -B time_drive.py <exe X> <exe Y> <rows.jsonl> <out.tsv> <lists> <label> [first:last]
import os, subprocess, sys, time, json
X, Y, ROWS, OUT, LISTS, LABEL = sys.argv[1:7]
rng = sys.argv[7] if len(sys.argv) > 7 else None
n = sum(1 for _ in open(ROWS))
idx = list(range(n))
if rng:
    a, b = rng.split(":"); idx = idx[int(a):int(b)]
heavy = lambda: subprocess.run(["bash", "/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh"], capture_output=True, text=True).stdout.strip()
env0 = dict(os.environ, QPB_MODE="time", QPB_ROWS=ROWS, QPB_LIST=LISTS)
def run(exe, i, side):
    env = dict(env0, QPB_IDX=str(i), QPB_FIX=f"/private/tmp/claude-501/qpb/fixt/{LABEL}-{side}")
    p = subprocess.run([exe, "qpb", "--exact", "--nocapture", "--test-threads", "1"], env=env, capture_output=True, text=True)
    out = {}
    for l in p.stdout.splitlines():
        if "QPB-TIME " in l:
            l = l[l.index("QPB-TIME "):]   # with one test and --nocapture the line starts "test qpb ... "
            f = l.split(" | ")[0].split()
            out[f[2]] = (int(f[3]), " ".join(f[4:8]))
    if p.returncode != 0 or not out:
        raise SystemExit(f"run failed {exe} {i}: rc {p.returncode} {p.stderr[-500:]}")
    return out
os.makedirs("/private/tmp/claude-501/qpb/fixt", exist_ok=True)
t0 = time.time()
with open(OUT, "w") as f:
    f.write(f"# {LABEL} X={X} Y={Y} lists={LISTS} heavy_start={heavy()} start={time.strftime('%T')}\n")
    for k, i in enumerate(idx):
        r1 = run(X, i, "x"); r2 = run(Y, i, "y"); r3 = run(X, i, "x"); r4 = run(Y, i, "y")
        for lst in LISTS.split(","):
            x = min(r1[lst][0], r3[lst][0]); y = min(r2[lst][0], r4[lst][0])
            f.write(f"{i}\t{lst}\t{x}\t{y}\t{(y - x) / 1000:.1f}\t{r1[lst][1]}\t{r2[lst][1]}\n")
        f.flush()
        if k % 50 == 0:
            f.write(f"# progress {k}/{len(idx)} heavy={heavy()} t={time.strftime('%T')}\n")
    f.write(f"# end={time.strftime('%T')} heavy_end={heavy()} seconds={time.time() - t0:.0f}\n")
print(f"{LABEL} done {len(idx)} rows in {time.time() - t0:.0f}s")
