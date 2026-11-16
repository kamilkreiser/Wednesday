#!/usr/bin/env python3
# Probe how THIS volume resolves unusual spellings of a name. Creates only empty files in argv[1].
import os, sys, subprocess
d = sys.argv[1]
os.makedirs(d, exist_ok=True)
base = {
    "ssh_probe": "ssh_probe",
    "docker_probe": "docker_probe",
    "zshrc_probe": "zshrc_probe",
    "fi_probe": "fi_probe",
    "st_probe": "st_probe",
    "env_probe": "env_probe",
    "i_probe": "i_probe",
    "ss_probe": "ss_probe",
}
for b in base:
    open(os.path.join(d, b), "w").close()
tests = [
    ("long s", "ſsh_probe", "ssh_probe"),
    ("Kelvin", "docKer_probe", "docker_probe"),
    ("fi ligature", "ﬁ_probe", "fi_probe"),
    ("st ligature", "ﬆ_probe", "st_probe"),
    ("fullwidth z", "ｚshrc_probe", "zshrc_probe"),
    ("ZWSP inside", "zsh​rc_probe", "zshrc_probe"),
    ("ZWJ inside", "zsh‍rc_probe", "zshrc_probe"),
    ("soft hyphen", "zsh­rc_probe", "zshrc_probe"),
    ("var selector", "zsh️rc_probe", "zshrc_probe"),
    ("BOM FEFF", "zsh﻿rc_probe", "zshrc_probe"),
    ("tag char", "zsh\U000e0041rc_probe", "zshrc_probe"),
    ("RLO", "zsh‮rc_probe", "zshrc_probe"),
    ("upper", "ZSHRC_PROBE", "zshrc_probe"),
    ("dotless i", "ı_probe", "i_probe"),
    ("capital I dot", "İ_probe", "i_probe"),
    ("sharp s", "ß_probe", "ss_probe"),
    ("capital sharp s", "ẞ_probe", "ss_probe"),
    ("math bold e", "\U0001d41env_probe", "env_probe"),
    ("superscript", "ᵉnv_probe", "env_probe"),
    ("trailing dot", "env_probe.", "env_probe"),
    ("trailing space", "env_probe ", "env_probe"),
    ("combining dot below on s", "ṣsh_probe", "ssh_probe"),
]
for label, name, target in tests:
    p = os.path.join(d, name)
    try:
        st = os.stat(p)
        same = os.path.samefile(p, os.path.join(d, target))
        print(f"{label:28} RESOLVES {'(same file as ' + target + ')' if same else '(different file)'}")
    except FileNotFoundError:
        print(f"{label:28} not found")
    except OSError as e:
        print(f"{label:28} error {e}")
# NFD vs NFC: create precomposed, look up decomposed
open(os.path.join(d, "café_probe"), "w").close()
print("NFD lookup of NFC name     ", "RESOLVES" if os.path.exists(os.path.join(d, "café_probe")) else "not found")
# exec lookup through PATH with a folded name: a harmless script that prints a word
s = os.path.join(d, "sudoprobe")
with open(s, "w") as f:
    f.write("#!/bin/sh\necho EXEC-FOUND\n")
os.chmod(s, 0o755)
for sh in ["/bin/zsh", "/bin/bash"]:
    r = subprocess.run([sh, "-c", "ſudoprobe"], env={"PATH": d + ":/usr/bin:/bin"}, capture_output=True, text=True)
    print(f"{sh} exec of 'ſudoprobe' via PATH: rc={r.returncode} out={r.stdout.strip()!r} err={r.stderr.strip()[:80]!r}")
# brace expansion
for sh in ["/bin/zsh", "/bin/bash"]:
    r = subprocess.run([sh, "-c", "printf '%s\\n' " + d + "/.a{ws,}/credentials"], capture_output=True, text=True)
    print(f"{sh} brace: {r.stdout.split()}")
# glob with folded literal component in another component
os.makedirs(os.path.join(d, ".docker"), exist_ok=True)
open(os.path.join(d, ".docker", "config.json"), "w").close()
for sh in ["/bin/zsh", "/bin/bash"]:
    r = subprocess.run([sh, "-c", "ls " + d + "/.docKer/conf*.json"], capture_output=True, text=True)
    print(f"{sh} ls .doc<Kelvin>er/conf*.json: rc={r.returncode} {r.stdout.strip()!r} {r.stderr.strip()[:100]!r}")
