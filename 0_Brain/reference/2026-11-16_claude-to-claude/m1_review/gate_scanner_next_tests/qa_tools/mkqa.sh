#!/bin/bash
# QA-SCANNER-NEXT: scratch scanner modules in <clone>/crates/coagent-scanner/tests/ (never committed).
#   qa_base     = debbb44's src (lib.rs -> mod.rs; families.rs with `use crate::` -> `use super::`)
#   qa_headcopy = dd70630's src the same way, unchanged (control: the copy equals the library)
#   qa_headmut  = qa_headcopy with ONE character changed in a rule (HEX_MIN 16 -> 15) (planted control)
#   qa_t03_base.rs = debbb44's t03 (its lists, as a module)
set -eu
C="$1"; T="$C/crates/coagent-scanner/tests"; S=crates/coagent-scanner/src
B=debbb4442fc90b1d5c1f04f123a665dcd8cf381f; H=dd70630dd74cd1dac9261f1ac83542514562c767
mk() { mkdir -p "$T/$1"; git -C "$C" show "${2}:$S/lib.rs" > "$T/$1/mod.rs"
       git -C "$C" show "${2}:$S/families.rs" | sed 's/use crate::/use super::/' > "$T/$1/families.rs"; }
mk qa_base $B; mk qa_headcopy $H; mk qa_headmut $H
python3 -B -I -c 'import sys
p=sys.argv[1]; s=open(p).read(); o="pub(crate) const HEX_MIN: usize = 16;"; assert s.count(o)==1
open(p,"w").write(s.replace(o,"pub(crate) const HEX_MIN: usize = 15;"))' "$T/qa_headmut/families.rs"
git -C "$C" show "${B}:crates/coagent-scanner/tests/t03_known_overflag.rs" > "$T/qa_t03_base.rs"
for d in qa_base qa_headcopy qa_headmut; do
  echo "$d: mod.rs vs head lib.rs $(diff <(git -C "$C" show "${H}:$S/lib.rs") "$T/$d/mod.rs" | grep -c '^[<>]') lines; families.rs vs head (crate->super) $(diff <(git -C "$C" show "${H}:$S/families.rs" | sed 's/use crate::/use super::/') "$T/$d/families.rs" | grep -c '^[<>]') lines; families.rs vs own git sha raw $(diff <(git -C "$C" show "${H}:$S/families.rs") "$T/$d/families.rs" | grep -c '^>') lines"
done
echo "qa_base vs base git: lib $(git -C "$C" show "${B}:$S/lib.rs" | diff - "$T/qa_base/mod.rs" | wc -l) diff lines; families $(git -C "$C" show "${B}:$S/families.rs" | diff - "$T/qa_base/families.rs" | grep -c '^>') changed"
