#!/bin/bash
q() { /opt/homebrew/opt/postgresql@15/bin/psql -X -At -h /tmp/wed-braindb-501-wednesday -d braindb "$@"; }
date
echo "total paths: $(q -c "select count(*) from brain.files")"
echo "(positive control) lower(path) like '%learnings/2026-%' : $(q -c "select count(*) from brain.files where lower(path) like '%learnings/2026-%'")"
for pat in '%4_credentials%' '%3_access_keys%' '%0_brain/dashboard%' '%0_brain/reference%' '%tuesday%' '%friday%' '%laptop_datasec%' '%daily_tuesday%' '%daily_friday%' '%pickup%' '%week%' '%conflict_on_%' '%.pre-%' '%chat_%' '%.env%' '%/.%' '%..%'; do
  echo "files.path like $pat : $(echo "select count(*) from brain.files where lower(path) like :'p'" | q -v p="$pat")   chunks distinct path: $(echo "select count(distinct path) from brain.chunks where lower(path) like :'p'" | q -v p="$pat")"
done
echo "---- the paths that DO match tuesday/friday/laptop_datasec/week/pickup (kind and path only)"
q -c "select kind, path from brain.files where lower(path) ~ 'tuesday|friday|laptop_datasec|week|pickup' order by 1,2"
echo "---- kinds and directories of every indexed path"
q -c "select kind, regexp_replace(path, '[^/]*\$', '') as dir, count(*) from brain.files group by 1,2 order by 1,2"
echo "---- tables holding a path not in brain.files (want all 0)"
q -c "select 'chunks', count(distinct path) from brain.chunks where path not in (select path from brain.files) union all select 'lessons', count(*) from brain.lessons where path not in (select path from brain.files) union all select 'ledger_rows', count(distinct path) from brain.ledger_rows where path not in (select path from brain.files) union all select 'daily_rows', count(distinct path) from brain.daily_rows where path not in (select path from brain.files)"
echo "---- rules rows whose lesson file is not an indexed lesson (want 0)"
q -c "select count(*) from brain.rules where file not in (select file from brain.lessons)"
echo "---- rules seats distribution (indexed rule lines)"
q -c "select seats, count(*) from brain.rules group by 1 order by 2 desc"
echo "---- lessons tier distribution"
q -c "select coalesce(tier,'(none)'), count(*) from brain.lessons group by 1 order by 2 desc"
echo "---- ledger/daily file names indexed"
q -c "select kind, path from brain.files where kind in ('ledger','rules','rules_index') order by 1,2"
q -c "select 'daily min/max', min(path), max(path) from brain.files where kind='daily'"
echo "---- lsof on the server pid (network sockets; want nothing)"
PID="$(sed -n 1p /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/brain-db/pgdata-wednesday/postmaster.pid | tr -d ' ')"
echo "pid $PID: $(ps -ww -p "$PID" -o command=)"
/usr/sbin/lsof -nP -a -p "$PID" -i; echo "lsof -i rc=$?"
echo "(control) unix sockets of the same pid:"; /usr/sbin/lsof -nP -a -p "$PID" -U; echo "lsof -U rc=$?"
echo "---- all children of the postmaster holding any network socket"
for c in $(pgrep -P "$PID"); do /usr/sbin/lsof -nP -a -p "$c" -i; done; echo "(children checked: $(pgrep -P "$PID" | wc -l | tr -d ' '))"
echo "---- socket dir"; stat -f '%Sp %Su %N' /tmp/wed-braindb-501-wednesday /tmp/wed-braindb-501-wednesday/.s.PGSQL.5432
echo "---- server settings"; q -c "select name, setting from pg_settings where name in ('listen_addresses','unix_socket_directories','unix_socket_permissions','data_directory','port','max_connections')"
echo "---- hba (non-comment lines)"; /usr/bin/grep -v -i -E '^\s*(#|$)' /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/brain-db/pgdata-wednesday/pg_hba.conf
