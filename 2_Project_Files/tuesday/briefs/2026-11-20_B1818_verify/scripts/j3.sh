#!/bin/bash
L=/private/tmp/b1818-gate/logs/chain; C=/private/tmp/b1818-gate/clone
bash $C/scripts/secret-scan.sh --self-test > $L/secret_selftest.log 2>&1; echo "secret_selftest rc=$?" >> $L/RCS.txt
bash $C/scripts/secret-scan.sh --tree > $L/secret_tree.log 2>&1; echo "secret_tree rc=$?" >> $L/RCS.txt
