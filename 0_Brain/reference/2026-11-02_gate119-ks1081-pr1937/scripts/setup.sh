R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937/repo
git -C $R config core.sshCommand "ssh -i '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes -o BatchMode=yes"
git -C $R remote set-url --push origin no_push_qa_gate
git -C $R fetch origin refs/pull/1937/head:pr1937 2>&1 | tail -2
git -C $R fetch origin 8f313815f415 2>&1 | tail -2
git -C $R rev-parse pr1937 origin/develop
git -C $R diff --numstat origin/develop...pr1937
git -C $R merge-base origin/develop pr1937
