# QA-POLICY-WORDS argv printer (own): defines `curl` as a function that prints each argument in brackets and,
# for an argument @NAME or the value after -T, whether NAME is an existing file. Sourced by argv_qpw.py per shell.
curl() {
  local out="ARGV curl" a prev=""
  for a in "$@"; do out="$out [$a]"; done
  printf '%s\n' "$out"
  for a in "$@"; do
    case "$a" in
      @*) f="${a#@}"; if [ -f "$f" ]; then printf '  READS %s (file exists)\n' "$f"; else printf '  NOFILE %s\n' "$f"; fi;;
    esac
    if [ "$prev" = "-T" ]; then if [ -f "$a" ]; then printf '  UPLOADS %s (file exists)\n' "$a"; else printf '  NOFILE %s\n' "$a"; fi; fi
    prev="$a"
  done
}
