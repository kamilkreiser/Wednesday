W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate76-ks1868-nft-1891
P=$W/repo/Blockchain/Dev/services/nft-certificate/src/cardano/provider.ts
H0=$(shasum -a 256 $P | cut -d' ' -f1); echo head sha $H0
git -C $W/repo show refs/gate/develop:Blockchain/Dev/services/nft-certificate/src/cardano/provider.ts > $P
$W/scripts/vt.sh $W/logs/suite_base.log --exclude '**/ks1868-provider-fetch-protocol-params-unreadable-throw.test.ts' ; echo base rc $?
git -C $W/repo checkout -- Blockchain/Dev/services/nft-certificate/src/cardano/provider.ts
H1=$(shasum -a 256 $P | cut -d' ' -f1); echo restored sha $H1; [ "$H0" = "$H1" ] && echo RESTORE_OK
$W/scripts/vt.sh $W/logs/suite_head.log ; echo head rc $?
