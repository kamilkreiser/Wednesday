---
date: 2026-10-09
type: reference
source: read-only research sub-agent commissioned by Wednesday 17:23 after Kam ruled card wed-studio-256-measure-before-buying-1009 = a ("Measure first", 17:22:01). No signup, no request to any model; only OpenRouter's public listing endpoints + provider docs read 2026-10-09. Returned as text; saved by Wednesday.
status: live
---

# Hosted APIs for MiMo-V2.6-Flash, GLM-5.3-Flash (and DeepSeek V4 Flash 0731 as the Spark reference)

## BLUF
- **All three are on OpenRouter** (one OpenAI-compatible endpoint; provider and precision can be pinned).
- **MiMo-V2.6-Flash:** DeepInfra fp8, $0.14 in / $0.28 out per M tokens, listed zero retention. Xiaomi direct is the same price but RETAINS prompts 30 days. Thinking can be disabled.
- **GLM-5.3-Flash:** Z.ai first-party fp8, $0.15 / $0.50, listed no training / no retention. **Thinking CANNOT be disabled** (docs.z.ai: "GLM-5.3 and GLM-5.3-FLASH no longer support disabling thinking"; OpenRouter `mandatory: true`, lowest effort "low"). It can only be scored at "low" thinking, unlike our thinking-OFF harness; output tokens likely far above 3K/task.
- **DeepSeek V4 Flash 0731:** DeepSeek's own API retired the name (routes to V4.1-Flash). DeepInfra fp8 still serves 0731, $0.06 / $0.18. `reasoning.effort: "none"` disables thinking.
- **Estimated cost (Wednesday's token estimate: 46 tasks × 25K in + 3K out, one attempt): MiMo $0.20, GLM $0.24, DeepSeek $0.09 → both targets $0.44 at 1×, $1.32 at 3×; with the reference $0.53 / $1.60.**
- **Data controls for Secuura code:** `provider.zdr: true` (or `data_collection: "deny"`) + pin the provider with `only`. Avoid Xiaomi direct (30-day retention), StreamLake, GMICloud, Darkbloom (retain prompts) and DeepSeek direct (training: true). The retention flags are OpenRouter's provider data, not each provider's legal text; OpenRouter's privacy page says provider settings have "no bearing on OpenRouter's own policies" and does not state its own retention period.
- **Same-weights caveat:** OpenRouter maps MiMo to `XiaomiMiMo/MiMo-V2.6-Flash-RL`; precision is fp8 at the recommended hosts (GMICloud bf16 is the only full-precision host and retains prompts).

## Per model (read at openrouter.ai/api/v1/models and …/endpoints, 2026-10-09)
**MiMo-V2.6-Flash** `xiaomi/mimo-v2.6-flash` (309B/15B): DeepInfra fp8 0.14/0.28 no retention · Xiaomi fp8 1M ctx 0.14/0.28 RETAINS 30 d · Novita fp8 0.14/0.28 no · Makora fp8 0.13/0.28 no · Darkbloom fp4 0.10/0.28 retains · Venice fp8 0.175/0.35 no · GMICloud bf16 0.14/0.28 retains (degraded). Thinking off: `thinking: {"type":"disabled"}` (docs.litellm.ai/blog/mimo_v2_6). DeepInfra: "We do not use data you submit to our APIs for training models" / "Input data is not stored to disk" (docs.deepinfra.com/account/data-privacy).
**GLM-5.3-Flash** `z-ai/glm-5.3-flash` (320B/18B; 33 endpoints): Z.ai fp8 1M 0.15/0.50 (cached in $0.03) no · Novita fp8 0.084/0.28 no · DeepInfra fp4 0.075/0.25 no · Together/Fireworks 0.15/0.50 no · SiliconFlow/BaseTen fp8 0.15/0.50 no (degraded). Efforts: max (default), high, low.
**DeepSeek V4 Flash 0731** `deepseek/deepseek-v4-flash-0731` (284B/13B): DeepInfra fp8 0.06/0.18 no · Parasail fp8 0.14/0.28 no · Together 0.14/0.28 no · BaseTen fp8 0.13/0.26 no · StreamLake fp8 0.044/0.132 retains.

## Arithmetic
Per model: 46 × 25,000 = 1.15M input; 46 × 3,000 = 0.138M output (estimates, not measurements).
MiMo: 1.15 × 0.14 + 0.138 × 0.28 = 0.161 + 0.0386 = $0.20 · GLM: 0.1725 + 0.069 = $0.24 · DeepSeek: 0.069 + 0.0248 = $0.09.

## UNREAD
Xiaomi's own pricing/privacy pages (JS-only); HF model cards (401); Together/Fireworks/Novita/SiliconFlow own sites; Z.ai's and Novita's own privacy wording; OpenRouter's credit-purchase fee / minimum top-up; GLM's real output tokens at "low" thinking.

## Sources (2026-10-09)
openrouter.ai/api/v1/models, /api/v1/models/{id}/endpoints, /api/v1/providers, /api/frontend/v1/all-providers; openrouter.ai/docs/features/provider-routing, /privacy-and-logging, /use-cases/reasoning-tokens; api-docs.deepseek.com/quick_start/pricing; docs.z.ai/guides/overview/pricing, /guides/capabilities/thinking; docs.deepinfra.com/account/data-privacy; docs.litellm.ai/blog/mimo_v2_6. Raw JSON: session scratchpad `hostedapi/` (not durable).
