#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate173-ks915-pr1989
C="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files"; R=$W/repo
git -C $R -c core.sshCommand="$(git -C "$C" config --get core.sshCommand)" fetch -q origin refs/heads/develop:refs/gate/develop_end refs/pull/1989/head:refs/gate/pr_end || exit 1
git -C $R rev-parse refs/gate/develop_end refs/gate/pr_end
git -C $R merge-tree --write-tree refs/gate/develop_end refs/gate/pr_end; echo "merge-tree rc=$?"
echo "develop commits since de8d208a:"; git -C $R log --oneline de8d208a8426747b3a752309e08167fa0de4b2ff..refs/gate/develop_end | cat
echo "files touched since de8d208a that the script reads:"; git -C $R diff --stat de8d208a8426747b3a752309e08167fa0de4b2ff refs/gate/develop_end -- Blockchain/Dev/docker-compose.yml docker-compose.local.yml Blockchain/Dev/env.example Blockchain/Dev/.env.local.example Blockchain/Dev/scripts/bootstrap-env.sh Blockchain/Dev/docker/pgbouncer .gitignore Blockchain/Dev/.gitignore Start_Up/start-secuura.sh | cat
