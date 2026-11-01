#!/bin/bash
# Gate 70: create gate70-pg (postgres:15-alpine, loopback, random port), init from scratch copies of the
# repo's docker/init + docker/init-platform, then apply migrations with the repo's scripts/run-migrations.sh
# inside the container. Passwords: openssl rand into the scratchpad pw.env (0600); scrubbed from every log.
set -u
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate70-ks1384-r2b-1884
D=$G/repo/Blockchain/Dev
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c6cc71e2-d540-45eb-85fa-5aca0154bf77/scratchpad/g70
mkdir -p $S/tmp
docker inspect gate70-pg >/dev/null 2>&1 && { echo "REFUSE: gate70-pg already exists"; exit 9; }
umask 077
printf 'SU=%s\nAPP=%s\n' "$(openssl rand -hex 24)" "$(openssl rand -hex 24)" > $S/pw.env
chmod 600 $S/pw.env
SU=$(grep '^SU=' $S/pw.env | cut -d= -f2); APP=$(grep '^APP=' $S/pw.env | cut -d= -f2)
umask 022
rm -rf $S/init $S/init-platform $S/mig
cp -R $D/docker/init $S/init; cp -R $D/docker/init-platform $S/init-platform
mkdir -p $S/mig; cp -R $D/migrations $S/mig/migrations; cp $D/scripts/run-migrations.sh $S/mig/run-migrations.sh
docker run -d --name gate70-pg -p 127.0.0.1::5432 \
  -e POSTGRES_USER=secuura -e POSTGRES_PASSWORD="$SU" -e POSTGRES_DB=secuura \
  -e APP_DB_USER=secuura_app -e APP_DB_PASSWORD="$APP" -e TZ=UTC \
  -e POSTGRES_INITDB_ARGS="--auth-host=scram-sha-256 --auth-local=scram-sha-256" \
  -v $S/init:/docker-entrypoint-initdb.d -v $S/init-platform:/docker-entrypoint-initdb.d/platform -v $S/mig:/mig \
  postgres:15-alpine postgres -c max_connections=1000 > $G/evidence/pg_container_id.txt 2>&1
echo "docker run rc=$?"
chmod 600 $G/evidence/pg_container_id.txt
for i in $(seq 1 60); do
  docker exec gate70-pg pg_isready -U secuura -d secuura -h 127.0.0.1 >/dev/null 2>&1 && break; sleep 2
done
sleep 4
for i in $(seq 1 30); do
  docker exec gate70-pg pg_isready -U secuura -d secuura -h 127.0.0.1 >/dev/null 2>&1 && break; sleep 2
done
docker logs gate70-pg > $G/evidence/pg_init.log 2>&1
docker exec -e DATABASE_URL="postgresql://secuura:${SU}@127.0.0.1:5432/secuura" \
  -e PLATFORM_DATABASE_URL="postgresql://secuura:${SU}@127.0.0.1:5432/secuura_platform" \
  -w /mig gate70-pg sh /mig/run-migrations.sh > $G/evidence/migrate.log 2>&1
echo "migrate rc=$?" >> $G/evidence/migrate.log
sed -i '' -e "s/${SU}/<SU>/g" -e "s/${APP}/<APP>/g" $G/evidence/migrate.log $G/evidence/pg_init.log
echo "password occurrences in migrate.log: $(grep -c -e "$SU" -e "$APP" $G/evidence/migrate.log)"
echo "password occurrences in pg_init.log: $(grep -c -e "$SU" -e "$APP" $G/evidence/pg_init.log)"
tail -3 $G/evidence/migrate.log
docker port gate70-pg 5432
