#!/bin/bash
B=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/brain-db/braindb.sh
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-27_qa-braindb
: > "$O/14_ten_questions_rerun_raw.txt"; : > "$O/15_five_new_questions_raw.txt"
n=0
while IFS= read -r q; do [ -n "$q" ] || continue; n=$((n+1)); { echo "=================== Q$n: $q"; /bin/bash "$B" search "$q"; echo "rc=$?"; } >> "$O/14_ten_questions_rerun_raw.txt" 2>&1; done <<'QS'
what must be true before I close a pane
what do I check before telling Kam something is absent
rules about typed clock times
what provenance does each fact in a brief need before I send it
an agent has gone quiet, what proves the wake can fire before I wait on it
what do I do instead of deleting files when cleaning up
a deploy failed, can I skip it and move on
the usage gauge is high, which model do I launch a seat on
how do I word a decision card for Kam
what do I verify before merging after the QA gate returns
QS
n=0
while IFS= read -r q; do [ -n "$q" ] || continue; n=$((n+1)); { echo "=================== N$n: $q"; /bin/bash "$B" search "$q"; echo "rc=$?"; } >> "$O/15_five_new_questions_raw.txt" 2>&1; done <<'QS'
how do I brief a builder seat so it does not edit shared files
when Kam says good night what do I do first
can I tell Kam a task is done before I have checked it myself
which coordinator gets the wrap mail for a Datasec project
the drive is about to be ejected, what must be stopped or synced first
how do I bake sourdough bread at high altitude
one question at a time
never edit files inside other coding projects
QS
