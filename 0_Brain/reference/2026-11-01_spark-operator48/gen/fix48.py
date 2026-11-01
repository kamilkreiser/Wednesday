PROD='systemTest/__tests__/package_format_gate.test.sh'
OLD='dead=$((50000 + RANDOM % 9000)); while kill -0 "$dead" 2>/dev/null; do dead=$((dead + 1)); done\n'
CMT='# KS-1926: ps -p, as the gate does; kill -0 reports EPERM, i.e. "dead", for a live process owned by another user.\n'
NEW='dead=$((50000 + RANDOM % 9000)); while ps -p "$dead" >/dev/null 2>&1; do dead=$((dead + 1)); done\n'
EDITS=[
 ('R20="$(fx_new case20)"; fx_pkg_tgz "$R20" inst prettier\n'+OLD, 'R20="$(fx_new case20)"; fx_pkg_tgz "$R20" inst prettier\n'+CMT+NEW),
 ('R32b="$(fx_new tree5b)"; fx_tree_pkg "$R32b" tp good; fx_commit "$R32b"; G32="$(sha_of "$R32b")"\n'+OLD, 'R32b="$(fx_new tree5b)"; fx_tree_pkg "$R32b" tp good; fx_commit "$R32b"; G32="$(sha_of "$R32b")"\n'+CMT+NEW),
]
