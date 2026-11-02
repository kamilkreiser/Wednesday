R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate120-ks1725-pr1938/repo
git -C $R config core.sshCommand "ssh -i '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes -o BatchMode=yes"
git -C $R remote set-url --push origin no_push_qa_gate
git -C $R fetch origin refs/pull/1938/head:pr1938 2>&1; echo fetchrc=$?
git -C $R rev-parse pr1938 origin/develop 8f313815f415
