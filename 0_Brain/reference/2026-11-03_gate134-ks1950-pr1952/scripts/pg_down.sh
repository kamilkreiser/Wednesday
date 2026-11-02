#!/bin/bash
docker rm -f gate134-pg; echo "rm rc=$?"; echo "remaining: $(docker ps -a --filter name=gate134 -q | wc -l)"
