#!/bin/bash
# operator 26 screen: plant violations per guard in a fresh scratch tree with PATH stubs; report rc + output.
# usage: screen26.sh <clone root> <scratch base>
CL="$1"; BASE="$2"; SRC="$CL/Blockchain/Dev/scripts"; N=0
run() { echo "=== $1"; shift; ( "$@" ) 2>&1 | sed 's/^/    /'; echo "    rc=${PIPESTATUS[0]}"; }

# ---------- akto-container-names ----------
akto() { # akto <label> <relpath> <content>   (corpus complete + one planted file)
  N=$((N+1)); T="$BASE/akto$N"; mkdir -p "$T/src" "$T/bin" "$T/scripts"
  printf 'export const a = 1;\n' > "$T/src/ok.ts"; printf 'export const b = 1;\n' > "$T/bin/ok.ts"; printf '#!/bin/bash\necho hi\n' > "$T/scripts/ok.sh"
  if [ -n "$2" ]; then printf '%s\n' "$3" > "$T/$2"; fi
  run "akto: $1" bash "$SRC/check-akto-container-names.sh" "$T"
}
akto "clean control" "" ""
akto "literal docker exec akto-mongo (ts)" src/a.ts 'run("docker exec akto-mongo mongosh")'
akto "docker exec -it akto-mongo (flags between)" scripts/z.sh 'docker exec -it akto-mongo mongosh'
akto "docker exec -i akto-mongo (flag, quoted)" scripts/z.sh 'docker exec -i "akto-mongo" mongosh'
akto "docker logs --tail 5 akto-testing" scripts/z.sh 'docker logs --tail 5 akto-testing'
akto "docker compose exec akto-mongo" scripts/z.sh 'docker compose exec akto-mongo mongosh'
akto "docker exec akto-mongo (plain, sh)" scripts/z.sh 'docker exec akto-mongo mongosh'
akto "_CONTAINER const" src/a.ts "const MONGO_CONTAINER = 'akto-mongo';"
akto "defaulted shell var" scripts/z.sh 'M=${AKTO_MONGO_CONTAINER:-akto-mongo}'
akto "defaulted shell var with digit in name" scripts/z.sh 'M=${AKTO_MONGO2:-akto-mongo}'
akto "TS ?? default" src/a.ts "const m = env.X ?? 'akto-mongo';"
akto "TS || default" src/a.ts "const m = env.X || \"akto-testing\";"
akto "TS template default" src/a.ts 'const m = env.X || `akto-testing`;'
akto "hit in .mjs under scripts" scripts/z.mjs "const m = env.X ?? 'akto-mongo';"
akto "hit in .js under src (not in --include)" src/a.js "const m = env.X ?? 'akto-mongo';"
akto "derived form (the fix) control" scripts/z.sh 'M=${AKTO_PREFIX:-akto}-mongo'
akto "comment hit skipped control" scripts/z.sh '# docker exec akto-mongo mongosh'
akto "indented // comment skipped" src/a.ts '   // docker exec akto-mongo'
akto "hit in a file with a comment-looking code prefix" src/a.ts 'x(); // docker exec akto-mongo'
akto "hit in nested src/sub/a.ts" src/sub/a.ts 'docker exec akto-mongo x'
# nested dir creation
N=$((N+1)); T="$BASE/akto$N"; mkdir -p "$T/src/sub" "$T/bin" "$T/scripts"; printf 'x\n' > "$T/src/ok.ts"; printf 'x\n' > "$T/bin/ok.ts"; printf 'x\n' > "$T/scripts/ok.sh"; printf 'docker exec akto-mongo x\n' > "$T/src/sub/a.ts"
run "akto: nested dir hit (real)" bash "$SRC/check-akto-container-names.sh" "$T"
N=$((N+1)); T="$BASE/akto$N"; mkdir -p "$T/src" "$T/bin"; printf 'x\n' > "$T/src/ok.ts"; printf 'x\n' > "$T/bin/ok.ts"
run "akto: scripts/ missing (expect rc 2)" bash "$SRC/check-akto-container-names.sh" "$T"
run "akto: no such dir (expect rc 2)" bash "$SRC/check-akto-container-names.sh" "$BASE/nope"
# real akto package in the clone
run "akto: real systemTest/akto (expect rc 0)" bash "$SRC/check-akto-container-names.sh" "$CL/systemTest/akto"

# ---------- app-db-password-default ----------
STUB="$BASE/stub"; mkdir -p "$STUB"
cat > "$STUB/docker" <<'EOF'
#!/bin/bash
# stub: `docker compose version` rc 0; `docker compose ... config` rc from $STUB_CONFIG_RC_UNSET / _SET by whether APP_DB_PASSWORD is set
if [ "$1" = compose ] && [ "$2" = version ]; then echo "Docker Compose version stub"; exit 0; fi
if [ "$1" = compose ]; then
  if [ -n "${APP_DB_PASSWORD:-}" ]; then exit "${STUB_RC_SET:-0}"; else exit "${STUB_RC_UNSET:-0}"; fi
fi
exit 0
EOF
chmod +x "$STUB/docker"
appdb() { # appdb <label> <env assignments...> -- <compose content> [extra files via global XF]
  local label="$1"; shift
  N=$((N+1)); T="$BASE/appdb$N"; mkdir -p "$T/Blockchain/Dev/scripts" "$T/Blockchain/Dev/docker"
  cp "$SRC/check-app-db-password-default.sh" "$T/Blockchain/Dev/scripts/"
  printf '%s\n' "$CONTENT" > "$T/Blockchain/Dev/docker-compose.yml"
  [ -n "${EXTRA_FILE:-}" ] && printf '%s\n' "$EXTRA_CONTENT" > "$T/Blockchain/Dev/$EXTRA_FILE"
  git -C "$T" init -q; git -C "$T" add -A; git -C "$T" -c user.email=a@b -c user.name=n commit -q -m x
  run "app-db: $label" env PATH="$STUB:$PATH" "$@" bash "$T/Blockchain/Dev/scripts/check-app-db-password-default.sh"
}
EXTRA_FILE=""; EXTRA_CONTENT=""
CONTENT='  PW: ${APP_DB_PASSWORD:-hunter2}'
appdb "HELD state (literal fallback only) expect rc 0" STUB_RC_UNSET=0
CONTENT='  PW: ${APP_DB_PASSWORD:-hunter2}
  PX: ${APP_DB_PASSWORD:?required}'
appdb "half applied expect rc 1" STUB_RC_UNSET=0
CONTENT='  PX: ${APP_DB_PASSWORD:?required}'
appdb "switched, config fails unset and ok set expect rc 0" STUB_RC_UNSET=1 STUB_RC_SET=0
appdb "switched, config resolves unset expect rc 1" STUB_RC_UNSET=0 STUB_RC_SET=0
appdb "switched, config fails even set expect rc 1" STUB_RC_UNSET=1 STUB_RC_SET=1
CONTENT='  PW: ${APP_DB_PASSWORD:-hunter2}'
appdb "HELD but config fails unset expect rc 1" STUB_RC_UNSET=1
CONTENT='  nothing here'
appdb "neither form expect rc 1" STUB_RC_UNSET=0
CONTENT='  PW: ${APP_DB_PASSWORD:=hunter2}'
appdb "':=' assign-default literal (expect rc 1 if seen as neither; shape check)" STUB_RC_UNSET=0
CONTENT='  PW: ${APP_DB_PASSWORD-hunter2}'
appdb "'-' (no colon) literal default (shape check)" STUB_RC_UNSET=0
CONTENT='  PW: ${APP_DB_PASSWORD:-"hunter2"}
  PX: ${APP_DB_PASSWORD:-${DB_PASS}}'
appdb "quoted literal + var-ref fallback (HELD, 1 site)" STUB_RC_UNSET=0
CONTENT='  PW: ${APP_DB_PASSWORD:-}
  PX: ${APP_DB_PASSWORD:?required}'
appdb "empty fallback + required (switched, not half) expect rc 0 w/ stub" STUB_RC_UNSET=1 STUB_RC_SET=0
CONTENT='  PX: ${APP_DB_PASSWORD:?required}'
EXTRA_FILE="x.sh"; EXTRA_CONTENT='echo ${APP_DB_PASSWORD:-leak}'
appdb "switched + literal in a .sh (half applied) expect rc 1" STUB_RC_UNSET=1 STUB_RC_SET=0
EXTRA_FILE="notes (a).txt"; EXTRA_CONTENT='APP_DB_PASSWORD:-x'
CONTENT='  PX: ${APP_DB_PASSWORD:?required}'
appdb "literal in a file whose name has spaces and parens (half applied?) expect rc 1" STUB_RC_UNSET=1 STUB_RC_SET=0
EXTRA_FILE="a:b.txt"; EXTRA_CONTENT='APP_DB_PASSWORD:-x'
appdb "literal in a file named with a colon (half applied?) expect rc 1" STUB_RC_UNSET=1 STUB_RC_SET=0
EXTRA_FILE=""
# no docker at all
N=$((N+1)); T="$BASE/appdb$N"; mkdir -p "$T/Blockchain/Dev/scripts"; cp "$SRC/check-app-db-password-default.sh" "$T/Blockchain/Dev/scripts/"; printf '  PW: ${APP_DB_PASSWORD:-hunter2}\n' > "$T/Blockchain/Dev/docker-compose.yml"; git -C "$T" init -q; git -C "$T" add -A; git -C "$T" -c user.email=a@b -c user.name=n commit -q -m x
mkdir -p "$BASE/nodocker"; for b in git env dirname bash sed awk grep cat; do ln -sf "$(command -v $b)" "$BASE/nodocker/$b" 2>/dev/null; done
run "app-db: no docker on PATH (expect SKIP rc 0)" env PATH="$BASE/nodocker" /bin/bash "$T/Blockchain/Dev/scripts/check-app-db-password-default.sh"
# the real tree
run "app-db: real tree, docker stub, rc_unset=0" env PATH="$STUB:$PATH" bash "$CL/Blockchain/Dev/scripts/check-app-db-password-default.sh"
