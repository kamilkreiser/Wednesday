#!/bin/bash
# Gate 64 race probe: the PR's exact conditional UPDATE on real Postgres 15 (container gate64-race-pg, --network none).
# T1 holds a row lock inside a transaction, T2 (autocommit, like the route's pool.query) runs while T1 is open.
# usage: race.sh   (prints one line per scenario; rc 0 always unless psql fails)
set -u
C=gate64-race-pg
ID=c1860000-0000-4000-8000-000000000001
P() { docker exec -i "$C" psql -U postgres -v ON_ERROR_STOP=1 -At "$@"; }
P -c "DROP TABLE IF EXISTS tenants; CREATE TABLE tenants (id uuid PRIMARY KEY, status varchar(20) NOT NULL CHECK (status IN ('provisioning','active','suspended','archived')), updated_at timestamptz DEFAULT now());" || exit 5
GUARDED='UPDATE tenants SET status = $1, updated_at = now() WHERE id = $2 AND status = ANY($3::text[])'
# scenario: start_status | T1 target | T1 from-list | T2 target | T2 from-list | label
run() {
  local start="$1" t1="$2" f1="$3" t2="$4" f2="$5" label="$6"
  P -c "DELETE FROM tenants; INSERT INTO tenants (id, status) VALUES ('$ID', '$start');" || exit 5
  ( P <<SQL > /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/8eb04056-8fef-4c17-8fb3-31eec776f98e/scratchpad/gate64_t1.$$ 2>&1
BEGIN;
PREPARE s(text, uuid, text[]) AS $GUARDED;
EXECUTE s('$t1', '$ID', '{$f1}');
SELECT pg_sleep(2);
COMMIT;
SQL
  ) &
  local T1PID=$!
  perl -e 'select(undef,undef,undef,0.7)'
  local out2
  out2=$(P <<SQL 2>&1
\\echo T2_START
PREPARE s(text, uuid, text[]) AS $GUARDED;
EXECUTE s('$t2', '$ID', '{$f2}');
SQL
)
  local rc2=$?
  wait $T1PID; local rc1=$?
  local fin; fin=$(P -c "SELECT status FROM tenants WHERE id = '$ID'")
  echo "$label | start=$start | T1 $t1 from {$f1} rc=$rc1 | T2 $t2 from {$f2} rc=$rc2 out=[$(echo $out2 | tr '\n' ' ')] | final=$fin"
  rm -f /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/8eb04056-8fef-4c17-8fb3-31eec776f98e/scratchpad/gate64_t1.$$
}
run suspended archived suspended active provisioning,suspended "RACE1 suspended->archived vs suspended->active"
run active suspended active suspended active "RACE2 two concurrent active->suspended"
run suspended active provisioning,suspended archived suspended "RACE3 suspended->active vs suspended->archived"
run active suspended active active provisioning,suspended "RACE4 active->suspended vs (reactivate) ->active"
# CONTROL: the check-then-write shape the single statement replaces (read, decide in the app, unconditional write)
P -c "DELETE FROM tenants; INSERT INTO tenants (id, status) VALUES ('$ID', 'suspended');"
SEEN=$(P -c "SELECT status FROM tenants WHERE id = '$ID'")
( P <<SQL > /dev/null 2>&1
BEGIN;
UPDATE tenants SET status = 'archived' WHERE id = '$ID';
SELECT pg_sleep(2);
COMMIT;
SQL
) &
CP=$!
perl -e 'select(undef,undef,undef,0.7)'
case "$SEEN" in provisioning|suspended) OUTC=$(P -c "UPDATE tenants SET status = 'active', updated_at = now() WHERE id = '$ID'" 2>&1);; *) OUTC=refused;; esac
wait $CP
echo "CONTROL check-then-write (app saw '$SEEN', T1 archives meanwhile) | T2 out=[$OUTC] | final=$(P -c "SELECT status FROM tenants WHERE id = '$ID'")"
