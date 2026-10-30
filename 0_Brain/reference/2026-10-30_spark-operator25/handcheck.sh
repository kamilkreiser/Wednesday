#!/bin/bash
# tip vs fixed for the four suites. usage: handcheck.sh <clone scripts dir> <work dir>
S="$1"; W="$2"; H=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_spark-operator25
mkdir -p "$W"
for k in p1:check-dockerfile-non-root:CHECK_DOCKERFILE_NON_ROOT_SH p2:check-no-strictness-patches:CHECK_NO_STRICTNESS_PATCHES_SH p3:check-connector-xss:CHECK_CONNECTOR_XSS_SH p4:check-no-pii-store:CHECK_NO_PII_STORE_SH; do
  key=${k%%:*}; rest=${k#*:}; stem=${rest%%:*}; var=${rest#*:}
  python3 -I "$H/apply_fix.py" "$S/$stem.sh" "$W/$stem.fixed.sh" $key || exit 1
  echo "##### $key TIP"; env $var="$S/$stem.sh" bash "$H/suites/$key.sh"; echo "rc=$?"
  echo "##### $key FIXED"; env $var="$W/$stem.fixed.sh" bash "$H/suites/$key.sh"; echo "rc=$?"
done
