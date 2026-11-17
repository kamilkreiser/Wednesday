#!/bin/bash
# selftest for pr_checks_wait.sh (2026-11-18 --min-checks / MIXED change). Stub gh, fixtures in this folder.
S="$(mktemp -d)"   # fixtures + stub gh live in a fresh temp dir
W="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../tools" && pwd)/pr_checks_wait.sh"
mkdir -p "$S/bin"
cat > "$S/bin/gh" <<'EOF'
#!/bin/bash
case "$2" in *pulls*) echo abc;; *check-runs*) cat "$FIX";; esac
EOF
chmod +x "$S/bin/gh"
mk(){ out="$1"; shift; python3 -c '
import json,sys
runs=[]
for s in sys.argv[2:]:
    name,st,co,t=s.split(":")
    runs.append({"name":name,"status":st,"conclusion":None if co=="-" else co,"started_at":"2026-11-18T0%s:00:00Z"%t})
json.dump({"check_runs":runs},open(sys.argv[1],"w"))' "$out" "$@"; }
G=(a:completed:success:1 b:completed:success:1 c:completed:success:1 d:completed:success:1 e:completed:success:1 f:completed:success:1)
mk "$S/partial.json" a:completed:success:1
mk "$S/green.json" "${G[@]}" g:completed:success:1
mk "$S/fail.json" "${G[@]}" g:completed:failure:1
mk "$S/mixed.json" "${G[@]}" g:completed:failure:1 g:completed:success:2
mk "$S/newfail.json" "${G[@]}" g:completed:success:1 g:completed:failure:2
PASS=0; FAILN=0
t(){ name="$1"; want="$2"; fix="$3"; shift 3
  out=$(FIX="$S/$fix" PATH="$S/bin:$PATH" timeout 20 bash "$W" "$@" 2>&1); rc=$?
  if [ "$rc" = "$want" ]; then PASS=$((PASS+1)); r=PASS; else FAILN=$((FAILN+1)); r=FAIL; fi
  echo "$r $name: rc $rc (want $want) | $(printf '%s' "$out" | tail -1)"; }
t partial-nexusai 4 partial.json datasecau/Reporting_Dashboard_Au 1 abc 1 0
t green 0 green.json datasecau/Reporting_Dashboard_Au 1 abc 1 0
t fail 1 fail.json datasecau/Reporting_Dashboard_Au 1 abc 1 0
t mixed 5 mixed.json datasecau/Reporting_Dashboard_Au 1 abc 1 0
t mixed-accepted 0 mixed.json datasecau/Reporting_Dashboard_Au 1 abc 1 0 --accept-superseded
t newest-fail 1 newfail.json datasecau/Reporting_Dashboard_Au 1 abc 1 0
t unknown-repo 2 green.json datasecau/HPSM-POC 1 abc 1 0
t unknown-repo-flag 0 green.json datasecau/HPSM-POC 1 abc 1 0 --min-checks 7
t min-too-high 4 green.json datasecau/HPSM-POC 1 abc 1 0 --min-checks 8
t bad-min 2 green.json datasecau/HPSM-POC 1 abc 1 0 --min-checks x
t head-moved 3 green.json datasecau/Reporting_Dashboard_Au 1 zzz 1 0
echo "SELFTEST: $PASS pass, $FAILN fail"
