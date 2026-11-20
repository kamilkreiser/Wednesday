#!/bin/bash
L=/private/tmp/b1818-gate/logs
docker image inspect --format '{{.Id}} {{.Created}} {{.Config.WorkingDir}}' pc-b1803-node:merged > $L/j1_image.txt 2>&1
docker run --rm --network none --entrypoint sh pc-b1803-node:merged -c 'cd /repo && find . -type f ! -path "*/node_modules/*" ! -path "*/dist/*" ! -name "*.tsbuildinfo" -exec sha256sum {} +' > $L/image_sha_raw.txt 2>$L/j1_err.txt
echo "rc=$?"
