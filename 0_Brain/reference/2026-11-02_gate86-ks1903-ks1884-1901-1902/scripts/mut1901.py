#!/usr/bin/env python3
import os, subprocess
W = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate86-ks1903-ks1884-1901-1902"
SD = W + "/wt_1901/Blockchain/Dev/scripts/"
S = open(SD + "check-dockerfile-non-root.sh").read()
SUITE = SD + "__tests__/check_dockerfile_non_root_reports_root.test.sh"
def rep(a, b):
    assert a in S, a
    return S.replace(a, b, 1)
STRIP = "  last_user=${last_user%%:*}\n"
LOW = "  last_user=$(printf '%s' \"$last_user\" | tr 'A-Z' 'a-z')\n"
M = {
 "M1_no_group_strip": rep(STRIP, ""),
 "M2_no_lowercase": rep(LOW, ""),
 "M3_strip_shortest_suffix_%:*": rep(STRIP, "  last_user=${last_user%:*}\n"),
 "M4_keep_group_##*:": rep(STRIP, "  last_user=${last_user##*:}\n"),
 "M5_lower_before_strip(order swapped)": rep(STRIP + LOW, LOW + STRIP),
 "M6_tr_A-Z_to_a-z_no_op(tr a-z a-z)": rep("tr 'A-Z' 'a-z'", "tr 'a-z' 'a-z'"),
 "M7_lower_only_A-M": rep("tr 'A-Z' 'a-z'", "tr 'A-M' 'a-m'"),
 "M8_drop_0_check": rep('|| [ "$last_user" = "0" ]', ''),
 "M9_drop_root_check_keep_0": rep('[ "$last_user" = "root" ] || ', ''),
 "M10_strip_only_if_group_is_digits": rep(STRIP, "  case \"$last_user\" in *:[0-9]*) last_user=${last_user%%:*};; esac\n"),
 "M11_strip_only_root_prefix": rep(STRIP, "  case \"$last_user\" in root:*) last_user=root;; esac\n"),
 "M12_strip_only_0_and_root_same_group": rep(STRIP, "  case \"$last_user\" in root:root|0:0) last_user=${last_user%%:*};; esac\n"),
 "M13_lowercase_only_ROOT": rep("tr 'A-Z' 'a-z'", "sed 's/ROOT/root/'"),
}
out = []
for n, s in M.items():
    assert s != S, n
    d = "/private/tmp/gate86_spark/mut1901/" + n.split("(")[0]
    os.makedirs(d, exist_ok=True)
    open(d + "/check-dockerfile-non-root.sh", "w").write(s)
    p = subprocess.run(["bash", SUITE], capture_output=True, text=True, env=dict(os.environ, CHECK_DOCKERFILE_NON_ROOT_SH=d + "/check-dockerfile-non-root.sh"))
    open(W + "/logs/mut1901_%s.log" % n.split("(")[0], "w").write(p.stdout + "\n--- stderr ---\n" + p.stderr + "\nRC=%s\n" % p.returncode)
    last = [l for l in p.stdout.splitlines() if "passed" in l][-1:] or ["?"]
    out.append("%-42s rc=%s %-8s %s" % (n, p.returncode, "SURVIVED" if p.returncode == 0 else "KILLED", last[0].split(":")[-1].strip()))
print("\n".join(out)); open(W + "/logs/mut1901_summary.log", "w").write("\n".join(out) + "\n")
