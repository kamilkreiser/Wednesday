#!/bin/bash
# Probes run inline during gate M2-POLICY r2 (recorded here for reproduction). Scratch files only.
P=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m2_policy_r2/probe
mkdir -p "$P/fold" "$P/t"; printf 'alpha\nbeta\nTOKEN=x\n' > "$P/t/a.txt"
# 1. APFS full case folding (result here: long s, ﬅ, ﬆ, ﬀ, Kelvin all FOUND; dotless i, l-caron missing)
echo x > "$P/fold/.ssh_probe"; echo y > "$P/fold/Makefile"; echo z > "$P/fold/st_probe"; echo z > "$P/fold/ff_probe"
/usr/bin/python3 -I -c '
import os,sys
P=sys.argv[1]
for n in [".ſsh_probe","MAKEFILE","Makefıle","ﬅ_probe","ﬆ_probe","ﬀ_probe"]:
    print(repr(n), os.path.exists(os.path.join(P,n)))
' "$P/fold"
# 2. zsh: the "constant" echo "$?" evaluates subscripts (math, with assignment) and modifiers
/bin/zsh -f -c 'x=1; echo "$?[x=5]"; echo "x=$x"'          # prints x=5
/bin/zsh -f -c 'echo "$?[PATH=7]"; echo "PATH now: $PATH"'  # prints PATH now: 7
/bin/zsh -f -c 'echo "$?[1]" "$?:h" "$??"'                   # prints: 0 . 0?
# 3. macOS tail: obsolete '+Nf' operand follows forever (killed by alarm, rc=142)
/usr/bin/perl -e 'alarm 2; exec @ARGV' /usr/bin/tail +1f "$P/t/a.txt"; echo "rc=$?"
# 4. macOS cat/head/wc do not permute: an option after the first operand is a FILE
/bin/cat "$P/t/a.txt" -n; /usr/bin/head "$P/t/a.txt" -n 1; /usr/bin/wc "$P/t/a.txt" -l
