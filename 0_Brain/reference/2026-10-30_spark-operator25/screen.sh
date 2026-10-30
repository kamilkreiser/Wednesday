#!/bin/bash
# operator 25 screen: plant a violation per sibling guard in a fresh scratch tree, run the script, report rc + output.
# usage: screen.sh <clone scripts dir> <scratch base>
SRC="$1"; BASE="$2"; N=0
fresh() { N=$((N+1)); T="$BASE/case$N"; mkdir -p "$T/scripts" "$T/services/s/src" "$T/packages" "$T/frontend" "$T/deployment" "$T/docker" "$T/connectors/c/src"; cp "$SRC"/check-*.sh "$T/scripts/"; }
run() { echo "=== $1"; shift; ( "$@" ) 2>&1 | sed 's/^/    /'; echo "    rc=${PIPESTATUS[0]}"; }

fresh; printf 'RUN x && noUnusedLocals = false\n' > "$T/services/s/Dockerfile"
run "strictness: real hit in services/" bash "$T/scripts/check-no-strictness-patches.sh"
fresh; mkdir -p "$T/services/s/node_modules/dep"; printf 'x: noUnusedLocals = false\n' > "$T/services/s/node_modules/dep/ci.yml"
run "strictness: hit ONLY in node_modules (expect rc 0 if pruned)" bash "$T/scripts/check-no-strictness-patches.sh"
fresh
run "strictness: clean control" bash "$T/scripts/check-no-strictness-patches.sh"

fresh; printf 'const a = Math.random();\n' > "$T/services/s/src/a.ts"
run "math-random: real hit" bash "$T/scripts/check-no-math-random.sh"
fresh; mkdir -p "$T/services/s/src/node_modules/d"; printf 'const a = Math.random();\n' > "$T/services/s/src/node_modules/d/a.ts"
run "math-random: hit only in node_modules" bash "$T/scripts/check-no-math-random.sh"
fresh; run "math-random: clean control" bash "$T/scripts/check-no-math-random.sh"

fresh; printf "const a = req.headers['x-user-id'];\n" > "$T/services/s/src/b.ts"
run "trust-header: real hit" bash "$T/scripts/check-no-trust-header-reads.sh"
fresh; printf "const a = req.headers['x-user-id'];\n" > "$T/services/s/src/b.ts"
run "trust-header: warn mode" env TRUST_HEADER_LINT_MODE=warn bash "$T/scripts/check-no-trust-header-reads.sh"
fresh; run "trust-header: clean control" bash "$T/scripts/check-no-trust-header-reads.sh"

fresh; printf "const p = {password: 'admin123'};\n" > "$T/services/s/src/c.ts"
run "default-passwords: real hit" bash "$T/scripts/check-no-default-passwords.sh"
fresh; run "default-passwords: clean control" bash "$T/scripts/check-no-default-passwords.sh"

fresh; printf "const h = '<a onclick=\"x()\">';\n" > "$T/connectors/c/src/a.js"
run "connector-xss: real hit" bash "$T/scripts/check-connector-xss.sh"
fresh; mkdir -p "$T/connectors/c/node_modules/d/deep"; printf "const h = '<a onclick=\"x()\">';\n" > "$T/connectors/c/node_modules/d/deep/a.js"
run "connector-xss: hit only in node_modules (expect rc 0)" bash "$T/scripts/check-connector-xss.sh"
fresh; run "connector-xss: clean control" bash "$T/scripts/check-connector-xss.sh"

fresh; printf 'FROM node\n' > "$T/services/s/Dockerfile"
run "dockerfile-non-root: no USER" bash "$T/scripts/check-dockerfile-non-root.sh"
fresh; printf 'FROM node\nUSER root\n' > "$T/services/s/Dockerfile"
run "dockerfile-non-root: USER root" bash "$T/scripts/check-dockerfile-non-root.sh"
fresh; printf 'FROM node\nUSER 0\n' > "$T/services/s/Dockerfile"
run "dockerfile-non-root: USER 0" bash "$T/scripts/check-dockerfile-non-root.sh"
fresh; printf 'FROM node\nUSER app\n' > "$T/services/s/Dockerfile"
run "dockerfile-non-root: USER app (clean control)" bash "$T/scripts/check-dockerfile-non-root.sh"
fresh; printf 'FROM node\nUSER root\n' > "$T/services/s/Dockerfile"
run "dockerfile-non-root: GNU-sed simulation absent; sed \\s probe" sh -c "printf 'USER root\n' | sed -E 's/^\\s*USER\\s+//'"

fresh; printf 'TEST_WALLET_ADDRESS=addr1qxyz\n' > "$T/test-wallet.env"
run "test-wallet: mainnet" bash "$T/scripts/check-test-wallet-testnet.sh"
fresh; printf 'TEST_WALLET_ADDRESS=addr_test1qxyz\n' > "$T/test-wallet.env"
run "test-wallet: testnet control" bash "$T/scripts/check-test-wallet-testnet.sh"
fresh; printf 'LACE_WALLET_ADDRESS="addr1qxyz"\n' > "$T/test-wallet.env"
run "test-wallet: quoted mainnet" bash "$T/scripts/check-test-wallet-testnet.sh"
fresh; printf 'export LACE_WALLET_ADDRESS=addr1qxyz\n' > "$T/test-wallet.env"
run "test-wallet: export-prefixed mainnet" bash "$T/scripts/check-test-wallet-testnet.sh"

fresh; printf 'image: foo:latest\n' > "$T/docker-compose.production.yml"
run "latest-tags: hit (4 files missing too)" bash "$T/scripts/check-no-latest-tags.sh"

fresh; printf 'rg: secuura-evil-rg\n' > "$T/deployment/x.yml"
run "env-consistency: bad rg" bash "$T/scripts/check-env-consistency.sh"
fresh; run "env-consistency: clean" bash "$T/scripts/check-env-consistency.sh"

fresh; mkdir -p "$T/services/a/src"; printf 'x\n' > "$T/services/a/src/index.ts"
run "production-guard: uncovered svc" bash "$T/scripts/check-production-guard.sh"

fresh; printf '#!/bin/bash\ntimeout 600 foo\n' > "$T/scripts/zz.sh"
run "portability: timeout hit" bash "$T/scripts/check-script-portability.sh" "$T"
fresh; mkdir -p "$T/pkg/node_modules/m/deep"; printf '#!/bin/bash\ntimeout 600 foo\n' > "$T/pkg/node_modules/m/deep/zz.sh"
run "portability: hit only in node_modules" bash "$T/scripts/check-script-portability.sh" "$T"
fresh; printf '#!/bin/bash\nsed -i s/a/b/ f\n' > "$T/scripts/zz.sh"
run "portability: sed -i hit" bash "$T/scripts/check-script-portability.sh" "$T"
fresh; printf '#!/bin/bash\nx=$(readlink -f foo)\n' > "$T/scripts/zz.sh"
run "portability: readlink -f hit" bash "$T/scripts/check-script-portability.sh" "$T"
fresh; printf '#!/bin/bash\nmapfile -t a < f\n' > "$T/scripts/zz.sh"
run "portability: mapfile hit" bash "$T/scripts/check-script-portability.sh" "$T"
