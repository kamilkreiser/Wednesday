W=/private/tmp/claude-501/qdnx
for t in "-p coagent-daemon --test dnx_guard" "-p coagent-daemon --test dn_mcp" "-p coagent-mcp --bin coagent-mcp" "-p coagent-daemon --test dnx_flags"; do
  echo "=== cargo test --locked $t ($(date +%T))"; bash $W/r.sh $W/c $W/t cargo test --locked $t 2>&1 | grep -E '^test |test result|panicked|error' ; echo "exit ${PIPESTATUS[0]}"
done
