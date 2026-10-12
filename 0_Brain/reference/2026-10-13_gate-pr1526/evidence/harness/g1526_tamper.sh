#!/bin/bash
G=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad
D=$G/w/Blockchain/Dev
T=$D/scripts/__tests__
KEEP=$G/g1526keep/orig; mkdir -p $KEEP
for f in docker-compose.yml scripts/preflight/preflight.sh scripts/start-local.sh; do mkdir -p $KEEP/$(dirname $f); cp $D/$f $KEEP/$f; done
restore() { for f in docker-compose.yml scripts/preflight/preflight.sh scripts/start-local.sh; do cp $KEEP/$f $D/$f; done; }
pyrep() { # file old new : assert anchor present, replace
  python3 -I - "$1" "$2" "$3" <<'EOF'
import sys
p,old,new=sys.argv[1:4]
s=open(p).read()
assert old in s, "ANCHOR ABSENT: "+old
open(p,'w').write(s.replace(old,new,1))
EOF
}
detect() {
  local n
  node $D/scripts/check-compose-stack-safety.mjs >$G/g1526r/t.out 2>&1; echo "    mjs                      rc=$? $(grep -m1 -E '^::error|^OK' $G/g1526r/t.out | cut -c1-170)"
  bash $D/scripts/check-stack-safety.sh >$G/g1526r/t.out 2>&1; echo "    check-stack-safety.sh    rc=$? $(grep -m1 -E '^::error|^OK' $G/g1526r/t.out | cut -c1-170)"
  for n in preflight_gateway_slot ks1355_slot_blind_launchers ks1417_env_example_no_dead_gateway_port; do
    bash $T/$n.test.sh >$G/g1526r/t.out 2>&1; echo "    $n rc=$? $(tail -1 $G/g1526r/t.out) first: $(grep -m1 '^FAIL' $G/g1526r/t.out | cut -c1-110)"
  done
}
tamper() { # label file old new
  echo "### TAMPER $1"
  pyrep "$D/$2" "$3" "$4" || { echo "  ANCHOR FAILED - no tamper applied"; restore; return; }
  if diff -q $KEEP/$2 $D/$2 >/dev/null; then echo "  !! tamper did NOT land"; else echo "  tamper landed (diff lines: $(diff $KEEP/$2 $D/$2 | grep -c '^[<>]'))"; fi
  detect; restore; diff -q $KEEP/$2 $D/$2 >/dev/null && echo "  restored clean"
}
echo "### CONTROL untampered"; detect
tamper "T1 revert auth FRONTEND_URL to slot-1 literal (compose :767)" docker-compose.yml 'FRONTEND_URL=${FRONTEND_URL:-http://localhost:${GATEWAY_PORT:-6882}}' 'FRONTEND_URL=${FRONTEND_URL:-http://localhost:6882}'
tamper "T2 revert api-gateway CORS_ORIGINS (compose :503) to literals" docker-compose.yml 'http://localhost:6103,http://localhost:${GATEWAY_PORT:-6882},http://localhost:${WEBSITE_PORT:-6881}}' 'http://localhost:6103,http://localhost:6882,http://localhost:6881}'
tamper "T3 revert demo-service CORS_ORIGINS (compose :2185) website half only" docker-compose.yml 'http://localhost:${GATEWAY_PORT:-6882},http://localhost:${WEBSITE_PORT:-6881}}
      - DEMO_MODE' 'http://localhost:${GATEWAY_PORT:-6882},http://localhost:6881}
      - DEMO_MODE'
tamper "T4 revert preflight derivation to the old one-liner (drop slot branch)" scripts/preflight/preflight.sh 'elif [ -n "$_pf_slot_named" ]; then' 'elif false; then'
tamper "T5 preflight: swallow a malformed slot (fall back to :6882 instead of refusing)" scripts/preflight/preflight.sh '        exit 2
    fi
    GATEWAY="http://localhost:${_pf_gw_port}"' '        _pf_gw_port=6882
    fi
    GATEWAY="http://localhost:${_pf_gw_port}"'
tamper "T6 start-local: drop the stack_env source" scripts/start-local.sh 'source "$_sl_dev_dir/scripts/stack_env.sh"' ': # dropped'
echo "### TAMPER T7 start-local: .env sourced AFTER stack_env (stale .env literal beats the slot)"
pyrep "$D/scripts/start-local.sh" 'source .env
' ': # moved
' && pyrep "$D/scripts/start-local.sh" 'PROJECT_ROOT="$_sl_dev_dir"

# Functions' 'PROJECT_ROOT="$_sl_dev_dir"
source .env

# Functions'
diff -q $KEEP/scripts/start-local.sh $D/scripts/start-local.sh >/dev/null && echo "  !! did NOT land" || echo "  tamper landed"
detect; restore
tamper "T8 start-local: one v1 docker-compose token reintroduced" scripts/start-local.sh '    docker compose ps
' '    docker-compose ps
'
echo "### CONTROL after all"; detect; git -C /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad/w status --short
