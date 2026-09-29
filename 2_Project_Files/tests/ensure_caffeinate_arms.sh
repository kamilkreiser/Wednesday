#!/bin/bash
# Arms for fleet/cockpit/ensure_caffeinate.sh (canned `ps` output + DRY: nothing is armed). PASS/FAIL each; exit 1 if any fail.
E="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../fleet/cockpit" && pwd)/ensure_caffeinate.sh"; S="$(mktemp -d)"; F=0; P=0; N=0
arm(){ # name, ps-text, laptop, expect-substring
  printf '%s\n' "$2" > "$S/ps"; out="$(ENSURE_CAFF_PS_FILE="$S/ps" ENSURE_CAFF_LAPTOP="$3" ENSURE_CAFF_DRY=1 bash "$E" 2>&1)"; rc=$?; N=$((N+1))
  case "$out" in *"$4"*) [ "$rc" = 0 ] && { echo "PASS  $1"; P=$((P+1)); } || { echo "FAIL  $1 (rc=$rc)"; F=1; } ;; *) echo "FAIL  $1"; F=1 ;; esac
  echo "      $out"; }
arm "a none running on a laptop -> would arm"                 "  101 00:10 /bin/zsh"                                        1 "WOULD ARM"
arm "b a fresh -dims -t 21600 (10 min old) -> OK"             " 7260 10:00 caffeinate -dims -t 21600"                        1 "OK — caffeinate -dims pid 7260"
arm "c today's 09-29 shape: armed 6 h, 5h50 elapsed -> arm"    " 4688 05:50:00 caffeinate -dims -t 21600"                     1 "best has only 10 min left"
arm "d short -i -t 300 assertions do not count"               "14025 00:30 caffeinate -i -t 300
14182 00:10 caffeinate -i -t 300"                                                                                            1 "WOULD ARM"
arm "e separate flags -d -i -m -s count"                      "  900 01:00 caffeinate -d -i -m -s -t 21600"                  1 "OK"
arm "f no -t = never expires -> OK"                            "  901 2-03:00:00 /usr/bin/caffeinate -dims"                   1 "OK"
arm "g not a laptop -> nothing to do"                          "  101 00:10 /bin/zsh"                                        0 "not a laptop"
arm "h a process merely NAMED like caffeinate is ignored"     "  902 00:10 /bin/bash caffeinate_helper.sh -dims -t 21600"   1 "WOULD ARM"
arm "i day-format etime (1-00:00:00) counted as elapsed"      "  903 1-00:00:00 caffeinate -dims -t 21600"                   1 "WOULD ARM"
mkdir -p "$S/_quarantine" && mv "$S/ps" "$S/_quarantine/" 2>/dev/null
echo "TOTAL: $P/$N passed"; exit $F
