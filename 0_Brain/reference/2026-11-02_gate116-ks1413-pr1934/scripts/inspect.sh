#!/bin/bash
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate116-ks1413-pr1934; R=$D/repo
git -C $R checkout -q pr1934
echo "--- demo123 / admin123 / grafana literal in the two scripts"
grep -nE 'demo123|admin123|secuura_grafana' $R/Start_Up/start-secuura.sh $R/Blockchain/Dev/scripts/start-local.sh
echo "--- password-ish lines in start-secuura.sh that print"
grep -niE '(echo|printf|log|info|warn|success|print).*(passw|secret|token|key|credential|PGPASS|_PWD|demo123)' $R/Start_Up/start-secuura.sh | head -80
echo "--- same start-local.sh"
grep -niE '(echo|printf|log|info|warn|success|print).*(passw|secret|token|key|credential|PGPASS|_PWD|demo123)' $R/Blockchain/Dev/scripts/start-local.sh | head -60
echo "--- other changed shell files: other scripts in repo that print demo123"
git -C $R grep -nE 'demo123' -- '*.sh' ':!*__tests__*' | head -40
