#!/bin/bash
# Probes of real macOS tools on scratch files only. Nothing here writes outside $P or runs a network.
P=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m2_policy_r2/probe/t
mkdir -p "$P/d/sub"
printf 'alpha\nbeta\nTOKEN=x\n' > "$P/a.txt"
printf 'TOKEN=secret\n' > "$P/d/sub/.env"
printf 'TOKEN=other\n' > "$P/b.txt"
G=/usr/bin/grep
echo "== BSD grep permutes options after operands? grep TOKEN a.txt -n"; (builtin cd "$P" && $G TOKEN a.txt -n)
echo "== BSD grep: grep TOKEN a.txt -e b.txt (does -e after operand consume b.txt as pattern?)"; (builtin cd "$P" && $G TOKEN a.txt -e b.txt; echo "rc=$?")
echo "== BSD grep -C 5 TOKEN a.txt"; (builtin cd "$P" && $G -C 5 TOKEN a.txt; echo "rc=$?")
echo "== BSD egrep -r with no operand reads stdin or cwd? (stdin = pipe)"; (builtin cd "$P/d" && echo "nothing" | /usr/bin/egrep -r TOKEN; echo "rc=$?")
echo "== BSD grep --include=sub/.env with no operand and piped stdin"; (builtin cd "$P/d" && echo nothing | $G -e TOKEN --include=sub/.env; echo "rc=$?")
echo "== BSD sort -k with -t: sort -t, -k2 b.txt"; (builtin cd "$P" && /usr/bin/sort -t, -k2 b.txt)
echo "== BSD sort accepts file operand after options from a pipe: echo z | sort -n a.txt"; (builtin cd "$P" && echo z | /usr/bin/sort -n a.txt)
echo "== BSD tail +2 a.txt (operand or offset?)"; (builtin cd "$P" && /usr/bin/tail +2 a.txt; echo "rc=$?")
echo "== BSD head -c 3 a.txt"; (builtin cd "$P" && /usr/bin/head -c 3 a.txt; echo; echo "rc=$?")
echo "== BSD ls -R follows symlinked dir operand? (ln -s d L)"; ln -sfn "$P/d" "$P/L"; (builtin cd "$P" && /bin/ls -R L | head -5)
echo "== BSD du -d 0 L (symlink operand)"; (builtin cd "$P" && /usr/bin/du -d 0 L)
echo "== BSD cut -d , -f 1 b.txt"; (builtin cd "$P" && /usr/bin/cut -d , -f 1 b.txt)
echo "== BSD wc -m a.txt"; (builtin cd "$P" && /usr/bin/wc -m a.txt)
echo "== BSD file -b a.txt"; (builtin cd "$P" && /usr/bin/file -b a.txt)
echo "== BSD stat a.txt"; (builtin cd "$P" && /usr/bin/stat a.txt >/dev/null; echo "rc=$?")
echo "== BSD uniq -c with operand refused by recogniser; BSD tr -d a"; (echo abc | /usr/bin/tr -d a)
echo "== zsh: echo \"\$?[1]\" and \"\$?:h\""; /bin/zsh -f -c 'echo "$?[1]" "$?:h" "$??"'
echo "== zsh: echo with -e escapes"; /bin/zsh -f -c "echo -e 'a\\x41'"
echo "== BSD find: find . -name x -newer a.txt (roots after expression?) find -name x ."; (builtin cd "$P" && /usr/bin/find -name x . ; echo "rc=$?")
echo "== BSD grep -h -s -q -H -I -x -w -o -c -l -v -i -n -E -F all accepted:"; (builtin cd "$P" && $G -hsHIxwoclvinEF TOKEN a.txt; echo "rc=$?")
