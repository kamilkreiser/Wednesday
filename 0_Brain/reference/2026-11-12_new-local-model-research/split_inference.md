# Split inference across GB10 (CUDA/Linux) + Mac Studio 256 GB (Metal) — research 2026-11-12
All sources read 2026-11-12. UNVERIFIED = not confirmed at a primary source.

| Tool | CUDA-Linux + Metal-Mac in ONE model? | Split type | Per-node memory cap | Interconnect | MoE / DeepSeek | Maturity |
|---|---|---|---|---|---|---|
| **llama.cpp RPC (ggml-rpc)** | **YES** — README diagram shows CUDA, Metal, CPU hosts feeding one main host; each host builds "the backends for each accelerator" with -DGGML_RPC=ON. A third-party run did exactly Mac(Metal)+DGX Spark(CUDA). [1][5] | Default `-sm layer` = "split layers and KV across GPUs (pipelined)"; `row`; `tensor` "(EXPERIMENTAL)". [2] | Indirect only: `--tensor-split` proportions; `--fit-target` "target margin per device"; `-ot` tensor placement. rpc-server itself has NO memory-limit flag (options: -t -d -H -p -c). [1][2][3] | TCP default; RDMA "if both peers can use RDMA", else falls back to TCP. No speed recommended. [1] | DeepSeek V4 merged PR #24162 (2026-06-29); TODOs incl. MTP, `-sm tensor`, lightning indexer. `--cpu-moe`/`--n-cpu-moe`/`-ot` for expert placement. [2][6] | Latest build b12292 (11 Nov). README: RPC "proof-of-concept", "fragile and insecure", never on open network. [1][7] |
| **exo** | **NO** (today) — "A Mac and a Linux machine don't join each other, even on the same commit, because they run different builds of MLX." Linux: "runs on CPU… GPU support for Linux platforms is under development." [4] | Pipeline + tensor, topology-aware placement. TP "up to 1.8x speedup on 2 devices". [4] | None documented. [4] | RDMA over Thunderbolt 5 (macOS 26.2+, Mac-only). [4] | Model list incl. DeepSeek v3.1 671B, Kimi-K2; V4/MiMo not in release notes. [4][8] | v1.0.71 (23 Apr). [8] |
| exo "DGX Spark + Mac" blog | Not a model split: **prefill on Spark, KV streamed, decode on M3 Ultra** (disaggregation). [9] | Phase split | n/a | 10 GbE | Llama-3.1 8B only | Availability not stated; README contradicts mixing → treat as UNVERIFIED/not shipped. |
| **MLX mx.distributed** | **Unclear/no** — backends: MPI, RING (TCP), JACCL (RDMA over TB5, Macs), NCCL ("for CUDA environments"). Docs never state cross-platform. [10] Third party: ring "hangs indefinitely on the CUDA backend". [5] | Library primitives (TP/PP is up to user code) | n/a | Ring over Thunderbolt/Ethernet; JACCL "fully connected" TB5 only; JACCL "Necessary for… tensor parallelism". [10] | via mlx-lm (not checked) | — |
| **vLLM multi-node** | **NO** — requires "identical execution environment" on every node; no Apple mention. [11] vllm-metal: cross-Mac collectives "not yet implemented"; only single Mac validated. [12] | TP per node, PP across nodes (uneven PP splits OK). [11] | `gpu_memory_utilization` exists but not documented on the multi-node page (UNVERIFIED here). | "preferably… InfiniBand"; raw TCP "not efficient for cross-node tensor parallelism". [11] | Strong DeepSeek support (not re-checked) | — |
| **SGLang multi-node** | **NO evidence** — multi-node page shows CUDA `--nnodes/--tp` only; no Apple/MPS statement. [13] | TP shown; PP not on page. [13] | `--mem-fraction-static` (not on page, UNVERIFIED) | not stated | Refers to DeepSeek docs | — |

## Published heterogeneous numbers (only one found, third party)
dev.to (Mar 31, year not shown), llama.cpp RPC, Mac Studio M2 Ultra 128 GB (host, Metal) + DGX Spark GB10 (CUDA 13), direct 10GbE (9.41 Gbps measured): [5]
- Qwen2.5-72B Q4_K_M: local Metal 28 pp / 11 tg tok/s → RPC split (31 GB Metal / 14 GB CUDA) 30 pp / **6 tg** tok/s.
- Qwen2.5-7B: 92 tg local → 53 tg over RPC. i.e. splitting **halved decode** at 10GbE.
- Author's 200B+ MoE "~4–8 tok/s" is a projection, not measured.
exo disaggregation (Llama-3.1 8B FP16, 8K prompt, 10GbE): Spark prefill 1.47 s, M3 Ultra decode 0.85 s/32 tok, 2.8x vs Mac alone. [9]

## Notes
- Memory cap: no tool offers a hard "give X GB" per node. llama.cpp is closest: `--tensor-split` (proportions) + `--fit-target` (headroom per device) + `-ot`. Note rpc-server allocates on the remote's device; macOS Metal wired-memory limit (iogpu.wired_limit_mb) also governs the Mac side — UNVERIFIED in docs read today.
- Bandwidth caveat: layer split sends only activations per token, but each token pays a network round trip per split boundary; at 10GbE/TCP decode roughly halved in the one measured case. RDMA in ggml-rpc needs RDMA-capable NICs on both ends; GB10 has ConnectX-7 but Mac Studio has no RDMA Ethernet (TB5 RDMA is Mac↔Mac) → expect TCP. (hardware NIC claim UNVERIFIED)
- Model sizes: DeepSeek V4 Flash reported 284B (third-party blog [14]); "V4.1 Flash ~763B" and "MiMo V2.6 Flash 309B" UNVERIFIED. MiMo V2-Flash: only community GGUFs (mradermacher); llama.cpp native "MiMo2" support claimed on a V2.5 GGUF card — UNVERIFIED for V2.6.
- Combined capacity: 128 + 256 = 384 GB minus OS/workload headroom; a ~284B Q4 (~150-185 GB) fits; 763B Q4 (~400 GB+) would not (arithmetic, not sourced).

## Sources (all read 2026-11-12)
[1] https://github.com/ggml-org/llama.cpp/blob/master/tools/rpc/README.md
[2] https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
[3] https://raw.githubusercontent.com/ggml-org/llama.cpp/master/tools/rpc/rpc-server.cpp
[4] https://github.com/exo-explore/exo
[5] https://dev.to/ljkunal/distributed-llm-inference-across-nvidia-blackwell-and-apple-silicon-over-10gbe-2feg
[6] https://github.com/ggml-org/llama.cpp/pull/24162
[7] https://github.com/ggml-org/llama.cpp/releases
[8] https://github.com/exo-explore/exo/releases
[9] https://blog.exolabs.net/nvidia-dgx-spark/
[10] https://ml-explore.github.io/mlx/build/html/usage/distributed.html
[11] https://docs.vllm.ai/en/latest/serving/parallelism_scaling.html
[12] https://docs.vllm.ai/projects/vllm-metal/en/latest/distributed/ (via search summary; page not fetched directly)
[13] https://docs.sglang.io/references/multi_node_deployment/multi_node.html
[14] https://blog.asadfaizee.is-a.dev/posts/deepseek-v4-flash-0731-gguf-run-284b-ai-model-locally/ (search snippet only)
