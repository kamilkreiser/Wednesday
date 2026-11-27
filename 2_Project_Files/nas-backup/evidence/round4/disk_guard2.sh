#!/bin/bash
# stops MY mutant pass if free space on / falls under 52 GiB (the brief's floor is 50). Ends by itself when the pass is over.
while pgrep -f "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/15609ed4-7998-4256-a61d-5f55d5689085/scratchpad/final_pass2.sh" > /dev/null 2>&1; do
  free_kb=$(df -k / | tail -1 | awk '{print $4}')
  echo "$(date '+%H:%M:%S') free on /: $((free_kb / 1048576)) GiB" >> "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/15609ed4-7998-4256-a61d-5f55d5689085/scratchpad/disk_guard.log"
  if [ "$free_kb" -lt $((52 * 1048576)) ]; then
    echo "$(date '+%H:%M:%S') UNDER 52 GiB: stopping the mutant pass" >> "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/15609ed4-7998-4256-a61d-5f55d5689085/scratchpad/disk_guard.log"
    pkill -TERM -f "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/15609ed4-7998-4256-a61d-5f55d5689085/scratchpad/final_pass2.sh"; pkill -TERM -f "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/15609ed4-7998-4256-a61d-5f55d5689085/scratchpad/final2/WEDNESDAY/2_Project_Files/nas-backup/tests/mutants.sh"; pkill -TERM -f "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/15609ed4-7998-4256-a61d-5f55d5689085/scratchpad/mfinal2/"
    : > "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/15609ed4-7998-4256-a61d-5f55d5689085/scratchpad/STOPPED_BY_DISK_GUARD"; exit 3
  fi
  /opt/homebrew/bin/python3 -c 'import time; time.sleep(45)'
done
echo "$(date '+%H:%M:%S') the pass is over; guard ends" >> "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/15609ed4-7998-4256-a61d-5f55d5689085/scratchpad/disk_guard.log"
