#!/bin/bash
L=/private/tmp/b1818-gate/logs/chain; C=/private/tmp/b1818-gate/clone
PC_NODE_CI_IMAGE=pc-b1803-node:merged bash $C/scripts/test-db.sh > $L/test_db.log 2>&1; echo "test_db rc=$?" >> $L/RCS.txt
echo "left containers: $(docker ps -a --format '{{.Names}}' | grep -c -E 'pc-dbtest')  networks: $(docker network ls --format '{{.Name}}' | grep -c pc-dbtest)" >> $L/RCS.txt
