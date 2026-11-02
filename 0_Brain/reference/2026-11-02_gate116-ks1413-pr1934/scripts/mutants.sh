#!/bin/bash
# Mutants on a COPY of the head tree (wt_mut), product only; tests untouched; sha256 restore check.
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate116-ks1413-pr1934; R=$D/repo
git -C $R worktree add -f $D/wt_mut pr1934 >/dev/null 2>&1
M=$D/wt_mut
T=$M/Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh
B=$M/Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh
A=$M/Start_Up/start-secuura.sh; L=$M/Blockchain/Dev/scripts/start-local.sh
shaA=$(shasum -a 256 $A | cut -c1-12); shaL=$(shasum -a 256 $L | cut -c1-12)
run() { echo "== $1"; bash $T 2>&1 | grep -E '^(ok|FAIL)|passed'; echo "banner suite: $(bash $B 2>&1 | grep -E 'FAIL' | head -3 | tr '\n' ' ')"; }
restore() { git -C $M checkout -q -- Start_Up/start-secuura.sh Blockchain/Dev/scripts/start-local.sh; [ "$(shasum -a 256 $A | cut -c1-12)" = $shaA ] && [ "$(shasum -a 256 $L | cut -c1-12)" = $shaL ] && echo RESTORE_OK || echo RESTORE_FAIL; }
run "M0 head unmutated"
# M1: undo secuura hunk (restore value in echo)
sed -i '' 's|(password: the published demo default - see CLAUDE.md)|/ demo123|' $A; run "M1 start-secuura value back"; restore
# M2: undo local hunk
sed -i '' 's|(password: the published demo default - see CLAUDE.md)|/ demo123|' $L; run "M2 start-local value back"; restore
# M3: value via printf (evades echo matcher?) in secuura
sed -i '' 's|^echo -e "    Issuer:  demo@secuura.io (password: the published demo default - see CLAUDE.md)"|printf "    Issuer:  demo@secuura.io / demo123\\n"|' $A; run "M3 start-secuura value via printf"; restore
# M4: value via echo on a different physical line (echo, then continuation)
sed -i '' 's|^echo -e "    Issuer:  demo@secuura.io (password: the published demo default - see CLAUDE.md)"|echo -e "    Issuer:  demo@secuura.io"; echo "pw demo123"|' $A; run "M4 start-secuura second echo with value (same line)"; restore
# M5: value in a variable-expanded echo
sed -i '' 's|^echo -e "    Issuer:  demo@secuura.io (password: the published demo default - see CLAUDE.md)"|P=demo; echo -e "    Issuer:  demo@secuura.io ${P}123"|' $A; run "M5 start-secuura value assembled by expansion"; restore
# M6: banner line dropped (issuer account no longer named)
sed -i '' '/Issuer:  demo@secuura.io (password/d' $A; run "M6 start-secuura issuer line deleted"; restore
# M7: Admin password echoed in start-local is untouched by tests (expect survive = out of test scope)
sed -i '' 's|echo "    Admin:   admin@secuura.com / admin123"|echo "    Admin:   admin@secuura.com / admin123x"|' $L; run "M7 admin123 line changed (not covered)"; restore
