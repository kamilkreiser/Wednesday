#!/bin/bash
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark
for i in $(seq 1 90); do
  a=$(grep -c "ks_1410_p5a_mcp_http_500_no_echo_register_to_documents |" $L/done.md)
  b=$(grep -c "ks_1410_p5b_mcp_http_500_no_echo_workflow_to_generate_package |" $L/done.md)
  [ "$a" -ge 1 ] && [ "$b" -ge 1 ] && break
  sleep 20
done
echo "a=$a b=$b" > /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_spark-operator23/wait23.done
