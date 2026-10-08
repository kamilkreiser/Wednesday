#!/bin/bash
# oMLX test setup (2026-10-08, Kam's live-board ask 16:12): drive-local venv + the pinned checkpoint download.
# Plan + evidence: 0_Brain/reference/2026-10-08_omlx-flash-next/REPORT.md. Rollback = quarantine this folder.
set -u
T=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/omlx
export UV_CACHE_DIR=$T/uv-cache HF_HOME=$T/hf-home OMLX_BASE_PATH=$T/base
echo "== $(date '+%F %T') venv"
[ -x $T/venv/bin/python ] || uv venv --python /opt/homebrew/bin/python3.12 $T/venv || exit 10
echo "== $(date '+%F %T') install omlx 0.7.0"
uv pip install --python $T/venv/bin/python https://github.com/jundot/omlx/releases/download/v0.7.0/omlx-0.7.0-cp312-cp312-macosx_15_0_universal2.whl || exit 11
$T/venv/bin/python -c 'import mlx.core as mx; print("mlx", mx.__version__)' || exit 12
HF=$T/venv/bin/hf; [ -x $HF ] || { uv pip install --python $T/venv/bin/python 'huggingface_hub[cli]' || exit 13; }
echo "== $(date '+%F %T') download"
$T/venv/bin/hf download Jundot/Qwen3.8-Flash-Next-oQ4e-mtp --revision 2615fc0e976e65c2f3b55daca3a948f1cdc5b9f8 --local-dir $T/models/Qwen3.8-Flash-Next-oQ4e-mtp
rc=$?
echo "== $(date '+%F %T') download rc=$rc; files: $(ls $T/models/Qwen3.8-Flash-Next-oQ4e-mtp 2>/dev/null | wc -l); size: $(du -sh $T/models 2>/dev/null | cut -f1)"
exit $rc
