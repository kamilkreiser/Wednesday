#!/bin/bash
# render.sh CLONE ENTRY(dev|root) TAG [VAR=v ...]: what pgbouncer's entrypoint renders from what compose passes it.
# compose config -> node keeps ONLY the pool/upstream keys (never a *PASSWORD*) -> 0600 env file in scratch ->
# entrypoint.sh lines 42-56 (the render block, cut from the repo file, not retyped) run by busybox sh+sed in a
# --network none throwaway alpine container (redis:7-alpine; the edoburu image is not on this host) on a COPY of
# the committed pgbouncer.ini. Prints the [section] and `secuura =` lines (crafted marker only).
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate174-ks915-pr1989-r2/harness/lib.sh
c="$1"; entry="$2"; tag="$3"; shift 3; X=("$@"); d=$W/scratch/render-$tag; mkdir -p $d; umask 077
if [[ $entry == dev ]]; then (cd $c/Blockchain/Dev && env -i PATH=$GPATH HOME=$W/home ${X[@]+"${X[@]}"} docker compose config --format json 2>/dev/null)
else (cd $c && env -i PATH=$GPATH HOME=$W/home ${X[@]+"${X[@]}"} docker compose -f docker-compose.local.yml config --format json 2>/dev/null); fi \
 | node -e 'let b="";process.stdin.on("data",x=>b+=x).on("end",()=>{const e=((JSON.parse(b).services||{}).pgbouncer||{}).environment||{};for(const k of ["POSTGRES_HOST","POSTGRES_PORT","POSTGRES_DB","PGBOUNCER_MAX_CLIENT_CONN","PGBOUNCER_DEFAULT_POOL_SIZE","PGBOUNCER_RESERVE_POOL_SIZE","PGBOUNCER_MAX_DB_CONNECTIONS","PGBOUNCER_MAX_USER_CONNECTIONS"]) if(k in e && !/PASSWORD/.test(k)) console.log(k+"="+String(e[k]??"").replace(/\n/g,"<NL>"))})' > $d/pgb.env
mkdir -p $d/etc; cp $R/Blockchain/Dev/docker/pgbouncer/pgbouncer.ini $d/etc/pgbouncer.ini; chmod 755 $d/etc; chmod 666 $d/etc/pgbouncer.ini
sed -n '42,56p' $R/Blockchain/Dev/docker/pgbouncer/entrypoint.sh > $d/render_block.sh
docker run --rm --network none --env-file $d/pgb.env -v $d:/w -v $d/etc:/etc/pgbouncer --entrypoint /bin/sh redis:7-alpine -c 'sh /w/render_block.sh; echo "render rc=$?"' 2>&1 | tail -3
printf '  rendered [section]/secuura lines: '; grep -n -E '^\[|^secuura|^max_client_conn|^default_pool_size|^reserve_pool_size|^max_db_connections' $d/etc/pgbouncer.ini | tr '\n' ' '; echo
