export GIT_OPTIONAL_LOCKS=0
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB172
SRC=/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-13_seatB-171st/clone
git clone --no-checkout --quiet "$SRC" $D/clone; echo clone rc=$?
git -C $D/clone remote set-url origin git@github.com:Secuura/Distributed_Secuura.git
git -C $D/clone remote set-url --push origin no_push_drafter_b172
git -C $D/clone config core.sshCommand "ssh -i /Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"
git -C $D/clone config gc.auto 0
