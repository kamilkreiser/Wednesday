# Reload DeepSeek V4 Flash (after it was stopped to free memory)

Everything is on disk. No re-download. Expect ~5 minutes to /health.

    cd ~/DeepSeek-v4-Flash-One-DGX-Spark
    ./run-a2.sh            # wrapper: SERVING_HOST=127.0.0.1, STARTUP_WAIT, HF_TOKEN

or without the watcher:

    cd ~/DeepSeek-v4-Flash-One-DGX-Spark
    SERVING_HOST=127.0.0.1 ./start.sh --no-wait

Verify:

    curl -sf http://127.0.0.1:8888/health && echo OK
    free -g        # ~118G used once loaded

Preserved on disk (do not delete):
  hf-hub/   100G  weights, 190/190 files
  data/      99G  coalesced TP1 checkpoint + K64 draft
  cache/     80M  torch compile cache
  docker image, pinned by digest

NOTE: port 8888 and ~118G of RAM are needed. Stop Ollama/Ornith first:
    pkill -f 'ollama serve'
