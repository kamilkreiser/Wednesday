#!/bin/bash
docker rm -f gate136-pg; echo "rm rc=$?"; echo "remaining: $(docker ps -a --filter name=gate136 -q | wc -l)"
