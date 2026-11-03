#!/bin/bash
# Run the PR's own suite (the head copy) against SCRIPT: Usage q0_suite.sh LABEL [SCRIPT_SRC|absent]
# A non-head script runs in a separate mirror tree under scratch/ (never in repo/). No deletes: a reused label refuses.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate174-ks915-pr1989-r2
R=$W/repo
LABEL=$1; SRC=${2:-head}
GPATH=/Users/kamilkreiser/.docker/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin
if [[ "$SRC" == head ]]; then
  T=$R/Blockchain/Dev/scripts/__tests__/restore_local_secrets.test.sh
else
  M=$W/scratch/suite-$LABEL; [[ -e $M ]] && { echo "EXISTS $M"; exit 9; }
  mkdir -p $M/Blockchain/Dev/scripts/__tests__ $M/Blockchain/Dev/services/auth/src/repositories
  cp $R/.gitignore $R/docker-compose.local.yml $M/
  cp $R/Blockchain/Dev/env.example $R/Blockchain/Dev/.env.local.example $R/Blockchain/Dev/docker-compose.yml $M/Blockchain/Dev/
  cp $R/Blockchain/Dev/services/auth/src/repositories/userRepo.ts $M/Blockchain/Dev/services/auth/src/repositories/
  cp $R/Blockchain/Dev/scripts/bootstrap-env.sh $R/Blockchain/Dev/scripts/stack_env.sh $M/Blockchain/Dev/scripts/
  cp $R/Blockchain/Dev/scripts/__tests__/restore_local_secrets.test.sh $M/Blockchain/Dev/scripts/__tests__/
  ln -s "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/node_modules" $M/Blockchain/Dev/node_modules
  if [[ "$SRC" != absent ]]; then cp "$SRC" $M/Blockchain/Dev/scripts/restore-local-secrets.sh; chmod 755 $M/Blockchain/Dev/scripts/restore-local-secrets.sh; fi
  T=$M/Blockchain/Dev/scripts/__tests__/restore_local_secrets.test.sh
fi
mkdir -p $W/tmp/$LABEL
env -i HOME=$W/home PATH=$GPATH TMPDIR=$W/tmp/$LABEL bash "$T"
echo "SUITE-RC=$?"
