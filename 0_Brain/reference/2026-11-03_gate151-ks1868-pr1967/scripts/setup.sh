W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate151-ks1868-pr1967
KEY='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw'
SSHC="ssh -i '$KEY' -o IdentitiesOnly=yes -o BatchMode=yes"
git -c core.sshCommand="$SSHC" clone --filter=blob:none git@github.com:Secuura/Distributed_Secuura.git $W/repo
echo clone rc=$?
git -C $W/repo config core.sshCommand "$SSHC"
git -C $W/repo remote set-url --push origin no_push_qa_gate
git -C $W/repo fetch origin refs/pull/1967/head:pr1967
echo fetch rc=$?
