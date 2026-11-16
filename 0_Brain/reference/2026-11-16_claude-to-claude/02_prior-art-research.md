# Claude-to-Claude — Prior-Art Research (02)

**Date researched:** 2026-11-16 · **Scope:** standards, vendor permission models, open-source precedents, pairing/transport, remote-support consent models, security model, oversight-console UX.

**How to read this.** Every claim carries a source in the list at the end (`[S#]`). Pages were read on 2026-11-16 through a fetch tool that summarises long pages with a small model, so field names quoted here were relayed by that summariser — re-open the cited page before pinning any name in code. **UNVERIFIED** means I could not confirm it from a primary source in this session (it is from secondary coverage or general knowledge). Licences and "last pushed" dates come from the public GitHub API on 2026-11-16.

---

## Executive summary

1. **No vendor has shipped cross-USER agent linking.** Not found in Anthropic, OpenAI, Google, Cursor, GitHub, Cognition, Warp or Amp docs. Claude Code's cross-session messaging is explicitly "your other sessions" only [S9]; the nearest shipped thing is Warp's agent session sharing, where a second *human* steers one agent with view/edit roles [S27]. The gap is real; community MCP bridges (claude-peers, repowire, claude-mesh) fill it without an oversight model [S38].
2. **Anthropic has already written the trust rule we need, and we should copy it verbatim:** a message from another session "never counts as your consent", cannot approve a prompt, cannot change configuration, and commands in it do not run; the receiver's own permission prompts still fire [S9][S8].
3. **Phase 1 enforcement point exists and is stable: Claude Code hooks + Agent SDK `canUseTool`.** `PreToolUse` (allow/deny/ask/defer, runs even in bypass mode) and `canUseTool` (allow with `updatedInput`, deny with message, `updatedPermissions` for "remember") give per-action gating outside the model [S5][S6][S7]. The console should be a client of these, not a new permission system.
4. **Claude Code "Channels" is the first-party shape of our prototype** (an MCP server that pushes events into a session, with an opt-in permission-relay capability) — but it is a research preview, custom channels need `--dangerously-load-development-channels`, and it needs claude.ai login [S10]. Use it as a design reference; do not depend on it yet.
5. **Phase 2: ACP is the least-custom-work route to agent-agnostic.** Agent Client Protocol already standardises exactly our console's data model — `session/request_permission` with `allow_once / allow_always / reject_once / reject_always`, tool-call kinds, diff content, and "follow-along" locations — and ~50 agents are listed (Claude via adapter, Codex via adapter, Gemini CLI, Cursor, Copilot, OpenCode, Cline, Goose, OpenHands…) [S3][S4].
6. **The standards are layers, not rivals:** MCP = agent↔tools, ACP (Zed) = UI/host↔agent, A2A = agent↔agent across organisations. IBM's ACP merged into A2A (Aug/Sep 2025); A2A (v1.0.x) and MCP now both sit in the Linux Foundation's Agentic AI Foundation [S1][S2][S13][S14].
7. **A2A fits our semantics but not our topology.** Its task states `INPUT_REQUIRED` / `AUTH_REQUIRED` map well onto "waiting for host approval", but A2A assumes HTTPS-reachable servers with TLS identity; two laptops behind NAT are not that. Borrow the data model (it permits custom bindings); do not adopt its transport in phase 1 [S1].
8. **Pairing: keep the relayed WebSocket, fix the handshake.** A short code must feed a PAKE (SPAKE2, as Magic Wormhole does) so the relay cannot man-in-the-middle; a 16-bit wormhole code gives an attacker a 1-in-65,536 single guess [S15][S16]. Then pin long-term identity keys and show a short authentication string. Whether the current prototype's 8-character code authenticates the X25519 exchange is the first thing to check.
9. **Every serious vendor now pairs approvals with an OS sandbox and an LLM "auto-review" tier** (Claude auto mode, Codex `auto_review`, Cursor Auto-review) — and each says plainly it is not a security boundary [S6][S19][S20]. Our "approved trust" mode should be: sandbox + deterministic allow-rules + classifier + always-ask class, never "approve everything".
10. **This product sits squarely on the lethal trifecta / Rule of Two:** untrusted remote text + private local data + ability to act and communicate. Meta's rule and Willison's framing both conclude the same thing — with all three present, a human approves or the agent does not run autonomously [S30][S31]. That is the argument for CONTROLLED being the default mode.

---

## A. Agent-to-agent interoperability standards

### A.1 A2A (Agent2Agent) — Linux Foundation / AAIF

- **Version read:** the spec site showed `1.0.0` as "Latest Released Version" [S1]; the GitHub repo has tags `v1.0.0` (2026-03-12) and `v1.0.1` (2026-05-28) [S39]. Apache-2.0.
- **Governance:** donated by Google to the Linux Foundation in June 2025; announced as a hosted project of the Agentic AI Foundation (AAIF) on 2026-08-17 (AAIF blog) [S14]. "150+ partner organisations" is the AAIF's own figure; I did not verify it independently — treat the number as UNVERIFIED.
- **Agent Card:** JSON at `https://{domain}/.well-known/agent-card.json`; declares `supportedInterfaces` (each with protocol + `tenant`), `capabilities.streaming / pushNotifications / extendedAgentCard`, `skills`, `securitySchemes`, `security`, and optional `signatures` (JWS over a JCS-canonicalised card). `GetExtendedAgentCard` returns more after authentication [S1].
- **Tasks:** states `SUBMITTED, WORKING, COMPLETED, FAILED, CANCELED, REJECTED` plus two interrupted states **`INPUT_REQUIRED`** and **`AUTH_REQUIRED`**. Operations: `SendMessage`, `SendStreamingMessage`, `GetTask`, `ListTasks`, `CancelTask`, `SubscribeToTask`, push-notification config CRUD [S1].
- **Bindings:** JSON-RPC, gRPC, HTTP+JSON, and a section for custom bindings; the `.proto` is normative [S1].
- **Auth:** API key, HTTP auth, OAuth2 (incl. `DeviceCodeOAuthFlow`), OIDC, mutual TLS. Production "MUST use encrypted communication". The spec warns that the `AUTH_REQUIRED` transition "by itself" is not authorisation, and that credentials should arrive out of band [S1].
- **What we should take from this:** adopt A2A's *vocabulary* for the cross-party message layer (task, artifact, `INPUT_REQUIRED` = "waiting on the host's approval", `REJECTED` = host said no) so a later A2A gateway is a mapping exercise. Do not adopt its transport/identity model in phase 1: it presumes each agent is a TLS-terminated HTTP server, which is the opposite of two NAT-ed laptops.

### A.2 Model Context Protocol (MCP)

- **Version read:** revision **2026-07-28** (changelog relative to 2025-11-25) [S2]. This revision is a large break:
  - Protocol made **stateless**: `initialize` handshake and `Mcp-Session-Id` removed; every request carries version and capabilities in `_meta`; new mandatory `server/discover` [S2].
  - **Server-initiated requests are gone.** Elicitation, sampling and roots are now delivered by the Multi Round-Trip Request pattern: the server returns `InputRequiredResult` (`resultType: "input_required"`) and the client retries with `inputResponses` [S2][S11].
  - **Sampling, Roots and Logging are deprecated** (12-month window); SSE resumability removed; HTTP+SSE transport deprecated; tasks moved to an extension `io.modelcontextprotocol/tasks` [S2].
- **Elicitation:** form mode (flat JSON-schema form) and URL mode (out-of-band, for secrets and third-party OAuth). Three response actions: `accept / decline / cancel`. Servers "MUST NOT" request secrets in form mode; clients must show which server is asking [S11].
- **Authorization:** optional, HTTP transports only (stdio takes credentials from the environment). OAuth 2.1 subset; servers MUST publish Protected Resource Metadata (RFC 9728); clients MUST send Resource Indicators (RFC 8707); tokens are audience-bound and token passthrough is forbidden; Client ID Metadata Documents preferred, Dynamic Client Registration deprecated; step-up on `insufficient_scope` [S12].
- **Agent-to-agent:** nothing in the core spec addresses agent-to-agent. MCP remains agent↔tool. Claude Code's Channels and cross-session messaging are vendor extensions riding on MCP, not MCP features [S9][S10].
- **What we should take from this:** MCP is the right way to *expose our link to each agent* (it is what every CLI already loads), and its elicitation semantics (`accept/decline/cancel`, "show who is asking") are a good approval-dialog contract. But do not build on sampling or server-initiated requests — they are deprecated or removed as of 2026-07-28. Design our MCP server as request/response with `input_required` round trips.

### A.3 Agent Client Protocol (ACP, Zed) — editor/host ↔ agent

- **Version read:** repo `agentclientprotocol/agent-client-protocol`, release `v1.18.0` and `schema-v1.32.0` on 2026-11-14, with a `schema-v2.0.0-alpha.16` line in progress. Apache-2.0 [S39][S3].
- **Transport:** JSON-RPC over stdio for local agents (agent is a subprocess of the client). Remote agents over HTTP/WebSocket: "Full support for remote agents is a work in progress" [S3].
- **Permission flow:** the agent reports a tool call (`session/update` → `tool_call` with `toolCallId`, `title`, `kind`, `status`), then may call **`session/request_permission`** with `options[]`, each `{optionId, name, kind}` where kind ∈ **`allow_once | allow_always | reject_once | reject_always`**. The client answers `selected` (with `optionId`) or `cancelled`. The agent, not the client, stores remembered decisions and "should not apply a remembered decision beyond the scope it stated" [S3].
- **Console-relevant types:** tool kinds `read, edit, delete, move, search, execute, think, fetch, switch_mode, other`; statuses `pending, in_progress, completed, failed`; **diff content** `{path, oldText, newText}`; **locations** `{path, line}` for following the agent — "Locations are display metadata and do not grant file access" [S3].
- **Agents listed** (~50) [S4]: Claude Agent (via the `claude-agent-acp` adapter, now in the `agentclientprotocol` org, Apache-2.0 [S39]), Codex CLI (via an adapter; note `zed-industries/codex-acp` is archived as of 2026-07 [S39] — which adapter is current is UNVERIFIED), Gemini CLI, Cursor, GitHub Copilot (public preview), OpenCode, Cline, Goose, OpenHands, Kiro CLI, Junie, Qwen Code, Mistral Vibe, Augment, Factory Droid, and others.
- **What we should take from this:** ACP is the phase-2 adapter layer. If the host-side daemon speaks ACP *as a client*, it can drive any listed agent and receives permission requests, diffs and locations in one schema — which is exactly the right-hand approvals pane and the main "changing code" pane. Model our internal event schema on ACP's tool-call/permission types from day one, even while phase 1 uses Claude-specific hooks.

### A.4 IBM / BeeAI Agent Communication Protocol

- Merged into A2A under the Linux Foundation in late August / early September 2025 (sources disagree on the exact day: 25 Aug, 29 Aug, 1 Sep); the ACP repo is archived and points to an A2A migration guide. **UNVERIFIED** — secondary sources only [S13].
- **What we should take from this:** ignore it as a target; the name collision with Zed's ACP is the only thing to remember.

### A.5 AGNTCY, ANP and others

- **AGNTCY** (Cisco-originated, Linux Foundation): Agent Directory + OASF schema + **SLIM** (Secure Low-Latency Interactive Messaging), which uses **MLS (RFC 9420)** for end-to-end group encryption and can carry A2A and MCP; an IETF Internet-Draft `draft-mpsb-agntcy-slim` exists. `agntcy/slim` is Apache-2.0, active [S13][S39]. Details beyond the repo metadata are from secondary sources — UNVERIFIED.
- **ANP** (Agent Network Protocol): DID-based identity for open agent networks; repo Apache-2.0, ~1.5k stars, active [S39]. Standardisation status UNVERIFIED.
- **What we should take from this:** SLIM is the only prior art that puts *content-blind relay + MLS group keys* under agent protocols — the right reference if we ever go beyond two parties. Not needed for phase 1.

### A.6 How they relate, and the phase-2 answer

| Layer | Standard | Role for us |
|---|---|---|
| Agent ↔ its tools | MCP (2026-07-28) | How each agent sees the link (tools: send, read, propose) |
| Host UI/daemon ↔ agent | ACP (Zed) | Agent-agnostic driving, permission requests, diffs, follow |
| Party ↔ party | A2A (1.0.x) data model | Cross-party message/task vocabulary; future gateway |
| Transport/E2E | none of the above | Ours: PAKE pairing + E2E channel over a blind relay |

They are **complementary**. Least custom work for phase 2: **ACP on the host side** (one client implementation, ~50 agents) + **MCP on the guest side** (every CLI already loads MCP servers) + **A2A-shaped messages in between**.

---

## B. How vendors do human-in-the-loop permissioning today

### B.1 Claude Code (docs reference versions up to v2.1.317)

- **Permission modes:** `default` (Manual), `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`. Deny rules apply in every mode including bypass [S6].
- **Rules:** `allow / ask / deny` with specifiers — `Bash(npm test *)` command patterns, `Read(...)`/`Edit(...)` path globs, `WebFetch` domain rules, `mcp__server__tool` [S5][S7].
- **Remember semantics by tool type:** Bash "Yes, don't ask again" = permanent per repository and command; file edits = until session end; WebFetch = permanent per repository and domain [S5].
- **Evaluation order (SDK):** hooks → deny rules → ask rules → permission mode → allow rules → `canUseTool`. A hook `allow` does not skip deny/ask rules; a hook `deny` holds even in `bypassPermissions` [S7].
- **Hooks:** 33 events incl. `PreToolUse`, `PermissionRequest`, `PermissionDenied`, `PostToolUse`, `Elicitation`, `SessionStart`. `PreToolUse` returns `permissionDecision: allow | deny | ask | defer`. Hook types include `command` and **`http`** (POST JSON to a URL, with `onFailure: "block"`) [S5a]. `defer` lets a process exit and resume later [S8].
- **`canUseTool` (Agent SDK):** `(toolName, input, {signal, suggestions})` → `{behavior:"allow", updatedInput, updatedPermissions?}` or `{behavior:"deny", message}`; can stay pending indefinitely; also receives `AskUserQuestion`. `setPermissionMode()` changes mode mid-session — "start restrictive and loosen permissions as trust builds" [S7][S8].
- **Auto mode:** a separate classifier model reviews actions; tool results are stripped from the classifier's input so hostile file/web content cannot steer it; blocks `curl | bash`, exfiltration, force-push, prod deploys, IAM grants by default; 3 consecutive or 20 total blocks drops back to prompting. Docs state it "does not guarantee safety" [S6].
- **Sandbox:** Seatbelt on macOS; bubblewrap + socat (+ optional seccomp) on Linux/WSL2; native Windows unsupported. Network via a local proxy with an `allowedDomains` list that starts empty. Built-in file tools, MCP servers and hooks run *outside* the sandbox. Open-sourced as `@anthropic-ai/sandbox-runtime` (Apache-2.0) [S20][S39].
- **Remote Control:** continue a local session from claude.ai or the mobile app. Outbound HTTPS only, no inbound ports, traffic via the Anthropic API over TLS, short-lived scoped credentials; permission prompts and questions are forwarded and can be pushed to the phone; optional Trusted Devices. **Same account only** — subscription login required, not API keys [S21].
- **Cross-session messaging (v2.1.224+):** Claude can message "your other Claude Code sessions" on the same machine (Unix socket restricted to your OS user) or your other machines/cloud (via Anthropic servers + Remote Control). Plain text only. Inbound control `crossSessionInbound: accept | hold | refuse`; `isolatePeerMachines` forces approval before a message leaves the machine. **Not cross-user.** [S9]
- **Agent teams (experimental):** lead + teammates, shared task list, JSON-file mailboxes under `~/.claude/teams/`. One machine, one session; teammate permission prompts bubble to the lead; "a teammate can't approve a permission prompt or supply consent on your behalf" [S8a].
- **Channels (research preview):** an MCP server declaring `claude/channel` pushes `<channel source=…>` events into a session; with `claude/channel/permission` Claude Code sends `notifications/claude/channel/permission_request` (`request_id`, `tool_name`, `description`, `input_preview`) and accepts a verdict `{request_id, behavior: allow|deny}`. Docs: "An ungated channel is a prompt injection vector"; gate on sender identity, not room [S10].
- **Cloud session sharing:** share links are view-only snapshots (Team or Public visibility), not live steering [S22].
- **What we should take from this:** the host-side integration for phase 1 is `PreToolUse` (HTTP hook to our local daemon) plus `canUseTool` where we own the process. Copy `hold` as a first-class inbound state, the per-tool-type "remember" scopes, and the rule that forwarded text is never consent.

### B.2 OpenAI Codex (CLI/app; doc page undated, references Codex 0.115)

- Two independent axes: **sandbox** (`read-only`, `workspace-write` default, `danger-full-access`) and **approval policy** (`on-request`, `never`, or granular `{sandbox_approval, rules, mcp_elicitations, request_permissions, skill_approval}`); `untrusted` is retired [S19].
- OS sandbox: Seatbelt (macOS), bwrap + seccomp (Linux); Windows via a mechanism the page calls MXC (as relayed by the summariser — verify). Network off by default in `workspace-write`; optional proxy with domain allow/deny where deny wins. Protected paths inside writable roots: `.git`, `.codex`, `.agents`, `.aws` [S19].
- **Auto-review:** `approvals_reviewer = "auto_review"` reviews only actions that already need approval; low/medium proceed, critical denied, failures and timeouts fail closed [S19].
- App-server protocol: bidirectional JSON-RPC with server-initiated approval requests (`item/commandExecution/requestApproval`, decisions incl. accept / acceptForSession / decline / cancel) — **UNVERIFIED**, from community notes [S40].
- **What we should take from this:** the two-axis framing (what is technically possible vs. when to ask) is the clearest mental model on the market; use it in our UI copy. "Fail closed on reviewer timeout" is the right default for our approval queue too.

### B.3 Gemini CLI (docs at geminicli.com, undated)

- Approval modes `default`, `autoEdit`, `plan`, `yolo` (CLI flag only). A **policy engine** of TOML rules: `toolName`, `mcpName`, `commandPrefix`, `commandRegex`, `argsPattern`, `decision: allow | deny | ask_user`, `priority`, `modes`; tiers Default < Extension < Workspace < User < Admin. `ask_user` becomes `deny` when non-interactive. "Allow for all future sessions" persistence is scoped by the mode it was granted in [S23].
- **What we should take from this:** a declarative, prioritised rule file with tiers is the right shape for a *grant*: the host owner's tier must always outrank anything the guest or the project supplies.

### B.4 Cursor (3.6+, docs dated by version)

- Run modes: **Auto-review** (default since 3.6, 2026-05-29), **Allowlist**, **Run Everything**. Auto-review = allowlist → sandbox → LLM classifier; the docs say it "is not a security boundary". `permissions.json` takes plain-English `allow_instructions` / `block_instructions`; `sandbox.json` controls reach. Sandbox: Seatbelt on macOS, Landlock + user namespaces on Linux (kernel 6.2+). Extra protections that still prompt: file-deletion, external-file, browser [S20a].
- Cloud/background agent permission model: not found in the pages I read.
- **What we should take from this:** named "protections" for irreversible classes (delete, outside-workspace, browser) that survive every automatic mode. We need the same always-ask class in APPROVED TRUST.

### B.5 Cline / Roo Code

- Cline auto-approve categories: Read project files / Read all files / Edit project files / Edit all files / Execute safe commands / Execute all commands / Use the browser / Use MCP servers, plus OS notifications; a separate YOLO checkbox [S24]. Apache-2.0 [S39].
- Roo Code has the same category toggles with a per-category risk table (secondary search summary of official docs) [S24a]; **the Roo-Code repo is archived as of 2026-05** [S39].
- **What we should take from this:** category toggles with an inside/outside-project split are what users already understand; that is the natural "trust dial" granularity.

### B.6 Warp

- Per-action-type autonomy: "Agent Decides", "Always ask", "Always allow", "Never"; regex command allowlist and a denylist that always wins; team-enforced denylist cannot be bypassed; named profiles (e.g. a restrictive "Prod mode") [S26].
- **Agent session sharing:** share a live agent session with invited people, a team, or anyone with the link; viewers can **request edit access**, the sharer approves; editors can send agent queries and run commands. Goes through Warp's servers; no end-to-end encryption is mentioned; secret redaction is not applied to scrollback [S27].
- **What we should take from this:** the closest shipped precedent to our product. Copy the view → request-edit → approve escalation; do better on E2E and redaction.

### B.7 Amp

- `amp.permissions` rules: tool + `matches` + action **`allow | reject | ask | delegate`**; `delegate` hands the decision to an external program (exit 0 allow, 1 ask, ≥2 reject). Documented as the legacy format; a plugin API is now preferred [S25].
- **What we should take from this:** `delegate` is precisely our integration pattern — the agent defers the decision to an external authority (our daemon).

### B.8 GitHub Copilot coding agent, Devin, OpenHands

- **Copilot cloud agent:** runs in GitHub's environment behind a default-on firewall with a recommended + custom allowlist; blocked requests are surfaced as a warning in the PR; GitHub says the firewall is not a comprehensive security solution. A "mission control" agents panel shows session logs, lets you steer mid-run, and links each commit to its session log [S28].
- **Devin:** plan review via Interactive Planning; wait-for-approval is a setting; a human can stop and "take over" the shell/IDE/browser [S29].
- **OpenHands (MIT):** each tool call carries a `security_risk` label (LOW/MEDIUM/HIGH/UNKNOWN) supplied by the LLM; confirmation policy threshold default HIGH; `AlwaysConfirm` / `NeverConfirm`; ensemble analysers take the worst verdict [S29a].
- **What we should take from this:** commit-to-session-log linkage (Copilot) is a cheap, strong audit feature. Do **not** copy OpenHands' self-declared risk as a gate — the model that may be injected is grading its own action; use it only as a display hint.

### B.9 Common patterns

| Dimension | What the field converged on |
|---|---|
| Granularity | Per tool; per command prefix/regex; per path glob (inside vs outside workspace); per network domain; per MCP server/tool |
| Decision verbs | allow / ask / deny (+ `defer`, `delegate`) — deny always wins |
| Remember scope | once · this session · always for this project (Claude varies it by tool type; ACP has `allow_once/allow_always/reject_once/reject_always`) |
| Trust levels | 3–6 named modes from read-only/plan to bypass; mode switch mid-session |
| Automatic tier | OS sandbox + LLM reviewer for the residue; every vendor disclaims it as a boundary |
| Never-auto class | critical-path deletes, writes to agent config/hooks, outside-workspace writes, credentials |
| Pending-action display | tool name + human description + exact input (command or diff) |
| Interrupt/steer | Esc/stop, queued messages, "steer" at next step, take-over |
| Audit | session transcripts/logs; commit ↔ session links; little tamper-evidence anywhere |
| Admin override | managed settings / team denylist that local users and repos cannot loosen |

**Cross-user agent linking shipped by a vendor: not found.** Closest: Warp shared agent sessions (human guests), Claude Code cross-session messaging (same user), Copilot sessions visible to org collaborators.

---

## C. Open-source projects

| Project | What it is | Reusable for us | Licence (GitHub API, 2026-11-16) |
|---|---|---|---|
| **slopus/happy** | Mobile/web client for Claude Code & Codex via an E2E-encrypted relay; QR pairing with a one-time public key; relay stores only ciphertext and lets clients catch up after drops [S32] | The whole relay + pairing + encrypted-history pattern; closest architecture to ours (single-user). Permission approval from phone: not confirmed on the page read — UNVERIFIED | MIT, active |
| **anthropics/sandbox-runtime** | Seatbelt/bubblewrap wrapper with network proxy | Sandbox for the host-side agent process | Apache-2.0 |
| **agentclientprotocol/agent-client-protocol** + **claude-agent-acp** | ACP schema/SDKs; Claude adapter | Phase-2 adapter layer; event schema | Apache-2.0 |
| **BloopAI/vibe-kanban** | Kanban orchestration of many coding agents with diff review | Review/queue UX reference | Apache-2.0, active |
| **smtg-ai/claude-squad** | tmux + worktree manager for multiple terminal agents | Fleet UX reference only | **AGPL-3.0** — do not copy code |
| **stravu/crystal** (now Nimbalyst) | Parallel Claude/Codex sessions in worktrees | UX reference | MIT, stale since 2026-02 |
| **louislva/claude-peers-mcp** | Local broker letting Claude Codes message each other; uses Channels | Proof that MCP + channels works for peer chat | MIT, last push 2026-04 |
| **prassanna-ravishankar/repowire** | Mesh for Claude Code/OpenCode/Codex across machines | Cross-vendor peer messaging reference | no licence detected — do not reuse |
| **mcp_agent_mail** (+ Rust rewrite) | Mailbox + file "leases" for agents | Lease concept for file ownership | Python repo deprecated, licence NOASSERTION |
| **coder/agentapi** | HTTP API wrapping terminal agents | Adapter idea | MIT, **archived 2026-09** |
| **OpenHands** | Agent platform with confirmation mode | Risk-tier display | MIT |
| **LangGraph** | `interrupt()` pauses a graph, state persisted, resumed with `Command(resume=…)` [S33] | Durable pause/resume semantics for approvals | MIT |
| **AG2** (ex-AutoGen) | Multi-agent framework with human input modes (not verified this session) | — | Apache-2.0 |
| **CrewAI** | Multi-agent framework (human-input feature not verified this session) | — | MIT |
| **Conductor (Melty)** | Mac app for parallel Claude Codes | UNVERIFIED — not researched from a primary source; believed closed-source | — |

**What we should take from this:** Happy proves the relay-plus-E2E model works for coding agents at scale and is MIT — read its server and pairing code before writing ours. LangGraph's lesson is that an approval must be a *persisted* pause that survives a process restart, not an in-memory promise. Avoid AGPL (claude-squad, Teleport) and unlicensed code.

---

## D. Linking, pairing and transport

### D.1 Short-code PAKE pairing

- **Magic Wormhole:** a nameplate + words code feeds **SPAKE2**; a mailbox (rendezvous) server relays messages over WebSocket; a separate transit relay carries bulk data when direct connection fails. Default code has **16 bits of entropy → "one-in-65536"** per guess; a failed guess is visible to the user; an attacker controlling the network or the mailbox server can attempt exactly one man-in-the-middle guess per code; the server should refuse immediate nameplate reuse; DoS on the public mailbox has no good mitigation [S15]. Python impl MIT; Go `wormhole-william` MIT; Rust impl **EUPL-1.2** (copyleft) [S39].
- **SPAKE2** is RFC 9382 (Informational, Sept 2023), with mandatory key-confirmation MACs over the transcript [S16]. CPace/OPAQUE status not checked — UNVERIFIED.
- **What we should take from this:** the code must be the PAKE password, not a room name. One guess per code, short expiry, single use, visible failure. If our current 8-character code only selects a relay room and X25519 public keys are exchanged unauthenticated, the relay can MITM today — verify this first.

### D.2 Noise

- Noise rev 34 (2018-07-11): `XX` = mutual authentication with static keys sent encrypted; `IK` = initiator already knows responder's key (0-RTT); `psk` modifiers mix a 32-byte shared secret (e.g. `NNpsk0`, `XXpsk3`); the handshake hash can be exposed for channel binding; `Rekey()` for forward secrecy within a session [S17].
- **What we should take from this:** first contact = PAKE output as PSK into a Noise `XXpsk` handshake that also exchanges long-term static keys; reconnects = `IK`/`KK` with the pinned keys and no code. Derive the SAS from the handshake hash (my inference from §11.2 — the spec does not prescribe SAS).

### D.3 Device-code / QR

- Happy pairs by QR carrying a one-time public key [S32]; Claude Remote Control shows a URL/QR and relies on account login [S21]; A2A lists an OAuth device-code flow [S1]; Quick Assist uses a time-limited security code spoken over the phone [S34].
- **What we should take from this:** offer both a typed short code (strangers on a call) and a QR/link (same room or trusted chat). The code proves "the person I am talking to", nothing more.

### D.4 WebRTC vs relayed WebSocket vs iroh/libp2p

- Relayed outbound-only connections are what Claude Remote Control and Happy both chose — no inbound ports, works behind corporate firewalls [S21][S32]. VS Code Live Share tries P2P and falls back to a cloud relay, with SSH end-to-end encryption layered over TLS WebSockets so that "even if the relay was compromised, it could not decrypt" [S35].
- **iroh** 1.0 announced 2026-07-09 (wire format and API stable), current `v1.4.1`; QUIC, dial-by-public-key, hole punching with relay fallback, bindings for most languages. Apache-2.0 per the GitHub API [S18][S39]. The ~90% hole-punch figure is from secondary coverage — UNVERIFIED.
- **libp2p DCUtR** measured at ~70% (±7.1%) hole-punch success over 4.4M attempts, TCP ≈ QUIC [S18a].
- WebRTC data channels (DTLS/SCTP, ICE/STUN/TURN) — not researched from a primary source this session; UNVERIFIED general knowledge: workable in browsers but needs signalling plus TURN, i.e. a relay anyway.
- **What we should take from this:** our traffic is small JSON, not bulk data; P2P buys latency we do not need and costs NAT complexity. Stay on a content-blind WebSocket relay. If the console later streams large diffs or terminal output, iroh is the upgrade path (stable 1.x, permissive licence).

### D.5 Identity and peer verification

- Live Share: per-session host key pair published with the invitation; guest verifies the host holds the private key; guest identity is a signed token from a sign-in provider; host may additionally require approval [S35].
- Tailscale SSH "check mode" forces re-authentication with a default 12-hour check period (official docs via search summary) [S36]. Tailscale's identity model otherwise not researched — UNVERIFIED.
- **What we should take from this:** three layers — (1) PAKE code binds the first session, (2) a displayed SAS both humans can read aloud catches a relay MITM, (3) pinned identity keys make later sessions "known peer" vs "new peer" with a loud warning on key change (SSH `known_hosts` behaviour).

### D.6 MLS for more than two parties

- MLS is RFC 9420 (July 2023), architecture in RFC 9750 [S17a]; OpenMLS is MIT [S39]; AGNTCY SLIM uses MLS under agent protocols [S13].
- **What we should take from this:** design the envelope so the key schedule is swappable; do not implement MLS until a third party (e.g. an auditor observer) is a real requirement.

### D.7 Reconnection and resumption

- MCP 2026-07-28 *removed* stream resumability: a broken stream loses the in-flight request and the client must re-issue it [S2]. Claude Code holds messages for offline peers and delivers on reconnect; approval dialogs expire (default five minutes) and the message is dropped [S9][S21]. Happy's relay stores encrypted history for catch-up [S32].
- **What we should take from this:** make every cross-party request idempotent with a client-generated ID; the relay stores ciphertext with sequence numbers for a bounded window; pending approvals survive reconnect but **expire to deny**.

### D.8 Recommendation for a small team

1. Keep the WebSocket relay; make it provably content-blind (ciphertext + routing ID only).
2. Replace the handshake: short one-time code → SPAKE2 → Noise `XXpsk` exchanging long-term Ed25519/X25519 identities; show a 6-digit or word SAS; pin peers.
3. Sequence-numbered, idempotent messages; relay buffers N minutes of ciphertext; approvals expire to deny.
4. Use audited libraries (a maintained SPAKE2 and Noise implementation) — do not hand-roll beyond composition. Get the composition reviewed.
5. Defer P2P (iroh) and group keys (MLS) until a concrete need.

---

## E. Remote-support and shared-terminal precedents

| Product | Consent / oversight model | Source |
|---|---|---|
| **Windows Quick Assist** | Helper generates a time-limited security code; sharer enters it; sharer gets an **Allow** dialog for screen view; helper must separately **Request control**, sharer gets Allow/Deny; helper has the sharer's permissions except UAC prompts; sharer sees only helper's first name + initial; no local logs. Microsoft's own page leads with tech-support-scam warnings | [S34] |
| **VS Code Live Share** | Host is notified of every join with a **Remove** button; `liveshare.guestApprovalRequired`; anonymous guests are read-only and prompt by default (`liveshare.anonymousGuestApproval`); read-only sessions; `.vsls.json` `excludeFiles` / `hideFiles`; only the host can start a shared terminal and chooses read-only vs read/write (VS Code auto-shares terminals read-only); shared servers are explicit per port; co-debugging warned as command-execution risk | [S35] |
| **Teleport** | Participant modes `observer` (default), `peer`, `moderator` (can terminate; Enterprise). `require_session_join` with `count`, `modes`, and `on_leave: terminate | pause` — a session will not start until the required moderators join and pauses or dies when they leave. With per-session MFA, moderators re-confirm presence every 30 s. Just-in-time Access Requests with reviewers and `max_duration` (≤ 14 days). AGPL-3.0 | [S37][S36] |
| **Warp** | View → request edit → sharer approves; stop-share ends access immediately; share expires in a week | [S27] |
| **AnyDesk** | Without unattended access, a person must accept each connection in an accept window; permission profiles define what the remote user may do (search summary of official docs) | [S36a] |
| **TeamViewer, tmate** | Not verified from primary sources this session — UNVERIFIED. (tmate is commonly described as issuing separate read-only and read-write session strings.) | — |

**Patterns to copy**

- **Two-step escalation:** observing is one consent, acting is a second, explicit one (Quick Assist, Warp).
- **Presence-bound sessions:** the session pauses when the overseer is absent (`on_leave: pause`) — the right semantic for CONTROLLED mode when the host owner walks away.
- **Host-only origination of power:** only the host creates writable surfaces (Live Share terminals, shared ports); the guest can never mint capability.
- **Exclusion lists that beat everything:** `.vsls.json`-style excluded paths that are invisible even when the agent "follows" into them.
- **Always-visible indicator and one-click eject** on the host side; revocation takes effect immediately.
- **Time-boxed grants** with a hard ceiling and reviewer-adjustable start/end (Teleport).
- **Anti-scam framing at pairing time:** state who initiated, never auto-accept, show the peer's verified identity. Quick Assist is the cautionary tale: a code-based support tool becomes a social-engineering tool if the consent screen is weak.

---

## F. Security model

### F.1 The threat in one paragraph

Text authored by another person's agent arrives at a local agent that has file, shell and network tools. That is prompt injection by construction. Willison's lethal trifecta — private data + untrusted content + external communication — is fully present [S30]; Meta's Agents Rule of Two says an agent holding all three of [A] untrustworthy input, [B] sensitive access, [C] state change/external communication must not run autonomously and needs human approval or equivalent validation [S31]. OWASP's Top 10 for Agentic Applications (dated 2025-12-09) names the same risks: ASI01 Agent Goal Hijack, ASI02 Tool Misuse and Exploitation, ASI03 Identity and Privilege Abuse, ASI07 Insecure Inter-Agent Communication, ASI09 Human-Agent Trust Exploitation (list titles from a secondary source; OWASP page confirmed title and date only) [S41].

### F.2 Capability grants (least privilege)

- Express every permission as a **grant object** the host owner signs: `{scope: paths[], commands[], domains[], tools[]; mode: ask|auto; expires_at; max_actions; revocable}`. Prior art for each field: Claude rule specifiers and working directories [S5], Codex writable roots and domain rules [S19], Gemini policy tiers [S23], Teleport time-boxed requests [S37].
- Grants are evaluated by a **deterministic policy engine outside the model** — hook/`canUseTool`/ACP client — never by instructing the agent. Anthropic's own wording: boundaries stated in conversation "live in the transcript, not as stored rules… Use a deny rule for a hard guarantee" [S6].
- The guest never holds a credential for the host machine. The guest holds a session key that lets it *send requests*; the host daemon decides.
- **Confused-deputy guard:** MCP forbids token passthrough and requires audience-bound tokens [S12]; equivalent rule for us — the host agent must never act with authority the guest's request merely *claims*, and approvals are bound to the exact action hash, not to a description.

### F.3 OS sandboxing options

| OS | Mechanism | Used by |
|---|---|---|
| macOS | Seatbelt (`sandbox-exec`) | Claude Code, Codex, Cursor [S20][S19][S20a] |
| Linux / WSL2 | bubblewrap + seccomp; or Landlock + user namespaces (kernel 6.2+) | Claude Code & Codex (bwrap); Cursor (Landlock) |
| Windows | Claude Code: none natively (use WSL2). Codex: a Windows sandbox the docs call MXC (verify) | [S20][S19] |
| Any | Container / VM / devcontainer | The only setting Anthropic recommends for `bypassPermissions` [S6] |

Limits to design around: in Claude Code the built-in file tools, MCP servers and hooks run *outside* the Bash sandbox; reads are broad by default (including `~/.ssh`) unless denied; environment variables are inherited [S20]. For third-party hosts (audit/troubleshooting use cases) the default should be a read-only grant with `denyRead` on credential paths, and a container or throwaway worktree for anything that writes.

### F.4 Prompt-injection mitigations that hold up

1. **Remote content is data.** Deliver guest messages in a labelled envelope the host agent is told is from another party; strip/neutralise control and bidi characters as Claude Code does for relayed permission previews [S10].
2. **Remote text can never be consent.** Hard rule, enforced in code [S9].
3. **Policy outside the model**, deny wins, admin tier outranks all (F.2).
4. **The approval shows the real action**, not the agent's summary: Claude's channel docs warn that `description` may be only "Run shell command" and tell implementers to render `input_preview` [S10].
5. **Dual-approval / always-ask classes** irrespective of trust level: credential reads, writes to agent config/hooks/`.git/hooks`, outside-scope writes, network egress to new domains, destructive deletes, privilege changes (cf. Cursor protections, Claude critical paths, Codex protected paths) [S20a][S6][S19].
6. **Break the trifecta where possible:** in audit mode grant read without network egress; in config mode grant write without access to secrets.
7. **Classifier as a helper only**, never fed raw tool results (Anthropic strips them) [S6]; fail closed on timeout (Codex) [S19].
8. **Structural defences** (DeepMind's CaMeL — separate planner from quarantined reader, capability-tracked data flow) exist in research; noted from secondary sources only, UNVERIFIED [S42].
9. **Rate and loop limits** on cross-agent messages (Claude Code throttles per sender and drops identical repeats) [S9].

### F.5 Tamper-evident audit

- No coding-agent vendor reviewed here documents a tamper-evident log; Copilot links commits to session logs [S28], Quick Assist keeps none [S34].
- Standard construction (transparency-log literature): append-only hash chain or Merkle tree, periodically signed tree heads, optional independent witnesses to prevent split views [S43].
- **What we should take from this:** both parties already share an authenticated channel — make each side sign every event (request, approval, denial, action result hash) and chain it to the previous event hash. Each party keeps a copy; either can later prove what was requested and what was approved. This is cheap, and for the security-audit use case it is a differentiator.

---

## G. UX patterns for the oversight console

| Pattern | Who does it well | Detail to copy | Pitfall |
|---|---|---|---|
| **Diff review surface** | Zed: "Review Changes" opens one multi-buffer with every edit, accept/reject per hunk or all [S44]; Claude Code web: Changes card `+42 -18`, inline line comments sent back to the agent, compare against a branch [S22] | One aggregated diff view, per-hunk decisions, comments that become instructions | Claude web diff misses changes made by commands until pushed [S22] — show filesystem truth, not only tool-reported edits |
| **Follow the agent** | Zed crosshair "follow" jumps to each file the agent touches [S44]; ACP `locations` standardise it [S3]; Live Share follow mode | A toggle, off-able, that never opens excluded paths | Following into secrets — honour exclusions (Live Share `excludeFiles`) [S35] |
| **Approval prompt** | Claude Code: what will run + options + optional comment when answering [S5]; ACP four option kinds [S3] | Exact command/diff, scope of "remember" spelled out in the button label | Approval fatigue — Anthropic documents prompts "create friction" and recommends pre-approval [S8a] |
| **Approval queue + batching** | Agent teams: teammates' prompts bubble to one place [S8a]; Codex statuses Reviewing/Approved/Denied/Aborted/Timed out [S19] | A queue with states, grouped by kind, "approve all reads in this folder" as a generated grant | Batching must never include the always-ask class |
| **Risk tiers** | OpenHands LOW/MEDIUM/HIGH/UNKNOWN [S29a]; Codex low/medium/high/critical [S19]; Roo risk table [S24a] | Colour + default action by tier; UNKNOWN treated as high | Model-self-reported risk as a gate |
| **Activity timeline** | Copilot session log with progress, tokens, duration; commits link to logs [S28] | One chronological stream: message → proposed action → decision → result | Logs-only UIs hide the diff; pair timeline with the main pane |
| **Pause / interrupt / steer** | Zed: queued messages, "Steer" delivers at next step, stop button [S44]; Devin: pause before taking over [S29]; Teleport `on_leave: pause` [S37] | Three distinct controls: **Pause** (finish current step, hold), **Stop** (abort turn), **Revoke** (end grant, drop link) | One overloaded "stop" button |
| **Trust dial** | Claude modes cycle with Shift+Tab [S6]; Cline category toggles [S24]; Warp profiles incl. "Prod mode" [S26] | A visible, always-reachable dial with 3–4 named positions and a per-category breakdown underneath | Hidden mode state — Anthropic had to document cases where the status bar shows one mode and behaviour follows another [S8a] |
| **Remote approval** | Claude Remote Control push "when actions required" [S21]; channel relay with short request IDs [S10] | Phone push for pending approvals with first-answer-wins | Approving from a notification without seeing the command |
| **Presence & indicator** | Live Share join notification + Remove [S35]; Warp avatars/cursors [S27] | Persistent banner: who is linked, their verified key name, current mode, time left | Silent background sessions |

**Layout verdict on the proposed UI** (chat bottom, main pane for changing code, approvals + history right): it matches the Zed agent panel + review multibuffer and the Claude web "session rail" arrangement. Two additions the precedents argue for: a **persistent top status strip** (peer identity, mode, grant expiry, Pause/Revoke) and a **timeline tab** in the right rail that is the signed audit log rendered for humans.

---

## Recommended approach (synthesis)

**Phase 1 — two Claude Codes**
- Host side: our daemon launches or attaches to Claude Code and gates every action through `PreToolUse` (HTTP hook) and/or `canUseTool`; console renders the queue. Guest messages reach the host agent as labelled data via our existing MCP tools. Guest side: MCP server only.
- CONTROLLED = `default` mode + every non-read action to the queue. APPROVED TRUST = signed grant → generated allow-rules + sandbox + classifier, with an always-ask class and presence-aware pause.
- Transport: current relay, new PAKE + Noise handshake, SAS, pinned identities, signed hash-chained event log.
- Internal event schema modelled on ACP tool-call/permission types and A2A task states.

**Phase 2 — agent-agnostic**
- Host daemon becomes an **ACP client**; any ACP agent plugs in. Guest side stays MCP. Optional A2A gateway for server-hosted agents. MLS only if multi-party.

---

## Open questions surfaced by the research

1. Does the prototype's 8-character code authenticate the X25519 exchange, or only name a relay room? (Determines whether the relay can MITM today.)
2. Which current adapter gives Codex CLI ACP support now that `zed-industries/codex-acp` is archived?
3. Is depending on `--dangerously-load-development-channels` acceptable for any phase-1 feature, or do we stay on plain MCP tools + hooks?
4. Windows hosts: no native Claude Code sandbox — is WSL2-only acceptable for phase 1?
5. Legal/consent: do we need a recorded, signed consent artefact per session for the security-audit use case?

---

## Sources (all accessed 2026-11-16)

- **[S1]** A2A Protocol Specification (shows v1.0.0 as latest released) — https://a2a-protocol.org/latest/specification/
- **[S2]** MCP specification changelog, revision 2026-07-28 — https://modelcontextprotocol.io/specification/latest/changelog
- **[S3]** Agent Client Protocol: tool calls & permissions — https://agentclientprotocol.com/protocol/tool-calls ; introduction — https://agentclientprotocol.com/overview/introduction
- **[S4]** ACP agents list — https://agentclientprotocol.com/overview/agents
- **[S5]** Claude Code: Configure permissions — https://code.claude.com/docs/en/permissions
- **[S5a]** Claude Code: Hooks reference — https://code.claude.com/docs/en/hooks
- **[S6]** Claude Code: Permission modes / auto mode — https://code.claude.com/docs/en/permission-modes
- **[S7]** Claude Agent SDK: Configure permissions — https://code.claude.com/docs/en/agent-sdk/permissions
- **[S8]** Claude Agent SDK: Handle approvals and user input (`canUseTool`) — https://code.claude.com/docs/en/agent-sdk/user-input
- **[S8a]** Claude Code: Agent teams — https://code.claude.com/docs/en/agent-teams
- **[S9]** Claude Code: Cross-session messaging — https://code.claude.com/docs/en/cross-session-messaging
- **[S10]** Claude Code: Channels reference (research preview) — https://code.claude.com/docs/en/channels-reference
- **[S11]** MCP 2026-07-28: Elicitation — https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation
- **[S12]** MCP 2026-07-28: Authorization — https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
- **[S13]** Secondary coverage of IBM ACP → A2A merge and AGNTCY (UNVERIFIED): https://rywalker.com/research/acp-agent-communication-protocol ; https://rywalker.com/research/agntcy ; SLIM draft https://spec.slim.agntcy.org/draft-mpsb-agntcy-slim.html ; https://docs.agntcy.org
- **[S14]** AAIF blog: A2A joins AAIF — https://aaif.io/blog/a2a-joins-aaif (via search summary)
- **[S15]** Magic Wormhole: Known attacks — https://magic-wormhole.readthedocs.io/en/latest/attacks.html
- **[S16]** RFC 9382, SPAKE2 — https://www.rfc-editor.org/rfc/rfc9382.html
- **[S17]** Noise Protocol Framework, revision 34 — https://noiseprotocol.org/noise.html
- **[S17a]** RFC 9420 (MLS) — https://www.rfc-editor.org/rfc/rfc9420.txt (via search summary)
- **[S18]** iroh: The road to iroh 1.0 (2026-07-09) — https://iroh.computer/blog/the-road-to-iroh-1-0
- **[S18a]** Trautwein et al., "Challenging Tribal Knowledge — Large Scale Measurement Campaign on Decentralized NAT Traversal", arXiv:2510.27500 — https://arxiv.org/abs/2510.27500
- **[S19]** OpenAI Codex: Agent approvals & security — https://learn.chatgpt.com/docs/agent-approvals-security.md (redirect from developers.openai.com/codex/agent-approvals-security)
- **[S20]** Claude Code: Sandboxing — https://code.claude.com/docs/en/sandboxing
- **[S20a]** Cursor: Run modes — https://cursor.com/docs/agent/security/run-modes
- **[S21]** Claude Code: Remote Control — https://code.claude.com/docs/en/remote-control
- **[S22]** Claude Code in the cloud (share sessions, review changes) — https://code.claude.com/docs/en/claude-code-on-the-web
- **[S23]** Gemini CLI: Policy engine — https://geminicli.com/docs/reference/policy-engine.md
- **[S24]** Cline: Auto-approve — https://docs.cline.bot/features/auto-approve.md
- **[S24a]** Roo Code: Auto-approving actions — https://docs.roocode.com/features/auto-approving-actions (via search summary)
- **[S25]** Amp: permissions — https://ampcode.com/manual/appendix/legacy-permissions-rules.txt ; https://ampcode.com/news/tool-level-permissions (via search summary)
- **[S26]** Warp: Agent profiles & permissions — https://docs.warp.dev/agent-platform/capabilities/agent-profiles-permissions (via search summary)
- **[S27]** Warp: Agent session sharing — https://docs.warp.dev/agent-platform/warp-agents/session-sharing
- **[S28]** GitHub Copilot: agent firewall — https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/customize-the-agent-firewall ; tracking sessions — https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/track-copilot-sessions (via search summaries)
- **[S29]** Devin: session tools — https://docs.devin.ai/work-with-devin/devin-session-tools ; interactive planning — https://docs.devin.ai/work-with-devin/interactive-planning.md (via search summary)
- **[S29a]** OpenHands SDK: security — https://docs.openhands.dev/sdk/guides/security ; https://docs.openhands.dev/sdk/arch/security (via search summary)
- **[S30]** Simon Willison, "The lethal trifecta for AI agents" (2025-06-16) — https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
- **[S31]** Meta AI, "Agents Rule of Two: A Practical Approach to AI Agent Security" (2025-10-31) — https://ai.meta.com/blog/practical-ai-agent-security/
- **[S32]** Happy: How it works — https://happy.engineering/docs/how-it-works/ ; repo https://github.com/slopus/happy
- **[S33]** LangGraph: Interrupts — https://docs.langchain.com/oss/python/langgraph/interrupts (via search summary)
- **[S34]** Microsoft: Use Quick Assist to help users (updated 2025-09-30) — https://learn.microsoft.com/en-us/windows/client-management/client-tools/quick-assist
- **[S35]** Microsoft: Live Share security (doc dated 2022, updated 2023-06-30) — https://learn.microsoft.com/en-us/visualstudio/liveshare/reference/security
- **[S36]** Tailscale SSH / session recording — https://tailscale.com/docs/features/tailscale-ssh ; Teleport access request configuration — https://goteleport.com/docs/identity-governance/access-requests/access-request-configuration/ (both via search summary)
- **[S36a]** AnyDesk: unattended access / permission profiles — https://support.anydesk.com/docs/unattended-access.md (via search summary)
- **[S37]** Teleport: Joining sessions / moderated sessions — https://goteleport.com/docs/zero-trust-access/authentication/joining-sessions.md
- **[S38]** Community peer-messaging projects: https://github.com/louislva/claude-peers-mcp ; https://pypi.org/project/repowire/ ; https://glama.ai/mcp/servers/pouriamrt/claude-mesh ; https://github.com/Dicklesworthstone/mcp_agent_mail
- **[S39]** GitHub REST API repository and release metadata (licence, stars, pushed_at, archived, tags) for the repositories named in this report — https://api.github.com/repos/{owner}/{repo}
- **[S40]** Codex app-server approval flow (community notes, UNVERIFIED) — https://scrapbox.io/mrsekut-p/codex-app-server ; https://openai.com/index/unlocking-the-codex-harness
- **[S41]** OWASP Top 10 for Agentic Applications for 2026 (2025-12-09) — https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ ; item titles from https://www.giskard.ai/knowledge/owasp-top-10-for-agentic-application-2026
- **[S42]** CaMeL, "Defeating Prompt Injections by Design" (arXiv:2503.18813) — secondary summaries only, UNVERIFIED — https://simonw.substack.com/p/camel-offers-a-promising-new-direction
- **[S43]** Verifiable data structures / transparency logs — https://transparency.dev/verifiable-data-structures/ (via search summary)
- **[S44]** Zed: Agent panel — https://zed.dev/docs/ai/agent-panel ; External agents — https://zed.dev/docs/ai/external-agents
