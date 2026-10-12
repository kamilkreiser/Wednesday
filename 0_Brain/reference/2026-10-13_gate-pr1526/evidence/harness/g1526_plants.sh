#!/bin/bash
# Plants against the gate's OWN scratch clone (never the project checkout). Each plant asserts its marker landed (charter: read why a green is green).
G=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad
W=$G/w
D=$W/Blockchain/Dev
KEEP=$G/g1526keep; mkdir -p $KEEP
cp $D/docker-compose.yml $KEEP/docker-compose.yml.orig
g() { git -C /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad/w "$@"; }
sh_guard() { bash $D/scripts/check-stack-safety.sh >$G/g1526r/p.sh.out 2>&1; echo "  stack-safety.sh rc=$? :: $(grep -E '^::error|^OK' $G/g1526r/p.sh.out | head -2 | cut -c1-260)"; }
mjs_guard() { node $D/scripts/check-compose-stack-safety.mjs >$G/g1526r/p.mjs.out 2>&1; echo "  compose-stack-safety.mjs rc=$? :: $(grep -E '^::error|^OK' $G/g1526r/p.mjs.out | head -2 | cut -c1-260)"; }
restore() { cp $KEEP/docker-compose.yml.orig $D/docker-compose.yml; }

echo "### CONTROL: unplanted"; sh_guard; mjs_guard

echo "### P1 literal slot-1 host URL INSIDE the mjs scope (an env value of a rendered service)"
sed -i '' 's|^      - FRONTEND_URL=\${FRONTEND_URL:-http://localhost:\${GATEWAY_PORT:-6882}}|&\n      - QA_PLANT_URL=http://localhost:6882|' $D/docker-compose.yml
grep -c "QA_PLANT_URL=http://localhost:6882" $D/docker-compose.yml | sed 's/^/  marker landed (count)=/'
mjs_guard; restore

echo "### P2a literal slot-1 port OUTSIDE the scope: a healthcheck/command string, not an env value"
sed -i '' 's|^      - FRONTEND_URL=\${FRONTEND_URL:-http://localhost:\${GATEWAY_PORT:-6882}}|&\n      - QA_PLANT_NOTE=see_http_localhost:6882_in_docs|' $D/docker-compose.yml
grep -c "QA_PLANT_NOTE" $D/docker-compose.yml | sed 's/^/  marker landed (count)=/'
mjs_guard; restore

echo "### P2b slot-1 literal for a slot-offset port the regex list omits (cardano mock 6090 is offset by stack_env.sh)"
sed -i '' 's|^      - FRONTEND_URL=\${FRONTEND_URL:-http://localhost:\${GATEWAY_PORT:-6882}}|&\n      - QA_PLANT_URL=http://localhost:6090|' $D/docker-compose.yml
grep -c "QA_PLANT_URL=http://localhost:6090" $D/docker-compose.yml | sed 's/^/  marker landed (count)=/'
mjs_guard; restore

echo "### P2c a literal slot-1 port in a launcher script (outside both guards' scope)"
printf '#!/bin/bash\ncurl -s http://localhost:6882/health\n' > $D/scripts/qa-plant-literal.sh
g add -N Blockchain/Dev/scripts/qa-plant-literal.sh
sh_guard; mjs_guard
g rm -q --cached Blockchain/Dev/scripts/qa-plant-literal.sh 2>/dev/null; mv $D/scripts/qa-plant-literal.sh $G/g1526keep/

echo "### P3a NEW launcher running the platform compose WITHOUT sourcing stack_env.sh - UNTRACKED"
printf '#!/bin/bash\ndocker compose up -d postgres\n' > $D/scripts/qa-plant-launcher.sh
sh_guard
echo "### P3b same file, TRACKED (git add -N)"
g add -N Blockchain/Dev/scripts/qa-plant-launcher.sh
g ls-files Blockchain/Dev/scripts/qa-plant-launcher.sh | sed 's/^/  tracked: /'
sh_guard
echo "### P3c launcher variants (each tracked) - which does the census see?"
i=0
for body in 'docker compose \\\n  up -d postgres' 'DC="docker compose"\n$DC up -d postgres' 'docker-compose up -d postgres' 'exec docker compose -f x.yml up' 'docker compose --project-name foo up -d' 'compose_cmd="docker compose"; ${compose_cmd} up -d' 'docker compose up' 'sudo docker compose down'; do
  i=$((i+1)); f=$D/scripts/qa-plant-v$i.sh
  printf "#!/bin/bash\n$body\n" > $f
  g add -N Blockchain/Dev/scripts/qa-plant-v$i.sh
  bash $D/scripts/check-stack-safety.sh >$G/g1526r/p.sh.out 2>&1; rc=$?
  echo "  v$i [$(printf "$body" | tr '\n' '~')] -> rc=$rc $(grep -c "qa-plant-v$i" $G/g1526r/p.sh.out) mentions"
  g rm -q --cached Blockchain/Dev/scripts/qa-plant-v$i.sh; mv $f $G/g1526keep/
done
echo "### P3d launcher WITH the source line, but not added to PLATFORM_LAUNCHERS (should it red?)"
printf '#!/bin/bash\nsource "$(dirname "$0")/stack_env.sh"\ndocker compose up -d postgres\n' > $D/scripts/qa-plant-sourced.sh
g add -N Blockchain/Dev/scripts/qa-plant-sourced.sh
sh_guard
g rm -q --cached Blockchain/Dev/scripts/qa-plant-sourced.sh; mv $D/scripts/qa-plant-sourced.sh $G/g1526keep/
g rm -q --cached Blockchain/Dev/scripts/qa-plant-launcher.sh; mv $D/scripts/qa-plant-launcher.sh $G/g1526keep/
echo "### CONTROL after cleanup"; sh_guard; mjs_guard; g status --short
