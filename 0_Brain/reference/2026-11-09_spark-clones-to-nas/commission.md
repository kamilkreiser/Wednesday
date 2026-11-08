# Commission: move Wednesday's regenerable Spark work clones from DevMASTER to the NAS (Kam's rulings 2026-11-09). Wednesday's own tree only.

## Authority (Kam, live board, verbatim)
- 07:51:45 card wed-disk-16gib-prune-freed-nothing-1109 = a: "Remove the regenerable clones my own agents made". The card's option text: list every unmarked folder under spark/cache/work with its size and creator, remove only the regenerable work clones made by Wednesday's own operators and drafters (never records, run dirs, quarantines or the cache clone), report df before and after.
- 07:52:10 card wed-disk-clone-delete-blocked-by-hook-1108 note: "use the nas". Wednesday's reading (receipted on the panel bf-b4ec20c65b0e07af): COPY to the NAS, verify, then free DevMASTER; nothing deleted outright.

## Scope
SOURCE: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/ (about 600 directories named spark_secuura_<date>_ks_..._-control_<HHMMSS> or ...-control-r...). These are the Spark operators' per-round work clones (regenerable from git).
NOT IN SCOPE, never touched: spark/cache/deps, spark/cache/src (the cache clone), any run directory (local-model/runs/), any READY_* or brief, any _quarantine_* folder, anything outside spark/cache/work/.
EXCLUDE any work directory modified in the last 2 hours (a live round may be using it), and anything whose name is not a spark_ work clone: list exclusions with the reason.
DESTINATION: /Volumes/DEV-Working/Secuura/Blockchain/WIP/2026-11-09_spark-work-clones/ (create it). ABORT if /Volumes/DEV-Working is not mounted.

## Method (copy the proven pattern)
Read /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/archive_gate_clones_20261108_nas.sh whole and write a sibling script /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/archive_spark_work_20261109_nas.sh by copy-and-change (destination, list, source dir). Per folder: count files at source; rsync -a (no --delete) to the destination; count at the destination; ONLY if the counts match, remove the SOURCE folder (that is the only removal, and only of a verified copy); on a mismatch leave the source and record it. Write a manifest (name | files at source | files at destination | result) under the destination and a copy in /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-clones-to-nas/.
1. INVENTORY first (read-only): count, total size (du -sk, bounded), the 10 largest, the exclusions. Write inventory.md here.
2. DRY RUN with the script's dry mode; then a RED-PROOF: point it at a scratch copy of 2 folders in /private/tmp with one file deleted from the destination copy, and show it keeps the source on a mismatch.
3. REAL RUN detached (nohup, log in this folder), because it is long: you need not wait for the end. Report the pid, the first folders' manifest rows, and df before.
Never cd (absolute paths); never rm anything except a source folder whose destination count matched; never touch another project's folders; no git commands; never print credentials.

## Output
/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-clones-to-nas/report.md (or your final message if the Write is refused): BLUF; inventory numbers; exclusions with reasons; red-proof result; the pid and log path of the real run; df before (and after if it finished); UNMEASURED.
