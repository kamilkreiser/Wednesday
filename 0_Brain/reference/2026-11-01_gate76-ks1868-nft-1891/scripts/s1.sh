W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate76-ks1868-nft-1891
R=$W/repo
git -C $R rev-parse refs/gate/pr1891 refs/gate/develop > $W/logs/head_start.log 2>&1; cat $W/logs/head_start.log
git -C $R checkout -q refs/gate/pr1891 > $W/logs/checkout.log 2>&1; echo checkout rc $?
git -C $R diff --stat refs/gate/develop refs/gate/pr1891
git -C $R diff refs/gate/develop refs/gate/pr1891 -- services/nft-certificate/src docs
