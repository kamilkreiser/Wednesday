#!/bin/bash
# c5_spec_gate54a.sh — gate54a C5 OPENAPI / SPEC. bash 3.2 / zsh safe; no rc read through a pipe.
#   static [REPO]          READ ONLY (git ls-tree / diff / log / rev-parse / show) on the shared checkout or your clone:
#                          SP1 docs/openapi/secuura-api.yaml blob at base == at head == kit spec_yaml_blob;
#                          SP2 0 paths matching kit openapi_ts_rx (*.openapi.ts) and 0 yaml in `git diff --name-only base head`;
#                              MUST-HIT CONTROL: the same two filters over the LAST develop commit that touched the yaml (found by
#                              `git log -1 -- <yaml>` from base) list >= 1 path, and the tree at head carries >= 1 *.openapi.ts;
#                          SP3 the /api/users/lookup operation in the yaml at head declares at least 200 400 401 403 404 (the statuses the
#                              handler can produce; the handler body is byte-equal base == head per C3 S4, so the shape is unchanged).
#   run WS OUT             in YOUR installed head worktree (c2 install first): `npm run check:openapi` at Blockchain/Dev, rc 0 wanted;
#                          CONTROL that can fail: a one-line plant appended to the yaml in WS -> check:openapi MUST go non-zero; the yaml
#                          is then restored from the head blob, sha256 proven equal, `git status --porcelain` empty.
# REFUSES (rc 2, before writing) a WS inside /Volumes/DevMASTER/!CODING/ or whose HEAD is not the pinned head; an OUT inside !CODING/
# other than the QA reports root. Env G54A_HEAD (default kit expected_head). rc 0 PASS / 1 FAIL / 2 refusal / 3 tool step failed.
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))[sys.argv[2]]; print(v if isinstance(v,str) else json.dumps(v))' "$GS/kit.json" "$1"; }
BASE="$(KJ base)"; HEADSHA="${G54A_HEAD:-$(KJ expected_head)}"; Y="$(KJ spec_yaml)"; YB="$(KJ spec_yaml_blob)"; ORX="$(KJ openapi_ts_rx)"
usage() { sed -n '2,19p' "$0" | sed 's/^# \{0,1\}//'; }
sha() { shasum -a 256 "$1" | awk '{print $1}'; }
CMD="${1:-}"
case "$CMD" in
  ''|-h|--help) usage; [ -n "$CMD" ] && exit 0; exit 2;;
  static)
    REPO="${2:-$(KJ checkout)}"; T="$(date -u +%Y-%m-%dT%H:%M:%SZ)"; F=0
    echo "C5 STATIC $T | repo $REPO | base ${BASE:0:12} | head ${HEADSHA:0:12}"
    b="$(git -C "$REPO" rev-parse "$BASE:$Y" 2> /dev/null)"; h="$(git -C "$REPO" rev-parse "$HEADSHA:$Y" 2> /dev/null)"
    git -C "$REPO" cat-file -e "$HEADSHA:$Y.g54a-absent-control" 2> /dev/null; crc=$?
    if [ "$b" = "$YB" ] && [ "$h" = "$YB" ] && [ "$crc" != 0 ]; then echo "PASS SP1 yaml blob base $b == head $h == kit $YB (absent-path control rc $crc: rev-parse cannot echo us a fake)"; else echo "FAIL SP1 yaml blob base '$b' head '$h' kit $YB (control rc $crc)"; F=1; fi
    git -C "$REPO" diff --name-only "$BASE" "$HEADSHA" > "$GS/.c5_names_head.tmp" 2> /dev/null; rc1=$?
    n_ts="$(grep -c -E "$ORX" "$GS/.c5_names_head.tmp")"; n_y="$(grep -c -x -F "$Y" "$GS/.c5_names_head.tmp")"
    LT="$(git -C "$REPO" log -1 --format=%H "$BASE" -- "$Y")"
    git -C "$REPO" diff --name-only "$LT~1" "$LT" > "$GS/.c5_names_ctl.tmp" 2> /dev/null; rc2=$?
    c_ts="$(grep -c -E "$ORX" "$GS/.c5_names_ctl.tmp")"; c_y="$(grep -c -x -F "$Y" "$GS/.c5_names_ctl.tmp")"
    git -C "$REPO" ls-tree -r --name-only "$HEADSHA" -- Blockchain/Dev/services > "$GS/.c5_tree.tmp" 2> /dev/null
    t_ts="$(grep -c -E "$ORX" "$GS/.c5_tree.tmp")"
    if [ "$rc1" = 0 ] && [ "$n_ts" = 0 ] && [ "$n_y" = 0 ] && [ "$rc2" = 0 ] && [ "$c_y" -ge 1 ] && [ "$t_ts" -ge 1 ]; then
      echo "PASS SP2 base..head: *.openapi.ts $n_ts, yaml $n_y | MUST-HIT: last yaml commit ${LT:0:12} lists yaml $c_y / *.openapi.ts $c_ts; head tree carries $t_ts *.openapi.ts"
    else echo "FAIL SP2 base..head rc $rc1: *.openapi.ts $n_ts, yaml $n_y | control ${LT:0:12} rc $rc2: yaml $c_y / ts $c_ts | tree ts $t_ts"; F=1; fi
    mv "$GS/.c5_names_head.tmp" "$GS/c5_static_names_head.txt"; mv "$GS/.c5_names_ctl.tmp" "$GS/c5_static_names_control.txt"; mv "$GS/.c5_tree.tmp" "$GS/c5_static_tree_head.txt"
    git -C "$REPO" show "$HEADSHA:$Y" > "$GS/.c5_yaml.tmp" 2> /dev/null
    # bash 3.2 mis-parses a heredoc inside $( ): the reader writes a file instead
    python3 - "$GS/.c5_yaml.tmp" > "$GS/.c5_codes.tmp" <<'PY'
import re, sys
t = open(sys.argv[1], encoding='utf-8').read().split('\n')
i = next((k for k, l in enumerate(t) if l == '  /api/users/lookup:'), None)
if i is None: print('ABSENT'); raise SystemExit
blk = []
for l in t[i + 1:]:
    if re.match(r'^  \S', l): break
    blk.append(l)
codes = sorted(set(re.findall(r'''^\s+["']?(\d{3})["']?:\s*$''', '\n'.join(blk), re.M)))
print(' '.join(codes))
PY
    ST="$(cat "$GS/.c5_codes.tmp")"; mv "$GS/.c5_codes.tmp" "$GS/c5_static_lookup_codes.txt"
    mv "$GS/.c5_yaml.tmp" "$GS/c5_static_yaml_head.yaml"
    miss=""; for c in 200 400 401 403 404; do case " $ST " in *" $c "*) ;; *) miss="$miss $c";; esac; done
    if [ -z "$miss" ]; then echo "PASS SP3 /api/users/lookup declares 200 400 401 403 404 (all statuses in the head yaml: $ST; the extra are the shared commonErrorResponses)"; else echo "FAIL SP3 /api/users/lookup statuses '$ST' lack:$miss"; F=1; fi
    [ "$F" = 0 ] && { echo "C5 STATIC PASS"; exit 0; }; echo "C5 STATIC FAIL"; exit 1;;
  run)
    WS="${2:-}"; O="${3:-}"; [ -n "$WS" ] && [ -n "$O" ] || { usage; exit 2; }
    L="$(python3 -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$O")"
    case "$L" in "/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/"*) ;; "/Volumes/DevMASTER/!CODING/"*) echo "REFUSING: OUT $L inside !CODING/ (nothing created)"; exit 2;; esac
    [ -d "$WS" ] || { echo "REFUSING: WS $WS is not a directory"; exit 2; }
    W="$(/bin/realpath "$WS")"
    case "$W" in "/Volumes/DevMASTER/!CODING/"*) echo "REFUSING: WS $W is inside /Volumes/DevMASTER/!CODING/ (READ ONLY)"; exit 2;; esac
    [ "$(git -C "$W" rev-parse HEAD 2> /dev/null)" = "$HEADSHA" ] || { echo "REFUSING: WS HEAD is not $HEADSHA"; exit 2; }
    mkdir -p "$L" || exit 2
    echo "C5 RUN $(date -u +%Y-%m-%dT%H:%M:%SZ) | WS $W @ $HEADSHA | OUT $L"
    ( cd "$W/Blockchain/Dev" && npm run check:openapi ) > "$L/c5_check_openapi.out" 2> "$L/c5_check_openapi.err"; r1=$?; echo "$r1" > "$L/c5_check_openapi.rc"
    echo "  check:openapi at head rc=$r1 (want 0)"
    s0="$(sha "$W/$Y")"; printf '\n# g54a drift-control plant\n' >> "$W/$Y"
    ( cd "$W/Blockchain/Dev" && npm run check:openapi ) > "$L/c5_check_openapi_planted.out" 2> "$L/c5_check_openapi_planted.err"; r2=$?; echo "$r2" > "$L/c5_check_openapi_planted.rc"
    echo "  CONTROL check:openapi with a planted yaml line rc=$r2 (want NON-ZERO: the drift check can fail)"
    git -C "$W" show "$HEADSHA:$Y" > "$W/$Y" 2> "$L/c5_restore.err"; s1="$(sha "$W/$Y")"
    git -C "$W" status --porcelain > "$L/c5_status_after.out" 2> "$L/c5_status_after.err"; nd="$(wc -l < "$L/c5_status_after.out" | tr -d ' ')"
    echo "  yaml restored: sha256 equal $([ "$s0" = "$s1" ] && echo yes || echo NO) | dirty paths after: $nd"
    [ "$r1" = 0 ] && [ "$r2" != 0 ] && [ "$s0" = "$s1" ] && [ "$nd" = 0 ] && { echo "C5 RUN PASS"; exit 0; }
    echo "C5 RUN FAIL"; exit 1;;
  *) usage; exit 2;;
esac
