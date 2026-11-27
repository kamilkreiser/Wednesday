#!/usr/bin/env python3
# sweep.py — ANSWER-1 step 3: READ-ONLY walk of the mirror. Reports (a) every DIRECTORY named 4_Credentials or
# 3_Access_Keys (case-insensitive), by its own path and no further: the walk never enters one; (b) COUNTS ONLY of
# secret-shaped FILE names, grouped by the top two path levels under the mirror. No file is opened. No file name
# is printed. Nothing is moved or touched.
#   sweep.py <root> <max depth or 0 for unlimited> <out.json>
import json, os, sys, time
MIRROR = "/Volumes/Backup/DevMASTER-mirror"
SECRET_DIRS = ("4_credentials", "3_access_keys")
def classify(name):
    low = name.lower()
    if low == ".env" or low.startswith(".env."): return "env"
    if low in ("id_rsa", "id_ed25519"): return "ssh_private_name"
    if low in ("id_rsa.pub", "id_ed25519.pub"): return "ssh_pub"
    for ext in (".pem", ".key", ".p12", ".pfx"):
        if low.endswith(ext): return ext[1:]
    return None
def group(path):
    rel = os.path.relpath(path, MIRROR)
    parts = [] if rel == "." else rel.split(os.sep)
    return "/".join(parts[:2]) if parts else "(mirror top level)"
def main():
    root, maxdepth, outp = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    t0 = time.time(); found_dirs = []; counts = {}; n_dirs = n_files = errs = 0
    stack = [(root, 0)]
    while stack:
        path, depth = stack.pop()
        try:
            it = os.scandir(path)
        except OSError:
            errs += 1; continue
        with it:
            for e in it:
                try:
                    if e.is_dir(follow_symlinks=False):
                        n_dirs += 1
                        if e.name.lower() in SECRET_DIRS:
                            found_dirs.append(e.path)          # recorded; NOT entered
                        elif maxdepth == 0 or depth + 1 < maxdepth:
                            stack.append((e.path, depth + 1))
                    else:
                        n_files += 1
                        c = classify(e.name)
                        if c:
                            g = counts.setdefault(group(path), {})
                            g[c] = g.get(c, 0) + 1
                except OSError:
                    errs += 1
    res = {"root": root, "max_depth": maxdepth, "started": time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime(t0)),
           "finished": time.strftime("%Y-%m-%d %H:%M:%S %Z"), "seconds": round(time.time() - t0, 1),
           "dirs_seen": n_dirs, "files_seen": n_files, "read_errors": errs,
           "secret_named_directories": sorted(found_dirs), "secret_shaped_file_counts_by_top_two_levels": counts}
    json.dump(res, open(outp, "w"), indent=1, sort_keys=True)
    print(json.dumps(res, indent=1, sort_keys=True)); print("SWEEP-EXIT 0")
main()
