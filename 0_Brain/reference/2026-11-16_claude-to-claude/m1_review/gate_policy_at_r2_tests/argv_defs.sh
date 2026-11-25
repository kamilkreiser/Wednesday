# QA-POLICY-AT-R2 argv printer (the check's own; does NOT shadow echo/printf/builtin; never runs the real program).
# Each client is a shell function that prints its argv and, per argument, what file a real run would reach.
__qa_show() {
  local prog="$1"; shift
  local out="ARGV $prog" a p
  for a in "$@"; do out="$out [$a]"; done
  builtin printf '%s\n' "$out"
  for a in "$@"; do
    p="$a"
    case "$a" in @-) builtin printf '  %s\n' "STDIN-ARG $a: reads standard input"; continue;; @*) p="${a#@}";; esac
    case "$a" in *=@*) p="${a#*=@}"; p="${p%%;*}";; esac
    if [ -f "$p" ]; then builtin printf '  %s\n' "FILE $a -> $p (exists)";
    elif [ -d "$p" ]; then builtin printf '  %s\n' "DIR $a -> $p (holds: $(cd "$p" && ls -A | tr '\n' ' '))";
    elif [ "$p" != "$a" ]; then builtin printf '  %s\n' "NOFILE $a -> $p (no such file)"; fi
  done
  case " $* " in *" @- "*) local s; s=$(command cat); builtin printf '  %s\n' "STDIN carried: $(builtin printf '%s' "$s" | tr '\n' '|')";; esac
}
curl() { __qa_show curl "$@"; }
cat() { __qa_show cat "$@" >&2; command cat "$@"; }  # argv to stderr; then the real content (fake files), so a pipe carries what a real cat sends
grep() { __qa_show grep "$@"; }
rm() { __qa_show rm "$@"; }
sed() { __qa_show sed "$@"; }
tar() { __qa_show tar "$@"; }
http() { __qa_show http "$@"; }
wget() { __qa_show wget "$@"; }
