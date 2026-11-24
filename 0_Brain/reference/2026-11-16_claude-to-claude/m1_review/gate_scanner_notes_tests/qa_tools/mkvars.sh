#!/bin/bash
# QA-SCANNER-NOTES: build scratch scanner modules (old heads from git, one-item-reverted copies of the head).
# Usage: mkvars.sh <clone> ; writes under <clone>/crates/coagent-scanner/tests/qa_*/ (never committed)
set -eu
C="$1"; T="$C/crates/coagent-scanner/tests"; S=crates/coagent-scanner/src
mk() { # name sha
  mkdir -p "$T/$1"
  git -C "$C" show "$2:$S/lib.rs" > "$T/$1/mod.rs"
  git -C "$C" show "$2:$S/families.rs" | sed 's/use crate::/use super::/' > "$T/$1/families.rs"
}
# sub <dir> <file> <python-literal old> <python-literal new>: exactly one replacement, else fail
sub() { python3 -B -I -c 'import sys
p,o,n=sys.argv[1],sys.argv[2],sys.argv[3]
s=open(p).read(); c=s.count(o)
assert c==1,(p,o,c)
open(p,"w").write(s.replace(o,n))' "$T/$1/$2" "$3" "$4"; }
mk qa_main f193620c14082df985cff3bb1b96d02575218811
mk qa_old  b0835a90c1c14638537707d9ebcc7cec5471f911
H=430dde30be41e026b909e271f698f8013325e892
for v in v_r1 v_r2 v_r2_3v v_r3 v_all3 v_ansi v_lf v_htp v_m3 v_none; do mk qa_$v $H; done
# item 1 reverted: main's lone-CR rule
sub qa_v_r1 families.rs 'b'"'"'\r'"'"' if cfg!(coagent_scanner_red = "cr_run_split")' 'b'"'"'\r'"'"' if true'
# item 2 reverted: main's one stripped view
sub qa_v_r2 mod.rs 'if cfg!(coagent_scanner_red = "one_stripped_view") {' 'if true {'
# item 2 with three views only (view 4 dropped): FR-2's first state
sub qa_v_r2_3v mod.rs 'if has_format && text.contains("\u{1b}[") {' 'if false {'
# item 3 reverted: forms (a)-(c) off
sub qa_v_r3 families.rs 'let forms = !cfg!(coagent_scanner_red = "argv_space_only");' 'let forms = false;'
# all three
sub qa_v_all3 families.rs 'b'"'"'\r'"'"' if cfg!(coagent_scanner_red = "cr_run_split")' 'b'"'"'\r'"'"' if true'
sub qa_v_all3 mod.rs 'if cfg!(coagent_scanner_red = "one_stripped_view") {' 'if true {'
sub qa_v_all3 families.rs 'let forms = !cfg!(coagent_scanner_red = "argv_space_only");' 'let forms = false;'
# the r2 check's causes, on the head (for b0835a9 -> head)
sub qa_v_ansi mod.rs '&& !cfg!(coagent_scanner_red = "ansi_kept")' '&& false'
sub qa_v_lf families.rs '_ if cfg!(coagent_scanner_red = "line_end_lf_only") => 0,' '_ if true => 0,'
sub qa_v_htp families.rs 'let letters = &b[i + 1..e];' 'let letters = &lower[i + 1..e];'
python3 -B -I -c 'import sys
p=sys.argv[1]; s=open(p).read()
o="""        | '"'"'\\u{17B4}'"'"' | '"'"'\\u{17B5}'"'"' | '"'"'\\u{180B}'"'"'..='"'"'\\u{180D}'"'"' | '"'"'\\u{180F}'"'"' | '"'"'\\u{206A}'"'"'..='"'"'\\u{206F}'"'"'
        | '"'"'\\u{1BCA0}'"'"'..='"'"'\\u{1BCA3}'"'"' | '"'"'\\u{0600}'"'"'..='"'"'\\u{0605}'"'"' | '"'"'\\u{FFF9}'"'"'..='"'"'\\u{FFFB}'"'"')"""
assert s.count(o)==1,s.count(o)
open(p,"w").write(s.replace(o,"        )"))' "$T/qa_v_m3/mod.rs"
# v_none: the head unchanged (control that the copy itself equals the library)
for d in "$T"/qa_v_*; do echo "$(basename $d): $(diff <(git -C "$C" show $H:$S/lib.rs) $d/mod.rs | grep -c '^>') mod.rs lines, $(diff <(git -C "$C" show $H:$S/families.rs | sed 's/use crate::/use super::/') $d/families.rs | grep -c '^>') families.rs lines changed"; done
# (added) b0835a9 without its netrc rule, to attribute lf PasswordArgument losses to N-R3 by an own method
mkdir -p "$T/qa_old_nonetrc"; cp "$T/qa_old/mod.rs" "$T/qa_old_nonetrc/mod.rs"
python3 -B -I -c 'import sys
p=sys.argv[1]; s=open(sys.argv[2]).read(); o="    netrc_passwords(t, r);\n"; assert s.count(o)==1
open(p,"w").write(s.replace(o,"    // QA: netrc rule removed\n"))' "$T/qa_old_nonetrc/families.rs" "$T/qa_old/families.rs"
# (added) line-end probes: main and head copies with one pub helper appended (behaviour unchanged)
for pair in "qa_le_main:qa_main:line_term(t.b, i)" "qa_le_head:qa_v_none:line_term(t.b, &t.cr_lf, i)"; do
  d="${pair%%:*}"; rest="${pair#*:}"; src="${rest%%:*}"; call="${rest#*:}"
  mkdir -p "$T/$d"; cp "$T/$src/families.rs" "$T/$d/families.rs"
  sed 's/^mod families;$/pub mod families;/' "$T/$src/mod.rs" > "$T/$d/mod.rs"
  grep -q '^pub mod families;$' "$T/$d/mod.rs"
  printf '\n/// QA probe: every index where a line terminator starts (for the line shapes), with its length.\npub fn qa_line_ends(s: &str) -> Vec<(usize, usize)> {\n    let t = Text::new(s);\n    (0..t.b.len()).map(|i| (i, %s)).filter(|x| x.1 > 0).collect()\n}\n' "$call" >> "$T/$d/families.rs"
done
