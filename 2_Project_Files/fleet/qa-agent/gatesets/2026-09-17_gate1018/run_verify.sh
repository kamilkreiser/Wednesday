#!/bin/bash
E="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"
export GH_TOKEN=$(grep -E '^GH_TOKEN=' "$E" | head -1 | cut -d= -f2- | tr -d '"'"'")
export LINEAR_API_KEY=$(grep -E '^LINEAR_API_KEY=' "$E" | head -1 | cut -d= -f2- | tr -d '"'"'")
python3 "$(dirname "$0")/${VERIFY:-merged_verify.py}"
