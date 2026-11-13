export GIT_OPTIONAL_LOCKS=0
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB173
git clone --no-checkout --quiet /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB172/clone $D/clone; echo clone rc=$?
git -C $D/clone remote set-url origin git@github.com:Secuura/Distributed_Secuura.git
git -C $D/clone remote set-url --push origin no_push_drafter_b173
git -C $D/clone config core.sshCommand "ssh -i /Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"
git -C $D/clone config gc.auto 0
git -C $D/clone ls-remote origin refs/heads/develop 'refs/pull/*/head' 'refs/heads/feature/ks-1699*' 'refs/heads/feature/ks-2194*' 'refs/heads/*hono*' > $D/lsr.txt; echo lsr rc=$? lines=$(wc -l < $D/lsr.txt) at $(date +%H:%M:%S)
