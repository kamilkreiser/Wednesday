#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate84-ks1868-minting-1899
R=$W/repo
export GIT_SSH_COMMAND="ssh -i '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes -o BatchMode=yes"
git -C $R config core.sshCommand "$GIT_SSH_COMMAND"
git -C $R remote set-url --push origin no_push_qa_gate
git -C $R fetch -q origin refs/pull/1899/head:refs/gate/pr1899 +refs/heads/develop:refs/gate/develop > $W/logs/fetch.log 2>&1; echo fetch rc=$?
{ echo "START $(date -u +%FT%TZ)"; echo "pr $(git -C $R rev-parse refs/gate/pr1899)"; echo "develop $(git -C $R rev-parse refs/gate/develop)"; git -C $R ls-remote origin refs/pull/1899/head refs/heads/develop; } 2>&1 | tee $W/logs/head_start.log
