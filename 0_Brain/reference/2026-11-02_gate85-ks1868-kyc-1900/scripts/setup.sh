#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate85-ks1868-kyc-1900
R=$W/repo
export GIT_SSH_COMMAND="ssh -i '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes -o BatchMode=yes"
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate85-ks1868-kyc-1900/repo config core.sshCommand "$GIT_SSH_COMMAND"
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate85-ks1868-kyc-1900/repo remote set-url --push origin no_push_qa_gate
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate85-ks1868-kyc-1900/repo fetch -q origin refs/pull/1900/head:refs/gate/pr1900 +refs/heads/develop:refs/gate/develop > $W/logs/fetch.log 2>&1; echo fetch rc=$?
{ echo "START $(date -u +%FT%TZ)"; echo "pr $(git -C $R rev-parse refs/gate/pr1900)"; echo "develop $(git -C $R rev-parse refs/gate/develop)"; echo "pr parent $(git -C $R rev-parse refs/gate/pr1900^)"; echo "merge-base $(git -C $R merge-base refs/gate/pr1900 refs/gate/develop)"; git -C $R ls-remote origin refs/pull/1900/head refs/heads/develop; git -C $R remote -v; } 2>&1 | tee $W/logs/head_start.log
