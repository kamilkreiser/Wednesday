W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate152-ks1868-pr1968
SSH="ssh -i '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes -o BatchMode=yes"
[ -e $W/repo ] && { echo repo exists; exit 1; }
git clone --filter=blob:none -c core.sshCommand="$SSH" git@github.com:Secuura/Distributed_Secuura.git $W/repo
git -C $W/repo config core.sshCommand "$SSH"
git -C $W/repo remote set-url --push origin no_push_qa_gate
git -C $W/repo fetch origin refs/pull/1968/head:pr1968 develop
git -C $W/repo ls-remote origin refs/pull/1968/head refs/heads/develop
date -u
