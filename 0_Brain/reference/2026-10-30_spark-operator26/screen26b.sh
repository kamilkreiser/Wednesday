#!/bin/bash
# operator 26 screen part 2: container-isolation (fixture), no-demo-mutation (scratch git repos), environment (PATH stubs)
CL="$1"; BASE="$2"; SRC="$CL/Blockchain/Dev/scripts"; mkdir -p "$BASE"
run() { echo "=== $1"; shift; ( "$@" ) 2>&1 | sed 's/^/    /'; echo "    rc=${PIPESTATUS[0]}"; }
TAB=$'\t'
inv() { printf '%s\n' "$1" | tr '|' '\t' > "$BASE/inv.tsv"; }
iso() { local label="$1"; shift; run "isolation: $label" env CONTAINER_INVENTORY_FILE="$BASE/inv.tsv" bash "$SRC/check-container-isolation.sh"; }
HEALTHY='container|ks-666|secuura-api|Up
container|ks-666|secuura-stk|Up
container|secuura_slot2|secuura-s2-api|Up
container|secuura_slot2|secuura-s2-stk|Up
volume|ks-666|v1
volume|secuura_slot2|v2
network|ks-666|n1
network|secuura_slot2|n2'
inv "$HEALTHY"; iso "healthy control"
inv "$HEALTHY
container|other|secuura-api|Up"; iso "dup container name"
inv "$HEALTHY
volume|secuura_slot2|v1"; iso "shared named volume"
inv "$HEALTHY
volume|a|<anon-ish>
volume|b|<anon-ish>"; iso "same-name volume in two projects (named)"
inv "$HEALTHY
network|secuura_slot2|n1"; iso "shared network"
inv "$HEALTHY
container|secuura_slot2|secuura-api-x|Up"; iso "slot2 wrong prefix (+count mismatch)"
inv "container|ks-666|secuura-api|Up
container|ks-666|secuura-stk|Up
container|secuura_slot2|secuura-s3-api|Up
container|secuura_slot2|secuura-s2-stk|Up
container|secuura_slot1|secuura-s2-zzz|Up"; iso "slot-1 project wearing slot marker (secuura_slot1)"
inv "container|ks-666|secuura-api|Up
container|ks-666|secuura-stk|Up
container|secuura_slot2|secuura-s2-api|Up
container|secuura_slot2|secuura-s2-stk|Up
container|akto_s3|akto-s4-mongo|Up"; iso "akto_s3 with s4 name"
inv "container|ks-666|secuura-api|Up
container|ks-666|secuura-s2-sneak|Up
container|secuura_slot2|secuura-s2-api|Up
container|secuura_slot2|secuura-s2-stk|Up"; iso "slot 1 project with -s2- name"
inv "$HEALTHY
container|ks-666|secuura-extra|Up"; iso "uneven counts"
inv "container|ks-666|secuura-api|Up
container|ks-666|secuura-stk|Up"; iso "only one stack (vacuous)"
inv "container|ks-666|secuura-api|Up
container|ks-666|secuura-stk|Up
container|ks-666|secuura-obs-prom|Up"; iso "one stack + obs (still vacuous)"
inv "$HEALTHY
container|ks-666|secuura-mig|Exited (1) 2 minutes ago
container|secuura_slot2|secuura-s2-mig|Exited (0) 2 minutes ago"; iso "exited 1 (ks-666) vs exited 0"
inv "$HEALTHY
container|ks-666|secuura-obs-x|Restarting (1) 3 seconds ago"; iso "restarting obs container"
inv "$HEALTHY
container|ks-666|secuura-obs-x|Exited (137) 3 hours ago"; iso "exited 137 obs container"
inv "$HEALTHY
container|ks-666|secuura-obs-y|Dead"; iso "Dead container"
inv "$HEALTHY
container|ks-666|secuura-zz|Created"; iso "Created never started (+count mismatch)"
inv ""; iso "empty inventory (rc 2)"
N=0
# ---- docker stub for isolation live path
S2="$BASE/dstub"; mkdir -p "$S2"; cat > "$S2/docker" <<'EOF'
#!/bin/bash
case "$1" in
 info) exit 0;;
 ps) printf 'container\tks-666\tsecuura-a\tUp\ncontainer\tks-666\tsecuura-b\tUp\ncontainer\tsecuura_slot2\tsecuura-s2-a\tUp\ncontainer\tsecuura_slot2\tsecuura-s2-b\tUp\n';;
 volume) if [ "$2" = ls ]; then echo vol1; echo vol2; else echo ks-666; fi;;
 network) if [ "$2" = ls ]; then echo bridge; echo net1; else echo ks-666; fi;;
esac
EOF
chmod +x "$S2/docker"
run "isolation: live path through docker stub" env PATH="$S2:$PATH" bash "$SRC/check-container-isolation.sh"

# ---- no-demo-mutation
mkrepo() { R="$BASE/demo$1"; mkdir -p "$R/Blockchain/Dev/scripts" "$R/Blockchain/Dev/deployment/azure/migrate"; cp "$SRC/check-no-demo-mutation.sh" "$R/Blockchain/Dev/scripts/"
  git -C "$R" init -q -b develop; echo a > "$R/README"; git -C "$R" add -A; git -C "$R" -c user.email=a@b -c user.name=n commit -q -m base; git -C "$R" update-ref refs/remotes/origin/develop HEAD; git -C "$R" checkout -q -b feat; }
cm() { git -C "$R" add -A; git -C "$R" -c user.email=a@b -c user.name=n commit -q -m "$1"; }
g() { ( cd "$R" && bash Blockchain/Dev/scripts/check-no-demo-mutation.sh "$@" ); }
mkrepo 1; echo x > "$R/Blockchain/Dev/deployment/azure/env.demo.json"; cm "edit demo"
run "demo: env.demo.json touched" g
mkrepo 2; echo x > "$R/Blockchain/Dev/deployment/azure/migrate/a.bicep"; cm "edit bicep"
run "demo: migrate/ prefix touched" g
mkrepo 3; echo x > "$R/Blockchain/Dev/deployment/azure/env.demo.json"; cm "edit demo [demo-mutation-allowed]"
run "demo: override token" g
mkrepo 4; echo x > "$R/other.txt"; cm "other"
run "demo: clean control" g
mkrepo 5; echo x > "$R/Blockchain/Dev/deployment/azure/env.demo.json"; cm "edit demo"
run "demo: explicit base arg" g origin/develop HEAD
mkrepo 6; echo x > "$R/Blockchain/Dev/deployment/azure/env.demo.json"; cm "edit demo"
run "demo: bad base (rc 2)" g origin/nope
mkrepo 7; echo x > "$R/Blockchain/Dev/deployment/azure/env.demo.json"; cm "edit demo"
run "demo: GITHUB_BASE_REF=develop" env GITHUB_BASE_REF=develop bash -c "cd '$R' && bash Blockchain/Dev/scripts/check-no-demo-mutation.sh"
mkrepo 8; mkdir -p "$R/Blockchain/Dev/deployment/azure/migrate/sub"; echo x > "$R/Blockchain/Dev/deployment/azure/migrate/sub/a.bicep"; echo y > "$R/Blockchain/Dev/deployment/azure/env.demo.json"; cm "two"
run "demo: two mutations listed" g
mkrepo 9; echo x > "$R/Blockchain/Dev/deployment/azure/env.demo.json"; cm "edit demo"; echo y > "$R/Blockchain/Dev/deployment/azure/env.demo.json"; cm "Reverse: removed [demo-mutation-allowed] token mention"
run "demo: token text only inside a LATER commit message" g
mkrepo 10; git -C "$R" mv README "x y.txt" 2>/dev/null; mkdir -p "$R/Blockchain/Dev/deployment/azure"; echo x > "$R/Blockchain/Dev/deployment/azure/migrate/with space.bicep"; cm "space name"
run "demo: filename with a space under prefix" g
mkrepo 11; git -C "$R" mv README Blockchain/Dev/deployment/azure/env.demo.json; cm "rename INTO demo path"
run "demo: rename into demo path" g
mkrepo 12; echo x > "$R/Blockchain/Dev/deployment/azure/env.demo.json"; cm "edit demo"; git -C "$R" checkout -q develop
run "demo: HEAD is base itself (no diff)" g

# ---- check-environment with PATH stubs
E="$BASE/env"; mkdir -p "$E/bin"; for b in cut tr head echo sw_vers uname; do :; done
mkbin() { local d="$E/$1"; mkdir -p "$d"; for b in cut tr head sw_vers; do ln -sf "$(command -v $b)" "$d/$b"; done; }
mkbin full; cat > "$E/full/brew" <<'EOF'
#!/bin/bash
echo "Homebrew 4.0"
EOF
cat > "$E/full/node" <<'EOF'
#!/bin/bash
echo "${STUB_NODE:-v20.1.0}"
EOF
cat > "$E/full/npm" <<'EOF'
#!/bin/bash
echo 10.0.0
EOF
cat > "$E/full/docker" <<'EOF'
#!/bin/bash
case "$1" in --version) echo "Docker version 25.0.0, build abc";; info) exit "${STUB_DOCKER_INFO_RC:-0}";; esac
EOF
chmod +x "$E/full/"*
CE="$SRC/check-environment.sh"
export HOME="$BASE/home"; mkdir -p "$HOME"
run "env: all stubbed, healthy (rc 0)" env PATH="$E/full:/bin" /bin/bash "$CE"
run "env: node v16 (rc 1)" env STUB_NODE=v16.0.0 PATH="$E/full:/bin" /bin/bash "$CE"
run "env: docker daemon down (rc 1)" env STUB_DOCKER_INFO_RC=1 PATH="$E/full:/bin" /bin/bash "$CE"
run "env: node prints garbage 'v'" env STUB_NODE=v PATH="$E/full:/bin" /bin/bash "$CE"
run "env: node v8 (single digit)" env STUB_NODE=v8.1.0 PATH="$E/full:/bin" /bin/bash "$CE"
run "env: node v100 (3-digit)" env STUB_NODE=v100.0.0 PATH="$E/full:/bin" /bin/bash "$CE"
mkbin nodocker; cp "$E/full/brew" "$E/full/node" "$E/full/npm" "$E/nodocker/"
run "env: docker missing (rc 1)" env PATH="$E/nodocker:/bin" /bin/bash "$CE"
mkbin nothing
run "env: nothing installed (expect rc 4: brew node npm docker)" env PATH="$E/nothing:/bin" /bin/bash "$CE"
