#!/bin/bash
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator90; S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
lab() { case $1 in
  p2) echo DEMO-SERVICE-STATE-REDIS-LISTENER-AND-PRESENTER-MODE-CATCH-MESSAGE-COERCE;;
  p3) echo ORIGINATE-CERTIFICATIONS-INIT-REPO-CATCH-MESSAGE-COERCE;;
  p4) echo REFERRAL-MILESTONE-DB-READ-CATCHES-MESSAGE-COERCE;;
  p5) echo REFERRAL-MILESTONE-DB-WRITE-CATCHES-MESSAGE-COERCE;;
  p6) echo STAKING-STAKE-VERIFY-DB-READY-CATCH-MESSAGE-COERCE;;
  p7) echo STAKING-REWARDS-VERIFY-DB-READY-CATCH-MESSAGE-COERCE;;
  p8) echo VC-ISSUER-CREDENTIAL-REPO-READ-CATCHES-MESSAGE-COERCE;;
  p9) echo VC-ISSUER-CREDENTIAL-REPO-STORE-LIST-REVOKE-CATCHES-MESSAGE-COERCE;;
  p10) echo M365-OAUTH-STATE-DB-CATCHES-MESSAGE-COERCE;;
  p11) echo REFERRAL-SERVICE-DB-READ-CATCHES-MESSAGE-COERCE;;
  p12) echo REFERRAL-FRAUD-DETECTION-LOAD-FROM-DB-CATCH-MESSAGE-COERCE;;
  p13) echo TRANSFER-DELEGATION-SERVICE-VERIFY-AND-EXPIRE-CATCHES-MESSAGE-COERCE;;
esac; }
i=0
while [ $i -lt 240 ] && [ ! -e $O/STOP ]; do
 for k in p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13; do
  [ -e $O/hold_$k.log ] && continue
  n=$(/usr/bin/grep "o90_${k}_" $S/spark/done.md | /usr/bin/grep -v -i "CONTROL-" | /usr/bin/grep -c "PASS (7/7)")
  if [ "$n" -ge 1 ]; then bash $O/ch90.sh $k "$(lab $k)" > $O/ch_$k.out 2>&1; echo "$(date +%T) $k held-attempt" >> $O/holdloop90.log; fi
 done
 sleep 20; i=$((i+1))
done
