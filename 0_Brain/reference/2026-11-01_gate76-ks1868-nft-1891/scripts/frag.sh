W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate76-ks1868-nft-1891
R=$W/repo
S=$R/Blockchain/Dev/scripts/docs-fragments.mjs
chk(){ nice -n 10 node $S check --root $R > $W/logs/$1.log 2>&1; echo "$1 rc=$?" | tee -a $W/logs/$1.log; }
chk frag_check
for k in cheat flow; do
  F="$R/Projects Documents/fragments/$k/KS-1868-nft-certificate-provider-unreadable-thrown-value.html"
  H0=$(shasum -a 256 "$F"|cut -d' ' -f1)
  printf '<div><span>planted\n' >> "$F"
  chk frag_planted_$k
  git -C $R checkout -- "Projects Documents/fragments/$k/KS-1868-nft-certificate-provider-unreadable-thrown-value.html"
  H1=$(shasum -a 256 "$F"|cut -d' ' -f1); echo "$k sha before $H0 after $H1"; [ "$H0" = "$H1" ] && echo "$k RESTORE_OK"
done
chk frag_check_after
