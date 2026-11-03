#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate155-ks1868-pr1972
TREE_ID=$1; O=$2; OUT=$3; : > $OUT
for arm in ctor listener initdb; do for k in ordinary revoked_proxy getter_throws symbol_message frozen_throwing_toString message_frozen_throwing_toString message_nullproto message_toPrimitive_object proxy_get_throws null undefined number string; do
  node $W/recorder/case.cjs $O $arm $k 2>/dev/null | grep '@@REC@@' | sed "s/^@@REC@@/$TREE_ID /" >> $OUT || echo "$TREE_ID NOREC $arm $k" >> $OUT
done; done
