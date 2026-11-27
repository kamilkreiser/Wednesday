#!/bin/bash
# The ONE licensed real dry run of round 4: reads only. Lists the real destination read-only before and after.
set -u
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/nas-backup; E="$L/evidence/round4"
naslist() { /opt/homebrew/bin/python3 - <<'PY'
import os, subprocess
for p in ("/Volumes/DEV-Working", "/Volumes/DEV-Working/Secuura", "/Volumes/DEV-Working/General", "/Volumes/DEV-Working/General/Wednesday"):
    print(p, sorted(os.listdir(p)), "mtime", int(os.stat(p).st_mtime), "is a symlink:", os.path.islink(p))
r = subprocess.run(["/bin/df", "-k", "/Volumes/DEV-Working"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
print(r.stdout.strip().splitlines()[-1]); print(r.stderr.strip())
PY
}
naslist > "$E/nas_before_dry.txt" 2> "$E/nas_before_dry.err"
{ date "+%Y-%m-%d %H:%M:%S %Z"; uptime; shasum -a 256 "$L/nb_core.py"; df -h / | tail -1; } > "$E/real_dry_times.txt" 2>&1
bash "$L/nas_backup.sh" --dry > "$E/real_dry_run_round4.out" 2> "$E/real_dry_run_round4.err"; echo "dry rc=$?" >> "$E/real_dry_times.txt"
{ date "+%Y-%m-%d %H:%M:%S %Z"; uptime; df -h / | tail -1; } >> "$E/real_dry_times.txt" 2>&1
naslist > "$E/nas_after_dry.txt" 2> "$E/nas_after_dry.err"
diff "$E/nas_before_dry.txt" "$E/nas_after_dry.txt" > "$E/nas_diff.txt" 2>&1; echo "nas diff rc=$?" >> "$E/real_dry_times.txt"
